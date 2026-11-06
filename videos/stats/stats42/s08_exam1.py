from __future__ import annotations

import numpy as np

from videos.stats.stats42.common import *  # noqa: F403

LTOP = 1.45  # the first ladder row, under a lifted card


class ExamLikelihood(ExamMixin, VoiceoverScene):
    def construct(self):
        self.card()
        self.p1()
        self.p2()
        self.p3()

    def card(self):
        card = chapter_card(7, r"Exam I: \ likelihood", r"Problems 1--3", part=PART)
        with self.voiceover("Chapter seven. The exam begins, with three problems on likelihood."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------------------------------ Problem 1
    def p1(self):
        d = load("p_mle")
        ys = ", ".join(f"{int(v)}" for v in d["y"])
        card = ExamCard(1, r"an MLE, \ its information, \ and a sandwich", r"Parts 22, 24", [
            rf"Twelve adults report their visits to a doctor last year: \ {ys}.",
            r"Model them as independent Poisson($\lambda$). \ Find $\hat\lambda$, \ its standard error from the Fisher information,",
            r"and the sandwich standard error. \ Which would you report, \ and why?"], marks=10, color=MODELC)
        self.pose_voiceover(
            "Problem one. Twelve adults report how many times they visited a doctor last year: four zeros, a one, two twos, "
            "a four, five, six, nine and eleven. Model the counts as independent Poisson with mean lambda. Find the maximum "
            "likelihood estimate, its standard error from the Fisher information, and the sandwich standard error. Which "
            "would you report, and why? Pause the video and try it.", card)
        rows = [
            cmath(r"\ell(\lambda)", r"=", r"\textstyle\sum y_i \log\lambda - n\lambda, \ \ \ell'(\lambda) = \sum y_i / \lambda - n = 0", font_size=30),
            cmath(r"\hat\lambda", r"=", rf"\bar y = {d['sumy']:.0f} / {d['n']} = {d['lam']:.3f}, \ \ I(\lambda) = n / \lambda", font_size=32),
            cmath(r"\text{SE}_{\text{model}}", r"=", rf"\sqrt{{\hat\lambda / n}} = \sqrt{{{d['lam']:.3f} / 12}} = {d['se_model']:.3f}", font_size=32),
            cmath(r"\text{SE}_{\text{sand}}", r"=", rf"\sqrt{{A^{{-1}} B A^{{-1}}}} = \sqrt{{\textstyle\sum (y_i - \bar y)^2}} / n = \sqrt{{{d['ss']:.1f}}} / 12 = {d['se_sand']:.3f}", font_size=30),
        ]
        rows[3][-1].set_color(SAND)
        whys = [why(r"the log-likelihood and score"), why(r"the MLE and information"), why(r"trust the model"), why(r"trust only the score")]
        with self.voiceover(
            f"<bookmark mark='a'/> The log-likelihood is the sum of y times log lambda, minus n lambda, and the score sets "
            f"its derivative to zero. <bookmark mark='b'/> So the estimate is the sample mean, forty over twelve, "
            f"{say(d['lam'], 3)}; the information is n over lambda. <bookmark mark='c'/> The model-based standard error is "
            f"the root of lambda hat over n: {say(d['se_model'], 3)}. <bookmark mark='d'/> The sandwich of Part twenty-two "
            f"replaces the model's variance of the score with its empirical variance: A inverse B A inverse, which here "
            f"reduces to the root of the sum of squared deviations, over n. It is {say(d['se_sand'], 3)}, almost twice as "
            f"large."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=LTOP, x=-0.9, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not card])
        s2 = d["ss"] / (d["n"] - 1)
        rows2 = fit_rows(VGroup(
            label(rf"the Poisson says variance $=$ mean: \ but $s^2 = {s2:.1f}$, \ $\bar y = {d['lam']:.2f}$", font_size=26, color=MODELC),
            label(r"overdispersed: \ the model-based SE is too small by half", font_size=26, color=MODELC),
            label(r"report the sandwich \ (or fit a negative binomial, \ Part 24)", font_size=26, color=SAND),
            label(rf"the World's whole adult population: \ variance / mean $= {d['dispersion']:.1f}$", font_size=24, color=EXACT),
        ), 12.4, 0.5, [0, -0.9, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Which to report? A Poisson's variance equals its mean, but these twelve counts have mean "
            f"{say(d['lam'], 2)} and variance {say(s2, 1)}. <bookmark mark='b'/> They are overdispersed, so the model-based "
            f"standard error, which trusts the Poisson's variance, is too small by about half. <bookmark mark='c'/> Report "
            f"the sandwich, which needs only the mean model to be right, or fit a negative binomial as in Part twenty-four. "
            f"<bookmark mark='d'/> In the World's whole adult population, the variance of visits is {say(d['dispersion'], 1)} "
            f"times the mean, so this was no fluke of twelve people."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows2[k], shift=RIGHT * 0.2))
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        show_board(self, board_rows("Poisson"),
                   "<bookmark mark='a'/> The Board settles it, with five hundred of the World's adults at a time. The "
                   "Poisson model's interval for the mean number of visits covers half the time: broken. <bookmark "
                   "mark='b'/> The sandwich covers eighty-nine percent: kept.",
                   [("a", [0]), ("b", [1])])

    # ------------------------------------------------------------------------------------------ Problem 2
    def p2(self):
        d = load("p_irls")
        h0, h1 = d["hist"][0], d["hist"][1]
        card = ExamCard(2, r"one step of IRLS", r"Parts 21, 24", [
            r"Bliss's beetles (1935): \ at eight doses of carbon disulphide, \ $n_i$ beetles exposed, \ $k_i$ killed.",
            r"For logistic regression of the kill rate on $x = \log_{10}$ dose, \ start IRLS at $\beta = 0$:",
            r"give the weights, \ the working response, \ and the first step's $\beta$."], marks=10, color=S.PRIOR)
        self.pose_voiceover(
            "Problem two. In 1935 Chester Bliss exposed batches of flour beetles to eight doses of carbon disulphide and "
            "counted how many were killed. Fit a logistic regression of the kill rate on the log dose by iteratively "
            "reweighted least squares. Starting from beta equal to zero, give the weights, the working response, and the "
            "first step. Pause and try it.", card)
        rows = [
            cmath(r"\beta = 0", r":", r"\mu_i = \tfrac12, \ \ w_i = n_i \mu_i (1 - \mu_i) = n_i / 4", font_size=32),
            cmath(r"z_i", r"=", r"\eta_i + \frac{\hat p_i - \mu_i}{\mu_i (1 - \mu_i)} = 4 (\hat p_i - \tfrac12)", font_size=32),
            cmath(r"X^\top W X", r"=", rf"\begin{{pmatrix}} {h0['XtWX'][0][0]:.2f} & {h0['XtWX'][0][1]:.2f} \\ {h0['XtWX'][1][0]:.2f} & {h0['XtWX'][1][1]:.2f} \end{{pmatrix}}, \ \ X^\top W z = \begin{{pmatrix}} {h0['XtWz'][0]:.2f} \\ {h0['XtWz'][1]:.2f} \end{{pmatrix}}", font_size=28),
            cmath(r"\beta^{(1)}", r"=", rf"(X^\top W X)^{{-1}} X^\top W z = ({h1['b'][0]:.2f}, \ {h1['b'][1]:.2f})", font_size=32),
        ]
        rows[3][-1].set_color(S.PRIOR)
        whys = [why(r"the binomial variance"), why(r"the working response"), why(r"weighted least squares"), why(r"solve")]
        with self.voiceover(
            f"<bookmark mark='a'/> At beta equal to zero, every fitted probability is a half, so each dose's weight is its "
            f"number of beetles times a half times a half: n i over four. <bookmark mark='b'/> The working response is the "
            f"linear predictor, zero, plus the residual divided by the variance function: four times the observed kill "
            f"rate minus a half. <bookmark mark='c'/> Then one weighted least squares fit: the two by two matrix X "
            f"transpose W X, and the vector X transpose W z. <bookmark mark='d'/> Solving gives the first step: an "
            f"intercept of {say(h1['b'][0], 1)} and a slope of {say(h1['b'][1], 1)}. Newton's method for the logistic "
            f"likelihood is exactly this, repeated."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=LTOP, x=-0.9, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not card])
        x, p = np.asarray(d["x"]), np.asarray(d["p"])
        A = axes([1.65, 1.9], [0, 1], x_length=6.6, y_length=3.4, xlabel=r"$\log_{10}$ dose", ylabel=r"share killed",
                 xticks=[1.7, 1.8, 1.9], yticks=[0, 0.5, 1], center=[-2.6, -1.0, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=DATA) for a, b in zip(x, p)])
        xs = np.linspace(1.65, 1.9, 120)
        curves = VGroup()
        shades = [GREY_C, GREY_B, GREY_A, S.PRIOR, S.PRIOR]
        for i in range(1, 6):
            b = d["hist"][i]["b"] if i < len(d["hist"]) else d["b"]
            curves.add(curve(ax, xs, 1 / (1 + np.exp(-(b[0] + b[1] * xs))), shades[i - 1], 3 if i < 5 else 4))
        tab = table_rows([[r"step", r"$\beta_0$", r"$\beta_1$", r"$\ell$"]] +
                         [[f"{i}", f"{d['hist'][i]['b'][0]:.2f}", f"{d['hist'][i]['b'][1]:.2f}", f"{d['hist'][i]['ll']:.2f}"] for i in range(6)],
                         font_size=20, col_buff=0.35, row_buff=0.12).move_to([4.3, -1.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here are Bliss's eight doses and their kill rates, with the curve after each step. "
            f"<bookmark mark='b'/> The first step already has the right shape; the log-likelihood jumps from "
            f"{say(h0['ll'], 0)} to {say(h1['ll'], 0)}. <bookmark mark='c'/> By the fourth step the estimates agree to two "
            f"decimals, and by the sixth to eight: an intercept of {say(d['b'][0], 2)} and a slope of {say(d['b'][1], 2)}. "
            f"Newton's quadratic convergence, as Part twenty-one promised. The dose that kills half, minus the intercept "
            f"over the slope, is {say(d['ld50'], 3)} on the log scale: about {d['ld50_dose']:.0f} milligrams per litre."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Bliss (1935): \ beetles and carbon disulphide")))
            vo.wait_until("a")
            self.play(FadeIn(dots))
            vo.wait_until("b")
            self.play(Create(curves[0]), FadeIn(tab))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in curves[1:]], lag_ratio=0.5), run_time=3.0)
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------------------------------ Problem 3
    def p3(self):
        d = load("p_reml")
        card = ExamCard(3, r"ML and REML for a variance", r"Parts 23, 25", [
            r"In $y = X\beta + \varepsilon$, \ $\varepsilon \sim N(0, \sigma^2 I_n)$, \ $X$ of full rank $p$, \ show that ML gives",
            r"$\hat\sigma^2 = \text{RSS}/n$ \ and REML gives $\text{RSS}/(n - p)$. \ Compute both for Longley's 16 years \ ($p = 7$)."],
            marks=10, color=S.ALT)
        self.pose_voiceover(
            "Problem three. In the linear model with normal errors of variance sigma squared and a design of full rank p, "
            "show that maximum likelihood estimates sigma squared by the residual sum of squares over n, and restricted "
            "maximum likelihood by the residual sum of squares over n minus p. Then compute both for Longley's sixteen years "
            "of employment data, with seven coefficients. Pause and try it.", card)
        rows = [
            cmath(r"\ell(\hat\beta, \sigma^2)", r"=", r"-\tfrac n2 \log \sigma^2 - \tfrac{\text{RSS}}{2\sigma^2} \ \Rightarrow \ \hat\sigma^2_{\text{ML}} = \text{RSS}/n", font_size=30),
            cmath(r"E\,\hat\sigma^2_{\text{ML}}", r"=", r"\tfrac{n - p}{n}\, \sigma^2: \ \ \hat\beta \text{ used up } p \text{ dimensions}", font_size=30),
            cmath(r"K^\top y", r"\sim", r"N(0, \sigma^2 I_{n-p}), \ \ K^\top X = 0, \ K^\top K = I, \ \ \|K^\top y\|^2 = \text{RSS}", font_size=28),
            cmath(r"\ell_R(\sigma^2)", r"=", r"-\tfrac{n-p}{2} \log\sigma^2 - \tfrac{\text{RSS}}{2\sigma^2} \ \Rightarrow \ \hat\sigma^2_{\text{REML}} = \text{RSS}/(n - p)", font_size=30),
        ]
        rows[3][-1].set_color(S.ALT)
        whys = [why(r"profile out $\beta$"), why(r"biased low"), why(r"error contrasts: \ free of $\beta$"), why(r"the restricted likelihood")]
        with self.voiceover(
            "<bookmark mark='a'/> Maximize over beta first: at the least squares fit, the log-likelihood is minus n over two "
            "log sigma squared, minus the residual sum of squares over two sigma squared, maximized at RSS over n. "
            "<bookmark mark='b'/> Its expectation is n minus p over n times sigma squared, too small, because the fitted "
            "beta has used up p of the n dimensions. <bookmark mark='c'/> REML uses only the n minus p error contrasts: "
            "project y onto an orthonormal basis K of the space orthogonal to X's columns. These contrasts do not involve "
            "beta at all, are normal with variance sigma squared, and their squared length is the residual sum of squares. "
            "<bookmark mark='d'/> Their likelihood has n minus p in place of n, and its maximum is RSS over n minus p, "
            "unbiased."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=LTOP, x=-0.9, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not card])
        grid = np.asarray(d["grid"]) / 1e3
        A = axes([grid[0], grid[-1]], [-6, 0.5], x_length=6.6, y_length=3.4, xlabel=r"$\sigma^2$, \ thousands",
                 ylabel=r"log-likelihood, \ from its maximum", xticks=[50, 100, 150, 200, 250, 300, 350], yticks=[-6, -3, 0],
                 center=[-2.6, -1.0, 0])
        ax = A.ax
        ml = clip_curve(ax, grid, d["ll_ml"], MODELC, 4, ymin=-6)
        rl = clip_curve(ax, grid, d["ll_reml"], S.ALT, 4, ymin=-6)
        vml = DashedLine(ax.c2p(d["s2_ml"] / 1e3, -6), ax.c2p(d["s2_ml"] / 1e3, 0), color=MODELC, stroke_width=2)
        vrl = DashedLine(ax.c2p(d["s2_reml"] / 1e3, -6), ax.c2p(d["s2_reml"] / 1e3, 0), color=S.ALT, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"RSS $= {d['rss']:,.0f}$", font_size=24),
            label(rf"ML: \ RSS/16 $= {d['s2_ml']:,.0f}$", font_size=24, color=MODELC),
            label(rf"REML: \ RSS/9 $= {d['s2_reml']:,.0f}$", font_size=24, color=S.ALT),
            label(r"ratio $9/16$: \ ML is 44\% low", font_size=24, color=GREY_A),
            label(rf"20,000 simulations: \ means {d['sim_ml']:,.0f} \ and {d['sim_reml']:,.0f}", font_size=22, color=EXACT),
        ), 4.6, 0.36, [4.45, -1.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> For Longley's data the residual sum of squares is about {d['rss'] / 1e3:.0f} thousand. "
            f"<bookmark mark='b'/> The ordinary likelihood peaks at that over sixteen, {d['s2_ml'] / 1e3:.0f} thousand; "
            f"<bookmark mark='c'/> the restricted likelihood at that over nine, {d['s2_reml'] / 1e3:.0f} thousand. <bookmark "
            f"mark='d'/> With seven coefficients and only sixteen years, maximum likelihood is forty-four percent too low. "
            f"<bookmark mark='e'/> Simulating twenty thousand data sets from Longley's own design, with sigma squared at the "
            f"REML value, the ML estimates average nine sixteenths of the truth and the REML estimates average the truth. "
            f"In the mixed models of Part twenty-five the same correction applies to every variance component."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Longley (1967): \ US employment, \ 1947--1962")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ml), Create(vml), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(rl), Create(vrl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
