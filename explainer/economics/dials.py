"""The Dials (videos/economics/SYLLABUS.md, section 2.5): the numbers economics runs on, each with the range of its
estimates, how each estimate was identified, and the date the row was last checked.

"Economics runs on perhaps sixty numbers."  Each is a :class:`Dial`: the quantity and its units, the parts that use
it, and its :class:`Estimate` rows (author, year, design, sample, the estimate with its interval, where it was read,
the date it was checked).  A dial's status is one of :data:`STATUSES`.  On screen a *dial card* shows the estimates
as ticks on one axis, coloured by design (``explainer.economics.style.DESIGN_COLOR``).

The name is Hayek's (1945): the price system "enables individual producers to watch merely the movement of a few
pointers, as an engineer might watch the hands of a few dials".

The gate (``tools/check_dials.py econN``, as *Psychology, Built*'s Ledger gate): every estimate a part shows has a
row here, or the part declares in :data:`SHOWN` why it has none (a single study shown as an example, a number the
part computes itself, a row that a later part enters).
"""

from __future__ import annotations

from dataclasses import dataclass, field

STATUSES = ("settled within a range", "depends on the setting", "contested", "not identified")
DESIGNS = ("RCT", "IV", "RD", "DiD", "event study", "structural", "calibration", "survey", "narrative", "lab",
           "meta-analysis", "review", "regression")


@dataclass(frozen=True)
class Estimate:
    who: str
    year: int
    design: str
    sample: str
    value: float
    lo: float | None = None
    hi: float | None = None
    where: str = ""
    checked: str = ""


@dataclass(frozen=True)
class Dial:
    key: str
    name: str
    units: str
    parts: tuple  # the parts that enter or use it
    status: str = "not identified"
    estimates: tuple = field(default_factory=tuple)
    meaning: str = ""  # what changes in policy across the range
    checked: str = ""

    def __post_init__(self):
        assert self.status in STATUSES, self.status
        for e in self.estimates:
            assert e.design in DESIGNS, e.design


