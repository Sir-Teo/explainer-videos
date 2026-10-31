"""Precompute everything numerical in Part 3 of the AI series ("Vectors That Mean Things").

    python -m videos.ai.ai3.compute              # everything missing (Part 1's books are reused: .cache/ai1)
    python -m videos.ai.ai3.compute words jl     # specific items
    python -m videos.ai.ai3.compute --force gpt2 # recompute

Results are cached in ``.cache/ai3/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Every number the
narration quotes is computed here.  ``assert`` is kept for invariants (a factorization reproduces its matrix, tied
weights are tied), never for a hoped-for outcome: the narration reads the result and says what it is.

Every random choice is seeded.  The longer items (``galore``, ``sgns``, ``mf``) save finished pieces as they go
(``CACHE.partial``), so a killed run resumes.  The whole part computes in well under an hour on a laptop.

Items:
    gpt2      GPT-2's token vectors (its embedding matrix, 50,257 x 768): neighbours, a 3D map of seven categories,
              the logits of one prompt as dot products, and the space's lopsidedness (anisotropy): the mean cosine,
              the principal directions, the fix by centring, and the same inside the network, layer by layer
    einsum    the cost of a chain of matrix products in each order, and attention's contractions at GPT-2's size
    project   least squares: classical and modified Gram-Schmidt against Householder QR, and normal equations
              against QR, on ill-conditioned (Hilbert) matrices
    power     power iteration on two real matrices, with the error against the predicted (lambda_2/lambda_1)^k
    image     a landscape drawn by code, and its best rank-k copies (Eckart-Young: error = the tail singular values)
    letters   the 26 x 26 letter-bigram table of the books: singular values, rank-k copies, correspondence analysis
    norms     spectral and Frobenius norms, stable ranks of GPT-2's matrices; solving A x = b as the condition number
              grows, in 64- and 32-bit arithmetic
    depth     a vector through 40 random 256 x 256 layers with gains 0.8, 1.0, 1.2
    mp        the Marchenko-Pastur law against a random matrix, a shuffled trained matrix, and the trained matrices
              of GPT-2 and of the novels model (heavy tails fitted with a power law)
    galore    a small transformer trained on the novels: its gradients' singular values during training, and
              training with GaLore's low-rank gradient projection against full Adam (three learning rates, three
              seeds); Newton-Schulz orthogonalization of one real gradient (Muon's step)
    words     word vectors from the books by counting: co-occurrence (window 4), PPMI, truncated SVD to 100 numbers
    sgns      word2vec (skip-gram, negative sampling) trained on the same books, and Levy & Goldberg's theorem
              checked: SGNS dot products against the shifted PMI, at full rank (exactly) and at 100 dimensions
    highdim   random directions in d dimensions: angles, lengths, the 1/d law for cosines, the thin shell
    jl        random projections of GPT-2's vectors from 768 numbers down to k: worst distortion over all 499,500
              pairs against the proved bound, and the per-pair failure rate against the exact chi-squared tail
    mf        a synthetic ratings matrix (a small Netflix): matrix factorization trained by gradient descent, by rank
              and regularization, replayed
    twotower  two-tower retrieval on the same synthetic world, against popularity and matrix factorization,
              including users the model never saw
"""

from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import json
import math
import pickle
import time
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache
from explainer.cache_lock import cache_lock, locked_item
from videos.ai.ai3 import cache_integrity

CACHE_SCHEMAS = {name: 1 for name in ("gpt2", "norms", "mp", "galore", "words", "sgns", "jl", "mf", "twotower")}


