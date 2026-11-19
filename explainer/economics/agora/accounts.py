"""National accounts for a small economy (Agora, Part 3): one table, three ways to add it up, and the same answer.

An :class:`IOTable` records a year of an economy as an input-output table, the way statistical agencies lay it out:

* ``Z[i, j]``: what industry ``j`` bought from industry ``i`` to use up in production (intermediate inputs);
* ``final``: what each industry sold to final users, by column: households' consumption ``C``, investment ``I``,
  government ``G`` and exports ``X``;
* ``imports_used``: imported inputs each industry used up, and ``imports_final``: imported goods bought by final users
  (by the same columns);
* ``wages``, ``profits`` and ``taxes``: how each industry's value added was paid out.

From it, GDP three ways (:meth:`IOTable.gdp`):

* **output**: the sum over industries of value added, gross output less the inputs used up;
* **expenditure**: C + I + G + X - M, final uses of domestic and imported goods, less all imports;
* **income**: the wages, profits and taxes on production that the value added was paid out as.

The three agree by construction (:meth:`IOTable.check` raises if a table is inconsistent), which is the point: they
are three views of one set of transactions.  The table also gives Leontief's input-output model (1936): the
technical coefficients ``A = Z / x``, the inverse ``L = (I - A)^-1`` that says how much every industry must produce
for one more unit of final demand from any one of them (:meth:`IOTable.leontief`), and the domestic value added
embodied in each final use (:meth:`IOTable.value_added_in`), which is how exports are measured in value added.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

COLUMNS = ("C", "I", "G", "X")


@dataclass
class IOTable:
    industries: tuple
    Z: np.ndarray                      # (n, n) intermediate purchases: row sells to column
    final: dict                        # {"C": (n,), "I": (n,), "G": (n,), "X": (n,)} domestic output to final users
    imports_used: np.ndarray           # (n,) imported inputs used up by each industry
    imports_final: dict = field(default_factory=dict)   # {"C": m_C, ...} imported goods bought by final users
    wages: np.ndarray = None           # (n,) the parts of each industry's value added
    profits: np.ndarray = None
    taxes: np.ndarray = None

    def __post_init__(self):
        self.Z = np.asarray(self.Z, float)
        self.final = {k: np.asarray(self.final.get(k, np.zeros(len(self.industries))), float) for k in COLUMNS}
        self.imports_used = np.asarray(self.imports_used, float)
        self.imports_final = {k: float(self.imports_final.get(k, 0.0)) for k in COLUMNS}
        for name in ("wages", "profits", "taxes"):
            v = getattr(self, name)
            setattr(self, name, np.zeros(len(self.industries)) if v is None else np.asarray(v, float))

    # -- the accounts ----------------------------------------------------------
    def gross_output(self) -> np.ndarray:
        """Each industry's sales: to other industries plus to final users."""
        return self.Z.sum(axis=1) + sum(self.final.values())

    def inputs_used(self) -> np.ndarray:
        """Each industry's purchases of inputs it used up, domestic and imported."""
        return self.Z.sum(axis=0) + self.imports_used

    def value_added(self) -> np.ndarray:
        return self.gross_output() - self.inputs_used()

    def expenditure(self) -> dict:
        """The final uses, each including its imported part, and total imports M."""
        uses = {k: float(self.final[k].sum() + self.imports_final[k]) for k in COLUMNS}
        uses["M"] = float(self.imports_used.sum() + sum(self.imports_final.values()))
        return uses

    def income(self) -> dict:
        return {"wages": float(self.wages.sum()), "profits": float(self.profits.sum()),
                "taxes": float(self.taxes.sum())}

    def gdp(self) -> dict:
        """GDP by output, expenditure and income."""
        e = self.expenditure()
        return {"output": float(self.value_added().sum()),
                "expenditure": e["C"] + e["I"] + e["G"] + e["X"] - e["M"],
                "income": float(sum(self.income().values()))}

    def check(self, tol: float = 1e-9) -> None:
        """Raise unless the three measures agree and each industry's value added is fully paid out."""
        g = self.gdp()
        if max(g.values()) - min(g.values()) > tol * max(1.0, abs(g["output"])):
            raise ValueError(f"the three measures of GDP disagree: {g}")
        paid = self.wages + self.profits + self.taxes
        bad = np.abs(paid - self.value_added()) > tol * max(1.0, float(np.abs(paid).max()))
        if bad.any():
            raise ValueError(f"value added not fully paid out in {[self.industries[i] for i in np.flatnonzero(bad)]}")

    # -- Leontief --------------------------------------------------------------
    def coefficients(self) -> np.ndarray:
        """A[i, j]: input from industry i per unit of industry j's gross output."""
        return self.Z / self.gross_output()[None, :]

    def leontief(self) -> np.ndarray:
        """(I - A)^-1: column j is the gross output every industry must produce to deliver one more unit of j's
        product to final users."""
        n = len(self.industries)
        return np.linalg.inv(np.eye(n) - self.coefficients())

    def value_added_in(self, use: str) -> dict:
        """The domestic value added embodied in a final use (e.g. ``"X"``): v' L f, where v is value added per unit
        of output.  Compared with the gross value of that use, it says how much of it was made at home."""
        v = self.value_added() / self.gross_output()
        f = self.final[use]
        va = float(v @ self.leontief() @ f)
        return {"gross": float(f.sum()), "domestic_value_added": va, "share": va / float(f.sum())}
