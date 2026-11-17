"""Precompute every number in Part 5 of *Psychology, Built* ("The Neuron").

    python -m videos.psychology.psych5.compute            # everything missing (about a minute)
    python -m videos.psychology.psych5.compute --force spike

Results are cached in ``.cache/psych5/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Everything is
computed by Psyche's neuron (``explainer.psychology.psyche.neuron``) from published equations; the published
numbers it is set beside come from the Archive.  Every random choice is seeded.

Items:
    ions         Nernst potentials of the squid axon's ions, the slope per tenfold change of concentration, and
                 the Goldman voltage as the sodium permeability is raised from rest to the peak of the spike
    rc           the membrane as a circuit: the charging curve of a leaky capacitor beside the model membrane's
                 response to small currents; its resistance and time constant at rest
    clamp        the voltage clamp: sodium and potassium conductances in time for a family of voltage steps,
                 and the currents they carry
    gates        the steady values and time constants of the gates m, h and n against voltage
    spike        one action potential with its gates, conductances and currents; the threshold; all-or-none;
                 the refractory period; the rate under a steady current
    cable        the action potential travelling along the axon of the 1952 paper: frames, the speed, the speed
                 against radius, and the passive length constant
    fhn          FitzHugh-Nagumo: nullclines, the rest state, trajectories below and above threshold, repetitive
                 firing; and two ways of starting to fire (rate against current for Hodgkin-Huxley and for the
                 integrate-and-fire neuron)
    lif          integrate-and-fire: traces, the closed-form rate against simulation, and the same current given
                 to the full model
    codes        spike trains: rasters at several rates, the spread of counts, the Fano factor with and without
                 a dead time, a rate code for a stretch receptor, and the trains of the on-you exercise
    dendrites    coincidence detection against the delay between two inputs; a neuron with two thresholding
                 branches against every point neuron
"""

from __future__ import annotations

import itertools
import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import archive
from explainer.psychology.psyche import neuron as N

CACHE = Cache("psych5")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def compute_ions() -> dict:
    temp = 6.3
    e = {ion: N.nernst(*N.SQUID[ion], z=(-1 if ion == "Cl" else 1), temp_c=temp) for ion in N.SQUID}
    ratio = np.logspace(-2, 2, 81)  # P_Na / P_K
    return {
        "temp_c": temp, "rt_f": N.thermal_voltage(temp), "conc": {k: list(v) for k, v in N.SQUID.items()},
        "nernst": e, "slope_20c": N.thermal_voltage(20.0) * math.log(10), "slope_37c": N.thermal_voltage(37.0) * math.log(10),
        "ratio": ratio, "goldman": np.array([N.goldman(1.0, r, 0.0) for r in ratio]),
        "rest_ratio": 0.04, "rest_v": N.goldman(1.0, 0.04, 0.0), "peak_ratio": 20.0, "peak_v": N.goldman(1.0, 20.0, 0.0),
        # the K potential as the outside concentration is changed (the classic test of the Nernst equation)
        "k_out": np.logspace(0, math.log10(400), 60),
        "e_k_curve": np.array([N.nernst(c, 400.0, temp_c=temp) for c in np.logspace(0, math.log10(400), 60)]),
    }


def compute_rc() -> dict:
    hh = N.HH()
    s = N.steady(hh.rest)
    g_rest = hh.g_na * s["m"] ** 3 * s["h"] + hh.g_k * s["n"] ** 4 + hh.g_l  # mS/cm^2
    r_rest = 1 / g_rest  # kilohm cm^2, so that uA/cm^2 gives mV
    tau = hh.c / g_rest  # ms
    t = np.arange(0, 12.001, 0.02)
    amp = 0.5  # uA/cm^2: far below threshold
    resp = hh.simulate(lambda x: amp if x >= 1 else 0.0, 13.0, dt=0.02)
    return {"g_rest": g_rest, "r_rest": r_rest, "tau": tau, "amp": amp, "t": t,
            "rc": N.rc_step(t, amp, r_rest, hh.c), "hh_t": resp["t"] - 1.0, "hh": resp["v"] - hh.rest,
            "taus": [0.5 * tau, tau, 2 * tau],
            "family": np.array([N.rc_step(t, amp, r_rest * k, hh.c) for k in (0.5, 1.0, 2.0)])}


