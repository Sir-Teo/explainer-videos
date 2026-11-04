from __future__ import annotations

from videos.stats.stats2.common import *  # noqa: F403

PROBLEMS = [
    r"A fair game to be won by the first to reach a target is stopped when A needs $2$ more points and B needs $3$. "
    r"\ Find A's fair share by Fermat's enumeration and again by Pascal's recursion.",
    r"Prove inclusion--exclusion for three events, \ and the Bonferroni lower bound "
    r"$P(\bigcup_i A_i) \ge \sum_i P(A_i) - \sum_{i<j} P(A_i \cap A_j)$.",
    r"A test has sensitivity and specificity $0.99$; \ the condition has prevalence $1$ in $1{,}000$. \ Find "
    r"$P(\text{condition} \mid +)$, \ and after two positives that err independently given the condition.",
    r"Monty Hall with $n$ doors: \ the host, who knows, opens $n - 2$ goat doors other than yours. \ Show that "
    r"switching to the last closed door wins with probability $(n-1)/n$.",
    r"Use indicators to find the expected number of different faces seen in $n$ rolls of a die. \ How large must $n$ "
    r"be for the expectation to exceed $5$?",
    r"The St.\ Petersburg casino can pay at most $2^{20}$ ducats. \ Show that the game's expected prize is then "
    r"exactly $21$ ducats.",
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
            (r"Fermat counts the futures; \ Pascal averages them", PA),
            (r"equally likely cases: \ Cardano, Galileo, de M\'er\'e", S.MUSEUM),
            (r"counting: \ $n!$, \ $\binom nk$, \ stars and bars", EXACT),
            (r"Bertrand: \ ``at random'' needs a measure", S.ACCENT),
            (r"Kolmogorov's three axioms, \ and $1/e$", EXACT),
            (r"conditioning renormalizes a slice", S.EST),
            (r"posterior odds $=$ prior odds $\times$ likelihood ratio", S.POST),
            (r"$P(E \mid H) \ne P(H \mid E)$", S.RESID),
            (r"Monty Hall: \ the protocol is part of the data", GOAT),
            (r"independence: \ a product rule, \ pairwise $\ne$ mutual", S.LIK),
            (r"random variables push $P$ forward; \ the Cantor staircase", S.EST),
            (r"linearity of expectation needs no independence", EXACT),
            (r"St.\ Petersburg: \ an infinite mean", S.ACCENT),
            (r"generating functions: \ sums become products", S.PRIOR),
            (r"frequency, \ logic, \ belief: \ one set of axioms", GREY_A),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=31, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:8]).arrange(DOWN, aligned_edge=LEFT, buff=0.44),
                      VGroup(*rows[8:]).arrange(DOWN, aligned_edge=LEFT, buff=0.44)).arrange(RIGHT, buff=0.7,
                                                                                            aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 2, \ in fifteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.45)
        if cols.get_bottom()[1] < -3.7:
            cols.height = cols.height - (-3.7 - cols.get_bottom()[1])
            cols.next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "Part two in fifteen lines. <bookmark mark='a'/> Fermat completed the future and counted it; Pascal "
            "averaged over it, and expectation was born. Probability began with equally likely cases, and Galileo "
            "and de Méré showed how easy it is to choose the wrong ones. We learned to count. Bertrand showed that "
            "at random means nothing until a measure is chosen, and Kolmogorov's three axioms made the measure the "
            "foundation; from them came inclusion–exclusion and the one over e of the hat-check problem. "
            "Conditioning renormalizes a slice, and Bayes' theorem, in odds form, multiplies prior odds by a "
            "likelihood ratio. The chance of the evidence given innocence is not the chance of innocence given the "
            "evidence. In Monty Hall, the host's protocol is part of the data. Independence is a product rule, and "
            "pairwise is not mutual. Random variables push probability forward onto numbers, sometimes in strange "
            "ways. Expectation is linear without any independence; the St. Petersburg game has no finite mean; "
            "generating functions turn sums into products. And three different meanings of probability lead to the "
            "same axioms."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=30.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"expectation and linearity", [6, 9, 22]),
            (r"conditioning and Bayes", [15, 26, 33]),
            (r"conditional independence", [5, 36]),
            (r"the likelihood", [9, 22]),
            (r"generating functions", [3, 6]),
            (r"the union bound", [33, 51, 54]),
            (r"measure and singular laws", [43]),
            (r"what probability means", [15, 26]),
        ], font_size=22)
        with self.voiceover(
            "Almost all of it comes back. <bookmark mark='a'/> Expectation and its linearity drive the laws of "
            "averages in Part 6 and estimation in Parts 9 and 22. Bayes' theorem becomes Bayesian statistics in "
            "Parts 15 and 26, and the false discovery rate in Part 33. Conditional independence is the language of "
            "Part 5's joint distributions and Part 36's causal graphs. The likelihood, which Monty Hall showed us "
            "depends on the protocol, is the subject of Parts 9 and 22. Generating functions name the distributions "
            "in Part 3 and prove the central limit theorem in Part 6. The humble union bound holds up multiple "
            "testing and learning theory. Measure theory returns in Part 43; the meaning of probability in Parts "
            "15 and 26."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in this part's README. <bookmark mark='a'/> A problem of points "
            "solved both ways; inclusion–exclusion for three events and a Bonferroni bound; a screening test with "
            "a rarer condition; Monty Hall with many doors; the number of different faces in n rolls, by "
            "indicators; and the St. Petersburg game at a casino with a finite bankroll. Pause here if you want to "
            "try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"W. Feller, \emph{An Introduction to Probability Theory and Its Applications}, vol.~1 (3rd ed., 1968)",
             r"J. Blitzstein \& J. Hwang, \emph{Introduction to Probability} (2nd ed., 2019); \ S. Ross, \emph{A "
             r"First Course in Probability} (10th ed., 2019)",
             r"G. Grimmett \& D. Stirzaker, \emph{Probability and Random Processes} (4th ed., 2020)",
             r"A. Hald, \emph{A History of Probability and Statistics \dots\ before 1750} (1990); \ I. Hacking, "
             r"\emph{An Introduction to Probability and Inductive Logic} (2001)"],
            [r"B. Pascal \& P. de Fermat, letters (1654); \ C. Huygens (1657); \ D. Bernoulli (1738)",
             r"J. Bertrand (1889); \ A. Kolmogorov, \emph{Grundbegriffe} (1933); \ B. de Finetti (1937); \ R. T. Cox "
             r"(1946)",
             r"E. T. Jaynes, ``The well-posed problem'' (1973); \ S. Selvin (1975); \ G. Gigerenzer \& U. Hoffrage "
             r"(1995)",
             r"Royal Statistical Society, statement on \emph{R v Clark} (2001); \ R. Hill (2004); \ J. Halpern (1999)"])
        with self.voiceover(
            "The books and papers this part follows are on screen and in the README: Feller's classic first "
            "volume, the modern textbooks of Blitzstein and Hwang, Ross, and Grimmett and Stirzaker, Hald's history, "
            "and the original papers, from the letters of 1654 to the Royal Statistical Society's statement of 2001."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=2, current=None)
        nxt = VGroup(label(r"Part 3", font_size=30, color=GREY_B), label(r"The Family of Distributions", font_size=48),
                     label(r"why do the same few shapes keep appearing?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Two parts of sixty-five. <bookmark mark='a'/> We can now compute any probability on a finite space "
            "exactly, and we've seen how random variables carry probability onto numbers. But the same few shapes "
            "keep appearing: the bell, the exponential, the Poisson that fitted our shuffled decks. "
            "<bookmark mark='b'/> In 1898 a statistician counted the Prussian cavalrymen killed by the kicks of their "
            "horses, corps by corps and year by year, and found one of those shapes in them. Why do the same few "
            "distributions turn up everywhere? That's Part 3."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(tr.cells[0].animate.set_fill(S.ACCENT, opacity=0.9), tr.cells[1].animate.set_fill(S.ACCENT, opacity=0.9))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
