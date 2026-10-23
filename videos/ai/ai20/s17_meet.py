from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (AR, DATA, EBM, FAM, FLOW, GAN_C, HIST, PART, SCORE_C, VAE_C, VQ_C, digit_sheet,
                                   load, node_box)

DIFF = "#7FD3FF"  # diffusion, the next part


class Meet(VoiceoverScene):
    def construct(self):
        self.card()
        self.turn()
        self.tokens()
        self.ours()
        self.scales()
        self.distill()
        self.tree()

    def card(self):
        card = chapter_card(16, r"Where the families meet", r"What happened to the four answers?", lit=(2015,),
                            part=PART)
        with self.voiceover("Chapter sixteen. Where the families meet."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def turn(self):
        rows_ = [(r"BigGAN-deep", GAN_C, 6.95, 0.87, 0.28), (r"ADM (diffusion)", DIFF, 10.94, 0.69, 0.63),
                 (r"ADM, guided", DIFF, 4.59, 0.82, 0.52)]
        head = VGroup(*[label(t, font_size=22, color=GREY_A) for t in (r"ImageNet $256^2$", r"FID", r"precision",
                                                                         r"recall")])
        xs = [-4.4, -1.9, -0.4, 1.1]
        tab = VGroup(head)
        for nm, col, f, p, r in rows_:
            tab.add(VGroup(label(nm, font_size=24, color=col), MathTex(f"{f:.2f}", font_size=28, color=col),
                           MathTex(f"{p:.2f}", font_size=28, color=col), MathTex(f"{r:.2f}", font_size=28, color=col)))
        for k, r_ in enumerate(tab):
            for j, m in enumerate(r_):
                m.move_to([xs[j], 1.6 - 0.7 * k, 0])
        g = axes([0, 1], [0, 1], x_length=3.4, y_length=3.4, xlabel=r"precision", ylabel=r"recall",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], center=[4.4, 0.3, 0])
        dots = VGroup(*[Dot(g.ax.c2p(p, r), radius=0.09, color=col) for _, col, _, p, r in rows_])
        why_ = VGroup(label(r"a likelihood-style objective: \ every mode is paid for", font_size=22),
                      label(r"one stable regression: \ no game to balance", font_size=22),
                      label(r"scale: \ bigger simply works", font_size=22)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.18)
        why_.move_to([-2.6, -2.3, 0])
        cite_ = cite(r"Dhariwal \& Nichol, \textit{Diffusion Models Beat GANs on Image Synthesis} (2021), Table 5",
                     corner=DR)
        with self.voiceover(
            "For six years GANs drew the sharpest images. In 2021 Prafulla Dhariwal and Alex Nichol, at OpenAI, "
            "titled a paper with what happened: diffusion models beat GANs on image synthesis. "
            "<bookmark mark='a'/> On ImageNet at 256 pixels, BigGAN-deep had an FID of 6.95; guided diffusion, "
            "4.59. <bookmark mark='b'/> The GAN's precision was the highest, but its recall only 0.28: convincing "
            "images of a narrow slice of the world. <bookmark mark='c'/> The reasons are ones this part has met: "
            "an objective that charges for every mode missed, a stable regression instead of a game, and a recipe "
            "that kept improving as it grew."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(w_, shift=UP * 0.1) for w_ in why_], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tokens(self):
        x = node_box(r"image", DATA, font_size=24).move_to([-6.0, 0.8, 0])
        enc = node_box(r"encoder", VQ_C, font_size=24, height=0.9).move_to([-4.1, 0.8, 0])
        book = VGroup(*[Square(0.32, stroke_color=VQ_C, stroke_width=1.5, fill_color=VQ_C,
                               fill_opacity=0.15 + 0.07 * (k % 4)) for k in range(8)]).arrange(DOWN, buff=0.04)
        book.move_to([-1.9, 0.8, 0])
        bl = label(r"codebook", font_size=20, color=VQ_C).next_to(book, UP, buff=0.1)
        grid = VGroup(*[Square(0.3, stroke_color=GREY_C, stroke_width=1) for _ in range(16)]).arrange_in_grid(
            4, 4, buff=0.03).move_to([0.2, 0.8, 0])
        nums = VGroup(*[MathTex(str(v), font_size=16, color=VQ_C).move_to(s) for v, s in
                        zip([3, 3, 17, 4, 9, 22, 22, 1, 30, 5, 5, 12, 7, 7, 26, 0], grid)])
        gl = label(r"tokens", font_size=20, color=VQ_C).next_to(grid, UP, buff=0.1)
        dec = node_box(r"decoder", VQ_C, font_size=24, height=0.9).move_to([2.4, 0.8, 0])
        out = node_box(r"image", DATA, font_size=24).move_to([4.2, 0.8, 0])
        A = lambda a, b: Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
        arrs = VGroup(A(x, enc), A(enc, book), A(book, grid), A(grid, dec), A(dec, out))
        nl = label(r"each vector snapped to its nearest code; \ gradients pass straight through the snap",
                   font_size=20, color=GREY_A).move_to([-0.8, -0.4, 0])
        prior = node_box(r"an autoregressive model over the tokens", AR, font_size=22).move_to([0.2, -1.3, 0])
        pa = Arrow(prior.get_top(), grid.get_bottom(), buff=0.08, color=AR, stroke_width=2.5)
        hist = VGroup(
            history_card(2017, r"van den Oord, Vinyals \& Kavukcuoglu: \ VQ-VAE", r"a discrete code, \ a PixelCNN "
                         r"prior over it", width=4.2, font_size=17),
            history_card(2021, r"Esser, Rombach \& Ommer: \ VQGAN", r"a GAN loss on the decoder, \ a transformer "
                         r"prior", width=4.2, font_size=17),
            history_card(2021, r"Ramesh et al.: \ DALL$\cdot$E", r"a discrete VAE, \ a transformer over text and "
                         r"image tokens", width=4.2, font_size=17),
        ).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.25)
        if hist.width > 13.4:
            hist.width = 13.4
        with self.voiceover(
            "Meanwhile the families combined. In 2017 Aaron van den Oord, Oriol Vinyals and Koray Kavukcuoglu gave "
            "the VAE a discrete code. <bookmark mark='a'/> Each encoder vector snaps to the nearest entry of a "
            "learned codebook, so an image becomes a grid of integers: tokens. Gradients pass straight through the "
            "snap. <bookmark mark='b'/> Over the tokens, a PixelCNN learns the prior. <bookmark mark='c'/> In "
            "2021 VQGAN added a GAN loss to sharpen the decoder and a transformer over the tokens; DALL-E wrote "
            "text and image tokens with one transformer. A VAE to make tokens, a GAN to make them look good, an "
            "autoregressive model to write them: the front end of today's image systems, opened up in Parts 22 "
            "and 23."
        ) as vo:
            self.play(FadeIn(x), GrowArrow(arrs[0]), FadeIn(enc))
            vo.wait_until("a")
            self.play(GrowArrow(arrs[1]), FadeIn(book), FadeIn(bl), GrowArrow(arrs[2]), FadeIn(grid), FadeIn(nums),
                      FadeIn(gl), GrowArrow(arrs[3]), FadeIn(dec), GrowArrow(arrs[4]), FadeIn(out))
            self.play(FadeIn(nl))
            vo.wait_until("b")
            self.play(FadeIn(prior), GrowArrow(pa), FadeIn(hist[0]))
            vo.wait_until("c")
            self.play(FadeIn(hist[1]), FadeIn(hist[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        v, e, c = load("vq"), load("evaluate"), load("classifier")
        src, rec, codes = np.asarray(v["src"]), np.asarray(v["recon"]), np.asarray(v["codes"])
        d0 = digit_sheet(src[:1], 1, 1, size=1.6).move_to([-5.2, 1.4, 0])
        cg = VGroup(*[Square(0.27, stroke_color=GREY_D, stroke_width=1) for _ in range(49)]).arrange_in_grid(
            7, 7, buff=0.02).move_to([-2.8, 1.4, 0])
        cn = VGroup(*[MathTex(str(int(k)), font_size=13, color=VQ_C).move_to(s) for k, s in zip(codes[0].ravel(), cg)])
        r0 = digit_sheet(rec[:1], 1, 1, size=1.6).move_to([-0.4, 1.4, 0])
        a1 = Arrow(d0.get_right(), cg.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5)
        a2 = Arrow(cg.get_right(), r0.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5)
        K, n = int(v["K"]), int(v["grid"]) ** 2
        lab = VGroup(label(r"a test digit", font_size=18, color=DATA).next_to(d0, DOWN, buff=0.1),
                     label(rf"${n}$ tokens, \ each one of ${K}$", font_size=18, color=VQ_C).next_to(cg, DOWN, buff=0.1),
                     label(r"decoded", font_size=18, color=DATA).next_to(r0, DOWN, buff=0.1))
        rows = Group(digit_sheet(src, 1, 8, size=0.4, gap=0.03), digit_sheet(rec, 1, 8, size=0.4, gap=0.03))
        rows.arrange(DOWN, buff=0.08).move_to([4.2, 1.5, 0])
        rl = label(r"test digits, \ and decoded from their tokens", font_size=18, color=GREY_A).next_to(rows, UP,
                                                                                                    buff=0.1)
        sm = digit_sheet(np.asarray(v["show"])[:24], 3, 8, size=0.42, gap=0.03).move_to([-2.6, -2.0, 0])
        sl = label(r"new digits: \ tokens written by a small transformer, \ then decoded", font_size=18,
                   color=AR).next_to(sm, UP, buff=0.1)
        j = v["judge"]
        best = min((float(np.mean([r["fid"] for r in e["table"][f]])), f) for f in e["table"])
        stats = VGroup(
            label(rf"codebook in use: \ perplexity ${float(v['perplexity']):.1f}$ of ${K}$", font_size=20, color=VQ_C),
            label(rf"raw size: \ ${n} \times \log_2 {K} = {float(v['codebook_bits']):.0f}$ bits; \ the prior needs "
                  rf"${float(v['prior_bits']):.0f}$", font_size=20, color=AR),
            label(rf"FID of the two-stage model: \ ${float(j['fid']):.1f}$", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.8, -1.7, 0])
        vfid, bfid, perp = float(j["fid"]), best[0], float(v["perplexity"])
        rawb, prb = float(v["codebook_bits"]), float(v["prior_bits"])
        if vfid < bfid:
            verdict = (f"Its samples score an FID of {vfid:.1f}, better than any of the five single models of the last "
                       "chapter, though it was trained outside that budget.")
        else:
            verdict = (f"Its samples score an FID of {vfid:.1f}; the best single model of the last chapter scored "
                       f"{bfid:.1f}, and this one was trained outside that budget.")
        with self.voiceover(
            "We built a small one: each digit becomes a seven-by-seven grid of tokens, each "
            f"one of {K} codebook entries, and a decoder turns the grid back. <bookmark mark='a'/> The codebook's "
            f"perplexity is {perp:.1f}: that many of its {K} entries are, in effect, in use. <bookmark mark='b'/> "
            f"Written plainly a grid is {rawb:.0f} bits; a small transformer predicts it in {prb:.0f}. "
            "<bookmark mark='c'/> Sampling tokens from the transformer and decoding them draws new digits. "
            f"{verdict}"
        ) as vo:
            self.play(FadeIn(d0), GrowArrow(a1), FadeIn(cg), FadeIn(cn), GrowArrow(a2), FadeIn(r0), FadeIn(lab))
            vo.wait_until("a")
            self.play(FadeIn(rows), FadeIn(rl), FadeIn(stats[0]))
            vo.wait_until("b")
            self.play(FadeIn(stats[1]))
            vo.wait_until("c")
            self.play(FadeIn(sm), FadeIn(sl), FadeIn(stats[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scales(self):
        sizes = [1, 2, 3, 4, 6]
        maps = VGroup()
        for s in sizes:
            cell = 1.6 / s
            g = VGroup(*[Square(cell, stroke_color=AR, stroke_width=1.2, fill_color=AR,
                                fill_opacity=0.12 + 0.5 * ((i * 7 + s) % 5) / 5) for i in range(s * s)])
            g.arrange_in_grid(s, s, buff=0)
            maps.add(g)
        maps.arrange(RIGHT, buff=0.55).move_to([0, 1.0, 0])
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
                       for a, b in zip(maps, maps[1:])])
        cap = label(r"each map of tokens predicted at once, \ given all the coarser ones", font_size=22,
                    color=AR).next_to(maps, DOWN, buff=0.35)
        card = history_card(2024, r"Tian, Jiang, Yuan, Peng \& Wang: \ VAR, next-scale prediction",
                            r"ImageNet $256^2$: \ FID $1.73$, \ from $18.65$ for raster-order tokens; \ about "
                            r"$20\times$ faster; \ NeurIPS 2024 outstanding paper", width=8.4, font_size=20)
        card.to_edge(DOWN, buff=0.45)
        tg = note(r"schematic").to_corner(UR, buff=0.25)
        with self.voiceover(
            "Reading order is slow, and a strange order for a picture. In 2024 Keyu Tian and colleagues at "
            "ByteDance and Peking University predicted not the next token but the next scale. <bookmark "
            "mark='a'/> One token for the whole image, then a two-by-two map, then larger maps, each predicted at "
            "once given all the coarser ones. <bookmark mark='b'/> On ImageNet at 256 pixels: an FID of 1.73, "
            "from 18.65 for raster order, about twenty times faster; a NeurIPS 2024 outstanding paper."
        ) as vo:
            self.play(FadeIn(tg), FadeIn(maps[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a_), FadeIn(m_)) for a_, m_ in zip(arr, maps[1:])],
                                  lag_ratio=0.5), FadeIn(cap), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(card, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def distill(self):
        cards = VGroup(
            history_card(2023, r"Sauer et al.: \ adversarial diffusion distillation", r"SDXL-Turbo: \ $1$ to $4$ "
                         r"steps, \ a GAN loss plus a teacher", width=4.3, font_size=17),
            history_card(2024, r"Sauer et al.: \ latent ADD", r"SD3-Turbo: \ $4$ steps, \ the discriminator built "
                         r"from a diffusion model", width=4.3, font_size=17),
            history_card(2024, r"Yin et al.: \ DMD2", r"one step, \ a GAN loss on real images: \ FID $1.28$ on "
                         r"ImageNet $64^2$", width=4.3, font_size=17),
            history_card(2024, r"Huang et al.: \ R3GAN", r"a GAN rebuilt from first principles, \ with convergence "
                         r"guarantees", width=4.3, font_size=17),
            history_card(2024, r"Lu \& Song: \ continuous-time consistency", r"$2$ steps: \ FID $1.88$ on ImageNet "
                         r"$512^2$, \ 1.5B parameters", width=4.3, font_size=17),
            history_card(2026, r"Deng, Li, Li, Du \& He: \ drifting models", r"one step, \ trained to drift its "
                         r"samples onto the data: \ FID $1.54$, ImageNet $256^2$", width=4.3, font_size=17),
        )
        cards.arrange_in_grid(2, 3, buff=(0.2, 0.25)).move_to(DOWN * 0.2)
        if cards.width > 13.6:
            cards.width = 13.6
        head = label(r"the GAN comes back: \ one step instead of fifty", font_size=30, color=GAN_C).to_edge(UP,
                                                                                                         buff=0.35)
        with self.voiceover(
            "And the GAN didn't die. Diffusion needs dozens of network passes per image; a generator needs one. "
            "To get one step back, diffusion models are distilled into generators, and the best distillers use a "
            "discriminator. <bookmark mark='a'/> Axel Sauer and colleagues at Stability AI trained SDXL-Turbo, one "
            "to four steps, with a GAN loss and a diffusion teacher; then SD3-Turbo, with a discriminator built "
            "from a diffusion model. <bookmark mark='b'/> Tianwei Yin and colleagues' DMD2 added a GAN loss on "
            "real images: an FID of 1.28 on small ImageNet images, in one step. <bookmark mark='c'/> R3GAN rebuilt "
            "the GAN itself with a principled loss. Consistency models reach diffusion quality in two steps, and "
            "in 2026 Kaiming He's group trained one-step generators by drifting their samples onto the data: an "
            "FID of 1.54 on ImageNet."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cards[0]), FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
            vo.wait_until("c")
            self.play(FadeIn(cards[3]), FadeIn(cards[4]), FadeIn(cards[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tree(self):
        fam = VGroup(node_box(r"autoregressive", AR, font_size=22), node_box(r"VAE", VAE_C, font_size=22),
                     node_box(r"GAN", GAN_C, font_size=22), node_box(r"flow", FLOW, font_size=22),
                     node_box(r"energy and score", EBM, font_size=22)).arrange(DOWN, buff=0.35).move_to([-5.0, 0, 0])
        out = VGroup(node_box(r"tokenizers and latent spaces \ (Parts 22, 23)", VQ_C, font_size=22),
                     node_box(r"next-token and next-scale models \ (Parts 22, 23)", AR, font_size=22),
                     node_box(r"diffusion: \ the score at every noise level \ (Part 21)", DIFF, font_size=22),
                     node_box(r"flow matching: \ continuous flows by regression \ (Part 21)", FLOW, font_size=22),
                     node_box(r"few-step distillation with discriminators \ (Part 21)", GAN_C, font_size=22))
        out.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([2.6, 0, 0])
        links = [(0, 1), (1, 0), (2, 0), (2, 4), (3, 3), (4, 2), (1, 2)]
        arrs = VGroup(*[Arrow(fam[a].get_right(), out[b].get_left(), buff=0.1, color=GREY_B, stroke_width=2,
                              max_tip_length_to_length_ratio=0.05).set_opacity(0.8) for a, b in links])
        with self.voiceover(
            "So this is where the four answers, and the fifth, ended up. <bookmark mark='a'/> The VAE and the GAN "
            "became the tokenizers and latent spaces that every image and video model starts from. The "
            "autoregressive model writes those tokens, a scale or a token at a time. The energy model's score, "
            "learned at every noise level, became diffusion, with the VAE's bound inside it. The neural ODE "
            "became flow matching. And the GAN's discriminator came back to make diffusion fast. <bookmark "
            "mark='b'/> Which is why the next part, diffusion, is built from pieces you have now seen."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(f_, shift=RIGHT * 0.1) for f_ in fam], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(arrs[i]), FadeIn(out[links[i][1]]))
                                    for i in range(len(links))], lag_ratio=0.35), run_time=max(4.0, vo.until("b")))
        self.wait(0.3)
        self.clear_scene()
