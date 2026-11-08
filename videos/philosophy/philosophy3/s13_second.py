from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403


class Second(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Second-order logic", r"What if we may quantify over properties?", lit=(1888,),
                            part=PART)
        with self.voiceover("Chapter twelve. Second-order logic."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.induction()
        self.says()
        self.price()
        self.ch()
        self.henkin()
        self.plurals()

    def induction(self):
        hc = history_card(1888, r"Richard Dedekind", r"\textit{Was sind und was sollen die Zahlen?}: the numbers "
                          r"are fixed by their axioms", width=6.6, color=HIST).to_corner(UL, buff=0.35)
        fo = VGroup(label(r"first-order induction: \ a scheme, one axiom per formula", font_size=24, color=P.CLAIM),
                    MathTex(r"\varphi(0) \land \forall n\, (\varphi(n) \to \varphi(n + 1)) \ \to\ \forall n\, "
                            r"\varphi(n)", font_size=34, color=P.CLAIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        so = VGroup(label(r"second-order induction: \ one axiom, about every property", font_size=24, color=GOAL),
                    MathTex(r"\forall X\, \big(X(0) \land \forall n\, (X(n) \to X(n + 1)) \ \to\ \forall n\, X(n)\big)",
                            font_size=34, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        both = VGroup(fo, so).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.2, 0])
        thm = label(r"Dedekind: \ every model of the second-order axioms is a copy of $\mathbb{N}$: \ no "
                    r"nonstandard numbers", font_size=26, color=OK).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Chapter eight showed that no first-order theory can rule out nonstandard numbers. The culprit is "
            "induction. <bookmark mark='a'/>In first-order arithmetic, induction is a scheme: one axiom for each "
            "formula phi, and there are only countably many formulas. <bookmark mark='b'/>Allow variables for "
            "properties, written with capital letters, and induction becomes a single axiom: for every property X, "
            "if zero has X and X passes from each number to the next, every number has X. "
            "<bookmark mark='c'/>Richard Dedekind proved in 1888 that every model of these axioms is a copy of the "
            "natural numbers. A nonstandard number c would break it: take X to be 'is a standard number', which "
            "zero has, which passes to successors, and which c lacks."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(fo))
            vo.wait_until("b")
            self.play(FadeIn(so))
            vo.wait_until("c")
            self.play(FadeIn(thm))
        self.clear_scene()

    def says(self):
        head = label(r"What second-order logic can say", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rows = VGroup(
            VGroup(label(r"`the domain is finite'", font_size=26, color=GOAL),
                   MathTex(r"\forall F\, \big(F \text{ one-to-one} \to F \text{ onto}\big)", font_size=32)).arrange(
                RIGHT, buff=0.6),
            VGroup(label(r"`$a$ and $b$ are identical'", font_size=26, color=GOAL),
                   MathTex(r"\forall X\, (X(a) \leftrightarrow X(b))", font_size=32)).arrange(RIGHT, buff=0.6),
            VGroup(label(r"`the real numbers'", font_size=26, color=GOAL),
                   label(r"a complete ordered field: \ every bounded set has a least upper bound", font_size=24,
                         color=GREY_A)).arrange(RIGHT, buff=0.6),
            VGroup(label(r"`uncountable'", font_size=26, color=GOAL),
                   label(r"no one-to-one map into the natural numbers exists", font_size=24, color=GREY_A)).arrange(
                RIGHT, buff=0.6)).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(head, DOWN, buff=0.5)
        leib = label(r"Leibniz's law, as one sentence: \ the identity of indiscernibles (Part 21)", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "With variables over properties and relations, everything compactness forbade comes back. "
            "<bookmark mark='a'/>'The domain is finite': every one-to-one map from the domain to itself is onto. "
            "<bookmark mark='b'/>Identity itself: a and b are identical when they share every property, which is "
            "Leibniz's law. <bookmark mark='c'/>The real numbers, fixed up to isomorphism as a complete ordered "
            "field. <bookmark mark='d'/>And 'uncountable' in its intended sense, so Skolem's paradox disappears: a "
            "countable model would now get uncountability wrong."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
            self.play(FadeIn(leib))
        self.clear_scene()

    def price(self):
        hd = [label(t, font_size=24, color=P.CLAIM) for t in (r"property", r"first-order", r"second-order")]
        props = [(r"complete proof system", True, False), (r"compactness", True, False),
                 (r"Löwenheim--Skolem", True, False), (r"validity semi-decidable", True, False),
                 (r"fixes $\mathbb{N}$ up to isomorphism", False, True), (r"can say `finite'", False, True)]
        rows = [[label(p, font_size=24)] + [a, b] for p, a, b in props]
        grid = ValueGrid(hd, rows, col_w=[5.6, 2.4, 2.4], font_size=26).move_to([0, 0.3, 0])
        why = label(r"no proof system can capture second-order validity: \ it would decide the truths of arithmetic "
                    r"(Part 7)", font_size=24, color=BAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "But there is a bill. <bookmark mark='a'/>Here are the properties side by side. First-order logic has a "
            "complete proof system, compactness, the Löwenheim-Skolem theorems, and semi-decidable validity. "
            "<bookmark mark='b'/>Second-order logic loses every one of them, because it gains the power to pin down "
            "the natural numbers and to say 'finite'. <bookmark mark='c'/>Completeness cannot survive. If the "
            "second-order axioms fix the natural numbers, then a sentence of arithmetic is true exactly when it "
            "follows from them. A complete proof system would therefore list all the truths of arithmetic, and Part "
            "7 proves that nothing can."
        ) as vo:
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            self.play(LaggedStart(*[FadeIn(grid.cell[r][0]) for r in range(len(rows))], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][1]) for r in range(len(rows))], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][2]) for r in range(len(rows))], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(why))
        self.clear_scene()

    def ch(self):
        q = quote_card(r"Set theory in sheep's clothing.", r"Quine, \textit{Philosophy of Logic} (1970), on "
                       r"second-order logic", width=8.0, font_size=34).move_to([0, 2.0, 0])
        chv = VGroup(MathTex(r"\models_2 \ \mathsf{CH}^{*} \quad \text{or} \quad \models_2 \lnot\,\mathsf{CH}^{*}",
                             font_size=42, color=GOAL),
                     label(r"there is a second-order sentence $\mathsf{CH}^*$ that is valid exactly if the continuum "
                           r"hypothesis is true", font_size=24, color=GREY_A),
                     label(r"and set theory cannot settle which (Gödel 1940, Cohen 1963)", font_size=24,
                           color=BAD)).arrange(DOWN, buff=0.25).move_to([0, -0.9, 0])
        with self.voiceover(
            "Is second-order logic even logic? <bookmark mark='a'/>W. V. Quine said no: it is set theory in "
            "sheep's clothing. A variable over properties ranges over all subsets of the domain, so second-order "
            "validity depends on what subsets exist. <bookmark mark='b'/>Here is how far that goes. There is a "
            "second-order sentence that is valid exactly if Cantor's continuum hypothesis is true, the hypothesis "
            "that there is no size strictly between the natural numbers and the reals. <bookmark mark='c'/>And the "
            "axioms of set theory, by the work of Gödel and Paul Cohen, cannot decide the continuum hypothesis. So "
            "either that sentence or its rival is a 'logical truth', and no one knows which. We return to this in "
            "Part 9."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Write(chv[0]), FadeIn(chv[1]))
            vo.wait_until("c")
            self.play(FadeIn(chv[2]))
        self.clear_scene()

    def henkin(self):
        hc = history_card(1950, r"Leon Henkin", r"general models: \ let the property variables range over some "
                          r"subsets only", width=6.4, color=HIST).to_corner(UL, buff=0.4)
        two = VGroup(
            VGroup(label(r"standard semantics", font_size=28, color=P.AGENT),
                   label(r"all subsets", font_size=22, color=GREY_A),
                   label(r"categorical, \ incomplete", font_size=24, color=GOAL)).arrange(DOWN, buff=0.15),
            VGroup(label(r"Henkin semantics", font_size=28, color=P.CLAIM),
                   label(r"a chosen family of subsets", font_size=22, color=GREY_A),
                   label(r"complete, compact, \ not categorical", font_size=24, color=GOAL)).arrange(DOWN, buff=0.15))
        two.arrange(RIGHT, buff=2.0).move_to([0, -0.2, 0])
        moral = label(r"Henkin semantics is first-order logic in disguise: \ the power and the bill come together",
                      font_size=24, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1950 Leon Henkin offered a compromise. <bookmark mark='a'/>Let the property variables range not "
            "over all subsets, but over some chosen family of them. <bookmark mark='b'/>With these general models, "
            "second-order logic regains completeness and compactness, and it loses categoricity: nonstandard models "
            "of arithmetic return. <bookmark mark='c'/>In fact it becomes a many-sorted first-order logic. The power "
            "and the bill come together. You cannot have one without the other."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(two[1]))
            vo.wait_until("b")
            self.play(FadeIn(two[0]))
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()

    def plurals(self):
        s = label(r"`Some critics admire only one another.'", font_size=36).to_edge(UP, buff=0.6)
        gk = MathTex(r"\exists X\, \big(\exists x\, X(x) \land \forall x\, \forall y\, (X(x) \land \mathrm{A}(x, y) "
                     r"\to x \neq y \land X(y))\big)", font_size=36, color=GOAL).next_to(s, DOWN, buff=0.5)
        k = label(r"Geach and Kaplan: \ no first-order sentence says this \ (proved with nonstandard models of "
                  r"arithmetic)", font_size=24, color=GREY_A).next_to(gk, DOWN, buff=0.4)
        hc = history_card(1984, r"George Boolos", r"`To be is to be a value of a variable (or to be some values of "
                          r"some variables)'", width=7.6, color=HIST).next_to(k, DOWN, buff=0.5)
        pl = label(r"read $\exists X$ as `there are some things': \ plural logic, with no new objects", font_size=24,
                   color=OK).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Second-order quantifiers also turn up in plain English. <bookmark mark='a'/>'Some critics admire only "
            "one another.' <bookmark mark='b'/>The natural formalization says: there are some things, the critics in "
            "question, such that each of them admires only others among them. <bookmark mark='c'/>Peter Geach and "
            "David Kaplan showed that no first-order sentence says this, by a proof that uses nonstandard models of "
            "arithmetic. <bookmark mark='d'/>In 1984 George Boolos argued that such quantifiers are innocent: "
            "'there exist some critics' does not posit a new object, a set of critics, only the critics themselves. "
            "To be, he wrote, is to be a value of a variable, or to be some values of some variables. "
            "<bookmark mark='e'/>That slogan rewrites a famous one, which is the subject of Chapter fourteen."
        ) as vo:
            self.play(FadeIn(s))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Write(gk))
            vo.wait_until("c")
            self.play(FadeIn(k))
            vo.wait_until("d")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(pl))
        self.clear_scene()
