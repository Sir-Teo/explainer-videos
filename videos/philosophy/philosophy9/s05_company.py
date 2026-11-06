from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Company(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Bad company", r"Which definitions are allowed?", part=PART)
        with self.voiceover("Chapter four. Bad company."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.neologicism()
        self.directions()
        self.company()
        self.verdict()

    def neologicism(self):
        hc = history_card(2001, r"Bob Hale \& Crispin Wright", r"\textit{The Reason's Proper Study}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            label(r"neo-logicism: \ Hume's principle is an \textit{implicit definition} of `the number of'", font_size=26,
                  color=NUM),
            label(r"like a dictionary entry: \ it fixes what the words mean, \ so it is known by knowing the words",
                  font_size=24, color=GREY_A),
            label(r"the left side \ (numbers are equal) \ is a new way of saying the right \ (concepts pair off)",
                  font_size=24, color=GREY_A),
            label(r"so we know there are numbers \ as we know that bachelors are unmarried: \ Benacerraf's access "
                  r"problem, \ answered?", font_size=24, color=OK)).arrange(DOWN, buff=0.35).move_to([0, -0.5, 0])
        with self.voiceover(
            "Wright and Bob Hale built a philosophy on Frege's theorem, called neo-logicism. <bookmark mark='a'/>"
            "Hume's principle, they argue, is an implicit definition of the phrase 'the number of'. "
            "<bookmark mark='b'/>Like a dictionary entry, it fixes what the words mean, so anyone who understands "
            "the words knows it is true. <bookmark mark='c'/>Its left side, that two numbers are equal, is a new way "
            "of carving up the content of its right side, that two concepts pair off. <bookmark mark='d'/>If so, we "
            "know there are numbers in roughly the way we know that bachelors are unmarried, and Benacerraf's "
            "problem of access has an answer: no telescope is needed."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def directions(self):
        head = label(r"Abstraction: \ Frege's own example", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        eq = MathTex(r"\mathrm{dir}(a) = \mathrm{dir}(b) \iff a \parallel b", font_size=42, color=NUM).move_to(
            [0, 1.6, 0])
        lines = VGroup()
        cols = [CONCRETE, OK, ABSTRACT]
        for k, (ang, col) in enumerate(zip((0.35, 1.2, 2.3), cols)):
            for j in range(3):
                v = np.array([np.cos(ang), np.sin(ang), 0])
                nrm = np.array([-v[1], v[0], 0])
                c = np.array([-3.2 + 3.2 * k, -0.9, 0]) + nrm * (j - 1) * 0.45
                lines.add(Line(c - v * 1.1, c + v * 1.1, color=col, stroke_width=3))
        arrows = VGroup(*[Arrow([-3.2 + 3.2 * k, -2.25, 0], [-3.2 + 3.2 * k, -2.85, 0], buff=0, color=GREY_B,
                                stroke_width=2) for k in range(3)])
        dirs = VGroup(*[label(rf"a direction", font_size=22, color=c).move_to([-3.2 + 3.2 * k, -3.15, 0])
                        for k, c in enumerate(cols)])
        gl = label(r"lines are concrete enough; \ directions are new abstract objects, \ one per class of parallels",
                   font_size=22, color=GREY_A).next_to(eq, DOWN, buff=0.25)
        with self.voiceover(
            "Hume's principle is one of a family that Frege himself described, now called abstraction principles. "
            "<bookmark mark='a'/>His own example: the direction of line a is the direction of line b exactly when "
            "a and b are parallel. <bookmark mark='b'/>Lines are drawn on paper. Directions are abstract objects, one "
            "for each class of parallel lines, and the principle introduces them by saying when two are the same. "
            "Numbers are to concepts as directions are to lines."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), LaggedStart(*[Create(x) for x in lines], lag_ratio=0.1), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(gl), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(dirs))
        self.clear_scene()

    def company(self):
        d = load("demands")["rows"]
        head = label(r"Good and bad abstraction principles", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        laws = VGroup(
            MathTex(r"\text{HP:}\;\; \#F = \#G \iff F \approx G", font_size=30, color=NUM),
            MathTex(r"\text{BLV:}\;\; \epsilon F = \epsilon G \iff \forall x\,(Fx \leftrightarrow Gx)", font_size=30,
                    color=BAD),
            MathTex(r"\text{NP:}\;\; \nu F = \nu G \iff F \text{ and } G \text{ differ on finitely many objects}",
                    font_size=30, color=CONCRETE)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, 2.0, 0])
        hd = [label(r"objects in the world", font_size=21, color=P.CLAIM),
              label(r"HP needs", font_size=21, color=NUM), label(r"BLV needs", font_size=21, color=BAD),
              label(r"NP needs", font_size=21, color=CONCRETE)]

        def cell(need, have, color):
            return MathTex(str(need), font_size=26, color=OK if need <= have else BAD)
        rows = [[MathTex(str(r["n"]), font_size=26), cell(r["HP"], r["n"], NUM), cell(r["BLV"], r["n"], BAD),
                 cell(r["NP"], r["n"], CONCRETE)] for r in d]
        rows.append([MathTex(r"\aleph_0", font_size=26), MathTex(r"\aleph_0", font_size=26, color=OK),
                     MathTex(r"2^{\aleph_0}", font_size=26, color=BAD),
                     MathTex(r"2^{\aleph_0}", font_size=26, color=BAD)])
        grid = ValueGrid(hd, rows, col_w=[3.0, 2.4, 2.4, 2.4], cell_h=0.44, font_size=22).move_to([0, -1.3, 0])
        note_ = label(r"the Reasoner counts the classes of concepts; \ the infinite row is Cantor (Part 6)",
                      font_size=20, color=GREY_B).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "But not every abstraction principle is good. <bookmark mark='a'/>Basic Law Five has exactly the same "
            "form: the extension of F equals the extension of G exactly when the same things fall under them. And it "
            "is inconsistent. <bookmark mark='b'/>The Reasoner shows why, by counting. Each principle needs one "
            "object for each class of concepts it identifies. In a world of n objects, Hume's principle needs n plus "
            "one objects, which is too many for any finite world, but fine for an infinite one. Basic Law Five needs "
            "two to the n, one for every concept, which is too many for every world, finite or infinite: that is "
            "Cantor's theorem, from Part 6. <bookmark mark='c'/>Now a third principle, Wright's nuisance principle: "
            "two concepts have the same nuisance when they differ on only finitely many objects. On a finite world "
            "all concepts have the same nuisance, so it needs one object, and is fine. On an infinite world it needs "
            "more objects than there are. <bookmark mark='d'/>So the nuisance principle is consistent, but only in "
            "finite worlds, while Hume's principle is consistent only in infinite ones. Each looks like a definition; "
            "they cannot both be true."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(laws[0]), FadeIn(laws[1]))
            vo.wait_until("b")
            self.play(FadeIn(grid.head[:3]), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r][:3])) for r in range(len(rows))], lag_ratio=0.3),
                      FadeIn(note_), run_time=5)
            vo.wait_until("c")
            self.play(FadeIn(laws[2]), FadeIn(grid.head[3]),
                      LaggedStart(*[FadeIn(grid.cell[r][3]) for r in range(len(rows))], lag_ratio=0.3), run_time=3)
            vo.wait_until("d")
            self.play(Indicate(grid.head[1], color=NUM), Indicate(grid.head[3], color=CONCRETE))
        self.clear_scene()

    def verdict(self):
        head = label(r"The bad company objection", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = rows_at([
            (r"Dummett; \ Boolos", r"a definition that can be inconsistent \ is not a definition by its form alone"),
            (r"Boolos (1997)", r"`Is Hume's principle analytic?': \ it implies infinitely many objects"),
            (r"Fine (2002)", r"keep only the \textit{stable} principles: \ true in every big enough world"),
            (r"Caesar again", r"Hume's principle still does not say whether $\#F$ is Julius Caesar"),
        ], x_left=-6.2, x_right=-2.6, y0=1.4, dy=0.9, font_size=25, left_color=GOAL)
        moral = label(r"logicism lives on, \ as a question: \ which ways of introducing objects are legitimate?",
                      font_size=26, color=OK).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "This is the bad company objection. <bookmark mark='a'/>Michael Dummett and George Boolos argued that if "
            "a principle of the right form can be inconsistent, the form alone cannot make it a definition. "
            "<bookmark mark='b'/>Boolos asked, in 1997, whether a principle that implies there are infinitely many "
            "objects can really be analytic. <bookmark mark='c'/>Kit Fine, in The Limits of Abstraction, proposed to "
            "keep only stable principles, the ones true in every large enough world: Hume's principle passes, the "
            "nuisance principle fails. <bookmark mark='d'/>And Julius Caesar has not gone away. <bookmark mark='e'/>"
            "So logicism survives, not as a finished foundation, but as a sharp question: which ways of introducing "
            "objects by definition are legitimate?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(moral))
        self.clear_scene()
