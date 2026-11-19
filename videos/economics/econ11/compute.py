"""Precompute every number in Part 11 of *Economics, Built* ("Games").

    python -m videos.economics.econ11.compute            # everything missing (seconds)
    python -m videos.economics.econ11.compute --force tournament

Results are cached in ``.cache/econ11/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the Federation of American Scientists' estimates of nuclear warhead stockpiles via Our
World in Data, 1945-2026; transcribed results from Nagel 1995, Thaler's Financial Times contest of 1997, Flood 1952,
Henrich et al. 2001, Camerer, Ho and Chong 2004 and Axelrod 1980).  Models: Agora's games (``agora.games``), with the
Island's Part 11 truths.  Every random draw is seeded.

Items:
    guess       the guessing game: an Island crowd from the cognitive hierarchy, level-k steps, Nagel's and the FT's
                results
    dominance   iterated elimination in a small game (Gibbons's example)
    nash        best responses crossing in the battle of the sexes; all its equilibria
    grammar     coordination, the battle of the sexes, chicken and the stag hunt: pure and mixed equilibria
    penalty     the penalty kick's mixed equilibrium
    entry       the entry game: Nash equilibria of the strategic form, and the one that is subgame perfect
    centipede   McKelvey and Palfrey's four-move centipede by backward induction
    repeated    grim trigger's threshold, and the folk theorem's region
    tournament  Axelrod's round robin on the Island's field, with and without noise; the ecology; two noisy matches
    correlated  chicken's mixed equilibrium against the best correlated equilibrium (the traffic light)
    evolution   hawk and dove under the replicator; rock-paper-scissors; fictitious play
    levelk      the cognitive hierarchy against tau; fits to Nagel's and the FT's means
    bayes       a Bayesian game: is Ana tough?
    bargain     Rubinstein's split
    regret      regret matching on rock-paper-scissors and on chicken
    dial        the depth-of-reasoning dial's rows
    film        the intermission's data film: two nuclear stockpiles, 1945-2026
    melody      its data melody: the two stockpiles' total, year by year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import games as gm
from explainer.economics.data import tables

CACHE = Cache("econ11")
load = CACHE.load
TRUTH = island.truths(11)


def _bimatrix(cells):
    """((a, b), (a, b), (a, b), (a, b)) in row-major order for a 2x2 game -> (A, B)."""
    A = np.array([[cells[0][0], cells[1][0]], [cells[2][0], cells[3][0]]], float)
    B = np.array([[cells[0][1], cells[1][1]], [cells[2][1], cells[3][1]]], float)
    return A, B


def compute_guess() -> dict:
    t = TRUTH["guess"]
    nz = tables.NAGEL_1995.data["p_2_3"]
    ft = tables.THALER_FT_1997.data
    tau = gm.fit_tau(nz["mean"], t["p"])
    ch = gm.cognitive_hierarchy(tau, t["p"])
    rng = np.random.default_rng(t["seed"])
    lv = np.minimum(rng.poisson(tau, t["crowd"]), len(ch["choices"]) - 1)
    x = np.where(lv == 0, rng.uniform(0, 100, t["crowd"]), ch["choices"][lv] + rng.normal(0, t["noise"], t["crowd"]))
    x = np.clip(np.round(x), 0, 100)
    w = gm.guessing_winner(x, t["p"])
    return {"crowd": x, "levels": lv, "tau": tau, "winner": w, "steps": gm.level_k(t["p"], 8),
            "nagel": nz, "nagel_target": t["p"] * nz["mean"], "ft": ft, "p": t["p"],
            "bounds": [100 * t["p"] ** k for k in range(9)]}


def compute_dominance() -> dict:
    # Gibbons (1992), section 1.1.B: row Up/Down, column Left/Middle/Right
    A = np.array([[1, 1, 0], [0, 0, 2]], float)
    B = np.array([[0, 2, 1], [3, 1, 0]], float)
    ie = gm.iterated_elimination(A, B)
    return {"A": A, "B": B, **ie, "nash": gm.pure_nash(A, B)}


def compute_nash() -> dict:
    A, B = _bimatrix(TRUTH["grammar"]["battle"])
    br = gm.best_response_curves(A, B)
    eqs = gm.support_enumeration(A, B)
    return {"A": A, "B": B, **br, "equilibria": [{"p": e["p"][0], "q": e["q"][0], "row": e["row_payoff"],
                                                  "col": e["col_payoff"]} for e in eqs]}


def compute_grammar() -> dict:
    out = {}
    for name, cells in TRUTH["grammar"].items():
        A, B = _bimatrix(cells)
        out[name] = {"A": A, "B": B, "pure": gm.pure_nash(A, B), "mixed": gm.mixed_2x2(A, B)}
    T = TRUTH["pd"]
    A = np.array([[T["R"], T["S"]], [T["T"], T["P"]]])
    out["pd"] = {"A": A, "B": A.T, "pure": gm.pure_nash(A, A.T), "dominant": gm.iterated_elimination(A, A.T)}
    return out


def compute_penalty() -> dict:
    S = np.array(TRUTH["penalty"]["score"])          # kicker's scoring chance: rows kick left/right, cols dive
    m = gm.mixed_2x2(S, 1 - S)
    q = m["q"]
    by_side = S @ np.array([q, 1 - q])               # kicker's scoring rate when kicking each side
    p = m["p"]
    by_dive = np.array([p, 1 - p]) @ S               # scoring rate against each dive
    return {"S": S, "kick_left": p, "dive_left": q, "value": m["row_payoff"], "by_side": by_side,
            "by_dive": by_dive}


def compute_entry() -> dict:
    t = TRUTH["entry"]
    tree = gm.entry_game(t["fight"], t["accommodate"], t["stay_out"])
    bi = gm.backward_induction(tree)
    # the strategic form: entrant (enter, stay out) x incumbent (accommodate, fight if entry)
    A = np.array([[t["accommodate"][0], t["fight"][0]], [t["stay_out"][0], t["stay_out"][0]]], float)
    B = np.array([[t["accommodate"][1], t["fight"][1]], [t["stay_out"][1], t["stay_out"][1]]], float)
    return {"spe": bi["path"], "value": bi["value"], "nash": gm.pure_nash(A, B), "A": A, "B": B, **t}


def compute_centipede() -> dict:
    t = TRUTH["centipede"]
    tree = gm.centipede(t["moves"], t["start"], t["grow"])
    bi = gm.backward_induction(tree)
    takes = [(t["start"][0] * t["grow"] ** k, t["start"][1] * t["grow"] ** k) for k in range(t["moves"] + 1)]
    return {"path": bi["path"], "value": bi["value"], "takes": takes, "henrich": tables.HENRICH_2001.data, **t}


def compute_repeated() -> dict:
    T = TRUTH["pd"]
    A = np.array([[T["R"], T["S"]], [T["T"], T["P"]]])
    fr = gm.folk_region(A, A.T)
    thr = gm.grim_threshold(T["T"], T["R"], T["P"], T["S"])
    rows = []
    for d in TRUTH["repeated"]["deltas"]:
        coop = T["R"] / (1 - d)
        dev = T["T"] + d * T["P"] / (1 - d)
        rows.append({"delta": d, "cooperate": coop, "deviate": dev, "holds": coop >= dev})
    return {"threshold": thr, "rows": rows, "feasible": fr["feasible"], "rational": fr["rational"],
            "minmax": fr["minmax"], **T}


def compute_tournament() -> dict:
    t = TRUTH["tournament"]
    clean = gm.tournament(t["field"], t["rounds"], 0.0, t["repeats"], t["seed"])
    noisy = gm.tournament(t["field"], t["rounds"], t["noise"], t["repeats"], t["seed"])
    eco = gm.ecology(clean["matrix"], 150)
    def one_slip(name, rounds=30, at=4):
        """The strategy against itself with exactly one mistake: the second player's move in round ``at + 1``."""
        f = gm.STRATEGIES[name]
        ha, hb = [], []
        for k in range(rounds):
            x, y = f(ha, hb, None), f(hb, ha, None)
            if k == at:
                y = 1 - y
            ha.append(x)
            hb.append(y)
        return [ha, hb]

    m_tft, m_wsls = one_slip("TFT"), one_slip("WSLS")
    return {"field": list(t["field"]), "clean": {"score": clean["score"], "ranking": clean["ranking"]},
            "noisy": {"score": noisy["score"], "ranking": noisy["ranking"]}, "eco": eco,
            "tft_moves": m_tft, "wsls_moves": m_wsls, "noise": t["noise"], "rounds": t["rounds"],
            "axelrod": tables.AXELROD_1980.data}


