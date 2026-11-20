"""The Facts (videos/economics/README.md, "The devices"): about forty regularities, fixed for the whole series, that
any account of an economy has to reproduce.

Each fact has three columns on screen: **your guess** (asked before the others are shown), **the data** (from the
Data Room or a cited study) and **Agora** (what the built economy produces, filled in by the part that builds the
mechanism).  :data:`FACTS` lists them with the part that shows the data and the part that explains it; a part fills a
fact's ``agora`` column by entering a row in :data:`AGORA` (``{fact key: (part, result line)}``).  In the last part
Agora sits the whole list (:func:`scorecard`).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Fact:
    key: str
    group: str
    statement: str
    shown: int  # the part that shows the data
    explained: int  # the part that builds the mechanism
    source: str = ""  # the data or study behind it


GROUPS = ("households and firms", "markets", "growth", "cycles", "money and finance", "the world", "distribution")

FACTS = [
    # households and firms
    Fact("engel", "households and firms", "the poorer a household, the larger the share of its budget spent on food "
         "(Engel's law)", 6, 6, "Engel 1857; household budget surveys"),
    Fact("demand_slopes", "households and firms", "demand curves slope down, and the one known exception is rare",
         2, 6, "Jensen and Miller 2008"),
    Fact("smooth_consumption", "households and firms", "consumption is smoother than income", 22, 22, "BEA"),
    Fact("zipf_firms", "households and firms", "the sizes of firms follow Zipf's law", 43, 52, "Axtell 2001"),
    Fact("dispersion", "households and firms", "productivity differs about two to one among plants in one narrow "
         "industry", 43, 62, "Syverson 2011"),
    Fact("sticky_prices", "households and firms", "most prices change less than once a quarter", 30, 30,
         "Bils and Klenow 2004; Nakamura and Steinsson 2008"),
    # markets
    Fact("auctions_converge", "markets", "double auctions converge to the competitive price within a few periods",
         1, 2, "Smith 1962; Gode and Sunder 1993"),
    Fact("one_price", "markets", "the law of one price holds for gold and fails for haircuts", 9, 34,
         "Engel and Rogers 1996"),
    Fact("winners_curse", "markets", "winners of common-value auctions tend to overpay", 16, 16,
         "Capen, Clapp and Campbell 1971; Kagel and Levin"),
    Fact("passthrough", "markets", "cost changes pass through to prices incompletely", 10, 36, ""),
    # growth
    Fact("flat_for_millennia", "growth", "income per head was nearly flat for millennia, then rose without stopping",
         1, 19, "Maddison Project Database 2023"),
    Fact("kaldor", "growth", "output per worker grows at a roughly steady rate; capital per worker too; the return "
         "to capital and the shares of income are roughly stable (Kaldor's facts)", 3, 20, "Kaldor 1961"),
    Fact("conditional_convergence", "growth", "poor countries grow faster than rich ones once saving and schooling "
         "are held fixed, and not otherwise", 20, 20, "Barro 1991; Mankiw, Romer and Weil 1992"),
    Fact("labour_share", "growth", "the labour share was stable for decades, then fell in many countries", 3, 39,
         "Karabarbounis and Neiman 2014"),
    Fact("price_of_light", "growth", "the labour cost of light fell by a factor of hundreds of thousands", 21, 21,
         "Nordhaus 1996"),
    # cycles
    Fact("okun", "cycles", "a point of unemployment above normal goes with about two points of output below it",
         27, 27, "Okun 1962"),
    Fact("beveridge", "cycles", "vacancies and unemployment move in opposite directions (the Beveridge curve)", 24,
         24, "JOLTS"),
    Fact("volatility", "cycles", "investment is about three times as volatile as output; consumption less volatile",
         29, 29, "BEA"),
    Fact("hours", "cycles", "hours worked rise in booms and fall in recessions", 29, 29, "BLS"),
    Fact("hump", "cycles", "output's response to a monetary tightening is hump-shaped and peaks after a year or more",
         31, 30, "Christiano, Eichenbaum and Evans 1999"),
    Fact("persistence", "cycles", "inflation is persistent", 28, 30, "BLS"),
    Fact("asymmetry", "cycles", "expansions are long and recessions short", 27, 29, "NBER"),
    # money and finance
    Fact("quantity", "money and finance", "across countries and decades, inflation tracks money growth; over a year "
         "or two it does not", 25, 25, "IFS"),
    Fact("equity_premium", "money and finance", "stocks have paid several points a year more than bills", 23, 23,
         "Mehra and Prescott 1985"),
    Fact("unpredictable", "money and finance", "returns are hard to predict and their volatility is not", 23, 23,
         "Shiller 1981"),
    Fact("yield_curve", "money and finance", "the yield curve inverts before most recessions", 57, 31,
         "Estrella and Mishkin 1998"),
    Fact("credit_booms", "money and finance", "credit booms precede financial crises", 33, 33,
         "Schularick and Taylor 2012"),
    # the world
    Fact("gravity", "the world", "trade between two countries rises with their sizes and falls with the distance "
         "between them", 36, 36, "Tinbergen 1962; Head and Mayer 2014"),
    Fact("random_walk", "the world", "exchange rates are a random walk at short horizons and return toward "
         "purchasing power parity over years", 34, 34, "Meese and Rogoff 1983; Rogoff 1996"),
    Fact("intra_industry", "the world", "rich countries mostly trade similar goods with each other", 35, 36,
         "Grubel and Lloyd 1975"),
    Fact("few_exporters", "the world", "exporters are few, large and productive", 36, 36,
         "Bernard and Jensen 1995"),
    Fact("zipf_cities", "the world", "the sizes of cities follow Zipf's law", 37, 37, "Gabaix 1999"),
    # distribution
    Fact("mincer", "distribution", "log wages rise roughly linearly with years of schooling", 38, 38, "Mincer 1974"),
    Fact("pareto", "distribution", "top incomes and wealth have Pareto tails", 40, 40, "Piketty and Saez 2003"),
    Fact("gatsby", "distribution", "more unequal countries have less mobility between generations (the Great "
         "Gatsby curve)", 40, 40, "Corak 2013"),
    Fact("child_penalty", "distribution", "the gender gap in earnings opens at the birth of the first child", 39, 39,
         "Kleven, Landais and Sogaard 2019"),
]
BY_KEY = {f.key: f for f in FACTS}

# Agora's column: {fact key: (part, what the built economy produces)}.  Filled as parts land.
AGORA = {
    # Part 1 entered the row; Part 2 tested it on lopsided markets (Cliff and Bruten's question) and kept it
    "auctions_converge": (2, "traders who adjust their margins converge by the third period in balanced and lopsided "
                             "markets alike; random traders capture most of the surplus, but find the price only when "
                             "the market is balanced"),
    # Part 19 built the Malthusian economy and the unified growth toy
    "flat_for_millennia": (19, "with diminishing returns to land and a population that grows when income is above "
                               "subsistence, better technology raises population, not income; a unified model in which "
                               "technology's growth rises with population and parents switch to education when it is "
                               "fast enough stays flat for six centuries, then takes off around 1800"),
    # Part 20 built the Solow model
    "kaldor": (20, "the Solow model's balanced growth path has output and capital per worker growing at the rate of "
                   "technical progress, a constant capital-output ratio, a constant return to capital and constant "
                   "factor shares; it explains five of Kaldor's six facts and leaves the sixth, differences in growth "
                   "rates, to transitions and to differences in technology"),
    "conditional_convergence": (20, "a Solow economy below its own steady state grows faster the further below it is; "
                                    "across 89 countries, 1960-2019, holding investment, population growth and "
                                    "schooling fixed, the gap closes at about 1.3% a year, and with no controls not at "
                                    "all"),
    # Part 30 built sticky prices
    "sticky_prices": (30, "with Calvo pricing calibrated so that prices last three quarters on average (13% change "
                          "each month), the Island's prices follow a rise in money slowly: half has passed through "
                          "after 7 months; with menu costs and the same frequency, after 1, because the firms that "
                          "reprice are those furthest from their best price"),
    "hump": (30, "in the three-equation model a monetary tightening cuts output most at once; with habits (0.9), "
                 "price indexation (0.9) and a smoothed rule (0.8) the trough comes two quarters after the shock, still "
                 "sooner than in the data"),
    # Part 36 built the models of scale, firms and gravity
    "intra_industry": (36, "in Agora, two identical islands trade different varieties of the same good because of "
                           "love of variety and fixed costs, raising real wages 26%; America's two-way trade in "
                           "capital goods scores 0.77 on the Grubel-Lloyd index in 2025"),
    "gravity": (36, "in Agora, Eaton and Kortum's islands trade by a gravity formula; on CEPII's 2019 data trade "
                    "falls with distance with an elasticity of -1.18 by least squares and -0.71 by PPML with fixed "
                    "effects"),
    "few_exporters": (36, "in Agora, Melitz's firms: of 4,000 draws 260 survive, the most productive 19% export and "
                          "sell 67% of output, nine times the size of firms that sell only at home"),
    # Part 34 reran Meese and Rogoff and fitted the PPP half-life
    "random_walk": (34, "in Agora, overshooting makes the exchange rate jump 15% on a "
                        "10% rise in money because prices are sticky and asset markets are not; in the data, no "
                        "model beat the random walk at one to twelve months for four currencies since 1990, and real "
                        "exchange rates since 1870 lose half of a deviation in 5.2 years "
                        "(2.6 since 1973)"),
    # Part 33 built the amplification mechanisms and fitted the predictor
    "credit_booms": (33, "in Agora, credit amplifies: a 1% loss for farmers who borrow against land cuts their land "
                         "5.3% once the land price feeds back (0.67% if it did not), and leverage bought on the "
                         "optimists' beliefs makes a price fall from 0.95 to 0.69 on news worth 9%; in the data, a "
                         "crisis follows within three years in 18% of the fastest credit booms and 33% when house "
                         "prices boom too, against 6% after the slowest"),
    # Part 29 measured the US cycle (1948-2019) and simulated the real business cycle model
    "volatility": (29, "in a growth model with random technology, consumption smoothing and capital's long life make "
                       "investment swing and consumption hold steady: in the Island's real business cycle investment is "
                       "3.2 times as volatile as output and consumption 0.29 times; in US data, 1948-2019, investment "
                       "is 4.6 times and consumption (durables included) 0.77 times"),
    "hours": (29, "in the model, hours rise in booms because a temporary rise in productivity makes this the time to "
                  "work; with Hansen's indivisible labour hours are 0.76 times as volatile as output, against 0.90 in "
                  "the data, but they move almost one for one with productivity (correlation 0.76) where the data "
                  "show none (-0.07)"),
    # Part 27 measured Okun's law against the CBO's potential and built the Keynesian economy
    "okun": (27, "when spending, not capacity, sets output, firms hire and lay off with demand, so unemployment rises "
                 "as output falls below potential; against the CBO's potential, 1949-2025, the unemployment gap moves "
                 "0.62 points per point of the output gap (R-squared 0.78): about one and a half points of output per "
                 "point of unemployment, against Okun's three and Ball, Leigh and Loungani's two"),
    # Part 25 drew the world's money and inflation and built Cagan's economy
    "quantity": (25, "with velocity steady and output growing for its own reasons, inflation is money growth less output "
                     "growth; across 146 countries' averages for 1990-2024 the slope is 0.96 (0.98 net of output "
                     "growth), while year by year the correlation is only 0.28, because velocity and output move and "
                     "prices adjust slowly"),
    # Part 24 drew the JOLTS curve and built the labour market with frictions
    "beveridge": (24, "workers and jobs meet through a matching function with constant returns, so unemployment and "
                      "vacancies coexist in a steady state; productivity moves the economy along a downward-sloping "
                      "curve (the Island: 3.5% unemployment and 6.6% vacancies), and worse matching shifts the curve "
                      "out; with Shimer's calibration, though, tightness moves only 1.7% per 1% of productivity, "
                      "against about 25 in the data"),
    # Part 23 computed the premium from Shiller's data and built the trees
    "equity_premium": (23, "the premium is risk aversion times an asset's covariance with bad times; with consumption "
                           "as smooth as the data show, power utility gives at most a third of a point at sensible "
                           "risk aversion (Mehra and Prescott's economy, solved), and the Hansen-Jagannathan bound needs "
                           "a risk aversion above eight; rare disasters (a 1.7% chance a year of a fall averaging 30%) "
                           "give a 5% premium and a 2% safe rate with a risk aversion of 3.5"),
    "unpredictable": (23, "in an efficient market prices use what is known, so next year's return is hard to "
                          "forecast (an R-squared of 0.03 on the dividend yield in Shiller's data); a risk premium "
                          "that rises in bad times, as with habits, makes returns over a decade partly forecastable "
                          "(0.24) without leaving money on the table"),
    # Part 22 showed the US series and built the households
    "smooth_consumption": (22, "a household that can save and borrow spreads a windfall over the rest of its life, "
                               "so its spending follows permanent income, not this year's; even Agora's buffer-stock "
                               "households, who hold little cash, spend only about a quarter of a month's windfall "
                               "within the year; in US data from 1960 to 2019, spending on nondurables and services "
                               "grew with half the quarterly volatility of disposable income"),
    # Part 21 showed Nordhaus's table and built the idea economy
    "price_of_light": (21, "an idea, once found, can be used by everyone at once, so its cost is paid once and its "
                           "benefit grows with the number who use it; in Romer's economy ideas accumulate without "
                           "diminishing returns and the cost of a unit of anything made with them falls for ever, "
                           "as the labour cost of light fell about 45,000-fold from the tallow candle to the compact "
                           "fluorescent bulb"),
    # Part 16 showed the jar of coins and explained it
    "winners_curse": (16, "bidders who bid their own unbiased estimates of a common value lose, on average, the "
                          "expected overestimate of the highest of n estimates, which grows with n (a third of the "
                          "noise's half-width with 2 bidders, 94 percent of it with 32); shading by that much removes "
                          "the loss"),
}


def scorecard() -> list[dict]:
    """Every fact with its Agora column (empty where no part has filled it yet)."""
    return [{"key": f.key, "group": f.group, "statement": f.statement, "shown": f.shown, "explained": f.explained,
             "agora": AGORA.get(f.key)} for f in FACTS]
