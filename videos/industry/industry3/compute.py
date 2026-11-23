"""Every number in Part 3 of *Industry, Built* ("The Accounts"), from the Register and the Filing Room.

    python -m videos.industry.industry3.compute        # prints the film's numbers; writes .cache/industry3/computed.json

Items:
    six         Costco, Microsoft, JPMorgan Chase, NextEra Energy, Delta and Eli Lilly: their latest annual statements
                and the ratios that travel (margins, turns, leverage, return on equity and on capital, capital spending
                and research per dollar of sales)
    cards       the matching game: the six as anonymous cards, in the film's order
    dollar      a dollar of revenue down five income statements
    balance     what each owns and who paid for it, per dollar of assets
    bakery      the model bakery's first entries, double entry, and its year (explainer.industry.works.firm)
    growth      the bakery that grows too fast: profitable every year, out of cash in the second
    cash        profit against cash: Microsoft's fiscal 2026 and the start of fiscal 2027, NextEra's 2025
    capex       Microsoft's capital spending and operating cash by fiscal year (the intermission)
    costco      paid before it pays: Costco's days of stock and of payables, its fees per member
    delta       the airline per seat mile: revenue, cost, fuel, labour, American Express
    enron       revenue, profit and operating cash, 1998-2000, the restatement, the bankruptcy
"""

from __future__ import annotations

import functools
import json
from pathlib import Path

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from explainer.industry.works import firm

OUT = Path(__file__).resolve().parents[3] / ".cache" / "industry3"
TAX = 0.21  # the statutory federal rate, used for one comparable after-tax operating return

NAMES = {"cost": "Costco", "msft": "Microsoft", "jpm": "JPMorgan Chase", "nee": "NextEra Energy", "dal": "Delta",
         "lly": "Eli Lilly"}
KIND = {"cost": "a warehouse grocer", "msft": "a software company", "jpm": "a bank", "nee": "an electric utility",
        "dal": "an airline", "lly": "a drug maker"}
YEAR = {"cost": "fiscal 2026 (to August 2026)", "msft": "fiscal 2026 (to June 2026)", "jpm": "2025", "nee": "2025",
        "dal": "2025", "lly": "2025"}
ORDER = ["nee", "cost", "lly", "jpm", "dal", "msft"]  # the cards A-F


def _company(k: str) -> dict:
    """One company's figures from the Register, with the gaps a bank's or a utility's statements leave."""
    if k == "cost":
        d = dict(rev=get("cost.rev"), oi=get("cost.oi"), ni=get("cost.ni"), assets=get("cost.assets"),
                 equity=get("cost.equity"), capex=get("cost.capex"), rd=0.0, gross=get("cost.rev") - get("cost.cogs"),
                 ocf=get("cost.ocf"), debt=5.713 + 0.0)
    elif k == "msft":
        d = dict(rev=get("msft.rev"), oi=get("msft.oi"), ni=get("msft.ni"), assets=get("msft.assets"),
                 equity=get("msft.equity"), capex=get("msft.capex"), rd=get("msft.rd"),
                 gross=get("msft.rev") - get("msft.cogs"), ocf=get("msft.ocf"), debt=40.294)
    elif k == "jpm":
        d = dict(rev=get("jpm.rev"), oi=get("jpm.pretax"), ni=get("jpm.ni"), assets=get("jpm.assets"),
                 equity=get("jpm.equity"), capex=0.0, rd=0.0, gross=None, ocf=None, debt=None)
    elif k == "nee":
        d = dict(rev=get("nee.rev"), oi=get("nee.oi"), ni=get("nee.ni"), assets=get("nee.assets"),
                 equity=get("nee.equity"), capex=get("nee.capex_fpl") + get("nee.capex_neer"), rd=0.0, gross=None,
                 ocf=get("nee.ocf"), debt=get("nee.debt"))
    elif k == "dal":
        d = dict(rev=get("dal.rev"), oi=get("dal.oi"), ni=get("dal.ni"), assets=get("dal.assets"),
                 equity=get("dal.equity"), capex=get("dal.capex"), rd=0.0, gross=None, ocf=get("dal.ocf"),
                 debt=13.308)
    else:  # Lilly reports income before tax, not an operating line: add back its non-operating items
        d = dict(rev=get("lly.rev"), oi=get("lly.pretax") - get("lly.nonop"), ni=get("lly.ni"),
                 assets=get("lly.assets"), equity=get("lly.equity"), capex=get("lly.capex"), rd=get("lly.rd"),
                 gross=get("lly.rev") - get("lly.cogs"), ocf=get("lly.ocf"), debt=40.868)
    d["name"], d["kind"], d["year"] = NAMES[k], KIND[k], YEAR[k]
    d["op_margin"] = d["oi"] / d["rev"]
    d["net_margin"] = d["ni"] / d["rev"]
    d["turnover"] = d["rev"] / d["assets"]
    d["leverage"] = d["assets"] / d["equity"]
    d["roe"] = firm.dupont(d["net_margin"], d["turnover"], d["leverage"])
    d["roa"] = d["ni"] / d["assets"]
    d["capex_sales"] = d["capex"] / d["rev"]
    d["rd_sales"] = d["rd"] / d["rev"]
    d["gross_margin"] = d["gross"] / d["rev"] if d["gross"] is not None else None
    d["roic"] = d["oi"] * (1 - TAX) / (d["equity"] + d["debt"]) if d["debt"] is not None else None
    return d


