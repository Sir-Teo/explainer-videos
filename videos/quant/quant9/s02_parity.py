from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.zh_text import verbatim
from videos.quant.quant9.common import (ARB, CALL, FWD, PART, PUT, Q_C, answer_under, load, pause_at, real_data,
                                        side_why)


class Parity(VoiceoverScene):
    def construct(self):
        p, fb = load("parity"), load("futures_basis")
        self.card()
        self.definition()
        self.sticks()
        self.ledger()
        self.bounds()
        self.lab(p)
        self.futures(p, fb)
        self.predict()

    def card(self):
        c = chapter_card(1, r"Parity, assembled", r"Why must a call minus a put cost what a forward costs?",
                         lit=(1973,), part=PART)
        with self.voiceover("Chapter one. Parity, assembled."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def definition(self):
        d = definition_card(r"Arbitrage", r"a portfolio that costs nothing or less today, can never lose, and wins "
                            r"with positive probability: cost $\le 0$, payoff $\ge 0$ in every state, payoff $> 0$ "
                            r"in some state", color=ARB, width=6.4)
        lo = definition_card(r"The law of one price", r"two portfolios with the same payoff in every state have the "
                             r"same price; otherwise buy the cheap one, sell the dear one, and pocket the difference",
                             color=Q_C, width=6.0, kind=r"Corollary")
        VGroup(d, lo).arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to(UP * 0.3)
        with self.voiceover(
            "Start with a definition. An arbitrage is a portfolio that costs nothing or less today, can never lose, "
            "and wins with positive probability. Three conditions: cost at most zero, payoff never negative, payoff "
            "sometimes positive. <bookmark mark='a'/> The law of one price follows at once. If two portfolios pay the "
            "same in every state of the world but cost different amounts, buy the cheap one and sell the dear one: "
            "you collect the difference today and owe nothing later. Everything in this part is that sentence, "
            "pushed as far as it will go."
        ) as vo:
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(lo, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    def sticks(self):
        K = 100.0
        g = axes([50, 150], [-55, 55], x_length=6.4, y_length=4.6, xlabel=r"stock price at expiry, $S_T$",
                 ylabel=r"payoff", xticks=[50, 100, 150], yticks=[-50, 0, 50], font_size=17)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        xs = np.linspace(50, 150, 201)
        zero = DashedLine(ax.c2p(50, 0), ax.c2p(150, 0), color=GREY_D, stroke_width=1.5)
        call = curve(ax, xs, np.maximum(xs - K, 0), CALL, stroke_width=4)
        sput = curve(ax, xs, -np.maximum(K - xs, 0), PUT, stroke_width=4)
        fwd = curve(ax, xs, xs - K, FWD, stroke_width=5)
        leg = legend([(CALL, r"long call: $(S_T - K)^+$"), (PUT, r"short put: $-(K - S_T)^+$"),
                      (FWD, r"together: $S_T - K$, a forward")], font_size=19)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        rows = [cmath(r"(S_T - K)^+ - (K - S_T)^+", r"=", r"S_T - K", font_size=34),
                cmath(r"C - P", r"=", r"S - K e^{-rT}", font_size=38, colors={r"C - P": CALL}),
                cmath(r"\tilde C - \tilde P", r"=", r"1 - \frac{K}{F}", font_size=38, colors={r"\tilde C - \tilde P": Q_C})]
        whys = [side_why(r"split at $K$: above it the call pays and the put is worthless; below, the reverse", 5.6),
                side_why(r"the right side is bought today with one share and a loan of $K e^{-rT}$; by the law of one "
                         r"price the two sides cost the same (Stoll 1969)", 5.6),
                side_why(r"Deribit's options are paid in bitcoin: divide every dollar price by the forward $F$, the "
                         r"price of the unit (chapter 11)", 5.6)]
        step = ladder(self, rows, whys, keep=3, top=3.3, x=3.6, buff=0.5, edge=6.9)
        with self.voiceover(
            "Now build parity instead of quoting it. On the left, payoffs at expiry against the stock price. A long "
            "call is a hockey stick bending up at the strike. <bookmark mark='a'/> A short put is a hockey stick "
            "bending down. <bookmark mark='b'/> Add them. Above the strike the call pays and the put is worthless; "
            "below it, the reverse. The kinks cancel, and what is left is a straight line: the stock minus the "
            "strike, the payoff of a forward contract, in every state of the world. <bookmark mark='c'/> The "
            "straight line can be bought today another way: one share, financed by borrowing the present value of "
            "the strike. Same payoff, so the same price: call minus put equals the stock minus the discounted "
            "strike. Hans Stoll wrote this down in 1969. <bookmark mark='d'/> On Deribit, where options are priced "
            "in bitcoin, divide every dollar price by the forward, and parity reads one minus K over F."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(leg[0]), Create(call))
            vo.wait_until("a")
            self.play(FadeIn(leg[1]), Create(sput))
            vo.wait_until("b")
            self.play(Transform(call.copy(), fwd), Transform(sput.copy(), fwd), FadeIn(leg[2]), run_time=2)
            self.add(fwd)
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    def ledger(self):
        K, S0 = 100.0, 103.0
        g = axes([60, 140], [-45, 45], x_length=6.6, y_length=4.4, xlabel=r"stock price at expiry, $S_T$",
                 ylabel=r"payoff of the package", xticks=[60, 100, 140], yticks=[-40, 0, 40], font_size=17)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.25)
        ax = g.ax
        xs = np.linspace(60, 140, 161)
        legs = [(r"sell the call at 10", -np.maximum(xs - K, 0), +10.0, CALL),
                (r"buy the put at 6", np.maximum(K - xs, 0), -6.0, PUT),
                (r"buy the stock at 103", xs, -103.0, FWD),
                (r"borrow 99, repay 99", -99.0 + 0 * xs, +99.0, GREY_B)]
        total = np.zeros_like(xs)
        sums, rows = [], VGroup()
        for name, pay, cash, col in legs:
            total = total + pay
            sums.append(total.copy())
            rows.add(VGroup(label(name, font_size=21, color=col),
                            MathTex(rf"{cash:+.0f}", font_size=26, color=col)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        head = label(r"the put at 6: cash today", font_size=22, color=GREY_A)
        tot = VGroup(label(r"net cost today", font_size=21), MathTex(r"0", font_size=28)).arrange(RIGHT, buff=0.3)
        side = VGroup(head, rows, Line(LEFT, RIGHT * 3.2, color=GREY_C), tot).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.22)
        side.to_edge(RIGHT, buff=0.7).shift(UP * 0.6)
        cur = curve(ax, xs, np.clip(sums[0], -45, 45), legs[0][3], stroke_width=4)
        g_ = np.random.default_rng(1)
        ST = np.clip(S0 * np.exp(0.3 * g_.standard_normal(200) - 0.045), 61, 139)
        dots = VGroup(*[Dot(ax.c2p(s, 30 + 12 * g_.random()), radius=0.035, color=WHITE).set_opacity(0.8) for s in ST])
        landed = VGroup(*[Dot(ax.c2p(s, 1), radius=0.035, color=Q_C) for s in ST])
        res = wrapped_label(r"200 possible prices at expiry: every one lands on $+1$. No state of the world is left "
                            r"in the payoff", 5.0, 21, Q_C).next_to(side, DOWN, buff=0.35).align_to(side, LEFT)
        with self.voiceover(
            "Now misprice the put at six and watch the arbitrage lock in. The call minus the put is now four, more "
            "than the forward's three. Sell what is dear and buy what is cheap. <bookmark mark='a'/> Sell the call: "
            "ten dollars in, and a payoff that falls away above the strike. <bookmark mark='b'/> Buy the put for six: "
            "now the package pays minus the stock plus the strike, a downward line. <bookmark mark='c'/> Buy the "
            "stock for a hundred and three, and the slope cancels: the line goes flat. <bookmark mark='d'/> Borrow "
            "the ninety-nine dollars you are short, and the package costs nothing today. At expiry it pays one "
            "dollar. <bookmark mark='e'/> Draw two hundred possible stock prices at expiry. Every one of them lands "
            "on the same flat line at plus one. That flattening is the idea of the whole part: a hedged position "
            "has no state of the world left in it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(head))
            vo.wait_until("a")
            self.play(Create(cur), FadeIn(rows[0]))
            for i, mk in ((1, "b"), (2, "c"), (3, "d")):
                vo.wait_until(mk)
                self.play(Transform(cur, curve(ax, xs, np.clip(sums[i], -45, 45), legs[i][3] if i < 3 else Q_C,
                                               stroke_width=4)), FadeIn(rows[i]), run_time=1.3)
            self.play(FadeIn(side[2]), FadeIn(tot))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.01, run_time=1.2))
            self.play(Transform(dots, landed), FadeIn(res), run_time=1.8)
        self.wait(0.3)
        self.clear_scene()

    def bounds(self):
        K = 100.0
        g = axes([40, 160], [0, 165], x_length=6.4, y_length=4.4, xlabel=r"stock price today, $S$",
                 ylabel=r"call price", xticks=[50, 100, 150], yticks=[0, 50, 100, 150], font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        xs = np.linspace(40, 160, 241)
        lo = np.maximum(xs - K * np.exp(-0.04), 0)
        region = band(ax, xs, lo, xs, Q_C, 0.18)
        lo_c = curve(ax, xs, lo, Q_C, stroke_width=3)
        hi_c = curve(ax, xs, xs, Q_C, stroke_width=3)
        from explainer.quant.house import bs
        cc = curve(ax, xs, bs.price(xs, K, 1.0, 0.3, 0.04), CALL, stroke_width=4)
        side = VGroup(
            MathTex(r"\max(S - K e^{-rT},\, 0) \le C \le S", font_size=34, color=Q_C),
            wrapped_label(r"below: a call is worth at least the forward it can be turned into, and never less than "
                          r"nothing; above: it can never be worth more than the share it may buy", 5.2, 20, GREY_A),
            wrapped_label(r"green: one model's call (Black--Scholes, 30\% volatility, 4\% rates); any model must keep "
                          r"its curve inside the band", 5.2, 20, CALL),
            wrapped_label(r"Bj\"ork, ch.\ 10; Hull, ch.\ 11", 5.2, 18, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Parity is one of a family of model-free facts. A call is worth at least what you could lock in by "
            "converting it into a forward, and never less than nothing. And it can never be worth more than the "
            "share it gives you the right to buy. <bookmark mark='a'/> That gives a band, drawn in purple, with no "
            "model at all. Any model's call price, like this Black-Scholes curve, must live inside it, or there is an "
            "arbitrage against that model. Björk's chapter ten collects these parity relations."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[1]))
            self.play(FadeIn(region), Create(lo_c), Create(hi_c))
            vo.wait_until("a")
            self.play(Create(cc), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def lab(self, p):
        with verbatim():
            card = lab_card(r"the forward from every call--put pair", [
                "def implied_forward(trades, window=600, max_logm=0.2):",
                "    by = group(trades, key=(expiry, strike, call_or_put))",
                "    for (e, K, cp), calls in by.items():",
                "        if cp != 1 or (e, K, -1) not in by: continue",
                "        for s, c, index in calls:",
                "            p = nearest_put(by[(e, K, -1)], s)",
                "            if abs(p.time - s) > window: continue",
                "            if abs(log(K / index)) > max_logm: continue",
                "            F = K / (1 - (c - p.price))   # C - P = 1 - K/F",
                "            rows.append((T, F / index, e))",
            ], source="explainer/quant/house/arbitrage.py", width=8.4).to_edge(UP, buff=0.35)
        ex = p["expiries"]
        outs = [f"pairs = implied_forward(deribit_trades('{p['day']}'))",
                f"len(pairs) = {p['n_pairs']}    expiries = {len(ex)}",
                f"median |residual| = {p['trade_p50']:.1f} bp (trades), {p['mark_p50']:.1f} bp (marks)"]
        with self.voiceover(
            "Here is the House's code that reads the forward out of real trades. Group the day's option trades by "
            "expiry, strike and type. For every call, find the put at the same strike traded closest in time, "
            "and keep the pair if they are within ten minutes and near the money. <bookmark mark='a'/> Each pair "
            "gives the forward by parity: the strike, divided by one minus the call-minus-put price. Run it on the "
            f"Surface's morning of trades. <bookmark mark='b'/> {p['n_pairs']} pairs, across {len(ex)} expiries, "
            f"and half of them sit within {p['trade_p50']:.1f} basis points of their expiry's median forward."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(card.code[8], color=Q_C, scale_factor=1.04))
            vo.wait_until("b")
            with verbatim():
                lab_run(self, card, outs, run_time=2.4)
        self.wait(2.5)
        self.clear_scene()

    def futures(self, p, fb):
        rows = [r for r in fb["rows"] if "gap_bp" in r]
        g = axes([0, 220], [0.02, 0.055], x_length=6.4, y_length=4.2, xlabel=r"days to expiry",
                 ylabel=r"forward over index, as an annual rate", xticks=[0, 100, 200],
                 yticks=[0.02, 0.03, 0.04, 0.05], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        od = VGroup(*[Dot(ax.c2p(e["T"] * 365, e["rate"]), radius=0.08, color=FWD) for e in p["expiries"]
                      if e["T"] * 365 > 2])
        fd = VGroup(*[Square(0.16, color=QC.IMPLIED, stroke_width=3).move_to(ax.c2p(r["T"] * 365, r["rate"]))
                      for r in fb["rows"] if r["T"] * 365 > 2])
        leg = legend([(FWD, r"from option parity (dots)"), (QC.IMPLIED, r"dated futures, traded (squares)")],
                     font_size=19).next_to(g, UP, buff=0.05).align_to(g, LEFT)
        gp50, gmax = fb["gap_p50"], fb["gap_max"]
        verdict = (r"the two forwards agree to within the width of a quote: this is the cash-and-carry check"
                   if gmax < 10 else r"the two forwards disagree by more than a quote is wide: a basis trade")
        side = VGroup(
            label(rf"{fb['n_trades']:,} futures trades, same hours".replace(",", "{,}"), font_size=22, color=QC.IMPLIED),
            wrapped_label(rf"{fb['n_matched']} expiries have both: median gap {gp50:.1f} bp of price, largest "
                          rf"{gmax:.1f} bp", 4.6, 21, WHITE),
            wrapped_label(verdict, 4.6, 20, Q_C),
            wrapped_label(r"a future is a forward settled daily; a forward above the index is crypto's own interest "
                          r"rate, paid by leveraged buyers (Part 2's funding rate)", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.45)
        src = real_data(r"Deribit BTC options and futures trades, 10 December 2025, 00:00--12:00 UTC")
        tail = ("The two markets agree to within the width of a quote. If they did not, buying the cheap forward and "
                "selling the dear one would be the cash-and-carry arbitrage, and traders do exactly that."
                if gmax < 10 else "That is wider than a quote: the basis between the two markets is itself a trade.")
        with self.voiceover(
            "Is that forward real? Deribit also lists futures on the same expiries, and a future is, up to daily "
            "settlement, a forward you can trade directly. The House fetched every futures trade from the same "
            f"hours, {fb['n_trades']:,} of them, most in the perpetual contract. <bookmark mark='a'/> The dots are "
            "the forwards that option parity implies, as annual rates over the index; the squares are where the "
            f"dated futures actually traded. On the {fb['n_matched']} expiries that have both, the median gap is "
            f"{gp50:.1f} basis points of price, and the largest {gmax:.1f}. <bookmark mark='b'/> " + tail
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in od], lag_ratio=0.15), run_time=1.6)
            self.play(LaggedStart(*[GrowFromCenter(d) for d in fd], lag_ratio=0.15), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"If the put had been 8 instead of 6, which of the four legs flip?")
        with self.voiceover(
            "Pause and predict. If the put had been eight instead of six, which of the four legs flip? "
            "<bookmark mark='a'/> All four. Now the call minus the put is two, less than the forward's three, so "
            "buy the call, sell the put, short the stock and lend a hundred: one dollar in hand today, and nothing "
            "owed at expiry."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"all four: buy the call, sell the put, short the stock, lend "
                                                r"100; $+1$ today, and the package nets to zero at expiry")))
        self.wait(0.4)
        self.clear_scene()
