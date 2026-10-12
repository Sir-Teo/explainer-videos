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
        box_l = label(r"same area as a box $(b - a) \times \sup|f_n - f|$", font_size=22, color=C.EPS).next_to(ax, DOWN,
                                                                                                    buff=0.15)
        thm = VGroup(label(r"\textbf{Rudin 7.16} \ $f_n \to f$ uniformly on $[a, b]$ $\Rightarrow$", font_size=28),
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
        ax = plain_axes([-1, 1, 0.5], [-0.55, 0.55, 0.5], 5.2, 2.7).move_to([-4.0, 0.6, 0])
        bx = plain_axes([-1, 1, 0.5], [-0.3, 1.1, 0.5], 5.2, 2.7).move_to([-4.0, -2.35, 0])
        x = np.linspace(-1, 1, 1601)
        nT = ValueTracker(1.0)
        fseq = lambda n, t: t / (1 + n * t * t)  # noqa: E731
        dseq = lambda n, t: (1 - n * t * t) / (1 + n * t * t) ** 2  # noqa: E731
        gf = always_redraw(lambda: polyline(ax, x, fseq(nT.get_value(), x), color=C.FUNC, stroke_width=3.5))
        gd = always_redraw(lambda: polyline(bx, x, np.clip(dseq(nT.get_value(), x), -0.3, 1.1), color=C.APPROX,
                                            stroke_width=3))
        fl = MathTex(r"f_n(x) = \frac{x}{1 + n x^2}", font_size=28, color=C.FUNC).next_to(ax, RIGHT, buff=0.15)
        dl = MathTex(r"f_n'(x) = \frac{1 - n x^2}{(1 + n x^2)^2}", font_size=28, color=C.APPROX).next_to(bx, RIGHT,
                                                                                                buff=0.15)
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
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.3, -0.75, 0])
        n_l = always_redraw(lambda: MathTex(rf"n = {round(nT.get_value())}", font_size=28).next_to(ax, UP, buff=0.05))
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
            vo.wait_until("b")
            self.play(Create(gf), FadeIn(fl), FadeIn(n_l), FadeIn(facts[0]))
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
        head = label(r"Which swap needs what \ (so far)", font_size=36).to_edge(UP, buff=0.5)
        rows = [
            (r"$\lim_n$ and continuity", r"uniform convergence", r"7.12"),
            (r"$\lim_n$ and $\int$", r"uniform convergence", r"7.16"),
            (r"$\lim_n$ and $\frac{d}{dx}$", r"uniform convergence of the derivatives", r"7.17"),
            (r"$\lim_n$ and $\int$, without uniformity", r"Lebesgue's dominated convergence", r"Part 5"),
        ]
        tab = VGroup()
        for i, (a, b_, c) in enumerate(rows):
            col = C.EPS if i < 3 else GREY_B
            tab.add(VGroup(label(a, font_size=28), label(b_, font_size=28, color=col),
                           label(c, font_size=24, color=GREY_B)))
        for r_ in tab:
            r_[0].move_to([-3.6, 0, 0])
            r_[1].move_to([1.6, 0, 0])
            r_[2].move_to([5.6, 0, 0])
        tab.arrange(DOWN, buff=0.45).move_to([0, -0.3, 0])
        with self.voiceover(
            "So far, then: <bookmark mark='a'/> uniform convergence lets limits pass through continuity and through "
            "integrals, and for derivatives we need the derivatives to converge uniformly. <bookmark mark='b'/> "
            "Uniformity is a strong demand, and in Part 5 a better integral will let limits pass through integrals "
            "under a much weaker condition."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab[:3]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(tab[3], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()
