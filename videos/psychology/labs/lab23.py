"""Lab 23: Zipf's law for thirty novels and a typing monkey; the interactive activation model's word superiority;
finding words in a syllable stream by transitional probabilities; a past-tense learner's U-shaped curve; and the
surprisal of every word of the Natural Stories corpus, from a trigram model, against its reading times."""

from collections import Counter

import numpy as np

from videos.coursekit import labs
from explainer.psychology import opendata
from explainer.psychology.psyche import language as LG

TITLE = "Language"
GOAL = ("Fit Zipf's law and see a monkey obey it; watch knowledge of words feed back into letters; find words in a "
        "stream by statistics alone; grow a past-tense learner's vocabulary and see it over-regularize; and fit "
        "reading times to surprisal with length and frequency held fixed.")
TASKS = [
    "Refit the reading times with a bigram model (drop the trigram counts) and with discounts of 0.5 and 0.9. Does "
    "the cost per bit on the next word change?",
    "Add a fifth word to the stream that shares its first syllable with another word. How many words of exposure "
    "does the segmenter need now?",
    "Grow the past-tense learner's vocabulary in five steps instead of one. Does the U-shaped dip survive Pinker and "
    "Prince's objection?",
]


def _novels(limit: int = 1_500_000) -> list:
    from explainer.tts import REPO_ROOT

    p = REPO_ROOT / ".cache" / "ai1" / "train.txt"
    if not p.exists():
        from videos.ai.ai1 import compute as ai1

        ai1._save("corpus", ai1.compute_corpus())
    return LG.tokenize(p.read_text()[:12_000_000])[:limit]


def run(seed=0):
    out = labs.Lab()
    rng = np.random.default_rng(seed)
    toks = _novels()
    C = Counter(toks)

    # 1. Zipf, and a monkey
    z = LG.zipf_fit(C, top=5000)
    zm = LG.zipf_fit(LG.random_typing(n_chars=2_000_000, rng=rng), top=2000)
    out.row("Zipf exponent: novels; typing monkey", f"{z['s']:.2f} (R^2 {z['r2']:.3f}); {zm['s']:.2f} (R^2 {zm['r2']:.2f})")
    assert 0.9 < z["s"] < 1.4

    # 2. word superiority
    four = [w for w, _ in C.most_common(20000) if len(w) == 4 and w.isalpha()][:1200]
    m = LG.InteractiveActivation(four, [C[w] for w in four])
    pw = m.forced_choice(list("WORK"), 3, "K", "D", mask_at=16)
    pa = m.forced_choice([None, None, None, "K"], 3, "K", "D", mask_at=16)
    out.row("K or D after WORK, and after K alone (16 cycles)", f"{pw:.3f}, {pa:.3f}")
    assert pw > pa

    # 3. segmentation
    st = LG.syllable_stream(n=180, rng=rng)
    tp = LG.transitional_probabilities(st)
    seg = LG.segment(st, tp)
    out.row("segments that are words; word and part-word scores",
            f"{np.mean([w in LG.SAFFRAN_WORDS for w in seg]):.2f}; {LG.word_score('golabu', tp):.2f}, "
            f"{LG.word_score('labubi', tp):.2f}")

    # 4. the past tense
    irr, reg = list(LG.IRREGULAR), list(LG.REGULAR)
    r = LG.past_tense_learner([irr[:10] + reg[:2], irr[:10] + reg], epochs_per_stage=12, lr=0.3, l2=1e-3, rng=rng)
    k = int((r["stage"] == 0).sum())
    out.row("early irregulars right: before the flood, at the dip, at the end",
            f"{r['right'][k - 1]:.2f}, {r['right'][k:k + 4].min():.2f}, {r['right'][-1]:.2f}")
    assert r["right"][k:k + 4].min() < r["right"][k - 1]

    # 5. surprisal and reading time
    if opendata.available("naturalstories_words"):
        import re

        ns = opendata.natural_stories()
        words = [re.sub(r"[^a-z']", "", w.lower()).strip("'") or "x" for w in ns["word"]]
        lm = LG.KneserNey(toks)
        surp = np.zeros(len(words))
        for s_ in np.unique(ns["story"]):
            idx = np.where(ns["story"] == s_)[0]
            surp[idx] = lm.surprisal([words[i] for i in idx])
        prev = np.r_[np.nan, surp[:-1]]
        prev[np.r_[True, ns["story"][1:] != ns["story"][:-1]]] = np.nan
        ok = ~np.isnan(prev)
        logf = np.log10([C.get(w, 0) + 1 for w in words])
        length = np.array([len(w) for w in words], float)
        fit = LG.rt_regression(ns["rt"][ok], surp[ok], length[ok], logf[ok], prev[ok])
        cf = dict(zip(fit["names"], fit["coef"]))
        out.row("ms per bit: this word, next word; R^2", f"{cf['surprisal']:.2f}, {cf['prev_surprisal']:.2f}; "
                f"{fit['r2']:.3f}")
        assert cf["prev_surprisal"] > 0
    else:
        out.row("surprisal and reading time", "the Natural Stories data could not be fetched")

    out.note = ("Novels and monkeys both give power laws; WORK's K beats K alone because the word feeds back; dips in "
                "transitional probability mark the words; a vocabulary flood makes the network say goed; and a "
                "surprising word costs time on the word after it.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].loglog(z["rank"], z["freq"], color=labs.GOLD, lw=1.5, label="novels")
    ax[0].loglog(zm["rank"], zm["freq"], color=labs.BLUE, lw=1.2, label="monkey")
    ax[0].set(title="Zipf's law", xlabel="rank", ylabel="frequency")
    ax[0].legend(fontsize=8)
    ax[1].plot(r["right"], color=labs.GOLD, label="right form")
    ax[1].plot(r["over"], color="#ef6f6c", label="add -ed")
    ax[1].axvline(k - 0.5, color="#9aa4b2", ls="--")
    ax[1].set(title="The past tense", xlabel="epoch", ylabel="probability")
    ax[1].legend(fontsize=8)
    out.fig = fig
    return out
