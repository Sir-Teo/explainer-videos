from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403


class Montague(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"English as a formal language", r"Can natural language be given a logic?",
                            lit=(1970,), part=PART)
        with self.voiceover("Chapter nine. English as a formal language."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.thesis()
        self.types()
        self.lam()
        self.beta()
        self.lifting()

    def thesis(self):
        q = quote_card(r"There is in my opinion no important theoretical difference between natural languages and the "
                       r"artificial languages of logicians.", r"Richard Montague", r"`Universal Grammar' \ (1970)",
                       width=10.4, font_size=26).to_edge(UP, buff=0.6)
        rows = stack([(r"syntax and semantics built in parallel: \ each rule that forms a phrase has a rule that "
                       r"interprets it", SENSE),
                      (r"meanings composed by function application, \ in a typed $\lambda$-calculus", NAME),
                      (r"Frege's compositionality, \ made into an algorithm", GOAL)], font_size=22, aligned_edge=LEFT,
                     width=11.6, buff=0.3).move_to([0, -1.3, 0])
        with self.voiceover(
            "The logicians of the twentieth century mostly thought natural language too messy for logic; it was to "
            "be replaced, not analysed. <bookmark mark='a'/>Richard Montague disagreed. There is in my opinion, he "
            "wrote in 1970, no important theoretical difference between natural languages and the artificial "
            "languages of logicians. <bookmark mark='b'/>His method: build syntax and semantics in parallel, so that "
            "every rule that forms a phrase comes with a rule that interprets it. <bookmark mark='c'/>The "
            "interpretations compose by applying functions to arguments, in a typed lambda calculus. "
            "<bookmark mark='d'/>It is Frege's principle of compositionality turned into an algorithm."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def types(self):
        head = label(r"Types", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        M_ = M.SCOPE_MODEL
        hd = [r"\text{type}", r"\text{what it is}", r"\text{example}", r"\text{in the model}"]
        cells = [
            [MathTex(r"e", font_size=26, color=REF), label(r"an individual", font_size=20),
             label(r"`Ann'", font_size=20, color=NAME), label(r"ann", font_size=20, color=REF)],
            [MathTex(r"t", font_size=26, color=TRUTH), label(r"a truth value", font_size=20),
             label(r"`Ann smokes'", font_size=20, color=NAME), tv(True, 22)],
            [MathTex(r"\langle e, t\rangle", font_size=26, color=SENSE), label(r"a property: \ $e$ to $t$",
                                                                              font_size=20),
             label(r"`smokes'", font_size=20, color=NAME), label(r"\{" + ", ".join(sorted(M_.preds["smoke"])) + r"\}",
                                                                 font_size=20, color=REF)],
            [MathTex(r"\langle e, \langle e, t\rangle\rangle", font_size=26, color=SENSE),
             label(r"a relation", font_size=20), label(r"`likes'", font_size=20, color=NAME),
             label(r"pairs", font_size=20, color=REF)],
            [MathTex(r"\langle\langle e, t\rangle, t\rangle", font_size=26, color=SENSE),
             label(r"a property of properties", font_size=20), label(r"`every student'", font_size=20, color=NAME),
             label(r"the sets containing every student", font_size=20, color=REF)],
            [MathTex(r"\langle\langle e, t\rangle, \langle\langle e, t\rangle, t\rangle\rangle", font_size=26,
                     color=SENSE), label(r"a relation between properties", font_size=20),
             label(r"`every'", font_size=20, color=NAME), label(r"$\subseteq$", font_size=22, color=REF)],
        ]
        assert sorted(M_.preds["smoke"]) == ["ann", "bob"]
        grid = ValueGrid(hd, cells, col_w=[3.0, 3.8, 2.4, 4.2], cell_h=0.5, font_size=21).move_to([0, -0.2, 0])
        with self.voiceover(
            "Every expression gets a type. <bookmark mark='a'/>Type e is for individuals, like the referent of Ann; "
            "type t for truth values, like the referent of a sentence, as Frege said. <bookmark mark='b'/>Every other "
            "type is a function type. A property, like smokes, takes an individual to a truth value: type e to t. In "
            "the model, it is the set of smokers, Ann and Bob. <bookmark mark='c'/>A transitive verb takes an "
            "individual and gives a property. <bookmark mark='d'/>A noun phrase like every student is a property of "
            "properties: it is true of exactly the properties every student has. <bookmark mark='e'/>And a "
            "determiner like every relates two properties: every A is B is true when the A's are among the B's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            self.play(*[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in grid.cell[1]])
            for mk, r in zip("bcde", range(2, 6)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]])
        self.clear_scene()

    def lam(self):
        head = label(r"The $\lambda$-calculus", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        lines = VGroup(
            MathTex(r"\lambda z.\, \textsc{smoke}(z)", font_size=40, color=SENSE),
            MathTex(r"\big(\lambda z.\, \textsc{smoke}(z)\big)(\mathit{ann})", font_size=40, color=NAME),
            MathTex(r"\rightsquigarrow\; \textsc{smoke}(\mathit{ann})", font_size=40, color=TRUTH),
        ).arrange(DOWN, buff=0.5).move_to([0, 0.9, 0])
        rule = MathTex(r"(\lambda x.\, M)(N) \;\rightsquigarrow\; M[x := N]", font_size=34, color=GOAL).move_to(
            [0, -1.3, 0])
        rows = stack([(r"$\lambda z$ makes a function: \ `the property of being a $z$ such that $z$ smokes'", SENSE),
                      (r"applying it substitutes the argument for the variable: \ $\beta$-reduction", NAME),
                      (r"evaluated in the model: \ ann is a smoker, \ so true", OK)], font_size=21, aligned_edge=LEFT,
                     width=11.6, buff=0.25).to_edge(DOWN, buff=0.4)
        assert M.evaluate(("pred", "smoke", (("c", "ann"),)), M.SCOPE_MODEL) is True
        with self.voiceover(
            "The glue is Alonzo Church's lambda calculus. <bookmark mark='a'/>Lambda z, smoke of z, is a function: "
            "the property of being a z such that z smokes. <bookmark mark='b'/>Apply it to Ann. "
            "<bookmark mark='c'/>The rule, called beta reduction, substitutes the argument for the variable: smoke "
            "of Ann. <bookmark mark='d'/>That is the whole of the machinery: lambda to make functions, application to "
            "use them, and beta reduction to simplify. <bookmark mark='e'/>Evaluated in the model, smoke of Ann is "
            "true."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(lines[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(lines[1]))
            vo.wait_until("c")
            self.play(Write(lines[2]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Write(rule))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def beta(self):
        d = load("beta")
        head = label(r"`Every student smokes', \ reduced", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        steps = d["tex"]
        assert len(steps) == 5 and d["value"] is False
        lines = VGroup()
        for i, s in enumerate(steps):
            m = MathTex((r"\rightsquigarrow\; " if i else "") + s, font_size=28,
                        color=TRUTH if i == len(steps) - 1 else (NAME if i == 0 else WHITE))
            if m.width > 12.6:
                m.width = 12.6
            lines.add(m)
        lines.arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to([0, 0.3, 0])
        rows = stack([(r"[[every]] applied to [[student]], \ then to [[smokes]]: \ four $\beta$-steps", SENSE),
                      (r"in the model: \ the students are ann, bob and cy; \ cy does not smoke: \ false", BAD)],
                     font_size=21, aligned_edge=LEFT, width=11.6, buff=0.22).to_edge(DOWN, buff=0.35)
        assert sorted(M.SCOPE_MODEL.preds["student"]) == ["ann", "bob", "cy"] and "cy" not in M.SCOPE_MODEL.preds["smoke"]
        with self.voiceover(
            "Now a quantified sentence. <bookmark mark='a'/>The meaning of every is a function that takes two "
            "properties, P and Q, and says that everything P is Q. Apply it to the meaning of student, and then to the "
            "meaning of smokes. <bookmark mark='b'/>The Reasoner reduces the term one step at a time. First the "
            "outer lambda P takes student. <bookmark mark='c'/>Then lambda Q takes smokes. <bookmark mark='d'/>Then "
            "the two inner applications reduce, <bookmark mark='e'/>leaving a plain first-order formula: for every x, "
            "if x is a student, x smokes. <bookmark mark='f'/>In the model the students are Ann, Bob and Cy, and Cy "
            "does not smoke, so the sentence is false."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(rows[0]))
            for mk, l in zip("bcde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=DOWN * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def lifting(self):
        head = label(r"Noun phrases as quantifiers", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"every student", r"$\lambda Q.\, \forall x\,[\textsc{student}(x) \rightarrow Q(x)]$: \ the properties "
                               r"every student has", SENSE),
            (r"Ann, \ lifted", r"$\lambda Q.\, Q(\mathit{ann})$: \ the properties Ann has \ (Montague treated every "
                               r"noun phrase so)", NAME),
            (r"a mismatch", r"`Ann likes every student': \ `likes' wants an individual, \ $e$, \ but `every student' is "
                            r"of type $\langle\langle e,t\rangle,t\rangle$", BAD),
            (r"the fix", r"move the quantifier, \ and leave a variable behind: \ the next chapter builds it", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "One of Montague's insights is that noun phrases are not names. <bookmark mark='a'/>Every student "
            "denotes a property of properties: the set of properties every student has. <bookmark mark='b'/>Even a "
            "name can be lifted to that type: Ann, as lambda Q, Q of Ann, the set of properties Ann has. Montague "
            "treated every noun phrase this way, so all of them have one type. <bookmark mark='c'/>But there is a "
            "mismatch. In Ann likes every student, the verb likes wants an individual as its object, and every "
            "student is a quantifier. The types do not fit. <bookmark mark='d'/>The standard fix moves the "
            "quantifier out of the way, leaving a variable behind. The next chapter builds it, in a working parser."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
