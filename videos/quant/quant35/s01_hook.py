from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant35.common import (BAD, FLOW_C, GOOD, HURDLE, INF_C, PART, PRICE_C, VALUE_C, era_strip,
                                         illustration, load)


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.leak(load("kyle"))
        self.claims(load("flow"), load("vpin"), load("measures"))
        self.act()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Who Trades With Whom")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-five. Who trades with whom: the dealers, the informed and the rest, and what their orders reveal. "
            "Act six begins: market microstructure."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def leak(self, k):
        t = np.asarray(k["bridge_t"], float)
        p = np.asarray(k["bridge_example"][0], float)
        v = float(k["bridge_v"][0])
        lo = float(np.floor(min(p.min(), v, 0) - 0.5))
        hi = float(np.ceil(max(p.max(), v, 0) + 0.5))
        g = axes([0, 1], [lo, hi], x_length=8.0, y_length=4.4, xlabel=r"the trading day", ylabel=r"the price",
                 xticks=[0, 0.5, 1], yticks=[], font_size=15).move_to(LEFT * 1.0 + DOWN * 0.2)
        ax = g.ax
        val = DashedLine(ax.c2p(0, v), ax.c2p(1, v), color=VALUE_C, stroke_width=2)
        c1 = curve(ax, t, p, PRICE_C, stroke_width=3)
        lv = label(r"what the insider knows", font_size=17, color=VALUE_C).next_to(ax.c2p(0, v), UR, buff=0.1)
        ill = illustration(r"simulated: Kyle's market in continuous time")
        with self.voiceover(
            "One trader knows what the asset is worth. <bookmark mark='a'/> Everyone else sees only the price, and the "
            "orders. <bookmark mark='b'/> The insider buys slowly, hidden among traders who know nothing, and the price "
            "drifts, through noise, to exactly what the insider knew, by the end of the day. This part is about how "
            "information gets into prices, who pays to put it there, and what it costs everyone else to trade."
        ) as vo:
            self.play(FadeIn(g), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(val), FadeIn(lv))
            vo.wait_until("b")
            self.play(Create(c1), run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def claims(self, f, v, m):
        lam = f["full"]["lambda"]
        spy = m["etfs"][0]["roll_bp"]
        cards = VGroup(
            desk_question(r"the price of order flow", rf"on Bitcoin, each million dollars of net aggressive buying moves "
                          rf"the price {lam:.1f} basis points within the minute, and the response is concave, as Part 31's "
                          r"square-root law says", width=12.4, font_size=19),
            desk_question(r"measures that fail", rf"Roll's spread from daily prices puts SPY at {spy:.0f} basis points; "
                          r"its quoted spread is a third of one; VPIN tracks volatility, not the true order imbalance",
                          width=12.4, font_size=19),
            desk_question(r"an exact theorem", r"in continuous time the insider earns twice the one-shot profit and the "
                          r"price reaches the value exactly: a Brownian bridge (the research chapter)", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What this part finds. <bookmark mark='a'/> On Bitcoin, every million dollars of net aggressive buying moves "
            f"the price {lam:.1f} basis points within the minute, and the response is concave. "
            "<bookmark mark='b'/> Classic liquidity measures built from daily prices fail badly on today's liquid "
            f"markets: Roll's spread for SPY is {spy:.0f} basis points, against a true third of one, and a famous "
            "toxicity measure tracks volatility rather than the true imbalance of orders. <bookmark mark='c'/> And an "
            "exact theorem: an insider who trades continuously earns twice as much as one who trades once, and the price "
            "ends exactly at the value."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits. Act five built strategies and the firm. Act six goes inside the trade itself: this part, "
            "who trades with whom; then the limit order book, execution, market making, and digital-asset markets. It "
            "uses Part four's martingales, Part seven's filters, Part eight's control, and Part thirty-one's impact."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        entries = [(1976, r"Garman", I), (1981, r"Ho--Stoll", I), (1984, r"Roll", I), (1985, r"Kyle; Glosten--Milgrom", I),
                   (1992, r"Back", I), (1995, r"Hasbrouck", I), (1996, r"PIN", I), (2002, r"Amihud", I),
                   (2005, r"Reg NMS", I), (2010, r"the flash crash", BAD), (2012, r"VPIN", I),
                   (2015, r"batch auctions", I), (2024, r"T+1", I)]
        strip = era_strip(entries, y0=1972, y1=2027, font_size=12, step=10).move_to(DOWN * 0.3)
        head = label(r"Fifty years of microstructure", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 5), (5, 9), (9, 13)]
        with self.voiceover(
            "Fifty years of the field. Mark Garman named it in 1976; Ho and Stoll, Roll, then Kyle and Glosten and "
            "Milgrom in 1985, and Back's continuous-time proof in 1992. <bookmark mark='a'/> Then measurement: "
            "Hasbrouck's price discovery, PIN, Amihud's illiquidity, and the rules that built today's fragmented "
            "American market. <bookmark mark='b'/> And the electronic era: the flash crash, VPIN, batch auctions, and "
            "next-day settlement."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk in zip(groups, [None, "a", "b"]):
                if mk:
                    vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"The dealer's problem: inventory (Garman; Ho and Stoll)",
            r"Glosten and Milgrom: the spread as insurance against the informed",
            r"Kyle: how an insider trades, and lambda",
            r"Measuring liquidity: Roll, Corwin--Schultz, Amihud; Kyle's lambda on Bitcoin",
            r"Toxic flow (PIN, VPIN) and price discovery across markets",
            r"Market structure, high-frequency traders, and when liquidity vanishes",
            r"For the researcher: Kyle in continuous time, proved",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: the dealer's inventory problem; Glosten and Milgrom's spread; Kyle's insider; measuring liquidity "
            "from prices; Kyle's lambda measured on Bitcoin; toxic flow; price discovery between spot and futures; the "
            "plumbing of American markets; high-frequency market makers; the flash crashes and batch auctions; and Kyle's "
            "model in continuous time, proved."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("compliance", "data"))
        with self.voiceover(
            "In the House, this part gives the compliance desk its surveillance tools, and the data desk a feed of signed "
            "order flow: the raw material for the execution and market-making desks still to come."
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()
