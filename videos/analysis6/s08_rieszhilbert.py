from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import left_y_axis, load, plain_axes, polyline, right_angle, square_axes


class RieszHilbert(VoiceoverScene):
    def construct(self):
        self.card()
        self.stacks()
        self.proof()
        self.functions()
        self.evaluation()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Every functional is an inner product", r"What does a bounded linear functional look like?",
                            lit=(), part=6)
        with self.voiceover("Chapter seven: in a Hilbert space, every bounded linear functional is an inner product "
                            "with one fixed vector."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def stacks(self):
        ax = square_axes([-2.2, 2.2, 1], [-2.2, 2.2, 1], 1.15).move_to([-3.4, -0.6, 0])
        ax.set_opacity(0.3)
        y = np.array([2.0, 1.0])
        ny = float(np.linalg.norm(y))
        nrm = y / ny
        tang = np.array([-nrm[1], nrm[0]])
        lines = VGroup()
        for k in range(-4, 5):
            p0 = k / ny * nrm
            a, b = p0 - 3.2 * tang, p0 + 3.2 * tang
            # clip to the window
            ts = np.linspace(-3.2, 3.2, 400)
            pts = np.array([p0 + t * tang for t in ts])
            ok = (np.abs(pts[:, 0]) <= 2.2) & (np.abs(pts[:, 1]) <= 2.2)
            if ok.sum() < 2:
                continue
            seg = Line(ax.c2p(*pts[ok][0]), ax.c2p(*pts[ok][-1]), color=C.EPS if k == 0 else C.FUNCTIONAL,
                       stroke_width=4 if k == 0 else 1.8)
            if k != 0:
                seg.set_stroke(opacity=0.75)
            lines.add(seg)
        ker_l = MathTex(r"\ker \Lambda", font_size=26, color=C.EPS).move_to(ax.c2p(-1.45, 2.0))
        lev = VGroup()
        for k in (-2, -1, 1, 2, 3):  # each value on its own line (boxed), where the line is clear of both axes
            for t_ in (1.75, 1.45, 1.15, 2.0, -1.45, -1.75):
                q_ = k / ny * nrm + t_ * tang
                if np.all(np.abs(q_) <= 1.95) and np.all(np.abs(q_) >= 0.35):
                    break
            else:
                raise AssertionError(k)
            lev.add(tagged(str(k), color=C.FUNCTIONAL, font_size=22).move_to(ax.c2p(*q_)))
        yarr = Arrow(ax.c2p(0, 0), ax.c2p(*y), buff=0, color=C.INNER, stroke_width=5, tip_length=0.2)
        y_l = MathTex(r"y = (2, 1)", font_size=26, color=C.INNER).next_to(ax.c2p(*y), RIGHT, buff=0.1)
        ra = right_angle(ax, (0, 0), nrm, tang, size=0.2, color=GREY_B)
        xT = ValueTracker(0.0)

        def xv():
            s = xT.get_value()
            return np.array([1.2 * math.cos(s) - 0.3, 0.9 * math.sin(s) + 0.8 * math.cos(s)])

        xd = always_redraw(lambda: Dot(ax.c2p(*xv()), radius=0.08, color=WHITE))
        shown = ValueTracker(2)

        def readout():
            rows = VGroup(
                MathTex(rf"x = ({xv()[0]:.2f},\ {xv()[1]:.2f})", font_size=28),
                MathTex(rf"\Lambda x = 2x_1 + x_2 = {2 * xv()[0] + xv()[1]:.2f}", font_size=28, color=C.FUNCTIONAL),
                MathTex(rf"\langle x, y\rangle = {xv() @ y:.2f}", font_size=28, color=C.INNER),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, 1.15, 0])
            return VGroup(*rows[:int(shown.get_value())])

        rd = always_redraw(readout)
        facts = VGroup(
            label(r"level sets of $\Lambda$: \ parallel lines, \ spacing $1/\|y\|$", font_size=24),
            label(r"$\Lambda x$ = how many lines $x$ has crossed", font_size=24),
            label(r"$y$ is perpendicular to $\ker \Lambda$", font_size=24, color=C.INNER),
            MathTex(rf"\|\Lambda\| = \sup_{{\|x\| = 1}} |\Lambda x| = \|y\| = \sqrt 5 = {ny:.4f}", font_size=28,
                    color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.4, -1.45, 0])
        th = np.linspace(0, 2 * np.pi, 3601)
        vals = 2 * np.cos(th) + np.sin(th)
        assert abs(vals.max() - math.sqrt(5)) < 1e-6
        unit = Circle(radius=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], color=GREY_B, stroke_width=2).move_to(ax.c2p(0, 0))
        best = Dot(ax.c2p(*nrm), radius=0.08, color=C.EPS)
        head = label(r"A functional on $\R^2$: \ $\Lambda x = 2x_1 + x_2$, \ drawn as a stack of lines",
                     font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Start in the plane. A linear functional, two x one plus x two, is best drawn as a "
            "stack of parallel lines, its level sets, with the zero level, the kernel, in yellow. "
            "<bookmark mark='b'/> The value at a point counts how many lines you've crossed to get there. "
            "<bookmark mark='c'/> And there's a vector hiding in the stack: y equals two, one, perpendicular to the "
            "lines. At every point, the functional equals the inner product with y. <bookmark mark='d'/> The norm of "
            "the functional, its largest value on the unit circle, is the length of y, root five. Riesz's theorem "
            "says this picture holds in every Hilbert space."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.1), FadeIn(ker_l), run_time=2.0)
            self.play(FadeIn(lev), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(xd), FadeIn(rd), FadeIn(facts[1]))
            self.play(xT.animate.set_value(2 * math.pi), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            shown.set_value(3)
            self.play(GrowArrow(yarr), FadeIn(y_l), Create(ra), FadeIn(facts[2]))
            self.play(xT.animate.set_value(3.5 * math.pi), run_time=3.0)
            vo.wait_until("d")
            self.play(Create(unit), FadeIn(best, scale=2), FadeIn(facts[3]))
        for m in (xd, rd):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        head = VGroup(label(r"Every bounded functional is an inner product", font_size=34),
                      label(r"\textbf{RCA 4.12} \ (F.~Riesz, 1907) \ if $\Lambda$ is a bounded linear functional on $H$,",
                            font_size=26),
                      MathTex(r"\Lambda x = \langle x, y\rangle \ \text{ for a unique } y \in H, \qquad \|\Lambda\| = \|y\|",
                              font_size=30, color=C.EPS)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        rows = [
            MathTex(r"M", r"=", r"\ker \Lambda \ \text{ is closed};\ \text{pick } z \perp M,\ \|z\| = 1", font_size=32),
            MathTex(r"(\Lambda x) z - (\Lambda z) x", r"\in", r"M \quad \text{for every } x", font_size=32),
            MathTex(r"(\Lambda x)\langle z, z\rangle - (\Lambda z)\langle x, z\rangle", r"=", r"0", font_size=32),
            MathTex(r"\Lambda x", r"=", r"\langle x,\ \overline{\Lambda z}\, z\rangle", font_size=32),
        ]
        whys = [why(r"continuity; \ the projection theorem, if $M \ne H$"), why(r"apply $\Lambda$: \ it gives $0$"),
                why(r"take the inner product with $z \perp M$"), why(r"so $y = \overline{\Lambda z}\, z$")]
        step = ladder(self, rows, whys, keep=4, top=1.3, buff=0.45, x=-1.0)
        # the picture the proof follows, small: the kernel, its parallel level sets, and the unit normal z
        c0 = np.array([-4.55, -2.55, 0])
        sc = 1.3  # the picture sits in the free lower-left strip, below and left of the proof rows
        nrm = np.array([1.0, 2.0, 0]) / math.sqrt(5)
        tang = np.array([-nrm[1], nrm[0], 0])
        mini = VGroup()
        for k in range(-2, 3):
            mini.add(Line(c0 + sc * (0.36 * k * nrm - 0.8 * tang), c0 + sc * (0.36 * k * nrm + 0.8 * tang),
                          color=C.EPS if k == 0 else C.FUNCTIONAL, stroke_width=3 if k == 0 else 1.6,
                          stroke_opacity=0.5 if k == 0 else 0.75))
        zarr = Arrow(c0, c0 + sc * 0.62 * nrm, buff=0, color=C.INNER, stroke_width=6, tip_length=0.2)
        mini_l = VGroup(MathTex(r"M = \ker\Lambda", font_size=26, color=C.EPS).next_to(c0 + sc * 0.8 * tang, LEFT, buff=0.08),
                        MathTex(r"z", font_size=30, color=C.INNER).next_to(c0 + sc * 0.62 * nrm, RIGHT, buff=0.08))
        # the key step drawn, with Lambda = <., z> (so Lambda z = 1): (Lambda x) z - x = -<x, t> t lies on M
        xv = 0.55 * tang + 0.6 * nrm
        lx = float(np.dot(xv, nrm))
        comb = lx * nrm - xv
        assert abs(np.dot(comb, nrm)) < 1e-12  # the combination is perpendicular to z: it is in the kernel
        xarr = Arrow(c0, c0 + sc * xv, buff=0, color=WHITE, stroke_width=5, tip_length=0.18)
        xl = MathTex("x", font_size=30).next_to(c0 + sc * xv, LEFT, buff=0.08)
        shadow = DashedLine(c0 + sc * xv, c0 + sc * lx * nrm, color=GREY_B, stroke_width=2)
        lz = Dot(c0 + sc * lx * nrm, radius=0.06, color=C.INNER)
        # the combination lies in the kernel, so it runs along the (dimmed) kernel line: drawn in its own colour
        carr = Arrow(c0, c0 + sc * comb, buff=0, color=C.DELTA, stroke_width=6, tip_length=0.18)
        cl = MathTex(r"(\Lambda x) z - (\Lambda z) x", font_size=24, color=C.DELTA).next_to(c0 + sc * comb, DR, buff=0.12)
        pic = VGroup(mini, zarr, mini_l, xarr, xl, shadow, lz, carr, cl)
        assert pic.get_left()[0] > -6.95 and pic.get_bottom()[1] > -3.95 and pic.get_top()[1] < -1.05
        note_ = label(r"$z$ is the normal to the kernel: \ the arrow in the stack of lines", font_size=26,
                      color=C.INNER).move_to([1.6, -3.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The theorem: every bounded linear functional on a Hilbert space is the inner "
            "product with a unique vector y, and the norm of the functional is the length of y. "
            "<bookmark mark='b'/> The proof follows the picture. The kernel is a closed subspace. If it's not "
            "everything, the projection theorem gives a unit vector z perpendicular to it. "
            "<bookmark mark='c'/> For any x, this combination is in the kernel: apply lambda and it cancels. "
            "<bookmark mark='d'/> So it's perpendicular to z. <bookmark mark='e'/> Expand, and lambda of x is the "
            "inner product of x with the conjugate of lambda z, times z. <bookmark mark='f'/> The representing "
            "vector is the normal to the kernel, scaled."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), LaggedStart(*[Create(m_) for m_ in mini], lag_ratio=0.15), FadeIn(mini_l[0]))
            vo.wait_until("b")
            self.play(GrowArrow(zarr), FadeIn(mini_l[1]))
            step(0)
            vo.wait_until("c")
            step(1)
            self.play(GrowArrow(xarr), FadeIn(xl))
            self.play(Create(shadow), FadeIn(lz))
            self.play(GrowArrow(carr), FadeIn(cl))
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            step(3)
            vo.wait_until("f")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def functions(self):
        d = load("rieszh")
        coef, xs, w, partials, Ns, errs, nrm = d["coef"], d["xs"], d["w"], d["partials"], d["Ns"], d["errs"], float(d["norm"])
        ax = plain_axes([-1, 1, 0.5], [-2.0, 2.0, 1], 5.4, 3.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.6, -0.75, 0])
        gw = polyline(ax, xs, w, color=C.INNER, stroke_width=5).set_stroke(opacity=0.5)
        gw_l = MathTex(r"w(x) = \sin 3x + x", font_size=26, color=C.INNER).next_to(ax, UP, buff=0.1)
        curves = [polyline(ax, xs, p, color=C.EPS, stroke_width=3) for p in partials]
        clabels = [MathTex(rf"\sum_{{n < {N}}} \overline{{\Lambda e_n}}\, e_n: \ \sup|\cdot - w| = {sci(e, 2)}",
                           font_size=26, color=C.EPS).next_to(ax, DOWN, buff=0.15) for N, e in zip(Ns, errs)]
        bx = plain_axes([-1, 12, 1], [-1.0, 2.0, 0.5], 5.0, 2.4).move_to([3.5, 0.15, 0])
        bars = VGroup()
        for n in range(12):
            v = float(coef[n])
            if abs(v) < 1e-12:
                continue
            bars.add(Rectangle(width=0.3, height=abs(bx.c2p(0, v)[1] - bx.c2p(0, 0)[1]), stroke_width=0,
                               fill_color=C.FUNCTIONAL, fill_opacity=0.9).move_to(bx.c2p(n, v / 2)))
        b_l = MathTex(r"\Lambda e_n, \ n = 0, 1, \ldots, 11", font_size=26, color=C.FUNCTIONAL).next_to(bx, UP, buff=0.1)
        bx.x_axis.add_numbers(0, 5, 10, num_decimal_places=0, font_size=18)
        bnum = left_y_axis(bx, (-0.5, 0.5, 1.0, 1.5), decimals=1)
        n_l = MathTex("n", font_size=24, color=GREY_B).next_to(bx.c2p(11.5, 0), DR, buff=0.08)
        # 'a': the black box at work on one f; 'b': its probes, the first Legendre polynomials
        from numpy.polynomial import legendre as Lg
        xg, wg = Lg.leggauss(200)
        lam_f = float(np.sum(wg * (1 + xg) * (np.sin(3 * xg) + xg)))
        gf_ = polyline(ax, xs, 1 + xs, color=C.FUNC, stroke_width=3.5)
        gf_l = VGroup(MathTex(r"f = 1 + x", font_size=26, color=C.FUNC).next_to(ax.c2p(0.55, 1.55), LEFT, buff=0.1),
                      MathTex(rf"\Lambda f = {lam_f:.4f}", font_size=28, color=C.FUNCTIONAL).next_to(ax, DOWN, buff=0.15))
        En = [Lg.legval(xs, [0] * n + [1]) * math.sqrt((2 * n + 1) / 2) for n in range(4)]
        for n in range(4):
            en_g = Lg.legval(xg, [0] * n + [1]) * math.sqrt((2 * n + 1) / 2)
            assert abs(np.sum(wg * en_g * en_g) - 1) < 1e-12
            assert abs(np.sum(wg * en_g * (np.sin(3 * xg) + xg)) - coef[n]) < 1e-10  # the bars are Lambda(e_n)
        assert max(np.abs(e_).max() for e_ in En) < 2.0
        probes = VGroup(*[polyline(ax, xs, e_, color=GREY_B, stroke_width=2).set_stroke(opacity=0.8) for e_ in En])
        probes_l = MathTex(r"e_0, e_1, e_2, e_3", font_size=26, color=GREY_B).next_to(ax, DOWN, buff=0.15)
        side = VGroup(
            label(r"$e_n$: \ the orthonormal Legendre polynomials \ (ch.~8)", font_size=22, color=GREY_A),
            MathTex(r"y = \sum_n \overline{\Lambda e_n}\, e_n \ \text{ represents } \Lambda", font_size=28),
            MathTex(rf"\|\Lambda\| = \|y\|_2 = \Big(\sum |\Lambda e_n|^2\Big)^{{1/2}} = {nrm:.4f}", font_size=28,
                    color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, -2.2, 0])
        assert np.all(np.diff(errs) < 0) and errs[-1] < 1e-4
        assert abs(nrm - math.sqrt(float(np.sum(coef**2)))) < 1e-10
        head = VGroup(label(r"Find the vector from the functional alone", font_size=34),
                      label(r"$\Lambda f = \int_{-1}^1 f(x)\,w(x)\,dx$, \ $w$ hidden", font_size=28, color=GREY_A)
                      ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Now a functional on L two of minus one to one: lambda of f is the integral of f "
            "times a hidden weight w. Can we find w just by testing lambda? <bookmark mark='b'/> Feed it the "
            "orthonormal Legendre polynomials, which chapter eight will build, and record the numbers lambda of e n. "
            "<bookmark mark='c'/> Then the sum of those numbers times e n converges to the representing vector. With "
            "two terms it's crude; with six it's close; with ten the largest error is ten to the minus five. "
            "<bookmark mark='d'/> And it's w, exactly as the theorem promised. The norm of the functional is the "
            "length of w, 1.7595."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(gf_), FadeIn(gf_l))
            vo.wait_until("b")
            self.play(FadeOut(gf_), FadeOut(gf_l), Create(probes), FadeIn(probes_l), Create(bx), FadeIn(bnum), FadeIn(n_l),
                      FadeIn(b_l), FadeIn(side[0]))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeOut(probes), FadeOut(probes_l), FadeIn(side[1]), Create(curves[0]), FadeIn(clabels[0]))
            for k in range(1, len(curves)):
                self.play(ReplacementTransform(curves[k - 1], curves[k]), FadeTransform(clabels[k - 1], clabels[k]),
                          run_time=1.0)
            vo.wait_until("d")
            self.play(Create(gw), FadeIn(gw_l))
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def evaluation(self):
        ax = plain_axes([0, 1, 0.25], [0, 8.5, 2], 5.6, 3.8, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.4, -0.7, 0])
        ns = (1, 4, 16, 64)
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.PATHOLOGY), k / 3) for k in range(4)]
        rects = []
        for n, c in zip(ns, cols):
            h, wdt = math.sqrt(n), 1 / n
            r = Rectangle(width=ax.c2p(wdt, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, h)[1] - ax.c2p(0, 0)[1],
                          stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.25)
            r.move_to(ax.c2p(wdt / 2, h / 2))
            rects.append(r)
            assert abs(h * h * wdt - 1) < 1e-12
        rl = [MathTex(rf"n = {n}: \ \|f_n\|_2 = 1, \ f_n(0) = \sqrt n = {math.sqrt(n):.0f}", font_size=28, color=c)
              .next_to(ax, DOWN, buff=0.15) for n, c in zip(ns, cols)]
        card = museum_card(r"$f \mapsto f(0)$ \ on $L^2$", r"the tall thin bump $\sqrt n\, \mathbf 1_{[0, 1/n]}$",
                           r"boundedness: \ $|f_n(0)| / \|f_n\|_2 = \sqrt n \to \infty$",
                           r"so no $y$ with $f(0) = \langle f, y\rangle$", width=5.4).move_to([3.4, 0.6, 0])
        note_ = VGroup(label(r"on $C[0, 1]$ with the sup norm, \ $f \mapsto f(0)$ is bounded,", font_size=24),
                       label(r"but that space has no inner product:", font_size=24, color=C.MEASURE),
                       label(r"its functionals are measures \ (ch.~12)", font_size=24, color=C.MEASURE)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.4, -2.0, 0])
        if note_.width > 6.4:
            note_.width = 6.4
        head = label(r"The hypothesis \emph{bounded} is not decoration", font_size=34).to_edge(UP, buff=0.3)
        f_l = MathTex(r"f_n = \sqrt n\, \mathbf 1_{[0, 1/n]}", font_size=28).next_to(ax, UP, buff=0.1)
        with self.voiceover(
            "<bookmark mark='a'/> Boundedness matters. Evaluating at zero isn't a bounded functional on L two. "
            "<bookmark mark='b'/> The tall thin bumps, root n on an interval of length one over n, all have norm "
            "one, but their values at zero grow like root n. No vector y can represent evaluation, which is no "
            "surprise: in L two, the value at a single point isn't even defined. <bookmark mark='c'/> On the "
            "continuous functions with the sup norm, evaluation is bounded, but that space has no inner product. "
            "Its functionals turn out to be measures, in chapter twelve."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(f_l))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rects[0]), FadeIn(rl[0]))
            for k in range(1, 4):
                self.play(FadeIn(rects[k]), rects[k - 1].animate.set_fill(opacity=0.06).set_stroke(opacity=0.4),
                          FadeTransform(rl[k - 1], rl[k]), run_time=0.9)
            self.play(FadeIn(card))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()
