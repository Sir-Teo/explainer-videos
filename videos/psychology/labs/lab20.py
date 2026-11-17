"""Lab 20: Ebbinghaus's savings with three laws; serial position, first recall and the lag-CRP on the PEERS open data
(or, offline, on Psyche's context model); SAM's symmetric contiguity against CMR's forward lean; the context model's
exact likelihood, with a held-out comparison against serial position alone; Murre's divers with an exact sign-flip
test; a Hopfield network's capacity; and pattern separation by a sparse expansion."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import archive, opendata
from explainer.psychology.psyche import memory as M

TITLE = "Memory: forgetting, free recall, context, attractors"
GOAL = ("Fit three forgetting laws to Ebbinghaus's savings; measure serial position and contiguity on real free "
        "recall; see SAM's buffer give symmetric contiguity and a drifting context give a forward lean; score the "
        "context model's likelihood on held-out lists against serial position alone; redo the divers' test exactly; "
        "and find where a Hopfield network runs out of room.")
TASKS = [
    "Compute the lag-CRP of the sequence 16, 15, 14, 1, 2, 9 by hand, then check it with `memory.lag_crp`.",
    "Set `gamma_fc` to 0 and then to 0.9 in `memory.cmr_simulate`. What happens to the forward lean of the lag-CRP, "
    "and why?",
    "With Murre's per-diver effects, how many divers would a test need for 80% power to detect the 1975 effect of "
    "four words, at his spread?",
]

# CMR at the values Part 20 fitted to half of PEERS (videos/psychology/psych20, item `cmr`)
FITTED = {"B_enc": 0.9494, "B_rec": 0.916, "B_start": 0.0443, "gamma_fc": 0.1067, "phi_s": 8.5093, "phi_d": 1.5536,
          "tau": 1.1928, "stop_s": 0.0071, "stop_r": 0.2987}


def run(seed=0):
    out = labs.Lab()
    rng = np.random.default_rng(seed)

    # 1. Ebbinghaus
    e = archive.EBBINGHAUS_1885.data
    f = M.fit_forgetting(e["minutes"], e["saving"])
    for law in ("ebbinghaus", "power", "exponential"):
        out.row(f"{law} law: parameters, residual SS", ", ".join(f"{v:.3g}" for v in f[law]["params"])
                + f"; {f[law]['sse']:.1f}")
    assert f["power"]["sse"] < f["exponential"]["sse"]  # fast, then slow: not exponential

    # 2. free recall: the open data if it can be fetched, else the context model
    if opendata.available("peers_free_recall"):
        R = opendata.peers_free_recall()["recalls"]
        source = "PEERS (Kahana lab), as packaged with psifr"
    else:
        R = M.cmr_simulate(16, 3000, FITTED, rng)
        source = "Psyche's context model (offline: the open data could not be fetched)"
    s = M.recall_summary(R, 16, max_lag=3)
    out.row("free-recall data", f"{source}: {len(R)} lists")
    out.row("serial position 1, 8, 16", f"{s['spc'][0]:.2f}, {s['spc'][7]:.2f}, {s['spc'][15]:.2f}")
    out.row("first recall from position 16", f"{s['pfr'][15]:.2f}")
    out.row("lag-CRP at -3..+3", ", ".join("-" if np.isnan(v) else f"{v:.2f}" for v in s["crp"]))
    assert s["spc"][15] > s["spc"][7] and s["crp"][4] > s["crp"][2]  # recency; a forward lean

    # 3. SAM against CMR
    sam = M.recall_summary(M.sam_simulate(16, 2000, rng=rng), 16, max_lag=1)
    cmr = M.recall_summary(M.cmr_simulate(16, 2000, FITTED, rng), 16, max_lag=1)
    out.row("SAM: CRP at -1, +1", f"{sam['crp'][0]:.2f}, {sam['crp'][2]:.2f}")
    out.row("CMR (fitted values): CRP at -1, +1", f"{cmr['crp'][0]:.2f}, {cmr['crp'][2]:.2f}")

    # 4. the likelihood on held-out lists: CMR against serial position alone
    fit_half, test_half = R[::2], R[1::2][:600]
    cm = M.cmr_loglik(FITTED, test_half, 16, parts=True)
    base = M.position_choice_loglik(M.spc(fit_half, 16), test_half, 16)
    bits_c, bits_p = (-x["choice"] / x["recalls"] / np.log(2) for x in (cm, base))
    out.row("bits per held-out recall: serial position alone, context model", f"{bits_p:.2f}, {bits_c:.2f}")
    assert bits_c < bits_p  # the context model predicts the next word better

    # 5. the divers
    if opendata.available("murre_2021"):
        S = opendata.murre_2021()["scores"]
        eff = (S[:, 0] + S[:, 3]) / 2 - (S[:, 1] + S[:, 2]) / 2
        signs = ((np.arange(2 ** len(eff))[:, None] >> np.arange(len(eff))) & 1) * 2 - 1
        p = np.mean(np.abs((signs * eff).mean(1)) >= abs(eff.mean()) - 1e-12)
        out.row("Murre (2021): mean context effect (words), exact sign-flip p", f"{eff.mean():+.2f}, {p:.3f}")
    gb = archive.GODDEN_BADDELEY_1975.data["means"]
    out.row("Godden and Baddeley (1975): same minus other place (words)",
            f"{(gb[0] + gb[3] - gb[1] - gb[2]) / 2:+.2f}")

    # 6. Hopfield capacity
    h = M.hopfield_capacity(200, [0.05, 0.10, 0.14, 0.18, 0.25], trials=20, rng=rng)
    out.row("Hopfield, N = 200: share recalled at P/N = 0.05, 0.10, 0.14, 0.18, 0.25",
            ", ".join(f"{v:.2f}" for v in h["recalled"]))
    assert h["recalled"][0] > h["recalled"][-1]

    # 7. pattern separation
    sep = M.pattern_separation([0.2, 0.5, 0.8], pairs=20, rng=rng)
    out.row("overlap of codes for inputs overlapping 20, 50, 80%", ", ".join(f"{v:.2f}" for v in sep))

    out.note = ("Power and Ebbinghaus's laws fit his savings; an exponential cannot. Real recall shows primacy, "
                "recency, a start at the end and a forward-leaning contiguity. SAM's contiguity is symmetric; the "
                "context model's leans forward, and it predicts each next held-out word better than serial position "
                "alone. Murre's divers show no context effect. A Hopfield network fails near 0.14 patterns per unit; "
                "a sparse expansion makes similar inputs less alike.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    x = np.arange(1, 17)
    ax[0].plot(x, s["spc"], color=labs.GOLD, lw=1.8, marker="o", ms=3, label="recalled")
    ax[0].bar(x, s["pfr"], color=labs.BLUE, alpha=0.6, label="recalled first")
    ax[0].set(title=f"Serial position: {source.split(' (')[0]}", xlabel="position in the list", ylabel="probability")
    ax[0].legend(fontsize=8)
    lg = s["lags"]
    for side in (lg < 0, lg > 0):
        ax[1].plot(lg[side], s["crp"][side], color=labs.GOLD, lw=1.8, marker="o", ms=3)
    ax[1].set(title="Lag-CRP: one word leads to the next", xlabel="lag", ylabel="conditional probability")
    out.fig = fig
    return out
