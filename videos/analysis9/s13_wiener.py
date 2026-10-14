from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis9.common import SQ2PI, load, plain_axes, polyline, trap


class Wiener(VoiceoverScene):
    def construct(self):
        self.card()
        self.translates()
        self.algebra()
        self.zeta()
        self.primes()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(12, r"Wiener and the primes", r"When do the translates of one function fill $L^1$?", lit=(),
                            part=9)
        with self.voiceover("Chapter twelve: Wiener's Tauberian theorem, and the prime number theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def translates(self):
        d = load("wiener")
        x, tg, ag, as_ = d["x"], d["target"], d["ag"], d["as_"]
        eg, es, bound, inside = float(d["eg"]), float(d["es"]), float(d["bound"]), float(d["inside"])
        ax = plain_axes([-4, 4, 1], [-1.1, 1.1, 1], 6.2, 2.0).move_to([-3.3, 1.35, 0])
        bx = plain_axes([-9, 9, 3], [0, 1.1, 0.5], 6.2, 2.0, numbers=True, font_size=16,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.3, -1.6, 0])
        g0 = polyline(ax, x, tg, color=C.FUNC, stroke_width=5)
        g1 = polyline(ax, x, ag, color=C.APPROX, stroke_width=2.5)
        g2 = polyline(ax, x, as_, color=C.FREQ, stroke_width=3)
        l0 = MathTex(r"g = e^{-x^2}\cos 5x", font_size=24, color=C.FUNC).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        t = np.linspace(-9, 9, 1201)
        th = (np.exp(-((t - 5) ** 2) / 4) + np.exp(-((t + 5) ** 2) / 4)) / (2 * math.sqrt(2))
        kg = np.exp(-0.02 * t * t)  # e^(-u^2 / 0.08) has transform proportional to e^(-0.02 t^2)
        tri = np.clip(1 - np.abs(t) / 2, 0, None)  # sinc^2 has transform proportional to the triangle on [-2, 2]
        h0 = polyline(bx, t, th / th.max(), color=C.FUNC, stroke_width=3.5)
        h1 = polyline(bx, t, kg, color=C.APPROX, stroke_width=3)
        h2 = polyline(bx, t, tri, color=C.FREQ, stroke_width=3)
        zero = VGroup(*[Rectangle(width=bx.c2p(9, 0)[0] - bx.c2p(2, 0)[0], height=bx.c2p(0, 1.1)[1] - bx.c2p(0, 0)[1],
                                  stroke_width=0, fill_color=C.PATHOLOGY, fill_opacity=0.15).move_to(
            bx.c2p(s * 5.5, 0.55)) for s in (-1, 1)])
        ll = VGroup(MathTex(r"|\hat g|", font_size=22, color=C.FUNC), MathTex(r"\hat k_{\text{Gauss}}", font_size=22,
                                                                              color=C.APPROX),
                    MathTex(r"\hat k_{\text{sinc}^2}", font_size=22, color=C.FREQ)).arrange(RIGHT, buff=0.3).next_to(
            bx, UP, buff=0.05)
        assert eg < 1e-12 and abs(es - bound) < 1e-5
        rows = VGroup(
            label(r"approximate $g$ by $\sum_k c_k\, k(x - s_k)$, \ 241 translates, \ least squares:", font_size=22),
            MathTex(rf"k = e^{{-x^2/0.08}}: \ \text{{error }} {sci(eg, 1)}", font_size=26, color=C.APPROX),
            MathTex(rf"k = \Big(\frac{{\sin x}}{{x}}\Big)^2: \ \text{{error }} {100 * es:.4f}\%", font_size=26, color=C.FREQ),
            MathTex(r"\widehat{\textstyle\sum_k c_k k(\cdot - s_k)} = \hat k(t)\textstyle\sum_k c_k e^{-is_k t} = 0 "
                    r"\ \text{ where } \hat k = 0", font_size=24),
            MathTex(rf"\text{{best possible: }} \sqrt{{1 - {100 * inside:.4f}\%}} = {100 * bound:.4f}\%", font_size=24,
                    color=GREY_A),
            label(r"\textbf{Wiener} (1932): \ the translates of $k \in L^1$ span a dense subspace", font_size=24, color=C.EPS),
            label(r"$\iff$ \ $\hat k$ never vanishes", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -0.3, 0])
        for r_ in rows:
            if r_.width > 6.0:
                r_.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -0.3, 0])
        assert rows.get_right()[0] <= 6.6
        head = label(r"Which kernels can build everything?", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Here's a question that sounds like linear algebra. Take one integrable kernel k. "
            "Can sums of its translates approximate every integrable function? Try a target with frequencies near "
            "five. <bookmark mark='b'/> With a narrow Gaussian kernel, two hundred forty-one translates reproduce it "
            "to rounding error. <bookmark mark='c'/> With sine x over x, squared, the best fit misses by 99.93 "
            "percent. <bookmark mark='d'/> The frequency side says why. Transforming a sum of translates multiplies "
            "the kernel's transform by a trigonometric sum, so it's zero wherever the kernel's transform is. The "
            "squared sinc has a triangle for its transform, zero beyond two, exactly where the target lives, and the "
            "computed error is the best possible. <bookmark mark='e'/> Wiener's theorem is the converse: if the "
            "kernel's transform never vanishes, the translates fill everything."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(g0), FadeIn(l0), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(g1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(g2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(bx), Create(h0), FadeIn(ll[0]))
            self.play(Create(h1), Create(h2), FadeIn(ll[1:]), FadeIn(zero), FadeIn(rows[3]))
            self.play(FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algebra(self):
        # L^1 under convolution: ||f * g||_1 <= ||f||_1 ||g||_1 and (f * g)^ = sqrt(2 pi) f^ g^
        x = np.linspace(-20, 20, 8001)
        h = x[1] - x[0]
        f = np.exp(-np.abs(x)) * np.sign(x - 0.3)
        g = np.where(np.abs(x - 1) <= 1, 1.0, 0.0) - 0.5 * np.exp(-((x + 2) ** 2))
        fg = np.convolve(f, g)[4000:12001] * h
        n1 = trap(np.abs(fg), x)
        n2 = trap(np.abs(f), x) * trap(np.abs(g), x)
        tt = np.array([0.0, 0.7, 1.9])

        def hat(v, t_):
            return trap(v * np.exp(-1j * x * t_), x) / SQ2PI

        errs = [abs(hat(fg, t_) - SQ2PI * hat(f, t_) * hat(g, t_)) for t_ in tt]
        assert n1 <= n2 and max(errs) < 1e-3
        ax = plain_axes([-6, 6, 2], [0, 1.1, 0.5], 6.2, 2.0).move_to([-3.3, 0.9, 0])
        # 'a': the f, g and f * g of the inequality, drawn
        win = np.abs(x) <= 5
        assert max(np.abs(f[win]).max(), np.abs(g[win]).max(), np.abs(fg[win]).max()) < 1.2
        fax = plain_axes([-5, 5, 1], [-1.2, 1.2, 1], 6.2, 2.4).move_to([-3.3, 0.9, 0])
        cpic = VGroup(polyline(fax, x[win], f[win], color=C.FUNC, stroke_width=3),
                      polyline(fax, x[win], g[win], color=C.APPROX, stroke_width=3),
                      polyline(fax, x[win], fg[win], color=C.EPS, stroke_width=4))
        cl_ = MathTex("f", r",\ ", "g", r",\ ", "f * g", font_size=26).next_to(fax, UP, buff=0.1)
        for i_, c_ in ((0, C.FUNC), (2, C.APPROX), (4, C.EPS)):
            cl_[i_].set_color(c_)
        t = np.linspace(-6, 6, 1201)
        tri = np.clip(1 - np.abs(t) / 2, 0, None)
        kg = np.exp(-0.02 * t * t)
        line = Line(ax.c2p(-6, 0), ax.c2p(6, 0), color=C.SPECTRUM, stroke_width=6)
        ga = polyline(ax, t, kg, color=C.APPROX, stroke_width=3)
        gb = polyline(ax, t, tri, color=C.FREQ, stroke_width=3)
        zs = VGroup(*[Line(ax.c2p(a_, 0), ax.c2p(b_, 0), color=C.PATHOLOGY, stroke_width=9) for a_, b_ in ((-6, -2), (2, 6))])
        lt = label(r"each $t \in \mathbb R$ \ is a homomorphism \ $f \mapsto \hat f(t)$", font_size=22,
                   color=C.SPECTRUM).next_to(ax, DOWN, buff=0.15)
        lz = label(r"$\operatorname{sinc}^2$ lies in the ideals at $|t| \ge 2$", font_size=22, color=C.PATHOLOGY).next_to(
            lt, DOWN, buff=0.1)
        rows = VGroup(
            label(r"$L^1(\mathbb R)$ with $*$ is a commutative Banach algebra:", font_size=24),
            MathTex(rf"\|f * g\|_1 \le \|f\|_1\|g\|_1: \ \ {n1:.4f} \le {n2:.4f}", font_size=26),
            MathTex(rf"(f * g)^\wedge = \sqrt{{2\pi}}\,\hat f\,\hat g: \ \ \text{{error }} {sci(max(errs), 0)}", font_size=26),
            label(r"\textbf{RCA 9.23} \ its complex homomorphisms are exactly $f \mapsto \hat f(t)$", font_size=24,
                  color=C.SPECTRUM),
            label(r"$\hat k(t) = 0$ \ $\iff$ \ $k$ lies in that homomorphism's kernel, \ a maximal ideal", font_size=22,
                  color=GREY_A),
            label(r"Wiener: \ no zeros $\Rightarrow$ in no maximal ideal $\Rightarrow$ the translates span", font_size=24,
                  color=C.EPS),
            label(r"Part 10: \ Gelfand's theory of exactly this", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -0.2, 0])
        for r_ in rows:
            if r_.width > 6.0:
                r_.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.5, -0.2, 0])
        assert rows.get_right()[0] <= 6.6
        head = label(r"The algebra behind Wiener's theorem", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Why is it true? Integrable functions under convolution form an algebra, with the L "
            "one norm of a convolution at most the product of the norms, and the transform turns convolution into "
            "multiplication. <bookmark mark='b'/> The homomorphisms from this algebra to the complex numbers are "
            "exactly the evaluations of the transform at a point t. So the real line is the space of maximal ideals, "
            "and a kernel lies in one exactly where its transform vanishes. <bookmark mark='c'/> The squared sinc "
            "lies in all the ideals beyond two. A kernel whose transform never vanishes lies in none of them, and "
            "that is what makes its translates span. <bookmark mark='d'/> This is the first glimpse of Gelfand's "
            "theory, which is Part 10."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:3]), Create(fax), FadeIn(cl_))
            self.play(LaggedStart(*[Create(c_) for c_ in cpic], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeOut(VGroup(fax, cpic, cl_)), run_time=0.6)
            self.play(Create(ax), Create(line), FadeIn(lt), FadeIn(rows[3:5]))
            vo.wait_until("c")
            self.play(Create(gb), Create(zs), FadeIn(lz))
            self.play(Create(ga), FadeIn(rows[5]))
            vo.wait_until("d")
            self.play(FadeIn(rows[6]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zeta(self):
        d = load("zeta")
        ts, sig, Q, lim, tg, one, half = d["ts"], d["sig"], d["Q"], d["lim"], d["tg"], d["one"], d["half"]
        # tall enough for the whole of both curves (|zeta(1/2 + it)| reaches 2.94 near t = 35): nothing clamped
        ax = plain_axes([0, 40, 10], [0, 3.0, 1], 6.4, 2.6, numbers=True, font_size=16,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.2, 1.0, 0])
        assert max(one.max(), half.max()) < 3.0
        g1 = polyline(ax, tg, one, color=C.SPECTRUM, stroke_width=3.5)
        g2 = polyline(ax, tg, half, color=GREY_B, stroke_width=2.5)
        l1 = MathTex(rf"|\zeta(1 + it)| \ge {one.min():.3f} \ (t \le 40)", font_size=24, color=C.SPECTRUM).next_to(ax, UP, buff=0.05).align_to(
            ax, LEFT)
        l2 = MathTex(r"|\zeta(\tfrac12 + it)|: \text{ zeros at } 14.13, 21.02, \ldots", font_size=22, color=GREY_B).next_to(
            l1, RIGHT, buff=0.4)
        tl = MathTex(r"t", font_size=22).next_to(ax.x_axis, RIGHT, buff=0.1)
        # the 3-4-1 trick
        bx = plain_axes([0, 2 * math.pi, math.pi / 2], [0, 8, 4], 3.2, 1.4).move_to([-4.6, -2.3, 0])
        th = np.linspace(0, 2 * math.pi, 400)
        trig = 3 + 4 * np.cos(th) + np.cos(2 * th)
        assert np.allclose(trig, 2 * (1 + np.cos(th)) ** 2) and trig.min() >= -1e-12
        g3 = polyline(bx, th, trig, color=C.EPS, stroke_width=3)
        l3 = MathTex(r"3 + 4\cos\theta + \cos 2\theta = 2(1 + \cos\theta)^2 \ge 0", font_size=22, color=C.EPS).next_to(
            bx, UP, buff=0.05).align_to(bx, LEFT)
        k = 1  # the row at t = 14.134725
        tab = VGroup(MathTex(r"\sigma", r"\quad |\zeta(\sigma)^3\zeta(\sigma + it)^4\zeta(\sigma + 2it)|", font_size=22,
                             color=GREY_A))
        for s, q in zip(sig, Q[k]):
            tab.add(MathTex(f"{s:g}", rf"\quad {q:,.3f}".replace(",", r"{,}"), font_size=22))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.6, 1.2, 0])
        regrid(tab)
        tt = MathTex(rf"t = {ts[k]:.6f}", font_size=22, color=GREY_A).next_to(tab, UP, buff=0.1)
        assert np.all(Q >= 1)
        rows = VGroup(
            label(r"$\log$ of it $= \sum_{p, m} \frac{3 + 4\cos(mt\log p) + \cos(2mt\log p)}{m\,p^{m\sigma}} \ge 0$",
                  font_size=22),
            label(r"a zero at $1 + it$ would make it $\sim (\sigma - 1)^{4 - 3} \to 0$", font_size=22, color=C.PATHOLOGY),
            MathTex(rf"\text{{instead }} (\sigma - 1)^3 \times \text{{it}} \to |\zeta(1 + it)|^4|\zeta(1 + 2it)| = {lim[k]:.4f}",
                    font_size=22, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.0, -2.2, 0])
        for r_ in rows:
            if r_.width > 7.6:
                r_.width = 7.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.0, -2.2, 0])
        head = label(r"$\zeta$ has no zeros on the line $\mathrm{Re}\,s = 1$", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The road to the primes needs one fact about the zeta function from the Riemann "
            "video: it has no zeros on the line where the real part is one. On that line, over this stretch, its size stays above a third, "
            "while on the critical line it touches zero again and again. <bookmark mark='b'/> The proof is a "
            "trigonometric inequality: three plus four cos theta plus cos two theta is twice a square, so it's never "
            "negative. <bookmark mark='c'/> Feed it into the Euler product, and the product of zeta at sigma cubed, "
            "zeta at sigma plus i t to the fourth, and zeta at sigma plus two i t, is always at least one. "
            "<bookmark mark='d'/> If zeta vanished at one plus i t, the fourth power would beat the cube of the pole, "
            "and the product would go to zero. It doesn't."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(tl), Create(g2), FadeIn(l2))
            self.play(Create(g1), FadeIn(l1))
            vo.wait_until("b")
            self.play(Create(bx), Create(g3), FadeIn(l3))
            vo.wait_until("c")
            self.play(FadeIn(tt), FadeIn(tab[0]), FadeIn(rows[0]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(rows[1:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def primes(self):
        d = load("primes")
        xs, pi_, r1, r2, r3 = d["xs"], d["pi"], d["r1"], d["r2"], d["r3"]
        lx = np.log10(xs)
        ax = plain_axes([2, 8, 1], [0.8, 1.2, 0.1], 6.4, 3.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.2, -0.3, 0])
        xl = MathTex(r"\log_{10} x", font_size=22).next_to(ax.x_axis, DOWN, buff=0.35)
        one = DashedLine(ax.c2p(2, 1), ax.c2p(8, 1), color=GREY_B, stroke_width=2)
        cols = [C.FUNC, C.EPS, C.SPECTRUM]
        gs = [polyline(ax, lx, r, color=c, stroke_width=3.5) for r, c in zip((r1, r3, r2), cols)]
        ds = [VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=c) for a, b in zip(lx, r)]) for r, c in zip((r1, r3, r2), cols)]
        labs = VGroup(
            MathTex(rf"\pi(x) \big/ \tfrac{{x}}{{\log x}}: \ {r1[-1]:.4f}", font_size=24, color=cols[0]),
            MathTex(rf"\psi(x) / x: \ {r3[-1]:.6f}", font_size=24, color=cols[1]),
            MathTex(rf"\pi(x) / \operatorname{{li}}(x): \ {r2[-1]:.6f}", font_size=24, color=cols[2]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        pc = MathTex(rf"\pi(10^8) = {int(pi_[-1]):,}".replace(",", r"{,}"), font_size=24).next_to(labs, RIGHT, buff=0.4)
        assert int(pi_[-1]) == 5761455 and abs(r3[-1] - 1) < 1e-4 and abs(r2[-1] - 1) < 2e-4
        pm = ProofMap([
            r"$\zeta(1 + it) \ne 0$ \ (3--4--1)",
            r"so the transform of a kernel built from $\zeta$ never vanishes",
            r"Wiener's Tauberian theorem moves a limit from that kernel to every kernel",
            r"$\psi(x) = \sum_{p^m \le x}\log p \sim x$",
            r"partial summation: \ $\pi(x) \sim x/\log x$",
        ], font_size=20, width=6.0, buff=0.14, direction=DOWN)
        pm.move_to([3.6, -0.4, 0])
        thm = label(r"\textbf{FA 9.12} \ the prime number theorem \ (Hadamard, de la Vall\'ee Poussin 1896; \ "
                    r"Wiener 1932)", font_size=22, color=C.EPS).to_edge(DOWN, buff=0.35)
        head = label(r"The prime number theorem, \ from Wiener", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Wiener's theorem then gives the prime number theorem. The non-vanishing of zeta "
            "on the line says that a certain kernel's transform has no zeros. <bookmark mark='b'/> Wiener's "
            "Tauberian theorem moves a known average from that kernel to every other kernel, and that unlocks "
            "Chebyshev's function psi, the sum of log p over prime powers, which is asymptotic to x. Partial summation "
            "converts that into the count of primes. <bookmark mark='c'/> Up to ten to the eight, counted exactly: psi "
            "of x over x is within two parts in a hundred thousand of one; pi of x over x over log x is still six "
            "percent high, closing in slowly; and the logarithmic integral fits to about one part in ten thousand. "
            "<bookmark mark='d'/> That's the analytic engine behind the Riemann video's second chapter."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(pm))
            self.play(*pm.light(0))
            self.play(*pm.light(1))
            vo.wait_until("b")
            for i in (2, 3, 4):
                self.play(*pm.light(i), run_time=0.8)
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl), Create(one))
            for g_, d_, l_ in zip(gs, ds, labs):
                self.play(Create(g_), FadeIn(d_), FadeIn(l_), run_time=1.2)
            self.play(FadeIn(pc))
            vo.wait_until("d")
            self.play(*pm.done(), FadeIn(thm))
        self.wait(0.4)
        self.clear_scene()
