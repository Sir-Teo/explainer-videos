from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import AUSTEN, DICKENS, HIDDEN, PART, era_strip, load, mix


class Hook(VoiceoverScene):
    def construct(self):
        self.unlabelled()
        self.era()
        self.plan()

    # ------------------------------------------------------------------
    def unlabelled(self):
        p = load("pca")
        g = load("gmm")
        xyz = np.asarray(p["proj"])[:, :3] / 3.2
        y = np.asarray(p["y"])
        r = np.asarray(g["r"])[-1]
        flip = ((r > 0.5) == y).mean() < 0.5  # which mixture component is Dickens's?
        r = 1 - r if flip else r
        # A rotation preserves this radius: every page stays clear of the heading
        # and bottom caption throughout the shot, including outlying pages.
        cloud_scale = 2.65 / max(float(np.linalg.norm(xyz, axis=1).max()), 1e-9)
        cloud = Cloud3D(xyz, [GREY_B] * len(y), scale=cloud_scale, radius=0.045, tilt=0.4,
                        center=[-0.6, -0.1, 0])
        head = label(rf"${p['n']:,}$ pages, \ ${p['d']}$ numbers each \ (Part 6) \ --- \ no authors given".replace(",", "{,}"), font_size=30)
        head.to_edge(UP, buff=0.4)
        found = label(rf"two hidden groups, found from the data alone: \ ${100 * g['agree']:.0f}\%$ match the authors",
                      font_size=30, color=WHITE).to_edge(DOWN, buff=0.45)
        key = VGroup(label(r"Austen", font_size=26, color=AUSTEN), label(r"Dickens", font_size=26, color=DICKENS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.5).shift(DOWN * 0.7)
        q = label(r"?", font_size=80, color=HIDDEN).move_to([4.6, 0.4, 0])
        with self.voiceover(
            f"Here are part six's {p['n']:,} pages again, each a point in {p['d']} dimensions, seen "
            "along the three directions in which they vary most. But this time, nobody tells us who wrote which. "
            "<bookmark mark='a'/> Can the data reveal its own hidden structure? <bookmark mark='b'/> A model that "
            "assumes there are two hidden sources, and fits them with no labels at all, finds two groups. "
            f"<bookmark mark='c'/> And they're the two authors: {100 * g['agree']:.0f} percent of the pages land with "
            "the right one."
        ) as vo:
            self.play(FadeIn(cloud), FadeIn(head), run_time=1.5)
            self.play(cloud.angle.animate.set_value(1.2), run_time=6.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(q, scale=0.6), cloud.angle.animate.set_value(1.8), run_time=2.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeOut(q), cloud.angle.animate.set_value(2.6),
                      *[d.animate.set_color(mix(AUSTEN, DICKENS, r[i])) for i, d in enumerate(cloud.dots)],
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(found), FadeIn(key), cloud.angle.animate.set_value(2.6 + math.pi / 4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def era(self):
        head = label(r"How we got here: \ the statistical era", font_size=40).to_edge(UP, buff=0.35)
        base, items = era_strip([
            (1901, r"Pearson: \\ lines of closest fit", 1),
            (1933, r"Hotelling: \\ principal components", -1),
            (1967, r"Viterbi's \\ decoder", 1),
            (1970, r"Baum: \\ training hidden states", -1),
            (1977, r"Dempster, Laird \\ \& Rubin: EM", 2),
            (1988, r"Pearl: \\ Bayesian networks", -2),
            (1993, r"IBM: \\ translation by EM", 1),
            (2003, r"topic \\ models", -1),
            (2006, r"Gaussian \\ processes", 2),
        ], y=0.35, font_size=21)
        rules = label(r"rules written by experts \ (Part 2) \ $\longrightarrow$ \ probabilities learned from data",
                      font_size=28, color=C.BITS).to_edge(DOWN, buff=0.3)
        lives = label(r"today: \ the ELBO, \ mixtures of experts, \ the forward algorithm, \ $n$-grams over trillions",
                      font_size=26, color=HIDDEN).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How did we get here? In 1901 Karl Pearson asked for the line that passes closest to a cloud of points. In "
            "1933 Harold Hotelling asked for the directions of greatest variance, and called them principal "
            "components. <bookmark mark='a'/> In the 1960s, engineers and code breakers learned to reason about states "
            "they could not see: Andrew Viterbi's decoder in 1967, Leonard Baum's training method in 1970. "
            "<bookmark mark='b'/> In 1977 Dempster, Laird and Rubin showed that one algorithm, EM, fits almost any "
            "model with missing pieces. <bookmark mark='c'/> Judea Pearl gave the field a language of graphs for "
            "reasoning under uncertainty. <bookmark mark='d'/> At IBM, Fred Jelinek's group turned speech "
            "recognition, and then translation, into statistics: count, smooth, and let the data decide. "
            "<bookmark mark='e'/> By the 1990s, the hand-written rules of part two's expert systems had given way to "
            "probabilities learned from data. <bookmark mark='f'/> Topic models in 2003 and the Gaussian process book "
            "of 2006 crowned a decade in which machine learning meant statistics. <bookmark mark='g'/> Deep learning "
            "absorbed it all, but didn't replace it. The ELBO trains today's generative models, mixtures route words "
            "to experts, the forward algorithm aligns speech, and n-grams over trillions of words check what "
            "language models have memorized."
        ) as vo:
            self.play(FadeIn(head), Create(base))
            self.play(FadeIn(items[0], shift=UP * 0.1))
            self.play(FadeIn(items[1], shift=DOWN * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(items[2], shift=UP * 0.1))
            self.play(FadeIn(items[3], shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(items[4], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(items[5], shift=DOWN * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(items[6], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(rules))
            vo.wait_until("f")
            self.play(FadeIn(items[7], shift=DOWN * 0.1), FadeIn(items[8], shift=UP * 0.1))
            vo.wait_until("g")
            self.play(FadeOut(rules), FadeIn(lives))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Statistical ML", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"models with hidden parts", font_size=32, color=HIDDEN).next_to(title, DOWN, buff=0.25)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 1.0)
        obj = objectives_card([
            r"hidden directions and sources: \ principal components, \ probabilistic PCA, \ the cocktail party",
            r"mixtures and the EM algorithm, \ proved; \ $k$-means; \ topic models",
            r"hidden Markov models, \ and the statistical revolution in speech and translation",
            r"how to count: \ Good--Turing, \ Kneser--Ney, \ and an $\infty$-gram over the thirty novels",
            r"graphical models, \ belief propagation, \ and cause and effect",
            r"Gaussian processes, \ Occam's razor, \ Bayesian optimization, \ variational inference",
        ], font_size=26)
        with self.voiceover(
            "This is part seven of AI, Built: models with hidden parts, directions, sources, states and functions "
            "that we never observe, only infer. <bookmark mark='a'/> In this part: hidden directions and sources, from "
            "principal components to the cocktail party; <bookmark mark='r2'/> mixtures, and the EM algorithm that "
            "fits them, with k-means and topic models; <bookmark mark='r3'/> hidden Markov models, and the statistical "
            "revolution they started in speech and translation; <bookmark mark='r4'/> the best ways to count, ending "
            "with an infinity-gram over all thirty novels; <bookmark mark='r5'/> graphical models, and what they can "
            "say about cause and effect; <bookmark mark='r6'/> and the Bayesian toolkit: Gaussian processes, Occam's "
            "razor, Bayesian optimization, and variational inference. Every method is written out and run."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(VGroup(title, sub, smap)), FadeIn(obj))
            self.play(Indicate(obj.rows[0], scale_factor=1.04, color=C.BITS))
            for k in range(2, 7):
                vo.wait_until(f"r{k}")
                self.play(Indicate(obj.rows[k - 1], scale_factor=1.04, color=C.BITS))
        self.wait(0.5)
        self.clear_scene()
