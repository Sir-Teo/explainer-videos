from __future__ import annotations

from videos.stats.stats49.common import *  # noqa: F403

PROBLEMS = [
    r"Show that the tangent space of 'X$_1$ independent of X$_2$' is $\{a(x_1) + b(x_2)\}$, \ and project $\mathbf 1\{x = (1,1)\} - p_{11}$ onto it.",
    r"Derive the influence function of $\psi = E\,Y$ along $p(1 + ts)$, \ and of $F^{-1}(p)$.",
    r"Derive the ATE's efficient influence function, \ and show its variance is $\mathrm{Var}\,\tau(X) + E[\sigma_1^2/e + \sigma_0^2/(1 - e)]$.",
    r"Show that the one-step ATE's bias is $E[(e - \hat e)(\mu_1 - \hat\mu_1)/\hat e] - E[(\hat e - e)(\mu_0 - \hat\mu_0)/(1 - \hat e)]$.",
    r"For symmetric location, \ show that $-f'/f$ is orthogonal to every even function in $L_2(f)$.",
    r"Show that the TMLE update with $H = T/e - (1-T)/(1-e)$ solves $P_n \phi^* = 0$.",
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
            (r"adaptation: \ Stein, \ Stone, \ Bickel", EFFC), (r"tangent spaces: \ the directions of a model", TANC),
            (r"gradients; \ $\phi^*$ as a projection", GRADC), (r"bounds: \ the least favourable submodel", EFFC),
            (r"worked: \ mean, \ ATE, \ PLR, \ Cox", GRADC), (r"the efficient score; \ adaptation explained", NUIC),
            (r"one-step, \ estimating equations, \ TMLE", OSC), (r"double robustness: \ a product", TANC),
            (r"DML: \ orthogonality, \ cross-fitting, \ $a + b \ge \tfrac12$", OSC), (r"missing data: \ RRZ's augmentation", GRADC),
            (r"higher order: \ $\int f^2$ and U-statistics", EFFC), (r"the World test", NUIC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 49, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-nine in twelve lines. Adaptive estimation, from Stein to Bickel. Tangent spaces. "
            "Gradients, and the efficient influence function as a projection. The bound, as the hardest one-dimensional "
            "submodel. Worked influence functions for the mean, the treatment effect, the partially linear model and Cox. "
            "The efficient score, which explains adaptation. <bookmark mark='b'/> One-step, estimating-equation and targeted "
            "estimators. Double robustness, as a product. The theory of double machine learning. Missing data, by "
            "augmentation. Higher-order influence functions. And the World test."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.3), run_time=5.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(49, r"the best possible root-$n$ estimation of a smooth functional",
                            r"that root-$n$ is the right scale, \ and regular estimators",
                            r"Part 50: \ minimax theory: \ Le Cam, \ Assouad, \ Fano, \ Pinsker, \ rates for any method")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. This one found the best possible root-n estimation of a "
            "smooth functional. <bookmark mark='b'/> It assumed that root n was the right scale, and compared only regular "
            "estimators. <bookmark mark='c'/> Part fifty drops both assumptions: minimax theory, with the lower bounds of Le "
            "Cam, Assouad and Fano, and Pinsker's theorem, for how well anyone can estimate anything, at any rate."
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
            (r"minimax rates when root-$n$ is impossible", [50]), (r"Bernstein--von Mises for semiparametric models", [53]),
            (r"debiased inference in high dimensions", [52]), (r"double robustness under shift", [60]),
            (r"proximal inference, \ policy learning, \ efficient frontiers", [62]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part fifty finds minimax rates when root n is impossible. Part "
            "fifty-three asks when Bayesian posteriors for semiparametric models are efficient. Part fifty-two uses the same "
            "debiasing for high-dimensional regression. Part sixty extends double robustness to distribution shift. And "
            "Part sixty-two, on the frontiers of causal inference, builds proximal and policy-learning estimators from "
            "efficient influence functions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The independence projection; two influence "
            "functions; the ATE's efficient influence function and its variance; the one-step's bias as a product; the "
            "orthogonality behind adaptation; and why TMLE solves the efficient equation. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"P. Bickel, \ C. Klaassen, \ Y. Ritov \& J. Wellner, \emph{Efficient and Adaptive Estimation for Semiparametric Models} (1993)",
             r"A. Tsiatis, \emph{Semiparametric Theory and Missing Data} (2006); \ A. van der Vaart, \emph{Asymptotic Statistics}, ch.\ 25 (1998)",
             r"M. van der Laan \& S. Rose, \emph{Targeted Learning} (2011); \ E. Kennedy, \emph{Semiparametric doubly robust targeted double machine learning: a review} (2022)"],
            [r"C. Stein (1956); \ C. Stone (1975); \ P. Bickel (1982); \ J. Pfanzagl (1982); \ A. Schick (1986)",
             r"P. Robinson (1988); \ J. Robins, \ A. Rotnitzky \& L. P. Zhao (1994); \ J. Hahn (1998)",
             r"M. van der Laan \& D. Rubin (2006); \ J. Robins, \ L. Li, \ E. Tchetgen Tchetgen \& A. van der Vaart (2008)",
             r"V. Chernozhukov, \ D. Chetverikov, \ M. Demirer, \ E. Duflo, \ C. Hansen, \ W. Newey \& J. Robins (2018)"])
        with self.voiceover(
            "The books this part follows: Bickel, Klaassen, Ritov and Wellner; Tsiatis on semiparametric theory and missing "
            "data; chapter twenty-five of van der Vaart; van der Laan and Rose on targeted learning; and Kennedy's review; "
            "with the papers from Stein to Chernozhukov and colleagues."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=49, current=None)
        nxt = VGroup(label(r"Part 50", font_size=30, color=GREY_B), label(r"Minimax Theory", font_size=48),
                     label(r"how well can anyone estimate, \ with any method?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Forty-nine parts of sixty-five. <bookmark mark='a'/> To estimate one number well inside an infinite model, find "
            "its efficient influence function, and remove the plug-in's first-order bias; then estimate the nuisances as well "
            "as you can, on separate folds, and let the product of their errors take care of itself. <bookmark mark='b'/> Next, Part "
            "fifty: minimax theory."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(49)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
