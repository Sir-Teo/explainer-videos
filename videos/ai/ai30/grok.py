"""Grokking on (a + b) mod p with an adapted local recipe inspired by Nanda et al. (2023).

    the model    tokens a, b, "=" (vocabulary p + 1); learned positions; one attention layer (4 heads of 32), a ReLU MLP of
                 512 units, no layer norm; the logits over the p answers read at "="
    training     full batch on 30% of the p^2 pairs, AdamW (lr 1e-3, weight decay 1, betas 0.9 / 0.98).
                 Initialization, split RNG, output vocabulary and budget are local adaptations, not an exact replication.
    the size     p = 59 (Nanda et al. used 113)
    measured     every ``SNAP`` steps: train and test loss and accuracy; the embedding's Fourier spectrum (how much of
                 W_E lies along cos(wk a) and sin(wk a) for each frequency k); legacy adaptive embedding-key metrics;
                 and raw logits for retrospective fixed-final-output-key restricted and excluded losses.

Atomic, pinned checkpoints every ``CKPT`` steps and at the endpoint retain raw logits (~119 MiB at default settings).
Restricted logits keep the sum waves AND each answer's input mean; excluded logits remove only the sum waves.
The final constrained cosine fit is a separate diagnostic from the sum-wave projection.
"""

from __future__ import annotations

import math
import os
import hashlib
from pathlib import Path
import tempfile

import numpy as np

P, D, H, DMLP = 59, 128, 4, 512
FRAC, LR, WD = 0.3, 1e-3, 1.0
STEPS, SNAP, CKPT = 15000, 100, 1000
SEED = 2023  # fixed seed of this local adaptation
METRIC_SCHEMA = "ai30-grok-fixed-output-keys-v1"
N_KEY = 5
KEY_RULE = "top5_non_dc_final_WL_output_fourier_energy; WL=W2@WU; ties=lower_frequency"


