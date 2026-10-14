from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import boxes_overlap, fixed_runs, load, logn_axes, plain_axes, polyline
from videos.analysis8.compute import lebesgue_constant


class UniformBoundedness(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.fourier()
        self.not_onto()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"Uniform boundedness", r"If every orbit is bounded, is the family bounded?", lit=(1932,),
                            part=8)
        with self.voiceover("Chapter four: the uniform boundedness principle of Banach and Steinhaus."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def theorem(self):
        head = label(r"Pointwise bounds become uniform bounds", font_size=34).to_edge(UP, buff=0.3)
        thm = VGroup(
            label(r"\textbf{RCA 5.8} \ (Banach--Steinhaus) \ $X$ Banach, \ $\{\Lambda_\alpha\}$ bounded linear maps $X \to Y$:",
                  font_size=26),
            label(r"either \ $\sup_\alpha \|\Lambda_\alpha\| < \infty$, \ or \ $\sup_\alpha \|\Lambda_\alpha x\| = \infty$ "
                  r"for all $x$ in a dense $G_\delta$", font_size=26, color=C.EPS),
        ).arrange(DOWN, buff=0.12).next_to(head, DOWN, buff=0.25)
        # the family this part is about: the Fourier partial sums S_n on C(T), whose norms (the Lebesgue constants)
        # are unbounded, so Banach-Steinhaus puts us in its second case. Drawn like the hook's plot: log n across
        d = load("lebesgue")
        ns, L, asym = d["ns"], d["L"], d["asym"]
        assert np.allclose(L, [lebesgue_constant(int(n)) for n in ns])
        assert np.all(np.abs(L[2:] - asym[2:]) / L[2:] < 0.01)  # n >= 10: within 1% of (4/pi^2) log n + 1.27
        lax, ldec = logn_axes(9.0, 2.8, center=[0.3, -1.25, 0])
        lg = np.log10(ns)
        ldots = VGroup(*[Dot(lax.c2p(a, b), radius=0.06, color=C.OPERATOR) for a, b in zip(lg, L)])
        uu = np.linspace(0.5, 6, 100)
        lfit = polyline(lax, uu, 4 / math.pi**2 * np.log(10**uu) + 1.2703, color=WHITE, stroke_width=1.5)
        llab = MathTex(r"\|S_n\| \text{ on } C(\mathbb T) = \|D_n\|_1 \ \approx \tfrac{4}{\pi^2}\log n + 1.27 \to \infty",
                       font_size=26, color=C.OPERATOR).next_to(lax, UP, buff=0.15).align_to(lax, LEFT).shift(RIGHT * 0.3)
        lpic = VGroup(lax, ldec, ldots, lfit, llab)
        # the Baire picture: X a square, the closed sets E_1 c E_2 c ... c E_5 as nested blobs, all inside X
        side, c0 = 5.0, np.array([-3.6, -0.75, 0])
        sq = Square(side_length=side, color=GREY_C, stroke_width=1.5).move_to(c0)
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.EPS), k / 4) for k in range(5)]
        th = np.linspace(0, 2 * np.pi, 721)

        def R(k, t):  # the outline of E_{k+1} in polar coordinates about c0
            return (0.36 + 0.42 * k) * (1 + 0.10 * np.sin(5 * t + 0.3 * k) + 0.06 * np.cos(3 * t - 0.3 * k))

        outl = [np.c_[R(k, th) * np.cos(th), R(k, th) * np.sin(th)] for k in range(5)]
        assert all(np.abs(o).max() < side / 2 - 0.1 for o in outl)  # every E_k lies inside X
        assert all(np.all(R(k + 1, th) > R(k, th) + 0.25) for k in range(4))  # nested, with room between outlines
        blobs = VGroup(*[Polygon(*[c0 + [a, b, 0] for a, b in o[:-1]], stroke_color=cols[k], stroke_width=2.5,
                                 fill_color=cols[k], fill_opacity=0.08) for k, o in enumerate(outl)])
        allp = np.vstack([c0[:2] + o for o in outl] + [c0[:2] + np.c_[np.linspace(-1, 1, 200), np.full(200, s_)] * side / 2
                                                        for s_ in (-1, 1)])

        def clear(m, pad=0.05):  # no outline passes through the label's box
            l_, r_, b_, t_ = m.get_left()[0] - pad, m.get_right()[0] + pad, m.get_bottom()[1] - pad, m.get_top()[1] + pad
            return not np.any((allp[:, 0] > l_) & (allp[:, 0] < r_) & (allp[:, 1] > b_) & (allp[:, 1] < t_))

        # each E_k is labelled in the band just outside its own outline, in the upper left (the ball goes lower right)
        e_l = VGroup()
        for k in range(5):
            m = MathTex(rf"E_{{{k + 1}}}", font_size=22, color=cols[k])

            def at(t):
                outer = R(k + 1, t) if k < 4 else R(k, t) + 0.45
                return (R(k, t) + outer) / 2 * np.array([math.cos(t), math.sin(t), 0]), outer - R(k, t)

            best = None
            for sector in ((0.5 * np.pi, np.pi), (-np.pi, np.pi)):  # the upper left first, where the ball is not
                for t in np.linspace(*sector, 201):
                    pos, gap = at(t)
                    m.move_to(c0 + pos)
                    if clear(m) and all(not boxes_overlap(m, o_, 0.05) for o_ in e_l) and (best is None or gap > best[0]):
                        best = (gap, t)
                if best is not None:
                    break
            assert best is not None, k
            e_l.add(m.move_to(c0 + at(best[1])[0]))
        # the ball Baire finds: inside E_4 (it may cut E_3: the sets are nested)
        bc, br = c0 + np.array([0.94, -0.34, 0]), 0.3
        bpts = np.c_[np.cos(th), np.sin(th)] * br + (bc - c0)[:2]
        assert np.all(np.hypot(bpts[:, 0], bpts[:, 1]) < R(3, np.arctan2(bpts[:, 1], bpts[:, 0])) - 0.03)
        ball = Circle(radius=br, color=WHITE, stroke_width=3).move_to(bc)
        assert all(not boxes_overlap(ball, m, 0.05) for m in e_l)
        sch = note(r"schematic").next_to(sq, DOWN, buff=0.08)
        steps = VGroup(
            MathTex(r"E_k = \{x : \sup_\alpha \|\Lambda_\alpha x\| \le k\}", font_size=30),
            label(r"closed \ (an intersection of closed sets)", font_size=22, color=GREY_A),
            label(r"if every orbit is bounded, \ $X = \bigcup_k E_k$", font_size=24),
            label(r"Baire: \ some $E_k$ contains a ball $B(x_0, r)$", font_size=24, color=C.EPS),
            MathTex(r"\|x\| < r \Rightarrow \|\Lambda_\alpha x\| \le \|\Lambda_\alpha(x_0 + x)\| + \|\Lambda_\alpha x_0\| "
                    r"\le 2k", font_size=26),
            label(r"so $\|\Lambda_\alpha\| \le 2k/r$ for every $\alpha$: \ uniform", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        for r_ in steps:
            if r_.width > 6.4:
                r_.width = 6.4
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.2, -0.75, 0])
        assert steps.get_right()[0] < 6.6 and steps.get_left()[0] > sq.get_right()[0] + 0.3
        with self.voiceover(
            "<bookmark mark='a'/> Banach and Steinhaus: for a family of bounded operators on a Banach space, either "
            "their norms are bounded, or they blow up on a dense G delta. <bookmark mark='b'/> The proof is Baire. "
            "Let E k be the set of points whose orbit stays within k: a closed set. <bookmark mark='c'/> If every "
            "orbit is bounded, the E k cover the whole space, and Baire says one of them must contain a ball. "
            "<bookmark mark='d'/> A ball's worth of uniform bounds, shifted to the origin by linearity, bounds every "
            "operator's norm by the same constant. Pointwise bounds become uniform bounds."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(thm), Create(lax), FadeIn(ldec), Create(lfit), FadeIn(llab))
            self.play(LaggedStart(*[FadeIn(p_, scale=0.5) for p_ in ldots], lag_ratio=0.12), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(lpic), run_time=0.5)
            self.play(Create(sq), FadeIn(sch), FadeIn(steps[:2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(b_) for b_ in blobs], lag_ratio=0.25), FadeIn(e_l), FadeIn(steps[2]),
                      run_time=2.5)
            self.play(Create(ball), FadeIn(steps[3]))
            vo.wait_until("d")
            self.play(FadeIn(steps[4:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fourier(self):
        d = load("lebesgue")
        L, ns = d["L"], d["ns"]
        n = 10
        x = np.linspace(-math.pi, math.pi, 4001)
        with np.errstate(invalid="ignore", divide="ignore"):
            D = np.sin((n + 0.5) * x) / np.sin(x / 2)
        D[np.isclose(x, 0)] = 2 * n + 1
        f = np.tanh(D / 0.05)
        ax = plain_axes([-math.pi, math.pi, math.pi / 2], [-6, 22, 5], 6.2, 3.0).move_to([-3.2, 0.6, 0])
        gD = polyline(ax, x, D, color=C.SEQ, stroke_width=2.5)
        bx = plain_axes([-math.pi, math.pi, math.pi / 2], [-1.3, 1.3, 1], 6.2, 1.6).move_to([-3.2, -2.1, 0])
        gf = polyline(bx, x, f, color=C.EPS, stroke_width=2.5)
        l1 = MathTex(r"D_{10}", font_size=26, color=C.SEQ).next_to(ax, UP, buff=0.05)
        l2 = MathTex(r"f_{10} \approx \operatorname{sign} D_{10}, \ \text{continuous}, \ |f_{10}| \le 1", font_size=24,
                     color=C.EPS).next_to(bx, UP, buff=0.05)
        rows = VGroup(
            label(r"\textbf{RCA 5.11} \ on $X = C(T)$:", font_size=26),
            MathTex(r"\Lambda_n f = s_n(f)(0), \quad \|\Lambda_n\| = \|D_n\|_1", font_size=30),
            MathTex(rf"\|D_{{10}}\|_1 = {lebesgue_constant(10):.4f}, \ \ \|D_{{10^6}}\|_1 = {L[-1]:.4f} \to \infty",
                    font_size=26, color=C.PATHOLOGY),
            label(r"so the norms are unbounded, \ and Banach--Steinhaus says:", font_size=24),
            label(r"for $f$ in a dense $G_\delta$ of $C(T)$, \ $\sup_n |s_n(f)(0)| = \infty$", font_size=26,
                  color=C.EPS),
            label(r"no construction needed", font_size=22, color=GREY_A),
            label(r"Carleson (1966): \ for $f \in L^2$, \ $s_n f \to f$ a.e.", font_size=24, color=C.INNER),
            label(r"Kolmogorov (1926): \ some $f \in L^1$ diverges everywhere", font_size=24, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.5, -0.5, 0])
        for r_ in rows:
            if r_.width > 6.0:
                r_.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.6, -0.5, 0])
        head = label(r"The hook's question, answered by counting", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Now the hook. On the continuous functions on the circle, the functional that takes "
            "f to its n-th partial sum at zero has norm equal to the integral of the absolute Dirichlet kernel. "
            "<bookmark mark='b'/> A continuous function shaped like the sign of the kernel nearly achieves it. "
            "<bookmark mark='c'/> Those norms grow like the log of n. So the family isn't uniformly bounded, and "
            "Banach and Steinhaus say the partial sums at zero are unbounded for a dense G delta of continuous "
            "functions. Most continuous functions have Fourier series that diverge at zero. "
            "<bookmark mark='d'/> For square-integrable functions, Carleson proved in 1966 that the series converge "
            "almost everywhere; for integrable ones, Kolmogorov had found a series diverging everywhere."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(gD), FadeIn(l1), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(Create(bx), Create(gf), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:4]))
            self.play(FadeIn(rows[4:6]))
            vo.wait_until("d")
            self.play(FadeIn(rows[6:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def not_onto(self):
        rows = VGroup(
            label(r"\textbf{RCA 5.14} \ (Riemann--Lebesgue) \ $f \in L^1(T)$ \ $\Rightarrow$ \ $\hat f(n) \to 0$:", font_size=26),
            MathTex(r"f \mapsto \hat f \ \text{ maps } L^1(T) \text{ into } c_0, \text{ one-to-one}", font_size=30),
            label(r"\textbf{RCA 5.15} \ but not onto. \ If it were, \ the open mapping theorem (next chapter) would give",
                  font_size=24),
            MathTex(r"\|f\|_1 \le C\, \|\hat f\|_\infty \ \text{ for all } f", font_size=32, color=C.EPS),
            label(r"test it on $D_n$: \ $\hat D_n(k) = 1$ for $|k| \le n$, \ so $\|\hat D_n\|_\infty = 1$, \ while", font_size=24),
        ).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.3)
        tab = VGroup(*[MathTex(rf"n = {n}: \ \ \|D_n\|_1 / \|\hat D_n\|_\infty = {lebesgue_constant(n):.4f}", font_size=26,
                               color=C.PATHOLOGY) for n in (10, 1000, 100000)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        tab.next_to([0.6, -1.0, 0], RIGHT, buff=0)
        concl = label(r"no constant $C$ works: \ some sequence tending to $0$ is no Fourier series of an $L^1$ function",
                      font_size=24, color=C.EPS).to_edge(DOWN, buff=0.3)
        # the picture: ||D_n||_1 / ||D_n^||_inf = ||D_n||_1 against log n, through any fixed C
        es = np.arange(1, 5.01, 0.25)
        Ls = np.array([lebesgue_constant(int(round(10**e))) for e in es])
        assert np.all(np.diff(Ls) > 0) and Ls[0] < 3 < 5 < Ls[-1]
        pax = plain_axes([1, 5, 1], [2, 6, 1], 5.6, 2.6, numbers=True, font_size=18,
                         x_axis_config={"include_numbers": False},
                         y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.6, -1.35, 0])
        pxl = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=18).next_to(pax.c2p(k, 2), DOWN, buff=0.1) for k in range(1, 6)])
        pdots = VGroup(*[Dot(pax.c2p(e, L_), radius=0.05, color=C.PATHOLOGY) for e, L_ in zip(es, Ls)])
        cline = DashedLine(pax.c2p(1, 5), pax.c2p(5, 5), color=C.EPS, stroke_width=2)
        cl = MathTex(r"\text{any fixed } C", font_size=20, color=C.EPS).next_to(pax.c2p(1.05, 5), UP, buff=0.05).align_to(
            pax.c2p(1.05, 5), LEFT)
        pl = MathTex(r"\|D_n\|_1 \ \text{against } n", font_size=20, color=C.PATHOLOGY).next_to(pax, UP, buff=0.05)
        # first, Riemann-Lebesgue itself: the coefficients of the box 1_[-1,1] on the circle, sin(n)/(pi n), tend to 0
        nn = np.arange(1, 41)
        cf = np.abs(np.sin(nn) / (np.pi * nn))
        tq = np.linspace(-np.pi, np.pi, 200001)
        num = np.array([np.sum(np.where(np.abs(tq) <= 1, 1.0, 0.0) * np.cos(k * tq)) * (tq[1] - tq[0]) / (2 * np.pi)
                        for k in (1, 2, 7)])
        assert np.allclose(np.abs(num), cf[[0, 1, 6]], atol=1e-4) and cf.max() < 0.3
        cax = plain_axes([0, 40, 10], [0, 0.3, 0.1], 5.6, 2.6, numbers=True, font_size=18,
                         x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                         y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.6, -1.35, 0])
        stems = VGroup(*[VGroup(Line(cax.c2p(k, 0), cax.c2p(k, v), color=C.FREQ, stroke_width=3),
                                Dot(cax.c2p(k, v), radius=0.04, color=C.FREQ)) for k, v in zip(nn, cf)])
        cfl = MathTex(r"f = \mathbf 1_{[-1, 1]}: \ \ |\hat f(n)| = \frac{|\sin n|}{\pi n} \to 0", font_size=22,
                      color=C.FREQ).next_to(cax, UP, buff=0.05)
        cpic = VGroup(cax, stems, cfl)
        with self.voiceover(
            "<bookmark mark='a'/> The same kernel answers another question. The Fourier coefficients of an integrable "
            "function tend to zero, by the Riemann-Lebesgue lemma, so the Fourier transform maps L one into the "
            "sequences converging to zero. <bookmark mark='b'/> Is every such sequence a Fourier series? If so, the "
            "open mapping theorem, coming next, would bound the L one norm by the largest coefficient. "
            "<bookmark mark='c'/> The Dirichlet kernels break that bound: their coefficients are all one, and their "
            "L one norms grow without limit. So the map isn't onto, and nobody had to find the missing sequence."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[:2]), Create(cax), FadeIn(cfl))
            self.play(LaggedStart(*[GrowFromEdge(s_, DOWN) for s_ in stems], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[2:4]))
            vo.wait_until("c")
            self.play(FadeOut(cpic), FadeIn(rows[4]), Create(pax), FadeIn(pxl), FadeIn(pl), Create(cline), FadeIn(cl))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in pdots], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(t_) for t_ in tab], lag_ratio=0.4), run_time=2.0)
            self.play(FadeIn(concl))
        self.wait(0.4)
        self.clear_scene()
