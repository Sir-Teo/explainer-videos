from __future__ import annotations

from videos.philosophy.philosophy2.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Boole: logic as algebra; \ $x^2 = x$ gives two truth values",
            r"formulas are trees; \ sixteen binary connectives; \ nand alone is enough; \ Post's five classes",
            r"validity is truth preserved in every valuation: \ decidable by tables, at $2^n$ rows",
            r"normal forms; \ Tseitin's linear encoding; \ Horn clauses are easy",
            r"natural deduction; \ soundness and completeness: \ $\vdash$ and $\models$ agree",
            r"resolution, DPLL, CDCL: \ the solvers inside industry",
            r"SAT is NP-complete; \ pigeonhole proofs are exponential for resolution",
            r"the elenchus as SAT: \ minimal correction sets are the positions",
        ]
        card = objectives_card(items, title=r"What we built", font_size=25)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Boole wrote logic as algebra, and his law x squared "
            "equals x gave logic its two values. Formulas are trees; there are sixteen ways to connect two sentences, "
            "and one, nand, is enough for all of them, by Post's criterion. <bookmark mark='b'/>Validity is truth "
            "preserved in every valuation, decidable by truth tables, at a cost of two to the n rows. Normal forms "
            "turn every question into a list of clauses. <bookmark mark='c'/>Natural deduction gives proofs a machine "
            "can check, and soundness and completeness say that proof and truth agree exactly. <bookmark mark='d'/>"
            "Resolution, DPLL and clause learning are the solvers inside industry. SAT is NP-complete, and some "
            "obvious truths have only enormous proofs. And Socrates' method, run as SAT, lists every way out of a "
            "contradiction."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mk, idx in (("a", [1]), ("b", [2, 3]), ("c", [4]), ("d", [5, 6, 7])):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(card.rows[i], shift=RIGHT * 0.2) for i in idx], lag_ratio=0.3))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{prop.parse, show, evaluate}", r"formulas as trees"),
                (r"\texttt{truth\_table, entails}", r"validity, with countermodels"),
                (r"\texttt{post\_complete}", r"Post's criterion"),
                (r"\texttt{cnf\_clauses, tseitin}", r"normal forms"),
                (r"\texttt{check\_fitch}", r"natural deduction, checked"),
                (r"\texttt{resolution\_refute, dpll, cdcl}", r"the solvers"),
                (r"\texttt{mus\_mcs, hitting\_sets}", r"the Price List engine")]
        rows = VGroup(*[VGroup(label(a, font_size=24, color=P.WORLD), label(b, font_size=24, color=GREY_A)).arrange(
            RIGHT, buff=0.5) for a, b in mods]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN,
                                                                                               buff=0.4)
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.5)
        tests = label(r"every algorithm checked against brute force: \ \texttt{tests/philosophy/test\_prop.py}",
                      font_size=22, color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=2, current=2).scale(0.5).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner now has its first module: formulas, tables, normal forms, a proof checker, three solvers, "
            "and the Price List engine, each tested against brute force. <bookmark mark='a'/>Every later part adds "
            "to it, and Part 39 will use this very SAT solver to check a case of Arrow's theorem about voting. "
            "<bookmark mark='b'/>And the Wall has its second brick: the price of calculation."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w))
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that $\{\to, \bot\}$ is functionally complete. Is $\{\lor, \to\}$? Use Post's criterion.",
            r"Give a Fitch proof of $(p \to q) \to ((q \to r) \to (p \to r))$.",
            r"How many clauses does Tseitin's encoding produce for a formula with $k$ binary connectives, none "
            r"of them $\leftrightarrow$? With $m$ of them $\leftrightarrow$?",
            r"On another island, A says `B is a knave' and B says `A and C are of the same kind'. What can you "
            r"conclude about A? About C?",
            r"Prove one half of Reiter's duality: every minimal correction set meets every minimal unsatisfiable "
            r"subset.",
            r"(Essay) In \textit{Republic} I Socrates gives up both definitions. Make the best case for a "
            r"different exit from one of the two contradictions.",
        ], font_size=23)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Two on connectives and "
            "proofs, one on encodings, one more island, one half of Reiter's theorem, and one to argue with Socrates. "
            "Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"SAT and the Price List", [5, 23, 30, 32, 39]),
            (r"completeness and compactness", [3, 7]),
            (r"double negation and intuitionism", [9]),
            (r"the conditional as a truth function", [14]),
            (r"Horn rules and forward chaining", [14, 20]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 3, \textit{All and Some}: \ quantifiers, models, and the first limits",
                    font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>The SAT solver and the Price List return in the sorites, "
            "the problem of evil, the mind and body, free will, and Arrow's theorem. Completeness and compactness "
            "return in Parts 3 and 7. The double-negation rule is where Part 9's intuitionists get off. Philo's "
            "conditional is cross-examined in Part 14. <bookmark mark='b'/>And next, in Part 3, we open up the atoms: "
            "'all', 'some', relations and models, Gödel's completeness theorem, and the first result that no "
            "calculation can get around."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Enderton, \textit{A Mathematical Introduction to Logic}, ch.\ 1",
             r"van Dalen, \textit{Logic and Structure}, chs.\ 1--2",
             r"Sider, \textit{Logic for Philosophy}, ch.\ 2",
             r"Biere, Heule, van Maaren \& Walsh (eds.), \textit{Handbook of Satisfiability} (2nd ed., 2021)",
             r"Kneale \& Kneale, \textit{The Development of Logic}"],
            [r"Boole 1854; Sheffer 1913; Post 1921, 1941; Gentzen 1935; Tseitin 1968",
             r"Davis \& Putnam 1960; Davis, Logemann \& Loveland 1962; Robinson 1965",
             r"Cook 1971; Cook \& Reckhow 1979; Haken 1985; Marques-Silva \& Sakallah 1996",
             r"Reiter 1987; Liffiton \& Sakallah 2008; Heule, Kullmann \& Marek 2016",
             r"Mackie 1955; Plantinga, \textit{God, Freedom, and Evil} (1974); Tymoczko 1979"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(2)
        self.clear_scene()
