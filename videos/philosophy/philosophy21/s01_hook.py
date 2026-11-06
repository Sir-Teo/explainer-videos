from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzles()
        self.stakes()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"Everything is what it is, \ and not another thing.", r"Joseph Butler",
                       r"\textit{Fifteen Sermons} \ (1726)", width=8.6, font_size=26).next_to(t, DOWN, buff=0.5)
        with self.voiceover(
            "Part 20 asked what there is. This part asks what it is for something to be the same thing: at one time, "
            "over time, and through change. <bookmark mark='a'/>Bishop Butler's line sounds like the most obvious "
            "truth in philosophy: everything is what it is, and not another thing. <bookmark mark='b'/>Identity "
            "itself is simple. The trouble comes from the things we want it to apply to."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=GOAL, scale_factor=1.03))
        self.clear_scene()

    def puzzles(self):
        head = label(r"Three puzzles", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        ship = VGroup(*[Rectangle(width=0.32, height=0.5, stroke_width=1, stroke_color=GREY_B,
                                  fill_color=WHOLE if i % 3 else PARTC, fill_opacity=0.8).move_to(
            [-5.6 + 0.34 * i, 0.9, 0]) for i in range(8)])
        hull = Polygon([-5.85, 0.62, 0], [-3.05, 0.62, 0], [-3.4, 0.2, 0], [-5.5, 0.2, 0], color=WHOLE,
                       stroke_width=2)
        person = VGroup(Circle(radius=0.22, color=NOM), Line(ORIGIN, DOWN * 0.7, color=NOM).shift(DOWN * 0.22),
                        Line(DOWN * 0.45, DOWN * 0.45 + LEFT * 0.3, color=NOM),
                        Line(DOWN * 0.45, DOWN * 0.45 + RIGHT * 0.3, color=NOM)).move_to([-4.4, -1.0, 0])
        beam = DashedLine([-4.0, -1.0, 0], [-2.8, -1.0, 0], color=UNIV)
        person2 = person.copy().move_to([-2.4, -1.0, 0])
        rows = stack([(r"a ship whose planks are replaced one by one, \ until none is original: \ the same ship?",
                       WHOLE),
                      (r"and if the old planks are reassembled, \ which ship is the original?", WHOLE),
                      (r"a teleporter scans you, \ destroys you, \ and builds an exact copy on Mars: \ is it you?",
                       NOM),
                      (r"and if it builds two copies?", BAD),
                      (r"a child and the old woman she became share almost no matter, \ and few memories", GOAL)],
                     font_size=22, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.55)
        VGroup(ship, hull).scale(1.3).move_to([-2.8, 1.5, 0])
        VGroup(person, beam, person2).scale(1.2).move_to([2.8, 1.45, 0])
        with self.voiceover(
            "Three puzzles. <bookmark mark='a'/>A ship's planks are replaced one at a time, until none of the "
            "original wood remains. Is it the same ship? <bookmark mark='b'/>And if someone collects the old planks "
            "and reassembles them, which ship is the original? <bookmark mark='c'/>A teleporter scans you, destroys "
            "your body, and builds an exact copy on Mars. Have you travelled, or died? <bookmark mark='d'/>And if it "
            "builds two copies? <bookmark mark='e'/>Closer to home: a girl and the old woman she becomes share almost "
            "no matter and few memories. What makes them one person?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(ship), Create(hull))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(person), Create(beam), FadeIn(person2), FadeIn(rows[2]))
            for mk, r in zip("de", rows[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def stakes(self):
        head = label(r"Why it matters", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"responsibility", r"punish the person who did it: \ but is the prisoner of eighty the youth of twenty?",
             NOM),
            (r"prudence", r"save for retirement: \ why care about that future person more than a stranger?", WHOLE),
            (r"medicine", r"advance directives, \ dementia, \ and who has the authority to refuse treatment", BAD),
            (r"technology", r"uploads, \ backups, \ and programs run as many copies at once", UNIV),
            (r"the method", r"logic first; \ then cases; \ then a Price List where the cases collide", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "These are not idle puzzles. <bookmark mark='a'/>We punish the person who did the deed; but is the prisoner "
            "of eighty the young man of twenty? <bookmark mark='b'/>We save for retirement; why should I care about "
            "that future person more than about a stranger? <bookmark mark='c'/>Advance directives ask whether the "
            "person I am now can bind the person I may become with dementia. <bookmark mark='d'/>And technology is "
            "making copies of minds conceivable, and copies of programs routine. <bookmark mark='e'/>The method is the "
            "series' usual one: logic first, then cases, and a Price List wherever the cases collide."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"the logic of identity; \ Leibniz's law and its converse",
            r"Black's spheres and quantum particles: \ grades of discernibility, \ computed",
            r"the statue and the lump; \ the ship of Theseus, \ plank by plank; \ sortals",
            r"Evans's argument that identity cannot be vague, \ model-checked",
            r"endurance, \ perdurance, \ stages; \ temporary intrinsics",
            r"Locke, \ Reid's brave officer, \ and Parfit's teleporter",
            r"fission \ (the Wall and a Price List); \ animalism; \ the Buddhist chariot",
            r"copies, \ uploads, \ and a model run as many instances",
        ], font_size=23)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>The logic of identity. <bookmark mark='b'/>Whether two things could share "
            "every property, with the grades of discernibility computed. <bookmark mark='c'/>Coincident objects, the "
            "ship of Theseus, and sortal concepts. <bookmark mark='d'/>Evans's proof that identity is never vague, "
            "checked on models. <bookmark mark='e'/>How things persist through time. <bookmark mark='f'/>Personal "
            "identity, from Locke to Parfit. <bookmark mark='g'/>Fission, this part's brick in the Wall; animalism; and "
            "the Buddhist denial of a self. <bookmark mark='h'/>And copies: uploads, and an artificial system running "
            "as many simultaneous instances."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
