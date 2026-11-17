from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403
from videos.psychology.psych13.s09_cones import wl_axes


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.solid()
        self.v1()
        self.four()
        self.open()

    def card(self):
        card = chapter_card(15, r"Frontier: \ what V1 does with the world", r"How much of early vision do we understand?",
                            lit={2010: r"a tetrachromat"}, part=PART, scale=("circuit", "mind"), marr=("what", "how"))
        with self.voiceover("Chapter fifteen. The frontier: what the first stage of cortex does with the world."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def solid(self):
        head = heading(r"What is solid, \ and what is argued")
        left = rows_of([
            (r"what is solid", MODEL),
            (r"the eye's limits in physics' units: \ quanta, \ diffraction, \ sampling", WHITE),
            (r"three cones, \ colour matching, \ metamers: \ exact linear algebra", WHITE),
            (r"centre-surround and orientation-tuned cells; \ the CSF and its channels", WHITE),
        ], 5.6, 26, 0.3)
        right = rows_of([
            (r"what is argued", BAD),
            (r"what V1 does with natural scenes, \ beyond gratings and bars", WHITE),
            (r"what the many kinds of retinal output cell are each for", WHITE),
            (r"how separate the two streams are", WHITE),
        ], 5.6, 26, 0.3)
        g = VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.4, 0])
        reply = wrapped_label(r"Kant's first objection: \ the eye's threshold is now counted in quanta, \ and colour is a "
                              r"matrix: \ mathematics applies, \ exactly", 12.0, 28, KANT).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Here's where things stand. <bookmark mark='a'/> Solid: the eye's limits, stated in the units of physics: "
            "quanta, diffraction, sampling. Colour matching and metamers, as exact linear algebra. Centre-surround "
            "cells, orientation-tuned cells, and the contrast sensitivity function with its channels. "
            "<bookmark mark='b'/> Argued: what the first stage of cortex does with real scenes, rather than gratings "
            "and bars; what the many kinds of retinal output cell are each for; and how separate the two streams "
            "really are. <bookmark mark='c'/> For Kant's first objection, that mathematics can't apply to the inner "
            "sense, this part is about as strong a reply as the series will offer: a threshold counted in quanta, "
            "and colour experience predicted by a matrix."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left[0]), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in left[1:]], lag_ratio=0.8), run_time=4.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in right[1:]], lag_ratio=0.8), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(reply))
        self.clear_scene()

    def v1(self):
        head = heading(r"How close are we to understanding V1?")
        big = Ellipse(width=7.0, height=2.2, color=GREY_B, stroke_width=3).move_to([0, 1.5, 0])
        small = Ellipse(width=2.6, height=1.2, color=CELL, stroke_width=3, fill_color=CELL, fill_opacity=0.2)
        small.move_to(big.get_center() + LEFT * 1.8)
        ls = wrapped_label(r"recorded, \ and well modelled", 2.4, 20, CELL).move_to(small)
        lb = label(r"V1", font_size=26, color=GREY_B).next_to(big, LEFT, buff=0.2)
        q = label(r"?", font_size=60, color=GREY_B).move_to(big.get_center() + RIGHT * 1.6)
        bar = VGroup(big, small, ls, lb)
        rows = rows_of([
            (r"Olshausen and Field, \ 2005: \ the cells that get recorded are a biased sample, \ those that respond "
             r"well to bars and gratings", WHITE),
            (r"and models built on gratings predict only part of how even those cells respond to natural scenes", CELL),
            (r"their estimate: \ much of what V1 does is still unexplained (the picture is of the argument, \ not a "
             r"measurement)", GREY_A),
            (r"today's best predictors of V1 responses are deep networks trained on images: \ accurate, \ and hard to "
             r"read", LIGHT),
        ], 12.2, 26, 0.32).move_to([0, -1.3, 0])
        with self.voiceover(
            "Start with the cortex. <bookmark mark='a'/> In 2005 Bruno Olshausen and David Field asked how close we "
            "are to understanding V1, and their answer was uncomfortable. The cells that get recorded are a biased "
            "sample: the ones that respond well to bars and gratings, the stimuli experimenters use. "
            "<bookmark mark='b'/> And even for those cells, models built from gratings predict only part of their "
            "response to natural scenes. <bookmark mark='c'/> Their estimate was that much of what V1 does is still "
            "unexplained. The picture on the screen is a picture of that argument, not a measurement. "
            "<bookmark mark='d'/> Today, the best predictors of how V1 cells respond to images are deep neural "
            "networks trained on photographs. They're accurate, and very hard to read: a prediction is not yet an "
            "explanation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar), FadeIn(q))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r))
        self.clear_scene()

    def four(self):
        d = load("cones")
        head = heading(r"Twenty kinds of output, \ and a fourth cone")
        A = wl_axes([-3.4, -0.4, 0], y_length=3.4, x_length=6.0)
        ax = A.ax
        wl = d["wl"]
        lms = d["lms"]
        cl = curve_in(ax, wl, lms[:, 0], LCONE, stroke_width=4)
        cm = curve_in(ax, wl, lms[:, 1], MCONE, stroke_width=4)
        cs = curve_in(ax, wl, lms[:, 2], SCONE, stroke_width=4)
        shift = np.interp(wl + 12, wl, lms[:, 0], left=0, right=0)
        cx = DashedVMobject(curve_in(ax, wl, shift, LIGHT, stroke_width=4), num_dashes=50)
        rows = rows_of([
            (r"the retina has about twenty types of output cell in primates, \ more than forty in mice: \ we have "
             r"described a few of them in detail", WHITE),
            (r"some women carry a gene for a fourth, \ shifted long-wave pigment", LIGHT),
            (r"Jordan and colleagues, \ 2010: \ of 24 such carriers, \ one behaved as a true tetrachromat on every test",
             LIGHT),
            (r"a fourth dimension of colour in one person: \ a possibility, \ not yet a finding", GREY_A),
        ], 5.6, 25, 0.3).move_to([3.6, -0.3, 0])
        keep_in_frame(rows)
        tags = VGroup(published_tag(archive.JORDAN_2010.cite), psyche_tag(r"drawn: \ the L curve shifted 12 nm"))
        with self.voiceover(
            "Two more open questions. <bookmark mark='a'/> The retina doesn't have two kinds of output cell, on and "
            "off. Primates have about twenty, mice more than forty, each tiling the retina, each sending its own "
            "version of the image. We know a handful in detail. What the rest are for is an active field. "
            "<bookmark mark='b'/> And colour may have a fourth dimension in a few people. Some women carry genes "
            "for two slightly different long-wave pigments, so their retinas could hold four cone types. "
            "<bookmark mark='c'/> In 2010 Gabriele Jordan and her colleagues tested twenty-four such carriers. One "
            "of them made colour discriminations on every test that only a four-dimensional colour space allows. "
            "<bookmark mark='d'/> One person. A possibility, carefully tested, not yet a general finding."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tags), Create(cl), Create(cm), Create(cs))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cx), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def open(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"what does V1 compute on the scenes it evolved for?", CELL),
            (r"why twenty kinds of retinal output, \ and what does each tell the brain?", CENTRE),
            (r"how far does normalization go as a canonical computation?", SURROUND),
            (r"$\star$ \ design a test that would show a fourth colour dimension, \ and say why ordinary colour matching "
             r"would miss it", YOU),
        ], 12.4, 30, 0.45).move_to([0, -0.1, 0])
        with self.voiceover(
            "Four questions to carry out of this part. <bookmark mark='a'/> What does V1 compute on the scenes it "
            "evolved for? <bookmark mark='b'/> Why twenty kinds of retinal output, and what does each one tell the "
            "brain? <bookmark mark='c'/> How far does normalization go, as a single computation the brain uses "
            "everywhere? <bookmark mark='d'/> And the starred problem: design a test that would reveal a fourth "
            "dimension of colour, and explain why ordinary three-primary matching would miss it."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r))
        self.clear_scene()
