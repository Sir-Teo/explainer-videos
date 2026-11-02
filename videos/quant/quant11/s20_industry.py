from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, pause, real_data

# Contracts cleared by the Options Clearing Corporation (billions; options and futures), as OCC published them:
# 2019 4.98 and 2021 9.93 and 2022 10.38 (OCC press releases, January 2020, 2022, 2023); 2023 11.1 (OCC, January
# 2024); 2025 15.3 (OCC 2025 annual report).
OCC = [(2019, 4.98), (2021, 9.93), (2022, 10.38), (2023, 11.1), (2025, 15.3)]


class Industry(VoiceoverScene):
    def construct(self):
        self.card()
        self.scale_()
        self.retail()
        self.firms()
        self.desk()

    def card(self):
        c = chapter_card(17, r"Industry: who makes options markets", r"How do the desks actually do it?",
                         lit=(1987, 2000), part=PART)
        with self.voiceover("Chapter seventeen. The industry: who makes options markets, and how."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def scale_(self):
        g = axes([2018.4, 2025.6], [0, 17], x_length=7.0, y_length=4.2, ylabel=r"contracts cleared by the OCC, billions",
                 xticks=[2019, 2021, 2022, 2023, 2025], xfmt=lambda u: f"{int(u)}", yticks=[0, 5, 10, 15],
                 font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        bars, nums = VGroup(), VGroup()
        for y, v in OCC:
            a, b = g.ax.c2p(y, 0), g.ax.c2p(y, v)
            bars.add(Rectangle(width=0.6, height=b[1] - a[1], stroke_width=0, fill_color=OPT, fill_opacity=0.85).move_to(
                (a + b) / 2))
            nums.add(MathTex(f"{v:g}", font_size=24, color=OPT).next_to(bars[-1], UP, buff=0.06))
        side = VGroup(
            wrapped_label(r"the US options market's clearing house, which stands between the two sides of every "
                          r"listed option", 4.4, 20, GREY_A),
            wrapped_label(r"growth driven by short-dated options and retail traders since 2020; same-day (0DTE) "
                          r"options are Part 12's", 4.4, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        src = real_data(r"OCC press releases and the OCC 2025 annual report (options and futures)")
        with self.voiceover(
            "First the scale. Every listed American option is cleared by one company, the Options Clearing "
            "Corporation, which stands between buyer and seller. In 2019 it cleared about five billion contracts. "
            "<bookmark mark='a'/> Then retail traders arrived, and short-dated options with them: ten billion in "
            "2021, eleven in 2023, and fifteen point three billion in 2025, by its own annual report. Someone has to "
            "quote every one of those strikes, all day."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), GrowFromEdge(bars[0], DOWN), FadeIn(nums[0]), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_, DOWN), FadeIn(n_)) for b_, n_ in
                                    zip(bars[1:], nums[1:])], lag_ratio=0.4, run_time=3), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def retail(self):
        c1 = theorem_card(r"Bryzgalova, Pavlova and Sikorskaya (2023)", r"Retail trading reached over 60\% of US option "
                          r"volume by their measure. Nearly 90\% of options payment for order flow comes from three "
                          r"wholesalers: Citadel Securities, Susquehanna and Wolverine. Retail favours cheap, "
                          r"short-dated options, pays wide spreads, and loses on average.",
                          who=r"\textit{Retail trading in options and the rise of the big three wholesalers}, JF",
                          color=QC.FIRM, width=6.3, font_size=20)
        c2 = theorem_card(r"Muravyev and Pearson (2020)", r"Quoted spreads overstate what careful traders pay: measured "
                          r"against a fair value that moves with the underlying, traders who time their orders pay "
                          r"effective spreads under 40\% of the conventional measure.",
                          who=r"\textit{Options trading costs are lower than you think}, RFS", color=QC.FIRM, width=6.3,
                          font_size=20)
        cards = VGroup(c1, c2).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(UP, buff=0.5)
        if cards.width > 13.2:
            cards.scale_to_fit_width(13.2)
        pc = pause(r"Why would a wholesaler pay a broker for your option orders?", width=5.6, font_size=22,
                   corner=DOWN)
        with self.voiceover(
            "Who is on the other side of retail? Svetlana Bryzgalova, Anna Pavlova and Taisiya Sikorskaya traced it. "
            "By their measure retail trading reached over sixty percent of American option volume, and nearly ninety "
            "percent of the payment for order flow in options comes from three wholesalers: Citadel Securities, "
            "Susquehanna and Wolverine. Retail traders favour cheap, short-dated options, pay wide spreads, and lose "
            "on average. <bookmark mark='a'/> Dmitriy Muravyev and Neil Pearson showed the other side of the coin: a "
            "trader who times orders against a fair value that moves with the stock pays an effective spread less "
            "than forty percent of the conventional measure. <bookmark mark='b'/> Pause and predict: why would a wholesaler pay a broker for your orders? "
            "Because, on average, your orders are not informed: chapter eight's adverse selection, running the other "
            "way."
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(pc))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def firms(self):
        cards = VGroup(
            firm_card(r"Susquehanna (SIG)", r"Founded in May 1987, months before Black Monday, as an options market "
                      r"maker. Its graduate training, by its own job postings, teaches game theory and decision science, "
                      r"with classes in poker.", width=4.3, font_size=21),
            firm_card(r"Optiver and IMC", r"Amsterdam market makers founded in 1986 and 1989 on the European Options "
                      r"Exchange floor; now electronic, quoting options and ETFs worldwide.", width=4.3, font_size=21),
            firm_card(r"Jane Street", r"Founded in 2000; a market maker in ETFs, bonds and options across the world's "
                      r"exchanges, and a large trader in India's index options (chapter 15).", width=4.3,
                      font_size=21),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(UP, buff=0.5)
        if cards.width > 13.2:
            cards.scale_to_fit_width(13.2)
        opt = crisis_card(r"2008--2012", r"CFTC v.\ Optiver", r"The CFTC charged in 2008 that Optiver's traders tried "
                          r"to manipulate the settlement prices of NYMEX crude oil, heating oil and gasoline futures at "
                          r"least 19 times in March 2007, by trading heavily near the close. In 2012 a consent order "
                          r"required \$14 million in penalty and disgorgement.", width=9.6, font_size=19)
        opt.next_to(cards, DOWN, buff=0.4)
        src = note(r"firms' own pages and job postings; CFTC press releases 5521-08 and 6239-12", font_size=16,
                   color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "The firms, from the public record. Susquehanna was founded in May 1987 as an options "
            "market maker; its training, by its own job postings, teaches game theory and poker. <bookmark mark='a'/> Optiver and IMC began on the Amsterdam options "
            "floor in 1986 and 1989, and quote electronically across the world. <bookmark mark='b'/> Jane Street, "
            "founded in 2000, makes markets in funds, bonds and options. <bookmark mark='c'/> The record includes "
            "trouble too. In 2008 the American commodity regulator charged that Optiver's traders had tried to "
            "manipulate the settlement prices of oil and gasoline futures at least nineteen times in one month of "
            "2007, by trading heavily into the close; a 2012 consent order made the firm and its traders pay "
            "fourteen million dollars."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(opt, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def desk(self):
        steps = [
            (r"fit", r"a volatility surface to the market, refitted as quotes and trades arrive", VEGA, r"Part 12"),
            (r"quote", r"bids and offers in volatility around the surface, leaning against inventory", OPT, r"chapter 9"),
            (r"limit", r"each Greek, by expiry and by strike, against the desk's limits", ALT, r"chapter 10"),
            (r"hedge", r"delta automatically in futures; gamma and vega with other options", GAMMA, r"chapter 10"),
            (r"explain", r"every day's P\&L, term by term; investigate what is unexplained", QC.HOUSE, r"chapter 1"),
        ]
        boxes = VGroup()
        for name, what, col, ref in steps:
            b = RoundedRectangle(width=2.35, height=2.3, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                 fill_color=col, fill_opacity=0.08)
            t = VGroup(label(name, font_size=26, color=col), wrapped_label(what, 2.0, 17, GREY_A),
                       label(ref, font_size=16, color=GREY_B)).arrange(DOWN, buff=0.15)
            boxes.add(VGroup(b, t.move_to(b)))
        boxes.arrange(RIGHT, buff=0.35).move_to(UP * 0.6)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, color=GREY_B, stroke_width=3)
                          for i in range(len(boxes) - 1)])
        venue = VGroup(
            label(r"and the venue's rules shape the trade:", font_size=21, color=GREY_A),
            label(r"Deribit settles on a 30-minute average of its index (chapter 11)", font_size=19, color=GREY_B),
            label(r"NSE's expiry-day margins and SEBI's position limits (chapters 14 and 15)", font_size=19, color=GREY_B),
            label(r"Cboe's indices turn options into a price of correlation (chapter 13)", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(boxes, DOWN, buff=0.5)
        with self.voiceover(
            "And how does a desk run, as the firms describe it in public and as this part has built it? A loop. Fit a "
            "volatility surface, Part twelve, and refit it as quotes and trades arrive. <bookmark mark='a'/> Quote "
            "bids and offers in volatility around it, leaning against inventory, chapter nine. Keep every Greek, by "
            "expiry and by strike, inside limits. Hedge delta automatically in futures, and gamma and vega with other "
            "options, chapter ten. <bookmark mark='b'/> And every morning, explain yesterday term by term, chapter "
            "one, and chase anything unexplained. <bookmark mark='c'/> Around the loop, the venue's rules shape the "
            "trade: how expiries settle, what margins and position limits apply, and which indices the exchange "
            "publishes."
        ) as vo:
            self.play(FadeIn(boxes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a_), FadeIn(b_)) for a_, b_ in zip(arrows[:3], boxes[1:4])],
                                  lag_ratio=0.5, run_time=3))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[3]), FadeIn(boxes[4]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(v_) for v_ in venue], lag_ratio=0.3, run_time=2))
        self.wait(0.4)
        self.clear_scene()
