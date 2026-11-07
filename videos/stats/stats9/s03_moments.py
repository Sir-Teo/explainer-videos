from __future__ import annotations

import numpy as np

from videos.stats.stats9.common import *  # noqa: F403


class Moments(VoiceoverScene):
    def construct(self):
        self.card()
        self.pearson()
        self.recipe()
        self.gamma_fit()
        self.tanks()
        self.sampling()
        self.delta()

    def card(self):
        card = chapter_card(2, r"The method of moments", r"Match the model's averages to the sample's", lit=(1894,), part=PART)
        with self.voiceover("Chapter two. The method of moments."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def pearson(self):
        hc = history_card(1894, r"Karl Pearson, \ ``Contributions to the mathematical theory of evolution''",
                          r"W. F. R. Weldon's 1,000 crabs from Naples: \ the forehead-to-body ratio looked lopsided. \ "
                          r"Two races mixed? \ Pearson fitted a mixture of two normals, \ five unknowns, \ by matching the "
                          r"first five moments, \ and solved a polynomial of degree nine", color=S.MUSEUM, width=9.8,
                          font_size=24).move_to([0, 0.9, 0])
        rows = fit_rows(VGroup(
            label(r"the method needs computable, finite identifying moments; \ no density required", font_size=24,
                  color=S.ACCENT),
            label(r"Fisher (1912, 1922) would attack it as inefficient, \ and propose maximum likelihood", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.3, [0, -2.2, 0])
        intro = label("Pearson's crab mixture problem", font_size=36)
        with self.voiceover(
            "In 1893 the zoologist Raphael Weldon measured a thousand crabs from the Bay of Naples, and found that one "
            "ratio, forehead breadth to body length, had a lopsided distribution. Perhaps two races of crab were mixed "
            "together. <bookmark mark='a'/> Karl Pearson took up the problem in 1894. A mixture of two normals has five "
            "unknowns: two means, two variances and a mixing proportion. Pearson's idea was to choose them so that the "
            "model's first five moments, its average, its average square and so on, matched the sample's. That led him "
            "to a polynomial of degree nine, which he solved by hand. <bookmark mark='b'/> The method needs nothing but "
            "averages, so it works even when the density is too complicated to handle. <bookmark mark='c'/> Twenty "
            "years later, the young Ronald Fisher would argue that it throws information away, and propose maximum "
            "likelihood instead. We'll build both, and then settle the argument."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def recipe(self):
        rows = [
            cmath(r"\mu_j(\theta)", r"=", r"E_\theta X^j", r",\quad j = 1, \dots, p", font_size=36),
            cmath(r"m_j", r"=", r"\frac1n \sum_{i=1}^n x_i^j", font_size=36),
            cmath(r"\mu_j(\hat\theta)", r"=", r"m_j", r",\quad j = 1, \dots, p", font_size=36),
            cmath(r"\hat\theta", r"=", r"\mu^{-1}(m_1, \dots, m_p)", font_size=36),
        ]
        rows[3][2].set_color(MOM)
        whys = [why(r"the model's moments: \ functions of $\theta$"), why(r"the sample's moments: \ numbers"),
                why(r"$p$ unknowns, \ $p$ equations"), why(r"invert; \ often any moments will do, \ e.g.\ the variance for $\mu_2$")]
        with self.voiceover(
            "The recipe. <bookmark mark='a'/> A model with p unknown parameters has moments, the expected value of X, "
            "of X squared, and so on, each a function of theta. <bookmark mark='b'/> The sample has moments too: plain "
            "numbers, the averages of the data, their squares, and so on. <bookmark mark='c'/> Set the first p of them "
            "equal: p equations in p unknowns. <bookmark mark='d'/> Solve, and that's the estimator. Choose finite moments that identify the parameters: in practice we usually match the mean and the variance rather than the raw second moment. "
            "For independent identically distributed data with those moments finite, the law of large numbers makes the sample moments converge to the model's, so if the identifying inversion is "
            "continuous, the estimator is consistent. That's the whole method."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.5, x=-0.6, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gamma_fit(self):
        d = load("moments")
        xs = np.asarray(d["xs"])
        A = axes([0, 20], [0, 0.32], x_length=7.0, y_length=4.2, xlabel=r"$x$: \ 50 draws", ylabel=r"density",
                 xticks=[0, 5, 10, 15, 20], yticks=[0, 0.1, 0.2, 0.3], center=[-2.4, -0.2, 0])
        ax = A.ax
        bars = hist_bars(ax, np.linspace(0, 20, 21), np.asarray(d["hist_x"]), color=DATA, opacity=0.6)
        true = DashedVMobject(curve(ax, xs, np.asarray(d["pdf_true"]), WHITE, 2.5), num_dashes=50)
        mom = curve(ax, xs, np.asarray(d["pdf_mom"]), MOM, 3.5)
        a, b = d["mom"]
        rows = fit_rows(VGroup(
            MathTex(r"\text{Gamma}(\alpha, \beta):\ \ E X = \alpha\beta,\quad \mathrm{Var}\,X = \alpha\beta^2", font_size=28),
            MathTex(rf"\bar x = {d['mean']:.2f},\quad v_n = {d['var']:.2f}", font_size=28, color=DATA),
            MathTex(r"\hat\beta = \frac{v_n}{\bar x},\qquad \hat\alpha = \frac{\bar x^2}{v_n}", font_size=30, color=MOM),
            MathTex(rf"\hat\alpha = {a:.2f},\quad \hat\beta = {b:.2f}", font_size=30, color=MOM),
            MathTex(rf"\text{{truth (dashed): }} \alpha = {d['a0']:g},\ \beta = {d['sc0']:g}", font_size=28, color=WHITE),
        ), 5.4, 0.3, [4.1, 0.0, 0])
        tag = simulated_tag(r"simulated: \ Gamma$(2.5, 2)$, \ $n = 50$", corner=DR)
        with self.voiceover(
            "An example. <bookmark mark='a'/> Fifty draws from a gamma distribution, the skewed distribution of waiting "
            "times and rainfall totals. It has a shape alpha and a scale beta. Its mean is alpha beta, and its variance "
            "is alpha beta squared. <bookmark mark='b'/> The sample has mean four point eight and divisor-n variance seven point "
            "three five. <bookmark mark='c'/> Divide the variance by the mean to get beta, and square the mean over the "
            "variance to get alpha. <bookmark mark='d'/> Three point one four and one point five three. "
            "<bookmark mark='e'/> The truth, which only the simulation knows, was two point five and two. The fitted "
            "density, in orange, is close to the true one, dashed in white. Two lines of algebra, and a fit."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bars, lag_ratio=0.05), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Create(mom))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]), Create(true))
        self.clear_scene()

    def tanks(self):
        d = load("tanks")
        one = d["one"]
        rows = [
            cmath(r"E X", r"=", r"\frac{1 + 2 + \dots + N}{N} = \frac{N + 1}{2}", font_size=36),
            cmath(r"\frac{\hat N + 1}{2}", r"=", r"\bar x", font_size=36),
            cmath(r"\hat N", r"=", r"2\bar x - 1", font_size=36),
            cmath(r"\hat N", r"=", rf"2 \times {np.mean(one):.2f} - 1 = {d['one_est']['mom']:.1f}\ <\ {max(one)} = \max", font_size=34),
        ]
        rows[2][2].set_color(MOM)
        rows[3][2].set_color(S.RESID)
        whys = [why(r"one capture: \ any serial equally likely"), why(r"match the first moment"), why(r"unbiased: \ $E\bar X = (N+1)/2$"),
                why(r"our factory: \ an estimate the data rule out")]
        intro = label('Matching the average captured serial', font_size=36)
        with self.voiceover(
            "The tanks, by moments. <bookmark mark='a'/> A single captured tank is equally likely to carry any serial "
            "from one to N, so its average serial is N plus one over two. <bookmark mark='b'/> Set that equal to the "
            "sample mean, <bookmark mark='c'/> and solve: two x-bar minus one. Sampling without replacement doesn't "
            "change the expected mean, so it's unbiased. <bookmark mark='d'/> But look at our factory. Its six serials "
            "average a hundred and three, so the estimate is two hundred and five, and we have a tank numbered two "
            "hundred and fourteen in our hands. The method of moments can produce estimates the data have already "
            "ruled out. It only listens to averages, and here the average is the wrong thing to listen to."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.5, x=-0.6, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def sampling(self):
        d = load("moments")
        ed = np.asarray(d["edges"])
        A = axes([0.5, 6], [0, 0.9], x_length=7.4, y_length=4.2, xlabel=r"estimated shape $\hat\alpha$", ylabel=r"density",
                 xticks=[1, 2, 2.5, 3, 4, 5, 6], yticks=[0, 0.4, 0.8], center=[-2.0, -0.3, 0])
        ax = A.ax
        hm = hist_bars(ax, ed, np.asarray(d["h_mom"]), color=MOM, opacity=0.55)
        hl = hist_bars(ax, ed, np.asarray(d["h_mle"]), color=LIK, opacity=0.55)
        truth = DashedLine(ax.c2p(2.5, 0), ax.c2p(2.5, 0.9), color=EXACT, stroke_width=2.5)
        leg = legend([(MOM, r"method of moments"), (LIK, r"maximum likelihood (ch.~3)")], font_size=22).move_to([4.4, 2.2, 0])
        eff = (d["sd_mle"] / d["sd_mom"]) ** 2
        rows = fit_rows(VGroup(
            MathTex(rf"\mathrm{{SD}}:\ {d['sd_mom']:.3f}\ \text{{vs}}\ {d['sd_mle']:.3f}", font_size=28),
            MathTex(rf"\text{{bias}}:\ {d['bias_mom']:+.3f}\ \text{{vs}}\ {d['bias_mle']:+.3f}", font_size=28),
            MathTex(rf"\text{{variance ratio}} = \Big(\tfrac{{{d['sd_mle']:.3f}}}{{{d['sd_mom']:.3f}}}\Big)^2 = {eff:.2f}", font_size=28,
                    color=S.ACCENT),
            label(rf"about {100 * (1 - eff):.0f}\% less information by this variance comparison", font_size=24, color=S.ACCENT),
        ), 5.0, 0.32, [4.4, -0.4, 0])
        tag = simulated_tag(r"simulated: \ 4,000 samples of 50", corner=DR)
        with self.voiceover(
            "Is the method of moments any good? Grade it. <bookmark mark='a'/> Four thousand samples of fifty from the "
            "same gamma, the shape estimated from each by moments. It's centred near two and a half, but spread out: "
            "standard deviation point six two. <bookmark mark='b'/> Now the same samples, estimated by maximum "
            "likelihood, which we'll build in the next chapter. Tighter: point five two, and less biased too. "
            "<bookmark mark='c'/> The simulated variance ratio is point seven one. If variance scales inversely with sample size, fitting by moments here is approximately "
            "like throwing away about thirty percent of the data. That was exactly Fisher's complaint. The method of "
            "moments is simple, it's often a good starting point, as we'll use it in chapter four, but it isn't the "
            "best that can be done."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag), Create(truth))
            vo.wait_until("a")
            self.play(FadeIn(hm, lag_ratio=0.02), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(hl, lag_ratio=0.02), FadeIn(leg[1]), FadeIn(rows[:2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def delta(self):
        tc = theorem_card(r"Moment estimators are asymptotically normal",
                          r"If $m = (m_1, \dots, m_p)$ has $\sqrt n\,(m - \mu) \to N(0, \Sigma)$ (Part 6's CLT, \ needing $2p$ moments) \ "
                          r"and $\hat\theta = h(m)$ with $h$ differentiable, \ then \ "
                          r"$\sqrt n\,(\hat\theta - \theta) \to N\big(0,\ \nabla h\, \Sigma\, \nabla h^\top\big)$.",
                          who=r"the delta method (Part 6)", color=MOM, width=10.4, font_size=26).move_to([0, 1.2, 0])
        rows = fit_rows(VGroup(
            label(r"so moment estimators come with standard errors, \ from the same averages", font_size=24),
            label(r"the catch: \ high moments are noisy, \ and Pearson's fifth moment needs the tenth to be finite", font_size=24,
                  color=GREY_A),
            label(r"generalized method of moments (Hansen, 1982): \ more equations than unknowns, \ weighted (Part 37)", font_size=24,
                  color=S.ACCENT),
        ), 12.6, 0.32, [0, -1.9, 0])
        intro = label('When moment estimators have a normal limit', font_size=36)
        with self.voiceover(
            "One more thing the method gives for free. <bookmark mark='a'/> With independent identically distributed data and finite moments through order twice the highest moment used, the multivariate central "
            "limit theorem gives a joint normal limit for the moments. If the identifying inversion is differentiable, the delta "
            "method of Part 6 makes the estimator approximately normal too, with a variance we can compute from the "
            "gradient of the inversion and the covariance of the moments. <bookmark mark='b'/> So moment estimators come "
            "with standard errors. <bookmark mark='c'/> The catch is that higher moments are noisy: Pearson's fifth "
            "moment needs a finite tenth moment for its standard error to exist. <bookmark mark='d'/> The idea lives on "
            "in econometrics, where Lars Hansen's generalized method of moments, from 1982, uses more equations than "
            "unknowns and weights them optimally. It won him a share of the 2013 Nobel prize, and it returns with instrumental variables in Part 37."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(tc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
