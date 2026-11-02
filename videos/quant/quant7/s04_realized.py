from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data, tbar


class Realized(VoiceoverScene):
    def construct(self):
        z = load("realized")
        self.card()
        self.measures(z)
        self.har(load("har"))

    def card(self):
        c = chapter_card(3, r"Realized volatility and HAR", r"Can you measure volatility after the fact?", part=PART)
        with self.voiceover("Chapter three. Realized volatility, and the HAR model."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def measures(self, z):
        names = [("vol_rv1", r"RV,\\1-minute", BAD), ("vol_rv5", r"RV,\\5-minute", RET), ("vol_tsrv", r"two-scale\\RV", VOL),
                 ("vol_rk", r"realized\\kernel", VOL), ("vol_bv", r"bipower\\(no jumps)", ALT)]
        g = axes([0, len(names)], [0, 1.2], x_length=7.4, y_length=4.2, ylabel=r"Bitcoin's average volatility, Aug.\ 2017 -- 2020",
                 xticks=[], yticks=[0, 0.4, 0.8, 1.2], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[tbar(ax, i + 0.5, z[k], c, width=0.55) for i, (k, _, c) in enumerate(names)])
        vals = VGroup(*[MathTex(f"{100 * z[k]:.0f}\\%", font_size=24, color=c).next_to(b, UP, buff=0.06)
                        for (k, _, c), b in zip(names, bars)])
        labs = VGroup(*[Tex(r"\begin{tabular}{c}" + n_ + r"\end{tabular}", font_size=17,
                            color=GREY_A).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.1) for i, (_, n_, _) in enumerate(names)])
        side = VGroup(
            wrapped_label(r"sampling every minute picks up bid--ask bounce: microstructure noise inflates RV (Part 5's "
                          r"signature plot)", 4.6, 21, GREY_A),
            wrapped_label(r"two-scale RV (Zhang, Mykland and A\"it-Sahalia 2005) averages sparse grids and subtracts the "
                          r"noise; the realized kernel (Barndorff-Nielsen, Hansen, Lunde and Shephard 2008) adds weighted "
                          r"autocovariances", 4.6, 21, VOL),
            MathTex(rf"\text{{jumps: }} {100 * z['jump_share']:.0f}\% \text{{ of the variance}}", font_size=30, color=ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(rf"Binance BTCUSDT one-minute candles; {z['n_days']:,} days".replace(",", "{,}"))
        with self.voiceover(
            "Part five showed that sampling faster doesn't measure volatility better forever: at the finest scales the "
            "bid-ask bounce adds noise. Over three and a half years of Bitcoin, the sum of squared one-minute returns "
            "gives an average volatility of a hundred and six percent; five-minute returns give ninety-six. "
            "<bookmark mark='a'/> Two estimators use all the data and correct for the noise: the two-scale estimator, "
            "which averages several sparse grids and subtracts the noise measured on the dense one, and the realized "
            "kernel, which adds back the autocovariances the noise creates. Both land near ninety-three. "
            "<bookmark mark='b'/> Bipower variation, which multiplies neighbouring absolute returns so that a single "
            "jump barely counts, gives ninety-two: jumps carry about a tenth of Bitcoin's daily variance."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(labs), GrowFromEdge(bars[0], DOWN), FadeIn(vals[0]),
                      GrowFromEdge(bars[1], DOWN), FadeIn(vals[1]), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(vals[2]), GrowFromEdge(bars[3], DOWN), FadeIn(vals[3]),
                      FadeIn(side[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[4], DOWN), FadeIn(vals[4]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def har(self, h):
        eq = MathTex(r"RV_{t+1}", r"=", r"b_0", r"+ b_d\,RV_t", r"+ b_w\,\overline{RV}_{t-4:t}", r"+ b_m\,\overline{RV}_{t-21:t}",
                     font_size=36).to_edge(UP, buff=0.55)
        eq[0].set_color(VOL)
        eq[3].set_color(BAD)
        eq[4].set_color(RET)
        eq[5].set_color(GOOD)
        src = label(r"HAR (Corsi 2009): a day, a week and a month of past realized variance, fitted by least squares",
                    font_size=20, color=GREY_A).next_to(eq, DOWN, buff=0.15)
        tt = np.asarray(h["cascade_t"])
        g = axes([2019, 2020], [0, 2.0], x_length=6.8, y_length=4.2, ylabel=r"Bitcoin's volatility in 2019, annualised",
                 xticks=[2019, 2019.5, 2020], xfmt=lambda u: {2019: "Jan", 2019.5: "Jul", 2020: "Jan"}[round(u * 2) / 2],
                 yticks=[0, 0.5, 1.0, 1.5, 2.0], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16)
        g.to_edge(LEFT, buff=0.6).to_edge(DOWN, buff=0.75)
        ax = g.ax
        cd = curve(ax, tt, np.clip(h["cascade_d"], 0, 2.0), BAD, stroke_width=1.2).set_stroke(opacity=0.7)
        cw = curve(ax, tt, np.clip(h["cascade_w"], 0, 2.0), RET, stroke_width=2.5)
        cm = curve(ax, tt, np.clip(h["cascade_m"], 0, 2.0), GOOD, stroke_width=4)
        leg = legend([(BAD, r"yesterday"), (RET, r"last week"), (GOOD, r"last month")], font_size=18)
        leg.move_to(ax.c2p(2019.85, 1.75))
        b, t = h["HAR"]["beta"], h["HAR"]["t"]
        bq, tq = h["HARQ"]["beta"], h["HARQ"]["t"]

        def row(name, val, tv, color):
            return VGroup(MathTex(name, font_size=30, color=color), MathTex(f"{val:.2f}", font_size=30, color=color),
                          MathTex(f"({tv:.1f})", font_size=26, color=GREY_B))

        rows = [row(r"b_d", b[1], t[1], BAD), row(r"b_w", b[2], t[2], RET), row(r"b_m", b[3], t[3], GOOD)]
        tab = VGroup(*[m for r in rows for m in r]).arrange_in_grid(rows=3, cols=3, buff=(0.5, 0.22),
                                                                   col_alignments="lrr")
        head = label(r"fitted on Bitcoin, 2017--2019 (Newey--West $t$)", font_size=20, color=GREY_A)
        r2 = label(rf"$R^2 = {h['HAR']['r2']:.2f}$ on {h['HAR']['n']} days", font_size=20, color=GREY_A)
        harq = VGroup(MathTex(r"b_d \to b_d + b_q\sqrt{RQ_t}", font_size=32, color=ALT),
                      MathTex(rf"b_q = {bq[4]:.1f}\ \ (t = {tq[4]:.1f})", font_size=28, color=ALT),
                      wrapped_label(r"HARQ (Bollerslev, Patton and Quaedvlieg 2016): trust yesterday less when it was "
                                    rf"measured noisily. The sign is right; on {h['HARQ']['n']} days of Bitcoin it is not significant.",
                                    4.6, 19, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        side = VGroup(head, tab, r2, harq).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        side.align_to(g, DOWN).shift(UP * 0.1)
        with self.voiceover(
            "With a daily realized variance in hand, forecasting becomes a regression. Fulvio Corsi's HAR model of 2009 "
            "predicts tomorrow's realized variance from three averages of the past. <bookmark mark='a'/> Yesterday, "
            "which jumps around; the last week; and the last month, which moves slowly. The idea is a market of "
            "traders at different horizons, each reacting to volatility at their own scale. <bookmark mark='b'/> "
            "Fitted on Bitcoin through 2019, yesterday and the last month carry the weight, with coefficients of about "
            "four tenths each. Four numbers and least squares reproduce the long memory that GARCH needs persistence "
            "near one to approximate. <bookmark mark='c'/> In 2016 Tim Bollerslev, Andrew Patton and Rogier "
            "Quaedvlieg added one refinement: when yesterday's realized variance was measured with a lot of error, "
            "trust it less. On Bitcoin the correction has the right sign, but with three years of data it is not "
            "significant. The race will say whether it helps."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(leg), Create(cd), run_time=1.5)
            self.play(Create(cw), Create(cm), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), FadeIn(r2))
            vo.wait_until("c")
            self.play(FadeIn(harq))
        self.wait(0.5)
        self.clear_scene()
