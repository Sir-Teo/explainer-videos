"""Precompute every number in Part 6 of *Psychology, Built* ("Synapses and Circuits").

    python -m videos.psychology.psych6.compute            # everything missing (about a minute), into .cache/psych6/
    python -m videos.psychology.psych6.compute --force lateral

Results are cached in ``.cache/psych6/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Everything is
computed by Psyche's circuits (``explainer.psychology.psyche.circuits``); the published findings it is set beside
come from the Archive.  Every random choice is seeded.

Items:
    quanta       transmitter released in packets: 2,000 responses of a synapse with five release sites, each
                 releasing one packet with probability 0.3; the histogram's peaks at whole numbers of packets
    integration  one EPSP and one IPSP; two EPSPs together and apart; the peak against the interval between two
                 inputs and against the number arriving at once; shunting inhibition against hyperpolarizing
                 inhibition (division against subtraction)
    hebb         a cloud of correlated inputs; a linear unit trained by Hebb's rule (it diverges) and by Oja's
                 rule (it settles on the first principal component)
    plasticity   the spike-timing window; a BCM unit becoming selective to one of two patterns, with its
                 sliding threshold
    lateral      a row of units with lateral inhibition, shown a step and a ramp of light: Mach bands; the
                 kernel; a uniform field for comparison
    hermann      the Hermann grid and Geier's curved grid under a centre-surround filter: the response at a
                 crossing and along a street in each
    wta          a pair of units with mutual inhibition: who wins, a choice held after the evidence has gone,
                 the same pair without its loop, and the time to decide against the size of the difference
    rhythm       a half-centre oscillator: the two outputs and their fatigue; the period against the time
                 constant of fatigue; the same pair with too little inhibition
    populations  Wilson and Cowan's excitatory and inhibitory populations: rest, a rhythm, saturation, and the
                 range of the excitatory activity and the frequency against the drive
    knobs        a neuromodulator as a gain on a unit's response curve, and as a learning rate for Oja's rule
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import circuits as C

CACHE = Cache("psych6")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def compute_quanta() -> dict:
    g = rng(60)
    sites, p, q, sd, trials = 5, 0.3, 0.4, 0.07, 2000
    k = g.binomial(sites, p, trials)
    size = k * q + sd * np.sqrt(np.maximum(k, 0.15)) * g.standard_normal(trials)
    edges = np.linspace(-0.3, 2.3, 66)
    counts = np.bincount(k, minlength=sites + 1) / trials
    return {"sites": sites, "p": p, "q": q, "trials": trials, "edges": edges,
            "hist": np.histogram(size, edges)[0] / trials, "share": counts, "failures": float(counts[0]),
            "expected_failures": float((1 - p) ** sites), "mean": float(size.mean()), "example": size[:60]}


def compute_integration() -> dict:
    m = C.Membrane()
    one = m.response(exc=[5.0])
    ipsp = m.response(inh=[5.0])
    together = m.response(exc=[5.0, 5.0])
    close = m.response(exc=[5.0, 8.0])
    apart = m.response(exc=[5.0, 35.0])
    gaps = np.arange(0.0, 40.01, 1.0)
    peak_gap = np.array([m.response(exc=[5.0, 5.0 + g], t_end=90.0)["peak"] for g in gaps])
    counts = np.arange(1, 13)
    peak_n = np.array([m.response(exc=[5.0] * int(k))["peak"] for k in counts])
    # steady conductances: excitation alone, with a shunt (E_I at rest), with hyperpolarizing inhibition
    ge = np.linspace(0.0, 0.3, 61)
    alone = np.array([m.steady_voltage(g) - m.e_l for g in ge])
    shunt = np.array([m.steady_voltage(g, 0.15, e_i=m.e_l) - m.e_l for g in ge])
    hyper = np.array([m.steady_voltage(g, 0.05) - m.e_l for g in ge])
    k = int(np.argmin(np.abs(ge - 0.05)))
    return {"tau": m.tau, "e_l": m.e_l, "t": one["t"], "one": one["v"], "ipsp": ipsp["v"], "together": together["v"],
            "close": close["v"], "apart": apart["v"], "peak_one": one["peak"], "peak_together": together["peak"],
            "peak_close": close["peak"], "peak_apart": apart["peak"], "trough_ipsp": ipsp["trough"],
            "gaps": gaps, "peak_gap": peak_gap, "counts": counts, "peak_n": peak_n, "linear_n": one["peak"] * counts,
            "ge": ge, "alone": alone, "shunt": shunt, "hyper": hyper, "g_shunt": 0.15,
            "ratio_small": float(shunt[k] / alone[k]), "ratio_large": float(shunt[-1] / alone[-1]),
            "to_threshold": 15.0, "needed": int(counts[np.argmax(peak_n >= 15.0)]) if (peak_n >= 15.0).any() else 0}


def compute_hebb() -> dict:
    g = rng(61)
    x = g.standard_normal((4000, 2)) @ np.array([[2.0, 0.0], [1.2, 0.5]])
    h = C.hebb(x, eta=0.01, rule="hebb", rng=rng(62))
    o = C.hebb(x, eta=0.01, rule="oja", rng=rng(62))
    vals = np.linalg.eigvalsh(x.T @ x / len(x))
    stop = int(np.argmax(h["norm"] > 50)) or len(h["norm"])
    return {"cloud": x[:400], "pc": o["pc"] * np.sign(o["pc"] @ o["w"]), "share": float(vals[-1] / vals.sum()),
            "hebb_norm": h["norm"][:stop], "hebb_path": h["path"][:stop:max(1, stop // 150)],
            "hebb_steps_to_50": stop, "hebb_cosine": float(h["cosine"][min(stop, len(h["cosine"]) - 1)]),
            "oja_norm": o["norm"], "oja_cosine": o["cosine"], "oja_path": o["path"][::20], "oja_w": o["w"],
            "oja_final_norm": float(np.linalg.norm(o["w"])), "oja_final_cosine": float(o["cosine"][-200:].mean())}


def compute_plasticity() -> dict:
    dt = np.linspace(-100, 100, 401)
    b = C.bcm([[1.0, 0.2], [0.2, 1.0]], eta=0.005, rng=rng(63))
    first = int(np.argmax(b["final"]))
    late = slice(3 * len(b["theta"]) // 4, None)
    # with two patterns shown equally often, the selective fixed point has theta = y^2 / 2 = y, so y = 2
    return {"dt": dt, "stdp": C.stdp(dt), "window": 20, "at_plus_10": float(C.stdp(10.0)), "at_minus_10": float(C.stdp(-10.0)),
            "bcm_steps": np.arange(len(b["theta"])) * 50, "bcm_pref": b["response"][:, first],
            "bcm_other": b["response"][:, 1 - first], "bcm_theta": b["theta"],
            "bcm_start": b["response"][0], "bcm_late_pref": float(b["response"][late, first].mean()),
            "bcm_late_other": float(b["response"][late, 1 - first].mean()),
            "bcm_late_theta": float(b["theta"][late].mean()), "bcm_predicted": 2.0}


def compute_lateral() -> dict:
    n = 80
    step = np.r_[np.full(n // 2, 1.0), np.full(n // 2, 2.0)]
    foot, top = 35, 45
    ramp = np.r_[np.full(foot, 1.0), np.linspace(1.0, 2.0, top - foot), np.full(n - top, 2.0)]
    flat = np.full(n, 1.5)
    r_step, r_ramp, r_flat = C.lateral(step), C.lateral(ramp), C.lateral(flat)
    k = C.inhibition_kernel(n)[n // 2]
    low, high = float(r_step[15:25].mean()), float(r_step[55:65].mean())
    return {"x": np.arange(n), "step": step, "ramp": ramp, "flat": flat, "r_step": r_step, "r_ramp": r_ramp,
            "r_flat": r_flat, "kernel_x": np.arange(n) - n // 2, "kernel": k, "low": low, "high": high,
            "dark_band": float(r_step[n // 2 - 6:n // 2].min()), "bright_band": float(r_step[n // 2:n // 2 + 6].max()),
            "contrast_in": 2.0, "contrast_out": high / low, "foot": foot, "top": top,
            "ramp_dip": float(r_ramp[foot - 6:foot + 4].min()), "ramp_peak": float(r_ramp[top - 4:top + 6].max()),
            "edge_out": float(r_step[n // 2:n // 2 + 6].max() / r_step[n // 2 - 6:n // 2].min())}


def compute_hermann() -> dict:
    straight, curved = C.hermann_response(), C.hermann_response(wave=4.0)
    return {"image": straight["image"], "filtered": straight["filtered"], "row": straight["row"], "at": straight["at"],
            "crossing": straight["crossing"], "street": straight["street"],
            "curved_image": curved["image"], "curved_filtered": curved["filtered"],
            "curved_crossing": curved["crossing"], "curved_street": curved["street"], "wave": 4.0, "street_px": 10}


def compute_wta() -> dict:
    w = C.WTA()
    a, b = w.simulate((1.2, 1.0)), w.simulate((1.0, 1.2))

    def then_equal(t):
        return (1.2, 1.0) if t < 150 else (1.1, 1.1)

    held = w.simulate(then_equal)
    loose = C.WTA(w_self=0.0, w_cross=0.5).simulate(then_equal)
    diffs = np.array([0.02, 0.05, 0.1, 0.2, 0.4, 0.8])
    times = []
    for d in diffs:
        s = w.simulate((1.1 + d / 2, 1.1 - d / 2), t_end=3000.0)
        gap = np.abs(s["r"][:, 0] - s["r"][:, 1])
        times.append(float(s["t"][np.argmax(gap > 0.5)]) if (gap > 0.5).any() else float("nan"))
    keep = slice(None, None, 4)
    return {"t": a["t"][keep], "a": a["r"][keep], "b": b["r"][keep], "held": held["r"][keep], "loose": loose["r"][keep],
            "switch": 150.0, "held_margin": held["margin"], "loose_margin": loose["margin"], "diffs": diffs,
            "times": np.array(times)}


def compute_rhythm() -> dict:
    h = C.HalfCentre()
    s = h.simulate()
    quiet = C.HalfCentre(a=0.8).simulate()
    fat = np.array([100.0, 200.0, 300.0, 450.0, 600.0, 900.0])
    periods = np.array([C.HalfCentre(t_fatigue=f).simulate(t_end=8000.0)["period"] for f in fat])
    keep = slice(None, None, 8)
    return {"t": s["t"][keep], "y": s["y"][keep], "fatigue": s["fatigue"][keep], "period": s["period"],
            "correlation": s["correlation"], "quiet": quiet["y"][keep], "a": h.a, "beta": h.beta,
            "lo": 1 + h.tau / h.t_fatigue, "hi": 1 + h.beta, "fatigues": fat, "periods": periods}


def compute_populations() -> dict:
    wc = C.WilsonCowan()
    rest, osc, sat = wc.simulate(0.0), wc.simulate(1.25), wc.simulate(3.5)
    drives = np.linspace(0.0, 4.0, 81)
    amp, freq, lo, hi = [], [], [], []
    for p in drives:
        s = wc.simulate(float(p))
        late = s["e"][len(s["e"]) // 2:]
        amp.append(s["amplitude"])
        freq.append(s["frequency"])
        lo.append(float(late.min()))
        hi.append(float(late.max()))
    amp, freq = np.array(amp), np.array(freq)
    on = drives[amp > 0.05]
    keep = slice(None, None, 10)
    return {"t": rest["t"][keep], "rest_e": rest["e"][keep], "osc_e": osc["e"][keep], "osc_i": osc["i"][keep],
            "sat_e": sat["e"][keep], "frequency": osc["frequency"], "amplitude": osc["amplitude"], "drives": drives,
            "amp": amp, "freq": freq, "e_lo": np.array(lo), "e_hi": np.array(hi),
            "onset": float(on.min()), "offset": float(on.max()), "freq_max": float(freq.max()),
            "freq_onset": float(freq[amp > 0.05][0]), "sat_level": float(sat["e"][-1])}


def compute_knobs() -> dict:
    x = np.linspace(-2, 8, 201)
    gains = [0.5, 1.0, 2.0]
    curves = np.array([C.sigmoid(x, g, 3.0) for g in gains])
    g = rng(64)
    data = g.standard_normal((3000, 2)) @ np.array([[2.0, 0.0], [1.2, 0.5]])
    slow = C.hebb(data, eta=0.002, rule="oja", rng=rng(65))
    fast = C.hebb(data, eta=0.05, rule="oja", rng=rng(65))
    return {"x": x, "gains": gains, "curves": curves, "slow": slow["cosine"], "fast": fast["cosine"],
            "slow_eta": 0.002, "fast_eta": 0.05,
            "slow_steps": int(np.argmax(slow["cosine"] > 0.99)), "fast_steps": int(np.argmax(fast["cosine"] > 0.99)),
            "slow_wobble": float(1 - slow["cosine"][-500:].min()), "fast_wobble": float(1 - fast["cosine"][-500:].min())}


ITEMS = {
    "quanta": compute_quanta,
    "integration": compute_integration,
    "hebb": compute_hebb,
    "plasticity": compute_plasticity,
    "lateral": compute_lateral,
    "hermann": compute_hermann,
    "wta": compute_wta,
    "rhythm": compute_rhythm,
    "populations": compute_populations,
    "knobs": compute_knobs,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
