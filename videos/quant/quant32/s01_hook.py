from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, PART, SIXTY_C, SPY_C, TREND_C, era_strip


from videos.quant.quant32.illustrations import trend_paths


class Hook(VoiceoverScene):
    def construct(self):
        t = trend_paths()
        self.title_card()
        self.crisis(t)
        self.questions()
        self.premium()
        self.act()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Systematic Macro and Alternative Premia").scale(0.58).to_edge(UP, buff=0.3)
        example = MathTex(r"r=(1,1,1,1),\quad x=(0,1,2,3),\quad P=6", font_size=36).shift(UP * 0.25)
        rule = MathTex(r"x_t=\sum_{s<t}r_s,\qquad P=\frac{S^2-Q}{2}", font_size=35).shift(DOWN * 1.0)
        scope = wrapped_label(r"chosen increments; squared-increment profit, without capital normalisation or costs",
                              12.2, 20, GREY_A).shift(DOWN * 2.1)
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        self.add(card, example, rule, scope, disc)
        with self.voiceover(
            "Part thirty-two. Systematic macro and alternative premia: the books that trade whole asset classes by rule, "
            "and the premia that are paid for holding risks other people want to shed."
        ):
            self.play(Indicate(example, color=TREND_C, scale_factor=1.02))
        self.play(FadeOut(card), FadeOut(example), FadeOut(rule), FadeOut(scope), FadeOut(disc))

    def crisis(self, t):
        up, chop = t["persistent rise"], t["alternating"]
        head = label(r"A chosen four-increment example", font_size=32).to_edge(UP, buff=0.55)
        rows = VGroup(
            VGroup(label(r"persistent rise", font_size=23, color=TREND_C),
                   MathTex(rf"r=(1,1,1,1):\quad S={up['S']:.0f},\ Q={up['Q']:.0f},\ P={up['P']:.0f}", font_size=32)),
            VGroup(label(r"alternating", font_size=23, color=BAD),
                   MathTex(rf"r=(1,-1,1,-1):\quad S={chop['S']:.0f},\ Q={chop['Q']:.0f},\ P={chop['P']:.0f}", font_size=32)),
        )
        for row in rows:
            row.arrange(RIGHT, buff=0.5)
        rows.arrange(DOWN, buff=0.65).move_to(UP * 0.25)
        equation = MathTex(r"x_t=\sum_{s<t}r_s,\qquad P=\sum_t x_t r_t=\frac{S^2-Q}{2}", font_size=34).move_to(DOWN * 2.0)
        foot = wrapped_label(r"fixed mathematical increments; PnL in squared increment units, without wealth normalisation "
                             r"or costs; no market observation or investment return", 12.2, 18, GREY_A).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Start with two chosen mathematical paths, not a market record. The position on each period equals the "
            "sum of earlier increments, so today's increment is never used to choose today's position. Four increments "
            f"of one give total S equal to {up['S']:.0f}, sum of squares Q equal to {up['Q']:.0f}, and profit P equal to "
            f"{up['P']:.0f}. The profit is in squared increment units, not a six percent investment return. "
            "<bookmark mark='a'/> Alternate one and minus one instead. "
            f"The total is {chop['S']:.0f}, the same sum of squares is {chop['Q']:.0f}, and profit is {chop['P']:.0f}. "
            "<bookmark mark='b'/> This linear rule's exact identity is half the squared total minus half the sum of "
            "squared increments. It helps explain a convex response to sustained moves and the losses from reversals. "
            "It does not prove that an implementable trend strategy earns a premium or protects every crisis. The "
            "literature's crisis-alpha description is an empirical claim about specified rules and episodes. Our task "
            "is to separate the algebra, that evidence, and the costs of holding a real book."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Write(equation))
        self.wait(0.4)
        self.clear_scene()


    def questions(self):
        cards = VGroup(
            desk_question(r"trend following", r"when can a rule based on past returns benefit from sustained moves, and lose from "
                          r"reversals?", width=12.4, font_size=20),
            desk_question(r"risk parity", r"how can capital weights hide concentrated risk, and what "
                          r"happens when stocks and bonds fall together?", width=12.4, font_size=20),
            desk_question(r"the premia", r"value, carry, momentum, defensive, selling insurance: who pays them, and "
                          r"would they pay them again?", width=12.4, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0], shift=UP * 0.2))
        with self.voiceover(
            "Three questions run through the part. <bookmark mark='a'/> When can a rule based on past returns benefit "
            "from sustained moves and lose from reversals? <bookmark mark='b'/> How can capital weights hide "
            "concentrated risk, and what happens when stocks and bonds fall together? <bookmark mark='c'/> And "
            "the alternative premia: who pays them, and why should they keep paying?"
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Indicate(cards[0], scale_factor=1.01) if k == 0
                          else FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


    def premium(self):
        cards = VGroup(
            desk_question(r"a risk premium", r"paid for bearing a risk that hurts in bad times: carry and selling "
                          r"insurance can lose when investors can least afford it", width=12.4, font_size=19),
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
        self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.2))
        with self.voiceover(
            "What makes a premium alternative? It is a return earned by a rule, not by owning the market, and it has to "
            "come from somewhere. <bookmark mark='a'/> A risk premium is paid for bearing a risk that hurts in bad times. "
            "<bookmark mark='b'/> A behavioural premium is paid by investors who under-react or over-extrapolate. "
            "<bookmark mark='c'/> A structural premium is paid by participants who must trade whatever the price: "
            "hedgers, index funds, pension funds. Each premium in this part will be asked which of the three it is, "
            "because plausible stories and repeatable evidence have different roles."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Indicate(cards[0], scale_factor=1.01) if k == 0
                          else FadeIn(cards[k], shift=UP * 0.2))
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
            r"Trend following: signal timing, chosen paths and the scope of published evidence",
            r"The smile: convexity, reversals and the limits of the straddle analogy",
            r"Volatility targeting, asset by asset",
            r"Risk parity, leverage, financing and chosen correlation scenarios",
            r"Published value, momentum, carry and defensive series; exact fixed carry arithmetic",
            r"Selling insurance; calendars, nights and events",
            r"For the researcher: the exact linear-rule PnL identity and Gaussian reference law",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: trend following, with timing and chosen arithmetic paths; convexity, reversals and the limits "
            "of crisis protection; volatility forecasts and exposure caps; risk budgets, leverage, financing and "
            "correlation scenarios; the published alternative-premia series and what their construction permits us to "
            "infer; carry with explicit currency and futures units; the put index and selling insurance; calendars, "
            "events and overnight arithmetic; an evaluation protocol with fixed macro-book calculations; and the "
            "linear trend identity, its stationary mean and its independent-Gaussian reference distribution."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("macro", "portfolio"))
        with self.voiceover(
            "In the House, the macro desk, built in Part twenty-two for the curve and the basis, gets its systematic "
            "book designs and measurement interfaces. The portfolio desk still needs appropriate data, costs and "
            "independent evidence before an allocation decision."
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()
