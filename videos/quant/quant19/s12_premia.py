from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, FWD, GOOD, PART, VAS, ZERO, ask, fit_right, illustration, load

CP_C, NN_C = QC.SPOT, QC.OPTION


class Premia(VoiceoverScene):
    def construct(self):
        p = load("premia")
        self.card()
        self.theory()
        self.famabliss(load("famabliss"))
        self.coefs(p)
        self.series(p)
        self.verdict(p)
        self.acm(load("premia_acm"))
        self.macro()

    def card(self):
        c = chapter_card(11, r"Bond risk premia", r"Can the curve forecast its own returns?", part=PART)
        with self.voiceover("Chapter eleven. Bond risk premia: does the curve forecast what bonds will earn?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theory(self):
        rows = [cmath(r"rx^{(n)}_{t+1}", r"=", r"p^{(n-1)}_{t+1} - p^{(n)}_t - y^{(1)}_t", font_size=42,
                      colors={r"rx^{(n)}_{t+1}": ZERO}),
                cmath(r"\mathbb{E}_t\big[rx^{(n)}_{t+1}\big]", r"=", r"\text{const}\quad\text{(expectations hypothesis)}",
                      font_size=38, colors={r"\mathbb{E}_t\big[rx^{(n)}_{t+1}\big]": ZERO}),
                cmath(r"\overline{rx}_{t+1}", r"=", r"\gamma_0 + \gamma_1 y^{(1)}_t + \gamma_2 f^{(2)}_t + \dots + "
                      r"\gamma_5 f^{(5)}_t + \varepsilon_{t+1}", font_size=38, colors={r"\overline{rx}_{t+1}": ZERO})]
        whys = [why(r"the excess return: buy an $n$-year zero, sell it a year later as an $(n{-}1)$-year zero, minus "
                    r"the one-year rate ($p$ are log prices)"),
                why(r"if long bonds paid the same premium at all times, the curve would only forecast rates; Fama and "
                    r"Bliss (1987) and Campbell and Shiller (1991) found that a steep curve forecasts high returns instead"),
                why(r"Cochrane and Piazzesi (2005): one combination of the five forward rates forecasts every maturity's "
                    r"excess return, with $R^2$ of about 35\% in their data")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.4, buff=0.7, edge=6.9)
        with self.voiceover(
            "Part eighteen split a long yield into the expected path of short rates and a term premium. Is the premium "
            "constant? Define the excess return: buy a bond, sell it a year later, and subtract what a one-year bill "
            "earned. <bookmark mark='a'/> If the premium were constant, the slope of the curve would forecast only "
            "future rates. Eugene Fama and Robert Bliss in 1987, and John Campbell and Robert Shiller in 1991, found "
            "the opposite: a steep curve forecasts high bond returns. <bookmark mark='b'/> In 2005 John Cochrane and "
            "Monika Piazzesi went further: a single combination of five forward rates forecast the excess returns of "
            "every maturity, explaining a third or more of their variation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def famabliss(self, fb):
        rows = fb["rows"]
        g = axes([1.4, 5.6], [-0.2, 2.0], x_length=6.6, y_length=4.2, xlabel=r"bond maturity $n$, years",
                 ylabel=r"slope on the forward spread", xticks=[2, 3, 4, 5], yticks=[0, 0.5, 1.0, 1.5, 2.0], font_size=14
                 ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        eh = Line(ax.c2p(1.4, 0), ax.c2p(5.6, 0), color=BAD, stroke_width=3)
        pts = VGroup()
        for r_ in rows:
            n_, b_, se = r_["n"], r_["slope"], r_["se"]
            pts.add(VGroup(Line(ax.c2p(n_, b_ - 2 * se), ax.c2p(n_, b_ + 2 * se), color=CP_C, stroke_width=4),
                           Dot(ax.c2p(n_, b_), color=CP_C, radius=0.09)))
        side = VGroup(
            MathTex(r"rx^{(n)}_{t+1} = \alpha + \beta_n\big(f^{(n)}_t - y^{(1)}_t\big) + \varepsilon", font_size=28),
            legend([(BAD, r"expectations hypothesis: $\beta_n = 0$"), (CP_C, r"estimate, $\pm$ 2 Newey--West s.e.")],
                   font_size=16),
            MathTex(rf"R^2:\ {100 * rows[0]['r2']:.0f}\text{{--}}{100 * rows[-1]['r2']:.0f}\%", font_size=26),
            wrapped_label(rf"monthly, {fb['start']}--{fb['end']}, overlapping one-year returns on the Fed's zero curve. "
                          r"A slope of one means the forward spread is all premium: none of it forecasts higher rates",
                          3.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Fama and Bliss's test is one line. Regress each bond's excess return on its own forward spread, the "
            "forward rate minus the one-year yield. <bookmark mark='a'/> If the expectations hypothesis held, the "
            "slope would be zero: a high forward would only forecast higher rates, and no extra return. "
            f"<bookmark mark='b'/> On the Fed's curve since 1964, the slopes run from {rows[0]['slope']:.1f} to "
            f"{rows[-1]['slope']:.1f}, each about three standard errors from zero, and close to one: a steep curve "
            "is mostly premium, not forecast. The fit is modest, under a tenth of the variance, which is what bond "
            "returns are like."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(eh), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.25), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def coefs(self, p):
        g1, g2 = np.asarray(p["gamma"])[1:], np.asarray(p["gamma_full"])[1:]
        names = [r"y^{(1)}", r"f^{(2)}", r"f^{(3)}", r"f^{(4)}", r"f^{(5)}"]
        lim = 12
        g = axes([0.4, 5.6], [-lim, lim], x_length=7.6, y_length=4.4, xlabel=r"", ylabel=r"coefficient $\gamma$",
                 xticks=[], yticks=[-10, -5, 0, 5, 10], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(0.4, 0), ax.c2p(5.6, 0), color=WHITE, stroke_width=1.5)

        def bars(vals, dx, col):
            out = VGroup()
            for i, v in enumerate(vals):
                x = ax.c2p(i + 1 + dx, 0)[0]
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, float(np.clip(v, -lim, lim)))[1]
                out.add(Rectangle(width=0.34, height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=col,
                                  fill_opacity=0.8).move_to([x, (y0 + y1) / 2, 0]))
            return out
        b1, b2 = bars(g1, -0.2, CP_C), bars(g2, 0.2, QC.IMPLIED)
        ticks = VGroup(*[MathTex(n_, font_size=26).move_to([ax.c2p(i + 1, 0)[0], ax.c2p(0, -lim)[1] - 0.3, 0])
                         for i, n_ in enumerate(names)])
        side = VGroup(
            legend([(CP_C, r"fitted 1964--2003"), (QC.IMPLIED, r"fitted 1964--2025")], font_size=18),
            MathTex(rf"R^2 = {100 * p['r2_in']:.0f}\%\ \ \text{{and}}\ \ {100 * p['r2_full']:.0f}\%", font_size=28),
            wrapped_label(r"the five inputs are nearly collinear on the Fed's smoothed curve, so the coefficients swing "
                          r"with the sample; Cochrane and Piazzesi's famous tent shape was found in unsmoothed "
                          r"Fama--Bliss data. What survives is the forecast, not the shape", 3.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Run that regression on the Fed's own zero curve. Average excess return of the two- to five-year zeros, "
            "a year ahead, on the one-year yield and four forwards. <bookmark mark='a'/> Fitted to 1964 through 2003, "
            f"it explains {100 * p['r2_in']:.0f} percent. <bookmark mark='b'/> Fitted through 2025, the coefficients "
            f"change completely, and the fit falls to {100 * p['r2_full']:.0f} percent. The five forwards move almost "
            "together on a smoothed curve, so the individual weights are fragile. Cochrane and Piazzesi's famous tent "
            "shape came from rougher data. What matters is whether the forecast holds up out of sample."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(ticks), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN if v >= 0 else UP) for r_, v in zip(b1, g1)], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN if v >= 0 else UP) for r_, v in zip(b2, g2)], lag_ratio=0.15),
                      FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def series(self, p):
        t, rx = np.asarray(p["t"]), np.asarray(p["rx"]) * 100
        pc, pn = np.asarray(p["pred_cp"]) * 100, np.asarray(p["pred_nn"]) * 100
        g = axes([1964, 2025.5], [-12, 12], x_length=12.0, y_length=4.4, xlabel=r"forecast date",
                 ylabel=r"1-year excess return, \%", xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[-10, -5, 0, 5, 10],
                 font_size=14).shift(DOWN * 0.5)
        ax = g.ax
        zones = VGroup()
        for a, b, col, txt in [(1964, 2004, GREY_D, r"fit"), (2004, 2021, QC.IMPLIED, r"validation"),
                               (2021, 2025.5, QC.HOUSE, r"sealed hold-out")]:
            r_ = Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0], height=ax.c2p(0, 12)[1] - ax.c2p(0, -12)[1],
                           stroke_width=0, fill_color=col, fill_opacity=0.12)
            r_.move_to([(ax.c2p(a, 0)[0] + ax.c2p(b, 0)[0]) / 2, ax.c2p(0, 0)[1], 0])
            zones.add(VGroup(r_, label(txt, font_size=17, color=GREY_A).next_to(r_, UP, buff=0.05)))
        real = curve(ax, t, np.clip(rx, -12, 12), WHITE, stroke_width=1.6)
        lc = curve(ax, t, np.clip(pc, -12, 12), CP_C, stroke_width=2.4)
        ln = curve(ax, t, np.clip(pn, -12, 12), NN_C, stroke_width=2.4)
        leg = legend([(WHITE, r"realised"), (CP_C, r"Cochrane--Piazzesi forecast"),
                      (NN_C, r"network forecast (5--16--1, three seeds)")], font_size=17).arrange(RIGHT, buff=0.5
                                                                                                   ).to_edge(UP, buff=0.35)
        with self.voiceover(
            "So here is the honest version. Fit both models on 1964 through 2003: the regression, and a small neural "
            "network on the same five inputs, in the spirit of Daniele Bianchi, Matthias Büchner and Andrea Tamoni, "
            "who in 2021 found that networks forecast bond returns better than regressions. <bookmark mark='a'/> "
            "Judge them on 2004 to 2020, the validation years. <bookmark mark='b'/> And the years since 2021 were "
            "sealed in the House's registry before either model was fitted: the trial counter now reads "
            f"{p['trials']}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(zones[0]), FadeIn(leg), Create(real), run_time=2)
            self.play(Create(lc), Create(ln), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(zones[1]))
            vo.wait_until("b")
            self.play(FadeIn(zones[2]))
        self.wait(0.6)
        self.clear_scene()

    def verdict(self, p):
        t, rx = np.asarray(p["t"]), np.asarray(p["rx"])
        pc, pn = np.asarray(p["pred_cp"]), np.asarray(p["pred_nn"])
        val, hold = (t >= 2004) & (t < 2021), t >= 2021

        def corr(a, b, s):
            return float(np.corrcoef(a[s], b[s])[0, 1])
        hx = [-3.2, 0.4, 3.6]
        head = VGroup(label(r"Cochrane--Piazzesi", font_size=22, color=CP_C), label(r"network", font_size=22, color=NN_C))
        for h, x in zip(head, hx[1:]):
            h.move_to([x, 2.3, 0])
        lines = [(r"$R^2_{\text{oos}}$, 2004--2020", p["val"]["cp"], p["val"]["nn"], "{:+.2f}"),
                 (r"$R^2_{\text{oos}}$, 2021--2025 (sealed)", p["hold"]["cp"], p["hold"]["nn"], "{:+.2f}"),
                 (r"correlation with realised, 2021--2025", corr(rx, pc, hold), corr(rx, pn, hold), "{:+.2f}"),
                 (r"mean forecast / realised, 2021--2025", None, None, "")]
        cells = VGroup()
        for i, (name, a, b, fmt) in enumerate(lines):
            y = 1.4 - 0.85 * i
            if a is None:
                a_s = rf"{100 * pc[hold].mean():+.1f}\% / {100 * rx[hold].mean():+.1f}\%"
                b_s = rf"{100 * pn[hold].mean():+.1f}\% / {100 * rx[hold].mean():+.1f}\%"
            else:
                a_s, b_s = fmt.format(a), fmt.format(b)
            cells.add(VGroup(label(name, font_size=19).move_to([hx[0], y, 0]),
                             MathTex(a_s, font_size=30).move_to([hx[1], y, 0]),
                             MathTex(b_s, font_size=30).move_to([hx[2], y, 0])))
        foot = wrapped_label(
            r"$R^2_{\text{oos}} = 1 - \sum(\text{realised} - \text{forecast})^2 / \sum(\text{realised} - \text{fit-period "
            r"mean})^2$. Both models lose to the historical mean through the bond bull market of 2004--2020. In the "
            r"hold-out both win, because both forecast negative premia when realised returns were negative; but within "
            r"the hold-out neither times the ups and downs. One registered test each; no investment advice",
            12.4, 18, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The verdict, against the simplest rival: forecast the average return of the fitting years. "
            "<bookmark mark='a'/> Through 2004 to 2020, both models lose to it badly; the network loses by less. "
            "Long bonds rallied for most of those years while the forecasts said they would not. "
            "<bookmark mark='b'/> In the sealed years, both win, and the network wins by more. <bookmark mark='c'/> "
            "Look closer before celebrating. Within those years, the forecasts are barely, or even negatively, "
            "correlated with what happened month by month. <bookmark mark='d'/> They won by forecasting a negative premium, in years when bonds lost "
            "money. A level, not a timing. That is what one honest test can tell you, and it is less than a "
            "backtest would have claimed."
        ) as vo:
            self.play(FadeIn(head))
            for i, m in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m)
                self.play(FadeIn(cells[i], shift=RIGHT * 0.2))
            self.play(FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()

    def acm(self, a):
        t, cp, tp = np.asarray(a["t"]), np.asarray(a["cp"]), np.asarray(a["tp5"])
        g = axes([1963, 2025.5], [-6, 8], x_length=8.6, y_length=4.4, xlabel=r"year", ylabel=r"\%",
                 xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[-4, 0, 4, 8], font_size=14
                 ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(1963, 0), ax.c2p(2025.5, 0), color=GREY_C, stroke_width=1.2)
        l1 = curve(ax, t, np.clip(cp, -6, 8), CP_C, stroke_width=2.2)
        l2 = curve(ax, t, np.clip(tp, -6, 8), QC.IMPLIED, stroke_width=2.6)
        side = VGroup(
            legend([(CP_C, r"Cochrane--Piazzesi: expected 1-year excess return"),
                    (QC.IMPLIED, r"ACM: the 5-year term premium (Part 18)")], font_size=16),
            MathTex(rf"\text{{correlation}} = {a['corr']:.2f}", font_size=30),
            wrapped_label(r"two routes to one quantity: a regression of realised returns on forwards, and an affine "
                          r"model of the whole curve's prices of risk. Both say the premium was high around 1982, fell "
                          r"for four decades, and went negative in the 2010s", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "There is a cross-check. Part eighteen took the New York Fed's term premium, from an affine model of the "
            "whole curve that never looks at a forecasting regression. Put it beside the Cochrane and Piazzesi "
            "forecast, month by month since 1963. <bookmark mark='a'/> They are different objects, an expected "
            "one-year return and a premium in a five-year yield, built by different methods, and they are correlated "
            f"{a['corr']:.2f}. High in the early eighties, falling for four decades, below zero in the 2010s: the "
            "price of duration risk moves slowly, and both methods see it move."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]), Create(l1), run_time=2)
            vo.wait_until("a")
            self.play(Create(l2), FadeIn(side[1]), FadeIn(side[2]), run_time=2)
        self.add(illustration(r"NY Fed ACM term premium, monthly; CP fitted 1964--2003"))
        self.wait(0.4)
        self.clear_scene()

    def macro(self):
        rows = [cmath(r"X_t", r"=", r"\big(\text{inflation},\ \text{real activity},\ \text{latent}_1, \dots\big)",
                      font_size=40, colors={r"X_t": FWD}),
                cmath(r"r_t", r"=", r"\delta_0 + \delta_1^\top X_t,\quad \lambda_t = \lambda_0 + \lambda_1 X_t", font_size=40,
                      colors={r"r_t": ZERO}),
                cmath(r"y^{(n)}_t", r"=", r"A_n + B_n^\top X_t", font_size=42, colors={r"y^{(n)}_t": ZERO})]
        whys = [why(r"Ang and Piazzesi (2003): put macroeconomic variables into the state of an affine model, beside the "
                    r"curve's own factors"),
                why(r"a Taylor-like rule for the short rate (Part 18), and prices of risk that move with the state: a "
                    r"time-varying premium, which the expectations hypothesis forbids"),
                why(r"still affine (chapter 2), so every yield is in closed form, and every yield splits into expected "
                    r"rates and a premium, as the ACM model of Part 18 does")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.2, buff=0.7, edge=6.9)
        with self.voiceover(
            "The models that connect these premia to the economy are the macro-finance term-structure models. In 2003 "
            "Andrew Ang and Monika Piazzesi put inflation and real activity into the state of an affine model. "
            "<bookmark mark='a'/> The short rate follows something like a Taylor rule, and the price of risk moves "
            "with the state, so the premium varies through time. <bookmark mark='b'/> And it stays affine: every yield "
            "is in closed form, and every yield splits into expected rates and a premium, the decomposition the "
            "central banks publish."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        q = ask(r"a model forecasts bond excess returns with an out-of-sample $R^2$ of 0.3, but only by getting the "
                r"average right. Could you trade it, and what would you be betting on?")
        with self.voiceover("A model forecasts bond returns out of sample, but only by getting their average right. "
                            "Could you trade it, and what would you really be betting on?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
