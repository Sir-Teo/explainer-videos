from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import CASH, GAIN, OPT, PART, SPOT, THE, load


class American(VoiceoverScene):
    def construct(self):
        d = load("tree")
        self.card()
        self.calls()
        self.puts(d)
        self.boundary(d)

    def card(self):
        c = chapter_card(10, r"Early exercise", r"When should you stop waiting?", lit=(1979,), part=PART)
        with self.voiceover("Chapter ten. Early exercise."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def calls(self):
        rows = VGroup(
            MathTex(r"C_{\text{American}}", r"\;\ge\;", r"C_{\text{European}}", r"\;\ge\;", r"S - K e^{-rT}",
                    r"\;>\;", r"S - K", font_size=42),
            label(r"alive, a call is worth more than exercised: never exercise early (no dividends)",
                  font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.4).shift(UP * 1.3)
        rows[0][2].set_color(OPT)
        rows[0][4].set_color(CASH)
        rows[0][6].set_color(GAIN)
        put = VGroup(
            MathTex(r"P_{\text{American}} = \max\big(\,K - S,\ \text{value of waiting}\,\big)", font_size=40,
                    color=OPT),
            label(r"a deep put: exercise, take $K$ now, and earn interest on it", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.35).next_to(rows, DOWN, buff=0.9)
        with self.voiceover(
            "European options can be exercised only at expiry. Most traded stock options are American: they can be "
            "exercised any day. Is that right worth anything? For a call on a stock that pays no dividends, no. "
            "Parity bounds a call below by the stock minus the discounted strike, which is more than the stock "
            "minus the strike: alive, the call is always worth more than exercised. Robert Merton proved it in "
            "1973. <bookmark mark='a'/> A put is different. Exercising a deep in-the-money put hands you the strike "
            "now, and cash earns interest; waiting keeps the chance of an even lower price, but that chance is "
            "worth little when the put is already deep. At some price, stopping beats waiting. Which price is a "
            "problem of optimal stopping, the subject of Part eight, and it has no closed form."
        ) as vo:
            self.play(Write(rows[0]), run_time=2)
            self.play(FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(put, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def puts(self, d):
        spots = np.asarray(d["spots"], float)
        am, eu = np.asarray(d["am_curve"], float), np.asarray(d["eu_curve"], float)
        g = axes([60, 140], [0, 42], x_length=7.6, y_length=4.4, xlabel=r"stock price $S$",
                 ylabel=r"put value, one year to expiry", xticks=[60, 80, 100, 120, 140], yticks=[0, 20, 40],
                 font_size=20).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        payoff = curve(ax, [60, 100, 140], [40, 0, 0], GREY_B, stroke_width=2.5)
        eu_l = curve(ax, spots, eu, THE, stroke_width=3.5)
        am_l = curve(ax, spots, am, OPT, stroke_width=4)
        prem = Polygon(*[ax.c2p(s, a) for s, a in zip(spots, am)], *[ax.c2p(s, e) for s, e in zip(spots[::-1],
                                                                                                eu[::-1])],
                       stroke_width=0, fill_color=OPT, fill_opacity=0.25)
        leg = legend([(OPT, r"American (tree, 600 steps)"), (THE, r"European (formula)"),
                      (GREY_B, r"exercise now: $K - S$")], font_size=22).next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        nums = VGroup(
            label(r"at $S = K = 100$:", font_size=26, color=GREY_A),
            MathTex(rf"\text{{American}}\ {d['american_put']:.4f}", font_size=32, color=OPT),
            MathTex(rf"\text{{European}}\ {d['european_put']:.4f}", font_size=32, color=THE),
            MathTex(rf"\text{{early-exercise premium}}\ {d['american_put'] - d['european_put']:.4f}", font_size=28,
                    color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(leg, DOWN, buff=0.6).align_to(leg, LEFT)
        params = note(r"$K = 100$, $T = 1$, $\sigma = 20\%$, $r = 5\%$", font_size=20).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The tree of chapter four solves it. At every node, the put is worth the larger of exercising now and "
            "the discounted risk-neutral average of the two nodes after it: wait only if waiting is worth more. "
            "Here is the result for a one-year put with a five percent interest rate. The European put, in blue, "
            "dips below its payoff for deep prices: alive, it is worth less than exercised, because of the "
            "interest. <bookmark mark='a'/> The American put, in magenta, never does: it meets the payoff and runs "
            f"along it. At the money it is worth {d['american_put']:.4f} against the European "
            f"{d['european_put']:.4f}: an early-exercise premium of "
            f"{d['american_put'] - d['european_put']:.2f}, the shaded gap. The tree's value matches the "
            "textbook benchmark for this option to four digits."
        ) as vo:
            self.play(FadeIn(g), Create(payoff), FadeIn(params), FadeIn(leg[2]))
            self.play(Create(eu_l), FadeIn(leg[1]))
            vo.wait_until("a")
            self.play(Create(am_l), FadeIn(leg[0]))
            self.play(FadeIn(prem), FadeIn(nums, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def boundary(self, d):
        t = np.asarray(d["boundary_t"], float)
        b = np.asarray(d["boundary"], float)
        ok = np.isfinite(b)
        t, b = t[ok], b[ok]
        # the tree's boundary moves in lattice steps; draw it through the points where it steps
        ch = np.flatnonzero(np.diff(b)) + 1
        t = np.concatenate([[t[0]], t[ch], [1.0]])
        b = np.concatenate([[b[0]], b[ch], [100.0]])
        g = axes([0, 1], [60, 102], x_length=7.0, y_length=4.6, xlabel=r"time (years)",
                 ylabel=r"stock price", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[60, 80, 100], font_size=20)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, t, b, OPT, stroke_width=4, smooth=True)
        region = Polygon(*[ax.c2p(x, y) for x, y in zip(t, b)], ax.c2p(t[-1], 60), ax.c2p(t[0], 60), stroke_width=0,
                         fill_color=OPT, fill_opacity=0.22)
        k_line = DashedLine(ax.c2p(0, 100), ax.c2p(1, 100), color=QC.STRIKE, stroke_width=1.2)
        lab_ex = label(r"exercise", font_size=30, color=OPT).move_to(ax.c2p(0.45, 68))
        lab_wait = label(r"wait", font_size=30, color=GREY_A).move_to(ax.c2p(0.45, 94))
        side = VGroup(
            label(r"the free boundary $S^*(t)$", font_size=28, color=OPT),
            label(rf"a year out: \${b[0]:.1f}; at expiry: \$100", font_size=24, color=GREY_A),
            label(r"no formula; trees, PDEs (Part 16),", font_size=24, color=GREY_B),
            label(r"regression Monte Carlo (Longstaff--Schwartz)", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        if side.width > 4.6:
            side.scale_to_fit_width(4.6).to_edge(RIGHT, buff=0.4)
        div = wrapped_label(r"Dividends change the call's answer: just before an ex-dividend date, exercising a deep "
                            r"call to collect the dividend can beat waiting.", 4.4, 22, GREY_A)
        div.next_to(side, DOWN, buff=0.5).align_to(side, LEFT)
        with self.voiceover(
            "The tree also draws where exercise begins. For each time, the highest stock price at which "
            "exercising is optimal: the early-exercise boundary. Below it, exercise; above it, wait. A year out, the "
            f"put should be exercised only if the stock has fallen to about {b[0]:.0f}; as expiry approaches, the "
            "boundary rises towards the strike, because there is less time for waiting to pay. "
            "<bookmark mark='a'/> The boundary is part of the solution, not an input to it: the equation holds in "
            "the wait region, the payoff holds in the exercise region, and the price and its slope must join "
            "smoothly across the line. Problems like this are called free-boundary problems; they have no closed "
            "form, and desks solve them with trees, with the finite-difference methods of Part sixteen, or with "
            "regression Monte Carlo. And dividends bring calls back into the game: just before a stock goes ex "
            "dividend, exercising a deep call to collect the dividend can beat waiting."
        ) as vo:
            self.play(FadeIn(g), Create(k_line))
            self.play(Create(line), run_time=2)
            self.play(FadeIn(region), FadeIn(lab_ex), FadeIn(lab_wait), FadeIn(side[:2]))
            vo.wait_until("a")
            self.play(FadeIn(side[2:]))
            self.play(FadeIn(div))
        self.wait(0.4)
        self.clear_scene()
