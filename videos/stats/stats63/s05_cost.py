from __future__ import annotations

import numpy as np

from videos.stats.stats63.common import *  # noqa: F403


class Cost(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter four. The cost of privacy, measured as a minimax rate.", 4,
                            r"The cost of privacy", r"Minimax rates with a budget", lit=(2013,))
        self.central()
        self.local()
        self.chart()
        self.dims()
        self.lower()
        self.lessons()

    def central(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Start with the simplest problem: estimate a proportion p from n people's bits. "
            "<bookmark mark='b'/> In the central model a trusted curator holds the data and adds Laplace noise to the count. "
            "<bookmark mark='c'/> The mean squared error is the sampling variance, p times one minus p over n, plus the "
            "noise's variance, two over n epsilon squared. <bookmark mark='d'/> The privacy term falls like one over n "
            "squared, faster than sampling error. For large samples, central privacy is nearly free.",
            [(r"\text{task}", r":", r"\text{estimate } p \text{ from } n \text{ bits}", 40),
             (r"\text{central}", r":", r"\hat p = (\textstyle\sum x_i + \mathrm{Lap}(1/\varepsilon)) / n", 40),
             (r"\mathrm{MSE}", r"=", r"\frac{p(1 - p)}{n} + \frac{2}{(n\varepsilon)^2}", 40),
             (r"\text{privacy's share}", r":", r"O(1/n^2) \ \ \text{vs} \ \ O(1/n)", 40)],
            [r"a proportion", r"a trusted curator", r"exact", r"nearly free"],
            colors=[(2, OKC)])

    def local(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> In the local model there is no trusted curator: each person randomizes their own bit "
            "before sending it, by randomized response. Apple and Google have used local privacy for usage statistics. "
            "<bookmark mark='b'/> The estimator from chapter one has variance about one over n times the factor e to the "
            "epsilon over e to the epsilon minus one, squared. <bookmark mark='c'/> For small epsilon that is one over n "
            "epsilon squared: the noise is now order one over n, the same order as sampling error, multiplied by a large "
            "constant. <bookmark mark='d'/> John Duchi, Michael Jordan and Martin Wainwright proved in 2013 that this is "
            "unavoidable: under local privacy, the minimax rates of whole families of problems are those of a sample of size "
            "n epsilon squared.",
            [(r"\text{local}", r":", r"\text{each person randomizes}", 40),
             (r"\mathrm{MSE}", r"\approx", r"\frac{1}{n} \cdot \frac{e^{\varepsilon}}{(e^{\varepsilon} - 1)^2}", 40),
             (r"\text{small } \varepsilon", r":", r"\text{about } 1/(n\varepsilon^2)", 40),
             (r"\text{effective sample}", r":", r"n \ \to \ n\varepsilon^2", 40)],
            [r"no trusted curator", r"randomized response", r"same order as sampling", r"Duchi, \ Jordan \& Wainwright (2013)"],
            colors=[(3, BADC)])

    def chart(self):
        d = load("cost")
        rows = d["rows"]
        ns = np.log10([r["n"] for r in rows])
        A = axes([1.9, 4.1], [-5.0, -1.6], x_length=7.2, y_length=4.4, xlabel=r"sample size $n$ (log scale)",
                 ylabel=r"mean squared error of $\hat p$ (log scale)", xticks=[2, 3, 4], xfmt=lambda v: f"10^{{{int(v)}}}",
                 yticks=[-5, -4, -3, -2], yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.4, 0.2, 0])
        ax = A.ax

        def line(key, color, dash=False):
            ys = np.log10([r[key] for r in rows])
            pl = polyline(ax, ns, ys, color, 3.5)
            if dash:
                pl = DashedVMobject(pl, num_dashes=30)
            return VGroup(pl, *[Dot(ax.c2p(a, b), radius=0.07, color=color) for a, b in zip(ns, ys)])
        samp, cen, loc = line("sampling", GREY_B, True), line("central", OKC), line("local", BADC)
        r0, r1 = rows[0], rows[-1]
        side = side_groups([
            [(rf"$p = {d['p']}$, \ $\varepsilon = {d['eps']:g}$, \ 20{{,}}000 runs per $n$", WHITE)],
            [(r"grey dashes: \ no privacy, \ $p(1-p)/n$", GREY_B)],
            [(r"green: \ central Laplace", OKC), (rf"exactly {100 * (r0['central_exact'] / r0['sampling'] - 1):.1f}\% above at $n = 100$", OKC),
             (rf"{100 * (r1['central_exact'] / r1['sampling'] - 1):.1f}\% above at $n = 10{{,}}000$", OKC)],
            [(r"red: \ local randomized response", BADC), (rf"about {r1['local'] / r1['central']:.0f} times the central error", BADC),
             (r"at every $n$", BADC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> Simulated, with p of {d['p']} and epsilon of one, twenty thousand runs at each sample size, on "
            f"log scales. <bookmark mark='b'/> The grey dashed line is the error without privacy. <bookmark mark='c'/> The "
            f"central Laplace estimator sits just above it, and the gap closes as n grows, because the noise term falls like "
            f"one over n squared. <bookmark mark='d'/> Local randomized response runs parallel, about "
            f"{r1['local'] / r1['central']:.0f} times the central error at every sample size. In effect, every five people "
            f"count as one. A parallel line on a log-log plot is a constant factor that no amount of data removes."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(samp[0]), FadeIn(VGroup(*samp[1:])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cen[0]), FadeIn(VGroup(*cen[1:])), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(loc[0]), FadeIn(VGroup(*loc[1:])), FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def dims(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> In more dimensions the price grows. <bookmark mark='b'/> T. Tony Cai, Yichen Wang and "
            "Linjun Zhang found in 2021 the minimax rate for estimating a d-dimensional mean under central epsilon-delta "
            "privacy: d over n, the usual rate, plus d squared log one over delta over n squared epsilon squared. <bookmark "
            "mark='c'/> The privacy term dominates until n exceeds about d times the square root of log one over delta, over "
            "epsilon. With d of a thousand, epsilon of one and delta of ten to the minus five, that is about 3,400 people. <bookmark mark='d'/> They "
            "called it the cost of privacy, and found matching rates for linear regression, with the private estimator built "
            "from noisy, clipped gradient steps, the method of chapter seven.",
            [(r"\text{mean in } d \text{ dims}", r":", r"\frac{d}{n} + \frac{d^2 \log(1/\delta)}{n^2\varepsilon^2}", 40),
             (r"\text{privacy dominates until}", r"\ ", r"n \gtrsim d\sqrt{\log(1/\delta)}/\varepsilon", 40),
             (r"d = 1000, \ \varepsilon = 1", r":", r"n \approx 3{,}400", 40),
             (r"\text{regression}", r":", r"\text{noisy clipped gradients}", 40)],
            [r"Cai, \ Wang \& Zhang (2021)", r"the crossover", r"$\delta = 10^{-5}$", r"chapter 7"],
            colors=[(0, OKC), (1, BADC)])

    def lower(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The lower bounds use Part fifty's machinery, with one new ingredient. <bookmark "
            "mark='b'/> Under local privacy, two input distributions that are close in total variation produce output "
            "distributions whose Kullback-Leibler divergence is at most a constant times e to the epsilon minus one, squared, "
            "times their total variation squared. A strong data-processing inequality: the privatizing channel contracts "
            "information. <bookmark mark='c'/> Feed that into Le Cam's two-point method or Fano's inequality, and n is "
            "replaced by n times e to the epsilon minus one, squared. <bookmark mark='d'/> Under central privacy the tool is a "
            "coupling argument, or tracing attacks, which show that an accurate estimator must reveal who was in the sample: "
            "accuracy beyond the rate would let an attacker win the test of chapter two.",
            [(r"\text{local channel}", r":", r"\mathrm{KL}(M_P \| M_Q) \le 4(e^{\varepsilon} - 1)^2 \, \mathrm{TV}(P, Q)^2", 36),
             (r"\text{strong DPI}", r":", r"\text{privacy contracts information}", 40),
             (r"\text{Le Cam, \ Fano}", r":", r"n \ \to \ n(e^{\varepsilon} - 1)^2", 40),
             (r"\text{central}", r":", r"\text{tracing attacks}", 40)],
            [r"Duchi et al. (2013)", r"a contraction", r"Part 50", r"Cai, \ Wang \& Zhang (2021)"],
            colors=[(0, PRIVC)])

    def lessons(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The lessons. <bookmark mark='b'/> Central privacy is cheap for large populations and "
            "simple statistics: its cost is second order. <bookmark mark='c'/> It is expensive for small groups, many "
            "statistics, or high dimensions, where the second-order term is not small. A census block of five people is a "
            "small sample, however large the country. <bookmark mark='d'/> Local privacy, which needs no trust, costs a "
            "constant factor at every sample size, so it suits only enormous populations and simple questions.",
            [(r"\text{central, \ large } n", r":", r"\text{second order}", 40),
             (r"\text{small groups, \ high } d", r":", r"\text{expensive}", 40),
             (r"\text{a block of five}", r":", r"\text{a small sample}", 40),
             (r"\text{local}", r":", r"\text{a constant factor, \ always}", 40)],
            [r"cheap", r"not cheap", r"chapter 6", r"trust is worth data"],
            colors=[(0, OKC), (1, BADC), (3, BADC)])
