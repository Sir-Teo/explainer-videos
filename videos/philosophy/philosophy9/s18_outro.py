from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"the Meno; \ platonism; \ Benacerraf's access problem; \ Field's reliability challenge",
            r"Frege's numbers, \ built; \ Frege's theorem; \ Hume's principle needs infinity; \ bad company",
            r"formalism and Bombelli's $\sqrt{-1}$; \ Hilbert's ideal elements; \ Brouwer and the weak counterexamples",
            r"Curry--Howard, \ built: \ proof search, \ type checking, \ running a proof",
            r"the vicious circle and the typical Englishman; \ structuralism; \ $i$ and $-i$ \ (the Wall)",
            r"indispensability and the cicadas; \ Field's representation theorem; \ the Price List",
            r"univalence; \ Lakatos; \ pictures that prove and lie; \ proofs by machine",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>The boy in the Meno, platonism, and the problem of how "
            "we could know abstract objects. <bookmark mark='b'/>Frege's numbers, built on a world of four objects; "
            "Frege's theorem; the discovery that Hume's principle needs infinitely many things; and bad company. "
            "<bookmark mark='c'/>Mathematics as a game, Bombelli's impossible numbers, Hilbert's ideal elements, and "
            "Brouwer's mathematics of construction. <bookmark mark='d'/>Proofs as programs, searched for, checked "
            "and run. <bookmark mark='e'/>The vicious circle, structuralism, and the puzzle of i and minus i. "
            "<bookmark mark='f'/>The argument from science, the cicadas, Field's numbers recovered from points, and "
            "the Price List. <bookmark mark='g'/>And mathematics in practice: a new foundation, proofs and "
            "refutations, pictures, and machines."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{types.prove, type\_of}", r"proof search as program search; \ a forty-line kernel"),
                (r"\texttt{types.normalize, transport\_check}", r"running proofs; \ carrying a property across"),
                (r"\texttt{types.countermodel, winding\_number}", r"Kripke countermodels; \ loops on a circle"),
                (r"\texttt{mathphil.frege\_numbers, abstraction\_demands}", r"Hume's principle and its company"),
                (r"\texttt{mathphil.pi\_digits, goldbach\_checked}", r"Brouwer's examples"),
                (r"\texttt{mathphil.typical, automorphisms}", r"the vicious circle; \ structure and symmetry"),
                (r"\texttt{mathphil.representations, euler}", r"Field's points; \ Lakatos's polyhedra"),
                (r"\texttt{truth.*}, \ \texttt{arith.*}, \ \texttt{sets.*}, \ \dots", r"Parts 1--8")]
        lefts = [label(a, font_size=21, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=21, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.55
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.52
            a.move_to([x0 + a.width / 2, y, 0])
            b.move_to([1.2 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_types.py}", font_size=22, color=GREY_B).to_edge(
            DOWN, buff=0.4)
        w = wall(upto=9, current=9).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has two new modules. <bookmark mark='a'/>One treats propositions as types: it searches for "
            "proofs as programs and checks them with a forty-line kernel, runs proofs to normal form, carries a "
            "property across an equivalence, finds Kripke countermodels, and counts the turns of loops. The other "
            "builds Frege's numbers and counts what abstraction principles demand, computes pi and checks Goldbach, "
            "builds Russell's typical Englishman, finds the symmetries of structures, recovers coordinates from "
            "points, and counts Euler's polyhedra. <bookmark mark='b'/>And the Wall has its ninth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[9], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"On a domain of five objects: \ how many concepts, \ how many numbers, \ and how many concepts in each? \ "
            r"Why can Hume's principle not hold there?",
            r"Show that Basic Law V has no model of any size, \ and that Hume's principle has one on $\{0, 1, 2, "
            r"\dots\}$.",
            r"Find a program of type \ $(A \to B) \to (B \to C) \to A \to C$, \ and a two-world countermodel to "
            r"$((A \to B) \to A) \to A$.",
            r"Why can `$r = 0$ or $r \neq 0$' not be asserted constructively for Brouwer's $r$? \ Why must a "
            r"computable function on the reals be continuous?",
            r"Which points of a path of four points can structure alone pick out? \ Find a symmetry of the square "
            r"that fixes no corner.",
            r"(Essay) Which exit from the Benacerraf--Field Price List? \ Defend it against its strongest objection.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Frege's numbers on five "
            "objects; Basic Law Five and Hume's principle; a program and a countermodel; Brouwer's real number and "
            "continuity; symmetries of small structures; and an essay on the Price List. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the a priori, \ and Kant's synthetic a priori", [10]),
            (r"Quine's web of belief, \ and holism", [11, 15]),
            (r"abstract objects, \ and what there is", [20]),
            (r"identity and indiscernibility", [21]),
            (r"knowing what is possible", [22]),
            (r"machines that reason, \ and whether to trust them", [30, 42]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 10, \textit{The Mind's Own Laws}", font_size=26, color=P.CONCL).to_edge(DOWN,
                                                                                                         buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>The a priori, and Kant's synthetic a priori, in Part 10. "
            "Quine's web of belief, in Parts 11 and 15. Abstract objects and the question of what there is, in Part "
            "20. Identity and indiscernibility, in Part 21. Knowledge of possibility, in Part 22. And machines that "
            "reason, and whether to trust them, in Parts 30 and 42. <bookmark mark='b'/>This ends the second act, "
            "on the limits of reason. Next, Part 10 opens the act on knowledge: the mind's own laws, from Descartes "
            "to Kant."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Shapiro, \textit{Thinking about Mathematics} (2000); \ Linnebo, \textit{Philosophy of Mathematics} "
             r"(2017)",
             r"Benacerraf \& Putnam (eds.), \textit{Philosophy of Mathematics: Selected Readings} (1964, 1983)",
             r"Hale \& Wright, \textit{The Reason's Proper Study} (2001); \ Colyvan, \textit{The Indispensability of "
             r"Mathematics} (2001)",
             r"Lakatos, \textit{Proofs and Refutations} (1976); \ the HoTT Book (2013); \ Sørensen \& Urzyczyn, "
             r"\textit{Lectures on the Curry--Howard Isomorphism} (2006)"],
            [r"Frege 1884; Hilbert 1899, 1925; Brouwer 1907; Poincaré 1906; Weyl 1918; Gödel 1944, 1964; Curry \& Feys "
             r"1958",
             r"Benacerraf 1965, 1973; Howard 1969/1980; Putnam 1971; Wright 1983; Boolos 1987, 1997; Field 1980, 1989",
             r"Hellman 1989; Maddy 1990, 1992; Griffin 1990; Shapiro 1997, 2008; Keränen 2001; Baker 2005; Ladyman 2005",
             r"Steiner 1978; Tymoczko 1979; Thurston 1994; Pollack 1998; Manders 2008; Licata \& Shulman 2013; "
             r"Avigad 2024"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
