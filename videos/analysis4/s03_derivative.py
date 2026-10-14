from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis4.common import angle_ticks, load, mapped_grid, plain_axes, polyline, square_axes
from videos.analysis4.compute import f_surf, grad_surf


def chain_f(P):
    x, y = P[..., 0], P[..., 1]
    return np.stack([x + 0.3 * np.sin(1.5 * y), y + 0.3 * np.sin(1.5 * x)], -1)


def chain_g(P):
    u, v = P[..., 0], P[..., 1]
    return np.stack([u + 0.25 * v * v, v - 0.25 * u * u], -1)


def jac(F, p, h=1e-6):
    p = np.asarray(p, float)
    cols = [(F(p + h * e) - F(p - h * e)) / (2 * h) for e in np.eye(2)]
    return np.stack(cols, -1)


class Derivative(VoiceoverScene):
    def construct(self):
        self.card()
        self.zoom()
        self.definition()
        self.chain()
        self.gradient()
        self.dictionary()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"The derivative is a linear map",
                            r"What is the derivative of a function of several variables?", lit=(), part=4)
        with self.voiceover("Chapter two: what the derivative becomes when there is more than one variable."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def zoom(self):
        d = load("derivative")
        p, A = d["p"], d["A"]
        f0 = float(f_surf(*p))
        gnorm = float(np.linalg.norm(A))
        S = 4.6
        axL = square_axes([-1, 1, 1], [-1, 1, 1], S / 2).move_to([-3.4, -0.55, 0])
        axR = square_axes([-1, 1, 1], [-1, 1, 1], S / 2).move_to([3.4, -0.55, 0])
        frames = VGroup(*[Square(side_length=S, color=GREY_C, stroke_width=2).move_to(a) for a in (axL, axR)])
        u = np.linspace(-1, 1, 161)
        ws = [1.6, 0.4, 0.1, 0.025]
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.APPROX), k / 8) for k in range(9)]

        def panel(ax, F, w):
            delta = gnorm * w * 2 / 9  # nine level lines across the window in the linear picture
            g = VGroup()
            for k in range(-12, 13):
                segs = contour_segments(lambda U, V: F(p[0] + w * U, p[1] + w * V), u, u, f0 + k * delta)
                if len(segs):
                    g.add(contour_mobject(ax, segs, cols[(k + 12) % 9], 2.2))
            return g

        lin = lambda X, Y: f0 + A[0] * (X - p[0]) + A[1] * (Y - p[1])  # noqa: E731
        left = [panel(axL, f_surf, w) for w in ws]
        right = panel(axR, lin, ws[0])
        dotL, dotR = Dot(axL.c2p(0, 0), radius=0.07, color=WHITE), Dot(axR.c2p(0, 0), radius=0.07, color=WHITE)
        gdir = A / gnorm
        garr = Arrow(axL.c2p(0, 0), axL.c2p(*(0.55 * gdir)), buff=0, color=C.EPS, stroke_width=5, tip_length=0.18)
        labs = [MathTex(rf"\text{{window width }} {2 * w:g}", font_size=28, color=GREY_A).next_to(frames[0], DOWN,
                                                                                                buff=0.15)
                for w in ws]
        tl = MathTex(r"f(x, y) = \sin x \cos y + 0.3\,xy", font_size=30, color=C.SEQ).next_to(frames[0], UP, buff=0.15)
        tr = MathTex(r"f(p) + \nabla f(p) \cdot h", font_size=30, color=C.APPROX).next_to(frames[1], UP, buff=0.15)
        trl = label(r"a linear function: \ parallel, evenly spaced level lines", font_size=22, color=GREY_A).next_to(
            frames[1], DOWN, buff=0.15)
        head = label(rf"Zoom in on the level curves of $f$ at $p = ({p[0]:g}, {p[1]:g})$", font_size=34).to_edge(UP,
                                                                                                         buff=0.3)
        assert np.allclose(p, [0.6, 0.4])
        with self.voiceover(
            "<bookmark mark='a'/> Here's a function of two variables, drawn by its level curves, the way a map shows "
            "a landscape. <bookmark mark='b'/> Zoom in at a point. The curves straighten, and their spacing evens "
            "out. <bookmark mark='c'/> In the limit they become the level lines of a linear function: parallel, and "
            "equally spaced. That linear function is the derivative. In one variable, a curve under the microscope "
            "becomes a line; in two, a landscape becomes a tilted plane."
        ) as vo:
            self.play(FadeIn(head), Create(frames[0]), FadeIn(tl))
            vo.wait_until("a")
            self.play(Create(left[0]), FadeIn(dotL), FadeIn(labs[0]), run_time=2.0)
            vo.wait_until("b")
            cur, cl = left[0], labs[0]
            for k in range(1, len(ws)):
                self.play(ReplacementTransform(cur, left[k]), FadeTransform(cl, labs[k]), run_time=1.5)
                cur, cl = left[k], labs[k]
            vo.wait_until("c")
            self.play(Create(frames[1]), FadeIn(tr), Create(right), FadeIn(dotR), FadeIn(trl), run_time=2.0)
            self.play(GrowArrow(garr))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def definition(self):
        d = load("derivative")
        hs, worst, p, A = d["hs"], d["worst"], d["p"], d["A"]
        head = VGroup(label(r"Differentiable: \ a linear map $A$ with a small error", font_size=34),
                      MathTex(r"\lim_{h \to 0} \frac{|f(x + h) - f(x) - Ah|}{|h|} = 0",
                              r"\quad \text{\small (Rudin 9.11)}", font_size=38),
                      label(r"then $f'(x) = A$; \ it is unique (9.12)", font_size=24, color=GREY_A)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        head[1][0].set_color(C.EPS)
        head[1][1].set_color(GREY_B)
        # the definition as a picture: along one direction u, the change f(p + tu) - f(p) and the linear guess
        # t A u; their gap (the error) shrinks faster than t
        u = np.array([math.cos(0.5), math.sin(0.5)])
        tt = np.linspace(-1, 1, 401)
        chg = f_surf(p[0] + tt * u[0], p[1] + tt * u[1]) - f_surf(*p)
        lin = tt * (A @ u)
        lo, hi = math.floor(min(chg.min(), lin.min()) * 2) / 2, math.ceil(max(chg.max(), lin.max()) * 2) / 2
        cax = plain_axes([-1, 1, 0.5], [lo, hi, 0.5], 6.0, 3.3).move_to([-2.6, -1.4, 0])
        c_chg = polyline(cax, tt, chg, color=C.FUNC, stroke_width=3.5)
        c_lin = polyline(cax, tt, lin, color=C.APPROX, stroke_width=3)
        t1 = 0.8
        e_chg = float(f_surf(*(p + t1 * u)) - f_surf(*p))
        assert abs(e_chg - t1 * (A @ u)) > 0.08  # visible at t = 0.8 ...
        assert np.abs(chg - lin)[np.abs(tt) <= 0.1].max() < 0.1 * 0.1 * 0.5  # ... and of order t^2 near 0
        tv = ValueTracker(t1)

        def err_at(t):
            return abs(float(f_surf(*(p + t * u)) - f_surf(*p)) - t * (A @ u))

        # the error bar and the ratio error / t, as the step shrinks: both go to 0, the ratio too
        err = always_redraw(lambda: Line(cax.c2p(tv.get_value(), tv.get_value() * (A @ u)),
                                         cax.c2p(tv.get_value(), float(f_surf(*(p + tv.get_value() * u)) - f_surf(*p))),
                                         color=C.EPS, stroke_width=6))
        ro = always_redraw(lambda: VGroup(
            MathTex(rf"t = {tv.get_value():.2f}", font_size=30),
            MathTex(rf"|\text{{error}}| = {err_at(tv.get_value()):.4f}", font_size=30, color=C.EPS),
            MathTex(rf"|\text{{error}}| / t = {err_at(tv.get_value()) / tv.get_value():.4f}", font_size=30,
                    color=C.EPS)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to([1.6, -0.9, 0], RIGHT, buff=0))
        ts_ = np.linspace(0.1, t1, 50)
        ratios_ = np.array([err_at(t) / t for t in ts_])
        assert np.all(np.diff(ratios_) > 0) and ratios_[0] < 0.1 * ratios_[-1] * 1.5  # shrinks like t
        cl = VGroup(MathTex(r"f(p + tu) - f(p)", font_size=26, color=C.FUNC),
                    MathTex(r"t\, A u", font_size=26, color=C.APPROX),
                    MathTex(r"\text{error}", font_size=26, color=C.EPS))
        cl.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(cax.c2p(-1, hi), DR, buff=0.15)
        tlab = MathTex(r"t", font_size=26, color=GREY_A).next_to(cax.c2p(1, 0), UR, buff=0.08)
        sec = VGroup(cax, c_chg, c_lin, err, cl, tlab, ro)
        ax = plain_axes([-3, 0, 1], [-4, 0, 1], 6.0, 3.3, numbers=True, font_size=20,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-2.6, -1.4, 0])
        xl = MathTex(r"\log_{10}|h|", font_size=24, color=GREY_A).next_to(ax.c2p(-1.5, 0), UP, buff=0.4)
        # set along the y-axis (it is the axes' right edge), so it stays clear of the table to its right
        yl = MathTex(r"\log_{10}\text{ratio}", font_size=24, color=GREY_A).rotate(PI / 2).next_to(ax.c2p(0, -2), RIGHT,
                                                                                                    buff=0.15)
        pts = VGroup(*[Dot(ax.c2p(math.log10(h), math.log10(w)), radius=0.07, color=C.EPS) for h, w in zip(hs, worst)])
        slope = DashedLine(ax.c2p(-3, math.log10(worst[-1]) - 0.0), ax.c2p(0, math.log10(worst[-1]) + 3),
                           color=GREY_B, stroke_width=2)
        sl = label(r"dashed: slope $1$, \ the error is of order $|h|^2$", font_size=22, color=GREY_B).next_to(
            ax, DOWN, buff=0.12)  # below the axes, clear of the tick labels
        tab = VGroup(MathTex(r"|h|", r"\text{worst ratio, 200 directions}", font_size=26, color=GREY_A))
        for h, w in zip(hs, worst):
            tab.add(MathTex(rf"{h:g}", rf"{w:.5f}", font_size=26))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        regrid(tab, gap=0.5)
        tab.next_to([1.6, 0.2, 0], DR, buff=0)
        assert tab.get_right()[0] <= 6.6 and tab.get_bottom()[1] > -3.6 and ax.get_top()[1] < head.get_bottom()[1]
        assert yl.get_right()[0] < tab.get_left()[0] - 0.2
        assert np.all(np.diff(worst) < 0)
        with self.voiceover(
            "<bookmark mark='a'/> Rudin's definition: f is differentiable at x if some linear map A approximates the "
            "change in f so well that the error is small even compared with the size of the step: the error divided "
            "by the length of h goes to zero. That A is unique, and it is the derivative. <bookmark mark='b'/> Check "
            "it at our point. For each step length, try two hundred directions and record the worst ratio. "
            "<bookmark mark='c'/> On a log scale the ratios fall along a line of slope one: the error is of the order "
            "of the step squared, far smaller than the step itself."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head[0]), Create(cax), Create(c_chg), FadeIn(cl[0]), FadeIn(tlab))
            self.play(FadeIn(head[1]), Create(c_lin), FadeIn(cl[1]))
            self.play(Create(err), FadeIn(cl[2]), FadeIn(ro))
            self.play(tv.animate.set_value(0.1), run_time=3.0)
            self.play(FadeIn(head[2]))
            vo.wait_until("b")
            for m_ in (err, ro):
                m_.clear_updaters()
            self.play(FadeOut(sec), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(tab[0]))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(p_, scale=1.5), FadeIn(r_)) for p_, r_ in zip(pts, tab[1:])],
                                  lag_ratio=0.35), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(slope), FadeIn(sl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chain(self):
        p = np.array([0.4, 0.3])
        Jf, Jg = jac(chain_f, p), jac(chain_g, chain_f(p))
        Jgf = jac(lambda q: chain_g(chain_f(q)), p)
        assert np.allclose(Jgf, Jg @ Jf, atol=1e-6)
        h = 0.32
        U_, X_ = 2.5, (-4.6, 0.0, 4.6)  # scene units per unit; panel centres
        axs = [square_axes([-0.75, 0.75, 0.5], [-0.75, 0.75, 0.5], U_).move_to([x, -0.2, 0]) for x in X_]
        for a in axs:
            a.set_opacity(0.35)
        sq = np.array([[-h, -h], [h, -h], [h, h], [-h, h]])
        side = np.concatenate([np.linspace(sq[i], sq[(i + 1) % 4], 40, endpoint=False) for i in range(4)])
        P0 = p + side
        P1 = chain_f(P0)
        P2 = chain_g(P1)
        c0, c1, c2 = p, chain_f(p), chain_g(chain_f(p))
        for Q, c_ in ((P0, c0), (P1, c1), (P2, c2), (c1 + side @ Jf.T, c1), (c2 + side @ (Jg @ Jf).T, c2)):
            assert np.abs(Q - c_).max() < 0.72  # every shape fits its panel

        def poly(ax, Q, center, color, fill=0.2, dashed=False):
            m = VMobject(color=color, stroke_width=3, fill_color=color, fill_opacity=fill).set_points_as_corners(
                [ax.c2p(*(q - center)) for q in np.vstack([Q, Q[:1]])])
            return DashedVMobject(m, num_dashes=40) if dashed else m

        shapes = [poly(axs[0], P0, c0, C.SEQ), poly(axs[1], P1, c1, C.APPROX), poly(axs[2], P2, c2, C.EPS)]
        lin1 = poly(axs[1], c1 + side @ Jf.T, c1, WHITE, fill=0, dashed=True)
        lin2 = poly(axs[2], c2 + side @ (Jg @ Jf).T, c2, WHITE, fill=0, dashed=True)
        gaps_ = [(axs[0].get_right()[0], axs[1].get_left()[0]), (axs[1].get_right()[0], axs[2].get_left()[0])]
        arrows = VGroup(*[Arrow([l_ + 0.05, -0.2, 0], [r_ - 0.05, -0.2, 0], buff=0, color=GREY_B, stroke_width=4,
                                max_tip_length_to_length_ratio=0.35) for l_, r_ in gaps_])
        assert all(r_ - l_ > 0.6 for l_, r_ in gaps_)
        al = VGroup(MathTex("f", font_size=32, color=GREY_B).next_to(arrows[0], UP, buff=0.08),
                    MathTex("g", font_size=32, color=GREY_B).next_to(arrows[1], UP, buff=0.08))
        # one MathTex, so the three names share a baseline; each is then slid under its panel
        names = MathTex(r"\text{near } x", r"\qquad", r"\text{near } f(x)", r"\qquad", r"\text{near } g(f(x))",
                        font_size=26)
        names.next_to(axs[1], DOWN, buff=0.12)
        for part, a in zip((names[0], names[2], names[4]), axs):
            part.set_x(a.get_x())
        names = VGroup(names[0], names[2], names[4])
        head = VGroup(label(r"The chain rule: \ compose the derivatives", font_size=34),
                      MathTex(r"(g \circ f)'(x) = g'(f(x))\, f'(x)", r"\quad \text{\small (Rudin 9.15)}", font_size=38)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        head[1][0].set_color(C.EPS)
        head[1][1].set_color(GREY_B)
        note_ = label(r"dashed: \ the parallelograms the derivatives predict \ (matrix product, computed)",
                      font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        assert axs[0].get_top()[1] < head.get_bottom()[1] - 0.2 and names.get_bottom()[1] > note_.get_top()[1] + 0.1
        with self.voiceover(
            "<bookmark mark='a'/> With derivatives as linear maps, the chain rule says: the derivative of a "
            "composition is the composition of the derivatives, which for matrices is their product. "
            "<bookmark mark='b'/> Follow a small square. The first map bends it into a curvy quadrilateral, nearly the "
            "parallelogram its derivative predicts. <bookmark mark='c'/> The second map bends it again, and the result "
            "is nearly the parallelogram of the product of the two matrices."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), *[Create(a) for a in axs], FadeIn(names), FadeIn(shapes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(al[0]), TransformFromCopy(shapes[0], shapes[1]), run_time=1.5)
            self.play(Create(lin1))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(al[1]), TransformFromCopy(shapes[1], shapes[2]), run_time=1.5)
            self.play(Create(lin2), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gradient(self):
        d = load("derivative")
        p, A = d["p"], d["A"]
        ax = square_axes([-0.6, 1.8, 1], [-0.8, 1.6, 1], 2.3).move_to([-3.5, -0.75, 0])
        ax.set_opacity(0.5)
        xs, ys = np.linspace(-0.6, 1.8, 161), np.linspace(-0.8, 1.6, 161)
        levels = np.linspace(-0.6, 1.0, 17)
        cmap = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.APPROX), k / 16) for k in range(17)]
        lines = VGroup(*[contour_mobject(ax, contour_segments(f_surf, xs, ys, lv), c, 1.8) for lv, c in zip(levels, cmap)])
        arrows = VGroup()
        qs = [(0.0, 0.0), (0.6, 0.4), (1.2, -0.3), (0.2, 1.1), (1.4, 1.0), (-0.3, -0.5), (1.0, 0.9)]
        gmax = max(np.linalg.norm(grad_surf(*q)) for q in qs)  # arrow length proportional to |grad f|
        assert np.allclose(qs[1], p)
        for q in qs:
            g = grad_surf(*q)
            arrows.add(Arrow(ax.c2p(*q), ax.c2p(*(np.array(q) + 0.42 * g / gmax)), buff=0,
                             color=C.EPS, stroke_width=6 if np.allclose(q, p) else 4, tip_length=0.14,
                             max_tip_length_to_length_ratio=0.4))
        pdot = Dot(ax.c2p(*p), radius=0.08, color=WHITE).set_z_index(3)
        # the directional derivative at p as a function of the direction's angle: a pure cosine
        th = np.linspace(0, 2 * np.pi, 361)
        hh = 1e-6
        Du = np.array([(f_surf(p[0] + hh * math.cos(t), p[1] + hh * math.sin(t)) -
                        f_surf(p[0] - hh * math.cos(t), p[1] - hh * math.sin(t))) / (2 * hh) for t in th])
        assert np.allclose(Du, A[0] * np.cos(th) + A[1] * np.sin(th), atol=1e-6)
        bx = plain_axes([0, 2 * np.pi, np.pi / 2], [-1.0, 1.0, 0.5], 5.0, 2.4).move_to([3.4, -1.3, 0])
        dg = VMobject(color=C.EPS, stroke_width=3).set_points_as_corners([bx.c2p(t, v) for t, v in zip(th, Du)])
        assert np.abs(Du).max() < 0.95  # the cosine stays inside the plot, clear of the angle labels below it
        bt = angle_ticks(bx)
        bl = MathTex(r"D_u f(p) = \nabla f(p) \cdot u, \quad u = (\cos\theta, \sin\theta)", font_size=26,
                     color=C.EPS).next_to(bx, UP, buff=0.1)
        bl2 = label(r"a pure cosine in $\theta$: \ largest along $\nabla f$", font_size=22, color=GREY_A).next_to(
            bt, DOWN, buff=0.15)
        head = VGroup(label(r"The matrix of $f'(x)$: \ the Jacobian $(\partial f_i / \partial x_j)$", font_size=34),
                      MathTex(r"\nabla f = \Big(\frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}\Big)"
                              r"\ \perp \text{ the level curves}", r"\quad \text{\small (Rudin 9.17--9.18)}",
                              font_size=32)).arrange(DOWN, buff=0.12)
        head[1][1].set_color(GREY_B)
        head.to_edge(UP, buff=0.3)
        assert bt.get_right()[0] <= 6.6 and bl2.get_bottom()[1] > -3.6 and ax.get_top()[1] < head.get_bottom()[1]
        with self.voiceover(
            "<bookmark mark='a'/> In coordinates, the matrix of the derivative is the Jacobian, the array of partial "
            "derivatives. For a real-valued function it's a single row, the gradient. <bookmark mark='b'/> On the "
            "level-curve map the gradient points uphill, perpendicular to the curves, longest where they crowd "
            "together. <bookmark mark='c'/> The rate of change in a direction u is the gradient dotted with u. As u "
            "turns, that's a pure cosine of the angle: a linear function of the direction. Remember this shape: in "
            "the next chapter, a function will fail it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head[0]), Create(ax), Create(lines), FadeIn(pdot), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(head[1]), LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(bt), FadeIn(bl), Create(dg), run_time=2.0)
            self.play(FadeIn(bl2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dictionary(self):
        pairs = [(r"$f'(x)$ is a number: \ a slope", r"$f'(x)$ is a linear map $\R^n \to \R^m$"),
                 (r"the tangent line", r"the best linear approximation"),
                 (r"chain rule: \ multiply the slopes", r"chain rule: \ multiply the matrices"),
                 (r"$|f(b) - f(a)| \le M|b - a|$", r"on convex sets: \ $\|f'\| \le M$ \ (9.19)")]
        for pr in pairs:  # dictionary_card would shrink a wider row; keep every row at full size (20.8 after 0.8)
            assert all(label(t_, font_size=26).width <= 12.4 / 2 - 1.3 for t_ in pr)
        card = dictionary_card(r"one variable", r"several variables", pairs, font_size=26)
        card.scale(0.8).to_edge(UP, buff=0.3)
        # the rows as pictures. Left, one variable: y = sin x and its tangent at x0, slope cos x0
        x0 = 0.6
        lax = plain_axes([0, 2, 1], [0, 1.2, 0.5], 3.0, 1.8).move_to([-4.6, -2.0, 0])
        xs = np.linspace(0, 2, 200)
        sine = polyline(lax, xs, np.sin(xs), color=C.FUNC, stroke_width=3)
        slope = math.cos(x0)
        x_hi = x0 + (1.2 - math.sin(x0)) / slope  # where the tangent leaves the window
        tang = Line(lax.c2p(0, math.sin(x0) - x0 * slope), lax.c2p(x_hi, 1.2), color=C.APPROX, stroke_width=3)
        assert math.sin(x0) - x0 * slope > 0 and x_hi < 2
        ldot = Dot(lax.c2p(x0, math.sin(x0)), radius=0.06, color=WHITE)
        lcap = MathTex(rf"\text{{slope }} \cos {x0:g} = {slope:.3f}", font_size=24, color=C.APPROX).next_to(
            lax, DOWN, buff=0.15)
        lname = MathTex(r"y = \sin x", font_size=24, color=C.FUNC).next_to(lax.c2p(2, math.sin(2)), UP, buff=0.12)
        lname.align_to(lax, RIGHT)
        # right, several variables: near p, the level curves of f (blue) hug the parallel, evenly spaced level lines
        # of f(p) + grad f(p) . h (pink); the gradient arrow is perpendicular to them
        d = load("derivative")
        p, A = d["p"], d["A"]
        w = 0.35
        rax = square_axes([-w, w, w], [-w, w, w], 1.9 / (2 * w)).move_to([4.6, -1.95, 0])
        rax.set_opacity(0)
        frame = Square(side_length=1.9, color=GREY_C, stroke_width=2).move_to(rax)
        uu = np.linspace(-w, w, 81)
        f0 = float(f_surf(*p))
        step = float(np.linalg.norm(A)) * 2 * w / 7
        lvls = [f0 + k * step for k in range(-3, 4)]  # all inside the window's range of values
        lin_l = VGroup(*[contour_mobject(rax, contour_segments(lambda U, V: f0 + A[0] * U + A[1] * V, uu, uu, lv),
                                         C.APPROX, 2.5) for lv in lvls])
        f_l = VGroup(*[contour_mobject(rax, contour_segments(lambda U, V: f_surf(p[0] + U, p[1] + V), uu, uu, lv),
                                       C.FUNC, 2.0) for lv in lvls])
        assert all(len(m_.points) for m_ in lin_l) and all(len(m_.points) for m_ in f_l)
        garr = Arrow(rax.c2p(0, 0), rax.c2p(*(0.25 * A / np.linalg.norm(A))), buff=0, color=C.EPS, stroke_width=5,
                     tip_length=0.15)
        rdot = Dot(rax.c2p(0, 0), radius=0.06, color=WHITE)
        rcap = MathTex(r"\text{level lines of } f(p) + \nabla f(p)\cdot h", font_size=24, color=C.APPROX).next_to(
            frame, DOWN, buff=0.15)
        # middle, the chain rule: a square, its image under f'(x), and under g'(f(x)) f'(x)
        pc = np.array([0.4, 0.3])
        Jf, Jg = jac(chain_f, pc), jac(chain_g, chain_f(pc))
        hq, k_ = 0.32, 1.15
        sq = np.array([[-hq, -hq], [hq, -hq], [hq, hq], [-hq, hq]])
        mids = (-1.95, 0.0, 1.95)
        mats = (np.eye(2), Jf, Jg @ Jf)
        trio = VGroup(*[Polygon(*[np.array([cx + k_ * q[0], -1.85 + k_ * q[1], 0]) for q in sq @ M.T], color=col,
                                stroke_width=3, fill_color=col, fill_opacity=0.25)
                        for cx, M, col in zip(mids, mats, (C.SEQ, C.APPROX, C.EPS))])
        for a_, b_ in zip(trio[:-1], trio[1:]):
            assert b_.get_left()[0] - a_.get_right()[0] > 0.45
        tarr = VGroup(*[Arrow([a_.get_right()[0] + 0.05, -1.85, 0], [b_.get_left()[0] - 0.05, -1.85, 0], buff=0,
                              color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.4)
                        for a_, b_ in zip(trio[:-1], trio[1:])])
        tlab = VGroup(MathTex(r"f'(x)", font_size=22, color=GREY_B).next_to(tarr[0], UP, buff=0.06),
                      MathTex(r"g'(f(x))", font_size=22, color=GREY_B).next_to(tarr[1], UP, buff=0.06))
        tcap = MathTex(r"g'(f(x))\, f'(x): \ \text{a product of matrices}", font_size=24, color=C.EPS).next_to(
            trio, DOWN, buff=0.35)
        tcap.set_y(lcap.get_y())
        assert card.get_bottom()[1] > max(lax.get_top()[1], frame.get_top()[1], tlab.get_top()[1]) + 0.2
        assert lax.get_left()[0] > -6.6 and frame.get_right()[0] < 6.6 and lcap.get_bottom()[1] > -3.6
        assert lax.get_right()[0] < trio.get_left()[0] - 0.3 and trio.get_right()[0] < frame.get_left()[0] - 0.3
        with self.voiceover(
            "So the dictionary from one variable to several: <bookmark mark='a'/> the derivative stops being a number "
            "and becomes a linear map; <bookmark mark='b'/> the tangent line becomes the best linear approximation; "
            "<bookmark mark='c'/> the chain rule multiplies matrices instead of numbers; <bookmark mark='d'/> and the "
            "mean value inequality survives on convex sets, with the norm of the derivative in place of the "
            "absolute value."
        ) as vo:
            self.play(FadeIn(card.titles))
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                pics = []
                if i == 0:
                    pics = [Create(lax), Create(sine), FadeIn(lname), FadeIn(ldot), FadeIn(lcap), Create(frame),
                            Create(lin_l), GrowArrow(garr), FadeIn(rdot), FadeIn(rcap)]
                elif i == 1:
                    pics = [Create(tang), Create(f_l)]
                elif i == 2:
                    pics = [FadeIn(trio[0]), *[GrowArrow(a_) for a_ in tarr], FadeIn(tlab), FadeIn(trio[1:]),
                            FadeIn(tcap)]
                self.play(FadeIn(card.rows[i][0], shift=RIGHT * 0.15), FadeIn(card.arrows[i]),
                          FadeIn(card.rows[i][1], shift=LEFT * 0.15), *pics, run_time=1.2 if pics else 1.0)
        self.wait(0.6)
        self.clear_scene()
