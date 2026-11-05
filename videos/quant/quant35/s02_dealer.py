from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant35.common import (ASK_C, BAD, BID_C, DEALER_C, FLOW_C, GOOD, HURDLE, PART, PRICE_C, comma, fit_right,
                                         illustration, load)


class Dealer(VoiceoverScene):
    def construct(self):
        d = load("dealer")
        self.card()
        self.garman()
        self.inventory()
        self.paths(d)
        self.optimal()
        self.numbers(d)
        self.today()
        self.three()
        self.question()

    def card(self):
        c = chapter_card(1, r"The dealer's problem", r"Why does a market maker quote two prices, and move them?", part=PART)
        with self.voiceover("Chapter one. Every trade has two sides, and on most markets one side is a dealer: someone "
                            "who quotes a price to buy and a price to sell, all day, to anyone. In 1976 Mark Garman gave "
                            "the field its name, market microstructure, by asking what that dealer must do to survive."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def garman(self):
        rows = [cmath(r"\text{buyers}", r"\sim", r"\text{Poisson}(\lambda_b(\text{ask}))", font_size=34,
                      colors={r"\text{buyers}": ASK_C}),
                cmath(r"\text{sellers}", r"\sim", r"\text{Poisson}(\lambda_s(\text{bid}))", font_size=34,
                      colors={r"\text{sellers}": BID_C}),
                cmath(r"\text{inventory}", r"=", r"\text{sellers} - \text{buyers}:\ \text{a random walk}", font_size=32,
                      colors={r"\text{inventory}": DEALER_C})]
        whys = [why(r"Garman (1976): buy orders arrive at a rate that falls as the ask rises"),
                why(r"sell orders at a rate that falls as the bid falls"),
                why(r"with equal rates, the dealer's inventory wanders like a random walk and eventually ruins it; the "
                    r"quotes must manage the inventory")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Garman's model. <bookmark mark='a'/> Buy orders arrive at random, less often the higher the ask. "
            "<bookmark mark='b'/> Sell orders arrive less often the lower the bid. <bookmark mark='c'/> Even if the two "
            "rates balance on average, the dealer's inventory, sellers minus buyers, is a random walk: it wanders "
            "without limit, and a dealer with a fixed capital is eventually ruined. The quotes must do more than earn a "
            "spread. They must steer the inventory."
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

    def inventory(self):
        rows = [cmath(r"\text{mid}_t", r"=", r"v_t - \gamma\, q_t", font_size=38, colors={r"\gamma\, q_t": DEALER_C}),
                cmath(r"\text{ask}, \text{bid}", r"=", r"\text{mid}_t \pm s/2", font_size=36),
                cmath(r"q_t > 0", r"\Rightarrow", r"\text{both quotes fall: sell more, buy less}", font_size=32)]
        whys = [why(r"Ho and Stoll (1981): a risk-averse dealer shades both quotes against its inventory $q$"),
                why(r"the spread pays for the service; the shading manages the risk"),
                why(r"long inventory makes the dealer's offer more attractive and its bid less, so trades push the "
                    r"inventory back toward zero")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Thomas Ho and Hans Stoll's answer. <bookmark mark='a'/> Shade both quotes against the inventory: the "
            "middle of the quotes is the fair value minus a constant times what the dealer holds. "
            "<bookmark mark='b'/> The spread around it pays for the service. <bookmark mark='c'/> A dealer who is long "
            "lowers both quotes: its offer becomes more attractive and its bid less, so the next trades sell inventory "
            "back down. Avellaneda and Stoikov's model of Part eleven is the same idea, optimised."
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

    def paths(self, d):
        a = np.asarray(d["0.0"]["path"], float)
        b = np.asarray(d["0.05"]["path"], float)
        x = np.arange(len(a)) * 20
        lim = float(np.ceil(max(np.abs(a).max(), 10) / 50) * 50)
        g = axes([0, x[-1]], [-lim, lim], x_length=7.6, y_length=4.4, xlabel=r"trades offered", ylabel=r"inventory, units",
                 xticks=[0, 10000, 20000], yticks=[-lim, 0, lim], xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"),
                 yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, x, a, BAD, stroke_width=2.5)
        c2 = curve(ax, x, b, DEALER_C, stroke_width=3)
        leg = legend([(BAD, r"no shading: $\gamma = 0$"), (DEALER_C, r"Ho--Stoll shading: $\gamma = 0.05$")],
                     font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        ill = illustration(r"simulated: fair value a random walk; one unit per trade")
        with self.voiceover(
            "Simulated, twenty thousand arrivals. <bookmark mark='a'/> Without shading, the inventory wanders off into "
            "the hundreds of units. <bookmark mark='b'/> With shading, it stays within a few units of zero, because "
            "every trade that adds to it makes the next one less likely."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(c1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c2), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def optimal(self):
        rows = [cmath(r"r_t", r"=", r"v_t - q_t\,\gamma\sigma^2 (T - t)", font_size=36, colors={r"r_t": DEALER_C}),
                cmath(r"\delta^a + \delta^b", r"=", r"\gamma\sigma^2 (T - t) + \tfrac{2}{\gamma}\ln\big(1 + \tfrac{\gamma}{k}\big)",
                      font_size=32),
                cmath(r"\text{more risk}", r"\Rightarrow", r"\text{more shading, wider quotes}", font_size=32,
                      colors={r"\text{more risk}": BAD})]
        whys = [why(r"Avellaneda and Stoikov (2008), Part 11: the dealer's reservation price falls with its inventory, by "
                    r"risk aversion $\gamma$ times the variance it must still carry"),
                why(r"the optimal total spread: an inventory term, and a term set by how fast order arrival falls with "
                    r"distance, $k$"),
                why(r"Ho and Stoll's two effects made exact: volatility and time left raise both the shading and the spread")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Part eleven made this optimal. <bookmark mark='a'/> In Marco Avellaneda and Sasha Stoikov's model the "
            "dealer's reservation price is the value minus its inventory times risk aversion times the variance it still "
            "has to carry. <bookmark mark='b'/> The best total spread has two parts: inventory risk, and a part set by "
            "how fast customers stop trading as the quote moves away. <bookmark mark='c'/> More volatility, more time "
            "left, or more risk aversion: more shading and wider quotes. Ho and Stoll's two effects, made exact."
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

    def numbers(self, d):
        a, b = d["0.0"], d["0.05"]
        hx = [-3.6, -0.6, 2.4, 5.0]
        head = VGroup(label(r"20 runs", font_size=17, color=GREY_B), label(r"inventory sd", font_size=17, color=GREY_B),
                      label(r"mean P\&L", font_size=17, color=GOOD), label(r"P\&L sd", font_size=17, color=BAD))
        tab = VGroup(head,
                     VGroup(label(r"no shading", font_size=20, color=BAD), MathTex(f"{a['inv_sd']:.0f}", font_size=26),
                            MathTex(comma(a["pnl_mean"]), font_size=26), MathTex(comma(a["pnl_sd"]), font_size=26)),
                     VGroup(label(r"shading", font_size=20, color=DEALER_C), MathTex(f"{b['inv_sd']:.1f}", font_size=26),
                            MathTex(comma(b["pnl_mean"]), font_size=26), MathTex(comma(b["pnl_sd"]), font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.4 - 0.9 * j, 0])
        ra, rb = a["pnl_mean"] / a["pnl_sd"], b["pnl_mean"] / b["pnl_sd"]
        foot = wrapped_label(r"P\&L in units of the fair value's daily move, at the end of 20{,}000 arrivals", 11.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The trade-off, measured. <bookmark mark='a'/> Shading gives up some spread, because the dealer sometimes "
            "quotes against its own interest to unload: the mean profit falls. <bookmark mark='b'/> But the risk falls "
            f"far more: the profit's mean over its spread across runs goes from {ra:.1f} to {rb:.0f}. A dealer is paid "
            "for the spread and survives by the shading."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(VGroup(tab[2][0], tab[2][1], tab[2][2])))
            vo.wait_until("b")
            self.play(FadeIn(tab[2][3]))
        self.wait(0.4)
        self.clear_scene()

    def today(self):
        cards = VGroup(
            desk_question(r"specialists, then designated market makers", r"the NYSE once gave each stock one specialist "
                          r"with a duty to keep an orderly market; today designated market makers have obligations to quote "
                          r"and privileges at the auctions", width=12.4, font_size=19),
            desk_question(r"dealers in bonds and currencies", r"most bonds and currencies still trade with dealers, by "
                          r"request for quote; the dealer's balance sheet is the market's inventory (Part 18)", width=12.4,
                          font_size=19),
            desk_question(r"electronic market makers", r"everywhere else, algorithms quoting thousands of instruments, "
                          r"with inventory limits in place of a specialist's capital", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Who the dealers are today. <bookmark mark='a'/> The New York Stock Exchange once gave each stock one "
            "specialist, with a duty to keep an orderly market; today designated market makers have quoting obligations "
            "and privileges at the auctions. <bookmark mark='b'/> Most bonds and currencies still trade with dealers, by "
            "request for a quote, and the dealers' balance sheets are the market's inventory. <bookmark mark='c'/> "
            "Everywhere else, algorithms quote thousands of instruments, with inventory limits in place of a specialist's "
            "capital: Chapter nine's subject."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def three(self):
        cards = VGroup(
            desk_question(r"order processing", r"the cost of being there: systems, fees, capital; it is the whole spread in "
                          r"a market with no information", width=12.4, font_size=19),
            desk_question(r"inventory", r"the risk of holding what customers sold: Ho and Stoll's shading, paid for by a "
                          r"spread that widens with volatility and position size", width=12.4, font_size=19),
            desk_question(r"adverse selection", r"some customers know more than the dealer: the next two chapters, and the "
                          r"component that does not vanish with competition", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "So a spread has three parts. <bookmark mark='a'/> Order processing: the cost of being there at all. "
            "<bookmark mark='b'/> Inventory: the risk of holding what customers sold, paid for by a spread that widens "
            "with volatility and with the position. <bookmark mark='c'/> And adverse selection: some customers know "
            "more than the dealer. That part survives even among competitive, risk-neutral dealers, and it is the "
            "subject of the next two chapters."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a dealer holding 40 units shades its mid by 0.05 per unit. Where are its quotes, relative to fair "
                       r"value, with a spread of 1?")
        with self.voiceover(
            "Pause and predict. A dealer holding forty units shades its mid by five hundredths per unit. Where are its "
            "quotes, relative to fair value, with a spread of one?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
