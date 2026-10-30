"""Part 15's two language models on the series' thirty novels: a plain transformer and a gated-delta hybrid.

Both read the novels' byte-level BPE (4,096 tokens, ``explainer.ai.novels``), 256 tokens at a time, with the same width,
depth, MLPs, optimizer, batches and steps:

    transformer   four attention layers with rotary positions (as the series' other models)
    hybrid        three gated-delta layers, then one attention layer without positions (the layout of Qwen3-Next and
                  Kimi Linear, three linear layers to one attention layer; Kimi Linear's attention layers use no
                  positional encoding, NoPE, and leave order to the recurrent layers)
    gdn           four gated-delta layers, no attention at all

A run is seeded and resumable: the batch at step s depends only on (seed, s); the model and optimizer are saved every
``SAVE_EVERY`` steps.  At a few steps along the way the run records held-out loss and a sample (the training replay).
"""

from __future__ import annotations

import math
import time

import numpy as np
import torch
import torch.nn.functional as F

from explainer.ai import novels as N
from videos.ai.ai15.mixers import Net

SEQ, BATCH, D, LAYERS, HEADS = 256, 16, 64, 4, 2
SAVE_EVERY = 100
ARCHS = {"transformer": ["softmax"] * 4, "hybrid": ["gdn", "gdn", "gdn", "softmax"], "gdn": ["gdn"] * 4}
PROMPT = "The door opened, and"


def build(arch: str, seed: int) -> Net:
    torch.manual_seed(seed)
    layers = ARCHS[arch]
    rope = tuple(range(4)) if arch == "transformer" else ()
    m = Net(N.tokenizer().get_vocab_size(), D, layers, D // HEADS, heads=HEADS, mlp=int(round(8 * D / 3 / 16)) * 16,
            rope_layers=rope, chunk=SEQ, conv=4, attn_conv=0)  # one chunk per window in training
    for name, p in m.named_parameters():  # the series' initialization (explainer.lm.pocket)
        if p.dim() != 2:
            continue
        std = 0.02 if name.startswith(("emb", "head")) else 1 / math.sqrt(p.shape[1])
        if name.endswith((".o.weight", "down.weight")):
            std /= math.sqrt(2 * LAYERS)
        torch.nn.init.normal_(p, std=std)
    return m


def batch(train: np.ndarray, seed: int, step: int) -> torch.Tensor:
    g = np.random.default_rng([seed, step])
    ix = g.integers(0, len(train) - SEQ - 1, BATCH)
    return torch.from_numpy(np.stack([train[i:i + SEQ + 1] for i in ix]).astype(np.int64))


def val_windows(valid: np.ndarray, n: int = 48) -> torch.Tensor:
    starts = np.linspace(0, len(valid) - SEQ - 2, n).astype(int)
    return torch.from_numpy(np.stack([valid[s:s + SEQ + 1] for s in starts]).astype(np.int64))


@torch.no_grad()
def val_loss(m, win) -> float:
    m.eval()
    tot = 0.0
    for i in range(0, len(win), 16):
        x = win[i:i + 16]
        tot += float(F.cross_entropy(m(x[:, :-1]).flatten(0, 1), x[:, 1:].flatten())) * len(x)
    m.train()
    return tot / len(win)


@torch.no_grad()
def sample(m, prompt: str, n: int = 40, seed: int = 0, temperature: float = 0.8) -> str:
    m.eval()
    ids = N.encode(prompt)
    g = torch.Generator().manual_seed(seed)
    for _ in range(n):
        logits = m(torch.tensor([ids[-SEQ:]]))[0, -1] / temperature
        ids.append(int(torch.multinomial(logits.softmax(-1), 1, generator=g)))
    m.train()
    return N.decode(ids[len(N.encode(prompt)):])


def snap_steps(steps: int) -> list[int]:
    return sorted({0, steps} | {int(round(x)) for x in np.geomspace(20, steps, 9)})


