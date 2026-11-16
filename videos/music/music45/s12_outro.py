from __future__ import annotations

import numpy as np

from videos.music.music45.common import *  # noqa: F403
from videos.music.variations import rows_before


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.ledger()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune")
        c = clip("tune.variation45")
        head = VGroup(label(r"Variation 45", font_size=48, color=TUNE), label(r"the Tune, \ hidden and found", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        keys, cols = [], []
        for a, b in zip(d["tune"], d["distractor"]):
            keys += [a, b]
            cols += [TUNE, GREY_B]
        r = keyroll(keys, width=11.4, height=1.8, lo=min(keys) - 2, hi=max(keys) + 2, colors=cols).move_to(UP * 0.7)
        stages = VGroup(*[label(t, font_size=19, color=WHITE) for t in (r"1. \ hidden: \ both lines on the piano", r"2. \ the other line on the chip's thin pulse",
                                                                       r"3. \ and two octaves lower")]).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=1.3)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here, the Tune's first "
            "two phrases interleaved with a line of ours that crosses it at almost every note, both on the piano: the Tune "
            "should vanish. Then the other line moves to the chip's thin, buzzing pulse, at the same pitches: timbre alone. "
            "Then it drops two octaves as well."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(r), FadeIn(stages))
        st = d["starts"]
        ioi = d["ioi"]
        with self.listen(c) as snd:
            window(snd, r"Variation 45", kind="synthesized", detail=r"Part 7's piano, \ our chip", corner=DL, tag_corner=DR)
            for i, k in enumerate(("hidden", "timbre", "register")):
                flash(snd, r.notes, [st[k] + j * ioi for j in range(len(keys))], hot=WHITE, base=GREY_A)
                end = st[["hidden", "timbre", "register"][i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, stages[i], st[k], end, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        d = load("tune")
        with self.voiceover(
            f"Row forty-five of the ledger: {say(v['seconds'], 1)} seconds; the measurement is how hidden the Tune was: "
            f"{say(len(d['tune']))} of its notes interleaved with as many others, the two lines crossing "
            f"{say(d['crossings'])} times."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"the ear groups by pitch proximity before it trusts which ear heard what",
            r"one line becomes two when notes are far apart and fast",
            r"a one-constant competition model fits the streaming boundary",
            r"harmonicity, \ common onset, \ common fate and continuity group partials",
            r"counterpoint's rules protect those groupings",
            r"pitch has height and chroma; \ memory keeps absolute pitch without the labels",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? The ear groups by pitch proximity before it trusts which ear heard what. "
            "<bookmark mark='a'/> One line becomes two when the notes are far apart and fast. <bookmark mark='b'/> A model "
            "with one constant, a competition between nearness in time and nearness in pitch, fits the streaming boundary. "
            "<bookmark mark='c'/> Harmonicity, common onset, common fate and continuity group partials into sources. "
            "<bookmark mark='d'/> Counterpoint's rules protect those groupings. <bookmark mark='e'/> And pitch has height and "
            "chroma, and many listeners retain approximate pitch information for familiar music without explicit labels."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"With the fitted model, \ at what tone repetition time do 7 semitones at 1 kHz split into two streams?",
            r"Prove that the competition model's boundary is a straight line in T, \ and find its slope in ERB-numbers.",
            r"\textbf{Ear.} \ The lab plays ABA- triplets at random intervals and speeds; \ say one stream or two.",
            r"\textbf{Build.} \ Add a sixth measurement to the timbre space \ (say, \ spectral flux) \ and redraw it.",
            r"$\bigstar$ \ Do networks trained on natural sound reproduce human streaming boundaries?",
        ], font_size=22)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, marked "
            "with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"expectation and emotion", [46]),
            (r"origins and universals: \ what is shared across cultures", [47]),
            (r"rooms and space: \ where a sound comes from", [55]),
            (r"pitch, \ onsets and transcription by machine", [61]),
            (r"source separation", [64]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In expectation and emotion. In origins and universals, what is shared across "
            "cultures. In rooms and space, where a sound comes from. In machine transcription. And in source separation."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"arrangers", r"separate parts by register and timbre so each can be followed"),
            (r"mix engineers", r"carve each source its own band and place in the stereo field"),
            (r"composers", r"use implied polyphony and Shepard-like effects on purpose"),
            (r"teachers", r"train relative pitch; \ absolute pitch is a label, \ not a requirement"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Arrangers separate parts by register and timbre so each can be followed. Mix engineers carve "
            "each source its own band and its own place in the stereo field. Composers use implied polyphony, and Shepard-like "
            "endless rises, on purpose. And teachers train relative pitch, because absolute pitch is a label, not a "
            "requirement."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"A. S. Bregman, \ \textit{Auditory Scene Analysis} \ (1990)",
             r"D. Deutsch \ (ed.), \ \textit{The Psychology of Music} \ (3rd ed., \ 2013)",
             r"D. Huron, \ `Tone and voice' \ (2001)",
             r"L. P. A. S. van Noorden, \ \textit{Temporal Coherence in the Perception of Tone Sequences} \ (1975)"],
            [r"D. Deutsch, \ `Two-channel listening to musical scales' \ (1975)",
             r"W. J. Dowling, \ `The perception of interleaved melodies' \ (1973)",
             r"B. C. J. Moore, \ B. R. Glasberg and R. W. Peters, \ on mistuned harmonics \ (1986)",
             r"A. J. E. Kell and others, \ `A task-optimized neural network replicates human auditory behavior' \ (2018)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"why does music move us, \ and can that be measured?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act VIII: \ the mind", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"We have seen how the ear builds a scene.", font_size=24, color=WHITE).move_to(UP * 1.7)
        nxt = VGroup(label(r"Part 46", font_size=32, color=GREY_B), label(r"Expectation and Emotion", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "We have seen how the ear builds a scene. <bookmark mark='a'/> Why does music move us, and can that be measured? "
            "<bookmark mark='b'/> Next time. Part 46: Expectation and Emotion."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
