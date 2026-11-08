from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403


class Complete(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Gödel's completeness theorem", r"Does proof capture truth?", lit=(1929,),
                            part=PART)
        with self.voiceover("Chapter seven. Gödel's completeness theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.question()
        self.statement()
        self.henkin_plan()
        self.henkin_demo()
        self.consequences()
        self.two_senses()

    def question(self):
        hcs = VGroup(history_card(1928, r"Hilbert \& Ackermann", r"\textit{Principles of Theoretical Logic}: is "
                                  r"every valid formula provable?", width=5.6, color=HIST),
                     history_card(1929, r"Kurt Gödel, aged 23, Vienna", r"doctoral thesis: \ yes", width=5.6,
                                  color=HIST)).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.5)
        two = VGroup(VGroup(MathTex(r"\Gamma \vdash \varphi", font_size=56, color=P.CLAIM),
                            label(r"a proof exists: \ finite, \ checkable", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.2),
                     VGroup(MathTex(r"\Gamma \models \varphi", font_size=56, color=P.AGENT),
                            label(r"true in every structure: \ infinitely many", font_size=24,
                                  color=GREY_A)).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=2.2).move_to(
            [0, -0.7, 0])
        q = MathTex(r"\overset{?}{\Longleftrightarrow}", font_size=56, color=GOAL).move_to(
            (two[0][0].get_center() + two[1][0].get_center()) / 2)
        with self.voiceover(
            "We now have two ideas of 'follows from'. <bookmark mark='a'/>The first is proof: a finite list of "
            "steps, each checkable by a machine. <bookmark mark='b'/>The second is truth: the conclusion is true in "
            "every structure where the premises are, and there are infinitely many structures, of every size. "
            "<bookmark mark='c'/>In 1928 David Hilbert and Wilhelm Ackermann asked in their textbook whether the "
            "rules of proof catch every valid formula. <bookmark mark='d'/>The next year Kurt Gödel, a 23-year-old "
            "student in Vienna, answered yes, in his doctoral thesis."
        ) as vo:
            self.play(FadeIn(two[0]))
            vo.wait_until("a")
            self.play(Indicate(two[0], color=P.CLAIM))
            vo.wait_until("b")
            self.play(FadeIn(two[1]), Write(q))
            vo.wait_until("c")
            self.play(FadeIn(hcs[0], shift=DOWN * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(hcs[1], shift=DOWN * 0.2))
        self.clear_scene()

    def statement(self):
        thm = theorem_card(r"Completeness (Gödel 1929)", r"if $\Gamma \models \varphi$ then $\Gamma \vdash \varphi$:"
                           r" \ every valid argument has a proof", who=r"with soundness: \ $\vdash$ and $\models$ "
                           r"coincide", width=8.4, font_size=26).move_to([0, 1.6, 0])
        eq = VGroup(label(r"equivalently:", font_size=26, color=GREY_A),
                    label(r"every \textit{consistent} set of sentences has a \textit{model}", font_size=32,
                          color=GOAL)).arrange(DOWN, buff=0.2).move_to([0, -0.6, 0])
        why = label(r"($\Gamma \nvdash \varphi$ \ means \ $\Gamma \cup \{\lnot\varphi\}$ is consistent: \ a model "
                    r"of it is a countermodel)", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Here is the theorem. <bookmark mark='a'/>If a conclusion follows from premises, in the sense of truth "
            "in every structure, then there is a proof of it. Together with soundness, which says that proofs never "
            "lead from truth to falsehood, proof and truth coincide exactly. <bookmark mark='b'/>There is an "
            "equivalent form that is easier to prove: every consistent set of sentences, every set from which no "
            "contradiction can be proved, has a model. <bookmark mark='c'/>Why equivalent? If phi cannot be proved "
            "from gamma, then gamma together with not-phi is consistent, and a model of that set is exactly a "
            "countermodel to the argument."
        ) as vo:
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(thm, color=P.CONCL))
            vo.wait_until("b")
            self.play(FadeIn(eq))
            vo.wait_until("c")
            self.play(FadeIn(why))
        self.clear_scene()

    def henkin_plan(self):
        hc = history_card(1949, r"Leon Henkin", r"the proof in every textbook: \ build the model out of words",
                          width=6.4, color=HIST).to_corner(UL, buff=0.4)
        steps = VGroup(
            label(r"1. \ witnesses: \ for each $\exists x\, \varphi(x)$, a new name $c$ with $\varphi(c)$",
                  font_size=26, color=P.CLAIM),
            label(r"2. \ decide everything: \ take the sentences one by one; add each, or its negation, keeping "
                  r"consistency", font_size=26, color=P.AGENT),
            label(r"3. \ the model: \ the objects are the names; \ $\mathrm{R}(c, d)$ holds when the set says so",
                  font_size=26, color=OBJ),
            label(r"4. \ truth lemma: \ a sentence is true in this model exactly when it is in the set",
                  font_size=26, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.5, 0])
        if steps.width > 13.2:
            steps.width = 13.2
        with self.voiceover(
            "Gödel's original proof was intricate. In 1949 Leon Henkin found the proof every textbook now uses, and "
            "its idea is wonderful: build the model out of the language itself. <bookmark mark='a'/>First, give "
            "every existential claim a witness: for each 'there is an x such that phi', a new name c, and the "
            "claim phi of c. <bookmark mark='b'/>Second, decide everything. List all the sentences and take them "
            "one at a time, adding each one or its negation, whichever keeps the set consistent. This is the "
            "Lindenbaum step from Part 2. <bookmark mark='c'/>Third, let the names themselves be the objects, and "
            "let a relation hold between two names exactly when the set says it does. <bookmark mark='d'/>Finally, "
            "prove by induction on formulas that a sentence is true in this model exactly when it belongs to the "
            "set. The witnesses are what make the existential case work."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, st in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=RIGHT * 0.2))
        self.clear_scene()

    def henkin_demo(self):
        d = load("henkin")
        head = label(r"Henkin's construction, in miniature", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        gam = VGroup(label(r"$\Gamma$:", font_size=28, color=GREY_A),
                     *[fm(g, font_size=34) for g in d["gamma"]]).arrange(RIGHT, buff=0.5)
        gl = label(r"`$a$ loves someone; \ nobody loves themselves'", font_size=22, color=GREY_A)
        top = VGroup(gam, gl).arrange(DOWN, buff=0.12).next_to(head, DOWN, buff=0.35)
        wit = VGroup(label(r"1. witness:", font_size=26, color=P.CLAIM), fm(d["witness"], font_size=34,
                                                                            color=P.CLAIM)).arrange(RIGHT, buff=0.3)
        rows = VGroup()
        for at, keep in d["decided"]:
            f = fm(at, font_size=32, color=OK if keep else BAD)
            verdict = label(r"add" if keep else r"deny: \ it would contradict $\Gamma$", font_size=22,
                            color=OK if keep else BAD)
            rows.add(VGroup(f, verdict).arrange(RIGHT, buff=0.35))
        dec_head = label(r"2. decide each atomic sentence, in order:", font_size=26, color=P.AGENT)
        left = VGroup(wit, dec_head, *rows).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(top, DOWN, buff=0.4)
        left.to_edge(LEFT, buff=0.7)
        for r in rows:
            r.shift(RIGHT * 0.4)
        g = relation_graph(d["domain"], [(d["domain"].index(a), d["domain"].index(b)) for a, b in d["L"]],
                           radius=1.1, center=[4.3, -1.3, 0])
        ml = label(r"3. the term model: \ the names are the objects", font_size=24, color=OBJ).next_to(g, UP, buff=0.4)
        ok = label(r"4. \ both sentences of $\Gamma$ are true in it \ $\checkmark$", font_size=24, color=GOAL).next_to(
            g, DOWN, buff=0.35)
        with self.voiceover(
            "Here is the construction on a toy example. <bookmark mark='a'/>The set gamma says that a loves "
            "someone, and that nobody loves themselves. <bookmark mark='b'/>Step one: the existential claim gets a "
            "witness, a new name c, and the sentence 'a loves c'. <bookmark mark='c'/>Step two: decide every atomic "
            "sentence about a and c, in order. Does a love a? Adding that would contradict gamma, so deny it. "
            "<bookmark mark='d'/>Does a love c? Yes, already. <bookmark mark='e'/>Does c love a? That is consistent "
            "with everything so far, so add it. <bookmark mark='f'/>Does c love c? Deny. <bookmark mark='g'/>Step "
            "three: the two names become two objects, and the arrows are the atomic sentences we added. "
            "<bookmark mark='h'/>Both sentences of gamma are true in this model, made out of nothing but words. In "
            "the real proof the list of sentences is infinite, and the Reasoner's model finder is replaced by "
            "consistency, which is defined by proof."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top))
            vo.wait_until("b")
            self.play(FadeIn(wit))
            vo.wait_until("c")
            self.play(FadeIn(dec_head), FadeIn(rows[0]))
            for mk, r in zip("def", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("g")
            self.play(FadeIn(ml), FadeIn(g.nodes))
            self.play(LaggedStart(*[GrowArrow(a) for a in g.arrows], lag_ratio=0.3))
            vo.wait_until("h")
            self.play(FadeIn(ok))
        self.clear_scene()

    def consequences(self):
        head = label(r"Three consequences", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        cs = VGroup(
            VGroup(label(r"validity is \textit{semi-decidable}", font_size=28, color=OK),
                   label(r"list every proof, check each: \ a valid argument is eventually confirmed (Chapter 10)",
                         font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"compactness", font_size=28, color=GOAL),
                   label(r"a proof uses finitely many premises: \ so does every consequence (Chapter 8)",
                         font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"small models", font_size=28, color=P.AGENT),
                   label(r"Henkin's model is built from countably many names: \ every consistent theory has a "
                         r"countable model (Chapter 9)", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                             buff=0.1)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "The theorem has three consequences, and they fill the next three chapters. <bookmark mark='a'/>First, "
            "validity can be confirmed by brute force: list every possible proof and check each in turn. If the "
            "argument is valid, a proof will eventually turn up. <bookmark mark='b'/>Second, compactness: a proof "
            "uses only finitely many premises, so anything that follows from a set of premises follows from a "
            "finite part of it. <bookmark mark='c'/>Third, Henkin's model is made of names, and there are only "
            "countably many names. So every consistent theory has a countable model, even a theory that says there "
            "are uncountably many things."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abc", cs):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=RIGHT * 0.2))
        self.clear_scene()

    def two_senses(self):
        left = VGroup(label(r"1929: \ the \textit{logic} is complete", font_size=30, color=OK),
                      label(r"every valid consequence is provable", font_size=24, color=GREY_A),
                      MathTex(r"\Gamma \models \varphi \ \Rightarrow\ \Gamma \vdash \varphi", font_size=36,
                              color=OK)).arrange(DOWN, buff=0.2)
        right = VGroup(label(r"1931: \ arithmetic is \textit{incomplete}", font_size=30, color=BAD),
                       label(r"some sentence is neither provable nor refutable", font_size=24, color=GREY_A),
                       MathTex(r"\mathsf{PA} \nvdash G \ \text{ and } \ \mathsf{PA} \nvdash \lnot G", font_size=36,
                               color=BAD)).arrange(DOWN, buff=0.2)
        both = VGroup(left, right).arrange(RIGHT, buff=1.4).move_to([0, 0.6, 0])
        bar = Line(UP * 1.4, DOWN * 1.4, color=GREY_C).move_to([both.get_center()[0], 0.6, 0])
        rec = label(r"no contradiction: \ $G$ is true in some models of arithmetic and false in others", font_size=26,
                    color=GOAL).to_edge(DOWN, buff=1.0)
        fwd = label(r"the second theorem, and the false models: \ Part 7, \textit{The Limits of Proof}",
                    font_size=24, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "One warning, because the words are confusing. <bookmark mark='a'/>Gödel's completeness theorem, of "
            "1929, says the logic is complete: everything that follows is provable. <bookmark mark='b'/>Two years "
            "later his incompleteness theorem said that arithmetic is incomplete: there is a sentence about numbers "
            "that the axioms neither prove nor refute. <bookmark mark='c'/>These do not conflict. The undecided "
            "sentence does not follow from the axioms, because it is true in some models of them and false in "
            "others, and completeness only promises proofs of what follows. <bookmark mark='d'/>The strange models "
            "where it fails are the subject of the next chapter, and the theorem itself of Part 7."
        ) as vo:
            self.play(FadeIn(left))
            vo.wait_until("a")
            self.play(Indicate(left, color=P.CLAIM))
            vo.wait_until("b")
            self.play(Create(bar), FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(rec))
            vo.wait_until("d")
            self.play(FadeIn(fwd))
        self.clear_scene()
