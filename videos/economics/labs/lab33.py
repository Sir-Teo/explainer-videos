"""Lab 33: crises: Minsky's borrowers, debt deflation, the costly-state-verification contract and the financial
accelerator, Kiyotaki and Moore's collateral cycle, Geanakoplos's leverage cycle, households' balance sheets on the
Island's counties, the crisis predictor on 150 years of data in and out of sample, the shape of financial recessions,
and Basel III's credit-gap guide."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import credit
from explainer.economics.island import truths

TITLE = "Crises: amplification, and how far it can be foreseen"
GOAL = ("Watch a boom turn hedge borrowers into Ponzi borrowers; compute debt deflation; trace the external finance "
        "premium and the accelerator; solve the collateral cycle exactly and separate its static and dynamic "
        "multipliers; solve the leverage cycle; recover a planted spending response from county data; and fit the "
        "crisis predictor to the Macrohistory Database, in sample and, honestly, out of sample.")
TASKS = [
    "Collateral: raise the elasticity of land supply eta from 2 to 4. How do the static and dynamic multipliers "
    "change, and why?",
    "Prediction: start the out-of-sample scoring in 1975 instead of 1950. Does the real-loans model do better?",
    "Basel's guide: compute it for Ireland and the United Kingdom. When would each have reached the full buffer?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(33)

    M = credit.minsky_boom(**{**T["minsky"], "seed": T["minsky"]["seed"] + seed})
    lab.row("Minsky on the Island: hedge borrowers at the start and end; Ponzi at the end",
            f"{100 * M['hedge'][0]:.0f}%, {100 * M['hedge'][-1]:.0f}%; {100 * M['ponzi'][-1]:.0f}%")
    assert M["hedge"][0] > 0.9 and M["ponzi"][-1] > M["ponzi"][0]

    b = credit.debt_deflation(1.0, [0.1] * 4, -0.05, repay=0.05)
    lab.row("debt deflation: debt over income after four years of 10% deflation, repaying 5% a year", f"{b[-1]:.3f}")
    assert abs(b[-1] - 1 / 0.9 ** 4) < 1e-9

    B = T["bgg"]
    C = credit.csv_contract(B["sigma"], B["mu"])
    s2 = credit.premium_at(2.0, C)
    base = credit.accelerator(1.0, C, K_star=B["K_star"], theta=B["theta"])
    low = credit.accelerator(1 - B["N_fall"], C, K_star=B["K_star"], theta=B["theta"])
    lab.row("the debt contract at leverage 2: premium; default rate",
            f"{100 * (s2 - 1):.2f}%; {100 * float(np.interp(2.0, C['leverage'], C['default'])):.1f}%")
    lab.row("the accelerator: investment after a 10% loss of net worth", f"{100 * (low['K'] / base['K'] - 1):+.2f}%")
    assert np.all(np.diff(C["premium"]) > 0) and low["K"] < base["K"]

    K = T["km"]
    A = credit.km_amplification(K["shock"], R=K["R"], eta=K["eta"], a=K["a"], c=K["c"])
    lab.row("Kiyotaki-Moore: farmers' land per unit of the shock, price fixed and with feedback; the land price",
            f"{A['static']:.2f}, {A['dynamic']:.2f}; {A['q0']:+.2f}%")
    assert A["dynamic"] > 3 * A["static"]

    Ls, Ln = credit.leverage_static(0.2, True), credit.leverage_static(0.2, False)
    cyc = credit.leverage_cycle(0.2)
    lab.row("the leverage cycle: price without and with borrowing; today and after bad news; margins",
            f"{Ln['p']:.3f}, {Ls['p']:.3f}; {cyc['p0']:.3f} -> {cyc['pD']:.3f}; {100 * cyc['margin0']:.0f}% -> "
            f"{100 * cyc['marginD']:.0f}%")
    assert cyc["ok"] and Ls["p"] > Ln["p"] and cyc["marginD"] > cyc["margin0"]

    Cn = credit.counties(**{**T["counties"], "seed": T["counties"]["seed"] + seed})
    lab.row("the Island's counties: spending per dollar of housing wealth, overall and by leverage fifth (cents)",
            f"{100 * Cn['mpc']:.1f}; " + ", ".join(f"{100 * q['mpc']:.1f}" for q in Cn["by_quintile"]))
    assert Cn["by_quintile"][-1]["mpc"] > Cn["by_quintile"][0]["mpc"]

    P = credit.jst_panel(data.jst())
    for measure in ("real_loans", "credit_gdp"):
        R = credit.crisis_predictor(P, measure)
        lab.row(f"the predictor ({measure}): AUC in sample; out of sample from 1950 ({R['crises_oos']} crises)",
                f"{R['auc_in']:.2f}; {R['auc_oos']:.2f}")
    O = credit.boom_odds(P)
    lab.row("a crisis within three years, by fifth of the three-year rise in loans to GDP",
            ", ".join(f"{100 * v:.0f}%" for v in O["by_quintile"]) + f"; both credit and houses {100 * O['both']:.0f}%")
    assert O["by_quintile"][-1] > 2 * O["by_quintile"][0]
    Rc = credit.recession_paths(P, first=1948)
    lab.row("since 1948: output per head five years after the peak, normal and financial recessions",
            f"{Rc['normal'][5]:+.1f}%, {Rc['financial'][5]:+.1f}% ({Rc['n_normal']} and {Rc['n_financial']})")
    assert Rc["normal"][5] > Rc["financial"][5]

    D = data.jst()
    iso, yr = np.array(D["iso"]), np.array(D["year"], int)
    m = (iso == "ESP") & (yr >= 1960) & (yr <= 2015)
    with np.errstate(divide="ignore", invalid="ignore"):
        cg = 100 * np.array(D["tloans"], float)[m] / np.array(D["gdp"], float)[m]
    buf = credit.ccyb_guide(credit.one_sided_gap(cg))
    first = [int(y) for y, v in zip(yr[m], buf) if v >= 2.5 and y >= 1990]
    lab.row("Basel's guide for Spain: the first year of the full buffer after 1990", f"{first[0] if first else None}")

    lab.note = ("Finance amplifies: debt fixed in money grows heavier as prices fall, a loss of net worth raises the "
                "cost of borrowing, land that is both an input and collateral multiplies a small shock several times, "
                "and leverage changes whose opinion sets prices. Credit booms raise the odds of a crisis several times "
                "over, but most end quietly, and out of sample the date is hard to call.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    st, dy = A["static_path"], A["dynamic_path"]
    ax[0].plot(st["t"][:16], st["k"][:16], color="grey", label="land price held fixed")
    ax[0].plot(dy["t"][:16], dy["k"][:16], color=labs.ORANGE, label="with the price's feedback")
    ax[0].axhline(0, color="grey", lw=0.8)
    ax[0].set(title="Kiyotaki-Moore: farmers' land after a 1% shock", xlabel="periods", ylabel="% from normal")
    ax[0].legend()
    R = credit.crisis_predictor(P, "real_loans")
    ax[1].plot(R["roc_in"]["fpr"], R["roc_in"]["tpr"], color=labs.BLUE, label=f"in sample ({R['auc_in']:.2f})")
    ax[1].plot(R["roc_oos"]["fpr"], R["roc_oos"]["tpr"], color="red", label=f"out of sample ({R['auc_oos']:.2f})")
    ax[1].plot([0, 1], [0, 1], color="grey", ls="--")
    ax[1].set(title="Predicting crises from credit growth", xlabel="calm years flagged", ylabel="crises caught")
    ax[1].legend()
    lab.fig = fig
    return lab
