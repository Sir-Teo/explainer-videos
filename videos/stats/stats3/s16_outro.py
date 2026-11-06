from __future__ import annotations

from videos.stats.stats3.common import *  # noqa: F403

PROBLEMS = [
    r"If $X \sim$ Poisson$(a)$ and $Y \sim$ Poisson$(b)$ are independent, \ show that given $X + Y = n$, \ $X$ is "
    r"binomial$(n,\ a/(a+b))$.",
    r"Show that the exponential is the only continuous law on $(0, \infty)$ with $P(T > s + t \mid T > s) = P(T > t)$ "
    r"for all $s, t \ge 0$.",
    r"$U$ is uniform on $(0, 1)$. \ Find the laws of $U^2$ and of $-2\log U$; \ name both families.",
    r"Show that the minimum of $n$ independent exponential$(\lambda)$ waits is exponential$(n\lambda)$. \ Three bus "
    r"routes each run every 10 minutes on average: \ how long until the first bus?",
    r"Capture--recapture: \ $200$ fish tagged, \ $150$ caught later, \ $12$ of them tagged. \ Compute the "
    r"Lincoln--Petersen and Chapman estimates.",
    r"With $\alpha$ known, write the gamma$(\alpha, \theta)$ density as an exponential family: \ find $\eta$, $T$, "
    r"$A(\eta)$, \ and check that $A'(\eta) = E T$.",
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
            (r"horse kicks fit a Poisson model: \ Bortkiewicz, 1898", S.MUSEUM),
            (r"binomial: \ paths, \ $\binom nk$, \ $np$ and $np(1-p)$", DISC),
            (r"many rare chances $\to$ Poisson; \ Le Cam's bound", DISC),
            (r"geometric and exponential forget the past", DISC),
            (r"capture--recapture: \ the hypergeometric, \ and a biased ratio", S.WORLD),
            (r"the inspection paradox: \ you land in long gaps", S.RESID),
            (r"the normal: \ de Moivre, \ Gauss, \ Herschel--Maxwell", CONT),
            (r"densities transform with the Jacobian; \ Box--Muller", CONT),
            (r"$\chi^2$, $t$, $F$; \ the lighthouse has no mean", CONT),
            (r"order statistics of uniforms are beta; \ tanks", CONT),
            (r"power laws: \ use likelihood, not log--log lines", S.ACCENT),
            (r"generating functions turn sums into products", EXACT),
            (r"mixtures make overdispersion and heavy tails", S.PRIOR),
            (r"exponential families: \ $A'(\eta) = E T$", S.POST),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=30, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.44),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.44)).arrange(RIGHT, buff=0.7,
                                                                                            aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 3, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part three in fourteen lines. <bookmark mark='a'/> The horse-kick counts fit a Poisson model. The binomial counts "
            "paths, with mean n p and variance n p q. Many rare chances make a Poisson, and Le Cam said how closely. "
            "The geometric and the exponential forget the past. Sampling without replacement is hypergeometric, and "
            "the capture–recapture ratio is biased. You land in long gaps between buses. The normal came three ways. "
            "Densities transform with the Jacobian, and two uniforms make two normals. Chi-squared, t and F are "
            "statistics' own distributions, and the lighthouse has no mean. Uniform order statistics are beta, and "
            "they counted tanks. Power laws need likelihood, not straight lines. Generating functions turn sums into "
            "products; mixtures make overdispersion and heavy tails; and exponential families tie most of it "
            "together."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=28.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the normal and sums", [6, 8]),
            (r"$\chi^2$, $t$, $F$", [8, 10, 11, 12]),
            (r"order statistics, the tank problem", [9, 16]),
            (r"exponential families", [9, 22, 24, 45]),
            (r"mixtures, overdispersion", [15, 24, 25]),
            (r"the Poisson process", [17, 40]),
            (r"heavy tails", [30, 60]),
            (r"capture--recapture", [18, 41]),
        ], font_size=22)
        with self.voiceover(
            "And where it comes back. <bookmark mark='a'/> The normal and sums return in the laws of averages of "
            "Part 6 and the sampling theory of Part 8; chi-squared, t and F in every interval and test from Part 8 "
            "on. Order statistics and the tank problem return in estimation and in rank methods. Exponential "
            "families are the backbone of estimation, likelihood and generalized linear models. Mixtures become "
            "Bayesian and mixed models. The Poisson process returns in time series and survival analysis, heavy "
            "tails in robust statistics, and capture–recapture in surveys and missing data."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Splitting a Poisson sum; why only "
            "the exponential is memoryless; two transformations of a uniform; the first of several buses; a "
            "capture–recapture estimate; and the gamma as an exponential family. Pause here if you want to try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"J. Blitzstein \& J. Hwang, \emph{Introduction to Probability} (2nd ed., 2019), chs.~3--8",
             r"G. Casella \& R. Berger, \emph{Statistical Inference} (2nd ed., 2002), chs.~2--5",
             r"N. Johnson, S. Kotz \& N. Balakrishnan, \emph{Continuous Univariate Distributions} (2nd ed., 1994--95)",
             r"W. Feller, \emph{An Introduction to Probability Theory}, vols.~1--2; \ S. Stigler, \emph{The History of "
             r"Statistics} (1986)"],
            [r"S. D. Poisson (1837); \ L. von Bortkiewicz (1898); \ L. Le Cam (1960)",
             r"A. de Moivre (1733); \ C. F. Gauss (1809); \ J. Herschel (1850); \ J. C. Maxwell (1860)",
             r"F. Helmert (1876); \ ``Student'' (1908); \ R. A. Fisher (1924); \ G. Box \& M. Muller (1958)",
             r"C. Petersen (1896); \ D. Chapman (1951); \ R. Ruggles \& H. Brodie (1947)",
             r"A. Clauset, C. Shalizi \& M. Newman (2009); \ L. Leemis \& J. McQueston (2008)"])
        with self.voiceover(
            "The books and papers this part follows are on screen and in the README: Blitzstein and Hwang, Casella "
            "and Berger, the encyclopedic volumes of Johnson, Kotz and Balakrishnan, Feller and Stigler, and the "
            "original papers, from Poisson to Clauset, Shalizi and Newman."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=3, current=None)
        nxt = VGroup(label(r"Part 4", font_size=30, color=GREY_B), label(r"Matrices for Statistics", font_size=48),
                     label(r"a cloud of points in many dimensions: \ what shape is it?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Three parts of sixty-five. <bookmark mark='a'/> We now have a family of distributions for one variable "
            "at a time. But every real data set is a table: heights and weights and incomes and ages, measured on "
            "the same people, moving together. <bookmark mark='b'/> To see the shape of a cloud of points in many "
            "dimensions, its directions of greatest spread, its correlations, its projections, we need the language "
            "of matrices. That's Part 4."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(3)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
