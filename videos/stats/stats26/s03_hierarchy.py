from __future__ import annotations

import numpy as np

from videos.stats.stats26.common import *  # noqa: F403


class Hierarchy(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.marginal()
        self.explorer()
        self.draws()
        self.summaries()
        self.questions()
        self.vs_eb()

    def card(self):
        card = chapter_card(2, r"Hierarchical models", r"The eight schools on a grid", lit=(1981,), part=PART)
        with self.voiceover("Chapter two. Hierarchical models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def model(self):
        rows = [
            cmath(r"y_j \mid \theta_j", r"\sim", r"N(\theta_j, \sigma_j^2), \ \ \sigma_j \text{ known}", font_size=30),
            cmath(r"\theta_j \mid \mu, \tau", r"\sim", r"N(\mu, \tau^2)", font_size=30),
            cmath(r"p(\mu, \tau)", r"\propto", r"1, \ \ \tau > 0", font_size=30),
            cmath(r"p(\theta, \mu, \tau \mid y)", r"\propto", r"p(\mu, \tau) \textstyle\prod_j N(\theta_j \mid \mu, \tau^2) N(y_j \mid \theta_j, \sigma_j^2)", font_size=26),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"each school's experiment"), why(r"the population of coaching effects"),
                why(r"flat hyperprior: \ chapter three asks if that is wise"), why(r"ten unknowns, \ one posterior")]
        with self.voiceover(
            "<bookmark mark='a'/> The model has three levels. Each school's estimate is its true effect plus noise of known "
            "size. <bookmark mark='b'/> The true effects come from a normal population with mean mu and spread tau. "
            "<bookmark mark='c'/> And mu and tau get a prior, here flat, a choice chapter three examines. "
            "<bookmark mark='d'/> Bayes's rule then gives one joint posterior for all ten unknowns: eight effects, a mean "
            "and a spread."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def marginal(self):
        rows = [
            cmath(r"p(\theta, \mu, \tau \mid y)", r"=", r"p(\tau \mid y)\, p(\mu \mid \tau, y)\, p(\theta \mid \mu, \tau, y)", font_size=28),
            cmath(r"p(\tau \mid y)", r"\propto", r"p(\tau)\, V_\mu^{1/2} \textstyle\prod_j (\sigma_j^2 + \tau^2)^{-1/2} e^{-(y_j - \hat\mu)^2/2(\sigma_j^2 + \tau^2)}", font_size=26),
            cmath(r"\mu \mid \tau, y", r"\sim", r"N(\hat\mu_\tau, V_\mu), \ \ \hat\mu_\tau = \tfrac{\sum y_j/(\sigma_j^2 + \tau^2)}{\sum 1/(\sigma_j^2 + \tau^2)}", font_size=26),
            cmath(r"\theta_j \mid \mu, \tau, y", r"\sim", r"N\Bigl(\tfrac{y_j/\sigma_j^2 + \mu/\tau^2}{1/\sigma_j^2 + 1/\tau^2}, \ \tfrac{1}{1/\sigma_j^2 + 1/\tau^2}\Bigr)", font_size=26),
        ]
        rows[1][2].set_color(POST)
        whys = [why(r"factor the posterior"), why(r"one dimension: \ a grid"), why(r"normal, \ given $\tau$"),
                why(r"Part 15's normal update, \ school by school")]
        with self.voiceover(
            "<bookmark mark='a'/> Ten dimensions sound hard, but the posterior factors. <bookmark mark='b'/> Integrating out "
            "the effects and the mean leaves a one-dimensional posterior for tau, which a grid of four thousand points "
            "computes exactly. <bookmark mark='c'/> Given tau, the mean is normal, centred at a precision-weighted average "
            "of the schools. <bookmark mark='d'/> Given both, each school's effect is Part 15's normal update: a weighted "
            "average of its own estimate and the population mean. Draw tau, then mu, then the effects, and we have exact "
            "draws from the full posterior, no Markov chain needed."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def explorer(self):
        d = load("schools")
        T = TauExplorer(d["tau"], d["cond_mean"], d["post_tau"], d["labels"], tau_max=30.0, width=7.6, center=[-1.3, -0.2, 0],
                        y_range=(-5, 30), colors=SCHOOL)
        tr = ValueTracker(0.0)
        cursor = always_redraw(lambda: T.line_at(tr.get_value()))
        dots = always_redraw(lambda: T.dots_at(tr.get_value()))
        rows = fit_rows(VGroup(
            label(r"top: \ each school's estimate, \ given $\tau$", font_size=22),
            label(r"$\tau = 0$: \ all at the pooled 7.7", font_size=22, color=POOLED),
            label(r"$\tau$ large: \ each back to its own $y_j$", font_size=22, color=RAW),
            label(r"bottom: \ how plausible each $\tau$ is", font_size=22, color=POST),
            label(rf"median $\tau$ {d['tau_med']:.1f}; \ 95\%: \ [{d['tau_lo']:.1f}, {d['tau_hi']:.1f}]", font_size=22, color=POST),
        ), 3.4, 0.42, [5.3, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> This is the tau explorer. The top panel shows each school's estimate given tau. "
            "<bookmark mark='b'/> At tau equal to zero, every school sits at the pooled mean, seven point seven. "
            "<bookmark mark='c'/> As tau grows, each school is trusted more, and the lines fan out towards the schools' own "
            "estimates: A's climbs towards twenty-eight. <bookmark mark='d'/> The bottom panel is the posterior for tau. "
            "It is highest at zero and falls slowly: the data can't rule out identical schools, but can't rule out "
            "differences of fifteen or twenty points either. <bookmark mark='e'/> Its median is five, and its ninety-five "
            "percent interval runs from nearly zero to twenty. The Bayesian answer averages the top panel over the bottom "
            "one."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(T.top), FadeIn(T.bottom))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in T.curves], lag_ratio=0.1), FadeIn(T.names), FadeIn(rows[0]), run_time=2.5)
            self.add(cursor, dots)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(tr.animate.set_value(28.0), FadeIn(rows[2]), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(T.area), Create(T.density), FadeIn(rows[3]))
            self.play(tr.animate.set_value(d["tau_med"]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def summaries(self):
        d = load("schools")
        y, lab = np.asarray(d["y"]), d["labels"]
        lo, hi, med = np.asarray(d["theta_lo"]), np.asarray(d["theta_hi"]), np.asarray(d["theta_med"])
        A = axes([-0.6, 7.6], [-35, 60], x_length=7.6, y_length=4.8, xlabel=r"school", ylabel=r"effect, \ SAT points",
                 xticks=[], yticks=[-20, 0, 20, 40], center=[-1.8, 0.2, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(-0.6, 0), ax.c2p(7.6, 0), color=GREY_C, stroke_width=1.5)
        raw = VGroup(*[Dot(ax.c2p(j - 0.15, v), radius=0.07, color=RAW) for j, v in enumerate(y)])
        post = VGroup(*[VGroup(Line(ax.c2p(j + 0.15, a), ax.c2p(j + 0.15, b), color=SHRUNK, stroke_width=4),
                               Dot(ax.c2p(j + 0.15, m), radius=0.08, color=SHRUNK)) for j, (a, b, m) in enumerate(zip(lo, hi, med))])
        names = VGroup(*[label(lab[j], font_size=22, color=SCHOOL[j]).next_to(ax.c2p(j, -35), DOWN, buff=0.15) for j in range(8)])
        mu = DashedLine(ax.c2p(-0.6, d["mu_mean"]), ax.c2p(7.6, d["mu_mean"]), color=POOLED, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"blue: \ each school's own estimate", font_size=22, color=RAW),
            label(r"green: \ posterior median and 95\% interval", font_size=22, color=SHRUNK),
            label(rf"A: \ 28 $\to$ {med[0]:.1f}, \ [{lo[0]:.0f}, {hi[0]:.0f}]", font_size=22, color=SCHOOL[0]),
            label(rf"C: \ $-3$ $\to$ {med[2]:.1f}", font_size=22, color=SCHOOL[2]),
            label(rf"teal: \ $\mu$, \ mean {d['mu_mean']:.1f}", font_size=22, color=POOLED),
        ), 3.3, 0.42, [5.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The result, school by school. In blue, each school's own estimate. "
            "<bookmark mark='b'/> In green, its posterior median and ninety-five percent interval. <bookmark mark='c'/> "
            "School A's twenty-eight becomes ten, with an interval from minus two to thirty-one: probably a positive effect, "
            "probably much smaller than its own experiment suggested. <bookmark mark='d'/> C's minus three becomes six and a "
            "half. <bookmark mark='e'/> All are pulled towards the population mean of about eight: further than no pooling "
            "allows, not as far as complete pooling forces."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(A), Create(zero), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in raw], lag_ratio=0.1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in post], lag_ratio=0.1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(post[0], scale_factor=1.3), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Indicate(post[2], scale_factor=1.3), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Create(mu), FadeIn(rows[4]))
        self.clear_scene()

    def questions(self):
        d = load("schools")
        best = np.asarray(d["p_best"])
        A = axes([-0.6, 7.6], [0, 0.3], x_length=7.6, y_length=4.2, xlabel=r"school", ylabel=r"P(this school's effect is the largest)",
                 xticks=[], yticks=[0, 0.1, 0.2, 0.3], center=[-1.6, 0.3, 0])
        ax = A.ax
        bars = bars_at(ax, list(range(8)), best, 0.6, SHRUNK, 0.85)
        for j, b in enumerate(bars):
            b.set_fill(SCHOOL[j])
        names = VGroup(*[label(d["labels"][j], font_size=22, color=SCHOOL[j]).next_to(ax.c2p(j, 0), DOWN, buff=0.15) for j in range(8)])
        even = DashedLine(ax.c2p(-0.6, 1 / 8), ax.c2p(7.6, 1 / 8), color=GREY_B, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(r"any question, \ from the same draws", font_size=22),
            label(rf"P(A's effect $>$ C's) $= {d['p_A_gt_C']:.2f}$", font_size=22, color=SCHOOL[0]),
            label(rf"P(A is the best school) $= {best[0]:.2f}$", font_size=22, color=SCHOOL[0]),
            label(r"dashed: \ 1 in 8, \ no information", font_size=22, color=GREY_B),
        ), 4.0, 0.42, [4.9, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The posterior draws answer any question directly, with no new theory. "
            "<bookmark mark='b'/> The probability that coaching helped more at A than at C is point six eight: suggestive, "
            "far from certain. <bookmark mark='c'/> The probability that A had the largest effect of all eight is a quarter. "
            "<bookmark mark='d'/> If we knew nothing it would be one in eight; the data have doubled it, no more. Rankings "
            "of noisy units, Part 25's league tables, come out of the posterior honestly."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(even), FadeIn(rows[3]))
        self.clear_scene()

    def vs_eb(self):
        rows = fit_rows(VGroup(
            label(r"empirical Bayes: \ plug in $\hat\tau$; \ here $\hat\tau = 0$, \ so complete pooling", font_size=24, color=POOLED),
            label(r"full Bayes: \ average over $p(\tau \mid y)$, \ which leaves room for $\tau = 15$", font_size=24, color=SHRUNK),
            label(r"the difference matters when the groups are few", font_size=24, color=RES),
            label(r"with 400 schools, \ $p(\tau \mid y)$ is narrow and the two agree", font_size=24, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Compare Part 25. Empirical Bayes plugs in an estimate of tau; here the estimate is zero, "
            "so every school would be told seven point seven, with intervals far too narrow. <bookmark mark='b'/> Full "
            "Bayes averages over tau's posterior, which still gives real weight to differences of fifteen points, and "
            "widens the intervals accordingly. <bookmark mark='c'/> With eight groups the difference is large. "
            "<bookmark mark='d'/> With Part 25's four hundred schools, tau's posterior is narrow and the two approaches "
            "agree."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def draws(self):
        d = load("schools")
        th, tau = np.asarray(d["draws_theta"]), np.asarray(d["draws_tau"])
        A = axes([-0.6, 7.6], [-25, 50], x_length=7.6, y_length=4.6, xlabel=r"school", ylabel=r"a posterior draw of $\theta_j$",
                 xticks=[], yticks=[-20, 0, 20, 40], center=[-1.8, 0.2, 0])
        ax = A.ax
        names = VGroup(*[label(d["labels"][j], font_size=22, color=SCHOOL[j]).next_to(ax.c2p(j, -25), DOWN, buff=0.15) for j in range(8)])
        order = np.argsort(tau)
        lines = VGroup()
        for i in list(order[:6]) + list(order[-6:]):
            col = interpolate_color(ManimColor(POOLED), ManimColor(RAW), min(tau[i] / 15, 1))
            lines.add(VGroup(polyline(ax, np.arange(8), th[i], col, 1.8, 0.85),
                             *[Dot(ax.c2p(j, v), radius=0.04, color=col) for j, v in enumerate(th[i])]))
        rows = fit_rows(VGroup(
            label(r"twelve exact draws of all eight effects", font_size=22),
            label(r"teal: \ draws with small $\tau$: \ nearly flat", font_size=22, color=POOLED),
            label(r"blue: \ large $\tau$: \ the schools differ", font_size=22, color=RAW),
            label(r"the posterior is all of them at once", font_size=22, color=SHRUNK),
        ), 3.3, 0.42, [5.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What does a draw from this posterior look like? Each line is one exact draw of all eight "
            "effects together, coloured by its value of tau. <bookmark mark='b'/> Draws with small tau are nearly flat: in "
            "those worlds the schools barely differ. <bookmark mark='c'/> Draws with large tau zigzag: in those worlds "
            "coaching worked very differently from school to school. <bookmark mark='d'/> The posterior is the whole "
            "collection, and every summary that follows is a summary of draws like these."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines[:6]], lag_ratio=0.2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(l_) for l_ in lines[6:]], lag_ratio=0.2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
