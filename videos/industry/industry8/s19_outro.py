from __future__ import annotations

from videos.industry.industry8.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        head = tx("Oil and gas", 40, GOLD, bold=True).to_edge(UP, buff=0.45)
        brl = draw.barrel(2.6, color="#2F6FA8").move_to([-4.8, -0.6, 0])
        lvl = ValueTracker(0.0)
        fill = always_redraw(lambda: Rectangle(width=brl.width * 0.92, height=max(2.5 * lvl.get_value(), 0.001),
                                               stroke_width=0, fill_color=CRUDE, fill_opacity=0.85).move_to(
            brl.get_bottom() + UP * (0.05 + 1.25 * lvl.get_value())))
        lines = VGroup(
            tx("A barrel costs a few dollars in Saudi Arabia and sixty-odd in Texas;", 22),
            tx("the last barrel the world needs sets the price.", 22, GREY_A),
            tx("Wells fade; shale wells fast, so shale must keep drilling.", 22),
            tx("Reserves are a forecast at a price.", 22),
            tx("The owner of the rock, usually a state, keeps most of the difference.", 22),
            tx("Neither side can move fast, so small shortages make huge swings;", 22),
            tx("cartels, wars and shale drillers fight over the swing.", 22, GREY_A),
            tx("Refiners live on spreads, service companies on others' spending.", 22)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to([1.6, -0.4, 0])
        groups = [VGroup(lines[0], lines[1]), VGroup(lines[2]), VGroup(lines[3]), VGroup(lines[4]), VGroup(lines[5], lines[6]),
                  VGroup(lines[7])]
        with self.voiceover(
            "Oil and gas. <bookmark mark='a'/> A barrel costs a few dollars to lift in Saudi Arabia and sixty-odd to "
            "drill anew in Texas, and the last barrel the world needs sets the price. <bookmark mark='b'/> Every well "
            "fades, shale wells fastest, so shale must keep drilling. <bookmark mark='c'/> Reserves are a forecast at "
            "a price. <bookmark mark='d'/> The owner of the rock, usually a state, keeps most of the difference. "
            "<bookmark mark='e'/> Neither buyers nor sellers can move fast, so small shortages make huge price swings, "
            "and cartels, wars and shale drillers fight over the swing. <bookmark mark='f'/> Between the well and the "
            "pump, refiners live on a spread and service companies on everyone else's spending. And the price of a "
            "barrel, from minus thirty-seven dollars to a hundred and twenty-four, is the sum of all of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(brl))
            self.add(fill)
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(groups[k]), lvl.animate.set_value((k + 1) / 6), run_time=1.2)
        fill.clear_updaters()
        self.clear_scene()
        nxt = VGroup(tx("Next: Part 9", 26, GREY_B), tx("Mining and Metals", 60, WHITE, bold=True)).arrange(DOWN, buff=0.3)
        pics = VGroup(draw.truck(1.6, color="#F2C14E"), draw.crane(1.4), draw.factory(1.6)).arrange(RIGHT, buff=0.8).next_to(
            nxt, DOWN, buff=0.6)
        VGroup(nxt, pics).move_to(ORIGIN)
        with self.voiceover(
            "Oil is one thing the ground gives up. The next part digs for the others: copper, iron, lithium and the "
            "metals the rest of industry is built from, where the same arithmetic of grades, costs and decades-long "
            "projects plays out in rock you can hold."
        ):
            self.play(FadeIn(nxt[0]), FadeIn(nxt[1], scale=1.1), run_time=1.4)
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in pics], lag_ratio=0.3), run_time=1.6)
        self.wait(1.0)
        self.clear_scene()
