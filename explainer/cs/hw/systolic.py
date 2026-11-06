"""Systolic arrays and quantization (Part 60, "Domain-Specific Hardware").

A systolic array (Kung and Leiserson, "Systolic arrays (for VLSI)", 1978; Kung, "Why systolic architectures?", IEEE
Computer 15(1), 1982) is a grid of identical cells, each talking only to its neighbours, through which data "pulses"
one cell per clock.  For C = A B on an N x N grid:

    output-stationary   cell (i, j) keeps the running sum C[i][j].  Row i of A enters the west edge delayed by i
                        cycles and moves east; column j of B enters the north edge delayed by j and moves south, so
                        A[i][k] and B[k][j] meet in cell (i, j) at cycle i + j + k: diagonal wavefronts.  The last
                        product (i = j = k = N - 1) happens at cycle 3N - 3, so a product takes 3N - 2 cycles and the
                        grid is busy N^3 / (N^2 (3N - 2)) of the time (about a third, for one product).
    weight-stationary   cell (k, j) holds the weight W[k][j] (loaded in N cycles, shifted down the columns).  Rows
                        of X stream in from the west (row k delayed by k), partial sums flow south, and Y = X W leaves
                        the south edge: M rows of X take M + 2N - 2 cycles, so a long stream keeps every cell busy.
                        This is the dataflow of Google's TPU (Jouppi et al., "In-datacenter performance analysis of a
                        tensor processing unit", ISCA 2017): a 256 x 256 grid of 8-bit multiply-accumulate cells.

Each cell is built here at gate level from Part 4's blocks (``explainer/cs/pebble/blocks.py``: a multiplier and an
adder), wired into a grid with Part 5's registers (``seq.Seq``), and stepped clock by clock by the HDL simulator
(``hdl.simulate``, or its compiled twin ``fast.Fast``: the same gates).  Operands are unsigned ``width``-bit integers
and accumulators ``acc_width`` bits (8 and 24 by default: 8 x 255^2 < 2^24, so nothing overflows for N <= 256).
``dataflow_model`` runs the same dataflow on integers (numpy) for large N, signed operands included.

Quantization: the TPU multiplies 8-bit integers, not floats.  ``quantized_matmul`` and ``quantized_classifier``
measure what symmetric per-tensor int8 quantization (scale = max |x| / 127, int32 accumulation) costs in accuracy;
``energy_area`` gives the energy and area argument from Horowitz's 45 nm table (ISSCC 2014, approximate figures) and
the TPU paper's headline numbers, beside the gate counts of our own multipliers.
"""

from __future__ import annotations

import time

import numpy as np

from explainer.cs.pebble.blocks import (array_multiplier, mux2_bus, prefix_adder, ripple_adder, tree_multiplier)
from explainer.cs.pebble.fast import Fast
from explainer.cs.pebble.hdl import Circuit, simulate
from explainer.cs.pebble.seq import Seq

WIDTH, ACC = 8, 24
KINDS = {"tree": "Dadda multiplier + Kogge-Stone adder", "array": "array multiplier + ripple-carry adder"}


def _bus(w) -> list[int]:
    return [w] if isinstance(w, int) else list(w)


# ---------------------------------------------------------------------------
# the cell
# ---------------------------------------------------------------------------
def mac_cell(width: int = WIDTH, acc_width: int = ACC, kind: str = "tree") -> Circuit:
    """acc_out = acc + a b (mod 2^acc_width): one of Part 4's multipliers feeding one of its adders."""
    if acc_width < 2 * width:
        raise ValueError("the accumulator must hold a full product")
    if kind == "tree":
        mul, add = tree_multiplier(width, "dadda"), prefix_adder(acc_width, "kogge-stone")
    elif kind == "array":
        mul, add = array_multiplier(width), ripple_adder(acc_width)
    else:
        raise ValueError(kind)
    c = Circuit(f"MAC cell ({width}-bit x {width}-bit + {acc_width}-bit, {kind})")
    a, b = _bus(c.input("a", width)), _bus(c.input("b", width))
    acc = _bus(c.input("acc", acc_width))
    p = c.embed(mul, a=a, b=b)["p"]
    zero = c.const(0)
    s = c.embed(add, a=acc, b=p + [zero] * (acc_width - len(p)), cin=zero)["s"]
    c.output("acc_out", s)
    return c.pruned()


