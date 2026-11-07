from __future__ import annotations

import numpy as np

from videos.stats.stats21.common import *  # noqa: F403


class Lagrange(VoiceoverScene):
    def construct(self):
        self.card()
        self.multinomial()
        self.boundary()
        self.conditions()
        self.lasso_kkt()
        self.isotonic()
        self.uses()

    def card(self):
        card = chapter_card(2, r"Lagrange and KKT", r"Optimizing under constraints", part=PART)
        with self.voiceover("Chapter two. Lagrange multipliers, and the Karush–Kuhn–Tucker conditions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def multinomial(self):
        rows = [
            cmath(r"\max_p", r"", r"\textstyle\sum_k n_k \log p_k \ \ \text{subject to} \ \ \textstyle\sum_k p_k = 1", font_size=30),
            cmath(r"\mathcal{L}(p, \lambda)", r"=", r"\textstyle\sum_k n_k \log p_k - \lambda\big(\textstyle\sum_k p_k - 1\big)", font_size=30),
            cmath(r"\partial \mathcal{L} / \partial p_k = 0", r":", r"n_k / p_k = \lambda", font_size=30),
            cmath(r"\textstyle\sum_k p_k = 1", r"\Rightarrow", r"\lambda = n, \ \ \hat p_k = n_k / n", font_size=30),
        ]
        rows[3][2].set_color(TRUE)
        whys = [why(r"a multinomial likelihood: \ Part 14"), why(r"Lagrange (1788): \ price the constraint"),
                why(r"at the optimum, \ every gradient is the same multiple"), why(r"the sample proportions, \ derived")]
        intro = label('A multiplier enforces the probability-sum constraint', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The simplest constrained estimator: the probabilities of K categories, from counts "
            "n k. The log likelihood is the sum of n k log p k, but the p's must add to one. <bookmark mark='b'/> "
            "Lagrange's idea: add the constraint with a price lambda, and optimize freely. <bookmark mark='c'/> With "
            "positive counts, the optimum is interior: setting each derivative to zero makes n k over p k the same "
            "multiplier. Zero counts require the corresponding boundary conditions. <bookmark mark='d'/> The "
            "constraint fixes lambda at n, and the estimates are the sample proportions, as everyone guessed, now "
            "derived."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def boundary(self):
        d = load("kkt")
        panels = VGroup()
        anims = []
        for k, (key, cx) in enumerate((("binding", -3.4), ("slack", 3.4))):
            r = d[key]
            p, ll = np.asarray(r["p"]), np.asarray(r["ll"])
            m = (p > 0.15) & (p < 0.85)
            lo = float(ll[m].min())
            A = axes([0.15, 0.85], [lo, float(ll.max()) + 2], x_length=5.4, y_length=3.6, xlabel=r"$p$", ylabel=r"log likelihood",
                     xticks=[0.2, 0.4, 0.5, 0.6, 0.8], center=[cx, 0.6, 0], font_size=18)
            ax = A.ax
            feas = Rectangle(width=ax.c2p(0.5, lo)[0] - ax.c2p(0.15, lo)[0], height=ax.c2p(0, float(ll.max()) + 2)[1] - ax.c2p(0, lo)[1],
                             stroke_width=0, fill_color=HIT, fill_opacity=0.12).move_to(ax.c2p(0.15, lo), aligned_edge=DL)
            cv = curve(ax, p[m], ll[m], FIT, 3.5)
            mle = Dot(ax.c2p(r["phat"], float(np.interp(r["phat"], p, ll))), color=GREY_B, radius=0.08)
            con = Dot(ax.c2p(r["pc"], r["ll_c"]), color=PATH, radius=0.1)
            t = label(rf"{r['k']} of {r['n']}: \ $\hat p = {r['phat']:.1f}$; \ multiplier {r['mult']:.0f}", font_size=22,
                      color=PATH).next_to(A, DOWN, buff=0.35)
            panels.add(VGroup(A, feas, cv, mle, con, t))
        head = label(r"Constrained likelihood: \ a maximum may bind or lie inside $p \le 1/2$", font_size=36, color=HIT).move_to([0, 3.3, 0])
        if head.width > 12.5:
            head.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Inequality constraints are subtler. Suppose theory says a probability can't exceed "
            "a half. <bookmark mark='b'/> On the left, thirty successes in fifty trials: the unconstrained estimate, "
            "point six, is outside the allowed region, so the constrained maximum sits on the boundary, at a half. "
            "There the likelihood is still rising, with slope twenty: that slope is the multiplier, the price the "
            "constraint is charging. <bookmark mark='c'/> On the right, twenty in fifty: the estimate, point four, is"
            " inside the region. The constraint doesn't bind, and its multiplier is zero. A slack constraint must "
            "have multiplier zero, and a positive multiplier requires a binding constraint. A binding constraint can "
            "also have multiplier zero. That is complementary slackness."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(panels[0][:4]), run_time=1.5)
            self.play(FadeIn(panels[0][4], scale=1.5), FadeIn(panels[0][5]))
            vo.wait_until("c")
            self.play(FadeIn(panels[1][:4]), run_time=1.5)
            self.play(FadeIn(panels[1][4], scale=1.5), FadeIn(panels[1][5]))
        self.wait(1.0)
        self.clear_scene()

    def conditions(self):
        rows = [
            cmath(r"\text{stationarity}", r":", r"\nabla f(x) + \textstyle\sum_i \mu_i \nabla g_i(x) = 0", font_size=30),
            cmath(r"\text{primal feasibility}", r":", r"g_i(x) \le 0", font_size=30),
            cmath(r"\text{dual feasibility}", r":", r"\mu_i \ge 0", font_size=30),
            cmath(r"\text{complementary slackness}", r":", r"\mu_i\, g_i(x) = 0", font_size=30),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"minimize $f$ subject to $g_i(x) \le 0$"), why(r"the constraints hold"), why(r"prices are never negative"),
                why(r"a price only where a constraint binds")]
        intro = label('KKT combines stationarity, feasibility and slackness', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "In general, to minimize f subject to constraints g i of x at most zero, Karush in 1939 and Kuhn and "
            "Tucker in 1951 gave four conditions. <bookmark mark='a'/> Stationarity: the gradient of f is balanced by"
            " the constraints' gradients, weighted by multipliers mu. <bookmark mark='b'/> The constraints hold. "
            "<bookmark mark='c'/> The multipliers are non-negative. <bookmark mark='d'/> And complementary slackness:"
            " each multiplier is zero unless its constraint is binding. At an optimum, necessity requires an "
            "appropriate constraint qualification. For differentiable convex objectives and constraints, satisfying "
            "the KKT conditions is sufficient for global optimality."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lasso_kkt(self):
        rows = [
            cmath(r"\tfrac1n X_j'(y - X\hat\beta)", r"=", r"\lambda\, s_j", font_size=30),
            cmath(r"\hat\beta_j \ne 0", r":", r"s_j = \operatorname{sign}(\hat\beta_j)", font_size=30),
            cmath(r"\hat\beta_j = 0", r":", r"s_j \in [-1, 1]", font_size=30),
            cmath(r"\text{so}", r":", r"|\tfrac1n X_j'r| < \lambda \Rightarrow \hat\beta_j = 0;\ \text{equality can be active}", font_size=30),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"the lasso's stationarity, \ with a subgradient"), why(r"active: \ correlation exactly $\pm\lambda$"),
                why(r"the kink of $|b|$ at zero"), why(r"strict inequality forces a zero; \ equality alone does not")]
        intro = label('Strict KKT inequality forces a zero lasso coefficient', font_size=36).move_to([0, 3.35, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> The lasso's KKT conditions explain its zeros. The absolute value has no derivative "
            "at zero, but it has a subgradient, any number between minus one and one. Stationarity says each "
            "predictor's correlation with the residual equals lambda times s j. <bookmark mark='b'/> If the "
            "coefficient is non-zero, s j is its sign, so the correlation is exactly plus or minus lambda. <bookmark "
            "mark='c'/> If it's zero, s j can be anything in between. <bookmark mark='d'/> A zero coefficient "
            "requires absolute residual inner product divided by n at most lambda. Strictly below lambda forces a "
            "zero; at equality, the coefficient can be zero or non-zero: Part 19's diamond corners, as an equation."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def isotonic(self):
        d = load("pava")
        mid = np.log10(np.asarray(d["mid"]))
        A = axes([0.6, 2.6], [0.1, 0.75], x_length=8.0, y_length=4.4, xlabel=r"income, \ thousands (log scale)", ylabel=r"share voting Blue",
                 xticks=[1, 1.5, 2, 2.5], yticks=[0.2, 0.4, 0.6], center=[-1.6, 0.3, 0], xfmt=lambda v: f"{10 ** v:.0f}",
                 yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        raw = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=GREY_B) for a, b in zip(mid, d["share"])])
        fit = VGroup()
        for s, e in d["blocks"]:
            x0 = mid[s] - (0.02 if s == e else 0)
            x1 = mid[e] + (0.02 if s == e else 0)
            fit.add(Line(ax.c2p(x0, d["fit"][s]), ax.c2p(x1, d["fit"][s]), color=PATH, stroke_width=5))
        truth = polyline(ax, mid, d["truth"], TRUE, 2.5)
        rows = fit_rows(VGroup(
            label(r"1,500 adults in 25 income bins", font_size=22),
            label(rf"grey: \ raw shares, \ {d['violations']} dips", font_size=22, color=GREY_B),
            label(r"gold: \ isotonic fit, \ never falling", font_size=22, color=PATH),
            label(r"thin: \ the World's truth", font_size=22, color=TRUE),
            label(r"PAVA: \ pool any adjacent pair that breaks the order", font_size=20, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A constraint that's common in practice: a relationship known to go one way. In the World, "
            "support for Blue rises with income. Here are fifteen hundred adults in twenty-five income bins, and the share "
            "voting Blue in each. <bookmark mark='b'/> Sampling noise makes the raw shares dip eight times. "
            "<bookmark mark='c'/> Isotonic regression finds the closest non-decreasing fit, least squares subject to the order "
            "constraints. Its KKT conditions lead to a simple algorithm: pool adjacent violators. Whenever two neighbours are "
            "in the wrong order, replace both by their weighted average, and repeat. <bookmark mark='d'/> The result is a "
            "staircase, close to the World's truth, with no assumption about its shape except that it never falls."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ the World's vote"))
            self.play(FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in raw], lag_ratio=0.05), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(f) for f in fit], lag_ratio=0.2), FadeIn(rows[2]), FadeIn(rows[4]), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(truth), FadeIn(rows[3]))
        self.clear_scene()

    def uses(self):
        rows = fit_rows(VGroup(
            label(r"constrained MLEs: \ proportions, \ ordered means (isotonic regression)", font_size=24, color=FIT),
            label(r"estimates on a boundary: \ a variance of zero, \ a probability of one", font_size=24, color=RES),
            label(r"there, \ Wald and LR tests change their distributions: \ Parts 46--47", font_size=22, color=GREY_A),
            label(r"multipliers as sensitivities: \ how much the optimum moves if the constraint relaxes", font_size=24, color=PATH),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Constraints are everywhere in statistics: probabilities that add to one, means "
            "known to be ordered, which isotonic regression handles. <bookmark mark='b'/> Sometimes the best estimate"
            " sits on a boundary: a variance component of zero, a probability of one. <bookmark mark='c'/> There the "
            "usual chi-squared theory of tests breaks down, a subject for Parts 46 and 47. <bookmark mark='d'/> Under"
            " suitable sensitivity regularity, a multiplier gives the local derivative of the optimal value when the "
            "constraint is relaxed, the shadow price of the bakery."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
