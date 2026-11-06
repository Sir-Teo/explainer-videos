from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Laws(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Explanation by laws", r"What does it take to explain why?", lit=(1948, 1971),
                            part=PART)
        with self.voiceover("Chapter two. Explanation by laws."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.dn()
        self.flagpole()
        self.irrelevance()
        self.statistical()
        self.whatlaw()

    def dn(self):
        hc = history_card(1948, r"Carl Hempel and Paul Oppenheim", r"`Studies in the Logic of Explanation'",
                          width=6.6, color=HIST).to_corner(UL, buff=0.35)
        sch = VGroup(
            label(r"$L_1, \dots, L_k$ \ \ general laws", font_size=24, color=THEORY),
            label(r"$C_1, \dots, C_r$ \ \ particular conditions", font_size=24, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        line = Line(LEFT * 2.4, RIGHT * 2.4, color=GREY_B).next_to(sch, DOWN, buff=0.2)
        concl = label(r"$E$ \ \ the explanandum", font_size=24, color=GOAL).next_to(line, DOWN, buff=0.2)
        schema = VGroup(sch, line, concl).move_to([-2.6, -0.3, 0])
        side = stack([(r"the explanation is a valid deduction", WHITE),
                      (r"its premises are true, \ and include a law essentially", WHITE),
                      (r"symmetry thesis: \ explanation and prediction have the same form", REAL),
                      (r"example: \ why did the car radiator crack? \ water expands on freezing; \ the night was "
                       r"$-10^\circ$C", GREY_A)], font_size=20, aligned_edge=LEFT, width=5.8).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Logical empiricism's most influential product was a theory of explanation. <bookmark mark='a'/>Carl "
            "Hempel and Paul Oppenheim proposed that to explain an event is to deduce it: from general laws, "
            "<bookmark mark='b'/>and particular conditions, <bookmark mark='c'/>to the event to be explained. "
            "<bookmark mark='d'/>The deduction must be valid, its premises true, and a law must be essential to it. "
            "<bookmark mark='e'/>One consequence is the symmetry thesis: an explanation is a prediction made after "
            "the fact, and a prediction is an explanation in advance. <bookmark mark='f'/>Why did the radiator "
            "crack? Because water expands when it freezes, and the night fell to ten below."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(sch[0]))
            vo.wait_until("b")
            self.play(FadeIn(sch[1]), Create(line))
            vo.wait_until("c")
            self.play(FadeIn(concl))
            for mk, r in zip("def", [VGroup(side[0], side[1]), side[2], side[3]]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def flagpole(self):
        d = load("explain")["flagpole"]
        head = label(r"The flagpole and its shadow \ (Bromberger)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        base = np.array([-4.6, -2.0, 0])
        h = 3.0
        s = h / np.tan(np.radians(d["elevation"]))
        pole = Line(base, base + UP * h, color=REAL, stroke_width=6)
        flag = Polygon(base + UP * h, base + UP * (h - 0.5) + RIGHT * 0.7, base + UP * (h - 0.8), color=REAL,
                       fill_opacity=0.6, stroke_width=2)
        shadow = Line(base, base + RIGHT * s, color=GREY_C, stroke_width=8)
        ray = DashedLine(base + UP * h, base + RIGHT * s, color=GOAL)
        ang = Arc(radius=0.6, start_angle=PI - np.radians(d["elevation"]), angle=np.radians(d["elevation"]),
                  arc_center=base + RIGHT * s, color=GOAL)
        thl = label(r"$\theta = " + f"{d['elevation']:.0f}" + r"^\circ$", font_size=20, color=GOAL).next_to(
            ang, LEFT, buff=0.1).shift(UP * 0.1)
        hl = label(r"$h = " + f"{d['height']:.0f}" + r"$ m", font_size=20, color=REAL).next_to(pole, LEFT, buff=0.15)
        sl = label(r"$s = " + f"{d['shadow']:.1f}" + r"$ m", font_size=20, color=GREY_A).next_to(shadow, DOWN,
                                                                                               buff=0.15)
        law = MathTex(r"\tan\theta = \frac{h}{s}", font_size=36, color=THEORY).move_to([3.2, 1.6, 0])
        d1 = stack([(r"$h, \theta$ \ $\Rightarrow$ \ $s = h/\tan\theta = " + f"{d['shadow']:.1f}" + r"$: \ explains "
                     r"the shadow", OK),
                    (r"$s, \theta$ \ $\Rightarrow$ \ $h = s\tan\theta = " + f"{d['height_from_shadow']:.1f}" +
                     r"$: \ a valid D-N argument too", BAD),
                    (r"but the shadow does not explain the height", BAD),
                    (r"the asymmetry the model misses is causal: \ Part 17", GOAL)], font_size=21, aligned_edge=LEFT,
                   width=6.2).next_to(law, DOWN, buff=0.45)
        with self.voiceover(
            "Sylvain Bromberger's flagpole broke the symmetry. <bookmark mark='a'/>A pole ten metres tall, the sun "
            "at thirty-seven degrees. <bookmark mark='b'/>From the law of rectilinear light and some trigonometry, "
            "<bookmark mark='c'/>the height and the angle entail the shadow: thirteen point three metres. That "
            "explains the shadow. <bookmark mark='d'/>But the shadow and the angle entail the height just as "
            "validly, from the same law. By Hempel's lights, that is an explanation too. "
            "<bookmark mark='e'/>Yet no one thinks the shadow explains why the pole is ten metres tall. "
            "<bookmark mark='f'/>The missing ingredient is the direction of causation: the pole makes the shadow, "
            "not the reverse, which is the subject of Part 17."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(pole), FadeIn(flag), FadeIn(hl))
            vo.wait_until("b")
            self.play(Create(ray), Create(shadow), Create(ang), FadeIn(thl), Write(law))
            vo.wait_until("c")
            self.play(FadeIn(sl), FadeIn(d1[0]))
            for mk, r in zip("def", d1[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def irrelevance(self):
        d = load("explain")["salmon"]
        head = label(r"Irrelevance, \ and statistical relevance", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        hd = [r"", r"\text{pill}", r"\text{no pill}"]
        rows = [[MathTex(r"\text{men}", font_size=24), MathTex(f"{d['cells']['man|pill']:.2f}", font_size=24, color=BAD),
                 MathTex(f"{d['cells']['man|no pill']:.2f}", font_size=24, color=BAD)],
                [MathTex(r"\text{women}", font_size=24), MathTex(f"{d['cells']['woman|pill']:.2f}", font_size=24,
                                                                 color=OK),
                 MathTex(f"{d['cells']['woman|no pill']:.2f}", font_size=24, color=OK)]]
        grid = ValueGrid(hd, rows, col_w=[2.0, 1.8, 1.8], cell_h=0.55, font_size=20).move_to([-3.2, 0.4, 0])
        gl = label(r"$P(\text{pregnant})$, \ illustrative", font_size=18, color=GREY_A).next_to(grid, UP, buff=0.2)
        side = stack([(r"`John took his wife's pills, \ so he did not get pregnant': \ a valid D-N argument", WHITE),
                      (r"`this salt was hexed, \ so it dissolved': \ likewise", WHITE),
                      (r"Salmon \ (1971): \ an explanation must cite factors that \textit{change} the probability", OK),
                      (r"the pill is relevant for women, \ irrelevant for men; \ the hex, \ for no one", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=6.4).move_to([3.4, 0.3, 0])
        assert not d["relevant"]["man"] and d["relevant"]["woman"] and not d["hex_relevant"]
        with self.voiceover(
            "Two more counterexamples, one from Wesley Salmon and one from Henry Kyburg. <bookmark mark='a'/>John Jones "
            "took his wife's birth-control pills regularly, and did not become pregnant. Men who take the pill do "
            "not become pregnant; so we have a valid deduction from a true law. <bookmark mark='b'/>And a sample of "
            "salt, hexed by a wizard, dissolved in water; hexed salt dissolves. <bookmark mark='c'/>Salmon's "
            "diagnosis: explanations must cite factors that make a difference to the probability of what they "
            "explain. <bookmark mark='d'/>Among women the pill changes the probability of pregnancy greatly; among "
            "men it changes nothing, and the hex changes nothing for anyone. Statistical relevance, not "
            "deducibility, is what matters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule), FadeIn(gl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(VGroup(*grid.cell[0])))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(VGroup(*grid.cell[1])))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Create(grid.row_box(0, BAD)), Create(grid.row_box(1, OK)))
        self.clear_scene()

    def statistical(self):
        head = label(r"Explaining the improbable", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"inductive-statistical", r"Hempel \ (1962): \ premises make the explanandum highly \textit{probable}, "
                                       r"\ not certain", THEORY),
            (r"paresis \ (Scriven, \ 1959)", r"only about a quarter of untreated syphilitics develop paresis; \ yet "
                                              r"syphilis explains it", BAD),
            (r"the lesson", r"explanation can make an event \textit{less} improbable without making it probable", GOAL),
            (r"what came next", r"causal processes \ (Salmon, \ 1984); \ unification \ (Kitcher); \ mechanisms; \ "
                                r"interventions \ (Woodward)", REAL),
        ]
        g = rows_table(rows, top=1.5, gap=0.55, width=8.4, x_text=-2.0)
        with self.voiceover(
            "Hempel extended the model to probabilistic laws. <bookmark mark='a'/>An inductive-statistical "
            "explanation shows that the event was highly probable, given the laws and conditions. "
            "<bookmark mark='b'/>Michael Scriven's reply: only about a quarter of people with untreated syphilis go "
            "on to develop paresis, yet syphilis is the explanation of paresis, because no one gets paresis without "
            "it. <bookmark mark='c'/>An explanation can raise the probability of an event without making it "
            "probable. <bookmark mark='d'/>Since the 1970s the field has moved to causal processes, unification, "
            "mechanisms, and interventions, the subjects of the next chapter and of Part 17."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def whatlaw(self):
        head = label(r"But what is a law?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        pair = VGroup(
            VGroup(Circle(radius=0.55, color=GOAL, fill_opacity=0.35), label(r"gold", font_size=18, color=GOAL)),
            VGroup(Circle(radius=0.55, color=OK, fill_opacity=0.35), label(r"uranium", font_size=18, color=OK)))
        for p_ in pair:
            p_[1].move_to(p_[0])
        pair.arrange(RIGHT, buff=5.6).move_to([0, 1.3, 0])
        cap = VGroup(label(r"`no gold sphere is a mile wide': \ true, \ by accident", font_size=19,
                           color=GOAL).next_to(pair[0], DOWN, buff=0.25),
                     label(r"`no uranium sphere is a mile wide': \ true, \ by law \ (critical mass)", font_size=19,
                           color=OK).next_to(pair[1], DOWN, buff=0.25))
        rows = [
            (r"the difference", r"laws support counterfactuals: \ a uranium sphere \textit{could not} be built that "
                                r"big", REAL),
            (r"regularity \ (Mill, \ Ramsey, \ Lewis)", r"a law is a theorem of the best system: \ the axioms that "
                                                        r"best balance simplicity and strength", THEORY),
            (r"necessitation \ (Armstrong, \ 1983)", r"a law is a relation between universals that necessitates "
                                                     r"the regularity", ANTI),
            (r"Part 24", r"the best-system account computed, \ and what it implies for chance", GOAL),
        ]
        g = rows_table(rows, top=-0.6, gap=0.4, width=8.4, x_text=-2.2, label_size=20, text_size=19)
        with self.voiceover(
            "Hempel's model needs laws, and so needs to say what a law is. <bookmark mark='a'/>No sphere of gold is "
            "a mile wide, and no sphere of uranium is a mile wide. Both generalizations are true. But the first is "
            "an accident of history, while the second holds by law: a uranium sphere would reach critical mass and "
            "explode long before. <bookmark mark='b'/>Laws, unlike accidents, support counterfactuals: no uranium "
            "sphere could be built that big. <bookmark mark='c'/>On the regularity view of Mill, Ramsey and Lewis, "
            "laws are the theorems of the best system: the axioms that best balance simplicity and strength in "
            "describing everything that happens. <bookmark mark='d'/>On David Armstrong's view, a law is a relation "
            "between universals that necessitates the regularity. <bookmark mark='e'/>Part 24 returns to the "
            "debate, and computes a best system."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pair), FadeIn(cap))
            for mk, r in zip("bcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
