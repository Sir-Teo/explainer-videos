from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import BAD, GOOD, HURDLE, PART, PERP_C, SPOT_C, load


class Carry(VoiceoverScene):
    def construct(self):
        c = load("carry")
        self.card()
        self.book()
        self.risks()
        self.variants(c)
        self.register(c)
        self.opened(c)
        self.years(c)
        self.curve_(c)
        self.decay(c)
        self.hidden_tail(c)
        self.premium()
        self.question()

    def card(self):
        cd = chapter_card(7, r"The carry trade, registered", r"Is collecting funding free money?", part=PART)
        with self.voiceover(
            "Chapter seven, and the answer to the pause: three things. Funding can turn negative, so the desk pays. A "
            "rally makes the short perpetual lose on margin before the spot gain can be used, so it needs spare "
            "capital. And the exchange can fail, taking everything held there. This chapter registers the trade, opens "
            "the sealed hold-out, and then asks what its returns do not show."
        ):
            self.play(FadeIn(cd[0], shift=UP * 0.2), FadeIn(cd[1]))
        self.play(FadeOut(cd))

    def book(self):
        rows = [cmath(r"\text{long } 1 \text{ spot}", r"+", r"\text{short } 1 \text{ perpetual}", font_size=40,
                      colors={r"\text{long } 1 \text{ spot}": SPOT_C, r"\text{short } 1 \text{ perpetual}": PERP_C}),
                cmath(r"\text{P\&L}", r"=", r"\text{funding received} + \Delta(S - F)", font_size=40),
                cmath(r"\text{capital}", r"=", r"\text{spot} + \tfrac13 \text{ margin}", font_size=40),
                cmath(r"\text{cost}", r"=", r"15\ \text{bp to enter or leave}", font_size=40)]
        whys = [why(r"the position has no exposure to the coin's price"),
                why(r"it earns funding at each settlement, plus or minus the change in the perpetual's premium"),
                why(r"the spot is bought outright; the short perpetual is margined at a third of its value, so a dollar "
                    r"of spot needs $\$1.33$ of capital"),
                why(r"7.5 bp on each leg; variants that switch on and off pay it at each switch")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The book. <bookmark mark='a'/> Long one unit of spot, short one unit of the perpetual: no exposure to the "
            "coin's price. <bookmark mark='b'/> It earns the funding at each settlement, plus or minus changes in the "
            "premium. <bookmark mark='c'/> The spot is bought outright and the short is margined at a third of its "
            "value, so each dollar of spot needs a dollar thirty-three of capital. <bookmark mark='d'/> And entering or "
            "leaving costs fifteen basis points."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def risks(self):
        cards = VGroup(
            desk_question(r"funding turns negative", r"in crashes shorts pay; a book that is always on pays through those "
                          r"spells", width=12.4, font_size=19),
            desk_question(r"the short leg is margined", r"a 50\% rally costs the short half its notional before the spot's "
                          r"gain can be moved across; without spare capital it is liquidated, and the hedge is gone",
                          width=12.4, font_size=19),
            desk_question(r"the venue and the dollar", r"the exchange can fail, and the stablecoin the trade is quoted in "
                          r"can lose its peg", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What can go wrong, before any data. <bookmark mark='a'/> Funding turns negative in crashes, and a book that "
            "is always on pays through them. <bookmark mark='b'/> The short leg is margined: a fifty percent rally costs "
            "it half its notional before the spot's gain can be moved across, and without spare capital it is "
            "liquidated and the hedge is gone. <bookmark mark='c'/> And the venue can fail, and the stablecoin that "
            "everything is quoted in can lose its peg."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def variants(self, c):
        hx = [-4.4, -2.2, 0.0, 2.2, 4.4]
        head = VGroup(*[label(t, font_size=15, color=GREY_B) for t in (r"asset", r"rule", r"a year", r"Sharpe",
                                                                         r"worst drawdown")])
        tab = VGroup(head)
        rn = {"always": r"always on", "pos7": r"7-day funding $> 0$", "hurdle7": r"7-day funding $> 5\%$"}
        for v in c["variants"]:
            best = v["asset"] == c["best"]["asset"] and v["rule"] == c["best"]["rule"]
            col = HURDLE if best else WHITE
            tab.add(VGroup(label(v["asset"], font_size=17, color=col), label(rn[v["rule"]], font_size=15, color=col),
                           MathTex(rf"{v['ann_pct']:.1f}\%", font_size=22, color=col),
                           MathTex(f"{v['sharpe']:.2f}", font_size=22, color=col),
                           MathTex(rf"{v['maxdd_pct']:.1f}\%", font_size=22, color=col)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.9 - 0.56 * j, 0])
        foot = wrapped_label(r"research window: Binance's perpetual funding files begin in January 2020, so it is twelve "
                             r"months long; monthly returns, net of costs", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.35)
        rule_name = {"always": "always on", "pos7": "on while the week's funding is positive",
                     "hurdle7": "on while the week's funding exceeds five percent"}[c["best"]["rule"]]
        with self.voiceover(
            "Nine variants, on the research window. <bookmark mark='a'/> Bitcoin, ether, or both; always on, on while the "
            "past week's funding is positive, or on while it exceeds five percent a year. The window is short: Binance's "
            "public funding files begin in January twenty twenty, so research has only that year. "
            f"<bookmark mark='b'/> The best: {c['best']['asset']}, {rule_name}, at "
            f"{c['best']['ann_pct']:.0f} percent a year with a Sharpe ratio of {c['best']['sharpe']:.1f}. The filters "
            "barely matter, because in twenty twenty funding was almost always positive."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.15))
            vo.wait_until("b")
            best_row = [i for i, v in enumerate(c["variants"]) if v["asset"] == c["best"]["asset"]
                        and v["rule"] == c["best"]["rule"]][0]
            self.play(Indicate(tab[1 + best_row], color=HURDLE, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()

    def register(self, c):
        rows = [cmath(r"\text{registered}", r":", rf"\text{{{c['best']['asset']}, always on, 15 bp a switch, a third margin}}",
                      font_size=32, colors={r"\text{registered}": HURDLE}),
                cmath(r"\text{trials}", r"=", rf"{c['n_trials']}", font_size=40),
                cmath(r"\text{the counter}", r"=", rf"{c['trials']:,}".replace(",", "{,}"), font_size=40,
                      colors={r"\text{the counter}": HURDLE})]
        whys = [why(r"the code's hash and its parameters, recorded before the hold-out is opened (Part 1's envelope)"),
                why(r"every variant tried counts, including the eight that lost"),
                why(r"the series' running total of configurations tried, against which every hold-out result is read")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "So the House registers it. <bookmark mark='a'/> The ether book, always on, with its costs and margin, and "
            "the hash of its code. <bookmark mark='b'/> Nine trials. <bookmark mark='c'/> The series' counter of "
            f"configurations tried rises to {c['trials']:,}. Then the envelope is opened, once."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def opened(self, c):
        r, h = c["res"], c["hold"]
        rows = [cmath(r"\text{research, 2020}", r":", rf"{r['ann_pct']:.1f}\%\ \text{{a year, Sharpe}}\ {r['sharpe']:.2f}",
                      font_size=36),
                cmath(r"\text{hold-out, 2021--25}", r":", rf"{h['ann_pct']:.1f}\%\ \text{{a year, Sharpe}}\ {h['sharpe']:.2f}",
                      font_size=36, colors={r"\text{hold-out, 2021--25}": HURDLE}),
                cmath(r"\text{worst drawdown}", r":", rf"{h['maxdd_pct']:.1f}\%", font_size=38)]
        whys = [why(r"what was promised, on twelve months"),
                why(rf"what came, on {c['hold_months']} months never seen: less than half the return, still a high "
                    r"Sharpe ratio"),
                why(r"monthly, net of costs; this is the return the data can show")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            f"The envelope. <bookmark mark='a'/> Promised: {r['ann_pct']:.0f} percent a year, a Sharpe ratio of "
            f"{r['sharpe']:.1f}. <bookmark mark='b'/> Delivered, over five unseen years: {h['ann_pct']:.1f} percent a "
            f"year, Sharpe {h['sharpe']:.1f}. Less than half the return, and still one of the highest Sharpe ratios in "
            f"the Track Record. <bookmark mark='c'/> Its worst drawdown was {abs(h['maxdd_pct']):.1f} percent. On these "
            "numbers it looks like free money. Keep that thought."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def years(self, c):
        ys = c["years"]
        hx = [-3.0, 0.0, 3.0]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"year", r"return", r"Sharpe")])
        tab = VGroup(head)
        for y_ in sorted(ys):
            v = ys[y_]
            tab.add(VGroup(MathTex(y_, font_size=28), MathTex(rf"{v['ret_pct']:+.1f}\%", font_size=28,
                                                               color=GOOD if v["ret_pct"] > 2 else BAD),
                           MathTex(f"{v['sharpe']:.1f}", font_size=28)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.75 * j, 0])
        with self.voiceover(
            f"Year by year. <bookmark mark='a'/> Twenty twenty-one, the leverage boom: {ys['2021']['ret_pct']:.0f} "
            f"percent. <bookmark mark='b'/> Twenty twenty-two, Terra and FTX: {ys['2022']['ret_pct']:.1f} percent, as "
            f"ether's funding was negative at a third of its settlements. <bookmark mark='c'/> Then {ys['2023']['ret_pct']:.0f}, "
            f"{ys['2024']['ret_pct']:.0f} and {ys['2025']['ret_pct']:.0f} percent. The carry is paid by leveraged "
            "longs, so it is largest when they are most eager, and close to nothing when they are being liquidated."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[3:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def curve_(self, c):
        d = np.asarray(c["eq"]["day"], float) / 365.25 + 2021
        v = np.asarray(c["eq"]["v"], float)
        g = axes([2021, 2026], [0.95, float(v.max()) * 1.05], x_length=7.6, y_length=4.0, xlabel=r"the hold-out",
                 ylabel=r"growth of \$1 of capital", xticks=[2021, 2022, 2023, 2024, 2025, 2026],
                 yticks=[1.0, 1.2, 1.4, 1.6], font_size=16).move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, d, v, PERP_C, stroke_width=3)
        with self.voiceover(
            "The hold-out as a curve. <bookmark mark='a'/> A steep climb through twenty twenty-one, a flat year, and a "
            f"gentler slope after: a dollar became {v[-1]:.2f}. Almost no wobble along the way. A curve like this is "
            "exactly what should make a risk manager ask what it is not showing."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def decay(self, c):
        se = c["row"]["research"]["sharpe_se"]
        se_h = c["row"]["holdout"]["sharpe_se"]
        cards = VGroup(
            desk_question(r"the trade got crowded", r"from 2024 the basis trade was packaged at scale: Ethena's USDe, a "
                          r"dollar token backed by spot hedged with short perpetuals, grew to billions, as reported, and "
                          r"Part 31 met it as a near-riskless coin", width=12.4, font_size=19),
            desk_question(r"the rule capped the carry", r"in 2025 neither Bitcoin's nor ether's funding rose above the "
                          r"interest term even once, on this data", width=12.4, font_size=19),
            desk_question(r"research was one year", rf"twelve months of a boom is a thin basis for a promise: the "
                          rf"research Sharpe ratio's standard error is {se:.2f}, against {se_h:.2f} on the hold-out",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it decayed. <bookmark mark='a'/> The trade became crowded: from twenty twenty-four it was packaged at "
            "scale, as reported, in Ethena's dollar token, backed by spot hedged with short perpetuals, the near-riskless "
            "coin that Part thirty-one's search kept finding. <bookmark mark='b'/> In twenty twenty-five, neither "
            "Bitcoin's nor ether's funding rose above the interest term even once. <bookmark mark='c'/> And the promise "
            f"rested on one year of a boom: on twelve months, the Sharpe ratio's standard error is {se:.2f}, three times "
            "that of the five-year hold-out."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def hidden_tail(self, c):
        ms = c["margin_share"]
        h = c["hold"]
        yrs = ms * 100 / h["ann_pct"]
        rows = [cmath(r"\text{at the venue}", r":", r"\text{margin} = \tfrac{1/3}{4/3} = 25\%\ \text{of capital}", font_size=36,
                      colors={r"\text{at the venue}": BAD}),
                cmath(r"\text{spot at the venue too}", r":", r"100\%", font_size=38, colors={r"100\%": BAD}),
                cmath(r"25\% \text{ lost}", r"=", rf"{yrs:.1f}\ \text{{years of carry}}", font_size=40,
                      colors={rf"{yrs:.1f}\ \text{{years of carry}}": BAD})]
        whys = [why(r"even with the spot held elsewhere, the short's margin sits at the exchange"),
                why(r"most such books keep both legs on one exchange, to net margin; then a failure takes everything"),
                why(r"one FTX in the hold-out would have erased years of gains; the backtest's maximum drawdown is a "
                    r"statement about Binance having survived")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "What the returns do not show. <bookmark mark='a'/> Even with the spot held in custody elsewhere, the short's "
            "margin, a quarter of the capital, sits at the exchange. <bookmark mark='b'/> Most such books keep both legs "
            "on one exchange to net their margin, and then a failure takes everything. <bookmark mark='c'/> Losing just "
            f"the margin would erase about {yrs:.1f} years of the hold-out's carry. The backtest's drawdown of "
            f"{abs(h['maxdd_pct']):.1f} percent is really a statement that Binance survived. Traders who ran the same "
            "book on FTX lost their collateral."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def premium(self):
        cards = VGroup(
            desk_question(r"a premium, not an arbitrage", r"the House is paid for supplying leverage to the long side and "
                          r"for bearing venue and stablecoin risk: Part 22's carry, in a new market", width=12.4,
                          font_size=19),
            desk_question(r"it crashes with its market", r"it earned nothing in 2022, when crypto's balance sheets were "
                          r"failing: carry pays least exactly when the lenders are most at risk", width=12.4, font_size=19),
            desk_question(r"size it by the tail", r"the House sizes it so that losing a venue's collateral is survivable, "
                          r"not by its Sharpe ratio", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "So what is it? <bookmark mark='a'/> A premium, not an arbitrage: payment for supplying leverage to the long "
            "side, and for bearing venue and stablecoin risk, Part twenty-two's carry in a new market. "
            "<bookmark mark='b'/> It crashes with its market: it earned nothing in twenty twenty-two, when crypto's "
            "lenders were failing. <bookmark mark='c'/> So the House sizes it by its tail, the loss of a venue's "
            "collateral, and not by its Sharpe ratio."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"on 10 March 2023 the bank holding part of USD Coin's reserves failed. USDC fell to about 88 cents. "
                       r"Was that a run, and what did a holder who waited three days receive?")
        with self.voiceover(
            "Pause and predict. On the tenth of March twenty twenty-three, the bank holding part of USD coin's reserves "
            "failed, and the coin fell to about eighty-eight cents. Was that a run, and what did a holder who simply "
            "waited three days receive?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
