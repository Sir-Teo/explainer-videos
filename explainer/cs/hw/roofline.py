"""The roofline model of this machine, and the energy of moving a word against computing on it (Part 60).

Williams, Waterman and Patterson, "Roofline: an insightful visual performance model for multicore architectures",
CACM 52(4), 2009.  A kernel that does F floating-point operations while moving Q bytes to and from DRAM has
arithmetic intensity I = F / Q; on a machine with peak P (FLOP/s) and memory bandwidth β (bytes/s) it can attain at
most

    min(P, I β)

a sloped roof (memory-bound) meeting a flat one (compute-bound) at the ridge point I = P / β.  ``machine`` measures
P (a large float64 matrix product through NumPy's BLAS, on all cores) and β (STREAM-style copy and add kernels on
arrays far larger than the last-level cache; McCalpin, "Memory bandwidth and machine balance", 1995, counting bytes
as STREAM does, without write-allocate traffic).  ``kernels`` places measured kernels on it with intensities from
their compulsory traffic: axpy, dot, matrix-vector, matrix-matrix at several sizes, a 5-point stencil, Part 52's BLAS
levels (``explainer/cs/numeric/speed.blas_levels``), and the Job in Python (integer work, intensity estimated).

``HOROWITZ_45NM``: energy (and area) per operation from M. Horowitz, "Computing's energy problem (and what we can do
about it)", ISSCC 2014, for a 45 nm process at 0.9 V.  The figures are approximate by the source's own account and
are labelled so; ``energy`` turns them into the ratio of fetching a word from DRAM to computing on it.
"""

from __future__ import annotations

import contextlib
import ctypes
import glob
import os
import time

import numpy as np
import scipy.linalg.blas as blas

from explainer.cs.numeric import speed

# Horowitz 2014, 45 nm, 0.9 V (approximate).  pJ per operation; um2 is the area of the unit (None: not in the table).
HOROWITZ_45NM = [
    {"op": "int8 add", "bits": 8, "pj": 0.03, "um2": 36},
    {"op": "int32 add", "bits": 32, "pj": 0.1, "um2": 137},
    {"op": "int8 multiply", "bits": 8, "pj": 0.2, "um2": 282},
    {"op": "int32 multiply", "bits": 32, "pj": 3.1, "um2": 3495},
    {"op": "fp16 add", "bits": 16, "pj": 0.4, "um2": 1360},
    {"op": "fp32 add", "bits": 32, "pj": 0.9, "um2": 4184},
    {"op": "fp16 multiply", "bits": 16, "pj": 1.1, "um2": 1640},
    {"op": "fp32 multiply", "bits": 32, "pj": 3.7, "um2": 7700},
    {"op": "8 KB SRAM read (64 bits)", "bits": 64, "pj": 10.0, "um2": None},
    {"op": "32 KB SRAM read (64 bits)", "bits": 64, "pj": 20.0, "um2": None},
    {"op": "1 MB SRAM read (64 bits)", "bits": 64, "pj": 100.0, "um2": None},
    {"op": "DRAM read (64 bits), low", "bits": 64, "pj": 1300.0, "um2": None},
    {"op": "DRAM read (64 bits), high", "bits": 64, "pj": 2600.0, "um2": None},
]
HOROWITZ_SOURCE = "M. Horowitz, ISSCC 2014, 45 nm at 0.9 V; approximate figures"

# The Job in Python, as integer work per byte (an estimate, not a count): classify the byte, lower-case it, update
# a word's hash or end it.  Each byte of text is read once.
JOB_OPS_PER_BYTE = 4.0


def _best(f, reps: int = 5) -> float:
    best = float("inf")
    for _ in range(reps):
        t = time.perf_counter()
        f()
        best = min(best, time.perf_counter() - t)
    return best


def attainable(intensity: float, peak: float, bandwidth: float) -> float:
    """The roofline: min(peak, intensity x bandwidth)."""
    return min(peak, intensity * bandwidth)


