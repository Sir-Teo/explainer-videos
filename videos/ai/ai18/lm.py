"""Part 18's training runs on the thirty novels: ``explainer.lm.pocket``'s PocketGPT with the pieces of a frontier
recipe switchable one at a time.

    spec = Spec(d=64, layers=2, steps=300, precision="fp16")       # every field is plain data (cached with the result)
    out = train(spec, ckpt=path)                                    # resumes from path if it exists

What can be switched (``Spec``):

* the optimizer (AdamW, or Muon for the hidden matrices) and the schedule (cosine, warmup-stable-decay);
* QK-norm and the z-loss (stability);
* a depth-1 multi-token-prediction module, DeepSeek-V3's design (the main model's last hidden state and the next
  token's embedding, joined and passed through one more block, predict the token after next with the shared head);
* the number formats of every matrix product inside the blocks (``precision``), emulated exactly: the inputs of each
  product (activations and weights going forward, the output gradient going backward) are rounded to the format
  and the product is accumulated in FP32, as tensor cores do.  ``fp16`` rounds the gradients with no loss scaling,
  ``fp16_scaled`` adds dynamic loss scaling, ``fp8_tensor`` is the 2022 recipe (E4M3 forward, E5M2 gradients, one
  scale per tensor) and ``fp8_tile`` DeepSeek-V3's (E4M3 everywhere, one scale per 1 x tile of an activation or
  gradient and per tile x tile block of a weight); the embedding, the output head and attention's own products stay
  in FP32, as in DeepSeek-V3;
* the data: the natural text, or a mixture of groups of books with given weights.

Every run is seeded, and the batch at step s depends only on (seed, s), so a run killed and resumed from its
checkpoint is the same run.
"""

from __future__ import annotations

import math
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from explainer.ai import novels as N
from explainer.lm import pocket

PROMPT = "The door opened, and"  # the replay's prompt (Part 14's)
VOCAB = 4096


@dataclass
class Spec:
    d: int = 64
    layers: int = 2
    heads: int = 2
    seq: int = 128
    batch: int = 16
    steps: int = 200
    lr: float = 3e-3
    warmup: int = 20
    schedule: str = "cosine"  # cosine | wsd | constant
    decay_frac: float = 0.2
    final: float = 0.1
    decay_start: int | None = None
    optimizer: str = "adamw"  # adamw | muon
    wd: float = 0.1
    clip: float = 1.0
    qk_norm: bool = False
    z_loss: float = 0.0
    mtp: float = 0.0  # weight of the depth-1 MTP loss; 0: no MTP module
    mtp_late: float | None = None  # its weight over the last decay_frac of the run (DeepSeek-V3: 0.3, then 0.1)
    precision: str = "fp32"  # fp32 | bf16 | fp16 | fp16_scaled | fp8_tensor | fp8_tile
    tile: int = 32
    grad_div: float = 1.0  # the loss is divided by this before the backward pass and the gradients multiplied back
    # after it: what accumulating a step's gradient over grad_div micro-batches does to the gradients' size
    seed: int = 0
    mix: list | None = None  # weights over the groups of books (None: the natural text)
    probe_every: int = 0
    eval_every: int = 0  # 0: about 30 evaluations
    eval_windows: int = 32
    snaps: list = field(default_factory=list)  # steps at which to record a sample (training replays)
    keep: list = field(default_factory=list)  # steps whose full state is kept (for cooldown branches)


# ---------------------------------------------------------------------------
# Number formats: rounding a tensor, with one scale per tensor, per tile or per block
# ---------------------------------------------------------------------------
STATS = {"n": 0, "zero": 0, "sub": 0}  # gradient elements rounded, flushed to zero, landed in the subnormals


def _r16(t):
    return t.half().float()


def _rb16(t):
    return t.bfloat16().float()


def _f8(t, dtype, vmax):
    amax = t.abs().amax()
    if not torch.isfinite(amax) or amax == 0:
        return t
    s = amax / vmax
    return (t / s).to(dtype).float() * s


