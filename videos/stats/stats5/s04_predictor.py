from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403


class Predictor(VoiceoverScene):
    def construct(self):
        self.card()
        self.incomes()
        self.proof()
        self.tower()
        self.projection()

    def card(self):
        card = chapter_card(3, r"Conditional expectation", r"The best possible prediction of $Y$ from $X$", lit=(), part=PART)
        with self.voiceover("Chapter three. Conditional expectation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def incomes(self):
        d = load("predictor")
        age, inc = np.asarray(d["age"]), np.asarray(d["inc"])
        ages, cond = np.asarray(d["ages"]), np.asarray(d["cond"])
        A = axes([18, 96], [1.5, 6.0], x_length=7.8, y_length=4.6, xlabel=r"age", ylabel=r"log income (thousands)",
                 xticks=[20, 40, 60, 80], yticks=[2, 3, 4, 5], center=[-2.2, -0.4, 0])
        ax = A.ax
        pts = scatter(ax, age + np.random.Generator(np.random.PCG64(1)).uniform(-0.4, 0.4, len(age)), inc, color=WORLD,
                      radius=0.018, opacity=0.4)
        cst = Line(ax.c2p(18, d["const"]), ax.c2p(96, d["const"]), color=GREY_A, stroke_width=3)
        lin = Line(ax.c2p(18, d["b0"] + d["b1"] * 18), ax.c2p(96, d["b0"] + d["b1"] * 96), color=S.EST, stroke_width=3)
        cm = curve(ax, ages, cond, COND, 4)
        rows = VGroup(
            MathTex(rf"\text{{best constant: MSE }} {d['mse_const']:.3f}", font_size=26, color=GREY_A),
            MathTex(rf"\text{{best line: MSE }} {d['mse_line']:.3f}\ \ (R^2 = {d['r2_line']:.3f})", font_size=26, color=S.EST),
            MathTex(rf"E[Y \mid X]:\ \text{{MSE }} {d['mse_cond']:.3f}\ \ (R^2 = {d['r2_cond']:.3f})", font_size=26, color=COND),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, 1.8, 0])
        hump = label(r"the career curve: \ rises, \ levels off, \ drops at retirement (67); \ no line can follow it", font_size=22,
                     color=GREY_B).move_to([4.2, 0.0, 0])
        if hump.width > 5.4:
            hump.width = 5.4
        tag = simulated_tag(r"simulated: 3,000 of the World's adults (MSE over all)")
        with self.voiceover(
            "Suppose we must predict a variable Y from another, X, and we're judged by mean squared error. What's "
            "the best possible prediction? <bookmark mark='a'/> Here are the World's adults: age across, the "
            "logarithm of income up. <bookmark mark='b'/> Ignoring age, the best constant is the mean. "
            "<bookmark mark='c'/> The best straight line in age barely helps: in the World, incomes rise through the "
            "early career, level off, and drop at retirement, at sixty-seven, and a line can't follow that. <bookmark mark='d'/> The best prediction of any kind is the "
            "conditional mean: for each age, the average log income of adults of that age. It follows the career "
            f"curve, step and all, and its mean squared error, {d['mse_cond']:.3f}, is the smallest any function of age can "
            "achieve."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(pts, lag_ratio=0.0005), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(cst), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(lin), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Create(cm), FadeIn(rows[2]), FadeIn(hump), run_time=2.5)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"E[(Y - g(X))^2]", r"=", r"E[(Y - m(X) + m(X) - g(X))^2]", font_size=32),
            cmath(r"E[(Y - g(X))^2]", r"=", r"E[(Y - m(X))^2]", r"+", r"E[(m(X) - g(X))^2]", r"+", r"2E[(Y - m(X))(m(X) - g(X))]",
                  font_size=28),
            cmath(r"E[(Y - m(X))\, h(X)]", r"=", r"E\big[h(X)\, E[Y - m(X) \mid X]\big]", r"=", r"0", font_size=30),
            cmath(r"E[(Y - g(X))^2]", r"\ge", r"E[(Y - m(X))^2]", font_size=34),
        ]
        rows[3][2].set_color(COND)
        whys = [why(r"$m(X) = E[Y \mid X]$; \ add and subtract"), why(r"expand"),
                why(r"condition on $X$: \ the cross term vanishes"), why(r"equality only for $g = m$")]
        with self.voiceover(
            "The proof is Part 1's Pythagoras, one level up. <bookmark mark='a'/> Write m of X for the conditional "
            "mean, and compare any other predictor g of X. Add and subtract m. <bookmark mark='b'/> Expand the "
            "square: three terms. <bookmark mark='c'/> The cross term vanishes: condition on X, and the error Y minus "
            "m of X averages to zero for every value of X, whatever function of X it's multiplied by. "
            "<bookmark mark='d'/> So any predictor's error is the conditional mean's error plus something "
            "nonnegative. The conditional mean is the best predictor, uniquely."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.8, buff=0.55, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=k in (1, 3))
        self.clear_scene()

    def tower(self):
        rows = [
            cmath(r"E\big[E[Y \mid X]\big]", r"=", r"E[Y]", font_size=40),
            cmath(r"E[Y]", r"=", r"\sum_x P(X = x)\, E[Y \mid X = x]", font_size=36),
        ]
        rows[0][0].set_color(COND)
        whys = [why(r"the tower property"), why(r"Part 2's total probability, \ for means")]
        ex = label(r"the World: \ average the age-by-age means, weighted by how many adults are each age, \ and you recover the "
                   r"overall mean", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.8)
        if ex.width > 12.6:
            ex.width = 12.6
        with self.voiceover(
            "One property of conditional expectation is used more than any other. <bookmark mark='a'/> The average "
            "of the conditional means is the overall mean: the tower property, or the law of total expectation. "
            "<bookmark mark='b'/> For a discrete X it's Part 2's law of total probability, applied to means. "
            "<bookmark mark='c'/> Average the World's age-by-age mean incomes, weighting each age by how many adults "
            "have it, and you recover the overall mean exactly. We'll lean on this in every part that conditions."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=1.8, x=-0.4, buff=0.8, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.clear_scene()

    def projection(self):
        ns = NSpace(scale=0.8, center=[-3.2, -1.2, 0], angle=-0.6, tilt=0.38, axis_len=4.0,
                    axis_labels=[r"", r"", r""])
        ns.axes3.set_opacity(0)
        pl = ns.plane([1, 0, 0], [0, 1, 0], extent=2.6, color=COND, opacity=0.18)
        y = np.array([1.2, 0.9, 2.2])
        my = np.array([1.2, 0.9, 0.0])
        vy = ns.vector(y, color=WHITE)
        vm = ns.vector(my, color=COND, stroke_width=6)
        vr = ns.vector(y - my, color=S.RESID, origin=my)
        ra = ns.right_angle(my, -my, y - my, size=0.35)
        ly = ns.point_label(MathTex(r"Y", font_size=32), y, offset=(0.25, 0.25))
        lm = ns.point_label(MathTex(r"E[Y \mid X]", font_size=28, color=COND), my, offset=(0.6, -0.3))
        pll = label(r"all functions $g(X)$", font_size=24, color=COND).move_to([-3.8, -2.9, 0])
        txt = VGroup(label(r"$E[Y \mid X]$ is the orthogonal projection of $Y$", font_size=28, color=COND),
                     label(r"onto the subspace of functions of $X$, \ in $L^2$", font_size=28, color=COND),
                     label(r"the error is $\perp$ every $h(X)$: \ that was the cross term", font_size=24, color=GREY_A),
                     label(r"made rigorous with measure theory: \ Part 44", font_size=22, color=GREY_B))
        txt.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, 0.4, 0])
        with self.voiceover(
            "And here's the picture behind the proof. <bookmark mark='a'/> In the inner-product space of random "
            "variables, the functions of X form a subspace, drawn as a plane. <bookmark mark='b'/> Y is a vector off "
            "the plane. <bookmark mark='c'/> The best predictor of Y from X is the closest point of the plane: the "
            "orthogonal projection. That's the conditional expectation. <bookmark mark='d'/> The prediction error "
            "stands at right angles to the plane, which is exactly the vanishing cross term. Regression in Part 12 "
            "projects onto the smaller subspace of linear functions; conditional expectation projects onto all "
            "functions. Part 44 builds this properly, with measure theory."
        ) as vo:
            self.add(ns)
            vo.wait_until("a")
            self.add(pl)
            self.play(NSpace.reveal(pl), FadeIn(pll))
            vo.wait_until("b")
            self.add(vy)
            self.play(NSpace.reveal(vy), FadeIn(ly))
            vo.wait_until("c")
            self.add(vm)
            self.play(NSpace.reveal(vm), FadeIn(lm), FadeIn(txt[:2]))
            vo.wait_until("d")
            self.add(vr, ra)
            self.play(NSpace.reveal(vr, ra), FadeIn(txt[2:]))
            self.play(ns.turn(0.8, run_time=4.0))
        for m in (pl, vy, vm, vr, ra):
            m.clear_updaters()
        self.clear_scene()
