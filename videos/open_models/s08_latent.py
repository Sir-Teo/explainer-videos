from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.open_models.common import (
    cfg, label, model_tag, note, random_values, schematic_tag, show_chapter_card, source, vector_strip,
)
from videos.open_models.toys import kv_cache


def funnel(left_h, right_h, width, color) -> Polygon:
    return Polygon([0, left_h / 2, 0], [width, right_h / 2, 0], [width, -right_h / 2, 0], [0, -left_h / 2, 0],
                   stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.2)


class LatentAttention(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 7, "GLM: compress the memory")
        self.c = cfg("glm")
        self.tag = model_tag("glm")
        self.add(self.tag)
        self.compress()
        self.absorb()
        self.tweaks()

    # ------------------------------------------------------------------
    def compress(self):
        c = self.c
        assert c["kv_lora_rank"] == 512 and c["qk_rope_head_dim"] == 64 and c["hidden"] == 6144
        kv = kv_cache()["glm"]
        assert kv["latent"] == 576 and kv["per_layer_mha"] == 32768 and round(32768 / 576) == 57
        x = vector_strip(random_values(16, seed=1), cell=0.2).move_to(LEFT * 5.7)
        x_l = label(r"token\\6{,}144 numbers", font_size=22, color=C.EMBED).next_to(x, DOWN, buff=0.15)
        down = funnel(x.height, 1.2, 1.1, C.LATENT).next_to(x, RIGHT, buff=0.1)
        lat = vector_strip(random_values(6, seed=2), cell=0.18, color=C.LATENT).next_to(down, RIGHT, buff=0.1)
        rope = vector_strip(random_values(2, seed=3), cell=0.12, color=C.POSITION).next_to(lat, DOWN, buff=0.12)
        lat_l = label(r"latent: 512", font_size=22, color=C.LATENT).next_to(lat, UP, buff=0.15)
        rope_l = label(r"+ 64 for position", font_size=20, color=C.POSITION).next_to(rope, DOWN, buff=0.1)
        cache = VGroup()
        for i in range(9):
            col = VGroup(vector_strip(random_values(6, seed=10 + i), cell=0.12, color=C.LATENT, outline=False),
                         vector_strip(random_values(2, seed=30 + i), cell=0.08, color=C.POSITION, outline=False))
            col.arrange(DOWN, buff=0.08)
            cache.add(col)
        cache.arrange(RIGHT, buff=0.1).move_to(RIGHT * 0.2 + UP * 1.8)
        cache_l = label(r"the cache: one latent per token", font_size=24, color=C.LATENT).next_to(cache, UP, buff=0.15)
        heads = VGroup()
        for h in range(4):
            k = vector_strip(random_values(6, seed=50 + h), cell=0.13, color=C.KEY, outline=False)
            v = vector_strip(random_values(6, seed=60 + h), cell=0.13, color=C.VALUE, outline=False)
            heads.add(VGroup(k, v).arrange(RIGHT, buff=0.06))
        heads.add(MathTex(r"\cdots", font_size=36))
        heads.arrange(RIGHT, buff=0.35).move_to(RIGHT * 3.6 + DOWN * 1.2)
        ups = VGroup(*[Arrow(lat.get_right(), hd.get_top(), buff=0.12, color=C.LATENT, stroke_width=2,
                             max_tip_length_to_length_ratio=0.06) for hd in heads[:4]])
        h_l = label(r"each of 64 heads rebuilds its own key and value", font_size=24).next_to(heads, DOWN, buff=0.25)
        to_cache = Arrow(lat.get_top(), cache.get_left() + DOWN * 0.2, buff=0.15, color=C.LATENT, stroke_width=3)
        with self.voiceover(
            "GLM takes a different route. Its attention uses a design DeepSeek introduced, called multi-head latent "
            "attention, or MLA. <bookmark mark='i'/> The idea: don't cache each head's keys and values at all. "
            "<bookmark mark='c'/> Instead, squeeze the token's vector down into one small latent vector, just 512 "
            "numbers, <bookmark mark='s'/> and cache only that. <bookmark mark='u'/> When a head needs a key and a value, "
            "it rebuilds them from the latent, with its own pair of up-projection matrices. One small cached vector "
            "serves all 64 heads."
        ) as vo:
            self.play(FadeIn(x), FadeIn(x_l))
            vo.wait_until("c")
            self.play(FadeIn(down), TransformFromCopy(x, lat), FadeIn(lat_l), run_time=1.3)
            vo.wait_until("s")
            self.play(GrowArrow(to_cache), LaggedStart(*[FadeIn(cc[0], shift=LEFT * 0.1) for cc in cache], lag_ratio=0.08),
                      FadeIn(cache_l))
            vo.wait_until("u")
            self.play(LaggedStart(*[GrowArrow(a) for a in ups], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(hd, shift=DOWN * 0.1) for hd in heads], lag_ratio=0.1), FadeIn(h_l), run_time=1.6)

        tally = VGroup(
            MathTex(r"\text{textbook: } 64 \times (256 + 256)", r"= 32{,}768", font_size=34),
            MathTex(r"\text{MLA: } 512 + 64", r"= 576", font_size=34),
            MathTex(r"57\times", r"\text{ less memory per token}", font_size=38),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.25).to_corner(DR, buff=0.4).shift(UP * 0.2)
        tally[0][1].set_color(RED)
        tally[1][1].set_color(C.LATENT)
        tally[2][0].set_color(YELLOW)
        with self.voiceover(
            "<bookmark mark='p'/> Position needs special care. Rotary position encoding doesn't play well with this "
            "compression, so 64 extra numbers carry a separate, position-rotated key, shared by all the heads. <bookmark mark='t'/> In total, "
            "576 numbers per token per layer, <bookmark mark='x'/> versus 32,768 if all 64 heads cached full keys and "
            "values: <bookmark mark='r'/> 57 times less memory."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(rope), FadeIn(rope_l), LaggedStart(*[FadeIn(cc[1]) for cc in cache], lag_ratio=0.05))
            self.play(FadeOut(heads), FadeOut(ups), FadeOut(h_l))
            vo.wait_until("t")
            self.play(Write(tally[1]))
            vo.wait_until("x")
            self.play(Write(tally[0]))
            vo.wait_until("r")
            self.play(Write(tally[2]))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def absorb(self):
        e1 = MathTex(r"\text{score}", "=", r"\vec q_h", r"\cdot", r"(", r"W_h", r"\,\vec c", r")", font_size=56)
        e2 = MathTex(r"\text{score}", "=", r"(", r"W_h^{\top}", r"\vec q_h", r")", r"\cdot", r"\vec c", font_size=56)
        for e in (e1, e2):
            e.move_to(UP * 1.0)
        e1[2].set_color(C.QUERY)
        e1[5].set_color(C.KEY)
        e1[6].set_color(C.LATENT)
        e2[3].set_color(C.KEY)
        e2[4].set_color(C.QUERY)
        e2[7].set_color(C.LATENT)
        b1 = Brace(VGroup(*e1[4:8]), DOWN, color=C.KEY)
        b1t = label(r"the head's key, rebuilt from the latent", font_size=26, color=C.KEY).next_to(b1, DOWN, buff=0.1)
        b2 = Brace(VGroup(*e2[2:6]), DOWN, color=C.QUERY)
        b2t = label(r"fold the matrix into the query, once per token", font_size=26, color=C.QUERY).next_to(b2, DOWN, 0.1)
        res = label(r"$\Rightarrow$ compare queries directly against the cached latents; never decompress the cache",
                    font_size=28, color=YELLOW).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "And there's an elegant trick that makes this cheap. <bookmark mark='a'/> A head's score for a past token is "
            "its query dotted with its rebuilt key, and that key is a matrix times the cached latent. "
            "<bookmark mark='b'/> But a dot product lets you move the matrix to the other side, onto the query. "
            "<bookmark mark='l'/> So each head transforms its query once, and then compares it directly against the "
            "cached latents, without ever decompressing them."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(e1))
            self.play(GrowFromCenter(b1), FadeIn(b1t))
            vo.wait_until("b")
            self.play(FadeOut(b1), FadeOut(b1t))
            self.play(TransformMatchingTex(e1, e2, path_arc=PI / 2), run_time=1.6)
            self.play(GrowFromCenter(b2), FadeIn(b2t))
            vo.wait_until("l")
            self.play(FadeIn(res, shift=UP * 0.2))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def tweaks(self):
        c = self.c
        assert c["heads"] == 64 and c["qk_nope_head_dim"] + c["qk_rope_head_dim"] == 256
        t1 = VGroup(label(r"\textbf{1.} Muon Split", font_size=32, color=C.GLM),
                    label(r"With the Muon optimizer, MLA trained worse than ordinary grouped-query attention,",
                          font_size=26),
                    label(r"until each head's up-projection was orthogonalized on its own. Then it matched.",
                          font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        h96 = VGroup(*[Rectangle(width=0.07, height=0.192 * 3, stroke_width=0, fill_color=C.QUERY, fill_opacity=0.8)
                       for _ in range(96)]).arrange(RIGHT, buff=0.025)
        h64 = VGroup(*[Rectangle(width=0.07, height=0.256 * 3, stroke_width=0, fill_color=C.QUERY, fill_opacity=0.8)
                       for _ in range(64)]).arrange(RIGHT, buff=0.025)
        hl96 = label(r"96 heads $\times$ 192 dims", font_size=24, color=GREY_A)
        hl64 = label(r"64 heads $\times$ 256 dims", font_size=24, color=C.GLM)
        g96 = VGroup(h96, hl96).arrange(DOWN, buff=0.12)
        g64 = VGroup(h64, hl64).arrange(DOWN, buff=0.12)
        heads = VGroup(g96, g64).arrange(RIGHT, buff=1.0, aligned_edge=DOWN)
        heads.width = 11.5
        arrow = Arrow(g96.get_right(), g64.get_left(), buff=0.15, color=WHITE)
        t2 = VGroup(label(r"\textbf{2.} Fewer, bigger heads", font_size=32, color=C.GLM),
                    label(r"Same parameters and training compute; less work at each decoding step.", font_size=26))
        t2.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        col = VGroup(t1, t2, heads).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 0.1)
        col.to_edge(LEFT, buff=0.9)
        arrow.put_start_and_end_on(g96.get_right() + RIGHT * 0.15, g64.get_left() + LEFT * 0.15)
        title = label(r"Two adjustments in GLM-5", font_size=34).to_edge(UP, buff=0.9)
        src = source(r"GLM-5 technical report (Z.ai, arXiv:2602.15763), Section 2.1")
        with self.voiceover(
            "GLM made two adjustments of its own. <bookmark mark='m'/> First, the team found that MLA, trained with the "
            "Muon optimizer, did worse than ordinary grouped-query attention, until they orthogonalized each head's "
            "projection matrix separately in the optimizer. That closed the gap. <bookmark mark='h'/> Second, it uses "
            "fewer, bigger heads: 64 heads of 256 dimensions, instead of 96 heads of 192. That keeps the parameter "
            "count and the training compute the same, while cutting the work at each decoding step."
        ) as vo:
            self.play(FadeIn(title), FadeIn(src))
            vo.wait_until("m")
            self.play(FadeIn(t1, shift=UP * 0.1))
            vo.wait_until("h")
            self.play(FadeIn(t2, shift=UP * 0.1))
            self.play(FadeIn(g96))
            self.play(GrowArrow(arrow), FadeIn(g64))
        self.clear_scene(self.tag)

        but = VGroup(label(r"MLA shrinks what each token costs to remember \dots", font_size=34, color=C.LATENT),
                     label(r"\dots but at a million tokens, each new token still compares itself\\against a million "
                           r"cached latents, in every layer.", font_size=32)).arrange(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='b'/> But MLA shrinks what each token costs to remember; it doesn't change how many tokens "
            "there are. <bookmark mark='m'/> At a million tokens, each new token still compares itself against a million "
            "cached latents, in every layer."
        ) as vo:
            vo.wait_until("b")
            self.play(FadeIn(but[0]))
            vo.wait_until("m")
            self.play(FadeIn(but[1]))
        self.clear_scene()
