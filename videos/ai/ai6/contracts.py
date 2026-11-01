"""Part 6 data and score contracts; no loaders, models or production jobs."""
from __future__ import annotations

import math
import os
import hashlib
import json
import platform
import sys

import numpy as np

BOOK_IDS = (1342, 158, 98, 1400, 46)
N_WORDS = 70
FOLDS = 10
BOARD_CASES = {
    "ls": (2, 70), "lasso": (70,), "lr": (2, 70), "nb": (70,),
    "lda": (2, 70), "knn": (2, 70), "svm_lin": (2, 70), "svm_rbf": (2, 70),
    "tree": (2, 70), "forest": (2, 70), "ada": (2, 70), "xgb": (2, 70),
}


def content_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     default=float, allow_nan=False).encode()).hexdigest()


def benchmark_protocol():
    """The declared transductive lexicon is distinct from classifier fitting."""
    return dict(book_ids=list(BOOK_IDS), page_words=1000, vocabulary_size=N_WORDS,
                vocabulary_fit="all five novels, including evaluation pages",
                transductive_vocabulary=True, split_unit="nonoverlapping 1000-word page",
                split_seed=1964, split="author-stratified 70/30 page split",
                evaluation_scope="unseen pages within these same five novels; not unseen novels",
                standardization="respective training split or fold only", plot=["the", "not"])


