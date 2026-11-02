from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, illustration, load


class India(VoiceoverScene):
    def construct(self):
        self.card()
        self.boom()
        self.case()
        self.toy(load("alleged"))

    def card(self):
        c = chapter_card(6, r"India's expiry-day boom, and a case file", r"Who wins when retail buys weekly options?",
                         part=PART)
        with self.voiceover("Chapter six. India's expiry-day boom, and a case file."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def boom(self):
        stats = VGroup(
            VGroup(MathTex(r"91\%", font_size=56, color=THETA),
                   wrapped_label(r"of individual traders in equity derivatives lost money in 2023--24 (SEBI study, "
                                 r"September 2024)", 3.4, 19, GREY_A)).arrange(DOWN, buff=0.1),
            VGroup(MathTex(r"\text{Rs } 1.8\ \text{lakh crore}", font_size=40, color=THETA),
                   wrapped_label(r"their net losses over 2021--22 to 2023--24, about \$21 billion", 3.4, 19,
                                 GREY_A)).arrange(DOWN, buff=0.1),
            VGroup(MathTex(r"\text{Rs } 1.06\ \text{lakh crore}", font_size=40, color=THETA),
                   wrapped_label(r"losses in 2024--25 alone, after the rules were tightened (SEBI, July 2025)", 3.4, 19,
                                 GREY_A)).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=0.6, aligned_edge=UP).to_edge(UP, buff=0.7)
        rules = VGroup(
            label(r"SEBI's circular of 1 October 2024, effective 20 November 2024:", font_size=22, color=GREY_A),
            label(r"$\cdot$ weekly expiries on one benchmark index per exchange (the Nifty 50, the Sensex)", font_size=21),
            label(r"$\cdot$ minimum contract size raised to Rs 15 lakh", font_size=21),
            label(r"$\cdot$ an extra 2\% margin on short options on expiry day", font_size=21),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(stats, DOWN, buff=0.6)
        foot = wrapped_label(r"weekly options are cheap and short-dated: lottery tickets with expiry every few days, "
                             r"priced with Part 10's gamma at its most extreme", 11.0, 20, GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "India's National Stock Exchange has been the world's largest derivatives exchange by number of contracts "
            "traded for several years, most of them short-dated index options, many bought by individuals. In September 2024 India's regulator, SEBI, "
            "published what happened to them: ninety-one percent of individual traders in equity derivatives lost "
            "money in the year to March 2024, and their net losses over three years came to about one point eight "
            "lakh crore rupees, some twenty-one billion dollars. <bookmark mark='a'/> SEBI tightened the rules from "
            "November 2024: weekly expiries on only one index per exchange, larger contracts, and extra margin on "
            "expiry day. <bookmark mark='b'/> Losses the following year were still above one lakh crore rupees, and "
            "ninety-one percent still lost. Somebody is on the other side of those trades."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(s_) for s_ in stats[:2]], lag_ratio=0.5, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(rules), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(stats[2]))
        self.wait(0.4)
        self.clear_scene()

    def case(self):
        card = crisis_card(
            r"3 July 2025", r"SEBI's interim order against Jane Street",
            r"In an interim order, SEBI alleged that on expiry days of the Bank Nifty index, entities of the Jane "
            r"Street group bought the index's constituents and futures in the morning, supporting the index while "
            r"building large positions in index options that would profit from a fall, and then sold in the "
            r"afternoon, pushing the index down. SEBI barred the entities and impounded about Rs 4{,}844 crore of "
            r"what it called unlawful gains. Jane Street disputes the findings; it deposited the amount in escrow and "
            r"was allowed to resume trading while the case continues.",
            stats=[(r"\text{Rs } 4{,}844\ \text{cr}", r"impounded, pending the case"), (r"\text{alleged}",
                                                                                     r"not proven; contested by the firm")],
            width=11.4, font_size=24)
        card.move_to(ORIGIN)
        src = note(r"SEBI interim order, 3 July 2025; the firm's public statements. These are allegations; no final "
                   r"finding had been made at the time of writing.", font_size=17, color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "In July 2025 SEBI issued an interim order against entities of Jane Street. These are allegations, "
            "contested by the firm, and no final finding had been made when this was written. SEBI alleged that on "
            "expiry days of the Bank Nifty index, the firm bought the index's member stocks and futures in the "
            "morning, holding the index up while building large positions in index options that would gain if it "
            "fell, then sold in the afternoon and pushed it down. SEBI barred the entities and impounded about four "
            "thousand eight hundred crore rupees of what it called unlawful gains. Jane Street disputed the "
            "findings, deposited the amount in escrow, and was allowed to resume trading while the case continued."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()

    def toy(self, a):
        t, idx = np.asarray(a["t"]), np.asarray(a["index"])
        g = axes([0, 1], [98.5, 101.5], x_length=6.4, y_length=3.6, xlabel=r"the trading day",
                 ylabel=r"index", xticks=[0, 0.5, 1], xfmt=lambda u: {0: "open", 0.5: "noon", 1: "close"}[round(u * 2) / 2],
                 yticks=[99, 100, 101], font_size=17).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, t, idx, SPOT, stroke_width=3.5)
        rows = VGroup(
            label(r"a toy with linear price impact, to explain the mechanics alleged:", font_size=21, color=GREY_A),
            MathTex(rf"\text{{morning: buy }} Q = {a['Q']:.0f}\ \Rightarrow\ +{a['move_up']:.0f}\ \text{{point}}",
                    font_size=28),
            MathTex(rf"\text{{options: short delta of }} {a['D']:.0f}\ \text{{units, near the top}}", font_size=28,
                    color=VEGA),
            MathTex(rf"\text{{afternoon: sell }} 2Q\ \Rightarrow\ -{a['move_down']:.0f}\ \text{{points}}", font_size=28),
            MathTex(rf"\text{{cash and futures: }} {a['cash_leg']:+.0f};\ \ \text{{options: }} {a['options_leg']:+.0f}",
                    font_size=28, color=OPT),
            wrapped_label(r"the point: if the options position is much larger than the trading that moves the index, "
                          r"the trading can lose money and the whole still profit. Whether this happened is for SEBI "
                          r"and the courts; this shows only why regulators watch expiry days and position sizes "
                          r"together", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        src = illustration(r"illustration: invented numbers, not the case's")
        with self.voiceover(
            "Why would anyone do what is alleged? A toy model with invented numbers shows the mechanics. Buying in "
            "the morning pushes an index up a point. <bookmark mark='a'/> Meanwhile a position in index options that "
            "gains if the index falls is built, much larger than the trading. <bookmark mark='b'/> In the afternoon, "
            "selling twice as much pushes the index two points down by the close. The cash and futures trading "
            "roughly breaks even, but the options gain on a scale set by their size. <bookmark mark='c'/> That is "
            "all this toy shows: why regulators watch expiry days, and the size of options positions next to the "
            "trading in the underlying, together. Whether it happened in this case is for SEBI and the courts."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(rows[0]))
            self.play(Create(line), FadeIn(rows[1]), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()