def _cpu() -> str:
    try:
        with open("/proc/cpuinfo") as fh:
            for line in fh:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return "unknown"


def _openblas():
    """The OpenBLAS copies bundled with NumPy and with SciPy (SciPy's daxpy uses its own), as (set, get) pairs for
    their thread counts; None if neither can be found."""
    site = os.path.join(os.path.dirname(np.__file__), "..")
    pairs = []
    for path in glob.glob(os.path.join(site, "numpy.libs", "*openblas*.so*")) + \
            glob.glob(os.path.join(site, "scipy.libs", "*openblas*.so*")):
        try:
            lib = ctypes.CDLL(path)
        except OSError:
            continue
        found = None
        for pre in ("scipy_openblas", "openblas"):
            for suf in ("64_", "_64_", ""):
                try:
                    found = getattr(lib, f"{pre}_set_num_threads{suf}"), getattr(lib, f"{pre}_get_num_threads{suf}")
                    break
                except AttributeError:
                    continue
            if found:
                break
        if found:
            pairs.append(found)
    return pairs or None


@contextlib.contextmanager
def blas_threads(n: int | None):
    """Run NumPy's and SciPy's BLAS on ``n`` threads (None: leave them alone)."""
    libs = _openblas() if n else None
    if not libs:
        yield None
        return
    old = [get() for _, get in libs]
    for setn, _ in libs:
        setn(n)
    try:
        yield n
    finally:
        for (setn, _), o in zip(libs, old):
            setn(o)


def peak(ns=(256, 512, 1024, 2048), threads: int | None = 1) -> dict:
    """Peak float64 FLOP/s: the best n x n matrix product (2 n^3 flops) through BLAS over a few sizes, on
    ``threads`` threads (one core by default: NumPy's elementwise kernels, and so the bandwidth, are one core's,
    and one core's numbers stay steady on a shared machine)."""
    rng = np.random.default_rng(0)
    rows = []
    with blas_threads(threads) as got:
        for n in ns:
            A, B = rng.standard_normal((n, n)), rng.standard_normal((n, n))
            A @ B
            t = _best(lambda: A @ B, max(3, int(2e9 / n ** 3)))
            rows.append({"n": n, "seconds": t, "gflops": 2 * n ** 3 / t / 1e9})
    best = max(rows, key=lambda r: r["gflops"])
    return {"sizes": rows, "n": best["n"], "gflops": best["gflops"], "threads": got}


def llc_bytes() -> int | None:
    """The last-level cache's size, from sysfs (None if unknown)."""
    best = None
    for f in glob.glob("/sys/devices/system/cpu/cpu0/cache/index*/size"):
        try:
            with open(f) as fh:
                v = fh.read().strip()
        except OSError:
            continue
        mult = {"K": 1 << 10, "M": 1 << 20, "G": 1 << 30}.get(v[-1], 1)
        size = int(v[:-1] if v[-1] in "KMG" else v) * mult
        best = max(best or 0, size)
    return best


def bandwidth(n: int = 1 << 26, reps: int = 5) -> dict:
    """Sustained DRAM bandwidth on float64 arrays of ``n`` elements (512 MB each by default, beyond this machine's
    last-level cache), counting bytes as STREAM does (no write-allocate traffic): copy (c = a, 16 bytes per
    element), add (c = a + b, 24), BLAS daxpy (y += s x, 24) and dot (16, reads only).  The roof is the best of
    them, as STREAM reports."""
    rng = np.random.default_rng(1)
    a = rng.standard_normal(n)
    b = rng.standard_normal(n)
    c = np.empty_like(a)
    np.copyto(c, a)
    tc = _best(lambda: np.copyto(c, a), reps)
    ta = _best(lambda: np.add(a, b, out=c), reps)
    ok = bool(np.allclose(c[:1000], a[:1000] + b[:1000]))
    tx = _best(lambda: blas.daxpy(a, c, a=1e-9), reps)
    td = _best(lambda: np.dot(a, b), reps)
    kinds = {"copy_gbs": 16 * n / tc / 1e9, "add_gbs": 24 * n / ta / 1e9, "daxpy_gbs": 24 * n / tx / 1e9,
             "dot_gbs": 16 * n / td / 1e9}
    return {"n": n, "array_mb": 8 * n / 2 ** 20, **kinds, "gbs": max(kinds.values()), "best": max(kinds, key=kinds.get),
            "add_checked": ok, "llc_bytes": llc_bytes()}