def runtime_identity():
    """Observed numeric runtime, without importing a model or inspecting credentials."""
    return dict(python=platform.python_version(), implementation=platform.python_implementation(),
                numpy=np.__version__, machine=platform.machine(), byteorder=sys.byteorder,
                numeric_thread_environment={k: os.environ.get(k) for k in
                                            ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")})


def score_summary(logits, labels, probabilities, bins=10):
    """Reliability/Brier from probabilities; uncapped log loss from OOF logits.

    The old probability floor is counted only as a diagnostic. It never alters
    the score, including saturated sigmoid outputs at finite extreme logits.
    """
    z, y, p = (np.asarray(a, dtype=float) for a in (logits, labels, probabilities))
    if (z.ndim != 1 or not len(z) or y.shape != z.shape or p.shape != z.shape
            or not all(np.isfinite(a).all() for a in (z, y, p))
            or not np.isin(y, [0, 1]).all() or np.any((p < 0) | (p > 1))
            or type(bins) is not int or bins < 1):
        raise ValueError("finite matching logits/binary labels/probabilities and positive bins required")
    expected = .5 * (1 + np.tanh(.5 * z))
    if not np.allclose(p, expected, rtol=1e-12, atol=1e-14):
        raise ValueError("probabilities do not match the supplied OOF logits")
    k = np.digitize(p, np.linspace(0, 1, bins + 1)[1:-1])
    count = np.bincount(k, minlength=bins).astype(float)
    conf = np.bincount(k, weights=p, minlength=bins) / np.maximum(count, 1)
    frac = np.bincount(k, weights=y, minlength=bins) / np.maximum(count, 1)
    losses = np.logaddexp(0, np.where(y == 1, -z, z))
    floor = 1e-12
    threshold = math.log1p(-floor) - math.log(floor)
    return dict(count=count, conf=conf, frac=frac,
                ece=float((count * np.abs(conf - frac)).sum() / len(y)),
                brier=float(np.mean((p - y) ** 2)), logloss=float(losses.mean()),
                score=dict(definition="mean binary log loss from stored out-of-fold logits",
                           unit="nats per page", probability_clip=None,
                           old_probability_floor=floor,
                           rows_beyond_old_probability_floor=int(np.sum(np.abs(z) > threshold)),
                           wrong_label_losses_above_old_cap=int(np.sum(losses > -math.log(floor))),
                           n_pages=len(y)))


def finite_tree(value):
    """Reject nonfinite numeric leaves/object arrays, retaining meaningful None/string fields."""
    if isinstance(value, dict):
        return all(isinstance(k, (str, int)) and finite_tree(v) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return all(finite_tree(v) for v in value)
    if isinstance(value, np.ndarray):
        return value.dtype.kind in "biuf" and bool(np.isfinite(value).all())
    if isinstance(value, (float, np.floating)):
        return math.isfinite(float(value))
    return value is None or isinstance(value, (str, bool, int, np.integer, np.bool_))


def array(value, shape=None, *, ndim=None, low=-math.inf, high=math.inf):
    try:
        a = np.asarray(value)
        return bool(a.dtype.kind in "biuf" and (shape is None or a.shape == shape)
                    and (ndim is None or a.ndim == ndim) and np.isfinite(a).all()
                    and (a >= low).all() and (a <= high).all())
    except (TypeError, ValueError):
        return False


def integer(value, low=0):
    return isinstance(value, (int, np.integer)) and not isinstance(value, (bool, np.bool_)) and value >= low


def board_piece(piece, folds=FOLDS):
    """A cached row must agree with its actual fold scores; no preferred winner."""
    if not isinstance(piece, dict) or not set("cv sd lo hi folds held".split()) <= piece.keys():
        return False
    if not finite_tree(piece) or not array(piece["folds"], (folds,), low=0, high=1):
        return False
    a = np.asarray(piece["folds"], float)
    return bool(array(piece["held"], (), low=0, high=1)
                and np.allclose([piece["cv"], piece["sd"], piece["lo"], piece["hi"]],
                                [a.mean(), a.std(ddof=1), a.min(), a.max()], rtol=1e-10, atol=1e-12))


def bagging_piece(piece):
    return (isinstance(piece, dict) and set("s2 cov rho meas acc".split()) <= piece.keys()
            and finite_tree(piece) and array(piece["s2"], (), low=0)
            and array(piece["cov"], ()) and array(piece["rho"], (), low=-1, high=1)
            and array(piece["meas"], (8,), low=0) and array(piece["acc"], (8,), low=0, high=1))


REQUIRED = {
    "pages": "vocab X y book test plot X2 example example_label example_i n_pages n_austen n_dickens titles protocol",
    "zipf": "words f r beta r2 n_words",
    "gaussmarkov": "x beta R w_ols w_end w_mix theory gauss t3 hist_bins hist_ols hist_end hist_ts samples",
    "lsq": "kappa_A kappa_AtA diff_ne_qr diff_qr_pinv acc_train acc_test rank_dup cols_dup smin_dup w_not w_not_a w_not_b same_fit ne_dup",
    "ridge": "d lams shows shrink df uy cv_mse cv_mse_se cv_acc cv_acc_sd best one_se lam_best test_acc coef d_ratio",
    "lasso": "twin_lasso twin_enet twin_corr k8 acc8 words8 lams lam_max path nnz sweeps kkt order test_acc cv_mse cv_se cv_acc cv_acc_sd best one_se selected n_selected acc_one_se acc_best epath enet_nnz pair pair_idx pair_corr",
    "logistic": "w b acc2 acc70 xs ys prob loss_bits path curve hess_eig n_te",
    "irls": "newton_gap n_newton gd fstar l2 lines_newton lines_gd pens norms train_acc losses separable acc_test gd_iters_to cond_H",
    "calibration": "lr2 lr70 nb nb_platt acc nb_z nb_extreme nb_median_abs_z p_lr2 p_lr70 p_nb p_nb_platt z_lr2 z_lr70 z_nb z_nb_platt fold_ids evaluation",
    "nbvslr": "sizes nb lr nb_better_at crossover nb_bias nb_austen nb_dickens",
    "lda": "w c angles sep best acc2 mA mD SB SW covA covD eigvals cos_eig rq cos_ls acc70 top top_signs rank_SB",
    "knn": "xs ys ks cv cv_sd k_cv acc_kcv",
    "coverhart": "mu Rstar lim1 bound ns e1 ek",
    "curse": "dims contrast nn_frac noise knn lr edge",
    "kernel": "lift_w lift_b lift_sv lift_sep poly_err ev2 ev70 ev_sig min_ev2 min_ev70 min_sig n_neg_sig n taylor_err rep_err rep_resid rep_dims krr_acc xor_mistakes_100 xor_lift_mistakes xor_lift_epochs",
    "svm": "toy_w toy_b toy_sv toy_margin toy_alpha toy_sum_at perc_mistakes perc_bound perc_w xs ys mu sd Cs gammas kkt cv cv_sd C_cv g_cv acc_cv2 acc70_lin n_sv70_lin acc70_rbf n_sv70_rbf n_train",
    "trees": "box depths tree3 acc_deep2 train_deep2 rects_deep acc_tree70 cv cv_sd boot_roots boot_acc",
    "bagging": "syn syn_B mf70 mf8 mf2 Bm Rs T m forest_acc forest_oob bag_acc one_tree",
    "adaboost": "xs ys alpha_check snaps first_words",
    "xgb": "check_gain check_direct check_true check_word check_thr check_G check_H xs ys snaps lam eta depth T",
    "metrics": "lr2 lr70 nb rare roc_rare pr_rare split_acc cv_acc fold_acc",
    "board": "rows n folds fold_ids evaluation",
}

# These fields are produced as top-level arrays, so absence of the NPZ cannot
# masquerade as a complete JSON-only item. Additional arrays are manifested too.
REQUIRED_ARRAYS = {
    "pages": "X y book test X2", "zipf": "f r beta",
    "gaussmarkov": "x w_ols w_end w_mix hist_bins hist_ols hist_end hist_ts samples",
    "ridge": "d lams df uy cv_mse cv_mse_se cv_acc cv_acc_sd test_acc coef",
    "lasso": "twin_lasso twin_enet lams path nnz test_acc cv_mse cv_se cv_acc cv_acc_sd epath enet_nnz",
    "logistic": "w xs ys prob path curve hess_eig", "irls": "gd",
    "calibration": "nb_z p_lr2 p_lr70 p_nb p_nb_platt z_lr2 z_lr70 z_nb z_nb_platt fold_ids",
    "lda": "w angles sep mA mD SB SW covA covD eigvals", "knn": "xs ys cv cv_sd",
    "kernel": "lift_w lift_sv ev2 ev70 ev_sig",
    "svm": "toy_w toy_sv toy_alpha perc_w xs ys mu sd cv cv_sd",
    "trees": "cv cv_sd", "adaboost": "xs ys", "xgb": "xs ys",
    "metrics": "roc_lr2 pr_lr2 roc_lr70 pr_lr70 roc_nb pr_nb roc_rare pr_rare",
    "board": "fold_ids",
}


def required_arrays(name, data):
    """Include dynamic fields consumed by scenes, not just a minimal NPZ marker."""
    keys = set(REQUIRED_ARRAYS.get(name, "").split())
    if name == "knn":
        keys.update(f"region{k}" for k in data["ks"])
    elif name == "svm":
        keys.update(f"{prefix}_C{c:g}" for c in data["Cs"] for prefix in ("region", "alpha", "sv"))
        keys.update(f"region_g{g:g}" for g in data["gammas"])
    elif name == "trees":
        keys.update(f"scan_{word}_{kind}" for word in ("not", "the") for kind in ("t", "gini", "entropy", "error"))
    elif name in ("adaboost", "xgb"):
        keys.update(f"region{k}" for k in data["snaps"])
        if name == "adaboost":
            keys.update(f"w{k}" for k in data["snaps"])
    return keys


def valid_structure(name, d, cohort=None):
    """Required consumed fields, numeric domains and bounded shape/cohort checks.

    This validates cache integrity and reporting structure, not every scientific
    conclusion or an undocumented legacy payload's original consumed lineage.
    """
    if (name not in REQUIRED or not isinstance(d, dict)
            or not set(REQUIRED[name].split()) <= d.keys() or not finite_tree(d)):
        return False
    try:
        n = cohort.get("n_pages") if cohort else None
        nt = cohort.get("n_train") if cohort else None
        if name == "pages":
            n = d["n_pages"]
            if not (integer(n, 2) and len(d["vocab"]) == len(set(d["vocab"])) == N_WORDS
                    and all(isinstance(w, str) and w for w in d["vocab"])
                    and set(["the", "not"]) <= set(d["vocab"])
                    and d["protocol"] == benchmark_protocol() and d["plot"] == ["the", "not"]
                    and array(d["X"], (n, N_WORDS), low=0, high=1000)
                    and array(d["X2"], (n, 2), low=0, high=1000)
                    and array(d["y"], (n,), low=0, high=1)
                    and np.asarray(d["y"]).dtype.kind in "iu"
                    and np.asarray(d["book"]).shape == (n,)
                    and np.asarray(d["book"]).dtype.kind in "iu"
                    and np.asarray(d["test"]).shape == (n,) and np.asarray(d["test"]).dtype.kind == "b"):
                return False
            y, test, book = (np.asarray(d[k]) for k in ("y", "test", "book"))
            return bool(set(map(int, book)) == set(BOOK_IDS)
                        and np.array_equal(y, np.isin(book, BOOK_IDS[2:]).astype(int))
                        and np.array_equal(d["X2"], np.asarray(d["X"])[:, [d["vocab"].index(w) for w in d["plot"]]])
                        and np.all(np.asarray(d["X"]).sum(1) <= 1000)
                        and d["n_austen"] == int(np.sum(y == 0))
                        and d["n_dickens"] == int(np.sum(y == 1))
                        and all(np.any(test & (y == k)) and np.any(~test & (y == k)) for k in (0, 1))
                        and integer(d["example_i"]) and d["example_i"] < n and test[d["example_i"]]
                        and d["example_label"] == y[d["example_i"]] and isinstance(d["example"], str))
        if name == "zipf":
            m = len(d["f"])
            return array(d["f"], (m,), low=1) and array(d["r"], (m,), low=1) and array(d["beta"], (2,)) and integer(d["n_words"], 1)
        if name == "gaussmarkov":
            m = len(d["x"])
            return (array(d["x"], (m,)) and all(array(d[k], (m,)) for k in ("w_ols", "w_end", "w_mix"))
                    and array(d["samples"], (6, m)) and all(array(d[k], (len(d["hist_bins"]) - 1,), low=0) for k in ("hist_ols", "hist_end", "hist_ts")))
        if name == "lsq":
            return array(d["acc_train"], (), low=0, high=1) and array(d["acc_test"], (), low=0, high=1) and d["ne_dup"] in ("solved", "singular")
        if name in ("ridge", "lasso"):
            m = len(d["lams"])
            vectors = ("df", "uy", "cv_mse", "cv_mse_se", "cv_acc", "cv_acc_sd", "test_acc") if name == "ridge" else ("nnz", "sweeps", "cv_mse", "cv_se", "cv_acc", "cv_acc_sd", "test_acc", "enet_nnz")
            # Ridge uy has one entry per direction, not per lambda.
            if not all(array(d[k], (N_WORDS if k == "uy" else m,)) for k in vectors):
                return False
            if not all(integer(d[k]) and d[k] < m for k in ("best", "one_se")):
                return False
            fields = ("coef",) if name == "ridge" else ("path", "epath")
            return (all(array(d[k], (m, N_WORDS)) for k in fields)
                    and (array(d["d"], (N_WORDS,), low=0) if name == "ridge" else
                         array(d["twin_lasso"], (m, 2)) and array(d["twin_enet"], (m, 2))))
        if name == "logistic":
            return (array(d["w"], (2,)) and array(d["prob"], (len(d["ys"]), len(d["xs"])), low=0, high=1)
                    and array(d["path"], ndim=2) and np.asarray(d["path"]).shape[1] == 5
                    and array(d["curve"], ndim=2) and np.asarray(d["curve"]).shape[1] == 2
                    and array(d["hess_eig"], (3,), low=0)
                    and all(array(d[k], (), low=0, high=1) for k in ("acc2", "acc70"))
                    and (cohort is None or d["n_te"] == cohort["n_test"]))
        if name == "irls":
            return (array(d["gd"], ndim=2) and np.asarray(d["gd"]).shape[1] == 2
                    and array(d["lines_newton"], (7, 4)) and array(d["lines_gd"], (7, 4))
                    and all(array(d[k], (len(d["pens"]),)) for k in ("norms", "train_acc", "losses"))
                    and len(d["newton_gap"]) == d["n_newton"] + 1 and isinstance(d["separable"], bool))
        if name == "calibration":
            m = n if n is not None else len(d["nb_z"])
            if not (array(d["fold_ids"], (m,), low=0, high=FOLDS - 1) and np.asarray(d["fold_ids"]).dtype.kind in "iu"):
                return False
            for k in ("lr2", "lr70", "nb", "nb_platt"):
                p, z, row = d[f"p_{k}"], d[f"z_{k}"], d[k]
                if not (array(p, (m,), low=0, high=1) and array(z, (m,))
                        and np.allclose(p, .5 * (1 + np.tanh(.5 * np.asarray(z))), rtol=1e-12, atol=1e-14)
                        and set("count conf frac ece brier logloss score".split()) <= row.keys()
                        and array(row["count"], (10,), low=0) and np.sum(row["count"]) == m
                        and array(row["conf"], (10,), low=0, high=1) and array(row["frac"], (10,), low=0, high=1)
                        and array(row["logloss"], (), low=0) and row["score"]["probability_clip"] is None
                        and row["score"]["unit"] == "nats per page" and row["score"]["n_pages"] == m):
                    return False
                if cohort is not None:
                    expected = score_summary(z, cohort["labels"], p)
                    if not all(np.allclose(row[field], expected[field], rtol=1e-10, atol=1e-12)
                               for field in ("count", "conf", "frac", "ece", "brier", "logloss")):
                        return False
                    if row["score"] != expected["score"]:
                        return False
                    if not np.isclose(d["acc"][k], np.mean((np.asarray(p) > .5) == np.asarray(cohort["labels"]))):
                        return False
            if not (d["evaluation"]["folds"] == FOLDS and d["evaluation"]["seed"] == 1950
                    and d["evaluation"]["inner_platt_folds"] == 5
                    and d["evaluation"]["fold_sha256"] == content_digest(np.asarray(d["fold_ids"]).tolist())
                    and d["evaluation"]["protocol"] == benchmark_protocol()):
                return False
            return np.array_equal(d["nb_z"], d["z_nb"])
        if name == "nbvslr":
            return all(set(map(str, d["sizes"])) == set(d[k]) and all(set("mean lo hi se".split()) <= d[k][str(m)].keys() and array([d[k][str(m)][x] for x in ("mean", "lo", "hi")], (3,), low=0, high=1) for m in d["sizes"]) for k in ("nb", "lr"))
        if name == "lda":
            return (all(array(d[k], (2,)) for k in ("w", "mA", "mD"))
                    and all(array(d[k], (2, 2)) for k in ("covA", "covD"))
                    and all(array(d[k], (N_WORDS, N_WORDS)) for k in ("SB", "SW"))
                    and array(d["angles"], ndim=1) and array(d["sep"], (len(d["angles"]),)) and array(d["eigvals"], (5,)))
        if name == "knn":
            return (all(array(d[f"region{k}"], (len(d["ys"]), len(d["xs"])), low=0, high=1)
                        and array(d[f"acc{k}"], (), low=0, high=1) and array(d[f"train{k}"], (), low=0, high=1) for k in d["ks"])
                    and array(d["cv"], (len(d["ks"]),), low=0, high=1) and array(d["cv_sd"], (len(d["ks"]),), low=0)
                    and d["k_cv"] in d["ks"])
        if name == "coverhart":
            return all(set(map(str, d["ns"])) == set(d[k]) and all(array([d[k][str(m)][x] for x in ("mean", "lo", "hi")], (3,), low=0, high=1) for m in d["ns"]) for k in ("e1", "ek"))
        if name == "curse":
            return (array(d["contrast"], (len(d["dims"]),), low=0) and array(d["nn_frac"], (len(d["dims"]),), low=0)
                    and all(set(map(str, d["noise"])) == set(d[k]) for k in ("knn", "lr")))
        if name == "kernel":
            m = nt if nt is not None else d["n"]
            return all(array(d[k], (m,)) for k in ("ev2", "ev70", "ev_sig")) and array(d["lift_w"], (3,)) and array(d["taylor_err"], (20,), low=0)
        if name == "svm":
            m = nt if nt is not None else d["n_train"]
            if not (array(d["cv"], (len(d["Cs"]), len(d["gammas"])), low=0, high=1)
                    and array(d["cv_sd"], (len(d["Cs"]), len(d["gammas"])), low=0)
                    and array(d["mu"], (2,)) and array(d["sd"], (2,), low=np.finfo(float).tiny)):
                return False
            return (all(array(d[f"region_C{c:g}"], (len(d["ys"]), len(d["xs"])))
                        and array(d[f"alpha_C{c:g}"], (m,), low=0)
                        and array(d[f"sv_C{c:g}"], ndim=1, low=0, high=m - 1)
                        and np.asarray(d[f"sv_C{c:g}"]).dtype.kind in "iu" for c in d["Cs"])
                    and all(array(d[f"region_g{g:g}"], (len(d["ys"]), len(d["xs"]))) for g in d["gammas"]))
        if name == "trees":
            return (array(d["cv"], (7,), low=0, high=1) and array(d["cv_sd"], (7,), low=0)
                    and len(d["boot_roots"]) == len(d["boot_acc"]) == 20
                    and all(f"rects{i}" in d and array(d[f"acc{i}"], (), low=0, high=1) and array(d[f"train{i}"], (), low=0, high=1) for i in d["depths"])
                    and all(array(d[f"scan_{word}_{kind}"], (len(d[f"scan_{word}_t"]),)) for word in ("not", "the") for kind in ("gini", "entropy", "error")))
        if name == "bagging":
            return (all(bagging_piece(d[f"mf{mf}"]) for mf in (70, 8, 2))
                    and all(array(d[k], (300,), low=0, high=1) for k in ("forest_acc", "forest_oob"))
                    and array(d["bag_acc"], (100,), low=0, high=1))
        if name in ("adaboost", "xgb"):
            for f, rounds in (("2", 300 if name == "adaboost" else d["T"]), ("70", 400 if name == "adaboost" else d["T"])):
                fields = ("eps", "alpha", "exp_loss", "train_err", "test_err") if name == "adaboost" else ("train_loss", "test_loss", "test_acc", "train_acc", "first_loss", "first_acc")
                if not all(array(d[f"{key}_{f}"], (rounds,)) for key in fields):
                    return False
            return (all(array(d[f"region{k}"], (len(d["ys"]), len(d["xs"])), low=-1 if name == "adaboost" else 0, high=1) for k in d["snaps"])
                    and (name != "adaboost" or all(array(d[f"w{k}"], (nt,) if nt is not None else None, ndim=1, low=0, high=1)
                                                   and np.isclose(np.sum(d[f"w{k}"]), 1.) for k in d["snaps"])))
        if name == "metrics":
            return (all(array(d[f"{plot}_{k}"], ndim=2, low=0, high=1) and np.asarray(d[f"{plot}_{k}"]).shape[1] == 2 for k in ("lr2", "lr70", "nb", "rare") for plot in ("roc", "pr"))
                    and all(array([d[k][field] for field in ("auc", "ap", "mw")], (3,), low=0, high=1)
                            and np.isclose(d[k]["auc"], d[k]["mw"]) for k in ("lr2", "lr70", "nb"))
                    and array(d["split_acc"], (100,), low=0, high=1) and array(d["cv_acc"], (20,), low=0, high=1) and array(d["fold_acc"], (200,), low=0, high=1))
        if name == "board":
            if not (integer(d["n"], 2) and d["folds"] == FOLDS and len(d["rows"]) == len(BOARD_CASES)
                    and array(d["fold_ids"], (d["n"],), low=0, high=FOLDS - 1) and np.asarray(d["fold_ids"]).dtype.kind in "iu"
                    and (n is None or d["n"] == n)
                    and d["evaluation"]["fold_sha256"] == content_digest(np.asarray(d["fold_ids"]).tolist())
                    and d["evaluation"]["seed"] == 2025
                    and d["evaluation"]["protocol"] == benchmark_protocol()
                    and d["evaluation"]["method_feature_cases"] ==
                        [f"{key}_{nf}" for key, features in BOARD_CASES.items() for nf in features]):
                return False
            return all(row["key"] == key and isinstance(row["name"], str)
                       and {k for k in row if k.isdigit()} == set(map(str, features))
                       and all(board_piece(row[str(nf)]) for nf in features)
                       for row, (key, features) in zip(d["rows"], BOARD_CASES.items()))
    except (KeyError, TypeError, ValueError, IndexError, AttributeError, OverflowError):
        return False
    return False
