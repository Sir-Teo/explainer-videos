from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import left_y_axis, load, plain_axes, polyline, trap


class FourierL2(VoiceoverScene):
    def construct(self):
        self.card()
        self.complete()
        self.unbounded()
        self.fejer()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"Fourier series in $L^2$, and Fej\'er", r"Which functions equal their Fourier series?",
                            lit=(1807, 1907), part=6)
        with self.voiceover("Chapter nine: the Fourier question, answered in L two."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def complete(self):
        d = load("trigdense")
        t, ks, errs, kerns, smooths, f = d["t"], d["ks"], d["errs"], d["kerns"], d["smooths"], d["f"]
        kx = plain_axes([-math.pi, math.pi, math.pi / 2], [0, 30, 10], 5.0, 3.4, numbers=False).move_to([-3.6, -0.8, 0])
        kyn = left_y_axis(kx, (10, 20, 30))  # numbered at -pi: the narrowing bump never crosses a number
        assert 25 < float(kerns[-1].max()) < 30
        # 'a': the exponentials themselves, real parts cos nt, on the same window
        ex = plain_axes([-math.pi, math.pi, math.pi / 2], [-1.3, 1.3, 1], 5.0, 3.4, numbers=False).move_to(kx)
        ecols = [C.SEQ, C.APPROX, C.CONNECTED_SET, C.MEASURE]
        tt = np.linspace(-math.pi, math.pi, 400)
        eg = VGroup(*[polyline(ex, tt, np.cos(n * tt), color=ecols[n], stroke_width=3) for n in range(4)])
        e_l = MathTex(r"\mathrm{Re}\, e^{int} = \cos nt, \ ", "n = 0,", "\ 1,", "\ 2,", "\ 3", font_size=26).next_to(
            ex, UP, buff=0.1)
        for n in range(4):
            e_l[1 + n].set_color(ecols[n])
        # orthonormal in L^2(T) with <f, g> = (1/2pi) int f conj(g): check on the grid
        tq = np.linspace(-math.pi, math.pi, 4001)
        gram_ = np.array([[trap(np.exp(1j * m * tq) * np.exp(-1j * n * tq), tq) / (2 * math.pi) for n in range(4)]
                          for m in range(4)])
        assert np.allclose(gram_, np.eye(4), atol=1e-6)
        on_l = MathTex(r"\tfrac{1}{2\pi}\int_{-\pi}^{\pi} e^{imt}\,\overline{e^{int}}\,dt = \delta_{mn}", font_size=28,
                       color=C.INNER).move_to([2.6, -0.8, 0])
        kt = VGroup(*[MathTex(s, font_size=20).next_to(kx.c2p(v, 0), DOWN, buff=0.1)
                      for s, v in ((r"-\pi", -math.pi), ("0", 0), (r"\pi", math.pi))])
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.EPS), i / (len(ks) - 1)) for i in range(len(ks))]
        kc = [polyline(kx, t, kerns[i], color=cols[i], stroke_width=3) for i in range(len(ks))]
        k_l = [MathTex(rf"Q_{{{k}}}(t) = c_{{{k}}}\Big(\frac{{1 + \cos t}}{{2}}\Big)^{{{k}}}", font_size=26,
                       color=cols[i]).next_to(kx, UP, buff=0.1) for i, k in enumerate(ks)]
        fx = plain_axes([-math.pi, math.pi, math.pi / 2], [0, 3.4, 1], 5.0, 3.4, numbers=False).move_to([2.6, -0.8, 0])
        ft = VGroup(*[MathTex(s, font_size=20).next_to(fx.c2p(v, 0), DOWN, buff=0.1)
                      for s, v in ((r"-\pi", -math.pi), ("0", 0), (r"\pi", math.pi))])
        gf = polyline(fx, t, f, color=WHITE, stroke_width=4)
        f_l = MathTex(r"f(t) = |t|", font_size=26).next_to(fx.c2p(0.2, 3.1), RIGHT, buff=0)  # inside the V
        sc = [polyline(fx, t, smooths[i], color=cols[i], stroke_width=3) for i in range(len(ks))]
        s_l = [MathTex(rf"\|Q_{{{k}}} * f - f\|_\infty = {e:.4f}", font_size=26, color=cols[i]).next_to(fx, UP, buff=0.1)
               for i, (k, e) in enumerate(zip(ks, errs))]
        assert np.all(np.diff(errs) < 0)
        chain = VGroup(
            label(r"$Q_k * f$ is a trigonometric polynomial of degree $k$, \ and $\to f$ uniformly \ (RCA 4.24)",
                  font_size=24),
            label(r"$C(T)$ is dense in $L^2(T)$ \ $\Rightarrow$ \ trigonometric polynomials are dense in $L^2(T)$ "
                  r"\ $\Rightarrow$ \ $\{e^{int}\}$ is maximal", font_size=24, color=C.EPS),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.35)
        head = label(r"Is $\{e^{int} : n \in \Z\}$ a maximal orthonormal set in $L^2(T)$?", font_size=34).to_edge(UP,
                                                                                                             buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The exponentials e to the i n t are orthonormal in L two of the circle. Are they "
            "maximal? If so, the last chapter's theorem answers the Fourier question at once. "
            "<bookmark mark='b'/> Rudin's proof uses a bump made from a trigonometric polynomial: one plus cosine "
            "t, over two, to the power k, scaled to have average one. As k grows it narrows onto zero. "
            "<bookmark mark='c'/> Convolving a continuous function with it averages the function over a shrinking "
            "window, and the result is a trigonometric polynomial. On the absolute value, the largest error falls "
            "from 0.93 to 0.07. <bookmark mark='d'/> So trigonometric polynomials are uniformly dense in the "
            "continuous functions, and those are dense in L two. Nothing nonzero is perpendicular to every "
            "exponential: the system is maximal."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ex), LaggedStart(*[Create(g_) for g_ in eg], lag_ratio=0.3), FadeIn(e_l),
                      run_time=2.0)
            self.play(FadeIn(on_l))
            vo.wait_until("b")
            self.play(FadeOut(ex), FadeOut(eg), FadeOut(e_l), FadeOut(on_l), Create(kx), FadeIn(kyn), FadeIn(kt),
                      Create(kc[0]), FadeIn(k_l[0]))
            for i in range(1, len(ks)):
                self.play(kc[i - 1].animate.set_stroke(opacity=0.3, width=1.5), Create(kc[i]),
                          FadeTransform(k_l[i - 1], k_l[i]), run_time=0.8)
            vo.wait_until("c")
            self.play(Create(fx), FadeIn(ft), Create(gf), FadeIn(f_l))
            self.play(Create(sc[0]), FadeIn(s_l[0]))
            for i in range(1, len(ks)):
                self.play(ReplacementTransform(sc[i - 1], sc[i]), FadeTransform(s_l[i - 1], s_l[i]), run_time=0.9)
            vo.wait_until("d")
            self.play(FadeIn(chain[0]))
            self.play(FadeIn(chain[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unbounded(self):
        d = load("unbounded")
        c, norm2, Ns, l2, xs, curves = d["c"], float(d["norm2"]), d["Ns"], d["l2"], d["xs"], d["curves"]
        ax = plain_axes([-math.pi, math.pi, math.pi / 2], [0, 4.2, 1], 6.0, 3.8, numbers=False).move_to([-3.0, -0.4, 0])
        tk = VGroup(*[MathTex(s, font_size=20).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for s, v in ((r"-\pi", -math.pi), ("0", 0), (r"\pi", math.pi))])
        ax.y_axis.set_opacity(0)  # the y-axis at x = 0 would run under the spike: it stands at -pi instead
        yk = left_y_axis(ax, (1, 2, 3, 4), font_size=20)
        xr = np.concatenate([np.linspace(-math.pi, -0.0037, 600), np.linspace(0.0037, math.pi, 600)])
        fr = np.abs(xr) ** -0.25
        gf = VGroup(polyline(ax, xr[:600], fr[:600], color=WHITE, stroke_width=4),
                    polyline(ax, xr[600:], fr[600:], color=WHITE, stroke_width=4))
        arrow_up = Arrow(ax.c2p(0, 3.2), ax.c2p(0, 4.2), buff=0, color=WHITE, stroke_width=3, tip_length=0.15)
        f_l = MathTex(r"f(x) = |x|^{-1/4}", font_size=28).next_to(ax.c2p(0.4, 3.6), RIGHT, buff=0.1)
        cols = [C.SEQ, C.APPROX, C.EPS]
        pc = [runs(ax, xs, cv, cols[i], 2.5) for i, cv in enumerate(curves)]
        pl = [MathTex(rf"s_{{{N}}}", font_size=28, color=cols[i]).next_to(ax.c2p(-2.6, 0.5), UP, buff=0.0)
              for i, N in enumerate((4, 16, 64))]
        facts = VGroup(
            label(r"unbounded, \ so not Riemann integrable", font_size=24, color=C.PATHOLOGY),
            MathTex(rf"\|f\|_2^2 = \frac{{1}}{{2\pi}}\int_{{-\pi}}^{{\pi}} |x|^{{-1/2}}dx = \frac{{2}}{{\sqrt\pi}} = {norm2:.4f}",
                    font_size=26),
            MathTex(r"N", r"\quad \|f - s_N\|_2", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.9, 1.4, 0])
        tab = VGroup()
        for N, v in zip(Ns, l2):
            tab.add(MathTex(f"{N}", rf"\quad {v:.4f}", font_size=26, color=C.EPS))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(facts, DOWN, buff=0.12).align_to(facts, LEFT)
        col2 = max(max(r_[0].get_right()[0] for r_ in tab), facts[2][0].get_right()[0]) + 0.3
        for row in list(tab) + [facts[2]]:  # the second column starts clear of the widest N
            row[1].shift((col2 - row[1].get_left()[0]) * RIGHT)
        rate = label(r"$\times 0.707 = 4^{-1/4}$ per factor 4 in $N$: \ slow, \ but to $0$", font_size=22,
                     color=GREY_A).next_to(tab, DOWN, buff=0.12).align_to(facts, LEFT)
        assert np.all(np.diff(l2) < 0) and np.all(np.abs(l2[1:] / l2[:-1] - 4 ** -0.25) < 0.02)
        thm = VGroup(
            label(r"\textbf{RCA 4.26} \ for every $f \in L^2(T)$: \ $\|f - s_N f\|_2 \to 0$ \ and \ "
                  r"$\sum_{n \in \Z} |\hat f(n)|^2 = \|f\|_2^2$", font_size=26, color=C.EPS),
            label(r"and every square-summable $(c_n)$ is the Fourier series of some $f \in L^2$: \ $L^2(T) \cong \ell^2(\Z)$",
                  font_size=24, color=C.INNER),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.35)
        head = label(r"The answer in $L^2$, \ even for functions Riemann could not integrate", font_size=34).to_edge(UP,
                                                                                                                 buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> So Parseval holds for every square-integrable function, with nothing assumed "
            "about continuity or boundedness. Here's a function Riemann's integral can't handle: the absolute value "
            "of x, to the minus a quarter. It's unbounded at zero, but its square has finite integral. "
            "<bookmark mark='b'/> Its Fourier partial sums with four, sixteen and sixty-four terms climb toward the "
            "spike. <bookmark mark='c'/> The mean square error falls steadily: each fourfold increase in N "
            "multiplies it by 0.707. Slowly, but to zero. <bookmark mark='d'/> That's the Fourier thread's answer: "
            "for every function in L two, the partial sums converge to it in L two, and Parseval's identity holds. "
            "Conversely, every square-summable sequence of coefficients comes from a function. L two of the circle "
            "and little l two of the integers are the same Hilbert space."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(tk), FadeIn(yk), Create(gf), GrowArrow(arrow_up), FadeIn(f_l))
            self.play(FadeIn(facts[:2]))
            vo.wait_until("b")
            self.play(Create(pc[0]), FadeIn(pl[0]))
            for i in (1, 2):
                self.play(pc[i - 1].animate.set_stroke(opacity=0.3), Create(pc[i]), FadeTransform(pl[i - 1], pl[i]),
                          run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(rate))
            vo.wait_until("d")
            self.play(FadeIn(thm[0]))
            self.play(FadeIn(thm[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fejer(self):
        d = load("fejer")
        x, Ns, K = d["x"], d["Ns"], d["K"]
        xs, f, s200, sig200, l2, sup_err = d["xs"], d["f"], d["s200"], d["sig200"], d["l2"], d["sup_err"]
        N = 10
        kx = plain_axes([-math.pi, math.pi, math.pi / 2], [-5, 22, 5], 5.4, 3.2, numbers=False).move_to([-3.6, 0.55, 0])
        with np.errstate(invalid="ignore", divide="ignore"):
            D = np.sin((N + 0.5) * x) / np.sin(x / 2)
        D[np.isclose(x, 0)] = 2 * N + 1
        assert abs(trap(D, x) / (2 * math.pi) - 1) < 1e-6
        L1 = trap(np.abs(D), x) / (2 * math.pi)
        gD = polyline(kx, x[::4], D[::4], color=C.SEQ, stroke_width=2.5)
        neg = VGroup()
        Dn = np.minimum(D, 0)
        pts = [kx.c2p(a, 0) for a in x[::4]] + [kx.c2p(a, b) for a, b in zip(x[::-4], Dn[::-4])]
        neg = Polygon(*pts, stroke_width=0, fill_color=C.PATHOLOGY, fill_opacity=0.5)
        Kn = K[list(Ns).index(N)]
        gK = polyline(kx, x[::4], Kn[::4], color=C.EPS, stroke_width=3.5)
        assert Kn.min() >= -1e-12 and abs(trap(Kn, x) / (2 * math.pi) - 1) < 1e-6
        kl = VGroup(MathTex(rf"D_{{{N}}}: \ \tfrac{{1}}{{2\pi}}\!\int |D_{{{N}}}| = {L1:.3f}", font_size=24, color=C.SEQ),
                    MathTex(rf"K_{{{N}}} = \tfrac{{1}}{{N + 1}}\sum_{{n \le N}} D_n \ge 0, \ \tfrac{{1}}{{2\pi}}\!\int K_{{{N}}} = 1",
                            font_size=24, color=C.EPS)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(kx, UP,
                                                                                                    buff=0.08)
        sx = plain_axes([0, 2 * math.pi, math.pi / 2], [-2.1, 2.1, 1], 5.4, 2.4, numbers=False).move_to([-3.6, -2.5, 0])
        saw = VGroup(polyline(sx, xs, f, color=WHITE, stroke_width=2.5))
        gs = polyline(sx, xs[::2], s200[::2], color=C.SEQ, stroke_width=2)
        gsig = polyline(sx, xs[::2], sig200[::2], color=C.EPS, stroke_width=3)
        lvl = DashedLine(sx.c2p(0, math.pi / 2), sx.c2p(2.7, math.pi / 2), color=GREY_B, stroke_width=1.5)  # stops before the inset
        sl = MathTex(r"s_{200}", font_size=24, color=C.SEQ).move_to(sx.c2p(0.9, -0.9))
        sgl = MathTex(r"\sigma_{200}", font_size=24, color=C.EPS).move_to(sx.c2p(0.9, -1.55))
        # the overshoot, magnified: x in [0, 0.25], y in [1.3, 1.95], in the empty upper right of the plot
        zx0, zx1, zy0, zy1 = 0.0, 0.25, 1.3, 1.95
        za = plain_axes([zx0, zx1, 0.05], [zy0, zy1, 0.25], 2.1, 0.95, numbers=False).move_to(sx.c2p(4.75, 1.25))
        zm = (xs >= zx0) & (xs <= zx1)
        zs = runs(za, xs[zm], s200[zm], C.SEQ, 2)
        zg = runs(za, xs[zm], sig200[zm], C.EPS, 3)
        zl = DashedLine(za.c2p(zx0, math.pi / 2), za.c2p(zx1, math.pi / 2), color=GREY_B, stroke_width=1.5)
        zf = SurroundingRectangle(za, buff=0.04, color=GREY_B, stroke_width=1.5)
        src = Rectangle(width=sx.c2p(zx1, 0)[0] - sx.c2p(zx0, 0)[0], height=sx.c2p(0, zy1)[1] - sx.c2p(0, zy0)[1],
                        color=GREY_B, stroke_width=1.5).move_to(sx.c2p((zx0 + zx1) / 2, (zy0 + zy1) / 2))
        link = DashedLine(src.get_right(), zf.get_left(), color=GREY_B, stroke_width=1.2)
        zt = MathTex(rf"\times {(zf.width / src.width):.0f}", font_size=20, color=GREY_B).move_to(zf.get_corner(DR) + np.array([-0.25, 0.17, 0]))
        assert s200[zm].max() > math.pi / 2 + 0.25 and sig200[zm].max() < math.pi / 2  # the overshoot is in the window
        assert s200.max() > math.pi / 2 + 0.25 and sig200.max() <= math.pi / 2
        panel = VGroup(
            label(r"$s_N$ \ (partial sums)", font_size=26, color=C.SEQ),
            MathTex(r"\|f - s_N\|_2 = " + ",\\ ".join(f"{v:.3f}" for v in l2) + r"\ (N = 10, 50, 200)", font_size=24),
            MathTex(rf"\max s_{{200}} = {s200.max():.3f} > \tfrac{{\pi}}{{2}} = {math.pi / 2:.3f} \ \text{{(Gibbs)}}",
                    font_size=24, color=C.PATHOLOGY),
            label(r"$\sigma_N = \frac{s_0 + \cdots + s_N}{N + 1} = f * K_N$ \ (Fej\'er, 1900)", font_size=26, color=C.EPS),
            MathTex(rf"\max \sigma_{{200}} = {sig200.max():.3f} \le \tfrac{{\pi}}{{2}}: \ \text{{no overshoot, ever}}",
                    font_size=24, color=C.CONNECTED_SET),
            label(r"continuous $f$ (the triangle wave): \ $\sigma_N \to f$ uniformly", font_size=24),
            MathTex(r"\|f - \sigma_N\|_\infty = " + ",\\ ".join(f"{v:.3f}" for v in sup_err) + r"\ (N = 4, 16, 64)",
                    font_size=24, color=C.CONNECTED_SET),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.55, -0.75, 0])
        for r_ in panel:
            if r_.width > 6.4:
                r_.width = 6.4
        panel.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.55, -0.75, 0])
        panel[3].shift(DOWN * 0.15)
        panel[4:].shift(DOWN * 0.15)
        assert np.all(np.diff(sup_err) < 0)
        head = label(r"Two kernels: \ Dirichlet's has negative lobes, \ Fej\'er's has none", font_size=32).to_edge(UP,
                                                                                                            buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> In the uniform norm the story is different, and the kernels show why. The n-th "
            "partial sum is the convolution with Dirichlet's kernel, which has negative lobes, shaded red. Its "
            "absolute integral grows with N, and that's what allows Gibbs' overshoot and even divergence. "
            "<bookmark mark='b'/> Fejér averaged the partial sums. The average is a convolution with Fejér's kernel, "
            "which is never negative and has mass one, the same narrowing bump as before. "
            "<bookmark mark='c'/> On the sawtooth, the partial sums overshoot to 1.844, above pi over two. Fejér's "
            "means never do: an average with positive weights can't leave the range of the function. "
            "<bookmark mark='d'/> So the dashboard splits. Partial sums converge in L two for every square-integrable "
            "function. Fejér's means converge uniformly for every continuous one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(kx))
            self.play(Create(gD), FadeIn(neg), FadeIn(kl[0]))
            vo.wait_until("b")
            self.play(Create(gK), FadeIn(kl[1]))
            vo.wait_until("c")
            self.play(Create(sx), Create(saw), Create(lvl))
            self.play(Create(gs), FadeIn(sl), FadeIn(panel[:3]))
            self.play(Create(src), Create(link), Create(zf), Create(zl), Create(zs), FadeIn(zt))
            self.play(Create(gsig), Create(zg), FadeIn(sgl), FadeIn(panel[3:5]))
            vo.wait_until("d")
            self.play(FadeIn(panel[5:]))
        self.wait(0.4)
        self.clear_scene()
