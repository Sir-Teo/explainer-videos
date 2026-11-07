from __future__ import annotations

from videos.stats.stats35.common import *  # noqa: F403

PROBLEMS = [
    r"Show that under complete randomization $E(\bar Y_1 - \bar Y_0) = \bar\tau$, \ with the science fixed.",
    r"Derive $\mathrm{Var}(\bar Y_1 - \bar Y_0) = S_1^2/n_1 + S_0^2/n_0 - S_\tau^2/n$.",
    r"Show that $E(s_1^2/n_1 + s_0^2/n_0)$ exceeds the true variance by $S_\tau^2/n$.",
    r"Under randomization, \ exclusion and monotonicity, \ show that $\mathrm{ITT}_Y/\mathrm{ITT}_D$ is the compliers' average effect.",
    r"Show that $K$ looks at $|z| > 1.96$ give a false-positive rate above 5\% for $K = 2$, \ and find it.",
    r"Show that the design effect of equal clusters of size $m$ with correlation $\rho$ is $1 + (m-1)\rho$.",
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
            (r"Salk: \ the randomized half told the truth", BANDC), (r"potential outcomes; \ the science table", TAUC),
            (r"estimands; \ SUTVA", TAUC), (r"selection bias: \ $-2.2$ vs $-7.8$", MISSC),
            (r"Fisher: \ the sharp null, \ exactly", Y0C), (r"Neyman: \ the conservative variance", Y0C),
            (r"blocks and pairs: \ variance $\times 0.6$", BANDC), (r"adjustment: \ Freedman's warning, \ Lin's fix", BANDC),
            (r"clusters: \ deff about 11; \ 36\% vs 90\%", MISSC), (r"noncompliance: \ ITT, \ LATE $= -8.7$", TAUC),
            (r"interference; \ subgroups; \ sequential boundaries", SEQC), (r"surrogates (CAST); \ transport", MISSC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 35, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part thirty-five in twelve lines. <bookmark mark='a'/> The Salk trial ran two designs, and the "
            "randomized comparison avoids the selection bias that threatens the observed-control comparison. A causal"
            " effect compares potential outcomes, and the science table is always half missing. Estimands must be "
            "named, and SUTVA rules out interference and hidden versions. When a doctor chooses, selection bias "
            "swallows most of the effect; a coin removes it. Fisher's sharp null gives exact tests; Neyman's "
            "conservative variance gives intervals for the average effect. Blocking and pairing cut the variance by "
            "two fifths. Regression adjustment helps, provided we interact and use sandwich errors, as Lin showed "
            "against Freedman's warning. Randomizing schools means analysing schools. With noncompliance, intention "
            "to treat and the local average treatment effect are honest; as-treated is not. Vaccination strategies "
            "with spillovers can be studied with two-stage designs; subgroups need suspicion; interim looks need "
            "boundaries. Surrogates can mislead, and trials must be transported to the people who will use them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(35, r"randomization identifies the average effect, \ with no model",
                            r"that we can randomize, \ and that patients follow the assignment",
                            r"Part 36: \ causes from observational data: \ unconfoundedness, \ propensity scores, \ DAGs, \ sensitivity analysis")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for later. This part showed that randomization identifies average causal "
            "effects with no model for the outcomes. <bookmark mark='b'/> It assumed that we can randomize, and, apart from "
            "chapter nine, that patients do as they are assigned. <bookmark mark='c'/> Part 36 asks what can be learned "
            "when no one randomized at all: unconfoundedness, propensity scores, causal diagrams, and how sensitive the "
            "conclusions are to what was not measured."
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
            (r"observational studies, \ target trials", [36]), (r"instruments and natural experiments", [37]),
            (r"survival endpoints in trials", [40]), (r"missing outcomes, \ dropout", [41]),
            (r"efficient estimation of the ATE", [49]), (r"anytime-valid sequential tests", [58]),
            (r"heterogeneous effects, \ interference, \ mediation", [62]), (r"fairness and counterfactuals", [63]),
        ], font_size=22)
        self.add(card.head)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 36 estimates causal effects without randomization, framed as "
            "target trials. Part 37 uses natural experiments and instruments, the LATE's home. Part 40 analyses survival "
            "endpoints. Part 41 handles patients who drop out. Part 49 finds the most efficient estimator of an average "
            "effect. Part 58 makes sequential testing valid at any time. Part 62 estimates heterogeneous effects, "
            "interference and mediation. And Part 63 asks what counterfactual fairness means."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The unbiasedness of the difference in "
            "means; Neyman's variance; the conservativeness of its estimate; the local average treatment effect; the "
            "false-positive rate of two looks; and the design effect. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"G. Imbens \& D. Rubin, \emph{Causal Inference for Statistics, Social, and Biomedical Sciences} (2015)",
             r"P. Ding, \emph{A First Course in Causal Inference} (2024)",
             r"P. Rosenbaum, \emph{Design of Observational Studies} (2010); \ A. Gerber \& D. Green, \emph{Field Experiments} (2012)",
             r"C. Jennison \& B. Turnbull, \emph{Group Sequential Methods with Applications to Clinical Trials} (1999)"],
            [r"J. Neyman (1923/1990); \ R. A. Fisher (1935); \ D. Rubin (1974, 1980); \ P. Holland (1986); \ P. Meier (1972)",
             r"D. Freedman (2008); \ W. Lin (2013); \ J. Cornfield (1978); \ G. Imbens \& J. Angrist (1994); \ J. Angrist, G. Imbens \& D. Rubin (1996)",
             r"M. Hudgens \& E. Halloran (2008); \ ISIS-2 (1988); \ S. Pocock (1977); \ P. O'Brien \& T. Fleming (1979); \ K. Lan \& D. DeMets (1983)",
             r"R. Prentice (1989); \ D. Echt et al. (1991); \ E. Stuart et al. (2011); \ I. Dahabreh et al. (2019)"])
        with self.voiceover(
            "The books this part follows: Imbens and Rubin's Causal Inference; Peng Ding's First Course in Causal "
            "Inference; Rosenbaum's Design of Observational Studies and Gerber and Green's Field Experiments; and Jennison "
            "and Turnbull on group sequential methods; with the papers from Neyman to Dahabreh."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=35, current=None)
        nxt = VGroup(label(r"Part 36", font_size=30, color=GREY_B), label(r"Causes Without Experiments", font_size=48),
                     label(r"what can we learn when no one flipped a coin?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Thirty-five parts of sixty-five. <bookmark mark='a'/> We know what a causal effect is, and why a coin lets us "
            "measure it. <bookmark mark='b'/> But most questions about causes, smoking and cancer, schooling and income, "
            "policy and growth, can never be put to a coin. Part 36: causes without experiments."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(35)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
