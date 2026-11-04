from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, COLL, EXPO, PART, ask, fit_right, illustration, load


class Archegos(VoiceoverScene):
    def construct(self):
        self.card()
        self.trs()
        self.fire()
        self.lessons()

    def card(self):
        c = chapter_card(13, r"March 2021: Archegos", r"How does a client's margin become the bank's loss?", lit=(2021,),
                         part=PART)
        with self.voiceover("Chapter thirteen. March 2021: how a client's margin became the banks' losses."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def trs(self):
        rows = [cmath(r"\text{client P\&L}", r"=", r"N\,\Big(\frac{S_T}{S_0} - 1\Big) - \text{financing}", font_size=38,
                      colors={r"\text{client P\&L}": EXPO}),
                cmath(r"\text{bank's exposure}", r"=", r"\max\big(-\text{client P\&L} - \text{margin},\ 0\big)",
                      font_size=36, colors={r"\text{bank's exposure}": BAD})]
        whys = [why(r"a total return swap: the bank buys the shares as its hedge and pays the client their return; the "
                    r"client pays financing and posts margin. The client owns the economics, the bank the shares, so "
                    r"no ownership filing shows the client's size"),
                why(r"if the shares fall by more than the margin, the client owes more than it posted; if it cannot pay, "
                    r"the bank must sell its hedge, and it loses whatever the fall exceeds the margin")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Archegos held its positions through total return swaps. The bank buys the shares as its hedge and pays "
            "the client their return; the client pays interest and posts margin. The client has the economics; the "
            "bank holds the shares, so no public filing showed how much of each company Archegos controlled. "
            "<bookmark mark='a'/> To the bank, the swap is a loan secured by the shares. If they fall by more than "
            "the margin and the client cannot pay, the bank sells, and keeps the difference as a loss."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def fire(self):
        rng = np.random.default_rng(4)
        d = np.arange(0, 6)
        price = np.array([100, 91, 70, 64, 52, 47.0])
        g = axes([-0.3, 5.3], [40, 105], x_length=6.8, y_length=4.2, xlabel=r"trading days from the offering",
                 ylabel=r"price, stylised", xticks=[0, 1, 2, 3, 4, 5], yticks=[50, 75, 100], font_size=14).to_edge(
            LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = VGroup(curve(ax, d, price, BAD, stroke_width=3.5), *[Dot(ax.c2p(a, b), color=BAD) for a, b in zip(d, price)])
        margin = DashedLine(ax.c2p(-0.3, 80), ax.c2p(5.3, 80), color=COLL, stroke_width=2)
        ml = label(r"margin covers a 20\% fall", font_size=17, color=COLL).next_to(ax.c2p(5.3, 80), UP, buff=0.1).shift(LEFT * 1.4)
        side = VGroup(
            wrapped_label(r"22 March 2021: ViacomCBS, one of the largest positions, announced a share offering, and its "
                          r"shares fell over the following days; Archegos could not meet the calls", 3.6, 17, GREY_A),
            wrapped_label(r"26 March: banks that sold blocks first recovered most; those that waited bore the fall. The "
                          r"same shares, sold by everyone at once: the collateral was the risk", 3.6, 17, BAD),
            wrapped_label(r"stylised path, not the record of any one stock", 3.6, 15, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "In March 2021 one of the largest positions, ViacomCBS, announced a share offering, and its shares fell. "
            "<bookmark mark='a'/> With margin sized for an ordinary fall, a decline of a third or more wiped it out. "
            "Archegos could not meet the calls. <bookmark mark='b'/> On the twenty-sixth of March the banks began to "
            "sell, each its own hedge, and each sale pushed the prices down for the others. Those who sold first "
            "recovered most of their money; those who hesitated sold into a collapse. The collateral was the risk: "
            "wrong-way risk in its purest form."
        ) as vo:
            self.play(FadeIn(g), Create(margin), FadeIn(ml), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"concentration", r"margin sized for a diversified portfolio's moves is far too little for a "
                          r"few stocks held in size; liquidation itself moves the price (Part 37)", width=12.0,
                          font_size=21),
            desk_question(r"the whole client", r"each bank saw only its own swaps; no one measured the client's total "
                          r"position across the street, which is what determined the fire sale", width=12.0,
                          font_size=21),
            desk_question(r"the record", r"the special committee's report to Credit Suisse (Paul, Weiss, July 2021) found "
                          r"repeated limit breaches the bank did not act on; Archegos's founder was convicted of fraud in "
                          r"2024", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "What went wrong is in the public record. Margin was set as if the positions were diversified, when they "
            "were a few stocks held in enormous size, and selling them moved the price. <bookmark mark='a'/> Each bank "
            "saw only its own swaps; no one measured the whole client. <bookmark mark='b'/> The report commissioned by "
            "Credit Suisse's board found repeated breaches of its limits that the bank did not act on; in 2024 a jury "
            "convicted Archegos's founder of fraud."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a client posts 20\% margin on a single-stock swap. What one number about the client would you most want "
                r"to know, and why can't you see it?")
        with self.voiceover("A client posts twenty percent margin on a single-stock swap. What one number about the client "
                            "would you most want to know, and why can't you see it?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
