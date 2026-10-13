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
        dax = square_axes([-1.2, 0.8, 1], [-0.4, 6.8, 1], 0.55, numbers=True, font_size=16,
                          x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                          y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-5.0, -0.55, 0])
        iax = square_axes([-2.4, 2.4, 1], [-2.4, 2.4, 1], 1.0).move_to([0.3, -0.55, 0])
        iax.set_opacity(0.5)
        dom = mapped_grid(dax, lambda P: P, (-1.0, 0.6), (0, 2 * math.pi), n=9, color=GREY_C, stroke_width=1.4)
        img = mapped_grid(iax, F, (-1.0, 0.6), (0, 2 * math.pi), n=9, color=C.OPERATOR, stroke_width=1.6, samples=120)
        a = np.array([0.0, 0.6])
        h = 0.18
        sq = np.array([[-h, -h], [h, -h], [h, h], [-h, h]])
        edge = np.concatenate([np.linspace(sq[i], sq[(i + 1) % 4], 30, endpoint=False) for i in range(4)])

        def patch(ax, Q, color):
            return VMobject(color=color, stroke_width=3, fill_color=color, fill_opacity=0.35).set_points_as_corners(
                [ax.c2p(*q) for q in np.vstack([Q, Q[:1]])])

        s1 = patch(dax, a + edge, C.EPS)
        s2 = patch(dax, a + np.array([0, 2 * math.pi]) + edge, C.APPROX)
        i1 = patch(iax, F(a + edge), C.EPS)
        i2 = patch(iax, F(a + np.array([0, 2 * math.pi]) + edge), C.APPROX)
        assert np.allclose(F(a + edge), F(a + np.array([0, 2 * math.pi]) + edge))
        arrow = Arrow([-3.9, 1.6, 0], [-2.3, 1.6, 0], buff=0, color=GREY_B, stroke_width=4)
        fl = MathTex(r"f(x, y) = (e^x \cos y,\ e^x \sin y)", font_size=30).next_to(arrow, UP, buff=0.1).shift(RIGHT * 0.6)
        side = VGroup(
            label(r"vertical lines $\to$ circles", font_size=24, color=C.OPERATOR),
            label(r"horizontal lines $\to$ rays", font_size=24, color=C.OPERATOR),
            MathTex(r"\det f'(x, y) = e^{2x} \ne 0", font_size=30),
            label(r"near each point: \ one-to-one", font_size=24, color=C.EPS),
            label(r"but $f(x, y + 2\pi) = f(x, y)$:", font_size=24, color=C.APPROX),
            label(r"not one-to-one globally", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([5.0, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the map that sends x, y to e to the x times cosine y, e to the x times sine "
            "y: the complex exponential, seen as a map of the plane. <bookmark mark='b'/> It wraps the strip on the "
            "left around the origin: vertical lines become circles, horizontal lines become rays. "
            "<bookmark mark='c'/> Its derivative is invertible everywhere, and near each point the map is one-to-one: "
            "a small square goes to a small curved square. <bookmark mark='d'/> But a square two pi higher lands in "
            "exactly the same place. The map can be undone near every point, and not globally. The inverse function "
            "theorem is precisely the local statement."
        ) as vo:
            self.play(Create(dax), Create(dom), FadeIn(fl))
            vo.wait_until("a")
            self.play(GrowArrow(arrow))
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
        thm = VGroup(
            label(r"\textbf{Rudin 9.24} \ $f$ is $\mathcal C^1$ near $a$, \ $f'(a)$ is invertible, \ $b = f(a)$:",
                  font_size=30),
            label(r"there are open $U \ni a$ and $V \ni b$ with $f: U \to V$ one-to-one and onto,", font_size=30),
            label(r"and the inverse $g: V \to U$ is $\mathcal C^1$, \ with $g'(y) = f'(g(y))^{-1}$", font_size=30,
                  color=C.EPS),
        ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)
        pm = ProofMap([r"$\varphi_y$ is a contraction", r"$f$ is one-to-one on a ball $U$", r"$V = f(U)$ is open",
                       r"$g' = (f')^{-1}$"], font_size=24, width=3.0, buff=0.3)
        pm.next_to(thm, DOWN, buff=0.6)
        idea = VGroup(
            label(r"the idea: \ to solve $f(x) = y$, \ correct $x$ by the linear guess", font_size=26),
            MathTex(r"x \;\mapsto\; x + A^{-1}\big(y - f(x)\big), \qquad A = f'(a)", font_size=34, color=C.EPS),
            label(r"a fixed point is a solution; \ near $a$ this map barely moves distances", font_size=26,
                  color=GREY_A),
            MathTex(r"\varphi_y'(x) = I - A^{-1} f'(x) \approx 0 \text{ near } a", font_size=32),
        ).arrange(DOWN, buff=0.2).next_to(pm, DOWN, buff=0.5)
        # the statement as a picture: a disk U around a, its image V around b, f one way and g back
        a = np.array([0.0, 0.6])
        r = 0.35
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
        dl = VGroup(MathTex(r"a", font_size=26, color=C.EPS).next_to(dots[0], DL, buff=0.05),
                    MathTex(r"b", font_size=28, color=C.EPS).next_to(dots[1], DR, buff=0.05),
                    MathTex(r"U", font_size=30, color=C.OPEN_SET).next_to(U, UP, buff=0.08),
                    MathTex(r"V = f(U)", font_size=30, color=C.OPEN_SET).next_to(V, UP, buff=0.08))
        fa = Arrow([-1.2, -0.75, 0], [1.2, -0.75, 0], buff=0, color=C.OPERATOR, stroke_width=4)
        ga = Arrow([1.2, -1.55, 0], [-1.2, -1.55, 0], buff=0, color=C.EPS, stroke_width=4)
        fal = MathTex(r"f", font_size=30, color=C.OPERATOR).next_to(fa, UP, buff=0.08)
        gal = MathTex(r"g = f^{-1}", font_size=30, color=C.EPS).next_to(ga, DOWN, buff=0.08)
        assert abs(np.linalg.det(J_exp(a)) - math.exp(2 * a[0])) < 1e-12
        pic = VGroup(dax2, iax2, U, V, g1, g2, dots, dl, fa, ga, fal, gal)
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
            self.play(FadeIn(thm[0]), Create(dax2), Create(U), Create(g1), FadeIn(dots[0]), FadeIn(dl[0]), FadeIn(dl[2]))
            self.play(FadeIn(thm[1]), GrowArrow(fa), FadeIn(fal), Create(iax2), TransformFromCopy(U, V),
                      TransformFromCopy(g1, g2), FadeIn(dots[1]), FadeIn(dl[1]), FadeIn(dl[3]), run_time=2.0)
            self.play(FadeIn(thm[2]), GrowArrow(ga), FadeIn(gal))
            vo.wait_until("b")
            self.play(FadeOut(pic), FadeIn(pm))
            vo.wait_until("c")
            self.play(*pm.light(0), FadeIn(idea[0]), FadeIn(idea[1]))
            self.play(FadeIn(idea[2]))
            vo.wait_until("d")
            self.play(FadeIn(idea[3]))
            self.play(*pm.light(1))
            self.play(*pm.light(2))
            self.play(*pm.light(3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def run(self):
        d = load("inverse")
        a, A, target, its, res, r, lip = d["a"], d["A"], d["target"], d["its"], d["res"], float(d["r"]), float(d["lip"])
        ud, ui = 4.6, 4.4
        dax = square_axes([-0.45, 0.45, 0.25], [0.15, 1.05, 0.25], ud).move_to([-4.75, -0.75, 0])
        dax.set_opacity(0.5)
        b = f_exp(a)
        iax = square_axes([b[0] - 0.4, b[0] + 0.55, 0.25], [b[1] - 0.55, b[1] + 0.4, 0.25], ui).move_to([-0.2, -0.75, 0])
        iax.set_opacity(0.5)
        ball = Circle(radius=ud * r, color=C.CONNECTED_SET, stroke_width=2).move_to(dax.c2p(*a)).set_fill(
            C.CONNECTED_SET, 0.06)
        th = np.linspace(0, 2 * np.pi, 200)
        bimg = VMobject(color=C.CONNECTED_SET, stroke_width=2, fill_color=C.CONNECTED_SET, fill_opacity=0.06)
        bimg.set_points_as_corners([iax.c2p(*F(a + r * np.array([math.cos(t), math.sin(t)]))) for t in th])
        adot = Dot(dax.c2p(*a), radius=0.07, color=WHITE)
        bdot = Dot(iax.c2p(*b), radius=0.07, color=WHITE)
        ydot = Dot(iax.c2p(*target), radius=0.09, color=C.EPS)
        al = MathTex("a", font_size=28).next_to(adot, DL, buff=0.05)
        bl = MathTex("f(a)", font_size=28).next_to(bdot, DL, buff=0.05)
        yl = MathTex("y", font_size=30, color=C.EPS).next_to(ydot, UR, buff=0.05)
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.EPS), k / 7) for k in range(8)]
        xdots = [Dot(dax.c2p(*its[k]), radius=0.06, color=cols[k]) for k in range(8)]
        fdots = [Dot(iax.c2p(*f_exp(its[k])), radius=0.06, color=cols[k]) for k in range(8)]
        xpath = VGroup(*[Line(dax.c2p(*its[k]), dax.c2p(*its[k + 1]), color=GREY_B, stroke_width=2) for k in range(7)])
        fpath = VGroup(*[Line(iax.c2p(*f_exp(its[k])), iax.c2p(*f_exp(its[k + 1])), color=GREY_B, stroke_width=2)
                         for k in range(7)])
        tl = VGroup(label(r"domain: \ the iterates $x_k$", font_size=24).next_to(dax, UP, buff=0.1),
                    label(r"target: \ their images $f(x_k)$", font_size=24).next_to(iax, UP, buff=0.1))
        head = MathTex(r"x_{k+1} = x_k + A^{-1}\big(y - f(x_k)\big)", font_size=34, color=C.EPS).to_edge(UP, buff=0.25)
        tab = VGroup(MathTex(r"k", r"\quad |f(x_k) - y|", font_size=26, color=GREY_A))
        for k in range(7):
            tab.add(MathTex(rf"{k}", rf"\quad {res[k]:.4f}" if res[k] >= 1e-3 else rf"\quad {sci(float(res[k]), 2)}",
                            font_size=26))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to([2.6, 0.9, 0], DR, buff=0)
        regrid(tab, gap=0.35)
        ratio = float(np.median(res[2:8] / res[1:7]))
        assert abs(ratio - 0.31) < 0.01 and abs(lip - 0.42) < 0.005  # the narration: "0.42", "about a third"
        note_ = VGroup(label(r"on the green ball:", font_size=22, color=C.CONNECTED_SET),
                       label(rf"$\|\varphi'\| \le {lip:.2f}$: \ each error is at most", font_size=22, color=C.CONNECTED_SET),
                       label(rf"${lip:.2f}$ of the last; \ here about ${ratio:.2f}$", font_size=22,
                             color=C.CONNECTED_SET)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).next_to(tab, DOWN, buff=0.35, aligned_edge=LEFT)
        assert lip < 0.5 and np.all(np.diff(res[:8]) < 0) and np.all(np.linalg.norm(its[:8] - a, axis=1) < r)
        with self.voiceover(
            "<bookmark mark='a'/> Here it is, run. Choose a target y near f of a. <bookmark mark='b'/> Start at a and "
            "apply the correction again and again. On the left, the iterates in the domain; on the right, their "
            "images, closing in on y. <bookmark mark='c'/> On the green ball, which holds every iterate, the correction "
            "map shrinks distances by a factor of at most 0.42, and here each error is about a third of the one "
            "before. "
            "<bookmark mark='d'/> If we updated A at every step, using the derivative at the current point, this "
            "would be Newton's method from the opening, and it would converge even faster."
        ) as vo:
            self.play(FadeIn(head), Create(dax), Create(iax), FadeIn(tl))
            self.play(FadeIn(adot), FadeIn(al), FadeIn(bdot), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(ydot, scale=1.5), FadeIn(yl))
            vo.wait_until("b")
            self.play(FadeIn(xdots[0]), FadeIn(fdots[0]), FadeIn(tab[0]), FadeIn(tab[1]))
            for k in range(1, 7):
                self.play(Create(xpath[k - 1]), FadeIn(xdots[k]), Create(fpath[k - 1]), FadeIn(fdots[k]),
                          FadeIn(tab[k + 1]), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(ball), FadeIn(bimg), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()
