from __future__ import annotations

import numpy as np

from videos.music.music37.common import *  # noqa: F403
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
        c = clip("tune.variation37")
        n = d["n"]
        a = [[m, i, 1.0] for i, m in d["a"]]
        b = [[m, i, 1.0] for i, m in d["b"]]
        head = VGroup(label(r"Variation 37", font_size=48, color=TUNE), label(r"the Tune that nobody plays", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        roll = voices_roll([a, b], width=11.4, height=2.8, colors=[TUNE, BLUE], total=n, lo=53, hi=83, bar_h=0.11).move_to(DOWN * 0.1)
        leg = VGroup(label(r"part A: \ even pulses", font_size=18, color=TUNE), label(r"part B: \ odd pulses", font_size=18, color=BLUE)).arrange(RIGHT, buff=0.8).next_to(roll, UP, buff=0.25)
        stage = VGroup(*[label(t, font_size=19, color=GREY_A) for t in (r"A alone", r"B alone", r"both", r"over the bell pattern on claves")]).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here the Tune's first "
            "two phrases become an inherent pattern. The program places each of its fourteen notes on a grid of forty-eight "
            f"pulses, three to a beat, and shares the pulses between two mbira parts, even and odd, filling the rest with a "
            f"low figure. Part A holds {say(len(d['high_a']))} of the Tune's notes and part B {say(len(d['high_b']))}; neither "
            "plays the Tune. Hear each part alone, then both together, eight notes a second, then both over the standard "
            "pattern on claves with a drum on the four beats."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(roll), FadeIn(leg), FadeIn(stage))
        st = d["starts"]
        p = d["pulse"]
        with self.listen(c) as snd:
            window(snd, r"Variation 37", detail=r"tine, \ bar and membrane models", corner=DL, tag_corner=DR)
            for k, which, reps in (("a", (0,), 1), ("b", (1,), 1), ("both", (0, 1), 2), ("claves", (0, 1), 2)):
                for j in which:
                    v_ = [a, b][j]
                    times = [st[k] + r * n * p + nn[1] * p for r in range(reps) for nn in v_]
                    flash(snd, roll.parts[j].notes * reps, times, hot=WHITE, base=[TUNE, BLUE][j])
            ks = ["a", "b", "both", "claves"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i < 3 else c.duration
                pulse(snd, stage[i], st[k], end, buff=0.08)
        self.play(FadeOut(roll), FadeOut(leg), FadeOut(stage))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row thirty-seven of the ledger: {say(v['seconds'])} seconds; the measurement is how the Tune's fourteen notes "
            "are shared between the parts, and the speed that makes them one melody."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"the standard pattern's steps are the major scale's: \ both maximally even, \ both deep",
            r"measures of timelines: \ son clave is the most central of six",
            r"an ensemble of parts defined against a bell; \ four against six",
            r"hocket: \ a melody shared by pitch among players",
            r"the mbira's near-pure tines; \ inherent patterns, \ predicted by streaming",
            r"tresillo and clave, \ samba, \ call and response; \ uneven grids measured",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? The standard pattern's steps are the major scale's, and both are maximally even and deep. "
            "<bookmark mark='a'/> Timelines can be measured, and son clave is the most central of its family of six. "
            "<bookmark mark='b'/> An Ewe ensemble defines each part against the bell, and four beats run against six. "
            "<bookmark mark='c'/> Hocket shares a melody among players by pitch. <bookmark mark='d'/> The mbira's tines are "
            "nearly pure, and its parts make melodies nobody plays, which a streaming model predicts. <bookmark mark='e'/> "
            "And the tresillo and clave, samba and call and response carry these ideas through the Americas, while "
            "measurement shows that the grid itself need not be even."
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
            r"Compute the swap distances among the six five-stroke claves, \ and each one's total.",
            r"Prove that pulse k of an n-pulse cycle lies on a regular polygon through pulse 0 \ (a diameter counts) \ exactly when gcd(k, \ n) > 1.",
            r"\textbf{Ear.} \ The lab plays interlocking parts at several speeds; \ say when the inherent melody appears.",
            r"\textbf{Build.} \ Design two interlocking parts whose high notes spell a melody of your own; \ check them with the streaming model.",
            r"$\bigstar$ \ How are rhythm categories learned, \ and how fast can they change?",
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
            (r"swing, \ the blues and the tresillo", [38]),
            (r"the riff and the loop", [40]),
            (r"composing with patterns that emerge", [42]),
            (r"auditory streaming, \ in full", [45]),
            (r"meter and universals", [47]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? Next, in swing, the blues and the tresillo. In the riff and the loop. In composing "
            "with patterns that emerge. In auditory streaming, in full. And in meter and the question of universals."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"drummers", r"learn parts by syllables, \ always against the bell"),
            (r"arrangers", r"write `in clave', \ even when no one plays it"),
            (r"producers", r"program tresillo and clave into drum machines"),
            (r"teachers", r"use interlocking parts so that beginners make music together at once"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Drummers learn their parts by syllables, always against the bell. Arrangers write in clave, "
            "even when no one plays it. Producers program the tresillo and the clave into drum machines. And teachers use "
            "interlocking parts so that beginners make music together from the first day."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"K. Agawu, \ \textit{Representing African Music} \ (2003)",
             r"D. Locke, \ \textit{Drum Gahu} \ (1987)",
             r"P. Berliner, \ \textit{The Soul of Mbira} \ (1978)",
             r"S. Arom, \ \textit{African Polyphony and Polyrhythm} \ (1985; \ English 1991)"],
            [r"G. T. Toussaint, \ \textit{The Geometry of Musical Rhythm} \ (2013; \ 2nd ed. 2020)",
             r"G. Kubik, \ `The phenomenon of inherent rhythms in East and Central African instrumental music' \ (1962)",
             r"R. Polak, \ `Rhythmic feel as meter' \ (2010); \ R. Polak and J. London \ (2014)",
             r"N. Jacoby and others, \ `Commonality and variation in mental representations of music' \ (2024)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what happens when the tresillo, \ call and response, \ and a new kind of beat meet in America?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act VI: \ many musics", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        nxt = VGroup(label(r"Part 38", font_size=32, color=GREY_B), label(r"Blues and Swing", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Timelines crossed the Atlantic. <bookmark mark='a'/> What happens when the tresillo, call and response, and a new "
            "kind of beat meet in America, and the pulse itself begins to swing? <bookmark mark='b'/> Next time. Part 38: "
            "Blues and Swing."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