def cell_stats(width: int = WIDTH, acc_width: int = ACC) -> dict:
    """Gate counts (by kind), size, NAND-equivalent size and depth of one cell, for both constructions, and its
    flip-flops in each dataflow (output-stationary: a, b, acc; weight-stationary: x, w, partial sum)."""
    out = {"width": width, "acc_width": acc_width, "kinds": {}}
    for kind, desc in KINDS.items():
        c = mac_cell(width, acc_width, kind)
        out["kinds"][kind] = {"description": desc, "counts": c.counts(), "gates": c.size(),
                              "nand_gates": c.to_nand().size(), "depth": c.depth()}
    out["flip_flops"] = {"output_stationary": 2 * width + acc_width, "weight_stationary": 2 * width + acc_width}
    return out


# ---------------------------------------------------------------------------
# the grids, as synchronous circuits
# ---------------------------------------------------------------------------
def os_grid(n: int, width: int = WIDTH, acc_width: int = ACC, kind: str = "tree") -> Seq:
    """Output-stationary N x N grid.  Inputs ``w{i}`` (west edge, row i) and ``n{j}`` (north edge, column j);
    registers ``a{i}_{j}`` and ``b{i}_{j}`` (the operands cell (i, j) used last cycle, passed east and south) and
    ``c{i}_{j}`` (its running sum)."""
    cell = mac_cell(width, acc_width, kind)
    s = Seq(f"{n} x {n} output-stationary systolic array")
    c = s.c
    west = [_bus(c.input(f"w{i}", width)) for i in range(n)]
    north = [_bus(c.input(f"n{j}", width)) for j in range(n)]
    A, B, C = {}, {}, {}
    for i in range(n):
        for j in range(n):
            A[i, j] = s.reg(f"a{i}_{j}", width)
            B[i, j] = s.reg(f"b{i}_{j}", width)
            C[i, j] = s.reg(f"c{i}_{j}", acc_width)
    for i in range(n):
        for j in range(n):
            a_in = west[i] if j == 0 else A[i, j - 1]
            b_in = north[j] if i == 0 else B[i - 1, j]
            s.set_next(f"a{i}_{j}", a_in)
            s.set_next(f"b{i}_{j}", b_in)
            s.set_next(f"c{i}_{j}", c.embed(cell, a=a_in, b=b_in, acc=C[i, j])["acc_out"])
    return s


def ws_grid(n: int, width: int = WIDTH, acc_width: int = ACC, kind: str = "tree") -> Seq:
    """Weight-stationary N x N grid.  Inputs ``x{k}`` (west edge, row k), ``wt{j}`` (north edge: weights, shifted
    down while ``load`` = 1); registers ``w{k}_{j}`` (the stationary weight), ``x{k}_{j}`` (the activation passed
    east) and ``p{k}_{j}`` (the partial sum passed south: the south row holds Y)."""
    cell = mac_cell(width, acc_width, kind)
    s = Seq(f"{n} x {n} weight-stationary systolic array")
    c = s.c
    west = [_bus(c.input(f"x{k}", width)) for k in range(n)]
    north = [_bus(c.input(f"wt{j}", width)) for j in range(n)]
    load = c.input("load")
    zero = c.const(0)
    W, X, P = {}, {}, {}
    for k in range(n):
        for j in range(n):
            W[k, j] = s.reg(f"w{k}_{j}", width)
            X[k, j] = s.reg(f"x{k}_{j}", width)
            P[k, j] = s.reg(f"p{k}_{j}", acc_width)
    for k in range(n):
        for j in range(n):
            x_in = west[k] if j == 0 else X[k, j - 1]
            p_in = [zero] * acc_width if k == 0 else P[k - 1, j]
            w_above = north[j] if k == 0 else W[k - 1, j]
            s.set_next(f"w{k}_{j}", mux2_bus(c, load, W[k, j], w_above))
            s.set_next(f"x{k}_{j}", x_in)
            s.set_next(f"p{k}_{j}", c.embed(cell, a=x_in, b=W[k, j], acc=p_in)["acc_out"])
    return s


