from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats38.common import *  # noqa: F403


class UnitRoot(VoiceoverScene):
    def construct(self):
        self.card()
        self.two()
        self.regression()
        self.distribution()
        self.kpss_()
        self.breaks()
        self.macro()
        self.board()

    def card(self):
        card = chapter_card(3, r"Unit roots", r"Does the series come back?", lit=(1979, 1992), part=PART)
        with self.voiceover("Chapter three. Unit roots."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def two(self):
        d = load("unitroot")
        rw, st = np.asarray(d["rw"], float), np.asarray(d["st"], float)
        lo, hi = float(min(rw.min(), st.min())) - 1, float(max(rw.max(), st.max())) + 1
        A = axes([0, 200], [lo, hi], x_length=10.0, y_length=3.8, xlabel=r"time", ylabel=r"", xticks=[0, 100, 200],
                 yticks=[0], center=[0, 0.5, 0])
        c1 = series_line(A.ax, np.arange(200), rw, MISSC, 2.2)
        c2 = series_line(A.ax, np.arange(200), st, Y0C, 2.2)
        foot = fit_rows(VGroup(
            label(r"red: \ a random walk, \ $X_t = X_{t-1} + \varepsilon_t$: \ shocks are permanent", font_size=24, color=MISSC),
            label(r"blue: \ $X_t = 0.9 X_{t-1} + \varepsilon_t$: \ shocks fade, \ slowly; \ the same shocks", font_size=24, color=Y0C),
        ), 12.4, 0.3, [0, -2.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two series driven by the same shocks. In red, a random walk: each value is the last plus a "
            "shock, so every shock is permanent and the variance grows with time. <bookmark mark='b'/> In blue, an "
            "autoregression with coefficient point nine: shocks fade, slowly, and the series returns to zero. Over two "
            "hundred steps they can look alike. Whether a series like gross domestic product has a unit root decides "
            "whether a recession is ever made up, whether forecasts revert, and, chapter four, whether regressions on it "
            "mean anything."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(foot[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(foot[1]), run_time=2.5)
        self.clear_scene()

    def regression(self):
        rows = [
            cmath(r"\Delta X_t", r"=", r"\alpha + \gamma X_{t-1} + \textstyle\sum_j c_j \Delta X_{t-j} + \varepsilon_t", font_size=30),
            cmath(r"H_0", r":", r"\gamma = 0 \ \text{(a unit root)} \quad H_1: \gamma < 0", font_size=30),
            cmath(r"\tau = \hat\gamma / \text{SE}", r"\Rightarrow", r"\dfrac{\int_0^1 W\, dW}{(\int_0^1 W^2)^{1/2}} \quad \text{(no constant)}", font_size=30),
            cmath(r"\text{not normal}", r":", r"\text{skewed left; \ 5\% point } -2.86 \text{ with a constant}", font_size=30),
        ]
        rows[2][-1].set_color(MISSC)
        whys = [why(r"augmented: \ lags soak up short-run dynamics"), why(r"Dickey \& Fuller (1979)"),
                why(r"a functional of Brownian motion \ (Part 44)"), why(r"MacKinnon's tables")]
        with self.voiceover(
            "<bookmark mark='a'/> David Dickey and Wayne Fuller's test, of 1979, regresses the change in the series on its "
            "last level, with lagged changes to absorb short-run dynamics. <bookmark mark='b'/> A unit root means the "
            "coefficient on the level is zero; a stationary series pulls back, with a negative coefficient. <bookmark "
            "mark='c'/> The catch: under the unit root, the usual t statistic does not converge to a normal. Scaled sums "
            "of a random walk converge to integrals of Brownian motion, by the functional central limit theorem that Part "
            "forty-four proves, and the statistic converges to a ratio of such integrals. <bookmark mark='d'/> Its "
            "distribution is skewed to the left, and its five percent point, with a constant in the regression, is minus "
            "two point eight six, not minus one point six four."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def distribution(self):
        d = load("unitroot")
        e = np.asarray(d["edges"], float)
        h = np.asarray(d["hist"], float)
        w = e[1] - e[0]
        A = axes([-5, 3], [0, 0.6], x_length=8.0, y_length=4.0, xlabel=r"Dickey--Fuller $\tau$ under a unit root, \ $T = 100$",
                 ylabel=r"density", xticks=[-4, -2.89, -1.645, 0, 2], yticks=[0, 0.2, 0.4], xfmt=lambda v: f"{v:g}",
                 yfmt=lambda v: f"{v:g}", center=[-1.6, 0.2, 0])
        ax = A.ax
        bars = hist_bars(ax, e, h / h.sum() / w, color=MISSC, opacity=0.55)
        xs = np.linspace(-5, 3, 200)
        nrm = curve(ax, xs, stats.norm.pdf(xs), GREY_A, 3)
        c1 = DashedLine(ax.c2p(-1.645, 0), ax.c2p(-1.645, 0.6), color=GREY_A, stroke_width=2.5)
        c2 = DashedLine(ax.c2p(d["crit"], 0), ax.c2p(d["crit"], 0.6), color=BANDC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"20,000 random walks", font_size=22),
            label(r"grey: \ the normal the $t$-table assumes", font_size=22, color=GREY_A),
            label(rf"using $-1.645$: \ rejects {100 * d['size_normal']:.0f}\% of true unit roots", font_size=22, color=MISSC),
            label(rf"MacKinnon's $-2.89$: \ the simulated 5\% point is {d['q05']:.2f}", font_size=22, color=BANDC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Twenty thousand random walks of length one hundred, each tested with a constant in the "
            "regression. <bookmark mark='b'/> In grey, the normal curve the ordinary t table assumes. The real distribution "
            "sits well to its left, centred near minus one and a half. <bookmark mark='c'/> A test that rejects the unit "
            "root when tau is below minus one point six four five rejects " + str(round(100 * d["size_normal"])) + " "
            "percent of the time when the unit root is true. <bookmark mark='d'/> James MacKinnon's critical value for this "
            "sample size, minus two point eight nine, matches the simulated five percent point, " + say(d["q05"], 2) + "."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(bars), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(nrm), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(c2), FadeIn(side[3]))
        self.clear_scene()

    def kpss_(self):
        rows = fit_rows(VGroup(
            label(r"Dickey--Fuller's null is the unit root: \ failing to reject is weak evidence", font_size=26, color=MISSC),
            label(r"near a unit root, \ $\phi = 0.95$ say, \ the test has little power in short samples", font_size=26),
            label(r"KPSS \ (Kwiatkowski, \ Phillips, \ Schmidt \& Shin 1992): \ the null is stationarity", font_size=26, color=BANDC),
            label(r"use both: \ the four combinations of verdicts say different things", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Dickey and Fuller's null hypothesis is the unit root, so failing to reject it is weak "
            "evidence for it. <bookmark mark='b'/> A stationary series with coefficient nought point nine five is hard to "
            "tell from a random walk in a few decades of data, and the test's power is low. <bookmark mark='c'/> Denis "
            "Kwiatkowski, Peter Phillips, Peter Schmidt and Yongcheol Shin reversed the roles in 1992: their KPSS test takes "
            "stationarity as the null, and rejects when the partial sums of the deviations wander too far. <bookmark "
            "mark='d'/> Using both gives four possible verdicts: unit root, stationary, both rejected, or neither, which "
            "means the data cannot tell."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def macro(self):
        d = load("unitroot")["tests"]
        rows = [[r"series, \ US 1959--2009", r"ADF $\tau$", r"5\% point", r"KPSS", r"5\% point", r"verdict"]]
        verdict = {"log real GDP": r"unit root", "unemployment": r"cannot tell", "T-bill rate": r"cannot tell",
                   "inflation": r"cannot tell", "GDP growth": r"stationary"}
        cols = [GREY_A]
        for k in ("log real GDP", "unemployment", "T-bill rate", "inflation", "GDP growth"):
            v = d[k]
            rows.append([k, f"{v['adf']:.2f}".replace("-", "$-$"), f"{v['crit']:.2f}".replace("-", "$-$"), f"{v['kpss']:.3f}",
                         f"{v['kcrit']:.3f}", verdict[k]])
            cols.append(MISSC if verdict[k] == "unit root" else (BANDC if verdict[k] == "stationary" else TAUC))
        tab = table_rows(rows, font_size=22, col_buff=0.55, row_buff=0.3, colors=cols).move_to([0, 0.6, 0])
        foot = label(r"log GDP with a trend in both tests; \ 4 lags in the ADF; \ Nelson \& Plosser (1982) began this debate",
                     font_size=22, color=GREY_A).move_to([0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> US quarterly data, 1959 to 2009. <bookmark mark='b'/> Log real gross domestic product: the "
            "Dickey-Fuller test, allowing a trend, cannot reject a unit root, and KPSS rejects trend-stationarity. Both "
            "point to a unit root, as Charles Nelson and Charles Plosser argued for most US series in 1982. <bookmark "
            "mark='c'/> Unemployment, the Treasury-bill rate and inflation: neither test rejects. Fifty years of quarterly "
            "data cannot say whether these series revert. <bookmark mark='d'/> The growth rate of GDP: Dickey-Fuller rejects "
            "the unit root decisively, and KPSS does not reject stationarity. Differencing a unit-root series gives a "
            "stationary one."
        ) as vo:
            self.add(macro_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[2:5]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(tab[5]))
        self.clear_scene()

    def board(self):
        rows = board_rows("Dickey", "KPSS")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board, as tests of size five percent. The Dickey-Fuller statistic with the "
                   "normal critical value: broken. <bookmark mark='b'/> With MacKinnon's critical value: kept. And KPSS on a "
                   "stationary autoregression, with its long-run variance: kept.",
                   [("a", [0]), ("b", [1, 2])])

    def breaks(self):
        rows = fit_rows(VGroup(
            label(r"Perron (1989): \ a stationary series around a trend that breaks once looks like a unit root", font_size=26, color=MISSC),
            label(r"the 1929 crash and the 1973 oil shock: \ allow those breaks, \ and many unit roots vanish", font_size=26, color=TAUC),
            label(r"Zivot \& Andrews (1992): \ let the data choose the break date, \ with new critical values", font_size=26, color=BANDC),
            label(r"the honest conclusion: \ persistence is high; \ its exact form is hard to pin down", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A further complication. Pierre Perron showed in 1989 that a stationary series moving around a "
            "trend that shifts once looks, to the Dickey-Fuller test, like a unit root: the test mistakes one permanent "
            "change for an accumulation of permanent shocks. <bookmark mark='b'/> Allowing breaks at the 1929 crash and the "
            "1973 oil shock, he rejected unit roots in many of Nelson and Plosser's series. <bookmark mark='c'/> Eric Zivot and "
            "Donald Andrews then let the data choose the break date, which changes the critical values again, because "
            "searching for the best break is another garden of forking paths. <bookmark mark='d'/> The honest conclusion "
            "for many economic series is that persistence is high, and its exact form is hard to pin down."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
