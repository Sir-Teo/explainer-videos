from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import area_under, between, load, plain_axes, polyline, trap
from videos.analysis6.compute import ramp


class RieszFischer(VoiceoverScene):
    def construct(self):
        self.card()
        self.proof()
        self.limit()
        self.dense()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"$L^p$ is complete", r"Does every Cauchy sequence in $L^p$ converge?", lit=(1907,),
                            part=6)
        with self.voiceover("Chapter four: the theorem of Riesz and Fischer, from 1907. L p has no holes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def proof(self):
        pm = ProofMap([r"a fast subsequence: \ $\|f_{n_{i+1}} - f_{n_i}\|_p < 2^{-i}$",
                       r"$g = \sum_i |f_{n_{i+1}} - f_{n_i}|$ \ has $\|g\|_p \le 1$",
                       r"so $g < \infty$ a.e., \ and $f_{n_i} \to f$ a.e.",
                       r"Fatou: \ $\|f - f_m\|_p \le \varepsilon$ \ for $m \ge N$"],
                      font_size=20, width=5.6, buff=0.2, direction=DOWN).move_to([3.6, 0.55, 0])
        head = VGroup(label(r"Riesz--Fischer: \ $L^p(\mu)$ is complete, \ $1 \le p \le \infty$", font_size=34),
                      label(r"\textbf{RCA 3.11} \ the idea: \ a Cauchy sequence has a subsequence whose steps are "
                            r"summable", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"every partial sum of $g$ is small:", font_size=22, color=GREY_B),
            MathTex(r"\Big\|\sum_{i \le k} |f_{n_{i+1}} - f_{n_i}|\Big\|_p \le \sum_{i \le k} 2^{-i} < 1", font_size=28),
            label(r"(Minkowski), \ and monotone convergence lets $k \to \infty$", font_size=22, color=GREY_B),
            MathTex(r"f = f_{n_1} + \sum_i (f_{n_{i+1}} - f_{n_i}) \ \text{ converges where } g < \infty", font_size=28),
            MathTex(r"\int |f - f_m|^p \le \liminf_i \int |f_{n_i} - f_m|^p \le \varepsilon^p", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([-3.3, -0.9, 0])
        for r_ in steps:
            if r_.width > 6.4:
                r_.width = 6.4
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.3, -0.6, 0])
        # the picture: a fast subsequence as a walk whose steps halve, so its total length is finite
        z = [np.zeros(2)]
        for i in range(1, 11):
            z.append(z[-1] + 2.2 * 0.5**i * np.array([math.cos(0.95 * i + 0.3), math.sin(0.95 * i + 0.3)]))
        z = np.array(z)
        org = np.array([0.9, -3.4, 0])
        P = [org + np.array([p_[0], p_[1], 0]) * 1.6 for p_ in z]  # height 1.49 * 1.6: under the proof map
        walk = VGroup(*[Line(P[i], P[i + 1], color=C.SEQ, stroke_width=3) for i in range(10)])
        wdots = VGroup(*[Dot(q, radius=0.04, color=C.SEQ) for q in P[:-1]])
        lim = Star(n=5, outer_radius=0.08, color=C.EPS, fill_opacity=1).move_to(P[-1])
        wl = VGroup(MathTex(r"f_{n_1}", font_size=24, color=C.SEQ).next_to(P[0], LEFT, buff=0.1),
                    MathTex(r"f", font_size=26, color=C.EPS).next_to(P[-1], RIGHT, buff=0.2))
        assert max(q_[1] for q_ in P) < pm.get_bottom()[1] - 0.15 and min(q_[1] for q_ in P) > -3.6
        seglen = np.linalg.norm(np.diff(z, axis=0), axis=1)
        assert np.allclose(seglen, 2.2 * 0.5 ** np.arange(1, 11)) and seglen.sum() < 2.2
        wt = VGroup(label(r"steps $< 2^{-i}$: \ total length $< 1$,", font_size=22, color=GREY_A),
                    label(r"so the walk has an end", font_size=22, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(walk, RIGHT, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Riesz-Fischer: L p is complete, for every p from one to infinity. Here's the plan "
            "of Rudin's proof. <bookmark mark='b'/> Start with a Cauchy sequence. Pick a subsequence so fast that the "
            "steps between its terms are smaller than one half, one quarter, one eighth, and so on. "
            "<bookmark mark='c'/> Add up the absolute values of those steps into one function g. By Minkowski, every "
            "partial sum has norm less than one, and monotone convergence passes to the whole sum. "
            "<bookmark mark='d'/> A function with finite norm is finite almost everywhere. So at almost every point "
            "the steps are summable, and the subsequence converges there, to a function f. "
            "<bookmark mark='e'/> Finally Fatou's lemma turns the Cauchy condition into convergence in norm. The "
            "only tools are the three limit theorems of Part 5, which is why Riemann's integral couldn't do this."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head[0]))
            self.play(FadeIn(pm))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d_), Create(w_)) for d_, w_ in zip(wdots, walk)], lag_ratio=0.5),
                      FadeIn(wl[0]), run_time=2.5)
            self.play(FadeIn(lim), FadeIn(wl[1]), FadeIn(wt))
            vo.wait_until("b")
            self.play(*pm.light(0), FadeIn(head[1]))
            vo.wait_until("c")
            self.play(*pm.light(1), FadeIn(steps[:3]))
            vo.wait_until("d")
            self.play(*pm.light(2), FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(*pm.light(3), FadeIn(steps[4]))
            self.play(*pm.done())
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limit(self):
        d = load("stacking")
        nk, inc = d["nk"], d["inc"]
        ax = plain_axes([0, 1, 0.25], [0, 1.1, 0.5], 5.8, 3.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.3, -0.5, 0])
        x = np.linspace(0, 1, 2001)
        K = 6
        incs = [np.abs(ramp(x, 2 * n) - ramp(x, n)) for n in nk[:K]]
        layers, gs = [], []
        base = ramp(x, 1)
        g0 = polyline(ax, x, base, color=C.SEQ, stroke_width=3)
        cur = base.copy()
        cols = [interpolate_color(ManimColor(C.MEASURE), ManimColor(C.EPS), k / (K - 1)) for k in range(K)]
        for k in range(K):
            nxt = cur + incs[k]
            layers.append(between(ax, x, nxt, cur, cols[k], 0.55))
            gs.append(polyline(ax, x, nxt, color=cols[k], stroke_width=2.5))
            cur = nxt
        g_lim = np.where(x < 0.5, 2 * x, 1.0)
        # the partial stack telescopes: g - g_K = |step - r_(2^K)|, of area 1 / (4 * 2^K)
        gK = base + sum(np.abs(ramp(x, 2 * n) - ramp(x, n)) for n in nk)
        assert abs(trap(np.abs(g_lim - gK), x) - 1 / (8 * nk[-1])) < 1e-4
        g_inf = polyline(ax, x, g_lim, color=WHITE, stroke_width=2).set_stroke(opacity=0.7)
        g_l = MathTex(r"g = r_1 + \sum_k |r_{2^{k+1}} - r_{2^k}|", font_size=28, color=C.EPS).next_to(ax, UP, buff=0.15)
        r1l = MathTex(r"r_1", font_size=26, color=C.SEQ).move_to(ax.c2p(0.8, 0.62))
        bars = VGroup()
        bx0, by0, W = 1.4, -1.9, 4.6
        scale = W / 0.25
        acc = 0.0
        for k in range(len(inc)):
            w = float(inc[k]) * scale
            bars.add(Rectangle(width=max(w, 0.02), height=0.42, stroke_width=1, stroke_color=BACKGROUND,
                               fill_color=cols[min(k, K - 1)], fill_opacity=0.85).move_to([bx0 + acc + w / 2, by0, 0]))
            acc += w
        frame = Rectangle(width=W, height=0.42, stroke_color=GREY_B, stroke_width=1.5).move_to([bx0 + W / 2, by0, 0])
        b_l = MathTex(r"\|r_{2n} - r_n\|_1 = \tfrac{1}{8n}: \ " + r",\ ".join(f"{v:.4f}" for v in inc[:3]) + r",\ \ldots",
                      font_size=24, color=C.MEASURE).next_to(frame, UP, buff=0.15).align_to(frame, LEFT)
        tot = MathTex(rf"\sum = {inc.sum():.4f} < \tfrac14", font_size=28, color=C.EPS).next_to(frame, DOWN, buff=0.15)
        assert np.allclose(inc, 1 / (8 * nk), rtol=1e-3) and inc.sum() < 0.25
        gn = MathTex(rf"\|g\|_1 = \tfrac12 + \tfrac14 = {trap(g_lim, x):.4f}", font_size=28, color=WHITE).next_to(
            frame, UP, buff=1.0).align_to(frame, LEFT)
        lim_t = VGroup(label(r"and the series $r_1 + \sum_k (r_{2^{k+1}} - r_{2^k})$ converges everywhere", font_size=24),
                       label(r"(except at $\tfrac12$) \ to the step $\mathbf 1_{(1/2, 1]}$", font_size=24,
                             color=C.EPS)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.6, 2.0, 0])
        head = label(r"The proof, run on the hook's ramps \ ($n_k = 2^k$)", font_size=34).to_edge(UP, buff=0.3)
        # the partial sums of the telescoping series are the ramps r_(2^k); they close in on the step
        part = [polyline(ax, x, ramp(x, 2**k), color=C.SEQ, stroke_width=3) for k in range(7)]
        assert all(abs(trap(np.abs(ramp(x, 2**k) - (x > 0.5)), x) - 1 / (4 * 2**k)) < 1e-4 for k in range(7))
        stp = VGroup(Line(ax.c2p(0, 0), ax.c2p(0.5, 0), color=C.EPS, stroke_width=3),
                     Line(ax.c2p(0.5, 1), ax.c2p(1, 1), color=C.EPS, stroke_width=3),
                     Dot(ax.c2p(0.5, 0), radius=0.06, color=C.EPS),
                     Circle(radius=0.06, color=C.EPS, stroke_width=2.5).set_fill(BACKGROUND, 1).move_to(ax.c2p(0.5, 1)),
                     Dot(ax.c2p(0.5, 0.5), radius=0.05, color=C.SEQ)).set_z_index(3)
        r_k = MathTex(r"r_1, r_2, r_4, \ldots, r_{64}", font_size=26, color=C.SEQ).next_to(ax.c2p(0.62, 0.42), RIGHT,
                                                                                         buff=0.1)
        with self.voiceover(
            "<bookmark mark='a'/> Let's run the proof on the ramps from the beginning of this part. The subsequence "
            "one, two, four, eight is fast enough: the step from ramp n to ramp two n has area one over eight n. "
            "<bookmark mark='b'/> Stack those steps on top of the first ramp. Each layer is a thin sliver near one "
            "half, and the stack grows toward a bounded function g. <bookmark mark='c'/> The areas of the layers "
            "form a geometric series, adding up to a quarter, so g has finite integral. "
            "<bookmark mark='d'/> So the telescoping series converges, at every point except one half, and its sum "
            "is the step. The hole from the hook is filled, by a function in L one."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(Create(g0), FadeIn(r1l), FadeIn(g_l))
            vo.wait_until("b")
            for k in range(K):
                self.play(FadeIn(layers[k]), Create(gs[k]), run_time=0.7)
            self.play(Create(g_inf))
            vo.wait_until("c")
            self.play(Create(frame), FadeIn(b_l))
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.4), run_time=2.5)
            self.play(FadeIn(tot), FadeIn(gn))
            vo.wait_until("d")
            stack = VGroup(*layers, *gs, g0, g_inf)
            self.play(stack.animate.set_opacity(0.25), FadeOut(r1l), FadeIn(lim_t))
            self.play(Create(part[0]), FadeIn(r_k), run_time=0.5)
            for k in range(1, 7):
                self.play(ReplacementTransform(part[k - 1], part[k]), run_time=0.45)
            self.play(FadeIn(stp))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dense(self):
        d = load("ramps")
        ns = d["ns"]
        ax = plain_axes([0, 1, 0.25], [-0.6, 1.6, 0.5], 5.6, 3.6).move_to([-3.4, -0.75, 0])
        x = np.linspace(0, 1, 2001)
        step = (x > 0.5).astype(float)
        st = VGroup(Line(ax.c2p(0, 0), ax.c2p(0.5, 0), color=WHITE, stroke_width=3),
                    Line(ax.c2p(0.5, 1), ax.c2p(1, 1), color=WHITE, stroke_width=3))
        ax.y_axis.add_numbers([-0.5, 0.5, 1.0, 1.5], num_decimal_places=1, font_size=18)
        st.set_z_index(3)
        tube = VGroup(between(ax, x[x <= 0.5], step[x <= 0.5] + 0.5, step[x <= 0.5] - 0.5, C.EPS, 0.14),
                      between(ax, x[x > 0.5], step[x > 0.5] + 0.5, step[x > 0.5] - 0.5, C.EPS, 0.14),
                      *[DashedLine(ax.c2p(a_, h_), ax.c2p(b_, h_), color=C.EPS, stroke_width=2, dash_length=0.08)
                        for a_, b_, h_ in ((0, 0.5, 0.5), (0, 0.5, -0.5), (0.5, 1, 1.5), (0.5, 1, 0.5))])
        # a continuous g, and why it fails: near 1/2 it is close to g(1/2), which is 1/2 away from 0 or from 1
        gfun = 0.5 + 0.5 * np.tanh(40 * (x - 0.5))
        assert np.max(np.abs(gfun - step)) >= 0.5 - 1e-3 and abs(gfun[1000] - 0.5) < 1e-12 and x[1000] == 0.5
        gg = polyline(ax, x, gfun, color=C.APPROX, stroke_width=3.5)
        gg_l = MathTex(r"g", font_size=28, color=C.APPROX).next_to(ax.c2p(0.62, float(np.interp(0.62, x, gfun))), DR,
                                                                   buff=0.08)
        gap_ = VGroup(Line(ax.c2p(0.5, 0), ax.c2p(0.5, 0.5), color=C.PATHOLOGY, stroke_width=5),
                      Line(ax.c2p(0.5, 0.5), ax.c2p(0.5, 1), color=C.PATHOLOGY, stroke_width=5),
                      Dot(ax.c2p(0.5, 0.5), radius=0.06, color=C.APPROX))
        gap_l = MathTex(r"\ge \tfrac12", font_size=28, color=C.PATHOLOGY).next_to(ax.c2p(0.5, 0.25), LEFT, buff=0.12)
        tube_l = label(r"the tube of half-width $\tfrac12$", font_size=22, color=C.EPS).next_to(ax, UP, buff=0.1)
        ramps_ = [polyline(ax, x, ramp(x, n), color=C.SEQ, stroke_width=3) for n in (2, 8, 64)]
        sup = [float(np.abs(ramp(x, n) - step).max()) for n in ns]
        assert all(abs(s - 0.5) < 1e-3 for s in sup)
        rows = VGroup(
            label(r"\textbf{RCA 3.14} \ for $1 \le p < \infty$, \ $C_c(X)$ is dense in $L^p(\mu)$", font_size=26),
            label(r"the ramps were exactly that: \ continuous, \ $\to \mathbf 1_{(1/2, 1]}$ in $L^1$", font_size=24,
                  color=GREY_A),
            label(r"\textbf{but not in $L^\infty$:} \ $\|r_n - \mathbf 1_{(1/2, 1]}\|_\infty = \tfrac12$ for every $n$",
                  font_size=24, color=C.PATHOLOGY),
            label(r"any continuous $g$ is within $\tfrac12$ of $0$ or of $1$ near $\tfrac12$, \ never both:", font_size=22,
                  color=GREY_A),
            MathTex(r"\|g - \mathbf 1_{(1/2, 1]}\|_\infty \ge \tfrac12", font_size=30, color=C.PATHOLOGY),
            label(r"uniform limits of continuous functions are continuous (Part 3): \ $C$ is closed in $L^\infty$",
                  font_size=22, color=GREY_A),
            label(r"in $L^\infty$, \ simple functions are dense instead \ (RCA 3.13)", font_size=24, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.15, -0.6, 0])
        for r_ in rows:
            if r_.width > 6.3:
                r_.width = 6.3
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.15, -0.6, 0])
        rows[4].shift(RIGHT * 0.4)
        head = label(r"Which functions are dense in $L^p$?", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The ramps show something else. Continuous functions with compact support are dense "
            "in L p, for every finite p: every function in L p is a limit of them, as the step is a limit of ramps. "
            "<bookmark mark='b'/> Infinity is the exception. In the sup norm, every ramp stays at distance one half "
            "from the step: the yellow tube of half-width one half. <bookmark mark='c'/> In fact any continuous "
            "function, near one half, can't be close to zero on the left and close to one on the right. And uniform "
            "limits of continuous functions are continuous, as Part 3 showed, so the continuous functions are a "
            "closed subspace of L infinity, not a dense one. Simple functions take over there."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(st))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(ramps_[0]))
            self.play(ReplacementTransform(ramps_[0], ramps_[1]), FadeIn(rows[1]))
            self.play(ReplacementTransform(ramps_[1], ramps_[2]))
            vo.wait_until("b")
            self.play(FadeIn(tube), FadeIn(tube_l), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(ramps_[2].animate.set_stroke(opacity=0.3), Create(gg), FadeIn(gg_l))
            self.play(Create(gap_), FadeIn(gap_l), FadeIn(rows[3:5]))
            self.play(FadeIn(rows[5:]))
        self.wait(0.4)
        self.clear_scene()
