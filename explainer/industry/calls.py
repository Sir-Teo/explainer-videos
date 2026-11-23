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
         "This series, Part 1, chapter 12; reasoning: IDC's -7.4% in Q2 and Counterpoint's -20% in Q3 2026",
         rule="IDC's first full-year release for 2026 (preliminary figure); true if below 1,150 million",
         due="2027-01", ours=True),
]


def calls(part: int | None = None, ours: bool | None = None) -> list[Call]:
    return [c for c in CALLS if (part is None or c.part == part) and (ours is None or c.ours == ours)]
