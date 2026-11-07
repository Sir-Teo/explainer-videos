from __future__ import annotations

import numpy as np

from videos.stats.stats15.common import *  # noqa: F403


class Hypotheses(VoiceoverScene):
    def construct(self):
        self.card()
        self.odds()
        self.coin()
        self.lindley()
        self.births_bf()
        self.bound()
        self.scale()

    def card(self):
        card = chapter_card(10, r"Hypotheses, \ the Bayesian way", r"Posterior odds and Bayes factors, \ a first look", lit=(1939,), part=PART)
        with self.voiceover("Chapter ten. Hypotheses, the Bayesian way."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def odds(self):
        rows = [
            cmath(r"\frac{P(H_1 \mid y)}{P(H_0 \mid y)}", r"=", r"\frac{p(y \mid H_1)}{p(y \mid H_0)} \times \frac{P(H_1)}{P(H_0)}", font_size=34),
            cmath(r"\text{BF}_{10}", r"=", r"\frac{p(y \mid H_1)}{p(y \mid H_0)}", font_size=34),
            cmath(r"p(y \mid H_1)", r"=", r"\int p(y \mid \theta)\,\pi(\theta \mid H_1)\,d\theta", font_size=32),
            cmath(r"\text{posterior odds}", r"=", r"\text{BF} \times \text{prior odds}", font_size=32),
        ]
        rows[1][2].set_color(POST)
        whys = [why(r"Part 2's odds form of Bayes's rule"), why(r"the Bayes factor: \ how much the data shift the odds"),
                why(r"the marginal likelihood: \ averaged over $H_1$'s prior"), why(r"Jeffreys (1939)")]
        intro = label('Update model odds using marginal likelihoods', font_size=36)
        with self.voiceover(
            "Can a Bayesian test a hypothesis? <bookmark mark='a'/> Use Part 2's odds form of Bayes's rule, with two hypotheses "
            "instead of two diseases: the posterior odds of H one against H zero equal the ratio of how well each predicted the "
            "data, times the prior odds. <bookmark mark='b'/> That ratio is the Bayes factor, the factor by which the data "
            "multiply the odds, whatever they were. <bookmark mark='c'/> For a hypothesis that leaves a parameter free, how well it "
            "predicted the data means its likelihood averaged over its own prior: the marginal likelihood. "
            "<bookmark mark='d'/> Harold Jeffreys built a whole theory of testing on this, in 1939."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def coin(self):
        d = load("bf")
        rows = [
            cmath(r"H_0: p = \tfrac12", r",", r"H_1: p \sim \text{Uniform}(0, 1)", font_size=32),
            cmath(r"60 \text{ heads in } 100", r":", rf"\text{{two-sided }} p = {d['p60']:.3f}", font_size=32),
            cmath(r"\text{BF}_{10}", r"=", rf"\frac{{B(61, 41)}}{{2^{{-100}}}} = {d['bf60']:.2f}", font_size=32),
            cmath(r"P(H_0 \mid y)", r"=", rf"\frac{{1}}{{1 + {d['bf60']:.2f}}} = {1 / (1 + d['bf60']):.2f}\ \text{{(even prior odds)}}", font_size=30),
        ]
        rows[3][2].set_color(POST)
        whys = [why(r"a fair coin, \ or one whose bias could be anything"), why(r"Part 10: \ ``nearly significant''"),
                why(r"the data barely favour either"), why(r"the fair coin is still as likely as not")]
        with self.voiceover(
            "<bookmark mark='a'/> Is a coin fair? H zero says p is exactly a half; H one says it could be anything, uniformly. "
            "<bookmark mark='b'/> Toss it a hundred times and get sixty heads. Part 10's two-sided p-value is point zero five "
            "seven: nearly significant. <bookmark mark='c'/> The Bayes factor is the beta function's average of the likelihood "
            "under H one, over the likelihood under H zero: point nine one. The data barely move the odds, and in fact very "
            "slightly favour the fair coin. <bookmark mark='d'/> Starting from even odds, the fair coin keeps a posterior "
            "probability of point five two. A nearly significant p-value and a nearly neutral Bayes factor, from the same "
            "tosses."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lindley(self):
        d = load("bf")
        tab = table_rows([[r"tosses $n$", r"heads", r"$p$-value", r"BF$_{10}$", r"$P(H_0 \mid y)$"]] +
                         [[rf"{r['n']:,}", rf"{r['s']:,}", rf"{r['p']:.3f}", rf"{r['bf10']:.3f}", rf"{1 / (1 + r['bf10']):.2f}"] for r in d["rows"]],
                         font_size=28, col_buff=0.8, row_buff=0.3, colors=[GREY_B] + [None] * 4).move_to([0, 0.8, 0])
        for r in tab[1:]:
            r[4].set_color(POST)
            r[2].set_color(S.ALT)
        foot = fit_rows(VGroup(
            label(r"the same $p$-value, \ 0.05, \ at every sample size", font_size=24, color=S.ALT),
            label(r"the Bayes factor swings ever more strongly towards $H_0$", font_size=24, color=POST),
            label(r"Lindley (1957): \ with enough data, \ ``just significant'' is evidence for the null", font_size=24, color=OBS),
        ), 12.4, 0.28, [0, -2.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now hold the p-value fixed at about point oh five and let the number of tosses grow: a hundred, "
            "a thousand, ten thousand, a hundred thousand, with just enough heads each time to be on the edge of significance. "
            "<bookmark mark='b'/> The p-value stays at point oh five. The Bayes factor falls from point nine to point oh three, "
            "and the posterior probability of the fair coin climbs to ninety-seven percent. <bookmark mark='c'/> With a hundred "
            "thousand tosses, fifty point three percent heads is just significant, and a bias that small is better "
            "explained by a fair coin than by a coin whose bias could be anywhere. Dennis Lindley pointed this out in 1957; Part "
            "26 takes up what it means for testing."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in tab[1:]], lag_ratio=0.4), run_time=3.0)
            for k, m_ in enumerate("bc"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k]))
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def bound(self):
        p = 0.05
        b = -np.e * p * np.log(p)
        rows = [
            cmath(r"\text{BF}_{01}", r"\ge", r"-e\,p\log p\quad (p < 1/e)", font_size=34),
            cmath(r"p = 0.05", r":", rf"\text{{BF}}_{{01}} \ge {b:.2f}", font_size=34),
            cmath(r"P(H_0 \mid y)", r"\ge", rf"\frac{{{b:.2f}}}{{1 + {b:.2f}}} = {b / (1 + b):.2f}", font_size=34),
            cmath(r"\text{so}", r":", r"\text{a bound within the stated continuous }p\text{-model class}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"Sellke, \ Bayarri \& Berger (2001): \ null-uniform $p$; alternative mixtures of Beta$(a,1)$, $0<a\le1$"), why(r"the most $H_1$ can gain"),
                why(r"with even prior odds"), why(r"Part 10's warning, \ quantified")]
        intro = label('A continuous p-value calibration under stated alternatives', font_size=36)
        with self.voiceover(
            "Is that just the uniform prior's fault? <bookmark mark='a'/> Thomas Sellke, Maria Bayarri and James Berger showed in "
            "2001 that, for a continuous p-value uniform under the null, with alternative p-value densities that are mixtures of Beta a one for zero less than a at most one, the Bayes factor in favour of the null can't fall below "
            "minus e times p times the log of p. <bookmark mark='b'/> At p equals point oh five, that's point four one: the "
            "data can make the alternative at most two and a half times more likely relative to the null. "
            "<bookmark mark='c'/> Starting from even odds, the null keeps a posterior probability of at least twenty-nine percent. "
            "<bookmark mark='d'/> A p-value of point oh five is much weaker evidence than it sounds, within that model class. This is not a universal bound over all alternatives or a direct exact calibration for discrete binomial p-values. That's the quantitative version of Part 10's warnings."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def scale(self):
        tab = table_rows([[r"BF$_{10}$", r"Jeffreys's description"],
                          [r"1 to 3", r"barely worth mentioning"], [r"3 to 10", r"substantial"], [r"10 to 30", r"strong"],
                          [r"30 to 100", r"very strong"], [r"above 100", r"decisive"]],
                         font_size=28, col_buff=1.2, row_buff=0.28, colors=[GREY_B, None, None, None, None, None]).move_to([-2.4, 0.4, 0])
        rows = fit_rows(VGroup(
            label(r"Bayes factors depend on $H_1$'s prior, \ even with lots of data", font_size=22, color=RES),
            label(r"vague priors penalize $H_1$ for predicting everything", font_size=22),
            label(r"an automatic Occam's razor", font_size=24, color=OBS),
            label(r"Part 26: \ choosing priors for testing; \ Part 28: \ model choice", font_size=22, color=GREY_A),
        ), 4.8, 0.38, [4.3, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Jeffreys offered a scale for reading Bayes factors: up to three, barely worth mentioning; three "
            "to ten, substantial; then strong, very strong, and above a hundred, decisive. <bookmark mark='b'/> Two cautions. "
            "Unlike posteriors for parameters, Bayes factors stay sensitive to the alternative's prior however much data there "
            "are: <bookmark mark='c'/> a very vague prior spreads H one's predictions over everything, and so penalizes it. "
            "<bookmark mark='d'/> That's an automatic Occam's razor, simpler hypotheses win unless the data demand more, but it "
            "means the prior must be chosen with care. Part 26 returns to priors for testing, and Part 28 to choosing between "
            "models."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab, lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.clear_scene()

    def births_bf(self):
        rows = [
            cmath(r"H_0: p = \tfrac12", r",", r"H_1: p \sim U(0, 1)", font_size=32),
            cmath(r"\text{Paris births}", r":", r"251{,}527 \text{ boys of } 493{,}472", font_size=30),
            cmath(r"\log_{10}\text{BF}_{10}", r"\approx", r"38", font_size=34),
            cmath(r"\text{so}", r":", r"\text{overwhelming for ordinary prior odds, \ within this binomial model}", font_size=30),
        ]
        rows[2][2].set_color(POST)
        whys = [why(r"boys and girls equally likely, \ or not"), why(r"the hook's data"), why(r"far beyond Jeffreys's ``decisive'' 100"),
                why(r"when the data are overwhelming, \ every method agrees")]
        intro = label('Compare the two models using the birth counts', font_size=36)
        with self.voiceover(
            "The other extreme. <bookmark mark='a'/> Test Laplace's question as a pair of hypotheses: boys and girls exactly "
            "equally likely, or a chance of a boy that could be anything. <bookmark mark='b'/> With the Paris births, "
            "<bookmark mark='c'/> the Bayes factor is about ten to the thirty-eight. <bookmark mark='d'/> It overwhelms ordinary prior odds within this IID binomial model; arbitrary prior odds or a different sampling model can change the conclusion. When the data are overwhelming, the p-value, the posterior and the Bayes factor all say "
            "the same thing; it's in the borderline cases, like sixty heads in a hundred, that they part company, and that's "
            "where the care is needed."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()
