from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import (BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, SPOT, VAR, illustration, load, pause,
                                         real_data)


class RHeston(VoiceoverScene):
    def construct(self):
        rh = load("rheston")
        rs = load("rbskew")
        pr = load("rprofile")
        s = load("skew")
        self.card()
        self.memory(load("lift"))
        self.model()
        self.fit(rh, pr)
        self.skews(rh, rs, pr, s)

    def card(self):
        c = chapter_card(7, r"Rough Heston: the Volterra equation and its Riccati", r"Can a rough model keep a closed form?",
                         lit=(2019,), part=PART)
        with self.voiceover("Chapter seven. Rough Heston: the Volterra equation and its Riccati."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def memory(self, L):
        from scipy.special import gamma as G
        from explainer.quant.house import rough as R
        v0, lam, theta, nu, rho, _ = L["x"]
        T, n = 0.5, 500
        dW = np.random.default_rng(11).standard_normal((1, n)) * np.sqrt(T / n)
        t = np.linspace(0, T, n + 1)
        V = {}
        vh = np.empty(n + 1)
        vh[0] = v0
        for k in range(n):  # Heston (H = 1/2): the kernel is the constant 1
            vp = max(vh[k], 0.0)
            vh[k + 1] = vh[k] + lam * (theta - vp) * T / n + nu * np.sqrt(vp) * dW[0, k]
        V[0.5] = vh
        for H in (0.3, 0.1):
            V[H] = R.lifted_heston_paths(v0, lam, theta, nu, H, 20, T, n, dW)[0]
        lo, hi = 0.0, 1.0
        g = axes([0, 1], [0, 3.0], x_length=4.6, y_length=3.2, xlabel=r"lag $\tau$ (years)", ylabel=r"memory kernel $K(\tau)$",
                 xticks=[0, 0.5, 1], yticks=[0, 1, 2, 3], font_size=14).to_corner(UL, buff=0.5).shift(DOWN * 0.4)
        g2 = axes([0, 0.5], [lo, hi], x_length=7.0, y_length=3.2, xlabel=r"years", ylabel=r"variance $V_t$",
                  xticks=[0, 0.25, 0.5], yticks=[0, 0.5, 1.0], font_size=14).to_corner(UR, buff=0.5).shift(DOWN * 0.4)
        tau = np.linspace(1e-3, 1, 200)

        def kern(H):
            a = H + 0.5
            return curve(g.ax, tau, np.clip(tau ** (a - 1) / G(a), 0, 3.0), ROUGH if H < 0.5 else VAR, stroke_width=3)

        k_ = kern(0.5)
        p_ = curve(g2.ax, t, np.clip(V[0.5], lo, hi), VAR, stroke_width=1.8)
        lab_ = MathTex(r"H = \tfrac12\ \text{(Heston)}", font_size=30, color=VAR).next_to(g, DOWN, buff=0.4)
        eq = MathTex(r"V_t = V_0 + \int_0^t K(t - s)\big[\lambda(\theta - V_s)\,ds + \nu\sqrt{V_s}\,dW_s\big]",
                     font_size=34).to_edge(DOWN, buff=0.5)
        src = illustration(r"one path, the same shocks for every kernel; rough kernels by the lift of chapter 10 ($N = 20$)",
                           corner=DR).shift(UP * 0.0)
        with self.voiceover(
            "Rough Bergomi has no closed form. Omar El Euch and Mathieu Rosenbaum found a rough model that keeps "
            "Heston's gift, and the way in is to write Heston's variance differently: today's value equals the "
            "starting value plus the memory of every past push, the mean-reverting drift and the random shocks, "
            "each weighted by a kernel. <bookmark mark='a'/> For Heston the kernel is a constant: every push is "
            "remembered fully. Here is a variance path driven by one set of shocks. <bookmark mark='b'/> Now change "
            "only the kernel, to a power law with H of three-tenths, then a tenth: recent pushes count enormously, "
            "old ones fade. Same shocks, and the path turns jagged. That is rough Heston."
        ) as vo:
            self.play(FadeIn(g), FadeIn(g2), Create(k_), Create(p_), FadeIn(lab_), FadeIn(eq), FadeIn(src))
            vo.wait_until("a")
            self.play(Indicate(k_, color=YELLOW))
            vo.wait_until("b")
            for H in (0.3, 0.1):
                self.play(Transform(k_, kern(H)), Transform(p_, curve(g2.ax, t, np.clip(V[H], lo, hi), ROUGH, stroke_width=1.8)),
                          Transform(lab_, MathTex(rf"H = {H:g}", font_size=30, color=ROUGH).next_to(g, DOWN, buff=0.4)),
                          run_time=2)
                self.wait(0.6)
        self.wait(0.4)
        self.clear_scene()

    def model(self):
        rows = [cmath(r"V_t", r"=", r"V_0 + \frac{1}{\Gamma(\alpha)}\int_0^t (t - s)^{\alpha - 1}\Big(\lambda(\theta - V_s)\,ds"
                      r" + \nu\sqrt{V_s}\,dW_s\Big)", font_size=32, colors={r"V_t": VAR}),
                cmath(r"\log\mathbb{E}\,e^{iuX_T}", r"=", r"\int_0^T F\big(u, h(T - s)\big)\,g_0(s)\,ds,\quad g_0(t) = V_0 + "
                      r"\lambda\theta\!\int_0^t\! K", font_size=32, colors={r"\log\mathbb{E}\,e^{iuX_T}": OPT}),
                cmath(r"D^\alpha h", r"=", r"-\tfrac12(u^2 + iu) + (i\rho\nu u - \lambda)\,h + \tfrac12\nu^2 h^2",
                      font_size=36, colors={r"D^\alpha h": ROUGH}),
                cmath(r"\mathbb{E}\,e^{iuX_T}", r"=", r"\exp\!\Big(\theta\lambda\,I^1 h(T) + V_0\,I^{1 - \alpha}h(T)\Big)",
                      font_size=34, colors={r"\mathbb{E}\,e^{iuX_T}": OPT}),
                cmath(r"\alpha = 1:\ D^1 h = h'", r"=", r"\text{Heston's Riccati equation}", font_size=34,
                      colors={r"\alpha = 1:\ D^1 h = h'": VAR})]
        whys = [why(r"Heston (Part 13) with the constant kernel replaced by the fractional one, $\alpha = H + \tfrac12$"),
                why(r"an affine Volterra process: the log characteristic function is linear in the initial curve $g_0$ "
                    r"(Abi Jaber, Larsson and Pulido 2019; \textit{Rough Volatility}, ch. 5)"),
                why(r"$h = K * F(u, h)$: convolution with $t^{\alpha - 1}/\Gamma(\alpha)$ is the fractional integral $I^\alpha$; "
                    r"its inverse, the fractional derivative $D^\alpha$, turns it into this fractional Riccati equation"),
                why(r"substitute $g_0$ and integrate: El Euch and Rosenbaum (2019); no closed form for $h$, but one "
                    r"equation, for every $u$"),
                why(r"the consistency check the House's tests run: at $H = \tfrac12$ it is exactly Heston")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.9, buff=0.7, edge=6.9)
        q = pause(r"Set $H = \tfrac12$ in the fractional Riccati equation. What do you get?", width=6.0,
                  font_size=22).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Now the derivation. Rough Heston's variance is Heston's, with the constant kernel replaced by the "
            "fractional one, t to the alpha minus one over gamma of alpha, with alpha equal to H plus a half. "
            "<bookmark mark='a'/> It is an affine Volterra process, and for those, Eduardo Abi Jaber, Martin "
            "Larsson and Sergio Pulido showed, the log characteristic function is an integral of a function F of h "
            "against the initial curve g zero. <bookmark mark='b'/> h itself solves a convolution equation, and "
            "convolution with the fractional kernel is a fractional integral. Invert it: the fractional derivative "
            "of h equals Heston's own Riccati right-hand side. <bookmark mark='c'/> Substitute g zero, and the "
            "characteristic function is the exponential of two fractional integrals of h: El Euch and Rosenbaum's "
            "formula. No closed form for h, but one equation, solved once for every frequency. "
            "<bookmark mark='d'/> Pause and predict: set H to one half. What do you get? <bookmark mark='e'/> Alpha "
            "is one, the fractional derivative is the ordinary one, and this is Heston's Riccati equation. The "
            "House's tests check exactly that."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("e")
            self.play(FadeOut(q))
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def fit(self, rh, pr):
        p = rh["params"]
        r1 = next(r for r in pr["rows"] if abs(r["H"] - 0.1) < 1e-9)
        x1 = r1["x"]
        hdr = VGroup(VectorizedPoint(), label(r"left free", font_size=22, color=MODEL_COL["rough Heston"]),
                     label(r"$H$ held at 0.1", font_size=22, color=ROUGH)).arrange(RIGHT, buff=1.2)
        rows = [(r"H", f"{p['H']:.2f}", "0.10"), (r"\nu\ \text{(vol of vol)}", f"{p['nu']:.1f}", f"{x1[3]:.1f}"),
                (r"\lambda\ \text{(mean reversion)}", f"{p['lambda']:.1f}", f"{x1[1]:.1f}"),
                (r"\rho", f"{p['rho']:.2f}", f"{x1[4]:.2f}"),
                (r"\text{error (vol points)}", f"{rh['rmse']:.2f}", f"{r1['rmse']:.2f}")]
        tab = VGroup()
        for name, a_, b_ in rows:
            tab.add(VGroup(MathTex(name, font_size=28, color=GREY_A), MathTex(a_, font_size=30), MathTex(b_, font_size=30)))
        tab.arrange(DOWN, buff=0.28)
        for row in tab:
            row[0].set_x(-3.4)
            row[1].set_x(hdr[1].get_x() - 0.2 + 0.2)
            row[2].set_x(hdr[2].get_x())
        grid = VGroup(hdr, tab).arrange(DOWN, buff=0.35)
        for row in tab:
            row[0].set_x(-3.4)
            row[1].set_x(hdr[1].get_x())
            row[2].set_x(hdr[2].get_x())
        grid.move_to(UP * 0.5)
        note_ = wrapped_label(r"left free, the model drifts back toward Heston and buys its fit with Heston's absurd numbers; "
                              r"held rough, it fits almost as well with a sensible vol of vol and mean reversion. On this "
                              r"day's quotes the data cannot tell the two apart: vega weighting favours the long expiries, "
                              r"where roughness matters least", 11.5, 20, GREY_A).to_edge(DOWN, buff=0.6)
        src = real_data(r"the Surface, 10 December 2025; fractional Adams (80 steps) and COS, least squares")
        with self.voiceover(
            "Fit it to the Surface with all six numbers free, and something unexpected happens. The roughness comes "
            f"out at {p['H']:.2f}, barely rough, with a vol of vol of {p['nu']:.1f} and mean reversion of "
            f"{p['lambda']:.0f}: Heston's absurd numbers again. The error is {rh['rmse']:.2f} volatility points. "
            "<bookmark mark='a'/> Now hold H at a tenth, as the time series suggested, and refit the rest. The error "
            f"rises only to {r1['rmse']:.2f}, and the other parameters become sensible: a vol of vol of {x1[3]:.1f} "
            f"and mean reversion of {x1[1]:.0f}. <bookmark mark='b'/> On this day's quotes the data cannot tell the "
            "two apart: vega weighting favours the long expiries, where roughness matters least. The next chapter measures how much the "
            "Surface cares about H, and chapter eleven takes up the debate."
        ) as vo:
            self.play(FadeIn(hdr[1]), FadeIn(src), FadeIn(VGroup(*[VGroup(r_[0], r_[1]) for r_ in tab])))
            vo.wait_until("a")
            self.play(FadeIn(hdr[2]), FadeIn(VGroup(*[r_[2] for r_ in tab])))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def skews(self, rh, rs, pr, s):
        T = np.asarray(s["T"])
        y = np.asarray(s["skew"])
        g = axes([np.log10(2 / 365), 0], [-1.6, 0.6], x_length=7.0, y_length=4.4, xlabel=r"years to expiry (log scale)",
                 ylabel=r"at-the-money skew $|\partial_k\sigma|$ (log scale)",
                 xticks=[np.log10(x) for x in (3 / 365, 10 / 365, 30 / 365, 0.25, 1.0)],
                 xfmt=lambda u: {0: "1y"}.get(round(u, 3), f"{365 * 10 ** u:.0f}d"), log_x=True, font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        for v in (0.05, 0.1, 0.3, 1, 3):
            g.add(label(f"{v:g}", font_size=15, color=GREY_B).next_to(ax.c2p(np.log10(2 / 365), np.log10(v)), LEFT, buff=0.12))
        dots = VGroup(*[Dot(ax.c2p(np.log10(a), np.log10(b)), radius=0.07, color=WHITE) for a, b in zip(T, y) if b > 0.02])
        r1 = next(r for r in pr["rows"] if abs(r["H"] - 0.1) < 1e-9)
        series = (("rBergomi", rs["skew_T"], rs["skew"], MODEL_COL["rBergomi"]),
                  ("free", rh["skew_T"], rh["skew"], MODEL_COL["rough Heston"]),
                  ("H01", pr["skew_T"], r1["skew"], ROUGH))
        curves = VGroup()
        for _, tt, sk, col in series:
            tt, sk = np.asarray(tt), np.abs(np.asarray(sk))
            ok = sk > 1e-3
            curves.add(curve(ax, np.log10(tt[ok]), np.clip(np.log10(sk[ok]), -1.6, 0.6), col, stroke_width=3))
        leg = legend([(WHITE, r"the Surface"),
                      (MODEL_COL["rBergomi"], rf"rough Bergomi, $H = {load('rbergomi')['params']['H']:.2f}$"),
                      (MODEL_COL["rough Heston"], rf"rough Heston, free: $H = {rh['params']['H']:.2f}$"),
                      (ROUGH, r"rough Heston, $H = 0.1$")], font_size=17)
        leg.next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        side = wrapped_label(r"rough Bergomi, with its market variance curve, follows the quotes from 4 days to 200 but misses "
                             r"the 3-day point; both rough Hestons are steep enough for that point and overshoot the days "
                             r"just after it",
                             4.0, 19, GREY_A).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        with self.voiceover(
            "Now the test that motivated all this: the skew against maturity. Here are the Surface's expiries. "
            "<bookmark mark='a'/> Rough Bergomi, carrying the market's own variance curve, follows them from four "
            "days out to two hundred, though it misses the three-day point. <bookmark mark='b'/> Both versions of "
            "rough Heston are steep enough to reach that point, and overshoot the days just after it. No single model "
            "here gets every expiry. The rough kernel bends the curve the right way; the market's variance curve does "
            "much of the rest."
            " Next: solving its Riccati equation, step by step."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg[0]), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(leg[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(curves[1]), FadeIn(leg[2]), Create(curves[2]), FadeIn(leg[3]), FadeIn(side), run_time=3)
        self.wait(0.4)
        self.clear_scene()
