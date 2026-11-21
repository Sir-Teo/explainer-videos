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
    Call("bernanke_2002", 30, "Ben Bernanke, a governor of the Federal Reserve, before the National Economists Club",
         "November 2002", "the Federal Reserve, with other parts of the government, has sufficient policy instruments "
                          "to ensure that any deflation that might occur in the United States would be both mild and "
                          "brief",
         "even with its interest rate at zero, a central bank can buy longer-term assets, lend widely and, with the "
         "fiscal authorities, put more money into circulation: under paper money, a determined government can "
         "always raise spending",
         "after the federal funds rate reached zero in December 2008 it stayed there for seven years; consumer prices "
         "fell over twelve months in 14 months between 2008 and 2015, by at most 2.0 percent (July 2009, with oil), "
         "while core PCE inflation never went below 0.6 percent; but it averaged 1.5 percent over 2009-2019, below the "
         "2 percent target the Fed adopted in 2012",
         "right",
         ("B. S. Bernanke, \"Deflation: Making Sure 'It' Doesn't Happen Here\", remarks before the National Economists "
          "Club, Washington, D.C., 21 November 2002",
          "BLS: the CPI; BEA: the core PCE price index; Federal Reserve: the federal funds rate; via FRED")),
    Call("imf_2010", 32, "the IMF's forecasters, in the World Economic Outlook", "April 2010",
         "growth in 2010-11 for the European economies, forecast with each government's planned budget consolidation "
         "already taken into account",
         "the IMF's models and judgement, with the consolidation plans of spring 2010",
         "across 26 European economies, each percentage point of GDP of planned consolidation went with growth over "
         "2010-11 about 1.1 points lower than forecast (Blanchard and Leigh's regression, recomputed here from their "
         "replication data); the forecasts had underestimated the multiplier, by about one",
         "wrong",
         ("O. Blanchard and D. Leigh, \"Growth Forecast Errors and Fiscal Multipliers\", American Economic Review "
          "103(3): 117-120 (2013), and NBER Working Paper 18779",
          "IMF World Economic Outlook forecasts (spring 2010, fall 2012) as compiled in the replication files")),
    Call("romer_2000", 31, "Christina and David Romer, in the American Economic Review", "June 2000",
         "the Federal Reserve has considerable information about inflation beyond what is known to commercial "
         "forecasters: once its staff's forecast is known, the others add almost nothing",
         "the Greenbook's inflation forecasts, released after five years, against those of commercial forecasters, "
         "1965-1991",
         "on the Philadelphia Fed's data, over the four quarters ahead, the Greenbook's error was 1.33 points against "
         "the professional forecasters' 1.69 in 1969-91, and given both, the best combination put all the weight on "
         "the Greenbook; over 1992-2020 the errors were 0.98 and 0.95, and the edge was gone",
         "partly right",
         ("C. D. Romer and D. H. Romer, \"Federal Reserve Information and the Behavior of Interest Rates\", American "
          "Economic Review 90(3): 429-457 (2000)",
          "Federal Reserve Bank of Philadelphia: the Tealbook (Greenbook) Data Set and the Survey of Professional "
          "Forecasters; BEA: the GDP price index via FRED")),
    Call("prescott_75", 29, "Edward Prescott, in the Federal Reserve Bank of Minneapolis's Quarterly Review",
         "Fall 1986", "technology shocks account for more than half of America's postwar fluctuations, with a best "
                      "estimate near 75 percent; in the theory, an improvement in technology raises output, investment "
                      "and hours worked together",
         "the growth model with random technology, its parameters chosen from growth facts, reproduced the size and "
         "comovement of America's postwar cycles, with the shocks measured by the Solow residual",
         "the residual was partly not technology: firms work people and machines harder in booms, and corrected for "
         "that (Basu, Fernald and Kimball 2006) improvements cut hours and investment at first; long-run VARs split: "
         "with hours in growth rates (Gali 1999) hours fall and technology explains little of the cycle, in levels "
         "(Christiano, Eichenbaum and Vigfusson 2003) hours rise and it explains much; few now say three quarters, "
         "but technology matters, and the method won",
         "partly right",
         ("E. C. Prescott, \"Theory Ahead of Business Cycle Measurement\" and \"Response to a Skeptic\", Federal "
          "Reserve Bank of Minneapolis Quarterly Review 10(4) (1986)",
          "J. Gali, \"Technology, Employment, and the Business Cycle\", American Economic Review 89(1) (1999): 249-271",
          "S. Basu, J. Fernald and M. Kimball, \"Are Technology Improvements Contractionary?\", American Economic "
          "Review 96(5) (2006): 1418-1448",
          "L. Christiano, M. Eichenbaum and R. Vigfusson, \"What Happens After a Technology Shock?\", NBER Working "
          "Paper 9819 (2003)",
          "J. Fernald, \"Trend Breaks, Long-Run Restrictions, and Contractionary Technology Improvements\", Journal of "
          "Monetary Economics 54 (2007): 2467-2485",
          "BLS: output per hour and hours in the nonfarm business sector, via FRED")),
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
    Call("survey_1979", 38, "Economists surveyed by Kearl, Pope, Whiting and Wimmer", "1979",
         "a minimum wage increases unemployment among young and unskilled workers: 90% of 211 economists agreed, "
         "or agreed with provisos",
         "the employment effect of the minimum wage",
         "for the moderate increases studied since, the average effect on employment has been close to zero, from "
         "Card and Krueger's restaurants to Cengiz et al.'s 138 state increases; losses appear where minimums are high "
         "relative to local wages, as in Seattle's hours; later surveys found the agreement falling",
         "partly right",
         ("J. R. Kearl, C. L. Pope, G. C. Whiting and L. T. Wimmer, \"A Confusion of Economists?\", American "
          "Economic Review 69(2): 28-37 (1979)",
          "D. Card and A. B. Krueger, American Economic Review 84(4): 772-793 (1994)",
          "D. Cengiz, A. Dube, A. Lindner and B. Zipperer, Quarterly Journal of Economics 134(3): 1405-1454 (2019)",
          "E. Jardim et al., American Economic Journal: Economic Policy 14(2): 263-314 (2022)")),
    Call("leontief_1983", 39, "Wassily Leontief, at a National Academy of Engineering symposium", "1983",
         "the role of humans as the most important factor of production is bound to diminish, as the role of horses "
         "in agriculture was diminished and then eliminated by tractors",
         "machines' substitution for human labour",
         "forty years on, a larger share of prime-age Americans work than in 1983, but labour's share of business "
         "income has fallen and the middle of the wage distribution has hollowed out; artificial intelligence "
         "reopens the question",
         "too early to say",
         ("W. Leontief, \"National Perspective: The Definition of Problem and Opportunity\", in The Long-Term Impact "
          "of Technology on Employment and Unemployment, National Academy of Engineering (1983), as quoted in "
          "secondary listings",
          "BLS via FRED: LNS12300060 (employment-population ratio, 25-54) and PRS85006173 (labor share)")),
    Call("aaa_2006", 53, "Moody's and Standard & Poor's, rating mortgage-backed securities",
         "2006",
         "the senior tranches of securities built from subprime and other risky mortgages deserved the highest "
         "rating, triple-A: as unlikely to default as the safest corporate and government bonds",
         "models of default fitted to years of rising house prices, and ratings paid for by the issuers who chose "
         "which agency to hire",
         "after house prices began to fall in 2006, most mortgage securities rated triple-A that year were "
         "downgraded within a few years, many of them to junk, and the downgrades helped turn falling house prices "
         "into a financial crisis",
         "wrong",
         ("Financial Crisis Inquiry Commission, The Financial Crisis Inquiry Report (2011), conclusions",
          "U.S. Senate Permanent Subcommittee on Investigations, Wall Street and the Financial Crisis (2011)")),
    Call("sydney_1957", 58, "the government of New South Wales", "1957",
         "the Sydney Opera House would cost about A$7 million and be finished by January 1963",
         "an estimate made when Jorn Utzon's competition-winning design was a sketch, before anyone knew how to build "
         "its shells",
         "it opened in October 1973, ten years late, at a cost of A$102 million, about fourteen times the estimate",
         "wrong",
         ("Sydney Opera House, Sydney Opera House facts", "National Museum of Australia, Defining Moments: Sydney "
          "Opera House", "Guinness World Records, largest proportional increase in cost for a building project")),
    Call("sahm_2024", 57, "Claudia Sahm, in a Bloomberg Opinion column", "August 2024",
         "the United States was not in a recession, although her own rule had just been triggered by July's rise in "
         "unemployment", "unemployment had risen partly because more people were looking for work, not only because "
         "people were losing jobs, so the rule's signal could be false",
         "no recession followed: output kept growing, and no business-cycle peak has been dated since 2020",
         "right",
         ("C. Sahm, Bloomberg Opinion, 7 August 2024", "Congressional Research Service, Insight IN12410 (August 2024)",
          "NBER business-cycle dates via FRED (USREC)")),
    Call("google_flu", 54, "Google's flu-tracking model (Ginsberg and colleagues, in Nature)", "2008",
         "the share of doctor visits for influenza-like illness in each region of the United States could be "
         "estimated from the volume of 45 search queries, a week or two before the CDC's surveillance reports",
         "a correlation, fitted to past years of the CDC's reports, between the rate of flu-like illness and the "
         "share of searches for terms like it; no model of why people search",
         "the first version missed the 2009 pandemic, which came out of season; in the 2012-13 season its estimate "
         "of doctor visits for flu-like illness was about twice what the CDC recorded, and three-week-old CDC "
         "data forecast the present better than it did",
         "partly right",
         ("J. Ginsberg et al., \"Detecting influenza epidemics using search engine query data\", Nature 457 "
          "(2009): 1012-1014",
          "D. Lazer, R. Kennedy, G. King and A. Vespignani, \"The parable of Google Flu: traps in big data analysis\","
          " Science 343 (2014): 1203-1205")),
    Call("krusell_smith_1998", 52, "Per Krusell and Anthony Smith, in the Journal of Political Economy",
         "October 1998",
         "in a calibrated economy with uninsurable income risk and aggregate shocks, the behaviour of the "
         "macroeconomic aggregates can be almost perfectly described using only the mean of the wealth distribution",
         "a forecasting rule in mean capital, solved for and checked by its fit in simulations of the whole economy",
         "for the path of capital the finding has held in many variants; but where many households have little "
         "liquid wealth, aggregate spending and the transmission of monetary and fiscal policy depend on the "
         "distribution, as heterogeneous-agent New Keynesian models showed twenty years later",
         "partly right",
         ("P. Krusell and A. A. Smith, Journal of Political Economy 106(5) (1998): 867-896",
          "G. Kaplan, B. Moll and G. L. Violante, American Economic Review 108(3) (2018): 697-743")),
    Call("moore_1965", 51, "Gordon Moore, director of research at Fairchild Semiconductor, in Electronics",
         "April 1965",
         "by 1975 the number of components on an integrated circuit, at the lowest cost per component, would reach "
         "about 65,000, doubling every year",
         "a handful of points from 1959 to 1965 on a logarithmic scale, and the economics of making chips",
         "in 1975 Moore reported that the projection had been realized, and revised the pace to a doubling every two "
         "years; at that pace the largest microprocessor grew from about 2,300 transistors in 1971 to tens of "
         "billions fifty years later",
         "right",
         ("G. Moore, Electronics 38(8), 19 April 1965; G. Moore, IEEE International Electron Devices Meeting (1975)",
          "Computer History Museum, The Silicon Engine; K. Rupp, Microprocessor Trend Data (2022), via Our World in "
          "Data")),
    Call("corinth_2021", 50, "Kevin Corinth, Bruce Meyer, Matthew Stadnicki and Derek Wu, in an NBER working paper",
         "September 2021",
         "replacing the child tax credit with a permanent child allowance would lead about 1.5 million working parents "
         "to leave work, and child poverty would fall by at most 22%",
         "simulation with participation elasticities from the mainstream of the literature, applied to the end of "
         "the credit's work requirement and to the income the allowance adds",
         "the temporary 2021 allowance showed no detectable effect on parents' work; Canada's permanent Child "
         "Benefit showed none either; but no permanent American allowance has been tried, and a temporary payment "
         "may not change behaviour as a permanent one would",
         "too early to say",
         ("K. Corinth, B. Meyer, M. Stadnicki and D. Wu, NBER Working Paper 29366 (2021)",
          "E. Ananat, B. Glasner, C. Hamilton and Z. Parolin, NBER Working Paper 29823 (2022); M. Baker, D. Messacar "
          "and M. Stabile, Journal of Labor Economics (2023)")),
    Call("diiulio_1995", 49, "John DiIulio, a political scientist at Princeton, in The Weekly Standard",
         "November 1995",
         "a coming wave of juvenile 'super-predators': some 270,000 more young predators on the streets by 2010 than "
         "in 1990",
         "a projection from the number of boys who would be teenagers, the share of them assumed to be violent, and "
         "the rise in youth violence of the early 1990s",
         "juvenile violence was already falling: by 2004 the arrest rate of juveniles for violent crime was half its "
         "1994 peak; DiIulio later said the prediction was wrong, but by then most states had made it easier to try "
         "juveniles as adults",
         "wrong",
         ("J. DiIulio, \"The Coming of the Super-Predators\", The Weekly Standard, 27 November 1995",
          "Office of Juvenile Justice and Delinquency Prevention, juvenile arrest bulletins (1998-2006)")),
    Call("hubbert_1956", 48, "M. King Hubbert, a geophysicist at Shell", "March 1956",
         "US oil production would peak between 1965, the likeliest year, and 1970, then decline for good",
         "a bell-shaped curve fitted to the discoveries and production of the lower 48 states",
         "production peaked in 1970 and fell for 38 years to its low in 2008; then shale drilling took crude "
         "output past the 1970 peak in 2018", "partly right",
         ("Hubbert (1956), as summarized by Deming, AAPG Bulletin 107(6), 2023",
          "Energy Institute, Statistical Review of World Energy (2026), via Our World in Data")),
    Call("treasury_2016", 47, "HM Treasury, in its analysis of the immediate impact of leaving the EU", "May 2016",
         "a vote to leave would tip the economy into a year-long recession, with GDP about 3.6 percent lower after two "
         "years than after a vote to remain (6 percent in a severe shock) and around 500,000 more people unemployed",
         "a shock to confidence and to the financial markets, with business investment and spending held back by "
         "uncertainty, in a model run by a government campaigning for one side",
         "there was no recession: the economy grew by about 2 percent in 2016 and unemployment kept falling; business "
         "investment did come in well below forecasts, and the longer-run costs of leaving are a separate, and "
         "continuing, argument",
         "wrong",
         ("HM Treasury, HM Treasury Analysis: The Immediate Economic Impact of Leaving the EU, Cm 9292 (May 2016)",
          "Institute for Fiscal Studies, post-referendum assessments (2016-17); Office for Budget Responsibility, "
          "Economic and Fiscal Outlook, November 2016")),
    Call("sachs_2005", 46, "Jeffrey Sachs, in The End of Poverty", "2005",
         "extreme poverty can be ended by 2025, if rich countries raise their aid to about $135 to $195 billion a "
         "year and spend it on investments in health, schools, farms and roads",
         "the Millennium Development Goals and the falls in poverty already under way in China and India; the idea "
         "of a poverty trap that a big push of aid could break",
         "aid rose, but never to the share of rich countries' incomes the plan required; poverty fell fast, mostly in "
         "Asia and with growth rather than aid, but in "
         "2025 about 808 million people still lived below the World Bank's line of $3.00 a day, about one in ten; "
         "the Millennium Villages' evaluation found gains on 30 of 40 outcomes, with poverty less conclusive",
         "wrong",
         ("J. D. Sachs, The End of Poverty: Economic Possibilities for Our Time (Penguin, 2005)",
          "S. Mitchell et al., \"The Millennium Villages Project: A Retrospective, Observational, Endline "
          "Evaluation\", Lancet Global Health 6(5), 2018, e500-e513",
          "World Bank, Poverty, Prosperity and Planet Report and June 2025 update; the UN Sustainable Development "
          "Goals Report 2025")),
    Call("experts_2018", 45, "many of 208 experts forecasting an effort experiment", "2016",
         "paying a token piece rate, a tenth of a cent, would crowd out effort: people paid almost nothing would work "
         "less than people paid nothing at all",
         "the psychology of motivation crowding out (a small payment turning a favour into a poor deal), and earlier "
         "experiments such as the day-care fine",
         "in DellaVigna and Pope's eighteen treatments, the token piece rate raised effort by 24% over no piece rate; "
         "experts as a group anticipated other patterns well, such as the power of psychological motivators, and "
         "averaging their forecasts beat most individual experts",
         "wrong",
         ("S. DellaVigna and D. Pope, \"What Motivates Effort? Evidence and Expert Forecasts\", Review of Economic "
          "Studies 85(2), 2018, 1029-1069, abstract",
          "S. DellaVigna and D. Pope, \"Predicting Experimental Results: Who Knows What?\", working paper (2017)")),
    Call("ballmer_2007", 44, "Steve Ballmer, chief executive of Microsoft, in an interview with USA Today", "April 2007",
         "there's no chance that the iPhone is going to get any significant market share; no chance",
         "an expensive phone entering a market of established makers, against Microsoft's own mobile software with "
         "its many licensed handset makers",
         "the iPhone and the App Store built a two-sided platform of buyers and developers; in 2023 Apple shipped "
         "234.6 million smartphones, 20.1% of the world market and the most of any maker (IDC), and Microsoft left "
         "the phone business; Ballmer later said he had been wrong",
         "wrong",
         ("USA Today interview, April 2007, as reported by InformationWeek and MacRumors",
          "IDC, press release of 15 January 2024")),
    Call("jcpenney_2012", 60, "Ron Johnson, chief executive of J.C. Penney, launching `fair and square' pricing",
         "January 2012",
         "shoppers would welcome honest everyday prices in place of a store run on sales and coupons; the new "
         "pricing went to every store at once, without a test",
         "his experience at Apple, whose stores did not run sales, and a belief that shoppers disliked the game of "
         "inflated list prices and constant markdowns",
         "sales in 2012 fell 24.8% to $12.99 billion, and sales in comparable stores 25.2%; the board removed Johnson "
         "in April 2013, and the company brought back sales and coupons",
         "wrong",
         ("Fortune, 8 April 2013", "J.C. Penney's fourth-quarter 2012 results, as reported by JCK (February 2013)",
          "Knowledge at Wharton, 'J.C. Penney's new strategy: consumers aren't buying it -- yet' (2012)")),
    Call("att_2016", 59, "Randall Stephenson, chief executive of AT&T, announcing its purchase of Time Warner",
         "October 2016",
         "the future of video is mobile and the future of mobile is video: owning Time Warner's channels and studio "
         "alongside AT&T's networks would create a stronger company, worth $85.4 billion to buy",
         "the bet that content and distribution are worth more under one owner, with about $1 billion a year of cost "
         "savings expected within three years",
         "the government's suit failed and the purchase closed in June 2018; in May 2021 AT&T agreed to spin "
         "WarnerMedia off and combine it with Discovery, and the transaction closed in April 2022, less than four "
         "years after the purchase",
         "wrong",
         ("AT&T, press release of 22 October 2016",
          "United States v. AT&T, 310 F. Supp. 3d 161 (D.D.C. 2018)",
          "AT&T, press release on the completion of the WarnerMedia transaction, April 2022")),
    Call("millercoors_2008", 43, "The U.S. Department of Justice, closing its investigation of the MillerCoors joint "
         "venture", "June 2008",
         "the joint venture of SABMiller and Molson Coors is not likely to lessen competition substantially, and its "
         "cost savings are substantial and credible",
         "an eight-month investigation that judged the savings in brewing and shipping verifiable and specific to "
         "the venture, large enough to offset its incentive to raise prices",
         "the savings were real: Coors moved into Miller's breweries, nearer its customers, and Ashenfelter, Hosken "
         "and Weinberg find they offset, at the mean, the roughly 2% that concentration added to prices; but prices "
         "of MillerCoors and Anheuser-Busch jumped together after the venture, and Miller and Weinberg estimate "
         "them 6-8% above what competition with those savings would give, consistent with coordination",
         "partly right",
         ("U.S. Department of Justice, statement of 5 June 2008",
          "Ashenfelter, Hosken and Weinberg, RAND Journal of Economics 46(2) (2015)",
          "Miller and Weinberg, Econometrica 85(6) (2017)")),
    Call("ss_1983", 42, "The 1983 Social Security Amendments, as projected by the program's actuaries", "1983",
         "the reforms would keep Social Security solvent for 75 years, with surpluses in the early years offsetting "
         "deficits later",
         "a rise in the payroll tax, taxation of benefits and a later retirement age, scored over 75 years",
         "the trustees and the Congressional Budget Office now expect the trust funds to run out in 2034, about a "
         "quarter of a century early; the actuaries had expected annual deficits from about 2025, and the economy "
         "and the population turned out differently from the 1983 assumptions",
         "wrong",
         ("Congressional Research Service, R47040 (2022)",
          "Brookings, 'Social Security: Today's financing challenge is at least double what it was in 1983'",
          "Social Security Administration, The 2025 OASDI Trustees Report")),
    Call("tcja_2017", 41, "Steven Mnuchin, Secretary of the Treasury", "September 2017",
         "not only will this tax plan pay for itself, but it will pay down debt",
         "the claim that lower rates on corporations and individuals would raise growth enough to replace the revenue",
         "federal receipts fell from about 17% of GDP in fiscal 2017 to about 16% in 2018 and 2019; the Congressional "
         "Budget Office estimated in April 2018 that the act would add about $1.9 trillion to deficits over ten "
         "years, after counting its effect on growth",
         "wrong",
         ("S. Mnuchin, as quoted by the Joint Economic Committee (2017)",
          "Congressional Budget Office, The Budget and Economic Outlook: 2018 to 2028 (April 2018)",
          "OMB via FRED: FYFRGDA188S (federal receipts as a percentage of GDP)")),
    Call("kuznets_1955", 40, "Simon Kuznets, in his presidential address to the American Economic Association",
         "December 1954",
         "income inequality widens in the early phases of economic growth, as people move from agriculture to "
         "industry, becomes stable for a while, and then narrows",
         "a few income series for the United States, Britain and Germany, and the arithmetic of migration from a "
         "poorer, more equal sector to a richer, less equal one",
         "inequality in rich countries did narrow from the 1920s to the 1970s, but mostly through depression, war "
         "and policy rather than migration; from about 1980 it widened again in America and Britain, long after "
         "industrialization",
         "partly right",
         ("S. Kuznets, \"Economic Growth and Income Inequality\", American Economic Review 45(1): 1-28 (1955)",
          "T. Piketty and E. Saez, top income shares updated to 2022; WID.world via Our World in Data")),
    Call("cairncross_1997", 37, "Frances Cairncross, in The Death of Distance", "1997",
         "distance would no longer decide the cost of communicating; location would cease to matter for most "
         "business decisions, and more people would work from home",
         "where economic activity locates once communication is nearly free",
         "the cost of communicating did collapse, and after 2020 about a quarter of paid working days in America "
         "were worked from home; but activity kept concentrating in large, expensive cities, whose wage premium "
         "grew, and face-to-face work in them survived the shift",
         "partly right",
         ("F. Cairncross, The Death of Distance: How the Communications Revolution Will Change Our Lives, Harvard "
          "Business School Press (1997)",
          "J. M. Barrero, N. Bloom and S. J. Davis, the work-from-home rate (SWAA), via FRED, series "
          "WFHCOVIDMATQUESTION",
          "E. Moretti, The New Geography of Jobs, Houghton Mifflin Harcourt (2012)")),
    Call("krugman_1995", 36, "Paul Krugman, in the Brookings Papers on Economic Activity", "1995",
         "trade with low-wage countries had only a modest effect on American wage inequality: about 3 percentage "
         "points on the ratio of skilled to unskilled wages, in line with the decade's other estimates",
         "the effect of trade with developing countries on US wages and jobs",
         "for the years he studied the estimate has held up, as Krugman himself later argued; but after 2000 "
         "imports from China grew far faster, and Autor, Dorn and Hanson (2013) found large, lasting losses of "
         "manufacturing jobs concentrated in the places that made the same goods, which aggregate models had "
         "averaged away",
         "partly right",
         ("P. R. Krugman, \"Growing World Trade: Causes and Consequences\", Brookings Papers on Economic Activity "
          "1995(1): 327-377",
          "P. R. Krugman, \"Trade and Wages, Reconsidered\", Brookings Papers on Economic Activity 2008(1): 103-154",
          "D. H. Autor, D. Dorn and G. H. Hanson, \"The China Syndrome\", American Economic Review 103(6): "
          "2121-2168 (2013)")),
    Call("heckscher_ohlin_us", 35, "Heckscher and Ohlin's theory, read for the United States", "1933",
         "the country best endowed with capital should export goods that use capital intensively and import goods "
         "that use labour intensively",
         "the most capital-abundant economy in the world after 1945, the United States",
         "Leontief's 1947 table found the reverse: a million dollars of exports needed $13,991 of capital per "
         "worker-year, import replacements $18,184; Leamer (1980) showed that with unbalanced trade this was the "
         "wrong test, and by the right one America was capital-abundant; Trefler (1995) found factor content far "
         "smaller than the theory predicts unless technology differs across countries",
         "partly right",
         ("B. Ohlin, Interregional and International Trade (Harvard University Press, 1933)",
          "W. Leontief, \"Domestic Production and Foreign Trade: The American Capital Position Re-examined\", "
          "Proceedings of the American Philosophical Society 97(4): 332-349 (1953)",
          "E. E. Leamer, \"The Leontief Paradox, Reconsidered\", Journal of Political Economy 88(3): 495-503 (1980)",
          "D. Trefler, \"The Case of the Missing Trade and Other Mysteries\", American Economic Review 85(5): "
          "1029-1046 (1995)")),
    Call("meese_rogoff_1983", 34, "Richard Meese and Kenneth Rogoff, in the Journal of International Economics",
         "February 1983",
         "the structural models of exchange rates of the 1970s forecast no better than a random walk at one to twelve "
         "months, even when given the actual future values of the variables they say drive the rate",
         "out-of-sample forecasts for the dollar against the mark, the yen and the pound, 1976-1981",
         "forty years on, this film's rerun for the pound, the yen, the Canadian dollar and the Swiss franc, "
         "1990-2026, finds interest parity and a fitted time-series model within half a percent of the random walk's "
         "error at one, three and twelve months; surveys since find that some models beat it at times, but not "
         "reliably out of sample",
         "right",
         ("R. A. Meese and K. Rogoff, \"Empirical Exchange Rate Models of the Seventies: Do They Fit Out of "
          "Sample?\", Journal of International Economics 14(1-2): 3-24 (1983)",
          "B. Rossi, \"Exchange Rate Predictability\", Journal of Economic Literature 51(4): 1063-1119 (2013)")),
    Call("rajan_2005", 33, "Raghuram Rajan, at the Federal Reserve Bank of Kansas City's Jackson Hole symposium",
         "August 2005",
         "financial development has made the world riskier in ways that are not appreciated: managers paid for "
         "returns relative to their peers are drawn to hide tail risks and to herd, and these behaviours can "
         "reinforce each other in a boom, creating a greater (albeit still small) probability of a catastrophic "
         "meltdown",
         "the incentives of intermediaries' managers, and the illiquidity of the markets they would all try to sell in "
         "at once",
         "three years later the system came close to the meltdown he described: tail risks written by AIG and held "
         "in banks' off-balance-sheet vehicles came due together, and the markets everyone relied on for liquidity "
         "froze; he did not name housing or a date, and the paper says more work was needed to size the risk",
         "right",
         ("R. G. Rajan, \"Has Financial Development Made the World Riskier?\", Proceedings of the Economic Policy "
          "Symposium, Jackson Hole (2005): 313-369; NBER Working Paper 11728",
          "Federal Reserve Bank of Minneapolis, The Region (December 2009), on the paper's reception")),
    Call("adwords_roi", 61, "Google's advice to AdWords advertisers on measuring their return, as quoted by Blake, "
         "Nosko and Tadelis", "2014",
         "determining your AdWords return can be a very straightforward process: take the revenue from sales made "
         "via your AdWords advertising, subtract the cost of the advertising, and divide by that cost",
         "every click on an ad, and every sale that follows it, is recorded, so the sales that come through the ads "
         "look like the sales the ads produced",
         "eBay's experiment: switching off non-brand paid search for 60 days in regions holding 30% of its American "
         "traffic cost almost "
         "no sales; the return was -63% (95% interval -124% to -3%), against over 1,400% from a regression of sales "
         "on spending; most of the sales through the ads came from regular buyers who would have bought anyway",
         "wrong",
         ("T. Blake, C. Nosko and S. Tadelis, \"Consumer Heterogeneity and Paid Search Effectiveness: A Large Scale "
          "Field Experiment\", NBER Working Paper 20171 (2014), section 6 and table 4; Econometrica 83(1): 155-174 "
          "(2015)",)),
    Call("peter_1969", 62, "Laurence J. Peter and Raymond Hull, The Peter Principle", "1969",
         "in a hierarchy every employee tends to rise to his level of incompetence",
         "people are promoted for doing their present job well, until they reach a job they do badly, where they "
         "stay, because nobody is promoted for doing a job badly",
         "Benson, Li and Shue's sales workers at 131 firms: firms do promote their best salespeople, who then make "
         "worse managers than colleagues who sold less; but firms limit the cost, giving sales less weight when the "
         "manager's job carries more responsibility",
         "partly right",
         ("L. J. Peter and R. Hull, The Peter Principle: Why Things Always Go Wrong (1969)",
          "A. Benson, D. Li and K. Shue, \"Promotions and the Peter Principle\", Quarterly Journal of Economics "
          "134(4): 2085-2134 (2019), abstract")),
    Call("granovetter_1973", 63, "Mark Granovetter, \"The Strength of Weak Ties\"", "1973",
         "weak ties are more likely than strong ones to carry news of a job you have not heard of",
         "people you see rarely move in other circles and know what your close friends already know you know; of 54 "
         "Boston-area professionals who found a job through a contact, 17% saw the contact often, 56% occasionally "
         "and 28% rarely",
         "Rajkumar, Saint-Jacques, Bojinov, Brynjolfsson and Aral used LinkedIn's randomized variation in suggested "
         "connections among 20 million people over five years: moderately weak ties raised job mobility the most, "
         "the strongest and the weakest the least, and weak ties mattered most in digital industries",
         "right",
         ("M. S. Granovetter, \"The Strength of Weak Ties\", American Journal of Sociology 78(6): 1360-1380 (1973)",
          "K. Rajkumar, G. Saint-Jacques, I. Bojinov, E. Brynjolfsson and S. Aral, \"A causal test of the strength "
          "of weak ties\", Science 377(6612): 1304-1310 (2022), abstract")),
    Call("meehl_1954", 64, "Paul E. Meehl, Clinical versus Statistical Prediction", "1954",
         "a simple statistical rule predicts as well as, or better than, the trained clinician's judgement",
         "in the studies he could find, mechanical combinations of a few facts matched or beat the experts who "
         "weighed the same facts in their heads, who are inconsistent and give weight to vivid details",
         "Grove, Zald, Lebow, Snitz and Nelson's meta-analysis of 136 studies: mechanical prediction was about 10% "
         "more accurate on average, substantially better in 33-47% of studies and substantially worse in 6-16%; "
         "Kleinberg et al.'s bail algorithm (2018) and later deployments extend the finding, with the caveat that "
         "experts sometimes see what the records do not",
         "right",
         ("P. E. Meehl, Clinical versus Statistical Prediction: A Theoretical Analysis and a Review of the Evidence "
          "(1954)",
          "W. M. Grove, D. H. Zald, B. S. Lebow, B. E. Snitz and C. Nelson, \"Clinical versus mechanical "
          "prediction: a meta-analysis\", Psychological Assessment 12(1): 19-30 (2000), abstract")),
]}
