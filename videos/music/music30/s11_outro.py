from __future__ import annotations

import numpy as np

from videos.music.music30.common import *  # noqa: F403
from videos.music.variations import rows_before

ORDER = ["phase", "cloud", "partials"]


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
        c = clip("tune.variation30")
        head = VGroup(label(r"Variation 30", font_size=48, color=TUNE), label(r"the Tune, \ as sound", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        g1 = mroll(d["head"], width=3.4, height=1.4, lo=70, hi=84, color=TUNE, bar_h=0.1)
        g1b = g1.copy().set_color(BLUE).shift(RIGHT * 0.25 + DOWN * 0.15)
        W, H = 3.6, 1.6
        lines = VGroup(*[Line([-W / 2 + W * g["t0"] / d["cloud_seconds"], -H / 2 + H * (g["p0"] - 55) / 35, 0],
                              [-W / 2 + W * g["t1"] / d["cloud_seconds"], -H / 2 + H * (g["p1"] - 55) / 35, 0], color=TUNE, stroke_width=2) for g in d["glissandi"]])
        g3 = mroll([[k, a, du] for k, a, du, h in d["partials"]], width=3.4, height=1.4, lo=70, hi=84, color=EAR, bar_h=0.1)
        cells = VGroup(VGroup(label(r"phased against itself", font_size=20, color=GREY_A), VGroup(g1, g1b)).arrange(DOWN, buff=0.3),
                       VGroup(label(r"a cloud of glissandi \ following it", font_size=20, color=GREY_A), lines).arrange(DOWN, buff=0.3),
                       VGroup(label(r"on the harmonics of a low C string", font_size=20, color=GREY_A), g3).arrange(DOWN, buff=0.3)).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.2)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> This time, three "
            "sounds. The Tune's first phrase phased against itself, two pianos drifting apart. A cloud of thirty glissandi "
            "drawn towards its first two phrases, so that the melody is a tendency of the mass rather than a line. And the "
            "Tune played on the harmonics of Part 1's low C string, eighth to thirteenth, so that its F and its A are not "
            "the piano's."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"Variation 30", kind="synthesized", detail=r"piano, \ glissandi, \ string harmonics", corner=DL, tag_corner=DR)
            for i, k in enumerate(ORDER):
                st = d["starts"][k]
                end = d["starts"][ORDER[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, cells[i][0], st, end, buff=0.06)
            flash(snd, g3.notes, [d["starts"]["partials"] + p[1] * d["unit3"] for p in d["partials"]], hot=WHITE, base=EAR)
        self.play(FadeOut(cells))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row thirty of the ledger: {say(v['seconds'])} seconds. The measurement: on C's harmonics the Tune's A is "
            f"{say(round(-d['cents']['13']))} cents flatter than the piano's, and its F {say(round(d['cents']['11']))} cents "
            "sharper: the harmonic series and the keyboard disagree."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        cl = load("clouds")
        ph = load("phasing")
        card = objectives_card([
            r"tape: \ speed, \ reversal, \ and the cut attack that hides a bell",
            r"chance and silence: \ the composer's choices given away",
            r"Studie II's 81 frequencies; \ Xenakis's clouds obey Poisson's law",
            r"clusters beat about 8 times a second: \ roughness from physics",
            r"two loops pass through 12 alignments, \ symmetric about 6",
            r"one brass note rebuilt by an ensemble, \ in quarter and eighth tones",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Tape can speed, reverse and cut a sound, and without its attack a bell is hardly a bell. "
            "<bookmark mark='a'/> Chance and silence gave the composer's choices away. <bookmark mark='b'/> Studie Two built "
            "sounds from eighty-one sine frequencies, and Xenakis's clouds follow Poisson's law. <bookmark mark='c'/> "
            "Clusters beat about eight times a second, which is why they sound rough. <bookmark mark='d'/> Two loops of one "
            "figure pass through twelve alignments, symmetric about six. <bookmark mark='e'/> And one brass note can be "
            "rebuilt by an ensemble, if it plays between the piano's keys."
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
            r"A tape is played at 1.5 times its speed. \ By how many cents does every pitch rise, \ and how long does a 3-second sound last?",
            r"Show that for a Poisson process of rate $\lambda$ the gaps between events have mean and standard deviation $1/\lambda$.",
            r"\textbf{Ear.} \ The lab plays six clouds; \ some at Poisson times, \ some evenly spaced. \ Sort them.",
            r"\textbf{Build.} \ Write the phasing engine for any figure, \ and find the figures whose twelve alignments are all different.",
            r"$\bigstar$ \ For which patterns in data does listening beat looking?",
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
            (r"transformations as a group: \ the next part", [31]),
            (r"phasing, \ even rhythms and the mathematics of loops", [33]),
            (r"the ear's scene: \ masses, \ streams and roughness", [45]),
            (r"synthesis: \ oscillators, \ FM, \ grains, \ physical models", [51, 52]),
            (r"the studio: \ sampling and the sequencer", [53]),
            (r"generative audio", [66]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In the next part's mathematics of transformations. In the mathematics of loops and "
            "even rhythms. In the ear's scene, where masses and streams form. In synthesis, oscillators, frequency modulation, "
            "grains and physical models. In the studio's samplers and sequencers. And in generative audio, near the end."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"producers", r"loop, \ reverse, \ re-pitch and cut attacks every day"),
            (r"sound designers", r"build clouds and masses for film and games"),
            (r"composers", r"write processes, \ and orchestrate spectra"),
            (r"scientists", r"listen to data, \ and test when it helps"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Producers loop, reverse, re-pitch and cut attacks every day. Sound designers build clouds and "
            "masses for film and games. Composers write processes and orchestrate spectra. And scientists listen to data, and "
            "test when that helps."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"I. Xenakis, \ \textit{Formalized Music} \ (1963; \ rev. 1992)",
             r"S. Reich, \ \textit{Writings on Music, \ 1965--2000} \ (2002)",
             r"J. Fineberg \ (ed.), \ `Spectral music: \ history and techniques', \ \textit{Contemporary Music Review} \ (2000)",
             r"A. Ross, \ \textit{The Rest Is Noise} \ (2007)"],
            [r"P. Schaeffer, \ \textit{Traité des objets musicaux} \ (1966)",
             r"J. Cage, \ \textit{Silence} \ (1961)",
             r"M. V. Mathews, \ `The digital computer as a musical instrument', \ \textit{Science} \ (1963)",
             r"J. M. Chowning, \ `The synthesis of complex audio spectra by means of frequency modulation' \ (1973)"],
            font_size=19)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        q = label(r"what do all these operations have in common?", font_size=30, color=EAR).move_to(UP * 0.4)
        top = label(r"Act V: \ after tonality", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"Transposing, inverting, reversing, phasing: this act has been full of operations on music.", font_size=24, color=WHITE).move_to(UP * 1.7)
        lead.scale_to_fit_width(min(lead.width, 12.5))
        nxt = VGroup(label(r"Part 31", font_size=32, color=GREY_B), label(r"Transformations", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Transposing, inverting, reversing, phasing: this act has been full of operations on music. "
            "<bookmark mark='a'/> What do they have in common, and what can be said about all of them at once? "
            "<bookmark mark='b'/> Next time. Part 31: Transformations."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
