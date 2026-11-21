"""Lab 49: the economic approach: Becker's offenders and planner, the chance against the sentence, police measured
on the Island, a Choo-Siow marriage market, same-sex siblings on the 1980 census, STAR within schools, teachers' value
added and the move test, cigarette demand by 2SLS, and a rational addict."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import family as fm
from explainer.economics.island import truths

TITLE = "The economic approach"
GOAL = ("Build Becker's offenders and find what deters them; measure police and crime three ways; read the gains from "
        "marriage from counts; estimate the effect of a third child, of a small class and of a teacher; and watch a "
        "rational addict respond to news of a price rise.")
TASKS = [
    "Offenders: make them like risk (a CARA coefficient of -0.3). Which deters more now, the chance or the sentence?",
    "Police: raise the counting error from 0.35 to 0.7. What happens to the first-difference estimate, and why?",
    "Teachers: estimate value added from one year instead of two. What happens to the reliability and to the spread "
    "of the raw estimates?",
]


def _pct(x, ref):
    ref = np.sort(ref)
    return 100.0 * np.searchsorted(ref, x, side="right") / len(ref)


def run(seed=0):
    lab = labs.Lab()
    T = truths(49)

    O = T["offenders"]
    rng = np.random.default_rng(O["seed"] + seed)
    g = O["median"] * np.exp(O["sigma"] * rng.standard_normal(O["n"]))
    play = fm.play_doubling(O["p"], O["sentence"], g, T["kinds"])
    for k, r in play.items():
        lab.row(f"{k}: offend now, chance doubled, sentence doubled",
                f"{100 * r['start']:.0f}%, {100 * r['double_p']:.0f}%, {100 * r['double_s']:.0f}%")
    assert abs(play["risk-neutral"]["double_p"] - play["risk-neutral"]["double_s"]) < 1e-9
    assert play["risk-averse"]["double_s"] < play["risk-averse"]["double_p"]
    assert play["present-minded"]["double_p"] < play["present-minded"]["double_s"]

    P = T["planner"]
    plan = fm.optimal_enforcement(g, P["harm"], P["cost_p"], P["f_max"], n_p=60, n_f=60)
    lab.row("Becker's planner: the fine, the chance, the share offending",
            f"{plan['f_star']:.0f}, {100 * plan['p_star']:.0f}%, {100 * plan['offences_star']:.1f}%")
    assert plan["f_star"] == P["f_max"]

    pb = fm.police_blocks(**{**T["police"], "seed": T["police"]["seed"] + seed})
    lab.row("police: naive; first differences, noisy; random (truth -0.3)",
            f"{pb['naive']:+.2f}; {pb['fd_noisy']:+.2f}; {pb['experiment']:+.2f}")

    M = T["marriage"]
    eq = fm.choo_siow(M["men"], M["women"], np.array(M["phi"]))
    phi_hat = fm.choo_siow_estimate(eq["mu"], eq["single_men"], eq["single_women"])
    lab.row("Choo-Siow: the surplus read back exactly (largest error)", f"{np.abs(phi_hat - M['phi']).max():.1e}")
    assert np.allclose(phi_hat, M["phi"], atol=1e-6)

    F = data.fertility()
    same = (np.array(F["boy1"]) == np.array(F["boy2"])).astype(float)
    w = fm.wald(same, F["morekids"], F["work"])
    lab.row("same-sex siblings: first stage; weeks of work, Wald (s.e.)",
            f"{w['first_stage']:.3f}; {w['wald']:.1f} ({w['se']:.1f})")

    S = data.star()
    st, r, m = np.array(S["stark"]), np.array(S["readk"]), np.array(S["mathk"])
    ok = (st != "") & np.isfinite(r) & np.isfinite(m)
    reg = ok & (st != "small")
    p = (_pct(r, r[reg]) + _pct(m, m[reg])) / 2
    lab.row("STAR, kindergarten: small minus regular, percentile points (raw)",
            f"{p[ok & (st == 'small')].mean() - p[ok & (st == 'regular')].mean():.1f}")

    tv = fm.teacher_va(**{**T["teachers"], "seed": T["teachers"]["seed"] + seed})
    lab.row("teachers: spread raw, shrunk, true; the move test",
            f"{tv['sd_raw']:.3f}, {tv['sd_shrunk']:.3f}, {tv['sd_true']:.3f}; {tv['forecast_coef']:.2f}")

    C = data.cigarettes()
    yr = np.array(C["year"])
    k = yr == 1995
    cpi = np.array(C["cpi"])[k]
    lq = np.log(np.array(C["packs"])[k])
    lp = np.log(np.array(C["price"])[k] / cpi)
    z = (np.array(C["taxs"])[k] - np.array(C["tax"])[k]) / cpi
    Z = np.column_stack([np.ones(k.sum()), z])
    lph = Z @ np.linalg.lstsq(Z, lp, rcond=None)[0]
    b = np.linalg.lstsq(np.column_stack([np.ones(k.sum()), lph]), lq, rcond=None)[0]
    lab.row("cigarettes, 1995: 2SLS elasticity with the sales tax", f"{b[1]:.2f}")
    assert -1.5 < b[1] < -0.7

    A = T["addiction"]
    ra = fm.addiction_path(**A, rational=True)
    my = fm.addiction_path(**A, rational=False)
    i0, i1 = A["announce_at"], A["rise_at"]
    lab.row("addiction: change in use between the news and the rise (rational; myopic)",
            f"{100 * (ra['consumption'][i1 - 1] / ra['consumption'][i0 - 1] - 1):+.0f}%; "
            f"{100 * (my['consumption'][i1 - 1] / my['consumption'][i0 - 1] - 1):+.0f}%")

    lab.note = ("Who offends depends on the expected punishment and on how offenders weigh risk and time; police go "
                "where crime is, so only designs that move them for other reasons measure their effect; counts of "
                "marriages reveal the gains from each match; a third child costs its mother weeks of work; small "
                "classes raise scores; shrunk value added passes the move test; smokers respond to price and look "
                "ahead.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    t = np.arange(40)
    ax[0].plot(t, ra["consumption"][:40], color=labs.ORANGE, label="rational")
    ax[0].plot(t, my["consumption"][:40], color=labs.BLUE, label="myopic")
    ax[0].axvline(i0, color="grey", ls=":")
    ax[0].axvline(i1, color="grey", ls="--")
    ax[0].set(title="use of an addictive good", xlabel="period")
    ax[0].legend()
    ax[1].scatter(lp, lq, s=12, color=labs.BLUE)
    ax[1].set(title="cigarettes by state, 1995", xlabel="log real price", ylabel="log packs a head")
    lab.fig = fig
    return lab
