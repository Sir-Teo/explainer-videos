from __future__ import annotations

import numpy as np

from videos.music.music29.common import *  # noqa: F403
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
        c = clip("tune.variation29")
        head = VGroup(label(r"Variation 29", font_size=48, color=TUNE), label(r"the Tune, \ as a row", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cl = pc_clock(d["row"], radius=1.25, color=TUNE, order=True).move_to(LEFT * 4.4 + DOWN * 0.2)
        g1 = mroll(d["plain"], width=4.6, height=1.5, lo=58, hi=73, color=TUNE, bar_h=0.1)
        lo = min(n[0] for n in d["points"]) - 1
        hi = max(n[0] for n in d["points"]) + 1
        g2 = mroll(d["points"], width=6.2, height=2.0, lo=lo, hi=hi, color=BLUE, bar_h=0.08)
        right = VGroup(VGroup(label(r"the row, \ grown from the Tune's intervals", font_size=20, color=GREY_A), g1).arrange(DOWN, buff=0.2),
                       VGroup(label(r"a pointillist variation on three of its forms", font_size=20, color=GREY_A), g2).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.45).move_to(RIGHT * 1.8 + DOWN * 0.3)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> This time the Tune "
            "becomes a row. Follow its intervals in order, up a fifth, up a whole step, down, down, skipping any step that "
            "would repeat a pitch class, and fill in what is left: zero, seven, nine, eleven, one, two, four, six, eight, "
            "ten, three, five. Then a pointillist variation on three of its forms, scattered across the registers, on the "
            "piano and the bowed string."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cl), FadeIn(right))
        with self.listen(c) as snd:
            window(snd, r"Variation 29", detail=r"Part 7's piano and bowed string", corner=DL, tag_corner=DR)
            flash(snd, g1.notes, [d["starts"]["row"] + n[1] * d["unit"] for n in d["plain"]], hot=WHITE, base=TUNE)
            flash(snd, g2.notes, [d["starts"]["points"] + n[1] * d["unit"] for n in d["points"]], hot=WHITE, base=BLUE)
            pulse(snd, right[0][0], d["starts"]["row"], d["starts"]["points"] - 0.5, buff=0.06)
            pulse(snd, right[1][0], d["starts"]["points"], c.duration, buff=0.06)
        self.play(FadeOut(cl), FadeOut(right))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row twenty-nine of the ledger: {say(v['seconds'])} seconds. The measurement is the row itself, and "
            f"{say(d['notes']['points'])} notes drawn from three of its forty-eight forms."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"free atonality: \ a centre made of an interval, \ all twelve notes in play",
            r"224 set classes, \ by brute force and by Burnside's lemma; \ Forte's table confirmed",
            r"23 Z-related pairs; \ the hexachord theorem checked on 924 sets and proved",
            r"the row's 48 forms; \ Webern's canon: \ 45 of 45 intervals inverted",
            r"3,856 all-interval rows; \ first and last notes always a tritone apart".replace(",", "{,}"),
            r"six all-combinatorial hexachords; \ and listeners hear contour more than rows",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Free atonality keeps a centre, an interval rather than a tonic, with all twelve notes in play. "
            "<bookmark mark='a'/> There are two hundred and twenty-four set classes, by brute force and by Burnside's lemma, "
            "as in Forte's table. <bookmark mark='b'/> Twenty-three Z-related pairs, and a hexachord theorem checked on all "
            "nine hundred and twenty-four hexachords and proved. <bookmark mark='c'/> A row's forty-eight forms, and a canon "
            "by Webern in which every interval is inverted. <bookmark mark='d'/> Three thousand eight hundred and fifty-six "
            "all-interval rows, whose ends are always a tritone apart. <bookmark mark='e'/> Six all-combinatorial "
            "hexachords. And listeners hear contour and texture far more than rows."
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
            r"Find the prime form and interval vector of \{2, 5, 9, 11\}. \ Which familiar chord is it?",
            r"Prove that a hexachord and its complement have the same number of tritones.",
            r"\textbf{Ear.} \ The lab plays a row and eight lines; \ four are forms of it. \ Which?",
            r"\textbf{Build.} \ Write a program that finds, \ in a twelve-tone piece's encoding, \ which forms of its row each passage uses.",
            r"$\bigstar$ \ Do listeners hear interval content, \ or only surface features?",
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
            (r"after the row: \ sound itself, \ electronic music, \ Xenakis", [30]),
            (r"operations on music as a group: \ transformations", [31]),
            (r"the geometry of chords and voice leading", [32]),
            (r"the Fourier view of sets and rhythms", [33]),
            (r"what listeners expect, \ and how it is measured", [46]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? Next, in music made of sound itself. In the theory of transformations, which treats "
            "these operations as a group. In the geometry of chords. In the Fourier view of sets and rhythms. And in what "
            "listeners expect, and how it can be measured."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"composers", r"build a row with the properties they want, \ and know its forms"),
            (r"analysts", r"name sets, \ and check segmentations against chance"),
            (r"programmers", r"enumerate, \ and prove what the enumeration shows"),
            (r"listeners", r"follow contour and texture when the key is gone"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Composers build rows with the properties they want. Analysts name sets and check their "
            "segmentations against chance. Programmers enumerate, and then prove what the enumeration shows. And listeners "
            "follow contour and texture when the key is gone."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"J. N. Straus, \ \textit{Introduction to Post-Tonal Theory} \ (4th ed., \ 2016)",
             r"A. Forte, \ \textit{The Structure of Atonal Music} \ (1973)",
             r"M. Babbitt, \ `Some aspects of twelve-tone composition' \ (1955); \ \textit{Collected Essays} \ (2003)",
             r"A. Schoenberg, \ `Composition with twelve tones' \ (1941), \ in \textit{Style and Idea}"],
            [r"A. L. Patterson, \ `Ambiguities in the X-ray analysis of crystal structures', \ \textit{Physical Review} \ (1944)",
             r"C. L. Krumhansl, \ G. J. Sandell, \ D. C. Sergeant, \ \textit{Music Perception} \ (1987)",
             r"E. Amiot, \ \textit{Music Through Fourier Space} \ (2016)",
             r"M. S. Cuthbert and C. Ariza, \ `music21' \ (2010): \ the Schoenberg and Webern encodings"],
            font_size=19)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what if music were made of sound, \ not notes?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act V: \ after tonality", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        nxt = VGroup(label(r"Part 30", font_size=32, color=GREY_B), label(r"Sound Itself", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The row ordered pitch; total serialism ordered everything else, and the critics said the result was a cloud. "
            "<bookmark mark='a'/> The next step was to compose the cloud: music made of sound itself, noise, texture and "
            "electronics. <bookmark mark='b'/> Next time. Part 30: Sound Itself."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