def digest_json(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def file_digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class SchemaCache(Cache):
    """Semantic revisions and corpus lineage, checked without invoking a producer."""

    @locked_item(lambda self, name: self.path(name))
    def current(self, name):
        p = self.path(name)
        if not p.is_file():
            return False
        if name not in CACHE_SCHEMAS:
            return cache_integrity.current(name, self.dir, Path(__file__).resolve().parents[3], Path(__file__))
        try:
            data = json.loads(p.read_text())
            if not isinstance(data, dict):
                return False
            if data.get("schema_version") != CACHE_SCHEMAS[name] or data.get("recipe") != item_recipe(name):
                return False
            npz = p.with_suffix(".npz")
            if data.get("arrays_sha256") != (file_digest(npz) if npz.exists() else None):
                return False
            if name in ("words", "sgns"):
                lineage = data["provenance"]
                if lineage["corpus_sha256"] != file_digest(self.dir.parent / "ai1" / "train.txt"):
                    return False
                if lineage["vocab_sha256"] != digest_json(data["vocab"]):
                    return False
                if lineage["recipe"] != item_recipe(name):
                    return False
                if lineage["fingerprint"] != digest_json({k: v for k, v in lineage.items() if k != "fingerprint"}):
                    return False
                if name == "sgns" and not self.current("words"):
                    return False
                if name == "sgns":
                    words = json.loads(self.path("words").read_text())
                    if words["vocab"] != data["vocab"] or data["words_fingerprint"] != words["provenance"]["fingerprint"]:
                        return False
            return True
        except (OSError, ValueError, KeyError, TypeError):
            return False

    @locked_item(lambda self, name: self.path(name))
    def load(self, name):
        if not self.current(name):
            self._produce(name, self.items[name])
        return super().load(name)

    def _produce(self, name, producer):
        # load/main hold the item lock throughout observation, generation and save.
        if name not in cache_integrity.ITEMS:
            self.save(name, producer())
            return
        observations = getattr(self, "_integrity_generations", None)
        if observations is None:
            observations = self._integrity_generations = {}
        observations[name] = cache_integrity.observe_generation(
            name, self.dir, Path(__file__).resolve().parents[3], Path(__file__))
        try:
            self.save(name, producer())
        finally:
            observations.pop(name, None)

    @locked_item(lambda self, name, out: self.path(name))
    def save(self, name, out):
        if name in ("words", "sgns") and out["provenance"]["corpus_sha256"] != file_digest(self.dir.parent / "ai1" / "train.txt"):
            raise ValueError("corpus changed after it was consumed; refusing completed cache publication")
        # Publish arrays before the completion marker, authenticating their bytes.
        self.dir.mkdir(parents=True, exist_ok=True)
        arrays = {k: v for k, v in out.items() if isinstance(v, np.ndarray)}
        rest = {k: v for k, v in out.items() if k not in arrays}
        if name in cache_integrity.ITEMS:
            cache_integrity.sidecar_path(self.dir, name).unlink(missing_ok=True)
        self.path(name).unlink(missing_ok=True)
        self._loaded.pop(name, None)
        npz = self.path(name).with_suffix(".npz")
        if arrays:
            tmp = self.path(name).with_suffix(".tmp.npz")
            np.savez_compressed(tmp, **arrays)
            tmp.replace(npz)
        else:
            npz.unlink(missing_ok=True)
        if name in CACHE_SCHEMAS:
            rest.update(schema_version=CACHE_SCHEMAS[name], recipe=item_recipe(name),
                        arrays_sha256=file_digest(npz) if arrays else None)
        tmp = self.path(name).with_suffix(".tmp.json")
        tmp.write_text(json.dumps(rest, ensure_ascii=False, indent=1, default=float))
        tmp.replace(self.path(name))
        if name in cache_integrity.ITEMS:
            cache_integrity.publish(name, self.dir, Path(__file__).resolve().parents[3], Path(__file__),
                                    origin="producer-save",
                                    generation=getattr(self, "_integrity_generations", {}).get(name))
        (self.dir / f"{name}.partial.json").unlink(missing_ok=True)
        if name == "sgns":
            (self.dir / "sgns.ckpt").unlink(missing_ok=True)

    def main(self, items, doc=None):
        self.items = items
        ap = argparse.ArgumentParser(description=doc, formatter_class=argparse.RawDescriptionHelpFormatter)
        ap.add_argument("names", nargs="*", default=list(items))
        ap.add_argument("--force", action="store_true")
        args = ap.parse_args()
        for name in args.names:
            with cache_lock(self.path(name)):
                if self.current(name) and not args.force:
                    print(f"  cached  {name}")
                    continue
                started = time.time()
                print(f"  compute {name} ...", flush=True)
                self._produce(name, items[name])
                print(f"  done    {name} in {time.time() - started:.0f}s", flush=True)


CACHE = SchemaCache("ai3")


def cache_current(name):
    return CACHE.current(name)


def load(name):
    # Deliberate indirection: cached-only QA guards this instance before any upgrade.
    return CACHE.load(name)

VOWELS = "aeiou"
CATEGORIES = {
    "animals": "dog cat horse cow sheep wolf lion tiger bear rabbit mouse fox pig goat deer bird eagle fish snake duck",
    "colors": "red blue green yellow black white purple orange pink brown grey silver golden violet",
    "numbers": "one two three four five six seven eight nine ten twenty hundred thousand million",
    "places": "London Paris Berlin Rome Moscow Tokyo China France Germany England Italy Russia Japan Spain",
    "family": "mother father sister brother son daughter wife husband uncle aunt cousin grandmother",
    "body": "hand head eye nose mouth arm leg foot heart face finger ear hair shoulder",
    "verbs": "run walk jump swim eat drink sleep write read sing dance speak think climb",
}
NEIGHBOUR_WORDS = ["dog", "king", "red", "London", "Monday", "three", "happy"]
BOOK_WORDS = ["dog", "king", "woman", "red", "monday", "three", "walked", "eyes", "ship", "father", "happy", "london"]
ANALOGIES = [("france", "paris", "england"), ("man", "king", "woman"), ("he", "his", "she")]
PROMPT = "The Eiffel Tower is located in the city of"
# an analogy test built for the books' vocabulary: within a relation, a:b :: c:? for every ordered pair of pairs
RELATIONS = {
    "gender": "man woman king queen father mother son daughter brother sister uncle aunt husband wife boy girl "
              "sir madam lord lady mr mrs prince princess nephew niece grandfather grandmother he she his her",
    "plural": "dog dogs horse horses house houses hand hands eye eyes door doors book books friend friends girl girls "
              "boy boys day days year years thing things word words room rooms ship ships",
    "past": "walk walked look looked turn turned ask asked call called open opened answer answered seem seemed "
            "want wanted pass passed stop stopped live lived",
    "comparative": "great greater small smaller old older young younger long longer strong stronger high higher "
                   "near nearer",
    "ordinal": "two second three third four fourth five fifth six sixth seven seventh ten tenth",
}


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def ai1():
    """Part 1's compute module (the books, the letter tables)."""
    from videos.ai.ai1 import compute as c1

    return c1


def torch_threads(n: int = 2):
    import torch

    torch.set_num_threads(n)
    torch.set_grad_enabled(True)  # (gpt2() switches it off for the items that only read GPT-2)
    return torch


# ---------------------------------------------------------------------------
# GPT-2's vectors
# ---------------------------------------------------------------------------
def gpt2():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch_threads(2)
    torch.set_grad_enabled(False)
    tok = AutoTokenizer.from_pretrained("openai-community/gpt2")
    model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2", dtype=torch.float32)
    model.eval()
    return tok, model


def token_id(tok, word: str) -> int | None:
    ids = tok(" " + word)["input_ids"]
    return ids[0] if len(ids) == 1 else None


def mean_cos(X, n_pairs=20000, seed=0):
    """Mean and spread of the cosine between random pairs of rows of X (distinct rows)."""
    g = rng(seed)
    i = g.integers(0, len(X), n_pairs)
    j = g.integers(0, len(X), n_pairs)
    keep = i != j
    i, j = i[keep], j[keep]
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    c = (Xn[i] * Xn[j]).sum(1)
    return float(c.mean()), float(c.std())


def compute_gpt2():
    import torch
    from scipy.stats import spearmanr

    tok, model = gpt2()
    W = model.transformer.wte.weight.numpy().astype(np.float64)
    assert W.shape == (50257, 768)
    assert model.lm_head.weight.data_ptr() == model.transformer.wte.weight.data_ptr()  # input and output are tied
    norms = np.linalg.norm(W, axis=1)
    Wn = W / norms[:, None]
    out = dict(vocab=int(W.shape[0]), width=int(W.shape[1]), norm_mean=float(norms.mean()))
    # neighbours (other casings and the word itself without a leading space are skipped)
    nb = {}
    for w in NEIGHBOUR_WORDS:
        i = token_id(tok, w)
        sim = Wn @ Wn[i]
        res = []
        order = np.argsort(-sim, kind="stable")
        # Keep the original 79-other-token search budget, independent of ties.
        for j in order[order != i][:79]:
            s = tok.decode([int(j)]).strip()
            if s.lower() == w.lower() or s.lower() in [r[0].lower() for r in res] or not s.isalpha():
                continue
            res.append((s, float(sim[j])))
            if len(res) == 6:
                break
        nb[w] = res
    out["neighbours"] = nb
    # a 3D map: the category words, centred, on their own top three principal directions
    words, cats, ids = [], [], []
    for c, ws in CATEGORIES.items():
        for w in ws.split():
            i = token_id(tok, w)
            if i is not None:
                words.append(w), cats.append(c), ids.append(i)
    X = W[ids] - W[ids].mean(0)
    _, S, Vt = np.linalg.svd(X, full_matrices=False)
    Y = X @ Vt[:3].T
    Y /= np.abs(Y).max()
    out.update(map_words=words, map_cats=cats, map_xyz=Y)
    # separation check: how many words are nearer their own category's centre than any other (in the 3D map)
    centres = {c: Y[[k for k, cc in enumerate(cats) if cc == c]].mean(0) for c in CATEGORIES}
    hits = sum(min(centres, key=lambda c: np.linalg.norm(Y[k] - centres[c])) == cats[k] for k in range(len(cats)))
    out["map_hits"] = int(hits)
    # a few vectors in full, for the "barcode" of 768 numbers
    pick = ["dog", "puppy", "tobacco", "cat"]
    out["barcode_words"] = pick
    out["barcodes"] = np.array([W[token_id(tok, w)] for w in pick])
    out["barcode_cos"] = [[float(Wn[token_id(tok, a)] @ Wn[token_id(tok, b)]) for b in pick] for a in pick]
    # anisotropy: random common tokens share a direction
    g = rng(2)
    common = g.choice(np.arange(1000, 20000), 2000, replace=False)
    A = Wn[common]
    iu = np.triu_indices(len(common), 1)
    c_raw = (A @ A.T)[iu]
    mu = W.mean(0)
    B = W[common] - mu
    B /= np.linalg.norm(B, axis=1, keepdims=True)
    c_centred = (B @ B.T)[iu]
    out.update(cos_random_mean=float(c_raw.mean()), cos_random_sd=float(c_raw.std()),
               cos_centred_mean=float(c_centred.mean()), cos_centred_sd=float(c_centred.std()),
               hist_raw=np.histogram(c_raw, bins=60, range=(-0.3, 0.6))[0],
               hist_centred=np.histogram(c_centred, bins=60, range=(-0.3, 0.6))[0],
               mean_vec_norm=float(np.linalg.norm(mu)),
               mean_vec_cos=float(np.mean((W[common] @ mu) / norms[common] / np.linalg.norm(mu))))
    # principal directions of the whole embedding matrix (centred): the share of the spread each one carries
    Xc = W - mu
    cov = Xc.T @ Xc / len(Xc)
    lam, Q = np.linalg.eigh(cov)
    lam, Q = lam[::-1], Q[:, ::-1]
    out["pc_share"] = lam[:40] / lam.sum()
    out["pc_share_iso"] = 1.0 / 768
    # all-but-the-top (Mu & Viswanath 2018): centre, then remove the top D principal directions
    abtt = []
    for D in (0, 1, 2, 5, 10, 20):
        Z = W[common] - mu
        if D:
            Z = Z - (Z @ Q[:, :D]) @ Q[:, :D].T
        Z /= np.linalg.norm(Z, axis=1, keepdims=True)
        cc = (Z @ Z.T)[iu]
        abtt.append((D, float(cc.mean()), float(cc.std())))
    out["abtt"] = abtt
    # what the first principal direction tracks: the token's id (BPE merges come roughly in order of frequency)
    pc1 = Xc @ Q[:, 0]
    rho_id = float(spearmanr(pc1, np.arange(len(W))).statistic)
    rho_norm = float(spearmanr(norms, np.arange(len(W))).statistic)
    out.update(pc1_id_spearman=rho_id, norm_id_spearman=rho_norm)
    # the 10 most common tokens' and 10 of the rarest tokens' projections on pc1 (for the picture)
    sample_ids = rng(9).choice(len(W), 3000, replace=False)
    out["pc12_sample"] = np.stack([Xc[sample_ids] @ Q[:, 0], Xc[sample_ids] @ Q[:, 1]], 1)
    out["pc12_ids"] = sample_ids
    # the last step of the model is dot products with the same vectors
    pids = tok(PROMPT)["input_ids"]
    h = model.transformer(torch.tensor([pids])).last_hidden_state[0, -1].numpy().astype(np.float64)
    logits = W @ h
    ref = model(torch.tensor([pids])).logits[0, -1].numpy()
    assert np.allclose(logits, ref, atol=1e-3)
    p = np.exp(logits - logits.max())
    p /= p.sum()
    top = np.argsort(-logits)[:6]
    out.update(prompt=PROMPT, h_norm=float(np.linalg.norm(h)),
               top_tokens=[tok.decode([int(i)]) for i in top], top_logits=[float(logits[i]) for i in top],
               top_probs=[float(p[i]) for i in top], top_cos=[float(Wn[i] @ h / np.linalg.norm(h)) for i in top])
    # inside the network: the passage, layer by layer (Ethayarajh 2019)
    text = ai1().text("passage")
    tid = tok(text)["input_ids"][:1024]
    hs = model.transformer(torch.tensor([tid]), output_hidden_states=True).hidden_states
    layers = []
    for L, H in enumerate(hs):
        H = H[0].numpy().astype(np.float64)
        m_raw, s_raw = mean_cos(H, seed=L)
        m_cen, s_cen = mean_cos(H - H.mean(0), seed=L)
        Hc = H - H.mean(0)
        sv = np.linalg.svd(Hc, compute_uv=False)
        # how much of the raw cosine three dimensions carry (rogue dimensions, Timkey & van Schijndel 2021)
        Hn = H / np.linalg.norm(H, axis=1, keepdims=True)
        gi = rng(100 + L)
        i, j = gi.integers(0, len(H), 20000), gi.integers(0, len(H), 20000)
        keep = i != j
        contrib = (Hn[i[keep]] * Hn[j[keep]]).mean(0)
        top3 = np.argsort(-np.abs(contrib))[:3]
        layers.append(dict(layer=L, cos=m_raw, cos_sd=s_raw, cos_centred=m_cen, cos_centred_sd=s_cen,
                           pc1_share=float(sv[0] ** 2 / (sv ** 2).sum()),
                           top3_dims=[int(d) for d in top3], top3_share=float(contrib[top3].sum() / contrib.sum()),
                           norm_mean=float(np.linalg.norm(H, axis=1).mean())))
    out["layers"] = layers
    out["passage_tokens"] = len(tid)
    return out


# ---------------------------------------------------------------------------
# einsum: what a contraction costs, in each order
# ---------------------------------------------------------------------------
def compute_einsum():
    g = rng(17)
    # a chain of three matrices: (A B) C against A (B C)
    a, b, c, d = 1000, 20, 1000, 20
    A, B, Cm = g.normal(size=(a, b)), g.normal(size=(b, c)), g.normal(size=(c, d))
    left = (A @ B) @ Cm
    right = A @ (B @ Cm)
    assert np.allclose(left, right) and np.allclose(np.einsum("ij,jk,kl->il", A, B, Cm, optimize=True), left)
    macs_left = a * b * c + a * c * d
    macs_right = b * c * d + a * b * d
    path, info = np.einsum_path("ij,jk,kl->il", A, B, Cm, optimize="optimal")
    # attention at GPT-2 small's size: scores and the weighted sum, per layer, for a 1,024-token context
    h, n, dh = 12, 1024, 64
    macs_scores = h * n * n * dh
    macs_values = h * n * n * dh
    macs_proj = 4 * n * 768 * 768  # q, k, v and the output projection
    # a check of the notation on a small case: einsum equals explicit loops
    q, k = g.normal(size=(2, 3, 4, 5)), g.normal(size=(2, 3, 6, 5))
    s = np.einsum("bhqd,bhkd->bhqk", q, k)
    loop = np.zeros((2, 3, 4, 6))
    for bb in range(2):
        for hh in range(3):
            for i in range(4):
                for j in range(6):
                    loop[bb, hh, i, j] = sum(q[bb, hh, i, x] * k[bb, hh, j, x] for x in range(5))
    assert np.allclose(s, loop)
    return dict(shapes=[a, b, c, d], macs_left=macs_left, macs_right=macs_right, path=[list(p) for p in path[1:]],
                heads=h, n=n, dh=dh, macs_scores=macs_scores, macs_values=macs_values, macs_proj=macs_proj)


# ---------------------------------------------------------------------------
# Projection, Gram-Schmidt, least squares
# ---------------------------------------------------------------------------
def gram_schmidt(A, modified=False):
    A = np.array(A, float)
    m, n = A.shape
    Q = np.zeros((m, n))
    for j in range(n):
        v = A[:, j].copy()
        for i in range(j):
            r = Q[:, i] @ (v if modified else A[:, j])
            v -= r * Q[:, i]
        Q[:, j] = v / np.linalg.norm(v)
    return Q


def compute_project():
    ns = list(range(2, 15))
    rows = []
    for n in ns:
        m = 2 * n
        A = 1.0 / (np.arange(m)[:, None] + np.arange(n)[None] + 1.0)  # the first n columns of a 2n x 2n Hilbert matrix
        kappa = float(np.linalg.cond(A))
        I = np.eye(n)
        loss = {}
        for name, Q in (("cgs", gram_schmidt(A)), ("mgs", gram_schmidt(A, True)), ("householder", np.linalg.qr(A)[0])):
            loss[name] = float(np.linalg.norm(Q.T @ Q - I, 2))
        x = np.ones(n)
        b = A @ x
        x_ne = np.linalg.solve(A.T @ A, A.T @ b)
        Qh, Rh = np.linalg.qr(A)
        x_qr = np.linalg.solve(Rh, Qh.T @ b)
        rows.append(dict(n=n, kappa=kappa, **loss, err_normal=float(np.linalg.norm(x_ne - x) / np.linalg.norm(x)),
                         err_qr=float(np.linalg.norm(x_qr - x) / np.linalg.norm(x))))
    # an invariant: the projection matrix is symmetric, idempotent and leaves a residual orthogonal to the columns
    g = rng(3)
    A = g.normal(size=(30, 3))
    P = A @ np.linalg.solve(A.T @ A, A.T)
    y = g.normal(size=30)
    assert np.allclose(P, P.T) and np.allclose(P @ P, P) and np.allclose(A.T @ (y - P @ y), 0)
    return dict(rows=rows, eps=float(np.finfo(float).eps))


# ---------------------------------------------------------------------------
# Power iteration
# ---------------------------------------------------------------------------
def power_run(matvec, n, v_true, lam, steps, seed):
    g = rng(seed)
    v = g.normal(size=n)
    v /= np.linalg.norm(v)
    sins, rq = [], []
    for _ in range(steps + 1):
        c = float(v @ v_true)
        sins.append(float(np.linalg.norm(v - c * v_true)))  # sin of the angle, accurate to round-off
        w = matvec(v)
        rq.append(float(v @ w))
        v = w / np.linalg.norm(w)
    tan0 = sins[0] / math.sqrt(1 - sins[0] ** 2)
    pred = [tan0 * (lam[1] / lam[0]) ** k for k in range(steps + 1)]
    return dict(sin=sins, rq=rq, pred_tan=pred, rq_err=[abs(r - lam[0]) / lam[0] for r in rq])


def compute_power():
    from transformers import AutoModelForCausalLM

    out = {}
    # 1. the covariance of GPT-2's token vectors (768 x 768)
    import torch

    torch_threads(2)
    model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2", dtype=torch.float32)
    W = model.transformer.wte.weight.detach().numpy().astype(np.float64)
    Xc = W - W.mean(0)
    S = Xc.T @ Xc / len(Xc)
    lam, Q = np.linalg.eigh(S)
    lam, Q = lam[::-1], Q[:, ::-1]
    r = power_run(lambda v: S @ v, 768, Q[:, 0], lam, 60, seed=1)
    out["gpt2"] = dict(lam=lam[:8], ratio=float(lam[1] / lam[0]), **r)
    # 2. the letter table's M^T M (26 x 26): independence dominates, so the gap is wide
    M = load("letters")["M"]
    T = np.asarray(M).T @ np.asarray(M)
    lt, Qt = np.linalg.eigh(T)
    lt, Qt = lt[::-1], Qt[:, ::-1]
    r = power_run(lambda v: T @ v, 26, Qt[:, 0], lt, 30, seed=2)
    out["letters"] = dict(lam=lt[:8], ratio=float(lt[1] / lt[0]), **r)
    # measured rate: the slope of log(sin) over the steps where it is above round-off
    for key in ("gpt2", "letters"):
        s = np.array(out[key]["sin"])
        k = np.arange(len(s))
        ok = (s > 1e-13) & (k >= 3)
        slope = np.polyfit(k[ok], np.log(s[ok]), 1)[0]
        out[key]["rate_measured"] = float(math.exp(slope))
    return out


# ---------------------------------------------------------------------------
# An image, rank by rank
# ---------------------------------------------------------------------------
IMG_RANKS = [1, 2, 4, 8, 16, 32, 64]


def landscape(h=180, w=288, seed=1936):
    """A grey landscape drawn by code: sky, a sun, two mountain ranges, a lake with a reflection, a shore of pines."""
    g = rng(seed)
    y, x = np.mgrid[0:h, 0:w] / np.array([h, w])[:, None, None]
    img = 0.55 + 0.4 * (y / 0.62)  # sky, brighter towards the horizon
    sun = np.exp(-(((x - 0.72) * w) ** 2 + ((y - 0.24) * h) ** 2) / (2 * 9.0 ** 2))
    img = np.maximum(img, 0.35 + 0.65 * sun) + 0.25 * np.exp(-(((x - 0.72) * w) ** 2 + ((y - 0.24) * h) ** 2) / 2000)

    def ridge(base, amp, octaves, s):
        gg = rng(s)
        xs = np.linspace(0, 1, w)
        r = np.full(w, base)
        for o in range(octaves):
            f = 2 ** o
            ph = gg.uniform(0, 2 * np.pi, 3)
            r += amp / f * sum(np.sin(2 * np.pi * (f * (k + 1)) * xs + ph[k]) / (k + 1) for k in range(3))
        return r

    horizon = int(0.62 * h)
    far = ridge(0.40, 0.06, 5, seed + 1)
    near = ridge(0.50, 0.05, 6, seed + 2)
    for col in range(w):
        f0, n0 = int(far[col] * h), int(near[col] * h)
        img[f0:horizon, col] = 0.42 + 0.08 * (np.arange(f0, horizon) - f0) / max(1, horizon - f0)
        img[n0:horizon, col] = 0.22 + 0.05 * g.random(max(0, horizon - n0)) ** 3
    # pines on the shore
    for cx in g.uniform(0.02, 0.98, 26):
        ht = g.uniform(0.07, 0.16)
        base = 0.62 + g.uniform(-0.005, 0.01)
        mask = (y < base) & (y > base - ht) & (np.abs(x - cx) < (y - (base - ht)) * 0.28 * (h / w))
        img[mask] = 0.10
    # the lake: the scene above, flipped, darker and rippled
    above = img[:horizon][::-1]
    lake = img[horizon:]
    for row in range(lake.shape[0]):
        src = above[min(row, horizon - 1)]
        shift = int(round(2.0 * math.sin(row * 0.9) + g.normal() * 0.6))
        lake[row] = 0.15 + 0.6 * np.roll(src, shift) * (1 - 0.35 * row / lake.shape[0])
    img[horizon:] = lake
    return np.clip(img, 0, 1)


def compute_image():
    X = landscape()
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    recon, err, tail = [], [], []
    for k in IMG_RANKS:
        R = (U[:, :k] * S[:k]) @ Vt[:k]
        recon.append(np.clip(R, 0, 1))
        err.append(float(np.linalg.norm(X - R)))
        tail.append(float(math.sqrt((S[k:] ** 2).sum())))
        assert abs(err[-1] - tail[-1]) < 1e-8 * max(1.0, tail[-1])  # Eckart-Young: the error is the tail, exactly
    h, w = X.shape
    return dict(img=(X * 255).astype(np.uint8), recon=(np.array(recon) * 255).astype(np.uint8), S=S, ranks=IMG_RANKS,
                err=err, tail=tail, total=float(np.linalg.norm(X)), shape=[h, w],
                storage=[k * (h + w + 1) for k in IMG_RANKS], pixels=h * w,
                energy=[float((S[:k] ** 2).sum() / (S ** 2).sum()) for k in IMG_RANKS])


# ---------------------------------------------------------------------------
# Letters: the SVD of the bigram table
# ---------------------------------------------------------------------------
def compute_letters():
    c1 = ai1()
    if not c1.path("bigram").exists():
        c1._save("bigram", c1.ITEMS["bigram"]())
    J = np.asarray(c1.load("bigram")["joint"])[1:, 1:]  # letters only: previous x next
    J = J / J.sum()
    M = np.sqrt(J)  # the square root keeps rare pairs visible and makes the rank-1 part "independence"
    U, S, Vt = np.linalg.svd(M)
    recon = np.array([(U[:, :k] * S[:k]) @ Vt[:k] for k in range(1, 27)])
    err = np.array([np.linalg.norm(M - r) for r in recon])
    tail = np.array([math.sqrt(float((S[k:] ** 2).sum())) for k in range(1, 27)])
    assert np.allclose(err, tail, atol=1e-9)  # Eckart-Young: the error is exactly the singular values left out
    # correspondence analysis: the table's departure from independence, scaled
    r, c = J.sum(1), J.sum(0)
    R = (J - np.outer(r, c)) / np.sqrt(np.outer(r, c))
    Uc, Sc, Vct = np.linalg.svd(R)
    row = Uc[:, 0] * Sc[0] / np.sqrt(r)  # principal coordinates of each letter as the previous letter
    col = Vct[0] * Sc[0] / np.sqrt(c)  # ... and as the next letter
    if row[0] > 0:  # orient: 'a' on the left
        row, col = -row, -col
    letters = "abcdefghijklmnopqrstuvwxyz"
    left5 = [letters[i] for i in np.argsort(row)[:5]]
    return dict(M=M, S=S, U=U, Vt=Vt, recon=recon, err=err, total=float(np.linalg.norm(M)), ca_s=Sc[:5],
                ca_row=row, ca_col=col, ca_share=float(Sc[0] ** 2 / (Sc ** 2).sum()), ca_left5=left5,
                ca_vowels_left=int(sorted(left5) == sorted(VOWELS)))


# ---------------------------------------------------------------------------
# Norms and conditioning
# ---------------------------------------------------------------------------
def gpt2_matrices():
    """GPT-2's 48 weight matrices in the blocks: (layer, kind, array)."""
    from transformers import AutoModelForCausalLM
    import torch

    torch_threads(2)
    model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2", dtype=torch.float32)
    out = []
    for L, blk in enumerate(model.transformer.h):
        for kind, mod in (("attn", blk.attn.c_attn), ("attn_out", blk.attn.c_proj), ("mlp_in", blk.mlp.c_fc),
                          ("mlp_out", blk.mlp.c_proj)):
            out.append((L, kind, mod.weight.detach().numpy().astype(np.float64)))
    return out


def compute_norms():
    rows = []
    for L, kind, Wm in gpt2_matrices():
        s = np.linalg.svd(Wm, compute_uv=False)
        fro = float(np.sqrt((s ** 2).sum()))
        rows.append(dict(layer=L, kind=kind, shape=list(Wm.shape), spec=float(s[0]), fro=fro,
                         stable=float(fro ** 2 / s[0] ** 2), kappa=float(s[0] / s[-1]), rank=int(min(Wm.shape))))
        assert s[0] <= fro + 1e-9 <= math.sqrt(min(Wm.shape)) * s[0] + 1e-6
    # a random matrix of GPT-2's MLP shape, for comparison
    g = rng(21)
    G = g.normal(size=(768, 3072))
    sg = np.linalg.svd(G, compute_uv=False)
    rand = dict(shape=[768, 3072], seed=21, distribution="iid-standard-normal", stable=float((sg ** 2).sum() / sg[0] ** 2), kappa=float(sg[0] / sg[-1]),
                stable_pred=768 * 3072 / (math.sqrt(768) + math.sqrt(3072)) ** 2)
    # solving A x = b as the condition number grows: the error is about kappa times the machine's rounding unit
    kappas = [10.0 ** e for e in range(0, 15)]
    solve = []
    for kap in kappas:
        e64, e32 = [], []
        for seed in range(5):
            gg = rng(1000 + seed)
            n = 60
            U, _ = np.linalg.qr(gg.normal(size=(n, n)))
            V, _ = np.linalg.qr(gg.normal(size=(n, n)))
            s = np.logspace(0, -math.log10(kap), n)
            A = (U * s) @ V.T
            x = gg.normal(size=n)
            b = A @ x
            e64.append(float(np.linalg.norm(np.linalg.solve(A, b) - x) / np.linalg.norm(x)))
            x32 = np.linalg.solve(A.astype(np.float32), b.astype(np.float32)).astype(np.float64)
            e32.append(float(np.linalg.norm(x32 - x) / np.linalg.norm(x)))
        solve.append(dict(kappa=kap, e64=float(np.median(e64)), e32=float(np.median(e32))))
    return dict(rows=rows, random=rand, solve=solve, eps64=float(np.finfo(np.float64).eps),
                eps32=float(np.finfo(np.float32).eps))


# ---------------------------------------------------------------------------
# Depth: a vector through many random layers
# ---------------------------------------------------------------------------
def compute_depth():
    """x -> W_l x through 40 layers of random 256 x 256 matrices with entries N(0, g^2 / 256): the length is
    multiplied by about g per layer (Part 9's initialization story, in miniature)."""
    g = rng(5)
    n, L = 256, 40
    out = dict(n=n, layers=L, gains=[0.8, 1.0, 1.2])
    for gain in out["gains"]:
        x = g.normal(size=n)
        x /= np.linalg.norm(x)
        lengths, sig = [1.0], []
        for _ in range(L):
            W = g.normal(size=(n, n)) * gain / math.sqrt(n)
            sig.append(float(np.linalg.svd(W, compute_uv=False)[0]))
            x = W @ x
            lengths.append(float(np.linalg.norm(x)))
        out[f"len{gain}"] = np.array(lengths)
        out[f"sigma{gain}"] = float(np.mean(sig))
        out[f"rate{gain}"] = float((lengths[-1] / lengths[0]) ** (1 / L))
    return out


# ---------------------------------------------------------------------------
# Random matrices: Marchenko-Pastur against trained weights
# ---------------------------------------------------------------------------
def esd(Wm):
    """The eigenvalues of W W^T / M for an N x M matrix (N <= M), entries scaled to variance one first, and the
    Marchenko-Pastur edges for its aspect ratio."""
    Wm = np.asarray(Wm, float)
    if Wm.shape[0] > Wm.shape[1]:
        Wm = Wm.T
    N, M = Wm.shape
    Z = (Wm - Wm.mean()) / Wm.std()
    ev = np.linalg.eigvalsh(Z @ Z.T / M)
    q = N / M
    return ev, q, (1 - math.sqrt(q)) ** 2, (1 + math.sqrt(q)) ** 2


def powerlaw_fit(ev, min_tail=10):
    """Continuous-tail MLE, choosing xmin by the two-sided empirical KS distance.

    This is a descriptive tail fit, not a power-law goodness-of-fit test.
    """
    x = np.sort(np.asarray(ev, float))
    x = x[np.isfinite(x) & (x > 0)]
    if not isinstance(min_tail, (int, np.integer)) or min_tail < 2:
        raise ValueError("min_tail must be an integer >= 2")
    best = None
    for i in range(len(x) // 2, len(x) - min_tail + 1):
        xmin, t = x[i], x[i:]
        n = len(t)
        log_sum = np.log(t / xmin).sum()
        if log_sum <= 0:
            continue
        alpha = 1 + n / log_sum
        cdf = 1 - (t / xmin) ** (1 - alpha)
        ks = float(max(np.max(np.arange(1, n + 1) / n - cdf),
                       np.max(cdf - np.arange(n) / n)))
        if best is None or ks < best[2]:
            best = (float(alpha), float(xmin), ks, n)
    if best is None:
        return dict(alpha=float("nan"), xmin=float("nan"), ks=float("nan"), n_tail=0,
                    fit_status="unavailable", fit_method="continuous-two-sided-KS")
    return dict(alpha=best[0], xmin=best[1], ks=best[2], n_tail=best[3],
                fit_status="fitted", fit_method="continuous-two-sided-KS")


def mp_density(x, q):
    lo, hi = (1 - math.sqrt(q)) ** 2, (1 + math.sqrt(q)) ** 2
    x = np.asarray(x, float)
    d = np.zeros_like(x)
    m = (x > lo) & (x < hi)
    d[m] = np.sqrt((hi - x[m]) * (x[m] - lo)) / (2 * math.pi * q * x[m])
    return d


def compute_mp():
    import torch

    from explainer.ai import novels
    from explainer.lm import pocket

    out = dict(edge_margin=0.0, edge_rule="strictly-greater-than-limiting-MP-edge")
    g = rng(1967)
    G = g.normal(size=(768, 3072))
    ev, q, lo, hi = esd(G)
    out["random"] = dict(ev=ev, q=q, lo=lo, hi=hi, above=int((ev > hi).sum()), max_over_edge=float(ev[-1] / hi))
    # GPT-2: every block matrix; the MLP's first matrix of layer SHOW in full, with a shuffled control
    rows = []
    SHOW = 6
    for L, kind, Wm in gpt2_matrices():
        e, q_, lo_, hi_ = esd(Wm)
        fit = powerlaw_fit(e)
        rows.append(dict(layer=L, kind=kind, q=q_, hi=hi_, max_over_edge=float(e[-1] / hi_),
                         above=int((e > hi_).sum()), n=len(e), **fit))
        if L == SHOW and kind == "mlp_in":
            out["show"] = dict(layer=L, kind=kind, ev=e, q=q_, lo=lo_, hi=hi_, **fit)
            flat = Wm.ravel().copy()
            rng(7).shuffle(flat)
            es, *_ = esd(flat.reshape(Wm.shape))
            out["shuffled"] = dict(ev=es, above=int((es > hi_).sum()), max_over_edge=float(es[-1] / hi_))
    out["gpt2"] = rows
    # the novels model, trained, against the same architecture freshly initialized
    torch_threads(2)
    model = novels.load_base()
    torch.manual_seed(0)
    fresh = pocket.PocketGPT(model.cfg)
    nrows = []
    for (name, p), (_, p0) in zip(model.named_parameters(), fresh.named_parameters()):
        if p.dim() != 2 or not name.startswith("blocks"):
            continue
        e, q_, lo_, hi_ = esd(p.detach().numpy())
        e0, *_ = esd(p0.detach().numpy())
        fit = powerlaw_fit(e)
        nrows.append(dict(name=name, shape=list(p.shape), q=q_, hi=hi_, max_over_edge=float(e[-1] / hi_),
                          above=int((e > hi_).sum()), n=len(e), init_max_over_edge=float(e0[-1] / hi_),
                          init_above=int((e0 > hi_).sum()), **fit))
    out["novels"] = nrows
    out["novels_d"] = int(model.cfg.d)
    return out


# ---------------------------------------------------------------------------
# GaLore: gradients are low rank; train through a low-rank window
# ---------------------------------------------------------------------------
GL_CFG = dict(d=128, layers=2, heads=4, seq=64)
GL_STEPS, GL_BATCH, GL_WARM = 600, 16, 30
GL_TRACK = "blocks.1.mlp.up.weight"
GL_TRACK_STEPS = [1, 2, 5, 10, 20, 50, 100, 200, 300, 400, 600]
GL_LRS = [1e-3, 3e-3, 1e-2]
GL_METHODS = ["adam", "galore32", "galore8"]
GL_REFRESH, GL_SCALE = 100, 0.25


def stable_rank(s):
    s = np.asarray(s, float)
    return float((s ** 2).sum() / s[0] ** 2)


def effective_rank(s):
    """exp(entropy of the normalized singular values) (Roy & Vetterli 2007)."""
    p = np.asarray(s, float) / np.sum(s)
    p = p[p > 0]
    return float(np.exp(-(p * np.log(p)).sum()))


def galore_run(method: str, lr: float, seed: int, track=False) -> dict:
    """Train the small transformer for GL_STEPS steps.  'adam' is Adam on every parameter; 'galoreR' keeps the
    Adam statistics of each block matrix in a rank-R window: the gradient G (m x n) is projected to P^T G, where
    P holds the top R left singular vectors of G (recomputed every GL_REFRESH steps), Adam runs there, and the
    update P (...) is scaled by GL_SCALE (Zhao et al. 2024, Algorithm 1)."""
    torch = torch_threads(1)
    import torch.nn.functional as F

    from explainer.ai import novels
    from explainer.lm import pocket

    train, valid = novels.token_arrays()
    torch.manual_seed(seed)
    cfg = pocket.Config(vocab=novels.tokenizer().get_vocab_size(), **GL_CFG)
    model = pocket.PocketGPT(cfg)
    data = pocket.TokenStream(train, valid, cfg.seq, seed=seed)
    rank = int(method[6:]) if method.startswith("galore") else 0
    mats = {n: p for n, p in model.named_parameters() if p.dim() == 2 and n.startswith("blocks")} if rank else {}
    rest = [p for n, p in model.named_parameters() if n not in mats]
    if method == "adamsplit":  # the control: full Adam, with GaLore's step scale on the block matrices only
        blk = [p for n, p in model.named_parameters() if p.dim() == 2 and n.startswith("blocks")]
        ids = {id(p) for p in blk}
        opt = torch.optim.Adam([dict(params=[p for p in rest if id(p) not in ids], mult=1.0),
                                dict(params=blk, mult=GL_SCALE)], lr=lr, betas=(0.9, 0.95))
    else:
        opt = torch.optim.Adam(rest, lr=lr, betas=(0.9, 0.95))
    st = {n: dict(P=None, m=None, v=None, t=0) for n in mats}
    W0 = {n: p.detach().clone() for n, p in model.named_parameters() if p.dim() == 2 and n.startswith("blocks")}
    curve, tracked, grads_kept = [], [], {}
    prev_U = None
    for step in range(1, GL_STEPS + 1):
        f = pocket.lr_factor(step - 1, GL_STEPS, "cosine", GL_WARM)
        for gr in opt.param_groups:
            gr["lr"] = lr * f * gr.get("mult", 1.0)
        x, y = data.batch(GL_BATCH)
        loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten())
        opt.zero_grad(set_to_none=True)
        for p in mats.values():
            p.grad = None
        loss.backward()
        if track and step in GL_TRACK_STEPS:
            G = dict(model.named_parameters())[GL_TRACK].grad.detach().numpy().astype(np.float64)
            U, s, _ = np.linalg.svd(G, full_matrices=False)
            ent = dict(step=step, s=(s / s[0]).tolist(), stable=stable_rank(s), eff=effective_rank(s),
                       top8=float((s[:8] ** 2).sum() / (s ** 2).sum()), top32=float((s[:32] ** 2).sum() / (s ** 2).sum()),
                       shape=list(G.shape))
            if prev_U is not None:  # how much the top-8 subspace moved since the last tracked step
                ent["overlap8"] = float(np.linalg.norm(prev_U.T @ U[:, :8]) ** 2 / 8)
            prev_U = U[:, :8]
            tracked.append(ent)
            if step == 300:
                grads_kept["G"] = G
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        with torch.no_grad():
            for n, p in mats.items():
                G = p.grad
                s_ = st[n]
                tall = G.shape[0] >= G.shape[1]  # project on the shorter side (the paper's choice)
                if s_["P"] is None or (step - 1) % GL_REFRESH == 0:
                    U, _, Vh = torch.linalg.svd(G, full_matrices=False)
                    s_["P"] = Vh[:rank].T if tall else U[:, :rank]
                R = G @ s_["P"] if tall else s_["P"].T @ G
                if s_["m"] is None:
                    s_["m"], s_["v"] = torch.zeros_like(R), torch.zeros_like(R)
                s_["t"] += 1
                s_["m"].mul_(0.9).add_(R, alpha=0.1)
                s_["v"].mul_(0.95).addcmul_(R, R, value=0.05)
                mh = s_["m"] / (1 - 0.9 ** s_["t"])
                vh = s_["v"] / (1 - 0.95 ** s_["t"])
                N = mh / (vh.sqrt() + 1e-8)
                upd = N @ s_["P"].T if tall else s_["P"] @ N
                p.add_(upd, alpha=-lr * f * GL_SCALE)
        curve.append(float(loss))
    val = pocket.evaluate(model, data, 16, 8)
    dW = {}
    for n, p in model.named_parameters():
        if n in W0:
            s = np.linalg.svd((p.detach() - W0[n]).numpy().astype(np.float64), compute_uv=False)
            dW[n] = dict(stable=stable_rank(s), eff=effective_rank(s), rank=int(min(p.shape)))
    # optimizer memory for the block matrices, in numbers kept: Adam keeps two per weight; GaLore two per entry of
    # the projected gradient, plus the projector
    mem = 0
    for n, w in W0.items():
        m_, n_ = w.shape
        if rank:
            mem += 2 * rank * max(m_, n_) + min(m_, n_) * rank
        else:
            mem += 2 * m_ * n_
    res = dict(method=method, lr=lr, seed=seed, curve=curve[::5], val=float(val), dW=dW, opt_numbers=mem,
               weights=int(sum(w.numel() for w in W0.values())))
    if track:
        res["tracked"] = tracked
        res["G"] = grads_kept["G"].tolist()
    return res


def compute_galore():
    params = dict(cfg=GL_CFG, steps=GL_STEPS, batch=GL_BATCH, lrs=GL_LRS, methods=GL_METHODS, refresh=GL_REFRESH,
                  scale=GL_SCALE, track=GL_TRACK, v=2)
    part = CACHE.partial("galore", params)
    if "track" not in part:
        part["track"] = galore_run("adam", 3e-3, 0, track=True)
    for m in GL_METHODS:
        for lr in GL_LRS:
            key = f"{m}_{lr:g}_0"
            if key not in part:
                print(f"    {key}", flush=True)
                part[key] = galore_run(m, lr, 0)
    best = {}
    for m in GL_METHODS:
        best[m] = min(GL_LRS, key=lambda lr: part[f"{m}_{lr:g}_0"]["val"])
        for seed in (1, 2):
            key = f"{m}_{best[m]:g}_{seed}"
            if key not in part:
                print(f"    {key}", flush=True)
                part[key] = galore_run(m, best[m], seed)
    tr = part["track"]
    G = np.array(tr["G"])
    # Muon's step on a real gradient: Newton-Schulz drives every singular value towards one
    import torch

    from explainer.lm import pocket

    hist = []
    pocket.newton_schulz(torch.tensor(G, dtype=torch.float32), steps=5, history=hist)
    ns = [np.linalg.svd(h.numpy().astype(np.float64), compute_uv=False) for h in hist]
    U, s, Vt = np.linalg.svd(G, full_matrices=False)
    exact = U @ Vt
    final = hist[-1].numpy().astype(np.float64)
    final = final.T if final.shape != G.shape else final
    runs = {k: part[k] for k in part.done if k != "track"}
    out = dict(track=dict((k, v) for k, v in tr.items() if k != "G"), runs=runs, best_lr=best,
               ns_sv=[x.tolist() for x in ns], ns_err=float(np.linalg.norm(final - exact) / np.linalg.norm(exact)),
               g_sv=(s / s[0]).tolist(), steps=GL_STEPS, batch=GL_BATCH, seq=GL_CFG["seq"], refresh=GL_REFRESH,
               cfg=GL_CFG, ns_initialization="G/(frobenius_norm(G)+1e-7)",
               ns_coefficients=list(pocket.NS_COEFFS), ns_iterations=5, ns_dtype="float32")
    part.finish()
    return out


def compute_galorectl():
    """The control for GaLore's comparison: GaLore scales the block matrices' steps by GL_SCALE while the embedding
    and output layer train at the full learning rate.  Full-rank Adam with the same split shows how much of
    GaLore's result is that split rather than the low-rank projection (same learning rates, same seeds)."""
    params = dict(cfg=GL_CFG, steps=GL_STEPS, batch=GL_BATCH, lrs=GL_LRS, scale=GL_SCALE, v=1)
    part = CACHE.partial("galorectl", params)
    for lr in GL_LRS:
        key = f"adamsplit_{lr:g}_0"
        if key not in part:
            print(f"    {key}", flush=True)
            part[key] = galore_run("adamsplit", lr, 0)
    best = min(GL_LRS, key=lambda lr: part[f"adamsplit_{lr:g}_0"]["val"])
    for seed in (1, 2):
        key = f"adamsplit_{best:g}_{seed}"
        if key not in part:
            print(f"    {key}", flush=True)
            part[key] = galore_run("adamsplit", best, seed)
    out = dict(runs={k: part[k] for k in part.done}, best_lr=best)
    part.finish()
    return out


# ---------------------------------------------------------------------------
# Words from the books
# ---------------------------------------------------------------------------
VOCAB, WINDOW, DIM = 10000, 4, 100


def book_words(with_source=False):
    source = CACHE.dir.parent / "ai1" / "train.txt"
    if not source.is_file():
        ai1().text("train27")  # normal compute may create the missing corpus
    # Read the exact artifact authenticated by lineage; avoid ai1's memoized text.
    raw = source.read_bytes()
    source_sha256 = hashlib.sha256(raw).hexdigest()
    words = ai1().to27(raw.decode("utf-8")).split()
    cnt = collections.Counter(words)
    vocab = [w for w, _ in cnt.most_common(VOCAB)]
    idx = {w: i for i, w in enumerate(vocab)}
    ids = np.array([idx.get(w, -1) for w in words])
    result = (words, vocab, idx, ids, cnt)
    return (*result, source_sha256) if with_source else result


def neighbours(E, vocab, idx, w, k=6):
    """Other rows ranked by dot product; ties keep vocabulary order.

    E is row-normalized by callers. A zero query has no directional neighbours.
    """
    E = np.asarray(E, float)
    query = idx[w]
    if not np.linalg.norm(E[query]):
        return []
    sim = E @ E[query]
    candidates = np.flatnonzero((np.arange(len(E)) != query) & np.isfinite(sim)
                                & (np.linalg.norm(E, axis=1) > 0))
    order = candidates[np.argsort(-sim[candidates], kind="stable")[:max(0, k)]]
    return [(vocab[i], float(sim[i])) for i in order]


def analogy(E, idx, vocab, a, b, c, k=5):
    v = E[idx[b]] - E[idx[a]] + E[idx[c]]
    sim = E @ (v / np.linalg.norm(v))
    for x in (a, b, c):
        sim[idx[x]] = -9
    return [vocab[i] for i in np.argsort(-sim)[:k]]


def analogy_test(E, idx, vocab):
    """3CosAdd accuracy on RELATIONS (pairs present in the vocabulary): a:b :: c:d for every ordered pair of pairs."""
    res = {}
    for rel, ws in RELATIONS.items():
        t = ws.split()
        pairs = [(t[i], t[i + 1]) for i in range(0, len(t), 2) if t[i] in idx and t[i + 1] in idx]
        hit = tot = 0
        for a, b in pairs:
            for c, d in pairs:
                if (a, b) == (c, d):
                    continue
                tot += 1
                hit += analogy(E, idx, vocab, a, b, c, k=1)[0] == d
        res[rel] = dict(acc=hit / max(tot, 1), n=tot, pairs=len(pairs))
    allh = sum(v["acc"] * v["n"] for v in res.values())
    alln = sum(v["n"] for v in res.values())
    res["all"] = dict(acc=allh / alln, n=alln)
    return res


def category_purity(E, idx):
    """Of each category word's 5 nearest neighbours among all the category words, the share in its own category."""
    words, cats = [], []
    for c, ws in CATEGORIES.items():
        for w in ws.lower().split():
            if w in idx and w not in words:
                words.append(w), cats.append(c)
    X = E[[idx[w] for w in words]]
    X = X / np.linalg.norm(X, axis=1, keepdims=True)
    S = X @ X.T
    np.fill_diagonal(S, -9)
    hits = [np.mean([cats[j] == cats[i] for j in np.argsort(-S[i])[:5]]) for i in range(len(words))]
    chance = np.mean([(cats.count(c) - 1) / (len(cats) - 1) for c in cats])
    return dict(purity=float(np.mean(hits)), chance=float(chance), n=len(words))


def cooccurrence(ids, V=VOCAB, window=WINDOW):
    import scipy.sparse as sp

    rows, cols = [], []
    for d in range(1, window + 1):
        a, b = ids[:-d], ids[d:]
        m = (a >= 0) & (b >= 0)
        rows.append(a[m]), cols.append(b[m])
    rows, cols = np.concatenate(rows), np.concatenate(cols)
    C = sp.coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(V, V)).tocsr()
    return (C + C.T).tocoo(), len(rows)


