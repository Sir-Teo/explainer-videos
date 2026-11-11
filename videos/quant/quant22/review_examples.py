"""Named price illustrations after legacy EIA raw hashes stopped matching.

These do not restore the blocked ``oil``, ``gas`` or ``storage_theory`` items.
Public workbook bytes have independent pins; the original manifest is untouched.
The storage simulation uses the original numerical law and seed. No historical
futures strategy, return comparison, parameter search or sealed experiment runs.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import xlrd

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import exotics as EX

ROOT = Path(__file__).resolve().parents[3]
CACHE = Cache("quant22")


def public_eia(series, kind="pet", *, weekly=False):
    name = f"{series}{'w' if weekly else 'd'}.xls"
    pins = json.loads(Path(__file__).with_name("public_example_pins.json").read_text())
    pin = pins["files"][name]
    raw = (ROOT / pin["path"]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != pin["sha256"]:
        raise ValueError(f"Named public example pin changed: {name}")
    book = xlrd.open_workbook(file_contents=raw)
    sheet = book.sheet_by_index(1)
    rows = []
    for i in range(3, sheet.nrows):
        date, value = sheet.row_values(i)[:2]
        if value in ("", None):
            continue
        y, m, d, *_ = xlrd.xldate_as_tuple(date, book.datemode)
        rows.append((y * 10000 + m * 100 + d, float(value)))
    a = np.asarray(rows)
    return {"date": a[:, 0].astype(int), "value": a[:, 1]}


def original_numerical_namespace():
    """Reuse only the explicitly audited original fixed numerical definitions."""
    source = Path(__file__).with_name("compute.py").read_text()
    tree = ast.parse(source)
    names = {"_json", "_fy", "compute_gas", "compute_storage_theory"}
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == names
    public = SimpleNamespace(fred=data.fred, eia_daily=public_eia,
                             eia_weekly=lambda series: public_eia(series, weekly=True))
    ns = {"np": np, "json": json, "data": public, "EX": EX, "THROUGH": "2025-12-31"}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(Path(__file__).with_name("compute.py")), "exec"), ns)
    return ns


def oil_public_example():
    series = [public_eia(f"RCLC{i}") for i in range(1, 5)]
    dates = series[0]["date"]
    for item in series[1:]:
        dates = np.intersect1d(dates, item["date"])
    dates = dates[(dates >= 19860101) & (dates <= 20240430)]
    prices = np.stack([s["value"][np.searchsorted(s["date"], dates)] for s in series], axis=1)
    fy = lambda d: d // 10000 + (d // 100 % 100 - 1) / 12 + (d % 100 - 1) / 365
    valid = np.all(prices > 0, axis=1)
    slope = np.full(len(dates), np.nan)
    slope[valid] = np.log(prices[valid, 3] / prices[valid, 0]) / 0.25
    snapshots = {}
    for date in (20080703, 20081219, 20140620, 20160211, 20200417, 20200420, 20200421, 20220308):
        i = int(np.searchsorted(dates, date))
        assert dates[i] == date
        text = f"{date // 10000:04d}-{date // 100 % 100:02d}-{date % 100:02d}"
        snapshots[text] = {"date": date, "P": prices[i].tolist()}
    april = (dates >= 20200401) & (dates <= 20200430)
    return {"t": fy(dates)[::5].tolist(), "c1": prices[::5, 0].tolist(),
            "slope": slope[::5].tolist(), "contango_share": float(np.mean(prices[valid, 1] > prices[valid, 0])),
            "snaps": snapshots, "april": {"dates": dates[april].tolist(), "P": prices[april].tolist()},
            "scope": "Named pinned public price illustration; approximate three-month annualisation; positive-price days only for log slopes. No historical rolling strategy return calculated.",
            "valid_positive_price_days": int(valid.sum()), "excluded_nonpositive_days": int((~valid).sum())}


def gas_public_example():
    result = original_numerical_namespace()["compute_gas"]()
    result["scope"] = "Named public gas price context and original fixed Margrabe illustration; four nearest contracts do not reconstruct Amaranth's positions or P&L."
    return result


def storage_public_example():
    result = original_numerical_namespace()["compute_storage_theory"]()
    result["scope"] = "Original fixed storage law, bounded grid, quadrature and seed; separately pinned public inventory/price association. No market strategy return."
    return result


ITEMS = {"oil_public_example": oil_public_example, "gas_public_example": gas_public_example,
         "storage_public_example": storage_public_example}
CACHE.items = ITEMS

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
