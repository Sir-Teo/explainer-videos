from __future__ import annotations

from videos.stats.stats28.common import *  # noqa: F403

PROBLEMS = [
    r"For $\hat y = Sy$ with $S$ fixed and $\mathrm{Var}(y) = \sigma^2 I$, \ show that the optimism is $2\sigma^2 \mathrm{tr}(S)/n$.",
    r"For least squares with hat matrix $H$, \ show that $y_i - \hat y_{-i} = (y_i - \hat y_i)/(1 - h_{ii})$.",
    r"Derive BIC from Laplace's method: \ show $\log p(y \mid M) = \ell(\hat\theta) - \tfrac k2 \log n + O_p(1)$.",
    r"Show AIC's penalty for the normal mean with known $\sigma$: \ $E[\ell(\hat\mu)] - E[\ell_{\text{new}}(\hat\mu)] = 1$, \ exactly.",
    r"Show that for nested models differing by one parameter, \ AIC prefers the larger with probability $\to P(\chi^2_1 > 2) = 0.157$.",
    r"Show that the log score is strictly proper: \ $E_g[-\log f(Y)]$ is minimized over densities $f$ at $f = g$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"Freedman: \ noise becomes a model", RES), (r"optimism $= 2\sigma^2\,\mathrm{df}/n$", HIT),
            (r"Cp, \ AIC, \ TIC, \ AICc", AICC), (r"BIC: \ consistent, \ not efficient", BICC),
            (r"CV estimates the procedure's error", CVC), (r"PSIS-LOO, \ $\hat k$, \ WAIC", LOOC),
            (r"singular: \ $\lambda = \tfrac12$, \ not 1", LOOC), (r"MDL: \ the shortest code", PATH),
            (r"stacking beats BMA when all are wrong", HIT), (r"after selection: \ 75\% coverage", RES),
            (r"subsets vs lasso: \ the SNR decides", PATH), (r"PIT and proper scores", HIT),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 28, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part twenty-eight in twelve lines. <bookmark mark='a'/> Freedman's screening turned fifty columns of noise into a "
            "significant regression. Training error is optimistic by two sigma squared times the degrees of freedom over n, "
            "and degrees of freedom can be measured for any procedure. Mallows's Cp and Akaike's AIC add the optimism back; "
            "Takeuchi's TIC handles the wrong model and AICc small samples. BIC, from the Laplace approximation, finds the "
            "true model when it is a candidate, but predicts worse when none is. Cross-validation estimates the error of the "
            "procedure, not of the fit in hand. PSIS-LOO and WAIC bring prediction to Bayesian models, with k-hat as a "
            "warning light. Singular models like mixtures have Watanabe's lambda, one half here, in place of d over two. "
            "MDL chooses the model that compresses the data most, and rediscovers BIC. Stacking combines wrong models into a "
            "right one, where Bayesian model averaging picks one at random. Intervals after selection covered seventy-five "
            "percent, and splitting restored ninety-five. Best subsets beat the lasso only when the signal is strong. And "
            "forecasts should be calibrated, checked by the PIT, and compared by proper scores."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"GCV and degrees of freedom for smoothers", [29]), (r"the lasso's df; \ high-dimensional selection", [32]),
            (r"FDR and selected effects", [33]), (r"conformal prediction", [34]),
            (r"model choice in causal inference", [36]), (r"forecast evaluation", [38]),
            (r"oracle inequalities and minimax rates", [50]), (r"selective inference in depth", [56]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 29 chooses smoothing parameters by GCV and counts their degrees of "
            "freedom. Part 32 studies selection in high dimensions. Part 33 controls the false discovery rate and the coverage "
            "of selected effects. Part 34's conformal prediction gives predictive intervals that hold whatever model was "
            "chosen. Part 36 picks nuisance models for causal estimates by cross-fitting. Part 38 evaluates forecasts. Part 50 "
            "proves oracle inequalities for model selection. And Part 56 returns to inference after selection, in depth."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The optimism of a linear smoother; the "
            "leave-one-out shortcut; BIC from Laplace's method; AIC's penalty, exactly, for a normal mean; the probability that "
            "AIC overfits by one parameter, fifteen point seven percent, which explains chapter three's plateau; and why the "
            "log score is proper. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"K. Burnham \& D. Anderson, \emph{Model Selection and Multimodel Inference} (2nd ed., 2002)",
             r"T. Hastie, R. Tibshirani \& J. Friedman, \emph{The Elements of Statistical Learning} (2nd ed., 2009), \ ch.\ 3 and 7",
             r"G. Claeskens \& N. Hjort, \emph{Model Selection and Model Averaging} (2008)",
             r"S. Watanabe, \emph{Algebraic Geometry and Statistical Learning Theory} (2009); \ P. Gr\"unwald, \emph{The MDL Principle} (2007)"],
            [r"D. Freedman (1983); \ C. Mallows (1973); \ H. Akaike (1973); \ G. Schwarz (1978); \ B. Efron (1986, 2004)",
             r"M. Stone (1974); \ P. Craven \& G. Wahba (1979); \ Y. Yang (2005); \ S. Bates, T. Hastie \& R. Tibshirani (2024)",
             r"A. Vehtari, A. Gelman \& J. Gabry (2017); \ S. Watanabe (2010, 2013); \ J. Rissanen (1978, 1996); \ A. P. Dawid (1984)",
             r"J. Hoeting et al.\ (1999); \ Y. Yao et al.\ (2018); \ R. Berk et al.\ (2013); \ T. Hastie, R. \& R. Tibshirani (2020); \ T. Gneiting \& A. Raftery (2007)"])
        with self.voiceover(
            "The books this part follows: Burnham and Anderson on multimodel inference, chapters three and seven of The "
            "Elements of Statistical Learning, Claeskens and Hjort on model selection and averaging, Watanabe's algebraic "
            "geometry and Grünwald's MDL; with the papers from Mallows and Akaike to Bates, Hastie and Tibshirani."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=28, current=None)
        nxt = VGroup(label(r"Part 29", font_size=30, color=GREY_B), label(r"Smoothing", font_size=48),
                     label(r"histograms, \ kernels, \ splines, \ wavelets, \ and the curse of dimension", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Twenty-eight parts of sixty-five. <bookmark mark='a'/> We can now choose among models, and know what the choice "
            "costs. <bookmark mark='b'/> But every candidate today had a fixed number of parameters. What if the thing to "
            "estimate is a whole curve? The eruptions of Old Faithful have a distribution with two humps, or perhaps three, "
            "and no finite family is obliged to contain it. Part 29: smoothing."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(28)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
