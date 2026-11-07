from __future__ import annotations

from videos.stats.stats58.common import *  # noqa: F403

PROBLEMS = [
    r"Show that Wald's thresholds give $P_0(\text{reject}) \le \alpha/(1 - \beta)$, \ by a change of measure.",
    r"Prove Wald's identity $E[S_N] = E[N]\,E[Z_1]$ for a stopping time with $E N < \infty$.",
    r"Prove Ville's inequality $P(\sup_t M_t \ge 1/\alpha) \le \alpha$ for a nonnegative martingale with $M_0 = 1$.",
    r"Show that $f_\kappa(p) = \kappa p^{\kappa - 1}$ is a calibrator, \ and that the mean of e-values is an e-value.",
    r"Derive Robbins's normal-mixture confidence sequence from the mixture martingale.",
    r"Show that e-BH controls the FDR at $\alpha m_0/m$ under arbitrary dependence.",
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
            (r"the SPRT: \ about half the shells on average, \ in this example", SPRTC), (r"Wald--Wolfowitz: \ optimal at two simple hypotheses", SPRTC),
            (r"group-sequential looks, \ and biased early stops", FIXEDC), (r"Ville: \ a test martingale rarely gets rich", WEALTHC),
            (r"e-values: \ calibrate, \ average, \ multiply", WEALTHC), (r"composite nulls: \ split LRT, \ GROW", WEALTHC),
            (r"confidence sequences, \ by mixtures and bets", CSC), (r"CAST totals: \ wealth 333 under a working death-label model", FIXEDC),
            (r"e-BH under any dependence; \ CUSUM on the Nile", CHANGEC), (r"Thompson sampling: \ earn while learning", BANDITC),
            (r"adaptive data: \ biased means, \ weighted AIPW", BANDITC), (r"off-policy values; \ five open problems", S.ACCENT),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 58, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            (
            "<bookmark mark='a'/> Part fifty-eight in twelve lines. The example SPRT uses about half the fixed "
            "count test's sample size on average; its optimality compares actual errors at two simple IID "
            'hypotheses. Group-sequential designs calibrate planned or validly timed looks, and stopping can bias '
            'reported effects. Ville protects nonnegative test supermartingales. E-values average under arbitrary '
            'dependence, while products require independence or conditional fairness. Composite nulls need a '
            "construction fair against the whole family. <bookmark mark='b'/> Confidence sequences provide "
            "simultaneous coverage over time under their assumptions. CAST's aggregate totals illustrate a working "
            'death-label bet, not its clinical monitoring history. E-BH combines valid null e-values for a '
            'specified family. CUSUM uses mean run length rather than an ever-alarm probability. Adaptive '
            'allocation needs appropriate inference, and logged propensities enable off-policy evaluation.'
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.5), run_time=12.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.5), run_time=12.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(58, r"guarantees under a model with a fixed number of parameters", r"$p$ stays small as $n$ grows",
                            r"Part 59: \ classical statistics when $p$ and $n$ grow together")
        with self.voiceover(
            (
            "<bookmark mark='a'/> Many examples here used a fixed, small number of model parameters. <bookmark "
            "mark='b'/> That is a useful bridge to the next part, but not an assumption required by all the "
            "nonparametric and betting guarantees just developed. <bookmark mark='c'/> Part fifty-nine studies "
            'classical likelihood, estimation and bootstrap procedures when the number of fitted parameters grows '
            'proportionally with sample size.'
        )
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
            (r"robustness when the future shifts", [60]), (r"adaptive and sequential causal designs", [62]),
            (r"privacy budgets spent over time", [63]), (r"evaluating AI systems as they are deployed", [64]),
            (r"the dissertation's monitoring plan", [65]),
        ], font_size=22)
        self.play(FadeIn(card.head))
        with self.voiceover(
            (
            "Where it comes back. <bookmark mark='a'/> Part sixty's robustness when the future shifts. Part "
            "sixty-two's adaptive and sequential causal designs. Part sixty-three's privacy budgets, spent over "
            "time. Part sixty-four's evaluation of AI systems as they are deployed. And the dissertation's "
            'monitoring plan.'
        )
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            (
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Wald's error bound; Wald's "
            "identity; Ville's inequality; calibrators and merging; Robbins's mixture sequence; and e-BH's "
            'guarantee. Pause here if you want to try them.'
        )
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"A. Wald, \ \emph{Sequential Analysis} (1947); \ D. Siegmund, \ \emph{Sequential Analysis} (1985)",
             r"C. Jennison \& B. Turnbull, \ \emph{Group Sequential Methods} (2000); \ G. Shafer \& V. Vovk, \ \emph{Game-Theoretic Foundations} (2019)",
             r"A. Ramdas \& R. Wang, \ \emph{Hypothesis Testing with E-values} (2024); \ T. Lattimore \& C. Szepesv\'ari, \ \emph{Bandit Algorithms} (2020)"],
            [r"J. Ville (1939); \ H. Robbins, \ \emph{Ann. Math. Stat.} (1970); \ E. Page, \ \emph{Biometrika} (1954); \ G. Lorden (1971)",
             r"G. Shafer, \ \emph{JRSS A} (2021); \ V. Vovk \& R. Wang, \ \emph{Ann. Stat.} (2021); \ L. Wasserman et al., \ \emph{PNAS} (2020)",
             r"S. Howard et al., \ \emph{Ann. Stat.} (2021); \ I. Waudby-Smith \& A. Ramdas, \ \emph{JRSS B} (2024); \ R. Wang \& A. Ramdas, \ \emph{JRSS B} (2022)",
             r"P. Gr\"unwald et al., \ \emph{JRSS B} (2024); \ V. Hadad et al., \ \emph{PNAS} (2021); \ M. Kasy \& A. Sautmann, \ \emph{Econometrica} (2021)"])
        with self.voiceover(
            (
            "The books behind this part: Wald's and Siegmund's on sequential analysis; Jennison and Turnbull on "
            "group sequential methods; Shafer and Vovk's game-theoretic foundations; Ramdas and Wang on e-values; "
            'and Lattimore and Szepesvári on bandits; with the papers from Ville to the present.'
        )
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=58, current=None)
        nxt = VGroup(label(r"Part 59", font_size=30, color=GREY_B), label(r"High-Dimensional Asymptotics", font_size=48),
                     label(r"what happens to classical statistics when $p$ and $n$ grow together?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            (
            "Fifty-eight parts of sixty-five. <bookmark mark='a'/> Fit a logistic regression with one variable for "
            'every five observations, and the textbook likelihood-ratio test, the one every software package '
            'prints, is badly miscalibrated: its p-values are far too small. Pragya Sur and Emmanuel Candès worked '
            "out why, and what the right answer is. <bookmark mark='b'/> Next, Part fifty-nine: high-dimensional "
            'asymptotics.'
        )
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(58)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
