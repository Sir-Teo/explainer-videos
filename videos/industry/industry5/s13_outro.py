from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        lines = VGroup(
            tx("The moat", 40, GOLD, bold=True),
            tx("Some industries earn far more than their capital costs, and the gap fades only slowly.", 23),
            tx("The industry explains about a fifth of the differences in profit; the company more.", 23),
            tx("Few firms earn high returns only if newcomers are kept out and the few do not fight.", 23),
            tx("The walls are cost, habit, networks and law; five forces can drain what they protect.", 23),
            tx("And no wall survives the day customers stop wanting what is inside.", 23),
        ).arrange(DOWN, buff=0.32).move_to(UP * 0.5)
        with self.voiceover(
            "The moat. Some industries earn far more than their capital costs, and the gap fades only slowly. The "
            "industry a business is in explains about a fifth of the differences in profit; the business itself "
            "explains more. A few firms earn high returns only if newcomers are kept out and the few do not fight. "
            "The walls are made of cost, habit, networks and law, and five forces can drain what they protect. And "
            "no wall survives the day customers stop wanting what is inside it. When you look at an industry, ask "
            "what its castles are made of, who could walk round the walls, and what the customers would do if "
            "they could leave."
        ):
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in lines], lag_ratio=0.6), run_time=6)
        self.clear_scene()
        nxt = VGroup(tx("Next: Part 6", 26, GREY_B), tx("The Cycle", 64, WHITE, bold=True),
                     tx("Why do industries keep building too much at the top?", 26, GREY_A, italic=True)).arrange(
            DOWN, buff=0.3)
        with self.voiceover(
            "Which leads to the next question. When the castle is full of treasure, everyone builds, and the new "
            "plants arrive just as the boom ends. Part six: the cycle."
        ):
            self.play(FadeIn(nxt[0]), FadeIn(nxt[1], scale=1.1), run_time=1.5)
            self.play(FadeIn(nxt[2], shift=UP * 0.1))
        self.wait(1.0)
        self.clear_scene()