def machine(peak_ns=(256, 512, 1024, 2048), stream_n: int = 1 << 26, threads: int | None = 1) -> dict:
    p = peak(peak_ns, threads)
    with blas_threads(threads):           # daxpy and dot go through BLAS: one core, like the elementwise kernels
        bw = bandwidth(stream_n)
    P, beta = p["gflops"] * 1e9, bw["gbs"] * 1e9
    try:
        load = os.getloadavg()[0]
    except OSError:
        load = None
    return {"cpu": _cpu(), "cores": os.cpu_count(), "threads": p["threads"], "load_average": load, "peak": p,
            "bandwidth": bw, "peak_gflops": p["gflops"], "bandwidth_gbs": bw["gbs"], "ridge_flops_per_byte": P / beta}


_LLC = None


def _point(name, size, flops, nbytes, seconds, P, beta, unit="flop") -> dict:
    """One kernel on the roofline.  ``in_cache``: its whole working set fits in the last-level cache, so DRAM's
    roof does not bind it (such a point can sit above the sloped roof)."""
    global _LLC
    _LLC = _LLC if _LLC is not None else (llc_bytes() or 0)
    I = flops / nbytes
    perf = flops / seconds
    roof = attainable(I, P, beta)
    return {"kernel": name, "size": size, "flops": flops, "bytes": nbytes, "intensity": I, "seconds": seconds,
            "gflops": perf / 1e9, "roof_gflops": roof / 1e9, "fraction_of_roof": perf / roof,
            "bound": "memory" if I < P / beta else "compute", "unit": unit,
            "in_cache": bool(_LLC and nbytes <= _LLC)}


def stencil(u: np.ndarray, out: np.ndarray) -> np.ndarray:
    """One Jacobi sweep of the 5-point Laplacian: each interior point becomes the mean of its four neighbours
    (3 adds and 1 multiply: 4 flops per point)."""
    out[1:-1, 1:-1] = 0.25 * (u[:-2, 1:-1] + u[2:, 1:-1] + u[1:-1, :-2] + u[1:-1, 2:])
    return out


def job_python(tape: bytes) -> dict:
    """The Job in Python (``programs.job_words`` and a dictionary): its bytes per second."""
    from explainer.cs.pebble.programs import job_words

    def run():
        counts: dict[bytes, int] = {}
        for w in job_words(tape):
            counts[w] = counts.get(w, 0) + 1
        return counts

    t = _best(run, 3)
    return {"bytes": len(tape), "seconds": t, "bytes_per_second": len(tape) / t, "distinct": len(run())}


def kernels(m: dict | None = None, vec_n: int = 1 << 26, gemv_n: int = 8192, gemm_ns=(64, 256, 1024, 2048),
            stencil_n: int = 8192, part52_ns=(1024,), job_tape: bytes | None = None, threads: int | None = 1) -> dict:
    """Each kernel's measured GFLOP/s, intensity (flops per byte of compulsory DRAM traffic) and roof.  The Job's
    "flops" are its estimated integer operations (``JOB_OPS_PER_BYTE`` per byte, one byte moved per byte)."""
    m = m or machine(threads=threads)
    with blas_threads(threads):
        return _kernels(m, vec_n, gemv_n, gemm_ns, stencil_n, part52_ns, job_tape)


