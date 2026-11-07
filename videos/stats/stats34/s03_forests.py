from __future__ import annotations

import math

import numpy as np

from videos.stats.stats34.common import *  # noqa: F403

MTRY_C = {"10": GREY_B, "5": TREEC, "3": PREDC, "1": BOOSTC}


class Forests(VoiceoverScene):
    def construct(self):
        self.card()
        self.bagging()
        self.var_ladder()
        self.var_chart()
        self.mtry_table()
        self.cancer()
        self.oob()
        self.consistency()
        self.importance()
        self.ij_ladder()
        self.ij_result()
        self.ij_sub()
        self.board()

    def card(self):
        card = chapter_card(2, r"Forests", r"An average of many noisy trees", lit=(2001,), part=PART)
        with self.voiceover("Chapter two. Forests."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def bagging(self):
        rows = [
            cmath(r"\text{one tree } t(x)", r":", r"\text{low bias, \ high variance}", font_size=32),
            cmath(r"\text{bagging}", r":", r"\hat f(x) = \tfrac1B \textstyle\sum_{b=1}^B t_b(x), \ t_b \text{ on a bootstrap sample}", font_size=28),
            cmath(r"\text{random forest}", r":", r"\text{each split looks at only } m_{\rm try} \text{ of the } p \text{ features}", font_size=28),
            cmath(r"\text{default}", r":", r"m_{\rm try} = \sqrt p \ \text{(classes)}, \ \ p/3 \ \text{(regression)}", font_size=30),
        ]
        rows[2][-1].set_color(TREEC)
        whys = [why(r"Part 19's CART, \ grown deep"), why(r"Breiman (1996)"), why(r"Breiman (2001); \ Ho (1995); \ Amit \& Geman (1997)"),
                why(r"Breiman's recommendations")]
        with self.voiceover(
            "<bookmark mark='a'/> A decision tree grown deep, as in Part 19, has little bias, since it can follow "
            "almost any shape, and enormous variance: change a few training cases and the tree changes completely. "
            "<bookmark mark='b'/> In 1996 Breiman proposed bootstrap aggregation, bagging: grow a tree on each of B "
            "bootstrap samples and average their predictions. <bookmark mark='c'/> In 2001 he added one more twist, "
            "building on ideas of Tin Kam Ho and of Yali Amit and Donald Geman: at every split, let each tree "
            "consider only a random subset of m try features. That is a random forest. <bookmark mark='d'/> His "
            "defaults, the square root of p for classification and a third of p for regression, are historical "
            "recommendations; software defaults and useful tuning choices vary. Why would deliberately hobbling each "
            "tree make the average better?"
        ) as vo:
            intro=label('Bagging averages resampled trees; forests also randomize features',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def var_ladder(self):
        rows = [
            cmath(r"\mathrm{Var}\,t_b(x)", r"=", r"\sigma^2, \ \ \mathrm{Corr}(t_b, t_{b'}) = \rho", font_size=32),
            cmath(r"\mathrm{Var}\Big(\tfrac1B\textstyle\sum_b t_b\Big)", r"=", r"\tfrac{1}{B^2}\big(B\sigma^2 + B(B-1)\rho\sigma^2\big)", font_size=30),
            cmath(r"", r"=", r"\rho\,\sigma^2 + \dfrac{1 - \rho}{B}\,\sigma^2", font_size=34),
            cmath(r"B \to \infty", r":", r"\rho\,\sigma^2: \ \text{only decorrelation helps}", font_size=32),
        ]
        rows[2][-1].set_color(TREEC)
        whys = [why(r"identically distributed trees"), why(r"$B$ variances, \ $B(B-1)$ covariances"),
                why(r"Hastie, \ Tibshirani \& Friedman, \ (15.1)"), why(r"the floor is $\rho\sigma^2$")]
        with self.voiceover(
            "<bookmark mark='a'/> Here is the reason. Over the randomness of the training set and of the trees "
            "themselves, each tree's prediction at x has some variance sigma squared, and two trees of the same forest "
            "have some correlation rho, since they were grown on overlapping samples of the same data. <bookmark mark='b'/> "
            "The variance of their average has B variance terms and B times B minus one covariances. <bookmark mark='c'/> "
            "It simplifies to rho sigma squared, plus one minus rho over B times sigma squared. <bookmark mark='d'/> The "
            "second term vanishes as the forest grows. The first does not: however many trees you average, the variance "
            "never falls below rho sigma squared. Bagging can only shrink the second term. Restricting the features at "
            "each split shrinks rho, at the price of making each tree a little worse."
        ) as vo:
            intro=label('Correlated trees leave a variance floor as the forest grows',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def var_chart(self):
        d = load("variance")
        Bg = np.log10(np.asarray(d["Bgrid"], float))
        A = axes([0, 2.7], [0, max(max(v) for v in d["curves"].values())*1.05], x_length=7.2, y_length=4.4, xlabel=r"trees $B$", ylabel=r"Var of the forest",
                 xticks=[0, 1, 2], yticks=[0, 5, 10, 15], xfmt=lambda v: rf"{10 ** v:.0f}", center=[-2.0, 0.2, 0])
        ax = A.ax
        cs = {k: polyline(ax, Bg, np.asarray(v), MTRY_C[k], 3.5) for k, v in d["curves"].items()}
        floors = {k: DashedLine(ax.c2p(0, v["rho"] * v["sigma2"]), ax.c2p(2.7, v["rho"] * v["sigma2"]),
                                color=MTRY_C[k], stroke_width=1.5) for k, v in d["by_mtry"].items()}
        bm = d["by_mtry"]
        side = fit_rows(VGroup(
            label(r"Friedman 1: \ $n = 300$, \ $p = 10$", font_size=22),
            label(rf"bagging ($m_{{\rm try}} = 10$): \ $\rho = {bm['10']['rho']:.2f}$", font_size=22, color=MTRY_C["10"]),
            label(rf"$m_{{\rm try}} = 3$: \ $\rho = {bm['3']['rho']:.2f}$", font_size=22, color=MTRY_C["3"]),
            label(rf"$m_{{\rm try}} = 1$: \ $\rho = {bm['1']['rho']:.2f}$", font_size=22, color=MTRY_C["1"]),
            label(r"dashed: \ the floor $\rho\sigma^2$", font_size=20, color=GREY_A),
        ), 4.2, 0.4, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> We can measure both quantities. Jerome Friedman's 1991 test function has ten inputs, "
            "five of which matter, through a sine of a product, a square, and two straight lines. Forty training sets of "
            "three hundred points, a forest of forty trees on each, and the predictions at two hundred test points give "
            "sigma squared and rho directly. <bookmark mark='b'/> For bagging, with all ten features at every split, two "
            "trees are correlated at " + say(bm['10']['rho']) + ". <bookmark mark='c'/> With "
            "three features per split, rho falls to " + say(bm['3']['rho']) + ", <bookmark "
            "mark='d'/> and with a single random feature per split, to " + say(bm['1']['rho'])
            + ". <bookmark mark='e'/> Each curve falls with B towards its own dashed floor, rho sigma squared, and "
            "after a hundred trees the remaining Monte Carlo term depends on rho and the tree count; adding trees can"
            " still help."
        ) as vo:
            self.add(friedman_tag())
            self.play(FadeIn(A), FadeIn(side[0]))
            for m_, k, r in (("b", "10", 1), ("c", "3", 2), ("d", "1", 3)):
                vo.wait_until(m_)
                self.play(Create(cs[k]), FadeIn(side[r]))
            vo.wait_until("e")
            self.play(*[Create(f) for f in floors.values()], Create(cs["5"]), FadeIn(side[4]))
        self.clear_scene()

    def mtry_table(self):
        d = load("variance")
        bm = d["by_mtry"]
        rows = [[r"$m_{\rm try}$", r"$\sigma^2$ (one tree)", r"$\rho$", r"Var (forest)", r"bias$^2$", r"MSE"]]
        for k in ("10", "5", "3", "1"):
            v = bm[k]
            rows.append([k, rf"{v['sigma2']:.2f}", rf"{v['rho']:.2f}", rf"{v['forest_var']:.2f}", rf"{v['bias2']:.2f}",
                         rf"{v['mse']:.2f}"])
        tab = table_rows(rows, font_size=26, col_buff=0.55, row_buff=0.28,
                         colors=[GREY_A, MTRY_C["10"], MTRY_C["5"], MTRY_C["3"], MTRY_C["1"]]).move_to([0, 1.0, 0])
        best = min(("10", "5", "3", "1"), key=lambda k: bm[k]["mse"])
        foot = fit_rows(VGroup(
            label(r"fewer features per split: \ each tree noisier and more biased, \ but far less correlated", font_size=24),
            label(rf"the best mean squared error here: \ $m_{{\rm try}} = {best}$", font_size=24, color=TREEC),
            label(r"the forest's error is a bias--variance sum like any estimator's", font_size=24, color=CALC),
        ), 12.4, 0.4, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The whole trade in one table. As m try falls from ten to one, a single tree gets "
            "noisier, sigma squared rises, and the bias of the forest rises, because a tree that must sometimes split on "
            "an irrelevant feature wastes its depth. But rho falls much faster, so the forest's variance falls. <bookmark "
            "mark='b'/> The mean squared error is smallest at m try equals " + best + " here. <bookmark mark='c'/> "
            "Nothing magical: the forest is an estimator of the regression function, and its error is a bias plus a "
            "variance, like every estimator in this series. m try is the knob that trades one for the other."
        ) as vo:
            self.add(friedman_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def cancer(self):
        d = load("forest")
        Bs = np.log10(np.asarray(d["Bs"], float))
        A = axes([0, 2.6], [0, max(max(d["err_bag"]),max(d["err_rf"]),1-d["acc_tree"])*1.1], x_length=7.2, y_length=4.4, xlabel=r"trees $B$", ylabel=r"test error",
                 xticks=[0, 1, 2], yticks=[0, 0.05, 0.1], xfmt=lambda v: rf"{10 ** v:.0f}", yfmt=lambda v: rf"{100 * v:.0f}\%",
                 center=[-2.0, 0.2, 0])
        ax = A.ax
        cb = polyline(ax, Bs, d["err_bag"], GREY_B, 3)
        cr = polyline(ax, Bs, d["err_rf"], TREEC, 3.5)
        tree = DashedLine(ax.c2p(0, 1 - d["acc_tree"]), ax.c2p(2.6, 1 - d["acc_tree"]), color=MISSC, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"one deep tree: \ {100 * (1 - d['acc_tree']):.1f}\% wrong", font_size=22, color=MISSC),
            label(rf"bagging, \ 300 trees: \ {100 * (1 - d['acc_bag']):.1f}\%", font_size=22, color=GREY_B),
            label(rf"forest, \ $m_{{\rm try}} = {d['mtry']}$: \ {100 * (1 - d['acc_rf']):.1f}\%", font_size=22, color=TREEC),
            label(r"169 test cases: \ one case is 0.6\%", font_size=20, color=GREY_A),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Back to the biopsies, with two columns of pure noise added to the thirty features, for "
            "later. One deep tree misclassifies seven percent of the hundred and sixty-nine test cases. <bookmark "
            "mark='b'/> Bagging three hundred trees brings that down to six percent, <bookmark mark='c'/> and the forest, "
            "with six features per split, also to six. The curves wander a little with B, mostly because each test case is "
            "six tenths of a percent. <bookmark mark='d'/> On a problem this easy every reasonable method is close; on "
            "harder ones, like Friedman's, the forest's advantage over bagging is larger."
        ) as vo:
            self.add(bc_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(tree), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cr), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def oob(self):
        d = load("forest")
        rows = [
            cmath(r"P(i \notin \text{bootstrap sample})", r"=", r"(1 - 1/n)^n \to e^{-1} \approx 0.368", font_size=30),
            cmath(r"\hat f_{\rm OOB}(x_i)", r"=", r"\text{average of the trees that never saw } i", font_size=30),
            cmath(r"\text{OOB error}", r"=", rf"{100 * d['oob_err']:.1f}\% \ \text{{(test: {100 * d['test_err']:.1f}\%)}}", font_size=32),
            cmath(r"\text{cost}", r":", r"\text{none: \ a free cross-validation}", font_size=32),
        ]
        rows[2][-1].set_color(TREEC)
        whys = [why(r"Part 16"), why(r"about $B/e$ trees each"), why(r"on the 400 training cases"), why(r"Breiman (1996b)")]
        with self.voiceover(
            "<bookmark mark='a'/> Bagging comes with its own test set. A given case is left out of a bootstrap sample "
            "with probability one minus one over n, to the n, which tends to one over e, about thirty-seven percent. "
            "<bookmark mark='b'/> So each training case has about a third of the trees that never saw it, and their "
            "average is an honest, out-of-bag prediction for it. <bookmark mark='c'/> The out-of-bag error on the four "
            "hundred training cases is three and a half percent, against six on the separate test set: the same "
            "order, as two noisy estimates of one error rate should be. <bookmark mark='d'/> It costs nothing: a "
            "cross-validation that comes free with the forest."
        ) as vo:
            intro=label('Out-of-bag predictions exclude the case being evaluated',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def consistency(self):
        rows = fit_rows(VGroup(
            label(r"is a forest consistent? \ Breiman's own algorithm resisted proof for years", font_size=26),
            label(r"simplified forests: \ Biau, \ Devroye \& Lugosi (2008); \ Biau (2012)", font_size=26, color=GREY_A),
            label(r"Breiman's forests, \ additive regression: \ Scornet, \ Biau \& Vert (2015)", font_size=26, color=TREEC),
            label(r"`honest' trees are asymptotically normal: \ Wager \& Athey (2018)", font_size=26, color=PREDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Is the forest a consistent estimator of the regression function? For Breiman's own "
            "algorithm, with its bootstrap, its data-dependent splits and its fully grown trees, the question resisted "
            "proof for years. <bookmark mark='b'/> Gérard Biau, Luc Devroye and Gábor Lugosi proved consistency in 2008 "
            "for simplified forests whose splits ignore the responses, and Biau extended it in 2012. <bookmark mark='c'/> "
            "In 2015 Erwan Scornet, Biau and Jean-Philippe Vert proved that Breiman's forests, with subsampling instead "
            "of the bootstrap, are consistent when the regression function is additive. <bookmark mark='d'/> And Stefan "
            "Wager and Susan Athey showed in 2018 that forests of honest trees, which use one half of each subsample to "
            "choose the splits and the other half to fill the leaves, are asymptotically normal. That opens the door to "
            "confidence intervals."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def importance(self):
        d = load("forest")
        top = [int(i) for i in d["top"][:6]]
        idx = top + [d["p"] - 2, d["p"] - 1]
        imp = np.asarray(d["imp"])[idx]
        pim = np.asarray(d["perm"])[idx]
        names = [d["names"][i].replace("_", " ") for i in idx]
        names[-2], names[-1] = r"noise (continuous)", r"noise (coin)"
        A = axes([0, 8], [min(0,float(pim.min()/pim.max()))*1.1, 1.05], x_length=8.0, y_length=4.0, xlabel=r"", ylabel=r"share of the largest",
                 xticks=[], yticks=[0, 0.5, 1], center=[-1.6, 0.4, 0])
        ax = A.ax
        bi = bars_at(ax, np.arange(8) + 0.32, imp / imp.max(), 0.34, TREEC)
        bp = bars_at(ax, np.arange(8) + 0.68, pim / pim.max(), 0.34, CALC)
        labs = VGroup(*[label(n, font_size=15, color=MISSC if i >= 6 else GREY_A).rotate(PI / 6)
                        .next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.35) for i, n in enumerate(names)])
        ratio = d["noise_imp"][0] / max(d["noise_imp"][1], 1e-9)
        side = fit_rows(VGroup(
            label(r"green: \ impurity (Gini) importance", font_size=20, color=TREEC),
            label(r"gold: \ permutation importance", font_size=20, color=CALC),
            label(rf"pure noise: \ continuous gets {ratio:.0f}$\times$ the coin", font_size=20, color=MISSC),
            label(r"permutation: \ both $\approx 0$", font_size=20, color=CALC),
        ), 3.6, 0.4, [5.1, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Forests also report which features matter, in two ways. Breiman's impurity importance "
            "adds up, for each feature, how much its splits reduced the training error, across all the trees. <bookmark "
            "mark='b'/> His permutation importance instead scrambles one feature in held-out data and measures how much "
            "the error grows. For the real features they broadly agree. <bookmark mark='c'/> Now look at the two noise "
            "columns we added, one continuous and one a coin flip. Neither carries any information. Impurity importance "
            "credits the continuous one with " + f"{ratio:.0f}" + " times the coin's importance, because a feature with many "
            "distinct values offers many more chances to find a split that happens to fit the training data. Carolin "
            "Strobl and her colleagues documented this bias in 2007. <bookmark mark='d'/> Permutation importance, "
            "measured on data the trees did not see, gives both noise columns essentially zero."
        ) as vo:
            self.add(bc_tag())
            self.play(FadeIn(A), FadeIn(labs))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bi], lag_ratio=0.1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bp], lag_ratio=0.1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Indicate(bi[6], color=MISSC), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def ij_ladder(self):
        rows = [
            cmath(r"N_{bi}", r"=", r"\text{times case } i \text{ is in tree } b\text{'s sample}", font_size=30),
            cmath(r"\hat V_{IJ}(x)", r"=", r"\textstyle\sum_{i=1}^n \mathrm{Cov}_b\big(N_{bi}, \, t_b(x)\big)^2", font_size=32),
            cmath(r"\text{bias correction}", r":", r"- \tfrac{n}{B^2} \textstyle\sum_b \big(t_b(x) - \hat f(x)\big)^2", font_size=30),
            cmath(r"\text{interval}", r":", r"\hat f(x) \pm 1.645 \sqrt{\hat V_{IJ}(x)}", font_size=32),
        ]
        rows[1][-1].set_color(TREEC)
        whys = [why(r"recorded while growing"), why(r"Efron (2014): \ the infinitesimal jackknife"),
                why(r"Monte Carlo noise of finite $B$"), why(r"Wager, \ Hastie \& Efron (2014)")]
        with self.voiceover(
            "<bookmark mark='a'/> How uncertain is a forest's prediction? Record, while growing the forest, how many times "
            "each training case appears in each tree's bootstrap sample. <bookmark mark='b'/> Efron's infinitesimal "
            "jackknife asks how the prediction would move if case i got a little more weight; for a bagged estimator that "
            "derivative is the covariance, across trees, between case i's count and the tree's prediction. Summing the "
            "squares over cases estimates the variance. <bookmark mark='c'/> With finitely many trees this is biased "
            "upwards by Monte Carlo noise, and Stefan Wager, Trevor Hastie and Efron subtract a correction. <bookmark "
            "mark='d'/> Then an interval is the prediction plus or minus one point six four five standard errors, for "
            "ninety percent. One forest, no refitting."
        ) as vo:
            intro=label('The infinitesimal jackknife approximates sampling variance',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ij_chart(self, d, lo_y, hi_y):
        first = d["first"][:20]
        A = axes([0, 21], [lo_y, hi_y], x_length=7.4, y_length=4.4, xlabel=r"training set", ylabel=r"$\hat f(x_0)$",
                 xticks=[1, 10, 20], yticks=[lo_y, round(d["Ef"]), round(d["mu0"])], center=[-2.0, 0.2, 0])
        ax = A.ax
        bars = VGroup()
        for k, f in enumerate(first):
            lo, hi = f["pred"] - 1.645 * f["se"], f["pred"] + 1.645 * f["se"]
            ok = lo <= d["Ef"] <= hi
            bars.add(VGroup(Line(ax.c2p(k + 1, max(lo, lo_y)), ax.c2p(k + 1, min(hi, hi_y)), color=BANDC if ok else MISSC, stroke_width=4),
                            Dot(ax.c2p(k + 1, f["pred"]), radius=0.05, color=WHITE)))
        ef = DashedLine(ax.c2p(0, d["Ef"]), ax.c2p(21, d["Ef"]), color=TREEC, stroke_width=2.5)
        mu = DashedLine(ax.c2p(0, d["mu0"]), ax.c2p(21, d["mu0"]), color=TRUEC, stroke_width=2.5)
        return A, bars, ef, mu

    def ij_result(self):
        d = load("ij")
        A, bars, ef, mu = self.ij_chart(d, 17, 24)
        side = fit_rows(VGroup(
            label(r"a peak of Friedman's surface", font_size=22),
            label(rf"truth $\mu(x_0) = {d['mu0']:.1f}$", font_size=22, color=TRUEC),
            label(rf"independent pilot mean $\mathrm{{E}}\hat f(x_0) = {d['Ef']:.1f}$", font_size=22, color=TREEC),
            label(rf"covers pilot mean: \ only {100 * d['cov_E']:.0f}\%", font_size=22, color=MISSC),
            label(rf"mean SE {d['mean_se']:.2f}; \ sampling SD estimate {d['sd_pred']:.2f}", font_size=22, color=CALC),
        ), 4.2, 0.4, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Try it at a point x nought near a peak of Friedman's surface. Three hundred training sets "
            "of two hundred and fifty points, a forest of five hundred trees on each, and an infinitesimal jackknife "
            "interval from each forest. Here are the first twenty. <bookmark mark='b'/> The true value of the regression "
            "function there is " + say(d["mu0"], 1) + ". <bookmark mark='c'/> The forests, averaged over training sets, "
            "reach only " + say(d["Ef"], 1) + ": averaging over leaves pulls peaks down and valleys up. <bookmark "
            "mark='d'/> Worse, the intervals do not even cover the forests' own average at the promised rate: only "
            + f"{100 * d['cov_E']:.0f}" + " percent. <bookmark mark='e'/> Their standard errors average " + say(d["mean_se"])
            + ", but the forests' predictions really vary with a standard deviation of " + say(d["sd_pred"]) + ". The "
            "infinitesimal jackknife captures only the linear part of an estimator's variability, and a deep tree grown "
            "on a bootstrap sample of the whole data set does not ensure an accurate linear approximation at this sample size."
        ) as vo:
            self.add(friedman_tag())
            self.play(FadeIn(A), FadeIn(side[0]), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.1), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(mu), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ef), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def ij_sub(self):
        d = load("ij_sub")
        A, bars, ef, mu = self.ij_chart(d, 15, 24)
        side = fit_rows(VGroup(
            label(rf"each tree: \ {d['s']} of the 250 points, \ no replacement", font_size=22),
            label(rf"{d['B']:,} trees; \ the subsampling IJ", font_size=22, color=TREEC),
            label(rf"covers pilot mean: \ {100 * d['cov_E']:.0f}\%", font_size=22, color=BANDC),
            label(rf"but $\mathrm{{E}}\hat f = {d['Ef']:.1f}$: \ covers $\mu$ {100 * d['cov_mu']:.0f}\%", font_size=22, color=MISSC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Wager and Athey's remedy is to grow each tree on a small subsample drawn without "
            "replacement, here fifty of the two hundred and fifty points. Subsampling alone does not establish the "
            "honest-forest asymptotic theorem. Then each tree depends on any one case only rarely, the forest becomes"
            " nearly linear in the data, like a U-statistic, and the infinitesimal jackknife, with the subsampling "
            "correction, captures most of its variance. <bookmark mark='b'/> With two thousand trees per forest, "
            "<bookmark mark='c'/> the intervals now cover the forests' own average "
            + f"{100 * d['cov_E']:.0f}" + " percent of the time: far better, though still short of ninety, because the "
            "standard errors remain about a tenth too small on average, and are themselves noisy. <bookmark mark='d'/> But trees on fifty points are "
            "coarser, so the forests are more biased, averaging " + say(d["Ef"], 1) + " against the true "
            + say(d["mu0"], 1) + ", and the intervals almost never cover the truth. Honest variance, dishonest centre: the "
            "infinitesimal jackknife measures variance, not bias. Wager and Athey's asymptotic theory makes the bias "
            "negligible under conditions on honest tree construction, regularity and the subsampling rate. These ordinary CART trees are not an implementation of their honest forest theorem."
        ) as vo:
            self.add(friedman_tag())
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.1), FadeIn(side[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(ef), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(mu), FadeIn(side[3]))
        self.clear_scene()

    def board(self):
        rows = board_rows("forest IJ")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board. The infinitesimal jackknife interval of a bootstrap forest, for the "
                   "forest's own expectation: broken, far too narrow. <bookmark mark='b'/> For a subsampled forest: much "
                   "closer, but with three hundred forests the Board can tell that eighty-three is not ninety. <bookmark mark='c'/> And the same subsampled interval as an interval for the true "
                   "regression function at a peak: broken, by the bias. Every estimator needs to be told what it is "
                   "estimating, and a forest is no exception.",
                   [("a", [0]), ("b", [1]), ("c", [2])])
