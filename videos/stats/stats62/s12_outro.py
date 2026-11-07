from __future__ import annotations

from videos.stats.stats62.common import *  # noqa: F403

PROBLEMS = [
    r"Derive the front-door formula from the back-door formula applied twice, \ on $A \to M$ and on $M \to Y$.",
    r"Show that under the marginal sensitivity model each IPW weight lies in $[1 + (1/e - 1)/\Lambda, \ 1 + (1/e - 1)\Lambda]$.",
    r"In the linear proximal model, \ show the 2SLS of $Y$ on $(A, W)$ with instruments $(A, Z)$ is consistent for $b_A$.",
    r"Under the stated exposure model and Bernoulli assignment, show $E[Y_i\mid Z_i=1]-E[Y_i\mid Z_i=0]=2$; distinguish this from finite-sample ratio bias.",
    r"Show that the in-sample value of the EWM rule is biased upward: \ $E\max_\pi \hat V(\pi) \ge \max_\pi V(\pi)$.",
    r"Show that inverse-odds weights $(1 - p)/p$ turn the trial's covariate law into the target's.",
]


class Outro(LectureMixin, VoiceoverScene):
    def construct(self):
        self.recap()
        self.upgrade()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"HIV-CAUSAL and START: \ complementary evidence", TRTC), (r"the front door: \ 1.01 vs naive 2.83", IDC),
            (r"do-calculus is complete", IDC), (r"NSW: \ sensitivity to $\Lambda$", HIDC),
            (r"proximal: \ two proxies, \ 95\% kept", IDC), (r"interference: \ exposure mappings", TRTC),
            (r"EWM: \ the winner's curse", NAIVEC), (r"Q-learning: \ backward induction", TRTC),
            (r"discovery: \ equivalence, \ varsortability", HIDC), (r"transport: \ selection diagrams", IDC),
            (r"surrogates: \ the index, \ the paradox", GOLDC), (r"open problems", S.ACCENT),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 62, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Part sixty-two in twelve lines. An observational emulation of when to start HIV treatment, "
            "followed by a trial with a related but different target and endpoint. The front door identified an effect through a mediator, where the naive estimate "
            "was nearly three times too large. The do-calculus is complete. The National Supported Work data are sensitive "
            "to modest hidden confounding. Appropriate proxies and valid bridge assumptions can identify an effect that naive adjustment misses. <bookmark "
            "mark='b'/> Exposure mappings separate direct effects from spillovers. Learned rules suffer the winner's curse, "
            "addressed by truly independent evaluation with appropriate nuisance training. Q-learning optimizes regimes backward. Discovery is limited by equivalence and can be "
            "fooled by scale. Selection diagrams say when to transport. Surrogates save time and can mislead silently."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.5), run_time=12.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.5), run_time=12.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(62, r"individual-level data, \ freely analysed", r"privacy costs nothing; \ fairness is not asked",
                            r"Part 63: \ privacy and fairness")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. Every analysis here used individual-level data, freely. "
            "<bookmark mark='b'/> It assumed privacy costs nothing, and never asked whether the learned rules were fair. "
            "<bookmark mark='c'/> Part sixty-three prices privacy exactly, and asks what fairness can require."
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
            (r"fair treatment rules and counterfactual fairness", [63]), (r"causal questions about AI systems", [64]),
            (r"the dissertation's causal chapter", [65]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part sixty-three's fair treatment rules and counterfactual fairness. "
            "Part sixty-four's causal questions about AI systems. And the dissertation's causal chapter."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=5.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The front-door formula from two back "
            "doors; the sensitivity model's weight box; proximal two-stage least squares; what the naive difference "
            "estimates under interference; the winner's curse of empirical welfare maximization; and why inverse-odds "
            "weights transport. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"J. Pearl, \ \emph{Causality} (2nd ed., 2009)",
             r"M. Hern\'an \& J. Robins, \ \emph{Causal Inference: What If} (2020)",
             r"J. Peters, \ D. Janzing \& B. Sch\"olkopf, \ \emph{Elements of Causal Inference} (2017)"],
            [r"HIV-CAUSAL Collaboration, \ \emph{Ann. Intern. Med.} (2011); \ INSIGHT START, \ \emph{NEJM} (2015)",
             r"I. Shpitser \& J. Pearl (2006); \ Z. Tan (2006); \ Q. Zhao, \ D. Small \& B. Bhattacharya, \ \emph{JRSS B} (2019)",
             r"W. Miao, \ Z. Geng \& E. Tchetgen Tchetgen, \ \emph{Biometrika} (2018); \ P. Aronow \& C. Samii, \ \emph{Ann. Appl. Stat.} (2017)",
             r"T. Kitagawa \& A. Tetenov, \ \emph{Econometrica} (2018); \ S. Athey \& S. Wager, \ \emph{Econometrica} (2021); \ S. Athey et al. (2019)"])
        with self.voiceover(
            "The books behind this part: Pearl's Causality; Hernán and Robins's Causal Inference: What If; and Peters, "
            "Janzing and Schölkopf's Elements of Causal Inference; with the papers from the HIV-CAUSAL Collaboration to the "
            "surrogate index."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=62, current=None)
        nxt = VGroup(label(r"Part 63", font_size=30, color=GREY_B), label(r"Privacy and Fairness", font_size=48),
                     label(r"how much does protecting individuals cost the statistics, \ and what does fairness require?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Sixty-two parts of sixty-five. <bookmark mark='a'/> The HIV studies illustrate complementary observational and randomized evidence. Explicit assumptions permit interpretation; agreement is not proof that every assumption was correct. <bookmark mark='b'/> Next, Part sixty-three: privacy and fairness."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(62)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
