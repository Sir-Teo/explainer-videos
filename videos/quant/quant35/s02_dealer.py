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
        self.add(c)
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
                why('equal rates give diffusing inventory; with imposed inventory bounds it eventually exits them. Financial ruin also requires a specified wealth and capital model')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Garman's model. <bookmark mark='a'/> Buy arrivals become less frequent as the ask rises. <bookmark mark='b'/> Sell arrivals become less frequent as the bid falls. <bookmark mark='c'/> With balanced independent arrivals, inventory behaves like a random walk. It eventually exits fixed inventory limits under the usual nondegeneracy conditions. That is not by itself a proof of financial ruin: wealth also depends on spread income, prices and capital. Inventory control addresses a real risk without that stronger claim."
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
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Ho and Stoll explain why inventory changes quotes. <bookmark mark='a'/> Our illustration specifies a linear heuristic: shift the mid below fair value by a constant times long inventory. It is not the solution of an optimal-control problem. <bookmark mark='b'/> Keep a fixed spread around that mid. Arrival probabilities fall exponentially with nonnegative quote distance and are capped at one. <bookmark mark='c'/> Lowering both quotes encourages selling inventory and discourages buying more. Part eleven solves a related utility model under its own assumptions."
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
        self.add(g, c1, leg, ill)
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
        self.add(rows[0], whys[0])
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
        foot = wrapped_label('Terminal cash plus inventory marked to fair value, after 20{,}000 arrivals; model currency units, twenty seeds', 11.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        self.add(tab[0], tab[1], foot)
        with self.voiceover(
            f"""The stipulated simulation across twenty seeds. <bookmark mark='a'/> Read terminal mean profit and its across-seed standard deviation separately; shading also changes which arrivals execute. <bookmark mark='b'/> The mean divided by that standard deviation is {ra:.1f} without shading and {rb:.0f} with it. This is a terminal-outcome ratio, not an annualized time-series Sharpe, confidence interval or proof of an optimal quote policy. The table describes these chosen parameters."""
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
                          r"and privileges at the auctions", width=12.4, font_size=25),
            desk_question(r"dealers in bonds and currencies", r"most bonds and currencies still trade with dealers, by "
                          r"request for quote; the dealer's balance sheet is the market's inventory (Part 18)", width=12.4,
                          font_size=25),
            desk_question(r"electronic market makers", r"everywhere else, algorithms quoting thousands of instruments, "
                          r"with inventory limits in place of a specialist's capital", width=12.4, font_size=25),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
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
                          r"a market with no information", width=12.4, font_size=25),
            desk_question(r"inventory", r"the risk of holding what customers sold: Ho and Stoll's shading, paid for by a "
                          r"spread that widens with volatility and position size", width=12.4, font_size=25),
            desk_question(r"adverse selection", r"some customers know more than the dealer: the next two chapters, and the "
                          r"component that does not vanish with competition", width=12.4, font_size=25),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
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
        eq = MathTex('\\operatorname{mid}=v-\\gamma q,\\quad q=40,\\ \\gamma=0.05,\\ s=1', font_size=32)
        if eq.width > 12.1:
            eq.scale_to_fit_width(12.1)
        conditions = wrapped_label('Stipulated linear quote heuristic. Derive bid and ask relative to fair value v; this is not an optimal-control claim.', 12.0, 22, GREY_A)
        setup = VGroup(eq, conditions).arrange(DOWN, buff=0.6).move_to(UP * 0.2)
        q = pause_card(r"Use the stated assumptions; derive the result and check its units and interpretation.")
        self.add(setup, q)
        with self.voiceover('Pause and predict. Under the stated quote heuristic, inventory is forty, shading is point zero five per unit and full spread is one. Derive bid and ask relative to fair value. State what the calculation assumes.'):
            self.wait(0.4)
        self.wait(0.5)
        self.clear_scene()
