from __future__ import annotations

import numpy as np

from videos.stats.stats28.common import *  # noqa: F403


class LOO(VoiceoverScene):
    def construct(self):
        self.card()
        self.elpd()
        self.psis()
        self.waic_idea()
        self.schools()
        self.khats()
        self.waic_vs_loo()
        self.compare()

    def card(self):
        card = chapter_card(5, r"Bayesian LOO and WAIC", r"Predictive accuracy from posterior draws", lit=(2010,), part=PART)
        with self.voiceover("Chapter five. Bayesian leave-one-out and WAIC."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def elpd(self):
        rows = [
            cmath(r"\text{elpd}", r"=", r"\textstyle\sum_i E_{\tilde y_i} \log p(\tilde y_i \mid y)", font_size=32),
            cmath(r"\text{elpd}_{\text{loo}}", r"=", r"\textstyle\sum_i \log p(y_i \mid y_{-i})", font_size=32),
            cmath(r"p(y_i \mid y_{-i})", r"=", r"\textstyle\int p(y_i \mid \theta)\, p(\theta \mid y_{-i})\, d\theta", font_size=30),
            cmath(r"\text{cost}", r":", r"n \text{ refits: \ too many with MCMC}", font_size=30),
        ]
        rows[1][2].set_color(LOOC)
        whys = [why(r"expected log predictive density"), why(r"leave each point out in turn"),
                why(r"the posterior predictive without it"), why(r"chapter one of Part 27 helps")]
        with self.voiceover(
            "<bookmark mark='a'/> For Bayesian models, the natural target is the expected log predictive density of new data: "
            "how probable the posterior predictive makes fresh observations. <bookmark mark='b'/> Leave-one-out estimates it "
            "by predicting each observation from the posterior fitted without it. <bookmark mark='c'/> Each term is a "
            "posterior predictive density, an integral over the leave-one-out posterior. <bookmark mark='d'/> Done literally, "
            "that is n separate fits, each an MCMC run. Part 27's importance sampling avoids them."
        ) as vo:
            intro=label('Leave-one-out predicts observations omitted from fitting',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def psis(self):
        rows = [
            cmath(r"\dfrac{p(\theta \mid y_{-i})}{p(\theta \mid y)}", r"\propto", r"\dfrac{1}{p(y_i \mid \theta)}", font_size=32),
            cmath(r"w_s^{(i)}", r"=", r"1/p(y_i \mid \theta_s), \ \ \theta_s \text{ from the full posterior}", font_size=30),
            cmath(r"p(y_i \mid y_{-i})", r"\approx", r"\dfrac{\sum_s w_s^{(i)} p(y_i \mid \theta_s)}{\sum_s w_s^{(i)}}", font_size=30),
            cmath(r"\hat k_i", r":", r"\text{Pareto-smoothed, \ with a diagnostic for every point}", font_size=30),
        ]
        rows[3][2].set_color(LOOC)
        whys = [why(r"removing one likelihood term"), why(r"weights from draws you already have"),
                why(r"importance sampling, \ Part 27"), why(r"Vehtari, Gelman \& Gabry (2017)")]
        with self.voiceover(
            "<bookmark mark='a'/> The leave-one-out posterior differs from the full posterior only by one likelihood "
            "term. <bookmark mark='b'/> So the full posterior's draws can be reweighted by one over that "
            "observation's likelihood. <bookmark mark='c'/> The weighted average then estimates the leave-one-out "
            "predictive density. <bookmark mark='d'/> These weights can have heavy tails, so Aki Vehtari, Andrew "
            "Gelman and Jonah Gabry smooth them with Part 27's Pareto fit, and each estimated k-hat warns about a "
            "deletion's weight-tail stability. The warning threshold depends on effective sample size and is capped "
            "near point seven."
        ) as vo:
            intro=label('Deletion reweighting needs a proper posterior and stable tails',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def waic_idea(self):
        rows = [
            cmath(r"\text{lpd}", r"=", r"\textstyle\sum_i \log \tfrac1S \sum_s p(y_i \mid \theta_s)", font_size=30),
            cmath(r"p_{\text{WAIC}}", r"=", r"\textstyle\sum_i \mathrm{Var}_s \log p(y_i \mid \theta_s)", font_size=30),
            cmath(r"\text{elpd}_{\text{WAIC}}", r"=", r"\text{lpd} - p_{\text{WAIC}}", font_size=32),
            cmath(r"\text{asymptotically}", r":", r"= \text{LOO, \ even for singular models}", font_size=30),
        ]
        rows[2][2].set_color(LOOC)
        whys = [why(r"the in-sample predictive fit"), why(r"an effective number of parameters"),
                why(r"Watanabe (2010)"), why(r"chapter six")]
        with self.voiceover(
            "<bookmark mark='a'/> Sumio Watanabe's WAIC takes another route. Start from the log predictive density of"
            " the observed data, which is optimistic. <bookmark mark='b'/> Estimate the optimism by the posterior "
            "variance of each observation's log likelihood, summed: an effective number of parameters. <bookmark "
            "mark='c'/> Subtract. <bookmark mark='d'/> Under suitable analytic and integrability assumptions, "
            "Watanabe established asymptotic equivalence to Bayesian leave-one-out for important singular-model "
            "settings. This is not a finite-sample guarantee for every model."
        ) as vo:
            intro=label('WAIC estimates a predictive optimism term from posterior variation',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def schools(self):
        d = load("loo")
        hdr = [r"\textbf{eight schools model}", r"\textbf{elpd, \ PSIS-LOO}", r"\textbf{exact LOO}", r"\textbf{$p_{\text{loo}}$}", r"\textbf{WAIC}"]
        body = []
        for k, name in (("pooled", r"complete pooling"), ("hierarchical", r"hierarchical"), ("separate", r"no pooling")):
            v = d[k]
            body.append([name, f"{v['elpd']:.2f}", (f"{v['exact']:.2f}" if v.get("exact") is not None else r"---"),
                         f"{v['p_loo']:.2f}", f"{v['waic']:.2f}"])
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.7, row_buff=0.32, colors=[GREY_A, AICC, HIT, RES])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"higher is better; \ exact LOO: \ refit without each school", font_size=22),
            label(r"whole-school prediction; \ independent priors are explicit, \ and PSIS needs the analytic check", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Compare predictions of a whole left-out school. Complete pooling uses a flat "
            "common-mean prior; the hierarchy uses flat mean and scale priors with a proper posterior. Independent "
            "effects now have explicit normal priors with standard deviation one hundred: a flat prior would leave "
            "the held-out effect undefined. <bookmark mark='b'/> Complete pooling has PSIS score minus thirty point "
            "six zero, versus analytic leave-one-out minus thirty point five six. <bookmark mark='c'/> The hierarchy "
            "gives minus thirty-one point one eight, versus the numerical reference minus thirty-one point three "
            "four. <bookmark mark='d'/> The independent model's PSIS score is minus thirty-six point four six, but "
            "its analytic score is minus forty-four point three three. The failed importance approximation is much "
            "too optimistic. The small pooling-versus-hierarchy difference also needs uncertainty, not just a "
            "ranking."
        ) as vo:
            self.add(schools_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tb[k + 1]))
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def khats(self):
        d = load("loo")
        lab = d["labels"]
        A = axes([-0.6, 7.6], [-0.2, 1.2], x_length=7.6, y_length=4.2, xlabel=r"school", ylabel=r"Pareto $\hat k$",
                 xticks=[], yticks=[0, 0.5, 0.7, 1], center=[-1.8, 0.3, 0])
        ax = A.ax
        thr = DashedLine(ax.c2p(-0.6, 0.7), ax.c2p(7.6, 0.7), color=RES, stroke_width=2)
        groups = {}
        for k, (key, col, dx) in enumerate((("pooled", AICC, -0.2), ("hierarchical", HIT, 0.0), ("separate", RES, 0.2))):
            groups[key] = VGroup(*[Dot(ax.c2p(j + dx, v), radius=0.08, color=col) for j, v in enumerate(d[key]["khat"])])
        names = VGroup(*[label(lab[j], font_size=22, color=GREY_A).next_to(ax.c2p(j, -0.2), DOWN, buff=0.15) for j in range(8)])
        rows = fit_rows(VGroup(
            label(r"blue: \ complete pooling: \ all small", font_size=22, color=AICC),
            label(r"green: \ hierarchical deletion-weight diagnostics", font_size=22, color=HIT),
            label(r"red: \ independent effects; \ high k-hat warns of unstable weights", font_size=22, color=RES),
            label(r"each school dominates its own $\theta_j$", font_size=22, color=GREY_A),
        ), 3.6, 0.42, [5.0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The weight-tail diagnostics help explain these approximations. Complete pooling "
            "shares information across schools, so each deletion changes relatively little. <bookmark mark='b'/> The "
            "hierarchy has more variable deletion weights and needs closer inspection. <bookmark mark='c'/> For "
            "independent effects under the diffuse proper prior, deleting a school's only measurement leaves its "
            "broad prior; reweighting the much narrower full posterior is difficult. <bookmark mark='d'/> Large "
            "k-hats warn against trusting PSIS. Here exact analytic prediction is available; in other cases refit or "
            "integrate out local latent effects. A low k-hat alone would not prove accuracy."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(A), Create(thr), FadeIn(names))
            for k, (key, m_) in enumerate((("pooled", "a"), ("hierarchical", "b"), ("separate", "c"))):
                vo.wait_until(m_)
                self.play(LaggedStart(*[FadeIn(x) for x in groups[key]], lag_ratio=0.1), FadeIn(rows[k]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def compare(self):
        rows = fit_rows(VGroup(
            label(r"report differences in elpd with their SE, \ not just the winner", font_size=24),
            label(rf"pooled minus hierarchical: {load('loo')['comparison']['pooled_minus_hierarchical']:.2f}; rough paired SE {load('loo')['comparison']['paired_se']:.2f}", font_size=24, color=PATH),
            label(r"LOO and WAIC estimate prediction; \ they do not test truth", font_size=24, color=RES),
            label(r"use them to choose, \ or better, \ to weight: \ chapter eight", font_size=24, color=HIT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> When comparing models this way, report the differences in elpd with their standard "
            "errors. <bookmark mark='b'/> For these eight schools the pooling-versus-hierarchy lead is small and "
            "uncertain. The caption reports a rough paired pointwise standard error; with only eight heterogeneous "
            "schools, it needs caution. Four elpd units is a practical heuristic, not a universal decision boundary. "
            "<bookmark mark='c'/> These are estimates of predictive accuracy, not tests of which model is true. "
            "<bookmark mark='d'/> And rather than choose, it is often better to weight, chapter eight."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def waic_vs_loo(self):
        d = load("loo")
        s, h = d["separate"], d["hierarchical"]
        rows = [
            cmath(r"\text{no pooling, \ PSIS-LOO}", r":", rf"{s['elpd']:.2f}, \ \ p_{{\text{{loo}}}} = {s['p_loo']:.2f}", font_size=30),
            cmath(r"\text{no pooling, \ WAIC}", r":", rf"{s['waic']:.2f}, \ \ p_{{\text{{WAIC}}}} = {s['p_waic']:.2f}", font_size=30),
            cmath(r"\text{hierarchical}", r":", rf"\text{{LOO }} {{{h['elpd']:.2f}}}, \ \text{{WAIC }} {{{h['waic']:.2f}}}, \ \text{{exact }} {{{h['exact']:.2f}}}", font_size=28),
            cmath(r"\text{prefer}", r":", r"\text{PSIS-LOO: \ it says when it fails}", font_size=30),
        ]
        rows[1][2].set_color(RES)
        whys = [why(r"explicit independent $N(0,100^2)$ priors"), why(r"compare both approximations with analytic LOO"), why(r"this hierarchy is closer to its numerical reference"),
                why(r"Vehtari, Gelman \& Gabry (2017)")]
        with self.voiceover(
            "<bookmark mark='a'/> With the explicit proper independent-effect priors, compare both approximations "
            "against the analytic leave-one-school-out score of minus forty-four point three three. <bookmark "
            "mark='b'/> PSIS gives about minus thirty-six point five and WAIC about minus thirty-three point nine: "
            "both are too optimistic, with high k-hats warning that importance sampling is unstable. Their difference"
            " is not itself a measurement of the truth. <bookmark mark='c'/> For the hierarchy, both approximations "
            "are much closer to the numerical refit reference. <bookmark mark='d'/> PSIS-LOO is useful because its "
            "tail diagnostics help identify difficult deletions, which should then be checked or refitted."
        ) as vo:
            self.add(schools_tag())
            intro=label('Check both approximations against an independent predictive reference',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
