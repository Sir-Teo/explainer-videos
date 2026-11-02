from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import PART, load


class House(VoiceoverScene):
    def construct(self):
        m = load("margin")
        self.card()
        self.desk(m)

    def card(self):
        c = chapter_card(10, r"The funding desk", r"What does it cost to hold a position?", part=PART)
        with self.voiceover("Chapter ten. The funding desk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def desk(self, m):
        chart = house_chart(PART, lit=("treasury",)).scale(0.72).to_edge(UP, buff=0.25)
        items = VGroup(
            label(r"margin accounts: variation margin, funding, and the exchange's liquidation rule (chapter 4)", font_size=22),
            label(r"financing: cash borrowed at SOFR plus a spread; short positions pay a borrow fee", font_size=22),
            label(r"clearing: netting and the call-auction price (chapters 2, 3)", font_size=22),
            label(r"fees: management and performance fees with a high-water mark (chapter 8)", font_size=22),
            label(r"haircuts: the leverage each kind of collateral allows (chapter 6)", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(chart, DOWN, buff=0.4)
        if items.width > 13.0:
            items.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 3: every backtest pays for its funding, its margin and its fees, and is closed out "
                             r"when the exchange would close it out.", 12.0, 24, QC.HOUSE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The House's second desk, treasury and funding, is now built and tested. It keeps the margin account of "
            "every leveraged position, with variation margin, funding payments and the exchange's liquidation rule; "
            "the code that liquidated our three traders in chapter four. <bookmark mark='a'/> It charges cash "
            "borrowed at SOFR plus a spread, and borrow fees on shorts. It nets trades and computes auction prices. "
            "It charges fees with a high-water mark, and it knows the leverage each kind of collateral allows. "
            "<bookmark mark='b'/> And it adds the House's third rule: every backtest pays for its funding, its margin "
            "and its fees, and is closed out when the exchange would have closed it out. A strategy that only works "
            "with free leverage doesn't work."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["treasury"], color=QC.HOUSE, scale_factor=1.05))
            self.play(LaggedStart(*[FadeIn(i) for i in items[:1]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(i) for i in items[1:]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
