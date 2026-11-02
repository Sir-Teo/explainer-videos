from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, SPOT, VAR, load, real_data


class RHeston(VoiceoverScene):
    def construct(self):
        rh = load("rheston")
        rs = load("rbskew")
        pr = load("rprofile")
        s = load("skew")
        self.card()
        self.model()
        self.fit(rh, pr)
        self.skews(rh, rs, pr, s)

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
            "two apart. Vega weighting favours the long expiries, where roughness matters least, and a smooth model "
            "can imitate a rough one there by turning its own dials to extremes. Which to believe is the debate of "
            "chapter seven."
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
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg[0]), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(leg[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(curves[1]), FadeIn(leg[2]), Create(curves[2]), FadeIn(leg[3]), FadeIn(side), run_time=3)
        self.wait(0.4)
        self.clear_scene()
