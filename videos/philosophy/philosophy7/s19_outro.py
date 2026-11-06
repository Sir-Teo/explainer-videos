from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Hilbert's program; \ MIU, \ and an argument \textit{about} a system",
            r"$Q$ and PA; \ recursive functions; \ Ackermann; \ Master Sun's remainders and the $\beta$-function",
            r"Gödel numbering; \ quines; \ the diagonal lemma",
            r"Gödel I, \ Rosser, \ Gödel II; \ provability logic \ (the Wall)",
            r"Turing machines; \ busy beavers to BB(5); \ the thesis; \ Rice",
            r"Ramsey and Paris--Harrington; \ Berry, \ Chaitin, \ $\Omega$; \ Tarski; \ Löb",
            r"Lucas, Penrose, \ and Gödel's disjunction; \ Gentzen and $\varepsilon_0$",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Hilbert's program, and a toy formal system whose "
            "limits we proved from outside. <bookmark mark='b'/>Arithmetic, axiom by axiom; the recursive functions "
            "it can express; and Master Sun's remainders, which let it talk about lists. <bookmark mark='c'/>Formulas "
            "as numbers, programs that print themselves, and the diagonal lemma. <bookmark mark='d'/>The two "
            "incompleteness theorems, and the modal logic that captures them. <bookmark mark='e'/>Turing machines, "
            "and the busy beavers that mark the edge of the knowable. <bookmark mark='f'/>Independence in ordinary "
            "mathematics, Berry's paradox made exact, and the theorems of Tarski and Löb. "
            "<bookmark mark='g'/>And what the theorems do, and do not, say about minds, and Gentzen's way of "
            "trusting arithmetic after all."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{arith.q\_steps, numeral}", r"Robinson's $Q$, \ step by step"),
                (r"\texttt{arith.PR, ackermann}", r"recursive functions"),
                (r"\texttt{arith.crt, beta\_code}", r"Sunzi's remainders; \ Gödel's $\beta$"),
                (r"\texttt{arith.godel\_number, godel\_decode}", r"Gödel numbering, \ both ways"),
                (r"\texttt{arith.quine\_check, diag}", r"self-reference, \ checked"),
                (r"\texttt{arith.run\_tm, busy\_beaver\_search}", r"Turing machines; \ busy beavers"),
                (r"\texttt{arith.gl\_valid}", r"provability logic on finite frames"),
                (r"\texttt{sets.*}, \ \texttt{modal.*}, \ \texttt{fol.*}, \ \dots", r"Parts 1--6")]
        lefts = [label(a, font_size=22, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=22, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.6
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.52
            a.move_to([x0 + a.width / 2, y, 0])
            b.move_to([0.6 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked against known values: \ \texttt{tests/philosophy/test\_arith.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=7, current=7).scale(0.4).to_corner(DR, buff=0.3).shift(UP * 0.55)
        with self.voiceover(
            "The Reasoner has a module for arithmetic. <bookmark mark='a'/>It runs Robinson's Q, builds recursive "
            "functions, solves Master Sun's problem and codes lists with Gödel's beta, numbers and unnumbers "
            "formulas, runs a quine and checks the diagonal sentence, simulates Turing machines up to the five-state "
            "champion, and checks provability logic on finite frames. Its tests compare it with the published "
            "values: the busy beaver numbers, the Ramsey number, and Sunzi's twenty-three. "
            "<bookmark mark='b'/>And the Wall has its seventh brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[7], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Derive \texttt{MIIIII} \ (five I's) \ in MIU; \ then show that \texttt{MUIIIU} is not a theorem.",
            r"Using $Q$'s axioms only, \ derive $1 \times 2 = 2$, \ naming the axiom at each step.",
            r"Find the least $x$ with $x \equiv 1 \pmod 4$, \ $x \equiv 2 \pmod 5$, \ $x \equiv 3 \pmod 7$; \ then "
            r"code the list $1, 2, 3$ with $\beta$.",
            r"Prove from the derivability conditions that $\mathrm{PA} \vdash \mathrm{Con}(\mathrm{PA}) \to G$.",
            r"Use Rice's theorem to show that no program decides whether two programs compute the same function.",
            r"(Essay) Does Gödel's theorem show that minds are not machines? \ Defend an answer against Lucas or "
            r"against Benacerraf.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>A puzzle in MIU, a "
            "derivation in Q, a Chinese remainder problem with its beta code, the formalized first theorem, an "
            "application of Rice, and an essay on minds and machines. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the liar, \ and truth predicates that survive it", [8]),
            (r"what mathematics is about, \ after Gödel", [9]),
            (r"minds, machines, \ and the Chinese room", [30]),
            (r"Kolmogorov complexity and induction: \ Solomonoff", [15]),
            (r"agents that trust themselves: \ the Löbian obstacle", [42]),
            (r"computation in physics", [26]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 8, \textit{The Liar}: \ truth and paradox", font_size=26,
                    color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>The liar, and the theories of truth built to survive it, "
            "in Part 8. What mathematics is about, after Gödel, in Part 9. Minds and machines again in Part 30. "
            "Kolmogorov complexity becomes a theory of induction in Part 15. Löb's theorem returns at the very end, "
            "in Part 42, as an obstacle for agents that must trust their own reasoning. And computation in physics, "
            "in Part 26. <bookmark mark='b'/>Next, Part 8: the liar."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Smith, \textit{An Introduction to Gödel's Theorems} (2nd ed., 2013); \ Franzén, \textit{Gödel's "
             r"Theorem} (2005)",
             r"Boolos, Burgess \& Jeffrey, \textit{Computability and Logic} (5th ed., 2007), chs.\ 15--18",
             r"Boolos, \textit{The Logic of Provability} (1993); \ Hofstadter, \textit{Gödel, Escher, Bach} (1979)",
             r"Aaronson, `The busy beaver frontier' (2020); \ Li \& Vitányi, \textit{Kolmogorov Complexity} (2008)"],
            [r"Hilbert 1926, 1930; Hilbert \& Ackermann 1928; Ackermann 1928; Ramsey 1930; Gödel 1931, 1951",
             r"Tarski 1933; Carnap 1934; Turing 1936, 1947; Church 1936; Rosser 1936; Gentzen 1936, 1943; Kleene 1938",
             r"Hilbert \& Bernays 1939; Robinson 1950; Henkin 1952; Rice 1953; Löb 1955; Lucas 1961; Radó 1962",
             r"Benacerraf 1967; Chaitin 1974, 1975; de Jongh 1975; Solovay 1976; Paris \& Harrington 1977",
             r"Kirby \& Paris 1982; Brady 1983; Marxen \& Buntrock 1989; Yedidia \& Aaronson 2016; bbchallenge 2024"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
