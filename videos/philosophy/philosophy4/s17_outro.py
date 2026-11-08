from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Aristotle's sea battle; \ Diodorus's master argument and its three exits",
            r"Lewis's strict implication; \ K, T, S4, S5; \ S4's 14 modalities = Kuratowski's 14",
            r"Kripke: \ necessity is truth in every accessible world",
            r"axioms are frame conditions: \ T, D, B, 4, 5, checked on all 65,536 frames of 4 worlds",
            r"Löb's axiom: \ no first-order frame condition \ (the Wall); \ Sahlqvist; \ canonical models",
            r"bisimulation and van Benthem; \ filtration and decidability",
            r"the Barcan formula; \ Chisholm's paradox; \ branching time",
            r"LTL, CTL, \ a model checker for Peterson's algorithm; \ Hoare and dynamic logic",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>The ancient puzzles: the sea battle and the master "
            "argument. Lewis's strict implication, the modern systems, and the fourteen modalities of S4. "
            "<bookmark mark='b'/>Kripke's semantics, and the exact match between axioms and shapes of arrows, "
            "checked on every frame of up to four worlds. <bookmark mark='c'/>Then the wall: Löb's axiom has no "
            "first-order frame condition. Canonical models, bisimulation, filtration, and decidability. "
            "<bookmark mark='d'/>The Barcan formula, obligation, and time. And temporal logic in industry, with our "
            "own model checker verifying Peterson's algorithm and catching its broken twin."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mk, idx in (("a", [1]), ("b", [2, 3]), ("c", [4, 5]), ("d", [6, 7])):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(card.rows[i], shift=RIGHT * 0.2) for i in idx], lag_ratio=0.3))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{modal.parse, holds}", r"Kripke models, \ tense operators"),
                (r"\texttt{modal.valid\_on\_frame, correspondence}", r"axioms against frame conditions"),
                (r"\texttt{modal.find\_model}", r"satisfiability in a class of frames"),
                (r"\texttt{modal.bisimulation, minimize}", r"what modal logic cannot see"),
                (r"\texttt{modal.System, ctl\_eu, ctl\_eg, fair\_eg}", r"explicit-state model checking"),
                (r"\texttt{fol.*}, \ \texttt{prop.*}, \ \texttt{syllogism.*}", r"Parts 1--3")]
        lefts = [label(a, font_size=22, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=22, color=GREY_A) for _, b in mods]
        lw = max(m.width for m in lefts)
        x0, y0 = -6.2, head.get_bottom()[1] - 0.6
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.55
            a.move_to([x0 + a.width / 2, y, 0])
            b.move_to([x0 + lw + 0.5 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked against counts known from the literature: \ \texttt{tests/philosophy/test\_modal.py}",
                      font_size=22, color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=4, current=4).scale(0.42).to_corner(DR, buff=0.3).shift(UP * 0.55)
        with self.voiceover(
            "The Reasoner has a third module, for modal logic: Kripke models, an exhaustive checker of axioms "
            "against frames, a model finder, bisimulation, and an explicit-state model checker with fairness. "
            "<bookmark mark='a'/>Each is tested against numbers known from the literature: fourteen modalities, one "
            "hundred and seventy-one transitive relations on three points, two hundred and nineteen partial orders "
            "on four. <bookmark mark='b'/>And the Wall has its fourth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w))
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that B, $p \to \Box\Diamond p$, is valid on exactly the symmetric frames.",
            r"Show that in S5, $\Diamond\Box p \to \Box p$ is valid. Which axiom does the work?",
            r"Draw a frame on which $\Box p \to \Box\Box p$ fails, with as few worlds as possible.",
            r"Find two non-isomorphic models that are bisimilar, one of them with a cycle and one without.",
            r"Write `the light is never green in both directions' and `every request is eventually granted' in LTL.",
            r"(Essay) Which exit from the master argument would you take, and what does it say `possible' means?",
        ], font_size=23)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Two correspondence proofs, "
            "a countermodel, a pair of bisimilar models, two specifications in temporal logic, and one for Diodorus. "
            "Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"knowledge as a modality, \ introspection", [11, 12]),
            (r"provability logic GL", [7]),
            (r"possible worlds, rigid designators, essence", [22]),
            (r"branching time and foreknowledge", [23]),
            (r"deontic logic and conditional obligation", [35, 41]),
            (r"specification and verification", [42]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 5, \textit{Beyond True and False}: \ many values, gaps, gluts, and vagueness",
                    font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Knowledge as a modality, and the debate over introspection, "
            "in Parts 11 and 12. Provability logic in Part 7. Possible worlds, rigid designators and essence in Part "
            "22. Branching time and divine foreknowledge in Part 23. Obligation in ethics and in fair machines. And "
            "specification, at the very end. <bookmark mark='b'/>Next, Part 5: logics with more than two truth "
            "values, sentences that are neither true nor false, and the paradox of the heap."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Hughes \& Cresswell, \textit{A New Introduction to Modal Logic} (1996)",
             r"Blackburn, de Rijke \& Venema, \textit{Modal Logic} (2001), chs.\ 1--4",
             r"Sider, \textit{Logic for Philosophy}, ch.\ 6",
             r"Baier \& Katoen, \textit{Principles of Model Checking} (2008)",
             r"Boolos, \textit{The Logic of Provability} (1993)"],
            [r"Aristotle, \textit{De Interpretatione} 9; Epictetus, \textit{Discourses} II.19; Lewis 1912, 1932",
             r"Kripke 1959, 1963; Barcan 1946, 1947; McKinsey \& Tarski 1944; Prior 1957, 1967",
             r"Löb 1955; Solovay 1976; Sahlqvist 1975; Goldblatt \& Thomason 1975; van Benthem 1976; Ladner 1977",
             r"von Wright 1951; Ross 1941; Chisholm 1963; Floyd 1967; Hoare 1969; Pratt 1976",
             r"Pnueli 1977; Clarke \& Emerson 1981; Queille \& Sifakis 1982; Peterson 1981; Newcombe et al.\ 2015"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(2)
        self.clear_scene()
