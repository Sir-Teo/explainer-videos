from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter1d

from explainer import *  # noqa: F403
from videos.stochastic.common import (Tank, boxed, density, hero, hist_shape, label, load, mtex, mult_table, note, num,
                                      path_curve, polyline, pour, square_on, tw_axes)

Y_RANGE = (-1.0, 1.6, 0.5)
Y_LEN = 5.2
UNIT = Y_LEN / (Y_RANGE[1] - Y_RANGE[0])  # screen units per unit of W: squares are drawn to this scale


def smooth_path(n_out=4096):
    """A smooth curve through the same territory as the hero path (the hero path, heavily blurred)."""
    w = gaussian_filter1d(hero(4096), 260, mode="nearest")
    return w - w[0]


class QuadraticVariation(VoiceoverScene):
    def construct(self):
        self.setup_stage()
        self.smooth()
        self.brownian()
        self.why()
        self.histograms()
        self.running()
        self.rule()

    # ------------------------------------------------------------------
    def setup_stage(self):
        ax = tw_axes(x_length=8.0, y_range=Y_RANGE, y_length=Y_LEN).to_edge(LEFT, buff=0.6).shift(DOWN * 0.35)
        tank = Tank(1.0, UNIT, width=UNIT, cap_label=r"T = 1")
        tank.move_to([4.6, 0, 0], aligned_edge=DOWN).shift(DOWN * (Y_LEN / 2 + 0.35) + UP * 0.0)
        tank.shift(UP * (ax.c2p(0, Y_RANGE[0])[1] - tank.floor.get_center()[1]))
        tlab = label(r"total area of the squares", font_size=26, color=GREY_A).next_to(tank, UP, buff=0.25)
        self.ax, self.tank, self.tlab = ax, tank, tlab
        self.readout_val = DecimalNumber(0, num_decimal_places=3, font_size=36, color=C.QV)
        self.readout = VGroup(MathTex(r"\sum (\Delta W)^2 =", font_size=34), self.readout_val).arrange(RIGHT, buff=0.15)
        self.readout.next_to(tank, DOWN, buff=0.25)

    def squares(self, w, ts, opacity=0.45):
        return VGroup(*[square_on(self.ax, ts[i], w[i], w[i + 1], UNIT, opacity=opacity) for i in range(len(w) - 1)])

    def empty_tank(self, strips):
        self.tank.level = 0.0
        return FadeOut(strips)

    # ------------------------------------------------------------------
    def smooth(self):
        ax, tank = self.ax, self.tank
        f = smooth_path()
        curve = path_curve(ax, f, color=C.DRIFT, stroke_width=3)
        title = label(r"Square every step's change, and add up the areas", font_size=34).to_edge(UP, buff=0.35)

        def sub(n):
            idx = np.linspace(0, 4096, n + 1).astype(int)
            return f[idx], np.linspace(0, 1, n + 1)

        self.readout[0].become(MathTex(r"\sum (\Delta f)^2 =", font_size=34).move_to(self.readout[0], RIGHT))
        with self.voiceover(
            "Here's that surprise. <bookmark mark='c'/> Take a smooth curve, and chop time into steps. "
            "<bookmark mark='s'/> On each step, build a square whose side is the curve's change over that step. "
            "<bookmark mark='t'/> Then pour all of the squares' area into this tank. Its capacity is exactly one unit of "
            "area: the same number as the length of our time interval, T equals one."
        ) as vo:
            self.play(FadeIn(title), Create(ax), FadeIn(ax.x_labels))
            vo.wait_until("c")
            self.play(Create(curve))
            w, ts = sub(16)
            sq = self.squares(w, ts)
            vo.wait_until("s")
            self.play(LaggedStart(*[GrowFromEdge(s_, LEFT) for s_ in sq], lag_ratio=0.08), run_time=2)
            vo.wait_until("t")
            self.play(FadeIn(tank), FadeIn(self.tlab))
        q16 = float(np.sum(np.diff(w) ** 2))
        with self.voiceover(
            "For a smooth curve, the squares fill only part of the tank. <bookmark mark='f'/> And finer steps make it "
            "emptier and emptier: <bookmark mark='g'/> each change is about the slope times delta t, so each square is "
            "about delta t squared, and the n of them add up to something on the order of delta t, which goes to zero."
        ) as vo:
            strips = pour(self, tank, list(sq), np.diff(w) ** 2, run_time=1.8, color=C.DRIFT)
            self.readout_val.set_value(q16)
            self.play(FadeIn(self.readout))
            vo.wait_until("f")
            w2, ts2 = sub(64)
            sq2 = self.squares(w2, ts2)
            self.play(self.empty_tank(strips), LaggedStart(*[GrowFromEdge(s_, LEFT) for s_ in sq2], lag_ratio=0.02),
                      run_time=1.2)
            strips = pour(self, tank, list(sq2), np.diff(w2) ** 2, run_time=1.5, lag=0.02, color=C.DRIFT)
            self.play(self.readout_val.animate.set_value(float(np.sum(np.diff(w2) ** 2))))
            w3, ts3 = sub(256)
            sq3 = self.squares(w3, ts3)
            self.play(self.empty_tank(strips), FadeIn(sq3), run_time=0.8)
            strips = pour(self, tank, list(sq3), np.diff(w3) ** 2, run_time=1.2, lag=0.003, color=C.DRIFT)
            self.play(self.readout_val.animate.set_value(float(np.sum(np.diff(w3) ** 2))))
            vo.wait_until("g")
            est = MathTex(r"\sum_i (\Delta f_i)^2", r"\approx", r"\sum_i f'(t_i)^2\,\Delta t^2", r"\le",
                          r"\big(\max |f'|\big)^2\, T\,\Delta t", r"\;\to 0", font_size=34)
            est.next_to(title, DOWN, buff=0.25)
            est[0].set_color(C.DRIFT)
            self.play(Write(est), run_time=2.5)
        self.wait(0.5)
        self.play(FadeOut(VGroup(curve, est)), self.empty_tank(strips), FadeOut(title))
        self.readout[0].become(MathTex(r"\sum (\Delta W)^2 =", font_size=34).move_to(self.readout[0], RIGHT))
        self.readout_val.set_value(0)

    # ------------------------------------------------------------------
    def brownian(self):
        ax, tank = self.ax, self.tank
        h = load("hero")
        qv = dict(zip(h["n"].tolist(), h["qv"].tolist()))
        path = path_curve(ax, hero(), stroke_width=2).set_stroke(opacity=0.85)
        title = label(r"The same for Brownian motion", font_size=34).to_edge(UP, buff=0.35)
        strips = VGroup()
        with self.voiceover(
            "Now the Brownian path. <bookmark mark='a'/> Sixteen steps: the squares more than fill the tank. "
        ) as vo:
            self.play(FadeIn(title), Create(path), run_time=1.5)
            vo.wait_until("a")
            w, ts = hero(16), np.linspace(0, 1, 17)
            sq = self.squares(w, ts)
            self.play(LaggedStart(*[GrowFromEdge(s_, LEFT) for s_ in sq], lag_ratio=0.06), run_time=1.5)
            strips = pour(self, tank, list(sq), np.diff(w) ** 2, run_time=2.0)
            self.play(self.readout_val.animate.set_value(qv[16]))
        for n, text in [(64, "Sixty-four steps: just over the brim."),
                        (256, "Two hundred and fifty-six: just under.")]:
            with self.voiceover(text) as vo:
                w, ts = hero(n), np.linspace(0, 1, n + 1)
                sq = self.squares(w, ts, opacity=0.5)
                self.play(self.empty_tank(strips), LaggedStart(*[GrowFromEdge(s_, LEFT) for s_ in sq], lag_ratio=0.01),
                          run_time=1.0)
                strips = pour(self, tank, list(sq), np.diff(w) ** 2, run_time=1.4, lag=0.004)
                self.play(self.readout_val.animate.set_value(qv[n]), run_time=0.6)
        fill = tank.fill_rect(qv[256])
        self.remove(*strips)
        self.add(fill)
        with self.voiceover(
            f"Four thousand: {qv[4096]:.3f}. <bookmark mark='m'/> Four million: {qv[4194304]:.4f}. "
            "<bookmark mark='e'/> The squares' total area converges to exactly one: the elapsed time."
        ) as vo:
            self.play(Transform(fill, tank.fill_rect(qv[4096])), self.readout_val.animate.set_value(qv[4096]))
            vo.wait_until("m")
            self.readout_val.num_decimal_places = 4
            self.play(Transform(fill, tank.fill_rect(qv[4194304])), self.readout_val.animate.set_value(qv[4194304]))
            vo.wait_until("e")
            self.play(Indicate(tank.brim, color=C.CLOCK), Indicate(tank.cap, color=C.CLOCK))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        lines = VGroup(
            MathTex(r"\Delta W_i \sim \mathcal N(0,\Delta t)", r"\quad\Rightarrow\quad",
                    r"\mathbb E\big[(\Delta W_i)^2\big] = \Delta t", font_size=38),
            MathTex(r"\mathbb E\Big[\sum_i (\Delta W_i)^2\Big]", r"=", r"n\,\Delta t", r"=", r"T", font_size=38),
            MathTex(r"\operatorname{Var}\big[(\Delta W_i)^2\big]", r"=", r"\mathbb E[\Delta W_i^4] - \Delta t^2", r"=",
                    r"3\Delta t^2 - \Delta t^2", r"=", r"2\,\Delta t^2", font_size=38),
            MathTex(r"\operatorname{Var}\Big[\sum_i (\Delta W_i)^2\Big]", r"=", r"n \cdot 2\,\Delta t^2", r"=",
                    r"2\,T\,\Delta t", r"\;\longrightarrow\; 0", font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(UP * 0.4)
        lines[1][4].set_color(C.CLOCK)
        lines[3][4:].set_color(C.QV)
        b_ind = Brace(lines[3][2], DOWN, buff=0.1, color=GREY_B)
        b_ind_l = label(r"independent: variances add", font_size=24, color=GREY_B).next_to(b_ind, DOWN, buff=0.08)
        b4 = Brace(lines[2][4], DOWN, buff=0.1, color=GREY_B)
        b4_l = label(r"Gaussian: $\mathbb E[Z^4] = 3$", font_size=24, color=GREY_B).next_to(b4, DOWN, buff=0.08)
        concl = label(r"so $\displaystyle\sum_i (\Delta W_i)^2 \to T$: \ not just on average, but on every path",
                      font_size=32, color=C.QV).to_edge(DOWN, buff=0.6)

        with self.voiceover(
            "Why? <bookmark mark='a'/> Each increment is a bell curve with variance delta t, so each square has an "
            "expected area of exactly delta t. <bookmark mark='b'/> Add up n of them, and the expected total is n delta "
            "t: the elapsed time, T."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(lines[0]))
            vo.wait_until("b")
            self.play(Write(lines[1]))
        with self.voiceover(
            "That's only the average. But the randomness disappears too. <bookmark mark='c'/> The variance of a single "
            "square works out to two delta t squared, <bookmark mark='g'/> using the fact that a standard bell curve has "
            "fourth moment three. <bookmark mark='d'/> The increments are independent, so the variances add, "
            "<bookmark mark='e'/> giving two T delta t. And that goes to zero as the steps shrink."
        ) as vo:
            vo.wait_until("c")
            self.play(Write(lines[2]))
            vo.wait_until("g")
            self.play(GrowFromCenter(b4), FadeIn(b4_l))
            vo.wait_until("d")
            self.play(FadeOut(VGroup(b4, b4_l)), Write(lines[3][:3]), GrowFromCenter(b_ind), FadeIn(b_ind_l))
            vo.wait_until("e")
            self.play(Write(lines[3][3:]))
        with self.voiceover(
            "A sum of many small, independent, positive pieces, whose fluctuations die away: it converges to a constant. "
            "Not just on average. On essentially every path."
        ):
            self.play(FadeIn(concl, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def histograms(self):
        q = load("qv")
        panels = VGroup()
        for n, ymax in [(16, 1.4), (256, 5.4), (4096, 21.0)]:
            ax = Axes(x_range=[0, 2.4, 0.5], y_range=[0, ymax, ymax], x_length=3.8, y_length=3.6, tips=False,
                      axis_config={"stroke_color": GREY_B, "include_ticks": False})
            edges = np.linspace(0, 2.4, 97)
            sh = hist_shape(ax, edges, density(q[f"q{n}"], edges), color=C.QV, fill_opacity=0.45)
            one = DashedLine(ax.c2p(1, 0), ax.c2p(1, ymax), color=C.CLOCK, stroke_width=2)
            ticks = VGroup(*[MathTex(f"{x:g}", font_size=22).next_to(ax.c2p(x, 0), DOWN, buff=0.1) for x in (0, 1, 2)])
            sd = q[f"q{n}"].std()
            t = MathTex(rf"n = {n:,}".replace(",", "{,}"), font_size=32).next_to(ax, UP, buff=0.15)
            s = MathTex(rf"\text{{sd}} = {sd:.3f}", font_size=28, color=C.QV).next_to(ticks, DOWN, buff=0.15)
            th = MathTex(rf"\sqrt{{2/n}} = {np.sqrt(2 / n):.3f}", font_size=24, color=GREY_B).next_to(s, DOWN, buff=0.1)
            panels.add(VGroup(ax, sh, one, ticks, t, s, th))
        panels.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.2)
        title = label(r"$\sum (\Delta W)^2$ on 4{,}000 fresh simulated paths", font_size=34).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here it is across four thousand fresh paths. <bookmark mark='a'/> With sixteen steps, the sum of squares is "
            "all over the place. <bookmark mark='b'/> With 256, it bunches up around one. <bookmark mark='c'/> With four "
            "thousand, it's nearly a spike. The spread shrinks exactly like root of two over n."
        ) as vo:
            self.play(FadeIn(title))
            for m, p in zip("abc", panels):
                vo.wait_until(m)
                self.play(Create(p[0]), FadeIn(p[2]), FadeIn(p[3]), FadeIn(p[4]), FadeIn(p[1], shift=UP * 0.2),
                          FadeIn(p[5]), FadeIn(p[6]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def running(self):
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1.4, 0.25], x_length=6.4, y_length=5.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        xl = MathTex("t", font_size=30, color=C.CLOCK).next_to(ax.x_axis.get_end(), RIGHT, buff=0.12)
        yl = MathTex(r"\sum_{t_i < t} (\Delta W_i)^2", font_size=30, color=C.QV).next_to(ax.y_axis.get_end(), UP, buff=0.12)
        nums = VGroup(*[MathTex(f"{v:g}", font_size=22).next_to(ax.c2p(v, 0), DOWN, buff=0.1) for v in (0, 0.5, 1)],
                      *[MathTex(f"{v:g}", font_size=22).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0.5, 1)])
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=C.CLOCK, stroke_width=3)
        diag_l = MathTex(r"y = t", font_size=30, color=C.CLOCK).next_to(ax.c2p(1, 1), RIGHT, buff=0.15)

        def stairs(n):
            w = hero(n)
            q = np.concatenate([[0], np.cumsum(np.diff(w) ** 2)])
            ts = np.linspace(0, 1, n + 1)
            if n > 512:
                return polyline(ax, ts, q, color=C.QV, stroke_width=2.5)
            xs, ys = [0.0], [0.0]
            for i in range(n):
                xs += [ts[i + 1], ts[i + 1]]
                ys += [q[i], q[i + 1]]
            return polyline(ax, xs, ys, color=C.QV, stroke_width=2.5)

        cur = stairs(16)
        nl = MathTex("n = 16", font_size=34).move_to(ax.c2p(0.2, 1.3))
        path_ax = tw_axes(x_length=4.4, y_range=Y_RANGE, y_length=2.4, numbers=False).move_to([4.2, 0.6, 0])
        path = path_curve(path_ax, hero(), stroke_width=1.6)
        path_l = label(r"the path: random", font_size=26, color=C.BROWNIAN).next_to(path_ax, DOWN, buff=0.15)
        clock_l = label(r"its squared wiggle: a clock", font_size=26, color=C.QV).next_to(path_l, DOWN, buff=0.25)
        with self.voiceover(
            "The same is true at every moment along the way. <bookmark mark='s'/> Add up the squares only up to time t, "
            "and plot that running total. With sixteen steps it's a ragged staircase. <bookmark mark='r'/> Refine the "
            "steps: sixty-four, two fifty-six, four thousand. <bookmark mark='d'/> The staircase lies down on the line y "
            "equals t. <bookmark mark='c'/> The path is random, but its accumulated squared wiggle is a perfect clock: "
            "quadratic variation equals time."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(nums), Create(path_ax), Create(path), FadeIn(path_l))
            vo.wait_until("s")
            self.play(Create(cur), FadeIn(nl), run_time=1.5)
            vo.wait_until("r")
            per = max(0.6, (vo.until("d") - 0.2) / 3)
            for n in (64, 256, 4096):
                self.play(Transform(cur, stairs(n)), Transform(nl, MathTex(rf"n = {n:,}".replace(",", "{,}"),
                                                                             font_size=34).move_to(nl)), run_time=per)
            vo.wait_until("d")
            self.play(Create(diag), FadeIn(diag_l))
            vo.wait_until("c")
            self.play(FadeIn(clock_l))
        qv_def = MathTex(r"[W]_t", r"=", r"t", font_size=48).to_edge(UP, buff=0.4).shift(RIGHT * 3.2)
        qv_def[0].set_color(C.QV)
        qv_def[2].set_color(C.CLOCK)
        self.play(Write(qv_def))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rule(self):
        g = np.random.default_rng(5)
        z2 = g.standard_normal(32) ** 2
        ax = Axes(x_range=[0, 32, 8], y_range=[0, 5, 1], x_length=6.0, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).to_corner(UL, buff=0.7).shift(DOWN * 0.6)
        bars = VGroup(*[Rectangle(width=6.0 / 32 * 0.8, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01),
                                  stroke_width=0, fill_color=C.QV, fill_opacity=0.7).move_to(ax.c2p(i + 0.5, 0), aligned_edge=DOWN)
                        for i, v in enumerate(z2)])
        mean = DashedLine(ax.c2p(0, 1), ax.c2p(32, 1), color=C.CLOCK, stroke_width=2.5)
        mean_l = MathTex(r"\text{mean } 1", font_size=26, color=C.CLOCK).next_to(mean, RIGHT, buff=0.1)
        bl = MathTex(r"(\Delta W_i)^2 / \Delta t", font_size=30, color=C.QV).next_to(ax, UP, buff=0.15)
        rule = MathTex(r"(dW)^2", r"=", r"dt", font_size=72)
        rule[0].set_color(C.QV)
        rule[2].set_color(C.CLOCK)
        rb = boxed(rule, color=C.QV, buff=0.3)
        rb.to_corner(UR, buff=0.8).shift(DOWN * 0.3)
        meaning = label(r"in any sum over many small steps,\\ the squares add up exactly like $dt$", font_size=28,
                        color=GREY_A).next_to(rb, DOWN, buff=0.3)
        table = mult_table(44).to_edge(DOWN, buff=0.6).shift(LEFT * 3.2)
        why = VGroup(
            MathTex(r"\sum (\Delta t)^2 = T\,\Delta t \to 0", font_size=32),
            MathTex(r"\sum |\Delta t\,\Delta W| \approx T\sqrt{2\Delta t/\pi} \to 0", font_size=32),
            MathTex(r"\sum (\Delta W)^2 \to T", font_size=32, color=C.QV),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(table, RIGHT, buff=1.0)

        with self.voiceover(
            "This is the one rule that makes stochastic calculus different, and we write it in a single line: "
            "<bookmark mark='r'/> d W squared equals d t. <bookmark mark='m'/> It doesn't mean each little square equals "
            "delta t. <bookmark mark='b'/> Each one is delta t times a random number with mean one, which can be almost "
            "zero or bigger than four. <bookmark mark='s'/> It means that in any sum over many small steps, the squares "
            "add up exactly like delta t would."
        ) as vo:
            self.play(Write(rule), run_time=1.5)
            vo.wait_until("r")
            self.play(Create(rb[0]), Indicate(rule, color=C.QV, scale_factor=1.1))
            vo.wait_until("m")
            self.play(Create(ax), FadeIn(bl))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), run_time=1.6)
            self.play(Create(mean), FadeIn(mean_l))
            vo.wait_until("s")
            self.play(FadeIn(meaning))
        with self.voiceover(
            "And the other products of small quantities vanish. <bookmark mark='a'/> d t times d t sums to T delta t, "
            "which goes to zero. <bookmark mark='b'/> d t times d W sums to something like T root delta t, which also goes "
            "to zero. <bookmark mark='c'/> Only d W times d W survives. <bookmark mark='t'/> That's the multiplication "
            "table of stochastic calculus. In ordinary calculus, every product of two small changes is negligible. Here, "
            "d W is the size of root d t, so its square is as big as d t itself, and it stays."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(why[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(why[1], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(why[2], shift=RIGHT * 0.2))
            vo.wait_until("t")
            self.play(FadeIn(table[1:]), LaggedStart(*[FadeIn(c) for c in table.cells], lag_ratio=0.08), run_time=1.5)
            self.play(Indicate(table.cells[8], color=C.QV, scale_factor=1.4))
        self.wait(0.6)
        self.clear_scene()
