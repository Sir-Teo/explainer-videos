"""Part 14's own lineage, on the series' thirty novels: GPT-style (causal) and BERT-style (masked) models.

Both kinds are ``explainer.lm.pocket``'s PocketGPT (pre-norm RMSNorm, rotary positions, SwiGLU, no biases) with the
same shape and the same initial weights; the masked model's attention looks both ways.  The vocabulary is the
novels' byte-level BPE (4,096 tokens, ``explainer.ai.novels``) plus one ``[MASK]`` token, for both kinds, so the two
have exactly the same parameters.

A run is resumable and seeded: the batch at step s depends only on (seed, s), and the state is checkpointed every
``SAVE_EVERY`` steps to ``.cache/ai14/<name>.ckpt.pt``.  At a few steps along the way (``snap_steps``) the run
freezes the model and records what it can do: held-out loss, the loss at each position of the context, a
repeated-string test, and a sample (GPT) or a fill-in-the-blanks (BERT).  These are the training replays.
"""

from __future__ import annotations

import math
import time

import numpy as np
import torch
import torch.nn.functional as F

from explainer.ai import novels as N
from explainer.lm import pocket

VOCAB, MASK = 4097, 4096  # the novels BPE + [MASK]
SEQ, BATCH = 256, 16
SAVE_EVERY = 100
MASK_RATE, MASK_SPLIT = 0.15, (0.8, 0.1)  # BERT: 15% of positions; 80% [MASK], 10% a random token, 10% kept
PROMPT = "The door opened, and"  # the GPT replay's prompt
FILL = "It was a cold [MASK] in the [MASK] of winter, and the [MASK] was falling."  # the BERT replay's sentence


class BiAttention(pocket.Attention):
    """pocket's attention without the causal mask: every position sees every other."""

    def forward(self, x, probe=False):
        B, T, D = x.shape
        q, k, v = self.qk(x)
        y = F.scaled_dot_product_attention(q, k, v, is_causal=False)
        return self.out(y.transpose(1, 2).reshape(B, T, D))


def build(shape: dict, kind: str, seed: int = 0) -> pocket.PocketGPT:
    """A model of the given shape (d, layers, heads); kind 'gpt' or 'bert'.  The same seed gives both kinds the same
    initial weights."""
    torch.manual_seed(seed)
    cfg = pocket.Config(vocab=VOCAB, seq=SEQ, **shape)
    m = pocket.PocketGPT(cfg)
    if kind == "bert":
        for b in m.blocks:
            a = BiAttention(cfg)
            a.load_state_dict(b.attn.state_dict())
            b.attn = a
    m.kind = kind
    return m


def n_params(m) -> dict:
    c = m.count()
    return dict(total=int(c["total"]), body=int(c["body"]), head=int(c["head"]), compute=int(c["compute"]))


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def batch(train: np.ndarray, seed: int, step: int, B: int = BATCH) -> torch.Tensor:
    g = np.random.default_rng([seed, step])
    ix = g.integers(0, len(train) - SEQ - 1, B)
    return torch.from_numpy(np.stack([train[i:i + SEQ + 1] for i in ix]).astype(np.int64))


def corrupt(x: torch.Tensor, g: np.random.Generator):
    """BERT's corruption of a batch: (input, positions to predict)."""
    B, T = x.shape
    pick = g.random((B, T)) < MASK_RATE
    r = g.random((B, T))
    inp = x.numpy().copy()
    to_mask = pick & (r < MASK_SPLIT[0])
    to_rand = pick & (r >= MASK_SPLIT[0]) & (r < MASK_SPLIT[0] + MASK_SPLIT[1])
    inp[to_mask] = MASK
    inp[to_rand] = g.integers(4, 4096, int(to_rand.sum()))  # never a special token
    return torch.from_numpy(inp), torch.from_numpy(pick)


def val_windows(valid: np.ndarray, n: int = 64) -> torch.Tensor:
    starts = np.linspace(0, len(valid) - SEQ - 2, n).astype(int)
    return torch.from_numpy(np.stack([valid[s:s + SEQ + 1] for s in starts]).astype(np.int64))


def word_tokens(train: np.ndarray, top: int = 2000) -> list[int]:
    """The most frequent tokens that are a whole word with its leading space (' house'), most frequent first."""
    counts = np.bincount(train.astype(np.int64), minlength=4096)
    out = []
    for t in np.argsort(-counts):
        s = N.decode([int(t)])
        if len(s) >= 4 and s[0] == " " and s[1:].isalpha() and s[1:].islower():
            out.append(int(t))
        if len(out) >= top:
            break
    return out


