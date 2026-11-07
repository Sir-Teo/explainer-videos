from __future__ import annotations

from videos.stats.stats19.common import *  # noqa: F403

PROBLEMS = [
    r"OLS with $p$ terms, \ fixed $x$'s: \ show $E[\text{train}] = \sigma^2(1 - p/n)$ and $E[\text{test at the same } x\text{'s}] = \sigma^2(1 + p/n)$.",
    r"$f(x) = x^2$, \ neighbours at $x_0 + jh$, \ $j = -m, \dots, m$: \ the bias and variance of $k$-NN, \ $k = 2m + 1$.",
    r"In $p = 10$ dimensions, \ the edge of a cube holding 1\% of uniform data; \ and in $p = 100$.",
    r"\emph{upon}: \ 3.3 per 1,000 for Hamilton, \ 0.18 for Madison. \ A 2,000-word paper with none: \ the Poisson $\log_{10}$ odds.",
    r"Standardized orthogonal design $X^\top X=nI$: \ show ridge gives $\hat\beta / (1 + \lambda)$ and the lasso the soft threshold of $\hat\beta$ at $\lambda$.",
    r"A test with sensitivity 90\%, \ specificity 95\%, \ base rate 1\%: \ its precision, \ and its accuracy.",
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
            (r"\emph{upon}: \ the dull words decide", HAM), (r"training error is optimistic; \ $C_p$", TRAIN),
            (r"test error $=$ noise $+$ bias$^2$ $+$ variance", OBS), (r"$\mathrm{df} = \mathrm{tr}\,S$", GREY_A),
            (r"cross-validation; \ the one-SE rule", CVC), (r"CV $\pm$ 2 SE: \ 90.15\%, \ broken", RES),
            (r"$k$-NN; \ the curse of dimensionality", BLUE), (r"naive Bayes vs logistic", MAD),
            (r"trees: \ grow, \ then prune", HIT), (r"ridge and the lasso: \ the diamond", OBS),
            (r"recall, \ precision, \ ROC, \ calibration", TEST), (r"the \emph{Federalist}: \ Madison, \ 12 of 12", MAD),
            (r"No. 55: \ the fragile case", RES), (r"leakage: \ 11\% from pure noise", RED),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 19, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part nineteen in fourteen lines. <bookmark mark='a'/> Mosteller and Wallace told Hamilton from Madison "
            "by the rates of dull words like upon. Prediction has its own measure of success, the test error, and "
            "familiar fitted rules have optimistic training error on average. The Cp-style penalty estimates "
            "same-input prediction error under its stated assumptions. Test error splits into noise, squared bias and"
            " variance, and the effective degrees of freedom of a smoother is the trace of its matrix. "
            "Cross-validation estimates the prediction curve from one data set, with the one-standard-error rule for "
            "a simpler choice, though the Board found ninety point one five percent coverage for its nominal "
            "ninety-five percent interval. Nearest neighbours need no model but suffer the curse of dimensionality. "
            "Naive Bayes and logistic regression model the same odds from opposite ends; trees grow and are pruned; "
            "ridge and the lasso shrink, and the lasso's diamond sets coefficients to zero. Accuracy is one number "
            "among recall, precision, the ROC curve and calibration. Naive Bayes favoured Madison on all twelve "
            "disputed papers; ridge logistic agreed on eleven and favoured Hamilton on the fragile fifty-fifth. And "
            "selection outside the loop found eleven percent error in pure noise."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=34.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the BSc capstone: \ an analysis from question to report", [20]),
            (r"model selection: \ AIC, \ BIC, \ and CV compared", [28]), (r"smoothing: \ kernels, \ splines, \ df", [29]),
            (r"sparsity: \ the lasso in depth", [32]), (r"conformal prediction: \ intervals with guarantees", [34]),
            (r"high-dimensional statistics", [51, 52]), (r"learning theory: \ why the test error can be bounded", [54]),
            (r"inference after selection", [56]),
        ], font_size=22)
        intro = label('Where prediction and honest evaluation return', font_size=36)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part 20, the bachelor's capstone, takes one analysis from question to "
            "report, with an honest held-out check. Part 28 compares the ways of choosing a model. Part 29 builds the "
            "smoothers whose degrees of freedom we met here. Part 32 takes the lasso deep. Part 34 turns prediction errors into "
            "intervals with guarantees. Parts 51 and 52 face the curse of dimensionality head on. Part 54 asks why test error "
            "can be bounded at all. And Part 56 makes inference honest after the data has chosen the model, which is "
            "chapter ten's problem in its general form."
        ) as vo:
            intro.scale_to_fit_width(min(intro.width, 12.5))
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The optimism of least squares, exactly; the "
            "bias and variance of nearest neighbours for a parabola; the size of a neighbourhood in ten and a hundred "
            "dimensions; the odds from a paper without upon; ridge and the lasso for a standardized orthogonal design; and the precision "
            "of a good test for a rare condition. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"G. James, D. Witten, T. Hastie \& R. Tibshirani, \emph{An Introduction to Statistical Learning} (2nd ed., 2021)",
             r"T. Hastie, R. Tibshirani \& J. Friedman, \emph{The Elements of Statistical Learning} (2nd ed., 2009)",
             r"F. Mosteller \& D. Wallace, \emph{Inference and Disputed Authorship: The Federalist} (1964)",
             r"L. Breiman, J. Friedman, R. Olshen \& C. Stone, \emph{Classification and Regression Trees} (1984)"],
            [r"T. Cover \& P. Hart (1967); \ C. Mallows (1973); \ M. Stone (1974); \ B. Efron (1986, 2004)",
             r"R. Tibshirani (1996); \ A. Hoerl \& R. Kennard (1970); \ A. Ng \& M. Jordan (2002)",
             r"C. Ambroise \& G. McLachlan (2002); \ S. Kaufman et al.\ (2012); \ A. Blum \& M. Hardt (2015)",
             r"S. Bates, T. Hastie \& R. Tibshirani (2023); \ L. Breiman, \emph{Statistical Modeling: The Two Cultures} (2001)"])
        with self.voiceover(
            "The books and papers this part follows: An Introduction to Statistical Learning and The Elements of Statistical "
            "Learning, Mosteller and Wallace's book on the Federalist, and Breiman, Friedman, Olshen and Stone on trees, with "
            "the papers from Cover and Hart to Bates, Hastie and Tibshirani, and Leo Breiman's essay on the two cultures of "
            "statistical modelling."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=19, current=None)
        nxt = VGroup(label(r"Part 20", font_size=30, color=GREY_B), label(r"The Analysis", font_size=48),
                     label(r"one question, \ start to finish: \ the bachelor's capstone", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Nineteen parts of sixty-five, the ninth of Stage II. <bookmark mark='a'/> We can now predict, and say honestly "
            "how well we predict. <bookmark mark='b'/> Next, the bachelor's capstone: no new method, but one real question "
            "taken all the way, from the data's origins through exploration, a model, its checks, and a held-out test, to a "
            "report a reader could trust. Part 20: the analysis."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(19)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
