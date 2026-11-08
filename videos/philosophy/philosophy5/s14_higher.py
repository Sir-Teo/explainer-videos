from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403


class Higher(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Vague about vagueness", r"Where does the borderline begin?", lit=(1994,), part=PART)
        with self.voiceover("Chapter thirteen. Vague about vagueness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.problem()
        self.model()
        self.levels()
        self.revenge()

    def problem(self):
        n = 21
        heads = men_row([None] * n, width=12.0, r=0.2, y=1.3)
        step = 12.0 / (n - 1)
        x0 = -6.0
        zones = VGroup(Rectangle(width=step * 7, height=0.3, stroke_width=0, fill_color=OK, fill_opacity=0.7),
                       Rectangle(width=step * 7, height=0.3, stroke_width=0, fill_color=HALF, fill_opacity=0.7),
                       Rectangle(width=step * 7, height=0.3, stroke_width=0, fill_color=BAD, fill_opacity=0.7))
        for i, z in enumerate(zones):
            z.move_to([x0 + step * (7 * i + 3), 0.5, 0])
        edges = VGroup(*[DashedLine([x0 + step * x, 0.9, 0], [x0 + step * x, 0.1, 0], color=WHITE) for x in (6.5, 13.5)])
        qs = VGroup(label(r"is man 7 clearly bald, \ or borderline?", font_size=28, color=GOAL),
                    label(r"if the penumbra has sharp edges, \ we have traded one sharp line for two", font_size=26),
                    label(r"`definitely': \ $D\varphi$ \ (Fine 1975) \ \ borderline: \ $\lnot D B_i \land \lnot D \lnot B_i$",
                          font_size=26, color=GREY_A)).arrange(DOWN, buff=0.3).move_to([0, -1.6, 0])
        with self.voiceover(
            "Every theory so far divides the men into three groups: clearly bald, borderline, clearly not. "
            "<bookmark mark='a'/>But where does the borderline begin? Is man seven clearly bald, or a borderline "
            "case? <bookmark mark='b'/>If the penumbra has sharp edges, we have traded one sharp line for two, and "
            "the original puzzle returns at each of them. <bookmark mark='c'/>To talk about this, add an operator, "
            "'definitely'. A man is borderline when he is neither definitely bald nor definitely not bald. "
            "Higher-order vagueness is the claim that 'definitely bald' is itself vague."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(h) for h in heads], lag_ratio=0.04), FadeIn(zones))
            vo.wait_until("a")
            self.play(FadeIn(qs[0]), Indicate(heads[7], color=GOAL, scale_factor=1.6))
            vo.wait_until("b")
            self.play(Create(edges), FadeIn(qs[1]))
            vo.wait_until("c")
            self.play(FadeIn(qs[2]))
        self.clear_scene()

    def model(self):
        d = load("higher")
        W = d["worlds"]
        head = label(r"`Definitely' as a box, \ with Part 4's modal logic", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.4)
        xs = {k: -5.25 + 1.5 * i for i, k in enumerate(W)}
        nodes = VGroup()
        for k in W:
            nodes.add(VGroup(Circle(radius=0.34, color=P.WORLD, stroke_width=3, fill_color="#0B0F17", fill_opacity=1),
                             MathTex(str(k), font_size=26)).move_to([xs[k], 0.7, 0]))
        for g in nodes:
            g[1].move_to(g[0])
        arcs = VGroup()
        for a in W:
            for b in W:
                if a < b <= a + d["margin"]:
                    arcs.add(ArcBetweenPoints(nodes[W.index(a)].get_top(), nodes[W.index(b)].get_top(),
                                              angle=-PI / 2 if b - a == 1 else -PI / 1.6, color=CONN,
                                              stroke_width=2))
        nl = label(r"worlds: \ the admissible sharpenings, \ named by where the line falls", font_size=22,
                   color=GREY_A).next_to(nodes, DOWN, buff=0.35)
        rl = label(rf"a sharpening `sees' those within {d['margin']}: \ the ones we cannot tell apart from it",
                   font_size=22, color=CONN).next_to(nl, DOWN, buff=0.15)
        df = MathTex(r"D\varphi \text{ at } k \iff \varphi \text{ at every sharpening } k \text{ sees}", font_size=32,
                     color=GOAL).next_to(rl, DOWN, buff=0.45)
        ax = label(r"reflexive and symmetric, \ but not transitive: \ axiom 4 fails, \ so $DB$ does not give $DDB$",
                   font_size=24, color=BAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "There is a precise model, and we already have the tools: Part 4's modal logic. "
            "<bookmark mark='a'/>Let the worlds be the admissible sharpenings, each named by where it draws the "
            "line. <bookmark mark='b'/>A sharpening 'sees' the sharpenings within two of it: the ones we could not "
            "tell apart from it by anything in our use of the word. <bookmark mark='c'/>Then 'definitely' is the "
            "box: definitely phi holds at a sharpening if phi holds at every sharpening it sees. "
            "<bookmark mark='d'/>Notice the shape. Every sharpening sees itself, and seeing is symmetric, but not "
            "transitive: from seven you can see nine, and from nine eleven, but not eleven from seven. By Part 4's "
            "correspondence, axiom T holds and axiom 4 fails. That failure is where higher-order vagueness lives."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(nd) for nd in nodes], lag_ratio=0.1), FadeIn(nl))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.05), FadeIn(rl))
            vo.wait_until("c")
            self.play(Write(df))
            vo.wait_until("d")
            self.play(FadeIn(ax))
        self.clear_scene()

    def levels(self):
        d = load("higher")
        R = d["rows"]
        head = label(r"Each level has its own borderline", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        names = [("B", r"bald"), ("DB", r"definitely bald"), ("DDB", r"definitely definitely bald"),
                 ("borderline", r"borderline")]
        strips = VGroup()
        for k, t in names:
            strips.add(VGroup(label(t, font_size=22, color=GREY_A), status_strip(R[k], width=9.0, height=0.36)).arrange(
                RIGHT, buff=0.35))
        strips.arrange(DOWN, aligned_edge=RIGHT, buff=0.35).next_to(head, DOWN, buff=0.55)
        idx = VGroup(*[MathTex(str(i), font_size=16, color=GREY_B).next_to(strips[0][1][i], UP, buff=0.08)
                       for i in range(0, 21, 2)])
        keys = VGroup(label(r"true at every sharpening", font_size=20, color=OK),
                      label(r"at some", font_size=20, color=HALF),
                      label(r"at none", font_size=20, color=BAD)).arrange(RIGHT, buff=0.8).next_to(strips, DOWN, buff=0.35)
        span = lambda k: [i for i, s in enumerate(R[k]) if s == "I"]  # noqa: E731
        b, db, ddb = span("B"), span("DB"), span("DDB")
        cap = VGroup(label(rf"borderline for `bald': \ men {b[0]}--{b[-1]}; \ for `definitely bald': \ {db[0]}--{db[-1]}; "
                           rf"\ for `definitely definitely': \ {ddb[0]}--{ddb[-1]}", font_size=22, color=GOAL),
                     label(r"and no man is \textit{definitely} borderline: \ the borderline has no clear members",
                           font_size=22, color=BAD)).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        assert "T" not in R["borderline"]
        with self.voiceover(
            "The Reasoner evaluates every man at every sharpening. <bookmark mark='a'/>'Bald' is settled for the "
            f"first seven men and the last seven, and unsettled for men {b[0]} to {b[-1]}. "
            "<bookmark mark='b'/>'Definitely bald' is also unsettled, for a shorter stretch. Whether a man is "
            "definitely bald depends on the sharpening: 'definitely bald' has borderline cases of its own. "
            "<bookmark mark='c'/>So does 'definitely definitely bald', for a shorter stretch still. "
            "<bookmark mark='d'/>And 'borderline' itself is never definitely true of anyone. There is no man of "
            "whom it is settled that he is a borderline case. The penumbra has no sharp edges, because its edges "
            "are themselves vague, all the way up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(keys))
            vo.wait_until("a")
            self.play(FadeIn(strips[0]), FadeIn(idx))
            vo.wait_until("b")
            self.play(FadeIn(strips[1]))
            vo.wait_until("c")
            self.play(FadeIn(strips[2]), FadeIn(cap[0]))
            vo.wait_until("d")
            self.play(FadeIn(strips[3]), FadeIn(cap[1]))
        self.clear_scene()

    def revenge(self):
        head = label(r"Revenge", font_size=36, color=P.WALL).to_edge(UP, buff=0.5)
        rows = VGroup(label(r"three values: \ the line between 1 and $\tfrac12$ is sharp", font_size=26),
                      label(r"supervaluations: \ the set of admissible sharpenings has sharp edges", font_size=26),
                      label(r"degrees: \ `bald to degree exactly 0.6' is as sharp as any cutoff", font_size=26),
                      label(r"epistemicism: \ no revenge, \ but a line no one could ever find", font_size=26,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        moral = label(r"the Wall's real message: \ any precise model of vagueness is precise about something",
                      font_size=26, color=GOAL).to_edge(DOWN, buff=0.5)
        who = label(r"Sainsbury, `Concepts without boundaries' (1990); \ Williamson 1999; \ Wright 1992",
                    font_size=20, color=GREY_B).next_to(moral, UP, buff=0.3)
        with self.voiceover(
            "This is the sorites taking its revenge. <bookmark mark='a'/>A three-valued theory draws a sharp line "
            "between true and indeterminate. <bookmark mark='b'/>A supervaluation draws one around the set of "
            "admissible sharpenings, unless, as in our model, the sharpenings themselves are vague. "
            "<bookmark mark='c'/>A degree theory says a man is bald to degree exactly zero point six, which is as "
            "sharp as any cutoff. <bookmark mark='d'/>Only the epistemicist escapes, by accepting the sharpest line "
            "of all, and saying we can never find it. <bookmark mark='e'/>Mark Sainsbury drew the moral in 1990: "
            "vague concepts are concepts without boundaries, and any model with a boundary misdescribes them. That "
            "is the Wall's real message. A precise model of vagueness is always precise about something."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(who), FadeIn(moral))
        self.clear_scene()
