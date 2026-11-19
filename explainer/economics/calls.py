"""Called it? (videos/economics/SYLLABUS.md, section 1.3): dated predictions, scored against what happened.

Once a part, a prediction made in advance is put beside the outcome: who predicted what, when, on what basis, and
what happened.  Right and wrong calls are both shown.  A :class:`Call` records the prediction and its sources; the
numbers of both sides come from the Data Room in the part's ``compute.py`` and are asserted there, so the card on
screen cannot drift from the data.
"""

from __future__ import annotations

from dataclasses import dataclass

VERDICTS = ("right", "wrong", "partly right", "too early to say")


@dataclass(frozen=True)
class Call:
    key: str
    part: int
    who: str
    when: str
    said: str  # the prediction, in words
    basis: str  # what it rested on
    outcome: str  # what happened, in words (numbers come from compute.py)
    verdict: str
    sources: tuple

    def __post_init__(self):
        assert self.verdict in VERDICTS, self.verdict


CALLS = {c.key: c for c in [
    Call("spf_2008", 1, "the median of the Survey of Professional Forecasters", "August 2008",
         "real GDP in 2009 a little higher than in 2008", "the professional forecasters the Federal Reserve Bank "
         "of Philadelphia surveys each quarter",
         "real GDP fell in 2009, by more than in any year since 1946", "wrong",
         ("Federal Reserve Bank of Philadelphia, SPF median forecasts, 2008 Q3 survey", "BEA via FRED (GDPCA)")),
    Call("smith_1956", 2, "Vernon Smith, about to run his first market experiment", "January 1956",
         "the competitive model would fail to predict the outcome, so a more competitive trading procedure would "
         "make a stronger case against it than Chamberlin's",
         "Chamberlin's classroom markets of 1948, which traded more than the competitive quantity at scattered "
         "prices, and the textbook's own doubts",
         "the market converged quickly to near the predicted price and volume with 22 traders who knew only their "
         "own cards; a lopsided design later converged too", "wrong",
         ("V. L. Smith, autobiography, Nobel Prize in Economic Sciences 2002 (nobelprize.org)",
          "V. L. Smith (1962), Journal of Political Economy 70(2): 111-137")),
]}
