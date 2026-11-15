"""Lab 60: the business of music, computed: a million streams divided among their claimants, an advance recouped,
a service's month divided pro rata and user by user, a social-influence market, and how many melodies a model of
folk melody really makes.  Every term is illustrative (2026); none of it is legal or financial advice."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord import business as B
from explainer.music.monochord import melody as M
from explainer.music.monochord.partkit import organ_tone

TITLE = "The business of music, computed"
GOAL = ("Divide a million streams among the service, the label, the artist, the publisher and the songwriters; find how "
        "many streams repay an advance; divide a simulated month two ways and see who gains; run a social-influence market; "
        "and count how many distinct melodies a model of folk melody makes, and how often two songs share a phrase.")
TASKS = [
    "Change ROYALTY and ADVANCE. How many streams does the artist need, and how many does the label need, to break even?",
    "Change INFLUENCE (0 is the independent world). How do the Gini coefficient and the unpredictability move?",
    "Change K. At how many notes does a shared phrase become rare between two songs of 60 notes?",
]
ROYALTY, ADVANCE = 0.18, 150_000.0
INFLUENCE = 0.8
K = 8


def tone_line(pitches, beat=0.32):
    parts = [organ_tone(261.63 * 2 ** (p / 12), beat * 0.95, partials=5) for p in pitches]
    return np.concatenate(parts)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    p = B.population(n_users=3000, seed=seed)
    rate = float(p.fees.sum() / p.plays.sum())
    t = B.Terms(artist_royalty=ROYALTY)
    pm = B.per_million(rate, t)
    lab.row("simulated rate to all rights holders, cents a stream", f"{100 * rate:.3f}")
    lab.row("a million streams: service, label, artist, each songwriter",
            f"${pm['the service']:,.0f}, ${pm['the label']:,.0f}, ${pm['the artist (credited, against the advance)']:,.0f}, ${pm['each songwriter']:,.0f}")
    label_rate = rate * t.recording() / (1 - t.service)
    r = B.recoup(ADVANCE, [0], label_rate, royalty=ROYALTY)
    lab.row(f"streams to recoup ${ADVANCE:,.0f} at {100 * ROYALTY:.0f}%; the label's break-even", f"{r['need'] / 1e6:.0f}M; {ADVANCE / (label_rate * (1 - ROYALTY)) / 1e6:.0f}M")
    a, b = B.by_group(p, B.pro_rata(p)), B.by_group(p, B.user_centric(p))
    for g in ("chart", "niche", "fraud"):
        lab.row(f"{g}: pro rata, user-centric", f"${a[g]:,.0f}, ${b[g]:,.0f} ({100 * (b[g] / a[g] - 1):+.0f}%)")
    assert b["niche"] > a["niche"] and b["fraud"] < a["fraud"]
    ml = B.musiclab(influence=INFLUENCE, seed=seed, worlds=6)
    lab.row(f"market (influence {INFLUENCE}): Gini social / independent", f"{ml['gini_social']:.2f} / {ml['gini_independent']:.2f}")
    lab.row("unpredictability social / independent", f"{ml['U_social']:.4f} / {ml['U_independent']:.4f}")
    mdl = M.NGram(2).fit(M.corpus())
    q = B.collision(mdl, K)
    lab.row(f"{K}-note openings: effective number, against {len(mdl.alphabet)}^{K}", f"{1 / q:,.0f} against {len(mdl.alphabet) ** K:.2e}")
    lab.row(f"two 60-note songs share some {K}-note window", f"{100 * B.shared_window_prob(q, 61 - K, 61 - K):.1f}%")

    # the ear problem: four pairs of melodies; some pairs share their first six notes
    pool, seen, shared = {}, [], []
    for s in range(6000):
        mel = mdl.generate(12, start=(), seed=s)
        key = tuple(mel[:6])
        if key in pool and pool[key][6:] != mel[6:] and len(set(key)) >= 3:
            shared.append((pool[key], mel))
        pool.setdefault(key, mel)
        if len(shared) >= 2:
            break
    others = [(mdl.generate(12, start=(), seed=9000 + 2 * i), mdl.generate(12, start=(), seed=9001 + 2 * i)) for i in range(2)]
    pairs = [(x, True) for x in shared] + [(x, False) for x in others]
    order = list(rng.permutation(len(pairs)))
    clips = []
    for i in order:
        (m1, m2), _ = pairs[i]
        clips += [Clip(tone_line(m1), SR), Clip(tone_line(m2), SR)]
    lab.audio = concat(clips, gap=0.5)
    lab.row("ear problem: four pairs; which share their opening? (listen first)", ", ".join("yes" if pairs[i][1] else "no" for i in order))

    fig, (ax1, ax2) = labs.figure(2)
    ks = list(range(3, 13))
    ax1.semilogy(ks, [1 / B.collision(mdl, k) for k in ks], "o-", color=labs.GOLD, label="the model")
    ax1.semilogy(ks, [len(mdl.alphabet) ** k for k in ks], color="0.6", label="uniform")
    ax1.set_xlabel("notes")
    ax1.set_ylabel("effective number")
    ax1.legend(fontsize=7)
    for sh in ml["social"]:
        ax2.plot(np.sort(sh)[::-1], color="C0", lw=0.8)
    for sh in ml["independent"]:
        ax2.plot(np.sort(sh)[::-1], color=labs.GOLD, lw=1.5)
    ax2.set_xlabel("rank")
    ax2.set_ylabel("market share")
    lab.fig = fig
    lab.note = ("A song is two works with two owners; a stream pays its rights holders about half a cent, divided by "
                "contract; a pool divided pro rata lets heavy listeners and bots decide where everyone's fees go; social "
                "influence makes hits larger and less predictable; and melodies are far fewer than their notes suggest.")
    return lab
