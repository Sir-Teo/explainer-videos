from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import AUSTEN, DICKENS, HIDDEN, load, mix


class Hook(VoiceoverScene):
    def construct(self):
        self.unlabelled()
        self.plan()

    # ------------------------------------------------------------------
    def unlabelled(self):
        p = load("pca")
        g = load("gmm")
        xyz = np.asarray(p["proj"])[:, :3] / 3.2
        y = np.asarray(p["y"])
        r = np.asarray(g["r"])[-1]
        # which mixture component is Dickens's?
        flip = ((r > 0.5) == y).mean() < 0.5
        r = 1 - r if flip else r
        cloud = Cloud3D(xyz, [GREY_B] * len(y), scale=1.7, radius=0.045, tilt=0.4, center=[-0.6, -0.2, 0])
        head = label(r"$639$ pages, \ $70$ numbers each \ (Part 6) \ --- \ no authors given", font_size=30)
        head.to_edge(UP, buff=0.4)
        found = label(rf"two hidden groups, found from the data alone: \ ${100 * g['agree']:.0f}\%$ match the authors",
                      font_size=30, color=WHITE).to_edge(DOWN, buff=0.45)
        key = VGroup(label(r"Austen", font_size=26, color=AUSTEN), label(r"Dickens", font_size=26, color=DICKENS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.5).shift(DOWN * 0.7)
        q = label(r"?", font_size=80, color=HIDDEN).move_to([4.6, 0.4, 0])
        with self.voiceover(
            "Here are part six's six hundred and thirty-nine pages again, each a point in seventy dimensions, seen "
            "along the three directions in which they vary most. But this time, nobody tells us who wrote which. "
            "<bookmark mark='a'/> Can the data reveal its own hidden structure? <bookmark mark='b'/> A model that "
            "assumes there are two hidden sources, and fits them with no labels at all, finds two groups. "
            f"<bookmark mark='c'/> And they're the two authors: {100 * g['agree']:.0f} percent of the pages land with "
            "the right one."
        ) as vo:
            self.play(FadeIn(cloud), FadeIn(head), run_time=1.5)
            self.play(cloud.angle.animate.set_value(1.2), run_time=6.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(q, scale=0.6), cloud.angle.animate.set_value(1.8), run_time=2.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeOut(q), cloud.angle.animate.set_value(2.6),
                      *[d.animate.set_color(mix(AUSTEN, DICKENS, r[i])) for i, d in enumerate(cloud.dots)],
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(found), FadeIn(key), cloud.angle.animate.set_value(2.6 + math.pi / 4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 7: \ Statistical ML", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"models with hidden parts", font_size=32, color=HIDDEN).next_to(title, DOWN, buff=0.25)
        smap = series_map(current=7, done=6).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "This part is about models with hidden parts: directions, sources, states and functions that we never "
            "observe, only infer. <bookmark mark='a'/> Principal components, mixtures, hidden Markov models, "
            "Gaussian processes, and variational inference, plus a new row for the scoreboard."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
