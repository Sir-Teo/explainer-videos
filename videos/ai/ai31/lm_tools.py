"""Part 31's experiments on the series' own language model (``explainer/ai/novels.py``: 6.8 million parameters,
trained on Part 1's thirty novels).

* :func:`passage_bits`: the model on the Falcon passage, paragraph by paragraph (the scoreboard's row);
* :func:`shannon_game`: Shannon's sentence played letter by letter: the model's guesses among 27 symbols, its
  token-level probabilities turned into next-letter probabilities by summing over every way the tokens can spell
  the next letter;
* :func:`extraction`: training text against held-out text: does greedy decoding reproduce the next 32 tokens
  (Carlini et al. 2023, Definition 3.1)?  Checked with one teacher-forced pass: greedy decoding reproduces the
  continuation exactly when, at every position of it, the model's top token is the true next token;
* :func:`pretrain_weak`, :func:`weak_to_strong`: Burns et al. (2023) in miniature, on Part 27's which-book task.
"""

from __future__ import annotations

import copy
import math
import os

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from explainer.ai import novels as N
from explainer.tts import REPO_ROOT

THREADS = int(os.environ.get("AI31_THREADS", "2"))
torch.set_num_threads(THREADS)
OUT = REPO_ROOT / ".cache" / "ai31"


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def _passage() -> str:
    from videos.ai.ai1 import compute as c1

    return c1.text("passage")


# ---------------------------------------------------------------------------
# The scoreboard's passage
# ---------------------------------------------------------------------------
@torch.no_grad()
def passage_bits(window: int = 256, stride: int = 128) -> dict:
    """Bits for every token of the passage (each paragraph encoded with its closing newline, as the training text
    was), with at least ``window - stride`` tokens of context after the start; summed per paragraph."""
    from videos.ai.ai31 import compute as C

    model = N.load_base()
    passage = _passage()
    paras = passage.split("\n")
    ids, owner = [N.special("<|endoftext|>")], [-1]
    for k, p in enumerate(paras):
        t = N.encode(p + ("\n" if k < len(paras) - 1 else ""))
        ids += t
        owner += [k] * len(t)
    ids_t = torch.tensor(ids)
    bits = np.zeros(len(ids))
    done = 1  # ids[0] is the start marker, not scored
    while done < len(ids):
        start = max(0, done - (window - stride)) if done > 1 else 0
        end = min(len(ids), start + window)
        logits = model(ids_t[start:end][None])[0]
        lp = torch.log_softmax(logits.float(), -1)
        for pos in range(max(done, start + 1), end):
            bits[pos] = -float(lp[pos - 1 - start, ids[pos]]) / math.log(2)
        done = end
    owner = np.array(owner)
    n_par = len(paras)
    par_bits = np.bincount(owner[1:], bits[1:], n_par)
    par_chars = np.array([len(p) + (1 if k < n_par - 1 else 0) for k, p in enumerate(paras)], float)
    assert par_chars.sum() == len(passage)
    bpc = float(par_bits.sum() / len(passage))
    # bootstrap and the paired comparison with Part 1's best counting model, on the same resamples as `measure`
    m = C.load("measure")
    g = C.rng(0)
    idx = g.integers(0, n_par, (m["boots"], n_par))
    r_nov = par_bits[idx].sum(1) / par_chars[idx].sum(1)
    b4, n4 = np.asarray(m["par_bits_4"]), np.asarray(m["par_n_4"])
    r4 = b4[idx].sum(1) / n4[idx].sum(1)
    diff = r4 - r_nov
    pb_nov, pb_4 = par_bits / par_chars, b4 / np.maximum(n4, 1)
    params = int(sum(p.numel() for p in model.parameters()))
    return dict(bpc=bpc, tokens=len(ids) - 1, chars=len(passage), par_bits=par_bits, par_chars=par_chars,
                ci=(float(np.percentile(r_nov, 2.5)), float(np.percentile(r_nov, 97.5))),
                diff_ci=(float(np.percentile(diff, 2.5)), float(np.percentile(diff, 97.5))),
                diff=float(np.mean(r4) - np.mean(r_nov)), par_better=int((pb_nov < pb_4).sum()), params=params)


# ---------------------------------------------------------------------------
# Shannon's guessing game, played by a token model
# ---------------------------------------------------------------------------
ALPHA27 = " abcdefghijklmnopqrstuvwxyz"


def _vocab_strings() -> list[str]:
    tok = N.tokenizer()
    out = []
    for i in range(tok.get_vocab_size()):
        s = N.decode([i])
        out.append("" if s.startswith("<|") and s.endswith("|>") else s)
    return out


