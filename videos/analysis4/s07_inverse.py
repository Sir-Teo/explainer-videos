from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis4.common import load, mapped_grid, square_axes
from videos.analysis4.compute import J_exp, f_exp


def F(P):
    x, y = P[..., 0], P[..., 1]
    return np.stack([np.exp(x) * np.cos(y), np.exp(x) * np.sin(y)], -1)


class InverseFunction(VoiceoverScene):
    def construct(self):
        self.card()
        self.picture()
        self.theorem()
        self.run()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"The inverse function theorem", r"When can a map of the plane be undone near a point?",
                            lit=(), part=4)
        with self.voiceover("Chapter six: the inverse function theorem, built from one contraction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def picture(self):
        head = label(r"The exponential as a map of the plane: \ $f(x, y) = (e^x \cos y,\ e^x \sin y)$", font_size=34)
        head.to_edge(UP, buff=0.3)
        ytop = 7.4  # the strip reaches past 2 pi, so the square 2 pi higher is inside it
        dax = square_axes([-1.2, 0.8, 1], [-0.4, ytop + 0.2, 1], 0.7)
        dax.move_to([-5.15, 0, 0]).align_to([0, head.get_bottom()[1] - 0.3, 0], UP)
        iax = square_axes([-2.4, 2.4, 1], [-2.4, 2.4, 1], 1.0).move_to([-0.55, -0.6, 0])
        iax.set_opacity(0.5)
        dom = mapped_grid(dax, lambda P: P, (-1.0, 0.6), (0, ytop), n=9, color=GREY_C, stroke_width=1.4)
        img = mapped_grid(iax, F, (-1.0, 0.6), (0, ytop), n=9, color=C.OPERATOR, stroke_width=1.6, samples=160)
        assert np.exp(0.6) < 2.4  # the image fits its axes
        # the y values that matter, outside the strip on the left (no tick numbers inside the grid)
        ylab = VGroup(*[MathTex(t_, font_size=20, color=GREY_B).next_to(dax.c2p(-1.0, v), LEFT, buff=0.15)
                        for t_, v in ((r"0", 0.0), (r"\pi", math.pi), (r"2\pi", 2 * math.pi))])
        yticks = VGroup(*[Line(dax.c2p(-1.0, v) + LEFT * 0.1, dax.c2p(-1.0, v), color=GREY_B, stroke_width=2)
                          for v in (0.0, math.pi, 2 * math.pi)])
        xlab = MathTex(r"x = 0", font_size=20, color=GREY_B).next_to(dax.c2p(0, 0), DOWN, buff=0.15)
        a = np.array([0.0, 0.6])
        h = 0.18
        sq = np.array([[-h, -h], [h, -h], [h, h], [-h, h]])
        edge = np.concatenate([np.linspace(sq[i], sq[(i + 1) % 4], 30, endpoint=False) for i in range(4)])

        def patch(ax, Q, color):
            return VMobject(color=color, stroke_width=3, fill_color=color, fill_opacity=0.35).set_points_as_corners(
                [ax.c2p(*q) for q in np.vstack([Q, Q[:1]])])

        a2 = a + np.array([0, 2 * math.pi])
        assert a2[1] + h < ytop  # the second square lies inside the drawn strip
        s1 = patch(dax, a + edge, C.EPS)
        s2 = patch(dax, a2 + edge, C.APPROX)
        i1 = patch(iax, F(a + edge), C.EPS)
        i2 = patch(iax, F(a2 + edge), C.APPROX)
        assert np.allclose(F(a + edge), F(a2 + edge))
        arrow = Arrow([dax.get_right()[0] + 0.25, iax.get_y(), 0], [iax.get_left()[0] - 0.1, iax.get_y(), 0], buff=0,
                      color=GREY_B, stroke_width=4)
        fl = MathTex(r"f", font_size=32, color=GREY_B).next_to(arrow, UP, buff=0.08)
        side = VGroup(
            label(r"vertical lines $\to$ circles", font_size=24, color=C.OPERATOR),
            label(r"horizontal lines $\to$ rays", font_size=24, color=C.OPERATOR),
            MathTex(r"\det f'(x, y) = e^{2x} \ne 0", font_size=30),
            label(r"near each point: \ one-to-one", font_size=24, color=C.EPS),
            label(r"but $f(x, y + 2\pi) = f(x, y)$:", font_size=24, color=C.APPROX),
            label(r"not one-to-one globally", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        side.next_to([iax.get_right()[0] + 0.35, -0.6, 0], RIGHT, buff=0)
        assert side.get_right()[0] <= 6.6 and dax.get_bottom()[1] > -3.6 and ylab.get_left()[0] > -6.7
        assert arrow.get_length() > 0.5 and iax.get_top()[1] < head.get_bottom()[1] - 0.1
        with self.voiceover(
            "<bookmark mark='a'/> Here's the map that sends x, y to e to the x times cosine y, e to the x times sine "
            "y: the complex exponential, seen as a map of the plane. <bookmark mark='b'/> It wraps the strip on the "
            "left around the origin: vertical lines become circles, horizontal lines become rays. "
            "<bookmark mark='c'/> Its derivative is invertible everywhere, and near each point the map is one-to-one: "
            "a small square goes to a small curved square. <bookmark mark='d'/> But a square two pi higher lands in "
            "exactly the same place. The map can be undone near every point, and not globally. The inverse function "
            "theorem is precisely the local statement."
        ) as vo:
            self.play(FadeIn(head), Create(dom), FadeIn(ylab), Create(yticks), FadeIn(xlab))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(fl))
            vo.wait_until("b")
            self.play(TransformFromCopy(dom, img), run_time=2.5)
            self.play(FadeIn(side[:2]))
            vo.wait_until("c")
            self.play(FadeIn(s1), FadeIn(side[2]))
            self.play(TransformFromCopy(s1, i1), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(s2), FadeIn(side[4]))
            self.play(TransformFromCopy(s2, i2), FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        title = label(r"The inverse function theorem", font_size=34).to_edge(UP, buff=0.3)
        thm = VGroup(
            VGroup(label(r"$f$ is $\mathcal C^1$ near $a$, \ $f'(a)$ is invertible, \ $b = f(a)$:", font_size=28),
                   label(r"(Rudin 9.24)", font_size=22, color=GREY_B)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN),
            label(r"there are open $U \ni a$ and $V \ni b$ with $f: U \to V$ one-to-one and onto,", font_size=28),
            label(r"and the inverse $g: V \to U$ is $\mathcal C^1$, \ with $g'(y) = f'(g(y))^{-1}$", font_size=28,
                  color=C.EPS),
        ).arrange(DOWN, buff=0.16).next_to(title, DOWN, buff=0.2)
        pm = ProofMap([r"$\varphi_y$ is a contraction", r"$f$ is one-to-one on a ball $U$", r"$V = f(U)$ is open",
                       r"$g' = (f')^{-1}$"], font_size=24, width=3.0, buff=0.3)
        pm.next_to(title, DOWN, buff=0.2)
        idea = VGroup(
            label(r"to solve $f(x) = y$: \ correct $x$ by the linear guess", font_size=26),
            MathTex(r"x \;\mapsto\; x + A^{-1}\big(y - f(x)\big), \qquad A = f'(a)", font_size=34, color=C.EPS),
            label(r"a fixed point is a solution; \ near $a$ this map barely moves distances", font_size=26,
                  color=GREY_A),
            MathTex(r"\varphi_y'(x) = I - A^{-1} f'(x) \approx 0 \text{ near } a", font_size=32),
        ).arrange(DOWN, buff=0.18).next_to(pm, DOWN, buff=0.3)
        # the statement as a picture: a disk U around a, its image V around b, f one way and g back (no axes:
        # the picture is about the two regions)
        d = load("inverse")
        a, r, y_t, its = d["a"], float(d["r"]), d["target"], d["its"]
        th = np.linspace(0, 2 * math.pi, 241)
        circ = a + r * np.c_[np.cos(th), np.sin(th)]
        dax2 = square_axes([-0.7, 0.7, 0.5], [-0.1, 1.3, 0.5], 1.9).move_to([-3.2, -1.15, 0])
        iax2 = square_axes([0.2, 1.6, 0.5], [0.0, 1.4, 0.5], 1.9).move_to([3.2, -1.15, 0])
        U = VMobject(color=C.OPEN_SET, stroke_width=3, fill_color=C.OPEN_SET, fill_opacity=0.15).set_points_as_corners(
            [dax2.c2p(*q) for q in circ])
        V = VMobject(color=C.OPEN_SET, stroke_width=3, fill_color=C.OPEN_SET, fill_opacity=0.15).set_points_as_corners(
            [iax2.c2p(*q) for q in F(circ)])
        sq = (a[0] - 0.22, a[0] + 0.22), (a[1] - 0.22, a[1] + 0.22)
        g1 = mapped_grid(dax2, lambda P: P, *sq, n=7, color=GREY_B, stroke_width=1.2)
        g2 = mapped_grid(iax2, F, *sq, n=7, color=C.OPERATOR, stroke_width=1.4)
        b = F(a)
        dots = VGroup(Dot(dax2.c2p(*a), radius=0.06, color=C.EPS), Dot(iax2.c2p(*b), radius=0.06, color=C.EPS))
        # labels outside the regions, each with a thin leader to its point
        la = MathTex(r"a", font_size=30, color=C.EPS).next_to(U, LEFT, buff=0.35).set_y(dots[0].get_y())
        lb = MathTex(r"b", font_size=30, color=C.EPS).next_to(V, RIGHT, buff=0.35).set_y(dots[1].get_y())
        leads = VGroup(Line(la.get_right() + RIGHT * 0.06, dots[0].get_center(), color=GREY_B, stroke_width=1.5),
                       Line(lb.get_left() + LEFT * 0.06, dots[1].get_center(), color=GREY_B, stroke_width=1.5))
        dl = VGroup(la, lb, MathTex(r"U", font_size=30, color=C.OPEN_SET).next_to(U, UL, buff=0.0),
                    MathTex(r"V = f(U)", font_size=30, color=C.OPEN_SET).next_to(V, UP, buff=0.08))
        fa = Arrow([-1.2, -0.75, 0], [1.2, -0.75, 0], buff=0, color=C.OPERATOR, stroke_width=4)
        ga = Arrow([1.2, -1.55, 0], [-1.2, -1.55, 0], buff=0, color=C.EPS, stroke_width=4)
        fal = MathTex(r"f", font_size=30, color=C.OPERATOR).next_to(fa, UP, buff=0.08)
        gal = MathTex(r"g = f^{-1}", font_size=30, color=C.EPS).next_to(ga, DOWN, buff=0.08)
        assert abs(np.linalg.det(J_exp(a)) - math.exp(2 * a[0])) < 1e-12
        # one correction step, the first: from a, add A^-1 times the remaining error y - f(a)
        A = J_exp(a)
        x1 = a + np.linalg.solve(A, y_t - b)
        assert np.allclose(x1, its[1]) and np.linalg.norm(its[-1] - a) < r and np.linalg.norm(x1 - a) < r
        sol = Circle(radius=0.09, color=WHITE, stroke_width=2.5).move_to(dax2.c2p(*its[-1]))
        ydot = Dot(iax2.c2p(*y_t), radius=0.07, color=C.APPROX)
        yl = MathTex(r"y", font_size=30, color=C.APPROX).next_to(V, RIGHT, buff=0.35).set_y(ydot.get_y() - 0.15)
        ylead = Line(yl.get_left() + LEFT * 0.06, ydot.get_center(), color=GREY_B, stroke_width=1.5)
        errv = DashedLine(iax2.c2p(*b), iax2.c2p(*y_t), color=C.APPROX, stroke_width=3)
        stepv = Arrow(dax2.c2p(*a), dax2.c2p(*x1), buff=0, color=C.APPROX, stroke_width=4, tip_length=0.15,
                      max_tip_length_to_length_ratio=0.35)
        x1dot = Dot(dax2.c2p(*x1), radius=0.06, color=WHITE)
        fx1 = Dot(iax2.c2p(*F(x1)), radius=0.06, color=WHITE)
        pic = VGroup(dax2, iax2, U, V, g1, g2, dots, dl, leads, fa, ga, fal, gal)
        later = VGroup(sol, ydot, yl, ylead, errv, stepv, x1dot, fx1)
        whole = VGroup(pic, later)
        assert thm.get_bottom()[1] > whole.get_top()[1] + 0.2
        assert np.allclose(pic.copy().scale(0.8).get_center(), pic.get_center())
        # after the statement: the picture moves down and shrinks under the idea
        small = whole.copy().scale(0.8).next_to(idea, DOWN, buff=0.35)
        assert small.get_bottom()[1] > -3.65 and small.get_left()[0] > -6.6
        assert idea.get_right()[0] <= 6.6 and pm.get_bottom()[1] > idea.get_top()[1] + 0.1
        with self.voiceover(
            "<bookmark mark='a'/> The theorem, Rudin 9.24: if f is continuously differentiable near a and its "
            "derivative at a is invertible, then f maps some neighborhood of a one-to-one onto a neighborhood of f of "
            "a, and the inverse is continuously differentiable too, with derivative the inverse matrix. "
            "<bookmark mark='b'/> The proof has four steps, and the first carries the weight. "
            "<bookmark mark='c'/> To solve f of x equals y, start at a and correct x by the linear guess: add A "
            "inverse times the remaining error. A fixed point of that correction is exactly a solution. "
            "<bookmark mark='d'/> Its derivative is the identity minus A inverse times f prime of x, which is zero at "
            "a and small nearby. So on a small ball it's a contraction, and the contraction principle finds the "
            "solution, and only one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(title), FadeIn(thm[0]), Create(U), Create(g1), FadeIn(dots[0]), FadeIn(la),
                      Create(leads[0]), FadeIn(dl[2]))
            self.play(FadeIn(thm[1]), GrowArrow(fa), FadeIn(fal), TransformFromCopy(U, V), TransformFromCopy(g1, g2),
                      FadeIn(dots[1]), FadeIn(lb), Create(leads[1]), FadeIn(dl[3]), run_time=2.0)
            self.play(FadeIn(thm[2]), GrowArrow(ga), FadeIn(gal))
            vo.wait_until("b")
            self.play(FadeOut(thm), FadeIn(pm), pic.animate.scale(0.8).move_to(small[0]))
            sol_, ydot_, yl_, ylead_, errv_, stepv_, x1dot_, fx1_ = small[1]
            vo.wait_until("c")
            self.play(*pm.light(0), FadeIn(idea[0]), FadeIn(idea[1]))
            self.play(FadeIn(ydot_, scale=1.5), FadeIn(yl_), Create(ylead_), Create(errv_))
            self.play(GrowArrow(stepv_), FadeIn(x1dot_), FadeIn(fx1_))
            self.play(FadeIn(idea[2]), Create(sol_))
            vo.wait_until("d")
            self.play(FadeIn(idea[3]))
            self.play(*pm.done())
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def run(self):
        d = load("inverse")
        a, A, target, its, res, r, lip = d["a"], d["A"], d["target"], d["its"], d["res"], float(d["r"]), float(d["lip"])
        head = VGroup(label(r"Run it: \ the correction, again and again", font_size=34),
                      MathTex(r"x_{k+1} = x_k + A^{-1}\big(y - f(x_k)\big)", font_size=32, color=C.EPS)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        P = 3.4  # panel size
        ud, ui = P / 0.9, P / 0.95
        top = head.get_bottom()[1] - 0.65
        dax = square_axes([-0.45, 0.45, 0.25], [0.15, 1.05, 0.25], ud)
        dax.move_to([-6.55 + P / 2, top - P / 2, 0])
        dax.set_opacity(0.5)
        b = f_exp(a)
        iax = square_axes([b[0] - 0.4, b[0] + 0.55, 0.25], [b[1] - 0.55, b[1] + 0.4, 0.25], ui)
        iax.move_to([dax.get_right()[0] + 0.4 + P / 2, dax.get_y(), 0])
        iax.set_opacity(0.5)
        ball = Circle(radius=ud * r, color=C.CONNECTED_SET, stroke_width=1.5).move_to(dax.c2p(*a)).set_fill(
            C.CONNECTED_SET, 0.06)
        th = np.linspace(0, 2 * np.pi, 200)
        bimg = VMobject(color=C.CONNECTED_SET, stroke_width=1.5, fill_color=C.CONNECTED_SET, fill_opacity=0.06)
        bimg.set_points_as_corners([iax.c2p(*F(a + r * np.array([math.cos(t), math.sin(t)]))) for t in th])
        adot = Dot(dax.c2p(*a), radius=0.07, color=WHITE).set_z_index(2)
        bdot = Dot(iax.c2p(*b), radius=0.07, color=WHITE).set_z_index(2)
        ydot = Dot(iax.c2p(*target), radius=0.09, color=C.EPS).set_z_index(2)
        al = MathTex("a", font_size=28).next_to(adot, DL, buff=0.05)
        bl = MathTex("f(a)", font_size=28).next_to(bdot, DL, buff=0.05)
        yl = MathTex("y", font_size=30, color=C.EPS).next_to(ydot, DR, buff=0.06)
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.EPS), k / 7) for k in range(8)]
        xdots = [Dot(dax.c2p(*its[k]), radius=0.06, color=cols[k]).set_z_index(2) for k in range(8)]
        fdots = [Dot(iax.c2p(*f_exp(its[k])), radius=0.06, color=cols[k]).set_z_index(2) for k in range(8)]
        xpath = VGroup(*[Line(dax.c2p(*its[k]), dax.c2p(*its[k + 1]), color=GREY_B, stroke_width=2) for k in range(7)])
        fpath = VGroup(*[Line(iax.c2p(*f_exp(its[k])), iax.c2p(*f_exp(its[k + 1])), color=GREY_B, stroke_width=2)
                         for k in range(7)])
        # one MathTex for both titles, so they share a baseline
        tl = MathTex(r"\text{domain: the iterates } x_k", r"\qquad", r"\text{target: their images } f(x_k)",
                     font_size=26)
        tl.next_to(VGroup(dax, iax), UP, buff=0.12)
        tl[0].set_x(dax.get_x())
        tl[2].set_x(iax.get_x())
        tl = VGroup(tl[0], tl[2])
        # from the second image on, the f(x_k) are within 0.02 of y: magnify a window around y, equal scales
        W, H, hw = 2.4, 1.8, 0.022
        xw, yw = (target[0] - hw, target[0] + hw), (target[1] - hw * H / W, target[1] + hw * H / W)
        inset, mag = magnifier(iax, xw, yw, center=[iax.get_right()[0] + 0.45 + W / 2, iax.get_y() + 0.1, 0], width=W,
                               height=H, color=GREY_B)
        sc = W / (2 * hw)
        fx = np.array([f_exp(its[k]) for k in range(8)])
        inside = [k for k in range(8) if xw[0] < fx[k, 0] < xw[1] and yw[0] < fx[k, 1] < yw[1]]
        assert inside == list(range(2, 8)), inside
        assert sc * res[2] > 0.5 and sc * res[3] > 0.2 and sc * res[4] > 0.06  # three steps apart, then merged
        ifd = VGroup(*[Dot(inset.c2p(*fx[k]), radius=0.06, color=cols[k]).set_z_index(2) for k in inside])
        iy = Dot(inset.c2p(*target), radius=0.08, color=C.EPS).set_z_index(1)

        def clip(p, q):
            t0, t1, dv = 0.0, 1.0, q - p
            for lo, hi, pc, dc in ((xw[0], xw[1], p[0], dv[0]), (yw[0], yw[1], p[1], dv[1])):
                for num_, den_ in ((pc - lo, -dc), (hi - pc, dc)):
                    if abs(den_) > 1e-15:
                        t_ = num_ / den_
                        t0, t1 = (max(t0, t_), t1) if den_ < 0 else (t0, min(t1, t_))
            return (p + t0 * dv, p + t1 * dv) if t1 - t0 > 1e-9 else None

        ipath = VGroup()
        for k in range(1, 7):
            cp = clip(fx[k], fx[k + 1])
            if cp is not None:
                ipath.add(Line(inset.c2p(*cp[0]), inset.c2p(*cp[1]), color=GREY_B, stroke_width=2))
        tab = VGroup(MathTex(r"k", r"\quad |f(x_k) - y|", font_size=24, color=GREY_A))
        for k in range(7):
            tab.add(MathTex(rf"{k}", rf"\quad {res[k]:.4f}" if res[k] >= 1e-3 else rf"\quad {sci(float(res[k]), 2)}",
                            font_size=24))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        regrid(tab, gap=0.35)
        tab.next_to([mag.frame.get_right()[0] + 0.4, top, 0], DR, buff=0)
        ratio = float(np.median(res[2:8] / res[1:7]))
        assert abs(ratio - 0.31) < 0.01 and abs(lip - 0.42) < 0.005  # the narration: "0.42", "about a third"
        note_ = VGroup(label(rf"on the green ball, which holds every iterate: \ $\|\varphi'\| \le {lip:.2f}$,",
                             font_size=22, color=C.CONNECTED_SET),
                       label(rf"so each error is at most ${lip:.2f}$ of the last; \ here about ${ratio:.2f}$", font_size=22,
                             color=C.CONNECTED_SET)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        note_.next_to(VGroup(dax, iax), DOWN, buff=0.3).align_to(dax, LEFT)
        assert lip < 0.5 and np.all(np.diff(res[:8]) < 0) and np.all(np.linalg.norm(its[:8] - a, axis=1) < r)
        assert tab.get_right()[0] <= 6.6 and note_.get_bottom()[1] > -3.6 and mag.tag.get_top()[1] < tl.get_bottom()[1]
        assert dax.get_left()[0] >= -6.6 and tl.get_top()[1] < head.get_bottom()[1] - 0.1
        with self.voiceover(
            "<bookmark mark='a'/> Here it is, run. Choose a target y near f of a. <bookmark mark='b'/> Start at a and "
            "apply the correction again and again. On the left, the iterates in the domain; on the right, their "
            "images, closing in on y. <bookmark mark='c'/> On the green ball, which holds every iterate, the correction "
            "map shrinks distances by a factor of at most 0.42, and here each error is about a third of the one "
            "before. "
            "<bookmark mark='d'/> If we updated A at every step, using the derivative at the current point, this "
            "would be Newton's method from the opening, and it would converge even faster."
        ) as vo:
            self.play(FadeIn(head), Create(dax), Create(iax), FadeIn(tl), FadeIn(adot), FadeIn(al), FadeIn(bdot),
                      FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(ydot, scale=1.5), FadeIn(yl))
            vo.wait_until("b")
            self.play(FadeIn(xdots[0]), FadeIn(fdots[0]), FadeIn(tab[0]), FadeIn(tab[1]))
            self.play(Create(xpath[0]), FadeIn(xdots[1]), Create(fpath[0]), FadeIn(fdots[1]), FadeIn(tab[2]),
                      run_time=0.7)
            self.play(Create(mag.src), Create(mag.guides), FadeIn(mag.frame), FadeIn(mag.tag), FadeIn(iy), run_time=0.7)
            for k in range(2, 7):
                extra = [FadeIn(ifd[k - 2])] + ([Create(ipath[k - 2])] if k - 2 < len(ipath) else [])
                self.play(Create(xpath[k - 1]), FadeIn(xdots[k]), Create(fpath[k - 1]), FadeIn(fdots[k]),
                          FadeIn(tab[k + 1]), *extra, run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(ball), FadeIn(bimg), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()
