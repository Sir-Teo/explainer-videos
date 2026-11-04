from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, FORMULA, GOOD, HURDLE, PART


class China(VoiceoverScene):
    def construct(self):
        self.card()
        self.enhancement()
        self.february()
        self.lingjun()
        self.hedge()
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(10, r"China's quant industry", r"What happens when many miners crowd into the same trade?",
                         part=PART)
        with self.voiceover("Chapter ten. Alpha mining at industrial scale has its largest laboratory in China. What "
                            "happens when many miners, using similar methods on similar data, crowd into the same trade?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def enhancement(self):
        rows = [cmath(r"r_{\text{fund}}", r"=", r"r_{\text{CSI 500 or 1000}} + \alpha", font_size=34,
                      colors={r"r_{\text{fund}}": FORMULA}),
                cmath(r"\text{market neutral}", r":", r"\text{long the stocks, short index futures}: \ r = \alpha", font_size=30),
                cmath(r"\alpha", r"\leftarrow", r"\text{thousands of mined factors, combined daily}", font_size=30,
                      colors={r"\alpha": HURDLE})]
        whys = [why(r"index enhancement (指数增强): a fund benchmarked to an index of mid- or small-cap stocks, which aims "
                    r"to beat it by stock selection"),
                why(r"the hedged version sells index futures against the stocks and keeps only the excess return"),
                why(r"the excess return comes from factor libraries of the kind this part mines, rebalanced often; and "
                    r"much of it, in practice, from a tilt toward the smallest stocks")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The dominant product is index enhancement. <bookmark mark='a'/> A fund benchmarked to an index of mid-sized "
            "or small Chinese stocks, the CSI 500 or the CSI 1000, that tries to beat it by stock selection. "
            "<bookmark mark='b'/> A hedged version sells index futures against the stocks and keeps only the excess "
            "return. <bookmark mark='c'/> That excess return comes from large libraries of mined factors, combined and "
            "rebalanced daily, and much of it, in practice, from leaning toward the smallest stocks. Between 2019 and 2023 "
            "these private quant funds grew into one of the largest pools of systematic money in the world."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def february(self):
        card = crisis_card(r"February 2024", r"China's quant quake",
                           body=r"a crowded tilt to small caps, hedged with index futures, met a falling small-cap market; "
                                r"leveraged swaps sold into the fall",
                           stats=((r"-31\%", r"an index of China's smallest listed companies, in the first five trading days "
                                            r"of February, as reported"),
                                  (r"\text{DMA}", r"direct-market-access swaps, leveraged quant products, amplified the "
                                                  r"selling, as reported"),
                                  (r"20\ \text{Feb}", r"the exchanges froze a major quant fund's accounts for three days"),
                                  (r"-14\%", r"quant funds tracking the CSI 1000, first half of 2024, as reported")),
                           width=10.6, font_size=21).move_to(ORIGIN)
        with self.voiceover(
            "Then came February 2024. <bookmark mark='a'/> Many funds held the same tilt toward small stocks, hedged "
            "with futures on larger indices. When small caps fell, the hedge did not cover the loss, and as reported by "
            "Bloomberg and Reuters, an index of the smallest listed companies fell thirty-one percent in the first five "
            "trading days of the month. <bookmark mark='b'/> Leveraged swap products, known as DMA, sold into the fall. "
            "On the twentieth of February the exchanges froze a large quant fund's trading accounts for three days, and "
            "the regulator tightened its supervision of these swaps and of high-frequency trading. Quant funds tracking "
            "the CSI 1000 were reported down about fourteen percent in the first half of the year."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card, color=QC.CRISIS, scale_factor=1.01))
        self.wait(0.4)
        self.clear_scene()

    def lingjun(self):
        card = firm_card(r"Ningbo Lingjun Investment (宁波灵均)", r"a quantitative fund manager; at the open on Monday 19 "
                         r"February 2024 it sold about 2.57 billion yuan of A-shares within one minute, as the exchanges "
                         r"reported. The Shanghai and Shenzhen exchanges barred it from trading from 20 to 22 February",
                         numbers=((r"2.57\ \text{bn}", r"yuan of shares sold between 9:30 and 9:31, as reported"),
                                  (r"60\ \text{bn}+", r"yuan managed, by the firm's own account; it apologised, saying its "
                                                       r"models had been hit by abnormal short-term market conditions")),
                         source=r"exchange notices; Bloomberg, Reuters and SCMP, 20--21 February 2024", kind=r"Public record",
                         width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "The fund whose accounts were frozen is a matter of public record. <bookmark mark='a'/> At the open on the "
            "nineteenth of February, Ningbo Lingjun Investment sold about two and a half billion yuan of shares within "
            "a single minute, as the exchanges reported, and both exchanges barred it from trading for the next three "
            "days. <bookmark mark='b'/> The firm apologised, saying its models had been hit by abnormal short-term "
            "market conditions. The episode shows the other side of automation: a model's sell order, executed at "
            "machine speed into a falling market, became a regulatory event."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def hedge(self):
        rows = [cmath(r"r_{\text{book}}", r"=", r"r_{\text{long}} - \beta\, r_{\text{future}}", font_size=34,
                      colors={r"r_{\text{book}}": FORMULA}),
                cmath(r"r_{\text{long}}", r"=", r"\beta\,r_{\text{index}} + \underbrace{(r_{\text{small}} - r_{\text{index}})}"
                      r"_{\text{the size spread}} + \alpha", font_size=30),
                cmath(r"r_{\text{book}}", r"\approx", r"\alpha + (r_{\text{small}} - r_{\text{index}}) - \text{basis change}",
                      font_size=30, colors={r"r_{\text{book}}": BAD}),
                cmath(r"\text{loss}", r"=", r"L \times \big|r_{\text{small}} - r_{\text{index}}\big|", font_size=32,
                      colors={r"\text{loss}": BAD})]
        whys = [why(r"a long book of stocks, short index futures in proportion to its beta"),
                why(r"a book tilted toward smaller stocks than the index carries the size spread on top of its stock picks"),
                why(r"the hedge removes the index, not the spread; and futures can trade at a discount that moves too"),
                why(r"with leverage $L$, the spread's fall is multiplied, and margin calls turn it into forced selling")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "The arithmetic of the hedge. <bookmark mark='a'/> A book is long stocks and short index futures in "
            "proportion to its beta. <bookmark mark='b'/> If its stocks are smaller than the index's, the long side "
            "carries the spread between small and large stocks, on top of whatever the stock picks add. "
            "<bookmark mark='c'/> The hedge removes the index's move but not that spread, and the futures' own discount to "
            "the index can move against you as well. <bookmark mark='d'/> Add leverage and the spread's fall is "
            "multiplied; margin calls then turn the loss into selling, and the selling into the next day's loss."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"the factors were not independent", r"mined libraries at different firms share data, operators "
                          r"and the small-cap tilt: their crashes are one crash", width=12.4, font_size=19),
            desk_question(r"the hedge had a basis", r"small caps against index futures is a bet on the spread between "
                          r"them, which widens exactly when everyone exits", width=12.4, font_size=19),
            desk_question(r"leverage turns a drawdown into forced selling", r"Part 21's margin spiral, in equities", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons for the miner. <bookmark mark='a'/> Factors mined at different firms are not independent: they "
            "share data, operators and the same tilt, so their crashes are one crash. <bookmark mark='b'/> A hedge with a "
            "basis is a bet on that basis, and the basis widens exactly when everyone leaves at once. "
            "<bookmark mark='c'/> And leverage turns a drawdown into forced selling: Part twenty-one's margin spiral, in "
            "equities."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a fund is long small caps and short CSI 300 futures. Small caps fall 20\%, the CSI 300 falls 5\%. "
                       r"What did the `market-neutral' fund lose, per unit of gross long?")
        with self.voiceover(
            "Pause and predict. A fund is long small caps and short futures on the large-cap index. Small caps fall twenty "
            "percent and the large-cap index five. What did the market-neutral fund lose?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
