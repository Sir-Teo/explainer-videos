from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, COMB, GOOD, HURDLE, OOS_C, PART, TRAIN_C, comma, fit_right, load, tt


class Envelope(VoiceoverScene):
    def construct(self):
        e = load("envelope")
        self.card()
        self.register(e)
        self.research(e)
        self.opened(e)
        self.years(e)
        self.checks(e)
        self.reading(e)
        self.question(e)

    def card(self):
        c = chapter_card(13, r"The mined combination, registered and opened", r"Did the patterns the miners found survive "
                         r"five sealed years?", part=PART)
        with self.voiceover("Chapter thirteen. One strategy from this part's mining, registered with every trial counted, "
                            "and opened once on the sealed years 2021 to 2025."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def register(self, e):
        card = firm_card(r"The mined combination", rf"the {e['K']} best random formulas by 2018--19 IC, de-duplicated; their "
                         r"daily long-short books combined with mean-variance weights fitted on 2018--2020, the number "
                         r"of formulas chosen by its 2020 Sharpe ratio; rebalanced at each day's close",
                         numbers=((comma(e["n_trials"]), r"trials: Chapter 8's count"),
                                  (r"10\ \text{bp}", rf"a round trip, on the measured turnover of {e['turnover']:.2f} "
                                                     r"dollars a day per dollar long: the cost charged")),
                         kind=r"Registered", width=10.6, font_size=22).move_to(UP * 0.5)
        ctr = MathTex(rf"\text{{the counter}}:\ {comma(e['trials'] - e['n_trials'])}\ \to\ {comma(e['trials'])}", font_size=30,
                      color=QC.HOUSE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"The registration. <bookmark mark='a'/> The {e['K']} best random formulas, each traded as a daily long-short "
            "book, combined with weights estimated on 2018 to 2020. The number of formulas was chosen by the estimated "
            "combination's score on 2020, a rule written before Chapter seven's comparison, and kept: equal weights look "
            "better there, but switching now would be a second look. <bookmark mark='b'/> "
            f"{comma(e['n_trials']).replace('{,}', ',')} trials, and costs of ten basis points a round trip on the "
            f"turnover the book actually needs. The counter moves to {comma(e['trials']).replace('{,}', ',')}."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(ctr))
        self.wait(0.4)
        self.clear_scene()

    def _cum(self, dates, cum, color, title):
        d = np.asarray(dates)
        x = d // 10000 + ((d // 100) % 100 - 1) / 12 + (d % 100) / 365
        y = 100 * np.asarray(cum, float)
        lo, hi = float(min(y.min(), 0) - 2), float(max(y.max(), 0) + 2)
        step = 20 if hi - lo > 60 else 10
        g = axes([x[0], x[-1]], [lo, hi], x_length=7.0, y_length=4.2, xlabel=title,
                 ylabel=r"cumulative log return, \% of the long side", xticks=list(range(int(np.ceil(x[0])), int(x[-1]) + 1)),
                 yticks=[0, step * math.floor(hi / step)], xfmt=lambda v: f"{v:.0f}", font_size=14)
        ax = g.ax
        line = curve(ax, x, y, color, stroke_width=3)
        zero = DashedLine(ax.c2p(x[0], 0), ax.c2p(x[-1], 0), color=GREY_B, stroke_width=1.5)
        return VGroup(g, zero), line

    def research(self, e):
        g1, l1 = self._cum(e["res_dates"], e["cum_res"], TRAIN_C, r"2018--2020: the research years")
        r = e["row"]["research"]
        VGroup(g1, l1).move_to(LEFT * 2.2 + DOWN * 0.2)
        side = VGroup(MathTex(rf"SR = {r['sharpe']:.2f} \pm {r['sharpe_se']:.2f}", font_size=26, color=TRAIN_C),
                      MathTex(rf"\text{{net of costs}}:\ {r['sharpe_net']:.2f}", font_size=24),
                      wrapped_label(r"monthly returns, annualised; the weights were fitted on these years, so this is "
                                    r"what was promised, not evidence", 3.4, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                  buff=0.25).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "First, the research years, on which everything was chosen. <bookmark mark='a'/> A Sharpe ratio of "
            f"{r['sharpe']:.2f} before costs, {r['sharpe_net']:.2f} after. That is the promise, and promises from a search "
            "of thirteen thousand formulas are cheap."
        ) as vo:
            self.play(FadeIn(g1))
            vo.wait_until("a")
            self.play(Create(l1), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def opened(self, e):
        g2, l2 = self._cum(e["hold_dates"], e["cum_hold"], OOS_C, r"2021--2025: sealed until now")
        h = e["row"]["holdout"]
        VGroup(g2, l2).move_to(LEFT * 2.2 + DOWN * 0.2)
        side = VGroup(MathTex(rf"SR = {h['sharpe']:.2f} \pm {h['sharpe_se']:.2f}", font_size=26, color=OOS_C),
                      MathTex(rf"\text{{net of costs}}:\ {h['sharpe_net']:.2f}", font_size=24),
                      MathTex(rf"\text{{worst fall}}\ {100 * h['maxdd']:.1f}\%", font_size=24),
                      MathTex(rf"{h['n']}\ \text{{months}}", font_size=24)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.25).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "Then the envelope. <bookmark mark='a'/> Five years the miners never saw: a crypto boom, the crash of 2022, "
            "and the recovery. <bookmark mark='b'/> The combination rose steadily through all of it. A Sharpe ratio of "
            f"{h['sharpe']:.2f} with a standard error of {h['sharpe_se']:.2f} before costs, {h['sharpe_net']:.2f} after, "
            f"and a worst fall of {abs(100 * h['maxdd']):.1f} percent. The patterns the miners found were not noise."
        ) as vo:
            self.play(FadeIn(g2))
            vo.wait_until("a")
            self.play(Create(l2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def years(self, e):
        by = e["by_year"]
        ys = sorted(by)
        vals = [by[y] for y in ys]
        top = float(np.ceil(max(vals)))
        g = axes([2020.4, 2025.6], [0, top], x_length=7.0, y_length=4.0, xlabel=r"", ylabel=r"Sharpe ratio that year, "
                 r"daily returns annualised, before costs", xticks=[2021, 2022, 2023, 2024, 2025], yticks=[0, top / 2, top],
                 xfmt=lambda v: f"{v:.0f}", font_size=14).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.6, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=OOS_C, fill_opacity=0.85).move_to(ax.c2p(int(y), 0), aligned_edge=DOWN)
                      for y, v in zip(ys, vals)])
        labs = VGroup(*[MathTex(f"{v:.1f}", font_size=22).next_to(b, UP, buff=0.1) for b, v in zip(bars, vals)])
        side = wrapped_label(rf"the coin market, equal-weighted, over the same years: a Sharpe ratio of "
                             rf"{e['sr_market']:.2f}", 3.4, 15, GREY_A).to_edge(RIGHT, buff=0.5)
        fit_right(side)
        with self.voiceover(
            "Year by year. <bookmark mark='a'/> Positive in every one of the five, weakest in the boom of 2021 and "
            "strongest in the years after. <bookmark mark='b'/> Over the same years an equal-weighted basket of the coins "
            f"themselves had a Sharpe ratio of {e['sr_market']:.2f}. The book did not need the market to rise."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), FadeIn(labs))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def checks(self, e):
        h = e["row"]["holdout"]
        c10 = e["cost_year"]
        be = 10 * h["mean"] / c10
        net20 = (h["mean"] - 2 * c10) / h["vol"]
        m = e["n_registered"]
        bar = math.sqrt(2 * math.log(m))
        z_g, z_n = h["sharpe"] / h["sharpe_se"], h["sharpe_net"] / h["sharpe_se"]
        rows = [cmath(r"\text{break-even cost}", r"=", rf"10\ \text{{bp}} \times \frac{{{100 * h['mean']:.1f}\%}}"
                      rf"{{{100 * c10:.1f}\%}} \approx {be:.0f}\ \text{{bp a round trip}}", font_size=30,
                      colors={r"\text{break-even cost}": HURDLE}),
                cmath(r"\text{at 20 bp}", r":", rf"SR_{{\text{{net}}}} = {net20:.2f}", font_size=30),
                cmath(r"\beta_{\text{market}}", r"=", rf"{e['beta']:+.2f},\quad SR\ \text{{after hedging it}} = "
                      rf"{e['sr_hedged']:.2f}", font_size=30, colors={r"\beta_{\text{market}}": COMB}),
                cmath(rf"\sqrt{{2\ln {m}}} = {bar:.2f}", r"\ \text{vs}\ ", rf"\tfrac{{SR}}{{\text{{s.e.}}}} = {z_g:.1f}\ "
                      rf"\text{{gross}},\ {z_n:.1f}\ \text{{net}}", font_size=30)]
        whys = [why(r"the cost per round trip at which the hold-out's mean return would be used up"),
                why(r"Binance's standard spot fee is 0.1\% a side: 20 basis points a round trip before any spread"),
                why(r"the book's beta to the equal-weighted coin market (daily); it is close to market neutral"),
                why(rf"the series has opened {m} envelopes: the best of {m} pure-noise hold-outs would sit about "
                    r"$\sqrt{2\ln m}$ standard errors up")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Now the checks a sceptic would run. <bookmark mark='a'/> Costs: the edge would be used up at about "
            f"{be:.0f} basis points a round trip. <bookmark mark='b'/> A standard Binance account pays twenty, before "
            f"the spread, and at twenty the Sharpe ratio is {net20:.2f}: the edge belongs to whoever trades cheapest. "
            "<bookmark mark='c'/> The market: the book's beta to the coin market is close to zero, and hedging it leaves "
            f"a Sharpe ratio of {e['sr_hedged']:.2f}. <bookmark mark='d'/> And the series' own multiple testing: of "
            f"{m} envelopes opened, the luckiest pure-noise one would sit about {bar:.1f} standard errors up. This one "
            f"is {z_g:.1f} before costs, which clears it, and {z_n:.1f} after, which does not."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def reading(self, e):
        cards = VGroup(
            desk_question(r"what was found", r"not ten thousand ideas but a few, above all that calm coins beat wild ones "
                          r"the next day: a low-volatility effect, of the kind Part 24 met in stocks", width=12.4,
                          font_size=19),
            desk_question(r"why it may not be money", r"the short side means borrowing coins or using perpetual futures, "
                          r"with their own costs; fees and spreads take most of the edge; and the backtest trades at the "
                          r"close it measures", width=12.4, font_size=19),
            desk_question(r"what the Track Record keeps", r"the row, gross and net, with the trials counted; the finale "
                          r"deflates it with everything else", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What to make of it. <bookmark mark='a'/> The miners found something real, but it was not ten thousand ideas. "
            "It was a few, above all that calm coins beat wild ones the next day: a low-volatility effect of the kind Part "
            "twenty-four met in stocks. <bookmark mark='b'/> Why it may still not be money: the short side requires "
            "borrowing coins or using perpetual futures, which have their own costs; fees and spreads take most of the "
            "edge; and the backtest trades at the very close it uses to compute the signal, which in practice means a "
            "little later and a little worse. <bookmark mark='c'/> The Track Record keeps the row, gross and net, with "
            "its trials counted, and the finale deflates it with everything else."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self, e):
        h = e["row"]["holdout"]
        mu, cst, vol = 100 * h["mean"], 100 * e["cost_year"], 100 * h["vol"]
        q = pause_card(rf"the hold-out earned {mu:.0f}\% a year before costs and the costs at 10 bp were {cst:.0f}\%. "
                       rf"What Sharpe ratio remains at 30 bp, with a volatility of {vol:.0f}\%?")
        with self.voiceover(
            f"Pause and predict. The hold-out earned about {mu:.0f} percent a year before costs, and costs at ten basis "
            f"points were about {cst:.0f} percent. With a volatility of {vol:.0f} percent, what Sharpe ratio is left at "
            "thirty basis points?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
