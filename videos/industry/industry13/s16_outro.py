from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        head = tx("Power, priced", 40, GOLD, bold=True).to_edge(UP, buff=0.45)
        pics = VGroup(draw.cooling_tower(1.0), draw.gas_plant(0.9), draw.pylon(1.0), draw.wind_turbine(1.1), draw.battery(0.6)).arrange(
            DOWN, buff=0.25)
        pics.scale_to_fit_height(5.6).move_to([-5.4, -0.5, 0])
        lines = VGroup(
            tx("Electricity is made the instant it is used, so the grid is built for its busiest hour.", 21),
            tx("Load factor, average over peak, sets the cost; Insull built an industry on it.", 21),
            tx("Plants trade fixed cost against running cost; the last one needed sets the price.", 21),
            tx("The wires are a monopoly, and a commission decides what they earn.", 21),
            tx("Markets pay for scarcity; in a storm, that can mean the cap and the dark.", 21),
            tx("Wind, sun and batteries are remaking the day, and data centres the demand.", 21, PRICE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22)
        lines.scale_to_fit_width(min(lines.width, 9.6)).move_to([1.5, -0.4, 0])
        with self.voiceover(
            "Power, priced. <bookmark mark='a'/> Electricity is made the very instant it is used, so the whole system is "
            "built for its busiest hour. <bookmark mark='b'/> Insull saw in 1910 that the ratio of average use to peak "
            "decides what it costs, and built an industry on spreading it. <bookmark mark='c'/> Plants trade fixed cost "
            "against running cost, and the last one needed sets the price for all. <bookmark mark='d'/> The wires are a "
            "monopoly, and a commission decides what they earn. <bookmark mark='e'/> Markets pay for scarcity, and in a "
            "storm that can mean the price at the cap and the lights out. <bookmark mark='f'/> And now wind, sun and "
            "batteries are remaking the shape of the day, while data centres remake the demand."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(p_, shift=RIGHT * 0.2) for p_ in pics], lag_ratio=0.15), run_time=1.6)
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(lines[k]), run_time=1.2)
        self.clear_scene()
        nxt = VGroup(tx("Next: Part 14", 26, GREY_B), tx(PARTS[14], 60, WHITE, bold=True)).arrange(DOWN, buff=0.3)
        icons = VGroup(draw.tank(1.0), draw.truck(1.4), draw.pylon(0.9), draw.house(0.8)).arrange(RIGHT, buff=0.8, aligned_edge=DOWN).next_to(
            nxt, DOWN, buff=0.6)
        VGroup(nxt, icons).move_to(ORIGIN)
        with self.voiceover(
            "The wires are one of the networks nobody thinks about until they fail. The next part follows two more: the "
            "pipes that bring water in and take it away, and the trucks that collect what we throw out, and asks why "
            "these quiet businesses are among the steadiest there are."
        ):
            self.play(FadeIn(nxt[0]), FadeIn(nxt[1], scale=1.1), run_time=1.4)
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in icons], lag_ratio=0.3), run_time=1.6)
        self.wait(1.0)
        self.clear_scene()
