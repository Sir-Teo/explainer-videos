from __future__ import annotations

import itertools

import numpy as np

from explainer.stats.kit import survey as Sv
from videos.stats.stats18.common import *  # noqa: F403


class HorvitzThompson(VoiceoverScene):
    def construct(self):
        self.card()
        self.estimator()
        self.enumerate()
        self.variance()
        self.elephants()
        self.verdict()
        self.hajek()

    def card(self):
        card = chapter_card(7, r"Horvitz--Thompson", r"Weight each unit by one over its chance", part=PART)
        with self.voiceover("Chapter seven. Horvitz–Thompson."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def estimator(self):
        rows = [
            cmath(r"\pi_i", r"=", r"P(\text{unit } i \text{ is in the sample}),\ \ \text{any design}", font_size=30),
            cmath(r"\hat T_{\text{HT}}", r"=", r"\textstyle\sum_{i \in s} y_i / \pi_i", font_size=34),
            cmath(r"E[\hat T_{\text{HT}}]", r"=", r"\textstyle\sum_{i=1}^{N} \pi_i \cdot y_i/\pi_i = \sum_i y_i = T", font_size=30),
            cmath(r"1/\pi_i", r":", r"\text{each sampled unit stands for } 1/\pi_i \text{ units}", font_size=30),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"its inclusion probability, \ known from the design"), why(r"Horvitz \& Thompson (1952)"),
                why(r"unbiased whenever every $\pi_i > 0$"), why(r"the design weight")]
        intro = label('Inverse inclusion probabilities recover population totals', font_size=36)
        with self.voiceover(
            "Probability proportional to size is one design among many. Daniel Horvitz and Donovan Thompson, in 1952,"
            " gave an estimator for all of them. <bookmark mark='a'/> Let pi i be the probability that unit i is in "
            "the sample, whatever the design. <bookmark mark='b'/> Estimate the population total by adding, over the "
            "sampled units, each value divided by its inclusion probability. <bookmark mark='c'/> Taking expectations"
            " over the design, each unit appears with probability pi i and contributes y i over pi i, so the "
            "estimator is exactly unbiased, provided every unit has some chance. <bookmark mark='d'/> One over pi i "
            "is the design weight: a unit drawn with probability one in a hundred stands for a hundred units of the "
            "population."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def enumerate(self):
        y = np.array([3.0, 7.0, 1.0, 9.0, 4.0])
        x = np.array([1.0, 3.0, 1.0, 4.0, 2.0])
        pi = 0.9 * x / x.max()
        samples = []
        tot = 0.0
        for s in itertools.product([0, 1], repeat=5):
            s = np.array(s, bool)
            prob = float(np.prod(np.where(s, pi, 1 - pi)))
            est = Sv.horvitz_thompson(y[s], pi[s]) if s.any() else 0.0
            samples.append((s, prob, est))
            tot += prob * est
        tab = table_rows([
            [r"unit", r"1", r"2", r"3", r"4", r"5"],
            [r"$y_i$", *[f"{v:g}" for v in y]],
            [r"$\pi_i$", *[f"{v:.3f}" for v in pi]],
        ], font_size=28, colors=[GREY_B, None, OBS]).move_to([0, 2.0, 0])
        ex = sorted(samples, key=lambda t: -t[1])[:4]
        ex_rows = VGroup(*[MathTex(rf"\{{{', '.join(str(i + 1) for i in np.flatnonzero(s))}\}}:\ \ P = {p:.3f},\ \ \hat T = {e:.1f}",
                                   font_size=26) for s, p, e in ex]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-2.4, -0.6, 0])
        res = VGroup(MathTex(r"\textstyle\sum_s P(s)\,\hat T(s)", font_size=30), MathTex(rf"= {tot:.4f}", font_size=34, color=HIT),
                     MathTex(rf"T = {y.sum():g}", font_size=30)).arrange(DOWN, buff=0.25).move_to([4.0, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A check by brute force. Five units, with values three, seven, one, nine and four, "
            "each included independently with a probability proportional to a size measure. <bookmark mark='b'/> "
            "There are thirty-two possible samples. Here are the four most likely, with their probabilities and their"
            " Horvitz–Thompson estimates, which range widely. <bookmark mark='c'/> Average the estimate over all "
            "thirty-two samples, weighting each by its probability: exactly twenty-four, the true total. Unbiasedness"
            " here is not an approximation; it's algebra."       ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in ex_rows], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.clear_scene()

    def variance(self):
        rows = [
            cmath(r"\mathrm{Var}(\hat T_{\text{HT}})", r"=", r"\textstyle\sum_i \sum_j (\pi_{ij} - \pi_i \pi_j)\,\frac{y_i}{\pi_i}\frac{y_j}{\pi_j}",
                  font_size=30),
            cmath(r"\pi_{ij}", r"=", r"P(i \text{ and } j \text{ both sampled}),\ \ \pi_{ii} = \pi_i", font_size=30),
            cmath(r"\pi_i \propto y_i,\ |s|=n", r":", r"y_i/\pi_i \text{ constant} \Rightarrow \text{variance } 0", font_size=30),
            cmath(r"\text{in practice}", r":", r"\pi_i \propto \text{a size measure correlated with } y", font_size=30),
        ]
        rows[2][2].set_color(HIT)
        whys = [why(r"the design's joint probabilities enter"), why(r"Sen (1953), \ Yates \& Grundy (1953): \ an unbiased estimate"),
                why(r"the ideal, \ if we knew $y$"), why(r"chapter six's PPS: \ town size for town income")]
        with self.voiceover(
            "<bookmark mark='a'/> The variance involves the joint inclusion probabilities, the chance that two units "
            "are both sampled. <bookmark mark='b'/> A. R. Sen in 1953, and Frank Yates and Patricia Grundy the same "
            "year, gave an unbiased variance estimates under their design conditions, including positive pairwise "
            "inclusion probabilities where needed. <bookmark mark='c'/> Its message is simple: for positive y and a "
            "fixed-size sample, feasible inclusion probabilities proportional to y make every term y over pi constant"
            " and the total has zero variance. With random-size Poisson sampling, the number of terms still varies, "
            "so constant contributions alone do not give zero variance. <bookmark mark='d'/> We don't know y, but a "
            "size measure correlated with it gets close, which is what chapter six's probability proportional to size"
            " did with town populations."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def elephants(self):
        rows = fit_rows(VGroup(
            label(r"Basu (1971): \ a circus owner must ship 50 elephants, \ and wants their total weight", font_size=24),
            label(r"three years ago he weighed them all: \ Sambo was about average", font_size=22, color=GREY_A),
            label(r"plan: \ weigh Sambo, \ multiply by 50", font_size=24, color=HIT),
            label(r"the statistician: \ that's not a probability sample!", font_size=24, color=RES),
            label(r"his design: \ Sambo with probability $99/100$, \ each other elephant $1/4900$", font_size=24, color=OBS),
        ), 12.4, 0.45, [0, 0.4, 0])
        tag = historical_tag(r"D. Basu, \ in \emph{Foundations of Statistical Inference} (1971)", corner=DR)
        intro = label('An unbiased estimator can still have a poor error distribution', font_size=36)
        with self.voiceover(
            "Unbiasedness isn't everything, as Debabrata Basu showed in 1971 with a famous story. <bookmark "
            "mark='a'/> A circus owner has to ship fifty elephants and needs their total weight. <bookmark mark='b'/>"
            " Three years ago he weighed them all, and Sambo, the middle elephant, was about average. <bookmark "
            "mark='c'/> So his plan is to weigh Sambo again and multiply by fifty. <bookmark mark='d'/> The circus "
            "statistician is horrified: that isn't a probability sample, and there's no way to say how accurate it "
            "is. <bookmark mark='e'/> Instead he proposes a design: choose Sambo with probability ninety-nine in a "
            "hundred, and each of the other forty-nine elephants with probability one in four thousand nine hundred."
        ) as vo:
            self.play(FadeIn(intro))
            self.add(tag)
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def verdict(self):
        rows = [
            cmath(r"\text{Sambo drawn}", r":", r"\hat T = y_{\text{Sambo}} \times \tfrac{100}{99}", font_size=32),
            cmath(r"\text{Jumbo drawn}", r":", r"\hat T = y_{\text{Jumbo}} \times 4{,}900", font_size=32),
            cmath(r"E[\hat T]", r"=", r"T\ \ \text{exactly}", font_size=32),
            cmath(r"\text{the lesson}", r":", r"\text{unbiased, \ and absurd}", font_size=32),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"one elephant's weight, \ for the whole herd"), why(r"the biggest elephant, \ times 4,900"),
                why(r"Horvitz--Thompson keeps its promise"), why(r"the design must use what we know")]
        intro = label('An unbiased procedure can still give absurd individual estimates', font_size=36)
        with self.voiceover(
            "Sambo is drawn, of course. <bookmark mark='a'/> The Horvitz–Thompson estimate is Sambo's weight times a "
            "hundred over ninety-nine: about one elephant's weight, for a herd of fifty. <bookmark mark='b'/> Had the"
            " giant Jumbo been drawn instead, the estimate would have been Jumbo's weight times four thousand nine "
            "hundred. <bookmark mark='c'/> On average over the design, the estimator is exactly unbiased. <bookmark "
            "mark='d'/> And it's absurd. In Basu's story the circus owner fires the statistician, who becomes a "
            "teacher of statistics. The moral is not to abandon randomization but to design with what you know: "
            "inclusion probabilities should track the quantity being measured, and an estimator should be judged by "
            "its whole distribution, not only its mean."       ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def hajek(self):
        rows = [
            cmath(r"\hat{\bar y}_{\text{HT}}", r"=", r"\frac1N \textstyle\sum_{s} y_i/\pi_i", font_size=32),
            cmath(r"\hat{\bar y}_{\text{H\'ajek}}", r"=", r"\frac{\sum_s y_i/\pi_i}{\sum_s 1/\pi_i}", font_size=32),
            cmath(r"\text{slightly biased}", r",", r"\text{often far less variable}", font_size=30),
            cmath(r"\text{weights}", r":", r"\text{the language of every survey dataset}", font_size=30),
        ]
        rows[1][2].set_color(WEIGHT)
        whys = [why(r"divide the HT total by $N$"), why(r"H\'ajek (1971): \ divide by the estimated $N$"),
                why(r"a ratio estimator: \ chapter eight"), why(r"a weight column, \ $w_i = 1/\pi_i$, \ adjusted")]
        intro = label('A weighted mean can divide by a known or estimated population size', font_size=36).move_to([0, 3.2, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> For a mean, the Horvitz–Thompson estimate divides the weighted total by the known "
            "population size. <bookmark mark='b'/> Jaroslav Hájek suggested dividing instead by the sum of the "
            "weights, the sample's own estimate of N. <bookmark mark='c'/> It is generally biased, often only "
            "slightly for well-behaved large samples; an empty sample also needs a convention. When the sample size "
            "is random or the weights uneven it's usually much less variable: it doesn't let a lucky draw of heavily "
            "weighted units inflate the total. <bookmark mark='d'/> Every survey dataset you'll meet carries a weight"
            " column of this kind: one over the inclusion probability, adjusted, as chapter nine will show."      ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
