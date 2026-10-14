from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import load, plain_axes, polyline
from videos.analysis3.compute import tent


def secant(t, x, y):
    """g_xy for f = e^x and the polynomial algebra: the line through (x, e^x) and (y, e^y)."""
    if abs(x - y) < 1e-12:  # y = x: the tangent, the limit of the secants
        return math.exp(x) + math.exp(x) * (t - x)
    s = (math.exp(y) - math.exp(x)) / (y - x)
    return math.exp(x) + s * (t - x)


def interval_bars(ax, t, mask, y, color, height=0.07, opacity=0.85) -> VGroup:
    """The set {t : mask} drawn as bars on a row at height y (scene units) under the axes ``ax``."""
    g, start = VGroup(), None
    for i in range(len(t) + 1):
        on = i < len(t) and mask[i]
        if on and start is None:
            start = i
        elif not on and start is not None:
            a, b = ax.c2p(t[start], 0)[0], ax.c2p(t[i - 1], 0)[0]
            g.add(Rectangle(width=max(b - a, 0.02), height=height, stroke_width=0, fill_color=color,
                            fill_opacity=opacity).move_to([(a + b) / 2, y, 0]))
            start = None
    return g


class StoneWeierstrass(VoiceoverScene):
    def construct(self):
        self.card()
        self.needs()
        self.theorem()
        self.step_abs()
        self.step_lattice()
        self.caps_one()
        self.caps_all()
        self.complex_case()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(12, r"Stone--Weierstrass", r"Which families of functions can imitate every continuous one?",
                            lit=(), part=3)
        with self.voiceover(
            "Chapter twelve. In 1937 Marshall Stone asked what it is about polynomials that makes Weierstrass's "
            "theorem true."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def needs(self):
        defs = VGroup(
            label(r"an \textbf{algebra} $\mathcal A$: \ closed under $f + g$, \ $fg$, \ $cf$ \ (Rudin 7.28)", font_size=26),
            label(r"\textbf{separates points}: \ $x \ne y \Rightarrow$ some $f \in \mathcal A$ has $f(x) \ne f(y)$ "
                  r"\ (7.30)", font_size=26, color=C.SEQ),
            label(r"\textbf{vanishes at no point}: \ every $x$ has some $f \in \mathcal A$ with $f(x) \ne 0$",
                  font_size=26, color=C.MEASURE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(UP, buff=0.3)
        W, H = 3.7, 2.4
        cx = (-4.55, 0.0, 4.55)
        cy = -1.15
        axA = plain_axes([-1, 1, 0.5], [-1.2, 1.2, 0.5], W, H).move_to([cx[0], cy, 0])
        axB = plain_axes([0, 1, 0.5], [-0.3, 1.3, 0.5], W, H).move_to([cx[1], cy, 0])
        axC = plain_axes([0, 1, 0.5], [-0.05, 0.6, 0.25], W, H).move_to([cx[2], cy, 0])
        xa = np.linspace(-1, 1, 801)
        xb = np.linspace(0, 1, 801)
        # panel A: even polynomials on [-1, 1] cannot reach f(x) = x
        evens = [np.array([0.0, 0.0, 0.0]), np.array([0.1, 0.9, -0.2]), np.array([-0.3, 1.6, -1.2]),
                 np.array([0.2, -0.8, 0.5])]  # coefficients of 1, x^2, x^4
        for c in evens:
            g = c[0] + c[1] * xa**2 + c[2] * xa**4
            assert np.abs(g - xa).max() >= 1 - 1e-12 and np.allclose(g, g[::-1])
        sA = ValueTracker(0.0)

        def ev(x):
            s = sA.get_value()
            i = min(int(s), len(evens) - 2)
            c = evens[i] + (s - i) * (evens[i + 1] - evens[i])
            return c[0] + c[1] * x**2 + c[2] * x**4

        x0 = 0.7
        tgtA = polyline(axA, xa, xa, color=WHITE, stroke_width=3.5).set_z_index(2)
        gA = always_redraw(lambda: runs(axA, xa, ev(xa), C.APPROX, 3))

        def pairA():
            v = float(ev(np.array([x0]))[0])
            pL, pR = axA.c2p(-x0, v), axA.c2p(x0, v)
            return VGroup(DashedLine(pL, pR, color=C.APPROX, stroke_width=1.5, dash_length=0.06),
                          Line(pL, axA.c2p(-x0, -x0), color=C.PATHOLOGY, stroke_width=3),
                          Line(pR, axA.c2p(x0, x0), color=C.PATHOLOGY, stroke_width=3),
                          Dot(pL, radius=0.05, color=C.APPROX), Dot(pR, radius=0.05, color=C.APPROX))

        prA = always_redraw(pairA)
        tA = VGroup(label(r"even polynomials on $[-1, 1]$", font_size=22),
                    MathTex(r"g(-x) = g(x), \ \text{target } f(x) = x", font_size=24, color=GREY_A)
                    ).arrange(DOWN, buff=0.06).next_to(axA, UP, buff=0.12)
        vA = label(r"no separation: \ $\sup|g - x| \ge 1$", font_size=22, color=C.PATHOLOGY).next_to(axA, DOWN,
                                                                                                 buff=0.12)
        # panel B: polynomials without constant term on [0, 1] cannot reach 1
        zeros = [lambda x: 1.6 * x - 0.7 * x**2, lambda x: 3 * x - 3 * x**2 + x**3, lambda x: 1 - (1 - x) ** 8,
                 lambda x: 1 - (1 - x) ** 30]
        for g in zeros:
            assert g(0.0) == 0 and np.abs(g(xb) - 1).max() >= 1 - 1e-12
        tgtB = DashedLine(axB.c2p(0, 1), axB.c2p(1, 1), color=WHITE, stroke_width=4, dash_length=0.1).set_z_index(2)
        gB = runs(axB, xb, zeros[0](xb), C.APPROX, 3)
        gapB = Line(axB.c2p(0, 0), axB.c2p(0, 1), color=C.PATHOLOGY, stroke_width=5)
        tB = VGroup(label(r"polynomials with $p(0) = 0$ on $[0, 1]$", font_size=22),
                    MathTex(r"\text{target } f = 1", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.06)
        tB.next_to(axB, UP, buff=0.12)
        vB = label(r"all vanish at $0$: \ $\sup|g - 1| \ge 1$", font_size=22, color=C.PATHOLOGY).next_to(axB, DOWN,
                                                                                                   buff=0.12)
        # panel C: all polynomials (chapter 11's Landau approximant of the tent)
        dl = load("landau")
        tgtC = polyline(axC, dl["x"], tent(dl["x"]), color=WHITE, stroke_width=3.5).set_z_index(2)
        gC = polyline(axC, dl["x"], dl["P"][-1], color=C.APPROX, stroke_width=2.5)
        tC = VGroup(label(r"all polynomials on $[0, 1]$", font_size=22),
                    MathTex(r"\text{target: any continuous } f", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.06)
        tC.next_to(axC, UP, buff=0.12)
        vC = label(rf"both hold: \ dense \ (error ${float(dl['err'][-1]):.4f}$ here)", font_size=22,
                   color=C.CONNECTED_SET).next_to(axC, DOWN, buff=0.12)
        # the algebra at work: two polynomials and their product (members of the algebra), in the panel slots
        xp = np.linspace(0, 1, 401)
        pp, qq = 0.2 + 0.9 * xp, 1.1 - 1.6 * xp + 1.2 * xp**2
        assert np.allclose(pp * qq, np.polyval(np.polymul([0.9, 0.2], [1.2, -1.6, 1.1]), xp))
        alg = VGroup()
        for k_, (yv, tx) in enumerate(((pp, r"p(x) = 0.2 + 0.9x"), (qq, r"q(x) = 1.1 - 1.6x + 1.2x^2"),
                                       (pp * qq, r"p(x)\,q(x)"))):
            a_ = plain_axes([0, 1, 0.5], [0, 1.2, 0.5], W, H).move_to([cx[k_], cy, 0])
            assert 0 <= yv.min() and yv.max() < 1.2
            alg.add(VGroup(a_, polyline(a_, xp, yv, color=C.APPROX, stroke_width=3),
                           MathTex(tx, font_size=26, color=C.APPROX).next_to(a_, UP, buff=0.15)))
        ops = VGroup(MathTex(r"\times", font_size=40, color=GREY_A).move_to([(cx[0] + cx[1]) / 2, cy, 0]),
                     MathTex(r"=", font_size=40, color=GREY_A).move_to([(cx[1] + cx[2]) / 2, cy, 0]))
        alg_note = label(r"also $p + q$ and $c\,p$: \ the algebra never leaves itself", font_size=22, color=GREY_A).next_to(
            alg, DOWN, buff=0.3)
        with self.voiceover(
            "He found that only two properties matter. <bookmark mark='a'/> The setting is an algebra of functions: a "
            "family closed under sums, products and "
            "constant multiples, like the polynomials. <bookmark mark='b'/> Here is the first thing that can go wrong. "
            "The even polynomials on the interval from minus one to one form an algebra, but each one takes the same "
            "value at x and at minus x, so none of them can come near the function x: at plus and minus one, the "
            "error is at least one. The algebra fails to separate points. <bookmark mark='c'/> Second, the "
            "polynomials with no constant term form an algebra, but they all vanish at zero, so none comes near the "
            "constant one. <bookmark mark='d'/> All polynomials have neither defect, and they are dense: that was "
            "chapter eleven."
        ) as vo:
            self.play(FadeIn(defs[0]), FadeIn(alg[0]), FadeIn(alg[1]), run_time=1.2)
            vo.wait_until("a")
            self.play(Indicate(defs[0], color=C.EPS, scale_factor=1.05), FadeIn(ops), FadeIn(alg[2]))
            self.play(FadeIn(alg_note))
            vo.wait_until("b")
            self.play(FadeOut(alg), FadeOut(ops), FadeOut(alg_note), run_time=0.6)
            self.play(FadeIn(defs[1]), Create(axA), FadeIn(tA), Create(tgtA), FadeIn(gA), FadeIn(prA))
            self.play(sA.animate.set_value(3.0), run_time=4.5, rate_func=linear)
            self.play(FadeIn(vA))
            vo.wait_until("c")
            self.play(FadeIn(defs[2]), Create(axB), FadeIn(tB), Create(tgtB), Create(gB), FadeIn(gapB))
            for g in zeros[1:]:
                self.play(Transform(gB, runs(axB, xb, g(xb), C.APPROX, 3)), run_time=0.9)
            self.play(FadeIn(vB))
            vo.wait_until("d")
            self.play(Create(axC), FadeIn(tC), Create(tgtC), Create(gC))
            self.play(FadeIn(vC))
        for m in (gA, prA):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        thm = VGroup(
            label(r"\textbf{Rudin 7.32} \ (Stone, 1937; \ this proof 1948)", font_size=30, color=GREY_A),
            label(r"$K$ compact, \ $\mathcal A$ an algebra of real continuous functions on $K$", font_size=32),
            label(r"that separates points and vanishes at no point", font_size=32),
            MathTex(r"\Longrightarrow \quad \overline{\mathcal A} = C(K) \qquad (\text{the uniform closure})",
                    font_size=40, color=C.EPS),
        ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.45)
        box = SurroundingRectangle(thm, color=C.EPS, buff=0.25, corner_radius=0.1, stroke_width=2)
        ex = VGroup(
            label(r"polynomials in $x_1, \dots, x_k$", font_size=26),
            label(r"\quad on any compact $K \subset \R^k$", font_size=26),
            label(r"sums $\sum_{n=0}^{N} a_n e^{-nx}$ on $[0, 1]$", font_size=26),
            label(r"the even polynomials on $[0, 1]$:", font_size=26, color=C.APPROX),
            label(r"\quad $x^2$ separates points there", font_size=26, color=C.APPROX),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([-3.9, -1.75, 0])
        ex_h = label(r"so, for example, these are dense:", font_size=26, color=GREY_A).next_to(ex, UP, buff=0.22)
        ex_h.align_to(ex, LEFT)
        d = load("stone")
        xe, ek, EV, eerr = d["xe"], d["ek"], d["EV"], d["eerr"]
        eax = plain_axes([0, 1, 0.5], [0, 1.05, 0.5], 4.4, 2.6).move_to([1.0, -1.85, 0])
        tgt = polyline(eax, xe, xe, color=WHITE, stroke_width=3)
        fits = [polyline(eax, xe, EV[i], color=C.APPROX, stroke_width=3) for i in range(len(ek))]
        etl = MathTex(r"\text{target } f(x) = x", font_size=24).next_to(eax, UP, buff=0.08)
        elabs = [MathTex(rf"\text{{degree }} {2 * int(k)} \text{{ in }} x: \ \sup|g - x| = {e:.4f}", font_size=24,
                         color=C.APPROX).next_to(eax, DOWN, buff=0.12) for k, e in zip(ek, eerr)]
        enote = VGroup(label(r"the algebra that failed", font_size=22, color=GREY_A),
                       label(r"on $[-1, 1]$ succeeds here", font_size=22, color=GREY_A)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(eax, RIGHT, buff=0.25)
        xi = np.linspace(0, 1, 801)
        fi_ = 0.55 + 0.25 * np.sin(7 * xi) + 0.3 * np.abs(xi - 0.62)
        ci = np.polynomial.chebyshev.chebfit(2 * xi - 1, fi_, 40)
        gi = np.polynomial.chebyshev.chebval(2 * xi - 1, ci)
        eps_i = 0.06
        assert np.abs(gi - fi_).max() < eps_i / 2
        iax = plain_axes([0, 1, 0.5], [0, 1.1, 0.5], 6.4, 2.4).move_to([0, -2.1, 0])
        band_i = Polygon(*[iax.c2p(a_, b_) for a_, b_ in zip(xi[::8], fi_[::8] + eps_i)],
                         *[iax.c2p(a_, b_) for a_, b_ in zip(xi[::-8], fi_[::-8] - eps_i)], stroke_width=0,
                         fill_color=C.EPS, fill_opacity=0.22)
        illus = VGroup(iax, band_i, polyline(iax, xi, gi, color=C.APPROX, stroke_width=2.5),
                       polyline(iax, xi, fi_, color=WHITE, stroke_width=3).set_z_index(2))
        illus_l = VGroup(MathTex(r"f \in C(K)", font_size=26), MathTex(r"f \pm \varepsilon", font_size=26, color=C.EPS),
                         MathTex(r"g \in \mathcal A", font_size=26, color=C.APPROX)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.12)
        illus_l.next_to(iax, RIGHT, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> Stone's theorem says these two defects are the only obstructions. If an algebra of "
            "continuous functions on a compact set separates points and vanishes at no point, then its uniform closure "
            "is everything: every continuous function is a uniform limit of members of the algebra. "
            "<bookmark mark='b'/> So polynomials in several variables are dense on any compact set in R k, and so are "
            "sums of decaying exponentials on the unit interval. And the even polynomials, which failed on the "
            "symmetric interval, are dense on the interval from zero to one, where x squared separates points: here "
            "they close in on the function x, the very function they could not reach before."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm[:3]), Create(box))
            self.play(Write(thm[3]), Create(iax), FadeIn(illus[3]), FadeIn(illus_l[0]))
            self.play(FadeIn(band_i), FadeIn(illus_l[1]))
            self.play(Create(illus[2]), FadeIn(illus_l[2]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeOut(illus), FadeOut(illus_l), run_time=0.6)
            self.play(FadeIn(ex_h), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in ex[:3]], lag_ratio=0.4),
                      run_time=2)
            self.play(FadeIn(ex[3:]), Create(eax), Create(tgt), FadeIn(etl), Create(fits[0]), FadeIn(elabs[0]))
            cur, cl = fits[0], elabs[0]
            for i in range(1, len(ek)):
                self.play(ReplacementTransform(cur, fits[i]), FadeTransform(cl, elabs[i]), run_time=0.9)
                cur, cl = fits[i], elabs[i]
            self.play(FadeIn(enote))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof_map(self):
        pm = ProofMap([r"$f \in \mathcal B \Rightarrow |f| \in \mathcal B$", r"$\max(f, g)$, $\min(f, g) \in \mathcal B$",
                       r"interpolate at two points", r"caps: max, then min"], font_size=22, width=3.05, buff=0.3)
        pm.to_edge(UP, buff=0.2)
        return pm

    def step_abs(self):
        d = load("stone")
        pm = self.proof_map()
        y, absdeg, absP, abserr = d["y"], d["absdeg"], d["absP"], d["abserr"]
        t, f1, Pf1 = d["t"], d["f1"], d["Pf1"]
        axL = plain_axes([-1, 1, 0.5], [0, 1.1, 0.5], 5.2, 3.0).move_to([-3.7, 0.2, 0])
        axR = plain_axes([0, 1, 0.25], [-1, 1, 0.5], 5.2, 3.0).move_to([3.3, 0.2, 0])
        absg = polyline(axL, y, np.abs(y), color=WHITE, stroke_width=3)
        Pl = [polyline(axL, y, absP[i], color=C.APPROX, stroke_width=3) for i in range(len(absdeg))]
        f1g = polyline(axR, t, f1, color=C.FUNC, stroke_width=2.5)
        af1 = polyline(axR, t, np.abs(f1), color=WHITE, stroke_width=3)
        Pr = [polyline(axR, t, Pf1[i], color=C.APPROX, stroke_width=3) for i in range(len(absdeg))]
        tl = MathTex(r"P_n(y) \to |y| \text{ on } [-a, a]", font_size=28, color=C.APPROX).next_to(axL, UP, buff=0.12)
        tr = MathTex(r"f", r",\ |f|", r",\ P_n(f)", font_size=28).next_to(axR, UP, buff=0.12)
        tr[0].set_color(C.FUNC)
        tr[2].set_color(C.APPROX)
        errs = [MathTex(rf"\deg P_n = {int(n)}: \quad \sup|P_n(y) - |y|| = {e:.3f}", font_size=26, color=C.APPROX)
                .next_to(axL, DOWN, buff=0.2) for n, e in zip(absdeg, abserr)]
        why_ = VGroup(MathTex(r"P_n(f) = \sum_k c_k f^k \in \mathcal B", font_size=30),
                      MathTex(r"\sup_K |P_n(f) - |f|| \le \sup_{[-a, a]} |P_n(y) - |y||", font_size=30, color=C.EPS)
                      ).arrange(DOWN, buff=0.12).next_to(axR, DOWN, buff=0.2)
        foot = label(r"(Bernstein's polynomials here; \ subtract $P_n(0)$ so that no constant is needed)", font_size=20,
                     color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The proof has four steps. Let B be the uniform closure of the algebra; B is itself an algebra, and we "
            "want to show it contains every continuous function. <bookmark mark='a'/> Step one: if f is in B, so is "
            "its absolute value. f is bounded, say by a, and by Weierstrass's theorem there are polynomials P n "
            "converging to the absolute value of y uniformly on the interval from minus a to a. <bookmark mark='b'/> "
            "Plug f into them. P n of f is built from f by sums, products and constants, so it lies in B, and it is "
            "within the same distance of the absolute value of f. <bookmark mark='c'/> As the degree grows, P n of f "
            "converges uniformly to the absolute value of f, and B is closed, so the absolute value is in B."
        ) as vo:
            self.play(FadeIn(pm), Create(axL), Create(absg))
            vo.wait_until("a")
            self.play(*pm.light(0))
            self.play(FadeIn(tl), Create(Pl[0]), FadeIn(errs[0]))
            vo.wait_until("b")
            self.play(Create(axR), FadeIn(tr), Create(f1g), Create(af1), TransformFromCopy(Pl[0], Pr[0]),
                      FadeIn(why_[0]))
            self.play(FadeIn(why_[1]))
            vo.wait_until("c")
            cl, cr, ce = Pl[0], Pr[0], errs[0]
            for i in range(1, len(absdeg)):
                self.play(ReplacementTransform(cl, Pl[i]), ReplacementTransform(cr, Pr[i]),
                          FadeTransform(ce, errs[i]), run_time=1.3)
                cl, cr, ce = Pl[i], Pr[i], errs[i]
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def step_lattice(self):
        pm = self.proof_map()
        self._set_state(pm, 1)
        t = np.linspace(0, 1, 801)
        ax = plain_axes([0, 1, 0.25], [0, 1.6, 0.5], 6.0, 2.6).move_to([-3.4, 0.5, 0])
        g1 = 0.35 + 0.9 * t
        g2 = 1.1 - 2.6 * (t - 0.45) ** 2 + 0.3 * np.sin(9 * t)
        G1 = polyline(ax, t, g1, color=C.SEQ, stroke_width=2.5)
        G2 = polyline(ax, t, g2, color=C.APPROX, stroke_width=2.5)
        mx = polyline(ax, t, np.maximum(g1, g2), color=C.EPS, stroke_width=10).set_stroke(opacity=0.4).set_z_index(-1)
        mn = polyline(ax, t, np.minimum(g1, g2), color=C.CONNECTED_SET, stroke_width=10).set_stroke(opacity=0.4)
        mn.set_z_index(-1)
        assert np.allclose(np.maximum(g1, g2), (g1 + g2) / 2 + np.abs(g1 - g2) / 2)
        lab = MathTex(r"f", r",\ g", font_size=30).next_to(ax, UP, buff=0.12)
        lab[0].set_color(C.SEQ)
        lab[1].set_color(C.APPROX)
        fm = VGroup(MathTex(r"\max(f, g) = \frac{f + g}{2} + \frac{|f - g|}{2}", font_size=34, color=C.EPS),
                    MathTex(r"\min(f, g) = \frac{f + g}{2} - \frac{|f - g|}{2}", font_size=34, color=C.CONNECTED_SET),
                    label(r"so $\mathcal B$ is closed under max and min \ (a lattice);", font_size=26),
                    label(r"by induction, under the max of finitely many", font_size=26, color=GREY_A),
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, 0.3, 0])
        # step 3 on the same screen, below: two-point interpolation
        ax2 = plain_axes([0, 1, 0.25], [-0.5, 1.5, 0.5], 6.0, 1.9).move_to([-3.4, -2.35, 0])
        assert ax2.get_top()[1] < ax.get_bottom()[1] - 0.3
        xp, yp = 0.25, 0.75
        cT, dT = ValueTracker(0.4), ValueTracker(1.1)

        def interp():
            c, d_ = cT.get_value(), dT.get_value()
            g = c * (t - yp) / (xp - yp) + d_ * (t - xp) / (yp - xp)
            return VGroup(runs(ax2, t, g, C.EPS, 3.5), Dot(ax2.c2p(xp, c), radius=0.07, color=WHITE),
                          Dot(ax2.c2p(yp, d_), radius=0.07, color=WHITE))

        ig = always_redraw(interp)
        uv = VGroup(runs(ax2, t, t - xp, C.SEQ, 2), runs(ax2, t, t - yp, C.APPROX, 2))
        fi = VGroup(label(r"\textbf{7.31} \ separates points + vanishes nowhere $\Rightarrow$", font_size=26),
                    label(r"for $x \ne y$ and any $c, d$: \ some $g \in \mathcal A$ has $g(x) = c$, $g(y) = d$",
                          font_size=26, color=C.EPS),
                    MathTex(r"\text{polynomials: } g = c\,\frac{t - y}{x - y} + d\,\frac{t - x}{y - x}", font_size=28,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.4, -2.55, 0])
        for r_ in fi:
            if r_.width > 6.6:
                r_.width = 6.6
        fi.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.4, -2.55, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Step two. The larger of two functions is their average plus half their difference "
            "in absolute value, and the smaller is the average minus it. <bookmark mark='b'/> So by step one, B is "
            "closed under taking the maximum or the minimum of two functions, and by induction, of finitely many. "
            "<bookmark mark='c'/> Step three uses the two hypotheses. Because the algebra separates points and "
            "vanishes nowhere, it can match any two values at any two points. For polynomials that's just the line "
            "through two points, a combination of one function vanishing at x and one vanishing at y."
        ) as vo:
            self.add(pm)
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(lab), Create(G1), Create(G2))
            self.play(FadeIn(fm[0]), Create(mx))
            self.play(FadeIn(fm[1]), Create(mn))
            vo.wait_until("b")
            self.play(FadeIn(fm[2:]))
            vo.wait_until("c")
            self.play(*pm.light(2))
            self.play(Create(ax2), FadeIn(fi[0]), Create(uv))
            self.play(FadeIn(ig), FadeIn(fi[1:]))
            self.play(cT.animate.set_value(1.2), dT.animate.set_value(0.0), run_time=2.0)
            self.play(cT.animate.set_value(0.2), dT.animate.set_value(1.3), run_time=2.0)
        ig.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def _set_state(self, pm, i):
        """Put the proof map in the state 'step i current' without animating."""
        for j, b in enumerate(pm.boxes):
            if j < i:
                b[0].set_stroke(C.CONNECTED_SET, 2).set_fill(C.CONNECTED_SET, 0.10)
                b[1].set_opacity(0.8)
            elif j == i:
                b[0].set_stroke(C.EPS, 3).set_fill(C.EPS, 0.16)
                b[1].set_opacity(1.0)
        for j, a in enumerate(pm.arrows):
            if j < i:
                a.set_color(C.CONNECTED_SET)

    # ------------------------------------------------------------------
    def caps_axes(self):
        ax = plain_axes([0, 1, 0.25], [0.8, 3.0, 0.5], 7.0, 3.6).move_to([-2.7, 0.35, 0])
        return ax

    def caps_one(self):
        d = load("stone")
        t, f, eps, xs, ys = d["t"], d["f"], float(d["eps"]), d["xs"], d["ys"]
        pm = self.proof_map()
        self._set_state(pm, 3)
        ax = self.caps_axes()
        fg = polyline(ax, t, f, color=WHITE, stroke_width=3.5)
        band = VGroup(polyline(ax, t, f - eps, color=C.EPS, stroke_width=1.5),
                      polyline(ax, t, f + eps, color=C.EPS, stroke_width=1.5))
        x = float(xs[7])
        lines = [runs(ax, t, secant(t, x, float(y)), C.APPROX, 1.6) for y in ys]
        Gs = np.array([secant(t, x, float(y)) for y in ys])
        hx = Gs.max(axis=0)
        assert abs(np.interp(x, t, hx) - math.exp(x)) < 1e-9 and np.all(hx > f - eps)
        hxg = runs(ax, t, hx, C.CLOSED_SET, 5)
        xdot = Dot(ax.c2p(x, math.exp(x)), radius=0.08, color=C.CLOSED_SET)
        ydots = VGroup(*[Dot(ax.c2p(float(y), math.exp(float(y))), radius=0.05, color=C.APPROX) for y in ys])
        # the open sets U_y = {g_xy > f - eps}, as bars under the axes
        y_top = ax.get_bottom()[1] - 0.3
        bars = VGroup(*[interval_bars(ax, t, G > f - eps, y_top - 0.13 * j, C.APPROX, height=0.08) for j, G in
                        enumerate(Gs)])
        cover = np.any(Gs > f - eps, axis=0)
        assert cover.all()
        bl = label(r"where $g_{xy} > f - \varepsilon$:", font_size=20, color=C.APPROX).next_to(bars, DOWN, buff=0.08)
        bl.align_to(bars, LEFT)  # under the bars: left of them is off-screen
        flab = MathTex(r"f(x) = e^x", font_size=28).next_to(ax.c2p(0.95, math.exp(0.95)), UL, buff=0.1)
        side = VGroup(
            label(rf"fix $x = {x:.2f}$; \ for each $y$, \ step 3 gives", font_size=24),
            MathTex(r"g_{xy} \in \mathcal A: \ g_{xy}(x) = f(x), \ g_{xy}(y) = f(y)", font_size=28, color=C.APPROX),
            label(r"$g_{xy} > f - \varepsilon$ on an open set around $y$", font_size=24),
            label(r"compactness: \ finitely many $y$ cover \ (here $9$)", font_size=24, color=C.COMPACT_SET),
            MathTex(r"h_x = \max_y g_{xy} \in \mathcal B", font_size=32, color=C.CLOSED_SET),
            MathTex(r"h_x(x) = f(x), \qquad h_x > f - \varepsilon", font_size=30, color=C.CLOSED_SET),
        )
        for r_ in side:
            if r_.width > 5.6:
                r_.width = 5.6
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -0.2, 0])
        epsl = MathTex(r"f \pm \varepsilon, \ \varepsilon = 0.1", font_size=24, color=C.EPS).next_to(ax, UP, buff=0.08)
        epsl.align_to(ax, LEFT).shift(RIGHT * 0.6)
        with self.voiceover(
            "<bookmark mark='a'/> Step four builds the approximation, here for e to the x on the interval from zero to "
            "one, with epsilon equal to a tenth, using the polynomial algebra. <bookmark mark='b'/> Fix a point x. For "
            "each other point y, step three gives a member of the algebra that agrees with f at both x and y: here, "
            "the line through the two points of the graph. <bookmark mark='c'/> Each such line exceeds f minus "
            "epsilon on an open set around y. These open sets cover the interval, so by compactness finitely many "
            "of them do: here, nine. <bookmark mark='d'/> Take the largest of those nine lines. It's in B by step two; "
            "it agrees with f at x; and it never drops below f minus epsilon. Call it the cap at x."
        ) as vo:
            self.add(pm)
            vo.wait_until("a")
            self.play(Create(ax), Create(fg), FadeIn(flab), FadeIn(band), FadeIn(epsl))
            vo.wait_until("b")
            self.play(FadeIn(xdot), FadeIn(side[0]), FadeIn(side[1]))
            self.play(LaggedStart(*[AnimationGroup(Create(l_), FadeIn(dd)) for l_, dd in zip(lines, ydots)],
                                  lag_ratio=0.25), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(bl), LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.1) for b_ in bars],
                                                                lag_ratio=0.15), run_time=2.0)
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(Create(hxg), *[l_.animate.set_stroke(opacity=0.25) for l_ in lines], FadeIn(side[4]))
            self.play(FadeIn(side[5]), Flash(xdot, color=C.CLOSED_SET))
        self.wait(0.3)
        self.clear_scene()

    def caps_all(self):
        d = load("stone")
        t, f, eps, xs, H, approx, err = d["t"], d["f"], float(d["eps"]), d["xs"], d["H"], d["approx"], float(d["err"])
        pm = self.proof_map()
        self._set_state(pm, 3)
        ax = self.caps_axes()
        fg = polyline(ax, t, f, color=WHITE, stroke_width=3.5)
        band = VGroup(polyline(ax, t, f - eps, color=C.EPS, stroke_width=1.5),
                      polyline(ax, t, f + eps, color=C.EPS, stroke_width=1.5))
        caps = VGroup(*[runs(ax, t, h, C.CLOSED_SET, 1.8) for h in H])
        hg = polyline(ax, t, approx, color=C.APPROX, stroke_width=5)
        y_top = ax.get_bottom()[1] - 0.3
        Wsets = [h < f + eps for h in H]
        assert np.any(Wsets, axis=0).all()
        bars = VGroup(*[interval_bars(ax, t, w, y_top - 0.075 * j, C.CLOSED_SET, height=0.05) for j, w in
                        enumerate(Wsets)])
        bl = label(r"where $h_x < f + \varepsilon$:", font_size=20, color=C.CLOSED_SET).next_to(bars, DOWN, buff=0.08)
        bl.align_to(bars, LEFT)  # under the bars: left of them is off-screen
        dots = VGroup(*[Dot(ax.c2p(float(x), math.exp(float(x))), radius=0.04, color=C.CLOSED_SET) for x in xs])
        side = VGroup(
            label(r"a cap $h_x$ at each $x$", font_size=24, color=C.CLOSED_SET),
            label(r"$h_x < f + \varepsilon$ on an open set around $x$", font_size=24),
            label(rf"compactness again: \ finitely many $x$ \ (here ${len(xs)}$)", font_size=24, color=C.COMPACT_SET),
            MathTex(r"h = \min_x h_x \in \mathcal B", font_size=32, color=C.APPROX),
            MathTex(r"f - \varepsilon < h < f + \varepsilon", font_size=32, color=C.EPS),
            label(rf"computed: \ $\sup|h - f| = {err:.4f} < \varepsilon$", font_size=24, color=GREY_A),
        )
        for r_ in side:
            if r_.width > 5.6:
                r_.width = 5.6
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -0.2, 0])
        concl = label(r"$\varepsilon$ was arbitrary and $\mathcal B$ is closed: \ $f \in \mathcal B$", font_size=26,
                      color=C.EPS).to_edge(DOWN, buff=0.35)
        assert err < eps
        with self.voiceover(
            "<bookmark mark='a'/> Now build a cap at every point. <bookmark mark='b'/> Each cap is below f plus "
            "epsilon on an open set around its own point, because it agrees with f there. Compactness again: finitely "
            "many of these sets cover, here twenty one. <bookmark mark='c'/> Take the smallest of those caps. It is "
            "still above f minus epsilon, since every cap is, and now it's below f plus epsilon everywhere too. "
            "Computed, the minimum is within two hundredths of e to the x. <bookmark mark='d'/> Epsilon was arbitrary "
            "and B is closed, so f is in B. Separating points and vanishing nowhere were used only in step three, "
            "to make the lines exist."
        ) as vo:
            self.add(pm)
            self.play(Create(ax), Create(fg), FadeIn(band))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(Create(c_), FadeIn(dd)) for c_, dd in zip(caps, dots)],
                                  lag_ratio=0.12), FadeIn(side[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(bl), LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.08),
                      run_time=2.0)
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(hg), caps.animate.set_stroke(opacity=0.3), FadeIn(side[3]))
            self.play(FadeIn(side[4]), FadeIn(side[5]))
            vo.wait_until("d")
            self.play(*pm.done(), FadeIn(concl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def complex_case(self):
        d = load("stone")
        th, W = d["th"], d["W"]
        head = VGroup(label(r"Complex functions: \ separating points is not enough \ (Rudin, Exercise 7.21)", font_size=30),
                      label(r"polynomials $P(z)$ on the unit circle $|z| = 1$; \ target $f(z) = \bar z$", font_size=26,
                            color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        # left: z and conj(z) running around the circle in opposite directions
        o = np.array([-4.8, -0.4, 0])
        R = 1.45
        circ = Circle(radius=R, color=GREY_C, stroke_width=2).move_to(o)
        axl = VGroup(Line(o + LEFT * (R + 0.3), o + RIGHT * (R + 0.3), color=GREY_D, stroke_width=1.5),
                     Line(o + DOWN * (R + 0.3), o + UP * (R + 0.3), color=GREY_D, stroke_width=1.5))
        aT = ValueTracker(0.4)
        zd = always_redraw(lambda: Dot(o + R * np.array([np.cos(aT.get_value()), np.sin(aT.get_value()), 0]),
                                       radius=0.08, color=C.FUNC))
        zbd = always_redraw(lambda: Dot(o + R * np.array([np.cos(aT.get_value()), -np.sin(aT.get_value()), 0]),
                                        radius=0.08, color=C.PATHOLOGY))
        zl = always_redraw(lambda: MathTex(r"z", font_size=28, color=C.FUNC).move_to(
            o + (R + 0.35) * np.array([np.cos(aT.get_value()), np.sin(aT.get_value()), 0])))
        zbl = always_redraw(lambda: MathTex(r"\bar z", font_size=28, color=C.PATHOLOGY).move_to(
            o + (R + 0.35) * np.array([np.cos(aT.get_value()), -np.sin(aT.get_value()), 0])))
        # middle: the curve 1 - z P(z), whose average is exactly 1
        po = np.array([0.2, -0.4, 0])
        u = 1.15

        def P2S(w):
            return np.c_[po[0] + u * w.real, po[1] + u * w.imag, np.zeros(len(w))]

        plane = VGroup(Line(P2S(np.array([-1.2]))[0], P2S(np.array([2.3]))[0], color=GREY_D, stroke_width=1.5),
                       Line(P2S(np.array([-1.3j]))[0], P2S(np.array([1.3j]))[0], color=GREY_D, stroke_width=1.5))
        disk = DashedVMobject(Circle(radius=u, color=GREY_A, stroke_width=2).move_to(po), num_dashes=40)
        disk_l = MathTex(r"|w| = 1", font_size=22, color=GREY_A).next_to(disk, DL, buff=-0.25)
        one = Dot(P2S(np.array([1.0 + 0j]))[0], radius=0.07, color=C.EPS)
        assert all(w_.imag.min() > -1.3 for w_ in W)  # the label below stays clear of every loop
        one_t = MathTex(r"\text{mean} = 1", font_size=24, color=C.EPS).move_to(P2S(np.array([1.75 - 1.55j]))[0])
        one_l = VGroup(one_t, Line(one_t.get_corner(UL) + 0.05 * UP, one.get_center(), color=C.EPS, stroke_width=1.5,
                                   buff=0.09))
        curves = [VMobject(color=C.APPROX, stroke_width=3).set_points_as_corners(P2S(w)) for w in W]
        far = []
        for w in W:
            k = int(np.argmax(np.abs(w)))
            far.append(VGroup(Line(po, P2S(w[k:k + 1])[0], color=C.PATHOLOGY, stroke_width=3),
                              Dot(P2S(w[k:k + 1])[0], radius=0.06, color=C.PATHOLOGY)))
        cl = MathTex(r"w(\theta) = 1 - zP(z), \ z = e^{i\theta}", font_size=26, color=C.APPROX).next_to(plane, UP,
                                                                                                  buff=0.1)
        rows = VGroup(
            MathTex(r"\int_0^{2\pi} P(e^{i\theta})\,e^{i\theta}\,d\theta = 0", font_size=30),
            label(r"(every term $e^{i(k+1)\theta}$ integrates to $0$)", font_size=20, color=GREY_B),
            MathTex(r"\int_0^{2\pi} \bar z\, z\,d\theta = 2\pi", font_size=30, color=C.PATHOLOGY),
            MathTex(r"|\bar z - P(z)| = |1 - zP(z)|", font_size=30),
            label(r"$1 - zP$ has mean $1$: \ $\max |1 - zP| \ge 1$", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([5.0, -0.3, 0])
        for r_ in rows:
            if r_.width > 3.6:
                r_.width = 3.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.8, -0.3, 0])
        assert rows.get_left()[0] > 2.9 and rows.get_right()[0] < 6.95
        fix = label(r"add $\bar z$ (a \textbf{self-adjoint} algebra): \ the trigonometric polynomials "
                    r"$\sum c_n e^{in\theta}$ are dense in $C(\mathbb T)$", font_size=26, color=C.CONNECTED_SET)
        fix.to_edge(DOWN, buff=0.35)
        for w in W:
            assert np.abs(w).max() >= 1
        with self.voiceover(
            "<bookmark mark='a'/> For complex-valued functions there's a catch. On the unit circle, the polynomials "
            "in z separate points and contain the constants, yet they can't approximate z bar, the complex conjugate, "
            "which runs around the circle the other way. <bookmark mark='b'/> Here's why. Every polynomial times z has "
            "average zero around the circle, because each power of e to the i theta integrates to zero. But z bar "
            "times z is one. <bookmark mark='c'/> So the distance from z bar to P of z is the size of one minus z P of z, "
            "and one minus z P of z averages to exactly one: the curve it traces is centered at one, so it can never "
            "stay inside the unit disk. <bookmark mark='d'/> Whatever polynomial we try, somewhere the error "
            "is at least one. <bookmark mark='e'/> The fix, Rudin 7.33, is to require the algebra to contain the "
            "conjugate of each of its members. Adding z bar gives the trigonometric polynomials, and those are dense: "
            "the key to Fourier series, three chapters from now."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(axl), Create(circ), FadeIn(zd), FadeIn(zbd), FadeIn(zl), FadeIn(zbl))
            self.play(aT.animate.set_value(0.4 + 2 * np.pi), run_time=3.5, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]), Create(plane), Create(disk), FadeIn(disk_l), FadeIn(one), FadeIn(one_l),
                      FadeIn(cl))
            self.play(Create(curves[0]), run_time=1.5)
            self.play(FadeIn(far[0]), FadeIn(rows[4]))
            vo.wait_until("d")
            cur, cf = curves[0], far[0]
            for k in range(1, len(W)):
                self.play(ReplacementTransform(cur, curves[k]), ReplacementTransform(cf, far[k]),
                          aT.animate.increment_value(np.pi), run_time=1.3, rate_func=linear)
                cur, cf = curves[k], far[k]
            vo.wait_until("e")
            self.play(FadeIn(fix))
        for m in (zd, zbd, zl, zbl):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
