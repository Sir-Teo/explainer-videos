"""Precompute everything numerical in Part 17 of the AI series ("Silicon").

    python -m videos.ai.ai17.compute                 # everything missing (single-thread items; run under nice)
    python -m videos.ai.ai17.compute matmul_mt       # the 4-thread measurement: short, run when the machine is quiet
    python -m videos.ai.ai17.compute --force formats

Results are cached in ``.cache/ai17/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The measurements are of
the machine that runs this, so they differ from machine to machine (and from run to run on a busy one: each records the
load average it saw).  Published numbers (GPUs, TPUs, papers) are in ``specs.py``, cited there.

Items:
    machine     the CPU, its caches and SIMD, the BLAS libraries, the compiler
    matmul      matrix products C = AB of growing size (numpy fp32/fp64, torch fp32/bf16), matrix-vector products and
                STREAM-style copies, one thread each: the points of this machine's roofline
    matmul_mt   the same with every core (4 threads here): short, and sensitive to other jobs
    hierarchy   one core reading arrays from 4 KiB to 256 MiB (bandwidth per cache level) and chasing random pointers
                through them (latency per level); STREAM triad and copy from main memory
    blocking    C = AB at n = 1024 three ways in C (the textbook loop, loops reordered, tiled) against BLAS; and the
                tiled loop for tile sizes 8 to 512
    systolic    a 4 x 4 output-stationary systolic array computing C = AB cycle by cycle (checked against numpy); the
                utilization of a 256 x 256 array on matrices of every size up to 1,024
    formats     FP32 ... FP4 and the block formats (MXFP8, MXFP4, NVFP4): rounding error on Gaussian samples and on
                the series' own trained weights, against the unit-roundoff prediction; one number in every format
    warps       a warp scheduler hiding memory latency with more warps (simulated); branch divergence on random and
                sorted data (simulated); H100 occupancy by registers and shared memory (NVIDIA's limits)
    collectives this machine's processes as a cluster: point-to-point time against message size (fit to alpha +
                n/beta), and ring against tree all-reduce on 4 processes, measured and predicted; a ring all-reduce
                traced step by step for the animation
    trends      clock speed, single-thread speed, transistors and cores, 1971-2021 (K. Rupp's data); accelerator
                FLOP/s, memory bandwidth and FLOP/s per watt, 2010-2026 (Epoch AI's database): fits and doubling times
"""

from __future__ import annotations

import csv
import json
import math
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

# This process measures one core: numpy's BLAS (OpenBLAS, MKL, or Apple's Accelerate on macOS) gets one thread
# unless the caller says otherwise; the multi-thread measurement runs in a subprocess with its own settings.
if __name__ == "__main__":
    for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        os.environ.setdefault(_v, "1")

import numpy as np  # noqa: E402

from explainer.ai.cache import Cache  # noqa: E402

CACHE = Cache("ai17")
load = CACHE.load
HERE = Path(__file__).parent
DATA = HERE / "data"


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def loadavg() -> list[float]:
    try:
        return [round(x, 2) for x in os.getloadavg()]
    except OSError:
        return []


# ---------------------------------------------------------------------------
# The machine
# ---------------------------------------------------------------------------
def _sysctl(key: str) -> str:
    try:
        return subprocess.run(["sysctl", "-n", key], capture_output=True, text=True).stdout.strip()
    except OSError:
        return ""


def cpu_info() -> dict:
    out = dict(platform=platform.platform(), machine=platform.machine(), cores=os.cpu_count(), model="", caches={},
               simd=[])
    if sys.platform.startswith("linux"):
        try:
            txt = Path("/proc/cpuinfo").read_text()
            for line in txt.splitlines():
                if line.startswith("model name") and not out["model"]:
                    out["model"] = line.split(":", 1)[1].strip()
                if line.startswith("flags"):
                    fl = set(line.split(":", 1)[1].split())
                    out["simd"] = [f for f in ("sse4_2", "avx", "avx2", "fma", "avx512f", "avx512_bf16", "amx_tile")
                                   if f in fl]
                    break
        except OSError:
            pass
        base = Path("/sys/devices/system/cpu/cpu0/cache")
        for d in sorted(base.glob("index*")):
            try:
                lvl, typ = (d / "level").read_text().strip(), (d / "type").read_text().strip()
                size = (d / "size").read_text().strip()
                shared = (d / "shared_cpu_list").read_text().strip()
            except OSError:
                continue
            if typ in ("Data", "Unified"):
                kb = int(size.rstrip("K")) if size.endswith("K") else int(size.rstrip("M")) * 1024
                out["caches"][f"L{lvl}"] = dict(kib=kb, shared=shared)
    elif sys.platform == "darwin":
        out["model"] = _sysctl("machdep.cpu.brand_string") or _sysctl("hw.model")  # "Apple M3 Pro"; "MacBookPro18,3"
        for lvl, key in (("L1", "hw.l1dcachesize"), ("L2", "hw.l2cachesize"), ("L3", "hw.l3cachesize")):
            v = _sysctl(key)
            if v.isdigit() and int(v) > 0:
                out["caches"][lvl] = dict(kib=int(v) // 1024, shared="")
        out["simd"] = ["neon"] if platform.machine() == "arm64" else []
        if _sysctl("hw.optional.arm.FEAT_BF16") == "1" or "AVX512BF16" in _sysctl("machdep.cpu.leaf7_features"):
            out["simd"].append("bf16")
    out["model"] = out["model"] or platform.processor() or platform.machine()
    try:
        out["ram_gib"] = round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2**30, 1)
    except (ValueError, OSError, AttributeError):
        out["ram_gib"] = 0.0
    return out


