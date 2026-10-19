from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, load
from videos.ai.ai11.compute import VALLEY


class Hook(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.race()
        self.plan()

    # ------------------------------------------------------------------
    def race(self):
        v = load("valley")

        def f(x, y):
            return 0.5 * (VALLEY[0] * x * x + VALLEY[1] * y * y)

        axes = ThreeDAxes(x_range=[-5, 1, 1], y_range=[-1.2, 1.2, 1], z_range=[0, 24, 6], x_length=10.0, y_length=4.0,
                          z_length=3.2, axis_config={"stroke_color": GREY_D, "include_ticks": False, "include_tip": False})
        axes.shift(DOWN * 1.0)
        surf = loss_surface(axes, lambda x, y: min(f(x, y), 24.0), [-5, 1], [-1.2, 1.2], resolution=(60, 30), z_lo=0.0,
                            z_hi=24.0, opacity=0.8)
        bottom = Dot3D(axes.c2p(0, 0, 0) + OUT * 0.05, radius=0.09, color=WHITE)
        runners = {}
        for key, name in (("gd", r"gradient descent"), ("momentum", r"momentum"), ("adam", r"Adam")):
            P = np.asarray(v[key])
            col = {"gd": GREY_A, "momentum": OPT_COLORS["momentum"], "adam": OPT_COLORS["adam"]}[key]
            trail = surface_path(axes, f, P, color=col, lift=0.07, stroke_width=5)
            track = surface_path(axes, f, P, color=col, lift=0.12)
            ball = surface_ball(axes, f, *P[0], color=col, radius=0.12)
            runners[key] = (trail, ball, label(name, font_size=26, color=col), track)
        key = VGroup(*[r[2] for r in runners.values()]).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.5)
        steps = v["steps_to_5pct"]
        tally = VGroup(*[label(rf"${steps[k]}$ steps", font_size=24, color=runners[k][2].get_color())
                         .next_to(runners[k][2], DOWN, buff=0.12) for k in runners])
        tag = label(r"a narrow valley: \ curvature $1$ one way, \ $30$ the other \ (illustrative)", font_size=22,
                    color=GREY_B).to_edge(DOWN, buff=0.3)
        for m in (key, tally, tag):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-150 * DEGREES, zoom=0.78)  # from behind the walkers
        with self.voiceover(
            "Every model in this series is trained by walking downhill. But how you walk matters enormously. "
            "<bookmark mark='a'/> Here's part four's narrow valley again, and three walkers starting from the same "
            "place. <bookmark mark='b'/> Plain gradient descent zigzags across the valley. Momentum builds up speed "
            "along it. Adam rescales each direction separately, and heads almost straight for the bottom."
        ) as vo:
            self.play(FadeIn(surf), FadeIn(bottom), FadeIn(tag), run_time=1.5)
            self.begin_ambient_camera_rotation(rate=0.09)  # swinging round to the side as they go
            vo.wait_until("a")
            self.play(FadeIn(key), *[FadeIn(r[1]) for r in runners.values()])
            vo.wait_until("b")
            self.play(*[Create(r[0]) for r in runners.values()],
                      *[MoveAlongPath(r[1], r[3]) for r in runners.values()], run_time=5.5, rate_func=linear)
            self.stop_ambient_camera_rotation()
            self.move_camera(phi=0, theta=-90 * DEGREES, zoom=0.95, run_time=2.0)  # look straight down: the paths
            self.play(FadeIn(tally))
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 11: \ Going Downhill", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"noise, \ the edge of stability, \ Adam, \ Muon, \ schedules", font_size=30, color=C.BITS)
        sub.next_to(title, DOWN, buff=0.25)
        smap = series_map(current=11, done=10).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "This part is about the optimizers that train real models: why the noise of small batches helps, why "
            "training lives at the edge of instability, how Adam and the newer Muon reshape each step, <bookmark mark='a'/> "
            "and how the learning rate should change over a training run."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
