from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, FORMULA, GOOD, HURDLE, PART


class China(VoiceoverScene):
    def construct(self):
        self.card()
        self.enhancement()
        self.february()
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