def short_model(model: str) -> str:
    """'Intel(R) Xeon(R) Processor @ 2.80GHz' -> 'Intel Xeon Processor @ 2.80GHz'"""
    return " ".join(model.replace("(R)", "").replace("(TM)", "").replace("CPU", "").split())


def compute_machine():
    from videos.ai.ai17 import native

    info = cpu_info()
    info["model_short"] = short_model(info["model"])
    np_cfg = {}
    try:
        cfg = np.show_config(mode="dicts")
        blas = cfg.get("Build Dependencies", {}).get("blas", {})
        np_cfg = dict(blas=blas.get("name", ""), blas_version=blas.get("version", ""))
    except Exception:  # noqa: BLE001
        pass
    info["numpy"] = dict(version=np.__version__, **np_cfg)
    try:
        import torch

        par = torch.__config__.parallel_info()
        lib = "MKL" if "Math Kernel Library" in par else ("OpenBLAS" if "OpenBLAS" in par else "")
        info["torch"] = dict(version=torch.__version__, blas=lib)
    except Exception:  # noqa: BLE001
        info["torch"] = {}
    lib = native.load()
    info["compiler"] = dict(native.INFO) if lib is not None else {}
    info["python"] = platform.python_version()
    info["loadavg"] = loadavg()
    print(f"    {info['model_short']}, {info['cores']} cores, caches {info['caches']}, {info['simd']}")
    return info


# ---------------------------------------------------------------------------
# Matrix products, matrix-vector products and copies: the points of the roofline
# ---------------------------------------------------------------------------
_BENCH = r'''
import json, sys, time
import numpy as np
cfg = json.loads(sys.argv[1])

def best_rate(fn, flops, min_t=0.15, trials=7):
    fn()
    t = time.perf_counter(); fn(); one = max(time.perf_counter() - t, 1e-7)
    reps = max(1, int(min_t / one))
    rates = []
    for _ in range(trials):
        t = time.perf_counter()
        for _ in range(reps):
            fn()
        rates.append(flops * reps / (time.perf_counter() - t))
    rates.sort()
    return rates[-1], rates[len(rates) // 2]

out = {}
g = np.random.default_rng(0)
for dt in cfg["np_dtypes"]:
    rows = []
    for n in cfg["sizes"]:
        a = g.standard_normal((n, n)).astype(dt); b = g.standard_normal((n, n)).astype(dt); c = np.empty_like(a)
        best, med = best_rate(lambda: np.matmul(a, b, out=c), 2.0 * n ** 3, trials=cfg["trials"])
        rows.append([n, best, med])
    out["np_" + dt] = rows
rows = []
for n in cfg["gemv"]:
    a = g.standard_normal((n, n)).astype("float32"); x = g.standard_normal(n).astype("float32"); y = np.empty(n, "float32")
    best, med = best_rate(lambda: np.matmul(a, x, out=y), 2.0 * n * n, trials=cfg["trials"])
    rows.append([n, best, med])
out["gemv"] = rows
if cfg["torch"]:
    import torch
    torch.set_num_threads(cfg["threads"])
    for name, dt in (("torch_float32", torch.float32), ("torch_bfloat16", torch.bfloat16)):
        rows = []
        for n in cfg["torch_sizes"]:
            a = torch.randn(n, n, dtype=dt); b = torch.randn(n, n, dtype=dt)
            best, med = best_rate(lambda: torch.mm(a, b), 2.0 * n ** 3, trials=cfg["trials"])
            rows.append([n, best, med])
        out[name] = rows
    x = torch.randn(cfg["copy_n"]); y = torch.empty_like(x)
    best, med = best_rate(lambda: y.copy_(x), 8.0 * x.numel(), trials=cfg["trials"])
    out["torch_copy"] = [best, med]   # bytes per second (read + write)
x = g.standard_normal(cfg["copy_n"]).astype("float32"); y = np.empty_like(x)
best, med = best_rate(lambda: np.copyto(y, x), 8.0 * x.size, trials=cfg["trials"])
out["np_copy"] = [best, med]
print(json.dumps(out))
'''


def run_bench(threads: int, **cfg) -> dict:
    env = dict(os.environ)
    for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS",
              "NUMEXPR_NUM_THREADS"):
        env[k] = str(threads)
    cfg = dict(threads=threads, **cfg)
    try:
        import torch  # noqa: F401
        cfg.setdefault("torch", True)
    except ImportError:
        cfg["torch"] = False
    r = subprocess.run([sys.executable, "-c", _BENCH, json.dumps(cfg)], env=env, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr[-2000:])
    return json.loads(r.stdout)


SIZES = [32, 64, 128, 256, 512, 1024, 2048, 4096]


def compute_matmul():
    la = loadavg()
    b = run_bench(1, sizes=SIZES, np_dtypes=["float32", "float64"], gemv=[1024, 2048, 4096, 8192],
                  torch_sizes=[256, 1024], copy_n=1 << 26, trials=7)
    out = dict(threads=1, loadavg_before=la, loadavg_after=loadavg(), **{k: np.asarray(v) for k, v in b.items()})
    best = max(r[1] for r in b["np_float32"])
    print(f"    one thread: fp32 matmul up to {best / 1e9:.1f} GFLOP/s; copy {b['np_copy'][0] / 1e9:.1f} GB/s;"
          f" gemv {max(r[1] for r in b['gemv']) / 1e9:.1f} GFLOP/s; load {la}")
    return out


