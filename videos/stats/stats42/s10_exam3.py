from __future__ import annotations

import numpy as np

from videos.stats.stats42.common import *  # noqa: F403

LTOP = 1.45


class ExamNonparametric(ExamMixin, VoiceoverScene):
    def construct(self):
        self.card()
        self.p7()
        self.p8()
        self.p9()

    def card(self):
        card = chapter_card(9, r"Exam III: \ smoothing, \ robustness, \ sparsity", r"Problems 7--9", part=PART)
        with self.voiceover("Chapter nine. Three problems from the middle of the master's: smoothing, robustness and sparsity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------------------------------ Problem 7
    def p7(self):
        d = load("p_kde")
        card = ExamCard(7, r"a KDE bandwidth", r"Part 29", [
            rf"Old Faithful's {d['n']} waiting times between eruptions have SD {d['s']:.2f} min and IQR {d['iqr']:.1f} min.",
            r"Compute Silverman's rule-of-thumb bandwidth for a Gaussian kernel density estimate.",
            rf"Least-squares cross-validation chooses $h = {d['h_cv']:.2f}$. \ Which would you use, \ and why do they differ?"],
            marks=8, color=S.ALT)
        self.pose_voiceover(
            f"Problem seven. Old Faithful's {d['n']} waiting times between eruptions have a standard deviation of "
            f"{say(d['s'], 2)} minutes and an interquartile range of twenty-four. Compute Silverman's rule-of-thumb "
            f"bandwidth for a Gaussian kernel density estimate. Least-squares cross-validation chooses "
            f"{say(d['h_cv'], 2)}. Which would you use, and why do the two differ? Pause and try it.", card)
        rows = [
            cmath(r"h", r"=", r"0.9 \, \min\big(s, \ \text{IQR}/1.349\big)\, n^{-1/5}", font_size=34),
            cmath(r"\phantom{h}", r"=", rf"0.9 \times \min({d['s']:.2f}, \ {d['iqr'] / 1.349:.2f}) \times {d['n']}^{{-1/5}}", font_size=32),
            cmath(r"\phantom{h}", r"=", rf"0.9 \times {d['a']:.2f} \times {d['n_fifth']:.4f} = {d['h_s']:.2f} \text{{ min}}", font_size=32),
            cmath(r"\text{LSCV}(h)", r"=", r"\textstyle\int \hat f_h^2 - \tfrac2n \sum_i \hat f_{h,-i}(x_i) \ \ \text{(expectation: expected ISE} - \int f^2)", font_size=28),
        ]
        rows[2][-1].set_color(S.ALT)
        whys = [why(r"Silverman (1986)"), why(r"robust scale"), why(r"the rule's answer"), why(r"Rudemo, \ Bowman")]
        with self.voiceover(
            f"<bookmark mark='a'/> Silverman's rule is nought point nine times the smaller of the standard deviation and the interquartile range over one point three four nine, times n to the minus a fifth. <bookmark mark='b'/> The interquartile range over one point three four nine is {say(d['iqr'] / 1.349, 2)}, so the standard deviation is the smaller. <bookmark mark='c'/> The rule gives {say(d['h_s'], 2)} minutes. <bookmark mark='d'/> Cross-validation instead minimizes an estimate whose expectation is expected integrated squared error minus the fixed integral of the true density squared, computed by leaving each point out, and it picks {say(d['h_cv'], 2)}: a third less smoothing."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=LTOP, x=-0.9, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not card])
        A = axes([35, 105], [0, 0.05], x_length=6.6, y_length=3.4, xlabel=r"minutes to the next eruption", ylabel=r"density",
                 xticks=[40, 60, 80, 100], yticks=[0, 0.025, 0.05], center=[-2.6, -1.0, 0])
        ax = A.ax
        h, e = d["hist"]
        h, e = np.asarray(h), np.asarray(e)
        bars = bars_at(ax, (e[:-1] + e[1:]) / 2, h, e[1] - e[0], GREY_D, opacity=0.8)
        g = np.asarray(d["grid"])
        fs = curve(ax, g, d["f_s"], S.ALT, 4)
        fc = curve(ax, g, d["f_cv"], S.ACCENT, 3)
        fb = curve(ax, g, d["f_big"], GREY_B, 3)
        side = fit_rows(VGroup(
            label(rf"Silverman: \ $h = {d['h_s']:.2f}$", font_size=24, color=S.ALT),
            label(rf"LSCV: \ $h = {d['h_cv']:.2f}$", font_size=24, color=S.ACCENT),
            label(rf"$3\times$ the rule: \ one mode lost", font_size=24, color=GREY_A),
            label(r"$0.9$: robust rule; normal-reference constant $1.06$", font_size=22, color=GREY_A),
            label(r"use LSCV, \ or Sheather--Jones; \ show both", font_size=24, color=GOODC),
        ), 4.6, 0.36, [4.45, -1.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the histogram, the rule's estimate in teal and cross-validation's in gold. "
            "<bookmark mark='b'/> Both find two modes, near fifty-five and eighty minutes, and cross-validation's are"
            " sharper. <bookmark mark='c'/> Triple the bandwidth and the shape is wrong. <bookmark mark='d'/> They "
            "differ because the point nine rule is a robust rule of thumb; the Gaussian normal-reference AMISE "
            "constant is about one point zero six. For these two well-separated modes, and a density with two "
            "well-separated modes has far more curvature than a normal with the same spread, so it needs less "
            "smoothing. <bookmark mark='e'/> Use cross-validation, or the Sheather–Jones plug-in of Part twenty-nine,"
            " and when the choice matters, show the reader both."
        ) as vo:
            self.play(FadeIn(A), FadeIn(bars), FadeIn(museum_tag(r"Old Faithful, \ August 1978--79")))
            vo.wait_until("a")
            self.play(Create(fs), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(fc), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(fb), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------------------------------ Problem 8
    def p8(self):
        d = load("p_if")
        card = ExamCard(8, r"an influence function", r"Part 30", [
            r"Derive the influence function of the variance functional $T(F) = \int (x - \mu_F)^2 \, dF(x)$.",
            r"Newcomb's 66 timings of light (1882) include one of $-44$ \ (deviations from 24,800 ns).",
            r"What does the influence function say about it? \ Compare the mean, \ the median and Huber's estimate."],
            marks=10, color=S.RESID)
        self.pose_voiceover(
            "Problem eight. Derive the influence function of the variance, written as a functional: the integral of x minus "
            "the mean, squared, against the distribution F. Simon Newcomb's sixty-six timings of light from 1882 include "
            "one value of minus forty-four. What does the influence function say about it? And compare the mean, the median "
            "and Huber's M-estimate of the centre. Pause and try it.", card)
        rows = [
            cmath(r"F_\varepsilon", r"=", r"(1 - \varepsilon) F + \varepsilon \delta_x, \ \ \mu_\varepsilon = \mu + \varepsilon (x - \mu)", font_size=32),
            cmath(r"T(F_\varepsilon)", r"=", r"(1 - \varepsilon) \textstyle\int (y - \mu_\varepsilon)^2 dF(y) + \varepsilon (x - \mu_\varepsilon)^2", font_size=30),
            cmath(r"\frac{d}{d\varepsilon} T(F_\varepsilon)\Big|_0", r"=", r"-\sigma^2 - 2(x - \mu) \textstyle\int (y - \mu)\, dF + (x - \mu)^2", font_size=28),
            cmath(r"\text{IF}(x)", r"=", r"(x - \mu)^2 - \sigma^2: \ \ \text{unbounded, \ growing like } x^2", font_size=32),
        ]
        rows[3][-1].set_color(S.RESID)
        whys = [why(r"contaminate at $x$"), why(r"the variance of the mixture"), why(r"the middle term is zero"), why(r"Hampel (1974)")]
        with self.voiceover(
            "<bookmark mark='a'/> Contaminate F with a little mass epsilon at the point x; the mean moves by epsilon times x "
            "minus mu. <bookmark mark='b'/> The variance of the mixture is one minus epsilon times the spread of F around "
            "the moved mean, plus epsilon times the new point's squared distance. <bookmark mark='c'/> Differentiate at "
            "epsilon equal to zero. The first term gives minus sigma squared; the cross term is zero, because deviations from "
            "the mean integrate to zero; the last gives x minus mu squared. <bookmark mark='d'/> So the influence function is x "
            "minus mu squared, minus sigma squared: unbounded, and growing like the square of the distance. One wild point "
            "can move the variance as far as it likes."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=LTOP, x=-0.9, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not card])
        g = np.asarray(d["grid"])
        A = axes([-60, 80], [-40, 60], x_length=6.6, y_length=3.4, xlabel=r"where one extra timing is added", ylabel=r"its effect $\times (n + 1)$",
                 xticks=[-40, 0, 40, 80], yticks=[-40, 0, 40], center=[-2.6, -1.0, 0])
        ax = A.ax
        cm = clip_curve(ax, g, d["sc"]["mean"], S.RESID, 4, ymin=-40, ymax=60)
        cmed = clip_curve(ax, g, d["sc"]["median"], S.CTRL, 4, ymin=-40, ymax=60)
        ch = clip_curve(ax, g, d["sc"]["huber"], GOODC, 4, ymin=-40, ymax=60)
        side = fit_rows(VGroup(
            label(rf"IF of the variance at $-44$: \ {d['if_var_at_out'][0]:,.0f}", font_size=22, color=S.RESID),
            label(rf"variance: \ {d['var']:.1f} with it, \ {d['var_clean']:.1f} without", font_size=22, color=S.RESID),
            label(rf"mean {d['mean']:.2f}: \ its curve is a line", font_size=22, color=S.RESID),
            label(rf"median {d['median']:.1f}: \ bounded, \ a step", font_size=22, color=S.CTRL),
            label(rf"Huber {d['huber']:.2f}: \ bounded, \ piecewise smooth", font_size=22, color=GOODC),
            label(r"the modern value: \ 33.0", font_size=22, color=EXACT),
        ), 4.6, 0.32, [4.45, -1.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> At Newcomb's minus forty-four, the variance's influence function is about {d['if_var_at_out'][0]:,.0f}. <bookmark mark='b'/> Divided by sixty-six, its first-order influence predicts roughly seventy-three variance units. The exact deletion effect differs because the mean and denominator also change: {say(d['var'], 1)} with it, {say(d['var_clean'], 1)} without. <bookmark mark='c'/> For the centre, here are the sensitivity curves: the effect of adding one more timing anywhere. The mean's is a straight line, unbounded, <bookmark mark='d'/> the median's a bounded step, <bookmark mark='e'/> and Huber's estimate is bounded and piecewise smooth. Its efficiency depends on the tuning, scale and population model. The mean is {say(d['mean'], 2)}, Huber's estimate {say(d['huber'], 2)}. <bookmark mark='f'/> The modern value of the speed of light corresponds to thirty-three: the bias in Newcomb's data was systematic, and robustness to extreme points alone cannot identify or correct a shared systematic offset."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Newcomb (1882), \ Stigler (1977)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cm), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cmed), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(ch), FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------------------------------ Problem 9
    def p9(self):
        d = load("p_kkt")
        bw = ", ".join(f"{v:.2f}" for v in d["bw"])
        card = ExamCard(9, r"a lasso KKT check", r"Part 32", [
            rf"The lasso $\tfrac{{1}}{{2n}}\|y - X\beta\|^2 + \lambda \|\beta\|_1$ on Stamey's prostate data \ ($n = {d['n']}$, \ 8 standardized predictors, \ $\lambda = {d['lam']}$).",
            rf"A colleague reports $\hat\beta = ({bw})$.",
            r"State the KKT conditions and check them. \ Is it the solution?"], marks=10, color=S.ACCENT)
        self.pose_voiceover(
            f"Problem nine. The lasso, with the squared error scaled by one over two n, is fitted to Stamey's prostate cancer "
            f"data: {d['n']} men in the training set, eight standardized predictors, and lambda equal to point one. A "
            f"colleague reports the coefficients on the card. State the Karush–Kuhn–Tucker conditions, check them, and say "
            f"whether this is the lasso solution. Pause and try it.", card)
        rows = [
            cmath(r"g_j", r"=", r"\tfrac1n x_j^\top (y - X\hat\beta)", font_size=34),
            cmath(r"\hat\beta_j \neq 0", r":", r"g_j = \lambda\, \text{sign}(\hat\beta_j)", font_size=32),
            cmath(r"\hat\beta_j = 0", r":", r"|g_j| \le \lambda", font_size=32),
            cmath(r"\text{colleague}", r":", rf"g_{{\text{{lcavol}}}} = {d['grad_w'][0]:.3f} \neq 0.1; \ \ \max_{{\text{{on}}}} |g_j - \lambda s_j| = {d['on_err_w']:.3f}", font_size=30),
        ]
        rows[3][-1].set_color(S.RESID)
        whys = [why(r"the correlation with the residual"), why(r"the subgradient of $|\beta_j|$"), why(r"inside $[-\lambda, \lambda]$"), why(r"it fails")]
        with self.voiceover(
            f"<bookmark mark='a'/> Let g j be each predictor's inner product with the residual, over n. <bookmark "
            f"mark='b'/> At the lasso solution, every predictor in the model has g j equal to lambda times the sign of its "
            f"coefficient: the subgradient of the absolute value. <bookmark mark='c'/> Every predictor out of the model has "
            f"g j between minus lambda and lambda. <bookmark mark='d'/> For the colleague's answer, log cancer volume has g "
            f"of {say(d['grad_w'][0], 3)}, not point one, and the worst violation among the nonzero coefficients is "
            f"{say(d['on_err_w'], 3)}. It is not the solution. It is the least squares fit soft-thresholded once, which would be "
            f"right only if the predictors were uncorrelated, and here two of them correlate at {say(d['corr_max'], 2)}."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=LTOP, x=-0.9, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not card])
        names = d["names"]
        gmax = max(0.2, float(np.ceil(np.max(np.abs(d["grad_w"]))*10)/10))
        A = axes([0, 8], [0, gmax], x_length=6.6, y_length=3.2, ylabel=r"$|g_j|$", xticks=[], yticks=[0, 0.1, 0.2], center=[-2.6, -0.9, 0])
        ax = A.ax
        lam = DashedLine(ax.c2p(0, 0.1), ax.c2p(8, 0.1), color=S.ACCENT, stroke_width=2.5)
        laml = label(r"$\lambda$", font_size=24, color=S.ACCENT).next_to(ax.c2p(8, 0.1), RIGHT, buff=0.1)
        gw, gc = np.abs(np.asarray(d["grad_w"])), np.abs(np.asarray(d["grad"]))
        b_w = bars_at(ax, np.arange(8) + 0.3, gw, 0.36, S.RESID, opacity=0.8)
        b_c = bars_at(ax, np.arange(8) + 0.7, gc, 0.36, GOODC, opacity=0.85)
        on = np.asarray(d["b"]) != 0
        nm = VGroup(*[label(n, font_size=16, color=GREY_A if not on[j] else WHITE).rotate(0.6).next_to(ax.c2p(j + 0.5, 0), DOWN, buff=0.25)
                      for j, n in enumerate(names)])
        sel = ", ".join(n for n, o in zip(names, on) if o)
        side = fit_rows(VGroup(
            label(r"red: \ the colleague's $|g_j|$", font_size=22, color=S.RESID),
            label(r"green: \ coordinate descent's", font_size=22, color=GOODC),
            label(rf"in the model ($|g_j| = \lambda$): \ {sel}", font_size=20, color=GOODC),
            label(rf"out of it: \ max $|g_j| = {d['off_max']:.3f} < 0.1$", font_size=22, color=GOODC),
            label(r"signed KKT conditions certify numerical optimality to tolerance", font_size=22, color=GREY_A),
        ), 4.6, 0.36, [4.45, -1.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> In red, the colleague's g values against the line at lambda: some nonzero coefficients sit above it, some below, and none exactly on it. <bookmark mark='b'/> In green, coordinate descent's answer. <bookmark mark='c'/> Every predictor in its model satisfies the signed KKT equality to numerical tolerance: {sel}. <bookmark mark='d'/> Every predictor left out sits below it, the largest at {say(d['off_max'], 3)}. <bookmark mark='e'/> Because the lasso is convex, these conditions are not just necessary but sufficient: passing their signed conditions to solver tolerance certifies numerical optimality to that tolerance. A KKT check is the cheapest proof in statistics, and an examiner's favourite."
        ) as vo:
            self.play(FadeIn(A), FadeIn(lam), FadeIn(laml), FadeIn(nm), FadeIn(museum_tag(r"Stamey et al. (1989): \ prostate cancer")))
            vo.wait_until("a")
            self.play(FadeIn(b_w), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(b_c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
