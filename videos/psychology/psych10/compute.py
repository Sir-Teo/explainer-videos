"""Precompute every number in Part 10 of *Psychology, Built* ("Chemistry and Clocks").

    python -m videos.psychology.psych10.compute            # everything missing (about a minute), into .cache/psych10/
    python -m videos.psychology.psych10.compute --force clock

Results are cached in ``.cache/psych10/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.body``); the published figures they are set beside come from the
Archive.  Nothing here is random except the animals in ``tolerance``, which are seeded.

Items:
    clock      the model clock left alone, on a 24-hour day, and on Kleitman's 28-hour day
    light      a phase response curve; re-entrainment after flights of three, six and nine time zones
    sleep      the two-process model: four ordinary days; a night without sleep and the recovery
    alert      alertness through an ordinary day and through a night without sleep
    debt       lapses of attention over two weeks at eight, six and four hours in bed
    stress     the stress loop: its daily curve, a one-hour stressor, and the same with a worn brake
    dose       Hill curves, a competitive antagonist, first- and zero-order elimination, a day of caffeine
    tolerance  the opponent process over ten doses; a large dose in the usual place and in a new one
    chrono     midsleep and social jetlag for three example sleepers
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import archive
from explainer.psychology.psyche import body as B

CACHE = Cache("psych10")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def _thin(t, *ys, step=10):
    return (t[::step], *[y[::step] for y in ys])


# ---------------------------------------------------------------------------
def compute_clock() -> dict:
    c = B.Clock()
    t, x, _ = c.run(24.0 * 12, lambda _t: 0.0)
    home = B.entrain(c)
    cave_dim, cave_room = B.entrain(c, day=28.0, lux=40.0), B.entrain(c, day=28.0, lux=300.0)
    days = np.array([22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0])
    locked = np.array([bool(B.entrain(c, day=float(d))["locked"]) for d in days])
    tt, xx = _thin(t, x)
    th, xh = _thin(home["t"][-24 * 20 * 4:], home["x"][-24 * 20 * 4:])
    cz = archive.CZEISLER_1999.data
    return {"free_period": B.free_running_period(c), "published_period": cz["period_h"], "t": tt, "x": xx,
            "home_t": th - th[0], "home_x": xh, "home_minimum": home["minimum_at"], "home_period": home["period"],
            "cave_period_dim": cave_dim["period"], "cave_period_room": cave_room["period"],
            "cave_locked": bool(cave_dim["locked"] or cave_room["locked"]), "days": days, "locked": locked,
            "cave_minima": cave_dim["minima"][-12:] % 28.0}


def compute_light() -> dict:
    c = B.Clock()
    p = B.phase_response(c, steps=24)
    out = {"prc_h": p["hours_from_minimum"], "prc_shift": p["shift"], "max_delay": float(p["shift"].min()),
           "max_advance": float(p["shift"].max()),
           "delay_at": float(p["hours_from_minimum"][p["shift"].argmin()]),
           "advance_at": float(p["hours_from_minimum"][p["shift"].argmax()])}
    for z in (3, 6, 9):
        for name, zones in (("east", z), ("west", -z)):
            j = B.jet_lag(zones, c)
            out[f"{name}_{z}_days"] = j["days_to_adjust"]
            out[f"{name}_{z}_off"] = j["hours_off"][:12]
    return out


def compute_sleep() -> dict:
    b = archive.BORBELY_1982.data
    r = B.two_process(hours=144.0, s0=0.5)
    lost = B.two_process(hours=144.0, s0=0.5, keep_awake=[(40.0, 71.0)])
    usual = [e - s for s, e in r["episodes"][2:]]
    recovery = [e - s for s, e in lost["episodes"] if s >= 70.9][0]
    awake_before = 71.0 - [e for s, e in lost["episodes"] if e < 40.0][-1]
    sel = slice(None, None, 20)
    return {"tau_rise": b["tau_rise_h"], "tau_fall": b["tau_fall_h"], "t": r["t"][sel], "S": r["S"][sel],
            "upper": r["upper"][sel], "lower": r["lower"][sel], "asleep": r["asleep"][sel],
            "bed": float(r["episodes"][3][0] % 24), "rise": float(r["episodes"][3][1] % 24), "usual": float(np.mean(usual)),
            "lost_t": lost["t"][sel], "lost_S": lost["S"][sel], "lost_upper": lost["upper"][sel],
            "lost_lower": lost["lower"][sel], "lost_asleep": lost["asleep"][sel], "awake_before": float(awake_before),
            "recovery": float(recovery)}


def compute_alert() -> dict:
    r = B.two_process(hours=144.0, s0=0.5)
    lost = B.two_process(hours=144.0, s0=0.5, keep_awake=[(40.0, 71.0)])
    a, al = B.alertness(r["t"], r["S"]), B.alertness(lost["t"], lost["S"])
    day = (r["t"] >= 72) & (r["t"] < 96) & ~r["asleep"]
    night = (lost["t"] >= 31) & (lost["t"] < 71)
    t_n, a_n = lost["t"][night], al[night]
    low = float(t_n[a_n.argmin()])
    at = lambda h: float(al[np.argmin(np.abs(lost["t"] - h))])  # noqa: E731
    sel = slice(None, None, 20)
    return {"day_t": (r["t"][day] % 24)[sel], "day_a": a[day][sel], "night_t": t_n[sel], "night_a": a_n[sel],
            "lowest_clock": low % 24, "at_dawn": at(low), "next_afternoon": at(63.0), "second_wind": at(63.0) - at(low)}


def compute_debt() -> dict:
    v = archive.VAN_DONGEN_2003.data
    days = np.arange(1, v["days"] + 1)
    out = {"days": days, "threshold": v["threshold_awake_h"]}
    for h in v["hours_in_bed"]:
        out[f"lapses_{h}"] = B.lapses(float(h), v["days"])
    out["excess_6"] = 24 - 6 - v["threshold_awake_h"]
    out["excess_4"] = 24 - 4 - v["threshold_awake_h"]
    out["ratio"] = out["excess_4"] / out["excess_6"]
    return out


def compute_stress() -> dict:
    base = B.hpa(hours=96.0)
    hit = B.hpa(hours=96.0, stress=[(58.0, 1.0, 3.0)])
    worn0 = B.hpa(hours=96.0, feedback=0.3)
    worn = B.hpa(hours=96.0, feedback=0.3, stress=[(58.0, 1.0, 3.0)])
    day = (base["t"] >= 48) & (base["t"] < 72)
    extra, extra_w = hit["cortisol"] - base["cortisol"], worn["cortisol"] - worn0["cortisol"]
    gone = float(base["t"][np.where(extra > 0.1 * extra.max())[0][-1]] - 59.0)
    gone_w = float(base["t"][np.where(extra_w > 0.1 * extra_w.max())[0][-1]] - 59.0)
    sel = slice(None, None, 20)
    return {"t": base["t"][sel], "cortisol": base["cortisol"][sel], "crh": base["crh"][sel], "acth": base["acth"][sel],
            "hit": hit["cortisol"][sel], "worn": worn["cortisol"][sel], "worn_base": worn0["cortisol"][sel],
            "peak_hour": float(base["t"][day][base["cortisol"][day].argmax()] % 24),
            "trough_hour": float(base["t"][day][base["cortisol"][day].argmin()] % 24),
            "swing": float(base["cortisol"][day].max() / base["cortisol"][day].min()), "stress_at": 58.0 % 24,
            "extra_peak": float(extra.max()), "gone_hours": gone, "worn_peak": float(extra_w.max()),
            "worn_gone_hours": gone_w, "worn_mean_ratio": float(worn0["cortisol"][day].mean() / base["cortisol"][day].mean())}


def compute_dose() -> dict:
    d = np.logspace(-2, 2, 161)
    t = np.linspace(0, 24, 241)
    caf = B.dosing([8.0, 13.0, 16.0], hours=48.0, half_life=5.0)
    one = B.dosing([8.0], hours=48.0, half_life=5.0)
    at = lambda arr, h: float(arr[np.searchsorted(caf["t"], h)])  # noqa: E731
    sel = slice(None, None, 20)
    return {"dose": d, "hill_1": B.occupancy(d), "hill_3": B.occupancy(d, n=3.0), "blocked": B.with_antagonist(d, 9.0),
            "shift": 10.0, "at_kd": float(B.occupancy(1.0)), "at_9kd": float(B.occupancy(9.0)),
            "t": t, "first": B.first_order(t, 1.0, 5.0), "zero": B.zero_order(t, 1.0, 0.15), "half_life": 5.0,
            "caf_t": caf["t"][sel], "caf": caf["level"][sel], "one": one["level"][sel], "caf_peak": float(caf["level"].max()),
            "caf_at_23": at(caf["level"], 23.0), "one_at_23": at(one["level"], 23.0),
            "caf_share_at_23": at(caf["level"], 23.0) / float(caf["level"].max())}


def compute_tolerance() -> dict:
    s = archive.SIEGEL_1982.data
    o = B.opponent(doses=10)
    first = B.opponent(doses=1, hours=24.0)
    model = B.conditioned_tolerance(1.6, 0.75, 0.45, rng=rng(1000))
    sel = slice(None, None, 10)
    return {"t": o["t"][sel], "a": o["a"][sel], "b": o["b"][sel], "net": o["net"][sel], "felt": o["felt"],
            "troughs": o["troughs"], "first_t": first["t"][sel], "first_net": first["net"][sel],
            "felt_first": float(o["felt"][0]), "felt_last": float(o["felt"][-1]),
            "after_first": float(o["troughs"][0]), "after_last": float(o["troughs"][-1]),
            "published": np.array([s["usual_place"], s["new_place"], s["no_history"]]),
            "model": np.array([model["usual"], model["new"], model["none"]])}


def compute_chrono() -> dict:
    people = [("early", 22.0, 6.0, 22.5, 7.0), ("middle", 23.5, 7.0, 0.5, 9.0), ("late", 1.0, 7.0, 3.0, 11.5)]
    out = {"names": [p[0] for p in people]}
    out["mid_work"] = np.array([B.midsleep(p[1], p[2]) for p in people])
    out["mid_free"] = np.array([B.midsleep(p[3], p[4]) for p in people])
    out["jetlag"] = np.array([B.social_jetlag(*p[1:]) for p in people])
    out["sleep_work"] = np.array([(p[2] - p[1]) % 24 for p in people])
    out["sleep_free"] = np.array([(p[4] - p[3]) % 24 for p in people])
    return out


ITEMS = {
    "clock": compute_clock,
    "light": compute_light,
    "sleep": compute_sleep,
    "alert": compute_alert,
    "debt": compute_debt,
    "stress": compute_stress,
    "dose": compute_dose,
    "tolerance": compute_tolerance,
    "chrono": compute_chrono,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
