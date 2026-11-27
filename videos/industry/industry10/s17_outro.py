from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        head = tx("Farming and food", 40, GOLD, bold=True).to_edge(UP, buff=0.45)
        fld = draw.field(3.6, 3, 7, "dwarf", 0.7).move_to([-5.0, -0.6, 0])
        lines = VGroup(
            tx("Farmers sell a commodity into a market of millions, so each one takes the price.", 21),
            tx("New methods raise output; the price falls; the gain passes to everyone who eats.", 21),
            tx("They buy from a few and sell to a few; the money is kept where things are hard to copy.", 21),
            tx("Traders live on spreads; packers on the number of animals; brands on loyalty.", 21),
            tx("Governments pay farmers in bad years and stop exports when food gets dear.", 21),
            tx("And the land, the one thing that cannot be made, keeps the good years.", 21, LAND)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2)
        lines.scale_to_fit_width(min(lines.width, 9.4)).move_to([1.85, -0.4, 0])
        with self.voiceover(
            "Farming and food. <bookmark mark='a'/> A farmer sells a commodity into a market of millions, so each one "
            "takes the price. <bookmark mark='b'/> Every new method raises output, the price falls, and the gain passes "
            "to everyone who eats. <bookmark mark='c'/> Farmers buy from a few companies and sell to a few, and the "
            "money is kept where something is hard to copy: a patent, a plant, a brand. <bookmark mark='d'/> Traders "
            "live on spreads, packers on the number of animals, brands on loyalty. <bookmark mark='e'/> Governments pay "
            "farmers in bad years and stop exports when food gets dear. <bookmark mark='f'/> And the land, the one thing "
            "that cannot be made, keeps the good years. That is why farmers grow ever more and keep so little of what "
            "we pay. And it is why, against every prophecy, the world is fed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fld))
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(lines[k]), run_time=1.2)
        self.clear_scene()
        nxt = VGroup(tx("Next: Part 11", 26, GREY_B), tx(PARTS[11], 60, WHITE, bold=True)).arrange(DOWN, buff=0.3)
        pics = VGroup(draw.factory(1.6), draw.crane(1.3), draw.truck(1.6, color=GREY_B)).arrange(RIGHT, buff=0.8).next_to(
            nxt, DOWN, buff=0.6)
        VGroup(nxt, pics).move_to(ORIGIN)
        with self.voiceover(
            "Food is grown. Most of what the modern world is built from is made in furnaces and kilns. The next part "
            "follows the heavy materials, steel and cement above all, where the cost is mostly energy and the plants "
            "last for half a century, and asks why the things everything is made of earn so little."
        ):
            self.play(FadeIn(nxt[0]), FadeIn(nxt[1], scale=1.1), run_time=1.4)
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in pics], lag_ratio=0.3), run_time=1.6)
        self.wait(1.0)
        self.clear_scene()
