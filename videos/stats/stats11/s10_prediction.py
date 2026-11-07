from __future__ import annotations

import numpy as np

from videos.stats.stats11.common import *  # noqa: F403


class Prediction(VoiceoverScene):
    def construct(self):
        self.card()
        self.confusion()
        self.formula()
        self.skewed()
        self.log_scale()
        self.wilks()
        self.tolerance()

    def card(self):
        card = chapter_card(9, r"Prediction and tolerance", r"Where will the next observation fall?", part=PART)
        with self.voiceover("Chapter nine. Prediction and tolerance intervals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def confusion(self):
        d = load("prediction")
        bars = VGroup()
        for i, (t, v, c) in enumerate(((r"the 95\% CI for the mean", d["ci"], MISS), (r"the 95\% prediction interval", d["pi"], HIT))):
            y = 0.9 - 1.4 * i
            bars.add(VGroup(label(t, font_size=26, color=c).move_to([-3.8, y, 0]),
                            Rectangle(width=6.0 * v + 0.01, height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.8).move_to([-0.2, y, 0], aligned_edge=LEFT),
                            MathTex(rf"{100 * v:.1f}\%", font_size=32, color=c).move_to([6.4, y, 0])))
        head = label(r"how often does the interval from 10 men contain the \emph{next} man's height?", font_size=26).to_edge(UP, buff=0.8)
        foot = label(r"a confidence interval is for the mean, \ not for individuals: \ the normal prediction width is $\sqrt{n+1}$ times the mean-CI width", font_size=26,
                     color=OBS).to_edge(DOWN, buff=0.9)
        tag = simulated_tag(r"simulated: \ the World, \ 20,000 samples", corner=DR)
        with self.voiceover(
            "A common confusion. You've measured ten men and computed the ninety-five percent interval for the mean "
            "height. Will the next man you meet be inside it? <bookmark mark='a'/> Only half the time: forty-nine point "
            "eight percent. <bookmark mark='b'/> A prediction interval, built for the next observation, contains him "
            "ninety-five point one percent of the time. <bookmark mark='c'/> The confidence interval describes "
            "uncertainty about the average; an individual varies around the average by a whole standard deviation, not a "
            "standard error."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                self.play(FadeIn(bars[k][0]), GrowFromEdge(bars[k][1], LEFT), FadeIn(bars[k][2]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def formula(self):
        rows = [
            cmath(r"X_{n+1} - \bar X", r"\sim", r"N\Big(0,\ \sigma^2\big(1 + \tfrac1n\big)\Big)", font_size=34),
            cmath(r"\frac{X_{n+1} - \bar X}{s\sqrt{1 + 1/n}}", r"\sim", r"t_{n-1}", font_size=34),
            cmath(r"\bar x", r"\pm", r"t_{n-1,\,0.975}\ s\sqrt{1 + \tfrac1n}", font_size=36),
        ]
        rows[2][2].set_color(HIT)
        whys = [why(r"the new draw's own variance, \ plus the mean's"), why(r"a pivot, \ for normal data"),
                why(r"as $n \to \infty$: \ $\mu \pm 1.96\sigma$, \ not a point")]
        with self.voiceover(
            "<bookmark mark='a'/> The new observation differs from the sample mean by its own deviation, variance sigma "
            "squared, plus the mean's error, variance sigma squared over n. <bookmark mark='b'/> Studentized, that's again "
            "a t pivot for independent normal observations. <bookmark mark='c'/> So the prediction interval is x-bar plus or minus t times s times root one "
            "plus one over n. As n grows it doesn't shrink to a point, as a confidence interval does: it settles at the "
            "mean plus or minus one point nine six standard deviations, the central ninety-five percent range of a normal population."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.4, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def skewed(self):
        d = load("prediction")
        rows = fit_rows(VGroup(
            label(r"but the pivot needs normal data", font_size=28),
            MathTex(rf"\text{{the World's incomes, }} n = 19:\ \ \text{{normal prediction interval covers }} {100 * d['pi_inc']:.1f}\%", font_size=30,
                    color=MISS),
            label(r"averaging rescues confidence intervals for means (Part 6's CLT); \ nothing rescues a prediction for one person", font_size=24),
            label(r"a prediction interval depends on the shape of the population, \ not just its mean and SD", font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> There's a catch. The prediction pivot needs normal data, and here the central limit "
            "theorem can't help. <bookmark mark='b'/> On the World's skewed incomes, with nineteen observations, the "
            "normal prediction interval covers the next income only ninety-three point seven percent of the time. "
            "<bookmark mark='c'/> A confidence interval for a mean is "
            "rescued by averaging; a prediction for one person has nothing to average. <bookmark mark='d'/> Predicting an "
            "individual requires knowing the shape of the population. Or does it?"
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def wilks(self):
        d = load("prediction")
        g = np.random.Generator(np.random.PCG64(5))
        vals = np.sort(g.random(19))
        nl = NumberLine(x_range=[0, 1, 0.1], length=11.0, include_numbers=False, color=GREY_C).move_to([0, 1.6, 0])
        dots = VGroup(*[Dot(nl.n2p(v), radius=0.08, color=DATA) for v in vals])
        gaps = VGroup(*[Line(nl.n2p(a), nl.n2p(b), color=c, stroke_width=8, stroke_opacity=0.6)
                        for (a, b), c in zip(zip(np.r_[0, vals], np.r_[vals, 1]), [S.PRIOR, S.POST] * 10)])
        rows = [
            cmath(r"P\big(X_{(1)} < X_{n+1} < X_{(n)}\big)", r"=", r"\frac{n - 1}{n + 1}", font_size=34),
            cmath(r"n = 19", r":", rf"\frac{{18}}{{20}} = 0.90\qquad\text{{incomes, simulated: }} {100 * d['order_inc']:.1f}\%", font_size=32),
        ]
        rows[1][2].set_color(HIT)
        whys = [why(r"$n + 1$ exchangeable draws: \ the new one is equally likely to be any rank"),
                why(r"any continuous distribution whatsoever")]
        intro = label('Exchangeability gives an unconditional prediction guarantee', font_size=36)
        with self.voiceover(
            "It doesn't, and the argument is one of the prettiest in statistics, due to Samuel Wilks in 1941. "
            "<bookmark mark='a'/> Nineteen observations cut the line into twenty gaps. <bookmark mark='b'/> Add a new "
            "observation from the same distribution. Among the twenty draws, the new one is equally likely to have any "
            "rank, so before observing the spacings, its rank is uniform over those twenty gaps. Conditional on the observed data, gap probabilities generally differ. <bookmark mark='c'/> It falls between the "
            "smallest and the largest of the first nineteen unless it lands in one of the two end gaps: probability "
            "eighteen in twenty, ninety percent, for every continuous distribution. <bookmark mark='d'/> On the World's "
            "incomes, simulated: eighty-nine point six. This symmetry argument, exchangeability of the new point with the "
            "old ones, is the seed of conformal prediction, Part 34."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(Create(nl), LaggedStart(*[FadeIn(dt, scale=1.5) for dt in dots], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(FadeIn(gaps))
            step = ladder(self, rows, whys, keep=2, top=0.2, x=-0.4, buff=0.9, edge=6.9)
            vo.wait_until("c")
            step(0, transform=False)
            vo.wait_until("d")
            step(1, transform=False)
        self.clear_scene()

    def tolerance(self):
        dc = definition_card(r"Tolerance interval", r"$[L(X), U(X)]$ is a $(P, \gamma)$ tolerance interval if, \ with probability at least $\gamma$ over "
                             r"the sample, \ it contains at least a proportion $P$ of the population.", color=OBS, width=9.6,
                             font_size=26).move_to([0, 1.4, 0])
        rows = fit_rows(VGroup(
            label(r"manufacturing: \ ``95\% confident that 99\% of the bolts are within these limits''", font_size=24),
            label(r"three different promises: \ about a parameter (CI), \ one future draw (PI), \ most of the population (TI)", font_size=24,
                  color=OBS),
            label(r"Wilks (1941) gives distribution-free tolerance limits from order statistics too", font_size=24, color=GREY_A),
        ), 12.6, 0.34, [0, -1.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A third kind of interval makes a third kind of promise. A tolerance interval is one that, "
            "with confidence gamma, contains at least a proportion P of the whole population. <bookmark mark='b'/> It's "
            "the engineer's interval: ninety-five percent confident that ninety-nine percent of the bolts are within "
            "these limits. <bookmark mark='c'/> So there are three distinct promises: about a parameter, a confidence "
            "interval; about one future observation, a prediction interval; about most of the population, a tolerance "
            "interval. Confusing them is among the most common errors in applied work. <bookmark mark='d'/> Wilks' order "
            "statistics give distribution-free tolerance limits as well."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def log_scale(self):
        from explainer.stats.kit import intervals as I
        from explainer.stats.world import World

        inc = World().income
        inc = inc[World().adult]
        g = np.random.Generator(np.random.PCG64(1942))
        R = 10000
        raw = logs = 0
        for _ in range(R):
            s = inc[g.integers(0, len(inc), 20)]
            lo, hi = I.prediction_interval(s[:19])
            raw += lo <= s[19] <= hi
            lo, hi = I.prediction_interval(np.log(s[:19]))
            logs += lo <= np.log(s[19]) <= hi
        rows = fit_rows(VGroup(
            label(r"incomes are roughly log-normal: \ predict on the log scale, \ then exponentiate", font_size=26),
            MathTex(rf"\text{{raw scale: }} {100 * raw / R:.1f}\%\qquad \text{{log scale: }} {100 * logs / R:.1f}\%", font_size=32, color=OBS),
            label(r"a prediction interval transforms exactly: \ $P(a < \log Y < b) = P(e^a < Y < e^b)$", font_size=24, color=GREY_A),
            label(r"and the back-transformed interval is lopsided, \ as the incomes are", font_size=24, color=GREY_A),
        ), 12.6, 0.4, [0, 0.0, 0])
        tag = simulated_tag(r"simulated: \ the World, \ 10,000 samples of 19", corner=DR)
        intro = label('Predict incomes on the log scale', font_size=36)
        with self.voiceover(
            "Sometimes the shape problem has a simple cure. <bookmark mark='a'/> The World's incomes are roughly "
            "log-normal, so take logs, build the normal prediction interval there, and exponentiate the ends. "
            "<bookmark mark='b'/> On the raw scale, about ninety-four percent; on the log scale, ninety-five point one, "
            "right back at the promise. <bookmark mark='c'/> Unlike a confidence interval for a mean, a prediction interval transforms "
            "exactly: the new income is between e to the a and e to the b exactly when its log is between a and b. "
            "<bookmark mark='d'/> And the back-transformed interval is lopsided, long on the high side, just like incomes."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tag))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
