from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        head = tx("From molecules to money", 40, GOLD, bold=True).to_edge(UP, buff=0.45)
        pics = VGroup(draw.molecule("CH4", bond=0.5), draw.cracker_unit(1.6), draw.sack(0.8, NITRO, label_="N"), draw.cylinder(0.9),
                      draw.paint_can(0.8)).arrange(DOWN, buff=0.25)
        pics.scale_to_fit_height(5.6).move_to([-5.4, -0.5, 0])
        lines = VGroup(
            tx("A few raw materials, gas, oil and salt, become a few building blocks, then almost everything.", 21),
            tx("At the root, the feedstock is most of the cost, and the cheapest molecules win.", 21),
            tx("Shale gave America the cheap molecules; Europe's dear gas is closing its plants.", 21),
            tx("Everyone builds in the good years, so commodity profits swing from boom to loss.", 21),
            tx("Gas companies sign contracts that pass on the cycle; paint makers sell performance.", 21),
            tx("The harm comes later, and the bill with it.", 21, PRICE)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        lines.scale_to_fit_width(min(lines.width, 9.6)).move_to([1.5, -0.4, 0])
        with self.voiceover(
            "From molecules to money. <bookmark mark='a'/> The chemical industry turns a few raw materials, gas, oil and "
            "salt, into a handful of building blocks, and those into almost everything. <bookmark mark='b'/> At the root "
            "of the tree, the feedstock is most of the cost, and the cheapest molecules win. <bookmark mark='c'/> Shale "
            "gave America the cheapest molecules in the rich world; Europe's dear gas is closing its plants. "
            "<bookmark mark='d'/> Everyone builds in the good years, so the commodity makers' profits swing from boom to "
            "loss. <bookmark mark='e'/> Further along the tree, the money steadies: gas companies write contracts that "
            "hand the cycle to their customers, and paint makers sell colour and service, not tonnes. "
            "<bookmark mark='f'/> And the harm a chemical does often arrives decades after its profits, with the bill "
            "close behind."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(p_, shift=RIGHT * 0.2) for p_ in pics], lag_ratio=0.15), run_time=1.6)
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(lines[k]), run_time=1.2)
        self.clear_scene()
        nxt = VGroup(tx("Next: Part 13", 26, GREY_B), tx(PARTS[13], 60, WHITE, bold=True)).arrange(DOWN, buff=0.3)
        icons = VGroup(draw.pylon(1.4), draw.gas_plant(1.0), draw.wind_turbine(1.4), draw.solar_panel(1.0)).arrange(
            RIGHT, buff=0.8, aligned_edge=DOWN).next_to(nxt, DOWN, buff=0.6)
        VGroup(nxt, icons).move_to(ORIGIN)
        with self.voiceover(
            "Gas has been the hero and the villain of this part: the raw material, and the fuel. In the next part it is "
            "one of the fuels of a machine the size of a continent, the electricity grid, where supply has to equal demand "
            "every second, and the question is how you sell a product that cannot be stored, and who pays for the "
            "wires."
        ):
            self.play(FadeIn(nxt[0]), FadeIn(nxt[1], scale=1.1), run_time=1.4)
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in icons], lag_ratio=0.3), run_time=1.6)
        self.wait(1.0)
        self.clear_scene()
