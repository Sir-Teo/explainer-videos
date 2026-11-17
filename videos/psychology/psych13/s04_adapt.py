from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403


class Adapt(VoiceoverScene):
    def construct(self):
        self.card()
        self.range()
        self.gain()
        self.weber()

    def card(self):
        card = chapter_card(3, r"Ten billion to one", r"How does one eye work in starlight and in sunlight?",
                            lit=(), part=PART, scale=("molecule", "circuit"), marr=("how",))
        with self.voiceover("Chapter three. Ten billion to one."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def range(self):
        head = heading(r"Starlight to sunlight")
        bar = Rectangle(width=11.5, height=0.5, stroke_width=0).set_fill(color=[ManimColor("#05070a"), ManimColor("#fff6d0")],
                                                                          opacity=1).set_sheen_direction(RIGHT)
        bar.move_to([0, 1.2, 0])
        ends = VGroup(label(r"a moonless night", font_size=24, color=GREY_B).next_to(bar, DOWN, buff=0.2).align_to(bar, LEFT),
                      label(r"noon sun", font_size=24, color=LIGHT).next_to(bar, DOWN, buff=0.2).align_to(bar, RIGHT))
        span = DoubleArrow(bar.get_left() + UP * 0.55, bar.get_right() + UP * 0.55, buff=0, color=LIGHT, stroke_width=3)
        sl = label(r"about ten log units: \ ten billion to one", font_size=28, color=LIGHT).next_to(span, UP, buff=0.12)
        one = Rectangle(width=11.5 * 1.5 / 10, height=0.5, stroke_color=CENTRE, stroke_width=4).move_to(bar.get_center() + RIGHT * 1.2)
        ol = label(r"one neuron's working range: \ one or two log units", font_size=24, color=CENTRE).next_to(one, DOWN, buff=0.75)
        rows = rows_of([
            (r"rods for the dark, \ cones for the day", ROD),
            (r"the pupil changes the light only about sixteenfold", GREY_A),
            (r"the rest is done by changing the gain: \ the receptors and the cells after them turn their own "
             r"sensitivity up and down", WHITE),
        ], 12.0, 28, 0.3).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The light you see by ranges from a moonless night to the noon sun. <bookmark mark='a'/> That's about "
            "ten log units: the brightest light is about ten billion times the dimmest. <bookmark mark='b'/> But a "
            "single neuron can only signal over a range of one or two log units before it's silent or saturated. "
            "<bookmark mark='c'/> Part of the answer is two kinds of receptor: rods for the dark, cones for the day. "
            "<bookmark mark='d'/> The pupil helps a little: it changes the light reaching the retina only about "
            "sixteen-fold. <bookmark mark='e'/> Most of the work is done by gain control. The receptors, and the "
            "cells after them, keep turning their own sensitivity up and down to match the light they're in."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar), FadeIn(ends))
            vo.wait_until("a")
            self.play(GrowFromCenter(span), FadeIn(sl))
            vo.wait_until("b")
            self.play(Create(one), FadeIn(ol))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def gain(self):
        d = load("adapt")
        head = heading(r"A response curve that slides")
        A = axes([-4, 8], [0, 1], x_length=7.6, y_length=3.6, xticks=list(range(-4, 9, 2)), yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"10^{{{int(v)}}}", xlabel=r"light", ylabel=r"response", center=[-2.2, 0.2, 0])
        ax = A.ax
        cols = [ROD, MCONE, LIGHT, LCONE]
        cs = VGroup(*[curve(ax, d["li"], d["curves"][str(b)], c, stroke_width=4) for b, c in zip(d["bgs"], cols)])
        marks = VGroup(*[Triangle(color=c, fill_opacity=1).scale(0.09).rotate(PI).move_to(ax.c2p(b, 1.06))
                         for b, c in zip(d["bgs"], cols)])
        eq = MathTex(r"R = \frac{I^{\,n}}{I^{\,n} + \sigma^{n}}", font_size=40, color=WHITE).move_to([4.5, 1.6, 0])
        rows = rows_of([
            (r"each curve: \ silent far below $\sigma$, \ saturated far above, \ useful for about two log units "
             r"around it", WHITE),
            (r"adaptation moves $\sigma$ to the light you are in (triangles): \ the same short curve, \ slid along "
             r"ten log units", LIGHT),
            (r"the price: \ what the eye reports is light relative to its surroundings, \ not the absolute amount",
             GREY_A),
        ], 4.6, 25, 0.3).move_to([4.5, -1.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ the Naka-Rushton function")
        with self.voiceover(
            "Here's how it works in Psyche. <bookmark mark='a'/> A receptor's response to light follows a "
            "saturating curve: nothing far below a half-way point, sigma; full far above it; and a useful range of "
            "about two log units in between. It's called the Naka-Rushton function, and it fits responses all the "
            "way from photoreceptors to cortex. <bookmark mark='b'/> Adaptation moves sigma to wherever the light "
            "is. In starlight the curve sits far to the left; at noon, far to the right. One short curve, slid "
            "along ten log units. <bookmark mark='c'/> The price is that the eye stops reporting how much light "
            "there is, and reports how much there is compared with the surroundings. Which is why a page looks white "
            "indoors and out, though outdoors it may reflect a hundred times more light."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(eq))
            vo.wait_until("a")
            self.play(Create(cs[1]), FadeIn(marks[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(cs[i]) for i in (0, 2, 3)], lag_ratio=0.4),
                      *[FadeIn(marks[i]) for i in (0, 2, 3)], FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def weber(self):
        d = load("adapt")
        head = heading(r"Gain control gives Weber's law")
        A = axes([-4, 8], [-3, 7], x_length=6.6, y_length=4.0, xticks=list(range(-4, 9, 2)), yticks=list(range(-2, 7, 2)),
                 xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}", xlabel=r"background light",
                 ylabel=r"smallest visible increment", center=[-2.8, -0.4, 0])
        ax = A.ax
        adapt = curve(ax, d["lb"], d["tvi"], MODEL, stroke_width=5)
        fixed = curve(ax, d["lb"], np.where(d["tvi_fixed"] < 7, d["tvi_fixed"], np.nan), BAD, stroke_width=4)
        rows = rows_of([
            (r"fixed gain: \ the curve saturates, \ and soon no increment can be seen at all", BAD),
            (rf"gain that follows the background: \ the visible increment is a fixed fraction of it, \ "
             rf"{pct(d['weber'], 1)} here, \ over ten log units", MODEL),
            (r"that is Weber's law, \ Part 11's constant fraction, \ and here is one mechanism that makes it", WHITE),
            (r"in very dim light the quanta's own noise rules instead: \ the square-root law of chapter 1", GREY_A),
        ], 4.8, 26, 0.3).move_to([4.2, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ the smallest increment that raises the response by 0.01")
        with self.voiceover(
            "This has a consequence you've already met. Ask Psyche for the smallest flash it can see against each "
            "background. <bookmark mark='a'/> With a fixed curve, the receptor soon saturates, and beyond that no "
            "increment, however large, makes a difference. The red curve shoots off the chart. <bookmark mark='b'/> "
            "With a curve that follows the background, the smallest visible increment is always the same fraction "
            "of the background: about four percent, across ten log units. <bookmark mark='c'/> That's Weber's law, "
            "the constant fraction of Part 11. Fechner took it as a law of the mind. Here it falls out of a "
            "mechanism for keeping a neuron in its working range. <bookmark mark='d'/> At the very dim end, the "
            "quanta's own randomness takes over, and with it the square-root law from chapter one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(fixed), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(adapt), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