class _Sim:
    """One clocked simulation, by ``hdl.simulate`` (``engine="hdl"``, through ``Seq.step``) or by the compiled
    evaluator (``engine="fast"``); both evaluate the same netlist."""

    def __init__(self, seq: Seq, engine: str, copies: int):
        self.engine = engine
        if engine == "hdl":
            self.seq = seq
            seq.reset(copies)
        elif engine == "fast":
            self.f = Fast(seq)
            self.f.reset(copies)
        else:
            raise ValueError(engine)

    def step(self, inputs: dict) -> None:
        if self.engine == "hdl":
            self.seq.step(inputs)
        else:
            self.f.eval(inputs, commit=True)

    def get(self, reg: str) -> np.ndarray:
        if self.engine == "hdl":
            return self.seq.state[reg].astype(np.int64)
        return self.f.get(reg).astype(np.int64)


def _grid(sim: _Sim, prefix: str, n: int) -> list[list[int]]:
    return [[int(sim.get(f"{prefix}{i}_{j}")[0]) for j in range(n)] for i in range(n)]


def output_stationary(n: int = 4, width: int = WIDTH, acc_width: int = ACC, trials: int = 1, seed: int = 0,
                      engine: str = "hdl", kind: str = "tree", trace: bool = True) -> dict:
    """C = A B for ``trials`` random pairs of unsigned ``width``-bit N x N matrices at once (bit-parallel copies of the
    grid), clock by clock at gate level.  ``trace`` (copy 0): per cycle, the k of the product each cell computed
    (None when idle), the operands sitting in its a and b registers, and its running sum."""
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed)
    A = rng.integers(0, 1 << width, (trials, n, n), dtype=np.int64)
    B = rng.integers(0, 1 << width, (trials, n, n), dtype=np.int64)
    s = os_grid(n, width, acc_width, kind)
    sim = _Sim(s, engine, trials)
    cycles = 3 * n - 2
    rows, busy = [], 0
    for t in range(cycles):
        ins = {}
        for i in range(n):
            k = t - i
            ins[f"w{i}"] = A[:, i, k] if 0 <= k < n else 0
            ins[f"n{i}"] = B[:, k, i] if 0 <= k < n else 0
        sim.step(ins)
        kg = [[(t - i - j) if 0 <= t - i - j < n else None for j in range(n)] for i in range(n)]
        busy += sum(x is not None for r in kg for x in r)
        if trace:
            rows.append({"t": t, "k": kg, "a": _grid(sim, "a", n), "b": _grid(sim, "b", n), "acc": _grid(sim, "c", n)})
    C = np.stack([np.stack([sim.get(f"c{i}_{j}") for j in range(n)], axis=1) for i in range(n)], axis=1)
    ref = np.einsum("tik,tkj->tij", A, B) % (1 << acc_width)
    return {"n": n, "dataflow": "output-stationary", "width": width, "acc_width": acc_width, "kind": kind,
            "engine": engine, "trials": trials, "cycles": cycles, "macs": n ** 3, "busy_cell_cycles": busy,
            "utilization": busy / (n * n * cycles), "correct": bool(np.array_equal(C, ref)),
            "gates": s.c.size(), "flip_flops": s.flip_flops, "A": A[0].tolist(), "B": B[0].tolist(),
            "C": C[0].tolist(), "trace": rows, "seconds": time.perf_counter() - t0}


