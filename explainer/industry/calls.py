"""Called it? (SYLLABUS §2.10): dated forecasts about each industry, other people's and this series' own.

Other people's calls are taken from dated primary documents (or the best surviving record of one) and shown with what
happened.  The series' own calls are logged with the date made, the rule that will score them and the date they come
due; a refresh scores the ones that have come due (SYLLABUS §7, phase 3).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Call:
    part: int
    who: str
    made: str          # ISO date (or month) the call was made
    claim: str
    source: str
    outcome: str = ""  # what happened, with its source; empty while pending
    rule: str = ""     # for the series' own calls: how it will be scored
    due: str = ""      # when it can be scored
    ours: bool = False


CALLS = [
    Call(1, "Steve Ballmer, chief executive of Microsoft", "2007-04",
         "\"There's no chance that the iPhone is going to get any significant market share. No chance.\"",
         "USA Today CEO Forum, 2007-04-29, as quoted by MacRumors 2007-04-30",
         outcome="Apple's share of smartphone shipments was 19.7% in 2025 (IDC) and its iPhone sales $254.1bn in "
                 "fiscal 2026 (10-K): about a fifth of the phones and most of the industry's profit"),
    Call(1, "Industry, Built", "2026-11-23",
         "Smartphone shipments worldwide in calendar 2026 will be below 1.15 billion (2025: 1.26 billion).",
         "This series, Part 1, chapter 15; reasoning: IDC's -7.4% in Q2 and Counterpoint's -20% in Q3 2026",
         rule="IDC's first full-year release for 2026 (preliminary figure); true if below 1,150 million",
         due="2027-01", ours=True),
    Call(2, "Wassily Leontief", "1983",
         "\"The role of humans as the most important factor of production is bound to diminish in the same way that "
         "the role of horses in agricultural production was first diminished and then eliminated by the introduction "
         "of tractors.\"", "Leontief (1983), in The Long-Term Impact of Technology on Employment and Unemployment, "
                          "National Academy of Engineering, p. 3",
         outcome="US payroll employment rose from 90.3 million (1983) to 158.4 million (2025) (BLS via FRED); the "
                 "work moved between industries rather than disappearing, so far"),
    Call(2, "Industry, Built", "2026-11-23",
         "In 2030, health care and social assistance will employ more people than manufacturing and retail trade "
         "combined (2025: 23.3 million against 28.1 million). Probability: 40%.",
         "This series, Part 2, chapter 18; health care added about 0.78 million jobs in 2025, manufacturing and "
         "retail were flat",
         rule="BLS Current Employment Statistics annual averages for 2030: CES6562000001 against MANEMP + USTRADE",
         due="2031-02", ours=True),
    Call(3, "Bethany McLean, Fortune", "2001-03-05",
         "\"How exactly does Enron make its money?\" Enron trades at about 55 times earnings, earns about 7% on its "
         "invested capital, and its operating cash flow fell to $100 million in the first nine months of 2000.",
         "Fortune, \"Is Enron Overpriced?\", 5 March 2001",
         outcome="Enron restated 1997-2000 net income down by $591m (Form 8-K, 8 November 2001) and filed for "
                 "chapter 11 on 2 December 2001 (Form 8-K, 17 December 2001)"),
    Call(3, "Industry, Built", "2026-11-23",
         "Microsoft's free cash flow in fiscal 2027 (operating cash flow less additions to property and equipment) "
         "will be below fiscal 2026's $67.0bn, while its operating income rises above fiscal 2026's $155.2bn. "
         "Probability: 65%.",
         "This series, Part 3, chapter 14; Q1 FY2027 free cash $18.6bn against $25.7bn a year earlier; capex "
         "guidance about $170bn including finance leases",
         rule="Microsoft Form 10-K FY2027, cash-flow statement and income statement: both conditions must hold",
         due="2027-08", ours=True),
]


def calls(part: int | None = None, ours: bool | None = None) -> list[Call]:
    return [c for c in CALLS if (part is None or c.part == part) and (ours is None or c.ours == ours)]