def train(arch: str, seed: int, steps: int, ckpt_dir, lr: float = 3e-3, warmup: int = 40, threads: int = 1,
          log=print) -> dict:
    torch.set_num_threads(threads)
    tr, va = N.token_arrays()
    m = build(arch, seed)
    decay = [p for n, p in m.named_parameters() if p.dim() == 2]
    rest = [p for n, p in m.named_parameters() if p.dim() < 2]
    opt = torch.optim.AdamW([dict(params=decay, weight_decay=0.1), dict(params=rest, weight_decay=0.0)], lr=lr,
                            betas=(0.9, 0.95))
    win = val_windows(va)
    ck = ckpt_dir / f"lm_{arch}_{seed}.ckpt.pt"
    st = dict(step=0, curve=[], snaps=[], seconds=0.0)
    if ck.exists():
        saved = torch.load(ck, weights_only=False)
        m.load_state_dict(saved["model"])
        opt.load_state_dict(saved["opt"])
        st = saved["state"]
        log(f"    resuming {arch} seed {seed} at step {st['step']}")
    snaps = set(snap_steps(steps))
    t0 = time.time() - st["seconds"]
    for step in range(st["step"], steps + 1):
        if step % SAVE_EVERY == 0 and step > st["step"]:
            st.update(step=step, seconds=time.time() - t0)
            torch.save(dict(model=m.state_dict(), opt=opt.state_dict(), state=st), str(ck) + ".tmp")
            (ckpt_dir / (ck.name + ".tmp")).replace(ck)
        if step in snaps and not any(s_[0] == step for s_ in st["snaps"]):
            st["snaps"].append((step, val_loss(m, win), sample(m, PROMPT, 40, seed=1)))
            log(f"    {arch} seed {seed} step {step}: held-out {st['snaps'][-1][1]:.3f}")
        if step == steps:
            break
        f = (step + 1) / warmup if step < warmup else 0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * (step - warmup) / (steps - warmup)))
        for gr in opt.param_groups:
            gr["lr"] = lr * f
        x = batch(tr, seed, step)
        loss = F.cross_entropy(m(x[:, :-1]).flatten(0, 1), x[:, 1:].flatten())
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if step % 10 == 0:
            st["curve"].append((step, float(loss.detach())))
    st.update(step=steps, seconds=time.time() - t0)
    torch.save(dict(model=m.state_dict()), ckpt_dir / f"lm_{arch}_{seed}.pt")
    ck.unlink(missing_ok=True)
    return dict(arch=arch, seed=seed, steps=steps, tokens=steps * BATCH * SEQ, params=m.n_params(), curve=st["curve"],
                snaps=st["snaps"], seconds=st["seconds"], final_val=st["snaps"][-1][1])


def load_trained(arch: str, seed: int, ckpt_dir) -> Net:
    m = build(arch, seed)
    m.load_state_dict(torch.load(ckpt_dir / f"lm_{arch}_{seed}.pt")["model"])
    for mx in m.mix:  # longer texts at test time: chunks of 64, the state handed from chunk to chunk
        mx.chunk = 64
    return m.eval()


# ---------------------------------------------------------------------------
# Measurements
# ---------------------------------------------------------------------------
@torch.no_grad()
def bits_per_char(m, text: str, window: int = SEQ, stride: int = 128) -> float:
    """As Part 14's: windows of ``window`` tokens sliding by ``stride``; each token scored once, with at least
    window - stride tokens before it (after the first window)."""
    ids = N.encode(text)
    nats, done, lo = 0.0, 0, 0
    while done < len(ids) - 1:
        hi = min(len(ids), lo + window + 1)
        x = torch.tensor([ids[lo:hi]])
        ce = F.cross_entropy(m(x[:, :-1])[0], x[0, 1:], reduction="none")
        nats += float(ce[done - lo:].sum())
        done = hi - 1
        lo += stride
    return nats / math.log(2) / len(text)


@torch.no_grad()
def loss_by_position(m, valid: np.ndarray, L: int = 1024, n: int = 12) -> np.ndarray:
    """Mean loss at each position of windows of L tokens, read in one go (past the 256 it was trained on)."""
    starts = np.linspace(0, len(valid) - L - 2, n).astype(int)
    tot = np.zeros(L)
    for s in starts:
        x = torch.from_numpy(valid[s:s + L + 1].astype(np.int64))[None]
        tot += F.cross_entropy(m(x[:, :-1])[0], x[0, 1:], reduction="none").numpy()
    return tot / n


@torch.no_grad()
def copy_test(m, valid: np.ndarray, gaps, n: int = 24, span: int = 24, seed: int = 0) -> dict:
    """A needle the model can only get by remembering: a run of ``span`` random tokens, then ``gap`` tokens of a
    novel, then the same run again; accuracy of the next-token guesses inside the second copy (after its first
    token), read in one go."""
    g = np.random.default_rng(seed)
    out = {}
    vocab = N.tokenizer().get_vocab_size()
    for gap in gaps:
        hits = tot = 0
        for _ in range(n):
            run = g.integers(300, vocab - 8, span)
            s = int(g.integers(0, len(valid) - gap - 70))
            pre = valid[s:s + 32].astype(np.int64)
            mid = valid[s + 32:s + 32 + gap].astype(np.int64)
            seq = np.concatenate([pre, run, mid, run])
            x = torch.from_numpy(seq)[None]
            p = m(x[:, :-1])[0].argmax(-1).numpy()
            a = len(pre) + span + gap  # where the second copy starts
            hits += int((p[a:a + span - 1] == seq[a + 1:a + span]).sum())
            tot += span - 1
        out[str(gap)] = hits / tot
    return out


def run_and_measure(arch: str, seed: int, steps: int, ckpt_dir: str, gaps) -> dict:
    """One run, trained (resuming) and measured: what compute.py's ``lm`` item keeps.  A top-level function, so a
    pool of spawned processes can run it."""
    from pathlib import Path

    from videos.ai.ai1 import compute as c1

    torch.set_num_threads(1)
    ckpt_dir = Path(ckpt_dir)
    r = train(arch, seed, steps, ckpt_dir)
    m = load_trained(arch, seed, ckpt_dir)
    _, va = N.token_arrays()
    r["bits"] = bits_per_char(m, c1.text("passage"))
    r["by_pos"] = loss_by_position(m, va).tolist()
    r["copy"] = copy_test(m, va, gaps)
    print(f"    {arch} seed {seed}: held-out {r['final_val']:.3f}, passage {r['bits']:.3f} bits/char, copy {r['copy']}",
          flush=True)
    return r
