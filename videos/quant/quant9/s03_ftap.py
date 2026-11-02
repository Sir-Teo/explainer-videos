from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.zh_text import verbatim
from videos.quant.quant9.common import ARB, CALL, FWD, PART, Q_C, answer_under, load, pause_at

VARS = [r"\psi_1", r"\psi_2", r"\psi_3", r"t", r"s_1", r"s_2", r"s_3"] + [rf"a_{k}" for k in range(1, 6)]


class FTAP(VoiceoverScene):
    def construct(self):
        f = load("ftap")
        self.card()
        self.theorem()
        self.proof()
        self.cone(f)
        self.lab(f)
        self.predict()

    def card(self):
        c = chapter_card(4, r"The fundamental theorem, proved and solved", r"Why must a price lie inside a cone?",
                         lit=(1979,), part=PART)
        with self.voiceover("Chapter four. The fundamental theorem of asset pricing, proved and solved."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theorem(self):
        t = theorem_card(r"The fundamental theorem (one period, finitely many states)",
                         r"There is no arbitrage if and only if there are strictly positive state prices "
                         r"$\psi \gg 0$ with $p = D\psi$: every asset's price is the sum over states of what it pays "
                         r"there, times that state's price.",
                         who=r"Harrison and Kreps (1979); the lemma: Farkas (1902), Stiemke (1915)", color=Q_C,
                         width=10.6, font_size=26).move_to(UP * 0.4)
        with self.voiceover(
            "The theorem. In a market with one period and finitely many states, there is no arbitrage if and only if "
            "there are strictly positive state prices, one per state, such that every asset's price is the sum over "
            "states of what it pays there, times that state's price. <bookmark mark='a'/> Michael Harrison and David "
            "Kreps stated it this way in 1979. The mathematics underneath is a lemma about linear inequalities, from "
            "Gyula Farkas in 1902 and, in the strictly positive form we need, Erich Stiemke in 1915."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(t, color=Q_C, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"\theta\cdot p", r"=", r"\theta\cdot D\psi = \psi\cdot D^\top\theta > 0", font_size=36,
                      colors={r"\theta\cdot p": Q_C}),
                cmath(r"L", r"=", r"\{(-\theta\cdot p,\ D^\top\theta)\} \subset \mathbb{R}^{1+m},\quad L \cap "
                      r"\mathbb{R}^{1+m}_+ = \{0\}", font_size=32, colors={r"L": FWD}),
                cmath(r"\lambda\cdot x > 0\ \ \forall x\in\Delta", r",", r"\lambda\cdot \ell = 0\ \ \forall \ell \in L",
                      font_size=34, colors={r"\lambda\cdot x > 0\ \ \forall x\in\Delta": Q_C}),
                cmath(r"-\lambda_0\,\theta\cdot p + \lambda_{1:m}\cdot D^\top\theta", r"=", r"0\ \ \forall\theta "
                      r"\ \Rightarrow\ p = D\psi,\ \ \psi = \lambda_{1:m}/\lambda_0 \gg 0", font_size=32,
                      colors={r"0\ \ \forall\theta \ \Rightarrow\ p = D\psi,\ \ \psi = \lambda_{1:m}/\lambda_0 \gg 0": Q_C})]
        whys = [why(r"($\Leftarrow$) if $D^\top\theta \ge 0$ and is not zero, its inner product with a strictly "
                    r"positive $\psi$ is positive: every portfolio that never loses costs something", 21),
                why(r"($\Rightarrow$) the cost and payoffs of every portfolio form a subspace $L$; no arbitrage says it "
                    r"meets the non-negative orthant only at zero", 21),
                why(r"so $L$ misses the simplex $\Delta$ (compact, convex): a hyperplane separates them strictly, and a "
                    r"linear function bounded on a subspace is zero on it; $x = e_j$ gives every $\lambda_j > 0$", 21),
                why(r"write out $\lambda\cdot\ell = 0$ for every portfolio: the prices are positive combinations of the "
                    r"payoffs", 21)]
        step = ladder(self, rows, whys, keep=4, top=3.3, x=-0.4, buff=0.62, edge=6.9)
        with self.voiceover(
            "The easy direction first. Suppose positive state prices exist, and take any portfolio whose payoff is "
            "never negative and not zero. Its price is its payoff, dotted with the state prices: a sum of "
            "non-negative terms, at least one positive. So it costs something. No free lunch. "
            "<bookmark mark='a'/> Now the hard direction. Collect, for every portfolio, its cost with a minus sign "
            "and its payoffs: a subspace L. No arbitrage says this subspace touches the non-negative orthant only at "
            "the origin. <bookmark mark='b'/> So it misses the simplex of non-negative vectors summing to one, which "
            "is compact and convex. A hyperplane separates them strictly, and because a linear function that is "
            "bounded on a subspace must vanish on it, the hyperplane's normal lambda is orthogonal to L and strictly "
            "positive. <bookmark mark='c'/> Write out that orthogonality for every portfolio, divide by lambda's "
            "first entry, and the price vector is the payoff matrix times a strictly positive vector. That is the "
            "theorem, and the normal you saw in three dimensions is lambda."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    def cone(self, f):
        S = np.array([80.0, 100.0, 125.0])
        g = axes([0, 1.4], [0, 150], x_length=5.6, y_length=5.0, xlabel=r"pays in bonds", ylabel=r"the stock pays",
                 xticks=[0, 0.5, 1.0], yticks=[0, 50, 100, 150], font_size=17)
        g.to_edge(LEFT, buff=0.9).shift(DOWN * 0.2)
        ax = g.ax
        o = ax.c2p(0, 0)
        cone = Polygon(o, ax.c2p(1.4, 80 * 1.4), ax.c2p(150 / 125, 150), stroke_width=0, fill_color=Q_C,
                       fill_opacity=0.2)
        arrows = VGroup(*[Arrow(o, ax.c2p(1, s), buff=0, color=FWD, stroke_width=4, max_tip_length_to_length_ratio=0.06)
                          for s in S])
        slabs = VGroup(*[label(rf"state {i + 1}", font_size=18, color=FWD).next_to(ax.c2p(1, s), RIGHT, buff=0.1)
                         for i, s in enumerate(S)])
        p = ValueTracker(100.0)
        dot = always_redraw(lambda: Dot(ax.c2p(1, p.get_value()), radius=0.1,
                                        color=Q_C if p.get_value() < 124.999 else ARB))
        rd = DecimalNumber(100, num_decimal_places=0, font_size=30, color=Q_C)
        rd.add_updater(lambda m: m.set_value(p.get_value()))
        th = f["ftap_130"]["theta"]
        side = VGroup(
            VGroup(label(r"price vector: bond 1, stock", font_size=22, color=Q_C), rd).arrange(RIGHT, buff=0.15),
            wrapped_label(r"the state arrows are what the two assets pay in each state; the purple cone is every "
                          r"positive combination of them", 4.8, 20, GREY_A),
            wrapped_label(r"inside the cone: positive state prices exist (the theorem); on its edge at 125 or outside "
                          r"it: an arbitrage", 4.8, 20, Q_C),
            MathTex(rf"130:\ \theta = ({th[0]:+.2f}\ \text{{bonds}},\ {th[1]:+.4f}\ \text{{stock}})", font_size=26,
                    color=ARB),
            wrapped_label(r"this is the dual view of chapter 3: there, the free payoffs' line pierced the corner; "
                          r"here, the price leaves the cone", 4.8, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The same fact has a second picture, in the space of prices. Each state is an arrow: what the bond and "
            "the stock pay in it. Positive combinations of the arrows fill this cone. <bookmark mark='a'/> The "
            "theorem says no arbitrage exactly when the price vector, one for the bond and a hundred for the stock, "
            "lies strictly inside the cone. <bookmark mark='b'/> Raise the stock's price. The dot climbs toward the "
            "cone's upper edge, the arrow of the best state, and at a hundred and twenty-five it sits on the edge. "
            "Past it, at a hundred and thirty, it is outside, and the linear program returns the separating "
            "portfolio instead: hold bonds, short a little stock. <bookmark mark='c'/> This is the dual of the "
            "previous chapter's picture: there the line of free payoffs pierced the corner; here the price leaves "
            "the cone, at the same moment."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), FadeIn(slabs),
                      FadeIn(side[1]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(cone), FadeIn(dot), FadeIn(side[0]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(p.animate.set_value(125.0), run_time=3, rate_func=smooth)
            self.play(p.animate.set_value(130.0), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
        rd.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def lab(self, f):
        with verbatim():
            card = lab_card(r"a teaching simplex", [
                "def simplex(c, A, b):            # min c.x, A x = b, x >= 0",
                "    T = hstack([A, I, b]); basis = artificials",
                "    while True:",
                "        r = cost - cost[basis] @ T[:, :-1]  # reduced costs",
                "        enter = [j for j in cols if r[j] < 0]",
                "        if not enter: return T, basis       # optimal",
                "        j = enter[0]                 # Bland's rule: never cycles",
                "        ratio = T[:, -1] / T[:, j]   # where T[:, j] > 0",
                "        i = argmin(ratio)            # who leaves the basis",
                "        T[i] /= T[i, j]; eliminate(T, column=j, row=i)",
                "        basis[i] = j; trace.append(objective)",
            ], source="explainer/quant/house/arbitrage.py", width=7.6, font_size=17).to_corner(UL, buff=0.3)
        s100, s130 = f["simplex_100"], f["simplex_130"]
        st100, st130 = s100["steps"], s130["steps"]
        n = max(len(st100), len(st130))
        g = axes([0, n], [0, 135], x_length=4.6, y_length=2.8, xlabel=r"pivot", ylabel=r"infeasibility (phase 1)",
                 xticks=list(range(0, n + 1)), yticks=[0, 50, 100], font_size=15)
        g.to_corner(UR, buff=0.4)
        ax = g.ax
        y100 = [101.0] + [s["obj"] for s in st100]
        y130 = [131.0] + [s["obj"] for s in st130]
        k = ValueTracker(0)

        def path(ys, col):
            def mk():
                v = k.get_value()
                pts = [ax.c2p(i, y) for i, y in enumerate(ys) if i <= v]
                if len(pts) < 2:
                    return VGroup(Dot(pts[0], radius=0.06, color=col))
                return VGroup(VMobject(color=col, stroke_width=3).set_points_as_corners(pts),
                              *[Dot(q, radius=0.05, color=col) for q in pts])
            return always_redraw(mk)

        a100, a130 = path(y100, Q_C), path(y130, ARB)
        leg = legend([(Q_C, r"stock at 100"), (ARB, r"stock at 130")], font_size=17).next_to(g, DOWN, buff=0.15)
        x100 = s100["x"]
        fk = s130["farkas"]
        res = VGroup(
            MathTex(rf"100:\ \psi = ({x100[0]:.3f},\ {x100[1]:.3f},\ {x100[2]:.3f}),\ \ t^* = {x100[3]:.3f}",
                    font_size=26, color=Q_C),
            MathTex(rf"130:\ \text{{infeasible; certificate }}\ \theta = ({fk[0]:.0f}\ \text{{bonds}},\ {fk[1]:.0f}\ "
                    rf"\text{{stock}})", font_size=26, color=ARB),
            MathTex(rf"\text{{cost }} {fk[0]:.0f} - 130 = {fk[0] - 130:.0f},\ \ \text{{payoff }} (45,\ 25,\ 0)",
                    font_size=26, color=ARB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        lp = MathTex(r"\max\ t\ \ \text{s.t.}\ \ D\psi = p,\ \ \psi \ge t\,\mathbf{1}", font_size=28, color=Q_C)
        lp.next_to(leg, DOWN, buff=0.2)
        with self.voiceover(
            "The House decides the theorem by linear programming: maximize the smallest state price t, subject to "
            "prices equal to payoffs times state prices. A positive optimum means no arbitrage. Here is the "
            "teaching version of the simplex method that solves it, a dozen lines. <bookmark mark='a'/> Start from "
            "artificial variables that make the equations trivially true, then pivot: pick a column whose reduced "
            "cost is negative, the lowest-numbered one, which is Bland's rule and guarantees it never cycles; the "
            "ratio test picks which variable leaves; eliminate; repeat. <bookmark mark='b'/> Run it with the stock "
            f"at a hundred. In {len(st100)} pivots the artificial variables are driven to zero, and the state "
            f"prices appear: the smallest is {x100[3]:.3f}, positive. <bookmark mark='c'/> Now at a hundred and "
            f"thirty. After {len(st130)} pivots it is stuck: the artificial variables cannot be removed, so no "
            "state prices exist. And the stuck tableau's dual variables are the certificate: a hundred and "
            "twenty-five in bonds, short one share. It costs minus five and pays forty-five, twenty-five, or zero. "
            "Farkas's lemma, run by a machine."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(g), FadeIn(lp))
            vo.wait_until("a")
            self.play(Indicate(card.code[6], color=Q_C, scale_factor=1.04))
            vo.wait_until("b")
            self.add(a100)
            self.play(FadeIn(leg[0]))
            self.play(k.animate.set_value(len(st100)), run_time=3, rate_func=linear)
            self.play(FadeIn(res[0]))
            vo.wait_until("c")
            k.set_value(0)
            self.remove(a100)
            frozen = VGroup(VMobject(color=Q_C, stroke_width=3).set_points_as_corners(
                [ax.c2p(i, y) for i, y in enumerate(y100)]))
            self.add(frozen, a130)
            self.play(FadeIn(leg[1]))
            self.play(k.animate.set_value(len(st130)), run_time=3, rate_func=linear)
            self.play(FadeIn(res[1]), FadeIn(res[2]))
        a130.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"Split the states more finely: add a state between every two. For which stock prices between "
                        r"80 and 125 does the program stop finding state prices?")
        with self.voiceover(
            "Pause and predict. Split the states more finely, adding a state between every two. For which stock "
            "prices between eighty and a hundred and twenty-five does the program stop finding state prices? "
            "<bookmark mark='a'/> None. More states add more arrows inside the same extremes, so the cone can only "
            "grow. What decides arbitrage is the best and the worst the stock can pay, not how many states lie "
            "between."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"none: new states add arrows between the extremes, so the cone never "
                                                r"shrinks; only the worst and best payoffs matter")))
        self.wait(0.4)
        self.clear_scene()