def compute_words():
    import scipy.sparse as sp
    from scipy.sparse.linalg import svds

    words, vocab, idx, ids, cnt, source_sha256 = book_words(with_source=True)
    C, n_rows = cooccurrence(ids)
    tot = float(C.sum())
    rs = np.asarray(C.tocsr().sum(1)).ravel()
    cs = rs ** 0.75
    cs /= cs.sum()  # context distribution smoothing (Levy, Goldberg & Dagan 2015)
    pmi = np.log(C.data / tot / (rs[C.row] / tot) / cs[C.col])
    keep = pmi > 0
    P = sp.coo_matrix((pmi[keep], (C.row[keep], C.col[keep])), shape=(VOCAB, VOCAB)).tocsr()
    u, s, _ = svds(P, k=DIM, random_state=0)
    o = np.argsort(-s)
    u, s = u[:, o], s[o]
    E = u * np.sqrt(s)
    E /= np.maximum(np.linalg.norm(E, axis=1, keepdims=True), 1e-12)
    nb = {w: neighbours(E, vocab, idx, w) for w in BOOK_WORDS}
    an = {f"{a}:{b}::{c}": analogy(E, idx, vocab, a, b, c) for a, b, c in ANALOGIES}
    # a 2D picture of the analogy: the four words on the plane of their two differences
    fp = [idx[w] for w in ("france", "paris", "england", "london")]
    D = np.stack([E[fp[1]] - E[fp[0]], E[fp[2]] - E[fp[0]]])
    Q, _ = np.linalg.qr(D.T)
    xy = (E[fp] - E[fp].mean(0)) @ Q
    T = np.asarray(P[:300, :300].todense(), np.float32)  # the corner of the table among the 300 commonest words
    # the pmi of a few pairs, for the definition
    Cc = C.tocsr()
    show_pairs = []
    for a, b in (("monday", "morning"), ("ship", "sea"), ("dog", "barked"), ("the", "of")):
        if a in idx and b in idx:
            n_ab = float(Cc[idx[a], idx[b]])
            if n_ab > 0:
                show_pairs.append((a, b, n_ab, float(np.log(n_ab * tot / rs[idx[a]] / rs[idx[b]]))))
    return dict(provenance=word_provenance("words", vocab, words, source_sha256=source_sha256), vocab=vocab, n_words=len(words), n_pairs=int(n_rows * 2), density=float(keep.mean()), top300=T,
                nnz=int(P.nnz), s=s, E=E.astype(np.float32), neighbours=nb, analogies=an, analogy_xy=xy,
                counts=[int(cnt[w]) for w in vocab[:20]], analogy_test=analogy_test(E, idx, vocab),
                purity=category_purity(E, idx), show_pairs=show_pairs, cells=VOCAB * VOCAB)


