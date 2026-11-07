from __future__ import annotations

import numpy as np

from videos.stats.stats8.common import *  # noqa: F403

ITEMS = [("mean", r"mean height", S.EST, "{:.1f}"), ("sd", r"SD of height", S.LIK, "{:.2f}"),
         ("median", r"median income", S.POST, "{:,.0f}"), ("iqr", r"IQR of income", S.PRIOR, "{:,.0f}"),
         ("corr", r"father--son $r$", S.ACCENT, "{:.3f}")]


class PlugIn(VoiceoverScene):
    def construct(self):
        self.card()
        self.functional()
        self.paths()
        self.fisherz()
        self.consistent()
        self.maximum()
        self.bootstrap()

    def card(self):
        card = chapter_card(8, r"Consistency and plug-in", r"Estimate a population feature by the same feature of the sample", part=PART)
        with self.voiceover("Chapter eight. Consistency, and the plug-in principle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def functional(self):
        rows = [
            cmath(r"\theta", r"=", r"T(F)", r"\qquad \text{a feature of the population's distribution}", font_size=32),
            cmath(r"\hat\theta", r"=", r"T(\hat F_n)", r"\qquad \hat F_n \text{: the sample's ECDF (Part 1)}", font_size=32),
            cmath(r"\int x\,dF \ \to\ \bar x,\quad F^{-1}(\tfrac12)", r"\ \to\ ", r"\text{sample median}", font_size=30),
            cmath(r"\int (x - \mu)^2 dF", r"\ \to\ ", r"\tfrac1n \textstyle\sum (x_i - \bar x)^2", font_size=30),
        ]
        rows[1][2].set_color(SIM)
        whys = [why(r"a statistical functional"), why(r"plug in the empirical distribution"), why(r"these summaries follow the plug-in principle"),
                why(r"the variance, \ with divisor $n$")]
        note_ = label(r"(the plug-in variance divides by $n$: \ chapter 2's small bias, \ which vanishes as $n$ grows)", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.8)
        intro = label('Apply a population summary to the empirical distribution', font_size=36)
        with self.voiceover(
            "How do we invent estimators in the first place? The simplest answer is a principle. <bookmark mark='a'/> "
            "Most quantities we care about are features of the population's distribution: its mean, its median, its "
            "spread, a correlation. Write the feature as T of F. <bookmark mark='b'/> Then estimate it by the same "
            "feature of the sample's own distribution, the empirical CDF of Part 1: T of F hat. "
            "<bookmark mark='c'/> The population mean becomes the sample mean; the population median, the sample "
            "median; the variance, the average squared deviation, with divisor n, and so a small bias that disappears "
            "as n grows."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.6, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            step(3, transform=False)
            self.play(FadeIn(note_))
        self.clear_scene()

    def paths(self):
        d = load("plugin")
        ns = np.asarray(d["ns"], float)
        panels = VGroup()
        for k, (key, nm, c, fmt) in enumerate(ITEMS):
            p = np.asarray(d["paths"][key])
            tr = d["truth"][key]
            dev = (p - tr) / abs(tr) if key != "corr" else (p - tr)
            lim = 0.5 if key != "corr" else 0.5
            A = axes([1, 4], [-lim, lim], x_length=3.6, y_length=1.9, xticks=[1, 2, 3, 4], yticks=[-lim, 0, lim],
                     xfmt=lambda v: f"10^{{{int(v)}}}", center=[-4.4 + 4.4 * (k % 3), 1.3 - 3.0 * (k // 3), 0], font_size=16)
            zero = DashedLine(A.ax.c2p(1, 0), A.ax.c2p(4, 0), color=EXACT, stroke_width=1.5)
            ln = polyline(A.ax, np.log10(ns), dev, c, 2.5)
            t = label(nm, font_size=22, color=c).next_to(A, UP, buff=0.08)
            panels.add(VGroup(A, zero, ln, t))
        side = fit_rows(VGroup(
            label(r"relative error of the plug-in estimate \ (difference, for $r$)", font_size=20, color=GREY_A),
            label(r"one sample from the World, \ growing from 10 to 10,000", font_size=20, color=GREY_A),
            label(r"finite paths approach zero; \ consistency is an asymptotic property", font_size=22, color=S.ACCENT),
        ), 3.8, 0.2, [4.4, -1.7, 0])
        tag = simulated_tag()
        intro = label('Follow estimates as the sample grows', font_size=36)
        with self.voiceover(
            "Plug-in estimators are consistent, under mild conditions. <bookmark mark='a'/> Take one sample from the "
            "World and let it grow from ten people to ten thousand, recomputing five estimates as it grows: the mean and "
            "standard deviation of height, the median and interquartile range of income, and the father–son "
            "correlation. Each panel shows the error, relative to the truth. <bookmark mark='b'/> Every path wanders "
            "early and settles on zero: the estimates converge to the population values. The empirical CDF converges "
            "to the true CDF, uniformly, by the Glivenko–Cantelli theorem of Part 48, and a feature continuous in the relevant topology follows it. Means and variances also require moment control; quantiles require uniqueness and continuity. It is not true that every feature follows merely from "
            "uniform CDF convergence."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(*[FadeIn(p[0]) for p in panels], *[FadeIn(p[3]) for p in panels], *[Create(p[1]) for p in panels])
            vo.wait_until("b")
            self.play(*[Create(p[2]) for p in panels], FadeIn(side), run_time=3.0)
        self.clear_scene()

    def consistent(self):
        rows = fit_rows(VGroup(
            label(r"consistent: \ $\hat\theta_n \to \theta$ in probability (Part 6)", font_size=26),
            label(r"unbiased and consistent are different things:", font_size=26, color=S.ACCENT),
            MathTex(r"\tfrac1n\textstyle\sum(x_i - \bar x)^2:\ \text{biased, consistent}", font_size=28),
            MathTex(r"x_1 \text{ alone}:\ \text{unbiased for } \mu,\ \text{not consistent}", font_size=28),
            label(r"consistency is the least we ask; \ Part 9 asks how fast, \ and how efficiently", font_size=24, color=GREY_A),
        ), 12.6, 0.38, [0, 0.2, 0])
        intro = label('Unbiasedness and consistency are different properties', font_size=36)
        with self.voiceover(
            "<bookmark mark='a'/> An estimator that converges in probability to the truth is called consistent. "
            "<bookmark mark='b'/> Notice that this is a different property from unbiasedness. <bookmark mark='c'/> The "
            "plug-in variance is biased for every finite n, yet consistent. <bookmark mark='d'/> The first observation "
            "alone is an unbiased estimate of the mean, yet it never improves, however much data you collect, so it is "
            "not consistent. <bookmark mark='e'/> Consistency is the least we should ask of an estimator. Part 9 asks "
            "how fast it converges, and whether any estimator could do better."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def maximum(self):
        d = load("extras")["maximum"]
        ed = np.asarray(d["edges"])
        A = axes([500, 1000], [0, 0.012], x_length=6.2, y_length=4.2, xlabel=r"the largest of 10 serial numbers, \ $1, \dots, 1000$",
                 xticks=[500, 600, 700, 800, 900, 1000], yticks=[0, 0.005, 0.01], center=[-3.0, -0.4, 0])
        ax = A.ax
        h = hist_bars(ax, ed, np.asarray(d["hist"]), color=SIM, opacity=0.7)
        tr = DashedLine(ax.c2p(1000, 0), ax.c2p(1000, 0.012), color=EXACT, stroke_width=2.5)
        avg = DashedLine(ax.c2p(d["mean_max"], 0), ax.c2p(d["mean_max"], 0.012), color=RESID, stroke_width=2.5)
        rows = fit_rows(VGroup(
            label(r"plug-in for $N$: \ the sample maximum", font_size=24),
            MathTex(rf"E\max = \frac{{n}}{{n + 1}}(N + 1) = {d['theory']:.0f}", font_size=28, color=RESID),
            label(r"never above $N$; \ downward biased", font_size=24, color=GREY_A),
            MathTex(rf"\max \cdot \Big(1 + \frac1n\Big) - 1:\ \text{{average }} {d['fixed_mean']:.0f}", font_size=28, color=EXACT),
            label(r"the German tank problem: \ Part 9", font_size=24, color=S.ACCENT),
        ), 5.0, 0.3, [3.9, 0.2, 0])
        tag = simulated_tag(r"simulated: 20,000 samples of 10")
        with self.voiceover(
            "Plug-in has its limits. <bookmark mark='a'/> Suppose objects carry serial numbers one to N, and we see ten "
            "of them at random. To estimate N, the plug-in answer is the largest serial number in the sample. "
            "<bookmark mark='b'/> It can equal the endpoint but can never exceed the true maximum, and on "
            "average, with ten serials out of a thousand, it's nine hundred and ten. <bookmark mark='c'/> A small "
            "correction, scaling up by one plus one over n and subtracting one, is exactly unbiased under simple random sampling without replacement. Where "
            "that correction comes from, and why it's the best possible, is the opening story of Part 9: the German "
            "tank problem."
        ) as vo:
            self.play(FadeIn(A), Create(tr), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(h, lag_ratio=0.02), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(avg), FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def fisherz(self):
        d = load("extras2")["fisherz"]
        A = axes([-0.2, 1], [0, 4.3], x_length=5.2, y_length=3.8, xlabel=r"$r$, \ samples of 10, \ $\rho = 0.8$", xticks=[0, 0.5, 1],
                 yticks=[0, 1, 2, 3, 4], center=[-3.6, -0.4, 0])
        h1 = hist_bars(A.ax, np.asarray(d["r_edges"]), np.asarray(d["r_hist"]), color=S.ACCENT, opacity=0.7)
        B = axes([-0.4, 2.4], [0, 1.2], x_length=5.2, y_length=3.8, xlabel=r"$z = \tanh^{-1} r$", xticks=[0, 1, 2], yticks=[0, 0.5, 1],
                 center=[2.6, -0.4, 0])
        h2 = hist_bars(B.ax, np.asarray(d["z_edges"]), np.asarray(d["z_hist"]), color=SIM, opacity=0.7)
        zz = np.linspace(-0.4, 2.4, 200)
        nrm = curve(B.ax, zz, normal_pdf_(zz, d["atanh_rho"], d["z_sd_theory"]), EXACT, 3)
        rows = VGroup(
            MathTex(rf"\text{{skewness}}\ {d['r_skew']:.2f}", font_size=26, color=S.ACCENT).next_to(A, UP, buff=0.15),
            MathTex(rf"\text{{skewness}}\ {d['z_skew']:.2f},\ \ \mathrm{{SD}}\ {d['z_sd']:.3f} \approx \tfrac{{1}}{{\sqrt{{n - 3}}}} = {d['z_sd_theory']:.3f}",
                    font_size=24, color=SIM).next_to(B, UP, buff=0.15))
        foot = label(r"Fisher (1915, 1921): \ a transformation that approximately normal for bivariate-normal data; \ SE $\approx1/\sqrt{n-3}$", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.3)
        tag = note(r"simulated: 20,000 samples").to_corner(UR, buff=0.25)
        with self.voiceover(
            "Plug-in estimates can have awkward sampling distributions, and sometimes a transformation tames them. "
            "<bookmark mark='a'/> The sample correlation, with ten independent bivariate-normal pairs whose correlation is point "
            "eight, is squeezed against its ceiling of one and badly skewed. <bookmark mark='b'/> Fisher's 1915 paper, the "
            "one that introduced his geometry, found the cure: take the inverse hyperbolic tangent. The transformed "
            "values are approximately normal, with an approximate standard deviation of one over root n minus three; finite-sample bias and accuracy still depend on the true "
            "correlation. Intervals are built on that scale and transformed back."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(h1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(h2), Create(nrm), FadeIn(rows[1]), FadeIn(foot))
        self.clear_scene()

    def bootstrap(self):
        rows = fit_rows(VGroup(
            label(r"plug-in, \ one level up:", font_size=28, color=S.ACCENT),
            MathTex(r"\mathrm{SE}_F(\hat\theta) \ \text{depends on the unknown } F", font_size=30),
            MathTex(r"\Rightarrow\ \text{estimate it by } \mathrm{SE}_{\hat F_n}(\hat\theta)", font_size=30, color=SIM),
            label(r"compute it by simulation: \ resample the data with replacement (Part 7's inverted ECDF), \ recompute, \ repeat",
                  font_size=24, color=GREY_A),
            label(r"Efron's bootstrap (1979): \ a resampling standard error under regularity conditions \ \textemdash{} \ Part 16", font_size=26, color=S.ACCENT),
        ), 12.6, 0.36, [0, 0.2, 0])
        intro = label('Estimate sampling uncertainty by resampling', font_size=36)
        with self.voiceover(
            "The plug-in principle has a second, more powerful use. <bookmark mark='a'/> Apply it one level up. "
            "<bookmark mark='b'/> The standard error of any estimator is itself a feature of the unknown population. "
            "<bookmark mark='c'/> So estimate it by the same feature of the sample's distribution. <bookmark mark='d'/> "
            "There's rarely a formula, but there's always a simulation: draw new samples from the data itself, with "
            "replacement, recompute the estimator each time, and measure the spread. <bookmark mark='e'/> That is "
            "Bradley Efron's bootstrap of 1979, a resampling standard error under regularity conditions, and the subject of Part 16."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
