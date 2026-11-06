from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load, predict, show_card

DML_CODE = [
    "# condensed from econ.dml_plr: cross-fitted",
    "fold = rng.permutation(n) % 5",
    "for k in range(5):",
    "    tr, te = fold != k, fold == k",
    "    ry[te] = y[te] - ridge_fit_predict(X[tr], y[tr], X[te])",
    "    rd[te] = d[te] - ridge_fit_predict(X[tr], d[tr], X[te])",
    "theta = rd @ ry / (rd @ rd)               # residual on residual",
    "psi = (ry - theta * rd) * rd",
    "se = sqrt(mean(psi**2) / mean(rd**2)**2 / n)",
]


class DML(VoiceoverScene):
    def construct(self):
        dm = load("dml_demo")
        d = load("dml")
        lam = load("dml_lambda")
        self.card()
        self.slide(dm)
        self.derive()
        self.lab(d)
        self.penalty(lam)

    def card(self):
        c = chapter_card(15, r"Double machine learning", r"How do you let a flexible model control for confounders?",
                         part=PART)
        with self.voiceover("Chapter fifteen. Double machine learning."):
            show_card(self, c)
        self.play(FadeOut(c))

    def slide(self, dm):
        d, y, x1, rd, ry = (np.asarray(dm[k]) for k in ("d", "y", "x1", "rd", "ry"))
        fold = np.asarray(dm["fold"])
        g = axes([-5.5, 5.5], [-5, 10], x_length=6.2, y_length=5.0, xlabel=r"treatment $d$", ylabel=r"outcome $y$",
                 xticks=[-5, 0, 5], yticks=[-5, 0, 5, 10], font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        cmap = lambda v: interpolate_color(ManimColor(DATA_C), ManimColor(ALT), (v + 2) / 4)  # noqa: E731
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.03, color=cmap(c_))
                        for a, b, c_ in zip(d, y, x1)])
        xs = np.array([-3.8, 3.8])
        raw = Line(ax.c2p(xs[0], y.mean() + dm["slope_raw"] * (xs[0] - d.mean())),
                   ax.c2p(xs[1], y.mean() + dm["slope_raw"] * (xs[1] - d.mean())), color=BAD, stroke_width=3)
        res = Line(ax.c2p(xs[0], dm["slope_res"] * xs[0]), ax.c2p(xs[1], dm["slope_res"] * xs[1]), color=GOOD,
                   stroke_width=4)
        fcols = [DATA_C, ALT, EST, GOOD, QC.Q]
        side = VGroup(
            MathTex(r"y = \theta\,d + g(X) + \varepsilon,\quad d = m(X) + v", font_size=30),
            label(r"simulated: $\theta = 0.3$; $g$, $m$ nonlinear in $X$; colour: $X_1$", font_size=19, color=GREY_B),
            MathTex(rf"\text{{slope of }} y \text{{ on }} d: {dm['slope_raw']:.2f}", font_size=28, color=BAD),
            MathTex(rf"\text{{residual on residual: }} {dm['slope_res']:.2f}", font_size=28, color=GOOD),
            label(r"each point's $\hat m$, $\hat\ell$ learned on the other four folds", font_size=19, color=GREY_A),
            wrapped_label(r"Causal interpretation assumes no unobserved confounding and a valid partially linear model.",
                          5.2, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Machine learning enters causal inference through a careful door. A treatment d moves an outcome y by "
            "theta, but many controls X drive both. A causal interpretation still assumes no unobserved confounding "
            "and a valid partially linear model; cross-fitting does not establish those assumptions. A simulated sample with a planted theta of zero point three, "
            f"coloured by the first control. <bookmark mark='a'/> The raw slope is {dm['slope_raw']:.2f}, "
            f"{dm['slope_raw'] / 0.3:.0f} times too large. <bookmark mark='b'/> Chernozhukov and coauthors' double machine "
            "learning, from 2018, learns the outcome given the controls and the treatment given the controls, and "
            "subtracts both: every point slides into a residual cloud. <bookmark mark='c'/> Residual on residual: "
            f"{dm['slope_res']:.2f}. <bookmark mark='d'/> And each point's predictions come from models fitted on the other "
            "folds."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[5]), LaggedStart(*[FadeIn(p) for p in dots],
                                                                              lag_ratio=0.002, run_time=2))
            vo.wait_until("a")
            self.play(Create(raw), FadeIn(side[2]))
            vo.wait_until("b")
            residual_x = label(r"residual treatment $d - \hat m(X)$", font_size=18, color=GREY_A).move_to(g.xlabel)
            residual_y = label(r"residual outcome $y - \hat\ell(X)$", font_size=18, color=GREY_A)
            residual_y.next_to(ax, UP, buff=0.18).align_to(ax, LEFT)
            self.play(FadeOut(raw), Transform(g.xlabel, residual_x), Transform(g.ylabel, residual_y),
                      *[p.animate.move_to(ax.c2p(a, b)) for p, a, b in zip(dots, rd, ry)], run_time=3)
            vo.wait_until("c")
            self.play(Create(res), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(*[p.animate.set_color(fcols[f_]) for p, f_ in zip(dots, fold)], FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        C_ = {r"\psi": EST, r"\eta": ALT}
        rows = [cmath(r"\psi(W; \theta, \eta)", r"=", r"\big(y - \ell(X) - \theta(d - m(X))\big)\big(d - m(X)\big)",
                      font_size=34, colors=C_),
                cmath(r"\partial_\eta\, \mathbb{E}[\psi(W; \theta_0, \eta)]\big|_{\eta_0}", r"=", r"0", font_size=36,
                      colors=C_),
                cmath(r"\sqrt n(\hat\theta - \theta_0)", r"=", r"Z_n + R_n + o_p(1)", font_size=36, colors=C_),
                cmath(r"R_n", r"=", r"O_p\big(\sqrt n\,a_n(a_n+b_n)\big)", font_size=36, colors=C_),
                cmath(r"\text{plug-in:}\ \ \hat\theta", r"=", r"\frac{\sum d\,(y - \hat g(X))}{\sum d^2}"
                      r"\ \Rightarrow\ \text{error} \propto \|\hat g - g\|", font_size=34, colors=C_)]
        whys = [why(r"the residual-on-residual score; $\ell = \mathbb{E}[y \mid X]$, $m = \mathbb{E}[d \mid X]$ are the "
                    r"nuisances $\eta$"),
                why(r"Neyman orthogonality: a small error in either nuisance does not move the score's mean, to first "
                    r"order"),
                why(r"$Z_n=n^{-1/2}\sum_i\psi(W_i;\theta_0,\eta_0)/\mathbb E[v^2]$: the score's CLT term"),
                why(r"$a_n=\|\hat m-m\|$, $b_n=\|\hat\ell-\ell\|$; require $a_n(a_n+b_n)=o_p(n^{-1/2})$ and regularity."),
                why(r"the naive plug-in is not orthogonal: regularisation bias in $\hat g$ passes straight into "
                    r"$\hat\theta$")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.6, buff=0.65, edge=6.8)
        with self.voiceover(
            "Why residualise both? The estimate solves the residual-on-residual score: residual outcome minus theta "
            "times residual treatment, times residual treatment, averaging zero. <bookmark mark='a'/> That score is "
            "Neyman-orthogonal: differentiate its mean with respect to the two learned functions, at the truth, and you "
            "get zero. Small errors in the learned functions do not move it, to first order. <bookmark mark='b'/> So the "
            "error is the usual normal term plus a second-order remainder: the treatment-model error times the sum "
            "of the outcome-model and treatment-model errors. "
            "Machine learners converge slowly, but if each is faster than n to the minus a quarter, the product vanishes "
            "faster than the root-n noise. Valid inference also needs identification, suitable moments and sampling "
            "conditions; this iid score standard error does not handle arbitrary time dependence. <bookmark mark='c'/> The "
            "naive plug-in, learn g and regress what is left on d, is not orthogonal: its derivative with respect to g "
            "is the covariance of d with the controls, not zero, so regularisation bias in g passes straight into theta. "
            "Cross-fitting handles the other danger: a learner that has memorised a point makes that point's residual "
            "artificially small."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            step(3)
            vo.wait_until("c")
            step(4)
        self.wait(0.5)
        self.clear_scene()

    def lab(self, d):
        card = lab_card(r"double ML in the House", DML_CODE, source="explainer/quant/house/econ.py (condensed)",
                        width=8.6, font_size=18).to_corner(UL, buff=0.35)
        outs = [f"dml_plr over 60 samples of 4,000:  theta = {d['dml_mean']:.3f} +/- {d['dml_sd']:.3f}",
                f"OLS with linear controls:          {d['naive_mean']:.2f}"]
        with self.voiceover(
            "The House's version: five folds; ridge on spline features, fitted on four, residualise the fifth; then "
            "residual on residual, with the score's standard error. <bookmark mark='a'/> Over sixty samples: "
            f"{d['dml_mean']:.3f}, spread {d['dml_sd']:.3f}; least squares with linear controls, {d['naive_mean']:.2f}."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=1.8)
        self.wait(0.4)
        self.clear_scene()

    def penalty(self, lam):
        L = np.log10(np.asarray(lam["lams"]))
        dm, pl = np.asarray(lam["dml"]), np.asarray(lam["plugin"])
        mm, ml = np.asarray(lam["mse_m"]), np.asarray(lam["mse_l"])
        g1 = axes([L[0], L[-1]], [0.2, 1.2], x_length=6.0, y_length=3.2, xlabel=r"ridge penalty $\lambda$ (log scale)",
                  ylabel=r"$\hat\theta$, 5 seeds", xticks=[-2, 0, 2, 4], xfmt=lambda v: f"10^{{{int(v)}}}",
                  yticks=[0.3, 0.6, 0.9, 1.2], font_size=15).to_edge(LEFT, buff=0.6).shift(DOWN * 0.6)
        g2 = axes([L[0], L[-1]], [0.9, 4.6], x_length=4.6, y_length=2.6, xlabel=r"$\lambda$ (log scale)",
                  ylabel=r"out-of-fold error of the learners", xticks=[-2, 0, 2, 4], xfmt=lambda v: f"10^{{{int(v)}}}",
                  yticks=[1, 2, 3, 4], font_size=14).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.6)
        a1, a2 = g1.ax, g2.ax
        truth = DashedLine(a1.c2p(L[0], 0.3), a1.c2p(L[-1], 0.3), color=WHITE, stroke_width=2)
        k = ValueTracker(1)

        def draw():
            j = int(min(max(k.get_value(), 1), len(L) - 1)) + 1
            return VGroup(seed_band(a1, L[:j], np.minimum(pl[:, :j], 1.2), BAD),
                          seed_band(a1, L[:j], np.minimum(dm[:, :j], 1.2), GOOD),
                          seed_band(a2, L[:j], np.minimum(ml[:, :j], 4.6), ALT, stroke_width=2.5),
                          seed_band(a2, L[:j], np.minimum(mm[:, :j], 4.6), EST, stroke_width=2.5))
        dr = always_redraw(draw)
        leg1 = legend([(BAD, r"naive plug-in"), (GOOD, r"double ML"), (WHITE, r"truth")], font_size=17).next_to(
            g1, UP, buff=0.15).align_to(g1, LEFT)
        leg2 = legend([(ALT, r"$\hat\ell$: $y$ on $X$"), (EST, r"$\hat m$: $d$ on $X$")], font_size=17).next_to(
            g2, UP, buff=0.15).align_to(g2, LEFT)
        i1 = int(np.argmin(np.abs(L - 0)))
        i3 = int(np.argmin(np.abs(L - 1)))
        q = predict(r"If $\hat m$ is perfect but $\hat\ell$ is poor, is $\hat\theta$ still fine?", width=7.0)
        q.to_corner(UR, buff=0.3)
        with self.voiceover(
            "Now train the learners at every ridge penalty, five seeds each. <bookmark mark='a'/> On the right, their "
            "out-of-fold errors, rising once the penalty flattens the fits. On the left, theta. At a penalty of one, "
            f"double ML gives {dm[:, i1].mean():.3f} and the plug-in {pl[:, i1].mean():.3f}; at ten, {dm[:, i3].mean():.3f} "
            f"against {pl[:, i3].mean():.3f}. The plug-in drifts as soon as its learner is biased; double ML holds longer. "
            "<bookmark mark='b'/> At extreme penalties both fail: the product of two bad errors is not small. Robustness, "
            "not immunity. <bookmark mark='c'/> Pause and predict: a perfect treatment model and a poor outcome model. "
            "Is theta fine? Yes, to first order."
            " All of this assumes enough data. Next: how much is enough."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(truth), FadeIn(leg1), FadeIn(leg2))
            self.add(dr)
            vo.wait_until("a")
            self.play(k.animate.set_value(len(L) - 1), run_time=vo.until("b"), rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(q))
        dr.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
