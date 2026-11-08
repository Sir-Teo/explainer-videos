from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"expansion, \ revision, \ contraction; \ update; \ recovery",
            r"the AGM postulates, \ checked; \ Grove's spheres; \ partial meet; \ Levi and Harper",
            r"Spohn's ranks; \ Darwiche and Pearl; \ the forgotten red bird",
            r"the Ramsey test, \ and Gärdenfors's impossibility \ (the Wall)",
            r"counterfactuals; \ Lewis's triviality \ (the Wall); \ the triviality Price List",
            r"McGee; \ default logic, \ circumscription, \ System P, \ System Z",
            r"Dung's argumentation; \ truth maintenance; \ knowledge editing",
        ]
        card = objectives_card(items, title=r"What we built", font_size=24)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>The three ways to change, and update. "
            "<bookmark mark='b'/>The AGM postulates, checked, and the spheres and remainders that realize them. "
            "<bookmark mark='c'/>Changing again, with ranks. <bookmark mark='d'/>The Ramsey test and Gärdenfors's "
            "theorem. <bookmark mark='e'/>Counterfactuals, and Lewis's triviality, which together make this part's "
            "brick. <bookmark mark='f'/>Modus ponens questioned, and the logics of defaults. <bookmark mark='g'/>And "
            "arguments that attack, and machines that revise."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{revision.revise, contract, levi, harper}", r"AGM on spheres"),
                (r"\texttt{revision.check\_agm, postulate\_table}", r"the postulates, \ checked"),
                (r"\texttt{revision.natural, lexicographic, spohn, check\_dp}", r"iterated revision"),
                (r"\texttt{revision.gardenfors}", r"the impossibility"),
                (r"\texttt{cond.Model, classic\_models, triviality\_search}", r"conditionals"),
                (r"\texttt{argue.extensions, z\_rank, check\_klm, AF}", r"defaults; \ arguments"),
                (r"\texttt{credence.*}, \ \texttt{epistemic.*}, \ \dots", r"Parts 1--13")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.55
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.55
            if a.width > 7.4:
                a.width = 7.4
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.4:
                b.width = 4.4
            b.move_to([1.8 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_revision.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=14, current=14).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has three new modules. <bookmark mark='a'/>Revision: expansion, revision and contraction on "
            "spheres, the AGM and Darwiche--Pearl postulates checked exhaustively, and Gärdenfors's theorem. "
            "Conditionals: counterfactual models and the triviality search. And defeasible reasoning: default "
            "extensions, System Z, the KLM rules, and Dung's frameworks. <bookmark mark='b'/>And the Wall has its "
            "fourteenth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[14], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"With ranks $pq{:}\,0$, \ $p\bar q{:}\,1$, \ $\bar p q{:}\,2$, \ $\bar p \bar q{:}\,3$: \ compute "
            r"$K * \lnot p$ \ and \ $K \div p$.",
            r"Show that full meet revision \ ($K * A = A$ when $\lnot A \in K$) \ satisfies K*7 and K*8.",
            r"Revise that ranking by $\lnot q$, \ then by $q$, \ naturally and amnesically. \ What is lost?",
            r"Build a three-world model where `if $A$, $B$' and `if $A$, $\lnot B$' are both false.",
            r"Run Lewis's proof with $P(AC) = 0.5$, \ $P(A\bar C) = 0.25$, \ $P(\bar A \bar C) = 0.25$.",
            r"Find all extensions of the framework $a \to b \to c \to d$, \ $d \to c$.",
        ], font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Revision and contraction on "
            "a ranking; full meet revision and the supplementary postulates; iterated revision, natural and amnesic; "
            "a counterfactual model; Lewis's proof with new numbers; and an argumentation framework. Pause here, and "
            "try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"induction, \ confirmation, \ and grue", [15]),
            (r"counterfactuals and causation", [17]),
            (r"theory change in science", [18]),
            (r"laws, \ chance, \ and what would have happened", [24]),
            (r"causal decision theory: \ choosing by imaging", [33]),
            (r"machines that reason, \ revise and argue", [42]),
        ], font_size=23)
        nxt = label(r"Next: \ Part 15, \textit{The Problem of Induction}", font_size=26, color=P.CONCL).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Induction and confirmation, in Part 15. Counterfactuals and "
            "causation, in Part 17. Theory change in science, in Part 18. Laws and chance, in Part 24. Causal "
            "decision theory, which chooses by imaging, in Part 33. And machines that reason, revise and argue, in the finale. "
            "<bookmark mark='b'/>Next, Part 15: the problem of induction."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Gärdenfors, \textit{Knowledge in Flux} (1988); \ Hansson, \textit{A Textbook of Belief Dynamics} (1999)",
             r"Lewis, \textit{Counterfactuals} (1973); \ Bennett, \textit{A Philosophical Guide to Conditionals} (2003)",
             r"Edgington, `Indicative Conditionals' \ (SEP); \ Makinson, \textit{Bridges from Classical to "
             r"Nonmonotonic Logic} (2005)",
             r"Baroni et al.\ (eds.), \textit{Handbook of Formal Argumentation} (2018)"],
            [r"Ramsey 1929; Stalnaker 1968; Adams 1970; Lewis 1976; Reiter 1980; McCarthy 1980; Alchourrón et al.\ 1985",
             r"McGee 1985; Gärdenfors 1986; Grove 1988; Spohn 1988; Kraus, Lehmann and Magidor 1990; Pearl 1990",
             r"Katsuno and Mendelzon 1991; Makinson and Gärdenfors 1991; Hansson 1991; Lehmann and Magidor 1992",
             r"Dung 1995; Darwiche and Pearl 1997; Kolodny and MacFarlane 2010; Meng et al.\ 2022; Cohen et al.\ 2024"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
