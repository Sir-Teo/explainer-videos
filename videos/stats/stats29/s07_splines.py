from __future__ import annotations

import numpy as np

from videos.stats.stats29.common import *  # noqa: F403


class Splines(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.theorem()
        self.reinsch()
        self.fits()
        self.spectrum()
        self.ridge()

    def card(self):
        card = chapter_card(6, r"Smoothing splines", r"The smoothest curve that fits", lit=(1967,), part=PART)
        with self.voiceover("Chapter six. Smoothing splines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"\min_g", r"\ ", r"\textstyle\sum_i (y_i - g(x_i))^2 + \lambda \int g''(t)^2\, dt", font_size=30),
            cmath(r"\lambda \to 0", r":", r"\text{interpolation at distinct $x$; \ averages at ties}", font_size=30),
            cmath(r"\lambda \to \infty", r":", r"g'' = 0: \ \text{the least-squares line}", font_size=30),
            cmath(r"\text{search}", r":", r"\text{over } g \text{ with square-integrable weak }g''", font_size=30),
        ]
        rows[0][2].set_color(SPLC)
        whys = [why(r"fit plus a roughness penalty"), why(r"the $\lambda\downarrow0$ limit"), why(r"lines cost nothing"),
                why(r"an infinite-dimensional problem")]
        with self.voiceover(
            "<bookmark mark='a'/> Instead of a local average, penalize roughness. Among all curves, minimize the "
            "residual sum of squares plus lambda times the integrated squared second derivative, the bending energy. "
            "<bookmark mark='b'/> As positive lambda tends to zero, distinct observations are interpolated; tied x "
            "values are fitted by their averages. <bookmark mark='c'/> As lambda grows, curvature becomes "
            "unaffordable and the solution tends to the least-squares line, which has no curvature at all. <bookmark "
            "mark='d'/> The search is over functions with square-integrable weak second derivative, an "
            "infinite-dimensional space. Remarkably, the answer is finite-dimensional."
        ) as vo:
            intro=label('A roughness penalty trades data fit against bending energy',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def theorem(self):
        rows = [
            cmath(r"s", r":", r"\text{the natural cubic spline with } s(x_i) = g(x_i)", font_size=28),
            cmath(r"\textstyle\int s''(g'' - s'')", r"=", r"[s''(g' - s')] - \textstyle\int s'''(g' - s') = 0", font_size=28),
            cmath(r"\textstyle\int g''^2", r"=", r"\textstyle\int s''^2 + \int (g'' - s'')^2 \ \ge \int s''^2", font_size=30),
            cmath(r"\text{so}", r":", r"\text{the minimizer is a natural cubic spline, \ knots at the } x_i", font_size=28),
        ]
        rows[3][2].set_color(SPLC)
        whys = [why(r"piecewise cubic, \ linear beyond the ends"), why(r"$s'' = 0$ at the ends; \ $s'''$ constant between knots"),
                why(r"Pythagoras, \ in function space"), why(r"Reinsch (1967); \ Schoenberg (1964)")]
        with self.voiceover(
            "<bookmark mark='a'/> Take any candidate g, and let s be the natural cubic spline through g's values at the "
            "data points: cubic between them, linear beyond the ends. Then s fits the data exactly as well as g. "
            "<bookmark mark='b'/> Integrate s double prime times g double prime minus s double prime by parts: the boundary "
            "term vanishes because s double prime is zero at the ends, and the remaining integral vanishes because s triple "
            "prime is constant between knots, where g minus s takes equal values at both ends. <bookmark mark='c'/> So the "
            "bending energy of g is that of s plus a non-negative remainder, Pythagoras in function space. "
            "<bookmark mark='d'/> Every candidate is beaten by a natural cubic spline, so the minimizer is one, with knots at "
            "the data: the theorem of Isaac Schoenberg and Christian Reinsch."
        ) as vo:
            intro=label('Natural cubic splines minimize roughness at fixed knot values',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def reinsch(self):
        rows = [
            cmath(r"\textstyle\int s''^2", r"=", r"g^\top K g, \ \ K = Q R^{-1} Q^\top", font_size=30),
            cmath(r"\hat g", r"=", r"\arg\min \|y - g\|^2 + \lambda g^\top K g = (I + \lambda K)^{-1} y", font_size=30),
            cmath(r"S_\lambda", r"=", r"(I + \lambda K)^{-1}: \ \text{the smoother matrix}", font_size=30),
            cmath(r"\text{cost}", r":", r"O(n) \text{ with banded solves; teaching code is dense}", font_size=30),
        ]
        rows[1][2].set_color(SPLC)
        whys = [why(r"$g$: \ the spline's values at the knots"), why(r"a ridge regression in disguise"),
                why(r"$\mathrm{df} = \mathrm{tr}\, S_\lambda$, \ Part 28"), why(r"banded Reinsch solver; \ dense reference implementation here")]
        with self.voiceover(
            "<bookmark mark='a'/> A natural cubic spline is determined by its values at the knots, and its bending "
            "energy is a quadratic form in them, g transpose K g, with K built from two banded matrices, Peter Green "
            "and Bernard Silverman's Q and R. <bookmark mark='b'/> The infinite problem becomes a finite penalized "
            "least squares, with solution I plus lambda K, inverse, times y. <bookmark mark='c'/> The smoother matrix"
            " S; its trace is the degrees of freedom of Part 28. <bookmark mark='d'/> A banded Reinsch implementation"
            " can solve a fixed-lambda fit in order n operations after sorting. Our teaching implementation forms "
            "dense matrices; tests compare its values with SciPy, rather than claiming linear complexity for this "
            "code."
        ) as vo:
            intro=label('A finite quadratic penalty represents the infinite-dimensional problem',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fits(self):
        d = load("spline")
        t, a, tt = np.asarray(d["t"]), np.asarray(d["a"]), np.asarray(d["tt"])
        A = axes([0, 60], [-150, 90], x_length=7.4, y_length=4.4, xlabel=r"milliseconds after impact",
                 ylabel=r"head acceleration ($g$)", xticks=[0, 20, 40, 60], yticks=[-100, 0, 50], center=[-2.0, 0.3, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(x, y), radius=0.045, color=WHITE, fill_opacity=0.7) for x, y in zip(t, a)])
        cs = {k: clip_curve(ax, tt, np.asarray(v["fit"]), SPLC, 3.5, ymin=-150, ymax=90) for k, v in d["fits"].items()}
        rows = fit_rows(VGroup(
            label(r"the motorcycle data again", font_size=22),
            label(r"df 4: \ too stiff for the dip", font_size=22, color=SPLC),
            label(r"df 8: \ the dip, \ not the rebound", font_size=22, color=SPLC),
            label(r"df 12: \ dip, \ rebound, \ decay", font_size=22, color=SPLC),
            label(r"df 25: \ chasing the noise", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Smoothing splines on the motorcycle data, indexed by their degrees of freedom rather than "
            "lambda, which has awkward units. <bookmark mark='b'/> Four degrees of freedom: too stiff to follow the dip. "
            "<bookmark mark='c'/> Eight: the dip, but the rebound is flattened. <bookmark mark='d'/> Twelve: dip, rebound and "
            "decay. <bookmark mark='e'/> Twenty-five: the curve starts chasing individual readings."
        ) as vo:
            self.add(mcycle_tag())
            self.play(FadeIn(A), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            cur = None
            for k, (key, m_) in enumerate((("4", "b"), ("8", "c"), ("12", "d"), ("25", "e"))):
                vo.wait_until(m_)
                if cur is None:
                    self.play(Create(cs[key]), FadeIn(rows[k + 1]))
                else:
                    self.play(ReplacementTransform(cur, cs[key]), FadeIn(rows[k + 1]), run_time=1.5)
                cur = cs[key]
        self.clear_scene()

    def spectrum(self):
        d = load("spline")
        knots = np.asarray(d["knots"])
        U = np.column_stack([np.asarray(d["basis"][str(j)]) for j in range(8)])
        # the null space comes back from eigh in an arbitrary rotation: show it as a constant and a centred line
        U[:, 0] = 1.0 / np.sqrt(len(knots))
        c = knots - knots.mean()
        U[:, 1] = c / np.linalg.norm(c)
        eig = np.asarray(d["eig"])[:8]
        s8, s25 = np.asarray(d["shrink"]["df8"]), np.asarray(d["shrink"]["df25"])
        lam8 = (1 / s8[2] - 1) / eig[2]
        lam25 = (1 / s25[2] - 1) / eig[2]
        sp = SplineSpectrum(knots, U, eig, lam8, k=8, width=8.4, height=5.4, center=[-1.6, -0.2, 0], curve_color=SPLC,
                            bar_color=PATH)
        b25 = sp.bars(lam25)
        rows = fit_rows(VGroup(
            label(r"$K = U\, \mathrm{diag}(d_j)\, U^\top$", font_size=22),
            label(r"$S_\lambda = U\, \mathrm{diag}\bigl(\tfrac{1}{1 + \lambda d_j}\bigr)\, U^\top$", font_size=22, color=PATH),
            label(r"$u_1, u_2$: \ constant, \ line: \ kept whole", font_size=22, color=SPLC),
            label(r"df 8: \ the wiggly ones damped", font_size=22, color=PATH),
            label(r"df 25: \ more of them let through", font_size=22, color=PATH),
        ), 3.2, 0.42, [5.3, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The spline spectrum: this part's instrument. Diagonalize K. Its eigenvectors, the "
            "Demmler–Reinsch basis, are oscillating curves on the crash times, ordered from smooth to wiggly, "
            "<bookmark mark='b'/> and the smoother keeps each component in proportion one over one plus lambda d j. "
            "<bookmark mark='c'/> The first two, a constant and a line, have zero bending energy and pass whole. "
            "<bookmark mark='d'/> At eight degrees of freedom the components with more and more oscillations are damped "
            "harder and harder. <bookmark mark='e'/> At twenty-five, more of them get through. A smoothing spline is a "
            "low-pass filter in this basis, and its degrees of freedom are the sum of the bars."
        ) as vo:
            self.add(mcycle_tag())
            vo.wait_until("a")
            self.play(FadeIn(sp.head), FadeIn(sp.tags), LaggedStart(*[Create(c) for c in sp.curves], lag_ratio=0.15), FadeIn(rows[0]),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(sp.frame), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(sp.stack[0], LEFT), GrowFromEdge(sp.stack[1], LEFT), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in sp.stack[2:]], lag_ratio=0.15), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Transform(sp.stack, b25), FadeIn(rows[4]), run_time=2.0)
        self.clear_scene()

    def ridge(self):
        rows = [
            cmath(r"\hat g", r"=", r"\textstyle\sum_j \frac{1}{1 + \lambda d_j} (u_j^\top y)\, u_j", font_size=30),
            cmath(r"\mathrm{df}(\lambda)", r"=", r"\textstyle\sum_j \frac{1}{1 + \lambda d_j}", font_size=32),
            cmath(r"d_j", r"\approx", r"c\, j^4: \ \text{wiggles cost the fourth power}", font_size=30),
            cmath(r"\text{ridge, \ Part 25}", r":", r"\text{shrink each principal component by } \tfrac{d}{d + \lambda}", font_size=28),
        ]
        rows[0][2].set_color(SPLC)
        whys = [why(r"project, \ shrink, \ add up"), why(r"between 2 and $n$"), why(r"Demmler \& Reinsch (1975)"),
                why(r"the same idea: \ shrink the rough directions most")]
        with self.voiceover(
            "<bookmark mark='a'/> So the fit is: project the data on each basis curve, shrink by its factor, add up. "
            "<bookmark mark='b'/> The degrees of freedom are the sum of the factors, between two, for the line, and "
            "n, for interpolation. <bookmark mark='c'/> Under regular designs the eigenvalues grow roughly like the "
            "fourth power of the oscillation index. Irregular knot spacing changes the spectrum. <bookmark mark='d'/>"
            " It is Part 25's ridge regression, which shrinks each principal direction, with the roughness penalty "
            "deciding which directions are rough."
        ) as vo:
            intro=label('The penalty eigenbasis reveals which directions are shrunk',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
