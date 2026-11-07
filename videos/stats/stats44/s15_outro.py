from __future__ import annotations

from videos.stats.stats44.common import *  # noqa: F403

PROBLEMS = [
    r"Show that $E[X \mid \mathcal G]$ minimizes $E(X - Z)^2$ over $\mathcal G$-measurable $Z$, \ and that it is unique a.s.",
    r"For a fair $\pm 1$ walk from $a$, \ stopped at $0$ or $b$, \ derive $E\tau = a(b - a)$ from $S_n^2 - n$.",
    r"Show that $(q/p)^{S_n}$ is a martingale for a $p$-coin walk, \ and derive the probability of reaching $b$.",
    r"For a two-state chain with $P(1 \mid 1) = a$, $P(1 \mid 0) = b$, \ find $\pi_1$ and the lag-$k$ autocorrelation $(a - b)^k$.",
    r"Use McDiarmid to show that the empty-bin count $Z$ satisfies $P(|Z - EZ| \ge t) \le 2e^{-2t^2/n}$.",
    r"Derive the Nelson--Aalen bracket and its estimator $\sum d_j/Y_j^2$; distinguish them.",
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
            (r"Markov: \ \emph{Onegin}'s letters, \ a dependent law of large numbers", VOWC), (r"$E[X \mid \mathcal G]$: \ Radon--Nikodym, \ projection", CHAINC),
            (r"martingales: \ likelihood ratios, \ P\'olya's urn", MARTC), (r"optional stopping; \ ruin; \ doubling fails", MARTC),
            (r"Ville: \ $P(\sup M \ge 1/\alpha) \le \alpha$", MARTC), (r"convergence: \ upcrossings; \ reverse martingales", MARTC),
            (r"Azuma, \ McDiarmid, \ Freedman", S.PRIOR), (r"the martingale CLT; \ AR(1) and its unit root", S.PRIOR),
            (r"drift and minorization; \ the MCMC CLT", CHAINC), (r"coupling, \ mixing, \ seven shuffles, \ P\'olya", CHAINC),
            (r"Brownian motion; \ Donsker; \ Dickey--Fuller", S.ALT), (r"the LIL; \ counting processes", S.ALT),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 44, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part forty-four in twelve lines. <bookmark mark='a'/> Markov counted Onegin's letters to show that the "
            "law of large numbers survives dependence. Conditional expectation is a Radon–Nikodym derivative and, for"
            " square-integrable variables, a projection. Martingales are fair games: likelihood ratios under the "
            "null, Pólya's urn. Optional stopping cannot beat a fair game, unless its conditions fail, as the "
            "doubling strategy does. Ville's inequality bounds a nonnegative martingale's chance of ever growing "
            "large, which makes betting a valid test at any time. Upcrossings make martingales converge, and reverse "
            "martingales prove the strong law and outline de Finetti through conditional factorization. Azuma and "
            "Freedman control adapted increments; McDiarmid controls functions of independent inputs. and the "
            "martingale central limit theorem gives normal limits, until a unit root breaks it. Drift, minorization, "
            "irreducibility, aperiodicity and suitable moments give the stated MCMC central limit theorem. Coupling "
            "measures mixing, seven Gilbert–Shannon–Reeds riffles bring total variation below one half, and random "
            "walks return in two dimensions but not three. Brownian motion is the standardized limit of centered "
            "independent finite-variance walks, which explains Dickey and Fuller. And the iterated logarithm and "
            "counting processes close the part."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=38.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(44, r"tools for limits in time: \ martingales, \ chains, \ Brownian motion",
                            r"estimators judged only by their limits",
                            r"Part 45: \ the theory of estimation: \ sufficiency, \ unbiasedness, \ Cram\'er--Rao, \ decisions")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. This one built the tools for limits in time. <bookmark "
            "mark='b'/> But an estimator is not judged by its limit alone: at a finite sample size, some estimators are "
            "better than others, and some can be proved best. <bookmark mark='c'/> Part forty-five is the theory of "
            "estimation: sufficiency, unbiasedness, the Cramér–Rao bound, and statistical decision theory."
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
            (r"sufficiency and Rao--Blackwell, \ as conditional expectations", [45]), (r"the score is a martingale: \ asymptotics of the MLE", [47]),
            (r"Donsker for empirical processes", [48]), (r"posterior consistency, \ beyond Doob's theorem", [53]),
            (r"Ville's inequality: \ e-values and confidence sequences", [58]),
        ], font_size=22)
        self.add(card.head)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part forty-five's Rao–Blackwell theorem is a conditional expectation. "
            "Part forty-seven treats the score as a martingale. Part forty-eight extends Donsker's theorem to empirical "
            "processes. Part fifty-three goes beyond Doob's posterior consistency. And Part fifty-eight builds e-values and "
            "confidence sequences from Ville's inequality."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Conditional expectation as the "
            "best predictor; the expected length of a fair game; de Moivre's martingale; a two-state chain's "
            "stationary law and autocorrelations; McDiarmid for empty bins; and the Nelson–Aalen bracket and its "
            "observed-event variance estimator. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"D. Williams, \emph{Probability with Martingales} (1991); \ R. Durrett, \emph{Probability: Theory and Examples} (5th ed. 2019)",
             r"S. Meyn \& R. Tweedie, \emph{Markov Chains and Stochastic Stability} (2nd ed. 2009); \ P. Hall \& C. Heyde (1980)",
             r"D. Levin, \ Y. Peres \& E. Wilmer, \emph{Markov Chains and Mixing Times} (2nd ed. 2017)",
             r"P. K. Andersen, \ \O. Borgan, \ R. Gill \& N. Keiding, \emph{Statistical Models Based on Counting Processes} (1993)"],
            [r"A. A. Markov (1906, 1913); \ \'E. Borel (1909); \ N. Wiener (1923); \ A. Khinchin (1924); \ G. P\'olya (1921)",
             r"J. Ville (1939); \ J. Doob (1949, 1953); \ M. Donsker (1951); \ K. Azuma (1967); \ D. McLeish (1974)",
             r"D. Freedman (1975); \ O. Aalen (1978); \ R. Rebolledo (1980); \ C. McDiarmid (1989)",
             r"D. Bayer \& P. Diaconis (1992); \ K. Mengersen \& R. Tweedie (1996)"])
        with self.voiceover(
            "The books this part follows: Williams's Probability with Martingales and Durrett; Meyn and Tweedie, and Hall "
            "and Heyde; Levin, Peres and Wilmer on mixing times; and Andersen, Borgan, Gill and Keiding on counting "
            "processes; with the papers from Markov's Onegin to Bayer and Diaconis's shuffles."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=44, current=None)
        nxt = VGroup(label(r"Part 45", font_size=30, color=GREY_B), label(r"The Theory of Estimation", font_size=48),
                     label(r"what makes an estimator good, \ and when is one the best?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Forty-four parts of sixty-five. <bookmark mark='a'/> Randomness that unfolds in time has its own "
            "theorems: fair games, chains that forget, and the Brownian limit under finite-variance invariance "
            "conditions. <bookmark mark='b'/> Next, Part forty-five: the theory of estimation."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(44)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
