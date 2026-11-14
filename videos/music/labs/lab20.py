"""Lab 20: canons counted and found, crab canons from both ends, the four forms of a line, invertible counterpoint,
tonal answers, strettos of a subject of your own, and the forms of a phrase by ear."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import canon as K
from explainer.music.monochord import chords as CH
from explainer.music.monochord import melody as M
from explainer.music.monochord.partkit import organ_tone

TITLE = "Canons, solved"
GOAL = ("Count the canons a melody can make at every interval, find one, count crab canons, check the four forms' "
        "table, see what inversion at the octave does, answer a subject tonally, list a subject's strettos, and name "
        "the forms of a phrase by ear.")
TASKS = [
    "Change N and DELAY. Which interval is hardest now? Does the fourth stay the hardest?",
    "Write a SUBJECT of your own (midi pitches and beats) and list its strettos. Which subjects allow close strettos?",
    "Set STEPS to 7 (a canon at the octave) and listen to the canon the solver finds. Is it a melody you would sing?",
]
N, DELAY, STEPS = 12, 2, 4                               # canon length, follower delay (beats), interval (scale steps)
SUBJECT = ([67, 72, 71, 72, 74, 72, 71, 69, 67], [1, 1, 0.5, 0.5, 1, 1, 1, 1, 2])   # G C B C D C B A G, in C
SR = 48_000


def tone(midi, seconds):
    return organ_tone(CH.hz(midi), seconds, partials=6, rolloff=0.7, decay=1.4)


def render(lines, beat=0.32):
    T = max(K.end(ln) for ln in lines)
    y = np.zeros(int((T * beat + 1.0) * SR))
    for ln in lines:
        for p, a, d in ln:
            t = tone(p, d * beat * 1.1)
            i = int(a * beat * SR)
            y[i:i + len(t)] += t[: len(y) - i]
    return Clip(y, SR).fade(0.01, 0.2).at_level(-20.0)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. canons at every interval
    counts = {K.STEP_NAMES[s]: K.count_canons(N, DELAY, s) for s in range(0, 9)}
    lab.row(f"canons of {N} notes, follower {DELAY} beats later and above", ",  ".join(f"{k} {v:,}" for k, v in counts.items()))
    mel = K.sample_canon(N, DELAY, STEPS, rng=rng)
    lead, fol = K.line(mel), K.shift(K.line([K.diatonic(p, STEPS) for p in mel]), DELAY)
    f = K.faults([lead, fol], start=DELAY, stop=N)
    lab.row(f"a canon at the {K.STEP_NAMES[abs(STEPS)]}", " ".join(str(p) for p in mel) + f"   (dissonant beats {f['dissonant']}, parallels {f['parallels']})")

    # 2. crab canons
    crabs = {n: K.count_crabs(n) for n in (4, 6, 8, 10)}
    lab.row("crab canons of 4, 6, 8, 10 notes", ",  ".join(f"{v:,}" for v in crabs.values()))
    crab = K.sample_crab(10, rng=rng)
    lab.row("one crab canon", " ".join(str(p) for p in crab) + f"   (against its retrograde: {K.crab_ok(crab)['dissonant']} dissonant beats)")

    # 3. the four forms, and inversion at the octave
    lab.row("the four forms' table closes on a real line", str(K.check_table_on([60, 64, 67, 65, 62, 71])))
    lab.row("inversion at the octave: unison, third, fifth, sixth, octave become",
            ", ".join(K.STEP_NAMES[r["becomes"]] if r["becomes"] < 9 else str(r["becomes"]) for s, r in K.invertible(7).items() if s in (0, 2, 4, 5, 7)))

    # 4. answers and strettos of SUBJECT
    subj = K.line(*SUBJECT)
    lab.row("the subject", " ".join(str(p) for p, _, _ in subj))
    lab.row("real answer / tonal answer", " ".join(str(p) for p, _, _ in K.real_answer(subj)) + "  /  " + " ".join(str(p) for p, _, _ in K.tonal_answer(subj)))
    st = K.strettos(subj)
    lab.row("its strettos (delay in beats, interval in semitones)", ",  ".join(f"({x['delay']:g}, {x['interval']:+d})" for x in st) or "none")

    # 5. rounds in the corpus
    rc = K.round_census(M.corpus())
    lab.row("the best rounds in Part 14's tunes", ";  ".join(f"{r['name']} (every {r['delay']:g} beats)" for r in rc[:5]))

    # 6. Problem 3, for the ear: eight forms of three short phrases
    phrases = [K.line([72, 72, 79, 79, 81, 81, 79], [1, 1, 1, 1, 1, 1, 2]), K.line([64, 65, 67, 72, 71], [1, 1, 1, 2, 1]),
               K.line([67, 64, 65, 62, 60], [0.5, 0.5, 1, 1, 3])]
    answers, clips = [], []
    for _ in range(8):
        ph = phrases[int(rng.integers(0, 3))]
        form = K.FORMS[int(rng.integers(0, 4))]
        ax = K.degree_of(ph[0][0])[0]
        x = {"P": ph, "I": K.diatonic_invert(ph, ax), "R": K.retrograde(ph), "RI": K.retrograde(K.diatonic_invert(ph, ax))}[form]
        clips.append(render([ph]))
        clips.append(render([x]))
        answers.append({"P": "the phrase", "I": "inverted", "R": "backwards", "RI": "both"}[form])
    lab.audio = concat(clips, gap=0.8)
    lab.row("ear problem, each phrase then its form (listen first)", ";  ".join(answers))

    fig, (a, b) = labs.figure(2)
    a.bar(range(9), [counts[k] / 1000 for k in counts], color=[labs.GOLD if k not in ("fourth", "seventh") else "#d66" for k in counts])
    a.set_xticks(range(9))
    a.set_xticklabels(list(counts), rotation=40)
    a.set_ylabel("thousands")
    a.set_title(f"Canons of {N} notes at each interval")
    ns = list(crabs)
    b.semilogy(ns, [crabs[n] for n in ns], "o-", color=labs.GOLD)
    b.set_xlabel("notes")
    b.set_ylabel("crab canons")
    b.set_title("Crab canons, counted from both ends")
    lab.fig = fig
    lab.note = ("Canons exist at every interval but are rare among melodies, hardest at the fourth and seventh; crab "
                "canons grow about twenty-five-fold for every two notes; the four forms make a group of four; a tonal "
                "answer swaps tonic and dominant in the head; and a subject's strettos can be listed by trying every "
                "delay and interval.")
    return lab
