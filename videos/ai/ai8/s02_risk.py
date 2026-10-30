from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import BAYES, HIST, NEG, POS, TEST, TRAIN, chapter, curve, load


class Risk(VoiceoverScene):
    def construct(self):
        chapter(self, 1, r"Risk, and the best possible rule", r"What exactly are we trying to make small?",
                "Chapter one. Risk, and the best possible rule.", lit=(1967,))
        self.define()
        self.bayes()
        self.learn()

    # ------------------------------------------------------------------
    def densities(self, r, center=(0, -0.9, 0), x_length=9.0, y_length=3.4):
        xg, p1, p0 = np.asarray(r["xg"]), np.asarray(r["p1"]), np.asarray(r["p0"])
        top = float(max(p1.max(), p0.max())) * 1.1
        g = axes([-4.5, 4.5], [0, top], x_length=x_length, y_length=y_length, xticks=[-4, -2, 0, 2, 4],
                 xlabel=r"$x$", center=center)
        ax = g.ax
        c1 = curve(ax, xg, p1, POS, 3.5)
        c0 = curve(ax, xg, p0, NEG, 3.5)
        return g, ax, c1, c0, xg, p1, p0

    def define(self):
        r = load("risk")
        g, ax, c1, c0, xg, p1, p0 = self.densities(r, center=(-1.6, -1.2, 0), x_length=7.6, y_length=3.0)
        x40, y40 = np.asarray(r["x40"]), np.asarray(r["y40"])
        dots = VGroup(*[Dot(ax.c2p(float(x), 0.012 + 0.018 * (i % 3)), radius=0.055, color=POS if y else NEG)
                        for i, (x, y) in enumerate(zip(x40, y40))])
        k1 = label(r"class $1$", font_size=24, color=POS).next_to(ax.c2p(1.0, float(p1.max())), UP, buff=0.1)
        k0 = label(r"class $0$", font_size=24, color=NEG).next_to(ax.c2p(-2.6, float(np.interp(-2.6, xg, p0))), UP, buff=0.15)
        dfn = definition_card(r"risk and empirical risk",
                              r"a rule $h$ predicts $y$ from $x$; \ the loss $\ell(h(x), y)$ is $1$ when it is wrong. "
                              r"\\ Risk: \ $R(h) = \mathbb{E}_{(x,y) \sim \mathcal{D}}\,\ell(h(x), y)$, \ the error on "
                              r"all the data there could be. \\ Empirical risk: \ $\hat R_S(h) = \frac1n \sum_{i=1}^n "
                              r"\ell(h(x_i), y_i)$, \ on the sample $S$ we have.",
                              width=6.6, font_size=21).to_corner(UR, buff=0.3)
        head = label(r"Two classes, \ equally likely \ (illustrative)", font_size=28).to_corner(UL, buff=0.35)
        with self.voiceover(
            "To say what generalizing means, we need two numbers. Here's a problem small enough to know completely: "
            "two classes, equally likely, each with its own spread of a single measurement x. <bookmark mark='a'/> A "
            "sample is forty points drawn from it. <bookmark mark='b'/> A rule h guesses the class from x, and the "
            "loss is one when it's wrong. Its risk is the expected loss over everything the world could send, the "
            "error rate on data it has never seen. <bookmark mark='c'/> Its empirical risk is the average loss on "
            "the sample we have: the training error. Generalizing means the second is a good guide to the first, "
            "even for a rule we chose by looking at the sample."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(c1), Create(c0), FadeIn(k1), FadeIn(k0), run_time=1.8)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.04), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(dfn, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(Indicate(dfn.body, color=WHITE, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bayes(self):
        r = load("risk")
        g, ax, c1, c0, xg, p1, p0 = self.densities(r, center=(0, -1.75, 0), x_length=9.4, y_length=2.6)
        lo = np.minimum(p1, p0)
        pts = [ax.c2p(x, y) for x, y in zip(xg, lo)] + [ax.c2p(xg[-1], 0), ax.c2p(xg[0], 0)]
        overlap = Polygon(*pts, stroke_width=0, fill_color=BAYES, fill_opacity=0.45)
        a, b = float(r["a"]), float(r["b"])
        band = Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0], height=0.18, stroke_width=0, fill_color=POS,
                         fill_opacity=0.6).move_to([(ax.c2p(a, 0)[0] + ax.c2p(b, 0)[0]) / 2, ax.c2p(0, 0)[1] - 0.14, 0])
        bl = label(r"Bayes rule: \ say $1$ here", font_size=22, color=POS).next_to(band, DOWN, buff=0.1)
        rows = [
            cmath(r"R(h)", r"=", r"\mathbb{E}_x\, P\big(y \ne h(x) \mid x\big)", font_size=34),
            cmath(r"R(h)", r"\ge", r"\mathbb{E}_x\, \min\big(\eta(x),\, 1 - \eta(x)\big)", font_size=34),
            cmath(r"R(h)", r"\ge", r"R^* = \textstyle\int \min\big(p_0(x),\, p_1(x)\big)\, dx", font_size=34,
                  colors={r"R^* = \textstyle\int \min\big(p_0(x),\, p_1(x)\big)\, dx": BAYES}),
        ]
        whys = [why(r"average over $x$ the chance of a wrong guess"),
                why(r"$\eta(x) = P(y = 1 \mid x)$: \ the best guess at $x$ errs with the smaller one"),
                why(r"equality for $h^*(x) = [\eta(x) > \tfrac12]$: \ the Bayes rule")]
        step = ladder(self, rows, whys, keep=3, top=3.3, x=-3.6, buff=0.42, edge=6.9)
        val = label(rf"here \ $R^* = {r['bayes']:.3f}$: \ the overlap", font_size=26, color=BAYES)
        val.next_to(ax.c2p(-4.2, float(max(p1.max(), p0.max()))), RIGHT, buff=0.1)
        hist = history_card(1967, r"T.~Cover \& P.~Hart", r"one nearest neighbour, given endless data, errs at most "
                            r"twice as often as the Bayes rule", width=4.6, font_size=19, color=HIST)
        hist.to_corner(DR, buff=0.25).shift(UP * 2.1)
        with self.voiceover(
            "What's the best any rule could do? Average over x the chance that the guess at x is wrong. "
            "<bookmark mark='a'/> At each x the true class is one with some probability, eta of x; the best guess "
            "picks the likelier class, and is wrong with the smaller of eta and one minus eta. "
            "<bookmark mark='b'/> So no rule beats the average of that minimum: the Bayes risk, here the area where "
            f"the two curves overlap, {r['bayes']:.3f}. The rule that achieves it says one wherever class one is the "
            "likelier: here, on an interval. <bookmark mark='c'/> It needs the true distribution, which we never "
            "have; it's the floor to measure learners against. Cover and Hart showed in 1967 that a single nearest "
            "neighbour, with endless data, errs at most twice as often."
        ) as vo:
            self.play(FadeIn(g), Create(c1), Create(c0))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(overlap), FadeIn(val))
            self.play(FadeIn(band), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(hist, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learn(self):
        r = load("risk")
        g, ax, c1, c0, xg, p1, p0 = self.densities(r, center=(-3.3, 1.2, 0), x_length=6.0, y_length=2.1)
        t40 = np.asarray(r["t40"])
        ts = float(r["t_star"])
        top = ax.c2p(0, float(max(p1.max(), p0.max())))[1]
        tl = VGroup(*[Line(ax.c2p(float(t), 0), [ax.c2p(float(t), 0)[0], top, 0], color=WHITE, stroke_width=1.2)
                      .set_stroke(opacity=0.35) for t in np.clip(t40, -4.4, 4.4)])
        best = DashedLine(ax.c2p(ts, 0), [ax.c2p(ts, 0)[0], top, 0], color=TEST, stroke_width=3)
        cap = label(r"rules ``$1$ if $x > t$'', \ learned from $40$ points, \ $30$ times", font_size=22, color=GREY_A)
        cap.next_to(g, DOWN, buff=0.15)
        ns = np.asarray(r["ns"], float)
        lx = np.log10(ns)
        em, tm = np.asarray(r["emp_mean"]), np.asarray(r["true_mean"])
        tq = np.asarray(r["true_q"])
        bay, rc = float(r["bayes"]), float(r["r_class"])
        ya, yb = 0.12, 0.32
        G = axes([1, 3.5], [ya, yb], x_length=6.0, y_length=4.4, xticks=[1, 2, 3], xfmt=lambda v: f"10^{{{int(v)}}}",
                 yticks=[0.15, 0.2, 0.25, 0.3], yfmt=lambda v: rf"{100 * v:.0f}\%", xlabel=r"$n$: examples",
                 ylabel=r"error", center=(3.4, -0.6, 0))
        A = G.ax
        cb = band(A, lx, np.clip(tq[0], ya, yb), np.clip(tq[1], ya, yb), TEST, 0.15)
        ct, ce = curve(A, lx, tm, TEST, 4), curve(A, lx, np.clip(em, ya, yb), TRAIN, 3.5)
        hb = DashedLine(A.c2p(1, bay), A.c2p(3.5, bay), color=BAYES, stroke_width=2.5)
        hc = DashedLine(A.c2p(1, rc), A.c2p(3.5, rc), color=GREY_A, stroke_width=2)
        lab = VGroup(label(r"true risk $R(\hat h)$", font_size=20, color=TEST),
                     label(r"training error $\hat R(\hat h)$", font_size=20, color=TRAIN),
                     label(r"best threshold $R(h_{\mathcal H})$", font_size=20, color=GREY_A),
                     label(r"Bayes risk $R^*$", font_size=20, color=BAYES))
        lab[0].next_to(A.c2p(1.05, tm[0]), UP, buff=0.08).align_to(A.c2p(1.05, 0), LEFT)
        lab[1].next_to(A.c2p(1.05, max(em[0], ya)), DOWN, buff=0.08).align_to(A.c2p(1.05, 0), LEFT)
        lab[2].next_to(A.c2p(3.5, rc), UP, buff=0.05).align_to(A.c2p(3.5, 0), RIGHT)
        lab[3].next_to(A.c2p(3.5, bay), DOWN, buff=0.05).align_to(A.c2p(3.5, 0), RIGHT)
        colors = {r"R(h_{\mathcal H}) - R^*": BAYES, r"R(\hat h) - R(h_{\mathcal H})": TEST}
        dec = cmath(r"R(\hat h) - R^*", "=", r"R(h_{\mathcal H}) - R^*", "+", r"R(\hat h) - R(h_{\mathcal H})",
                    colors=colors, font_size=30).move_to([-3.3, -1.3, 0])
        braces = VGroup(brace_note(dec[2], r"approximation: \\ the family is too simple", font_size=20, color=BAYES),
                        brace_note(dec[4], r"estimation: \\ too few examples", font_size=20, color=TEST))
        n0, nN = int(ns[0]), int(ns[-1])
        with self.voiceover(
            "Now a learner. Suppose it may only use thresholds: say one if x is above t. It picks the threshold with "
            "the fewest training errors. <bookmark mark='a'/> From forty points, thirty times, the chosen threshold "
            f"jumps around the best one. <bookmark mark='b'/> Average over {r['draws']} samples at each size. With "
            f"{n0} examples, the training error is {100 * em[0]:.0f} percent, but the true risk of the chosen rule "
            f"is {100 * tm[0]:.0f}: the training error is optimistic, because the rule was picked to look good on "
            f"exactly those points. <bookmark mark='c'/> With {nN:,}, both settle near {100 * rc:.1f} percent, the best "
            f"threshold's risk, and stay above the Bayes risk, {100 * bay:.1f}. <bookmark mark='d'/> That splits "
            "the excess risk in two: approximation, because no threshold can draw an interval, and estimation, "
            "because the sample is finite. More data shrinks only the second; a richer family shrinks the first, and "
            "the rest of this part is about what it costs the second."
        ) as vo:
            self.play(FadeIn(g), Create(c1), Create(c0), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(best), LaggedStart(*[Create(m) for m in tl], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(G), FadeIn(cb), Create(ct), Create(ce), FadeIn(lab[0]), FadeIn(lab[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(hc), Create(hb), FadeIn(lab[2]), FadeIn(lab[3]))
            vo.wait_until("d")
            self.play(Write(dec))
            self.play(FadeIn(braces))
        self.wait(0.3)
        self.clear_scene()
