from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import CFG_C, HIST, PART, PATCH, TXT, glyph_sheet, load

GUIDE_C = CFG_C["zero"]


def cross_attention_picture() -> VGroup:
    """Cross-attention: every picture token asks the prompt's tokens; keys and values come from the text."""
    img = VGroup(*[Square(0.34, stroke_color=PATCH, stroke_width=1.5, fill_color=PATCH, fill_opacity=0.2) for _ in range(6)]
                 ).arrange(RIGHT, buff=0.08)
    txt = VGroup(*[Square(0.34, stroke_color=TXT, stroke_width=1.5, fill_color=TXT, fill_opacity=0.25) for _ in range(4)]
                 ).arrange(RIGHT, buff=0.08)
    VGroup(img, txt).arrange(DOWN, buff=1.2)
    words = VGroup(*[data_text(w, font="DejaVu Sans Mono", font_size=16, color=TXT).next_to(s_, DOWN, buff=0.08)
                     for w, s_ in zip(("a", "red", "fox", "jumps"), txt)])
    lines = VGroup(*[Line(img[i].get_bottom(), txt[j].get_top(), color=C.ATTN, stroke_width=1.2, stroke_opacity=0.7)
                     for i in range(6) for j in range(4)])
    li = label(r"picture tokens: \ queries", font_size=18, color=PATCH).next_to(img, UP, buff=0.12)
    lt = label(r"prompt tokens: \ keys and values", font_size=18, color=TXT).next_to(words, DOWN, buff=0.1)
    return VGroup(img, txt, words, lines, li, lt)


