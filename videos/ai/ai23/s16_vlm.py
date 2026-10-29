from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import CLIP_C, IMG_C, PART, TEXT_C, band, curve, gray_image, load, node_box

VIS_C = IMG_C


def tok_row(n, color, size=0.26):
    return VGroup(*[Square(size, stroke_color=color, stroke_width=1.2, fill_color=color, fill_opacity=0.35)
                    for _ in range(n)]).arrange(RIGHT, buff=0.04)


class VLM(VoiceoverScene):
    def construct(self):
        self.card()
        self.connectors()
        self.resolution()
        self.positions()
        self.fusion()

    def card(self):
        card = chapter_card(15, r"Models that see", r"How does a language model read a picture?", part=PART)
        with self.voiceover("Chapter fifteen. Models that see."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def connectors(self):
        cols = VGroup()
        specs = [
            (r"Flamingo \ (DeepMind, 2022)", r"a resampler squeezes the picture \\ into $64$ tokens; \ new cross-attention "
             r"\\ layers in a frozen language model", 8),
            (r"BLIP-2 \ (Salesforce, 2023)", r"$32$ learned queries ask the \\ frozen image encoder \ (the Q-Former)", 6),
            (r"LLaVA \ (2023)", r"a linear map turns each patch \\ into a word vector: \ $576$ tokens \\ (LLaVA-1.5: \ a "
             r"two-layer MLP)", 12)]
        for i, (name, what, n) in enumerate(specs):
            enc = node_box(r"vision encoder \\ (CLIP)", VIS_C, font_size=18)
            con = node_box(r"connector", C.MODEL_Q, font_size=18)
            toks = tok_row(n, VIS_C, 0.2)
            lm = node_box(r"language model", TEXT_C, font_size=18, width=2.8)
            g = VGroup(enc, con, toks, lm).arrange(DOWN, buff=0.3)
            arr = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.05, color=GREY_B, stroke_width=2,
                                 max_tip_length_to_length_ratio=0.3) for a, b in zip(g, g[1:])])
            col = VGroup(label(name, font_size=22, color=WHITE), g, arr, label(what, font_size=17, color=GREY_A))
            col[0].next_to(g, UP, buff=0.25)
            col[3].next_to(g, DOWN, buff=0.25)
            cols.add(col)
        cols.arrange(RIGHT, buff=0.7, aligned_edge=UP).scale(1.2).move_to(DOWN * 0.2)
        if cols.width > 13.2:
            cols.width = 13.2
        hd = label(r"giving a language model eyes", font_size=40).to_edge(UP, buff=0.35)
        tag = note(r"schematic", font_size=18).to_corner(DL, buff=0.3)
        data = label(r"LLaVA's training: \ align the connector on captions; \ then $158$ thousand examples of chat about "
                     r"pictures, \ written by GPT-4", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.35)
        if data.width > 12.8:
            data.width = 12.8
        with self.voiceover(
            "CLIP matches pictures with captions, but it can't answer a question about a picture. For that, connect a "
            "vision encoder to a language model. <bookmark mark='a'/> DeepMind's Flamingo, in 2022, squeezed each "
            "picture into 64 tokens and added new cross-attention layers to a frozen language model. "
            "<bookmark mark='b'/> Salesforce's BLIP-2 sent 32 learned queries to a frozen image encoder. "
            "<bookmark mark='c'/> And in April 2023 LLaVA showed how little it takes: a single linear map turns each "
            "of CLIP's patch vectors into a vector in the language model's word space, and the picture is just more "
            "tokens at the start of the prompt. <bookmark mark='d'/> Train the map on captions, then fine-tune on 158 "
            "thousand examples of chat about pictures that GPT-4 wrote from their captions. Nearly every open "
            "vision-language model since has this shape."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hd))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]))
            vo.wait_until("b")
            self.play(FadeIn(cols[1]))
            vo.wait_until("c")
            self.play(FadeIn(cols[2]))
            vo.wait_until("d")
            self.play(FadeIn(data))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def resolution(self):
        c = load("clip")
        v = load("vlm")
        res = [int(r) for r in c["res"]]
        B = int(c["batches"][-1])
        A = np.asarray(c[f"res_clip_{B}"], float)
        ax = axes([0, 20, 5], [0, 1, 0.25], x_length=5.0, y_length=3.2, xlabel=r"pixels on a side",
                  ylabel=r"letters our CLIP reads right", xticks=[5, 10, 15, 20], yticks=[0, 0.5, 1],
                  yfmt=lambda y: f"{int(round(100 * y))}\\%", center=[-3.6, 0.2, 0])
        cv = curve(ax.ax, res, A.mean(0), CLIP_C, 3.5)
        bd = band(ax.ax, res, A.min(0), A.max(0), CLIP_C, 0.25)
        dots = VGroup(*[Dot(ax.ax.c2p(r, a), radius=0.06, color=CLIP_C) for r, a in zip(res, A.mean(0))])
        from videos.ai.ai23.clip import shrink, styled_glyphs

        im = styled_glyphs(1)[0][40:41]
        thumbs = Group(*[gray_image(shrink(im, r)[0], 0.55) for r in res]).arrange(RIGHT, buff=0.12)
        thumbs.next_to(ax, DOWN, buff=0.7)
        tl = VGroup(*[MathTex(str(r), font_size=16, color=GREY_B).next_to(t_, DOWN, buff=0.05) for r, t_ in zip(res, thumbs)])
        rows = v["rows"]
        hdr = VGroup(*[label(t, font_size=20, color=GREY_B) for t in (r"picture", r"resized to", r"tokens")])
        tab = VGroup()
        xs = [1.6, 3.6, 5.5]
        for j, h in enumerate(hdr):
            h.move_to([xs[j], 2.3, 0])
        for i, r in enumerate(rows):
            vals = [MathTex(rf"{r['w']} \times {r['h']}", font_size=24), MathTex(rf"{r['W']} \times {r['H']}", font_size=24),
                    MathTex(f"{r['tokens']:,}".replace(",", "{,}"), font_size=24, color=VIS_C)]
            row = VGroup()
            for j, m in enumerate(vals):
                m.move_to([xs[j], 1.75 - 0.5 * i, 0])
                row.add(m)
            tab.add(row)
        tabl = label(r"Qwen2-VL's dynamic resolution: \ $14$-pixel patches, \ merged $2 \times 2$: \\ one token per "
                     r"$28 \times 28$ pixels, \ at most $1{,}280$ by default", font_size=18, color=GREY_A)
        tabl.next_to(tab, DOWN, buff=0.3).align_to(hdr, LEFT)
        i10 = res.index(10) if 10 in res else len(res) // 2
        i5 = res.index(5) if 5 in res else 1
        with self.voiceover(
            "Early models resized every picture to one small square, 224 or 336 pixels on a side. That's fine for a "
            "dog, fatal for a receipt. <bookmark mark='a'/> Our letter-reading CLIP shows the effect: shrink its "
            f"twenty-pixel letters and blow them back up. At ten pixels it still reads {100 * A.mean(0)[i10]:.0f} "
            f"percent of the letters; at five, {100 * A.mean(0)[i5]:.0f}. <bookmark mark='b'/> In 2024 Qwen2-VL "
            "stopped resizing to a square. A picture keeps roughly its own size and shape, is cut into 14-pixel "
            "patches, and every two by two patches become one token, so a small icon costs a few dozen tokens and a "
            "big screenshot over a thousand. These counts come from the published code."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(thumbs), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(bd), Create(cv), FadeIn(dots), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.25), FadeIn(tabl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def positions(self):
        v = load("vlm")
        kinds = [str(k) for k in v["mrope_kind"]]
        ids = [tuple(int(x) for x in t) for t in v["mrope_ids"]]
        gh, gw = (int(x) for x in v["grid"])
        cells = VGroup()
        for k, (kind, pid) in enumerate(zip(kinds, ids)):
            col = TEXT_C if kind == "text" else VIS_C
            sq = Square(0.62, stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=0.25)
            lab = MathTex(rf"({pid[0]},{pid[1]},{pid[2]})", font_size=18, color=WHITE)
            cells.add(VGroup(sq, lab.next_to(sq, DOWN, buff=0.08)))
        cells.arrange(RIGHT, buff=0.12).move_to(UP * 1.5)
        if cells.width > 13.2:
            cells.width = 13.2
        cl = label(r"each token's position: \ (time, \ row, \ column)", font_size=22, color=GREY_A).next_to(cells, UP, buff=0.3)
        img_idx = [k for k, kd in enumerate(kinds) if kd == "image"]
        grid = VGroup(*[cells[k][0].copy() for k in img_idx])
        for i, sq in enumerate(grid):
            sq.move_to([-1.2 + (i % gw) * 0.66, -0.9 - (i // gw) * 0.66, 0])
        gl = label(rf"the picture's ${gh} \times {gw}$ tokens: \ one time, \ their own rows and columns", font_size=20,
                   color=VIS_C).next_to(grid, DOWN, buff=0.2)
        rope = MathTex(r"\text{rotary dimensions} = \underbrace{\cdots}_{\text{time}}\ \underbrace{\cdots}_{\text{row}}\ "
                       r"\underbrace{\cdots}_{\text{column}}", font_size=28).move_to([3.9, -1.1, 0])
        notes = VGroup(*[label(t, font_size=18, color=GREY_A) for t in (
            r"Qwen2.5-VL (2025): \ video time in absolute seconds", r"Qwen3-VL (2025): \ the three interleaved across "
            r"frequencies; \\ features from several encoder layers (DeepStack)")]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        notes.to_edge(DOWN, buff=0.4).shift(RIGHT * 1.0)
        tag = note(r"computed with Qwen2-VL's rule: \ $3$ text tokens, \ a $2 \times 3$ picture, \ $3$ text tokens",
                   font_size=18).to_corner(UL, buff=0.3)
        with self.voiceover(
            "A picture's tokens are a grid, not a line, and positions should say so. <bookmark mark='a'/> Qwen2-VL's "
            "answer, M-RoPE, gives every token three coordinates: time, row and column. Text tokens use the same "
            "number three times, so for text it is ordinary RoPE from Part 13. <bookmark mark='b'/> A picture's "
            "tokens share one time and take their own rows and columns, and the text after it carries on past the "
            "largest number used. <bookmark mark='c'/> The rotary dimensions are split three ways, each part rotated "
            "by one coordinate, so attention can tell neighbours in the picture from neighbours in the sentence. "
            "<bookmark mark='d'/> Video adds frames in time; Qwen2.5-VL tied that axis to real seconds, and Qwen3-VL "
            "spread the three across the frequencies."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(cl), LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(TransformFromCopy(VGroup(*[cells[k][0] for k in img_idx]), grid), FadeIn(gl), run_time=1.5)
            vo.wait_until("c")
            self.play(Write(rope))
            vo.wait_until("d")
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fusion(self):
        def stack(title, parts, color):
            g = VGroup(*[node_box(p, c, font_size=18) for p, c in parts]).arrange(DOWN, buff=0.25)
            return VGroup(label(title, font_size=24, color=color), g).arrange(DOWN, buff=0.3)

        left = stack(r"bolted on", [(r"a language model, \ trained on text", TEXT_C), (r"$+$ \ a connector", C.MODEL_Q),
                                    (r"$+$ \ a vision encoder, \ trained apart", VIS_C)], GREY_A)
        right = stack(r"early fusion", [(r"one model, \ trained from the start \\ on text and picture tokens mixed", WHITE),
                                        (r"(still a vision encoder for the patches)", VIS_C)], WHITE)
        VGroup(left, right).arrange(RIGHT, buff=1.6).move_to(UP * 0.6)
        arr = Arrow(left.get_right(), right.get_left(), buff=0.3, color=GREY_B)
        facts = VGroup(*[label(t, font_size=20, color=GREY_A) for t in (
            r"Chameleon (Meta, 2024): \ pictures as VQ tokens in the text's own vocabulary",
            r"Qwen3.5 (Alibaba, February 2026): \ early fusion; \ on text as good as Qwen3, \ on pictures better than "
            r"Qwen3-VL \ (model card)")]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.5)
        if facts.width > 13:
            facts.width = 13
        tag = note(r"schematic", font_size=18).to_corner(UL, buff=0.3)
        with self.voiceover(
            "The connector recipe bolts a vision encoder onto a model that learned language alone. "
            "<bookmark mark='a'/> The newer recipe trains on mixed sequences from the start, early fusion. In 2024 "
            "Meta's Chameleon wrote pictures as VQ tokens in the same vocabulary as words, Part 22's image tokens. "
            "<bookmark mark='b'/> In February 2026 Alibaba's Qwen3.5 was trained from the start on text and picture "
            "tokens together; by its model card it matches its text-only predecessor on text and beats the dedicated "
            "vision-language models on pictures. Seeing is no longer an add-on."
        ) as vo:
            self.play(FadeIn(left), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowArrow(arr), FadeIn(right), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
        self.wait(0.3)
        self.clear_scene()