def compute_clamp() -> dict:
    hh = N.HH()
    steps = [-40.0, -20.0, 0.0, 20.0, 40.0]
    out = {"steps": steps, "rest": hh.rest}
    for v in steps:
        c = hh.clamp(v, 8.0, dt=0.02)
        out[f"g_na_{int(v)}"], out[f"g_k_{int(v)}"] = c["g_na"], c["g_k"]
        out[f"i_{int(v)}"] = c["i_na"] + c["i_k"] + hh.g_l * (v - hh.e_l)
        out[f"i_na_{int(v)}"], out[f"i_k_{int(v)}"] = c["i_na"], c["i_k"]
    out["t"] = c["t"]
    c0 = hh.clamp(0.0, 8.0, dt=0.02)
    out["peak_g_na_0"], out["t_peak_na_0"] = float(c0["g_na"].max()), float(c0["t"][c0["g_na"].argmax()])
    out["final_g_k_0"] = float(c0["g_k"][-1])
    out["half_g_k_0"] = float(c0["t"][np.argmax(c0["g_k"] >= c0["g_k"][-1] / 2)])
    return out


def compute_gates() -> dict:
    v = np.linspace(-100, 50, 301)
    s = N.steady(v)
    r = N.steady(N.HH().rest)
    return {"v": v, **{k: s[k] for k in ("m", "h", "n", "tau_m", "tau_h", "tau_n")},
            "rest": {k: float(r[k]) for k in ("m", "h", "n", "tau_m", "tau_h", "tau_n")}}


def compute_spike() -> dict:
    hh = N.HH()
    th = hh.threshold(0.5)
    r = hh.pulse(2 * th, 0.5, 18.0)
    amps = np.array([0.5, 0.8, 0.95, 1.05, 1.5, 2.0, 3.0]) * th
    family = [hh.pulse(a, 0.5, 12.0) for a in amps]
    delays = np.array([2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0])
    second = hh.refractory(delays)
    currents = np.arange(0.0, 30.01, 1.0)
    fine = np.arange(5.5, 7.01, 0.1)
    rate = np.array([hh.firing_rate(c) for c in currents])
    rate_fine = np.array([hh.firing_rate(c) for c in fine])
    onset = float(fine[np.argmax(rate_fine > 0)])
    train = hh.simulate(10.0, 100.0, dt=0.02)
    peak_i = int(r["v"].argmax())
    return {
        "rest": hh.rest, "threshold": th, "t": r["t"], "v": r["v"], "m": r["m"], "h": r["h"], "n": r["n"],
        "g_na": r["g_na"], "g_k": r["g_k"], "i_na": r["i_na"], "i_k": r["i_k"],
        "peak": float(r["v"].max()), "t_peak": float(r["t"][peak_i]), "trough": float(r["v"].min()),
        "amplitude": float(np.ptp(r["v"])), "e_na": hh.e_na, "e_k": hh.e_k,
        "width": float((r["v"] > (r["v"].max() + hh.rest) / 2).sum() * (r["t"][1] - r["t"][0])),
        "amps": amps, "family_t": family[0]["t"], "family": np.array([f["v"] for f in family]),
        "family_peaks": np.array([f["v"].max() for f in family]),
        "delays": delays, "second": np.where(np.isinf(second), np.nan, second),
        "absolute": float(delays[np.isinf(second)].max()) if np.isinf(second).any() else 0.0,
        "currents": currents, "rate": rate, "onset": onset, "rate_at_onset": float(rate_fine[rate_fine > 0][0]),
        "rate_10": float(hh.firing_rate(10.0)), "train_t": train["t"], "train_v": train["v"],
    }


