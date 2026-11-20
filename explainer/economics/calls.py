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
    Call("nash_guessing", 11, "game theory's equilibrium for the guessing game (Nash's concept, 1950, with every "
         "player rational and knowing the others are)", "1950",
         "everyone chooses 0 in two-thirds of the average, the only Nash equilibrium",
         "iterated elimination of dominated choices: no one should name more than 66.7, so no one more than 44.4, and "
         "so on down to 0",
         "in Nagel's first rounds (1995) the 67 students' choices averaged 36.73, so the winning number was about 25; "
         "in the Financial Times contest of 1997 the readers' average was 18.9 and the winning number 13; only with "
         "repetition do choices fall toward 0, as Nagel's later rounds showed",
         "wrong",
         ("R. Nagel, American Economic Review 85(5) (1995), section IV and Figure 1",
          "R. Thaler's Financial Times contest (1997), as reported in Chicago Booth Review (2015)")),
    Call("stigler_cheating", 12, "George Stigler, \"A Theory of Oligopoly\" (1964)", "1964",
         "collusion is a problem of policing: cartels fail when members can cut prices in secret, so what breaks "
         "them is cheating that goes undetected",
         "each member gains by shading its price to a few buyers; the cartel survives only if it can detect the "
         "shading from what buyers do",
         "Levenstein and Suslow's survey of the empirical studies (2006) found that cartels break up occasionally "
         "from cheating or weak monitoring, but most often from entry and from bargaining problems among the "
         "members; and many cartels survive for years (the durations they found are bimodal: many short-lived "
         "cartels, many long-lived ones)",
         "partly right",
         ("G. J. Stigler, Journal of Political Economy 72(1) (1964): 44-61",
          "M. C. Levenstein and V. Y. Suslow, Journal of Economic Literature 44(1) (2006): 43-95, abstract and "
          "conclusion")),
    Call("lemons_referees", 13, "the referees and editors who turned down Akerlof's paper", "before 1970",
         "the paper was trivial (the American Economic Review and the Review of Economic Studies), or wrong: if it "
         "were right, no goods could be traded (the Journal of Political Economy)",
         "used cars are traded every day, so a theory in which quality uncertainty stops trade must be mistaken",
         "the Quarterly Journal of Economics printed it in 1970; it became one of the most cited papers in economics, "
         "and Akerlof shared the 2001 Nobel prize with Spence and Stiglitz for the analysis of markets with "
         "asymmetric information; used goods do trade, through the guarantees, brand names and dealers that the "
         "paper itself said grow up to counter the problem",
         "wrong",
         ("G. A. Akerlof, Quarterly Journal of Economics 84(3) (1970), the section \"Counteracting Institutions\"",
          "G. A. Akerlof, \"Writing 'The Market for Lemons'\" (2003), as excerpted",
          "The Nobel Foundation, the 2001 prize in economic sciences")),
    Call("acid_rain_benefits", 15, "Paul Portney and other analysts of the 1990 Clean Air Act Amendments",
         "1990", "the acid-rain programme's benefits would be roughly equal to its costs",
         "the damage of acid rain to lakes, forests and buildings, valued against the cost of cutting sulphur emissions",
         "by Schmalensee and Stavins's tally, the programme's annual benefits came to $59 to $116 billion against costs "
         "of $0.5 to $2 billion, more than 95 percent of the benefits from fewer fine particles in the air people "
         "breathe, which nobody had counted; the ecological benefits alone were probably smaller than the costs",
         "wrong",
         ("P. R. Portney, \"Economics and the Clean Air Act\", Journal of Economic Perspectives 4(4) (1990): 173-181, "
          "as cited by Schmalensee and Stavins",
          "R. Schmalensee and R. N. Stavins, Journal of Economic Perspectives 27(1) (2013): 103-122, Table 1")),
    Call("ehrlich", 19, "Paul Ehrlich, The Population Bomb",
         "1968", "the battle to feed all of humanity is over: in the 1970s hundreds of millions of people will starve to "
                 "death in spite of any crash programmes embarked upon then",
         "Malthus's arithmetic, population against food, applied to a world of 3.5 billion growing at about 2% a year",
         "the world's population passed 8 billion in 2022, and food supply per person rose; the famines of the 1970s and "
         "after, terrible as they were, killed far fewer than hundreds of millions, and most were made by war and "
         "policy; in 1980 Ehrlich bet Julian Simon that five metals would be dearer in 1990, and in 1990 he paid "
         "Simon $576.07",
         "wrong",
         ("P. R. Ehrlich, The Population Bomb (1968), prologue",
          "United Nations, World Population Prospects; Our World in Data, population",
          "J. Tierney, \"Betting on the Planet\", New York Times Magazine, 2 December 1990")),
    Call("romer_scale", 21, "Paul Romer, Endogenous Technological Change",
         "1990", "the stock of human capital determines the rate of growth: an economy that puts more people to work "
                 "on research grows faster, for ever",
         "a model in which each researcher adds ideas in proportion to the ideas already known, so growth is "
         "proportional to the number of researchers",
         "the effective number of American researchers rose about 23-fold from the 1930s to the 2010s while growth of "
         "productivity did not rise at all (Bloom, Jones, Van Reenen and Webb 2020); Jones (1995) had already "
         "rejected the scale effect on American time series; the theory survived by letting ideas get harder to find",
         "wrong",
         ("P. M. Romer, Journal of Political Economy 98(5) (1990): S71-S102, abstract",
          "C. I. Jones, Quarterly Journal of Economics 110(2) (1995): 495-525",
          "N. Bloom, C. I. Jones, J. Van Reenen and M. Webb, American Economic Review 110(4) (2020)")),
    Call("stress_2022", 26, "the Federal Reserve's 2022 stress test scenarios",
         "February 2022", "the severe but plausible scenario that large banks must be able to survive: a deep recession "
                          "with the 10-year Treasury yield falling to 3/4 percent, short rates near zero throughout, and "
                          "unemployment rising to 10 percent",
         "a recession of the kind that had hit banks before, in which rates fall; the Fed stresses that a scenario is "
         "not a forecast",
         "rates rose instead: the federal funds rate went from near zero to over 4 percent within the year and the "
         "10-year yield to about 4 percent; the losses that sank Silicon Valley Bank in March 2023 came from long "
         "bonds losing value as rates rose, a risk the scenario did not test",
         "wrong",
         ("Board of Governors of the Federal Reserve System, 2022 Stress Test Scenarios (February 2022)",
          "FRED: the federal funds rate and the 10-year Treasury yield",
          "Board of Governors, Review of the Federal Reserve's Supervision and Regulation of Silicon Valley Bank "
          "(April 2023)")),
    Call("friedman_1967", 28, "Milton Friedman, in his presidential address to the American Economic Association",
         "December 1967", "there is always a temporary trade-off between inflation and unemployment; there is no "
                          "permanent trade-off: holding unemployment below its natural rate would take ever faster "
                          "inflation, because people come to expect any steady rate",
         "expectations catch up with any inflation that lasts; only surprises lower unemployment, and surprises cannot "
         "be repeated forever",
         "in the decade after the address, America's inflation and unemployment both rose: from 5.4 percent and 3.5 "
         "percent in 1969 to 9.1 percent and 8.5 percent in 1975, and 13.5 percent and 7.2 percent in 1980; the stable "
         "curve of the 1960s disappeared, and the natural rate became the core of the textbooks",
         "right",
         ("M. Friedman, \"The Role of Monetary Policy\", American Economic Review 58(1) (1968): 1-17",
          "BLS: the consumer price index and the unemployment rate, via FRED")),
    Call("team_transitory", 28, "the Federal Reserve's projections, with many forecasters",
         "June 2021", "the median projection had PCE inflation at 3.4 percent in 2021 falling to 2.1 percent in 2022, "
                      "as the bottlenecks of the reopening cleared: a transitory rise",
         "supply shocks from the pandemic's reopening, which would unwind, and long-run expectations anchored near 2 "
         "percent",
         "PCE inflation was 5.7 percent over 2021 and 6.1 percent over 2022 (fourth quarter to fourth quarter, as now "
         "revised); the Federal Reserve began raising rates in March 2022, and inflation fell to about 3 percent "
         "during 2023 as supply recovered, without a recession",
         "wrong",
         ("Board of Governors of the Federal Reserve System, press conference and Summary of Economic Projections, "
          "16 June 2021",
          "BEA: the PCE price index, via FRED")),
    Call("keynes_peace", 27, "John Maynard Keynes, in The Economic Consequences of the Peace",
         "1919", "the reparations the Allies meant to demand were more than Germany could pay, and pressing them would "
                 "impoverish Central Europe and end in disaster: if we aim deliberately at the impoverishment of "
                 "Central Europe, vengeance, I dare predict, will not limp",
         "his estimates of what Germany could export once it had lost its colonies, ships and much of its coal, and of "
         "how far a defeated economy could be squeezed",
         "the bill was set only in 1921, cut by the Dawes Plan (1924) and the Young Plan (1929), suspended in 1931 and "
         "ended in 1932, so it was never paid in full; Germany went through hyperinflation in 1923 and depression "
         "after 1929, and the peace ended in war; but Etienne Mantoux argued in 1946 that Germany could have paid, "
         "as its spending on rearmament later showed, and Keynes himself judged the 1921 figure more reasonable",
         "partly right",
         ("J. M. Keynes, The Economic Consequences of the Peace (1919), chapter 6",
          "E. Mantoux, The Carthaginian Peace, or the Economic Consequences of Mr. Keynes (1946)",
          "P. Clavin, G. Corsetti, M. Obstfeld and A. Tooze (eds.), Keynes's Economic Consequences of the Peace after "
          "100 Years (2023)")),
    Call("cagan_ceiling", 25, "the revenue theory of hyperinflation, in Phillip Cagan's estimates",
         "1956", "a government printing money to pay its bills raises the most real revenue at a steady inflation of "
                 "one over the semi-elasticity of money demand, about 20 percent a month for Germany; a government "
                 "after revenue should not inflate faster than that",
         "Cagan's money demand, in which real balances fall exponentially as expected inflation rises, estimated on "
         "seven hyperinflations",
         "governments inflated far faster: German prices rose 322 percent a month on average from August 1922 to "
         "November 1923, and in most of Cagan's seven cases inflation ran above the revenue-maximizing rate, a puzzle "
         "known since as Cagan's paradox; explanations include expectations that lag, so that faster printing pays "
         "for a while, and governments that could not commit to stop",
         "wrong",
         ("P. Cagan, \"The Monetary Dynamics of Hyperinflation\", in M. Friedman (ed.), Studies in the Quantity Theory "
          "of Money (1956): 25-117",
          "secondary summaries of Cagan's table (the German average and the revenue-maximizing rate)")),
    Call("dmp_volatility", 24, "Dale Mortensen and Christopher Pissarides",
         "1994", "a matching model driven by aggregate productivity shocks alone reproduces reasonably well the "
                 "cyclical behaviour of job creation and job destruction in the United States",
         "simulations of the model with Nash-bargained wages and an aggregate shock process",
         "the pattern held: in recessions job destruction jumps and job creation falls; the size did not: Shimer "
         "(2005) calibrated the model to American data, and shocks to productivity of the observed size move the "
         "vacancy-unemployment ratio about as much as productivity itself, while in the data it is almost twenty "
         "times as volatile; the model needs implausibly large shocks (Hall 2005), and twenty years of repairs "
         "followed",
         "partly right",
         ("D. T. Mortensen and C. A. Pissarides, Review of Economic Studies 61(3) (1994): 397-415, abstract",
          "R. Shimer, American Economic Review 95(1) (2005): 25-49, abstract",
          "R. E. Hall, American Economic Review 95(1) (2005): 50-65, abstract")),
    Call("fisher_plateau", 23, "Irving Fisher, speaking in New York",
         "October 1929", "stock prices have reached what looks like a permanently high plateau",
         "the decade's rise in earnings, new industries and better management, which he thought justified the prices",
         "the market crashed within days; in Shiller's January figures the S&P composite was worth 24.86 in 1929 and "
         "8.30 in 1932, two-thirds lower in nominal terms and three-fifths lower after inflation, and it did not "
         "regain its 1929 real level until the 1950s",
         "wrong",
         ("I. Fisher, remarks to the Purchasing Agents Association, New York, 15 October 1929, as reported in the "
          "New York Times, 16 October 1929",
          "R. J. Shiller, Market Volatility (1989), ch. 26 data, updated (S&P composite, January values)")),
    Call("hall_random_walk", 22, "Robert Hall, Stochastic Implications of the Life Cycle-Permanent Income Hypothesis",
         "1978", "consumption follows a random walk: nothing known today, anticipated changes in income included, "
                 "should predict how consumption changes next quarter",
         "the Euler equation of a household that borrows and lends freely and forms rational expectations: it has "
         "already spent out of any income it can foresee",
         "anticipated payments do move spending: the randomly timed rebates of 2001 and payments of 2008 raised "
         "spending in the quarter they arrived, most for households with little liquid wealth; Alaska's large, "
         "regular dividend showed no response in survey data, though account data later found one; the theory "
         "holds for households with cash to spare",
         "partly right",
         ("R. E. Hall, Journal of Political Economy 86(6) (1978): 971-987",
          "D. S. Johnson, J. A. Parker and N. S. Souleles, American Economic Review 96(5) (2006): 1589-1610",
          "C.-T. Hsieh, American Economic Review 93(1) (2003): 397-405",
          "L. Kueng, Quarterly Journal of Economics 133(4) (2018): 1693-1751")),
    Call("samuelson_soviet", 20, "Paul Samuelson, Economics (the textbook)",
         "1961", "Soviet national income would overtake America's between 1984 and 1997, on the growth rates the "
                 "edition assumed; the 1980 edition still drew the crossing, between 2002 and 2012",
         "extrapolation of measured Soviet growth, which came mostly from accumulating capital and moving people out "
         "of farming, into the future at its past rate",
         "Soviet growth slowed through the 1970s and 1980s, as diminishing returns to capital say it must when the "
         "residual is small, and the Soviet Union dissolved in 1991 without having overtaken; in the Maddison Project "
         "its income per head grew 3.3% a year in the 1950s, 1.4% in the 1970s and 0.7% in the 1980s, and never passed 38% of "
         "America's",
         "wrong",
         ("P. A. Samuelson, Economics, 5th ed. (1961) and 11th ed. (1980), as documented by D. M. Levy and S. J. Peart, "
          "Journal of Economic Behavior & Organization 78(1-2) (2011): 110-125",
          "Maddison Project Database 2023")),
    Call("duverger", 18, "Maurice Duverger, Les partis politiques",
         "1951", "plurality rule in single-member districts tends to produce two-party systems: voters desert third "
                 "parties that cannot win, and politicians stop joining them",
         "the mechanics of the rule (a third party's votes are wasted) and the psychology of voters who know it",
         "in the United States every president since 1853 has been a Democrat or a Republican; but Britain, Canada and "
         "India, which also elect by plurality, keep third and regional parties in parliament, strong where their "
         "votes are concentrated, as Riker's history of the law records",
         "partly right",
         ("M. Duverger, Les partis politiques (1951)",
          "W. H. Riker, American Political Science Review 76(4) (1982): 753-766")),
    Call("roth_stability", 17, "Alvin Roth, on the American medical match",
         "1984", "a clearinghouse survives if the matches it produces are stable; one whose matches can be blocked, by a "
                 "doctor and a hospital who both prefer each other to what they were given, will be abandoned as people "
                 "act on that",
         "the history of the American market for interns, and Gale and Shapley's theorem",
         "in Britain, where each region of the health service built its own clearinghouse in the 1960s and 1970s, both "
         "stable ones (Edinburgh from 1969, Cardiff) were still in use, and four of the six unstable ones (Birmingham, "
         "Edinburgh's of 1967, Newcastle, Sheffield) were abandoned; the two unstable survivors, Cambridge and the "
         "London Hospital, each matched one medical school to one hospital, where instabilities were hard to act on",
         "right",
         ("A. E. Roth, Journal of Political Economy 92(6) (1984): 991-1016",
          "A. E. Roth, American Economic Review 81(3) (1991): 415-440",
          "A. E. Roth, Nobel Prize lecture (2012), table of clearinghouses")),
    Call("dutch_3g", 16, "the Dutch government, before its 3G auction",
         "2000", "its five licences for third-generation mobile spectrum would raise almost 10 billion euros",
         "Britain's auction three months earlier, scaled to the Netherlands' population",
         "the auction in July 2000 raised less than 3 billion euros, about 170 euros a head against Britain's 650: "
         "five licences for five incumbents, the strongest would-be entrants partnered with incumbents, and the one "
         "weak entrant stopped bidding after a letter from an incumbent threatening legal action; Klemperer had warned "
         "in the Dutch press that the design would deter entry",
         "wrong",
         ("P. Klemperer, \"How (Not) to Run Auctions: the European 3G Telecom Auctions\", European Economic Review "
          "46(4-5) (2002): 829-845",)),
    Call("multitask_tests", 14, "Bengt Holmström and Paul Milgrom, \"Multitask Principal-Agent Analyses\" (1991)",
         "1991", "when only some of a job's tasks can be measured, strong pay for the measured ones pulls effort away "
         "from the rest; so where measures are narrow, incentives should be weak",
         "effort on one task raises the cost of effort on another; the agent goes where the pay is",
         "when Chicago tied schools' fortunes to test scores, Jacob and Levitt found serious cheating by teachers or "
         "administrators in at least 4 to 5 percent of elementary classrooms each year: effort diverted from "
         "teaching to the measure itself",
         "right",
         ("B. Holmström and P. Milgrom, Journal of Law, Economics and Organization 7 (1991): 24-52",
          "B. A. Jacob and S. D. Levitt, Quarterly Journal of Economics 118(3) (2003): 843-877, abstract")),
]}
