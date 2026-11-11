from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C,
                                         comma, fit_right, ladder, load)


class Research(VoiceoverScene):
    """Analytical estimator arguments and audited ordinary fund simulations only."""

    def construct(self):
        self.card()
        self.objects()
        self.theorem()
        self.proof()
        self.clipping()
        self.variance()
        self.analytic_curves()
        self.bsw_limits()
        f = load('fdr')
        self.fdr(f)
        self.qtable(f)
        self.bg_setting()
        self.bg_proof()
        self.bg_check(load('bg_theory'))
        self.related()
        self.question()

    def card(self):
        c = research_card(r"Counting nulls and allocating capital",
                          r"Which expectation bounds survive clipping, dependence and selection?", part=PART)
        with self.voiceover(
            "For the researcher. Two mathematical arguments, with their boundaries. First, the uncapped "
            "large-p-value estimator has an upward expectation bound, but the practical cap changes that result. "
            "Second, competitive Bayesian allocation can give zero expected dollar alpha under an idealised model, "
            "even though managers have different skills. The chapter proves the statements, gives a clipping "
            "counterexample and compares a finite simulation with the conditional allocation argument."
        ):
            self.play(FadeIn(c[0], shift=UP * .2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def objects(self):
        rows = [cmath(r"m=m_0+m_1", r",", r"\pi_0=m_0/m,\quad 0\le\lambda<1", font_size=40),
                cmath(r"p_i\sim U(0,1)", r":", r"i\in H_0\quad\text{(valid continuous nulls)}", font_size=36),
                cmath(r"W(\lambda)", r"=", r"\sum_i 1\{p_i>\lambda\}", font_size=42),
                cmath(r"\widetilde\pi_0", r"=", r"\frac{W(\lambda)}{m(1-\lambda)},\qquad\widehat\pi_0=\min(1,\widetilde\pi_0)", font_size=36)]
        whys = [why(r"the null is a mathematical hypothesis; zero alpha and nonpositive alpha are different null sets"),
                why(r"validity is an assumption to justify, not a consequence of naming a statistic a p-value"),
                why(r"a count of large p-values, with no independence assumed yet"),
                why(r"tilde denotes the raw estimator; hat denotes the cap used in the unchanged simulation helper")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=0, buff=.5)
        with self.voiceover(
            "Define the objects carefully. <bookmark mark='a'/> There are m tests, with m nought true nulls. "
            "<bookmark mark='b'/> Assume each true null has a uniform p-value. Dependence is allowed, and validity "
            "still needs justification. <bookmark mark='c'/> Count the p-values above lambda. "
            "<bookmark mark='d'/> Divide by m times one minus lambda to obtain the raw estimator, denoted with a "
            "tilde. The unchanged helper caps this number at one. We use a hat for that different random variable."
        ) as vo:
            step(0)
            for k, mark in enumerate(('a', 'b', 'c', 'd')):
                vo.wait_until(mark)
                if k:
                    step(k)
        self.clear_scene()

    def theorem(self):
        st = VGroup(
            MathTex(r"\mathbb E\widetilde\pi_0=\pi_0+\frac{\sum_{i\in H_1}P(p_i>\lambda)}{m(1-\lambda)}\ge\pi_0", font_size=35),
            wrapped_label(r"Fixed threshold, valid uniform nulls: linearity needs no independence. The statement is "
                          r"about the uncapped estimator's expectation, not a confidence bound for one sample.", 10.1, 21)
        ).arrange(DOWN, buff=.35)
        card = theorem_card(r"Raw large-p-value expectation", st, r"after Storey (2002)", width=11.8, font_size=23)
        with self.voiceover(
            "The raw expectation bound. <bookmark mark='a'/> Its expectation is the true null share plus the "
            "alternatives' large-p-value probabilities, divided by a positive denominator. "
            "<bookmark mark='b'/> Therefore it is at least the null share, without any independence requirement. "
            "This does not say every realised estimate is above the truth, nor does it give a confidence interval. "
            "Uniform nulls give the equality shown; suitable superuniform nulls give a lower-bound version."
        ) as vo:
            self.play(FadeIn(card, shift=UP * .2))
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Indicate(st[0], color=HURDLE, scale_factor=1.02))
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"\mathbb E W", r"=", r"\sum_i\mathbb E1\{p_i>\lambda\}=\sum_iP(p_i>\lambda)", font_size=35),
                cmath(r"", r"=", r"m_0(1-\lambda)+\sum_{i\in H_1}P(p_i>\lambda)", font_size=38),
                cmath(r"\mathbb E\widetilde\pi_0-\pi_0", r"=", r"\frac{\sum_{i\in H_1}P(p_i>\lambda)}{m(1-\lambda)}\ge0", font_size=38)]
        whys = [why(r"linearity of expectation applies to dependent indicators too"),
                why(r"each uniform null contributes exactly one minus lambda"),
                why(r"divide and subtract; equality holds when the sum of alternative tail probabilities is zero")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=0, buff=.6)
        with self.voiceover(
            "The proof is short. <bookmark mark='a'/> A count is a sum of indicators. Expectation turns it into "
            "the sum of their probabilities, even when the indicators depend on each other. "
            "<bookmark mark='b'/> Uniform nulls contribute one minus lambda each. "
            "<bookmark mark='c'/> Divide and subtract the null share. The remaining numerator is a sum of "
            "nonnegative probabilities. The bound is exact for the raw estimator at a fixed threshold. A threshold "
            "selected from these same p-values requires a separate argument."
        ) as vo:
            step(0)
            for k, mark in enumerate(('a', 'b', 'c')):
                vo.wait_until(mark)
                if k:
                    step(k)
        self.clear_scene()

    def clipping(self):
        rows = [cmath(r"p_1=\cdots=p_m=U", r",", r"U\sim U(0,1),\quad\pi_0=1", font_size=38),
                cmath(r"\lambda=1/2", r"\Rightarrow", r"\widetilde\pi_0=2\,1\{U>1/2\},\quad\mathbb E\widetilde\pi_0=1", font_size=34),
                cmath(r"\widehat\pi_0=\min(1,\widetilde\pi_0)", r"\Rightarrow", r"\mathbb E\widehat\pi_0=1/2<1", font_size=36)]
        whys = [why(r"all tests are true nulls, each with a valid uniform marginal; dependence is perfect"),
                why(r"the raw estimator is zero or two, each with probability one half"),
                why(r"clipping is nonlinear: expectation of the cap differs from the cap of the expectation")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=0, buff=.6)
        with self.voiceover(
            "Why the cap matters. <bookmark mark='a'/> Let all null p-values equal the same uniform random "
            "variable. Each marginal remains valid, and every test is a true null. "
            "<bookmark mark='b'/> At lambda one half, the raw estimator is zero or two, equally likely. Its "
            "expectation is one, as proved. <bookmark mark='c'/> Cap at one and the estimator becomes zero or one, "
            "equally likely, with expectation one half. Thus the capped estimator can underestimate the null share "
            "on average. Capping the theoretical mean at one cannot stand in for taking the mean of capped estimates."
        ) as vo:
            step(0)
            for k, mark in enumerate(('a', 'b', 'c')):
                vo.wait_until(mark)
                if k:
                    step(k)
        self.clear_scene()

    def variance(self):
        rows = [cmath(r"I_i=1\{p_i>\lambda\}", r",", r"q_i=P(p_i>\lambda)", font_size=40),
                cmath(r"\operatorname{Var}\widetilde\pi_0", r"=", r"\frac{\sum_iq_i(1-q_i)+2\sum_{i<j}\operatorname{Cov}(I_i,I_j)}{m^2(1-\lambda)^2}", font_size=32),
                cmath(r"\text{all-null, independent}", r":", r"\operatorname{Var}\widetilde\pi_0=\frac{\lambda}{m(1-\lambda)}", font_size=36),
                cmath(r"\operatorname{Corr}(I_i,I_j)=\kappa", r"\Rightarrow", r"\operatorname{Var}\widetilde\pi_0=\frac{\lambda[1+(m-1)\kappa]}{m(1-\lambda)}", font_size=32)]
        whys = [why(r"indicator correlation is different from correlation between the underlying z-statistics"),
                why(r"the general covariance identity; dependence need not always increase variance"),
                why(r"alternatives add their own Bernoulli variances under independence"),
                why(r"fixed positive feasible indicator correlation gives a nonvanishing variance limit")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=0, buff=.5)
        with self.voiceover(
            "Expectation is only one property. <bookmark mark='a'/> Write each count contribution as an indicator. "
            "<bookmark mark='b'/> The variance includes individual Bernoulli variances and every pairwise covariance, "
            "divided by the squared scaling constant. Dependence can increase or decrease it. "
            "<bookmark mark='c'/> Under independent uniform nulls and no alternatives, the variance is lambda over "
            "m times one minus lambda. <bookmark mark='d'/> If the indicators instead have a fixed positive common "
            "correlation, that covariance contribution need not disappear as the test family grows. This is an "
            "indicator-correlation example, not a conversion from a Gaussian factor correlation."
        ) as vo:
            step(0)
            for k, mark in enumerate(('a', 'b', 'c', 'd')):
                vo.wait_until(mark)
                if k:
                    step(k)
        self.clear_scene()

    def analytic_curves(self):
        xs = np.linspace(.1, .9, 81)
        axg = axes([0, 1], [.75, 1.05], x_length=7.1, y_length=4.1, xlabel=r"fixed threshold $\lambda$",
                   ylabel=r"raw estimator expectation", xticks=[0, .5, 1], yticks=[.8, .9, 1.0],
                   font_size=15).move_to(LEFT * 1.5 + DOWN * .15)
        ax = axg.ax
        cols = [COST_C, HURDLE, SKILL_C]
        curves = VGroup()
        for mu, col in zip((1., 2., 3.), cols):
            cut = stats.norm.isf(xs / 2)
            alt_tail = stats.norm.cdf(cut - mu) - stats.norm.cdf(-cut - mu)
            expected = .8 + .2 * alt_tail / (1 - xs)
            curves.add(curve(ax, xs, expected, col, stroke_width=2.5))
        truth = DashedLine(ax.c2p(0, .8), ax.c2p(1, .8), color=GOOD, stroke_width=2)
        side = VGroup(legend([(COST_C, r"$Z\sim N(1,1)$"), (HURDLE, r"$Z\sim N(2,1)$"),
                              (SKILL_C, r"$Z\sim N(3,1)$"), (GOOD, r"true null share $.8$")], font_size=17),
                      wrapped_label(r"Analytical normal-tail expectations; no capped means or Monte Carlo dots.", 4.3, 17)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=.35).next_to(axg, RIGHT, buff=.35)
        fit_right(side)
        with self.voiceover(
            "An analytical example makes the bias visible. <bookmark mark='a'/> Take eighty percent nulls and "
            "two-sided normal p-values. For an alternative with mean mu, the large-p-value probability is the normal "
            "probability between minus c and c, with c set by lambda. <bookmark mark='b'/> Substituting that probability "
            "gives these exact raw-estimator expectation curves for means one, two and three. They are analytical "
            "curves, not new simulations or capped estimates. <bookmark mark='c'/> Strong alternatives contribute "
            "less large-p-value mass here. A general claim that increasing lambda always reduces bias needs "
            "assumptions about alternative tails; an arbitrary alternative distribution need not have that property."
        ) as vo:
            self.play(FadeIn(axg), FadeIn(truth), FadeIn(side), Create(curves[0]), run_time=1.5)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Create(curves[1]), Create(curves[2]), run_time=1.5)
            vo.wait_until('c')
        self.clear_scene()

    def bsw_limits(self):
        cards = VGroup(
            desk_question(r"tail subtraction", r"observed right-tail share minus an estimated zero-null lucky share", width=12.4, font_size=19),
            desk_question(r"power and leakage", r"positive-alpha funds can miss the tail; negative-alpha alternatives can enter it", width=12.4, font_size=19),
            desk_question(r"nonlinear guards", r"capping the null estimate and taking a positive part do not preserve the raw expectation proof", width=12.4, font_size=19),
        ).arrange(DOWN, buff=.25)
        with self.voiceover(
            "Return to the fund decomposition. <bookmark mark='a'/> Subtracting estimated lucky zero-alpha nulls "
            "from a right-tail share gives a useful descriptive component estimate. "
            "<bookmark mark='b'/> Its relation to the positive-alpha population also depends on power and on other "
            "alternatives entering the right tail. <bookmark mark='c'/> The unchanged helper caps the null estimate "
            "and takes the positive part of the subtraction. Those nonlinear operations do not inherit the raw "
            "expectation theorem. We therefore do not claim a universal lower bound on the skilled share from that implementation."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mark in enumerate(('a', 'b', 'c')):
                vo.wait_until(mark)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * .2))
        self.clear_scene()

    def fdr(self, f):
        q = f['q']['0.1']
        rows = [cmath(r"\mathrm{FDP}", r"=", r"V/\max(R,1),\qquad\mathrm{FDR}=\mathbb E[\mathrm{FDP}]", font_size=36),
                cmath(r"k^*", r"=", r"\max\{k:p_{(k)}\le .1\,k/m\}", font_size=42),
                cmath(r"\text{naive }p<.05", r":", rf"R={f['naive_n']},\quad\mathrm{{FDP}}={100*f['naive_fdr']:.0f}\%", font_size=36),
                cmath(r"\text{BH at }.1", r":", rf"R={q['bh']},\quad\mathrm{{FDP}}={100*q['bh_fdr']:.0f}\%", font_size=36)]
        whys = [why(r"V counts selected nonpositive-alpha funds; zero discoveries give FDP zero"),
                why(r"one-sided t p-values; BH control needs valid nulls and independence or suitable positive dependence"),
                why(r"one realised fund population, not an estimate of expected FDR across repeated samples"),
                why(r"the capped two-sided pi0 adaptive version is exploratory; its target null set differs")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=0, buff=.5)
        with self.voiceover(
            "Now distinguish an error fraction from an error rate. <bookmark mark='a'/> False discovery proportion "
            "is false selections divided by selections, using zero when there are no selections. False discovery "
            "rate is its expectation over repeated samples. <bookmark mark='b'/> Here the ordinary BH procedure "
            "uses one-sided t p-values for positive alpha. Valid nulls and independence, or a suitable dependence "
            "condition, justify its error control. <bookmark mark='c'/> In this one simulated population, the naive "
            f"rule selects {f['naive_n']}, with realised false fraction {100*f['naive_fdr']:.0f} percent. "
            f"<bookmark mark='d'/> BH at ten percent selects {q['bh']}, with realised false fraction "
            f"{100*q['bh_fdr']:.0f} percent. That one realised fraction is not expected FDR. The adaptive calculation "
            "uses a capped estimate from two-sided p-values targeting zero alpha, whereas the discovery null includes "
            "negative alpha too; no automatic adaptive-control claim follows."
        ) as vo:
            step(0)
            for k, mark in enumerate(('a', 'b', 'c', 'd')):
                vo.wait_until(mark)
                if k:
                    step(k)
        self.clear_scene()

    def qtable(self, f):
        top = f['top'][:12]
        tab = VGroup(VGroup(*[label(h, font_size=18, color=QC.IDEA) for h in
                              (r"rank", r"$t$", r"adaptive $q$ score", r"known simulation truth")]))
        for x in top:
            tab.add(VGroup(label(str(x['rank']), font_size=18), label(rf"{x['t']:.2f}", font_size=18, color=ACT_C),
                           label(rf"{x['q']:.3f}", font_size=18, color=HURDLE),
                           label(r"positive alpha" if x['skilled'] else r"nonpositive alpha", font_size=17,
                                 color=SKILL_C if x['skilled'] else LUCK_C)))
        for j, row in enumerate(tab):
            for cell, x in zip(row, (-4.7, -2.1, .5, 3.7)):
                cell.move_to([x, 3.05 - .46*j, 0])
        with self.voiceover(
            "The adaptive q scores rank the same simulated funds. <bookmark mark='a'/> They are reverse cumulative "
            "minima of the estimated null share times m times the ordered p-value divided by rank. "
            "<bookmark mark='b'/> They describe thresholds in that estimated tail procedure. They are not posterior "
            "probabilities that individual funds are false, and their calibration requires assumptions beyond the "
            "sorting formula. The truth column is available because this is a simulation; an empirical table would "
            "not know each fund's true alpha."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until('a')
            self.play(LaggedStart(*[FadeIn(r)for r in tab[2:7]], lag_ratio=.15), run_time=1.5)
            vo.wait_until('b')
            self.play(LaggedStart(*[FadeIn(r)for r in tab[7:]], lag_ratio=.15), run_time=1.5)
        self.clear_scene()

    def bg_setting(self):
        rows = [cmath(r"\mu_t=\mathbb E[a\mid\mathcal F_t]", r",", r"b>0,\quad f\ge0", font_size=40),
                cmath(r"A_t", r"=", r"\max\{0,(\mu_t-f)/b\}", font_size=42),
                cmath(r"\eta_{t+1}", r"=", r"a-bA_t-f+\varepsilon_{t+1},\quad\mathbb E_t\varepsilon_{t+1}=0", font_size=34)]
        whys = [why(r"a correctly specified Bayesian conditional mean, with current public information"),
                why(r"nonnegative competitive allocation with linear decreasing returns"),
                why(r"idealised net alpha; the zero-allocation hypothetical return is not an invested dollar")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=0, buff=.6)
        with self.voiceover(
            "The second argument concerns allocation. <bookmark mark='a'/> Under a correctly specified Bayesian "
            "model, mu is the conditional mean of first-dollar skill. Let b be positive scale cost and f the fee. "
            "<bookmark mark='b'/> Competitive investors allocate the positive part of mu minus f, divided by b. "
            "<bookmark mark='c'/> Next period's net alpha is true skill minus scale cost and fee, plus conditionally "
            "mean-zero noise. This is an idealised allocation model, with a known prior and no capacity, liquidity or "
            "flow frictions beyond the linear scale term."
        ) as vo:
            step(0)
            for k, mark in enumerate(('a', 'b', 'c')):
                vo.wait_until(mark)
                if k:
                    step(k)
        self.clear_scene()

    def bg_proof(self):
        rows = [cmath(r"\mathbb E_t\eta_{t+1}", r"=", r"\mu_t-bA_t-f=\min(\mu_t-f,0)", font_size=36),
                cmath(r"A_t>0", r"\Rightarrow", r"\mathbb E_t\eta_{t+1}=0", font_size=40),
                cmath(r"\mathbb E_t[A_t\eta_{t+1}]", r"=", r"0\quad\text{including }A_t=0", font_size=40),
                cmath(r"X_t\in\mathcal F_t", r"\Rightarrow", r"\mathbb E[X_tA_t\eta_{t+1}]=0", font_size=38)]
        whys = [why(r"substitute the positive-part allocation; zero allocation can have negative hypothetical net alpha"),
                why(r"the interior conditional mean cancels, under the assumed Bayesian model"),
                why(r"no invested dollars at the boundary; assume the displayed products are integrable"),
                why(r"tower property for a measurable predictable X; conditioning on future survival changes the question")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=0, buff=.5)
        with self.voiceover(
            "The proof also handles the boundary. <bookmark mark='a'/> Substitute the allocation into the "
            "conditional expectation. The result is the smaller of mu minus the fee and zero. "
            "<bookmark mark='b'/> For a positive allocation, that conditional expected net alpha is zero. "
            "<bookmark mark='c'/> Multiplying by allocated assets gives zero expected dollar alpha even at the "
            "boundary, where no dollars are invested. <bookmark mark='d'/> With integrable products, the tower "
            "property makes that dollar gain orthogonal to current measurable information. It does not say the "
            "hypothetical net return of every inactive fund is a martingale difference, or that a sample selected "
            "for survival next year obeys the same conditional statement."
        ) as vo:
            step(0)
            for k, mark in enumerate(('a', 'b', 'c', 'd')):
                vo.wait_until(mark)
                if k:
                    step(k)
        self.clear_scene()

    def bg_check(self, b):
        rows = VGroup(
            label(rf"with flows, survivor-selected pooled slope: {b['slope']:+.3f}", font_size=24, color=ACT_C),
            label(rf"fixed sizes, pooled slope: {b['slope_fixed']:.3f}", font_size=24, color=SKILL_C),
            label(rf"fixed-size population reference: $.03^2/(.03^2+.05^2)={b['theory_fixed']:.3f}$", font_size=22),
            wrapped_label(r"Finite simulations; repeated fund observations and future-survival selection. Naive pooled "
                          r"standard errors are not valid general confidence intervals or a proof of no persistence.", 11.5, 20, BAD)
        ).arrange(DOWN, buff=.4)
        with self.voiceover(
            "The ordinary simulation is descriptive. <bookmark mark='a'/> Pooling fund-years with assets in both "
            f"years gives slope {b['slope']:+.3f}; that sample uses future survival. "
            f"<bookmark mark='b'/> A separate fixed-size simulation gives {b['slope_fixed']:.3f}, compared with "
            f"the population signal-to-total-variance reference {b['theory_fixed']:.3f}. "
            "<bookmark mark='c'/> Repeated observations share fund skill, and the survivor-selected sample is not "
            "the conditional population used in the proof. The original naive pooled standard errors are therefore "
            "not presented as general confidence intervals. These finite slopes illustrate different allocation "
            "designs; they do not prove the theorem or identify a universal causal effect of flows."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until('c')
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def related(self):
        cards = VGroup(
            desk_question(r"error criteria", r"family-wise error, expected false discovery proportion and local posterior error answer different questions", width=12.4, font_size=19),
            desk_question(r"empirical Bayes", r"a local false discovery probability needs an identified mixture model; a q score alone does not supply one", width=12.4, font_size=19),
            desk_question(r"open problems", r"valid inference with common factors, data-dependent thresholds, changing skill and adaptive research", width=12.4, font_size=19),
        ).arrange(DOWN, buff=.25)
        with self.voiceover(
            "Connections and remaining questions. <bookmark mark='a'/> Family-wise error, expected false discovery "
            "proportion and a local posterior error probability are distinct quantities. "
            "<bookmark mark='b'/> Empirical Bayes can estimate local error probabilities under an appropriate mixture "
            "model; the q-score formula alone is not that model. <bookmark mark='c'/> Common factors, changing "
            "skill, data-chosen thresholds and adaptive research all create additional inference problems. Counting "
            "tests is useful, but it is not a substitute for identifying the null, the information set and the decision rule."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mark in enumerate(('a', 'b', 'c')):
                vo.wait_until(mark)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * .2))
        self.clear_scene()

    def question(self):
        q = pause_card(r"all valid null p-values equal one uniform variable. At $\lambda=1/2$, what are the raw "
                       r"and capped estimator expectations?")
        with self.voiceover(
            "Pause and predict. All valid null p-values equal one uniform variable. At lambda one half, what are "
            "the raw and capped null-share estimator expectations? Explain why dependence alone does not change "
            "the raw expectation, while clipping does."
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
