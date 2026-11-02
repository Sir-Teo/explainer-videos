from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CASH, CCP, LOSS, PART, RATE, TRADE, load

PAPERS = [
    (r"Greenwood and Sammon (2025)", r"``The Disappearing Index Effect,'' \textit{Journal of Finance} 80(2)",
     r"the S\&P 500 inclusion effect shrank from about 7.4\% in the 1990s to under 1\%", 2025.2, QC.IDEA),
    (r"Pavlova and Sikorskaya (2023)", r"``Benchmarking Intensity,'' \textit{Review of Financial Studies} 36(3)",
     r"stocks tied to more benchmarks have less elastic demand, and lower returns after the intensity rises",
     2023.2, QC.IDEA),
    (r"Bryzgalova, Pavlova and Sikorskaya (2023)", r"``Retail Trading in Options and the Rise of the Big Three "
     r"Wholesalers,'' \textit{Journal of Finance} 78(6)", r"retail is over 60\% of US options volume; nearly 90\% of "
     r"options PFOF from three wholesalers; retail buys cheap weekly options with 12.6\% spreads and loses on average",
     2023.9, TRADE),
    (r"Schwarz, Barber, Huang, Jorion and Odean (2025)", r"``The `Actual Retail Price' of Equity Trades,'' "
     r"\textit{Journal of Finance} 80(5)", r"85,000 simultaneous orders at several brokers: prices differ across "
     r"brokers, because wholesalers price each broker's flow differently, not because of PFOF", 2025.7, TRADE),
    (r"Glicoes, Iorio, Monin and Petrasek (2024); Monin (2026)", r"FEDS Notes, Federal Reserve Board",
     r"measuring the Treasury cash-futures basis trade: about \$830 billion by September 2025", 2024.2, RATE),
    (r"Pinter (2023)", r"``An anatomy of the 2022 gilt market crisis,'' Bank of England Staff Working Paper 1019",
     r"who sold gilts in September 2022, and how pension funds' collateral calls drove it", 2023.5, LOSS),
]
RULES = [(r"T+1 in the US", 2024.4, True, CCP), (r"Rule 612: half-penny ticks", 2027.84, False, TRADE),
         (r"Treasury clearing: cash", 2026.99, False, RATE), (r"Treasury clearing: repo", 2027.5, False, RATE),
         (r"EU and UK T+1", 2027.78, False, CCP), (r"SEC Rules 13f-2, 10c-1a", 2028.0, False, LOSS)]


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.papers()
        self.rules()

    def card(self):
        c = chapter_card(18, r"Frontier, 2023 to 2026", r"What is new, and what is about to change?",
                         lit=(2023, 2024, 2025), part=PART)
        with self.voiceover("Chapter eighteen. The frontier, from 2023 to 2026."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def _axis(self):
        x0, x1, W = 2023.0, 2028.2, 12.4

        def X(y):
            return -W / 2 + W * (y - x0) / (x1 - x0)
        line = Line([X(x0), -2.9, 0], [X(x1), -2.9, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(y), -2.96, 0], [X(y), -2.84, 0], color=GREY_C),
                                MathTex(str(y), font_size=20, color=GREY_C).next_to([X(y), -2.9, 0], DOWN, buff=0.1))
                         for y in range(2023, 2029)])
        now = VGroup(DashedLine([X(2026.84), -3.2, 0], [X(2026.84), -2.6, 0], color=YELLOW),
                     label(r"today", font_size=16, color=YELLOW).next_to([X(2026.84), -2.6, 0], UP, buff=0.04))
        return X, VGroup(line, ticks, now)

    def papers(self):
        X, ax = self._axis()
        cards = []
        for who, where, what, yr, col in PAPERS:
            body = VGroup(label(who, font_size=21, color=col), wrapped_label(where, 5.6, 16, GREY_B),
                          wrapped_label(what, 5.6, 18, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            frame = RoundedRectangle(width=6.1, height=body.height + 0.3, corner_radius=0.1, stroke_color=col,
                                     stroke_width=1.5, fill_color="#0E141C", fill_opacity=1).move_to(body)
            cards.append((VGroup(frame, body), Dot([X(yr), -2.9, 0], radius=0.08, color=col)))
        left = VGroup(*[c for c, _ in cards[:3]]).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        right = VGroup(*[c for c, _ in cards[3:]]).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        VGroup(left, right).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(UP, buff=0.3)
        if VGroup(left, right).height > 5.6:
            VGroup(left, right).scale_to_fit_height(5.6).to_edge(UP, buff=0.3)
        dots = VGroup(*[d for _, d in cards])
        with self.voiceover(
            "Six pieces of recent research, placed on a timeline. Greenwood and Sammon show the index-inclusion "
            "effect of chapter fifteen has nearly disappeared. Pavlova and Sikorskaya measure how much of each stock "
            "is tied to benchmarks, and find that the more it is, the less elastic its demand. "
            "<bookmark mark='a'/> Bryzgalova, Pavlova and Sikorskaya document the rise of retail options trading, "
            "now over sixty percent of American options volume, with almost all of its payment for order flow coming "
            "from three wholesalers, and retail buyers paying wide spreads and losing on average. "
            "<bookmark mark='b'/> Schwarz, Barber, Huang, Jorion and Odean placed tens of thousands of identical "
            "orders at different brokers at the same moment and got different prices: the gap came from how "
            "wholesalers priced each broker's flow, not from payment for order flow. <bookmark mark='c'/> Federal "
            "Reserve economists have measured the Treasury basis trade, about eight hundred and thirty billion "
            "dollars by September 2025. And Pinter's anatomy of the 2022 gilt crisis shows who sold, and why."
        ) as vo:
            self.play(FadeIn(ax))
            self.play(FadeIn(cards[0][0]), FadeIn(cards[0][1]), FadeIn(cards[1][0]), FadeIn(cards[1][1]))
            vo.wait_until("a")
            self.play(FadeIn(cards[2][0]), FadeIn(cards[2][1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[3][0]), FadeIn(cards[3][1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[4][0]), FadeIn(cards[4][1]), FadeIn(cards[5][0]), FadeIn(cards[5][1]))
        self.wait(0.4)
        self.clear_scene()

    def rules(self):
        X, ax = self._axis()
        marks = VGroup()
        for k, (name, yr, done, col) in enumerate(RULES):
            d = Dot([X(yr), -2.9, 0], radius=0.11, color=col) if done else \
                Circle(radius=0.11, color=col, stroke_width=3).move_to([X(yr), -2.9, 0])
            t = label(name, font_size=18, color=col).move_to([X(yr), -2.3 + 0.45 * (k % 4), 0])
            if t.get_right()[0] > 6.9:
                t.shift(LEFT * (t.get_right()[0] - 6.9))
            marks.add(VGroup(d, Line(d.get_center(), t.get_bottom(), color=GREY_D, stroke_width=1), t))
        notes = VGroup(
            label(r"T+1 (28 May 2024): clearing fund $-20\%$, affirmation 73\% $\to$ 95\%, fails unchanged", font_size=19),
            label(r"Rule 612 (adopted September 2024): compliance moved to the first business day of November 2027 "
                  r"by an order of 11 June 2026", font_size=19),
            label(r"Treasury central clearing: cash trades by 31 December 2026, repo by 30 June 2027; Duffie (2023, "
                  r"Jackson Hole) argues for", font_size=19),
            label(r"broad central clearing and all-to-all trading to make the market more resilient", font_size=19),
            label(r"Rules 13f-2 and 10c-1a (short positions, securities lending): remanded, not vacated, by the Fifth "
                  r"Circuit (August 2025); compliance in 2028", font_size=19),
            label(r"EU and UK T+1 on 11 October 2027; India's 2024 F\&O measures; China's 2024 short-selling and "
                  r"program-trading rules", font_size=19),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(UP, buff=0.5)
        if notes.width > 13.2:
            notes.scale_to_fit_width(13.2).to_edge(UP, buff=0.5)
        leg = label(r"filled: in force; hollow: pending", font_size=16, color=GREY_B).to_corner(DR, buff=0.15)
        with self.voiceover(
            "And the plumbing is being rebuilt as we watch. Filled dots are in force, hollow ones pending. American "
            "settlement went to T plus one in May 2024, and the clearing fund fell a fifth. <bookmark mark='a'/> The "
            "half-penny tick, adopted in 2024, was due today, the second of November 2026; in June the SEC moved it "
            "to November 2027. <bookmark mark='b'/> Treasuries, the market behind every repo in this part, move into "
            "central clearing: cash trades by the end of this year, repo by the middle of next. Duffie argued at "
            "Jackson Hole in 2023 for exactly that, with all-to-all trading, to make the market more resilient. "
            "<bookmark mark='c'/> New SEC rules on reporting short positions and securities loans were sent back to "
            "the agency by the courts and now start in 2028. Europe and Britain go to T plus one in October 2027. "
            "Every one of these changes a number in this part."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(leg), FadeIn(marks[0]), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(marks[1]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(marks[2]), FadeIn(marks[3]), FadeIn(notes[2:4]))
            vo.wait_until("c")
            self.play(FadeIn(marks[4]), FadeIn(marks[5]), FadeIn(notes[4:]))
        self.wait(0.4)
        self.clear_scene()
