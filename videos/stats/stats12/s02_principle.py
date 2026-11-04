from __future__ import annotations

import numpy as np

from videos.stats.stats12.common import *  # noqa: F403


class Principle(VoiceoverScene):
    def construct(self):
        self.card()
        self.squares()
        self.normal_equations()
        self.closed_form()
        self.why_squares()
        self.gauss_derivation()
        self.lad()
        self.losses()

    def card(self):
        card = chapter_card(1, r"The principle", r"Minimize the sum of squared misses", lit=(1805,), part=PART)
        with self.voiceover("Chapter one. The principle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def squares(self):
        d = load("line")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        A = axes([-2.2, 2.2], [-2.6, 2.6], x_length=6.6, y_length=6.0, xlabel=r"mid-parent height ($z$)", ylabel=r"child ($z$)",
                 xticks=[-2, -1, 0, 1, 2], yticks=[-2, 0, 2], center=[-2.6, -0.3, 0])
        ax = A.ax
        pts = scatter(ax, x, y)
        slope = ValueTracker(-0.4)
        a0 = float(y.mean())
        xm = float(x.mean())

        def line():
            b = slope.get_value()
            a = a0 - b * xm
            return fit_line(ax, a, b, -2.2, 2.2)

        def squares():
            b = slope.get_value()
            a = a0 - b * xm
            g = VGroup()
            for xi, yi in zip(x, y):
                yh = a + b * xi
                p0, p1 = ax.c2p(xi, yi), ax.c2p(xi, yh)
                side = abs(p1[1] - p0[1])
                sq = Square(side_length=max(side, 1e-3), stroke_width=1, stroke_color=RES, fill_color=RES, fill_opacity=0.12)
                sq.move_to([p0[0] + side / 2, (p0[1] + p1[1]) / 2, 0])
                g.add(sq)
            return g

        def total():
            b = slope.get_value()
            a = a0 - b * xm
            rss = float(((y - a - b * x) ** 2).sum())
            return MathTex(rf"\textstyle\sum e_i^2 = {rss:.2f}", font_size=34, color=RES).move_to([4.2, 1.8, 0])

        ln, sq, tot = always_redraw(line), always_redraw(squares), always_redraw(total)
        rows = fit_rows(VGroup(
            label(r"each residual $e_i = y_i - (a + b x_i)$ \ as a square", font_size=24),
            label(r"turn the line: \ the total area changes", font_size=24, color=GREY_A),
            MathTex(rf"\text{{least squares: }} \hat b = {d['coef'][1]:.3f}", font_size=30, color=FIT),
            label(r"30 of the World's families \ (Part 5's Galton)", font_size=22, color=GREY_A),
        ), 5.0, 0.36, [4.3, -0.6, 0])
        tag = simulated_tag(r"the World: \ families", corner=DR)
        with self.voiceover(
            "Here's the principle in one picture. <bookmark mark='a'/> Thirty of the World's families: across, the "
            "parents' average height, and up, the adult child's, both in standard units, as in Part 5. "
            "<bookmark mark='b'/> Draw any line. Each point misses it by a vertical distance, the residual. Draw each "
            "residual as a square: its area is the residual squared. <bookmark mark='c'/> Now turn the line. The squares "
            "grow and shrink, and their total area changes. <bookmark mark='d'/> Least squares chooses the line with the "
            "smallest total area. Here, a slope of point five three: children of tall parents are taller than average, but "
            "only about half as much, Galton's regression toward the mean."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, scale=1.5) for p_ in pts], lag_ratio=0.03))
            vo.wait_until("b")
            self.add(ln, sq, tot)
            self.play(FadeIn(ln), FadeIn(sq), FadeIn(tot), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(slope.animate.set_value(1.4), run_time=3.0)
            self.play(slope.animate.set_value(0.0), run_time=3.0)
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(slope.animate.set_value(d["coef"][1]), run_time=2.5)
            self.play(FadeIn(rows[2:]))
        for m in (ln, sq, tot):
            m.clear_updaters()
        self.clear_scene()

    def normal_equations(self):
        rows = [
            cmath(r"S(a, b)", r"=", r"\sum_i (y_i - a - b x_i)^2", font_size=34),
            cmath(r"\frac{\partial S}{\partial a}", r"=", r"-2\sum_i (y_i - a - b x_i) = 0", font_size=34),
            cmath(r"\frac{\partial S}{\partial b}", r"=", r"-2\sum_i x_i (y_i - a - b x_i) = 0", font_size=34),
            cmath(r"X^\top X\,\hat\beta", r"=", r"X^\top y", r"\quad\text{the normal equations}", font_size=36),
        ]
        rows[3][0].set_color(FIT)
        whys = [why(r"a quadratic bowl in $(a, b)$"), why(r"the residuals sum to zero: \ the line passes through $(\bar x, \bar y)$"),
                why(r"the residuals are uncorrelated with $x$"), why(r"for any number of predictors: \ Legendre's equations")]
        with self.voiceover(
            "The algebra. <bookmark mark='a'/> The total squared miss is a quadratic function of the intercept and slope: "
            "a bowl. <bookmark mark='b'/> At the bottom of the bowl both derivatives vanish. The first says the residuals add "
            "up to zero, so the line passes through the point of averages. <bookmark mark='c'/> The second says the "
            "residuals are uncorrelated with x: whatever is left over has no linear relation to the predictor. "
            "<bookmark mark='d'/> With any number of predictors, written as a matrix X with a column of ones, these are "
            "the normal equations: X transpose X beta-hat equals X transpose y. Legendre wrote them down in 1805."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.7, x=-0.6, buff=0.55, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def closed_form(self):
        d = load("line")
        rows = [
            cmath(r"\hat b", r"=", r"\frac{\sum (x_i - \bar x)(y_i - \bar y)}{\sum (x_i - \bar x)^2} = r\,\frac{s_y}{s_x}", font_size=34),
            cmath(r"\hat a", r"=", r"\bar y - \hat b\,\bar x", font_size=34),
            cmath(r"\hat\beta", r"=", r"(X^\top X)^{-1}X^\top y", r"\quad\text{solved by QR, \ never by inverting (Part 4)}", font_size=32),
        ]
        rows[0][2].set_color(FIT)
        whys = [why(r"Part 5's regression slope: \ the correlation, \ rescaled"), why(r"through the point of averages"),
                why(r"\texttt{statkit.ols.fit}, \ checked against statsmodels")]
        with self.voiceover(
            "<bookmark mark='a'/> For one predictor, the solution is Part 5's regression slope: the covariance over the "
            "variance of x, which is the correlation times the ratio of standard deviations. <bookmark mark='b'/> The "
            "intercept puts the line through the point of averages. <bookmark mark='c'/> In general, beta-hat is X "
            "transpose X inverse, X transpose y, though, as Part 4 insisted, you compute it with a QR decomposition, never "
            "by forming the inverse. statkit's ordinary least squares module does exactly that, and its every output is "
            "checked against the statsmodels library."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def why_squares(self):
        rows = fit_rows(VGroup(
            label(r"why squares, \ and not absolute values, \ or the largest miss?", font_size=30, color=OBS),
            label(r"convenience: \ a smooth bowl, \ linear equations, \ a unique answer (Legendre)", font_size=24),
            label(r"probability: \ if errors are normal, \ least squares is maximum likelihood (Gauss, 1809; \ Part 9)", font_size=24),
            label(r"optimality without normality: \ the best linear unbiased estimator (Gauss, 1821; \ ch.~3)", font_size=24),
            label(r"geometry: \ the closest point in a plane, \ in ordinary distance (ch.~2)", font_size=24),
            label(r"the price: \ squares give big misses big weight, \ so outliers pull hard", font_size=24, color=RES),
        ), 12.6, 0.4, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why squares, and not absolute values, or the largest miss? There are four good answers. "
            "<bookmark mark='b'/> Convenience: squares give a smooth bowl, linear equations and a unique answer, which was "
            "Legendre's argument. <bookmark mark='c'/> Probability: if the errors are normal, least squares is maximum "
            "likelihood, which was Gauss's argument in 1809, and Part 9's. <bookmark mark='d'/> Optimality without "
            "normality: Gauss proved in 1821 that it's the best linear unbiased estimator, chapter three. "
            "<bookmark mark='e'/> And geometry: it finds the closest point in a plane in ordinary distance, chapter two. "
            "<bookmark mark='f'/> The price is that squaring gives large misses great weight, so a single outlier pulls the "
            "line hard."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lad(self):
        d = load("lad")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        A = axes([3, 15], [4, 14], x_length=7.0, y_length=4.6, xlabel=r"Anscombe's third data set", xticks=[4, 8, 12, 14],
                 yticks=[5, 10], center=[-2.4, -0.3, 0])
        ax = A.ax
        pts = scatter(ax, x, y)
        ls = fit_line(ax, d["ls"][0], d["ls"][1], 3, 15, FIT)
        la = fit_line(ax, d["lad"][0], d["lad"][1], 3, 15, S.POST)
        out = Circle(radius=0.22, color=RES).move_to(ax.c2p(13, 12.74))
        rows = fit_rows(VGroup(
            label(r"Boscovich (1757), \ then Laplace: \ minimize $\sum |e_i|$", font_size=24, color=S.POST),
            MathTex(rf"\text{{least squares: }} {d['ls'][0]:.2f} + {d['ls'][1]:.3f}\,x", font_size=28, color=FIT),
            MathTex(rf"\text{{least absolute: }} {d['lad'][0]:.2f} + {d['lad'][1]:.3f}\,x", font_size=28, color=S.POST),
            label(r"one point tilts least squares; \ the absolute-error line goes through the other ten", font_size=24, color=GREY_A),
            label(r"older than least squares, \ harder to compute; \ robust regression returns in Part 30", font_size=22, color=GREY_A),
        ), 5.0, 0.32, [4.3, -0.3, 0])
        src = historical_tag(r"Anscombe (1973)", corner=DR)
        with self.voiceover(
            "The alternative is older than least squares. <bookmark mark='a'/> In 1757 Roger Boscovich, studying the shape "
            "of the Earth, fitted lines by minimizing the sum of absolute misses, and Laplace developed the idea. "
            "<bookmark mark='b'/> Here's Anscombe's third data set: ten points on a perfect line, and one outlier. "
            "<bookmark mark='c'/> Least squares tilts toward the outlier: slope point five. <bookmark mark='d'/> The least "
            "absolute deviations line ignores it and passes exactly through the other ten: slope point three four five. "
            "<bookmark mark='e'/> It's more robust, but harder to compute and to do theory with, which is why least squares "
            "won the nineteenth century. Robust regression returns in Part 30."
        ) as vo:
            self.play(FadeIn(A), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_, scale=1.5) for p_ in pts], lag_ratio=0.05), Create(out))
            vo.wait_until("c")
            self.play(Create(ls), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Create(la), FadeIn(rows[2:4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def gauss_derivation(self):
        rows = [
            cmath(r"\text{postulate}", r":", r"\text{for repeated measurements, \ the average is the most probable value}", font_size=28),
            cmath(r"\sum_i \frac{\phi'(x_i - \mu)}{\phi(x_i - \mu)}", r"=", r"0 \ \text{ exactly when } \ \sum_i (x_i - \mu) = 0", font_size=30),
            cmath(r"\frac{\phi'(u)}{\phi(u)}", r"=", r"-k\,u", font_size=32),
            cmath(r"\phi(u)", r"\propto", r"e^{-k u^2/2}", r"\quad\text{the normal law}", font_size=34),
        ]
        rows[3][2].set_color(FIT)
        whys = [why(r"Gauss (1809): \ assume what everyone already did"), why(r"the likelihood equation for an error law $\phi$"),
                why(r"for every possible sample: \ the score must be linear"), why(r"and then maximum likelihood is least squares")]
        with self.voiceover(
            "Gauss's 1809 argument ran in a surprising direction. <bookmark mark='a'/> He postulated what every astronomer "
            "already did: when a quantity is measured several times, the average is the most probable value. "
            "<bookmark mark='b'/> If errors follow some law phi, the most probable value solves a likelihood equation, and "
            "Gauss demanded that its solution be the average, for every possible set of measurements. "
            "<bookmark mark='c'/> That forces the log-derivative of phi to be linear, <bookmark mark='d'/> so phi must be e to "
            "the minus k u squared: the normal curve. And under that law, the most probable fit of any linear model is least "
            "squares. The normal distribution entered the world as a justification for least squares, which is why it carries "
            "Gauss's name. Laplace's central limit theorem, a year later, gave the deeper reason it fits."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.6, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def losses(self):
        us = np.linspace(-3, 3, 200)
        A = axes([-3, 3], [0, 4], x_length=6.4, y_length=4.0, xlabel=r"residual $e$", ylabel=r"loss", xticks=[-3, -1, 0, 1, 3], yticks=[0, 2, 4],
                 center=[-2.8, -0.3, 0])
        ax = A.ax
        sq = clip_curve(ax, us, us ** 2, FIT, 3.5, ymax=4)
        ab = clip_curve(ax, us, np.abs(us), S.POST, 3.5, ymax=4)
        hub = clip_curve(ax, us, np.where(np.abs(us) < 1, us ** 2 / 2, np.abs(us) - 0.5), S.PRIOR, 3, ymax=4)
        leg = legend([(FIT, r"$e^2$: \ least squares \ (the mean)"), (S.POST, r"$|e|$: \ least absolute \ (the median)"),
                      (S.PRIOR, r"Huber (1964): \ squares near 0, \ absolute far out")], font_size=22).move_to([3.8, 1.6, 0])
        rows = fit_rows(VGroup(
            label(r"each loss defines a different ``centre'': \ fit a constant and you get the mean, \ the median, \ or in between", font_size=22),
            label(r"a big miss costs $e^2$ under squares: \ one outlier can dominate", font_size=22, color=RES),
            label(r"robust losses grow slowly: \ Part 30", font_size=22, color=GREY_A),
        ), 5.6, 0.3, [3.8, -1.2, 0])
        with self.voiceover(
            "It helps to see the choice as a choice of loss. <bookmark mark='a'/> Least squares charges each residual its "
            "square. Fit just a constant with this loss and you get the mean. <bookmark mark='b'/> Least absolute deviations "
            "charges the absolute value, and a constant fit gives the median. <bookmark mark='c'/> Peter Huber's 1964 loss is "
            "quadratic near zero and linear far out, a compromise between the two. <bookmark mark='d'/> The shape of the loss "
            "far from zero is what decides how much one wild point can pull: under squares, a miss twice as big costs four "
            "times as much. Part 30 builds regression on the slower-growing losses."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(sq), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(ab), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(Create(hub), FadeIn(leg[2]), FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1:]))
        self.clear_scene()
