from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats15.common import *  # noqa: F403

XS = np.linspace(0, 1, 301)


class Machinery(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.three_panels()
        self.sequential()
        self.batch()
        self.history()
        self.meaning()

    def card(self):
        card = chapter_card(1, r"The machinery", r"Prior $\times$ likelihood $\propto$ posterior", lit=(1763, 1774), part=PART)
        with self.voiceover("Chapter one. The machinery."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def rule(self):
        rows = [
            cmath(r"\pi(\theta \mid y)", r"=", r"\frac{p(y \mid \theta)\,\pi(\theta)}{p(y)}", font_size=36),
            cmath(r"p(y)", r"=", r"\int p(y \mid \theta)\,\pi(\theta)\,d\theta", font_size=34),
            cmath(r"\pi(\theta \mid y)", r"\propto", r"p(y \mid \theta) \times \pi(\theta)", font_size=36),
            cmath(r"\text{posterior}", r"\propto", r"\text{likelihood} \times \text{prior}", font_size=34),
        ]
        rows[2][2].set_color(POST)
        whys = [why(r"Part 2's Bayes rule, \ with $\theta$ as the unknown"), why(r"a constant: \ it does not involve $\theta$"),
                why(r"so we can ignore it, \ and normalize at the end"), why(r"Part 9's likelihood, \ weighted by belief")]
        with self.voiceover(
            "<bookmark mark='a'/> The rule is Part 2's Bayes's rule, with the unknown parameter theta playing the role of the "
            "hypothesis: the posterior density of theta given the data equals the likelihood times the prior, divided by the "
            "probability of the data. <bookmark mark='b'/> That denominator averages the likelihood over the prior. It doesn't "
            "depend on theta at all. <bookmark mark='c'/> So the posterior is proportional to likelihood times prior, and we "
            "can normalize at the end, by making the area one. <bookmark mark='d'/> In words: the posterior is Part 9's "
            "likelihood, weighted by what you believed before. Fisher's likelihood said which parameter values make the data "
            "probable. Bayes turns that into a probability distribution for the parameter, at the price of a prior."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def panel(self, center, ys, color, title, ymax=3.5):
        A = axes([0, 1], [0, ymax], x_length=3.6, y_length=2.6, xlabel=r"$p$", ylabel=r"", xticks=[0, 0.5, 1], yticks=[], center=center)
        t = label(title, font_size=24, color=color).next_to(A, UP, buff=0.1)
        return VGroup(A, t), density(A.ax, XS, ys, color)

    def three_panels(self):
        pr = stats.beta(2, 2).pdf(XS)
        lik = XS ** 7 * (1 - XS) ** 3
        lik = lik / np.trapezoid(lik, XS)
        po = stats.beta(9, 5).pdf(XS)
        f1, c1 = self.panel([-4.6, 0.4, 0], pr, PRIOR, r"prior: \ Beta(2, 2)")
        f2, c2 = self.panel([0, 0.4, 0], lik, LIKE, r"likelihood: \ 7 of 10")
        f3, c3 = self.panel([4.6, 0.4, 0], po, POST, r"posterior: \ Beta(9, 5)")
        times = MathTex(r"\times", font_size=48).move_to([-2.3, 0.4, 0])
        prop = MathTex(r"\propto", font_size=48).move_to([2.3, 0.4, 0])
        rows = fit_rows(VGroup(
            label(r"a mild prior belief that $p$ is near one half", font_size=24, color=PRIOR),
            label(r"the data: \ 7 successes in 10", font_size=24, color=LIKE),
            label(r"multiply pointwise, \ rescale: \ the posterior sits between them, \ nearer the data", font_size=24, color=POST),
            MathTex(r"p^{1}(1 - p)^{1} \times p^{7}(1 - p)^{3} = p^{8}(1 - p)^{4}", font_size=30),
        ), 12.4, 0.28, [0, -2.4, 0])
        intro = label('Multiply the prior and likelihood point by point', font_size=36)
        with self.voiceover(
            "Here's the machinery at work. <bookmark mark='a'/> A prior: Beta two two, a mild belief that a probability p is "
            "somewhere near a half. <bookmark mark='b'/> The likelihood of seven successes in ten trials, drawn as a curve in p, "
            "peaking at point seven. <bookmark mark='c'/> Multiply the two curves point by point, and rescale so the area is "
            "one. The posterior sits between them, nearer the data, which carry more information than this mild prior. "
            "<bookmark mark='d'/> In symbols, the powers just add: p to the one times p to the seven gives p to the eight, and "
            "the posterior is Beta nine five."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(f1), FadeIn(c1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(times), FadeIn(f2), FadeIn(c2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(prop), FadeIn(f3), TransformFromCopy(VGroup(c1, c2), c3), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def sequential(self):
        d = load("billiard")
        posts = d["post"]
        left = d["left"]
        A = axes([0, 1], [0, 3.6], x_length=7.4, y_length=4.2, xlabel=r"W's position $p$", ylabel=r"density", xticks=[0, 0.25, 0.5, 0.75, 1],
                 yticks=[0, 1, 2, 3], center=[-2.2, 0.2, 0])
        ax = A.ax
        cur = density(ax, XS, np.ones_like(XS), PRIOR)
        tally = label(r"ball 0: \ Beta(1, 1)", font_size=26, color=PRIOR).move_to([4.5, 1.6, 0])
        rows = fit_rows(VGroup(
            label(r"one ball at a time", font_size=24),
            label(r"left: \ multiply by $p$; \ right: \ by $1 - p$", font_size=24, color=LIKE),
            label(r"each posterior is the next prior", font_size=24, color=POST),
        ), 4.6, 0.36, [4.5, -0.6, 0])
        truth = DashedLine(ax.c2p(d["u0"], 0), ax.c2p(d["u0"], 3.4), color=S.TRUTH, stroke_width=2)
        with self.voiceover(
            "<bookmark mark='a'/> Back to the billiard table, one ball at a time. Start flat. <bookmark mark='b'/> Each ball "
            "that lands left multiplies the curve by p, pushing belief to the right; each ball that lands right multiplies it "
            "by one minus p, pushing it left. <bookmark mark='c'/> After each ball, today's posterior becomes tomorrow's prior. "
            "Watch the curve sharpen, ball by ball, around the hidden position."
        ) as vo:
            self.play(FadeIn(A), FadeIn(cur), FadeIn(tally))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            for k, (a, b) in enumerate(posts):
                new = density(ax, XS, stats.beta(a, b).pdf(XS), POST)
                nt = label(rf"ball {k + 1} \ ({'left' if left[k] else 'right'}): \ Beta({a}, {b})", font_size=26, color=POST).move_to(tally)
                self.play(Transform(cur, new), Transform(tally, nt), run_time=0.7)
            self.play(Create(truth))
        self.clear_scene()

    def batch(self):
        rows = [
            cmath(r"\pi(\theta \mid y_1)", r"\propto", r"p(y_1 \mid \theta)\,\pi(\theta)", font_size=34),
            cmath(r"\pi(\theta \mid y_1, y_2)", r"\propto", r"p(y_2 \mid \theta)\,\pi(\theta \mid y_1)", font_size=34),
            cmath(r"\pi(\theta \mid y_1, y_2)", r"\propto", r"p(y_1, y_2 \mid \theta)\,\pi(\theta)", font_size=34),
            cmath(r"\text{so}", r":", r"\text{the order and the batching do not matter}", font_size=32),
        ]
        rows[3][2].set_color(POST)
        whys = [why(r"update on the first data"), why(r"then on the second, \ with the first posterior as prior"),
                why(r"conditional independence here; otherwise use $p(y_2\mid y_1,\theta)$"), why(r"learning is coherent")]
        with self.voiceover(
            "<bookmark mark='a'/> Updating on the first piece of data gives a posterior. <bookmark mark='b'/> Use it as the "
            "prior for the second piece. <bookmark mark='c'/> The result is the same as updating on both at once, whenever the "
            "pieces are independent given theta, because their likelihoods multiply. With dependent data, use the conditional likelihood of the next piece given the earlier data; coherent sequential updating still works. <bookmark mark='d'/> So it doesn't "
            "matter whether you learn from data one observation at a time, in batches, or all together, or in what order: "
            "you end in the same place. That's one sense in which Bayesian learning is coherent."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def meaning(self):
        rows = fit_rows(VGroup(
            label(r"frequentist (Parts 8--14): \ $\theta$ is fixed; \ the data are random", font_size=26),
            label(r"a 95\% interval: \ the procedure catches $\theta$ in 95\% of repeated samples", font_size=24, color=S.ALT),
            label(r"Bayesian: \ $\theta$ is unknown, \ so it gets a probability distribution", font_size=26, color=POST),
            label(r"a 95\% credible interval: \ given these data, \ $P(\theta \in \text{interval}) = 0.95$", font_size=24, color=POST),
            label(r"the price: \ a prior; \ the reward: \ direct statements about $\theta$", font_size=24, color=OBS),
            label(r"de Finetti (Part 5): \ infinitely exchangeable Bernoulli data are a mixture of IID laws", font_size=22, color=GREY_A),
        ), 12.4, 0.4, [0, 0, 0])
        with self.voiceover(
            "What has changed? <bookmark mark='a'/> Since Part 8, the parameter has been a fixed number and the data random. "
            "<bookmark mark='b'/> A ninety-five percent confidence interval was a promise about a procedure, over repeated "
            "samples. <bookmark mark='c'/> In the Bayesian view, the parameter is unknown, so it gets a probability "
            "distribution that expresses what we know about it. <bookmark mark='d'/> A ninety-five percent credible interval "
            "then says, of these data, that theta lies inside with probability point nine five: the statement people usually "
            "think a confidence interval makes. <bookmark mark='e'/> The price is a prior; the reward is a direct answer. "
            "<bookmark mark='f'/> And de Finetti's theorem from Part 5 says the prior isn't arbitrary decoration: an infinitely extendible exchangeable Bernoulli sequence has an IID mixture representation. Finite exchangeability alone does not guarantee it."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def history(self):
        rows = fit_rows(VGroup(
            label(r"nineteenth century: \ ``inverse probability'', \ Laplace's method, \ used everywhere", font_size=24),
            label(r"Boole (1854), \ Venn (1866): \ where does the prior come from?", font_size=24, color=RES),
            label(r"Fisher (1922): \ likelihood instead; \ inverse probability ``must be wholly rejected''", font_size=24, color=S.ALT),
            label(r"Ramsey (1926), \ de Finetti (1937), \ Savage (1954): \ probability as coherent belief", font_size=24, color=POST),
            label(r"from about 1990: \ MCMC makes it computable \ (Gelfand \& Smith 1990)", font_size=24, color=OBS),
        ), 12.4, 0.44, [0, 0, 0])
        with self.voiceover(
            "A little history. <bookmark mark='a'/> Through the nineteenth century, Laplace's method, then called inverse "
            "probability, was simply how inference was done, in astronomy, geodesy and the social sciences. "
            "<bookmark mark='b'/> George Boole and John Venn attacked its weak point: where does the prior come from, and why "
            "should ignorance be uniform? <bookmark mark='c'/> Fisher, in 1922, built likelihood as an alternative and declared "
            "that the theory of inverse probability must be wholly rejected. <bookmark mark='d'/> Frank Ramsey, Bruno de "
            "Finetti and Leonard Savage rebuilt the foundations, with probability as the coherent degree of belief of a person "
            "who acts on it. <bookmark mark='e'/> And from about 1990, Markov chain Monte Carlo, popularized in applied Bayesian statistics by Alan Gelfand and Adrian Smith, made a wider range of models practical. Earlier MCMC methods and applications predate their paper. Part 26 picks up the modern story."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
