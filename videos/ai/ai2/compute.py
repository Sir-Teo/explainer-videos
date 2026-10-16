"""Precompute everything numerical in Part 2 of the AI series ("Vectors That Mean Things").

    python -m videos.ai.ai2.compute              # everything missing (Part 1's books are reused: .cache/ai1)
    python -m videos.ai.ai2.compute words jl     # specific items
    python -m videos.ai.ai2.compute --force gpt2 # recompute

Results are cached in ``.cache/ai2/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Every number the
narration quotes is computed here and asserted against the statement it illustrates.

Items:
    gpt2      GPT-2's token vectors (its embedding matrix, 50,257 x 768): neighbours of a few words, a 3D map of seven
              categories of words, the shared direction (anisotropy), and the logits of one prompt as dot products
    letters   the 26 x 26 letter-bigram table of the books: its singular values, its rank-k approximations, and the
              correspondence-analysis axis that puts the vowels at one end
    words     word vectors from the books by counting: co-occurrence (window 4), PPMI, truncated SVD to 100 numbers
    sgns      word2vec (skip-gram, negative sampling) trained on the same books, for comparison
    highdim   random directions in d dimensions: angles, lengths, and how many nearly perpendicular directions fit
    jl        random projections of GPT-2's vectors from 768 numbers down to k: how far distances move
"""

from __future__ import annotations

import collections
import math

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("ai2")
load = CACHE.load

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


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def ai1():
    """Part 1's compute module (the books, the letter tables)."""
    from videos.ai.ai1 import compute as c1

    return c1


def ai1_load(name: str) -> dict:
    c1 = ai1()
    if not c1.path(name).exists():
        c1._save(name, c1.ITEMS[name]())
    return c1.load(name)


# ---------------------------------------------------------------------------
# GPT-2's vectors
# ---------------------------------------------------------------------------
def gpt2():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_grad_enabled(False)
    tok = AutoTokenizer.from_pretrained("openai-community/gpt2")
    model = AutoModelForCausalLM.from_pretrained("openai-community/gpt2", dtype=torch.float32)
    return tok, model


def token_id(tok, word: str) -> int | None:
    ids = tok(" " + word)["input_ids"]
    return ids[0] if len(ids) == 1 else None


def compute_gpt2():
    import torch

    tok, model = gpt2()
    W = model.transformer.wte.weight.numpy()
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
        for j in np.argsort(-sim)[1:60]:
            s = tok.decode([int(j)]).strip()
            if s.lower() == w.lower() or s.lower() in [r[0].lower() for r in res] or not s.isalpha():
                continue
            res.append((s, float(sim[j])))
            if len(res) == 6:
                break
        nb[w] = res
    assert [r[0] for r in nb["Monday"][:3]] == ["Tuesday", "Thursday", "Wednesday"]
    assert "puppy" in [r[0] for r in nb["dog"]] and "queen" in [r[0] for r in nb["king"]]
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
    # separation check: each category's centre is closer to its own words than to any other category's centre
    centres = {c: Y[[k for k, cc in enumerate(cats) if cc == c]].mean(0) for c in CATEGORIES}
    hits = sum(min(centres, key=lambda c: np.linalg.norm(Y[k] - centres[c])) == cats[k] for k in range(len(cats)))
    out["map_hits"] = int(hits)
    assert hits > 0.8 * len(cats), hits
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
    B = W[common] - W.mean(0)
    B /= np.linalg.norm(B, axis=1, keepdims=True)
    c_centred = (B @ B.T)[iu]
    out.update(cos_random_mean=float(c_raw.mean()), cos_random_sd=float(c_raw.std()),
               cos_centred_mean=float(c_centred.mean()), cos_centred_sd=float(c_centred.std()),
               hist_raw=np.histogram(c_raw, bins=60, range=(-0.3, 0.6))[0],
               hist_centred=np.histogram(c_centred, bins=60, range=(-0.3, 0.6))[0])
    assert c_raw.mean() > 0.2 and abs(c_centred.mean()) < 0.02
    # the last step of the model is dot products with the same vectors
    ids = tok(PROMPT)["input_ids"]
    h = model.transformer(torch.tensor([ids])).last_hidden_state[0, -1].numpy()  # after the final layer norm
    logits = W @ h
    ref = model(torch.tensor([ids])).logits[0, -1].numpy()
    assert np.allclose(logits, ref, atol=1e-3)
    p = np.exp(logits - logits.max())
    p /= p.sum()
    top = np.argsort(-logits)[:6]
    out.update(prompt=PROMPT, h_norm=float(np.linalg.norm(h)),
               top_tokens=[tok.decode([int(i)]) for i in top], top_logits=[float(logits[i]) for i in top],
               top_probs=[float(p[i]) for i in top], top_cos=[float(Wn[i] @ h / np.linalg.norm(h)) for i in top])
    assert out["top_tokens"][0] == " Paris"
    return out


