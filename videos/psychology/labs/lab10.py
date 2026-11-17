"""Lab 10: a clock that light can set, two processes that time sleep, a loop that switches itself off, and a dose."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import body as B

TITLE = "A clock, a pressure, a brake and a dose: four small models of the body the brain lives in"
GOAL = ("Run Psyche's clock in darkness and on days of different lengths, and find which it can follow; measure "
        "what a pulse of light does at each hour and how long a flight's shift takes to make up; let the "
        "two-process model sleep, then keep it awake for forty hours and time the recovery; count lapses over two "
        "weeks of short sleep; stress the cortisol loop with its brake whole and worn; fill receptors with a drug, "
        "with and without a blocker; follow three coffees to bedtime; and give ten doses to an opponent process.")
TASKS = [
    "In entrain, raise the light from 300 to 3,000 lux and find the day lengths the clock now locks to. Why does "
    "brighter light widen the range, and what would that have meant for the lamps in Kleitman's cave?",
    "In two_process, keep the model awake for 16, 28, 40, 52 and 64 hours (keep_awake) and record the recovery "
    "sleep. Why does it not grow in proportion, and why is a sleep begun at eleven in the morning shorter than one "
    "begun at eleven at night?",
    "In dosing, move the last of the three coffees from 16:00 to 12:00 and find what is left at 23:00. Then halve "
    "and double the half-life. Which matters more for bedtime: when the last cup was, or whose liver it is?",
]


def run(seed=0):
    out = labs.Lab()
    c = B.Clock()

    # 1. the clock
    free = B.free_running_period(c)
    home = B.entrain(c)
    out.row("the clock's own period, in darkness (published for people: 24.18 h)", f"{free:.2f} h")
    out.row("on a 24-hour day with 16 h of room light: period; low point", f"{home['period']:.1f} h; "
            f"{int(home['minimum_at'])}:{int(round(60 * (home['minimum_at'] % 1))):02d}")
    locked = [d for d in (22, 23, 24, 25, 26, 28) if B.entrain(c, day=float(d))["locked"]]
    cave = B.entrain(c, day=28.0, lux=40.0)
    out.row("day lengths the clock locks to, of 22, 23, 24, 25, 26 and 28 h", ", ".join(str(d) for d in locked))
    out.row("its period on the cave's 28-hour day (Kleitman's stayed near 24)", f"{cave['period']:.1f} h")
    assert abs(free - 24.18) < 0.1 and locked == [23, 24, 25] and not cave["locked"]

    # 2. light
    p = B.phase_response(c, steps=12)
    out.row("three hours of bright light: largest delay; largest advance", f"{p['shift'].min():+.1f} h; {p['shift'].max():+.1f} h")
    before = p["shift"][p["hours_from_minimum"] < -1].mean()
    after = p["shift"][(p["hours_from_minimum"] > 0.5) & (p["hours_from_minimum"] < 6)].mean()
    out.row("average shift for light before the low point; in the six hours after it", f"{before:+.2f} h; {after:+.2f} h")
    j = B.jet_lag(6, c)
    out.row("six time zones: hours wrong on days 0, 2, 4; days to come within an hour",
            f"{abs(j['hours_off'][0]):.1f}, {abs(j['hours_off'][2]):.1f}, {abs(j['hours_off'][4]):.1f}; {j['days_to_adjust']:.0f}")
    assert before < 0 < after and 2 <= j["days_to_adjust"] <= 9

    # 3. two processes
    r = B.two_process(hours=144.0, s0=0.5)
    usual = float(np.mean([e - s for s, e in r["episodes"][2:]]))
    lost = B.two_process(hours=144.0, s0=0.5, keep_awake=[(40.0, 71.0)])
    recovery = [e - s for s, e in lost["episodes"] if s >= 70.9][0]
    out.row("the model's ordinary night: asleep, awake, hours", f"{r['episodes'][3][0] % 24:.1f} h, {r['episodes'][3][1] % 24:.1f} h, {usual:.1f}")
    out.row("after 40 hours awake: the pressure reached; the recovery sleep", f"{lost['S'].max():.2f}; {recovery:.1f} h")
    al = B.alertness(lost["t"], lost["S"])
    night = (lost["t"] >= 31) & (lost["t"] < 71)
    low = float(lost["t"][night][al[night].argmin()] % 24)
    at = lambda h: float(al[np.argmin(np.abs(lost["t"] - h))])  # noqa: E731
    out.row("a night awake: alertness lowest at; at dawn against 15:00 the next day", f"{low:.1f} h; {at(48 + low):.2f} against {at(63.0):.2f}")
    assert 7.5 < usual < 8.6 and recovery < usual + 1.5 and at(63.0) > at(48 + low)

    # 4. sleep loss
    six, four = B.lapses(6.0, 14), B.lapses(4.0, 14)
    out.row("lapses after 14 days on 8, 6 and 4 hours in bed (the scale is arbitrary)",
            f"{B.lapses(8.0, 14)[-1]:.1f}, {six[-1]:.1f}, {four[-1]:.1f}")
    out.row("sleep that keeps the count level", f"{24 - 15.84:.2f} h")
    assert abs((four[-1] - 1) / (six[-1] - 1) - (20 - 15.84) / (18 - 15.84)) < 1e-6

    # 5. the stress loop
    base, hit = B.hpa(hours=96.0), B.hpa(hours=96.0, stress=[(58.0, 1.0, 3.0)])
    worn0, worn = B.hpa(hours=96.0, feedback=0.3), B.hpa(hours=96.0, feedback=0.3, stress=[(58.0, 1.0, 3.0)])
    day = (base["t"] >= 48) & (base["t"] < 72)
    extra, extra_w = hit["cortisol"] - base["cortisol"], worn["cortisol"] - worn0["cortisol"]
    gone = lambda e: float(base["t"][np.where(e > 0.1 * e.max())[0][-1]] - 59.0)  # noqa: E731
    out.row("cortisol's daily peak; its swing", f"{base['t'][day][base['cortisol'][day].argmax()] % 24:.1f} h; "
            f"{base['cortisol'][day].max() / base['cortisol'][day].min():.1f}-fold")
    out.row("a one-hour stressor: the rise; hours after its end to come back", f"{extra.max():.2f}; {gone(extra):.1f}")
    out.row("the same with the brake at 30%: the rise; hours; the daily level", f"{extra_w.max():.2f}; {gone(extra_w):.1f}; "
            f"{100 * (worn0['cortisol'][day].mean() / base['cortisol'][day].mean() - 1):+.0f}%")
    assert extra_w.max() > extra.max() and gone(extra_w) > gone(extra)

    # 6. dose and response
    out.row("receptors occupied at K, 9K and 99K", ", ".join(f"{100 * B.occupancy(k):.0f}%" for k in (1.0, 9.0, 99.0)))
    d80 = 4.0  # p = D / (D + K) = 0.8 at D = 4 K
    out.row("dose for 80%: alone; with a blocker at four times its own K", f"{d80:.0f} K; {d80 * 5:.0f} K")
    out.row("... and the occupancy that dose of 4 K gives once the blocker is there", f"{100 * B.with_antagonist(d80, 4.0):.0f}%")
    out.row("dose ratio from 10% to 90% of the effect: one site; three sites", f"{81:.0f}-fold; {81 ** (1 / 3):.1f}-fold")
    caf = B.dosing([8.0, 13.0, 16.0], hours=48.0, half_life=5.0)
    one = B.dosing([8.0], hours=48.0, half_life=5.0)
    at23 = lambda d: float(d["level"][np.searchsorted(d["t"], 23.0)])  # noqa: E731
    out.row("three coffees (8:00, 13:00, 16:00): the peak; left at 23:00; with the first only", f"{caf['level'].max():.2f}; "
            f"{at23(caf):.2f}; {at23(one):.2f} cups")
    t = np.array([0.0, 2.0, 4.0, 6.0, 8.0])
    out.row("a dose after 0, 2, 4, 6, 8 h: a half-life of 5 h; a constant 0.15 an hour",
            ", ".join(f"{v:.2f}" for v in B.first_order(t, 1.0, 5.0)) + "; " + ", ".join(f"{v:.2f}" for v in B.zero_order(t, 1.0, 0.15)))
    assert abs(B.occupancy(9.0) - 0.9) < 1e-9 and abs(B.with_antagonist(20.0, 4.0) - 0.8) < 1e-9 and at23(caf) > 4 * at23(one)

    # 7. the body answers back
    o = B.opponent(doses=10)
    out.row("ten daily doses: the effect felt, first and tenth; the low afterwards, first and tenth",
            f"{o['felt'][0]:.2f}, {o['felt'][-1]:.2f}; {o['troughs'][0]:.2f}, {o['troughs'][-1]:.2f}")
    m = B.conditioned_tolerance(1.6, 0.75, 0.45, rng=np.random.default_rng(seed + 1))
    out.row("deaths from one large dose: usual room, new room, no history (published: 32, 64, 96%)",
            f"{100 * m['usual']:.0f}%, {100 * m['new']:.0f}%, {100 * m['none']:.0f}%")
    out.row("social jetlag of a sleeper on 1:00 to 7:00 at work and 3:00 to 11:30 when free", f"{B.social_jetlag(1.0, 7.0, 3.0, 11.5):.2f} h")
    assert o["felt"][-1] < 0.5 * o["felt"][0] and o["troughs"][-1] < 2 * o["troughs"][0] and m["usual"] < m["new"] < m["none"]
    out.note = ("The clock keeps its own time, a little slow, and follows days of 23 to 25 hours but not the cave's "
                "28. Light before its low point moves it later and light after moves it earlier, and a shift of six "
                "hours takes days to make up. A pressure that rises over 18 hours and falls over 4, gated by the "
                "clock, gives an eight-hour night and a recovery sleep only a little longer after a lost night, "
                "with alertness coming back the next afternoon before any sleep. Lapses add up with every hour "
                "awake beyond about sixteen. A loop whose product shuts off its source returns to rest after a "
                "stressor, and more slowly with its brake worn. Occupancy follows D/(D+K); a blocker multiplies K. "
                "Three coffees leave most of a cup at bedtime. An opponent process that strengthens with use turns "
                "a lift into a debt.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    k = (lost["t"] >= 24) & (lost["t"] <= 120)
    ax[0].plot(lost["t"][k] / 24, lost["S"][k], color=labs.BLUE, lw=1.8, label="sleep pressure")
    ax[0].plot(lost["t"][k] / 24, lost["upper"][k], color=labs.GREY, lw=1.0, label="the clock's thresholds")
    ax[0].plot(lost["t"][k] / 24, lost["lower"][k], color=labs.GREY, lw=1.0)
    ax[0].set(title="Forty hours awake, then recovery", xlabel="days", ylabel="pressure")
    ax[0].legend(loc="upper right", fontsize=8)
    kk = (caf["t"] >= 6) & (caf["t"] <= 30)
    ax[1].plot(caf["t"][kk], caf["level"][kk], color=labs.GREEN, lw=1.8, label="coffee at 8, 13 and 16")
    ax[1].plot(one["t"][kk], one["level"][kk], color=labs.GREY, lw=1.4, label="at 8 only")
    ax[1].axvline(23, color=labs.PINK, lw=1.2, ls="--")
    ax[1].set(title="Caffeine through a day (half-life 5 h)", xlabel="clock hour", ylabel="cups in the body")
    ax[1].legend(loc="upper right", fontsize=8)
    out.fig = fig
    return out
