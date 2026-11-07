from __future__ import annotations

import numpy as np

from videos.stats.stats32.common import *  # noqa: F403


class Choosing(VoiceoverScene):
    def construct(self):
        self.card()
        self.options()
        self.quad()
        self.cvplot()
        self.models()
        self.mismatch()
        self.stability_def()
        self.stability_plot()
        self.advice()

    def card(self):
        card = chapter_card(7, r"Choosing $\lambda$", r"Prediction, \ selection, \ and stability", lit=(1974,), part=PART)
        with self.voiceover("Chapter seven. Choosing lambda."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def options(self):
        rows = [
            cmath(r"\text{theory}", r":", r"\lambda \approx \sigma\sqrt{2\log p / n}", font_size=32),
            cmath(r"C_p / \text{SURE}", r":", r"\mathrm{RSS} + 2\sigma^2 \cdot \#\{\hat\beta_j \ne 0\}", font_size=30),
            cmath(r"K\text{-fold CV}", r":", r"\text{the } \lambda \text{ with the smallest held-out error}", font_size=30),
            cmath(r"\text{one-SE rule}", r":", r"\text{the largest } \lambda \text{ within one SE of the minimum}", font_size=30),
        ]
        rows[2][-1].set_color(LASSO)
        whys = [why(r"needs $\sigma$; \ chapter nine's scale"), why(r"chapter four's df"), why(r"Part 19; \ Stone (1974)"),
                why(r"Breiman et al. (1984): \ a simpler model")]
        with self.voiceover(
            "<bookmark mark='a'/> There are several ways to choose lambda. Theory suggests a level proportional to the noise "
            "standard deviation times root two log p over n, just above the size of the largest pure-noise correlation, but "
            "it needs sigma. <bookmark mark='b'/> Mallows's C p, or Stein's unbiased risk estimate, uses chapter four's fact "
            "that the degrees of freedom are the number of nonzeros. <bookmark mark='c'/> K-fold cross-validation, Part 19's "
            "tool, picks the lambda with the smallest held-out prediction error. <bookmark mark='d'/> And the one standard "
            "error rule picks the most heavily penalized model whose error is within one standard error of the minimum."
        ) as vo:
            intro=label('Penalty tuning depends on the intended prediction or selection target',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def quad(self):
        rows = fit_rows(VGroup(
            label(r"the LARS paper's quadratic model for the diabetes data", font_size=26),
            label(r"10 main effects \ + \ 45 interactions \ + \ 9 squares \ = \ 64 candidate terms", font_size=26, color=LASSO),
            label(r"$2^{64}$ subsets: \ chapter three's 585 years", font_size=26, color=RES),
            label(r"one lasso path: \ a fraction of a second", font_size=26, color=HIT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A harder test: the quadratic model of the LARS paper, built from the standardized "
            "diabetes variables. <bookmark mark='b'/> Ten main effects, forty-five pairwise interactions and nine "
            "squares, sixty-four candidate terms for four hundred and forty-two patients. <bookmark mark='c'/> "
            "Exhaustively enumerating every subset would take chapter three's five hundred and eighty-five years at "
            "that hypothetical rate; pruning and integer solvers can do better. <bookmark mark='d'/> The lasso path "
            "takes a fraction of a second."
        ) as vo:
            self.add(diabetes_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def cvplot(self):
        d = load("cv")
        lams, cv, se = np.asarray(d["lams"]), np.asarray(d["cv"]), np.asarray(d["se"])
        x = np.log10(lams)
        A = axes([x.min() - 0.05, x.max() + 0.05], [2600, 6200], x_length=7.6, y_length=4.6, xlabel=r"$\log_{10}\lambda$",
                 ylabel=r"10-fold CV mean squared error", xticks=[-0.5, 0, 0.5, 1, 1.5], yticks=[3000, 4000, 5000, 6000],
                 center=[-2.0, 0.2, 0])
        ax = A.ax
        band_ = band(ax, x, cv - se, cv + se, LASSO, 0.2)
        line = polyline(ax, x, cv, LASSO, 3)
        im, i1 = d["i_min"], d["i_1se"]
        vmin = DashedLine(ax.c2p(x[im], 2600), ax.c2p(x[im], 6200), color=SPIKE, stroke_width=2.5)
        v1 = DashedLine(ax.c2p(x[i1], 2600), ax.c2p(x[i1], 6200), color=HIT, stroke_width=2.5)
        rows = fit_rows(VGroup(
            label(r"CV error, descriptive fold SE; all preprocessing fitted within training folds", font_size=22, color=LASSO),
            label(rf"gold: \ the minimum, \ {d['nz_min']} terms", font_size=22, color=SPIKE),
            label(rf"green: \ the one-SE rule, \ {d['nz_1se']} terms", font_size=22, color=HIT),
            label(rf"error {cv[im]:.0f} \ vs \ {cv[0]:.0f} for no predictors", font_size=22, color=GREY_A),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Ten-fold cross-validated error along the path, with a descriptive band based on "
            "fold variability. Overlapping training folds mean this is not a calibrated confidence band. Large "
            "lambdas on the right, where the model is empty. <bookmark mark='b'/> The minimum keeps fifteen of the "
            "sixty-four terms. <bookmark mark='c'/> The one standard error rule moves right to the simplest model "
            "whose error is within a standard error of the minimum, and keeps eleven. <bookmark mark='d'/> Either way"
            " the prediction error is about half that of predicting the mean for everyone."
        ) as vo:
            self.add(diabetes_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(band_), Create(line), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(vmin), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(v1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def models(self):
        d = load("cv")
        nice = {"age": "age", "sex": "sex", "bmi": "BMI", "bp": "BP", "tc": "TC", "ldl": "LDL", "hdl": "HDL", "tch": "TC/HDL",
                "ltg": "LTG", "glu": "glucose"}

        def pretty(t):
            if ":" in t:
                a, b = t.split(":")
                return rf"{nice[a]} $\times$ {nice[b]}"
            if t.endswith("^2"):
                return rf"{nice[t[:-2]]}$^2$"
            return nice[t]

        sel = d["sel_1se"]
        main = [pretty(t) for t in sel if ":" not in t and "^2" not in t]
        inter = [pretty(t) for t in sel if ":" in t or "^2" in t]
        rows = fit_rows(VGroup(
            label(r"the one-SE model's eleven terms", font_size=26),
            label(r"main effects: \ " + r", \ ".join(main), font_size=24, color=LASSO),
            label(r"curvature and interaction: \ " + r", \ ".join(inter), font_size=24, color=ENET),
            label(r"BMI, \ blood pressure and log triglycerides: \ the same core as chapter five", font_size=24, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The one standard error model's eleven terms. <bookmark mark='b'/> Five main effects: sex, "
            "body-mass index, blood pressure, HDL and log triglycerides. <bookmark mark='c'/> And six terms of curvature and "
            "interaction, such as age with sex and body-mass index with blood pressure. <bookmark mark='d'/> The core is the "
            "same as in chapter five's linear model; the quadratic terms add modest refinements."
        ) as vo:
            self.add(diabetes_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def mismatch(self):
        rows = [
            cmath(r"\text{CV}", r":", r"\text{targets prediction error}", font_size=32),
            cmath(r"\text{prediction}", r"\Rightarrow", r"\text{small } \lambda: \ \text{keep doubtful variables, \ shrink less}", font_size=28),
            cmath(r"\lambda_{\mathrm{CV}}", r":", r"\text{no general guarantee of selection consistency}", font_size=32),
            cmath(r"\text{the fix}", r":", r"\text{decide what you want: \ predict, \ or select}", font_size=30),
        ]
        rows[2][-1].set_color(RES)
        whys = [why(r"what it measures"), why(r"one $\lambda$, \ two jobs"), why(r"Meinshausen \& B\"uhlmann (2006); \ Leng et al. (2006)"),
                why(r"then stability, \ next")]
        with self.voiceover(
            "<bookmark mark='a'/> Cross-validation measures prediction error, and that is all it can measure. "
            "<bookmark mark='b'/> For prediction, the lasso likes a small lambda, which shrinks the real effects "
            "less, and it pays for that by admitting doubtful variables. <bookmark mark='c'/> So the cross-validated "
            "lambda is not consistent for selection: there are asymptotic regimes where it continues including noise "
            "variables, as Nicolai Meinshausen and Peter Bühlmann, and independently Chenlei Leng, Yi Lin and Grace "
            "Wahba, showed in 2006. <bookmark mark='d'/> The lesson: decide whether you want predictions or a list of"
            " variables, and tune for that."
        ) as vo:
            intro=label('Prediction-optimal tuning need not recover the exact support',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def stability_def(self):
        rows = [
            cmath(r"\text{subsample}", r":", r"\text{draw half the data, \ run the lasso path; \ repeat } B \text{ times}", font_size=28),
            cmath(r"\hat\Pi_j(\lambda)", r"=", r"\text{the share of subsamples selecting } x_j", font_size=30),
            cmath(r"\text{stable set}", r":", r"\{j : \max_\lambda \hat\Pi_j(\lambda) \ge \pi_{\text{thr}}\}", font_size=30),
            cmath(r"E(\text{false selections})", r"\le", r"\dfrac{q^2}{(2\pi_{\text{thr}} - 1)\, p}", font_size=30),
        ]
        rows[1][-1].set_color(LASSO)
        whys = [why(r"Meinshausen \& B\"uhlmann (2010)"), why(r"selection probabilities"), why(r"e.g. $\pi_{\text{thr}} = 0.8$"),
                why(r"$q$: expected union over the specified path; exchangeable noise assumptions")]
        with self.voiceover(
            "<bookmark mark='a'/> For selection, Meinshausen and Bühlmann's stability selection of 2010 is more "
            "reliable. Draw half the data at random, run the lasso path, and repeat many times. <bookmark mark='b'/> "
            "For each variable and each lambda, record the share of subsamples in which it was selected. <bookmark "
            "mark='c'/> Keep the variables whose selection probability reaches a high threshold, such as point eight,"
            " somewhere on the path. <bookmark mark='d'/> Their expected false-selection bound also requires "
            "noise-variable exchangeability and a base procedure no worse than random selection. For a whole lambda "
            "region, q counts the union selected per subsample. The diabetes paths are descriptive stability "
            "estimates, not a verified false-selection guarantee."
        ) as vo:
            intro=label('Stability frequencies and error-control assumptions are different objects',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def stability_plot(self):
        d = load("cv")
        lams, P = np.asarray(d["stab_lams"]), np.asarray(d["stab"])
        labs = d["stab_labels"]
        x = np.log10(lams)
        A = axes([x.min() - 0.05, x.max() + 0.05], [0, 1.05], x_length=7.4, y_length=4.6, xlabel=r"$\log_{10}\lambda$",
                 ylabel=r"selection probability \ (60 half-samples)", xticks=[0, 0.5, 1, 1.5], yticks=[0, 0.5, 0.8, 1], center=[-2.0, 0.2, 0])
        ax = A.ax
        thr = DashedLine(ax.c2p(x.min(), 0.8), ax.c2p(x.max(), 0.8), color=SPIKE, stroke_width=2)
        mx = P.max(0)
        lines = VGroup(*[polyline(ax, x, P[:, k], LASSO if mx[k] >= 0.8 else GREY_C, 3 if mx[k] >= 0.8 else 1.5)
                         for k in range(P.shape[1])])
        rows = fit_rows(VGroup(
            label(r"the twelve most often selected terms", font_size=22),
            label(rf"blue: \ the {d['n_stable']} that reach 0.8", font_size=22, color=LASSO),
            label(r"sex, \ BMI, \ BP, \ HDL, \ LTG, \ glucose", font_size=22, color=LASSO),
            label(r"age $\times$ sex, age $\times$ LDL, sex $\times$ BMI, BMI $\times$ BP, glucose$^2$", font_size=22, color=ENET),
            label(r"grey: \ in and out with the subsample", font_size=22, color=GREY_B),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Stability paths for the quadratic diabetes model: the twelve terms selected most "
            "often, against lambda. <bookmark mark='b'/> Eleven reach the threshold of point eight in this "
            "simulation: <bookmark mark='c'/> six main effects, <bookmark mark='d'/> and five quadratic terms: age "
            "with sex, age with LDL, sex with body-mass index, body-mass index with blood pressure, and glucose "
            "squared. <bookmark mark='e'/> Other terms have lower selection frequencies on this chosen path. This "
            "measures stability of association, not which variables truly cause the outcome."
        ) as vo:
            self.add(diabetes_tag())
            self.play(FadeIn(A), Create(thr))
            vo.wait_until("a")
            self.play(Create(lines), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"to predict: \ CV, \ the minimum or one SE", font_size=26, color=LASSO),
            label(r"to select: \ stability selection, \ or a nonconvex penalty tuned by CV", font_size=26, color=ENET),
            label(r"to make claims about coefficients: \ chapter ten", font_size=26, color=RES),
            label(r"always: \ report how many variables, \ and how stable they were", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In short. To predict, cross-validate. <bookmark mark='b'/> To select, use stability "
            "selection, or a nonconvex penalty whose selection is less tied to shrinkage. <bookmark mark='c'/> To make "
            "claims about individual coefficients, with intervals, you need the tools of chapter ten. "
            "<bookmark mark='d'/> And always report how many variables were selected and how stable that selection was."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