def compute_cable() -> dict:
    hh_d = archive.HODGKIN_HUXLEY_1952.data
    a = hh_d["radius_um"] * 1e-4
    p = N.propagate(radius_cm=a, r_i=hh_d["resistivity_ohm_cm"])
    radii = np.array([0.25, 0.5, 1.0, 2.0, 4.0]) * a
    speeds = np.array([N.propagate(radius_cm=r, r_i=hh_d["resistivity_ohm_cm"],
                                   length_cm=6.0 * math.sqrt(r / a) + 1.0)["velocity"] for r in radii])
    lam = N.length_constant(a, 1 / (N.HH().g_l * 1e-3), hh_d["resistivity_ohm_cm"])
    x = np.linspace(0, 4, 81)
    keep = np.linspace(0, len(p["t"]) - 1, 120).astype(int)
    return {"x": p["x"], "t": p["t"][keep], "v": p["v"][keep], "velocity": p["velocity"],
            "published": hh_d["velocity_computed"], "observed": hh_d["velocity_observed"],
            "temp_c": hh_d["velocity_temp_c"], "radius_um": hh_d["radius_um"],
            "radii_um": radii * 1e4, "speeds": speeds,
            "sqrt_fit": float(np.polyfit(np.log(radii), np.log(speeds), 1)[0]),
            "lambda_cm": lam, "passive_x": x, "passive": np.exp(-x / lam),
            "helmholtz": list(archive.HELMHOLTZ_1850.data["speed_frog"])}


def compute_fhn() -> dict:
    f = N.FHN()
    v = np.linspace(-2.4, 2.4, 241)
    nv0, nw = f.nullclines(v, 0.0)
    nv1, _ = f.nullclines(v, 0.5)
    rest = f.fixed_point(0.0)
    below = f.simulate(0.0, 60.0, v0=(-0.9, rest[1]))
    above = f.simulate(0.0, 60.0, v0=(-0.5, rest[1]))
    firing = f.simulate(0.5, 200.0)
    currents = np.linspace(0.0, 1.6, 81)
    amp = np.array([np.ptp(f.simulate(c, 600.0, dt=0.1)["v"][3000:]) for c in currents])
    on = currents[amp > 1.0]
    # two ways to start firing: the full model jumps to a finite rate, the integrator starts from zero
    hh, lif = N.HH(), N.LIF()
    i_hh = np.arange(0.0, 20.01, 0.25)
    r_hh = np.array([hh.firing_rate(c) for c in i_hh])
    i_lif = np.linspace(0.0, 4.0, 161)
    return {"v": v, "null_v_0": nv0, "null_v_1": nv1, "null_w": nw, "rest": list(rest),
            "below_v": below["v"], "below_w": below["w"], "above_v": above["v"], "above_w": above["w"],
            "t": below["t"], "firing_t": firing["t"], "firing_v": firing["v"], "firing_w": firing["w"],
            "currents": currents, "amplitude": amp, "on": [float(on.min()), float(on.max())],
            "a": f.a, "b": f.b, "eps": f.eps,
            "i_hh": i_hh, "r_hh": r_hh, "hh_onset": float(i_hh[np.argmax(r_hh > 0)]),
            "hh_first_rate": float(r_hh[r_hh > 0][0]),
            "i_lif": i_lif, "r_lif": lif.rate(i_lif), "lif_rheobase": lif.rheobase}