def repeat_batch(words: list[int], n: int = 32, L: int = 60, seed: int = 99) -> torch.Tensor:
    """n sequences: a newline, L random common words, then the same L words again."""
    g = np.random.default_rng(seed)
    nl = N.encode("\n")[0]
    rows = []
    for _ in range(n):
        w = g.choice(words[:1000], L, replace=False)
        rows.append([nl] + list(w) + list(w))
    return torch.tensor(rows, dtype=torch.long)


# ---------------------------------------------------------------------------
# Measurements (any causal model with a .cfg: ours or the series' base model)
# ---------------------------------------------------------------------------
@torch.no_grad()
def per_position(model, windows: torch.Tensor, B: int = 16) -> np.ndarray:
    """Next-token loss (nats) at each position of the context, averaged over the windows."""
    model.eval()
    tot = torch.zeros(windows.shape[1] - 1)
    for i in range(0, len(windows), B):
        x = windows[i:i + B]
        logits = model(x[:, :-1])
        ce = F.cross_entropy(logits.flatten(0, 1).float(), x[:, 1:].flatten(), reduction="none").view(len(x), -1)
        tot += ce.sum(0)
    return (tot / len(windows)).numpy()


@torch.no_grad()
def masked_loss(model, windows: torch.Tensor, B: int = 16, seed: int = 12345) -> float:
    """BERT's held-out loss: cross-entropy on a fixed 15% of held-out positions, corrupted as in training."""
    model.eval()
    g = np.random.default_rng(seed)
    tot, n = 0.0, 0
    for i in range(0, len(windows), B):
        x = windows[i:i + B, :SEQ]
        inp, pick = corrupt(x, g)
        logits = model(inp)
        tot += float(F.cross_entropy(logits[pick].float(), x[pick], reduction="sum"))
        n += int(pick.sum())
    return tot / n


@torch.no_grad()
def repeat_test(model, rep: torch.Tensor) -> dict:
    """Accuracy and loss on the first and second copies of a random word list (an induction test)."""
    model.eval()
    L = (rep.shape[1] - 1) // 2
    logits = model(rep[:, :-1])
    y = rep[:, 1:]
    ok = (logits.argmax(-1) == y).float()
    ce = F.cross_entropy(logits.flatten(0, 1).float(), y.flatten(), reduction="none").view(y.shape)
    first, second = slice(0, L - 1), slice(L, 2 * L)  # predicting words 2..L of the first copy; all of the second
    return dict(acc1=float(ok[:, first].mean()), acc2=float(ok[:, second].mean()), loss1=float(ce[:, first].mean()),
                loss2=float(ce[:, second].mean()))


@torch.no_grad()
def sample(model, prompt: str, n: int = 24, temperature: float = 0.8, seed: int = 0) -> str:
    model.eval()
    g = torch.Generator().manual_seed(seed)
    ids = N.encode(prompt)
    start = len(ids)
    for _ in range(n):
        logits = model(torch.tensor([ids[-model.cfg.seq:]]))[0, -1].float() / temperature
        logits[:4] = -float("inf")  # no special tokens in a replay sample
        if logits.shape[0] > 4096:
            logits[4096:] = -float("inf")
        ids.append(int(torch.multinomial(logits.softmax(-1), 1, generator=g)))
    return N.decode(ids[start:])


def fill_ids(text: str = FILL) -> tuple[list[int], list[int]]:
    """The fill-in sentence as token ids, and the positions of its [MASK]s."""
    ids, where = [], []
    parts = text.split("[MASK]")
    for k, part in enumerate(parts):
        if part:
            ids += N.encode(part)
        if k < len(parts) - 1:
            where.append(len(ids))
            ids.append(MASK)
    return ids, where


@torch.no_grad()
def fill(model, text: str = FILL) -> list[str]:
    """BERT's best guess for each [MASK] (whole words only, so a guess reads as a word)."""
    model.eval()
    ids, where = fill_ids(text)
    logits = model(torch.tensor([ids]))[0].float()
    out = []
    for p in where:
        lp = logits[p, :4096].clone()
        lp[:4] = -float("inf")
        out.append(N.decode([int(lp.argmax())]).strip())
    return out


@torch.no_grad()
def bits_per_char(model, text: str, stride: int = 128) -> dict:
    """Bits per character of a text under a causal model.  Windows of the model's context slide by ``stride``; each
    token is scored once, and after the first window with at least (context - stride) tokens before it."""
    model.eval()
    ids = N.encode(text)
    T = model.cfg.seq
    nats, done, lo = 0.0, 0, 0  # tokens 1..done have been scored
    while done < len(ids) - 1:
        hi = min(len(ids), lo + T + 1)
        x = torch.tensor([ids[lo:hi]])
        ce = F.cross_entropy(model(x[:, :-1])[0].float(), x[0, 1:], reduction="none")  # ce[j]: token lo + j + 1
        nats += float(ce[done - lo:].sum())
        done = hi - 1
        lo += stride
    return dict(bits=nats / math.log(2) / len(text), tokens=len(ids), chars=len(text))


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
def snap_steps(steps: int) -> list[int]:
    s = sorted({0, steps} | {int(round(x)) for x in np.geomspace(10, steps, 13)})
    return [x for x in s if x <= steps]


