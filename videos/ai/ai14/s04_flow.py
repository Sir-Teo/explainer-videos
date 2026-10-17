from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import DATA, FM_C, NOISE, RF_C, cloud, curve, load, move_cloud


class Flow(VoiceoverScene):
    def construct(self):
        self.card()
        self.straight()
        self.paths()
        self.reflow()

    def card(self):
        card = chapter_card(3, r"Flow matching", r"Why not go in a straight line?", part=14)
        with self.voiceover("Chapter three. Flow matching."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def straight(self):
        g = np.random.default_rng(5)
        f = load("flow")
        data = np.asarray(f["fm100"])[:12]
        noise = g.normal(size=(12, 2))
        S = 0.85
        pairs = VGroup()
        for z, x in zip(noise, data):
            a, b = np.array([z[0] * S - 3.0, z[1] * S - 0.4, 0]), np.array([x[0] * S + 0.2, x[1] * S - 0.4, 0])
            pairs.add(VGroup(Dot(a, radius=0.05, color=NOISE), Dot(b, radius=0.05, color=DATA),
                             DashedLine(a, b, color=GREY_B, stroke_width=1.5, dash_length=0.06)))
        colors = {r"x_0": NOISE, r"x_1": DATA, r"v_\theta": FM_C}
        f1 = cmath(r"x_t", "=", r"(1-t)\,", r"x_0", "+", r"t\,", r"x_1", colors=colors, font_size=38)
        f2 = cmath(r"\mathcal{L}", "=", r"\big\|", r"v_\theta", r"(x_t, t)", "-", r"(", r"x_1", "-", r"x_0", r")", r"\big\|^2",
                   colors=colors, font_size=38)
        f3 = cmath(r"x", r"\;\leftarrow\;", r"x", "+", r"v_\theta", r"(x, t)\,\Delta t", colors=colors, font_size=38)
        fs = VGroup(f1, f2, f3).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.2, 0.6, 0])
        l1 = label(r"pair a noise point with a data point", font_size=20, color=GREY_A).next_to(f1, DOWN, buff=0.08).align_to(f1, LEFT)
        l2 = label(r"learn the velocity of the straight line", font_size=20, color=GREY_A).next_to(f2, DOWN, buff=0.08).align_to(f2, LEFT)
        l3 = label(r"to sample: \ follow the learned velocity", font_size=20, color=FM_C).next_to(f3, DOWN, buff=0.08).align_to(f3, LEFT)
        cite_ = cite(r"Y.~Lipman et al., \textit{Flow Matching} (2023); \ X.~Liu et al., \textit{Rectified Flow} (2023)", corner=DR)
        with self.voiceover(
            "Flow matching asks for the simplest path there is. Pair a random noise point with a random data point "
            "and join them with a straight line. <bookmark mark='a'/> Train a network to output the velocity along "
            "that line: just the data point minus the noise point. <bookmark mark='b'/> To sample, start from noise "
            "and follow the learned velocity, a few steps at a time. It's the same idea as diffusion, with simpler "
            "bookkeeping, and it's what Stable Diffusion 3 and Flux are trained with."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p) for p in pairs], lag_ratio=0.1), Write(f1), FadeIn(l1), FadeIn(cite_), run_time=2.0)
            vo.wait_until("a")
            self.play(Write(f2), FadeIn(l2))
            vo.wait_until("b")
            self.play(Write(f3), FadeIn(l3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def paths(self):
        f = load("flow")
        P = np.asarray(f["fm_path"])
        S, sh = 0.75, np.array([-1.6, -0.5])
        n = 120
        trails = VGroup(*[VMobject(stroke_width=1.4, stroke_color=FM_C, stroke_opacity=0.7).set_points_smoothly(
            [[p[i, 0] * S + sh[0], p[i, 1] * S + sh[1], 0] for p in P[::5]]) for i in range(0, n, 3)])
        d = cloud(P[0][:n], NOISE, radius=0.03, scale=S, shift=sh)
        st = float(f["straight_fm"])
        note_ = label(r"each training line is straight, \\ but the learned paths bend: \\ "
                      r"a noise point could belong \\ to many data points", font_size=24, color=GREY_A).move_to([4.6, 0.8, 0])
        sl = label(rf"straightness: \ ${st:.3f}$ \\ ($1$ = a straight line)", font_size=24, color=FM_C).next_to(note_, DOWN, buff=0.4)
        with self.voiceover(
            "Here are the learned paths. <bookmark mark='a'/> Each training line was straight, but the paths bend. "
            "A noise point was paired with a different random data point every time, so the network learns the "
            "average direction, and averages of straight lines curve. <bookmark mark='b'/> Curved paths still need "
            "many steps."
        ) as vo:
            self.play(FadeIn(d))
            vo.wait_until("a")
            self.play(*move_cloud(d, P[-1][:n], S, sh), Create(trails), run_time=3.0)
            self.play(d.animate.set_color(DATA), FadeIn(note_))
            vo.wait_until("b")
            self.play(FadeIn(sl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reflow(self):
        f = load("flow")
        ks = [int(k) for k in f["steps"]]
        fm = np.array([float(f[f"sw_fm{k}"]) for k in ks])
        rf = np.array([float(f[f"sw_rf{k}"]) for k in ks])
        lx = np.log10(ks)
        hi = max(fm.max(), rf.max()) * 1.1
        ystep = next(v for v in (0.05, 0.1, 0.2, 0.25, 0.5, 1.0) if v >= hi / 5)  # round tick values
        ax = Axes(x_range=[-0.1, 2.1, 0.5], y_range=[0, hi, ystep], x_length=6.4, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-3.0, -0.8, 0])
        xt = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(ax.c2p(math.log10(k), 0), DOWN, buff=0.1) for k in ks])
        xn = label(r"sampling steps", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"distance from the real data", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        yt = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(ax.c2p(-0.1, v), LEFT, buff=0.08)
                      for v in np.arange(ystep, hi + 1e-9, ystep)])
        cf = VGroup(curve(ax, lx, fm, FM_C, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=FM_C) for a, b in zip(lx, fm)])
        cr = VGroup(curve(ax, lx, rf, RF_C, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=RF_C) for a, b in zip(lx, rf)])
        k1 = label(r"flow matching", font_size=24, color=FM_C).move_to([3.0, 2.4, 0])
        k2 = label(r"after reflow", font_size=24, color=RF_C).next_to(k1, DOWN, buff=0.2).align_to(k1, LEFT)
        S = 0.42
        one = VGroup(cloud(np.asarray(f["fm1"])[:400], FM_C, radius=0.018, scale=S),
                     cloud(np.asarray(f["rf1"])[:400], RF_C, radius=0.018, scale=S)).arrange(DOWN, buff=0.5).move_to([4.2, -1.0, 0])
        ol = VGroup(label(r"$1$ step", font_size=20, color=FM_C).next_to(one[0], LEFT, buff=0.15),
                    label(r"$1$ step", font_size=20, color=RF_C).next_to(one[1], LEFT, buff=0.15))
        s1, s2 = float(f["straight_fm"]), float(f["straight_rf"])
        with self.voiceover(
            "The fix is called reflow. Run the trained model to pair each noise point with the sample it actually "
            "leads to, and train a second model on those pairs. <bookmark mark='a'/> Now the pairs agree with each "
            f"other, and the paths straighten: from {s1:.3f} to {s2:.3f}. <bookmark mark='b'/> On a straight path, "
            "one big step lands where a hundred small ones would. Distilled this way, image models now make a "
            "picture in one to four steps."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(cf[0]), FadeIn(cf[1:]), FadeIn(k1))
            vo.wait_until("a")
            self.play(Create(cr[0]), FadeIn(cr[1:]), FadeIn(k2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(one), FadeIn(ol))
        self.wait(0.3)
        self.clear_scene()