def compute_lif() -> dict:
    lif = N.LIF()
    trace = lif.simulate(2.0, 120.0)
    currents = np.array([1.6, 1.8, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0])
    sim = np.array([1000 / np.diff(lif.simulate(c, 3000.0)["spikes"]).mean() for c in currents])
    fine = np.linspace(0, 8.5, 341)
    noisy = lif.simulate(1.4, 400.0, noise=1.2, rng=rng(51))  # below rheobase, fires on the noise
    return {"tau": lif.tau, "r": lif.resistance, "e_l": lif.e_l, "v_th": lif.v_th, "t_ref": lif.t_ref,
            "rheobase": lif.rheobase, "t": trace["t"], "v": trace["v"], "spikes": trace["spikes"],
            "currents": currents, "simulated": sim, "closed": lif.rate(currents), "fine": fine,
            "curve": lif.rate(fine), "ceiling": 1000 / lif.t_ref,
            "noisy_t": noisy["t"][::5], "noisy_v": noisy["v"][::5], "noisy_spikes": noisy["spikes"]}


def compute_codes() -> dict:
    g = rng(52)
    rates = [5.0, 20.0, 60.0]
    rasters = {f"r{int(r)}": [N.poisson_train(r, 1.0, g).tolist() for _ in range(8)] for r in rates}
    c = N.counts(20.0, 1.0, 2000, g)
    cr = N.counts(20.0, 1.0, 2000, g, refractory=0.03)
    edges = np.arange(-0.5, 45.5, 1.0)
    stretch = np.logspace(-1.3, 1.2, 60)
    # the on-you exercise: three trains of one second; which stimulus was strongest?
    order = [35.0, 12.0, 70.0]
    quiz = [N.poisson_train(r, 1.0, g, refractory=0.004).tolist() for r in order]
    # how well can a count over a window tell 20 from 30 spikes a second?
    windows = np.array([0.05, 0.1, 0.2, 0.5, 1.0, 2.0])
    correct = []
    for w in windows:
        a_, b_ = g.poisson(20 * w, 20000), g.poisson(30 * w, 20000)
        correct.append(float(np.mean(b_ > a_) + 0.5 * np.mean(b_ == a_)))
    return {"rates": rates, "rasters": rasters, "edges": edges,
            "hist": np.histogram(c, edges)[0] / len(c), "hist_ref": np.histogram(cr, edges)[0] / len(cr),
            "mean": float(c.mean()), "fano": N.fano(c), "mean_ref": float(cr.mean()), "fano_ref": N.fano(cr),
            "stretch": stretch, "adrian": N.adrian(stretch), "quiz_rates": order, "quiz": quiz,
            "quiz_counts": [len(q) for q in quiz], "windows": windows, "correct": np.array(correct)}


def compute_dendrites() -> dict:
    lif = N.LIF()
    delays = np.arange(0.0, 12.01, 0.25)
    fires = np.array([lif.coincidence(float(d)) for d in delays])
    window = float(delays[fires].max())
    one = lif.simulate(lambda t: 11.0 / lif.resistance * lif.tau * math.exp(-(t - 5)) * (t >= 5), 40.0, dt=0.02)
    x = np.array(list(itertools.product((0, 1), repeat=4)))
    y = N.dendritic_neuron(x, [(0, 1), (2, 3)], branch_threshold=2)
    any_two = (x.sum(axis=1) >= 2).astype(int)
    xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    return {"delays": delays, "fires": fires.astype(int), "window": window,
            "epsp_peak": float(one["v"].max() - lif.e_l), "gap": lif.v_th - lif.e_l,
            "x": x, "y": y, "any_two": any_two, "separable": N.separable(x, y),
            "separable_any_two": N.separable(x, any_two), "xor_separable": N.separable(xor, [0, 1, 1, 0]),
            "fires_on": int(y.sum())}


ITEMS = {
    "ions": compute_ions,
    "rc": compute_rc,
    "clamp": compute_clamp,
    "gates": compute_gates,
    "spike": compute_spike,
    "cable": compute_cable,
    "fhn": compute_fhn,
    "lif": compute_lif,
    "codes": compute_codes,
    "dendrites": compute_dendrites,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
