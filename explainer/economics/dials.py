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
           "meta-analysis", "review", "regression", "reconstruction")


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
         "point of the real interest rate", (7, 22, 23, 51), status="contested", checked="2026-11-19",
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
         "consumption", (7, 22, 23, 54), status="contested", checked="2026-11-19",
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
             Estimate("this film (Hansen-Jagannathan bound)", 2026, "calibration", "power utility on Shiller's "
                      "1889-2009 stocks and consumption: the least risk aversion that meets the bound", 8.2,
                      where="videos/economics/econ23/compute.py, hj", checked="2026-11-20"),
             Estimate("this film (consumption CAPM)", 2026, "calibration", "the premium over its covariance with "
                      "consumption growth, Shiller's data 1889-1978", 12.3,
                      where="videos/economics/econ23/compute.py, ccapm", checked="2026-11-20"),
             Estimate("this film (rare disasters)", 2026, "calibration", "the Island's disasters (1.7% a year, "
                      "average fall 30%): the risk aversion that gives a 5% premium", 3.5,
                      where="videos/economics/econ23/compute.py, disasters", checked="2026-11-20"),
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
             Estimate("Mankiw, Romer and Weil", 1992, "regression", "98 non-oil countries, income in 1985 on saving, "
                      "population growth and schooling: the augmented Solow model's physical-capital share (a "
                      "human-capital share of 0.28 beside it)", 0.31, 0.23, 0.39,
                      where="QJE 107(2): 407-437, table II (restricted regression, s.e. 0.04)", checked="2026-11-19"),
         )),
    Dial("social_return_rd", "social rate of return to R&D", "percent a year: the return to society of a dollar of "
         "R&D, counting what it does for other firms (and against it)", (21, 44, 66), status="settled within a range",
         checked="2026-11-20",
         meaning="large: estimates of the social return run from about 30% to nearly 60% a year, two to four times "
                 "the private return, because the ideas one firm finds spill over to others more than its "
                 "business-stealing takes from rivals; so the market does too little research, and the case for "
                 "subsidies and public science rests on the gap, not on the level",
         estimates=(
             Estimate("Jones and Williams", 1998, "calibration", "the US economy: a growth model's lower bound on "
                      "the social return, the conservative value used to find optimal R&D at two to four times "
                      "actual", 30.0, where="QJE 113(4): 1119-1135; Federal Reserve FEDS 1997-12 (the 30% value), "
                      "abstract (two to four times)", checked="2026-11-20"),
             Estimate("Bloom, Schankerman and Van Reenen", 2013, "regression", "US firms 1981-2001, technology "
                      "spillovers net of product-market rivalry, baseline (private return 21%)", 55.0,
                      where="Econometrica 81(4): 1347-1393; the March 2012 version's introduction gives 55% and 21%",
                      checked="2026-11-20"),
             Estimate("Lucking, Bloom and Van Reenen", 2019, "regression", "US firms over three decades, marginal "
                      "social return (private return 14%)", 58.0,
                      where="Fiscal Studies 40(4): 561-590, section on returns", checked="2026-11-20"),
         )),
    Dial("investment_user_cost", "investment's response to the user cost of capital", "elasticity of investment "
         "(or the capital stock) with respect to the user cost; negative", (23, 32, 41), status="contested",
         checked="2026-11-20",
         meaning="aggregate time series once found almost no response; firm-level studies that use variation in the "
                 "user cost across firms find more, and reviews settled on about -0.5 to -1; studies of temporary tax "
                 "incentives find larger responses, most of all among small firms short of cash; how much a tax "
                 "break or a rate cut raises investment depends on which of these is right",
         estimates=(
             Estimate("Chirinko, Fazzari and Meyer", 1999, "regression", "US firms (Compustat), 1981-1991, user cost "
                      "varying across firms and years", -0.25, where="Journal of Public Economics 74(1): 53-80, "
                      "abstract", checked="2026-11-20"),
             Estimate("Hassett and Hubbard", 2002, "review", "the range of then-recent studies (midpoint shown)", -0.75,
                      -1.0, -0.5, where="Handbook of Public Economics vol. 3, ch. 20, as quoted by later papers "
                      "(p. 1321)", checked="2026-11-20"),
             Estimate("Zwick and Mahon", 2017, "DiD", "bonus depreciation, 120,000 US firms, 2001-2004 and "
                      "2008-2010: the implied user-cost elasticity", -1.6, where="AER 107(1): 217-248, as reported in "
                      "the paper's comparison with earlier estimates", checked="2026-11-20"),
         )),
    Dial("mpc_windfall", "marginal propensity to consume out of a transitory windfall", "percent of a one-off payment "
         "spent soon after it arrives (on nondurables within a quarter, unless the row says otherwise)",
         (22, 27, 32, 52), status="depends on the setting", checked="2026-11-20",
         meaning="far above the permanent-income hypothesis's one percent a quarter: households spend 10 to 40 percent "
                 "of a windfall on nondurables within a quarter, and more counting cars; the share is highest for "
                 "those with little liquid wealth, whatever their net worth, and smaller when many households have "
                 "cash in hand (2020); so a stimulus works through liquidity, and who receives it matters most",
         estimates=(
             Estimate("Johnson, Parker and Souleles", 2006, "RCT", "2001 tax rebates, mailing week set by the "
                      "Social Security number: nondurables, the quarter received", 30.0, 20.0, 40.0,
                      where="AER 96(5): 1589-1610, abstract", checked="2026-11-20"),
             Estimate("Parker, Souleles, Johnson and McClelland", 2013, "RCT", "2008 stimulus payments, timing set by "
                      "the Social Security number: nondurables, the quarter received (50-90% with durables)", 21.0,
                      12.0, 30.0, where="AER 103(6): 2530-2553, abstract", checked="2026-11-20"),
             Estimate("Parker, Schild, Erhard and Johnson", 2022, "event study", "2020 economic impact payments: "
                      "nondurable goods and services, the three months of arrival (s.e. 3.4)", 10.0, 3.2, 16.8,
                      where="NBER WP 29648, abstract", checked="2026-11-20"),
             Estimate("Kueng", 2018, "event study", "Alaska's Permanent Fund dividend, account data: nondurables and "
                      "services, within a quarter", 25.0, where="QJE 133(4): 1693-1751, abstract",
                      checked="2026-11-20"),
             Estimate("Jappelli and Pistaferri", 2014, "survey", "Italy, 2010: the reported share of a transitory "
                      "income gain that would be consumed", 48.0, where="AEJ: Macroeconomics 6(4): 107-136, abstract",
                      checked="2026-11-20"),
             Estimate("this film (the Island's buffer-stock households)", 2026, "calibration", "Carroll's model, a "
                      "month's windfall, spent within a year", 23.3, where="videos/economics/econ22/compute.py, mpc",
                      checked="2026-11-20"),
         )),
    Dial("convergence_speed", "speed of convergence to the steady state", "percent of the gap to its own steady state "
         "that a country closes in a year", (20, 46), status="contested", checked="2026-11-19",
         meaning="the textbook Solow model with capital's share at a third predicts about 5% a year, a half-life of 13 "
                 "years; cross-country regressions that hold saving and schooling fixed find 1 to 2% (half-lives of 35 "
                 "to 70 years), which fits a broad capital share of about three quarters; panels with country fixed "
                 "effects find 5% or more, because each country then converges to its own level. Without the "
                 "controls, poor countries did not catch up at all until about 2000, and have since by about 0.7% a "
                 "year",
         estimates=(
             Estimate("Mankiw, Romer and Weil", 1992, "regression", "98 non-oil countries, 1960-1985, conditional on "
                      "investment, population growth and schooling", 1.37, 0.99, 1.75,
                      where="QJE 107(2): 407-437, table V (implied lambda 0.0137, s.e. 0.0019)", checked="2026-11-19"),
             Estimate("Mankiw, Romer and Weil", 1992, "regression", "22 OECD countries, 1960-1985, the same controls",
                      2.03, 1.63, 2.43, where="as above, table V (0.0203, s.e. 0.0020)", checked="2026-11-19"),
             Estimate("Islam", 1995, "regression", "the same non-oil countries in five-year panels with country fixed "
                      "effects, 1960-1985", 5.07, 3.25, 6.89,
                      where="QJE 110(4): 1127-1170, table IV (LSDV, unrestricted; 0.0507, s.e. 0.0091)",
                      checked="2026-11-19"),
             Estimate("this film (Penn World Table 11.0)", 2026, "regression", "89 countries of a million people or "
                      "more, 1960-2019, conditional on investment, population growth and schooling in 1960", 1.3, 0.3,
                      3.6, where="explainer/economics/agora/growth.py (convergence), computed on screen; interval from "
                                 "two HC1 standard errors of the slope", checked="2026-11-19"),
             Estimate("Kremer, Willis and You", 2022, "regression", "unconditional: all countries, 2005-2015 (they "
                      "find divergence of about 0.5% a year in 1985-1995)", 0.7,
                      where="NBER Macroeconomics Annual 36: 337-412; NBER WP 29484, introduction",
                      checked="2026-11-19"),
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
             Estimate("this film (the Island's cereal aisle)", 2026, "calibration", "twelve brands from four firms, "
                      "random-coefficient logit, Nash-Bertrand prices: the median brand", 1.73,
                      where="videos/economics/econ43/compute.py, item cereal", checked="2026-11-20"),
             Estimate("this film (the Island's plants)", 2026, "structural", "De Loecker and Warzynski's ratio with "
                      "labour's elasticity estimated by Ackerberg, Caves and Frazer (planted median 1.3)", 1.30,
                      where="videos/economics/econ43/compute.py, item dlw", checked="2026-11-20"),
         )),
    Dial("merger_retro", "price effects of mergers, measured after the fact", "percent change in the merging "
         "firms' prices after a merger, against a control", (43, 44, 59), status="contested", checked="2026-11-21",
         meaning="if mergers the agencies cleared or settled are followed by price rises of several percent, review "
                 "has been too lenient; critics reply that the studied mergers are a selected sample and that "
                 "simple averages of different studies mislead, so how much enforcement errs remains disputed",
         estimates=(
             Estimate("Kwoka", 2013, "meta-analysis", "46 American mergers with retrospective studies: 38 (83%) "
                      "followed by price rises averaging almost 10%", 10.0, where="Antitrust Law Journal 78(3), as "
                      "summarized by Northeastern University", checked="2026-11-20"),
             Estimate("Kwoka", 2015, "meta-analysis", "mergers the agencies challenged (as reported in reviews of "
                      "the book)", 7.71, where="Mergers, Merger Control, and Remedies (MIT Press)",
                      checked="2026-11-20"),
             Estimate("Ashenfelter, Hosken and Weinberg", 2015, "DiD", "MillerCoors: the effect of the rise in "
                      "concentration, before the efficiency offset", 2.0, where="RAND Journal of Economics 46(2), "
                      "abstract", checked="2026-11-20"),
             Estimate("Miller and Weinberg", 2017, "structural", "MillerCoors: prices against Nash-Bertrand "
                      "competition with the venture's savings", 7.0, lo=6.0, hi=8.0,
                      where="Econometrica 85(6), abstract", checked="2026-11-20"),
             Estimate("this film (the Island's aisle)", 2026, "calibration", "the two smaller of four cereal makers, "
                      "simulated with random-coefficient logit", 5.8,
                      where="videos/economics/econ43/compute.py, item merger", checked="2026-11-20"),
             Estimate("Ashenfelter and Hosken", 2010, "DiD", "five consumer-product mergers near the enforcement "
                      "margin: four raised prices, typically by 3-7%", 5.0, lo=3.0, hi=7.0,
                      where="Journal of Law and Economics 53(3); NBER WP 13859, abstract", checked="2026-11-21"),
             Estimate("Cooper, Craig, Gaynor and Van Reenen", 2019, "DiD", "hospital mergers within five miles of each "
                      "other", 6.0, where="QJE 134(1), as summarized in M. Gaynor's testimony to the House "
                      "Judiciary Committee, 7 March 2019", checked="2026-11-21"),
             Estimate("this film (the Island's superstores)", 2026, "DiD", "Alder and Birch, consummated: 36 towns "
                      "against 24, twelve months either side (planted effect 11.9)", 11.7,
                      where="videos/economics/econ59/compute.py, item retro", checked="2026-11-21"),
         )),
    Dial("merger_passthrough", "pass-through of a merger's cost savings", "percent of a cut in one firm's marginal "
         "cost that reaches its prices", (59,), status="depends on the setting", checked="2026-11-21",
         meaning="a saving that only the merging firm enjoys is passed on far less than a cost change that hits a "
                 "whole industry, and a merged firm passes on less than an independent one, because a lower price "
                 "now also takes sales from its own other products; claimed savings must be discounted accordingly",
         estimates=(
             Estimate("Ashenfelter, Ashmore, Baker and McKernan", 1998, "regression", "Staples' historical pass-through "
                      "of firm-specific cost changes, cited by the court against the parties' claim of two-thirds",
                      16.0, lo=15.0, hi=17.0, where="FTC working paper 217; FTC v. Staples, 970 F. Supp. 1066 "
                      "(D.D.C. 1997), as quoted in an FTC speech", checked="2026-11-21"),
             Estimate("this film (the Island: one chain alone)", 2026, "calibration", "a 2% cut in Alder's marginal "
                      "cost, nested logit with Bertrand pricing", 66.9,
                      where="videos/economics/econ59/compute.py, item efficiency", checked="2026-11-21"),
             Estimate("this film (the Island: merged)", 2026, "calibration", "the same cut at Alder and Birch once "
                      "they have one owner", 53.3, where="videos/economics/econ59/compute.py, item efficiency",
                      checked="2026-11-21"),
         )),
    Dial("dynamic_beta", "the discount factor of a dynamic decision maker", "monthly discount factor implied by "
         "choices", (44, 54), status="not identified", checked="2026-11-20",
         meaning="the data can reject myopia, but the likelihood is nearly flat among patient discount factors, so "
                 "the value is usually fixed by assumption; with it fixed, the estimated costs follow",
         estimates=(
             Estimate("this film (Rust's buses, NFXP)", 2026, "structural", "groups 1-4, 104 buses, 60 rebuilds: the "
                      "best of seven values from 0 to 0.9999 (log likelihood -299.2, against "
                      "-305.7 at 0)", 0.9999, lo=0.99, hi=0.9999,
                      where="videos/economics/econ44/compute.py, item rust (the range: within 0.6 log points of the "
                            "best)", checked="2026-11-20"),
         )),
    Dial("product_elasticity", "own-price elasticity of demand for one differentiated product", "percent change in "
         "a product's sales for a 1% rise in its own price", (43, 60), status="depends on the setting",
         checked="2026-11-21",
         meaning="one brand's demand is far more elastic than its category's, because buyers switch brands before "
                 "they stop buying; a firm that sets its price to maximize profit never prices where its own demand "
                 "is inelastic, so an estimate below one in magnitude is a sign that the method is biased, usually "
                 "because price is correlated with quality the econometrician cannot see",
         estimates=(
             Estimate("this film (BLP's cars, plain logit by OLS)", 2026, "regression", "2,217 model-years, "
                      "1971-1990: the median model; 1,491 of them inelastic", -0.78,
                      where="videos/economics/econ43/compute.py, item blpdata", checked="2026-11-20"),
             Estimate("this film (BLP's cars, plain logit by IV)", 2026, "IV", "the same, price instrumented by "
                      "the characteristics of the firm's other models and of rivals' models; 726 inelastic", -1.20,
                      where="videos/economics/econ43/compute.py, item blpdata", checked="2026-11-20"),
             Estimate("this film (the Island's cars, BLP's estimator)", 2026, "structural", "40 simulated "
                      "markets of 40 years each; the planted median is -3.87", -3.80, lo=-4.27, hi=-3.33,
                      where="videos/economics/econ43/compute.py, item cars (mean, plus or minus two standard "
                            "deviations across Islands)", checked="2026-11-20"),
             Estimate("this film (the Island's cereal aisle)", 2026, "calibration", "twelve brands, the median "
                      "brand", -2.74, where="videos/economics/econ43/compute.py, item cereal", checked="2026-11-20"),
             Estimate("DellaVigna and Gentzkow", 2019, "regression", "stores within the typical US retail chain: the "
                      "10th to 90th percentile of store-level elasticity (the midpoint shown)", -2.52, lo=-2.81,
                      hi=-2.22, where="QJE 134(4); NBER WP 23996", checked="2026-11-21"),
         )),
    Dial("retail_passthrough", "cost pass-through to retail prices", "share of a change in producers' prices that "
         "reaches retail prices", (60,), status="depends on the setting", checked="2026-11-21",
         meaning="retail prices move with producer prices, but by less than one for one when the retailer's own costs "
                 "do not move, and by much less when only one firm's costs change; in 2021-23, when costs rose "
                 "everywhere at once, American grocery prices followed factory-gate food prices more closely than "
                 "the relation of the quiet years predicted",
         estimates=(
             Estimate("this film (food: CPI on PPI)", 2026, "regression", "monthly, 2000-2019: the cumulative effect "
                      "after twelve months of processed-food producer prices on food-at-home consumer prices", 0.58,
                      lo=0.47, hi=0.69, where="videos/economics/econ60/compute.py, item passthrough (plus or minus "
                      "two standard errors)", checked="2026-11-21"),
             Estimate("this film (food: 2021-23)", 2026, "reconstruction", "the rise in food-at-home prices over "
                      "the rise in processed-food producer prices, December 2020 to December 2023", 0.93,
                      where="videos/economics/econ60/compute.py, item passthrough", checked="2026-11-21"),
             Estimate("Ashenfelter, Ashmore, Baker and McKernan", 1998, "regression", "Staples: a cost change at "
                      "one firm only (Part 59's Dial)", 0.16, lo=0.15, hi=0.17, where="FTC working paper 217; FTC v. "
                      "Staples (D.D.C. 1997)", checked="2026-11-21"),
         )),
    Dial("surge_elasticity", "the elasticity of rides to the surge price", "percent change in rides booked per "
         "percent change in the fare shown", (61,), status="depends on the setting", checked="2026-11-21",
         meaning="ride-hailing demand is inelastic in the short run: a fare 10% higher loses about 5% of bookings, "
                 "less in a city where the alternatives are poor and more on weekend days; inelastic demand is why a "
                 "surge clears the market mainly by bringing out drivers, and why riders keep a large surplus",
         estimates=(
             Estimate("Cohen, Hahn, Hall, Levitt and Metcalfe", 2016, "RD", "UberX in its four largest American "
                      "markets, 2015: the whole sample, from the surge's rounding thresholds", -0.55, lo=-0.59,
                      hi=-0.51, where="NBER Working Paper 22627, table 4, top row (standard error 0.02)",
                      checked="2026-11-21"),
             Estimate("Cohen, Hahn, Hall, Levitt and Metcalfe", 2016, "RD", "the same, Los Angeles", -0.33, lo=-0.43,
                      hi=-0.23, where="NBER Working Paper 22627, table 4 (standard error 0.05)", checked="2026-11-21"),
             Estimate("Cohen, Hahn, Hall, Levitt and Metcalfe", 2016, "RD", "the same, weekend days", -0.66,
                      lo=-0.76, hi=-0.56, where="NBER Working Paper 22627, table 4 (standard error 0.05)",
                      checked="2026-11-21"),
             Estimate("Cohen, Hahn, Hall, Levitt and Metcalfe", 2016, "RD", "the same, weekdays outside rush hours",
                      -0.46, lo=-0.58, hi=-0.34, where="NBER Working Paper 22627, table 4 (standard error 0.06)",
                      checked="2026-11-21"),
             Estimate("this film (the Island's sessions)", 2026, "regression", "200,000 sessions at random surge "
                      "levels: the fitted demand curve's elasticity at the normal fare", -0.59,
                      where="videos/economics/econ61/compute.py, item surplus", checked="2026-11-21"),
         )),
    Dial("search_ad_return", "the return on search advertising", "extra revenue per dollar spent on paid search, "
         "less the dollar (0 breaks even)", (61,), status="contested", checked="2026-11-21",
         meaning="measured without an experiment, search ads look enormously profitable, because the people who "
                 "click them are often on their way to buy anyway; switched off at random, a well-known brand's "
                 "ads returned less than they cost, while ads that reach new customers can pay; the observational "
                 "and experimental numbers disagree in sign, and most advertisers cannot run the experiment",
         estimates=(
             Estimate("Blake, Nosko and Tadelis", 2015, "RCT", "eBay: non-brand keywords switched off for 60 days "
                      "in regions holding 30% of American traffic, by difference in differences", -0.63, lo=-1.24,
                      hi=-0.03, where="NBER Working Paper 20171, table 4, columns 4-5; Econometrica 83(1): 155-174",
                      checked="2026-11-21"),
             Estimate("Blake, Nosko and Tadelis", 2015, "regression", "the same data without the experiment: log "
                      "revenue on log spending with region and day controls", 16.32, lo=6.97, hi=22.65,
                      where="NBER Working Paper 20171, table 4, column 2", checked="2026-11-21"),
             Estimate("this film (the Island's experiment)", 2026, "RCT", "ads off in a random 30% of 210 regions "
                      "for eight weeks: the mean of 200 runs, plus or minus two standard deviations", -0.64,
                      lo=-1.29, hi=0.01, where="videos/economics/econ61/compute.py, item ads", checked="2026-11-21"),
             Estimate("this film (the Island's regression)", 2026, "regression", "log revenue on log ad spending "
                      "across regions and weeks, ads running everywhere", 26.07,
                      where="videos/economics/econ61/compute.py, item ads", checked="2026-11-21"),
         )),
    Dial("management_effect", "what better management adds", "proportional change in productivity from adopting "
         "basic management practices", (62,), status="settled within a range", checked="2026-11-21",
         meaning="in the one large randomized test, free consulting on basic practices (quality records, inventory "
                 "control, targets) raised large textile plants' productivity by about a sixth within a year; "
                 "smaller trials elsewhere find gains of the same sign, measured differently; the practices are "
                 "cheap, so the puzzle is why firms had not adopted them",
         estimates=(
             Estimate("Bloom, Eifert, Mahajan, McKenzie and Roberts", 2013, "RCT", "Indian textile plants near "
                      "Mumbai, consulting randomized by firm: productivity in the first year", 0.17,
                      where="Quarterly Journal of Economics 128(1): 1-51, abstract", checked="2026-11-21"),
             Estimate("this film (the Island's experiment)", 2026, "RCT", "28 plants in 17 firms, consulting "
                      "randomized by firm: the mean of 400 runs, plus or minus two standard deviations", 0.17,
                      lo=0.10, hi=0.24, where="videos/economics/econ62/compute.py, item experiment",
                      checked="2026-11-21"),
         )),
    Dial("ceo_pay_performance", "how a chief executive's wealth moves with the firm's", "dollars of the chief "
         "executive's wealth per $1,000 change in shareholders' wealth", (62,), status="contested",
         checked="2026-11-21",
         meaning="counting only salary, bonus and dismissal, chief executives look like bureaucrats, gaining a few "
                 "dollars per thousand their shareholders gain; counting the stock and options they hold, the "
                 "typical sensitivity is several times larger and the average far larger still; which number "
                 "matters depends on whether incentives come from holdings or from pay",
         estimates=(
             Estimate("Jensen and Murphy", 1990, "regression", "American chief executives, 1974-86: pay, options, "
                      "stockholdings and dismissal", 3.25, where="Journal of Political Economy 98(2): 225-264, "
                      "abstract", checked="2026-11-21"),
             Estimate("Hall and Liebman (mean)", 1998, "regression", "American chief executives, 1994: the whole "
                      "portfolio of stock and options", 25.11, where="Quarterly Journal of Economics 113(3), as "
                      "reported in later surveys", checked="2026-11-21"),
             Estimate("Hall and Liebman (median)", 1998, "regression", "the same, the median chief executive", 5.29,
                      where="Quarterly Journal of Economics 113(3), as reported in later surveys",
                      checked="2026-11-21"),
         )),
    Dial("reasoning_depth", "depth of strategic reasoning", "average steps of thinking (the cognitive hierarchy's "
         "tau)", (11, 45, 53), status="depends on the setting", checked="2026-11-19",
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
             Estimate("this film (the Island's cement)", 2026, "regression", "before-during-after regression on "
                      "fifteen years of monthly prices (planted 18)", 17.7,
                      where="videos/economics/econ59/compute.py, item cartel", checked="2026-11-21"),
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
    Dial("school_effects", "what a sought-after school adds", "effect on test scores, in standard deviations of "
         "students' scores, of an offer at (exam schools) or attendance at (charters) an oversubscribed school",
         (17, 49), status="depends on the setting", checked="2026-11-19",
         meaning="a school's popularity is not its value added: an offer at Boston's exam schools, whose pupils score far "
                 "higher, changes scores by about nothing, while attending Denver's oversubscribed charter schools "
                 "raises math scores by about four tenths of a standard deviation; cutoffs and lotteries make both "
                 "estimates credible",
         estimates=(
             Estimate("Abdulkadiroğlu, Angrist and Pathak", 2014, "RD", "Boston exam schools: an offer, math, grades "
                      "7, 8 and 10 pooled, at the admission cutoffs", -0.035, -0.088, 0.018,
                      where="NBER WP 17264, Table 4, column 8 (s.e. 0.027)", checked="2026-11-19"),
             Estimate("Abdulkadiroğlu, Angrist and Pathak", 2014, "RD", "Boston exam schools: an offer, English, "
                      "pooled", 0.022, -0.033, 0.077, where="NBER WP 17264, Table 4, column 8 (s.e. 0.028)",
                      checked="2026-11-19"),
             Estimate("Abdulkadiroğlu, Angrist, Narita and Pathak", 2017, "IV", "Denver charter schools: attending, "
                      "math, lottery offers from deferred acceptance, propensity-score controls", 0.415, 0.313, 0.517,
                      where="IZA DP 10429, Table 6, column 3 (s.e. 0.052)", checked="2026-11-19"),
             Estimate("Abdulkadiroğlu, Angrist, Narita and Pathak", 2017, "IV", "Denver charter schools: attending, "
                      "reading", 0.166, 0.062, 0.270, where="IZA DP 10429, Table 6, column 3 (s.e. 0.053)",
                      checked="2026-11-19"),
         )),
    Dial("return_schooling", "return to a year of school", "proportional rise in earnings per year of schooling",
         (4, 38, 46), status="settled within a range", checked="2026-11-19",
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
             Estimate("Duflo (published)", 2001, "IV", "Indonesia: over 61,000 schools built in 1973-79, by region "
                      "and cohort", 0.087, 0.068, 0.106,
                      where="American Economic Review 91(4), abstract: returns of 6.8 to 10.6 percent (the range "
                            "shown; the dot its middle)", checked="2026-11-20"),
             Estimate("this film (the Island's school-building programme)", 2026, "IV", "280 regions, the Wald ratio "
                      "of the wage and schooling differences-in-differences (planted 0.08)", 0.095,
                      where="videos/economics/econ46/compute.py, item inpres", checked="2026-11-20"),
             Estimate("this film (Card's data)", 1995, "IV", "Card's 3,010 young men of 1976, a four-year college "
                      "nearby as the instrument, with his controls (first-stage F 13)", 0.132, lo=0.025, hi=0.238,
                      where="videos/economics/econ38/compute.py, item returns", checked="2026-11-20"),
             Estimate("this film (wage2, with IQ)", 1980, "regression", "935 men of the 1980 National Longitudinal "
                      "Survey: 0.075 without IQ, 0.056 with it", 0.056, lo=0.041, hi=0.071,
                      where="videos/economics/econ38/compute.py, item returns", checked="2026-11-20"),
             Estimate("this film (Mincer, 1976 CPS)", 1976, "regression", "526 workers: log wage on schooling, "
                      "experience and its square", 0.090, lo=0.075, hi=0.106,
                      where="videos/economics/econ38/compute.py, item mincer", checked="2026-11-20"),
         )),
    Dial("labour_supply", "elasticity of labour supply (Hicksian, Frisch, extensive)", "elasticity of hours or "
         "participation to the wage", (38, 41, 50), status="depends on the setting", checked="2026-11-20",
         meaning="how much people work more when pay rises: about 0.3 for hours and 0.25 for whether to work at "
                 "all when the change is permanent; about 0.5 for a temporary rise; far more where hours are free to "
                 "move, as for rideshare drivers; the permanent elasticities price a tax, the temporary ones a "
                 "business cycle",
         estimates=(
             Estimate("Chetty Guren Manoli and Weber (Hicksian intensive)", 2011, "review", "quasi-experimental "
                      "micro estimates, synthesized", 0.30, where="American Economic Review 101(3): 471-475",
                      checked="2026-11-20"),
             Estimate("Chetty Guren Manoli and Weber (Hicksian extensive)", 2011, "review", "the same, for "
                      "participation", 0.25, where="American Economic Review 101(3): 471-475", checked="2026-11-20"),
             Estimate("Chetty Guren Manoli and Weber (Frisch intensive)", 2011, "review", "the same, for a "
                      "temporary change", 0.50, where="American Economic Review 101(3): 471-475", checked="2026-11-20"),
             Estimate("Chetty Guren Manoli and Weber (Frisch extensive)", 2011, "review", "the same, temporary, for "
                      "participation", 0.25, where="American Economic Review 101(3): 471-475", checked="2026-11-20"),
             Estimate("Angrist Caldwell and Hall (Uber)", 2021, "RCT", "Boston Uber drivers offered random changes "
                      "in the platform's fee: an intertemporal elasticity", 1.2,
                      where="American Economic Journal: Applied Economics 13(3): 272-308, abstract",
                      checked="2026-11-20"),
         )),
    Dial("minimum_wage", "employment effect of the minimum wage", "own-wage elasticity of employment", (38,),
         status="contested", checked="2026-11-20",
         meaning="the percent change in low-wage employment per percent rise in low-wage pay caused by a minimum: "
                 "near zero for the moderate increases studied most, with intervals wide enough to include modest "
                 "losses; larger losses in hours where the minimum is high relative to local wages; a small or "
                 "positive number points to employers with wage-setting power",
         estimates=(
             Estimate("this film (Card and Krueger's data)", 1994, "DiD", "410 restaurants, New Jersey against "
                      "Pennsylvania, 1992: employment +10.7% relative, the starting wage +11.0% relative; 90% "
                      "bootstrap interval", 0.97, lo=-0.05, hi=2.09,
                      where="videos/economics/econ38/compute.py, item ck", checked="2026-11-20"),
             Estimate("Cengiz Dube Lindner and Zipperer", 2019, "event study", "138 state increases, 1979-2016, by "
                      "bunching in the wage distribution (s.e. 0.43)", 0.41, lo=-0.45, hi=1.27,
                      where="Quarterly Journal of Economics 134(3): 1405-1454", checked="2026-11-20"),
             Estimate("Jardim et al. (Seattle)", 2022, "DiD", "Seattle's $11 and $13 minimums against a synthetic "
                      "control: hours at low wages", -1.1, lo=-2.0, hi=-0.2,
                      where="American Economic Journal: Economic Policy 14(2), abstract (the midpoint is this "
                      "film's)", checked="2026-11-20"),
             Estimate("this film (the Island, competitive)", 2026, "DiD", "the same design, 200 runs, stores on "
                      "their demand curves (planted elasticity -0.5)", -0.50,
                      where="videos/economics/econ38/compute.py, item border", checked="2026-11-20"),
             Estimate("this film (the Island, monopsony)", 2026, "DiD", "the same design, 200 runs, stores that set "
                      "wages (supply elasticity 3)", 1.16, where="videos/economics/econ38/compute.py, item border",
                      checked="2026-11-20"),
         )),
    Dial("skill_substitution", "elasticity of substitution between skilled and unskilled labour",
         "elasticity of substitution between college and high-school workers (sigma)", (39,),
         status="settled within a range", checked="2026-11-20",
         meaning="how far the college premium falls when college graduates become more plentiful: estimates from "
                 "national time series, cohorts and states run from about 1.4 to 2.5; at the low end, a rise in "
                 "graduates lowers the premium a lot, so education policy can offset technology's push; recent "
                 "national data alone cannot pin it down, because supply has grown almost exactly in a line",
         estimates=(
             Estimate("Katz and Murphy", 1992, "regression", "US, 1963-87: the premium on a trend and relative "
                      "supply (coefficient about -0.709)", 1.41,
                      where="Quarterly Journal of Economics 107(1): 35-78; Blanchard's account (FRBNY EPR 1995)",
                      checked="2026-11-20"),
             Estimate("Ciccone and Peri", 2005, "IV", "US states, 1950-90, with child-labour and compulsory "
                      "schooling laws as instruments", 1.5,
                      where="Review of Economics and Statistics 87(4): 652-663, abstract", checked="2026-11-20"),
             Estimate("Card and Lemieux", 2001, "structural", "US, UK and Canada, cohorts and age groups, 1959-95 "
                      "(about 5 between age groups)", 2.5,
                      where="Quarterly Journal of Economics 116(2): 705-746, abstract", checked="2026-11-20"),
         )),
    Dial("firm_premium_share", "the firm share of wage variance", "percent of the variance of log wages due to "
         "firm effects in a two-way fixed-effects (AKM) model", (39,), status="depends on the setting",
         checked="2026-11-20",
         meaning="how much of pay is where you work rather than who you are: in large administrative panels "
                 "firm premiums account for something like a fifth of wage variance, and the sorting of high-paid "
                 "workers into high-paying firms has grown; with few movers the plug-in estimates overstate firm "
                 "effects and understate sorting",
         estimates=(
             Estimate("Card Heining and Kline (1985-91)", 2013, "regression", "West German social security "
                      "records, AKM", 18.5, where="NBER Working Paper 18522, Table 3", checked="2026-11-20"),
             Estimate("Card Heining and Kline (2002-09)", 2013, "regression", "West German social security "
                      "records, AKM", 21.2, where="NBER Working Paper 18522, Table 3", checked="2026-11-20"),
             Estimate("this film (the Island)", 2026, "regression", "20,000 workers, 400 firms, six years, a tenth "
                      "moving each year; planted share 10.7%", 11.0, where="videos/economics/econ39/compute.py, item firms",
                      checked="2026-11-20"),
         )),
    Dial("callback_gap", "the call-back gap in hiring experiments", "call-backs for White applicants per call-back "
         "for African-American applicants, minus one, percent", (39,), status="settled within a range",
         checked="2026-11-20",
         meaning="how much more often employers call back the same application under a White-sounding name: "
                 "about a third to a half more in American field experiments, with no decline since 1989; it "
                 "measures the first step of hiring, not wages",
         estimates=(
             Estimate("this film (Bertrand and Mullainathan's data)", 2004, "RCT", "4,870 resumes to 1,323 "
                      "advertisements, Boston and Chicago, 2001-02; 95% interval", 49.7, lo=23.3, hi=81.7,
                      where="videos/economics/econ39/compute.py, item resume", checked="2026-11-20"),
             Estimate("Quillian Pager Hexel and Midtboen", 2017, "meta-analysis", "24 US field experiments since "
                      "1989", 36.0, where="PNAS 114(41): 10870-10875", checked="2026-11-20"),
         )),
    Dial("ige", "intergenerational elasticity of income", "the slope of children's log income on parents' log "
         "income, measured over long spans", (40,), status="contested", checked="2026-11-20",
         meaning="how much of a parent's income advantage the child keeps: at 0.3 a doubling of parents' income is "
                 "worth about 23% to the child, at 0.6 about 52%; estimates rise as parents' long-run income is "
                 "measured better, and move with the age at which children are observed and with how zero "
                 "incomes are treated, which is why rank slopes are now preferred",
         estimates=(
             Estimate("Solon", 1992, "regression", "PSID fathers and sons, fathers' earnings averaged over "
                      "several years; '0.4 or higher'", 0.4, where="AER 82(3): 393-408", checked="2026-11-20"),
             Estimate("Mazumder", 2005, "regression", "fathers' Social Security earnings over long spans", 0.6,
                      where="Review of Economics and Statistics 87(2): 235-255", checked="2026-11-20"),
             Estimate("Chetty Hendren Kline and Saez", 2014, "regression", "tax records, children born 1980-82, "
                      "family income, log-log", 0.344, where="QJE 129(4): 1553-1623", checked="2026-11-20"),
             Estimate("this film (Opportunity Insights' percentile means)", 2014, "regression", "log mean child "
                      "income on log mean parent income across parents' percentiles 10-90", 0.41,
                      where="videos/economics/econ40/compute.py, item ige", checked="2026-11-20"),
         )),
    Dial("pareto_wealth", "Pareto exponent of top wealth", "alpha in P(W > w) proportional to w^-alpha, for the "
         "top of the US wealth distribution", (40,), status="depends on the setting", checked="2026-11-20",
         meaning="the lower it is, the fatter the tail: at 1.5 the richest 0.1% hold almost half of what the richest "
                 "1% hold, at 2 about a third; through random growth it depends on the return the very wealthy "
                 "earn relative to growth, its risk, and how often fortunes are split, spent or taxed",
         estimates=(
             Estimate("this film (the Fed's accounts in 1989)", 2026, "reconstruction", "from the "
                      "top 1% and top 10% shares of household net worth, 1989 Q3", 1.74,
                      where="videos/economics/econ40/compute.py, item wealth", checked="2026-11-20"),
             Estimate("this film (the Fed's accounts in 2026)", 2026, "reconstruction", "the same, "
                      "2026 Q2", 1.48, where="videos/economics/econ40/compute.py, item wealth",
                      checked="2026-11-20"),
             Estimate("Klass Biham Levy Malcai and Solomon", 2006, "regression", "the Forbes 400, 1988-2003, "
                      "average", 1.49, where="Economics Letters 90(2): 290-295", checked="2026-11-20"),
         )),
    Dial("eti", "elasticity of taxable income", "the percentage change in reported taxable income for a one percent "
         "change in the net-of-tax rate, 1 - t", (41, 50), status="depends on the setting", checked="2026-11-20",
         meaning="how much revenue a higher rate loses to smaller reported incomes; at 0.25 the revenue-maximizing top "
                 "rate is about 73%, at 1 about 40%; estimates are larger where income can be relabelled, deferred or "
                 "hidden, which is why the elasticity is partly a policy choice",
         estimates=(
             Estimate("Feldstein", 1995, "DiD", "a Treasury panel of more than 4,000 returns around the 1986 reform; "
                      "'at least one'", 1.0, where="JPE 103(3): 551-572", checked="2026-11-20"),
             Estimate("Gruber and Saez", 2002, "regression", "panel of returns over several reforms", 0.4,
                      where="Journal of Public Economics 84(1): 1-32", checked="2026-11-20"),
             Estimate("Diamond and Saez", 2011, "review", "the mid-range value used for the top rate", 0.25,
                      where="JEP 25(4): 165-190", checked="2026-11-20"),
         )),
    Dial("top_rate", "revenue-maximizing top income tax rate", "the combined marginal rate on top incomes that "
         "raises the most revenue, 1 / (1 + a e)", (41,), status="contested", checked="2026-11-20",
         meaning="above it, a higher top rate raises less revenue; below it, the rate trades revenue from the top "
                 "against the welfare of top earners; it rests on the Pareto parameter, which is measured well, and "
                 "the elasticity, which is not",
         estimates=(
             Estimate("Diamond and Saez", 2011, "calibration", "a = 1.5, e = 0.25; all taxes combined", 73.0,
                      where="JEP 25(4): 165-190", checked="2026-11-20"),
             Estimate("this film (Piketty and Saez's 2022 shares)", 2026, "calibration", "a from the top 1% and "
                      "0.1% shares in 2022, e = 0.25", 72.0, where="videos/economics/econ41/compute.py, item top",
                      checked="2026-11-20"),
             Estimate("this film (with Feldstein's elasticity)", 2026, "calibration", "the same a, e = 1", 39.0,
                      where="videos/economics/econ41/compute.py, item top", checked="2026-11-20"),
         )),
    Dial("corp_incidence", "corporate tax incidence on wages", "the share of the corporate tax's burden borne by "
         "workers through lower wages, percent", (41,), status="depends on the setting", checked="2026-11-20",
         meaning="near zero in a closed economy where capital cannot leave, as Harberger found; large where capital "
                 "is mobile, so that a corporate tax is partly a tax on wages; the answer differs by country, by "
                 "time horizon and by how mobile firms and profits are",
         estimates=(
             Estimate("Fuest Peichl and Siegloch", 2018, "event study", "about 6,800 changes in German municipal "
                      "business taxes", 51.0, where="AER 108(2): 393-418", checked="2026-11-20"),
             Estimate("this film (the Island closed)", 2026, "calibration", "Cobb-Douglas, capital fixed", 0.0,
                      where="videos/economics/econ41/compute.py, item harberger", checked="2026-11-20"),
             Estimate("this film (the Island open)", 2026, "calibration", "Cobb-Douglas, capital perfectly mobile",
                      100.0, where="videos/economics/econ41/compute.py, item harberger", checked="2026-11-20"),
         )),
    Dial("ui_duration", "duration elasticity of unemployment benefits", "percent longer unemployment for a 1% higher "
         "weekly benefit", (24, 42), status="settled within a range", checked="2026-11-20",
         meaning="the cost side of the Baily-Chetty formula: at 0.4 to 0.8, benefits that replace half of wages "
                 "cost more in longer unemployment than they gain in smoother consumption unless people are very "
                 "averse to risk, or unless much of the response is liquidity rather than moral hazard",
         estimates=(
             Estimate("Meyer", 1990, "regression", "American spells of the 1970s and 1980s, a semiparametric hazard "
                      "model; a 10% higher benefit lengthens spells by 4-8%", 0.6, lo=0.4, hi=0.8,
                      where="Econometrica 58(4): 757-782, as summarized by Chetty", checked="2026-11-20"),
             Estimate("this film (the Island week by week)", 2026, "calibration", "26 weeks of half the wage, then "
                      "a fifth; no savings", 0.41, where="videos/economics/econ42/compute.py, item weekly",
                      checked="2026-11-20"),
         )),
    Dial("med_price", "price elasticity of medical spending", "percent change in medical spending for a 1% higher "
         "out-of-pocket price", (42,), status="contested", checked="2026-11-20",
         meaning="how much of insurance's extra spending is moral hazard: at -0.2, a 10% higher out-of-pocket price "
                 "cuts spending by about 2%; the optimal coinsurance rate rises with the elasticity, and the "
                 "summary itself is fragile because plans have deductibles and caps, so no single price applies",
         estimates=(
             Estimate("RAND (Manning et al.)", 1987, "RCT", "2,750 families at six sites, the 1970s to 1982, "
                      "plans from free care to 95% coinsurance", -0.2, where="AER 77(3): 251-277", checked="2026-11-20"),
             Estimate("this film (the Island)", 2026, "calibration", "arc elasticity between 25% and 95% "
                      "coinsurance, with free care costing 1/0.7 times the 95% plan", -0.23,
                      where="videos/economics/econ42/compute.py, item health", checked="2026-11-20"),
         )),
    Dial("mvpf", "marginal value of public funds", "dollars of benefit to recipients per dollar of net cost to the "
         "government", (42, 50), status="depends on the setting", checked="2026-11-20",
         meaning="one yardstick for every policy: above one, a dollar spent delivers more than a dollar of value, "
                 "because the policy raises other revenue; policies for children often pay for themselves, while "
                 "most for adults lie between a half and two",
         estimates=(
             Estimate("Hendren and Sprung-Keyser", 2020, "review", "133 American policies; those aimed at adults",
                      1.0, lo=0.5, hi=2.0, where="QJE 135(3): 1209-1318", checked="2026-11-20"),
             Estimate("this film (the Island's UI at its best)", 2026, "calibration", "Baily's model at the "
                      "welfare-maximizing benefit, a third of the wage", 1.0,
                      where="videos/economics/econ42/compute.py, item mvpf", checked="2026-11-20"),
             Estimate("this film (the Island's EITC)", 2026, "calibration", "a 10% larger credit for single "
                      "parents who choose whether to work", 1.06,
                      where="videos/economics/econ42/compute.py, item mvpf", checked="2026-11-20"),
         )),
    Dial("matching", "elasticity of matches to unemployment", "eta in M = A U^eta V^(1-eta); one minus the elasticity "
         "of the job-finding rate with respect to openings per searcher", (24, 29, 42), status="settled within a range",
         checked="2026-11-20",
         meaning="when the searchers counted are the unemployed, estimates cluster at a half to seven-tenths, with "
                 "constant returns; counting all hires, job-to-job moves included, or correcting for endogenous "
                 "matching efficiency gives lower values; by Hosios's condition it is also the worker's share of the "
                 "surplus at which the market creates the right number of jobs",
         estimates=(
             Estimate("Petrongolo and Pissarides", 2001, "review", "aggregate matching functions across countries "
                      "(the survey's range; midpoint shown)", 0.6, 0.5, 0.7, where="JEL 39(2): 390-431, as summarized "
                      "by later papers", checked="2026-11-20"),
             Estimate("Shimer", 2005, "regression", "US 1951-2003: the job-finding rate on the vacancy-unemployment "
                      "ratio (help-wanted index and CPS); one minus the slope", 0.72, where="AER 95(1): 25-49, the "
                      "calibration", checked="2026-11-20"),
             Estimate("this film (Agora)", 2026, "regression", "US 2001-2019, quarterly: the CPS job-finding rate "
                      "(Shimer's method) on JOLTS openings per unemployed worker; one minus the slope", 0.58,
                      where="videos/economics/econ24/compute.py, item matching", checked="2026-11-20"),
             Estimate("this film (Agora)", 2026, "regression", "US 2001-2019, monthly: JOLTS hires per unemployed "
                      "worker on openings per unemployed worker; hires include job-to-job moves", 0.31,
                      where="videos/economics/econ24/compute.py, item matching", checked="2026-11-20"),
         )),
    Dial("bargaining_share", "the worker's bargaining share", "beta, the worker's share of a match's surplus under "
         "Nash bargaining", (24, 29, 38), status="contested", checked="2026-11-20",
         meaning="it cannot be read off wages without knowing what the worker's fallback is worth, so calibrations "
                 "choose it with the fallback: Hosios's condition gives about 0.7, the small-surplus calibration "
                 "that makes unemployment volatile 0.05; structural estimates that let employers compete for workers "
                 "find little bargaining power at all below the top of the skill distribution, the rent coming "
                 "from competition between employers instead",
         estimates=(
             Estimate("Shimer", 2005, "calibration", "set equal to the matching elasticity (Hosios's condition)", 0.72,
                      where="AER 95(1): 25-49, the calibration", checked="2026-11-20"),
             Estimate("Hagedorn and Manovskii", 2008, "calibration", "chosen with the value of non-work (0.955) to "
                      "match the costs of vacancies and the cyclicality of wages", 0.052,
                      where="AER 98(4): 1692-1706, the calibration", checked="2026-11-20"),
             Estimate("Cahuc, Postel-Vinay and Robin", 2006, "structural", "French matched employer-employee data, "
                      "low- and intermediate-skill workers: no significant bargaining power (shown at zero; modestly "
                      "positive for the high-skilled)", 0.0, where="Econometrica 74(2): 323-364, abstract and "
                      "post-print summary", checked="2026-11-20"),
         )),
    Dial("okun", "Okun's coefficient", "percentage points of unemployment above its natural rate per percent of "
         "output below potential (negative)", (27, 29), status="depends on the setting", checked="2026-11-20",
         meaning="in the United States unemployment moves about half a point for each point output falls short of "
                 "potential, so a recession that costs four points of output adds about two points of unemployment; "
                 "the coefficient is stable over time but differs across countries with their labour markets: small "
                 "in Japan, where firms hoard labour, large in Spain, where temporary contracts are cut first",
         estimates=(
             Estimate("Okun", 1962, "regression", "US quarterly, 1947-1960: about three points of output per point of "
                      "unemployment (shown as one third)", -0.33, where="Proceedings of the Business and Economic "
                      "Statistics Section, ASA (1962): 98-104", checked="2026-11-20"),
             Estimate("Ball, Leigh and Loungani", 2017, "regression", "United States, annual, 1948-2011: gaps from "
                      "an HP filter (a range of -0.4 to -0.5; R-squared about 0.8)", -0.45,
                      where="JMCB 49(7): 1413-1441; NBER WP 18668, introduction", checked="2026-11-20"),
             Estimate("Ball, Leigh and Loungani", 2017, "regression", "Japan, annual, 1980-2011", -0.15,
                      where="NBER WP 18668, introduction", checked="2026-11-20"),
             Estimate("Ball, Leigh and Loungani", 2017, "regression", "Spain, annual, 1980-2011", -0.85,
                      where="NBER WP 18668, introduction", checked="2026-11-20"),
             Estimate("this film (Agora)", 2026, "regression", "US quarterly, 1949-2025: unemployment less the CBO's "
                      "natural rate on real GDP against the CBO's potential (R-squared 0.78)", -0.62,
                      where="videos/economics/econ27/compute.py, item okun", checked="2026-11-20"),
         )),
    Dial("price_frequency", "frequency of price changes", "share of consumer prices changing in a month", (30, 31),
         status="settled within a range", checked="2026-11-20",
         meaning="how often prices change sets how slowly the price level follows money, and so how much a change in "
                 "money or interest rates moves output; American consumer prices change at a rate of about one in "
                 "five a month counting temporary sales and about one in ten without them, and whether sales matter "
                 "for money is itself argued (they appear to matter less than their number)",
         estimates=(
             Estimate("Bils and Klenow", 2004, "reconstruction", "BLS micro data, 350 categories, 1995-97: implied by "
                      "the median duration of 4.3 months", 0.208, where="JPE 112(5): 947-985", checked="2026-11-20"),
             Estimate("Nakamura and Steinsson", 2008, "reconstruction", "BLS micro data: all price changes, sales "
                      "included", 0.195, lo=0.19, hi=0.20, where="QJE 123(4): 1415-1464, abstract",
                      checked="2026-11-20"),
             Estimate("Nakamura and Steinsson", 2008, "reconstruction", "the same data, regular prices (sales "
                      "excluded)", 0.105, lo=0.09, hi=0.12, where="QJE 123(4): 1415-1464, abstract",
                      checked="2026-11-20"),
             Estimate("this film (Agora)", 2026, "calibration", "the Island's Calvo pricing (prices last three "
                      "quarters on average), per month", 0.126,
                      where="videos/economics/econ30/compute.py, item calvo", checked="2026-11-20"),
         )),
    Dial("phillips_slope", "slope of the Phillips curve", "percentage points of inflation (or of its change) per "
         "point of unemployment; negative", (28, 30), status="contested", checked="2026-11-20",
         meaning="the trade-off looked steep in the 1960s and has looked flat since the 1990s: a point of unemployment "
                 "moved inflation by more than half a point a year before 1984 and by less than a tenth after 2000; "
                 "part of the flattening is anchored expectations, which hide the curve, and estimates across "
                 "American states (Hazell, Herreno, Nakamura and Steinsson 2022) find it was small even in the early "
                 "1980s, so that the disinflation then came from expectations more than from slack",
         estimates=(
             Estimate("Phillips", 1958, "regression", "Britain, 1861-1913: the fitted wage curve's slope at 3% "
                      "unemployment", -0.97, where="Economica 25(100): 283-299, the fitted curve",
                      checked="2026-11-20"),
             Estimate("Samuelson and Solow", 1960, "calibration", "United States: their menu, from price stability at "
                      "5-6% unemployment to 4-5% inflation at 3% (shown at the midpoints)", -1.8,
                      where="AER 50(2): 177-194", checked="2026-11-20"),
             Estimate("this film (Agora)", 2026, "regression", "US 1960-1983, annual: the change in core inflation "
                      "on unemployment less the CBO's natural rate", -0.65,
                      where="videos/economics/econ28/compute.py, item flat", checked="2026-11-20"),
             Estimate("this film (Agora)", 2026, "regression", "US 1984-1999: the same regression", -0.18,
                      where="videos/economics/econ28/compute.py, item flat", checked="2026-11-20"),
             Estimate("this film (Agora)", 2026, "regression", "US 2000-2019: the same regression", -0.07,
                      where="videos/economics/econ28/compute.py, item flat", checked="2026-11-20"),
         )),
    Dial("sacrifice", "sacrifice ratio", "point-years of output lost per point by which trend inflation falls", (28,),
         status="contested", checked="2026-11-20",
         meaning="bringing inflation down by a point has cost about two years' worth of a point of output in America, "
                 "less when the disinflation is fast and wage-setting flexible (Ball 1994) and, on some accounts, "
                 "less when the central bank is believed; structural estimates are so imprecise that their intervals "
                 "include zero",
         estimates=(
             Estimate("Ball", 1994, "event study", "US, the disinflation of 1979-83, trend output and trend inflation "
                      "(as cited by Federal Reserve staff; other citations give 2.4)", 1.8,
                      where="in N. G. Mankiw (ed.), Monetary Policy (1994): 155-193", checked="2026-11-20"),
             Estimate("Mankiw", 1991, "calibration", "US 1982-85: the unemployment above normal, turned into output "
                      "by Okun's law, per point of disinflation", 2.8,
                      where="Mankiw, Macroeconomics, the Volcker disinflation", checked="2026-11-20"),
             Estimate("this film (Agora)", 2026, "event study", "US 1980-1985: output below the CBO's potential, "
                      "summed, per point by which core inflation fell (12.4% to 4.4%)", 2.04,
                      where="videos/economics/econ28/compute.py, item volcker", checked="2026-11-20"),
         )),
    Dial("frisch", "Frisch elasticity of labour supply", "the percentage change in hours worked per percentage "
         "change in the wage, holding the marginal utility of wealth fixed", (29, 30, 52),
         status="contested", checked="2026-11-20",
         meaning="how far people move their hours when a wage change is temporary; models of the business cycle need "
                 "a large value (hours swing almost as much as output), while studies of individual workers find a "
                 "small one; part of the gap closes by counting people who move in and out of work (the extensive "
                 "margin), part remains, and it decides whether recessions can be read as people choosing leisure",
         estimates=(
             Estimate("Chetty, Guren, Manoli and Weber", 2011, "review", "micro studies, the intensive margin (hours "
                      "of those who work)", 0.54, where="AER 101(3): 471-475", checked="2026-11-20"),
             Estimate("Chetty, Guren, Manoli and Weber", 2011, "review", "micro studies, the extensive margin (who "
                      "works)", 0.28, where="AER 101(3): 471-475", checked="2026-11-20"),
             Estimate("Chetty, Guren, Manoli and Weber", 2011, "review", "the two margins together: aggregate hours",
                      0.82, where="AER 101(3): 471-475", checked="2026-11-20"),
             Estimate("Chetty, Guren, Manoli and Weber", 2011, "review", "the value typical in macroeconomic models, "
                      "as reported in the same review", 2.84, where="AER 101(3): 471-475", checked="2026-11-20"),
             Estimate("this film (Agora)", 2026, "calibration", "the elasticity at which the Island's hours are half "
                      "as volatile as its output (US data: 0.90)", 2.14,
                      where="videos/economics/econ29/compute.py, item frisch", checked="2026-11-20"),
         )),
    Dial("money_demand", "interest semi-elasticity of money demand", "the change in the log of real money balances "
         "(relative to income) per percentage point of the nominal interest rate; negative", (25, 28, 31),
         status="contested", checked="2026-11-20",
         meaning="how much people economize on money when interest rates rise; it sets the welfare cost of inflation "
                 "(chapter 12) and how far a central bank must move rates to change money holdings; estimates for "
                 "American M1 range from about -0.07 before 1981 to -0.02 or less afterwards, and depend on which "
                 "deposits are counted as money",
         estimates=(
             Estimate("Ball", 2001, "regression", "US M1, postwar years through 1996, long-run money demand", -0.05,
                      where="Journal of Monetary Economics 47(1): 31-44, abstract", checked="2026-11-20"),
             Estimate("Ireland", 2009, "regression", "US, post-1980 data, Cagan's semi-log form: a semi-elasticity "
                      "below 2 per unit of the rate (shown at the bound)", -0.02, where="AER 99(3): 1040-1052, abstract",
                      checked="2026-11-20"),
             Estimate("this film (Agora)", 2026, "regression", "US 1959-1980, quarterly: ln(M1/GDP) on the three-month "
                      "bill rate", -0.067, where="videos/economics/econ25/compute.py, item baumol",
                      checked="2026-11-20"),
             Estimate("this film (Agora)", 2026, "regression", "US 1994-2019, quarterly: the same regression", -0.032,
                      where="videos/economics/econ25/compute.py, item baumol", checked="2026-11-20"),
         )),
    Dial("deposit_beta", "deposit beta", "the share of a rise in the policy rate that banks pass on to a deposit rate, "
         "over a tightening cycle", (26, 31), status="depends on the setting", checked="2026-11-20",
         meaning="banks pay depositors much less than the policy rate, and pass on its rises slowly: savings accounts "
                 "almost nothing, time deposits a third, the average interest-bearing deposit about two-fifths by the "
                 "end of a cycle; the low beta is the deposit franchise that hedges a bank's long assets, and it "
                 "lasts only while depositors stay",
         estimates=(
             Estimate("Federal Reserve Bank of New York", 2022, "regression", "US banks, interest-bearing deposits: "
                      "the 2004-06 cycle's peak cumulative beta, approaching 0.6 (shown at 0.6)", 0.6,
                      where="Liberty Street Economics, 'How do deposit rates respond to monetary policy?', November "
                            "2022", checked="2026-11-20"),
             Estimate("Federal Reserve Bank of New York", 2022, "regression", "US banks, interest-bearing deposits: "
                      "the 2015-19 cycle, never above 0.4 (shown at the bound)", 0.4,
                      where="Liberty Street Economics, November 2022", checked="2026-11-20"),
             Estimate("Federal Reserve Bank of New York", 2023, "regression", "US banks, interest-bearing deposits, "
                      "cumulative to 2022 Q4: almost 0.4 (shown at 0.39)", 0.39,
                      where="Liberty Street Economics, 'Deposit betas: up, up, and away?', April 2023",
                      checked="2026-11-20"),
             Estimate("S&P Global Market Intelligence", 2023, "survey", "US banks, all deposits, aggregate cumulative "
                      "beta to 2023 Q3", 0.385, where="S&P Global Market Intelligence, October 2023",
                      checked="2026-11-20"),
             Estimate("this film (FDIC national rates)", 2026, "regression", "savings accounts, February 2022 to "
                      "December 2023, against the federal funds rate", 0.076,
                      where="videos/economics/econ26/compute.py, item betas", checked="2026-11-20"),
             Estimate("this film (FDIC national rates)", 2026, "regression", "12-month CDs, February 2022 to "
                      "December 2023", 0.328, where="videos/economics/econ26/compute.py, item betas",
                      checked="2026-11-20"),
         )),
    Dial("crisis_cost", "output cost of a banking crisis", "percent of GDP: the fall from peak to trough, or the "
         "persistent gap below the pre-crisis path, as each study measures it", (26, 33, 55), status="contested",
         checked="2026-11-20",
         meaning="output falls by about a tenth after the typical systemic banking crisis and does not fully recover, "
                 "but averages mix crises with what caused them; in rich countries the average decline is nearer six "
                 "percent and varies with how severe the financial distress was; the gap that persists depends on "
                 "which trend you draw",
         estimates=(
             Estimate("Reinhart and Rogoff", 2009, "event study", "systemic banking crises: real GDP per capita, "
                      "peak to trough, average (over 9 percent; shown at 9)", 9.0,
                      where="AER 99(2): 466-472, abstract", checked="2026-11-20"),
             Estimate("Cerra and Saxena", 2008, "regression", "190 countries, banking crises: the persistent loss of "
                      "output", 10.0, where="AER 98(1): 439-457; the authors' summary, IMF blog, 21 March 2018",
                      checked="2026-11-20"),
             Estimate("Romer and Romer", 2017, "regression", "24 OECD countries, 1967-2012, a new measure of "
                      "financial distress: peak decline of GDP after a crisis (4 percent by GLS)", 6.0,
                      where="AER 107(10): 3072-3118", checked="2026-11-20"),
             Estimate("this film (US 2007-09)", 2026, "event study", "US real GDP, 2007 Q4 to 2009 Q2, peak to trough",
                      3.8, where="videos/economics/econ26/compute.py, item crisis", checked="2026-11-20"),
             Estimate("this film (US 2007-09)", 2026, "event study", "US real GDP in 2019 Q4 below its 1990-2007 "
                      "trend (3.2 percent a year)", 17.6, where="videos/economics/econ26/compute.py, item crisis",
                      checked="2026-11-20"),
             Estimate("this film (JST since 1948)", 2026, "event study", "18 advanced economies, 1948-2020: real "
                      "GDP per head five years after the peak, recessions with a banking crisis against normal ones "
                      "(25 and 86)", 7.7,
                      where="videos/economics/econ33/compute.py, item recessions", checked="2026-11-20"),
             Estimate("this film (JST since 1870)", 2026, "event study", "the same, 1870-2020, war years left out "
                      "(97 and 230)", 2.4,
                      where="videos/economics/econ33/compute.py, item recessions", checked="2026-11-20"),
         )),
    Dial("credit_warning", "warning value of a credit boom", "percent chance that a banking crisis starts within "
         "three years, after a boom in credit (and, where stated, asset prices)", (33,),
         status="settled within a range", checked="2026-11-20",
         meaning="credit booms are the best single warning of a crisis: after the fastest growth in credit the chance "
                 "of a crisis within three years is two to four times the usual one in ten, and higher when house or "
                 "stock prices have boomed too; but most booms still end without one, and out of sample the timing is "
                 "hard to call, so a warning justifies leaning against a boom, not predicting the date",
         estimates=(
             Estimate("Greenwood, Hanson, Shleifer and Sorensen", 2022, "regression", "42 countries, 1950-2016: "
                      "rapid credit and asset-price growth in the business or household sector (about 7% otherwise)",
                      40.0, where="Journal of Finance 77(2): 863-921, abstract", checked="2026-11-20"),
             Estimate("this film (JST: credit and houses)", 2026, "regression", "18 countries, 1870-2017: the "
                      "three-year rise in loans to GDP and in real house prices both in their top fifth "
                      "(5% when neither)", 33.3,
                      where="videos/economics/econ33/compute.py, item panel", checked="2026-11-20"),
             Estimate("this film (JST: credit alone)", 2026, "regression", "the same, the top fifth of the rise in "
                      "loans to GDP alone (6% in the bottom fifth)",
                      18.4, where="videos/economics/econ33/compute.py, item panel",
                      checked="2026-11-20"),
         )),
    Dial("monetary_shock", "effect of a 100-basis-point tightening on output", "percent fall in industrial "
         "production at its peak, one to three years after the shock", (31, 55), status="contested",
         checked="2026-11-20",
         meaning="how much a central bank's rate moves the economy: a recursive VAR says little, under one percent of "
                 "industrial production; Romer and Romer's narrative shocks say several times more, with the price "
                 "level about 6% lower after four years; Coibion traced most of the gap to the 1979-82 period and the "
                 "lag lengths and put the effect at 2-3%; the methods disagree because each must separate what the "
                 "bank did on its own from what it did in response to the economy",
         estimates=(
             Estimate("a standard recursive VAR (reported by Coibion)", 2012, "structural", "US monthly data, "
                      "1969-96: the peak fall in industrial production", -0.7,
                      where="Coibion, AEJ: Macroeconomics 4(2): 1-32, and his VoxEU column on it", checked="2026-11-20"),
             Estimate("Romer and Romer", 2004, "narrative", "shocks purged of the Greenbook's forecasts, 1969-96: the "
                      "peak fall in industrial production", -4.3, where="AER 94(4): 1055-1084, as reported by "
                      "Coibion (2012)", checked="2026-11-20"),
             Estimate("Coibion", 2012, "review", "the two reconciled: the 1979-82 period and lag lengths accounted "
                      "for", -2.5, lo=-3.0, hi=-2.0, where="AEJ: Macroeconomics 4(2): 1-32, abstract",
                      checked="2026-11-20"),
             Estimate("this film (US 1965-2007)", 2026, "structural", "a recursive VAR with commodity prices: "
                      "industrial production's trough, 29 months after the shock", -1.33, lo=-1.67, hi=-0.72,
                      where="videos/economics/econ31/compute.py, item usvar", checked="2026-11-20"),
             Estimate("this film (US 1965-1995)", 2026, "structural", "Sims's recursive VAR, 12 monthly lags, no "
                      "commodity prices: industrial production's trough, 22 months", -0.80, lo=-1.01, hi=-0.65,
                      where="videos/economics/econ55/compute.py, item puzzle (16-84% bootstrap band)",
                      checked="2026-11-21"),
             Estimate("this film (US 1965-1995)", 2026, "structural", "the same with commodity prices: the trough, "
                      "23 months", -1.12, lo=-1.28, hi=-0.77,
                      where="videos/economics/econ55/compute.py, item puzzle (16-84% bootstrap band)",
                      checked="2026-11-21"),
         )),
    Dial("multipliers", "government-spending multiplier", "dollars of output per dollar of government purchases, "
         "cumulative over about two years", (32, 55), status="depends on the setting", checked="2026-11-20",
         meaning="whether a dollar of government spending adds more or less than a dollar to output: national "
                 "estimates for the United States come out below one, because private spending falls and the central "
                 "bank leans against the spending; comparisons across regions of one currency union come out above "
                 "one, because they hold monetary policy and national taxes fixed; theory says the national "
                 "multiplier should be larger at the zero bound, and whether it is larger in slumps is argued",
         estimates=(
             Estimate("Ramey and Zubairy", 2018, "narrative", "US 1889-2015, military news, local projections: two "
                      "years", 0.67, where="JPE 126(2), replication output (Multiplier-Standard-Errors.xlsx); this "
                      "film reproduces it", checked="2026-11-20"),
             Estimate("Ramey and Zubairy", 2018, "structural", "the same data, Blanchard-Perotti timing: two years",
                      0.41, where="JPE 126(2), replication output; this film reproduces it", checked="2026-11-20"),
             Estimate("Nakamura and Steinsson", 2014, "IV", "US states, defence procurement: the open-economy "
                      "relative multiplier", 1.5, where="AER 104(3): 753-792; NBER WP 17391, abstract",
                      checked="2026-11-20"),
             Estimate("Chodorow-Reich", 2019, "review", "cross-sectional (regional) studies, preferred estimate", 1.8,
                      where="AEJ: Economic Policy 11(2): 1-34, abstract", checked="2026-11-20"),
         )),
    Dial("gdp_forecast_rmse", "error of forecasts of real GDP growth", "root mean squared error of forecasts of "
         "US real GDP growth, percentage points at an annual rate, against the first published estimate", (57,),
         status="settled within a range", checked="2026-11-21",
         meaning="how far ahead the economy can be read: professional forecasts of the current quarter miss by about "
                 "two points, and by three a year ahead, no better than the average of the past decade; so policy "
                 "a year out is made with the average, and what matters is how fast forecasts are revised",
         estimates=(
             Estimate("this film: the SPF", 2026, "survey", "median forecast for the current quarter, surveys "
                      "1968Q4-2026Q3, the pandemic's 2020Q2-Q3 left out", 1.86,
                      where="videos/economics/econ57/compute.py, item score", checked="2026-11-21"),
             Estimate("this film: the SPF", 2026, "survey", "one quarter ahead", 2.47,
                      where="videos/economics/econ57/compute.py, item score", checked="2026-11-21"),
             Estimate("this film: the SPF", 2026, "survey", "two quarters ahead", 2.78,
                      where="videos/economics/econ57/compute.py, item score", checked="2026-11-21"),
             Estimate("this film: the SPF", 2026, "survey", "four quarters ahead", 2.97,
                      where="videos/economics/econ57/compute.py, item score", checked="2026-11-21"),
             Estimate("this film: a benchmark", 2026, "reconstruction", "the previous ten years' average growth, "
                      "for the current quarter", 3.06, where="videos/economics/econ57/compute.py, item score",
                      checked="2026-11-21"),
         )),
    Dial("social_discount_rate", "the social discount rate", "real percent a year, applied to the costs and benefits "
         "of public projects and rules in their first decades", (58,), status="contested", checked="2026-11-21",
         meaning="how much a benefit decades away counts today: at 7% a pound in thirty years is worth 13 pence now, "
                 "at 2% it is worth 55; the rates governments prescribe have drifted down with real interest rates and "
                 "the experts' views, and they move with politics too, which is why a hundred-year bridge or a climate "
                 "rule can pass or fail on this one number",
         estimates=(
             Estimate("OMB Circular A-4", 2003, "review", "the rate of return on private capital, for rules that "
                      "displace investment", 7.0, where="Circular A-4 (2003); reinstated by memorandum M-25-15, "
                      "February 2025", checked="2026-11-21"),
             Estimate("OMB Circular A-4", 2003, "review", "the rate at which consumers trade consumption over time",
                      3.0, where="as above", checked="2026-11-21"),
             Estimate("HM Treasury's Green Book", 2003, "calibration", "Ramsey's rule: 0.5% time preference, 1.0% "
                      "catastrophe risk, 1.0 x 2.0% growth; years 0-30, declining after", 3.5,
                      where="The Green Book (2003 to 2026), discounting annex", checked="2026-11-21"),
             Estimate("HM Treasury's Green Book", 2026, "review", "the headline rate for years 1 to 30, accepted "
                      "after Freeman and Groom's review", 3.0,
                      where="Green Book Discount Rate Review: HM Treasury response, 28 October 2026",
                      checked="2026-11-21"),
             Estimate("OMB Circular A-4", 2023, "review", "the 30-year average real yield on 10-year Treasury notes; "
                      "rescinded in 2025", 2.0, where="Circular A-4 (9 November 2023)", checked="2026-11-21"),
             Estimate("Drupp, Freeman, Groom and Nesje", 2018, "survey", "over 200 experts on discounting: the mean "
                      "recommendation (the median is 2%)", 2.27, 0.0, 10.0,
                      where="AEJ: Economic Policy 10(4): 109-134, as summarized by the LSE's Grantham Institute",
                      checked="2026-11-21"),
             Estimate("this film: the market", 2026, "reconstruction", "the average real yield on 10-year inflation-"
                      "protected Treasuries, 2003-2025", 0.97, where="videos/economics/econ58/compute.py, item "
                      "discount (FRED: DFII10)", checked="2026-11-21"),
         )),
    Dial("cost_overrun", "cost overruns of public works", "percent by which the outturn cost exceeds the cost "
         "forecast at the decision to build, in constant prices", (58,), status="depends on the setting",
         checked="2026-11-21",
         meaning="how far to trust a project's cost estimate: transport projects come in over budget nine times in "
                 "ten, by about a fifth for roads and nearly a half for rail, with long tails; the averages differ by "
                 "type and by country, and samples of projects with good records may flatter or worsen them, but an "
                 "appraisal that takes the estimate at face value is biased towards building",
         estimates=(
             Estimate("Flyvbjerg, Holm and Buhl", 2002, "review", "rail: 58 projects", 44.7,
                      where="JAPA 68(3): 279-295, table of cost escalation by project type (s.d. 38.4)",
                      checked="2026-11-21"),
             Estimate("Flyvbjerg, Holm and Buhl", 2002, "review", "bridges and tunnels: 33 projects", 33.8,
                      where="as above (s.d. 62.4)", checked="2026-11-21"),
             Estimate("Flyvbjerg, Holm and Buhl", 2002, "review", "roads: 167 projects", 20.4,
                      where="as above (s.d. 29.9)", checked="2026-11-21"),
             Estimate("Flyvbjerg, Holm and Buhl", 2002, "review", "all 258 projects", 28.0,
                      where="as above and Flyvbjerg's later papers (s.d. 39)", checked="2026-11-21"),
         )),
    Dial("tax_multiplier", "tax multiplier", "percent fall in real GDP after a tax increase of 1% of GDP, at its "
         "largest within three years", (32,), status="contested", checked="2026-11-20",
         meaning="how much output a tax increase costs: estimates from the narrative record of tax laws are two to "
                 "three, larger than most spending multipliers and the opposite of the simple Keynesian ranking, with "
                 "much of the effect through investment; why they are so large, and whether tax increases made to "
                 "close an inherited deficit cost less, are argued",
         estimates=(
             Estimate("Romer and Romer", 2010, "narrative", "US postwar exogenous tax changes: output over three years",
                      3.0, lo=2.0, hi=3.0, where="AER 100(3): 763-801 (nearly 3%); NBER digest (2 to 3%)",
                      checked="2026-11-20"),
             Estimate("this film", 2026, "narrative", "the Romers' changes, local projections with four lags: the "
                      "trough, ten quarters after", 2.2, where="videos/economics/econ32/compute.py, item taxes",
                      checked="2026-11-20"),
         )),
    Dial("neutral_rate", "neutral real interest rate", "percent a year: the real short rate that neither "
         "stimulates nor restrains the economy, once temporary shocks have passed", (31,), status="contested",
         checked="2026-11-20",
         meaning="where policy is tight or loose depends on it; estimates for the United States fell from about 3.5% "
                 "in 2000 to under 1% in the 2010s and have edged up since, while the euro area's fell to about zero; "
                 "each estimate is uncertain by a point or more either way, and the Island's filter shows why: the "
                 "natural rate is inferred from slow drifts in output, which other shocks swamp",
         estimates=(
             Estimate("Holston-Laubach-Williams (US)", 2026, "structural", "one-sided estimate for 2026Q2, "
                      "the New York Fed's current estimates", 1.01, where="FRBNY, Holston_Laubach_Williams_current_"
                      "estimates.xlsx (data.hlw)", checked="2026-11-20"),
             Estimate("Holston-Laubach-Williams (euro area)", 2026, "structural", "one-sided estimate for 2026Q2",
                      0.09, where="FRBNY, Holston_Laubach_Williams_current_estimates.xlsx (data.hlw)",
                      checked="2026-11-20"),
             Estimate("Holston-Laubach-Williams (Canada)", 2026, "structural", "one-sided estimate for 2026Q2",
                      1.76, where="FRBNY, Holston_Laubach_Williams_current_estimates.xlsx (data.hlw)",
                      checked="2026-11-20"),
             Estimate("FOMC participants (US)", 2026, "survey", "the median longer-run funds rate in the September "
                      "projections (3.2%), less the 2% target", 1.2, where="FRED FEDTARMDLR", checked="2026-11-20"),
             Estimate("FOMC participants (US)", 2012, "survey", "the same, in the first projections, January 2012 "
                      "(4.3%), less 2%", 2.3, where="FRED FEDTARMDLR", checked="2026-11-20"),
         )),
    Dial("qe_yield", "effect of asset purchases on long-term yields", "basis points on the 10-year Treasury yield "
         "or its term premium, for the Fed's first purchases ($1.725 trillion announced, 2008-09)", (31,),
         status="contested", checked="2026-11-20",
         meaning="whether a central bank at zero can still lower long rates by buying bonds: event studies of the "
                 "announcement days find large falls, and time-series models of the term premium find falls of "
                 "similar size; sceptics note that yields rose on the days in between and that the event-study result "
                 "is fragile to the choice of days",
         estimates=(
             Estimate("Gagnon, Raskin, Remache and Sack", 2011, "event study", "the 10-year Treasury yield over the "
                      "eight baseline announcements, November 2008 to November 2009", -91,
                      where="IJCB 7(1): 3-43; FRBNY Economic Policy Review 17(1), chart 5", checked="2026-11-20"),
             Estimate("Gagnon, Raskin, Remache and Sack", 2011, "event study", "the 10-year term premium, depending "
                      "on the event set and window", -75, lo=-100, hi=-50, where="FRBNY Economic Policy Review 17(1)",
                      checked="2026-11-20"),
             Estimate("Gagnon, Raskin, Remache and Sack", 2011, "regression", "the 10-year term premium, by a time-"
                      "series model of the supply of long-term debt", -60, lo=-82, hi=-38,
                      where="FRBNY Economic Policy Review 17(1), table 6", checked="2026-11-20"),
             Estimate("this film", 2026, "event study", "the 10-year Treasury yield (FRED DGS10) on the same eight "
                      "days, close to close", -94, where="videos/economics/econ31/compute.py, item qe",
                      checked="2026-11-20"),
         )),
    Dial("trade_elasticity", "the trade elasticity", "the percent fall in imports from a 1% rise in their cost "
         "(absolute value)", (36, 66), status="depends on the setting", checked="2026-11-20",
         meaning="how strongly trade responds to its costs: gravity studies across countries put it at five to ten; "
                 "tariff changes traced over time give under one within a year and about two after a decade; the gains "
                 "from trade shrink as the elasticity rises, so the smaller long-run values imply larger gains",
         estimates=(
             Estimate("Anderson and van Wincoop (review)", 2004, "review", "the gravity literature's range, used by "
                      "Arkolakis, Costinot and Rodriguez-Clare (2012)", 7.5, lo=5.0, hi=10.0,
                      where="Journal of Economic Literature 42(3): 691-751; ACR (2012)", checked="2026-11-20"),
             Estimate("Boehm Levchenko and Pandalai-Nayar (short run)", 2023, "event study", "MFN tariff changes, "
                      "local projections: the first year", 0.76, where="American Economic Review 113(4): 861-905, "
                      "abstract", checked="2026-11-20"),
             Estimate("Boehm Levchenko and Pandalai-Nayar (long run)", 2023, "event study", "the same, after seven to "
                      "ten years", 2.0, where="American Economic Review 113(4): 861-905, abstract",
                      checked="2026-11-20"),
         )),
    Dial("import_competition_jobs", "local effect of import competition on manufacturing jobs", "percentage points "
         "of a local labour market's working-age population employed in manufacturing, per $1,000 of import exposure "
         "per worker over a decade", (36,), status="settled within a range", checked="2026-11-20",
         meaning="the China shock's local footprint: places whose industries faced more imports from China lost "
                 "manufacturing jobs, and the jobs were not quickly replaced; least squares understates the effect "
                 "because demand shocks raise imports and jobs together",
         estimates=(
             Estimate("Autor Dorn and Hanson (2SLS)", 2013, "IV", "722 US commuting zones, 1990-2007, exposure "
                      "instrumented with China's exports to eight other rich countries", -0.596,
                      where="American Economic Review 103(6), table 3, column 6", checked="2026-11-20"),
             Estimate("Autor Dorn and Hanson (OLS)", 2013, "regression", "the same, least squares", -0.171,
                      where="NBER Working Paper 18054, section on OLS against 2SLS", checked="2026-11-20"),
             Estimate("this film (the Island)", 2026, "IV", "400 simulated zones with a planted effect of -0.6: the "
                      "instrumented estimate", -0.578, where="videos/economics/econ36/compute.py, item china",
                      checked="2026-11-20"),
         )),
    Dial("passthrough", "pass-through of tariffs and exchange rates to prices", "share of a change in the exchange "
         "rate (or a tariff) that reaches import prices", (34, 36, 66), status="depends on the setting",
         checked="2026-11-20",
         meaning="how far a currency's fall raises the prices a country pays: for goods priced in the importer's "
                 "currency, such as most American imports priced in dollars, little at first and under half after a "
                 "year; for goods priced in the exporter's currency, nearly all; so the dollar's share of invoicing "
                 "decides how exchange rates move trade",
         estimates=(
             Estimate("Gopinath Itskhoki and Rigobon (dollar-priced)", 2010, "regression", "US import prices at the "
                      "dock, goods priced in dollars, conditional on a price change", 0.25,
                      where="AER 100(1): 304-336, abstract", checked="2026-11-20"),
             Estimate("Gopinath Itskhoki and Rigobon (other currencies)", 2010, "regression", "the same, goods priced "
                      "in other currencies", 0.95, where="AER 100(1): 304-336, abstract", checked="2026-11-20"),
             Estimate("Amiti Redding and Weinstein (2018 tariffs)", 2019, "event study", "US import prices of goods "
                      "hit by the 2018 tariffs: tariff-inclusive prices rose by the tariff", 1.0,
                      where="Journal of Economic Perspectives 33(4): 187-210", checked="2026-11-20"),
             Estimate("Fajgelbaum et al. (2018-19 tariffs)", 2020, "regression", "variety-level US import prices: "
                      "complete pass-through of the tariffs to buyers", 1.0,
                      where="Quarterly Journal of Economics 135(1): 1-55, abstract", checked="2026-11-20"),
             Estimate("this film (US imports ex fuel)", 2026, "regression", "BLS import prices excluding fuel on the "
                      "Fed's broad dollar index, 2001-2019, twelve monthly lags: the "
                      "cumulative pass-through after a year", 0.44,
                      where="videos/economics/econ34/compute.py, item dollar", checked="2026-11-20"),
         )),
    Dial("ppp_halflife", "half-life of deviations from purchasing power parity", "years for half of a real "
         "exchange rate's deviation from its mean to disappear", (34,), status="settled within a range",
         checked="2026-11-20",
         meaning="real exchange rates do return toward parity, but slowly: half of a deviation lasts three to five "
                 "years in most estimates, longer in samples with pegs and shorter in the floating era; too slow to "
                 "blame on sticky prices alone, which is Rogoff's puzzle",
         estimates=(
             Estimate("Rogoff (the consensus)", 1996, "review", "the consensus of the long-horizon and panel "
                      "studies he surveyed: three to five years", 4.0, lo=3.0, hi=5.0,
                      where="Journal of Economic Literature 34(2): 647-668", checked="2026-11-20"),
             Estimate("this film (JST since 1870)", 2026, "regression", "18 countries against the dollar, "
                      "1870-2020, pooled AR(1) with country means", 5.2,
                      where="videos/economics/econ34/compute.py, item ppp", checked="2026-11-20"),
             Estimate("this film (JST since 1973)", 2026, "regression", "the same, 1973-2020, the floating era",
                      2.6, where="videos/economics/econ34/compute.py, item ppp",
                      checked="2026-11-20"),
         )),
    Dial("gains_from_trade", "the gains from trade", "percent of real income lost by moving to autarky (or gained by "
         "opening)", (35, 36), status="depends on the setting", checked="2026-11-20",
         meaning="the static gains from comparative advantage are a few percent of income: an upper bound of 8-9% for "
                 "Japan's opening in 1859, about 5% lost in America's embargo of 1807-09, and 1-3% for the United "
                 "States today by the one-sector formula; models with many sectors, intermediate goods and differing "
                 "firms give larger numbers",
         estimates=(
             Estimate("Bernhofen and Brown (Japan 1859)", 2005, "reconstruction", "Japan's autarky prices of "
                      "1851-53 and its trade of the 1870s: an upper bound on the gain from opening, percent of GDP",
                      8.5, lo=8.0, hi=9.0, where="American Economic Review 95(1): 208-225, abstract",
                      checked="2026-11-20"),
             Estimate("Irwin (the embargo of 1807)", 2005, "reconstruction", "the Jeffersonian embargo, December "
                      "1807 to March 1809: the welfare cost of near-autarky, percent of 1807 GNP", 5.0,
                      where="Review of International Economics 13(4): 631-645, abstract", checked="2026-11-20"),
             Estimate("Arkolakis Costinot and Rodriguez-Clare (US)", 2012, "calibration", "the United States with a "
                      "domestic share of 0.93 and trade elasticities of 5 to 10", 1.05, lo=0.7, hi=1.4,
                      where="American Economic Review 102(1): 94-130", checked="2026-11-20"),
             Estimate("this film (US 2025)", 2026, "calibration", "the same formula with imports of goods and "
                      "services over GDP in 2025 (13.8%) as the import share, elasticities 5 to 10", 2.2, lo=1.5,
                      hi=2.9, where="videos/economics/econ35/compute.py, item dials", checked="2026-11-20"),
         )),
    Dial("agglomeration", "agglomeration elasticity", "percent productivity per doubling of density", (37,),
         status="settled within a range", checked="2026-11-20",
         meaning="how much more productive a worker is where work is denser: the raw premium of dense places is "
                 "several percent per doubling, but much of it is who lives there; following the same workers "
                 "leaves one to three percent, and within a city, holding commutes fixed, about five; small per "
                 "worker, large summed over a city, and the case for letting productive cities grow",
         estimates=(
             Estimate("Ciccone and Hall", 1996, "regression", "US states' output per worker against employment "
                      "density, controlling for education", 5.5, lo=5.0, hi=6.0,
                      where="American Economic Review 86(1): 54-70; the 5-6 percent from secondary summaries",
                      checked="2026-11-20"),
             Estimate("Combes Duranton Gobillon and Roux (raw)", 2010, "regression", "306 French employment areas, "
                      "1976-1996: mean log wages on density, an elasticity of about 0.05", 3.5,
                      where="Agglomeration Economics (NBER, 2010), ch. 1, section 1.1", checked="2026-11-20"),
             Estimate("Combes Duranton Gobillon and Roux (preferred)", 2010, "IV", "the same, with worker fixed "
                      "effects, historical and geological instruments and spillovers across areas: 0.02 (0.033 "
                      "with worker effects alone)", 1.4, lo=1.4, hi=2.3,
                      where="Agglomeration Economics (NBER, 2010), ch. 1, section 1.1", checked="2026-11-20"),
             Estimate("Ahlfeldt Redding Sturm and Wolf", 2015, "structural", "Berlin's blocks in 1936, 1986 and "
                      "2006 and the Wall's division and fall: lambda = 0.071, holding travel times fixed", 5.0,
                      lo=4.3, hi=5.8, where="Econometrica 83(6): 2127-2189, Table V, column (3)",
                      checked="2026-11-20"),
             Estimate("Rosenthal and Strange (review)", 2004, "review", "the survey's range for a doubling of city "
                      "or industry size, as quoted by Ahlfeldt et al.", 5.5, lo=3.0, hi=8.0,
                      where="Handbook of Regional and Urban Economics vol. 4, ch. 49", checked="2026-11-20"),
             Estimate("this film (the Island)", 2026, "regression", "60,000 workers in 60 towns, planted at 0.03 "
                      "(2.1 percent a doubling): movers' wage changes give 0.029", 2.0,
                      where="videos/economics/econ37/compute.py, item agglo", checked="2026-11-20"),
         )),
    Dial("housing_supply", "elasticity of housing supply", "percent more housing for a 1 percent higher price",
         (37,), status="depends on the setting", checked="2026-11-20",
         meaning="how far new building, rather than price, absorbs a rise in demand for a place: below one in "
                 "coastal cities hemmed in by water, hills and rules, above three on open plains; where it is low, a "
                 "boom becomes rents and a transfer to landowners, where it is high, more homes and more people",
         estimates=(
             Estimate("Saiz (Miami)", 2010, "IV", "the least elastic of 95 large metropolitan areas, from developable "
                      "land and regulation", 0.60, where="Quarterly Journal of Economics 125(3), Table VI",
                      checked="2026-11-20"),
             Estimate("Saiz (San Francisco)", 2010, "IV", "the same", 0.66,
                      where="Quarterly Journal of Economics 125(3), Table VI", checked="2026-11-20"),
             Estimate("Saiz (one elasticity for all)", 2010, "IV", "a common elasticity across metropolitan areas, "
                      "1970-2000, instrumented with demand shocks", 1.54,
                      where="Quarterly Journal of Economics 125(3), Table III, column (1)", checked="2026-11-20"),
             Estimate("Saiz (population-weighted mean)", 2010, "IV", "the metropolitan elasticities weighted by "
                      "population (2.5 unweighted)", 1.75, where="Quarterly Journal of Economics 125(3), "
                      "introduction and conclusion", checked="2026-11-20"),
             Estimate("Saiz (Houston)", 2010, "IV", "the same table", 2.30,
                      where="Quarterly Journal of Economics 125(3), Table VI", checked="2026-11-20"),
             Estimate("Saiz (Wichita)", 2010, "IV", "the most elastic of the 95", 5.45,
                      where="Quarterly Journal of Economics 125(3), Table VI", checked="2026-11-20"),
         )),
    Dial("corruption_share", "the share of public spending lost to corruption in audited programmes",
         "percent of the money", (47,), status="depends on the setting", checked="2026-11-21",
         meaning="how much of a programme's money never reaches its purpose, where someone has measured it directly: "
                 "about a quarter of road spending in Indonesian villages before audits, at least a fifth of "
                 "subsidized rice, and four-fifths of school grants in Uganda in the mid-1990s before the transfers "
                 "were published; it depends on the programme and on whether anyone is looking, and it can be cut",
         estimates=(
             Estimate("Olken (roads, no audit)", 2007, "RCT", "over 600 Indonesian village roads: missing "
                      "expenditure where the audit probability stayed at 4 percent", 27.7,
                      where="J-PAL's summary of the JPE 115(2) study: 27.7 to 19.2 percent with audits",
                      checked="2026-11-21"),
             Estimate("Olken (roads, audited)", 2007, "RCT", "the same, where every project was audited", 19.2,
                      where="J-PAL's summary of the JPE 115(2) study", checked="2026-11-21"),
             Estimate("Olken (rice)", 2006, "survey", "Indonesia's subsidized rice: administrative records against "
                      "what households reported receiving (a lower bound)", 18.0,
                      where="Journal of Public Economics 90(4-5), abstract: at least 18 percent",
                      checked="2026-11-21"),
             Estimate("Reinikka and Svensson", 2004, "survey", "Ugandan primary schools' capitation grants, 1996 "
                      "tracking survey: the share that did not reach the schools", 80.0,
                      where="QJE 119(2): about one-fifth reached the schools", checked="2026-11-21"),
             Estimate("this film (the Island's roads, no audit)", 2026, "RCT", "600 projects, planted at 28 percent "
                      "missing without an audit", 28.0,
                      where="explainer/economics/island.py, TRUTHS[47]['roads']", checked="2026-11-21"),
         )),
    Dial("incumbency", "the incumbency advantage in close elections", "percentage points of the vote at the next "
         "election", (47,), status="contested", checked="2026-11-21",
         meaning="how much a party gains at the next election from barely winning this one, by regression "
                 "discontinuity at a margin of zero: about seven or eight points in the U.S. House and Senate; "
                 "critics show bare winners and losers in the House differ before the election, and in Indian state "
                 "elections the same design finds incumbents at a disadvantage, so the number belongs to a place and "
                 "a period",
         estimates=(
             Estimate("Lee", 2008, "RD", "U.S. House elections, 1946-1998: the party's vote share at the next "
                      "election (global quartic)", 7.7,
                      where="Journal of Econometrics 142(2), as reported by later reanalyses", checked="2026-11-21"),
             Estimate("this film (Cattaneo, Frandsen and Titiunik's Senate data)", 2026, "RD", "U.S. Senate, "
                      "1914-2010: the party's share at the seat's next election; local linear, triangular kernel, "
                      "bandwidth 17.75 points", 7.41, lo=4.56, hi=10.27,
                      where="videos/economics/econ47/compute.py, item senate (matching rdrobust's documented "
                            "conventional estimate)", checked="2026-11-21"),
         )),
    Dial("return_capital_poor", "return to capital for small firms in poor countries", "percent a month", (46,),
         status="depends on the setting", checked="2026-11-20",
         meaning="what a small firm earns on one more dollar of capital: in randomized grants to Sri Lankan and Mexican "
                 "microenterprises, 5 to 30 percent a month, far above the interest rates of banks and above most "
                 "microlenders'; but zero on average for women-owned firms in Sri Lanka, and microcredit trials find "
                 "modest average effects: high returns are real for some firms, not for the typical borrower",
         estimates=(
             Estimate("de Mel, McKenzie and Woodruff", 2008, "RCT", "Sri Lankan microenterprises given random grants "
                      "of $100 or $200", 5.0, 4.6, 5.3,
                      where="Quarterly Journal of Economics 123(4), abstract: real returns of 4.6 to 5.3 percent a "
                            "month", checked="2026-11-20"),
             Estimate("McKenzie and Woodruff", 2008, "RCT", "Mexican microenterprises given random grants in cash or "
                      "equipment", 26.5, 20.0, 33.0,
                      where="World Bank Economic Review 22(3), abstract: at least 20 to 33 percent a month",
                      checked="2026-11-20"),
             Estimate("de Mel, McKenzie and Woodruff (women)", 2009, "RCT", "the Sri Lankan grants, women-owned firms",
                      0.0, where="AEJ: Applied Economics 1(3), abstract: zero on average for female owners",
                      checked="2026-11-20"),
             Estimate("this film (the Island's best businesses)", 2026, "calibration", "the 15 percent of the "
                      "village's businesses planted with a return of 60 percent a year", 5.0,
                      where="explainer/economics/island.py, TRUTHS[46]['credit']", checked="2026-11-20"),
             Estimate("this film (the Island's other businesses)", 2026, "calibration", "the rest, planted with 5 "
                      "percent a year", 0.42,
                      where="explainer/economics/island.py, TRUTHS[46]['credit']", checked="2026-11-20"),
         )),
    Dial("cash_consumption", "the consumption effect of a cash transfer", "percent rise in household consumption",
         (46,), status="depends on the setting", checked="2026-11-20",
         meaning="how much a household's consumption rises after a large transfer: about a fifth in the year after "
                 "GiveDirectly's transfers in Kenya, with neighbours who got nothing gaining about as much through "
                 "local spending; the gains in Haushofer and Shapiro's study were no longer evident three years on, "
                 "so the size depends on the transfer, the place and the horizon",
         estimates=(
             Estimate("Haushofer and Shapiro", 2016, "RCT", "GiveDirectly's transfers of $404 or $1,525 (PPP) in rural "
                      "Kenya: monthly consumption, about nine months on", 22.2,
                      where="QJE 131(4), abstract: $158 to $193 a month (PPP); the percentage computed here",
                      checked="2026-11-20"),
             Estimate("Egger et al. (non-recipients)", 2022, "RCT", "households that got nothing, in villages where "
                      "others got about $1,000: annualized consumption 18 months on", 13.0,
                      where="NBER Working Paper 26600, text: 13 percent, roughly comparable to recipients' gains",
                      checked="2026-11-20"),
         )),
    Dial("vsl", "value of a statistical life", "millions of 2024 dollars (older figures converted with the CPI-U)",
         (18, 58), status="contested", checked="2026-11-19",
         meaning="what people accept, in pay or in time, for a small change in the risk of death, scaled up to one "
                 "death; American agencies use about $12-14 million, wage-risk studies give a few million to ten, and "
                 "the speed-limit natural experiment an upper bound near $3 million: the number moves with the method "
                 "and the people asked, and it is a rate of exchange for small risks, not the worth of a person",
         estimates=(
             Estimate("Ashenfelter and Greenstone", 2004, "DiD", "US states raising rural interstate limits to 65 mph "
                      "from 1987: hours saved per extra death, valued at the wage (an upper bound)", 3.01, 1.00, 5.02,
                      where="JPE 112(S1), abstract: $1.54m in 1997 dollars, sampling error about a third of it; "
                            "converted x 1.954 (CPI-U, 1997 to 2024)", checked="2026-11-19"),
             Estimate("EPA", 2006, "meta-analysis", "a Weibull distribution fitted to 26 studies (mostly wage-risk); "
                      "the agency's central value", 11.52,
                      where="EPA, Mortality Risk Valuation: $7.4m in 2006 dollars (s.d. $4.7m); converted x 1.556 "
                            "(CPI-U, 2006 to 2024)", checked="2026-11-19"),
             Estimate("U.S. Department of Transportation", 2024, "review", "the department's value for analyses with a "
                      "2024 base year, from wage-risk and stated-preference studies", 13.7,
                      where="DOT VSL guidance, table by base year", checked="2026-11-19"),
         )),
    Dial("preindustrial_growth", "growth of English living standards before industrialization",
         "percent a year, 1300 to 1700", (19, 46), status="contested", checked="2026-11-19",
         meaning="how fast living standards rose in the four centuries before the Industrial Revolution: day wages say "
                 "barely at all, about 0.07% a year; the same wages counting the extra days people worked, about 0.1%; "
                 "output per head, about 0.2%. At 0.07% a year income doubles in a thousand years, at 0.2% in 350: the "
                 "gap is the debate over whether England was already escaping slowly or stuck until about 1800",
         estimates=(
             Estimate("Broadberry, Campbell, Klein, Overton and van Leeuwen", 2015, "reconstruction",
                      "England's real GDP per head, built up from agriculture, industry and services, 1300 to 1700 "
                      "(784 to 1,668 pounds at 2013 prices)", 0.189,
                      where="British Economic Growth, 1270-1870 (2015), as compiled in the Bank of England's Millennium "
                            "dataset v3.1, sheet A21; compound growth computed here", checked="2026-11-19"),
             Estimate("Bank of England (day wages)", 2017, "reconstruction",
                      "real consumption wages from daily wage rates, England, 1300 to 1700 (26.5 to 35.4, 1900 = 100)",
                      0.072, where="Millennium dataset v3.1, sheet A48, the traditional measure from daily wage rates "
                                   "before 1750; compound growth computed here", checked="2026-11-19"),
             Estimate("Humphries and Weisdorf", 2019, "reconstruction",
                      "the same real wages adjusted for the days worked a year, England, 1300 to 1700 (18.2 to 27.6)",
                      0.104, where="Millennium dataset v3.1, sheet A48, the index adjusted for days worked before 1750 "
                                   "(after Humphries and Weisdorf's 2016 working paper, published in the Economic "
                                   "Journal 129(623), 2019); compound growth computed here", checked="2026-11-19"),
         )),
    Dial("discount", "the social cost of carbon, and the discount rate behind it", "dollars per tonne of CO2 (each "
         "study's own dollars)", (48, 58), status="contested", checked="2026-11-21",
         meaning="what one more tonne of carbon dioxide emitted today costs, in today's money, summed over the "
                 "centuries it stays in the air: about 30 to 90 dollars where future damages are discounted at 3 to "
                 "5 percent, nearly 200 at 2 percent, and several hundred near zero; the models agree more than the "
                 "headline numbers suggest once their discount rates are matched, and the choice of rate is partly "
                 "ethics, partly evidence about returns, so the carbon price a country should set depends on it",
         estimates=(
             Estimate("Nordhaus (DICE-2016R)", 2017, "calibration", "the social cost of carbon for 2015, 2010 dollars",
                      31.0, where="PNAS 114(7): 1518-1523, abstract", checked="2026-11-21"),
             Estimate("Barrage and Nordhaus (DICE-2023, base)", 2024, "calibration", "for 2020, 2019 dollars; the "
                      "cost-benefit optimum's is 50", 66.0, where="PNAS 121(13), Table 2", checked="2026-11-21"),
             Estimate("Barrage and Nordhaus (DICE-2023, 2%)", 2024, "calibration", "for 2020, a constant 2 percent "
                      "discount rate", 176.0, where="PNAS 121(13), Table 2", checked="2026-11-21"),
             Estimate("Stern Review", 2006, "calibration", "PAGE2002, 0.1 percent pure time preference and log "
                      "utility: over $300 a tonne of carbon", 82.0,
                      where="as reported by Anthoff, Tol and Yohe and by Hope and Newbery; $300/tC is $82/tCO2",
                      checked="2026-11-21"),
             Estimate("Rennert et al. (GIVE)", 2022, "calibration", "for 2020, 2020 dollars, a 2 percent near-term "
                      "rate; 5-95 percent range", 185.0, 44.0, 413.0, where="Nature 610: 687-692, abstract",
                      checked="2026-11-21"),
             Estimate("EPA", 2023, "review", "central estimate for 2020 emissions, 2020 dollars", 190.0,
                      where="EPA's report on the social cost of greenhouse gases (2023), as summarized by RFF and EPA",
                      checked="2026-11-21"),
             Estimate("this film (Agora's DICE-style model)", 2026, "calibration", "for 2025, 2019 dollars: "
                      "Ramsey discounting with rho 1.5 percent and eta 1.45", 63.0,
                      where="videos/economics/econ48/compute.py, scc", checked="2026-11-21"),
             Estimate("this film (the same, 2%)", 2026, "calibration", "a constant 2 percent discount rate", 183.0,
                      where="videos/economics/econ48/compute.py, scc", checked="2026-11-21"),
         )),
    Dial("energy_elasticity", "price elasticity of gasoline and of electricity", "percent change in quantity per "
         "percent change in price", (48,), status="depends on the setting", checked="2026-11-21",
         meaning="small in the short run and larger in the long run, as people change cars, appliances and where "
                 "they live: a fuel tax or a carbon price cuts emissions little in its first months and more over "
                 "years, and how much depends on the period and on how the response is measured",
         estimates=(
             Estimate("Hughes, Knittel and Sperling (gasoline, 2001-06)", 2008, "regression", "US, short run",
                      -0.055, -0.077, -0.034, where="The Energy Journal 29(1): 113-134, abstract",
                      checked="2026-11-21"),
             Estimate("Hughes, Knittel and Sperling (gasoline, 1975-80)", 2008, "regression", "US, short run",
                      -0.275, -0.34, -0.21, where="The Energy Journal 29(1): 113-134, abstract",
                      checked="2026-11-21"),
             Estimate("Havranek, Irsova and Janda (gasoline)", 2012, "meta-analysis", "long run, corrected for "
                      "publication bias", -0.31, where="Energy Economics 34(1): 201-207, abstract (as in Part 2)",
                      checked="2026-11-18"),
             Estimate("Deryugina, MacKay and Reif (electricity, 6 months)", 2020, "DiD", "Illinois towns whose "
                      "prices changed with municipal aggregation", -0.09,
                      where="AEJ: Applied 12(1): 86-114, abstract", checked="2026-11-21"),
             Estimate("Deryugina, MacKay and Reif (electricity, 2 years)", 2020, "DiD", "the same, two years later",
                      -0.27, where="AEJ: Applied 12(1): 86-114, abstract", checked="2026-11-21"),
         )),
    Dial("warming_output", "the effect of a warmer year on economic growth", "percentage points of growth per "
         "degree C", (48,), status="contested", checked="2026-11-21",
         meaning="how much a year one degree warmer than usual changes a country's growth: in hot, poor countries "
                 "about a point lower, in cool, rich ones little or nothing; whether the losses add up over the "
                 "decades or fade with adaptation is what separates small estimates of climate damage from large ones",
         estimates=(
             Estimate("Dell, Jones and Olken (poor countries)", 2012, "regression", "all countries, 1950-2003, "
                      "country and year effects", -1.3, where="AEJ: Macroeconomics 4(3): 66-95, abstract",
                      checked="2026-11-21"),
             Estimate("this film (a country averaging 25 C)", 2026, "regression", "185 countries, 1961-2023, ERA5 "
                      "temperature, World Bank growth; Burke, Hsiang and Miguel's specification", -1.03,
                      where="videos/economics/econ48/compute.py, panel: b1 + 2 b2 x 25", checked="2026-11-21"),
             Estimate("this film (poorer half, linear)", 2026, "regression", "the same data, Dell, Jones and Olken's "
                      "interaction", -0.39, -0.97, 0.19,
                      where="videos/economics/econ48/compute.py, panel: djo_poor +/- 1.96 s.e.",
                      checked="2026-11-21"),
             Estimate("this film (a country averaging 5 C)", 2026, "regression", "the same quadratic at 5 C", 0.39,
                      where="videos/economics/econ48/compute.py, panel", checked="2026-11-21"),
         )),
    Dial("loss_aversion", "loss aversion", "lambda: how many times more a loss is felt than an equal gain", (7, 45),
         status="contested", checked="2026-11-21",
         meaning="losses weigh more than equal gains in most settings, but how much depends on the setting and on how "
                 "lambda is measured: around two across a broad literature, close to one in risky choices between "
                 "modest gambles, and little at all for experienced traders handling goods meant for exchange; the "
                 "size matters for pricing, insurance, labour supply and the stickiness of defaults",
         estimates=(
             Estimate("Tversky and Kahneman", 1992, "lab", "choices between gambles; the median parameters", 2.25,
                      where="Journal of Risk and Uncertainty 5: 297-323, as used in Psychology, Built, Part 26",
                      checked="2026-11-21"),
             Estimate("Brown, Imai, Vieider and Camerer", 2024, "meta-analysis", "empirical estimates reported "
                      "1992-2017 across economics, psychology and neuroscience", 1.955, 1.820, 2.102,
                      where="Journal of Economic Literature 62(2): 485-516, abstract (95% interval)",
                      checked="2026-11-21"),
             Estimate("Walasek, Mullett and Stewart", 2024, "meta-analysis", "estimates from individual choices "
                      "between risky prospects, random effects", 1.31, 1.10, 1.53,
                      where="Journal of Economic Psychology 103: 102740, abstract (95% interval)",
                      checked="2026-11-21"),
             Estimate("this film (choices13k, prospect theory fitted)", 2026, "structural", "1,928 gamble problems "
                      "described without feedback, 31,700 choices (Peterson et al. 2021)", 1.13,
                      where="videos/economics/econ45/compute.py, item c13k (as in Psychology, Built, Part 26)",
                      checked="2026-11-21"),
         )),
    Dial("present_bias", "present bias", "beta: the weight on everything after today relative to today (1 = none)",
         (7, 45), status="depends on the setting", checked="2026-11-21",
         meaning="people are present-biased on average, most clearly over effort and consumption and much less over "
                 "money, which can be saved or borrowed; a meta-analysis of 220 convex-time-budget estimates from 28 "
                 "articles finds present bias on average, with wide variation and some selective reporting (Imai, "
                 "Rutter and Camerer 2021); the size, and whether people know it, decides the value of commitment and "
                 "of defaults",
         estimates=(
             Estimate("Laibson, Repetto and Tobacman", 2007, "structural", "US households' wealth and credit-card "
                      "borrowing over the life cycle, by simulated moments", 0.50,
                      where="NBER working paper 13314 (2007 version): beta 0.50, delta 0.99, relative risk aversion "
                            "1.3; a later revision reports annualized discount rates instead", checked="2026-11-21"),
             Estimate("Cerrone et al.", 2026, "lab", "real-effort tasks chosen for today against a future day", 0.745,
                      0.70, 0.79, where="Experimental Economics, \"Estimating present bias and sophistication over "
                                        "effort and money\", abstract (the range of estimates)",
                      checked="2026-11-21"),
             Estimate("Augenblick, Niederle and Sprenger", 2015, "lab", "choices over money paid at different dates: "
                      "virtually no present bias (shown at 1); over effort, considerably more", 1.0,
                      where="QJE 130(3): 1067-1115, abstract", checked="2026-11-21"),
             Estimate("this film (the Island's gym members)", 2026, "calibration", "planted, uniform between 0.5 and "
                      "0.95", 0.725, 0.5, 0.95, where="explainer/economics/island.py, TRUTHS[45]['gym']",
                      checked="2026-11-21"),
         )),
    Dial("default_effect", "the effect of a default", "percentage points more people ending at the default outcome",
         (42, 45), status="depends on the setting", checked="2026-11-21",
         meaning="defaults move choices a great deal when people put decisions off or read the default as advice, and "
                 "little when preferences are strong and varied; across 58 studies a meta-analysis finds d = 0.68 "
                 "(0.53 to 0.83) with wide variation (Jachimowicz et al. 2019); a default is a policy whether it is "
                 "chosen deliberately or not",
         estimates=(
             Estimate("Madrian and Shea", 2001, "event study", "401(k) participation of new hires at one large firm, "
                      "months 3 to 15 of tenure, before and after automatic enrollment (37% to 86%)", 49,
                      where="QJE 116(4): 1149-1187; the figures as the authors summarized them in the NBER Reporter "
                            "(2024)", checked="2026-11-21"),
             Estimate("this film (the Island's naive new hires)", 2026, "calibration", "participation after a year, "
                      "sign-up against automatic enrollment at 3% (63% to 98%)", 35,
                      where="videos/economics/econ45/compute.py, item enrol", checked="2026-11-21"),
             Estimate("this film (the Island's time-consistent new hires)", 2026, "calibration", "the same, with no "
                      "present bias (90% either way)", 0,
                      where="videos/economics/econ45/compute.py, item enrol", checked="2026-11-21"),
         )),
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
    Dial("crime_police", "the elasticity of crime with respect to police", "percent change in crime per percent "
         "change in police", (49,), status="contested", checked="2026-11-21",
         meaning="police go where crime is, so a simple comparison makes police look as if they cause crime; designs "
                 "that move police for reasons unrelated to crime find that more police mean less crime, by about a "
                 "third of a percent for each percent more police in London; how large the effect is for the most "
                 "costly crimes, murder above all, decides whether cities have too few officers or too many",
         estimates=(
             Estimate("Levitt (murder)", 1997, "IV", "US cities, 1970-92, police hired before mayoral and "
                      "gubernatorial elections", -3.05, -7.11, 1.01,
                      where="American Economic Review 87(3), as quoted by Chalfin and McCrary (2018): -3.05 +/- 4.06",
                      checked="2026-11-21"),
             Estimate("Evans and Owens (murder)", 2007, "IV", "US cities, federal COPS hiring grants", -0.84, -1.78,
                      0.10, where="Journal of Public Economics 91, as quoted by Chalfin and McCrary (2018): -0.84 +/- "
                      "0.94", checked="2026-11-21"),
             Estimate("Draca, Machin and Witt", 2011, "IV", "London's boroughs after the July 2005 bombings: police "
                      "moved to central London", -0.35, -0.4, -0.3,
                      where="American Economic Review 101(5): 2157-2181, abstract (about -0.3 to -0.4)",
                      checked="2026-11-21"),
         )),
    Dial("class_size", "the effect of a smaller class on test scores", "percentile points from a class of 13-17 "
         "rather than 22-25 pupils", (49,), status="contested", checked="2026-11-21",
         meaning="Tennessee's experiment found a few percentile points for a class a third smaller, more for poor and "
                 "black pupils; designs on other data range from that to nothing; at the cost of a third more "
                 "teachers, whether smaller classes beat other uses of the money turns on which estimate holds where",
         estimates=(
             Estimate("Krueger (STAR, first year)", 1999, "RCT", "Tennessee, 79 schools, 1985-89: pupils and teachers "
                      "assigned at random within schools", 4.0,
                      where="Quarterly Journal of Economics 114(2), abstract: about 4 percentile points the first year "
                            "in a small class", checked="2026-11-21"),
             Estimate("this film (STAR, kindergarten)", 2026, "RCT", "5,786 kindergarteners, reading and maths "
                      "percentiles against regular classes, within schools, errors clustered by school", 5.63, 2.82,
                      8.44, where="videos/economics/econ49/compute.py, item star", checked="2026-11-21"),
             Estimate("Angrist, Lavy, Leder-Luis and Shany", 2019, "RD", "Israel, 2002-2011: Maimonides' rule with "
                      "later data", 0.0, where="AER: Insights 1(3): 309-324, abstract: no effect, a precisely "
                      "estimated zero", checked="2026-11-21"),
         )),
    Dial("teacher_va", "the spread of teachers' effects", "standard deviations of pupils' scores from a teacher one "
         "standard deviation better", (49,), status="settled within a range", checked="2026-11-21",
         meaning="a teacher one standard deviation better raises a class's scores by about a tenth of a standard "
                 "deviation in a year, and the gains show up in earnings; how far value added can be used to hire, "
                 "pay or dismiss teachers turns on whether it is biased by which pupils a teacher gets, and on how "
                 "noisy a few years of classes are",
         estimates=(
             Estimate("Chetty, Friedman and Rockoff (maths)", 2014, "regression", "New York City-area district, "
                      "grades 3-8, 1989-2009, value added validated by teachers' moves", 0.14,
                      where="American Economic Review 104(9), 'Measuring the Impacts of Teachers I', NBER WP 19423",
                      checked="2026-11-21"),
             Estimate("Chetty, Friedman and Rockoff (English)", 2014, "regression", "the same", 0.10,
                      where="as above", checked="2026-11-21"),
             Estimate("Hanushek and Rivkin (reading)", 2010, "review", "the average across the studies they survey",
                      0.13, where="American Economic Review 100(2): 267-271", checked="2026-11-21"),
         )),
    Dial("idiosyncratic_share", "how much of the cycle comes from firms' and sectors' own shocks", "share of the "
         "variance of aggregate output growth", (63,), status="contested", checked="2026-11-21",
         meaning="the old view was that millions of firm-level shocks cancel out, leaving the cycle to aggregate "
                 "shocks; with fat-tailed firm sizes and lopsided input-output networks they need not, and estimates "
                 "of their share range from about a third to more than half, depending on the period, the data and "
                 "how much the elasticities of substitution are allowed to amplify sectoral shocks",
         estimates=(
             Estimate("Gabaix", 2011, "regression", "the 100 largest American firms: output growth on their "
                      "idiosyncratic growth (the granular residual)", 0.33, where="Econometrica 79(3): 733-772, "
                      "abstract (about one third)", checked="2026-11-21"),
             Estimate("Foerster, Sarte and Watson", 2011, "structural", "American industrial production by "
                      "industry, quarterly, after the mid-1980s", 0.5, where="Journal of Political Economy 119(1), "
                      "abstract (about half)", checked="2026-11-21"),
             Estimate("Atalay", 2017, "structural", "American industries, with the elasticities of substitution "
                      "estimated rather than set to one: at least half", 0.5, where="American Economic Journal: "
                      "Macroeconomics 9(4), working-paper abstract", checked="2026-11-21"),
             Estimate("this film (the Island's granular residual)", 2026, "regression", "1,000 Zipf-sized firms, 40 "
                      "years: the median R-squared over 400 histories, 5th to 95th percentile; the planted share is "
                      "0.34", 0.27, lo=0.09, hi=0.49, where="videos/economics/econ63/compute.py, item dials",
                      checked="2026-11-21"),
         )),
    Dial("input_substitution", "how easily firms swap one input for another within a year", "elasticity of "
         "substitution between intermediate inputs, short run", (63,), status="settled within a range",
         checked="2026-11-21",
         meaning="within a year, firms can hardly replace one input with another: the estimates are well below one, "
                 "near zero to about 0.2, so production networks behave almost like Leontief's and large shocks to "
                 "essential inputs cost more than their sales share; over longer horizons substitution is easier, "
                 "and how much easier is still being measured",
         estimates=(
             Estimate("Atalay (range of specifications)", 2017, "structural", "American industries' input "
                      "shares and prices: the elasticity among intermediate inputs", 0.075, lo=0.0, hi=0.15,
                      where="American Economic Journal: Macroeconomics 9(4), working paper", checked="2026-11-21"),
             Estimate("Boehm, Flaaen and Pandalai-Nayar", 2019, "event study", "Japanese-owned plants in America "
                      "after the 2011 earthquake: among material inputs", 0.2, where="Review of Economics and "
                      "Statistics 101(1): 60-75 (structural estimate in the working paper)", checked="2026-11-21"),
             Estimate("this film (the Island's input-output tables)", 2026, "regression", "eight sectors, 30 years "
                      "of cost shares and prices, pair fixed effects; planted 0.15", 0.16, lo=0.14, hi=0.19,
                      where="videos/economics/econ63/compute.py, item dials", checked="2026-11-21"),
         )),
    Dial("algorithm_gain", "what an algorithm adds to a judge's decision", "proportional fall in the outcome "
         "to be prevented (crime, failure to appear) at the same detention rate, from ranking cases by a model",
         (64,), status="depends on the setting", checked="2026-11-21",
         meaning="where the decision is a prediction and the records carry most of the signal, ranking by a model "
                 "can prevent a sixth to a quarter more of the bad outcomes at the same detention rate; the estimate "
                 "rests on a design that copes with selective labels (random assignment of judges, contraction), "
                 "and shrinks when the judges see what the records do not",
         estimates=(
             Estimate("Kleinberg, Lakkaraju, Leskovec, Ludwig and Mullainathan", 2018, "structural", "New York City "
                      "bail decisions, 2008-13: crime at the judges' jailing rate, up to", 0.247,
                      where="Quarterly Journal of Economics 133(1): 237-293, abstract", checked="2026-11-21"),
             Estimate("this film (the Island, truth)", 2026, "regression", "the test half, with every defendant's "
                      "outcome known: failures at the judges' detention rate", 0.18,
                      where="videos/economics/econ64/compute.py, item courts", checked="2026-11-21"),
             Estimate("this film (the Island, contraction)", 2026, "regression", "the most lenient fifth of judges' "
                      "cases contracted to four stricter fifths' detention rates: the range", 0.157, lo=0.146,
                      hi=0.165, where="videos/economics/econ64/compute.py, item contraction", checked="2026-11-21"),
         )),
]}

