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
        # all six panels on one scale (x and t in [-8, 8], same size), so "the same Gaussian" looks the same
        x = np.linspace(-8, 8, 3201)
        mt_ = np.abs(t) <= 8 + 1e-9
        rows = []
        specs = [
            (np.where(np.abs(x) <= 1, 1.0, 0.0), bh, r"\mathbf 1_{[-1, 1]}", r"\sqrt{\tfrac{2}{\pi}}\,\frac{\sin t}{t}", eb),
            (np.exp(-x * x / 2), gh, r"e^{-x^2/2}", r"e^{-t^2/2}", eg),
            (np.clip(1 - np.abs(x), 0, None), th, r"(1 - |x|)_+", r"\frac{2 - 2\cos t}{\sqrt{2\pi}\, t^2}", et),
        ]

        def panel():
            return plain_axes([-8, 8, 2], [-0.3, 1.2, 1], 3.5, 1.35,
                              x_axis_config={"numbers_to_include": [-6, 6], "font_size": 16})

        for k, (fx, fh, nx, nt, err) in enumerate(specs):
            y = 1.6 - 2.05 * k
            ax = panel().move_to([-3.55, y - 0.2, 0])
            bx = panel().move_to([0.95, y - 0.2, 0])
            g1 = polyline(ax, x, fx, color=C.FUNC, stroke_width=3)
            g2 = polyline(bx, t[mt_], fh[mt_], color=C.FREQ, stroke_width=3)
            l1 = MathTex(nx, font_size=26, color=C.FUNC)
            l1.move_to([-5.45 - l1.width / 2, y - 0.2, 0])  # the left labels share a right edge
            l2 = MathTex(nt, font_size=26, color=C.FREQ).next_to(bx, RIGHT, buff=0.15)
            ar = Arrow([-1.65, y - 0.2, 0], [-0.95, y - 0.2, 0], buff=0, color=GREY_B, stroke_width=3, tip_length=0.15)
            e_ = MathTex(rf"\text{{quadrature vs formula: }} {sci(err, 0)}", font_size=22, color=GREY_A).next_to(
                l2, DOWN, buff=0.12, aligned_edge=LEFT)
            row = VGroup(ax, g1, l1, ar, bx, g2, l2, e_)
            assert row.get_left()[0] >= -6.65 and row.get_right()[0] <= 6.65
            rows.append(row)
        conv = MathTex(r"\hat f(t) = \frac{1}{\sqrt{2\pi}}\int_{-\infty}^{\infty} f(x)\,e^{-ixt}\,dx", font_size=32)
        tag = label(r"Rudin's convention, \ used from here on", font_size=22, color=GREY_A)
        VGroup(conv, tag).arrange(RIGHT, buff=0.45).to_edge(UP, buff=0.3)
        assert eb < 1e-6 and eg < 1e-8 and et < 1e-6
        # what the transform measures: f = e^{-x^2/8}(cos 2x + 0.6 cos 5x) is made of frequencies 2 and 5, and its
        # transform is bumps at +-2 and +-5 (e^{-x^2/8} -> 2 e^{-2t^2}; cos(wx) g -> (g^(t - w) + g^(t + w))/2)
        xi = np.linspace(-6, 6, 2401)
        fi = np.exp(-xi * xi / 8) * (np.cos(2 * xi) + 0.6 * np.cos(5 * xi))
        ti = np.linspace(-7, 7, 1401)
        fhi = (np.exp(-2 * (ti - 2) ** 2) + np.exp(-2 * (ti + 2) ** 2)
               + 0.6 * (np.exp(-2 * (ti - 5) ** 2) + np.exp(-2 * (ti + 5) ** 2)))
        xq = np.linspace(-40, 40, 160001)
        fq = np.exp(-xq * xq / 8) * (np.cos(2 * xq) + 0.6 * np.cos(5 * xq))
        for t_ in (0.0, 2.0, 3.3, 5.0):
            v_ = np.trapezoid(fq * np.exp(-1j * xq * t_), xq) / SQ2PI
            assert abs(v_ - float(np.interp(t_, ti, fhi))) < 1e-6
        iax = plain_axes([-6, 6, 2], [-1.7, 1.7, 1], 5.4, 2.4).move_to([-3.6, -0.6, 0])
        ibx = plain_axes([-7, 7, 1], [-0.2, 1.2, 1], 5.4, 2.4).move_to([3.4, -0.6, 0])
        ig = polyline(iax, xi, fi, color=C.FUNC, stroke_width=3)
        ih = polyline(ibx, ti, fhi, color=C.FREQ, stroke_width=3.5)
        iar = Arrow([-0.6, -0.6, 0], [0.4, -0.6, 0], buff=0, color=GREY_B, stroke_width=3, tip_length=0.15)
        il = VGroup(MathTex(r"f(x) = e^{-x^2/8}\,(\cos 2x + 0.6\cos 5x)", font_size=26, color=C.FUNC).next_to(iax, UP, buff=0.15),
                    MathTex(r"\hat f(t): \ \text{bumps at } \pm 2 \text{ and } \pm 5", font_size=26, color=C.FREQ).next_to(
                        ibx, UP, buff=0.15))
        intro = VGroup(iax, ig, iar, ibx, ih, il)
        with self.voiceover(
            "<bookmark mark='a'/> The Fourier transform measures how much of each frequency a function contains. "
            "We fix Rudin's convention, with one over root two pi in front, for the rest of the series. "
            "<bookmark mark='b'/> A box becomes a sinc: sharp edges need many frequencies, so the transform decays "
            "slowly, like one over t. <bookmark mark='c'/> A Gaussian becomes the same Gaussian. "
            "<bookmark mark='d'/> A triangle, which is a box convolved with itself, becomes the sinc squared, decaying "
            "like one over t squared. Each formula is checked against direct quadrature."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(conv), FadeIn(tag), Create(iax), Create(ig), FadeIn(il[0]))
            self.play(GrowArrow(iar), Create(ibx), Create(ih), FadeIn(il[1]), run_time=1.5)
            for k, mk in enumerate(("b", "c", "d")):
                vo.wait_until(mk)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.6)
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
            (r"$f \in L^1$", r"$\hat f$ continuous, $\to 0$ \ (Riemann--Lebesgue)"),  # fits unshrunk
        ], font_size=26)
        card.scale(0.78).move_to(UP * 1.05)
        head = label(r"The dictionary of the transform", font_size=34).to_edge(UP, buff=0.3)
        thm = label(r"\textbf{RCA 9.2--9.6}", font_size=22, color=GREY_A)
        thm.move_to([-6.65 + thm.width / 2, card.titles.get_y(), 0])
        assert thm.get_right()[0] < card.get_left()[0] - 0.2
        # the first rules, live, on f = e^{-x^2/2} (whose transform is e^{-t^2/2}): translating by a multiplies the
        # transform by e^{-iat}, so Re f^ = cos(at) e^{-t^2/2} oscillates inside the fixed envelope |f^|
        xs = np.linspace(-14, 14, 5601)

        def ft(fx, t_):  # Rudin's normalization: integral of f(x) e^{-ixt} dx / sqrt(2 pi)
            return np.trapezoid(fx * np.exp(-1j * xs * t_), xs) / SQ2PI

        for a_ in (0.0, 1.3, 2.5):
            for t_ in (-1.0, 0.4, 1.7):
                assert abs(ft(np.exp(-(xs - a_) ** 2 / 2), t_) - np.exp(-1j * a_ * t_ - t_ * t_ / 2)) < 1e-8
        for t_ in (-1.2, 0.5, 2.0):
            assert abs(ft(-xs * np.exp(-xs ** 2 / 2), t_) - 1j * t_ * np.exp(-t_ * t_ / 2)) < 1e-8
        lx = plain_axes([-4, 4, 1], [-1.1, 1.1, 1], 5.6, 2.0).move_to([-3.4, -2.55, 0])
        rx = plain_axes([-4, 4, 1], [-1.1, 1.1, 1], 5.6, 2.0).move_to([3.4, -2.55, 0])
        av = ValueTracker(0.0)
        xg = np.linspace(-4, 4, 801)
        fcur = always_redraw(lambda: polyline(lx, xg, np.exp(-(xg - av.get_value()) ** 2 / 2), color=C.FUNC, stroke_width=3))
        env = VGroup(polyline(rx, xg, np.exp(-xg ** 2 / 2), color=GREY_B, stroke_width=2).set_stroke(opacity=0.6),
                     polyline(rx, xg, -np.exp(-xg ** 2 / 2), color=GREY_B, stroke_width=2).set_stroke(opacity=0.6))
        fre = always_redraw(lambda: polyline(rx, xg, np.cos(av.get_value() * xg) * np.exp(-xg ** 2 / 2),
                                             color=C.FREQ, stroke_width=3))
        ll = always_redraw(lambda: MathTex(rf"f(x - a), \ a = {av.get_value():.2f}", font_size=24, color=C.FUNC
                                           ).next_to(lx, UP, buff=0.05))
        rl = MathTex(r"\mathrm{Re}\,\hat f = \cos(at)\,e^{-t^2/2}, \quad |\hat f| = e^{-t^2/2} \text{ (grey)}",
                     font_size=24, color=C.FREQ).next_to(rx, UP, buff=0.05)
        fd = polyline(lx, xg, -xg * np.exp(-xg ** 2 / 2), color=C.FUNC, stroke_width=3)
        fdh = polyline(rx, xg, xg * np.exp(-xg ** 2 / 2), color=C.FREQ, stroke_width=3)
        ld = MathTex(r"f'(x) = -x\,e^{-x^2/2}", font_size=24, color=C.FUNC).next_to(lx, UP, buff=0.05)
        rd_ = MathTex(r"\widehat{f'}(t) = i t\,e^{-t^2/2} \ \text{(imaginary part shown)}", font_size=24,
                      color=C.FREQ).next_to(rx, UP, buff=0.05)
        assert card.get_bottom()[1] > rl.get_top()[1] + 0.05 and rl.get_right()[0] < 6.95
        # 'c': convolution -> multiplication, on g = 1_[-1/2, 1/2]: g * g = (1 - |x|)_+ (the triangle of the pairs) and
        # (g * g)^ = sqrt(2 pi) g^^2, with g^(t) = sqrt(2/pi) sin(t/2) / t
        with np.errstate(invalid="ignore", divide="ignore"):
            g_hat = np.where(xg == 0, 1 / SQ2PI, math.sqrt(2 / math.pi) * np.sin(xg / 2) / np.where(xg == 0, 1, xg))
            tri_hat = np.where(xg == 0, 1 / SQ2PI, (2 - 2 * np.cos(xg)) / (SQ2PI * np.where(xg == 0, 1, xg) ** 2))
        assert np.allclose(SQ2PI * g_hat**2, tri_hat, atol=1e-12)
        box_h = np.where(np.isclose(np.abs(xs), 0.5), 0.5, (np.abs(xs) < 0.5).astype(float))  # midpoint at the jumps
        for t_ in (0.3, 1.0, 2.7):
            assert abs(ft(box_h, t_) - math.sqrt(2 / math.pi) * math.sin(t_ / 2) / t_) < 1e-6
        xc = np.linspace(-3, 3, 6001)
        gc = np.where(np.abs(xc) < 0.5, 1.0, 0.0)
        assert np.abs(np.convolve(gc, gc, mode="same") * (xc[1] - xc[0]) - np.clip(1 - np.abs(xc), 0, None)).max() < 2e-3
        lc0 = polyline(lx, xg, np.where(np.abs(xg) <= 0.5, 1.0, 0.0), color=GREY_B, stroke_width=2).set_stroke(opacity=0.6)
        lc = polyline(lx, xg, np.clip(1 - np.abs(xg), 0, None), color=C.FUNC, stroke_width=3)
        rc0 = polyline(rx, xg, g_hat, color=GREY_B, stroke_width=2).set_stroke(opacity=0.6)
        rc = polyline(rx, xg, tri_hat, color=C.FREQ, stroke_width=3)
        lcl = MathTex(r"g = \mathbf 1_{[-\frac12, \frac12]} \text{ (grey)}, \ \ g * g = (1 - |x|)_+", font_size=24,
                      color=C.FUNC).next_to(lx, UP, buff=0.05)
        rcl = MathTex(r"\widehat{g * g} = \sqrt{2\pi}\,\hat g^{\,2}, \ \ \hat g \text{ (grey)}", font_size=24,
                      color=C.FREQ).next_to(rx, UP, buff=0.05)
        # 'd': Riemann-Lebesgue on the box 1_[-1, 1]: f^ = sqrt(2/pi) sin t / t, inside the envelopes +-sqrt(2/pi)/|t|
        rx2 = plain_axes([-16, 16, 4], [-1.1, 1.1, 1], 5.6, 2.0).move_to(rx.get_center())
        tw = np.linspace(-16, 16, 3201)
        with np.errstate(invalid="ignore", divide="ignore"):
            sinc_ = np.where(tw == 0, math.sqrt(2 / math.pi), math.sqrt(2 / math.pi) * np.sin(tw) / np.where(tw == 0, 1, tw))
            envv = math.sqrt(2 / math.pi) / np.abs(np.where(tw == 0, 1e-9, tw))
        box1 = np.where(np.isclose(np.abs(xs), 1), 0.5, (np.abs(xs) < 1).astype(float))
        for t_ in (0.5, 4.0, 11.0):
            assert abs(ft(box1, t_) - math.sqrt(2 / math.pi) * math.sin(t_) / t_) < 1e-6
        assert np.all(np.abs(sinc_) <= envv + 1e-12)
        ld_box = polyline(lx, xg, np.where(np.abs(xg) <= 1, 1.0, 0.0), color=C.FUNC, stroke_width=3)
        env_g = VGroup(runs(rx2, tw, envv, GREY_B, 2), runs(rx2, tw, -envv, GREY_B, 2)).set_stroke(opacity=0.7)
        rsinc = polyline(rx2, tw, sinc_, color=C.FREQ, stroke_width=3)
        ldl = MathTex(r"f = \mathbf 1_{[-1, 1]} \in L^1", font_size=24, color=C.FUNC).next_to(lx, UP, buff=0.05)
        rdl = MathTex(r"\hat f = \sqrt{2/\pi}\,\tfrac{\sin t}{t} \to 0, \ \ \text{inside } \pm\sqrt{2/\pi}\,/|t|",
                      font_size=24, color=C.FREQ).next_to(rx2, UP, buff=0.05)
        assert max(lcl.get_right()[0], ldl.get_right()[0]) < rcl.get_left()[0] - 0.2 and rdl.get_right()[0] < 6.65
        with self.voiceover(
            "<bookmark mark='a'/> The transform turns one kind of operation into another. Shifting a function "
            "multiplies its transform by a phase, and multiplying by a phase shifts the transform. "
            "<bookmark mark='b'/> Differentiation becomes multiplication by i t, which is why the transform turns "
            "differential equations into algebra. <bookmark mark='c'/> Convolution becomes multiplication. "
            "<bookmark mark='d'/> And for an integrable function, the transform is continuous and dies at infinity: "
            "the Riemann-Lebesgue lemma again."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(card.titles), FadeIn(thm))
            self.play(FadeIn(card.rows[0]), FadeIn(card.arrows[0]), Create(lx), Create(rx), FadeIn(fcur), FadeIn(fre),
                      FadeIn(env), FadeIn(ll), FadeIn(rl))
            self.play(av.animate.set_value(2.5), run_time=3.0, rate_func=smooth)
            self.play(FadeIn(card.rows[1]), FadeIn(card.arrows[1]), run_time=0.6)
            self.play(av.animate.set_value(0.0), run_time=1.5)
            for m_ in (fcur, fre, ll):
                m_.clear_updaters()
            vo.wait_until("b")
            self.play(FadeIn(card.rows[2]), FadeIn(card.arrows[2]), ReplacementTransform(fcur, fd),
                      ReplacementTransform(fre, fdh), FadeOut(env), FadeTransform(ll, ld), FadeTransform(rl, rd_))
            vo.wait_until("c")
            self.play(FadeIn(card.rows[3]), FadeIn(card.arrows[3]), ReplacementTransform(fd, lc), FadeIn(lc0),
                      ReplacementTransform(fdh, rc), FadeIn(rc0), FadeTransform(ld, lcl), FadeTransform(rd_, rcl))
            vo.wait_until("d")
            self.play(FadeIn(card.rows[4]), FadeIn(card.arrows[4]), FadeOut(lc0), ReplacementTransform(lc, ld_box),
                      FadeOut(VGroup(rc, rc0)), FadeTransform(rx, rx2), FadeTransform(lcl, ldl), FadeTransform(rcl, rdl))
            self.play(Create(env_g), Create(rsinc), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uncertainty(self):
        # one scale for both panels: at sigma = 1 the two pictures are identical (e^{-x^2/2} is its own transform)
        ax = plain_axes([-4, 4, 1], [0, 2.6, 1], 5.6, 2.8).move_to([-3.5, 0.2, 0])
        bx = plain_axes([-4, 4, 1], [0, 2.6, 1], 5.6, 2.8).move_to([3.0, 0.2, 0])
        ones = VGroup(*[VGroup(DashedLine(a_.c2p(-4, 1), a_.c2p(4, 1), color=GREY_B, stroke_width=2),
                               MathTex(r"1", font_size=22, color=GREY_B).next_to(a_.c2p(4, 1), RIGHT, buff=0.1))
                        for a_ in (ax, bx)])
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
            label(r"\textbf{FA, ch.\ 7} \ $e^{-x^2/2}$ is its own transform: \ both solve $u' = -xu$, \ $u(0) = 1$",
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
            self.play(FadeIn(head), Create(ax), Create(bx), FadeIn(ones), FadeIn(pp), FadeIn(l1), FadeIn(l2),
                      FadeIn(rows[0]))
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
