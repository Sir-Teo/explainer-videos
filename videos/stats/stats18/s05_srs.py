from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats18.common import *  # noqa: F403


class SimpleRandom(VoiceoverScene):
    def construct(self):
        self.card()
        self.fpc_derive()
        self.polls()
        self.size()
        self.town()
        self.systematic()
        self.soup()

    def card(self):
        card = chapter_card(4, r"Simple random sampling", r"Every set of $n$ equally likely", part=PART)
        with self.voiceover("Chapter four. Simple random sampling."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def fpc_derive(self):
        rows = [
            cmath(r"\bar y", r"=", r"\tfrac1n \textstyle\sum_i R_i y_i,\ \ P(R_i = 1) = f = n/N", font_size=30),
            cmath(r"\mathrm{Cov}(R_i, R_j)", r"=", r"-\frac{f(1 - f)}{N - 1}\ \ (i \ne j)", font_size=30),
            cmath(r"\mathrm{Var}(\bar y)", r"=", r"\Big(1 - \frac nN\Big)\frac{S^2}{n},\ \ S^2 = \tfrac{1}{N - 1}\textstyle\sum (y_i - \bar y_N)^2", font_size=30),
            cmath(r"1 - n/N", r":", r"\text{the finite-population correction}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"only $R$ is random"), why(r"drawing one person makes another less likely: \ $n$ is fixed"),
                why(r"Part 5's variance of a sum, \ term by term"), why(r"0 when $n = N$: \ a census has no sampling error")]
        with self.voiceover(
            "<bookmark mark='a'/> In a simple random sample of n from N without replacement, every set of n people is equally "
            "likely. Write the sample mean with inclusion indicators: each is one with probability f. <bookmark mark='b'/> But "
            "they aren't independent: the sample size is fixed, so including one person makes including another slightly less "
            "likely, a small negative covariance. <bookmark mark='c'/> Expanding the variance of the sum, Part 5's way, gives "
            "the variance of the mean: S squared over n, times one minus n over N. <bookmark mark='d'/> That factor is the "
            "finite-population correction. It's zero when the sample is the whole population, since a census has no sampling "
            "error, and very close to one whenever the sample is a small fraction of the population."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def polls(self):
        d = load("digest")
        N, K = d["N"], int(round(d["truth"] * d["N"]))
        g = np.random.Generator(np.random.PCG64(1000))
        est = g.hypergeometric(K, N - K, 1000, size=2000) / 1000
        e = np.linspace(0.3, 0.46, 33)
        A = axes([0.3, 0.46], [0, 260], x_length=8.4, y_length=4.0, xlabel=r"Blue's share in a poll of 1,000", ylabel=r"polls",
                 xticks=[0.32, 0.36, 0.4, 0.44], yticks=[0, 100, 200], center=[-1.4, 0.3, 0], xfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        bars = hist_bars(ax, e, np.histogram(est, e)[0], color=BLUE, opacity=0.8)
        tr = DashedLine(ax.c2p(d["truth"], 0), ax.c2p(d["truth"], 250), color=S.TRUTH, stroke_width=3)
        sd = float(np.std(est))
        rows = fit_rows(VGroup(
            label(r"2,000 simple random samples of 1,000", font_size=22),
            MathTex(rf"\text{{SD}} = {100 * sd:.2f}\ \text{{points}}", font_size=28, color=BLUE),
            MathTex(rf"\sqrt{{p(1-p)/n}} = {100 * np.sqrt(d['truth'] * (1 - d['truth']) / 1000):.2f}", font_size=26),
            label(r"centred on the truth: \ no bias", font_size=22, color=HIT),
            label(r"the hypergeometric law, \ exactly (Part 3)", font_size=20, color=GREY_A),
        ), 4.2, 0.38, [4.8, 0.3, 0])
        tag = simulated_tag(r"the World's polling firm", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Let the World's polling firm run two thousand honest polls, each a simple random sample of a "
            "thousand adults. <bookmark mark='b'/> Their estimates of Blue's share spread with a standard deviation of one and a "
            "half points, <bookmark mark='c'/> just as the formula says. <bookmark mark='d'/> And they're centred on the truth: "
            "a random sample has no bias. <bookmark mark='e'/> The number of Blue voters in each poll follows Part 3's "
            "hypergeometric distribution exactly; nothing here is an approximation except the normal curve we'll draw "
            "around it."
        ) as vo:
            self.play(FadeIn(A), Create(tr), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.03), FadeIn(rows[0]), run_time=1.8)
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def size(self):
        rows = [
            cmath(r"\text{margin of error}", r"=", r"1.96\sqrt{p(1 - p)/n}", font_size=32),
            cmath(r"p = \tfrac12", r":", r"1.96 \times \frac{0.5}{\sqrt n} \approx \frac{1}{\sqrt n}", font_size=32),
            cmath(r"\pm 3\ \text{points}", r":", r"n \approx 1/0.03^2 \approx 1{,}100", font_size=32),
            cmath(r"N", r":", r"\text{barely matters: \ the fpc is } 1 - n/N \approx 1", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"the 95\% half-width for a share"), why(r"the worst case"),
                why(r"the size of most national polls"), why(r"the same for the World as for a nation of 300 million")]
        with self.voiceover(
            "<bookmark mark='a'/> That's why polls have about a thousand people. The margin of error for a share is one point "
            "nine six times the square root of p times one minus p over n. <bookmark mark='b'/> At its worst, p equal to a "
            "half, that's about one over the square root of n. <bookmark mark='c'/> So plus or minus three points needs about "
            "eleven hundred people. <bookmark mark='d'/> And the size of the population hardly matters. The finite-population "
            "correction is one minus n over N, essentially one for a thousand people out of seven hundred thousand or out of "
            "three hundred million. A poll of a thousand is as accurate for a country as for a city."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def town(self):
        d = load("srs")
        rows = fit_rows(VGroup(
            label(rf"one town: \ {d['N']:,} adults; \ sample half of them, \ {d['n']}", font_size=24),
            MathTex(rf"1 - n/N = {d['fpc']:.2f}:\ \ \text{{the SE shrinks by }} \sqrt{{0.5}} = 0.71", font_size=28),
            MathTex(rf"\text{{coverage with the fpc}}: {100 * d['cover_fpc']:.1f}\%", font_size=28, color=HIT),
            MathTex(rf"\text{{without it}}: {100 * d['cover_no']:.1f}\%", font_size=28, color=S.CONS),
            label(r"too wide, \ not wrong: \ ignoring the fpc is conservative", font_size=22, color=GREY_A),
            label(r"incomes are skewed: \ 93.7\%, \ not quite 95", font_size=20, color=GREY_B),
        ), 12.0, 0.42, [0, 0, 0])
        tag = simulated_tag(r"4,000 samples of mean income", corner=DR)
        with self.voiceover(
            "When does the correction matter? When the sample is a large share of the population. <bookmark mark='a'/> Take "
            "one town of eleven hundred adults and sample half of them, to estimate their mean income. "
            "<bookmark mark='b'/> Now one minus n over N is a half, and the standard error is seventy-one percent of the naive "
            "one. <bookmark mark='c'/> With the correction, the ninety-five percent intervals cover the town's mean ninety-three "
            "point seven percent of the time. <bookmark mark='d'/> Without it, ninety-eight and a half percent: "
            "<bookmark mark='e'/> too wide, but not wrong. Leaving out the correction is always conservative. "
            "<bookmark mark='f'/> The small shortfall with it comes from the skew of incomes, Part 11's old enemy, not from the "
            "design."
        ) as vo:
            self.add(tag)
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def systematic(self):
        rows = [
            cmath(r"k", r"=", r"N/n;\ \ \text{start at random } r \in \{1, \ldots, k\}", font_size=30),
            cmath(r"\text{sample}", r":", r"r,\ r + k,\ r + 2k, \ldots", font_size=30),
            cmath(r"\text{a list in order}", r":", r"\text{an implicit stratification}", font_size=30),
            cmath(r"\text{a list with a period } k", r":", r"\text{disaster}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"every unit has chance $1/k$"), why(r"Bowley's one house in twenty"),
                why(r"sorted by street or size: \ a spread-out sample"), why(r"every $k$-th flat a corner flat")]
        with self.voiceover(
            "A cousin of simple random sampling deserves a word, because it's what Bowley did. <bookmark mark='a'/> In "
            "systematic sampling, divide the list into stretches of k and pick a random starting point in the first. "
            "<bookmark mark='b'/> Then take every k-th unit after it. Each unit has the same chance, one in k. "
            "<bookmark mark='c'/> If the list is ordered, by street or by size, the sample is automatically spread across the "
            "order: an implicit stratification, often more precise than an SRS. <bookmark mark='d'/> But if the list has a "
            "period that matches k, say every tenth flat on a register is a corner flat, the sample can be wildly "
            "unrepresentative, and nothing in the data will warn you."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k_, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k_, transform=False)
        self.clear_scene()

    def soup(self):
        rows = fit_rows(VGroup(
            label(r"``you don't have to eat the whole pot to taste the soup''", font_size=26, color=OBS),
            label(r"if it's well stirred: \ the stirring is the randomization", font_size=24),
            label(r"a spoonful's accuracy depends on the spoon, \ not the pot", font_size=24, color=HIT),
            label(r"unstirred, \ a bucketful from the top tells you about the top", font_size=24, color=RES),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "There's an old line about this. <bookmark mark='a'/> You don't have to eat the whole pot to know how the soup "
            "tastes, <bookmark mark='b'/> as long as it's well stirred. The stirring is the randomization. "
            "<bookmark mark='c'/> And a spoonful's accuracy depends on the size of the spoon, not of the pot. "
            "<bookmark mark='d'/> If the soup isn't stirred, a whole bucketful from the top tells you only about the top. That's "
            "the Digest."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