SG_EPOCHS, SG_B, SG_K = 3, 4096, 5


def word_provenance(name, vocab, words=None, *, seq=None, neg=None, source_sha256=None):
    """Content and ordered-row lineage; no loader is used to authenticate it."""
    out = dict(corpus_sha256=source_sha256 or file_digest(CACHE.dir.parent / "ai1" / "train.txt"),
               vocab_sha256=digest_json(vocab), recipe=item_recipe(name))
    if words is not None:
        out["normalized_tokens_sha256"] = hashlib.sha256(" ".join(words).encode()).hexdigest()
    for key, values in (("subsampled_sequence", seq), ("negative_distribution", neg)):
        if values is not None:
            arr = np.ascontiguousarray(values)
            out[key + "_sha256"] = hashlib.sha256(arr.dtype.str.encode() + str(arr.shape).encode() + arr.tobytes()).hexdigest()
    out["fingerprint"] = digest_json(out)
    return out


def sgns_data(seed=7):
    words, vocab, idx, ids, cnt, source_sha256 = book_words(with_source=True)
    freq = np.array([cnt[w] for w in vocab], float)
    f = freq / freq.sum()
    keep_p = np.minimum(1.0, np.sqrt(1e-4 / f) + 1e-4 / f)  # subsample very frequent words
    g = rng(seed)
    seq = ids[(ids >= 0)]
    seq = seq[g.random(len(seq)) < keep_p[seq]]
    neg = freq ** 0.75 / (freq ** 0.75).sum()
    centre = np.concatenate([seq[:-d] for d in range(1, WINDOW + 1)] + [seq[d:] for d in range(1, WINDOW + 1)])
    context = np.concatenate([seq[d:] for d in range(1, WINDOW + 1)] + [seq[:-d] for d in range(1, WINDOW + 1)])
    provenance = word_provenance("sgns", vocab, words, seq=seq, neg=neg, source_sha256=source_sha256)
    return vocab, idx, seq, neg, centre, context, g, provenance