class Prompt(VoiceoverScene):
    def construct(self):
        self.card()
        self.lineage()
        self.cross()
        self.guidance()

    def card(self):
        card = chapter_card(7, r"Words into pictures", r"How does a sentence steer a denoiser?", lit=(2014,), part=PART)
        with self.voiceover("Chapter seven. Words into pictures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def lineage(self):
        head = label(r"From GANs to text-to-image diffusion", font_size=34).to_edge(UP, buff=0.3)
        cards = VGroup(
            history_card(r"2014--19", r"GANs: \ BigGAN, \ StyleGAN", r"the sharpest pictures, \ hard to train \ (Part 20)",
                         color=HIST, width=3.3, font_size=18),
            history_card(r"Jan 2021", r"DALL$\cdot$E \ (Ramesh et al.)", r"$12$ billion weights: \ up to $256$ text tokens, "
                         r"\ then $32 \times 32$ picture tokens", color=HIST, width=3.3, font_size=18),
            history_card(r"May 2021", r"diffusion beats GANs", r"Dhariwal \& Nichol: \ ImageNet FID $4.59$ against "
                         r"BigGAN's $6.95$", color=HIST, width=3.3, font_size=18),
            history_card(r"Apr 2022", r"DALL$\cdot$E 2", r"text $\to$ a CLIP picture embedding $\to$ a diffusion "
                         r"decoder", color=HIST, width=3.3, font_size=18),
            history_card(r"May 2022", r"Imagen", r"a frozen T5 text encoder: \ a bigger language model helped more "
                         r"than a bigger denoiser", color=HIST, width=3.3, font_size=18),
            history_card(r"Jun 2022", r"Parti", r"$20$ billion weights, \ autoregressive over picture tokens", color=HIST,
                         width=3.3, font_size=18),
            history_card(r"Aug 2022", r"Stable Diffusion", r"latent diffusion, \ a CLIP text encoder, \ open weights",
                         color=HIST, width=3.3, font_size=18),
            history_card(r"Oct 2023", r"DALL$\cdot$E 3", r"retrain on long, detailed captions written by a model",
                         color=HIST, width=3.3, font_size=18),
        ).arrange_in_grid(rows=2, cols=4, buff=(0.2, 0.25)).next_to(head, DOWN, buff=0.3)
        if cards.width > 13.3:
            cards.width = 13.3
        with self.voiceover(
            "Until 2020, the sharpest generated pictures came from GANs, Part 20's BigGAN and StyleGAN. Text to "
            "image arrived from two directions. <bookmark mark='a'/> In January 2021 OpenAI's DALL-E treated it as "
            "language modelling: a twelve-billion-weight transformer wrote a caption's tokens, then a thirty-two by "
            "thirty-two grid of picture tokens. <bookmark mark='b'/> That May, Dhariwal and Nichol showed diffusion "
            "beating GANs on quality. <bookmark mark='c'/> In 2022 diffusion took over text to image: DALL-E 2 "
            "turned a caption into a CLIP picture embedding and decoded it by diffusion; <bookmark mark='d'/> "
            "Google's Imagen found that a bigger frozen language model, reading the prompt, helped more than a bigger "
            "denoiser; <bookmark mark='e'/> Parti kept the token route, at twenty billion weights; "
            "<bookmark mark='f'/> and Stable Diffusion put latent diffusion in everyone's hands, with open weights. "
            "<bookmark mark='g'/> In 2023 DALL-E 3 found the bottleneck was the data: it retrained on long, detailed "
            "captions written by a model, and followed prompts far better."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.1))
            for k, m in enumerate("abcdefg"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.1), run_time=0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cross(self):
        pic = cross_attention_picture().move_to([-3.4, 0.3, 0])
        f = MathTex(r"\operatorname{CrossAttn}(h, e) = \operatorname{softmax}\!\Big(\frac{(h W_Q)(e W_K)^{\top}}{\sqrt d}\Big)"
                    r"\,(e W_V)", font_size=30).move_to([3.2, 1.4, 0])
        fl = VGroup(label(r"$h$: \ the picture's tokens", font_size=20, color=PATCH),
                    label(r"$e$: \ the prompt's tokens, \ from a frozen text encoder \ (CLIP, \ T5)", font_size=20, color=TXT)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(f, DOWN, buff=0.3)
        side = label(r"the text never changes: \ it is read, \ not rewritten", font_size=22, color=GREY_A).next_to(fl, DOWN, buff=0.5)
        cite_ = cite(r"Rombach et al.\ (2022): \ cross-attention in every block of the U-Net", corner=DR)
        with self.voiceover(
            "How does the prompt reach the denoiser? In Stable Diffusion, by cross-attention. A frozen text encoder "
            "turns the prompt into tokens. <bookmark mark='a'/> In every block, each picture token asks a question, "
            "its query, and the prompt's tokens supply the keys and values: so each patch pulls in the words that "
            "matter to it. <bookmark mark='b'/> It's Part 13's attention with queries from one sequence and keys "
            "from another. <bookmark mark='c'/> Notice the text is only read, never updated by the picture. The "
            "next chapter's model changes that."
        ) as vo:
            self.play(FadeIn(pic[1]), FadeIn(pic[2]), FadeIn(pic[5]), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(pic[0]), FadeIn(pic[4]), LaggedStart(*[Create(l_) for l_ in pic[3]], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("b")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def guidance(self):
        g = load("guidance")
        ws = [float(w) for w in g["guides"]]
        acc, fd, var = (np.asarray(g[k], float) for k in ("acc", "fd", "variety"))
        shows = np.asarray(g["shows"])
        ax = axes([0, ws[-1]], [0, 1], x_length=4.6, y_length=2.6, xlabel=r"guidance weight $w$",
                  ylabel=r"read as the letter requested", xticks=ws[::2], yticks=[0, 0.5, 1], center=[-3.8, 1.1, 0],
                  font_size=17)
        top = float(var.max()) * 1.15
        bx = axes([0, ws[-1]], [0, top], x_length=4.6, y_length=2.6, xlabel=r"guidance weight $w$",
                  ylabel=r"variety: \ two drawings of one letter apart", xticks=ws[::2], yticks=[0, round(top / 2, 2)],
                  center=[2.0, 1.1, 0], font_size=17)
        la = VGroup(curve(ax.ax, ws, acc, GUIDE_C), *[Dot(ax.ax.c2p(w, a), radius=0.05, color=GUIDE_C) for w, a in zip(ws, acc)])
        lv = VGroup(curve(bx.ax, ws, var, C.TRUE_P), *[Dot(bx.ax.c2p(w, a), radius=0.05, color=C.TRUE_P) for w, a in zip(ws, var)])
        picks = [0, ws.index(2.0) if 2.0 in ws else 3, len(ws) - 1]
        rows = Group(*[Group(MathTex(rf"w = {ws[k]:g}", font_size=22, color=GUIDE_C),
                             glyph_sheet(shows[k], 1, 6, size=0.5, gap=0.05)).arrange(RIGHT, buff=0.25) for k in picks])
        rows.arrange(DOWN, buff=0.18, aligned_edge=RIGHT).move_to([4.6, -2.3, 0]).to_edge(RIGHT, buff=0.4)
        rl = label(r"six R's, \ the same noise", font_size=18, color=GREY_A).next_to(rows, LEFT, buff=0.3)
        cite_ = cite(r"Part 21's guidance on our adaLN-Zero transformer; \ $260$ letters per weight", corner=DL)
        a0, a2, aN = acc[0], acc[picks[1]], acc[-1]
        v0, vN = var[0], var[-1]
        verdict = (f"Unguided, the judge reads {100 * a0:.0f} percent as requested; at w = 2, {100 * a2:.0f}; at "
                   f"w = {ws[-1]:g}, {100 * aN:.0f}.")
        spread = (f"And the drawings of one letter grow alike: their spread falls from {v0:.2f} to {vN:.2f}." if vN < 0.9 * v0
                  else f"Their variety barely changes, {v0:.2f} to {vN:.2f}.")
        with self.voiceover(
            "And how hard should it listen? Part 21's classifier-free guidance pushes the denoiser away from its "
            "unconditional guess by a weight w; Stable Diffusion's default was seven and a half. We swept it on our "
            "letter transformer, using the letter as the prompt. <bookmark mark='a'/> " + verdict + " <bookmark mark='v'/> " + spread
            + " <bookmark mark='b'/> Guidance buys faithfulness with variety."
        ) as vo:
            self.play(Create(ax), Create(bx), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(la[0]), FadeIn(la[1:]), Create(lv[0]), FadeIn(lv[1:]), run_time=2.0)
            self.play(FadeIn(rows), FadeIn(rl))
            vo.wait_until("b")
            self.play(Indicate(rows[-1], color=GUIDE_C, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()
