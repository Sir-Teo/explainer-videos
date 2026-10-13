from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis8.common import load, plain_axes, polyline
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
        thm = VGroup(
            label(r"\textbf{RCA 5.8} \ (Banach--Steinhaus) \ $X$ Banach, \ $\{\Lambda_\alpha\}$ bounded linear maps $X \to Y$:",
                  font_size=26),
            label(r"either \ $\sup_\alpha \|\Lambda_\alpha\| < \infty$, \ or \ $\sup_\alpha \|\Lambda_\alpha x\| = \infty$ "
                  r"for all $x$ in a dense $G_\delta$", font_size=26, color=C.EPS),
        ).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        sq = Square(side_length=4.4, color=GREY_C, stroke_width=1.5).move_to([-3.6, -1.1, 0])
        rng = np.random.default_rng(5)
        blobs = VGroup()
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.EPS), k / 4) for k in range(5)]
        for k in range(5):
            r = 0.45 + 0.42 * k
            th = np.linspace(0, 2 * np.pi, 120)
            wob = 1 + 0.12 * np.sin(5 * th + k) + 0.08 * np.cos(3 * th - k)
            pts = [[-3.6 + r * w * math.cos(t), -1.1 + r * w * math.sin(t), 0] for t, w in zip(th, wob)]
            blobs.add(Polygon(*pts, stroke_color=cols[k], stroke_width=2.5, fill_color=cols[k], fill_opacity=0.08))
        e_l = VGroup(*[MathTex(rf"E_{{{k + 1}}}", font_size=22, color=cols[k]).move_to(
            [-3.6 + (0.45 + 0.42 * k) * 0.72, -1.1 + (0.45 + 0.42 * k) * 0.72, 0]) for k in range(5)])
        ball = Circle(radius=0.32, color=WHITE, stroke_width=3).move_to([-3.6 + 1.25, -1.1 - 0.6, 0])
        sch = note(r"schematic").next_to(sq, DOWN, buff=0.08)
        steps = VGroup(
            MathTex(r"E_k = \{x : \sup_\alpha \|\Lambda_\alpha x\| \le k\}", font_size=30),
            label(r"closed \ (an intersection of closed sets)", font_size=22, color=GREY_A),
            label(r"if every orbit is bounded, \ $X = \bigcup_k E_k$", font_size=24),
            label(r"Baire: \ some $E_k$ contains a ball $B(x_0, r)$", font_size=24, color=C.EPS),
            MathTex(r"\|x\| < r \Rightarrow \|\Lambda_\alpha x\| \le \|\Lambda_\alpha(x_0 + x)\| + \|\Lambda_\alpha x_0\| "
                    r"\le 2k", font_size=26),
            label(r"so $\|\Lambda_\alpha\| \le 2k/r$ for every $\alpha$: \ uniform", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.0, -1.1, 0])
        for r_ in steps:
            if r_.width > 6.6:
                r_.width = 6.6
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.0, -1.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Banach and Steinhaus: for a family of bounded operators on a Banach space, either "
            "their norms are bounded, or they blow up on a dense G delta. <bookmark mark='b'/> The proof is Baire. "
            "Let E k be the set of points whose orbit stays within k: a closed set. <bookmark mark='c'/> If every "
            "orbit is bounded, the E k cover the whole space, and Baire says one of them must contain a ball. "
            "<bookmark mark='d'/> A ball's worth of uniform bounds, shifted to the origin by linearity, bounds every "
            "operator's norm by the same constant. Pointwise bounds become uniform bounds."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
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
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.5, -0.5, 0])
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
        ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)
        tab = VGroup(*[MathTex(rf"n = {n}: \ \ \|D_n\|_1 / \|\hat D_n\|_\infty = {lebesgue_constant(n):.4f}", font_size=28,
                               color=C.PATHOLOGY) for n in (10, 1000, 100000)]).arrange(DOWN, buff=0.12).next_to(
            rows, DOWN, buff=0.3)
        concl = label(r"no constant $C$ works: \ some sequence tending to $0$ is no Fourier series of an $L^1$ function",
                      font_size=26, color=C.EPS).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> The same kernel answers another question. The Fourier coefficients of an integrable "
            "function tend to zero, by the Riemann-Lebesgue lemma, so the Fourier transform maps L one into the "
            "sequences converging to zero. <bookmark mark='b'/> Is every such sequence a Fourier series? If so, the "
            "open mapping theorem, coming next, would bound the L one norm by the largest coefficient. "
            "<bookmark mark='c'/> The Dirichlet kernels break that bound: their coefficients are all one, and their "
            "L one norms grow without limit. So the map isn't onto, and nobody had to find the missing sequence."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2:4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tab], lag_ratio=0.4), run_time=2.0)
            self.play(FadeIn(concl))
        self.wait(0.4)
        self.clear_scene()
