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
DESIGNS = ("RCT", "IV", "RD", "DiD", "event study", "structural", "calibration", "survey", "narrative", "lab")


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
         "change in price", (2, 6)),
    Dial("eis", "elasticity of intertemporal substitution", "", (7, 23)),
    Dial("risk_aversion", "relative risk aversion", "", (7, 23)),
    Dial("capital_share", "output elasticity of capital", "", (8, 20)),
    Dial("markups", "markups over marginal cost", "price over marginal cost", (10, 43)),
    Dial("return_schooling", "return to a year of school", "percent higher earnings", (38,)),
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