def compute_sgns():
    """Skip-gram with negative sampling (Mikolov et al. 2013) on the books, the same 10,000 words and window; then
    Levy & Goldberg's theorem, checked."""
    torch = torch_threads(2)
    torch.set_grad_enabled(True)  # (the GPT-2 items switch it off)
    torch.manual_seed(0)
    vocab, idx, seq, neg_np, centre, context, g, provenance = sgns_data()
    neg_p = torch.tensor(neg_np, dtype=torch.float32)
    E_in = torch.nn.Embedding(VOCAB, DIM)
    E_out = torch.nn.Embedding(VOCAB, DIM)
    torch.nn.init.uniform_(E_in.weight, -0.5 / DIM, 0.5 / DIM)
    torch.nn.init.zeros_(E_out.weight)
    opt = torch.optim.Adam(list(E_in.parameters()) + list(E_out.parameters()), lr=0.003)
    B, K, losses = SG_B, SG_K, []
    total = SG_EPOCHS * math.ceil(len(centre) / B)
    checks = sorted({0, max(1, total // 300), total // 100, total // 30, total // 10, total // 3, total})
    snaps, snap_steps = [], []

    def snap():  # how it learns: the nearest neighbours of the chosen words, along the way
        E_ = E_in.weight.detach().numpy()
        E_ = E_ / np.maximum(np.linalg.norm(E_, axis=1, keepdims=True), 1e-12)
        return {w: [x for x, _ in neighbours(E_, vocab, idx, w)][:5] for w in BOOK_WORDS}

    snaps.append(snap())
    snap_steps.append(0)
    # a checkpoint after every pass (vectors, optimizer, both random generators, curves), so a killed run resumes
    ckpt = CACHE.dir / "sgns.ckpt"
    start = 0
    checkpoint_contract = dict(provenance=provenance, vocab=vocab, checks=checks,
                               batches_per_epoch=math.ceil(len(centre) / B), epochs=SG_EPOCHS,
                               torch_version=torch.__version__, numpy_version=np.__version__, snapshot_words=list(BOOK_WORDS))
    if ckpt.exists():
        try:
            st = torch.load(ckpt, weights_only=False)
        except (EOFError, RuntimeError, pickle.UnpicklingError) as exc:
            raise ValueError(f"unreadable SGNS checkpoint {ckpt}; preserve and inspect before retry") from exc
        try:
            restore_sgns_checkpoint(st, checkpoint_contract, E_in, E_out, opt, g, torch)
        except IncompatibleSGNSCheckpoint as exc:
            rejected = ckpt.with_name("sgns.rejected-" + file_digest(ckpt)[:16] + ".ckpt")
            ckpt.replace(rejected)
            print(f"  ignoring incompatible SGNS checkpoint ({exc}); preserved as {rejected.name}", flush=True)
        else:
            losses, snaps, snap_steps, start = st["losses"], st["snaps"], st["snap_steps"], st["epoch"] + 1
            print(f"  resuming sgns after pass {start}", flush=True)
    for epoch in range(start, SG_EPOCHS):
        perm = g.permutation(len(centre))
        for s0 in range(0, len(perm), B):
            j = perm[s0:s0 + B]
            c = torch.tensor(centre[j])
            o = torch.tensor(context[j])
            n = torch.multinomial(neg_p, len(j) * K, replacement=True).view(len(j), K)
            vc = E_in(c)
            pos = torch.nn.functional.logsigmoid((vc * E_out(o)).sum(-1))
            neg = torch.nn.functional.logsigmoid(-(E_out(n) @ vc.unsqueeze(-1)).squeeze(-1)).sum(-1)
            loss = -(pos + neg).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            losses.append(float(loss.detach()))
            if len(losses) in checks:
                snaps.append(snap())
                snap_steps.append(len(losses))
        CACHE.dir.mkdir(parents=True, exist_ok=True)
        torch.save(dict(E_in=E_in.state_dict(), E_out=E_out.state_dict(), opt=opt.state_dict(), g=g.bit_generator.state,
                        torch=torch.get_rng_state(), losses=losses, snaps=snaps, snap_steps=snap_steps, epoch=epoch,
                        contract=checkpoint_contract, checkpoint_schema=1), ckpt.with_suffix(".tmp"))
        ckpt.with_suffix(".tmp").replace(ckpt)
    Wi = E_in.weight.detach().numpy().astype(np.float64)
    Wo = E_out.weight.detach().numpy().astype(np.float64)
    E = Wi / np.maximum(np.linalg.norm(Wi, axis=1, keepdims=True), 1e-12)
    nb = {w: neighbours(E, vocab, idx, w) for w in BOOK_WORDS}
    an = {f"{a}:{b}::{c}": analogy(E, idx, vocab, a, b, c) for a, b, c in ANALOGIES}
    svd = load("words")
    if svd["vocab"] != vocab or svd["provenance"]["corpus_sha256"] != provenance["corpus_sha256"]:
        raise ValueError("words/SGNS corpus or ordered vocabulary mismatch; comparison cannot proceed")
    Es = np.asarray(svd["E"], float)
    overlap = {w: len({x for x, _ in nb[w]} & {x for x, _ in neighbours(Es, vocab, idx, w)}) for w in BOOK_WORDS}
    # Levy & Goldberg on the trained model: the optimum of the SGNS loss puts w . c = log(#(w,c) / (#(w) P_n(c)))
    # - log k, for the pairs it saw (#(w) counts the pairs with w at the centre; P_n is the negative distribution)
    top = 2000
    mask = (centre < top) & (context < top)
    pair = np.bincount(centre[mask] * top + context[mask], minlength=top * top).reshape(top, top).astype(float)
    nw = np.bincount(centre, minlength=VOCAB).astype(float)[:top]
    sel = np.argwhere(pair >= 50)
    shifted = np.log(pair[sel[:, 0], sel[:, 1]] / (nw[sel[:, 0]] * neg_np[sel[:, 1]])) - math.log(K)
    dots = (Wi[sel[:, 0]] * Wo[sel[:, 1]]).sum(1)
    r = float(np.corrcoef(shifted, dots)[0, 1])
    slope = float(np.polyfit(shifted, dots, 1)[0])
    pick = rng(8).choice(len(sel), min(3000, len(sel)), replace=False)
    out = dict(provenance=provenance, vocab=vocab, words_fingerprint=svd["provenance"]["fingerprint"],
               neighbours=nb, analogies=an, loss=np.array(losses[::200]), loss_steps=list(range(1, len(losses) + 1, 200)), pairs=int(len(centre)), overlap=overlap,
               steps=len(losses), snap_steps=snap_steps, snap_neighbours=snaps, k=K,
               analogy_test=analogy_test(E, idx, vocab), purity=category_purity(E, idx),
               lg=dict(n=int(len(sel)), r=r, slope=slope, mae=float(np.abs(dots - shifted).mean()),
                       x=shifted[pick], y=dots[pick], min_count=50, top=top))
    out["lg_exact"] = sgns_exact(centre, context, neg_np, K)
    # Completion publication removes the checkpoint only after Cache.save succeeds.
    return out


class IncompatibleSGNSCheckpoint(ValueError):
    """A rejected checkpoint whose state has not touched the live training run."""


def restore_sgns_checkpoint(state, expected, E_in, E_out, opt, g, torch):
    """Preflight on independent objects; incompatible state never touches live state.

    Unexpected failure during the final commit propagates and aborts the run; the
    caller may only start fresh after an IncompatibleSGNSCheckpoint rejection.
    """
    try:
        if not isinstance(state, dict) or state.get("checkpoint_schema") != 1 or state.get("contract") != expected:
            raise ValueError("legacy or mismatched corpus/vocabulary/training contract")
        epoch = state["epoch"]
        if type(epoch) is not int or not 0 <= epoch < expected["epochs"]:
            raise ValueError("invalid epoch")
        completed = (epoch + 1) * expected["batches_per_epoch"]
        expected_snaps = [i for i in expected["checks"] if i <= completed]
        if (len(state["losses"]) != completed or not np.isfinite(state["losses"]).all()
                or state["snap_steps"] != expected_snaps or len(state["snaps"]) != len(expected_snaps)):
            raise ValueError("inconsistent loss/snapshot counters")
        for model, key in ((E_in, "E_in"), (E_out, "E_out")):
            actual = model.state_dict()
            if (set(state[key]) != set(actual)
                    or any(state[key][k].shape != v.shape or not torch.isfinite(state[key][k]).all()
                           for k, v in actual.items())):
                raise ValueError("incompatible/nonfinite embedding state")
            copy.deepcopy(model).load_state_dict(state[key])
        def finite_tensors(value):
            if torch.is_tensor(value):
                return bool(torch.isfinite(value).all())
            if isinstance(value, dict):
                return all(finite_tensors(v) for v in value.values())
            if isinstance(value, (list, tuple)):
                return all(finite_tensors(v) for v in value)
            return True
        if not finite_tensors(state["opt"]):
            raise ValueError("nonfinite optimizer state")
        query_words = expected.get("snapshot_words", [])
        if any(not isinstance(snap, dict) or any(w not in snap or not isinstance(snap[w], list)
               or any(v not in expected["vocab"] for v in snap[w]) for w in query_words)
               for snap in state["snaps"]):
            raise ValueError("invalid neighbour snapshot vocabulary")
        copy.deepcopy(opt).load_state_dict(state["opt"])
        probe_rng = np.random.Generator(type(g.bit_generator)())
        probe_rng.bit_generator.state = state["g"]
        torch.Generator().set_state(state["torch"])
    except (ValueError, KeyError, TypeError, RuntimeError, AttributeError) as exc:
        raise IncompatibleSGNSCheckpoint(str(exc)) from exc
    E_in.load_state_dict(state["E_in"])
    E_out.load_state_dict(state["E_out"])
    opt.load_state_dict(state["opt"])
    g.bit_generator.state = state["g"]
    torch.set_rng_state(state["torch"])


def sgns_exact(centre, context, neg_np, K, V=300, dims=(300, 30, 5), iters=3000):
    """The SGNS loss over the whole corpus, negatives taken in expectation, for the V commonest words: minimized with
    full rank its dot products should equal the shifted PMI exactly (Levy & Goldberg 2014); with fewer dimensions it
    is a weighted low-rank fit of the same matrix."""
    import torch

    mask = (centre < V) & (context < V)
    pair = np.bincount(centre[mask] * V + context[mask], minlength=V * V).reshape(V, V).astype(np.float64)
    nw = pair.sum(1)
    pn = neg_np[:V] / neg_np[:V].sum()
    tot = pair.sum()
    Npos = torch.tensor(pair / tot)
    Nneg = torch.tensor(K * np.outer(nw, pn) / tot)
    seen = pair >= 5
    target = np.full((V, V), np.nan)
    target[seen] = np.log(pair[seen] / (nw[:, None] * pn[None, :])[seen]) - math.log(K)
    res = {}
    for d in dims:
        torch.manual_seed(d)
        Wi = (0.1 * torch.randn(V, d, dtype=torch.float64)).requires_grad_()
        Wo = (0.1 * torch.randn(V, d, dtype=torch.float64)).requires_grad_()
        opt = torch.optim.Adam([Wi, Wo], lr=0.05)
        hist = []
        for it in range(iters):
            X = Wi @ Wo.T
            loss = -(Npos * torch.nn.functional.logsigmoid(X) + Nneg * torch.nn.functional.logsigmoid(-X)).sum()
            opt.zero_grad()
            loss.backward()
            opt.step()
            if it % 50 == 0 or it == iters - 1:
                Xn = X.detach().numpy()
                hist.append((it, float(loss), float(np.nanmedian(np.abs(Xn - target)[seen]))))
        Xn = (Wi @ Wo.T).detach().numpy()
        err = np.abs(Xn - target)[seen]
        pick = rng(9).choice(int(seen.sum()), min(2500, int(seen.sum())), replace=False)
        res[str(d)] = dict(d=d, median_err=float(np.median(err)), p90_err=float(np.percentile(err, 90)),
                           r=float(np.corrcoef(Xn[seen], target[seen])[0, 1]), hist=hist,
                           x=target[seen][pick], y=Xn[seen][pick])
    # the exact optimum, cell by cell (a check of the algebra): where d/dx of the loss vanishes
    x_star = target[seen]
    grad = (pair / tot)[seen] * (1 - 1 / (1 + np.exp(-x_star))) - (K * np.outer(nw, pn) / tot)[seen] / (1 + np.exp(-x_star))
    assert np.abs(grad).max() < 1e-12
    return dict(V=V, cells=int(seen.sum()), min_count=5, dims=list(dims), runs=res)


# ---------------------------------------------------------------------------
# High dimensions
# ---------------------------------------------------------------------------
DIMS = [2, 3, 10, 100, 768]
VAR_DIMS = [2, 3, 5, 10, 20, 50, 100, 200, 500, 768, 1000, 2000, 4096]


def compute_highdim():
    g = rng(11)
    out = dict(dims=DIMS)
    for d in DIMS:
        a = g.normal(size=(20000, d))
        b = g.normal(size=(20000, d))
        c = (a * b).sum(1) / np.linalg.norm(a, axis=1) / np.linalg.norm(b, axis=1)
        ang = np.degrees(np.arccos(np.clip(c, -1, 1)))
        out[f"angles{d}"] = np.histogram(ang, bins=36, range=(0, 180))[0]
        out[f"angle_sd{d}"] = float(ang.std())
        r = np.linalg.norm(a, axis=1) / math.sqrt(d)
        out[f"norms{d}"] = np.histogram(r, bins=40, range=(0, 2))[0]
    # the 1/d law: the variance of the cosine between two random directions, and the spread of a random length
    var, nsd = [], []
    for d in VAR_DIMS:
        cs, ls = [], []
        per = min(5000, 2_000_000 // d)
        for _ in range(max(4, 20000 // per)):
            a = g.normal(size=(per, d))
            b = g.normal(size=(per, d))
            na, nb_ = np.linalg.norm(a, axis=1), np.linalg.norm(b, axis=1)
            cs.append((a * b).sum(1) / na / nb_)
            ls.append(na)
        cs, ls = np.concatenate(cs), np.concatenate(ls)
        var.append(float(cs.var()))
        nsd.append(float(ls.std()))
    out.update(var_dims=VAR_DIMS, cos_var=var, norm_sd=nsd)
    # the volume of a ball lies near its surface: the share within 1% of the radius, (1 - 0.99^d)
    out["shell"] = {str(d): 1 - 0.99 ** d for d in DIMS}
    # many directions, all nearly perpendicular: 10,000 random directions in 768 dimensions
    A = g.normal(size=(10000, 768)).astype(np.float32)
    A /= np.linalg.norm(A, axis=1, keepdims=True)
    G = A @ A.T
    np.fill_diagonal(G, 0)
    worst = float(np.abs(G).max())
    out.update(n_dirs=10000, worst_cos=worst, worst_angle=float(np.degrees(np.arccos(worst))))
    return out


# ---------------------------------------------------------------------------
# Johnson-Lindenstrauss
# ---------------------------------------------------------------------------
KS = [2, 5, 20, 100, 400]
KS_FINE = [2, 5, 10, 20, 50, 100, 200, 400, 768]
JL_EPS = 0.1
JL_DELTA = 0.05


def jl_bound_eps(k, n, delta=JL_DELTA):
    """Squared-distance distortion with union failure bound <= delta.

    NaN means this sufficient bound certifies no epsilon strictly below one.
    """
    if (isinstance(k, bool) or isinstance(n, bool) or not isinstance(k, (int, np.integer))
            or not isinstance(n, (int, np.integer)) or k <= 0 or n < 2
            or not math.isfinite(delta) or not 0 < delta < 1):
        raise ValueError("require integer k>0, n>=2 and 0<delta<1")
    target = 2 * (math.log(n) + math.log(n - 1) - math.log(delta)) / k
    if target >= 1 / 6:
        return float("nan")
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if mid ** 2 / 2 - mid ** 3 / 3 < target:
            lo = mid
        else:
            hi = mid
    return hi


def compute_jl():
    from scipy.stats import chi2

    tok, model = gpt2()
    W = model.transformer.wte.weight.numpy()
    g = rng(3)
    pts = W[g.choice(np.arange(1000, 20000), 1000, replace=False)].astype(np.float64)
    n = len(pts)
    i, j = np.triu_indices(n, 1)
    pick = g.choice(len(i), 2000, replace=False)
    pi_, pj_ = i[pick], j[pick]
    d0 = np.linalg.norm(pts[pi_] - pts[pj_], axis=1)
    out = dict(ks=KS, d0=d0, n=n, delta=JL_DELTA, confidence=1 - JL_DELTA,
               bound_units="squared-relative-error", bound_formula="two-tail-union-v2")
    for k in KS:
        R = g.normal(size=(768, k)) / math.sqrt(k)
        P = pts @ R
        d1 = np.linalg.norm(P[pi_] - P[pj_], axis=1)
        ratio = d1 / d0
        out[f"d{k}"] = d1
        out[f"band{k}"] = [float(x) for x in np.percentile(ratio, [5, 95])]
        out[f"within10_{k}"] = float(np.mean(np.abs(ratio - 1) < 0.1))

    def sqd(X):
        sq = (X * X).sum(1)
        return (sq[:, None] + sq[None] - 2 * X @ X.T)[i, j]

    D0 = sqd(pts)
    fine = []
    for k in KS_FINE:
        worst, fail, p95 = [], [], []
        for seed in range(5):
            R = rng(500 + 31 * k + seed).normal(size=(768, k)) / math.sqrt(k)
            r2 = sqd(pts @ R) / D0
            dev = np.abs(r2 - 1)
            worst.append(float(dev.max()))
            fail.append(float(np.mean(dev > JL_EPS)))
            p95.append(float(np.percentile(dev, 95)))
        exact = float(chi2.sf(k * (1 + JL_EPS), k) + chi2.cdf(k * (1 - JL_EPS), k))
        chern = float(min(1.0, 2 * math.exp(-k * (JL_EPS ** 2 / 2 - JL_EPS ** 3 / 3) / 2)))
        fine.append(dict(k=k, worst=worst, fail=fail, p95=p95, exact_fail=exact, chernoff=chern,
                         bound_eps=jl_bound_eps(k, n)))
    out["fine"] = fine
    out["eps"] = JL_EPS
    out["pairs"] = int(len(i))
    # the dimension the proof asks for, for n points within eps (Dasgupta & Gupta 2003)
    out["jl_k"] = int(math.ceil(4 * math.log(n) / (JL_EPS ** 2 / 2 - JL_EPS ** 3 / 3)))
    return out


# ---------------------------------------------------------------------------
# A small Netflix: matrix factorization on a synthetic ratings matrix
# ---------------------------------------------------------------------------
N_USERS, N_ITEMS, N_GENRES = 4000, 1200, 6
GENRES = ["comedy", "drama", "action", "romance", "horror", "documentary"]
MF_RANKS = [1, 2, 4, 8, 16, 32]
MF_LAMS = [0.0, 0.01, 0.03, 0.1, 0.3]
MF_EPOCHS = 40


def ratings_world(seed=2006):
    """A synthetic world: each film has a main genre and a taste vector; each user a taste vector shaped by an age
    group and a region; a rating is the global mean + biases + taste agreement + noise, rounded to 1..5 stars.
    Users rate what they are likely to watch: popular films, and films they will like."""
    g = rng(seed)
    gen = g.choice(N_GENRES, N_ITEMS, p=[0.24, 0.24, 0.18, 0.14, 0.1, 0.1])
    q = np.eye(N_GENRES)[gen] * 1.0 + 0.35 * g.normal(size=(N_ITEMS, N_GENRES))
    year = g.integers(0, 5, N_ITEMS)
    pop = g.lognormal(0, 1.0, N_ITEMS)
    b_i = 0.35 * g.normal(size=N_ITEMS) + 0.15 * np.log(pop)
    age = g.integers(0, 5, N_USERS)
    region = g.integers(0, 8, N_USERS)
    age_taste = 0.6 * g.normal(size=(5, N_GENRES))
    region_taste = 0.4 * g.normal(size=(8, N_GENRES))
    p = age_taste[age] + region_taste[region] + 0.8 * g.normal(size=(N_USERS, N_GENRES))
    b_u = 0.4 * g.normal(size=N_USERS)
    mu = 3.6
    users, items = [], []
    n_u = np.clip(g.lognormal(3.2, 0.7, N_USERS).astype(int), 5, 400)
    for u in range(N_USERS):
        w = pop * np.exp(0.5 * (q @ p[u]))
        w /= w.sum()
        its = g.choice(N_ITEMS, n_u[u], replace=False, p=w)
        users.append(np.full(len(its), u)), items.append(its)
    users, items = np.concatenate(users), np.concatenate(items)
    raw = mu + b_u[users] + b_i[items] + 0.6 * (p[users] * q[items]).sum(1) + 0.7 * g.normal(size=len(users))
    r = np.clip(np.round(raw), 1, 5)
    split = g.random(len(r))
    return dict(users=users, items=items, r=r, split=split, genre=gen, year=year, age=age, region=region, mu=mu)


def mf_train(Wd, rank, lam, seed, epochs=MF_EPOCHS, snaps=False, train_mask=None, eval_mask=None):
    torch = torch_threads(1)
    u_all, i_all, r_all = Wd["users"], Wd["items"], Wd["r"]
    tr = train_mask
    ev = eval_mask
    ut, it, rt = (torch.tensor(a[tr]) for a in (u_all, i_all, r_all))
    ue, ie, re_ = (torch.tensor(a[ev]) for a in (u_all, i_all, r_all))
    mu = float(r_all[tr].mean())
    torch.manual_seed(seed)
    P = torch.nn.Parameter(0.1 * torch.randn(N_USERS, max(rank, 1), dtype=torch.float64) * (rank > 0))
    Q = torch.nn.Parameter(0.1 * torch.randn(N_ITEMS, max(rank, 1), dtype=torch.float64) * (rank > 0))
    bu = torch.nn.Parameter(torch.zeros(N_USERS, dtype=torch.float64))
    bi = torch.nn.Parameter(torch.zeros(N_ITEMS, dtype=torch.float64))
    params = [bu, bi] + ([P, Q] if rank else [])
    opt = torch.optim.Adam(params, lr=0.01)
    g = rng(seed)
    B = 4096
    hist, qs = [], []

    def rmse(u, i, r):
        with torch.no_grad():
            pred = mu + bu[u] + bi[i] + ((P[u] * Q[i]).sum(1) if rank else 0)
            return float(torch.sqrt(((pred.clamp(1, 5) - r) ** 2).mean()))

    hist.append((0, rmse(ut, it, rt), rmse(ue, ie, re_)))
    if snaps:
        qs.append(Q.detach().numpy().copy())
    for ep in range(1, epochs + 1):
        perm = torch.tensor(g.permutation(len(rt)))
        for s0 in range(0, len(perm), B):
            j = perm[s0:s0 + B]
            u, i, r = ut[j], it[j], rt[j]
            pred = mu + bu[u] + bi[i] + ((P[u] * Q[i]).sum(1) if rank else 0)
            loss = ((pred - r) ** 2).mean()
            if rank:
                loss = loss + lam * ((P[u] ** 2).sum(1) + (Q[i] ** 2).sum(1)).mean()
            loss = loss + 0.01 * (bu[u] ** 2 + bi[i] ** 2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
        hist.append((ep, rmse(ut, it, rt), rmse(ue, ie, re_)))
        if snaps and ep in (1, 2, 4, 8, 16, 40):
            qs.append(Q.detach().numpy().copy())
    return dict(hist=hist, Q=Q.detach().numpy(), P=P.detach().numpy(), bu=bu.detach().numpy(),
                bi=bi.detach().numpy(), mu=mu, qs=qs)


def compute_mf():
    Wd = ratings_world()
    split = Wd["split"]
    train, valid, test = split < 0.8, (split >= 0.8) & (split < 0.9), split >= 0.9
    r = Wd["r"]
    out = dict(n_ratings=int(len(r)), users=N_USERS, items=N_ITEMS, density=float(len(r) / N_USERS / N_ITEMS),
               genres=GENRES, star_counts=[int((r == s).sum()) for s in range(1, 6)])
    final_train = train | valid
    out["fit_counts"] = dict(tuning_train=int(train.sum()), validation=int(valid.sum()),
                             final_train=int(final_train.sum()), test=int(test.sum()))
    out["split_fingerprint"] = hashlib.sha256(np.ascontiguousarray(split).tobytes()).hexdigest()
    out.update(bias_penalty=0.01, evaluation_clip=[1, 5], final_fit="train|valid")
    mu = float(r[final_train].mean())
    out["rmse_mean"] = float(np.sqrt(((r[test] - mu) ** 2).mean()))
    part = CACHE.partial("mf", dict(ranks=MF_RANKS, lams=MF_LAMS, epochs=MF_EPOCHS, split=out["split_fingerprint"], final_fit="train|valid", v=2))
    if "bias" not in part:
        res = mf_train(Wd, 0, 0.0, 0, train_mask=final_train, eval_mask=test)
        part["bias"] = dict(hist=res["hist"])
    out["rmse_bias"] = part["bias"]["hist"][-1][2]
    # choose lambda per rank on the validation ratings
    for k in MF_RANKS:
        for lam in MF_LAMS:
            key = f"v_{k}_{lam:g}"
            if key not in part:
                print(f"    {key}", flush=True)
                res = mf_train(Wd, k, lam, 0, train_mask=train, eval_mask=valid)
                part[key] = dict(hist=res["hist"], best=min(h[2] for h in res["hist"]), last=res["hist"][-1][2])
    best_lam = {k: min(MF_LAMS, key=lambda lam: part[f"v_{k}_{lam:g}"]["last"]) for k in MF_RANKS}
    out["best_lam"] = {str(k): v for k, v in best_lam.items()}
    out["valid"] = {f"{k}_{lam:g}": part[f"v_{k}_{lam:g}"] for k in MF_RANKS for lam in MF_LAMS}
    # test, three seeds, at each rank's chosen lambda
    test_rmse = {}
    for k in MF_RANKS:
        vals = []
        for seed in range(3):
            key = f"t_{k}_{seed}"
            if key not in part:
                res = mf_train(Wd, k, best_lam[k], seed, train_mask=train | valid, eval_mask=test)
                part[key] = dict(last=res["hist"][-1][2], hist=res["hist"])
            vals.append(part[key]["last"])
        test_rmse[str(k)] = vals
    out["test_rmse"] = test_rmse
    # the replayed run: rank 8 at its chosen lambda, and the same with no regularization (overfitting)
    K = 8
    res = mf_train(Wd, K, best_lam[K], 0, snaps=True, train_mask=train | valid, eval_mask=test)
    res0 = mf_train(Wd, K, 0.0, 0, train_mask=train | valid, eval_mask=test)
    out["replay"] = dict(rank=K, lam=best_lam[K], hist=res["hist"], hist_noreg=res0["hist"])
    Qf = res["Q"]
    Qc = Qf - Qf.mean(0)
    _, _, Vt = np.linalg.svd(Qc, full_matrices=False)
    out["q_snaps"] = np.array([(q - Qf.mean(0)) @ Vt[:2].T for q in res["qs"]])
    out["q_snap_epochs"] = [0, 1, 2, 4, 8, 16, 40]
    out["genre"] = Wd["genre"]
    # do the learned film vectors know the genres?  Of each film's 10 nearest (cosine), the share of its genre
    Qn = Qf / np.linalg.norm(Qf, axis=1, keepdims=True)
    S = Qn @ Qn.T
    np.fill_diagonal(S, -9)
    gen = Wd["genre"]
    nn10 = np.argsort(-S, axis=1)[:, :10]
    out["genre_nn"] = float((gen[nn10] == gen[:, None]).mean())
    counts = np.bincount(gen)
    out["genre_chance"] = float(np.sum(counts * (counts - 1)) / (len(gen) * (len(gen) - 1)))
    # the singular values of the completed matrix's taste part (rank-8 P Q^T): how many directions matter
    sv = np.linalg.svd(res["P"] @ res["Q"].T, compute_uv=False)
    out["completed_sv"] = sv[:K] / sv[0]
    part.finish()
    return out


# ---------------------------------------------------------------------------
# Two towers
# ---------------------------------------------------------------------------
TT_DIM, TT_STEPS, TT_BATCH, TT_TAU = 32, 3000, 512, 0.1


def retrieval_recall(score_fn, users, targets, seen, k=10):
    """Macro recall over distinct eligible targets; empty-target users are excluded.

    Seen targets are ineligible and removed. Nonfinite-score items cannot be recommended.
    An empty evaluated cohort is unavailable (NaN), not a zero/success measurement.
    """
    if not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    values, target_count, hits, excluded = [], 0, 0, 0
    for u in users:
        scores = np.asarray(score_fn(u), float).copy()
        if scores.ndim != 1:
            raise ValueError("scores must be a one-dimensional catalog vector")
        blocked = set(seen.get(u, ()))
        relevant = set(targets.get(u, ())) - blocked
        if any(type(i) not in (int, np.int32, np.int64) or not 0 <= i < len(scores) for i in relevant | blocked):
            raise ValueError("target/seen item outside catalog")
        if not relevant:
            excluded += 1
            continue
        eligible = np.array([i for i in range(len(scores)) if i not in blocked and np.isfinite(scores[i])], int)
        top = set(eligible[np.argsort(-scores[eligible], kind="stable")[:k]].tolist())
        count = len(top & relevant)
        values.append(count / len(relevant))
        hits += count
        target_count += len(relevant)
    return dict(recall=float(np.mean(values)) if values else float("nan"), evaluated_users=len(values),
                eligible_targets=target_count, hits=hits, excluded_empty_users=excluded, k=k,
                aggregation="macro", target_policy="distinct-unseen-targets")


def compute_twotower():
    torch = torch_threads(2)
    Wd = ratings_world()
    g = rng(2016)
    users, items, r = Wd["users"], Wd["items"], Wd["r"]
    cold = g.random(N_USERS) < 0.1  # users the model never trains on
    split = Wd["split"]
    pos = r >= 4
    # warm users: train on 80% of their ratings; held-out liked films are the targets
    tr = ~cold[users] & (split < 0.8)
    te = ~cold[users] & (split >= 0.8) & pos
    # cold users: their first five ratings are their history; the rest of what they liked are the targets
    hist_items = [[] for _ in range(N_USERS)]
    for u, i, s, cu in zip(users, items, split, cold[users]):
        if cu or s < 0.8:
            hist_items[u].append(i)
    rng_h = rng(5)
    cold_hist, cold_target = {}, {}
    for u in np.where(cold)[0]:
        its = np.array(hist_items[u])
        rng_h.shuffle(its)
        cold_hist[u] = its[:5].tolist()
        liked = set(items[(users == u) & pos].tolist())
        cold_target[u] = [i for i in liked if i not in cold_hist[u]]
    hist_train = {u: [i for i, s_ in zip(items[users == u], split[users == u]) if s_ < 0.8] for u in np.where(~cold)[0]}
    genre, year = torch.tensor(Wd["genre"]), torch.tensor(Wd["year"])
    age, region = torch.tensor(Wd["age"]), torch.tensor(Wd["region"])
    torch.manual_seed(0)

    class Tower(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.item_id = torch.nn.Embedding(N_ITEMS, TT_DIM)
            self.genre = torch.nn.Embedding(N_GENRES, TT_DIM)
            self.year = torch.nn.Embedding(5, TT_DIM)
            self.hist = torch.nn.EmbeddingBag(N_ITEMS, TT_DIM, mode="mean")
            self.age = torch.nn.Embedding(5, TT_DIM)
            self.region = torch.nn.Embedding(8, TT_DIM)
            self.f_item = torch.nn.Sequential(torch.nn.Linear(3 * TT_DIM, 64), torch.nn.ReLU(), torch.nn.Linear(64, TT_DIM))
            self.f_user = torch.nn.Sequential(torch.nn.Linear(3 * TT_DIM, 64), torch.nn.ReLU(), torch.nn.Linear(64, TT_DIM))

        def items_(self, i):
            x = torch.cat([self.item_id(i), self.genre(genre[i]), self.year(year[i])], -1)
            return torch.nn.functional.normalize(self.f_item(x), dim=-1)

        def users_(self, u, flat, offsets):
            x = torch.cat([self.hist(flat, offsets), self.age(age[u]), self.region(region[u])], -1)
            return torch.nn.functional.normalize(self.f_user(x), dim=-1)

    m = Tower()
    opt = torch.optim.Adam(m.parameters(), lr=3e-3)
    tr_pos = np.where(tr & pos)[0]

    def user_batch(us, hists):
        flat, offs = [], []
        for h in hists:
            offs.append(len(flat))
            flat.extend(h if h else [0])
        return torch.tensor(us), torch.tensor(flat), torch.tensor(offs)

    all_items = torch.arange(N_ITEMS)
    warm_eval = [u for u in np.unique(users[te])][:600]
    warm_target = {u: items[te & (users == u)].tolist() for u in warm_eval}
    pop = np.bincount(items[tr & pos], minlength=N_ITEMS).astype(float)

    def recall(score_fn, us, targets, seen):
        return retrieval_recall(score_fn, us, targets, seen)["recall"]

    def tower_scores(us, hists):
        with torch.no_grad():
            U = m.users_(*user_batch(us, hists))
            I = m.items_(all_items)
            return (U @ I.T).numpy()

    seen_w = {u: set(hist_train[u]) for u in warm_eval}
    cold_users = list(cold_hist)
    seen_c = {u: set(cold_hist[u]) for u in cold_users}

    prior = np.log((pop + 1) / (pop + 1).sum())

    def eval_tt():
        """Raw scores are the intended conditional ranking after corrected training.

        Prior-added scores remain an explicitly separate popularity-weighted ablation.
        Finite neural fits need not attain the ideal conditional optimum.
        """
        Sw = tower_scores(warm_eval, [hist_train[u] for u in warm_eval]) / TT_TAU
        Sc = tower_scores(cold_users, [cold_hist[u] for u in cold_users]) / TT_TAU
        out = []
        for add in (0.0, 1.0):
            out.append(recall(lambda u: Sw[warm_eval.index(u)] + add * prior, warm_eval, warm_target, seen_w))
            out.append(recall(lambda u: Sc[cold_users.index(u)] + add * prior, cold_users, cold_target, seen_c))
        return out

    curve = []
    for step in range(1, TT_STEPS + 1):
        j = g.choice(tr_pos, TT_BATCH, replace=False)
        us, its = users[j], items[j]
        hists = []
        for u, i in zip(us, its):
            h = [x for x in hist_train[u] if x != i]
            hists.append(h[:50])
        U = m.users_(*user_batch(us, hists))
        I = m.items_(torch.tensor(its))
        logits = U @ I.T / TT_TAU
        # in-batch softmax, corrected for how often each film appears as a negative (Yi et al. 2019)
        logits = logits - torch.tensor(np.log(pop[its] / pop.sum() + 1e-9))[None]
        same = torch.tensor(its[:, None] == its[None, :]) & ~torch.eye(len(its), dtype=torch.bool)
        logits = logits.masked_fill(same, -1e9)
        loss = torch.nn.functional.cross_entropy(logits, torch.arange(len(its)))
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step in (1, 50, 100, 200, 400, 700, 1000, 1500, 2000, 2500, 3000):
            curve.append((step, float(loss.detach()), *eval_tt()))
    # the baseline: recommend the most popular films the user hasn't seen
    r_pop_w = recall(lambda u: pop, warm_eval, warm_target, seen_w)
    r_pop_c = recall(lambda u: pop, cold_users, cold_target, seen_c)
    last = curve[-1]
    return dict(curve=curve, recall_warm=last[2], recall_cold=last[3], recall_warm_prior=last[4],
                recall_cold_prior=last[5], pop_warm=r_pop_w, pop_cold=r_pop_c, n_warm=len(warm_eval),
                n_cold=len(cold_users), dim=TT_DIM, items=N_ITEMS, tau=TT_TAU, steps=TT_STEPS,
                default_inference="raw-conditional-score", metric="macro-recall@10",
                evaluation=dict(warm=retrieval_recall(lambda u: pop, warm_eval, warm_target, seen_w),
                                cold=retrieval_recall(lambda u: pop, cold_users, cold_target, seen_c)),
                prior_ablation="raw-score-plus-log-smoothed-popularity")


def item_recipe(name):
    recipes = {
        "gpt2": dict(neighbours="explicit-self-mask-stable-ties-v1", candidate_cap=79,
                     returned_cap=6, queries=NEIGHBOUR_WORDS),
        "norms": dict(random_shape=[768, 3072], random_seed=21, reference="single-MLP-shape"),
        "mp": dict(ks="two-sided-empirical-v1", edge_margin=0.0, min_tail=10),
        "galore": dict(ns_initialization="frobenius-plus-1e-7", ns_steps=5,
                       ns_coefficients=[3.4445, -4.7750, 2.0315], cfg=GL_CFG, steps=GL_STEPS,
                       batch=GL_BATCH, lrs=GL_LRS, methods=GL_METHODS, refresh=GL_REFRESH, scale=GL_SCALE),
        "words": dict(vocab=VOCAB, window=WINDOW, dim=DIM, normalization="ai1-to27-v1",
                      context="symmetric-original-token-positions", smoothing=0.75, svd_seed=0,
                      neighbours="explicit-self-mask-stable-ties-nonzero-v1"),
        "sgns": dict(vocab=VOCAB, window=WINDOW, dim=DIM, epochs=SG_EPOCHS, batch=SG_B,
                     negatives=SG_K, seed=7, torch_seed=0, subsample=1e-4, negative_power=0.75,
                     context="symmetric-subsampled-sequence-v1", optimizer="Adam", lr=0.003,
                     betas=[0.9, 0.999], eps=1e-8, dtype="float32", checkpoint="epoch-v1",
                     exact=dict(vocab=300, dims=[300, 30, 5], iterations=3000),
                     neighbours="explicit-self-mask-stable-ties-nonzero-v1"),
        "jl": dict(delta=JL_DELTA, squared_error=JL_EPS, bound="two-tail-union-v2"),
        "mf": dict(ranks=MF_RANKS, lams=MF_LAMS, epochs=MF_EPOCHS, seed=2006,
                   final_fit="train|valid", bias_penalty=0.01, evaluation_clip=[1, 5]),
        "twotower": dict(dim=TT_DIM, steps=TT_STEPS, batch=TT_BATCH, tau=TT_TAU,
                         metric="macro-recall-distinct-unseen-v1", inference="raw-conditional-score",
                         training="in-batch-log-q-correction", q="positive-train-frequency-plus-1e-9",
                         seed=2016, history_seed=5, torch_seed=0, world_seed=2006),
    }
    if name in ("words", "sgns"):
        recipes[name].update(queries=BOOK_WORDS, analogies=[list(row) for row in ANALOGIES],
                             relations=RELATIONS, categories=CATEGORIES)
    return recipes[name]


def tidy(x, top=True):
    """Arrays nested inside dicts or lists become lists (the cache keeps only top-level arrays in its .npz)."""
    if isinstance(x, dict):
        return {k: (v if top and isinstance(v, np.ndarray) else tidy(v, False)) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [tidy(v, False) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    return x


def tidied(f):
    def g():
        return tidy(f())

    g.__name__ = f.__name__
    return g


ITEMS = {
    "gpt2": compute_gpt2,
    "einsum": compute_einsum,
    "project": compute_project,
    "letters": compute_letters,
    "power": compute_power,
    "image": compute_image,
    "norms": compute_norms,
    "depth": compute_depth,
    "mp": compute_mp,
    "galore": compute_galore,
    "galorectl": compute_galorectl,
    "words": compute_words,
    "sgns": compute_sgns,
    "highdim": compute_highdim,
    "jl": compute_jl,
    "mf": compute_mf,
    "twotower": compute_twotower,
}
ITEMS = {k: tidied(f) for k, f in ITEMS.items()}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
