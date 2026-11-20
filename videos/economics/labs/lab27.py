"""Lab 27: the Keynesian revolution: the babysitting co-op, the cross and Kahn's multiplier, the paradox of thrift,
IS-LM with a zero lower bound, aggregate demand and supply, sticky wages, Okun's law and the length of expansions."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import keynes as ks
from explainer.economics.island import truths

TITLE = "The Keynesian revolution: when spending sets output"
GOAL = ("Run a babysitting co-op short of money and cure it; add up Kahn's multiplier; watch thrift lower saving; "
        "solve IS-LM with a zero bound and see money stop working; shock aggregate demand and supply; and measure "
        "Okun's law and the length of America's expansions.")
TASKS = [
    "The co-op: lower the reserve each couple wants from 10 to 6. Where is the best number of coupons now, and why?",
    "IS-LM: raise h, the interest sensitivity of money demand. What happens to the fiscal multiplier outside the "
    "trap, and why?",
    "Okun's law: estimate it before 1985 and after. Has the coefficient changed?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(27)

    C = T["coop"]
    r = ks.coop(n=C["n"], coupons=C["start"], target=C["target"], weeks=C["weeks"], p=C["p"], seed=C["seed"] + seed,
                print_at=C["print_at"], print_to=C["print_to"])
    before, after = np.mean(r["evenings"][20:C["print_at"]]), np.mean(r["evenings"][C["print_at"] + 20:])
    assert after > before
    lab.row("co-op: evenings per couple a week, before and after printing", f"{before:.3f}, {after:.3f}")
    curve = ks.coop_curve(np.arange(1, 25), n=C["n"], target=C["target"], p=C["p"], seed=C["seed"] + seed)
    k = int(np.argmax(curve["evenings"]))
    lab.row("co-op: the best number of coupons per couple", f"{curve['coupons'][k]:.0f}")

    X = T["cross"]
    c = ks.cross(X["a"], X["b"], X["I"], X["G"], X["T"])
    rounds = ks.multiplier_rounds(X["dG"], X["b"], 30)
    n90 = int(np.argmax(np.array(rounds["cumulative"]) >= 0.9 * rounds["limit"])) + 1
    lab.row("the cross: income; multiplier; rounds to 90% of the effect",
            f"{c['Y']:.0f}; {c['multiplier']:.2f}; {n90}")

    Th = T["thrift"]
    th = ks.paradox_of_thrift(Th["a"], Th["b"], Th["I"], 0.0, Th["da"], h=Th["h"])
    assert th["dS"] < 0
    lab.row("thrift with induced investment: change in income and in saving", f"{th['dY']:.1f}, {th['dS']:.1f}")

    L = T["islm"]
    kw = {k_: L[k_] for k_ in ("a", "b", "T", "I0", "d", "k", "h")}
    base, fis = ks.islm(L["G"], L["M"], **kw), ks.islm(L["G"] + L["dG"], L["M"], **kw)
    slump = {**kw, "I0": L["I0"] - L["slump"]}
    s0, s1 = ks.islm(L["G"], L["M"] + 2 * L["dM"], **slump), ks.islm(L["G"], L["M"] + 4 * L["dM"], **slump)
    assert s0["trap"] and abs(s1["Y"] - s0["Y"]) < 1e-9
    lab.row("IS-LM: Y and i; fiscal multiplier; extra money in the trap adds",
            f"{base['Y']:.0f}, {base['i']:.2f}%; {(fis['Y'] - base['Y']) / L['dG']:.2f}; {s1['Y'] - s0['Y']:.1f}")

    A = T["asad"]
    e0 = ks.asad(L["G"], L["M"], A["Ystar"], A["Pe"], A["kappa"], **kw)
    dm = ks.asad(L["G"], L["M"] + A["dM"], A["Ystar"], A["Pe"], A["kappa"], **kw)
    sp = ks.asad(L["G"], L["M"], A["Ystar"], A["Pe"], A["kappa"], cost=A["cost"], **kw)
    assert dm["P"] < e0["P"] < sp["P"]
    lab.row("AS-AD: (Y, P) at rest, after a money shock, after a cost shock",
            f"({e0['Y']:.0f}, {e0['P']:.3f}), ({dm['Y']:.0f}, {dm['P']:.3f}), ({sp['Y']:.0f}, {sp['P']:.3f})")

    W = T["wages"]
    w = ks.wage_changes(n=W["n"], mean=W["mean"], sd=W["sd"], rigid=W["rigid"], seed=W["seed"] + seed)
    lab.row("sticky wages: share due a cut; share at exactly zero",
            f"{w['share_cut_wanted']:.3f}; {w['share_zero']:.3f}")

    gdp = dict(zip(data.fred("GDPC1")["date"], data.fred("GDPC1")["value"]))
    pot = dict(zip(data.fred("GDPPOT")["date"], data.fred("GDPPOT")["value"]))
    nr = dict(zip(data.fred("NROU")["date"], data.fred("NROU")["value"]))
    un = data.fred("UNRATE")
    uq: dict = {}
    for x, v in zip(un["date"], un["value"]):
        uq.setdefault(f"{x[:4]}-{(int(x[5:7]) - 1) // 3 * 3 + 1:02d}-01", []).append(v)
    ds = sorted(d for d in gdp if d in pot and d in nr and d in uq and len(uq[d]) == 3 and all(np.isfinite(uq[d]))
                and d <= "2025-12-31")
    gap = np.array([100 * (gdp[d] / pot[d] - 1) for d in ds])
    ug = np.array([np.mean(uq[d]) - nr[d] for d in ds])
    beta = np.polyfit(gap, ug, 1)[0]
    assert -1 < beta < -0.3
    lab.row("Okun's law: unemployment gap per point of output gap, 1949-2025", f"{beta:.3f}")

    rec = data.fred("USREC")
    sp_ = ks.spells(rec["value"], rec["date"])
    lab.row("NBER cycles since 1854: mean expansion and recession, months",
            f"{np.mean(sp_['expansions']):.1f}, {np.mean(sp_['recessions']):.1f}")

    lab.note = ("A co-op short of coupons is short of evenings out, though nobody's skills or tastes have changed; "
                "more coupons cure it. In the cross every dollar of spending becomes 1/(1-b) of income, and trying to "
                "save more can leave saving lower. In IS-LM, fiscal policy is partly crowded out, except at the zero "
                "bound, where money stops working and spending works fully. Sticky wages pile up at zero, and "
                "output, not pay, takes the shock: unemployment moves about six-tenths of a point per point of the "
                "output gap.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot(curve["coupons"], curve["evenings"], color=labs.BLUE, label="evenings")
    ax[0].plot(curve["coupons"], curve["goers"], color=labs.ORANGE, lw=1, label="want to go out")
    ax[0].plot(curve["coupons"], curve["sitters"], color="grey", lw=1, label="willing to sit")
    ax[0].set(title="The co-op", xlabel="coupons per couple", ylabel="per couple per week")
    ax[0].legend()
    ax[1].scatter(gap, ug, s=8, color=labs.BLUE)
    xx = np.linspace(gap.min(), gap.max(), 2)
    ax[1].plot(xx, np.polyval(np.polyfit(gap, ug, 1), xx), color=labs.ORANGE)
    ax[1].set(title="Okun's law, 1949-2025", xlabel="output gap, %", ylabel="unemployment gap, points")
    lab.fig = fig
    return lab
