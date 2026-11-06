from __future__ import annotations

from math import gamma, pi

import numpy as np
from scipy import stats as st

from videos.stats.stats7.common import *  # noqa: F403


class Rejection(VoiceoverScene):
    def construct(self):
        self.card()
        self.darts()
        self.proof()
        self.envelope()
        self.adaptive()
        self.dimension()

    def card(self):
        card = chapter_card(3, r"Rejection sampling", r"Throw darts, \ keep the ones under the curve", lit=(1951,), part=PART)
        with self.voiceover("Chapter three. Rejection sampling."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def darts(self):
        d = load("rejection")
        M = d["M"]
        x, y, acc = np.asarray(d["x"]), np.asarray(d["y"]), np.asarray(d["acc"]).astype(bool)
        A = axes([0, 1], [0, 2.6], x_length=7.4, y_length=4.6, xlabel=r"$x$", ylabel=r"density", xticks=[0, 0.25, 0.5, 0.75, 1],
                 yticks=[0, 1, 2], center=[-2.0, -0.4, 0])
        ax = A.ax
        xs = np.linspace(0, 1, 200)
        cv = curve(ax, xs, st.beta.pdf(xs, 2, 5), EXACT, 3.5)
        box = Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, M)[1] - ax.c2p(0, 0)[1], stroke_color=GREY_B,
                        stroke_width=2).move_to(ax.c2p(0.5, M / 2))
        ml = MathTex(rf"M = {M:.3f}", font_size=26, color=GREY_B).next_to(box, UP, buff=0.1).align_to(box, RIGHT)
        acc_d = VGroup(*[Dot(ax.c2p(a, b), radius=0.03, color=ACC) for a, b in zip(x[acc], y[acc])])
        rej_d = VGroup(*[Dot(ax.c2p(a, b), radius=0.03, color=REJ, fill_opacity=0.6) for a, b in zip(x[~acc], y[~acc])])
        rows = fit_rows(VGroup(
            MathTex(r"\text{target: } \mathrm{Beta}(2, 5),\ f(x) = 30x(1-x)^4", font_size=26, color=EXACT),
            label(r"1. \ a dart: \ $X \sim U(0, 1)$, \ $Y \sim U(0, M)$", font_size=24),
            label(r"2. \ keep $X$ if $Y \le f(X)$", font_size=24, color=ACC),
            MathTex(rf"\text{{kept: }} {100 * d['rate']:.1f}\%\ \approx\ 1/M = {100 / M:.1f}\%", font_size=26),
        ), 5.0, 0.3, [4.4, 0.8, 0])
        tag = note(r"600 darts, \ PCG32 uniforms").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Von Neumann's second idea, from the same 1951 paper, needs no inverse at all. Suppose we want draws "
            "from the beta distribution with parameters two and five, whose CDF has no simple inverse. "
            "<bookmark mark='a'/> Draw a box around its density: as wide as the support, as tall as the highest "
            "point, M. <bookmark mark='b'/> Throw darts uniformly into the box: a uniform x, and a uniform height "
            "between zero and M. <bookmark mark='c'/> Keep the dart if it lands under the curve; throw it away if "
            "it lands above. The x-coordinates of the kept darts are draws from the beta. "
            "<bookmark mark='d'/> Of six hundred darts, about forty-one percent were kept, which is the area under the "
            "curve, one, divided by the area of the box, M."
        ) as vo:
            self.play(FadeIn(A), Create(cv), FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(box), FadeIn(ml))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(p) for p in VGroup(*acc_d, *rej_d)], lag_ratio=0.004), run_time=3.0)
            vo.wait_until("c")
            self.play(rej_d.animate.set_opacity(0.15), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"P(\text{accept})", r"=", r"\int_0^1 \frac{f(x)}{M}\,dx", r"=", r"\frac1M", font_size=32),
            cmath(r"P(X \le t,\ \text{accept})", r"=", r"\int_0^t \frac{f(x)}{M}\,dx", r"=", r"\frac{F(t)}{M}", font_size=32),
            cmath(r"P(X \le t \mid \text{accept})", r"=", r"\frac{F(t)/M}{1/M}", r"=", r"F(t)", font_size=34),
            cmath(r"E[\text{darts per draw}]", r"=", r"M", r"\qquad \text{(geometric, Part 3)}", font_size=32),
        ]
        rows[2][4].set_color(EXACT)
        rows[3][2].set_color(S.ACCENT)
        whys = [why(r"$X$ uniform, \ then keep with chance $f(X)/M$"), why(r"the same, \ only for $X \le t$"),
                why(r"Part 2's conditional probability: \ exactly the target"), why(r"a tight box is a cheap box")]
        with self.voiceover(
            "Why does it work? <bookmark mark='a'/> A dart at x is kept with chance f of x over M; averaging over the "
            "uniform x, the chance of keeping a dart is one over M. <bookmark mark='b'/> The chance that it's kept "
            "and lies below t is the same integral, up to t: F of t over M. <bookmark mark='c'/> Divide, and given "
            "that a dart was kept, its x has CDF F of t: exactly the target, with no approximation. "
            "<bookmark mark='d'/> The number of darts needed for one draw is geometric, with mean M. A loose box "
            "wastes darts; the whole art of rejection sampling is a tight envelope."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.6, buff=0.62, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=False)
        self.clear_scene()

    def envelope(self):
        A = axes([-4, 4], [0, 0.7], x_length=7.4, y_length=4.4, xlabel=r"$x$", xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.2, 0.4],
                 center=[-2.0, -0.4, 0])
        ax = A.ax
        xs = np.linspace(-4, 4, 300)
        M = np.sqrt(2 * np.e / np.pi)
        f = curve(ax, xs, st.norm.pdf(xs), EXACT, 3.5)
        g = curve(ax, xs, M * 0.5 * np.exp(-np.abs(xs)), S.POST, 3)
        rows = fit_rows(VGroup(
            MathTex(r"\text{target: } \phi(x) = \tfrac{1}{\sqrt{2\pi}} e^{-x^2/2}", font_size=28, color=EXACT),
            MathTex(r"\text{proposal: } g(x) = \tfrac12 e^{-|x|}\ \ \text{(Laplace, by inversion)}", font_size=28, color=S.POST),
            MathTex(r"\phi \le M g,\quad M = \sqrt{2e/\pi} = " + f"{M:.3f}", font_size=28),
            label(r"accept $x \sim g$ \ with chance $\phi(x) / M g(x)$: \ 76\% of proposals kept", font_size=24, color=ACC),
            label(r"any proposal you can sample, \ scaled to cover the target", font_size=22, color=GREY_A),
        ), 5.4, 0.3, [4.2, 0.6, 0])
        with self.voiceover(
            "The box needn't be a box. <bookmark mark='a'/> To sample a normal, which has no bounded support, use a "
            "proposal you can already sample: here the Laplace, or double exponential, which inversion handles "
            "easily. <bookmark mark='b'/> Scale it up until it covers the normal everywhere; the smallest factor "
            "that works is root two e over pi, about one point three two. <bookmark mark='c'/> Draw from the "
            "Laplace, and keep each draw with chance equal to the ratio of the normal density to the scaled "
            "envelope. The same proof goes through, and about three draws in four are kept."
        ) as vo:
            self.play(FadeIn(A), Create(f), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Create(g), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def dimension(self):
        ds = np.arange(1, 21)
        rate = np.array([pi ** (d / 2) / gamma(d / 2 + 1) / 2 ** d for d in ds])
        A = axes([0.5, 20.5], [-8, 0], x_length=7.4, y_length=4.4, xlabel=r"dimension $d$",
                 ylabel=r"acceptance rate (log scale)", xticks=[1, 5, 10, 15, 20], yticks=[-8, -6, -4, -2, 0],
                 yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.0, -0.4, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(d, np.log10(r)), radius=0.07, color=BAD) for d, r in zip(ds, rate)])
        ln = polyline(ax, ds, np.log10(rate), BAD, 2.5)
        rows = fit_rows(VGroup(
            label(r"uniform points in the ball, \ by rejection from the cube", font_size=24),
            MathTex(r"\text{rate} = \frac{\pi^{d/2}/\Gamma(d/2 + 1)}{2^d}", font_size=30, color=BAD),
            MathTex(rf"d = 2:\ {100 * rate[1]:.0f}\%,\quad d = 10:\ {100 * rate[9]:.2f}\%,\quad d = 20:\ 2.5 \times 10^{{-8}}", font_size=26),
            label(r"in high dimensions almost every dart misses: \ the corners are everything", font_size=22, color=GREY_A),
            label(r"one option: \ a chain that stays where the mass is \ (chapter 11)", font_size=22, color=S.ACCENT),
        ), 5.6, 0.3, [4.2, 0.6, 0])
        with self.voiceover(
            "Rejection has a weakness that grows with dimension. <bookmark mark='a'/> To draw a uniform point in a "
            "ball, throw darts into the cube around it and keep those inside. <bookmark mark='b'/> The acceptance "
            "rate is the ball's volume over the cube's. <bookmark mark='c'/> In two dimensions it's seventy-nine "
            "percent. In ten dimensions, a quarter of a percent. In twenty, two and a half in a hundred million. "
            "<bookmark mark='d'/> In high dimensions almost all of a cube's volume lies outside its inscribed ball, and almost every "
            "dart misses. <bookmark mark='e'/> One option for high-dimensional Bayesian problems is "
            "not to throw darts independently but to walk: a Markov chain that stays where the probability is. "
            "That's chapter eleven."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ln), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def adaptive(self):
        A = axes([-3.2, 3.2], [-5.5, 2.0], x_length=7.0, y_length=4.4, xlabel=r"$x$", ylabel=r"$\log f(x)$", xticks=[-2, 0, 2],
                 yticks=[-4, -2, 0], center=[-2.4, -0.4, 0])
        ax = A.ax
        lf = lambda x: -0.5 * x ** 2  # noqa: E731
        xs = np.linspace(-3.2, 3.2, 200)
        cv = curve(ax, xs, lf(xs), EXACT, 3.5)
        knots = [-1.5, 0.4, 2.0]
        tans = VGroup()
        for k in knots:
            xx = np.linspace(k - 1.8, k + 1.8, 20)
            yy = lf(k) - k * (xx - k)
            keep = (yy > -5.5) & (xx > -3.2) & (xx < 3.2)
            tans.add(polyline(ax, xx[keep], yy[keep], S.POST, 2))
        kd = VGroup(*[Dot(ax.c2p(k, lf(k)), radius=0.07, color=S.POST) for k in knots])
        rows = fit_rows(VGroup(
            label(r"log-concave $f$: \ $\log f$ bends down \ (normal, gamma with $\alpha \ge 1$, logistic)",
                  font_size=22),
            label(r"tangents to $\log f$ lie above it: \ their minimum is an envelope", font_size=24, color=S.POST),
            label(r"exponentiated: \ a piecewise-exponential proposal, \ sampled by inversion", font_size=24),
            label(r"every rejection adds a tangent: \ the envelope tightens as it runs", font_size=24, color=ACC),
            label(r"adaptive rejection sampling: \ Gilks \& Wild (1992), \ inside the first BUGS", font_size=22, color=GREY_A),
        ), 5.4, 0.3, [4.1, 0.2, 0])
        with self.voiceover(
            "Building an envelope by hand is an art; for a large family of densities it can be automatic. "
            "<bookmark mark='a'/> Call a density log-concave if its logarithm bends downwards everywhere: the normal, "
            "the gamma with shape at least one, the logistic, and canonical logistic or Poisson posteriors with log-concave priors in later "
            "parts. <bookmark mark='b'/> Then every tangent line to the log density lies above it, so the lowest of a "
            "few tangents is an envelope. <bookmark mark='c'/> Exponentiate it, and the envelope is piecewise "
            "exponential, easy to sample by inversion. <bookmark mark='d'/> And each time a proposal is rejected, add a "
            "tangent at that point: the envelope tightens as the sampler runs. Walter Gilks and Pascal Wild's "
            "adaptive rejection sampling, from 1992, was the engine inside the first general-purpose Bayesian "
            "software, BUGS."
        ) as vo:
            self.play(FadeIn(A), Create(cv))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(tans), FadeIn(kd), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()
