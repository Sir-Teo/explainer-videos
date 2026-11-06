from __future__ import annotations

from videos.stats.stats48.common import *  # noqa: F403

PROBLEMS = [
    r"Show that $E\,\|P_n - P\|_{\mathcal F} \le 2\,\mathcal R_n(\mathcal F)$ \ by introducing a ghost sample and random signs.",
    r"Show that intervals on the line pick out exactly $n(n+1)/2 + 1$ subsets of $n$ distinct points, \ so their VC dimension is 2.",
    r"Build $\lceil 1/\varepsilon^2 \rceil$ brackets for the half-lines in $L_2(P)$, \ and deduce the Glivenko--Cantelli theorem.",
    r"For Brownian motion with $d(s,t) = \sqrt{|s-t|}$, \ show $N(\varepsilon) \le 1/\varepsilon^2 + 1$ \ and evaluate Dudley's integral.",
    r"For $\theta = E|X - c|$ with $c$ the sample mean, \ find the influence function and the variance for Exp(1) data.",
    r"Show that the law of $D_n$ with $\hat\mu$, $\hat\sigma$ plugged in does not depend on $(\mu, \sigma)$ \ for normal data.",
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
            (r"Doob's heuristic; \ Donsker's theorem", EMPC), (r"Glivenko--Cantelli; \ symmetrization; \ Rademacher", EMPC),
            (r"VC dimension; \ Sauer--Shelah", CLASSC), (r"covering and bracketing; \ entropy", CLASSC),
            (r"chaining: \ Dudley's refining nets", CLASSC), (r"Donsker classes: \ entropy integrals", GOODC),
            (r"Talagrand, \ Bousquet, \ DKW", BOUNDC),
            (r"the functional delta method: \ quantiles, \ KM", GOODC), (r"nuisance parameters: \ the footprint", S.ALT),
            (r"rates: \ $n^{1/3}$, \ Chernoff's distribution", S.ALT), (r"learning: \ ERM and VC bounds", S.ALT),
            (r"bootstraps: \ Giné--Zinn; \ multipliers", BADC), (r"KS with estimated parameters: \ Durbin", BADC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 48, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-eight in thirteen lines. Doob's heuristic and Donsker's theorem. "
            "Glivenko–Cantelli classes, proved by symmetrization and Rademacher averages. The VC dimension and the "
            "Sauer–Shelah lemma. Covering and bracketing numbers. Dudley's chaining. Donsker classes and their entropy "
            "integrals. Talagrand's concentration inequality, in Bousquet's form, and the DKW inequality. <bookmark mark='b'/> "
            "The functional delta method, for quantiles and Kaplan–Meier. Nuisance parameters and their footprint. Rates of "
            "convergence, the cube root and Chernoff's distribution. Empirical risk minimization. The bootstrap and "
            "multiplier empirical processes. And the Kolmogorov–Smirnov test with estimated parameters, done right."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:7]], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[7:]], lag_ratio=0.3), run_time=5.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(48, r"uniform laws and process limits, \ for parametric models",
                            r"a finite-dimensional parameter of interest, \ and nuisances that are finite or harmless",
                            r"Part 49: \ semiparametric efficiency: \ tangent spaces, \ efficient influence functions, \ DML")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. This one built uniform laws and process limits. <bookmark "
            "mark='b'/> Chapter eight showed that a plugged-in nuisance can cost something, and that sometimes it costs "
            "nothing, but only for simple nuisances. <bookmark mark='c'/> Part forty-nine takes the nuisance to be an entire "
            "unknown distribution, and asks how well a single number can then be estimated: tangent spaces, efficient "
            "influence functions, and the theory behind double machine learning."
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
            (r"Donsker conditions for one-step estimators and TMLE", [49]), (r"entropy and minimax rates; \ Fano and Le Cam", [50]),
            (r"concentration, \ chaining and suprema in high dimensions", [51]), (r"VC, \ Rademacher and margin bounds", [54]),
            (r"multiplier bootstraps for simultaneous inference", [56]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part forty-nine needs Donsker conditions for its one-step and targeted "
            "estimators. Part fifty turns entropy into minimax rates, with the lower bounds of Fano and Le Cam. Part "
            "fifty-one develops concentration and chaining in high dimensions. Part fifty-four is statistical learning "
            "theory, built on VC dimension, Rademacher complexity and margins. And Part fifty-six uses the multiplier "
            "bootstrap for inference after selection."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Symmetrization; the intervals' growth "
            "function; brackets for half-lines; Dudley's integral for Brownian motion; the mean absolute deviation's "
            "footprint; and why the estimated-parameter KS law is free of the parameters. Pause here if you want to try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"A. van der Vaart \& J. Wellner, \emph{Weak Convergence and Empirical Processes} (1996; 2nd ed. 2023)",
             r"M. Kosorok, \emph{Introduction to Empirical Processes and Semiparametric Inference} (2008); \ D. Pollard, \emph{Convergence of Stochastic Processes} (1984)",
             r"E. Giné \& R. Nickl, \emph{Mathematical Foundations of Infinite-Dimensional Statistical Models} (2016); \ R. Dudley, \emph{Uniform Central Limit Theorems} (1999)"],
            [r"A. Kolmogorov (1933); \ J. Doob (1949); \ M. Donsker (1952); \ A. Dvoretzky, \ J. Kiefer \& J. Wolfowitz (1956)",
             r"R. Dudley (1967, 1978); \ V. Vapnik \& A. Chervonenkis (1971); \ N. Sauer (1972); \ J. Durbin (1973)",
             r"D. Pollard (1982); \ M. Ossiander (1987); \ P. Massart (1990); \ E. Giné \& J. Zinn (1990); \ J. Kim \& D. Pollard (1990)",
             r"M. Talagrand (1996); \ P. Groeneboom \& J. Wellner (2001); \ O. Bousquet (2002); \ V. Chernozhukov, \ D. Chetverikov \& K. Kato (2013)"])
        with self.voiceover(
            "The books this part follows: van der Vaart and Wellner's Weak Convergence and Empirical Processes, Kosorok, "
            "Pollard, Giné and Nickl, and Dudley's Uniform Central Limit Theorems; with the papers from Kolmogorov and Doob "
            "to Chernozhukov, Chetverikov and Kato."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=48, current=None)
        nxt = VGroup(label(r"Part 49", font_size=30, color=GREY_B), label(r"Semiparametric Efficiency", font_size=48),
                     label(r"how well can you estimate a number when the rest of the model is infinite dimensional?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Forty-eight parts of sixty-five. <bookmark mark='a'/> A class is small enough for uniform laws when it cannot fit "
            "noise, and its entropy says how small. <bookmark mark='b'/> Next, Part forty-nine: semiparametric efficiency."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(48)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
