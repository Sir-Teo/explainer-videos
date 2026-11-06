from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"de re and de dicto, \ Quine's three grades, \ and the cyclist on a model",
            r"descriptions and rigid names; \ the modal, \ epistemic and semantic arguments; \ the causal chain",
            r"Hesperus, \ Twin Earth and the standard metre: \ necessity and the \textit{a priori} come apart",
            r"Lewis's plurality, \ `actual' as an indexical, \ propositions as sets of worlds",
            r"counterpart theory translated, \ and every small model checked against Kripke's semantics",
            r"ersatz books and alien properties; \ the Barcan formula and necessitism",
            r"conceivability; \ the two-dimensional matrix \ (the Wall); \ Pierre \ (a Price List); \ Fine on "
            r"essence",
            r"counterpossibles; \ finks and masks; \ counterfactual explanations and ProbLog",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>The distinction between necessity de dicto and de re, "
            "Quine's objection, and his cyclist on a model. <bookmark mark='b'/>Kripke's rigid names, and three "
            "arguments against the description theory. <bookmark mark='c'/>Necessity and a priority prised apart, in "
            "both directions. <bookmark mark='d'/>Lewis's concrete worlds, with actuality as an indexical and "
            "propositions as sets of worlds. <bookmark mark='e'/>Counterpart theory, translated into first-order "
            "logic and checked on every small model. <bookmark mark='f'/>Ersatz worlds, alien properties, and "
            "Williamson's necessitism. <bookmark mark='g'/>Conceivability, the two-dimensional matrix and this part's "
            "brick in the Wall, Kripke's Pierre, and Fine's essences. <bookmark mark='h'/>And impossible worlds, "
            "dispositions, and possible worlds at work in machine learning and probabilistic programming."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{worlds.kholds, holds\_cp}", r"Kripke and Lewis semantics"),
                (r"\texttt{worlds.translate, fo\_holds}", r"Lewis's 1968 translation"),
                (r"\texttt{worlds.census}", r"every small model"),
                (r"\texttt{worlds.twod, matrix\_2d}", r"two dimensions"),
                (r"\texttt{worlds.alien\_properties, barcan, essence}", r"ersatz; \ necessitism; \ Fine"),
                (r"\texttt{worlds.counterpossibles, dispositions}", r"impossible worlds; \ finks"),
                (r"\texttt{worlds.counterfactual\_explanation}", r"closest worlds"),
                (r"\texttt{worlds.distribution\_semantics}", r"ProbLog"),
                (r"\texttt{persist.*}, \ \texttt{mereo.*}, \ \texttt{dl.*}, \ \dots", r"Parts 1--21")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.5
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.5
            if a.width > 7.6:
                a.width = 7.6
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.2:
                b.width = 4.2
            b.move_to([1.9 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_worlds.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=22, current=22).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has a new module, worlds. <bookmark mark='a'/>It evaluates quantified modal logic in "
            "Kripke's semantics and in Lewis's, translates modal sentences into counterpart theory, checks every "
            "small model, fills two-dimensional matrices, counts ersatz descriptions, tests the Barcan formula and "
            "the modal account of essence, evaluates counterpossibles and dispositions, and searches for the "
            "closest world where a decision flips, or sums probabilities over worlds. <bookmark mark='b'/>And the "
            "Wall has its twenty-second brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[22], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that `the number of planets is necessarily odd' is false de dicto. \ Is it true de re?",
            r"Translate $\Box \exists x\, Fx \to \exists x\, \Box Fx$ into counterpart theory. \ Find a countermodel.",
            r"Build a counterpart model where the 4 axiom fails, \ with one individual per world.",
            r"Fill the two-dimensional matrix of `Julius invented the zip'. \ Which box does it belong in?",
            r"Pierre's puzzle: \ which principle does a Fregean give up, \ and what does it cost?",
            r"Give a counterpossible about logic that seems false, \ and say which impossible world decides it.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>A de re and de dicto "
            "exercise; a translation into counterpart theory, with a countermodel; a counterpart model breaking the "
            "four axiom; a two-dimensional matrix for Evans's Julius; the Fregean's price in Pierre's puzzle; and a "
            "counterpossible of your own. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"God's necessary existence; \ the modal ontological argument", [23]),
            (r"necessary laws, \ chance, \ and the open future", [24, 25]),
            (r"Everett's branching worlds", [26]),
            (r"names, \ descriptions and the meaning of `meaning'", [27, 28]),
            (r"conceivability, \ zombies and the mind", [30, 31]),
            (r"free will and alternative possibilities", [32]),
            (r"possible people; \ counterfactual fairness", [36, 41]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 23, \textit{God and the Philosophers}", font_size=26, color=P.CONCL).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>The modal ontological argument for God's existence, in Part "
            "23. Necessary laws, chance and the open future, in Parts 24 and 25. Everett's branching worlds in "
            "quantum mechanics, in Part 26. Names and meaning, in Parts 27 and 28. Conceivability and zombies, in "
            "Parts 30 and 31. Alternative possibilities and free will, in Part 32. And possible people, who might "
            "or might not be brought into existence, and counterfactual fairness, in Parts 36 and 41. "
            "<bookmark mark='b'/>Next, Part 23: God and the philosophers."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Kripke, \textit{Naming and Necessity} (1980); \ Lewis, \textit{On the Plurality of Worlds} (1986)",
             r"Williamson, \textit{Modal Logic as Metaphysics} (2013); \ Menzel, `Possible Worlds', "
             r"\textit{Stanford Encyclopedia} (2021)",
             r"Chalmers, `The Foundations of Two-Dimensional Semantics' (2006); \ Gendler and Hawthorne (eds.), "
             r"\textit{Conceivability and Possibility} (2002)",
             r"Berto and Jago, \textit{Impossible Worlds} (2019); \ Fine, `Essence and Modality' (1994)"],
            [r"Barcan 1946; Quine 1953, 1960; Prior 1956; Kripke 1963, 1970, 1979; Lewis 1968, 1973, 1997",
             r"Plantinga 1974; Stalnaker 1968, 1976, 1978; Putnam 1975; Evans 1973, 1979; Davies and Humberstone 1980",
             r"Forrest and Armstrong 1984; Armstrong 1989; Yablo 1993; Martin 1994; Nolan 1997; Bird 1998, 2007",
             r"Sato 1995; De Raedt et al. 2007; Wachter et al. 2017; Kusner et al. 2017; Ustun et al. 2019"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
