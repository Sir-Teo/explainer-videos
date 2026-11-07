from __future__ import annotations

import numpy as np

from videos.stats.stats56.common import *  # noqa: F403


class Clustering(VoiceoverScene):
    def construct(self):
        self.card()
        self.double_dip()
        self.test()
        self.faithful()
        self.null_hist()
        self.why_works()
        self.extensions()

    def card(self):
        card = chapter_card(9, r"Selection in unsupervised problems", r"Testing the clusters you found", lit=(2022,), part=PART)
        with self.voiceover("Chapter nine. Selection in unsupervised problems: testing the clusters you found."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def double_dip(self):
        rows = [
            cmath(r"\text{cluster}", r":", r"\text{split the data into groups } \hat C_1, \hat C_2 \text{ by an algorithm}", font_size=34),
            cmath(r"\text{test}", r":", r"H_0: \mu_{\hat C_1} = \mu_{\hat C_2} \text{ with a } z\text{- or } t\text{-test}", font_size=34),
            cmath(r"\text{but}", r":", r"\text{the split makes the means differ: \ rejects anyway}", font_size=32),
            cmath(r"\text{e.g.}", r":", r"\text{single-cell RNA: \ are these cell types, \ or one type cut in two?}", font_size=32),
        ]
        rows[2][-1].set_color(NAIVEC)
        whys = [why(r"$k$-means, \ hierarchical"), why(r"the obvious next step"), why(r"double dipping"), why(r"the motivating science")]
        head = label('Double dip', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> In unsupervised learning the selection is the whole analysis. An algorithm splits the data "
            "into clusters. <bookmark mark='b'/> The obvious next step is to test whether the clusters' means differ. "
            "<bookmark mark='c'/> But the algorithm chose the split precisely to make the means differ, so the test rejects "
            "even when there is only one group: double dipping. <bookmark mark='d'/> In single-cell genomics this is the "
            "everyday question: are these two clusters different cell types, or one type cut in two?"
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def test(self):
        rows = [
            cmath(r"\nu", r":", r"\text{the contrast with } \nu'x = \bar x_{\hat C_2} - \bar x_{\hat C_1}", font_size=36),
            cmath(r"x'(\phi)", r"=", r"x + (\phi - \nu'x)\,\nu/\|\nu\|^2: \ \text{move only along the difference}", font_size=32),
            cmath(r"S", r"=", r"\{\phi \ge 0: \ \text{clustering } x'(\phi) \text{ gives the same clusters}\}", font_size=34),
            cmath(r"p", r"=", r"P\big(\phi \ge \nu'x \mid \phi \in S\big), \ \ \phi \sim \sigma\|\nu\|\chi_1 \text{ under } H_0", font_size=32),
        ]
        rows[2][-1].set_color(SELC)
        rows[3][-1].set_color(CONDC)
        whys = [why(r"in $d$ dimensions, \ its norm"), why(r"keep everything else fixed"), why(r"analytic quadratic inequalities for global 1D two-means"), why(r"Gao, \ Bien \& Witten (2024)")]
        head = label('Test', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Lucy Gao, Jacob Bien and Daniela Witten condition on the clustering. Let nu be the contrast that gives the difference of the two clusters' means. <bookmark mark='b'/> Perturb the data along that contrast only, replacing the observed difference by phi and keeping everything else fixed. <bookmark mark='c'/> The set S collects the values of phi for which the algorithm, rerun on the perturbed data, finds the same clusters. <bookmark mark='d'/> Under the null the difference is sigma times the norm of nu times a chi variable, and the selective p-value is its chance of exceeding the observed difference, conditional on lying in S. For our global one dimensional two-means algorithm, alternative sorted split costs are quadratic in phi. Solving their inequalities gives the selection region analytically, without a grid. The cited papers develop related calculations for hierarchical and k-means algorithms."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def faithful(self):
        d = load("cluster")
        f, n = d["faithful"], d["newcomb"]
        xs = np.asarray(f["x"])
        A = axes([1.4, 5.3], [0, 40], x_length=5.6, y_length=3.2, xlabel=r"Old Faithful: \ eruption (minutes)", ylabel=r"",
                 xticks=[2, 3, 4, 5], yticks=[0, 20, 40], center=[-3.6, 1.35, 0])
        B = axes([14, 42], [0, 14], x_length=5.6, y_length=3.2, xlabel=r"Newcomb, \ outliers removed", ylabel=r"",
                 xticks=[20, 30, 40], yticks=[0, 7, 14], center=[3.3, 1.35, 0])

        def hist(ax, x, lo, hi, nb, cut):
            e = np.linspace(lo, hi, nb + 1)
            h, _ = np.histogram(x, e)
            g = VGroup()
            for a, b, c in zip(e[:-1], e[1:], h):
                if c == 0:
                    continue
                col = SELC if (a + b) / 2 > cut else CONDC
                g.add(Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0] - 0.02, height=ax.c2p(0, c)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                fill_color=col, fill_opacity=0.8).move_to([(ax.c2p(a, 0)[0] + ax.c2p(b, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, c)[1]) / 2, 0]))
            return g

        hf = hist(A.ax, xs, 1.5, 5.2, 37, f["cut"])
        hn = hist(B.ax, np.asarray(n["x"]), 15, 41, 26, n["cut"])
        rows = fit_rows(VGroup(
            label(rf"Old Faithful: \ two-means splits at {f['cut']:.2f} min: \ {f['n'][0]} and {f['n'][1]} eruptions", font_size=24, color=GREY_A),
            label(rf"naive $p = {f['naive']:.0e}$; \ selective $p = {f['selective']:.0e}$: \ working Gaussian model", font_size=24, color=HYBC),
            label(rf"Newcomb: \ splits at {n['cut']:.1f}: \ {n['n'][0]} and {n['n'][1]} measurements", font_size=24, color=GREY_A),
            label(rf"naive $p = {n['naive']:.0e}$; \ selective $p = {n['selective']:.2f}$: \ working Gaussian model", font_size=24, color=NAIVEC),
        ), 12.4, 0.3, [0, -2.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Two real data sets in one dimension, each split by two-means. Old Faithful's eruptions split at {say(f['cut'], 2)} minutes into {f['n'][0]} short and {f['n'][1]} long ones. <bookmark mark='b'/> The naive test's P-value is astronomically small, and so is this working-model selective value, consistent with the visible separation. These historical data are not verified Gaussian observations with known variance. <bookmark mark='c'/> Newcomb's passage times, without the two outliers, are one population of repeated measurements, but two-means still splits them, at {say(n['cut'], 1)}. <bookmark mark='d'/> The naive test calls the split hugely significant. The selective test gives a P-value of {say(n['selective'], 2)}: the algorithm alone can create a striking naive comparison. In both historical examples sigma is the overall sample standard deviation, which is not a certified upper bound. These are approximate illustrations; removing Newcomb outliers also changes the analysis."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(museum_tag(r"Old Faithful; \ Newcomb (1891)")))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in hf], lag_ratio=0.03), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in hn], lag_ratio=0.03), FadeIn(rows[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def null_hist(self):
        d = load("cluster")["null"]
        s = np.asarray(d["selective"])
        nv = np.asarray(d["naive"])
        bins = np.linspace(0, 1, 11)
        h, _ = np.histogram(s, bins)
        A = axes([0, 1], [0, max(1.6 * len(s) / 10, max(h) * 1.1)], x_length=7.4, y_length=4.4, xlabel=r"$p$-value", ylabel=r"count",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 100, 200], center=[-2.5, 0.2, 0])
        ax = A.ax
        bars = VGroup(*[Rectangle(width=ax.c2p(b1, 0)[0] - ax.c2p(b0, 0)[0] - 0.04, height=ax.c2p(0, c)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                  fill_color=CONDC, fill_opacity=0.8).move_to([(ax.c2p(b0, 0)[0] + ax.c2p(b1, 0)[0]) / 2, (ax.c2p(0, 0)[1] + ax.c2p(0, c)[1]) / 2, 0])
                        for b0, b1, c in zip(bins[:-1], bins[1:], h)])
        flat = DashedLine(ax.c2p(0, len(s) / 10), ax.c2p(1, len(s) / 10), color=WHITE, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"{len(s):,} samples of 40 from one normal: \ no clusters", font_size=22),
            label(rf"blue: \ selective $p$-values: \ flat; \ {100 * np.mean(s < 0.05):.1f}\% below 0.05", font_size=22, color=CONDC),
            label(rf"naive $p$-values below 0.05: \ {100 * np.mean(nv < 0.05):.0f}\%", font_size=22, color=NAIVEC),
            label(r"conditioning on the clustering restores the null", font_size=22, color=HYBC),
        ), 4.6, 0.4, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The check. {len(s):,} samples of forty from a single normal, so there are no clusters at all. <bookmark mark='b'/> With independent Gaussian data and known sigma one, these exact pivots should be uniform. A conservative valid p-value need only be superuniform. Here {100 * np.mean(s < 0.05):.1f} percent fall below five percent. <bookmark mark='c'/> The naive P-values fall below five percent {100 * np.mean(nv < 0.05):.0f} percent of the time. <bookmark mark='d'/> Conditioning on the clustering restores the null."
        ) as vo:
            self.play(FadeIn(A), FadeIn(flat), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def why_works(self):
        rows = [
            cmath(r"\text{condition on}", r":", r"\text{the partition, \ contrast direction, \ and data orthogonal to }\nu", font_size=34),
            cmath(r"\text{then}", r":", r"\text{the only randomness left is the size of the difference}", font_size=34),
            cmath(r"\text{under } H_0", r":", r"\text{that size is } \sigma\|\nu\|\chi_1, \ \text{truncated to } S", font_size=34),
            cmath(r"\text{so}", r":", r"\text{exact: \ the polyhedral lemma's idea}", font_size=32),
        ]
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"the nuisance part"), why(r"one dimension"), why(r"Gaussian data, \ known $\sigma$"), why(r"chapter 3, \ again")]
        head = label('Why works', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Why is it exact? The test conditions on the clustering and on every feature of the "
            "data that is orthogonal to the contrast nu. <bookmark mark='b'/> What remains random is only the size of "
            "the difference between the two clusters. <bookmark mark='c'/> Under the null, for Gaussian data with "
            "known sigma, that size is sigma times the norm of nu times a chi variable, truncated to the set S where "
            "the clustering would not change. <bookmark mark='d'/> So the P-value is exact, and the argument is "
            "chapter three's: condition on everything except one direction, and work out the law along it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def extensions(self):
        rows = [
            cmath(r"\sigma \text{ unknown}", r":", r"\text{a fixed known upper bound is conservative}", font_size=32),
            cmath(r"\text{many clusters}", r":", r"\text{test each pair; \ multiplicity, \ again}", font_size=34),
            cmath(r"\text{other problems}", r":", r"\text{changepoints, \ PCA, \ trees}", font_size=32),
            cmath(r"\text{or}", r":", r"\text{thin first: \ cluster on one part, \ test on the other}", font_size=32),
        ]
        rows[3][-1].set_color(SPLITC)
        whys = [why(r"sample SD is not a certified upper bound"), why(r"Part 33"), why(r"the same perturbation idea"), why(r"for count data")]
        head = label('Extensions', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> Some practicalities. A fixed known upper bound on sigma is conservative in this truncated chi model. The sample standard deviation is not such a bound. An estimated upper bound needs its own error budget or a justified conditional argument. <bookmark mark='b'/> With many clusters, every pair can be tested, and the multiplicity of Part thirty-three returns. <bookmark mark='c'/> The same perturbation idea gives selective tests after detecting changepoints, after principal components, and after fitting trees. <bookmark mark='d'/> And for count data such as gene expression, chapter five's thinning gives a simpler route: cluster on one thinned copy, test on the other."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
