from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 12, r"Frontier: \ predicting the listener", r"What does a listener expect, \ and why does it matter?", extra=((2019, r"medium surprise is liked best"),),
                spoken="Frontier: predicting the listener")
        self.scores()
        self.memory()
        self.open()

    # ------------------------------------------------------------------
    def scores(self):
        d = load("frontier")
        vals = [d["uniform"], d["unigram"], d["proximity"], d["ngram"]]
        names = [r"knows nothing", r"which notes are common", r"``the next note is near''", r"the counting model"]
        ch = columns(vals, names, width=10.5, height=2.6, color=WEAK, hot=(3,), hot_color=TUNE, fmt="{:.1f}", font_size=22, top=4.6).move_to(DOWN * 0.9)
        yl = label(r"bits per note, \ LOO counting models; proximity fitted in-sample \quad (lower is better)", font_size=22, color=GREY_B).next_to(ch, DOWN, buff=0.15)
        head = label(r"three ways to guess the next note", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            f"How good is our model? Compare three predictors. The counting models use leave-one-tune-out evaluation; the proximity baseline is optimized on this same corpus, so its score is an optimistic in-sample reference, not an independent held-out test. <bookmark mark='a'/> One knows only which notes are common: {say(d['unigram'], 1)} bits a note. <bookmark mark='b'/> One knows only that the next note is probably near the last one, which is most of what the old rules of melody say: also {say(d['proximity'], 1)}. <bookmark mark='c'/> The counting model: {say(d['ngram'], 1)}. The learned model scores lower here, though this small comparison does not establish performance across traditions or datasets."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch[0]), FadeIn(VGroup(ch.bars[0], ch.labels[0], ch.values[0])), FadeIn(yl))
            for mark, k in zip("abc", (1, 2, 3)):
                vo.wait_until(mark)
                self.play(FadeIn(VGroup(ch.bars[k], ch.labels[k], ch.values[k])))
        cap = VGroup(label(r"M. Pearce's IDyOM: \ hundreds of melodies; \ pitch, \ scale degree and rhythm together", font_size=24, color=WHITE),
                     label(r"model surprise correlates with expectation judgments \ and some measured brain responses", font_size=24, color=TUNE)).arrange(DOWN, buff=0.18).next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Pearce's full model learns from hundreds of melodies, and tracks scale degree and rhythm "
            "as well as pitch. Its predictions correlate with expectation judgments in reported experiments; "
            "and related measures correlate with some event-related brain responses, measured at "
            "the scalp. Expectation is not a figure of speech. It can be computed, and it can be seen."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        g = axes([0, 10], [0, 1.2], x_length=5.4, y_length=2.8, xlabel=r"how surprising the music is", ylabel=r"how much it is liked", font_size=22).move_to(LEFT * 3.6 + DOWN * 0.3)
        xs = np.linspace(0.3, 9.7, 60)
        u = curve_from(g, xs, 1.05 * np.exp(-((xs - 5.0) / 2.6) ** 2), TUNE, stroke_width=4)
        ul = VGroup(label(r"obvious", font_size=20, color=GREY_B).move_to(g.ax.c2p(1.2, -0.12)), label(r"random", font_size=20, color=GREY_B).move_to(g.ax.c2p(8.8, -0.12)))
        note = label(r"a sketch of the finding, \ not data", font_size=18, color=GREY_B).next_to(g, DOWN, buff=0.55)
        star = VGroup(label(r"$\bigstar$ \ open", font_size=30, color=LIMIT),
                      label(r"which tunes will stick?", font_size=34, color=WHITE),
                      label(r"some melodies are remembered after one hearing;", font_size=24, color=GREY_A),
                      label(r"others are soon forgotten.", font_size=24, color=GREY_A),
                      label(r"prediction remains imperfect, \\ especially across listeners.", font_size=28, color=TUNE)).arrange(DOWN, buff=0.22).move_to(RIGHT * 3.2 + UP * 0.1)
        with self.voiceover(
            "Neural networks trained on far more music now predict a little better still. But prediction is not the whole of melody. <bookmark mark='a'/> Some experiments find an intermediate-predictability preference, dependent also on uncertainty, listener and stimulus: neither obvious nor random. Experiments by Benjamin Gold and colleagues in 2019 found that liking follows an upside-down U. <bookmark mark='b'/> Predicting which tunes will be remembered remains difficult; models can explain some variance without perfectly predicting individuals. One melody lodges in the memories of millions after a single hearing, while a thousand others, equally well formed, are gone by the next morning. Our model assigns different average likelihoods to these tune and shuffled examples; we have not established a general tune-versus-noise classifier. It cannot tell a good tune from a dull one. Likelihood alone is not a complete theory of musical quality or memory."
        ) as vo:
            lead = label(r"prediction is not the whole of melody", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
            self.play(FadeIn(lead), FadeIn(g), FadeIn(ul))
            vo.wait_until("a")
            self.play(Create(u), FadeIn(note))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in star], lag_ratio=0.5), run_time=5.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def memory(self):
        rows = VGroup(label(r"we remember contour and rhythm first; \ exact pitches last", font_size=28, color=WHITE),
                      label(r"transposition often preserves recognition; register and experience matter", font_size=28, color=WHITE),
                      label(r"tunes that get stuck in the head: \ fast, \ with a common overall shape", font_size=28, color=WHITE),
                      label(r"and one or two unusual leaps", font_size=28, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.1)
        head = label(r"what is known about memory for melody", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "What about memory? A few things are well established. <bookmark mark='a'/> Listeners keep contour and rhythm first, and exact pitches last. <bookmark mark='b'/> Melodies can often be recognized after transposition, with effects of register, timbre and listener experience. <bookmark mark='c'/> And in 2017 Kelly Jakubowski and colleagues compared tunes that people report getting stuck in their heads with similar tunes that do not. The sticky ones were faster, and had the most common overall shapes, the arch above all; <bookmark mark='d'/> but they also had one or two leaps that were out of the ordinary. A familiar shape, with a small surprise in it. That is very nearly a description of the Tune."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
