from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"logical matrices; \ Łukasiewicz, Kleene, Bochvar; \ consequence by enumeration",
            r"K3 and LP: \ gaps and gluts, \ the same tables, \ dual logics",
            r"Belnap and Dunn's FOUR; \ the catuṣkoṭi and its fifth corner; \ the seven predications",
            r"paraconsistency and classical recapture; \ relevance; \ Gödel: \ no finite matrix for intuitionism",
            r"t-norms and a fuzzy train controller",
            r"the sorites \ (the Wall); \ supervaluations, degrees, margins for error, contexts; \ higher-order vagueness",
            r"linear logic and resources; \ quantum logic; \ logical constants; \ pluralism",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Logical matrices, and the three-valued logics of "
            "Łukasiewicz, Kleene and Bochvar, decided by writing down every row. <bookmark mark='b'/>Gaps and "
            "gluts: the same tables, opposite designated values, and an exact duality. <bookmark mark='c'/>Four "
            "values for a computer that hears conflicting reports, and the same four in Nāgārjuna's corners, with a "
            "fifth for emptiness, and the Jaina count of seven. <bookmark mark='d'/>Logics that tolerate "
            "contradiction and recapture classical reasoning where it is safe; relevance; and Gödel's proof that "
            "intuitionistic logic has no finite table. <bookmark mark='e'/>Degrees of truth, and a train that "
            "stops smoothly. <bookmark mark='f'/>The heap: this part's brick in the Wall, five theories computed "
            "side by side, and vagueness about vagueness. <bookmark mark='g'/>Resources, quantum propositions, and "
            "the question of what makes an argument logical at all."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{matrix.consequence, tautology}", r"any finite matrix: \ K3, LP, Ł3, G3, RM3, B3, FDE"),
                (r"\texttt{matrix.lpm\_consequence}", r"minimally inconsistent LP"),
                (r"\texttt{matrix.supervaluate, degree\_report}", r"the sorites, \ theory by theory"),
                (r"\texttt{matrix.fuzzy\_brake, simulate\_stop}", r"a Mamdani controller"),
                (r"\texttt{matrix.meet, join, complement}", r"the lattice of subspaces"),
                (r"\texttt{linear.prove}", r"linear logic by proof search"),
                (r"\texttt{modal.*}, \ \texttt{fol.*}, \ \texttt{prop.*}, \ \texttt{syllogism.*}", r"Parts 1--4")]
        lefts = [label(a, font_size=22, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=22, color=GREY_A) for _, b in mods]
        lw = max(m.width for m in lefts)
        x0, y0 = -6.4, head.get_bottom()[1] - 0.6
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.52
            a.move_to([x0 + a.width / 2, y, 0])
            b.move_to([x0 + lw + 0.5 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked against textbook facts: \ \texttt{tests/philosophy/test\_matrix.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=5, current=5).scale(0.4).to_corner(DR, buff=0.3).shift(UP * 0.55)
        with self.voiceover(
            "The Reasoner has two new modules. <bookmark mark='a'/>The matrix module decides consequence in any "
            "finite matrix, computes minimally inconsistent consequence, runs the sorites under each theory of "
            "vagueness, drives a fuzzy controller, and does the lattice algebra of subspaces. The linear module "
            "searches for proofs in linear logic. Each is tested against facts from the textbooks: the duality of "
            "K3 and LP, Gödel's disjunctions, the four invariant relations. <bookmark mark='b'/>And the Wall has "
            "its fifth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w))
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that K3 has no tautologies, \ and that LP has exactly the classical ones.",
            r"Is $(p \to q) \lor (q \to p)$ a tautology of K3? \ of Ł3? \ of G3? \ Explain the pattern.",
            r"Belnap's computer has $p = \mathbf{B}$ and $q = \mathbf{N}$. \ Compute $(p \land \lnot p) \lor q$ and "
            r"$\lnot(p \lor q)$.",
            r"Neither $A \otimes B \vdash A \mathbin{\&} B$ nor $A \mathbin{\&} B \vdash A \otimes B$ is provable in "
            r"linear logic. \ Which structural rule would each need?",
            r"Men 0--4; \ 0 and 1 clearly bald, \ 3 and 4 clearly not. \ Which of $B_1 \to B_2$, \ $B_2 \lor \lnot B_2$, "
            r"\ $\exists i\,(B_i \land \lnot B_{i+1})$ are super-true?",
            r"(Essay) Which exit from the sorites quartet would you take, \ and what is its second price?",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Two proofs about K3 and "
            "LP, a conditional that tells three logics apart, a query for Belnap's computer, a question about "
            "resources, a small supervaluation, and an essay on the heap. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"naive sets, \ contraction, \ and paraconsistency", [6]),
            (r"the liar: \ gaps, gluts, and revenge", [8]),
            (r"intuitionism, \ BHK, \ and proofs as programs", [9]),
            (r"degrees of belief, \ not degrees of truth", [13]),
            (r"vague objects, \ composition, \ persons", [20, 21]),
            (r"quantum logic and Kochen--Specker", [26]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 6, \textit{Paradise and Paradox}: \ sets, Russell, and the axioms", font_size=26,
                    color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Naive set theory, and the logics that might save it, in "
            "Part 6. The liar, with its gaps, gluts and revenge, in Part 8. Intuitionism in Part 9. Degrees of "
            "belief, which are not degrees of truth, in Part 13. Vague objects and persons in Parts 20 and 21. "
            "Quantum logic in Part 26. <bookmark mark='b'/>Next, Part 6: Cantor's paradise of sets, Russell's "
            "paradox, and the axioms chosen to escape it."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Priest, \textit{An Introduction to Non-Classical Logic: From If to Is} (2nd ed., 2008)",
             r"Williamson, \textit{Vagueness} (1994); \ Keefe \& Smith (eds.), \textit{Vagueness: A Reader} (1996)",
             r"Beall \& Restall, \textit{Logical Pluralism} (2006); \ Restall, \textit{An Introduction to Substructural "
             r"Logics} (2000)",
             r"Hájek, \textit{Metamathematics of Fuzzy Logic} (1998); \ Priest, \textit{The Fifth Corner of Four} (2018)"],
            [r"Łukasiewicz 1920; Post 1921; Bochvar 1938; Kleene 1938; Łoś \& Suszko 1958; Asenjo 1966; Priest 1979, 1991",
             r"Dunn 1976; Belnap 1977; Anderson \& Belnap 1975; Routley \& Meyer 1972--73; Sobociński 1952; Gödel 1932",
             r"Zadeh 1965; Yasunobu \& Miyamoto 1985; Fine 1975; Wright 1975; Sorensen 1988; Sainsbury 1990; Hyde 1997",
             r"Cobreros, Égré, Ripley \& van Rooij 2012; Girard 1987; Birkhoff \& von Neumann 1936; Putnam 1968",
             r"Tarski 1936, 1966; Etchemendy 1990; Sher 1991; Prior 1960; Belnap 1962; Ganeri 2002; Priest 2008, 2010"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(2)
        self.clear_scene()