def weight_stationary(n: int = 4, m: int | None = None, width: int = WIDTH, acc_width: int = ACC, trials: int = 1,
                      seed: int = 0, engine: str = "hdl", kind: str = "tree", trace: bool = True) -> dict:
    """Y = X W, X M x N (M rows streamed), W N x N (stationary), clock by clock at gate level: N load cycles, then
    M + 2N - 2 compute cycles.  ``trace`` (copy 0): per cycle, the phase, the row m of X each cell worked on (None
    when idle), and its x, w and partial-sum registers."""
    t0 = time.perf_counter()
    m = n if m is None else m
    rng = np.random.default_rng(seed)
    X = rng.integers(0, 1 << width, (trials, m, n), dtype=np.int64)
    Wt = rng.integers(0, 1 << width, (trials, n, n), dtype=np.int64)
    s = ws_grid(n, width, acc_width, kind)
    sim = _Sim(s, engine, trials)
    rows, busy = [], 0
    for t in range(n):  # load: the last row of W first, so that after n shifts row k sits in row k
        ins = {"load": 1, **{f"x{k}": 0 for k in range(n)}, **{f"wt{j}": Wt[:, n - 1 - t, j] for j in range(n)}}
        sim.step(ins)
        if trace:
            rows.append({"t": t, "phase": "load", "m": [[None] * n for _ in range(n)], "x": _grid(sim, "x", n),
                         "w": _grid(sim, "w", n), "p": _grid(sim, "p", n)})
    compute = m + 2 * n - 2
    Y = np.zeros((trials, m, n), np.int64)
    for t in range(compute):
        ins = {"load": 0, **{f"wt{j}": 0 for j in range(n)}}
        for k in range(n):
            r = t - k
            ins[f"x{k}"] = X[:, r, k] if 0 <= r < m else 0
        sim.step(ins)
        for j in range(n):
            r = t - (n - 1) - j
            if 0 <= r < m:
                Y[:, r, j] = sim.get(f"p{n - 1}_{j}")
        mg = [[(t - k - j) if 0 <= t - k - j < m else None for j in range(n)] for k in range(n)]
        busy += sum(x is not None for r_ in mg for x in r_)
        if trace:
            rows.append({"t": n + t, "phase": "compute", "m": mg, "x": _grid(sim, "x", n), "w": _grid(sim, "w", n),
                         "p": _grid(sim, "p", n)})
    loaded = all(np.array_equal(np.stack([sim.get(f"w{k}_{j}") for j in range(n)], axis=1), Wt[:, k, :])
                 for k in range(n))
    ref = np.einsum("tmk,tkj->tmj", X, Wt) % (1 << acc_width)
    return {"n": n, "m": m, "dataflow": "weight-stationary", "width": width, "acc_width": acc_width, "kind": kind,
            "engine": engine, "trials": trials, "load_cycles": n, "compute_cycles": compute, "cycles": n + compute,
            "macs": m * n * n, "busy_cell_cycles": busy, "utilization": busy / (n * n * (n + compute)),
            "compute_utilization": busy / (n * n * compute), "weights_loaded": bool(loaded),
            "correct": bool(np.array_equal(Y, ref)), "gates": s.c.size(), "flip_flops": s.flip_flops,
            "X": X[0].tolist(), "W": Wt[0].tolist(), "Y": Y[0].tolist(), "trace": rows,
            "seconds": time.perf_counter() - t0}


def gate_level(ns=(2, 4, 8), trials: int = 16, seed: int = 0) -> list[dict]:
    """Both dataflows at gate level for each N, ``trials`` random products each, against numpy (traces dropped
    except for the smallest N's output-stationary run)."""
    rows = []
    for n in ns:
        for f in (output_stationary, weight_stationary):
            r = f(n, trials=trials, seed=seed + n, trace=(n == min(ns)))
            rows.append(r)
    return rows


# ---------------------------------------------------------------------------
# the same dataflows on integers, for large N
# ---------------------------------------------------------------------------
def _edge(M: np.ndarray, t: int, axis_rows: bool) -> tuple[np.ndarray, np.ndarray]:
    """The skewed edge feed at cycle t: lane i gets M[i, t - i] (rows) or M[t - i, i] (columns), or 0."""
    n = M.shape[0] if axis_rows else M.shape[1]
    lanes = np.arange(n)
    idx = t - lanes
    lim = M.shape[1] if axis_rows else M.shape[0]
    ok = (idx >= 0) & (idx < lim)
    idc = np.clip(idx, 0, lim - 1)
    v = M[lanes, idc] if axis_rows else M[idc, lanes]
    return np.where(ok, v, 0), ok


