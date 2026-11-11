from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import (BAD, IV, LV, OPT, PART, RV, SPOT, axes3, fixed, grid_fn, load, real_data,
                                         surf3)


class LocalVol(VoiceoverScene, ThreeDScene):
    def construct(self):
        b = load("bbf")
        t = load("dk_tree")
        self.card()
        self.surfaces(b)
        self.dupire()
        self.lab(b)
        self.bbf(b)
        self.tree(t)

    def card(self):
        c = chapter_card(6, r"Dupire's local volatility, derived", r"Which single diffusion reprices every option?",
                         lit=(1994,), part=PART)
        with self.voiceover("Chapter six. Dupire's local volatility, derived."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def surfaces(self, b):
        ks, Ts = np.asarray(b["ks"]), np.asarray(b["Ts"])
        imp, loc = np.asarray(b["imp"]), np.asarray(b["loc"])
        ax = axes3([-0.4, 0.4, 0.2], [0, 0.5, 0.1], [0.3, 1.3, 0.2], x_length=7.4, y_length=4.8, z_length=3.2)  # 7-day wings reach 1.27
        self.set_camera_orientation(phi=66 * DEGREES, theta=-58 * DEGREES, zoom=0.85)
        fi, fl = grid_fn(ks, Ts, imp), grid_fn(ks, Ts, loc)
        si = surf3(ax, fi, (-0.4, 0.4), (Ts[0], Ts[-1]), 0.3, 1.3, resolution=(20, 12), opacity=0.35)
        sl = surf3(ax, fl, (-0.4, 0.4), (Ts[0], Ts[-1]), 0.3, 1.3, colors=[(QC.IDEA, 0.35), (LV, 0.65), (QC.LOSS, 1.2)],
                   resolution=(20, 12), opacity=0.85)
        t1 = label(r"implied volatility (translucent)", font_size=22, color=IV).to_corner(UL, buff=0.35)
        t2 = label(r"local volatility, read from the implied surface's slopes", font_size=22, color=LV).next_to(t1, DOWN,
                                                                                                         aligned_edge=LEFT)
        src = real_data(r"the Surface's SSVI fit; Dupire by finite differences")
        fixed(self, t1, t2, src)
        with self.voiceover(
            "Can one model reprice every option on the surface at once? Let volatility depend only on the price and the date: a deterministic function sigma of S and t, evaluated at a random price. Here, translucent, is the Surface's implied volatility. <bookmark mark='a'/> And here, solid, is the local volatility that reproduces it, computed from its slopes. <bookmark mark='b'/> Drop the camera and look along the strikes: the local surface is steeper, roughly twice as steep as the implied one, and it bends hardest at the short end. Implied volatility is a price-based effective parameter, not a literal unconditional average of local volatility along paths."
        ) as vo:
            self.play(Create(ax), FadeIn(si), FadeIn(t1), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(sl), FadeIn(t2), run_time=2)
            vo.wait_until("b")
            self.move_camera(phi=88 * DEGREES, theta=-90 * DEGREES, zoom=0.7, run_time=3)  # clear of the captions
            self.wait(max(vo.remaining(0.5) - 0.5, 0.5))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, si, sl)), FadeOut(t1), FadeOut(t2),
                                                                  FadeOut(src)], run_time=1)
        self.clear()

    def dupire(self):
        rows = [cmath(r"dS = \sigma(S, t)\,S\,dW", r"\Rightarrow", r"\partial_T p = \tfrac12\,\partial_{KK}\big(\sigma^2 K^2 p\big)",
                      font_size=36, colors={r"dS = \sigma(S, t)\,S\,dW": SPOT}),
                cmath(r"\partial_T C", r"=", r"\tfrac12 \int (x - K)^+\,\partial_{xx}(\sigma^2 x^2 p)\,dx", font_size=36, colors={r"\partial_T C": OPT}),
                cmath(r"\partial_T C", r"=", r"\tfrac12\,\sigma^2(K, T)\,K^2\,p(K, T)", font_size=36,
                      colors={r"\partial_T C": OPT}),
                cmath(r"\sigma^2_{\text{loc}}(K, T)", r"=", r"\frac{\partial_T C}{\tfrac12 K^2\,\partial_{KK} C}", font_size=38,
                      colors={r"\sigma^2_{\text{loc}}(K, T)": LV}),
                cmath(r"\sigma^2_{\text{loc}}", r"=", r"\frac{\partial_T w}{g(k)}", font_size=40,
                      colors={r"\sigma^2_{\text{loc}}": LV}),
                cmath(r"\sigma_{\text{imp}}(k)", r"\approx", r"\Big(\frac1k\int_0^k \frac{du}{\sigma_{\text{loc}}(u)}\Big)^{-1}"
                      r"\ \Rightarrow\ \partial_k\sigma_{\text{imp}}(0) = \tfrac12\,\partial_k\sigma_{\text{loc}}(0)",
                      font_size=32, colors={r"\sigma_{\text{imp}}(k)": IV})]
        whys = [why(r"the Fokker--Planck equation for the density of $S_T$ (Part 5), zero rates"),
                why(r"differentiate the call price under the integral and substitute the Fokker--Planck equation"),
                why(r"integrate by parts twice: $\partial_{xx}(x - K)^+ = \delta(x - K)$, so only the density at the "
                    r"strike survives"),
                why(r"Dupire (1994): divide by Breeden and Litzenberger's $p = \partial_{KK}C$; one function, read off the "
                    r"surface"),
                why(r"change variables to $k$ and $w$ (Gatheral, eq.\ 1.10): Chapter 3's two conditions are exactly "
                    r"``local variance is real''"),
                why(r"Berestycki, Busca and Florent (2002): at short maturity implied vol is the harmonic mean of local "
                    r"vol along the straight line; differentiate at the money")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.6, buff=0.72, edge=6.9)
        with self.voiceover(
            "If the price diffuses with volatility sigma of S and t, its density obeys Part five's Fokker-Planck "
            "equation. <bookmark mark='a'/> Differentiate a call in maturity under the integral, <bookmark mark='a2'/> "
            "and integrate by parts twice: the payoff's second derivative is a spike at the strike, so only the density there survives. "
            "<bookmark mark='b'/> Divide by Part nine's density, the call's second strike derivative: Bruno Dupire's "
            "1994 formula. <bookmark mark='c'/> In total variance the denominator is Chapter three's g: the calendar and "
            "butterfly conditions are exactly the conditions for local variance to be positive. <bookmark mark='d'/> "
            "And at short maturity, Berestycki, Busca and Florent showed in 2002 that implied volatility is the "
            "harmonic average of local volatility from spot to strike: so the implied skew is half the local skew."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("a2")
            step(2)
            vo.wait_until("b")
            step(3)
            vo.wait_until("c")
            step(4)
            vo.wait_until("d")
            step(5)
        self.wait(0.4)
        self.clear_scene()

    def lab(self, b):
        card = lab_card(r"local variance from total variance", [
            "def g_function(k, w, dw, d2w):",
            "    return (1 - k * dw / (2 * w)) ** 2 - dw ** 2 / 4 * (1 / w + 0.25) + d2w / 2",
            "",
            "def dupire_local_var(k, w, dw, d2w, dwdT):",
            "    return np.asarray(dwdT, float) / g_function(k, w, dw, d2w)",
            "",
            "def numeric_derivs(f, k, T, h=1e-3, hT=1e-4):",
            "    w = f(k, T)",
            "    dw = (f(k + h, T) - f(k - h, T)) / (2 * h)",
            "    d2w = (f(k + h, T) - 2 * w + f(k - h, T)) / h ** 2",
            "    dT = (f(k, T + hT) - f(k, T - hT)) / (2 * hT)",
            "    return w, dw, d2w, dT",
        ], source="explainer/quant/house/volsurface.py", width=8.8).to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.5)
        L = b["lab"]
        out = [f"{d:>3} days:  g_min {L[d]['g_min']:.3f}   sigma_loc(0) {100 * L[d]['loc_atm']:.1f}%   "
               f"sigma_imp(0) {100 * L[d]['imp_atm']:.1f}%" for d in ("7", "30", "90")]
        g30 = L["30"]["g_min"]
        with self.voiceover(
            f"In the House it is three small functions. Gatheral's g, local variance as the time slope over g, and central differences to get the slopes from any total-variance function. <bookmark mark='a'/> Run on the Surface's SSVI at seven, thirty and ninety days. g stays well above zero, its smallest value at thirty days {g30:.2f}, so the tested local-variance grid is well defined; and at the money, local volatility sits a few points below implied, reflecting this fitted surface and its time and strike derivatives, rather than a universal level ordering."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, out)
        self.wait(0.6)
        self.clear_scene()

    def bbf(self, b):
        rows = b["rows"]
        g = axes([0, len(rows)], [0, 2.5], x_length=6.6, y_length=3.8, ylabel=r"local skew $/$ implied skew, at the money",
                 yticks=[0, 1, 2], font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        two = DashedLine(ax.c2p(0, 2), ax.c2p(len(rows), 2), color=GREY_B)
        twol = label(r"BBF: 2 as $T \to 0$", font_size=17, color=GREY_B).next_to(ax.c2p(len(rows), 2), UP, buff=0.05).shift(LEFT * 1.0)
        bars = VGroup(*[Rectangle(width=0.5, height=ax.c2p(0, r["ratio"])[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                  fill_color=LV, fill_opacity=0.85).move_to(ax.c2p(i + 0.5, r["ratio"] / 2))
                        for i, r in enumerate(rows)])
        vals = VGroup(*[label(f"{r['ratio']:.2f}", font_size=17).next_to(bars[i], UP, buff=0.06) for i, r in enumerate(rows)])
        ticks = VGroup(*[label(f"{r['days']:.0f}d", font_size=16, color=GREY_B).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.1)
                         for i, r in enumerate(rows)])
        lo, hi = min(r["ratio"] for r in rows), max(r["ratio"] for r in rows)
        r30 = [r for r in rows if abs(r["days"] - 30) < 1][0]
        side = VGroup(
            wrapped_label(r"pause and predict: implied skew at 30 days is "
                          rf"{r30['implied']:.3f} per unit of $k$. The local skew?", 4.4, 20, QC.HOUSE),
            MathTex(rf"\partial_k\sigma_{{\text{{loc}}}} = {r30['local']:.3f}", font_size=32, color=LV),
            wrapped_label(r"not exactly 2: BBF is a short-maturity statement, and the first-order average ignores the "
                          r"smile's curvature", 4.4, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(r"the Surface: Dupire from SSVI, slopes at $k = 0$")
        i30, l30 = r30["implied"], r30["local"]
        with self.voiceover(
            "Check the factor of two on the Surface. At each maturity, the local skew at the money divided by the "
            f"implied skew. <bookmark mark='a'/> It ranges from {lo:.2f} to {hi:.2f}: about two, not exactly two. "
            "The theorem is a short-maturity statement, and the straight-line average ignores the curvature of the "
            f"smile. Pause and predict: the implied skew at thirty days is {i30:.3f} per unit of log-moneyness. The "
            f"local skew? <bookmark mark='b'/> {l30:.3f}: nearly double."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(two), FadeIn(twol), FadeIn(ticks))
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in bars], lag_ratio=0.2, run_time=2))
            vo.wait_until("a")
            self.play(FadeIn(vals), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def tree(self, t):
        sm = t["small"]
        nodes = [np.asarray(x) for x in sm["nodes"]]
        lvs = [np.asarray(x) for x in sm["lv"]]
        N = len(nodes) - 1
        x0, dx = -5.6, 1.2
        log_span = max(max(float(np.max(np.abs(np.log(lev)))) for lev in nodes), 0.45 * np.sqrt(0.25 / N) * N)
        ylog = lambda s: 3.1 * np.log(s) / log_span  # noqa: E731
        lo_lv, hi_lv = 0.3, 0.8

        def col(v):
            return interpolate_color(ManimColor(QC.SPOT), ManimColor(BAD), float(np.clip((v - lo_lv) / (hi_lv - lo_lv), 0, 1)))
        pos = [[np.array([x0 + n * dx, float(ylog(s)), 0]) for s in lev] for n, lev in enumerate(nodes)]
        edges, dots = VGroup(), VGroup()
        for n in range(N):
            for i in range(len(nodes[n])):
                c = col(lvs[n][i]) if np.isfinite(lvs[n][i]) else GREY_C
                edges.add(Line(pos[n][i], pos[n + 1][i], color=c, stroke_width=3),
                          Line(pos[n][i], pos[n + 1][i + 1], color=c, stroke_width=3))
        for n in range(N + 1):
            for p_ in pos[n]:
                dots.add(Dot(p_, radius=0.06, color=WHITE))
        crr = VGroup()
        for n in range(N + 1):
            for j in range(n + 1):
                u = 0.45 * np.sqrt(0.25 / N)
                crr.add(Dot([x0 + n * dx, float(ylog(np.exp(u * (2 * j - n)))), 0], radius=0.04,
                            color=GREY_D))
        side = VGroup(
            label(r"Derman and Kani (1994): an implied tree", font_size=22, color=LV),
            wrapped_label('grey: evenly spaced comparison; white nodes target selected earlier-level option prices', 4.0, 18, GREY_A),
            wrapped_label(r"edges coloured by the node's local volatility, blue (low) to red (high): highest on the "
                          r"downside", 4.0, 18, GREY_A),
            wrapped_label(rf"40 steps over 91 days: maturity smile within {t['max_err']:.2f} vol points of the Surface "
                          rf"for $|k| \le 0.2$; node local vols within {t['lv_gap']:.1f} points of Dupire's (median)", 4.0,
                          18, QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        src = real_data(r"the Surface's SSVI; six steps drawn, forty computed")
        err, gap = t["max_err"], t["lv_gap"]
        with self.voiceover(
            f"""Derman and Kani's 1994 implied tree offers a discrete version. Grey nodes show an evenly spaced comparison. <bookmark mark='a'/> The implied nodes adjust to reprice calls or puts at selected earlier-level strikes. Their local branch-volatility colors are a display scale. <bookmark mark='b'/> With forty steps over three months, the near-money smile has RMSE {err:.2f} volatility points against the fitted Surface, and the median node-volatility difference from Dupire is {gap:.2f} points. These are finite numerical summaries, not uniform error bounds. The schematic now retains every node instead of collapsing its outer branches at a display boundary."""
        ) as vo:
            self.play(FadeIn(crr), FadeIn(src), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), LaggedStart(*[Create(e) for e in edges], lag_ratio=0.02, run_time=3), FadeIn(dots))
            self.play(FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
