from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ measuring the damage", r"How do economists put a number on a spillover, \ when "
             r"nobody pays for it?", "Chapter fifteen. Frontier: measuring the damage.",
             lit={2003: r"Chay and Greenstone", 2011: r"Currie and Walker", 2019: r"Deryugina et al."},
             scale=("city", "nation"), horizon=("a year", "a decade"))
        self.problem()
        self.ezpass()
        self.open()

    def problem(self):
        rows = VGroup(
            label(r"Pigou's tax needs a number: \ the damage of one more unit", font_size=25, color=E.ACCENT),
            label(r"but pollution isn't assigned at random: \ dirty places differ in a hundred other ways",
                  font_size=24, color=SOCIAL),
            label(r"the answer is part four's: \ find something that moves pollution and nothing else", font_size=24,
                  color=GOOD),
            label(r"Kenneth Chay and Michael Greenstone, \ 2003: \ the 1981--82 recession cut pollution unevenly \ "
                  r"across counties", font_size=22, color=GREY_A),
            label(r"where pollution fell more, \ fewer babies died", font_size=24, color=GOOD),
            label(r"Tatyana Deryugina and coauthors, \ 2019: \ days when the wind blows pollution in, \ and the "
                  r"deaths of older people", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Chay and Greenstone, QJE 118(3) (2003); \ Deryugina, Heutel, Miller, Molitor and Reif, "
                            r"AER 109(12) (2019)", corner=DR, font_size=12)
        with self.voiceover(
            "The frontier of this part is measurement. <bookmark mark='a'/> Pigou's tax needs a number: the damage "
            "done by one more unit. <bookmark mark='b'/> But pollution isn't handed out at random. The dirtiest "
            "places differ from the cleanest in a hundred other ways, and a simple comparison mixes them all up. "
            "<bookmark mark='c'/> The answer is part four's: find something that moves pollution and nothing else. "
            "<bookmark mark='d'/> In 2003 Kenneth Chay and Michael Greenstone used the recession of 1981 and 1982, "
            "which shut factories and cut pollution far more in some counties than in others. "
            "<bookmark mark='e'/> Where pollution fell more, fewer babies died. <bookmark mark='f'/> In 2019 Tatyana "
            "Deryugina and coauthors used the wind: on days when it blows a city's pollution toward a county, more "
            "older people there die, and spend more on hospital care."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def ezpass(self):
        cw = tables.CURRIE_WALKER_2011.data
        ax = plane([0, 3], [0, 14], center=LEFT * 2.9 + DOWN * 0.4, x_length=5.4, y_length=4.4, xticks=[],
                   yticks=[0, 4, 8, 12], xlabel="", ylabel=r"fall, \ percent", font_size=16, yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        u, uy = a.x_axis.get_unit_size(), a.y_axis.get_unit_size()
        vals = [(0.9, -100 * cw["prematurity"], r"premature \\ births"), (2.1, -100 * cw["low_birth_weight"],
                                                                           r"low birth \\ weight")]
        bars = VGroup()
        for x0, v, nm in vals:
            r = Rectangle(width=0.7 * u, height=v * uy, stroke_width=0, fill_color=GOOD, fill_opacity=0.85).move_to(
                a.c2p(x0, 0), aligned_edge=DOWN)
            bars.add(VGroup(r, label(rf"{v:.1f}\%", font_size=20, color=GOOD).next_to(r, UP, buff=0.1),
                            label(nm, font_size=16, color=GREY_A).next_to(a.c2p(x0, 0), DOWN, buff=0.2)))
        side = VGroup(
            label(r"Janet Currie and Reed Walker, \ 2011", font_size=21, color=GREY_A),
            label(r"electronic tolls, \ E-ZPass, \ came to New Jersey and Pennsylvania: \\ cars stopped queueing at "
                  r"the toll plazas", font_size=20),
            label(rf"mothers living within {cw['near_km']} km of a plaza, \\ against those {cw['control_km'][0]} to "
                  rf"{cw['control_km'][1]} km away", font_size=20, color=ROAD),
            label(r"after the switch, \ fewer premature \\ and underweight babies near the plazas", font_size=20,
                  color=GOOD),
            label(r"congestion's damage, \ measured: \\ part of what a toll would also buy", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Currie and Walker, AEJ: Applied 3(1) (2011)", corner=DR, font_size=13)
        with self.voiceover(
            "One study connects this part's threads. <bookmark mark='a'/> Janet Currie and Reed Walker looked at "
            "E-ZPass, the electronic toll system. <bookmark mark='b'/> When it came to toll plazas in New Jersey and "
            "Pennsylvania, cars no longer queued and idled at the booths, and the air around them cleared. "
            "<bookmark mark='c'/> They compared mothers who lived within two kilometres of a plaza with mothers two to "
            "ten kilometres away, before and after the switch. <bookmark mark='d'/> Near the plazas, premature births "
            "fell by about eleven percent, and low birth weight by about twelve. <bookmark mark='e'/> That is "
            "congestion's damage, measured, and part of what a congestion charge would also buy."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            for mk, r in zip("abc", side[1:4]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(*[GrowFromEdge(b_[0], DOWN) for b_ in bars], *[FadeIn(b_[1:]) for b_ in bars])
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def open(self):
        head = label(r"open questions", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"how should damages decades away be counted today? \ part forty-eight's discount rate",
                  font_size=23),
            label(r"what is a forest, \ a wetland, \ a species worth, \ beyond what anyone pays for it?",
                  font_size=23, color=FISH),
            label(r"when the spillover crosses borders, \ who bargains, \ and who enforces?", font_size=23,
                  color=SOCIAL),
            label(r"can new data, \ from satellites and sensors, \ price spillovers that were invisible?",
                  font_size=23, color=GOOD),
            label(r"next: \ markets designed on purpose: \ auctions", font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.42).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Open questions follow. How should damages that arrive decades from now be counted today? That is part "
            "forty-eight's fight over the discount rate. <bookmark mark='b'/> What is a forest, a wetland or a species "
            "worth, beyond what anyone pays to use it? <bookmark mark='c'/> When a spillover crosses borders, who "
            "bargains, and who enforces the bargain? <bookmark mark='d'/> Can new data, from satellites and cheap "
            "sensors, price spillovers that used to be invisible? <bookmark mark='e'/> And next: markets designed on "
            "purpose, starting with auctions."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(rows[0], shift=UP * 0.1))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
