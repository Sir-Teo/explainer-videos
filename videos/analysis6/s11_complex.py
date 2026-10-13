from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import area_under, load, plain_axes, polyline, square_axes, trap


class ComplexMeasures(VoiceoverScene):
    def construct(self):
        self.card()
        self.path()
        self.signed()
        self.singular()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(10, r"Complex measures", r"How big is a measure that can cancel itself?", lit=(), part=6)
        with self.voiceover("Chapter ten: measures that take negative and complex values."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def path(self):
        d = load("cpath")
        P, ns, lengths, tv = d["P"], d["ns"], d["lengths"], float(d["tv"])
        R = float(np.abs(P).max()) * 1.15
        ax = square_axes([-R, R, 0.25], [-R, R, 0.25], 2.6 / R).move_to([-3.5, -0.6, 0])
        ax.set_opacity(0.35)
        re_l = MathTex(r"\mathrm{Re}", font_size=22, color=GREY_B).next_to(ax, RIGHT, buff=0.05).shift(DOWN * 0.0)
        curve = VMobject(color=C.MEASURE, stroke_width=3).set_points_as_corners([ax.c2p(z.real, z.imag) for z in P])
        o = Dot(ax.c2p(0, 0), radius=0.06, color=WHITE)
        tT = ValueTracker(0.0)
        tip = always_redraw(lambda: Dot(ax.c2p(P[int(tT.get_value() * (len(P) - 1))].real,
                                               P[int(tT.get_value() * (len(P) - 1))].imag), radius=0.08, color=C.EPS))
        tl = always_redraw(lambda: MathTex(rf"\mu([0, t]), \ t = {2 * math.pi * tT.get_value():.2f}", font_size=26,
                                           color=C.EPS).next_to(ax, UP, buff=0.1))
        polys = []
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.EPS), i / (len(ns) - 1)) for i in range(len(ns))]
        for i, k in enumerate(ns):
            idx = np.linspace(0, len(P) - 1, k + 1).astype(int)
            polys.append(VMobject(color=cols[i], stroke_width=3).set_points_as_corners(
                [ax.c2p(P[j].real, P[j].imag) for j in idx]))
        reads = [MathTex(rf"{k} \text{{ pieces: }} \sum |\mu(E_i)| = {L:.4f}", font_size=28, color=cols[i]).move_to(
            [3.6, -0.2, 0]) for i, (k, L) in enumerate(zip(ns, lengths))]
        assert np.all(np.diff(lengths) > 0) and lengths[-1] < tv and abs(tv - 2 * math.pi) < 1e-8
        top = VGroup(
            MathTex(r"d\mu = (1 + \tfrac12 \cos x)\, e^{3ix}\, dx \ \text{ on } [0, 2\pi]", font_size=30),
            MathTex(r"\mu([0, 2\pi]) = 0", font_size=30, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, 1.7, 0])
        bot = VGroup(
            label(r"\textbf{RCA 6.1} \ $|\mu|(E) = \sup \sum_i |\mu(E_i)|$ \ over partitions of $E$", font_size=24),
            label(r"= the length of the path $t \mapsto \mu([0, t])$", font_size=24, color=GREY_A),
            MathTex(rf"|\mu|([0, 2\pi]) = \int_0^{{2\pi}} |h|\,dx = 2\pi = {tv:.4f}", font_size=28, color=C.EPS),
            label(r"\textbf{RCA 6.2, 6.4} \ $|\mu|$ is a positive measure, \ and $|\mu|(X) < \infty$", font_size=24,
                  color=C.MEASURE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -1.9, 0])
        head = label(r"A complex measure as a path in $\C$: \ total mass $0$, \ total variation $2\pi$", font_size=32).to_edge(
            UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> A complex measure assigns a complex number to each measurable set, countably "
            "additively. Here's one with density one plus half cosine x, times e to the three i x. "
            "<bookmark mark='b'/> Follow the measure of zero to t, as t runs from zero to two pi: it traces a loop in "
            "the complex plane, and comes back to zero. The whole interval has measure zero. "
            "<bookmark mark='c'/> But the measure isn't small. Cut the interval into pieces and add the sizes of their "
            "measures: these are the sides of a polygon inscribed in the loop. Finer cuts give longer polygons: "
            "<bookmark mark='d'/> point six eight, four, five point six six, and on toward two pi. "
            "<bookmark mark='e'/> The supremum is the total variation, the length of the loop. Rudin proves that it's "
            "always a positive measure, and always finite."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(o), FadeIn(top[0]))
            vo.wait_until("b")
            self.add(tip, tl)
            self.play(Create(curve), tT.animate.set_value(1.0), run_time=4.0, rate_func=linear)
            self.play(FadeIn(top[1]))
            vo.wait_until("c")
            self.remove(tip, tl)
            tip.clear_updaters()
            tl.clear_updaters()
            self.play(curve.animate.set_stroke(opacity=0.4), Create(polys[0]), FadeIn(reads[0]))
            vo.wait_until("d")
            for i in range(1, len(polys) - 1):
                self.play(ReplacementTransform(polys[i - 1], polys[i]), FadeTransform(reads[i - 1], reads[i]),
                          run_time=1.0)
            vo.wait_until("e")
            self.play(ReplacementTransform(polys[-2], polys[-1]), FadeTransform(reads[-2], reads[-1]))
            self.play(FadeIn(bot[:3]))
            self.play(FadeIn(bot[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def signed(self):
        d = load("variation")
        tv = float(d["tv"])
        ax = plain_axes([0, 2 * math.pi, math.pi / 2], [-1.3, 1.3, 1], 7.0, 3.0, numbers=False).move_to([-3.2, 0.5, 0])
        x = np.linspace(0, 2 * math.pi, 2001)
        y = np.sin(5 * x)
        g = polyline(ax, x, y, color=WHITE, stroke_width=3)
        pos = area_under(ax, x, np.maximum(y, 0), C.MEASURE, 0.55)
        neg = area_under(ax, x, np.minimum(y, 0), C.SEQ, 0.55)
        A = VGroup()
        for k in range(5):
            a, b = 2 * math.pi * k / 5, 2 * math.pi * k / 5 + math.pi / 5
            A.add(Line(ax.c2p(a, -1.55), ax.c2p(b, -1.55), color=C.MEASURE, stroke_width=8))
        A_l = MathTex(r"A", font_size=26, color=C.MEASURE).next_to(A, LEFT, buff=0.15)
        xf = np.linspace(0, 2 * math.pi, 400001)
        Pp = trap(np.maximum(np.sin(5 * xf), 0), xf)
        assert abs(Pp - 2) < 1e-6 and abs(tv - 4) < 1e-6
        rows = VGroup(
            MathTex(r"d\mu = \sin 5x\, dx: \quad \mu([0, 2\pi]) = 0", font_size=30),
            MathTex(rf"\mu^+ = \mu(\,\cdot \cap A) : \ \mu^+(X) = {Pp:.4f}", font_size=28, color=C.MEASURE),
            MathTex(rf"\mu^- = -\mu(\,\cdot \cap B) : \ \mu^-(X) = {Pp:.4f}", font_size=28, color=C.SEQ),
            MathTex(rf"|\mu| = \mu^+ + \mu^- : \ |\mu|(X) = \int |\sin 5x| = {tv:.4f}", font_size=28, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-2.4, -2.7, 0])
        thm = VGroup(label(r"\textbf{RCA 6.14} \ (Hahn) \ a real measure", font_size=28),
                     label(r"splits $X = A \cup B$:", font_size=28),
                     label(r"$\mu \ge 0$ on subsets of $A$,", font_size=28, color=C.MEASURE),
                     label(r"$\mu \le 0$ on subsets of $B$", font_size=28, color=C.SEQ),
                     label(r"(Jordan) \ $\mu = \mu^+ - \mu^-$, \ $|\mu| = \mu^+ + \mu^-$", font_size=28,
                           color=C.EPS))
        for r_ in thm:
            if r_.width > 5.6:
                r_.width = 5.6
        thm.arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to([0.85, 0.3, 0], RIGHT, buff=0)
        head = label(r"Real measures: \ split the space where the measure is positive", font_size=32).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> A real measure is a special case: sine of five x, dx. Its total is zero. "
            "<bookmark mark='b'/> Hahn's theorem splits the space into a set A where the measure is positive, the "
            "orange humps, and its complement B, where it's negative. <bookmark mark='c'/> Jordan's decomposition "
            "writes the measure as the difference of two positive measures, each of total mass two, and the total "
            "variation is their sum, four."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(g), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(pos), FadeIn(neg))
            self.play(Create(A), FadeIn(A_l), FadeIn(thm[:4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1:]), FadeIn(thm[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def singular(self):
        d = load("cantorac")
        xs, F, lens = d["xs"], d["F"], d["lens"]
        W, H = 3.6, 2.8
        axes = [plain_axes([0, 1, 0.5], [0, 1, 0.5], W, H, numbers=True, font_size=16,
                           x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                           y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([x, 0.15, 0])
                for x in (-4.6, -0.1, 4.4)]
        x = np.linspace(0, 1, 400)
        g1 = polyline(axes[0], x, x**2, color=C.CONNECTED_SET, stroke_width=4)
        g2 = VGroup(Line(axes[1].c2p(0, 0), axes[1].c2p(0.5, 0), color=C.PATHOLOGY, stroke_width=4),
                    Line(axes[1].c2p(0.5, 1), axes[1].c2p(1, 1), color=C.PATHOLOGY, stroke_width=4),
                    DashedLine(axes[1].c2p(0.5, 0), axes[1].c2p(0.5, 1), color=C.PATHOLOGY, stroke_width=1.5),
                    Dot(axes[1].c2p(0.5, 1), radius=0.06, color=C.PATHOLOGY))
        g3 = polyline(axes[2], xs, F, color=C.MEASURE, stroke_width=3)
        titles = VGroup(MathTex(r"d\lambda = 2x\,dx", font_size=28, color=C.CONNECTED_SET),
                        MathTex(r"\delta_{1/2}", font_size=28, color=C.PATHOLOGY),
                        MathTex(r"\text{the Cantor measure}", font_size=28, color=C.MEASURE))
        for t_, a in zip(titles, axes):
            t_.next_to(a, UP, buff=0.12)
        F_l = label(r"each drawn by $F(x) = \mu([0, x])$", font_size=24, color=GREY_A).to_edge(UP, buff=0.95)
        verdicts = VGroup(
            label(r"$\ll m$: \ absolutely continuous", font_size=22, color=C.CONNECTED_SET),
            label(r"$\perp m$: \ an atom", font_size=22, color=C.PATHOLOGY),
            label(r"$\perp m$, \ no atoms", font_size=22, color=C.MEASURE),
        )
        for v_, a in zip(verdicts, axes):
            v_.next_to(a, DOWN, buff=0.15)
        # the Cantor measure: 2^n intervals of length 3^-n carry all the mass
        n = 4
        ivs = [(0.0, 1.0)]
        for _ in range(n):
            ivs = [iv for a, b in ivs for iv in ((a, a + (b - a) / 3), (b - (b - a) / 3, b))]
        assert abs(sum(b - a for a, b in ivs) - lens[n]) < 1e-12
        band = VGroup(*[Line(axes[2].c2p(a, 0), axes[2].c2p(b, 0), color=C.EPS, stroke_width=7) for a, b in ivs])
        rows = VGroup(
            label(r"\textbf{RCA 6.7} \ $\lambda \ll \mu$: \ $\mu(E) = 0 \Rightarrow \lambda(E) = 0$; \quad "
                  r"$\lambda \perp \mu$: \ they live on disjoint sets", font_size=24),
            MathTex(r"\text{the Cantor measure: } 2^n \text{ intervals of length } 3^{-n}, \text{ total } (\tfrac23)^n = "
                    + ",\\ ".join(f"{v:.3f}" for v in lens[1:6]) + r",\ \ldots \to 0", font_size=24, color=C.EPS),
            label(r"carry all of its mass, \ and each point has mass $0$: \ singular, \ but continuous", font_size=24,
                  color=C.MEASURE),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.25)
        head = label(r"Three ways to be a measure on $[0, 1]$", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> How can one measure relate to another? Draw three measures on the unit interval "
            "through their distribution functions, the measure of zero to x. <bookmark mark='b'/> The first has a "
            "density, two x. It's absolutely continuous with respect to length: sets of length zero get measure zero. "
            "<bookmark mark='c'/> The second is a point mass at one half, a jump. It lives on a single point, a set "
            "of length zero: it's singular. <bookmark mark='d'/> The third is the Cantor measure, Part 1's staircase "
            "seen as a measure. Its mass sits on the Cantor set: the 2 to the n intervals of the n-th stage carry "
            "everything, while their total length, two thirds to the n, goes to zero. Singular, yet with no atoms at "
            "all. The next chapter shows these are the only possibilities."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(F_l), *[Create(a) for a in axes])
            self.play(Create(g1))
            vo.wait_until("b")
            self.play(FadeIn(titles[0]))
            self.play(FadeIn(verdicts[0]))
            vo.wait_until("c")
            self.play(Create(g2), FadeIn(titles[1]))
            self.play(FadeIn(verdicts[1]), FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(Create(g3), FadeIn(titles[2]), run_time=2.0)
            self.play(FadeIn(band), FadeIn(rows[1]))
            self.play(FadeIn(verdicts[2]), FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()
