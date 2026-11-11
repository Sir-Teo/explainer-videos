from __future__ import annotations

from videos.quant.quant20.common import lesson_cards

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, EQT, MEZZ, PART, SENIOR, ask, fit_right, illustration, load


class Tranches(VoiceoverScene):
    def construct(self):
        c = load("copula")
        self.card()
        self.waterfall()
        self.el(c)
        self.recovery(load("recovery"))
        self.base(c)
        self.feedback()

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
        side = wrapped_label('illustrative attachments: equity absorbs 0--3\\% and mezzanine 3--7\\% of pool loss. CDX and iTraxx schedules differ; a running spread prices both legs, not horizon expected loss alone', 4.4, 18,
                             GREY_A).move_to([3.6, -0.6, 0])
        with self.voiceover(
            "A collateralized debt obligation pools many credits and sells their losses in slices. "
            "<bookmark mark='a'/> The equity tranche absorbs the first three percent of losses; the mezzanine the next "
            "four; then the senior and super-senior slices. <bookmark mark='b'/> Let losses pile up. Up to three "
            "percent, only the equity pays. Beyond it, the equity is gone and the mezzanine starts to lose. The "
            "senior tranches are touched only when losses are large, which takes many defaults at once."
        ) as vo:
            self.play(FadeIn(blocks), FadeIn(side))
            vo.wait_until("a")
            self.play(Indicate(blocks[0]), Indicate(blocks[1]))
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
        g = axes([0, 0.9], [0, 45], x_length=7.4, y_length=4.4, xlabel=r"correlation $\rho$",
                 ylabel=r"expected loss, \% of the tranche", xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[0, 10, 20, 30, 40],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lines = VGroup(*[curve(ax, rh, 100 * np.asarray(c["el"][k]), c_, stroke_width=3.5)
                         for k, c_ in cols.items()])
        side = VGroup(
            legend([(EQT, r"equity 0--3\%"), (MEZZ, r"mezzanine 3--7\%"), (SENIOR, r"senior 15--30\%")], font_size=17),
            label(r"large pool, PD 2\% a year, recovery 40\%", font_size=18, color=GREY_A),
            wrapped_label('fixed-marginal Gaussian example: equity expected loss falls as dependence increases. A bounded senior tranche need not be monotone. Protection-side signs differ; horizon expected loss is not a complete price', 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here the pool is homogeneous, the marginal default probability and recovery are fixed, and the Gaussian common factor changes dependence. <bookmark mark='a'/> Equity first-loss expected loss falls as dependence concentrates more probability on joint survival and severe joint default. <bookmark mark='b'/> The displayed fifteen-to-thirty-percent tranche is more exposed to the tail over much of this example, but a bounded senior tranche need not be monotone for every parameter: its payoff is a difference of two stop-loss functions. Super-senior stop-loss behavior and a capped tranche are different questions. Total pool expected loss stays fixed. Correlation sensitivities also depend on whether one buys or sells protection, and loss comparisons at a horizon are not complete running-spread prices. The two thousand five correlation episode illustrates the danger of relying on unstable tranche hedges, rather than a universal rule that every pair must lose together."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines[2]), FadeIn(side[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def recovery(self, r):
        names = ["equity 0-3%", "mezzanine 3-7%", "senior 15-30%"]
        hx = [-4.4, -1.4, 1.3, 4.2]
        heads = [r"tranche", r"recovery fixed at 40\%", r"recovery falls in bad times", 'loss sensitivity']
        rows = VGroup(VGroup(*[label(h_, font_size=18, color=GREY_A).move_to([x, 2.0, 0]) for h_, x in zip(heads, hx)]))
        cols = [EQT, MEZZ, SENIOR]
        for i, (n_, c_) in enumerate(zip(names, cols)):
            y = 1.2 - 0.75 * i
            f, q, d = r["fixed"][n_], r["random"][n_], r["delta"][n_]
            fmt = (lambda v: rf"{1e4 * v:.1f}\ \text{{bp}}") if f < 0.001 else (lambda v: rf"{100 * v:.1f}\%")
            rows.add(VGroup(label(n_.replace("%", r"\%"), font_size=19, color=c_).move_to([hx[0], y, 0]),
                            MathTex(fmt(f), font_size=26).move_to([hx[1], y, 0]),
                            MathTex(fmt(q), font_size=26, color=BAD if q > f else WHITE).move_to([hx[2], y, 0]),
                            MathTex(f"{d:.3f}", font_size=26).move_to([hx[3], y, 0])))
        foot = wrapped_label(
            'stylized state-dependent recovery, PD 2\\%, $\\rho=0.2$: default-weighted mean recovery stays 40\\%, preserving pool expected loss. Loss sensitivity normalizes a PD bump by pool-loss change; it is not a complete market hedge ratio', 12.4, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"The next illustration lets recovery vary with the common factor while fixing the average recovery weighted by defaults at forty percent. That weighting keeps total expected pool loss the same; an unweighted average recovery would not suffice. <bookmark mark='a'/> The displayed senior tranche's expected loss is {r['random']['senior 15-30%'] / r['fixed']['senior 15-30%']:.1f} times the fixed-recovery value under these parameters. This is a model scenario, not an empirical multiplier for all recessions. <bookmark mark='b'/> The delta column is a finite-difference sensitivity of tranche loss to marginal pool PD, normalized by the corresponding expected pool-loss change. It is not a complete traded-index hedge ratio. Market hedging also needs premium legs, spread-curve bumps, recovery assumptions, dependence dynamics and residual basis risk."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1], r_[2])) for r_ in rows[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(*[FadeIn(r_[3]) for r_ in rows[1:]], FadeIn(foot))
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
            wrapped_label(r"no single constant correlation matches this mixture's tranche expected losses: "
                          r"interpolation need not define a valid joint loss distribution. Bespoke pricing requires checks of the "
                          r"interpolation (Andersen and Sidenius, 2004, among the fixes)", 3.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"For this example we mix two Gaussian dependence regimes: correlation point zero five with weight eighty-five percent and point eight with weight fifteen percent. This is a synthetic expected-loss construction, not a Student t calibration or observed market quote. <bookmark mark='a'/> For each zero-to-detachment tranche, solve the constant Gaussian correlation matching that expected loss. It ranges from {base[0]:.2f} at three percent detachment to {base[-1]:.2f} at thirty percent. Different detachments require different implied correlations. This is a base-correlation skew, analogous to using implied volatility as a quote coordinate. Interpolating those coordinates does not automatically define a consistent joint loss distribution or guarantee arbitrage-free bespoke prices. A full pricing exercise would also match maturities, premium legs and the risk-neutral measure."
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

    def feedback(self):
        title = wrapped_label('Answer: name the payoff and the position', 12.4, 32, QC.IDEA).to_edge(UP, buff=.6)
        answer = wrapped_label('Cash equity benefits from lower first-loss expectation under the stated ordering; protection has the opposite sign. A capped senior tranche needs its own sensitivity.', 11.8, 27, GREY_A).move_to(ORIGIN)
        with self.voiceover('Specify whether the investor holds the funded tranche or buys protection. Under the fixed-marginal homogeneous dependence comparison, cash equity benefits from a lower first-loss expectation, while equity protection has the opposite exposure. Super-senior protection responds differently. A bounded senior tranche can have a nonmonotone response, and a complete mark-to-market also includes premium legs and the fitted dependence surface.') as vo:
            self.play(FadeIn(title), FadeIn(answer))
        self.wait(.5)
        self.clear_scene()
