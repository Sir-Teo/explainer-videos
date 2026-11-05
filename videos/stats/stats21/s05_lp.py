from __future__ import annotations

import numpy as np

from videos.stats.stats21.common import *  # noqa: F403


class LinearProgramming(VoiceoverScene):
    def construct(self):
        self.card()
        self.boscovich()
        self.arcs()
        self.as_lp()
        self.interior()
        self.check()
        self.engel()
        self.summary()

    def card(self):
        card = chapter_card(4, r"Linear programming", r"Absolute deviations and quantiles", part=PART)
        with self.voiceover("Chapter four. Linear programming in statistics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def boscovich(self):
        hc = history_card(1757, r"Roger Boscovich, \ Rome",
                          r"is the Earth flattened at the poles, \ as Newton said? \ Five measurements of the length of a degree "
                          r"of meridian, \ from Quito to Lapland, \ and a line to fit them, \ minimizing the sum of absolute errors",
                          color=PATH, width=11.0, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"half a century before least squares (Legendre 1805)", font_size=24),
            label(r"least absolute deviations: \ robust, \ but with no formula", font_size=24, color=RES),
            label(r"its algorithm is a linear program", font_size=24, color=PATH),
        ), 12.0, 0.35, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The oldest optimization problem in statistics is older than least squares. In 1757 Roger "
            "Boscovich, a Jesuit astronomer in Rome, wanted to know whether the Earth is flattened at the poles, as Newton "
            "predicted. If it is, a degree of latitude is longer near the poles. He had five measurements, from Quito to "
            "Lapland, and fitted a line by making the sum of the absolute errors as small as possible. "
            "<bookmark mark='b'/> That was nearly fifty years before Legendre published least squares. <bookmark mark='c'/> "
            "Least absolute deviations resists outliers, but has no formula. <bookmark mark='d'/> Its solution is a linear "
            "program."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def arcs(self):
        d = load("lad")
        s2, arc = np.asarray(d["s2"]), np.asarray(d["arc"])
        A = axes([-0.05, 0.95], [56600, 57500], x_length=7.4, y_length=4.4, xlabel=r"$\sin^2(\text{latitude})$",
                 ylabel=r"toises per degree", xticks=[0, 0.25, 0.5, 0.75], yticks=[56600, 56900, 57200, 57500],
                 center=[-2.0, 0.3, 0], yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"))
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.09, color=PATH) for a, b in zip(s2, arc)])
        names = VGroup(*[label(n, font_size=18, color=GREY_A).next_to(dt, UP if k != 2 else DOWN, buff=0.12) for k, (n, dt) in enumerate(zip(d["names"], dots))])
        ls, lad = d["ls"], d["lad"]
        lsl = Line(ax.c2p(-0.05, ls[0] - 0.05 * ls[1]), ax.c2p(0.95, ls[0] + 0.95 * ls[1]), color=NEWT, stroke_width=3)
        ladl = Line(ax.c2p(-0.05, lad[0] - 0.05 * lad[1]), ax.c2p(0.95, lad[0] + 0.95 * lad[1]), color=RES, stroke_width=3.5)
        rows = fit_rows(VGroup(
            label(r"model: \ arc $= a + b \sin^2(\text{lat})$", font_size=22),
            label(rf"blue: \ least squares, \ $b = {ls[1]:.0f}$", font_size=22, color=NEWT),
            label(rf"red: \ least absolute deviations, \ $b = {lad[1]:.0f}$", font_size=22, color=RES),
            label(r"the LAD line passes through two points: \ Quito and Lapland", font_size=22, color=PATH),
            label(rf"absolute errors: \ {d['lad_sum']:.0f} vs {d['ls_sum']:.0f}", font_size=22),
            label(r"$b > 0$: \ longer degrees toward the poles: \ flattened", font_size=22, color=HIT),
        ), 4.4, 0.36, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are Boscovich's five arcs, in toises per degree, against the squared sine of the "
            "latitude, which makes the theory a straight line. <bookmark mark='b'/> The least-squares line, in blue, has "
            "slope seven hundred and twenty-five. <bookmark mark='c'/> The least-absolute-deviations line, in red, has slope "
            "eight hundred, <bookmark mark='d'/> and it passes exactly through two of the five points, Quito and Lapland. "
            "That's no accident: <bookmark mark='e'/> an LAD fit with two parameters always passes through two data points, "
            "and its total absolute error, three hundred and twenty-seven, beats least squares' three hundred and forty-nine. "
            "<bookmark mark='f'/> Either way, the degrees lengthen toward the poles. Newton was right."
        ) as vo:
            self.add(historical_tag(r"Boscovich (1757), \ via Stigler (1986)", corner=DR))
            self.play(FadeIn(A), LaggedStart(*[FadeIn(x, scale=1.5) for x in dots], lag_ratio=0.2), FadeIn(names), FadeIn(rows[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(lsl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ladl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Indicate(dots[0], color=RES, scale_factor=1.8), Indicate(dots[4], color=RES, scale_factor=1.8), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def as_lp(self):
        rows = [
            cmath(r"\min_{b}", r"", r"\textstyle\sum_i |y_i - x_i'b|", font_size=30),
            cmath(r"\text{as an LP}", r":", r"\min_{b, u, v} \textstyle\sum_i (u_i + v_i) \ \ \text{s.t.} \ \ y - Xb = u - v, \ u, v \ge 0", font_size=28),
            cmath(r"\text{vertices}", r":", r"\text{fits through } p \text{ of the } n \text{ points}", font_size=28),
            cmath(r"\text{algorithms}", r":", r"\text{Laplace (1793), \ Edgeworth (1887), \ Barrodale \& Roberts (1973)}", font_size=26),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"not differentiable"), why(r"split each residual into its positive and negative parts"),
                why(r"so the simplex method visits fits through points"), why(r"a simplex for LAD; \ interior points today")]
        with self.voiceover(
            "<bookmark mark='a'/> Why a linear program? The sum of absolute residuals has a kink at every data point, so "
            "calculus fails. <bookmark mark='b'/> But split each residual into a positive part u and a negative part v: the "
            "problem becomes minimizing the sum of u plus v, subject to linear equalities and signs, which is linear. "
            "<bookmark mark='c'/> The vertices of this LP are fits passing through p of the data points, which is why "
            "Boscovich's line hit two. <bookmark mark='d'/> Laplace found an algorithm for the two-parameter case in 1793, "
            "Edgeworth generalized it, and Barrodale and Roberts built a fast simplex method for it in 1973; modern solvers use "
            "interior-point methods."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def interior(self):
        rows = [
            cmath(r"\text{simplex}", r":", r"\text{fast in practice; \ exponential in the worst case}", font_size=28),
            cmath(r"\text{Klee--Minty (1972)}", r":", r"\text{a squashed cube: \ all } 2^n \text{ corners visited}", font_size=28),
            cmath(r"\text{Karmarkar (1984)}", r":", r"\text{interior points: \ polynomial time}", font_size=28),
            cmath(r"\text{quantile regression}", r":", r"\text{Portnoy \& Koenker (1997): \ interior points win for large } n", font_size=26),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"it walks the edges"), why(r"a polytope built to fool Dantzig's rule"),
                why(r"cut through the middle, \ following a central path"), why(r"the method in modern software")]
        with self.voiceover(
            "<bookmark mark='a'/> A curious fact about the simplex method: it's fast on almost every problem anyone meets, yet "
            "it can be exponentially slow. <bookmark mark='b'/> Victor Klee and George Minty built a squashed cube in 1972 on "
            "which Dantzig's rule visits every one of its two to the n corners. <bookmark mark='c'/> In 1984 Narendra "
            "Karmarkar found a method guaranteed to take polynomial time, which travels through the interior of the polytope "
            "instead of along its edges. <bookmark mark='d'/> For large quantile regressions, Stephen Portnoy and Roger Koenker "
            "showed in 1997 that interior-point methods beat the simplex handily, and that's what modern software uses."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def check(self):
        A = axes([-2, 2], [0, 1.8], x_length=6.0, y_length=3.6, xlabel=r"residual $r$", ylabel=r"$\rho_\tau(r)$",
                 xticks=[-2, -1, 0, 1, 2], yticks=[0, 1], center=[-2.6, 0.4, 0])
        ax = A.ax
        cols = {0.5: RES, 0.9: PATH, 0.1: NEWT}
        lines = VGroup()
        for tau, c in cols.items():
            lines.add(polyline(ax, [-2, 0, 2], [2 * (1 - tau), 0, 2 * tau], c, 3.5))
        rows = fit_rows(VGroup(
            label(r"$\rho_\tau(r) = r\,(\tau - 1\{r < 0\})$", font_size=26),
            label(r"red: \ $\tau = 0.5$, \ the absolute value (halved)", font_size=22, color=RES),
            label(r"gold: \ $\tau = 0.9$: \ under-predicting costs 9 times more; \ blue: \ $\tau = 0.1$", font_size=22, color=PATH),
            label(r"$\arg\min_\theta \sum_i \rho_\tau(x_i - \theta)$ \ = \ the $\tau$ quantile", font_size=22, color=TRUE),
            label(r"Koenker \& Bassett (1978): \ quantile regression", font_size=22, color=GREY_A),
        ), 5.4, 0.42, [3.6, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Tilt the absolute value and you get every quantile. The check function charges tau times a "
            "positive residual and one minus tau times a negative one. <bookmark mark='b'/> At tau one half it's half the "
            "absolute value, and its minimizer is the median. <bookmark mark='c'/> At tau point nine, under-predicting costs "
            "nine times as much as over-predicting, so the minimizer moves up until ninety percent of the data lie below it: the "
            "ninetieth percentile. <bookmark mark='d'/> Minimizing the check loss gives the tau quantile, <bookmark mark='e'/> "
            "and minimizing it over regression lines gives Roger Koenker and Gilbert Bassett's quantile regression, from 1978, "
            "still a linear program."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lines[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(lines[1]), Create(lines[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def engel(self):
        d = load("lad")
        inc, food = np.asarray(d["income"]) / 1000, np.asarray(d["food"]) / 1000
        A = axes([0, 3.2], [0, 2.0], x_length=7.4, y_length=4.6, xlabel=r"household income, \ 1,000 francs",
                 ylabel=r"food spending, \ 1,000 francs", xticks=[0, 1, 2, 3], yticks=[0, 0.5, 1, 1.5, 2], center=[-2.0, 0.2, 0])
        ax = A.ax
        m = (inc < 3.2) & (food < 2)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=GREY_A, fill_opacity=0.7) for a, b in zip(inc[m], food[m])])
        cols = [NEWT, TEAL, RES, PATH, HIT]
        qls = VGroup()
        for tau, c in zip(d["taus"], cols):
            b = d["qr"][str(tau)]
            qls.add(Line(ax.c2p(0.2, (b[0] + 0.2 * b[1]) / 1000), ax.c2p(3.2, (b[0] + 3.2 * b[1]) / 1000), color=c, stroke_width=3))
        ob = d["ols"]
        oll = DashedLine(ax.c2p(0.2, (ob[0] + 0.2 * ob[1]) / 1000), ax.c2p(3.2, (ob[0] + 3.2 * ob[1]) / 1000), color=WHITE, stroke_width=2)
        sl = [d["qr"][str(t)][1] / 1000 for t in d["taus"]]
        rows = fit_rows(VGroup(
            label(r"Engel (1857): \ 235 Belgian households", font_size=22),
            label(r"lines: \ quantiles 0.1, \ 0.25, \ 0.5, \ 0.75, \ 0.9", font_size=22, color=PATH),
            label(rf"slopes: \ {sl[0]:.2f} to {sl[-1]:.2f} per franc of income", font_size=22),
            label(r"they fan out: \ spread grows with income", font_size=22, color=RES),
            label(r"all below 1: \ the food share falls, \ Engel's law", font_size=22, color=HIT),
            label(r"dashed: \ least squares, \ pulled by the rich", font_size=20, color=GREY_A),
        ), 4.4, 0.4, [4.6, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The classic example: Ernst Engel's two hundred and thirty-five Belgian working-class "
            "households of 1857, their income and what they spent on food. <bookmark mark='b'/> Five quantile regression "
            "lines, each a linear program: the tenth, twenty-fifth, fiftieth, seventy-fifth and ninetieth percentiles of food "
            "spending at each income. <bookmark mark='c'/> Their slopes rise from point four zero to point six nine: "
            "<bookmark mark='d'/> the lines fan out, because spending varies more among richer households, something a single "
            "least-squares line hides. <bookmark mark='e'/> All the slopes are below one, so the share of income spent on food "
            "falls as income rises: Engel's law. <bookmark mark='f'/> The least-squares line, dashed, is pulled toward the few "
            "richest households."
        ) as vo:
            self.add(historical_tag(r"Engel (1857), \ via Koenker \& Bassett", corner=DR))
            self.play(FadeIn(A), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.005), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(q) for q in qls], lag_ratio=0.3), FadeIn(rows[1]), run_time=2.5)
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
            vo.wait_until("f")
            self.play(Create(oll), FadeIn(rows[5]))
        self.clear_scene()

    def summary(self):
        rows = fit_rows(VGroup(
            label(r"LAD and quantile regression: \ linear programs", font_size=24, color=PATH),
            label(r"solutions interpolate $p$ points; \ the simplex walks between such fits", font_size=24),
            label(r"robust to outliers in $y$, \ not in $x$ (Part 30)", font_size=24, color=RES),
            label(r"quantiles describe the whole conditional distribution", font_size=24, color=HIT),
            label(r"their standard errors: \ the density at the quantile, \ Part 47", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So least absolute deviations and quantile regression are linear programs, <bookmark mark='b'/> "
            "whose solutions pass through p data points. <bookmark mark='c'/> They resist outliers in the response, though not "
            "in the predictors, which is Part 30's subject. <bookmark mark='d'/> Together, quantile regressions describe the "
            "whole conditional distribution, not just its mean. <bookmark mark='e'/> Their standard errors involve the density "
            "at the quantile, which Part 47's asymptotics will explain."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
