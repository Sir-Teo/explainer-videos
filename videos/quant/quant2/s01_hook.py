from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CCP, PART, TRADE, arrow, node


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.life()
        self.robinhood()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"What happens when you press buy?")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part two. The machinery of markets. Part one treated prices as numbers that arrive by chance. Every one "
            "of those numbers was made by a machine: brokers, exchanges, clearing houses, lenders of cash and "
            "of shares, all wired together, all with rules about who must pay what, and when. A quant who doesn't "
            "know the machine will one day be surprised by it."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def life(self):
        names = [(r"you", GREY_B), (r"your broker", TRADE), (r"an exchange or\\a wholesaler", TRADE),
                 (r"the clearing\\house (CCP)", CCP), (r"the depository\\(settlement)", CCP), (r"your account", GREY_B)]
        nodes = VGroup()
        for t, c in names:
            nd = node(t, c, width=1.95, height=1.05, font_size=20)
            nd[1].become(Tex(r"\begin{tabular}{c}" + t + r"\end{tabular}", font_size=20).move_to(nd[0]))
            nodes.add(nd)
        nodes.arrange(RIGHT, buff=0.32).shift(UP * 0.9)
        arrows = VGroup(*[arrow(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)])
        caps = [r"an order", r"routed in microseconds", r"matched: a trade", r"novated: the CCP stands in the middle",
                r"T+1: shares and cash change hands"]
        cap_m = VGroup(*[wrapped_label(c, 2.1, 18, GREY_A).next_to(arrows[i], DOWN, buff=0.65) for i, c in enumerate(caps)])
        for i, c in enumerate(cap_m):
            c.set_x(arrows[i].get_center()[0])
        token = Dot(nodes[0].get_center(), radius=0.13, color=QC.IDEA)
        clock = VGroup(label(r"seconds", font_size=22, color=TRADE), label(r"a business day later", font_size=22, color=CCP))
        clock[0].next_to(VGroup(nodes[1], nodes[2]), UP, buff=0.35)
        clock[1].next_to(VGroup(nodes[3], nodes[4]), UP, buff=0.35)
        foot = wrapped_label(r"the US moved from settling two business days after a trade (T+2) to one (T+1) on 28 May "
                             r"2024; until settlement, the clearing house carries the risk that someone fails to pay",
                             12.0, 22, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is what happens when you press buy on a share. Your order goes to your broker, who routes it, in "
            "microseconds, to an exchange or to a wholesaler, a market maker that buys retail orders. "
            "<bookmark mark='a'/> There it meets a seller: a trade. In seconds you see the price. But nothing has "
            "changed hands yet. <bookmark mark='b'/> The trade goes to a clearing house, which steps into the middle: "
            "it becomes the buyer to every seller and the seller to every buyer. <bookmark mark='c'/> Only a "
            "business day later does the depository move the shares to your account and the cash to the seller. "
            "Until then, someone is carrying the risk that one side fails to pay, and that someone wants "
            "collateral."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.15), FadeIn(token))
            for i in range(2):
                self.play(GrowArrow(arrows[i]), FadeIn(cap_m[i]), token.animate.move_to(nodes[i + 1]), run_time=0.9)
            self.play(FadeIn(clock[0]))
            vo.wait_until("a")
            self.play(Indicate(nodes[2], color=TRADE))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[2]), FadeIn(cap_m[2]), token.animate.move_to(nodes[3]))
            self.play(GrowArrow(arrows[3]), FadeIn(cap_m[3]), FadeIn(clock[1]))
            vo.wait_until("c")
            self.play(token.animate.move_to(nodes[4]))
            self.play(GrowArrow(arrows[4]), FadeIn(cap_m[4]), token.animate.move_to(nodes[5]))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def robinhood(self):
        c = crisis_card(r"28 January 2021", r"The day a trading app stopped buying",
                        r"GameStop had risen nearly twentyfold in January. Before the open, the National Securities "
                        r"Clearing Corporation asked Robinhood for a deposit of about \$3 billion against two days of "
                        r"unsettled trades; Robinhood restricted buying in GameStop and other stocks, and the "
                        r"requirement was reduced, to about \$1.4 billion as its chief executive described it.",
                        stats=[(r"\sim\$3\,\text{bn}", r"the first request (accounts differ)"),
                               (r"\sim\$1.4\,\text{bn}", r"after talks"),
                               (r"\$3.4\,\text{bn}", r"raised by Robinhood in the following days")],
                        width=11.0, font_size=24)
        c.move_to(UP * 0.3)
        lesson = label(r"The plumbing, not the price, decided who could trade.", font_size=28, color=QC.IDEA)
        lesson.next_to(c, DOWN, buff=0.5)
        src = note(r"public record: Robinhood's statements and its chief executive's interviews (February 2021); "
                   r"SEC staff report on the January 2021 events (October 2021)", font_size=17).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "That collateral once decided who could trade. In January 2021 GameStop rose nearly twentyfold in a month, "
            "bought by millions of people through apps. Early on the 28th, the clearing house for American stocks "
            "asked Robinhood for a deposit of about three billion dollars against the trades it had not yet "
            "settled. Robinhood stopped its customers from buying GameStop and a handful of other stocks, and the "
            "requirement came down, to about one point four billion as its chief executive described it; accounts "
            "of the exact numbers differ. <bookmark mark='a'/> The price did not decide who could buy that day. The "
            "plumbing did. This part is a tour of the plumbing."
        ) as vo:
            self.play(FadeIn(c, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"The instruments, and how each one is quoted",
            r"Orders, the order book and the closing auction; exchanges, dealers and request-for-quote",
            r"Clearing and settlement: novation, netting, T+1",
            r"Margin and leverage, on a real crash: when are you liquidated?",
            r"Short selling, repo and securities lending, prime brokerage: the market's funding",
            r"Who earns what: fees, business models, the quant industry, markets around the world",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. The instruments and how each is quoted. Orders, the order book and the auction that sets "
            "the closing price. Clearing and settlement. Margin and leverage, tested on a real crash. Short "
            "selling and the market's funding: repo, securities lending, prime brokers. And who earns what: the "
            "fees, the business models, the quant industry, and markets around the world."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=9))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("treasury",))
        with self.voiceover(
            "The House gets its second desk. <bookmark mark='a'/> Treasury and funding: what it costs, in cash and "
            "collateral, to hold a position. From now on, every backtest in the series pays it."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["treasury"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
