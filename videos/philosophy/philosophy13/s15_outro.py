from __future__ import annotations

from videos.philosophy.philosophy13.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"credences as points; \ Kolmogorov's axioms; \ the simplex",
            r"the Dutch book, \ found by an LP, \ proved by a separating hyperplane",
            r"accuracy dominance; \ proper scoring rules; \ calibration",
            r"conditionalization, \ diachronic books, \ Jeffrey's rule; \ priors and MaxEnt",
            r"Bertrand's chords \ (the Wall); \ chance and the Principal Principle; \ imprecise credence",
            r"the lottery and the preface; \ stable belief; \ Sleeping Beauty; \ Doomsday",
            r"Bayesian networks, \ and what exact inference costs",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Credences as points, and the axioms as a simplex. "
            "<bookmark mark='b'/>The Dutch book, found by a linear program and proved by a separating hyperplane. "
            "<bookmark mark='c'/>Accuracy, and the proper scores that make honesty pay. <bookmark mark='d'/>How to "
            "update, and where to start. <bookmark mark='e'/>Bertrand's chords, this part's brick in the Wall; "
            "chance; and imprecision. <bookmark mark='f'/>Belief and credence; Sleeping Beauty; and the Doomsday "
            "argument. <bookmark mark='g'/>And Bayesian machines, with their costs."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{credence.dutch\_book, coherent}", r"the sure-loss LP"),
                (r"\texttt{credence.dominance, project\_simplex}", r"accuracy dominance"),
                (r"\texttt{credence.score, best\_report, forecasters}", r"proper scores; \ calibration"),
                (r"\texttt{credence.diachronic\_book, jeffrey, maxent\_die}", r"updating; \ priors"),
                (r"\texttt{credence.bertrand, cube\_factory, dilation}", r"indifference; \ imprecision"),
                (r"\texttt{credence.stable\_sets, sleeping\_beauty, doomsday}", r"belief; \ self-location"),
                (r"\texttt{epistemic.*}, \ \texttt{knowledge.*}, \ \dots", r"Parts 1--12")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.55
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.55
            if a.width > 7.2:
                a.width = 7.2
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.6:
                b.width = 4.6
            b.move_to([1.6 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_credence.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=13, current=13).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has a credence laboratory. <bookmark mark='a'/>The Dutch book program; projection onto "
            "the simplex; scoring rules and synthetic forecasters; diachronic books, Jeffrey's rule and maximum "
            "entropy; Bertrand's chords, the cube factory and dilation; stable sets, Sleeping Beauty and the "
            "Doomsday calculation. <bookmark mark='b'/>And the Wall has its thirteenth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[13], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"$A$ and $B$ are incompatible; \ $c(A) = 0.3$, \ $c(B) = 0.4$, \ $c(A \lor B) = 0.8$. \ Build a "
            r"Dutch book.",
            r"Show that the log score is strictly proper: \ minimize $-p \ln q - (1 - p)\ln(1 - q)$ over $q$.",
            r"Prevalence 0.1\%, \ sensitivity 99\%, \ false positives 1\%: \ find $P(\text{ill} \mid +)$.",
            r"Jeffrey's cloth: \ if the glimpse leaves $P(\text{blue}) = 0.2$, \ which $P(\text{violet})$ gives "
            r"$P(\text{sold}) = 0.5$?",
            r"For random-radius chords, \ what is the chance that a chord is longer than the radius?",
            r"(Essay) Halfer or thirder? \ Defend an answer, \ and say what it costs.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>A Dutch book to build; "
            "the log score's propriety; a rarer disease; Jeffrey's cloth in reverse; one more chord; and an essay "
            "on Sleeping Beauty. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the probability of conditionals, \ and Lewis's triviality", [14]),
            (r"confirmation, \ induction, \ and grue", [15]),
            (r"Bayesian and frequentist statistics", [16]),
            (r"chance, \ laws, \ and the big bad bug", [24]),
            (r"deciding under uncertainty, \ and Ellsberg again", [33]),
            (r"calibrated machines, \ and fair ones", [41, 42]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 14, \textit{Changing Your Mind}", font_size=26, color=P.CONCL).to_edge(DOWN,
                                                                                                    buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>The probability of conditionals, and Lewis's triviality "
            "theorem, in Part 14. Confirmation and induction, in Part 15. Bayesian and frequentist statistics, in "
            "Part 16. Chance and the big bad bug, in Part 24. Decisions under uncertainty, and Ellsberg again, in "
            "Part 33. And calibrated, fair machines, in Parts 41 and 42. <bookmark mark='b'/>Next, Part 14: changing "
            "your mind."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Titelbaum, \textit{Fundamentals of Bayesian Epistemology} (2022); \ Pettigrew, \textit{Accuracy and the "
             r"Laws of Credence} (2016)",
             r"Hájek, `Interpretations of Probability' \ (SEP); \ Jaynes, \textit{Probability Theory: The Logic of "
             r"Science} (2003)",
             r"Leitgeb, \textit{The Stability of Belief} (2017); \ Bostrom, \textit{Anthropic Bias} (2002)",
             r"Pearl, \textit{Probabilistic Reasoning in Intelligent Systems} (1988); \ Walley (1991)"],
            [r"Ramsey 1926; de Finetti 1937; Kemeny 1955; Lehman 1955; Teller 1973; Lewis 1980; Joyce 1998",
             r"Brier 1950; Good 1952; Savage 1971; Murphy 1973; Gneiting and Raftery 2007; Predd et al.\ 2009",
             r"Bertrand 1889; Jaynes 1957, 1973; van Fraassen 1989; Seidenfeld and Wasserman 1993; Elga 2010",
             r"Kyburg 1961; Makinson 1965; Elga 2000; Lewis 2001; Cooper 1990; Dagum and Luby 1993"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
