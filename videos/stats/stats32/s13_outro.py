from __future__ import annotations

from videos.stats.stats32.common import *  # noqa: F403

PROBLEMS = [
    r"Show that ridge's fitted values are $\sum_j u_j\, d_j^2/(d_j^2 + \lambda)\, u_j^\top y$ and that $\mathrm{df}(\lambda) = \sum_j d_j^2/(d_j^2 + \lambda)$.",
    r"Derive the soft-threshold solution of $\min_b \tfrac12(b - z)^2 + \lambda|b|$ from the subgradient condition.",
    r"Show that $\hat\beta = 0$ solves the lasso iff $\lambda \ge \|X^\top y\|_\infty / n$.",
    r"Prove: \ if $\|h_S\|_1 < \|h_{S^c}\|_1$ for every $0 \ne h \in \mathrm{null}(A)$, \ basis pursuit recovers every $x$ supported on $S$.",
    r"For $\theta \mid y$ with $y \sim N(\theta, 1)$ and a Laplace($\lambda$) prior, \ show $E(\theta \mid y) \ne 0$ for $y \ne 0$.",
    r"Show that the prox of $\lambda\|Z\|_*$ soft-thresholds the singular values of $Z$ \ (use von Neumann's trace inequality).",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.upgrade52()
        self.upgrade59()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"the phantom: \ exact from a fifth of k-space", SPIKE), (r"$p > n$: \ bet on sparsity", LASSO),
            (r"ridge: \ shrinks, \ never selects", RIDGE), (r"$\ell_1$: \ the convex envelope of $\ell_0$", LASSO),
            (r"the lasso: \ KKT, \ soft thresholds, \ corners", LASSO), (r"LARS: \ the exact path; \ HDL drops out", LASSO),
            (r"elastic net, \ group, \ fused, \ MCP", ENET), (r"CV predicts; \ stability selects", LASSO),
            (r"Laplace and horseshoe: continuous shrinkage, no exact-zero posterior mass", S.KEPT), (r"null space property, \ RIP, \ phase transitions", SPIKE),
            (r"naive CIs 75\%; \ debiased 95.6\%", RES), (r"matrix completion: \ $\ell_1$ of singular values", LASSO),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 32, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part thirty-two in twelve lines. <bookmark mark='a'/> The phantom came back exactly from a fifth of its "
            "Fourier coefficients. With more unknowns than equations we need structure; sparsity is one useful "
            "choice. Ridge stabilizes but never selects. On a unit coordinate box, the one norm is the convex "
            "envelope of counting. The lasso's optimality conditions pin active correlations at lambda, and its zeros"
            " come from corners. Least angle regression computes the exact path, on which HDL drops out and returns. "
            "The elastic net shares among correlated variables, the group lasso selects groups, the fused lasso finds"
            " jumps, and MCP removes the bias on large effects. Cross-validation predicts well; stability selection "
            "selects well. Both Laplace and horseshoe are continuous priors; the horseshoe provides stronger "
            "near-zero shrinkage, not exact posterior zeros. The null space property and the restricted isometry "
            "property explain compressed sensing, with its sharp phase transition. Naive intervals after the lasso "
            "cover seventy-five percent; debiased ones cover ninety-five. And matrix completion is the lasso of "
            "singular values."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def upgrade52(self):
        card = upgrade_card(32, r"the lasso recovers sparse signals; \ $n \gtrsim s \log(p/s)$ suffices",
                            r"stated, \ not proved: \ the error rates, \ the support recovery conditions",
                            r"Part 52: \ the oracle inequality $\|\hat\beta - \beta\|_2^2 \lesssim s\log p / n$, \ the primal--dual witness")
        with self.voiceover(
            "<bookmark mark='a'/> Two promises for later. This part claimed that the lasso recovers sparse signals from about "
            "s log p over s observations. <bookmark mark='b'/> It stated rates and conditions without proving them. "
            "<bookmark mark='c'/> Part 52 proves the lasso's oracle inequality, an error of order s log p over n under "
            "restricted eigenvalue conditions, and Martin Wainwright's primal–dual witness for exact support recovery."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card[0]), FadeIn(card[1][0]), FadeIn(card[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card[1][1][2]))
        self.clear_scene()

    def upgrade59(self):
        card = upgrade_card(32, r"a phase transition at $\rho(\delta)$, \ seen in simulation",
                            r"Donoho--Tanner's curve taken on trust; \ $s$ fixed or small",
                            r"Part 59: \ approximate message passing and its state evolution derive the curve, \ and exact lasso risk when $p/n$ is fixed")
        with self.voiceover(
            "<bookmark mark='a'/> And second: we saw a sharp phase transition in simulation <bookmark mark='b'/> and took "
            "Donoho and Tanner's curve on trust. <bookmark mark='c'/> Part 59's approximate message passing derives that curve "
            "from a one-line recursion, and gives the lasso's exact risk when p and n grow in proportion."
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
            (r"thousands of tests after screening", [33]), (r"conformal intervals around the lasso", [34]),
            (r"double machine learning", [36]), (r"sparse PCA's computational barrier", [50]),
            (r"Fano: \ $s\log(p/s)$ is optimal", [50]), (r"concentration for RIP", [51]),
            (r"oracle inequalities; \ low-rank recovery", [52]), (r"selective inference and PoSI", [56]),
        ], font_size=22)
        self.play(FadeIn(card.head))
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 33 handles the thousands of tests that screening creates. Part 34 "
            "wraps lasso predictions in conformal intervals with guarantees. Part 36's double machine learning extends double "
            "selection. Part 50 proves that s log p over s is the best possible rate, and why sparse principal components may "
            "be computationally hard. Part 51 proves the restricted isometry property for random matrices. Part 52 proves the "
            "oracle inequalities and returns to low-rank recovery. And Part 56 develops inference after selection in full."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> Ridge through the SVD; soft "
            "thresholding from the subgradient; where the lasso path begins; the null space property's sufficiency; "
            "why the independent normal-means Laplace posterior mean is nonzero for nonzero observations; and "
            "singular value thresholding as the nuclear norm's proximal map. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"T. Hastie, R. Tibshirani \& M. Wainwright, \emph{Statistical Learning with Sparsity} (2015)",
             r"P. B\"uhlmann \& S. van de Geer, \emph{Statistics for High-Dimensional Data} (2011)",
             r"S. Foucart \& H. Rauhut, \emph{A Mathematical Introduction to Compressive Sensing} (2013)",
             r"T. Hastie, R. Tibshirani \& J. Friedman, \emph{The Elements of Statistical Learning} (2009), \ ch. 3 and 18"],
            [r"A. Hoerl \& R. Kennard (1970); \ R. Tibshirani (1996); \ S. Chen, D. Donoho \& M. Saunders (1998)",
             r"B. Efron, T. Hastie, I. Johnstone \& R. Tibshirani (2004); \ J. Friedman, T. Hastie \& R. Tibshirani (2010)",
             r"E. Cand\`es, J. Romberg \& T. Tao (2006); \ D. Donoho (2006); \ D. Donoho \& J. Tanner (2009); \ E. Cand\`es \& B. Recht (2009)",
             r"H. Zou \& T. Hastie (2005); \ J. Fan \& R. Li (2001); \ C.-H. Zhang (2010); \ C. Carvalho, N. Polson \& J. Scott (2010); \ S. van de Geer et al. (2014); \ A. Belloni et al. (2014)"])
        with self.voiceover(
            "The books this part follows: Hastie, Tibshirani and Wainwright's Statistical Learning with Sparsity; Bühlmann "
            "and van de Geer; Foucart and Rauhut on compressive sensing; and The Elements of Statistical Learning; with the "
            "papers from Hoerl and Kennard to Belloni, Chernozhukov and Hansen."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=32, current=None)
        nxt = VGroup(label(r"Part 33", font_size=30, color=GREY_B), label(r"Thousands of Questions", font_size=48),
                     label(r"ask enough questions and chance will answer some: \ which answers are real?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Thirty-two parts of sixty-five. <bookmark mark='a'/> We can find a few real effects among thousands of "
            "candidates, and say honestly how sure we are. <bookmark mark='b'/> But selecting variables means asking "
            "thousands of questions at once, and when you ask enough questions, chance will answer some of them. Part 33: "
            "which answers are real? Thousands of questions."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(32)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
