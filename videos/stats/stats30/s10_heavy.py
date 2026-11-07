from __future__ import annotations

import numpy as np

from videos.stats.stats30.common import *  # noqa: F403


class Heavy(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.skew()
        self.mom()
        self.proof()
        self.catoni()
        self.vectors()
        self.race()
        self.lesson()

    def card(self):
        card = chapter_card(9, r"Heavy-tailed means", r"Median of means", lit=(1983,), part=PART)
        with self.voiceover("Chapter nine. Estimating the mean of heavy-tailed data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"\text{goal}", r":", r"\text{the mean } \mu \text{ itself, \ not a centre of symmetry}", font_size=30),
            cmath(r"\text{only}", r":", r"\mathrm{Var}\,X = \sigma^2 < \infty", font_size=32),
            cmath(r"\bar X", r":", r"P(|\bar X - \mu| > t) \le \sigma^2/(n t^2): \ \ \text{polynomial tails}", font_size=28),
            cmath(r"\text{want}", r":", r"|\hat\mu - \mu| \le C \sigma \sqrt{\log(1/\delta)/n} \ \text{ w.p. } 1 - \delta", font_size=28),
        ]
        rows[3][2].set_color(MOMC)
        whys = [why(r"skewed data: \ medians and trimming are biased"), why(r"no higher moments assumed"),
                why(r"Chebyshev: \ the bound is tight for the mean"), why(r"sub-Gaussian deviations")]
        with self.voiceover(
            "<bookmark mark='a'/> A different goal. Sometimes we want the mean itself, of income or of a loss, and "
            "the data are skewed, so the median, Hodges–Lehmann and trimmed means all estimate something else. "
            "<bookmark mark='b'/> Suppose only that the variance is finite. <bookmark mark='c'/> Then the sample "
            "mean's deviations always obey Chebyshev; without extra distributional assumptions no uniformly "
            "sub-Gaussian sample-mean bound follows. In particular, its tails can be polynomial, so a rare huge "
            "observation spoils it. <bookmark mark='d'/> What we'd like is a sub-Gaussian guarantee: error of order "
            "sigma root log one over delta over n, with probability one minus delta, as if the data were normal."
        ) as vo:
            intro=label('Estimating a mean differs from estimating a resistant center',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mom(self):
        g = np.random.default_rng(5)
        z = g.pareto(2.2, 60)
        k = 6
        blocks = np.array_split(z, k)
        means = [b.mean() for b in blocks]
        A = axes([0, 7], [0,max(4.5,float(z.max())+.2)], x_length=7.4, y_length=4.4, xlabel=r"block", ylabel=r"value", xticks=[1, 2, 3, 4, 5, 6],
                 yticks=[0, 1, 2, 3, 4], center=[-2.0, 0.3, 0])
        ax = A.ax
        pts = VGroup()
        for j, b in enumerate(blocks):
            for v in b:
                pts.add(Dot(ax.c2p(j + 1 + g.uniform(-0.25, 0.25), v), radius=0.04, color=GREY_B, fill_opacity=0.7))
        bm = VGroup(*[Line(ax.c2p(j + 0.65, m), ax.c2p(j + 1.35, m), color=MOMC, stroke_width=4) for j, m in enumerate(means)])
        med = DashedLine(ax.c2p(0.3, np.median(means)), ax.c2p(6.7, np.median(means)), color=HLC, stroke_width=3)
        tru = DashedLine(ax.c2p(0.3, 1 / 1.2), ax.c2p(6.7, 1 / 1.2), color=TRUE, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"60 Lomax draws, \ mean 0.83, \ in 6 blocks", font_size=22),
            label(r"orange: \ each block's mean", font_size=22, color=MOMC),
            label(rf"blue: \ their median, \ {np.median(means):.2f}", font_size=22, color=HLC),
            label(rf"vs the overall mean, \ {z.mean():.2f}", font_size=22, color=MEANC),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The median of means, found independently by Arkadi Nemirovski and David Yudin, by Mark "
            "Jerrum, Leslie Valiant and Vijay Vazirani, and by Noga Alon, Yossi Matias and Mario Szegedy. Split the sample "
            "into k blocks. <bookmark mark='b'/> Average each block. <bookmark mark='c'/> Report the median of the block "
            "means. <bookmark mark='d'/> A single huge observation can ruin one block's mean, but the median ignores a "
            "minority of ruined blocks."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b) for b in bm], lag_ratio=0.2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(med), Create(tru), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"P\bigl(|\bar X_j - \mu| > 2\sigma\sqrt{k/n}\bigr)", r"\le", r"\tfrac14", font_size=30),
            cmath(r"\text{median fails}", r"\Rightarrow", r"\ge k/2 \text{ blocks fail}", font_size=30),
            cmath(r"P(\text{Binomial}(k, \tfrac14) \ge \tfrac k2)", r"\le", r"e^{-k/8}", font_size=30),
            cmath(r"k = 8 \log(1/\delta)", r":", r"|\hat\mu - \mu| \le 2\sigma\sqrt{8 \log(1/\delta)/n} \ \text{ w.p. } 1 - \delta", font_size=26),
        ]
        rows[3][2].set_color(MOMC)
        whys = [why(r"Chebyshev in each block of size $n/k$"), why(r"the median is past half of them"),
                why(r"Hoeffding, \ Part 6"), why(r"sub-Gaussian, \ assuming only a variance")]
        with self.voiceover(
            "<bookmark mark='a'/> The proof is three lines. For equally sized independent blocks, each has n over k "
            "points, so by Chebyshev its mean is more than two sigma root k over n from mu with probability at most a"
            " quarter. <bookmark mark='b'/> For the median to be that far off, at least half the blocks must fail. "
            "<bookmark mark='c'/> The number of failing blocks is at most binomial with probability a quarter, and by"
            " Hoeffding's inequality reaching half has probability below e to the minus k over eight. <bookmark "
            "mark='d'/> Choose k as the ceiling of eight log one over delta, with at least one observation per block."
            " For unequal blocks use the floor of n over k in the error bound: the error is below a constant times "
            "sigma root log one over delta over n, with probability one minus delta. A sub-Gaussian guarantee from a "
            "variance alone."
        ) as vo:
            intro=label('Independent block averages turn Chebyshev bounds into a median guarantee',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def catoni(self):
        rows = [
            cmath(r"\textstyle\sum_i \psi\bigl(\alpha(x_i - \theta)\bigr)", r"=", r"0", font_size=32),
            cmath(r"\psi(u)", r"=", r"\mathrm{sign}(u) \log(1 + |u| + u^2/2)", font_size=30),
            cmath(r"\alpha", r"=", r"\sqrt{2L(n-2L)/(n^2 v)},\ L=\log(2/\delta),\ v\ge\sigma^2", font_size=30),
            cmath(r"\text{constant}", r":", r"\text{optimal: \ } \sqrt2\, \sigma \sqrt{\log(1/\delta)/n}(1 + o(1))", font_size=28),
        ]
        rows[1][2].set_color(HUBC)
        whys = [why(r"an M-estimator"), why(r"grows only logarithmically"), why(r"known variance bound; $n>2\log(2/\delta)$"),
                why(r"Catoni (2012); \ Lugosi \& Mendelson (2019)")]
        with self.voiceover(
            "<bookmark mark='a'/> Olivier Catoni found an M-estimator with the optimal constant. <bookmark mark='b'/>"
            " Its psi grows only like a logarithm, so huge observations have little pull. <bookmark mark='c'/> Its "
            "tuning alpha uses the confidence level and a supplied upper bound on the variance. Our simulation "
            "supplies the true Lomax variance, rather than substituting an unverified sample variance. <bookmark "
            "mark='d'/> Its deviation bound matches the normal's sample mean, root two sigma root log one over delta "
            "over n, to first order. Gábor Lugosi and Shahar Mendelson extended these ideas to vectors and to "
            "learning."
        ) as vo:
            intro=label('Catoni tuning uses a confidence level and a variance upper bound',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def race(self):
        d = load("mom")
        q = d["q"]
        hdr = [r"\textbf{estimator}", r"\textbf{median error}", r"\textbf{90\%}", r"\textbf{99\%}", r"\textbf{99.9\%}"]
        spec = (("mean", r"sample mean"), ("trim5", r"5\% trimmed mean"), ("mom", r"median of 20 means"), ("catoni", r"Catoni, \ $\delta = 0.001$"))
        body = [[t] + [f"{q[k][s]:.3f}" for s in ("0.5", "0.9", "0.99", "0.999")] for k, t in spec]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.32, colors=[GREY_A, MEANC, TRIMC, MOMC, HUBC])
        tb.move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(rf"{d['R']:,} samples of $n = {d['n']}$ from a Lomax (shifted Pareto) with shape {d['alpha']} \ (finite variance, \ infinite third moment)", font_size=22),
            label(rf"20 blocks: theorem failure bound {d['delta_k']:.3f}; Catoni $\delta=.001$ with known variance; empirical quantiles", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A race on four thousand samples of five hundred from a Pareto distribution with "
            "shape two point two: finite variance, infinite third moment, a long right tail. Quantiles of the "
            "absolute error. <bookmark mark='b'/> The sample mean has median absolute error about point oh five five,"
            " but its empirical point nine nine nine error is point eight one. Catoni with the known variance has "
            "median error about point oh five two here. <bookmark mark='c'/> In this experiment the fixed-fraction "
            "trimmed mean does not consistently target the original mean: it cuts the long tail and is biased by a "
            "quarter. <bookmark mark='d'/> The median of twenty means gives up a little in the middle and has an "
            "empirical point nine nine nine error quantile around point two six in this run. It does not cap the "
            "largest possible error. Here Catoni with the known variance has a one-in-a-thousand error about point "
            "two eight. That empirical quantile is based on only four expected tail observations and is not a "
            "finite-sample guarantee. When the tail matters, the right question is not average error but the "
            "guarantee at a confidence level."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tb[k + 1]))
            self.play(FadeIn(tb[4]), FadeIn(foot[1]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"robust to what? \ outliers, \ or heavy tails: \ different goals", font_size=24),
            label(r"symmetric contamination: \ estimate the centre \ (Huber, \ HL)", font_size=24, color=HUBC),
            label(r"heavy tails, \ the mean wanted: \ median of means, \ Catoni", font_size=24, color=MOMC),
            label(r"adversarial corruption in many dimensions: \ Part 60", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Robust to what? Gross errors and heavy tails are different problems. "
            "<bookmark mark='b'/> If a few observations are wrong and the rest symmetric, estimate the centre with Huber or "
            "Hodges–Lehmann. <bookmark mark='c'/> If every observation is genuine but the distribution has a heavy tail and "
            "you want its mean, use median of means or Catoni. <bookmark mark='d'/> And if an adversary corrupts a fraction of "
            "high-dimensional data, Part 60 has the modern answers."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def vectors(self):
        rows = [
            cmath(r"\text{vectors}", r":", r"\text{the coordinate-wise median of means is not enough}", font_size=28),
            cmath(r"\text{tournaments}", r":", r"\text{directional comparisons of candidate centers using block statistics}", font_size=30),
            cmath(r"\text{rate}", r":", r"\sqrt{\mathrm{tr}\,\Sigma / n} + \sqrt{\|\Sigma\| \log(1/\delta)/n}", font_size=30),
            cmath(r"\text{computation}", r":", r"\text{polynomial time: \ Hopkins (2020)}", font_size=30),
        ]
        rows[2][2].set_color(MOMC)
        whys = [why(r"its error grows with dimension"), why(r"Lugosi \& Mendelson (2019)"), why(r"as if the data were Gaussian"),
                why(r"Cherapanamjeri, \ Flammarion \& Bartlett (2019)")]
        with self.voiceover(
            "<bookmark mark='a'/> In many dimensions, applying median of means coordinate by coordinate loses a factor that "
            "grows with dimension. <bookmark mark='b'/> Gábor Lugosi and Shahar Mendelson's tournaments compare block means "
            "in every direction and pick the point that wins most contests. <bookmark mark='c'/> They achieve the error a "
            "Gaussian sample mean would have, with only a covariance assumed. <bookmark mark='d'/> Making that computable in "
            "polynomial time took until 2019 and 2020, in work by Samuel Hopkins and others, and it is part of Part 60."
        ) as vo:
            intro=label('Directional methods can achieve covariance-dependent deviation rates',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def skew(self):
        rows = [
            cmath(r"\text{symmetric } F", r":", r"\text{mean} = \text{median} = \text{trimmed means}", font_size=30),
            cmath(r"\text{skewed } F", r":", r"\text{trimmed means} \to \text{something else}", font_size=30),
            cmath(r"\text{Lomax}(2.2)", r":", r"\text{mean } 0.83, \ \text{median } 0.37", font_size=32),
            cmath(r"\text{so}", r":", r"\text{robust location } \ne \text{ robust estimation of the mean}", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"one centre, \ many estimators"), why(r"each targets its own functional"), why(r"a long right tail"),
                why(r"different targets")]
        with self.voiceover(
            "<bookmark mark='a'/> For a symmetric distribution with an existing mean, the mean and symmetric trimmed "
            "means equal the symmetry center; medians may be nonunique without additional conditions. <bookmark "
            "mark='b'/> For a skewed one they are different functionals, and each estimator converges to its own. "
            "<bookmark mark='c'/> The Pareto distribution of this chapter has mean point eight three but median point"
            " three seven. <bookmark mark='d'/> So the robust location estimators of the earlier chapters are not "
            "robust estimators of the mean: they answer a different question."
        ) as vo:
            intro=label('Under skewness, location procedures need not target the mean',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
