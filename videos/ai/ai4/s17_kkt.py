from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import CONS, GRAD, HIST, PART, VALUE, load

POSC, NEGC = C.TRUE_P, GRAD
PRIMAL, DUAL = WHITE, CONS


def svm_checks_pass(d):
    if not all(d["solvers"][k]["success"] for k in ("primal", "dual")):
        return False
    tolerances, residuals = d["tolerances"], d["residuals"]
    groups = {"feasibility": ("primal_feasibility", "dual_nonnegative", "dual_equality", "duality_gap"),
              "stationarity": ("stationarity_w", "stationarity_b"),
              "complementarity": ("complementarity",)}
    return all(math.isfinite(float(residuals[k])) and abs(float(residuals[k])) <= tolerances[t]
               for t, names in groups.items() for k in names)


def svm_solver_verdict(d):
    if svm_checks_pass(d):
        return "Both optimizers report success and all listed feasibility, stationarity, slackness and gap checks pass their tolerances."
    return "The candidate solutions have not passed all solver and residual checks; the displayed values are not certified optima."


def diagnostic_number(value):
    return sci(value, 0) if math.isfinite(value) else r"\mathrm{unavailable}"


def clipped_separator(w, b, level, bounds):
    """Intersect a linear level set with a rectangle, including vertical lines."""
    xmin, xmax, ymin, ymax = bounds
    points = []
    if abs(w[1]) > 1e-14:
        for x in (xmin, xmax):
            y = (level - b - w[0] * x) / w[1]
            if ymin - 1e-12 <= y <= ymax + 1e-12:
                points.append((x, min(ymax, max(ymin, y))))
    if abs(w[0]) > 1e-14:
        for y in (ymin, ymax):
            x = (level - b - w[1] * y) / w[0]
            if xmin - 1e-12 <= x <= xmax + 1e-12:
                point = (min(xmax, max(xmin, x)), y)
                if not any(abs(point[0] - p[0]) + abs(point[1] - p[1]) < 1e-10 for p in points):
                    points.append(point)
    return points[:2] if len(points) >= 2 else None