def compute_correlated() -> dict:
    A, B = _bimatrix(TRUTH["grammar"]["chicken"])
    ce = gm.correlated_equilibrium(A, B)
    mixed = gm.mixed_2x2(A, B)
    return {"A": A, "B": B, "P": ce["P"], "ce": ce["row_payoff"], "mixed": mixed["row_payoff"],
            "p_dare": mixed["p"], "pure": gm.pure_nash(A, B)}


def compute_evolution() -> dict:
    h = TRUTH["hawkdove"]
    V, C = h["V"], h["C"]
    A = np.array([[(V - C) / 2, V], [0, V / 2]])
    paths = [gm.replicator(A, [x0, 1 - x0], T=25, steps=500)[:, 0] for x0 in (0.05, 0.3, 0.7, 0.95)]
    R = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], float)
    rps = gm.replicator(R, [0.6, 0.25, 0.15], T=40, steps=2000)
    fp = gm.fictitious_play(np.array([[1, -1], [-1, 1]], float), np.array([[-1, 1], [1, -1]], float), rounds=1500)
    return {"A": A, "ess": V / C, "is_ess": gm.is_ess(A, [V / C, 1 - V / C]), "paths": paths,
            "t": np.linspace(0, 25, 501), "rps": rps, "fp_row": fp["row"][:, 0], "fp_col": fp["col"][:, 0], **h}


