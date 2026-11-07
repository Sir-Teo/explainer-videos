from __future__ import annotations

from videos.stats.stats13.common import *  # noqa: F403

PROBLEMS = [
    r"Six plots, three by lot get a new variety: \ yields 14, 16, 18 (new) and 10, 11, 15 (old). \ Find the exact "
    r"randomization $p$-value for the difference in means.",
    r"In a one-way layout, \ show $\text{SST} = \text{SSB} + \text{SSW}$: \ the cross term vanishes.",
    r"A $2^2$ factorial gives $(1) = 20$, \ $a = 30$, \ $b = 24$, \ $ab = 40$. \ Find the effects of A, B and AB by Yates's algorithm.",
    r"A $2^{5-1}$ design has $E = ABCD$. \ Give the defining relation, \ its resolution, \ and the aliases of $A$ and $AB$.",
    r"Straight-line regression on $[-1, 1]$: \ show $\det M$ is the design's variance of $x$, \ and find the D-optimal design.",
    r"How many plots per variety detect $\delta = 2.5$ with $\sigma = 4$, \ 80\% power, \ $\alpha = 0.05$ \ (normal approximation)?",
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
            (r"Rothamsted; \ design the data", DATA), (r"replicate, \ randomize, \ control locally", OBS),
            (r"the randomization distribution", S.LIK), (r"randomization balances the unseen", S.WORLD),
            (r"ANOVA: \ SST = SSB + SSW, \ $F$", FIT), (r"orthogonal contrasts; \ Tukey, \ Dunnett, \ Scheff\'e", S.PRIOR),
            (r"blocks: \ the soil leaves the error", BLOCK), (r"Latin squares; \ crossovers", S.ALT),
            (r"factorials: \ every plot, \ every question", OBS), (r"fractions, \ aliases, \ resolution", S.POST),
            (r"response surfaces: \ climb, \ then fit a quadratic", S.POST), (r"split plots: \ the right error", RES),
            (r"D-optimality; \ power; \ CUPED, \ SRM", HIT),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=27, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 13, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part thirteen in thirteen lines. <bookmark mark='a'/> Fisher found that seventy years of records couldn't answer "
            "a question, and decided to design the data instead. Replicate, randomize, and control locally. The randomization "
            "itself gives an exact test, with no model of the soil, and it balances every variable nobody measured. The analysis "
            "of variance splits the sum of squares into perpendicular pieces, and F compares them; orthogonal contrasts ask "
            "sharper questions, and Tukey, Dunnett and Scheffé pay honestly for asking many. Blocks take the soil out of the "
            "error; Latin squares do it two ways at once, and crossovers use each patient as a block. Factorials use every "
            "plot for every question and see interactions; fractions trade aliases for runs; response surfaces climb and then "
            "fit a quadratic. Split plots need the error from the scale of their randomization. D-optimal designs put the "
            "observations where they inform; power calculations size the experiment; and online, CUPED and the sample-ratio "
            "check carry it all to millions of users."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=30.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"logistic and Poisson regression for counts", [14]), (r"rank and resampling tests", [16]), (r"survey design", [18]),
            (r"the linear model in depth", [23]), (r"mixed models: \ split plots and clusters", [25]),
            (r"thousands of tests, \ the FDR", [33]), (r"potential outcomes, \ interference", [35, 62]),
            (r"sequential and adaptive experiments", [58]),
        ], font_size=22)
        intro = label('Where experimental design returns', font_size=36)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Outcomes that are counts and yes-or-no answers, in the next part; rank "
            "and resampling tests in Part 16; the design of surveys, a cousin of experimental design, in Part 18; the linear "
            "model in full in Part 23; mixed models, which handle split plots and clustered data in general, in Part 25; the "
            "false discovery rate in Part 33; potential outcomes and interference in Parts 35 and 62; and experiments that "
            "adapt as they run in Part 58."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> An exact randomization test by hand; the "
            "analysis-of-variance identity; Yates's algorithm on a small factorial; the aliases of a half fraction; the "
            "D-optimal design for a straight line; and a sample size. Each takes a page or less. Pause here if you want to try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"R. A. Fisher, \emph{The Design of Experiments} (1935)",
             r"G. Box, J. S. Hunter \& W. G. Hunter, \emph{Statistics for Experimenters} (2nd ed., 2005)",
             r"D. Montgomery, \emph{Design and Analysis of Experiments} (10th ed., 2019); \ W. Cochran \& G. Cox, \emph{Experimental Designs} (1957)",
             r"R. Kohavi, D. Tang \& Y. Xu, \emph{Trustworthy Online Controlled Experiments} (2020)"],
            [r"C. S. Peirce \& J. Jastrow (1884); \ R. A. Fisher (1921, 1926); \ R. A. Fisher \& W. Mackenzie (1923)",
             r"F. Yates (1935, 1936, 1937); \ D. Finney (1945); \ R. Plackett \& J. Burman (1946); \ G. Box \& K. Wilson (1951)",
             r"J. Tukey (1953); \ H. Scheff\'e (1953); \ C. Dunnett (1955); \ C. Daniel (1959)",
             r"K. Smith (1918); \ J. Kiefer \& J. Wolfowitz (1960); \ A. Deng et al. (2013); \ A. Gelman \& J. Carlin (2014)"])
        with self.voiceover(
            "The books and papers this part follows: Fisher's Design of Experiments, Box, Hunter and Hunter, Montgomery, "
            "Cochran and Cox, and Kohavi, Tang and Xu, with the papers from Peirce and Jastrow to CUPED."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=13, current=None)
        nxt = VGroup(label(r"Part 14", font_size=30, color=GREY_B), label(r"Counts and Categories", font_size=48),
                     label(r"27 January 1986: \ a chart that left out the flights with no damage", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Thirteen parts of sixty-five, the third of Stage II. <bookmark mark='a'/> We can now design an experiment whose "
            "answer has a defensible uncertainty assessment, and analyse it the way it was run. <bookmark mark='b'/> Many examples so far have used "
            "measurements. Many of the questions that matter most have yes-or-no answers, or counts. On the "
            "evening of the twenty-seventh of January, 1986, engineers and managers discussed whether cold weather would make "
            "a rocket's seals fail, using a chart that left out the flights that had no damage. Part 14: counts and categories."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(13)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
