from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import DATA, NOISE, cloud, gray_image, load, move_cloud


class Hook(VoiceoverScene):
    def construct(self):
        self.reverse()
        self.plan()

    # ------------------------------------------------------------------
    def reverse(self):
        t = load("toy")
        P = np.asarray(t["ddpm_path"])
        S = 1.1
        d = cloud(P[0], NOISE, radius=0.035, scale=S, shift=np.array([0, -0.3]))
        tag = note(r"a network trained here, \ walking $300$ points from noise; \ computed").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Noise. A cloud of random points. <bookmark mark='a'/> Now a network, trained on this computer, nudges "
            "each point a little, again and again. <bookmark mark='b'/> In part four we did this with the exact "
            "answer written in. This time, the network had to learn it from examples."
        ) as vo:
            self.play(FadeIn(d), FadeIn(tag))
            vo.wait_until("a")
            for k in range(1, len(P)):
                self.play(*move_cloud(d, P[k], S, np.array([0, -0.3])),
                          *([d.animate.set_color(DATA)] if k == len(P) - 1 else []), run_time=0.22, rate_func=linear)
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 14: \ Diffusion and Flow", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"denoising, \ DDPM and DDIM, \ flow matching, \ guidance, \ text by unmasking", font_size=28,
                    color=C.BITS).next_to(title, DOWN, buff=0.25)
        smap = series_map(current=14, done=13).scale(0.85).move_to(DOWN * 0.9)
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
