from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import cplot, load, square_axes, trap, zcurve


def quartic(z):
    return 1 / (1 + z**4)


class Residues(VoiceoverScene):
    def construct(self):
        self.card()
        self.contour()
        self.table()
        self.rouche()
        self.simply()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"The global Cauchy theorem and residues", r"What does a closed contour see?", lit=(),
                            part=7)
        with self.voiceover("Chapter five: Cauchy's theorem in its global form, and the calculus of residues."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def contour(self):
        d = load("residues")
        poles, res, I1, Q1, semis = d["poles"], d["res"], float(d["I1"]), float(d["Q1"]), d["semis"]
        cx = square_axes([-2.8, 2.8, 1], [-0.6, 2.8, 1], 1.2).move_to([-3.4, -0.75, 0])
        img = cplot(cx, quartic, (-2.8, 2.8), (-0.6, 2.8))
        frame = Rectangle(width=5.6 * 1.2, height=3.4 * 1.2, color=GREY_C, stroke_width=2).move_to(cx.c2p(0, 1.1))
        pm = VGroup(*[Square(side_length=0.2, color=WHITE, stroke_width=2).move_to(cx.c2p(p.real, p.imag)) for p in poles])
        RT = ValueTracker(1.4)

        def path():
            R = RT.get_value()
            t = np.linspace(0, np.pi, 200)
            return VGroup(Line(cx.c2p(-R, 0), cx.c2p(R, 0), color=WHITE, stroke_width=4),
                          zcurve(cx, R * np.exp(1j * t), WHITE, 4))

        pth = always_redraw(path)

        def value():
            R = RT.get_value()
            x = np.linspace(-R, R, 4001)
            t = np.linspace(0, np.pi, 4001)
            seg = trap(quartic(x), x)
            arc = trap(quartic(R * np.exp(1j * t)) * 1j * R * np.exp(1j * t), t)
            return VGroup(MathTex(rf"R = {R:.2f}", font_size=28),
                          MathTex(rf"\int_{{-R}}^R = {seg.real:.6f}", font_size=28),
                          MathTex(rf"\int_{{\text{{arc}}}} = {nz(arc.real, 6):+.6f} {nz(arc.imag, 6):+.6f}i", font_size=28, color=GREY_A),
                          MathTex(rf"\oint = {(seg + arc).real:.6f}", font_size=28, color=C.EPS)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.2, 1.05, 0])

        val = always_redraw(value)
        rows = VGroup(
            MathTex(r"\oint = 2\pi i \sum \mathrm{Res} = 2\pi i\Big(\tfrac{1}{4z^3}\Big|_{e^{i\pi/4}} + "
                    r"\tfrac{1}{4z^3}\Big|_{e^{3i\pi/4}}\Big)", font_size=26),
            MathTex(rf"= \frac{{\pi}}{{\sqrt2}} = {I1:.9f}", font_size=30, color=C.EPS),
            MathTex(rf"\text{{quadrature of }} \int_\R \frac{{dx}}{{1 + x^4}}: \ {Q1:.9f}", font_size=26, color=GREY_A),
            MathTex(r"|\text{arc}| \text{ at } R = 2, 5, 20: \ " + r",\ ".join(sci(v, 1) for v in semis), font_size=24,
                    color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, -2.0, 0])
        assert rows.get_right()[0] <= 6.6 and rows.get_bottom()[1] > -3.65 and rows.get_left()[0] > frame.get_right()[0]
        thm = VGroup(label(r"\textbf{RCA 10.42} \ (residues) \ $f$ holomorphic except at isolated points $a_k$:",
                           font_size=26),
                     MathTex(r"\frac{1}{2\pi i}\oint_\Gamma f\,dz = \sum_k \mathrm{Res}(f; a_k)\,\mathrm{Ind}_\Gamma(a_k)",
                             font_size=32, color=C.EPS)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.2)
        assert abs(I1 - math.pi / math.sqrt(2)) < 1e-14 and abs(Q1 - I1) < 1e-9
        RT.set_value(2.7)  # the readout at its widest and lowest R stays clear of the statement and the rows
        assert value().get_top()[1] < thm.get_bottom()[1] - 0.15 and value().get_bottom()[1] > rows.get_top()[1] + 0.15
        RT.set_value(1.4)
        with self.voiceover(
            "<bookmark mark='a'/> Rudin's global Cauchy theorem says a closed contour only sees what it winds around. "
            "If f is holomorphic except at isolated points, its integral is two pi i times the sum of the residues, "
            "each counted by its winding number. <bookmark mark='b'/> Use it on a real integral: one over one plus x "
            "to the fourth. In the upper half plane it has two poles. Close the interval from minus R to R with a "
            "semicircle. <bookmark mark='c'/> As R grows, the arc's contribution fades, but the total around the "
            "closed contour never changes, because the contour keeps enclosing the same two poles. "
            "<bookmark mark='d'/> Two residues, one over four z cubed at each pole, give pi over root two, and "
            "quadrature agrees to nine digits."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm), FadeIn(img), Create(frame))  # the picture under the statement from the start
            vo.wait_until("b")
            self.play(Create(pm))
            self.play(FadeIn(pth), FadeIn(val))
            vo.wait_until("c")
            self.play(RT.animate.set_value(2.7), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[:2]))
            self.play(FadeIn(rows[2:]))
        for m in (pth, val):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("residues")
        I1, Q1, I2, Q2, b, I3, Q3 = (float(d[k]) for k in ("I1", "Q1", "I2", "Q2", "b", "I3", "Q3"))
        poles = d["poles"]
        X = (-5.65, -3.15, 1.0, 4.85)  # columns: contour, integral, by residues, by quadrature
        hdr = VGroup(label(r"contour", font_size=26, color=GREY_A), label(r"integral", font_size=26, color=GREY_A),
                     label(r"by residues", font_size=26, color=GREY_A), label(r"by quadrature", font_size=26, color=GREY_A))
        rows_ = [
            (r"\int_{-\infty}^\infty \frac{dx}{1 + x^4}", rf"\frac{{\pi}}{{\sqrt2}} = {I1:.9f}", f"{Q1:.9f}",
             r"two poles in the upper half plane"),
            (r"\int_{-\infty}^\infty \frac{\sin x}{x}\,dx", rf"\pi = {I2:.9f}", f"{Q2:.9f}",
             r"$e^{iz}/z$, \ the contour dodges $0$ by a small semicircle"),
            (rf"\int_{{-\infty}}^\infty e^{{-x^2}}\cos({2 * b:.1f}x)\,dx", rf"\sqrt\pi\, e^{{-{b * b:.2f}}} = {I3:.9f}",
             f"{Q3:.9f}", r"no poles at all: \ shift the line to $\mathrm{Im}\,z = 0.7$"),
        ]
        # the three contours, drawn to scale (k = 0.42 scene units per unit of C, R = 1.6)
        k_, R, eps = 0.42, 1.6, 0.3
        assert np.all(np.abs(poles) < R) and np.all(poles.imag > 0) and abs(b - 0.7) < 1e-12

        def P(z, o):
            return o + np.array([z.real * k_, z.imag * k_, 0])

        def path(zs, o, color=WHITE, w=3):
            return VMobject(stroke_color=color, stroke_width=w).set_points_as_corners([P(z, o) for z in zs])

        def pole(z, o):
            return Square(side_length=0.12, color=WHITE, stroke_width=2).move_to(P(z, o))

        def sketch(kind, y):
            o = np.array([X[0], y - (0.25 if kind < 2 else 0.15), 0])
            axis = Line(P(-R - 0.25 + 0j, o), P(R + 0.25 + 0j, o), color=GREY_D, stroke_width=1.5)
            t = np.linspace(0, np.pi, 60)
            if kind == 0:
                g = VGroup(axis, path(np.concatenate([np.linspace(-R, R, 2), R * np.exp(1j * t)]), o),
                           *[pole(z, o) for z in poles])
            elif kind == 1:
                zs = np.concatenate([np.linspace(-R, -eps, 2), eps * np.exp(1j * t[::-1]), np.linspace(eps, R, 2),
                                     R * np.exp(1j * t)])
                g = VGroup(axis, path(zs, o), pole(0j, o))
            else:
                g = VGroup(axis, path(np.array([R + 1j * b, -R + 1j * b]), o, C.EPS, 4),
                           path(np.array([-R + 1j * b, -R + 0j, R + 0j, R + 1j * b]), o))
            return g

        table = VGroup()
        ys = [1.2, -0.25, -1.7]
        for kind, ((a, r, q, note_), y) in enumerate(zip(rows_, ys)):
            row = VGroup(MathTex(a, font_size=30).move_to([X[1], y, 0]), MathTex(r, font_size=28, color=C.EPS).move_to(
                [X[2], y, 0]), MathTex(q, font_size=28, color=GREY_A).move_to([X[3], y, 0]),
                label(note_, font_size=22, color=GREY_B).move_to([X[2], y - 0.55, 0]), sketch(kind, y))
            table.add(row)
        for h, x in zip(hdr, X):
            h.move_to([x, 2.3, 0])
        rule = Line([-6.6, 1.95, 0], [6.6, 1.95, 0], color=GREY_C, stroke_width=1.5)
        for row in table:
            assert row[4].get_right()[0] < row[0].get_left()[0] - 0.2 and row[4].get_left()[0] > -6.65
            assert row[1].get_right()[0] < row[2].get_left()[0] - 0.2 and row[2].get_right()[0] <= 6.6
            assert row[3].get_left()[0] > row[0].get_right()[0] + 0.1 or row[3].get_top()[1] < row[0].get_bottom()[1]
        assert abs(Q2 - I2) < 1e-7 and abs(Q3 - I3) < 1e-9
        head = label(r"Three real integrals, \ three contours", font_size=34).to_edge(UP, buff=0.3)
        foot = label(r"real integrals, \ computed by walking into the complex plane", font_size=26, color=C.EPS).to_edge(
            DOWN, buff=0.4)
        assert table.get_bottom()[1] > foot.get_top()[1] + 0.1
        with self.voiceover(
            "<bookmark mark='a'/> Two more classics. <bookmark mark='b'/> The integral of sine x over x is pi: take e "
            "to the i z over z, and let the contour step around the pole at zero with a tiny semicircle. "
            "<bookmark mark='c'/> And the Gaussian times a cosine needs no poles at all: Cauchy's theorem on a long "
            "rectangle shifts the line of integration up to height 0.7, where the integral is easy. Each answer "
            "matches quadrature to at least seven digits."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(hdr), Create(rule), FadeIn(table[0][:4]), Create(table[0][4]))
            vo.wait_until("b")
            self.play(FadeIn(table[1][:4]), Create(table[1][4]))
            vo.wait_until("c")
            self.play(FadeIn(table[2][:4]), Create(table[2][4]))
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rouche(self):
        d = load("residues")
        roots = d["roots"]
        ax = square_axes([-1.6, 1.6, 1], [-1.6, 1.6, 1], 1.2).move_to([-4.7, -0.7, 0])
        ax.set_opacity(0.35)
        u = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        circ = Circle(radius=u, color=WHITE, stroke_width=2.5).move_to(ax.c2p(0, 0))
        rd = VGroup(*[Dot(ax.c2p(r.real, r.imag), radius=0.08, color=C.EPS if abs(r) < 1 else C.SEQ) for r in roots])
        bx = square_axes([-5.2, 5.2, 2], [-5.2, 5.2, 2], 0.4).move_to([-0.35, -0.7, 0])
        bx.set_opacity(0.35)
        t = np.linspace(0, 2 * np.pi, 1200)
        z = np.exp(1j * t)
        p = z**5 + 3 * z + 1
        img = zcurve(bx, p, C.EPS, 3)
        big = zcurve(bx, 3 * z, GREY_B, 2)
        o = Dot(bx.c2p(0, 0), radius=0.07, color=WHITE)
        wind = (np.unwrap(np.angle(p))[-1] - np.angle(p[0])) / (2 * np.pi)
        assert abs(wind - 1) < 1e-6 and np.all(np.abs(z**5 + 1) < 3) and np.abs(p).max() < 5.2
        top = p[np.argmax(p.imag)]  # the top of the image curve, for its name
        b_lab = VGroup(MathTex(r"3z", font_size=26, color=GREY_B).next_to(bx.c2p(-2.3, 2.3), UL, buff=0.05),
                       MathTex(r"p(z)", font_size=26, color=C.EPS).next_to(bx.c2p(top.real, top.imag), UR, buff=0.08),
                       MathTex(r"0", font_size=24).next_to(o, DL, buff=0.06))
        tT = ValueTracker(0)

        def leash():
            i = int(tT.get_value() * (len(t) - 1))
            return VGroup(Line(bx.c2p((3 * z[i]).real, (3 * z[i]).imag), bx.c2p(p[i].real, p[i].imag), color=C.APPROX,
                               stroke_width=3),
                          Dot(bx.c2p(p[i].real, p[i].imag), radius=0.07, color=C.EPS),
                          Dot(bx.c2p((3 * z[i]).real, (3 * z[i]).imag), radius=0.06, color=GREY_B))

        ls = always_redraw(leash)
        rows = VGroup(
            MathTex(r"p(z) = z^5 + 3z + 1", font_size=30),
            VGroup(label(r"on $|z| = 1$:", font_size=24),
                   label(r"$|p(z) - 3z| = |z^5 + 1| \le 2 < 3 = |3z|$", font_size=24)).arrange(DOWN, aligned_edge=LEFT,
                                                                                             buff=0.1),
            label(r"the leash is shorter than the distance to $0$,", font_size=22, color=GREY_A),
            label(r"so $p$ and $3z$ wind around $0$ equally often:", font_size=22, color=GREY_A),
            MathTex(rf"\text{{winding}} = {wind:.4f}", font_size=28, color=C.EPS),
            VGroup(label(r"\textbf{RCA 10.43} \ (Rouch\'e):", font_size=24, color=C.EPS),
                   label(r"one root in $|z| < 1$", font_size=24, color=C.EPS)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            MathTex(rf"\text{{roots: }} {roots[np.abs(roots) < 1][0].real:.4f}\ \text{{inside}}, \ 4 \text{{ outside}}",
                    font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        rows.align_to(np.array([6.55 - rows.width, 0, 0]), LEFT).set_y(-0.6)
        assert rows.get_right()[0] <= 6.6 and rows.get_left()[0] > bx.get_right()[0] + 0.2
        assert ax.get_left()[0] > -6.65 and bx.get_left()[0] > ax.get_right()[0] + 0.2
        head = label(r"Rouch\'e: \ walk a dog on a short leash around a tree", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> How many roots does z to the fifth plus three z plus one have inside the unit "
            "circle? <bookmark mark='b'/> On the circle, it differs from three z by z to the fifth plus one, which is "
            "at most two, while three z has size three. <bookmark mark='c'/> Picture a person walking around a tree "
            "on the circle of radius three, with a dog on a leash shorter than that. The dog must go around the tree "
            "exactly as often as the person: once. <bookmark mark='d'/> So the polynomial has as many roots inside as "
            "three z: exactly one. That's Rouché's theorem."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(circ), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(bx), FadeIn(o), Create(big), Create(img), FadeIn(b_lab), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(ls), run_time=0.4)
            self.play(tT.animate.set_value(1.0), FadeIn(rows[2:4]), run_time=5.0, rate_func=linear)
            self.play(FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(rd), FadeIn(rows[5:]))
        ls.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def simply(self):
        items = [
            r"$\Omega$ is homeomorphic\\to the disk", r"every closed curve\\shrinks to a point",
            r"$\mathrm{Ind}_\gamma(\alpha) = 0$ for $\alpha \notin \Omega$", r"$S^2 \setminus \Omega$ is connected",
            r"$\oint_\gamma f = 0$ for every $f$ and $\gamma$", r"every $f$ has a primitive",
            r"every $f \ne 0$\\has a logarithm", r"every $f \ne 0$\\has a square root",
            r"every $f$ is a limit\\of polynomials",
        ]
        boxes = VGroup()
        bw, bh = 2.95, 0.95
        for i, t in enumerate(items):
            lab = Tex(r"\begin{tabular}{c}" + t + r"\end{tabular}", font_size=22)
            assert lab.width < bw - 0.2 and lab.height < bh - 0.15  # full size: never shrunk to fit its box
            box = RoundedRectangle(width=bw, height=bh, corner_radius=0.1, stroke_color=C.INNER, stroke_width=2)
            boxes.add(VGroup(box, lab.move_to(box)))
        boxes.arrange_in_grid(rows=3, cols=3, buff=(0.2, 0.22))
        boxes.align_to(np.array([6.55 - boxes.width, 0, 0]), LEFT).set_y(-1.0)
        head = label(r"The many faces of ``simply connected''", font_size=34).to_edge(UP, buff=0.3)
        sub = label(r"\textbf{RCA 13.11} \ for a region $\Omega \subset \C$, \ these nine are equivalent:", font_size=26)
        sub.next_to(boxes, UP, buff=0.3).align_to(boxes, LEFT)
        assert boxes.get_right()[0] <= 6.6 and sub.get_right()[0] <= 6.6 and boxes.get_bottom()[1] > -3.65
        # the failure, computed: on the annulus 1/2 < |z| < 2, the circle |z| = 1 does not shrink, and
        # the integral of 1/z around it is 2 pi i; continuing log z once around adds 2 pi i
        th = np.linspace(0, 2 * np.pi, 4001)
        zc = np.exp(1j * th)
        I = trap(1j * zc / zc, th)
        logz = np.log(zc[0]) + np.concatenate([[0], np.cumsum((1 / ((zc[1:] + zc[:-1]) / 2)) * np.diff(zc))])
        assert abs(I - 2j * np.pi) < 1e-9 and abs(logz[-1] - logz[0] - 2j * np.pi) < 1e-5
        ax = square_axes([-2.2, 2.2, 1], [-2.2, 2.2, 1], 0.68).move_to([-5.15, 0.0, 0])
        ax.set_opacity(0.35)
        u = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        ann = Annulus(inner_radius=0.5 * u, outer_radius=2 * u, fill_color=C.INNER, fill_opacity=0.25, stroke_width=1.5,
                      stroke_color=C.INNER).move_to(ax.c2p(0, 0))
        loop = Circle(radius=u, color=C.EPS, stroke_width=3).move_to(ax.c2p(0, 0))
        loop_tip = Arrow(ax.c2p(1, -0.25), ax.c2p(1, 0.25), buff=0, color=C.EPS, stroke_width=3, tip_length=0.15)
        hole = Dot(ax.c2p(0, 0), radius=0.05, color=C.PATHOLOGY)
        an = VGroup(MathTex(r"\tfrac12 < |z| < 2", font_size=22, color=C.INNER),
                    MathTex(rf"\oint_{{|z| = 1}} \frac{{dz}}{{z}} = {I.imag:.6f}\,i", font_size=22, color=C.EPS),
                    MathTex(r"= 2\pi i \ne 0", font_size=22, color=C.EPS),
                    MathTex(r"\log z \text{ comes back } + 2\pi i", font_size=22, color=C.PATHOLOGY)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, DOWN, buff=0.12)
        an.align_to(np.array([-6.55, 0, 0]), LEFT)
        an[2].shift(RIGHT * 0.35)
        ann_l = VGroup(label(r"a region with a hole:", font_size=22, color=C.PATHOLOGY),
                       label(r"all nine fail", font_size=22, color=C.PATHOLOGY)).arrange(DOWN, buff=0.06).next_to(ax, UP,
                                                                                                              buff=0.1)
        assert an.get_right()[0] < boxes.get_left()[0] - 0.15 and ax.get_right()[0] < boxes.get_left()[0] - 0.1
        assert ann_l.get_top()[1] < head.get_bottom()[1] - 0.1 and an.get_bottom()[1] > -3.65
        with self.voiceover(
            "<bookmark mark='a'/> Rudin collects the region's side of the story in one theorem. For a region in the "
            "plane, nine conditions are equivalent: <bookmark mark='b'/> topological ones, like having no holes; "
            "<bookmark mark='c'/> analytic ones, like Cauchy's theorem for every closed path, or the existence of "
            "logarithms and square roots, or approximation by polynomials, which is Runge's theorem, two chapters "
            "on. The square roots will build the Riemann mapping."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(sub), FadeIn(ann), FadeIn(hole), FadeIn(ann_l), FadeIn(an[0]))
            vo.wait_until("b")
            self.play(Create(loop), GrowArrow(loop_tip), FadeIn(an[1:3]))
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes[:4]], lag_ratio=0.3), FadeIn(an[3]), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes[4:]], lag_ratio=0.3), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()
