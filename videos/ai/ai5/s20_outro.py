from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, MODEL, SCORE, WALK, load, normal_pdf, ramp
from videos.ai.ai5.compute import density2


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def frame(caption, color):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            return box, label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)

        def plot(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH - 0.2, tips=False,
                        axis_config={"stroke_color": GREY_D, "include_ticks": False})

        out = []
        # 1. the bell from the Galton board
        g = load("galton")
        counts = np.asarray(g["counts"], float)
        ax = plot([-0.5, 12.5, 1], [0, 0.25, 1])
        bars = VGroup(*[Rectangle(width=ax.x_length / 13 * 0.85, height=ax.y_length * c / 1000 / 0.25, stroke_width=0,
                                  fill_color=DATA, fill_opacity=0.7).move_to(ax.c2p(k, c / 2000)) for k, c in
                        enumerate(counts)])
        xs = np.linspace(-0.5, 12.5, 100)
        out.append((VGroup(ax, bars, ax.plot_line_graph(xs, normal_pdf(xs, 6, math.sqrt(3)), add_vertex_dots=False,
                                                        line_color=MODEL, stroke_width=3)), r"the bell curve", MODEL))
        # 2. maximum likelihood: the fit hill, as contours
        m = load("mle")
        ax2 = Axes(x_range=[3, 9, 1], y_range=[0.9, 4, 1], x_length=TW, y_length=TH, tips=False,
                   axis_config={"stroke_width": 0})
        mu_hat, s_hat, top = float(m["mu_hat"]), float(m["sigma_hat"]), float(m["ll_hat"])
        v = s_hat ** 2

        def fit(a, b):
            return math.exp(-0.5 * math.log(2 * math.pi * b * b) - (v + (mu_hat - a) ** 2) / (2 * b * b) - top)

        cont = contour_lines(ax2, np.vectorize(fit), (3, 9), (0.9, 4), [0.2, 0.4, 0.6, 0.8, 0.95], n=(80, 60),
                             stroke_width=1.6)
        out.append((VGroup(cont, Dot(ax2.c2p(mu_hat, s_hat), radius=0.06, color=WHITE)), r"maximum likelihood", C.BITS))
        # 3. Bayes: the belief narrowing
        b = load("bayes")
        ps = np.linspace(0.001, 0.6, 200)
        ax3 = plot([0, 0.6, 1], [0, 1.1, 1])
        curves = VGroup()
        for k, n in enumerate((10, 100, 1000)):
            kk = int(b[f"k{n}"])
            lp = kk * np.log(ps) + (n - kk) * np.log1p(-ps)
            dens = np.exp(lp - lp.max())
            curves.add(ax3.plot_line_graph(ps, dens, add_vertex_dots=False, line_color=C.BITS, stroke_width=2.5)
                       .set_stroke(opacity=0.4 + 0.3 * k))
        out.append((VGroup(ax3, curves), r"belief, updated", C.BITS))
        # 4. temperature
        t = load("temperature")
        z = np.asarray(t["logits"], float)
        top10 = [int(i) for i in t["top"]]
        tb = VGroup()
        for j, T in enumerate((0.5, 1.0, 2.0)):
            q = np.exp((z - z.max()) / T)
            q = q / q.sum()
            for i in range(6):
                tb.add(Rectangle(width=0.13, height=max(1.5 * q[top10[i]] / 0.21, 0.02), stroke_width=0,
                                 fill_color=MODEL, fill_opacity=0.85)
                       .move_to([-1.1 + j * 1.05 + i * 0.16, 0, 0], aligned_edge=DOWN))
        out.append((tb, r"temperature", MODEL))
        # 5. a Markov chain
        pos = [np.array([0, 0.75, 0]), np.array([-1.0, -0.6, 0]), np.array([1.0, -0.6, 0])]
        mc = VGroup(*[Circle(radius=0.28, color=c, stroke_width=3).move_to(p) for p, c in zip(pos, (GREY_B, C.BITS,
                                                                                                    DATA))])
        for a_, b_ in ((0, 1), (1, 2), (2, 0)):
            d_ = (pos[b_] - pos[a_]) / np.linalg.norm(pos[b_] - pos[a_])
            mc.add(Arrow(pos[a_] + d_ * 0.3, pos[b_] - d_ * 0.3, buff=0, color=GREY_B, stroke_width=3,
                         max_tip_length_to_length_ratio=0.2))
        mc.add(glow_dot(pos[1], color=WALK, radius=0.08))
        out.append((mc, r"Markov chains", WALK))
        # 6. Monte Carlo
        mcd = load("montecarlo")
        pts, ins = np.asarray(mcd["pts"])[:500], np.asarray(mcd["inside"], bool)[:500]
        R = 0.95
        darts = VGroup(Square(2 * R, color=GREY_B, stroke_width=1.5), Circle(radius=R, color=DATA, stroke_width=2),
                       *[Dot([R * p[0], R * p[1], 0], radius=0.018, color=DATA if i else GREY_C) for p, i in zip(pts, ins)])
        out.append((darts, r"Monte Carlo", DATA))
        # 7. Metropolis
        ch = np.asarray(load("mcmc")["chain"])
        ax7 = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=TW, y_length=TH, tips=False, axis_config={"stroke_width": 0})
        c7 = contour_lines(ax7, density2, (-4, 4), (-3, 3), [0.1, 0.4, 0.7], n=(80, 60), stroke_width=1.4)
        trail = VMobject(color=WHITE, stroke_width=1.2, stroke_opacity=0.7).set_points_as_corners(
            [ax7.c2p(*p) for p in ch[:400:2]])
        out.append((VGroup(c7, trail), r"Metropolis", SCORE))
        # 8. noise into letters
        s = load("shape")
        bwd = np.asarray(s["bwd"])[-1]
        cols = ramp(bwd[:, 0] + 0.35 * bwd[:, 1], DATA, C.BITS)
        letters = VGroup(*[Dot([0.55 * p[0], 0.55 * p[1], 0], radius=0.02, color=c) for p, c in zip(bwd, cols)])
        out.append((letters, r"noise, run backwards", SCORE))
        tiles = Group()
        for pic, cap, col in out:
            box, c = frame(cap, col)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(r"Part 5, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Many small random pushes add up to a bell. Fitting a model means maximizing "
            "likelihood, which is minimizing cross-entropy. Bayes's rule turns evidence into a sharper belief. "
            "Sampling turns a distribution into a choice, with temperature as the dial. Markov chains forget where "
            "they started, at a rate set by an eigenvalue. Monte Carlo answers questions with random samples, and "
            "Metropolis's walk draws them from shapes we can only evaluate. And random motion, run backwards with the "
            "score, turns noise into data."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"maximum likelihood $=$ cross-entropy", [6, 7, 9]),
            (r"Bayes, posteriors, sampling them", [7, 8]),
            (r"Markov chains, hidden states", [7, 15]),
            (r"temperature, sampling text", [19, 28]),
            (r"importance sampling", [28, 29]),
            (r"SDEs: noisy descent; \ the score", [11, 21]),
        ], font_size=26)
        with self.voiceover(
            "All of this comes back. Maximum likelihood trains every model from part six on. Bayes and Markov "
            "chains return in statistical machine learning, in part seven. Sampling and importance weights come back "
            "when models reason and act, in parts nineteen, twenty-eight and twenty-nine. And stochastic differential equations "
            "describe both noisy gradient descent, in part eleven, and diffusion models, in part twenty-one."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 6, \ Classical ML", font_size=40).to_edge(UP, buff=0.35)
        g = np.random.default_rng(1805)  # Legendre's least squares, 1805
        x = np.sort(g.uniform(-5, 5, 26))
        y = 0.45 * x + 0.2 + g.normal(scale=0.8, size=x.size)
        b = np.polyfit(x, y, 1)
        dots = VGroup(*[Dot([xi, yi - 0.4, 0], radius=0.07, color=DATA) for xi, yi in zip(x, y)])
        fit = Line([-5.5, b[0] * -5.5 + b[1] - 0.4, 0], [5.5, b[0] * 5.5 + b[1] - 0.4, 0], color=MODEL, stroke_width=4)
        res = VGroup(*[Line([xi, yi - 0.4, 0], [xi, b[0] * xi + b[1] - 0.4, 0], color=C.SURPRISE, stroke_width=2)
                       for xi, yi in zip(x, y)])
        tag = label(r"least squares: \ Legendre (1805) and Gauss", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Next time, act two begins: learning. We start with the classics: least squares and its geometry, "
            "logistic regression, kernels and support vector machines, trees and boosting. <bookmark mark='a'/> "
            "They ran machine learning before deep learning, and on tables of data they still often win."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.05), FadeIn(tag), run_time=1.5)
            self.play(Create(fit), LaggedStart(*[Create(r) for r in res], lag_ratio=0.04), run_time=2.0)
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"J.~K.~Blitzstein \& J.~Hwang, \textit{Introduction to Probability}, 2nd ed.\ (2019)",
            r"D.~J.~C.~MacKay, \textit{Information Theory, Inference, and Learning Algorithms} (2003), chapters 29--30",
            r"B.~{\O}ksendal, \textit{Stochastic Differential Equations}, 6th ed.\ (2003)",
        ]
        papers = [
            r"N.~Metropolis, A.~W.~Rosenbluth, M.~N.~Rosenbluth, A.~H.~Teller \& E.~Teller, \textit{Equation of State "
            r"Calculations by Fast Computing Machines} (1953)",
            r"W.~K.~Hastings, \textit{Monte Carlo Sampling Methods Using Markov Chains and Their Applications} (1970)",
            r"A.~Einstein, \textit{On the Movement of Small Particles Suspended in Stationary Liquids} (1905)",
            r"B.~D.~O.~Anderson, \textit{Reverse-Time Diffusion Equation Models} (1982)",
            r"J.~Sohl-Dickstein et al., \textit{Deep Unsupervised Learning using Nonequilibrium Thermodynamics} (2015)",
            r"Y.~Song et al., \textit{Score-Based Generative Modeling through Stochastic Differential Equations} (2021)",
            r"A.~Holtzman et al., \textit{The Curious Case of Neural Text Degeneration} (2020)",
        ]
        card = reference_card(books, papers)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels); \ GPT-2's own weights. \ Every number on screen is "
                    r"computed and checked; \ schematics and illustrations are labeled.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "Blitzstein and Hwang's Introduction to Probability is a friendly place to start, and MacKay's book has "
            "the best chapters on Monte Carlo methods. Thanks for watching, and see you in part six."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
