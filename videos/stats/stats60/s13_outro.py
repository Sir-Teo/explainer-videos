from __future__ import annotations

from videos.stats.stats60.common import *  # noqa: F403

PROBLEMS = [
    r"Contaminate $N(0, 1)$ with $\varepsilon$ of mass at $+\infty$: \ show the median moves to $\Phi^{-1}\big(\tfrac{1}{2(1 - \varepsilon)}\big) \approx 1.25\,\varepsilon$.",
    r"Show $E_P[w(X) f(X, Y)] = E_Q[f(X, Y)]$ under covariate shift, \ and that $n_{\mathrm{eff}} = (\sum w)^2/\sum w^2$ equals the conditional information count for independent homoskedastic outcomes with a constant mean.",
    r"Derive $E[\hat q_{\mathrm{CC}}] = q\,\mathrm{TPR} + (1 - q)\,\mathrm{FPR}$, \ and show BBSE with two classes is Forman's adjusted count.",
    r"Show the $\chi^2$-ball worst case is $\bar\ell + \sqrt{2\rho\,\widehat{\mathrm{Var}}(\ell)}$ when no weight hits zero.",
    r"Show anchor regression with $\gamma = 1$ is OLS, \ and tends to unique 2SLS as $\gamma \to \infty$ when the projected design has full column rank.",
    r"Show that a classifier's odds $c/(1 - c)$, \ times $n_0/n_1$, \ equal the density ratio $q(x)/p(x)$.",
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
            (r"ImageNet rebuilt: \ 11--14 points lost", NAIVEC), (r"Tukey depth: \ robust, \ hard to compute", DEPTHC),
            (r"the filter: \ robust and efficient", FIXC), (r"list decoding: \ a majority of outliers", DEPTHC),
            (r"median of means: \ two moments suffice", FIXC), (r"covariate shift: \ weights, \ and their price", TGTC),
            (r"label shift: \ BBSE and EM", TGTC), (r"DRO: \ a certificate for a ball", FIXC),
            (r"invariance: \ ICP and anchors", FIXC), (r"transfer: \ borrow, \ then correct", SRCC),
            (r"detection: \ MMD and classifiers", SRCC), (r"open problems", S.ACCENT),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 60, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Part sixty in twelve lines. The MatchedFrequency rebuilt ImageNet set cost the evaluated models eleven to fourteen percentage points. Tukey's depth is robust in any dimension but hard to compute; certified spectral filters are robust and efficient; our trimming is an illustration. List decoding handles a majority of outliers, and median of means needs only two moments. Covariate shift is corrected by importance weights, at a price in effective sample size. <bookmark mark='b'/> Label shift is corrected through the confusion matrix, or by EM. Distributionally robust optimization certifies the risk over a ball of distributions. Invariance turns causal structure into robustness. Transfer learning borrows from a source and corrects the difference. Kernel and classifier tests detect a shift. And five problems remain open."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.5), run_time=12.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.5), run_time=12.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(60, r"distances between distributions: \ divergences, \ MMD, \ Wasserstein balls",
                            r"used as tools, \ never studied", r"Part 61: \ optimal transport")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. This part measured shifts with divergences, the maximum mean "
            "discrepancy, and Wasserstein balls. <bookmark mark='b'/> It used them as tools without studying them. "
            "<bookmark mark='c'/> Part sixty-one studies the Wasserstein distance itself: optimal transport, its "
            "computation, and its statistics."
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
            (r"Wasserstein distances, \ studied", [61]), (r"transporting causal effects across populations", [62]),
            (r"robustness and privacy, \ two sides of one coin", [63]), (r"the accuracy line of large models", [64]),
            (r"the dissertation's robustness checks", [65]),
        ], font_size=22)
        self.play(FadeIn(card.head))
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part sixty-one's study of Wasserstein distances. Part sixty-two's "
            "transport of causal effects to new populations. Part sixty-three, where robustness and differential privacy "
            "turn out to be two sides of one coin. Part sixty-four's large models and their accuracy line. And the "
            "dissertation's robustness checks."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The contaminated median's shift; the "
            "importance-weighting identity and Kish's effective sample size; classify and count's bias and the adjusted "
            "count; the chi-square ball's worst case; anchor regression's two limits; and the classifier's odds as a "
            "density ratio. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"I. Diakonikolas \& D. Kane, \ \emph{Algorithmic High-Dimensional Robust Statistics} (2023)",
             r"J. Qui\~nonero-Candela, \ M. Sugiyama, \ A. Schwaighofer \& N. Lawrence (eds.), \ \emph{Dataset Shift in Machine Learning} (2009)",
             r"J. Peters, \ D. Janzing \& B. Sch\"olkopf, \ \emph{Elements of Causal Inference} (2017)"],
            [r"J. Tukey (1975); \ M. Chen, \ C. Gao \& Z. Ren, \ \emph{Ann. Stat.} (2018); \ G. Lugosi \& S. Mendelson, \ \emph{Ann. Stat.} (2019)",
             r"I. Diakonikolas et al., \ FOCS (2016); \ K. Lai, \ A. Rao \& S. Vempala, \ FOCS (2016); \ M. Charikar, \ J. Steinhardt \& G. Valiant, \ STOC (2017)",
             r"H. Shimodaira (2000); \ Z. Lipton, \ Y.-X. Wang \& A. Smola, \ ICML (2018); \ J. Duchi \& H. Namkoong, \ \emph{Ann. Stat.} (2021)",
             r"J. Peters, \ P. B\"uhlmann \& N. Meinshausen, \ \emph{JRSS B} (2016); \ D. Rothenh\"ausler et al., \ \emph{JRSS B} (2021); \ S. Li, \ T. Cai \& H. Li, \ \emph{JRSS B} (2022)"])
        with self.voiceover(
            "The books behind this part: Diakonikolas and Kane on algorithmic robust statistics; Quiñonero-Candela, "
            "Sugiyama, Schwaighofer and Lawrence on dataset shift; and Peters, Janzing and Schölkopf on causal inference; "
            "with the papers from Tukey to Trans-Lasso."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=60, current=None)
        nxt = VGroup(label(r"Part 61", font_size=30, color=GREY_B), label(r"Optimal Transport in Statistics", font_size=48),
                     label(r"how far apart are two distributions, \ and what is the cheapest way to move one into the other?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Sixty parts of sixty-five. <bookmark mark='a'/> The models on the rebuilt ImageNet kept their ranking but lost substantial accuracy on the rebuilt collection: a guarantee is only as good as its assumption about where the data come from. <bookmark mark='b'/> Next, Part sixty-one: optimal transport."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(60)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
