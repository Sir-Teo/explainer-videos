from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Frege's quantifiers and relations; \ scope, binding, and capture-free substitution",
            r"Tarski: truth in a structure, \ quantifier by quantifier; \ $\forall\exists$ vs $\exists\forall$ "
            r"in 343 and 169 of 512 worlds",
            r"counting, Russell's descriptions, \ and all of Aristotle inside first-order logic",
            r"Gentzen's rules; \ tableaux that close, \ or hand back a countermodel",
            r"Gödel's completeness, by Henkin's model made of names",
            r"compactness: \ no `finite', \ nonstandard numbers, \ Robinson's infinitesimals",
            r"Löwenheim--Skolem and Skolem's paradox; \ Church and Turing: \ validity is undecidable",
            r"resolution and unification; \ second-order logic; \ Lindström; \ Quine's criterion",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what this part built. <bookmark mark='a'/>Frege's language of quantifiers and relations, "
            "with its rules of scope and substitution. Tarski's definition of truth in a structure, which showed "
            "exactly how 'everyone loves someone' and 'someone is loved by everyone' differ. "
            "<bookmark mark='b'/>Counting, descriptions, and all of Aristotle's logic, inside the new one. "
            "Gentzen's rules, and trees that either close or build a counterexample. <bookmark mark='c'/>Gödel's "
            "completeness theorem, proved by a model made of words, and its consequences: compactness, nonstandard "
            "numbers, and Skolem's countable model of the uncountable. <bookmark mark='d'/>Then the wall: validity "
            "is undecidable. And beyond it, resolution provers, second-order logic, Lindström's theorem on why this "
            "logic is special, and Quine's test for what a theory says there is."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mk, idx in (("a", [1]), ("b", [2, 3]), ("c", [4, 5, 6]), ("d", [7])):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(card.rows[i], shift=RIGHT * 0.2) for i in idx], lag_ratio=0.3))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{fol.parse, show, subst}", r"first-order formulas"),
                (r"\texttt{fol.holds}", r"Tarski's satisfaction, \ with a trace"),
                (r"\texttt{fol.find\_model, countermodel}", r"finite model search"),
                (r"\texttt{fol.prove}", r"tableaux, \ countermodels from open branches"),
                (r"\texttt{fol.check\_fitch}", r"natural deduction, \ with the eigenvariable conditions"),
                (r"\texttt{fol.unify, resolution}", r"Robinson's resolution"),
                (r"\texttt{prop.*}, \ \texttt{syllogism.*}", r"Parts 1 and 2")]
        lefts = [label(a, font_size=24, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=24, color=GREY_A) for _, b in mods]
        lw = max(m.width for m in lefts)
        x0, y0 = -6.2, head.get_bottom()[1] - 0.6
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.52
            a.move_to([x0 + a.width / 2, y, 0])
            b.move_to([x0 + lw + 0.5 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked against known validities and brute force: \ \texttt{tests/philosophy/test\_fol.py}",
                      font_size=22, color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=3, current=3).scale(0.42).to_corner(DR, buff=0.3).shift(UP * 0.55)
        with self.voiceover(
            "The Reasoner has a second module, for first-order logic: formulas, Tarski's satisfaction relation, a "
            "finite model finder, a tableau prover that returns countermodels, a natural-deduction checker that "
            "enforces the conditions on fresh names, and a resolution prover with unification. "
            "<bookmark mark='a'/>Each is tested against known validities and brute force. Part 4 extends the "
            "tableau to necessity and possibility. <bookmark mark='b'/>And the Wall has its third brick: in full "
            "first-order logic, validity is undecidable."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w))
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Write `nobody loves everybody' in two equivalent ways, one starting with $\lnot\exists$, one with "
            r"$\forall$. Then write `only philosophers admire Kant'.",
            r"Find a smallest countermodel to $\forall x\,(P(x) \lor Q(x)) \models \forall x\, P(x) \lor \forall x\, "
            r"Q(x)$.",
            r"Give a Fitch proof of $\exists x\, Q(x)$ from $\forall x\,(P(x) \to Q(x))$ and $\exists x\, P(x)$. "
            r"Which line needs a new name?",
            r"Use compactness: if a sentence has finite models of every size, it has an infinite model.",
            r"Skolemize $\forall x\, \exists y\, \forall z\, \exists w\ R(x, y, z, w)$. On which variables does "
            r"each Skolem function depend?",
            r"(Essay) Plato's beard has four exits. Defend one, and say what it costs.",
        ], font_size=23)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Two on translation and "
            "countermodels, one proof with a fresh name, one on compactness, one on Skolem functions, and one for "
            "the metaphysicians. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"tableaux and countermodels", [4, 22]),
            (r"descriptions and empty names", [5, 27]),
            (r"completeness, compactness, nonstandard models", [7, 9]),
            (r"the diagonal and undecidability", [7, 8, 30]),
            (r"Löwenheim--Skolem and reference", [18, 27]),
            (r"ontological commitment", [9, 20]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 4, \textit{Necessity and Possibility}: \ possible worlds, Kripke frames, and "
                    r"modal tableaux", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>The tableau returns in Part 4 for necessity and "
            "possibility, and in Part 22 for possible worlds. Russell's descriptions return with Frege's sense and "
            "reference. Completeness and nonstandard models return in Gödel's incompleteness theorems and the "
            "philosophy of mathematics. The diagonal returns three more times: in incompleteness, in the liar, and "
            "in the argument that minds are not machines. Putnam's argument returns in Parts 18 and 27, and Quine's "
            "criterion in Parts 9 and 20. <bookmark mark='b'/>Next, Part 4: what must be, what might have been, and "
            "the logic of possible worlds."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Enderton, \textit{A Mathematical Introduction to Logic}, ch.\ 2",
             r"Boolos, Burgess \& Jeffrey, \textit{Computability and Logic} (5th ed., 2007)",
             r"Smullyan, \textit{First-Order Logic} (1968)",
             r"Ebbinghaus, Flum \& Thomas, \textit{Mathematical Logic}",
             r"Shapiro, \textit{Foundations without Foundationalism} (1991)",
             r"Sider, \textit{Logic for Philosophy}, chs.\ 4--5"],
            [r"Frege 1879; Russell, `On Denoting' (1905); Löwenheim 1915; Skolem 1920, 1922, 1934",
             r"Gödel 1930; Tarski 1933; Gentzen 1935; Church 1936; Turing 1936; Henkin 1949",
             r"Quine, `On What There Is' (1948); Carnap, `Empiricism, Semantics, and Ontology' (1950)",
             r"Robinson 1965; Lindström 1969; Putnam, `Models and Reality' (1980); Boolos 1984",
             r"McCune, `Solution of the Robbins Problem' (1997); Robinson, \textit{Non-standard Analysis} (1966)"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(2)
        self.clear_scene()