@torch.no_grad()
def next_char_dist(model, vocab, ctx_ids: list[int], tail: str, floor: float = 1e-5) -> dict:
    """P(next character | context tokens, then the characters ``tail``): sum over every token path that spells
    ``tail`` and goes on, by the token that runs past it (paths below ``floor`` are dropped)."""
    acc: dict = {}
    stack = [(list(ctx_ids), tail, 1.0)]
    calls = 0
    while stack:
        ids, w_str, w = stack.pop()
        p = torch.softmax(model(torch.tensor([ids[-model.cfg.seq:]]))[0, -1].float(), -1).numpy()
        calls += 1
        for t in np.flatnonzero(p * w > floor * 1e-3):
            s = vocab[t]
            if not s:
                continue
            q = float(p[t]) * w
            if len(s) > len(w_str) and s.startswith(w_str):
                c = s[len(w_str)]
                acc[c] = acc.get(c, 0.0) + q
            elif w_str.startswith(s) and q > floor:
                stack.append((ids + [int(t)], w_str[len(s):], q))
    return acc


def shannon_game() -> dict:
    from videos.ai.ai1 import compute as c1

    model = N.load_base()
    vocab = _vocab_strings()
    sent = c1.SHANNON_SENTENCE
    prefix = "he said "  # the context Part 1's counting model was given
    ranks, bits, top, mass27, floors = [], [], [], [], []
    for i in range(len(sent)):
        full = prefix + sent[:i]
        cut = full.rfind(" ")
        head, tail = full[:cut], full[cut:]
        ctx = [N.special("<|endoftext|>")] + N.encode(head)
        floor = 1e-5
        while True:  # a rare word's spellings can all fall below the floor: lower it until one survives
            acc = next_char_dist(model, vocab, ctx, tail, floor)
            p = np.zeros(27)
            for ch, v in acc.items():
                c = ch.lower()
                if c in ALPHA27:
                    p[ALPHA27.index(c)] += v
            if p.sum() > 0 or floor < 1e-11:
                break
            floor /= 100
        floors.append(floor)
        mass27.append(float(p.sum()))
        if p.sum() == 0:
            p = np.ones(27)  # nothing to go on: every letter equally likely
        p = p / p.sum()
        true = ALPHA27.index(sent[i])
        order = np.argsort(-p, kind="stable")
        ranks.append(int(np.flatnonzero(order == true)[0]) + 1)
        bits.append(float(-math.log2(max(p[true], 1e-12))))
        top.append("".join(ALPHA27[k] for k in order[:3]))
    g = c1.load("game")
    r = np.array(ranks)
    return dict(sentence=sent, ranks=ranks, bits=bits, top3=top, total=float(sum(bits)),
                first=float((r == 1).mean()), mean_mass27=float(np.mean(mass27)), floors=floors,
                count_ranks=[int(x) for x in g["sentence_ranks"]], count_total=float(g["sentence_total"]),
                count_first=float(np.mean(np.array(g["sentence_ranks"]) == 1)), count_order=int(g["sentence_order"]))


# ---------------------------------------------------------------------------
# Extraction and membership
# ---------------------------------------------------------------------------
@torch.no_grad()
def _greedy_correct(model, windows: np.ndarray, batch: int = 32):
    """For each window: whether the model's top next token is right at each position, and the loss there."""
    ok, loss = [], []
    for k in range(0, len(windows), batch):
        x = torch.from_numpy(windows[k:k + batch].astype(np.int64))
        logits = model(x[:, :-1]).float()
        ok.append((logits.argmax(-1) == x[:, 1:]).numpy())
        loss.append(F.cross_entropy(logits.transpose(1, 2), x[:, 1:], reduction="none").numpy())
    return np.concatenate(ok), np.concatenate(loss)


def _wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def _clean(ids) -> str | None:
    """The tokens as text, or None if they split a character (a token boundary inside a UTF-8 sequence)."""
    t = N.decode(ids)
    return None if "\ufffd" in t else t


