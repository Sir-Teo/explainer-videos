from __future__ import annotations

from videos.stats.stats1.common import *  # noqa: F403

PROBLEMS = [
    r"Show that $\sum_i |x_i - c|$ is minimized by any median of $x_1, \dots, x_n$. \ When is the minimizer not "
    r"unique?",
    r"Show that $\sum_i (x_i - c)^2 = \sum_i (x_i - \bar x)^2 + n(\bar x - c)^2$ \ algebraically, \ and deduce that "
    r"the mean minimizes the left side.",
    r"For the data $1, 2, 3, 4, 100$, \ compute the mean, median, standard deviation (divisor $n$), MAD and IQR. \ Which "
    r"describe this data well?",
    r"Show that $r$ is unchanged when $x$ becomes $a + bx$ with $b > 0$, \ and changes sign when $b < 0$. \ What "
    r"happens to the slope of $y$ on $x$?",
    r"Construct a two-group table in which a treatment has the higher success rate in both groups and the lower "
    r"rate overall. \ Write each overall rate as a weighted average.",
    r"If $X$ is exponential with mean $\mu$, \ $\mathrm{SD}(X) = \mu$. \ Use the delta method to find a "
    r"transformation $g$ for which $\mathrm{SD}(g(X))$ does not depend on $\mu$.",
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
            (r"population $\theta$, \ sample $\hat\theta$", S.TRUTH),
            (r"the World: \ a population whose truth we know", S.WORLD),
            (r"histograms: \ bin width is a bias--variance choice", S.EST),
            (r"mean, median, mode: \ minimizers of losses", MEAN),
            (r"variance: \ Pythagoras in $\mathbb R^n$", DEV),
            (r"the ECDF, \ quantiles, \ box plots", MEDIAN),
            (r"skew, \ heavy tails, \ power laws", S.ACCENT),
            (r"QQ plots: \ near a line for the right family", S.EST),
            (r"Box--Cox: \ the log is $\lambda = 0$", S.LIK),
            (r"correlation $= \cos\theta$", MEDIAN),
            (r"same statistics, \ different pictures", S.MUSEUM),
            (r"aggregation can reverse a comparison", S.TREAT),
            (r"honest graphics: \ position, \ zero baselines", GREY_A),
            (r"every statistic has a sampling distribution", S.EST),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=31, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8,
                                                                                            aligned_edge=UP)
        if cols.width > 13.2:
            cols.width = 13.2
        head = label(r"Part 1, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part one in fourteen lines. <bookmark mark='a'/> A population has parameters, gold; a sample has "
            "statistics, blue; and the World is a population we built so we'd always know the truth. Histograms "
            "show shape, and their bin width trades noise against blur. The mean, the median and the mode are the "
            "solutions of three optimization problems, and squares won because of Pythagoras. The empirical "
            "distribution function holds the data exactly; quantiles and box plots read it. Some distributions "
            "have tails so heavy that their moments don't exist. QQ plots test a shape by asking for a straight "
            "line, and the Box–Cox family finds the transformation that straightens it. Correlation is the cosine "
            "of an angle. The same summaries can hide entirely different pictures; combining groups can reverse a "
            "comparison; and a picture can lie by its choice of axis or its encoding. And every statistic we "
            "compute is random: it has a distribution of its own."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.45), run_time=24.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the sampling distribution", [6, 8, 11]),
            (r"estimators as minimizers", [9, 21, 22]),
            (r"sums of squares as Pythagoras", [12, 13, 23]),
            (r"the ECDF and quantiles", [6, 16, 48]),
            (r"heavy tails", [3, 30, 60]),
            (r"QQ plots and transformations", [12, 24]),
            (r"Simpson's paradox", [14, 36]),
            (r"the Coverage Board", [8, 11, 65]),
        ], font_size=22)
        with self.voiceover(
            "Almost every idea here comes back. <bookmark mark='a'/> The sampling distribution is the subject of "
            "Parts 6, 8 and 11. Estimators as minimizers of a loss are the subject of estimation theory and "
            "optimization. Pythagoras returns in least squares and the analysis of variance; the empirical "
            "distribution function returns as the bootstrap and, in the PhD stage, as empirical process theory. "
            "Heavy tails return in robust statistics, Simpson's paradox in causal inference, and the Coverage "
            "Board in every part that makes a promise."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                 lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "Six problems to work on, with full solutions in this part's README. <bookmark mark='a'/> Two are about "
            "centres as minimizers; one asks you to summarize five numbers, one of them a hundred; one is about how "
            "correlation behaves under a change of units; one asks you to build your own Simpson's paradox; and the "
            "last asks for the transformation that tames an exponential's spread. Pause here if you want to try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"J. W. Tukey, \emph{Exploratory Data Analysis} (1977)",
             r"D. Freedman, R. Pisani \& R. Purves, \emph{Statistics} (4th ed., 2007)",
             r"W. S. Cleveland, \emph{Visualizing Data} (1993); \ E. Tufte, \emph{The Visual Display of "
             r"Quantitative Information} (1983)",
             r"S. M. Stigler, \emph{The History of Statistics} (1986) and \emph{The Seven Pillars of Statistical "
             r"Wisdom} (2016); \ I. Hacking, \emph{The Taming of Chance} (1990)"],
            [r"J. Graunt, \emph{Natural and Political Observations \dots\ upon the Bills of Mortality} (1662); \ "
             r"J. Arbuthnot (1710)",
             r"A. Quetelet (1846); \ F. Galton (1886); \ V. Pareto (1896); \ W. S. Robinson (1950)",
             r"G. Box \& D. Cox (1964); \ M. Wilk \& R. Gnanadesikan (1968); \ F. Anscombe (1973)",
             r"W. Cleveland \& R. McGill (1984); \ A. Clauset, C. Shalizi \& M. Newman (2009); \ P. Westfall (2014)",
             r"J. Matejka \& G. Fitzmaurice, ``Same stats, different graphs'' (2017)"])
        with self.voiceover(
            "The books and papers this part follows are listed here and in the README: Tukey's Exploratory Data "
            "Analysis, the classic textbook by Freedman, Pisani and Purves, Cleveland and Tufte on graphics, and "
            "Stigler's histories, along with the original papers from Graunt to Matejka and Fitzmaurice."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=1, current=None)
        nxt = VGroup(label(r"Part 2", font_size=30, color=GREY_B), label(r"Chance, Counted", font_size=48),
                     label(r"a game interrupted at two points to one: \ how should the stake be split?",
                           font_size=28, color=GREY_A)).arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "That's the first course on the transcript: one part of sixty-five. <bookmark mark='a'/> We ended with "
            "a discovery: every summary of a sample is random, and has a distribution of its own. To reason about "
            "that, we need a precise language for chance. <bookmark mark='b'/> It was invented in 1654, in letters "
            "between Pascal and Fermat, about a game of dice interrupted at two points to one. How should the stake "
            "be divided between the players? That question, and the theory of probability it started, is Part 2."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(tr.cells[0].animate.set_fill(S.ACCENT, opacity=0.9))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
