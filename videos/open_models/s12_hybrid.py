from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.open_models.common import (
    cfg, label, layer_strip, model_tag, note, random_values, show_chapter_card, vector_strip,
)
from videos.open_models.toys import kv_cache


class Hybrid(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 11, "Kimi: three to one")
        self.c = cfg("kimi")
        self.tag = model_tag("kimi")
        self.add(self.tag)
        self.limits()
        self.layout()
        self.nope()
        self.gates_and_cache()

    # ------------------------------------------------------------------
    def limits(self):
        mem = VGroup(*[Square(0.18, stroke_width=0, fill_color=C.MEMORY, fill_opacity=0.7) for _ in range(64)])
        mem.arrange_in_grid(8, 8, buff=0.03).move_to(LEFT * 4.2 + DOWN * 0.2)
        mem_l = label(r"$128\times128$ per head", font_size=26, color=C.MEMORY).next_to(mem, DOWN, buff=0.2)
        strip = VGroup(*[Rectangle(width=0.06, height=0.5, stroke_width=0, fill_color=C.TOKEN, fill_opacity=0.5)
                         for _ in range(110)]).arrange(RIGHT, buff=0.01).move_to(RIGHT * 2.0 + UP * 0.6)
        strip_l = label(r"a million tokens of context", font_size=26, color=GREY_A).next_to(strip, UP, buff=0.15)
        needle = strip[38].copy().set_fill(YELLOW, 1)
        needle_l = label(r"a phone number, 600{,}000 tokens back", font_size=24, color=YELLOW).next_to(needle, DOWN, 0.2)
        q = label(r"can a fixed-size summary still hold it exactly?", font_size=30).move_to(RIGHT * 2.0 + DOWN * 1.6)
        with self.voiceover(
            "A memory of fixed size has a limit, though. <bookmark mark='m'/> 128 by 128 numbers per head can't hold an "
            "exact copy of a million tokens. <bookmark mark='n'/> Ask for a phone number that appeared 600,000 tokens ago, "
            "and a running summary may well have smudged it."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(mem, lag_ratio=0.01), FadeIn(mem_l), FadeIn(strip, lag_ratio=0.005), FadeIn(strip_l))
            vo.wait_until("n")
            self.play(FadeIn(needle), FadeIn(needle_l))
            self.play(FadeIn(q))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def layout(self):
        c = self.c
        types = c["layer_types"]
        assert len(types) == 93 and types.count("kda") == 69 and types.count("mla") == 24
        assert types[3] == "mla" and types[:3] == ["kda"] * 3 and types[-2:] == ["mla", "mla"]
        strip = layer_strip(types, {"kda": C.MEMORY, "mla": C.GLOBAL}, cell=0.115, gap=0.024, height=0.9)
        strip.move_to(UP * 0.2)
        leg = VGroup(
            VGroup(Square(0.25, stroke_width=0, fill_color=C.MEMORY, fill_opacity=0.9),
                   label(r"69 KDA layers: fixed-size memory", font_size=28, color=C.MEMORY)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.25, stroke_width=0, fill_color=C.GLOBAL, fill_opacity=0.9),
                   label(r"24 global attention layers (MLA)", font_size=28, color=C.GLOBAL)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.8).next_to(strip, DOWN, buff=0.7)
        title = label(r"Kimi K3's 93 layers, from its config", font_size=32).to_edge(UP, buff=0.9)
        br = Brace(VGroup(*strip[:4]), UP, buff=0.1, color=WHITE)
        br_l = label(r"3 KDA + 1 global, repeated", font_size=24).next_to(br, UP, buff=0.1).align_to(strip, LEFT)
        top = label(r"plus one more global layer on top", font_size=24, color=C.GLOBAL)
        top.next_to(strip[-1], UP, buff=0.35).align_to(strip, RIGHT)
        with self.voiceover(
            "So Kimi K3 keeps some real attention. <bookmark mark='p'/> Every fourth layer is a full, global attention "
            "layer, <bookmark mark='t'/> with one extra at the very top, so the last layer always sees everything. "
            "<bookmark mark='n'/> That makes 69 KDA layers and 24 global ones. The global layers use the same latent "
            "attention as GLM, MLA."
        ) as vo:
            self.play(FadeIn(title))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in strip], lag_ratio=0.015), run_time=1.8)
            vo.wait_until("p")
            self.play(GrowFromCenter(br), FadeIn(br_l))
            self.play(LaggedStart(*[Indicate(r, color=WHITE, scale_factor=1.3) for r in strip if r.layer_type == "mla"],
                                  lag_ratio=0.06), run_time=2)
            vo.wait_until("t")
            self.play(FadeIn(top), Indicate(strip[-1], color=WHITE))
            vo.wait_until("n")
            self.play(FadeIn(leg))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def nope(self):
        c = self.c
        assert c["mla_use_nope"] and c["kda_conv"] == 4
        title = label(r"The global layers use \textbf{no position encoding at all}", font_size=34, color=C.GLOBAL)
        title.to_edge(UP, buff=0.9)
        reasons = VGroup(
            label(r"order and recency already come from the KDA layers below:", font_size=28),
            label(r"\quad their memories fade with time, and a tiny convolution mixes each token\\\quad with the 3 "
                  r"before it", font_size=26, color=C.MEMORY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        conv = VGroup(*[Square(0.4, stroke_color=C.TOKEN, stroke_width=1.5, fill_color=C.TOKEN, fill_opacity=0.12)
                        for _ in range(9)]).arrange(RIGHT, buff=0.1)
        win = SurroundingRectangle(VGroup(*conv[4:8]), color=C.MEMORY, buff=0.06, stroke_width=3)
        conv_l = label(r"short convolution over the last 4 tokens", font_size=22, color=C.MEMORY).next_to(win, DOWN, 0.15)
        stages = VGroup(*[label(t, font_size=28) for t in (r"8K", r"64K", r"256K", r"1M")]).arrange(RIGHT, buff=0.9)
        arrows = VGroup(*[Arrow(stages[i].get_right(), stages[i + 1].get_left(), buff=0.12, color=GREY_B, stroke_width=3)
                          for i in range(3)])
        st_l = label(r"context length during training: no position settings to retune at any step", font_size=26,
                     color=YELLOW)
        col = VGroup(reasons, VGroup(conv, win, conv_l), VGroup(stages, arrows), st_l).arrange(DOWN, buff=0.45)
        col.next_to(title, DOWN, buff=0.5)
        st_l.next_to(stages, DOWN, buff=0.25)
        with self.voiceover(
            "Those global layers have one twist: <bookmark mark='n'/> no position encoding at all. No rotations, no "
            "position vectors. <bookmark mark='w'/> How can attention know word order, then? It doesn't have to. The KDA "
            "layers below already mix in order and recency: through their fading memories, <bookmark mark='c'/> and "
            "through a tiny convolution that blends each token with the three before it. <bookmark mark='x'/> A bonus: "
            "when Moonshot stretched the context during training, from 8 thousand tokens to 64 thousand, and later to a "
            "million, there were no position settings to retune."
        ) as vo:
            vo.wait_until("n")
            self.play(FadeIn(title))
            vo.wait_until("w")
            self.play(FadeIn(reasons[0]))
            self.play(FadeIn(reasons[1]))
            vo.wait_until("c")
            self.play(FadeIn(conv), Create(win), FadeIn(conv_l))
            self.play(win.animate.shift(RIGHT * 0.5), run_time=0.8)
            vo.wait_until("x")
            self.play(LaggedStart(*[FadeIn(s) for s in stages], lag_ratio=0.25), Create(arrows), run_time=1.5)
            self.play(FadeIn(st_l))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def gates_and_cache(self):
        kv = kv_cache()["kimi"]
        assert kv["n_mla"] == 24 and kv["per_token"] == 27648 and round(kv["fixed"] / 1e6) == 434
        out = vector_strip(random_values(8, seed=4), cell=0.24, color=C.ATTN, direction=RIGHT)
        gate = vector_strip([1, 0.1, 0.9, 0.5, 0.05, 0.95, 0.3, 0.8], cell=0.24, color=WHITE, direction=RIGHT, vmax=1)
        res = vector_strip(random_values(8, seed=4) * np.array([1, 0.1, 0.9, 0.5, 0.05, 0.95, 0.3, 0.8]), cell=0.24,
                           color=C.ATTN, direction=RIGHT, vmax=np.abs(random_values(8, seed=4)).max())
        times = MathTex(r"\odot", font_size=40)
        eq = MathTex("=", font_size=40)
        VGroup(out, times, gate, eq, res).arrange(RIGHT, buff=0.3).move_to(UP * 1.5)
        gl = VGroup(label(r"attention output", font_size=22, color=C.ATTN).next_to(out, DOWN, buff=0.15),
                    label(r"$\sigma(W_g \vec x)$: a gate per channel", font_size=22).next_to(gate, DOWN, buff=0.15),
                    label(r"what gets through", font_size=22, color=C.ATTN).next_to(res, DOWN, buff=0.15))
        bill = VGroup(
            MathTex(r"24 \text{ layers} \times 576 \times 2 \text{ bytes}", r"\approx 28\ \text{KB per token}",
                    font_size=34),
            MathTex(r"\Rightarrow 28\ \text{GB at a million tokens}", font_size=34, color=YELLOW),
            MathTex(r"+\; 69 \times 96 \times 128 \times 128 \times 4 \text{ bytes}", r"= 434\ \text{MB, fixed}",
                    font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 1.6)
        bill[0][1].set_color(C.GLOBAL)
        bill[2][1].set_color(C.MEMORY)
        src = note(r"cache sizes computed from the config (16-bit cache entries, 32-bit KDA memories)")
        src.to_edge(DOWN, buff=0.2)
        lin = note(r"Kimi Linear (Moonshot, 2025), same design at smaller scale: up to 75\% less cache and up to "
                   r"$6\times$ faster decoding at 1M tokens, vs.\ all-MLA", font_size=20).next_to(src, UP, buff=0.12)
        with self.voiceover(
            "<bookmark mark='g'/> Both kinds of layer also end with a gate: each output channel is multiplied by a "
            "sigmoid computed from the token, so each token decides which channels of the result to let through. "
            "<bookmark mark='c'/> Now the memory bill. K3's 24 global layers cache 576 numbers per token each: about 28 "
            "kilobytes per token, or 28 gigabytes at a million tokens. <bookmark mark='s'/> The 69 KDA memories add a "
            "fixed 434 megabytes, whether the context is ten tokens long or a million. <bookmark mark='l'/> In "
            "Moonshot's earlier, smaller Kimi Linear model, this design cut the cache by up to 75 percent, and sped up "
            "decoding at a million tokens by up to six times, compared with global attention in every layer."
        ) as vo:
            vo.wait_until("g")
            self.play(FadeIn(out), FadeIn(gl[0]))
            self.play(FadeIn(times), FadeIn(gate), FadeIn(gl[1]))
            self.play(FadeIn(eq), TransformFromCopy(out, res), FadeIn(gl[2]))
            vo.wait_until("c")
            self.play(Write(bill[0]), FadeIn(src))
            self.play(Write(bill[1]))
            vo.wait_until("s")
            self.play(Write(bill[2]))
            vo.wait_until("l")
            self.play(FadeIn(lin))
        self.clear_scene()
