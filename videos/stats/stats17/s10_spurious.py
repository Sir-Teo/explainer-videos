from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.stats.board import coverage_board, load_all
from explainer.stats.kit import ts as T
from videos.stats.stats17.common import *  # noqa: F403
from videos.stats.stats17.compute import rng, spurious_stats

def sci_p(p: float) -> str:
    e = int(np.floor(np.log10(p)))
    return rf"p \approx {p / 10 ** e:.0f} \times 10^{{{e}}}"


SEED = 2  # the first seed pair (2s, 2s + 1) whose walks give |t| > 8


class Spurious(VoiceoverScene):
    def construct(self):
        self.card()
        self.example()
        self.distribution()
        self.why()
        self.rule()
        self.cure()
        self.board()
        self.lessons()

    def card(self):
        card = chapter_card(9, r"Spurious regression", r"Yule's nonsense, \ made precise", part=PART)
        with self.voiceover("Chapter nine. Spurious regression, a first look."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def example(self):
        x, y = T.random_walk(100, rng(2 * SEED)), T.random_walk(100, rng(2 * SEED + 1))
        t, r2, dw = spurious_stats(x, y)
        b = np.polyfit(x, y, 1)
        lo, hi = min(x.min(), y.min()), max(x.max(), y.max())
        A = axes([0, 100], [lo, hi], x_length=5.6, y_length=3.4, xlabel=r"time", center=[-3.6, 0.8, 0], font_size=18)
        l1 = series_line(A.ax, np.arange(100), x, S.CTRL, 2.2)
        l2 = series_line(A.ax, np.arange(100), y, RES, 2.2)
        B = axes([x.min(), x.max()], [y.min(), y.max()], x_length=4.0, y_length=3.4, xlabel=r"$x_t$", ylabel=r"$y_t$",
                 center=[1.6, 0.8, 0], font_size=18)
        dots = scatter(B.ax, x, y, color=OBS, radius=0.045)
        fl = Line(B.ax.c2p(x.min(), np.polyval(b, x.min())), B.ax.c2p(x.max(), np.polyval(b, x.max())), color=MODEL, stroke_width=3)
        rows = fit_rows(VGroup(
            label(r"two independent random walks", font_size=22),
            MathTex(rf"t = {t:.1f}", font_size=32, color=RES),
            MathTex(rf"R^2 = {r2:.2f}", font_size=28),
            MathTex(sci_p(2 * stats.t.sf(abs(t), 98)), font_size=28, color=RES),
            label(r"and no connection at all", font_size=22, color=OBS),
        ), 2.6, 0.38, [5.4, 0.8, 0])
        tag = simulated_tag(r"seeded walks, \ $n = 100$", corner=DR)
        self.ex = (t, r2, dw)
        with self.voiceover(
            "Yule's nonsense correlations have a modern name: spurious regression. <bookmark mark='a'/> Here are two random "
            "walks of a hundred steps, generated completely independently. <bookmark mark='b'/> Regress one on the other by "
            "Part 12's least squares. <bookmark mark='c'/> The slope's t statistic is fourteen and a half. "
            "<bookmark mark='d'/> R squared is point six eight, <bookmark mark='e'/> and the p-value has twenty-five zeros "
            "after the decimal point. <bookmark mark='f'/> And the two series have nothing to do with each other."
        ) as vo:
            self.add(tag)
            vo.wait_until("a")
            self.play(FadeIn(A), Create(l1), Create(l2), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(dots), Create(fl))
            for k, m_ in enumerate("cdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def distribution(self):
        d = load("spurious")
        t = np.asarray(d["t"])
        e = np.linspace(-30, 30, 61)
        A = axes([-30, 30], [0, 0.42], x_length=9.0, y_length=4.0, xlabel=r"the slope's $t$ statistic", ylabel=r"density",
                 xticks=[-30, -20, -10, 0, 10, 20, 30], yticks=[0, 0.2, 0.4], center=[-1.2, 0.3, 0])
        ax = A.ax
        h = np.histogram(np.clip(t, -29.9, 29.9), e)[0] / (len(t) * 1.0)
        bars = hist_bars(ax, e, h, color=RES, opacity=0.75)
        xs = np.linspace(-6, 6, 300)
        tc = curve(ax, xs, stats.t(98).pdf(xs), GREY_A, 3)
        crit = VGroup(*[DashedLine(ax.c2p(s * 1.98, 0), ax.c2p(s * 1.98, 0.4), color=GREY_B, stroke_width=1.5) for s in (1, -1)])
        rows = fit_rows(VGroup(
            label(r"grey: \ Student's $t$, \ what the test assumes", font_size=22, color=GREY_A),
            label(r"red: \ 5,000 pairs of independent walks", font_size=22, color=RES),
            MathTex(rf"P(|t| > 1.98) = {d['reject']:.2f}", font_size=30, color=RES),
            label(r"half of the $|t|$ exceed 4.4", font_size=22),
        ), 3.6, 0.4, [5.2, 0.4, 0])
        tag = simulated_tag(r"Granger \& Newbold's experiment", corner=DR)
        with self.voiceover(
            "Was that a fluke? <bookmark mark='a'/> If the regression assumptions held, the t statistic would follow Student's "
            "t distribution, in grey, and exceed one point nine eight only five percent of the time. <bookmark mark='b'/> Here "
            "are five thousand pairs of independent random walks. The t statistics are spread over a range ten times wider. "
            "<bookmark mark='c'/> Seventy-five percent of them are significant at the five percent level. "
            "<bookmark mark='d'/> Half exceed four point four. Clive Granger and Paul Newbold ran this experiment in 1974 and "
            "warned econometricians that many published regressions between trending economic series were nonsense."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(tc), FadeIn(crit), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.02), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def why(self):
        rows = [
            cmath(r"y_t", r"=", r"a + b x_t + u_t,\ \ \text{true } b = 0", font_size=32),
            cmath(r"u_t", r"=", r"y_t - a\ \ \text{is a random walk}", font_size=32),
            cmath(r"\text{OLS SE}", r":", r"\text{assumes independent } u_t", font_size=32),
            cmath(r"t", r"\sim", r"\sqrt n \times \text{(a random limit)}", font_size=32),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"the regression we ran"), why(r"the errors inherit the wandering"),
                why(r"far too small for errors this persistent"), why(r"Phillips (1986): \ $t$ grows with $n$")]
        with self.voiceover(
            "Why does it happen? <bookmark mark='a'/> The true slope is zero, so the regression's error term is just the "
            "second walk itself, minus a constant. <bookmark mark='b'/> That error is a random walk: not independent, not even "
            "stationary. <bookmark mark='c'/> The usual standard error assumes independent errors, and with errors this "
            "persistent it's far too small, the problem of chapter one, in its most extreme form. "
            "<bookmark mark='d'/> Peter Phillips proved in 1986 that the t statistic doesn't settle down to any distribution: "
            "it grows like the square root of n. More data makes the nonsense more significant, not less."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rule(self):
        d = load("spurious")
        rows = [
            cmath(r"\text{DW}", r"=", r"\frac{\sum (\hat u_t - \hat u_{t-1})^2}{\sum \hat u_t^2} \approx 2(1 - \hat\rho_1)", font_size=30),
            cmath(r"\text{independent errors}", r":", r"\text{DW} \approx 2", font_size=30),
            cmath(r"\text{random walks}", r":", rf"\text{{median DW}} = {d['median_dw']:.2f},\ \ \text{{median }} R^2 = {d['median_r2']:.2f}", font_size=30),
            cmath(r"\text{Granger \& Newbold}", r":", r"R^2 > \text{DW} \Rightarrow \text{suspect nonsense}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"Durbin \& Watson (1950)"), why(r"no autocorrelation in the residuals"),
                why(r"the residuals barely change from step to step"), why(r"a rule of thumb, \ 1974")]
        with self.voiceover(
            "There's a warning light. <bookmark mark='a'/> James Durbin and Geoffrey Watson's statistic of 1950 compares "
            "the squared changes in the residuals with their squares: roughly two times one minus their lag-one "
            "autocorrelation. <bookmark mark='b'/> Independent residuals give a value near two. <bookmark mark='c'/> In the "
            "random-walk regressions, the median is point one five: the residuals hardly change from one step to the next. "
            "<bookmark mark='d'/> Granger and Newbold's rule of thumb: when R squared exceeds the Durbin–Watson statistic, "
            "suspect a spurious regression. In our example, R squared point six eight, Durbin–Watson point four seven."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cure(self):
        d = load("spurious")
        td = np.asarray(d["t_diff"])
        e = np.linspace(-5, 5, 41)
        A = axes([-5, 5], [0, 0.45], x_length=8.6, y_length=4.0, xlabel=r"the slope's $t$, \ regressing differences on differences",
                 ylabel=r"density", xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.2, 0.4], center=[-1.4, 0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, e, np.histogram(td, e)[0] / (len(td) * 0.25), color=HIT, opacity=0.7)
        xs = np.linspace(-5, 5, 300)
        tc = curve(ax, xs, stats.t(97).pdf(xs), GREY_A, 3)
        rows = fit_rows(VGroup(
            MathTex(r"\nabla y_t = a + b\,\nabla x_t + v_t", font_size=30),
            label(r"the differences are white noise", font_size=22),
            MathTex(rf"P(|t| > 1.98) = {d['reject_diff']:.3f}", font_size=30, color=HIT),
            label(r"unless the levels are cointegrated: \ Engle \& Granger (1987), \ Part 38", font_size=20, color=GREY_A),
        ), 3.8, 0.4, [5.1, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The cure is the one Box and Jenkins used: difference. Regress the changes in one series on the "
            "changes in the other. <bookmark mark='b'/> For random walks, the differences are white noise, and the regression "
            "assumptions hold. <bookmark mark='c'/> The t statistics now follow Student's t, and five point four percent "
            "exceed the critical value, as they should. <bookmark mark='d'/> There's one important exception. Sometimes two "
            "wandering series really are tied together, so that a combination of them is stationary, like a drunk and her dog "
            "on a lead. Robert Engle and Granger developed the theory of this cointegration in 1987; it was the work for which Granger "
            "shared the 2003 Nobel prize in economics. Part 38 tests for it."
        ) as vo:
            self.play(FadeIn(A), Create(tc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.03), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=17) if r.part == 17 and r.setting.startswith("two independent")]
        b = coverage_board(rows, lit_part=17, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "The Coverage Board, ten thousand pairs of walks of a hundred. <bookmark mark='a'/> The slope's t-test in levels has "
            "a size of seventy-seven percent where five was promised: the worst row the Board has seen since the bootstrap "
            "of a maximum. <bookmark mark='b'/> In differences, five point oh percent: kept."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[1]))
        self.wait(1.0)
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"regressing one trending series on another proves nothing by itself", font_size=24),
            label(r"look at the residuals: \ Durbin--Watson far below 2 is a red flag", font_size=24, color=RES),
            label(r"difference, \ or model the dependence, \ before testing", font_size=24, color=HIT),
            label(r"Yule's marriages and deaths: \ $r = 0.95$ in levels, \ 0.02 in changes", font_size=24, color=OBS),
            label(r"the same trap: \ anything that trends correlates with anything else that trends", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: regressing one trending series on another proves nothing by itself. "
            "<bookmark mark='b'/> Look at the residuals; a Durbin–Watson statistic far below two is a red flag. "
            "<bookmark mark='c'/> Difference, or model the dependence, before believing a test. <bookmark mark='d'/> Yule's "
            "marriages and deaths showed it in 1926: point nine five in levels, point oh two in changes. "
            "<bookmark mark='e'/> The trap is everywhere. Anything that changes steadily over time correlates with anything "
            "else that does: in a famous joke, global temperatures with the falling number of pirates."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
