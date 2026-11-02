from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data, tbar

MODEL_C = {"EWMA": GREY_B, "GARCH": FC, "GJR": FC, "HAR": VOL, "HARQ": VOL, "log-HAR": GOOD, "LSTM": ALT,
           "Transformer": ALT, "HARNet": RET}


class March(VoiceoverScene):
    def construct(self):
        race = load("race")
        self.card()
        self.file()
        self.day_before(race)
        self.scaling(load("scaling"))

    def card(self):
        c = chapter_card(16, r"March 2020", r"What did each model say the day before?", lit=(2020,), part=PART)
        with self.voiceover("Chapter sixteen. March 2020."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def file(self):
        card = crisis_card(
            r"12 -- 16 March 2020", r"The Covid crash",
            r"As Covid-19 closed economies, every asset was sold for cash at once. On 12 March the US stock market fell "
            r"9.6\%, and on 16 March 12.0\%, its worst day since 1987. Bitcoin fell 39.5\% on the 12th. As Ethereum's "
            r"network congested, a later report found that about \$8 million of MakerDAO collateral was auctioned for "
            r"bids of zero. On 16 March the VIX closed at 82.69, its highest close on record.",
            stats=[(r"-39.5\%", r"Bitcoin, 12 March (Binance)"), (r"-12.0\%", r"US stocks, 16 March"),
                   (r"82.69", r"the VIX, 16 March: a record close")],
            width=10.8, font_size=26)
        card.move_to(ORIGIN)
        src = real_data(r"Binance BTCUSDT daily; Kenneth French daily market return; facts from the public record")
        with self.voiceover(
            "In March 2020, as Covid-19 closed one economy after another, everything was sold for cash at once. On the "
            "twelfth of March the American stock market fell nine point six percent. Bitcoin fell thirty-nine and a "
            "half percent in a day. On Ethereum, the network clogged, and according to a later report, about eight "
            "million dollars of collateral in the MakerDAO lending protocol was auctioned off for bids of zero. On "
            "the sixteenth the stock market fell twelve percent, its worst day since 1987, and the VIX, the market's "
            "own forecast of volatility, closed at eighty-two point six nine, a record."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()

    def day_before(self, race):
        names = list(race["names"])
        m = race["march12"]
        vmax = 5.0
        g = axes([0, len(names)], [0, vmax], x_length=7.6, y_length=4.4, xticks=[], yticks=[0, 1, 2, 3, 4, 5],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", ylabel=r"forecast of 12 March's volatility, made on the 11th",
                 font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.15)
        ax = g.ax
        bars = VGroup(*[tbar(ax, i + 0.5, min(m[k], vmax), MODEL_C[k], width=0.6) for i, k in enumerate(names)])
        vals = VGroup(*[MathTex(f"{100 * m[k]:.0f}\\%", font_size=22, color=MODEL_C[k]).next_to(b, UP, buff=0.05)
                        for k, b in zip(names, bars)])
        labs = VGroup(*[label({"Transformer": r"Transf.", "log-HAR": r"log-HAR"}.get(k, k), font_size=16, color=GREY_A).next_to(
            ax.c2p(i + 0.5, 0), DOWN, buff=0.1) for i, k in enumerate(names)])
        real = m["realized"]
        top = min(real, vmax)
        rl = DashedLine(ax.c2p(0, top), ax.c2p(len(names), top), color=BAD, stroke_width=3)
        rlab = MathTex(rf"\text{{realized on 12 March: }} {100 * real:.0f}\%" + (r"\ (\text{off the chart})"
                                                                                 if real > vmax else ""),
                       font_size=26, color=BAD).next_to(rl, DOWN, buff=0.12).align_to(rl, RIGHT)
        best = max((k for k in names), key=lambda k: m[k])
        side = VGroup(
            wrapped_label(rf"every model forecast {100 * min(m[k] for k in names):.0f}--{100 * max(m[k] for k in names):.0f}\%: "
                          r"a volatile day, not this one", 4.5, 21, GREY_A),
            wrapped_label(r"no model can forecast the day the shock arrives; the test is how fast it reacts the day "
                          r"after", 4.5, 21, GREY_A),
            wrapped_label(r"forecasts are of the variance, so one 40\% day inside a calm month swamps every loss "
                          r"function; QLIKE (Patton 2011) punishes under-forecasts more than MSE, and stays consistent "
                          r"when the target is noisy", 4.5, 20, VOL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"Here is what each model said on the eleventh of March, about the twelfth. The highest, {best}, forecast "
            f"an annualised volatility of {100 * m[best]:.0f} percent. <bookmark mark='a'/> What happened was "
            f"{100 * real:.0f} percent. <bookmark mark='b'/> No model, classical or neural, saw the day coming, and "
            "none could have: the shock was news, not a pattern in the past. What a forecaster can do is react the "
            "next day, and the realized models, which see the whole intraday path, react fastest. <bookmark mark='c'/> "
            "A day like this also dominates any average of squared errors. That is why forecasts are scored with "
            "QLIKE, the loss Andrew Patton showed in 2011 still ranks models correctly when the realized variance "
            "they are judged against is itself measured with noise."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(v) for v in vals], lag_ratio=0.15), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(rl), FadeIn(rlab))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

        # the weeks around it: realized against the forecasts
        t = np.asarray(race["window_t"])
        rv = np.asarray(race["window_rv"])
        fc = race["window_fc"]
        g2 = axes([2020 + 31 / 365, 2020 + 120 / 365], [0, 3.0], x_length=9.0, y_length=4.4,
                  xticks=[2020 + 31 / 365, 2020 + 60 / 365, 2020 + 91 / 365, 2020 + 120 / 365],
                  xfmt=lambda u: {32: r"1\ Feb", 61: r"1\ Mar", 92: r"1\ Apr", 121: r"30\ Apr"}[round((u - 2020) * 365) + 1],
                  yticks=[0, 1, 2, 3], yfmt=lambda u: f"{100 * u:.0f}\\%", ylabel=r"Bitcoin's volatility, annualised",
                  font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        a2 = g2.ax
        dots = VGroup(*[Dot(a2.c2p(tt, min(v, 3.0)), radius=0.045, color=BAD) for tt, v in zip(t, rv)])
        lines = {k: curve(a2, t, np.clip(np.asarray(fc[k]), 0, 3.0), MODEL_C[k], stroke_width=3)
                 for k in ("GARCH", "HAR", "log-HAR")}
        leg = legend([(BAD, r"realized (5-minute)"), (FC, r"GARCH"), (VOL, r"HAR"), (GOOD, r"log-HAR")], font_size=19)
        leg.next_to(g2, RIGHT, buff=0.4).align_to(g2, UP)
        nt = wrapped_label(r"GARCH sees only the daily close; HAR sees the whole day's path. After the shock, both "
                           r"over-forecast for weeks: volatility decays faster than either expects.", 3.4, 20, GREY_A)
        nt.next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        with self.voiceover(
            "Here are the weeks around it. Dots are each day's realized volatility, lines are the forecasts made the "
            "day before. <bookmark mark='a'/> All three jump after the twelfth. Then all three stay high for weeks "
            "while the market calms: volatility decays faster after a shock than models fitted to calmer years "
            "expect."
        ) as vo:
            self.play(FadeIn(g2), FadeIn(leg), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01, run_time=2))
            vo.wait_until("a")
            self.play(*[Create(c) for c in lines.values()], run_time=2.5)
            self.play(FadeIn(nt))
        self.wait(0.4)
        self.clear_scene()

    def scaling(self, s):
        T = np.asarray(s["T"])
        gv = np.asarray(s["garch_vol"])
        sq = np.asarray(s["sqrt_rule"])
        un = s["uncond"]
        q = desk_question(r"Daily volatility is 1\%. What is the volatility over a week? Over a year? When is the "
                          r"square-root-of-time rule wrong?", width=11.0, font_size=28).move_to(ORIGIN)
        with self.voiceover(
            "A desk question. Daily volatility is one percent. What is it over a week, and over a year? And when is "
            "the answer wrong?"
        ):
            self.play(FadeIn(q, shift=UP * 0.2))
        self.play(q.animate.scale(0.62).to_edge(UP, buff=0.25))
        ans = MathTex(r"\sigma_T = \sigma_1\sqrt{T}:\quad 1\%\times\sqrt{5} = 2.2\%,\qquad 1\%\times\sqrt{252} = 15.9\%",
                      font_size=32).next_to(q, DOWN, buff=0.3)
        g = axes([0, 252], [0, 1.0], x_length=7.4, y_length=3.6, xticks=[1, 21, 63, 126, 252],
                 xfmt=lambda u: {1: "1d", 21: "1m", 63: "3m", 126: "6m", 252: "1y"}[int(u)], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", ylabel=r"US stocks: forecast volatility over the next $T$ days",
                 font_size=16).to_edge(LEFT, buff=0.6).to_edge(DOWN, buff=0.5)
        ax = g.ax
        l_sq = curve(ax, T, sq, BAD, stroke_width=3)
        l_g = curve(ax, T, gv, FC, stroke_width=4)
        l_u = DashedLine(ax.c2p(0, un), ax.c2p(252, un), color=GREY_B, stroke_width=2)
        lu = label(rf"long-run: {100 * un:.0f}\%", font_size=18, color=GREY_B).next_to(ax.c2p(252, un), UP, buff=0.05).shift(LEFT * 0.6)
        side = VGroup(
            label(r"13 March 2020, GARCH(1,1) on the US market:", font_size=21, color=GREY_A),
            MathTex(rf"\text{{next day: }} {100 * s['spot_vol']:.0f}\%", font_size=28, color=BAD),
            MathTex(rf"\text{{average over a year: }} {100 * gv[-1]:.0f}\%", font_size=28, color=FC),
            wrapped_label(r"$\sqrt{T}$ assumes volatility stays where it is. GARCH says it mean-reverts, at a half-life of "
                          r"about two months", 4.4, 20, GREY_A),
            wrapped_label(r"also wrong when returns are autocorrelated (Lo--MacKinlay variance ratios) and for "
                          r"quantiles of fat-tailed returns: a 1-day 99\% VaR times $\sqrt{10}$ is not the 10-day VaR "
                          r"(Part 40); the RiskMetrics Technical Document (1996) warns that $\sqrt{T}$ assumes constant "
                          r"variance", 4.4, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).align_to(g, DOWN)
        with self.voiceover(
            "If daily returns are independent with constant volatility, variances add, and volatility grows with the "
            "square root of time: two point two percent over a week, sixteen over a year. <bookmark mark='a'/> On "
            "the thirteenth of March 2020, GARCH put the next day's volatility of the American market at "
            f"{100 * s['spot_vol']:.0f} percent a year. The square-root rule carries that forward forever. "
            "<bookmark mark='b'/> Pause and predict: what does GARCH say for the average over the next year? It does "
            "not carry the spike forward: volatility mean-reverts toward its long-run "
            f"{100 * un:.0f} percent, so the average over the coming year is {100 * gv[-1]:.0f}. "
            "<bookmark mark='c'/> The rule also fails when returns are autocorrelated, and for the tails: ten-day "
            "value at risk is not the one-day figure times the square root of ten when returns are fat-tailed, a "
            "point Part forty returns to. RiskMetrics' own technical document warned that the rule assumes constant "
            "variance. This is the term structure of volatility, and Part ten will read it from option prices."
        ) as vo:
            self.play(FadeIn(ans))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(l_sq), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(l_g), Create(l_u), FadeIn(lu), FadeIn(side[2]), FadeIn(side[3]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()
