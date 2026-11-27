from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        head = tx("Heavy materials", 40, GOLD, bold=True).to_edge(UP, buff=0.45)
        pics = VGroup(draw.blast_furnace(1.6), draw.eaf(1.2), draw.rotary_kiln(1.6), draw.potline(1.6, 4), draw.quarry(1.4, 0.5)
                      ).arrange(DOWN, buff=0.25)
        pics.scale_to_fit_height(5.6).move_to([-5.4, -0.5, 0])
        lines = VGroup(
            tx("They are cheaper by the kilogram than fruit, made in plants that cost billions.", 21),
            tx("Fixed costs make every mill run, so gluts last and profits swing.", 21),
            tx("Scrap and electric furnaces beat ore and coal wherever scrap is plentiful.", 21),
            tx("Cement and stone travel badly: every plant and quarry owns a circle on the map.", 21),
            tx("Aluminium is electricity in solid form; it goes where power is cheap.", 21),
            tx("The money stays where something cannot be copied: a permit near town.", 21, PRICE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22)
        lines.scale_to_fit_width(min(lines.width, 9.6)).move_to([1.5, -0.4, 0])
        with self.voiceover(
            "Heavy materials. <bookmark mark='a'/> They are cheaper by the kilogram than fruit, and made in plants that "
            "cost billions. <bookmark mark='b'/> Their fixed costs make every mill run, so gluts last and profits swing "
            "from boom to loss. <bookmark mark='c'/> Scrap melted with electricity beats ore and coal wherever there is "
            "scrap to melt. <bookmark mark='d'/> Cement and stone travel so badly that every plant and quarry owns a "
            "small territory on the map. <bookmark mark='e'/> Aluminium is electricity in solid form, and goes wherever "
            "power is cheap. <bookmark mark='f'/> And the money stays where something cannot be copied: a scrap-fed mill "
            "near its customers, a quarry with a permit near a growing city. That is why the things everything is made "
            "of earn so little, and why a few of their makers earn a great deal."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(p_, shift=RIGHT * 0.2) for p_ in pics], lag_ratio=0.15), run_time=1.6)
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(lines[k]), run_time=1.2)
        self.clear_scene()
        nxt = VGroup(tx("Next: Part 12", 26, GREY_B), tx(PARTS[12], 60, WHITE, bold=True)).arrange(DOWN, buff=0.3)
        icons = VGroup(draw.column(1.4) if hasattr(draw, "column") else draw.factory(1.4), draw.tank(1.0), draw.barrel(0.7),
                       draw.bottle(0.8, "#7EC8F5", 0.6)).arrange(RIGHT, buff=0.8).next_to(nxt, DOWN, buff=0.6)
        VGroup(nxt, icons).move_to(ORIGIN)
        with self.voiceover(
            "Steel, cement and aluminium are made by changing what rock is made of. The next part goes one step further, "
            "into chemicals, the industry that turns oil, gas and salt into plastics, fertilizers, paints and medicines, "
            "and asks how a few giant plants supply almost everything else."
        ):
            self.play(FadeIn(nxt[0]), FadeIn(nxt[1], scale=1.1), run_time=1.4)
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in icons], lag_ratio=0.3), run_time=1.6)
        self.wait(1.0)
        self.clear_scene()
