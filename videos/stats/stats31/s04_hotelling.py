from __future__ import annotations

import numpy as np

from videos.stats.stats31.common import *  # noqa: F403


class Hotelling(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.ui()
        self.iris_test()
        self.projection()
        self.ellipsoid()
        self.manova_def()
        self.four()
        self.which()

    def card(self):
        card = chapter_card(3, r"Hotelling's $T^2$ and MANOVA", r"Testing mean vectors", lit=(1931,), part=PART)
        with self.voiceover("Chapter three. Hotelling's T squared and MANOVA."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"H_0", r":", r"\mu_1 = \mu_2 \ \text{in all } p \text{ coordinates}", font_size=30),
            cmath(r"p \ t\text{-tests}", r":", r"\text{multiple testing, \ and blind to correlation}", font_size=30),
            cmath(r"\text{Bonferroni}", r":", r"\text{valid, \ but ignores how variables combine}", font_size=30),
            cmath(r"\text{goal}", r":", r"\text{one test, \ using } S^{-1}", font_size=30),
        ]
        rows[3][2].set_color(PCC)
        whys = [why(r"two species, \ four measurements"), why(r"Part 33's problem"), why(r"conservative"),
                why(r"Hotelling (1931)")]
        with self.voiceover(
            "<bookmark mark='a'/> Do two species differ in their mean measurements? The null hypothesis is a vector: equal "
            "means in all p coordinates. <bookmark mark='b'/> Running p separate t-tests raises Part 33's multiple-testing "
            "problem, and ignores the correlations between the variables. <bookmark mark='c'/> Bonferroni's correction is "
            "valid, but still ignores how variables combine. <bookmark mark='d'/> Harold Hotelling's 1931 answer is a single "
            "test that uses the inverse covariance."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ui(self):
        rows = [
            cmath(r"t^2(a)", r"=", r"\dfrac{n_1 n_2}{n_1 + n_2} \dfrac{(a^\top (\bar x_1 - \bar x_2))^2}{a^\top S a}", font_size=28),
            cmath(r"\max_a t^2(a)", r"=", r"\dfrac{n_1 n_2}{n_1 + n_2} (\bar x_1 - \bar x_2)^\top S^{-1} (\bar x_1 - \bar x_2) = T^2", font_size=26),
            cmath(r"\text{best } a", r"\propto", r"S^{-1} (\bar x_1 - \bar x_2)", font_size=30),
            cmath(r"\text{reject}", r":", r"\text{if any combination's } t^2 \text{ is too big}", font_size=30),
        ]
        rows[1][2].set_color(PCC)
        whys = [why(r"the $t$-test of one linear combination"), why(r"Cauchy--Schwarz in the $S$ metric"),
                why(r"Fisher's discriminant, \ chapter seven"), why(r"Roy's union--intersection principle (1953)")]
        with self.voiceover(
            "<bookmark mark='a'/> The cleanest derivation is S. N. Roy's union–intersection principle. For any linear "
            "combination of the variables there is an ordinary two-sample t statistic. <bookmark mark='b'/> Maximize its "
            "square over all combinations: by Cauchy–Schwarz in the metric of S, the maximum is T squared. "
            "<bookmark mark='c'/> The maximizing combination is S inverse times the difference in means, which chapter seven "
            "will meet as Fisher's discriminant. <bookmark mark='d'/> So T squared rejects exactly when some linear "
            "combination of the variables shows a significant difference, with the threshold chosen to account for the "
            "search."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def iris_test(self):
        d = load("hotelling")
        hdr = [r"\textbf{versicolor vs virginica}", r"\textbf{$t$}", r"\textbf{$t^2$}"]
        nm = ["sepal length", "sepal width", "petal length", "petal width"]
        body = [[nm[j], f"{d['t_uni'][j]:.2f}", f"{d['t_uni'][j] ** 2:.1f}"] for j in range(4)]
        body.append([r"the best combination", f"{d['tmax']:.2f}", f"{d['tmax'] ** 2:.1f}"])
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.0, row_buff=0.3, colors=[GREY_A] + [None] * 4 + [PCC])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"$T^2 = {d['T2']:.1f}$, \ $F = {d['F']:.1f}$ on ({d['df'][0]}, {d['df'][1]}) df, \ $p = 10^{{{int(np.floor(np.log10(d['p'])))}}}$", font_size=22, color=PCC),
            label(r"the best combination's $t^2$ is $T^2$ itself: \ far beyond any single measurement", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Versicolor against virginica, fifty flowers each. The four separate t statistics run from "
            "minus three to minus fourteen and a half in size: petal width alone gives t squared of two hundred and fourteen. "
            "<bookmark mark='b'/> The best linear combination gives t squared of three hundred and fifty-five: that is T "
            "squared. Converted to F with four and ninety-five degrees of freedom, eighty-six, a p-value of ten to the minus "
            "thirty. The combination separates the species far better than any single measurement."
        ) as vo:
            self.add(iris_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r) for r in tb[1:5]], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(tb[5]), FadeIn(foot[0]), FadeIn(foot[1]))
        self.clear_scene()

    def projection(self):
        d = load("hotelling")
        pv, pg = np.asarray(d["proj"]["versicolor"]), np.asarray(d["proj"]["virginica"])
        lo, hi = float(min(pv.min(), pg.min())) - 0.2, float(max(pv.max(), pg.max())) + 0.2
        A = axes([lo, hi], [0, 16], x_length=8.4, y_length=4.2, xlabel=r"the best combination $a^\top x$", ylabel=r"count",
                 xticks=[], yticks=[0, 5, 10, 15], center=[-1.6, 0.3, 0])
        ax = A.ax
        edges = np.linspace(lo, hi, 31)
        b1 = hist_bars(ax, edges, np.histogram(pv, edges)[0], color=SP[1], opacity=0.65)
        b2 = hist_bars(ax, edges, np.histogram(pg, edges)[0], color=SP[2], opacity=0.65)
        a = np.asarray(d["direction"])
        rows = fit_rows(VGroup(
            label(r"green: \ versicolor; \ purple: \ virginica", font_size=22),
            label(rf"$a$: \ ({a[0]:.2f}, {a[1]:.2f}, {a[2]:.2f}, {a[3]:.2f})", font_size=22, color=PCC),
            label(r"opposite signs: \ petals against sepals", font_size=22, color=GREY_A),
        ), 3.6, 0.42, [5.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Project every flower onto that best combination. The two species barely overlap. "
            "<bookmark mark='b'/> The weights have one sign on the two sepal measurements and the opposite sign on the two "
            "petal measurements; the overall sign is arbitrary. <bookmark mark='c'/> So the combination asks: how big are the "
            "petals relative to the sepals? Virginicas have big petals for their sepal size, something no single measurement "
            "expresses."
        ) as vo:
            self.add(iris_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in b1], lag_ratio=0.02),
                      LaggedStart(*[GrowFromEdge(x, DOWN) for x in b2], lag_ratio=0.02), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def manova_def(self):
        rows = [
            cmath(r"H", r"=", r"\textstyle\sum_g n_g (\bar x_g - \bar x)(\bar x_g - \bar x)^\top", font_size=30),
            cmath(r"E", r"=", r"\textstyle\sum_g \sum_{i \in g} (x_i - \bar x_g)(x_i - \bar x_g)^\top", font_size=30),
            cmath(r"\lambda_1 \ge \dots", r":", r"\text{eigenvalues of } E^{-1} H", font_size=30),
            cmath(r"\text{one number}", r"\leftarrow", r"\text{several eigenvalues: \ no unique best way}", font_size=28),
        ]
        rows[2][2].set_color(PCC)
        whys = [why(r"between groups"), why(r"within groups"), why(r"$F$-ratios along the best directions"),
                why(r"hence four statistics")]
        with self.voiceover(
            "<bookmark mark='a'/> With more than two groups, MANOVA generalizes analysis of variance. The between-group sum "
            "of squares becomes a matrix H, <bookmark mark='b'/> the within-group sum a matrix E. <bookmark mark='c'/> "
            "Their comparison lives in the eigenvalues of E inverse H: F-like ratios along a sequence of best directions. "
            "<bookmark mark='d'/> With three species and four variables there are two nonzero eigenvalues, and there is no "
            "unique best way to reduce two numbers to one test. Hence four classical statistics."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def four(self):
        d = load("hotelling")["manova"]
        ev = d["eigen"]
        hdr = [r"\textbf{statistic}", r"\textbf{from the eigenvalues}", r"\textbf{the irises}"]
        body = [[r"Wilks's $\Lambda$ (1932)", r"$\prod 1/(1 + \lambda_i)$", f"{d['wilks']:.4f}"],
                [r"Pillai's trace (1955)", r"$\sum \lambda_i/(1 + \lambda_i)$", f"{d['pillai']:.3f}"],
                [r"Hotelling--Lawley trace", r"$\sum \lambda_i$", f"{d['hotelling_lawley']:.2f}"],
                [r"Roy's largest root (1953)", r"$\lambda_1$", f"{d['roy']:.2f}"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.0, row_buff=0.32, colors=[GREY_A, PCC, PCC, PCC, PCC])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"eigenvalues {ev[0]:.2f} and {ev[1]:.2f}: \ one direction separates the species", font_size=22),
            label(rf"Wilks's $F = {d['wilks_F']:.0f}$ on ({d['wilks_df'][0]}, {d['wilks_df'][1]:.0f}) df; \ statkit matches statsmodels to every digit", font_size=22, color=PATH),
            label(r"Pillai: \ most robust; \ Roy: \ most powerful when one direction dominates", font_size=22, color=GREY_A),
        ), 12.0, 0.22, [0, -2.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The four, on all three iris species. Wilks's lambda, a product; Pillai's trace; the "
            "Hotelling–Lawley trace; Roy's largest root. The eigenvalues are thirty-two and point two nine: almost all the "
            "separation lies in one direction. <bookmark mark='b'/> Wilks's lambda is point oh two three, an F of a hundred "
            "and ninety-nine, and statkit reproduces statsmodels' four statistics to every printed digit. "
            "<bookmark mark='c'/> As for which to use: Pillai's trace is the most robust to unequal covariances; Roy's "
            "largest root is the most powerful when, as here, one direction dominates."
        ) as vo:
            self.add(iris_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.3), FadeIn(foot[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def which(self):
        rows = fit_rows(VGroup(
            label(r"$T^2$ and MANOVA assume equal covariance matrices", font_size=24),
            label(r"Box's $M$ test checks it, \ but is itself very sensitive to non-normality", font_size=24, color=RES),
            label(r"with $p$ near $n$, \ $S^{-1}$ is unstable: \ chapter ten", font_size=24, color=RES),
            label(r"follow up with the directions: \ which combination differs?", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Cautions. T squared and MANOVA assume the groups share one covariance matrix. "
            "<bookmark mark='b'/> George Box's M test checks that, but it is so sensitive to non-normality that its verdicts "
            "are hard to use. <bookmark mark='c'/> With many variables relative to observations, S inverse becomes unstable, "
            "chapter ten's subject. <bookmark mark='d'/> And a significant result invites the real question: which "
            "combination of variables differs? The eigenvectors answer it."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def ellipsoid(self):
        rows = [
            cmath(r"n (\bar x - \mu)^\top S^{-1} (\bar x - \mu)", r"\le", r"\tfrac{p(n - 1)}{n - p} F_{p, n-p; 0.95}", font_size=28),
            cmath(r"a^\top \mu", r"\in", r"a^\top \bar x \pm \sqrt{c \, a^\top S a / n}", font_size=30),
            cmath(r"P(\text{all } a \text{ at once})", r"=", r"0.95", font_size=32),
            cmath(r"\text{price}", r":", r"\text{wider than Bonferroni for a few chosen } a", font_size=28),
        ]
        rows[0][-1].set_color(PCC)
        whys = [why(r"a confidence ellipsoid"), why(r"intervals for every combination"), why(r"simultaneous, \ by union--intersection"), why(r"the cost of insuring every question")]
        with self.voiceover(
            "<bookmark mark='a'/> Inverting the test gives a confidence region: an ellipsoid around the sample mean, "
            "shaped by S. <bookmark mark='b'/> Projecting the ellipsoid onto any direction gives an interval for that "
            "linear combination of the means. <bookmark mark='c'/> And because the ellipsoid contains the truth with "
            "probability ninety-five percent, all of these intervals hold simultaneously, for every combination, even "
            "ones chosen after looking at the data. <bookmark mark='d'/> The price is width. If you only care about a "
            "few combinations chosen in advance, Bonferroni intervals are narrower; the ellipsoid insures against "
            "every question you might ask."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