def build():
    import torch
    import torch.nn as nn

    class Grok(nn.Module):
        def __init__(self):
            super().__init__()
            self.WE = nn.Parameter(torch.randn(P + 1, D) / math.sqrt(D))
            self.pos = nn.Parameter(torch.randn(3, D) / math.sqrt(D))
            self.Wq, self.Wk, self.Wv = (nn.Parameter(torch.randn(H, D, D // H) / math.sqrt(D)) for _ in range(3))
            self.Wo = nn.Parameter(torch.randn(H, D // H, D) / math.sqrt(D))
            self.W1 = nn.Parameter(torch.randn(D, DMLP) / math.sqrt(D))
            self.b1 = nn.Parameter(torch.zeros(DMLP))
            self.W2 = nn.Parameter(torch.randn(DMLP, D) / math.sqrt(DMLP))
            self.b2 = nn.Parameter(torch.zeros(D))
            self.WU = nn.Parameter(torch.randn(D, P) / math.sqrt(D))

        def forward(self, x, keep=False):
            """x: (B, 3) ids; only the last position ("=") is read, so only its query is computed."""
            h = self.WE[x] + self.pos[None]  # (B, 3, D)
            q = torch.einsum("bd,hde->bhe", h[:, -1], self.Wq)
            k = torch.einsum("btd,hde->bhte", h, self.Wk)
            v = torch.einsum("btd,hde->bhte", h, self.Wv)
            att = torch.softmax(torch.einsum("bhe,bhte->bht", q, k) / math.sqrt(D // H), -1)
            z = torch.einsum("bht,bhte->bhe", att, v)
            r = h[:, -1] + torch.einsum("bhe,hed->bd", z, self.Wo)
            pre = r @ self.W1 + self.b1
            act = torch.relu(pre)
            r2 = r + act @ self.W2 + self.b2
            logits = r2 @ self.WU
            return (logits, dict(att=att, act=act, resid=r)) if keep else logits

    return Grok()


def dataset(seed=SEED):
    import torch

    a, b = np.meshgrid(np.arange(P), np.arange(P), indexing="ij")
    a, b = a.ravel(), b.ravel()
    x = np.stack([a, b, np.full_like(a, P)], 1)
    y = (a + b) % P
    perm = np.random.Generator(np.random.PCG64(seed)).permutation(len(a))
    n_tr = int(FRAC * len(a))
    tr, te = perm[:n_tr], perm[n_tr:]
    return torch.tensor(x), torch.tensor(y), torch.tensor(tr), torch.tensor(te)


def fourier_basis():
    """Orthonormal Fourier basis on Z_p: the constant, then cos and sin of each frequency k = 1 ... (p - 1) / 2."""
    t = np.arange(P)
    rows, names = [np.ones(P) / math.sqrt(P)], ["const"]
    for k in range(1, (P - 1) // 2 + 1):
        for f, nm in ((np.cos, "cos"), (np.sin, "sin")):
            v = f(2 * np.pi * k * t / P)
            rows.append(v / np.linalg.norm(v))
            names.append(f"{nm}{k}")
    return np.array(rows), names


def restricted(L, key):
    """The part of a logit table L (a, b, c) along cos and sin of w_k (a + b), for each c and each key frequency k."""
    a = np.arange(P)
    sab = (a[:, None] + a[None, :]) % P
    keep = np.zeros_like(L, dtype=np.float64)
    for k in key:
        for f in (np.cos, np.sin):
            w = f(2 * np.pi * k * sab / P)
            coef = np.einsum("ab,abc->c", w, L) / (w ** 2).sum()
            keep += w[:, :, None] * coef[None, None, :]
    return keep


def _array(value):
    """Convert CPU tensors or arrays without importing Torch in analytic helpers."""
    return value.detach().cpu().numpy() if hasattr(value, "detach") else np.asarray(value)


def _r2(L, fit):
    total = float(np.square(L).sum())
    return float(1 - np.square(L - fit).sum() / total) if total else float("nan")


def _ce(L, y, idx):
    idx = np.asarray(idx, dtype=int)
    z = np.asarray(L, dtype=np.float64).reshape(P * P, P)[idx]
    z = z - z.max(-1, keepdims=True)
    return float((np.log(np.exp(z).sum(-1)) - z[np.arange(len(z)), np.asarray(y)[idx]]).mean())


def output_key_frequencies(WL, n_key=N_KEY):
    """Own selection rule: top non-DC energies across neurons of final WL's output Fourier modes.

    WL has shape (neurons, answers). The cardinality is imposed, not a discovered count of important frequencies.
    """
    WL = np.asarray(WL, dtype=np.float64)
    if WL.ndim != 2 or WL.shape[1] != P or not np.isfinite(WL).all():
        raise ValueError("WL must be a finite (neurons, P) answer map")
    if not isinstance(n_key, int) or not 1 <= n_key <= (P - 1) // 2:
        raise ValueError("invalid key-frequency cardinality")
    B, _ = fourier_basis()
    coeff = WL @ B.T
    energy = np.square(coeff[:, 1:]).reshape(len(WL), (P - 1) // 2, 2).sum((0, 2))
    key = (np.argsort(-energy, kind="stable")[:n_key] + 1).tolist()
    spectrum = energy / energy.sum() if energy.sum() else np.zeros_like(energy)
    return key, spectrum


def progress_metrics(L, key, y, tr, te):
    """Fixed-key held-out restricted and training excluded CE; keep answer bias only in restricted.

    This sum-wave subspace permits arbitrary answer coefficients and is not the stricter cosine circuit fit.
    """
    L = np.asarray(L, dtype=np.float64)
    L = L - L.mean(-1, keepdims=True)  # harmless per-input softmax gauge
    waves = restricted(L, key)
    bias = L.mean((0, 1), keepdims=True)
    return dict(restricted_loss=_ce(waves + bias, y, te), excluded_loss=_ce(L - waves, y, tr))


def circuit_diagnostics(L, key):
    """Separate unconstrained sum-wave R² from sum alpha_k cos(w_k(a+b-c)) fit and accuracy.

    Coefficients are least-squares amplitudes, unconstrained in sign. Accuracy scores the fitted cosine logits
    against modular addition on ALL pairs; it is not the model's held-out accuracy. R² is undefined for zero logits.
    """
    L = np.asarray(L, dtype=np.float64)
    L = L - L.mean(-1, keepdims=True)
    a = np.arange(P)
    s = (a[:, None, None] + a[None, :, None] - a[None, None, :]) % P
    fit = np.zeros_like(L)
    coefficients = []
    for k in key:
        wave = np.cos(2 * np.pi * k * s / P)
        amplitude = float((L * wave).sum() / np.square(wave).sum())
        coefficients.append(amplitude)
        fit += amplitude * wave
    target = (a[:, None] + a[None, :]) % P
    return dict(sum_wave_r2=_r2(L, restricted(L, key)), strict_cos_r2=_r2(L, fit),
                strict_cos_coefficients=np.array(coefficients),
                strict_cos_accuracy=float((fit.argmax(-1) == target).mean()), strict_cos_key=list(key),
                strict_cos_accuracy_scope="fitted_logits_on_all_modular_addition_pairs",
                fit_reference="logits_centered_over_answers_per_input;no_answer_bias_in_fit")


def finalize_history(hist, key, output_spectrum, y, tr, te):
    """Reproject retained logits at every step onto the SAME final output keys, preserving legacy metrics."""
    for row in hist:
        row.update(progress_metrics(row["_logits"], key, y, tr, te))
        row.update(key=list(key), key_rule=KEY_RULE, key_selection="retrospective_final_output_map",
                   metric_schema=METRIC_SCHEMA, restricted_scope="held_out_pairs;sum_waves_plus_answer_input_mean",
                   excluded_scope="training_pairs;subtract_sum_waves_only")
    hist[-1]["output_spectrum"] = np.asarray(output_spectrum)
    hist[-1].update(circuit_diagnostics(hist[-1]["_logits"], key))
    return hist


def measure(model, x, y, tr, te, n_key=5):
    """Observe one model state and retain raw logits plus historical adaptive, zero-DC metrics.

    Fixed-final-output-key metrics are populated by finalize_history after the final model is available.
    """
    import torch

    with torch.no_grad():
        z = model(x)
        lp = torch.log_softmax(z.double(), -1)
        nll = -lp[torch.arange(len(y)), y]
        acc = (z.argmax(-1) == y).float()
        out = dict(train_loss=float(nll[tr].mean()), test_loss=float(nll[te].mean()),
                   train_acc=float(acc[tr].mean()), test_acc=float(acc[te].mean()))
        B, _ = fourier_basis()
        WE = model.WE[:P].double().numpy()
        coef = B @ WE  # (p, D): the embedding along each basis vector
        nk = (P - 1) // 2
        spec = np.array([np.sum(coef[2 * k - 1] ** 2 + coef[2 * k] ** 2) for k in range(1, nk + 1)])
        out["spectrum"] = spec / spec.sum()
        key = np.argsort(-spec)[:n_key] + 1  # the key frequencies (1-based)
        out["legacy_key"] = [int(k) for k in key]
        # Retain the actual float32 model outputs, not reconstructed or half-precision logits.
        out["_logits"] = z.detach().cpu().numpy().reshape(P, P, P).copy()
        L = z.double().numpy().reshape(P, P, P)
        L = L - L.mean(-1, keepdims=True)
        keep = restricted(L, key)
        y_np, tr_np, te_np = (_array(a) for a in (y, tr, te))
        out["legacy_restricted_loss"] = _ce(keep, y_np, te_np)
        out["legacy_excluded_loss"] = _ce(L - keep, y_np, tr_np)
        out["legacy_sum_wave_r2"] = _r2(L, keep)
        out["weight_norm"] = float(sum((p_.double() ** 2).sum() for p_ in model.parameters()) ** 0.5)
    return out


def checkpoint_pins(x, y, tr, te, steps=STEPS, runtime_versions=None):
    """Bind resume to this source, unchanged adapted recipe, actual split arrays and intended budget."""
    dataset_hash = hashlib.sha256()
    for value in (x, y, tr, te):
        a = np.ascontiguousarray(_array(value))
        dataset_hash.update(str((a.dtype.str, a.shape)).encode("ascii"))
        dataset_hash.update(a.tobytes())
    return dict(metric_schema=METRIC_SCHEMA, source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dataset_sha256=dataset_hash.hexdigest(), runtime_versions=runtime_versions or {},
                recipe=dict(P=P, D=D, H=H, DMLP=DMLP, frac=FRAC, lr=LR, weight_decay=WD, seed=SEED,
                            betas=[0.9, 0.98], warmup_steps=10, requested_steps=steps, snap=SNAP, ckpt=CKPT,
                            n_key=N_KEY, key_rule=KEY_RULE, split="numpy.PCG64(seed).permutation",
                            initialization="local WE,pos,Q,K,V,O,W1,WU:1/sqrt(D);W2:1/sqrt(DMLP);zero_MLP_biases",
                            objective="full_batch_cross_entropy;P_answer_classes;no_layernorm"))


def validate_checkpoint(ck, expected_pins, steps):
    """Validate metadata and retained measurements before loading any model/optimizer state.

    Legacy checkpoints cannot recover fixed-key history: reject them rather than mixing metric definitions.
    Checkpoint deserialization is only for locally owned trusted artifacts, as with the original trainer.
    """
    required = {"metric_schema", "pins", "model", "opt", "sched", "hist", "step", "rng"}
    if not isinstance(ck, dict) or required - ck.keys() or ck.get("metric_schema") != METRIC_SCHEMA:
        raise ValueError("legacy or incomplete grok checkpoint; preserve it and use a separate candidate path")
    saved = ck["step"]
    if not isinstance(saved, int) or isinstance(saved, bool) or saved < 0:
        raise ValueError("invalid grok checkpoint step")
    if saved > steps:
        raise ValueError(f"requested steps {steps} precede checkpoint step {saved}")
    if ck["pins"] != expected_pins:
        raise ValueError("grok checkpoint recipe/source/dataset/runtime pins mismatch")
    hist = ck["hist"]
    if not isinstance(hist, list) or not hist:
        raise ValueError("grok checkpoint has no retained measurement history")
    required_row = {"step", "_logits", "spectrum", "weight_norm", "train_loss", "test_loss", "train_acc", "test_acc",
                    "legacy_key", "legacy_restricted_loss", "legacy_excluded_loss", "legacy_sum_wave_r2"}
    previous = -1
    for row in hist:
        if not isinstance(row, dict) or required_row - row.keys():
            raise ValueError("incomplete grok metric history; raw logits and legacy metrics are required")
        st = row["step"]
        if not isinstance(st, int) or isinstance(st, bool) or not previous < st <= saved:
            raise ValueError("grok measurement steps must be strictly increasing within the saved interval")
        previous = st
        L = row["_logits"]
        if not isinstance(L, np.ndarray) or L.shape != (P, P, P) or L.dtype != np.float32 or not np.isfinite(L).all():
            raise ValueError("grok checkpoint needs finite float32 P-by-P-by-P logits for every measurement")
        for name in required_row - {"_logits", "legacy_key"}:
            if not np.isfinite(np.asarray(row[name])).all():
                raise ValueError(f"nonfinite retained grok metric: {name}")
        keys = row["legacy_key"]
        if len(keys) != N_KEY or len(set(keys)) != N_KEY or any(not 1 <= k <= (P - 1) // 2 for k in keys):
            raise ValueError("invalid retained adaptive grok keys")
    recorded = {row["step"] for row in hist}
    if hist[0]["step"] != 0 or hist[-1]["step"] != saved or not set(range(0, saved + 1, SNAP)) <= recorded:
        raise ValueError("grok checkpoint history does not cover all measurements through its saved state")


def _atomic_checkpoint(path, state):
    """Serialize locally owned state to a sibling temporary file and atomically replace the checkpoint."""
    import torch

    path = Path(path)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            torch.save(state, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def train(ckpt_path, steps=STEPS, log=print):
    """Train the unchanged local adaptation, retaining logits and pinned atomic resumable state.

    Returned history has corrected fixed-final-key metrics and distinct legacy_* adaptive metrics. Raw `_logits`
    remain in its rows/checkpoint for inspection; scene-result exporters should select named public fields only.
    """
    import torch
    import torch.nn.functional as F

    if not isinstance(steps, int) or isinstance(steps, bool) or steps < 0:
        raise ValueError("steps must be a nonnegative integer")
    x, y, tr, te = dataset()
    pins = checkpoint_pins(x, y, tr, te, steps, dict(torch=str(torch.__version__), numpy=np.__version__))
    torch.manual_seed(SEED)
    model = build()
    opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WD, betas=(0.9, 0.98))
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(s / 10, 1.0))
    hist, start = [], 0
    if os.path.exists(ckpt_path):
        ck = torch.load(ckpt_path, weights_only=False)
        validate_checkpoint(ck, pins, steps)
        model.load_state_dict(ck["model"])
        opt.load_state_dict(ck["opt"])
        sched.load_state_dict(ck["sched"])
        hist, start = ck["hist"], ck["step"]
        torch.set_rng_state(ck["rng"])
        log(f"    resuming grokking at step {start}")
    xt, yt = x[tr], y[tr]
    for s in range(start, steps + 1):
        if (s % SNAP == 0 or s % CKPT == 0 or s == steps) and (not hist or hist[-1]["step"] < s):
            m = measure(model, x, y, tr, te)
            m["step"] = s
            if s % 1000 == 0 or s in (100, 200, 500) or s == steps:
                m["WE"] = model.WE[:P].detach().numpy().astype(np.float16)  # the embedding at a few moments
            hist.append(m)
            if s % 1000 == 0:
                log(f"    step {s}: train {m['train_loss']:.3g} test {m['test_loss']:.3g} acc {m['test_acc']:.2f} "
                    f"legacy adaptive key {m['legacy_key']} restricted {m['legacy_restricted_loss']:.3g} "
                    f"excluded {m['legacy_excluded_loss']:.3g}")
        if s == steps:
            key, output_spectrum = output_key_frequencies(_array(model.W2).astype(np.float64) @ _array(model.WU))
            finalize_history(hist, key, output_spectrum, _array(y), _array(tr), _array(te))
        if (s % CKPT == 0 and s > start) or s == steps:
            _atomic_checkpoint(ckpt_path, dict(metric_schema=METRIC_SCHEMA, pins=pins, model=model.state_dict(),
                                             opt=opt.state_dict(), sched=sched.state_dict(), hist=hist,
                                             step=s, rng=torch.get_rng_state()))
        if s == steps:
            break
        loss = F.cross_entropy(model(xt), yt)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    return model, hist, (x, y, tr, te)


def analyse(model, x, y):
    """Final activations and separate sum-wave / phase-constrained cosine diagnostics for the local adaptation."""
    import torch

    B, names = fourier_basis()
    with torch.no_grad():
        _, c = model(x, keep=True)
        act = c["act"].double().numpy().reshape(P, P, DMLP)  # neuron activations over the grid of (a, b)
        z = model(x).double().numpy().reshape(P, P, P)
    # each neuron's activation in the 2D Fourier basis: its energy per frequency (a's and b's waves, and products)
    A2 = np.einsum("ia,jb,abn->ijn", B, B, act)  # (p, p, neurons)
    nk = (P - 1) // 2
    energy = np.zeros((nk, DMLP))
    for k in range(1, nk + 1):
        idx = [2 * k - 1, 2 * k]
        energy[k - 1] = (A2[np.ix_(idx, idx)] ** 2).sum((0, 1)) + (A2[np.ix_([0], idx)] ** 2).sum((0, 1)) + \
            (A2[np.ix_(idx, [0])] ** 2).sum((0, 1))
    tot = (A2 ** 2).sum((0, 1)) - A2[0, 0] ** 2
    frac = energy / np.maximum(tot, 1e-12)
    nfreq = frac.argmax(0) + 1
    nshare = frac.max(0)
    # the logits fit by the key frequencies' waves cos(w_k (a + b - c)) alone
    L = z - z.mean(-1, keepdims=True)
    a = np.arange(P)
    s = (a[:, None, None] + a[None, :, None] - a[None, None, :]) % P
    key, output_spectrum = output_key_frequencies(_array(model.W2).astype(np.float64) @ _array(model.WU))
    return dict(neuron_freq=nfreq, neuron_share=nshare, act=act, L=L, s=s, key_final=key, key_rule=KEY_RULE,
                output_spectrum=output_spectrum, **circuit_diagnostics(L, key))
