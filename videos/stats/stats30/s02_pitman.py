from __future__ import annotations

import numpy as np

from videos.stats.stats30.common import *  # noqa: F403


class Pitman(VoiceoverScene):
    def construct(self):
        self.card()
        self.upgrade()
        self.efficacy()
        self.sign()
        self.wilcoxon()
        self.table()
        self.bound()
        self.scores()
        self.estimators()

    def card(self):
        card = chapter_card(1, r"Pitman efficiency", r"How much do ranks cost?", lit=(1956,), part=PART)
        with self.voiceover("Chapter one. Pitman efficiency."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def upgrade(self):
        card = upgrade_card(16, r"the Wilcoxon test is 95.5\% as efficient as $t$ for normal data, \ and never below 86.4\%",
                            r"the numbers were quoted; \ where they come from was not shown",
                            r"derive Pitman's efficacy, \ the $3/\pi$, \ and the bound by the calculus of variations")
        with self.voiceover(
            "<bookmark mark='a'/> Part 16 quoted two numbers: the Wilcoxon test is ninety-five and a half percent as "
            "efficient as the t-test for normal data, and never less than eighty-six point four percent. "
            "<bookmark mark='b'/> It didn't show where they come from. <bookmark mark='c'/> Now we derive both."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card[0]), FadeIn(card[1][0]), FadeIn(card[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card[1][1][2]))
        self.clear_scene()

    def efficacy(self):
        rows = [
            cmath(r"H_n", r":", r"\theta_n = h/\sqrt n: \ \text{alternatives closing in}", font_size=30),
            cmath(r"T_n", r"\approx", r"N\bigl(\mu(\theta), \sigma^2(\theta)/n\bigr)", font_size=30),
            cmath(r"\text{efficacy}", r"=", r"\mu'(0)^2 / \sigma^2(0)", font_size=32),
            cmath(r"\text{ARE}(A : B)", r"=", r"\dfrac{\text{efficacy}_A}{\text{efficacy}_B} = \lim \dfrac{n_B}{n_A}", font_size=30),
        ]
        rows[3][2].set_color(HLC)
        whys = [why(r"Pitman (1948): \ hard, \ not hopeless, \ alternatives"), why(r"the test statistic's drift and noise"),
                why(r"signal squared over noise, \ per observation"), why(r"the sample-size ratio for equal power")]
        with self.voiceover(
            "<bookmark mark='a'/> Edwin Pitman's idea: compare tests on alternatives that close in on the null as n grows, at "
            "rate one over root n, so that power stays strictly between the level and one. <bookmark mark='b'/> Each test "
            "statistic is approximately normal, with a mean that drifts with theta and a variance over n. "
            "<bookmark mark='c'/> Its efficacy is the squared slope of the drift at zero over the variance: signal squared "
            "over noise, per observation. <bookmark mark='d'/> The ratio of efficacies is the limiting ratio of the sample "
            "sizes the two tests need for the same power."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def wilcoxon(self):
        rows = [
            cmath(r"t\text{-test}", r":", r"\mu(\theta) = \theta, \ \ \sigma^2 = \mathrm{Var}\,X: \ \ \text{efficacy } 1/\sigma^2", font_size=28),
            cmath(r"\text{Wilcoxon}", r":", r"\tfrac{1}{n^2}W \approx P(X_i + X_j > 0) = \textstyle\int F(x + 2\theta)\, dF \dots", font_size=26),
            cmath(r"\mu'(0)", r"=", r"2\textstyle\int f^2, \ \ \sigma^2(0) = \tfrac13: \ \ \text{efficacy } 12 \bigl(\int f^2\bigr)^2", font_size=28),
            cmath(r"\text{ARE}", r"=", r"12\, \sigma^2 \bigl(\textstyle\int f^2\bigr)^2 \ = \ 3/\pi \ \text{ at the normal}", font_size=30),
        ]
        rows[3][2].set_color(HLC)
        whys = [why(r"the mean drifts at rate one"), why(r"a U-statistic: \ the Walsh-average sign"),
                why(r"Hoeffding's projection, \ Part 47"), why(r"$\int \phi^2 = 1/(2\sqrt\pi)$: \ $12/(4\pi) = 0.955$")]
        with self.voiceover(
            "<bookmark mark='a'/> For the t-test the drift has slope one and the noise is the variance: efficacy one over "
            "sigma squared. <bookmark mark='b'/> The Wilcoxon signed-rank statistic, scaled, estimates the probability that "
            "a Walsh average is positive. <bookmark mark='c'/> Differentiating under the integral, its drift has slope twice "
            "the integral of f squared, and by Hoeffding's projection its variance is one third: efficacy twelve times the "
            "integral of f squared, squared. <bookmark mark='d'/> Their ratio is twelve sigma squared times that integral "
            "squared. At the normal the integral is one over two root pi, and the ratio is three over pi, ninety-five point "
            "five percent."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("are")
        pretty = {"normal": r"normal", "logistic": r"logistic", "Laplace": r"Laplace", "t_3": r"$t_3$", "t_5": r"$t_5$",
                  "t_10": r"$t_{10}$", "contam_0.01": r"1\% contaminated", "contam_0.05": r"5\% contaminated",
                  "contam_0.1": r"10\% contaminated", "uniform": r"uniform", "parabola": r"the parabola"}
        names = [r["name"] for r in d["rows"]]
        ares = [r["are"] for r in d["rows"]]
        A = axes([0.75, 2.0], [-0.6, len(names) - 0.4], x_length=7.0, y_length=4.8, xlabel=r"ARE of Wilcoxon to $t$",
                 ylabel=r"", xticks=[0.8, 1, 1.5, 2], yticks=[], xfmt=lambda v: f"{v:g}", center=[-0.6, 0.0, 0])
        ax = A.ax
        one = DashedLine(ax.c2p(1, -0.6), ax.c2p(1, len(names) - 0.4), color=GREY_B, stroke_width=2)
        dots, labs = VGroup(), VGroup()
        for k, (nm, v) in enumerate(zip(names, ares)):
            y = len(names) - 1 - k
            col = RES if v < 1 else HIT
            dots.add(VGroup(Line(ax.c2p(1, y), ax.c2p(v, y), color=col, stroke_width=4), Dot(ax.c2p(v, y), radius=0.07, color=col)))
            labs.add(label(rf"{pretty[nm]}: \ {v:.3f}", font_size=20, color=GREY_A).next_to(ax.c2p(0.75, y), LEFT, buff=0.15))
        with self.voiceover(
            "<bookmark mark='a'/> The efficiency across eleven distributions. At the normal, point nine five five. "
            "<bookmark mark='b'/> At every heavier-tailed distribution, the logistic, the Laplace, the t distributions and "
            "the contaminated normals, the rank test wins: by ten percent at the logistic, fifty at the Laplace, ninety at "
            "t with three degrees of freedom. <bookmark mark='c'/> At the uniform they tie. <bookmark mark='d'/> And at one "
            "peculiar distribution, a parabola, the rank test does worst: eighty-six point four percent. That is the "
            "bound, and no distribution goes lower."
        ) as vo:
            self.play(FadeIn(A), Create(one))
            vo.wait_until("a")
            self.play(FadeIn(dots[0]), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(dots[k], labs[k])) for k in range(1, 9)], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(dots[9]), FadeIn(labs[9]))
            vo.wait_until("d")
            self.play(FadeIn(dots[10]), FadeIn(labs[10]))
        self.clear_scene()

    def bound(self):
        rows = [
            cmath(r"\min_f", r"\ ", r"\textstyle\int f^2 \ \text{ s.t. } \int f = 1, \ \int x^2 f = 1, \ f \ge 0", font_size=30),
            cmath(r"\text{Lagrange}", r":", r"2 f(x) + a + b x^2 = 0 \ \text{ where } f > 0", font_size=30),
            cmath(r"f(x)", r"=", r"\tfrac{3}{20\sqrt5}(5 - x^2)_+", font_size=32),
            cmath(r"\text{ARE}", r"=", r"108/125 = 0.864", font_size=34),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"ARE is scale-free: \ fix $\sigma = 1$"), why(r"Part 29's Epanechnikov argument again"),
                why(r"a parabola on $[-\sqrt5, \sqrt5]$"), why(r"Hodges \& Lehmann (1956)")]
        with self.voiceover(
            "<bookmark mark='a'/> The bound is a calculus-of-variations problem. The efficiency is scale-free, so fix the "
            "variance at one and minimize the integral of f squared over densities. <bookmark mark='b'/> With Lagrange "
            "multipliers, wherever f is positive it must be a downward parabola, <bookmark mark='c'/> exactly Part 29's "
            "Epanechnikov argument: three over twenty root five times five minus x squared. <bookmark mark='d'/> Plugging "
            "in gives one hundred and eight over one hundred and twenty-five, point eight six four: Joseph Hodges and Erich "
            "Lehmann's theorem of 1956. Giving up the data's values for their ranks costs at most thirteen point six "
            "percent, and can gain without limit."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def scores(self):
        d = load("are")["normal_scores"]
        rows = fit_rows(VGroup(
            label(r"normal scores: \ replace rank $i$ by $\Phi^{-1}(i/(n + 1))$", font_size=24, color=HLC),
            label(rf"ARE to $t$: \ normal {d['normal']:.3f}; \ logistic {d['logistic']:.3f}; \ $t_3$ {d['t_3']:.2f}", font_size=24),
            label(r"Chernoff \& Savage (1958): \ ARE $\ge 1$ for every distribution", font_size=24, color=HIT),
            label(r"ranks with the right scores: \ nothing to lose, \ ever", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One more step. Replace each rank by the corresponding normal quantile: the normal-scores "
            "test. <bookmark mark='b'/> At the normal it is fully efficient; at the logistic it beats t by five percent; at "
            "t with three degrees of freedom by sixty-four. <bookmark mark='c'/> Herman Chernoff and Richard Savage proved in "
            "1958 that its efficiency relative to t is at least one for every distribution. <bookmark mark='d'/> Choose the "
            "scores well, and a rank test never loses to the t-test at all."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def estimators(self):
        rows = [
            cmath(r"\text{ARE}(\text{median} : \bar x)", r"=", r"4\sigma^2 f(0)^2 = 2/\pi = 0.637", font_size=30),
            cmath(r"\text{ARE}(\text{HL} : \bar x)", r"=", r"12\sigma^2(\textstyle\int f^2)^2 = 3/\pi = 0.955", font_size=30),
            cmath(r"\text{tests} \leftrightarrow \text{estimates}", r":", r"\text{same efficiency}", font_size=30),
            cmath(r"\text{Laplace}", r":", r"\text{median } 2.0, \ \text{HL } 1.5", font_size=30),
        ]
        rows[1][2].set_color(HLC)
        whys = [why(r"the sign test's efficiency"), why(r"the signed-rank test's"),
                why(r"Hodges \& Lehmann (1963): \ invert the test"), why(r"where the mean loses badly")]
        with self.voiceover(
            "<bookmark mark='a'/> The same numbers are efficiencies of estimators. The median, which inverts the sign test, "
            "has efficiency two over pi relative to the mean at the normal, sixty-four percent. <bookmark mark='b'/> The "
            "Hodges–Lehmann estimator, inverting the signed-rank test, has three over pi. <bookmark mark='c'/> An estimator "
            "inherits the efficiency of the test it inverts. <bookmark mark='d'/> At the Laplace distribution the median is "
            "twice as efficient as the mean, and Hodges–Lehmann one and a half times."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sign(self):
        rows = [
            cmath(r"S", r"=", r"\#\{i : x_i > 0\} \sim \text{Binomial}(n, \tfrac12) \ \text{under } H_0", font_size=30),
            cmath(r"\mu'(0)", r"=", r"f(0), \ \ \sigma^2(0) = \tfrac14: \ \ \text{efficacy } 4 f(0)^2", font_size=30),
            cmath(r"\text{ARE}(S : t)", r"=", r"4\sigma^2 f(0)^2 = 2/\pi \ \text{ at the normal}", font_size=30),
            cmath(r"\text{Laplace}", r":", r"2: \ \text{the sign test wins}", font_size=30),
        ]
        rows[2][2].set_color(MEDC)
        whys = [why(r"Arbuthnot's test of 1710"), why(r"$P(X > 0) = \frac12 + \theta f(0) + \dots$"),
                why(r"64\%: \ it ignores the sizes"), why(r"heavy tails reward ignoring them")]
        with self.voiceover(
            "<bookmark mark='a'/> The simplest case first: the sign test, John Arbuthnot's of 1710, counts the positive "
            "observations. Under the null the count is binomial with probability a half. <bookmark mark='b'/> Under a shift "
            "theta, the probability of a positive observation rises by theta times f of zero, and the variance is a quarter, "
            "so the efficacy is four f of zero squared. <bookmark mark='c'/> Against the t-test the efficiency is four sigma "
            "squared f of zero squared: two over pi at the normal, sixty-four percent, because the sign test throws away the "
            "sizes. <bookmark mark='d'/> At the Laplace, it is two: there, ignoring sizes is exactly right."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
