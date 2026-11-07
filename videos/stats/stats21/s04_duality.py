from __future__ import annotations

import numpy as np

from videos.stats.stats21.common import *  # noqa: F403


class Duality(VoiceoverScene):
    def construct(self):
        self.card()
        self.dual_function()
        self.bakery_dual()
        self.neyman_pearson()
        self.np_bars()
        self.gap()
        self.ridge_dual()

    def card(self):
        card = chapter_card(3, r"Duality", r"Dual bounds, \ and when they match", lit=(1939,), part=PART)
        with self.voiceover("Chapter three. Duality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def dual_function(self):
        rows = [
            cmath(r"\text{primal}", r":", r"p^* = \inf_x f(x) \ \text{s.t.} \ g(x) \le 0", font_size=30),
            cmath(r"\text{dual function}", r":", r"q(\mu) = \inf_x \, f(x) + \mu' g(x), \ \ \mu \ge 0", font_size=30),
            cmath(r"\text{weak duality}", r":", r"q(\mu) \le p^* \ \text{for every} \ \mu \ge 0", font_size=30),
            cmath(r"\text{strong duality}", r":", r"\sup_{\mu\ge0} q(\mu) = p^*", font_size=30),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"the problem we want"), why(r"price the constraints, \ then optimize freely"),
                why(r"any price gives a lower bound"), why(r"convex problems, \ mild conditions (Slater)")]
        intro = label('Feasible dual values bound the primal optimum', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Every constrained problem, the primal, has a partner. <bookmark mark='b'/> Put prices mu on "
            "the constraints and minimize without them: the result, as a function of the prices, is the dual function. "
            "<bookmark mark='c'/> For any non-negative prices it's a lower bound on the true minimum, since at a feasible point "
            "the penalty terms can only help. <bookmark mark='d'/> For convex problems, under a mild condition, the best lower "
            "bound is exact: maximizing the dual gives the same value as minimizing the primal. That's strong duality."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bakery_dual(self):
        d = load("bakery")
        y = d["dual"]
        rows = [
            cmath(r"\text{primal}", r":", r"\max\ 3x_1 + 4x_2 \ \ \text{s.t.} \ \ Ax \le (14, 24, 9),\ x\ge0", font_size=28),
            cmath(r"\text{dual}", r":", r"\min\ 14y_1 + 24y_2 + 9y_3 \ \ \text{s.t.} \ \ A'y \ge (3, 4), \ y \ge 0", font_size=28),
            cmath(r"y^*", r"=", rf"({y[0]:.0f}, {y[1]:.0f}, {y[2]:.0f}): \ 14 + 0 + 18 = {d['value']:.0f}", font_size=30),
            cmath(r"\text{reading}", r":", r"\text{what a buyer would pay for the bakery's resources}", font_size=28),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"the bakery of the hook"), why(r"price flour, \ oven, \ staff; \ each tray must be worth its price"),
                why(r"the shadow prices; \ equal to the best profit, \ 32"), why(r"complementary slackness: \ the idle oven is worth 0")]
        intro = label('Resource prices certify the best achievable bakery profit', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The bakery's dual is a story about prices. <bookmark mark='b'/> Suppose a buyer wants to rent "
            "the bakery's flour, oven and staff. She must offer prices high enough that each kind of tray is worth no more than "
            "its ingredients, or the baker would rather bake it, and she wants to pay as little as possible in total. "
            "<bookmark mark='c'/> Her best prices are one for flour, nothing for the oven, two for staff, and the total, "
            "fourteen plus eighteen, is thirty-two: exactly the best profit. <bookmark mark='d'/> The oven, which wasn't fully "
            "used, gets a price of zero: complementary slackness again."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def neyman_pearson(self):
        rows = [
            cmath(r"\max_{\phi}", r"", r"\textstyle\sum_x \phi(x) p_1(x) \ \ \text{(power)}", font_size=30),
            cmath(r"\text{s.t.}", r"", r"\textstyle\sum_x \phi(x) p_0(x) \le \alpha, \ \ 0 \le \phi(x) \le 1", font_size=30),
            cmath(r"\text{a linear program in}", r"", r"\phi(x), \ \text{the chance of rejecting at } x", font_size=28),
            cmath(r"\text{KKT}", r"\Rightarrow", r"\phi(x) = 1 \ \text{where} \ p_1/p_0 > k, \ \ 0 \ \text{where} \ < k", font_size=30),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"a test: \ reject with probability $\phi(x)$"), why(r"its size at most $\alpha$"),
                why(r"Dantzig \& Wald (1951)"), why(r"the likelihood-ratio test; \ $k$ is the multiplier")]
        intro = label('Allocate rejection probability to maximize power at fixed size', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Now Dantzig's homework. <bookmark mark='a'/> A test, on a finite set of possible outcomes, is a function phi: the "
            "probability of rejecting when x is observed. Its power is the sum of phi times the alternative's probabilities. "
            "<bookmark mark='b'/> Its size, the sum of phi times the null's probabilities, must be at most alpha, and each phi "
            "is between zero and one. <bookmark mark='c'/> Everything is linear in phi: the most powerful test is the solution "
            "of a linear program. <bookmark mark='d'/> And the KKT conditions solve it. Each outcome is a good buy if its power "
            "per unit of size, the likelihood ratio, beats the price of size, k: reject where the ratio exceeds k, never where "
            "it falls short. That's the Neyman–Pearson lemma, with the critical value revealed as a Lagrange multiplier."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def np_bars(self):
        d = load("np")
        k = np.asarray(d["x"])
        A = axes([-0.6, 20.6], [0, 0.2], x_length=9.0, y_length=3.6, xlabel=r"successes in 20 trials", ylabel=r"probability",
                 xticks=[0, 5, 10, 14, 15, 20], yticks=[0, 0.1, 0.2], center=[-1.0, 0.8, 0])
        ax = A.ax
        w = ax.c2p(0.38, 0)[0] - ax.c2p(0, 0)[0]
        b0 = VGroup(*[Rectangle(width=w, height=max(0.01, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=GREY_B,
                                fill_opacity=0.8).move_to(ax.c2p(x - 0.2, 0), aligned_edge=DOWN) for x, v in zip(k, d["p0"])])
        b1 = VGroup(*[Rectangle(width=w, height=max(0.01, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=NEWT,
                                fill_opacity=0.8).move_to(ax.c2p(x + 0.2, 0), aligned_edge=DOWN) for x, v in zip(k, d["p1"])])
        phi = np.asarray(d["phi"])
        rej = VGroup(*[Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], height=(ax.c2p(0, 0.2)[1] - ax.c2p(0, 0)[1]) * p,
                                 stroke_width=0, fill_color=PATH, fill_opacity=0.25).move_to(ax.c2p(x, 0), aligned_edge=DOWN)
                       for x, p in zip(k, phi) if p > 1e-6])
        i14 = int(np.flatnonzero((phi > 1e-6) & (phi < 1 - 1e-6))[0])
        rows = fit_rows(VGroup(
            label(r"grey: \ $H_0$, \ $p = 0.5$; \ blue: \ $H_1$, \ $p = 0.7$", font_size=22),
            label(rf"the LP's solution: \ reject at 15 or more; \ at 14, \ with probability {phi[i14]:.2f}", font_size=22, color=PATH),
            label(rf"size {d['size']:.3f}, \ power {d['power']:.3f}", font_size=22, color=NEWT),
            label(rf"the multiplier: \ $k = {d['k']:.2f} = p_1(14) / p_0(14)$", font_size=24, color=TRUE),
        ), 12.0, 0.25, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the linear program solved numerically. Twenty trials; the null says the success rate is "
            "a half, in grey, the alternative point seven, in blue. Size five percent. <bookmark mark='b'/> The solver rejects "
            "for fifteen or more successes, and at exactly fourteen rejects with probability point seven nine, a randomized "
            "test, to use up the size exactly. <bookmark mark='c'/> Its power is fifty-seven percent, the best any level-five-"
            "percent test can do. <bookmark mark='d'/> And the solver's multiplier on the size constraint is five point one "
            "eight, which is precisely the likelihood ratio at fourteen. The lemma's k is a shadow price: the power you'd gain "
            "per unit of extra size."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b0], lag_ratio=0.03),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in b1], lag_ratio=0.03), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rej), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def ridge_dual(self):
        rows = [
            cmath(r"\hat\beta_{\text{ridge}}", r"=", r"(X'X + n\lambda I_p)^{-1} X'y", font_size=30),
            cmath(r"", r"=", r"X'(XX' + n\lambda I_n)^{-1} y = X'\hat\alpha", font_size=30),
            cmath(r"\text{prediction}", r":", r"\hat f(x) = \textstyle\sum_i \hat\alpha_i \, x_i'x", font_size=30),
            cmath(r"\text{replace } x_i'x", r"\to", r"k(x_i, x): \ \text{kernel ridge regression}", font_size=30),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"normalized squared loss; \ $\lambda>0$; \ $p$ unknowns"), why(r"the dual: \ $n$ unknowns, \ one per observation"),
                why(r"only inner products of the data appear"), why(r"Parts 29 and 54")]
        intro = label('Ridge can be solved through predictors or observations', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Duality also changes how we compute. Ridge regression's solution involves a p by p "
            "matrix. <bookmark mark='b'/> Its dual form gives the same answer through an n by n matrix: the "
            "coefficient vector is X transposed times a vector alpha, one dual weight per observation. When there are"
            " more predictors than observations, the dual is the cheap one. <bookmark mark='c'/> And in the dual, a "
            "prediction depends on the data only through inner products between observations. <bookmark mark='d'/> "
            "Replace those inner products by a positive-semidefinite kernel and you have kernel ridge regression, a "
            "flexible nonlinear method fitted by a linear solve, which Parts 29 and 54 develop."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def gap(self):
        d = load("cd")
        g = np.maximum(np.asarray(d["gaps"]), 1e-11)
        ks = np.arange(len(g))
        A = axes([0, len(g)], [-11, 1], x_length=8.0, y_length=4.2, xlabel=r"coordinate updates", ylabel=r"duality gap (log$_{10}$)",
                 xticks=[0, 40, 80, 120], yticks=[-10, -8, -6, -4, -2, 0], center=[-1.6, 0.3, 0])
        ax = A.ax
        ln = polyline(ax, ks, np.log10(g), PATH, 3.5)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=PATH) for a, b in zip(ks[::4], np.log10(g)[::4])])
        rows = fit_rows(VGroup(
            label(r"the lasso's dual: \ the scaled residual, \ pulled inside $\|X'\theta\|_\infty \le \lambda$", font_size=22),
            label(r"primal $-$ dual $\ge$ primal $-$ optimum", font_size=22, color=PATH),
            label(r"a certificate: \ stop when the gap is below $10^{-6}$", font_size=22, color=HIT),
            label(r"no need to know the optimum", font_size=22, color=GREY_A),
        ), 3.45, 0.4, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Duality has a practical payoff: a certificate of how close we are. The lasso has a "
            "dual problem, and from any current estimate we can build a feasible dual point, the residual, scaled to "
            "satisfy the dual's constraint. <bookmark mark='b'/> The gap between the primal and dual values bounds "
            "how far the current objective is from the optimum, even though we don't know the optimum. <bookmark "
            "mark='c'/> Here it is falling as coordinate descent runs on two correlated predictors: a factor of ten "
            "every dozen or so updates, ten orders of magnitude in a hundred and twenty. A small feasible duality gap"
            " certifies objective accuracy. Software can also use other stopping rules; glmnet uses coordinate-update"
            " and KKT checks. <bookmark mark='d'/> No guessing about convergence."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(dots), FadeIn(rows[1]), run_time=2.0)
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()