class KKT(VoiceoverScene):
    def construct(self):
        self.card()
        self.conditions()
        self.duality()
        self.pictures()
        self.svm()

    def card(self):
        card = chapter_card(16, r"Inequalities, KKT and duality", r"What if the fence is a wall you may stay behind?",
                            lit=(1995,), part=PART)
        with self.voiceover("Chapter sixteen. Inequalities, and duality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def panel(self, c, x0, title, mu):
        ax = Axes(x_range=[-0.5, 2.6, 1], y_range=[-0.2, 2.2, 1], x_length=3.6, y_length=2.4, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to(x0)
        feas = Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(-0.5, 0)[0], height=2.4, stroke_width=0, fill_color=CONS,
                         fill_opacity=0.12).move_to(ax.c2p(0.25, 1.0))
        wall = DashedLine(ax.c2p(1, -0.2), ax.c2p(1, 2.2), color=CONS, stroke_width=2)
        lo_, hi_ = max(-0.5, c - math.sqrt(2.1 / 0.8)), min(2.6, c + math.sqrt(2.1 / 0.8))
        fc = ax.plot(lambda x: (x - c) ** 2 * 0.8, x_range=[lo_, hi_], color=WHITE, stroke_width=3)
        xs = min(c, 1.0)
        dot = Dot(ax.c2p(xs, (xs - c) ** 2 * 0.8), radius=0.08, color=GRAD)
        t = label(title, font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12)
        m = MathTex(rf"\mu = {mu:g}", font_size=26, color=CONS).next_to(ax, DOWN, buff=0.12)
        return VGroup(feas, wall, ax, fc, dot, t, m)

    def conditions(self):
        thm = theorem_card(
            r"KKT conditions",
            r"For $\min f(x)$ subject to $g_i(x) \le 0$: \ at a minimum, under a constraint qualification "
            r"(e.g. independent active constraint gradients), there are $\mu_i$ with "
            r"\\ $\nabla f + \sum_i \mu_i \nabla g_i = 0$ \ (stationarity), \quad $g_i(x) \le 0$ \ (feasible), \\ "
            r"$\mu_i \ge 0$ \ (dual feasible), \quad $\mu_i\, g_i(x) = 0$ \ (complementary slackness).",
            who=r"William Karush, master's thesis, Chicago (1939); \ Harold Kuhn and Albert Tucker (1951)",
            width=12.8, font_size=22).to_edge(UP, buff=0.3)
        p1 = self.panel(0.5, [-3.2, -2.1, 0], r"minimum inside: \ the wall is idle", 0)
        p2 = self.panel(2.0, [3.2, -2.1, 0], r"minimum on the wall: \ it pushes back", 2 * 0.8 * (2.0 - 1.0))
        tag = note(r"illustrative: \ $f = 0.8(x - c)^2$, \ $g = x - 1 \le 0$").next_to(thm, DOWN, buff=0.15).align_to(thm, RIGHT)
        with self.voiceover(
            "Most constraints are inequalities: a probability can't be negative, a margin must be at least one. "
            "William Karush worked out the conditions in his 1939 master's thesis; Harold Kuhn and Albert Tucker found "
            "them again in 1951. <bookmark mark='a'/> Under a constraint qualification, at a minimum there are "
            "multipliers mu, one per constraint, with "
            "the gradient of the Lagrangian zero, every constraint met, every multiplier non-negative, "
            "<bookmark mark='b'/> and each multiplier times its constraint equal to zero: complementary slackness. "
            "<bookmark mark='c'/> Either the minimum is inside and the wall is idle, its multiplier zero, "
            "<bookmark mark='d'/> or the minimum is on the wall. Its multiplier may be positive or zero; in this "
            "right-hand example it is positive and measures how hard the wall pushes."
        ) as vo:
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(p1), FadeIn(p2), FadeIn(tag))
            vo.wait_until("c")
            self.play(Indicate(p1, color=GRAD, scale_factor=1.03))
            vo.wait_until("d")
            self.play(Indicate(p2, color=GRAD, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def duality(self):
        rows = [
            cmath(r"q(\mu)", r"=", r"\inf_x\, \big(f(x) + \textstyle\sum_i \mu_i\, g_i(x)\big)", font_size=36,
                  colors={r"q(\mu)": DUAL}),
            cmath(r"q(\mu)", r"\le", r"f(x) \quad \text{for every feasible } x, \; \mu \ge 0", font_size=36,
                  colors={r"q(\mu)": DUAL}),
            cmath(r"d^* = \sup_{\mu \ge 0} q(\mu)", r"\le", r"p^* = \inf_{\text{feasible}} f", font_size=36),
            cmath(r"d^*", r"=", r"p^* \quad \text{for convex problems (with a strictly feasible point)}", font_size=34),
        ]
        whys = [why(r"the dual function: \ an infimum of lines in $\mu$, \ so concave, always", font_size=22),
                why(r"there $g_i(x) \le 0$, \ so the extra terms are $\le 0$", font_size=22),
                why(r"weak duality", font_size=22), why(r"strong duality \ (Slater)", font_size=22)]
        step = ladder(self, rows, whys, keep=4, top=2.7, x=-2.6, buff=0.65, edge=6.9)
        head = label(r"every constrained problem has a twin", font_size=28, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "The multipliers lead to a second problem. Fix them, and ask how low the Lagrangian can go over x: that's "
            "the dual function, q of mu. <bookmark mark='a'/> For any feasible x the added terms are at most zero, so the "
            "dual function is a lower bound on f, everywhere it can be met. <bookmark mark='b'/> The best lower bound, "
            "d star, is at most the true minimum, p star: weak duality, true for every problem. "
            "<bookmark mark='c'/> For convex problems with a strictly feasible point, the two are equal: strong "
            "duality. Both give the same optimal value."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pictures(self):
        d = load("kkt")
        lams, td = np.asarray(d["lams"]), np.asarray(d["toy_dual"])
        g1 = axes([0, 4, 1], [-0.6, 1.4, 0.5], x_length=5.0, y_length=3.2, xlabel=r"$\mu$", ylabel=r"$q(\mu)$",
                  xticks=[0, 2, 4], yticks=[0, 1], center=[-3.5, -0.4, 0])
        c1 = curve(g1.ax, lams, td, DUAL, 3.5)
        p1 = DashedLine(g1.ax.c2p(0, 1), g1.ax.c2p(4, 1), color=PRIMAL, stroke_width=2)
        t1 = label(r"convex: \ $\min x^2$ s.t. $x \ge 1$; \ $q(\mu) = \mu - \mu^2/4$", font_size=21, color=GREY_A)
        t1.next_to(g1, UP, buff=0.15)
        l1 = label(r"$p^* = 1 = d^*$", font_size=22, color=PRIMAL).next_to(g1.ax.c2p(2, 1), UP, buff=0.12)
        nl, nd = np.asarray(d["nc_l"]), np.asarray(d["nc_dual"])
        finite_dual = nd[np.isfinite(nd)]
        low = 2 * math.floor(min(float(finite_dual.min()), float(d["nc_p"]), -2.0) / 2)
        high = max(0.0, math.ceil(max(float(finite_dual.max()), float(d["nc_p"]))))
        g2 = axes([0, 6, 1], [low, high, 2], x_length=5.0, y_length=3.2, xlabel=r"$\mu$", ylabel=r"$\widetilde q_{\rm grid}(\mu)$",
                  xticks=[0, 2, 4, 6], yticks=list(np.arange(low, high + 0.1, 2)), center=[3.5, -0.4, 0])
        c2 = curve(g2.ax, nl, nd, DUAL, 3.5)
        p2 = DashedLine(g2.ax.c2p(0, d["nc_p"]), g2.ax.c2p(6, d["nc_p"]), color=PRIMAL, stroke_width=2)
        t2 = label(r"not convex: \ $\min x^4 - 3x^2 + x$ s.t. $x \ge \tfrac12$", font_size=21, color=GREY_A)
        t2.next_to(g2, UP, buff=0.15)
        l2 = label(rf"$\widetilde p_{{\rm grid}} = {d['nc_p']:.2f}$", font_size=22, color=PRIMAL).next_to(g2.ax.c2p(5, d["nc_p"]), UP, buff=0.1)
        l3 = label(rf"grid estimates: \ $\widetilde d = {d['nc_d']:.2f}$, \ $\widetilde p-\widetilde d = {d['nc_gap']:.2f}$", font_size=21, color=DUAL)
        l3.next_to(g2, DOWN, buff=0.2)
        pk = Dot(g2.ax.c2p(d["nc_lam"], d["nc_d"]), radius=0.07, color=DUAL)
        grid = d["grid"]
        tag = wrapped_label(rf"finite grid: \ $x\in[{grid['x_min']:g},{grid['x_max']:g}]$, \ spacing ${sci(grid['x_spacing'], 0)}$; "
                            rf"$\mu$ spacing ${grid['lambda_spacing']:g}$. \ Not a certified continuous dual bound.",
                            12.5, font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Two small examples. Minimize x squared, keeping x at least one. Its dual function is a hump that rises "
            "to touch the true minimum, one, exactly: no gap. <bookmark mark='a'/> Now a double well, the same kind of "
            f"constraint, and no convexity. On finite grids, the estimated primal value is {d['nc_p']:.2f} and "
            f"the best estimated dual value is {d['nc_d']:.2f}, a difference of {d['nc_gap']:.2f}. These are grid "
            "estimates, not a certified continuous dual bound. The exact weak-duality theorem still holds; this "
            "numerical picture illustrates how a gap can arise."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(t1), Create(p1), Create(c1), FadeIn(tag), run_time=1.6)
            self.play(FadeIn(l1))
            vo.wait_until("a")
            self.play(FadeIn(g2), FadeIn(t2), Create(p2), Create(c2), run_time=1.6)
            self.play(FadeIn(l2), FadeIn(l3), FadeIn(pk))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def svm(self):
        d = load("kkt")
        X, y = np.asarray(d["X"]), np.asarray(d["y"])
        w, b = np.asarray(d["w"]), float(d["b"])
        alpha = np.asarray(d["alpha"])
        alpha_tol = float(d["tolerances"]["alpha"])
        margin_tol = float(d["tolerances"]["margin"])
        sv = np.flatnonzero(alpha > alpha_tol).tolist()
        tight = np.flatnonzero(np.abs(np.asarray(d["margins"]) - 1) <= margin_tol).tolist()
        solver_verdict = svm_solver_verdict(d)
        ax = Axes(x_range=[-2.0, 2.5, 1], y_range=[-2.6, 2.8, 1], x_length=5.0, y_length=5.6, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-3.9, -0.4, 0])

        def line(c):
            segment = clipped_separator(w, b, c, (-2.0, 2.5, -2.6, 2.8))
            return Line(ax.c2p(*segment[0]), ax.c2p(*segment[1])) if segment else VectorizedPoint(ax.c2p(0, 0))

        mid = line(0).set_stroke(WHITE, 3)
        def margin(c):
            segment = clipped_separator(w, b, c, (-2.0, 2.5, -2.6, 2.8))
            return (DashedLine(ax.c2p(*segment[0]), ax.c2p(*segment[1]), color=GREY_B, stroke_width=2)
                    if segment else VectorizedPoint(ax.c2p(0, 0)))

        m1, m2 = margin(1), margin(-1)
        pts = VGroup(*[Dot(ax.c2p(*p), radius=0.07, color=POSC if c > 0 else NEGC) for p, c in zip(X, y)])
        rings = VGroup(*[Circle(radius=0.17, color=CONS, stroke_width=3).move_to(ax.c2p(*X[i])) for i in sv])
        # the multipliers, one bar per point
        amax = max(float(np.max(np.abs(alpha))), 1e-12)
        amin = min(0.0, float(alpha.min()) * 1.15)
        g2 = axes([0, len(alpha), 5], [amin, amax * 1.15, max(amax / 4, 1e-12)], x_length=5.6, y_length=1.6,
                  xlabel=rf"the ${len(alpha)}$ points", ylabel=r"multiplier $\alpha_i$", xticks=[], yticks=[0], font_size=18,
                  center=[3.4, -1.7, 0])
        bw = 5.6 / len(alpha) * 0.7
        abars = VGroup()
        for i, a in enumerate(alpha):
            base, tip = g2.ax.c2p(i + 0.5, 0), g2.ax.c2p(i + 0.5, a)
            if abs(tip[1] - base[1]) < 1e-12:
                abars.add(Line(base + LEFT * bw / 2, base + RIGHT * bw / 2, color=GREY_D, stroke_width=1))
            else:
                abars.add(Rectangle(width=bw, height=abs(tip[1] - base[1]), stroke_width=0,
                                    fill_color=CONS if i in sv else (C.PENALTY if a < 0 else GREY_D), fill_opacity=0.9)
                          .move_to((base + tip) / 2))
        eqs = VGroup(
            label(r"primal: \ $\min \tfrac12\|w\|^2$ \ s.t. \ $y_i(w\cdot x_i + b) \ge 1$", font_size=22, color=PRIMAL),
            label(r"dual: \ $\max_{\alpha \ge 0} \textstyle\sum_i \alpha_i - \tfrac12 \sum_{ij} \alpha_i \alpha_j y_i y_j\, "
                  r"x_i \cdot x_j$", font_size=22, color=DUAL),
            label(r"$\sum_i\alpha_i y_i=0$: \ stationarity in the free intercept $b$", font_size=22, color=DUAL),
            label(rf"solver candidates: \ $p = {d['p_star']:.6f}$, \ $d = {d['d_star']:.6f}$", font_size=22, color=WHITE),
            wrapped_label(r"$\alpha_i > 0 \Rightarrow y_i f(x_i)=1$ at an optimum; \ the reverse can fail in degenerate data", 5.1,
                          font_size=22, color=CONS),
            wrapped_label(rf"rings: \ ${len(sv)}$ multipliers above ${sci(alpha_tol, 0)}$; \ "
                          rf"${len(tight)}$ margins within ${sci(margin_tol, 0)}$ of $1$", 6.2, font_size=20, color=GREY_A),
            wrapped_label(solver_verdict, 6.2, font_size=20, color=GREY_B),
            wrapped_label(rf"feasibility residual ${diagnostic_number(max(d['residuals'][k] for k in ('primal_feasibility', 'dual_nonnegative', 'dual_equality')))}$, "
                          rf"tolerance ${sci(d['tolerances']['feasibility'], 0)}$; "
                          rf"stationarity residual ${diagnostic_number(max(d['residuals']['stationarity_w'], d['residuals']['stationarity_b']))}$, "
                          rf"tolerance ${sci(d['tolerances']['stationarity'], 0)}$; "
                          rf"slackness ${diagnostic_number(d['residuals']['complementarity'])}$, tolerance ${sci(d['tolerances']['complementarity'], 0)}$; "
                          rf"absolute gap ${diagnostic_number(abs(d['residuals']['duality_gap']))}$",
                          6.2, font_size=20, color=GREY_A),
        )
        VGroup(eqs[0], eqs[1], eqs[2], eqs[3], eqs[6], eqs[7]).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.3, 2.8, 0], aligned_edge=UP)
        eqs[4].next_to(ax, UP, buff=0.15)
        eqs[5].move_to([3.3, -3.3, 0])
        hist = cite(r"B.~Boser, I.~Guyon \& V.~Vapnik (1992); \ C.~Cortes \& V.~Vapnik (1995)", corner=UR)
        with self.voiceover(
            "Duality's most famous use: the support vector machine of Part 6. Find the widest street between two "
            "classes: the smallest w that puts every point at least one unit of margin from the line. "
            "<bookmark mark='a'/> Its dual has one multiplier per point, and depends on the points only through their "
            "dot products, which is what lets kernels in. Minimizing over the free intercept also requires the "
            f"label-weighted multipliers to sum to zero. <bookmark mark='b'/> We attempted separate primal and dual "
            f"solves on {len(X)} points. {solver_verdict} The candidate objective values are displayed with six "
            f"decimal places. <bookmark mark='c'/> We ring the points whose {len(sv)} multipliers exceed the stated "
            f"numerical zero threshold; {len(tight)} points have margins within the stated tolerance of one. At an optimum, "
            "a positive multiplier forces a point onto a margin, "
            "but a margin point can have a zero multiplier in degenerate data. Bernhard Boser, Isabelle Guyon and "
            "Vladimir Vapnik built the method on this dual in "
            "1992."
        ) as vo:
            self.play(Create(ax), FadeIn(pts), FadeIn(eqs[0]), FadeIn(hist))
            self.play(Create(mid), Create(m1), Create(m2))
            vo.wait_until("a")
            self.play(FadeIn(eqs[1]), FadeIn(eqs[2]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[3]), FadeIn(eqs[6]), FadeIn(eqs[7]))
            vo.wait_until("c")
            self.play(FadeOut(eqs[6]), FadeOut(eqs[7]), run_time=0.5)
            self.play(FadeIn(g2), LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in abars], lag_ratio=0.05),
                      Create(rings), FadeIn(eqs[4]), FadeIn(eqs[5]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
