from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats9.common import *  # noqa: F403


class Properties(VoiceoverScene):
    def construct(self):
        self.card()
        self.consistency()
        self.kl()
        self.normality()
        self.curvature()
        self.check()
        self.shapes()
        self.failures()

    def card(self):
        card = chapter_card(5, r"How good is the MLE?", r"Consistency, \ normality, \ and a standard error from curvature", part=PART)
        with self.voiceover("Chapter five. How good is the maximum likelihood estimator?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def consistency(self):
        g = np.random.Generator(np.random.PCG64(1949))
        lam0 = 0.7
        lams = np.linspace(0.2, 1.6, 200)
        A = axes([0.2, 1.6], [-1.6, -0.85], x_length=7.0, y_length=4.4, xlabel=r"$\lambda$",
                 ylabel=r"$\tfrac1n\,\ell(\lambda)$, \ Poisson, \ $\lambda_0 = 0.7$", xticks=[0.2, 0.7, 1.2, 1.6],
                 yticks=[-1.5, -1.2, -0.9], center=[-2.7, -0.4, 0])
        ax = A.ax
        x = g.poisson(lam0, 2000)
        cols = {10: S.PRIOR, 100: S.POST, 2000: LIK}
        cvs, pks = VGroup(), VGroup()
        for n, c in cols.items():
            xx = x[:n]
            ll = (xx.sum() * np.log(lams) - n * lams - np.sum([np.log(np.arange(1, v + 1)).sum() for v in xx])) / n
            cvs.add(clip_curve(ax, lams, ll, c, 2.8, ymin=-1.6, ymax=-0.85))
            lh = xx.mean()
            pks.add(Dot(ax.c2p(lh, (xx.sum() * np.log(lh) - n * lh - np.sum([np.log(np.arange(1, v + 1)).sum() for v in xx])) / n),
                        radius=0.07, color=c))
        el = lam0 * np.log(lams) - lams - np.sum(stats.poisson.pmf(np.arange(30), lam0) * np.array([np.log(np.arange(1, v + 1)).sum() for v in range(30)]))
        lim = DashedVMobject(clip_curve(ax, lams, el, WHITE, 2.5, ymin=-1.6, ymax=-0.85), num_dashes=50)
        tr = DashedLine(ax.c2p(lam0, -1.6), ax.c2p(lam0, -0.85), color=EXACT, stroke_width=2)
        leg = legend([(S.PRIOR, r"$n = 10$"), (S.POST, r"$n = 100$"), (LIK, r"$n = 2{,}000$"), (WHITE, r"$E_{\lambda_0}\log p_\lambda(X)$")],
                     font_size=22).move_to([4.6, 2.0, 0])
        rows = fit_rows(VGroup(
            label(r"$\tfrac1n\ell(\lambda)$ is an average: \ the law of large numbers", font_size=24),
            label(r"it converges to a fixed curve, \ whose peak is the truth", font_size=24, color=S.ACCENT),
        ), 4.6, 0.3, [4.4, -1.0, 0])
        tag = simulated_tag(r"simulated: \ one Poisson sequence", corner=DR)
        with self.voiceover(
            "Why should maximum likelihood work at all? <bookmark mark='a'/> Divide the log-likelihood by n. It becomes "
            "an average: the average, over the observations, of log p lambda of x. For ten Poisson observations, this "
            "curve is wobbly, and its peak can be far from the true rate, point seven. <bookmark mark='b'/> With a "
            "hundred, it's steadier. With two thousand, steadier still. <bookmark mark='c'/> By the law of large "
            "numbers, the whole curve converges to a fixed one: the expected log-density, averaged over the true "
            "distribution. <bookmark mark='d'/> And that limiting curve peaks exactly at the truth. If the curves "
            "converge, and the limit has a unique peak at the truth, the peaks converge too. That's consistency, and "
            "it's Abraham Wald's 1949 argument. Why does the limit peak at the truth? That's a theorem of its own."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag), Create(tr))
            vo.wait_until("a")
            self.play(Create(cvs[0]), FadeIn(pks[0]), FadeIn(leg[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cvs[1]), FadeIn(pks[1]), FadeIn(leg[1]))
            self.play(Create(cvs[2]), FadeIn(pks[2]), FadeIn(leg[2]))
            vo.wait_until("c")
            self.play(Create(lim), FadeIn(leg[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def kl(self):
        rows = [
            cmath(r"E_{\theta_0}\log p_\theta(X) - E_{\theta_0}\log p_{\theta_0}(X)", r"=", r"E_{\theta_0}\log\frac{p_\theta(X)}{p_{\theta_0}(X)}",
                  font_size=32),
            cmath(r"\vphantom{x}", r"\le", r"\log E_{\theta_0}\frac{p_\theta(X)}{p_{\theta_0}(X)}", font_size=32),
            cmath(r"\vphantom{x}", r"=", r"\log \int p_\theta(x)\,dx = \log 1 = 0", font_size=32),
            cmath(r"\mathrm{KL}(\theta_0 \,\|\, \theta)", r"=", r"E_{\theta_0}\log\frac{p_{\theta_0}(X)}{p_\theta(X)} \;\ge\; 0", font_size=32),
        ]
        rows[3][2].set_color(S.ACCENT)
        whys = [why(r"the gap between any $\theta$ and the truth"), why(r"Jensen: \ $\log$ is concave (Part 6)"),
                why(r"the ratio's mean is the total probability of $p_\theta$"),
                why(r"Kullback \& Leibler (1951): \ zero only if $p_\theta = p_{\theta_0}$")]
        foot = label(r"identifiability: \ different $\theta$ must give different distributions", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> Compare the expected log-density at any theta with the one at the truth, theta zero. "
            "The difference is the expected log of a ratio. <bookmark mark='b'/> The logarithm is concave, so by "
            "Jensen's inequality the average of the log is at most the log of the average. <bookmark mark='c'/> And "
            "the average of the ratio, under the truth, is just the total probability of p theta: one. The log of one "
            "is zero. <bookmark mark='d'/> So the gap is never positive. Turned around, the quantity is the "
            "Kullback–Leibler divergence, from information theory, and it is zero only when the two distributions "
            "agree. <bookmark mark='e'/> As long as different parameters give different distributions, which is called "
            "identifiability, the truth is the unique peak. Maximum likelihood is, in the limit, a search for the "
            "distribution closest to the truth in Kullback–Leibler divergence. Part 22 uses exactly this when the "
            "model is wrong."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def normality(self):
        rows = [
            cmath(r"0 = U(\hat\theta)", r"\approx", r"U(\theta_0) + (\hat\theta - \theta_0)\,U'(\theta_0)", font_size=34),
            cmath(r"\sqrt n\,(\hat\theta - \theta_0)", r"\approx", r"\frac{U(\theta_0)/\sqrt n}{-U'(\theta_0)/n}", font_size=34),
            cmath(r"\frac{U(\theta_0)}{\sqrt n} \to N\big(0, I(\theta_0)\big),", r"\quad", r"-\frac{U'(\theta_0)}{n} \to I(\theta_0)",
                  font_size=32),
            cmath(r"\sqrt n\,(\hat\theta - \theta_0)", r"\to", r"N\Big(0,\ \frac{1}{I(\theta_0)}\Big)", font_size=36),
        ]
        rows[3][2].set_color(LIK)
        whys = [why(r"Taylor-expand the score around the truth"), why(r"solve, \ and scale by $\sqrt n$"),
                why(r"CLT on the score's sum; \ LLN on its slope; \ $I$: \ ch.~9"), why(r"Slutsky (Part 6): \ the MLE is asymptotically normal")]
        with self.voiceover(
            "Next, how big is the error? The answer comes from the score. <bookmark mark='a'/> At the MLE, the score is "
            "zero. Expand it in a Taylor series around the true value: the score at the truth plus the distance times "
            "the score's slope. <bookmark mark='b'/> Solve for the distance and multiply by root n. "
            "<bookmark mark='c'/> The score is a sum of n independent pieces with mean zero, so the central limit "
            "theorem makes the numerator normal, with a variance we'll call the Fisher information. The slope is also a "
            "sum, so the law of large numbers sends the denominator to a constant, which, as chapter nine proves, is "
            "the same Fisher information. <bookmark mark='d'/> By Slutsky's theorem from Part 6, root n times the error "
            "is approximately normal, with variance one over the information. Fisher conjectured this in 1922; making "
            "it rigorous took until the 1940s, and Part 47 does it properly."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curvature(self):
        d = load("curvature")
        hk = d["hk"]
        lams = np.asarray(hk["lams"])
        lh, S_, n = hk["lam_hat"], hk["S"], hk["n"]
        J = S_ / lh ** 2
        A = axes([0.4, 1.0], [-6, 0.3], x_length=6.4, y_length=4.2, xlabel=r"$\lambda$, \ horse kicks",
                 ylabel=r"$\ell(\lambda) - \ell(\hat\lambda)$", xticks=[0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], yticks=[-6, -4, -2, 0],
                 center=[-2.8, -0.4, 0])
        ax = A.ax
        cv = clip_curve(ax, lams, hk["ll"], LIK, 3.5, ymin=-6)
        par = clip_curve(ax, lams, -0.5 * J * (lams - lh) ** 2, S.ACCENT, 2.5, ymin=-6)
        par = DashedVMobject(par, num_dashes=40)
        se = 1 / np.sqrt(J)
        lo, hi = lh - 1.96 * se, lh + 1.96 * se
        br = VGroup(Line(ax.c2p(lo, -1.92), ax.c2p(hi, -1.92), color=S.ACCENT, stroke_width=5),
                    Dot(ax.c2p(lo, -1.92), radius=0.06, color=S.ACCENT), Dot(ax.c2p(hi, -1.92), radius=0.06, color=S.ACCENT))
        rows = fit_rows(VGroup(
            MathTex(r"J(\hat\lambda) = -\ell''(\hat\lambda) = \frac{S}{\hat\lambda^2}", font_size=30),
            MathTex(rf"= \frac{{{S_}}}{{{lh:.2f}^2}} = {J:.1f}", font_size=30),
            MathTex(rf"\mathrm{{SE}}(\hat\lambda) = \frac{{1}}{{\sqrt{{J}}}} = {se:.4f}", font_size=30, color=S.ACCENT),
            MathTex(rf"\hat\lambda \pm 1.96\,\mathrm{{SE}} = [{lo:.3f},\ {hi:.3f}]", font_size=30, color=S.ACCENT),
            label(r"the observed information: \ how sharply the data's curve is bent", font_size=22, color=GREY_A),
        ), 5.4, 0.32, [4.0, 0.0, 0])
        with self.voiceover(
            "In practice we turn that into a standard error, using the curvature of the log-likelihood. "
            "<bookmark mark='a'/> Here again is the horse-kick log-likelihood. Near its peak, any smooth curve looks "
            "like a parabola, <bookmark mark='b'/> and the parabola that matches it, in orange, has curvature minus the "
            "second derivative at the peak. That's called the observed information. For the Poisson it's the total "
            "count over lambda hat squared: three hundred and twenty-eight. <bookmark mark='c'/> The standard error is "
            "one over its square root: point zero five five. A sharply bent likelihood means a small standard error. "
            "<bookmark mark='d'/> Plus or minus one point nine six standard errors gives an interval from point five "
            "zero to point seven two. And notice that the parabola's interval and the curve's interval, where it drops "
            "one point nine two, nearly agree. With two hundred observations, the likelihood is already almost "
            "perfectly quadratic."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A), Create(cv))
            vo.wait_until("b")
            self.play(Create(par), FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(br[0]), FadeIn(br[1:]), FadeIn(rows[3:]))
        self.clear_scene()

    def check(self):
        d = load("curvature")
        ns = ["20", "50", "200", "1000"]
        hdr = VGroup(*[label(t, font_size=26, color=GREY_A) for t in (r"$n$", r"simulated SD of $\hat\lambda$",
                                                                       r"$1/\sqrt{n I(\lambda)} = \sqrt{\lambda/n}$")])
        xs = [-4.4, -0.6, 3.8]
        for j, h in enumerate(hdr):
            h.move_to([xs[j], 1.9, 0])
        cells = VGroup()
        for i, n in enumerate(ns):
            y = 1.1 - 0.68 * i
            s_ = d["sims"][n]
            cells.add(VGroup(MathTex(n, font_size=32).move_to([xs[0], y, 0]), MathTex(f"{s_['sd']:.4f}", font_size=32, color=SIM).move_to([xs[1], y, 0]),
                             MathTex(f"{s_['bound']:.4f}", font_size=32, color=LIK).move_to([xs[2], y, 0])))
        foot = fit_rows(VGroup(
            label(r"for the Poisson, \ $\hat\lambda = \bar x$ and the formula is exact at every $n$", font_size=24, color=GREY_A),
            label(r"for most models it is only a large-sample approximation: \ next, \ how good", font_size=24, color=S.ACCENT),
        ), 12.6, 0.3, [0, -2.4, 0])
        tag = simulated_tag(r"simulated: \ 20,000 samples per $n$, \ $\lambda = 0.7$", corner=DR)
        with self.voiceover(
            "Does the formula match reality? <bookmark mark='a'/> Simulate twenty thousand Poisson samples at each of "
            "four sample sizes, with lambda equal to point seven, and measure the actual spread of the estimates. "
            "<bookmark mark='b'/> At twenty, the simulated standard deviation is point one eight seven, and the formula "
            "says point one eight seven. At fifty, two hundred and a thousand, the same agreement. "
            "<bookmark mark='c'/> For the Poisson that's no surprise, because lambda hat is a sample mean and its "
            "variance is lambda over n exactly. <bookmark mark='d'/> For most models the formula is only a large-sample "
            "approximation. So let's look at a case where it isn't exact."
        ) as vo:
            self.play(FadeIn(hdr), FadeIn(tag))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in cells], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def shapes(self):
        g = np.random.Generator(np.random.PCG64(1925))
        lam = 0.5
        panels = VGroup()
        for j, (n, xr, ed) in enumerate(((5, (0, 2.0), np.linspace(0, 2.0, 41)), (100, (0.3, 0.7), np.linspace(0.3, 0.7, 41)))):
            est = n / g.exponential(1 / lam, (40000, n)).sum(1)
            h, _ = np.histogram(est, ed, density=True)
            ymax = max(h.max(), stats.norm.pdf(0, 0, lam / np.sqrt(n))) * 1.15
            A = axes(list(xr), [0, ymax], x_length=5.6, y_length=3.6, xlabel=rf"$\hat\lambda$, \ $n = {n}$",
                     xticks=[xr[0], lam, xr[1]], center=[-3.4 + 6.8 * j, 0.2, 0])
            ax = A.ax
            bars = hist_bars(ax, ed, h, color=SIM, opacity=0.6)
            xs = np.linspace(*xr, 200)
            nc = curve(ax, xs, stats.norm.pdf(xs, lam, lam / np.sqrt(n)), LIK, 3)
            tl = DashedLine(ax.c2p(lam, 0), ax.c2p(lam, ymax), color=EXACT, stroke_width=2)
            panels.add(VGroup(A, bars, nc, tl))
        leg = legend([(SIM, r"simulated $\hat\lambda = 1/\bar x$"), (LIK, r"$N\big(\lambda, \lambda^2/n\big)$: \ the asymptotic law")],
                     font_size=22).to_edge(UP, buff=0.4)
        foot = label(r"$n = 5$: \ skewed, \ biased up 25\%, \ SD 0.36 vs 0.22 predicted; \ $n = 100$: \ indistinguishable", font_size=24,
                     color=S.ACCENT).to_edge(DOWN, buff=0.85)
        tag = simulated_tag(r"simulated: \ 40,000 samples, \ rate $0.5$", corner=DR)
        with self.voiceover(
            "The exponential rate. <bookmark mark='a'/> With five observations, the sampling distribution of one over "
            "x-bar is skewed, with a long right tail, and the normal approximation, in green, misses it badly: the "
            "estimator is biased up by a quarter, and its spread is larger than the formula predicts. "
            "<bookmark mark='b'/> With a hundred observations, the histogram and the normal curve are almost "
            "indistinguishable. <bookmark mark='c'/> Large-sample theory is a statement about large samples. How large "
            "is large enough depends on the model and the parameter, and simulation is how you find out. Part 11 "
            "tests the resulting intervals on the Coverage Board, and Part 22 shows how to do better with the "
            "likelihood's own shape."
        ) as vo:
            self.play(FadeIn(leg), FadeIn(tag), *[FadeIn(p[0]) for p in panels], *[Create(p[3]) for p in panels])
            vo.wait_until("a")
            self.play(FadeIn(panels[0][1], lag_ratio=0.02), Create(panels[0][2]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1][1], lag_ratio=0.02), Create(panels[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def failures(self):
        tc = theorem_card(r"When the theory holds", r"the model is identifiable; \ the support of $p_\theta$ does not depend on $\theta$; \ "
                          r"$\theta_0$ is inside the parameter space; \ $\log p_\theta$ is smooth enough in $\theta$; \ "
                          r"and the number of parameters stays fixed as $n$ grows", who=r"the regularity conditions (Cram\'er, 1946)",
                          color=LIK, width=10.4, font_size=24).move_to([0, 1.7, 0])
        rows = fit_rows(VGroup(
            label(r"the support moves: \ the uniform and the tanks, \ error $\propto 1/n$, \ not normal (ch.~10)", font_size=24),
            label(r"too many parameters: \ Neyman \& Scott (1948): \ pairs $x_{i1}, x_{i2} \sim N(\mu_i, \sigma^2)$ \ give "
                  r"$\hat\sigma^2 \to \sigma^2/2$", font_size=24),
            label(r"an unbounded likelihood: \ a normal mixture, \ one component shrinking onto one point", font_size=24),
            label(r"a boundary: \ a variance component that is truly zero (Part 25)", font_size=24),
        ), 12.6, 0.3, [0, -1.6, 0])
        for r in rows:
            r.set_color(GREY_A)
        with self.voiceover(
            "This all rests on conditions, and it's worth knowing exactly where they break. <bookmark mark='a'/> The "
            "model must be identifiable; the set of possible values mustn't depend on the parameter; the truth must be "
            "inside the parameter space, not on its edge; the log-density must be smooth; and the number of parameters "
            "must stay fixed as the data grow. <bookmark mark='b'/> Break the support condition and you get the uniform "
            "and the tanks, where the error shrinks like one over n and isn't normal. <bookmark mark='c'/> Let the "
            "parameters grow with the data, and the MLE can be inconsistent: Jerzy Neyman and Elizabeth Scott's 1948 "
            "example gives pairs of measurements, each pair with its own mean. The MLE of the common variance converges "
            "to half the truth, however much data you collect. <bookmark mark='d'/> A mixture of two normals has an "
            "unbounded likelihood: shrink one component onto a single data point and the likelihood goes to infinity. "
            "<bookmark mark='e'/> And a parameter on a boundary, like a variance that's truly zero, gives a distribution "
            "that's half a point mass, which Part 25 meets."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tc, shift=UP * 0.2))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
