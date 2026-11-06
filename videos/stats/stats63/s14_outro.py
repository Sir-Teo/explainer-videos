from __future__ import annotations

from videos.stats.stats63.common import *  # noqa: F403

PROBLEMS = [
    r"Show that randomized response, truthful with probability $\pi = e^\varepsilon/(1 + e^\varepsilon)$, is $\varepsilon$-DP, and find the variance of $\hat p$.",
    r"Show that adding $\mathrm{Laplace}(\Delta/\varepsilon)$ noise to a statistic of sensitivity $\Delta$ is $\varepsilon$-DP.",
    r"Show that the Gaussian mechanism with noise $\sigma$ and sensitivity $\Delta$ has trade-off curve $G_{\Delta/\sigma}$, \ and that $G_{\mu_1} \otimes G_{\mu_2} = G_{\sqrt{\mu_1^2 + \mu_2^2}}$.",
    r"For the central-DP mean of $n$ bits, \ find the $n$ at which the privacy term is a tenth of the MSE, \ at $p = 0.3$, $\varepsilon = 0.1$.",
    r"Derive Chouldechova's identity $\mathrm{FPR} = \frac{p}{1 - p}\,\frac{1 - \mathrm{PPV}}{\mathrm{PPV}}\,(1 - \mathrm{FNR})$.",
    r"Show that equal PPV and FNR in two groups with different base rates force unequal FPRs, \ unless PPV $= 1$ or FNR $= 1$.",
]


class Outro(LectureMixin, VoiceoverScene):
    def construct(self):
        self.recap()
        self.upgrade()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"Weld's record; \ 99.6\% unique in NHANES", BADC), (r"DP: \ a promise about the process", PRIVC),
            (r"DP is a test: \ trade-off curves, \ GDP", PRIVC), (r"accountants: \ 1{,}047 vs 50", OKC),
            (r"cost: \ central $1/n^2$, \ local $n\varepsilon^2$", PRIVC), (r"noise-aware CIs: \ 95.2\% kept", OKC),
            (r"Census: \ $\rho = 2.63$, \ small-block bias", BADC), (r"DP-SGD and membership audits", PRIVC),
            (r"criteria: \ independence, \ separation, \ sufficiency", GRPA), (r"impossibility: \ both sides right", S.ACCENT),
            (r"multicalibration: \ women 0.070 to 0.030", OKC), (r"counterfactual fairness: \ a causal model", GRPB),
            (r"open problems", S.ACCENT),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.38),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.38)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 63, \ in thirteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "<bookmark mark='a'/> Part sixty-three in thirteen lines. A governor's medical record was found from three "
            "harmless facts, and almost everyone in the NHANES extract is unique by four. Differential privacy is a promise "
            "about the release process, not the data, and it is a statement about every attacker's hypothesis test. Modern "
            "accountants are twenty times tighter than adding epsilons. Central privacy costs a second-order term; local "
            "privacy shrinks the sample. Intervals that model the noise keep their coverage. The census paid for consistent "
            "tables with bias in small blocks. <bookmark mark='b'/> Private training is audited by attacks. The three "
            "fairness criteria conflict, and on COMPAS both sides were right. Multicalibration repairs subgroups a model "
            "missed. And deciding which dependence is unfair needs a causal model."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:7]], lag_ratio=0.5), run_time=14.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[7:]], lag_ratio=0.5), run_time=10.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(63, r"a model's data, \ its predictions, \ its evaluation", r"people made the data; \ benchmarks are exact",
                            r"Part 64: \ statistics in the age of AI")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. This part treated a model as a statistic of people's data. "
            "<bookmark mark='b'/> It assumed people made the data and the labels, and that a model's measured accuracy was "
            "exact. <bookmark mark='c'/> Part sixty-four asks what honest uncertainty looks like when machines make the "
            "predictions, generate the data and grade each other."
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
            (r"membership attacks and benchmark contamination", [64]), (r"labels from models, \ and fairness of judges", [64]),
            (r"the dissertation's ethics and data chapter", [65]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part sixty-four's test sets that leak into training data, the same "
            "membership question asked of benchmarks; its labels produced by models, whose errors may differ by group; and "
            "the dissertation's chapter on its data, and who they describe."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=5.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Randomized response's guarantee and "
            "variance; the Laplace mechanism's proof; the Gaussian trade-off curve and its composition; the sample size at "
            "which central privacy becomes cheap; Chouldechova's identity; and the impossibility it implies. Pause here if "
            "you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"C. Dwork \& A. Roth, \ \emph{The Algorithmic Foundations of Differential Privacy} (2014)",
             r"S. Barocas, \ M. Hardt \& A. Narayanan, \ \emph{Fairness and Machine Learning} (2023)",
             r"L. Sweeney, \ \emph{Int. J. Uncertainty, Fuzziness and Knowledge-Based Systems} (2002)"],
            [r"C. Dwork, \ F. McSherry, \ K. Nissim \& A. Smith (2006); \ P. Kairouz, \ S. Oh \& P. Viswanath (2015)",
             r"J. Dong, \ A. Roth \& W. Su, \ \emph{JRSS B} (2022); \ I. Mironov (2017); \ M. Bun \& T. Steinke (2016)",
             r"J. Duchi, \ M. Jordan \& M. Wainwright (2013); \ T. Cai, \ Y. Wang \& L. Zhang, \ \emph{Ann. Statist.} (2021)",
             r"J. Abowd et al., \ \emph{HDSR} (2022); \ M. Abadi et al. (2016); \ N. Carlini et al. (2022)",
             r"A. Chouldechova, \ \emph{Big Data} (2017); \ J. Kleinberg, \ S. Mullainathan \& M. Raghavan (2016)",
             r"U. H\'ebert-Johnson et al. (2018); \ M. Kusner, \ J. Loftus, \ C. Russell \& R. Silva (2017)"])
        with self.voiceover(
            "The books behind this part: Dwork and Roth's Algorithmic Foundations of Differential Privacy, and Barocas, "
            "Hardt and Narayanan's Fairness and Machine Learning; with the papers from Sweeney's re-identification to "
            "counterfactual fairness."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=63, current=None)
        nxt = VGroup(label(r"Part 64", font_size=30, color=GREY_B), label(r"Statistics in the Age of AI", font_size=48),
                     label(r"when machines predict, \ generate the data and grade each other, \ what is honest uncertainty?",
                           font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Sixty-three parts of sixty-five. <bookmark mark='a'/> Removing names did not protect a governor; a "
            "guarantee about the process, priced in noise, protects everyone, and the price can be measured. <bookmark "
            "mark='b'/> Next, Part sixty-four: statistics in the age of AI."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(63)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
