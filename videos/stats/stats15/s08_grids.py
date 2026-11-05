from __future__ import annotations

import numpy as np

from videos.stats.stats15.common import *  # noqa: F403


class Grids(VoiceoverScene):
    def construct(self):
        self.card()
        self.recipe()
        self.challenger()
        self.marginal()
        self.p31()
        self.mixture_prior()
        self.curse()

    def card(self):
        card = chapter_card(7, r"Grids", r"Any posterior in one or two dimensions, \ by brute force", part=PART)
        with self.voiceover("Chapter seven. Grids."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def recipe(self):
        rows = [
            cmath(r"\theta_1 < \theta_2 < \cdots < \theta_G", r":", r"\text{a fine grid}", font_size=32),
            cmath(r"w_g", r"=", r"p(y \mid \theta_g)\,\pi(\theta_g)", font_size=34),
            cmath(r"\pi(\theta_g \mid y)", r"\approx", r"w_g \Big/ \textstyle\sum_h w_h\,\Delta", font_size=34),
            cmath(r"\mathbb E[f(\theta) \mid y]", r"\approx", r"\textstyle\sum_g f(\theta_g)\,\pi(\theta_g \mid y)\,\Delta", font_size=32),
        ]
        rows[2][2].set_color(POST)
        whys = [why(r"cover the plausible range"), why(r"likelihood $\times$ prior at each point (on the log scale, to avoid underflow)"),
                why(r"normalize numerically"), why(r"any summary is a weighted sum")]
        with self.voiceover(
            "Conjugacy is a lucky accident. For most models, the posterior has no formula. With one or two parameters there's "
            "a simple remedy. <bookmark mark='a'/> Lay a fine grid over the plausible values. <bookmark mark='b'/> At each "
            "point, compute the likelihood times the prior, working with logarithms so that tiny numbers don't underflow. "
            "<bookmark mark='c'/> Divide by the sum to normalize. <bookmark mark='d'/> Any summary, a mean, a probability, a "
            "quantile, is then a weighted sum over the grid. No conjugacy, no algebra: just arithmetic."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def challenger(self):
        d = load("grid")
        gx, gy = np.asarray(d["gx4"]), np.asarray(d["gy4"])
        dens = np.asarray(d["dens"])
        A = axes([gx[0], gx[-1]], [gy[0], gy[-1]], x_length=6.4, y_length=4.6, xlabel=r"$\beta_0$", ylabel=r"$\beta_1$",
                 xticks=[0, 10, 20, 30, 40], yticks=[-0.6, -0.4, -0.2, 0], center=[-2.6, 0.0, 0])
        ax = A.ax
        dx, dy = gx[1] - gx[0], gy[1] - gy[0]
        top = dens.max()
        cells = VGroup()
        for j, b1 in enumerate(gy):
            for i, b0 in enumerate(gx):
                t = float(dens[j, i] / top)
                if t < 0.01:
                    continue
                p0, p1 = ax.c2p(b0 - dx / 2, b1 - dy / 2), ax.c2p(b0 + dx / 2, b1 + dy / 2)
                cells.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0,
                                    fill_color=interpolate_color(ManimColor("#1B2733"), ManimColor(POST), t ** 0.7), fill_opacity=1).move_to((p0 + p1) / 2))
        rows = fit_rows(VGroup(
            label(r"Part 14's Challenger model, \ flat prior", font_size=24),
            MathTex(r"\pi(\beta_0, \beta_1 \mid y) \propto \prod_i p_i^{y_i}(1 - p_i)^{1 - y_i}", font_size=26),
            label(rf"{d['cells']:,} grid points", font_size=22, color=GREY_A),
            label(r"the same long ridge as the log-likelihood", font_size=24, color=POST),
            label(r"now a probability distribution over the coefficients", font_size=22, color=OBS),
        ), 4.6, 0.36, [4.5, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Bring back Part 14's Challenger model: logistic regression of O-ring distress on temperature, "
            "now with a flat prior on the two coefficients. <bookmark mark='b'/> The posterior is the likelihood, normalized. "
            "There's no conjugate prior for logistic regression, so no formula. <bookmark mark='c'/> Evaluate it on a grid of "
            "sixty thousand points. <bookmark mark='d'/> The picture is Part 14's long diagonal ridge, <bookmark mark='e'/> but "
            "now it's a probability distribution over the coefficients, and we can ask it questions directly."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(cells), FadeIn(rows[2]), run_time=2.0)
            for k, m_ in enumerate("de"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()

    def marginal(self):
        d = load("grid")
        gy, my = np.asarray(d["gy"]), np.asarray(d["my"])
        A = axes([-0.7, 0.1], [0, 3.6], x_length=7.0, y_length=4.2, xlabel=r"$\beta_1$, \ log-odds per $^\circ$F", ylabel=r"posterior density",
                 xticks=[-0.6, -0.4, -0.2, 0], yticks=[0, 1, 2, 3], center=[-2.4, 0.2, 0])
        ax = A.ax
        cv = density(ax, gy, my, POST)
        neg = gy < 0
        sh = shade(ax, gy[~neg], my[~neg], RES, 0.6)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 3.4), color=GREY_C, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"sum the grid over $\beta_0$: \ the marginal of $\beta_1$", font_size=22),
            MathTex(rf"\mathbb E[\beta_1 \mid y] = {d['b1_mean']:.3f}", font_size=28, color=POST),
            MathTex(rf"P(\beta_1 < 0 \mid y) = {d['p_b1_neg']:.4f}", font_size=28, color=OBS),
            label(r"``colder is worse'', \ with probability 0.999", font_size=22, color=OBS),
            label(r"Part 14 could only give a $p$-value", font_size=22, color=GREY_A),
        ), 4.6, 0.36, [4.5, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Add up the grid over the intercept, and you have the posterior for the slope alone. "
            "<bookmark mark='b'/> Its mean is minus point two eight seven, a little more negative than the maximum-likelihood "
            "minus point two three two, because the posterior is skewed. <bookmark mark='c'/> The probability that the slope is "
            "negative, the red sliver being the rest, is point nine nine eight seven. <bookmark mark='d'/> In words: given the "
            "twenty-three flights and a flat prior, colder launches are worse with probability about ninety-nine point nine "
            "percent. <bookmark mark='e'/> Part 14's likelihood-ratio test could only say that data like these would be rare "
            "if temperature didn't matter."
        ) as vo:
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(cv), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(sh), FadeIn(rows[2]))
            for k, m_ in enumerate("de"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()

    def p31(self):
        d = load("grid")
        h = np.asarray(d["p31_hist"], float)
        h = h / h.sum()
        A = axes([0.5, 1.0], [0, 1.0], x_length=7.0, y_length=4.2, xlabel=r"$p(31^\circ\text{F})$", ylabel=r"posterior probability",
                 xticks=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0], yticks=[0, 0.5, 1], center=[-2.4, 0.2, 0])
        ax = A.ax
        edges = np.linspace(0, 1, 41)
        keep = edges[:-1] >= 0.5
        bars = hist_bars(ax, edges[:-1][keep].tolist() + [1.0], h[keep], color=POST, opacity=0.85)
        rows = fit_rows(VGroup(
            label(r"each grid point implies a $p(31^\circ\text{F})$", font_size=22),
            MathTex(rf"\text{{median}}\ {d['p31_median']:.4f}", font_size=28, color=POST),
            MathTex(rf"P\big(p(31) > 0.9 \mid y\big) = {d['p_gt_09']:.3f}", font_size=28, color=OBS),
            MathTex(rf"2.5\%\ \text{{quantile:}}\ {d['p31_lo']:.2f}", font_size=26),
            label(r"compare Part 14's profile interval: \ [0.80, 1]", font_size=22, color=GREY_A),
            label(r"the extrapolation caveat is unchanged", font_size=22, color=RES),
        ), 4.6, 0.34, [4.5, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Each point of the grid implies a probability of distress at thirty-one degrees, so the "
            "posterior for the coefficients becomes a posterior for that probability. <bookmark mark='b'/> Its median is point "
            "nine nine nine nine. <bookmark mark='c'/> The posterior probability that the chance of distress exceeded ninety "
            "percent is point nine seven. <bookmark mark='d'/> Its lower two and a half percent point is point eight nine, "
            "<bookmark mark='e'/> a little above Part 14's profile-likelihood interval, which started at point eight oh. "
            "<bookmark mark='f'/> And the caveat is exactly the same: all of this rests on the logistic curve's shape below "
            "fifty-three degrees, where there are no data. A posterior doesn't cure an extrapolation."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.05), FadeIn(rows[0]))
            for k, m_ in enumerate("bcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def curse(self):
        ks = np.arange(1, 9)
        A = axes([0.5, 8.5], [0, 16.5], x_length=6.6, y_length=4.2, xlabel=r"parameters, \ $k$", ylabel=r"$\log_{10}$ grid points",
                 xticks=list(range(1, 9)), yticks=[0, 4, 8, 12, 16], center=[-2.6, 0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(k, 2 * k), radius=0.09, color=RES) for k in ks])
        ln = VMobject(stroke_color=RES, stroke_width=3).set_points_as_corners([ax.c2p(k, 2 * k) for k in ks])
        rows = fit_rows(VGroup(
            label(r"100 points per parameter: \ $100^k$ in all", font_size=24),
            label(r"2 parameters: \ 10,000", font_size=24, color=HIT),
            label(r"8 parameters: \ $10^{16}$", font_size=24, color=RES),
            label(r"and nearly all of them where the posterior is negligible", font_size=22),
            label(r"we need to visit only where the probability is: \ next chapter", font_size=22, color=OBS),
        ), 4.6, 0.36, [4.5, 0.2, 0])
        with self.voiceover(
            "The catch is dimension. <bookmark mark='a'/> With a hundred points per parameter, a grid in k dimensions has a "
            "hundred to the k points. <bookmark mark='b'/> Two parameters: ten thousand, easy. <bookmark mark='c'/> Eight "
            "parameters: ten to the sixteen, far beyond any computer. <bookmark mark='d'/> Worse, almost all those points sit "
            "where the posterior is negligible: in high dimensions the posterior occupies a vanishing fraction of any box around "
            "it. <bookmark mark='e'/> What we need is a method that visits only the places where the probability is, in "
            "proportion to how much there is. That's the next chapter."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(dots), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def mixture_prior(self):
        from scipy import stats as st
        xs = np.linspace(0.001, 0.999, 999)
        prior = 0.5 * st.beta(50, 50).pdf(xs) + 0.5
        lik = xs ** 7 * (1 - xs) ** 3
        post = prior * lik
        post /= np.trapezoid(post, xs)
        prior_n = prior / np.trapezoid(prior, xs)
        A = axes([0, 1], [0, 8], x_length=7.4, y_length=4.2, xlabel=r"$p$", ylabel=r"density", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 4, 8],
                 center=[-2.2, 0.2, 0])
        ax = A.ax
        cpr = density(ax, xs, np.minimum(prior_n, 7.8), PRIOR, fill=0.15)
        cpo = density(ax, xs, np.minimum(post, 7.8), POST)
        p_near = float(np.trapezoid(post[(xs > 0.4) & (xs < 0.6)], xs[(xs > 0.4) & (xs < 0.6)]))
        rows = fit_rows(VGroup(
            label(r"a prior no table lists: \ half ``probably fair'', \ half ``no idea''", font_size=24, color=PRIOR),
            MathTex(r"\pi(p) = \tfrac12\,\text{Beta}(50, 50) + \tfrac12\,\text{Uniform}", font_size=26, color=PRIOR),
            label(r"7 of 10, \ on a grid of 999 points", font_size=24),
            label(r"the posterior has two humps", font_size=24, color=POST),
            MathTex(rf"P(0.4 < p < 0.6 \mid y) = {p_near:.2f}", font_size=28, color=POST),
        ), 4.6, 0.36, [4.5, 0.2, 0])
        with self.voiceover(
            "Grids free the prior too. <bookmark mark='a'/> Suppose you believe a coin is probably fair, but you're not sure: "
            "half your belief is a tight bump at one half, Beta fifty fifty, and half is complete ignorance, uniform. "
            "<bookmark mark='b'/> No conjugate table lists that mixture. <bookmark mark='c'/> On a grid of a thousand points, "
            "seven heads in ten is no harder than before. <bookmark mark='d'/> The posterior has two humps: one at a half, from "
            "the \"fair\" component, and a broad one near point seven, from the \"no idea\" part. <bookmark mark='e'/> The "
            "posterior probability that p is between point four and point six is still about two thirds. The data have shifted belief toward an "
            "unfair coin without abandoning the fair one; ten tosses can't do more."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(cpr), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(cpo), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