@torch.no_grad()
def _example(model, W, k, cont, ext, first_miss) -> dict:
    """A passage to show: the first one reproduced exactly, else the one greedy decoding followed longest; among
    passages whose prompt end and continuation decode to whole characters.  With the model's greedy continuation."""
    ok = [j for j in range(len(W)) if _clean(W[j, k - 24:k]) is not None and _clean(W[j, k:k + cont]) is not None]
    hit = [j for j in ok if ext[j]]
    j = hit[0] if hit else max(ok, key=lambda i: (first_miss[i], -i))
    x = torch.from_numpy(W[j, :k].astype(np.int64))[None]
    gen = []
    for _ in range(cont):
        nxt = int(model(x[:, -model.cfg.seq:])[0, -1].argmax())
        gen.append(nxt)
        x = torch.cat([x, torch.tensor([[nxt]])], 1)
    lead = int(first_miss[j])
    return dict(prefix=N.decode(W[j, k - 24:k]), truth=N.decode(W[j, k:k + cont]), greedy=N.decode(gen),
                same=N.decode(W[j, k:k + lead]), extracted=bool(ext[j]), lead=lead)


def extraction(n_win: int = 800, L: int = 256, cont: int = 32, prefixes=(8, 16, 32, 64, 128, 192, 224)) -> dict:
    model = N.load_base()
    train, valid = N.token_arrays()
    eot = N.special("<|endoftext|>")
    g = rng(71)

    def sample(arr, n):
        out = []
        while len(out) < n:
            s = int(g.integers(0, len(arr) - L - 1))
            w = arr[s:s + L]
            if eot not in w:
                out.append(w)
        return np.stack(out)

    res = {}
    examples = {}
    for name, arr in (("train", train), ("valid", valid)):
        W = sample(arr, n_win)
        ok, loss = _greedy_correct(model, W)
        rates, lo, hi, lead = [], [], [], []
        for k in prefixes:
            seg = ok[:, k - 1:k - 1 + cont]  # predictions of tokens k .. k + cont - 1
            ext = seg.all(1)
            rates.append(float(ext.mean()))
            a, b = _wilson(int(ext.sum()), len(ext))
            lo.append(a)
            hi.append(b)
            first_miss = np.where(seg.all(1), cont, np.argmin(seg, 1))
            lead.append(float(first_miss.mean()))
            if k == 64:
                examples[name] = _example(model, W, k, cont, ext, first_miss)
        res[name] = dict(rate=rates, lo=lo, hi=hi, lead=lead, win_loss=loss[:, 63:].mean(1).tolist())
    # membership: a loss threshold (Yeom et al. 2018) separating training windows from held-out ones
    lt, lv = np.array(res["train"]["win_loss"]), np.array(res["valid"]["win_loss"])
    auc = float((lt[:, None] < lv[None, :]).mean() + 0.5 * (lt[:, None] == lv[None, :]).mean())
    # duplication: continuations that occur once, twice to four times, five or more times in the training text
    T = len(train) - cont
    h = np.zeros(T, np.int64)
    a64 = train.astype(np.int64)
    with np.errstate(over="ignore"):
        for k in range(cont):
            h = h * np.int64(4099) + a64[k:T + k]
    uniq, inv, counts = np.unique(h, return_inverse=True, return_counts=True)
    dup = counts[inv]
    buckets = [(1, 1), (2, 4), (5, 10 ** 9)]
    dup_rate, dup_n, dup_ci = [], [], []
    for lo_, hi_ in buckets:
        pos = np.flatnonzero((dup >= lo_) & (dup <= hi_))
        pos = pos[pos >= 64]
        if len(pos) == 0:
            dup_rate.append(float("nan"))
            dup_n.append(0)
            dup_ci.append((0.0, 0.0))
            continue
        pick = g.choice(pos, min(400, len(pos)), replace=False)
        Wd = np.stack([train[p - 64:p + cont] for p in pick])
        ok, _ = _greedy_correct(model, Wd)
        ext = ok[:, 63:63 + cont].all(1)
        dup_rate.append(float(ext.mean()))
        dup_n.append(int(len(pick)))
        dup_ci.append(_wilson(int(ext.sum()), len(ext)))
    return dict(prefixes=list(prefixes), cont=cont, n_win=n_win, train=res["train"], valid=res["valid"], auc=auc,
                examples=examples, dup_buckets=["1", "2-4", "5+"], dup_rate=dup_rate, dup_n=dup_n, dup_ci=dup_ci,
                dup_positions=[int(((dup >= a) & (dup <= b)).sum()) for a, b in buckets],
                train_tokens=int(len(train)), epochs=float(N.BASE_RUN["tokens"] / len(train)))


# ---------------------------------------------------------------------------
# Weak-to-strong generalization (Burns et al. 2023), on Part 27's which-book task
# ---------------------------------------------------------------------------
WEAK_CFG = dict(d=128, layers=2, heads=4, seq=256)


