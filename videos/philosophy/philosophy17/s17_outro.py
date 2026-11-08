from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"Hume's two definitions; \ al-Ghazālī; \ Mill's methods; \ INUS conditions",
            r"Lewis's counterfactuals, \ and preemption, \ trumping, \ transitivity",
            r"probability-raising and Hesslow's pills; \ Russell; \ Woodward's interventions",
            r"structural models; \ d-separation; \ back door, \ front door, \ the do-calculus",
            r"the ladder: \ twin networks, \ necessity and sufficiency; \ Halpern--Pearl, \ computed",
            r"Markov, \ Reichenbach, \ Yule and Bell; \ PC and Markov equivalence \ (the Wall)",
            r"potential outcomes, \ instruments, \ difference in differences; \ uplift and invariance",
            r"Kim's exclusion argument, \ and Yablo's pigeon",
        ]
        card = objectives_card(items, title=r"What we built", font_size=23)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Hume's two definitions, al-Ghazālī's challenge, Mill's "
            "methods and Mackie's conditions. <bookmark mark='b'/>Lewis's counterfactual theory, and the cases that "
            "break it. <bookmark mark='c'/>Probability-raising, Russell's challenge, and Woodward's interventions. "
            "<bookmark mark='d'/>Structural models and graphs, the back door and the front door, and the "
            "do-calculus. <bookmark mark='e'/>The ladder of causation, and actual causation, run on the classic "
            "cases. <bookmark mark='f'/>The Markov condition, the common cause and its two counterexamples, and "
            "causal discovery, with this part's brick in the Wall. <bookmark mark='g'/>The statistician's "
            "framework, and causes at work in industry. <bookmark mark='h'/>And the problem of mental causation."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{causal.SCM: solve, prob, counterfactual, sample}", r"models; \ do; \ rung 3"),
                (r"\texttt{causal.DAG: dsep, backdoor\_ok, calculus\_rule}", r"graphs; \ the calculus"),
                (r"\texttt{causal.backdoor\_adjust, frontdoor\_adjust}", r"identification"),
                (r"\texttt{causal.hp\_cause, classic\_cases, responsibility}", r"actual causation"),
                (r"\texttt{causal.pc, equivalence\_class, lingam\_demo}", r"discovery"),
                (r"\texttt{causal.instrumental, diff\_in\_diff, uplift\_demo}", r"causes at work"),
                (r"\texttt{stats.*}, \ \texttt{induction.*}, \ \dots", r"Parts 1--16")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.55
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.55
            if a.width > 7.6:
                a.width = 7.6
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.2:
                b.width = 4.2
            b.move_to([1.9 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_causal.py}", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4)
        w = wall(upto=17, current=17).scale(0.36).to_corner(DR, buff=0.3).shift(UP * 0.5)
        with self.voiceover(
            "The Reasoner has a new module, causal. <bookmark mark='a'/>It solves structural models under "
            "intervention and computes counterfactuals by abduction, action and prediction; tests d-separation and "
            "checks each rule of the do-calculus; adjusts through back and front doors; decides actual causation "
            "by the Halpern-Pearl definition; runs the PC algorithm and enumerates equivalence classes; and "
            "estimates effects with instruments, differences in differences and uplift. <bookmark mark='b'/>And "
            "the Wall has its seventeenth brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[17], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"In the sprinkler graph, \ list every set that d-separates $S$ and $R$. \ Does $\{C, L\}$?",
            r"Derive the back-door formula from the truncated factorization $\prod_{i \ne X} P(v_i \mid pa_i)$.",
            r"Let the gene also affect tar. \ Which front-door step fails, \ and which path is open?",
            r"With 10\% defiers, \ compute PN and PNS, \ and show PNS $\ne P(y \mid do(x)) - P(y \mid do(x'))$.",
            r"Show that $X \to Y \to Z$ and $X \leftarrow Y \to Z$ are Markov equivalent, \ but $X \to Y \leftarrow Z$ is not.",
            r"Model Schaffer's trumping case. \ Is the sergeant's order a cause by Halpern--Pearl?",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>D-separation in the "
            "sprinkler graph; the back-door formula from the truncated factorization; a broken front door; "
            "necessity with defiers; Markov equivalence by hand; and trumping, modelled. Pause here, and try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"causal explanation; \ underdetermination", [18]),
            (r"laws, \ chance, \ and the direction of causation", [24]),
            (r"Bell's correlations without a common cause", [26]),
            (r"mental causation; \ minds and machines", [30]),
            (r"determinism and free will", [32]),
            (r"causal decision theory and Newcomb's problem", [33]),
            (r"counterfactual fairness; \ responsibility", [41]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 18, \textit{Theories and Reality}", font_size=26, color=P.CONCL).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Causal explanation and underdetermination, in Part 18. Laws, "
            "chance and the direction of causation, in Part 24. Bell's correlations, in Part 26. Mental causation, "
            "in Part 30. Determinism and free will, in Part 32. Causal decision theory and Newcomb's problem, in "
            "Part 33. And counterfactual fairness and responsibility, in Part 41. <bookmark mark='b'/>Next, Part "
            "18: theories and reality."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Pearl, \textit{Causality} (2000, 2009); \ Pearl and Mackenzie, \textit{The Book of Why} (2018)",
             r"Spirtes, Glymour and Scheines, \textit{Causation, Prediction, and Search} (1993); \ Woodward, "
             r"\textit{Making Things Happen} (2003)",
             r"Halpern, \textit{Actual Causality} (2016); \ Paul and Hall, \textit{Causation: A User's Guide} (2013)",
             r"Imbens and Rubin, \textit{Causal Inference} (2015); \ Hernán and Robins, \textit{Causal Inference: What "
             r"If} (2020); \ Peters, Janzing and Schölkopf, \textit{Elements of Causal Inference} (2017)"],
            [r"Hume 1748; Mill 1843; Russell 1913; Wright 1921, 1928; Neyman 1923; Mackie 1965; Suppes 1970; Lewis 1973",
             r"Rubin 1974; Cartwright 1979; Holland 1986; Verma and Pearl 1990; Yablo 1992; Pearl 1995; Kim 1998",
             r"Hall 2004; Halpern and Pearl 2005; Shpitser and Pearl 2006; Halpern 2015; Peters et al.\ 2016",
             r"Card and Krueger 1994; Angrist and Krueger 1991; Chernozhukov et al.\ 2018; Bareinboim et al.\ 2022"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
