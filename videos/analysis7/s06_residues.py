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
                          MathTex(rf"\int_{{\text{{arc}}}} = {arc.real:+.6f} {arc.imag:+.6f}i", font_size=28, color=GREY_A),
                          MathTex(rf"\oint = {(seg + arc).real:.6f}", font_size=28, color=C.EPS)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.2, 1.3, 0])

        val = always_redraw(value)
        rows = VGroup(
            MathTex(r"\oint = 2\pi i \sum \mathrm{Res} = 2\pi i\Big(\tfrac{1}{4z^3}\Big|_{e^{i\pi/4}} + "
                    r"\tfrac{1}{4z^3}\Big|_{e^{3i\pi/4}}\Big)", font_size=26),
            MathTex(rf"= \frac{{\pi}}{{\sqrt2}} = {I1:.9f}", font_size=30, color=C.EPS),
            MathTex(rf"\text{{quadrature of }} \int_\R \frac{{dx}}{{1 + x^4}}: \ {Q1:.9f}", font_size=26, color=GREY_A),
            MathTex(r"|\text{arc}| \text{ at } R = 2, 5, 20: \ " + r",\ ".join(sci(v, 1) for v in semis), font_size=24,
                    color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, -1.75, 0])
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, -1.75, 0])
        thm = VGroup(label(r"\textbf{RCA 10.42} \ (residues) \ $f$ holomorphic except at isolated points $a_k$:",
                           font_size=26),
                     MathTex(r"\frac{1}{2\pi i}\oint_\Gamma f\,dz = \sum_k \mathrm{Res}(f; a_k)\,\mathrm{Ind}_\Gamma(a_k)",
                             font_size=32, color=C.EPS)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.2)
        assert abs(I1 - math.pi / math.sqrt(2)) < 1e-14 and abs(Q1 - I1) < 1e-9
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
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(img), Create(frame), Create(pm))
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
        hdr = VGroup(label(r"integral", font_size=26, color=GREY_A), label(r"by residues", font_size=26, color=GREY_A),
                     label(r"by quadrature", font_size=26, color=GREY_A))
        rows_ = [
            (r"\int_{-\infty}^\infty \frac{dx}{1 + x^4}", rf"\frac{{\pi}}{{\sqrt2}} = {I1:.9f}", f"{Q1:.9f}",
             r"two poles in the upper half plane"),
            (r"\int_{-\infty}^\infty \frac{\sin x}{x}\,dx", rf"\pi = {I2:.9f}", f"{Q2:.9f}",
             r"$e^{iz}/z$, \ the contour dodges $0$ by a small semicircle"),
            (rf"\int_{{-\infty}}^\infty e^{{-x^2}}\cos({2 * b:.1f}x)\,dx", rf"\sqrt\pi\, e^{{-{b * b:.2f}}} = {I3:.9f}",
             f"{Q3:.9f}", r"no poles at all: \ shift the line to $\mathrm{Im}\,z = 0.7$"),
        ]
        table = VGroup()
        ys = [1.5, 0.15, -1.2]
        for (a, r, q, note_), y in zip(rows_, ys):
            row = VGroup(MathTex(a, font_size=30).move_to([-4.3, y, 0]), MathTex(r, font_size=28, color=C.EPS).move_to(
                [0.4, y, 0]), MathTex(q, font_size=28, color=GREY_A).move_to([4.6, y, 0]),
                label(note_, font_size=20, color=GREY_B).move_to([0.4, y - 0.55, 0]))
            table.add(row)
        for h, x in zip(hdr, (-4.3, 0.4, 4.6)):
            h.move_to([x, 2.6, 0])
        rule = Line([-6.6, 2.25, 0], [6.6, 2.25, 0], color=GREY_C, stroke_width=1.5)
        assert abs(Q2 - I2) < 1e-7 and abs(Q3 - I3) < 1e-9
        foot = label(r"real integrals, \ computed by walking into the complex plane", font_size=26, color=C.EPS).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> Two more classics. <bookmark mark='b'/> The integral of sine x over x is pi: take e "
            "to the i z over z, and let the contour step around the pole at zero with a tiny semicircle. "
            "<bookmark mark='c'/> And the Gaussian times a cosine needs no poles at all: Cauchy's theorem on a long "
            "rectangle shifts the line of integration up to height 0.7, where the integral is easy. Each answer "
            "matches quadrature to at least seven digits."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hdr), Create(rule), FadeIn(table[0]))
            vo.wait_until("b")
            self.play(FadeIn(table[1]))
            vo.wait_until("c")
            self.play(FadeIn(table[2]))
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rouche(self):
        d = load("residues")
        roots = d["roots"]
        ax = square_axes([-1.6, 1.6, 1], [-1.6, 1.6, 1], 1.35).move_to([-4.3, -0.7, 0])
        ax.set_opacity(0.35)
        u = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        circ = Circle(radius=u, color=WHITE, stroke_width=2.5).move_to(ax.c2p(0, 0))
        rd = VGroup(*[Dot(ax.c2p(r.real, r.imag), radius=0.08, color=C.EPS if abs(r) < 1 else C.SEQ) for r in roots])
        bx = square_axes([-4.4, 4.4, 2], [-4.4, 4.4, 2], 0.5).move_to([0.6, -0.7, 0])
        bx.set_opacity(0.35)
        t = np.linspace(0, 2 * np.pi, 1200)
        z = np.exp(1j * t)
        p = z**5 + 3 * z + 1
        img = zcurve(bx, p, C.EPS, 3)
        big = zcurve(bx, 3 * z, GREY_B, 2)
        o = Dot(bx.c2p(0, 0), radius=0.07, color=WHITE)
        wind = (np.unwrap(np.angle(p))[-1] - np.angle(p[0])) / (2 * np.pi)
        assert abs(wind - 1) < 1e-6 and np.all(np.abs(z**5 + 1) < 3)
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
            label(r"on $|z| = 1$: \ $|p(z) - 3z| = |z^5 + 1| \le 2 < 3 = |3z|$", font_size=22),
            label(r"the leash is shorter than the distance to $0$,", font_size=22, color=GREY_A),
            label(r"so $p$ and $3z$ wind around $0$ equally often:", font_size=22, color=GREY_A),
            MathTex(rf"\text{{winding}} = {wind:.4f}", font_size=28, color=C.EPS),
            label(r"\textbf{RCA 10.43} \ (Rouch\'e) \ one root in $|z| < 1$", font_size=24, color=C.EPS),
            MathTex(rf"\text{{roots: }} {roots[np.abs(roots) < 1][0].real:.4f}\ \text{{inside}}, \ 4 \text{{ outside}}",
                    font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([5.0, -0.6, 0])
        for r_ in rows:
            if r_.width > 3.9:
                r_.width = 3.9
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([5.0, -0.6, 0])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([5.05, -0.6, 0])
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
            self.play(Create(bx), FadeIn(o), Create(big), Create(img), FadeIn(rows[1]))
            vo.wait_until("c")
            self.add(ls)
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
            r"$\Omega$ is homeomorphic to the disk", r"every closed curve shrinks to a point",
            r"$\mathrm{Ind}_\gamma(\alpha) = 0$ for $\alpha \notin \Omega$", r"$S^2 \setminus \Omega$ is connected",
            r"$\oint_\gamma f = 0$ for every $f$ and $\gamma$", r"every $f$ has a primitive",
            r"every $f \ne 0$ has a logarithm", r"every $f \ne 0$ has a square root",
            r"every $f$ is a limit of polynomials",
        ]
        boxes = VGroup()
        for i, t in enumerate(items):
            lab = label(t, font_size=22)
            if lab.width > 3.6:
                lab.width = 3.6
            box = RoundedRectangle(width=4.0, height=1.0, corner_radius=0.1, stroke_color=C.INNER, stroke_width=2)
            boxes.add(VGroup(box, lab.move_to(box)))
        boxes.arrange_in_grid(rows=3, cols=3, buff=(0.3, 0.3)).move_to(DOWN * 0.4)
        head = VGroup(label(r"\textbf{RCA 13.11} \ for a region $\Omega \subset \C$, \ these nine are equivalent", font_size=30),
                      label(r"the many faces of ``simply connected''", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.1)
        head.to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Rudin collects the region's side of the story in one theorem. For a region in the "
            "plane, nine conditions are equivalent: <bookmark mark='b'/> topological ones, like having no holes; "
            "<bookmark mark='c'/> analytic ones, like Cauchy's theorem for every closed path, or the existence of "
            "logarithms and square roots, or approximation by polynomials, which is Runge's theorem, two chapters "
            "on. The square roots will build the Riemann mapping."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes[:4]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes[4:]], lag_ratio=0.3), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()