def pretrain_weak(tokens: int = 2_000_000, batch: int = 16, lr: float = 3e-3, seed: int = 0) -> dict:
    """The weak supervisor's base: a 2-layer model pretrained on the same novels, as Part 27's distillation student
    (2 million tokens), checkpointed every 100 steps so a killed run resumes."""
    from explainer.lm import pocket
    from videos.ai.ai27 import post as P

    train, valid = N.token_arrays()
    cfg = pocket.Config(vocab=N.tokenizer().get_vocab_size(), **WEAK_CFG)
    run = pocket.Run(model=cfg, lr=lr, batch=batch, tokens=tokens, seed=seed)
    data = pocket.TokenStream(train, valid, cfg.seq, seed=1)
    OUT.mkdir(parents=True, exist_ok=True)
    res = pocket.train(run, data, threads=THREADS, verbose=True, ckpt=OUT / "weak_base.ckpt", ckpt_every=100)
    model = res.pop("_model").eval()
    res.pop("_opts")
    torch.save({"config": WEAK_CFG, "model": model.state_dict()}, OUT / "weak_base.pt.tmp")
    (OUT / "weak_base.pt.tmp").replace(OUT / "weak_base.pt")
    (OUT / "weak_base.ckpt").unlink(missing_ok=True)
    return dict(params=int(sum(p.numel() for p in model.parameters())), tokens=tokens, steps=res["steps"],
                curve=np.array([c[:2] for c in res["curve"]]), heldout=P.heldout_loss(model, valid))


def _load_weak():
    """The weak supervisor's base model (pretrained first, resuming, if it isn't saved yet)."""
    from explainer.lm import pocket

    if not (OUT / "weak_base.pt").exists():
        from videos.ai.ai31.compute import CACHE

        CACHE.save("weak", pretrain_weak())

    ck = torch.load(OUT / "weak_base.pt")
    m = pocket.PocketGPT(pocket.Config(vocab=N.tokenizer().get_vocab_size(), **ck["config"]))
    m.load_state_dict(ck["model"])
    return m.eval()


def _which_data():
    """Part 27's which-book questions, through its own compute module (so tools/make.py computes it first)."""
    from videos.ai.ai27 import compute as c27

    d = c27.load("data")
    return d["which_train"], d["which_test"], d["titles"]


def _encode_questions(rows, titles):
    from videos.ai.ai27 import compute as c27
    from videos.ai.ai27 import post as P

    ids = [P.chat(c27.which_q(s)) for s, _ in rows]
    y = np.array([titles.index(t) for _, t in rows])
    return ids, y


def _pad(ids_list):
    T = max(len(x) for x in ids_list)
    x = torch.zeros((len(ids_list), T), dtype=torch.long)
    last = torch.tensor([len(r) - 1 for r in ids_list])
    for k, r in enumerate(ids_list):
        x[k, :len(r)] = torch.tensor(r)
    return x, last


class Head(nn.Module):
    """Classify a question from the hidden state at its last token (the <|assistant|> marker): the model's final
    norm, then a new linear layer over the 30 titles (zero at the start)."""

    def __init__(self, body, n_classes):
        super().__init__()
        self.norm = copy.deepcopy(body.norm)
        self.out = nn.Linear(body.cfg.d, n_classes)
        nn.init.zeros_(self.out.weight)
        nn.init.zeros_(self.out.bias)

    def forward(self, h, last):
        return self.out(self.norm(h[torch.arange(len(h)), last]))


@torch.no_grad()
def _hidden(model, ids_list, upto, batch=64):
    """Hidden states after the first ``upto`` blocks, padded to the longest question."""
    T = max(len(x) for x in ids_list)
    outs = []
    for k in range(0, len(ids_list), batch):
        x, _ = _pad(ids_list[k:k + batch])
        x = F.pad(x, (0, T - x.shape[1]))
        h = model.emb(x)
        for b in model.blocks[:upto]:
            h = b(h)
        outs.append(h.half())
    return torch.cat(outs)


