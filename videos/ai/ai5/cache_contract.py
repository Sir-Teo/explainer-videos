"""Part 5 completed-cache contracts. Observations never load models or run producers.

These checks establish bounded structure, integrity and observed prerequisite
identity. They do not certify every scientific conclusion, or reconstruct the
original consumed-input lineage of legacy Part 1 artifacts.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import re
import time
import zipfile
import zlib

import numpy as np

from explainer.ai.cache import Cache
from explainer.cache_lock import cache_lock, locked_item


REQUIRED = {
    "galton": "rows n steps bins counts binom x normal chi2",
    "clt": "ks", "mle": "mus sigmas ll mu_hat sigma_hat ll_hat n",
    "bayes": "ns ps e_all n_all head", "temperature": "prompt temps top_tokens top logits samples prompt2 logits2 top2 top_tokens2",
    "markov": "dists tv freq stationary lam2 start P P3 pi3 walk3 states3",
    "montecarlo": "pts inside est N Ns rms slope true n plain_hits plain_est is_est is_y is_w plain_z plain_plot_indices is_w_full",
    "mcmc": "chain accept left true_left", "brownian": "walk8 walk64 walk1024 paths ends var",
    "diffusion": "theta sigma dt ou_paths ou_t ts ou_mean ou_var xs alphas dens scores fp_ts fp fp_hist fp_err hist_err",
    "shape": "data fwd bwd T grid final_med field2.0 field0.5 field0.1",
    "lln": "n idx run final", "conv": "ns show zg C exp_dist exp_dens exp_ratio exp_bound exp_slope uni_dist uni_dens uni_ratio uni_bound uni_slope",
    "gauss": "S L pts z a w n_slice slice_x1 m_th v_th m_emp v_emp evals evecs S4 b4 m4 C4 m4e C4e n4 err4 r s1 s2",
    "mlebias": "ns R mle bessel se theory hist5",
    "fisher": "ns R mle_nvar med_nvar mle_nvar_se mean_iqr score_mean score_var cr med_limit",
    "map": "n deg sigma lams med_err q25 q75 mle_med best_lam best_err x y xt fit_mle fit_best fit_big w_mle_norm tau_best",
    "maxent": "p lam H H_uniform path others H_others_max H_hist H_lo n_others x gauss_fit lap_fit gauss_lams lap_lam err_g err_l",
    "tails": "n eps exact sim markov cheb chern hoeff need e0 d0 j10",
    "draws": "ex ks_exp M rate ks_beta xp up acc bm_u bm_z ks_bm corr z_hist ex_hist beta_hist scores p freq chi2 N taus onehot gs_bias",
    "mixing": "xs U betas gap tmix lower upper pi ts snaps slope asym asym_pair flow_ij flow_ji",
    "ess": "s n dims ess top theory ess_rare n_rare",
    "scorefn": "mu N bs var_b mean_sf b_star var_star var_rep var_0 sig pop lr steps gerr_plain gerr_base gerr_mirror gnorm2 paths_plain paths_base final_plain final_base div_plain div_base",
    "langevin": "configs frames grids grid_t grid_steps target gx gy l1 flow_h flow_left true_left_halfspace true_spread_left_halfspace",
    "qv": "ks ns qv_mean qv_sd tv_mean tv_theory path path_qv n qv_example",
    "ito": "ns M left_err strat_err lemma_rms naive_rms e_mean e_half lemma_slope",
    "em": "mu sigma T M hs strong weak weak_se strong_slope weak_slope exact_path n_show",
    "decoding": "provenance metric_version prompt_count stochastic_samples greedy_samples settings kinds values prompt0 prompt3 human next_p next_tok",
}
ITEM_DEPENDENCIES = {"mle": ("galton",), "mixing": ("markov",), "ess": ("montecarlo",)}
TEXT_DEPENDENCIES = {"bayes": ("passage",), "markov": ("train",)}


def digest(path):
    path = Path(path)
    before = path.stat()
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
        raise ValueError(f"Prerequisite changed while fingerprinting: {path}")
    return h.hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=float).encode()).hexdigest()


def _same(a, b):
    # JSON identities distinguish bool from int, unlike Python equality.
    return canonical(a) == canonical(b)


def _integer(value, low=0):
    return isinstance(value, (int, np.integer)) and not isinstance(value, (bool, np.bool_)) and value >= low


def _finite(value, low=-math.inf, high=math.inf):
    a = np.asarray(value)
    return a.dtype.kind in "iuf" and bool(np.isfinite(a).all() and (a >= low).all() and (a <= high).all())


def _array(value, shape=None, ndim=None, low=-math.inf, high=math.inf):
    a = np.asarray(value)
    return ((shape is None or a.shape == shape) and (ndim is None or a.ndim == ndim)
            and _finite(a, low, high))


def _prob(value, shape=None, axis=None):
    a = np.asarray(value)
    return _array(a, shape, low=0, high=1) and (axis is None or np.allclose(a.sum(axis), 1, rtol=1e-6, atol=1e-7))


def valid_structure(name, d):
    """Required fields and bounded consumed-array contracts, not all science claims."""
    if name not in REQUIRED or not isinstance(d, dict) or not set(REQUIRED[name].split()) <= d.keys():
        return False
    try:
        if name == "galton":
            rows, n = d["rows"], d["n"]
            return (_integer(rows, 1) and _integer(n, 1) and _array(d["bins"], (n,), low=0, high=rows)
                    and _array(d["counts"], (rows + 1,), low=0) and np.sum(d["counts"]) == n
                    and _prob(d["binom"], (rows + 1,), axis=0) and _array(d["steps"], ndim=2, low=0, high=1)
                    and np.asarray(d["steps"]).shape[1] == rows and _finite(d["chi2"], 0))
        if name == "clt":
            return bool(d["ks"]) and all(_integer(k, 1) and _prob(d[f"k{k}"], (5 * k + 1,), axis=0) for k in d["ks"])
        if name == "mle":
            return (_array(d["mus"], ndim=1) and _array(d["sigmas"], ndim=1, low=np.finfo(float).tiny)
                    and _array(d["ll"], (len(d["mus"]), len(d["sigmas"]))) and _integer(d["n"], 1)
                    and _finite(d["sigma_hat"], 0) and _finite(d["mu_hat"]))
        if name == "bayes":
            if not (_array(d["ps"], ndim=1, low=0, high=1) and _integer(d["n_all"], 1)
                    and isinstance(d["head"], str) and _finite(d["e_all"], 0, 1)):
                return False
            return all(_integer(n) and n <= d["n_all"] and _integer(d[f"k{n}"])
                       and d[f"k{n}"] <= n and _array(d[f"post{n}"], (len(d["ps"]),), low=0)
                       and _finite(d[f"mean{n}"], 0, 1) and _array(d[f"ci{n}"], (2,), low=0, high=1)
                       and d[f"ci{n}"][0] <= d[f"ci{n}"][1]
                       and (d[f"mle{n}"] is None if n == 0 else _finite(d[f"mle{n}"], 0, 1)) for n in d["ns"])
        if name == "temperature":
            for suffix in ("", "2"):
                z, ids = np.asarray(d["logits" + suffix]), np.asarray(d["top" + suffix])
                if not (_array(z, ndim=1) and _array(ids, ndim=1, low=0, high=len(z) - 1)
                        and ids.dtype.kind in "iu" and len(np.unique(ids)) == len(ids)
                        and len(d["top_tokens" + suffix]) == len(ids)
                        and all(isinstance(t, str) and t for t in d["top_tokens" + suffix])):
                    return False
            return (isinstance(d["samples"], dict)
                    and all(isinstance(d["samples"].get(str(t)), str) and d["samples"][str(t)]
                            for t in [0.0] + list(d["temps"]))
                    and all(_finite(t, np.finfo(float).tiny)
                    and _prob(d[f"p{t}"], (len(d["top"]),))
                    and np.sum(d[f"p{t}"]) <= 1 + 1e-6 and _finite(d[f"H{t}"], 0) for t in d["temps"]))
        if name == "markov":
            return (_prob(d["P"], (27, 27), axis=1) and _prob(d["freq"], (27,), axis=0)
                    and _prob(d["stationary"], (27,), axis=0) and _prob(d["P3"], (3, 3), axis=1)
                    and _prob(d["pi3"], (3,), axis=0) and _prob(d["dists"], axis=1)
                    and np.asarray(d["dists"]).shape[1] == 27 and _finite(d["tv"], 0, 1))
        if name == "montecarlo":
            return (_integer(d["N"], 1) and _integer(d["n"], 1) and _integer(d["plain_hits"])
                    and d["plain_hits"] <= d["n"] and _array(d["pts"], ndim=2, low=-1, high=1)
                    and np.asarray(d["pts"]).shape[1] == 2 and len(d["inside"]) == len(d["pts"])
                    and _array(d["est"], (d["N"],), low=0, high=4)
                    and _array(d["rms"], (len(d["Ns"]),), low=0)
                    and _array(d["is_w"], (len(d["is_y"]),), low=0)
                    and _array(d["plain_z"], (d["n"],))
                    and _array(d["is_w_full"], (d["n"],), low=0)
                    and _array(d["plain_plot_indices"], ndim=1, low=0, high=d["n"] - 1)
                    and np.asarray(d["plain_plot_indices"]).dtype.kind in "iu"
                    and len(np.unique(d["plain_plot_indices"])) == len(d["plain_plot_indices"])
                    and d["plain_hits"] == int(np.sum(np.asarray(d["plain_z"]) > 4))
                    and _finite(d["plain_est"], 0, 1)
                    and abs(d["plain_est"] - d["plain_hits"] / d["n"]) < 1e-12
                    and np.array_equal(np.sort(d["plain_plot_indices"]), np.union1d(
                        np.arange(min(400, d["n"])), np.flatnonzero(np.asarray(d["plain_z"]) > 4))))
        if name == "mcmc":
            return _array(d["chain"], ndim=2) and np.asarray(d["chain"]).shape[1] == 2 and _finite(d["accept"], 0, 1) and _finite(d["left"], 0, 1)
        if name == "brownian":
            return (all(_array(d[f"walk{n}"], (3, n + 1)) for n in (8, 64, 1024))
                    and _array(d["paths"], ndim=2) and _array(d["ends"], (4, 40), low=0)
                    and _array(d["var"], (4,), low=0))
        if name == "diffusion":
            return (_array(d["ou_paths"], ndim=2) and np.asarray(d["ou_paths"]).shape[1] == len(d["ou_t"])
                    and _array(d["dens"], (len(d["alphas"]), len(d["xs"])), low=0)
                    and _array(d["scores"], np.asarray(d["dens"]).shape)
                    and _array(d["fp"], (len(d["fp_ts"]), len(d["xs"])))
                    and _array(d["fp_hist"], (len(d["fp_ts"]), 80), low=0)
                    and all(_array(d[k], (len(d["ts"]),), low=0 if k == "ou_var" else -math.inf)
                            for k in ("ou_mean", "ou_var")))
        if name == "shape":
            return (_array(d["data"], ndim=2) and np.asarray(d["data"]).shape[1] == 2
                    and _array(d["fwd"], ndim=3) and _array(d["bwd"], np.asarray(d["fwd"]).shape)
                    and np.asarray(d["fwd"]).shape[-1] == 2)
        if name == "lln":
            return (_integer(d["n"], 1) and _array(d["idx"], ndim=1, low=1, high=d["n"])
                    and _prob(d["run"]) and np.asarray(d["run"]).shape[1] == len(d["idx"])
                    and _prob(d["final"], (len(d["run"]),)))
        if name == "conv":
            return all(_array(d[f"{kind}_dens"], (len(d["show"]), len(d["zg"])), low=0)
                       and _array(d[f"{kind}_dist"], (len(d["ns"]),), low=0, high=1)
                       and _array(d[f"{kind}_bound"], (len(d["ns"]),), low=0)
                       for kind in ("exp", "uni"))
        if name == "gauss":
            return (all(_array(d[k], shape) for k, shape in
                        [("S", (2, 2)), ("L", (2, 2)), ("S4", (4, 4)), ("C4", (2, 2)),
                         ("m4", (2,)), ("m4e", (2,)), ("C4e", (2, 2))])
                    and _array(d["pts"], ndim=2) and np.asarray(d["pts"]).shape[1] == 2
                    and _array(d["z"], np.asarray(d["pts"]).shape) and _integer(d["n_slice"], 1)
                    and _integer(d["n4"], 1))
        if name == "map":
            return (_integer(d["n"], 1) and _integer(d["deg"])
                    and _array(d["y"], (d["n"],)) and _array(d["x"], (d["n"],))
                    and all(_array(d[k], (len(d["lams"]),), low=0) for k in ("med_err", "q25", "q75"))
                    and all(_array(d[k], (len(d["xt"]),)) for k in ("fit_mle", "fit_best", "fit_big")))
        if name == "maxent":
            return (_prob(d["p"], (6,), axis=0) and _array(d["path"], ndim=2)
                    and np.asarray(d["path"]).shape[1] == 7 and _prob(d["others"], axis=1)
                    and np.asarray(d["others"]).shape[1] == 6
                    and _array(d["gauss_fit"], (len(d["x"]),), low=0)
                    and _array(d["lap_fit"], (len(d["x"]),), low=0))
        if name == "draws":
            return (_prob(d["p"], axis=0) and _prob(d["freq"], np.asarray(d["p"]).shape, axis=0)
                    and _array(d["bm_u"], ndim=2, low=0, high=1) and np.asarray(d["bm_u"]).shape[1] == 2
                    and _array(d["bm_z"], np.asarray(d["bm_u"]).shape)
                    and _array(d["up"], (len(d["xp"]),), low=0, high=1))
        if name == "scorefn":
            if not (_array(d["mu"], ()) and _integer(d["steps"], 1) and _integer(d["pop"], 1)):
                return False
            for method in ("plain", "base"):
                paths = np.asarray(d[f"paths_{method}"])
                final = np.asarray(d[f"final_{method}"])
                if not (paths.ndim == 3 and paths.shape[-1] == 2 and paths.dtype.kind in "iuf"
                        and _array(final, (len(paths),), low=-1)
                        and _integer(d[f"div_{method}"]) and d[f"div_{method}"] == int(np.sum(final == -1))):
                    return False
                # A declared failed/censored run may retain NaN gaps. Never
                # accept them in a success row, or interpret a sentinel as loss.
                if np.isinf(paths).any() or any(not np.isfinite(row).all() and final[i] != -1
                                               for i, row in enumerate(paths)):
                    return False
            return True
        if name == "langevin":
            return (_array(d["frames"], ndim=3) and np.asarray(d["frames"]).shape[-1] == 2
                    and _array(d["grids"], (len(d["grid_t"]), len(d["gy"]), len(d["gx"])), low=0)
                    and _array(d["target"], (len(d["gy"]), len(d["gx"])), low=0)
                    and _array(d["l1"], (len(d["grid_t"]),), low=0)
                    and bool(d["configs"]) and all(_array(d[f"{key}_chain"], ndim=2)
                         and np.asarray(d[f"{key}_chain"]).shape[1] == 2
                         and _finite(d[f"{key}_left"], 0, 1) for key in d["configs"]))
        if name == "qv":
            return (_integer(d["n"], 1) and all(_array(d[k], (len(d["ks"]),), low=0)
                    for k in ("ns", "qv_mean", "qv_sd", "tv_mean", "tv_theory"))
                    and _array(d["path"], ndim=1) and len(d["path_qv"]) == len(d["path"]) - 1)
        if name == "ito":
            return _integer(d["M"], 1) and all(_array(d[k], (len(d["ns"]),), low=0)
                   for k in ("left_err", "strat_err", "lemma_rms", "naive_rms"))
        if name == "em":
            return _integer(d["M"], 1) and all(_array(d[k], (len(d["hs"]),), low=0)
                   for k in ("strong", "weak", "weak_se")) and _array(d["exact_path"], ndim=1)
        if name in ("mlebias", "fisher"):
            fields = ("mle", "bessel", "se", "theory") if name == "mlebias" else ("mle_nvar", "med_nvar", "mle_nvar_se", "mean_iqr")
            return _integer(d["R"], 1) and all(_array(d[k], (len(d["ns"]),), low=0) for k in fields)
        if name == "tails":
            return _integer(d["n"], 1) and all(_prob(d[k], (len(d["eps"]),)) for k in ("exact", "sim", "markov", "cheb", "chern", "hoeff"))
        if name == "mixing":
            return (_prob(d["pi"], (len(d["xs"]),), axis=0)
                    and _prob(d["snaps"], (len(d["ts"]), len(d["xs"])), axis=1)
                    and all(_array(d[k], (len(d["betas"]),), low=0) for k in ("gap", "tmix", "lower", "upper")))
        if name == "ess":
            return (_integer(d["n"], 1) and _array(d["ess"], ndim=2, low=1, high=d["n"] * (1 + 1e-12))
                    and np.asarray(d["ess"]).shape[1] == len(d["dims"]) and _prob(d["top"], np.asarray(d["ess"]).shape)
                    and _integer(d["n_rare"], 1) and _finite(d["ess_rare"], 1, d["n_rare"] * (1 + 1e-12)))
        if name == "decoding":
            from . import decoding_contract as contract
            from .decoding import configuration
            config = configuration()
            settings = d["settings"]
            expected_settings = [f"{kind}{value}" for kind, value in config["settings"]]
            return (settings == expected_settings
                    and _same(d["kinds"], [k for k, _ in config["settings"]])
                    and _same(d["values"], [v for _, v in config["settings"]])
                    and d["prompt_count"] == config["prompts"]
                    and d["stochastic_samples"] == config["samples"]
                    and type(d["metric_version"]) is int and d["metric_version"] == contract.METRIC_VERSION
                    and type(d["prompt_count"]) is int and d["prompt_count"] > 0
                    and d["greedy_samples"] == 1 and type(d["greedy_samples"]) is int
                    and type(d["stochastic_samples"]) is int and d["stochastic_samples"] > 1
                    and isinstance(settings, list) and len(settings) == len(set(settings)) == 16
                    and len(d["kinds"]) == len(d["values"]) == len(settings)
                    and contract.valid_piece("human", d["human"], d["prompt_count"])
                    and all(contract.valid_piece(k, d[k], d["prompt_count"]) for k in settings)
                    and _prob(d["next_p"], (60,)) and np.sum(d["next_p"]) <= 1 + 1e-6
                    and len(d["next_tok"]) == 60
                    and isinstance(d["provenance"], dict)
                    and bool(re.fullmatch(r"[0-9a-f]{64}", d["provenance"].get("selected_prompts_sha256", ""))))
        return True
    except (KeyError, TypeError, ValueError, IndexError, AttributeError):
        return False


class SchemaCache(Cache):
    """Conservative recipes, recursive prerequisite guards and atomic publication."""
    @property
    def repo_root(self):
        return getattr(self, "_repo_root", Path(__file__).resolve().parents[3])

    @repo_root.setter
    def repo_root(self, value):
        self._repo_root = Path(value)

    def recipe(self, name):
        if name not in REQUIRED:
            raise KeyError(name)
        paths = ["videos/ai/ai5/compute.py", "videos/ai/ai5/contracts.py", "videos/ai/ai5/cache_contract.py"]
        if name in ("temperature", "decoding"):
            paths += ["videos/ai/ai5/decoding.py", "videos/ai/ai5/decoding_contract.py"]
        if name in ("bayes", "markov"):
            paths += ["videos/ai/ai1/compute.py"]
        libraries = {}
        for package in ("numpy", "scipy", "torch"):
            try:
                libraries[package] = importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                libraries[package] = None
        return dict(item=name, schema_version=1, sources={p: digest(self.repo_root / p) for p in paths},
                    libraries=libraries, scope="whole Part5 producer/contracts/cache sources; decoder helpers only for model-backed items")

    def _files(self, paths):
        return {str(p.relative_to(self.dir.parent)): digest(p) for p in paths}

    def _ai1_payload(self, item):
        p = self.dir.parent / "ai1" / f"{item}.json"
        with cache_lock(p):
            d = self._read_payload(p)
            if item == "bigram":
                valid = _prob(d.get("cond"), (27, 27), axis=1)
            else:
                valid = _prob(d.get("p"), (27,), axis=0)
            if not valid:
                raise ValueError(f"Part1/{item}: consumed probability structure is invalid")
            return self._files([p, p.with_suffix(".npz")])

    def dependencies(self, name):
        if name not in REQUIRED:
            raise KeyError(name)
        out = {}
        for dependency in ITEM_DEPENDENCIES.get(name, ()):
            if not self.current(dependency):
                raise ValueError(f"{name}: missing/stale Part5/{dependency}; prepare it explicitly")
            p = self.path(dependency)
            out.update(self._files([q for q in [p, p.with_suffix(".npz")] if q.exists()]))
        for text in TEXT_DEPENDENCIES.get(name, ()):
            p = self.dir.parent / "ai1" / f"{text}.txt"
            if not p.is_file() or not p.stat().st_size:
                raise FileNotFoundError(f"{name}: nonempty Part1/{text}.txt required")
            out.update(self._files([p]))
        if name == "markov":
            out.update(self._ai1_payload("bigram")); out.update(self._ai1_payload("letters"))
        if name == "temperature":
            from .decoding_contract import judge_identity
            runtime = {p: importlib.metadata.version(p) for p in ("torch", "transformers", "tokenizers", "numpy")}
            out["pinned_judge"] = dict(identity=judge_identity(), runtime=runtime)
        if name == "decoding":
            from .decoding import cache_identity
            out["decoding_identity"] = cache_identity(self.repo_root)
        return out

    @staticmethod
    def _read_payload(path):
        d = json.loads(path.read_text())
        if not isinstance(d, dict):
            raise ValueError("Completed payload must be a dictionary")
        npz = path.with_suffix(".npz")
        if npz.exists():
            with np.load(npz, allow_pickle=False) as archive:
                for key in archive.files:
                    if key in d or archive[key].dtype.hasobject:
                        raise ValueError("Duplicate or object array in completed payload")
                    d[key] = archive[key]
        return d

    def _lineage_matches(self, name, data, dependencies):
        if name == "decoding":
            lineage = dict(data["provenance"])
            lineage.pop("selected_prompts_sha256", None)
            return _same(lineage, dependencies["decoding_identity"])
        if name == "ess":
            parent = json.loads(self.path("montecarlo").read_text())
            return type(data["n_rare"]) is int and data["n_rare"] == parent["n"]
        return True

    @locked_item(lambda self, name: self.path(name))
    def current(self, name):
        if name not in REQUIRED:
            return False
        try:
            p = self.path(name); raw = json.loads(p.read_text())
            if not isinstance(raw, dict):
                return False
            meta = raw.pop("_cache", None)
            if not isinstance(meta, dict) or type(meta.get("schema_version")) is not int:
                return False
            npz = p.with_suffix(".npz")
            expected = dict(schema_version=1, recipe=self.recipe(name), dependencies=self.dependencies(name),
                            payload_sha256=canonical(raw), arrays_sha256=digest(npz) if npz.exists() else None,
                            origin="producer-save")
            if not _same(meta, expected):
                return False
            d = self._read_payload(p)
            if not valid_structure(name, d):
                return False
            return self._lineage_matches(name, d, expected["dependencies"])
        except (OSError, ValueError, TypeError, KeyError, IndexError, AttributeError, EOFError,
                zipfile.BadZipFile, zlib.error, RuntimeError, importlib.metadata.PackageNotFoundError):
            return False

    def _produce(self, name, producer):
        recipe, dependencies = self.recipe(name), self.dependencies(name)
        out = producer()
        if not _same(recipe, self.recipe(name)) or not _same(dependencies, self.dependencies(name)):
            raise ValueError(f"{name}: sources/prerequisites changed during generation; not publishing")
        self.save(name, out, dependencies=dependencies, recipe=recipe)

    @locked_item(lambda self, name: self.path(name))
    def load(self, name):
        if name not in REQUIRED:
            raise KeyError(name)
        if not self.current(name):
            self._produce(name, self.items[name])
        return super().load(name)

    @locked_item(lambda self, name, out, **kwargs: self.path(name))
    def save(self, name, out, *, dependencies=None, recipe=None):
        if not isinstance(out, dict) or "_cache" in out or not valid_structure(name, out):
            raise ValueError(f"{name}: malformed producer result")
        recipe = self.recipe(name) if recipe is None else recipe
        dependencies = self.dependencies(name) if dependencies is None else dependencies
        if not _same(recipe, self.recipe(name)) or not _same(dependencies, self.dependencies(name)):
            raise ValueError(f"{name}: sources/prerequisites changed before publication")
        if not self._lineage_matches(name, out, dependencies):
            raise ValueError(f"{name}: result does not match observed prerequisite identity/cohort")
        arrays = {k: v for k, v in out.items() if isinstance(v, np.ndarray)}
        rest = json.loads(json.dumps({k: v for k, v in out.items() if k not in arrays}, default=float))
        if any(a.dtype.hasobject for a in arrays.values()):
            raise ValueError("Object arrays cannot be published")
        self.dir.mkdir(parents=True, exist_ok=True)
        p = self.path(name); npz = p.with_suffix(".npz"); tmp = p.with_suffix(".tmp.npz")
        if arrays:
            np.savez_compressed(tmp, **arrays)
            array_hash = digest(tmp)
        else:
            array_hash = None
        rest["_cache"] = dict(schema_version=1, recipe=recipe, dependencies=dependencies,
                              payload_sha256=canonical(rest), arrays_sha256=array_hash, origin="producer-save")
        marker = p.with_suffix(".tmp.json"); marker.write_text(json.dumps(rest, ensure_ascii=False, indent=1, default=float))
        p.unlink(missing_ok=True)
        if arrays:
            tmp.replace(npz)
        else:
            npz.unlink(missing_ok=True)
        marker.replace(p)
        self._loaded.pop(name, None)
        # Partial files are intentionally untouched, including incompatible or
        # expensive resumable pieces. Only their owner decides when to retire them.

    def main(self, items, doc=None):
        self.items = items
        parser = argparse.ArgumentParser(description=doc)
        parser.add_argument("names", nargs="*", default=list(items))
        parser.add_argument("--force", action="store_true")
        args = parser.parse_args()
        for name in args.names:
            if name not in REQUIRED or name not in items:
                raise KeyError(name)
            with cache_lock(self.path(name)):
                if self.current(name) and not args.force:
                    print(f"  cached  {name}", flush=True); continue
                start = time.monotonic()
                print(f"  compute {name} ...", flush=True)
                self._produce(name, items[name])
                print(f"  done    {name} in {time.monotonic() - start:.1f}s", flush=True)
