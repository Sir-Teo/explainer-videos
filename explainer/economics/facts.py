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
