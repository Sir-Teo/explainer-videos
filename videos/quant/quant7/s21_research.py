from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import BAD, FC, GOOD, PART, RET, VOL, load

DM_C, CW_C = BAD, GOOD


class Research(VoiceoverScene):
    def construct(self):
        t = load("nested_theory")
        self.card()
        self.problem()
        self.why_fails()
        self.adjust()
        self.laws(t)
        self.size_power(t)
        self.btc(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Comparing nested forecasts", r"When one model contains the other, why does the usual test "
                          r"fail?", part=PART)
        with self.voiceover("For the researcher: Chapter 12 compared forecasts with Diebold and Mariano's test. When one "
                            "model contains the other, as HAR contains a single lag, that test quietly fails. Here is why, "
                            "and the fix."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def problem(self):
        rows = [cmath(r"d_t", r"=", r"e_{1,t}^2 - e_{2,t}^2", font_size=34, colors={r"d_t": DM_C}),
                cmath(r"\mathrm{DM}", r"=", r"\frac{\bar d}{\sqrt{\widehat{\operatorname{LRV}}(d)/P}}\ \Rightarrow\ N(0, 1)",
                      font_size=34, colors={r"\mathrm{DM}": DM_C}),
                cmath(r"H_0:\ \beta_2 = 0", r"\Rightarrow", r"e_{1,t} = e_{2,t}\ \text{in population},\ \ d_t \equiv 0",
                      font_size=32, colors={r"H_0:\ \beta_2 = 0": FC})]
        whys = [why(r"the loss differential between the small model 1 and the big model 2, over $P$ out-of-sample forecasts"),
                why(r"Diebold and Mariano (1995): its mean, over a long-run standard error, is asymptotically normal when "
                    r"the two models' population forecasts differ"),
                why(r"but if model 1 is nested in model 2 and the extra coefficients are zero, the population forecasts are "
                    r"the same: the differential has variance zero, and the normal limit has nothing to scale")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.48, edge=6.9)
        with self.voiceover(
            "Recall the test. <bookmark mark='a'/> Take each day's squared error from the small model, less the big "
            "model's. <bookmark mark='b'/> Diebold and Mariano divide the average by its long-run standard error and "
            "compare with a normal. <bookmark mark='c'/> But suppose the small model is nested in the big one, and the "
            "extra coefficients are truly zero. Then in the population the two models make the same forecast, the "
            "differential is identically zero, and the normal approximation has no variance to work with."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def why_fails(self):
        rows = [cmath(r"\hat y_{2,t}", r"=", r"\hat y_{1,t} + \underbrace{x_t^{\top}(\hat\beta_{2,t} - 0)}_{\text{estimation noise}}",
                      font_size=32, colors={r"\hat y_{2,t}": FC}),
                cmath(r"\mathbb E\big[e_{2,t}^2\big]", r"\approx", r"\mathbb E\big[e_{1,t}^2\big] + \mathbb E\big[(\hat y_{1,t} - "
                      r"\hat y_{2,t})^2\big]", font_size=32, colors={r"\mathbb E\big[e_{2,t}^2\big]": DM_C}),
                cmath(r"\mathbb E[\bar d]", r"<", r"0\quad\text{and}\quad \mathrm{DM} \Rightarrow \text{a functional of Brownian "
                      r"motion}", font_size=30, colors={r"\mathbb E[\bar d]": DM_C})]
        whys = [why(r"under the null the big model's forecast is the small one's plus the noise of estimating coefficients "
                    r"that are really zero"),
                why(r"that noise is independent of the shock being forecast, so it adds its own mean square to the big "
                    r"model's error"),
                why(r"so the differential is negative on average: the test leans towards the small model. Clark and McCracken "
                    r"(2001) and McCracken (2007): with recursive estimation the limit is non-standard, a functional of "
                    r"Brownian motion that depends on $P/R$")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.48, edge=6.9)
        with self.voiceover(
            "And in a finite sample it is worse than degenerate. <bookmark mark='a'/> Under the null, the big model's "
            "forecast is the small model's, plus the noise from estimating coefficients that are really zero. "
            "<bookmark mark='b'/> That noise has nothing to do with the shock being forecast, so it adds its own mean "
            "square to the big model's error. <bookmark mark='c'/> The differential is negative on average, and the "
            "test leans towards the small model. Clark and McCracken showed that the limit is not normal at all but "
            "a functional of Brownian motion, depending on how long the forecast period is relative to the first "
            "estimation window."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def adjust(self):
        rows = [cmath(r"f_t", r"=", r"e_{1,t}^2 - \big[e_{2,t}^2 - (\hat y_{1,t} - \hat y_{2,t})^2\big]", font_size=34,
                      colors={r"f_t": CW_C}),
                cmath(r"\mathrm{CW}", r"=", r"\frac{\bar f}{\sqrt{\widehat{\operatorname{LRV}}(f)/P}},\quad \text{reject if }"
                      r"\ \mathrm{CW} > 1.645", font_size=34, colors={r"\mathrm{CW}": CW_C})]
        whys = [why(r"Clark and West (2007): subtract from the big model's squared error the noise its extra parameters "
                    r"add under the null, estimated by the squared gap between the two forecasts"),
                why(r"a one-sided $t$-test on the adjusted differential: approximately normal, approximately the right "
                    r"size, and simple to compute")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The fix, from Todd Clark and Kenneth West in 2007, is one line. <bookmark mark='a'/> Add back to the big "
            "model what its extra parameters cost it under the null: the squared gap between the two forecasts. "
            "<bookmark mark='b'/> Then test the adjusted differential one-sided, against a normal. It is not exact, but "
            "it is close, and it takes one line of code in the House."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
        self.wait(0.5)
        self.clear_scene()

    def laws(self, t):
        e = np.linspace(-5, 5, 41)
        c = (e[:-1] + e[1:]) / 2
        s0 = t["sim"]["0.0"]
        g = axes([-5, 5], [0, 0.5], x_length=8.2, y_length=3.8, xlabel=r"test statistic, the null true", ylabel=r"density",
                 xticks=[-4, -2, 0, 1.645, 4], yticks=[], font_size=13).move_to(LEFT * 1.4 + DOWN * 0.3)
        ax = g.ax
        xs = np.linspace(-5, 5, 300)
        nrm = curve(ax, xs, np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi), WHITE, stroke_width=2.5)
        crit = DashedLine(ax.c2p(1.645, 0), ax.c2p(1.645, 0.5), color=GREY_B, stroke_width=1.5)
        lines = VGroup()
        for key, col in (("dm_hist", DM_C), ("cw_hist", CW_C)):
            h = np.asarray(s0[key], float)
            h = h / h.sum() / (e[1] - e[0])
            lines.add(curve(ax, c, h, col, stroke_width=3))
        leg = legend([(WHITE, r"$N(0, 1)$"), (DM_C, rf"DM, mean {s0['dm_mean']:.2f}"), (CW_C, rf"CW, mean {s0['cw_mean']:.2f}")],
                     font_size=17).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"{t['M']} simulations: the target is pure noise, the big model adds a persistent regressor "
                             rf"($\rho = 0.9$); recursive estimation from $R = {t['R']}$, $P = {t['P']}$ one-step forecasts",
                             3.2, 15, GREY_A).next_to(leg, DOWN, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Simulate it. <bookmark mark='a'/> The target is pure noise, and the big model adds a persistent "
            "regressor that predicts nothing. The Diebold-Mariano statistic is centred well below zero: the big model "
            "is punished for its estimation noise. <bookmark mark='b'/> Clark and West's statistic is centred near zero, "
            "close to the normal curve."
        ) as vo:
            self.play(FadeIn(g), Create(nrm), Create(crit), FadeIn(leg), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lines[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def size_power(self, t):
        bs = ["0.0", "0.05", "0.1"]
        hx = [-3.4, 0.4, 3.4]
        head = VGroup(label(r"true slope on the extra regressor", font_size=18, color=GREY_B),
                      label(r"DM rejects", font_size=20, color=DM_C), label(r"CW rejects", font_size=20, color=CW_C))
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(MathTex(rf"\beta_2 = {b}", font_size=26),
                                                 MathTex(rf"{100 * t['sim'][b]['dm_reject']:.1f}\%", font_size=26),
                                                 MathTex(rf"{100 * t['sim'][b]['cw_reject']:.1f}\%", font_size=26))
                                          for b in bs]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.5 - 0.7 * j, 0])
            tab.add(row)
        foot = wrapped_label(r"one-sided tests at a nominal 5\%: the first row is the size, the others are power. A slope of "
                             r"0.1 on a unit-variance regressor is an $R^2$ of about 1\%, Part 27's world", 11.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Size and power. <bookmark mark='a'/> With the null true, Diebold and Mariano reject one time in two "
            "hundred and fifty, far below five percent: the test almost never favours the big model. Clark and West "
            "reject about three percent, a little conservative, as they reported. <bookmark mark='b'/> With a real "
            "slope of point zero five, Diebold and Mariano find it one time in a hundred and Clark and West eight times; "
            "at point one, still under four percent against one time in four. The wrong test throws away almost all "
            "the power to detect a small, real improvement."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
        self.wait(0.4)
        self.clear_scene()

    def btc(self, t):
        b = t["btc"]
        hx = [-3.6, 0.0, 2.4, 4.8]
        head = VGroup(label(r"Bitcoin's daily RV, recursive", font_size=18, color=GREY_B), label(r"MSE ratio", font_size=20),
                      label(r"DM $t$", font_size=20, color=DM_C), label(r"CW $t$", font_size=20, color=CW_C))
        names = {"AR1_vs_HAR": r"one lag $\subset$ HAR", "HAR_vs_HARQ": r"HAR $\subset$ HARQ"}
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(names[k], font_size=18, color=VOL),
                                                 MathTex(rf"{b[k]['mse_ratio']:.3f}", font_size=26),
                                                 MathTex(rf"{b[k]['t_dm']:.2f}", font_size=26),
                                                 MathTex(rf"{b[k]['t_cw']:.2f}", font_size=26)) for k in names]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.2 - 0.75 * j, 0])
            row[0].align_to(np.array([hx[0] - 2.4, 0, 0]), LEFT)
            tab.add(row)
        f, l_ = str(t["btc_first"]), str(t["btc_last"])
        foot = wrapped_label(rf"one-step forecasts of the next day's realized variance, refitted every day on all earlier "
                             rf"data, {f[:4]}-{f[4:6]}-{f[6:]} to {l_[:4]}-{l_[4:6]}-{l_[6:]}; MSE ratio: big model over small; "
                             r"Newey--West with 5 lags; positive $t$ favours the big model", 11.6, 16, GREY_A).to_edge(DOWN,
                                                                                                         buff=0.5)
        with self.voiceover(
            "On real data, Bitcoin's realized variance in 2019 and 2020. <bookmark mark='a'/> HAR against a single lag: "
            "HAR's mean squared error is one percent higher, Diebold and Mariano see nothing, and Clark and West, "
            "allowing for HAR's extra estimation noise, lean slightly towards HAR without significance. HARQ against "
            "HAR: HARQ's error is sixty-five percent higher, dominated by the days of March 2020, when its quarticity "
            "term exploded, and both statistics agree. No adjustment rescues a model that is genuinely worse."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: many nested models at once", r"a model confidence set over nested and non-nested models "
                          r"together (Hansen, Lunde and Nason 2011) inherits the degeneracy; valid joint inference is "
                          r"incomplete", width=12.4, font_size=18),
            desk_question(r"open: the estimated model or the method?", r"Giacomini and White (2006) test the forecasting "
                          r"method with its estimation window, which makes nesting harmless but asks a different question; "
                          r"which question a desk should ask is argued", width=12.4, font_size=18),
            desk_question(r"open: losses other than squared error", r"for quantiles and expected shortfall (Part 2's "
                          r"backtests), nested comparisons have no Clark--West analogue with a clean limit", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> A model confidence set over many models, some nested in others, "
            "inherits the same degeneracy, and valid joint inference is incomplete. <bookmark mark='b'/> Giacomini and "
            "White test the forecasting method, estimation window and all, which makes nesting harmless but asks a "
            "different question; which question a desk should ask is argued. <bookmark mark='c'/> And for losses "
            "other than squared error, such as the quantiles of Part 2's margin backtests, there is no clean analogue "
            "of Clark and West."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"over 200 forecasts, $\bar d = -0.02$ with standard error 0.03, and the mean squared gap between the "
                       r"two forecasts is 0.05. Compute DM and an approximate CW. Which model do they favour?")
        with self.voiceover(
            "Pause and predict. Over two hundred forecasts the average loss differential is minus point zero two with a "
            "standard error of point zero three, and the average squared gap between the forecasts is point zero five. "
            "Compute both statistics, roughly. Which model do they favour?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
