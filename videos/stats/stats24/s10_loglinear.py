from __future__ import annotations

import numpy as np

from videos.stats.stats24.common import *  # noqa: F403


class LogLinear(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()
        self.idea()
        self.models()
        self.reading()
        self.graphical()
        self.logistic_link()

    def card(self):
        card = chapter_card(9, r"Log-linear models", r"Tables as Poisson regressions", part=PART)
        with self.voiceover("Chapter nine. Log-linear models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def table(self):
        d = load("loglinear")
        c = np.asarray(d["count"])
        hdr = [r"", r"\textbf{18--39}", r"", r"\textbf{40--59}", r"", r"\textbf{60+}", r""]
        sub = [r"", r"not told", r"told", r"not told", r"told", r"not told", r"told"]
        men = [r"\textbf{men}"] + [f"{v:.0f}" for v in c[:6]]
        wom = [r"\textbf{women}"] + [f"{v:.0f}" for v in c[6:]]
        t = table_rows([hdr, sub, men, wom], font_size=26, col_buff=0.5, row_buff=0.3, colors=[GREY_A, GREY_B, BLUE, RED])
        t.move_to([0, 0.8, 0])
        pct = lambda a, b: 100 * b / (a + b)  # noqa: E731
        foot = fit_rows(VGroup(
            label(r"5,000 of the World's adults: \ sex $\times$ age $\times$ told they have high blood pressure", font_size=22),
            label(rf"told, \ men: \ {pct(c[0], c[1]):.0f}\%, {pct(c[2], c[3]):.0f}\%, {pct(c[4], c[5]):.0f}\%; \ "
                  rf"women: \ {pct(c[6], c[7]):.0f}\%, {pct(c[8], c[9]):.0f}\%, {pct(c[10], c[11]):.0f}\%", font_size=22, color=PATH),
            label(r"which associations are real, \ and which follow from others?", font_size=22, color=GREY_A),
        ), 12.0, 0.25, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A three-way table from the World: five thousand adults, classified by sex, age group, and "
            "whether a doctor has told them they have high blood pressure. <bookmark mark='b'/> Among men, eight, seventeen "
            "and forty-four percent have been told, by age group; among women, four, nine and forty-two. "
            "<bookmark mark='c'/> With three variables there are many possible associations. Which are real, and which "
            "follow from the others?"
        ) as vo:
            self.add(simulated_tag())
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in t], lag_ratio=0.2), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def idea(self):
        rows = [
            cmath(r"n_{sat}", r"\sim", r"\text{Poisson}(\mu_{sat})", font_size=30),
            cmath(r"\log\mu_{sat}", r"=", r"\lambda + \lambda^S_s + \lambda^A_a + \lambda^T_t + \lambda^{SA}_{sa} + \lambda^{AT}_{at} + \cdots", font_size=28),
            cmath(r"\text{a missing term}", r"=", r"\text{a restriction; not always an independence}", font_size=30),
            cmath(r"[SA][AT]", r":", r"T \perp S \mid A", font_size=30),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"each cell count, \ a Poisson count"), why(r"main effects and interactions, \ like an ANOVA"),
                why(r"zeros in the model are statements"), why(r"told and sex independent, \ given age")]
        intro = label('Log-linear interactions encode restrictions on a table', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Treat each cell count as a Poisson count. <bookmark mark='b'/> Model its log mean "
            "with main effects and interactions, like an analysis of variance on the log scale: this is a log-linear "
            "model, a Poisson GLM whose design matrix is built from the table's margins. <bookmark mark='c'/> "
            "Specific collections of absent interactions encode independence. Omitting one higher-order interaction "
            "need not imply any conditional independence. <bookmark mark='d'/> The model with only the sex-by-age and"
            " age-by-told interactions, written S A, A T, says that being told is independent of sex once age is "
            "known: conditional independence."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def models(self):
        d = load("loglinear")
        m = d["models"]
        names = [("[SA][T]", r"$T$ independent of age and sex"), ("[SA][AT]", r"$T \perp S \mid A$"),
                 ("[SA][AT][ST]", r"no three-way interaction"), ("saturated", r"everything")]
        hdr = [r"\textbf{model}", r"\textbf{meaning}", r"\textbf{deviance}", r"\textbf{df}", r"$p$"]
        body = [[k.replace("[", r"$[").replace("]", r"]$"), mean, f"{m[k]['deviance']:.1f}", f"{m[k]['df']}",
                 r"$< 10^{-10}$" if m[k]["p"] < 1e-10 else (r"$< 10^{-4}$" if m[k]["p"] < 1e-4 else f"{m[k]['p']:.4f}")] for k, mean in names]
        t = table_rows([hdr] + body, font_size=24, col_buff=0.6, row_buff=0.3, colors=[GREY_A, RES, RES, PATH, HIT])
        t.move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"each step: \ a drop in deviance, \ chapter four", font_size=22),
            label(r"even [SA][AT][ST] fails: \ the sex difference changes with age", font_size=22, color=PATH),
        ), 12.0, 0.25, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fit a ladder of models. Being told independent of both age and sex: deviance eight hundred "
            "on five degrees of freedom, hopeless. <bookmark mark='b'/> Told independent of sex given age: thirty-nine on "
            "three, still rejected, so sex matters even within age groups. <bookmark mark='c'/> All three two-way "
            "associations but no three-way interaction: sixteen on two, p of point oh oo three, also rejected. "
            "<bookmark mark='d'/> Only the saturated model fits. The difference between men and women depends on age, "
            "which is how the World was built: women's blood pressure is lower until about sixty, and then the gap closes."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(t[0]))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(t[k + 1]))
                if k == 2:
                    self.play(FadeIn(foot))
        self.clear_scene()

    def reading(self):
        d = load("loglinear")
        lo, hi = d["st_ci"]
        rows = [
            cmath(r"\lambda^{ST}", r"=", r"\log \text{(odds ratio of told, \ women vs men, \ within age)}", font_size=28),
            cmath(r"[SA][AT][ST]", r":", rf"\text{{OR}} = {d['st_or']:.2f}, \ \ [{lo:.2f}, {hi:.2f}]", font_size=30),
            cmath(r"\text{collapsing}", r":", r"\text{a margin can mislead: \ Simpson, \ Part 5}", font_size=30),
            cmath(r"\text{fitting}", r":", r"\text{IRLS, \ or iterative proportional fitting}", font_size=30),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"interactions are log odds ratios"), why(r"a common odds ratio, \ like Part 14's CMH"),
                why(r"collapsibility needs specific independence conditions"),
                why(r"Deming \& Stephan (1940): \ Part 18's raking")]
        intro = label('A homogeneous odds-ratio fit is a model-based summary', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The interaction terms are log odds ratios. <bookmark mark='b'/> In the model "
            "without a three-way term, the sex-by-told term is a common odds ratio across age groups, point six "
            "eight: women are less often told, at any given age. It is a homogeneous-association likelihood estimate,"
            " related to but not generally identical to Mantel–Haenszel's ratio-of-sums estimate. This common-odds "
            "model was rejected here, so its estimate is only a summary of varying age-group associations. <bookmark "
            "mark='c'/> Log-linear models also say when it is safe to collapse a table over a variable, the question "
            "behind Simpson's paradox. <bookmark mark='d'/> They're fitted by IRLS, or by iterative proportional "
            "fitting, which is Part 18's raking applied to model margins."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def graphical(self):
        rows = [
            cmath(r"\text{graph}", r":", r"\text{a node per variable; all maximal-clique interactions}", font_size=30),
            cmath(r"\text{separation}", r":", r"A \text{ separates } S \text{ and } T \Rightarrow S \perp T \mid A", font_size=30),
            cmath(r"\text{hierarchical}", r":", r"\text{keep a term } \Rightarrow \text{ keep every sub-term}", font_size=30),
            cmath(r"\text{many variables}", r":", r"\text{a sparse graph \ = \ a few interactions}", font_size=30),
        ]
        rows[1][-1].set_color(PATH)
        whys = [why(r"Darroch, \ Lauritzen \& Speed (1980)"), why(r"read independences off the picture"), why(r"the usual convention"), why(r"Part 31: \ Gaussian graphical models")]
        intro = label('Graphical models include every maximal-clique interaction', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Log-linear models have pictures. For a graphical log-linear model, draw one node "
            "per variable and include all interactions within each maximal clique. <bookmark mark='b'/> If every path"
            " between two variables passes through a third, they're conditionally independent given it: the model S "
            "A, A T is a chain with age in the middle. <bookmark mark='c'/> Graphical models are a subset of "
            "hierarchical models. The all-pairs, no-three-way model on three variables is hierarchical but not "
            "graphical: its complete graph would also require the three-way interaction. <bookmark mark='d'/> For "
            "positive model cell probabilities, graph separation gives conditional independences. Sparse graphs "
            "restrict clique interactions, the starting point of graphical models, which Part 31 develops for "
            "continuous data."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def logistic_link(self):
        rows = fit_rows(VGroup(
            label(r"when one variable is a response: \ a log-linear model with all its predictors' margins fixed", font_size=24),
            label(r"is the logistic regression of that response on the others", font_size=24, color=MODEL),
            label(r"the Poisson and multinomial likelihoods give the same $\hat\beta$", font_size=24, color=HIT),
            label(r"the Poisson trick: \ fit a multinomial with Poisson software", font_size=24, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> When one variable is naturally the response, being told, a log-linear model that "
            "includes every interaction among the predictors <bookmark mark='b'/> is the same as a logistic "
            "regression of the response on them. <bookmark mark='c'/> With the required saturated predictor margins "
            "or stratum-specific nuisance intercepts, Poisson and conditional multinomial likelihoods give the same "
            "response-association estimates. <bookmark mark='d'/> That's the Poisson trick, and it's how the next "
            "chapter's multinomial models can be fitted with ordinary Poisson software."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
