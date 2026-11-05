from __future__ import annotations

import numpy as np

from videos.stats.stats21.common import *  # noqa: F403


class Convexity(VoiceoverScene):
    def construct(self):
        self.card()
        self.definitions()
        self.picture()
        self.jensen()
        self.likelihoods()
        self.partition()
        self.conditioning()
        self.families()

    def card(self):
        card = chapter_card(1, r"Convex sets and functions", r"When local is global", part=PART)
        with self.voiceover("Chapter one. Convex sets and functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definitions(self):
        rows = [
            cmath(r"C \text{ convex}", r":", r"x, y \in C \Rightarrow t x + (1 - t) y \in C", font_size=30),
            cmath(r"f \text{ convex}", r":", r"f(t x + (1 - t) y) \le t f(x) + (1 - t) f(y)", font_size=30),
            cmath(r"\text{first order}", r":", r"f(y) \ge f(x) + \nabla f(x)'(y - x)", font_size=30),
            cmath(r"\text{second order}", r":", r"\nabla^2 f(x) \succeq 0", font_size=30),
            cmath(r"\text{strongly convex}", r":", r"\nabla^2 f(x) \succeq m I,\ m > 0", font_size=30),
        ]
        whys = [why(r"the segment stays inside"), why(r"the chord lies above the graph"), why(r"every tangent lies below"),
                why(r"curvature never negative"), why(r"curvature bounded away from zero: \ a unique minimum")]
        with self.voiceover(
            "<bookmark mark='a'/> A set is convex if the segment between any two of its points stays inside it: a disc, a "
            "polygon, a half-plane; not a crescent. <bookmark mark='b'/> A function is convex if its chord between any two "
            "points lies above its graph. <bookmark mark='c'/> Equivalently, for a smooth function, every tangent lies below the "
            "graph. <bookmark mark='d'/> Or, with two derivatives, the Hessian, the matrix of second derivatives, is positive "
            "semidefinite everywhere: the curvature is never negative in any direction. <bookmark mark='e'/> Strong convexity "
            "asks for curvature bounded away from zero, which guarantees a unique minimum and fast algorithms."
        ) as vo:
            step = ladder(self, rows, whys, keep=5, top=2.8, x=-0.6, buff=0.62, edge=6.9)
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        A = axes([-3, 3], [0, 4], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"$f(x)$", xticks=[-3, 0, 3],
                 yticks=[0, 2, 4], center=[-2.2, 0.2, 0])
        ax = A.ax
        f = lambda x: np.log1p(np.exp(x)) + 0.12 * x ** 2  # noqa: E731
        fp = lambda x: 1 / (1 + np.exp(-x)) + 0.24 * x  # noqa: E731
        xs = np.linspace(-3, 3, 200)
        g = curve(ax, xs, f(xs), FIT, 3.5)
        a, b = -2.4, 2.0
        chord = Line(ax.c2p(a, f(a)), ax.c2p(b, f(b)), color=PATH, stroke_width=3)
        ends = VGroup(Dot(ax.c2p(a, f(a)), color=PATH), Dot(ax.c2p(b, f(b)), color=PATH))
        x0 = 0.6
        tx = np.array([-3, 3.0])
        tan = Line(ax.c2p(-3, f(x0) + fp(x0) * (-3 - x0)), ax.c2p(3, f(x0) + fp(x0) * (3 - x0)), color=HIT, stroke_width=3)
        rows = fit_rows(VGroup(
            label(r"$f(x) = \log(1 + e^x) + 0.12x^2$", font_size=22, color=FIT),
            label(r"gold: \ a chord, \ always above", font_size=22, color=PATH),
            label(r"green: \ a tangent, \ always below", font_size=22, color=HIT),
            label(r"so a point with zero slope is the global minimum", font_size=22, color=TRUE),
        ), 4.6, 0.4, [4.0, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's a convex function, a smoothed hinge plus a little curvature, the kind of thing a "
            "logistic loss looks like. <bookmark mark='b'/> Any chord lies above it. <bookmark mark='c'/> Any tangent lies "
            "below it. <bookmark mark='d'/> And the tangent fact has the consequence that matters most for us: if the gradient "
            "is zero somewhere, the tangent there is flat, and the whole function lies above it. A stationary point of a "
            "convex function is its global minimum. No local traps."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(g), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(chord), FadeIn(ends), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(tan), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def jensen(self):
        rows = [
            cmath(r"\text{Jensen}", r":", r"f(E X) \le E f(X) \text{ for convex } f", font_size=30),
            cmath(r"f(x) = x^2", r":", r"(E X)^2 \le E X^2, \ \text{so} \ \mathrm{Var}\,X \ge 0", font_size=30),
            cmath(r"f(x) = -\log x", r":", r"E \log X \le \log E X", font_size=30),
            cmath(r"\text{so}", r":", r"E \log \frac{q(X)}{p(X)} \le \log E \frac{q(X)}{p(X)} = 0", font_size=30),
        ]
        rows[3][2].set_color(TRUE)
        whys = [why(r"the chord inequality, \ with many points"), why(r"Part 6"), why(r"the geometric mean $\le$ the arithmetic"),
                why(r"Gibbs: \ Kullback--Leibler $\ge 0$; \ why MLE works, \ Part 22")]
        with self.voiceover(
            "<bookmark mark='a'/> The chord inequality with many points, weighted by probabilities, is Jensen's inequality: "
            "f of the mean is at most the mean of f. <bookmark mark='b'/> With x squared it says a variance is never negative. "
            "<bookmark mark='c'/> With minus log it says the average of logs is at most the log of the average. "
            "<bookmark mark='d'/> And applied to a likelihood ratio, it says the expected log likelihood is highest at the "
            "true distribution: the Kullback–Leibler divergence is never negative. That one line is the reason maximum "
            "likelihood works, which Part 22 develops."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def likelihoods(self):
        d = load("convex")
        A = axes([-0.5, 1.5], [min(d["logistic"]), max(d["logistic"]) + 2], x_length=5.2, y_length=3.8, xlabel=r"slope $\beta$",
                 ylabel=r"log likelihood", xticks=[-0.5, 0, 0.5, 1, 1.5], center=[-3.4, 0.4, 0], font_size=18)
        B = axes([-6, 10], [min(d["cauchy"]), max(d["cauchy"]) + 1], x_length=5.2, y_length=3.8, xlabel=r"location $\theta$",
                 ylabel=r"log likelihood", xticks=[-6, -2, 2, 6, 10], center=[3.4, 0.4, 0], font_size=18)
        la = curve(A.ax, d["b"], d["logistic"], FIT, 3.5)
        lb = curve(B.ax, d["theta"], d["cauchy"], RES, 3.5)
        mx = Dot(A.ax.c2p(d["b_hat"], max(d["logistic"])), color=PATH)
        th = np.asarray(d["theta"])
        cy = np.asarray(d["cauchy"])
        peaks = VGroup(*[Dot(B.ax.c2p(t, float(np.interp(t, th, cy))), color=PATH) for t in d["local_max"]])
        data = VGroup(*[Line(B.ax.c2p(x, min(d["cauchy"])), B.ax.c2p(x, min(d["cauchy"]) + 0.6), color=GREY_B, stroke_width=2)
                        for x in d["x"]])
        ta = label(r"logistic regression: \ concave, \ one peak", font_size=22, color=FIT).next_to(A, UP, buff=0.2)
        tb = label(r"Cauchy location: \ two peaks", font_size=22, color=RES).next_to(B, UP, buff=0.2)
        foot = label(r"start an optimizer in the wrong valley and it finds the wrong peak", font_size=24, color=OBS).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> Statistics meets both kinds. On the left, the log likelihood of a logistic regression slope "
            "for the World's vote, eight hundred adults: concave, the negative of convex, with a single peak. "
            "<bookmark mark='b'/> On the right, the log likelihood for the centre of a Cauchy distribution, from seven "
            "observations in two clusters. It has two peaks, one near each cluster, with a valley between. "
            "<bookmark mark='c'/> An algorithm that only looks locally can climb the wrong one."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(Create(la), FadeIn(mx), FadeIn(ta))
            vo.wait_until("b")
            self.play(FadeIn(data), Create(lb), FadeIn(peaks), FadeIn(tb))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def partition(self):
        rows = [
            cmath(r"f(x \mid \theta)", r"=", r"h(x)\,\exp\{\theta\,T(x) - A(\theta)\}", font_size=30),
            cmath(r"A'(\theta)", r"=", r"E_\theta\, T(X), \ \ \ A''(\theta) = \mathrm{Var}_\theta\, T(X) \ge 0", font_size=30),
            cmath(r"\ell(\theta)", r"=", r"\theta \textstyle\sum_i T(x_i) - n A(\theta) + \text{const}", font_size=30),
            cmath(r"\ell'(\hat\theta) = 0", r"\iff", r"A'(\hat\theta) = \bar T: \ \text{match the mean}", font_size=30),
        ]
        rows[3][2].set_color(TRUE)
        whys = [why(r"an exponential family, \ natural parameter $\theta$"), why(r"differentiate under the integral: \ $A$ is convex"),
                why(r"linear minus convex: \ concave"), why(r"one peak, \ found by Newton in a few steps")]
        with self.voiceover(
            "Why are exponential families safe? <bookmark mark='a'/> Write the density as h of x times the exponential of "
            "theta times T of x, minus a normalizing function A of theta, the log-partition function. "
            "<bookmark mark='b'/> Differentiating the normalization shows that A's first derivative is the mean of T and its "
            "second derivative is the variance of T, which can't be negative: A is convex. <bookmark mark='c'/> The log "
            "likelihood is theta times the sum of the T's, which is linear, minus n times A, which is convex, so it's concave. "
            "<bookmark mark='d'/> Its single peak is where the model's mean of T matches the sample's: maximum likelihood, for "
            "these families, is the method of moments."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def conditioning(self):
        rows = [
            cmath(r"m I \preceq \nabla^2 f \preceq L I", r":", r"\kappa = L / m, \ \text{the condition number}", font_size=30),
            cmath(r"\text{gradient descent, \ step } 1/L", r":", r"f(x_k) - f^* \le (1 - 1/\kappa)^k \,(f(x_0) - f^*)", font_size=28),
            cmath(r"\kappa = 10", r":", r"\text{a digit every 22 steps; \ } \kappa = 10^4: \ 23{,}000 \text{ steps}", font_size=28),
            cmath(r"\text{remedies}", r":", r"\text{centre and scale the predictors; \ or use the curvature (Newton)}", font_size=28),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"the flattest and steepest curvatures"), why(r"a linear rate, \ set by $\kappa$"),
                why(r"$\ln 10 \cdot \kappa$ steps per digit"), why(r"chapter five shows both")]
        with self.voiceover(
            "Convexity says an algorithm can't get trapped; how fast it gets there depends on the shape of the bowl. "
            "<bookmark mark='a'/> If the curvature is everywhere between m and L, their ratio kappa is the condition number: one "
            "for a round bowl, huge for a long thin valley. <bookmark mark='b'/> Gradient descent with step one over L then "
            "shrinks the error by a factor of one minus one over kappa per step. <bookmark mark='c'/> With kappa ten, that's a "
            "correct digit every twenty-two steps; with kappa ten thousand, every twenty-three thousand. <bookmark mark='d'/> "
            "In statistics a large kappa usually comes from predictors on very different scales, or strongly correlated. "
            "Centring and scaling them rounds the bowl, and Newton's method, which uses the curvature itself, doesn't care "
            "about kappa at all. Chapter five shows both."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def families(self):
        rows = fit_rows(VGroup(
            label(r"concave log likelihoods: \ exponential families in their natural parameter", font_size=24, color=FIT),
            label(r"so: \ GLMs with the canonical link, \ logistic and Poisson regression (Part 14)", font_size=22, color=FIT),
            label(r"convex penalized losses: \ ridge, \ the lasso, \ quantile regression", font_size=24, color=HIT),
            label(r"not convex: \ mixtures, \ Cauchy, \ factor models, \ neural networks", font_size=24, color=RES),
            label(r"there: \ several starts, \ and humility", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Which statistical problems are convex? Exponential families, written in their natural "
            "parameter, have concave log likelihoods, because the log-partition function is convex. <bookmark mark='b'/> So "
            "generalized linear models with the canonical link, logistic and Poisson regression, are safe. "
            "<bookmark mark='c'/> So are ridge, the lasso and quantile regression. <bookmark mark='d'/> Mixtures, heavy-tailed "
            "location models, factor models and neural networks are not. <bookmark mark='e'/> For those we use several starting "
            "points, and some humility about whether we found the best answer."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
