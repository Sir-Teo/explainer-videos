from __future__ import annotations

import numpy as np

from videos.music.music39.common import *  # noqa: F403
from explainer.music.monochord import blues as BL
from videos.music.variations import rows_before


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune")
        v = load("variation")
        c = clip("tune.variation39")
        head = VGroup(label(r"Variation 39", font_size=48, color=TUNE), label(r"the Tune, \ changed", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        g1 = line_over([tuple(x) for x in d["head"]], d["changes"], width=5.6, height=1.3, color=TUNE, lo=66, hi=86, size=10)
        g2 = line_over([tuple(x) for x in d["solo"]], d["changes"] * 2, width=5.6, height=1.3, color=BLUE, lo=56, hi=86, size=8)
        g3 = line_over([tuple(x) for x in d["cycle_line"]], d["third"], width=5.6, height=1.3, color=EAR, lo=64, hi=86, size=9)
        panels = VGroup(VGroup(label(r"a bebop head: \ each Tune note enclosed", font_size=16, color=TUNE), g1).arrange(DOWN, buff=0.15),
                        VGroup(label(r"the program's chorus, \ twice through", font_size=16, color=BLUE), g2).arrange(DOWN, buff=0.15),
                        VGroup(label(r"its opening through C, \ A$\flat$, \ E", font_size=16, color=EAR), g3).arrange(DOWN, buff=0.15))
        panels.arrange_in_grid(rows=2, cols=2, buff=(0.6, 0.5)).move_to(DOWN * 0.3)
        j = d["judge_solo"]
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> First as a bebop head: "
            "each of its notes held on a strong beat and enclosed, a step above and a semitone below, by the eighths before "
            "it, over two-fives of our own. Then the improviser takes a chorus over the same changes, twice through; "
            f"{say(round(100 * j['on_beat_chord_tones']))} per cent of its beats land on chord tones. Then the Tune's opening, "
            "do, do, sol, sol, is carried through C, A flat and E over Coltrane's third cycle."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(panels))
        st = d["starts"]
        bpm = d["bpm"]
        with self.listen(c) as snd:
            window(snd, r"Variation 39", kind="synthesized", detail=r"an additive saxophone, \ piano, \ string and cymbal", corner=DL, tag_corner=DR)
            for g, key, k, col in ((g1, "head", "head", TUNE), (g2, "solo", "solo", BLUE), (g3, "cycle_line", "thirds", EAR)):
                L = d[key]
                flash(snd, g.roll.notes, list(BL.swing_times([e for _, e in L], bpm) + st[k]), hot=WHITE, base=col)
                cursor(snd, g.roll, st[k], 30.0 / bpm, color=col)
        self.play(FadeOut(panels))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row thirty-nine of the ledger: {say(v['seconds'])} seconds; the measurement is the program's own chorus, judged "
            "by the series' measures."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"bebop: \ contrafacts on shared changes",
            r"the bebop scale interleaves four chord tones with four others: \ chord tones on every beat",
            r"targets, \ enclosures, \ formulas; \ chord scales and their avoid notes",
            r"modal jazz: \ few chords, \ quartal voicings",
            r"third cycles: \ three keys sharing three notes each, \ a line on the Tonnetz",
            r"the toy improviser improves selected descriptors against these baselines, \ and does not listen",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Bebop built new tunes on shared changes. <bookmark mark='a'/> The bebop scale interleaves a "
            "chord's four notes with four others, so chord tones fall on every beat, as the proof and the check showed. "
            "<bookmark mark='b'/> Lines aim at targets, enclose them, and draw on formulas; chord scales say which notes are "
            "safe. <bookmark mark='c'/> Modal jazz slowed the changes and voiced chords in fourths. <bookmark mark='d'/> "
            "Coltrane's third cycles join keys that share only three notes, a line up the Tonnetz. <bookmark mark='e'/> And a "
            "page-long improviser scores higher than these simple baselines on some descriptors its design targets, while scale adherence is lower than the scale-only baseline, and still does not listen."
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
            r"For F7, \ list the bebop scale and check that a run down from E$\flat$ lands chord tones on every beat for two octaves.",
            r"Prove that two major scales a major third apart share exactly three notes.",
            r"\textbf{Ear.} \ The lab plays lines by the improviser and by random choice; \ say which is which.",
            r"\textbf{Build.} \ Give the improviser motifs: \ repeat and transpose its own figures, \ and judge the result.",
            r"$\bigstar$ \ How much of an improvised solo is recalled, \ and how much invented?",
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
            (r"the song and its riffs", [40]),
            (r"composing as search", [42]),
            (r"performing and improvising together", [43]),
            (r"finding patterns in music collections", [63]),
            (r"machines that compose and improvise", [65]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? Next, in the popular song and its riffs. In composing as search. In performing and "
            "improvising together. In finding patterns across collections of music. And in machines that compose and "
            "improvise."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"students", r"learn tunes by their changes, \ in all twelve keys"),
            (r"players", r"practise bebop scales and enclosures until they are reflexes"),
            (r"pianists", r"reharmonise standards, \ chorus by chorus"),
            (r"software", r"generates practice accompaniments for any changes"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Students learn tunes by their changes, in all twelve keys. Players practise bebop scales and "
            "enclosures until they are reflexes. Pianists reharmonise standards chorus by chorus. And software generates "
            "practice accompaniments for any set of changes."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"T. Owens, \ \textit{Bebop: \ The Music and Its Players} \ (1995)",
             r"P. F. Berliner, \ \textit{Thinking in Jazz} \ (1994)",
             r"M. Levine, \ \textit{The Jazz Theory Book} \ (1995)",
             r"G. Russell, \ \textit{The Lydian Chromatic Concept of Tonal Organization} \ (1953)"],
            [r"J. Pressing, \ `Improvisation: \ methods and models' \ (1988)",
             r"P. N. Johnson-Laird, \ `How jazz musicians improvise' \ (2002)",
             r"M. Norgaard, \ `How jazz musicians improvise: \ the central role of auditory and motor patterns' \ (2014)",
             r"C. J. Limb and A. R. Braun, \ `Neural substrates of spontaneous musical performance' \ (2008)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 39, "twenty seconds, then five",
            "Why did the introductions of hit songs shrink from twenty seconds to five?",
            "Jazz kept its changes; popular song kept its hooks. <bookmark mark='a'/> Between the nineteen-eighties "
            "and the twenty-tens, the average introduction of a hit single shrank from about twenty seconds to about "
            "five. Why, and what has each technology that sold the song done to its shape? <bookmark mark='b'/> Next "
            "time. Part 40: The Song.")
