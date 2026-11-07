from __future__ import annotations

from videos.stats.stats36.common import *  # noqa: F403


class DML(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.orthogonal()
        self.crossfit()
        self.design()
        self.results()
        self.board()
        self.plr()

    def card(self):
        card = chapter_card(10, r"Double machine learning", r"Flexible nuisances, \ honest intervals", lit=(2018,), part=PART)
        with self.voiceover("Chapter ten. Double machine learning."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = fit_rows(VGroup(
            label(r"real confounding is not linear: \ thresholds, \ interactions, \ curves", font_size=26),
            label(r"so fit $\mu_t$ and $e$ by forests, \ boosting, \ lasso, \ networks (Part 34)", font_size=26, color=BANDC),
            label(r"but machine learning trades bias for variance, \ and the bias leaks into $\hat\tau$", font_size=26, color=MISSC),
            label(r"and it overfits: \ residuals on its own training data are too small", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Real confounding is rarely linear: doctors use thresholds, effects interact, risks curve. "
            "<bookmark mark='b'/> So it is natural to fit the outcome regressions and the propensity score with the flexible "
            "learners of Part 34. <bookmark mark='c'/> But machine learning methods deliberately accept bias to reduce "
            "variance, and a regularized nuisance fit leaks its bias into the causal estimate. <bookmark mark='d'/> And they "
            "overfit: their residuals on the data they were trained on are too small, which makes any standard error built "
            "from them too small."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def orthogonal(self):
        rows = [
            cmath(r"\hat\tau - \tau", r"\approx", r"\text{(average of } \psi-\tau \text{ at the truth)} + \text{(nuisance error terms)}", font_size=26),
            cmath(r"\text{AIPW's score}", r":", r"\text{first-order insensitive to errors in } \mu \text{ and } e", font_size=28),
            cmath(r"\text{remainder}", r"\lesssim", r"\|\hat\mu - \mu\| \cdot \|\hat e - e\|", font_size=30),
            cmath(r"\text{each } o(n^{-1/4})", r"\Rightarrow", r"\text{the product is } o(n^{-1/2}): \ \text{negligible}", font_size=28),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"a Taylor expansion"), why(r"Neyman orthogonality"), why(r"a product of two errors"),
                why(r"slower than parametric is enough")]
        with self.voiceover(
            "<bookmark mark='a'/> The resolution has two parts. Expand the estimation error: the average of the "
            "centered score at the true nuisances, which is the good part, plus terms from the errors in the fitted "
            "nuisances. <bookmark mark='b'/> The doubly robust score has a special property, Neyman orthogonality: "
            "its derivative with respect to the nuisances is zero, so small errors in them have no first-order "
            "effect. <bookmark mark='c'/> What remains is roughly the product of the outcome model's error and the "
            "propensity model's error. <bookmark mark='d'/> If each converges faster than n to the minus a quarter, "
            "much slower than a parametric model's n to the minus a half, their product is negligible, and, with "
            "overlap, suitable moments and the other regularity conditions, the estimate has the same first-order "
            "behavior as if the nuisances were known. Part 49 proves this."
        ) as vo:
            intro=label('Orthogonality controls first-order nuisance errors under regularity',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def crossfit(self):
        boxes = VGroup(*[Rectangle(width=5.4, height=0.6, stroke_color=GREY_B, stroke_width=2,
                                   fill_color=(BANDC if k == 0 else PSC), fill_opacity=0.35) for k in range(2)]).arrange(RIGHT, buff=0.2)
        boxes.move_to([0, 1.4, 0])
        labs = VGroup(label(r"half 1", font_size=22).move_to(boxes[0]), label(r"half 2", font_size=22).move_to(boxes[1]))
        rows = fit_rows(VGroup(
            label(r"fit $\hat\mu_0, \hat\mu_1, \hat e$ on half 2; \ evaluate $\psi_i$ on half 1", font_size=24, color=BANDC),
            label(r"then swap; \ average all the $\psi_i$", font_size=24, color=PSC),
            label(r"no direct own-outcome reuse; \ approximation and finite-sample bias can remain", font_size=24, color=TAUC),
            label(r"Chernozhukov, \ Chetverikov, \ Demirer, \ Duflo, \ Hansen, \ Newey \& Robins (2018)", font_size=22, color=GREY_A),
        ), 12.4, 0.45, [0, -0.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The second part is cross-fitting. Split the data in two. <bookmark mark='b'/> Fit "
            "the outcome regressions and the propensity score on the second half, and evaluate each patient's score "
            "on the first half. <bookmark mark='c'/> Then swap the halves, and average all the scores. <bookmark "
            "mark='d'/> No patient's score uses a nuisance model trained on that patient. This removes direct reuse "
            "of its outcome in nuisance fitting; finite-sample bias and nuisance approximation error can still "
            "remain. <bookmark mark='e'/> Victor Chernozhukov and six colleagues set out this double, or debiased, "
            "machine learning in 2018; it works with any learner fast enough."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(boxes), FadeIn(labs))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k]))
        self.clear_scene()

    def design(self):
        rows = [
            cmath(r"X", r"\sim", r"U[0, 1]^5, \ \ n = 1{,}000", font_size=32),
            cmath(r"\mathrm{logit}\, e(x)", r"=", r"2 \sin(\pi x_1 x_2) + 4 (x_3 - \tfrac12)^2 - 1.2", font_size=28),
            cmath(r"\mu_0(x)", r"=", r"10 \sin(\pi x_1 x_2) + 20 (x_3 - \tfrac12)^2 + 10 x_4", font_size=28),
            cmath(r"\tau(x)", r"=", r"2 + 2 x_5, \ \ \text{ATE} = 3", font_size=32),
        ]
        rows[1][-1].set_color(PSC)
        whys = [why(r"five covariates"), why(r"curved, \ interacting confounding"), why(r"Part 34's Friedman function"),
                why(r"the target")]
        with self.voiceover(
            "<bookmark mark='a'/> A test with nonlinear confounding. Five uniform covariates and a thousand patients. "
            "<bookmark mark='b'/> The chance of treatment depends on a sine of a product and a parabola. <bookmark mark='c'/> "
            "The untreated outcome is Friedman's function from Part 34, sharing those shapes. <bookmark mark='d'/> The "
            "effect varies, with an average of three."
        ) as vo:
            intro=label('A nonlinear confounding simulation has population average effect three',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def results(self):
        d = load("dml")
        rows = [[r"estimator", r"bias", r"mean SE", r"90\% coverage"],
                [r"OLS, \ linear in $X$", rf"{d['ols']['bias']:.2f}", r"", rf"{100 * d['ols']['cover']:.0f}\%"],
                [r"AIPW, \ forests, \ no cross-fitting", rf"{d['nocf']['bias']:.2f}", rf"{d['nocf']['mean_se']:.2f}", rf"{100 * d['nocf']['cover']:.0f}\%"],
                [r"DML: \ forests, \ cross-fitted", rf"{d['dml']['bias']:.2f}", rf"{d['dml']['mean_se']:.2f}", rf"{100 * d['dml']['cover']:.0f}\%"]]
        tab = table_rows(rows, font_size=26, col_buff=0.8, row_buff=0.3, colors=[GREY_A, MISSC, MISSC, BANDC]).move_to([0, 0.9, 0])
        foot = label(rf"{d['reps']} simulated studies; \ sampling SD estimate {d['dml']['sd']:.2f}", font_size=22, color=GREY_A).move_to([0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A hundred and fifty simulated studies. <bookmark mark='b'/> Linear regression "
            "adjustment is biased by over one, and its intervals never cover the truth. <bookmark mark='c'/> The "
            "doubly robust estimator with random forests fitted to all the data is biased by more than half a point, "
            "and its standard errors are too small: it never covers either. <bookmark mark='d'/> The same estimator "
            "with cross-fitting has a small bias, standard errors that match its estimated sampling variability, and "
            "covers " + f"{100 * d['dml']['cover']:.0f}" + " percent of "
            "the time."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
            self.play(FadeIn(foot))
        self.clear_scene()

    def board(self):
        rows = board_rows("OLS adjustment, \\ linear", "no cross-fitting", "cross-fitted")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board. Linear adjustment under nonlinear confounding: broken. Forests "
                   "without cross-fitting: broken. <bookmark mark='b'/> Double machine learning is within the Board's "
                   "Monte Carlo tolerance here. This finite simulation does not establish a coverage guarantee.",
                   [("a", [0, 1]), ("b", [2])])

    def plr(self):
        rows = fit_rows(VGroup(
            label(r"for a constant effect: \ the partially linear model $Y = \theta T + g(X) + \varepsilon$", font_size=26),
            label(r"Robinson (1988): \ regress $Y - \hat E[Y \mid X]$ on $T - \hat E[T \mid X]$", font_size=26, color=BANDC),
            label(r"Frisch--Waugh--Lovell with machine learning: \ residuals on residuals", font_size=26, color=GREY_A),
            label(r"next: \ effects that differ from person to person", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> When the effect is assumed constant, the same ideas give the partially linear model. "
            "<bookmark mark='b'/> Peter Robinson showed in 1988 that one can regress the outcome's residual from its "
            "prediction given X on the treatment's residual from its prediction given X. <bookmark mark='c'/> It is Part 12's "
            "Frisch–Waugh–Lovell theorem with machine-learned residuals, cross-fitted. <bookmark mark='d'/> Next, effects "
            "that are allowed to differ from one person to the next."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
