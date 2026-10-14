from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis10.common import load, plain_axes, polyline, square_axes


def stems(ax, ks, vals, color, stroke_width=3):
    return VGroup(*[Line(ax.c2p(k, 0), ax.c2p(k, v), color=color, stroke_width=stroke_width) for k, v in zip(ks, vals)])


def zpath(ax, z, color, stroke_width=3.5):
    return VMobject(color=color, stroke_width=stroke_width).set_points_as_corners([ax.c2p(w.real, w.imag) for w in z])


class Gelfand(VoiceoverScene):
    def construct(self):
        self.card()
        self.transform()
        self.inverse()
        self.cstar()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"Gelfand theory", r"What does a commutative Banach algebra look like?", lit=(), part=10)
        with self.voiceover("Chapter four: Gelfand's theory, which turns every commutative Banach algebra into functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def transform(self):
        d = load("wiener")
        th, f = d["theta"], d["f"]
        ks = np.arange(-6, 9)
        a = np.where(ks == 0, 1.2, np.where(ks > 0, 1 / np.maximum(ks, 1) ** 2, 0.0))
        ax = plain_axes([-6, 8, 2], [0, 1.3, 0.5], 5.6, 2.0).move_to([-3.5, 1.2, 0])
        st = stems(ax, ks, a, C.FUNC)
        tops = VGroup(*[Dot(ax.c2p(k, v), radius=0.05, color=C.FUNC) for k, v in zip(ks, a) if v > 0])
        al = MathTex(r"a = (\ldots, 0, 1.2, 1, \tfrac14, \tfrac19, \ldots) \in \ell^1(\mathbb Z)", font_size=24,
                     color=C.FUNC).next_to(ax, UP, buff=0.08)
        cx = square_axes([-0.6, 3.2, 1], [-1.6, 1.6, 1], 0.95).move_to([3.4, 0.9, 0])
        curve = zpath(cx, np.append(f, f[0]), C.FREQ)
        zero = Dot(cx.c2p(0, 0), radius=0.06, color=C.PATHOLOGY)
        zl = MathTex(r"0", font_size=22, color=C.PATHOLOGY).next_to(zero, DL, buff=0.04)
        cl = MathTex(r"\hat a(\theta) = \sum_n a_n e^{in\theta}", font_size=26, color=C.FREQ).next_to(cx, UP, buff=0.08)
        arr = Arrow([-0.4, 1.2, 0], [1.4, 1.2, 0], buff=0, color=GREY_B, stroke_width=4)
        arl = label(r"Gelfand", font_size=22, color=GREY_B).next_to(arr, UP, buff=0.05)
        rows = VGroup(
            label(r"\textbf{RCA 18.17} \ maximal ideals $=$ kernels of the homomorphisms $h: A \to \mathbb C$",
                  font_size=22),
            MathTex(r"\hat x(h) = h(x): \ \ x \text{ becomes a continuous function on } \Delta = \{h\} \ (\text{compact, by "
                    r"Alaoglu})", font_size=24),
            MathTex(r"\sigma(x) = \text{the range of } \hat x", font_size=30, color=C.SPECTRUM),
            label(r"for $\ell^1(\mathbb Z)$: \ $h_\theta(a) = \sum a_n e^{in\theta}$, \ $\Delta$ is the circle, \ and "
                  r"$\hat a$ is the Fourier series", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.3)
        for r_ in rows:
            if r_.width > 13:
                r_.width = 13
        assert np.abs(f).min() > 0.3
        # the model case first: in C[0, 1] every point t gives a homomorphism h_t(g) = g(t), and they are all of them
        ex = plain_axes([0, 1, 0.25], [0, 1.3, 0.5], 5.6, 2.0).move_to(ax.get_center())
        xg = np.linspace(0, 1, 401)
        gfun = lambda t_: 0.65 + 0.3 * np.sin(5 * t_) * np.exp(-t_) + 0.15 * t_  # noqa: E731
        assert gfun(xg).min() > 0 and gfun(xg).max() < 1.3
        gcur = polyline(ex, xg, gfun(xg), color=C.FUNC, stroke_width=3)
        tT = ValueTracker(0.15)
        probe = always_redraw(lambda: VGroup(
            DashedLine(ex.c2p(tT.get_value(), 0), ex.c2p(tT.get_value(), gfun(tT.get_value())), color=C.EPS,
                       stroke_width=2.5),
            Dot(ex.c2p(tT.get_value(), gfun(tT.get_value())), radius=0.07, color=C.EPS)))
        hl = VGroup(MathTex(r"\text{in } C[0, 1]: \ h_t(g) = g(t), \ \ t =", font_size=24, color=C.EPS),
                    DecimalNumber(0.15, num_decimal_places=2, font_size=24, color=C.EPS),
                    MathTex(r":\ \ h_t(g) =", font_size=24, color=C.EPS),
                    DecimalNumber(float(gfun(0.15)), num_decimal_places=3, font_size=24, color=C.EPS)).arrange(
            RIGHT, buff=0.1).next_to(ex, UP, buff=0.08)
        hl[1].add_updater(lambda m: m.set_value(tT.get_value()))
        hl[3].add_updater(lambda m: m.set_value(float(gfun(tT.get_value()))))
        head = label(r"Every element becomes a function", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> In a commutative Banach algebra, the maximal ideals are exactly the kernels of the "
            "homomorphisms to the complex numbers. Gelfand's idea: evaluate x at every homomorphism. That turns x "
            "into a continuous function on the space of homomorphisms, which is compact, by Alaoglu's theorem. "
            "<bookmark mark='b'/> In summable sequences under convolution, the homomorphisms are indexed by an angle "
            "theta: sum a n times e to the i n theta. <bookmark mark='c'/> So the Gelfand transform of a sequence is "
            "its Fourier series, a closed curve in the plane. <bookmark mark='d'/> And the spectrum of x is the range "
            "of its transform: here, the curve itself."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[:2]), Create(ex), Create(gcur))
            self.play(FadeIn(probe), FadeIn(hl))
            self.play(tT.animate.set_value(0.9), run_time=7.0)
            self.play(tT.animate.set_value(0.45), run_time=3.0)
            vo.wait_until("b")
            for m_ in (probe, hl[1], hl[3]):
                m_.clear_updaters()
            self.play(FadeOut(VGroup(ex, gcur, probe, hl)), run_time=0.6)
            self.play(Create(ax), Create(st), FadeIn(tops), FadeIn(al), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(GrowArrow(arr), FadeIn(arl), Create(cx), FadeIn(zero), FadeIn(zl))
            self.play(Create(curve), FadeIn(cl), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), curve.animate.set_color(C.SPECTRUM))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inverse(self):
        d = load("wiener")
        f, Ns, partial, C_ = d["f"], d["Ns"], d["partial"], float(d["C"])
        cx = square_axes([-0.3, 2.8, 1], [-1.2, 1.2, 1], 1.05).move_to([-4.3, 1.1, 0])
        g = 1 / f
        curve = zpath(cx, np.append(g, g[0]), C.APPROX)
        cl = MathTex(r"1/\hat a(\theta) = \sum_n b_n e^{in\theta}", font_size=24, color=C.APPROX).next_to(cx, UP, buff=0.08)
        nl, tail = d["nl"], d["tail"]
        ax = plain_axes([0, 5, 1], [-11, 0, 2], 5.4, 2.4, numbers=True, font_size=16,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.6, -2.2, 0])
        dts = VGroup(*[Dot(ax.c2p(math.log10(n_), math.log10(v)), radius=0.04, color=C.APPROX) for n_, v in zip(nl, tail)])
        env = VMobject(color=GREY_B, stroke_width=2).set_points_as_corners(
            [ax.c2p(L_, math.log10(C_) - 2 * L_) for L_ in np.linspace(0.3, 5, 40)])
        yl = MathTex(r"\log_{10}|b_n| \ \text{vs} \ \log_{10} n; \ \ \text{line: } C/n^2", font_size=22).next_to(ax, UP,
                                                                                                      buff=0.05)
        late = nl >= 100
        assert np.allclose(np.log10(tail[late]), np.log10(C_ / nl[late] ** 2), atol=0.03)
        tab = VGroup(MathTex(r"N", r"\quad \sum_{|n| \le N}|b_n|", font_size=24, color=GREY_A))
        for N_, p_ in zip(Ns, partial):
            tab.add(MathTex(f"{N_:,}".replace(",", r"{,}"), rf"\quad {p_:.6f}", font_size=24))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.3, 1.65, 0])
        regrid(tab, gap=0.6)
        rows = VGroup(
            label(r"\textbf{Wiener's lemma} \ (RCA 18.21)", font_size=26, color=C.EPS),
            label(r"if $\hat a$ has $\sum |a_n| < \infty$ and never vanishes,", font_size=24),
            label(r"then $1/\hat a$ also has absolutely summable coefficients", font_size=24),
            label(r"proof, \ in three lines:", font_size=22, color=GREY_A),
            label(r"$\hat a(h) \ne 0$ for every $h$, \ so $a$ lies in no maximal ideal;", font_size=22),
            label(r"so $a$ is invertible in $\ell^1(\mathbb Z)$; \ and $\widehat{a^{-1}} = 1/\hat a$", font_size=22),
            label(r"Wiener's own proof (1932) took pages", font_size=22, color=GREY_A),
        )
        for r_ in rows:
            if r_.width > 5.6:
                r_.width = 5.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to([1.3, -1.35, 0], RIGHT, buff=0)
        assert np.all(np.diff(partial) > 0) and partial[-1] - partial[-2] < 1e-4
        head = label(r"Wiener's $1/f$ theorem, \ in three lines", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Here's what that buys. Our curve never passes through zero. Wiener asked: does one "
            "over it also have absolutely summable Fourier coefficients? <bookmark mark='b'/> Computed by fast "
            "Fourier transform: the coefficients of one over f decay like one over n squared, and their absolute "
            "sums settle at 2.65427. <bookmark mark='c'/> Gelfand's proof is three lines. The transform never "
            "vanishes, so the sequence lies in no maximal ideal. So it's invertible in the algebra, and the inverse "
            "transforms to one over f. Wiener's original proof took pages."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(cx), Create(curve), FadeIn(cl), FadeIn(rows[:3]))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yl), Create(env))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dts], lag_ratio=0.02), run_time=1.5)
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[3:6]))
            self.play(FadeIn(rows[6]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cstar(self):
        d = load("normal")
        lam, es, ef = d["lam"], float(d["err_star"]), float(d["err_f"])
        card = dictionary_card(r"commutative $C^*$-algebra", r"continuous functions", [
            (r"$\|x^*x\| = \|x\|^2$", r"$\sup|f|^2 = \sup|\bar f f|$"),
            (r"$x$ normal, \ $\sigma(x)$", r"the function $z$ on $\sigma(x)$"),
            (r"$f(x)$ for $f \in C(\sigma(x))$", r"$f \circ z$"),
            (r"$x^*$", r"$\bar z$"),
        ], font_size=24)
        card.scale_to_fit_width(10.5).move_to([0, 0.6, 0])
        thm = label(r"\textbf{FA 11.18} \ (Gelfand--Naimark) \ a commutative $C^*$-algebra is $C(\Delta)$, \ "
                    r"isometrically", font_size=26, color=C.EPS).to_edge(UP, buff=1.0)
        cx = square_axes([-1.6, 1.2, 1], [-1.4, 1.2, 1], 0.6).to_corner(DL, buff=0.4)
        dots = VGroup(*[Dot(cx.c2p(l_.real, l_.imag), radius=0.045, color=C.SPECTRUM) for l_ in lam])
        rows = VGroup(
            label(r"for a normal $6 \times 6$ matrix $A$ (spectrum, left):", font_size=22),
            MathTex(rf"A^* = p(A), \ p \text{{ interpolating }} \bar z \text{{ on }} \sigma(A): \ \text{{error }} {sci(es, 0)}",
                    font_size=24),
            MathTex(rf"\sqrt{{A}} \text{{ by eigenvectors}} = \sqrt{{A}} \text{{ by interpolation: }} {sci(ef, 0)}",
                    font_size=24),
            label(r"\textbf{GNS} (12.41): \ every $C^*$-algebra is an algebra of operators on a Hilbert space",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(cx, RIGHT, buff=0.5).align_to(cx, DOWN)
        assert es < 1e-9 and ef < 1e-9
        head = label(r"$C^*$-algebras are function algebras", font_size=34).to_edge(UP, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Add an adjoint, with the norm of x star x equal to the norm of x squared, the "
            "identity that holds for operators on Hilbert space. Then Gelfand-Naimark says: a commutative such "
            "algebra is exactly an algebra of continuous functions, with nothing lost. <bookmark mark='b'/> The "
            "dictionary: a normal element becomes the coordinate z on its spectrum, its adjoint becomes z bar, and "
            "any continuous f of it becomes f composed with z. <bookmark mark='c'/> For a normal matrix this is "
            "concrete. Its adjoint is a polynomial in the matrix, the one that interpolates z bar at the "
            "eigenvalues, and a square root computed two ways agrees to rounding error. <bookmark mark='d'/> And by "
            "the Gelfand-Naimark-Segal construction, every C-star algebra, commutative or not, is an algebra of "
            "operators."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(thm), Create(cx), FadeIn(dots))  # the spectrum, the space the functions live on
            vo.wait_until("b")
            self.play(FadeIn(card.titles))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_), FadeIn(a_)) for r_, a_ in zip(card.rows, card.arrows)],
                                  lag_ratio=0.4), run_time=3.0)
            vo.wait_until("c")
            self.play(Indicate(dots, color=C.SPECTRUM), FadeIn(rows[:3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()
