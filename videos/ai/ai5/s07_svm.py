from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import (AUSTEN, DICKENS, crop_to_axes, load, page_dots, page_plane,
                                  region_image)
from videos.ai.ai5.compute import svm_dual

GOLD = C.BITS


def toy_clusters(seed=7):
    g = np.random.default_rng(seed)
    A = g.normal([-1.3, -0.6], 0.45, (14, 2))
    B = g.normal([1.2, 0.8], 0.45, (14, 2))
    return np.vstack([A, B]), np.array([0] * 14 + [1] * 14)


def toy_ring(seed=8):
    g = np.random.default_rng(seed)
    r_in, r_out = g.uniform(0, 0.9, 40), g.uniform(1.5, 2.1, 60)
    t_in, t_out = g.uniform(0, 2 * math.pi, 40), g.uniform(0, 2 * math.pi, 60)
    P = np.vstack([np.stack([r_in * np.cos(t_in), r_in * np.sin(t_in)], 1),
                   np.stack([r_out * np.cos(t_out), r_out * np.sin(t_out)], 1)])
    return P, np.array([0] * 40 + [1] * 60)


class SVM(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.street()
        self.lift()
        self.pages()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"The widest street", r"Which line, of all the lines that work?", part=5, lit=(1995,))
        with self.voiceover("Chapter six. Support vector machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def street(self):
        P, y = toy_clusters()
        s = 2 * y - 1.0
        a = svm_dual(P @ P.T + 1, y, C=1e4, epochs=2000)
        w, b = (a * s) @ P, float((a * s).sum())
        f = P @ w + b
        assert np.all(np.sign(f) == s)  # separable
        sv = np.nonzero(a > 1e-6)[0]
        U = 1.15
        C0 = np.array([-0.4, -0.6, 0])

        def S(z):
            return C0 + U * np.array([z[0], z[1], 0])

        dots = VGroup(*[Dot(S(p), radius=0.08, color=AUSTEN if l_ == 0 else DICKENS) for p, l_ in zip(P, y)])
        wn = w / np.linalg.norm(w)
        perp = np.array([-wn[1], wn[0]])
        c0 = -b / np.linalg.norm(w) * wn  # a point on the boundary
        m = 1 / np.linalg.norm(w)
        L = 2.3

        def band(off, color, dashed=False, sw=4):
            p0, p1 = S(c0 + off * wn - L * perp), S(c0 + off * wn + L * perp)
            return (DashedLine if dashed else Line)(p0, p1, color=color, stroke_width=sw)

        mid = band(0, GOLD)
        edges = VGroup(band(m, GREY_A, True, 2.5), band(-m, GREY_A, True, 2.5))
        street = Polygon(S(c0 + m * wn - L * perp), S(c0 + m * wn + L * perp), S(c0 - m * wn + L * perp),
                         S(c0 - m * wn - L * perp), stroke_width=0, fill_color=GOLD, fill_opacity=0.12)
        rings = VGroup(*[Circle(radius=0.16, color=WHITE, stroke_width=3).move_to(S(P[i])) for i in sv])
        # other lines that also separate the two groups
        others = VGroup()
        for ang, sh in ((0.35, 0.1), (-0.3, -0.15), (0.6, 0.0)):
            u = rotate_vector(np.array([*perp, 0]), ang)[:2]
            others.add(Line(S(c0 + sh * wn - L * u), S(c0 + sh * wn + L * u), color=GREY_B, stroke_width=2))
        head = label(r"Of all the lines that separate them, \ the one with the widest margin", font_size=30).to_edge(UP, buff=0.35)
        svl = label(r"support vectors", font_size=28, color=WHITE).next_to(rings, DOWN, buff=0.3).to_edge(RIGHT, buff=0.6)
        tag = label(r"illustrative", font_size=22, color=GREY_B).to_corner(DL, buff=0.3)
        cite_ = cite(r"C.~Cortes \& V.~Vapnik, \textit{Support-Vector Networks} (1995)", corner=DR)
        with self.voiceover(
            "Support vector machines ask for the widest street. Many lines separate these two groups. "
            "<bookmark mark='a'/> Choose the one with the widest empty margin on both sides. "
            "<bookmark mark='b'/> The street's edges rest on just a few points, the support vectors. Move any other "
            "point, and nothing changes. <bookmark mark='c'/> Cortes and Vapnik made it practical in 1995, with a "
            "twist for groups that overlap: points may stand in the street, at a price."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.03), FadeIn(tag))
            self.play(LaggedStart(*[Create(o) for o in others], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(others), FadeIn(street), Create(mid), Create(edges))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.2), FadeIn(svl))
            vo.wait_until("c")
            self.play(FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lift(self):
        P, y = toy_ring()
        axes = ThreeDAxes(x_range=[-2.4, 2.4, 1], y_range=[-2.4, 2.4, 1], z_range=[0, 5, 1], x_length=5.4, y_length=5.4,
                          z_length=3.2, axis_config={"stroke_color": GREY_C, "include_ticks": False, "include_tip": False})
        axes.shift(DOWN * 0.3)
        flat = VGroup(*[Dot(axes.c2p(p[0], p[1], 0), radius=0.06, color=AUSTEN if l_ == 0 else DICKENS)
                        for p, l_ in zip(P, y)])
        high = VGroup(*[Dot(axes.c2p(p[0], p[1], p @ p), radius=0.06, color=AUSTEN if l_ == 0 else DICKENS)
                        for p, l_ in zip(P, y)])
        bowl = Surface(lambda u, v: axes.c2p(u * math.cos(v), u * math.sin(v), u * u), u_range=[0, 2.2],
                       v_range=[0, 2 * math.pi], resolution=(14, 32), fill_opacity=0.12, stroke_width=0.4,
                       stroke_color=GREY_D, checkerboard_colors=False, fill_color=GREY_B)
        cz = 1.45
        cut = Surface(lambda u, v: axes.c2p(u, v, cz), u_range=[-2.3, 2.3], v_range=[-2.3, 2.3], resolution=(2, 2),
                      fill_opacity=0.35, fill_color=GOLD, stroke_width=0, checkerboard_colors=False)
        circle3 = ParametricFunction(lambda t: axes.c2p(math.sqrt(cz) * math.cos(t), math.sqrt(cz) * math.sin(t), cz),
                                     t_range=[0, 2 * math.pi], color=GOLD, stroke_width=5)
        circle0 = ParametricFunction(lambda t: axes.c2p(math.sqrt(cz) * math.cos(t), math.sqrt(cz) * math.sin(t), 0),
                                     t_range=[0, 2 * math.pi], color=GOLD, stroke_width=5)
        colors = {r"x_1^2 + x_2^2": GOLD}
        lf = cmath(r"(x_1, x_2)", r"\;\mapsto\;", r"(x_1,\, x_2,\,", r"x_1^2 + x_2^2", r")", colors=colors, font_size=38)
        lf.to_corner(UL, buff=0.4)
        kt = label(r"the kernel trick: \ only dot products are needed, \\ and a kernel computes them directly",
                   font_size=26, color=GREY_A).to_corner(DL, buff=0.4)
        no_line = label(r"no straight line separates these", font_size=28, color=GREY_A).to_corner(UR, buff=0.4)
        tag = label(r"illustrative", font_size=22, color=GREY_B).to_corner(DR, buff=0.3)
        for m_ in (lf, kt, no_line, tag):
            self.add_fixed_in_frame_mobjects(m_)
            self.remove(m_)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        with self.voiceover(
            "For groups that no straight line can separate, there's a trick. <bookmark mark='a'/> Lift each point "
            "into a third dimension, at a height equal to its squared distance from the centre. "
            "<bookmark mark='b'/> Now a flat plane separates them. <bookmark mark='c'/> And seen from above, that "
            "plane cuts out a circle. <bookmark mark='d'/> The kernel trick does this without ever computing the "
            "lifted points. The method only needs dot products between them, and a kernel, a similarity score "
            "computed straight from two original points, supplies those directly, even for infinitely many "
            "dimensions."
        ) as vo:
            self.play(FadeIn(flat), FadeIn(no_line), FadeIn(tag))
            vo.wait_until("a")
            self.move_camera(phi=68 * DEGREES, theta=-50 * DEGREES, zoom=0.85, run_time=2.0)
            self.play(Create(axes), FadeIn(bowl), Transform(flat, high), Write(lf), run_time=2.0)
            self.begin_ambient_camera_rotation(rate=0.08)
            vo.wait_until("b")
            self.play(FadeIn(cut), Create(circle3))
            vo.wait_until("c")
            self.stop_ambient_camera_rotation()
            self.play(FadeOut(cut), FadeOut(bowl))
            self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=2.0)
            self.play(Transform(flat, VGroup(*[Dot(axes.c2p(p[0], p[1], 0), radius=0.06, color=AUSTEN if l_ == 0 else DICKENS)
                                               for p, l_ in zip(P, y)])), ReplacementTransform(circle3, circle0))
            vo.wait_until("d")
            self.play(FadeIn(kt))
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    def pages(self):
        p = load("pages")
        sv = load("svm")
        X2, y, test = np.asarray(p["X2"]), np.asarray(p["y"]), np.asarray(p["test"], bool)
        plane = page_plane(x_length=7.6, y_length=5.0, center=[-2.2, -0.3, 0])
        ax = plane[0]
        v, xs, ys = crop_to_axes(sv["region"], sv["xs"], sv["ys"])
        img = region_image((v > 0).astype(float), xs, ys, ax, opacity=0.42)
        te = np.nonzero(test)[0]
        dots = page_dots(ax, X2, y, idx=te, jitter=0.35, radius=0.055)
        n_te = int(test.sum())
        a2 = label(rf"Gaussian kernel, \ $2$ rates: \ ${100 * sv['acc_rbf']:.0f}\%$", font_size=30)
        a70 = label(rf"all $70$ rates: \ ${100 * sv['acc70']:.1f}\%$ \ (${round(sv['acc70'] * n_te)}$ of ${n_te}$)",
                    font_size=30, color=C.BITS)
        VGroup(a2, a70).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.3, 0.6, 0])
        # the Gaussian kernel, pictured: a bump on one page; its neighbours lit by how similar they are
        kx = np.linspace(-2.0, 2.0, 80)
        bump = VMobject(stroke_color=C.BITS, stroke_width=3).set_points_smoothly(
            [np.array([u, 1.0 * math.exp(-u * u), 0]) for u in kx])
        nbrs = VGroup(*[Dot([u, 0, 0], radius=0.08, color=C.BITS).set_opacity(0.15 + 0.85 * math.exp(-u * u))
                        for u in (-1.8, -1.2, -0.6, 0.6, 1.2, 1.8)])
        kpic = VGroup(Line([-2.1, 0, 0], [2.1, 0, 0], color=GREY_C, stroke_width=1.5), bump, nbrs,
                      Dot([0, 0, 0], radius=0.1, color=WHITE),
                      MathTex("1", font_size=22, color=C.BITS).next_to([0, 1.0, 0], UP, buff=0.06),
                      label(r"a page", font_size=20, color=WHITE).next_to([0, 0, 0], DOWN, buff=0.15))
        kcard = gloss(r"Gaussian kernel", r"a similarity score between two points:\\ $1$ for identical points, "
                      r"fading towards $0$ with distance", picture=kpic, corner=DR, width=4.4)
        with self.voiceover(
            "Back to the pages, with a Gaussian kernel: a similarity score between two pages that's one when they're "
            "identical, and fades towards zero as they move apart. The boundary bends wherever the data asks it to. "
            f"<bookmark mark='a'/> On new pages, {100 * sv['acc_rbf']:.0f} percent right with two rates. "
            "<bookmark mark='b'/> With all seventy, 99.5 percent, the same as logistic regression."
        ) as vo:
            self.play(Create(ax), FadeIn(plane[1:]), FadeIn(img), FadeIn(kcard))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(a2))
            vo.wait_until("b")
            self.play(FadeIn(a70))
        self.wait(0.3)
        self.clear_scene()
