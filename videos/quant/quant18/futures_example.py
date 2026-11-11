"""Correct the illustrative delivery grade using already cached synthetic prices.

The protected original builder includes 6.5--10y notes. CBOT submission
25-099, Exhibit A, specifies 6.5--<8y for December 2025 (quarter rounding).
This named derived illustration neither edits that cache nor fetches quotes.
"""
from __future__ import annotations

import numpy as np


def delivery_example(source: dict) -> dict:
    notes = source["notes"]
    selected = [i for i, n in enumerate(notes)
                if 78 <= 3 * ((12 * n["years"] + n["months"]) // 3) < 96]
    assert selected, "No notes satisfy the cited historical delivery grade"
    factors = np.array([n["cf_factor"] for n in notes], float)
    table = []
    for row in source["table"]:
        # The original cache retains basis=P-F*CF, so recover precisely the same
        # synthetic clean prices before restricting the eligible set.
        prices = (np.asarray(row["basis"], float) + row["F"] * factors)[selected]
        ratios = prices / factors[selected]
        k = int(np.argmin(ratios))
        forward = float(ratios[k])
        table.append({"shift": row["shift"], "y10": row["y10"], "F": forward,
                      "ctd": k, "basis": (prices - forward * factors[selected]).tolist()})
    base = next(r for r in table if r["shift"] == 0)
    return {"notes": [notes[i] for i in selected], "table": table,
            "shifts": source["shifts"], "base_ctd": notes[selected[base["ctd"]]]["cusip"],
            "base_F": base["F"],
            "switch": [table[i]["shift"] for i in range(1, len(table))
                       if table[i]["ctd"] != table[i - 1]["ctd"]],
            "scope": "named grade-corrected, carry-free synthetic illustration; not exchange quotes",
            "source_note_indices": selected,
            "grade_source": "https://www.cmegroup.com/content/dam/cmegroup/market-regulation/rule-filings/2025/2/25-099.pdf"}
