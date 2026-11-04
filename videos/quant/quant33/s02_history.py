from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant33.common import BAD, GOOD, HURDLE, PART, RES_C, SPREAD_C


class History(VoiceoverScene):
    def construct(self):
        self.card()
        self.thorp()
        self.morgan()
        self.shaw()
        self.renaissance()
        self.pdt()
        self.what_changed()
        self.question()

    def card(self):
        c = chapter_card(1, r"From Morgan Stanley's back office to the quant firms", r"Where did statistical arbitrage "
                         r"come from?", part=PART)
        with self.voiceover("Chapter one. Statistical arbitrage was not invented in a university. It grew out of trading "
                            "desks that had more computing power than ideas about what to do with it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def thorp(self):
        card = firm_card(r"Princeton/Newport Partners", r"founded in 1969 by Edward Thorp and Jay Regan to run hedged "
                         r"strategies: convertible bonds and warrants against the stock, priced with a model of what the "
                         r"option inside was worth; one of the first funds to make market-neutral, model-driven "
                         r"arbitrage a business", source=r"Thorp's own accounts; press reports", kind=r"Firm file",
                         width=10.6, font_size=22).move_to(UP * 0.2)
        with self.voiceover(
            "The first firm file is older than the name. Edward Thorp, who had beaten blackjack with probability, and "
            "Jay Regan founded Princeton/Newport Partners in 1969. They bought convertible bonds and warrants that a "
            "model said were cheap, and sold the stock against them, so the market's direction hardly mattered. Thorp's "
            "model of the option inside was, as he later wrote, close to Black and Scholes's, before theirs was published: Part ten's "
            "formula, used as a trading tool."
        ):
            self.play(FadeIn(card))
            self.wait(1.0)
        self.clear_scene()

    def morgan(self):
        card = firm_card(r"Morgan Stanley's quantitative group", r"in the mid-1980s Gerry Bamberger, and then a group led "
                         r"by Nunzio Tartaglia, traded pairs of stocks whose prices had diverged, by computer and in "
                         r"size; the group reportedly earned about \$50 million in 1987 and was disbanded in 1989 after "
                         r"weaker years", numbers=((r"\$50\ \text{m}", r"reported profit, 1987"),
                                                   (r"1989", r"the group disbanded, as reported")),
                         source=r"Gatev, Goetzmann and Rouwenhorst (2006); interviews and press accounts",
                         kind=r"Firm file", width=10.6, font_size=22).move_to(UP * 0.2)
        with self.voiceover(
            "The name came from Morgan Stanley. In the mid-1980s Gerry Bamberger, and then a group led by Nunzio "
            "Tartaglia, used computers to find pairs of stocks whose prices had drifted apart, and bet on their "
            "reunion, in size. As reported, the group earned about fifty million dollars in 1987, and it was disbanded "
            "in 1989 after weaker years. Its alumni spread the idea across Wall Street."
        ):
            self.play(FadeIn(card))
            self.wait(1.0)
        self.clear_scene()

    def shaw(self):
        card = firm_card(r"D. E. Shaw", r"founded in 1988 by David Shaw, a computer scientist who had worked in Morgan "
                         r"Stanley's quantitative trading; it began with computerised statistical arbitrage in equities "
                         r"and grew into one of the largest systematic investment firms", source=r"company history; press "
                                                                                                r"reports",
                         kind=r"Firm file", width=10.6, font_size=22).move_to(UP * 0.2)
        with self.voiceover(
            "One of those alumni was David Shaw, a computer scientist from Columbia, who founded his firm in 1988. It "
            "began with computerised statistical arbitrage in equities, many small mean-reversion bets hedged against "
            "the market and industries, and grew into one of the largest systematic investment firms. The design was "
            "the one this part builds: a factor model to remove what is common, and a bet that what is left reverts."
        ):
            self.play(FadeIn(card))
            self.wait(1.0)
        self.clear_scene()

    def renaissance(self):
        card = firm_card(r"Renaissance Technologies", r"founded by the mathematician James Simons; its Medallion fund, "
                         r"started in 1988, became famous for returns far above any other fund's, as reported, while "
                         r"saying almost nothing in public about how; it later returned outside investors' money and runs "
                         r"for its employees", source=r"press reports; Zuckerman, \textit{The Man Who Solved the Market} "
                                                       r"(2019)",
                         kind=r"Firm file", width=10.6, font_size=22).move_to(UP * 0.2)
        with self.voiceover(
            "And Renaissance Technologies, founded by the mathematician James Simons. Its Medallion fund, started in "
            "1988, became famous for returns far above any other fund's, as reported, while its methods stayed private. "
            "It later returned outside investors' money, and runs mostly for its own employees: the profit-maximising "
            "size of Part thirty-one, chosen by a firm that owns its strategy."
        ):
            self.play(FadeIn(card))
            self.wait(1.0)
        self.clear_scene()

    def pdt(self):
        card = firm_card(r"Process Driven Trading", r"started inside Morgan Stanley in 1993 by Peter Muller, as reported; "
                         r"a proprietary quantitative group that ran statistical arbitrage among other strategies for the "
                         r"bank's own capital, and was spun out as an independent firm in 2012", kind=r"Firm", width=10.6,
                         font_size=22).move_to(UP * 0.4)
        foot = wrapped_label(r"the public record only: firm histories as reported in the press and in the firms' own "
                             r"statements; nothing here is an allegation or a performance claim", 11.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Morgan Stanley tried again. <bookmark mark='a'/> In 1993 Peter Muller started a quantitative group inside the "
            "bank, Process Driven Trading, which, as reported, ran statistical arbitrage among other strategies with the "
            "bank's own capital, and was spun out as an independent firm in 2012, after new rules limited banks' "
            "proprietary trading. The pattern repeats through this history: the methods start inside a bank and end up in "
            "independent firms."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def what_changed(self):
        cards = VGroup(
            desk_question(r"then", r"a few desks with computers, wide spreads, slow competitors: pairs held for weeks "
                          r"earned double digits", width=12.4, font_size=19),
            desk_question(r"later", r"decimal prices, electronic markets and many firms with the same models: holding "
                          r"periods shrank to days and hours, and the edge per trade with them", width=12.4, font_size=19),
            desk_question(r"now", r"the return is largely pay for providing liquidity, and it is earned by whoever "
                          r"trades most cheaply: Part 37's execution decides it", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What changed. <bookmark mark='a'/> In the beginning, a few desks had computers, spreads were wide and "
            "competitors were slow: pairs held for weeks earned large returns. <bookmark mark='b'/> Then prices went "
            "decimal, markets went electronic, and many firms ran the same models: holding periods shrank to days and "
            "hours, and the edge per trade shrank with them. <bookmark mark='c'/> Today the return is mostly pay for "
            "providing liquidity, and it goes to whoever trades most cheaply."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a strategy's edge is 3 bp per trade and it trades each position daily. What happens to it when "
                       r"spreads fall from 10 bp to 2 bp, and why might it still get worse?")
        with self.voiceover(
            "Pause and predict. A strategy's edge is three basis points a trade, and it trades every position daily. "
            "What happens when spreads fall from ten basis points to two, and why might it still get worse?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
