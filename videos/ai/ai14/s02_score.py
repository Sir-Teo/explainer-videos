from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import DATA, NOISE, SCORE, arrows_field, cloud, load


class Score(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.objective()
        self.landscape()
        self.field()

    def card(self):
        card = chapter_card(1, r"Learning to denoise", r"How does a network learn the score?", part=14, lit=(2015,))
        with self.voiceover("Chapter one. Learning to denoise."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def objective(self):
        t = load("toy")
        data = np.asarray(t["data"])[:500]
        g = np.random.default_rng(0)
        eps = g.normal(size=data.shape)
        a, s = np.cos(np.pi * 0.35 / 2), np.sin(np.pi * 0.35 / 2)
        noisy = a * data + s * eps
        S, sh = 0.75, np.array([-3.4, -0.6])
        pts = cloud(data, DATA, radius=0.025, scale=S, shift=sh)
        colors = {r"x_0": DATA, r"\varepsilon": NOISE, r"\hat\varepsilon_\theta": SCORE}
        f1 = cmath(r"x_t", "=", r"\alpha_t\,", r"x_0", "+", r"\sigma_t\,", r"\varepsilon", colors=colors, font_size=40)
        f2 = cmath(r"\mathcal{L}", "=", r"\big\|", r"\hat\varepsilon_\theta", r"(x_t, t)", "-", r"\varepsilon", r"\big\|^2",
                   colors=colors, font_size=40)
        f3 = cmath(r"\nabla \log p_t(x_t)", r"\;\approx\;", r"-\,\hat\varepsilon_\theta(x_t, t)\,/\,\sigma_t",
                   colors={r"-\,\hat\varepsilon_\theta(x_t, t)\,/\,\sigma_t": SCORE}, font_size=40)
        fs = VGroup(f1, f2, f3).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.0, 0.6, 0])
        l1 = label(r"add noise, \ any amount", font_size=22, color=GREY_A).next_to(f1, DOWN, buff=0.1).align_to(f1, LEFT)
        l2 = label(r"train a network to guess the noise", font_size=22, color=GREY_A).next_to(f2, DOWN, buff=0.1).align_to(f2, LEFT)
        l3 = label(r"and the guess \emph{is} the score, \ Part 4's arrows", font_size=22, color=SCORE).next_to(f3, DOWN, buff=0.1)
        l3.align_to(f3, LEFT)
        idx = list(range(0, 500, 25))
        arrows = VGroup(*[Arrow([noisy[i, 0] * S + sh[0], noisy[i, 1] * S + sh[1], 0],
                                [data[i, 0] * S + sh[0], data[i, 1] * S + sh[1], 0], buff=0, color=SCORE, stroke_width=2,
                                max_tip_length_to_length_ratio=0.2) for i in idx])
        cite_ = cite(r"J.~Ho, A.~Jain \& P.~Abbeel, \textit{DDPM} (2020); \ Y.~Song et al., \textit{Score-Based SDEs} (2021)", corner=DR)
        with self.voiceover(
            "In part four, we ran Brownian motion backwards to turn noise into the letters A I, but we cheated: we "
            "computed the score, the uphill direction of the data's density, from the data itself. A real model has to "
            "learn it. <bookmark mark='a'/> Here's how. Take a data point, add a random amount of noise. "
            "<bookmark mark='b'/> Train a network to look at the noisy point and guess the noise that was added. "
            "That's all: a regression. <bookmark mark='c'/> And the guess, divided by the noise level, turns out to "
            "be exactly the score. Learning to denoise is learning the arrows."
        ) as vo:
            self.play(FadeIn(pts), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(l1), *[d.animate.move_to([p[0] * S + sh[0], p[1] * S + sh[1], 0])
                                               for d, p in zip(pts, noisy)], run_time=2.0)
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(l2))
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("c")
            self.play(Write(f3), FadeIn(l3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def landscape(self):
        t = load("toy")
        lx, ly = np.asarray(t["land_x"]), np.asarray(t["land_y"])
        ts = [float(v) for v in t["land_ts"]]
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-2, 2, 1], z_range=[0, 1, 0.5], x_length=9.0, y_length=6.0,
                          z_length=2.6, axis_config={"stroke_color": GREY_D, "include_ticks": False, "include_tip": False})
        axes.shift(DOWN * 0.4)

        def height(level):
            H = np.sqrt(np.asarray(t[f"land{level:g}"]))
            H = H / H.max()

            def h(u, v):  # bilinear, on the computed grid
                i = np.clip((v - ly[0]) / (ly[1] - ly[0]), 0, len(ly) - 1.001)
                j = np.clip((u - lx[0]) / (lx[1] - lx[0]), 0, len(lx) - 1.001)
                i0, j0 = int(i), int(j)
                fi, fj = i - i0, j - j0
                return float((1 - fi) * ((1 - fj) * H[i0, j0] + fj * H[i0, j0 + 1]) + fi * ((1 - fj) * H[i0 + 1, j0] + fj * H[i0 + 1, j0 + 1]))

            return loss_surface(axes, h, [-3, 3], [-2, 2], resolution=(60, 40), z_lo=0.0, z_hi=1.0, opacity=0.9,
                                stroke_width=0.2)

        surfs = [height(v) for v in ts]
        lab = [label(rf"noise level $t = {v:g}$", font_size=28, color=C.MODEL_Q).to_corner(UR, buff=0.4) for v in ts]
        note_ = label(r"height: \ the density of the noised data \ (square-rooted, \ each level scaled to fit)", font_size=20,
                      color=GREY_B).to_corner(DL, buff=0.35)
        for m in (*lab, note_):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        self.set_camera_orientation(phi=58 * DEGREES, theta=-62 * DEGREES, zoom=0.78)
        with self.voiceover(
            "Picture the data's density as a landscape over the plane. <bookmark mark='a'/> Under heavy noise, it's "
            "one smooth hill. <bookmark mark='b'/> Take the noise away, step by step, and the hill splits and "
            "sharpens into ridges, in the shape of the letters. The score is simply the uphill direction on this "
            "landscape, at every noise level. That's what the network has to learn."
        ) as vo:
            self.play(FadeIn(surfs[0]), FadeIn(lab[0]), FadeIn(note_), run_time=1.5)
            self.begin_ambient_camera_rotation(rate=0.05)
            vo.wait_until("b")
            cur = surfs[0]
            for i in range(1, len(ts)):
                self.play(Transform(cur, surfs[i]), FadeOut(lab[i - 1]), FadeIn(lab[i]), run_time=1.3)
            self.stop_ambient_camera_rotation()
            self.move_camera(phi=0, theta=-90 * DEGREES, zoom=0.9, run_time=2.0)  # from above: the letters
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    def field(self):
        t = load("toy")
        grid = np.asarray(t["grid"])
        ts = [float(v) for v in t["field_ts"]]
        data = np.asarray(t["data"])[:600]
        U, sh = 1.15, np.array([-0.6, -0.4])
        pts = cloud(data, DATA, radius=0.02, scale=U, shift=sh, opacity=0.5)
        fields = [arrows_field(grid, t[f"field{v:g}"], unit=U, shift=sh) for v in ts]
        tl = [label(rf"noise level $t = {v:g}$", font_size=28, color=SCORE).to_corner(UR, buff=0.4) for v in ts]
        head = label(r"the learned score: \ the trained network's arrows, \ on a grid", font_size=26, color=GREY_A)
        head.to_edge(UP, buff=0.35).shift(LEFT * 1.5)
        with self.voiceover(
            "Here are the arrows our trained network draws. <bookmark mark='a'/> At high noise, they all point "
            "roughly towards the middle: from far away, the data is one blob. <bookmark mark='b'/> As the noise "
            "drops, the arrows bend towards the letters, <bookmark mark='c'/> and at low noise they point to the "
            "nearest stroke. One network, told the noise level, knows the right arrows for every level: that's what "
            "a sampler needs to walk from noise to data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pts), FadeIn(fields[0]), FadeIn(tl[0]))
            vo.wait_until("b")
            self.play(ReplacementTransform(fields[0], fields[1]), ReplacementTransform(tl[0], tl[1]), run_time=1.5)
            self.play(ReplacementTransform(fields[1], fields[2]), ReplacementTransform(tl[1], tl[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(ReplacementTransform(fields[2], fields[3]), ReplacementTransform(tl[2], tl[3]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()
