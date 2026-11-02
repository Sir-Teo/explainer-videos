from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, SPOT, VAR, load, real_data


class RHeston(VoiceoverScene):
    def construct(self):
        rh = load("rheston")
        rb = load("rbergomi")
        s = load("skew")
        self.card()
        self.model()
        self.fit(rh)
        self.skews(rh, rb, s)

    def card(self):
        c = chapter_card(4, r"Rough Heston", r"Can a rough model keep a closed form?", part=PART)
        with self.voiceover("Chapter four. Rough Heston."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"v_t", r"=", r"v_0 + \frac{1}{\Gamma(\alpha)}\int_0^t (t - s)^{\alpha - 1}\Big(\lambda(\theta - v_s)\,ds"
                      r" + \nu\sqrt{v_s}\,dW_s\Big)", font_size=32, colors={r"v_t": VAR}),
                cmath(r"\mathbb{E}\,e^{iu\ln S_T/F}", r"=", r"\exp\!\Big(\theta\lambda\,I^1 h(T) + v_0\,I^{1 - \alpha}h(T)\Big)",
                      font_size=34, colors={r"\mathbb{E}\,e^{iu\ln S_T/F}": OPT}),
                cmath(r"D^\alpha h", r"=", r"-\tfrac12(u^2 + iu) + (i\rho\nu u - \lambda)\,h + \tfrac12\nu^2 h^2", font_size=34,
                      colors={r"D^\alpha h": ROUGH})]
        whys = [why(r"Heston's variance (Part 13), with its memory replaced by the rough kernel, $\alpha = H + \tfrac12$"),
                why(r"El Euch and Rosenbaum (2019): the characteristic function survives, through fractional integrals "
                    r"$I^\beta$ of one function $h$"),
                why(r"$h$ solves Heston's Riccati equation with a fractional derivative; Diethelm's Adams scheme solves "
                    r"it in milliseconds, and COS prices follow")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-1.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "Omar El Euch and Mathieu Rosenbaum found a rough model that keeps Heston's gift. Write Heston's variance "
            "as an integral over its past, and replace the memory with the rough kernel. <bookmark mark='a'/> The "
            "characteristic function survives: it is built from fractional integrals of a single function h. "
            "<bookmark mark='b'/> And h solves Heston's own Riccati equation, with an ordinary derivative replaced by "
            "a fractional one. There is no closed form, but a fractional Adams scheme solves it in milliseconds, and "
            "Part thirteen's Fourier pricing does the rest. At H one half it is exactly Heston: the House's tests check "
            "that."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def fit(self, rh):
        p = rh["params"]
        tab = VGroup(
            MathTex(rf"H = {p['H']:.2f},\quad \nu = {p['nu']:.2f},\quad \rho = {p['rho']:.2f}", font_size=36,
                    color=MODEL_COL["rough Heston"]),
            MathTex(rf"\sqrt{{v_0}} = {100 * np.sqrt(p['v0']):.0f}\%,\quad \sqrt{{\theta}} = {100 * np.sqrt(p['theta']):.0f}\%,"
                    rf"\quad \lambda = {p['lambda']:.1f}", font_size=32),
            MathTex(rf"\text{{error}}\ {rh['rmse']:.2f}\ \text{{vol points}}\ \ (\text{{{rh['n']} quotes}})", font_size=30),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        src = real_data(r"the Surface, 10 December 2025; fractional Adams (80 steps) and COS, least squares")
        with self.voiceover(
            "Fitted to the Surface, rough Heston finds a roughness of "
            f"{p['H']:.2f}, a vol of vol of {p['nu']:.1f}, and a correlation of {p['rho']:.2f}. <bookmark mark='a'/> "
            f"Its error is {rh['rmse']:.2f} volatility points, with six numbers and no variance curve to lean on."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
        self.wait(0.4)
        self.clear_scene()

    def skews(self, rh, rb, s):
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
        curves = VGroup()
        for name, d in (("rBergomi", rb), ("rough Heston", rh)):
            tt = np.asarray(d["skew_T"])
            sk = np.abs(np.asarray(d["skew"]))
            ok = sk > 1e-3
            curves.add(curve(ax, np.log10(tt[ok]), np.clip(np.log10(sk[ok]), -1.6, 0.6), MODEL_COL[name], stroke_width=3))
        leg = legend([(WHITE, r"the Surface"), (MODEL_COL["rBergomi"], rf"rough Bergomi, $H = {rb['params']['H']:.2f}$"),
                      (MODEL_COL["rough Heston"], rf"rough Heston, $H = {rh['params']['H']:.2f}$")], font_size=17)
        leg.next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        side = wrapped_label(r"both rough models produce a skew that keeps growing as expiry nears, as the market's does; "
                             r"Part 13's diffusions flattened, its jumps exploded", 4.0, 19, GREY_A).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        with self.voiceover(
            "Now the test that motivated all this: the skew against maturity. Here are the Surface's expiries. "
            "<bookmark mark='a'/> Rough Bergomi's skew, and rough Heston's, keep growing as expiry nears, the way the "
            "market's does. Part thirteen's diffusions flattened at the short end, and its jumps exploded. A rough "
            "kernel is the one ingredient that bends the curve the right way across all of these maturities."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg[0]), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(leg[1]), Create(curves[1]), FadeIn(leg[2]), FadeIn(side), run_time=3)
        self.wait(0.4)
        self.clear_scene()
