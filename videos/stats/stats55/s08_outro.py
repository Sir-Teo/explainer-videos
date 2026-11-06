from __future__ import annotations

from videos.stats.stats55.common import *  # noqa: F403

PROBLEMS = [
    r"(43) \ Show that if $\sum_n P(|X_n - X| > \varepsilon) < \infty$ for every $\varepsilon > 0$, \ then $X_n \to X$ almost surely.",
    r"(44) \ For the walk stopped at $-a$ or $b$, \ show $E\,T = ab$ from the martingale $S_n^2 - n$, \ checking the hypotheses.",
    r"(46) \ For $X \sim$ Bin($n, p$), \ show that the one-sided UMP test of $p \le p_0$ is randomized at one point, \ and find it.",
    r"(48) \ Show that $\{1\{x \le t\}\}$ has VC dimension 1, \ and deduce Glivenko--Cantelli from the VC bound.",
    r"(50) \ Prove Le Cam's two-point bound: \ $\inf_{\hat\theta}\max_{j} E_j|\hat\theta - \theta_j| \ge \frac{|\theta_0 - \theta_1|}{4}(1 - \mathrm{TV}(P_0, P_1))$.",
    r"(53) \ For a Beta(1, 1) prior and $n$ Bernoulli($p_0$) draws, \ show the posterior contracts at rate $n^{-1/2}$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.results()
        self.core()
        self.upgrade()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"$M_n/\log n \to 1$: \ Borel--Cantelli twice", PROBC), (r"$E S_T = 1$: \ no uniform integrability", PROBC),
            (r"$(1 - 1/n)^T$, \ above Cram\'er--Rao", ESTC5), (r"$X$ admissible in 1D; \ gap $\times$ mass $\to 0$", ESTC5),
            (r"Snow: \ rate ratio 8.4, \ $P \approx 10^{-163}$", TESTC5), (r"local power: \ AREs 0.91 and 0.75", TESTC5),
            (r"half-lines: \ brackets, \ Donsker", EMPC), (r"the median: \ $(\frac12 - 1\{x \le m\})/f(m)$", EMPC),
            (r"Fano: \ $\sigma^2 s\log(d/s)/n$", HDC), (r"matrix Bernstein: \ a ball for $\Sigma$", HDC),
            (r"the lasso: \ $9s\lambda^2/\phi^2$", BAYC), (r"contraction: \ $n^{-\min(\alpha,\beta)/(1+2\alpha)}$", BAYC),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"The exam, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> The exam in twelve lines. The maximum of exponentials over log n tends to one, by "
            "Borel–Cantelli on each side. The walk stopped at one has mean one, because the stopped walk is not uniformly "
            "integrable. The UMVUE of a Poisson zero is one minus one over n to the total, strictly above the Cramér–Rao "
            "bound. X is admissible in one dimension, because the Bayes-risk gap times the prior mass vanishes. Snow's "
            "rate ratio is eight point four, with a P-value near ten to the minus one hundred and sixty-three. The t and "
            "sign tests have relative efficiencies of ninety-one and seventy-five percent in the logistic model. <bookmark "
            "mark='b'/> Half-line indicators have finite bracketing entropy and are Donsker. The median's influence "
            "function is a bounded step. Fano gives the sparse rate. Matrix Bernstein gives a confidence ball for a "
            "covariance. The lasso's prediction error is at most nine s lambda squared over phi squared. And a Gaussian "
            "prior contracts at a rate set by the smaller of its smoothness and the truth's."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.6), run_time=16.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.6), run_time=14.0)
        self.clear_scene()

    def results(self):
        pm = ProofMap([(r"tails, \ BC", 43), (r"martingales", 44), (r"sufficiency, \ Bayes", 45), (r"Neyman structure", 46),
                       (r"LAN", 47), (r"brackets", 48), (r"pathwise derivatives", 49), (r"Fano", 50),
                       (r"concentration", 51), (r"cones", 52), (r"posteriors", 53), (r"the learning bounds", 54)],
                      per_row=6, font_size=20, color=S.ACCENT, box_h=0.8).move_to([0, -0.1, 0])
        head = label(r"the twelve tools, \ one per part of the core", font_size=30, color=GREY_A).to_edge(UP, buff=0.6)
        with self.voiceover(
            "<bookmark mark='a'/> Put the twelve proofs side by side and the core of a statistics PhD appears as a chain of "
            "tools: tails and Borel–Cantelli, martingales, sufficiency and Bayes rules, Neyman structure, local asymptotic "
            "normality, brackets, <bookmark mark='b'/> pathwise derivatives, Fano's inequality, concentration, cones, "
            "posteriors, and the learning bounds of Part fifty-four, which several of the proofs borrowed: the union bound "
            "over Gaussian tails in the lasso problem is chapter one of that part. <bookmark mark='c'/> Every one of them "
            "has now been used, not just learned."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pm.boxes), FadeIn(pm.texts), FadeIn(pm.tags), FadeIn(pm.arrows))
            vo.wait_until("a")
            self.play(LaggedStart(*[pm.light(k) for k in range(6)], lag_ratio=0.4), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[pm.light(k) for k in range(6, 12)], lag_ratio=0.4), run_time=5.0)
            vo.wait_until("c")
            self.play(pm.done())
        self.wait(1.0)
        self.clear_scene()

    def core(self):
        rows = fit_rows(VGroup(
            label(r"Stage IV: \ the PhD core, \ Parts 43--55", font_size=28, color=GREY_A),
            label(r"measure, \ martingales and Markov chains, \ the theories of estimation and of testing, \ asymptotics", font_size=22),
            label(r"empirical processes, \ semiparametric efficiency, \ minimax theory, \ high-dimensional probability", font_size=22),
            label(r"high-dimensional statistics, \ Bayesian asymptotics, \ learning theory", font_size=22),
            label(r"and an exam: \ twelve problems, \ every one proved", font_size=26, color=S.ACCENT),
            label(r"Candidacy", font_size=48, color=S.ACCENT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> That completes the fourth stage, the PhD core. <bookmark mark='b'/> Measure-theoretic "
            "probability, martingales and Markov chains, the theories of estimation and of testing, and asymptotic "
            "statistics; <bookmark mark='c'/> empirical processes, semiparametric efficiency, minimax theory and "
            "high-dimensional probability; <bookmark mark='d'/> high-dimensional statistics, Bayesian asymptotics and "
            "learning theory. <bookmark mark='e'/> And an exam, twelve problems, every one proved. <bookmark mark='f'/> In "
            "most departments, this is the point at which a student becomes a candidate: the courses are over, and the "
            "research begins."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=UP * 0.15))
        self.wait(1.5)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(55, r"theorems for a model, \ a method, \ a sample, \ all fixed in advance",
                            r"the question was chosen before the data were seen",
                            r"Parts 56--65: \ the frontier, \ where the question, \ the model and the data interact")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the last stage. Every theorem in the exam was about a model, a method and a "
            "sample fixed in advance. <bookmark mark='b'/> It assumed the question was chosen before anyone looked at the "
            "data. <bookmark mark='c'/> Real research rarely works that way, and the final stage, the research frontier, "
            "begins exactly there: with inference about questions chosen by looking at the data."
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
            (r"inference after selection: \ the winner's curse", [56]), (r"distribution-free inference", [57]),
            (r"anytime-valid inference: \ optional stopping, \ safely", [58]), (r"proportional asymptotics", [59]),
            (r"the dissertation", [65]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part fifty-six asks for honest inference after selection. Part "
            "fifty-seven, for inference with no model at all. Part fifty-eight returns to problem two: optional stopping, "
            "made safe by test martingales and e-values. Part fifty-nine to the lasso and the posterior when p and n grow "
            "together. And Part sixty-five is the dissertation."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six more problems for the PhD problem bank, with full solutions in the README beside the exam's twelve. "
            "<bookmark mark='a'/> Almost-sure convergence from summable tails; Wald's second identity, with its hypotheses "
            "checked; the randomized one-sided binomial test; Glivenko–Cantelli from a VC bound; Le Cam's two-point lower "
            "bound; and the contraction of a Beta posterior. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"D. Hilbert, \emph{Mathematical Problems} (1900); \ D. Cox \& D. Hinkley, \emph{Problems and Solutions in Theoretical Statistics} (1978)",
             r"R. Durrett, \emph{Probability: Theory and Examples} (5th ed. 2019); \ E. Lehmann \& G. Casella (1998); \ E. Lehmann \& J. Romano (2005)",
             r"A. van der Vaart, \emph{Asymptotic Statistics} (1998); \ A. van der Vaart \& J. Wellner (2023); \ A. Tsybakov (2009)",
             r"R. Vershynin (2018); \ P. B\"uhlmann \& S. van de Geer (2011); \ S. Ghosal \& A. van der Vaart (2017); \ P. Rigollet \& J.-C. H\"utter (2023)"],
            [r"J. Snow, \emph{On the Mode of Communication of Cholera} (2nd ed. 1855); \ S. Newcomb (1891); \ S. Stigler (1977)",
             r"C. Blyth (1951); \ C. Stein (1956); \ L. Brown (1971); \ L. Le Cam (1960); \ M. Ossiander (1987); \ M. Donsker (1952)",
             r"J. Tropp (2012); \ S. van de Geer (2007); \ P. Bickel, \ Y. Ritov \& A. Tsybakov (2009); \ D. Donoho \& I. Johnstone (1994)",
             r"S. Ghosal, \ J. Ghosh \& A. van der Vaart (2000); \ B. Knapik, \ A. van der Vaart \& H. van Zanten (2011)"])
        with self.voiceover(
            "The books behind the exam: Hilbert's problems, and Cox and Hinkley's book of problems and solutions; Durrett on "
            "probability; Lehmann with Casella and with Romano on estimation and testing; van der Vaart, van der Vaart and "
            "Wellner, and Tsybakov on asymptotics, empirical processes and minimax theory; Vershynin, Bühlmann and van de "
            "Geer, Ghosal and van der Vaart, and Rigollet and Hütter for the high-dimensional problems; with the papers "
            "from Snow and Newcomb to Knapik, van der Vaart and van Zanten."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=55, current=None)
        nxt = VGroup(label(r"Part 56", font_size=30, color=GREY_B), label(r"Inference After Selection", font_size=48),
                     label(r"how do you give honest uncertainty about a question chosen by looking at the data?", font_size=26, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Fifty-five parts of sixty-five, and the third milestone. <bookmark mark='a'/> Candidacy. <bookmark mark='b'/> "
            "The research stage begins with a question every working scientist meets: published effects shrink when they "
            "are replicated, because the questions were chosen after looking at the data. How do you give honest "
            "uncertainty about a question chosen that way? Part fifty-six: inference after selection."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(55)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
