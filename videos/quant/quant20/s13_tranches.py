from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, EQT, MEZZ, PART, SENIOR, ask, fit_right, illustration, load


class Tranches(VoiceoverScene):
    def construct(self):
        c = load("copula")
        self.card()
        self.waterfall()
        self.el(c)
        self.base(c)

    def card(self):
        c = chapter_card(12, r"CDOs and tranches", r"Who loses first?", part=PART)
        with self.voiceover("Chapter twelve. Tranches: slicing a pool's losses by who bears them first."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def waterfall(self):
        H, W = 5.0, 2.4
        x0, y0 = -3.6, -2.4
        cuts = [(0, 0.03, EQT, r"equity 0--3\%"), (0.03, 0.07, MEZZ, r"mezzanine 3--7\%"),
                (0.07, 0.15, QC.SPOT, r"senior 7--15\%"), (0.15, 0.30, SENIOR, r"super senior 15--30\%")]
        scale = H / 0.30
        blocks = VGroup()
        for a, d, c_, t in cuts:
            r_ = Rectangle(width=W, height=(d - a) * scale, stroke_color=WHITE, stroke_width=1.5, fill_color=c_,
                           fill_opacity=0.35).move_to([x0, y0 + (a + d) / 2 * scale, 0])
            blocks.add(VGroup(r_, label(t, font_size=19).next_to(r_, RIGHT, buff=0.25)))
        loss = Rectangle(width=W, height=0.01, stroke_width=0, fill_color=BAD, fill_opacity=0.85).move_to(
            [x0, y0, 0], aligned_edge=DOWN)
        tracker = ValueTracker(0.0)
        loss.add_updater(lambda m: m.stretch_to_fit_height(max(tracker.get_value() * scale, 0.01)).move_to(
            [x0, y0, 0], aligned_edge=DOWN))
        val = always_redraw(lambda: MathTex(rf"\text{{pool loss}} = {100 * tracker.get_value():.1f}\%", font_size=30,
                                            color=BAD).move_to([3.6, 1.6, 0]))
        side = wrapped_label(r"each tranche is a slice of the pool's losses: the equity takes the first 3\%, the "
                             r"mezzanine the next 4\%, and so on. A tranche's spread pays for its own slice only. "
                             r"Index tranches on CDX and iTraxx traded on exactly these points", 4.4, 18,
                             GREY_A).move_to([3.6, -0.6, 0])
        with self.voiceover(
            "A collateralized debt obligation pools many credits and sells their losses in slices. "
            "<bookmark mark='a'/> The equity tranche absorbs the first three percent of losses; the mezzanine the next "
            "four; then the senior and super-senior slices. <bookmark mark='b'/> Let losses pile up. Up to three "
            "percent, only the equity pays. Beyond it, the equity is gone and the mezzanine starts to lose. The "
            "senior tranches are touched only when losses are large, which takes many defaults at once."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in blocks], lag_ratio=0.3), FadeIn(side))
            vo.wait_until("b")
            self.add(loss, val)
            self.play(tracker.animate.set_value(0.05), run_time=3)
            self.play(tracker.animate.set_value(0.11), run_time=3)
        loss.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def el(self, c):
        rh = np.asarray(c["rhos"])
        cols = {"equity 0-3%": EQT, "mezzanine 3-7%": MEZZ, "senior 15-30%": SENIOR}
        g = axes([0, 0.9], [0, 0.45], x_length=7.4, y_length=4.4, xlabel=r"correlation $\rho$",
                 ylabel=r"expected loss, \% of the tranche", xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[0, 0.1, 0.2, 0.3, 0.4],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lines = VGroup(*[curve(ax, rh, np.clip(np.asarray(c["el"][k]), 0, 0.45), c_, stroke_width=3.5)
                         for k, c_ in cols.items()])
        side = VGroup(
            legend([(EQT, r"equity 0--3\%"), (MEZZ, r"mezzanine 3--7\%"), (SENIOR, r"senior 15--30\%")], font_size=17),
            label(r"large pool, PD 2\% a year, recovery 40\%", font_size=18, color=GREY_A),
            wrapped_label(r"correlation moves loss from the equity to the senior tranche: equity holders are long "
                          r"correlation, senior holders short it. The mezzanine is not even monotone", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "What does each slice expect to lose, as the correlation varies? <bookmark mark='a'/> The equity's "
            "expected loss falls as correlation rises: correlated names tend to survive together, sparing the first "
            "loss. <bookmark mark='b'/> The senior tranche's rises from almost nothing: correlated names also fail "
            "together, and only then does loss reach it. The pool's total expected loss never changes; correlation "
            "only moves it between the slices. So a tranche is a position in correlation."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines[2]), FadeIn(side[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def base(self, c):
        dets, base = np.asarray(c["dets"]) * 100, np.asarray(c["base"])
        g = axes([0, 32], [0, 0.7], x_length=7.0, y_length=4.2, xlabel=r"detachment point, \%",
                 ylabel=r"base correlation", xticks=[3, 7, 10, 15, 30], yticks=[0, 0.2, 0.4, 0.6], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = VGroup(curve(ax, dets, base, BAD, stroke_width=3.5),
                      *[Dot(ax.c2p(a, b), color=BAD) for a, b in zip(dets, base)])
        (r1, w1), (r2, w2) = c["mix"]
        side = VGroup(
            wrapped_label(rf"a 'market' with two states: correlation {r1:g} with probability {w1:g}, {r2:g} with "
                          rf"{w2:g}. Price each $[0, d]$ tranche there, then find the one flat Gaussian correlation that "
                          r"matches it", 3.8, 18, GREY_A),
            wrapped_label(r"no single correlation fits every tranche: the skew is the Gaussian copula's admission that "
                          r"it is the wrong model. Desks interpolated it anyway, and priced bespoke tranches off the "
                          r"interpolation (Andersen and Sidenius, 2004, among the fixes)", 3.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "If the Gaussian copula were right, one correlation would price every tranche. Suppose instead the world "
            "has a calm state and a systemic one, and price each tranche from zero up to a detachment point there. "
            "<bookmark mark='a'/> Then ask what single Gaussian correlation matches each price. The answers rise "
            f"with seniority, from {base[0]:.2f} for the equity to {base[-1]:.2f} for the thirty-percent slice: a "
            "base-correlation skew, like the volatility smile of Part eleven, and for the same reason. The model is "
            "wrong, and the skew is how traders patched it, right up until 2007."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[1]), run_time=2)
        q = ask(r"an equity tranche and a senior tranche on the same pool. Correlation rises overnight. Which one gained?")
        with self.voiceover("An equity tranche and a senior tranche on the same pool. Correlation rises overnight. Which "
                            "one gained?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
