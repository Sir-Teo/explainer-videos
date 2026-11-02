from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, METHOD_COL, OPT, PART, illustration, load, loglog


class QMC(VoiceoverScene):
    def construct(self):
        q = load("qmc")
        self.card()
        self.points(q)
        self.bridge(q)

    def card(self):
        c = chapter_card(2, r"Quasi-Monte Carlo, and the Brownian bridge", r"Can points beat randomness?", part=PART)
        with self.voiceover("Chapter two. Quasi-Monte Carlo, and the Brownian bridge."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def points(self, q):
        boxes = VGroup()
        for pts, col, ttl in ((np.asarray(q["rand"]), GREY_B, r"256 pseudo-random points"),
                              (np.asarray(q["sobol"]), METHOD_COL["Sobol"], r"256 Sobol points")):
            sq = Square(side_length=4.2, stroke_color=GREY_C, stroke_width=1.5)
            dots = VGroup(*[Dot(sq.get_corner(DL) + 4.2 * np.array([x, y, 0]), radius=0.035, color=col) for x, y in pts])
            t = label(ttl, font_size=22, color=col).next_to(sq, UP, buff=0.15)
            boxes.add(VGroup(sq, dots, t))
        boxes.arrange(RIGHT, buff=1.2).move_to(DOWN * 0.1)
        foot = wrapped_label(r"random points clump and leave holes; Sobol's sequence (1967) is built digit by digit so that "
                             r"every small box gets its share. Integration error can fall almost like $1/n$ instead of "
                             r"$1/\sqrt{n}$, if the integrand's important directions are few", 11.0, 20, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Look at what random points actually do. Two hundred and fifty-six of them in a square: they clump, and "
            "leave holes. <bookmark mark='a'/> These are two hundred and fifty-six points of Ilya Sobol's sequence "
            "from 1967, built digit by digit so that every small box gets its fair share. Averaging a smooth function "
            "over such points converges almost like one over n, instead of one over root n. The catch is dimension: "
            "the guarantee weakens as dimensions grow, unless the function really depends on only a few of them."
        ) as vo:
            self.play(FadeIn(boxes[0][0]), FadeIn(boxes[0][2]), LaggedStart(*[FadeIn(d) for d in boxes[0][1]],
                                                                              lag_ratio=0.005, run_time=2))
            vo.wait_until("a")
            self.play(FadeIn(boxes[1][0]), FadeIn(boxes[1][2]), LaggedStart(*[FadeIn(d) for d in boxes[1][1]],
                                                                              lag_ratio=0.005, run_time=2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def bridge(self, q):
        ns = np.log10(np.asarray(q["ns"], float))
        g = loglog(2.2, 4.4, -3, 0, r"paths", r"spread of the price over 20 runs", xt=[3, 4], yt=[-3, -2, -1, 0])
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        lines = VGroup()
        for key in ("pseudo-random", "Sobol", "Sobol + bridge"):
            y = np.log10(np.asarray(q["sd"][key]))
            pts = [ax.c2p(a, np.clip(b, -3, 0)) for a, b in zip(ns, y)]
            lines.add(VGroup(VMobject(stroke_color=METHOD_COL[key], stroke_width=3).set_points_as_corners(pts),
                             *[Dot(p_, radius=0.05, color=METHOD_COL[key]) for p_ in pts]))
        leg = legend([(METHOD_COL[k], k) for k in ("pseudo-random", "Sobol", "Sobol + bridge")], font_size=17)
        leg.next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        sd = {k: q["sd"][k][-1] for k in q["sd"]}
        side = VGroup(
            wrapped_label(r"an Asian option on 64 fixings is a 64-dimensional integral; build each path step by step and "
                          r"the late Sobol coordinates, the least uniform, decide the average", 4.2, 18, GREY_A),
            wrapped_label(r"the Brownian bridge spends the first coordinate on the final value, the next on the midpoint, "
                          r"and so on (Caflisch, Morokoff and Owen 1997): the few best Sobol coordinates now carry most of "
                          r"the path's variance", 4.2, 18, WHITE),
            MathTex(rf"{sd['pseudo-random'] / sd['Sobol + bridge']:.0f}\times\ \text{{less spread at}}\ {q['ns'][-1]:,}"
                    .replace(",", "{,}") + r"\ \text{paths}", font_size=28, color=GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        src = illustration(r"arithmetic Asian call, 64 fixings, one year; 20 scrambled Sobol sequences or seeds per size")
        with self.voiceover(
            "A path-dependent price is a high-dimensional integral: an Asian option on sixty-four fixings needs "
            "sixty-four normal draws per path. Feed Sobol points in, step by step, and they help, but the later "
            "coordinates, the least uniform, matter as much as the first. <bookmark mark='a'/> The Brownian bridge "
            "fixes the order. Spend the first coordinate on where the path ends, the second on its midpoint, then the "
            "quarter points, and so on. The best coordinates now carry most of the variance, and the spread falls by "
            f"a factor of {sd['pseudo-random'] / sd['Sobol + bridge']:.0f} against random paths."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lines[0]), Create(lines[1]), FadeIn(leg[:2]), FadeIn(side[0]),
                      run_time=2)
            vo.wait_until("a")
            self.play(Create(lines[2]), FadeIn(leg[2]), FadeIn(side[1]), FadeIn(side[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()
