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
        ax = axes([0, 1], [-2.6, 2.2], x_length=6.0, y_length=4.8, xlabel=r"time", ylabel=r"Brownian motion",
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
        g2 = np.random.default_rng(16)
        big = np.cumsum(g2.standard_normal((1000, 20000)) * np.sqrt(1 / 1000), axis=0)
        x = 0.0
        touched_above = big[-1][(np.minimum(big.min(axis=0), 0) <= hb) & (big[-1] >= x)]
        below_mirror = big[-1][big[-1] <= 2 * hb - x]
        n1, n2 = len(touched_above), len(below_mirror)
        gap = 100 * (1 - n1 / n2)
        h1 = side_density(a, touched_above, (-2.6, 2.2), bins=30, width=1.2, color=BAD, opacity=0.6)
        h2 = side_density(a, 2 * hb - below_mirror, (-2.6, 2.2), bins=30, width=1.2, color=OPT, opacity=0.45)
        rows = VGroup(
            MathTex(r"P(m_T \le b,\ W_T \ge x) = P(W_T \le 2b - x)", font_size=28, color=OPT),
            wrapped_label(rf"of 20{{,}}000 paths on 1{{,}}000 steps, {n1} touched $b$ and ended above $x = 0$; {n2} "
                          r"ended below the mirror point $2b - x$", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)
        src = illustration(r"60 Brownian paths drawn; the histograms from 20{,}000; $m_T$ the minimum, $b$ the barrier")
        with self.voiceover(
            "Sixty Brownian paths run to the horizon; those that touch the barrier turn red. <bookmark mark='a'/> After its first touch, each red path gets a mirror twin, reflected "
            "across the barrier. The twin is just as likely, because Brownian motion forgets its past and is "
            "symmetric. <bookmark mark='b'/> So on the right, the paths that touched and ended above any level x "
            "pile up like all the paths that ended below the mirror point, two b minus x. Counted on twenty "
            f"thousand simulated paths: {n1} against {n2}. The touched count is {gap:.0f} percent short, and not by "
            "chance: on a grid, some paths cross the barrier between two steps and come back unseen, the subject of "
            "chapter four. In continuous time the two are equal, and that identity gives the joint law of the "
            "minimum and the endpoint, and from it every barrier price."
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
                why(r"integrate the payoff against the killed density; in log price $\nu = (r - q)/\sigma - \sigma/2$"),
                why(r"the same price from the PDE side: Black--Scholes on $S > H$, killed on the barrier"),
                why(r"the method of images: subtract the image of the vanilla and the boundary condition holds; the "
                    r"image term is exactly the reflected vanilla"),
                why(r"in--out parity: on every path exactly one of the two is alive at expiry")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.2, buff=0.75, edge=6.9)
        with self.voiceover(
            "Now the derivation. Reflection gives the joint law of the minimum and the endpoint: touching b and ending "
            "above x is as likely as ending below two b minus x. <bookmark mark='a'/> Prices have drift, so re-weight "
            "each path by its Girsanov density, as in Part five. <bookmark mark='b'/> Integrate the call's payoff against "
            "this killed density: the vanilla, minus the vanilla seen from the mirrored spot, scaled by H over S to the "
            "power two lambda minus two. <bookmark mark='c'/> The same price solves Black–Scholes above the barrier, "
            "pinned to zero on it. <bookmark mark='d'/> The two views meet in the method of images: if V solves "
            "Black–Scholes, so does this reflection of it, and subtracting it makes the boundary condition hold. "
            "<bookmark mark='e'/> And a down-and-in plus a down-and-out is the vanilla: on every path exactly one is alive."
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
        dsurf = Surface(lambda u, w: ax.c2p(u, w, zs * float(np.clip(fD((max(w, 0.005), max(u, H + 0.05))), 0, 1.2))),
                        u_range=[H, 130], v_range=[0.005, 0.5], resolution=(40, 18), fill_opacity=0.8,
                        stroke_width=0.3, stroke_color=GREY_D)
        dsurf.set_fill_by_value(axes=ax, colorscale=[(SPOT, 0), (DELTA, 20), (BAD, 34)], axis=2)
        wall = Polygon(ax.c2p(H, 0, 0), ax.c2p(H, 0.5, 0), ax.c2p(H, 0.5, 30), ax.c2p(H, 0, 30), stroke_color=BARRIER,
                       stroke_width=2, fill_color=BARRIER, fill_opacity=0.25)
        hint = VGroup(label(r"spot, 80 to 130", font_size=21, color=SPOT),
                      label(r"time to expiry, 0 to six months", font_size=21, color=GREY_A),
                      label(r"value of the down-and-out call", font_size=21, color=OPT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.4)
        hint2 = label(r"now its delta: a ridge along the wall", font_size=21, color=DELTA).to_corner(UL, buff=0.4)
        wl = label(r"the barrier: $V = 0$ on the wall", font_size=20, color=BARRIER).to_corner(DR, buff=0.4)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-115 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, wl, hint2)
        self.remove(hint, wl, hint2)
        with self.voiceover(
            "Here is the whole price, over spot and time to expiry. At expiry, the front edge, it is the call's "
            "hockey stick, cut off at the barrier. Further from expiry it rises and smooths, like any call. "
            "<bookmark mark='a'/> But it is pinned to zero along the barrier, a wall it can never cross, and right "
            "next to the wall the surface climbs steeply. <bookmark mark='b'/> Swap the height for the slope, the "
            "delta. A vanilla's delta near this spot would be modest. The barrier's delta stands as a ridge along "
            "the wall: the option is worth almost nothing there, yet its hedge is large, and it falls to zero the "
            "instant the barrier is touched."
            " Real barriers are watched at the close, and there is a way to hedge them without trading. Next."
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
        self.clear_scene()

