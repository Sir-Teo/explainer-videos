from __future__ import annotations

import numpy as np

from videos.stats.stats38.common import *  # noqa: F403


class Coint(VoiceoverScene):
    def construct(self):
        self.card()
        self.pair()
        self.tstats()
        self.idea()
        self.consumption()
        self.superconsistent()
        self.tests()
        self.board()

    def card(self):
        card = chapter_card(4, r"Spurious regression and cointegration", r"When two wanderers are tied together",
                            lit=(1974, 1987, 1988), part=PART)
        with self.voiceover("Chapter four. Spurious regression, and cointegration."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def pair(self):
        d = load("coint")
        x, y = (np.asarray(v, float) for v in d["example"])
        lo, hi = float(min(x.min(), y.min())) - 1, float(max(x.max(), y.max())) + 1
        A = axes([0, 100], [lo, hi], x_length=6.0, y_length=3.6, xlabel=r"time", ylabel=r"", xticks=[0, 50, 100], yticks=[0],
                 center=[-3.4, 0.4, 0])
        B = axes([float(x.min()) - 1, float(x.max()) + 1], [float(y.min()) - 1, float(y.max()) + 1], x_length=4.4, y_length=3.6,
                 xlabel=r"$x_t$", ylabel=r"$y_t$", xticks=[], yticks=[], center=[3.6, 0.4, 0])
        c1, c2 = series_line(A.ax, np.arange(100), x, Y0C, 2.2), series_line(A.ax, np.arange(100), y, MISSC, 2.2)
        dots = VGroup(*[Dot(B.ax.c2p(a, b), radius=0.04, color=TAUC) for a, b in zip(x, y)])
        b = np.polyfit(x, y, 1)
        fit = Line(B.ax.c2p(x.min(), b[1] + b[0] * x.min()), B.ax.c2p(x.max(), b[1] + b[0] * x.max()), color=MISSC, stroke_width=3)
        foot = label(r"two independent random walks: \ regress one on the other", font_size=24, color=GREY_A).move_to([0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part seventeen met Yule's nonsense correlations of 1926. Here is their modern form. Two "
            "random walks, generated independently. <bookmark mark='b'/> Plot one against the other and fit a line. The "
            "line has a steep slope, a high R squared, and a t statistic that any journal would accept. Yet the two series "
            "have nothing to do with each other."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(c1), Create(c2), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(dots), Create(fit))
        self.clear_scene()

    def tstats(self):
        d = load("coint")
        e = np.linspace(-20, 20, 41)
        h = np.asarray(d["t_hist"], float)
        A = axes([-20, 20], [0, 0.08], x_length=8.0, y_length=4.0, xlabel=r"$t$ statistic for the slope, \ independent walks, \ $T = 100$",
                 ylabel=r"share", xticks=[-20, -10, -1.96, 1.96, 10, 20], yticks=[0, 0.04, 0.08], xfmt=lambda v: f"{v:g}",
                 yfmt=lambda v: f"{v:g}", center=[-1.6, 0.2, 0])
        ax = A.ax
        bars = hist_bars(ax, e, h / h.sum(), color=MISSC, opacity=0.6)
        bands = Rectangle(width=ax.c2p(1.96, 0)[0] - ax.c2p(-1.96, 0)[0], height=ax.c2p(0, 0.08)[1] - ax.c2p(0, 0)[1],
                          stroke_width=0, fill_color=BANDC, fill_opacity=0.15).move_to(ax.c2p(0, 0.04))
        side = fit_rows(VGroup(
            label(r"5,000 pairs", font_size=22),
            label(rf"$|t| > 1.96$: \ {100 * d['reject']:.0f}\% of the time", font_size=22, color=MISSC),
            label(rf"median $R^2$ = {d['median_r2']:.2f}; \ above 0.5 in {100 * d['share_r2_05']:.0f}\%", font_size=22, color=TAUC),
            label(r"Granger \& Newbold (1974): \ 76\%", font_size=22, color=GREY_A),
            label(r"Phillips (1986): \ $t$ grows like $\sqrt{T}$", font_size=22, color=GREY_A),
        ), 3.8, 0.38, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Five thousand such pairs. The green band holds the t statistics a five percent test would "
            "accept. <bookmark mark='b'/> The real statistics spread far beyond it: the test declares a significant "
            "relationship " + str(round(100 * d["reject"])) + " percent of the time. <bookmark mark='c'/> Clive Granger and "
            "Paul Newbold found seventy-six percent in 1974, and suggested a rule of thumb: be suspicious when R squared "
            "exceeds the Durbin-Watson statistic. <bookmark mark='d'/> Peter Phillips explained it in 1986: with two unit "
            "roots, the slope does not converge, and the t statistic grows like the square root of the sample size. More "
            "data makes the nonsense more significant."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(bands), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def idea(self):
        rows = [
            cmath(r"x_t,\ y_t", r":", r"\text{each a unit root}", font_size=30),
            cmath(r"y_t - \beta x_t", r":", r"\text{stationary for some } \beta \ \Rightarrow \ \text{cointegrated}", font_size=30),
            cmath(r"\Delta y_t", r"=", r"\alpha\, (y_{t-1} - \beta x_{t-1}) + \ldots + \varepsilon_t", font_size=30),
            cmath(r"\text{test}", r":", r"\text{a unit root in } \hat u_t = y_t - \hat\beta x_t, \ \text{with stricter critical values}", font_size=28),
        ]
        rows[1][-1].set_color(BANDC)
        whys = [why(r"both wander"), why(r"Engle \& Granger (1987)"), why(r"the error-correction model"),
                why(r"MacKinnon: \ $-3.37$, \ not $-2.89$")]
        with self.voiceover(
            "<bookmark mark='a'/> But some wandering series really are tied together. Each has a unit root on its own; "
            "<bookmark mark='b'/> but some combination of them is stationary. Robert Engle and Clive Granger called such "
            "series cointegrated, in 1987. A drunk and her dog both wander, but the leash keeps them close. <bookmark "
            "mark='c'/> Cointegrated series obey an error-correction model: when they drift apart, the gap pulls them back. "
            "<bookmark mark='d'/> To test, estimate the combination by regression, and test its residuals for a unit root. "
            "Because the regression has already chosen the most stationary-looking combination, the critical values are "
            "stricter than Dickey and Fuller's: minus three point three seven for two series and a hundred observations. "
            "Engle and Granger shared the 2003 Nobel prize, Engle for chapter five."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def consumption(self):
        d = load("coint")
        t = np.asarray(d["t"], float)
        lc, ly = np.asarray(d["lc"], float), np.asarray(d["ly"], float)
        A = axes([1959, 2010], [7.4, 9.4], x_length=6.0, y_length=3.6, xlabel=r"year", ylabel=r"log, \ billions of 2005 \$",
                 xticks=[1960, 1980, 2000], yticks=[7.5, 8.5], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", center=[-3.4, 0.4, 0])
        res = np.asarray(d["eg_resid"], float)
        B = axes([1959, 2010], [float(res.min()) - 0.01, float(res.max()) + 0.01], x_length=4.6, y_length=3.6, xlabel=r"year",
                 ylabel=r"residual", xticks=[1960, 1980, 2000], yticks=[0], xfmt=lambda v: f"{v:.0f}", center=[3.6, 0.4, 0])
        c1, c2 = series_line(A.ax, t, lc, Y0C, 2.2), series_line(A.ax, t, ly, MISSC, 2.2)
        cr = series_line(B.ax, t, res, TAUC, 2)
        foot = fit_rows(VGroup(
            label(r"blue: \ log real consumption; \ red: \ log real disposable income", font_size=22, color=GREY_A),
            label(rf"each has a unit root \ (ADF with trend: \ {d['adf_lc']:.2f}, \ {d['adf_ly']:.2f}); \ slope $\hat\beta$ = {d['eg']['beta']:.3f}", font_size=22),
        ), 12.4, 0.25, [0, -2.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Friedman's permanent-income theory suggests consumption and income should be tied: "
            "people spend a stable share of what they expect to earn. US log consumption and log disposable income, 1959 to "
            "2009. <bookmark mark='b'/> Each, on its own, has a unit root. The regression of one on the other has a slope of "
            + say(d["eg"]["beta"], 2) + ": one for one. <bookmark mark='c'/> The residual, the gap between consumption and "
            "income, wanders less, but it wanders."
        ) as vo:
            self.add(macro_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(c1), Create(c2), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(B), Create(cr))
        self.clear_scene()

    def tests(self):
        d = load("coint")
        jo, jc = d["johansen"], d["jo_crit"]
        rows = fit_rows(VGroup(
            label(rf"Engle--Granger: \ residual $\tau$ = {d['eg']['t']:.2f} \ against $-3.37$: \ cannot reject no cointegration", font_size=26, color=MISSC),
            label(r"Johansen (1988): \ a VAR in levels, \ the rank of its long-run matrix by canonical correlations", font_size=26, color=TAUC),
            label(rf"consumption, \ income, \ investment: \ trace {jo[0]:.1f} vs {jc[0]:.1f} \ (rank 0 rejected); \ {jo[1]:.1f} vs {jc[1]:.1f}", font_size=26, color=BANDC),
            label(r"one long-run relation, \ barely: \ cointegration tests are weak in 200 quarters", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The Engle-Granger test on the residual gives minus " + say(-d["eg"]["t"], 2) + ", short of "
            "the critical value of minus three point three seven: it cannot reject that there is no cointegration. <bookmark "
            "mark='b'/> Søren Johansen's method of 1988 works with all the series at once, in a vector autoregression in "
            "levels, and estimates how many independent stationary combinations there are, from canonical correlations "
            "between changes and lagged levels. <bookmark mark='c'/> With consumption, income and investment, the trace "
            "test rejects zero relations, " + say(jo[0], 1) + " against a critical value of " + say(jc[0], 1) + ", and does "
            "not reject one. <bookmark mark='d'/> One long-run relation, barely. With two hundred quarters, cointegration "
            "tests, like unit-root tests, have little power, and the economics has to carry part of the argument."
        ) as vo:
            self.add(macro_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("random walks")
        rows = [r for r in rows if "regression" in r.method or "Engle" in r.method]
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board, as tests of size five percent on pairs of independent random walks. "
                   "The ordinary regression t test: broken, rejecting " + f"{100 * rows[0].achieved:.0f}" + " percent of the "
                   "time. <bookmark mark='b'/> The Engle-Granger test with MacKinnon's critical values: kept.",
                   [("a", [0]), ("b", [1])])

    def superconsistent(self):
        rows = fit_rows(VGroup(
            label(r"if they are cointegrated, \ $\hat\beta$ converges at rate $T$, \ not $\sqrt{T}$: \ super-consistent", font_size=26, color=BANDC),
            label(r"Stock (1987): \ but its distribution is not normal, \ so the OLS $t$-test is still wrong", font_size=26, color=MISSC),
            label(r"FM-OLS \ (Phillips \& Hansen 1990), \ DOLS \ (Stock \& Watson 1993): \ valid $t$-tests for $\beta$", font_size=26, color=TAUC),
            label(r"the error-correction speed $\alpha$: \ how fast a gap closes", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> When series are cointegrated, the regression has a surprising property. The slope converges "
            "to the truth at rate T rather than the square root of T, because any wrong slope leaves a residual that "
            "wanders off as a random walk, which least squares punishes heavily. James Stock called it super-consistency in "
            "1987. <bookmark mark='b'/> But its distribution is not normal, and correlated with the shocks, so the usual t "
            "test on the slope is still wrong. <bookmark mark='c'/> Fully modified least squares, of Peter Phillips and Bruce "
            "Hansen, and dynamic least squares, of Stock and Mark Watson, correct it. <bookmark mark='d'/> And the "
            "error-correction coefficient says how quickly a gap between the series closes."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
