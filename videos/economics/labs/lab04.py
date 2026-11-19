"""Lab 4: regress through a cloud, instrument it, omit ability, run a lottery, push the council, and scale a trial."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import econometrician as em
from explainer.economics.island import truths

TITLE = "The evidence: simultaneity, instruments, selection, lotteries and the Lucas critique"
GOAL = ("Simulate the Island's fish market many times and compare least squares with its probability limit and with "
        "the storm and feast instruments; check the omitted-variable formula on the school records and recover the "
        "planted return with the new school; see that choice biases the apprenticeship and a lottery does not; watch "
        "the council's menu fail once it is used; and find how many villages a trial needs to see a spillover.")
TASKS = [
    "Make feasts as variable as storms (or remove them). Which curve does least squares now find, and why does its "
    "probability limit say so?",
    "In the school records, make the new school move schooling by only 0.2 years. What happens to the first-stage F, "
    "to the spread of the IV estimate over many samples, and to its median?",
    "Make the Island's expectations rational (E = 8 from the first year of the push). What does output do now?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(4)

    # simultaneity: least squares converges to the weighted mixture, not to either curve
    s = dict(T["season"])
    b, d = s["b"], s["d"]
    slopes, storms, feasts = [], [], []
    for k in range(300):
        s["seed"] = 10_000 + 7 * k + seed
        x = em.fish_season(**s)
        slopes.append(em.ols(x["q"], x["p"])["slope"])
        storms.append(em.wald(x["q"], x["p"], x["storm"])["estimate"])
        feasts.append(em.wald(x["q"], x["p"], x["feast"])["estimate"])
    # the variances of the two curves' total shifts (shocks plus feasts or storms)
    fp, F = s["feast"]
    sp, S = s["storm"]
    var_u = s["noise"][0] ** 2 + F ** 2 * fp * (1 - fp)
    var_v = s["noise"][1] ** 2 + S ** 2 * sp * (1 - sp)
    plim = em.simultaneity_slope(b, d, var_u, var_v)
    lab.row("least squares, mean of 300 seasons", f"{np.mean(slopes):+.1f} fish per dollar (plim {plim:+.1f})")
    lab.row("storm instrument (demand, planted -66.7)", f"median {np.median(storms):.1f}")
    lab.row("feast instrument (supply, planted +88.9)", f"median {np.median(feasts):.1f}")
    assert abs(np.mean(slopes) - plim) < 2.0
    assert abs(np.median(storms) + b) < 3 and abs(np.median(feasts) - d) < 3

    # omitted ability: the formula, and the instrument
    sc = dict(T["schooling"], n=60_000)
    sc["return_"] = sc.pop("return")
    r = em.schooling_records(**sc)
    bias = em.ovb(sc["ability_on_wage"], np.cov(r["school"], r["ability"])[0, 1], r["school"].var())
    ols = em.ols(r["logw"], r["school"])["slope"]
    iv = em.iv(r["logw"], r["school"], r["near"])
    lab.row("schooling: least squares / truth + formula's bias", f"{ols:.4f} / {sc['return_'] + bias:.4f}")
    lab.row("the new school as instrument", f"{iv['estimate']:.4f} (first-stage F {iv['F']:.0f})")
    assert abs(ols - (sc["return_"] + bias)) < 0.003 and abs(iv["estimate"] - sc["return_"]) < 0.01

    # the apprenticeship: by choice and by lottery, many times
    a = dict(T["apprentice"])
    chose, lot, cover = [], [], 0
    reps = 300
    for k in range(reps):
        a["seed"] = 20_000 + k + seed
        x = em.apprenticeship(**a)
        chose.append(x["by_choice"]["diff"])
        lt = x["by_lottery"]
        lot.append(lt["diff"])
        cover += abs(lt["diff"] - a["effect"]) <= 1.96 * lt["se"]
    lab.row("apprenticeship by choice: mean of 300", f"{np.mean(chose):+.3f} (planted {a['effect']:+.2f})")
    lab.row("by lottery: mean, and 95% interval coverage", f"{np.mean(lot):+.3f}, {100 * cover / reps:.0f}%")
    assert np.mean(chose) < 0 and abs(np.mean(lot) - a["effect"]) < 0.01 and 0.9 < cover / reps < 0.99

    # Lucas: the calm years' menu, and what happens when the council uses it
    L = em.lucas_islands(**T["lucas"])
    c = L["calm"]
    menu = em.ols(L["y"][c], L["pi"][c])
    promise = menu["beta"][0] + menu["slope"] * T["lucas"]["pi_push"]
    lab.row("the menu's slope, and its promise at 8%", f"{menu['slope']:.2f}; output {promise:.1f}")
    lab.row("output: first year of the push / last ten years", f"{L['y'][~c][0]:.1f} / {L['y'][~c][-10:].mean():.1f}")
    assert abs(L["y"][~c][-10:].mean() - L["ystar"]) < 0.5

    # spillovers: within-village estimates against the policy's total effect, and the power of more villages
    v = dict(T["villages"])
    out = {}
    for G in (40, 100, 400):
        sp_hat, tot = [], []
        for k in range(100):
            v.update(villages=G, seed=30_000 + 13 * k + G + seed)
            x = em.village_trial(**v)
            sp_hat.append(x["spill_hat"])
            tot.append(x["total"])
        out[G] = (np.mean(sp_hat), np.std(sp_hat), np.mean(tot))
        lab.row(f"{G} villages: spillover estimate (mean, sd), total effect",
                f"{out[G][0]:+.3f} ({out[G][1]:.3f}), {out[G][2]:+.3f}")
    assert out[400][1] < out[40][1] / 2.5
    lab.note = ("Least squares through an equilibrium cloud converges to a mixture of the two slopes; an instrument "
                "that moves one curve recovers the other; the omitted-variable formula predicts the regression's "
                "bias exactly; a lottery's estimate is centred on the truth with honest intervals; a menu estimated "
                "in calm years fails once it is used; and a spillover is seen only across villages, so its precision "
                "grows with the number of villages.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].hist(slopes, bins=30, color="#C9A0FF", alpha=0.8, label="least squares")
    ax[0].hist(storms, bins=30, color="#7EC8F5", alpha=0.8, label="storm instrument")
    ax[0].hist(feasts, bins=30, color="#F2B84B", alpha=0.8, label="feast instrument")
    for val, col in ((-b, "#7BD88F"), (d, "#7BD88F")):
        ax[0].axvline(val, color=col, lw=2, ls="--")
    ax[0].set(title="300 seasons of the fish market", xlabel="estimated slope, fish per dollar", ylabel="seasons")
    ax[0].legend()
    ax[1].hist(chose, bins=30, color=labs.ORANGE, alpha=0.8, label="by choice")
    ax[1].hist(lot, bins=30, color="#7BD88F", alpha=0.8, label="by lottery")
    ax[1].axvline(a["effect"], color="white", lw=2, ls="--", label="planted")
    ax[1].set(title="The apprenticeship, 300 times", xlabel="difference in mean log earnings", ylabel="samples")
    ax[1].legend()
    lab.fig = fig
    return lab
