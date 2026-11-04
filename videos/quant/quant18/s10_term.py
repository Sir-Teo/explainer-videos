from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import BAD, GOOD, PART, ZERO, ask, fit_right, house_lab, illustration, load

EXP = QC.SPOT
TP = QC.OPTION


class Term(VoiceoverScene):
    def construct(self):
        t = load("term")
        self.card()
        self.hypothesis()
        self.regressions(t)
        self.acm_method()
        self.decompose(t)

    def card(self):
        c = chapter_card(14, r"Expectations and the term premium", r"Is a long yield a forecast, or a price for risk?",
                         part=PART)
        with self.voiceover("Chapter fourteen. Expectations, and the term premium."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def hypothesis(self):
        rows = [cmath(r"y_t^{(n)}", r"=", r"\frac1n\sum_{k=0}^{n-1}\mathbb{E}_t\big[r_{t+k}\big] + \text{TP}_t^{(n)}",
                      font_size=42, colors={r"y_t^{(n)}": ZERO, r"\text{TP}_t^{(n)}": TP}),
                cmath(r"\text{TP} = \text{const}", r"\Rightarrow",
                      r"y_{t+1}^{(n-1)} - y_t^{(n)} = a + b\,\frac{y_t^{(n)} - y_t^{(1)}}{n - 1},\ \ b = 1",
                      font_size=36, colors={r"\Rightarrow": WHITE}),
                cmath(r"rx_{t+1}^{(n)}", r"=", r"a + b\,\big(f_t^{(n-1,n)} - y_t^{(1)}\big) + \varepsilon,\ \ b = 0",
                      font_size=38, colors={r"rx_{t+1}^{(n)}": GOOD})]
        whys = [why(r"a long yield is the average short rate expected over its life, plus a term premium: what investors "
                    r"charge for locking money up at a rate that may move"),
                why(r"the expectations hypothesis (premium constant): a steep curve means short rates will rise, so long "
                    r"yields rise too, one for one. Campbell and Shiller (1991)"),
                why(r"and excess returns of long bonds over one year are unpredictable: Fama and Bliss (1987)")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.2, buff=0.7, edge=6.9)
        with self.voiceover(
            "Why does the ten-year bond yield what it does? Split it in two: the average short rate the market expects over "
            "the next ten years, plus a term premium, what investors charge for tying up money at a rate that may turn "
            "out wrong. <bookmark mark='a'/> If that premium were constant, the expectations hypothesis, a steep curve "
            "would mean short rates are about to rise, and long yields would rise with them: in John Campbell and Robert "
            "Shiller's regression the slope coefficient would be one. <bookmark mark='b'/> And in Eugene Fama and "
            "Robert Bliss's regression, the extra return from holding long bonds for a year would be unpredictable: "
            "zero."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def regressions(self, t):
        cs, fb = t["cs"], t["fb"]
        ks = ["12", "24", "36", "60", "120"]
        g1 = axes([-0.5, 4.5], [-3, 1.5], x_length=5.4, y_length=3.8, ylabel=r"Campbell--Shiller slope",
                  xticks=list(range(5)), xfmt=lambda v: f"{int(ks[int(v)]) // 12}" + r"\,\text{y}", yticks=[-3, -2, -1, 0, 1],
                  font_size=13)
        g2 = axes([-0.5, 3.5], [-0.5, 2], x_length=4.4, y_length=3.8, ylabel=r"Fama--Bliss slope",
                  xticks=list(range(4)), xfmt=lambda v: f"{int(v) + 2}" + r"\,\text{y}", yticks=[0, 1, 2], font_size=13)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).shift(DOWN * 0.4)

        def bars(ax, vals, ses, col, ref):
            out = VGroup()
            for i, (v, se) in enumerate(zip(vals, ses)):
                p0, p1 = ax.c2p(i - 0.25, 0), ax.c2p(i + 0.25, v)
                out.add(VGroup(Rectangle(width=p1[0] - p0[0], height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0,
                                         fill_color=col, fill_opacity=0.8).move_to((p0 + p1) / 2),
                               Line(ax.c2p(i, v - 2 * se), ax.c2p(i, v + 2 * se), color=WHITE, stroke_width=2)))
            line = DashedLine(ax.c2p(-0.5, ref), ax.c2p(len(vals) - 0.5, ref), color=WHITE, stroke_width=2)
            return out, line
        b1, r1 = bars(g1.ax, [cs[k]["b"] for k in ks], [cs[k]["se"] for k in ks], BAD, 1.0)
        b2, r2 = bars(g2.ax, [fb[k]["b"] for k in ("2", "3", "4", "5")], [fb[k]["se"] for k in ("2", "3", "4", "5")],
                      GOOD, 0.0)
        l1 = label(r"dashed: the hypothesis says 1", font_size=16, color=GREY_B).next_to(g1, UP, buff=0.05)
        l2 = label(r"dashed: the hypothesis says 0", font_size=16, color=GREY_B).next_to(g2, UP, buff=0.05)
        foot = wrapped_label(rf"monthly, 1961--2025, from the Fed's curve; bars $\pm 2$ standard errors (Fama--Bliss: "
                             rf"Newey--West, 12 lags). At 10 years $b = {cs['120']['b']:.2f}$; Fama--Bliss $R^2$ "
                             rf"{100 * fb['2']['r2']:.0f}--{100 * fb['5']['r2']:.0f}\%", 12.0, 18, GREY_A).to_edge(DOWN,
                                                                                                         buff=0.35)
        with self.voiceover(
            "Both regressions, on sixty-four years of the Fed's curve. <bookmark mark='a'/> Campbell and Shiller: the "
            "slope should be one at every maturity. It is near zero at one year and falls to "
            f"{cs['120']['b']:.1f} at ten: when the curve is steep, long yields tend to fall, not rise. "
            "<bookmark mark='b'/> Fama and Bliss: the slope should be zero. It is close to one, with about a tenth of "
            "the variance explained: when forwards sit above the short rate, long bonds tend to earn more. Both say the "
            "same thing. The premium is not constant; it moves, and a steep curve is partly a high premium."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(l1), FadeIn(l2), Create(r1), Create(r2))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, UP) for b_ in b1], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b2], lag_ratio=0.2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def acm_method(self):
        from explainer.quant.house import rates as R
        rows = [cmath(r"X_{t+1}", r"=", r"\mu + \Phi X_t + v_{t+1}", font_size=40, colors={r"X_{t+1}": ZERO}),
                cmath(r"rx_{t+1}^{(n)}", r"=", r"a_n + \beta_n^\top v_{t+1} + c_n^\top X_t + e_{t+1}^{(n)}", font_size=40,
                      colors={r"rx_{t+1}^{(n)}": GOOD}),
                cmath(r"(\lambda_0, \lambda_1)", r"=", r"(\beta\beta^\top)^{-1}\beta\,\big(a + \tfrac12(\cdots),\ c\big)",
                      font_size=40, colors={r"(\lambda_0, \lambda_1)": TP}),
                cmath(r"\text{TP}_t^{(n)}", r"=", r"y_t^{(n)}(\lambda) - y_t^{(n)}(\lambda = 0)", font_size=40,
                      colors={r"\text{TP}_t^{(n)}": TP})]
        whys = [why(r"the curve's state: its first five principal components, a vector autoregression"),
                why(r"one regression per maturity: what part of a bond's excess return is exposure to news, and what part "
                    r"was predictable"),
                why(r"the predictable part must be a price of risk times the exposure: one cross-sectional regression "
                    r"gives the prices of risk"),
                why(r"price every bond with them, and again with them set to zero: the difference is the premium")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.2, buff=0.55, edge=6.9)
        with self.voiceover(
            "To measure the premium month by month you need a model, and the most transparent one is Tobias Adrian, "
            "Richard Crump and Emanuel Moench's, from 2013: three linear regressions. First, the state of the curve is "
            "its first five principal components, following a vector autoregression. <bookmark mark='a'/> Second, for "
            "each maturity, regress the bond's excess return on the state's surprises and on the state itself: "
            "exposure to news, and a predictable part. <bookmark mark='b'/> Third, no arbitrage says the predictable "
            "part must be exposure times a price of risk; one more regression gives those prices. "
            "<bookmark mark='c'/> Price the whole curve with the estimated prices of risk, and again with them set to "
            "zero. The gap is the term premium. The New York Fed publishes this decomposition every day."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()
        card = house_lab(r"the term premium in three regressions", R.acm_decompose, "# 2. excess returns", 14, width=12.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "In the House it is forty lines, and the heart of it is here: the excess returns, the regression on news "
            "and state, and the prices of risk."
        ):
            self.play(FadeIn(card))
            self.wait(1.0)
        self.clear_scene()

    def decompose(self, t):
        T, y, rn, tp = (np.asarray(t[k]) for k in ("t", "y10", "rn10", "tp10"))
        nt, ntp = np.asarray(t["ny_t"]), np.asarray(t["ny_tp10"])
        g = axes([1961, 2026], [-3, 16], x_length=8.2, y_length=4.6, xlabel=r"year", ylabel=r"10-year, percent",
                 xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 5, 10, 15], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        zero = DashedLine(ax.c2p(1961, 0), ax.c2p(2026, 0), color=GREY_D, stroke_width=1.5)
        ly = curve(ax, T, y, ZERO, stroke_width=2.5)
        lr = curve(ax, T, rn, EXP, stroke_width=2.5)
        lt = curve(ax, T, tp, TP, stroke_width=3)
        ln = DashedVMobject(curve(ax, nt, ntp, WHITE, stroke_width=1.5), num_dashes=200)
        leg = legend([(ZERO, r"10-year yield (model fit)"), (EXP, r"expected average short rate"),
                      (TP, r"term premium (House)"), (WHITE, r"term premium (NY Fed)")], font_size=16).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.8)
        sc = t["since_cut"]
        a, b = sc["2024-08"], sc["2025-12"]
        side = VGroup(
            MathTex(rf"\rho = {t['corr']:.4f},\ \ \overline{{|\Delta|}} = {100 * t['mad']:.0f}\ \text{{bp}}", font_size=26),
            wrapped_label(rf"1981: premium {t['tp_1981']:.1f}\%; {int(t['tp_min']['t'])}: {t['tp_min']['v']:.1f}\%", 3.6,
                          17, TP),
            wrapped_label(rf"Aug 2024 to Dec 2025, while the Fed cut: yield {b['y'] - a['y']:+.2f}, expectations "
                          rf"{b['rn'] - a['rn']:+.2f}, premium {b['tp'] - a['tp']:+.2f}", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=0.35, aligned_edge=LEFT)
        fit_right(side)
        with self.voiceover(
            "Here is the ten-year yield split in two, re-estimated by the House on the Fed's curve. In blue, the "
            "expected path of short rates; in pink, the premium. <bookmark mark='a'/> The dashed white line is the New "
            f"York Fed's published premium. They agree to a correlation of {t['corr']:.4f}, about "
            f"{100 * t['mad']:.0f} basis points apart on average. <bookmark mark='b'/> In 1981 investors demanded about "
            f"{t['tp_1981']:.1f} points to hold ten-year bonds through Volcker's inflation fight. By "
            f"{int(t['tp_min']['t'])} the premium was {t['tp_min']['v']:.1f}: they paid for the privilege, with the Fed "
            "buying bonds and long Treasuries prized as a hedge. <bookmark mark='c'/> And since August 2024, while the "
            f"Fed cut by a point and three quarters, expected short rates fell {abs(b['rn'] - a['rn']):.2f} but the "
            f"premium rose {b['tp'] - a['tp']:.2f}, and the ten-year yield went up, not down."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(ly), Create(lr), FadeIn(leg[0]), FadeIn(leg[1]), run_time=2.5)
            self.play(Create(lt), FadeIn(leg[2]), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(leg[3]), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        q = ask(r"the Fed cut rates and the 10-year yield rose. Which part of the yield did the Fed control?")
        with self.voiceover("So which part of the long yield does the Fed control?"):
            self.play(FadeIn(q))
        self.add(illustration(r"Adrian, Crump and Moench (2013), re-estimated on GSW zero yields, 3--120 months"))
        self.wait(0.5)
        self.clear_scene()