def train(name: str, kind: str, shape: dict, tokens: int, cache_dir, lr: float = 3e-3, seed: int = 0,
          warmup: int = 100, threads: int = 2, log=print) -> dict:
    """Train one model (resumable); returns its curve and snapshots and saves its weights to <name>.pt."""
    torch.set_num_threads(threads)
    train_ids, valid_ids = N.token_arrays()
    model = build(shape, kind, seed)
    opts = pocket.make_optimizers(model, "adamw", lr, 0.1)
    steps = tokens // (BATCH * SEQ)
    snaps_at = set(snap_steps(steps))
    win = val_windows(valid_ids)
    words = word_tokens(train_ids)
    rep = repeat_batch(words)
    ck = cache_dir / f"{name}.ckpt.pt"
    state = dict(step=0, curve=[], snaps=[], seconds=0.0)
    if ck.exists():
        saved = torch.load(ck, weights_only=False)
        model.load_state_dict(saved["model"])
        for o, s in zip(opts, saved["opts"]):
            o.load_state_dict(s)
        state = saved["state"]
        log(f"{name}: resuming at step {state['step']}/{steps}")

    def snapshot(step):
        t = time.time()
        snap = dict(step=step, tokens=step * BATCH * SEQ)
        if kind == "gpt":
            pp = per_position(model, win)
            snap.update(val=float(pp.mean()), pos=pp.tolist(), sample=sample(model, PROMPT), **repeat_test(model, rep))
        else:
            snap.update(val=masked_loss(model, win), fill=fill(model))
        model.train()
        state["snaps"].append(snap)
        log(f"{name}: snapshot at {step}: val {snap['val']:.3f} ({time.time() - t:.0f}s)"
            + (f"  {snap['sample']!r}" if kind == "gpt" else f"  {snap['fill']}"))

    model.train()
    t0 = time.time()
    while state["step"] < steps:
        step = state["step"]
        if step in snaps_at and not any(s["step"] == step for s in state["snaps"]):
            snapshot(step)
        f = pocket.lr_factor(step, steps, "cosine", warmup, final=0.1)
        for o in opts:
            for gr in o.param_groups:
                gr["lr"] = lr * f
        x = batch(train_ids, seed, step)
        if kind == "gpt":
            logits = model(x[:, :-1])
            loss = F.cross_entropy(logits.flatten(0, 1), x[:, 1:].flatten())
        else:
            inp, pick = corrupt(x[:, :SEQ], np.random.default_rng([seed, step, 7]))
            logits = model(inp)
            loss = F.cross_entropy(logits[pick], x[:, :SEQ][pick])
        for o in opts:
            o.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        for o in opts:
            o.step()
        if step % 10 == 0:
            state["curve"].append([step, (step + 1) * BATCH * SEQ, float(loss)])
        state["step"] = step + 1
        if state["step"] % SAVE_EVERY == 0 or state["step"] == steps:
            state["seconds"] += time.time() - t0
            t0 = time.time()
            tmp = ck.with_suffix(".tmp")
            torch.save(dict(model=model.state_dict(), opts=[o.state_dict() for o in opts], state=state), tmp)
            tmp.replace(ck)
            log(f"{name}: step {state['step']}/{steps} loss {float(loss):.3f} "
                f"({state['seconds'] / state['step']:.2f}s/step)")
    if not any(s["step"] == steps for s in state["snaps"]):
        snapshot(steps)
        tmp = ck.with_suffix(".tmp")
        torch.save(dict(model=model.state_dict(), opts=[o.state_dict() for o in opts], state=state), tmp)
        tmp.replace(ck)
    torch.save(dict(shape=shape, kind=kind, model=model.state_dict()), cache_dir / f"{name}.pt")
    p = n_params(model)
    return dict(name=name, kind=kind, shape=shape, steps=steps, tokens=steps * BATCH * SEQ, lr=lr, seed=seed,
                params=p, flops=6.0 * p["compute"] * steps * BATCH * SEQ, seconds=state["seconds"],
                curve=np.array(state["curve"]), snaps=state["snaps"])


def load_trained(name: str, cache_dir):
    ck = torch.load(cache_dir / f"{name}.pt", weights_only=False)
    m = build(ck["shape"], ck["kind"])
    m.load_state_dict(ck["model"])
    return m.eval()