# What each part shows without entering a row, and why: {part: [(what is shown, the reason)]}
SHOWN = {
    64: [
        ("Kleinberg, Lakkaraju, Leskovec, Ludwig and Mullainathan (2018); Lakkaraju et al. (2017)", "the hook's "
         "story and the Dial; the Island's courts, contraction and selective labels computed"),
        ("Kleinberg, Ludwig, Mullainathan and Obermeyer (2015); Mullainathan and Spiess (2017)", "prediction policy "
         "problems, stated"),
        ("Meehl (1954); Grove, Zald, Lebow, Snitz and Nelson (2000)", "clinical against statistical prediction: "
         "Called it?, stated"),
        ("Obermeyer, Powers, Vogeli and Mullainathan (2019)", "the label choice, stated"),
        ("Chernozhukov et al. (2018); Robinson (1988)", "double machine learning, computed by Monte Carlo"),
        ("Wager and Athey (2018); Athey and Wager (2021); Kitagawa and Tetenov (2018)", "causal forests and policy "
         "learning, computed on the Island's programme"),
        ("Gentzkow, Kelly and Taddy (2019); Jean et al. (2016); Angelopoulos et al. (2023)", "text and images as "
         "data, stated; prediction-powered inference computed"),
        ("Brock and Mirman (1972); Maliar, Maliar and Winant (2021); Azinovic, Gaegauf and Scheidegger (2022)",
         "deep learning as a solution method, computed with the series' autodiff"),
        ("Calvano, Calzolari, Denicolo and Pastorello (2020); Zheng et al. (2022)", "learning agents: Part 44's "
         "Q-learners computed; the AI Economist stated"),
        ("Horton (2023); Ludwig and Mullainathan (2024)", "language models as subjects and assistants, stated"),
        ("Angwin et al. (2016); Chouldechova (2017); Kleinberg, Mullainathan and Raghavan (2017)", "fairness, stated; "
         "the Island's two groups computed"),
        ("Rupp, Microprocessor Trend Data, via Our World in Data", "the intermission, from the Data Room"),
    ],
    63: [
        ("Carvalho, Nirei, Saito and Tahbaz-Salehi (2021)", "the hook's story, stated; the Island's supply web "
         "computed"),
        ("Leontief (1936); Domar (1961); Antras, Chor, Fally and Hillberry (2012)", "input-output paths and "
         "upstreamness, computed on the Island's table"),
        ("Hulten (1978); Baqaee and Farhi (2019)", "Hulten's theorem and its second-order terms, computed on the "
         "Island's CES network"),
        ("Lucas (1977); Gabaix (2011); Acemoglu, Carvalho, Ozdaglar and Tahbaz-Salehi (2012)", "granular and "
         "network volatility: the Dial's rows; Zipf firms, stars and rings computed"),
        ("Barrot and Sauvagnat (2016); Boehm, Flaaen and Pandalai-Nayar (2019)", "supply chains measured, stated; "
         "the Dial's rows"),
        ("Kremer (1993); Challenger (1986)", "the O-ring, computed"),
        ("Eisenberg and Noe (2001); Acemoglu, Ozdaglar and Tahbaz-Salehi (2015); Elliott, Golub and Jackson (2014)",
         "financial networks: a clearing example and ring against complete contagion computed"),
        ("Granovetter (1973); Rajkumar et al. (2022)", "weak ties: Called it?, stated; the two forces illustrated"),
        ("Banerjee, Chandrasekhar, Duflo and Jackson (2013)", "diffusion, stated; the Island's village computed"),
        ("Ballester, Calvo-Armengol and Zenou (2006); Manski (1993); Bramoulle, Djebbari and Fortin (2009)",
         "the key player computed; peer effects' identification stated"),
        ("Jackson and Wolinsky (1996)", "network formation, computed for four players"),
        ("Elliott, Golub and Leduc (2022)", "fragile supply networks, computed"),
        ("OECD via FRED: JPNPROINDMISMEI", "the intermission, from the Data Room"),
    ],
    62: [
        ("Bloom, Eifert, Mahajan, McKenzie and Roberts (2013)", "the hook's story and the management Dial; the "
         "Island's experiment computed"),
        ("Syverson (2004, 2011)", "productivity dispersion, stated; the Island's industry computed"),
        ("Bloom and Van Reenen (2007)", "measuring management, stated; the Island's scores computed"),
        ("Bruhn, Karlan and Schoar (2018)", "consulting in Mexico, stated"),
        ("Lazear (2000); Benson, Li and Shue (2019); Peter and Hull (1969)", "piece rates and promotion, stated; "
         "the Island's workers and teams computed"),
        ("Gabaix and Landier (2008); Bertrand and Mullainathan (2001); Jensen and Murphy (1990); Hall and Liebman "
         "(1998)", "executive pay: the Dial's rows; the assignment model and pay for luck computed"),
        ("Modigliani and Miller (1958); Myers and Majluf (1984); Graham and Harvey (2001)", "capital structure, "
         "stated; the trade-off computed"),
        ("Jensen and Meckling (1976); Bennedsen, Nielsen, Perez-Gonzalez and Wolfenzon (2007)", "agency and "
         "governance, stated; the owner-manager computed"),
        ("Davis, Haltiwanger, Handley, Jarmin, Lerner and Miranda (2014)", "private equity, stated; the Island's "
         "buyouts computed"),
        ("Garicano (2000); Bloom, Garicano, Sadun and Van Reenen (2014)", "knowledge hierarchies, computed; the "
         "evidence stated"),
        ("Bloom, Liang, Roberts and Ying (2015); Bloom, Han and Liang (2024)", "working from home, stated; the "
         "Island's trial computed"),
        ("Gibbons and Henderson (2012); NUMMI (1984)", "relational contracts and copying, stated; Part 14's model "
         "computed"),
        ("Berger and Ofek (1995); Moeller, Schlingemann and Stulz (2005); DaimlerChrysler (1998, 2007)", "mergers, "
         "stated; the Island's conglomerates computed"),
        ("Brynjolfsson, Li and Raymond (2023, 2025)", "generative AI at work, stated"),
        ("BLS via FRED: OPHNFB", "the intermission, from the Data Room"),
    ],
    61: [
        ("Hall, Kendrick and Nosko (2015)", "the hook's story, stated; the Island's night computed"),
        ("Rochet and Tirole (2003); Einav, Farronato and Levin (2016); Athey and Luca (2019)", "platforms as designed "
         "markets and economists in tech, stated"),
        ("Cohen, Hahn, Hall, Levitt and Metcalfe (2016)", "consumer surplus from surge, stated; the Dial's rows"),
        ("the New York Attorney General's agreement with Uber (2014)", "the emergency cap, stated"),
        ("Ursu (2018); European Commission, AT.39740 (2017); Court of Justice, C-48/22 P (2024)", "ranking and "
         "self-preferencing, stated; the Island's click model computed"),
        ("Nosko and Tadelis (2015); Fradkin, Grewal and Holtz (2021); Tadelis (2016)", "reputation, stated; the "
         "Island's ratings computed"),
        ("Varian (2007); Edelman, Ostrovsky and Schwarz (2007); Ostrovsky and Schwarz (2009)", "ad auctions, stated; "
         "the reserve Dial returns"),
        ("Blake, Nosko and Tadelis (2015); Lewis and Rao (2015)", "advertising's returns: the Dial's rows; the "
         "arithmetic of power computed for the Island"),
        ("Deng, Xu, Kohavi and Walker (2013); Kohavi, Tang and Xu (2020)", "experimentation practice, stated; peeking "
         "and CUPED computed on the Island"),
        ("Johari, Li, Liskovich and Weintraub; Bajari et al. (2023)", "two-sided randomization, stated; the Island's "
         "switchback computed"),
        ("Athey, Chetty, Imbens and Kang (2019)", "the surrogate index, computed on the Island"),
        ("Chen, Chevalier, Rossi and Oehlsen (2019); Cook, Diamond, Hall, List and Oyer (2021); AB5 (2019); "
         "Proposition 22 (2020); Uber v Aslam (2021)", "gig work and the law, stated; flexibility computed on the "
         "Island"),
        ("Brynjolfsson, Collis and Eggers (2019); Athey, Catalini and Tucker (2017)", "free goods and privacy, "
         "stated; the Island's survey computed"),
        ("Census Bureau via FRED: ECOMPCTSA", "the intermission, from the Data Room"),
    ],
    60: [
        ("Smith, Leimkuhler and Darrow (1992); People Express and American Airlines, 1981-86", "the hook's story, "
         "stated; the Island's flight computed"),
        ("Hall and Hitch (1939); Blinder, Canetti, Lebow and Rudd (1998)", "what firms say, stated; the markup's "
         "robustness computed"),
        ("Murphy, Allen, Stevens and Weatherhead (2005); Becker, DeGroot and Marschak (1964)", "measuring willingness "
         "to pay, stated; a conjoint survey computed on the Island"),
        ("Blake and Coey (2014)", "interference in marketplace experiments, stated; the Island's hotel test computed"),
        ("Littlewood (1972); Belobaba (1987); Gallego and van Ryzin (1994)", "revenue management, computed on the "
         "Island"),
        ("Williams (2022); Hortacsu, Ory and Williams", "dynamic pricing's welfare, stated"),
        ("Mussa and Rosen (1978); Deneckere and McAfee (1996); Bakos and Brynjolfsson (1999)", "versions and bundles, "
         "computed on the Island; damaged goods, stated"),
        ("Blake, Moshary, Sweeney and Tadelis (2021); the FTC's fee rule (2024)", "drip pricing, stated"),
        ("DellaVigna and Gentzkow (2019)", "uniform pricing: the Dial row; the Island's chain computed"),
        ("Calvano, Calzolari, Denicolo and Pastorello (2020); United States v. RealPage (2024); United States v. Apple "
         "(2013)", "algorithms and clauses, stated"),
        ("BLS via FRED: CUSR0000SAF11, WPU02", "the pass-through chapter and the intermission, from the Data Room"),
        ("Misra, Schwartz and Abernethy (2019)", "bandit pricing, stated; Thompson sampling computed on the Island"),
    ],
    59: [
        ("FTC v. Staples (D.D.C. 1997); the FTC's case summary", "the hook's story, stated; the Island's price map "
         "computed"),
        ("the Clayton Act, section 7; Hart-Scott-Rodino (1976); Philadelphia National Bank (1963); Baker Hughes "
         "(1990)", "the law and the burden of proof, stated"),
        ("Harris and Simons (1989); Katz and Shapiro (2003); O'Brien and Wickelgren (2003); du Pont (1956)",
         "market definition: the test computed on the Island; the critical-loss debate and cellophane, stated"),
        ("the Horizontal Merger Guidelines (1982, 2010, 2023)", "the presumptions, applied to the Island's "
         "industries"),
        ("Farrell and Shapiro (2010); Crooke, Froeb, Tschantz and Werden (1999)", "pricing pressure and the "
         "functional-form problem, computed on the Island"),
        ("United States v. AT&T (D.D.C. 2018; D.C. Cir. 2019)", "the vertical case, stated; the bargaining model "
         "computed on the Island"),
        ("Abrantes-Metz, Froeb, Geweke and Taylor (2006)", "the variance screen: computed on the Island's cement; "
         "the frozen-perch case, stated"),
        ("Daubert (1993); Kumho Tire (1999); Federal Rule of Evidence 702 (2023); Ashenfelter, Ashmore, Baker, "
         "Gleason and Hosken (2006)", "regression in court: the standard stated; the cross-examination computed on "
         "the Island; Staples' 8.6% and 0.9%, stated"),
        ("Prager and Schmitt (2021); Krueger and Ashenfelter (2022); the 2023 Merger Guidelines, Guideline 10",
         "labour markets, stated; the Island's hospitals computed"),
        ("Brot-Goldberg, Cooper, Craig and Klarnet (2024)", "hospital merger enforcement, stated"),
        ("Hope Natural Gas (1944); Littlechild (1983); Baumol and Willig's rule", "regulated prices, stated; the "
         "Island's utility computed"),
        ("BLS via FRED: CUUR0000SETG01, CPIAUCNS; BLS, Monthly Labor Review (2005)", "the intermission's data film, "
         "from the Data Room; the index caveat, stated"),
        ("FTC v. Meta (D.D.C. 2025)", "the frontier, stated"),
    ],
    55: [
        ("Sims (1980, 1992)", "the hook's price puzzle, recomputed on FRED data; VARs stated"),
        ("Blanchard and Quah (1989); Uhlig (2005); Stock and Watson (2012, 2018); Mertens and Ravn (2013); Rigobon "
         "(2003); Baumeister and Hamilton (2015)", "the five schemes, stated and computed on the Island"),
        ("Jorda (2005); Plagborg-Moller and Wolf (2021); Li, Plagborg-Moller and Wolf (2024)", "local projections, "
         "stated and computed on the Island"),
        ("Romer and Romer (2004); Kuttner (2001); Gurkaynak, Sack and Swanson (2005); Gertler and Karadi (2015); "
         "Nakamura and Steinsson (2018)", "narrative and high-frequency instruments, stated; Part 31's Island "
         "computed"),
        ("An and Schorfheide (2007); Smets and Wouters (2007); Canova and Sala (2009)", "DSGE estimation and weak "
         "identification, stated and computed on the Island"),
        ("Nakamura and Steinsson (2014); Wolf (2023); Goldsmith-Pinkham, Sorkin and Swift (2020); Borusyak, Hull and "
         "Jaravel (2022)", "cross-sectional macro, stated; Part 32's regions computed"),
        ("Christiano, Eichenbaum and Evans (2005)", "impulse-response matching, computed on the Island"),
        ("Ramey (2016); Nakamura and Steinsson (2018, JEP)", "what macroeconomics knows, stated"),
        ("Federal Reserve Board, FRED: GS10, TB3MS, USREC, INDPRO, CPIAUCSL, FEDFUNDS, PPIACO", "the hook's VARs "
         "and the intermission, from the Data Room"),
    ],
    58: [
        ("The Flood Control Act (1936); Dupuit (1844)", "the hook: the act's sentence and the first measure of "
         "surplus, stated"),
        ("Boardman et al. (2018); HM Treasury, The Green Book; OMB Circular A-4", "the method, stated; the Island's "
         "bridge computed"),
        ("US DOT (2016); Norway's NOU 1997:27", "the value of time and the cost of public funds, stated and used"),
        ("Rosen (1974); Hotelling (1947) and Clawson (1959); Desvousges et al. (1993); Carson et al. (2003); the NOAA "
         "panel (1993); Diamond and Hausman (1994)", "values without prices: hedonic and travel-cost methods computed "
         "on the Island; stated preference, stated"),
        ("Schelling (1968); Thaler and Rosen (1976); Viscusi and Aldy (2003); EPA (2003)", "a statistical life: the "
         "Dial; the wage-risk regression computed on the Island; the senior discount, stated"),
        ("Saez (2001); Gruber and Saez (2002)", "the Play-it score: the formula, and the Dials' elasticity of taxable "
         "income"),
        ("Weitzman (1998, 2001); Drupp et al. (2018); HM Treasury (2026)", "discounting: the Dial; Weitzman's rate "
         "computed"),
        ("CBO (eval-projections); CBO (2018, 2025); JCT (2017); Auerbach (2005)", "budget scoring: CBO's record "
         "computed from its files; the scores of 2017 and 2025, stated"),
        ("NBER TAXSIM; EUROMOD", "microsimulation, stated; the Island's calculator computed"),
        ("Harberger (1962); Kehoe (2005)", "general equilibrium: the Island's model computed; NAFTA's models, stated"),
        ("Flyvbjerg, Holm and Buhl (2002, 2005); Kahneman and Lovallo (1993); Dixit and Pindyck (1994); Hendren and "
         "Sprung-Keyser (2020)", "risk and the record: the Dial; the reference class and the option computed on the "
         "Island; the MVPF league table, stated"),
        ("Executive Orders 12291 (1981) and 12866 (1993)", "regulatory impact analysis, stated; the Island's rule "
         "computed"),
        ("Goodhart (1975); Campbell (1979); Bevan and Hood (2006)", "targets, stated; the Island's emergency "
         "department simulated"),
        ("OMB Circular A-4 (2023); HM Treasury (2021)", "the frontier, stated"),
        ("CBO, eval-projections; FRED: DFII10", "the data, from the Data Room"),
    ],
    57: [
        ("Samuelson (1966); An, Jalles and Loungani (2018)", "the hook's two scorecards, stated"),
        ("Mankiw and Shapiro (1986); BLS benchmark releases (2024, 2025, 2026)", "revisions, stated; first and "
         "latest estimates computed from the real-time data set"),
        ("Shiskin, Young and Musgrave (1967)", "X-11, stated and computed in simplified form on payrolls"),
        ("Stock and Watson (2002); Giannone, Reichlin and Small (2008); GDPNow; the New York Fed staff nowcast",
         "nowcasting, stated; bridge equations on FRED data and a factor model on the Island computed"),
        ("Estrella and Mishkin (1998); Sahm (2019)", "recession signals, computed on FRED data"),
        ("Diebold and Mariano (1995); Romer and Romer (2000); Bates and Granger (1969); Stock and Watson (2004)",
         "forecast scoring and combination, computed on the SPF and Greenbook data"),
        ("Hamilton (1989); Lucas (1976)", "regime switching, computed on a simulated economy; the critique, stated"),
        ("Cavallo and Rigobon (2016); Chetty et al. (2024); Henderson, Storeygard and Weil (2012)", "new data, "
         "stated as findings"),
        ("Baker, Bloom and Davis (2016); Hansen, McMahon and Prat (2018); Gentzkow, Kelly and Taddy (2019)",
         "text as data: the index plotted from FRED; the others stated"),
        ("Bernanke (2024); the Bank of England's fan chart (1996); the IPCC's calibrated language", "communicating "
         "uncertainty, stated"),
        ("Halawi et al. (2024); Blanchet, Saez and Zucman (2022)", "the frontier, stated"),
        ("Philadelphia Fed (real-time data set, SPF, Greenbook); FRED: PAYEMS, PAYNSA, GDPC1, INDPRO, GDPDEF, GS10, "
         "TB3MS, USREC, UNRATE, SAHMREALTIME, USEPUINDXM", "the data, from the Data Room"),
    ],
    56: [
        ("Samuelson (1947); Mas-Colell, Whinston and Green (1995); Ljungqvist and Sargent (2000); Hayashi (2000); "
         "Gali (2008)", "where the core came from: the textbooks, stated"),
        ("Slutsky (1915); Burtless and Hausman (1978); Pigou (1920); Coase (1960); Vickrey (1961); Myerson (1981); "
         "Riley and Samuelson (1981); Mussa and Rosen (1978); Maskin and Riley (1984)", "the micro questions' models, "
         "stated and computed by Agora's exam module"),
        ("Ramsey (1928); Cass (1965); Koopmans (1965); Chamley (1986); McCall (1970); Shavell and Weiss (1979); "
         "Kydland and Prescott (1977); Barro and Gordon (1983); Clarida, Gali and Gertler (1999); Huggett (1993); "
         "Aiyagari (1994); Chamberlain and Wilson (2000)", "the macro questions' models, stated and computed"),
        ("Katz and Meyer (1990); Card, Chetty and Weber (2007)", "the exit spike at benefit exhaustion, stated as "
         "findings; no estimate is shown"),
        ("Philip Wright (1928); Wald (1940); Hansen (1982); Hansen and Singleton (1982); de Chaisemartin and "
         "D'Haultfoeuille (2020); Goodman-Bacon (2021); Callaway and Sant'Anna (2021); Borusyak, Jaravel and Spiess "
         "(2024); Blanchard and Quah (1989); Faust and Leeper (1997); Gali (1999)", "the econometrics questions' "
         "methods, stated and computed on simulated data"),
        ("Saez (2010); Kleven (2016); Ostrovsky and Schwarz; Rochet and Chone (1998); Straub and Werning (2020); "
         "Kolsrud, Landais, Nilsson and Spinnewijn (2018); Kaplan, Moll and Violante (2018); Andrews, Stock and Sun "
         "(2019); Roth, Sant'Anna, Bilinski and Poe (2023); Christiano, Eichenbaum and Vigfusson (2004)",
         "the frontier: open questions, stated, with no numbers"),
        ("BLS and NBER via FRED: UEMPMED, USREC", "the intermission's data film, from the Data Room"),
    ],
    54: [
        ("McFadden (1974, 2001, 2002)", "the hook's BART forecast (the Called it? record of Part 5) and the logit, "
         "computed on the Island"),
        ("Marschak (1953); Lucas (1976); Koopmans (1949)", "structural models and identification, stated"),
        ("Hansen (1982); Hansen and Singleton (1982)", "GMM and the Euler equation, computed on the Island"),
        ("McFadden (1989); Pakes and Pollard (1989); Gourieroux, Monfort and Renault (1993); Smith (1993)",
         "simulated moments and indirect inference, computed"),
        ("Gourinchas and Parker (2002)", "the method, applied to the Island's households; no estimate of theirs "
         "is shown"),
        ("Rust (1987); Hotz and Miller (1993); Keane and Wolpin (1997); Heckman (1981); Heckman and Singer (1984)",
         "dynamic choice and hidden types, stated and computed on the Island"),
        ("Andrews, Gentzkow and Shapiro (2017)", "the sensitivity matrix, computed"),
        ("Kydland and Prescott (1982, 1996); Hansen and Heckman (1996)", "the calibration debate, stated"),
        ("Baily (1978); Chetty (2006, 2009)", "sufficient statistics, computed on Part 42's model"),
        ("Todd and Wolpin (2006)", "PROGRESA's validation, stated without numbers; the Island's version computed"),
        ("Manski (1990, 2003)", "bounds, computed on the Island"),
        ("Ginsberg et al. (2009); Lazer, Kennedy, King and Vespignani (2014)", "the Called it? card, stated"),
        ("Federal Highway Administration, vehicle miles travelled", "the intermission's data, shown from the Data "
         "Room"),
    ],
    53: [
        ("Kamenica and Gentzkow (2011)", "the hook's prosecutor and the persuasion chapter, computed"),
        ("Harsanyi (1967-68); Cho and Kreps (1987); Kreps and Wilson (1982)", "the theory, stated and computed on "
         "examples"),
        ("Crawford and Sobel (1982); Bergemann and Morris (2005, 2016, 2019); Blackwell (1953)", "the models, "
         "computed here"),
        ("Aumann (1976); Geanakoplos and Polemarchakis (1982); Rubinstein (1989)", "common knowledge, computed on "
         "examples"),
        ("Carlsson and van Damme (1993); Morris and Shin (1998, 2003)", "the global game, computed"),
        ("Banerjee (1992); Bikhchandani, Hirshleifer and Welch (1992)", "cascades, computed exactly and simulated"),
        ("Selten (1978); Milgrom and Roberts (1982); Nash (1950); Rubinstein (1982); Coase (1972); Bull (1987); Levin "
         "(2003)", "the models, stated and computed"),
        ("Camerer, Ho and Chong (2004); Nagel (1995); DellaVigna and Kaplan (2007)", "the reasoning_depth dial and "
         "the persuasion rate, stated"),
        ("Financial Crisis Inquiry Commission (2011); US Senate PSI (2011)", "the Called it? card, stated"),
        ("University of Michigan, Surveys of Consumers; BLS CPI", "the intermission's data, shown from the Data Room"),
    ],
    52: [
        ("Kirman (1992); Krusell and Smith (1998); Kaplan, Moll and Violante (2018)", "the hook's essay, finding and "
         "reversal, stated"),
        ("Gorman (1953); Bewley (1977); Huggett (1993); Aiyagari (1994); Chamberlain and Wilson (2000)",
         "the theory, stated and computed on the Island"),
        ("Young (2010); Den Haan (2010); Den Haan, Judd and Juillard (2010)", "the methods and calibration, computed "
         "here"),
        ("Benhabib, Bisin and Zhu (2011, 2015); Federal Reserve, Distributional Financial Accounts", "the wealth "
         "chapter: the mechanism computed, the top shares shown from the Data Room"),
        ("Achdou, Han, Lasry, Lions and Moll (2022); Auclert, Bardóczy, Rognlie and Straub (2021)", "the methods, "
         "computed here"),
        ("Werning (2015); Kaplan and Violante (2014); Auclert, Rognlie and Straub (the intertemporal Keynesian cross); "
         "McKay, Nakamura and Steinsson (2016)", "results stated and reproduced in this part's economy"),
        ("Doepke and Schneider (2006)", "the inflation chapter's finding, stated"),
        ("Hopenhayn (1992); Khan and Thomas (2008); Haltiwanger, Jarmin and Miranda (2013)", "the firms chapter: "
         "Hopenhayn computed, the others stated"),
        ("Johnson, Parker and Souleles (2006); Parker et al. (2013, 2022); Kueng (2018); Jappelli and Pistaferri "
         "(2014); Fagereng, Holm and Natvik (2021)", "the mpc_windfall dial, read against the models"),
        ("Krusell and Smith (1998)", "the Called it? card"),
        ("Auclert, Rognlie and Straub (2020)", "the frontier chapter, stated"),
    ],
    51: [
        ("Bellman (1957, 1984); Dreyfus (2002)", "the hook's story, stated"),
        ("Howard (1960); Blackwell (1965); Banach (1922)", "the methods and theorems, computed on the growth model"),
        ("Judd (1992); Den Haan and Marcet (1994); Aruoba, Fernández-Villaverde and Rubio-Ramírez (2006)",
         "Euler-equation errors and the comparison of methods, computed here"),
        ("Carroll (2006); Tauchen (1986); Rouwenhorst (1995); Kopecky and Suen (2010); Runge (1901)",
         "the methods, computed here"),
        ("Achdou, Han, Lasry, Lions and Moll (2022); Guerrieri and Iacoviello (2015); Smolyak (1963); Krueger and "
         "Kubler (2004); Schmitt-Grohé and Uribe (2004)", "the methods, computed here"),
        ("Hall (1988); Vissing-Jorgensen (2002); Gruber (2013); Havranek (2015)", "the eis dial, read against method "
         "error"),
        ("Moore (1965, 1975)", "the Called it? card; the transistor counts shown from the Data Room"),
        ("Rust (1987); FRB/US; Dynare", "practice, stated"),
        ("Maliar, Maliar and Winant (2021); Azinovic, Gaegauf and Scheidegger (2022)", "the frontier chapter, "
         "stated"),
    ],
    50: [
        ("American Rescue Plan Act (2021); Census Bureau (2022, 2023)", "the hook's payments and the poverty "
         "measures, stated; the official rate since 1989 shown from the Data Room"),
        ("Chetty, Guren, Manoli and Weber (2011); Gruber and Saez (2002); Diamond and Saez (2011); Hendren and "
         "Sprung-Keyser (2020)", "the labour_supply, eti and mvpf dials, read for the memo"),
        ("Ananat, Glasner, Hamilton and Parolin (2022); Baker, Messacar and Stabile (2023)", "stated as the evidence "
         "on work and poverty; one temporary and one foreign policy, so not entered as a dial"),
        ("Aizer, Eli, Ferrie and Lleras-Muney (2016); Milligan and Stabile (2011)", "stated as the long-run "
         "evidence"),
        ("Corinth, Meyer, Stadnicki and Wu (2021)", "stated, and the Called it? card"),
        ("Orcutt (1957)", "the microsimulation, computed on the Island"),
        ("Milligan (2005); Egger et al. (2022)", "stated in the chapter on the wider economy"),
        ("Noble, Magnuson, Duncan, Gennetian et al. (2025)", "the frontier chapter, stated"),
    ],
    49: [
        ("Becker (1968, 1992)", "the hook's story and the model of crime, computed on the Island"),
        ("Di Tella and Schargrodsky (2004); Draca, Machin and Witt (2011); Chalfin and McCrary (2018); Levitt "
         "(1997); Evans and Owens (2007)", "stated and entered in the crime_police dial; the biases computed on the "
         "Island"),
        ("Ehrlich (1975); Leamer (1983); McManus (1985)", "stated; the 1950 murder rates shown from the Data Room"),
        ("Becker (1965, 1973); Choo and Siow (2006); Goldin and Katz (2002)", "stated; household production and the "
         "marriage market computed on the Island; participation shown from the Data Room"),
        ("Angrist and Evans (1998)", "estimated here on AER's extract of their census sample"),
        ("Becker and Lewis (1973)", "computed on the Island; fertility shown from the Data Room"),
        ("Lundberg, Pollak and Wales (1997)", "stated; the collective household computed on the Island"),
        ("Krueger (1999); Angrist and Lavy (1999, 2019)", "stated and entered in the class_size dial; STAR and the "
         "California districts analysed here; Maimonides' rule computed on the Island"),
        ("Chetty, Friedman and Rockoff (2014); Hanushek and Rivkin (2010)", "stated and entered in the teacher_va "
         "dial; value added computed on the Island"),
        ("Heckman et al. (2010); Head Start Impact Study (2010, 2012); Durkin et al. (2022); Rea and Burton (2020)",
         "stated"),
        ("Grossman (1972); Gruber and Owings (1996); Cooper et al. (2019)", "stated; the demand for health computed; "
         "the Australian Health Survey analysed here"),
        ("Case and Deaton (2015); Alpert et al. (2022)", "stated"),
        ("Becker and Murphy (1988); Gruber and Kőszegi (2001)", "the model computed on the Island; cigarette demand "
         "estimated here on AER's state data"),
        ("Lazear (2000); Gneezy and Rustichini (2000); Mellström and Johannesson (2008); Frey and Oberholzer-Gee "
         "(1997)", "stated"),
        ("DiIulio (1995)", "the Called it? card"),
        ("Wei and Zhang (2011); Doepke et al. (2023)", "the frontier chapter, stated; fertility shown from the Data "
         "Room"),
    ],
    48: [
        ("Simon and Ehrlich (1980); Sabin (2013); Kiel, Matheson and Golembiewski (2010)", "the wager stated; the "
         "metals' real prices and every ten-year window computed from the Data Room"),
        ("Hotelling (1931)", "the rule derived and computed on the Island; real resource prices from the Data Room"),
        ("Gordon (1954); Smith (1969); Costello, Gaines and Lynham (2008)", "the fishery computed on the Island; "
         "catch shares stated; FAO's stocks from the Data Room"),
        ("Nordhaus (1992, 2017); Barrage and Nordhaus (2024)", "the DICE-style model built and fitted here; "
         "DICE-2023's results stated and entered in the discount dial"),
        ("Stern (2006); Rennert et al. (2022); EPA (2023)", "stated and entered in the discount dial"),
        ("Weitzman (2009); Dietz et al. (2021)", "the dismal theorem's logic computed on the Island; tipping points "
         "stated"),
        ("British Columbia (2008-2025); the EU ETS", "stated"),
        ("Nordhaus (2015); Acemoglu, Aghion, Bursztyn and Hemous (2012)", "toys computed on the Island; findings "
         "stated"),
        ("Dell, Jones and Olken (2012); Burke, Hsiang and Miguel (2015)", "stated and entered in the warming_output "
         "dial; the specification run here on ERA5 and World Bank data"),
        ("Barreca et al. (2016); Chen et al. (2013); Ebenstein et al. (2017)", "stated"),
        ("Borenstein, Bushnell and Wolak (2002)", "stated; the merit order computed on the Island"),
        ("Hughes, Knittel and Sperling (2008); Deryugina, MacKay and Reif (2020)", "stated and entered in the "
         "energy_elasticity dial"),
        ("Hubbert (1956); Deming (2023)", "the Called it? card; oil production from the Data Room"),
        ("Bilal and Känzig (2024); McGlade and Ekins (2015)", "the frontier chapter, stated"),
    ],
    47: [
        ("Olken (2006, 2007, 2009)", "the audit trial's results stated and entered in the corruption_share dial; the "
         "design computed on the Island"),
        ("Olson (1965); GAO (2023); USDA (2022)", "stated; the sugar prices shown from the Data Room; collective action "
         "computed on the Island"),
        ("Tullock (1967); Krueger (1974)", "the contest computed; Krueger's estimates stated"),
        ("Lee, Moretti and Butler (2004); Lee (2008); Caughey and Sekhon (2011)", "stated and entered in the "
         "incumbency dial; the Senate data analysed here"),
        ("Stigler (1971); Grossman and Helpman (1994); Goldberg and Maggi (1999); Fisman (2001)", "stated; "
         "probabilistic voting with lobbying computed on the Island"),
        ("Barro (1973); Ferejohn (1986); Ferraz and Finan (2011)", "the model computed on the Island; the audit "
         "result stated"),
        ("Fisman and Miguel (2007); Reinikka and Svensson (2004)", "stated; the WGI shown from the Data Room"),
        ("Acemoglu and Robinson (2000, 2006); Acemoglu et al. (2019)", "the franchise model computed; democracy and "
         "growth stated; V-Dem shown from the Data Room"),
        ("Besley and Persson (2009)", "stated; tax revenue shown from the Data Room"),
        ("Miguel, Satyanath and Sergenti (2004); Sachs and Warner (1995)", "stated; the instrument computed on the "
         "Island"),
        ("DellaVigna and Kaplan (2007); Autor et al. (2020)", "stated; the persuasion rate computed"),
        ("Nordhaus (1975); Rogoff (1985)", "the cycle computed on the Island"),
        ("HM Treasury (2016)", "the Called it? card"),
        ("Funke, Schularick and Trebesch (2023)", "the frontier chapter, stated"),
    ],
    46: [
        ("Cohen and Dupas (2010)", "the nets' prices and use, stated from the abstract; the demand computed on the "
         "Island"),
        ("World Bank (1990-2025); Chen and Ravallion (2008); Deaton (2010)", "the line's history stated; the World "
         "Bank's headcounts shown from the Data Room"),
        ("Kraay and McKenzie (2014); Balboni et al. (2022)", "stated; a trap and a threshold computed on the Island"),
        ("Lewis (1954); Gollin, Lagakos and Waugh (2014)", "the model computed; the raw gap recomputed from the World "
         "Bank's data"),
        ("Aleem (1990); Banerjee, Karlan and Zinman (2015); Meager (2019)", "stated; the lender's rate and a "
         "randomized microlender computed on the Island"),
        ("Schultz (2004); Haushofer and Shapiro (2016); Egger et al. (2022)", "stated, and entered in the "
         "cash_consumption dial; the multiplier computed on the Island"),
        ("Manacorda, Miguel and Vigorito (2011)", "their PANES households analysed here by regression discontinuity"),
        ("Banerjee et al. (2015)", "the graduation programme's results stated"),
        ("Duflo (2001); Banerjee et al. (2016); learning poverty (2022)", "stated; Duflo's design computed on the "
         "Island and entered in the return_schooling dial"),
        ("Miguel and Kremer (2004); the 2015 re-analyses", "stated; spillovers computed on the Island"),
        ("Thornton (2008)", "her Malawi data analysed here: collecting results by incentive and by distance"),
        ("Townsend (1994); Cole et al. (2013)", "stated; the test and index insurance computed on the Island"),
        ("Cai, de Janvry and Sadoulet (2015)", "their farmers' take-up analysed here; the network result stated"),
        ("Duflo, Kremer and Robinson (2011); Suri and Jack (2016)", "stated; present-biased farmers computed on the "
         "Island"),
        ("Dell (2010); Nunn (2008)", "stated; a boundary discontinuity computed on the Island"),
        ("Deaton (2010); Vivalt (2020); Meager (2019); World Bank (2022) on China", "stated; heterogeneous sites "
         "computed on the Island"),
        ("de Mel, McKenzie and Woodruff (2008, 2009); McKenzie and Woodruff (2008)", "entered in the "
         "return_capital_poor dial"),
        ("Sachs (2005); Mitchell et al. (2018); GiveWell", "the Called it? card and the practice chapter"),
        ("Muralidharan and Niehaus (2017); Jean et al. (2016); Blumenstock et al. (2015); Aiken et al. (2022)",
         "the frontier chapter, stated"),
    ],
    45: [
        ("DellaVigna and Malmendier (2006)", "the gym's contracts and attendance, stated from the abstract"),
        ("DellaVigna (2009)", "the survey's three classes of departures, stated"),
        ("Kahneman, Knetsch and Thaler (1990); Koszegi and Rabin (2006)", "the mug experiments stated in words (about "
         "two to one); the reference point as expectations, stated"),
        ("List (2003)", "his card-show data analysed here: who swapped, by experience"),
        ("Allen, Dechow, Pope and Wu (2017); Pope and Schweitzer (2011); Genesove and Mayer (2001)", "the field "
         "findings stated from the abstracts; each mechanism computed on the Island"),
        ("Phelps and Pollak (1968); Laibson (1997); O'Donoghue and Rabin (1999); DellaVigna and Malmendier (2004)",
         "models, computed on the Island"),
        ("Ashraf, Karlan and Yin (2006)", "take-up and the savings effect stated; the design computed on the Island"),
        ("Madrian and Shea (2001); Thaler and Benartzi (2004); Carroll et al. (2009)", "entered in the default_effect "
         "dial; Save More Tomorrow's figures stated"),
        ("Gabaix and Laibson (2006); Lacetera, Pope and Sydnor (2012)", "the equilibrium computed; the car-market "
         "steps stated and the estimator run on the Island"),
        ("Fehr and Schmidt (1999); Gneezy and List (2006); List (2007); Metcalf et al. (2020)", "the model computed; "
         "the field findings and the day-care replication stated"),
        ("Bernheim and Rangel (2009); Thaler and Sunstein (2003, 2008); Shleifer and Vishny (1997)", "ideas, stated"),
        ("DellaVigna and Linos (2022)", "the two samples' average effects and the share due to selective "
         "publication, stated; the filter and its correction computed on the Island"),
        ("Sims (2003); Matejka and McKay (2015); Gabaix (2014); Bordalo et al. (2020); Coibion and Gorodnichenko "
         "(2015)", "models, computed on the Island"),
        ("DellaVigna and Pope (2018)", "the Called it? card"),
        ("Tversky and Kahneman (1992); Brown et al. (2024); Walasek et al. (2024); Laibson, Repetto and Tobacman "
         "(2007); Augenblick, Niederle and Sprenger (2015); Cerrone et al. (2026); Jachimowicz et al. (2019)",
         "entered in the loss_aversion, present_bias and default_effect dials"),
        ("Gabaix (2020); Peterson et al. (2021); the FTC's click-to-cancel rule; SECURE 2.0", "the practice and "
         "frontier chapters, stated"),
    ],
    44: [
        ("Rust (1987); Hotz and Miller (1993)", "the model estimated on Rust's data; CCPs computed; myopia rejected"),
        ("Ericson and Pakes (1995); Pakes and McGuire (1994)", "a small Markov-perfect duopoly computed"),
        ("Bajari, Benkard and Levin (2007); Ryan (2012)", "stated"),
        ("Spengler (1950); Bork (1978); Leegin (2007)", "double marginalization computed; the cases stated"),
        ("Rochet and Tirole (2003); Armstrong (2006); Rysman (2004); Ohio v. American Express (2018)",
         "a two-sided platform computed; the findings and the case stated"),
        ("David (1985); Liebowitz and Margolis (1990); Arthur (1989)", "lock-in simulated on the Island; the debate "
         "stated"),
        ("Arrow (1962); Aghion et al. (2005)", "the replacement effect and the inverted U computed; the finding "
         "stated"),
        ("Cunningham, Ederer and Ma (2021)", "the logic in numbers; the finding stated"),
        ("Calvano et al. (2020); Assad et al. (2024)", "Q-learning run on Calvano's game; the findings stated"),
        ("Standard Oil (1911); Microsoft (2001); Google (2024-25); Khan (2017)", "stated"),
        ("Baron and Myerson (1982); Laffont and Tirole (1993)", "computed with two types"),
        ("Kwoka (2013, 2015); Vita and Osinski (2018)", "entered in the merger dial"),
        ("USA Today (2007); IDC (2024)", "the Called it? card"),
    ],
    43: [
        ("the FTC's cereal case (1972-1982)", "stated: the complaint, the shares of 1980 and the dismissal"),
        ("Nevo (2001)", "the method stated and computed on the Island's cereal aisle; the finding stated"),
        ("Bain (1951); Demsetz (1973)", "Bain's comparison stated; Demsetz's objection computed on the Island"),
        ("Bresnahan (1982); Lau (1982)", "the identification argument computed on the Island"),
        ("Lancaster (1966); McFadden (1974); Berry (1994)", "stated, and the logit and its inversion computed"),
        ("Berry, Levinsohn and Pakes (1995)", "the estimator derived and run on the Island; plain logit run on their "
         "data and entered in a dial"),
        ("Petrin (2002)", "the problem of new goods computed on the Island; the finding stated"),
        ("Olley and Pakes (1996); Levinsohn and Petrin (2003); Ackerberg, Caves and Frazer (2015)", "the "
         "simultaneity problem and ACF's estimator computed on the Island's plants"),
        ("Syverson (2004, 2011); Axtell (2001)", "the Facts on dispersion and firm sizes, stated"),
        ("De Loecker and Warzynski (2012); De Loecker, Eeckhout and Unger (2020)", "the ratio computed on the "
         "Island's plants; the rise entered in the markups dial"),
        ("Traina (2018); Basu (2019); Bond et al. (2021)", "the critiques stated"),
        ("Bresnahan and Reiss (1991)", "the threshold estimator computed on the Island's towns; the finding stated"),
        ("Merger Guidelines (2023, 2010); Farrell and Shapiro (2010); Werden (1996)", "the screens stated and "
         "computed on the Island"),
        ("DOJ (2008); Ashenfelter, Hosken and Weinberg (2015); Miller and Weinberg (2017)", "the Called it? card"),
        ("Cowling and Waterson (1976); Marschak and Andrews (1944)", "stated, with the identity derived"),
        ("Berry, Levinsohn and Pakes (2004); Berry and Haile (2021); Gandhi and Houde (2019); Conlon and Gortmaker "
         "(2020)", "the frontier, stated in words"),
    ],
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
         "enters the loss_aversion dial in Part 45"),
        ("Rabin (2000); Rabin and Thaler (2001)", "a theorem: its tables are transcribed, and the CRRA calibration "
         "is computed on screen"),
        ("Thaler (1981); Imai, Rutter and Camerer (2021)", "evidence on present bias, shown for its direction; "
         "present bias enters the present_bias dial in Part 45"),
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
    17: [
        ("Gale and Shapley (1962); Shapley and Scarf (1974); Vickrey (1961), Clarke (1971) and Groves (1973); Myerson "
         "and Satterthwaite (1983); Shapley and Shubik (1971)", "theory, stated; every algorithm and mechanism is run "
         "in Agora (agora.matching)"),
        ("Roth (1984, 1991); Roth's Nobel lecture (2012)", "the market for doctors and the clearinghouses, transcribed "
         "(data.tables.ROTH_2012) and the Called it? outcome"),
        ("Roth and Peranson (1999); Abdulkadiroğlu and Sönmez (2003); Abdulkadiroğlu, Pathak and Roth (2005); "
         "Chen and Kesten (2017)", "redesigns of the residents' match and of school choice, told as history"),
        ("Roth, Sönmez and Ünver (2004); Rees et al. (2009)", "kidney exchange and chains, told as history with the "
         "lecture's numbers"),
        ("Roth (2007)", "repugnance, stated"),
        ("Bansak et al. (2018)", "refugee placement by algorithm: its predicted employment gains, stated with the "
         "range the authors report"),
    ],
    18: [
        ("Condorcet (1785); Borda (1781); Arrow (1950, 1951); Black (1948); Downs (1957); May (1952); Gibbard (1973); "
         "Satterthwaite (1975); Sen (1970); Harsanyi (1955); Rawls (1971); Atkinson (1970); Kaldor (1939); Hicks "
         "(1939); Scitovsky (1941); Geanakoplos (2005)", "theory, stated; every rule, axiom check and welfare function "
         "is run in Agora (agora.choice)"),
        ("Duverger (1951); Riker (1982)", "Duverger's law, stated, and the Called it? outcome told as history"),
        ("Kniesner, Viscusi, Woock and Ziliak (2012)", "a range of wage-risk estimates ($4-10 million), stated, not "
         "dialled, since its dollar year is not recorded here"),
        ("the Stern Review (2007); Nordhaus", "discount rates, stated for direction; the dial is Part 48's"),
        ("V-Dem via Our World in Data", "data, shown with its source; no parameter is estimated"),
        ("Robbins (1932); Hammond (1976); d'Aspremont and Gevers (1977); Okun (1975); Frohlich and Oppenheimer "
         "(1992); Kaplow and Shavell (1994); Ramsey (1928); Schelling (1968); Thaler and Rosen (1976)",
         "theory and classic findings, stated; the leaky bucket, the veils and the jetty are computed in Agora"),
        ("Ravallion (2012); the UNDP's HDI", "a critique and an index, stated; the scatter is the HDR's data"),
        ("Bernheim and Rangel (2009); Lalley and Weyl (2018); Siththaranjan, Laidlaw and Hadfield-Menell (2024); "
         "Conitzer et al. (2024); Huang et al. (2024)", "frontier work, described, not dialled"),
        ("E.O. 12291, 12866, 14192; OMB Circular A-4 (2003, 2023); HM Treasury's Green Book; Whitman v. American "
         "Trucking (2001); Michigan v. EPA (2015)", "rules and rulings, stated as practice"),
    ],
    19: [
        ("Malthus (1798); Ehrlich (1968)", "the hook's theory and the Called it?, stated with their outcomes"),
        ("Ashraf and Galor (2011)", "a cross-country test of Malthus's prediction, stated in words, not dialled"),
        ("Allen (2009); Mokyr (2009, 2016); North and Weingast (1989); Clark (1996); Kelly, Mokyr and Ó Gráda (2014); "
         "Humphries (2013)", "explanations of why Britain, each stated with its critics; no parameter is estimated"),
        ("Needham; Pomeranz (2000); Broadberry, Guan and Li (2018)", "the debate over China, stated; the series shown "
         "are Maddison's"),
        ("Crafts and Harley (1992); Allen (2009) on Engels's pause", "slow early growth and the pause, shown in the Bank "
         "of England's series"),
        ("Becker and Lewis (1973); Galor and Weil (2000); Kremer (1993)", "theory, run in Agora (agora.malthus)"),
        ("Spolaore and Wacziarg (2009); Ashraf and Galor (2013); Kelly (2019)", "frontier work, described, not "
         "dialled"),
    ],
    23: [
        ("Mehra and Prescott (1985)", "the two numbers, transcribed (tables.MEHRA_PRESCOTT_1985); their economy "
         "solved in Agora (agora.assets)"),
        ("Williams (1938); Gordon and Shapiro (1956); Jorgenson (1963); Hall and Jorgenson (1967); Tobin (1969); "
         "Hayashi (1982)", "theory, run in Agora"),
        ("McDonald and Siegel (1986); Dixit and Pindyck (1994); Bloom (2009)", "the option to wait, run in Agora; "
         "uncertainty shocks stated"),
        ("Modigliani and Miller (1958); Myers and Majluf (1984)", "theory, stated"),
        ("Lucas (1978); Breeden (1979); Hansen and Singleton (1982); Hansen and Jagannathan (1991); Weil (1989)",
         "theory, computed on Shiller's data (data.shiller); risk-aversion rows added to the risk_aversion dial"),
        ("Campbell and Cochrane (1999); Bansal and Yaron (2004); Epstein and Zin (1989); Rietz (1988); Barro (2006)",
         "repairs, simulated or stated; Barro's 1.7% and 29% stated from the paper's calibration"),
        ("Shiller (1981); Campbell and Shiller (1988); Samuelson (1965); Fama (1970)", "excess volatility and "
         "predictability rerun on Shiller's data; efficient markets stated"),
        ("Tirole (1985); Smith, Suchanek and Williams (1988)", "rational bubbles stated; the laboratory's 14 of 22 "
         "stated from the abstract, the Island's market simulated"),
        ("Fisher (1929)", "Called it? (calls.fisher_plateau)"),
        ("Poterba (1984); Himmelberg, Mayer and Sinai (2005)", "the user cost of housing, stated; the price-to-rent "
         "ratio computed from FRED"),
        ("Chirinko, Fazzari and Meyer (1999); Hassett and Hubbard (2002); Zwick and Mahon (2017)", "entered in the "
         "investment_user_cost dial"),
        ("Novy-Marx and Rauh (2011)", "public pension liabilities at Treasury rates, stated"),
        ("Jordà, Knoll, Kuvshinov, Schularick and Taylor (2019); He and Krishnamurthy (2013); Adrian, Etula and "
         "Muir (2014)", "frontier, stated from the abstracts and the NBER working paper"),
        ("Diamond (1982)", "the next part's hook, stated"),
    ],
    24: [
        ("Diamond (1982); Cooper and John (1988)", "the coconut island, computed in Agora; coordination failure, "
         "stated"),
        ("Davis and Haltiwanger (1992); Davis, Haltiwanger and Schuh (1996)", "gross job flows, stated in words; the "
         "flows shown are JOLTS's"),
        ("Stigler (1961); McCall (1970); Butters (1977); Hall (1979); Nash (1950); Rubinstein (1982)", "theory, "
         "derived and computed in Agora"),
        ("Katz and Meyer (1990); Card, Chetty and Weber (2007)", "two studies of benefits and job search, shown as "
         "examples; the duration elasticity is the ui_duration dial, entered by Part 42"),
        ("Beveridge (1944); Elsby, Michaels and Ratner (2015); Hobijn and Sahin", "the curve's history and survey, "
         "stated; the curve shown is JOLTS's"),
        ("Blanchard, Domash and Summers (2022); Figura and Waller (2022)", "the soft-landing debate, stated with what "
         "followed in the data"),
        ("Petrongolo and Pissarides (2001); Shimer (2005)", "the matching dial's rows"),
        ("Mortensen and Pissarides (1994); Shimer (2005); Hall (2005); Hagedorn and Manovskii (2008); Pissarides "
         "(2009); Hall and Milgrom (2008); Ljungqvist and Sargent (2017)", "the volatility puzzle: the Called it? "
         "card, the calibrations solved in Agora, and the repairs stated; the bargaining dial's rows"),
        ("Hosios (1990)", "the efficiency condition, computed in Agora"),
        ("Shimer (2012); Elsby, Michaels and Solon (2009)", "the ins-and-outs decomposition, computed by this film "
         "from the CPS"),
        ("Topel and Ward (1992); Burdett and Mortensen (1998); Manning (2003)", "a single study of careers, shown as "
         "an example; the ladder computed in Agora; monopsony, stated (Part 38 measures it)"),
        ("Friedman (1968); the CBO's natural rate", "the concept, stated; the estimate shown as data"),
        ("Kroft, Lange and Notowidigdo (2013); Davis and von Wachter (2011)", "duration dependence and the cost of job "
         "loss: single studies, shown as examples"),
        ("Cahuc, Postel-Vinay and Robin (2006)", "the bargaining dial's row"),
        ("Horton (2017); Belot, Kircher and Muller (2019)", "two field experiments on platforms, shown as examples"),
        ("Hershbein and Kahn (2018); Marinescu and Rathelot (2018); Hansen, Lambert, Bloom, Davis, Sadun and Taska "
         "(2023)", "frontier work, stated from the abstracts and the paper's appendix"),
        ("Pissarides (2000); Cahuc, Carcillo and Zylberberg (2014); Ljungqvist and Sargent (2018); Rogerson, Shimer "
         "and Wright (2005)", "the reading list"),
        ("Furness (1910)", "the next part's hook, stated"),
    ],
    28: [
        ("Friedman (1968); Phelps (1967)", "the natural rate and acceleration, stated and computed in Agora; "
         "Friedman's forecast is a Called it? card"),
        ("Phillips (1958); Samuelson and Solow (1960)", "the curve and the menu, stated; Phillips's fitted equation "
         "drawn"),
        ("Muth (1961); Lucas (1972, 1973, 1976); Sargent and Wallace (1975)", "rational expectations, the islands and "
         "the critique, stated and simulated in Agora"),
        ("Kydland and Prescott (1977); Barro and Gordon (1983); Rogoff (1985)", "time inconsistency and the "
         "conservative banker, solved in Agora"),
        ("Alesina and Summers (1993)", "central bank independence and inflation, stated"),
        ("Ball (1994); Mankiw (1991)", "the sacrifice-ratio dial's rows"),
        ("Hazell, Herreno, Nakamura and Steinsson (2022)", "the flat Phillips curve across states, stated; the "
         "aggregate slopes are the film's regressions"),
        ("Bernanke and Blanchard (2023); Benigno and Eggertsson (2023)", "accounts of 2021-23, stated; openings per "
         "unemployed and inflation are FRED's data"),
        ("the FOMC's Summary of Economic Projections, June 2021", "the Called it? card on 'team transitory'"),
        ("Coibion, Gorodnichenko and Kumar (2018); Weber, D'Acunto, Gorodnichenko and Coibion (2022)", "how households "
         "and firms form expectations, stated; Michigan's survey is FRED's data"),
    ],
    27: [
        ("Sweeney and Sweeney (1977); Krugman (1998)", "the babysitting co-op, stated; Agora's co-op is simulated"),
        ("Say (1803); Keynes (1919, 1923, 1936); Kahn (1931); Hicks (1937); Samuelson (1955)", "theory, stated and "
         "solved in Agora (the cross, the multiplier's series, IS-LM, AS-AD)"),
        ("Mandeville (1714)", "the paradox of thrift's ancestor, stated"),
        ("Krugman (1998)", "the liquidity trap and the promise of inflation, stated; computed in Agora's IS-LM"),
        ("Phillips's machine (1949)", "its history stated; a water version of the multiplier simulated"),
        ("Fisher (1933); Bewley (1999); Card and Hyslop (1997); Dickens et al. (2007)", "debt deflation and sticky "
         "wages, stated; the spike at zero simulated on the Island"),
        ("Eichengreen and Sachs (1985); Eichengreen (1992); Romer (1992)", "what ended the Depression, stated; the "
         "gold stock and industrial production are the NBER's and the Fed's data"),
        ("Hayek (1931); Friedman and Schwartz (1963); Lucas and Sargent (1979)", "the critics, stated"),
        ("Keynes (1919); Mantoux (1946)", "the Called it? card"),
        ("Johnson, Parker and Souleles (2006) and the other rows", "the propensity-to-spend dial, shown again from "
         "Part 22"),
        ("Okun (1962); Ball, Leigh and Loungani (2017)", "the Okun dial's rows; the film's own regression on the CBO's "
         "gaps"),
        ("the NBER's business cycle dates", "expansions and recessions measured from FRED's recession indicator"),
        ("Guerrieri, Lorenzoni, Straub and Werning (2022)", "frontier theory, stated"),
    ],
    26: [
        ("Barr (2023); the Federal Reserve's review of Silicon Valley Bank (2023)", "the hook's thirty-six hours and "
         "the bank's numbers, transcribed (tables.SVB_2023)"),
        ("Diamond and Dybvig (1983)", "the model, derived and solved in Agora"),
        ("Bagehot (1873)", "the lender of last resort, stated; the fire sale computed in Agora"),
        ("Merton (1977)", "deposit insurance as a put, computed in Agora"),
        ("Curry and Shibut (2000)", "the cost of the savings-and-loan crisis, stated"),
        ("Admati and Hellwig (2013)", "the capital debate, stated; the equity ratio is the FFIEC's data"),
        ("Gorton and Metrick (2012)", "the run on repo, stated; the haircut arithmetic computed in Agora"),
        ("Morris and Shin (1998); Goldstein and Pauzner (2005)", "global games, solved and simulated in Agora"),
        ("Friedman and Schwartz (1963); Calomiris and Mason (2003)", "the Depression's banking crises, stated; the "
         "suspensions are the NBER's data"),
        ("Jiang, Matvos, Piskorski and Seru (2024)", "banks' unrealized losses and uninsured deposits, stated"),
        ("Diamond (1984); Bernanke (1983)", "delegated monitoring computed in Agora; the cost of failures stated"),
        ("the New York Fed (2022, 2023); S&P Global (2023)", "the deposit-beta dial's rows"),
        ("Reinhart and Rogoff (2009); Cerra and Saxena (2008); Romer and Romer (2017)", "the crisis-cost dial's rows"),
        ("the Federal Reserve's 2022 stress test scenarios", "the Called it? card (tables.STRESS_2022)"),
        ("Drechsler, Savov and Schnabl (2017, 2021)", "the deposit franchise, stated"),
        ("Cookson et al. (2023); the USDC de-peg of March 2023", "frontier work on digital runs and stablecoins, "
         "stated"),
    ],
    25: [
        ("Furness (1910); Friedman (1991)", "the hook's stone money and the Bank of France's gold, stated"),
        ("Jevons (1875); Kocherlakota (1998)", "barter's double coincidence and money as memory, stated; the odds are "
         "computed"),
        ("Kiyotaki and Wright (1989)", "the search economy, simulated and solved in Agora"),
        ("Duffy and Ochs (1999)", "a laboratory study, shown as an example"),
        ("von Glahn (1996); Eichengreen (2019)", "histories of money behind the timeline, stated"),
        ("Fisher (1896, 1911, 1930); Sidrauski (1967); Friedman (1969)", "theory, stated; the Fisher equation and "
         "the cost of inflation computed on the data and in Agora"),
        ("McCandless and Weber (1995); Friedman and Schwartz (1963)", "the quantity theory's evidence, stated; the "
         "scatter is the World Bank's data"),
        ("Hanke and Krus (2012); Cagan (1956)", "the hyperinflation peaks, transcribed (tables.HANKE_KRUS_2012); "
         "Cagan's ceiling as the Called it? card; his money demand computed in Agora"),
        ("Sargent (1982); Wicker (1986)", "the four stabilizations and their critic, stated"),
        ("the IMF's statements of July and October 2018", "Venezuela's projected inflation, stated"),
        ("Baumol (1952); Tobin (1956); Lucas and Nicolini (2015)", "the square-root rule, derived and computed; the "
         "stability of money demand, stated"),
        ("McLeay, Radia and Thomas (2014)", "money creation by lending, stated; the multiplier is the Fed's data"),
        ("Lucas (2000)", "the cost of inflation on US data, stated beside Agora's"),
        ("Ball (2001); Ireland (2009)", "the money-demand dial's rows"),
        ("DeFi Llama (as reported, December 2025); the GENIUS Act (2025)", "the stablecoin market and its law, stated"),
        ("Gorton and Zhang (2023); Selgin", "frontier work and its critic, stated from the abstracts"),
        ("Walsh (2017); Sargent (2013); Lagos, Rocheteau and Wright (2017)", "the reading list"),
        ("Silicon Valley Bank (March 2023)", "the next part's hook, stated"),
    ],
    22: [
        ("Johnson, Parker and Souleles (2006); Parker et al. (2013, 2022); Kueng (2018); Jappelli and Pistaferri "
         "(2014)", "the propensity to spend a windfall, entered in the mpc_windfall dial"),
        ("Keynes (1936); Kuznets (1946); Friedman (1957); Modigliani and Brumberg (1954)", "theory, quoted and run "
         "on the Island (agora.household)"),
        ("Hall (1978)", "Called it? (calls.hall_random_walk); the test rerun on FRED's series"),
        ("Flavin (1981); Campbell and Mankiw (1989); Working (1960); Deaton (1987, 1992); Campbell and Deaton "
         "(1989)", "excess sensitivity and smoothness, rerun on FRED's series and on the Island; Campbell and "
         "Mankiw's own estimate stated as about one half"),
        ("Kimball (1990); Zeldes (1989); Deaton (1991); Carroll (1997, 2006)", "theory, solved in Agora by the "
         "endogenous grid method"),
        ("Hsieh (2003)", "Alaska's dividend in survey data, stated from the abstract"),
        ("Kaplan, Violante and Weidner (2014); Kaplan and Violante (2014)", "the hand-to-mouth shares stated from "
         "the paper's summary; the mechanism run on the Island"),
        ("Fuster, Kaplan and Zafar (2021); Fagereng, Holm and Natvik (2021)", "survey and lottery evidence, stated "
         "from the abstracts (tables.MPC_STUDIES)"),
        ("Barro (1974); Samuelson (1958); Diamond (1965)", "theory, run in Agora (agora.olg)"),
        ("Abel, Mankiw, Summers and Zeckhauser (1989)", "the test of dynamic efficiency, stated from the abstract"),
        ("Dynan, Skinner and Zeldes (2004); Kotlikoff and Summers (1981); Modigliani (1988); Carroll (2000)",
         "the saving of the rich and inherited wealth, stated"),
        ("Modigliani and Cao (2004); Chamon and Prasad (2010); Wei and Zhang (2011)", "explanations of China's "
         "saving, stated; household consumption shares from the Penn World Table (data.pwt)"),
        ("Sahm, Shapiro and Slemrod (2012); Madrian and Shea (2001)", "stimulus delivery and pension defaults, "
         "stated from the abstract and transcribed (tables.MADRIAN_SHEA_2001)"),
        ("Ganong and Noel (2019); Kaplan, Moll and Violante (2018)", "frontier: spending through unemployment and "
         "HANK, stated; the path drawn from the working paper's magnitudes"),
        ("Mehra and Prescott (1985)", "the next part's hook, stated"),
    ],
    21: [
        ("Nordhaus (1996)", "the price of light, a transcribed table (tables.NORDHAUS_LIGHT)"),
        ("Arrow (1962); Romer (1986, 1990); Aghion and Howitt (1992); Jones (1995)", "theory, run in Agora "
         "(agora.ideas)"),
        ("Bloom, Jones, Van Reenen and Webb (2020)", "the decline of research productivity, transcribed "
         "(tables.BLOOM_2020)"),
        ("Comin and Hobijn (2010)", "adoption lags, stated from the abstract, not dialled"),
        ("Hsieh and Klenow (2009)", "the misallocation dial (Parts 9 and 21), recalled; the measure run on the "
         "Island's plants"),
        ("Acemoglu, Johnson and Robinson (2001, 2002); Albouy (2012)", "settler mortality refitted on their data "
         "(data.ajr), the reversal of fortune and the critique stated"),
        ("Dell (2010); Acemoglu and Robinson (2012)", "borders as experiments, stated from the abstract and the book"),
        ("Alsan (2015); Nunn and Wantchekon (2011); Diamond (1997)", "geography, disease and culture, stated"),
        ("Acemoglu (2002)", "directed technical change, run in Agora"),
        ("Williams (2013); Moser (2005)", "patents and innovation, stated from the abstracts"),
        ("Putterman and Weil (2010)", "ancestry-adjusted early development, stated from the abstract as the reply to "
         "the reversal of fortune"),
        ("Jones (2022)", "frontier: growth with a declining population, stated"),
    ],
    20: [
        ("Kaldor (1961)", "the six facts, stated in Part 3 and checked here on the Penn World Table"),
        ("Harrod (1939); Domar (1946); Easterly (1999)", "the knife edge, run on the island; Easterly's test of the "
         "financing gap described with its published counterfactual for Zambia, not dialled"),
        ("Solow (1956, 1957); Swan (1956); Phelps (1961)", "theory, run in Agora (agora.growth); the 1957 residual's "
         "seven eighths quoted as published"),
        ("Barro (1991)", "conditional convergence, described; the speed is dialled from MRW, Islam and this film"),
        ("Young (1995); Krugman (1994); Hsieh (2002)", "the East Asian debate: Young's four residuals quoted as "
                                                       "published beside the same accounting on the Penn World Table"),
        ("Hall and Jones (1999); Caselli (2005)", "development accounting quoted as published beside the same "
                                                  "accounting for 2019"),
        ("Lucas (1990)", "the 58-to-1 calculation, redone on 2019 data"),
        ("Ramsey (1928); Cass (1965); Koopmans (1965)", "theory, solved on screen by shooting"),
        ("Song, Storesletten and Zilibotti (2011)", "a model of China's growth, described; the series shown are the "
                                                    "Penn World Table's"),
        ("Fernald (2015); Kremer, Willis and You (2022); Acemoglu and Molina (2022)", "frontier work: the slowdown "
         "shown in the Penn World Table, the convergence finding dialled with its critics"),
    ],
    29: [
        ("Burns and Mitchell (1946); Hodrick and Prescott (1997); Hamilton (2018)", "the cycle's definition and "
         "filters, computed on FRED's real GDP"),
        ("Kydland and Prescott (1982); Prescott (1986); Hansen (1985); Rogerson (1988)", "the real business cycle "
         "model, solved and simulated in Agora (agora.rbc); Prescott's estimate is a Called it? card"),
        ("Brock and Mirman (1972); Bellman (1957)", "the stochastic growth model and dynamic programming, solved on "
         "screen"),
        ("Tauchen (1986); Rouwenhorst (1995); Kopecky and Suen (2010)", "Markov chains for shocks, built and compared"),
        ("Blanchard and Kahn (1980); Klein (2000)", "the saddle-path condition and the QZ solution, computed"),
        ("Summers (1986)", "the sceptic's case, stated"),
        ("Gali (1999); Christiano, Eichenbaum and Vigfusson (2003); Basu, Fernald and Kimball (2006); Fernald (2007)",
         "technology shocks and hours: the long-run VAR re-estimated on FRED's data in both specifications; the "
         "purified-technology and trend-break findings stated"),
        ("Chetty, Guren, Manoli and Weber (2011)", "the Frisch elasticity dial's rows"),
        ("Chari, Kehoe and McGrattan (2007); Shimer (2009)", "wedges, stated; the labour wedge computed from FRED's "
         "data"),
        ("Beaudry and Portier (2006); Bloom (2009)", "news and uncertainty shocks, stated"),
        ("Leamer (2007)", "housing leads the cycle: Play it's average paths are FRED's data"),
    ],
    30: [
        ("Bils and Klenow (2004); Nakamura and Steinsson (2008)", "the frequency of price changes, stated and dialled"),
        ("Cecchetti (1986); Blinder, Canetti, Lebow and Rudd (1998)", "magazine prices and the survey of firms, "
         "stated"),
        ("Bryan and Meyer (2010)", "the sticky- and flexible-price CPIs: the Atlanta Fed's series via FRED"),
        ("Mankiw (1985); Akerlof and Yellen (1985)", "menu costs, computed for the Island's ferry"),
        ("Calvo (1983); Gali (2015); Woodford (2003)", "the New Keynesian model, derived and solved in Agora "
         "(agora.nk)"),
        ("Taylor (1993)", "the rule, computed on FRED's data and fitted for 1987-2005"),
        ("Clarida, Gali and Gertler (1999, 2000)", "determinacy, discretion and commitment, computed; the pre- and "
         "post-1979 estimates stated"),
        ("Blanchard and Gali (2007)", "the divine coincidence, computed"),
        ("Golosov and Lucas (2007); Caplin and Spulber (1987)", "the selection effect, simulated with 20,000 price "
         "setters"),
        ("Eggertsson and Woodford (2003); Del Negro, Giannoni and Patterson (2012); McKay, Nakamura and Steinsson "
         "(2016); Gabaix (2020)", "the zero bound and the forward-guidance puzzle, computed; the repairs stated"),
        ("Christiano, Eichenbaum and Evans (2005); Smets and Wouters (2007)", "medium-scale frictions; the hump "
         "computed with habits, indexation and smoothing"),
        ("Bernanke (2002)", "the Called it? card on deflation"),
    ],
    42: [
        ("Finkelstein et al. (2012); Baicker et al. (2013); Taubman et al. (2014)", "the Oregon lottery, its design "
         "computed on the Island and its results stated"),
        ("RAND (1974-1982); Manning et al. (1987); Aron-Dine, Einav and Finkelstein (2013)", "the experiment stated; "
         "the elasticity entered in a dial; moral hazard computed on the Island"),
        ("Arrow (1963)", "stated"),
        ("Baily (1978); Chetty (2006)", "the formula derived and checked on the Island"),
        ("Chetty (2008)", "the liquidity split computed on the Island; the 60% stated"),
        ("Meyer (1990); Card, Chetty and Weber (2007); Schmieder, von Wachter and Bender (2012)",
         "durations computed on the Island; findings stated; Meyer entered in a dial"),
        ("Gruber (1997); Ganong and Noel (2019)", "the consumption drop stated and used in the formula"),
        ("Madrian and Shea (2001); Chetty et al. (2014)", "defaults computed on the Island; findings stated"),
        ("Maestas, Mullen and Strand (2013)", "the examiner design computed on the Island; the finding stated"),
        ("Eissa and Liebman (1996); IRS (2025)", "the schedule computed; the finding stated"),
        ("Robins (1985)", "the negative income tax experiments, stated"),
        ("Kela (2020); Vivalt et al. (2024); Banerjee et al. (2023)", "basic income trials, stated"),
        ("Hendren and Sprung-Keyser (2020); Finkelstein, Hendren and Luttmer (2019)", "the MVPF computed on the "
         "Island and entered in a dial"),
        ("SSA Trustees (2025); CRS (2022)", "pension arithmetic computed; the Called it? card"),
    ],
    41: [
        ("Laffer (1974); Wanniski (1978)", "the napkin, its story and its dispute; the curve computed"),
        ("Harberger (1962); Fuest, Peichl and Siegloch (2018)",
         "incidence computed on the Island; Germany entered in a dial"),
        ("Ramsey (1927); Diamond and Mirrlees (1971); Atkinson and Stiglitz (1976)", "computed on the Island; stated"),
        ("Mirrlees (1971); Diamond (1998); Saez (2001, 2002)", "the schedule and the top rate computed"),
        ("Diamond and Saez (2011); Piketty, Saez and Stantcheva (2014)", "the top rate entered in a dial; bargaining "
         "stated"),
        ("Feldstein (1995); Gruber and Saez (2002); Saez, Slemrod and Giertz (2012)",
         "the elasticity entered in a dial"),
        ("Saez (2010); Kleven and Waseem (2013)", "bunching computed on the Island; findings stated"),
        ("Chetty, Looney and Kroft (2009)", "salience, stated"),
        ("Chamley (1986); Judd (1985); Straub and Werning (2020)", "capital taxation, stated"),
        ("Zucman (2013); Torslov, Wier and Zucman (2023); OECD (2021)", "havens and the minimum tax, stated"),
        ("Allingham and Sandmo (1972); Kleven et al. (2011)", "evasion computed; the Danish experiment stated"),
        ("Kleven, Landais and Saez (2013)", "migration at the frontier, stated"),
        ("Mnuchin (2017); CBO (2018)", "the Called it? card"),
    ],
    40: [
        ("Pen (1971)", "the parade, drawn with Opportunity Insights' and Piketty and Saez's data"),
        ("Atkinson (1970)", "the index, computed on the Island"),
        ("Piketty and Saez (2003); the World Inequality Database", "top shares, data shown with sources"),
        ("Auten and Splinter (2024); Piketty, Saez and Zucman", "the measurement dispute, stated with both sides' "
         "numbers"),
        ("Pareto (1896); Champernowne (1953); Gabaix (2009)", "the tail, computed from the shares and derived on the "
         "Island; the Pareto fact"),
        ("Gabaix, Lasry, Lions and Moll (2016)", "the speed of transitions, computed on the Island"),
        ("Piketty (2014); Rognlie (2015); Krusell and Smith (2015)", "r against g, the mechanism computed; the replies "
         "stated"),
        ("Klass et al. (2006)", "the Forbes 400's exponent, entered in a dial"),
        ("Kuznets (1955)", "the Called it? card"),
        ("Solon (1992); Mazumder (2005); Chetty et al. (2014)", "the intergenerational elasticity, entered in a dial"),
        ("Corak (2013)", "the Gatsby curve, the range stated; its mechanism computed; the Gatsby fact"),
        ("Chetty et al. (2014, 2017)", "rank slopes, the transition matrix, absolute mobility and places, from the "
         "published data"),
        ("Chetty and Hendren (2018); Chetty, Hendren and Katz (2016)", "movers and Moving to Opportunity, stated"),
        ("Lakner and Milanovic (2016)", "the elephant curve, described; inequality between countries computed from "
         "the Penn World Table"),
        ("Chetty et al. (2016)", "life expectancy by income, stated"),
        ("Piketty, Saez and Zucman (2018); Jakobsen et al. (2020); Black et al. (2020)", "the frontier, stated"),
    ],
    39: [
        ("Bertrand and Mullainathan (2004)", "the resumes, recomputed from the data and entered in a dial"),
        ("Katz and Murphy (1992); Goldin and Katz (2008); Tinbergen", "the race between education and technology, "
         "the elasticity entered in a dial and the regression refitted"),
        ("Card and Lemieux (2001); Ciccone and Peri (2005); Autor, Goldin and Katz (2020)", "elasticities and "
         "shares, stated and entered in a dial"),
        ("Autor, Levy and Murnane (2003); Acemoglu and Autor (2011)", "tasks, stated; the task model computed"),
        ("Autor and Dorn (2013)", "polarization, from the replication data"),
        ("Acemoglu and Restrepo (2020)", "robots, stated; the design mimicked on the Island"),
        ("Abowd, Kramarz and Margolis (1999); Card, Heining and Kline (2013)", "AKM, computed on the Island; "
         "Germany, stated and entered in a dial"),
        ("Rosen (1981); Autor et al. (2020)", "superstars, computed; the labour share from FRED; firms, stated"),
        ("Freeman and Medoff (1984); Vella and Verbeek (1998)", "unions, recomputed from the panel"),
        ("Smith (1776); Rosen (1974); Mas and Pallais (2017)", "compensating differentials, computed and stated"),
        ("Becker (1957); Phelps (1972); Arrow (1973)", "discrimination in theory, computed"),
        ("Goldin and Rouse (2000); Quillian et al. (2017)", "field experiments, stated; the meta-analysis entered "
         "in a dial"),
        ("Oaxaca (1973); Blinder (1973)", "the decomposition, on the CPS"),
        ("Goldin (2014); Kleven, Landais and Sogaard (2019)", "the gender gap, stated; the child penalty mimicked "
         "on the Island"),
        ("Cullen and Pakzad-Hurson (2023); Reuters (2018)", "pay transparency and a hiring algorithm, stated"),
        ("Leontief (1983)", "the Called it? card"),
    ],
    38: [
        ("Card and Krueger (1994)", "the New Jersey-Pennsylvania border, recomputed from the public data; the own-wage "
         "elasticity entered in a dial"),
        ("Robbins (1930); Chetty, Guren, Manoli and Weber (2011)", "the backward bend, computed; the elasticities, "
         "entered in the labour supply dial"),
        ("Camerer, Babcock, Loewenstein and Thaler (1997); Farber (2015); Angrist, Caldwell and Hall (2021)",
         "cab drivers' hours, stated; the Uber Frisch elasticity entered in the labour supply dial"),
        ("Stigler (1946)", "the competitive prediction for a wage floor, computed"),
        ("Neumark and Wascher (2000); Card and Krueger (2000)", "payroll records and the reply, stated"),
        ("Cengiz, Dube, Lindner and Zipperer (2019)", "the bunching estimator, illustrated; the elasticity entered in "
         "the minimum wage dial"),
        ("Jardim et al. (2022)", "Seattle's hours, stated and entered in the minimum wage dial"),
        ("Robinson (1933); Manning (2003); Sokolova and Sorensen (2021)", "monopsony and the minimum wage, computed; "
         "the meta-analysis, stated"),
        ("Becker (1964); Mincer (1974)", "Mincer's equation, fitted to the 1976 CPS; the return entered in the "
         "schooling dial"),
        ("Card (1995)", "college distance as an instrument, recomputed and entered in the schooling dial"),
        ("Angrist and Krueger (1991); Bound, Jaeger and Baker (1995); Oreopoulos (2006)", "quarter of birth, weak "
         "instruments and Britain's leaving age, stated"),
        ("Roy (1951); Heckman (1979)", "selection and the two-step correction, computed on the Island"),
        ("Card (1990); Borjas (2017); Peri and Yasenov (2019)", "the Mariel boatlift, stated"),
        ("Kearl, Pope, Whiting and Wimmer (1979)", "the survey of economists; the Called it? card"),
    ],
    37: [
        ("Schelling (1971); Sakoda (1949)", "the checkerboard, played by Agora"),
        ("von Thuenen (1826)", "the rings, computed for the Island's crops"),
        ("Alonso (1964); Mills (1967); Muth (1969)", "the monocentric city, computed"),
        ("Marshall (1890); Duranton and Puga (2004)", "sharing, matching and learning, stated"),
        ("Combes, Duranton, Gobillon and Roux (2010); Ciccone and Hall (1996)", "agglomeration and sorting, "
         "entered in a dial; sorting reproduced on the Island"),
        ("Zipf (1949); Gabaix (1999)", "Zipf's law on America's metropolitan areas and Gibrat's growth, computed"),
        ("Krugman (1991); Fujita, Krugman and Venables (1999)", "core and periphery and the tomahawk, computed"),
        ("Rosen (1979); Roback (1982); Albouy", "spatial equilibrium and quality of life, computed on the Island"),
        ("Saiz (2010)", "housing supply elasticities, entered in a dial and set against Case-Shiller prices"),
        ("Hsieh and Moretti (2019); Greaney (2026)", "the aggregate cost of tight housing and its correction, "
         "stated"),
        ("Diamond, McQuade and Qian (2019)", "San Francisco's rent control, stated"),
        ("Chetty, Hendren and Katz (2016)", "Moving to Opportunity's children, stated"),
        ("Ahlfeldt, Redding, Sturm and Wolf (2015)", "the Berlin Wall, stated, entered in a dial and mimicked on a "
         "line city"),
        ("Donaldson (2018); Baum-Snow (2007)", "railways and highways, stated; the highway mechanism computed"),
        ("Kline and Moretti (2014)", "the Tennessee Valley Authority, stated"),
        ("Barrero, Bloom and Davis", "working from home, shown from FRED"),
    ],
    36: [
        ("McLean's Ideal X (1956)", "the first container voyage and its costs, stated"),
        ("Grubel and Lloyd (1975)", "two-way trade, computed for America's end-use categories"),
        ("Krugman (1979, 1980)", "variety, scale and the home-market effect, computed for the Island"),
        ("Tinbergen (1962); Santos Silva and Tenreyro (2006)", "gravity, estimated on CEPII's 2019 data by least "
         "squares and PPML"),
        ("McCallum (1995); Anderson and van Wincoop (2003)", "the border effect and multilateral resistance, stated"),
        ("Bernard and Jensen (1995)", "exporters are few, large and better, stated; the Island's firms computed"),
        ("Melitz (2003); Pavcnik (2002); Trefler (2004)", "selection, computed; the liberalization evidence, stated"),
        ("Eaton and Kortum (2002)", "shares by formula and by simulation, computed"),
        ("Arkolakis, Costinot and Rodriguez-Clare (2012); Dekle, Eaton and Kortum (2008)", "the gains formula and a "
         "hat-algebra counterfactual, computed on 2019 trade"),
        ("Autor, Dorn and Hanson (2013); Borusyak, Hull and Jaravel (2022); Goldsmith-Pinkham, Sorkin and Swift "
         "(2020)", "the China shock, stated and entered in a dial; shift-share reproduced on the Island"),
        ("Amiti, Redding and Weinstein (2019); Fajgelbaum et al. (2020)", "the 2018-19 tariffs, stated and entered in "
         "the pass-through dial"),
        ("Xing and Detert (2010)", "the iPhone's value added, stated"),
        ("Boehm, Levchenko and Pandalai-Nayar (2023)", "short- and long-run trade elasticities, entered in the dial"),
        ("Krugman (1995, 2008)", "trade and wages; the Called it? card"),
    ],
    35: [
        ("Samuelson (1969)", "Ulam's challenge and Samuelson's answer, as Samuelson told it"),
        ("Ricardo (1817)", "the four numbers, computed with the world price and the wage band"),
        ("Dornbusch, Fischer and Samuelson (1977)", "the continuum model, computed for the Island"),
        ("Bernhofen and Brown (2004, 2005)", "Japan's trade composition and the inner-product test, from their tables; "
         "the upper bound on the gains entered in the dial"),
        ("Irwin (2005)", "the cost of the Jeffersonian embargo, entered in the dial"),
        ("Heckscher (1919); Ohlin (1933); Lerner (1952)", "factor proportions and the Lerner diagram, computed for the "
         "Island"),
        ("Stolper and Samuelson (1941); Rybczynski (1955)", "the theorems, computed for the Island"),
        ("Scheve and Slaughter (2001)", "skills and trade-policy preferences, stated"),
        ("Leontief (1953); Leamer (1980)", "the paradox from Leontief's table, and Leamer's answer, stated"),
        ("Trefler (1995); Davis and Weinstein (2001)", "the missing trade, recomputed from Trefler's data"),
        ("Jones (1971); Samuelson (1971); Olson (1965)", "specific factors, computed; collective action, stated"),
        ("Irwin (1998, 2011)", "Smoot-Hawley's tariff rates and the role of deflation, stated"),
        ("Berry, Levinsohn and Pakes (1999)", "the voluntary export restraint on Japanese cars, stated"),
        ("Bickerdike (1906)", "the optimal tariff, computed for the Island"),
        ("Grossman and Helpman (1994); Goldberg and Maggi (1999)", "protection for sale, computed for the Island; the "
         "estimated weight on welfare, stated"),
        ("Bagwell and Staiger (1999)", "trade agreements and the terms-of-trade externality; the tariff war computed"),
        ("Kaldor (1939); Hicks (1939)", "the compensation test, computed for the Island"),
        ("Hyman (2018)", "trade adjustment assistance's effect on earnings, stated"),
        ("Arkolakis, Costinot and Rodriguez-Clare (2012)", "the gains-from-trade formula, applied to 2025"),
        ("Costinot and Donaldson (2012)", "Ricardo tested on agricultural productivity, stated"),
        ("Eaton and Kortum (2002)", "the many-country Ricardian model, stated"),
    ],
    34: [
        ("HM Treasury (2005); Bank of England", "Black Wednesday's sequence and cost, stated"),
        ("Balassa (1964); Samuelson (1964); The Economist's Big Mac index", "the Big Mac and the Balassa-Samuelson "
         "slope, computed from the index"),
        ("Rogoff (1996)", "the PPP puzzle and its half-life, recomputed from the JST database and entered in the "
         "dial"),
        ("Fama (1984)", "the forward premium puzzle, recomputed for seven currencies"),
        ("Brunnermeier, Nagel and Pedersen (2008)", "carry crashes, stated; the carry trade computed"),
        ("Meese and Rogoff (1983)", "the horse race, rerun; the Called it? card"),
        ("Mundell (1961, 1963); Fleming (1962)", "Mundell-Fleming and optimum currency areas, computed for the "
         "Island and stated"),
        ("Dornbusch (1976)", "overshooting, derived and computed"),
        ("Krugman (1979); Flood and Garber (1984); Obstfeld (1996); Kaminsky and Reinhart (1999)", "currency crises "
         "in three generations, the first and second computed"),
        ("IMF Independent Evaluation Office (2003); Stiglitz (2002)", "the IMF in Asia, stated"),
        ("Bernanke (2005); Gourinchas and Rey (2007); Caballero, Farhi and Gourinchas (2017)", "the saving glut, the "
         "exorbitant privilege and safe assets, stated with the current accounts and the US position"),
        ("Gopinath, Itskhoki and Rigobon (2010); Gopinath et al. (2020)", "dollar pricing, in the pass-through dial; "
         "this film's US estimate"),
        ("Rey (2013)", "the global financial cycle, stated with the VIX"),
        ("Gabaix and Maggiori (2015); Itskhoki and Mukhin (2021)", "the frontier, stated"),
    ],
    33: [
        ("Besley and Hennessy (2009)", "the British Academy's letter to the Queen, quoted"),
        ("Kindleberger (1978); Minsky (1986)", "the anatomy of manias and Minsky's three kinds of borrower, computed "
         "for the Island"),
        ("Fisher (1933)", "debt deflation, quoted and computed; US 1929-33 from the JST database"),
        ("Bernanke (1983)", "bank failures as lost information, stated; the suspensions from FRED"),
        ("Townsend (1979); Bernanke, Gertler and Gilchrist (1999)", "costly state verification and the financial "
         "accelerator, computed in Agora"),
        ("Kiyotaki and Moore (1997)", "the collateral cycle, solved exactly in Agora"),
        ("Geanakoplos (2010); Shleifer and Vishny (1992); Brunnermeier and Pedersen (2009); Gorton and Metrick (2012)",
         "the leverage cycle computed; fire sales, liquidity spirals and repo haircuts stated"),
        ("Mian, Rao and Sufi (2013); Mian and Sufi (2014)", "the MPC out of housing wealth, stated; the design rerun "
         "on the Island's counties"),
        ("Schularick and Taylor (2012); Jorda, Schularick and Taylor (2013, 2017)", "the crisis predictor and the "
         "shape of recessions, recomputed from the Macrohistory Database"),
        ("Greenwood, Hanson, Shleifer and Sorensen (2022)", "predictable crises, entered in the credit-warning dial"),
        ("Reinhart and Rogoff (2009); Romer and Romer (2017)", "the aftermath of crises, in the crisis-cost dial"),
        ("Basel Committee (2010); Cerutti, Claessens and Laeven (2017); Jimenez, Ongena, Peydro and Saurina (2017)",
         "the countercyclical buffer's guide computed; macroprudential evidence stated"),
        ("Calvo (1998); Eichengreen and Hausmann (1999)", "sudden stops and original sin, stated with the exchange "
         "rates from FRED"),
        ("Brunnermeier and Sannikov (2014)", "the frontier: nonlinear macro-finance, stated"),
        ("Rajan (2005)", "the Called it? card"),
    ],
    32: [
        ("Reinhart and Rogoff (2010); Herndon, Ash and Pollin (2014)", "the 90% result, recomputed step by step from "
         "the replication data"),
        ("Domar (1944); Blanchard (2019)", "debt dynamics and r - g, computed for the Island and from FRED's data"),
        ("Kahn (1931); Barro (1974, 1979); Diamond (1965)", "theories of the multiplier, of debt and of tax smoothing, "
         "stated; tax smoothing computed for the Island"),
        ("Woodford (2011); Christiano, Eichenbaum and Rebelo (2011)", "the multiplier at the zero bound, computed in "
         "Agora"),
        ("Blanchard and Perotti (2002); Ramey (2011); Ramey and Zubairy (2018)", "spending multipliers, recomputed "
         "from the replication data and entered in the multipliers dial"),
        ("Nakamura and Steinsson (2014); Chodorow-Reich (2019)", "regional multipliers, entered in the dial; the "
         "missing intercept shown on the Island"),
        ("Auerbach and Gorodnichenko (2012)", "larger multipliers in recessions, stated as a contrary finding"),
        ("Romer and Romer (2010)", "the narrative tax changes, used for this film's projections and entered in the "
         "tax-multiplier dial"),
        ("Johnson, Parker and Souleles (2006); Parker, Souleles, Johnson and McClelland (2013)", "the rebates, "
         "recalled from Part 22"),
        ("Alesina and Ardagna (2010); Guajardo, Leigh and Pescatori (2014)", "expansionary austerity and the reply, "
         "stated qualitatively"),
        ("Sims (1994); Cochrane (2023); Sargent and Wallace (1981)", "the fiscal theory and unpleasant arithmetic, "
         "computed for the Island"),
        ("Eaton and Gersovitz (1981); Arellano (2008)", "sovereign default, Arellano's calibration solved and "
         "simulated in Agora"),
        ("Kelton (2020); Mankiw (2020)", "modern monetary theory and a critique, stated"),
        ("Blanchard and Leigh (2013)", "the Called it? card on the IMF's 2010 forecasts, recomputed from the "
         "replication data"),
    ],
    31: [
        ("Draghi (2012)", "the speech, quoted; the yields are the OECD's via FRED"),
        ("Sims (1992); Eichenbaum (1992)", "the price puzzle, reproduced with this film's VAR on FRED's data"),
        ("Christiano, Eichenbaum and Evans (1999); Romer and Romer (1989, 2004); Kuttner (2001); Gertler and Karadi "
         "(2015); Nakamura and Steinsson (2018)", "the four methods, run on the Island against the planted truth "
         "(agora.cb); their US estimates enter the monetary_shock dial"),
        ("Coibion (2012); Ramey (2016)", "the reconciliation and the survey, entered in the monetary_shock dial"),
        ("Orphanides (2001, 2003, 2004)", "real-time output gaps, computed from the Philadelphia Fed's vintages; the "
         "papers' findings stated"),
        ("Friedman (1961)", "long and variable lags, stated"),
        ("Wallace (1981); Vayanos and Vila (2021)", "the theory of asset purchases, stated"),
        ("Gagnon, Raskin, Remache and Sack (2011)", "the QE1 event study, recomputed on DGS10 and entered in the "
         "qe_yield dial"),
        ("Swanson (2021); Eggertsson, Juelsrud, Summers and Wold (2019)", "forward guidance against purchases, and "
         "negative rates in Sweden, stated"),
        ("Laubach and Williams (2003); Holston, Laubach and Williams (2023)", "the natural rate: the New York Fed's "
         "estimates, entered in the neutral_rate dial; the method run on the Island"),
        ("Calvo (1988); De Grauwe (2011)", "self-fulfilling sovereign yields, computed in Agora (agora.cb.debt_game); "
         "Eurostat's 2011 debt ratios stated"),
        ("Bernanke (2013, 2014)", "the taper tantrum's testimony and the QE quip, stated; the yields are FRED's"),
        ("Romer and Romer (2000)", "the Called it? card on the Greenbook, checked on the Philadelphia Fed's data"),
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