# The dials, as the plan lists them.  Rows are entered by the part that first measures each (its frontier sweep
# sets the status and the date); until then a dial has no estimates and is drawn empty, with the part that fills it.
DIALS = {d.key: d for d in [
    Dial("elasticity_staples", "price elasticity of demand for staples", "percent change in quantity per percent "
         "change in price", (2, 6), status="depends on the setting", checked="2026-11-19",
         meaning="below one in size for every staple measured in a market: a tax on any of them raises revenue and "
                 "cuts consumption a little, and how little decides whether it is a revenue tax or a health policy; "
                 "but for households poor enough to live on one staple, a dearer staple can mean more of it (Hunan's "
                 "rice), so a price subsidy meant to feed them can leave them eating less",
         estimates=(
             Estimate("Havranek, Irsova and Janda", 2012, "meta-analysis", "gasoline, short run: published "
                      "estimates, corrected for publication bias", -0.09, where="Energy Economics 34(1): 201-207, "
                      "abstract", checked="2026-11-18"),
             Estimate("Havranek, Irsova and Janda", 2012, "meta-analysis", "gasoline, long run: the same meta-analysis",
                      -0.31, where="Energy Economics 34(1): 201-207, abstract", checked="2026-11-18"),
             Estimate("Gallet and List", 2003, "meta-analysis", "cigarettes: mean of 523 estimates from 86 studies",
                      -0.48, where="Health Economics 12(10): 821-835; the mean as reported by Tobacco in Australia, "
                      "section 13.1 (Cancer Council Victoria)", checked="2026-11-18"),
             Estimate("Wagenaar, Salois and Komro", 2009, "meta-analysis", "beer: simple mean of 105 estimates",
                      -0.46, where="Addiction 104: 179-190 (accepted manuscript, Results)", checked="2026-11-18"),
             Estimate("Wagenaar, Salois and Komro", 2009, "meta-analysis", "wine: simple mean of 93 estimates",
                      -0.69, where="as above", checked="2026-11-18"),
             Estimate("Wagenaar, Salois and Komro", 2009, "meta-analysis", "spirits: simple mean of 103 estimates",
                      -0.80, where="as above", checked="2026-11-18"),
             Estimate("Jensen and Miller", 2008, "RCT", "rice, Hunan's urban poor: all 1,258 household changes",
                      0.224, 0.224 - 1.96 * 0.149, 0.224 + 1.96 * 0.149, where="AER 98(4), table 3, column 1",
                      checked="2026-11-19"),
             Estimate("Jensen and Miller", 2008, "RCT", "rice, Hunan: households with rice under 80% of calories",
                      0.451, 0.451 - 1.96 * 0.170, 0.451 + 1.96 * 0.170, where="AER 98(4), table 3, column 3",
                      checked="2026-11-19"),
             Estimate("Jensen and Miller", 2008, "RCT", "rice, Hunan: households with rice over 80% of calories",
                      -0.61, -0.61 - 1.96 * 0.296, -0.61 + 1.96 * 0.296, where="AER 98(4), table 3, column 5",
                      checked="2026-11-19"),
         )),
    Dial("cpi_bias", "measurement bias of the consumer price index", "percentage points a year by which the CPI "
         "overstates the rise in the cost of living", (3, 6, 28), status="settled within a range",
         checked="2026-11-19",
         meaning="pensions, tax brackets and many wages are indexed to the CPI: at 1 point a year an indexed payment "
                 "gains about a tenth in real terms over a decade, and the Boskin Commission put the cost to the "
                 "federal debt of 1997-2008 at about a trillion dollars; at 0.3 the drift is small",
         estimates=(
             Estimate("Boskin, Dulberger, Gordon, Griliches and Jorgenson", 1996, "review", "the CPI-U in 1995-96: "
                      "substitution 0.40, outlets 0.10, new products and quality 0.60", 1.10, 0.80, 1.60,
                      where="final report, p. 44, as tabulated by Moulton (2018), table 5, and Gordon (2006), table 1",
                      checked="2026-11-19"),
             Estimate("Lebow and Rudd", 2003, "review", "the CPI-U after the reforms of 1995-2002", 0.87, 0.30, 1.40,
                      where="Journal of Economic Literature 41(1): 159-201, p. 161 (via Moulton 2018, table 5); the "
                      "abstract rounds to 0.9", checked="2026-11-19"),
             Estimate("Gordon", 2006, "review", "the CPI-U in 1995-96, revisited: more upper-level substitution, "
                      "less quality bias", 1.25, 1.2, 1.3, where="NBER Working Paper 12311, abstract",
                      checked="2026-11-19"),
             Estimate("Gordon", 2006, "review", "the CPI-U in 2006, before new products and longevity", 0.8,
                      where="NBER Working Paper 12311, abstract", checked="2026-11-19"),
             Estimate("Moulton", 2018, "review", "the CPI-U in 2017", 0.85, 0.30, 1.40,
                      where="Brookings (July 2018), table 5", checked="2026-11-19"),
             Estimate("Hamilton", 2001, "regression", "food Engel curves in the PSID, 1974-91", 1.6,
                      where="AER 91(3): 619-630, as reported by Costa (2001), pp. 1305-1306", checked="2026-11-19"),
             Estimate("Costa", 2001, "regression", "food Engel curves in the Consumer Expenditure Surveys, 1972-94",
                      1.6, where="JPE 109(6), section VI", checked="2026-11-19"),
             Estimate("Costa", 2001, "regression", "food Engel curves, 1888-1919", -0.1, where="JPE 109(6), abstract",
                      checked="2026-11-19"),
             Estimate("Costa", 2001, "regression", "food Engel curves, 1919-35", 0.7, where="JPE 109(6), abstract",
                      checked="2026-11-19"),
         )),
    Dial("eis", "elasticity of intertemporal substitution", "percent change in consumption growth per percentage "
         "point of the real interest rate", (7, 22, 23), status="contested", checked="2026-11-19",
         meaning="near zero in aggregate data, about a third for stockholders and near one for bondholders, about two "
                 "from tax variation, and 1.5 or more in the calibrations of asset pricing; it decides how much "
                 "saving responds to interest rates and to taxes on interest, and how strongly a change in the "
                 "central bank's rate moves spending",
         estimates=(
             Estimate("Hall", 1988, "IV", "US aggregate consumption, twentieth century: \"no strong evidence\" that "
                      "it is positive", 0.0, where="JPE 96(2): 339-357, abstract", checked="2026-11-19"),
             Estimate("Barsky, Juster, Kimball and Shapiro", 1997, "survey", "HRS respondents: hypothetical choices "
                      "between consumption paths, mean", 0.2, where="QJE 112(2), abstract (NBER WP 5213)",
                      checked="2026-11-19"),
             Estimate("Vissing-Jorgensen", 2002, "IV", "US stockholders, Consumer Expenditure Survey", 0.35, 0.3, 0.4,
                      where="JPE 110(4): 825-853, abstract", checked="2026-11-19"),
             Estimate("Vissing-Jorgensen", 2002, "IV", "US bondholders, Consumer Expenditure Survey", 0.9, 0.8, 1.0,
                      where="JPE 110(4): 825-853, abstract", checked="2026-11-19"),
             Estimate("Gruber", 2013, "IV", "variation in after-tax interest rates across households, CEX, two "
                      "decades", 2.0, where="Quarterly Journal of Finance 3(1); NBER WP 11945, abstract",
                      checked="2026-11-19"),
             Estimate("Havranek", 2015, "meta-analysis", "2,735 estimates in 169 studies, corrected for selective "
                      "reporting: macro data", 0.0, where="JEEA 13(6): 1180-1204, abstract", checked="2026-11-19"),
             Estimate("Havranek", 2015, "meta-analysis", "the same, corrected: micro data on asset holders", 0.35,
                      0.3, 0.4, where="JEEA 13(6): 1180-1204, abstract", checked="2026-11-19"),
             Estimate("Bansal and Yaron", 2004, "calibration", "long-run risks: the value asset prices need", 1.5,
                      where="Journal of Finance 59(4): 1481-1509, abstract", checked="2026-11-19"),
         )),
    Dial("risk_aversion", "relative risk aversion", "the percentage fall in marginal utility per percent rise in "
         "consumption", (7, 22, 23), status="contested", checked="2026-11-19",
         meaning="about one when read from consumption or labour supply, two to seven in finance's estimates, four "
                 "from survey gambles over lifetime income, ten in the calibrations that fit asset prices; laboratory "
                 "choices over a few dollars give a fraction of one, which expected utility cannot square with the "
                 "rest (Rabin 2000).  How much insurance, how safe a pension, how large a precautionary buffer, and "
                 "how big the welfare cost of business cycles all move with it",
         estimates=(
             Estimate("Holt and Laury", 2002, "lab", "real stakes of a few dollars: 5.2 safe choices, its CRRA "
                      "interval", 0.28, 0.15, 0.41, where="AER 92(5), via Holt and Laury (2005), table 1; the "
                      "interval computed for five safe choices", checked="2026-11-19"),
             Estimate("Holt and Laury", 2002, "lab", "stakes times 90: 7.2 safe choices, its CRRA interval", 0.83,
                      0.68, 0.97, where="as above; the interval for seven safe choices", checked="2026-11-19"),
             Estimate("Chetty", 2006, "structural", "labour supply: wage and income elasticities from 33 studies, "
                      "mean", 1.0, where="AER 96(5): 1821-1834, abstract; NBER WP 12067", checked="2026-11-19"),
             Estimate("Elminejad, Havranek and Irsova", 2025, "meta-analysis", "1,021 Euler-equation estimates in 92 "
                      "studies: economics, corrected for publication bias", 1.0,
                      where="Journal of Economic Surveys 39(5): 2315-2333, abstract; IES WP 2022/14",
                      checked="2026-11-19"),
             Estimate("Elminejad, Havranek and Irsova", 2025, "meta-analysis", "the same: finance, corrected", 4.5,
                      2.0, 7.0, where="as above", checked="2026-11-19"),
             Estimate("Elminejad, Havranek and Irsova", 2025, "meta-analysis", "the same: the median reported "
                      "estimate", 3.77, where="IES WP 2022/14, table 1", checked="2026-11-19"),
             Estimate("Barsky, Juster, Kimball and Shapiro", 1997, "survey", "HRS respondents' gambles over lifetime "
                      "income: one over the mean risk tolerance (0.25)", 4.0, where="QJE 112(2), abstract (NBER WP "
                      "5213)", checked="2026-11-19"),
             Estimate("Elminejad, Havranek and Irsova", 2025, "calibration", "446 calibrations in 200 studies: the "
                      "median", 6.0, where="IES WP 2022/14, table 1", checked="2026-11-19"),
             Estimate("Bansal and Yaron", 2004, "calibration", "long-run risks: the value asset prices need", 10.0,
                      where="Journal of Finance 59(4): 1481-1509, abstract", checked="2026-11-19"),
         )),
    Dial("capital_share", "output elasticity of capital", "percent change in output per percent change in capital "
         "(capital's share of income, under competition)", (8, 20), status="settled within a range",
         checked="2026-11-19",
         meaning="about a quarter to a third: under competition and constant returns it is capital's share of income, "
                 "and most measurements put labour's share at two thirds to four fifths; it sets how fast growth "
                 "from saving runs into diminishing returns (Part 20), but the labour share has fallen since the "
                 "1980s, so the number is not a constant of nature",
         estimates=(
             Estimate("Cobb and Douglas", 1928, "regression", "US manufacturing, 1899-1922, constant returns imposed "
                      "(their table, refitted)", 0.25, where="AER 18(1) suppl.; the data via Felipe and Adams (2005), "
                      "table 1, fitted on screen", checked="2026-11-19"),
             Estimate("Felipe and Adams", 2005, "regression", "the same data, unrestricted", 0.233,
                      where="Eastern Economic Journal 31(3), table 2", checked="2026-11-19"),
             Estimate("Gollin", 2002, "review", "labour shares adjusted for self-employment, most countries: one "
                      "minus 0.65-0.80", 0.275, 0.20, 0.35, where="JPE 110(2): 458-474, abstract",
                      checked="2026-11-19"),
             Estimate("Feenstra, Inklaar and Timmer (Penn World Table)", 2015, "survey", "the United States, "
                      "1950-1999: one minus the mean labour share", 0.375, where="PWT via FRED (LABSHPUSA156NRUG), "
                      "computed on screen", checked="2026-11-19"),
         )),
    Dial("kl_substitution", "elasticity of substitution between capital and labour", "percent change in the "
         "capital-labour ratio per percent change in the wage relative to the rental of capital", (8, 20),
         status="contested", checked="2026-11-19",
         meaning="below one in most evidence, about a half: then capital and labour are complements, cheaper capital "
                 "raises labour's share, and Cobb-Douglas (exactly one) is the wrong benchmark; above one, as one "
                 "influential estimate has it, cheaper machines explain part of labour's falling share",
         estimates=(
             Estimate("Chirinko", 2008, "review", "the weight of the evidence, after 75 years of estimates", 0.5, 0.4,
                      0.6, where="Journal of Macroeconomics 30(2): 671-686, abstract", checked="2026-11-19"),
             Estimate("Gechert, Havranek, Irsova and Kolcunova", 2022, "meta-analysis", "3,186 estimates in 121 "
                      "studies: the mean as reported", 0.9, where="Review of Economic Dynamics 45: 55-82, abstract",
                      checked="2026-11-19"),
             Estimate("Gechert, Havranek, Irsova and Kolcunova", 2022, "meta-analysis", "the same, corrected for "
                      "publication bias and method choices", 0.3, where="as above", checked="2026-11-19"),
             Estimate("Oberfield and Raval", 2021, "structural", "US manufacturing plants aggregated, long run, "
                      "1970-2007", 0.6, 0.5, 0.7, where="Econometrica 89(2): 703-732, abstract",
                      checked="2026-11-19"),
             Estimate("Karabarbounis and Neiman", 2014, "regression", "across countries: labour shares against the "
                      "relative price of investment goods", 1.25, where="QJE 129(1); NBER WP 19136, abstract",
                      checked="2026-11-19"),
         )),
    Dial("misallocation", "TFP gain from equalizing marginal products across plants", "percent rise in "
         "manufacturing TFP if capital and labour were moved until marginal products were equal (or as equal as in "
         "the United States)", (9, 21), status="contested", checked="2026-11-19",
         meaning="the first welfare theorem says competitive markets equalize marginal products; measured gaps across "
                 "plants imply large losses where they are unequal (tens of percent of manufacturing TFP in China "
                 "and India), but measurement error inflates measured gaps: one correction cuts the potential gains "
                 "by a fifth in India and three fifths in the United States (Bils, Klenow and Ruane)",
         estimates=(
             Estimate("Hsieh and Klenow", 2009, "structural", "China, 2005: moving to the United States' dispersion "
                      "of 1997", 30.5, where="QJE 124(4), table 6 (accepted version)", checked="2026-11-19"),
             Estimate("Hsieh and Klenow", 2009, "structural", "India, 1994: moving to the United States' dispersion "
                      "of 1997", 59.2, where="as above, table 6", checked="2026-11-19"),
             Estimate("Hsieh and Klenow", 2009, "structural", "the United States, 1997: full equalization within "
                      "industries", 42.9, where="as above, table 4", checked="2026-11-19"),
             Estimate("Hsieh and Klenow", 2009, "structural", "China, 2005: full equalization within industries",
                      86.6, where="as above, table 4", checked="2026-11-19"),
             Estimate("Hsieh and Klenow", 2009, "structural", "India, 1994: full equalization within industries",
                      127.5, where="as above, table 4", checked="2026-11-19"),
         )),
    Dial("markups", "markups over marginal cost", "price over marginal cost", (10, 43), status="contested",
         checked="2026-11-19",
         meaning="the production approach finds the average American public firm's markup rising from about 1.2 in "
                 "1980 to about 1.6 by 2016, with the median unchanged and the rise at the top; others find it much "
                 "flatter once all costs and all firms are counted (Traina 2018: flat or falling once public firms "
                 "are reweighted to represent the economy), so how much market power has grown is open",
         estimates=(
             Estimate("De Loecker, Eeckhout and Unger", 2020, "structural", "US public firms, sales-weighted mean, "
                      "1980", 1.21, where="QJE 135(2): 561-644, abstract", checked="2026-11-19"),
             Estimate("De Loecker, Eeckhout and Unger", 2020, "structural", "the same, 2016", 1.61,
                      where="as above", checked="2026-11-19"),
         )),
    Dial("reasoning_depth", "depth of strategic reasoning", "average steps of thinking (the cognitive hierarchy's "
         "tau)", (11, 45), status="depends on the setting", checked="2026-11-19",
         meaning="people typically think one or two steps ahead of a naive player, not the infinitely many steps that "
                 "equilibrium assumes; newspaper readers with time to think, and players with experience, go deeper, "
                 "so how far reasoning goes depends on the setting, and first-time play is better predicted by levels "
                 "of thinking than by equilibrium",
         estimates=(
             Estimate("Camerer, Ho and Chong", 2004, "structural", "nearly 100 games: values from 1 to 2, typically "
                      "1.5", 1.5, 1.0, 2.0, where="QJE 119(3): 861-898, abstract and conclusion", checked="2026-11-19"),
             Estimate("Nagel", 1995, "lab", "first round of two-thirds of the average, 67 students: the tau whose mean "
                      "is 36.73 (Agora's fit)", 1.12, where="AER 85(5), Figure 1B; tau fitted in Agora",
                      checked="2026-11-19"),
             Estimate("Thaler (Financial Times)", 1997, "structural", "newspaper readers, two-thirds of the average: "
                      "the tau whose mean is 18.9 (Agora's fit)", 4.07, where="the reported mean; tau fitted in Agora",
                      checked="2026-11-19"),
         )),
    Dial("cartel_overcharge", "cartel overcharge", "percent by which a cartel's price exceeds the price without it",
         (12, 59), status="contested", checked="2026-11-19",
         meaning="a cartel that is caught has typically raised prices by something between a sixth and a quarter; "
                 "the low end argues for fines and damages of a few times the overcharge, the high end for more, and "
                 "whether the estimates in the literature are biased upward is itself the dispute",
         estimates=(
             Estimate("Connor", 2014, "review", "hundreds of cartels' published overcharge estimates: the long-run "
                      "median (the mean is at least 49 percent)", 23.0, where="Research in Law and Economics 26, "
                      "abstract", checked="2026-11-19"),
             Estimate("Boyer and Kotchoni", 2015, "meta-analysis", "Connor's database, corrected for estimation, "
                      "publication and endogeneity biases: the median (the mean 15.47)", 16.01,
                      where="Review of Industrial Organization 47(2), abstract", checked="2026-11-19"),
             Estimate("Connor", 1998, "narrative", "the lysine cartel of 1992-95, from the overcharge on direct "
                      "buyers ($65-140 million) and sales ($495-550 million)", 20.0, 12.0, 28.0,
                      where="Choices 13(3), p. 17", checked="2026-11-19"),
         )),
    Dial("selection_cost", "welfare cost of adverse selection", "percent of the money at stake (each study's own "
         "measure)", (13, 42), status="depends on the setting", checked="2026-11-19",
         meaning="in employer health plans, adverse selection costs a few percent of what is at stake, small enough "
                 "that subsidies to fix it can cost more than they save; where selection is stronger, as in individual "
                 "markets, mandates gain more; and making people choose better can make selection worse",
         estimates=(
             Estimate("Einav, Finkelstein and Cullen", 2010, "structural", "Alcoa's employees: $9.55 a year each, as "
                      "a share of the surplus at stake from efficient pricing", 3.0, where="NBER WP 14414, section "
                      "4.3", checked="2026-11-19"),
             Estimate("Cutler and Reber", 1998, "structural", "Harvard's employees after the 1995 reform, as a share "
                      "of baseline spending", 3.0, 2.0, 4.0, where="QJE 113(2), abstract", checked="2026-11-19"),
             Estimate("Hackmann, Kolstad and Kowalski", 2015, "structural", "Massachusetts's individual market: the "
                      "gain per person from the mandate's reduction in selection", 4.1, where="AER 105(3), abstract",
                      checked="2026-11-19"),
         )),
    Dial("piece_rate_response", "output response to piece rates", "percent rise in output per worker when pay "
         "follows output", (14, 62), status="settled within a range", checked="2026-11-19",
         meaning="paying for output raises it by something like a fifth to a half where output is easy to measure "
                 "and one person's work is their own; part of the rise is who the job attracts, and where work is "
                 "shared or hard to measure the response can be smaller, or perverse",
         estimates=(
             Estimate("Lazear", 2000, "DiD", "Safelite's windshield installers, hourly wages to piece rates (about half "
                      "from sorting; the working paper: 20 to 36)", 44.0, where="AER 90(5); NBER WP 5672",
                      checked="2026-11-19"),
             Estimate("Shearer", 2004, "RCT", "tree planters in British Columbia, piece rates against fixed wages",
                      20.0, where="REStud 71(2), abstract", checked="2026-11-19"),
             Estimate("Bandiera, Barankay and Rasul", 2005, "DiD", "fruit pickers, piece rates against relative "
                      "incentives (at least)", 50.0, where="QJE 120(3), abstract", checked="2026-11-19"),
         )),
    Dial("road_traffic", "traffic's response to roads", "percent rise in vehicle-kilometres travelled for a 1% rise "
         "in lane-kilometres (an elasticity)", (15, 37), status="settled within a range", checked="2026-11-19",
         meaning="in US cities, driving on interstate highways rises about in proportion to their lane kilometres: "
                 "new roads fill, and building them does not relieve congestion; a price on the road does",
         estimates=(
             Estimate("Duranton and Turner", 2011, "regression", "US metropolitan areas, 1983-2003, pooled OLS with "
                      "population and geography (their preferred OLS)", 0.86, where="AER 101(6), Table 3",
                      checked="2026-11-19"),
             Estimate("Duranton and Turner", 2011, "IV", "the same areas, lane kilometres instrumented by 1835 "
                      "exploration routes, 1898 railroads and the 1947 interstate plan", 1.03, 0.81, 1.25,
                      where="AER 101(6), Table 5, panel A, column 3 (standard error about 0.11)",
                      checked="2026-11-19"),
         )),
    Dial("reserve_revenue", "what a reserve price adds", "proportional change in an auction's revenue from setting "
         "reserve prices by Myerson's rule (from a low uniform floor)", (16, 61), status="depends on the setting",
         checked="2026-11-19",
         meaning="in Yahoo!'s sponsored-search auctions, reserves set by the theory raised revenue where many "
                 "advertisers bid on frequently searched words, and lowered it on rarely searched ones, where they "
                 "drove bidders away; a few percent overall, worth hundreds of millions of dollars a year",
         estimates=(
             Estimate("Ostrovsky and Schwarz", 2009, "RCT", "Yahoo! keywords, 438,632 treated and 23,016 "
                      "controls, difference in differences at fixed search volumes", 0.0271, 0.0159, 0.0383,
                      where="working paper, Table 4 (t = 4.73)", checked="2026-11-19"),
             Estimate("Ostrovsky and Schwarz", 2009, "RCT", "the same, keywords searched fewer than 10 times a "
                      "day", -0.0219, -0.0401, -0.0037, where="Table 5 (t = -2.36)", checked="2026-11-19"),
             Estimate("Ostrovsky and Schwarz", 2009, "RCT", "the same, keywords searched 10 or more times a day "
                      "(74 percent of searches)", 0.0330, 0.0051, 0.0609, where="Table 6 (t = 2.32)",
                      checked="2026-11-19"),
         )),
    Dial("return_schooling", "return to a year of school", "proportional rise in earnings per year of schooling",
         (4, 38), status="settled within a range", checked="2026-11-19",
         meaning="a year of school raises earnings by roughly 6 to 15 percent, a return few investments match; "
                 "the instruments' estimates sit at or above the regressions', which says less ability bias than "
                 "feared, and that the people an instrument moves gain more than the average",
         estimates=(
             Estimate("Angrist and Krueger", 1991, "IV", "US men born 1920-29: quarter of birth", 0.101, 0.036, 0.166,
                      where="Card (2001), Econometrica 69(5), table 2", checked="2026-11-19"),
             Estimate("Angrist and Krueger", 1991, "regression", "US men born 1920-29: OLS on the same data", 0.07,
                      where="Card (2001), table 2", checked="2026-11-19"),
             Estimate("Angrist and Krueger", 1991, "IV", "US men born 1930-39: quarter of birth", 0.06, 0.001, 0.119,
                      where="Card (2001), Econometrica 69(5), table 2", checked="2026-11-19"),
             Estimate("Angrist and Krueger", 1991, "regression", "US men born 1930-39: OLS on the same data", 0.063,
                      where="Card (2001), table 2", checked="2026-11-19"),
             Estimate("Angrist and Krueger", 1991, "IV", "US men born 1940-49: quarter of birth", 0.078, 0.019, 0.137,
                      where="Card (2001), Econometrica 69(5), table 2", checked="2026-11-19"),
             Estimate("Angrist and Krueger", 1991, "regression", "US men born 1940-49: OLS on the same data", 0.052,
                      where="Card (2001), table 2", checked="2026-11-19"),
             Estimate("Staiger and Stock", 1997, "IV", "US men born 1930-39: quarter of birth by state, LIML", 0.098, 0.069, 0.127,
                      where="Card (2001), Econometrica 69(5), table 2", checked="2026-11-19"),
             Estimate("Staiger and Stock", 1997, "regression", "US men born 1930-39: OLS on the same data", 0.063,
                      where="Card (2001), table 2", checked="2026-11-19"),
             Estimate("Kane and Rouse", 1993, "IV", "US women: tuition and distance to college", 0.091, 0.026, 0.156,
                      where="Card (2001), Econometrica 69(5), table 2", checked="2026-11-19"),
             Estimate("Kane and Rouse", 1993, "regression", "US women: OLS on the same data", 0.08,
                      where="Card (2001), table 2", checked="2026-11-19"),
             Estimate("Card", 1995, "IV", "US men: a four-year college nearby", 0.132, 0.036, 0.228,
                      where="Card (2001), Econometrica 69(5), table 2", checked="2026-11-19"),
             Estimate("Card", 1995, "regression", "US men: OLS on the same data", 0.073,
                      where="Card (2001), table 2", checked="2026-11-19"),
             Estimate("Conneely and Uusitalo", 1997, "IV", "Finnish men: growing up in a university town", 0.11, 0.063, 0.157,
                      where="Card (2001), Econometrica 69(5), table 2", checked="2026-11-19"),
             Estimate("Conneely and Uusitalo", 1997, "regression", "Finnish men: OLS on the same data", 0.085,
                      where="Card (2001), table 2", checked="2026-11-19"),
             Estimate("Harmon and Walker", 1995, "IV", "British men: changes in the school-leaving age", 0.153, 0.124, 0.182,
                      where="Card (2001), Econometrica 69(5), table 2", checked="2026-11-19"),
             Estimate("Harmon and Walker", 1995, "regression", "British men: OLS on the same data", 0.061,
                      where="Card (2001), table 2", checked="2026-11-19"),
             Estimate("Lemieux and Card", 1998, "IV", "Ontario men: the veterans' education programme", 0.164, 0.06, 0.268,
                      where="Card (2001), Econometrica 69(5), table 2", checked="2026-11-19"),
             Estimate("Lemieux and Card", 1998, "regression", "Ontario men: OLS on the same data", 0.07,
                      where="Card (2001), table 2", checked="2026-11-19"),
             Estimate("Maluccio", 1997, "IV", "rural Philippines: distance to a high school", 0.145, 0.065, 0.225,
                      where="Card (2001), Econometrica 69(5), table 2", checked="2026-11-19"),
             Estimate("Maluccio", 1997, "regression", "rural Philippines: OLS on the same data", 0.073,
                      where="Card (2001), table 2", checked="2026-11-19"),
             Estimate("Duflo", 1999, "IV", "Indonesia: the school-building programme", 0.064, 0.015, 0.113,
                      where="Card (2001), Econometrica 69(5), table 2", checked="2026-11-19"),
             Estimate("Duflo", 1999, "regression", "Indonesia: OLS on the same data", 0.078,
                      where="Card (2001), table 2", checked="2026-11-19"),
         )),
    Dial("labour_supply", "elasticity of labour supply (Hicksian, Frisch, extensive)", "", (38, 41)),
    Dial("minimum_wage", "employment effect of the minimum wage", "own-wage elasticity of employment", (38,)),
    Dial("skill_substitution", "elasticity of substitution between skilled and unskilled labour", "", (39,)),
    Dial("ige", "intergenerational elasticity of income", "", (40,)),
    Dial("eti", "elasticity of taxable income", "", (41,)),
    Dial("ui_duration", "duration elasticity of unemployment benefits", "", (42,)),
    Dial("mpc", "marginal propensity to consume out of a windfall", "share spent within a quarter", (22,)),
    Dial("matching", "elasticity of matches to unemployment", "", (24,)),
    Dial("price_frequency", "frequency of price changes", "share of prices changing per month", (30,)),
    Dial("phillips_slope", "slope of the Phillips curve", "points of inflation per point of slack", (28, 30)),
    Dial("sacrifice", "sacrifice ratio", "point-years of output per point of disinflation", (28,)),
    Dial("money_demand", "interest semi-elasticity of money demand", "", (25,)),
    Dial("monetary_shock", "effect of a 100-basis-point tightening on output and prices", "percent at the peak",
         (31, 55)),
    Dial("multipliers", "government-spending and tax multipliers", "dollars of output per dollar", (32,)),
    Dial("neutral_rate", "neutral real interest rate", "percent", (31,)),
    Dial("trade_elasticity", "trade elasticity", "", (36,)),
    Dial("passthrough", "pass-through of tariffs and exchange rates to prices", "share", (34, 36, 66)),
    Dial("agglomeration", "agglomeration elasticity", "percent productivity per doubling of density", (37,)),
    Dial("housing_supply", "elasticity of housing supply", "", (37,)),
    Dial("return_capital_poor", "return to capital for small firms in poor countries", "percent a month", (46,)),
    Dial("vsl", "value of a statistical life", "millions of dollars", (18, 58)),
    Dial("discount", "social discount rate and the social cost of carbon", "percent a year; dollars per tonne",
         (48, 58)),
    Dial("energy_elasticity", "price elasticity of gasoline and of electricity", "", (48,)),
    Dial("loss_present", "loss aversion and present bias", "", (45,)),
    Dial("genai_productivity", "productivity effect of generative AI on a task", "percent", (65,)),
    Dial("consistency", "consistency of choices with utility maximization", "Afriat's critical cost efficiency "
         "index: the share of each budget a person's choices keep once all revealed-preference contradictions are "
         "removed (1 = perfectly consistent)", (5, 45), status="settled within a range", checked="2026-11-19",
         meaning="most people, children included, choose far more consistently than chance; how consistently varies, "
                 "with income, education and age, and the variation goes with wealth; with too few or too similar "
                 "budgets the test has no power, so a score is read against random choosers on the same budgets",
         estimates=(
             Estimate("Harbaugh, Krause and Berry", 2001, "lab", "7-year-olds (31), 11 sets of chips and juice", 0.93,
                      where="AER 91(5), table 1 (Afriat's index)", checked="2026-11-19"),
             Estimate("Harbaugh, Krause and Berry", 2001, "lab", "11-year-olds (42), the same 11 sets", 0.96,
                      where="AER 91(5), table 1", checked="2026-11-19"),
             Estimate("Harbaugh, Krause and Berry", 2001, "lab", "undergraduates (55), the same 11 sets", 0.94,
                      where="AER 91(5), table 1", checked="2026-11-19"),
             Estimate("Choi, Fisman, Gale and Kariv", 2007, "lab", "93 Berkeley students and staff, 50 budgets", 0.954,
                      where="AER 97(5), as reported by Choi et al. (2014), footnote 5", checked="2026-11-19"),
             Estimate("Choi, Kariv, Mueller and Silverman", 2014, "survey", "1,182 Dutch adults (CentERpanel), 25 "
                      "budgets, online", 0.881, where="AER 104(6), section II", checked="2026-11-19"),
             Estimate("Chen, Liu, Shan and Zhong", 2023, "lab", "their human subjects, food budgets", 0.963,
                      where="arXiv 2305.12763v3, section 3", checked="2026-11-19"),
         )),
    Dial("engel_food", "income elasticity of spending on food", "percent change in food spending per percent "
         "change in income (or total spending)", (6, 46), status="depends on the setting", checked="2026-11-19",
         meaning="below one wherever it has been measured (Engel's law), and falling as countries grow richer: "
                 "food's share is a measure of living standards, and an Engel curve that shifts over time can be "
                 "read as a check on the price index (Hamilton 2001; Costa 2001)",
         estimates=(
             Estimate("Houthakker", 1957, "regression", "about 40 household surveys in 30 countries: \"one would not "
                      "be very far astray\"", 0.6, where="Econometrica 25(4), as quoted by Anker (2011), PERI WP 247, "
                      "p. 3", checked="2026-11-19"),
             Estimate("Seale and Regmi", 2006, "structural", "low-income countries", 0.7,
                      where="Review of Income and Wealth 52(4), as summarized by Anker (2011), p. 3",
                      checked="2026-11-19"),
             Estimate("Seale and Regmi", 2006, "structural", "lower-middle-income countries", 0.6, where="as above",
                      checked="2026-11-19"),
             Estimate("Seale and Regmi", 2006, "structural", "upper-middle-income countries", 0.5, where="as above",
                      checked="2026-11-19"),
             Estimate("Seale and Regmi", 2006, "structural", "high-income countries", 0.2, 0.1, 0.3,
                      where="as above", checked="2026-11-19"),
         )),
]}