def dataflow_model(n: int, m: int | None = None, dataflow: str = "os", A=None, B=None, seed: int = 0) -> dict:
    """The register-transfer behaviour of ``os_grid``/``ws_grid`` on integers (any sign, int64): cycles, busy cells,
    utilization, and the product checked against numpy (``result``, a numpy array, is left for callers to check or
    drop before caching).  For "os" A and B are N x N; for "ws" A is X (M x N) and B
    is W (N x N)."""
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed)
    m = n if m is None else m
    if A is None:
        A = rng.integers(-128, 128, ((n if dataflow == "os" else m), n), dtype=np.int64)
    if B is None:
        B = rng.integers(-128, 128, (n, n), dtype=np.int64)
    A, B = np.asarray(A, np.int64), np.asarray(B, np.int64)
    busy = 0
    if dataflow == "os":
        a = np.zeros((n, n), np.int64)
        b = np.zeros((n, n), np.int64)
        va = np.zeros((n, n), bool)
        vb = np.zeros((n, n), bool)
        acc = np.zeros((n, n), np.int64)
        cycles = 3 * n - 2
        for t in range(cycles):
            west, okw = _edge(A, t, True)
            north, okn = _edge(B, t, False)
            a = np.concatenate([west[:, None], a[:, :-1]], axis=1)
            va = np.concatenate([okw[:, None], va[:, :-1]], axis=1)
            b = np.concatenate([north[None, :], b[:-1, :]], axis=0)
            vb = np.concatenate([okn[None, :], vb[:-1, :]], axis=0)
            acc += a * b
            busy += int(np.count_nonzero(va & vb))
        result, ref = acc, A @ B
        load = 0
        macs = n ** 3
    elif dataflow == "ws":
        w = np.zeros((n, n), np.int64)
        for t in range(n):  # weights shift down the columns
            w = np.concatenate([B[n - 1 - t][None, :], w[:-1, :]], axis=0)
        load = n
        x = np.zeros((n, n), np.int64)
        vx = np.zeros((n, n), bool)
        p = np.zeros((n, n), np.int64)
        Y = np.zeros((m, n), np.int64)
        cycles = m + 2 * n - 2
        cols = np.arange(n)
        for t in range(cycles):
            west, okw = _edge(A, t, False)
            x = np.concatenate([west[:, None], x[:, :-1]], axis=1)
            vx = np.concatenate([okw[:, None], vx[:, :-1]], axis=1)
            p = np.concatenate([np.zeros((1, n), np.int64), p[:-1, :]], axis=0) + x * w
            busy += int(np.count_nonzero(vx))
            r = t - (n - 1) - cols
            ok = (r >= 0) & (r < m)
            Y[r[ok], cols[ok]] = p[n - 1, ok]
        result, ref = Y, A @ B
        macs = m * n * n
    else:
        raise ValueError(dataflow)
    total = cycles + load
    return {"n": n, "m": m if dataflow == "ws" else n, "dataflow": dataflow, "cycles": total, "compute_cycles": cycles,
            "load_cycles": load, "macs": macs, "busy_cell_cycles": busy, "utilization": busy / (n * n * total),
            "compute_utilization": busy / (n * n * cycles), "correct": bool(np.array_equal(result, ref)),
            "result": result, "seconds": time.perf_counter() - t0}


def scaling(ns=(16, 64, 256), stream: int = 16) -> list[dict]:
    """Cycles and utilization for large grids: one output-stationary product, and weight-stationary with M = N and
    with a long stream M = ``stream`` x N (rows of activations: a batch), against the closed forms
    N / (3N - 2), M / (M + 3N - 2) (load included) and M / (M + 2N - 2) (compute only)."""
    rows = []
    for n in ns:
        for df, m in (("os", n), ("ws", n), ("ws", stream * n)):
            r = dataflow_model(n, m, df, seed=n)
            r.pop("result")
            r["closed_form"] = n / (3 * n - 2) if df == "os" else m / (m + 3 * n - 2)
            r["closed_form_compute"] = n / (3 * n - 2) if df == "os" else m / (m + 2 * n - 2)
            rows.append(r)
    return rows


