from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import GAIN, LOSS, PART, PRICE, VALUE

OFFER, NOW, FALL = 50.0, 47.0, 35.0


class Events(VoiceoverScene):
    def construct(self):
        self.card()
        self.spread()
        self.put()
        self.shire()

    def card(self):
        c = chapter_card(8, r"Corporate events: merger arbitrage", r"What is a takeover spread paying you for?",
                         part=PART)
        with self.voiceover("Chapter eight. Corporate events, and merger arbitrage."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def spread(self):
        g = axes([0, 10], [25, 60], x_length=6.0, y_length=4.6, xlabel=r"time", ylabel=r"target's share price",
                 xticks=[], yticks=[30, 35, 40, 45, 50, 55], font_size=18).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        pre = curve(ax, [0, 1, 2, 3], [39, 40, 39.5, 40], GREY_B, stroke_width=3)
        jump = curve(ax, [3, 3.05, 4, 5, 6], [40, 46.5, 47, 47.3, 47], PRICE, stroke_width=3.5)
        offer = DashedLine(ax.c2p(3, OFFER), ax.c2p(10, OFFER), color=GAIN, stroke_width=2.5)
        up = curve(ax, [6, 8, 10], [47, 48.5, OFFER], GAIN, stroke_width=3.5)
        down = curve(ax, [6, 6.6, 8, 10], [47, FALL, 36, 35.5], LOSS, stroke_width=3.5)
        brace = BraceBetweenPoints(ax.c2p(4.6, OFFER), ax.c2p(4.6, NOW), direction=RIGHT, color=YELLOW)
        bl = MathTex(r"\text{spread } 3", font_size=26, color=YELLOW).next_to(brace, RIGHT, buff=0.08)
        lab = VGroup(label(r"offer 50", font_size=20, color=GAIN).next_to(ax.c2p(10, OFFER), UP, buff=0.08),
                     label(r"announced", font_size=19, color=GREY_B).next_to(ax.c2p(3, 46.5), LEFT, buff=0.1))
        p = (NOW - FALL) / (OFFER - FALL)
        side = VGroup(
            wrapped_label(r"buy the target at 47; the bidder pays 50 if the deal closes", 4.6, 22, GREY_A),
            MathTex(rf"\text{{closes: }}+{OFFER - NOW:.0f}\ (+{100 * (OFFER / NOW - 1):.1f}\%)", font_size=30,
                    color=GAIN),
            MathTex(rf"\text{{fails: }}-{NOW - FALL:.0f}\ (-{100 * (1 - FALL / NOW):.1f}\%)", font_size=30, color=LOSS),
            MathTex(r"\text{implied chance of closing: } \frac{47 - 35}{50 - 35}", rf"= {100 * p:.0f}\%", font_size=30),
            label(r"(ignoring time value; illustrative numbers)", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "When one company bids for another, the target's shares jump towards the offer, but not all the way. "
            "Here the bidder offers fifty a share, and the target trades at forty-seven. <bookmark mark='a'/> The "
            "gap is the spread. A merger arbitrageur buys the target, hedging the bidder's shares if it pays in stock, "
            "and waits. <bookmark mark='b'/> If the deal closes, the arbitrageur earns three, about six percent, in a few months. "
            "If it fails, on a regulator's veto, a lost vote or a financing that falls through, the shares fall back "
            "to where they were or lower: a loss of twelve. <bookmark mark='c'/> The price itself is a forecast: a "
            "spread of three against a downside of twelve says the market puts the chance of closing at about eighty "
            "percent."
        ) as vo:
            self.play(FadeIn(g), Create(pre))
            self.play(Create(jump), Create(offer), FadeIn(lab))
            vo.wait_until("a")
            self.play(GrowFromCenter(brace), FadeIn(bl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(up), FadeIn(side[1]))
            self.play(Create(down), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def put(self):
        m = np.linspace(-0.3, 0.3, 121)
        arb = np.where(m > -0.05, 0.01, 0.01 + 0.4 * (m + 0.05))
        g = axes([-0.3, 0.3], [-0.1, 0.04], x_length=6.6, y_length=4.4, xlabel=r"market return in the month",
                 ylabel=r"merger-arbitrage return", xticks=[-0.2, -0.1, 0, 0.1, 0.2], yticks=[-0.08, -0.04, 0, 0.04],
                 xfmt=lambda u: f"{100 * u:.0f}\\%", yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=18)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, m, arb, VALUE, stroke_width=4)
        side = VGroup(
            label(r"schematic, after Mitchell and Pulvino (2001)", font_size=19, color=GREY_B),
            wrapped_label(r"4,750 mergers, 1963--1998: in flat and rising markets the returns barely depend on the "
                          r"market; in severe falls they do, because deals break when markets crash", 4.8, 22, GREY_A),
            wrapped_label(r"the payoff of a short index put; after costs, an excess return of about 4\% a year: "
                          r"payment for insurance the arbitrageur provides", 4.8, 22, VALUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Add up many deals and you get a strategy, and in 2001 Mark Mitchell and Todd Pulvino measured it on four "
            "thousand seven hundred and fifty mergers from 1963 to 1998. <bookmark mark='a'/> In calm and rising "
            "markets its returns barely depend on the market: deals close or fail for their own reasons. But in "
            "severe falls they do depend on it, because in a crash buyers walk away and financing disappears, and "
            "deals break together. <bookmark mark='b'/> That shape, a small steady gain with a kink into losses "
            "when the market falls hard, is the payoff of selling a put on the market. After transaction costs they "
            "found an excess return of about four percent a year, which they read as payment for providing "
            "insurance. A strategy that looks like free money is often an option someone sold without saying so."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def shire(self):
        card = firm_card(r"AbbVie and Shire, 2014",
                         r"AbbVie agreed in July 2014 to buy Shire for about \$54 billion, partly to move its tax "
                         r"domicile abroad. On 22 September the US Treasury announced rules against such tax "
                         r"inversions; on 15 October AbbVie's board withdrew its recommendation, and the deal ended.",
                         numbers=[(r"\$1.6\text{bn}", r"break fee AbbVie paid Shire"),
                                  (r"\text{Oct.\ 2014}", r"spreads widened across the merger-arbitrage book")],
                         source=r"AbbVie, Form 8-K, October 2014; Gabelli funds' letters", width=8.4)
        card.move_to(ORIGIN)
        with self.voiceover(
            "A real break. In 2014 AbbVie agreed to buy Shire for about fifty-four billion dollars, partly to move its "
            "tax home out of the United States. In September the Treasury announced rules against such inversions, "
            "and in October AbbVie walked away, paying a break fee of about one point six billion. Shire's shares "
            "fell sharply. Funds holding the spread lost heavily, and spreads on other deals widened at the same "
            "time: the put was exercised, and on the whole book at once."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()
