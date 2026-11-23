"""The generic firm (SYLLABUS §2.1, Part 3): operations in, three statements out, always reconciled.

Two tools:

* :class:`Ledger`, double entry as Pacioli printed it: every transaction is posted twice, once to each side, so the
  books balance after every entry (assets = liabilities + equity, with the year's profit inside equity);
* :func:`run`, a firm year by year from its operations (units, prices, unit costs, fixed costs, capital spending, the
  days customers take to pay and the firm takes to pay its suppliers, borrowing): the income statement, the balance
  sheet and the cash-flow statement fall out, and :func:`check` proves they agree.

No manim and no data: numpy-free arithmetic that the scenes, the lab and the tests all call.
"""

from __future__ import annotations

from dataclasses import dataclass, field

ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE = "asset", "liability", "equity", "revenue", "expense"


@dataclass
class Ledger:
    """Double-entry books.  ``kinds`` maps each account to asset, liability, equity, revenue or expense."""

    kinds: dict
    balances: dict = field(default_factory=dict)
    journal: list = field(default_factory=list)

    def post(self, debit: str, credit: str, amount: float, memo: str = "") -> None:
        """Debit one account and credit another by the same amount.  A debit raises an asset or an expense and lowers
        a liability, equity or revenue; a credit does the opposite."""
        for acct in (debit, credit):
            if acct not in self.kinds:
                raise KeyError(f"unknown account {acct!r}")
        self.balances[debit] = self.balances.get(debit, 0.0) + self._sign(debit) * amount
        self.balances[credit] = self.balances.get(credit, 0.0) - self._sign(credit) * amount
        self.journal.append((debit, credit, amount, memo))

    def _sign(self, acct: str) -> int:
        return 1 if self.kinds[acct] in (ASSET, EXPENSE) else -1

    def total(self, kind: str) -> float:
        return sum(v for a, v in self.balances.items() if self.kinds[a] == kind)

    def profit(self) -> float:
        return self.total(REVENUE) - self.total(EXPENSE)

    def balanced(self, tol: float = 1e-9) -> bool:
        """Assets = liabilities + equity + (revenue - expenses): true after every post, by construction."""
        return abs(self.total(ASSET) - self.total(LIABILITY) - self.total(EQUITY) - self.profit()) < tol


@dataclass
class Year:
    """One year of a firm's operations.  Money in any unit (dollars, thousands); days out of 365."""

    units: float
    price: float
    unit_cost: float            # materials and other costs that vary with each unit
    fixed_costs: float          # wages, rent, selling and overheads for the year, paid in cash and expensed
    capex: float = 0.0          # spent on equipment this year
    life: float = 10.0          # years over which this year's capex is depreciated, straight line
    receivable_days: float = 0.0
    inventory_days: float = 0.0
    payable_days: float = 0.0
    tax_rate: float = 0.21
    interest_rate: float = 0.06
    borrow: float = 0.0
    repay: float = 0.0
    equity_in: float = 0.0
    dividends: float = 0.0


@dataclass
class Statements:
    income: dict
    balance: dict
    cash: dict


def run(years: list[Year], cash0: float = 0.0, equity0: float | None = None) -> list[Statements]:
    """The three statements for each year.  The firm starts with ``cash0`` of cash and (by default) the same amount of
    equity; depreciation starts in the year of the spending; a year's borrowing and repayment happen at its start, so
    interest is charged on the debt outstanding after them."""
    if equity0 is None:
        equity0 = cash0
    cash, rec, inv, ppe, pay, debt, eq = cash0, 0.0, 0.0, 0.0, 0.0, 0.0, equity0
    vintages: list[tuple[float, float]] = []  # (amount, life)
    out = []
    for y in years:
        vintages.append((y.capex, y.life))
        dep = 0.0
        for k, (amt, life) in enumerate(vintages):
            age = len(vintages) - 1 - k
            if age < life:
                dep += amt / life
        revenue = y.units * y.price
        cogs = y.units * y.unit_cost
        gross = revenue - cogs
        ebit = gross - y.fixed_costs - dep
        debt += y.borrow - y.repay  # borrowing and repayment at the start of the year
        interest = y.interest_rate * debt
        pretax = ebit - interest
        tax = max(0.0, y.tax_rate * pretax)
        net = pretax - tax
        rec1, inv1, pay1 = revenue * y.receivable_days / 365, cogs * y.inventory_days / 365, cogs * y.payable_days / 365
        cfo = net + dep - (rec1 - rec) - (inv1 - inv) + (pay1 - pay)
        cfi = -y.capex
        cff = y.borrow - y.repay + y.equity_in - y.dividends
        cash += cfo + cfi + cff
        rec, inv, pay = rec1, inv1, pay1
        ppe += y.capex - dep
        eq += net + y.equity_in - y.dividends
        out.append(Statements(
            income=dict(revenue=revenue, cogs=cogs, gross=gross, fixed=y.fixed_costs, depreciation=dep, ebit=ebit,
                        interest=interest, pretax=pretax, tax=tax, net=net),
            balance=dict(cash=cash, receivables=rec, inventory=inv, ppe=ppe, payables=pay, debt=debt, equity=eq),
            cash=dict(operating=cfo, investing=cfi, financing=cff, free=cfo + cfi)))
    return out


def check(stmts: list[Statements], cash0: float = 0.0, equity0: float | None = None, tol: float = 1e-6) -> None:
    """Raise if the statements disagree: the balance sheet must balance, cash must move by the three cash flows, and
    equity by profit plus new equity less dividends."""
    if equity0 is None:
        equity0 = cash0
    prev_cash, prev_eq = cash0, equity0
    for k, s in enumerate(stmts):
        b = s.balance
        assets = b["cash"] + b["receivables"] + b["inventory"] + b["ppe"]
        claims = b["payables"] + b["debt"] + b["equity"]
        if abs(assets - claims) > tol * max(1.0, abs(assets)):
            raise AssertionError(f"year {k}: assets {assets} != liabilities and equity {claims}")
        flow = s.cash["operating"] + s.cash["investing"] + s.cash["financing"]
        if abs(b["cash"] - prev_cash - flow) > tol * max(1.0, abs(flow)):
            raise AssertionError(f"year {k}: cash moved {b['cash'] - prev_cash}, the cash flows say {flow}")
        prev_cash = b["cash"]
        prev_eq = b["equity"]
    return None


def ratios(s: Statements, tax_rate: float = 0.21) -> dict:
    """The ratios that travel, from one year's statements (end-of-year balances)."""
    i, b = s.income, s.balance
    assets = b["cash"] + b["receivables"] + b["inventory"] + b["ppe"]
    invested = b["debt"] + b["equity"] - b["cash"]
    return dict(gross_margin=i["gross"] / i["revenue"], operating_margin=i["ebit"] / i["revenue"],
                net_margin=i["net"] / i["revenue"], turnover=i["revenue"] / assets, leverage=assets / b["equity"],
                roe=i["net"] / b["equity"], roa=i["net"] / assets,
                roic=i["ebit"] * (1 - tax_rate) / invested if invested > 0 else float("nan"))


def dupont(net_margin: float, turnover: float, leverage: float) -> float:
    """Return on equity = profit per dollar of sales x sales per dollar of assets x assets per dollar of equity."""
    return net_margin * turnover * leverage


def cash_cycle(inventory_days: float, receivable_days: float, payable_days: float) -> float:
    """Days between paying suppliers and being paid by customers; negative when customers pay first."""
    return inventory_days + receivable_days - payable_days
