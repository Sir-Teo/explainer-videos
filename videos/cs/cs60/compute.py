"""Precompute everything numerical in Part 60 of *Computer Science, Built* ("Domain-Specific Hardware").

    python -m videos.cs.cs60.compute              # everything missing
    python -m videos.cs.cs60.compute --force job  # one item again

Results are cached in ``.cache/cs60/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/hw/`` (systolic, roofline, accel); tests in tests/test_cs60_hw.py.

Items:
    cells       one multiply-accumulate cell at gate level (Dadda + Kogge-Stone, and array + ripple), checked
    wave        a 4 x 4 output-stationary grid, cycle by cycle (the diagonal wave), and a weight-stationary one
    gates       both dataflows at gate level for N = 2, 4, 8, verified against integer products
    scaling     cycles and utilization at N = 16, 64, 256 against the closed forms
    quant       float32, float16 and int8 products against float64; an int8 classifier against float32
    energy      Horowitz's energy and area per operation, the TPU's peak and ridge, our multipliers' sizes
    roofline    this machine measured: peak, bandwidth, ridge, and each kernel as a point
    accel       the word-counting unit: stages, gates, depth, clock, and a paragraph run cycle by cycle
    sweep       table size against lost words on the thirty novels
    job         ledger row 21: the thirty novels through the unit, with 1, 4, 16 and 64 lanes
"""

from __future__ import annotations

import json

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("cs60")
load = CACHE.load


def _j(x):
    """Make an instrument's result JSON-safe: numpy arrays to lists, numpy scalars to Python numbers."""
    if isinstance(x, dict):
        return {str(k): _j(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_j(v) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    if isinstance(x, bytes):
        return x.decode("latin-1")
    return x


def _S():
    from explainer.cs.hw import systolic
    return systolic


def _R():
    from explainer.cs.hw import roofline
    return roofline


def _A():
    from explainer.cs.hw import accel
    return accel


def compute_cells() -> dict:
    S = _S()
    return _j({**S.cell_stats(), "check": S.cell_check()})


def compute_wave() -> dict:
    S = _S()
    # 4-bit operands so every number on screen is a single digit or two
    os_ = S.output_stationary(n=4, width=4, acc_width=12, trials=1, seed=1, trace=True)
    ws = S.weight_stationary(n=4, m=6, width=4, acc_width=12, trials=1, seed=1, trace=True)
    return _j({"os": os_, "ws": ws})


def compute_gates() -> dict:
    rows = _S().gate_level()
    for r in rows:
        for k in ("A", "B", "C", "X", "W", "Y", "trace"):
            r.pop(k, None)
    return _j({"rows": rows})


def compute_scaling() -> dict:
    return _j({"rows": _S().scaling()})


def compute_quant() -> dict:
    S = _S()
    return _j({"matmul": S.quantized_matmul(), "classifier": S.quantized_classifier()})


def compute_energy() -> dict:
    return _j({**_S().energy_area(), "horowitz": _R().energy()})


def compute_roofline() -> dict:
    return _j(_R().kernels())


def compute_accel() -> dict:
    A = _A()
    tape = A.short_text()
    r = A.run(tape, lanes=8, trace_cycles=48)
    return _j({"timing": A.timing(), "timing_novels": A.timing(A.NOVEL_INDEX_BITS), "text": tape, "run": r})


def compute_sweep() -> dict:
    return _j({"rows": _A().table_sweep()})


def compute_job() -> dict:
    A = _A()
    job = A.job_on_novels()
    row = A.ledger_row(job)
    led = A.ledger_with_row(row)
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(_j(led), indent=1))
    return _j({"job": job, "row": row, "ledger": led})


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
