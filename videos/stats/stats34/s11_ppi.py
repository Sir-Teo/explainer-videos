from __future__ import annotations

import numpy as np

from videos.stats.stats34.common import *  # noqa: F403


def ci_row(ax, y, est, lo, hi, color, xmin, xmax):
    lo_, hi_ = max(lo, xmin), min(hi, xmax)
    return VGroup(Line(ax.c2p(lo_, y), ax.c2p(hi_, y), color=color, stroke_width=7, stroke_opacity=0.8),
                  Dot(ax.c2p(est, y), radius=0.08, color=WHITE))


class PPI(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.watch()
        self.bias()
        self.three()
        self.ladder_()
        self.variance()
        self.loose()
        self.board()
        self.lineage()
        self.uses()

    def card(self):
        card = chapter_card(10, r"Prediction-powered inference", r"Many guesses, \ a few labels", lit=(2023,), part=PART)
        with self.voiceover("Chapter ten. Prediction-powered inference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = fit_rows(VGroup(
            label(r"$n$ cases with the true label $Y$: \ expensive", font_size=26, color=LABC),
            label(r"$N \gg n$ cases with only a model's guess $f(X)$: \ cheap", font_size=26, color=GUESSC),
            label(r"protein structures from AlphaFold; \ galaxies classified by a network; \ text coded by a language model", font_size=24, color=GREY_A),
            label(r"estimate a population quantity $\theta$, \ with a valid interval", font_size=26, color=CALC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So far we have put intervals around predictions. Now turn it round: use predictions to "
            "estimate something else. Suppose measuring the truth is expensive, so we have it for only n cases. "
            "<bookmark mark='b'/> But a machine-learning model can guess it cheaply for a great many more, N. <bookmark "
            "mark='c'/> This is now common in science: protein structures predicted by AlphaFold instead of solved by "
            "crystallography, galaxies classified by a neural network instead of by volunteers, documents coded by a "
            "language model instead of by researchers. <bookmark mark='d'/> We want a population quantity, a mean or a "
            "regression coefficient, with an interval we can trust, and we want the guesses to help."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def watch(self):
        d = load("ppi")
        fy, yy = np.asarray(d["pts_f"], float), np.asarray(d["pts_y"], float)
        A = axes([95, 185], [95, 185], x_length=4.8, y_length=4.8, xlabel=r"watch's guess", ylabel=r"clinic reading",
                 xticks=[100, 140, 180], yticks=[100, 140, 180], center=[-3.4, 0.2, 0])
        ax = A.ax
        k = (fy > 95) & (fy < 185) & (yy > 95) & (yy < 185)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.03, color=GUESSC, fill_opacity=0.6) for a, b in zip(fy[k], yy[k])])
        diag = DashedLine(ax.c2p(95, 95), ax.c2p(185, 185), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"the island's mean systolic blood pressure", font_size=22),
            label(rf"a label: \ a clinic visit, \ three cuff readings; \ $n = {d['n']}$", font_size=22, color=LABC),
            label(rf"a guess: \ a smartwatch's estimate; \ $N = {d['N']:,}$", font_size=22, color=GUESSC),
            label(r"the watch: \ a forest on age, \ sex, \ BMI and its pulse wave", font_size=22, color=TREEC),
            label(r"trained on early users, \ all aged 18--50", font_size=22, color=MISSC),
            label(rf"correlation with the truth: \ {d['corr_fy']:.2f}", font_size=22, color=CALC),
        ), 5.4, 0.36, [3.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the World. A health agency wants the island's mean systolic blood pressure. "
            "<bookmark mark='b'/> The truth for a person requires a clinic visit with three cuff readings; it can afford "
            "three hundred. <bookmark mark='c'/> But twenty thousand residents wear a smartwatch that estimates blood "
            "pressure. <bookmark mark='d'/> The watch's estimate is a random forest on the wearer's age, sex, body-mass "
            "index and the watch's own pulse-wave signal, <bookmark mark='e'/> trained by the manufacturer on its early "
            "users, who were all aged eighteen to fifty. <bookmark mark='f'/> Its guesses track the clinic readings "
            "well, with correlation " + say(d["corr_fy"]) + ", but not along the diagonal."
        ) as vo:
            self.add(bp_tag())
            self.play(FadeIn(A), Create(diag))
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                if k == 2:
                    self.play(FadeIn(dots), FadeIn(side[k]))
                else:
                    self.play(FadeIn(side[k]))
        self.clear_scene()

    def bias(self):
        d = load("ppi")
        ba = d["by_age"]
        A = axes([0, 7], [105, 155], x_length=7.4, y_length=4.4, xlabel=r"age", ylabel=r"mean systolic (mm Hg)",
                 xticks=[], yticks=[110, 130, 150], center=[-2.0, 0.2, 0])
        ax = A.ax
        xs = np.arange(7) + 0.5
        yl = polyline(ax, xs, [b["y"] for b in ba], LABC, 3.5)
        fl = polyline(ax, xs, [b["f"] for b in ba], GUESSC, 3.5)
        yd = VGroup(*[Dot(ax.c2p(x, b["y"]), radius=0.07, color=LABC) for x, b in zip(xs, ba)])
        fd = VGroup(*[Dot(ax.c2p(x, b["f"]), radius=0.07, color=GUESSC) for x, b in zip(xs, ba)])
        labs = VGroup(*[label(b["band"].replace("-99", "+").replace("-", "--"), font_size=18, color=GREY_A)
                        .next_to(ax.c2p(x, 105), DOWN, buff=0.15) for x, b in zip(xs, ba)])
        train = Rectangle(width=ax.c2p(3, 0)[0] - ax.c2p(0, 0)[0], height=4.4, stroke_width=0, fill_color=TREEC,
                          fill_opacity=0.1).move_to(ax.c2p(1.5, 130))
        side = fit_rows(VGroup(
            label(r"truth by age", font_size=22, color=LABC),
            label(r"the watch by age", font_size=22, color=GUESSC),
            label(r"shaded: \ the ages it was trained on", font_size=22, color=TREEC),
            label(rf"80+: \ truth {ba[-1]['y']:.0f}, \ watch {ba[-1]['f']:.0f}", font_size=22, color=MISSC),
            label(rf"the island: \ guesses average {abs(d['bias']):.1f} too low", font_size=22, color=MISSC),
        ), 4.2, 0.4, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is the problem. By age, the true mean pressure rises steadily, <bookmark mark='b'/> "
            "and the watch agrees, <bookmark mark='c'/> over the ages it was trained on. <bookmark mark='d'/> Beyond fifty "
            "it falls behind, because a forest cannot extrapolate: for a pressure higher than any it saw in training, it "
            "cannot extrapolate its prediction beyond the range of training responses. For the over-eighties, the truth averages a hundred and fifty-one, the "
            "watch a hundred and thirty-six. <bookmark mark='e'/> Over the whole island, its guesses are about three "
            "millimetres of mercury too low."
        ) as vo:
            self.add(bp_tag())
            self.play(FadeIn(A), FadeIn(labs))
            vo.wait_until("a")
            self.play(Create(yl), FadeIn(yd), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(fl), FadeIn(fd), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(train), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def three(self):
        d = load("ppi")
        c, nv, pp = d["classical"], d["naive"], d["ppi"]
        xmin, xmax = 119.0, 127.0
        A = axes([xmin, xmax], [0, 4], x_length=7.4, y_length=3.6, xlabel=r"mean systolic pressure (mm Hg)", ylabel=r"",
                 xticks=[120, 122, 124, 126], yticks=[], center=[1.6, 0.6, 0])
        ax = A.ax
        tr = DashedLine(ax.c2p(d["truth"], 0), ax.c2p(d["truth"], 4), color=TRUEC, stroke_width=3)
        r1 = ci_row(ax, 3.2, c["est"], c["lo"], c["hi"], LABC, xmin, xmax)
        r2 = ci_row(ax, 2.0, nv["est"], nv["lo"], nv["hi"], GUESSC, xmin, xmax)
        r3 = ci_row(ax, 0.8, pp["est"], pp["lo"], pp["hi"], BANDC, xmin, xmax)
        names = VGroup(label(r"classical: \ 300 visits", font_size=20, color=LABC).next_to(ax.c2p(xmin, 3.2), LEFT, buff=0.2),
                       label(r"naive: \ 20,000 guesses", font_size=20, color=GUESSC).next_to(ax.c2p(xmin, 2.0), LEFT, buff=0.2),
                       label(r"prediction-powered", font_size=20, color=BANDC).next_to(ax.c2p(xmin, 0.8), LEFT, buff=0.2))
        foot = fit_rows(VGroup(
            label(rf"truth {d['truth']:.1f}; \ classical [{c['lo']:.1f}, {c['hi']:.1f}]; \ naive [{nv['lo']:.2f}, {nv['hi']:.2f}]; \ PPI [{pp['lo']:.1f}, {pp['hi']:.1f}]", font_size=22),
        ), 12.4, 0.3, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Three estimates, each with a ninety percent interval, from one draw of the labelled and "
            "unlabelled samples. The true island mean, which we know because this is the World, is the dashed line. "
            "<bookmark mark='b'/> The classical estimate uses the three hundred clinic visits alone. It is honest and "
            "wide. <bookmark mark='c'/> The naive estimate treats the twenty thousand guesses as if they were data. Its "
            "interval is tiny, and it is nowhere near the truth: it estimates the mean of the watch, not of the people. "
            "<bookmark mark='d'/> The prediction-powered estimate uses both, and is both honest and narrower than the "
            "classical one."
        ) as vo:
            self.add(bp_tag())
            self.play(FadeIn(A), Create(tr))
            vo.wait_until("b")
            self.play(FadeIn(r1), FadeIn(names[0]))
            vo.wait_until("c")
            self.play(FadeIn(r2), FadeIn(names[1]))
            vo.wait_until("d")
            self.play(FadeIn(r3), FadeIn(names[2]), FadeIn(foot))
        self.clear_scene()

    def ladder_(self):
        rows = [
            cmath(r"\theta", r"=", r"E f(X) - E\big[f(X) - Y\big]", font_size=32),
            cmath(r"\hat\theta^{PP}", r"=", r"\tfrac1N \textstyle\sum_{j} f(\tilde X_j) \ - \ \tfrac1n \sum_i \big(f(X_i) - Y_i\big)", font_size=30),
            cmath(r"E\,\hat\theta^{PP}", r"=", r"\theta \ \ \text{for any } f", font_size=32),
            cmath(r"\text{rectifier}", r":", r"\tfrac1n \textstyle\sum_i (f(X_i) - Y_i) \ \approx \ -2.8 \text{ here}", font_size=30),
        ]
        rows[1][-1].set_color(BANDC)
        whys = [why(r"add and subtract the guess"), why(r"guesses' mean, \ minus their bias on the labelled cases"),
                why(r"Angelopoulos, \ Bates, \ Fannjiang, \ Jordan \& Zrnic (2023)"), why(r"the watch's measured bias")]
        with self.voiceover(
            "<bookmark mark='a'/> The idea is one line of algebra. The mean of Y equals the mean of the guesses, minus "
            "the mean error of the guesses. <bookmark mark='b'/> Estimate the first term with the many unlabelled cases, "
            "and the second, the rectifier, with the few labelled ones, where we have both the guess and the truth. "
            "<bookmark mark='c'/> For a fixed prediction function, independent representative samples and finite moments, the mean estimator is unbiased even if the predictions are biased. That is Anastasios "
            "Angelopoulos, Stephen Bates, Clara Fannjiang, Michael Jordan and Tijana Zrnic's prediction-powered "
            "inference, published in Science in 2023. <bookmark mark='d'/> Here, the rectifier says the watch reads about "
            "three millimetres low on the labelled cases, and the estimate adds that back."
        ) as vo:
            intro=label('A representative labelled sample estimates prediction bias',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def variance(self):
        d = load("ppi")
        se = d["mean_se"]
        rows = [
            cmath(r"\mathrm{Var}\,\hat\theta^{PP}", r"=", r"\dfrac{\mathrm{Var} f(X)}{N} + \dfrac{\mathrm{Var}\big(Y - f(X)\big)}{n}", font_size=30),
            cmath(r"\text{classical}", r":", r"\mathrm{Var}(Y)/n", font_size=32),
            cmath(r"\text{better when}", r":", r"\mathrm{Var}(Y-f) + (n/N)\,\mathrm{Var}(f) < \mathrm{Var}(Y)", font_size=30),
            cmath(r"\text{here}", r":", rf"\mathrm{{se}}\ {se[3]:.2f} \text{{ vs }} {se[0]:.2f}: \ 300 \text{{ visits with PPI++ act like }} {d['n_equiv']:,.0f}", font_size=28),
        ]
        rows[3][-1].set_color(BANDC)
        whys = [why(r"two independent samples"), why(r"labels alone"), why(r"a good model has small residuals"),
                why(r"averaged over 300 draws")]
        with self.voiceover(
            "<bookmark mark='a'/> Its variance has two parts, one from each sample: the variance of the guesses over "
            "N, and the variance of the guesses' errors over n. <bookmark mark='b'/> The classical estimate's "
            "variance is the variance of Y over n. <bookmark mark='c'/> So plain prediction-powered inference wins "
            "when the residual variance plus n over N times the prediction variance is below the outcome variance. "
            "With enough unlabelled cases, that is approximately when the guesses' errors vary less than the truth "
            "itself, which is to say whenever the model explains some of the variation, even if it is biased. "
            "<bookmark mark='d'/> For the watch, the standard error falls from about one millimetre to about a half. "
            "Three hundred clinic visits, helped by twenty thousand biased guesses, are worth about "
            + f"{d['n_equiv']:,.0f}" + " visits alone."
        ) as vo:
            intro=label('Independent sample variances determine the precision gain',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def loose(self):
        d = load("ppi")
        b = d["bad_se"]
        rows = [
            cmath(r"\hat\theta_\lambda", r"=", r"\lambda\, \overline{f(\tilde X)} - \overline{\big(\lambda f(X) - Y\big)}", font_size=32),
            cmath(r"\hat\lambda", r"=", r"\dfrac{\mathrm{Cov}(Y, f)}{(1 + n/N)\, \mathrm{Var}(f)}", font_size=32),
            cmath(r"\text{a loose strap}", r":", rf"\mathrm{{se}} \ \text{{classical }} {b[0]:.2f}, \ \text{{PPI }} {b[1]:.2f}", font_size=30),
            cmath(r"\text{PPI++}", r":", rf"\hat\lambda \approx {d['bad_lam']:.2f}, \ \mathrm{{se}}\ {b[2]:.2f}", font_size=32),
        ]
        rows[3][-1].set_color(BANDC)
        whys = [why(r"unbiased for fixed $\lambda$; estimated weights need asymptotics"), why(r"the variance-minimizing weight"),
                why(r"guesses plus noise of SD 25"), why(r"Angelopoulos, \ Duchi \& Zrnic (2023)")]
        with self.voiceover(
            "<bookmark mark='a'/> What if the model is bad? Put a weight lambda on the guesses. The estimate stays "
            "unbiased for every fixed lambda; estimating lambda from the same data need not preserve exact unbiasedness, <bookmark mark='b'/> and the lambda that minimizes its variance is a regression "
            "coefficient of Y on the guesses, slightly shrunk. Angelopoulos, John Duchi and Zrnic call this PPI plus plus. "
            "<bookmark mark='c'/> Loosen the watch strap, so that each guess carries extra noise with a standard deviation "
            "of twenty-five. Plain prediction-powered inference, with lambda one, now has a standard error of "
            + say(b[1]) + ", worse than the " + say(b[0]) + " of the labels alone. <bookmark mark='d'/> PPI plus plus turns "
            "lambda down to about " + say(d["bad_lam"]) + ", and its standard error, " + say(b[2]) + ", is again a little "
            "better than the classical one. With lambda estimated, it is never worse than ignoring the guesses, up to "
            "terms that vanish with n."
        ) as vo:
            intro=label('Fixed-weight unbiasedness differs from estimated-weight asymptotics',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = board_rows("World blood pressure")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board, over a thousand draws of the clinic sample and the watch sample. The "
                   "classical interval: kept. <bookmark mark='b'/> The guesses treated as data: broken completely, never "
                   "covering the truth. <bookmark mark='c'/> Prediction-powered, and PPI plus plus: both kept, with "
                   "intervals about half as wide as the classical one.",
                   [("a", [0]), ("b", [1]), ("c", [2, 3])])

    def lineage(self):
        rows = fit_rows(VGroup(
            label(r"survey sampling knew this as the difference estimator", font_size=26, color=GREY_A),
            label(r"$\hat\theta = \bar f_{\text{population}} + \overline{(y - f)}_{\text{sample}}$: \ Part 18's model-assisted estimation", font_size=26),
            label(r"Cassel, \ S\"arndal \& Wretman (1976); \ Breidt \& Opsomer (2017): \ with machine learning", font_size=26, color=GREY_A),
            label(r"what is new: \ regression coefficients, \ quantiles, \ any M-estimand; \ power tuning", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Survey statisticians will recognize the estimator. <bookmark mark='b'/> With the "
            "population's guesses known and a random sample measured, it is the difference estimator, the simplest case "
            "of Part 18's model-assisted estimation: the population mean of the model, plus the sample mean of the "
            "residuals. <bookmark mark='c'/> Claes Cassel, Carl-Erik Särndal and Jan Wretman analysed it in 1976, and "
            "Jay Breidt and Jean Opsomer surveyed its use with machine-learning models in 2017. <bookmark mark='d'/> What "
            "the new work adds is generality, to regression coefficients, quantiles and any estimand defined by a convex "
            "loss, and the tuning of lambda; and, perhaps most of all, a reason for the many fields now flooded with "
            "machine-learning labels to use it."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def uses(self):
        rows = fit_rows(VGroup(
            label(r"the labelled cases must be a random sample of the same population", font_size=26, color=MISSC),
            label(r"the model must be trained on other data, \ or cross-fitted", font_size=26, color=MISSC),
            label(r"power tuning can protect asymptotic efficiency; plain PPI can hurt", font_size=26, color=BANDC),
            label(r"next: \ what do interpretation methods estimate?", font_size=26, color=CALC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two conditions carry the guarantee. The labelled cases must be a random sample from the "
            "same population as the unlabelled ones; if the clinic only sees the sick, no rectifier can save us. "
            "<bookmark mark='b'/> And the model must not have been trained on the labelled cases, or its errors there will "
            "look too small; with only one data set, cross-fitting does the job. <bookmark mark='c'/> With regularity conditions and asymptotically valid power tuning, a "
            "model can improve precision; plain PPI with weight one can increase variance. <bookmark mark='d'/> One last question about black "
            "boxes: when we ask one to explain itself, what are we estimating?"
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