@functools.lru_cache(maxsize=None)
def results() -> dict:
    R = {}
    six = {k: _company(k) for k in NAMES}
    R["six"] = six
    R["cards"] = [dict(letter=chr(65 + i), key=k, op_margin=six[k]["op_margin"], turnover=six[k]["turnover"],
                       leverage=six[k]["leverage"], rd_sales=six[k]["rd_sales"], capex_sales=six[k]["capex_sales"])
                  for i, k in enumerate(ORDER)]

    # --- a dollar of revenue down five income statements ----------------------------------------------------------
    c, m, dl, ly, ne, jp = (get("cost.rev"), get("msft.rev"), get("dal.rev"), get("lly.rev"), get("nee.rev"),
                            get("jpm.rev"))
    R["dollar"] = {
        "cost": [("Merchandise", get("cost.cogs") / c), ("Stores, staff, overheads", get("cost.sga") / c),
                 ("Operating profit", get("cost.oi") / c)],
        "msft": [("Cost of revenue", get("msft.cogs") / m), ("Research", get("msft.rd") / m),
                 ("Selling and admin", (m - get("msft.cogs") - get("msft.rd") - get("msft.oi")) / m),
                 ("Operating profit", get("msft.oi") / m)],
        "dal": [("Labour", get("dal.labor") / dl), ("Fuel", get("dal.fuel") / dl),
                ("Everything else", (dl - get("dal.labor") - get("dal.fuel") - get("dal.oi")) / dl),
                ("Operating profit", get("dal.oi") / dl)],
        "lly": [("Making the medicines", get("lly.cogs") / ly), ("Research", get("lly.rd") / ly),
                ("Selling and admin", get("lly.sga") / ly),
                ("Other charges", (ly - get("lly.cogs") - get("lly.rd") - get("lly.sga") - six["lly"]["oi"]) / ly),
                ("Operating profit", six["lly"]["oi"] / ly)],
        "nee": [("Fuel and power bought", 4.944 / ne), ("Running the plants", 5.399 / ne),
                ("Depreciation", 6.580 / ne), ("Taxes and other", (ne - 4.944 - 5.399 - 6.580 - get("nee.oi")) / ne),
                ("Operating profit", get("nee.oi") / ne)],
        "jpm": [("Staff and overheads", get("jpm.opex") / jp), ("Loans gone bad (provision)", get("jpm.provision") / jp),
                ("Tax", (get("jpm.pretax") - get("jpm.ni")) / jp), ("Net income", get("jpm.ni") / jp)],
    }
    for k, items in R["dollar"].items():
        assert abs(sum(v for _, v in items) - 1) < 1e-9, k

    # --- balance sheets per dollar of assets ------------------------------------------------------------------------
    A = {k: six[k]["assets"] for k in six}
    R["balance"] = {
        "jpm": dict(owns=[("Loans", get("jpm.loans")), ("Everything else", A["jpm"] - get("jpm.loans"))],
                    owes=[("Deposits", get("jpm.deposits")), ("Other borrowing", A["jpm"] - get("jpm.deposits") -
                                                                  get("jpm.equity")), ("Owners", get("jpm.equity"))]),
        "nee": dict(owns=[("Power plants and wires", get("nee.ppe")), ("Everything else", A["nee"] - get("nee.ppe"))],
                    owes=[("Long-term debt", get("nee.debt")), ("Other", A["nee"] - get("nee.debt") -
                                                                get("nee.equity")), ("Owners", get("nee.equity"))]),
        "cost": dict(owns=[("Stock on the shelves", get("cost.inventory")), ("Warehouses", get("cost.ppe")),
                           ("Cash", get("cost.cash")), ("Everything else", A["cost"] - get("cost.inventory") -
                                                        get("cost.ppe") - get("cost.cash"))],
                     owes=[("Owed to suppliers", get("cost.payables")), ("Other", A["cost"] - get("cost.payables") -
                                                                         get("cost.equity")),
                           ("Owners", get("cost.equity"))]),
        "dal": dict(owns=[("Aircraft and property", get("dal.ppe")), ("Everything else", A["dal"] - get("dal.ppe"))],
                    owes=[("Tickets and miles sold, not yet used", get("dal.atl") + get("dal.loyalty")),
                          ("Other", A["dal"] - get("dal.atl") - get("dal.loyalty") - get("dal.equity")),
                          ("Owners", get("dal.equity"))]),
        "msft": dict(owns=[("Data centres and property", get("msft.ppe")), ("Goodwill", get("msft.goodwill")),
                           ("Everything else", A["msft"] - get("msft.ppe") - get("msft.goodwill"))],
                     owes=[("Paid in advance by customers", get("msft.unearned")),
                           ("Other", A["msft"] - get("msft.unearned") - get("msft.equity")),
                           ("Owners", get("msft.equity"))]),
    }

    # --- the bakery: double entry, then its first year -------------------------------------------------------------
    kinds = {"Cash": firm.ASSET, "Oven": firm.ASSET, "Flour": firm.ASSET, "Owed by the cafe": firm.ASSET,
             "Bank loan": firm.LIABILITY, "Owed to the miller": firm.LIABILITY, "Owner's money": firm.EQUITY,
             "Sales": firm.REVENUE, "Flour used": firm.EXPENSE, "Wages": firm.EXPENSE}
    L = firm.Ledger(kinds)
    entries = [("Cash", "Owner's money", 40_000, "The owner puts in her savings"),
               ("Cash", "Bank loan", 20_000, "The bank lends"),
               ("Oven", "Cash", 45_000, "She buys an oven"),
               ("Flour", "Owed to the miller", 3_000, "Flour, on 30 days' credit"),
               ("Cash", "Sales", 6_000, "Bread sold for cash"),
               ("Owed by the cafe", "Sales", 3_000, "Bread sold to a cafe, on credit"),
               ("Flour used", "Flour", 3_000, "The flour baked into that bread"),
               ("Wages", "Cash", 4_000, "The baker's wages")]
    books = []
    for dr, cr, amt, memo in entries:
        L.post(dr, cr, amt, memo)
        assert L.balanced()
        books.append(dict(debit=dr, credit=cr, amount=amt, memo=memo, balances=dict(L.balances),
                          assets=L.total(firm.ASSET), liabilities=L.total(firm.LIABILITY),
                          equity=L.total(firm.EQUITY) + L.profit()))
    R["bakery"] = dict(entries=books, profit=L.profit(), kinds=kinds)

    # a year: 60,000 loaves at $3.60, flour and fillings $1.30 a loaf, staff (the owner's pay included) and rent
    # $115,000, the $45,000 oven over 10
    # years, customers (cafes) pay in 20 days on average, stock 10 days, the miller paid in 30
    year = firm.Year(units=60_000, price=3.6, unit_cost=1.3, fixed_costs=115_000, capex=45_000, life=10,
                     receivable_days=20, inventory_days=10, payable_days=30, tax_rate=0.21, interest_rate=0.07,
                     borrow=20_000)
    s = firm.run([year], cash0=40_000)
    firm.check(s, cash0=40_000)
    R["bakery_year"] = dict(income=s[0].income, balance=s[0].balance, cash=s[0].cash, ratios=firm.ratios(s[0]))

    # --- growing too fast: the same bakery opening shops, sales up 60% a year, cafes paying in 60 days ---------------
    yrs = [firm.Year(units=60_000 * 1.6 ** k, price=3.6, unit_cost=1.3, fixed_costs=115_000 * 1.6 ** k,
                     capex=45_000 if k == 0 else 30_000 * 1.6 ** k, life=10, receivable_days=60, inventory_days=10, payable_days=30,
                     interest_rate=0.07, borrow=20_000 if k == 0 else 0) for k in range(5)]
    g = firm.run(yrs, cash0=40_000)
    firm.check(g, cash0=40_000)
    R["growth"] = [dict(year=k + 1, sales=x.income["revenue"], profit=x.income["net"], cash=x.balance["cash"],
                        cfo=x.cash["operating"], capex=-x.cash["investing"]) for k, x in enumerate(g)]
    assert all(x["profit"] > 0 for x in R["growth"]) and min(x["cash"] for x in R["growth"]) < 0

    # --- profit against cash --------------------------------------------------------------------------------------
    R["cash"] = dict(
        msft=dict(ni=get("msft.ni"), ocf=get("msft.ocf"), capex=get("msft.capex"), fcf=get("msft.ocf") -
                  get("msft.capex"), openai=get("msft.openai"), sbc=get("msft.sbc"),
                  fcf25=get("msft.ocf25") - get("msft.capex25"),
                  q1=dict(ocf=get("msft.ocf_q1fy27"), capex=get("msft.capex_q1fy27"),
                          fcf=get("msft.ocf_q1fy27") - get("msft.capex_q1fy27"), oi=get("msft.oi_q1fy27")),
                  q1_prev=dict(ocf=get("msft.ocf_q1fy26"), capex=get("msft.capex_q1fy26"),
                               fcf=get("msft.ocf_q1fy26") - get("msft.capex_q1fy26"))),
        nee=dict(ni=get("nee.ni"), ocf=get("nee.ocf"), capex=get("nee.capex_fpl") + get("nee.capex_neer"),
                 fcf=get("nee.ocf") - get("nee.capex_fpl") - get("nee.capex_neer")),
    )
    sec = [r for r in read("sec_annual") if r["ticker"] == "MSFT" and r["year_end"] >= "2010"]
    R["capex"] = [dict(fy=int(r["year_end"][:4]), capex=r["capex"], ocf=r["operating_cash"], oi=r["operating_income"])
                  for r in sec]

    # --- Costco: paid before it pays ----------------------------------------------------------------------------
    cogs = get("cost.cogs")
    inv_days, pay_days = 365 * get("cost.inventory") / cogs, 365 * get("cost.payables") / cogs
    members = (get("cost.members") + 81.0) / 2  # average of the year's opening and closing paid members (millions)
    R["costco"] = dict(inventory_days=inv_days, payable_days=pay_days, cycle=firm.cash_cycle(inv_days, 0, pay_days),
                       fees=get("cost.fees"), fee_share=get("cost.fees") / get("cost.oi"),
                       per_member=dict(spend=1e3 * get("cost.rev") / members, fee=1e3 * get("cost.fees") / members,
                                       oi=1e3 * get("cost.oi") / members),
                       gross_margin_ex_fees=(get("cost.rev") - get("cost.fees") - cogs) / (get("cost.rev") -
                                                                                         get("cost.fees")))

    # --- Delta per available seat mile -----------------------------------------------------------------------------
    asm = get("dal.asm") * 1e6
    per = lambda x: 100 * x * 1e9 / asm  # noqa: E731  (cents per seat mile)
    nyla = 2475  # miles, New York (JFK) to Los Angeles (LAX), great circle as flown, approximately
    R["delta"] = dict(trasm=get("dal.trasm"), casm=get("dal.casm"), margin=get("dal.trasm") - get("dal.casm"),
                      fuel=per(get("dal.fuel")), labor=per(get("dal.labor")), amex=per(get("dal.amex")),
                      check=(get("dal.trasm") - get("dal.casm")) * asm / 100 / 1e9, miles=nyla,
                      seat=dict(revenue=nyla * get("dal.trasm") / 100, cost=nyla * get("dal.casm") / 100,
                                fuel=nyla * per(get("dal.fuel")) / 100, labor=nyla * per(get("dal.labor")) / 100,
                                amex=nyla * per(get("dal.amex")) / 100))
    assert abs(R["delta"]["check"] - get("dal.oi")) < 0.1  # the seat-mile margin rebuilds the operating income

    # --- Enron ----------------------------------------------------------------------------------------------------
    R["enron"] = dict(rev={1998: 31.260, 1999: 40.112, 2000: get("enron.rev.2000")},
                      ni={1998: 0.703, 1999: 0.893, 2000: get("enron.ni.2000")},
                      cfo={1998: 1.640, 1999: get("enron.cfo.1999"), 2000: get("enron.cfo.2000")},
                      cfo_9m_2000=0.1, restate=get("enron.restate"), prepays=get("levin.prepays"))
    return R


