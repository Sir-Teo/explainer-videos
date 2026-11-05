from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import making as M
from videos.quant.quant38.common import (ETF_C, FAST_C, GOOD, HURDLE, INV_C, MAKER_C, PART, SNIPE_C, SPREAD_C,
                                         house_lab, load)


class House(VoiceoverScene):
    def construct(self):
        self.answer()
        self.card()
        self.sheet(load("maker"), load("fills"), load("glft"), load("deep"), load("bcs"), load("etf"))
        self.limits()
        self.golive()
        self.capital()
        self.lab()
        self.lab2()
        self.lab3()
        self.lab4()
        self.two_desks()
        self.module()
        self.test()

    def answer(self):
        rows = [cmath(r"\text{1. its markout}", r"<", r"\tfrac{s}{2} + \text{rebate}", font_size=36,
                      colors={r"\text{1. its markout}": SNIPE_C}),
                cmath(r"\text{2. speed}", r":", r"\text{measured against its rivals}", font_size=36,
                      colors={r"\text{2. speed}": FAST_C}),
                cmath(r"\text{3. limits}", r":", r"\text{inventory, loss and a kill switch}", font_size=36,
                      colors={r"\text{3. limits}": INV_C})]
        whys = [why(r"a measured edge: the expected markout at the House's own speed and queue position must be smaller "
                    r"than what each fill earns; Chapter 2 showed a naive quote fails this by ten ticks"),
                why(r"its latency rank: Chapter 6 says the prize goes to the fastest, so the desk must know where it stands"),
                why(r"hard limits on position and loss, and a switch that stops all quoting at once: Knight Capital's "
                    r"lesson")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The answer to the pause. <bookmark mark='a'/> First, a measured edge: the expected markout at the House's "
            "own speed and queue position must be smaller than half the spread plus the rebate. Chapter two's naive "
            "quote failed by ten ticks. <bookmark mark='b'/> Second, its speed, measured against rivals, because the "
            "prize goes to the fastest. <bookmark mark='c'/> Third, hard limits on inventory and loss, and a switch that "
            "stops all quoting at once."
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

    def card(self):
        c = chapter_card(8, r"Rule 38: quote only what you can measure", r"What must a quoting desk show before it posts?",
                         part=PART)
        with self.voiceover("Chapter eight. The House's thirty-eighth rule belongs to the market-making desk it opens. "
                            "Quoting is the only business in the House that can lose a year's profit in an hour, so the "
                            "rule is strict."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, mk, f, g, dp, b, e):
        d = mk["days"]["2023-05-17"]
        r45 = [r for r in dp["rows"] if r["delta"] == 45][0]
        rows = [(r"maker at the touch, 17 May: P\&L per fill, slow and fast", rf"{d['slow']['pnl_per_fill']:+.1f},\ "
                 rf"{d['fast']['pnl_per_fill']:+.1f}", SNIPE_C),
                (r"fast and filtered by the queue imbalance", rf"{d['fast, filtered']['pnl_per_fill']:+.1f}", GOOD),
                (r"fill intensity: $A$ per second, $k$ per tick", rf"{f['A']:.2f},\ {f['k']:.3f}", SPREAD_C),
                (r"GLFT half-spread, small risk aversion, ticks", rf"{g['rows'][0]['half_spread']:.0f}", MAKER_C),
                (r"quotes 45 ticks out: P\&L per fill after a minute", rf"{r45['pnl60']:+.0f}", MAKER_C),
                (r"sniping half-spread on Bitcoin, model, ticks", rf"{b['btc']['half']:.2f}", HURDLE),
                (r"HYG, January high to 23 March 2020", rf"{100 * e['HYG']['drawdown']:.0f}\%", ETF_C)]
        hx = [-2.2, 4.8]
        tab = VGroup()
        for j, (txt, val, col) in enumerate(rows):
            y = 2.4 - 0.62 * j
            tab.add(VGroup(label(txt, font_size=16, color=col).move_to([hx[0], y, 0]),
                           MathTex(val, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The market-making desk's first sheet", font_size=28).to_edge(UP, buff=0.25)
        foot = wrapped_label(r"computed in this part from Binance's public best quotes and trades for the BTCUSDT perpetual "
                             r"(16, 17 and 20 May 2023), Yahoo Finance's daily bars, and simulation; ticks of \$0.10; none "
                             r"is advice", 12.0, 15, GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> A quote at the touch that loses, slow or fast, and loses less when it "
            "listens to the queues. Fill rates that decay slowly with distance, and optimal quotes far from the mid "
            "that earn, before queues and fees. A sniping spread under a tick. And a bond fund that fell more than a "
            "fifth in two months."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def limits(self):
        cards = VGroup(
            desk_question(r"position limits", r"per instrument and in total, with the hedge that brings each back; the "
                          r"replay's five units, scaled to capital", width=12.0, font_size=19),
            desk_question(r"loss limits and a kill switch", r"quoting stops automatically at a loss threshold or when "
                          r"messages, fills or inventory move faster than expected", width=12.0, font_size=19),
            desk_question(r"pre-trade checks", r"every order passes price collars and size limits before it leaves the "
                          r"building; in the US, the Market Access Rule requires it of broker-dealers", width=12.0,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Controls, before any edge. <bookmark mark='a'/> Position limits per instrument and in total, each with its "
            "hedge. <bookmark mark='b'/> Loss limits, and a switch that stops quoting automatically when losses, "
            "messages or fills move faster than expected. <bookmark mark='c'/> And pre-trade checks on every order, price "
            "collars and size limits, which in the United States the Market Access Rule requires of broker-dealers."
        ) as vo:
            for k_, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def golive(self):
        cards = VGroup(
            desk_question(r"replay first", r"a replay on the real tape, with fills at the House's own measured latency "
                          r"and queue position, and markouts at 1, 10 and 60 seconds", width=12.0, font_size=19),
            desk_question(r"then small and live", r"a minimal size with tight limits, measuring live markouts against "
                          r"the replay's; the gap between them is the replay's error", width=12.0, font_size=19),
            desk_question(r"then scale, slowly", r"size grows only while live markouts stay inside the replay's "
                          r"confidence band; any drift stops it", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How the desk would go live. <bookmark mark='a'/> A replay first, on the real tape, with fills at the "
            "House's own measured latency and queue position. <bookmark mark='b'/> Then small and live, with tight "
            "limits, measuring live markouts against the replay's: the gap is the replay's error. <bookmark mark='c'/> "
            "Then scale, slowly, and only while live markouts stay within the replay's confidence band."
        ) as vo:
            for k_, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def capital(self):
        cards = VGroup(
            desk_question(r"margin and collateral", r"every position needs margin at the venue or the clearing house; a "
                          r"maker quoting many venues posts collateral at each (Part 21)", width=12.0, font_size=19),
            desk_question(r"the worst minute, not the average day", r"capital is set by losses in a fast market, when "
                          r"fills arrive in bursts on one side and hedges slip", width=12.0, font_size=19),
            desk_question(r"capacity", r"a quoting desk's size is capped by its markout, its limits and its capital; the "
                          r"House would start small and grow only on live evidence", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And capital. <bookmark mark='a'/> Every position needs margin at the venue or the clearing house, and a maker "
            "on many venues posts collateral at each. <bookmark mark='b'/> Capital is set by the worst minute, not the "
            "average day: fills in bursts on one side, and hedges that slip. <bookmark mark='c'/> So the desk's size is "
            "capped by its markout, its limits and its capital."
        ) as vo:
            for k_, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Fill rates from the tape", M.fill_intensity, "up = np.full(nw, -np.inf)", 9, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter three's measurement. For each second, the furthest any buy reached above the starting mid, and any "
            "sell below it, in ticks; then, for each distance, the share of seconds that reached it."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"Guéant--Lehalle--Fernandez-Tapia quotes", M.glft, "xi = gamma if xi is None else xi", 4,
                         width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter one's closed form, in four lines: the skew constant from volatility, risk aversion and the fill "
            "parameters, and the half-spread as the base term plus half the skew."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab3(self):
        card = house_lab(r"The maker's fills", M.maker_replay, "if fast and through_b:", 14, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter two's replay at its core. A fast maker escapes any sweep through its price; otherwise a trade "
            "through the price, or trades at the price exceeding the queue ahead, fill it, and the inventory moves."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab4(self):
        card = house_lab(r"The sniping spread", M.bcs_spread, "return lam_jump * J", 1,
                         extra=((M.bcs_simulate, "if batch is None and J > half:", 4),), width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And Chapter six. The equilibrium half-spread in one line; and the simulation's race, in which the provider "
            "is sniped unless its cancel comes first, one time in N, and never in a batch auction."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def two_desks(self):
        cards = VGroup(
            desk_question(r"internal crossing", r"when the portfolio desk's order could trade against the market-making "
                          r"desk's inventory, crossing it inside the House saves both the spread", width=12.0, font_size=19),
            desk_question(r"the conflict", r"the maker sees the executor's flow; a maker that trades ahead of it would be "
                          r"front-running its own client, the abuse rules forbid", width=12.0, font_size=19),
            desk_question(r"the barrier", r"the two desks are separated; crossing happens only at a price fixed by the "
                          r"public market, and compliance (Part 34) reviews every case", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Two desks under one roof. <bookmark mark='a'/> When the portfolio desk's order could trade against the "
            "market-making desk's inventory, crossing it inside the House saves both sides the spread. "
            "<bookmark mark='b'/> But the maker would see the executor's flow, and trading ahead of it would be "
            "front-running its own client. <bookmark mark='c'/> So the desks are separated, crossing happens only at a "
            "price fixed by the public market, and compliance reviews every case."
        ) as vo:
            for k_, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("mm",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{fill\_intensity}, \texttt{glft}", r"fill rates and quotes"),
            (r"\texttt{maker\_replay}", r"a maker on the tape"),
            (r"\texttt{bcs\_spread}, \texttt{bcs\_simulate}", r"the speed race"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 38: the House quotes only where its measured markout, at its own speed and queue "
                             r"position, is below the spread plus rebate it earns; every quoting engine runs under position "
                             r"and loss limits with a kill switch; and fund arbitrage is sized to the balance sheet it "
                             r"would need in a stress like March 2020.", 12.4, 17, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds. <bookmark mark='a'/> Fill rates and quotes; a maker on the tape; and the speed "
            "race. <bookmark mark='b'/> And the thirty-eighth rule. The House quotes only where its measured markout, at "
            "its own speed and queue position, is below the spread and rebate it earns. Every quoting engine runs under "
            "position and loss limits with a kill switch. And any fund arbitrage is sized to the balance sheet it would "
            "need in a stress like March twenty twenty."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the backtest of a quoting strategy", r"ask how fills were simulated: at the back of the "
                          r"queue or the front, and whether sweeps through the price were counted (Chapter 2)", width=12.0,
                          font_size=19),
            desk_question(r"the vendor's optimal-quote model", r"ask for its markouts, not its fill rates: a model that "
                          r"assumes fills independent of moves can be right about distance for the wrong reason "
                          r"(Chapter 3)", width=12.0, font_size=19),
            desk_question(r"the ETF arbitrage that always works", r"ask what it does when the underlying cannot be sold at "
                          r"NAV, and whose balance sheet holds the basket (Chapter 5)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The rule against three cases. <bookmark mark='a'/> A backtest of a quoting strategy: ask how fills were "
            "simulated, at the back of the queue or the front, and whether sweeps were counted. <bookmark mark='b'/> A "
            "vendor's optimal-quote model: ask for its markouts, not its fill rates. <bookmark mark='c'/> An ETF "
            "arbitrage that always works: ask what happens when the bonds cannot be sold at their published value, and "
            "whose balance sheet holds them."
        ) as vo:
            for k_, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
