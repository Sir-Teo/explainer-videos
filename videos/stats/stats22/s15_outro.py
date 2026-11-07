from __future__ import annotations

from videos.stats.stats22.common import *  # noqa: F403

PROBLEMS = [
    r"Poisson: \ the score is $U = x/\lambda - 1$. \ Show $E\,U = 0$ and $\mathrm{Var}\,U = -E\,U' = 1/\lambda$.",
    r"Neyman--Scott with $m$ readings per group: \ show $\hat\sigma^2 \to (m - 1)\sigma^2/m$. \ What fixes it?",
    r"Fourteen successes in twenty, \ $H_0\colon p = 0.5$: \ check $W = 3.81$, \ $S = 3.20$, \ $\Lambda = 3.29$.",
    r"EM for $p$ alone, \ the components known: \ show $p_{t+1} = \bar r(p_t)$ and that $\ell(p_{t+1}) \ge \ell(p_t)$.",
    r"Intercept-only Poisson fitted to any counts: \ the sandwich SE of $\log\hat\mu$ is $\sqrt{s^2/(n\bar y^2)}$.",
    r"Alice and Bob: \ verify $P(X \ge 9) = 0.073$ (binomial) and $0.033$ (heads before the 3rd tail).",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"Pearson's nonic vs likelihood", PATH), (r"upgrade: \ six conditions", GREY_A),
            (r"consistency: \ KL $\ge 0$, \ the argmax", LIK), (r"normality: \ expand the score", LIK),
            (r"observed vs expected: \ conditional precision", LIK), (r"many parameters: \ the profile", PATH),
            (r"Wald, \ score, \ LR; \ Hauck--Donner", LRC), (r"Neyman--Scott: \ $\sigma^2/2$", RES),
            (r"EM: \ Jensen's bound, \ 1,622 steps", CRAB1), (r"spikes, \ twins and edges", RES),
            (r"the sandwich: \ 77\% vs 93\%", HIT), (r"quasi-, \ composite, \ pseudo", TEAL),
            (r"the likelihood principle", PRIOR), (r"the Fisher metric", PATH),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 22, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part twenty-two in fourteen lines. <bookmark mark='a'/> Pearson split Weldon's crabs with a ninth-degree"
            " polynomial; a midpoint-density local fit improved the likelihood. Our six-item checklist summarizes "
            "assumptions; precise theorems need additional integrability and information conditions. Consistency "
            "follows from the Kullback–Leibler inequality and the argmax of a converging curve; asymptotic normality "
            "from expanding the score. Observed information tracked conditional variance well in the Cauchy example. "
            "With many parameters, profile along the ridge. Wald, score and likelihood-ratio tests read one curve "
            "three ways, and can disagree badly. Neyman and Scott's incidental parameters halve the variance forever."
            " EM climbs a lower bound built from the missing labels, surely but slowly. Mixture likelihoods spike, "
            "switch labels, and sit on edges. Under a wrong model the estimate finds the closest wrong answer, and a "
            "sandwich estimates asymptotic precision under its own sampling and regularity assumptions. Quasi-, "
            "composite and pseudo-likelihoods replace likelihoods we can't write down. The likelihood principle asks "
            "whether unseen outcomes should matter. And the information is a ruler on the space of distributions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=36.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"GLMs and quasi-likelihood; \ GEE", [24]), (r"REML: \ Neyman--Scott, \ cured", [25]),
            (r"Jeffreys and reference priors", [26]), (r"EM's cousins: \ variational inference", [27]),
            (r"AIC: \ estimating the KL divergence", [28]), (r"M-estimators: \ the sandwich again", [30]),
            (r"EM for missing data", [41]), (r"LAN, \ Hodges and Le Cam", [47]),
        ], font_size=22)
        intro = label("Where the likelihood methods return", font_size=36)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 24 builds generalized linear models on quasi-likelihood, and GEE "
            "on the sandwich. Part 25's restricted likelihood cures Neyman–Scott for mixed models. Part 26 derives Jeffreys "
            "and reference priors from the information. Part 27's variational inference is EM's cousin. Part 28's AIC is an "
            "estimate of the Kullback–Leibler divergence. Part 30's M-estimators carry the sandwich everywhere. Part 41 uses EM "
            "for missing data. And Part 47 rebuilds this part's asymptotics on Le Cam's local asymptotic normality, where "
            "Hodges's estimator finally gets its explanation."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), FadeIn(card.head), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The score identities for the Poisson; "
            "Neyman–Scott with m readings per group; the trinity for fourteen of twenty, by hand; EM for the mixing proportion "
            "alone, and why it climbs; the sandwich for an intercept-only Poisson model; and Alice's and Bob's p-values. Pause "
            "here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Y. Pawitan, \emph{In All Likelihood} (2001)",
             r"A. W. van der Vaart, \emph{Asymptotic Statistics} (1998)",
             r"D. R. Cox, \emph{Principles of Statistical Inference} (2006)",
             r"G. McLachlan \& T. Krishnan, \emph{The EM Algorithm and Extensions} (2nd ed., 2008)"],
            [r"K. Pearson (1894); \ R. A. Fisher (1922, 1934); \ A. Wald (1949); \ C. R. Rao (1945, 1948)",
             r"J. Neyman \& E. Scott (1948); \ B. Efron \& D. Hinkley (1978); \ W. Hauck \& A. Donner (1977)",
             r"A. Dempster, \ N. Laird \& D. Rubin (1977); \ T. Louis (1982); \ P. Huber (1967); \ H. White (1982)",
             r"J. Besag (1975); \ B. Lindsay (1988); \ A. Birnbaum (1962); \ D. Mayo (2014); \ S. Amari (1998)"])
        with self.voiceover(
            "The books this part follows: Pawitan's In All Likelihood, van der Vaart's Asymptotic Statistics, Cox's Principles "
            "of Statistical Inference, and McLachlan and Krishnan on EM; with the papers from Pearson's crabs to Amari's "
            "natural gradient."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=22, current=None)
        nxt = VGroup(label(r"Part 23", font_size=30, color=GREY_B), label(r"The Linear Model in Depth", font_size=48),
                     label(r"what the linear model really estimates, \ and how far to trust its SEs", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Twenty-two parts of sixty-five. <bookmark mark='a'/> We know now why likelihood works, when it fails, and how to "
            "keep its standard errors honest when the model is wrong. <bookmark mark='b'/> Next, the linear model in full. In "
            "1967 James Longley ran a small, awkward data set through the era's regression programs, and many of them printed "
            "wrong digits. Part 23: the linear model in depth."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(22)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
