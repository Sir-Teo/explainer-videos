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
    Call("lalonde_1986", 4, "the standard non-experimental evaluation of a training programme", "the 1970s and 1980s",
         "the effect of the National Supported Work programme on men's 1978 earnings, from a comparison group drawn "
         "from a survey (the PSID) and a regression adjusting for age, schooling and race: -$8,067",
         "the methods of the day: survey comparison groups, regression adjustment, difference in differences",
         "the same programme had been run as an experiment: random assignment gave +$886; most non-experimental "
         "estimates missed it, many by thousands of dollars, and the specification tests could not say which",
         "wrong",
         ("R. J. LaLonde (1986), American Economic Review 76(4): 604-620, table 5",)),
    Call("mcfadden_bart", 5, "Daniel McFadden's model of travellers' choices", "1973",
         "BART, the San Francisco Bay Area's new rapid transit, would carry 6.3% of work trips (the official "
         "projection, from a zone-level model, was about 15%)",
         "a random-utility (logit) model of individual commuters' choices among car, bus and BART, estimated on a "
         "survey of travellers before BART opened",
         "BART carried 6.2% of work trips in 1975; McFadden re-interviewed the same travellers to check",
         "right",
         ("D. McFadden, \"The Path to Discrete-Choice Models\", Access 20 (2002)",
          "D. McFadden, \"Economic Choices\", Nobel lecture, American Economic Review 91(3) (2001)")),
    Call("engel_1857", 6, "Ernst Engel, director of the Saxon statistical bureau", "1857",
         "the poorer a family, the larger the share of its spending that must go on food; so that share, other things "
         "equal, measures a population's standard of living, and it falls as people grow richer",
         "about 150 Belgian working families' budgets from Ducpetiaux's survey, and Saxon data",
         "America's share of spending on food at home fell from about a fifth in 1929 to under a tenth in 2025 as real "
         "spending per head rose about sixfold; in 2024 the poorest fifth of households spent a third of their income "
         "on food, the richest a sixteenth",
         "right",
         ("C. C. Zimmerman, Quarterly Journal of Economics 47(1) (1932), as quoted by R. Anker, PERI WP 247 (2011)",
          "BEA via FRED (personal consumption expenditures by type of product)",
          "USDA ERS, Food Prices and Spending (2026), from the BLS Consumer Expenditure Survey")),
    Call("bernoulli_1738", 7, "Daniel Bernoulli, in St Petersburg", "1738",
         "a game with an infinite expected prize is worth a small, finite sum, more to the rich than to the poor: "
         "people value money by the logarithm of their wealth; on his rule, his game (one coin first, doubling) is "
         "worth about $6 to someone with $1,000 and about $11 to a millionaire",
         "diminishing marginal utility: a gain means less the richer you are",
         "in 2009, twenty students bidding real money paid a median $1.75 to play, and 220 people asked hypothetically "
         "$1.50; their bids barely changed when the game was cut off after three tosses or after fifteen, which the "
         "logarithm does not predict",
         "partly right",
         ("D. Bernoulli, Commentarii Academiae Scientiarum Imperialis Petropolitanae 5 (1738); Econometrica 22(1) "
          "(1954)", "B. Y. Hayden and M. L. Platt, Judgment and Decision Making 4(4) (2009)")),
    Call("nafta_1992", 9, "Horacio Sobarzo's applied general equilibrium model of Mexico, one of the models presented "
         "at the US International Trade Commission's 1992 conference on NAFTA",
         "1992",
         "free trade would raise Mexico's imports from North America, relative to its GDP, most in nonelectrical "
         "machinery (+20.7%), iron and steel (+17.7%) and mining (+13.2%), and lower them in tobacco, food and paper",
         "a multisector general equilibrium model of the kind used to assess trade agreements: trade grows most where "
         "it is already large and the barrier falls most, governed by Armington elasticities",
         "from 1989 to 2009 Mexico's imports from North America rose relative to GDP in 20 of 21 industries, by a "
         "median of about 95%, most in tobacco (+576%), chemicals (+219%) and beverages (+189%); across the 21 "
         "industries the weighted correlation between predicted and actual growth was -0.12, and Timothy Kehoe, who "
         "had worked on the model, said the forecasts' correlations with what happened \"average about zero\"",
         "wrong",
         ("T. J. Kehoe, NAFTA at 20 (Federal Reserve Bank of Dallas, 2014), ch. 1, table 1",
          "T. J. Kehoe, in Frontiers in Applied General Equilibrium Modeling (Cambridge, 2005)",
          "USITC publication 2516 (May 1992)")),
]}
