from __future__ import annotations

from videos.industry.industry4.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        lines = VGroup(
            tx("What one more costs", 40, PRICE, bold=True),
            tx("Decide on the cost of one more, not the average; sunk costs never count.", 24),
            tx("Fixed costs make a business hungry to run full, and amplify its good and bad years.", 24),
            tx("Size, scope, density and experience push each unit's cost down.", 24),
            tx("In a market, the last unit needed sets the price, and everyone below it keeps the gap.", 24),
            tx("Where fixed costs are huge and products alike, firms fight to the death, or find a way out.", 24),
        ).arrange(DOWN, buff=0.32).move_to(UP * 0.5)
        with self.voiceover(
            "What one more costs. A decision should weigh the cost of one more, not the average, and costs already "
            "sunk never count. Fixed costs make a business hungry to run full, and they amplify its good years and "
            "its bad ones. Size, scope, density and experience all push the cost of each unit down, and experience "
            "keeps pushing for as long as an industry keeps growing. In a market, the last unit needed sets the "
            "price, and everyone with lower costs keeps the gap. And where fixed costs are huge and products are "
            "alike, firms fight to the death, unless they find a way out."
        ):
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in lines], lag_ratio=0.6), run_time=6)
        self.clear_scene()
        nxt = VGroup(tx("Next: Part 5", 26, GREY_B), tx("The Moat", 64, WHITE, bold=True),
                     tx("Why do some industries earn high returns for decades while others never do?", 26, GREY_A,
                        italic=True)).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Which raises the next question. If costs fall for everyone who builds, and prices fall to the cost of "
            "one more, how does anyone earn more than the cost of their capital for long? Some industries do, for "
            "decades. Part five: the moat."
        ):
            self.play(FadeIn(nxt[0]), FadeIn(nxt[1], scale=1.1), run_time=1.5)
            self.play(FadeIn(nxt[2], shift=UP * 0.1))
        self.wait(1.0)
        self.clear_scene()
