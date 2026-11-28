"""Lab 36: the Works' software company by churn, budget split and price; its unit economics and lifetime value; the
cohorts; the licence-to-subscription J-curve against Adobe's; cost structures, stock pay and growth against cash across
the industry; Microsoft's and Oracle's capital spending; and this series' call."""

from explainer.industry.works import saas
from videos.coursekit import labs
from videos.industry.industry36.compute import results

TITLE = "Software: worth what customers will keep paying for the next copy"
GOAL = ("Run a subscription company for five years: count where its ARR comes from, watch margins rise with scale, split an "
        "extra budget between salespeople and engineers, raise the price; price a dollar of new business against its "
        "lifetime gross profit; draw the cohorts; switch a licence business to subscriptions; read real companies' costs, "
        "retention, backlogs and capital spending; and state a dated call.")
TASKS = [
    "With saas.Saas(churn=c).run(quarters=20), find the churn at which the company's ARR after five years equals what it "
    "would reach at 8% churn with an extra $30m a year spent half on salespeople. What is lower churn worth in dollars?",
    "With saas.j_curve(migrate=m), make existing licence owners convert faster (half a year) and slower (a tenth). How "
    "deep is the dip and how long until the switched company passes the one that kept selling licences?",
    "With saas.Saas(gross_margin=g).run(), lower the gross margin from 78% to 65%, as heavy AI use might. What happens "
    "to the operating margin in year five, and how much more would the company need to charge to restore it?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    H = R["hook"]
    lab.row("Microsoft, fiscal 2026: revenue; operating income; employees", f"${H['rev']:.0f}bn; ${H['op']:.0f}bn; {H['staff']:,}")
    lab.row("cost per dollar: licences and devices; services and cloud", f"{100 * H['pcost'] / H['product']:.0f}c; {100 * H['scost'] / H['service']:.0f}c")
    U = R["run"]
    b = U["base"]
    lab.row("the Works' company, no new hires: ARR by year, $m", ", ".join(f"{a / 1e6:.0f}" for a in b["arr"][3::4]))
    lab.row("growth and operating margin by year, %", "; ".join(f"{100 * g:.0f}/{100 * m:.0f}" for g, m in zip(b["growth"][3::4], b["op_margin"][3::4])))
    lab.row("cost to win $1 of new ARR; payback; lifetime gross profit over 10 years", f"${U['cac']:.2f}; {U['unit']['payback_months']:.0f} months; ${U['ltv'][10]:.2f}")
    for s_, r in U["alloc"].items():
        lab.row(f"extra $30m a year, {100 * s_:.0f}% on salespeople: ARR and cash after five years", f"${r['arr'][-1] / 1e6:.0f}m; ${r['cum_cash'] / 1e6:.0f}m")
    assert U["alloc"][0.5]["arr"][-1] > U["alloc"][0.0]["arr"][-1] and U["alloc"][0.0]["cum_cash"] > U["alloc"][1.0]["cum_cash"]
    lab.row("ARR after five years by churn 4/8/12/16%, $m", " / ".join(f"{v / 1e6:.0f}" for v in U["churn_sens"].values()))
    L = R["licence"]
    lab.row("Adobe: revenue 2012 / 2013 / 2025; licence share 2011 / 2013", f"${L['r12']:.2f}bn / ${L['r13']:.2f}bn / ${L['rev25']:.1f}bn; 81% / {L['prod13']}%")
    Cc = R["cohorts"]
    lab.row("net revenue retention: Snowflake; Datadog; the Works", f"{Cc['snow']}%; about {Cc['ddog']}%; {100 * Cc['nrr_works']:.0f}%")
    lab.row("Salesforce: operating income; cash from operations; RPO", f"${Cc['crm_op']:.1f}bn; ${Cc['crm_ocf']:.1f}bn; ${Cc['crm_rpo']:.1f}bn")
    A = R["ai"]
    lab.row("Microsoft's additions to property and equipment, 2016 / 2024 / 2026", f"${A['ms_capex'][2016]:.0f}bn / ${A['ms_capex'][2024]:.0f}bn / ${A['ms_capex'][2026]:.0f}bn")
    lab.row("Oracle: capital spending; free cash flow, fiscal 2026", f"${A['or_capex'][2026]:.0f}bn; -${-A['or_fcf'][2026]:.0f}bn")
    C = R["called"]
    lab.row("Salesforce: target for fiscal 2026; result", f"${C['target_crm']}bn+; ${C['crm26']:.1f}bn")
    lab.row(f"this series' call: Microsoft Cloud at least ${C['target']:.0f}bn in fiscal 2027",
            f"needs {100 * C['need']:.1f}% after 27% in fiscal 2026 and 30% in Q1; probability {100 * C['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    import numpy as np
    m = np.array(Cc["matrix"])
    bottom = np.zeros(m.shape[1])
    for c in range(m.shape[0]):
        ax1.bar(range(1, m.shape[1] + 1), m[c], bottom=bottom, color=labs.CYCLE[c % len(labs.CYCLE)], width=0.8)
        bottom += m[c]
    ax1.set_xlabel("year")
    ax1.set_title("The layer cake: ARR by cohort")
    ad = L["adobe"]
    ax2.plot(list(ad), [v[0] for v in ad.values()], color=labs.BLUE, lw=1.8, label="revenue")
    ax2.plot(list(ad), [v[1] for v in ad.values()], color=labs.GREEN, lw=1.8, label="operating income")
    ax2.set_title("Adobe's J-curve, $bn")
    ax2.legend(fontsize=8)
    lab.fig = fig
    lab.note = ("Software's costs are fixed and up front; its largest cost is finding customers; subscriptions turn one sale into "
                "a stream that lock-in keeps flowing; and AI is making each use cost something again.")
    _ = saas
    return lab