def _f8_rows(t, dtype, vmax, tile):
    """One scale per 1 x tile slice along the last dimension."""
    n = t.shape[-1]
    k = tile if n % tile == 0 else n
    v = t.reshape(-1, n // k, k)
    amax = v.abs().amax(-1, keepdim=True)
    s = torch.where(amax > 0, amax / vmax, torch.ones_like(amax))
    return ((v / s).to(dtype).float() * s).reshape(t.shape)


def _f8_blocks(w, dtype, vmax, tile):
    """One scale per tile x tile block of a weight matrix."""
    o, i = w.shape
    if o % tile or i % tile:
        return _f8(w, dtype, vmax)
    v = w.reshape(o // tile, tile, i // tile, tile)
    amax = v.abs().amax(dim=(1, 3), keepdim=True)
    s = torch.where(amax > 0, amax / vmax, torch.ones_like(amax))
    return ((v / s).to(dtype).float() * s).reshape(o, i)


def _counting(fn):
    """Wrap a gradient rounder: count the elements it flushes to zero or leaves subnormal (in FP16)."""
    def g(t):
        q = fn(t)
        STATS["n"] += t.numel()
        STATS["zero"] += int(((t != 0) & (q == 0)).sum())
        STATS["sub"] += int(((q != 0) & (q.abs() < 2.0 ** -14)).sum())
        return q
    return g


E4M3, E5M2 = torch.float8_e4m3fn, torch.float8_e5m2


def quantizers(kind: str, tile: int):
    """(activations, weights, output gradients) rounders for a precision recipe."""
    if kind == "bf16":
        return _rb16, _rb16, _rb16
    if kind in ("fp16", "fp16_scaled"):
        return _r16, _r16, _counting(_r16)
    if kind == "fp8_tensor":
        return (lambda t: _f8(t, E4M3, 448.0)), (lambda t: _f8(t, E4M3, 448.0)), (lambda t: _f8(t, E5M2, 57344.0))
    if kind == "fp8_tile":
        return ((lambda t: _f8_rows(t, E4M3, 448.0, tile)), (lambda w: _f8_blocks(w, E4M3, 448.0, tile)),
                (lambda t: _f8_rows(t, E4M3, 448.0, tile)))
    raise ValueError(kind)


class QLinear(torch.autograd.Function):
    """y = x W^T with x and W rounded going forward and dy rounded going back; products accumulate in FP32."""

    @staticmethod
    def forward(ctx, x, w, fa, fw, fg):
        shp = x.shape
        xq, wq = fa(x.reshape(-1, shp[-1])), fw(w)
        ctx.save_for_backward(xq, wq)
        ctx.fg, ctx.shp = fg, shp
        return (xq @ wq.t()).reshape(*shp[:-1], w.shape[0])

    @staticmethod
    def backward(ctx, gy):
        xq, wq = ctx.saved_tensors
        g = ctx.fg(gy.reshape(-1, gy.shape[-1]))
        return (g @ wq).reshape(ctx.shp), g.t() @ xq, None, None, None


def install_precision(model: nn.Module, kind: str, tile: int) -> None:
    if kind == "fp32":
        return
    fa, fw, fg = quantizers(kind, tile)
    for name, mod in model.named_modules():
        if isinstance(mod, nn.Linear) and (name.startswith("blocks") or name.startswith("mtp.block")):
            mod.forward = (lambda m: (lambda x: QLinear.apply(x, m.weight, fa, fw, fg)))(mod)


# ---------------------------------------------------------------------------
# The model, with an optional multi-token-prediction module
# ---------------------------------------------------------------------------
class MTPModule(nn.Module):
    """DeepSeek-V3's depth-1 MTP module: [RMSNorm(h_i); RMSNorm(Emb(t_{i+1}))] -> linear 2d -> d -> one block;
    the shared output head then predicts t_{i+2}."""

    def __init__(self, cfg: pocket.Config):
        super().__init__()
        self.nh, self.ne = nn.RMSNorm(cfg.d), nn.RMSNorm(cfg.d)
        self.proj = nn.Linear(2 * cfg.d, cfg.d, bias=False)
        self.block = pocket.Block(cfg)
        for name, p in self.named_parameters():
            if p.dim() == 2:
                std = 1 / math.sqrt(p.shape[1])
                if name.endswith(("out.weight", "down.weight")):
                    std /= math.sqrt(2 * (cfg.layers + 1))
                nn.init.normal_(p, std=std)

    def forward(self, h, e):
        return self.block(self.proj(torch.cat([self.nh(h), self.ne(e)], -1)))


def build(spec: Spec) -> pocket.PocketGPT:
    torch.manual_seed(spec.seed)
    cfg = pocket.Config(vocab=VOCAB, d=spec.d, layers=spec.layers, heads=spec.heads, seq=spec.seq,
                        qk_norm=spec.qk_norm)
    m = pocket.PocketGPT(cfg)
    if spec.mtp:
        m.mtp = MTPModule(cfg)  # built after the trunk, so the trunk starts from the same weights either way
    install_precision(m, spec.precision, spec.tile)
    return m


def hidden(model, idx, probe=False):
    x = model.emb(idx)
    for b in model.blocks:
        x = b(x, probe)
    return x


def logits_of(model, h):
    return model.head(model.norm(h))


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def batch_at(arrays: list, weights, seed: int, step: int, B: int, T: int) -> torch.Tensor:
    """The batch of step ``step``: B windows of T + 1 tokens, from one array or from a mixture of arrays."""
    g = np.random.default_rng([seed, step, 18])
    if weights is None:
        a = arrays[0]
        ix = g.integers(0, len(a) - T - 1, B)
        rows = [a[i:i + T + 1] for i in ix]
    else:
        dom = g.choice(len(arrays), B, p=np.asarray(weights) / np.sum(weights))
        rows = [arrays[k][j:j + T + 1] for k in dom for j in [int(g.integers(0, len(arrays[k]) - T - 1))]]
    return torch.from_numpy(np.stack(rows).astype(np.int64))


def windows(ids: np.ndarray, n: int, T: int) -> torch.Tensor:
    starts = np.linspace(0, len(ids) - T - 2, n).astype(int)
    return torch.from_numpy(np.stack([ids[s:s + T + 1] for s in starts]).astype(np.int64))


@torch.no_grad()
def eval_loss(model, win: torch.Tensor, B: int = 16) -> float:
    tot, n = 0.0, 0
    for i in range(0, len(win), B):
        x = win[i:i + B]
        lg = logits_of(model, hidden(model, x[:, :-1]))
        tot += float(F.cross_entropy(lg.flatten(0, 1), x[:, 1:].flatten(), reduction="sum"))
        n += x[:, 1:].numel()
    return tot / n


@torch.no_grad()
def text_nats(model, ids, stride: int | None = None) -> float:
    """Mean next-token loss (nats) over a token sequence, sliding windows of the model's context; each token is
    scored once."""
    T = model.cfg.seq
    stride = stride or T // 2
    nats, done, lo = 0.0, 0, 0
    while done < len(ids) - 1:
        hi = min(len(ids), lo + T + 1)
        x = torch.tensor([list(ids[lo:hi])])
        ce = F.cross_entropy(logits_of(model, hidden(model, x[:, :-1]))[0], x[0, 1:], reduction="none")
        nats += float(ce[done - lo:].sum())
        done = hi - 1
        lo += stride
    return nats / (len(ids) - 1)


@torch.no_grad()
def sample(model, prompt: str, n: int = 24, temperature: float = 0.8, seed: int = 1) -> str:
    g = torch.Generator().manual_seed(seed)
    ids = N.encode(prompt)
    start = len(ids)
    for _ in range(n):
        lg = logits_of(model, hidden(model, torch.tensor([ids[-model.cfg.seq:]])))[0, -1] / temperature
        ids.append(int(torch.multinomial(lg.softmax(-1), 1, generator=g)))
    return N.decode(ids[start:])


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
def _mtp_weight(spec: Spec, step: int) -> float:
    if not spec.mtp:
        return 0.0
    if spec.mtp_late is not None and step >= int(spec.steps * (1 - spec.decay_frac)):
        return spec.mtp_late
    return spec.mtp


def _save(path: Path, obj) -> None:
    tmp = Path(str(path) + ".tmp")
    torch.save(obj, tmp)
    tmp.replace(path)


def train(spec: Spec, *, arrays: list | None = None, valid: np.ndarray | None = None, ckpt=None, ckpt_every=100,
          threads: int = 1, log=None, init_state: dict | None = None) -> dict:
    """Train one run (resuming from ``ckpt`` if it exists, or continuing from ``init_state``, a kept state of
    another run); return its curves and diagnostics, with the model under ``_model``."""
    torch.set_num_threads(threads)
    if arrays is None or valid is None:
        tr, va = N.token_arrays()
        arrays = arrays or [tr]
        valid = va if valid is None else valid
    model = build(spec)
    opts = pocket.make_optimizers(model, spec.optimizer, spec.lr, spec.wd)
    win = windows(valid, spec.eval_windows, spec.seq)
    eval_every = spec.eval_every or max(1, spec.steps // 30)
    st = dict(step=0, curve=[], evals=[], probes=[], snaps=[], scale=2.0 ** 16, good=0, skipped=[], seconds=0.0,
              underflow=[])
    src = None
    if ckpt is not None and Path(ckpt).exists():
        src = torch.load(ckpt, weights_only=False)
    elif init_state is not None:
        src = init_state
    if src is not None:
        model.load_state_dict(src["model"])
        for o, s in zip(opts, src["opts"]):
            o.load_state_dict(s)
        st.update({k: v for k, v in src.items() if k not in ("model", "opts")})
        if log:
            log(f"    resuming at step {st['step']}/{spec.steps}")
    t0 = time.time() - st["seconds"]
    T = spec.seq
    scaled = spec.precision == "fp16_scaled"

    def snapshot(step):
        model.eval()
        st["snaps"].append(dict(step=step, tokens=step * spec.batch * T, val=eval_loss(model, win),
                                sample=sample(model, PROMPT)))
        model.train()

    for step in range(st["step"], spec.steps):
        if ckpt is not None and step > 0 and step % ckpt_every == 0 and step != st.get("_saved"):
            st["step"], st["seconds"], st["_saved"] = step, time.time() - t0, step
            _save(Path(ckpt), {"model": model.state_dict(), "opts": [o.state_dict() for o in opts], **st})
        if step in spec.keep and ckpt is not None:
            st["step"], st["seconds"] = step, time.time() - t0
            _save(Path(str(ckpt).replace(".ckpt.pt", f".step{step}.pt")),
                  {"model": model.state_dict(), "opts": [o.state_dict() for o in opts], **st})
        if step in spec.snaps and not any(s["step"] == step for s in st["snaps"]):
            snapshot(step)
        f = pocket.lr_factor(step, spec.steps, spec.schedule, spec.warmup, spec.decay_frac, spec.final,
                             spec.decay_start)
        for o in opts:
            for g in o.param_groups:
                g["lr"] = spec.lr * f
        x = batch_at(arrays, spec.mix, spec.seed, step, spec.batch, T)
        inp, tgt = x[:, :-1], x[:, 1:]
        probe = bool(spec.probe_every) and step % spec.probe_every == 0
        STATS.update(n=0, zero=0, sub=0)
        h = hidden(model, inp, probe)
        lg = logits_of(model, h)
        ce = F.cross_entropy(lg.flatten(0, 1), tgt.flatten())
        lz = torch.logsumexp(lg.float(), -1)
        total = ce
        if spec.z_loss:
            total = total + spec.z_loss * lz.pow(2).mean()
        lam = _mtp_weight(spec, step)
        mtp_ce = None
        if spec.mtp:
            h2 = model.mtp(h[:, :-1], model.emb(tgt[:, :-1]))
            mtp_ce = F.cross_entropy(logits_of(model, h2).flatten(0, 1), tgt[:, 1:].flatten())
            total = total + lam * mtp_ce
        for o in opts:
            o.zero_grad(set_to_none=True)
        (total * (st["scale"] if scaled else 1.0) / spec.grad_div).backward()
        skip = False
        if scaled:
            inv = 1.0 / st["scale"]
            finite = True
            for p in model.parameters():
                if p.grad is not None:
                    p.grad.mul_(inv)
                    finite &= bool(torch.isfinite(p.grad).all())
            if not finite:  # overflow: skip the update, halve the scale
                st["scale"] /= 2
                st["good"] = 0
                st["skipped"].append(step)
                skip = True
            else:
                st["good"] += 1
                if st["good"] % 50 == 0:  # (PyTorch's GradScaler waits 2,000 steps; our runs are short)
                    st["scale"] *= 2
        if spec.grad_div != 1.0 and not skip:
            for p in model.parameters():
                if p.grad is not None:
                    p.grad.mul_(spec.grad_div)
        gn = float("nan")
        if not skip:
            gn = float(torch.nn.utils.clip_grad_norm_(model.parameters(), spec.clip if spec.clip else 1e9))
            for o in opts:
                o.step()
        if STATS["n"]:
            st["underflow"].append([step, STATS["zero"] / STATS["n"], STATS["sub"] / STATS["n"]])
        lv = float(ce)
        st["curve"].append([step, lv, gn, f, float(lz.mean()), float(mtp_ce) if mtp_ce is not None else 0.0,
                            st["scale"] if scaled else 1.0])
        if probe:
            st["probes"].append([step, max(b.attn.max_logit for b in model.blocks), float(lg.detach().abs().amax()),
                                 float(lz.mean())])
        if (step + 1) % eval_every == 0 or step == spec.steps - 1:
            model.eval()
            st["evals"].append([step + 1, (step + 1) * spec.batch * T, eval_loss(model, win)])
            model.train()
            if log:
                log(f"    step {step + 1}/{spec.steps} loss {lv:.3f} val {st['evals'][-1][2]:.3f} "
                    f"{(time.time() - t0) / (step + 1 - (src or {}).get('step', 0) + 1e-9):.2f}s/step")
        if not math.isfinite(lv):
            break
    st["step"] = spec.steps
    if spec.steps in spec.snaps and not any(s["step"] == spec.steps for s in st["snaps"]):
        snapshot(spec.steps)
    st["seconds"] = time.time() - t0
    out = dict(spec=asdict(spec), counts={k: int(v) for k, v in model.count().items()},
               tokens=spec.steps * spec.batch * T, **{k: v for k, v in st.items() if not k.startswith("_")})
    out["final_val"] = out["evals"][-1][2] if out["evals"] else float("nan")
    out["_model"] = model
    out["_opts"] = opts
    return out


@torch.no_grad()
def mtp_acceptance(model, prompts: list, n: int = 48) -> dict:
    """Self-speculative decoding with the MTP module: generate greedily with the main model; at each position the
    MTP module drafts the token after next from the hidden state and the token just chosen; the draft is accepted
    if the main model then chooses the same token."""
    model.eval()
    acc = tot = 0
    for p in prompts:
        ids = list(p)
        for _ in range(n):
            lg = logits_of(model, hidden(model, torch.tensor([ids[-model.cfg.seq:]])))[0, -1]
            ids.append(int(lg.argmax()))
        x = torch.tensor([ids[-model.cfg.seq:]])
        L = len(p) - max(0, len(ids) - model.cfg.seq)  # where the generated part starts within x
        h = hidden(model, x)
        h2 = model.mtp(h[:, :-1], model.emb(x[:, 1:]))  # position i: h_i and token i+1 -> token i+2
        draft = logits_of(model, h2)[0].argmax(-1)  # draft[i] predicts x[i + 2]
        for i in range(L - 1, x.shape[1] - 2):
            acc += int(draft[i] == x[0, i + 2])
            tot += 1
    return dict(accepted=acc, drafted=tot, rate=acc / max(tot, 1))
