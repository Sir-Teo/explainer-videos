from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.stochastic.common import (density, gauss_pdf, hist_shape, label, load, mtex, note, part_card, path_curve,
                                      pdf_curve, polyline, tw_axes)

WALK_NS = [16, 64, 256, 1024, 4096]


class RandomWalk(VoiceoverScene):
    def construct(self):
        self.card()
        self.coin_walk()
        self.scaling()
        self.triptych()
        self.bell()
        self.limit()
        self.definition()

    def card(self):
        c = part_card(1, r"Brownian motion", r"the raw material of stochastic calculus")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def coin_walk(self):
        S = load("walk")["S16"]
        flips = np.diff(S)
        ax = Axes(x_range=[0, 16, 1], y_range=[-5, 5, 1], x_length=9, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": True, "tick_size": 0.05}).move_to(DOWN * 0.9)
        grid = VGroup(*[Line(ax.c2p(0, y), ax.c2p(16, y), color=GREY_D, stroke_width=1).set_stroke(opacity=0.5)
                        for y in range(-5, 6) if y])
        xl = label(r"step", font_size=26, color=C.CLOCK).next_to(ax.x_axis.get_end(), RIGHT, buff=0.15)
        coins = VGroup()
        for i, f in enumerate(flips):
            c = Circle(radius=0.22, stroke_color=GREY_A, stroke_width=2, fill_color="#1E2733", fill_opacity=1)
            t = Tex("H" if f > 0 else "T", font_size=26, color=WHITE if f > 0 else GREY_B).move_to(c)
            coins.add(VGroup(c, t))
        coins.arrange(RIGHT, buff=0.12).to_edge(UP, buff=0.6)
        legend = label(r"heads: step up \qquad tails: step down", font_size=28, color=GREY_A).next_to(coins, DOWN, buff=0.25)
        dot = Dot(ax.c2p(0, 0), radius=0.08, color=WHITE)
        segs = VGroup()

        with self.voiceover(
            "Brownian motion is the limit of the simplest random process there is. <bookmark mark='f'/> Flip a fair coin. "
            "Heads, take a step up; tails, a step down. <bookmark mark='w'/> Do it again, and again, and you trace out a "
            "random walk."
        ) as vo:
            self.play(Create(ax), FadeIn(grid), FadeIn(xl))
            vo.wait_until("f")
            self.play(FadeIn(legend), FadeIn(dot))
            vo.wait_until("w")
            per = max(0.18, (vo.remaining() - 0.3) / 16)
            for i in range(16):
                seg = Line(ax.c2p(i, S[i]), ax.c2p(i + 1, S[i + 1]), color=C.BROWNIAN, stroke_width=4)
                segs.add(seg)
                self.play(FadeIn(coins[i], scale=1.3), Create(seg), dot.animate.move_to(ax.c2p(i + 1, S[i + 1])),
                          run_time=per)
        self.play(FadeOut(VGroup(coins, legend)))
        self.walk = VGroup(ax, grid, xl, segs, dot)

    # ------------------------------------------------------------------
    def scaling(self):
        # The question: squeeze n steps into one unit of time. How tall is each step?
        ax = self.walk[0]
        S = load("walk")["S16"]
        i = int(np.flatnonzero(np.diff(S) > 0)[2])  # an up-step to annotate
        y0, y1 = int(S[i]), int(S[i + 1])
        dt_b = BraceBetweenPoints(ax.c2p(i, y0), ax.c2p(i + 1, y0), DOWN, buff=0.08, color=C.CLOCK)
        dt_l = MathTex(r"\Delta t = \tfrac1n", font_size=32, color=C.CLOCK).next_to(dt_b, DOWN, buff=0.08)
        dx_b = BraceBetweenPoints(ax.c2p(i + 1, y0), ax.c2p(i + 1, y1), RIGHT, buff=0.08, color=C.BROWNIAN)
        dx_l = MathTex(r"\Delta x = \;?", font_size=32, color=C.BROWNIAN).next_to(dx_b, RIGHT, buff=0.08)

        eqs = VGroup(
            MathTex(r"X_t", r"=", r"\Delta x", r"\,(\xi_1 + \xi_2 + \cdots + \xi_{t/\Delta t})", r",\qquad \xi_i = \pm 1",
                    font_size=38),
            MathTex(r"\operatorname{Var}(X_t)", r"=", r"\frac{t}{\Delta t}", r"\cdot", r"(\Delta x)^2", font_size=38),
            MathTex(r"=", r"t", r"\cdot", r"\frac{(\Delta x)^2}{\Delta t}", font_size=38),
        )
        eqs[0][2].set_color(C.BROWNIAN)
        eqs[1][2].set_color(C.CLOCK)
        eqs[1][4].set_color(C.BROWNIAN)
        eqs[2][1].set_color(C.CLOCK)
        eqs[2][3].set_color(C.QV)
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(UP, buff=0.4).shift(RIGHT * 0.3)
        eqs[2].next_to(eqs[1][1], DOWN, buff=0.45, aligned_edge=LEFT)
        b1 = Brace(eqs[1][2], DOWN, buff=0.08, color=C.CLOCK)
        b1l = label(r"number of steps", font_size=22, color=C.CLOCK).next_to(b1, DOWN, buff=0.05)
        b2 = Brace(eqs[1][4], DOWN, buff=0.08, color=C.BROWNIAN)
        b2l = label(r"variance of each", font_size=22, color=C.BROWNIAN).next_to(b2, DOWN, buff=0.05)

        with self.voiceover(
            "To get something in continuous time, we'll squeeze n steps into one unit of time. "
            "<bookmark mark='t'/> Each step takes a time delta t, equal to one over n. <bookmark mark='x'/> But how tall "
            "should each step be? Call the step size delta x."
        ) as vo:
            vo.wait_until("t")
            self.play(GrowFromCenter(dt_b), FadeIn(dt_l))
            vo.wait_until("x")
            self.play(GrowFromCenter(dx_b), FadeIn(dx_l))
        with self.voiceover(
            "There's only one choice that works, and here's why. <bookmark mark='a'/> At time t, the walker's position is "
            "delta x times a sum of plus and minus ones, one for each step taken. <bookmark mark='v'/> The coin flips "
            "are independent, so their variances add: <bookmark mark='n'/> the number of steps, t over delta t, "
            "<bookmark mark='e'/> times the variance of each step, delta x squared. <bookmark mark='r'/> That's t, times "
            "delta x squared over delta t."
        ) as vo:
            self.play(self.walk.animate.scale(0.55).to_corner(DR, buff=0.4),
                      FadeOut(VGroup(dt_b, dt_l, dx_b, dx_l)))
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("v")
            self.play(Write(eqs[1][:2]))
            vo.wait_until("n")
            self.play(Write(eqs[1][2]), GrowFromCenter(b1), FadeIn(b1l))
            vo.wait_until("e")
            self.play(Write(eqs[1][3:]), GrowFromCenter(b2), FadeIn(b2l))
            vo.wait_until("r")
            self.play(FadeOut(VGroup(b1, b1l, b2, b2l)), Write(eqs[2]))

        cases = VGroup(
            MathTex(r"\Delta x = \Delta t", r"\;\Rightarrow\;", r"\operatorname{Var} = t\,\Delta t \to 0", font_size=34),
            MathTex(r"\Delta x = \sqrt{\Delta t}", r"\;\Rightarrow\;", r"\operatorname{Var} = t", font_size=34),
            MathTex(r"\Delta x = \Delta t^{1/4}", r"\;\Rightarrow\;", r"\operatorname{Var} = t/\sqrt{\Delta t} \to \infty",
                    font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(eqs[2], DOWN, buff=0.5).align_to(eqs[0], LEFT)
        cases[1].set_color(C.QV)
        with self.voiceover(
            "So everything depends on that ratio. <bookmark mark='a'/> Make the steps as small as the time steps, and the "
            "variance dies away: the walk freezes. <bookmark mark='c'/> Make them bigger, like the fourth root, and the "
            "variance blows up. <bookmark mark='b'/> Only steps of size square root of delta t keep it finite: "
            "space has to scale like the square root of time. That square root is the seed of everything in this video."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cases[0], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cases[2], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cases[1], shift=RIGHT * 0.2))
            self.play(Circumscribe(cases[1], color=C.QV))
        self.clear_scene()

    # ------------------------------------------------------------------
    def triptych(self):
        w = load("walk")
        scal = [(r"\Delta x = \Delta t", lambda n: 1 / n, GREY_B),
                (r"\Delta x = \sqrt{\Delta t}", lambda n: n**-0.5, C.BROWNIAN),
                (r"\Delta x = \Delta t^{1/4}", lambda n: n**-0.25, C.RIGHT_PT)]
        Y = 3.0
        panels = VGroup()
        for j, (tex, _, col) in enumerate(scal):
            ax = Axes(x_range=[0, 1, 0.5], y_range=[-Y, Y, 1], x_length=3.9, y_length=4.4, tips=False,
                      axis_config={"stroke_color": GREY_C, "include_ticks": False})
            frame = Rectangle(width=3.9, height=4.4, stroke_color=GREY_D, stroke_width=1.5).move_to(ax)
            t = MathTex(tex, font_size=34, color=col if j else GREY_A).next_to(frame, UP, buff=0.2)
            panels.add(VGroup(frame, ax, t))
        panels.arrange(RIGHT, buff=0.45).move_to(DOWN * 0.35)

        def curves(n):
            S = w[f"S{n}"].astype(float)
            g = VGroup()
            for j, (_, f, col) in enumerate(scal):
                ax = panels[j][1]
                ys = np.clip(S * f(n), -Y, Y)
                g.add(path_curve(ax, ys, color=col, stroke_width=2.2 if n < 1024 else 1.6))
            return g

        def nlabel(n):
            return MathTex(rf"n = {n:,}".replace(",", "{,}"), font_size=40).to_edge(UP, buff=0.35)

        off = label(r"off the chart", font_size=24, color=C.RIGHT_PT)
        off.next_to(panels[2][0], DOWN, buff=0.15)
        frozen = label(r"freezes flat", font_size=24, color=GREY_B).next_to(panels[0][0], DOWN, buff=0.15)
        alive = label(r"stays alive", font_size=24, color=C.BROWNIAN).next_to(panels[1][0], DOWN, buff=0.15)
        cur, nl = curves(16), nlabel(16)
        same = note(r"the same coin flips in all three panels; only the step height differs", font_size=24)
        same.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Here's that argument as a picture. Three panels, the same coin flips in each; only the step height "
            "differs. <bookmark mark='g'/> Now let n grow. Sixty-four steps. Two hundred and fifty-six. A thousand. Four "
            "thousand. <bookmark mark='e'/> With steps as small as delta t, the walk flattens to nothing. "
            "<bookmark mark='q'/> With the fourth root, it runs off the chart. <bookmark mark='m'/> But with the square "
            "root, the picture keeps the same overall size and just gets finer and finer, rougher and rougher."
        ) as vo:
            self.play(FadeIn(panels), FadeIn(nl), FadeIn(same))
            self.play(LaggedStart(*[Create(c) for c in cur], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("g")
            per = max(0.6, (vo.until("e") - 0.2) / 4)
            for n in WALK_NS[1:]:
                self.play(Transform(cur, curves(n)), Transform(nl, nlabel(n)), run_time=per)
            vo.wait_until("e")
            self.play(FadeIn(frozen))
            vo.wait_until("q")
            self.play(FadeIn(off))
            vo.wait_until("m")
            self.play(FadeIn(alive), Indicate(panels[1][2], color=C.BROWNIAN))
        self.clear_scene()

    # ------------------------------------------------------------------
    def bell(self):
        w = load("walk")
        paths = w["paths64"].astype(float) / 8.0
        ends = w["ends64"].astype(float) / 8.0
        ax = tw_axes(x_length=7.0, y_range=(-3.2, 3.2, 1), y_length=5.6).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        hax = Axes(x_range=[0, 0.5, 0.25], y_range=[-3.2, 3.2, 1], x_length=3.4, y_length=5.6, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False})
        hax.next_to(ax, RIGHT, buff=0.15)
        hax.x_axis.set_opacity(0)
        edges = np.arange(-3.375, 3.376, 0.25)
        fan = VGroup(*[path_curve(ax, p, color=C.BROWNIAN, stroke_width=1.3).set_stroke(opacity=0.35) for p in paths])
        sizes = [200, 2000, 20000]
        hists = [hist_shape(hax, edges, density(ends[:m], edges), sideways=True) for m in sizes]
        xs = np.linspace(-3.2, 3.2, 200)
        normal = pdf_curve(hax, xs, gauss_pdf(xs), color=WHITE, stroke_width=2.5, sideways=True)
        clt = MathTex(r"X_1", r"=", r"\frac{\xi_1 + \cdots + \xi_n}{\sqrt n}", r"\;\longrightarrow\;",
                      r"\mathcal N(0, 1)", font_size=40).to_edge(UP, buff=0.45)
        clt[0].set_color(C.BROWNIAN)
        clt[4].set_color(C.PDF)
        count = MathTex(r"200 \text{ walks}", font_size=30, color=C.PDF).next_to(hax, DOWN, buff=0.15)
        sim = note(r"simulated: $n = 64$ coin flips per walk").to_corner(DR, buff=0.3)

        with self.voiceover(
            "And what does the endpoint look like? <bookmark mark='c'/> At time one, it's a sum of n independent coin "
            "flips, divided by root n. <bookmark mark='l'/> The central limit theorem says that as n grows, that becomes a "
            "bell curve: a normal distribution with mean zero and variance one. <bookmark mark='p'/> Run many walks, and "
            "pile up where they end."
        ) as vo:
            vo.wait_until("c")
            self.play(Write(clt[:3]))
            vo.wait_until("l")
            self.play(Write(clt[3:]))
            vo.wait_until("p")
            self.play(Create(ax), FadeIn(ax.x_labels), FadeIn(sim))
            self.play(LaggedStart(*[Create(p) for p in fan], lag_ratio=0.02), run_time=vo.remaining() + 0.5)
        h = hists[0]
        with self.voiceover(
            "Two hundred walks. <bookmark mark='a'/> Two thousand. <bookmark mark='b'/> Twenty thousand. "
            "<bookmark mark='n'/> And the bell curve emerges."
        ) as vo:
            self.play(FadeIn(h), FadeIn(count))
            vo.wait_until("a")
            self.play(Transform(h, hists[1]), Transform(count, MathTex(r"2{,}000 \text{ walks}", font_size=30,
                                                                         color=C.PDF).move_to(count)))
            vo.wait_until("b")
            self.play(Transform(h, hists[2]), Transform(count, MathTex(r"20{,}000 \text{ walks}", font_size=30,
                                                                         color=C.PDF).move_to(count)))
            vo.wait_until("n")
            self.play(Create(normal))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limit(self):
        f = load("fan")
        ax = tw_axes(x_length=9.6, y_range=(-3.2, 3.2, 1), y_length=5.2).move_to(LEFT * 1.4 + DOWN * 0.05)
        labels = VGroup(MathTex("t", font_size=30, color=C.CLOCK).next_to(ax.x_axis.get_end(), RIGHT, buff=0.15),
                        MathTex("W_t", font_size=30, color=C.BROWNIAN).next_to(ax.y_axis.get_end(), UP, buff=0.1))
        fan = VGroup(*[path_curve(ax, p, color=C.BROWNIAN, stroke_width=1.1).set_stroke(opacity=0.25)
                       for p in f["paths"]])
        env = VGroup()
        for k, op in [(1, 0.95), (2, 0.6)]:
            for s in (1, -1):
                env.add(ax.plot(lambda t, k=k, s=s: s * k * np.sqrt(t), x_range=[0, 1, 0.005], color=C.CLOCK,
                                stroke_width=2.5).set_stroke(opacity=op))
        env_l = VGroup(MathTex(r"\pm\sqrt t", font_size=30, color=C.CLOCK).next_to(ax.c2p(1.08, 1), RIGHT, buff=0.1),
                       MathTex(r"\pm 2\sqrt t", font_size=30, color=C.CLOCK).next_to(ax.c2p(1.08, 2), RIGHT, buff=0.1))
        snaps = VGroup()
        edges = np.linspace(-3.2, 3.2, 33)
        scale = 0.16  # data units of t per unit of density, so each snapshot fits between the times
        for key, t in [("t25", 0.25), ("t50", 0.5), ("t100", 1.0)]:
            dens = density(f[key], edges) * scale
            base = t
            hs = hist_shape(ax, edges, dens, sideways=True, base=base, fill_opacity=0.3)
            xs = np.linspace(-3.2, 3.2, 160)
            cv = pdf_curve(ax, xs, gauss_pdf(xs, 0, t) * scale, color=C.PDF, sideways=True, base=base, stroke_width=2.5)
            tl = MathTex(rf"\mathcal N(0,\,{t:g})", font_size=26, color=C.PDF).next_to(ax.c2p(t, -3.2), DOWN, buff=0.15)
            snaps.add(VGroup(hs, cv, tl))
        inside1, inside2 = f["inside"]
        stat = label(rf"at $t = 1$: {100 * inside1:.1f}\% of 20{{,}}000 paths within $\pm\sqrt t$,"
                     rf" {100 * inside2:.1f}\% within $\pm 2\sqrt t$", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.12)
        title = MathTex(r"W_t \sim \mathcal N(0,\, t)", font_size=44).to_corner(UR, buff=0.5)
        title.set_color(C.BROWNIAN)

        with self.voiceover(
            "Take the limit at every time, not just at the end, and you get Brownian motion, written W of t. "
            "<bookmark mark='f'/> Here are two hundred of its paths. <bookmark mark='s'/> At each time t, W of t is a bell "
            "curve with mean zero and variance t. <bookmark mark='e'/> So the spread of the paths grows like the square root "
            "of t: about two thirds stay within one root t, and ninety-five percent within two. The same square root "
            "law that Einstein found for the spreading cloud."
        ) as vo:
            self.play(Create(ax), FadeIn(labels), FadeIn(ax.x_labels))
            vo.wait_until("f")
            self.play(LaggedStart(*[Create(p) for p in fan], lag_ratio=0.01), run_time=2.2)
            vo.wait_until("s")
            self.play(FadeIn(title))
            self.play(LaggedStart(*[FadeIn(s) for s in snaps], lag_ratio=0.4), run_time=2)
            vo.wait_until("e")
            self.play(*[Create(e) for e in env], FadeIn(env_l))
            self.play(FadeIn(stat))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def definition(self):
        title = label(r"Brownian motion $W_t$", font_size=44).to_edge(UP, buff=0.45)
        props = VGroup(
            VGroup(label(r"1.", font_size=32), mtex(r"W_0 = 0", font_size=36)),
            VGroup(label(r"2.", font_size=32), label(r"increments over disjoint intervals are independent", font_size=32)),
            VGroup(label(r"3.", font_size=32), MathTex(r"W_t - W_s \sim \mathcal N(0,\;", r"t - s", r")", font_size=36)),
            VGroup(label(r"4.", font_size=32), label(r"$t \mapsto W_t$ is continuous", font_size=32)),
        )
        for p in props:
            p.arrange(RIGHT, buff=0.3)
        props.arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(title, DOWN, buff=0.45).to_edge(LEFT, buff=1.0)
        props[2][1][1].set_color(C.CLOCK)

        ax = tw_axes(x_length=7.5, y_range=(-1.0, 1.6, 0.5), y_length=2.6, numbers=False).to_edge(DOWN, buff=0.5).shift(RIGHT * 2.5)
        from videos.stochastic.common import hero
        W = hero(4096)
        path = path_curve(ax, W, stroke_width=2.2)
        s, t = 0.35, 0.8
        ws, wt = W[int(s * 4096)], W[int(t * 4096)]
        ms = DashedLine(ax.c2p(s, -1.0), ax.c2p(s, 1.6), color=GREY_B, stroke_width=1.5)
        mt = DashedLine(ax.c2p(t, -1.0), ax.c2p(t, 1.6), color=GREY_B, stroke_width=1.5)
        sl = MathTex("s", font_size=28, color=C.CLOCK).next_to(ax.c2p(s, -1.0), DOWN, buff=0.1)
        tl = MathTex("t", font_size=28, color=C.CLOCK).next_to(ax.c2p(t, -1.0), DOWN, buff=0.1)
        inc = Arrow(ax.c2p(t, ws), ax.c2p(t, wt), buff=0, color=C.QV, stroke_width=4)
        hline = DashedLine(ax.c2p(s, ws), ax.c2p(t, ws), color=C.QV, stroke_width=2)
        inc_l = MathTex(r"W_t - W_s", font_size=28, color=C.QV).next_to(inc, RIGHT, buff=0.12)
        credit = note(r"Wiener (1923): it exists. \ Donsker (1951): rescaled random walks converge to it.", font_size=24)
        credit.to_corner(DL, buff=0.35)

        with self.voiceover(
            "Let's pin down exactly what we've built. <bookmark mark='a'/> Brownian motion starts at zero. "
            "<bookmark mark='b'/> What it does over one stretch of time is independent of what it did over any earlier "
            "stretch, just like fresh coin flips. <bookmark mark='c'/> Each increment, from time s to time t, is a bell "
            "curve with mean zero and variance t minus s: the elapsed time. <bookmark mark='d'/> And its paths are "
            "continuous: no jumps."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(FadeIn(props[0], shift=RIGHT * 0.2), Create(ax), Create(path))
            vo.wait_until("b")
            self.play(FadeIn(props[1], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(props[2], shift=RIGHT * 0.2), Create(ms), Create(mt), FadeIn(sl), FadeIn(tl))
            self.play(Create(hline), GrowArrow(inc), FadeIn(inc_l))
            vo.wait_until("d")
            self.play(FadeIn(props[3], shift=RIGHT * 0.2))
        with self.voiceover(
            "Norbert Wiener proved in 1923 that a process with exactly these properties exists, and Monroe Donsker "
            "proved that rescaled random walks converge to it, whatever the step distribution, as long as it has mean "
            "zero and finite variance. So Brownian motion is universal: it's what any accumulation of many small, "
            "independent kicks looks like from far away."
        ) as vo:
            self.play(FadeIn(credit))
        self.wait(0.4)
        self.clear_scene()