# ---------------------------------------------------------------------------
# quantization
# ---------------------------------------------------------------------------
def quantize(x: np.ndarray, bits: int = 8) -> tuple[np.ndarray, float]:
    """Symmetric per-tensor quantization: q = round(x / s), s = max |x| / (2^(bits-1) - 1), so x ~ s q."""
    qmax = (1 << (bits - 1)) - 1
    s = float(np.max(np.abs(x))) / qmax or 1.0
    q = np.clip(np.rint(x / s), -qmax, qmax).astype(np.int8 if bits <= 8 else np.int32)
    return q, s


def int8_matmul(A: np.ndarray, B: np.ndarray) -> tuple[np.ndarray, dict]:
    """A B through int8: quantize both, multiply-accumulate in int32 (as the TPU's accumulators do), rescale."""
    qa, sa = quantize(A)
    qb, sb = quantize(B)
    acc = qa.astype(np.int32) @ qb.astype(np.int32)
    return acc.astype(np.float64) * (sa * sb), {"scale_a": sa, "scale_b": sb, "acc": acc}


def _rel(x, ref) -> float:
    return float(np.linalg.norm(x - ref) / np.linalg.norm(ref))


def quantized_matmul(n: int = 256, seed: int = 0, systolic_n: int = 64) -> dict:
    """Relative (Frobenius) error of a random Gaussian product in float32, with float16-rounded inputs, and in int8,
    against float64; and the int8 product of a ``systolic_n`` slice run through the systolic dataflow model (exact)."""
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((n, n))
    B = rng.standard_normal((n, n))
    ref = A @ B
    f32 = (A.astype(np.float32) @ B.astype(np.float32)).astype(np.float64)
    f16 = (A.astype(np.float16).astype(np.float32) @ B.astype(np.float16).astype(np.float32)).astype(np.float64)
    q, info = int8_matmul(A, B)
    k = systolic_n
    qa, _ = quantize(A[:k, :k])
    qb, _ = quantize(B[:k, :k])
    sys = dataflow_model(k, k, "ws", A=qa, B=qb)
    return {"n": n, "float32_rel_error": _rel(f32, ref), "float16_inputs_rel_error": _rel(f16, ref),
            "int8_rel_error": _rel(q, ref), "scale_a": info["scale_a"], "scale_b": info["scale_b"],
            "max_abs_int32_acc": int(np.max(np.abs(info["acc"]))), "int32_headroom_bits":
            float(31 - np.log2(max(1, int(np.max(np.abs(info["acc"])))))),
            "systolic_n": k, "systolic_int8_exact": sys["correct"], "systolic_cycles": sys["cycles"]}


def quantized_classifier(classes: int = 10, dim: int = 64, train: int = 5000, test: int = 5000, sep: float = 0.3,
                         seed: int = 0) -> dict:
    """A small linear classifier (least-squares on one-hot targets, a closed form, so deterministic) on Gaussian
    clusters; then the same weights and inputs quantized to int8, scores accumulated in int32.  Accuracy of each,
    and how often the two agree."""
    rng = np.random.default_rng(seed)
    mu = rng.standard_normal((classes, dim)) * sep
    def draw(k):
        y = rng.integers(0, classes, k)
        return (mu[y] + rng.standard_normal((k, dim))).astype(np.float32), y
    Xtr, ytr = draw(train)
    Xte, yte = draw(test)
    Xb = np.hstack([Xtr, np.ones((train, 1), np.float32)])
    T = np.eye(classes, dtype=np.float32)[ytr]
    Wb = np.linalg.solve(Xb.T @ Xb + 1e-3 * np.eye(dim + 1, dtype=np.float32), Xb.T @ T).astype(np.float32)
    W, bias = Wb[:-1], Wb[-1]
    s32 = Xte @ W + bias
    p32 = np.argmax(s32, axis=1)
    qx, sx = quantize(Xte)
    qw, sw = quantize(W)
    acc = qx.astype(np.int32) @ qw.astype(np.int32)
    s8 = acc.astype(np.float32) * (sx * sw) + bias
    p8 = np.argmax(s8, axis=1)
    return {"classes": classes, "dim": dim, "train": train, "test": test,
            "float32_accuracy": float(np.mean(p32 == yte)), "int8_accuracy": float(np.mean(p8 == yte)),
            "agreement": float(np.mean(p8 == p32)), "score_rel_error": _rel(s8.astype(np.float64),
                                                                            s32.astype(np.float64))}