def compute_levelk() -> dict:
    taus = np.linspace(0.05, 6, 120)
    means = [gm.cognitive_hierarchy(t)["mean"] for t in taus]
    nz, ft = tables.NAGEL_1995.data["p_2_3"], tables.THALER_FT_1997.data
    t_n, t_f = gm.fit_tau(nz["mean"]), gm.fit_tau(ft["mean"])
    ch_n, ch_f, ch_c = gm.cognitive_hierarchy(t_n), gm.cognitive_hierarchy(t_f), gm.cognitive_hierarchy(1.5)
    return {"taus": taus, "means": means, "tau_nagel": t_n, "tau_ft": t_f, "nagel": nz, "ft": ft,
            "chc": tables.CHC_2004.data, "ch_nagel": {"choices": ch_n["choices"][:7], "shares": ch_n["shares"][:7]},
            "ch_ft": {"choices": ch_f["choices"][:9], "shares": ch_f["shares"][:9]},
            "ch_15": {"choices": ch_c["choices"][:7], "shares": ch_c["shares"][:7], "mean": ch_c["mean"]}}


def compute_bayes() -> dict:
    b = TRUTH["bayes"]
    eqs = gm.bayes_nash_2x2([b["tough"], b["weak"]], [b["bo_vs_tough"], b["bo_vs_weak"]],
                            [b["prior_tough"], 1 - b["prior_tough"]])
    # Bo's expected payoff from entering, as the prior that Ana is tough varies (she fights if tough, shares if weak)
    ps = np.linspace(0, 1, 101)
    enter = [p * b["bo_vs_tough"][0][0] + (1 - p) * b["bo_vs_weak"][1][0] for p in ps]
    thr = b["bo_vs_weak"][1][0] / (b["bo_vs_weak"][1][0] - b["bo_vs_tough"][0][0])
    return {"equilibria": eqs, "ps": ps, "enter": enter, "threshold": thr, **b}


def compute_bargain() -> dict:
    d = TRUTH["bargain"]["delta"]
    grid = np.linspace(0.0, 0.99, 100)
    return {"delta": d, "share": gm.rubinstein(d)["proposer"], "grid": grid,
            "shares": [gm.rubinstein(x)["proposer"] for x in grid]}


def compute_regret() -> dict:
    R = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], float)
    rm = gm.regret_matching(R, -R, rounds=20000, seed=2000)
    A, B = _bimatrix(TRUTH["grammar"]["chicken"])
    rc = gm.regret_matching(A, B, rounds=20000, seed=2001)
    return {"rps_row": rm["row"], "rps_regret": rm["regret_row"], "chicken_row": rc["row"],
            "chicken_regret": rc["regret_row"]}


def compute_dial() -> dict:
    rows = [(e.who, e.year, e.design, e.sample, e.value, e.lo, e.hi) for e in dials.DIALS["reasoning_depth"].estimates]
    return {"rows": rows}


# ---------------------------------------------------------------------------------------------------------------
# the intermission: two stockpiles

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0
TREATIES = ((1963, "the Partial Test Ban Treaty"), (1972, "SALT I"), (1987, "the INF Treaty"), (1991, "START I"),
            (2010, "New START"))


def film_time(k: int, n: int) -> float:
    return 1.5 + FILM_SECONDS * k / (n - 1)


def compute_film() -> dict:
    us, ru = data.warheads("United States"), data.warheads("Russia")
    years = [y for y in us["year"] if y in set(ru["year"])]
    u = dict(zip(us["year"], us["value"]))
    r = dict(zip(ru["year"], ru["value"]))
    n = len(years)
    U, Rr = [u[y] for y in years], [r[y] for y in years]
    return {"years": years, "us": U, "ussr": Rr, "times": [film_time(k, n) for k in range(n)],
            "treaties": [{"year": y, "name": nm, "t": film_time(years.index(y), n)} for y, nm in TREATIES],
            "us_peak": (years[int(np.argmax(U))], max(U)), "ussr_peak": (years[int(np.argmax(Rr))], max(Rr)),
            "last": (years[-1], U[-1], Rr[-1])}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    total = np.array(f["us"]) + np.array(f["ussr"])
    times = f["times"]
    mel = score.data_melody(np.maximum(total, 1), MELODY_SECONDS, times=times, act=3, log=True, low=40, high=84)
    events = {"film_end": times[-1] + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.3, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], f["years"])],
                meta={"label": "the American and Soviet (later Russian) nuclear stockpiles together, year by year, "
                               "1945-2026, as a tune (computed)", "kind": "synthesized",
                      "needs": "headphones, for the sweep from left to right across the years"})
    ClipStore("econ11").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "total": total, "years": f["years"], "seconds": MELODY_SECONDS}


ITEMS = {
    "guess": compute_guess,
    "dominance": compute_dominance,
    "nash": compute_nash,
    "grammar": compute_grammar,
    "penalty": compute_penalty,
    "entry": compute_entry,
    "centipede": compute_centipede,
    "repeated": compute_repeated,
    "tournament": compute_tournament,
    "correlated": compute_correlated,
    "evolution": compute_evolution,
    "levelk": compute_levelk,
    "bayes": compute_bayes,
    "bargain": compute_bargain,
    "regret": compute_regret,
    "dial": compute_dial,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
