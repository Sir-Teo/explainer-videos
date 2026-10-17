from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import LETTERS, PATCH, gray_image, heat_image, load, patch_grid


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def frame(caption, color):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            return box, label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)

        out = []
        v = load("vit")
        im = gray_image(np.asarray(v["ex_imgs"])[0], 1.8)
        out.append((Group(im, patch_grid(im, 5)), r"patches as tokens", PATCH))
        out.append((Group(*[heat_image(a, 0.85) for a in np.asarray(v["cls_att"])]).arrange(RIGHT, buff=0.06), r"where it looks", C.ATTN))
        sim = np.asarray(v["pos_sim"])
        out.append((Group(*[heat_image(sim[i].reshape(5, 5), 0.34, color=C.TRUE_P, gamma=1.0) for i in range(25)])
                    .arrange_in_grid(rows=5, cols=5, buff=0.03), r"positions learn the grid", C.TRUE_P))
        lt = load("latent")
        out.append((Group(*[Group(gray_image(o, 0.5), gray_image(r, 0.5)).arrange(DOWN, buff=0.04)
                            for o, r in zip(np.asarray(lt["orig"])[:5], np.asarray(lt["rec"])[:5])]).arrange(RIGHT, buff=0.06),
                    r"$400 \to 16$ numbers", C.EMBED))
        out.append((Group(*[gray_image(x, 0.5) for x in np.asarray(lt["samples"])[:10]]).arrange_in_grid(rows=2, cols=5, buff=0.05),
                    r"latent diffusion", C.EMBED))
        d = load("dit")
        out.append((Group(*[gray_image(x, 0.42) for x in np.asarray(d["alphabet"])[:14]]).arrange_in_grid(rows=2, cols=7, buff=0.04),
                    r"a diffusion transformer", PATCH))
        vid = VGroup(*[Rectangle(width=1.4, height=0.8, stroke_color=GREY_B, stroke_width=1.2, fill_color="#121722", fill_opacity=1)
                       .shift(RIGHT * 0.16 * i + UP * 0.12 * i) for i in range(6)])
        out.append((vid, r"space and time", GREY_A))
        s = load("scales")
        out.append((Group(*[gray_image(p, 0.45) for p in np.asarray(s["pyramid"])]).arrange(RIGHT, buff=0.05), r"coarse to fine", PATCH))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = frame(cap, col)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(r"Part 15, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Cut a picture into patches and a transformer reads it like a sentence, learning the "
            "grid by itself. Squeeze pictures into a few numbers, and diffusion gets cheaper and cares about shapes. "
            "Make the denoiser a transformer, feed it the noise level and the request through its normalizations, "
            "and it draws what it's asked for; give text and picture one sequence, and you have today's image "
            "models. Video is the same with time, at a far higher token count; and coarse to fine is another road "
            "entirely."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"pictures and sound as tokens for one model", [16]),
            (r"world models that predict the next frame", [18]),
            (r"serving huge models fast", [19]),
        ], font_size=26)
        with self.voiceover(
            "Next, every sense becomes a token for one model, in part sixteen. World models in part eighteen "
            "predict the next frame of video, and part nineteen is about running all of this fast."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 16, \ Every Sense Is a Token", font_size=40).to_edge(UP, buff=0.4)
        rows = VGroup(*[VGroup(label(n, font_size=26, color=c_),
                               VGroup(*[Square(0.3, stroke_color=c_, stroke_width=1.5, fill_color=c_, fill_opacity=0.2)
                                        for _ in range(8)]).arrange(RIGHT, buff=0.05)).arrange(RIGHT, buff=0.4)
                        for n, c_ in ((r"text", C.TRUE_P), (r"pictures", PATCH), (r"sound", C.INTERVAL))])
        rows.arrange(DOWN, aligned_edge=RIGHT, buff=0.35).move_to(DOWN * 0.2)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Next time: how text, pictures and sound all become tokens, <bookmark mark='a'/> so one model can read, "
            "see, listen and speak, including the voice you're hearing now."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), chapters 10, 12 and 18"]
        papers = [
            r"A.~Dosovitskiy et al., \textit{An Image Is Worth 16x16 Words} (2020)",
            r"R.~Rombach et al., \textit{High-Resolution Image Synthesis with Latent Diffusion Models} (2022)",
            r"W.~Peebles \& S.~Xie, \textit{Scalable Diffusion Models with Transformers} (2023)",
            r"P.~Esser et al., \textit{Scaling Rectified Flow Transformers for High-Resolution Image Synthesis} (2024)",
            r"K.~Tian et al., \textit{Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction} (2024)",
        ]
        card = reference_card(books, papers)
        data = note(r"Letters drawn from the system's fonts; \ every model here is trained on this video's CPU; \ model "
                    r"sizes as published.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "The DiT paper is short and clear. Thanks for watching, and see you in part sixteen."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
