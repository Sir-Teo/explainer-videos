from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"the skeptical crisis; \ Descartes's doubt, \ the cogito, \ the circle",
            r"coordinates, \ and the method of normals, \ built",
            r"Spinoza's \textit{Ethics} as a proof graph: \ no circles, \ a ten-step chain, \ two idle axioms",
            r"Leibniz: \ finite and infinite analysis; \ least time; \ monads",
            r"Locke, \ Molyneux's question answered in 2011, \ Berkeley",
            r"Hume: \ ideas, \ the fork, \ causation, \ induction, \ the self",
            r"Kant: \ the grid, \ space and time, \ categories, \ antinomies \ (the Wall); \ after Kant; \ Hegel",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>The skeptical crisis, and Descartes's way out of it, "
            "with its circle. <bookmark mark='b'/>Coordinates, and Descartes's method of normals, solved by algebra. "
            "<bookmark mark='c'/>Spinoza's Ethics, read by the Reasoner as a graph of proofs. <bookmark mark='d'/>"
            "Leibniz's two kinds of truth, and nature's easiest path. <bookmark mark='e'/>Locke, a question about "
            "the newly sighted that took three centuries to test, and Berkeley. <bookmark mark='f'/>Hume's fork, "
            "his analysis of cause, and the problem of induction. <bookmark mark='g'/>And Kant's answer, its price, "
            "and what became of it."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{modern.parse\_ethics, ethics\_graph}", r"Spinoza's citations, \ read from the text"),
                (r"\texttt{modern.longest\_chain, unused}", r"depth, \ chains, \ idle axioms"),
                (r"\texttt{modern.descartes\_normal}", r"the method of normals, \ by computer algebra"),
                (r"\texttt{modern.continued\_fraction, sqrt\_cf}", r"Leibniz's finite and infinite analysis"),
                (r"\texttt{modern.least\_time, light\_bending}", r"Snell's law; \ Eddington's test"),
                (r"\texttt{modern.rival\_rules, spherical\_excess}", r"Hume's problem; \ Gauss's triangle"),
                (r"\texttt{types.*}, \ \texttt{mathphil.*}, \ \texttt{truth.*}, \ \dots", r"Parts 1--9")]
        lefts = [label(a, font_size=21, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=21, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.55
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.55
            a.move_to([x0 + a.width / 2, y, 0])
            b.move_to([1.0 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_modern.py}", font_size=22, color=GREY_B).to_edge(
            DOWN, buff=0.4)
        w = wall(upto=10, current=10).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has a module for the early moderns. <bookmark mark='a'/>It reads Spinoza's citations from "
            "the text and analyses the graph they make; solves Descartes's tangent problem by computer algebra; runs "
            "Euclid's algorithm to the end, or forever; finds the path of least time; computes Eddington's "
            "prediction and Gauss's excess; and writes down rules that fit the past and disagree about the future. "
            "<bookmark mark='b'/>And the Wall has its tenth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[10], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"In the graph of \textit{Ethics} I, \ which definitions, axioms and propositions does Proposition 14 "
            r"ultimately rest on?",
            r"Run Euclid's algorithm on $1071/462$ and on $\sqrt{3}$. \ Which analysis ends? \ What would Leibniz say?",
            r"By Descartes's method, \ find the centre on the $y$-axis of the circle touching $y = x^2$ at $(2, 4)$.",
            r"Write two rules that agree about every past sunrise \ and disagree about tomorrow. \ Why, for Hume, "
            r"can no argument choose?",
            r"Place in Kant's grid: \ `every effect has a cause'; \ `every event has a cause'; \ `a straight line is "
            r"the shortest between two points'.",
            r"(Essay) Which exit from the empiricist trilemma? \ Defend it against its strongest objection.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Spinoza's graph; Leibniz's "
            "two analyses; Descartes's method; Hume's rival rules; Kant's grid; and an essay on the Price List. "
            "Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"what knowledge is, \ and the web of belief", [11]),
            (r"the problem of induction", [15]),
            (r"cause and law", [17, 24]),
            (r"personal identity and the bundle", [21]),
            (r"space and time after Kant", [25]),
            (r"freedom and necessity", [32]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 11, \textit{What Is Knowledge?}", font_size=26, color=P.CONCL).to_edge(DOWN,
                                                                                                     buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>What knowledge is, and Quine's web of belief, in Part 11. The "
            "problem of induction, in Part 15. Cause and law, in Parts 17 and 24. The self as a bundle, in Part 21. "
            "Space and time after Kant, in Part 25. And Spinoza's freedom as understood necessity, in Part 32. "
            "<bookmark mark='b'/>Next, Part 11: what is knowledge?"
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Descartes, \textit{Meditations} (1641); \ Spinoza, \textit{Ethics} (1677; Curley and Elwes trans.); \ "
             r"Leibniz, \textit{Monadology} (1714)",
             r"Locke, \textit{Essay} (1689); \ Berkeley, \textit{Principles} (1710); \ Hume, \textit{Treatise} (1739) "
             r"and \textit{Enquiry} (1748)",
             r"Kant, \textit{Critique of Pure Reason} (1781, 1787; Guyer and Wood trans.); "
             r"\textit{Prolegomena} (1783)",
             r"Gardner, \textit{Kant and the Critique of Pure Reason} (1999); \ Allison, \textit{Kant's Transcendental "
             r"Idealism} (1983)"],
            [r"Sextus Empiricus, \textit{Outlines}; Montaigne 1580; Galileo 1610; Descartes 1637; Arnauld 1641",
             r"Fermat 1662; Leibniz 1682; Molyneux 1688; Held et al.\ 2011; Lobachevsky 1829; Bolyai 1832",
             r"Riemann 1854; Einstein 1915; Dyson, Eddington \& Davidson 1920; Reichenbach 1920; Strawson 1966",
             r"Langton 1998; Friedman 2001; Lawvere 1996; Priest 1987; Hegel 1807, 1812--16"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