def _block_at_last(block, x, last):
    """A transformer block's output at position ``last`` of each row only, which is all the classifier reads: keys
    and values for every position, but the query, the attention output and the MLP only there.  The same function
    as ``block(x)[arange, last]`` (causal attention: positions after ``last`` are never seen), at about a fifth of
    the work."""
    from explainer.lm.pocket import apply_rope

    B, T, D = x.shape
    a = block.attn
    h = block.n1(x)
    W = a.qkv.weight  # rows: q, k, v
    k, v = F.linear(h, W[D:]).view(B, T, 2, a.h, a.hd).permute(2, 0, 3, 1, 4)
    k = apply_rope(k, a.cos, a.sin)
    rows = torch.arange(B)
    q = F.linear(h[rows, last], W[:D]).view(B, a.h, 1, a.hd)
    c, s_ = a.cos[0, 0, last][:, None, None, :], a.sin[0, 0, last][:, None, None, :]
    q1, q2 = q[..., ::2], q[..., 1::2]
    q = torch.stack([q1 * c - q2 * s_, q1 * s_ + q2 * c], dim=-1).flatten(-2)
    if a.qk_norm:
        raise NotImplementedError("qk_norm")
    mask = (torch.arange(T)[None, :] <= last[:, None])[:, None, None, :]
    y = F.scaled_dot_product_attention(q, k, v, attn_mask=mask)
    xl = x[rows, last] + a.out(y.transpose(1, 2).reshape(B, D))
    return xl + block.mlp(block.n2(xl))


def _train_classifier(blocks, head, H, last, targets, steps, lr, seed, batch=32, conf=0.0, evals=None):
    """Train ``blocks`` (applied to the cached hidden states H) and ``head`` on soft ``targets`` (rows sum to 1).
    ``conf``: Burns et al.'s auxiliary confidence loss, weight warmed up from 0 to ``conf`` over the first 20% of
    training: the target becomes (1 - a) weak + a onehot(own prediction).  ``evals``: (H_test, last_test, y_test,
    every) to record test accuracy as it trains."""
    torch.manual_seed(seed)
    g = torch.Generator().manual_seed(seed)
    params = [p for b in blocks for p in b.parameters()] + list(head.parameters())
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.0)
    hist = []

    def run(h, l):
        h = h[:, :int(l.max()) + 1]  # causal: positions after the last question token change nothing
        for b in blocks[:-1]:
            h = b(h)
        return head.out(head.norm(_block_at_last(blocks[-1], h, l)))

    def acc(Ht, lt, yt):
        with torch.no_grad():
            for b in blocks:
                b.eval()
            preds = torch.cat([run(Ht[k:k + 128].float(), lt[k:k + 128]).argmax(-1) for k in range(0, len(Ht), 128)])
            for b in blocks:
                b.train()
        return float((preds.numpy() == yt).mean())

    n = len(H)
    for step in range(steps):
        cur = lr * min(1.0, (step + 1) / 20) * 0.5 * (1 + math.cos(math.pi * step / steps))
        for gr in opt.param_groups:
            gr["lr"] = cur
        k = torch.randint(0, n, (batch,), generator=g)
        z = run(H[k].float(), last[k])
        tgt = targets[k]
        if conf:
            a = conf * min(1.0, step / (0.2 * steps))
            hard = F.one_hot(z.detach().argmax(-1), tgt.shape[1]).float()
            tgt = (1 - a) * tgt + a * hard
        loss = -(tgt * F.log_softmax(z, -1)).sum(-1).mean()
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        if evals and ((step + 1) % evals[3] == 0 or step == steps - 1):
            hist.append((step + 1, acc(*evals[:3])))
    final = acc(*evals[:3]) if evals else None
    return final, hist, run


