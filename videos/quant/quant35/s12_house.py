from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import micro as M
from videos.quant.quant35.common import BAD, DEALER_C, FLOW_C, GOOD, INF_C, PART, PRICE_C, comma, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("dealer"), load("gm"), load("kyle"), load("flow"), load("measures"), load("vpin"),
                   load("discovery"))
        self.footprint(load("flow"))
        self.lab()
        self.lab2()
        self.lab3()
        self.lab4()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(11, r"Rule 35: know who is on the other side", r"What must the House know about a market "
                         r"before it trades there?", part=PART)
        with self.voiceover("Chapter eleven. The House's thirty-fifth rule is about the counterparty. Before any desk "
                            "trades in a market, it must know who it is likely to be trading with, and what its own "
                            "orders will tell them."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, dl, g, k, f, m, v, d):
        rows = [(r"dealer inventory sd, without and with shading", rf"{dl['0.0']['inv_sd']:.0f},\ "
                 rf"{dl['0.05']['inv_sd']:.1f}", DEALER_C),
                (r"Glosten--Milgrom, $\mu = 0.3$: trades to 99\% belief", rf"{g['0.3']['to99']:.0f}", PRICE_C),
                (r"Kyle, continuous: insider's profit, simulated", rf"{k['bridge_profit']:.3f}", INF_C),
                (r"Bitcoin: $\lambda$ per \$1m, $R^2$ at 1 min and 1 hour", rf"{f['full']['lambda']:.2f};\ "
                 rf"{f['agg']['1']['r2']:.2f},\ {f['agg']['60']['r2']:.2f}", FLOW_C),
                (r"SPY: Roll and Corwin--Schultz spreads, bp", rf"{m['etfs'][0]['roll_bp']:.0f},\ "
                 rf"{m['etfs'][0]['cs_bp']:.0f}", BAD),
                (r"VPIN's correlation with volatility and with true imbalance", rf"{v['corr_rv']:.2f},\ {v['corr_true']:.2f}",
                 INF_C),
                (r"perpetual vs spot: return correlation; IS bound width", rf"{d['corr0']:.3f};\ {d['width']:.2f}", GOOD)]
        hx = [-2.4, 4.6]
        tab = VGroup()
        for j, (txt, val, col) in enumerate(rows):
            y = 2.4 - 0.65 * j
            tab.add(VGroup(label(txt, font_size=17, color=col).move_to([hx[0], y, 0]),
                           MathTex(val, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The microstructure desk's first sheet", font_size=28).to_edge(UP, buff=0.25)
        foot = wrapped_label(r"computed in this part from simulation, Binance's public one-minute bars (2021--2024) and "
                             r"Yahoo Finance's daily ETF bars (2015--2020); none is advice", 12.0, 15,
                             GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> Shading keeps a dealer's inventory small. Informed trading makes the "
            "spread wide and the price fast. The continuous insider earns what the theorem says. Bitcoin's order flow "
            "has a measurable, concave price, and explains a fifth to a third of its moves. The classic daily spread "
            "estimators fail on liquid funds. VPIN measures volatility more than toxicity. And one-minute data cannot "
            "tell which Bitcoin market discovers the price."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def footprint(self, f):
        import math
        lam = f["full"]["lambda"]
        size = 10.0
        lin = lam * size
        sq_one = lam * 1.0
        cost_sq = sq_one * math.sqrt(size)
        per_min = size / 60
        sliced = 60 * lam * per_min * per_min
        rows = [cmath(r"\$10\text{m in one minute}", r":", rf"\lambda \times 10 = {lin:.0f}\ \text{{bp on the line}}",
                      font_size=32, colors={r"\$10\text{m in one minute}": BAD}),
                cmath(r"\text{square root}", r":", rf"\approx {cost_sq:.0f}\ \text{{bp}}", font_size=32),
                cmath(r"\$10\text{m over an hour}", r":", rf"\text{{each minute moves }} {lam * per_min:.2f}\ \text{{bp}}",
                      font_size=32, colors={r"\$10\text{m over an hour}": GOOD})]
        whys = [why(r"the House's book on the coins (Part 27) rebalancing ten million dollars of Bitcoin at once, on Kyle's "
                    r"straight line"),
                why(r"on the concave response measured in Chapter 5, scaled from the cost of one million"),
                why(r"sliced into sixty one-minute pieces, each moves the price by a fraction of a basis point, and much of "
                    r"each touch reverses: Part 37 finds the best schedule")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "And the House's own footprint. <bookmark mark='a'/> If the House's coin book rebalanced ten million dollars "
            f"of Bitcoin in one minute, Kyle's straight line says {lin:.0f} basis points. <bookmark mark='b'/> The "
            f"concave response measured in Chapter five says nearer {cost_sq:.0f}. <bookmark mark='c'/> Sliced over an "
            f"hour, each minute's piece moves the price by {lam * per_min:.2f} of a basis point, and much of each touch "
            "reverses. How to slice optimally is Part thirty-seven."
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

    def lab(self):
        card = house_lab(r"Glosten--Milgrom quotes", M.gm_quotes, "pb_hi, pb_lo", 4, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter two's quotes in four lines. The probability of a buy when the value is high, and when it is low; "
            "Bayes' rule for the value given a buy, and given a sell; and the quotes are the expected values. Nothing in "
            "it knows about profit: zero profit is built into the definition."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"Kyle's lambda from data", M.kyle_lambda, "r = np.asarray(ret, float)", 11, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter five's regression: drop missing minutes, regress returns on signed flow with a constant, and report "
            "lambda with its t-statistic and the share of variance explained. The research chapter's test of Kyle's "
            "model is that last number."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab3(self):
        card = house_lab(r"Hasbrouck's information shares", M.hasbrouck_is, "a_perp = np.array", 3,
                         extra=((M.hasbrouck_is, "for order in ((0, 1), (1, 0)):", 7),), width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And Chapter seven's shares. The common trend's weights are the complement of the adjustment speeds; then, "
            "for each ordering of the two markets, factor the residual covariance and take each market's part of the "
            "efficient price's variance. Two orderings, two answers, and the truth between them."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab4(self):
        card = house_lab(r"Kyle in continuous time, simulated", M.kyle_continuous, "for k in range(n):", 7, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And the research chapter's market. At each step the insider trades the remaining gap over the remaining "
            "time, the noise adds its random order, and the price moves by lambda times the total. Seven lines, and every "
            "path ends at the value."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("compliance", "data")).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{inventory\_dealer}, \texttt{gm\_quotes}, \texttt{gm\_simulate}", r"dealers"),
            (r"\texttt{kyle\_one}, \texttt{kyle\_multi}, \texttt{kyle\_continuous}", r"Kyle"),
            (r"\texttt{roll\_spread}, \texttt{amihud}, \texttt{kyle\_lambda}", r"liquidity"),
            (r"\texttt{bvc\_vpin}, \texttt{hasbrouck\_is}", r"toxicity, discovery"),
            (r"\texttt{data.binance\_klines}: \texttt{taker\_buy}", r"signed flow"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 35: before a desk trades in a market, it states who is likely on the other side "
                             r"(dealers, informed traders, others' algorithms) and measures the market's price of flow; "
                             r"it estimates its own orders' impact from signed flow where that exists, not from daily "
                             r"spread proxies; and the compliance desk's surveillance reads the desk's own orders as an "
                             r"adversary would.", 12.4, 17, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds. <bookmark mark='a'/> Dealers; Kyle in three forms; liquidity measures; toxicity "
            "and discovery; and a feed of signed flow. <bookmark mark='b'/> And the thirty-fifth rule. Before a desk "
            "trades in a market it states who is likely on the other side, and measures the market's price of flow. It "
            "estimates its own impact from signed flow where that exists, not from daily spread proxies. And the "
            "compliance desk reads the desk's own orders as an adversary would."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=4))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the research paper with Roll spreads", r"ask whether the asset's true spread is a cent; if it "
                          r"is, the estimator measures reversal (Chapter 4)", width=12.0, font_size=19),
            desk_question(r"the vendor selling a toxicity signal", r"ask for its correlation with volatility and with "
                          r"signed flow where both exist (Chapter 6)", width=12.0, font_size=19),
            desk_question(r"the desk that must buy \$50m today", r"ask for lambda, its concavity, and who will see the "
                          r"orders; then slice them (Chapter 5, Part 37)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The rule against three cases. <bookmark mark='a'/> A paper that measures spreads with Roll's estimator: ask "
            "whether the true spread is a cent. <bookmark mark='b'/> A vendor selling a toxicity signal: ask for its "
            "correlation with volatility, and with signed flow. <bookmark mark='c'/> A desk that must buy fifty million "
            "dollars today: ask for lambda, its concavity, and who will see the orders, then slice them."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
