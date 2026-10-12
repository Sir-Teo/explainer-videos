from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis7.common import phase_wheel
from videos.analysis9.common import SQ2PI, bump, cplot, load, plain_axes, polyline

_S = np.linspace(-1, 1, 401)
_W = bump(_S) * (_S[1] - _S[0])  # trapezoid weights; the bump vanishes at the ends


def bump_hat(Z):
    """The bump's transform (1/sqrt(2 pi)) int b(s) e^(-isz) ds, at every point of the complex array Z."""
    z = np.asarray(Z, complex).ravel()
    out = np.concatenate([np.exp(-1j * np.outer(z[i:i + 6000], _S)) @ _W for i in range(0, len(z), 6000)]) / SQ2PI
    return out.reshape(np.shape(Z))


class PaleyWiener(VoiceoverScene):
    def construct(self):
        self.card()
        self.entire()
        self.converse()
        self.quasianalytic()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"Paley--Wiener", r"What does compact support look like in frequency?", lit=(1945,), part=9)
        with self.voiceover("Chapter nine: the Paley-Wiener theorem, where support in space becomes growth in the complex "
                            "plane."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def entire(self):
        d = load("paleywiener")
        ys, vals, rates, tr, real = d["ys"], d["vals"], d["rates"], d["tr"], d["real"]
        assert np.allclose(np.abs(bump_hat(1j * ys[:6])), vals[:6], rtol=1e-8)
        cx = plain_axes([-24, 24, 8], [-6, 6, 3], 11.2, 2.6, numbers=True, font_size=16,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([0.3, 0.55, 0])
        img = cplot(cx, bump_hat, (-24, 24), (-6, 6), px=1200)
        wheel = phase_wheel(0.32).next_to(cx, LEFT, buff=0.2).shift(DOWN * 0.3)
        zl = MathTex(r"\hat b(z), \ \ z = t + iy", font_size=26, color=C.FREQ).next_to(cx, UP, buff=0.08).align_to(cx, LEFT)
        # the bump itself, small
        bx = plain_axes([-1.5, 1.5, 0.5], [0, 0.45, 0.2], 2.4, 0.8).next_to(zl, RIGHT, buff=1.2).align_to(zl, DOWN)
        xs = np.linspace(-1.5, 1.5, 601)
        bg = polyline(bx, xs, bump(xs), color=C.TEST_FN, stroke_width=3)
        bl = MathTex(r"b = e^{-1/(1 - x^2)} \text{ on } [-1, 1]", font_size=22, color=C.TEST_FN).next_to(bx, RIGHT,
                                                                                                         buff=0.15)
        rows = VGroup(
            MathTex(r"\hat b(z) = \frac{1}{\sqrt{2\pi}}\int_{-1}^{1} b(x)\,e^{-ixz}\,dx \ \text{ makes sense for every } "
                    r"z \in \mathbb C: \ \text{entire}", font_size=26),
            MathTex(r"|e^{-ixz}| = e^{x\,\mathrm{Im}\,z} \le e^{|\mathrm{Im}\,z|} \ \ (|x| \le 1)", font_size=26,
                    color=GREY_A),
            MathTex(r"\tfrac{1}{y}\log|\hat b(iy)|: \ \ " + r",\ ".join(f"{r:.3f}" for r in rates[2:]) +
                    r" \ \to 1 = A", font_size=26, color=C.EPS),
            MathTex(r"\text{on } \mathbb R: \ \ t^4 \max_{[t, 2t]}|\hat b| = " +
                    r",\ ".join(sci(v * t_**4, 1) for t_, v in zip(tr, real)) + r" \ \ (t = 10, \ldots, 160)",
                    font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.25)
        assert np.all(np.diff(rates) > 0) and rates[-1] > 0.89 and real[-1] * tr[-1] ** 4 < real[0] * tr[0] ** 4
        head = label(r"The transform of a bump is an entire function", font_size=34).to_edge(UP, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> Take the bump, supported on minus one to one. Its transform is an integral over a "
            "bounded interval, so it makes sense for complex t as well, and it's an entire function. "
            "<bookmark mark='b'/> Here it is, colored by phase, with brightness rising with size. Along the real axis "
            "it oscillates and dies, with its zeros where all the colors meet. <bookmark mark='c'/> Vertically, it "
            "grows: the exponential has size e to the x times the imaginary part, at most e to the absolute value of "
            "the imaginary part, because x stays within one. <bookmark mark='d'/> On the imaginary axis the growth "
            "rate creeps up toward exactly one, the half-width of the support. And along the real axis it decays "
            "faster than any power."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(bx), Create(bg), FadeIn(bl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(img), Create(cx), FadeIn(zl), FadeIn(wheel), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            self.play(FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def converse(self):
        d = load("pwshift")
        ys, inside, outside, b05 = d["ys"], d["inside"], d["outside"], float(d["b05"])
        cx = plain_axes([-12, 12, 4], [-1, 9, 2], 6.2, 2.6, numbers=True, font_size=16,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.4, 0.9, 0])
        img = cplot(cx, bump_hat, (-12, 12), (-1, 9), px=800)
        yT = ValueTracker(0.0)
        line = always_redraw(lambda: Line(cx.c2p(-12, yT.get_value()), cx.c2p(12, yT.get_value()), color=WHITE,
                                          stroke_width=4))
        yl = always_redraw(lambda: MathTex(rf"\mathrm{{Im}}\,z = {yT.get_value():.1f}", font_size=24).next_to(
            cx.c2p(12, yT.get_value()), RIGHT, buff=0.1))
        inv = MathTex(r"b(x) = \frac{1}{\sqrt{2\pi}}\int_{\mathrm{Im}\,z = y} \hat b(z)\,e^{ixz}\,dz", font_size=30).move_to(
            [3.6, 2.2, 0])
        tab = VGroup(MathTex(r"y", r"\quad x = 0.5", r"\quad x = 1.5", font_size=24, color=GREY_A))
        for y, a, b in zip(ys, inside, outside):
            tab.add(MathTex(f"{y:g}", rf"\quad {a:.6f}", rf"\quad {sci(abs(b), 0)}", font_size=24))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.6, 0.6, 0])
        for row in tab[1:]:
            row[1].align_to(tab[0][1], LEFT)
            row[2].align_to(tab[0][2], LEFT)
            row[1].set_color(C.TEST_FN)
            row[2].set_color(C.DISTRIBUTION)
        tnote = label(rf"inside: \ $b(0.5) = e^{{-4/3}} = {b05:.6f}$ \ at every height; \ outside: \ quadrature noise",
                      font_size=20, color=GREY_A).next_to(tab, DOWN, buff=0.12)
        pm = ProofMap([
            r"$|\hat b(z)| \le C_N (1 + |z|)^{-N} e^{A|y|}$",
            r"shift the inversion line to $\mathrm{Im}\,z = y$ \ (Cauchy)",
            r"$|e^{ixz}| = e^{-xy}$: \ the integrand is $\le C e^{(A - x)y}$",
            r"$x > A$: \ let $y \to \infty$, \ so $f(x) = 0$",
        ], font_size=22, width=3.1, buff=0.25, direction=RIGHT)
        pm.to_edge(DOWN, buff=0.3)
        thm = label(r"\textbf{FA 7.22} \ $f \in C_c^\infty$, \ $\operatorname{supp} f \subset [-A, A]$ \ $\iff$ \ "
                    r"$\hat f$ entire, \ $|\hat f(z)| \le C_N (1 + |z|)^{-N} e^{A|\mathrm{Im}\,z|}$", font_size=24,
                    color=C.EPS).next_to(pm, UP, buff=0.2)
        assert np.allclose(inside, b05, atol=1e-6) and np.abs(outside).max() < 1e-7
        head = label(r"Growth in the plane forces compact support", font_size=34).to_edge(UP, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> The Paley-Wiener theorem says this is a characterization: a smooth function is "
            "supported in minus A to A exactly when its transform is entire, decays on horizontal lines, and grows no "
            "faster than e to the A times the imaginary part. <bookmark mark='b'/> Here's the converse. Write the "
            "inversion integral along a horizontal line, and push the line up. By Cauchy's theorem the answer doesn't "
            "change: at x equal to one half, inside the support, every height gives the same value of the bump. "
            "<bookmark mark='c'/> But at x equal to one and a half, the factor e to the i x z shrinks like e to the "
            "minus x y, faster than the transform grows. As the line rises, the bound goes to zero, so the function "
            "is zero there. <bookmark mark='d'/> Support in space is growth in the complex plane."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(img), Create(cx), FadeIn(inv))
            self.add(line, yl)
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            for k in range(1, 4):
                self.play(yT.animate.set_value(float(ys[k])), FadeIn(tab[k + 1]), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(tnote), FadeIn(pm))
            for i in range(4):
                self.play(*pm.light(i), run_time=0.6)
            vo.wait_until("d")
            self.play(*pm.done())
        for m in (line, yl):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quasianalytic(self):
        d = load("gevrey")
        ns, sups, a, b = d["ns"], d["sups"], d["a"], d["b"]
        ax = plain_axes([0, 21, 5], [0, 28, 5], 6.2, 3.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.3, -0.2, 0])
        n1 = ns[1:]
        da = VGroup(*[Dot(ax.c2p(n, v), radius=0.05, color=C.PATHOLOGY) for n, v in zip(n1, a)])
        db = VGroup(*[Dot(ax.c2p(n, v), radius=0.05, color=C.TEST_FN) for n, v in zip(n1, b)])
        la = MathTex(r"\big(\sup|b^{(n)}| / n!\big)^{1/n}", font_size=24, color=C.PATHOLOGY).next_to(
            ax.c2p(14, a[13]), LEFT, buff=0.2)
        lb = MathTex(r"\big(\sup|b^{(n)}| / n!^2\big)^{1/n}", font_size=24, color=C.TEST_FN).next_to(ax.c2p(12, 3.4), UP,
                                                                                                     buff=0.3)
        nl = MathTex(r"n", font_size=22).next_to(ax.x_axis, RIGHT, buff=0.1)
        rows = VGroup(
            MathTex(rf"\sup|b^{{(n)}}|: \ {sups[0]:.4f},\ {sups[1]:.4f},\ {sups[2]:.3f},\ {sups[3]:.1f},\ \ldots,\ "
                    rf"{sci(sups[20], 3)} \ (n = 20)", font_size=22),
            label(r"an analytic function has $|f^{(n)}| \le C^{n+1} n!$: \ the red dots would stay bounded", font_size=22,
                  color=GREY_A),
            label(r"the bump is flat at $\pm 1$, \ so it cannot be analytic: \ they grow like $n$", font_size=22,
                  color=C.PATHOLOGY),
            label(r"\textbf{RCA 19.11} \ (Denjoy--Carleman) \ a class $|f^{(n)}| \le \beta^n M_n$ \ contains a bump", font_size=22),
            MathTex(r"\iff \ \sum_n \frac{M_{n-1}}{M_n} < \infty: \qquad M_n = n!: \ \sum \tfrac1n = \infty, "
                    r"\qquad M_n = n!^2: \ \sum \tfrac{1}{n^2} < \infty", font_size=24, color=C.EPS),
            label(r"so compact support needs derivatives growing faster than $n!$: \ the price of a bump",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.6, -0.3, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        head = label(r"How fast can derivatives grow? \ Quasi-analytic classes", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> This is the honest end of Part 2's function e to the minus one over x squared. A "
            "bump is smooth but can't be analytic, because it's flat at the edges of its support. How does that show? "
            "<bookmark mark='b'/> In the derivatives. Computed exactly up to order twenty, the largest derivative, "
            "divided by n factorial, to the one over n, grows without bound, so no analytic bound holds. "
            "<bookmark mark='c'/> Divided by n factorial squared instead, it stays bounded: the bump lives in the "
            "class with bounds like n factorial squared. <bookmark mark='d'/> The Denjoy-Carleman theorem says "
            "exactly which classes contain a bump: those whose sum of ratios converges. For n factorial it diverges, "
            "no bumps, the analytic world; for n factorial squared it converges, and bumps exist."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(nl))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in da], lag_ratio=0.12), FadeIn(la), run_time=2.0)
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in db], lag_ratio=0.12), FadeIn(lb), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3:5]))
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()
