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
        self.learning()

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
        pts = cloud(data, DATA, radius=0.022, scale=U, shift=sh, opacity=0.8)
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
        # follow the arrows: 40 particles from random places, stepping along the learned field as its noise level falls
        xs, ys = np.unique(grid[:, 0]), np.unique(grid[:, 1])
        idx = {(round(float(a), 6), round(float(b), 6)): k for k, (a, b) in enumerate(grid)}

        def interp(F, q):  # bilinear on the grid
            fx = np.clip((q[0] - xs[0]) / (xs[1] - xs[0]), 0, len(xs) - 1.001)
            fy = np.clip((q[1] - ys[0]) / (ys[1] - ys[0]), 0, len(ys) - 1.001)
            i0, j0 = int(fx), int(fy)
            a, b = fx - i0, fy - j0
            v = lambda i, j: F[idx[(round(float(xs[i]), 6), round(float(ys[j]), 6))]]
            return ((1 - a) * (1 - b) * v(i0, j0) + a * (1 - b) * v(i0 + 1, j0) + (1 - a) * b * v(i0, j0 + 1)
                    + a * b * v(i0 + 1, j0 + 1))

        g = np.random.default_rng(14)
        Q = np.column_stack([g.uniform(-2.6, 2.6, 40), g.uniform(-1.7, 1.7, 40)])
        tracks = [Q.copy()]
        for v_ in ts:
            F = np.asarray(t[f"field{v_:g}"])
            eta = 0.035 / np.median(np.linalg.norm(F, axis=1))
            for _ in range(16):
                Q = Q + eta * np.array([interp(F, q) for q in Q])
                Q = np.clip(Q, [-3, -2], [3, 2])
                tracks.append(Q.copy())
        tracks = np.array(tracks)  # step, particle, xy

        def at(q):
            return [q[0] * U + sh[0], q[1] * U + sh[1], 0]

        movers = VGroup(*[Dot(at(q), radius=0.05, color=WHITE) for q in tracks[0]])
        trails = VGroup(*[VMobject(stroke_width=2, stroke_color=WHITE, stroke_opacity=0.6).set_points_as_corners([at(q) for q in tracks[:, i]])
                          for i in range(tracks.shape[1])])
        fl = label(r"follow the arrows, \ noise level falling", font_size=24, color=WHITE).to_corner(DR, buff=0.4)
        self.play(fields[3].animate.set_opacity(0.25), FadeIn(movers), FadeIn(fl))
        self.play(*[MoveAlongPath(m, tr) for m, tr in zip(movers, trails)], *[Create(tr) for tr in trails], run_time=4.0,
                  rate_func=linear)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learning(self):
        """How the denoiser learns: the same noise, sampled at checkpoints during training, beside the loss."""
        import numpy as np

        from videos.ai.ai14.common import curve, move_cloud

        d = load("toytrain")
        checks = [int(c) for c in d["checks"]]
        snaps = np.asarray(d["snaps"])
        L = np.asarray(d["losses"])
        sw = [float(v) for v in d["sw"]]
        S, sh = 0.85, np.array([-3.0, -0.2, 0])
        pts = cloud(np.clip(snaps[0], -3.4, 3.4), DATA, radius=0.022, scale=S, shift=sh, opacity=0.85)
        frame = Rectangle(width=6.0 * S, height=4.4 * S, stroke_color=GREY_D, stroke_width=1.5).move_to(sh)
        ax = CornerAxes(x_range=[0, checks[-1], checks[-1] / 4], y_range=[0, float(L[:, 1].max()) * 1.05, 0.5], x_length=4.8,
                        y_length=2.6, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.7, 0.4, 0])
        yn = label(r"the loss: \ how wrong its noise guesses are", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        xn = label(r"training steps \ ($512$ noisy points each)", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.12)
        t = ValueTracker(0)
        dot = always_redraw(lambda: Dot(ax.c2p(t.get_value(), float(np.interp(t.get_value(), L[:, 0], L[:, 1]))), radius=0.07, color=C.BITS))
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}".replace(",", "{,}"), font_size=28, color=C.BITS)
                            .next_to(frame, UP, buff=0.15))
        swl = always_redraw(lambda: label(rf"distance from the data: \ ${np.interp(t.get_value(), checks, sw):.2f}$", font_size=20,
                                          color=DATA).next_to(frame, DOWN, buff=0.15))
        tag = label(r"$600$ points from the same noise, \\ drawn with $50$ steps at each checkpoint", font_size=18,
                    color=GREY_A).next_to(ax, DOWN, buff=0.9)
        with self.voiceover(
            "How does a denoiser learn this? Here is ours being trained. At each checkpoint, we stop, and use it to "
            "draw six hundred points from the same noise. <bookmark mark='a'/> Untrained, it flings them all over "
            f"the place. <bookmark mark='b'/> Within {checks[1]} steps it already has the rough shape: the loss "
            "plunges in the first hundred steps. <bookmark mark='c'/> The rest of training is refinement. The loss "
            f"barely moves, but the strokes keep sharpening: the distance from the data goes from {sw[1]:.2f} to "
            f"{sw[-1]:.2f}, not smoothly, but on the whole. Each step only ever asked it to guess the noise in one "
            "blurred point; the shape emerges from millions of those guesses."
        ) as vo:
            self.play(Create(frame), FadeIn(pts), Create(ax), FadeIn(yn), FadeIn(xn), FadeIn(tag))
            self.add(dot, cnt, swl)
            vo.wait_until("a")
            marks = {1: "b", 2: "c"}
            for k in range(1, len(checks)):
                if k in marks:
                    vo.wait_until(marks[k])
                seg = [ax.c2p(a, b) for a, b in L if checks[k - 1] <= a <= checks[k]]
                anims = [t.animate.set_value(checks[k]), *move_cloud(pts, np.clip(snaps[k], -3.4, 3.4), scale=S, shift=sh)]
                if len(seg) > 1:
                    anims.append(Create(VMobject(color=C.SURPRISE, stroke_width=3).set_points_as_corners(seg)))
                self.play(*anims, run_time=1.4)
        self.wait(0.3)
        self.remove(dot, cnt, swl)
        self.clear_scene()