# What each part shows without entering a row, and why: {part: [(what is shown, the reason)]}
SHOWN = {
    1: [
        ("Gneezy and Rustichini (2000), the day-care fine", "one field experiment, shown as an example of an "
         "incentive that backfires; its record (a survey-based study did not find the same effect) is entered with "
         "the behavioural dials in Part 45"),
        ("Smith (1962) and Chamberlin (1948)", "laboratory designs, shown for what they did, not for an estimate; "
         "the double auction's convergence is a Fact, and Part 2 measures it"),
        ("the Survey of Professional Forecasters, 2008", "a forecast scored against the outcome: a Called-it card "
         "(explainer.economics.calls), not an estimate of a parameter"),
        ("the Maddison Project Database and FRED", "data, shown with their sources; no parameter is estimated"),
    ],
    2: [
        ("Smith's double auction (1956-62) and Cliff and Bruten (1997)", "laboratory and simulation designs shown for "
         "what they found about convergence: the Fact of the double auction, not an estimate of a parameter"),
        ("Chetty, Looney and Kroft (2009); Kopczuk, Marion, Muehlegger and Slemrod (2016)", "two studies shown as "
         "exceptions to tax-collection invariance; their estimates enter the public-finance dials in Part 41"),
        ("Glaeser and Luttmer (2003); Deacon and Sonstelie (1985); Diamond, McQuade and Qian (2019)", "evidence on "
         "price controls, shown for its direction; rent control's supply response enters the housing-supply dial in "
         "Part 37"),
        ("Calvano and others (2020); Assad, Clark, Ershov and Xu (2024)", "the frontier chapter's evidence on "
         "algorithmic pricing; markups enter their dial in Part 10"),
        ("the Pink Sheet and PSD coffee data, and the frost's rough elasticity", "data, and a back-of-the-envelope "
         "calculation with its caveats stated; not an entry in the staples dial"),
    ],
    3: [
        ("National Income, 1929-32 (Kuznets, 1934) and Petty's Verbum Sapienti (1665)", "historical accounts, "
         "transcribed in data.tables and shown as history, not as estimates of a parameter"),
        ("Bridgman, Dugan, Lal, Osborne and Villones (2012); the ILO (2018); Brynjolfsson, Collis and Eggers (2019)",
         "measurements of what GDP leaves out (home production, informal work, free goods), shown for their size; "
         "no dial measures them"),
        ("Deaton and Heston (2010); Balassa (1964) and Samuelson (1964)", "a revision of purchasing power parities "
         "and the theory of the Penn effect; the WDI data are shown, no parameter is estimated"),
        ("Piketty, Saez and Zucman (2018); Auten and Splinter (2024)", "distributional national accounts, shown as "
         "a measurement dispute; the inequality dials enter in Part 40"),
        ("Leontief (1936)", "the input-output method, applied to the Island's simulated table"),
        ("Nordhaus and Tobin (1972); the HDI (UNDP); Jones and Klenow (2016)", "measures beyond GDP, shown for what "
         "they find; no dial is a welfare measure"),
        ("Corrado, Hulten and Sichel (2009); Henderson, Storeygard and Weil (2012); Martinez (2022)", "the frontier "
         "chapter's evidence on intangibles and on night lights, shown for direction and size"),
        ("FRED's national accounts, unemployment and price series; WDI; the HDR; the Philadelphia Fed's real-time "
         "data; the Penn World Table's labour share", "data, shown with their sources; Kaldor's facts and the "
         "labour share are entered in explainer.economics.facts"),
    ],
    4: [
        ("Moore (1914); Wright (1915, 1928); Working (1927); Haavelmo (1944)", "history of the identification problem, "
         "transcribed or paraphrased with sources; their estimates are shown as what went wrong or what was "
         "invented, not as entries in a dial"),
        ("Leamer (1983); LaLonde (1986); Dehejia and Wahba (1999)", "a test of methods against an experiment: the "
         "Called-it card lalonde_1986 records it; training programmes' effects enter the labour-market dials in "
         "Part 38"),
        ("Angrist (1990), the veterans' earnings", "a natural experiment shown as an instrument; the effect of "
         "military service is not a dial"),
        ("Card and Krueger (1994)", "the border design, shown as a design; its estimate enters the minimum-wage "
         "employment dial in Part 38, with the replies"),
        ("Angrist and Krueger (1991) and the other studies of Card (2001), table 2", "entered in the "
         "return_schooling dial (this part)"),
        ("Imbens and Angrist (1994); Bound, Jaeger and Baker (1995); Staiger and Stock (1997); Deaton, Imbens and "
         "Heckman (2010); Chetty (2009); Nakamura and Steinsson (2018); Lucas (1976)", "methods and arguments, "
         "shown for what they say; no parameter is estimated"),
        ("the negative income tax experiments (Munnell, ed., 1986); PROGRESA (Schultz 2004; Skoufias 2005)",
         "experiments shown for their design and the direction of their findings; labour-supply elasticities "
         "enter their dial in Part 38 and conditional transfers in Part 46"),
        ("Samuelson and Solow (1960); Friedman (1968); Phelps (1967)", "the Phillips curve's history, shown with "
         "FRED's data; its slope enters the Phillips-curve dial in Part 28"),
        ("Crepon et al. (2013); Egger et al. (2022); Muralidharan, Niehaus and Sukhtankar (2023)", "the frontier "
         "chapter's evidence on spillovers, shown for direction and size; the transfer multiplier enters the "
         "development dials in Part 46"),
        ("the 1969 draft lottery (Selective Service, JSE archive); FRED's unemployment rate and CPI", "data, shown "
         "with their sources; no parameter is estimated"),
    ],
    5: [
        ("Jevons (1871), Edgeworth (1881), Pareto (1906), Hicks and Allen (1934), Samuelson (1938), Houthakker (1950), "
         "Debreu (1954), Afriat (1967), Varian (1982)", "the theory's history, shown as history; no parameter is "
         "estimated"),
        ("Andreoni and Miller (2002); Chen, Lakshminarayanan and Santos (2006); Kagel, Battalio and Green (1995)",
         "experiments shown for what they show about consistency (and altruism); the share consistent, not a dial's "
         "row, since their designs and indices differ"),
        ("Saez (2010)", "bunching at the EITC's first kink, shown with simulated earners; the elasticity of reported "
         "earnings enters the taxable-income dial in Part 41"),
        ("Becker (1962)", "a thought experiment, simulated on the Island"),
        ("Blundell, Browning and Crawford (2008); Bronars (1987)", "methods, shown for what they do"),
        ("McFadden's BART forecast", "a Called-it card (explainer.economics.calls), not an estimate of a parameter"),
        ("Chen, Liu, Shan and Zhong (2023), GPT", "a language model's choices, shown at the frontier; the dial is "
         "about people"),
        ("Dean and Martin (2016); Echenique, Lee and Shum (2011); Kitamura and Stoye (2018); McFadden (1974); Block "
         "and Marschak (1960)", "the frontier chapter's methods and evidence, shown for what they do"),
        ("BEA's personal consumption expenditures by type of product, 1929-2025 (FRED)", "data, with GARP and its "
         "power computed; no parameter is estimated"),
    ],
    6: [
        ("Marshall (1895); Stigler (1947, 1987); Rosen (1999); Slutsky (1915) and its rediscovery; Hicks and Allen "
         "(1934); Antonelli (1886); Konus (1924); Hicks (1940); Engel (1857) in Zimmerman's translation",
         "the theory's history, shown as history; no parameter is estimated"),
        ("Jensen and Miller (2008): the inverted U across staple calorie shares, the meat response and Gansu",
         "shown with the study; its rice elasticities are entered in the elasticity_staples dial (this part)"),
        ("Hausman (1997), Apple-Cinnamon Cheerios", "one new good's value, shown as an example of a virtual price; "
         "new goods' share of CPI bias is in the cpi_bias dial's Boskin row"),
        ("Willig (1976); Hausman (1981); Deaton and Muellbauer (1980); Stone (1954); Gorman (1953); Working (1943) "
         "and Leser (1963); Blundell and Robin (1999); Ramsey (1927); Deaton (1989)", "methods, shown for what they "
         "do (Deaton and Muellbauer's rejection of homogeneity is reported as a finding about a method)"),
        ("the BLS's geometric means (1999) and chained CPI (2002)", "how the official index allows for "
         "substitution; no parameter is estimated"),
        ("Jaravel (2019); Jaravel and Lashkari (2024); Feenstra (1994); Redding and Weinstein (2020); Atkin, Faber, "
         "Fally and Gonzalez-Navarro (2024)", "the frontier chapter's evidence and methods, shown for direction and "
         "size; inflation by income group enters the inflation dials in Part 28"),
        ("USDA ERS's food spending by income quintile, 2024; BEA's personal consumption expenditures by type of "
         "product, 1929-2025 (FRED)", "data, shown with their sources; the elasticities drawn from them are "
         "computed on screen and labelled as such"),
    ],
    7: [
        ("Nicolaus Bernoulli (1713), Cramer (1728), Daniel Bernoulli (1738); Fisher (1930); Samuelson (1937); "
         "Koopmans (1960); von Neumann and Morgenstern (1944); Savage (1954); Allais (1953); Ellsberg (1961)",
         "the theory's history, shown as history; no parameter is estimated"),
        ("Arrow (1965); Pratt (1964); Mossin (1968); Merton (1969); Rothschild and Stiglitz (1970); Machina (1982); "
         "Chew's weighted utility; Kreps and Porteus (1978); Epstein and Zin (1989); Strotz (1955-56); Pollak "
         "(1968); Laibson (1997); Gilboa and Schmeidler (1989); Klibanoff, Marinacci and Mukerji (2005); Hansen and "
         "Sargent (2001, 2008); Manski (2004)", "methods and models, shown for what they do"),
        ("Kahneman and Tversky (1979); Tversky and Kahneman (1992)", "prospect theory in one card; loss aversion "
         "and probability weighting enter the loss_present dial in Part 45"),
        ("Rabin (2000); Rabin and Thaler (2001)", "a theorem: its tables are transcribed, and the CRRA calibration "
         "is computed on screen"),
        ("Thaler (1981); Imai, Rutter and Camerer (2021)", "evidence on present bias, shown for its direction; "
         "present bias enters the loss_present dial in Part 45"),
        ("Hayden and Platt (2009)", "bids for the St Petersburg game: a Called-it card "
         "(explainer.economics.calls), not an estimate of a parameter"),
        ("Post, van den Assem, Baltussen and Thaler (2008); Sydnor (2010)", "evidence on risk taking in a game show "
         "and in deductibles, shown for its direction; the deductible's implied aversion is computed on "
         "illustrative numbers"),
        ("Mehra and Prescott (1985); Weil (1989)", "the equity premium and risk-free rate puzzles, stated; asset "
         "pricing takes them up in Part 23"),
        ("Madrian and Shea (2001); Thaler and Benartzi (2004)", "pension design, shown for what happened; default "
         "effects enter the behavioural dials in Part 45"),
        ("FRED's real consumption, PCE prices and Treasury bill rate, 1934-2025", "data: Hall's regression is "
         "computed on screen and labelled as such, not entered as a row"),
    ],
    8: [
        ("Cobb and Douglas (1928), via Felipe and Adams (2005)", "data: the 1899-1922 table is transcribed and the "
         "regressions are refitted on screen; the constant-returns fit enters the capital_share dial"),
        ("Penn World Table's US labour share, via FRED", "data: plotted as a series; its mean enters the "
         "capital_share dial as one minus the labour share"),
        ("Hall and Hitch (1939); Alchian (1950); Friedman (1953)", "the marginalist controversy, shown as history; "
         "Alchian's argument is simulated on the Island, not estimated"),
        ("Coase (1937); Williamson (1975, 1985); Klein, Crawford and Alchian (1978); Grossman and Hart (1986); "
         "Hart and Moore (1990)", "theories of the firm, shown for what they say; hold-up and ownership are computed "
         "in Agora's models"),
        ("Coase (2000); Klein (2000); Freeland (2000); Casadesus-Masanell and Spulber (2000)", "the dispute over "
         "Fisher Body, shown as a dispute; no number is estimated"),
        ("Chenery (1949); Williams (1947); Wright (1936)", "engineering rules (pipelines, the six-tenths rule, the "
         "learning curve), shown with illustrative numbers"),
        ("Haskel and Westlake (2018); Corrado, Hulten and Sichel (2009)", "intangible capital, shown for its "
         "properties"),
        ("Brynjolfsson, Li and Raymond (2025)", "one firm's AI rollout, shown as a study card for its direction; "
         "Part 65 returns to it"),
        ("Shahidi, Rusak, Manning, Fradkin and Horton (2025)", "a working paper's argument about AI agents and "
         "transaction costs, stated as an open question"),
    ],
    9: [
        ("Radford (1945)", "the camp economy, told from the article itself (a transcribed table); its salmon is one "
         "column of the law-of-one-price Fact"),
        ("Edgeworth (1881); Walras (1874); Arrow and Debreu (1954); McKenzie (1954); Debreu (1959); Debreu and Scarf "
         "(1963); Aumann (1964); Arrow (1953)", "the theory's history and theorems, shown as such; every number about "
         "them is computed in Agora"),
        ("Arrow, Block and Hurwicz (1959); Scarf (1960, 1967); Anderson, Plott, Shimomura and Granat (2004)",
         "stability and computation: Scarf's economy is simulated; the laboratory study is shown for its direction"),
        ("Sonnenschein (1973); Mantel (1974); Debreu (1974); Kirman (1992); Brown and Matzkin (1996)",
         "theorems and arguments, stated; the three-equilibrium economy is computed"),
        ("Mises (1920); Lange (1936-37); Hayek (1945); Kantorovich (1939); Koopmans", "the calculation debate, shown "
         "as history; Kantorovich's method is run on the Island's machines"),
        ("Bils, Klenow and Ruane (2021)", "a correction to the misallocation dial's rows, stated in its meaning and on "
         "screen, not entered as a row (it is a share of the gains, not a gain)"),
        ("Kehoe (2005, 2014); USITC (1992)", "the 1992 NAFTA forecasts: a Called-it card (explainer.economics.calls), "
         "and Kehoe's table transcribed"),
        ("Papadimitriou (1994); Daskalakis, Goldberg and Papadimitriou (2009); Chen and Deng; Chen, Dai, Du and Teng "
         "(2009); Shapley and Scarf (1974); Roth (1982); Budish (2011); Budish, Cachon, Kessler and Othman (2017)",
         "the frontier, stated; the housing market is solved in Agora on the Island's huts"),
        ("Brent and WTI via FRED; the World Bank's WDI (2023)", "data for the law-of-one-price Fact and the "
         "intermission, computed on screen, not entered as dial rows"),
    ],
    10: [
        ("Dupuit (1844, 1849); Pigou (1920); Robinson (1933); Lerner (1934)", "the theory's history, told from the "
         "texts (the 1849 passage paraphrased); every number about it is computed in Agora"),
        ("Harberger (1954); Posner (1975); Tullock (1967)", "the cost of monopoly: Harberger's total is stated as "
         "history, Posner's argument as an argument; the ferry's triangle and rectangle are computed"),
        ("Schmalensee (1981); Varian (1985); Mussa and Rosen (1978); Deneckere and McAfee (1996); Oi (1971); "
         "Stigler (1963); Adams and Yellen (1976)", "theorems and cases, stated; each is computed on the Island"),
        ("Coase (1972); Stokey (1981); Bulow (1982, 1986); Gul, Sonnenschein and Wilson (1986)", "the Coase "
         "conjecture, stated; its equilibrium is solved in Agora"),
        ("Ramsey (1927); Boiteux (1956); Averch and Johnson (1962); Littlechild (1983); Littlewood (1972)",
         "rules and regulation, stated; Ramsey prices, the Averch-Johnson firm and Littlewood's rule are computed"),
        ("Nakamura and Zerom (2010)", "a structural decomposition of coffee's pass-through, shown beside the "
         "incomplete-pass-through Fact (a transcribed abstract); not a dial"),
        ("Hall (1988); De Loecker and Warzynski (2012)", "the production approach to markups, checked in Agora; "
         "its estimates enter the markups dial through De Loecker, Eeckhout and Unger"),
        ("Traina (2018)", "a challenge to the markups dial's rows, stated in its meaning and on screen; it reports no "
         "single markup to enter as a row"),
        ("Dube and Misra (2023); Calvano, Calzolari, Denicolo and Pastorello (2020); Assad, Clark, Ershov and Xu "
         "(2024)", "the frontier, stated from the papers' abstracts; the personalized-pricing experiment is rerun in "
         "Agora"),
        ("ground coffee (BLS via FRED) and arabica (the Pink Sheet)", "data for the pass-through Fact and the "
         "intermission, computed on screen, not entered as dial rows"),
    ],
    11: [
        ("Flood (1952); Nash (1950, 1951); von Neumann (1928); Tucker", "the history of the prisoner's dilemma and of "
         "equilibrium, told from the sources (the joint outcomes via Poundstone's account, a transcribed table)"),
        ("Gibbons (1992); Schelling (1960); Selten (1965, 1978); Harsanyi (1967-68); Aumann (1974); Rubinstein (1982)",
         "theory and examples, stated; every game shown is solved in Agora"),
        ("Chiappori, Levitt and Groseclose (2002); Palacios-Huerta (2003); Walker and Wooders (2001)", "tests of mixed "
         "strategies, shown for their findings; no parameter is estimated, so no dial"),
        ("Rosenthal (1981); McKelvey and Palfrey (1992); Guth, Schmittberger and Schwarze (1982); Henrich et al. "
         "(2001)", "experiments on backward induction and fairness, shown for their direction and range (Henrich's a "
         "transcribed table); fairness enters a dial in Part 45"),
        ("Friedman (1971); Fudenberg and Maskin (1986); Kreps, Milgrom, Roberts and Wilson (1982); Selten and "
         "Stoecker (1986); Axelrod (1980); Nowak and Sigmund (1993)", "repetition and cooperation: theorems and "
         "tournaments, stated; Axelrod's tournament is rerun in Agora"),
        ("Maynard Smith and Price (1973); Sinervo and Lively (1996); Brown (1951); Robinson (1951); Shapley (1964); "
         "Stahl and Wilson (1994)", "evolution and learning, stated; the dynamics are computed"),
        ("Keynes (1936)", "the beauty contest, quoted as the idea behind the depth-of-reasoning dial"),
        ("Schelling and Halperin (1961); Hart and Mas-Colell (2000); Bowling et al. (2015); Brown and Sandholm (2018, "
         "2019); Erev and Roth (1998); Camerer and Ho (1999)", "practice and the frontier, stated from the sources; "
         "regret matching is run in Agora"),
        ("nuclear warhead stockpiles (FAS via Our World in Data)", "data for the intermission and the arms-control "
         "section, shown as history, not entered as dial rows"),
    ],    12: [
        ("Cournot (1838); Bertrand (1883); Edgeworth (1897); Kreps and Scheinkman (1983); Hotelling (1929); Salop "
         "(1979); Chamberlin (1933); Dixit and Stiglitz (1977); von Stackelberg (1934); Dixit (1980); Fudenberg and "
         "Tirole (1984)", "theory, stated; every model is solved in Agora"),
        ("Stigler (1964); Friedman (1971); Green and Porter (1984); Porter (1983); Ellison (1994)", "collusion: "
         "theory and the railroad cartel's history, stated; the price wars are simulated in Agora"),
        ("Borenstein, Cameron and Gilbert (1997)", "rockets and feathers, stated as their finding with weekly data; "
         "the intermission's monthly BLS and EIA prices are checked in Agora and shown not to resolve it"),
        ("Salant, Switzer and Reynolds (1983); Farrell and Shapiro (1990); Williamson (1968); the Merger Guidelines",
         "mergers: theorems and thresholds (the guidelines a transcribed table); the merger paradox is computed"),
        ("Baumol, Panzar and Willig (1982); McGee (1958); Milgrom and Roberts (1982); Kreps and Wilson (1982)",
         "contestability, limit pricing and predation, stated"),
        ("Azar, Schmalz and Tecu (2018); O'Brien and Salop (2000); Calvano et al. (2020); Assad et al. (2024)",
         "the frontier, stated with its dispute; the modified HHI is computed, no estimate is entered as a dial row"),
    ],    13: [
        ("Akerlof (1970); Spence (1973); Rothschild and Stiglitz (1976); Stiglitz and Weiss (1981); Cho and Kreps "
         "(1987)", "theory, stated; every model is solved in Agora on the Island"),
        ("Cutler and Zeckhauser (1998)", "Harvard's death spiral, shown from their figures (a transcribed table); "
         "Cutler and Reber's welfare loss is a dial row"),
        ("Tyler, Murnane and Willett (2000)", "the GED's signalling value, shown for its finding; not a dial"),
        ("Chiappori and Salanié (2000); Finkelstein and McGarry (2006)", "tests for private information, shown for "
         "their findings; the test is run on simulated drivers in Agora"),
        ("Cabral and Hortaçsu (2010)", "eBay's feedback, shown for its direction; the reputation model is Agora's"),
        ("Handel (2013)", "inertia and selection, stated as the frontier's counterpoint; not entered as a row"),
        ("the CPI for used and new vehicles (BLS via FRED)", "data for the intermission, shown as history"),
    ],    14: [
        ("Alchian and Demsetz (1972); Holmström (1979, 1982, 1999); Holmström and Milgrom (1987, 1991); Lazear and "
         "Rosen (1981); Weitzman (1980); Shapiro and Stiglitz (1984); Stiglitz (1974); Grossman and Hart (1986)",
         "theory, stated; every model is solved in Agora"),
        ("Xiaogang (1978)", "history, told qualitatively: accounts of the 1979 harvest disagree, so no number is shown"),
        ("Raff and Summers (1987); Lin (1992)", "cases shown for their findings (a transcribed table)"),
        ("Jacob and Levitt (2003)", "multitasking's evidence, the Called it? outcome"),
        ("Gneezy and Rustichini (2000); Bénabou and Tirole (2003)", "crowding out: the day-care data of Part 1 "
         "replotted; theory stated"),
        ("Prendergast (1999, 2002)", "a survey and its explanation of the risk-incentive puzzle, stated for direction"),
        ("Bertrand and Mullainathan (2001); Jensen and Murphy (1990); Hall and Liebman (1998)", "executive pay: "
         "findings stated (pay for luck; $3.25 per $1,000; stock and options); the pay-performance link enters a "
         "dial in Part 62"),
        ("Ehrenberg and Bognanno (1990); Brown, Harlow and Starks (1996); Lazear (1989)", "tournament evidence, "
         "stated for direction"),
        ("Gibbons and Murphy (1992); Laffont and Tirole (1993)", "career concerns' evidence and the theory of "
         "regulation, stated"),
        ("Akerlof (1982); Fehr, Kirchsteiger and Riedl (1993); Gneezy and List (2006)", "gift exchange in the "
         "laboratory and the field, stated for direction"),
        ("Shaban (1987); Banerjee, Gertler and Ghatak (2002)", "sharecropping's evidence (a transcribed table, "
         "data.tables.TENANCY)"),
        ("Frey and Oberholzer-Gee (1997)", "a survey's acceptance rates, transcribed (data.tables.CROWDING)"),
        ("Kerr (1975); Brickley and Dark (1987)", "an essay and a franchising study, stated for direction"),
        ("Baker, Gibbons and Murphy (2002); Levin (2003); Gibbons and Henderson (2013)", "relational contracts: "
         "theory, solved in Agora"),
        ("Amodei and Clark (2016); Krakovna et al. (2020); Hadfield-Menell and Hadfield (2019); Gao, Schulman and "
         "Hilton (2023)", "incentives for machines: an example, a catalogue, an argument and the shape of a fitted "
         "curve, drawn with illustrative constants"),
    ],
    15: [
        ("Meade (1952); Pigou (1920); Coase (1960, 1974); Samuelson (1954); Lindahl (1919); Gordon (1954); Hardin "
         "(1968); Dales (1968); Weitzman (1974); Vickrey (1969)", "theory, stated; every model is solved in Agora "
         "(Coase's own table is transcribed, data.tables.COASE_1960)"),
        ("Cheung (1973)", "the beekeepers' rents, transcribed (data.tables.CHEUNG_1973): a market for a spillover, "
         "shown for what it prices"),
        ("Fehr and Gächter (2000); Ledyard (1995); Fischbacher, Gächter and Fehr (2001)", "laboratory public-goods "
         "games, stated for direction; the dynamics drawn are Agora's typed players"),
        ("Ostrom (1990); the northern cod moratorium (1992)", "governed and ungoverned commons, told as history"),
        ("Schmalensee and Stavins (2013); Portney (1990)", "the SO2 market's record, transcribed "
         "(data.tables.ACID_RAIN), and the Called it? outcome"),
        ("the Stockholm trial (2006); Currie and Walker (2011)", "a congestion charge and the damage of congestion, "
         "transcribed (data.tables.ROADS, CURRIE_WALKER_2011); the elasticity of congestion enters a dial in Part 37"),
        ("Katz and Shapiro (1985); David (1985); Jaffe, Trajtenberg and Henderson (1993)", "network externalities and "
         "knowledge spillovers, stated for direction; their dials are in Parts 21 and 44"),
        ("CEDS sulphur dioxide via Our World in Data", "data, shown with its source; no parameter is estimated"),
    ],
    16: [
        ("Vickrey (1961); Myerson (1981); Riley and Samuelson (1981); Milgrom and Weber (1982); Bulow and Klemperer "
         "(1996); Edelman, Ostrovsky and Schwarz (2007); Varian (2007)", "theory, stated; every format, reserve and "
         "equilibrium is computed in Agora (agora.auctions)"),
        ("Cox, Smith and Walker (1988); Kagel, Harstad and Levin (1987); Kagel and Levin (1993)", "laboratory "
         "bidding, stated for direction (bids above the risk-neutral equilibrium in first-price auctions, above value "
         "in second-price ones)"),
        ("Capen, Clapp and Campbell (1971); Bazerman and Samuelson (1983)", "the winner's curse: the oil engineers' "
         "argument told as history, the jar of coins transcribed (data.tables.BAZERMAN_SAMUELSON_1983)"),
        ("Binmore and Klemperer (2002); Klemperer (2002); Cramton and Schwartz (2000)", "the spectrum auctions, "
         "transcribed (data.tables.UK_3G_2000, EURO_3G_2000, COLLUSION_SIGNALS) and the Called it? outcome"),
        ("Garbade and Ingber (2005); Malvey and Archibald (1998)", "the Treasury's change of format, transcribed "
         "(data.tables.TREASURY_FORMAT); its evidence was inconclusive, so it is told, not dialled"),
        ("the FCC's incentive auction (2017)", "totals, transcribed (data.tables.INCENTIVE_AUCTION)"),
        ("FRED: the 3-month Treasury bill rate", "data, shown with its source; no parameter is estimated"),
    ],
}


def board(parts=None) -> list[dict]:
    """The dials (all, or those used by ``parts``), each with its status and the part that first fills it."""
    out = []
    for d in DIALS.values():
        if parts and not set(parts) & set(d.parts):
            continue
        out.append({"key": d.key, "name": d.name, "first": min(d.parts), "status": d.status,
                    "n": len(d.estimates)})
    return sorted(out, key=lambda r: r["first"])
