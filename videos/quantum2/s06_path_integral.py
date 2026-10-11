from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (WaveView, bar_chart, corner_wheel, gold_img, hue, label, ladder, load, mtex, note,
                                    num_table, part_card, plain_axes, polyline, tick_labels, wave_axes, why)


class PathIntegral(VoiceoverScene):
    def construct(self):
        self.card()
        self.propagator()
        self.screens()
        self.slicing_picture()
        self.derivation()
        self.imaginary_time()
        self.pimc()

    # ------------------------------------------------------------------
    def card(self):
        c = part_card(2, r"Sums over paths", r"Feynman's formulation, and what it explains")
        with self.voiceover("Part 2: Sums over paths."):
            self.play(FadeIn(c))
        self.wait(0.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def propagator(self):
        x = np.linspace(-8, 8, 2400)
        t = ValueTracker(1.0)

        def K(tt):
            return np.sqrt(1 / (2j * np.pi * tt)) * np.exp(1j * x**2 / (2 * tt))

        ax = wave_axes((-8, 8), (0, 0.75), x_length=11.5, y_length=2.4).move_to(DOWN * 1.6)
        wv = WaveView(ax, x, K(1.0), mode="abs", scale=1.0).follow(t, K)
        src = Dot(ax.c2p(0, 0), color=WHITE, radius=0.07)
        xl = MathTex(r"x_b", font_size=30, color=C.XPOS).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        tl = always_redraw(lambda: MathTex(f"t = {t.get_value():.2f}", font_size=30, color=C.QTIME).next_to(ax, UP, buff=0.05).to_edge(RIGHT, buff=0.7))
        d1 = MathTex(r"K(x_b, t;\, x_a, 0)", r"=", r"\bra{x_b}e^{-i\hat Ht/\hbar}\ket{x_a}", font_size=38).to_edge(UP, buff=0.4)
        d2 = MathTex(r"\psi(x_b, t)", r"=", r"\int K(x_b, t;\, x_a, 0)\,\psi(x_a, 0)\,dx_a", font_size=36).next_to(d1, DOWN, buff=0.3)
        d3 = MathTex(r"K_{\text{free}}", r"=", r"\sqrt{\frac{m}{2\pi i\hbar t}}\;\exp\!\Big(\frac{im(x_b - x_a)^2}{2\hbar t}\Big)", font_size=36).next_to(d2, DOWN, buff=0.3)
        d3[2].set_color(C.ACTION)
        hl = label(r"height $= |K|$, color $=$ phase; $\hbar = m = 1$, $x_a = 0$", font_size=22, color=GREY_B).next_to(ax, DOWN, buff=0.12)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.26)
        with self.voiceover(
            "Everything about time evolution is packed into one function: <bookmark mark='a'/> the amplitude to start at "
            "x a and be found at x b a time t later, called the propagator, K. <bookmark mark='b'/> Any initial "
            "wavefunction evolves by adding up the propagator from every starting point. <bookmark mark='c'/> For a free "
            "particle it's a Gaussian with an imaginary exponent: <bookmark mark='d'/> its size is the same everywhere, "
            "and its phase grows with the square of the distance, so the colors cycle faster and faster. "
            "<bookmark mark='e'/> A particle that starts at one point can be found anywhere a moment later."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(d1))
            vo.wait_until("b")
            self.play(Write(d2))
            vo.wait_until("c")
            self.play(Write(d3))
            vo.wait_until("d")
            self.add(tl)
            self.play(Create(ax), FadeIn(wv), FadeIn(src), FadeIn(xl), FadeIn(hl), FadeIn(wheel))
            vo.wait_until("e")
            self.play(t.animate.set_value(0.35), run_time=2.0)
            self.play(t.animate.set_value(2.0), run_time=2.0)
        wv.clear_updaters()
        tl.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def screens(self):
        S = LEFT * 6.2
        Dp = RIGHT * 6.2

        def layout(holes_per, n_screens):
            xs = np.linspace(-6.2, 6.2, n_screens + 2)[1:-1]
            scr = VGroup()
            holes = []
            for xsc, nh in zip(xs, holes_per):
                ys = np.linspace(-2.2, 2.2, nh) if nh > 1 else np.array([0.0])
                holes.append([np.array([xsc, y, 0]) for y in ys])
                segs = np.concatenate([[-3.0], ys, [3.0]])
                for a, b in zip(segs[:-1], segs[1:]):
                    lo, hi = a + (0.12 if a > -3 else 0), b - (0.12 if b < 3 else 0)
                    if hi > lo:
                        scr.add(Line([xsc, lo, 0], [xsc, hi, 0], color=C.WALL, stroke_width=6))
            return scr, holes

        def all_paths(holes, limit=400, seed=0):
            r = np.random.default_rng(seed)
            g = VGroup()
            idx = [[]]
            for hs in holes:
                idx = [p + [h] for p in idx for h in range(len(hs))]
            if len(idx) > limit:
                idx = [idx[i] for i in r.choice(len(idx), limit, replace=False)]
            for p in idx:
                pts = [S] + [holes[k][h] for k, h in enumerate(p)] + [Dp]
                g.add(VMobject(stroke_color=hue(r.uniform(0, 2 * np.pi)), stroke_width=1.6).set_points_as_corners(pts).set_stroke(opacity=0.7))
            return g, len(idx)

        ends = VGroup(Dot(S, color=WHITE), Dot(Dp, color=C.BORN))
        el = VGroup(label(r"source", font_size=22, color=GREY_B).next_to(S, DOWN), label(r"detector", font_size=22, color=GREY_B).next_to(Dp, DOWN))
        configs = [([2], 1), ([3], 1), ([3, 3], 2), ([5, 4, 5], 3), ([7, 7, 7, 7], 4)]
        stages = []
        for k, (hp, ns) in enumerate(configs):
            scr, holes = layout(hp, ns)
            pths, n = all_paths(holes, seed=k)
            cnt = MathTex(r"\text{paths: }" + str(int(np.prod(hp))), font_size=30).to_edge(UP, buff=0.4)
            stages.append((scr, pths, cnt))
        fh = note(r"after Feynman \& Hibbs, \emph{Quantum Mechanics and Path Integrals} (1965), ch.\ 1; schematic").to_edge(DOWN, buff=0.25)
        final = label(r"no screens left: \emph{every} path from source to detector", font_size=32, color=C.ACTION).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Feynman's way of thinking about K starts with the double slit. <bookmark mark='a'/> Add a third slit: three "
            "paths. <bookmark mark='b'/> Add a second screen with its own slits: the amplitude is a sum over every way "
            "through both. <bookmark mark='c'/> Keep adding screens and drilling holes, <bookmark mark='d'/> until "
            "there's nothing left of the screens. Now the amplitude is a sum over every path from source to detector."
        ) as vo:
            scr, pths, cnt = stages[0]
            self.play(FadeIn(ends), FadeIn(el), FadeIn(scr), FadeIn(pths), FadeIn(cnt), FadeIn(fh))
            cur = stages[0]
            for m, k in zip("abc", (1, 2, 3)):
                vo.wait_until(m)
                nxt = stages[k]
                self.play(FadeOut(cur[0]), FadeOut(cur[1]), FadeOut(cur[2]), FadeIn(nxt[0]), FadeIn(nxt[1]), FadeIn(nxt[2]), run_time=1.2)
                cur = nxt
            self.play(FadeOut(cur[0]), FadeOut(cur[1]), FadeOut(cur[2]), FadeIn(stages[4][0]), FadeIn(stages[4][1]), FadeIn(stages[4][2]))
            cur = stages[4]
            vo.wait_until("d")
            self.play(FadeOut(cur[0]), FadeOut(cur[2]), FadeIn(final), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def slicing_picture(self):
        N = 8
        ax = plain_axes((0, N), (-3, 3), 9.0, 4.6).move_to(DOWN * 0.4 + LEFT * 0.6)
        tl = MathTex("t", font_size=30, color=C.QTIME).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        xl = MathTex("x", font_size=30, color=C.XPOS).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        slices = VGroup(*[DashedLine(ax.c2p(k, -3), ax.c2p(k, 3), color=GREY_D, stroke_width=1.5) for k in range(1, N)])
        tks = VGroup(*[MathTex(f"t_{k}", font_size=22, color=C.QTIME).next_to(ax.c2p(k, -3), DOWN, buff=0.1) for k in range(0, N + 1)])
        xa, xb = -1.6, 1.4
        ea, eb = Dot(ax.c2p(0, xa), color=WHITE), Dot(ax.c2p(N, xb), color=C.BORN)
        la = MathTex(r"x_a", font_size=28).next_to(ea, LEFT, buff=0.1)
        lb = MathTex(r"x_b", font_size=28, color=C.BORN).next_to(eb, RIGHT, buff=0.1)
        r = np.random.default_rng(3)

        def zig(seed):
            rr = np.random.default_rng(seed)
            ys = [xa] + list(np.clip(np.linspace(xa, xb, N + 1)[1:-1] + rr.normal(0, 1.0, N - 1), -2.8, 2.8)) + [xb]
            return ys

        one = zig(11)
        path1 = VMobject(stroke_color=C.ACTION, stroke_width=4).set_points_as_corners([ax.c2p(k, y) for k, y in enumerate(one)])
        vtx = VGroup(*[Dot(ax.c2p(k, y), radius=0.06, color=C.ACTION) for k, y in enumerate(one[1:-1], start=1)])
        vl = VGroup(*[MathTex(f"x_{k}", font_size=22, color=C.ACTION).next_to(d, UP, buff=0.06) for k, d in enumerate(vtx, start=1)])
        many = VGroup(*[VMobject(stroke_color=hue(r.uniform(0, 2 * np.pi)), stroke_width=1.5).set_points_as_corners(
            [ax.c2p(k, y) for k, y in enumerate(zig(100 + s))]).set_stroke(opacity=0.55) for s in range(60)])
        eps = BraceBetweenPoints(ax.c2p(3, 3), ax.c2p(4, 3), direction=UP, color=C.QTIME)
        epl = MathTex(r"\epsilon", font_size=30, color=C.QTIME).next_to(eps, UP, buff=0.05)
        cap = MathTex(r"\hat U(T) = \hat U(\epsilon)^N", r",\quad", r"T = N\epsilon", font_size=36).to_edge(UP, buff=0.3).shift(RIGHT * 2.5)
        with self.voiceover(
            "Here's the same idea as mathematics. <bookmark mark='a'/> Cut the time into N short steps of length "
            "epsilon, so the evolution is U of epsilon, applied N times. <bookmark mark='b'/> At each intermediate time, "
            "the particle could be anywhere: x 1, x 2, and so on. <bookmark mark='c'/> One choice of all of them is a "
            "zigzag path; every choice is a different zigzag."
        ) as vo:
            self.play(Create(ax), FadeIn(tl), FadeIn(xl), FadeIn(ea), FadeIn(eb), FadeIn(la), FadeIn(lb))
            vo.wait_until("a")
            self.play(Create(slices), FadeIn(tks), FadeIn(eps), FadeIn(epl), Write(cap))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in vtx], lag_ratio=0.1), FadeIn(vl))
            self.play(Create(path1))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(m) for m in many], lag_ratio=0.03), run_time=3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derivation(self):
        rows = [
            MathTex(r"K", r"=", r"\bra{x_b}\hat U(\epsilon)\cdots\hat U(\epsilon)\ket{x_a}", font_size=36),
            MathTex(r"K", r"=", r"\int dx_1\cdots dx_{N-1}\;\prod_{k=0}^{N-1}\bra{x_{k+1}}\hat U(\epsilon)\ket{x_k}", font_size=36),
            MathTex(r"\bra{x'}\hat U(\epsilon)\ket{x}", r"\approx", r"\sqrt{\frac{m}{2\pi i\hbar\epsilon}}\,\exp\Big[\frac{i\epsilon}{\hbar}\Big(\frac m2\Big(\frac{x' - x}{\epsilon}\Big)^2 - V(x)\Big)\Big]",
                    font_size=34),
            MathTex(r"\bra{x'}\hat U(\epsilon)\ket{x}", r"\approx", r"A\;e^{\,i\epsilon L/\hbar}", font_size=36),
            MathTex(r"K", r"=", r"\int\mathcal D x\; e^{\,iS[x]/\hbar}", r",\qquad S = \int_0^T L\,dt", font_size=46),
        ]
        rows[3][2].set_color(C.ACTION)
        rows[4][2].set_color(C.ACTION)
        whys = [
            why(rows[0], r"$N$ short steps"),
            why(rows[1], r"insert $1 = \int\ket{x}\bra{x}dx$ between the factors"),
            why(rows[2], r"one short step: free motion times the potential's phase"),
            why(rows[3], r"the exponent is $\epsilon$ times the Lagrangian $L = \tfrac m2\dot x^2 - V$"),
            why(rows[4], r"$N$ factors multiply: the exponents add up to the action of the zigzag"),
        ]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-2.6, buff=0.5)
        hist = note(r"Dirac (1933): $e^{iS/\hbar}$ ``corresponds to'' the short-time kernel; Feynman (1948): the whole of quantum mechanics").to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Write the propagator as N short evolutions. <bookmark mark='b'/> Between each pair of "
            "factors, insert a complete set of positions: one integral over x k for each intermediate time. "
            "<bookmark mark='c'/> For one short step, the propagator is the free one times a phase from the potential, "
            "<bookmark mark='d'/> and its exponent is i epsilon over h-bar times the kinetic minus the potential "
            "energy: the Lagrangian."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        with self.voiceover(
            "<bookmark mark='a'/> Multiply N of these together and the exponents add up to i over h-bar times the action "
            "of the zigzag path through all the x k. Integrating over every x k means adding up every zigzag. In the "
            "limit, K is the integral over all paths of e to the i S over h-bar. <bookmark mark='b'/> Dirac noticed in "
            "1933 that e to the i S over h-bar plays this role; Feynman, in 1948, showed it is all of quantum mechanics."
        ) as vo:
            vo.wait_until("a")
            step(4)
            self.play(Create(SurroundingRectangle(rows[4], color=C.ACTION, buff=0.18, corner_radius=0.12)))
            vo.wait_until("b")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def imaginary_time(self):
        p = load("pathint")
        x, E0, eps = p["x"], p["E0"], p["eps"]
        wick = MathTex(r"t = -i\tau", r":\quad", r"e^{\,iS/\hbar}", r"\;\to\;", r"e^{-S_E/\hbar}", r",\quad", r"S_E = \int\Big(\frac m2\dot x^2 + V\Big)d\tau",
                       font_size=34).to_edge(UP, buff=0.3)
        wick[4].set_color(C.ACTION)
        bm = label(r"positive weights: the paths become Brownian motion (Feynman--Kac, 1949)", font_size=24, color=GREY_A).next_to(wick, DOWN, buff=0.15)
        # the short-time kernel of the oscillator, as a matrix
        sel = slice(80, 481, 2)
        xx = x[sel]
        Kimg = np.sqrt(1 / (2 * np.pi * 0.25)) * np.exp(-((xx[:, None] - xx[None, :]) ** 2) / (2 * 0.25) - 0.25 * (0.25 * (xx[:, None] ** 2 + xx[None, :] ** 2)))
        km = gold_img(Kimg[::-1], height=2.9, width=2.9, gamma=0.5).move_to(LEFT * 4.6 + DOWN * 0.9)
        kl = MathTex(r"K_\epsilon(x, x')", font_size=28, color=C.BORN).next_to(km, UP, buff=0.12)
        kn = note(r"oscillator, $\epsilon = 0.25$, $x, x' \in [-5, 5]$").next_to(km, DOWN, buff=0.12)
        # relaxation onto the ground state
        ax = plain_axes((-5, 5), (0, 1.0), 4.6, 2.6).move_to(RIGHT * 0.4 + DOWN * 0.9)
        taus, snaps = p["relax_tau"], p["relax"]
        k = ValueTracker(0)
        cur = always_redraw(lambda: polyline(ax, x, snaps[int(round(k.get_value()))], color=C.BORN, stroke_width=3.5))
        gs = polyline(ax, x, p["ground"], color=WHITE, stroke_width=2).set_stroke(opacity=0.5)
        tl = always_redraw(lambda: MathTex(r"\tau = " + f"{taus[int(round(k.get_value()))]:g}", font_size=28, color=C.QTIME).next_to(ax, UP, buff=0.05))
        rl = label(r"apply $K_\epsilon$ again and again", font_size=22, color=GREY_B).next_to(ax, DOWN, buff=0.12)
        rows = [[f"{e:g}", f"{v:.5f}"] for e, v in zip(eps, E0)]
        tab = num_table([r"\epsilon", r"E_0\ \text{estimate}"], rows, font_size=28, col_colors=[C.QTIME, C.ENERGY]).move_to(RIGHT * 5.1 + DOWN * 0.9)
        exact = MathTex(r"\to \tfrac12\hbar\omega", font_size=30, color=C.ENERGY).next_to(tab, DOWN, buff=0.2)
        with self.voiceover(
            "Can we actually do this sum? In real time the arrows spin so fast that sampling paths is hopeless. "
            "<bookmark mark='a'/> But if we let time be imaginary, each path gets a positive weight, e to the minus the "
            "action, and the paths become Brownian motion, the subject of our stochastic calculus video. Then the sum is "
            "ordinary arithmetic. <bookmark mark='b'/> Here's the short-time kernel of the harmonic oscillator, as a "
            "matrix."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(wick), FadeIn(bm))
            vo.wait_until("b")
            self.play(FadeIn(km), FadeIn(kl), FadeIn(kn))
        with self.voiceover(
            "<bookmark mark='a'/> Multiply it by itself again and again: any starting shape relaxes onto the ground "
            "state, the Gaussian, <bookmark mark='b'/> and the rate at which it shrinks gives the ground-state energy. "
            "<bookmark mark='c'/> With epsilon equal to one, the estimate is 0.481; at 0.05 it's 0.49995. The error falls "
            "like epsilon squared, toward exactly one half."
        ) as vo:
            vo.wait_until("a")
            self.add(cur, tl)
            self.play(Create(ax), FadeIn(gs), FadeIn(cur), FadeIn(tl), FadeIn(rl))
            for i in range(1, len(taus)):
                self.play(k.animate.set_value(i), run_time=0.6, rate_func=lambda a: float(a >= 1))
                self.wait(0.15)
            vo.wait_until("c")
            assert abs(E0[1] - 0.481) < 6e-4 and abs(E0[-1] - 0.49995) < 1e-5
            self.play(FadeIn(tab.header), Create(tab.rule), LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.2), FadeIn(exact), run_time=2)
        for m in (cur, tl):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pimc(self):
        p = load("pathint")
        paths, beta = p["pimc_paths"], float(p["pimc_beta"])
        M = paths.shape[1]
        ax = plain_axes((0, beta), (-3, 3), 7.4, 4.8).move_to(LEFT * 2.6 + DOWN * 0.3)
        tl = MathTex(r"\tau", font_size=30, color=C.QTIME).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        xl = MathTex("x", font_size=30, color=C.XPOS).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        taus = np.linspace(0, beta, M + 1)
        r = np.random.default_rng(1)
        loops = VGroup()
        for pth in paths:
            ys = np.concatenate([pth, pth[:1]])
            loops.add(VMobject(stroke_color=hue(r.uniform(0, 2 * np.pi)), stroke_width=1.6).set_points_as_corners(
                [ax.c2p(t, y) for t, y in zip(taus, ys)]).set_stroke(opacity=0.75))
        hist, edges = p["pimc_hist"], p["pimc_edges"]
        # histogram bars drawn sideways: x vertical (matching the path plot), density to the right
        bars = VGroup()
        y0 = ax.c2p(0, 0)[1]
        sx = 3.4 / 0.65
        sy = (ax.c2p(0, 3)[1] - ax.c2p(0, -3)[1]) / 6
        base_x = 2.4
        for h, a, b in zip(hist, edges[:-1], edges[1:]):
            yc = y0 + sy * (a + b) / 2
            bars.add(Rectangle(width=max(h * sx, 1e-3), height=sy * (b - a) * 0.9, stroke_width=0, fill_color=C.BORN, fill_opacity=0.7)
                     .move_to([base_x + h * sx / 2, yc, 0]))
        xs = np.linspace(-3, 3, 300)
        g = np.exp(-xs**2 / (2 * float(p["pimc_x2_exact"]))) / np.sqrt(2 * np.pi * float(p["pimc_x2_exact"]))
        gc = VMobject(stroke_color=WHITE, stroke_width=3).set_points_as_corners([[base_x + v * sx, y0 + sy * xv, 0] for xv, v in zip(xs, g)])
        base = Line([base_x, y0 + sy * -3, 0], [base_x, y0 + sy * 3, 0], color=GREY_B, stroke_width=2)
        hl = label(r"where the paths spend their time", font_size=22, color=C.BORN).next_to(base, UP, buff=0.12).shift(RIGHT * 1.3)
        gl = MathTex(r"|\psi_0(x)|^2", font_size=28, color=WHITE).move_to([base_x + 2.6, y0 + sy * 1.6, 0])
        n = note(r"Metropolis sampling of closed paths, 100 time slices, $\hbar\omega\tau_{\max} = 10$; "
                 r"$\langle x^2\rangle = " + f"{float(p['pimc_x2']):.3f}" + r"$ vs.\ " + f"{float(p['pimc_x2_exact']):.3f}" + r" exactly").to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Or sample the paths themselves. <bookmark mark='a'/> Here are closed random paths in imaginary time, each "
            "drawn with its proper weight, each with a hundred time slices. <bookmark mark='b'/> Histogram where they "
            "spend their time, <bookmark mark='c'/> and you get the ground-state density, computed from nothing but a "
            "sum over paths."
        ) as vo:
            self.play(Create(ax), FadeIn(tl), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(m) for m in loops], lag_ratio=0.12), run_time=3)
            vo.wait_until("b")
            self.play(Create(base), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.01), FadeIn(hl), run_time=2)
            vo.wait_until("c")
            self.play(Create(gc), FadeIn(gl), FadeIn(n))
        self.wait(0.4)
        self.clear_scene()
