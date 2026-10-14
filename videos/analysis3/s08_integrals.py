from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import plain_axes, polyline
from videos.analysis3.compute import trap


def base(x):
    return 0.8 + 0.4 * np.sin(2.2 * x) + 0.15 * x


class IntegralsDerivatives(VoiceoverScene):
    def construct(self):
        self.card()
        self.integrals()
        self.derivatives()
        self.summary()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Integrals and derivatives of limits", r"When may we integrate or differentiate term by term?",
                            lit=(), part=3)
        with self.voiceover(
            "Chapter seven: the two remaining swaps from the opening, integrals and derivatives."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def integrals(self):
        a, b = 0.0, 3.0
        ax = plain_axes([0, 3, 1], [0, 2.0, 0.5], 6.4, 4.4).move_to([-3.5, -0.8, 0])
        x = np.linspace(a, b, 1500)
        nT = ValueTracker(1.0)
        seq = lambda n, t: base(t) + np.sin(5 * n * t + 1) / (1.5 * n)  # noqa: E731
        lim = polyline(ax, x, base(x), color=WHITE, stroke_width=3)
        gn = always_redraw(lambda: polyline(ax, x, seq(nT.get_value(), x), color=C.FUNC, stroke_width=3))

        def gap_area():
            n = nT.get_value()
            fx, gx = seq(n, x), base(x)
            pts = [ax.c2p(u, v) for u, v in zip(x[::5], fx[::5])] + [ax.c2p(u, v) for u, v in zip(x[::-5], gx[::-5])]
            return Polygon(*pts, stroke_width=0, fill_color=C.MEASURE, fill_opacity=0.45)

        area = always_redraw(gap_area)

        def bound_box():
            n = nT.get_value()
            M = float(np.abs(seq(n, x) - base(x)).max())
            p0, p1 = ax.c2p(a, 0), ax.c2p(b, M)
            return Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 1e-3), stroke_color=C.EPS, stroke_width=2,
                             fill_color=C.EPS, fill_opacity=0.15).move_to((p0 + p1) / 2)

        box = always_redraw(bound_box)
        box_l = label(r"area at most a box's: \ $(b - a) \times \sup|f_n - f|$", font_size=22, color=C.EPS).next_to(ax, DOWN,
                                                                                                    buff=0.15)
        thm = VGroup(label(r"\textbf{Rudin 7.16} \ $f_n \in \mathcal R(\alpha)$, \ $f_n \to f$ uniformly on $[a, b]$ $\Rightarrow$", font_size=28),
                     MathTex(r"\int_a^b f\,d\alpha = \lim_{n \to \infty} \int_a^b f_n\,d\alpha", font_size=34, color=C.EPS),
                     MathTex(r"\Big|\int f_n - \int f\Big| \le \int |f_n - f| \le (b - a) \sup|f_n - f| \to 0",
                             font_size=28)).arrange(DOWN, buff=0.2)
        for r_ in thm:
            if r_.width > 6.0:
                r_.width = 6.0
        thm.arrange(DOWN, buff=0.2).move_to([3.75, 1.75, 0])
        I_f = trap(base(x), x)

        def readout():
            n = nT.get_value()
            In = trap(seq(n, x), x)
            return VGroup(MathTex(rf"\int_0^3 f_n = {In:.4f},", font_size=26, color=C.FUNC),
                          MathTex(rf"\int_0^3 f = {I_f:.4f},", font_size=26),
                          MathTex(rf"\text{{gap}} = {abs(In - I_f):.4f}", font_size=26, color=C.MEASURE)
                          ).arrange(RIGHT, buff=0.25).move_to([3.45, -0.2, 0])

        ro = always_redraw(readout)
        cor = VGroup(label(r"so a uniformly convergent series", font_size=26),
                     label(r"may be integrated term by term", font_size=26)).arrange(DOWN, buff=0.08).move_to([3.75, -1.35, 0])
        saw_note = VGroup(label(r"the sawtooth series is \emph{not} uniformly convergent", font_size=24, color=C.PATHOLOGY),
                          label(r"(it jumps): \ chapter 15 settles it another way", font_size=24, color=GREY_A)
                          ).arrange(DOWN, buff=0.06).move_to([3.75, -2.55, 0])
        n_l = always_redraw(lambda: MathTex(rf"n = {round(nT.get_value())}", font_size=28, color=C.FUNC).next_to(ax, UP,
                                                                                                         buff=0.1))
        with self.voiceover(
            "<bookmark mark='a'/> Integrals first. If f n converges to f uniformly on a closed interval, then the "
            "integral of the limit is the limit of the integrals. <bookmark mark='b'/> The picture is the whole proof: "
            "the difference of the integrals is at most the area between the graphs, and that area fits inside a box "
            "as wide as the interval and as tall as the largest gap. Uniform convergence squashes the box. "
            "<bookmark mark='c'/> So a uniformly convergent series may be integrated term by term. "
            "<bookmark mark='d'/> Fourier's sawtooth series doesn't qualify, because its partial sums can't converge "
            "uniformly to a function with a jump. We'll settle it another way in chapter fifteen."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), Create(lim), Create(gn), FadeIn(thm[:2]), FadeIn(n_l))
            vo.wait_until("b")
            self.play(FadeIn(area), FadeIn(box), FadeIn(box_l), FadeIn(thm[2]), FadeIn(ro))
            self.play(nT.animate.set_value(12), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(cor), nT.animate.set_value(40), run_time=3.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(saw_note))
        for m in (gn, area, box, n_l, ro):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derivatives(self):
        thm = VGroup(label(r"\textbf{Rudin 7.17} \ $f_n(x_0)$ converges and $f_n'$ converges \emph{uniformly} "
                           r"$\Rightarrow$", font_size=28),
                     MathTex(r"f_n \to f \text{ uniformly, and } f' = \lim f_n'", font_size=32, color=C.EPS)
                     ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        ax = plain_axes([-1, 1, 0.5], [-0.55, 0.55, 0.5], 5.4, 2.3).move_to([-3.65, 0.8, 0])
        bx = plain_axes([-1, 1, 0.5], [-0.3, 1.1, 0.5], 5.4, 2.3).move_to([-3.65, -2.5, 0])
        x = np.linspace(-1, 1, 1601)
        nT = ValueTracker(1.0)
        fseq = lambda n, t: t / (1 + n * t * t)  # noqa: E731
        dseq = lambda n, t: (1 - n * t * t) / (1 + n * t * t) ** 2  # noqa: E731
        gf = always_redraw(lambda: polyline(ax, x, fseq(nT.get_value(), x), color=C.FUNC, stroke_width=3.5))
        # f_n' ranges over [-1/8, 1] (min at n x^2 = 3), inside the axes: no clipping needed
        assert all(-0.13 < dseq(n, x).min() and dseq(n, x).max() <= 1 for n in (1, 10, 150))
        gd = always_redraw(lambda: polyline(bx, x, dseq(nT.get_value(), x), color=C.APPROX, stroke_width=3))
        fl = MathTex(r"f_n(x) = \frac{x}{1 + n x^2}", font_size=28, color=C.FUNC).next_to(ax, UP, buff=0.1)
        dl = MathTex(r"f_n'(x) = \frac{1 - n x^2}{(1 + n x^2)^2}", font_size=28, color=C.APPROX).next_to(bx, UP, buff=0.1)
        facts = VGroup(
            MathTex(r"\sup |f_n| = \frac{1}{2\sqrt n} \to 0", font_size=30),
            VGroup(MathTex(r"f_n'(0) = 1 \text{ for every } n,", font_size=30),
                   MathTex(r"f_n'(x) \to 0 \ \text{ for } x \ne 0", font_size=30)).arrange(DOWN, aligned_edge=LEFT,
                                                                                           buff=0.1),
            VGroup(label(r"so $\lim f_n'(0) = 1 \ne 0 = f'(0)$:", font_size=26, color=C.PATHOLOGY),
                   label(r"the derivatives converge, \ but not uniformly", font_size=26, color=C.PATHOLOGY)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"and $\sin(nx)/\sqrt n$ from the opening:", font_size=24, color=GREY_A),
                   label(r"$f_n \to 0$ uniformly, \ $f_n'$ does not converge", font_size=24, color=GREY_A)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        facts.move_to([0.4 + facts.width / 2, -0.75, 0])
        assert facts.get_right()[0] < 6.6
        n_l = always_redraw(lambda: MathTex(rf"n = {round(nT.get_value())}", font_size=28, color=C.FUNC).next_to(
            fl, RIGHT, buff=0.5))
        t = np.linspace(-1, 1, 200001)
        for n in (1, 4, 25, 100):
            assert abs(np.abs(fseq(n, t)).max() - 1 / (2 * np.sqrt(n))) < 1e-6 and dseq(n, np.array([0.0]))[0] == 1
        with self.voiceover(
            "<bookmark mark='a'/> Derivatives are more delicate: uniform convergence of the functions is not enough. "
            "Rudin's theorem asks instead for the derivatives to converge uniformly, and then the limit is "
            "differentiable with the expected derivative. <bookmark mark='b'/> Here's why the hypothesis is on the "
            "derivatives. The functions x over one plus n x squared shrink to zero uniformly: their largest value is "
            "one over two root n. <bookmark mark='c'/> But their derivatives at zero are all equal to one, while "
            "everywhere else the derivatives go to zero. The derivatives converge, but to a function that jumps at "
            "zero, and the limit of the derivatives at zero is one, while the derivative of the limit is zero. "
            "<bookmark mark='d'/> Small functions can have large slopes. Control has to come from the derivatives."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm), Create(ax), Create(bx))
            self.play(Create(gf), FadeIn(fl), FadeIn(n_l))
            vo.wait_until("b")
            self.play(FadeIn(facts[0]))
            vo.wait_until("c")
            self.play(Create(gd), FadeIn(dl), FadeIn(facts[1]))
            self.play(nT.animate.set_value(150), run_time=4.0, rate_func=rate_functions.ease_in_quad)
            self.play(FadeIn(facts[2]))
            vo.wait_until("d")
            self.play(FadeIn(facts[3]))
        for m in (gf, gd, n_l):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def summary(self):
        head = label(r"Which swap needs what \ (so far)", font_size=34).to_edge(UP, buff=0.3)
        rows = [
            (r"$\lim_n$ and continuity", r"uniform convergence", r"7.12"),
            (r"$\lim_n$ and $\int$", r"uniform convergence", r"7.16"),
            (r"$\lim_n$ and $\frac{d}{dx}$", r"uniform convergence of the derivatives", r"7.17"),
            (r"$\lim_n$ and $\int$, without uniformity", r"Lebesgue's dominated convergence", r"Part 5"),
        ]
        tab = VGroup()
        for i, (a, b_, c) in enumerate(rows):
            col = C.EPS if i < 3 else GREY_B
            tab.add(VGroup(label(a, font_size=26), label(b_, font_size=26, color=col),
                           label(c, font_size=24, color=GREY_B)))
        # columns: thumbnail | swap | what it needs | where; rows 1.3 apart, every column left-aligned
        TW, TH = 1.6, 0.95
        x_t = -6.55 + TW / 2
        x0 = -6.55 + TW + 0.35
        x1 = x0 + max(r_[0].width for r_ in tab) + 0.45
        x2 = x1 + max(r_[1].width for r_ in tab) + 0.45
        assert x2 + max(r_[2].width for r_ in tab) < 6.6
        ys = [1.75 - 1.35 * i for i in range(4)]
        for r_, y_ in zip(tab, ys):
            r_[0].move_to([x0 + r_[0].width / 2, y_, 0])
            r_[1].move_to([x1 + r_[1].width / 2, y_, 0])
            r_[2].move_to([x2 + r_[2].width / 2, y_, 0])
        thumbs = VGroup()
        u = np.linspace(0, 3, 300)
        # 1. continuity: f_n inside the uniform band around f
        f1, g1 = 0.5 + 0.3 * np.sin(2.5 * u), 0.5 + 0.3 * np.sin(2.5 * u) + 0.11 * np.sin(9 * u)
        a1 = plain_axes([0, 3, 1], [0, 1, 0.5], TW, TH, axis_config={"include_ticks": False})
        band1 = Polygon(*[a1.c2p(p_, q_) for p_, q_ in zip(u[::6], f1[::6] + 0.14)],
                        *[a1.c2p(p_, q_) for p_, q_ in zip(u[::-6], f1[::-6] - 0.14)], stroke_width=0, fill_color=C.EPS,
                        fill_opacity=0.25)
        assert np.abs(g1 - f1).max() < 0.14
        thumbs.add(VGroup(a1, band1, polyline(a1, u, f1, color=WHITE, stroke_width=2),
                          polyline(a1, u, g1, color=C.FUNC, stroke_width=2)))
        # 2. integrals: the area between f_n and f fits in the box (b - a) x sup|f_n - f|
        f2, g2 = base(u) * 0.45, base(u) * 0.45 + np.sin(5 * 3 * u + 1) / (1.5 * 3) * 0.45
        a2 = plain_axes([0, 3, 1], [0, 1.0, 0.5], TW, TH, axis_config={"include_ticks": False})
        M2 = float(np.abs(g2 - f2).max())
        assert trap(np.abs(g2 - f2), u) <= 3 * M2
        gap2 = Polygon(*[a2.c2p(p_, q_) for p_, q_ in zip(u[::3], g2[::3])], *[a2.c2p(p_, q_) for p_, q_ in
                                                                              zip(u[::-3], f2[::-3])],
                       stroke_width=0, fill_color=C.MEASURE, fill_opacity=0.5)
        p0_, p1_ = a2.c2p(0, 0), a2.c2p(3, M2)
        box2 = Rectangle(width=p1_[0] - p0_[0], height=p1_[1] - p0_[1], stroke_color=C.EPS, stroke_width=1.5,
                         fill_color=C.EPS, fill_opacity=0.15).move_to((p0_ + p1_) / 2)
        thumbs.add(VGroup(a2, gap2, box2, polyline(a2, u, f2, color=WHITE, stroke_width=2),
                          polyline(a2, u, g2, color=C.FUNC, stroke_width=2)))
        # 3. derivatives: x / (1 + 25 x^2) is small, but its slope at 0 is 1
        v = np.linspace(-1, 1, 400)
        a3 = plain_axes([-1, 1, 1], [-0.55, 0.55, 0.5], TW, TH, axis_config={"include_ticks": False})
        f3 = v / (1 + 25 * v * v)
        assert abs(np.abs(f3).max() - 0.1) < 1e-3 and abs(np.gradient(f3, v)[200] - 1) < 0.02
        thumbs.add(VGroup(a3, polyline(a3, v, f3, color=C.FUNC, stroke_width=2),
                          Line(a3.c2p(-0.5, -0.5), a3.c2p(0.5, 0.5), color=C.EPS, stroke_width=2)))
        # 4. without uniformity: x^n under the lid 1; the integrals 1/(n + 1) still go to 0 (Part 5)
        a4 = plain_axes([0, 1, 1], [0, 1.15, 1], TW, TH, axis_config={"include_ticks": False})
        w = np.linspace(0, 1, 300)
        fam4 = VGroup(*[polyline(a4, w, w**n, color=interpolate_color(ManimColor(GREY_D), ManimColor(GREY_A), k / 4),
                                 stroke_width=1.6) for k, n in enumerate((1, 2, 4, 8, 16))])
        assert all(abs(trap(w**n, w) - 1 / (n + 1)) < 1e-3 for n in (1, 2, 4, 8, 16))
        thumbs.add(VGroup(a4, DashedLine(a4.c2p(0, 1), a4.c2p(1, 1), color=GREY_B, stroke_width=1.5), fam4))
        for th_, y_ in zip(thumbs, ys):
            th_.move_to([x_t, y_, 0])
        with self.voiceover(
            "So far, then: <bookmark mark='a'/> uniform convergence lets limits pass through continuity and through "
            "integrals, and for derivatives we need the derivatives to converge uniformly. <bookmark mark='b'/> "
            "Uniformity is a strong demand, and in Part 5 a better integral will let limits pass through integrals "
            "under a much weaker condition."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(t_), FadeIn(r_, shift=RIGHT * 0.2)) for t_, r_ in
                                    zip(thumbs[:3], tab[:3])], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(thumbs[3]), FadeIn(tab[3], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()
