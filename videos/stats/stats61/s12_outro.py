from __future__ import annotations

from videos.stats.stats61.common import *  # noqa: F403

PROBLEMS = [
    r"Show that in one dimension $W_1(\mu, \nu) = \int |F(x) - G(x)|\,dx$.",
    r"Show that a vertex of the transport polytope $\Pi(a, b)$ has at most $n + m - 1$ nonzero entries.",
    r"Show that $W_2^2\big(N(m_1, \sigma_1^2), N(m_2, \sigma_2^2)\big) = (m_1 - m_2)^2 + (\sigma_1 - \sigma_2)^2$.",
    r"Derive Sinkhorn's updates as exact maximization of the entropic dual in $f$, \ then in $g$.",
    r"Show the 1D barycenter of a location-scale family has mean $\sum w_k m_k$ and sd $\sum w_k \sigma_k$.",
    r"For $\pi = N(0, \Sigma)$ and Langevin from $N(m_0, \Sigma)$, \ show $\mathrm{KL}_t \le e^{-2t/\lambda_{\max}(\Sigma)}\mathrm{KL}_0$.",
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
            (r"Monge's earthworks, \ Kantorovich's LP", TGT), (r"duality: \ plans and prices", PLANC),
            (r"the line: \ sort and pair", PLANC), (r"$W_p$: \ a geometry on laws", PLANC),
            (r"NHANES BMI: \ $W_1 = 1.25$, \ mostly spread", SRC), (r"geodesics: \ clouds in transit", FLOWC),
            (r"the curse: \ $n^{-1/d}$", NAIVEC2), (r"Sinkhorn: \ blur, \ and $n^{-1/2}$", ENTC),
            (r"maps: \ entropic beats empirical", ENTC), (r"barycenters: \ average positions", PLANC),
            (r"ranks: \ exactly distribution-free", TGT), (r"flows: \ Langevin, \ flow matching", FLOWC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 61, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Part sixty-one in twelve lines. Monge asked how to move earth at least cost, and "
            "Kantorovich made it a linear program. Its dual is a system of prices. On the line, the solution sorts and "
            "pairs. The Wasserstein distance is a geometry on distributions; in NHANES, men's and women's body-mass index "
            "differ by one and a quarter units, mostly in spread. Geodesics are clouds in transit. <bookmark mark='b'/> The "
            "plug-in is cursed, at n to the minus one over d. Sinkhorn's blur restores the parametric rate. Entropic maps "
            "beat empirical ones. Barycenters average positions, not heights. Transport ranks give exactly "
            "distribution-free tests. And sampling and generation are flows in the space of distributions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.5), run_time=12.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.5), run_time=12.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(61, r"transport moves one population's distribution onto another's",
                            r"no causal model of why they differ", r"Part 62: \ transportability and causal frontiers")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. Transport moves one population's distribution onto another's. "
            "<bookmark mark='b'/> It assumed nothing about why they differ. <bookmark mark='c'/> Part sixty-two asks when a "
            "causal effect learned in one population can be carried to another, and what can be identified when the "
            "textbook assumptions fail."
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
            (r"transporting effects across populations", [62]), (r"fair scores by barycenters", [63]),
            (r"generative models and their generalization", [64]), (r"the dissertation's comparisons of distributions", [65]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part sixty-two's transport of causal effects across populations. "
            "Part sixty-three's fair scores, by mapping groups onto their barycenter. Part sixty-four's generative models and "
            "the question of whether they generalize. And the dissertation's comparisons of distributions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> W one as the area between distribution "
            "functions; the sparsity of the transport polytope's vertices; W two between normal laws; Sinkhorn's updates as "
            "dual coordinate ascent; the barycenter of a location-scale family; and the decay of the divergence along the "
            "Langevin flow. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"C. Villani, \ \emph{Optimal Transport: Old and New} (2009)",
             r"G. Peyr\'e \& M. Cuturi, \ \emph{Computational Optimal Transport} (2019); \ V. Panaretos \& Y. Zemel, \ \emph{An Invitation to Statistics in Wasserstein Space} (2020)",
             r"S. Chewi, \ J. Niles-Weed \& P. Rigollet, \ \emph{Statistical Optimal Transport} (2025)"],
            [r"G. Monge (1781); \ L. Kantorovich (1942); \ Y. Brenier (1991); \ R. McCann (1997); \ R. Dudley (1969)",
             r"N. Fournier \& A. Guillin, \ \emph{PTRF} (2015); \ J. Weed \& F. Bach, \ \emph{Bernoulli} (2019); \ M. Cuturi, \ NeurIPS (2013)",
             r"J.-C. H\"utter \& P. Rigollet, \ \emph{Ann. Stat.} (2021); \ A.-A. Pooladian \& J. Niles-Weed (2021); \ M. Agueh \& G. Carlier (2011)",
             r"M. Hallin et al., \ \emph{Ann. Stat.} (2021); \ N. Deb \& B. Sen, \ \emph{JASA} (2023); \ R. Jordan, \ D. Kinderlehrer \& F. Otto (1998)"])
        with self.voiceover(
            "The books behind this part: Villani's Optimal Transport, Old and New; Peyré and Cuturi on computation; "
            "Panaretos and Zemel on statistics in Wasserstein space; and Chewi, Niles-Weed and Rigollet's Statistical "
            "Optimal Transport; with the papers from Monge to Deb and Sen."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=61, current=None)
        nxt = VGroup(label(r"Part 62", font_size=30, color=GREY_B), label(r"Frontiers of Causal Inference", font_size=48),
                     label(r"what can be identified, \ and estimated, \ when the textbook assumptions fail?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Sixty-one parts of sixty-five. <bookmark mark='a'/> Monge noticed in 1781 that optimal paths never cross; two "
            "centuries later the same fact straightened the flows that generate images. <bookmark mark='b'/> Next, Part "
            "sixty-two: frontiers of causal inference."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(61)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
