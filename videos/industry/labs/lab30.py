"""Lab 30: the Works' spectrum auction under each cap, a subscriber's worth by churn, a tower by tenants, the carriers'
revenue and margins against the services that run over them, capital spending, spectrum deals, American Tower, home
broadband, and this series' call on Comcast's broadband customers."""

from explainer.industry.works import telco
from videos.coursekit import labs
from videos.industry.industry30.compute import results

TITLE = "Telecoms: essential, costly, alike"
GOAL = ("Run a spectrum auction and see why asking for less can pay; value a subscriber from what she pays, how often she "
        "leaves and what she cost; see a tower's return rise with every tenant; compare the carriers' revenue, margins and "
        "capital spending with the companies whose services run over them; read the spectrum deals and the tower company's "
        "accounts; follow home broadband; place the companies; and state a dated call.")
TASKS = [
    "With telco.Auction(supply=s).run(cap=k), offer nine blocks instead of eight, then seven. For each, which cap leaves you "
    "best off, and what does the auction raise? Why does a larger supply make holding back pay less?",
    "With telco.Subscriber(churn=c, cac=x).lifetime(), find the acquisition cost at which an account leaving at 2% a month is "
    "worth nothing. What does that say about price wars that raise churn?",
    "With telco.Tower(rent=r).yield_(n), find the rent at which a one-tenant tower returns 10% a year, and what a three-tenant "
    "tower returns at that rent.",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    H = R["hook"]
    lab.row("revenue $bn 2015 / 2025: Verizon + AT&T + T-Mobile; Alphabet + Meta + Netflix",
            f"{H['carriers3'][2015]:.0f} / {H['carriers3'][2025]:.0f}; {H['over'][2015]:.0f} / {H['over'][2025]:.0f}")
    lab.row("operating margin 2025", ", ".join(f"{k}: {v:.1f}%" for k, v in H["margins"].items()))
    lab.row("telephone services after inflation (1998 = 1), 2025", f"{H['real'][2025]:.2f}")
    for k, r in R["run"]["runs"].items():
        lab.row(f"the Works' auction, you ask for at most {k}: price; won (you, A, B, C); you keep; raised",
                f"${r['price']:.2f}bn; {r['won']}; ${r['surplus'][0]:.2f}bn; ${r['revenue']:.1f}bn")
    assert R["run"]["runs"][2]["surplus"][0] > R["run"]["runs"][4]["surplus"][0]
    S = R["sub"]
    lab.row("a Verizon account: $ a month; months it stays; lifetime worth", f"{S['arpa']:.2f}; {S['months']:.0f}; ${S['life']:,.0f}")
    lab.row("lifetime worth by monthly churn", ", ".join(f"{100 * c:.2f}%: ${v:,.0f}" for c, v in S["by_churn"].items()))
    T = R["towers"]
    lab.row("the Works' tower: yield by tenants", ", ".join(f"{n}: {100 * v['yld']:.1f}%" for n, v in T["by_tenants"].items()))
    lab.row("American Tower US & Canada: revenue a site; costs a site; tenants implied at $45k", f"${T['per_site']:,.0f}; ${T['opex_site']:,.0f}; {T['implied']:.2f}")
    C = R["net"]["capex"]
    lab.row("capital spending per dollar of revenue, 2025", ", ".join(f"{k}: {100 * v[0] / v[1]:.1f}%" for k, v in C.items()))
    Sp = R["spectrum"]
    lab.row("spectrum $bn: Verizon C-Band; AT&T 2021 acquisitions; EchoStar to AT&T; to SpaceX",
            f"{Sp['vz']}; {Sp['att']:.1f}; {Sp['att_echo']}; about {Sp['spacex']}")
    Hm = R["home"]
    lab.row("home broadband changes in 2025, thousands", ", ".join(f"{n}: {v:+,}" for n, v in Hm["changes"]))
    C2 = R["called"]
    lab.row("this series' call: Comcast's domestic broadband customers lower at end-2027 than end-2026", f"probability {100 * C2['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    r4 = R["run"]["runs"][4]["path"]
    ax1.plot([p for p, _ in r4], [d for _, d in r4], color=labs.BLUE, lw=1.8, label="blocks wanted (honest)")
    r2 = R["run"]["runs"][2]["path"]
    ax1.plot([p for p, _ in r2], [d for _, d in r2], color=labs.GOLD, lw=1.4, ls="--", label="you ask for two")
    ax1.axhline(R["run"]["supply"], color=labs.MUTED, lw=1.0, ls=":", label="blocks on offer")
    ax1.set_xlabel("price per block, $bn")
    ax1.set_title("The Works' clock auction")
    ax1.legend(fontsize=7)
    ys = list(range(2015, 2026))
    ax2.plot(ys, [H["carriers3"][y] for y in ys], color=labs.BLUE, lw=1.8, label="Verizon, AT&T, T-Mobile")
    ax2.plot(ys, [H["over"][y] for y in ys], color=labs.GOLD, lw=1.8, label="Alphabet, Meta, Netflix")
    ax2.set_ylabel("$bn")
    ax2.set_title("The pipe and what runs through it")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("The carriers pay up front for airwaves sold like land, sell nearly the same thing to customers who leave for "
                "a better price, rebuild the network every generation, rent the towers from landlords who keep more, and "
                "carry services whose value belongs to whoever made them.")
    _ = telco
    return lab