def compute_matmul_mt():
    threads = os.cpu_count() or 4
    la = loadavg()
    b = run_bench(threads, sizes=SIZES, np_dtypes=["float32"], gemv=[4096, 8192], torch_sizes=[1024, 2048, 4096],
                  copy_n=1 << 26, trials=5)
    out = dict(threads=threads, loadavg_before=la, loadavg_after=loadavg(), **{k: np.asarray(v) for k, v in b.items()})
    best = max(r[1] for r in b["np_float32"])
    print(f"    {threads} threads: fp32 matmul up to {best / 1e9:.1f} GFLOP/s; load {la} -> {out['loadavg_after']}")
    return out


# ---------------------------------------------------------------------------
# The memory hierarchy, measured on one core
# ---------------------------------------------------------------------------
def compute_hierarchy():
    from videos.ai.ai17 import native

    L = native.load()
    la = loadavg()
    sizes = [int(2 ** e) for e in np.arange(12, 28.01, 0.5)]  # 4 KiB ... 256 MiB
    sizes = sorted({max(4096, s // 4096 * 4096) for s in sizes})
    bw, lat = [], []
    g = rng(17)
    for s in sizes:
        n = s // 4
        if L is not None:
            big = native.BigArray(L, n, np.float32)
            a = big.a
            a[:] = 1.0
            reps = max(1, int(2e9 / s))
            best = 0.0
            for _ in range(5):
                t = time.perf_counter()
                L.read_sum(native.ptr(a), n, reps)
                best = max(best, reps * s / (time.perf_counter() - t))
            big.close()
        else:
            a = np.ones(n, np.float32)
            reps = max(1, int(5e8 / s))
            best = 0.0
            for _ in range(3):
                t = time.perf_counter()
                for _ in range(reps):
                    a.sum()
                best = max(best, reps * s / (time.perf_counter() - t))
        bw.append(best)
        # latency: a random cycle through one int64 per 64-byte line
        lines = max(s // 64, 8)
        perm = g.permutation(lines)
        if L is not None:
            big = native.BigArray(L, lines * 8, np.int64)
            nxt = big.a
        else:
            nxt = np.zeros(lines * 8, np.int64)
        nxt[perm * 8] = np.roll(perm, -1) * 8
        steps = 4_000_000 if L is not None else 200_000
        best_t = float("inf")
        for _ in range(3):
            if L is not None:
                t = time.perf_counter()
                L.chase(native.ptr(nxt), steps)
                best_t = min(best_t, (time.perf_counter() - t) / steps)
            else:
                i, nx = 0, nxt.tolist()
                t = time.perf_counter()
                for _ in range(steps):
                    i = nx[i]
                best_t = min(best_t, (time.perf_counter() - t) / steps)
        if L is not None:
            nxt = None
            big.close()
        lat.append(best_t)
        print(f"    {s / 1024:9.0f} KiB  {best / 1e9:7.1f} GB/s  {best_t * 1e9:6.1f} ns", flush=True)
    stream = {}
    if L is not None:
        n = 1 << 25  # 128 MiB per array, well past the last cache
        a, b, c = (np.full(n, v, np.float32) for v in (0.0, 1.0, 2.0))
        kernels = {"triad": (lambda: L.triad(native.ptr(a), native.ptr(b), native.ptr(c), 3.0, n, 1), 12 * n),
                   "copy": (lambda: L.copy(native.ptr(a), native.ptr(b), n, 1), 8 * n)}
        for name, (fn, nbytes) in kernels.items():  # bytes as STREAM counts them: each array read or written once
            fn()
            best = 0.0
            for _ in range(8):
                t = time.perf_counter()
                fn()
                best = max(best, nbytes / (time.perf_counter() - t))
            stream[name] = best
    out = dict(sizes=np.asarray(sizes), bandwidth=np.asarray(bw), latency=np.asarray(lat), stream=stream,
               native=L is not None, loadavg_before=la, loadavg_after=loadavg())
    return out


# ---------------------------------------------------------------------------
# Cache blocking: the same arithmetic, three loop orders
# ---------------------------------------------------------------------------
def compute_blocking(n=1024, tiles=(8, 16, 32, 64, 128, 256, 512)):
    from videos.ai.ai17 import native

    L = native.load()
    la = loadavg()
    g = rng(1)
    A = g.standard_normal((n, n)).astype(np.float32)
    B = g.standard_normal((n, n)).astype(np.float32)
    C = np.zeros((n, n), np.float32)
    ref = (A.astype(np.float64) @ B.astype(np.float64))
    flops = 2.0 * n ** 3

    def timed(fn, trials):
        best = float("inf")
        for _ in range(trials):
            C[:] = 0
            t = time.perf_counter()
            fn()
            best = min(best, time.perf_counter() - t)
        err = float(np.abs(C - ref).max() / np.abs(ref).max())
        return flops / best, err

    out = dict(n=n, tiles=np.asarray(tiles), loadavg_before=la)
    if L is not None:
        out["lang"] = "C"
        out["naive"], e1 = timed(lambda: L.mm_naive(native.ptr(A), native.ptr(B), native.ptr(C), n), 2)
        out["ikj"], e2 = timed(lambda: L.mm_ikj(native.ptr(A), native.ptr(B), native.ptr(C), n), 3)
        rates, errs = [], [e1, e2]
        for bs in tiles:
            r, e = timed(lambda: L.mm_blocked(native.ptr(A), native.ptr(B), native.ptr(C), n, int(bs)), 3)
            rates.append(r)
            errs.append(e)
        out["blocked"] = np.asarray(rates)
        assert max(errs) < 1e-4, errs  # every loop order computes the same product
    else:  # no C compiler: the same three loop orders in Python, numpy doing the innermost loop (and saying so)
        out["lang"] = "numpy"
        def naive():
            for i in range(n):
                Ai = A[i]
                for j in range(n):
                    C[i, j] = Ai @ B[:, j]

        def ikj():
            for i in range(n):
                Ci = C[i]
                for k in range(n):
                    Ci += A[i, k] * B[k]

        def blocked(bs):
            for ii in range(0, n, bs):
                for kk in range(0, n, bs):
                    for jj in range(0, n, bs):
                        C[ii:ii + bs, jj:jj + bs] += A[ii:ii + bs, kk:kk + bs] @ B[kk:kk + bs, jj:jj + bs]

        out["naive"], e1 = timed(naive, 1)
        out["ikj"], e2 = timed(ikj, 1)
        rates, errs = [], [e1, e2]
        for bs in tiles:
            r, e = timed(lambda: blocked(int(bs)), 1 if bs < 32 else 2)
            rates.append(r)
            errs.append(e)
        out["blocked"] = np.asarray(rates)
        assert max(errs) < 1e-4, errs
    b = run_bench(1, sizes=[n], np_dtypes=["float32"], gemv=[256], torch_sizes=[64], copy_n=1 << 16, trials=5)
    out["blas"] = float(b["np_float32"][0][1])
    out["loadavg_after"] = loadavg()
    print(f"    n={n}: naive {out['naive'] / 1e9:.2f}, ikj {out['ikj'] / 1e9:.2f}, blocked "
          f"{', '.join(f'{r / 1e9:.1f}' for r in out['blocked'])}, BLAS {out['blas'] / 1e9:.1f} GFLOP/s")
    return out


# ---------------------------------------------------------------------------
# A systolic array, cycle by cycle
# ---------------------------------------------------------------------------
def systolic_trace(A: np.ndarray, B: np.ndarray):
    """Output-stationary n x n array (H. T. Kung's scheme): row i of A enters from the left delayed i cycles, column j
    of B from the top delayed j cycles; each processing element multiplies what passes through it and keeps a running
    sum. Returns per cycle the a and b values held in each PE (nan when empty) and the accumulators."""
    n, K = A.shape[0], A.shape[1]
    T = K + 2 * n - 2
    a_reg = np.full((T, n, n), np.nan)
    b_reg = np.full((T, n, n), np.nan)
    acc = np.zeros((T, n, n))
    cur_a = np.full((n, n), np.nan)
    cur_b = np.full((n, n), np.nan)
    c = np.zeros((n, n))
    for t in range(T):
        new_a = np.full((n, n), np.nan)
        new_b = np.full((n, n), np.nan)
        new_a[:, 1:] = cur_a[:, :-1]  # values move one PE right / down per cycle
        new_b[1:, :] = cur_b[:-1, :]
        for i in range(n):
            k = t - i
            if 0 <= k < K:
                new_a[i, 0] = A[i, k]
        for j in range(n):
            k = t - j
            if 0 <= k < K:
                new_b[0, j] = B[k, j]
        cur_a, cur_b = new_a, new_b
        both = ~np.isnan(cur_a) & ~np.isnan(cur_b)
        c = c + np.where(both, np.nan_to_num(cur_a) * np.nan_to_num(cur_b), 0.0)
        a_reg[t], b_reg[t], acc[t] = cur_a, cur_b, c
    return a_reg, b_reg, acc, T


def compute_systolic():
    g = rng(2017)
    n = 4
    A = g.integers(-3, 4, (n, n)).astype(float)
    B = g.integers(-3, 4, (n, n)).astype(float)
    a_reg, b_reg, acc, T = systolic_trace(A, B)
    assert np.array_equal(acc[-1], A @ B)  # the array computes the product exactly
    # every PE fires once per k; the last product lands at cycle K + 2n - 2
    fires = (~np.isnan(a_reg) & ~np.isnan(b_reg)).sum(axis=(1, 2))
    # a 256 x 256 weight-stationary array (TPU v1) running a d x d layer: tiles padded to multiples of 256
    d = np.arange(1, 1025)
    tiles = np.ceil(d / 256)
    util = (d / (256 * tiles)) ** 2
    # a bigger trace to check the cycle count formula
    for nn, K in ((3, 5), (6, 2), (8, 8)):
        _, _, ac, TT = systolic_trace(g.integers(-3, 4, (nn, K)).astype(float), g.integers(-3, 4, (K, nn)).astype(float))
        assert TT == K + 2 * nn - 2
    return dict(n=n, A=A, B=B, C=A @ B, a_reg=a_reg, b_reg=b_reg, acc=acc, cycles=T, fires=fires, d=d, util=util)


# ---------------------------------------------------------------------------
# Number formats
# ---------------------------------------------------------------------------
# name: (exponent bits, mantissa bits, largest finite value, smallest normal exponent)
FORMATS = {
    "FP32": (8, 23, float(np.finfo(np.float32).max), -126),
    "TF32": (8, 10, (2 - 2.0 ** -10) * 2.0 ** 127, -126),
    "BF16": (8, 7, (2 - 2.0 ** -7) * 2.0 ** 127, -126),
    "FP16": (5, 10, 65504.0, -14),
    "E4M3": (4, 3, 448.0, -6),
    "E5M2": (5, 2, 57344.0, -14),
    "E3M2": (3, 2, 28.0, -2),
    "E2M3": (2, 3, 7.5, 0),
    "E2M1": (2, 1, 6.0, 0),
}


SCALED = ("E4M3", "E5M2", "E3M2", "E2M3", "E2M1")  # eight bits and fewer: one scale per tensor, as in practice


def quantize(x: np.ndarray, fmt: str) -> np.ndarray:
    """Round to nearest (ties to even) in a binary floating-point format with subnormals, saturating at its largest
    finite value (as ML hardware does for FP8 and FP4)."""
    e_bits, m_bits, vmax, emin = FORMATS[fmt]
    x = np.asarray(x, np.float64)
    ax = np.abs(x)
    with np.errstate(divide="ignore"):
        e = np.floor(np.log2(np.where(ax > 0, ax, 1.0)))
    e = np.maximum(e, emin)  # below the normal range the spacing stays that of the smallest binade: subnormals
    step = 2.0 ** (e - m_bits)
    q = np.rint(x / step) * step
    return np.clip(q, -vmax, vmax)


def e8m0(x):
    """MX's shared scale: a power of two (an 8-bit exponent, no mantissa)."""
    return 2.0 ** np.floor(np.log2(np.maximum(x, 2.0 ** -127)))


def mx_quantize(x: np.ndarray, fmt: str, block=32) -> np.ndarray:
    """OCP Microscaling (2023): blocks of 32 share a power-of-two scale, 2^(floor(log2 amax) - emax of the element
    format); the elements are then rounded in the element format, saturating."""
    emax = {"E4M3": 8, "E5M2": 15, "E2M1": 2, "E2M3": 2, "E3M2": 4}[fmt]
    v = x.reshape(-1, block)
    amax = np.abs(v).max(1, keepdims=True)
    s = e8m0(amax) / 2.0 ** emax
    s = np.where(amax > 0, s, 1.0)
    return (quantize(v / s, fmt) * s).reshape(x.shape)


def nvfp4_quantize(x: np.ndarray, block=16) -> np.ndarray:
    """NVIDIA's NVFP4 (2025): E2M1 elements, an E4M3 scale per block of 16, and one FP32 scale per tensor."""
    v = x.reshape(-1, block)
    amax_t = np.abs(v).max()
    st = amax_t / (6.0 * 448.0) if amax_t > 0 else 1.0
    amax = np.abs(v).max(1, keepdims=True)
    sb = quantize(amax / 6.0 / st, "E4M3")
    sb = np.where(sb > 0, sb, 1.0)
    return (quantize(v / (sb * st), "E2M1") * sb * st).reshape(x.shape)


def tensor_scaled(x: np.ndarray, fmt: str) -> np.ndarray:
    """One scale per tensor: the largest magnitude lands on the format's largest value."""
    vmax = FORMATS[fmt][2]
    s = np.abs(x).max() / vmax
    return quantize(x / s, fmt) * s


def rel_rms(x, q) -> float:
    return float(np.sqrt(np.mean((q - x) ** 2) / np.mean(x ** 2)))


def bits_of(x: float, fmt: str) -> dict:
    """The sign, exponent and mantissa fields of x rounded into fmt (normal numbers)."""
    e_bits, m_bits, _, emin = FORMATS[fmt]
    q = float(quantize(np.array([x]), fmt)[0])
    bias = 2 ** (e_bits - 1) - 1
    if fmt in ("E2M1", "E2M3", "E3M2"):
        bias = 2 ** (e_bits - 1) - 1
    s = 0 if q >= 0 else 1
    a = abs(q)
    e = int(math.floor(math.log2(a)))
    frac = a / 2 ** e - 1
    man = int(round(frac * 2 ** m_bits))
    return dict(value=q, sign=s, exp=format(e + bias, f"0{e_bits}b"), man=format(man, f"0{m_bits}b"))


def narrator_weights(n=1 << 22):
    """The narrator's own weights, if Qwen3-TTS is in the Hugging Face cache here: one feed-forward matrix of its
    language model (stored in bfloat16), as float32."""
    import json as _json
    import struct

    hub = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface")) / "hub"
    files = sorted(hub.glob("models--Qwen--Qwen3-TTS-12Hz-1.7B-Base/snapshots/*/model.safetensors"))
    if not files:
        return None
    with open(files[0], "rb") as f:
        hlen = struct.unpack("<Q", f.read(8))[0]
        head = _json.loads(f.read(hlen))
        key = "talker.model.layers.10.mlp.down_proj.weight"
        if key not in head or head[key]["dtype"] != "BF16":
            return None
        a, b = head[key]["data_offsets"]
        f.seek(8 + hlen + a)
        raw = np.frombuffer(f.read(min(b - a, 2 * n)), np.uint16)
    return (raw.astype(np.uint32) << 16).view(np.float32).copy()


def series_weights():
    """Real weights to round: the series' own model (explainer/ai/novels.py) if it has been trained here, else the
    narrator's (Qwen3-TTS), else none. Returns (values, source)."""
    try:
        from explainer.ai import novels

        if (novels.OUT / "base.pt").exists():
            import torch

            ck = torch.load(novels.OUT / "base.pt", map_location="cpu", weights_only=False)
            mats = [v.float().numpy().ravel() for k, v in ck["model"].items() if v.ndim == 2]
            return np.concatenate(mats), "novels"
    except Exception as e:  # noqa: BLE001
        print("    (no series weights:", e, ")")
    try:
        w = narrator_weights()
        if w is not None:
            return w, "narrator"
    except Exception as e:  # noqa: BLE001
        print("    (no narrator weights:", e, ")")
    return None, ""


def compute_formats():
    g = rng(754)
    x = g.standard_normal(1 << 20)  # float64 Gaussian samples, a multiple of 32
    rows = {}
    for f, (eb, mb, vmax, emin) in FORMATS.items():
        rows[f] = dict(e=eb, m=mb, max=vmax, min_normal=2.0 ** emin, min_sub=2.0 ** (emin - mb),
                       u=2.0 ** -(mb + 1), predict=2.0 ** -mb * math.sqrt(math.log(2) / 18),
                       gauss=rel_rms(x, tensor_scaled(x, f) if f in SCALED else quantize(x, f)))
    blocks = {"MXFP8": lambda v: mx_quantize(v, "E4M3"), "MXFP6": lambda v: mx_quantize(v, "E2M3"),
              "MXFP4": lambda v: mx_quantize(v, "E2M1"), "NVFP4": nvfp4_quantize,
              "FP4 (one scale)": lambda v: tensor_scaled(v, "E2M1"), "FP8 (one scale)": lambda v: tensor_scaled(v, "E4M3")}
    block_rows = {k: dict(gauss=rel_rms(x, fn(x))) for k, fn in blocks.items()}
    w, src = series_weights()
    if w is not None:
        w = w[: (w.size // 32) * 32]
        for f in rows:
            rows[f]["weights"] = rel_rms(w, tensor_scaled(w, f) if f in SCALED else quantize(w, f))
        for k, fn in blocks.items():
            block_rows[k]["weights"] = rel_rms(w, fn(w))
    # one number in every format, field by field
    pi = {f: bits_of(math.pi, f) for f in FORMATS}
    # a slice of real values and their FP4 roundings, for the picture of a block being scaled
    sample = (w if w is not None else x)[:64].astype(np.float64)
    out = dict(rows=rows, blocks=block_rows, weights_source=src, n_weights=int(w.size) if w is not None else 0,
               pi=pi, sample=sample, sample_mx=mx_quantize(sample, "E2M1"), sample_nv=nvfp4_quantize(sample),
               sample_t=tensor_scaled(sample, "E2M1"), e2m1_grid=np.unique(np.abs(quantize(np.linspace(-7, 7, 2001), "E2M1"))))
    if w is not None:
        out["w_hist"], edges = np.histogram(w / np.abs(w).max(), bins=160, range=(-1, 1))
        out["w_std_over_max"] = float(w.std() / np.abs(w).max())
    for f in ("FP16", "BF16", "E4M3", "E2M1"):
        print(f"    {f}: Gaussian rel. RMS error {rows[f]['gauss']:.2e} (predicted {rows[f]['predict']:.2e})")
    return out


# ---------------------------------------------------------------------------
# Warps: latency hiding, divergence, occupancy
# ---------------------------------------------------------------------------
def simulate_scheduler(W: int, c: int, lat: int, T=40_000) -> float:
    """One warp scheduler issuing at most one instruction per cycle, greedy-then-oldest: it keeps issuing from the same
    warp until that warp has to wait, then turns to the oldest ready one. Each warp runs c arithmetic instructions, then
    a load, then waits ``lat`` cycles for it. Returns the fraction of cycles that issue an instruction."""
    ready_at = np.zeros(W, np.int64)
    left = np.full(W, c + 1)
    issued, cur = 0, 0
    for t in range(T):
        if ready_at[cur] > t:
            ready = np.flatnonzero(ready_at <= t)
            if ready.size == 0:
                continue
            cur = int(ready[0])
        issued += 1
        left[cur] -= 1
        if left[cur] == 0:
            ready_at[cur] = t + 1 + lat
            left[cur] = c + 1
    return issued / T


def compute_warps():
    from videos.ai.ai17.specs import CC90, H800_LAT

    lat = int(round(H800_LAT["glob"]))
    Ws = np.arange(1, 17)
    cs = (4, 16, 64)
    util = np.array([[simulate_scheduler(int(W), c, lat) for W in Ws] for c in cs])
    theory = np.array([[min(1.0, W * (c + 1) / (c + 1 + lat)) for W in Ws] for c in cs])
    # divergence: a branch on the data, if-path and else-path the same length
    g = rng(32)
    N = 32 * 4096
    qs = np.linspace(0.0, 1.0, 41)
    eff_rand, eff_sort = [], []
    for q in qs:
        v = g.random(N) < q
        for arr, store in ((v, eff_rand), (np.sort(v), eff_sort)):
            w_ = arr.reshape(-1, 32)
            any_t, any_f = w_.any(1), (~w_).any(1)
            store.append(float(32 / (32 * (any_t.astype(int) + any_f.astype(int))).mean()))
    # occupancy on an H100: warps resident per SM out of 64
    def occupancy(threads, regs, smem):
        wpb = math.ceil(threads / 32)
        regs_warp = math.ceil(regs * 32 / CC90["reg_unit"]) * CC90["reg_unit"]
        by_regs = CC90["regs"] // (regs_warp * wpb)
        by_smem = CC90["smem"] // (smem + CC90["smem_reserved"]) if smem else CC90["blocks"]
        by_warps = CC90["warps"] // wpb
        blocks = min(by_regs, by_smem, by_warps, CC90["blocks"])
        return blocks * wpb / CC90["warps"], dict(regs=by_regs, smem=by_smem, warps=by_warps, cap=CC90["blocks"])

    regs = np.arange(16, 256, 8)
    occ_regs = np.array([occupancy(256, int(r), 0)[0] for r in regs])
    smems = np.arange(0, 228 * 1024, 4 * 1024)
    occ_smem = np.array([occupancy(256, 32, int(s))[0] for s in smems])
    # the tiled matmul kernel of chapter 11: 32 x 32 tiles of A and B in shared memory, one thread per output
    ex_occ, ex_lim = occupancy(1024, 32, 2 * 32 * 32 * 4)
    ex2_occ, ex2_lim = occupancy(256, 128, 64 * 1024)
    return dict(lat=lat, Ws=Ws, cs=np.asarray(cs), util=util, theory=theory, qs=qs, eff_rand=np.asarray(eff_rand),
                eff_sort=np.asarray(eff_sort), regs=regs, occ_regs=occ_regs, smems=smems, occ_smem=occ_smem,
                ex_occ=ex_occ, ex_lim=ex_lim, ex2_occ=ex2_occ, ex2_lim=ex2_lim)


# ---------------------------------------------------------------------------
# Collectives
# ---------------------------------------------------------------------------
def ring_trace(p=4, seed=3):
    """A ring all-reduce of p vectors of p chunks each (small integers), state after every step."""
    g = rng(seed)
    X = g.integers(1, 10, (p, p)).astype(int)  # X[rank, chunk]
    want = X.sum(0)
    states = [X.copy()]
    sends = []
    cur = X.copy()
    for s in range(p - 1):  # reduce-scatter
        nxt = cur.copy()
        step = []
        for r in range(p):
            ch = (r - s) % p
            nxt[(r + 1) % p, ch] = cur[(r + 1) % p, ch] + cur[r, ch]
            step.append((r, (r + 1) % p, ch))
        cur = nxt
        states.append(cur.copy())
        sends.append(step)
    for s in range(p - 1):  # all-gather
        nxt = cur.copy()
        step = []
        for r in range(p):
            ch = (r + 1 - s) % p
            nxt[(r + 1) % p, ch] = cur[r, ch]
            step.append((r, (r + 1) % p, ch))
        cur = nxt
        states.append(cur.copy())
        sends.append(step)
    assert (cur == want[None, :]).all()  # every rank ends with the full sum
    return X, np.asarray(states), np.asarray(sends)


def alpha_beta(n, p, alpha, B):
    """Seconds for ring and binomial-tree all-reduce of n bytes over p devices: T = steps x alpha + bytes sent / B."""
    ring = 2 * (p - 1) * alpha + 2 * (p - 1) / p * n / B
    lg = np.ceil(np.log2(p))
    tree = 2 * lg * (alpha + n / B)
    return ring, tree


def compute_collectives(p=4, reps=7):
    import multiprocessing as mp

    X, states, sends = ring_trace()
    la = loadavg()
    ctx = mp.get_context("spawn")
    sizes = [int(2 ** e) for e in range(3, 26, 1)]  # 8 B ... 32 MiB
    pipes = {}
    for i in range(p):
        for j in range(i + 1, p):
            a, b = ctx.Pipe(duplex=True)
            pipes[(i, j)], pipes[(j, i)] = a, b
    barrier = ctx.Barrier(p)
    q = ctx.Queue()
    from videos.ai.ai17.comm import worker

    procs = [ctx.Process(target=worker, args=(r, p, {j: pipes[(r, j)] for j in range(p) if j != r}, barrier, sizes,
                                                reps, q)) for r in range(p)]
    for pr in procs:
        pr.start()
    res = dict(q.get() for _ in range(p))
    for pr in procs:
        pr.join()
    pp = np.asarray(res[0]["pingpong"])
    ns = np.asarray(sizes, float)
    # fit T = alpha + n / B on the point-to-point times (least squares, weighted by 1/T so small messages count)
    Am = np.stack([np.ones_like(ns), ns], 1) / pp[:, None]
    coef, *_ = np.linalg.lstsq(Am, np.ones_like(ns), rcond=None)
    alpha, B = float(coef[0]), float(1 / coef[1])
    meas = {}
    for algo in ("ring", "tree"):
        T = np.array([[res[r][algo][k] for r in range(p)] for k in range(len(sizes))])  # size, rank, rep
        meas[algo] = T.max(1).min(1)  # slowest rank, best repetition
    # the reduction itself costs time too: one add per element per step, measured with numpy
    a = np.ones(1 << 22, np.float32)
    b_ = np.ones_like(a)
    t = time.perf_counter()
    for _ in range(20):
        np.add(a, b_, out=a)
    gamma = (time.perf_counter() - t) / 20 / a.nbytes  # seconds per byte reduced
    ring_pred, tree_pred = alpha_beta(ns, p, alpha, B)
    ring_pred = ring_pred + (p - 1) / p * ns * gamma
    tree_pred = tree_pred + np.log2(p) * ns * gamma
    # the alpha-beta model in units of alpha, for p devices, against message size in units of alpha*B
    nu = np.logspace(-2, 4, 200)
    ps = np.array([8, 64, 512])
    model = {int(pp_): np.stack(alpha_beta(nu, pp_, 1.0, 1.0)) for pp_ in ps}
    cross = {int(pp_): float(2 * (np.ceil(np.log2(pp_)) - (pp_ - 1)) / (2 * (pp_ - 1) / pp_ - 2 * np.ceil(np.log2(pp_))))
             for pp_ in ps}
    print(f"    alpha {alpha * 1e6:.1f} us, B {B / 1e9:.2f} GB/s; checks ok: {all(res[r]['ok'] for r in range(p))}")
    return dict(p=p, sizes=ns, pingpong=pp, alpha=alpha, B=B, gamma=gamma, ring=meas["ring"], tree=meas["tree"],
                ring_pred=ring_pred, tree_pred=tree_pred, ok=all(res[r]["ok"] for r in range(p)), X=X, states=states,
                sends=sends, nu=nu, ps=ps, **{f"model_{k}": v for k, v in model.items()},
                cross={str(k): v for k, v in cross.items()}, loadavg_before=la, loadavg_after=loadavg())


# ---------------------------------------------------------------------------
# Trends
# ---------------------------------------------------------------------------
def _dat(name):
    a = np.loadtxt(DATA / f"{name}.dat")
    return a[:, 0], a[:, 1]


def doubling_years(t, y) -> float:
    k = np.polyfit(t, np.log2(y), 1)[0]
    return float(1 / k)


FLAGSHIPS = ("NVIDIA Tesla P100 SXM2", "NVIDIA Tesla V100 SXM2", "NVIDIA A100 SXM4 80 GB", "NVIDIA H100 SXM5 80GB",
             "NVIDIA H200 SXM", "NVIDIA B200", "NVIDIA GB200", "NVIDIA B300 (Blackwell Ultra)", "Google TPU v2",
             "Google TPU v3", "Google TPU v4", "Google TPU v5p", "Google TPU v6e Trillium", "Google TPU v7 Ironwood",
             "AMD Radeon Instinct MI250X", "AMD Instinct MI300X", "AMD Instinct MI325X", "AMD Instinct MI355X",
             "Amazon Trainium1", "Amazon Trainium2", "Amazon Trainium3")


def compute_trends():
    out = {}
    for name in ("transistors", "frequency", "specint", "watts", "cores"):
        t, y = _dat(name)
        out[f"{name}_t"], out[f"{name}_y"] = t, y
    ft, fy = out["frequency_t"], out["frequency_y"]
    early = (ft >= 1985) & (ft < 2004)
    late = ft >= 2006
    out["freq_doubling_early"] = doubling_years(ft[early], fy[early])
    out["freq_growth_late"] = float(2 ** (1 / doubling_years(ft[late], fy[late])))  # factor per year
    out["freq_max_late"] = float(fy[late].max())
    out["freq_2004"] = float(fy[(ft >= 2003) & (ft < 2005)].max())
    tt, ty = out["transistors_t"], out["transistors_y"]
    out["transistor_doubling"] = doubling_years(tt, ty)
    st, sy = out["specint_t"], out["specint_y"]
    out["specint_doubling_early"] = doubling_years(st[(st >= 1990) & (st < 2004)], sy[(st >= 1990) & (st < 2004)])
    out["specint_doubling_late"] = doubling_years(st[st >= 2010], sy[st >= 2010])
    # accelerators
    rows = list(csv.DictReader(open(DATA / "epoch_ml_hardware.csv", encoding="utf-8")))

    def f(r, k):
        try:
            return float(r[k])
        except ValueError:
            return float("nan")

    acc = []
    for r in rows:  # one flagship per generation from NVIDIA, Google, AMD and Amazon (no variants, no consumer cards)
        if not r["Release date"] or r["Hardware name"] not in FLAGSHIPS:
            continue
        y = int(r["Release date"][:4]) + (int(r["Release date"][5:7]) - 0.5) / 12
        acc.append(dict(name=r["Hardware name"], maker=r["Manufacturer"], year=y,
                        tensor=f(r, "Tensor-FP16/BF16 performance (FLOP/s)"),
                        fp32=f(r, "FP32 (single precision) performance (FLOP/s)"),
                        bw=f(r, "Memory bandwidth (byte/s)"), tdp=f(r, "TDP (W)"), price=f(r, "Release price (USD)")))
    yr = np.array([a["year"] for a in acc])
    ten = np.array([a["tensor"] for a in acc])
    bw = np.array([a["bw"] for a in acc])
    tdp = np.array([a["tdp"] for a in acc])
    fp32 = np.array([a["fp32"] for a in acc])
    ok_t = np.isfinite(ten) & (yr >= 2016)
    ok_b = np.isfinite(bw) & (yr >= 2016)
    ok_tb = ok_t & np.isfinite(bw)
    ok_e = ok_t & np.isfinite(tdp)
    out.update(acc_year=yr, acc_tensor=ten, acc_bw=bw, acc_tdp=tdp, acc_fp32=fp32,
               acc_names=np.array([a["name"] for a in acc]), acc_maker=np.array([a["maker"] for a in acc]),
               tensor_doubling=doubling_years(yr[ok_t], ten[ok_t]), bw_doubling=doubling_years(yr[ok_b], bw[ok_b]),
               ridge_doubling=doubling_years(yr[ok_tb], ten[ok_tb] / bw[ok_tb]),
               eff_doubling=doubling_years(yr[ok_e], ten[ok_e] / tdp[ok_e]),
               n_tensor=int(ok_t.sum()), n_bw=int(ok_b.sum()))
    print(f"    clock doubling {out['freq_doubling_early']:.1f} y (1985-2003), {out['freq_growth_late']:.3f}x/y after;"
          f" tensor FLOP/s doubling {out['tensor_doubling']:.2f} y, bandwidth {out['bw_doubling']:.2f} y")
    return out


ITEMS = {
    "machine": compute_machine,
    "trends": compute_trends,
    "systolic": compute_systolic,
    "warps": compute_warps,
    "formats": compute_formats,
    "hierarchy": compute_hierarchy,
    "blocking": compute_blocking,
    "matmul": compute_matmul,
    "collectives": compute_collectives,
    "matmul_mt": compute_matmul_mt,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
