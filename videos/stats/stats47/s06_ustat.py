from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class UStatistics(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.hoeffding()
        self.table()
        self.degenerate()
        self.chart()
        self.projection()

    def card(self):
        card = chapter_card(5, r"U-statistics", r"Averages over pairs", lit=(1948,), part=PART)
        with self.voiceover("Chapter five. U-statistics: averages over pairs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"U_n", r"=", r"\binom n2^{-1} \textstyle\sum_{i < j} h(X_i, X_j), \ \ \theta = E\,h(X_1, X_2)", font_size=32),
            cmath(r"h = \tfrac12 (x - y)^2", r":", r"U_n = s^2", font_size=34),
            cmath(r"h = |x - y|", r":", r"\text{Gini's mean difference}", font_size=34),
            cmath(r"h = \mathbf 1\{x + y > 0\}, \ \ \mathrm{sign}\ldots", r":", r"\text{Wilcoxon, \ Kendall's } \tau, \ \text{Mann--Whitney}", font_size=30),
        ]
        rows[0][-1].set_color(S.ACCENT)
        whys = [why(r"Hoeffding (1948)"), why(r"the sample variance"), why(r"a robust spread"), why(r"rank statistics")]
        with self.voiceover(
            "<bookmark mark='a'/> For independent identically distributed observations, a U-statistic averages a "
            "symmetric integrable kernel h over all pairs of observations; it is unbiased for the kernel's "
            "expectation, and Wassily Hoeffding developed their theory in 1948. <bookmark mark='b'/> With h equal to "
            "half the squared difference, U is the sample variance. <bookmark mark='c'/> With the absolute "
            "difference, Gini's mean difference. <bookmark mark='d'/> And with indicators of signs or sums, the "
            "Wilcoxon statistic, Kendall's tau and the Mann–Whitney statistic: much of nonparametric statistics is "
            "U-statistics."       ) as vo:
            heading=label('An integrable pair kernel defines an unbiased U-statistic',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hoeffding(self):
        rows = [
            cmath(r"h_1(x)", r"=", r"E\,h(x, X_2) - \theta, \ \ \zeta_1 = \mathrm{Var}\, h_1(X)", font_size=34),
            cmath(r"\hat U_n", r"=", r"\theta + \tfrac2n \textstyle\sum_i h_1(X_i): \ \text{the projection}", font_size=34),
            cmath(r"\mathrm{Var}\, U_n", r"=", r"\frac{4(n - 2)\zeta_1 + 2\zeta_2}{n(n - 1)}, \ \ \zeta_2 = \mathrm{Var}\, h", font_size=32),
            cmath(r"\zeta_1 > 0", r"\Rightarrow", r"\sqrt n(U_n - \theta) \Rightarrow N(0, 4\zeta_1)", font_size=34),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"average out one argument"), why(r"a sum of independent terms"), why(r"exact, \ any $n$"), why(r"$U_n - \hat U_n = O_P(1/n)$")]
        with self.voiceover(
            "<bookmark mark='a'/> Hoeffding's idea: average the kernel over its second argument, giving a function of"
            " one observation, h one, with variance zeta one. <bookmark mark='b'/> The projection of U onto sums of "
            "functions of single observations is theta plus two over n times the sum of h one: a plain average. "
            "<bookmark mark='c'/> The exact variance of U combines zeta one and the kernel's own variance, zeta two. "
            "<bookmark mark='d'/> With a finite second moment of the kernel, the difference between U and its "
            "projection is of order one over n in probability, so when zeta one is positive, root n times U minus "
            "theta is asymptotically normal with variance four zeta one."
        ) as vo:
            heading=label('A finite-variance kernel splits into projection and remainder',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("ustat")
        rows = [[r"$n$", r"exact $\mathrm{Var}\,U$", r"first order $4\zeta_1/n$", r"simulated"]]
        for r in d["rows"]:
            rows.append([str(r["n"]), f"{r['exact']:.4f}", f"{r['first']:.4f}", f"{r['sim']:.4f}"])
        tab = table_rows(rows, font_size=30, col_buff=0.9, row_buff=0.32, colors=[GREY_A, None, None, None]).move_to([0, 0.8, 0])
        note_ = fit_rows(VGroup(
            label(rf"Gini's mean difference, \ $N(0, 1)$ data: \ $\theta = 2/\sqrt\pi$, \ $\zeta_1 = {d['zeta1']:.4f}$, \ $\zeta_2 = {d['zeta2']:.4f}$", font_size=24, color=GREY_A),
            label(r"the exact formula matches the simulation; \ the projection's variance is already close at $n = 20$", font_size=24, color=S.ACCENT),
        ), 12.4, 0.25, [0, -1.9, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Gini's mean difference for normal data, where both zetas can be computed by quadrature. "
            f"<bookmark mark='b'/> The exact variance formula matches the simulation at ten, twenty and fifty observations. "
            f"<bookmark mark='c'/> The first-order variance from the projection alone is twelve percent too small at ten, "
            f"six percent at twenty and two and a half percent at fifty: the projection captures almost everything."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_[0]), FadeIn(exact_tag(r"exact; \ simulated: 4,000 samples")))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(note_[1]))
        self.clear_scene()

    def degenerate(self):
        rows = [
            cmath(r"\zeta_1 = 0", r":", r"\text{the projection vanishes: \ a degenerate kernel}", font_size=32),
            cmath(r"h(x, y)", r"=", r"\theta+\textstyle\sum_k \lambda_k \phi_k(x)\phi_k(y) \ \ (\text{an eigen-expansion})", font_size=32),
            cmath(r"n(U_n-\theta)", r"\Rightarrow", r"\textstyle\sum_k \lambda_k (Z_k^2 - 1), \ \ Z_k \text{ i.i.d. } N(0, 1)", font_size=32),
            cmath(r"h = xy, \ EX=0,\ \mathrm{Var}(X)=1", r":", r"n U_n \Rightarrow \chi^2_1 - 1", font_size=34),
        ]
        rows[2][-1].set_color(S.ACCENT)
        whys = [why(r"e.g.\ under a null"), why(r"centered square-integrable kernel"), why(r"a weighted $\chi^2$, \ rate $n$"), why(r"one eigenvalue")]
        with self.voiceover(
            "<bookmark mark='a'/> When zeta one is zero, the projection vanishes and the kernel is called degenerate;"
            " this is typical for test statistics under the null. <bookmark mark='b'/> For a centered degenerate "
            "square-integrable kernel, use the spectral expansion of its self-adjoint Hilbert–Schmidt operator. "
            "<bookmark mark='c'/> Then n times U, at the faster rate n, converges to a weighted sum of centred "
            "chi-squares, not to a normal. <bookmark mark='d'/> The simplest case, the kernel x times y for data with"
            " mean zero and variance one, has one nonzero eigenvalue equal to one, and n U converges to a chi-square "
            "with one degree of freedom, minus one. Energy distances and kernel two-sample tests are built on this."
        ) as vo:
            heading=label('Degeneracy removes the linear term and changes the limit',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("ustat")
        e = np.asarray(d["deg_edges"])
        hist_top=max(1.2,float(np.max(d["deg_hist"]))+.1)
        A = axes([-1.5, 6], [0, hist_top], x_length=7.4, y_length=4.4, xlabel=r"$n\, U_n$, \ $h = xy$, \ $n = 200$", ylabel=r"density",
                 xticks=[-1, 0, 2, 4, 6], yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        hb = hist_bars(ax, e, np.asarray(d["deg_hist"]), color=MLEC, opacity=0.7)
        u = np.linspace(-0.97, 6, 300)
        ch = clip_curve(ax, u, stats_chi1(u + 1), LIMC, 4, ymax=1.2)
        side = fit_rows(VGroup(
            label(r"blue: \ 20,000 values of $n U_n$", font_size=22, color=MLEC),
            label(r"white: \ the density of $\chi^2_1 - 1$", font_size=22, color=LIMC),
            label(rf"mean {d['deg_mean']:.3f} \ (0), \ variance {d['deg_var']:.2f} \ (2)", font_size=22, color=S.ACCENT),
            label(r"limiting law: \ skewed, \ bounded below by $-1$", font_size=22, color=HODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Simulated: twenty thousand values of n U with two hundred observations. <bookmark "
            f"mark='b'/> In white, the density of chi-square one minus one. <bookmark mark='c'/> The mean is "
            f"{say(d['deg_mean'], 3)} and the variance {say(d['deg_var'], 2)}, against zero and two. <bookmark mark='d'/> The "
            f"limit is skewed and bounded below by minus one: a normal approximation would be badly wrong."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 20,000 samples")))
            vo.wait_until("a")
            self.play(FadeIn(hb), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ch), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def projection(self):
        rows = fit_rows(VGroup(
            label(r"Hájek's projection (1968): \ for any statistic $T$ of independent $X_i$,", font_size=26),
            label(r"$\hat T = \sum_i E[T \mid X_i] - (n - 1) E T$ \ is its best approximation by a sum", font_size=26, color=GOODC),
            label(r"if the projection obeys a CLT and $\mathrm{Var}\,\hat T/\mathrm{Var}\,T\to1$, \ standardized $T$ inherits it", font_size=26, color=S.ACCENT),
            label(r"next: \ rank statistics, \ where no kernel is in sight", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Jaroslav Hájek generalized the idea in 1968. For any statistic of independent "
            "observations, <bookmark mark='b'/> the sum of its conditional expectations given each observation, "
            "suitably centred, is the best approximation by a sum of functions of one observation each: an orthogonal"
            " projection, in Part forty-four's sense. <bookmark mark='c'/> If the projection captures almost all "
            "variance and its independent summands satisfy a central limit theorem, for example by Lindeberg, the "
            "standardized statistic inherits that normal limit. Variance capture alone is insufficient. <bookmark "
            "mark='d'/> Next, this is applied where no obvious kernel is in sight: statistics built from ranks."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()


def stats_chi1(x):
    from scipy import stats

    return stats.chi2.pdf(np.asarray(x, float), 1)
