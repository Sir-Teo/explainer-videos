"""The Track Record (videos/quant/SYLLABUS.md, "The Track Record and the sealed envelope"): one row per registered
strategy, scored on the sealed hold-out (1 January 2021 to the freeze date) after it was opened once for it through
:func:`explainer.quant.house.pit.open_envelope`.

Each row keeps the research-window statistics beside the hold-out's, so a reader sees what was promised and what
came: annualised return, volatility, Sharpe ratio with its standard error, maximum drawdown, and the Sharpe ratio net
of the row's stated cost model. Rows are written to ``videos/quant/data/track_record.json`` (committed) and are never
edited by hand; a part recomputes its own rows.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

from explainer.quant.house import factors as FA

ROOT = Path(__file__).resolve().parents[3]
LEDGER = Path(os.environ.get("EXPLAINER_TRACK", ROOT / "videos" / "quant" / "data" / "track_record.json"))


def _read() -> dict:
    return json.loads(LEDGER.read_text()) if LEDGER.exists() else {}


def score(r, cost_per_year: float = 0.0) -> dict:
    """A row's columns from monthly returns: ``mean``, ``vol``, ``sharpe``, ``sharpe_se``, ``maxdd``, ``n`` and the
    Sharpe ratio after subtracting ``cost_per_year`` (spread evenly over months)."""
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    s = FA.stats(r)
    net = r - cost_per_year / 12
    return {"mean": s["mean"], "vol": s["vol"], "sharpe": s["sharpe"], "sharpe_se": s["sharpe_se"],
            "maxdd": s["maxdd"], "n": s["n"], "sharpe_net": float(net.mean() / net.std(ddof=1) * np.sqrt(12)),
            "cost_per_year": float(cost_per_year)}


def record(strategy: str, part: int, research, holdout, cost_per_year: float = 0.0, note: str = "") -> dict:
    """Write (or rewrite, from the same part) the row for ``strategy``: research-window and hold-out returns, scored
    with the same cost model."""
    row = {"part": int(part), "research": score(research, cost_per_year), "holdout": score(holdout, cost_per_year),
           "note": note}
    led = _read()
    old = led.get(strategy)
    if old is not None and old["part"] != part:
        raise RuntimeError(f"{strategy} belongs to Part {old['part']}")
    led[strategy] = row
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    tmp = LEDGER.with_suffix(".tmp")
    tmp.write_text(json.dumps(dict(sorted(led.items())), indent=1) + "\n")
    tmp.replace(LEDGER)
    return row


def rows(upto_part: int | None = None) -> dict:
    """The ledger, optionally only the rows registered up to ``upto_part``."""
    led = _read()
    return {k: v for k, v in led.items() if upto_part is None or v["part"] <= upto_part}