# ---------------------------------------------------------------------------
# Letters: the SVD of the bigram table
# ---------------------------------------------------------------------------
def compute_letters():
    J = np.asarray(ai1_load("bigram")["joint"])[1:, 1:]  # letters only: previous x next
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
    if row[0] > 0:  # orient: vowels on the left
        row, col = -row, -col
    letters = "abcdefghijklmnopqrstuvwxyz"
    v = np.array([ch in VOWELS for ch in letters])
    assert row[v].max() < row[~v].min() + 0.6  # all five vowels sit at one end ...
    assert sorted(np.argsort(row)[:5]) == sorted(letters.index(ch) for ch in VOWELS)  # ... the five leftmost
    return dict(M=M, S=S, U=U, Vt=Vt, recon=recon, err=err, total=float(np.linalg.norm(M)), ca_s=Sc[:5],
                ca_row=row, ca_col=col, ca_share=float(Sc[0] ** 2 / (Sc ** 2).sum()))


# ---------------------------------------------------------------------------
# Words from the books
# ---------------------------------------------------------------------------
VOCAB, WINDOW, DIM = 10000, 4, 100


def book_words():
    words = ai1().text("train27").split()
    cnt = collections.Counter(words)
    vocab = [w for w, _ in cnt.most_common(VOCAB)]
    idx = {w: i for i, w in enumerate(vocab)}
    ids = np.array([idx.get(w, -1) for w in words])
    return words, vocab, idx, ids, cnt


def neighbours(E, vocab, idx, w, k=6):
    sim = E @ E[idx[w]]
    return [(vocab[i], float(sim[i])) for i in np.argsort(-sim)[1:k + 1]]


def analogy(E, idx, vocab, a, b, c, k=5):
    v = E[idx[b]] - E[idx[a]] + E[idx[c]]
    sim = E @ (v / np.linalg.norm(v))
    for x in (a, b, c):
        sim[idx[x]] = -9
    return [vocab[i] for i in np.argsort(-sim)[:k]]


def compute_words():
    import scipy.sparse as sp
    from scipy.sparse.linalg import svds

    words, vocab, idx, ids, cnt = book_words()
    rows, cols = [], []
    for d in range(1, WINDOW + 1):
        a, b = ids[:-d], ids[d:]
        m = (a >= 0) & (b >= 0)
        rows.append(a[m]), cols.append(b[m])
    rows, cols = np.concatenate(rows), np.concatenate(cols)
    C = sp.coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(VOCAB, VOCAB)).tocsr()
    C = (C + C.T).tocoo()
    tot = float(C.sum())
    rs = np.asarray(C.tocsr().sum(1)).ravel()
    cs = rs ** 0.75
    cs /= cs.sum()  # context distribution smoothing (Levy, Goldberg & Dagan 2015)
    pmi = np.log(C.data / tot / (rs[C.row] / tot) / cs[C.col])
    keep = pmi > 0
    P = sp.coo_matrix((pmi[keep], (C.row[keep], C.col[keep])), shape=(VOCAB, VOCAB)).tocsr()
    u, s, _ = svds(P, k=DIM)
    o = np.argsort(-s)
    u, s = u[:, o], s[o]
    E = u * np.sqrt(s)
    E /= np.linalg.norm(E, axis=1, keepdims=True)
    nb = {w: neighbours(E, vocab, idx, w) for w in BOOK_WORDS}
    an = {f"{a}:{b}::{c}": analogy(E, idx, vocab, a, b, c) for a, b, c in ANALOGIES}
    assert {"wolf", "cat", "horse"} & {w for w, _ in nb["dog"]}
    assert nb["monday"][0][0] in ("saturday", "tuesday", "sunday") and nb["three"][0][0] in ("four", "two", "five")
    assert an["france:paris::england"][0] == "london" and "queen" in an["man:king::woman"][:2]
    # a 2D picture of the analogy: the four words on the plane of their two differences
    fp = [idx[w] for w in ("france", "paris", "england", "london")]
    D = np.stack([E[fp[1]] - E[fp[0]], E[fp[2]] - E[fp[0]]])
    Q, _ = np.linalg.qr(D.T)
    xy = (E[fp] - E[fp].mean(0)) @ Q
    T = np.asarray(P[:300, :300].todense(), np.float32)  # the corner of the table among the 300 commonest words
    return dict(vocab=vocab, n_words=len(words), n_pairs=int(len(rows) * 2), density=float(keep.mean()), top300=T,
                nnz=int(P.nnz), s=s, E=E.astype(np.float32), neighbours=nb, analogies=an, analogy_xy=xy,
                counts=[int(cnt[w]) for w in vocab[:20]])


