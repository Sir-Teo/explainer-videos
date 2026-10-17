from __future__ import annotations

import math

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
        TW, TH = 2.7, 1.4

        def frame(caption, color):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 0.65, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            return box, label(caption, font_size=20, color=color).move_to(box.get_bottom() + UP * 0.25)

        out = []
        v = load("vit")
        im = gray_image(np.asarray(v["ex_imgs"])[0], 1.3)
        out.append((Group(im, patch_grid(im, 5)), r"patches as tokens", PATCH))
        out.append((Group(*[heat_image(a, 0.8) for a in np.asarray(v["cls_att"])]).arrange(RIGHT, buff=0.06), r"where it looks", C.ATTN))
        sim = np.asarray(v["pos_sim"])
        out.append((Group(*[heat_image(sim[i].reshape(5, 5), 0.26, color=C.TRUE_P, gamma=1.0) for i in range(25)])
                    .arrange_in_grid(rows=5, cols=5, buff=0.02), r"positions learn the grid", C.TRUE_P))
        lt = load("latent")
        out.append((Group(*[Group(gray_image(o, 0.45), gray_image(r, 0.45)).arrange(DOWN, buff=0.04)
                            for o, r in zip(np.asarray(lt["orig"])[:5], np.asarray(lt["rec"])[:5])]).arrange(RIGHT, buff=0.06),
                    r"$400 \to 16$ numbers", C.EMBED))
        va = load("vae")
        tags = [f"{float(b):g}" for b in va["betas"]]
        best = max(tags, key=lambda t: float(va[f"clear_{t}"]))
        out.append((Group(*[gray_image(x, 0.45) for x in np.asarray(va[f"samples_{best}"])[:10]]).arrange_in_grid(rows=2, cols=5, buff=0.05),
                    r"rebuild or generate: \ $\beta$", C.SURPRISE))
        d = load("dit")
        out.append((Group(*[gray_image(x, 0.36) for x in np.asarray(d["alphabet"])[:14]]).arrange_in_grid(rows=2, cols=7, buff=0.04),
                    r"adaLN-Zero transformer", PATCH))
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1.8, 1], x_length=TW * 0.85, y_length=TH * 0.85, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        lnd = ax.plot(lambda t: math.exp(-math.log(t / (1 - t)) ** 2 / 2) / (math.sqrt(2 * math.pi) * t * (1 - t)),
                      x_range=[0.01, 0.99, 0.01], color=C.SURPRISE, stroke_width=3)
        out.append((VGroup(ax, lnd), r"logit-normal $t$, \ shifted", C.SURPRISE))
        vr = load("var")
        out.append((Group(*[gray_image(p, 0.4) for p in np.asarray(vr["example"])]).arrange(RIGHT, buff=0.04), r"coarse to fine", PATCH))
        v3 = load("vae3d")
        out.append((Group(*[gray_image(f_, 0.42) for f_ in np.asarray(v3["rec"])[0][::2]]).arrange(RIGHT, buff=0.04),
                    r"a causal video autoencoder", PATCH))
        vid = VGroup(*[Rectangle(width=1.2, height=0.7, stroke_color=GREY_B, stroke_width=1.2, fill_color="#121722", fill_opacity=1)
                       .shift(RIGHT * 0.14 * i + UP * 0.1 * i) for i in range(6)])
        out.append((vid, r"rotations in $f, h, w$", GREY_A))
        cl = load("clips")
        out.append((Group(*[gray_image(f_, 0.4) for f_ in np.asarray(cl["joint_clips"])[0][1:7]]).arrange(RIGHT, buff=0.04),
                    r"frames that agree", C.INTERVAL))
        out.append((Group(*[gray_image(f_, 0.4) for f_ in np.asarray(cl["forcing_rollout"])[0][::5][:6]]).arrange(RIGHT, buff=0.04),
                    r"diffusion forcing", C.INTERVAL))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = frame(cap, col)
            pic.move_to(box.get_center() + UP * 0.2)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=3, cols=4, buff=(0.2, 0.2)).move_to(DOWN * 0.35)
        return tiles

    def recap(self):
        tiles = self.tiles()
        cl = load("clips")
        held = float(cl["forcing_late_right"]) > float(cl["teacher_late_right"]) + 0.05  # did noisy pasts pay off here?
        head = label(r"Part 15, in twelve pictures", font_size=36).to_edge(UP, buff=0.25)
        with self.voiceover(
            "Let's take stock. Cut a picture into patches and a transformer reads it like a sentence, learning the "
            "grid by itself. Squeeze pictures into a few numbers, and diffusion gets cheaper, as long as the space "
            "is shaped for generating, not just for rebuilding. Make the denoiser a transformer that starts as the "
            "identity, train it most on the middle noise levels, shift them as pictures grow, and give text and "
            "picture one sequence: that's today's image models. Coarse to fine is another road entirely. Video is "
            "the same with time: a causal autoencoder, rotations in three directions, frames drawn together, and "
            + ("noisy pasts in training, so a model can roll forward on its own work." if held else
               "noisy pasts in training, meant to let a model roll forward on its own work.")
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
            r"D.~P.~Kingma \& M.~Welling, \textit{VAE} (2013); \ J.~Yao et al., \textit{VA-VAE} (2025)",
            r"B.~Chen et al., \textit{Diffusion Forcing} (2024); \ X.~Huang et al., \textit{Self Forcing} (2025)",
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
