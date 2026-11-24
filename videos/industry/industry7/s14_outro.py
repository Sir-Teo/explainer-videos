from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        head = tx("Sizing a market", 40, GOLD, bold=True).to_edge(UP, buff=0.45)
        bottle = draw.bottle(2.6, color=WATER, water=0.2).move_to([-4.6, -0.4, 0])
        level = ValueTracker(0.2)
        bottle.add_updater(lambda b: b[0].stretch_to_fit_height(max(0.01, 2.6 * 0.7 * level.get_value()),
                                                                about_edge=DOWN))
        lines = VGroup(
            tx("First the definition: which level, plants, products, buyers, year.", 23),
            tx("Then two ways to count: top-down from the census,", 23),
            tx("bottom-up from units times a price you must choose.", 23, GREY_A),
            tx("Compare only on one definition; report a range.", 23),
            tx("An addressable market is a dream, not a forecast;", 23),
            tx("an S-curve's ceiling cannot be read from its first years.", 23, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).move_to([1.8, -0.3, 0])
        groups = [VGroup(lines[0]), VGroup(lines[1], lines[2]), VGroup(lines[3]), VGroup(lines[4], lines[5])]
        with self.voiceover(
            "Sizing a market. <bookmark mark='a'/> Start with the definition: which level of the chain, which "
            "plants, which products, which buyers, which year. <bookmark mark='b'/> Then count it two ways: down from "
            "what the statistical offices count, and up from units times a price you have to choose. "
            "<bookmark mark='c'/> Compare estimates only once they share a definition, and report a range. "
            "<bookmark mark='d'/> Treat an addressable market as a company's dream, not a forecast, and never trust "
            "a ceiling read off the first few years of an S-curve. Do that, and the next time someone tells you a "
            "market is worth trillions, you will know the first question to ask: worth trillions of what?"
        ) as vo:
            self.add(bottle)
            self.play(FadeIn(head), FadeIn(bottle))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(groups[k]), level.animate.set_value(0.2 + 0.2 * (k + 1)), run_time=1.2)
        bottle.clear_updaters()
        self.clear_scene()
        nxt = VGroup(tx("Next: Act II, Out of the Ground", 26, GREY_B), tx("Oil and Gas", 64, WHITE, bold=True)).arrange(
            DOWN, buff=0.3).move_to(UP * 0.8)
        with self.voiceover(
            "That ends the first act of this series: how to read any industry, from its unit and its cost curve to "
            "its moat, its cycle and its size. The second act goes out of the ground, starting with the industry "
            "the modern economy runs on: oil and gas."
        ):
            self.play(FadeIn(nxt[0]), FadeIn(nxt[1], scale=1.1), run_time=1.6)
        self.wait(1.0)
        self.clear_scene()