def _kernels(m, vec_n, gemv_n, gemm_ns, stencil_n, part52_ns, job_tape) -> dict:
    P, beta = m["peak_gflops"] * 1e9, m["bandwidth_gbs"] * 1e9
    rng = np.random.default_rng(2)
    pts = []
    x, y = rng.standard_normal(vec_n), rng.standard_normal(vec_n)
    t = _best(lambda: blas.daxpy(x, y, a=1e-9), 5)                        # y += a x: read x, y; write y
    pts.append(_point("axpy", vec_n, 2 * vec_n, 24 * vec_n, t, P, beta))
    t = _best(lambda: np.dot(x, y), 5)                                     # read x, y
    pts.append(_point("dot", vec_n, 2 * vec_n, 16 * vec_n, t, P, beta))
    x = y = None  # free before the next kernel
    A, v = rng.standard_normal((gemv_n, gemv_n)), rng.standard_normal(gemv_n)
    t = _best(lambda: A @ v, 5)                                            # the matrix dominates: 8 n^2 bytes
    pts.append(_point("matrix-vector", gemv_n, 2 * gemv_n ** 2, 8 * gemv_n ** 2, t, P, beta))
    del A
    for n in gemm_ns:
        A, B = rng.standard_normal((n, n)), rng.standard_normal((n, n))
        reps = max(3, int(2e9 / n ** 3))
        t = _best(lambda: A @ B, reps)                                     # read A, B; write C: 24 n^2 bytes
        pts.append(_point("matrix-matrix", n, 2 * n ** 3, 24 * n ** 2, t, P, beta))
    u = rng.standard_normal((stencil_n, stencil_n))
    out = np.zeros_like(u)
    t = _best(lambda: stencil(u, out), 3)
    pts.append(_point("5-point stencil", stencil_n, 4 * (stencil_n - 2) ** 2, 16 * stencil_n ** 2, t, P, beta))
    u = out = None
    for r in speed.blas_levels(part52_ns):                                # Part 52's own timings, placed here
        n = r["n"]
        for lvl, fl in (("axpy", 2 * n * n), ("gemv", 2 * n * n), ("gemm", 2 * n ** 3)):
            g = r[f"{lvl}_gflops"] * 1e9
            nb = fl / r[f"{lvl}_intensity"]
            pts.append(_point(f"Part 52 {lvl}", n, fl, nb, fl / g, P, beta))
    if job_tape is None:
        from videos.cs.cs6.compute import novels
        from explainer.cs.pebble.programs import job_tape as tape_of

        job_tape = tape_of(novels()[1342])
    j = job_python(job_tape)
    pts.append(_point("the Job (Python)", j["bytes"], JOB_OPS_PER_BYTE * j["bytes"], j["bytes"], j["seconds"], P,
                      beta, unit="integer op (estimated)"))
    return {"machine": m, "points": pts, "job": j, "job_ops_per_byte": JOB_OPS_PER_BYTE}


def energy() -> dict:
    """The table, and the ratios that make the argument: a 64-bit DRAM read against a float multiply and an integer
    add, and an on-chip SRAM read against the same."""
    E = {r["op"]: r["pj"] for r in HOROWITZ_45NM}
    lo, hi = E["DRAM read (64 bits), low"], E["DRAM read (64 bits), high"]
    return {"table": HOROWITZ_45NM, "source": HOROWITZ_SOURCE,
            "dram_over_fp32_mult": [lo / E["fp32 multiply"], hi / E["fp32 multiply"]],
            "dram_over_int32_add": [lo / E["int32 add"], hi / E["int32 add"]],
            "dram_over_two_fp32_mults": [lo / (2 * E["fp32 multiply"]), hi / (2 * E["fp32 multiply"])],
            "sram8k_over_int32_add": E["8 KB SRAM read (64 bits)"] / E["int32 add"],
            "sram8k_over_fp32_mult": E["8 KB SRAM read (64 bits)"] / E["fp32 multiply"],
            "note": "a 64-bit DRAM read delivers two 32-bit words; 'dram_over_two_fp32_mults' compares it with one "
                    "multiply per word delivered"}
