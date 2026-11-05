from __future__ import annotations

import numpy as np

from videos.stats.stats21.common import *  # noqa: F403


class Proximal(VoiceoverScene):
    def construct(self):
        self.card()
        self.operator()
        self.thresholds()
        self.ista()
        self.rates()
        self.momentum()
        self.zoo()

    def card(self):
        card = chapter_card(8, r"Proximal methods", r"A gradient step, \ then a cleanup", lit=(2009,), part=PART)
        with self.voiceover("Chapter eight. Proximal methods."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def operator(self):
        rows = [
            cmath(r"\operatorname{prox}_{t g}(v)", r"=", r"\arg\min_x \ g(x) + \tfrac{1}{2t}\|x - v\|^2", font_size=30),
            cmath(r"g = \lambda\|\cdot\|_1", r":", r"\operatorname{prox} = S_{t\lambda}(v), \ \text{soft thresholding}", font_size=30),
            cmath(r"g = \text{indicator of } C", r":", r"\operatorname{prox} = \text{projection onto } C", font_size=30),
            cmath(r"g = 0", r":", r"\operatorname{prox} = v", font_size=30),
        ]
        rows[1][2].set_color(PATH)
        whys = [why(r"stay near $v$, \ but make $g$ small"), why(r"each coordinate on its own"),
                why(r"constraints are a special case"), why(r"nothing to clean up")]
        with self.voiceover(
            "Many penalties are simple even when they're not smooth. <bookmark mark='a'/> The proximal operator of a function "
            "g, at a point v, finds the point that keeps g small without straying far from v. <bookmark mark='b'/> For the "
            "lasso penalty it's soft thresholding, coordinate by coordinate. <bookmark mark='c'/> For a constraint, the "
            "indicator function of a set, it's projection onto the set. <bookmark mark='d'/> And with no penalty, it does "
            "nothing."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def thresholds(self):
        A = axes([-3, 3], [-3, 3], x_length=5.4, y_length=5.0, xlabel=r"input $v$", ylabel=r"output", xticks=[-3, -1, 0, 1, 3],
                 yticks=[-3, -1, 0, 1, 3], center=[-3.0, 0.0, 0], font_size=18)
        ax = A.ax
        v = np.linspace(-3, 3, 301)
        soft = polyline(ax, v, np.sign(v) * np.maximum(np.abs(v) - 1, 0), PATH, 4)
        hard = polyline(ax, v, np.where(np.abs(v) > 1, v, 0), RES, 2.5)
        diag = DashedLine(ax.c2p(-3, -3), ax.c2p(3, 3), color=GREY_D, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(r"gold: \ soft thresholding, \ the prox of $|x|$ ($t\lambda = 1$)", font_size=22, color=PATH),
            label(r"red: \ hard thresholding, \ keep or kill", font_size=22, color=RES),
            label(r"soft: \ continuous, \ shrinks survivors by 1", font_size=22),
            label(r"hard: \ the prox of a count of non-zeros, \ $\|x\|_0$", font_size=22),
            label(r"$\ell_0$ is not convex: \ best-subset selection is hard (Part 32)", font_size=20, color=GREY_A),
        ), 5.6, 0.42, [3.6, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the lasso's proximal operator as a picture. Soft thresholding sets anything within one "
            "threshold of zero to zero, and moves everything else toward zero by the threshold. <bookmark mark='b'/> Compare "
            "hard thresholding, which keeps a value untouched if it's big enough and kills it otherwise. "
            "<bookmark mark='c'/> Soft thresholding is continuous: a small change in the data never makes a coefficient jump. "
            "<bookmark mark='d'/> Hard thresholding is the proximal operator of the count of non-zero coefficients, the penalty "
            "behind best-subset selection. <bookmark mark='e'/> That penalty isn't convex, which is why best-subset selection is "
            "computationally hard and the lasso is its convex stand-in, a story Part 32 continues."
        ) as vo:
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(Create(soft), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(hard), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def ista(self):
        rows = [
            cmath(r"\min_\beta", r"", r"f(\beta) + g(\beta), \ \ f \text{ smooth}, \ g \text{ simple}", font_size=30),
            cmath(r"\beta_{k+1}", r"=", r"\operatorname{prox}_{g/L}\big(\beta_k - \tfrac1L \nabla f(\beta_k)\big)", font_size=30),
            cmath(r"\text{lasso}", r":", r"\beta_{k+1} = S_{\lambda/L}\big(\beta_k + \tfrac{1}{nL} X'(y - X\beta_k)\big)", font_size=30),
            cmath(r"F(\beta_k) - F^*", r"\le", r"\frac{L\|\beta_0 - \beta^*\|^2}{2k}", font_size=30),
        ]
        rows[2][2].set_color(GRAD)
        whys = [why(r"smooth loss $+$ simple penalty"), why(r"a gradient step on $f$, \ then the prox of $g$"),
                why(r"ISTA: \ iterative soft thresholding"), why(r"$L$: \ the curvature bound of $f$")]
        with self.voiceover(
            "<bookmark mark='a'/> Most penalized estimators are a smooth loss f plus a simple penalty g. <bookmark mark='b'/> "
            "The proximal gradient method takes a gradient step on the smooth part, with step one over L, where L bounds its "
            "curvature, then applies the penalty's proximal operator. <bookmark mark='c'/> For the lasso that's a gradient step "
            "on the least-squares loss followed by soft thresholding: ISTA, the iterative shrinkage-thresholding algorithm. "
            "<bookmark mark='d'/> Its objective error is guaranteed to shrink like one over k: a factor of ten more accuracy "
            "costs ten times as many steps."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rates(self):
        d = load("prox")
        K = d["K"]
        k = np.arange(1, K + 1)
        lk = np.log10(k)
        A = axes([0, np.log10(K)], [-6, 2], x_length=8.4, y_length=4.6, xlabel=r"iteration $k$ \ (log scale)",
                 ylabel=r"$F(\beta_k) - F^*$ \ (log$_{10}$)", xticks=[0, 1, 2, np.log10(400)], yticks=[-6, -4, -2, 0, 2],
                 center=[-1.4, 0.3, 0], xfmt=lambda v: f"{10 ** v:.0f}")
        ax = A.ax
        clip = lambda v: np.clip(np.log10(np.maximum(np.asarray(v), 1e-7)), -6, 2)  # noqa: E731
        li = polyline(ax, lk, clip(d["ista"]), GRAD, 3.5)
        lf = polyline(ax, lk, clip(d["fista"]), FAST, 3.5)
        bi = DashedLine(ax.c2p(0, clip(d["bound_ista"])[0]), ax.c2p(np.log10(K), clip(d["bound_ista"])[-1]), color=GRAD, stroke_width=2)
        bf = DashedLine(ax.c2p(0, clip(d["bound_fista"])[0]), ax.c2p(np.log10(K), clip(d["bound_fista"])[-1]), color=FAST, stroke_width=2)
        rows = fit_rows(VGroup(
            label(rf"a lasso with {d['p']} correlated predictors, \ $n = {d['n']}$", font_size=22),
            label(rf"condition number of $X'X/n$: \ {d['cond']:,.0f}", font_size=22, color=GREY_A),
            label(r"red: \ ISTA; \ dashed: \ its bound $\propto 1/k$", font_size=22, color=GRAD),
            label(r"green: \ FISTA; \ dashed: \ $\propto 1/k^2$", font_size=22, color=FAST),
            label(r"after 400 steps: \ $10^{-1.7}$ vs $10^{-4.8}$", font_size=22, color=TRUE),
            label(r"FISTA is not monotone: \ momentum overshoots", font_size=20, color=GREY_A),
        ), 3.45, 0.4, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's ISTA on a hard lasso: forty predictors, all strongly correlated, so the problem is "
            "badly conditioned. <bookmark mark='b'/> The objective error on a log scale against the iteration on a log scale: "
            "ISTA, in red, crawls, staying under its one-over-k bound. <bookmark mark='c'/> In green, FISTA: the same steps "
            "with momentum, from Amir Beck and Marc Teboulle in 2009. Its bound falls like one over k squared, and after four "
            "hundred steps it's three orders of magnitude closer than ISTA. <bookmark mark='d'/> It's not monotone: the "
            "momentum sometimes overshoots, and the error ripples, but the trend is what the theorem promises."
        ) as vo:
            self.play(FadeIn(A), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(li), Create(bi), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(lf), Create(bf), FadeIn(rows[3]), FadeIn(rows[4]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def momentum(self):
        rows = [
            cmath(r"z_k", r"=", r"\beta_k + \frac{t_{k-1} - 1}{t_k}(\beta_k - \beta_{k-1})", font_size=30),
            cmath(r"\beta_{k+1}", r"=", r"\operatorname{prox}_{g/L}\big(z_k - \tfrac1L\nabla f(z_k)\big)", font_size=30),
            cmath(r"t_{k+1}", r"=", r"\tfrac12\big(1 + \sqrt{1 + 4t_k^2}\big)", font_size=30),
            cmath(r"\text{rate}", r":", r"O(1/k^2), \ \text{the best any first-order method can do}", font_size=28),
        ]
        rows[3][2].set_color(FAST)
        whys = [why(r"look ahead, \ along the last move"), why(r"the same proximal step, \ from there"),
                why(r"the momentum weight grows to 1"), why(r"Nesterov (1983): \ optimal")]
        with self.voiceover(
            "How does momentum help? <bookmark mark='a'/> Instead of stepping from the current point, FISTA first extrapolates "
            "along the direction it was already moving. <bookmark mark='b'/> Then it takes the usual proximal step from "
            "there. <bookmark mark='c'/> The extrapolation weight follows a specific sequence, rising toward one. "
            "<bookmark mark='d'/> Yurii Nesterov showed in 1983 that one over k squared is the best rate any method using only "
            "gradients can guarantee on smooth convex problems, so this simple trick is optimal."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def zoo(self):
        rows = fit_rows(VGroup(
            label(r"group lasso: \ shrink whole blocks, \ $\big(1 - t\lambda/\|v_G\|\big)_+ v_G$", font_size=24, color=PATH),
            label(r"nuclear norm: \ soft-threshold the singular values \ (matrix completion, \ Part 52)", font_size=24, color=NEWT),
            label(r"nonnegativity, \ simplex, \ box constraints: \ projections", font_size=24, color=TEAL),
            label(r"and the step size can be found by backtracking, \ with no $L$ known", font_size=22, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The same recipe covers a zoo of penalties. The group lasso shrinks whole blocks of "
            "coefficients together. <bookmark mark='b'/> The nuclear norm of a matrix, for low-rank problems like filling in a "
            "matrix of ratings, has a proximal operator that soft-thresholds the singular values. <bookmark mark='c'/> "
            "Constraints become projections. <bookmark mark='d'/> And when the curvature bound L isn't known, a backtracking "
            "search finds a safe step."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
