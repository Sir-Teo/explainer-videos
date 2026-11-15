"""Lab 65: machines that compose, computed: Markov chains of several orders on Bach's chorale tunes, scored by how
well they predict tunes they never saw and by how much of what they write is copied; and a chain sampled exactly under
constraints."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import machines as M
from explainer.music.monochord.partkit import organ_tone

TITLE = "Machines that compose, computed"
GOAL = ("Train Markov chains of orders 0 to 6 on Bach's chorale melodies, split by hymn tune; measure bits per note on "
        "tunes kept back and how much each order's tunes copy; then sample a chain under constraints and hear the orders.")
TASKS = [
    "Change ORDERS. Where does prediction of new tunes stop improving, and where does copying take over?",
    "Change RUN, the copied-run length that counts as copying. Is Bach's own share of copying still small at RUN = 5?",
    "Change LENGTH, the constrained tune's length. How rare do legal endings become for a free draw?",
]
ORDERS = [0, 1, 2, 3, 4, 6]
RUN = 8
LENGTH = 32


def play(notes, sixteenth=0.15):
    t = sum(d for _, d, _ in notes) * sixteenth + 0.6
    y = np.zeros(int(t * SR))
    k = 0.0
    for p, d, f in notes:
        z = organ_tone(440 * 2 ** ((p - 69) / 12), d * sixteenth * (1.6 if f else 0.95), partials=6, rolloff=0.7)
        i = int(k * SR)
        y[i:i + len(z)] += z[: len(y) - i]
        k += d * sixteenth + (0.3 if f else 0.0)
    return Clip(y[: int((k + 0.5) * SR)] / (np.max(np.abs(y)) + 1e-12) * 0.8, SR)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    ts = M.tunes()
    train, test = M.split(ts, 0.2, seed=seed)
    grams = M.train_grams(train)
    lab.row("chorale tunes (major, 4/4); different hymn tunes; learn from; kept back", f"{len(ts)}; {len({t['group'] for t in ts})}; {len(train)}; {len(test)}")
    bits, share = {}, {}
    for o in ORDERS:
        m = M.Markov(o).fit(train)
        bits[o] = m.bits(test)
        share[o] = float(np.mean([M.copied_share(m.sample(seed=s), grams, RUN) for s in range(8)]))
        lab.row(f"order {o}: bits per note on new tunes; share inside a copied run of {RUN}", f"{bits[o]:.2f}; {100 * share[o]:.0f}%")
    bach = float(np.mean([M.copied_share(t["notes"], grams, RUN) for t in test]))
    lab.row(f"Bach's own tunes kept back, measured the same way", f"{100 * bach:.0f}%")
    best = min(bits, key=bits.get)
    assert 0 < best < max(ORDERS)                                          # a middle order predicts new tunes best
    if max(ORDERS) >= 6 and RUN == 8:
        assert share[max(ORDERS)] > 0.6 > bach                               # long memory copies; Bach's tunes mostly do not
    r = M.constrained(train, length=LENGTH, seed=seed)
    x = r["notes"]
    assert len(x) == LENGTH and x[-1][2] and x[-1][0] % 12 == 0
    lab.row(f"a free {LENGTH}-note draw ends legally with probability", f"{100 * r['p_legal']:.2f}%")
    order = list(rng.permutation(ORDERS[1:]))
    clips = [play(M.phrases(M.Markov(o).fit(train).sample(seed=seed + 1))[0] + M.phrases(M.Markov(o).fit(train).sample(seed=seed + 1))[1]) for o in order]
    lab.audio = concat(clips, gap=0.8)
    lab.row("ear problem: tunes from several orders, shuffled; which order was each? (listen first)", ", ".join(str(o) for o in order))
    fig, (ax1, ax2) = labs.figure(2)
    ax1.plot(ORDERS, [bits[o] for o in ORDERS], "o-", color=labs.GOLD)
    ax1.set_xlabel("order")
    ax1.set_ylabel("bits per note, new tunes")
    ax2.plot(ORDERS, [100 * share[o] for o in ORDERS], "o-", color=labs.GOLD, label="chain")
    ax2.axhline(100 * bach, color="0.6", ls="--", label="Bach kept back")
    ax2.set_xlabel("order")
    ax2.set_ylabel(f"% inside a copied run of {RUN}")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("A chain that remembers little predicts new tunes poorly and copies nothing; one that remembers much predicts "
                "them poorly too, because it copies; the best predictor sits between, near how much Bach's tunes share.")
    return lab
