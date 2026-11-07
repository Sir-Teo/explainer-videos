from __future__ import annotations

from videos.stats.stats47.common import *  # noqa: F403

PROBLEMS = [
    r"Show that Hodges's estimator satisfies $n\,E_0 T_n^2 \to 0$, \ and $n\,E_{\theta}(T_n - \theta)^2 \to 1$ for fixed $\theta \ne 0$.",
    r"For $\psi(x, \theta) = \mathrm{sign}(x - \theta)$, \ compute the sandwich $V^{-1}BV^{-1}$ \ and recover the median's variance.",
    r"Find the influence function of $T(F) = F^{-1}(p)$, \ and check that $E\,\mathrm{IF}^2 = p(1-p)/f(\xi_p)^2$.",
    r"For Gini's kernel $|x - y|$ with $N(0, 1)$ data, \ show that $h_1(x)=2\phi(x)+x(2\Phi(x)-1)-2/\sqrt\pi$.",
    r"Use Le Cam's third lemma to find the local power of the sign test, \ and its Pitman ARE $2/\pi$ against $t$.",
    r"Show that $P^*(M^* = M) = 1 - (1 - 1/n)^n$ \ for the bootstrap of a sample maximum.",
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
            (r"Hodges: \ superefficiency and its bump", HODC), (r"$o_P$, \ $O_P$, \ Slutsky, \ the delta method", MLEC),
            (r"M-estimators: \ consistency, \ the sandwich", MLEC), (r"quantiles: \ Bahadur's representation", MLEC),
            (r"influence functions; \ Hadamard derivatives", S.PRIOR), (r"U-statistics; \ Hoeffding; \ degeneracy", S.PRIOR),
            (r"rank tests: \ Wilcoxon, \ 0.864, \ normal scores", S.PRIOR),
            (r"LAN: \ one Gaussian observation", GOODC), (r"contiguity; \ the third lemma; \ local power", GOODC),
            (r"Hájek: \ convolution and LAM", GOODC), (r"Pitman and Bahadur efficiency", ALTC),
            (r"the bootstrap: \ second-order accuracy", ALTC), (r"saddlepoints; \ Lugannani--Rice", ALTC), (r"non-regular: \ the maximum; \ $m$ out of $n$", HODC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 47, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-seven in fourteen lines. Hodges's superefficient estimator and its bump of "
            "risk. The stochastic orders, Slutsky and the delta method. M-estimators, their consistency and the sandwich. "
            "Bahadur's representation of quantiles. Influence functions and Hadamard derivatives. U-statistics, with "
            "Hoeffding's projection and degenerate kernels. Rank tests and their efficiencies. <bookmark mark='b'/> Local "
            "asymptotic normality. Contiguity and the third lemma. Hájek's convolution and local asymptotic minimax "
            "theorems. Pitman and Bahadur efficiency. The bootstrap's second-order accuracy. Saddlepoints. And non-regular "
            "models, with the m out of n bootstrap."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:7]], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[7:]], lag_ratio=0.3), run_time=5.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(47, r"the asymptotics of estimators and tests, \ one parameter at a time",
                            r"uniform laws and process limits, \ on trust",
                            r"Part 48: \ empirical processes: \ Glivenko--Cantelli and Donsker classes, \ VC dimension, \ chaining")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. This one built the asymptotics of estimators and tests. "
            "<bookmark mark='b'/> Twice it took on trust a uniform law of large numbers, for consistency, and a process limit, "
            "for the functional delta method and the bootstrap. <bookmark mark='c'/> Part forty-eight proves them: empirical "
            "processes, Glivenko–Cantelli and Donsker classes, Vapnik–Chervonenkis dimension and chaining."
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
            (r"uniform laws, \ Donsker classes, \ the bootstrap empirical process", [48]), (r"efficient influence functions, \ semiparametrics", [49]),
            (r"minimax lower bounds beyond the local scale", [50]), (r"Bernstein--von Mises: \ the Bayesian LAN", [53]),
            (r"high-dimensional asymptotics, \ where $p$ grows with $n$", [59]),
        ], font_size=22)
        self.add(card.head)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part forty-eight proves the uniform laws and the Donsker theorems this "
            "part used. Part forty-nine finds efficient influence functions in semiparametric models. Part fifty extends "
            "lower bounds beyond the local scale. Part fifty-three is the Bayesian version of LAN, the Bernstein–von Mises "
            "theorem. And Part fifty-nine asks what survives when the number of parameters grows with n."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Hodges's limits; the median as a "
            "Z-estimator; the influence function of a quantile; Gini's projection; the sign test's local power; and the "
            "bootstrap maximum's atom. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"A. van der Vaart, \emph{Asymptotic Statistics} (1998); \ L. Le Cam \& G. Yang, \emph{Asymptotics in Statistics} (2nd ed. 2000)",
             r"E. Lehmann, \emph{Elements of Large-Sample Theory} (1999); \ P. Hall, \emph{The Bootstrap and Edgeworth Expansion} (1992)",
             r"J. Hájek \& Z. Šidák, \emph{Theory of Rank Tests} (1967); \ R. Serfling, \emph{Approximation Theorems} (1980)"],
            [r"W. Hoeffding (1948); \ J. Hodges (1951); \ L. Le Cam (1953, 1960); \ H. Daniels (1954)",
             r"P. Huber (1964, 1967); \ R. Bahadur (1960, 1966); \ J. Hájek (1968, 1970, 1972); \ F. Hampel (1974)",
             r"R. Lugannani \& S. Rice (1980); \ P. Bickel \& D. Freedman (1981); \ D. Politis \& J. Romano (1994)",
             r"P. Bickel, \ F. Götze \& W. van Zwet (1997); \ H. Leeb \& B. Pötscher (2005)"])
        with self.voiceover(
            "The books this part follows: van der Vaart's Asymptotic Statistics, Le Cam and Yang, Lehmann's Elements of "
            "Large-Sample Theory, Hall on the bootstrap and Edgeworth expansions, Hájek and Šidák, and Serfling; with the "
            "papers from Hoeffding to Leeb and Pötscher."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=47, current=None)
        nxt = VGroup(label(r"Part 48", font_size=30, color=GREY_B), label(r"Empirical Processes", font_size=48),
                     label(r"when does an average converge uniformly over a whole class of functions?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Forty-seven parts of sixty-five. <bookmark mark='a'/> The local minimax bound takes sample size to "
            "infinity before allowing the radius of a shrinking neighborhood to grow, and every regular model there "
            "is a single normal observation. <bookmark mark='b'/> Next, Part forty-eight: empirical processes."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(47)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
