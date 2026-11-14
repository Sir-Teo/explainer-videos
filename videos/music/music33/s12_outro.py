from __future__ import annotations

import numpy as np

from videos.music.music33.common import *  # noqa: F403
from videos.music.variations import rows_before
from videos.music.music33.s06_canon import tile_grid


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
        c = clip("tune.variation33")
        cn = load("canon")["vuza"]
        head = VGroup(label(r"Variation 33", font_size=48, color=TUNE), label(r"the Tune, \ tiled, \ rung, \ and without octaves", font_size=28, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        g = tile_grid(cn["n"], cn["A"], cn["B"], width=6.0, row_h=0.16).move_to(LEFT * 3.4 + DOWN * 0.2)
        bells = VGroup(*[VGroup(*[label(str(b), font_size=15, color=GREY_A) for b in r]).arrange(RIGHT, buff=0.15) for r in d["hunt"]]).arrange(DOWN, buff=0.08).move_to(RIGHT * 0.9 + DOWN * 0.2)
        bp = mroll([[p, a, dd] for p, a, dd in d["bp_notes"]], width=3.0, height=1.6, lo=-1, hi=14, color=EAR, bar_h=0.1).move_to(RIGHT * 4.6 + DOWN * 0.2)
        caps = VGroup(label(r"a Vuza canon: \ the Tune's first 12 notes as 12 voices", font_size=16, color=TUNE).next_to(g, DOWN, buff=0.3),
                      label(r"plain hunt on bells A, \ G, \ F, \ C", font_size=16, color=BLUE).next_to(bells, DOWN, buff=0.3),
                      label(r"Bohlen--Pierce, \ Lambda mode", font_size=16, color=EAR).next_to(bp, DOWN, buff=0.3))
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> First, the Vuza canon "
            "of chapter five, with the Tune's first twelve notes as its twelve voices: every pulse of seventy-two is struck "
            "exactly once, and a new melody falls out of the tiling. Then plain hunt on four bells tuned to the Tune's first "
            "four different pitches. Then the Tune's opening in the Bohlen–Pierce scale, each degree of the major scale "
            "moved to a degree of its Lambda mode, on a tone of odd harmonics."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(bells), FadeIn(bp), FadeIn(caps))
        with self.listen(c) as snd:
            window(snd, r"Variation 33", kind="synthesized", detail=r"piano, \ bells, \ additive tones", corner=DL, tag_corner=DR)
            vp = d["vpulse"]
            for j, b in enumerate(cn["B"]):
                for i, a in enumerate(cn["A"]):
                    t = ((a + b) % cn["n"]) * vp
                    pulse(snd, g.cells[j][i], t, t + vp * 1.5, buff=0.02)
            t = d["starts"]["bells"]
            for i in range(len(bells)):
                pulse(snd, bells[i], t, t + 4 * 0.18 - 0.05, buff=0.03)
                t += 4 * 0.18 + (0.18 if i % 2 == 1 else 0.0)
            flash(snd, bp.notes, [d["starts"]["bp"] + n[1] * 0.42 for n in d["bp_notes"]], hot=WHITE, base=EAR)
        self.play(FadeOut(g), FadeOut(bells), FadeOut(bp), FadeOut(caps))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row thirty-three of the ledger: {say(v['seconds'])} seconds; the measurement is the tiling, the changes and "
            "the thirteen steps."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"Euclid's algorithm spreads k strokes in n pulses: \ the world's timelines",
            r"maximally even: \ the bell pattern and the major scale are one shape",
            r"stacks of fifths give two step sizes at 5, \ 7, \ 12, \ 41, \ 53: \ continued fractions",
            r"oddity, \ homometry, \ and a Vuza canon at 72, \ verified",
            r"Fibonacci in Sanskrit metre; \ every order of four bells in Plain Bob",
            r"temperaments as linear maps; \ a scale with no octave",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Euclid's algorithm spreads strokes as evenly as possible and generates the world's timelines. "
            "<bookmark mark='a'/> The bell pattern and the major scale are one maximally even shape. <bookmark mark='b'/> "
            "Stacks of fifths have two step sizes exactly at five, seven, twelve and the other denominators of the fifth's "
            "continued fraction. <bookmark mark='c'/> Oddity, homometry, and a canon that tiles seventy-two pulses with "
            "neither part repeating. <bookmark mark='d'/> Fibonacci numbers in Sanskrit metre, and every order of four bells "
            "in Plain Bob. <bookmark mark='e'/> Temperaments as linear maps, and a scale with no octave."
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
            r"Compute E(5, 9) and E(4, 11) by Bjorklund's process, \ and find a tradition that uses one of them.",
            r"Prove that a rhythm with the oddity property has at most n/2 strokes in n pulses.",
            r"\textbf{Ear.} \ The lab plays rhythms of five strokes in twelve pulses; \ say which are Euclidean.",
            r"\textbf{Build.} \ Write a temperament finder for the 7-limit, \ and find which divisions temper out 225/224.",
            r"$\bigstar$ \ Is maximal evenness a cultural choice or a cognitive constraint?",
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
            (r"tala and its cycles", [34]),
            (r"timelines in their musical worlds", [37]),
            (r"tunings for new instruments", [52]),
            (r"algorithmic composition", [65]),
            (r"research in music", [67]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In the cycles of tala, next. In timelines in their own musical worlds. In tunings "
            "for new instruments. In algorithmic composition. And in doing research in music."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"drum machines", r"offer Euclidean pattern generators as a standard feature"),
            (r"producers", r"rotate and layer Euclidean rhythms for polyrhythm"),
            (r"microtonal musicians", r"choose equal divisions by the commas they temper out"),
            (r"bell ringers", r"still ring extents, \ and compose new methods"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Many drum machines and sequencers offer Euclidean pattern generators. Producers rotate and "
            "layer them for polyrhythm. Microtonal musicians choose equal divisions by the commas they temper out. And bell "
            "ringers still ring extents and compose new methods."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"G. Toussaint, \ \textit{The Geometry of Musical Rhythm} \ (2013; \ 2nd ed. 2019)",
             r"E. Amiot, \ \textit{Music Through Fourier Space} \ (2016)",
             r"D. J. Benson, \ \textit{Music: \ A Mathematical Offering} \ (2006)",
             r"S. Arom, \ \textit{African Polyphony and Polyrhythm} \ (1991)"],
            [r"G. Toussaint, \ `The Euclidean algorithm generates traditional musical rhythms' \ (2005)",
             r"E. Bjorklund, \ `The theory of rep-rate pattern generation in the SNS timing system' \ (2003)",
             r"J. Clough, \ J. Douthett, \ `Maximally even sets', \ \textit{Journal of Music Theory} \ (1991)",
             r"D. T. Vuza, \ `Supplementary sets and regular complementary unending canons', \ \textit{PNM} \ (1991--93)"],
            font_size=19)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what does a whole musical tradition build from cycles and scales?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act VI: \ many musics", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        nxt = VGroup(label(r"Part 34", font_size=32, color=GREY_B), label(r"Raga and Tala", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "This part ends Act Five. The mathematics of cycles and scales is universal; the music made from them is not. "
            "<bookmark mark='a'/> What does a whole musical tradition build from cycles of beats and families of scales? "
            "<bookmark mark='b'/> Act Six begins. Part 34: Raga and Tala."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
