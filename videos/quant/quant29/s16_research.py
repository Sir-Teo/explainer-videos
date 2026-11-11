from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, COMB, GOOD, HURDLE, PART, TRAIN_C, VALID_C, fit_right, load

T_COL = {"250": QC.LOSS, "500": QC.DELTA, "1000": QC.GAIN}


class Research(VoiceoverScene):
    def construct(self):
        t = load("theory")
        self.card()
        self.setup_()
        self.derive()
        self.mirror()
        self.theorem()
        self.sims(t)
        self.wishart(t)
        self.marginal(t)
        self.data(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"How many alphas can you combine?", r"When does one more weak signal make an estimated "
                          r"combination worse?", part=PART)
        with self.voiceover("For the researcher: Chapter seven combined mined alphas with weights estimated from the "
                            "data. Every extra signal brings some edge and some estimation error. Exactly how do they "
                            "trade off, and when does one more alpha make the combination worse?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"r_t", r"\sim", r"N(\mu, \Sigma),\quad t = 1, \dots, T,\quad r_t \in \mathbb R^K", font_size=32,
                      colors={r"r_t": COMB}),
                cmath(r"w^*", r"=", r"\Sigma^{-1}\mu,\qquad SR_*^2 = \mu^\top\Sigma^{-1}\mu = \|\theta\|^2,\quad \theta = "
                      r"\Sigma^{-1/2}\mu", font_size=30, colors={r"w^*": GOOD}),
                cmath(r"\hat w", r"=", r"\Sigma^{-1}\hat\mu,\qquad \hat\mu = \tfrac1T\textstyle\sum_t r_t", font_size=32,
                      colors={r"\hat w": HURDLE})]
        whys = [why(r"$K$ alphas' daily long-short returns, jointly normal and independent through time"),
                why(r"the best combination and its Sharpe ratio: the length of the vector of standardised means"),
                why(r"fixed pre-specified library and known covariance; only the "
                    r"means are estimated, from $T$ days")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Isolate estimation risk in a fixed population model. <bookmark mark='a'/> The K return coordinates are IID over T observation days, jointly Gaussian with positive definite covariance and fixed means. The alpha set is specified independently of this sample; no selection, costs, constraints or regime changes are modelled. <bookmark mark='b'/> The population tangency direction is inverse covariance times the mean; its squared per-day Sharpe is the squared norm of the whitened mean theta. <bookmark mark='c'/> Use the true covariance and estimate only the mean. All Sharpe quantities in this derivation are per observation period. Estimated covariance and a selected library are additional problems, not already accounted for."
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

    def derive(self):
        rows = [cmath(r"z", r"=", r"\Sigma^{1/2}\hat w = \Sigma^{-1/2}\hat\mu = \theta + \tfrac{1}{\sqrt T}\,\varepsilon,\quad "
                      r"\varepsilon \sim N(0, I_K)", font_size=30, colors={r"z": HURDLE}),
                cmath(r"SR(\hat w)", r"=", r"\frac{\hat w^\top\mu}{\sqrt{\hat w^\top\Sigma\hat w}} = \frac{z^\top\theta}{\|z\|}",
                      font_size=32, colors={r"SR(\hat w)": GOOD}),
                cmath(r"\mathbb E\,z^\top\theta", r"=", r"\|\theta\|^2,\qquad \mathbb E\,\|z\|^2 = \|\theta\|^2 + \frac KT",
                      font_size=32),
                cmath(r"SR(\hat w)", r"\approx", r"\frac{SR_*^2}{\sqrt{SR_*^2 + K/T}} = \frac{SR_*}{\sqrt{1 + K/(T\,SR_*^2)}}",
                      font_size=32, colors={r"SR(\hat w)": GOOD})]
        whys = [why(r"whiten: in the coordinates where the alphas are independent with unit variance, the estimated weights "
                    r"are the true direction plus noise of size $1/\sqrt T$ in each of $K$ directions"),
                why(r"the out-of-sample Sharpe ratio of any weights is the cosine of their angle to $\theta$, times $\|\theta\|$"),
                why(r"the signal adds $\|\theta\|^2$; the noise adds $1/T$ in every one of the $K$ directions"),
                why(r"finite-sample approximation; convergence needs deterministic $\|\theta\|^2\to S\in(0,\infty)$ and $K/T\to\gamma$: "
                    r"$z^\top\theta\to S$ and $\|z\|^2\to S+\gamma$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Whiten with the known population covariance. <bookmark mark='a'/> The estimated direction is theta plus a standard Gaussian vector divided by square root T. <bookmark mark='b'/> Its population out-of-sample Sharpe is the inner product with theta divided by its own length, exactly. <bookmark mark='c'/> The numerator has mean S and variance S over T. Squared length has mean S plus K over T and variance four S over T plus two K over T squared. <bookmark mark='d'/> Replacing these concentrating quantities by their limits gives S divided by square root S plus K over T. At finite K and T this is an approximation, not the expectation of a ratio. It requires a stated asymptotic regime before becoming a convergence claim."
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

    def mirror(self):
        rows = [cmath(r"SR_{\text{in}}(\hat w)", r"=", r"\frac{\hat w^\top\hat\mu}{\sqrt{\hat w^\top\Sigma\hat w}} = \|z\|",
                      font_size=32, colors={r"SR_{\text{in}}(\hat w)": TRAIN_C}),
                cmath(r"\|z\|", r"\approx", r"\sqrt{SR_*^2 + K/T}", font_size=32, colors={r"\|z\|": TRAIN_C}),
                cmath(r"SR_{\text{in}} \cdot SR_{\text{out}}", r"=", r"z^\top\theta\ \xrightarrow{p}\ S", font_size=34,
                      colors={r"SR_{\text{in}} \cdot SR_{\text{out}}": HURDLE})]
        whys = [why(r"measured on the same days that estimated the weights, the Sharpe ratio is the length of $z$ itself"),
                why(r"it grows with $K$ even when the alphas are worthless: $\sqrt{K/T}$ of pure fit"),
                why('exact product identity under known covariance; the product concentrates at S in the stated bounded-strength regime')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The same known-covariance model has an exact training identity. <bookmark mark='a'/> Replacing the population mean in the numerator by its fitted sample mean, but retaining the true covariance in the denominator, gives training score equal to the norm of z. This is not the usual fully sample-estimated Sharpe. <bookmark mark='b'/> Its concentrating scale is square root S plus K over T; even zero population strength can produce a positive fit. <bookmark mark='c'/> The product of that training score and population out-of-sample Sharpe is exactly z transpose theta, with expectation S. It concentrates at S in the bounded-strength regime. This model does not identify which losses in the selected coin library came from mean error, covariance error, selection or data conventions."
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

    def theorem(self):
        st = VGroup(MathTex(r"SR(\hat w)\xrightarrow{p}\frac{S}{\sqrt{S+\gamma}},\quad K/T\to\gamma,\quad \|\theta_K\|^2\to S\in(0,\infty)", font_size=29),
                    wrapped_label(r"IID Gaussian returns; known positive definite covariance; deterministic, pre-specified library. Numerator variance $S/T\to0$; squared-length variance $4S/T+2K/T^2\to0$", 9.6, 19),
                    wrapped_label(r"Finite samples: approximation, not an exact expected Sharpe. Estimated covariance adds direction noise; scalar inflation alone leaves Sharpe unchanged", 9.6, 19)
                    ).arrange(DOWN, buff=0.3)
        card = theorem_card(r"Known-covariance estimation risk", st, r"Gaussian concentration argument; estimation-risk context: Brown (1976), Kan--Zhou (2007)", width=11.4, font_size=21)
        with self.voiceover("State the regime precisely. <bookmark mark='a'/> Let the pre-specified dimension and observation count grow with K over T approaching finite gamma, and deterministic squared population strength approaching a finite positive S. Gaussian concentration makes the numerator tend to S and squared length to S plus gamma, so the population Sharpe tends to S over square root S plus gamma. <bookmark mark='b'/> The two variance calculations prove this known-covariance statement. It is not an exact finite-sample mean formula or a theorem about adaptively selected alphas. Brown and Kan-Zhou provide estimation-risk context; adding estimated covariance changes the problem. A scalar rescaling of weights does not itself reduce Sharpe, and shrinkage improvements depend on the rule and objective.") as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.5)
        self.clear_scene()

    def sims(self, t):
        Ks = np.asarray(t["Ks"], float)
        estimates = [r["estimated"] for rows in t["sims"].values() for r in rows]
        finite_estimates = [v for v in estimates if np.isfinite(v)]
        lo = min(0.0, math.floor(min(finite_estimates, default=0.0) * 20) / 20)
        omitted = sum(not np.isfinite(v) for v in estimates)
        g = axes([0, np.log10(Ks[-1]) + 0.05], [lo, 0.3], x_length=7.2, y_length=4.4, xlabel=r"number of alphas combined, $K$ "
                 r"(log scale)", ylabel=r"out-of-sample Sharpe ratio, per day", xticks=[0, 1, np.log10(Ks[-1])],
                 yticks=sorted({lo, 0, 0.1, 0.2, 0.3}), xfmt=lambda v: f"{10 ** v:.0f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        x = np.log10(Ks)
        star = [r["star"] for r in t["sims"]["500"]]
        top = curve(ax, x, star, GREY_B, stroke_width=2)
        lines, dots, est = VGroup(), VGroup(), VGroup()
        for T in ("250", "500", "1000"):
            rows = t["sims"][T]
            lines.add(curve(ax, x, [r["theory"] for r in rows], T_COL[T], stroke_width=3))
            dots.add(VGroup(*[Dot(ax.c2p(a, r["known"]), radius=0.05, color=T_COL[T]) for a, r in zip(x, rows)]))
            est.add(VGroup(*[Triangle(color=T_COL[T], fill_opacity=0.9).scale(0.06).move_to(ax.c2p(a, r["estimated"]))
                             for a, r in zip(x, rows) if np.isfinite(r["estimated"])]))
        leg = legend([(GREY_B, r"$SR_*$: what the true weights earn"), (T_COL["250"], r"$T = 250$ days"),
                      (T_COL["500"], r"$T = 500$"), (T_COL["1000"], r"$T = 1{,}000$")], font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"every alpha has a Sharpe ratio of {t['sr_each']:.2f} a day (about "
                             rf"{t['sr_each'] * math.sqrt(365):.1f} a year) and is independent of the others. Lines: the formula; "
                             r"dots: simulation with known covariance; triangles: estimated (300 draws each). "
                             rf"All finite triangles shown, including nonpositive values; {omitted} nonfinite cells omitted", 3.4, 14,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        r250 = t["sims"]["250"]
        sr_year = t["sr_each"] * math.sqrt(365)
        with self.voiceover(
            f"""The original simulation fixes each coordinate's daily Sharpe at0.03, about {sr_year:.2f} under365-day annualisation, and uses independent Gaussian coordinates. <bookmark mark='a'/> Population strength grows with K in this illustration, unlike the bounded-strength limit just stated. <bookmark mark='b'/> The coloured curves use250,500 and1,000 observation days, not one, two and four calendar years. Dots are300-replicate means, with sampling error; agreement need not be exact. At250 days and forty coordinates, the simulated mean is {r250[5]['known']:.3f} per day versus population optimum {r250[5]['star']:.3f}. <bookmark mark='c'/> Triangles estimate covariance too. All finite values, including nonpositive estimates, are shown; {omitted} nonfinite cells are explicitly omitted. This comparison illustrates estimation risk in the chosen Gaussian design, not a universal finite-sample guarantee."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(top))
            vo.wait_until("b")
            self.play(*[Create(l_) for l_ in lines], *[FadeIn(d_) for d_ in dots], run_time=2)
            vo.wait_until("c")
            self.play(*[FadeIn(e_) for e_ in est])
        self.wait(0.4)
        self.clear_scene()

    def wishart(self, t):
        rows = [cmath(r"(T - 1)\hat\Sigma", r"\sim", r"W_K(T - 1, \Sigma)", font_size=32, colors={r"(T - 1)\hat\Sigma": HURDLE}),
                cmath(r"\mathbb E\big[\hat\Sigma^{-1}\big]", r"=", r"\frac{T - 1}{T - K - 2}\,\Sigma^{-1}", font_size=32,
                      colors={r"\mathbb E\big[\hat\Sigma^{-1}\big]": BAD}),
                cmath(r"\hat w", r"=", r"\hat\Sigma^{-1}\hat\mu:\ \text{two noises, and the second is not averaged away}",
                      font_size=30, colors={r"\hat w": HURDLE})]
        whys = [why(r"the sample covariance of normal returns is a Wishart matrix with $T - 1$ degrees of freedom, "
                    r"independent of $\hat\mu$"),
                why(r"for $T>K+2$, the expected inverse has scalar inflation; its expectation diverges at that boundary; scale alone leaves Sharpe "
                    r"unchanged, while direction noise can impair the fitted portfolio"),
                why(rf"in the simulation: with $T = 250$ and $K = 80$, "
                    rf"{t['sims']['250'][-1]['known']:.3f} a day with $\Sigma$ known, "
                    rf"{t['sims']['250'][-1]['estimated']:.3f} with $\Sigma$ estimated")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        r80 = t["sims"]["250"][-1]
        with self.voiceover(
            f"""Under IID Gaussian observations and the unbiased sample covariance, <bookmark mark='a'/> T minus one times the estimated covariance is Wishart with T minus one degrees of freedom, independently of the sample mean. <bookmark mark='b'/> Its expected inverse equals T minus one over T minus K minus two times the population inverse, provided T exceeds K plus two. The moment fails at the boundary; the formula is not valid beyond it. Multiplying every weight by the same positive scalar leaves Sharpe unchanged. Random directional error, not scalar inflation alone, is the concern. <bookmark mark='c'/> In300-replicate simulations at250 days and eighty coordinates, the mean is {r80['known']:.3f} per day with covariance known and {r80['estimated']:.3f} estimated. The observed difference does not establish that every estimate or shrinkage rule improves or worsens every finite sample."""
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

    def marginal(self, t):
        rows = [cmath(r"f(S,K)", r"=", r"\frac{S}{\sqrt{S+K/T}},\quad S=SR_*^2,\quad a=s^2", font_size=29, colors={r"f(S,K)": GOOD}),
                cmath(r"f(S+a,K+1)>f(S,K)", r"\iff", r"(TS+K)a^2+(TS^2+2SK)a-S^2>0", font_size=26),
                cmath(r"a", r">", r"\frac{2S}{TS+2K+\sqrt{(TS+2K)^2+4(TS+K)}}", font_size=30, colors={r"a": HURDLE}),
                cmath(r"a", r">", r"\frac{S}{TS+2K}\quad\text{(first-order sufficient condition)}", font_size=29)]
        whys = [why(r"the approximation's objective, with per-observation squared population strengths and observation count $T$"),
                why(r"exact finite addition within this objective; add one fixed independent coordinate of true strength $a$"),
                why(r"positive quadratic root for $S>0$; this is not an exact finite-sample expected-Sharpe threshold"),
                why(r"linearising the finite change drops a positive quadratic term; this stronger condition is sufficient, not necessary")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        best = t["best_K_dim"]
        with self.voiceover(f"Now separate a finite addition from a differential approximation. <bookmark mark='a'/> Use f equal to S over square root S plus K over T, with daily squared strengths and a daily observation count. This objective already approximates actual finite-sample Sharpe. <bookmark mark='b'/> Adding one fixed independent coordinate of true squared strength a increases f exactly when the displayed quadratic is positive. <bookmark mark='c'/> Solving its positive root gives the finite-addition threshold. The often quoted S over T S plus two K is a first-order, stronger sufficient threshold, not the exact finite one. <bookmark mark='d'/> These are true residual strengths in the stated model, not selected in-sample estimates. In the original diminishing-strength illustration, at 500 observation days, the objective peaks near {best} among the displayed K values. That discrete-grid illustration is not a universally optimal library size.") as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def data(self, t):
        rows = t["data"]
        hx = [-4.2, -1.6, 1.0, 3.6]
        head = VGroup(label(r"alphas combined, $K$", font_size=18, color=GREY_B),
                      label(r"estimated weights, 2018--19", font_size=18, color=TRAIN_C),
                      label(r"estimated weights, 2020", font_size=18, color=VALID_C),
                      label(r"equal weights, 2020", font_size=18, color=COMB))
        tab = VGroup(head)
        for r in rows:
            tab.add(VGroup(MathTex(f"{r['K']}", font_size=26), MathTex(f"{r['mv_train']:.2f}", font_size=26),
                           MathTex(f"{r['mv_valid']:.2f}", font_size=26), MathTex(f"{r['ew_valid']:.2f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.2 - 0.62 * j, 0])
        foot = wrapped_label(r"annualised Sharpe ratios before costs; the $K$ best random formulas by training IC, "
                             r"de-duplicated; weights fitted on 2018--19 daily long-short returns", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.5)
        k_best = max(rows, key=lambda r: r["mv_valid"])["K"]
        r40 = rows[-1]
        with self.voiceover(
            f"""Return to the selected coin formulas. <bookmark mark='a'/> Training scores reuse the data that chose the library, signs and weights; they are optimistic for several reasons. <bookmark mark='b'/> Across these inspected sizes, validation estimated weighting is largest at {k_best}; at forty its annualised Sharpe is {r40['mv_valid']:+.2f}, versus {r40['ew_valid']:.2f} for equal weighting. Choosing that size after this table would spend the validation year. Equal weights still inherit formula selection, and missing-component conventions differ between the two rules. Correlation alone does not invalidate whitening with known covariance; selection, estimated covariance, nonstationarity and non-Gaussian dependence break the simple model here. The table does not isolate one causal explanation or establish net executable performance."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[2], r_[3])) for r_ in tab[1:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: alphas chosen by the same data", r"the formula assumes the $K$ alphas were fixed in advance; "
                          r"when they are the winners of a search on the same days, their means are biased up as well, and "
                          r"the joint correction is not settled", width=12.4, font_size=18),
            desk_question(r"open: time-varying edges", r"if each alpha's mean decays, $T$ is not a sample size but a trade-off "
                          r"between noise and staleness", width=12.4, font_size=18),
            desk_question(r"open: the best shrinkage for many weak alphas", r"nonlinear covariance shrinkage and shrinking the "
                          r"means toward equal weights both help; the optimal joint rule in high dimension is an active topic",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> The formula assumes the alphas were fixed in advance; when they "
            "are the winners of a search on the same days, their means are biased too, and the joint correction is not "
            "settled. <bookmark mark='b'/> If each alpha's edge decays, more days is not simply better: it trades noise "
            "against staleness. <bookmark mark='c'/> And the best way to shrink both the means and the covariance of many "
            "weak alphas at once is still an active topic."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"20 independent alphas, each with a daily Sharpe ratio of 0.02, and one year (365 days) of data. "
                       r"Compute $SR_*$ and the formula's out-of-sample Sharpe ratio.")
        with self.voiceover(
            "Pause and predict. Twenty independent alphas, each with a daily Sharpe ratio of point zero two, and a year of "
            "data. What is the best possible Sharpe ratio, and what does the formula say you will get out of sample?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
