from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import load, plain_axes, polyline


class Equicontinuity(VoiceoverScene):
    def construct(self):
        self.card()
        self.not_compact()
        self.bump()
        self.equi()
        self.uniform_equi()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"Equicontinuity", r"What does compactness cost in a space of functions?", lit=(), part=3)
        with self.voiceover(
            "Chapter nine. In R n, closed and bounded sets are compact. In the space of continuous functions, Part 1 "
            "already warned us, they are not. Here is what's missing."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def not_compact(self):
        ax = plain_axes([0, 2 * np.pi, np.pi], [-1.2, 1.2, 1], 6.6, 3.8).move_to([-3.3, -0.6, 0])
        x = np.linspace(0, 2 * np.pi, 2000)
        K = 8
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.APPROX), k / (K - 1)) for k in range(K)]
        gs = VGroup(*[polyline(ax, x, np.sin((k + 1) * x), color=cols[k], stroke_width=2) for k in range(K)])
        D = np.array([[np.abs(np.sin(j * x) - np.sin(k * x)).max() for k in range(1, K + 1)] for j in range(1, K + 1)])
        off = D[~np.eye(K, dtype=bool)]
        assert off.min() > 1.0 and off.max() < 2.0
        lo_, hi_ = float(off.min()), float(off.max())
        cs = 0.42
        cells = VGroup()
        for j in range(K):
            for k in range(K):
                v = D[j, k]
                a_ = (v - lo_) / (hi_ - lo_)
                sq = Square(side_length=cs * 0.92, stroke_width=0, fill_opacity=0.9,
                            fill_color=GREY_E if j == k else interpolate_color(ManimColor("#6B5A2E"), ManimColor(C.EPS), a_))
                sq.move_to([2.2 + k * cs, 1.2 - j * cs, 0])
                t = MathTex(f"{v:.1f}" if j != k else "0", font_size=16,
                            color=BLACK if (j != k and a_ > 0.45) else WHITE).move_to(sq)
                cells.add(VGroup(sq, t))
        jl = VGroup(*[MathTex(str(j + 1), font_size=18, color=GREY_B).next_to(cells[j * K], LEFT, buff=0.1)
                      for j in range(K)], MathTex(r"j", font_size=22, color=GREY_A).next_to(cells[0], UL, buff=0.12))
        kl = VGroup(*[MathTex(str(k + 1), font_size=18, color=GREY_B).next_to(cells[k], UP, buff=0.08) for k in range(K)])
        mlab = MathTex(r"\sup|\sin jx - \sin kx|", r"\ \ (k \to)", font_size=26).next_to(kl, UP, buff=0.1)
        mlab[1].set_color(GREY_A)
        mmin = MathTex(rf"\min_{{j \ne k}} = {lo_:.2f} > 1", font_size=26, color=C.EPS).next_to(cells, DOWN, buff=0.2)
        head = VGroup(label(r"$\sin nx$: \ all in the unit ball of $C[0, 2\pi]$, \ all far apart", font_size=30),
                      label(r"every pair is at sup distance $> 1$: \ no subsequence converges uniformly", font_size=24,
                            color=C.PATHOLOGY)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        foot = label(r"(Rudin 7.20 shows more: \ no subsequence converges even pointwise)", font_size=22,
                     color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='a'/> Take sine of n x on the interval from zero to two pi. Every one of them is bounded "
            "by one, so they all lie in the unit ball of the space. <bookmark mark='b'/> But compute their sup "
            "distances: every pair is more than one apart. No subsequence can be Cauchy, so none converges uniformly, "
            "and the closed, bounded unit ball is not compact. Rudin shows even more: no subsequence converges at "
            "every point."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(g_) for g_ in gs], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.01), FadeIn(mlab), FadeIn(jl), FadeIn(kl),
                      run_time=1.5)
            self.play(FadeIn(mmin))
            self.play(FadeIn(head[1]), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bump(self):
        d = load("equi")
        ax = plain_axes([0, 1, 0.25], [0, 1.1, 0.5], 7.6, 4.0).move_to([-2.4, -0.8, 0])
        x = np.unique(np.r_[np.linspace(0, 1, 2001), np.linspace(0, 0.1, 4001)])  # dense where the bump lives
        nT = ValueTracker(1.0)
        g = always_redraw(lambda: polyline(ax, x, x**2 / (x**2 + (1 - nT.get_value() * x) ** 2), color=C.FUNC,
                                           stroke_width=3.5))
        peak = always_redraw(lambda: Dot(ax.c2p(1 / nT.get_value(), 1), radius=0.07, color=C.PATHOLOGY))
        head = VGroup(MathTex(r"f_n(x) = \frac{x^2}{x^2 + (1 - nx)^2} \quad (\text{Rudin 7.21})", font_size=34),
                      label(r"$|f_n| \le 1$, \ \ $f_n(x) \to 0$ at every $x$, \ \ but $f_n(1/n) = 1$", font_size=26,
                            color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        side = VGroup(label(r"bounded, convergent everywhere,", font_size=24),
                      label(r"yet no subsequence converges uniformly:", font_size=24),
                      label(r"each bump is a full $1$ tall", font_size=24, color=C.PATHOLOGY)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                 buff=0.12)
        side.move_to([4.4, -0.6, 0])
        nl = always_redraw(lambda: MathTex(rf"n = {nT.get_value():.0f}", font_size=28, color=C.FUNC).next_to(ax, DOWN,
                                                                                                    buff=0.15))
        assert np.allclose(d["sups"], 1.0)
        inset, decor = magnifier(ax, (0, 0.1), (0, 1.1), center=[-2.05, -0.35, 0], width=3.8, height=2.0, color=GREY_B,
                                 tag=r"x\text{ stretched } \times 5")
        assert abs(3.8 / (ax.c2p(0.1, 0)[0] - ax.c2p(0, 0)[0]) - 5) < 1e-6
        xz = np.linspace(0, 0.1, 4001)
        gz = always_redraw(lambda: polyline(inset, xz, xz**2 / (xz**2 + (1 - nT.get_value() * xz) ** 2), color=C.FUNC,
                                            stroke_width=3))
        pz = always_redraw(lambda: Dot(inset.c2p(1 / nT.get_value(), 1), radius=0.07, color=C.PATHOLOGY))
        one_z = VGroup(DashedLine(inset.c2p(0, 1), inset.c2p(0.1, 1), color=GREY_B, stroke_width=1.5, dash_length=0.06),
                       MathTex(r"1", font_size=22, color=GREY_B).next_to(inset.c2p(0.1, 1), RIGHT, buff=0.08))
        for n_ in (30, 60):  # sampled finely enough that the drawn bump still reaches 1 at 1/n
            assert abs((xz**2 / (xz**2 + (1 - n_ * xz) ** 2)).max() - 1) < 1e-2
            assert abs((x**2 / (x**2 + (1 - n_ * x) ** 2)).max() - 1) < 1e-2
        with self.voiceover(
            "<bookmark mark='a'/> A second example, from Rudin. These functions are bounded by one and converge to zero "
            "at every single point. <bookmark mark='b'/> But each has a bump of height exactly one, at one over n, "
            "which slides toward zero and gets narrower. No subsequence can converge uniformly, since the sup distance "
            "to zero stays one. Being bounded, even converging pointwise, is not enough. What fails is the "
            "steepness: the family gets steeper and steeper."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(g), FadeIn(peak), FadeIn(nl))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(nT.animate.set_value(30), run_time=4.0, rate_func=rate_functions.ease_in_quad)
            self.play(FadeIn(decor), FadeIn(gz), FadeIn(pz), FadeIn(one_z))
            self.play(FadeIn(side))
            self.play(nT.animate.set_value(60), run_time=4.0, rate_func=linear)
        for m in (g, peak, nl, gz, pz):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def equi(self):
        d = load("equi")
        eps, d_soft, Ks, d_hard = float(d["eps"]), float(d["d_soft"]), d["Ks"], d["d_hard"]
        dfn = VGroup(label(r"\textbf{Rudin 7.22} \ a family $\mathcal F$ is \textbf{equicontinuous} if", font_size=28),
                     MathTex(r"\forall \varepsilon\ \exists \delta\ \forall f \in \mathcal F\ \forall x, y:\ "
                             r"|x - y| < \delta \Rightarrow |f(x) - f(y)| < \varepsilon", font_size=32),
                     label(r"the game board again: \ $\delta$ is chosen before the point \emph{and} before the function",
                           font_size=24, color=C.EPS)).arrange(DOWN, buff=0.14).to_edge(UP, buff=0.25)
        dfn[1][0][0:2].set_color(C.EPS)
        dfn[1][0][2:4].set_color(C.DELTA)
        x = np.linspace(0, 2 * np.pi, 2400)
        axL = plain_axes([0, 2 * np.pi, np.pi], [-1.1, 1.1, 1], 5.6, 3.0).move_to([-3.4, -0.75, 0])
        axR = plain_axes([0, 2 * np.pi, np.pi], [-1.1, 1.1, 1], 5.6, 3.0).move_to([3.4, -0.75, 0])
        K = 10
        fam_L = VGroup(*[polyline(axL, x, np.sin(k * x) / k, color=C.SEQ, stroke_width=2) for k in range(1, K + 1)])
        fam_R = VGroup(*[polyline(axR, x, np.sin(k * x), color=C.APPROX, stroke_width=1.6) for k in range(1, K + 1)])
        tL = MathTex(r"\{\sin(kx)/k\}", font_size=30, color=C.SEQ).next_to(axL, UP, buff=0.1)
        tR = MathTex(r"\{\sin kx : k \le K\}", font_size=30, color=C.APPROX).next_to(axR, UP, buff=0.1)

        def column(ax, dl, x0=2.0):
            p0, p1 = ax.c2p(x0, -1.1), ax.c2p(x0 + dl, 1.1)
            return Rectangle(width=max(p1[0] - p0[0], 0.012), height=p1[1] - p0[1], stroke_width=1.5, stroke_color=C.DELTA,
                             fill_color=C.DELTA, fill_opacity=0.35).move_to((p0 + p1) / 2)

        colL = column(axL, d_soft)
        colR = column(axR, float(d_hard[1]))
        labL = MathTex(rf"\delta = 2\arcsin\tfrac{{\varepsilon}}{{2}} = {d_soft:.4f}", font_size=26, color=C.DELTA).next_to(
            axL, DOWN, buff=0.15)
        labR = VGroup(*[MathTex(rf"K = {int(k)}: \ \delta = {dh:.4f}", font_size=26, color=C.DELTA) for k, dh in
                        zip(Ks, d_hard)]).arrange_in_grid(rows=2, cols=2, buff=(0.5, 0.12), flow_order="rd")
        labR.next_to(axR, DOWN, buff=0.15)
        verdict = VGroup(label(r"one $\delta$ for all: \ equicontinuous", font_size=24, color=C.CONNECTED_SET).next_to(
                             labL, DOWN, buff=0.12),
                         label(r"$\delta \to 0$ as $K$ grows: \ not equicontinuous", font_size=24,
                               color=C.PATHOLOGY).next_to(labR, DOWN, buff=0.12))
        with self.voiceover(
            "<bookmark mark='a'/> The missing ingredient is equicontinuity: one delta that works not only for every "
            "pair of points, but for every function in the family at once. It's the epsilon-delta game with delta "
            "chosen before the point and before the function. <bookmark mark='b'/> On the left, sine k x over k. "
            "Every one of them has slope at most one, so a single delta, just over a tenth, keeps every function's "
            "change below a tenth, whatever k is. <bookmark mark='c'/> On the right, sine k x without the damping. "
            "With ten of them, delta must be a hundredth; with a thousand, a ten-thousandth. No delta serves the whole "
            "family: the steep members ruin it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dfn[:2]), Create(axL), Create(axR), FadeIn(tL), FadeIn(tR))
            self.play(LaggedStart(*[Create(f_) for f_ in fam_L], lag_ratio=0.1),
                      LaggedStart(*[Create(f_) for f_ in fam_R], lag_ratio=0.1), run_time=2.5)
            self.play(FadeIn(dfn[2]))
            vo.wait_until("b")
            self.play(FadeIn(colL), FadeIn(labL))
            self.play(colL.animate.shift(RIGHT * (axL.c2p(4.0, 0)[0] - axL.c2p(2.0, 0)[0])), run_time=1.5)
            self.play(FadeIn(verdict[0]))
            vo.wait_until("c")
            self.play(FadeIn(colR), FadeIn(labR))
            self.play(FadeIn(verdict[1]))
        assert abs(d_soft - 0.1) < 1e-3 and abs(float(d_hard[1]) - d_soft / 10) < 1e-12
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uniform_equi(self):
        x = np.linspace(0, 2 * np.pi, 3001)
        dx = x[1] - x[0]
        N, eps = 8, 0.6
        fs = [np.sin(x) + 0.8 * np.sin(3 * n * x) / n for n in range(1, 25)]
        for n in range(N, 25):
            assert np.abs(fs[n - 1] - fs[N - 1]).max() < eps / 3

        def delta_for(y, eta):
            """The largest grid step h with max |y(t + h) - y(t)| < eta."""
            k = 1
            while np.abs(y[k + 1:] - y[:-(k + 1)]).max() < eta:
                k += 1
            return k

        ks = [delta_for(fs[n - 1], eps) for n in range(1, N)] + [delta_for(fs[N - 1], eps / 3)]
        kd = min(ks)
        delta = kd * dx
        assert all(np.abs(f[kd:] - f[:-kd]).max() < eps for f in fs)  # one delta for the whole family
        assert max(np.abs(f_).max() for f_ in fs) < 1.85
        ax = plain_axes([0, 2 * np.pi, np.pi], [-1.9, 1.9, 1], 6.2, 4.4).move_to([-3.3, -0.7, 0])
        early = VGroup(*[polyline(ax, x, fs[n - 1], color=C.SEQ, stroke_width=1.6) for n in range(1, N)])
        late = VGroup(*[polyline(ax, x, fs[n - 1], color=C.APPROX, stroke_width=1.2) for n in range(N + 1, 25)])
        fN = polyline(ax, x, fs[N - 1], color=C.EPS, stroke_width=3.5).set_z_index(2)
        pts = ([ax.c2p(a, b) for a, b in zip(x[::6], fs[N - 1][::6] + eps / 3)] +
               [ax.c2p(a, b) for a, b in zip(x[::-6], fs[N - 1][::-6] - eps / 3)])
        band = Polygon(*pts, stroke_width=0, fill_color=C.EPS, fill_opacity=0.18).set_z_index(1)
        x0 = 2.4
        p0, p1 = ax.c2p(x0, -1.9), ax.c2p(x0 + delta, 1.9)
        col = Rectangle(width=max(p1[0] - p0[0], 0.02), height=p1[1] - p0[1], stroke_width=1.5, stroke_color=C.DELTA,
                        fill_color=C.DELTA, fill_opacity=0.35).move_to((p0 + p1) / 2)
        tl = MathTex(r"f_n(x) = \sin x + \frac{0.8\,\sin 3nx}{n}, \ n \le 24", font_size=28).next_to(ax, UP, buff=0.1)
        rows = VGroup(
            label(r"\textbf{Rudin 7.24} \ $K$ compact, \ $f_n \in C(K)$,", font_size=28),
            label(r"$f_n$ converges uniformly \ $\Rightarrow$ \ $\{f_n\}$ is equicontinuous", font_size=28, color=C.EPS),
            label(rf"past $N = {N}$: \ every $f_n$ within $\varepsilon/3$ of $f_N$", font_size=26, color=C.EPS),
            label(rf"the first {N - 1}: \ finitely many, each uniformly continuous", font_size=26, color=C.SEQ),
            MathTex(rf"\delta = \min(\delta_1, \dots, \delta_{{{N}}}) = {delta:.4f}", font_size=30, color=C.DELTA),
            label(r"so equicontinuity is \emph{necessary} for uniform convergence;", font_size=26),
            label(r"next chapter: \ with boundedness, it is also \emph{enough}", font_size=26, color=C.COMPACT_SET),
        )
        for r_ in rows:
            if r_.width > 6.2:
                r_.width = 6.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.65, -0.35, 0])
        with self.voiceover(
            "<bookmark mark='a'/> And equicontinuity is necessary. If continuous functions converge uniformly on a "
            "compact set, they form an equicontinuous family. <bookmark mark='b'/> Past some N they're all within "
            "a third of epsilon of one function, f N, so they inherit its delta, up to two more thirds. "
            "<bookmark mark='c'/> The finitely many before N are each uniformly continuous, and the smallest of their "
            "finitely many deltas works for all of them. <bookmark mark='d'/> One column of that width serves the "
            "whole family. <bookmark mark='e'/> The next chapter shows the converse, which is the real prize: bounded "
            "and equicontinuous is enough for a convergent subsequence."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[:2]), Create(ax), FadeIn(tl), Create(fN), FadeIn(early), FadeIn(late))
            vo.wait_until("b")
            self.play(FadeIn(band), FadeIn(rows[2]), early.animate.set_stroke(opacity=0.25), fN.animate.set_stroke(width=4))
            vo.wait_until("c")
            self.play(early.animate.set_stroke(opacity=1.0), late.animate.set_stroke(opacity=0.3), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(late.animate.set_stroke(opacity=0.3), early.animate.set_stroke(opacity=0.6), FadeIn(col),
                      FadeIn(rows[4]))
            self.play(col.animate.shift(RIGHT * (ax.c2p(4.6, 0)[0] - ax.c2p(x0, 0)[0])), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(rows[5:]))
        self.wait(0.4)
        self.clear_scene()
