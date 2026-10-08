from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.stochastic.common import (Raster, axis_labels, fmt_int, glow, hero, label, load, mtex, note, num,
                                      num_table, path_curve, polyline, splat, traced_path, tw_axes)

SUB = 8  # substeps per frame in hook2d's single particle


class Hook(VoiceoverScene):
    def construct(self):
        self.pollen()
        self.kicks()
        self.cloud()
        self.one_path()
        self.puzzle()
        self.roadmap()

    # ------------------------------------------------------------------
    def pollen(self):
        P = load("hook2d")["particle"]
        R = 3.3
        P = P - P.mean(axis=0)
        P = P * min(1.0, 0.92 * R / np.abs(P).max())
        k = ValueTracker(0.0)
        n_frames = (len(P) - 1) // SUB

        lens = VGroup(*[Circle(radius=R + 0.05 + 0.06 * i, stroke_color=GREY_D, stroke_width=6 - 1.5 * i,
                               stroke_opacity=0.9 - 0.25 * i) for i in range(3)])
        field = Circle(radius=R, stroke_width=0, fill_color="#16202B", fill_opacity=1)
        rng = np.random.default_rng(3)
        specks = VGroup(*[Dot([r * np.cos(a), r * np.sin(a), 0], radius=0.012, color=GREY_D)
                          for r, a in zip(R * np.sqrt(rng.uniform(0, 0.95, 140)), rng.uniform(0, 2 * np.pi, 140))])

        def pos(i):
            return np.array([P[i, 0], P[i, 1], 0.0])

        def trail():
            i = int(k.get_value() * SUB)
            lo = max(0, i - 640)
            g = VGroup()
            for a in range(lo, i, 32):
                b = min(i, a + 32) + 1
                op = 0.06 + 0.8 * (a - lo) / 640
                seg = VMobject(stroke_color=C.BROWNIAN, stroke_width=2.4, stroke_opacity=op)
                seg.set_points_as_corners([pos(j) for j in range(a, b)])
                g.add(seg)
            return g

        def grain():
            p = pos(int(k.get_value() * SUB))
            return VGroup(Dot(p, radius=0.22, color=C.BROWNIAN, fill_opacity=0.12),
                          Dot(p, radius=0.14, color=C.BROWNIAN, fill_opacity=0.3),
                          Dot(p, radius=0.075, color=WHITE))

        tr, gr = always_redraw(trail), always_redraw(grain)
        year = label(r"Robert Brown, 1827", font_size=30, color=GREY_A).to_corner(UL, buff=0.45)
        sim = note(r"simulated: a 2D random walk of 3{,}360 tiny Gaussian kicks").to_corner(DR, buff=0.3)

        with self.voiceover(
            "In 1827, the botanist Robert Brown put grains of pollen in water, and looked at the tiny particles they "
            "released under his microscope. <bookmark mark='j'/> The particles never stopped moving. Each one "
            "jittered, darting this way and that, for no visible reason."
        ) as vo:
            self.play(FadeIn(field), FadeIn(lens), FadeIn(specks), FadeIn(year))
            self.add(tr, gr)
            vo.wait_until("j")
            self.play(k.animate.set_value(n_frames * 0.55), FadeIn(sim), run_time=vo.remaining() + 0.3, rate_func=linear)
        with self.voiceover(
            "And the jitter isn't a vibration around some home position. The particle wanders. Watch its trail: it never "
            "settles, and it never retraces a smooth curve."
        ) as vo:
            self.play(k.animate.set_value(n_frames), run_time=vo.remaining(), rate_func=linear)
        tr.clear_updaters()
        gr.clear_updaters()
        self.play(FadeOut(VGroup(tr, gr, specks, sim, year)), FadeOut(field), FadeOut(lens))

    # ------------------------------------------------------------------
    def kicks(self):
        """Schematic: molecules hit the particle from every side; the net kick is never zero."""
        particle = Circle(radius=0.6, stroke_color=WHITE, stroke_width=2, fill_color=C.BROWNIAN, fill_opacity=0.55)

        def hits(seed):
            r = np.random.default_rng(seed)
            angles = np.sort(r.uniform(0, 2 * np.pi, 26))
            strength = r.uniform(0.25, 1.0, 26)
            g, net = VGroup(), np.zeros(3)
            for a, s_ in zip(angles, strength):
                u = np.array([np.cos(a), np.sin(a), 0.0])
                start = u * (1.75 + 0.5 * s_)
                g.add(Dot(start, radius=0.07, color=GREY_B))
                g.add(Arrow(start, u * 0.66, buff=0.08, color=GREY_B, stroke_width=2.5, stroke_opacity=0.35 + 0.5 * s_,
                            max_tip_length_to_length_ratio=0.18))
                net -= u * s_
            arrow = Arrow(ORIGIN, net * 0.55, buff=0, color=C.QV, stroke_width=6, max_tip_length_to_length_ratio=0.25)
            return g, arrow

        g, net = hits(0)
        net_l = label(r"net kick", font_size=28, color=C.QV).next_to(net.get_end(), UR, buff=0.1)
        tag = note(r"schematic").to_corner(UR, buff=0.3)
        title = label(r"Einstein, 1905", font_size=34, color=GREY_A).to_corner(UL, buff=0.45)
        with self.voiceover(
            "In 1905, Einstein explained it. <bookmark mark='m'/> The particle is being hit from every side by water "
            "molecules, <bookmark mark='n'/> and at any instant the kicks never quite cancel. The leftover push points "
            "somewhere new every moment."
        ) as vo:
            self.play(FadeIn(title), FadeIn(particle), FadeIn(tag))
            vo.wait_until("m")
            self.play(LaggedStart(*[FadeIn(m) for m in g], lag_ratio=0.02), run_time=1.2)
            vo.wait_until("n")
            self.play(GrowArrow(net), FadeIn(net_l))
            seeds = iter(range(1, 50))
            while vo.remaining(0) > 0.9:
                g2, net2 = hits(next(seeds))
                self.play(Transform(g, g2), Transform(net, net2), net_l.animate.next_to(net2.get_end(), UR, buff=0.1),
                          run_time=0.6)
        self.play(FadeOut(VGroup(g, net, net_l, particle, tag, title)))

    # ------------------------------------------------------------------
    def cloud(self):
        d = load("hook2d")
        cloud, msd = d["cloud"], d["msd"]
        n_frames = len(cloud) - 1
        k = ValueTracker(0.0)
        extent = (-7.11, 7.11, -4.0, 4.0)
        shape = (640, 1138)

        def draw(v):
            pts = cloud[int(round(v))]
            return glow(splat(pts[:, 0], pts[:, 1], extent, shape, sigma=1.4), C.BROWNIAN, gain=1.4)

        img = Raster(draw, k, 14.22, 8.0, ORIGIN)

        def ring():
            r = float(np.sqrt(msd[int(round(k.get_value()))]))
            return Circle(radius=max(r, 0.01), stroke_color=C.QV, stroke_width=2.5).set_stroke(opacity=0.9)

        rg = always_redraw(ring)
        # Inset: mean squared displacement grows linearly in time (Einstein, 1905)
        ax = Axes(x_range=[0, n_frames, n_frames], y_range=[0, msd.max() * 1.05, msd.max()], x_length=3.4, y_length=2.1,
                  tips=False, axis_config={"stroke_color": GREY_B, "include_ticks": False}).to_corner(DR, buff=0.5)
        bg = BackgroundRectangle(ax, color=BACKGROUND, fill_opacity=0.85, buff=0.35)
        xl = MathTex("t", font_size=26, color=C.CLOCK).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        yl = MathTex(r"\langle r^2 \rangle", font_size=26, color=C.QV).next_to(ax.y_axis.get_end(), UP, buff=0.08)
        theory = ax.plot(lambda x: 2 * 0.12**2 * x, x_range=[0, n_frames], color=GREY_B, stroke_width=2)
        theory.set_stroke(opacity=0.6)
        ks = np.arange(n_frames + 1)

        def msd_curve():
            j = max(2, int(round(k.get_value())) + 1)
            return polyline(ax, ks[:j], msd[:j], color=C.QV, stroke_width=3)

        mc = always_redraw(msd_curve)
        einstein = VGroup(label(r"Einstein, 1905:", font_size=30),
                          mtex(r"\langle r^2 \rangle \propto t", font_size=32, color=C.QV)).arrange(RIGHT, buff=0.2)
        einstein.to_corner(UL, buff=0.45)
        width = label(r"width $\propto \sqrt{t}$", font_size=28, color=C.QV)
        sim = note(r"2{,}000 simulated particles released at one point").to_corner(DL, buff=0.3)

        einstein.add_background_rectangle(color=BACKGROUND, opacity=0.8, buff=0.12)
        with self.voiceover(
            "<bookmark mark='c'/> Release a crowd of such particles from one point, and they spread out like a drop of "
            "ink. <bookmark mark='w'/> Einstein's key prediction was how fast: the average squared "
            "distance grows in proportion to time, <bookmark mark='s'/> so the width of the cloud grows like the square "
            "root of time. A few years later, Jean Perrin measured exactly that, and used it to count molecules."
        ) as vo:
            vo.wait_until("c")
            self.add(img)
            self.play(FadeIn(sim), k.animate.set_value(n_frames * 0.3), run_time=vo.until("w"), rate_func=linear)
            self.add(rg)
            self.play(FadeIn(bg), Create(ax), FadeIn(xl), FadeIn(yl), Create(theory), FadeIn(einstein),
                      k.animate.set_value(n_frames * 0.42), run_time=1.5, rate_func=linear)
            self.add(mc)
            self.play(k.animate.set_value(n_frames * 0.7), run_time=vo.until("s"), rate_func=linear)
            width.next_to(rg, UP, buff=0.1)
            width.add_background_rectangle(color=BACKGROUND, opacity=0.7)
            self.play(FadeIn(width), k.animate.set_value(n_frames), run_time=vo.remaining(), rate_func=linear)
        self.clear_scene()

    # ------------------------------------------------------------------
    def one_path(self):
        ax = tw_axes(x_length=11.5, y_range=(-1.0, 1.6, 0.5), y_length=4.4).move_to(DOWN * 0.9)
        labels = axis_labels(ax)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(1, 0), color=GREY_D, stroke_width=1.5, dash_length=0.08)
        t = ValueTracker(0.0)
        path = traced_path(ax, hero(), t)
        title = label(r"Brownian motion", font_size=48).to_edge(UP, buff=0.5)
        who = note(r"Bachelier (1900): prices on the Paris Bourse \quad Einstein (1905): diffusion"
                   r" \quad Wiener (1923): a rigorous construction", font_size=22).next_to(title, DOWN, buff=0.2)
        with self.voiceover(
            "Now follow just one coordinate of one particle as time goes by, and you get a graph like this. "
            "<bookmark mark='b'/> This is Brownian motion: the mathematician's idealized version of that jitter. "
            "<bookmark mark='h'/> Louis Bachelier used it in 1900 to model prices on the Paris stock exchange, and "
            "Norbert Wiener made it rigorous in the 1920s. Today it's the basic model of noise in physics, biology, "
            "engineering, and finance."
        ) as vo:
            self.play(Create(ax), FadeIn(ax.x_labels), FadeIn(labels), Create(zero))
            self.add(path)
            self.play(t.animate.set_value(1.0), run_time=vo.until("h") + 0.5, rate_func=linear)
            self.play(FadeIn(title), FadeIn(who))
        path.curve.clear_updaters()
        self.remove(path)
        self.add(path.curve)
        tip = Dot(ax.c2p(1, hero()[-1]), radius=0.06, color=WHITE)
        self.add(tip)
        self.play(FadeOut(VGroup(title, who)))
        self.ax, self.path, self.labels, self.zero, self.tip = ax, path.curve, labels, zero, tip

    # ------------------------------------------------------------------
    def puzzle(self):
        h = load("hero")
        WT = float(hero()[-1])
        left, n = float(h["left"][-1]), int(h["n"][-1])
        assert n == 4_194_304 and abs(0.5 * WT**2 - left - 0.5) < 0.001

        ordinary = mtex(r"\int_0^{x} s\,ds = \tfrac12 x^2", font_size=40)
        oc = note(r"ordinary calculus", font_size=24)
        VGroup(ordinary, oc).arrange(DOWN, buff=0.12).to_corner(UL, buff=0.5)
        guess = MathTex(r"\int_0^1 W\,dW", r"\overset{?}{=}", r"\tfrac12 W_1^2", font_size=46)
        guess[0].set_color(C.GAINS)
        guess.to_edge(UP, buff=0.55).shift(RIGHT * 1.2)

        graph = VGroup(self.ax, self.ax.x_labels, self.path, self.labels, self.zero, self.tip)
        with self.voiceover(
            "And it breaks ordinary calculus. Here's a simple test. <bookmark mark='o'/> In ordinary calculus, the "
            "integral of s d s, from zero to x, is x squared over two. <bookmark mark='g'/> So for our path, the "
            "integral of W d W, from time zero to time one, ought to be W at time one, squared, over two."
        ) as vo:
            self.play(graph.animate.scale(0.6).to_corner(DL, buff=0.45))
            vo.wait_until("o")
            self.play(Write(ordinary), FadeIn(oc))
            vo.wait_until("g")
            self.play(Write(guess))

        ax = self.ax
        col_x = 3.6
        sum_ = MathTex(r"\sum_{i} W_{t_i}\,\big(W_{t_{i+1}} - W_{t_i}\big)", font_size=40).move_to([col_x, 1.55, 0])
        steps = note(rf"${fmt_int(n)}$ steps, \ $\Delta t = 1/{fmt_int(n)}$", font_size=24).next_to(sum_, DOWN, buff=0.15)
        WT_dot = Dot(ax.c2p(1, WT), radius=0.07, color=C.BROWNIAN)
        WT_l = MathTex(rf"W_1 = {WT:.4f}", font_size=28, color=C.BROWNIAN).next_to(WT_dot, RIGHT, buff=0.15)
        res = VGroup(
            MathTex(r"\tfrac12 W_1^2", "=", num(0.5 * WT**2, 4), font_size=42),
            MathTex(r"\textstyle\sum W\,\Delta W", "=", num(left, 4), font_size=42),
            MathTex(r"\text{gap}", "=", num(0.5 * WT**2 - left, 4), font_size=42),
        )
        for i, r in enumerate(res):
            r.shift([col_x - r[1].get_center()[0], -0.15 - 0.85 * i - r[1].get_center()[1], 0])
        res[1][0].set_color(C.GAINS)
        res[1][2].set_color(C.GAINS)
        res[2].set_color(C.QV)
        line = Line(res[1].get_corner(DL) + DOWN * 0.18 + LEFT * 0.2, res[1].get_corner(DR) + DOWN * 0.18 + RIGHT * 0.2,
                    color=GREY_C, stroke_width=1.5)

        with self.voiceover(
            "Let's just compute it, the way integrals are defined: <bookmark mark='s'/> chop time into steps, multiply "
            "W by its change over each step, and add up. We'll use more than four million steps. "
            "<bookmark mark='w'/> Our path ends at 1.2528, so half its square is 0.7847. <bookmark mark='r'/> But the sum "
            "comes out to 0.2847. <bookmark mark='d'/> We're off by 0.5000."
        ) as vo:
            vo.wait_until("s")
            self.play(Write(sum_), FadeIn(steps))
            vo.wait_until("w")
            self.play(FadeIn(WT_dot), FadeIn(WT_l), FadeIn(res[0]))
            vo.wait_until("r")
            self.play(FadeIn(res[1]))
            vo.wait_until("d")
            self.play(Create(line), FadeIn(res[2]))
            self.play(Indicate(res[2], color=C.QV))
        self.wait(0.5)

        # Five more paths
        o = load("others")
        rows = o["rows"]
        others = VGroup(*[path_curve(ax, p_, color=C.BROWNIAN, stroke_width=1.6).set_stroke(opacity=0.55) for p_ in o["paths"]])
        tab = num_table([r"W_1", r"\sum W\,\Delta W", r"\tfrac12 W_1^2", r"\text{gap}"],
                        [[num(r[0], 3), num(r[1], 3), num(r[2], 3), num(r[3], 3)] for r in rows],
                        font_size=30, col_colors=[C.BROWNIAN, C.GAINS, WHITE, C.QV])
        tab.move_to([col_x, -0.2, 0])
        gaps = ", ".join(f"{g:.3f}" for g in rows[:, 3])
        with self.voiceover(
            "Maybe that path was special. So here are five more, each with sixty-five thousand steps. "
            f"<bookmark mark='t'/> The gaps: {gaps}. Every time, almost exactly one half."
        ) as vo:
            self.play(FadeOut(VGroup(res, line, WT_dot, WT_l, steps, sum_)), self.path.animate.set_stroke(opacity=0.25),
                      FadeOut(self.tip))
            self.play(LaggedStart(*[Create(p_) for p_ in others], lag_ratio=0.2), run_time=2)
            vo.wait_until("t")
            self.play(FadeIn(tab.header), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.35), run_time=vo.remaining())
        self.play(Indicate(tab.cols[3], color=C.QV, scale_factor=1.1))

        itos = MathTex(r"\int_0^1 W\,dW", "=", r"\tfrac12 W_1^2", r"-\;\tfrac12", font_size=48)
        itos[0].set_color(C.GAINS)
        itos[3].set_color(C.QV)
        itos.move_to(guess, LEFT)
        with self.voiceover(
            "That missing half isn't rounding error, and it isn't bad luck. <bookmark mark='i'/> The true answer is "
            "one half W squared, minus one half. And that extra term is the first sign of a different kind of calculus: "
            "stochastic calculus, created by Kiyosi Itô in the 1940s."
        ) as vo:
            vo.wait_until("i")
            self.play(FadeOut(guess), FadeOut(VGroup(ordinary, oc)), Write(itos))
            self.play(Circumscribe(itos[3], color=C.QV))
        self.clear_scene()

    # ------------------------------------------------------------------
    def roadmap(self):
        items = [
            (r"Brownian motion", r"(dW)^2 = dt", C.QV),
            (r"The It\^o integral", r"\int_0^t W\,dW = \tfrac12 W_t^2 - \tfrac12 t", C.GAINS),
            (r"It\^o's lemma", r"df = f'\,dW + \tfrac12 f''\,dt", C.QV),
            (r"Equations of noise", r"\partial_t p = -\partial_x(\mu p) + \tfrac12\partial_x^2(\sigma^2 p)", C.PDF),
            (r"Pricing and changing the odds", r"V_t + rSV_S + \tfrac12\sigma^2S^2V_{SS} = rV", C.OPTION),
        ]
        title = label(r"The plan", font_size=44).to_edge(UP, buff=0.4)
        names = VGroup()
        for i, (name, _, _) in enumerate(items, 1):
            n = label(rf"Part {i}", font_size=28, color=C.DIM)
            t = label(name, font_size=34).next_to(n, RIGHT, buff=0.35)
            names.add(VGroup(n, t))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(title, DOWN, buff=0.55).to_edge(LEFT, buff=0.7)
        rows = VGroup()
        for nm, (_, formula, col) in zip(names, items):
            f = mtex(formula, font_size=32, color=col)
            f.move_to([4.0, nm.get_center()[1], 0])
            rows.add(VGroup(nm[0], nm[1], f))

        with self.voiceover(
            "Here's the plan. <bookmark mark='a'/> First, Brownian motion itself, and the one strange fact that drives "
            "everything else: d W squared equals d t. <bookmark mark='b'/> Then the Itô integral, and where the missing "
            "half comes from. <bookmark mark='c'/> Then Itô's lemma: the chain rule, corrected for randomness. "
            "<bookmark mark='d'/> Then the equations of noise, and a surprising bridge between random paths and the "
            "partial differential equations of physics. <bookmark mark='e'/> And finally two payoffs: how Black and "
            "Scholes priced options by hedging the noise away, and how Girsanov's theorem changes the odds."
        ) as vo:
            self.play(FadeIn(title))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r[0]), FadeIn(r[1], shift=RIGHT * 0.2), Write(r[2]), run_time=1.2)
        self.wait(0.6)
        self.clear_scene()
