from __future__ import annotations

from videos.stats.stats64.common import *  # noqa: F403

PROBLEMS = [
    r"Show that with singleton clusters the CR1 standard error equals the iid standard error $s/\sqrt{n}$.",
    r"For two 0/1 score vectors, \ show $\mathrm{Var}(\bar a - \bar b) = (\sigma_a^2 + \sigma_b^2 - 2\sigma_{ab})/n$ and that McNemar's statistic depends only on $n_{10}, n_{01}$.",
    r"Show that the Bradley--Terry log-likelihood is concave in $\theta$, \ and that only differences $\theta_i - \theta_j$ are identified.",
    r"Show that $E[\hat\sigma_t^2] = ((n - 1)/n)^t$ for the Gaussian refitted to its own samples, \ and that $\hat\sigma_t^2 \to 0$ a.s.",
    r"Show that the prediction-powered mean $\bar f_N + \overline{(y - f)}_n$ is unbiased for any judge $f$, \ and find its variance.",
    r"Derive Tweedie's formula $E[x \mid y] = y + \sigma^2 \nabla \log p_\sigma(y)$ for $y = x + \sigma Z$.",
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
            (r"85.2 vs 84.7: \ the order flips a third of the time", MODB), (r"clusters: \ iid 76\% vs clustered 95\%", HONC),
            (r"pairs: \ unpaired 99\%, \ paired 95\%", HONC), (r"arenas: \ Bradley--Terry, \ style control", MODA),
            (r"IRT: \ 100 anchors, \ a third less error", HONC), (r"holdouts: \ reuse 64\%, \ Thresholdout near 50\%", NAIVEC),
            (r"judges: \ PPI covers 95\%", HONC), (r"collapse: \ the variance random walk", NAIVEC),
            (r"conformal factuality", HONC), (r"watermarks: \ a binomial test", MODB),
            (r"simulators: \ check coverage", JUDGEC), (r"diffusion: \ the empirical score memorizes", JUDGEC),
            (r"markets: \ A/B 4$\times$ too large", NAIVEC), (r"open problems", S.ACCENT),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.36),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.36)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 64, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "<bookmark mark='a'/> Part sixty-four in fourteen lines. A half-point lead reversed a third of the time on a "
            "fresh benchmark. Clustered questions need clustered error bars. Models on the same questions need paired "
            "comparisons, and crowded leaderboards inflate the winner. Arenas are Bradley-Terry regressions, with style as a "
            "confounder. Item response theory makes small benchmarks informative. A reused holdout reported sixty-four "
            "percent for a coin flip. <bookmark mark='b'/> A few human labels rectify a biased judge. A model fitted to its "
            "own output collapses. Conformal filtering guarantees factual answers at a price. Watermarks are binomial tests. "
            "Simulators' posteriors need their coverage checked. The exact empirical score memorizes. And marketplaces need "
            "randomized markets, not randomized buyers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:7]], lag_ratio=0.5), run_time=14.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[7:]], lag_ratio=0.5), run_time=12.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(64, r"methods applied to someone else's question", r"the question, \ the data and the answer were given",
                            r"Part 65: \ the dissertation")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the last part. Every part so far applied methods to questions and data "
            "that someone else had posed and collected. <bookmark mark='b'/> It assumed the question, the data and even the "
            "answer's form were given. <bookmark mark='c'/> Part sixty-five asks how new statistical knowledge is made: a "
            "question chosen, a conjecture, a proof, a preregistered simulation, a real application, and an honest report."
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
            (r"a preregistered simulation study, \ reported whatever it shows", [65]),
            (r"the full Coverage Board, \ every promise of the degree", [65]),
            (r"the dissertation's open problem", [65]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> In Part sixty-five: a simulation study designed in advance and "
            "reported whatever it shows; the full Coverage Board, every promise of the degree tested; and an open problem "
            "from these last parts, attacked as a dissertation."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=5.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The cluster-robust standard error with "
            "singleton clusters; the paired variance and McNemar's statistic; the concavity of the Bradley-Terry likelihood; "
            "the Gaussian's collapse; the unbiasedness of prediction-powered inference; and Tweedie's formula. Pause here if "
            "you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. Barocas, \ M. Hardt \& A. Narayanan, \ \emph{Fairness and Machine Learning} (2023)",
             r"F. Lord, \ \emph{Applications of Item Response Theory to Practical Testing Problems} (1980)",
             r"C. Dwork \& A. Roth, \ \emph{The Algorithmic Foundations of Differential Privacy} (2014)"],
            [r"E. Miller, \ arXiv:2411.00640 (2024); \ W.-L. Chiang et al., \ ICML (2024); \ F. Maia Polo et al., \ ICML (2024)",
             r"C. Dwork et al., \ \emph{Science} (2015); \ A. Blum \& M. Hardt, \ ICML (2015)",
             r"A. Angelopoulos et al., \ \emph{Science} (2023); \ N. Egami et al., \ NeurIPS (2023)",
             r"I. Shumailov et al., \ \emph{Nature} (2024); \ M. Gerstgrasser et al. (2024)",
             r"C. Mohri \& T. Hashimoto, \ ICML (2024); \ J. Kirchenbauer et al., \ ICML (2023); \ S. Dathathri et al., \ \emph{Nature} (2024)",
             r"J. Hermans et al., \ TMLR (2022); \ K. Oko, \ S. Akiyama \& T. Suzuki, \ ICML (2023)"])
        with self.voiceover(
            "The books behind this part: Barocas, Hardt and Narayanan; Frederic Lord's item response theory; and Dwork and "
            "Roth; with the papers from Miller's error bars to the minimax rates of diffusion models."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=64, current=None)
        nxt = VGroup(label(r"Part 65", font_size=30, color=GREY_B), label(r"The Dissertation", font_size=48),
                     label(r"how is new statistical knowledge made, \ and what has the whole degree shown?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Sixty-four parts of sixty-five. <bookmark mark='a'/> A half-point lead on a leaderboard is a statistical claim, "
            "and every lesson of the degree applies to it. <bookmark mark='b'/> Next, the last part: the dissertation."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(64)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