def main():
    R = results()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "computed.json").write_text(json.dumps(R, indent=1, default=float))
    print(f"{'':16}{'op margin':>10}{'turnover':>10}{'leverage':>10}{'ROE':>8}{'ROIC':>8}{'capex/s':>9}{'R&D/s':>8}")
    for k, d in R["six"].items():
        roic = f"{100 * d['roic']:7.0f}%" if d["roic"] is not None else "      —"
        print(f"{d['name']:<16}{100 * d['op_margin']:9.1f}%{d['turnover']:10.2f}{d['leverage']:10.1f}"
              f"{100 * d['roe']:7.0f}%{roic}{100 * d['capex_sales']:8.0f}%{100 * d['rd_sales']:7.0f}%")
    c = R["costco"]
    print(f"Costco: {c['inventory_days']:.0f} days of stock, {c['payable_days']:.0f} days to pay; fees "
          f"{100 * c['fee_share']:.0f}% of operating income; per member ${c['per_member']['spend']:,.0f} spent, "
          f"${c['per_member']['fee']:.0f} fee, ${c['per_member']['oi']:.0f} operating income")
    d = R["delta"]
    print(f"Delta per seat mile: {d['trasm']}c in, {d['casm']}c out, margin {d['margin']:.2f}c (rebuilds "
          f"${d['check']:.2f}bn); fuel {d['fuel']:.2f}c, labour {d['labor']:.2f}c, Amex {d['amex']:.2f}c")
    m = R["cash"]["msft"]
    print(f"Microsoft FY2026: net income {m['ni']:.1f}, operating cash {m['ocf']:.1f}, capex {m['capex']:.1f}, free "
          f"cash {m['fcf']:.1f}; Q1 FY27 free cash {m['q1']['fcf']:.1f} (a year earlier {m['q1_prev']['fcf']:.1f})")
    print("growing bakery:", [(round(x["profit"]), round(x["cash"])) for x in R["growth"]])


if __name__ == "__main__":
    main()
