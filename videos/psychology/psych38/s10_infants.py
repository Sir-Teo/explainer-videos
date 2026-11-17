from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403


def hill_scene(helper: bool) -> VGroup:
    """The hill paradigm: a climber (red circle) on a slope, pushed up by a helper (triangle) or down by a
    hinderer (square)."""
    slope = Line([-1.6, -0.8, 0], [1.2, 0.8, 0], color=GREY_B, stroke_width=4)
    top = Line([1.2, 0.8, 0], [1.9, 0.8, 0], color=GREY_B, stroke_width=4)
    climber = Circle(radius=0.2, color=AUTH, fill_opacity=0.9, stroke_width=0).move_to([0.0, 0.25, 0])
    eyes = VGroup(Dot([-0.06, 0.3, 0], radius=0.03, color=BLACK), Dot([0.06, 0.3, 0], radius=0.03, color=BLACK))
    if helper:
        agent = Triangle(color=GOOD, fill_opacity=0.9, stroke_width=0).scale(0.25).move_to([-0.4, -0.15, 0])
        arrow = Arrow([-0.1, 0.0, 0], [0.7, 0.55, 0], color=GOOD, buff=0, stroke_width=4)
    else:
        agent = Square(side_length=0.4, color=WORLD, fill_opacity=0.9, stroke_width=0).move_to([0.45, 0.65, 0])
        arrow = Arrow([0.0, 0.5, 0], [-0.8, -0.05, 0], color=WORLD, buff=0, stroke_width=4)
    return VGroup(slope, top, climber, eyes, agent, arrow)


class Infants(VoiceoverScene):
    def construct(self):
        self.card()
        self.original()
        self.manybabies()

    def card(self):
        card = chapter_card(9, r"Do babies judge?", r"Is a moral sense there before culture?",
                            lit={2007: r"Hamlin, \ Wynn \& Bloom", 2025: r"Lucca et al."}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter nine. Do babies judge?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def original(self):
        head = heading(r"Helper and hinderer")
        h1 = hill_scene(True).move_to([-4.6, 0.9, 0])
        h2 = hill_scene(False).move_to([-1.7, 0.9, 0])
        l1 = label(r"helper", font_size=18, color=GOOD).next_to(h1, DOWN, buff=0.2)
        l2 = label(r"hinderer", font_size=18, color=WORLD).next_to(h2, DOWN, buff=0.2)
        A = axes([-0.6, 1.6], [0, 1.0], x_length=3.6, y_length=1.9, xticks=None, yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"reached for the helper", center=[-3.2, -2.1, 0],
                 font_size=13)
        b = bars(A.ax, [0, 1], [12 / 12, 14 / 16], [GOOD, GOOD], width=0.5)
        names = VGroup(label(r"6 months: \ 12 of 12", font_size=13, color=GREY_A).next_to(A.ax.c2p(0, 0), DOWN,
                                                                                         buff=0.12),
                       label(r"10 months: \ 14 of 16", font_size=13, color=GREY_A).next_to(A.ax.c2p(1, 0), DOWN,
                                                                                          buff=0.12))
        rows = rows_of([
            (r"Hamlin, \ Wynn and Bloom, \ 2007: \ a climber tries to get up a hill; \ one character pushes it up, "
             r"\ another pushes it down", WHITE),
            (r"offered both characters, \ 12 of 12 six-month-olds and 14 of 16 ten-month-olds reached for the "
             r"helper", GOOD),
            (r"read as a moral sense before language, \ before culture could teach one", PERSON),
            (r"critics: \ in some versions the helper's scene had more bouncing, \ a low-level cue the babies might "
             r"follow instead", AUTH),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Hamlin, \ Wynn \& Bloom (2007)")
        with self.voiceover(
            "If some morality is universal, maybe it's there before culture. <bookmark mark='a'/> In 2007 Kiley "
            "Hamlin, Karen Wynn and Paul Bloom showed babies a puppet show. A climber tries to get up a hill. One "
            "character pushes it up. Another pushes it down. <bookmark mark='b'/> Then the babies were offered both "
            "characters. Twelve of twelve six-month-olds, and fourteen of sixteen ten-month-olds, reached for the "
            "helper. <bookmark mark='c'/> It was read as a moral sense before language, before culture could teach "
            "one. <bookmark mark='d'/> Critics noted that in some versions the helper's scene had more bouncing, a "
            "low-level cue the babies might be following instead."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(h1), FadeIn(h2), FadeIn(l1), FadeIn(l2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(A), FadeIn(names), *[GrowFromEdge(x, DOWN) for x in b])
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def manybabies(self):
        head = heading(r"Thirty-seven laboratories")
        A = axes([-0.6, 1.6], [0, 1.0], x_length=4.2, y_length=3.2, xticks=None, yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"chose the helper (or the pusher-up)",
                 center=[-3.6, -0.1, 0], font_size=14)
        b = bars(A.ax, [0, 1], [0.4934, 0.5585], [GOOD, GREY_A], width=0.6)
        chance = DashedLine(A.ax.c2p(-0.6, 0.5), A.ax.c2p(1.6, 0.5), color=AUTH)
        cl = label(r"chance", font_size=14, color=AUTH).next_to(A.ax.c2p(1.6, 0.5), RIGHT, buff=0.08)
        names = VGroup(wrapped_label(r"social: \ helper or hinderer", 1.9, 14, GOOD).next_to(A.ax.c2p(0, 0), DOWN,
                                                                                           buff=0.15),
                       wrapped_label(r"non-social: \ an object pushed up or down", 1.9, 14, GREY_A).next_to(
                           A.ax.c2p(1, 0), DOWN, buff=0.15))
        tops = VGroup(label(r"49.3\%", font_size=16, color=GOOD).next_to(A.ax.c2p(0, 0.4934), UP, buff=0.08),
                      label(r"55.9\%", font_size=16, color=GREY_A).next_to(A.ax.c2p(1, 0.5585), UP, buff=0.08))
        rows = rows_of([
            (r"ManyBabies 4, \ 2025: \ a registered replication across 37 laboratories on five continents, \ "
             r"designed with the original authors", WHITE),
            (r"1{,}018 infants tested, \ 567 included, \ 5.5 to 10.5 months old", GREY_A),
            (r"49.3\% chose the helper; \ 55.9\% chose the character that pushed an object up; \ neither differed "
             r"from chance, \ or from each other", AUTH),
            (r"the authors: \ the effect is weaker than thought, \ absent, \ or develops later; \ the Ledger marks "
             r"the preference at this age as failed", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Lucca et al.\ (2025), \ ManyBabies 4")
        with self.voiceover(
            "So the field tested it at scale. <bookmark mark='a'/> ManyBabies 4 was a registered replication in "
            "thirty-seven laboratories on five continents, designed together with the original authors, and "
            "published in 2025. <bookmark mark='b'/> One thousand and eighteen infants were tested, and five "
            "hundred and sixty-seven were included, from five and a half to ten and a half months old. "
            "<bookmark mark='c'/> Forty-nine percent chose the helper. In a non-social version, fifty-six percent "
            "chose the character that pushed an object up. Neither differed from chance, or from each other. "
            "<bookmark mark='d'/> The authors concluded that the effect is weaker than thought, absent, or develops "
            "later. The Ledger marks the preference at this age as failed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), Create(chance), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), *[GrowFromEdge(x, DOWN) for x in b], FadeIn(tops))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
