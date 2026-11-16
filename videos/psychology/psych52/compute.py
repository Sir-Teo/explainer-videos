"""Precompute every number in Part 52 of *Psychology, Built* ("Designing for Minds").

    python -m videos.psychology.psych52.compute            # everything missing (seconds)

Results are cached in ``.cache/psych52/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.work``).

Items:
    mhp         the Model Human Processor's reaction-time predictions
    klm         keystroke-level predictions for three methods of one task, and a checkout form two ways
    ernestine   a toy critical path: a new workstation with fewer keystrokes but a longer critical path
    pointing    a pointing study (four distances, four widths): fitted Fitts's law, effective width, throughput
    steering    the steering law over tunnels of several lengths and widths
    menus       menu time by breadth for 64 items, practised and unpractised
    foraging    the marginal value theorem: optimal time in a patch by travel time
    discovery   the share of usability problems found by n users, with equal and unequal detectability
    charts      judgement error by graphical encoding
    contrast    WCAG contrast ratios for a set of colour pairs
    habit       automaticity curves and days to a habit for 96 simulated people
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import work as Wk

CACHE = Cache("psych52")
load = CACHE.load


def compute_mhp() -> dict:
    return {k: Wk.mhp_reaction(k) for k in ("simple", "physical", "name")}


def compute_klm() -> dict:
    # delete a word in a document: three methods (keyboard shortcut; mouse double-click and Delete; menu)
    methods = {"keys": "MKKKKK", "mouse": "HMPBBBBHMK", "menu": "HMPBBMPBBMPBB"}
    times = {k: Wk.klm_time(v) for k, v in methods.items()}
    # a checkout form: name, email, card number, expiry, CVC, address; two designs
    form_a = ("HMPBB" + "HM" + "K" * 12 + "HMPBB" + "HM" + "K" * 20 + "HMPBB" + "HM" + "K" * 16 + "HMPBB" + "HMPBB"
              + "MPBB" + "HM" + "K" * 4 + "HMPBB" + "HM" + "K" * 3 + "HMPBB" + "HM" + "K" * 25 + "HMPBB")
    form_b = ("HMPBB" + "M" + "K" * 12 + "K" + "M" + "K" * 20 + "K" + "M" + "K" * 16 + "K" + "M" + "K" * 4 + "K"
              + "M" + "K" * 3 + "K" + "M" + "K" * 25 + "MK")
    ta, tb = Wk.klm_time(form_a), Wk.klm_time(form_b)
    counts = {o: (form_a.count(o), form_b.count(o)) for o in "KPBHM"}
    return {"methods": list(methods), "ops": [methods[k] for k in methods], "times": np.array(list(times.values())),
            "form_a": ta, "form_b": tb, "counts": {k: list(v) for k, v in counts.items()},
            "skilled_a": Wk.klm_time(form_a, k=0.12), "skilled_b": Wk.klm_time(form_b, k=0.12)}


def compute_ernestine() -> dict:
    # a toy schedule: the old workstation's call, and a new one with fewer keystrokes whose saved keystrokes were off
    # the critical path (done while the customer was talking) and whose added steps are on it
    old = {"greet": 1.8, "listen": 6.2, "keys (in parallel)": 0.0, "look up": 2.0, "close": 1.2}
    new = {"greet": 1.8, "listen": 6.2, "keys (in parallel)": 0.0, "look up": 2.0, "extra keystroke on path": 0.6,
           "close": 1.2}
    return {"old": sum(old.values()), "new": sum(new.values()), "old_steps": list(old), "new_steps": list(new),
            "old_t": np.array(list(old.values())), "new_t": np.array(list(new.values()))}


def compute_pointing() -> dict:
    rng = np.random.default_rng(5201)
    rows = []
    for D in (64, 128, 256, 512):
        for Wd in (8, 16, 32, 64):
            r = Wk.fitts_effective(n=24, distance=D, width=Wd, a=0.2, b=0.2, seed=int(rng.integers(1 << 30)))
            rows.append((D, Wd, r["ID"], r["IDe"], float(r["t"].mean()), r["throughput"], r["errors"]))
    a = np.array(rows)
    b, c = np.polyfit(a[:, 2], a[:, 4], 1)
    be, ce = np.polyfit(a[:, 3], a[:, 4], 1)
    return {"D": a[:, 0], "W": a[:, 1], "ID": a[:, 2], "IDe": a[:, 3], "MT": a[:, 4], "TP": a[:, 5],
            "err": a[:, 6], "a": float(c), "b": float(b), "ae": float(ce), "be": float(be),
            "r": float(np.corrcoef(a[:, 2], a[:, 4])[0, 1]), "TP_mean": float(a[:, 5].mean())}


def compute_steering() -> dict:
    L = np.array([100, 200, 400, 800])
    W = np.array([10, 20, 40])
    grid = np.array([[Wk.steering_time(l, w) for l in L] for w in W])
    return {"L": L, "W": W, "t": grid}


def compute_menus() -> dict:
    p = Wk.menu_time()
    u = Wk.menu_time(practised=False, read=0.25)
    return {"breadth": p["breadth"], "depth": p["depth"], "practised": p["time"], "unpractised": u["time"]}


def compute_foraging() -> dict:
    tr = np.array([2, 5, 10, 20, 40, 80])
    res = [Wk.mvt_leave(float(t)) for t in tr]
    tt = np.linspace(0, 120, 241)
    return {"travel": tr, "leave": np.array([r["t"] for r in res]), "rate": np.array([r["rate"] for r in res]),
            "tt": tt, "gain": Wk.patch_gain(tt)}


def compute_discovery() -> dict:
    n = np.arange(1, 21)
    return Wk.discovery(n, a=0.6, b=1.34, seed=5202)


def compute_charts() -> dict:
    enc = list(Wk.STEVENS_EXP)
    out = [Wk.graphical_error(e, seed=5203 + i) for i, e in enumerate(enc)]
    return {"enc": enc, "log_err": np.array([o["log_err"] for o in out]), "mae": np.array([o["mae"] for o in out]),
            "exp": np.array([Wk.STEVENS_EXP[e] for e in enc])}


def compute_contrast() -> dict:
    pairs = [("black on white", (0, 0, 0), (255, 255, 255)), ("grey 767676 on white", (118, 118, 118), (255, 255, 255)),
             ("grey 959595 on white", (149, 149, 149), (255, 255, 255)), ("red on green", (255, 0, 0), (0, 128, 0)),
             ("yellow on white", (255, 255, 0), (255, 255, 255)), ("white on navy", (255, 255, 255), (0, 0, 128))]
    return {"names": [p[0] for p in pairs], "fg": np.array([p[1] for p in pairs]), "bg": np.array([p[2] for p in pairs]),
            "ratio": np.array([Wk.contrast_ratio(p[1], p[2]) for p in pairs])}


def compute_habit() -> dict:
    days = np.arange(0, 201)
    people = Wk.habit_people(seed=5204)
    return {"days": days, "curve": Wk.habit_curve(days), "people": np.sort(people),
            "median": float(np.median(people)), "share_21": float(np.mean(people <= 21)),
            "lo": float(people.min()), "hi": float(people.max())}


ITEMS = {"mhp": compute_mhp, "klm": compute_klm, "ernestine": compute_ernestine, "pointing": compute_pointing,
         "steering": compute_steering, "menus": compute_menus, "foraging": compute_foraging,
         "discovery": compute_discovery, "charts": compute_charts, "contrast": compute_contrast,
         "habit": compute_habit}

if __name__ == "__main__":
    CACHE.main(ITEMS)
