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
            "<bookmark mark='a'/> The leave-one-out posterior differs from the full posterior only by one likelihood term. "
            "<bookmark mark='b'/> So the full posterior's draws can be reweighted by one over that observation's likelihood. "
            "<bookmark mark='c'/> The weighted average then estimates the leave-one-out predictive density. "
            "<bookmark mark='d'/> These weights can have heavy tails, so Aki Vehtari, Andrew Gelman and Jonah Gabry smooth them "
            "with Part 27's Pareto fit, and the k-hat for each observation says whether its estimate can be trusted."
        ) as vo:
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
            "<bookmark mark='a'/> Sumio Watanabe's WAIC takes another route. Start from the log predictive density of the "
            "observed data, which is optimistic. <bookmark mark='b'/> Estimate the optimism by the posterior variance of each "
            "observation's log likelihood, summed: an effective number of parameters. <bookmark mark='c'/> Subtract. "
            "<bookmark mark='d'/> Watanabe proved that this matches leave-one-out asymptotically, even for the singular "
            "models of chapter six where AIC and BIC both break."
        ) as vo:
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
            label(r"pooling predicts a left-out school best; \ no pooling worst, \ with an unreliable estimate", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 26's eight schools, under three models, compared by how well they predict a left-out "
            "school's estimate. <bookmark mark='b'/> Complete pooling scores minus thirty point five six, its PSIS estimate "
            "matching exact leave-one-out to the second decimal. <bookmark mark='c'/> The hierarchical model scores minus "
            "thirty-one point two one, against an exact minus thirty-one point three four, with about one and a half effective "
            "parameters. <bookmark mark='d'/> No pooling is worst, minus thirty-seven, and its effective number of parameters, "
            "almost seven, says it is predicting each school from almost nothing. For these data, the simplest model predicts "
            "best."
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
            label(r"green: \ hierarchical: \ about 0.4--0.7", font_size=22, color=HIT),
            label(r"red: \ no pooling: \ above 0.7: \ do not trust", font_size=22, color=RES),
            label(r"each school dominates its own $\theta_j$", font_size=22, color=GREY_A),
        ), 3.6, 0.42, [5.0, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The k-hats explain the last line. Under complete pooling, leaving one school out barely "
            "changes the posterior, and every k-hat is small. <bookmark mark='b'/> Under the hierarchical model they run "
            "from point four to point seven: usable, with care. <bookmark mark='c'/> Under no pooling, each school's effect is "
            "determined by that school alone, so removing it changes everything, and most k-hats exceed point seven. "
            "<bookmark mark='d'/> There the PSIS estimate shouldn't be trusted, and the remedy is to refit those cases exactly, "
            "which the diagnostic tells you to do."
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
            label(r"differences under 4, \ or under 2 SE: \ the data barely distinguish the models", font_size=24, color=PATH),
            label(r"LOO and WAIC estimate prediction; \ they do not test truth", font_size=24, color=RES),
            label(r"use them to choose, \ or better, \ to weight: \ chapter eight", font_size=24, color=HIT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> When comparing models this way, report the differences in elpd with their standard errors. "
            "<bookmark mark='b'/> A difference smaller than about four, or than two standard errors, means the data barely "
            "distinguish the models: complete pooling's lead over the hierarchical model here is well within that. "
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
        whys = [why(r"8 parameters for 8 schools"), why(r"three too optimistic"), why(r"both close when all is well"),
                why(r"Vehtari, Gelman \& Gabry (2017)")]
        with self.voiceover(
            "<bookmark mark='a'/> When the k-hats are high, WAIC and PSIS-LOO part company. For no pooling, PSIS-LOO counts "
            "almost seven effective parameters, close to the eight there are. <bookmark mark='b'/> WAIC counts four, and scores "
            "the model three points too well. <bookmark mark='c'/> For the hierarchical model, where all is well, the two agree "
            "with each other and with exact leave-one-out to within a few tenths. <bookmark mark='d'/> Vehtari, Gelman and "
            "Gabry therefore recommend PSIS-LOO: they behave alike when both work, and only one of them tells you when it "
            "doesn't."
        ) as vo:
            self.add(schools_tag())
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
