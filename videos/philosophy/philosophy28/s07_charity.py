from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


class Charity(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Radical interpretation", r"How do we find out what others mean?", lit=(1973,),
                            part=PART)
        with self.voiceover("Chapter six. Radical interpretation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.problem()
        self.compute()
        self.sweep()
        self.schemes()

    def problem(self):
        hc = history_card(1973, r"Donald Davidson", r"`Radical Interpretation'", width=5.2, color=HIST).to_corner(UL,
                                                                                                     buff=0.3)
        eq = MathTex(r"\text{what is held true} \;=\; \text{meaning} \;+\; \text{belief}", font_size=34,
                     color=RULE_C).move_to([0, 1.2, 0])
        rows = stack([(r"the interpreter sees which sentences speakers hold true, \ and when", WHITE),
                      (r"`it is raining' held true: \ because it means that it is raining and they believe it, \ or "
                       r"means something else and they believe that", WORD),
                      (r"one equation, \ two unknowns", BAD),
                      (r"charity: \ assume the speakers are mostly right, \ and solve for meaning", OK)], font_size=21,
                     aligned_edge=LEFT, width=11.6, buff=0.28).move_to([0, -1.2, 0])
        with self.voiceover(
            "Donald Davidson replaced Quine's translator with an interpreter. <bookmark mark='a'/>What she can observe "
            "is which sentences speakers hold true, and in which circumstances. <bookmark mark='b'/>But a sentence is "
            "held true because of two things together: what it means, and what the speaker believes. A speaker holds "
            "true a sentence when it rains either because it means that it is raining and she believes that, or "
            "because it means something else and she believes that instead. <bookmark mark='c'/>One equation, two "
            "unknowns. <bookmark mark='d'/>Davidson's way out is charity: assume that speakers are mostly right about "
            "their surroundings, and solve for meaning."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def compute(self):
        d = load("charity")
        head = label(r"Charity, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["best_is_truth"] and d["observations"] == 60 and d["best_agree"] == 50
        rows_d = d["rows"]
        ax = NumberLine(x_range=[0, 60, 10], length=6.0, color=GREY_B, include_numbers=True, font_size=18,
                        decimal_number_config={"num_decimal_places": 0}).move_to([-0.5, -2.6, 0])
        bars, tags = VGroup(), VGroup()
        for i, r in enumerate(rows_d):
            y = 1.6 - 0.62 * i
            col = OK if i == 0 else GREY_B
            bar = Rectangle(width=6.0 * r["agree"] / 60, height=0.38, stroke_width=0, fill_color=col,
                            fill_opacity=0.85)
            bar.move_to(ax.n2p(r["agree"] / 2) + UP * (y - ax.get_center()[1]))
            bars.add(bar)
            sch = r["scheme"]
            t = label(r", \ ".join(f"{k} = {v}" for k, v in sch.items()), font_size=16,
                      color=OK if i == 0 else GREY_A).next_to(ax.n2p(0), LEFT, buff=0.3).set_y(y)
            tags.add(t)
        xl = label(r"observations the scheme makes true", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        side = stack([(r"three alien sentences, \ heard under rain, \ snow and sun, \ 60 times", WHITE),
                      (r"the speakers err one time in ten", BAD),
                      (r"all six translation schemes tried", RULE_C),
                      (r"charity picks the true one: \ 50 of 60 right; \ it does not make the speakers infallible",
                       OK)], font_size=19, aligned_edge=LEFT, width=4.0, buff=0.25).move_to([4.9, 0.4, 0])
        with self.voiceover(
            "The Reasoner plays interpreter. <bookmark mark='a'/>Three alien sentences, blim, zorf and kua, are heard "
            "sixty times, each under rain, snow or sunshine. <bookmark mark='b'/>The speakers are not perfect: one "
            "time in ten they say the wrong one. <bookmark mark='c'/>There are six ways to translate the three "
            "sentences. For each, the Reasoner counts how many observations it makes come out true. "
            "<bookmark mark='d'/>Charity picks the scheme that maximizes agreement: blim means snow, zorf sun, kua "
            "rain, which is the truth. It makes fifty of the sixty right, not all: the interpreter attributes errors "
            "where it must, and only there."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl), FadeIn(side[2]))
            for b, t in zip(bars, tags):
                self.play(GrowFromEdge(b, LEFT), FadeIn(t), run_time=0.5)
            vo.wait_until("d")
            self.play(Indicate(bars[0], color=OK), FadeIn(side[3]))
        self.clear_scene()

    def sweep(self):
        d = load("sweep")
        head = label(r"How wrong can the speakers be?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = d["rows"]
        by = {round(r["noise"], 2): r["right"] for r in rows}
        assert all(by[e] == 200 for e in (0.0, 0.1, 0.2, 0.3)) and by[0.4] == 198 and by[0.5] == 182
        assert by[0.6] == 97 and by[0.67] == 34 and by[0.7] == 16 and d["n_obs"] == 60
        ax = Axes(x_range=[0, 0.7, 0.1], y_range=[0, 200, 50], x_length=7.0, y_length=3.8, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16}, y_axis_config={"include_numbers": True,
                                                                                "decimal_number_config":
                                                                                    {"num_decimal_places": 0}}
                  ).move_to([-2.3, -0.4, 0])
        xs = VGroup(*[MathTex(f"{k / 10:.1f}", font_size=16, color=GREY_A).next_to(ax.c2p(k / 10, 0), DOWN, buff=0.12)
                      for k in range(0, 8)])
        xl = label(r"the speakers' error rate", font_size=17, color=GREY_A).next_to(xs, DOWN, buff=0.12)
        yl = label(r"trials of 200 in which charity finds the truth", font_size=17, color=GREY_A).next_to(
            ax.y_axis, UP, buff=0.12).align_to(ax, LEFT)
        pts = [ax.c2p(r["noise"], r["right"]) for r in rows]
        curve = VMobject(color=OK, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.06, color=OK) for p in pts])
        chance = DashedLine(ax.c2p(0, 200 / 6), ax.c2p(0.7, 200 / 6), color=BAD, stroke_width=2)
        ctag = label(r"chance: \ 1 in 6", font_size=16, color=BAD).next_to(chance.get_start(), UP, buff=0.08).shift(
            RIGHT * 0.7)
        third = DashedLine(ax.c2p(2 / 3, 0), ax.c2p(2 / 3, 200), color=GOAL, stroke_width=2)
        side = stack([(r"at each error rate, \ 200 fresh sets of 60 observations", WHITE),
                      (r"up to 3 errors in 10: \ the truth every time; \ at half, \ 182 of 200", OK),
                      (r"at $\tfrac23$ the words are independent of the weather: \ 34 of 200, \ chance", BAD),
                      (r"beyond it, \ worse than chance: \ the errors now carry the pattern", GOAL),
                      (r"charity needs speakers who track the world better than chance, \ not perfectly", RULE_C)],
                     font_size=19, aligned_edge=LEFT, width=4.4, buff=0.26).move_to([4.6, -0.2, 0])
        with self.voiceover(
            "How wrong can the speakers be before charity fails? <bookmark mark='a'/>The Reasoner repeats the "
            "experiment at each error rate, from none to seven in ten, with two hundred fresh sets of sixty "
            "observations each. <bookmark mark='b'/>Up to three errors in ten, charity finds the true translation "
            "every time. At four in ten it misses twice in two hundred; at half, it is still right a hundred and "
            "eighty-two times. <bookmark mark='c'/>Then it falls away. At two thirds it is right thirty-four times, "
            "which is chance, one in six: with three sentences, a speaker who errs two times in three picks her words "
            "independently of the weather, and there is nothing left to interpret. <bookmark mark='d'/>Beyond that "
            "point it does worse than chance, because the errors now carry more pattern than the truths. "
            "<bookmark mark='e'/>So charity does not need speakers who are always right, only speakers whose words "
            "track the world better than chance. Davidson's own claim was stronger: that most of a speaker's "
            "beliefs must be true."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xs), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curve), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.15), FadeIn(side[1]),
                      run_time=2)
            vo.wait_until("c")
            self.play(Create(chance), FadeIn(ctag), Create(third), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Indicate(dots[-1], color=GOAL, scale_factor=2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def schemes(self):
        head = label(r"Charity's consequences", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"no alien schemes", r"`On the Very Idea of a Conceptual Scheme' \ (1974): \ a language we could not "
                                  r"translate at all would not be recognizable as a language", RULE_C),
            (r"belief is veridical", r"if interpretation requires most beliefs to be true, \ massive error is "
                                     r"impossible \ (the omniscient interpreter)", OK),
            (r"triangulation", r"meaning is fixed by speaker, \ interpreter and a shared world, \ together", WORLD),
            (r"the critics", r"charity may be too strong: \ we know whole communities have been wrong about a great "
                             r"deal; \ Grandy: \ maximize \textit{humanity}, \ not truth", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "Charity has striking consequences. <bookmark mark='a'/>In 1974 Davidson argued against the very idea of "
            "a conceptual scheme radically different from ours: a language we could not translate at all would not be "
            "recognizable as a language. <bookmark mark='b'/>And if interpreting anyone requires taking most of their "
            "beliefs to be true, then massive error is impossible, a reply to Cartesian scepticism. "
            "<bookmark mark='c'/>Later he spoke of triangulation: meaning is fixed by a speaker, an interpreter, and a "
            "world they share, together. <bookmark mark='d'/>Critics say charity is too strong; whole communities "
            "have been wrong about a great deal. Richard Grandy proposed a principle of humanity instead: attribute "
            "the beliefs it would be reasonable to have, not the true ones."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
