from __future__ import annotations

import numpy as np

from videos.stats.stats13.common import *  # noqa: F403


class Optimal(VoiceoverScene):
    def construct(self):
        self.card()
        self.line()
        self.smith()
        self.criterion()
        self.search()
        self.variance_function()
        self.equivalence()
        self.caveat()

    def card(self):
        card = chapter_card(11, r"Optimal design, \ a first look", r"Where should the observations go?", part=PART)
        with self.voiceover("Chapter eleven. Optimal design, a first look."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def line(self):
        A = axes([-1.2, 1.2], [-0.5, 3.5], x_length=6.0, y_length=4.2, xlabel=r"$x$, \ the dose we may choose", ylabel=r"", xticks=[-1, 0, 1],
                 yticks=[], center=[-2.8, 0.1, 0])
        ax = A.ax
        xs_u = np.linspace(-1, 1, 10)
        xs_e = np.array([-1] * 5 + [1] * 5, float)
        uni = VGroup(*[Dot(ax.c2p(x, 2.6), radius=0.08, color=S.ALT) for x in xs_u])
        ends = VGroup(*[Dot(ax.c2p(x, 1.0 + 0.12 * (k % 5)), radius=0.08, color=OBS) for k, x in enumerate(xs_e)])
        l1 = label(r"spread evenly", font_size=22, color=S.ALT).next_to(ax.c2p(0, 2.6), UP, buff=0.2)
        l2 = label(r"half at each end", font_size=22, color=OBS).next_to(ax.c2p(0, 1.2), UP, buff=0.3)
        su = float(np.sqrt(1 / ((xs_u - xs_u.mean()) ** 2).sum()))
        se = float(np.sqrt(1 / ((xs_e - xs_e.mean()) ** 2).sum()))
        rows = fit_rows(VGroup(
            label(r"a line, \ 10 observations on $[-1, 1]$", font_size=24),
            MathTex(r"\mathrm{Var}(\hat b) = \frac{\sigma^2}{\sum_i (x_i - \bar x)^2}", font_size=32),
            MathTex(rf"\text{{even: }}\ \mathrm{{SE}} = {su:.3f}\,\sigma", font_size=28, color=S.ALT),
            MathTex(rf"\text{{ends: }}\ \mathrm{{SE}} = {se:.3f}\,\sigma", font_size=28, color=OBS),
            label(rf"ends: \ worth {(su / se) ** 2:.1f}$\times$ the observations", font_size=24, color=OBS),
            label(r"but blind to a curve", font_size=24, color=RES),
        ), 4.6, 0.36, [4.5, 0.1, 0])
        with self.voiceover(
            "Experiments also choose where to measure. <bookmark mark='a'/> Suppose we'll fit a straight line through ten "
            "observations, and we may choose the doses anywhere from minus one to one. <bookmark mark='b'/> With independent equal-variance errors, the slope's "
            "variance is sigma squared over the spread of the x's, Part 12. <bookmark mark='c'/> Spread evenly, the slope's "
            "standard error is point five oh sigma. <bookmark mark='d'/> Put half the observations at each end, and it's "
            "point three two. <bookmark mark='e'/> That's as good as two and a half times as many evenly spread observations. "
            "<bookmark mark='f'/> The catch is obvious: with all the points at two doses, you can't see whether the truth is "
            "a line at all. The best design for one model can be blind to another, a theme that runs through this chapter."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(uni, lag_ratio=0.1), FadeIn(l1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(ends, lag_ratio=0.1), FadeIn(l2), FadeIn(rows[3]))
            for k, m_ in enumerate("ef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 4]))
        self.clear_scene()

    def smith(self):
        hc = history_card(1918, r"Kirstine Smith, \ \emph{Biometrika}", r"``On the standard deviations of adjusted and interpolated values "
                          r"of an observed polynomial function \ldots \ and the guidance they give towards a proper choice of the "
                          r"distribution of observations'': \ the first optimal designs, \ for polynomials up to degree six",
                          color=S.PRIOR, width=10.6, font_size=22).move_to([0, 1.3, 0])
        rows = fit_rows(VGroup(
            label(r"a Danish statistician working in Karl Pearson's laboratory in London", font_size=24),
            label(r"her criterion: \ make the worst prediction variance over the range as small as possible", font_size=24, color=S.PRIOR),
            label(r"forty years later, \ Jack Kiefer and Jacob Wolfowitz turned the subject into a theory", font_size=24, color=OBS),
        ), 12.4, 0.3, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The first paper on optimal design was written in 1918 by Kirstine Smith, a Danish statistician "
            "working in Karl Pearson's laboratory in London. <bookmark mark='b'/> She asked where to place observations for "
            "fitting polynomials, of degrees up to six, and found the designs that make the worst prediction variance over the "
            "range as small as possible. <bookmark mark='c'/> The subject slept for forty years, until Jack Kiefer and Jacob "
            "Wolfowitz built a general theory around 1960. Let's rediscover her answer for a quadratic."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            self.play(FadeIn(rows[2], shift=RIGHT * 0.2))
        self.clear_scene()

    def criterion(self):
        d = load("doptimal")
        dets = d["dets"]
        rows = [
            cmath(r"y", r"=", r"\beta_0 + \beta_1 x + \beta_2 x^2 + \varepsilon,\qquad x \in [-1, 1]", font_size=32),
            cmath(r"\mathrm{Var}(\hat\beta)", r"=", r"\frac{\sigma^2}{n}\,M^{-1},\qquad M = \frac1n\sum_i f(x_i)f(x_i)^\top", font_size=30),
            cmath(r"\text{D-optimal}", r":", r"\max\ \det M", font_size=34),
            cmath(r"\det M", r"\propto", r"\big(\text{volume of the confidence ellipsoid}\big)^{-2}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"a quadratic dose--response"), why(r"$f(x) = (1, x, x^2)$: \ $M$ is the information per observation"),
                why(r"one number to compare designs"), why(r"small ellipsoid: \ all three coefficients pinned down")]
        with self.voiceover(
            "<bookmark mark='a'/> The model: a quadratic in x, with x anywhere from minus one to one. <bookmark mark='b'/> The "
            "coefficients' covariance is sigma squared over n times the inverse of M, the information matrix per observation, "
            "built from the vectors one, x, x squared at the design points; the design has full column rank and independent equal-variance errors. A good design makes M large. But M is a matrix: "
            "large in what sense? <bookmark mark='c'/> The most popular answer: make its determinant as large as possible. "
            "That's D-optimality, D for determinant. <bookmark mark='d'/> The determinant measures the volume of the joint "
            "confidence ellipsoid for all three coefficients: the bigger det M, the smaller the ellipsoid."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        del dets
        self.clear_scene()

    def search(self):
        d = load("doptimal")
        A = axes([-0.95, 0.95], [0, 0.16], x_length=5.4, y_length=3.6, xlabel=r"position of the middle point $m$", ylabel=r"$\det M$",
                 xticks=[-0.5, 0, 0.5], yticks=[0, 0.05, 0.1, 0.15], center=[-3.4, 0.4, 0])
        B = axes([0, 0.5], [0, 0.16], x_length=5.0, y_length=3.6, xlabel=r"weight $w$ on each end", ylabel=r"", xticks=[0, 1 / 6, 1 / 3, 0.5],
                 yticks=[0, 0.05, 0.1, 0.15], center=[3.3, 0.4, 0], xfmt=lambda v: {0: "0", 1 / 6: "1/6", 1 / 3: "1/3", 0.5: "1/2"}.get(v, f"{v:.2f}"))
        c1 = curve(A.ax, np.asarray(d["mids"]), np.asarray(d["det_mid"]), OBS, 3)
        c2 = curve(B.ax, np.asarray(d["ws"]), np.asarray(d["det_ws"]), S.ALT, 3)
        m1 = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, 4 / 27), color=EXACT, stroke_width=2)
        m2 = DashedLine(B.ax.c2p(1 / 3, 0), B.ax.c2p(1 / 3, 4 / 27), color=EXACT, stroke_width=2)
        t1 = label(r"points at $-1, \ m, \ 1$", font_size=22, color=OBS).next_to(A, UP, buff=0.1)
        t2 = label(r"$w$ at $\pm1$, \ $1 - 2w$ at 0", font_size=22, color=S.ALT).next_to(B, UP, buff=0.1)
        foot = fit_rows(VGroup(
            label(r"best: \ the middle point exactly in the middle, \ and a third of the observations at each of $-1, 0, 1$", font_size=24, color=EXACT),
            MathTex(rf"\det M = 4/27 = {4 / 27:.3f}\quad\text{{vs}}\quad\text{{21 evenly spaced points: }} {d['dets']['uniform 21']:.3f}", font_size=28),
        ), 12.6, 0.24, [0, -2.6, 0])
        with self.voiceover(
            "Search for it. <bookmark mark='a'/> Put the design's points at minus one, at one, and at a middle point m, a third "
            "of the observations each, and slide m. The determinant peaks with m exactly at zero. <bookmark mark='b'/> Now "
            "keep the points at minus one, zero and one, and vary how the observations are shared: a fraction w at each end, "
            "the rest in the middle. The peak is at w equals one third. <bookmark mark='c'/> So the D-optimal design for a "
            "quadratic puts a third of the observations at each end and a third in the middle. Its determinant is four over "
            "twenty-seven, point one four eight. <bookmark mark='d'/> Twenty-one evenly spaced points give point zero three nine, "
            "less than a third as much: the familiar even spread wastes most of its observations in places that tell us little."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(t1), Create(c1), run_time=2.0)
            self.play(Create(m1))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(t2), Create(c2), run_time=2.0)
            self.play(Create(m2))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def variance_function(self):
        d = load("doptimal")
        xs = np.asarray(d["xs"])
        A = axes([-1, 1], [0, 8], x_length=7.0, y_length=4.2, xlabel=r"$x$", ylabel=r"$d(x) = n\,\mathrm{Var}(\hat y(x))/\sigma^2$",
                 xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, 3, 6], center=[-2.4, 0.2, 0])
        ax = A.ax
        cu = curve(ax, xs, np.asarray(d["varfun"]["uniform 21"]), S.ALT, 3)
        ct = curve(ax, xs, np.asarray(d["varfun"]["thirds"]), OBS, 4)
        p3 = DashedLine(ax.c2p(-1, 3), ax.c2p(1, 3), color=EXACT, stroke_width=2)
        p3l = label(r"$p = 3$", font_size=22, color=EXACT).next_to(ax.c2p(1, 3), RIGHT, buff=0.1)
        sup = VGroup(*[Dot(ax.c2p(x, 3), radius=0.09, color=OBS) for x in (-1, 0, 1)])
        rows = fit_rows(VGroup(
            label(r"prediction variance across $x$", font_size=24),
            label(rf"even spread: \ worst {max(d['varfun']['uniform 21']):.1f}, \ at the ends", font_size=24, color=S.ALT),
            label(r"thirds: \ worst exactly 3", font_size=24, color=OBS),
            label(r"touched at $-1$, \ 0, \ 1", font_size=24, color=OBS),
            label(r"and 3 is the number of parameters", font_size=24, color=EXACT),
        ), 4.6, 0.36, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Kirstine Smith looked at a different quantity: how precise the fitted curve is at each x, "
            "the prediction variance, scaled so designs of any size compare. <bookmark mark='b'/> For the even spread, it's "
            "worst at the ends, seven and a half, where the even design has few neighbouring points to lean on. "
            "<bookmark mark='c'/> For the thirds design, it never exceeds three, and touches three exactly at the design points, "
            "minus one, zero and one. <bookmark mark='d'/> And three is the number of parameters. That's not a coincidence."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cu), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ct), FadeIn(sup), FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(Create(p3), FadeIn(p3l), FadeIn(rows[4]))
        self.clear_scene()

    def equivalence(self):
        rows = [
            cmath(r"d(x, \xi)", r"=", r"f(x)^\top M(\xi)^{-1} f(x)", font_size=34),
            cmath(r"\int d(x, \xi)\, \xi(dx)", r"=", r"\mathrm{tr}\big(M^{-1}M\big) = p\quad\text{for nonsingular }M", font_size=30),
            cmath(r"\xi^*\ \text{D-optimal}", r"\iff", r"\max_x d(x, \xi^*) = p", font_size=34),
            cmath(r"\text{D-optimal}", r"=", r"\text{G-optimal (Smith's criterion)}", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"the variance function of design $\xi$"), why(r"so its average over the design is always $p$"),
                why(r"Kiefer \& Wolfowitz (1960): \ the equivalence theorem"), why(r"two criteria, \ one design")]
        with self.voiceover(
            "<bookmark mark='a'/> Write the variance function as f transpose M inverse f. <bookmark mark='b'/> Averaged over the "
            "design's own points, it's the trace of M inverse times M: always p, the number of parameters, for any design "
            "with nonsingular information. So the maximum can't be less than p. <bookmark mark='c'/> Kiefer and Wolfowitz's equivalence theorem of "
            "1960, for approximate designs with freely chosen probability weights on a compact design space: a design is D-optimal exactly when its maximum is p, reached at its support points. <bookmark mark='d'/> So "
            "maximizing the determinant, a statement about the coefficients, and minimizing the worst prediction variance, "
            "Smith's 1918 criterion, give the same design. It also gives a practical check: compute the variance function, "
            "and if it ever exceeds p, moving weight toward that x can improve the approximate design. An exact finite-run design must also respect integer allocation constraints."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def caveat(self):
        rows = fit_rows(VGroup(
            label(r"other criteria: \ A (average variance), \ E (worst direction), \ I (average prediction variance)", font_size=24),
            label(r"the design is optimal for the model you assumed", font_size=26, color=OBS),
            label(r"thirds at $-1, 0, 1$ cannot detect a cubic: \ add a few points to test lack of fit", font_size=24, color=RES),
            label(r"Box \& Draper (1959): \ bias from the wrong model often matters more than variance", font_size=24),
            label(r"designs that adapt to the data as they arrive: \ Part 58", font_size=22, color=GREY_A),
        ), 12.4, 0.44, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> There are other criteria: A for the average variance of the coefficients, E for the worst "
            "direction, I for the average prediction variance. They often agree roughly, and the theory handles them all. "
            "<bookmark mark='b'/> The real caution is that a design is optimal for the model you assumed. <bookmark mark='c'/> "
            "Three support points can fit a quadratic exactly; they can't reveal a cubic. Practical designs add a few points "
            "to test for lack of fit. <bookmark mark='d'/> George Box and Norman Draper argued in 1959 that the bias from "
            "fitting the wrong model often matters more than the variance an optimal design minimizes. <bookmark mark='e'/> "
            "For nonlinear models the best design depends on the unknown parameters themselves, which suggests choosing each "
            "observation from the data so far. Adaptive designs, and the care their inference needs, come back in Part 58."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