def weak_to_strong(seeds: int = 3, steps: int = 300, lr_weak: float = 1e-3, lr_strong: float = 5e-4,
                   strong_top: int = 1, conf: float = 0.5, part=None) -> dict:
    """Per seed: a weak supervisor (the 2-layer model, fine-tuned whole on ground truth for half the training
    questions) labels the other half; the strong model (its last ``strong_top`` blocks and a new head) is fine-tuned
    on those labels (naively, and with the confidence loss), and, as the ceiling, on the true labels; all on equal
    budgets.  PGR = (weak-to-strong - weak) / (ceiling - weak) on the held-out questions.  ``part``: a Cache.partial
    holding finished seeds (each seed is independent and seeded, so a killed run resumes with the same numbers)."""
    rows_tr, rows_te, titles = _which_data()
    ids_tr, y_tr = _encode_questions(rows_tr, titles)
    ids_te, y_te = _encode_questions(rows_te, titles)
    torch.set_num_threads(THREADS)  # importing Part 27's compute module sets its own thread count
    C = len(titles)
    strong = N.load_base()
    weak_base = _load_weak()
    L = len(strong.blocks)
    up = L - strong_top
    H_all = _hidden(strong, ids_tr + ids_te, up)
    H_tr, H_te = H_all[:len(ids_tr)], H_all[len(ids_tr):]
    _, last_tr = _pad(ids_tr)
    _, last_te = _pad(ids_te)
    Hw_all = _hidden(weak_base, ids_tr + ids_te, 0)  # the weak model's embeddings: all its blocks are trained
    Hw_tr, Hw_te = Hw_all[:len(ids_tr)], Hw_all[len(ids_tr):]
    from videos.ai.ai27 import post as P

    _, valid = N.token_arrays()
    out = dict(seeds=seeds, steps=steps, n_train=len(ids_tr), n_test=len(ids_te), classes=C, chance=1 / C,
               strong_top=strong_top, strong_layers=L, weak_layers=len(weak_base.blocks), conf=conf,
               strong_params=int(sum(p.numel() for p in strong.parameters())),
               weak_params=int(sum(p.numel() for p in weak_base.parameters())),
               strong_heldout=P.heldout_loss(strong, valid), weak_heldout=P.heldout_loss(weak_base, valid))
    res = {k: [] for k in ("weak", "w2s", "w2s_conf", "ceiling", "agree_wrong", "agree_wrong_conf")}
    curves = {k: [] for k in ("w2s", "w2s_conf", "ceiling")}
    def one(sd):
        r = {k: None for k in res}
        cv = {}
        perm = rng(1000 + sd).permutation(len(ids_tr))
        A, B = perm[: len(perm) // 2], perm[len(perm) // 2:]
        onehot = lambda y: F.one_hot(torch.as_tensor(y), C).float()  # noqa: E731
        # the weak supervisor: the 2-layer model, all its blocks fine-tuned, on half A's true labels
        wb = [copy.deepcopy(b) for b in weak_base.blocks]
        wh = Head(weak_base, C)
        wacc, _, wrun = _train_classifier(wb, wh, Hw_tr[A], last_tr[A], onehot(y_tr[A]), steps, lr_weak, sd,
                                          evals=(Hw_te, last_te, y_te, steps))
        with torch.no_grad():
            for b in wb:
                b.eval()
            soft_B = torch.cat([F.softmax(wrun(Hw_tr[B][k:k + 128].float(), last_tr[B][k:k + 128]), -1)
                                for k in range(0, len(B), 128)])
            weak_test = torch.cat([wrun(Hw_te[k:k + 128].float(), last_te[k:k + 128]).argmax(-1)
                                   for k in range(0, len(ids_te), 128)]).numpy()
        r["weak"] = wacc
        every = max(1, steps // 6)
        for name, tgt, c in (("ceiling", onehot(y_tr[B]), 0.0), ("w2s", soft_B, 0.0), ("w2s_conf", soft_B, conf)):
            sb = [copy.deepcopy(b) for b in strong.blocks[up:]]
            sh = Head(strong, C)
            acc, hist, srun = _train_classifier(sb, sh, H_tr[B], last_tr[B], tgt, steps, lr_strong, sd, conf=c,
                                                evals=(H_te, last_te, y_te, every))
            r[name] = acc
            cv[name] = [list(h) for h in hist]
            if name != "ceiling":
                with torch.no_grad():
                    for b in sb:
                        b.eval()
                    pred = torch.cat([srun(H_te[k:k + 128].float(), last_te[k:k + 128]).argmax(-1)
                                      for k in range(0, len(ids_te), 128)]).numpy()
                wrong = weak_test != y_te
                key = "agree_wrong" if name == "w2s" else "agree_wrong_conf"
                r[key] = float((pred[wrong] == weak_test[wrong]).mean())
        print(f"    seed {sd}: weak {r['weak']:.3f}  w2s {r['w2s']:.3f}  conf {r['w2s_conf']:.3f}  "
              f"ceiling {r['ceiling']:.3f}", flush=True)
        return dict(res=r, curves=cv)

    for sd in range(seeds):
        if part is not None and str(sd) in part:
            piece = part[str(sd)]
        else:
            piece = one(sd)
            if part is not None:
                part[str(sd)] = piece
        for k in res:
            res[k].append(piece["res"][k])
        for k in curves:
            curves[k].append(piece["curves"][k])

    for k, v in res.items():
        out[k] = np.array(v)
    w, s, c, ce = (np.array(res[k]) for k in ("weak", "w2s", "w2s_conf", "ceiling"))
    out["pgr"] = (s - w) / (ce - w)
    out["pgr_conf"] = (c - w) / (ce - w)
    for k, v in curves.items():
        out[f"curve_{k}"] = np.array(v)
    return out
