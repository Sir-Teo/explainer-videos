from __future__ import annotations

import numpy as np

from videos.stats.stats26.common import *  # noqa: F403


class DP(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.sticks()
        self.restaurant()
        self.tables()
        self.uses()

    def card(self):
        card = chapter_card(13, r"Bayesian nonparametrics", r"A prior on distributions", lit=(1973,), part=PART)
        with self.voiceover("Chapter thirteen. Bayesian nonparametrics, a first look."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"G", r"\sim", r"\text{DP}(\alpha, G_0): \ \text{a random probability distribution}", font_size=30),
            cmath(r"(G(A_1), \dots, G(A_k))", r"\sim", r"\text{Dirichlet}(\alpha G_0(A_1), \dots, \alpha G_0(A_k))", font_size=28),
            cmath(r"E\,G", r"=", r"G_0; \ \ \alpha: \ \text{how tightly } G \text{ hugs } G_0", font_size=30),
            cmath(r"G \mid x_{1:n}", r"\sim", r"\text{DP}\bigl(\alpha + n, \ \tfrac{\alpha G_0 + \sum \delta_{x_i}}{\alpha + n}\bigr)", font_size=28),
        ]
        rows[3][2].set_color(SHRUNK)
        whys = [why(r"Ferguson (1973)"), why(r"for every partition of the space"), why(r"a centre and a concentration"),
                why(r"conjugate: \ prior guess and data, \ weighted")]
        with self.voiceover(
            "<bookmark mark='a'/> What if we don't want to assume the population of effects is normal, or any other shape? "
            "Thomas Ferguson's 1973 Dirichlet process is a prior on distributions themselves. <bookmark mark='b'/> A random "
            "distribution G is a Dirichlet process if, for every way of cutting the space into pieces, the probabilities G "
            "gives the pieces have a Dirichlet distribution. <bookmark mark='c'/> On average G is the base guess G nought, "
            "and alpha says how closely it follows that guess. <bookmark mark='d'/> And it is conjugate: after data, the "
            "posterior is another Dirichlet process, centred on a weighted average of the guess and the data's empirical "
            "distribution, chapter four's pseudo-data again, with alpha as the prior's sample size."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sticks(self):
        d = load("dp")
        group = VGroup()
        anims = []
        for k, a in enumerate(("1.0", "5.0")):
            w = np.asarray(d["sticks"][a])
            y = 1.3 - 2.4 * k
            total = 11.0
            x = -total / 2
            segs = VGroup()
            for j, wj in enumerate(w):
                seg = Rectangle(width=max(total * wj, 0.004), height=0.7, stroke_width=0.6, stroke_color=BLACK,
                                fill_color=SCHOOL[j % 8], fill_opacity=0.85)
                seg.move_to([x + total * wj / 2, y, 0])
                segs.add(seg)
                x += total * wj
            name = label(rf"$\alpha = {float(a):g}$", font_size=24).next_to(segs, LEFT, buff=0.3)
            group.add(name)
            anims.append(segs)
        rows = fit_rows(VGroup(
            label(r"break a stick of length 1: \ keep a Beta(1, $\alpha$) fraction, \ break the rest again", font_size=22),
            label(r"each piece is the weight of one atom of $G$", font_size=22, color=GREY_A),
            label(r"small $\alpha$: \ a few big pieces; \ large $\alpha$: \ many small ones", font_size=22, color=PATH),
            label(r"so $G$ is discrete, \ with probability one", font_size=22, color=RES),
        ), 12.0, 0.22, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Jayaram Sethuraman's construction shows what such a G looks like. Take a stick of length "
            "one. Break off a random fraction, drawn from a beta of one and alpha, and keep it; break the remainder again, "
            "and again. <bookmark mark='b'/> Each piece is the probability of one point, drawn from G nought. "
            "<bookmark mark='c'/> With alpha of one, a few large pieces take almost everything; with alpha of five, the "
            "weight is spread over many. <bookmark mark='d'/> Either way, a draw from a Dirichlet process is a discrete "
            "distribution, a fact that makes it a natural prior for clusters."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(group[0]))
            self.play(LaggedStart(*[GrowFromEdge(s_, LEFT) for s_ in anims[0]], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(group[1]), LaggedStart(*[GrowFromEdge(s_, LEFT) for s_ in anims[1]], lag_ratio=0.1), FadeIn(rows[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def restaurant(self):
        d = load("dp")
        z = np.asarray(d["first"])
        n_tab = int(z.max()) + 1
        tables = VGroup(*[Circle(radius=0.55, stroke_color=GREY_B, stroke_width=2).move_to([-5.2 + 1.45 * t, 1.4, 0]) for t in range(n_tab)])
        counts = [0] * n_tab
        guests = []
        for i, t in enumerate(z):
            ang = counts[t] * 0.9
            r = 0.3 + 0.12 * (counts[t] // 7)
            pos = tables[t].get_center() + np.array([r * np.cos(ang), r * np.sin(ang), 0])
            guests.append(Dot(pos, radius=0.07, color=SCHOOL[t % 8]))
            counts[t] += 1
        rows = fit_rows(VGroup(
            label(r"the Chinese restaurant: \ customer $n + 1$ arrives", font_size=24),
            label(r"joins a table with $n_k$ people: \ probability $n_k/(n + \alpha)$", font_size=24, color=SHRUNK),
            label(r"opens a new table: \ probability $\alpha/(n + \alpha)$", font_size=24, color=PATH),
            label(rf"30 customers, \ $\alpha = 2$: \ {n_tab} tables", font_size=24, color=GREY_A),
            label(r"the rich get richer", font_size=24, color=RES),
        ), 12.0, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Integrating G out gives the Chinese restaurant process, a story of Jim Pitman and Lester "
            "Dubins. Customers enter one at a time. <bookmark mark='b'/> Each new customer joins an occupied table with "
            "probability proportional to the number already seated there, <bookmark mark='c'/> or starts a new table with "
            "probability proportional to alpha. <bookmark mark='d'/> Thirty customers with alpha of two. "
            "<bookmark mark='e'/> Popular tables grow more popular: the rich get richer, and a few big clusters form with a "
            "tail of small ones."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ a seeded example"))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            shown = set()
            seq = []
            for g_, t in zip(guests, z):
                if t not in shown:
                    seq.append(Succession(Create(tables[t], run_time=0.15), FadeIn(g_, run_time=0.15)))
                    shown.add(t)
                else:
                    seq.append(FadeIn(g_, run_time=0.25))
            self.play(Succession(*seq), FadeIn(rows[3]), run_time=6.0)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def tables(self):
        d = load("dp")
        ns = np.asarray(d["ns"], float)
        A = axes([0, 4], [0, 45], x_length=7.4, y_length=4.2, xlabel=r"customers $n$ \ (log scale)", ylabel=r"expected number of tables",
                 xticks=[0, 1, 2, 3, 4], yticks=[0, 10, 20, 30, 40], xfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.0, 0.3, 0])
        ax = A.ax
        c1 = curve(ax, np.log10(ns), d["exp_tables"]["1.0"], SHRUNK, 3.5)
        c5 = curve(ax, np.log10(ns), d["exp_tables"]["5.0"], POST, 3.5)
        rows = fit_rows(VGroup(
            label(r"$E K_n = \sum_{i < n} \alpha/(\alpha + i) \approx \alpha \log(1 + n/\alpha)$", font_size=22),
            label(r"green: \ $\alpha = 1$", font_size=22, color=SHRUNK),
            label(r"orange: \ $\alpha = 5$", font_size=22, color=POST),
            label(rf"200 customers, \ $\alpha = 2$: \ {d['tables']} tables \ (expected {d['expected']:.1f})", font_size=22, color=GREY_A),
            label(r"the number of clusters is not fixed: \ it grows with the data", font_size=22, color=HIT),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How many tables? On average, the sum of alpha over alpha plus i, which grows like alpha "
            "times the log of the number of customers. <bookmark mark='b'/> With alpha of one, about ten tables for ten "
            "thousand customers; <bookmark mark='c'/> with alpha of five, about thirty-eight. <bookmark mark='d'/> A simulated "
            "restaurant of two hundred with alpha of two had twelve tables, against an expectation of about ten. "
            "<bookmark mark='e'/> The point for modelling: the number of clusters isn't fixed in advance. The model creates "
            "new clusters as the data demand them, slowly."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c5), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def uses(self):
        rows = fit_rows(VGroup(
            label(r"DP mixtures: \ clusters without choosing how many \ (Antoniak 1974; \ Escobar \& West 1995)", font_size=24, color=SHRUNK),
            label(r"the eight schools with a DP population: \ no normality assumed", font_size=24),
            label(r"Gaussian processes: \ priors on functions \ (Part 39)", font_size=24),
            label(r"posterior consistency can fail: \ Diaconis \& Freedman; \ Part 53", font_size=24, color=RES),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In practice the Dirichlet process sits inside mixture models, where each table is a "
            "cluster with its own parameters, and the data choose how many clusters there are. <bookmark mark='b'/> Put one "
            "in place of the eight schools' normal population, and the effects could fall into groups instead. "
            "<bookmark mark='c'/> Gaussian processes, priors on whole functions, are the other workhorse, in Part 39. "
            "<bookmark mark='d'/> But in infinite dimensions, Bernstein–von Mises no longer protects us, and the prior can "
            "matter for ever; Part 53 takes up the theory."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
