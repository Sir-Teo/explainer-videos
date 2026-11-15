"""Lab 46: expectation, computed: a variable-order listener's surprise and uncertainty, endings of your own,
statistical learning and a syncopation index."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat, mix
from explainer.music.monochord import listener as L
from explainer.music.monochord import melody as M
from videos.music.music46 import compute as C

TITLE = "Expectation, computed"
GOAL = ("Train a listener on a corpus and measure the surprise of every note; write your own endings for the Tune and "
        "price them; and score drum patterns for syncopation.")
TASKS = [
    "Change ORDER (0 to 6). Does a longer memory make the Tune more or less surprising? Why does it stop helping?",
    "Write ENDING (pitches after the Tune's sixth phrase, relative to C). Can you write a delay that makes the last C cheaper still?",
    "Edit PATTERN (onsets on 16 steps) and find the syncopation that grooves best for you.",
]
ORDER = 4
ENDING = [5, 5, 4, 4, 2, 2, -3, 5, 4, 2, 0]
PATTERN = [0, 3, 6, 10, 12, 14]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    corpus = [t.pitches for t in C.TUNES if t.name != M.THE_TUNE]
    lis = L.Listener(corpus, ORDER)
    r = lis.listen(C.THE.pitches)
    lab.row(f"the Tune heard at order {ORDER}: mean surprise / uncertainty (bits)", f"{r['mean_ic']:.2f} / {r['mean_entropy']:.2f}")
    head = C.THE.pitches[:-7]
    e = lis.listen(head + ENDING)
    ic = e["ic"][-len(ENDING):]
    assert all(x >= 0 for x in ic)
    lab.row("your ENDING, note by note (bits)", ", ".join(f"{x:.1f}" for x in ic))
    plain = lis.listen(C.THE.pitches)["ic"][-1]
    lab.row("the plain ending's last C, for comparison (bits)", f"{plain:.2f}")
    lab.row("PATTERN's syncopation index (Longuet-Higgins and Lee)", f"{L.syncopation(PATTERN)}")

    # sound: your ending; ear problem: a stream of words, then a word or a part-word at random
    clips = [C.play_line([(m, 1 if i < len(ENDING) - 1 else 2) for i, m in enumerate(ENDING)], beat=0.42)]
    words = C.WORDS
    s = L.saffran(words, 24, rng)
    ioi = 0.22
    clips.append(Clip(mix([(Clip(C.sine(m, 0.2), SR), i * ioi, 0.0) for i, m in enumerate(s["sequence"])], duration=len(s["sequence"]) * ioi + 0.3).y, SR))
    answers = []
    for i in range(3):
        if rng.random() < 0.5:
            trip, kind = words[int(rng.integers(4))], "word"
        else:
            a, b = rng.choice(4, 2, replace=False)
            trip, kind = (words[a][2], words[b][0], words[b][1]), "part-word"
        clips.append(Clip(mix([(Clip(C.sine(m, 0.2), SR), j * ioi, 0.0) for j, m in enumerate(trip)], duration=3 * ioi + 0.3).y, SR))
        answers.append(kind)
    lab.audio = concat(clips, gap=0.9)
    lab.row("ear problem: after the stream, each triplet is a word or a part-word (listen first)", ", ".join(answers))

    fig, (ax1, ax2) = labs.figure(2)
    ax1.bar(range(len(r["ic"])), r["ic"], color=labs.GOLD, label="surprise")
    ax1.plot(range(len(r["entropy"])), r["entropy"], color="C0", label="uncertainty")
    ax1.set_xlabel("note of the Tune")
    ax1.set_ylabel("bits")
    ax1.legend(fontsize=7)
    ax2.bar(range(len(ic)), ic, color="C3")
    ax2.set_title("your ending")
    ax2.set_xlabel("note")
    lab.fig = fig
    lab.note = ("Surprise is -log2 of the probability the model gave the note that came; uncertainty is the entropy of its "
                "prediction. A delay raises surprise at the turn and lowers it at the arrival.")
    return lab
