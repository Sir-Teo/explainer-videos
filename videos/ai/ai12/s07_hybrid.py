from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import A, STATE, curve, gib, load

LIN, ATT = C.INTERVAL, C.ATTN

STACKS = [  # (model, year, layers in one repeating unit: L = a linear-time layer, A = full attention)
    (r"Jamba", 2024, "LLLALLLL", r"Mamba"),
    (r"MiniMax-01", 2025, "LLLLLLLA", r"lightning attention"),
    (r"Qwen3-Next", 2025, "LLLA", r"Gated DeltaNet"),
    (r"Kimi Linear", 2025, "LLLA", r"Kimi Delta Attention"),
]


class Hybrid(VoiceoverScene):
    def construct(self):
        self.card()
        self.stacks()
        self.memory()

    def card(self):
        card = chapter_card(7, r"Hybrids", r"Why not have both?", part=12)
        with self.voiceover("Chapter seven. Hybrids."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def stacks(self):
        cols, atts = Group(), VGroup()
        for name, year, unit, lin_name in STACKS:
            reps = 16 // len(unit)
            seq = unit * reps
            blocks = VGroup(*[Rectangle(width=1.1, height=0.2, stroke_width=1, stroke_color=GREY_D,
                                        fill_color=ATT if ch == "A" else LIN, fill_opacity=0.85) for ch in seq])
            blocks.arrange(UP, buff=0.04)
            atts.add(*[b for b, ch in zip(blocks, seq) if ch == "A"])
            t = label(rf"{name} \ ({year})", font_size=24, color=WHITE).next_to(blocks, UP, buff=0.2)
            n_att = unit.count("A")
            r = label(rf"${n_att}$ in ${len(unit)}$", font_size=22, color=ATT).next_to(blocks, DOWN, buff=0.15)
            ln = label(lin_name, font_size=18, color=LIN).next_to(r, DOWN, buff=0.1)
            cols.add(VGroup(blocks, t, r, ln))
        cols.arrange(RIGHT, buff=1.0).move_to(DOWN * 0.1)
        key = VGroup(VGroup(Square(0.25, fill_color=LIN, fill_opacity=0.85, stroke_width=0),
                            label(r"a linear-time layer: \ fixed-size memory", font_size=22, color=LIN)).arrange(RIGHT, buff=0.15),
                     VGroup(Square(0.25, fill_color=ATT, fill_opacity=0.85, stroke_width=0),
                            label(r"full attention: \ a growing cache", font_size=22, color=ATT)).arrange(RIGHT, buff=0.15))
        key.arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.35)
        tag = note(r"the share of attention layers, \ from each model's report; \ 16 layers drawn, \ schematic order").to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Fixed-size memories are cheap, but they forget; attention remembers everything exactly, at a price. "
            "So the newest models mix them. <bookmark mark='a'/> Jamba, in 2024, put one attention layer among "
            "every eight, the rest Mamba. MiniMax-01 does the same with lightning attention. Qwen3-Next and Kimi "
            "Linear, in 2025, use one attention layer in four, the other three running the gated delta rule. "
            "<bookmark mark='b'/> The fast layers carry the gist of a long text cheaply; the few attention layers "
            "look up exact details when they're needed."
        ) as vo:
            self.play(FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cols], lag_ratio=0.35), run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(atts, color=WHITE, scale_factor=1.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def memory(self):
        k = load("kvcache")
        ctx = np.asarray(k["ctx"], float)
        lines = [("llama", r"Llama 3.1 70B", C.TRUE_P), ("mla", r"DeepSeek-V3", C.BITS), ("qwen", r"Qwen3-Next", LIN)]
        lx = np.log10(ctx)
        ys = {key: np.log2(np.asarray(k[f"total_{key}"]) / 2 ** 30) for key, _, _ in lines}
        y0, y1 = math.floor(min(v.min() for v in ys.values())), math.ceil(max(v.max() for v in ys.values()))
        # y measured from the bottom (log2 GiB minus y0), so the x axis sits at the bottom of the chart
        ys = {key: v - y0 for key, v in ys.items()}
        ax = Axes(x_range=[3, 6, 1], y_range=[0, y1 - y0, 1], x_length=7.6, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.8, -0.4, 0])
        xt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for t, v in ((r"1{,}000", 3), (r"10{,}000", 4), (r"100{,}000", 5), (r"10^6", 6))])
        yt = VGroup(*[MathTex(gib(2 ** (v + 30)), font_size=20, color=GREY_B).next_to(ax.c2p(3, v - y0), LEFT, buff=0.1)
                      for v in range(y0, y1 + 1, 2)])
        xn = label(r"context, \ in tokens", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"memory for one conversation \ (bf16, \ log scale)", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12)
        yn.align_to(ax, LEFT)
        cs = VGroup(*[curve(ax, lx, ys[key], c_, 4) for key, _, c_ in lines])
        i128 = list(ctx).index(128e3)
        ks = VGroup(*[label(rf"{n}: \ ${gib(float(np.asarray(k[f'total_{key}'])[i128]))}$", font_size=24, color=c_)
                      for key, n, c_ in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.6, 1.0, 0])
        kl = label(r"at $128{,}000$ tokens", font_size=22, color=GREY_A).next_to(ks, UP, buff=0.2).align_to(ks, LEFT)
        st = label(rf"Qwen3-Next's fixed state: \\ ${gib(float(k['qwen_state']))}$, \ the same at any length", font_size=22,
                   color=LIN).next_to(ks, DOWN, buff=0.5).align_to(ks, LEFT)
        keep_in_frame(VGroup(kl, ks, st))
        q, ll = np.asarray(k["total_qwen"])[i128], np.asarray(k["total_llama"])[i128]
        with self.voiceover(
            "The memory bill shows why. For one conversation of a hundred and twenty-eight thousand tokens, "
            f"<bookmark mark='a'/> Llama 3.1's grouped-query cache takes {ll / 2**30:.0f} gigabytes; DeepSeek-V3's "
            f"latent cache, {np.asarray(k['total_mla'])[i128] / 2**30:.1f}; Qwen3-Next, with attention in only a quarter "
            f"of its layers, {q / 2**30:.1f}, about {ll / q:.0f} times less than Llama. Its delta-rule layers add "
            f"just {k['qwen_state'] / 2**20:.0f} megabytes of state, the same at any length."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c_) for c_ in cs], lag_ratio=0.4), FadeIn(kl), FadeIn(ks), run_time=3.0)
            self.play(FadeIn(st))
        self.wait(0.3)
        self.clear_scene()
