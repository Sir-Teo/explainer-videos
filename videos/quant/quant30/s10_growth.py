from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EST_C, GOOD, HURDLE, PART, REAL_C, RP_C, SHRINK_C, TRUE_C, fit_right, load


class Growth(VoiceoverScene):
    def construct(self):
        g = load("growth")
        self.card()
        self.kelly(g)
        self.curve_(g)
        self.fractional(g)
        self.cover_math()
        self.cover(g)
        self.regret(g)
        self.fernholz(g)
        self.excess()
        self.question()

    def card(self):
        c = chapter_card(9, r"Kelly, Cover and Fernholz", r"What if the goal is not the best trade-off between mean and "
                         r"variance, but the fastest growth of wealth?", part=PART)
        with self.voiceover("Chapter nine. Mean-variance is a one-period idea. An investor who reinvests for decades cares "
                            "about something else: how fast wealth compounds. Three answers, from three traditions."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def kelly(self, g):
        rows = [cmath(r"g(w)", r"=", r"r + w^\top\mu - \tfrac12 w^\top\Sigma w", font_size=34, colors={r"g(w)": TRUE_C}),
                cmath(r"w^*", r"=", r"\Sigma^{-1}\mu", font_size=36, colors={r"w^*": TRUE_C}),
                cmath(r"f^*_{\text{market}}", r"=", rf"\frac{{\mu_m}}{{\sigma_m^2}} = \frac{{{100 * g['mu']:.1f}\%}}"
                      rf"{{{100 * g['s2']:.2f}\%}} = {g['kelly']:.2f}", font_size=30, colors={r"f^*_{\text{market}}": HURDLE})]
        whys = [why(r"the expected log growth rate of a constantly rebalanced portfolio in continuous time "
                    r"($\mu$: excess returns)"),
                why(r"Kelly (1956), Breiman (1961): maximising it gives the portfolio that, with probability one, "
                    r"maximises asymptotic growth under a specified stationary admissible model; not a finite-horizon guarantee"),
                why('US market, 1970--2020: fitted diffusion moments imply leverage 2.82; this is retrospective, not known future Kelly leverage')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"""Kelly under a specified model. <bookmark mark='a'/> For self-financing constant risky exposures in a continuous diffusion with constant known excess drift and covariance, log-growth rate is risk-free growth plus mean minus half variance. <bookmark mark='b'/> Positive-definite covariance gives inverse Sigma times mu as the growth optimum among this admissible class. Long-run comparisons need stationarity and integrability; universal finite-time domination is not implied. <bookmark mark='c'/> Plugging the research sample's market moments into that model gives leverage {g['kelly']:.2f}. This is a retrospective fitted quantity, not known future Kelly leverage."""
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

    def curve_(self, g):
        fs = np.asarray(g["fs"], float)
        th = 100 * np.asarray(g["g_theory"], float)
        em = 100 * np.asarray(g["g_emp"], float)
        lo = float(np.floor(np.nanmin(np.r_[th, em]) / 5) * 5)
        hi = float(np.ceil(np.nanmax(np.r_[th, em]) / 5) * 5)
        gr = axes([0, 4], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"fraction of wealth in the market (leverage)",
                  ylabel=r"growth rate of wealth, \% a year", xticks=[0, 1, 2, 3, 4], yticks=[lo, 0, hi], font_size=15
                  ).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = gr.ax
        lt, le = curve(ax, fs, th, TRUE_C, stroke_width=3), curve(ax, fs, em, REAL_C, stroke_width=3)
        k = float(g["kelly"])
        kl = DashedLine(ax.c2p(k, lo), ax.c2p(k, hi), color=HURDLE, stroke_width=2)
        leg = legend([(TRUE_C, r"$r + f\mu - f^2\sigma^2/2$"), (REAL_C, r"the actual monthly path, rebalanced")],
                     font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label('in the quadratic diffusion model, twice fitted Kelly returns to risk-free growth; discrete-path solvency, financing and drift estimation require separate analysis',
                             3.4, 15, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        i_emp = int(np.nanargmax(em))
        f_emp = fs[i_emp]
        with self.voiceover(
            f"""Compare a diffusion approximation with a historical discrete path. <bookmark mark='a'/> The quadratic peaks at the fitted Kelly leverage. <bookmark mark='b'/> The monthly log-wealth calculation over the displayed leverage grid peaks at {f_emp:.2f}; only solvent grid points have finite log growth. Twice Kelly returns to risk-free growth in the quadratic model, not necessarily in the discrete realised path. Estimation, financing and left-tail solvency can favour smaller exposure, but there is no universal half-Kelly prescription."""
        ) as vo:
            self.play(FadeIn(gr), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(lt), Create(kl))
            vo.wait_until("b")
            self.play(Create(le), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def fractional(self, g):
        import math
        sr2 = g["mu"] ** 2 / g["s2"]
        c51 = sr2 / (sr2 + 1 / 51)
        c5 = sr2 / (sr2 + 1 / 5)
        rows = [cmath(r"\hat f", r"=", r"c\,\hat\mu/\sigma^2,\quad \hat\mu \sim N(\mu,\ \sigma^2/T)", font_size=32,
                      colors={r"\hat f": HURDLE}),
                cmath(r"\mathbb E[g(\hat f)-r]", r"=", r"c\,\frac{\mu^2}{\sigma^2} - \frac{c^2}{2}\,\frac{\mu^2 + \sigma^2/T}{\sigma^2}",
                      font_size=30),
                cmath(r"c^*", r"=", r"\frac{SR^2}{SR^2 + 1/T}", font_size=36, colors={r"c^*": GOOD}),
                cmath(r"SR = " + f"{math.sqrt(sr2):.2f}", r":", rf"c^* = {c51:.2f}\ (T = 51\ \text{{years}}),\quad "
                      rf"{c5:.2f}\ (T = 5)", font_size=30)]
        whys = [why(r"bet a fraction $c$ of the Kelly leverage computed from an estimated mean ($T$ years of data)"),
                why(r"the expected growth rate, averaging over the estimation error: the error adds $\sigma^2/T$ to the "
                    r"squared mean in the penalty"),
                why(r"the best fraction of Kelly: always below one, and lower the shorter the history"),
                why(r"the US market's Sharpe ratio, 1970--2020: with five years of data, the plug-in model fraction is illustrative, not an identified optimum")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            f"""A scalar estimation-risk calculation. <bookmark mark='a'/> Assume known variance and an independent unbiased Gaussian mean estimate with variance sigma squared over T, in consistent annual units. <bookmark mark='b'/> Substituting a fixed fraction c into the quadratic growth model adds that estimation variance to the penalty. The displayed growth is excess over cash. <bookmark mark='c'/> The optimal fraction is true squared Sharpe divided by true squared Sharpe plus one over T. It is not feasible without knowing or estimating true strength. <bookmark mark='d'/> Substituting the historical fitted market strength gives {c51:.2f} at fifty-one years and {c5:.2f} at five. These are illustrative plugs into the model, not optimal allocations certified by the data."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def cover_math(self):
        rows = [cmath(r"S_n(b)", r"=", r"\textstyle\prod_{t \le n} b^\top x_t", font_size=34, colors={r"S_n(b)": RP_C}),
                cmath(r"\hat b_{n+1}", r"=", r"\frac{\int b\,S_n(b)\,db}{\int S_n(b)\,db}", font_size=34,
                      colors={r"\hat b_{n+1}": RP_C}),
                cmath(r"\frac{\max_b S_n(b)}{\hat S_n}", r"\le", r"(n + 1)^{m - 1}", font_size=34,
                      colors={r"\frac{\max_b S_n(b)}{\hat S_n}": HURDLE})]
        whys = [why(r"the wealth of the constant-rebalanced portfolio $b$ on the price relatives $x_t$"),
                why('Cover (1991): performance-weight all constant mixes under frictionless rebalancing; no probabilistic return model is required'),
                why('continuous uniform mixture, strictly positive price relatives: the wealth ratio to the best constant mix is polynomially bounded; the saved grid has a different comparator')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The second answer needs no model at all. <bookmark mark='a'/> Consider every constant-rebalanced mix of the "
            "assets, and its wealth so far. <bookmark mark='b'/> Thomas Cover's universal portfolio of 1991 holds their "
            "average, weighted by how well each has done. <bookmark mark='c'/> And he proved that its wealth trails the "
            "best mix chosen in hindsight by at most a polynomial factor in time: it grows at the same exponential rate "
            "as the best constant mix, whatever the market does."
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

    def cover(self, g):
        cv = g["cover"]
        b = np.asarray(cv["b"], float)
        W = np.log(np.asarray(cv["wealth"], float))
        lo, hi = float(np.floor(W.min())), float(np.ceil(W.max()))
        gr = axes([0, 1], [lo, hi], x_length=7.0, y_length=4.2, xlabel=rf"share in {cv['pair'][0]}, the rest in "
                  rf"{cv['pair'][1]}, rebalanced monthly", ylabel=r"log of final wealth, 1970--2020",
                  xticks=[0, 0.5, 1], yticks=[lo, hi], font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = gr.ax
        line = curve(ax, b, W, RP_C, stroke_width=3)
        uni = DashedLine(ax.c2p(0, math.log(cv["uni"][-1])), ax.c2p(1, math.log(cv["uni"][-1])), color=GOOD, stroke_width=2)
        ratio = cv["best"][-1] / cv["uni"][-1]
        side = VGroup(MathTex(rf"\text{{best mix}}: b = {cv['b_best']:.2f},\ \times{cv['best'][-1]:.0f}", font_size=22,
                              color=RP_C),
                      MathTex(rf"\text{{universal}}: \times{cv['uni'][-1]:.0f}", font_size=22, color=GOOD),
                      MathTex(rf"\text{{grid ratio}}\ {ratio:.2f} \le {len(cv['b'])}", font_size=22, color=HURDLE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        fit_right(side)
        with self.voiceover(
            f"""A finite-mixture illustration on {cv['pair'][0]} and {cv['pair'][1]}. <bookmark mark='a'/> The saved computation uses a fixed grid of {len(cv['b'])} constant monthly rebalanced mixes. The best grid mix in hindsight assigns {100 * cv['b_best']:.0f} percent to gold and multiplies wealth {cv['best'][-1]:.0f} times. <bookmark mark='b'/> Uniformly averaging those grid portfolios yields {cv['uni'][-1]:.0f} times, a ratio {ratio:.2f}. Since the mixture contains its best grid component with weight one over {len(cv['b'])}, their wealth ratio cannot exceed {len(cv['b'])}. This finite-mixture bound differs from Cover's continuous-uniform two-asset bound n plus one, here {cv['bound']}. Neither includes trading costs or guarantees beating buy-and-hold in every path."""
        ) as vo:
            self.play(FadeIn(gr))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
            vo.wait_until("b")
            self.play(Create(uni), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def regret(self, g):
        import math
        n = g["cover"]["n"]
        per = math.log(n + 1) / n
        rows = [cmath(r"\frac1n\log\frac{\max_b S_n(b)}{\hat S_n}", r"\le", r"\frac{(m - 1)\log(n + 1)}{n} \to 0", font_size=32,
                      colors={r"\frac1n\log\frac{\max_b S_n(b)}{\hat S_n}": HURDLE}),
                cmath(rf"m = 2,\ n = {n}", r":", rf"\le {100 * per:.2f}\%\ \text{{a month in growth rate}}", font_size=30),
                cmath(r"\text{the price}", r":", r"\text{no forecast, but no better than the best constant mix}", font_size=30)]
        whys = [why('continuous uniform mixture: the per-period log gap to the best constant mix vanishes for positive price relatives and frictionless rebalancing'),
                why('for 612 months this continuous bound is 1.05\\% monthly; the saved 201-point mixture instead competes with its grid best'),
                why(r"it competes with hindsight among constant mixes only; for many assets the bound grows with $m$ and "
                    r"the integral over mixes becomes expensive")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"""Two comparison classes. <bookmark mark='a'/> For a continuous uniform mixture over long-only constant mixes with strictly positive price relatives and frictionless rebalancing, Cover's polynomial wealth bound gives a per-period log gap tending to zero. <bookmark mark='b'/> For two assets and {n} months that continuous bound is {100 * per:.2f} percent monthly; the saved grid computation instead has the separate finite-mixture bound just shown. <bookmark mark='c'/> A fixed grid competes with its grid best, not every continuous weight. Neither result compares with arbitrary dynamic foresight strategies, and costs can change the conclusion."""
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

    def fernholz(self, g):
        sp = g["spt"]
        d = np.asarray(sp["dates"], float)
        x = d // 100 + ((d % 100) - 0.5) / 12
        rel = 100 * (np.asarray(sp["cum_div"]) - np.asarray(sp["cum_mkt"]))
        lo, hi = float(np.floor(min(rel.min(), 0) / 5) * 5), float(np.ceil(max(rel.max(), 0) / 5) * 5)
        gr = axes([x[0], x[-1]], [lo, hi], x_length=8.6, y_length=3.8, xlabel=r"",
                  ylabel=r"diversity-weighted minus cap-weighted, cumulative log return, \%", xticks=[1970, 1990, 2010, 2020],
                  yticks=[lo, 0, hi], xfmt=lambda v: f"{v:.0f}", font_size=14).move_to(LEFT * 0.6 + DOWN * 0.5)
        ax = gr.ax
        line = curve(ax, x, rel, SHRINK_C, stroke_width=3)
        zero = DashedLine(ax.c2p(x[0], 0), ax.c2p(x[-1], 0), color=GREY_B, stroke_width=1.2)
        eq = MathTex(r"w_i \propto \mu_i^{\,p},\ p = \tfrac12;\qquad \log\frac{V_{\text{div}}}{V_{\text{mkt}}} = "
                     r"\log\frac{D_p(\mu_T)}{D_p(\mu_0)} + (1 - p)\int_0^T\gamma^*_{\pi,t}\,dt", font_size=26).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"""Fernholz's continuous-time stochastic portfolio theory is a different result. <bookmark mark='a'/> Positive market weights raised to p below one tilt toward smaller names. Under a continuous self-financing model, the generating-function identity separates the change in diversity from an accumulated excess-growth term. A bounded adverse change in diversity and sufficient nondegeneracy are additional conditions for long-horizon relative outperformance. <bookmark mark='b'/> The saved monthly industry-cap proxy records average relative log return {100 * sp['excess']:.1f} percent annually. Broad retrospective baskets, discrete rebalancing and omitted costs make this an illustration, not a verification of continuous-time relative arbitrage."""
        ) as vo:
            self.play(FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(gr), Create(zero))
            vo.wait_until("b")
            self.play(Create(line), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def excess(self):
        rows = [cmath(r"\gamma^*_\pi", r"=", r"\tfrac12\Big(\textstyle\sum_i \pi_i\sigma_{ii} - \sigma_{\pi\pi}\Big)", font_size=34,
                      colors={r"\gamma^*_\pi": SHRINK_C}),
                cmath(r"\gamma^*_\pi", r"\ge", r"0", font_size=36, colors={r"\gamma^*_\pi": SHRINK_C}),
                cmath(r"\log V_\pi", r"=", r"\textstyle\sum_i \pi_i \log X_i + \int_0^t \gamma^*_\pi\,ds\ \ "
                      r"\text{(constant weights)}", font_size=28)]
        whys = [why(r"the excess growth rate: half the gap between the average variance of the holdings and the "
                    r"variance of the portfolio"),
                why('nonnegative for long-only fully invested weights and PSD covariance; positive if a held pair has positive weights and nonzero relative variance'),
                why('for constant weights this compares portfolio log wealth with weighted log price relatives; it does not guarantee positive absolute or market-relative returns')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The excess-growth identity in continuous time. <bookmark mark='a'/> For nonnegative fully invested weights and a positive-semidefinite instantaneous covariance, half the weighted individual variances minus portfolio variance equals a weighted sum of pairwise relative variances. <bookmark mark='b'/> It is nonnegative; strict positivity needs positive weight on a pair with nonzero relative variance, rather than merely unequal volatility labels. <bookmark mark='c'/> With constant weights, normalised log portfolio wealth equals the weighted log asset-price relatives plus accumulated excess growth. The term is relative to that weighted log benchmark, not a guarantee of positive absolute or market-relative returns after costs."
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

    def question(self):
        q = pause_card(r"an investor bets twice the Kelly fraction. What is the quadratic-model growth rate relative to the risk-free "
                       r"rate, and why?")
        with self.voiceover(
            "Pause and predict. An investor bets twice the Kelly fraction. What is the growth rate, and why?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
