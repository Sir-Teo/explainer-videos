from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import (CFG_C, GEN_C, GS_C, LAT_C, NERF_C, PART, PATCH, TXT, VID_C, glyph_sheet, gray_image,
                                   heat_image, load, node_box, rgb_image)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0
        out = []
        v = load("vit")
        sim = np.asarray(v["pos_sim"])
        row = np.clip(sim[12].reshape(5, 5), 0, None)
        row[2, 2] = 0
        out.append((heat_image(row, 1.7, color=C.TRUE_P), r"a ViT learns the grid", C.TRUE_P))
        lt = load("latents")
        cfgs = [tuple(int(x) for x in c) for c in lt["configs"]]
        ax = Axes(x_range=[4, 7, 1], y_range=[0, 0.3, 0.1], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        dots = VGroup(*[Dot(ax.c2p(math.log2(c[0] * c[0] * c[1]), float(lt[f"g{c[0]}c{c[1]}_rmse"])), radius=0.06, color=LAT_C)
                        for c in cfgs])
        out.append((VGroup(ax, dots), r"how small a space", LAT_C))
        d = load("denoisers")
        ev = np.asarray(d["eval_at"], float)
        ax2 = Axes(x_range=[0, ev[-1], ev[-1] / 2], y_range=[0, float(np.asarray(d["zero_fd"]).max()) * 1.1, 1e9],
                   x_length=TW * 0.9, y_length=TH * 0.85, tips=False, axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out.append((VGroup(ax2, curve(ax2, ev, np.asarray(d["zero_fd"]).mean(0), CFG_C["zero"], 3),
                           curve(ax2, ev, np.asarray(d["repa_fd"]).mean(0), CFG_C["repa"], 3)), r"REPA: \ borrowed eyes",
                    CFG_C["repa"]))
        out.append((glyph_sheet(np.asarray(d["alphabet"])[:26], 2, 13, size=0.2, gap=0.02, frame=False),
                    r"a DiT with adaLN-Zero", CFG_C["zero"]))
        s = load("shift")
        sg = np.asarray(s["sigmas"], float)
        ax3 = Axes(x_range=[0.3, 1, 0.35], y_range=[0, 1, 0.5], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out.append((VGroup(ax3, *[curve(ax3, sg, np.asarray(s[f"pshift_{n}"]), c_, 3) for n, c_ in
                                  ((20, GREY_B), (40, C.TRUE_P), (80, C.BITS))]), r"the resolution shift", C.BITS))
        tk = load("tokens")
        out.append((Group(*[gray_image(im, 0.55) for im in np.asarray(tk["var_trace"])[:, 0]]).arrange(RIGHT, buff=0.04),
                    r"VAR: \ coarse to fine", GEN_C["var"]))
        cl = load("clips")
        L_ = int(cl["long"])
        fr = np.arange(2, L_)
        top = max(float(np.asarray(cl[f"{m}_pos"])[:, 2:].mean(0).max()) for m in ("teacher", "forcing"))
        ax4 = Axes(x_range=[0, L_, 8], y_range=[0, top * 1.1, 1e9], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out.append((VGroup(ax4, *[curve(ax4, fr, np.asarray(cl[f"{m}_pos"])[:, 2:].mean(0), VID_C[m], 3)
                                  for m in ("teacher", "forcing")]), r"rolling forward", VID_C["forcing"]))
        n_, sp = load("nerf"), load("splat")
        out.append((Group(rgb_image(np.asarray(n_["replay_views"])[-1], 1.5), rgb_image(np.asarray(sp["replay_views"])[-1], 1.5))
                    .arrange(RIGHT, buff=0.1), r"NeRF and Gaussians", NERF_C))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
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
        head = label(rf"Part {PART}, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. A picture is a sequence of patches, and a transformer reads it, learning even the "
            "grid it came from. Models draw in a compressed space, and how small and how meaningful that space is "
            "shapes everything; borrowing a vision model's eyes speeds up learning to draw. The denoiser became a "
            "transformer, told what to draw through gated normalizations. Bigger pictures need their noise shifted, "
            "by a factor we derived and checked. Pictures can also be written as tokens, best coarse to fine, which "
            "lets one model read, draw and edit. Video is the same in time: frames drawn together agree, and frames "
            "drawn one by one can roll forward. And 3D is light added up along rays, or Gaussians splatted onto the "
            "screen."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"patches, \ encoders, \ CLIP and SigLIP, \ vision-language models", [23]),
            (r"self-supervised encoders: \ DINO, \ the eyes REPA borrows", [24]),
            (r"diffusion over 3D structure: \ AlphaFold 3", [25]),
            (r"video that responds to actions: \ world models", [29]),
            (r"telling real from generated", [31]),
        ], font_size=26)
        with self.voiceover(
            "All of this comes back. The image encoders, and the CLIP and SigLIP models that tie pictures to words, "
            "are Part 23, where every sense becomes a token. The self-supervised encoders whose eyes REPA borrows are "
            "Part 24. Diffusion over 3D structure returns in AlphaFold 3, Part 25. Video that responds to a player's "
            "actions is a world model, Part 29. And telling real pictures from generated ones is part of the last "
            "part, on trust."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"A ViT cuts a $224 \times 224$ picture into $p \times p$ patches. \ How many tokens for $p = 16$ and "
            r"$p = 8$? \ By what factors do attention's and the MLPs' costs grow when $p$ halves?",
            r"In an adaLN-Zero block with every gate $\alpha = 0$, show the block is the identity and the gradients of "
            r"its attention weights vanish, \ but the gradient of the gate's map $W$ does not.",
            r"Derive the resolution shift $\sigma_m = \alpha \sigma_n / (1 + (\alpha - 1)\sigma_n)$ from equal uncertainty "
            r"about a flat picture, \ show it lowers the log signal-to-noise ratio by $2 \log \alpha$, \ and evaluate "
            r"it for $\sigma_n = 0.5$, $\alpha = 3$.",
            r"MaskGIT draws $256$ tokens in $T = 8$ passes, \ leaving $\lfloor 256 \cos(\tfrac{\pi}{2} \tfrac{k}{T}) \rfloor$ "
            r"masked after pass $k$. \ How many are fixed in each pass? \ Compare a linear schedule.",
            r"For density $\sigma$ and colour $\mathbf c$ constant on $[t_i, t_i + \delta]$, show "
            r"$\int T\sigma\mathbf c\,dt = T_i (1 - e^{-\sigma\delta})\mathbf c$, \ and that the weights $T_i \alpha_i$ "
            r"sum to $1 - T_{N+1}$.",
            r"Compute the Jacobian of $(u, v) = (f x / z, f y / z)$, \ and the projected covariance of an isotropic "
            r"Gaussian $s^2 I$ centred on the optical axis at depth $z$.",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems, from counting a vision transformer's tokens to projecting a Gaussian. Pause "
            "here, and work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 23, \ Every Sense Is a Token", font_size=40).to_edge(UP, buff=0.5)
        rows = VGroup()
        for name, col in ((r"text", TXT), (r"pictures", PATCH), (r"sound", C.INTERVAL)):
            toks = VGroup(*[Square(0.32, stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=0.25) for _ in range(6)]
                          ).arrange(RIGHT, buff=0.05)
            rows.add(VGroup(label(name, font_size=24, color=col), toks).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, buff=0.35, aligned_edge=RIGHT).move_to([-3.0, -0.3, 0])
        one = node_box(r"one transformer", WHITE, font_size=28).move_to([3.4, -0.3, 0])
        arrs = VGroup(*[Arrow(r_.get_right(), one.get_left(), buff=0.15, color=GREY_B, stroke_width=2.5) for r_ in rows])
        topics = label(r"byte-pair encoding, \ codebooks, \ audio codecs, \ speech recognition, \ CLIP, \ "
                       r"vision-language models", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Next time: every sense as a token. How text is cut into tokens, how sound becomes tokens too, how "
            "CLIP ties pictures to words, and how one transformer reads them all: Part 23."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3), FadeIn(one),
                      LaggedStart(*[GrowArrow(a_) for a_ in arrs], lag_ratio=0.3), FadeIn(topics),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), \ ch.~12 and 18",
             r"R.~Szeliski, \textit{Computer Vision: Algorithms and Applications}, 2nd ed.\ (2022)",
             r"K.~P.~Murphy, \textit{Probabilistic Machine Learning: Advanced Topics} (2023), \ ch.~20--25"],
            [r"Krizhevsky, Sutskever \& Hinton (2012); \ Dosovitskiy et al., ViT (2020); \ Touvron et al., DeiT (2021); "
             r"\ Liu et al., ConvNeXt (2022)",
             r"Rombach et al., Latent Diffusion (2022); \ Chen et al., DC-AE (2024); \ Yu et al., REPA (2024); \ Yao et "
             r"al., VA-VAE (2025); \ Leng et al., REPA-E (2025); \ Zheng et al., RAE (2025)",
             r"Ronneberger et al., U-Net (2015); \ Dhariwal \& Nichol (2021); \ Peebles \& Xie, DiT (2023); \ Esser "
             r"et al., SD3 (2024); \ Black Forest Labs, FLUX.1, Kontext, FLUX.2 (2024--25)",
             r"Ramesh et al., DALL$\cdot$E (2021), DALL$\cdot$E 2 (2022); \ Saharia et al., Imagen (2022); \ Yu et al., "
             r"Parti (2022); \ Betker et al., DALL$\cdot$E 3 (2023); \ Brooks et al., InstructPix2Pix (2022)",
             r"Esser et al., VQGAN (2020); \ Chang et al., MaskGIT (2022); \ Tian et al., VAR (2024); \ Li et al., MAR "
             r"(2024); \ Han et al., Infinity (2024)",
             r"Chameleon Team (2024); \ Zhou et al., Transfusion (2024); \ Wu et al., Janus (2024); \ Deng et al., "
             r"BAGEL (2025)",
             r"OpenAI, Sora (2024); \ Meta, Movie Gen (2024); \ Kong et al., HunyuanVideo (2024); \ Wan Team (2025); \ "
             r"Lightricks, LTX-2 (2026); \ Chen et al., Diffusion Forcing (2024); \ Yin et al., CausVid (2024); \ "
             r"Huang et al., Self Forcing (2025)",
             r"Mildenhall et al., NeRF (2020); \ Tancik et al.\ (2020); \ M\"uller et al., Instant-NGP (2022); \ "
             r"Zwicker et al., EWA (2001); \ Kerbl et al., 3D Gaussian Splatting (2023); \ Wang et al., VGGT (2025)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Simon Prince's Understanding Deep Learning is a good next step for the image models, and Richard "
            "Szeliski's Computer Vision for the 3D. Thanks for watching, and see you in Part 23."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
