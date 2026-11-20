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
             Estimate("this film (US, 2007-09)", 2026, "event study", "US real GDP, 2007 Q4 to 2009 Q2, peak to trough",
                      3.8, where="videos/economics/econ26/compute.py, item crisis", checked="2026-11-20"),
             Estimate("this film (US, 2007-09)", 2026, "event study", "US real GDP in 2019 Q4 below its 1990-2007 "
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
             Estimate("this film (JST, credit and houses)", 2026, "regression", "18 countries, 1870-2017: the "
                      "three-year rise in loans to GDP and in real house prices both in their top fifth "
                      "(5% when neither)", 33.3,
                      where="videos/economics/econ33/compute.py, item panel", checked="2026-11-20"),
             Estimate("this film (JST, credit alone)", 2026, "regression", "the same, the top fifth of the rise in "
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
             Estimate("this film (US, 1965-2007)", 2026, "structural", "a recursive VAR with commodity prices: "
                      "industrial production's trough, 29 months after the shock", -1.33, lo=-1.67, hi=-0.72,
                      where="videos/economics/econ31/compute.py, item usvar", checked="2026-11-20"),
         )),
    Dial("multipliers", "government-spending multiplier", "dollars of output per dollar of government purchases, "
         "cumulative over about two years", (32,), status="depends on the setting", checked="2026-11-20",
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
    Dial("trade_elasticity", "trade elasticity", "", (36,)),
    Dial("passthrough", "pass-through of tariffs and exchange rates to prices", "share", (34, 36, 66)),
    Dial("agglomeration", "agglomeration elasticity", "percent productivity per doubling of density", (37,)),
    Dial("housing_supply", "elasticity of housing supply", "", (37,)),
    Dial("return_capital_poor", "return to capital for small firms in poor countries", "percent a month", (46,)),
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
