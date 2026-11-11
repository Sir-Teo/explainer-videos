from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import riskmodel as RM
from videos.quant.quant31.common import BAD, GOOD, HURDLE, IC_C, OOS_C, PART, REAL_C, exact_ic_ir, fit_right, load


class Research(VoiceoverScene):
    def construct(self):
        t = load("theory")
        self.card()
        self.setup_()
        self.proof()
        self.theorem()
        self.sims(t)
        self.breadth()
        self.coins(t)
        self.tails(t)
        self.ladder_of_corrections(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"The information ratio when the IC moves", r"What does a forecast's instability cost, exactly?",
                          part=PART)
        with self.voiceover('For the researcher. An exact moment identity in a specified normalised-score model. A latent correlation parameter may vary across periods. We derive the resulting information ratio, compare existing toy simulations, then distinguish those assumptions from measured research-period rank correlations.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"r_{i,t}", r"=", r"\rho_t\, z_{i,t} + \sqrt{1 - \rho_t^2}\;\varepsilon_{i,t}", font_size=36,
                      colors={r"\rho_t": IC_C}),
                cmath(r"\rho_t", r"\overset{\text{iid}}{\sim}", r"(\mu,\ \sigma^2),\quad |\rho_t|\le1,\quad N\ge2,\ "
                      r"\varepsilon_{i,t} \overset{\text{iid}}{\sim} (0, 1)", font_size=32),
                cmath(r"\pi_t", r"=", r"\tfrac1N\textstyle\sum_i z_{i,t}\, r_{i,t}", font_size=36)]
        whys = [why(r"latent correlation model, distinct from a finite cross-sectional sample correlation; $\sum_i z_i=0$, $\sum_i z_i^2=N$"),
                why(r"the IC varies across periods with mean $\mu$ and standard deviation $\sigma$, independently of the "
                    r"noise; the scores have mean 0 and variance 1 across the $N$ assets"),
                why(r"the long--short book with holdings proportional to the scores: its return in period $t$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Specify the toy. <bookmark mark='a'/> Scores have cross-sectional sum zero and sum of squares N, with N at least two. Returns equal a latent parameter rho times scores plus noise scaled by square root of one minus rho squared. <bookmark mark='b'/> Rho is bounded between minus and plus one, with mean mu and variance sigma squared. Conditional on rho and scores, noise has zero mean, unit variance and no cross-asset covariance. Periods are independent for annual square-root scaling. <bookmark mark='c'/> The book holds scores divided by N. Rho is a latent parameter; a measured finite-sample Pearson or rank correlation is not the same object."
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

    def proof(self):
        rows = [cmath(r"\pi_t", r"=", r"\rho_t\cdot\tfrac1N\textstyle\sum_i z_{i,t}^2 + \sqrt{1 - \rho_t^2}\cdot\tfrac1N\sum_i "
                      r"z_{i,t}\varepsilon_{i,t}", font_size=30),
                cmath(r"\pi_t", r"=", r"\rho_t + \sqrt{1 - \rho_t^2}\;\frac{\xi_t}{\sqrt N},\qquad \xi_t \sim (0, 1)", font_size=34),
                cmath(r"\mathbb E\,\pi_t", r"=", r"\mu", font_size=36),
                cmath(r"\operatorname{Var}\pi_t", r"=", r"\sigma^2 + \frac{\mathbb E(1 - \rho_t^2)}{N} = \sigma^2\Big(1 - "
                      r"\frac1N\Big) + \frac{1 - \mu^2}{N}", font_size=30, colors={r"\operatorname{Var}\pi_t": HURDLE})]
        whys = [why(r"substitute the return model into the book's return"),
                why(r"the scores are standardised, so the first average is one; the second is noise with variance "
                    r"$1/N$ conditionally; Gaussian noise additionally gives a standard-normal projection"),
                why(r"the expected return is the mean IC"),
                why(r"the law of total variance: the IC's own variance, plus the noise averaged over $N$ assets, where "
                    r"$\mathbb E\,\rho_t^2 = \mu^2 + \sigma^2$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "Four steps establish the moments. <bookmark mark='a'/> Substitute the return model into the book's payoff. <bookmark mark='b'/> Normalisation makes the first average one. Conditional noise has mean zero and variance one over N; Gaussian noise gives the displayed standard-normal projection. <bookmark mark='c'/> Unconditional mean payoff is mu. <bookmark mark='d'/> Total variance is sigma squared plus one minus mu squared minus sigma squared, divided by N. The persistent part does not diversify. Appropriate conditional first and second moments suffice for this variance identity."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def theorem(self):
        st = VGroup(MathTex(r"IR \;=\; \frac{\mu}{\sqrt{\sigma^2(1 - 1/N) + (1 - \mu^2)/N}}", font_size=40),
                    MathTex(r"\sigma = 0:\ IR = \frac{\mu\sqrt N}{\sqrt{1 - \mu^2}} \approx \mu\sqrt N,\qquad "
                            r"N\to\infty:\ IR \to \frac{\mu}{\sigma}", font_size=30),
                    wrapped_label(r"per period; for $T$ independent periods a year, the annual IR is $\sqrt T$ times it. "
                                  r"The form $\mu/\sqrt{\sigma^2 + (1-\mu^2)/N}$ is Qian and Hua (2004) and Ding (2010); "
                                  r"the factor $1 - 1/N$ is exact in this model", 9.6, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"The law with a moving IC", st, r"Qian and Hua (2004); Ding (2010)", width=11.4, font_size=22)
        per = exact_ic_ir(0.05, 0.10, 500)
        with self.voiceover(
            f"""The theorem is exact for this toy's actual latent moments. <bookmark mark='a'/> Divide mu by square root of sigma squared times one minus one over N, plus one minus mu squared over N. <bookmark mark='b'/> At zero dispersion the exact value is mu root N divided by square root of one minus mu squared; mu root N is a small-correlation approximation. For nonnegative mu and positive sigma, the limit is mu over sigma. This is not a universal bound for market strategies. <bookmark mark='c'/> With the hook's chosen moments and five hundred assets, the exact toy gives {per:.2f} monthly and {per * math.sqrt(12):.2f} annually, assuming independent months."""
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
            vo.wait_until("c")
            self.wait(0.1)
        self.wait(0.5)
        self.clear_scene()

    def sims(self, t):
        rows = t["sims"]
        g = axes([1.2, 3.1], [0, 1.5], x_length=7.4, y_length=4.4, xlabel=r"breadth $N$", ylabel=r"IR per period",
                 xticks=[1.3, 2, 3], yticks=[0, 0.5, 1.0], xfmt=lambda v: {1.3: "20", 2: "100", 3: "1000"}[v],
                 yfmt=lambda v: f"{v:.1f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        xs = np.linspace(1.2, 3.1, 80)
        Ns = 10 ** xs
        naive = curve(ax, xs, 0.04 * np.sqrt(Ns), IC_C, stroke_width=3)
        cols = {0.03: GOOD, 0.08: BAD}
        forms, lims, dots = VGroup(), VGroup(), VGroup()
        for sd, col in cols.items():
            forms.add(curve(ax, xs, [exact_ic_ir(0.04, sd, float(n)) for n in Ns], col, stroke_width=3))
            lims.add(DashedLine(ax.c2p(1.2, min(0.04 / sd, 1.5)), ax.c2p(3.1, min(0.04 / sd, 1.5)), color=col,
                                stroke_width=1.5))
            for r in rows:
                if r["ic_sd"] == sd:
                    dots.add(Dot(ax.c2p(math.log10(r["N"]), r["sim"]), radius=0.07, color=col))
        leg = legend([(IC_C, r"$0.04\sqrt N$"), (GOOD, r"$\sigma = 0.03$"), (BAD, r"$\sigma = 0.08$")], font_size=17)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_right(leg)
        txt = wrapped_label(r"dots: simulated strategies, 6 of 1{,}500 periods each, mean IC 0.04; dashed: the limits "
                            r"$\mu/\sigma$; curves use pre-clipping parameter moments", 3.8, 16, GREY_A).next_to(leg, DOWN, buff=0.5)
        fit_right(txt)
        big = [r for r in rows if r["N"] == 1000]
        with self.voiceover(
            f"""Compare existing fixed simulations. <bookmark mark='a'/> The small-correlation benchmark rises with breadth. <bookmark mark='b'/> Solid references use the exact moment identity at the chosen latent parameters; dashed lines show their asymptotes. The saved simulator clips Gaussian latent draws between minus point nine nine and plus point nine nine. Its input moments are therefore pre-clipping parameters, while the theorem uses post-clipping moments. <bookmark mark='c'/> The saved thousand-asset simulated ratios are {big[0]['sim']:.2f} and {big[1]['sim']:.2f}. Cached reference values {big[0]['formula']:.2f} and {big[1]['formula']:.2f} use the unchanged House approximation, omitting the finite-N subtraction of sigma squared over N. Neither finite simulation nor pre-clipping curves establish exact equality."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(txt))
            vo.wait_until("a")
            self.play(Create(naive))
            vo.wait_until("b")
            self.play(*[Create(f) for f in forms], *[Create(l_) for l_ in lims], run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.1))
        self.wait(0.4)
        self.clear_scene()

    def breadth(self):
        rows = [cmath(r"N^*", r"=", r"\frac{1-\mu^2-\sigma^2}{\sigma^2}\quad(\sigma>0)", font_size=40,
                      colors={r"N^*": HURDLE}),
                cmath(r"IR(N^*)", r"=", r"\frac{\mu}{\sigma\sqrt 2}\ \approx\ 71\%\ \text{of the ceiling}", font_size=36),
                cmath(r"\mu=0.05,\ \sigma = 0.10", r":", r"N^*=98.75\approx99", font_size=36)]
        whys = [why(r"the breadth at which the IC's own variance equals the noise variance: beyond it, extra assets buy "
                    r"little"),
                why(r"at that breadth the information ratio is already $1/\sqrt2$ of its limit"),
                why(r"fixed toy moments, not a typical market calibration; if $N^*<2$, crossover is below feasible breadth")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A crossover within the toy. <bookmark mark='a'/> Equate persistent variance sigma squared with diversifiable variance, one minus mu squared minus sigma squared over N. This gives the displayed N star, assuming positive sigma and feasible nondegenerate moments. <bookmark mark='b'/> At this continuous reference breadth, the ratio is exactly one over root two of its asymptote. <bookmark mark='c'/> Mu point zero five and sigma point one give ninety-eight point seven five, about ninety-nine assets. Extra assets still help, with diminishing gains. If N star is below two, even the smallest feasible breadth is beyond the crossover."
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

    def coins(self, t):
        rows = t["coins"]
        hx = [-4.6, -2.6, -0.9, 0.8, 2.7, 4.9]
        head = VGroup(label(r"signal", font_size=17, color=GREY_B), label(r"mean IC", font_size=17, color=IC_C),
                      label(r"sd of IC", font_size=17, color=HURDLE), label(r"$|\mu|\sqrt N$", font_size=17, color=IC_C),
                      label(r"helper approx.", font_size=17, color=GOOD), label(r"realised", font_size=17, color=REAL_C))
        tab = VGroup(head)
        for r in rows:
            tab.add(VGroup(label(r["signal"], font_size=19), MathTex(f"{r['ic']:+.3f}", font_size=24),
                           MathTex(f"{r['ic_sd']:.2f}", font_size=24), MathTex(f"{r['naive']:.2f}", font_size=24),
                           MathTex(f"{r['formula']:.2f}", font_size=24), MathTex(f"{r['realised']:.3f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.5 - 0.6 * j, 0])
        foot = wrapped_label(rf"daily rank ICs, 2018--2020; an average breadth of {rows[0]['N']:.0f} coins; IR per day; "
                             r"realised: the long--short book's own daily Sharpe ratio", 11.6, 16,
                             GREY_A).to_edge(DOWN, buff=0.4)
        m = [r for r in rows if r["signal"] == "mined"][0]
        with self.voiceover(
            f"""Now separate the empirical objects. <bookmark mark='a'/> These are saved daily rank correlations in the reused research sample; the mined signal has mean {m['ic']:.3f} and standard deviation {m['ic_sd']:.2f}. <bookmark mark='b'/> Substituting observed rank moments into the unchanged approximate helper gives {m['formula']:.2f}, compared with naive {m['naive']:.2f}. This is heuristic: observed dispersion already includes cross-sectional estimation noise, so adding another sampling-noise term can double count. <bookmark mark='c'/> The actual research book's daily mean-over-standard-deviation is {m['realised']:.3f}. The difference does not establish a missing causal correction."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[:3])) for r_ in tab[1:]], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[3:5])) for r_ in tab[1:]], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_[5]) for r_ in tab[1:]], lag_ratio=0.15))
        self.wait(0.4)
        self.clear_scene()

    def tails(self, t):
        rows = [cmath(r"\pi_t", r"=", r"N\,\operatorname{sd}_{cs}(w_t)\operatorname{sd}_{cs}(r_t)\operatorname{Corr}_{P}(w_t,r_t)", font_size=32),
                cmath(r"\operatorname{Corr}_{\text{Spearman}}", r"\neq", r"\operatorname{Corr}_{\text{Pearson}}\ \ "
                      r"\text{in general, including Gaussian returns}", font_size=32, colors={r"\neq": BAD}),
                cmath(r"\text{kurtosis}", r"=", rf"{t['kurtosis']:.0f}\ \text{{(excess, the coins' daily returns)}}",
                      font_size=32)]
        whys = [why(r"the book's return is the linear correlation of its weights with the returns, not the rank "
                    r"correlation the IC measures"),
                why(r"the rank IC ignores how large the winners and losers were; a few extreme moves dominate the linear "
                    r"one"),
                why(r"pooled excess kurtosis is descriptive; heteroskedastic mixtures can contribute to it")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""Definitions and scaling matter. <bookmark mark='a'/> For zero-sum weights, payoff equals N times cross-sectional weight dispersion times return dispersion times Pearson correlation. Use population-divisor cross-sectional dispersions. Weight normalisation and universe changes can change the prefactor. <bookmark mark='b'/> Spearman and Pearson correlations generally differ, including under Gaussian distributions. Rank correlation discards magnitudes; fat tails are not an identified explanation of the whole gap. <bookmark mark='c'/> Saved pooled excess kurtosis is {t['kurtosis']:.0f}. It is descriptive and can reflect heterogeneous volatility, not solely one stationary heavy-tailed law."""
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

    def ladder_of_corrections(self, t):
        m = [r for r in t["coins"] if r["signal"] == "mined"][0]
        steps_ = [(r"the fundamental law, $|\mu|\sqrt N$", m["naive"], IC_C),
                  (r"rank-moment helper approximation", m["formula"], GOOD),
                  (r"mean over sd of the Pearson IC of the weights", m["pearson_ir"], HURDLE),
                  (r"what the book earned", m["realised"], REAL_C)]
        mx = max(v for _, v, _ in steps_)
        bars = VGroup()
        for j, (nm, v, col) in enumerate(steps_):
            r = Rectangle(width=6.0 * v / mx, height=0.55, fill_color=col, fill_opacity=0.8, stroke_width=0)
            r.move_to([-1.0, 1.6 - 1.0 * j, 0], aligned_edge=LEFT)
            bars.add(VGroup(label(nm, font_size=19, color=col).next_to(r, UP, buff=0.08).align_to(r, LEFT), r,
                            MathTex(f"{v:.3f}", font_size=26).next_to(r, RIGHT, buff=0.2)))
        bars.move_to(DOWN * 0.1)

        foot = wrapped_label(rf"the mined alpha, daily, 2018--2020; the Pearson IC of its rank weights averages "
                             rf"{m['pearson']:.3f} with sd {m['pearson_sd']:.2f}; descriptive reused-sample ratios, with no confidence interval estimated", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"""Compare four descriptive ratios for the selected formula. <bookmark mark='a'/> Naive rank mean times root breadth gives {m['naive']:.2f}; the rank-moment helper approximation gives {m['formula']:.2f}. <bookmark mark='b'/> Mean over standard deviation of the weights' measured Pearson correlation is {m['pearson_ir']:.3f}. <bookmark mark='c'/> The actual book's daily ratio is {m['realised']:.3f}. These are different definitions on reused selected data. Their numerical proximity is not a causal decomposition, a confidence interval or independent validation. No serial-dependence or selection-adjusted uncertainty was estimated."""
        ) as vo:
            self.play(FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[1]))
            vo.wait_until("b")
            self.play(FadeIn(bars[2]))
            vo.wait_until("c")
            self.play(FadeIn(bars[3]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"memory and model uncertainty", r"serial dependence changes annual scaling; specified linear-quadratic models can have Riccati solutions, while costs and constraints need explicit assumptions", width=12.4, font_size=18),
            desk_question(r"estimating effective breadth", r"known covariance permits model-based calculations; noisy covariance, overlapping decisions and changing universes make reliable estimation difficult", width=12.4, font_size=18),
            desk_question(r"robust weights and finite moments", r"known finite-variance mean and covariance retain the formal mean--variance solution; estimating them robustly and handling nonlinear constraints is the harder task", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three research directions, with precise limits. <bookmark mark='a'/> Memory changes annual scaling. Some specified linear-quadratic models already have Riccati solutions; broader models require explicit dynamics and costs. "
            "<bookmark mark='b'/> Known covariance allows effective-breadth calculations. Reliable estimation under changing correlation and overlapping decisions is difficult. "
            "<bookmark mark='c'/> With known finite moments, heavy tails do not erase the formal mean--variance solution. Robust estimation, moment existence and realistic nonlinear constraints remain substantive questions."
        ) as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(Indicate(cards[0]))
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def question(self):
        q = pause_card(r"the toy's independent monthly latent correlation has mean 0.03 and sd 0.06. What is the largest annual IR any breadth can "
                       r"give it?")
        with self.voiceover(
            "Pause and predict. The toy's independent monthly latent correlation has mean point zero three and standard deviation point zero six. "
            "What is the largest annual information ratio any breadth can give it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
