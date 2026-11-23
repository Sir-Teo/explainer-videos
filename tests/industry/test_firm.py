"""The generic firm's books reconcile for any operations, and double entry always balances."""

import random

import pytest

from explainer.industry.works import firm


def test_ledger_balances_after_every_post():
    L = firm.Ledger({"cash": "asset", "oven": "asset", "flour": "asset", "owed by cafe": "asset",
                     "loan": "liability", "owed to miller": "liability", "owner": "equity",
                     "sales": "revenue", "flour used": "expense", "wages": "expense"})
    L.post("cash", "owner", 40_000, "the owner puts in savings")
    L.post("cash", "loan", 20_000, "a bank loan")
    L.post("oven", "cash", 45_000, "an oven")
    L.post("flour", "owed to miller", 3_000, "flour on credit")
    L.post("cash", "sales", 6_000, "bread sold for cash")
    L.post("owed by cafe", "sales", 3_000, "bread sold on credit")
    L.post("flour used", "flour", 3_000, "the flour baked")
    L.post("wages", "cash", 4_000, "the baker's wages")
    assert L.balanced()
    assert L.profit() == pytest.approx(2_000)
    assert L.total("asset") == pytest.approx(40_000 + 20_000 + 3_000 + 2_000)  # money in: owner, bank, miller, profit
    with pytest.raises(KeyError):
        L.post("cash", "nowhere", 1)


def test_statements_reconcile_for_random_firms():
    rng = random.Random(3)
    for _ in range(200):
        years = [firm.Year(units=rng.uniform(0, 5e4), price=rng.uniform(1, 20), unit_cost=rng.uniform(0.5, 15),
                           fixed_costs=rng.uniform(0, 1e5), capex=rng.uniform(0, 2e5), life=rng.choice([3, 5, 10]),
                           receivable_days=rng.uniform(0, 90), inventory_days=rng.uniform(0, 90),
                           payable_days=rng.uniform(0, 90), borrow=rng.uniform(0, 1e5), repay=rng.uniform(0, 5e4),
                           equity_in=rng.uniform(0, 5e4), dividends=rng.uniform(0, 2e4)) for _ in range(6)]
        s = firm.run(years, cash0=5e4)
        firm.check(s, cash0=5e4)


def test_growing_too_fast_runs_out_of_cash():
    # profitable every year, but customers take 60 days and growth needs stock and ovens: cash goes negative
    years = [firm.Year(units=10_000 * 1.6 ** k, price=5, unit_cost=2, fixed_costs=10_000, capex=30_000 * 1.6 ** k,
                       life=8, receivable_days=60, inventory_days=45, payable_days=10) for k in range(5)]
    s = firm.run(years, cash0=30_000)
    firm.check(s, cash0=30_000)
    assert all(x.income["net"] > 0 for x in s)
    assert min(x.balance["cash"] for x in s) < 0


def test_dupont_and_cash_cycle():
    assert firm.dupont(0.03, 3.4, 2.5) == pytest.approx(0.255)
    assert firm.cash_cycle(27, 4, 31) == pytest.approx(0)
    s = firm.run([firm.Year(units=1000, price=10, unit_cost=6, fixed_costs=1000, capex=5000, life=5)], cash0=10_000)
    r = firm.ratios(s[0])
    assert r["roe"] == pytest.approx(r["net_margin"] * r["turnover"] * r["leverage"])
