from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, GOOD, IM_C, PART, ask, fit_right, illustration, load


class IM(VoiceoverScene):
    def construct(self):
        m = load("im")
        self.card()
        self.rules()
        self.derive()
        self.simm(m)
        self.schedule(m)
        self.profile(m)
        self.tradeoff(load("imcva"))

    def card(self):
        c = chapter_card(8, r"Initial margin", r"How much must each side post in advance?", part=PART)
        with self.voiceover("Chapter eight. Initial margin: collateral posted in advance, against the gap."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rules(self):
        rows = [cmath(r"\text{IM}", r"\approx", r"\text{the 99th percentile of the 10-day change in value}", font_size=36,
                      colors={r"\text{IM}": IM_C}),
                cmath(r"\text{IM}_{\text{SIMM}}", r"=", r"\sqrt{\textstyle\sum_{k,l} \rho_{kl}\,WS_k\,WS_l},\quad WS_k = "
                      r"RW_k\,s_k", font_size=36, colors={r"\text{IM}_{\text{SIMM}}": IM_C})]
        whys = [why(r"variation margin settles yesterday's move; initial margin covers the move during the margin period "
                    r"of risk, posted by both sides to a third party, and not re-usable. Required for uncleared "
                    r"derivatives between large firms in phases from September 2016 to September 2022"),
                why(r"ISDA's Standard Initial Margin Model: sensitivities $s_k$ by risk factor (here, DV01 by tenor), "
                    r"risk weights, and correlations that let offsetting tenors net. The weights here are illustrative, "
                    r"not ISDA's calibration")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Variation margin covers yesterday's move. Initial margin is posted in advance, by both sides, to cover the "
            "move during the margin period of risk, at about the ninety-ninth percentile, and it is held by a third "
            "party, so it cannot be re-used. After 2008, regulators required it between large firms for derivatives "
            "that are not centrally cleared, phased in from 2016 to 2022. <bookmark mark='a'/> To agree on the number, "
            "the industry wrote a common model, ISDA's SIMM: sensitivities by risk factor, times risk weights, "
            "combined with correlations so that offsetting positions net."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\Delta V", r"\approx", r"\textstyle\sum_k s_k\,\Delta r_k", font_size=40, colors={r"\Delta V": IM_C}),
                cmath(r"\text{sd}(\Delta V)", r"=", r"\sqrt{\textstyle\sum_{k,l}\rho_{kl}\,(\sigma_k s_k)(\sigma_l s_l)}",
                      font_size=38),
                cmath(r"q_{99}", r"=", r"2.33\,\text{sd}(\Delta V) = \sqrt{\textstyle\sum_{k,l}\rho_{kl}\,WS_k\,WS_l},\ "
                      r"RW_k = 2.33\,\sigma_k", font_size=34, colors={r"q_{99}": IM_C})]
        whys = [why(r"over ten days the change in value is, to first order, each sensitivity times its rate's move"),
                why(r"if the moves are normal with volatilities $\sigma_k$ (over ten days) and correlations $\rho_{kl}$, "
                    r"the variance is a quadratic form"),
                why('so the 99th percentile is the square root of the same form with each sensitivity scaled by its risk weight. This normal delta-only quadratic form motivates a SIMM-style illustration; full SIMM uses prescribed risk classes, buckets, concentration, vega and curvature rules')]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            'A normal delta approximation motivates the quadratic form. <bookmark mark="a"/> Linearize value in rate sensitivities. <bookmark mark="b"/> Under joint normal moves, variance is a covariance quadratic form. <bookmark mark="c"/> For a zero-mean one-sided ninety-nine percent normal quantile, multiply standard deviation by about two point three three. That explains our illustrative risk-weighted aggregation. Full ISDA SIMM is a prescribed methodology with risk classes, buckets, concentration, vega and curvature, not simply this normal formula. Our fixed weights and neglected floating-leg risk are not the current regulatory calibration.'
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def simm(self, m):
        keys, dv = np.asarray(m["keys"]), np.asarray(m["dv01"]) * 1e3
        g = axes([-0.5, 8.5], [-80, 30], x_length=7.2, y_length=4.2, xlabel=r"tenor",
                 ylabel=r"key-rate DV01, \$ thousand per bp", xticks=[], yticks=[-80, -40, 0, 20], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(-0.5, 0), ax.c2p(8.5, 0), color=WHITE, stroke_width=1.2)
        bars = VGroup()
        for i, (k, v) in enumerate(zip(keys, dv)):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            bars.add(VGroup(Rectangle(width=0.55, height=max(abs(y1 - y0), 0.01), stroke_width=0,
                                      fill_color=BAD if v < 0 else GOOD, fill_opacity=0.8).move_to(
                [ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]), label(f"{k:g}y", font_size=15).next_to(ax.c2p(i, -80), DOWN, buff=0.1)))
        side = VGroup(
            MathTex(rf"\text{{IM}} = \${m['im']:.1f}\text{{m}}", font_size=32, color=IM_C),
            label(r"on \$200 million of swaps", font_size=19, color=GREY_A),
            wrapped_label(r"the book's risk sits at 3, 5 and 10 years and partly offsets: pay 10 years, receive 5. Without "
                          r"the correlations the margin would be the sum of the parts", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "For the netting set: its rate sensitivity tenor by tenor, in thousands of dollars a basis point. "
            "<bookmark mark='a'/> The ten-year payer dominates, partly offset by the five-year receiver. "
            f"<bookmark mark='b'/> Weighted and combined, the initial margin is about {m['im']:.1f} million dollars, "
            "posted by each side, on two hundred million of swaps."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def schedule(self, m):
        rows = [cmath(r"\text{IM}_{\text{sched}}", r"=", r"\big(0.4 + 0.6\,\text{NGR}\big)\textstyle\sum_i w_i\,N_i,\quad "
                      r"\text{NGR} = \frac{\text{net replacement cost}}{\text{gross replacement cost}}", font_size=32,
                      colors={r"\text{IM}_{\text{sched}}": IM_C})]
        whys = [why(r"the regulators' fallback (BCBS--IOSCO, 2015): a percentage of notional by asset class and "
                    r"maturity; for interest rates 1\% under two years, 2\% from two to five, 4\% beyond. Netting only "
                    r"through the ratio NGR")]
        step = ladder(self, rows, whys, keep=1, top=2.7, x=-0.4, buff=0.8, edge=6.9)
        trades = [(r"10-year payer, \$100m", 0.04, 100.0), (r"5-year receiver, \$60m", 0.02, 60.0),
                  (r"3-year payer, \$40m", 0.02, 40.0)]
        hx = [-3.6, 0.0, 3.2]
        tab = VGroup(VGroup(*[label(t_, font_size=18, color=GREY_A).move_to([x, 0.2, 0]) for t_, x in
                              zip([r"trade", r"schedule weight", r"margin, \$m"], hx)]))
        for i, (nm, w_, n_) in enumerate(trades):
            y = -0.35 - 0.48 * i
            tab.add(VGroup(label(nm, font_size=18).move_to([hx[0], y, 0]),
                           MathTex(rf"{100 * w_:g}\%", font_size=24).move_to([hx[1], y, 0]),
                           MathTex(f"{w_ * n_:.1f}", font_size=24).move_to([hx[2], y, 0])))
        gross = sum(w_ * n_ for _, w_, n_ in trades)
        tot = VGroup(label(r"schedule, no netting credit", font_size=18, color=BAD).move_to([hx[0], -1.95, 0]),
                     MathTex(f"{gross:.1f}", font_size=28, color=BAD).move_to([hx[2], -1.95, 0]),
                     label(r"SIMM-style, with offsets", font_size=18, color=IM_C).move_to([hx[0], -2.45, 0]),
                     MathTex(f"{m['im']:.1f}", font_size=28, color=IM_C).move_to([hx[2], -2.45, 0]))
        with self.voiceover(
            "Firms need not use a model at all. The regulators' fallback is a schedule: a fixed percentage of "
            "notional, by asset class and maturity, with netting allowed only through one ratio of net to gross "
            "replacement cost. <bookmark mark='a'/> For our three swaps: four percent of the ten-year's notional, two "
            f"percent of the others', {gross:.0f} million dollars before any netting credit. <bookmark mark='b'/> The "
            f"sensitivity-based model, which sees that the five-year receiver offsets part of the ten-year payer, asks "
            f"for {m['im']:.1f}. The schedule is simple and blunt, and so expensive for hedged books that almost "
            "every large dealer adopted the industry model instead."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(tot[0]), FadeIn(tot[1]))
            vo.wait_until("b")
            self.play(FadeIn(tot[2]), FadeIn(tot[3]))
        self.wait(0.4)
        self.clear_scene()

    def profile(self, m):
        t, p = np.asarray(m["times"]), np.asarray(m["profile"])
        g = axes([0, 10], [0, max(p) * 1.2], x_length=7.4, y_length=4.2, xlabel=r"years", ylabel=r"initial margin, \$ million",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 1, 2, 3], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, p, IM_C, stroke_width=3.5)
        side = wrapped_label(r"initial margin falls as the swaps run off, and is funded every day it is posted: the "
                             r"funding cost of this profile is MVA (chapter 5). For a dealer with thousands of trades, "
                             r"margin became one of the largest uses of cash", 3.8, 18, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The margin must be funded for as long as the trades live. <bookmark mark='a'/> As the swaps run off, the "
            "required margin falls, step by step. The cost of funding this whole profile is the margin valuation "
            "adjustment of chapter five; for large dealers, posting margin became one of the biggest uses of cash on "
            "the balance sheet."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def tradeoff(self, k):
        rows = k["rows"]
        qs = [r_["q"] for r_ in rows]
        cv = np.array([r_["cva"] for r_ in rows]) * 1e3
        mv = np.array([r_["mva"] for r_ in rows]) * 1e3
        g = axes([-0.5, 4.5], [0, 140], x_length=7.4, y_length=4.2, xlabel=r"initial margin set at the quantile",
                 ylabel=r"\$ thousand, first 3 years", xticks=[], yticks=[0, 40, 80, 120], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (a, b, q_) in enumerate(zip(cv, mv, qs)):
            grp = VGroup()
            for dx, val, c_ in ((-0.17, a, BAD), (0.17, b, IM_C)):
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, val)[1]
                grp.add(Rectangle(width=0.3, height=max(y1 - y0, 0.01), stroke_width=0, fill_color=c_,
                                  fill_opacity=0.85).move_to([ax.c2p(i + dx, 0)[0], (y0 + y1) / 2, 0]))
            grp.add(label(r"none" if q_ == 0 else rf"{100 * q_:g}\%", font_size=16).next_to(ax.c2p(i, 0), DOWN, buff=0.12))
            bars.add(grp)
        side = VGroup(
            legend([(BAD, r"CVA left after margin"), (IM_C, r"MVA: funding the margin")], font_size=17),
            MathTex(rf"\text{{IM at 99\%}} = \${rows[3]['im']:.1f}\text{{m}}", font_size=26, color=IM_C),
            wrapped_label(r"the netting set with daily variation margin and a 10-day margin period, over its first three "
                          r"years; funding at 80 bp. Initial margin all but removes the remaining credit risk, and costs "
                          r"several times more to fund than the risk it removed", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Is initial margin worth what it costs? Take the netting set with daily variation margin, over its first "
            f"three years. <bookmark mark='a'/> With no initial margin, the credit adjustment left is about "
            f"{cv[0]:.0f} thousand dollars: the gap risk. <bookmark mark='b'/> Margin at the ninety-ninth percentile "
            f"cuts it to {cv[3]:.1f} thousand, but funding that margin costs {mv[3]:.0f}. At ninety-nine point nine, "
            f"{mv[4]:.0f} thousand of funding removes the last fraction. <bookmark mark='c'/> For one bank, initial "
            "margin is an expensive way to buy protection. Regulators required it anyway, because it is not meant for "
            "the bank: it is there so that when a large dealer fails, its losses stay with it instead of spreading to "
            "everyone it traded with."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars[1:]], lag_ratio=0.3), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"initial margin is set at the 99th percentile of a 10-day move. What happens to it, and to everyone "
                r"posting it, the day volatility doubles?")
        with self.voiceover("Initial margin is set at the ninety-ninth percentile of ten days' moves. What happens to it, "
                            "and to everyone posting it, the day volatility doubles?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
