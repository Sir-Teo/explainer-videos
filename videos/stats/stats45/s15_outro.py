from __future__ import annotations

from videos.stats.stats45.common import *  # noqa: F403

PROBLEMS = [
    r"Show that $(X + \sqrt n/2)/(n + \sqrt n)$ has constant risk for $X \sim \mathrm{Bin}(n, p)$, \ and deduce that it is minimax.",
    r"Prove that $\max X_i$ is complete for $U(0, \theta)$, \ and find the UMVUE of $\theta$.",
    r"Show that $(-1)^X$ is the only unbiased estimator of $e^{-2\lambda}$ from one Poisson count.",
    r"Use Basu's theorem to show that $\bar X$ and $X_{(n)} - X_{(1)}$ are independent for $N(\mu, 1)$ data.",
    r"Find the Pitman estimator for $f(x) = e^{-(x - \theta)}$, $x > \theta$, \ and show it is $\min x_i - 1/n$.",
    r"For $\delta = (1 - c/\|X\|^2) X$, \ $X \sim N_p(\theta, I)$, \ show that SURE is minimized at $c = p - 2$.",
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
            (r"Stein (1956): \ $X$ is inadmissible for $p \ge 3$", JSC), (r"risk, \ admissibility, \ minimax, \ Bayes", MMC),
            (r"risk sets; \ least favourable priors", MMC), (r"complete classes; \ limits of Bayes rules", BAYESC),
            (r"exponential families: \ $A$ and $A^*$", MLEC), (r"sufficiency, \ minimality, \ completeness", MLEC),
            (r"Rao--Blackwell, \ Lehmann--Scheff\'e; \ $(-1)^X$", ADMC),
            (r"Basu; \ Cox's instruments; \ conditioning", ADMC), (r"Cram\'er--Rao, \ Bhattacharyya, \ Chapman--Robbins", S.PRIOR),
            (r"equivariance; \ Pitman's estimator", S.PRIOR), (r"Stein's lemma, \ SURE, \ James--Stein", JSC),
            (r"Brown: \ admissibility $\iff$ recurrence", JSC), (r"Baranchik, \ Strawderman", JSC), (r"Robbins, \ the NPMLE, \ regret", BAYESC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 45, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-five in fourteen lines. Stein's paradox. Wald's risk, admissibility, "
            "minimax and Bayes rules, and the risk set with its least favourable prior. Complete classes, and "
            "admissible rules as limits of Bayes rules. Exponential families as a convex function and its conjugate. "
            "Sufficiency, minimality and completeness; Rao–Blackwell and Lehmann–Scheffé, with the absurd minus one "
            "to the X. <bookmark mark='b'/> Basu's theorem and Cox's two instruments. The information bounds of "
            "Cramér and Rao, Bhattacharyya, and Chapman and Robbins. Pitman's equivariant estimator. Stein's lemma, "
            "SURE and James–Stein; Brown's link between admissibility and recurrence; Baranchik's and Strawderman's "
            "minimax rules; and Robbins's empirical Bayes, with a numerical NPMLE approximation and the separate "
            "asymptotic theory for vanishing regret."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:7]], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[7:]], lag_ratio=0.3), run_time=5.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(45, r"what makes an estimator good: \ risk, \ sufficiency, \ shrinkage",
                            r"tests and intervals judged by their size and coverage alone",
                            r"Part 46: \ optimal tests, \ Neyman--Pearson to Lehmann, \ and what an interval can promise")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. This one set out what makes an estimator good. <bookmark "
            "mark='b'/> Tests and intervals have so far been judged by whether they keep their size and coverage, as the "
            "Board checks. <bookmark mark='c'/> Part forty-six asks when a test is optimal, from the Neyman–Pearson lemma to "
            "Lehmann's uniformly most powerful unbiased tests, and what a confidence interval can honestly promise."
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
            (r"risk sets and least favourable priors, \ for tests", [46]), (r"local asymptotic minimax: \ H\'ajek and Le Cam", [47]),
            (r"Bayes rules and their frequentist risk, \ asymptotically", [53]), (r"minimax rates, \ Le Cam, \ Assouad, \ Fano", [50]),
            (r"shrinkage and empirical Bayes in high dimensions", [52]),
        ], font_size=22)
        self.add(card.head)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part forty-six draws risk sets and least favourable priors for "
            "tests. Part forty-seven gives the local asymptotic minimax theorem of Hájek and Le Cam. Part fifty-three "
            "studies the frequentist risk of Bayes rules as the sample grows. Part fifty computes minimax rates with "
            "the methods of Le Cam, Assouad and Fano. And Part fifty-two takes empirical Bayes and shrinkage into high "
            "dimensions."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The binomial minimax rule; completeness "
            "of the uniform maximum and its UMVUE; the absurd unbiased estimator; Basu's theorem for the range; Pitman's "
            "estimator for a shifted exponential; and the SURE-optimal amount of shrinkage. Pause here if you want to try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"E. Lehmann \& G. Casella, \emph{Theory of Point Estimation} (2nd ed. 1998); \ J. Berger, \emph{Statistical Decision Theory} (1985)",
             r"T. Ferguson, \emph{Mathematical Statistics: A Decision Theoretic Approach} (1967); \ R. Keener, \emph{Theoretical Statistics} (2010)",
             r"L. Brown, \emph{Fundamentals of Statistical Exponential Families} (1986)",
             r"B. Efron \& T. Hastie, \emph{Computer Age Statistical Inference} (2016)"],
            [r"A. Wald (1939, 1950); \ C. R. Rao (1945); \ D. Blackwell (1947); \ P. Halmos \& L. Savage (1949)",
             r"E. Lehmann \& H. Scheff\'e (1950); \ D. Basu (1955); \ C. Stein (1956, 1981); \ H. Robbins (1956); \ D. Cox (1958)",
             r"W. James \& C. Stein (1961); \ A. Baranchik (1970); \ L. Brown (1971); \ W. Strawderman (1971)",
             r"J. Kiefer \& J. Wolfowitz (1956); \ W. Jiang \& C.-H. Zhang (2009); \ B. Efron (2014)"])
        with self.voiceover(
            "The books this part follows: Lehmann and Casella's Theory of Point Estimation, Berger's Statistical Decision "
            "Theory, Ferguson, Keener, and Brown's monograph on exponential families, with Efron and Hastie; and the papers "
            "from Wald to Jiang and Zhang."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=45, current=None)
        nxt = VGroup(label(r"Part 46", font_size=30, color=GREY_B), label(r"The Theory of Testing and Confidence", font_size=48),
                     label(r"when is a test optimal, \ and what can an interval honestly promise?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Forty-five parts of sixty-five. <bookmark mark='a'/> Best is a word that needs a definition: a risk, a class of "
            "rules, or a prior, and in three dimensions the obvious answer loses. <bookmark mark='b'/> Next, Part "
            "forty-six: the theory of testing and confidence."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(45)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
