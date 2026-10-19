from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import DATA, NOISE, cloud, load


class Hook(VoiceoverScene):
    def construct(self):
        self.reverse()
        self.plan()

    # ------------------------------------------------------------------
    def reverse(self):
        t = load("toy")
        P = np.asarray(t["ddim_path"])[::2]  # the deterministic sampler: each point's path is a smooth curve
        S = 1.35
        d = cloud(P[0], NOISE, radius=0.035, scale=S, shift=np.array([0, -0.3]))
        tag = note(r"a network trained here, \ walking $300$ points from noise; \ computed").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Noise. A cloud of random points. <bookmark mark='a'/> Now a network, trained on this computer, nudges "
            "each point a little, again and again. <bookmark mark='b'/> In part five we did this with the exact "
            "answer written in. This time, the network had to learn it from examples."
        ) as vo:
            self.play(FadeIn(d), FadeIn(tag))
            vo.wait_until("a")
            sh = np.array([0, -0.3])
            for k in range(1, len(P)):  # each point walks, and warms from the noise colour to the data colour
                col = interpolate_color(ManimColor(NOISE), ManimColor(DATA), k / (len(P) - 1))
                self.play(*[dot.animate.move_to([p_[0] * S + sh[0], p_[1] * S + sh[1], 0]).set_color(col)
                            for dot, p_ in zip(d, P[k])], run_time=0.2, rate_func=linear)
            vo.wait_until("b")
            # the paths a few points took: noise on one end, the data on the other
            idx = np.linspace(0, P.shape[1] - 1, 16).astype(int)
            def path(i):  # short segments warming from the noise colour to the data colour along the way
                Q = [[P[k][i][0] * S + sh[0], P[k][i][1] * S + sh[1], 0] for k in range(len(P))]
                return VGroup(*[Line(Q[k], Q[k + 1], stroke_width=1.8, stroke_opacity=0.75,
                                     color=interpolate_color(ManimColor(NOISE), ManimColor(DATA), k / (len(Q) - 2)))
                                for k in range(len(Q) - 1)])

            paths = VGroup(*[path(i) for i in idx])
            self.play(LaggedStart(*[Create(pa) for pa in paths], lag_ratio=0.08), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 21: \ Diffusion and Flow", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"denoising, \ DDPM and DDIM, \ flow matching, \ guidance, \ text by unmasking", font_size=28,
                    color=C.BITS).next_to(title, DOWN, buff=0.25)
        smap = series_map(current=21, done=20).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "This part is about how image, video and now even text models make things from noise: what the network "
            "learns, how to walk back, why straight paths are faster, how to ask for something specific, "
            "<bookmark mark='a'/> and how to do it for words."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
