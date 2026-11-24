from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        head = tx("Mining and metals", 40, GOLD, bold=True).to_edge(UP, buff=0.45)
        pit = draw.open_pit(4.6, 2.2, benches=6)
        pit.scale_to_fit_width(3.3).move_to([-5.3, -0.4, 0])
        lines = VGroup(
            tx("A mine is billions spent up front, repaid over decades", 22),
            tx("at prices nobody can know; waiting has value, so mines are built in booms.", 22, GREY_A),
            tx("Grade is destiny: halve it and you double the rock.", 22),
            tx("Every miner takes the exchange's price; only its cost is its own.", 22),
            tx("The state owns the minerals, takes its share, and sometimes the market.", 22),
            tx("A critical mineral is critical to its buyers; to its sellers it is a cycle.", 22),
            tx("Over a century, the price swings around a level that barely moves.", 22)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.17)
        lines.scale_to_fit_width(min(lines.width, 9.2)).move_to([1.85, -0.4, 0])
        groups = [VGroup(lines[0], lines[1]), VGroup(lines[2]), VGroup(lines[3]), VGroup(lines[4]), VGroup(lines[5]),
                  VGroup(lines[6])]
        with self.voiceover(
            "Mining and metals. <bookmark mark='a'/> A mine is billions of dollars spent up front and repaid over "
            "decades, at prices nobody can know, and because waiting has value, mines get built in booms. "
            "<bookmark mark='b'/> Grade is destiny: halve the copper in the ore, and you double the rock you must move. "
            "<bookmark mark='c'/> Every miner takes the exchange's price; the only thing it controls is its cost. "
            "<bookmark mark='d'/> The state owns the minerals, takes its share, and sometimes takes the market. "
            "<bookmark mark='e'/> A critical mineral is critical to its buyers; to its sellers it is still a cycle. "
            "<bookmark mark='f'/> And over a century, the price of metal swings in long waves around a level that "
            "barely moves, because every boom pays for the mines and the ideas that end it. Six holes in the Atacama "
            "were a wager on that wave. The sixth paid for everything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pit))
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(groups[k]), run_time=1.2)
        self.clear_scene()
        nxt = VGroup(tx("Next: Part 10", 26, GREY_B), tx(PARTS[10], 60, WHITE, bold=True)).arrange(DOWN, buff=0.3)
        pics = VGroup(draw.factory(1.4), draw.truck(1.6, color=LITH), draw.ship(2.0, boxes=6)).arrange(
            RIGHT, buff=0.8).next_to(nxt, DOWN, buff=0.6)
        VGroup(nxt, pics).move_to(ORIGIN)
        with self.voiceover(
            "Metal comes out of the rock once. Food comes out of the soil every year. The next part follows a bushel "
            "of wheat from the field to a loaf of bread, and asks why farmers take whatever price they are given, and "
            "who along the chain does not."
        ):
            self.play(FadeIn(nxt[0]), FadeIn(nxt[1], scale=1.1), run_time=1.4)
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in pics], lag_ratio=0.3), run_time=1.6)
        self.wait(1.0)
        self.clear_scene()
