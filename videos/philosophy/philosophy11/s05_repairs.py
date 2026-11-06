from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class Repairs(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Justified true belief, plus X", r"Can the analysis be repaired?", lit=(1963,),
                            part=PART)
        with self.voiceover("Chapter four. Justified true belief, plus X."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.lemmas()
        self.defeat()
        self.recipe()

    def lemmas(self):
        head = label(r"Repair 1: \ no false lemmas", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        idea = label(r"Clark (1963): \ knowledge must not rest on any falsehood", font_size=25, color=JUST).next_to(
            head, DOWN, buff=0.3)
        road = Line([-6.6, -1.2, 0], [6.6, -1.2, 0], color=GREY_B, stroke_width=4)
        fakes = VGroup()
        xs = [-5.6, -4.1, -2.6, -1.1, 1.9, 3.4, 4.9]
        for x in xs:
            fakes.add(barn(color="#6E8F5A", fake=True, fill=0.25).move_to([x, -0.5, 0]))
        real = barn(color=BAD, fill=0.6).move_to([0.4, -0.5, 0])
        car = VGroup(RoundedRectangle(width=0.9, height=0.35, corner_radius=0.1, color=BEL, fill_opacity=0.6),
                     Dot([-0.25, -0.2, 0], radius=0.08, color=WHITE), Dot([0.25, -0.2, 0], radius=0.08,
                                                                         color=WHITE)).move_to([-6.0, -1.5, 0])
        fl = label(r"Barn County: \ papier-mâché facades, \ indistinguishable from the road", font_size=22,
                   color="#8FB27A").move_to([0, 1.1, 0])
        rows = VGroup(label(r"Henry looks at the one real barn: \ `that's a barn'", font_size=24),
                      label(r"true, \ justified, \ and inferred from nothing false", font_size=24, color=OK),
                      label(r"but he would have said the same of any facade: \ he doesn't know", font_size=24,
                            color=BAD)).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The first repair came at once. <bookmark mark='a'/>Michael Clark, in 1963, noticed that in both of "
            "Gettier's cases the belief is inferred from a falsehood: Jones will get the job; Jones owns a Ford. So "
            "add a fourth condition: knowledge must not rest on any false lemma. <bookmark mark='b'/>Alvin Goldman, "
            "crediting Carl Ginet, answered with Barn County. Henry is driving through the countryside. Unknown to "
            "him, the locals have put up papier-mâché barn facades, which from the road look exactly like barns. "
            "<bookmark mark='c'/>Henry happens to look at the one real barn, and thinks: that's a barn. "
            "<bookmark mark='d'/>His belief is true and justified, and it is not inferred from anything false. It is "
            "a plain perceptual belief. <bookmark mark='e'/>But had he looked at any of the facades, he would have "
            "believed the same thing. Most people judge that he does not know."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(idea))
            vo.wait_until("b")
            self.play(Create(road), LaggedStart(*[FadeIn(f) for f in fakes], lag_ratio=0.1), FadeIn(real),
                      FadeIn(fl), FadeIn(car))
            vo.wait_until("c")
            self.play(car.animate.move_to([0.4, -1.5, 0]), run_time=2)
            self.play(Indicate(real, color=GOAL), FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]), *[Indicate(f, color=BAD, scale_factor=1.05) for f in fakes])
        self.clear_scene()

    def defeat(self):
        head = label(r"Repair 2: \ no defeaters", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        idea = VGroup(label(r"Lehrer and Paxson (1969); \ Klein (1971):", font_size=24, color=JUST),
                      label(r"no truth, \ if added to S's evidence, \ would defeat the justification", font_size=24,
                            color=WHITE)).arrange(DOWN, buff=0.15).next_to(head, DOWN, buff=0.3)
        good = label(r"Gettier: \ `Smith will get the job' \ is such a truth: \ defeated, \ so no knowledge",
                     font_size=23, color=OK).next_to(idea, DOWN, buff=0.45)
        tom = VGroup(label(r"Tom Grabit:", font_size=25, color=GOAL),
                     label(r"I see Tom steal a library book, \ clearly, \ in good light", font_size=23),
                     label(r"his mother says he has an identical twin, \ who was there", font_size=23,
                           color=GREY_A),
                     label(r"she is deluded: \ there is no twin", font_size=23, color=GREY_A),
                     label(r"the truth `his mother said so' \ would defeat my justification", font_size=23,
                           color=BAD),
                     label(r"yet I know that Tom took the book: \ a \textit{misleading} defeater", font_size=24,
                           color=KNOW)).arrange(DOWN, buff=0.2).move_to([0, -1.5, 0])
        with self.voiceover(
            "The second repair looks at evidence you lack. <bookmark mark='a'/>Keith Lehrer and Thomas Paxson, in "
            "1969, and Peter Klein: you know only if there is no truth which, added to your evidence, would defeat "
            "your justification. <bookmark mark='b'/>This handles Gettier's cases. The truth that Smith himself will "
            "get the job would destroy Smith's reason for his belief. <bookmark mark='c'/>But consider Tom Grabit. I "
            "see Tom steal a book from the library, clearly, in good light. Unknown to me, his mother has told the "
            "police that Tom has an identical twin, who was in the library that day. She is deluded: there is no "
            "twin. Still, the truth that she said so would defeat my justification, if I learned it. Yet surely I "
            "know that Tom took the book. Her claim is a misleading defeater. And telling misleading defeaters from "
            "genuine ones turned out to require something very like knowledge itself."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(idea))
            vo.wait_until("b")
            self.play(FadeIn(good))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t) for t in tom], lag_ratio=0.8), run_time=8)
        self.clear_scene()

    def recipe(self):
        z = load("zagzebski")
        hc = history_card(1994, r"Linda Zagzebski", r"`The Inescapability of Gettier Problems'", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        s1 = VGroup(label(r"step 1: \ X holds, \ the belief is false", font_size=24, color=BEL),
                    label(r"Dr Jones diagnoses virus X \ from textbook symptoms;", font_size=21, color=GREY_A),
                    label(r"in fact virus Y \ is causing them", font_size=21, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([-3.6, 0.9, 0])
        s2 = VGroup(label(r"step 2: \ add independent luck", font_size=24, color=LUCK),
                    label(r"the patient caught X yesterday too, \ too recently", font_size=21, color=GREY_A),
                    label(r"for any symptom: \ the diagnosis is true", font_size=21, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, 0.9, 0])
        hd = [label(r"", font_size=20), label(r"step 1", font_size=22, color=BEL),
              label(r"step 2", font_size=22, color=LUCK)]
        names = [("believes", r"she believes it"), ("justified", r"justified by the symptoms"),
                 ("reliable", rf"a reliable method \ ({round(100 * z['reliability'])}\% right)"),
                 ("true", r"true")]
        rows = [[label(t, font_size=21), mark(z["step1"][k], 26), mark(z["step2"][k], 26)] for k, t in names]
        grid = ValueGrid(hd, rows, col_w=[4.4, 1.6, 1.6], cell_h=0.48, font_size=21).move_to([-2.6, -1.6, 0])
        safe = VGroup(label(r"the Reasoner: \ in the nearby world of step 1,", font_size=21, color=GREY_A),
                      label(r"the same belief, \ false: \ not safe", font_size=21, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(grid, RIGHT, buff=0.5)
        assert not z["safe"]
        dil = VGroup(label(r"if X leaves a gap between justification and truth: \ the recipe applies", font_size=23,
                           color=LUCK),
                     label(r"if X closes the gap: \ justification must guarantee truth, \ and we know almost "
                           r"nothing", font_size=23, color=SKEP)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Dozens of repairs followed, each met by a new case. In 1994 Linda Zagzebski explained why. "
            "<bookmark mark='a'/>Take any proposed condition X that does not guarantee truth. Step one: find a case "
            "where a belief satisfies X and is false. Dr Jones, a careful physician, diagnoses virus X from the "
            "textbook symptoms; in fact virus Y is causing them. <bookmark mark='b'/>Step two: add a piece of luck, "
            "independent of the evidence, that makes the belief true. The patient also caught virus X yesterday, "
            "too recently to show any symptom. <bookmark mark='c'/>The Reasoner runs both steps. She believes it in "
            "both; she is justified in both; her method is reliable in both; in step two the belief is true. Every "
            "condition short of truth survives the luck. <bookmark mark='d'/>And in the nearby world of step one, "
            "the same belief is false: it is not safe. <bookmark mark='e'/>So the dilemma: if X leaves any gap "
            "between justification and truth, the recipe produces a Gettier case. If X closes the gap, then "
            "justification guarantees truth, and we know almost nothing."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(s1))
            vo.wait_until("b")
            self.play(FadeIn(s2))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(4)], lag_ratio=0.5), run_time=4)
            vo.wait_until("d")
            self.play(FadeIn(safe))
            vo.wait_until("e")
            self.play(FadeIn(dil[0]))
            self.play(FadeIn(dil[1]))
        self.clear_scene()