# TPU v1, from Jouppi et al. 2017 (Table 2 and section 2 of the paper).
TPU_V1 = {"grid": 256, "macs": 65536, "operand_bits": 8, "accumulator_bits": 32, "clock_mhz": 700,
          "peak_tops_reported": 92, "process_nm": 28, "unified_buffer_mib": 24, "dram_gb_per_s": 34,
          "source": "Jouppi et al., ISCA 2017"}


def energy_area() -> dict:
    """The argument for 8-bit integers: energy and area of 8-bit integer against 16- and 32-bit float arithmetic
    (Horowitz 2014, 45 nm, approximate), the TPU's peak recomputed from its grid and clock, its ridge point, and
    the gate counts of our own multipliers at the mantissa widths of each format (24 bits for float32, 11 for
    float16) beside 8 bits."""
    from .roofline import HOROWITZ_45NM

    E = {r["op"]: r for r in HOROWITZ_45NM}
    ratios = {
        "fp16_mult_over_int8_mult_energy": E["fp16 multiply"]["pj"] / E["int8 multiply"]["pj"],
        "fp16_mult_over_int8_mult_area": E["fp16 multiply"]["um2"] / E["int8 multiply"]["um2"],
        "fp16_add_over_int8_add_energy": E["fp16 add"]["pj"] / E["int8 add"]["pj"],
        "fp16_add_over_int8_add_area": E["fp16 add"]["um2"] / E["int8 add"]["um2"],
        "fp32_mult_over_int8_mult_energy": E["fp32 multiply"]["pj"] / E["int8 multiply"]["pj"],
        "fp32_mult_over_int8_mult_area": E["fp32 multiply"]["um2"] / E["int8 multiply"]["um2"],
        "fp32_mac_over_int8_mac_energy": (E["fp32 multiply"]["pj"] + E["fp32 add"]["pj"])
        / (E["int8 multiply"]["pj"] + E["int32 add"]["pj"]),
    }
    ours = {}
    for bits in (8, 11, 24):
        c = tree_multiplier(bits, "dadda")
        ours[bits] = {"gates": c.size(), "depth": c.depth()}
    peak = TPU_V1["macs"] * 2 * TPU_V1["clock_mhz"] * 1e6
    return {"horowitz": [r for r in HOROWITZ_45NM if r["um2"] is not None], "ratios": ratios, "tpu": TPU_V1,
            "tpu_peak_ops_computed": peak, "tpu_ridge_ops_per_byte": peak / (TPU_V1["dram_gb_per_s"] * 1e9),
            "our_multipliers": ours, "our_gate_ratio_24_over_8": ours[24]["gates"] / ours[8]["gates"],
            "note": "Horowitz's figures are approximate (45 nm, 0.9 V); the TPU paper credits this comparison for "
                    "choosing 8-bit integers.  Our gate counts are a technology-free proxy for area."}


def cell_check(width: int = WIDTH, acc_width: int = ACC, samples: int = 4096, seed: int = 0) -> dict:
    """One cell against integer arithmetic on random inputs (bit-parallel, ``hdl.simulate``)."""
    rng = np.random.default_rng(seed)
    a = rng.integers(0, 1 << width, samples)
    b = rng.integers(0, 1 << width, samples)
    acc = rng.integers(0, 1 << acc_width, samples)
    out = {}
    for kind in KINDS:
        r = simulate(mac_cell(width, acc_width, kind), {"a": a, "b": b, "acc": acc})["acc_out"].astype(np.int64)
        out[kind] = bool(np.array_equal(r, (acc + a * b) % (1 << acc_width)))
    return {"samples": samples, "correct": out}
