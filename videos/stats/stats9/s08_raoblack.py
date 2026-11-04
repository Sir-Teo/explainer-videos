from __future__ import annotations

import numpy as np

from videos.stats.stats9.common import *  # noqa: F403


class RaoBlackwell(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.theorem()
        self.proof()
        self.poisson()
        self.poisson_hist()
        self.tank_algebra()
        self.tank_collapse()
        self.legacy()

    def card(self):
        card = chapter_card(7, r"Rao--Blackwell", r"Conditioning on a sufficient statistic never hurts", part=PART)
        with self.voiceover("Chapter seven. The Rao–Blackwell theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        h1 = history_card(1945, r"C. R. Rao, \ aged 24, \ Calcutta", r"``Information and the accuracy attainable in the estimation of "
                          r"statistical parameters'': \ in one paper, \ the improvement theorem and the variance bound of ch.~10",
                          color=UMVUE, width=6.0, font_size=22).move_to([-3.3, 0.6, 0])
        h2 = history_card(1947, r"David Blackwell, \ Howard University", r"``Conditional expectation and unbiased sequential "
                          r"estimation'': \ the same theorem, \ found independently, \ and extended to sequential sampling",
                          color=UMVUE, width=6.0, font_size=22).move_to([3.3, 0.6, 0])
        foot = label(r"the move is now called ``Rao--Blackwellization''", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "<bookmark mark='a'/> In 1945 Calyampudi Radhakrishna Rao, twenty-four years old and working at the Indian "
            "Statistical Institute in Calcutta, published a paper in the Bulletin of the Calcutta Mathematical Society "
            "that contains two of the central results of estimation theory: the one in this chapter, and the variance "
            "bound of chapter ten. <bookmark mark='b'/> Two years later, David Blackwell at Howard University found the "
            "first result independently, and extended it to sequential sampling. Blackwell was the first Black "
            "scholar elected to the National Academy of Sciences, and Rao lived to be a hundred and two, receiving the "
            "International Prize in Statistics in 2023. <bookmark mark='c'/> The process their theorem describes is now "
            "called Rao–Blackwellization."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(h1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(h2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def theorem(self):
        tc = theorem_card(r"Rao--Blackwell", r"Let $\hat\theta$ be any estimator with $E\hat\theta^2 < \infty$ \ and $T$ a sufficient "
                          r"statistic. \ Then $\tilde\theta = E(\hat\theta \mid T)$ \ (i) is an estimator, \ (ii) has the same mean as "
                          r"$\hat\theta$, \ and (iii) has \ $\mathrm{MSE}(\tilde\theta) \le \mathrm{MSE}(\hat\theta)$ for every $\theta$, \ "
                          r"with equality only if $\hat\theta$ is already a function of $T$.", who=r"Rao (1945); \ Blackwell (1947)",
                          color=UMVUE, width=10.8, font_size=26).move_to([0, 1.0, 0])
        foot = fit_rows(VGroup(
            label(r"(i) needs sufficiency: \ the conditional law of the data given $T$ is free of $\theta$, \ so the average can be computed",
                  font_size=24, color=S.ACCENT),
            label(r"take any crude estimator, \ average away everything but $T$: \ it can only get better", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the theorem. Take any estimator at all, however crude, and a sufficient "
            "statistic T. Replace the estimator by its conditional expectation given T. Three things are true. The "
            "result is a genuine estimator: you can compute it without knowing theta. It has the same mean as the "
            "original, so if the original was unbiased, so is the new one. And its mean squared error is never larger, "
            "for any value of theta, and strictly smaller unless the original was already a function of T. "
            "<bookmark mark='b'/> The first point is exactly where sufficiency is needed. To average over the data "
            "given T, you need the conditional distribution of the data given T, and sufficiency says that "
            "distribution doesn't involve theta. <bookmark mark='c'/> So the recipe is: take any estimator, and "
            "average away everything except the sufficient statistic."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"E\tilde\theta", r"=", r"E\big[E(\hat\theta \mid T)\big] = E\hat\theta", font_size=34),
            cmath(r"\mathrm{Var}\,\hat\theta", r"=", r"E\big[\mathrm{Var}(\hat\theta \mid T)\big] + \mathrm{Var}\big[E(\hat\theta \mid T)\big]",
                  font_size=34),
            cmath(r"\vphantom{x}", r"=", r"E\big[\mathrm{Var}(\hat\theta \mid T)\big] + \mathrm{Var}\,\tilde\theta", font_size=34),
            cmath(r"\mathrm{Var}\,\tilde\theta", r"\le", r"\mathrm{Var}\,\hat\theta", font_size=36),
            cmath(r"E\,L(\theta, \tilde\theta)", r"\le", r"E\,L(\theta, \hat\theta)\quad\text{for any convex loss } L", font_size=32),
        ]
        rows[3][2].set_color(UMVUE)
        rows[4][2].set_color(GREY_A)
        whys = [why(r"the tower property (Part 5)"), why(r"Eve's law (Part 5): \ within plus between"), why(r"the second term is $\tilde\theta$'s variance"),
                why(r"the first term is $\ge 0$; \ equal means, \ so MSE too"), why(r"Jensen, \ conditionally: \ $L(\theta, E[\hat\theta \mid T]) \le E[L(\theta,\hat\theta) \mid T]$")]
        with self.voiceover(
            "The proof uses nothing but Part 5. <bookmark mark='a'/> The mean is unchanged, by the tower property: the "
            "average of conditional averages is the overall average. <bookmark mark='b'/> For the variance, use Eve's "
            "law: the total variance is the average variance within each value of T, plus the variance between the "
            "conditional means. <bookmark mark='c'/> But the conditional means are the new estimator, so the second term "
            "is its variance. <bookmark mark='d'/> The first term can't be negative. So the new variance is no bigger, "
            "and since the means agree, neither is the mean squared error. What's thrown away is exactly the "
            "within-T wobble, which is noise. <bookmark mark='e'/> And the same argument, using Jensen's inequality "
            "conditionally, works for any convex loss, not just squared error."
        ) as vo:
            step = ladder(self, rows, whys, keep=5, top=2.9, x=-0.6, buff=0.55, edge=6.9)
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def poisson(self):
        d = load("raoblack")
        rows = [
            cmath(r"\theta = P(X = 0)", r"=", r"e^{-\lambda}", r"\quad\text{a quiet corps-year}", font_size=34),
            cmath(r"\hat\theta", r"=", r"\mathbf 1\{X_1 = 0\}", r"\quad\text{unbiased, \ and absurd}", font_size=34),
            cmath(r"X_1 \mid S = s", r"\sim", r"\mathrm{Binomial}\big(s, \tfrac1n\big)", r"\quad S = \textstyle\sum X_i", font_size=34),
            cmath(r"\tilde\theta = E(\hat\theta \mid S)", r"=", r"P(X_1 = 0 \mid S) = \Big(1 - \frac1n\Big)^{S}", font_size=34),
        ]
        rows[3][2].set_color(UMVUE)
        whys = [why(r"a function of $\lambda$ we want"), why(r"uses one observation, \ and only says 0 or 1"),
                why(r"given the total, \ each event falls in corps-year 1 with chance $1/n$"),
                why(r"Rao--Blackwellized: \ uses every observation, \ still unbiased")]
        with self.voiceover(
            "Let's watch it work. <bookmark mark='a'/> Suppose we want the probability of a quiet year, one with no "
            "deaths: e to the minus lambda, for Poisson counts. <bookmark mark='b'/> Here's a terrible estimator: look "
            "at the first observation only, and say one if it's zero and zero otherwise. It's unbiased, since its "
            "average is exactly the probability we want. But it ignores nine tenths of the data and can only say zero "
            "or one. <bookmark mark='c'/> Now condition on the total, which is sufficient. Given the total, each event "
            "is equally likely to have happened in any of the n years, so the first year's count is binomial, with s "
            "trials and probability one over n. <bookmark mark='d'/> The chance it's zero is one minus one over n, to "
            "the power S. That's the improved estimator. It uses all the data, through their total, and it's still "
            "exactly unbiased."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.6, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def poisson_hist(self):
        d = load("raoblack")
        g = np.random.Generator(np.random.PCG64(1945))
        lam, n = 0.7, 10
        x = g.poisson(lam, (20000, n))
        naive = (x[:, 0] == 0).astype(float)
        rb = ((n - 1) / n) ** x.sum(1)
        ed = np.linspace(0, 1.0, 41)
        A = axes([0, 1.05], [0, 1.0], x_length=7.4, y_length=4.2, xlabel=r"estimate of $e^{-\lambda}$", ylabel=r"share of samples",
                 xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.5, 1.0], center=[-2.0, -0.3, 0])
        ax = A.ax
        w = (ax.c2p(0.025, 0)[0] - ax.c2p(0, 0)[0])
        nb = VGroup(*[Rectangle(width=w, height=ax.c2p(0, np.mean(naive == v))[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=MOM,
                                fill_opacity=0.7).move_to(ax.c2p(v if v == 0 else 1.0 - 0.0125, 0), aligned_edge=DOWN)
                    for v in (0.0, 1.0)])
        nb[0].move_to(ax.c2p(0.0125, 0), aligned_edge=DOWN)
        h, _ = np.histogram(rb, ed)
        rbb = hist_bars(ax, ed, h / len(rb), color=UMVUE, opacity=0.8)
        tr = DashedLine(ax.c2p(d["truth"], 0), ax.c2p(d["truth"], 1.0), color=EXACT, stroke_width=2.5)
        rows = fit_rows(VGroup(
            MathTex(rf"e^{{-0.7}} = {d['truth']:.4f}", font_size=28, color=EXACT),
            MathTex(rf"\mathbf 1\{{X_1 = 0\}}:\ \text{{mean }} {d['naive_mean']:.3f},\ \text{{SD }} {d['naive_sd']:.3f}", font_size=26, color=MOM),
            MathTex(rf"(1 - \tfrac1n)^S:\ \text{{mean }} {d['rb_mean']:.3f},\ \text{{SD }} {d['rb_sd']:.3f}", font_size=26, color=UMVUE),
            label(rf"the variance falls by a factor of {(d['naive_sd'] / d['rb_sd']) ** 2:.0f}", font_size=26, color=S.ACCENT),
        ), 5.0, 0.34, [4.4, -0.2, 0])
        tag = simulated_tag(r"simulated: \ 20,000 samples, \ $n = 10$, \ $\lambda = 0.7$", corner=DR)
        with self.voiceover(
            "Twenty thousand samples of ten Poisson counts, with lambda point seven, so the target is point four nine "
            "seven. <bookmark mark='a'/> The crude estimator is a coin flip: zero about half the time, one the other "
            "half. On average it's right, but every single estimate is off by a half. Its standard deviation is point "
            "five. <bookmark mark='b'/> The Rao–Blackwellized estimator spreads over a range of values centred on the "
            "truth, and its standard deviation is point one three. <bookmark mark='c'/> Same mean, and fourteen times "
            "less variance, from one line of conditioning. And there's more: chapter eight will show that no unbiased "
            "estimator of this quantity does better."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag), Create(tr), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(nb), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rbb, lag_ratio=0.03), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def tank_algebra(self):
        rows = [
            cmath(r"\hat N", r"=", r"2\bar X - 1", r"\quad\text{unbiased, \ not a function of } m", font_size=34),
            cmath(r"E\big(\bar X \mid m\big)", r"=", r"\frac1k\Big(m + (k - 1)\cdot\frac{m}{2}\Big)", font_size=34),
            cmath(r"\vphantom{x}", r"=", r"\frac{m(k + 1)}{2k}", font_size=34),
            cmath(r"E\big(2\bar X - 1 \mid m\big)", r"=", r"m\Big(1 + \frac1k\Big) - 1", font_size=36),
        ]
        rows[3][2].set_color(UMVUE)
        whys = [why(r"chapter 2's moment estimator"), why(r"the max, \ plus $k - 1$ uniform draws from $1, \dots, m - 1$, \ mean $m/2$"),
                why(r"simplify"), why(r"Rao--Blackwell turns the moment estimator into the scaled maximum")]
        with self.voiceover(
            "Now the tanks. <bookmark mark='a'/> Start with the moment estimator, two x-bar minus one. It's unbiased, "
            "but it isn't a function of the sufficient statistic, the maximum m. So condition on m. "
            "<bookmark mark='b'/> Given m, one serial is m itself, and the other k minus one are a random sample from "
            "one to m minus one, each with average m over two. <bookmark mark='c'/> So the conditional mean of x-bar "
            "is m times k plus one over two k. <bookmark mark='d'/> Double it and subtract one: m times one plus one "
            "over k, minus one. Rao–Blackwell has turned the moment estimator into exactly the scaled maximum, the "
            "estimator that won chapter one. It wasn't a lucky guess. It's what you get by stripping the noise out of "
            "the average."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.6, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tank_collapse(self):
        d = load("raoblack")
        g = np.random.Generator(np.random.PCG64(47))
        N, k, R = 300, 6, 700
        s = np.array([g.choice(N, k, replace=False) + 1 for _ in range(R)])
        m = s.max(1)
        mom = 2 * s.mean(1) - 1
        A = axes([100, 300], [50, 550], x_length=6.6, y_length=5.0, xlabel=r"largest serial $m$", ylabel=r"estimate of $N$",
                 xticks=[100, 150, 200, 250, 300], yticks=[100, 200, 300, 400, 500], center=[-2.9, -0.2, 0])
        ax = A.ax
        keep = (m >= 100) & (mom >= 50) & (mom <= 550)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=MOM, fill_opacity=0.7) for a, b in zip(m[keep], mom[keep])])
        targets = [ax.c2p(a, a * (1 + 1 / k) - 1) for a in m[keep]]
        line = Line(ax.c2p(100, 100 * (1 + 1 / k) - 1), ax.c2p(300, 300 * (1 + 1 / k) - 1), color=UMVUE, stroke_width=3)
        truth = DashedLine(ax.c2p(100, 300), ax.c2p(300, 300), color=EXACT, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"each dot: \ one factory; \ $(m,\ 2\bar x - 1)$", font_size=24, color=MOM),
            label(r"the vertical scatter at fixed $m$ is noise", font_size=24, color=GREY_A),
            label(r"average it away: \ every dot drops onto $m(1 + \tfrac1k) - 1$", font_size=24, color=UMVUE),
            MathTex(rf"\mathrm{{SD}}:\ {d['tank_mom_sd']:.1f}\ \to\ {d['tank_umvue_sd']:.1f}", font_size=32, color=S.ACCENT),
        ), 4.6, 0.36, [4.3, -0.2, 0])
        tag = simulated_tag(r"simulated: \ 700 factories, \ $N = 300$, \ $k = 6$", corner=DR)
        with self.voiceover(
            "Here it is as a picture. <bookmark mark='a'/> Seven hundred factories, each with three hundred tanks, six "
            "captured. Each dot is one factory: across, the largest serial captured, and up, the moment estimate. "
            "<bookmark mark='b'/> For a given maximum, the moment estimate still wobbles up and down, depending on "
            "where the other five serials happened to fall. That wobble is pure noise: it has the same distribution "
            "whatever N is. <bookmark mark='c'/> Rao–Blackwell averages it away. Watch every dot drop onto its "
            "conditional mean, the line m times one plus one over k, minus one. <bookmark mark='d'/> The spread of "
            "estimates around the truth falls from seventy to forty-two, and the estimator is still unbiased."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag), Create(truth))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.002), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(rows[2]))
            self.play(*[dt.animate.move_to(t).set_color(UMVUE) for dt, t in zip(dots, targets)], run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def legacy(self):
        rows = fit_rows(VGroup(
            label(r"Rao--Blackwellization, \ everywhere:", font_size=30, color=S.ACCENT),
            label(r"Monte Carlo: \ average a conditional expectation instead of raw draws \ (Gelfand \& Smith, 1990; \ Part 27)",
                  font_size=24),
            label(r"particle filters: \ integrate out the linear part exactly \ (Part 38)", font_size=24),
            label(r"survey sampling: \ weight by what you know about who was sampled \ (Part 18)", font_size=24),
            label(r"the lesson: \ any randomness that does not depend on $\theta$ \ can only add variance", font_size=26,
                  color=S.ACCENT),
        ), 12.6, 0.44, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The idea reaches far beyond estimators. <bookmark mark='b'/> In Monte Carlo, if you "
            "can compute a conditional expectation exactly, average that instead of the raw draws: Alan Gelfand and "
            "Adrian Smith made this standard in Bayesian computation in 1990, and Part 27 uses it. "
            "<bookmark mark='c'/> Particle filters integrate out whatever part of the model can be done exactly. "
            "<bookmark mark='d'/> Survey statisticians condition on what they know about the design. "
            "<bookmark mark='e'/> The lesson in each case is the same: randomness that carries no information about "
            "the parameter can only add variance, and it should be averaged out."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
