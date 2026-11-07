from __future__ import annotations

from videos.stats.stats46.common import *  # noqa: F403

PROBLEMS = [
    r"Find the UMP level-$\alpha$ test of $\lambda \le 1$ vs $\lambda > 1$ from $n$ Poisson counts, \ and its power function.",
    r"Show that the two-sided $z$ test of $\mu = 0$ is UMPU, \ using $E_0\phi = \alpha$ and $E_0[\bar X \phi] = 0$.",
    r"For $U(0, \theta)$, \ show that $\phi = \mathbf 1\{\max x_i > \theta_0 (1 - \alpha)^{1/n}\}$ is UMP for $\theta \le \theta_0$, \ but not unique.",
    r"Show that $\max(0, Z)^2$ has the law $\tfrac12 \chi^2_0 + \tfrac12 \chi^2_1$ under $\mu = 0$.",
    r"Prove that closed testing with level-$\alpha$ local tests controls the familywise error rate.",
    r"Show that $\min_{\xi \in (0,1)} 1/(\xi p^{\xi - 1}) = -e\,p \log p$ \ for $p < 1/e$.",
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
            (r"Behrens--Fisher: \ Welch, \ Linnik", H1C), (r"Neyman--Pearson, \ randomized; \ the LP", UMPC),
            (r"MLR and Karlin--Rubin; \ no UMP two-sided", UMPC), (r"UMPU; \ Neyman structure; \ the $t$ test", UMPC),
            (r"invariance; \ Hunt--Stein; \ the $F$ test", UMPC), (r"Wilks; \ Chernoff's boundary mixture", S.PRIOR),
            (r"inversion; \ belts; \ UMA sets; \ Pratt", CIC),
            (r"Fieller; \ Gleser--Hwang", REJC), (r"Feldman--Cousins vs flip-flopping", CIC),
            (r"Scheff\'e; \ closed testing", S.PRIOR), (r"Welch's uniform; \ Buehler's subsets", REJC),
            (r"Berger--Sellke; \ $-e\,p\log p$", CIC), (r"Pearson's $\chi^2$; \ Lilliefors; \ Durbin", H0C),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 46, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-six in thirteen lines. The Behrens–Fisher problem, Welch's answer and "
            "Linnik's theorem. The Neyman–Pearson lemma with its randomization and its linear programme. Monotone "
            "likelihood ratio and Karlin–Rubin, and the absence of a UMP two-sided test in the binomial example. "
            "Unbiased tests by Neyman structure, and the t test's optimality. Invariance, Hunt–Stein and the F test. "
            "Wilks's theorem and Chernoff's boundary. Confidence sets by inversion. <bookmark mark='b'/> Fieller's "
            "unbounded sets and Gleser and Hwang's impossibility. Feldman and Cousins against flip-flopping. "
            "Scheffé's projections and closed testing. Welch's uniform example and Buehler's recognizable subsets. "
            "Berger and Sellke's bounds. And goodness of fit, with Lilliefors and Durbin."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:7]], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[7:]], lag_ratio=0.3), run_time=5.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(46, r"exact optimal tests and honest confidence sets",
                            r"finite samples and exact distributions",
                            r"Part 47: \ asymptotic statistics: \ contiguity, \ LAN, \ the convolution theorem, \ the delta method")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. This one found exact optimal tests and honest confidence "
            "sets. <bookmark mark='b'/> But exact theory needs exact distributions, which most models do not have. "
            "<bookmark mark='c'/> Part forty-seven is asymptotic statistics: contiguity, local asymptotic normality, the "
            "convolution theorem that makes the MLE optimal, and the delta method, proved."
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
            (r"Wilks, \ score and Wald tests, \ proved; \ local power", [47]), (r"Kolmogorov--Smirnov and Durbin's processes", [48]),
            (r"selective inference: \ conditioning on the selection", [56]), (r"conformal and permutation tests, \ exact", [57]),
            (r"e-values and anytime-valid confidence sequences", [58]),
        ], font_size=22)
        self.add(card.head)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part forty-seven proves Wilks's theorem and the local power of"
            " the score and Wald tests. Part forty-eight studies the processes behind Kolmogorov–Smirnov. Part "
            "fifty-six conditions on selection, while chapter ten examined recognizable subsets, which need not be "
            "ancillary. Part fifty-seven builds exact distribution-free tests. And Part fifty-eight turns tests into "
            "e-values and confidence sequences that stay valid however long you watch."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> A UMP Poisson test; the z test as UMPU; "
            "the uniform's non-unique UMP test; Chernoff's mixture; closed testing's error control; and the p-value "
            "calibration. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"E. Lehmann \& J. Romano, \emph{Testing Statistical Hypotheses}",
             r"J. Shao, \emph{Mathematical Statistics} (2nd ed. 2003); \ M. Schervish, \emph{Theory of Statistics} (1995)",
             r"Y. Linnik, \emph{Statistical Problems with Nuisance Parameters} (1968)"],
            [r"J. Neyman \& E. Pearson (1933); \ J. Neyman (1937); \ S. Wilks (1938); \ B. Welch (1938, 1947)",
             r"S. Karlin \& H. Rubin (1956); \ H. Chernoff (1954); \ R. Buehler (1959); \ J. Pratt (1961)",
             r"R. Marcus, \ E. Peritz \& K. Gabriel (1976); \ L. Gleser \& J. Hwang (1987); \ J. Berger \& T. Sellke (1987)",
             r"G. Feldman \& R. Cousins (1998); \ T. Sellke, \ M. Bayarri \& J. Berger (2001); \ H. Lilliefors (1967)"])
        with self.voiceover(
            "The books this part follows: Lehmann and Romano's Testing Statistical Hypotheses, Shao, Schervish, and "
            "Linnik's monograph; and the papers from Neyman and Pearson to Feldman and Cousins."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=46, current=None)
        nxt = VGroup(label(r"Part 47", font_size=30, color=GREY_B), label(r"Asymptotic Statistics", font_size=48),
                     label(r"what is the best estimator in large samples, \ and why is ``best'' so hard to define?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Forty-six parts of sixty-five. <bookmark mark='a'/> An optimal test is one that wins inside a class, unbiased "
            "or invariant, and an honest interval is sometimes infinite. <bookmark mark='b'/> Next, Part forty-seven: "
            "asymptotic statistics."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(46)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
