from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats27.common import *  # noqa: F403

PC = {"narrow": RES, "wide": SAMPLER, "t3": HIT}
PN = {"narrow": r"$N(0, 0.5^2)$", "wide": r"$N(0, 3^2)$", "t3": r"Student $t_3$"}


class Importance(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.weights()
        self.table()
        self.optimal()
        self.reweight()
        self.psis_idea()

    def card(self):
        card = chapter_card(1, r"Importance sampling", r"Sample from the wrong distribution, \ reweight", lit=(), part=PART)
        with self.voiceover("Chapter one. Importance sampling."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"E_\pi f", r"=", r"\textstyle\int f(x)\,\frac{\pi(x)}{q(x)}\,q(x)\,dx", font_size=32),
            cmath(r"\hat E", r"=", r"\dfrac{\sum_s w_s f(x_s)}{\sum_s w_s}, \ \ x_s \sim q, \ \ w_s = \dfrac{\pi(x_s)}{q(x_s)}", font_size=30),
            cmath(r"\text{ESS}", r"=", r"\dfrac{(\sum w_s)^2}{\sum w_s^2}", font_size=32),
            cmath(r"\text{danger}", r":", r"q \text{ too light-tailed: \ weights can have infinite variance}", font_size=28),
        ]
        rows[1][2].set_color(SAMPLER)
        whys = [why(r"multiply and divide by a proposal $q$"), why(r"self-normalized: \ $\pi$ need not be normalized"),
                why(r"Kish's effective sample size"), why(r"a few huge weights dominate")]
        with self.voiceover(
            "<bookmark mark='a'/> The simplest Monte Carlo trick for a distribution you can't sample: sample from one"
            " you can, covering the target support, and correct. Multiply and divide by a proposal density q. "
            "<bookmark mark='b'/> Draw from q, weight each draw by the ratio of target to proposal, and take a "
            "weighted average; normalizing by the sum of the weights means the target's constant cancels. <bookmark "
            "mark='c'/> Kish's effective sample size summarizes weight concentration. It is a heuristic, not the "
            "accuracy of every integrand. <bookmark mark='d'/> The danger: if the proposal has lighter tails than the"
            " target, a rare draw far out gets an enormous weight, and the estimator's variance can be infinite."
        ) as vo:
            intro = label('Importance weights require proposal support across the target', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def weights(self):
        d = load("importance")
        group = VGroup()
        anims = []
        for k, key in enumerate(("narrow", "wide", "t3")):
            P_ = d["props"][key]
            x, w = np.asarray(P_["x"]), np.asarray(P_["w"])
            ymax = max(float(w.max()) * 1.1, 2.5)
            A = axes([-6, 6], [0, ymax], x_length=3.8, y_length=2.8, xlabel=rf"draws from {PN[key]}", ylabel=r"",
                     xticks=[-4, 0, 4], yticks=[], center=[-4.5 + 4.5 * k, 0.7, 0])
            sticks = VGroup(*[Line(A.ax.c2p(a, 0), A.ax.c2p(a, b), color=PC[key], stroke_width=1.5, stroke_opacity=0.7)
                              for a, b in zip(x, w) if -6 <= a <= 6])
            info = label(rf"max weight {100 * P_['max_w']:.1f}\% \ of the total", font_size=20, color=PC[key]).next_to(A, DOWN, buff=0.25)
            group.add(A)
            anims.append((sticks, info))
        foot = fit_rows(VGroup(
            label(r"target: \ $N(0, 1)$; \ each stick is one draw's weight", font_size=22),
            label(r"too narrow: \ the tails get a handful of giant weights", font_size=22, color=RES),
        ), 12.0, 0.2, [0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Three proposals for a standard normal target, two thousand draws each; each stick is one "
            "draw's weight. <bookmark mark='b'/> A proposal narrower than the target, standard deviation a half, almost "
            "never reaches the tails, so when it does the weight is huge: one draw carries eleven percent of the total. "
            "<bookmark mark='c'/> A wide normal wastes draws far out, but its weights are bounded. <bookmark mark='d'/> A "
            "Student t, with heavier tails than the target, gives nearly even weights: the best of the three."
        ) as vo:
            self.play(FadeIn(group), FadeIn(foot[0]))
            vo.wait_until("a")
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                sticks, info = anims[k]
                self.play(LaggedStart(*[Create(s_) for s_ in sticks], lag_ratio=0.002), FadeIn(info), run_time=1.5)
                if k == 0:
                    self.play(FadeIn(foot[1]))
        self.clear_scene()

    def table(self):
        d = load("importance")
        hdr = [r"\textbf{proposal}", r"\textbf{estimate of } $E\,x^2 = 1$", r"\textbf{after PSIS}", r"\textbf{ESS of 2,000}", r"\textbf{$\hat k$}"]
        body = [[PN[k], f"{d['props'][k]['est']:.3f}", f"{d['props'][k]['est_psis']:.3f}", f"{d['props'][k]['ess']:,.0f}",
                 f"{d['props'][k]['khat']:.2f}"] for k in ("narrow", "wide", "t3")]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.7, row_buff=0.3, colors=[GREY_A, RES, SAMPLER, HIT])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"the narrow proposal: \ wrong by 30\%, \ and its ESS of 62 looks respectable", font_size=22, color=RES),
            label(r"$\hat k > 0.7$: \ the Pareto tail of the weights says do not trust it", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Estimating the variance, whose true value is one. <bookmark mark='b'/> The narrow "
            "proposal gives one point three one, thirty percent wrong. Worse, its effective sample size of sixty-two "
            "looks respectable, because the ESS is computed from the same unreliable weights. <bookmark mark='c'/> "
            "The wide normal and the t give about one point oo five and one point oo three, much closer in this run. "
            "<bookmark mark='d'/> The last column is the honest alarm: the Pareto shape k-hat, next."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[1]), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(tb[2]), FadeIn(tb[3]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def optimal(self):
        d = load("importance")["tail"]
        rows = [
            cmath(r"q^*(x)", r"\propto", r"|f(x)|\,\pi(x)", font_size=32),
            cmath(r"P(X > 3)", r"=", rf"{d['truth']:.5f}, \ \ X \sim N(0, 1)", font_size=30),
            cmath(r"\text{naive}, \ n = 2{,}000", r":", rf"{d['naive']:.4f}, \ \ \text{{SD }} {d['sd_naive']:.5f}", font_size=30),
            cmath(r"q = N(3.15, 1)", r":", rf"{d['is']:.5f}, \ \ \text{{SD }} {d['sd_is']:.6f}", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"ordinary IS; \ zero variance if $f$ has one sign"), why(r"a rare event"),
                why(r"only about 3 draws land beyond 3"), why(r"16 times smaller error")]
        with self.voiceover(
            "<bookmark mark='a'/> Importance sampling can also beat sampling from the target itself. For ordinary "
            "importance sampling with a normalized target, the minimum-variance proposal is proportional to the "
            "absolute value of f times pi. It has zero variance when f has one sign. The self-normalized estimator "
            "has a different optimum. <bookmark mark='b'/> Take the rare event that a standard normal exceeds three, "
            "probability point oo one three five. <bookmark mark='c'/> Sampling the normal directly, two thousand "
            "draws see about three such events, and the estimate's standard deviation is point oo oo nine, nearly as "
            "large as the answer. <bookmark mark='d'/> Proposing from a normal centred just beyond three, many more "
            "draws reach the event, and the error is sixteen times smaller. Rare-event simulation, in engineering and"
            " finance, is built on this."
        ) as vo:
            intro = label('Optimal proposals depend on the estimator and integrand', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def psis_idea(self):
        rows = [
            cmath(r"\text{fit}", r":", r"\text{a generalized Pareto to the largest } M \text{ weights}", font_size=30),
            cmath(r"\hat k", r":", r"\text{positive population } k: \ E(w^r)<\infty \text{ for } r<1/k", font_size=30),
            cmath(r"\hat k < 0.7", r":", r"\text{smoothing can help; \ still check Monte Carlo error}", font_size=30),
            cmath(r"\hat k > 0.7", r":", r"\text{warning: \ improve proposal, \ draws, \ or refit}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"Vehtari, Simpson, Gelman, Yao \& Gabry (2024)"), why(r"$k \ge 0.5$: \ infinite variance in the Pareto-tail model"),
                why(r"Pareto-smoothed importance sampling"), why(r"used again: \ LOO in Part 28, \ VI in chapter ten")]
        with self.voiceover(
            "<bookmark mark='a'/> Pareto-smoothed importance sampling, from Aki Vehtari and colleagues, fits a "
            "generalized Pareto distribution to the largest weights. <bookmark mark='b'/> Its estimated shape "
            "diagnoses the weight tail. For a positive population shape k, moments of order below one over k exist; a"
            " shape at least a half implies infinite variance. A fitted k-hat is a noisy diagnostic, not proof of "
            "that property. <bookmark mark='c'/> Below a sample-size-dependent threshold capped at point seven, "
            "Pareto smoothing can stabilize the estimate. Low k-hat alone does not guarantee accuracy. <bookmark "
            "mark='d'/> Above it, as for the narrow proposal's point nine three, the estimate is unreliable; "
            "improving the proposal, collecting more effective draws or refitting may be necessary. Part 28 uses it "
            "for cross-validation, and chapter ten to check variational approximations."
        ) as vo:
            intro = label('Pareto tail estimates diagnose weight stability', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def reweight(self):
        rows = [
            cmath(r"\text{draws from}", r":", r"p(\theta \mid y) \text{ under prior } p_0", font_size=30),
            cmath(r"\text{a new prior } p_1", r":", r"w_s = p_1(\theta_s)/p_0(\theta_s)", font_size=30),
            cmath(r"\text{one observation left out}", r":", r"w_s = 1/p(y_i \mid \theta_s)", font_size=30),
            cmath(r"\text{both}", r":", r"\text{check support, \ effective draws and weight tails}", font_size=30),
        ]
        rows[3][-1].set_color(HIT)
        whys = [why(r"existing MCMC draws"), why(r"prior sensitivity, \ for free"), why(r"leave-one-out: \ Part 28"), why(r"check the weights' tail")]
        with self.voiceover(
            "<bookmark mark='a'/> Importance sampling also recycles draws you already have. Suppose you sampled a posterior "
            "under one prior. <bookmark mark='b'/> To see the posterior under another, weight each draw by the ratio of the "
            "new prior to the old: a sensitivity analysis without refitting. <bookmark mark='c'/> Weighting each draw by one "
            "over the likelihood of a single observation gives the posterior with that observation left out, the trick "
            "behind Part 28's fast cross-validation. <bookmark mark='d'/> Both are only as good as the weights, so both are "
            "checked by k-hat."
        ) as vo:
            intro = label('Reweighting needs overlap, stable weights and effective draws', font_size=36).move_to([0, 3.3, 0])
            if intro.width > 12.5: intro.width = 12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
