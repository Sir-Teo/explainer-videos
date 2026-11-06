from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Curry(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Proofs are programs", r"What is a proof made of?", lit=(1958,), part=PART)
        with self.voiceover("Chapter seven. Proofs are programs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.dictionary()
        self.tree()
        self.search()
        self.running()

    def dictionary(self):
        hcs = VGroup(history_card(1958, r"Haskell Curry \& Robert Feys", r"\textit{Combinatory Logic}: \ the types of "
                                  r"$\mathsf{K}$ and $\mathsf{S}$ are axioms", width=5.6, color=HIST),
                     history_card(1969, r"William Howard", r"`The formulae-as-types notion of construction' \ "
                                  r"(published 1980)", width=5.6, color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP,
                                                                                                         buff=0.3)
        hd = [label(r"logic", font_size=24, color=P.CLAIM), label(r"programming", font_size=24, color=PROOF)]
        pairs = [(r"a proposition $A$", r"a type $A$"), (r"a proof of $A$", r"a program of type $A$"),
                 (r"$A \to B$", r"a function from $A$ to $B$"), (r"$A \wedge B$", r"a pair: \ one $A$, one $B$"),
                 (r"$A \vee B$", r"a tagged value: \ an $A$ or a $B$, \ and which"),
                 (r"$\bot$", r"the empty type: \ no values at all"), (r"$\lnot A$", r"a function from $A$ to $\bot$"),
                 (r"simplifying a proof", r"running the program")]
        rows = [[label(a, font_size=22), label(b, font_size=22, color=PROOF)] for a, b in pairs]
        grid = ValueGrid(hd, rows, col_w=[4.6, 6.4], cell_h=0.5, font_size=22).move_to([0, -1.1, 0])
        with self.voiceover(
            "Brouwer's reading of the connectives, the BHK reading of Part 5, turned out to be more than "
            "philosophy. <bookmark mark='a'/>Haskell Curry noticed in 1934, and wrote up with Robert Feys in 1958, "
            "that the types of his basic combinators are exactly the axioms of the logic of 'if'. William Howard "
            "extended the observation in 1969, in notes that circulated for a decade before they were published. "
            "<bookmark mark='b'/>The result is a dictionary. A proposition is a type. A proof of it is a program of "
            "that type. A proof of 'if A then B' is a function from A to B. A proof of 'A and B' is a pair. A proof of "
            "'A or B' is a tagged value: an A or a B, together with which. Falsehood is the empty type, which has no "
            "values, so 'not A' is a function from A into the empty type. And simplifying a proof is running the "
            "program."
        ) as vo:
            self.play(FadeIn(hcs))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(len(rows))], lag_ratio=0.5),
                      run_time=10)
        self.clear_scene()

    def tree(self):
        head = label(r"A proof, \ and the same proof as a program", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        plain = [r"[A \wedge B]^1", r"[A \wedge B]^1", r"B", r"A", r"B \wedge A", r"A \wedge B \to B \wedge A"]
        typed = [r"p : A \wedge B", r"p : A \wedge B", r"\mathsf{snd}\ p : B", r"\mathsf{fst}\ p : A",
                 r"\langle \mathsf{snd}\ p,\ \mathsf{fst}\ p \rangle : B \wedge A",
                 r"\lambda p.\ \langle \mathsf{snd}\ p,\ \mathsf{fst}\ p \rangle : A \wedge B \to B \wedge A"]
        pos = [(-2.0, 1.4), (2.0, 1.4), (-2.0, 0.35), (2.0, 0.35), (0, -0.7), (0, -1.75)]
        nodes = VGroup(*[MathTex(t, font_size=34).move_to([x, y, 0]) for t, (x, y) in zip(plain, pos)])
        nodes_t = VGroup(*[MathTex(t, font_size=32, color=PROOF).move_to([x, y, 0]) for t, (x, y) in zip(typed, pos)])

        def bar(x, y, w):
            return Line([x - w / 2, y, 0], [x + w / 2, y, 0], color=GREY_B, stroke_width=2)
        bars = VGroup(bar(-2.0, 0.88, 2.6), bar(2.0, 0.88, 2.6), bar(0, -0.17, 6.2), bar(0, -1.22, 6.4))
        rules = VGroup(*[label(t, font_size=20, color=GREY_B).next_to(b, RIGHT, buff=0.15) for t, b in zip(
            (r"$\wedge$E$_2$", r"$\wedge$E$_1$", r"$\wedge$I", r"$\to$I$^1$"), bars)])
        notes = VGroup(label(r"a hypothesis \ = \ a variable", font_size=22, color=PROOF),
                       label(r"$\wedge$-elimination \ = \ taking a pair apart", font_size=22, color=PROOF),
                       label(r"$\wedge$-introduction \ = \ building a pair", font_size=22, color=PROOF),
                       label(r"discharging a hypothesis \ = \ $\lambda$, \ making a function", font_size=22,
                             color=PROOF)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is the dictionary at work. <bookmark mark='a'/>A natural deduction proof, in Gentzen's style, that "
            "if A and B, then B and A. Assume A and B. From it, take B; from it again, take A. Put them together as "
            "B and A. Then discharge the assumption, to get the conditional. <bookmark mark='b'/>Now write beside "
            "each formula the program it corresponds to. <bookmark mark='c'/>The assumption becomes a variable, p. "
            "Taking B out of 'A and B' becomes taking the second part of the pair p. Putting B and A together "
            "becomes building a new pair. And discharging the assumption becomes lambda: a function that takes p "
            "and returns the swapped pair. <bookmark mark='d'/>The proof is the program that swaps a pair, and the "
            "formula it proves is its type."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(nodes[:2]))
            self.play(Create(bars[:2]), FadeIn(rules[:2]), FadeIn(nodes[2:4]))
            self.play(Create(bars[2]), FadeIn(rules[2]), FadeIn(nodes[4]))
            self.play(Create(bars[3]), FadeIn(rules[3]), FadeIn(nodes[5]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Transform(a, b) for a, b in zip(nodes, nodes_t)], lag_ratio=0.3), run_time=4)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(n) for n in notes], lag_ratio=0.6), run_time=4)
            vo.wait_until("d")
            self.play(Indicate(nodes[5], color=GOAL, scale_factor=1.05))
        self.clear_scene()

    def search(self):
        d = load("curry")["rows"]
        head = label(r"The Reasoner searches for programs", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        hd = [label(r"proposition", font_size=21, color=P.CLAIM), label(r"name", font_size=21, color=P.CLAIM),
              label(r"a program of that type \ (type-checked)", font_size=21, color=PROOF)]
        rows = []
        for r in d:
            prog = (term_mob(r["term"], font_size=24) if "term" in r else
                    label(r"none: \ two-world countermodel \ (Part 5)", font_size=20, color=BAD))
            rows.append([MathTex(r["tex"], font_size=24, color=WHITE if "term" in r else BAD),
                         label(r["name"], font_size=19, color=GREY_A), prog])
        grid = ValueGrid(hd, rows, col_w=[5.2, 3.2, 5.0], cell_h=0.5, font_size=21).move_to([0, -0.35, 0])
        found = sum("term" in r for r in d)
        cm = label(r"root: \ $A$ not yet proved; \ later world: \ $A$ proved", font_size=20, color=GREY_B).to_edge(
            DOWN, buff=0.22)
        with self.voiceover(
            "So the Reasoner can prove things by writing programs. <bookmark mark='a'/>Its proof search takes a "
            "proposition and looks for a program of that type, then hands the program to a small type checker "
            "to make sure. <bookmark mark='b'/>For 'if A, then if B, then A', the program takes x, ignores y, and "
            "returns x: Curry's combinator K. For the next it finds S, which feeds z to both x and y. Then swapping "
            "a pair, currying, and reasoning by cases, which becomes a case analysis on a tagged value. "
            "'A implies not not A' is the program that takes x and a refutation y, and applies y to x. "
            "<bookmark mark='c'/>The most charming is 'not not, A or not A'. Given a refutation x of 'A or not A', "
            "the program hands x a proof of 'not A'. That proof, if ever given an A, turns around and hands x the "
            "A instead. A program that changes its story when caught. <bookmark mark='d'/>But for excluded middle "
            "itself, Peirce's law, and double negation elimination, there is no program. The Reasoner finds instead "
            "the two-world Kripke model of Part 5 that refutes each one: at the root A is not yet proved, and later "
            "it is."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(found - 1)], lag_ratio=0.6),
                      run_time=8)
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*grid.cell[found - 1])))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(found, len(rows))], lag_ratio=0.5),
                      FadeIn(cm), run_time=3)
        self.clear_scene()

    def running(self):
        d = load("normal")
        head = label(r"Running a proof", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        steps = VGroup()
        for i, (s, ty) in enumerate(zip(d["steps"], d["types"])):
            row = VGroup(term_mob(s, font_size=32), MathTex(r":\ " + term_tex(ty), font_size=30, color=GREY_A))
            row.arrange(RIGHT, buff=0.3)
            steps.add(row)
        steps.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([-0.6, 0.6, 0])
        arrows = VGroup(*[MathTex(r"\rightsquigarrow", font_size=34, color=GOAL).next_to(steps[i + 1], LEFT, buff=0.3)
                          for i in range(len(steps) - 1)])
        gl = VGroup(label(r"a detour: \ build a pair, \ then at once take it apart", font_size=22, color=GREY_A),
                    label(r"each step removes one, \ and keeps the type: \ Prawitz's normalization (1965), \ "
                          r"Gentzen's cut elimination (Part 7)", font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.15).next_to(steps, DOWN, buff=0.45)
        griffin = label(r"classical logic is computational too: \ Griffin (1990): \ \texttt{call/cc}, \ a jump, \ has "
                        r"the type of Peirce's law", font_size=22, color=OK).to_edge(DOWN, buff=0.75)
        ml = label(r"add $\forall$ and $\exists$: \ Martin-Löf's dependent types \ (1972), \ the logic inside Lean "
                   r"and Coq", font_size=22, color=PROOF).to_edge(DOWN, buff=0.3)
        assert len(set(d["types"])) == 1
        with self.voiceover(
            "If proofs are programs, we can run them. <bookmark mark='a'/>Here is a proof with a detour: it proves "
            "'B and A' by first building the swap function, then at once applying it to the pair a, b. "
            "<bookmark mark='b'/>Each step of running it removes one detour. Apply the function. Take the second "
            "part of the pair, then the first. What is left is the direct proof: the pair b, a. And every step keeps "
            "the type, B and A. <bookmark mark='c'/>This is Dag Prawitz's normalization theorem of 1965 for natural "
            "deduction, Gentzen's cut elimination from Part 7 seen in another light. <bookmark mark='d'/>For decades "
            "it seemed that only constructive proofs computed. Then Timothy Griffin showed, in 1990, that the "
            "control operator call with current continuation, a jump in the program, has the type of Peirce's law. "
            "Classical proofs are programs too, with jumps. <bookmark mark='e'/>Add the quantifiers, and you get "
            "Per Martin-Löf's dependent types: the logic inside today's proof assistants, Lean and Coq, which we "
            "will meet at the end of this part."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            for i in range(1, len(steps)):
                self.play(FadeIn(arrows[i - 1]), FadeIn(steps[i], shift=DOWN * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(gl))
            vo.wait_until("d")
            self.play(FadeIn(griffin))
            vo.wait_until("e")
            self.play(FadeIn(ml))
        self.clear_scene()
