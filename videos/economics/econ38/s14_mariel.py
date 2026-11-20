from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class Mariel(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Immigration: \ the Mariel boatlift", r"What does a sudden wave of workers do to wages?",
             "Chapter twelve. Immigration: the Mariel boatlift.",
             lit={1980: r"the boatlift", 1990: r"Card", 2017: r"Borjas"}, scale=("city", "market"),
             horizon=("a year", "a decade"))
        self.boatlift()
        self.debate()

    def boatlift(self):
        Mr = tables.MARIEL.data
        bars = VGroup()
        for k, (nm, v, col) in enumerate(((r"Miami's labour force", Mr["labour_force"], FISH),
                                          (r"its Cuban labour force", Mr["cuban_lf"], BOAT))):
            y = 0.6 - 1.2 * k
            r = Rectangle(width=v * 0.3, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-1.5 + v * 0.15, y, 0]))
            bars.add(VGroup(label(nm, font_size=21, color=col).next_to(r, LEFT, buff=0.25).align_to(
                np.array([-1.6, 0, 0]), RIGHT), r, label(f"+{v}\\%", font_size=24, color=WHITE).next_to(r, RIGHT,
                                                                                                       buff=0.15)))
        head = label(rf"May to September 1980: \ about {Mr['arrivals']:,} Cubans reach Miami by boat",
                     font_size=26, color=E.ACCENT).to_edge(UP, buff=0.8)
        foot = label(r"most with little schooling: \ the supply of less-skilled workers rose even more",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Card, \ \emph{ILR Review} 43(2) (1990)", corner=DR, font_size=12)
        cuba = Ellipse(width=9.0, height=0.9, stroke_width=0, fill_color=GREY_D, fill_opacity=0.8).rotate(
            -0.12).move_to(np.array([-1.2, -2.5, 0]))
        florida = Polygon(*[np.array([x, y, 0]) for x, y in ((0.6, 2.5), (4.2, 2.5), (4.2, 0.9), (3.3, -1.1),
                                                               (2.6, -1.5), (2.0, -0.5), (1.2, 1.5))],
                          stroke_width=0, fill_color=GREY_D, fill_opacity=0.8)
        pm, pmi = np.array([-3.4, -2.0, 0]), np.array([3.25, -0.5, 0])
        mapg = VGroup(cuba, florida, Dot(pm, radius=0.08, color=BOAT), Dot(pmi, radius=0.08, color=FISH),
                      label(r"Mariel, \ Cuba", font_size=22, color=BOAT).next_to(pm, DOWN, buff=0.12),
                      label(r"Miami", font_size=22, color=FISH).next_to(pmi, RIGHT, buff=0.12),
                      label(r"April 1980: \ Castro opens the port", font_size=20, color=GREY_A).move_to(
                          np.array([-3.6, 1.4, 0])),
                      label(r"a schematic map", font_size=13, color=GREY_B).to_corner(DL, buff=0.2))
        route = ArcBetweenPoints(pm + UP * 0.1, pmi + LEFT * 0.1, angle=-0.6)
        boats = VGroup(*[Dot(pm, radius=0.05, color=WHITE) for _ in range(14)])
        with self.voiceover(
            "Immigration poses Card and Krueger's question from the other side: what happens to wages when the number "
            "of workers jumps? In April 1980 Fidel Castro allowed Cubans who wished to leave to depart from the port "
            f"of Mariel. <bookmark mark='a'/> From May to September about {Mr['arrivals']:,} reached Miami by boat. "
            f"<bookmark mark='b'/> Miami's labour force grew {Mr['labour_force']} percent almost overnight, "
            f"<bookmark mark='c'/> its Cuban labour force {Mr['cuban_lf']} percent. <bookmark mark='d'/> Most of the "
            "newcomers had little schooling, so the supply of less-skilled workers rose even more. If any shock should "
            "lower wages, this one should."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(mapg[:6]))
            self.play(FadeIn(mapg[6:]))
            vo.wait_until("a")
            self.play(FadeIn(head), Create(DashedVMobject(route.copy().set_stroke(GREY_B, 2), num_dashes=30)),
                      LaggedStart(*[MoveAlongPath(b_, route) for b_ in boats], lag_ratio=0.12), run_time=3.5)
            vo.wait_until("b")
            self.play(*[FadeOut(m) for m in self.mobjects if m not in (head, tag)], run_time=0.6)
            self.play(FadeIn(bars[0], shift=RIGHT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(bars[1], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def debate(self):
        Mr = tables.MARIEL.data
        cards = point_cards([
            (r"1990: \ Card", r"Miami against four \\ similar cities: \\ no measurable effect \\ on less-skilled wages",
             WAGE),
            (r"2017: \ Borjas", rf"non-Hispanic men \\ without high school: \\ wages fell \\ {Mr['borjas_lo']} to "
                                rf"{Mr['borjas_hi']}\%", LOSS),
            (r"2019: \ Peri and Yasenov", r"synthetic controls, \\ non-Cuban dropouts: \\ no significant \\ difference",
             WAGE),
            (r"the lesson", r"small subsamples \\ of a survey \\ can swing \\ either way", E.ACCENT),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"one event, \ three readings", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"national studies compare skill groups instead; \ the answer turns on substitution \ (Part 39)",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.MARIEL.tag, corner=DR, font_size=12)
        with self.voiceover(
            "What happened? <bookmark mark='a'/> In 1990 David Card compared Miami with four cities whose economies "
            "had moved with it before 1980, and found no measurable effect on less-skilled workers' wages or "
            "unemployment. <bookmark mark='b'/> In 2017 George Borjas looked at a narrower group, non-Hispanic men "
            f"without a high-school diploma, and found their wages fell {Mr['borjas_lo']} to {Mr['borjas_hi']} "
            "percent. <bookmark mark='c'/> Giovanni Peri and Vasil Yasenov built a synthetic Miami from many cities "
            "and found no significant difference, adding that very small subsamples of a survey can produce large "
            "differences in either direction. <bookmark mark='d'/> The debate turned on who counts as a competing "
            "worker and how many of them a survey actually interviewed. <bookmark mark='e'/> Many studies now "
            "compare groups with the same schooling and experience across the whole country instead; their answers "
            "turn on how easily newcomers and natives substitute for each other, the elasticity Part thirty-nine "
            "measures for skilled and unskilled workers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
