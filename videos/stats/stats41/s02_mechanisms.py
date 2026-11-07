from __future__ import annotations

import numpy as np

from videos.stats.stats41.common import *  # noqa: F403


class Mechanisms(VoiceoverScene):
    def construct(self):
        self.card()
        self.notation()
        self.three()
        self.grid()
        self.who()
        self.patterns()
        self.ignorability()
        self.graphs()
        self.dropout()
        self.untestable()

    def card(self):
        card = chapter_card(1, r"Mechanisms", r"Why is it missing?", lit=(1976,), part=PART)
        with self.voiceover("Chapter one. Mechanisms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def notation(self):
        rows = [
            cmath(r"Y", r"=", r"(Y_{\text{obs}}, Y_{\text{mis}})", font_size=34),
            cmath(r"R", r":", r"\text{the response indicators: \ } R_{ij} = 1 \text{ if } Y_{ij} \text{ is seen}", font_size=30),
            cmath(r"\text{the mechanism}", r":", r"P(R \mid Y, \phi)", font_size=32),
            cmath(r"\text{the question}", r":", r"\text{on what does } R \text{ depend?}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"seen and unseen"), why(r"a mask, \ a random variable"), why(r"Rubin (1976)"), why(r"three answers")]
        with self.voiceover(
            "<bookmark mark='a'/> Donald Rubin's paper of 1976 set out the framework. Split the data into the observed "
            "and the missing parts. <bookmark mark='b'/> Record which is which in a matrix R of response indicators, and "
            "treat R itself as random. <bookmark mark='c'/> The missing-data mechanism is the distribution of R given the "
            "data. <bookmark mark='d'/> Everything depends on what R depends on."
        ) as vo:
            heading = label('The response mask is part of the statistical model', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def three(self):
        rows = [
            cmath(r"\text{MCAR}", r":", r"P(R \mid Y) = P(R): \ \text{a coin}", font_size=32),
            cmath(r"\text{MAR}", r":", r"P(R \mid Y) = P(R \mid Y_{\text{obs}}): \ \text{explained by what we see}", font_size=30),
            cmath(r"\text{MNAR}", r":", r"P(R \mid Y) \text{ depends on } Y_{\text{mis}}: \ \text{the reason is hidden too}", font_size=30),
            cmath(r"\text{e.g. income}", r":", r"\text{a lost form; \ the young answer less; \ the rich refuse}", font_size=30),
        ]
        rows[1][-1].set_color(MIC)
        whys = [why(r"completely at random"), why(r"at random, \ given the observed"), why(r"not at random"), why(r"one each")]
        with self.voiceover(
            "<bookmark mark='a'/> Three answers. Missing completely at random: the mask is a coin, independent of the"
            " variables whose missingness is being modelled. <bookmark mark='b'/> Missing at random, a misleading "
            "name: the chance of being missing may depend on the data, but only on parts we observe. <bookmark "
            "mark='c'/> Missing not at random: it depends on the missing values themselves, so the reason is hidden "
            "along with the data. <bookmark mark='d'/> For income on a survey: a form lost in the post is completely "
            "at random; younger people skipping the question is at random, if age is recorded; the well-off refusing "
            "to say is not at random."
        ) as vo:
            heading = label('Missingness mechanisms depend on what is observed', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def grid(self):
        d = load("mech")["grid"]
        G = MaskGrid(24, [r"age", r"sex", r"region", r"BMI", r"income"], cell_w=0.95, cell_h=0.2, center=[-3.4, -0.1, 0])
        side = fit_rows(VGroup(
            label(r"the World's survey: \ 2,000 adults, \ 5 questions", font_size=22),
            label(r"blue: \ answered; \ dark: \ income withheld", font_size=22, color=GREY_A),
            label(r"MCAR: \ scattered at random", font_size=22, color=OBSV),
            label(r"MAR: \ more among the young", font_size=22, color=MIC),
            label(r"MNAR: \ more among the well-off", font_size=22, color=MNC),
        ), 4.6, 0.42, [3.8, 0.4, 0])
        ages = np.asarray(d["age"], float)
        age_lab = VGroup(*[MathTex(f"{int(a)}", font_size=16, color=GREY_B).next_to(G.cells[i][0], LEFT, buff=0.1) for i, a in enumerate(ages)])
        with self.voiceover(
            "<bookmark mark='a'/> The World's survey: two thousand adults asked five questions; here are the first "
            "twenty-four respondents, one row each, with their ages on the left. <bookmark mark='b'/> Thirty percent "
            "withhold their income, under three different mechanisms whose truth only the World knows. <bookmark "
            "mark='c'/> Completely at random, the dark cells are scattered. <bookmark mark='d'/> At random, they gather "
            "among the young. <bookmark mark='e'/> Not at random, they gather among the best-paid, which, crucially, we "
            "cannot see from the table."
        ) as vo:
            self.add(missing_tag())
            vo.wait_until("a")
            self.play(FadeIn(G), FadeIn(age_lab), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            for m_, key, k in (("c", "mcar", 2), ("d", "mar", 3), ("e", "mnar", 4)):
                vo.wait_until(m_)
                self.play(*[c.animate.set_fill(OBSV, opacity=0.8).set_stroke(width=0) for c in G.column(4)], run_time=0.4)
                self.play(*G.mark(4, d[key]), FadeIn(side[k]))
        self.clear_scene()

    def who(self):
        d = load("mech")
        rows = [[r"income withheld:", r"MCAR", r"MAR", r"MNAR"],
                [r"mean age, \ missing", f"{d['mcar']['miss_age']:.1f}", f"{d['mar']['miss_age']:.1f}", f"{d['mnar']['miss_age']:.1f}"],
                [r"mean age, \ observed", f"{d['mcar']['obs_age']:.1f}", f"{d['mar']['obs_age']:.1f}", f"{d['mnar']['obs_age']:.1f}"],
                [r"mean log income, \ missing \ (hidden)", f"{d['mcar']['miss_inc']:.2f}", f"{d['mar']['miss_inc']:.2f}", f"{d['mnar']['miss_inc']:.2f}"],
                [r"mean log income, \ observed", f"{d['mcar']['obs_inc']:.2f}", f"{d['mar']['obs_inc']:.2f}", f"{d['mnar']['obs_inc']:.2f}"]]
        tab = table_rows(rows, font_size=26, col_buff=0.9, row_buff=0.34, colors=[GREY_A, None, None, MNC, OBSV]).move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"MAR shows itself: \ the missing are younger, \ which we can see", font_size=24, color=MIC),
            label(r"MNAR hides: \ the missing are richer, \ which we cannot", font_size=24, color=MNC),
        ), 12.4, 0.3, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Compare the missing with the observed. <bookmark mark='b'/> Under the coin, they are "
            "alike in age. Under missing at random, those who withheld income are about twelve years younger, a "
            "difference the data reveal. <bookmark mark='c'/> Under missing not at random, the ages barely differ, but the "
            "hidden incomes of the refusers are about twice as high, in geometric mean, and nothing in "
            "the observed data says so."
        ) as vo:
            self.add(missing_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]), FadeIn(foot[1]))
        self.clear_scene()

    def ignorability(self):
        rows = [
            cmath(r"L(\theta, \phi \mid Y_{\text{obs}}, R)", r"=", r"\textstyle\int f(Y_{\text{obs}}, Y_{\text{mis}} \mid \theta)\, P(R \mid Y, \phi)\, dY_{\text{mis}}", font_size=28),
            cmath(r"\text{MAR}", r":", r"P(R \mid Y, \phi) = P(R \mid Y_{\text{obs}}, \phi) \ \text{leaves the integral}", font_size=30),
            cmath(r"\phantom{L}", r"=", r"P(R \mid Y_{\text{obs}}, \phi) \cdot f(Y_{\text{obs}} \mid \theta)", font_size=30),
            cmath(r"\text{ignorable}", r":", r"\text{MAR and distinct } \theta, \phi: \ \text{maximize } f(Y_{\text{obs}} \mid \theta) \text{ alone}", font_size=28),
        ]
        rows[3][-1].set_color(MIC)
        whys = [why(r"the full likelihood"), why(r"it does not involve $Y_{\text{mis}}$"), why(r"it factors"), why(r"Rubin's theorem")]
        with self.voiceover(
            "<bookmark mark='a'/> Why the distinction matters. The likelihood of what we saw, both the data and the "
            "mask, integrates over the missing values. <bookmark mark='b'/> Under missing at random, the mechanism "
            "depends only on observed values, so it comes out of the integral. <bookmark mark='c'/> The likelihood "
            "factors into a part for the mechanism and the ordinary likelihood of the observed data. <bookmark "
            "mark='d'/> If, in addition, their parameters are distinct, with a variation-independent parameter "
            "space, we can ignore the mechanism entirely and maximize the observed-data likelihood under a correctly "
            "specified observed-data model. Bayesian ignorability also needs the relevant prior factorization. Under "
            "MNAR, the mechanism must be modelled."
        ) as vo:
            heading = label('Likelihood ignorability needs MAR and distinct parameters', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def graphs(self):
        rows = fit_rows(VGroup(
            label(r"missingness graphs \ (Mohan \& Pearl 2021): \ draw $R$ as a node in the causal graph", font_size=26, color=TAUC),
            label(r"simple sufficient graph examples; hidden common causes also matter", font_size=26),
            label(r"some MNAR graphs still allow consistent estimates of some quantities", font_size=26, color=MIC),
            label(r"and the graph says which assumption each method needs", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Karthika Mohan and Judea Pearl draw the mechanism as part of a causal graph, with "
            "the response indicator as a node. <bookmark mark='b'/> In a simple graph without hidden common causes, "
            "no data-variable arrows into the response indicator is sufficient for completely at random; arrows only "
            "from always-observed variables can represent missing at random. General missingness graphs require more "
            "care than these sufficient examples. <bookmark mark='c'/> Graphs show that some MNAR situations still "
            "allow some quantities, such as a regression of y on x, to be estimated consistently, <bookmark "
            "mark='d'/> and they make explicit which assumption each method rests on: Part thirty-six's back-door "
            "reasoning applied to the mask."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def untestable(self):
        rows = fit_rows(VGroup(
            label(r"MCAR has testable implications; failure to reject does not prove it (Little 1988)", font_size=26, color=OBSV),
            label(r"MAR versus MNAR is not: \ every MNAR model has a MAR twin that fits the data equally well", font_size=26, color=MNC),
            label(r"so: \ argue MAR from how the data were collected, \ and test how much it matters", font_size=26, color=TAUC),
            label(r"chapter 6: \ sensitivity analysis and tipping points", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Which mechanism holds? Completely at random can be tested: systematic differences "
            "on observed variables can contradict it, allowing for sampling variation and the test’s modelling "
            "assumptions. Failure to reject does not establish MCAR. Roderick Little gave the standard test in 1988. "
            "<bookmark mark='b'/> But missing at random against not at random cannot be tested: for every MNAR model "
            "there is a MAR model that fits the observed data exactly as well, as Geert Molenberghs, Michael Kenward "
            "and colleagues proved in 2008. <bookmark mark='c'/> So MAR is argued from how the data were collected, "
            "and its importance is measured by sensitivity analysis, <bookmark mark='d'/> the subject of chapter six."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def patterns(self):
        rows = fit_rows(VGroup(
            label(r"patterns: \ monotone \ (a dropout never returns) \ or arbitrary \ (holes anywhere)", font_size=26, color=TAUC),
            label(r"monotone patterns allow sequential methods: \ impute visit by visit", font_size=26, color=None),
            label(r"unit nonresponse \ (nobody answered) \ vs item nonresponse \ (one question skipped)", font_size=26, color=GREY_A),
            label(r"the first is usually weighted, \ the second imputed", font_size=26, color=MIC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Missingness also has a shape. In a monotone pattern, once a value is missing all later ones "
            "are too, like a patient who leaves a trial and never returns; otherwise the holes are arbitrary. <bookmark "
            "mark='b'/> Monotone patterns allow simpler, sequential methods: impute the first visit, then the next given "
            "the first, and so on. <bookmark mark='c'/> Surveys distinguish unit nonresponse, where a person does not take "
            "part at all, from item nonresponse, where they skip one question. <bookmark mark='d'/> The first is usually "
            "handled by weighting, the second by imputation."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def dropout(self):
        rows = fit_rows(VGroup(
            label(r"in a trial, \ dropout that depends on the last visit's symptoms: \ MAR", font_size=26, color=MIC),
            label(r"dropout that depends on how one feels \ after the last visit: \ MNAR", font_size=26, color=MNC),
            label(r"the difference is often a matter of how often you measure", font_size=26, color=TAUC),
            label(r"collect the reasons for dropout: \ they are data about the mechanism", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In a trial the distinction becomes concrete. If patients leave because of symptoms recorded "
            "at their last visit, the dropout is missing at random given the recorded history. <bookmark mark='b'/> If they "
            "leave because of how they felt in the weeks after it, which was never recorded, it is not. <bookmark "
            "mark='c'/> So the difference is often a matter of how often outcomes are measured. <bookmark mark='d'/> And the "
            "reasons patients give for leaving are themselves data about the mechanism, worth collecting carefully."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

