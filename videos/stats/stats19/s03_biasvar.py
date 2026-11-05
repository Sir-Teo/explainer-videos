from __future__ import annotations

import numpy as np

from videos.stats.stats19.common import *  # noqa: F403


class BiasVariance(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.darts()
        self.knn_formulas()
        self.simulation()
        self.smoothers()
        self.lessons()

    def card(self):
        card = chapter_card(2, r"Bias and variance", r"Where the U comes from", part=PART)
        with self.voiceover("Chapter two. Bias and variance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def derive(self):
        rows = [
            cmath(r"E\big[(Y - \hat f(x_0))^2\big]", r"=", r"\sigma^2 + E\big[(f(x_0) - \hat f(x_0))^2\big]", font_size=30),
            cmath(r"\ ", r"=", r"\sigma^2 + \big(E\hat f(x_0) - f(x_0)\big)^2 + \mathrm{Var}\,\hat f(x_0)", font_size=30),
            cmath(r"\ ", r"=", r"\text{noise} + \text{bias}^2 + \text{variance}", font_size=32),
            cmath(r"\text{flexibility}", r":", r"\text{bias} \downarrow,\ \ \text{variance} \uparrow", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"chapter one: \ noise plus distance"), why(r"add and subtract $E\hat f$; \ the cross term is zero"),
                why(r"over training sets, \ at a fixed $x_0$"), why(r"the U is their sum")]
        with self.voiceover(
            "<bookmark mark='a'/> Start from chapter one: the expected test error at a point is the noise plus the expected "
            "squared distance between the rule and the truth. Here the expectation is over everything random, including the "
            "training set. <bookmark mark='b'/> Add and subtract the rule's average over training sets. The cross term "
            "vanishes, as in Part 9's mean squared error, <bookmark mark='c'/> and the error splits into three: noise, squared "
            "bias, and variance. Bias is how far the rule is from the truth on average; variance, how much it changes from "
            "one training set to another. <bookmark mark='d'/> Flexibility trades one for the other: a flexible rule has low "
            "bias and high variance, a stiff one the reverse. The U of chapter one is their sum."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def darts(self):
        g = np.random.Generator(np.random.PCG64(1992))
        boards = VGroup()
        specs = [(0.0, 0.15, r"low bias, \ low variance", HIT), (0.0, 0.5, r"low bias, \ high variance", OBS),
                 (0.55, 0.15, r"high bias, \ low variance", S.ALT), (0.55, 0.5, r"high bias, \ high variance", RES)]
        for k, (b, s, nm, col) in enumerate(specs):
            c = np.array([-4.5 + 3.0 * k, 0.4, 0])
            rings = VGroup(*[Circle(radius=r, color=GREY_C, stroke_width=1.5).move_to(c) for r in (0.4, 0.8, 1.2)])
            bull = Dot(c, radius=0.06, color=S.TRUTH)
            pts = g.normal(0, s, (12, 2)) + np.array([b, b * 0.6])
            darts = VGroup(*[Dot(c + np.array([p[0], p[1], 0]), radius=0.06, color=col) for p in pts])
            lab = label(nm, font_size=20, color=col).next_to(rings, DOWN, buff=0.25)
            boards.add(VGroup(rings, bull, darts, lab))
        foot = label(r"each dart: \ the rule fitted to one training set", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The usual picture is a dartboard, where each dart is the prediction at one point from a rule fitted to a different "
            "training set, and the bullseye is the truth. <bookmark mark='a'/> Low bias and low variance: a tight cluster on "
            "the bullseye. <bookmark mark='b'/> Low bias, high variance: centred on the bullseye, but scattered. "
            "<bookmark mark='c'/> High bias, low variance: tightly grouped, in the wrong place. <bookmark mark='d'/> And both "
            "at once. <bookmark mark='e'/> We never see the darts in practice, only one of them; that's what makes the trade-off "
            "hard to manage."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                b_ = boards[k]
                self.play(FadeIn(b_[0]), FadeIn(b_[1]), FadeIn(b_[3]), LaggedStart(*[FadeIn(x, scale=1.6) for x in b_[2]], lag_ratio=0.08))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def knn_formulas(self):
        rows = [
            cmath(r"\hat f_k(x_0)", r"=", r"\tfrac1k \textstyle\sum_{j \in N_k(x_0)} y_j", font_size=32),
            cmath(r"\mathrm{Var}\,\hat f_k(x_0)", r"\approx", r"\sigma^2 / k", font_size=32),
            cmath(r"\text{bias}", r"\approx", r"\tfrac1k \textstyle\sum_{j \in N_k} f(x_j) - f(x_0)\ \ \text{grows with } k", font_size=30),
            cmath(r"k \text{ small}", r":", r"\text{flexible};\ \ k \text{ large: \ stiff}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"$k$-nearest neighbours: \ average the $k$ closest"), why(r"averaging $k$ independent noises"),
                why(r"wider neighbourhoods reach further from $x_0$"), why(r"$k$ is the dial between bias and variance")]
        with self.voiceover(
            "The trade-off can be computed exactly for the simplest of all rules. <bookmark mark='a'/> The k-nearest-neighbour "
            "prediction at a point averages the y values of the k training points closest to it. <bookmark mark='b'/> Its "
            "variance is about sigma squared over k: the average of k independent noises. <bookmark mark='c'/> Its bias is the "
            "average of the true function over the neighbourhood, minus its value at the point, and as k grows the "
            "neighbourhood reaches further away, so the bias grows. <bookmark mark='d'/> Small k is flexible; large k is stiff. "
            "k is the dial between bias and variance."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def simulation(self):
        d = load("biasvar")
        ks = np.asarray(d["ks"], float)
        lk = np.log10(ks)
        A = axes([-0.1, 1.8], [0, 0.25], x_length=8.4, y_length=4.4, xlabel=r"$k$, \ neighbours averaged", ylabel=r"error at $x_0 = 0.25$",
                 xticks=[0, 0.5, 1, 1.5], yticks=[0, 0.1, 0.2], center=[-1.4, 0.3, 0], xfmt=lambda v: f"{10 ** v:.0f}")
        ax = A.ax
        cb = polyline(ax, lk, np.minimum(d["bias2"], 0.25), RES, 3.5)
        cv = polyline(ax, lk, d["var"], S.CTRL, 3.5)
        cf = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=S.CTRL) for a, b in zip(lk, d["var_formula"])])
        ct = polyline(ax, lk, np.minimum(d["total"], 0.25), OBS, 4)
        nz = DashedLine(ax.c2p(-0.1, d["noise"]), ax.c2p(1.8, d["noise"]), color=GREY_B, stroke_width=2)
        kbest = d["ks"][int(np.argmin(d["total"]))]
        rows = fit_rows(VGroup(
            label(r"3,000 training sets of 100", font_size=22),
            label(r"blue: \ variance; \ dots: \ $\sigma^2/k$", font_size=22, color=S.CTRL),
            label(r"red: \ bias$^2$", font_size=22, color=RES),
            label(r"gold: \ the total, \ with the noise 0.09", font_size=22, color=OBS),
            MathTex(rf"\text{{best}}: k = {kbest}", font_size=28, color=HIT),
        ), 4.0, 0.4, [4.9, 0.3, 0])
        tag = simulated_tag(r"the curve of chapter one", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Simulate it: three thousand training sets of a hundred points from chapter one's curve, and the "
            "k-nearest-neighbour prediction at x equals a quarter, near the curve's peak. <bookmark mark='b'/> The variance falls "
            "like sigma squared over k, the dots. <bookmark mark='c'/> The squared bias is negligible for small k and climbs "
            "steeply once the neighbourhood spreads over the peak. <bookmark mark='d'/> Their sum, plus the noise, is the U. "
            "<bookmark mark='e'/> Its bottom is at about twelve neighbours. Nobody would know that from one training set; the "
            "next chapter estimates it."
        ) as vo:
            self.play(FadeIn(A), Create(nz), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(cf), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cb), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(ct), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def smoothers(self):
        rows = [
            cmath(r"\hat{\mathbf f}", r"=", r"S\,\mathbf y\ \ \text{(a linear smoother)}", font_size=32),
            cmath(r"\mathrm{Var}\,\hat f(x_i)", r"=", r"\sigma^2 \textstyle\sum_j S_{ij}^2", font_size=32),
            cmath(r"\mathrm{df}", r"=", r"\mathrm{tr}(S)", font_size=32),
            cmath(r"\text{examples}", r":", r"\text{OLS: } \mathrm{tr}\,H = p;\ \ k\text{-NN: } n/k", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"$k$-NN, \ kernels, \ splines, \ least squares"), why(r"each fit is a weighted sum of noisy $y$'s"),
                why(r"the effective number of parameters"), why(r"Part 12's hat matrix; \ Part 29 goes deep")]
        with self.voiceover(
            "<bookmark mark='a'/> The same calculation covers a whole family. Many rules, nearest neighbours, Part 16's kernels, "
            "least squares itself, make fitted values that are fixed weighted sums of the observed y's: a matrix S times y. "
            "<bookmark mark='b'/> Then each fitted value's variance is sigma squared times the sum of its squared weights. "
            "<bookmark mark='c'/> The trace of S is the smoother's effective number of parameters, its degrees of freedom. "
            "<bookmark mark='d'/> For least squares it's the number of coefficients, the trace of Part 12's hat matrix; for k "
            "nearest neighbours, about n over k. Part 29 builds on this."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"test error = noise + bias$^2$ + variance", font_size=26),
            label(r"more flexible: \ less bias, \ more variance", font_size=24, color=OBS),
            label(r"the best flexibility depends on the noise and the sample size", font_size=24),
            label(r"more data: \ variance falls, \ so more flexibility pays", font_size=24, color=HIT),
            label(r"but the bias and variance are unseen: \ estimate the total directly", font_size=24, color=CVC),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: test error is noise plus squared bias plus variance. <bookmark mark='b'/> More flexibility "
            "means less bias and more variance. <bookmark mark='c'/> The best balance depends on the noise and the sample size, "
            "<bookmark mark='d'/> and with more data the variance falls, so more flexible rules pay. <bookmark mark='e'/> But "
            "bias and variance are never observed in practice. What we can estimate directly is the total, and that's "
            "cross-validation."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
