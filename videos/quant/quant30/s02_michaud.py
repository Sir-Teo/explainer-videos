from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EST_C, GOOD, HURDLE, PART, REAL_C, TRUE_C, fit_right, illustration, load


class Michaud(VoiceoverScene):
    def construct(self):
        m = load("michaud")
        self.card()
        self.recipe()
        self.sensitivity(m)
        self.frontiers(m)
        self.cloud(m)
        self.longer(m)
        self.resample(m)
        self.why_()
        self.question()

    def card(self):
        c = chapter_card(1, r"Error maximisation", r"What does the optimizer do with the errors in its inputs?", part=PART)
        with self.voiceover("Chapter one. Markowitz gave us the recipe in 1952: feed in expected returns and covariances, "
                            "and out comes the best portfolio. What does the optimizer do with the errors in its inputs?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def recipe(self):
        rows = [cmath(r"\min_w", r"\ ", r"w^\top\Sigma w\quad \text{s.t.}\ w^\top\mu = m,\ w^\top 1 = 1", font_size=34,
                      colors={r"\min_w": TRUE_C}),
                cmath(r"w(m)", r"=", r"\Sigma^{-1}(\lambda 1 + \gamma\mu),\quad \sigma^2(m) = \frac{A m^2 - 2Bm + C}{AC - B^2}",
                      font_size=30, colors={r"w(m)": TRUE_C}),
                cmath(r"\hat w", r"=", r"w(m;\ \hat\mu, \hat\Sigma)", font_size=34, colors={r"\hat w": EST_C})]
        whys = [why(r"the least risky fully invested portfolio with mean $m$ (Markowitz 1952)"),
                why(r"Lagrange multipliers give the weights in closed form; with $A = 1^\top\Sigma^{-1}1$, "
                    r"$B = 1^\top\Sigma^{-1}\mu$, $C = \mu^\top\Sigma^{-1}\mu$ the frontier is a hyperbola (Merton 1972)"),
                why(r"in practice $\mu$ and $\Sigma$ are estimated, and the optimizer treats the estimates as the truth")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The recipe. <bookmark mark='a'/> Find the least risky fully invested portfolio with a given mean. "
            "<bookmark mark='b'/> Lagrange multipliers give the weights in closed form, and the set of best portfolios, "
            "the frontier, is a hyperbola. <bookmark mark='c'/> But the means and covariances are estimated, and the "
            "optimizer cannot tell an estimate from the truth."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def sensitivity(self, m):
        sv = m["sens"]
        rows = [cmath(r"\mu_{\text{Softw}}", r"\to", rf"\mu_{{\text{{Softw}}}} + {100 * sv['shock_year']:.1f}\%\ \text{{a year}}", font_size=34,
                      colors={r"\mu_{\text{Softw}}": EST_C}),
                cmath(r"\textstyle\sum_i|\Delta w_i|", r"=", rf"{sv['dw_l1']:.2f}", font_size=34, colors={r"\textstyle\sum_i|\Delta w_i|": BAD}),
                cmath(r"w_{\text{Softw}}", r":", rf"{sv['w0_self']:.2f}\ \to\ {sv['w0_self'] + sv['dw_self']:.2f}", font_size=34)]
        whys = [why('the normalised inverse-covariance mean direction of 49 industries, using the stipulated 1970--2020 moments; raise one mean by its five-year IID standard-error scale'),
                why(rf"the total change in the weights, against a portfolio whose gross exposure is "
                    rf"{sv['gross0']:.1f}: Best and Grauer (1991) showed how sensitive the optimum is to the means"),
                why(r"one industry-specific IID standard-error scale; joint mean errors are correlated and heterogeneous")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"""Sensitivity in a stipulated population model. <bookmark mark='a'/> Use the industries' 1970 through 2020 moments as truth, and raise software's annualised mean by {100 * sv['shock_year']:.1f} percentage points: its own sixty-month IID standard-error scale. <bookmark mark='b'/> For the normalised inverse-covariance mean direction, gross exposure starts at {sv['gross0']:.1f}, and total absolute weight change is {sv['dw_l1']:.2f}. <bookmark mark='c'/> Software moves from {sv['w0_self']:.2f} to {sv['w0_self'] + sv['dw_self']:.2f}. Other means have their own, correlated uncertainty; they do not all suffer this exact error simultaneously."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def _axes(self, m):
        pts = np.asarray(m["sims"]["60"]["pts"], float)
        rs = np.asarray(m["sims"]["60"]["resampled"], float)
        xx = np.r_[pts[:, 0], pts[:, 2], rs[:, 0], np.asarray(m["true"]), np.asarray(m["sims"]["60"]["est"]).ravel()]
        yy = np.r_[pts[:, 1], pts[:, 3], rs[:, 1], m["targets"]]
        hi = float(np.ceil((xx.max() + 0.005) / 0.02) * 0.02)
        lo_y = float(np.floor((min(yy.min(), 0) - 0.001) / 0.005) * 0.005)
        hi_y = float(np.ceil((yy.max() + 0.001) / 0.005) * 0.005)
        g = axes([0, hi], [lo_y, hi_y], x_length=7.4, y_length=4.6, xlabel=r"volatility, per month",
                 ylabel=r"expected excess return, per month", xticks=[0, hi / 2, hi], yticks=[lo_y, 0, hi_y],
                 xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.1f}\\%", font_size=15)
        return g.move_to(LEFT * 1.8 + DOWN * 0.2)

    def frontiers(self, m):
        g = self._axes(m)
        ax = g.ax
        t = np.asarray(m["targets"], float)
        true = curve(ax, np.asarray(m["true"]), t, TRUE_C, stroke_width=4)
        ests = VGroup(*[curve(ax, np.asarray(e), t, EST_C, stroke_width=1.5).set_stroke(opacity=0.6)
                        for e in m["sims"]["60"]["est"]])
        leg = legend([(TRUE_C, r"the true frontier"), (EST_C, r"frontiers estimated from 5 years")], font_size=15
                     ).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(r"the truth: the means and covariance of the 49 French industries' monthly excess returns, "
                             r"1970--2020; each estimate: 60 months simulated from it", 3.4, 15, GREY_A
                             ).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "A known-truth simulation. <bookmark mark='a'/> Declare the industries' research-period mean and covariance to be fixed Gaussian population moments; draw sixty observations per fit. The green curve uses those stipulated moments. <bookmark mark='b'/> Twelve stored estimated frontiers show how sampling changes the target-return problem. Their positions are conditional on this experiment, not a theorem that every estimated frontier must be optimistic. The axes retain the full stored coordinates."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(side), FadeIn(illustration(r"simulated from the industries")))
            vo.wait_until("a")
            self.play(Create(true), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(e) for e in ests], lag_ratio=0.1, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    def cloud(self, m):
        g = self._axes(m)
        ax = g.ax
        t = np.asarray(m["targets"], float)
        true = curve(ax, np.asarray(m["true"]), t, TRUE_C, stroke_width=4)
        pts = np.asarray(m["sims"]["60"]["pts"], float)
        rng = np.random.default_rng(0)
        idx = np.arange(len(pts))
        promise = VGroup(*[Dot(ax.c2p(p[2], p[3]), radius=0.04, color=EST_C, fill_opacity=0.6)
                           for p in pts[idx]])
        real = VGroup(*[Dot(ax.c2p(p[0], p[1]), radius=0.04, color=REAL_C,
                            fill_opacity=0.6) for p in pts[idx]])
        med = np.median(pts, axis=0)
        leg = legend([(EST_C, r"what it promises"), (REAL_C, r"what it delivers")], font_size=15).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        side = VGroup(MathTex(rf"\text{{promised}}:\ {100 * med[3]:.1f}\%\ \text{{at}}\ {100 * med[2]:.1f}\%", font_size=22,
                              color=EST_C),
                      MathTex(rf"\text{{delivered}}:\ {100 * med[1]:.2f}\%\ \text{{at}}\ {100 * med[0]:.1f}\%", font_size=22,
                              color=REAL_C),
                      wrapped_label(r"medians of 300 draws; each the portfolio targeting 1\% a month on its own "
                                    r"estimates", 3.4, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(
            leg, DOWN, buff=0.35)
        fit_right(side)
        pm, pv, dm, dv = 100 * med[3], 100 * med[2], 100 * med[1], 100 * med[0]
        ratio = med[0] / med[2]
        with self.voiceover(
            "Now ask each estimated optimizer for a portfolio earning one percent a month, and then judge it under the "
            "truth. <bookmark mark='a'/> In red, what each one promised: about one percent at a volatility of "
            f"{pv:.1f} percent, better than the true frontier allows. <bookmark mark='b'/> In teal, what it delivered: "
            f"a median of {dm:.2f} percent a month at {dv:.1f} percent volatility, {ratio:.0f} times the risk it "
            "promised, and below the true frontier. Richard Michaud called mean-variance optimization an error "
            "maximizer: it seeks out the assets whose estimates are most flattering, which are the ones most likely "
            "to be wrong."
        ) as vo:
            self.play(FadeIn(g), Create(true), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in promise], lag_ratio=0.01, run_time=2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in real], lag_ratio=0.01, run_time=2), FadeIn(side[1]),
                      FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def longer(self, m):
        a = np.median(np.asarray(m["sims"]["60"]["pts"], float), axis=0)
        b = np.median(np.asarray(m["sims"]["240"]["pts"], float), axis=0)
        hx = [-3.6, 0.4, 3.6]
        head = VGroup(label(r"median of 300 draws", font_size=18, color=GREY_B), label(r"5 years of data", font_size=18,
                                                                                     color=GREY_B),
                      label(r"20 years of data", font_size=18, color=GREY_B))
        rows = [(r"promised volatility, a month", f"{100 * a[2]:.1f}", f"{100 * b[2]:.1f}", EST_C),
                (r"true volatility", f"{100 * a[0]:.1f}", f"{100 * b[0]:.1f}", REAL_C),
                (r"true expected return (target 1\%)", f"{100 * a[1]:.2f}", f"{100 * b[1]:.2f}", REAL_C),
                (r"largest weight", f"{m['sims']['60']['maxw_median']:.2f}", f"{m['sims']['240']['maxw_median']:.2f}", GREY_A)]
        tab = VGroup(head)
        for t, x, y, col in rows:
            tab.add(VGroup(label(t, font_size=19, color=col), MathTex(x, font_size=26), MathTex(y, font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.75 * j, 0])
        foot = wrapped_label(rf"the true minimum volatility of the 49 industries is {100 * m['true_min_vol']:.1f}\% a month; "
                             r"percentages a month; the largest weight in absolute value", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"""Compare two sample sizes in the same stipulated population. <bookmark mark='a'/> Median reported volatility changes from {100 * a[2]:.1f} to {100 * b[2]:.1f} percent monthly, and model-evaluated volatility from {100 * a[0]:.1f} to {100 * b[0]:.1f}. Median largest absolute weight changes from {m['sims']['60']['maxw_median']:.2f} to {m['sims']['240']['maxw_median']:.2f}. IID means have a square-root sample-size scale, but inverse covariance and constrained optimisation losses do not share one universal rate. More observations can also mean a less stable historical regime."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def resample(self, m):
        g = self._axes(m)
        ax = g.ax
        t = np.asarray(m["targets"], float)
        true = curve(ax, np.asarray(m["true"]), t, TRUE_C, stroke_width=4)
        pts = np.asarray(m["sims"]["60"]["pts"], float)[:100]
        rs = np.asarray(m["sims"]["60"]["resampled"], float)
        plain = VGroup(*[Dot(ax.c2p(p[0], p[1]), radius=0.04, color=REAL_C,
                             fill_opacity=0.5) for p in pts])
        res = VGroup(*[Dot(ax.c2p(p[0], p[1]), radius=0.045, color=GOOD,
                           fill_opacity=0.8) for p in rs])
        mp, mr = np.median(pts, axis=0), np.median(rs, axis=0)
        leg = legend([(REAL_C, r"the plain optimizer, delivered"), (GOOD, r"resampled (30 resamples each), delivered")],
                     font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        side = wrapped_label(rf"medians: {100 * mp[0]:.1f}\% volatility for {100 * mp[1]:.2f}\% a month, against "
                             rf"{100 * mr[0]:.1f}\% for {100 * mr[1]:.2f}\%. Every resample starts from the same estimated "
                             r"moments; averaging supplies no new independent information about their error", 3.4, 15, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"""Resampling in this fixed Gaussian experiment. <bookmark mark='a'/> For the first hundred base draws, average thirty target-return portfolios fitted to resamples of each draw's estimated distribution. <bookmark mark='b'/> Median population volatility is {100 * mr[0]:.1f} percent for the resampled weights, compared with {100 * mp[0]:.1f} for their matched plain portfolios. Both negative expected returns and high-volatility outcomes remain visible. Resampling can reduce variability, but it does not supply independent information about a shared input error; this experiment does not establish a universal ranking."""
        ) as vo:
            self.play(FadeIn(g), Create(true), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in plain], lag_ratio=0.01, run_time=1.5))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in res], lag_ratio=0.01, run_time=1.5), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def why_(self):
        cards = VGroup(
            desk_question(r"errors in the means matter most", 'mean-estimation errors can be costly in specific calibrations; relative error costs depend on scale, risk aversion and covariance (Best and Grauer 1991; Chopra and Ziemba 1993)', width=12.4, font_size=19),
            desk_question(r"the inverse amplifies", '$\\Sigma^{-1}$ amplifies small-eigenvalue directions; their estimation error can strongly affect weights',
                          width=12.4, font_size=19),
            desk_question('fitted risk has repeated-sample optimism', 'under the Gaussian model, fitted GMV risk is optimistic on average; individual draws can exceed population risk', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why estimation can matter. <bookmark mark='a'/> Chopra and Ziemba study sensitivity to errors in means, variances and covariances under specified loss and calibration assumptions. Their relative-cost findings are not a universal ten-to-one conversion. <bookmark mark='b'/> Covariance inversion amplifies estimated small-eigenvalue directions; their uncertainty and portfolio exposure both matter. <bookmark mark='c'/> Selection on flattering estimates creates optimism across repeated samples, without implying every fitted portfolio or every self-report is wrong in the same direction. The research chapter states an exact narrower model."
        ) as vo:
            self.add(cards[0])
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"with 20 years of data instead of 5, will the estimated frontiers move toward the true one, and "
                       r"by how much?")
        with self.voiceover(
            "Pause and predict. With twenty years of data instead of five, how far do the estimated frontiers move "
            "toward the truth?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
