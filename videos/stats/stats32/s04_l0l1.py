from __future__ import annotations

import numpy as np

from videos.stats.stats32.common import *  # noqa: F403


def lq_curve(q, center, r=1.25, color=None, n=400):
    th = np.linspace(0, 2 * np.pi, n)
    c, s = np.cos(th), np.sin(th)
    rad = 1.0 / (np.abs(c) ** q + np.abs(s) ** q) ** (1 / q)
    pts = [np.array(center) + r * np.array([a * c_, a * s_, 0]) for a, c_, s_ in zip(rad, c, s)]
    m = VMobject(stroke_color=color or LASSO, stroke_width=3, fill_color=color or LASSO, fill_opacity=0.15)
    m.set_points_as_corners(pts + [pts[0]])
    return m


class FromL0(VoiceoverScene):
    def construct(self):
        self.card()
        self.subset()
        self.hard()
        self.balls()
        self.relax()
        self.octahedron()
        self.hull()

    def card(self):
        card = chapter_card(3, r"From $\ell_0$ to $\ell_1$", r"The closest convex penalty to counting", lit=(1996,), part=PART)
        with self.voiceover("Chapter three. From counting to absolute values."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def subset(self):
        rows = [
            cmath(r"\min_\beta", r"", r"\tfrac1{2n}\|y - X\beta\|^2 \ \text{ subject to } \ \|\beta\|_0 \le k", font_size=30),
            cmath(r"\|\beta\|_0", r"=", r"\#\{j : \beta_j \ne 0\}", font_size=32),
            cmath(r"\text{orthonormal } X", r":", r"\text{keep the } k \text{ largest } |\hat\beta_j|: \ \text{hard thresholding}", font_size=28),
            cmath(r"\text{general } X", r":", r"\text{search } \tbinom{p}{k} \text{ subsets}", font_size=30),
        ]
        rows[0][-1].set_color(RES)
        whys = [why(r"best subset selection"), why(r"the `$\ell_0$ norm': \ a count, \ not a norm"),
                why(r"easy when the columns are orthogonal"), why(r"hard in general")]
        with self.voiceover(
            "<bookmark mark='a'/> The most natural sparse method is best subset selection: among all models with at "
            "most k variables, take the one with the smallest residual sum of squares. <bookmark mark='b'/> Its "
            "constraint counts nonzero coefficients, written as the zero norm, though it is not really a norm. "
            "<bookmark mark='c'/> When the columns are orthonormal it is easy: keep the k largest least-squares "
            "coefficients and zero the rest, hard thresholding. <bookmark mark='d'/> In general, the columns "
            "interact, and the worst-case search is combinatorial, although bounds, pruning and mixed-integer methods"
            " can avoid enumerating every subset."
        ) as vo:
            intro=label('Best-subset fitting constrains the number of nonzero coefficients',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hard(self):
        hdr = [r"\textbf{variables $p$}", r"\textbf{subsets $2^p$}", r"\textbf{at a billion fits a second}"]
        body = [["10", "1,024", r"a microsecond"], ["30", r"$1.1 \times 10^9$", r"a second"],
                ["64", r"$1.8 \times 10^{19}$", r"585 years"], ["20,000", r"$10^{6021}$", r"never"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.2, row_buff=0.32, colors=[GREY_A, None, None, RES, RES])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"Furnival \& Wilson's leaps and bounds (1974) reach $p \approx 40$", font_size=22),
            label(r"mixed-integer optimization (Bertsimas, King \& Mazumder 2016) reaches the hundreds", font_size=22, color=LASSO),
            label(r"Natarajan (1995): \ sparse approximation is NP-hard in general", font_size=22, color=RES),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The count of subsets doubles with every variable. Ten variables give a thousand subsets; "
            "thirty give a billion; the sixty-four candidate terms of the quadratic diabetes model of chapter seven give "
            "eighteen quintillion, five hundred and eighty-five years at a billion fits a second. Twenty thousand genes is "
            "beyond counting. <bookmark mark='b'/> Clever algorithms help: Furnival and Wilson's leaps and bounds of 1974 "
            "reaches about forty variables, and modern mixed-integer solvers reach the hundreds. <bookmark mark='c'/> But "
            "Balas Natarajan proved in 1995 that sparse approximation is NP-hard in general. We need a different idea."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def balls(self):
        qs = [2.0, 1.5, 1.0, 0.7, 0.4]
        cols = [RIDGE, S.KEPT, LASSO, NCV, RES]
        centers = [[-5.2 + 2.6 * k, 0.6, 0] for k in range(5)]
        shapes = VGroup(*[lq_curve(q, c, color=col) for q, c, col in zip(qs, centers, cols)])
        axs = VGroup(*[VGroup(Line(np.array(c) + LEFT * 1.4, np.array(c) + RIGHT * 1.4, color=GREY_D, stroke_width=1),
                              Line(np.array(c) + DOWN * 1.4, np.array(c) + UP * 1.4, color=GREY_D, stroke_width=1)) for c in centers])
        caps = VGroup(*[label(rf"$q = {q:g}$", font_size=24, color=col).next_to(np.array(c) + DOWN * 1.4, DOWN, buff=0.2)
                        for q, c, col in zip(qs, centers, cols)])
        rows = fit_rows(VGroup(
            label(r"the unit balls $\{\beta : \sum_j |\beta_j|^q \le 1\}$", font_size=24),
            label(r"$q \ge 1$: \ convex; \ $q < 1$: \ not convex", font_size=24, color=GREY_A),
            label(r"$q \to 0$: \ bounded axis segments; the unbounded count constraint is different", font_size=24, color=RES),
            label(r"$q = 1$ is where the corners appear and convexity survives", font_size=24, color=LASSO),
        ), 12.4, 0.2, [0, -2.6, 0])
        self.add(rows[0])
        with self.voiceover(
            "<bookmark mark='a'/> Look at the unit balls of the q-norms, the sum of absolute values to the power q. "
            "<bookmark mark='b'/> For q equal to two, the circle of ridge regression. As q falls, the ball pinches in"
            " towards the axes. For q at least one, the balls are convex; below one, they are not. <bookmark "
            "mark='c'/> As q goes to zero, these bounded unit balls approach the axis segments with amplitude at most"
            " one. The unbounded zero-count constraint alone would include whole axes. <bookmark mark='d'/> And q "
            "equal to one is the boundary case: the first q where corners appear on the axes, and the last where the "
            "ball is still convex."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(axs))
            self.play(LaggedStart(*[DrawBorderThenFill(s) for s in shapes], lag_ratio=0.3), FadeIn(caps), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(shapes[4], color=RES), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Indicate(shapes[2], color=LASSO, scale_factor=1.15), FadeIn(rows[3]))
        self.clear_scene()

    def relax(self):
        rows = [
            cmath(r"\ell_0", r":", r"\text{sparse, \ not convex: \ local search, \ no guarantees}", font_size=30),
            cmath(r"\ell_2", r":", r"\text{convex, \ not sparse}", font_size=30),
            cmath(r"\ell_1", r":", r"\text{convex \ and sparse}", font_size=30),
            cmath(r"\min \tfrac1{2n}\|y - X\beta\|^2 + \lambda\|\beta\|_1", r":", r"\text{the lasso}", font_size=30),
        ]
        rows[2][-1].set_color(LASSO)
        whys = [why(r"combinatorial"), why(r"ridge"), why(r"the best of both"), why(r"Tibshirani (1996); \ Chen, Donoho \& Saunders (1998)")]
        with self.voiceover(
            "<bookmark mark='a'/> So the trade is this. The zero norm gives sparsity but no convexity, so optimization is "
            "combinatorial. <bookmark mark='b'/> The two norm gives convexity but no sparsity. <bookmark mark='c'/> The one "
            "norm gives both. <bookmark mark='d'/> Replacing the count by the sum of absolute values gives the lasso, "
            "proposed by Robert Tibshirani in 1996, and at the same time, as basis pursuit, by Scott Chen, David Donoho and "
            "Michael Saunders for signal processing."
        ) as vo:
            intro=label('The absolute-value penalty is a convex alternative to counting',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def octahedron(self):
        t = ValueTracker(0.0)
        V = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], float)
        E = [(i, j) for i in range(6) for j in range(i + 1, 6) if abs(V[i] @ V[j]) < 0.5]
        c0 = np.array([-2.2, 0.0, 0.0])

        def proj(v):
            a = t.get_value()
            R = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
            w = R @ v
            # an oblique view: x to the right, z up, y receding
            return c0 + 2.2 * np.array([w[0] - 0.45 * w[1], w[2] + 0.3 * w[1], 0])

        def draw():
            g = VGroup()
            for i, j in E:
                depth = (V[i] + V[j])
                a = t.get_value()
                yv = -np.sin(a) * depth[0] + np.cos(a) * depth[1]
                g.add(Line(proj(V[i]), proj(V[j]), color=LASSO, stroke_width=3 if yv <= 0 else 1.5,
                           stroke_opacity=1.0 if yv <= 0 else 0.45))
            for v in V:
                g.add(Dot(proj(v), radius=0.08, color=SPIKE))
            return g

        oct_ = always_redraw(draw)
        rows = fit_rows(VGroup(
            label(r"$\|\beta\|_1 \le 1$ in three dimensions: \ an octahedron", font_size=22),
            label(r"6 vertices: \ one nonzero coordinate", font_size=22, color=SPIKE),
            label(r"12 edges: \ two nonzero; \ 8 faces: \ three", font_size=22, color=LASSO),
            label(r"the first face touched depends on design, data and budget", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In three dimensions the one-norm ball is an octahedron. <bookmark mark='b'/> Its "
            "six vertices lie on the axes: each has a single nonzero coordinate. <bookmark mark='c'/> Its twelve "
            "edges have two nonzero coordinates, and only its eight faces have three. <bookmark mark='d'/> An "
            "expanding loss contour can first touch a low-dimensional face, producing zeros. Which face is reached "
            "depends on the data, design and budget; geometry alone does not guarantee that most coordinates vanish."
        ) as vo:
            self.add(oct_)
            vo.wait_until("a")
            self.play(t.animate.set_value(0.8), FadeIn(rows[0]), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(1.6), FadeIn(rows[1]), run_time=3.0, rate_func=linear)
            vo.wait_until("c")
            self.play(t.animate.set_value(2.4), FadeIn(rows[2]), run_time=3.0, rate_func=linear)
            vo.wait_until("d")
            self.play(t.animate.set_value(3.6), FadeIn(rows[3]), run_time=5.0, rate_func=linear)
        oct_.clear_updaters()
        self.clear_scene()

    def hull(self):
        rows = [
            cmath(r"\{\beta : \|\beta\|_0 \le 1, \ \|\beta\|_\infty \le 1\}", r":", r"\text{axis segments, with vertices }\pm e_j", font_size=28),
            cmath(r"\mathrm{conv}\{\pm e_1, \dots, \pm e_p\}", r"=", r"\{\beta : \|\beta\|_1 \le 1\}", font_size=30),
            cmath(r"|\beta_j| \le 1", r"\Rightarrow", r"|\beta_j| \le |\beta_j|^q \to \mathbf 1\{\beta_j \ne 0\}", font_size=28),
            cmath(r"\text{so}", r":", r"\ell_1 \text{ is the largest convex function below } \ell_0 \text{ on the box}", font_size=28),
        ]
        rows[3][-1].set_color(LASSO)
        whys = [why(r"the sparsest nonzero points"), why(r"their convex hull is the $\ell_1$ ball"),
                why(r"$\ell_1$ sits below the count"), why(r"the convex envelope")]
        with self.voiceover(
            "<bookmark mark='a'/> There is a precise sense in which one is the right choice. Take the axis segments "
            "of the bounded one-coordinate set, whose extreme points are the signed unit vectors. <bookmark "
            "mark='b'/> Their convex hull is exactly the one-norm ball. <bookmark mark='c'/> And on the box where "
            "every coordinate is at most one in size, the absolute value lies below the indicator of being nonzero. "
            "<bookmark mark='d'/> In fact, on that box, the one norm is the largest convex function that never "
            "exceeds the count: its convex envelope. This convex-envelope statement applies on the specified unit "
            "box; rescaling or removing that bound changes the comparison."
        ) as vo:
            intro=label('The convex-envelope comparison needs a bounded coordinate box',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
