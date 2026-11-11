from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import BAD, COST_C, GOOD, HURDLE, PART, RES_C, SPREAD_C, fit_right, load


class Crowding(VoiceoverScene):
    def construct(self):
        n = load("nagel")
        self.card()
        self.liquidity()
        self.test(n)
        self.scatter(n)
        self.limits()
        self.demanders()
        self.quake()
        self.decay()
        self.question()

    def card(self):
        c = chapter_card(9, r"Liquidity, crowding and decay", r"Who pays the stat-arb trader, and when do they stop?",
                         part=PART)
        with self.voiceover("Chapter nine. A reversal strategy buys from people who are selling in a hurry. Its return is "
                            "the price of that hurry. That idea explains when it pays, when it crashes, and why it fades."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def liquidity(self):
        rows = [cmath(r"\text{reversal}", r"=", r"\text{the price of immediacy}", font_size=38, colors={r"\text{reversal}": RES_C}),
                cmath(r"\text{supply of liquidity}", r"\downarrow", r"\text{when market makers' capital is scarce}", font_size=30),
                cmath(r"\mathbb E[\text{reversal return}]", r"\uparrow", r"\text{with the VIX (Nagel 2012)}", font_size=32,
                      colors={r"\text{with the VIX (Nagel 2012)}": HURDLE})]
        whys = [why(r"Grossman and Miller (1988): an investor who must trade now accepts a worse price; whoever takes the "
                    r"other side is paid when the price recovers"),
                why(r"in a crisis, the market makers' own losses and margin calls cut how much risk they can absorb"),
                why(r"Stefan Nagel: short-term reversal returns in US stocks rise with lagged volatility, peaking in 2008: "
                    r"`evaporating liquidity'")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The theory. <bookmark mark='a'/> Sanford Grossman and Merton Miller: an investor who must trade now accepts a "
            "worse price, and whoever takes the other side is paid when the price recovers. Reversal is the price of "
            "immediacy. <bookmark mark='b'/> In a crisis, the liquidity providers' own capital is scarce. "
            "<bookmark mark='c'/> So the expected return of reversal should rise with market stress. Stefan Nagel found "
            "exactly that for American stocks: reversal returns rise with the VIX, and peaked in 2008."
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

    def test(self, n):
        rows = [cmath(r"\pi_{m}", r"=", r"a + b\,\text{VIX}_{m-1} + e_m", font_size=38),
                cmath(r"\hat b", r"=", rf"{1e4 * n['slope']:+.2f}\ \text{{bp per VIX point}},\quad t = {n['t']:.2f}",
                      font_size=32, colors={r"\hat b": HURDLE}),
                cmath(r"\text{Sharpe}", r"=", rf"{n['sharpe']:.2f}\ \ \text{{(1990--2020, monthly)}}", font_size=32,
                      colors={r"\text{Sharpe}": BAD})]
        whys = [why(r"the contrarian's monthly return on the 49 industries against the VIX at the previous month's end"),
                why(r"conventional OLS error, not HAC; a descriptive sample association, not a no-effect proof"),
                why(r"arithmetic sums of daily proxy profits; different universe and design from Nagel's stock study")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"A descriptive industry regression. <bookmark mark='a'/> Monthly outcomes add the daily gross-normalized contrarian P and L arithmetically; they are not compounded portfolio wealth. The predictor is the previous month's last VIX close. <bookmark mark='b'/> The stored slope is {1e4 * n['slope']:+.2f} basis points per VIX point, with t-statistic {n['t']:.2f}. That standard error assumes independent homoskedastic regression errors; it is not HAC robust. <bookmark mark='c'/> Its sample Sharpe is {n['sharpe']:.2f}. These results neither replicate Nagel's stock design nor prove that industry returns contain no liquidity effect."
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

    def scatter(self, n):
        v = np.asarray(n["vix"], float)
        r = 100 * np.asarray(n["ret"], float)
        lim = float(np.ceil(np.percentile(np.abs(r), 99)))
        g = axes([9, 60], [-lim, lim], x_length=7.0, y_length=4.2, xlabel=r"VIX at the previous month's end",
                 ylabel=r"industry contrarian, \% a month", xticks=[10, 30, 50], yticks=[-lim, 0, lim],
                 yfmt=lambda u: f"{u:.0f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(min(a, 60), np.clip(b, -lim, lim)), radius=0.04, color=RES_C, fill_opacity=0.7)
                        for a, b in zip(v, r)])
        zero = DashedLine(ax.c2p(9, 0), ax.c2p(60, 0), color=GREY_C, stroke_width=1)
        st = VGroup(label(rf"calmest fifth of months: {100 * n['low']:+.2f}\%", font_size=16, color=GREY_A),
                    label(rf"most stressed fifth: {100 * n['high']:+.2f}\%", font_size=16, color=GREY_A))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        fit_right(st)
        self.add(g, dots, zero)
        with self.voiceover(
            f"The calmest and most stressed research-sample VIX fifths have mean proxy outcomes {100 * n['low']:+.2f} and {100 * n['high']:+.2f} percent. <bookmark mark='a'/> These groups are defined from this sample's VIX distribution; they are descriptive associations. <bookmark mark='b'/> The scatter clips extreme observations for display. Neither the regression nor these groups identify the causal price of immediacy. Universe, timing, dependence and the return convention all affect the comparison with the stock literature."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.005), FadeIn(st))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def limits(self):
        rows = [cmath(r"\text{capital}_{t+1}", r"=", r"\text{capital}_t \times f(\text{past return})", font_size=34,
                      colors={r"\text{capital}_{t+1}": COST_C}),
                cmath(r"\text{loss}", r"\Rightarrow", r"\text{withdrawals} \Rightarrow \text{forced selling} \Rightarrow "
                      r"\text{wider spread}", font_size=30, colors={r"\text{loss}": BAD}),
                cmath(r"\text{the best trades}", r"=", r"\text{when the arbitrageur has least capital}", font_size=30,
                      colors={r"\text{the best trades}": GOOD})]
        whys = [why(r"Shleifer and Vishny (1997): arbitrageurs manage other people's money, and investors judge them by "
                    r"recent returns"),
                why(r"a spread that widens before it converges costs the arbitrageur capital at exactly the wrong time"),
                why(r"so mispricing can persist and grow: the limits of arbitrage are limits on the arbitrageur's capital, "
                    r"not on the idea")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why a reversal can widen before it closes. <bookmark mark='a'/> Andrei Shleifer and Robert Vishny: "
            "arbitrageurs manage other people's money, and investors judge them by recent returns. "
            "<bookmark mark='b'/> A spread that widens costs the arbitrageur capital, investors withdraw, and the forced "
            "selling widens it further. <bookmark mark='c'/> So the best trades arrive exactly when the arbitrageur has "
            "the least capital to take them. The limits of arbitrage are limits on capital, not on ideas."
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

    def demanders(self):
        cards = VGroup(
            desk_question(r"index changes", r"a stock added to the S\&P 500 must be bought by every index fund on one day; "
                          r"Shleifer (1986) found inclusion raised prices, a demand curve that slopes down", width=12.4,
                          font_size=19),
            desk_question(r"fire sales", r"Coval and Stafford (2007): mutual funds hit by outflows sell the stocks they "
                          r"hold, prices fall below value, and recover over the following months", width=12.4,
                          font_size=19),
            desk_question(r"margin calls and mandates", r"levered funds forced to cut risk, and portfolios rebalanced on a "
                          r"calendar: predictable sellers who care about the date, not the price", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Who demands immediacy, concretely? <bookmark mark='a'/> Index funds when a stock joins an index: they must "
            "buy on one day, and Andrei Shleifer found that inclusion raised prices. <bookmark mark='b'/> Mutual funds "
            "with outflows: Joshua Coval and Erik Stafford showed their forced sales push prices below value, and the "
            "prices recover over the following months. <bookmark mark='c'/> And funds meeting margin calls or "
            "rebalancing on a calendar. Each is a seller who cares about the date rather than the price, and the "
            "stat-arb trader is paid for taking the other side."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def quake(self):
        cards = VGroup(
            desk_question(r"August 2007, again", r"Part 31: the market-neutral stat-arb books lost heavily in three days "
                          r"as a crowd unwound the same positions; Khandani and Lo's contrarian lost and rebounded within "
                          r"the week", width=12.4, font_size=19),
            desk_question(r"why stat arb is crowd-prone", r"the same data, the same factor models, the same residuals and "
                          r"similar bands lead different firms to the same trades", width=12.4, font_size=19),
            desk_question(r"why it rebounds", r"forced selling is immediacy demanded at any price: the cited contrarian research series "
                          r"rebounded sharply; actual funds faced different holdings and funding constraints", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Crowding is the other face of liquidity. <bookmark mark='a'/> August 2007, from Part thirty-one: market-neutral stat-arb books lost heavily in three days as a crowd unwound the same positions, then rebounded. <bookmark mark='b'/> Stat arb is especially prone to crowds, because the same data and the same factor models lead different firms to the same residual trades. <bookmark mark='c'/> And the rebound is the theory again: forced selling is immediacy demanded at any price, and the cited contrarian series rebounded sharply. A rebound in that research series does not prove that every fund could hold its positions, avoid margin calls or earn the same return."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def decay(self):
        cards = VGroup(
            desk_question(r"competition", r"Avellaneda and Lee found their residual strategy's returns on US stocks fell "
                          r"after the early 2000s; the distance rule decayed after the 1980s (Do and Faff)", width=12.4,
                          font_size=19),
            desk_question(r"speed", r"as more firms trade the same reversal, it is harvested faster: the edge moves to "
                          r"shorter horizons, intraday and then to market making (Part 38)", width=12.4, font_size=19),
            desk_question(r"costs decide", r"what remains is a few basis points a trade, and the firm with the cheapest "
                          r"execution keeps it: Chapter 10's book is judged net of costs", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "And decay. <bookmark mark='a'/> Avellaneda and Lee found that their residual strategy's returns on American "
            "stocks fell after the early 2000s, as the distance rule had after the 1980s. <bookmark mark='b'/> As more "
            "firms trade a reversal, it is harvested faster, and the edge moves to shorter horizons, then into market "
            "making, Part thirty-eight's subject. <bookmark mark='c'/> What remains is a few basis points a trade, and the "
            "firm with the cheapest execution keeps it."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a reversal strategy earns 2 bp a day before costs and trades 40\% of its book daily at 5 bp per "
                       r"side. What does it earn after costs?")
        working = MathTex('\\mu_g=2\\ \\mathrm{bp/day},\\quad \\tau=\\sum_j|\\Delta w_j|=0.4,\\quad k=5\\ \\mathrm{bp},\\quad \\mu_n=\\mu_g-k\\tau', font_size=32).move_to(UP * 0.8)
        if working.width > 12.1:
            working.scale_to_fit_width(12.1)
        setup_note = wrapped_label('Define turnover as the sum of absolute one-way traded weights. If turnover instead means half that sum, the cost factor changes.', 11.7, 23).move_to(DOWN * 0.9)
        self.add(working, setup_note, q)
        with self.voiceover(
            "Pause and predict. A reversal strategy earns two basis points a day before costs, and trades forty percent "
            "of its book daily at five basis points a side. What does it earn after costs?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