def compute_sgns():
    """Skip-gram with negative sampling (Mikolov et al. 2013) on the books, the same 10,000 words and window."""
    import torch

    torch.set_grad_enabled(True)  # (the GPT-2 items switch it off)
    torch.manual_seed(0)
    words, vocab, idx, ids, cnt = book_words()
    freq = np.array([cnt[w] for w in vocab], float)
    f = freq / freq.sum()
    keep_p = np.minimum(1.0, np.sqrt(1e-4 / f) + 1e-4 / f)  # subsample very frequent words
    g = rng(7)
    seq = ids[(ids >= 0)]
    seq = seq[g.random(len(seq)) < keep_p[seq]]
    neg_p = torch.tensor(freq ** 0.75 / (freq ** 0.75).sum(), dtype=torch.float32)
    E_in = torch.nn.Embedding(VOCAB, DIM)
    E_out = torch.nn.Embedding(VOCAB, DIM)
    torch.nn.init.uniform_(E_in.weight, -0.5 / DIM, 0.5 / DIM)
    torch.nn.init.zeros_(E_out.weight)
    opt = torch.optim.Adam(list(E_in.parameters()) + list(E_out.parameters()), lr=0.003)
    centre = np.concatenate([seq[:-d] for d in range(1, WINDOW + 1)] + [seq[d:] for d in range(1, WINDOW + 1)])
    context = np.concatenate([seq[d:] for d in range(1, WINDOW + 1)] + [seq[:-d] for d in range(1, WINDOW + 1)])
    B, K, losses = 4096, 5, []
    for epoch in range(3):
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
            losses.append(float(loss))
    E = E_in.weight.detach().numpy()
    E = E / np.linalg.norm(E, axis=1, keepdims=True)
    nb = {w: neighbours(E, vocab, idx, w) for w in BOOK_WORDS}
    an = {f"{a}:{b}::{c}": analogy(E, idx, vocab, a, b, c) for a, b, c in ANALOGIES}
    svd = load("words")
    Es = np.asarray(svd["E"])
    overlap = {w: len({x for x, _ in nb[w]} & {x for x, _ in neighbours(Es, vocab, idx, w)}) for w in BOOK_WORDS}
    assert losses[-1] < losses[0] - 1.0
    return dict(neighbours=nb, analogies=an, loss=np.array(losses[::200]), pairs=int(len(centre) * 2), overlap=overlap,
                steps=len(losses))


# ---------------------------------------------------------------------------
# High dimensions
# ---------------------------------------------------------------------------
DIMS = [2, 3, 10, 100, 768]


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
    assert out["angle_sd768"] < 2.2 and out["angle_sd2"] > 45
    # the volume of a ball lies near its surface: the share within 1% of the radius, (1 - 0.99^d)
    out["shell"] = {str(d): 1 - 0.99 ** d for d in DIMS}
    # many directions, all nearly perpendicular: 10,000 random directions in 768 dimensions
    A = g.normal(size=(10000, 768)).astype(np.float32)
    A /= np.linalg.norm(A, axis=1, keepdims=True)
    G = A @ A.T
    np.fill_diagonal(G, 0)
    worst = float(np.abs(G).max())
    out.update(n_dirs=10000, worst_cos=worst, worst_angle=float(np.degrees(np.arccos(worst))))
    assert worst < 0.25
    return out


# ---------------------------------------------------------------------------
# Depth: a vector through many random layers
# ---------------------------------------------------------------------------
def compute_depth():
    """x -> W_l x through 40 layers of random 256 x 256 matrices with entries N(0, g^2 / 256): the length is
    multiplied by about g per layer (Part 8's initialization story, in miniature)."""
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
        rate = (lengths[-1] / lengths[0]) ** (1 / L)
        assert abs(rate - gain) < 0.05 * gain, (gain, rate)
    return out


# ---------------------------------------------------------------------------
# Johnson-Lindenstrauss
# ---------------------------------------------------------------------------
KS = [2, 5, 20, 100, 400]


def compute_jl():
    tok, model = gpt2()
    W = model.transformer.wte.weight.numpy()
    g = rng(3)
    pts = W[g.choice(np.arange(1000, 20000), 1000, replace=False)].astype(np.float64)
    i, j = np.triu_indices(len(pts), 1)
    pick = g.choice(len(i), 2000, replace=False)
    i, j = i[pick], j[pick]
    d0 = np.linalg.norm(pts[i] - pts[j], axis=1)
    out = dict(ks=KS, d0=d0, n=len(pts))
    for k in KS:
        R = g.normal(size=(768, k)) / math.sqrt(k)
        P = pts @ R
        d1 = np.linalg.norm(P[i] - P[j], axis=1)
        ratio = d1 / d0
        out[f"d{k}"] = d1
        out[f"band{k}"] = [float(x) for x in np.percentile(ratio, [5, 95])]
        out[f"within10_{k}"] = float(np.mean(np.abs(ratio - 1) < 0.1))
    assert out["band100"][0] > 0.85 and out["band100"][1] < 1.15
    # the JL dimension for n = 1000 points within 10%: k >= 8 ln(n) / eps^2 (a standard constant)
    out["jl_k"] = int(math.ceil(8 * math.log(1000) / 0.1 ** 2))
    return out


ITEMS = {
    "gpt2": compute_gpt2,
    "letters": compute_letters,
    "words": compute_words,
    "sgns": compute_sgns,
    "highdim": compute_highdim,
    "depth": compute_depth,
    "jl": compute_jl,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
