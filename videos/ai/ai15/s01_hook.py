from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import LETTERS, PATCH, gray_image, load, patch_grid


class Hook(VoiceoverScene):
    def construct(self):
        self.letters()
        self.plan()

    # ------------------------------------------------------------------
    def letters(self):
        d = load("dit")
        path = np.asarray(d["alphabet_path"])  # frames of the denoising, for each letter of the alphabet
        word = "PICTURES"
        idx = [LETTERS.index(c) for c in word]

        def row(k):
            return Group(*[gray_image(path[k][i], 1.35) for i in idx]).arrange(RIGHT, buff=0.12).move_to(UP * 0.3)

        pics = row(0)
        grids = VGroup(*[patch_grid(p, 5, stroke_width=1) for p in pics])
        tag = note(r"each letter drawn from noise by a small transformer trained here, \ asked for that letter").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Every letter here was drawn from pure noise by a small transformer we trained, asked for that letter. "
            "<bookmark mark='a'/> It sees each picture as a sequence of patches, just as a language model sees "
            "words."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p, scale=0.8) for p in pics], lag_ratio=0.15), FadeIn(tag), run_time=1.2)
            for k in range(1, len(path)):  # noise, then shapes, then letters
                self.play(Transform(pics, row(k)), run_time=0.35, rate_func=linear)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(g_) for g_ in grids], lag_ratio=0.1), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 15: \ Images and Video", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"patches as tokens, \ latent spaces, \ diffusion transformers, \ video, \ coarse to fine",
                    font_size=28, color=C.BITS).next_to(title, DOWN, buff=0.25)
        smap = series_map(current=15, done=14).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "This part brings everything so far to pictures and video: how a transformer reads an image, why models "
            "work in a compressed space, how a transformer becomes the denoiser, <bookmark mark='a'/> and what "
            "changes for video."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
