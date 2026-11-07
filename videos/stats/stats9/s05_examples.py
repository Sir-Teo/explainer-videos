from __future__ import annotations

import numpy as np
from scipy import special

from videos.stats.stats9.common import *  # noqa: F403


class Examples(VoiceoverScene):
    def construct(self):
        self.card()
        self.normal()
        self.surface()
        self.exponential()
        self.uniform()
        self.newton()
        self.digits()

    def card(self):
        card = chapter_card(4, r"Likelihoods in practice", r"Normal, \ exponential, \ uniform, \ gamma", part=PART)
        with self.voiceover("Chapter four. Likelihoods in practice."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def normal(self):
        rows = [
            cmath(r"\ell(\mu, \sigma^2)", r"=", r"-\frac n2\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_i (x_i - \mu)^2", font_size=34),
            cmath(r"\frac{\partial\ell}{\partial\mu}", r"=", r"\frac{1}{\sigma^2}\sum_i (x_i - \mu) = 0\ \Rightarrow\ \hat\mu = \bar x",
                  font_size=34),
            cmath(r"\frac{\partial\ell}{\partial\sigma^2}", r"=", r"-\frac{n}{2\sigma^2} + \frac{1}{2\sigma^4}\sum_i (x_i - \hat\mu)^2 = 0",
                  font_size=34),
            cmath(r"\hat\sigma^2", r"=", r"\frac1n\sum_i (x_i - \bar x)^2", r"\quad\text{divisor } n", font_size=34),
        ]
        rows[1][2].set_color(LIK)
        rows[3][2].set_color(LIK)
        whys = [why(r"the normal density, \ logged and summed"), why(r"the mean: \ the sample mean, \ for any $\sigma$"),
                why(r"plug in $\hat\mu$ and solve"), why(r"biased by $(n-1)/n$: \ the MLE is not unbiased (Part 8)")]
        with self.voiceover(
            "The normal distribution first. <bookmark mark='a'/> The log-likelihood has two parameters, the mean and "
            "the variance. The second term is minus the sum of squared deviations over twice the variance, so "
            "maximizing over mu means minimizing squared error: least squares is maximum likelihood for normal errors, "
            "which is how Gauss arrived at both. <bookmark mark='b'/> The derivative in mu vanishes at the sample "
            "mean, whatever sigma is. <bookmark mark='c'/> Plug that in and differentiate in the variance. "
            "<bookmark mark='d'/> The maximum likelihood estimate of the variance divides by n, not n minus one. It's "
            "biased, by a factor of n minus one over n, exactly the bias Part 8 removed. Maximum likelihood doesn't care "
            "about unbiasedness. As Part 8 also showed, the divisor n has a smaller mean squared error anyway."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def surface(self):
        g = np.random.Generator(np.random.PCG64(1809))
        x = g.normal(10, 2, 20)
        n = len(x)
        mus = np.linspace(8, 12, 44)
        sds = np.linspace(1.0, 4.0, 30)
        M, Sd = np.meshgrid(mus, sds)
        ll = -n * np.log(Sd) - ((x[None, None, :] - M[..., None]) ** 2).sum(-1) / (2 * Sd ** 2)
        ll -= -n * np.log(x.std()) - n / 2
        A = axes([8, 12], [1, 4], x_length=6.6, y_length=4.5, xlabel=r"$\mu$", ylabel=r"$\sigma$", xticks=[8, 9, 10, 11, 12],
                 yticks=[1, 2, 3, 4], center=[-2.6, -0.2, 0])
        ax = A.ax
        dx = ax.c2p(mus[1], 1)[0] - ax.c2p(mus[0], 1)[0]
        dy = ax.c2p(8, sds[1])[1] - ax.c2p(8, sds[0])[1]
        cells = VGroup()
        for i in range(len(sds)):
            for j in range(len(mus)):
                v = max(ll[i, j], -12) / 12 + 1  # 0 (far) .. 1 (peak)
                c = interpolate_color(ManimColor("#101521"), ManimColor(LIK), v ** 1.6)
                cells.add(Rectangle(width=dx * 1.02, height=dy * 1.02, stroke_width=0, fill_color=c, fill_opacity=1)
                          .move_to(ax.c2p(mus[j], sds[i])))
        mu_h, sd_h = x.mean(), x.std()
        pk = Dot(ax.c2p(mu_h, sd_h), radius=0.08, color=S.ACCENT)
        ring = VGroup()
        thr = -stats.chi2.ppf(0.95, df=2) / 2
        for i in range(len(sds)):
            for j in range(len(mus)):
                if ll[i, j] >= thr - 0.0 and (ll[i, j] - thr) < 0.6:
                    ring.add(Dot(ax.c2p(mus[j], sds[i]), radius=0.025, color=WHITE))
        rows = fit_rows(VGroup(
            MathTex(rf"\hat\mu = \bar x = {mu_h:.2f}", font_size=30, color=S.ACCENT),
            MathTex(rf"\hat\sigma = {sd_h:.2f}", font_size=30, color=S.ACCENT),
            MathTex(r"\text{truth: } \mu = 10,\ \sigma = 2", font_size=28, color=EXACT),
            label(r"a hill over the $(\mu, \sigma)$ plane; \ brighter is more likely", font_size=24, color=GREY_A),
            label(r"lopsided in $\sigma$: \ small $\sigma$ is ruled out fast,", font_size=24, color=GREY_A),
            label(r"large $\sigma$ slowly", font_size=24, color=GREY_A),
        ), 5.0, 0.34, [4.3, 0.0, 0])
        tag = simulated_tag(r"simulated: \ 20 draws from $N(10, 4)$", corner=DR)
        with self.voiceover(
            "With two parameters, the likelihood is a surface. <bookmark mark='a'/> Twenty draws from a normal with "
            "mean ten and standard deviation two. Each point of this plane is a candidate pair, mu and sigma, coloured "
            "by its log-likelihood: brighter is better. <bookmark mark='b'/> The top of the hill is at the sample mean "
            "and the divisor-n standard deviation. <bookmark mark='c'/> The truth, ten and two, sits inside the bright "
            "region. <bookmark mark='d'/> Notice the shape. The hill falls off steeply toward small sigma, since a "
            "narrow curve can't explain the spread we see, but only slowly toward large sigma. The white dots trace the "
            "contour about three log-likelihood units below the peak, an approximate ninety-five percent joint confidence region using two degrees of freedom. In more than one "
            "dimension, likelihood becomes geometry: a peak, a curvature matrix, and contours."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cells), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(pk, scale=1.6), FadeIn(rows[:2]))
            vo.wait_until("c")
            tr = Star(n=5, outer_radius=0.13, color=EXACT, fill_opacity=1).move_to(ax.c2p(10, 2))
            self.play(FadeIn(tr), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(ring), FadeIn(rows[3:]))
        self.clear_scene()

    def exponential(self):
        d = load("examples")
        r = np.asarray(d["rates"])
        A = axes([0.1, 1.5], [-6, 0], x_length=6.0, y_length=3.8, xlabel=r"rate $\lambda$", ylabel=r"$\ell(\lambda) - \ell(\hat\lambda)$",
                 xticks=[0.25, 0.5, 0.75, 1.0, 1.25, 1.5], yticks=[-6, -3, 0], center=[-3.2, -0.4, 0])
        ax = A.ax
        cv = clip_curve(ax, r, d["exp_ll"], LIK, 3.5, ymin=-6)
        pk = DashedLine(ax.c2p(d["rate_hat"], -6), ax.c2p(d["rate_hat"], 0), color=S.ACCENT, stroke_width=2)
        tr = DashedLine(ax.c2p(0.5, -6), ax.c2p(0.5, 0), color=EXACT, stroke_width=2)
        n = len(d["exp_x"])
        rows = fit_rows(VGroup(
            MathTex(r"p_\lambda(x) = \lambda e^{-\lambda x}", font_size=30),
            MathTex(r"\ell(\lambda) = n\log\lambda - \lambda\sum x_i", font_size=30),
            MathTex(r"U(\lambda) = \frac n\lambda - \sum x_i = 0\ \Rightarrow\ \hat\lambda = \frac{1}{\bar x}", font_size=30, color=LIK),
            MathTex(rf"n = {n}:\ \ \hat\lambda = {d['rate_hat']:.3f}\quad(\text{{truth }} 0.5)", font_size=28, color=S.ACCENT),
            MathTex(r"E\hat\lambda = \frac{n}{n - 1}\,\lambda\quad\text{biased up}", font_size=28, color=GREY_A),
        ), 5.8, 0.3, [3.4, 0.0, 0])
        tag = simulated_tag(r"simulated: \ 12 waiting times, \ rate $0.5$", corner=DR)
        with self.voiceover(
            "The exponential distribution, for waiting times. <bookmark mark='a'/> Its density is lambda e to the minus "
            "lambda x, <bookmark mark='b'/> so the log-likelihood is n log lambda minus lambda times the total waiting "
            "time. <bookmark mark='c'/> The score vanishes at one over the mean: if you waited two minutes on average, "
            "events happen at a rate of one half per minute. <bookmark mark='d'/> Twelve simulated waits give point five "
            "nine one; the truth was point five. <bookmark mark='e'/> And once again the MLE is biased: since one over "
            "the mean is a convex function of the mean, Jensen's inequality pushes it up, and the exact factor is n "
            "over n minus one. Chapter ten returns to this estimator to measure it against the best possible."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cv))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(pk))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Create(tr))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def uniform(self):
        d = load("examples")
        th = np.asarray(d["th"])
        u = np.asarray(d["u"])
        A = axes([0, 16], [0, 1.1], x_length=7.0, y_length=3.4, xlabel=r"$\theta$", ylabel=r"$L(\theta) \div L(\hat\theta)$",
                 xticks=[0, 4, 8, 12, 16], yticks=[0, 0.5, 1], center=[-2.4, -0.9, 0])
        ax = A.ax
        lik = np.asarray(d["u_lik"])
        keep = th >= d["u_max"]
        cv = curve(ax, th[keep], lik[keep], LIK, 3.5)
        zero = Line(ax.c2p(0, 0), ax.c2p(d["u_max"], 0), color=S.RESID, stroke_width=5)
        jump = DashedLine(ax.c2p(d["u_max"], 0), ax.c2p(d["u_max"], 1), color=S.ACCENT, stroke_width=2)
        pts = VGroup(*[Dot(ax.c2p(v, 0), radius=0.07, color=DATA) for v in u])
        rows = fit_rows(VGroup(
            MathTex(r"p_\theta(x) = \tfrac1\theta \text{ on } [0, \theta]", font_size=30),
            MathTex(r"L(\theta) = \theta^{-n}\,\mathbf 1\{\theta \ge \max x_i\}", font_size=30),
            MathTex(rf"\hat\theta = \max x_i = {d['u_max']:.2f}\quad(\text{{truth }} 10)", font_size=30, color=LIK),
            label(r"the support depends on $\theta$:", font_size=24, color=S.ACCENT),
            label(r"no derivative at the peak;", font_size=24, color=S.ACCENT),
            label(r"no Cram\'er--Rao bound (ch.~10)", font_size=24, color=S.ACCENT),
        ), 5.2, 0.34, [4.3, 0.2, 0])
        tag = simulated_tag(r"simulated: \ 8 draws, \ uniform on $[0, 10]$", corner=DR)
        with self.voiceover(
            "The uniform distribution on zero to theta is the tank problem with continuous serial numbers. "
            "<bookmark mark='a'/> Eight draws. <bookmark mark='b'/> The density is one over theta, but only up to "
            "theta, so the likelihood is theta to the minus n if theta is at least the largest observation, and zero "
            "otherwise. Any theta below nine point two four is impossible, because we've seen a value that big. "
            "<bookmark mark='c'/> Above it, the likelihood only falls. So the MLE is the largest observation. "
            "<bookmark mark='d'/> The peak sits at a jump. This is what statisticians call an irregular problem: the "
            "set of possible values depends on the parameter. The usual calculus fails, and chapter ten will show that "
            "the usual limits on accuracy fail too."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(zero), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(jump), Create(cv), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def newton(self):
        d = load("newton")
        aa = np.asarray(d["aa"])
        n, lm = d["n"], d["lm"]

        def U(a):
            return n * (np.log(a) - special.digamma(a) - lm)

        def dU(a):
            return n * (1 / a - special.polygamma(1, a))

        A = axes([0.8, 4.2], [-4, 24], x_length=7.2, y_length=4.4, xlabel=r"shape $\alpha$", ylabel=r"score $U(\alpha)$",
                 xticks=[1, 2, 3, 4], yticks=[0, 10, 20], center=[-2.0, -0.3, 0])
        ax = A.ax
        keep = aa <= 4.2
        cv = clip_curve(ax, aa[keep], np.asarray(d["score"])[keep], LIK, 3.5, ymin=-4, ymax=24)
        zero = DashedLine(ax.c2p(0.8, 0), ax.c2p(4.2, 0), color=GREY_C, stroke_width=1.5)
        steps = VGroup()
        a = 1.0
        path = [a]
        for _ in range(4):
            u, du = U(a), dU(a)
            a_new = a - u / du
            lo, hi = max(0.8, min(a, a_new) - 0.1), min(4.2, max(a, a_new) + 0.1)
            t = Line(ax.c2p(lo, u + du * (lo - a)), ax.c2p(hi, u + du * (hi - a)), color=S.ACCENT, stroke_width=2.2)
            v = DashedLine(ax.c2p(a_new, 0), ax.c2p(a_new, U(a_new)), color=GREY_B, stroke_width=1.5)
            steps.add(VGroup(Dot(ax.c2p(a, u), radius=0.06, color=S.ACCENT), t, Dot(ax.c2p(a_new, 0), radius=0.06, color=WHITE), v))
            a = a_new
            path.append(a)
        rows = fit_rows(VGroup(
            MathTex(r"U(\alpha) = n\big(\log\alpha - \psi(\alpha) - \log\bar x + \overline{\log x}\big)", font_size=26),
            label(r"$\psi$, \ the digamma function: \ no closed-form root", font_size=22, color=GREY_A),
            MathTex(r"\alpha_{t+1} = \alpha_t - \frac{U(\alpha_t)}{U'(\alpha_t)}", font_size=32, color=S.ACCENT),
            MathTex(r"\alpha:\ " + r"\to ".join(f"{p:.3f}" for p in path[:4]), font_size=24),
        ), 5.4, 0.32, [4.3, -0.2, 0])
        with self.voiceover(
            "Most likelihoods have no closed-form maximum. The gamma from chapter two is the classic example. "
            "<bookmark mark='a'/> The scale can be eliminated, and the score for the shape involves the digamma "
            "function, the derivative of the log of the gamma function. No algebra solves it. <bookmark mark='b'/> So "
            "we solve it numerically, with Newton's method. Start somewhere, at alpha equals one. Draw the tangent to "
            "the score curve there, <bookmark mark='c'/> and jump to where the tangent crosses zero. "
            "<bookmark mark='d'/> Repeat. Each step replaces the curve with its tangent line, which means replacing the "
            "log-likelihood with its best-fitting parabola and jumping to the parabola's peak. Because this score curve "
            "is convex, every step lands short of the root, and the steps close in from the left. Part 21 studies "
            "optimization properly: Newton, Fisher scoring, gradient methods and the EM algorithm."
        ) as vo:
            self.play(FadeIn(A), Create(zero), Create(cv), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(steps[0][0]), Create(steps[0][1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(steps[0][2]), Create(steps[0][3]))
            vo.wait_until("d")
            for s_ in steps[1:]:
                self.play(FadeIn(s_[0]), Create(s_[1]), run_time=0.8)
                self.play(FadeIn(s_[2]), Create(s_[3]), run_time=0.6)
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def digits(self):
        d = load("newton")
        path = d["path"][:4]
        root = d["path"][-1]
        hdr = VGroup(*[label(t, font_size=24, color=GREY_A) for t in (r"step", r"$\alpha_t$", r"error")]).arrange(RIGHT, buff=2.2)
        hdr.move_to([0, 2.1, 0])
        rows = VGroup()
        for t, a in enumerate(path):
            err = abs(a - root)
            e_tex = r"0" if err == 0 else (rf"{err:.1e}".replace("e-0", r"\times 10^{-").replace("e-", r"\times 10^{-") + "}")
            rows.add(VGroup(MathTex(str(t), font_size=30), MathTex(f"{a:.13f}", font_size=30, color=LIK), MathTex(e_tex, font_size=30)))
        for i, r in enumerate(rows):
            for j, c in enumerate(r):
                c.move_to([hdr[j].get_x(), 1.4 - 0.62 * i, 0])
        notes = fit_rows(VGroup(
            label(r"starting from the method-of-moments estimate, \ $\hat\alpha_{\mathrm{MoM}} = 3.136$", font_size=24, color=MOM),
            label(r"the error is squared at every step: \ quadratic convergence, \ the digits double", font_size=26, color=S.ACCENT),
            label(r"the moment estimator's best use: \ a starting point for likelihood", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -2.2, 0])
        intro = label("Newton's method near the root", font_size=36)
        with self.voiceover(
            "How fast does it converge? <bookmark mark='a'/> Start instead from the method-of-moments estimate, three "
            "point one three six, which is already close. <bookmark mark='b'/> After one Newton step the error is about "
            "two in ten million. After two, it's at the limit of double-precision arithmetic. <bookmark mark='c'/> Near "
            "the root, Newton's method squares the error at every step, so the number of correct digits doubles each "
            "time. That's quadratic convergence. And it suggests the method of moments' best role: not the final "
            "answer, but a good place to start the search for the maximum likelihood estimate."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(rows[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[1:]], lag_ratio=0.5))
            vo.wait_until("c")
            self.play(FadeIn(notes[1:]))
        self.clear_scene()
