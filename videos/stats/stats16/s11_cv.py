from __future__ import annotations

import numpy as np

from videos.stats.stats16.common import *  # noqa: F403


class CrossValidation(VoiceoverScene):
    def construct(self):
        self.card()
        self.fits()
        self.folds()
        self.curves()
        self.optimism()
        self.loo()
        self.cautions()

    def card(self):
        card = chapter_card(10, r"Cross-validation", r"How well will it predict data it hasn't seen?", part=PART)
        with self.voiceover("Chapter ten. Cross-validation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def fits(self):
        d = load("cv")
        age, y = np.asarray(d["age"]), np.asarray(d["y"])
        x = (age - 45) / 15
        A = axes([18, 70], [9, 12.5], x_length=7.6, y_length=4.4, xlabel=r"age", ylabel=r"log income", xticks=[20, 30, 40, 50, 60, 70],
                 yticks=[9, 10, 11, 12], center=[-2.0, 0.3, 0])
        ax = A.ax
        dots = scatter(ax, age, y, radius=0.045, opacity=0.6)
        ga = np.linspace(18, 69, 200)
        gx = (ga - 45) / 15
        curves = VGroup()
        for deg, col in ((1, S.ALT), (3, FIT), (8, RES)):
            c = np.polyfit(x, y, deg)
            curves.add(polyline(ax, ga, np.polyval(c, gx), col, 3.5))
        rows = fit_rows(VGroup(
            label(r"200 adults from the World, \ under 70", font_size=22),
            label(r"degree 1: \ a straight line", font_size=22, color=S.ALT),
            label(r"degree 3: \ rises, \ then flattens", font_size=22, color=FIT),
            label(r"degree 8: \ wiggles at the ends", font_size=22, color=RES),
            label(r"which will predict new people best?", font_size=24, color=OBS),
        ), 4.4, 0.36, [4.7, 0.3, 0])
        tag = simulated_tag(r"the World: \ 200 adults", corner=DR)
        with self.voiceover(
            "The bootstrap and jackknife resample to measure uncertainty. Cross-validation holds data out to measure "
            "prediction. <bookmark mark='a'/> Two hundred adults from the World: log income against age. "
            "<bookmark mark='b'/> A straight line. <bookmark mark='c'/> A cubic, which rises and then flattens, as incomes do "
            "over a career. <bookmark mark='d'/> A polynomial of degree eight, which wiggles at the ends where data are thin. "
            "<bookmark mark='e'/> The higher the degree, the smaller the training error: a more flexible curve always fits "
            "the points it was fitted to at least as well. But which will predict the incomes of new people best?"
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(Create(curves[k]), FadeIn(rows[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def folds(self):
        n_show = 50
        cell = 0.22
        g = np.random.Generator(np.random.PCG64(10))
        perm = g.permutation(n_show)
        fold_of = np.empty(n_show, int)
        fold_of[perm] = np.arange(n_show) % 10
        cols = [TRT[0], TRT[1], TRT[2], TRT[3], TRT[4], S.ALT, S.FIT, S.TRUTH, S.ACCENT, S.WORLD]
        squares = VGroup(*[Square(cell, stroke_width=1, stroke_color="#101418", fill_color=GREY_D, fill_opacity=0.9)
                           .move_to([(i - n_show / 2 + 0.5) * cell, 1.8, 0]) for i in range(n_show)])
        lab = label(r"the data (50 of the 200 shown)", font_size=20, color=GREY_B).next_to(squares, UP, buff=0.2)
        rows = [
            cmath(r"\text{split into } K = 10 \text{ folds}", r":", r"\text{at random}", font_size=30),
            cmath(r"\text{for } k = 1, \ldots, K", r":", r"\text{fit without fold } k;\ \text{predict fold } k", font_size=30),
            cmath(r"\text{CV}", r"=", r"\frac1n \textstyle\sum_i \big(y_i - \hat f^{(-k(i))}(x_i)\big)^2", font_size=30),
        ]
        whys = [why(r"each point in exactly one fold"), why(r"every prediction is for data the fit didn't see"),
                why(r"an honest estimate of prediction error")]
        with self.voiceover(
            "<bookmark mark='a'/> Cross-validation answers by pretending some of the data are new. Split the data at random "
            "into ten folds. <bookmark mark='b'/> Hold out the first fold, fit the curve to the other nine, and predict the "
            "held-out points. Then the second fold, and so on, so that every observation is predicted exactly once, by a fit "
            "that never saw it. <bookmark mark='c'/> The average squared error of those predictions estimates how well the "
            "method predicts new data. Mervyn Stone and Seymour Geisser set out the idea in 1974 and 1975; it's the jackknife's "
            "leave-out logic, aimed at prediction."
        ) as vo:
            self.play(FadeIn(squares), FadeIn(lab))
            step = ladder(self, rows, whys, keep=3, top=0.4, x=-0.6, buff=0.65, edge=6.9)
            vo.wait_until("a")
            self.play(*[squares[i].animate.set_fill(cols[fold_of[i]], 0.9) for i in range(n_show)])
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            for k in range(10):
                rt = 0.5 if k < 2 else 0.2
                self.play(*[squares[i].animate.set_opacity(1.0 if fold_of[i] == k else 0.25) for i in range(n_show)], run_time=rt)
            self.play(*[squares[i].animate.set_opacity(0.9) for i in range(n_show)], run_time=0.3)
            vo.wait_until("c")
            step(2, transform=False)
        self.clear_scene()

    def curves(self):
        d = load("cv")
        tr, cv = np.asarray(d["train"]), np.asarray(d["cv"])
        deg = np.arange(1, 9)
        A = axes([0.5, 8.5], [0.315, 0.36], x_length=8.0, y_length=4.4, xlabel=r"polynomial degree", ylabel=r"mean squared error",
                 xticks=list(range(1, 9)), yticks=[0.32, 0.33, 0.34, 0.35, 0.36], center=[-1.6, 0.3, 0],
                 yfmt=lambda v: f"{v:.2f}")
        ax = A.ax
        ct = polyline(ax, deg, tr, S.ALT, 3.5)
        cc = polyline(ax, deg, cv, OBS, 3.5)
        dt = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=S.ALT) for a, b in zip(deg, tr)])
        dc = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=OBS) for a, b in zip(deg, cv)])
        best = Circle(radius=0.2, color=HIT, stroke_width=3).move_to(ax.c2p(d["best"], cv[d["best"] - 1]))
        rows = fit_rows(VGroup(
            label(r"training error: \ falls every time", font_size=22, color=S.ALT),
            label(r"10-fold CV: \ falls, \ then rises", font_size=22, color=OBS),
            MathTex(rf"\text{{best: degree }} {d['best']},\ \ \text{{CV}} = {cv[d['best'] - 1]:.4f}", font_size=26, color=HIT),
            label(r"averaged over 5 random splits", font_size=20, color=GREY_A),
        ), 4.2, 0.36, [4.8, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are the two errors for polynomials of degree one to eight. The training error falls "
            "every time the degree goes up. <bookmark mark='b'/> The cross-validated error falls at first, while the curve "
            "learns the real shape of the career, then rises, as the extra flexibility fits noise that new people won't share. "
            "<bookmark mark='c'/> It's smallest at degree three. <bookmark mark='d'/> The differences are small, so the "
            "cross-validation was repeated over five random splits into folds and averaged: CV has its own randomness, which "
            "a single split can mislead you with."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(ct), FadeIn(dt), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cc), FadeIn(dc), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(best), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def optimism(self):
        d = load("cv")
        tr, cv = np.asarray(d["train"]), np.asarray(d["cv"])
        s2 = tr[2] * 200 / (200 - 4)
        rows = [
            cmath(r"E[\text{test error}] - E[\text{training error}]", r"\approx", r"\frac{2\sigma^2 p}{n}", font_size=30),
            cmath(r"\sigma^2 \approx", r"\ ", rf"{s2:.3f};\ \ \ n = 200", font_size=30),
            cmath(r"\text{degree 3}", r":", rf"{tr[2]:.4f} + \frac{{2 \cdot {s2:.3f} \cdot 4}}{{200}} = {tr[2] + 2 * s2 * 4 / 200:.4f}\ \ (\text{{CV}}\ {cv[2]:.4f})", font_size=28),
            cmath(r"\text{degree 8}", r":", rf"{tr[7]:.4f} + \frac{{2 \cdot {s2:.3f} \cdot 9}}{{200}} = {tr[7] + 2 * s2 * 9 / 200:.4f}\ \ (\text{{CV}}\ {cv[7]:.4f})", font_size=28),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"same-design fresh responses; \ homoskedastic linear errors"), why(r"from the cubic's residuals"),
                why(r"$p = 4$ coefficients"), why(r"$p = 9$: \ the formula and CV agree")]
        with self.voiceover(
            "Why does the training error mislead? <bookmark mark='a'/> For a fixed full-rank linear model with homoskedastic errors, compare fresh responses at the same design: on average the "
            "training error is too small by two sigma squared p over n, where p is the number of coefficients. Colin Mallows "
            "built his C-p criterion on it in 1973, and Part 19 will derive it. <bookmark mark='b'/> The cubic's residuals give "
            "sigma squared about point three three. <bookmark mark='c'/> For the cubic, four coefficients: training error plus "
            "the optimism is point three three nine, near the cross-validated point three four two. <bookmark mark='d'/> For "
            "degree eight, nine coefficients: point three four nine against cross-validation's point three five four. Cross-"
            "validation finds the optimism by brute force, with no formula, and so it works where no formula exists: trees, "
            "neural networks, anything that predicts."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def loo(self):
        rows = [
            cmath(r"K = n", r":", r"\text{leave-one-out}", font_size=32),
            cmath(r"\text{for least squares}", r":", r"y_i - \hat y^{(-i)}_i = \frac{y_i - \hat y_i}{1 - h_{ii}}", font_size=32),
            cmath(r"\text{LOOCV}", r"=", r"\frac1n \textstyle\sum_i \Big(\frac{e_i}{1 - h_{ii}}\Big)^2", font_size=32),
            cmath(r"K = 5 \text{ or } 10", r":", r"\text{a common cost, bias and variance compromise}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"the jackknife's scheme"), why(r"Part 12's leverage: \ no refitting needed"),
                why(r"Allen's PRESS (1974): \ one fit, \ $n$ predictions"), why(r"the usual choice")]
        with self.voiceover(
            "<bookmark mark='a'/> With as many folds as observations, cross-validation is leave-one-out: the jackknife's "
            "scheme. <bookmark mark='b'/> For least squares, when every deleted design has full rank and leverage is below one, it needs no refitting. The prediction error for a point "
            "left out is its ordinary residual divided by one minus its leverage, Part 12's h-i-i: high-leverage points pull the "
            "fit towards themselves, so their residuals understate their prediction errors. <bookmark mark='c'/> The whole "
            "leave-one-out error comes from one fit. David Allen called it PRESS, the prediction sum of squares, in 1974. "
            "<bookmark mark='d'/> In general, though, five or ten folds are the usual choice: fits on ninety percent of the data "
            "can differ from fits on all the data. The bias and variance trade-off depends on the learning method and data; fewer folds are cheaper, not universally less variable."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cautions(self):
        rows = fit_rows(VGroup(
            label(r"CV estimates the error of a \emph{procedure}, \ fitted to data like these", font_size=24),
            label(r"the minimum of many CV scores is optimistic: \ selection again (Part 10)", font_size=24, color=RES),
            label(r"to report the error of a tuned model, \ tune inside the folds: \ nested CV", font_size=24, color=OBS),
            label(r"folds must respect the structure: \ whole clusters, \ blocks of time", font_size=24, color=RES),
            label(r"Part 19: \ prediction, \ bias and variance, \ and model choice in full", font_size=24, color=GREY_A),
        ), 12.4, 0.46, [0, 0, 0])
        intro = label('Validation must match how predictions will be used', font_size=36)
        with self.voiceover(
            "Some cautions. <bookmark mark='a'/> Cross-validation estimates how well a procedure performs on data like these, "
            "not the error of the one fitted curve. <bookmark mark='b'/> If you try many models and report the smallest "
            "cross-validated error, that minimum is optimistic, the selection problem from Part 10 once more. "
            "<bookmark mark='c'/> To report honestly, the choosing must happen inside each fold: nested cross-validation. "
            "<bookmark mark='d'/> And the folds must respect the data's structure, as the bootstrap's resamples must: hold out "
            "whole clusters, or blocks of time, never single points from them. <bookmark mark='e'/> Part 19 takes prediction "
            "and model choice up in full."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
