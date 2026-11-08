from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Logic(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Description logic", r"Can a machine reason about kinds?", lit=(1991, 2003),
                            part=PART)
        with self.voiceover("Chapter thirteen. Description logic."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.syntax()
        self.tbox()
        self.tableau()
        self.counter()
        self.abox()

    def syntax(self):
        head = label(r"$\mathcal{ALC}$: \ concepts as sets", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{concept}", r"\text{meaning in an interpretation } (\Delta, \cdot^{\mathcal I})"]
        data = [(r"A", r"A^{\mathcal I} \subseteq \Delta"), (r"\lnot C", r"\Delta \setminus C^{\mathcal I}"),
                (r"C \sqcap D", r"C^{\mathcal I} \cap D^{\mathcal I}"), (r"C \sqcup D", r"C^{\mathcal I} \cup D^{\mathcal I}"),
                (r"\exists r.C", r"\{x : \exists y \,((x, y) \in r^{\mathcal I} \land y \in C^{\mathcal I})\}"),
                (r"\forall r.C", r"\{x : \forall y \,((x, y) \in r^{\mathcal I} \to y \in C^{\mathcal I})\}")]
        rows = [[MathTex(a, font_size=28, color=UNIV), MathTex(b, font_size=26)] for a, b in data]
        grid = ValueGrid(hd, rows, col_w=[2.4, 7.4], cell_h=0.55, font_size=20).move_to([0, 0.5, 0])
        notes = stack([(r"a fragment of first-order logic with one free variable: \ decidable", OK),
                       (r"satisfiability is PSPACE-complete \ (Schmidt-Schauß and Smolka, \ 1991)", GREY_A),
                       (r"OWL 2 DL, \ the web's ontology language, \ is the much larger $\mathcal{SROIQ}$", GOAL)],
                      font_size=19, width=12.0).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Ontology has an engineering branch, and its logic is description logic. <bookmark mark='a'/>The basic "
            "language, called ALC, has concept names, which denote sets of things, and roles, which denote relations. "
            "Concepts combine by negation, intersection and union, and by two quantifiers: the things with some "
            "r-successor in C, and the things all of whose r-successors are in C. <bookmark mark='b'/>It is a fragment "
            "of first-order logic, chosen so that reasoning is decidable. <bookmark mark='c'/>Deciding whether a "
            "concept can have instances is PSPACE-complete. <bookmark mark='d'/>The web ontology language, OWL 2, "
            "rests on a much larger description logic of the same family."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i])) for i in range(len(rows))], lag_ratio=0.3),
                      run_time=3)
            for mk, r in zip("bcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def tbox(self):
        d = load("family")
        head = label(r"A terminology \ (TBox)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        defs = VGroup()
        for name, body in d["tbox"].items():
            defs.add(MathTex(r"\mathit{" + name + r"} \equiv " + body, font_size=28))
        defs.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-1.2, 0.2, 0])
        for m in defs:
            m[0].set_color(WHITE)
        q = stack([(r"questions:", GREY_A),
                   (r"is every \textit{Mother} a \textit{Parent}?", UNIV),
                   (r"is every \textit{Grandmother} a \textit{Parent}?", UNIV),
                   (r"is every \textit{Parent} a \textit{Mother}?", UNIV),
                   (r"can a \textit{MotherWithoutDaughter} have a daughter?", UNIV)], font_size=19, aligned_edge=LEFT,
                  width=4.6).move_to([4.6, -2.2, 0])
        with self.voiceover(
            "Here is the textbook example, a terminology for families, from the Description Logic Handbook. "
            "<bookmark mark='a'/>A woman is a female person; a man, a person who is not female. A parent is a person "
            "with some child who is a person. A mother is a woman who is a parent; a grandmother, a mother with some "
            "child who is a parent. A mother without a daughter is a mother all of whose children are not women. "
            "<bookmark mark='b'/>The Reasoner's tableau will answer four questions about these definitions, none of "
            "which is stated in them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in defs], lag_ratio=0.35), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.clear_scene()

    def tableau(self):
        d = load("family")["queries"]["Mother is a Parent"]
        head = label(r"The tableau: \ is every \textit{Mother} a \textit{Parent}?", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        start = MathTex(r"\text{test: } \mathit{Mother} \sqcap \lnot \mathit{Parent} \text{ unsatisfiable?}",
                        font_size=30, color=GOAL).next_to(head, DOWN, buff=0.3)
        root = MathTex(r"x: \ \mathit{Person},\ \mathit{Female},\ \exists \mathit{hasChild}.\mathit{Person},\ "
                       r"\lnot \mathit{Person} \sqcup \forall \mathit{hasChild}.\lnot \mathit{Person}", font_size=26)
        root.move_to([0, 1.0, 0])
        rl = label(r"unfold the definitions, \ push negations in, \ split the conjunctions", font_size=16,
                   color=GREY_A).next_to(root, DOWN, buff=0.12)
        b1 = MathTex(r"x: \lnot \mathit{Person}", font_size=28, color=WHITE).move_to([-3.6, -0.6, 0])
        b2 = MathTex(r"x: \forall \mathit{hasChild}.\lnot \mathit{Person}", font_size=28).move_to([3.2, -0.6, 0])
        e1 = Line(rl.get_bottom() + LEFT * 1.0, b1.get_top(), color=GREY_B)
        e2 = Line(rl.get_bottom() + RIGHT * 1.0, b2.get_top(), color=GREY_B)
        c1 = label(r"clash: \ $\mathit{Person}$ and $\lnot \mathit{Person}$", font_size=18, color=BAD).next_to(
            b1, DOWN, buff=0.2)
        y = MathTex(r"y: \ \mathit{Person}, \ \lnot \mathit{Person}", font_size=28).next_to(b2, DOWN, buff=0.7)
        ey = Arrow(b2.get_bottom(), y.get_top(), buff=0.08, color=GREY_B, stroke_width=2)
        eyl = label(r"$\exists$ makes a child $y$; \ $\forall$ sends it $\lnot \mathit{Person}$", font_size=15,
                    color=GREY_A).next_to(ey, RIGHT, buff=0.1)
        c2 = label(r"clash", font_size=18, color=BAD).next_to(y, DOWN, buff=0.2)
        verdict = label(r"every branch closes: \ $\mathit{Mother} \sqsubseteq \mathit{Parent}$ \ \ (" +
                        f"{d['steps']}" + r" rule applications)", font_size=21, color=OK).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How does the Reasoner decide? <bookmark mark='a'/>To show that every mother is a parent, it tries to "
            "build something that is a mother but not a parent, and shows that this is impossible. "
            "<bookmark mark='b'/>Unfold the definitions and push the negation inwards. The individual x must be a "
            "female person with a child who is a person, and also either not a person, or such that all its children "
            "are not persons. <bookmark mark='c'/>Try the first option: x is not a person. But x is a person: a "
            "clash. <bookmark mark='d'/>Try the second: x has a child y who is a person, and every child of x is not "
            "a person. So y is a person and not a person: another clash. <bookmark mark='e'/>Every branch closes, so "
            "no such thing can exist: every mother is a parent. The Reasoner needed ten rule applications."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(start))
            vo.wait_until("b")
            self.play(FadeIn(root), FadeIn(rl))
            vo.wait_until("c")
            self.play(Create(e1), FadeIn(b1), FadeIn(c1))
            vo.wait_until("d")
            self.play(Create(e2), FadeIn(b2), GrowArrow(ey), FadeIn(eyl), FadeIn(y), FadeIn(c2))
            vo.wait_until("e")
            self.play(FadeIn(verdict))
        self.clear_scene()

    def counter(self):
        d = load("family")
        q = d["queries"]
        head = label(r"Four answers, \ and a model", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{question}", r"\text{answer}", r"\text{steps}"]
        names = list(q)
        rows = [[MathTex(r"\text{" + n + "?}", font_size=24),
                 MathTex(r"\text{yes}" if q[n]["subsumed"] else r"\text{no}", font_size=26,
                         color=OK if q[n]["subsumed"] else BAD), MathTex(str(q[n]["steps"]), font_size=24)]
                for n in names]
        grid = ValueGrid(hd, rows, col_w=[5.0, 1.6, 1.4], cell_h=0.55, font_size=20).move_to([-2.4, 1.0, 0])
        m = q["Parent is a Mother"]["model"]
        x = VGroup(Circle(radius=0.45, color=UNIV), MathTex(r"x", font_size=28)).move_to([3.4, 1.5, 0])
        yv = VGroup(Circle(radius=0.45, color=UNIV), MathTex(r"y", font_size=28)).move_to([3.4, -0.6, 0])
        x[1].move_to(x[0])
        yv[1].move_to(yv[0])
        ar = Arrow(x.get_bottom(), yv.get_top(), buff=0.08, color=GREY_B)
        arl = label(r"hasChild", font_size=16, color=GREY_A).next_to(ar, RIGHT, buff=0.1)
        xl = label(r"\textit{" + ", ".join(m["nodes"][0]).replace("~", r"not ") + "}", font_size=16,
                   color=WHITE).next_to(x, RIGHT, buff=0.2)
        yl = label(r"\textit{" + ", ".join(m["nodes"][1]) + "}", font_size=16, color=WHITE).next_to(yv, RIGHT,
                                                                                                 buff=0.2)
        cap = label(r"a counter-model: \ a parent who is not female", font_size=18, color=BAD).next_to(yv, DOWN,
                                                                                                    buff=0.4)
        contra = label(r"a \textit{MotherWithoutDaughter} with a daughter: \ " +
                       (r"possible" if d["contradiction"]["satisfiable"] else r"impossible") + r" \ (" +
                       f"{d['contradiction']['steps']}" + r" steps)", font_size=20, color=GOAL).move_to([-2.4, -1.8, 0])
        rows2 = label(r"the open-world reading: \ what is not entailed is unknown, \ not false", font_size=19,
                      color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The other questions go the same way. <bookmark mark='a'/>Every grandmother is a parent: yes. Every "
            "parent a mother: no. Every father a woman: no. <bookmark mark='b'/>When a tableau stays open, it hands "
            "back a model: here, a person x who is not female, with a child y who is a person. A father, in other "
            "words, which shows that not every parent is a mother. <bookmark mark='c'/>And a mother without a "
            "daughter who has a daughter is impossible. <bookmark mark='d'/>One feature matters philosophically. "
            "Description logics make the open-world assumption: whatever the definitions do not entail is unknown, "
            "not false. A database would say false."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i])) for i in range(len(rows))], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(x), FadeIn(xl), GrowArrow(ar), FadeIn(arl), FadeIn(yv), FadeIn(yl), FadeIn(cap))
            vo.wait_until("c")
            self.play(FadeIn(contra))
            vo.wait_until("d")
            self.play(FadeIn(rows2))
        self.clear_scene()

    def abox(self):
        d = load("abox")
        head = label(r"From kinds to individuals: \ the ABox", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ab = d["abox"]
        inds = list(ab["concepts"])
        pos = {i: np.array([-5.2, 1.6 - 1.6 * k, 0]) for k, i in enumerate(inds)}
        circles = VGroup(*[VGroup(Circle(radius=0.42, color=NOM).move_to(pos[i]),
                                  label(i, font_size=18, color=WHITE).move_to(pos[i])) for i in inds])
        tags = VGroup(*[label(r"\textit{" + ", ".join(ab["concepts"][i]) + "}", font_size=16, color=UNIV).next_to(
            pos[i], RIGHT, buff=0.55) for i in inds])
        arr = VGroup(*[Arrow(pos[a] + DOWN * 0.42, pos[b] + UP * 0.42, buff=0.05, color=GREY_B, stroke_width=2.5)
                       for a, _, b in ab["roles"]])
        al = VGroup(*[label(r"hasChild", font_size=14, color=GREY_A).next_to(a, LEFT, buff=0.1) for a in arr])
        hd = [r"\text{query}", r"\text{answer}"]
        rows = []
        for q in d["answers"]:
            col = OK if q["answer"] == "yes" else (BAD if q["answer"] == "no" else GOAL)
            rows.append([MathTex(r"\text{is " + q["ind"] + r" a " + q["concept"] + r"?}", font_size=22),
                         MathTex(r"\text{" + q["answer"] + "}", font_size=24, color=col)])
        grid = ValueGrid(hd, rows, col_w=[4.4, 1.8], cell_h=0.5, font_size=20).move_to([2.6, 0.4, 0])
        msc = MathTex(r"\mathit{Mary} : " + d["msc"]["Mary"], font_size=22, color=PARTC).to_edge(DOWN, buff=0.9)
        note = label(r"`roll up' each individual into its most specific concept, \ then ask the tableau", font_size=17,
                     color=GREY_A).next_to(msc, DOWN, buff=0.15)
        with self.voiceover(
            "A terminology describes kinds. Facts about individuals go in an ABox. <bookmark mark='a'/>Mary is a "
            "woman, with a child Tom, who is a person, with a child Ann, who is a woman. <bookmark mark='b'/>The "
            "Reasoner rolls each individual up into the most specific concept that describes it, and asks the tableau. "
            "<bookmark mark='c'/>Is Mary a mother? Yes. A grandmother? Yes: her child Tom has a child. Is Tom a "
            "parent? Yes. <bookmark mark='d'/>Is Tom a father? Unknown: nothing says he is not female. Is Ann a "
            "parent? Unknown: nothing says she has no children. Is Ann a man? No: she is a woman, so female. "
            "<bookmark mark='e'/>Three values, not two. That is the open world: an ontology says what it entails, and "
            "is silent about the rest."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(circles), FadeIn(tags), LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.4),
                      FadeIn(al))
            vo.wait_until("b")
            self.play(FadeIn(msc), FadeIn(note), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i])) for i in range(3)], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i])) for i in range(3, len(rows))], lag_ratio=0.3))
            vo.wait_until("e")
            self.play(*[Indicate(grid.cell[i][1], color=GOAL) for i, q in enumerate(d["answers"])
                        if q["answer"] == "unknown"])
        self.clear_scene()
