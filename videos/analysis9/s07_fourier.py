from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis9.common import SQ2PI, load, plain_axes, polyline


class FourierL1(VoiceoverScene):
    def construct(self):
        self.card()
        self.pairs()
        self.rules()
        self.uncertainty()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"The Fourier transform", r"How is a function built from frequencies?", lit=(1807,), part=9)
        with self.voiceover("Chapter six: the Fourier transform on the line."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pairs(self):
        d = load("pairs")
        t, bh, gh, th = d["t"], d["box_hat"], d["g_hat"], d["tri_hat"]
        eb, eg, et = float(d["eb"]), float(d["eg"]), float(d["et"])
        x = np.linspace(-3, 3, 1201)
        rows = []
        specs = [
            (np.where(np.abs(x) <= 1, 1.0, 0.0), bh, r"\mathbf 1_{[-1, 1]}", r"\sqrt{\tfrac{2}{\pi}}\,\frac{\sin t}{t}", eb),
            (np.exp(-x * x / 2), gh, r"e^{-x^2/2}", r"e^{-t^2/2}", eg),
            (np.clip(1 - np.abs(x), 0, None), th, r"(1 - |x|)_+", r"\frac{2 - 2\cos t}{\sqrt{2\pi}\, t^2}", et),
        ]
        for k, (fx, fh, nx, nt, err) in enumerate(specs):
            y = 1.35 - 2.05 * k
            ax = plain_axes([-3, 3, 1], [-0.3, 1.2, 1], 3.6, 1.35).move_to([-4.2, y - 0.2, 0])
            bx = plain_axes([-12, 12, 4], [-0.3, 1.0, 1], 4.4, 1.35).move_to([1.0, y - 0.2, 0])
            g1 = polyline(ax, x, fx, color=C.FUNC, stroke_width=3)
            g2 = polyline(bx, t, fh, color=C.FREQ, stroke_width=3)
            l1 = MathTex(nx, font_size=26, color=C.FUNC).next_to(ax, LEFT, buff=0.1)
            l2 = MathTex(nt, font_size=24, color=C.FREQ).next_to(bx, RIGHT, buff=0.1)
            ar = Arrow([-2.15, y - 0.2, 0], [-1.35, y - 0.2, 0], buff=0, color=GREY_B, stroke_width=3, tip_length=0.15)
            e_ = MathTex(rf"\text{{quadrature vs formula: }} {sci(err, 0)}", font_size=18, color=GREY_A).next_to(bx, DOWN,
                                                                                                         buff=0.02)
            row = VGroup(ax, g1, l1, ar, bx, g2, l2, e_)
            if row.get_left()[0] < -6.95:  # a wide label on the left: move the whole row in
                row.shift((-6.95 - row.get_left()[0]) * RIGHT)
            rows.append(row)
        conv = MathTex(r"\hat f(t) = \frac{1}{\sqrt{2\pi}}\int_{-\infty}^{\infty} f(x)\,e^{-ixt}\,dx", font_size=32).to_edge(
            UP, buff=0.2)
        tag = label(r"Rudin's convention, \ used from here on", font_size=20, color=GREY_A).next_to(conv, RIGHT, buff=0.3)
        assert eb < 1e-6 and eg < 1e-8 and et < 1e-6
        with self.voiceover(
            "<bookmark mark='a'/> The Fourier transform measures how much of each frequency a function contains. "
            "We fix Rudin's convention, with one over root two pi in front, for the rest of the series. "
            "<bookmark mark='b'/> A box becomes a sinc: sharp edges need many frequencies, so the transform decays "
            "slowly, like one over t. <bookmark mark='c'/> A Gaussian becomes the same Gaussian. "
            "<bookmark mark='d'/> A triangle, which is a box convolved with itself, becomes the sinc squared, decaying "
            "like one over t squared. Each formula is checked against direct quadrature."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(conv), FadeIn(tag))
            for k, mk in enumerate(("b", "c", "d")):
                vo.wait_until(mk)
                r_ = rows[k]
                self.play(Create(r_[0]), Create(r_[1]), FadeIn(r_[2]), run_time=0.8)
                self.play(GrowArrow(r_[3]), Create(r_[4]), Create(r_[5]), FadeIn(r_[6]), FadeIn(r_[7]), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        card = dictionary_card(r"space: \ $f(x)$", r"frequency: \ $\hat f(t)$", [
            (r"translate: \ $f(x - a)$", r"modulate: \ $e^{-iat}\hat f(t)$"),
            (r"modulate: \ $e^{iax} f(x)$", r"translate: \ $\hat f(t - a)$"),
            (r"differentiate: \ $f'$", r"multiply: \ $it\,\hat f$"),
            (r"convolve: \ $f * g$", r"multiply: \ $\sqrt{2\pi}\,\hat f\,\hat g$"),
            (r"$f \in L^1$", r"$\hat f$ continuous, \ $\to 0$ at $\pm\infty$ \ (Riemann--Lebesgue)"),
        ], font_size=26)
        card.move_to(DOWN * 0.3)
        head = label(r"\textbf{RCA 9.2--9.6} \ the dictionary of the transform", font_size=32).to_edge(UP, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> The transform turns one kind of operation into another. Shifting a function "
            "multiplies its transform by a phase, and multiplying by a phase shifts the transform. "
            "<bookmark mark='b'/> Differentiation becomes multiplication by i t, which is why the transform turns "
            "differential equations into algebra. <bookmark mark='c'/> Convolution becomes multiplication. "
            "<bookmark mark='d'/> And for an integrable function, the transform is continuous and dies at infinity: "
            "the Riemann-Lebesgue lemma again."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(card.titles))
            for i in (0, 1):
                self.play(FadeIn(card.rows[i]), FadeIn(card.arrows[i]), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(card.rows[2]), FadeIn(card.arrows[2]))
            vo.wait_until("c")
            self.play(FadeIn(card.rows[3]), FadeIn(card.arrows[3]))
            vo.wait_until("d")
            self.play(FadeIn(card.rows[4]), FadeIn(card.arrows[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uncertainty(self):
        ax = plain_axes([-4, 4, 1], [0, 1.2, 0.5], 5.6, 2.8).move_to([-3.5, 0.2, 0])
        bx = plain_axes([-4, 4, 1], [0, 3.2, 1], 5.6, 2.8).move_to([3.0, 0.2, 0])
        sT = ValueTracker(1.0)
        x = np.linspace(-4, 4, 801)

        def pics():
            s = sT.get_value()
            f = np.exp(-x * x / (2 * s * s))
            fh = s * np.exp(-s * s * x * x / 2)
            return VGroup(polyline(ax, x, f, color=C.FUNC, stroke_width=3.5), polyline(bx, x, fh, color=C.FREQ,
                                                                                       stroke_width=3.5))

        pp = always_redraw(pics)
        rd = always_redraw(lambda: MathTex(rf"\sigma = {sT.get_value():.2f}: \ \text{{width}} \times \text{{width}} = "
                                           rf"\sigma \cdot \tfrac{{1}}{{\sigma}} = 1", font_size=28).next_to(VGroup(ax, bx), DOWN,
                                                                                                         buff=0.3))
        l1 = MathTex(r"e^{-x^2/2\sigma^2}", font_size=28, color=C.FUNC).next_to(ax, UP, buff=0.1)
        l2 = MathTex(r"\sigma\, e^{-\sigma^2 t^2/2}", font_size=28, color=C.FREQ).next_to(bx, UP, buff=0.1)
        rows = VGroup(
            label(r"\textbf{RCA 9.7} \ $e^{-x^2/2}$ is its own transform: \ both solve $u' = -xu$, \ $u(0) = 1$",
                  font_size=24),
            label(r"narrow in space $\iff$ wide in frequency: \ the uncertainty principle \ (the quantum video's $\Delta x\,\Delta p$)",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        # the self-duality, via the ODE: the transform of xf is i (f^)'
        xx = np.linspace(-30, 30, 120001)
        tt = np.linspace(-5, 5, 41)
        g = np.exp(-xx * xx / 2)
        gh = np.array([np.sum(g * np.exp(-1j * xx * t_)) * (xx[1] - xx[0]) for t_ in tt]) / SQ2PI
        assert np.allclose(gh, np.exp(-tt * tt / 2), atol=1e-12)
        head = label(r"Narrow in space, \ wide in frequency", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Why is the Gaussian its own transform? Both it and its transform solve the same "
            "differential equation, u prime equals minus x u, with the same starting value. <bookmark mark='b'/> Now "
            "squeeze it. A narrower Gaussian in space has a wider transform, and the product of the two widths stays "
            "fixed. <bookmark mark='c'/> That's the uncertainty principle, the same one the quantum video met as "
            "position against momentum."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(bx), FadeIn(pp), FadeIn(l1), FadeIn(l2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rd))
            self.play(sT.animate.set_value(0.35), run_time=2.5)
            self.play(sT.animate.set_value(2.5), run_time=2.5)
            self.play(sT.animate.set_value(1.0), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        for m in (pp, rd):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
