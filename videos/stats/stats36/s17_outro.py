from __future__ import annotations

from videos.stats.stats36.common import *  # noqa: F403

PROBLEMS = [
    r"Prove that $e(X)$ is a balancing score: \ $X \perp\!\!\!\perp T \mid e(X)$.",
    r"Show that unconfoundedness given $X$ implies unconfoundedness given $e(X)$.",
    r"Show that $E[TY/e(X)] = E[Y(1)]$ under unconfoundedness and overlap.",
    r"Show that the AIPW estimator is consistent if either $\mu_t$ or $e$ is correct.",
    r"In the M-graph $T \leftarrow A \to M \leftarrow B \to Y$, $T \to Y$, \ show adjusting for $M$ alone violates the back-door criterion.",
    r"Derive the E-value: \ show $RR + \sqrt{RR(RR - 1)}$ solves $\frac{E^2}{2E - 1} = RR$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.upgrade()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"LaLonde: \ methods disagree, \ overlap decides", MISSC), (r"unconfoundedness and overlap", TAUC),
            (r"DAGs; \ chains, \ forks, \ colliders", Y0C), (r"back door; \ Berkson; \ M-bias; \ mediators", Y0C),
            (r"front door; \ do-calculus is complete", Y0C), (r"Simpson: \ the graph decides", BANDC),
            (r"g-computation; \ propensity scores", PSC), (r"IPW: \ the pseudo-trial, \ extreme weights", PSC),
            (r"AIPW: \ two chances; \ Kang--Schafer", BANDC), (r"DML: \ orthogonality and cross-fitting", BANDC),
            (r"CATE: \ meta-learners, \ causal forests", TAUC), (r"sensitivity; \ smoking; \ MSMs; \ target trials", MISSC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 36, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part thirty-six in twelve lines. <bookmark mark='a'/> LaLonde showed that non-experimental methods could miss "
            "an experimental answer, and forty years later the lesson is that overlap and pre-treatment outcomes decide more "
            "than methods do. Without a coin we need unconfoundedness and overlap. Causal diagrams make the assumptions "
            "explicit, and chains, forks and colliders say which paths carry association. The back-door criterion says what "
            "to adjust for, and Berkson's bias, M-bias and mediators what not to. The front door and the do-calculus "
            "identify effects beyond adjustment. Simpson's paradox is resolved by the graph, not the numbers. g-computation "
            "models the outcome, propensity scores model the treatment, and weighting builds a pseudo-trial at the price of "
            "extreme weights. Doubly robust estimation gives two chances to be right, but not with both models wrong. Double "
            "machine learning makes flexible models honest by orthogonality and cross-fitting. Meta-learners and causal "
            "forests estimate effects that vary. And sensitivity analysis, from Cornfield's smoking argument to E-values, "
            "with marginal structural models and target trials for treatments over time, completes the toolkit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(36, r"observational effects, \ identified by unconfoundedness and overlap",
                            r"that every confounder is measured: \ untestable",
                            r"Part 37: \ natural experiments, \ where nature or policy randomizes: \ instruments, \ regression discontinuity, \ difference-in-differences, \ synthetic control")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for later. This part identified causal effects from observational data under "
            "unconfoundedness and overlap. <bookmark mark='b'/> It assumed that every confounder was measured, which can "
            "never be tested. <bookmark mark='c'/> Part 37 looks for natural experiments, situations where nature, a lottery "
            "or a rule assigns treatment as if at random: instrumental variables, regression discontinuities, "
            "differences-in-differences and synthetic controls."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card[0]), FadeIn(card[1][0]), FadeIn(card[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card[1][1][2]))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"natural experiments", [37]), (r"survival and competing risks, \ causally", [40]),
            (r"missing data: \ the same weighting and DR ideas", [41]), (r"efficient influence functions", [49]),
            (r"high-dimensional confounding", [52]), (r"distribution shift as transport", [60]),
            (r"mediation, \ heterogeneity, \ causal discovery", [62]), (r"counterfactual fairness", [63]),
        ], font_size=22)
        self.add(card.head)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 37 finds natural experiments. Part 40 asks causal questions about "
            "survival. Part 41 applies the same weighting and doubly robust ideas to missing data. Part 49 derives the "
            "efficient influence functions behind AIPW and DML. Part 52 handles thousands of confounders. Part 60 treats "
            "distribution shift as a transport problem. Part 62 covers mediation, heterogeneous effects and discovering "
            "causal graphs from data. And Part 63 asks what counterfactual fairness means."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The balancing property of the propensity "
            "score; unconfoundedness given the score; the unbiasedness of weighting; double robustness; the M-graph; and the "
            "E-value formula. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"M. Hern\'an \& J. Robins, \emph{Causal Inference: What If} (2020)",
             r"J. Pearl, \emph{Causality} (2nd ed. 2009); \ J. Pearl, M. Glymour \& N. Jewell, \emph{Causal Inference in Statistics: A Primer} (2016)",
             r"G. Imbens \& D. Rubin (2015); \ P. Rosenbaum, \emph{Observational Studies} (2002)",
             r"S. Wager, \emph{Causal Inference: A Statistical Learning Approach} (2024)"],
            [r"R. LaLonde (1986); \ R. Dehejia \& S. Wahba (1999); \ J. Smith \& P. Todd (2005); \ G. Imbens \& Y. Xu (2024)",
             r"P. Rosenbaum \& D. Rubin (1983); \ W. Cochran (1968); \ J. Robins (1986); \ J. Robins, A. Rotnitzky \& L. Zhao (1994)",
             r"J. Kang \& J. Schafer (2007); \ V. Chernozhukov et al. (2018); \ S. Wager \& S. Athey (2018); \ S. K\"unzel et al. (2019)",
             r"J. Cornfield et al. (1959); \ T. VanderWeele \& P. Ding (2017); \ C. Cinelli \& C. Hazlett (2020); \ M. Hern\'an \& J. Robins (2016)"])
        with self.voiceover(
            "The books this part follows: Hernán and Robins's Causal Inference: What If; Pearl's Causality and his primer "
            "with Glymour and Jewell; Imbens and Rubin, and Rosenbaum's Observational Studies; and Stefan Wager's statistical "
            "learning approach; with the papers from Cornfield to Imbens and Xu."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=36, current=None)
        nxt = VGroup(label(r"Part 37", font_size=30, color=GREY_B), label(r"Natural Experiments", font_size=48),
                     label(r"when nature, \ a lottery or a rule flips the coin", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Thirty-six parts of sixty-five. <bookmark mark='a'/> We can estimate causes without experiments, if we measure "
            "enough, and say how wrong we might be if we did not. <bookmark mark='b'/> But sometimes we can do better: "
            "nature, a lottery or an arbitrary rule may have flipped the coin for us. Part 37: natural experiments."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(36)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
