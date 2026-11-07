from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from explainer.quant.house import exotics as X
from videos.quant.quant15.common import BAD, BARRIER, DELTA, GOOD, OPT, PART, SPOT, illustration, load, axes, data_range


class Barriers(VoiceoverScene, ThreeDScene):
    def construct(self):
        b = load("barrier")
        bs_ = load("barrier_surface")
        self.card()
        self.fan()
        self.derive()
        self.lab(b)
        self.surface(bs_)

    def card(self):
        c = chapter_card(3, r"Barriers: reflection, the closed form, the PDE", r"What is an option worth if it can die "
                         r"on the way?", lit=(1973, 1991), part=PART)
        with self.voiceover("Chapter three. Barriers: the reflection principle, the closed form, and the equation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fan(self):
        """Many driftless paths: the ones that touch the barrier are mirrored after the touch, and the two
        histograms at the horizon (touched and ending above the level, against all paths ending below its mirror)
        fill to the same height."""
        g = np.random.default_rng(15)
        n, m = 120, 60
        t = np.linspace(0, 1, n + 1)
        W = np.vstack([np.zeros(m), np.cumsum(g.standard_normal((n, m)) * np.sqrt(1 / n), axis=0)])
        hb = -0.5
        g2 = np.random.default_rng(16)
        big = np.cumsum(g2.standard_normal((1000, 20000)) * np.sqrt(1 / 1000), axis=0)
        x = 0.0
        touched_above = big[-1][(np.minimum(big.min(axis=0), 0) <= hb) & (big[-1] >= x)]
        below_mirror = big[-1][big[-1] <= 2 * hb - x]
        yr = data_range(W, 2 * hb - W, touched_above, 2 * hb - below_mirror)
        ax = axes([0, 1], yr, x_length=6.0, y_length=4.8, xlabel=r"time", ylabel=r"Brownian motion",
                  xticks=[], yticks=[], font_size=16).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        a = ax.ax
        bar = DashedLine(a.c2p(0, hb), a.c2p(1, hb), stroke_color=BARRIER, stroke_width=3)
        paths, mirrors = VGroup(), VGroup()
        for j in range(m):
            hit = np.where(W[:, j] <= hb)[0]
            col = BAD if len(hit) else SPOT
            paths.add(curve(a, t, W[:, j], col, stroke_width=1.3).set_stroke(opacity=0.55))
            if len(hit):
                k = hit[0]
                mirrors.add(curve(a, t[k:], 2 * hb - W[k:, j], OPT, stroke_width=1.3).set_stroke(opacity=0.55))
        # the histogram at the horizon, from many more draws (the same law)
        n1, n2 = len(touched_above), len(below_mirror)
        gap = 100 * (1 - n1 / n2)
        hist1, edges = np.histogram(touched_above, bins=30, range=yr)
        hist2, _ = np.histogram(2 * hb - below_mirror, bins=30, range=yr)
        scale = max(hist1.max(), hist2.max(), 1)

        def count_bars(hist, color, opacity):
            bars = VGroup()
            x0 = a.get_right()[0] + 0.12
            for k, count in enumerate(hist):
                if count == 0:
                    continue
                width = 1.2 * count / scale
                y0, y1 = a.c2p(0, edges[k])[1], a.c2p(0, edges[k + 1])[1]
                bars.add(Rectangle(width=width, height=max(y1 - y0 - 0.01, 0.005), stroke_width=0,
                                   fill_color=color, fill_opacity=opacity).move_to([x0 + width / 2, (y0 + y1) / 2, 0]))
            return bars
        h1 = count_bars(hist1, BAD, 0.6)
        h2 = count_bars(hist2, OPT, 0.45)
        rows = VGroup(
            MathTex(r"P(m_T \le b,\ W_T \ge x) = P(W_T \le 2b - x)", font_size=28, color=OPT),
            wrapped_label(rf"of 20{{,}}000 paths on 1{{,}}000 steps, {n1} touched $b$ and ended above $x = 0$; {n2} "
                          r"ended below the mirror point $2b - x$", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)
        src = illustration(r"grid-reflection illustration; 60 paths; 20{,}000 histogram paths, common count scale; $b<0$")
        with self.voiceover(
            f"Sixty Brownian paths run to the horizon; those observed below the barrier turn red. <bookmark mark='a'/> Continuous Brownian reflection starts exactly at the first touch. Strong Markov symmetry makes the reflected path equally likely. Our drawing mirrors at the first grid crossing, which can overshoot, so it illustrates that theorem rather than implementing an exact continuous coupling. <bookmark mark='b'/> For b below zero and x at least b, the probability of touching b and finishing above x equals the probability of finishing below two b minus x. On twenty thousand thousand-step paths we count {n1} against {n2}, a shortfall of {gap:.0f} percent. Grid monitoring misses crossings; Monte Carlo fluctuation also contributes. The two histograms use the same count scale. The continuous identity supplies the killed Brownian density used for the barrier formula."
        ) as vo:
            self.play(FadeIn(ax), Create(bar), FadeIn(src))
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.03, run_time=4))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p) for p in mirrors], lag_ratio=0.05, run_time=3))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r_, LEFT) for r_ in h1], lag_ratio=0.02),
                      LaggedStart(*[GrowFromEdge(r_, LEFT) for r_ in h2], lag_ratio=0.02), FadeIn(rows), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"P(m_T \le b,\ W_T \ge x)", r"=", r"P(W_T \le 2b - x),\quad x \ge b", font_size=36,
                  colors={r"P(m_T \le b,\ W_T \ge x)": OPT}),
            cmath(r"f_{m, W}^{\nu}(b, x)", r"=", r"e^{\nu x - \nu^2 T/2}\, f_{m, W}^{0}(b, x)", font_size=36,
                  colors={r"f_{m, W}^{\nu}(b, x)": QC.Q}),
            cmath(r"DOC", r"=", r"C(S, K) - \Big(\frac{H}{S}\Big)^{2\lambda - 2} C\Big(\frac{H^2}{S}, K\Big),\quad "
                  r"\lambda = \frac{r - q}{\sigma^2} + \frac12", font_size=34, colors={r"DOC": OPT}),
            cmath(r"\partial_t V + \tfrac12\sigma^2 S^2 V_{SS} + (r - q) S V_S - rV", r"=", r"0,\quad V(H, t) = 0",
                  font_size=34, colors={r"\partial_t V + \tfrac12\sigma^2 S^2 V_{SS} + (r - q) S V_S - rV": GOOD}),
            cmath(r"\tilde V(S, t)", r"=", r"\Big(\frac{S}{H}\Big)^{2 - 2\lambda} V\Big(\frac{H^2}{S}, t\Big)\ "
                  r"\text{also solves it}", font_size=34, colors={r"\tilde V(S, t)": BARRIER}),
            cmath(r"DIC + DOC", r"=", r"C", font_size=38, colors={r"DIC + DOC": OPT}),
        ]
        whys = [why(r"reflection after the first touch: the strong Markov property and symmetry ($m_T$ the minimum)"),
                why(r"drift $\nu$ by Girsanov (Part 5): re-weight each driftless path by its density"),
                why(r"constant Black--Scholes coefficients; zero rebate, $S>H$, $K\ge H$; scaled log-return drift $\nu=(r-q)/\sigma-\sigma/2$"),
                why(r"the same price from the PDE side: Black--Scholes on $S > H$, killed on the barrier"),
                why(r"the method of images: subtract the image of the vanilla and the boundary condition holds; the "
                    r"image term is exactly the reflected vanilla"),
                why(r"in--out parity: on every path exactly one of the two is alive at expiry")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.2, buff=0.75, edge=6.9)
        with self.voiceover(
            "Reflection gives the joint law of the minimum and endpoint for driftless Brownian motion. <bookmark mark='a'/> Add a constant drift by its Girsanov density. Here the coordinate is log return divided by sigma, so its drift is r minus q over sigma, minus sigma over two. <bookmark mark='b'/> Integrating the killed density gives this vanilla-minus-image formula for a continuously monitored down-and-out call, with constant Black-Scholes coefficients, zero rebate, spot above H, and strike at least H. Below that strike domain a different formula is needed. <bookmark mark='c'/> The price solves Black-Scholes above the barrier with zero boundary value. <bookmark mark='d'/> The image transformation preserves this constant-coefficient PDE; subtraction imposes the boundary and the appropriate terminal payoff. <bookmark mark='e'/> With matching monitoring, rebate and other terms, the down-and-in plus down-and-out equals the vanilla pathwise."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
            step(5)
        self.wait(0.4)
        self.clear_scene()

    def lab(self, b):
        p = b["params"]
        card = lab_card(r"the down-and-out call", [
            "def down_out_call(S, K, H, T, sigma, r=0.0, q=0.0):",
            "    lam = (r - q + 0.5 * sigma ** 2) / sigma ** 2",
            "    y = np.log(H * H / (S * K)) / (sigma * np.sqrt(T)) \\",
            "        + lam * sigma * np.sqrt(T)",
            "    din = (S * np.exp(-q * T) * (H / S) ** (2 * lam) * N(y)",
            "           - K * np.exp(-r * T) * (H / S) ** (2 * lam - 2)",
            "             * N(y - sigma * np.sqrt(T)))",
            "    out = bs.price(S, K, T, sigma, r, q, 1) - din",
            "    return np.where(S <= H, 0.0, out)",
        ], source="explainer/quant/house/exotics.py", width=7.6, font_size=17).to_corner(UL, buff=0.35)
        fine = b["rows"][-1]
        outs = [f"down_out_call({p['S']:.0f}, {p['K']:.0f}, {p['H']:.0f}, {p['T']}, {p['sigma']}, {p['r']})  ->  "
                f"{b['continuous']:.2f}",
                f"Monte Carlo, 100,000 paths, 20 steps a day: {fine['mc']:.2f} +/- {2 * fine['se']:.2f}",
                f"the vanilla: {b['vanilla']:.2f}"]
        pp = pause_card(r"A down-and-in call plus a down-and-out call with the same terms is worth\ldots?", width=4.8)
        pp.to_corner(UR, buff=0.35)
        with self.voiceover(
            "Here is that formula in the House's library: lambda, the reflected argument y, the down-and-in part, and the "
            "vanilla minus it. <bookmark mark='a'/> Run it on a six-month call, spot and strike "
            f"{p['S']:.0f}, barrier {p['H']:.0f}, twenty-five percent volatility: {b['continuous']:.2f}. A hundred thousand "
            f"paths give {fine['mc']:.2f}, within their noise; the vanilla is {b['vanilla']:.2f}. <bookmark mark='b'/> "
            "And a quick one for you: a down-and-in plus a down-and-out is worth the vanilla."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs, font_size=17)
            vo.wait_until("b")
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene()

    def surface(self, d):
        S = np.asarray(d["S"])
        tau = np.asarray(d["tau"])
        V = np.asarray(d["value"])
        D = np.asarray(d["delta"])
        fV = RegularGridInterpolator((tau, S), V, bounds_error=False, fill_value=None)
        fD = RegularGridInterpolator((tau, S), D, bounds_error=False, fill_value=None)
        H = d["H"]
        ax = ThreeDAxes(x_range=[80, 130, 10], y_range=[0, 0.5, 0.1], z_range=[0, 35, 10], x_length=7.0, y_length=4.6,
                        z_length=3.2, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                               "stroke_width": 2}).shift(DOWN * 0.5)
        zs = 35 / 1.2

        def val(u, w):
            return float(fV((max(w, 0.005), u))) if u > H else 0.0

        # both surfaces start at the barrier: a grid cell straddling it would draw a jagged step
        surf = Surface(lambda u, w: ax.c2p(u, w, val(u, w)), u_range=[H, 130], v_range=[0.005, 0.5],
                       resolution=(40, 18), fill_opacity=0.85, stroke_width=0.3, stroke_color=GREY_D)
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.DELTA, 0), (OPT, 12), ("#F7A8D8", 30)], axis=2)
        dsurf = Surface(lambda u, w: ax.c2p(u, w, zs * float(fD((max(w, 0.005), max(u, H + 0.05))))),
                        u_range=[H, 130], v_range=[0.005, 0.5], resolution=(40, 18), fill_opacity=0.8,
                        stroke_width=0.3, stroke_color=GREY_D)
        dsurf.set_fill_by_value(axes=ax, colorscale=[(SPOT, 0), (DELTA, 20), (BAD, 34)], axis=2)
        wall = Polygon(ax.c2p(H, 0, 0), ax.c2p(H, 0.5, 0), ax.c2p(H, 0.5, 30), ax.c2p(H, 0, 30), stroke_color=BARRIER,
                       stroke_width=2, fill_color=BARRIER, fill_opacity=0.25)
        hint = VGroup(label(r"spot, 80 to 130", font_size=21, color=SPOT),
                      label(r"time to expiry, 0.005 to 0.5 years", font_size=21, color=GREY_A),
                      label(r"value of the down-and-out call", font_size=21, color=OPT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.4)
        hint2 = label(r"delta: same height scale maps 0--1.2 units", font_size=21, color=DELTA).to_corner(UL, buff=0.4)
        wl = label(r"the barrier: $V = 0$ on the wall", font_size=20, color=BARRIER).to_corner(DR, buff=0.4)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-115 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, wl, hint2)
        self.remove(hint, wl, hint2)
        with self.voiceover(
            "Here is the price over spot and remaining time, from 0.005 years to six months. The near-expiry edge approaches the call payoff; it is not the exact expiry slice. <bookmark mark='a'/> For this zero-rebate contract the value is zero at the barrier. <bookmark mark='b'/> Replace price height by the numerical delta, without clipping it; the height scale now represents zero to 1.2 delta units. We interpolate a finite spot grid, so the slope at the absorbing boundary is a numerical approximation. Upon knock-out the position's remaining value and delta are zero. Contracts can be monitored continuously or at stated observation dates. Next, discrete monitoring and vanilla hedges."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), Create(surf), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(wall), FadeIn(wl))
            self.move_camera(theta=-150 * DEGREES, phi=70 * DEGREES, run_time=3)
            vo.wait_until("b")
            self.play(FadeOut(hint), FadeIn(hint2), ReplacementTransform(surf, dsurf), run_time=2)
            self.move_camera(theta=-80 * DEGREES, phi=62 * DEGREES, run_time=max(vo.remaining(1.0) - 1.0, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, dsurf, wall)), FadeOut(hint2),
                                                                  FadeOut(wl)], run_time=1.5)
        self.clear_scene(run_time=0.1)

