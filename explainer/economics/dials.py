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
         "change in price", (2, 6), status="settled within a range", checked="2026-11-18",
         meaning="below one in size for every staple measured: a tax on any of them raises revenue and cuts "
                 "consumption a little; how little decides whether it is a revenue tax or a health policy",
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
         )),
    Dial("cpi_bias", "measurement bias of the consumer price index", "percentage points a year by which the CPI "
         "overstates the rise in the cost of living", (3, 28), status="settled within a range", checked="2026-11-19",
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
         )),
    Dial("eis", "elasticity of intertemporal substitution", "", (7, 23)),
    Dial("risk_aversion", "relative risk aversion", "", (7, 23)),
    Dial("capital_share", "output elasticity of capital", "", (8, 20)),
    Dial("markups", "markups over marginal cost", "price over marginal cost", (10, 43)),
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
