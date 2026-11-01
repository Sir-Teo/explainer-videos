from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai5.common import DATA, MODEL, PART, SCORE, WALK, curve, load, normal_pdf, ramp
from videos.ai.ai5.compute import density2


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def plot(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH - 0.2, tips=False,
                        axis_config={"stroke_color": GREY_D, "include_ticks": False})

        out = []
        # 1. the bell from repeated convolution
        c = load("conv")
        zg, dens = np.asarray(c["zg"]), np.asarray(c["exp_dens"])
        a1 = plot([-4, 4, 1], [0, 1.0, 0.5])
        g1 = VGroup(a1, *[curve(a1, zg, np.minimum(dd, 1.0), color=interpolate_color(ManimColor(DATA), ManimColor(C.BITS),
                                                                                    k / (len(dens) - 1)), stroke_width=2.2)
                          for k, dd in enumerate(dens)], curve(a1, zg, normal_pdf(zg), color=MODEL, stroke_width=3))
        out.append((g1, r"sums become bells", MODEL))
        # 2. conditioning a Gaussian
        g = load("gauss")
        pts = np.asarray(g["pts"])[:500]
        a2 = Axes(x_range=[-3.5, 3.5, 1], y_range=[-4, 4, 1], x_length=TW, y_length=TH, tips=False, axis_config={"stroke_width": 0})
        sl = Rectangle(width=TW, height=0.08, stroke_width=0, fill_color=C.BITS, fill_opacity=0.5).move_to(a2.c2p(0, float(g["a"])))
        g2 = VGroup(*[Dot(a2.c2p(*p), radius=0.012, color=DATA) for p in pts], sl)
        out.append((g2, r"conditioning", C.BITS))
        # 3. Cramér-Rao reached
        f = load("fisher")
        ns, mv = np.log10(np.asarray(f["ns"], float)), np.asarray(f["mle_nvar"])
        a3 = plot([0.6, 2.8, 1], [0, 5, 1])
        g3 = VGroup(a3, DashedLine(a3.c2p(0.6, 2), a3.c2p(2.8, 2), color=C.BITS, stroke_width=2),
                    curve(a3, ns, np.minimum(mv, 5), color=MODEL, stroke_width=3))
        out.append((g3, r"the Cram\'er--Rao bound", MODEL))
        # 4. the maximum-entropy die
        me = load("maxent")
        p = np.asarray(me["p"])
        g4 = VGroup(*[Rectangle(width=0.3, height=4.5 * v, stroke_width=0, fill_color=C.SURPRISE, fill_opacity=0.85)
                      for v in p]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        out.append((g4, r"maximum entropy", C.SURPRISE))
        # 5. tails and their bounds
        t = load("tails")
        eps = np.asarray(t["eps"])
        a5 = plot([0, 0.3, 0.1], [-8, 0, 2])
        g5 = VGroup(a5, curve(a5, eps, np.log10(np.asarray(t["exact"])), color=WHITE, stroke_width=3),
                    curve(a5, eps, np.log10(np.asarray(t["hoeff"])), color=MODEL, stroke_width=2.5),
                    curve(a5, eps, np.log10(np.minimum(np.asarray(t["cheb"]), 1)), color=C.INTERVAL, stroke_width=2.5))
        out.append((g5, r"concentration", C.INTERVAL))
        # 6. decoding: predictability against diversity
        dd = load("decoding")
        a6 = plot([0.7, 1.0, 0.1], [0.5, 1.7, 0.5])
        g6 = VGroup(a6, DashedLine(a6.c2p(0.7, float(dd["human"]["nll"])), a6.c2p(1.0, float(dd["human"]["nll"])),
                                   color=WHITE, stroke_width=1.5))
        cols = {"temp": "#FF6B8B", "topk": C.INTERVAL, "topp": C.BITS, "minp": "#7FD3FF"}
        for k, col in cols.items():
            P = sorted([(min(max(float(dd[s]["div"]), 0.7), 1.0), min(float(dd[s]["nll"]), 1.7))
                        for s, kk in zip(dd["settings"], dd["kinds"]) if kk == k])
            g6.add(VMobject(color=col, stroke_width=2.5).set_points_as_corners([a6.c2p(a, b) for a, b in P]))
        out.append((g6, r"decoding", C.BITS))
        # 7. Langevin onto the two bumps
        lg = load("langevin")
        fr = np.asarray(lg["frames"])[-1][:400]
        a7 = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=TW, y_length=TH, tips=False, axis_config={"stroke_width": 0})
        c7 = contour_lines(a7, density2, (-4, 4), (-3, 3), [0.1, 0.4, 0.7], n=(80, 60), stroke_width=1.4)
        g7 = VGroup(c7, *[Dot(a7.c2p(*q), radius=0.013, color=WALK) for q in np.clip(fr, [-4, -3], [4, 3])])
        out.append((g7, r"Metropolis and Langevin", SCORE))
        # 8. noise into letters
        s = load("shape")
        bwd = np.asarray(s["bwd"])[-1]
        cl = ramp(bwd[:, 0] + 0.35 * bwd[:, 1], DATA, C.BITS)
        g8 = VGroup(*[Dot([0.55 * q[0], 0.55 * q[1], 0], radius=0.02, color=cc) for q, cc in zip(bwd, cl)])
        out.append((g8, r"noise, run backwards", SCORE))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, \ in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        c, f, t = load("conv"), load("fisher"), load("tails")
        need = dict(t["need"])
        lg = load("langevin")
        with self.voiceover(
            "Let's take stock. Centered, rescaled sums of independent, identically distributed pieces with positive "
            "finite variance approach a bell. With a finite third absolute moment, Berry-Esseen bounds the gap by "
            "a constant over the square root of n. Conditioning a bell gives a bell. In regular models, maximum "
            f"likelihood is asymptotically efficient: for our Cauchy fit, n times its measured variance is {float(f['mle_nvar'][-1]):.2f} "
            "against the bound of two. Bayes's rule is counting, and a prior is a regularizer. Maximum entropy gives "
            "the exponential family, softmax included. Hoeffding's bound needed "
            f"{need['hoeffding']} flips where {need['exact']} sufficed, and held everywhere. Sampling turns uniform "
            "numbers into anything; decoding trades diversity for predictability. Chains forget at the rate of "
            "their spectral gap in the lazy reversible setting; Monte Carlo errors with finite variance fall like "
            "one over root n, and importance weights can collapse in high dimensions. Metropolis corrections "
            "preserve the target; fixed-step unadjusted Langevin can bias it. Random motion has its "
            "own calculus, whose density obeys Fokker and Planck's law."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"maximum likelihood, \ Fisher information", [6, 11]),
            (r"Bayes, \ conjugacy, \ MAP as weight decay", [7, 8]),
            (r"concentration inequalities", [8, 26]),
            (r"Markov chains, \ MCMC, \ HMMs", [7]),
            (r"softmax, \ temperature, \ decoding", [19, 28]),
            (r"score-function gradients, \ importance weights", [26, 27]),
            (r"SDEs, \ Langevin, \ Fokker--Planck", [11, 20, 21]),
        ], font_size=24)
        with self.voiceover(
            "All of this comes back. Maximum likelihood and Fisher information train the models of parts six and "
            "eleven. Bayes, Markov chains and their samplers return in part seven, and the concentration "
            "inequalities become generalization bounds in part eight. Decoding is extended in part nineteen. "
            "Score-function gradients and importance weights are reinforcement learning, in parts twenty-six and "
            "twenty-seven. And stochastic differential equations describe noisy training in part eleven and "
            "generation in parts twenty and twenty-one."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Show that the density of $X + Y$, for independent $X, Y$ with densities $f, g$, is $f * g$. \ For "
            r"$f = g = e^{-x}$ on $x > 0$, compute $f * f$ and $f * f * f$.",
            r"Compute the Fisher information of $\mathcal{N}(\theta, \sigma^2)$ in $\theta$, and of the Cauchy location; "
            r"which estimators reach the Cram\'er--Rao bound?",
            r"Show that the maximum-entropy distribution on $\{0, 1, 2, \dots\}$ with mean $m$ is geometric.",
            r"Use Hoeffding's inequality to find $n$ so that an average of $n$ values in $[0, 1]$ is within $0.01$ of "
            r"its mean with probability $0.999$.",
            r"Show that $\arg\max_i (z_i + G_i)$, with independent Gumbel $G_i$, picks $i$ with probability "
            r"$e^{z_i} / \sum_j e^{z_j}$.",
            r"For the Ornstein--Uhlenbeck process $dx = -\theta x\,dt + \sigma\,dW$, find the stationary density from "
            r"the Fokker--Planck equation.",
        ], font_size=21)
        with self.voiceover(
            "Here are six problems to try, from convolutions to the Ornstein-Uhlenbeck process's stationary "
            "bell. Pause here and work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 6, \ Classical ML", font_size=40).to_edge(UP, buff=0.35)
        g = np.random.default_rng(1805)  # Legendre's least squares, 1805 (an illustration)
        x = np.sort(g.uniform(-5, 5, 26))
        y = 0.45 * x + 0.2 + g.normal(scale=0.8, size=x.size)
        b = np.polyfit(x, y, 1)
        dots = VGroup(*[Dot([xi, yi - 0.4, 0], radius=0.07, color=DATA) for xi, yi in zip(x, y)])
        fit = Line([-5.5, b[0] * -5.5 + b[1] - 0.4, 0], [5.5, b[0] * 5.5 + b[1] - 0.4, 0], color=MODEL, stroke_width=4)
        res = VGroup(*[Line([xi, yi - 0.4, 0], [xi, b[0] * xi + b[1] - 0.4, 0], color=C.SURPRISE, stroke_width=2)
                       for xi, yi in zip(x, y)])
        tag = label(r"least squares: \ Legendre (1805) and Gauss; \ illustration", font_size=24, color=GREY_B)
        tag.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Next time, act two begins: learning from data. We start with the classics: least squares and its "
            "geometry, which is maximum likelihood under Gaussian noise; logistic regression; kernels and support "
            "vector machines; trees and boosting. <bookmark mark='a'/> They ran machine learning before deep "
            "learning, and on tables of data they still often win."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.05), FadeIn(tag), run_time=1.5)
            self.play(Create(fit), LaggedStart(*[Create(r) for r in res], lag_ratio=0.04), run_time=2.0)
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"J.~K.~Blitzstein \& J.~Hwang, \textit{Introduction to Probability}, 2nd ed.\ (2019); \ "
            r"L.~Wasserman, \textit{All of Statistics} (2004)",
            r"D.~J.~C.~MacKay, \textit{Information Theory, Inference, and Learning Algorithms} (2003); \ "
            r"D.~A.~Levin \& Y.~Peres, \textit{Markov Chains and Mixing Times}, 2nd ed.\ (2017)",
            r"B.~{\O}ksendal, \textit{Stochastic Differential Equations}, 6th ed.\ (2003); \ "
            r"S.~Boucheron, G.~Lugosi \& P.~Massart, \textit{Concentration Inequalities} (2013)",
        ]
        papers = [
            r"de Moivre (1733); \ Laplace (1810); \ Berry (1941); \ Esseen (1942); \ Shevtsova (2011); \ Galton (1886); "
            r"\ Kalman (1960)",
            r"Fisher (1922, 1925); \ Rao (1945); \ Cram\'er (1946); \ Bayes (1763); \ Laplace (1774); \ Jaynes (1957)",
            r"Chebyshev (1867); \ Chernoff (1952); \ Hoeffding (1963); \ von Neumann (1951); \ Box \& Muller (1958); \ "
            r"Gumbel (1954); \ Jang, Gu \& Poole (2017); \ Maddison, Mnih \& Teh (2017)",
            r"Fan, Lewis \& Dauphin (2018); \ Holtzman et al., \textit{The Curious Case of Neural Text Degeneration} "
            r"(2020); \ Nguyen et al., min-$p$ (2024); \ Schaeffer et al.\ (2025)",
            r"Markov (1906); \ Metropolis \& Ulam (1949); \ Metropolis, Rosenbluth, Rosenbluth, Teller \& Teller "
            r"(1953); \ Hastings (1970); \ Glynn (1990); \ Williams (1992); \ Salimans et al.\ (2017)",
            r"Langevin (1908); \ Roberts \& Tweedie (1996); \ Welling \& Teh (2011); \ Einstein (1905); \ Bachelier "
            r"(1900); \ Wiener (1923); \ L\'evy (1940); \ It\^o (1944, 1951); \ Maruyama (1955)",
            r"Fokker (1914); \ Planck (1917); \ Kolmogorov (1931); \ Ornstein \& Uhlenbeck (1930); \ Anderson (1982); \ "
            r"Sohl-Dickstein et al.\ (2015); \ Song et al.\ (2021)",
        ]
        card = reference_card(books, papers, font_size=19)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels); \ GPT-2's own weights; \ the series' novels model. "
                    r"\ Every number on screen is computed or cited.", font_size=18).to_edge(DOWN, buff=0.2)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=18)
        credit.next_to(data, UP, buff=0.08)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.12:
            card.scale((card.height - (credit.get_top()[1] + 0.12 - card.get_bottom()[1])) / card.height)
            card.next_to(credit, UP, buff=0.12)
        with self.voiceover(
            "Blitzstein and Hwang's Introduction to Probability is a friendly place to start; MacKay's book has "
            "the best chapters on Monte Carlo methods, and Levin and Peres's on mixing. Thanks for watching, and "
            "see you in part six."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
