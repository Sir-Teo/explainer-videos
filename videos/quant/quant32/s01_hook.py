from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, PART, SIXTY_C, SPY_C, TREND_C, era_strip, load


class Hook(VoiceoverScene):
    def construct(self):
        t = load("trend")
        self.title_card()
        self.crisis(t)
        self.questions()
        self.premium()
        self.act()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Systematic Macro and Alternative Premia")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-two. Systematic macro and alternative premia: the books that trade whole asset classes by rule, "
            "and the premia that are paid for holding risks other people want to shed."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def crisis(self, t):
        y = t["y2008"]
        rows = VGroup()
        for nm, v, col in ((r"US stocks (SPY)", y["spy"], SPY_C), (r"60/40 stocks and Treasuries", y["6040"], SIXTY_C),
                           (r"the House's trend book", y["trend"], TREND_C),
                           (r"AQR's published trend series", t["aqr"]["y2008"], TREND_C)):
            bar = Rectangle(width=abs(v) * 12, height=0.5, fill_color=col, fill_opacity=0.85, stroke_width=0)
            rows.add(VGroup(label(nm, font_size=22, color=col), bar, MathTex(rf"{100 * v:+.1f}\%", font_size=28)))
        for j, r_ in enumerate(rows):
            v = [y["spy"], y["6040"], y["trend"], t["aqr"]["y2008"]][j]
            r_[0].move_to([-4.3, 1.6 - 1.0 * j, 0])
            r_[1].move_to([0.6, 1.6 - 1.0 * j, 0], aligned_edge=LEFT if v > 0 else RIGHT)
            r_[2].next_to(r_[1], RIGHT if v > 0 else LEFT, buff=0.2)
        axis = Line([0.6, 2.2, 0], [0.6, -2.0, 0], color=GREY_C, stroke_width=1.5)
        head = label(r"2008, the calendar year", font_size=32).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"returns in excess of Treasury bills; the trend book: 23 ETFs across five asset classes, "
                             r"long or short each on the sign of its past year, built in Chapter 1", 11.4, 17,
                             GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "2008. <bookmark mark='a'/> American stocks lost "
            f"{abs(100 * y['spy']):.0f} percent over Treasury bills. A balanced portfolio of sixty percent stocks and "
            f"forty percent Treasuries lost {abs(100 * y['6040']):.0f}. <bookmark mark='b'/> A rule that simply follows "
            f"each market's trend, long or short, across twenty-three funds, made {100 * y['trend']:.1f} percent. AQR's "
            f"published trend series, across many more futures markets, made {100 * t['aqr']['y2008']:.0f}. "
            "<bookmark mark='c'/> The industry calls it crisis alpha. This part asks whether it is real, why it happens, "
            "and what it costs the rest of the time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[:2]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[2:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def questions(self):
        cards = VGroup(
            desk_question(r"trend following", r"why does a rule with no view of value make money in crashes, and lose it "
                          r"slowly in between?", width=12.4, font_size=20),
            desk_question(r"risk parity", r"why does holding bonds with leverage beat holding stocks without it, and what "
                          r"happens when stocks and bonds fall together?", width=12.4, font_size=20),
            desk_question(r"the premia", r"value, carry, momentum, defensive, selling insurance: who pays them, and "
                          r"would they pay them again?", width=12.4, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Three questions run through the part. <bookmark mark='a'/> Why does a rule with no view of value make money "
            "in crashes, and give it back slowly in between? <bookmark mark='b'/> Why does a portfolio of levered bonds "
            "beat a portfolio of stocks, and what happens when stocks and bonds fall together? <bookmark mark='c'/> And "
            "the alternative premia: who pays them, and why should they keep paying?"
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


    def premium(self):
        cards = VGroup(
            desk_question(r"a risk premium", r"paid for bearing a risk that hurts in bad times: carry and selling "
                          r"insurance lose exactly when investors can least afford it", width=12.4, font_size=19),
            desk_question(r"a behavioural premium", r"paid by investors who under-react, over-extrapolate or chase "
                          r"lotteries: momentum and value have both a risk story and a behavioural one", width=12.4,
                          font_size=19),
            desk_question(r"a structural premium", r"paid by participants who must trade regardless of price: hedgers in "
                          r"commodity futures, index funds on rebalancing days, pension funds at month end", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"What makes a premium alternative?", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "What makes a premium alternative? It is a return earned by a rule, not by owning the market, and it has to "
            "come from somewhere. <bookmark mark='a'/> A risk premium is paid for bearing a risk that hurts in bad times. "
            "<bookmark mark='b'/> A behavioural premium is paid by investors who under-react or over-extrapolate. "
            "<bookmark mark='c'/> A structural premium is paid by participants who must trade whatever the price: "
            "hedgers, index funds, pension funds. Each premium in this part will be asked which of the three it is, "
            "because that decides whether it should survive."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits. Parts thirty and thirty-one built the portfolio and its risk model on single securities. "
            "This part moves up a level, to whole asset classes: equity indices, government bonds, credit, commodities "
            "and currencies, traded through futures and funds. The ideas of Part twenty-four's factor zoo reappear here "
            "as macro books, each with its own crisis."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        entries = [(1949, r"Donchian's channels", I), (1983, r"the Turtles", I),
                   (1987, r"AHL founded", I), (1996, r"All Weather", I), (1997, r"Winton founded", I),
                   (2001, r"Fung--Hsieh: lookback straddles", I), (2008, r"crisis alpha", I),
                   (2012, r"time-series momentum", I), (2017, r"a century of trend; vol-managed", I),
                   (2018, r"carry everywhere", I), (2022, r"stocks and bonds fall together", I)]
        strip = era_strip(entries, y0=1945, y1=2027, font_size=12, step=10).move_to(DOWN * 0.3)
        head = label(r"Seventy years of trading whole markets", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 3), (3, 7), (7, 11)]
        with self.voiceover(
            "Richard Donchian ran a public trend-following fund in 1949, buying breakouts above recent highs; Richard "
            "Dennis trained his Turtles in 1983; and Michael Adam, David Harding and Martin Lueck founded AHL in 1987. "
            "<bookmark mark='a'/> Bridgewater launched All Weather in 1996 for Ray Dalio's own trust, Harding founded "
            "Winton in 1997, and William Fung and David Hsieh showed in 2001 that trend followers' returns look like "
            "lookback straddles. <bookmark mark='b'/> Then 2008 made crisis alpha a sales line; academics named "
            "time-series momentum in 2012, traced it back to 1880, found carry in every asset class, and in 2022 watched "
            "stocks and bonds fall together."
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
            r"Trend following: time-series momentum built on 23 ETFs, and a century of evidence",
            r"The smile: why trend makes money in crises",
            r"Volatility targeting, asset by asset",
            r"Risk parity, its leverage, and the stock--bond correlation since 1962",
            r"Value, momentum, carry and defensive across asset classes, 1926--2020; carry made visible",
            r"Selling insurance; calendars, nights and events",
            r"For the researcher: the trend rule is long a straddle, exactly",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: trend following, built and measured; the smile, and why trend pays in crises; volatility "
            "targeting across assets; risk parity, its leverage, and sixty years of the stock-bond correlation; the four "
            "alternative premia everywhere for a century; carry, measured in the House's own funds, and the day oil went "
            "negative; selling insurance; calendar effects and the night; two books "
            "opened on sealed years; and an exact identity that says why trend following is long a straddle."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("macro", "portfolio"))
        with self.voiceover(
            "In the House, the macro desk, built in Part twenty-two for the curve and the basis, gets its systematic "
            "books, and the portfolio desk learns to hold them together."
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()
