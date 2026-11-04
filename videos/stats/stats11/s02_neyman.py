from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats11.common import *  # noqa: F403


class Neyman(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.definition()
        self.rain()
        self.not_meaning()
        self.one_sided()
        self.levels()
        self.planning()

    def card(self):
        card = chapter_card(1, r"Neyman's promise", r"What does ``95\% confident'' mean?", lit=(1937,), part=PART)
        with self.voiceover("Chapter one. Neyman's promise."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        hc = history_card(1937, r"Jerzy Neyman, \ \emph{Phil.\ Trans.\ A} 236", r"``Outline of a theory of statistical estimation based on the "
                          r"classical theory of probability'': \ intervals with a guaranteed long-run rate of success, \ whatever the "
                          r"true parameter", color=OBS, width=9.4, font_size=24).move_to([0, 1.2, 0])
        rows = fit_rows(VGroup(
            label(r"Laplace and Gauss had used $\pm$ probable errors for a century, \ informally", font_size=24, color=GREY_A),
            label(r"Fisher's rival idea, \ the \emph{fiducial} interval (1930), \ was never made coherent", font_size=24, color=GREY_A),
            label(r"Neyman made the interval itself the random object", font_size=28, color=OBS),
        ), 12.6, 0.32, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The theory of confidence intervals was set out by Jerzy Neyman in 1937, in a long paper "
            "with a modest title: an outline of a theory of statistical estimation based on the classical theory of "
            "probability. <bookmark mark='b'/> Laplace and Gauss had attached plus-or-minus errors to their estimates for a "
            "century, but informally. <bookmark mark='c'/> Fisher had proposed his own idea, the fiducial interval, which "
            "treated the parameter as if it had a distribution after the data; it led to paradoxes that were never "
            "resolved. <bookmark mark='d'/> Neyman's move was to make the interval itself the random object, and to ask "
            "how often it would succeed."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def definition(self):
        dc = definition_card(r"Confidence set", r"$C(X)$ is a $1 - \alpha$ \emph{confidence set} for $\theta$ \ if \ "
                             r"$P_\theta\big(\theta \in C(X)\big) \ge 1 - \alpha$ \ for every $\theta$.", color=OBS, width=9.4,
                             font_size=28).move_to([0, 1.6, 0])
        rows = fit_rows(VGroup(
            label(r"the probability is over the data $X$; \ $\theta$ is fixed, \ unknown, \ not random", font_size=26),
            label(r"``for every $\theta$'': \ the promise must hold whatever the truth is \ (the sawtooth breaks exactly this)", font_size=24,
                  color=GREY_A),
            label(r"the infimum over $\theta$ is the \emph{confidence coefficient}; \ the average over $\theta$ is not enough", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.34, [0, -1.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the definition. A rule that turns data into a set is a ninety-five percent "
            "confidence set if, for every possible value of the parameter, the probability that the set contains it is "
            "at least ninety-five percent. <bookmark mark='b'/> The probability is over the data. The parameter is fixed, "
            "unknown but not random. <bookmark mark='c'/> And the words for every theta matter. The promise must hold "
            "whatever the truth is, which is exactly what the Wald interval fails: it's fine for some p and terrible for "
            "others. <bookmark mark='d'/> Strictly, the guaranteed level is the worst case over all theta, called the "
            "confidence coefficient. An interval that's ninety-five percent only on average over theta hasn't kept the "
            "promise."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def rain(self):
        d = load("rain")
        ints = np.asarray(d["ints"])
        A = axes([160, 192], [0, 100], x_length=7.6, y_length=5.8, xlabel=r"mean height of the World's men (cm): \ $t$-intervals, \ $n = 10$",
                 xticks=[165, 170, 176, 180, 185, 190], center=[-1.8, -0.2, 0])
        ax = A.ax
        r = IntervalRain(ax, d["mu"], y_top=100, dy=1.0, stroke_width=2.2, font_size=28, tally_pos=[4.6, 1.8, 0])
        rows = fit_rows(VGroup(
            MathTex(rf"\mu = {d['mu']:.1f}\ \text{{cm}}", font_size=30, color=EXACT),
            label(r"each line: \ one sample of 10, \ its 95\% interval", font_size=24, color=GREY_A),
            label(rf"over 10,000 samples: \ {100 * d['cov10k']:.1f}\%", font_size=26, color=OBS),
            label(rf"average width {d['width']:.1f} cm", font_size=24, color=GREY_A),
        ), 4.8, 0.34, [4.6, -0.6, 0])
        tag = simulated_tag(r"the World: \ heights", corner=DR)
        with self.voiceover(
            "Here's the promise in action. The World knows the true mean height of its men: <bookmark mark='a'/> one "
            "hundred and seventy-six centimetres. <bookmark mark='b'/> Draw ten men, compute Student's t-interval, and "
            "draw it as a line. Green if it catches the truth, red if it misses. Another sample, another line. "
            "<bookmark mark='c'/> Let it rain: a hundred samples. Each interval is different, centred where its sample "
            "happened to fall. Most catch the truth; a few miss. <bookmark mark='d'/> Ninety-three out of this hundred. "
            "Over ten thousand samples, ninety-four point nine percent. That's what ninety-five percent confidence means: "
            "a long-run rate of success for the procedure."
        ) as vo:
            self.play(FadeIn(A), FadeIn(r), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            r.rain(self, ints[:1], run_time=1.0)
            r.rain(self, ints[1:3], run_time=1.0, lag=0.5)
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            r.rain(self, ints[3:100], run_time=6.0, lag=0.06)
            vo.wait_until("d")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def not_meaning(self):
        rows = fit_rows(VGroup(
            label(r"after the data are in: \ one interval, \ say $[171.4, 180.2]$", font_size=28),
            label(r"wrong: \ ``there is a 95\% chance that $\mu$ is in $[171.4, 180.2]$''", font_size=28, color=MISS),
            label(r"$\mu$ is in it, \ or it is not: \ the 95\% belongs to the procedure, \ not this interval", font_size=26),
            label(r"a ring-toss machine that rings the peg 95\% of the time: \ this throw either rang it or did not", font_size=24,
                  color=GREY_A),
            label(r"a probability for $\mu$ itself needs a prior: \ chapter 10, \ Part 15", font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now the hard part. You've collected your one sample and computed your one interval: "
            "say, a hundred and seventy-one point four to a hundred and eighty point two. <bookmark mark='b'/> It's very "
            "tempting to say there's a ninety-five percent chance the true mean lies in that interval. In Neyman's theory "
            "that's wrong. <bookmark mark='c'/> The mean is either in it or not; nothing about it is random any more. "
            "The ninety-five percent describes the procedure, not this particular interval. <bookmark mark='d'/> Think "
            "of a ring-toss machine that rings the peg ninety-five percent of the time. Once a ring has landed, it either "
            "rang the peg or it didn't. <bookmark mark='e'/> To put a probability on the mean itself, you need a prior "
            "distribution for it, which is the Bayesian answer of chapter ten and Part 15."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def levels(self):
        d = load("rain")
        lo, hi = d["ints"][0]
        m, half = (lo + hi) / 2, (hi - lo) / 2
        se = half / stats.t.ppf(0.975, 9)
        A = axes([160, 192], [0, 4], x_length=9.0, y_length=3.0, xlabel=r"one sample of 10 men (cm)", xticks=[165, 170, 175, 180, 185, 190],
                 center=[0, 0.6, 0])
        ax = A.ax
        lines = VGroup()
        for i, (lev, c) in enumerate(((0.80, S.PRIOR), (0.95, OBS), (0.99, MISS))):
            h = stats.t.ppf(1 - (1 - lev) / 2, 9) * se
            y = 3 - i
            lines.add(VGroup(Line(ax.c2p(m - h, y), ax.c2p(m + h, y), color=c, stroke_width=5),
                             label(rf"{int(lev * 100)}\%: \ $\pm {h:.1f}$", font_size=24, color=c).next_to(ax.c2p(m + h, y), RIGHT, buff=0.2)))
        foot = fit_rows(VGroup(
            label(r"more confidence costs width: \ the same data, \ three promises", font_size=26, color=OBS),
            label(r"a 100\% interval for a mean is the whole line: \ certain, \ and useless", font_size=24, color=GREY_A),
            label(r"the only way to buy both is more data: \ width $\propto 1/\sqrt n$", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The level is a choice, and it costs width. Here is one sample of ten men, with its "
            "eighty, ninety-five and ninety-nine percent intervals. <bookmark mark='b'/> More confidence, wider interval. "
            "<bookmark mark='c'/> A hundred percent interval for a mean would be the whole real line: certain to be right, "
            "and useless. <bookmark mark='d'/> To be both confident and precise, you need more data: width shrinks like "
            "one over root n, as Part 8 showed."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(l_[0]) for l_ in lines], lag_ratio=0.4), *[FadeIn(l_[1]) for l_ in lines])
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k]))
        self.clear_scene()

    def planning(self):
        rows = [
            cmath(r"\text{margin}", r"=", r"1.96\sqrt{\frac{p(1 - p)}{n}} \le 1.96\sqrt{\frac{1}{4n}}", font_size=34),
            cmath(r"1.96\sqrt{\frac{1}{4n}} = 0.03", r"\Rightarrow", r"n = \Big(\frac{1.96}{2 \times 0.03}\Big)^2 \approx 1{,}067", font_size=32),
            cmath(r"\text{halve the margin}", r"\Rightarrow", r"4\times \text{ the sample}", font_size=34),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"the worst case is $p = \tfrac12$"), why(r"the pollster's ``about a thousand'' (Part 8)"),
                why(r"width $\propto 1/\sqrt n$")]
        foot = label(r"a margin of error is half a confidence interval's width \ for one proportion, \ not for the gap between two", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Intervals also plan studies. <bookmark mark='a'/> A poll's margin of error is half the width of a ninety-five "
            "percent interval for a proportion, and it's largest when p is a half. <bookmark mark='b'/> Set it to three "
            "points and solve: about a thousand and sixty-seven respondents, the famous poll of about a thousand that Part "
            "8 met. <bookmark mark='c'/> Halving the margin to a point and a half needs four times the sample, over four "
            "thousand. <bookmark mark='d'/> And a common slip: the margin applies to one candidate's share. The gap "
            "between two candidates is uncertain by nearly twice as much."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=0.0, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def one_sided(self):
        rows = [
            cmath(r"P_\theta\big(\theta \le U(X)\big)", r"\ge", r"1 - \alpha", r"\quad\text{an upper confidence bound}", font_size=32),
            cmath(r"\bar x + t_{n-1,\,0.95}\,\frac{s}{\sqrt n}", r"\quad", r"\text{all of } \alpha \text{ in one tail}", font_size=32),
        ]
        rows[1][0].set_color(OBS)
        whys = [why(r"``the side-effect rate is at most\dots''; \ ``the strength is at least\dots''"),
                why(r"$t_{0.95}$, \ not $t_{0.975}$: \ a tighter bound on the side that matters")]
        foot = label(r"chosen before the data, \ like a one-sided test (Part 10): \ the duality again", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Sometimes only one side matters. <bookmark mark='a'/> A regulator wants an upper bound on a side-effect rate; "
            "an engineer wants a lower bound on a beam's strength. A one-sided confidence bound promises that the "
            "parameter is below it, or above it, with probability at least ninety-five percent. <bookmark mark='b'/> For a "
            "mean, that's x-bar plus t point nine five standard errors, with all five percent in one tail, so the bound is "
            "tighter than the end of the two-sided interval. <bookmark mark='c'/> Like a one-sided test, the side has to "
            "be chosen before looking at the data. It's the duality again: one-sided bounds invert one-sided tests."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=1.8, x=0.0, buff=1.0, edge=6.9)
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                step(k, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
