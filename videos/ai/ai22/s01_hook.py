from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import HIST, LETTERS, PART, PATCH, fmt_int, gray_image, load, patch_grid


class Hook(VoiceoverScene):
    def construct(self):
        self.letters()
        self.history()
        self.plan()

    # ------------------------------------------------------------------
    def letters(self):
        d = load("showcase")
        path = np.asarray(d["alphabet_path"])  # frames of the denoising, for each letter of the alphabet
        word = "PICTURES"
        idx = [LETTERS.index(c) for c in word]

        def row(k):
            return Group(*[gray_image(path[k][i], 1.5) for i in idx]).arrange(RIGHT, buff=0.14).move_to(UP * 0.2)

        pics = row(0)
        asked = VGroup(*[Text(c, font="DejaVu Sans Mono", font_size=24, color=PATCH).next_to(p, UP, buff=0.12)
                         for c, p in zip(word, pics)])
        al = label(r"asked for:", font_size=20, color=GREY_B).next_to(asked, UP, buff=0.2).align_to(pics, LEFT)
        grids = VGroup(*[patch_grid(p, 5, stroke_width=1) for p in pics])
        tag = note(r"each letter drawn from noise by a small transformer trained here, \ in $40$ steps").to_edge(DOWN, buff=0.35)
        n_par = int(d["params"])
        tl = label(rf"${fmt_int(n_par)}$ weights, \ ${fmt_int(d['steps'])}$ training steps, \ one CPU core",
                   font_size=22, color=GREY_A).next_to(pics, DOWN, buff=0.45)
        with self.voiceover(
            "Every letter here was drawn from pure noise by a small transformer we trained on this computer, asked "
            "for that letter. <bookmark mark='a'/> It sees each picture as a sequence of patches, the way a language "
            "model sees words, and it was trained by the flow matching of Part 21. <bookmark mark='b'/> The same "
            "recipe, a hundred thousand times larger, draws photographs, films, and whole scenes you can walk through."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p, scale=0.8) for p in pics], lag_ratio=0.12), FadeIn(asked), FadeIn(al),
                      FadeIn(tag), run_time=1.4)
            for k in range(1, len(path)):  # noise, then shapes, then letters
                self.play(Transform(pics, row(k)), run_time=0.4, rate_func=linear)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(g_) for g_ in grids], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(tl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        head = label(r"How we got here", font_size=40).to_edge(UP, buff=0.35)
        cards = [
            history_card(2012, r"AlexNet", r"a convolutional network wins ImageNet \ (Part 10)", color=HIST, width=4.3, font_size=24),
            history_card(2014, r"GANs", r"a generator against a judge \ (Part 20)", color=HIST, width=4.3, font_size=24),
            history_card(2020, r"the vision transformer", r"an image is a sequence of patches", color=HIST, width=4.3, font_size=24),
            history_card(2021, r"DALL$\cdot$E; \ diffusion beats GANs", r"text to image as tokens; \ denoising wins on quality",
                         color=HIST, width=4.3, font_size=24),
            history_card(2022, r"DALL$\cdot$E 2, \ Imagen, \ Stable Diffusion", r"diffusion from text; \ open weights",
                         color=HIST, width=4.3, font_size=24),
            history_card(2024, r"SD3, \ FLUX.1, \ Sora", r"flow-matching transformers; \ video as spacetime patches",
                         color=HIST, width=4.3, font_size=24),
            history_card(2025, r"Veo 3, \ BAGEL, \ Self Forcing", r"sound with the video; \ one model reads and draws; "
                         r"\ real-time video", color=HIST, width=4.3, font_size=24),
            history_card(2026, r"open audio--video models", r"LTX-2: \ sound and picture, \ open weights", color=HIST, width=4.3, font_size=24),
        ]
        grid = VGroup(*cards).arrange_in_grid(rows=3, cols=3, buff=(0.22, 0.3), cell_alignment=UP)
        if grid.width > 13.4:
            grid.width = 13.4
        if grid.height > 6.3:
            grid.height = 6.3
        grid.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "How we got here. In 2012 a convolutional network, AlexNet, won the ImageNet contest by a wide margin, "
            "and Part 10 told that story. <bookmark mark='a'/> In 2014 came GANs, a generator trained against a judge, "
            "Part 20's story. <bookmark mark='b'/> In 2020 a plain transformer read images as sequences of patches. "
            "<bookmark mark='c'/> In 2021 DALL-E drew pictures from text, as tokens, and diffusion beat GANs on "
            "quality. <bookmark mark='d'/> 2022 brought DALL-E 2, Imagen, and Stable Diffusion, with open weights. "
            "<bookmark mark='e'/> By 2024 flow-matching transformers drew pictures, and Sora drew video. "
            "<bookmark mark='f'/> In 2025 video came with sound, one model could both read and draw, and video "
            "could be generated as fast as it plays. <bookmark mark='g'/> And in 2026, open models make sound and "
            "picture together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.1))
            for k, m in enumerate("abcdefg"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.1), run_time=0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Images, Video and 3D", font_size=48).to_edge(UP, buff=0.35)
        obj = objectives_card([
            r"how a transformer reads a picture, \ and when convolutions still win",
            r"the compressed spaces models draw in, \ and borrowing a vision model's eyes",
            r"the denoiser: \ U-Net or transformer, \ and how the condition goes in",
            r"from text to image: \ Stable Diffusion 3, \ Flux, \ the resolution shift",
            r"pictures as tokens: \ MaskGIT, \ next-scale prediction, \ one model for words and pictures",
            r"video: \ squeezing time, \ frames that agree, \ rolling forward",
            r"3D: \ the volume-rendering integral, \ Gaussian splatting",
        ], title=r"In this part", font_size=30, width=12.6)
        obj.rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        obj.head.next_to(obj.rows, UP, buff=0.5).set_x(0)
        obj.next_to(title, DOWN, buff=0.3)
        if obj.height > 6.2:
            obj.height = 6.2
            obj.next_to(title, DOWN, buff=0.3)
        with self.voiceover(
            "This is Part 22 of AI, Built: images, video and 3D. <bookmark mark='a'/> First, how a transformer reads "
            "a picture, and when convolutions still win. <bookmark mark='b'/> Then the compressed spaces models "
            "draw in, and how borrowing a vision model's eyes speeds up training. <bookmark mark='c'/> The denoiser "
            "itself, and how the request gets in. <bookmark mark='d'/> Text to image, from DALL-E to Flux. "
            "<bookmark mark='e'/> Pictures written as tokens, and one model for words and pictures. "
            "<bookmark mark='f'/> Video. <bookmark mark='g'/> And 3D. <bookmark mark='h'/> Every model in this part "
            "is trained here, on letters, clips and a small scene, and we'll watch each one learn."
        ) as vo:
            self.play(FadeIn(title), FadeIn(obj.head))
            for k, m in enumerate("abcdefg"):
                vo.wait_until(m)
                self.play(FadeIn(obj.rows[k], shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until("h")
            self.play(Indicate(title, color=PATCH, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()
