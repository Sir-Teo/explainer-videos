from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.stochastic.common import Tank, boxed, hero, label, load, mtex, note, num, pour

K = 2.15  # screen units per unit of W, the same on both axes of the (w, y) plane
W_RANGE = (-1.0, 1.6)


class MissingHalf(VoiceoverScene):
    def construct(self):
        self.three_sums()
        self.algebra()
        self.triangles()
        self.stratonovich()

    # ------------------------------------------------------------------
    def three_sums(self):
        h = load("hero")
        L, R, M, Q = (float(h[k][-1]) for k in ("left", "right", "mid", "qv"))
        WT = float(hero()[-1])
        title = label(r"Where you sample the integrand now matters", font_size=36).to_edge(UP, buff=0.45)
        rows = VGroup(
            MathTex(r"\text{left:}", r"\sum W_{t_i}\,\Delta W_i", r"=", num(L, 4), font_size=40),
            MathTex(r"\text{right:}", r"\sum W_{t_{i+1}}\,\Delta W_i", r"=", num(R, 4), font_size=40),
            MathTex(r"\text{midpoint:}", r"\sum \tfrac12\big(W_{t_i} + W_{t_{i+1}}\big)\,\Delta W_i", r"=", num(M, 4),
                    font_size=40),
        )
        for r, c in zip(rows, (C.LEFT_PT, C.RIGHT_PT, C.MID_PT)):
            r[0].set_color(c)
            r[1].set_color(c)
            r[3].set_color(c)
        for r in rows:
            r.shift(-r[2].get_center()[0] * RIGHT)
        rows.arrange(DOWN, buff=0.4).move_to(UP * 0.6)
        for r in rows:
            r.shift((2.0 - r[2].get_center()[0]) * RIGHT)
        diff = MathTex(r"\text{right} - \text{left}", r"=", r"\sum (\Delta W_i)^2", r"=", num(Q, 4), r"\;\approx T",
                       font_size=40).next_to(rows, DOWN, buff=0.7)
        diff[2:].set_color(C.QV)
        half = MathTex(r"\tfrac12 W_1^2 = " + num(0.5 * WT**2, 4), font_size=36, color=GREY_A).next_to(diff, DOWN, buff=0.35)
        steps = note(r"our path, $4{,}194{,}304$ steps").to_corner(DR, buff=0.3)
        with self.voiceover(
            "So where does the missing half come from? <bookmark mark='a'/> In ordinary calculus, it doesn't matter "
            "where inside each little step you evaluate the integrand: the left end, the right end, the middle. All the "
            "choices give the same limit. Not here. <bookmark mark='l'/> On our path, sampling W at the left end of each "
            "step gives 0.2847. <bookmark mark='r'/> Sampling at the right end gives 1.2847. <bookmark mark='m'/> The "
            "midpoint gives 0.7847."
        ) as vo:
            self.play(FadeIn(title), FadeIn(steps))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r[:3], shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3), run_time=2)
            vo.wait_until("l")
            self.play(FadeIn(rows[0][3]))
            vo.wait_until("r")
            self.play(FadeIn(rows[1][3]))
            vo.wait_until("m")
            self.play(FadeIn(rows[2][3]))
        with self.voiceover(
            "The right sum minus the left sum is the sum of W at the right end minus W at the left end, times delta W: "
            "<bookmark mark='q'/> that's the sum of the squares, delta W squared. And we know where that goes: to T, which "
            "here is one. <bookmark mark='h'/> And notice the midpoint gives exactly half of W squared: the answer from "
            "ordinary calculus."
        ) as vo:
            vo.wait_until("q")
            self.play(Write(diff))
            vo.wait_until("h")
            self.play(FadeIn(half), Indicate(rows[2][3], color=C.MID_PT))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algebra(self):
        l1 = MathTex(r"W_{t_{i+1}}^2 - W_{t_i}^2", r"=", r"\big(W_{t_i} + \Delta W_i\big)^2 - W_{t_i}^2", font_size=42)
        l2 = MathTex(r"W_{t_{i+1}}^2 - W_{t_i}^2", r"=", r"2\,W_{t_i}\,\Delta W_i", r"+", r"(\Delta W_i)^2", font_size=42)
        l2[2].set_color(C.LEFT_PT)
        l2[4].set_color(C.QV)
        l3 = MathTex(r"W_T^2 - W_0^2", r"=", r"2\sum_i W_{t_i}\,\Delta W_i", r"+", r"\sum_i (\Delta W_i)^2", font_size=42)
        l3[2].set_color(C.LEFT_PT)
        l3[4].set_color(C.QV)
        l4 = MathTex(r"W_T^2", r"=", r"2\int_0^T W\,dW", r"+", r"T", font_size=42)
        l4[2].set_color(C.GAINS)
        l4[4].set_color(C.QV)
        l5 = MathTex(r"\int_0^T W\,dW", r"=", r"\tfrac12 W_T^2", r"-", r"\tfrac12 T", font_size=50)
        l5[0].set_color(C.GAINS)
        l5[4].set_color(C.QV)
        col = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.5).move_to(UP * 0.9)
        for m in (l2, l3, l4):
            m.shift((l1[1].get_center()[0] - m[1].get_center()[0]) * RIGHT)
        tel = Brace(l3[0], DOWN, buff=0.1, color=GREY_B)
        tel_l = label(r"telescopes", font_size=24, color=GREY_B).next_to(tel, DOWN, buff=0.05)
        b_q = Brace(l3[4], DOWN, buff=0.1, color=C.QV)
        b_q_l = MathTex(r"\to T", font_size=32, color=C.QV).next_to(b_q, DOWN, buff=0.05)
        res = boxed(l5, color=C.QV, buff=0.25).to_edge(DOWN, buff=0.5)

        with self.voiceover(
            "Here's the exact algebra, on one step. <bookmark mark='a'/> The change in W squared, from the left end to "
            "the right end, is W plus delta W, squared, minus W squared, <bookmark mark='b'/> which is two W delta W, "
            "plus delta W squared."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(l1))
            vo.wait_until("b")
            self.play(TransformMatchingTex(l1.copy(), l2))
        with self.voiceover(
            "Now add this up over all the steps. <bookmark mark='t'/> On the left, the sum telescopes: everything cancels "
            "except W squared at the end, minus W squared at the start, which is zero. <bookmark mark='r'/> On the right: "
            "twice the left-endpoint sum, plus the sum of the squares, <bookmark mark='q'/> which converges to T."
        ) as vo:
            self.play(Write(l3))
            vo.wait_until("t")
            self.play(GrowFromCenter(tel), FadeIn(tel_l))
            vo.wait_until("q")
            self.play(GrowFromCenter(b_q), FadeIn(b_q_l))
        with self.voiceover(
            "In the limit, W squared at time T equals twice the integral of W d W, plus T. <bookmark mark='s'/> So the "
            "integral is one half W squared, minus one half T. That's the missing half, and it is the quadratic "
            "variation, in disguise."
        ) as vo:
            self.play(FadeOut(VGroup(tel, tel_l, b_q, b_q_l)))
            self.play(Write(l4))
            vo.wait_until("s")
            self.play(Write(res[1]), Create(res[0]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def triangles(self):
        plane = Axes(x_range=[W_RANGE[0], W_RANGE[1], 0.5], y_range=[W_RANGE[0], W_RANGE[1], 0.5],
                     x_length=K * 2.6, y_length=K * 2.6, tips=False,
                     axis_config={"stroke_color": GREY_B, "include_ticks": False})
        plane.to_edge(LEFT, buff=0.6).shift(DOWN * 0.35)
        xl = MathTex("w", font_size=30, color=C.BROWNIAN).next_to(plane.x_axis.get_end(), RIGHT, buff=0.1)
        yl = MathTex("y", font_size=30).next_to(plane.y_axis.get_end(), UP, buff=0.1)
        diag = plane.plot(lambda x: x, x_range=list(W_RANGE), color=GREY_A, stroke_width=2.5)
        diag_l = MathTex(r"y = w", font_size=30, color=GREY_A).next_to(plane.c2p(1.45, 1.45), RIGHT, buff=0.1)

        tank = Tank(0.5, K, width=K * 0.9, cap_label=r"\tfrac12 T")
        tank.shift(RIGHT * (4.4 - tank.floor.get_center()[0]) + UP * (plane.c2p(0, W_RANGE[0])[1] - tank.floor.get_center()[1]))
        tl = label(r"area of the triangles", font_size=26, color=C.QV).next_to(tank, UP, buff=0.2)
        val = DecimalNumber(0, num_decimal_places=3, font_size=34, color=C.QV)
        tri_sum = VGroup(MathTex(r"\sum \tfrac12(\Delta W)^2 =", font_size=32, color=C.QV), val).arrange(RIGHT, buff=0.12)
        tri_sum.next_to(tank, DOWN, buff=0.3)
        tri_sum.shift(RIGHT * min(0, 7.0 - tri_sum.get_right()[0]))

        def rect(a, b):
            return Polygon(plane.c2p(a, 0), plane.c2p(b, 0), plane.c2p(b, a), plane.c2p(a, a), stroke_color=C.LEFT_PT,
                           stroke_width=2, fill_color=C.LEFT_PT, fill_opacity=0.3)

        def tri(a, b):
            return Polygon(plane.c2p(a, a), plane.c2p(b, a), plane.c2p(b, b), stroke_color=C.QV, stroke_width=2,
                           fill_color=C.QV, fill_opacity=0.75)

        def trap(a, b):
            return Polygon(plane.c2p(a, 0), plane.c2p(b, 0), plane.c2p(b, b), plane.c2p(a, a), stroke_width=0,
                           fill_color=C.MID_PT, fill_opacity=0.25)

        w16 = hero(16)
        a0, b0 = 0.3, 0.95  # one step, enlarged for the explanation
        a1, b1 = 0.95, 0.4
        dot = Dot(plane.c2p(0, 0), radius=0.08, color=C.BROWNIAN)
        intro = VGroup(
            MathTex(r"W_{t_i}\,\Delta W_i", r"=", r"\text{area of the rectangle}", font_size=32),
            MathTex(r"\text{area under } y = w", r"=", r"\tfrac12 W_{t_{i+1}}^2 - \tfrac12 W_{t_i}^2", font_size=32),
            MathTex(r"\text{difference}", r"=", r"\text{a triangle of area } \tfrac12 (\Delta W_i)^2", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_corner(UR, buff=0.4)
        intro[0][0].set_color(C.LEFT_PT)
        intro[1][0].set_color(C.MID_PT)
        intro[2][2].set_color(C.QV)

        with self.voiceover(
            "There's a lovely picture behind this. <bookmark mark='p'/> Draw a plane where both axes measure the value of "
            "W, and draw the line y equals w. <bookmark mark='d'/> As time runs, W moves back and forth along the "
            "horizontal axis."
        ) as vo:
            vo.wait_until("p")
            self.play(Create(plane), FadeIn(xl), FadeIn(yl), Create(diag), FadeIn(diag_l))
            vo.wait_until("d")
            self.play(FadeIn(dot))
            path_pts = hero(256)
            for i in range(0, 64, 4):
                self.play(dot.animate.move_to(plane.c2p(path_pts[i + 4], 0)), run_time=0.12, rate_func=linear)
            self.play(dot.animate.move_to(plane.c2p(0, 0)), run_time=0.3)

        # One step, explained
        r1, t1, z1 = rect(a0, b0), tri(a0, b0), trap(a0, b0)
        big = note(r"one step, enlarged").next_to(plane.c2p(1.0, -0.6), RIGHT, buff=0.1)
        with self.voiceover(
            "Take one step, from W at the left end to W at the right end. <bookmark mark='r'/> The left-endpoint gain, W "
            "times delta W, is the area of this rectangle: width delta W, height W. <bookmark mark='u'/> The area under the "
            "line over the same stretch is one half the new W squared, minus one half the old one. "
            "<bookmark mark='t'/> They differ by a triangle, with two legs of length delta W, and area one half delta W "
            "squared."
        ) as vo:
            self.play(dot.animate.move_to(plane.c2p(a0, 0)), FadeIn(big))
            self.play(dot.animate.move_to(plane.c2p(b0, 0)))
            vo.wait_until("r")
            self.play(FadeIn(r1), FadeIn(intro[0]))
            vo.wait_until("u")
            self.play(FadeIn(z1), FadeIn(intro[1]))
            vo.wait_until("t")
            self.play(FadeIn(t1), FadeIn(intro[2]))
        r2, t2 = rect(a1, b1), tri(a1, b1)
        with self.voiceover(
            "And when the step goes the other way, <bookmark mark='b'/> the rectangle counts as negative area, overshoots "
            "the region under the line, and again they differ by exactly the same kind of triangle. Up or down, the "
            "left-endpoint sum always loses one half delta W squared."
        ) as vo:
            self.play(FadeOut(VGroup(r1, z1)), t1.animate.set_fill(opacity=0.35))
            self.play(dot.animate.move_to(plane.c2p(b1, 0)))
            vo.wait_until("b")
            self.play(FadeIn(r2), FadeIn(t2))
        self.wait(0.3)
        self.play(FadeOut(VGroup(r2, t1, t2, intro, big)))
        self.play(dot.animate.move_to(plane.c2p(0, 0)))

        # All sixteen steps: rectangles flash, triangles pour into the tank
        with self.voiceover(
            "Now run all sixteen steps, and collect the triangles in a tank whose brim is at one half T. "
            "<bookmark mark='g'/> The areas under the line telescope to one half W squared at the end, no matter how the "
            "path wandered. But every step drops a triangle, and they pile up."
        ) as vo:
            self.play(FadeIn(tank), FadeIn(tl), FadeIn(tri_sum))
            vo.wait_until("g")
            per = max(0.42, (vo.remaining() - 0.3) / 16)
            strips = VGroup()
            for i in range(16):
                a, b = w16[i], w16[i + 1]
                r, t = rect(a, b), tri(a, b)
                self.play(dot.animate.move_to(plane.c2p(b, 0)), FadeIn(r), FadeIn(t), run_time=per * 0.45)
                strips.add(*pour(self, tank, [t], [0.5 * (b - a) ** 2], run_time=per * 0.55, lag=0))
                self.remove(r)
                val.set_value(tank.level)
        h = load("hero")
        qv = dict(zip(h["n"].tolist(), h["qv"].tolist()))
        with self.voiceover(
            f"With sixteen steps, the triangles hold {0.5 * qv[16]:.2f}, more than the brim. <bookmark mark='a'/> With 256 "
            f"steps, {0.5 * qv[256]:.3f}. <bookmark mark='b'/> With four million: {0.5 * qv[4194304]:.4f}. "
            "<bookmark mark='c'/> For a smooth path, these triangles are second-order small and add up to nothing. For a "
            "Brownian path there are so many of them that they add up to exactly half the elapsed time."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(strips))
            tank.level = 0.0
            w = hero(256)
            tris = VGroup(*[tri(w[i], w[i + 1]) for i in range(256)])
            self.play(FadeIn(tris), dot.animate.move_to(plane.c2p(w[-1], 0)), run_time=0.8)
            st = pour(self, tank, list(tris), 0.5 * np.diff(w) ** 2, run_time=1.5, lag=0.003)
            val.set_value(tank.level)
            vo.wait_until("b")
            fill = tank.fill_rect(0.5 * qv[4194304])
            val.num_decimal_places = 4
            self.play(FadeOut(st), FadeIn(fill), val.animate.set_value(0.5 * qv[4194304]))
            vo.wait_until("c")
            self.play(Indicate(tank.cap, color=C.CLOCK))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stratonovich(self):
        rows = VGroup(
            MathTex(r"\text{It\^o (left):}", r"\int_0^T W\,dW", r"=", r"\tfrac12 W_T^2 - \tfrac12 T", font_size=38),
            MathTex(r"\text{Stratonovich (midpoint):}", r"\int_0^T W\circ dW", r"=", r"\tfrac12 W_T^2", font_size=38),
            MathTex(r"\text{right endpoint:}", r"\phantom{\int_0^T W\,dW}", r"=", r"\tfrac12 W_T^2 + \tfrac12 T", font_size=38),
        )
        for r, c in zip(rows, (C.LEFT_PT, C.MID_PT, C.RIGHT_PT)):
            r[0].set_color(c)
        for r in rows:
            r.shift(-r[2].get_center()[0] * RIGHT)
        rows.arrange(DOWN, buff=0.4).to_edge(UP, buff=0.5)
        for r in rows:
            r.shift((1.0 - r[2].get_center()[0]) * RIGHT)
        means = VGroup(
            MathTex(r"\mathbb E[\,\cdot\,] = \tfrac12 T - \tfrac12 T = 0", font_size=32, color=C.LEFT_PT),
            MathTex(r"\mathbb E[\,\cdot\,] = \tfrac12 T", font_size=32, color=C.MID_PT),
            MathTex(r"\mathbb E[\,\cdot\,] = T", font_size=32, color=C.RIGHT_PT),
        )
        for m, r in zip(means, rows):
            m.next_to(r, RIGHT, buff=0.6)
        means.shift(RIGHT * min(0, 6.9 - means.get_right()[0]))
        peek = label(r"the midpoint and the right end use $W_{t_{i+1}}$: \ the price \emph{after} the bet", font_size=30,
                     color=GREY_A).next_to(rows, DOWN, buff=0.55)
        fair = label(r"It\^o integrals are fair games: \ $\mathbb E\!\left[\int H\,dW\right] = 0$", font_size=34,
                     color=C.GAINS).next_to(peek, DOWN, buff=0.4)
        wz = note(r"Wong--Zakai (1965): smooth approximations of noise converge to Stratonovich."
                  r" \ Convert with \ $\int H\circ dW = \int H\,dW + \tfrac12 [H, W]_T$", font_size=24)
        wz.to_edge(DOWN, buff=0.4)

        with self.voiceover(
            "So which choice is right? <bookmark mark='a'/> Itô's left-endpoint integral gives one half W squared minus one "
            "half T. <bookmark mark='b'/> The midpoint gives the ordinary-calculus answer, one half W squared. It's called "
            "the Stratonovich integral. <bookmark mark='c'/> The right endpoint overshoots by one half T."
        ) as vo:
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        with self.voiceover(
            "Think about the gambler again. <bookmark mark='p'/> The midpoint and right-end rules set your stake using the "
            "price after the move: they peek at the future. <bookmark mark='e'/> And it shows in the averages. Since W "
            "squared has mean T, Itô's answer has mean zero, <bookmark mark='f'/> while the others win money on average, "
            "in a perfectly fair game. Only cheating does that. <bookmark mark='g'/> The left endpoint is the honest "
            "choice: Itô integrals are fair games, with mean zero."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(peek))
            vo.wait_until("e")
            self.play(FadeIn(means[0]))
            vo.wait_until("f")
            self.play(FadeIn(means[1]), FadeIn(means[2]))
            vo.wait_until("g")
            self.play(FadeIn(fair, shift=UP * 0.2))
        with self.voiceover(
            "Stratonovich's integral isn't wrong, though. It's a different integral, and in physics it's often the "
            "natural one: if the noise is a limit of smooth, rapidly varying forces, the Stratonovich integral is what "
            "you get. The two are related by a simple correction term. In this video, we'll use Itô's, which is the "
            "standard in probability and finance."
        ):
            self.play(FadeIn(wz))
        self.wait(0.4)
        self.clear_scene()
