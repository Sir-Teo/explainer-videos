from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 14, r"Frontier: \ market power, \ services, \ time", r"What do the models still leave out?",
             "Chapter fourteen. Frontier: market power, services, time.",
             lit={2019: r"markups and trade", 2023: r"Boehm et al."}, scale=("firm", "world"),
             horizon=("a year", "a decade"))
        self.questions()

    def questions(self):
        rows = VGroup(
            label(r"open questions", font_size=27, color=E.ACCENT),
            label(r"market power: \ when a few large firms trade, \ do gains go to markups or to buyers?",
                  font_size=21, color=FIRM),
            label(r"services: \ the fastest-growing trade, \ and the hardest to measure", font_size=21, color=FISH),
            label(r"time: \ elasticities of one in a year and two in a decade; \ which governs the gains?",
                  font_size=21, color=ARCH),
            label(r"adjustment: \ why workers and places recover so slowly from shocks", font_size=21, color=CHINA),
            label(r"geography: \ why activity clusters in a few places \ (Part 37)", font_size=21, color=GAIN),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        tag = published_tag(tables.BOEHM_2023.tag + r"; \ Autor, \ Dorn and Hanson (2013)", corner=DR, font_size=12)
        with self.voiceover(
            "The frontier. <bookmark mark='a'/> Market power: when trade is dominated by a few large firms, how much "
            "of its gain goes into markups rather than lower prices? <bookmark mark='b'/> Services: the fastest-"
            "growing kind of trade, from software to tourism, and the hardest to measure. <bookmark mark='c'/> "
            "Time: an elasticity of one in the first year and two after a decade, so which governs the gains, and "
            "how should a counterfactual handle the path between? <bookmark mark='d'/> Adjustment: why the places "
            "hit by the China shock were still worse off a decade later. <bookmark mark='e'/> And geography: why "
            "economic activity clusters in a few places at all, the subject of the next part."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
