from __future__ import annotations

from videos.stats.stats18.common import *  # noqa: F403

PROBLEMS = [
    r"A town of 2,000; \ an SRS of 400 gives $\bar y = 52$, \ $s = 20$. \ The SE with and without the fpc.",
    r"Show that for an SRS without replacement, \ $\mathrm{Cov}(R_i, R_j) = -f(1 - f)/(N - 1)$.",
    r"Two strata, \ $N_1 = N_2$, \ $S_1 = 1$, \ $S_2 = 3$, \ $n = 100$: \ Neyman's allocation, \ and its variance vs proportional.",
    r"A self-selected sample of 1\% of a population has $\rho_{R,Y} = 0.01$. \ Its effective sample size.",
    r"Cluster sample, \ 30 per cluster, \ ICC 0.05: \ the design effect, \ and $n_{\text{eff}}$ for 1,500 interviews.",
    r"Show that the Horvitz--Thompson total is unbiased for any design with all $\pi_i > 0$.",
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
            (r"the \emph{Digest}: \ 2.4 million, \ wrong", RED), (r"coverage and nonresponse bias", RESP),
            (r"Meng: \ quality $\times$ quantity $\times$ difficulty", OBS), (r"$n_{\text{eff}}$: \ 34,588 ballots, \ worth 6", RES),
            (r"design-based: \ the randomness is ours", HIT), (r"SRS: \ the fpc; \ $\pm 3$ points from 1,000", BLUE),
            (r"strata: \ Neyman allocation", OBS), (r"clusters: \ the design effect", RESP),
            (r"PPS: \ SD reduced by a factor of 174", HIT), (r"Horvitz--Thompson; \ Basu's elephants", OBS),
            (r"ratio and regression estimators", FIT), (r"weights: \ post-strata, \ raking", WEIGHT),
            (r"MAR vs MNAR nonresponse", RES), (r"1948, \ 2016, \ 2020", GREY_A),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 18, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part eighteen in fourteen lines. <bookmark mark='a'/> The Literary Digest's two point four million "
            "ballots were wrong because of whom they reached and who replied. Meng's identity splits any sample's "
            "error into data quality, quantity and difficulty, and showed the World's Digest worth six random voters."
            " Design-based inference puts the randomness in our own lottery, and a simple random sample of a thousand"
            " gives about three percentage points of sampling margin for a large population under simple random "
            "sampling. Stratification with Neyman's allocation halves the error; clustering costs precision, measured"
            " by the design effect; probability proportional to size can save it a hundredfold. Horvitz–Thompson "
            "weighting is unbiased for any design, though Basu's elephants show that isn't everything. Ratio and "
            "regression estimators borrow strength from known totals. Weights and raking correct what they can see, "
            "which is why the polls of 1948, 2016 and 2020 went wrong in different ways."       ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=32.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"prediction and its honest evaluation", [19]), (r"the BSc capstone: \ an analysis from question to report", [20]),
            (r"multilevel models; \ MRP for polls", [25]), (r"potential outcomes: \ causal inference as missing data", [35]),
            (r"missing data: \ MCAR, \ MAR, \ MNAR; \ multiple imputation", [41]), (r"semiparametric efficiency of weighting", [49]),
            (r"privacy in surveys and censuses", [63]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 19 turns to prediction and how to evaluate it honestly, "
            "and Part 20, the bachelor's capstone, takes an analysis from question to report. Part 25 builds "
            "multilevel models and the MRP method pollsters now use. Part 35 treats causal inference as a "
            "missing-data problem, with Horvitz–Thompson weights in a new role. Part 41 gives missing data its full "
            "theory. Part 49 shows when weighting is efficient. And Part 63 asks how a census can publish its counts "
            "without revealing anyone."       ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The finite-population correction "
            "in a town; the covariance of inclusion indicators; Neyman's allocation for two strata; an effective "
            "sample size from Meng's identity; a design effect; and the unbiasedness of Horvitz–Thompson. Pause here "
            "if you want to try them."       ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. Lohr, \emph{Sampling: Design and Analysis} (3rd ed., 2022)",
             r"W. Cochran, \emph{Sampling Techniques} (3rd ed., 1977); \ L. Kish, \emph{Survey Sampling} (1965)",
             r"C.-E. S\"arndal, B. Swensson \& J. Wretman, \emph{Model Assisted Survey Sampling} (1992)",
             r"R. Groves et al., \emph{Survey Methodology} (2nd ed., 2009)"],
            [r"J. Neyman (1934); \ A. Bowley (1913); \ A. Kiær (1895); \ P.-S. Laplace (1802)",
             r"M. Hansen \& W. Hurwitz (1943); \ D. Horvitz \& D. Thompson (1952); \ D. Basu (1971)",
             r"W. E. Deming \& F. Stephan (1940); \ P. Squire (1988); \ F. Mosteller et al.\ (1949)",
             r"X.-L. Meng (2018); \ AAPOR task force reports (2017, 2021)"])
        with self.voiceover(
            "The books and papers this part follows: Sharon Lohr's Sampling, Cochran's and Kish's classics, Särndal, "
            "Swensson and Wretman's model-assisted survey sampling, and Groves and colleagues' survey methodology, "
            "with the papers from Laplace and Neyman to Meng and the polling post-mortems."        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=18, current=None)
        nxt = VGroup(label(r"Part 19", font_size=30, color=GREY_B), label(r"Learning from Data", font_size=48),
                     label(r"predicting well, \ and knowing how well you predict", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Eighteen parts of sixty-five, the eighth of Stage II. <bookmark mark='a'/> We can now say whom a sample "
            "speaks for, and how to make it speak for more. <bookmark mark='b'/> Next, a different goal: prediction. "
            "In the 1960s Frederick Mosteller and David Wallace settled who wrote twelve disputed Federalist papers, "
            "Alexander Hamilton or James Madison, by counting words like upon and whilst. Part 19: learning from "
            "data."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(18)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
