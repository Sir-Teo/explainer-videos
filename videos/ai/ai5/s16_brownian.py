from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, MODEL, WALK, follow, load, swarm

PATH_COLORS = [DATA, C.BITS, "#D4A5FF"]


class Brownian(VoiceoverScene):
    def construct(self):
        self.card()
        self.refine()
        self.fan()
        self.cloud()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"Brownian motion", r"What does pure randomness look like in time?", part=5)
        with self.voiceover("Chapter eight. Brownian motion."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def axes(self, y=2.4, x_length=8.4):
        ax = Axes(x_range=[0, 1, 0.25], y_range=[-y, y, 1], x_length=x_length, y_length=5.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
        xl = label(r"time $t$", font_size=24, color=GREY_A).next_to(ax.x_axis.get_right(), DOWN, buff=0.2)
        return ax, xl

    # ------------------------------------------------------------------
    def refine(self):
        d = load("brownian")
        ax, xl = self.axes(y=3.0, x_length=6.8)
        ax.move_to([-3.0, -0.3, 0])
        xl.next_to(ax.x_axis.get_right(), DOWN, buff=0.2)

        def walks(n):
            w = np.asarray(d[f"walk{n}"])
            return VGroup(*[VMobject(color=PATH_COLORS[k], stroke_width=3 if n < 100 else 2).set_points_as_corners(
                [ax.c2p(i / n, v) for i, v in enumerate(w[k])]) for k in range(3)])

        w8, w64, w1024 = walks(8), walks(64), walks(1024)
        nv = Integer(8, font_size=40, color=C.BITS)
        nlab = label(r"steps, \ each $\pm 1/\sqrt{n}$", font_size=30)
        nl = VGroup(nv, nlab).arrange(RIGHT, buff=0.2)
        nl.to_corner(UR, buff=0.5)
        nv.add_updater(lambda m: m.next_to(nlab, LEFT, buff=0.2))  # the number grows leftwards
        why = label(r"after time $t$: \ variance $= (nt) \times \dfrac{1}{n} = t$, \ whatever $n$", font_size=26,
                    color=GREY_A).next_to(nl, DOWN, buff=0.3).align_to(nl, RIGHT)
        bm = label(r"the limit: \ Brownian motion $W_t$", font_size=32, color=WALK).next_to(why, DOWN, buff=0.45)
        bm.align_to(nl, RIGHT)
        nd = label(r"continuous everywhere, \ smooth nowhere", font_size=26, color=GREY_A).next_to(bm, DOWN, buff=0.15)
        nd.align_to(nl, RIGHT)
        cite_ = cite(r"R.~Brown (1827); \ N.~Wiener (1923)", corner=DR)
        vx = np.linspace(-3, 3, 80)
        vbell = VMobject(stroke_color=MODEL, stroke_width=3).set_points_smoothly(
            [np.array([0.6 * x, 1.1 * math.exp(-x * x / 2), 0]) for x in vx])
        vpic = VGroup(Line([-1.9, 0, 0], [1.9, 0, 0], color=GREY_C, stroke_width=1.5), vbell,
                      DashedLine([0, 0, 0], [0, 1.15, 0], color=GREY_B, stroke_width=1.5),
                      DoubleArrow([0, 0.45, 0], [0.6, 0.45, 0], buff=0, color=C.BITS, stroke_width=3, tip_length=0.12),
                      label(r"spread", font_size=20, color=C.BITS).move_to([0.95, 0.75, 0]))
        var_card = gloss(r"variance", r"the average squared distance from the centre:\\ the spread, squared",
                         picture=vpic, corner=DR, width=4.4, color=C.BITS)
        var_card.shift(UP * 0.5)
        g = np.random.default_rng(1827)
        jig = np.cumsum(g.normal(scale=0.07, size=(160, 2)), 0)
        jig -= jig.mean(0)
        lens = Circle(radius=2.2, color=GREY_B, stroke_width=3, fill_color="#0F1622", fill_opacity=1)
        grain = glow_dot(np.array([*jig[0], 0]), color=C.BITS, radius=0.12)
        trace = VMobject(color=C.BITS, stroke_width=1.5, stroke_opacity=0.5).set_points_as_corners(
            [np.array([*p_, 0]) for p_ in jig])
        mic = label(r"pollen in water, \ under a microscope", font_size=26, color=GREY_A).next_to(lens, DOWN, buff=0.25)
        with self.voiceover(
            "In 1827, the botanist Robert Brown watched pollen in water under a microscope, and saw it jiggle, "
            "endlessly, for no visible reason. <bookmark mark='a'/> Here's a model: a walk that steps up or down at "
            "random. Eight steps. <bookmark mark='b'/> Sixty-four smaller steps. A thousand and twenty-four, smaller "
            "still. <bookmark mark='c'/> Shrink each step like one over the square root of their number, so the "
            "spread after any time stays the same: the variance, the average squared distance from the start, comes "
            "out at exactly t, and the walks settle into a single random object: Brownian "
            "motion. It's continuous everywhere, and so jagged it has no slope anywhere."
        ) as vo:
            self.play(FadeIn(lens), FadeIn(grain), FadeIn(mic))
            self.play(MoveAlongPath(grain, trace), Create(trace), run_time=5.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeOut(VGroup(lens, grain, trace, mic)))
            self.play(Create(ax), FadeIn(xl), FadeIn(nl))
            self.play(LaggedStart(*[Create(w) for w in w8], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(Transform(w8, w64), ChangeDecimalToValue(nv, 64), run_time=1.5)
            self.play(Transform(w8, w1024), ChangeDecimalToValue(nv, 1024), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(why), FadeIn(var_card))
            self.play(FadeIn(bm), FadeIn(nd), FadeIn(cite_))
        nv.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fan(self):
        d = load("brownian")
        paths, ends, var = np.asarray(d["paths"]), np.asarray(d["ends"], float), np.asarray(d["var"])
        assert np.allclose(var, [0.25, 0.5, 0.75, 1.0], rtol=0.05)
        ax, xl = self.axes(y=3.0)
        ax.move_to([-0.6, -0.3, 0])
        xl.next_to(ax.x_axis.get_right(), DOWN, buff=0.2)
        n = paths.shape[1] - 1
        fan = VGroup(*[VMobject(color=interpolate_color(ManimColor(DATA), ManimColor(WALK), k / 59), stroke_width=1.3,
                                stroke_opacity=0.7).set_points_as_corners([ax.c2p(i / n, v) for i, v in enumerate(p)])
                       for k, p in enumerate(paths)])
        ts = np.linspace(0.001, 1, 120)
        env = VGroup(*[VMobject(color=C.BITS, stroke_width=3).set_points_smoothly([ax.c2p(t, s * c * math.sqrt(t))
                                                                                     for t in ts])
                       for s in (1, -1) for c in (1, 2)])
        for k in (1, 3):
            env[k].set_stroke(opacity=0.45)
        el = MathTex(r"\pm\sqrt{t}", font_size=34, color=C.BITS).next_to(ax.c2p(1, 1), RIGHT, buff=0.1)
        el2 = MathTex(r"\pm 2\sqrt{t}", font_size=30, color=C.BITS).next_to(ax.c2p(1, 2), RIGHT, buff=0.1)
        el2.set_opacity(0.6)
        # sideways histograms of where 20,000 paths are at t = 1/4, 1/2, 3/4, 1
        hists = VGroup()
        edges = np.linspace(-3, 3, 41)
        for j, t in enumerate((0.25, 0.5, 0.75, 1.0)):
            dens = ends[j] / ends[j].sum() / (edges[1] - edges[0])
            x0 = ax.c2p(t, 0)[0]
            pts = [np.array([x0, ax.c2p(0, edges[0])[1], 0])]
            for k, h in enumerate(dens):
                xx = x0 + 0.55 * h
                pts += [np.array([xx, ax.c2p(0, edges[k])[1], 0]), np.array([xx, ax.c2p(0, edges[k + 1])[1], 0])]
            pts.append(np.array([x0, ax.c2p(0, edges[-1])[1], 0]))
            hists.add(Polygon(*pts, stroke_width=1, color=MODEL, fill_color=MODEL, fill_opacity=0.35))
        colors = {r"W_t": WALK, r"t": C.BITS}
        f = cmath(r"W_t", r"\sim", r"\mathcal{N}(0,\,", r"t", r")", colors=colors, font_size=46).to_corner(UL, buff=0.4)
        vl = label(r"variance measured on $20{,}000$ paths: \ " + ", \\ ".join(f"${v:.2f}$" for v in var), font_size=24,
                   color=MODEL).to_edge(DOWN, buff=0.25)
        slow = label(r"twice the time: \ $\sqrt{2} \approx 1.4$ times the spread", font_size=28, color=C.BITS)
        slow.next_to(f, DOWN, buff=0.25).align_to(f, LEFT)
        with self.voiceover(
            "Now draw sixty of them. <bookmark mark='a'/> At any moment, where they've got to follows a bell curve, "
            "centred at zero, with spread the square root of t. <bookmark mark='b'/> Twice the time gives about 1.4 "
            "times the spread, not twice. Randomness spreads slowly. It's the central limit theorem again: the "
            "position at time t is a sum of many tiny independent kicks. <bookmark mark='c'/> Measured on twenty "
            "thousand paths, the variances, the spreads squared, come out at a quarter, a half, three quarters and "
            "one: exactly t."
        ) as vo:
            self.play(Create(ax), FadeIn(xl))
            self.play(LaggedStart(*[Create(p) for p in fan], lag_ratio=0.03), run_time=3.0)
            vo.wait_until("a")
            self.play(Write(f), Create(env), FadeIn(el), FadeIn(el2))
            vo.wait_until("b")
            self.play(FadeIn(slow))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(h, LEFT) for h in hists], lag_ratio=0.25), FadeIn(vl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cloud(self):
        g = np.random.default_rng(1905)
        n, steps, dt = 400, 90, 1 / 90
        P = np.zeros((steps + 1, n, 2))
        for k in range(steps):
            P[k + 1] = P[k] + math.sqrt(dt) * g.normal(size=(n, 2))
        S = 1.3  # drawn 1.3 times life size
        c = np.array([-2.6, -0.3, 0])
        dots = swarm(P[0] * S + c[:2], [interpolate_color(ManimColor(DATA), ManimColor(WALK), i / n) for i in range(n)],
                     radius=0.03)
        t = ValueTracker(0.0)
        dots.add_updater(follow(dots, P, t, scale=S, shift=c))
        ring = always_redraw(lambda: Circle(radius=max(S * math.sqrt(2 * t.get_value() / steps), 0.01), color=C.BITS,
                                            stroke_width=2.5).move_to(c))
        rl = label(r"the typical distance grows like $\sqrt{t}$", font_size=26, color=C.BITS).to_edge(DOWN, buff=0.4)
        rl.set_x(c[0])
        colors = {r"p": MODEL}
        heat = cmath(r"\frac{\partial p}{\partial t}", "=", r"\tfrac12", r"\nabla^2 p", colors=colors, font_size=50)
        heat.move_to([3.9, 1.4, 0])
        hl = label(r"the heat equation: \ the density spreads smoothly", font_size=26, color=GREY_A)
        hl.next_to(heat, DOWN, buff=0.3)
        hist = label(r"Einstein (1905): \ molecules are real, \\ and this counts them \ (Perrin, 1908)", font_size=26,
                     color=WHITE).next_to(hl, DOWN, buff=0.6)
        with self.voiceover(
            "In two dimensions, a cloud of particles released at one point spreads into a widening bell. "
            "<bookmark mark='a'/> Follow the density instead of the particles, and it obeys a rule that says exactly "
            "how the cloud's shape changes from one moment to the next, an equation with no "
            "randomness in it at all: the heat equation. The jiggling of each particle becomes the smooth spreading "
            "of the whole. <bookmark mark='b'/> Einstein worked this out in 1905, and used it to argue that "
            "molecules are real. A few years later, Jean Perrin measured the jiggling, and counted them."
        ) as vo:
            self.play(FadeIn(dots), FadeIn(ring))
            self.play(t.animate.set_value(steps), FadeIn(rl), run_time=6.0, rate_func=linear)
            vo.wait_until("a")
            self.play(Write(heat), FadeIn(hl))
            vo.wait_until("b")
            self.play(FadeIn(hist))
        dots.clear_updaters()
        ring.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
