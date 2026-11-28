"""Lab 32: the Works' marketplace by take rate, ad load and delivery promise; the cost of an order against volume; take
rates; a seller's dollar; Amazon's revenue, advertising and segment profit; e-commerce's share; a direct brand's
customers; and this series' call."""

from explainer.industry.works import marketplace
from videos.coursekit import labs
from videos.industry.industry32.compute import results

TITLE = "E-commerce: a shop, a toll road and an ad business"
GOAL = ("Run a two-sided marketplace and find the take rate, the ad load and the delivery promise that pay best; split a "
        "seller's dollar; compute take rates and the cost of an order as a fixed network spread over volume; read where "
        "Amazon's revenue and profit come from; compute a direct brand's payback from the cost of a customer; and state a "
        "dated call.")
TASKS = [
    "With marketplace.Marketplace(pass_through=x).solve(), let sellers pass none of an extra fee into their prices (x = 0) "
    "and all of it (x = 1). How does the most profitable take rate move, and why?",
    "With marketplace.Marketplace(buyers_max=b, sellers_max=b / 100).with_(days=d).solve(), find the size at which a one-day "
    "promise first beats a two-day one. What does that say about who can offer next-day delivery?",
    "With marketplace.Brand(cac=c, retention=r), find the highest cost of acquiring a customer that still pays back within "
    "three years at retention of 30%, 40% and 50%. Which matters more to a direct brand: cheaper ads or loyal customers?",
]


def run(seed=0):
    lab = labs.Lab()
    R = results()

    H = R["hook"]
    lab.row("Amazon: revenue 2025; AWS share of revenue / of operating income", f"${H['rev']:.0f}bn; {100 * 128.725 / H['rev']:.0f}% / {100 * H['aws_share']:.0f}%")
    lab.row("Amazon: 1997 revenue; 2000 share price fall", f"${H['l97']:.1f}m; more than {H['down00']:.0f}%")
    U = R["run"]
    b = U["base"]
    lab.row("the Works' marketplace: buyers; sellers; GMV; revenue; profit",
            f"{b['buyers'] / 1e6:.0f}m; {b['sellers'] / 1e3:.0f}k; ${b['gmv'] / 1e9:.1f}bn; ${b['revenue'] / 1e9:.1f}bn; ${b['profit'] / 1e9:.1f}bn")
    T = U["by_take"]
    rev_best = max(T, key=lambda t: T[t]["revenue"])
    pro_best = max(T, key=lambda t: T[t]["profit"])
    lab.row("take rate with the most revenue / the most profit", f"{100 * rev_best:.1f}% / {100 * pro_best:.1f}%")
    A = U["by_ad"]
    lab.row("ad load with the most profit", f"{100 * max(A, key=lambda a: A[a]['profit']):.1f}% of sales")
    lab.row("cost an order, 1/2/3-day promise; four times bigger",
            " / ".join(f"${U['by_days'][d]['cost_per_order']:.2f}" for d in (1.0, 2.0, 3.0)) + "; "
            + " / ".join(f"${U['big_days'][d]['cost_per_order']:.2f}" for d in (1.0, 2.0, 3.0)))
    assert 0.2 <= pro_best <= 0.35 and U["big_days"][1.0]["cost_per_order"] < U["by_days"][1.0]["cost_per_order"]
    D = R["dollar"]
    lab.row("a $40 order: goods / referral / fulfilment / ads / the seller keeps",
            f"${D['goods']:.2f} / ${D['referral']:.2f} / ${D['fulfil']:.2f} / ${D['ads']:.2f} / ${D['keep']:.2f}")
    lab.row("take rates, 2025", "; ".join(f"{k} {v:.1f}%" for k, v in R["models"]["take"].items()))
    Ad = R["ads"]
    lab.row("Amazon: advertising against the shops' operating income",
            "; ".join(f"{y}: ${Ad['amzn'][y]:.0f}bn vs ${Ad['store_op'][y]:.1f}bn" for y in (2019, 2022, 2025)))
    Tr = R["traffic"]
    lab.row("e-commerce share of US retail: 1999 Q4 / spring 2020 / latest",
            f"{Tr['share'][min(Tr['share'])]:.1f}% / 16.0% / {Tr['last_share']:.1f}%")
    Dr = R["direct"]
    lab.row("a direct brand: lifetime value at $30 / $60 / $90 a customer", " / ".join(f"${Dr['life'][c]:.0f}" for c in (30.0, 60.0, 90.0)))
    Cl = R["called"]
    lab.row(f"this series' call: Census e-commerce share for 2027 Q4 at {Cl['line']:.1f}% or more", f"probability {100 * Cl['prob']:.0f}%")

    fig, (ax1, ax2) = labs.figure(2)
    ax1.plot([100 * t for t in T], [s["revenue"] / 1e9 for s in T.values()], color=labs.GOLD, lw=1.8, label="revenue")
    ax1.plot([100 * t for t in T], [s["profit"] / 1e9 for s in T.values()], color=labs.BLUE, lw=1.8, label="profit")
    ax1.axhline(0, color=labs.MUTED, lw=0.8)
    ax1.set_xlabel("take rate, %")
    ax1.set_ylabel("$bn a year")
    ax1.set_title("The Works' marketplace by take rate")
    ax1.legend(frameon=False)
    for c in (30.0, 60.0, 90.0):
        ax2.plot(range(6), Dr["cac"][c], lw=1.8, label=f"${c:.0f} a customer")
    ax2.axhline(0, color=labs.MUTED, lw=0.8)
    ax2.set_xlabel("years after the first order")
    ax2.set_title("A direct brand: profit per customer")
    ax2.legend(frameon=False)
    lab.fig = fig
    lab.note = ("A marketplace's fee is bounded by what both sides can do instead; its ads are nearly pure profit until they "
                "crowd out what buyers came for; fast delivery is a fixed cost that pays only at scale; and a brand that buys "
                "its customers lives on how often they come back.")
    _ = marketplace
    return lab
