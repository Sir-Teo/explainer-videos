from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import fmt_int, A, GATED, HYB, PART, STATE, axes, band, curve, gib, load, said

LIN, ATT = C.INTERVAL, C.ATTN
TF_C, HY_C = C.ATTN, HYB

STACKS = [  # (model, year, layers in one repeating unit: L = a linear-time layer, A = full attention, its fast layer)
    (r"Jamba", 2024, "LLLALLLL", r"Mamba"),
    (r"MiniMax-01", 2025, "LLLLLLLA", r"lightning \\ attention"),
    (r"Nemotron-H", 2025, "LLLLLLLA", r"Mamba-2"),
    (r"Granite 4.0", 2025, "LLLLLLLLLA", r"Mamba-2"),
    (r"Qwen3-Next", 2025, "LLLA", r"Gated \\ DeltaNet"),
    (r"Kimi Linear", 2025, "LLLA", r"Kimi Delta \\ Attention"),
    (r"Qwen3.5", 2026, "LLLA", r"Gated \\ DeltaNet"),
    (r"Kimi K3", 2026, "LLLA", r"Kimi Delta \\ Attention"),
]
RATIO = {r"Nemotron-H": r"$4$ in $28$", r"Granite 4.0": r"$1$ in $10$", r"Kimi K3": r"$24$ in $93$"}


class Hybrid(VoiceoverScene):
    def construct(self):
        self.card()
        self.stacks()
        self.ours()
        self.samples()
        self.memory()

    def card(self):
        card = chapter_card(12, r"Hybrids", r"Why not have both?", part=PART)
        with self.voiceover("Chapter twelve. Hybrids."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def stacks(self):
        cols, atts = Group(), VGroup()
        for name, year, unit, lin_name in STACKS:
            reps = max(1, 20 // len(unit))
            seq = (unit * reps)[:20]
            blocks = VGroup(*[Rectangle(width=0.95, height=0.15, stroke_width=1, stroke_color=GREY_D,
                                        fill_color=ATT if ch == "A" else LIN, fill_opacity=0.85) for ch in seq])
            blocks.arrange(UP, buff=0.035)
            atts.add(*[b for b, ch in zip(blocks, seq) if ch == "A"])
            t = label(rf"{name} \\ ({year})", font_size=19, color=WHITE).next_to(blocks, UP, buff=0.15)
            n_att = unit.count("A")
            r = label(RATIO.get(name, rf"${n_att}$ in ${len(unit)}$"), font_size=18, color=ATT).next_to(blocks, DOWN, buff=0.12)
            ln = label(lin_name, font_size=15, color=LIN).next_to(r, DOWN, buff=0.08)
            cols.add(VGroup(blocks, t, r, ln))
        cols.arrange(RIGHT, buff=0.42, aligned_edge=DOWN).move_to(DOWN * 0.15)
        key = VGroup(VGroup(Square(0.25, fill_color=LIN, fill_opacity=0.85, stroke_width=0),
                            label(r"a linear-time layer: \ fixed-size memory", font_size=22, color=LIN)).arrange(RIGHT, buff=0.15),
                     VGroup(Square(0.25, fill_color=ATT, fill_opacity=0.85, stroke_width=0),
                            label(r"full attention: \ a growing cache", font_size=22, color=ATT)).arrange(RIGHT, buff=0.15))
        key.arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.3)
        tag = note(r"the share of attention layers, \ from each model's report or card; \ 20 layers drawn, \ schematic order",
                   font_size=17).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Fixed-size memories are cheap, but they forget; attention remembers everything exactly, at a price. "
            "So the newest models mix them. <bookmark mark='a'/> Jamba, from AI21 in 2024, put one attention layer "
            "among every eight, the rest Mamba; MiniMax-01, in January 2025, did the same with its lightning "
            "attention. <bookmark mark='b'/> NVIDIA's Nemotron-H kept attention in four of its twenty-eight mixing "
            "layers, and IBM's Granite 4.0 in one of ten. <bookmark mark='c'/> Qwen3-Next and Kimi Linear, in the "
            "autumn of 2025, used one attention layer in four, the other three running the gated delta rule. "
            "<bookmark mark='d'/> And in 2026 that layout reached the frontier's open models: Qwen3.5, from eight "
            "hundred million to nearly four hundred billion parameters, and Kimi K3, two point eight trillion, with "
            "twenty-four attention layers among ninety-three. <bookmark mark='e'/> The fast layers carry the gist of "
            "a long text cheaply; the few attention layers look up exact details when they're needed."
        ) as vo:
            self.play(FadeIn(key), FadeIn(tag))
            groups = [cols[0:2], cols[2:4], cols[4:6], cols[6:8]]
            for g_, m in zip(groups, "abcd"):
                vo.wait_until(m)
                self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in g_], lag_ratio=0.35), run_time=1.5)
            vo.wait_until("e")
            self.play(Indicate(atts, color=WHITE, scale_factor=1.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        r = load("lm")
        steps = np.asarray(r["curve_steps"], float)
        ct, ch = np.asarray(r["transformer_curve"]), np.asarray(r["hybrid_curve"])

        def sm(x, k=5):
            return np.array([np.convolve(row, np.ones(k) / k, mode="valid") for row in x])

        st = steps[2:-2]
        ct_, ch_ = sm(ct), sm(ch)
        lo = math.floor(min(ct_.min(), ch_.min()) * 2) / 2
        hi = min(math.ceil(max(ct_[:, 3:].max(), ch_[:, 3:].max()) * 2) / 2, lo + 4)
        g = axes([0, steps[-1]], [lo, hi], x_length=6.6, y_length=4.0, xlabel=r"training steps",
                 ylabel=r"training loss \ (nats a token, \ smoothed)", xticks=[0, steps[-1] / 2, steps[-1]],
                 yticks=[lo, (lo + hi) / 2, hi], center=[-2.6, -0.4, 0], xfmt=lambda v: f"{int(v)}")
        ax = g.ax
        bands = VGroup(band(ax, st, np.clip(ct_.min(0), lo, hi), np.clip(ct_.max(0), lo, hi), TF_C, 0.25),
                       band(ax, st, np.clip(ch_.min(0), lo, hi), np.clip(ch_.max(0), lo, hi), HY_C, 0.25))
        lines = VGroup(curve(ax, st, np.clip(ct_.mean(0), lo, hi), TF_C, 3), curve(ax, st, np.clip(ch_.mean(0), lo, hi), HY_C, 3))
        pt, ph = int(r["transformer_params"]), int(r["hybrid_params"])
        d, Lr = int(r["d"]), int(r["layers"])
        arch = VGroup(label(rf"transformer: \ {Lr} attention layers, \ rotary positions \ (${fmt_int(pt)}$ weights)",
                            font_size=19, color=TF_C),
                      label(rf"hybrid: \ 3 gated-delta layers, \ then attention, \ no positions \ (${fmt_int(ph)}$)",
                            font_size=19, color=HY_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.8, 2.3, 0])
        bt, bh = np.asarray(r["transformer_bits"]), np.asarray(r["hybrid_bits"])
        rows = VGroup(*[label(rf"{n}: \ ${b.mean():.3f}$ \ (seeds ${b.min():.3f}$--${b.max():.3f}$)", font_size=20, color=c_)
                        for n, b, c_ in ((r"transformer", bt, TF_C), (r"hybrid", bh, HY_C))]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rows.move_to([3.8, 0.0, 0])
        rh = label(r"bits per character, \ the scoreboard's passage", font_size=18, color=GREY_A).next_to(rows, UP, buff=0.12).align_to(rows, LEFT)
        tok = int(r["tokens"])
        cap = note(rf"width ${d}$, \ ${Lr}$ layers, \ $256$ tokens of context, \ ${tok / 1e6:.1f}$ million tokens of the novels "
                   r"each; \ $3$ seeds; \ band: \ min to max", font_size=16).to_edge(DOWN, buff=0.25)
        diff = bh.mean() - bt.mean()
        sep = bh.max() < bt.min() or bt.max() < bh.min()
        v = (f"The hybrid ends ahead: {bh.mean():.3f} bits per character on the scoreboard's passage, against "
             f"{bt.mean():.3f} for the transformer. " if diff < -0.005 else
             f"The transformer ends ahead: {bt.mean():.3f} bits per character on the scoreboard's passage, against "
             f"{bh.mean():.3f} for the hybrid. " if diff > 0.005 else
             f"They end level: {bt.mean():.3f} bits per character for the transformer, {bh.mean():.3f} for the hybrid. ")
        vs = ("The two sets of seeds don't overlap. " if sep else "The seeds overlap: the difference is within their spread. ")
        with self.voiceover(
            "We built a small one. Two models on the thirty novels, with the same width, depth, MLPs, data and "
            "steps, three seeds each. <bookmark mark='a'/> One is a plain transformer with four attention layers. "
            "The other, like Kimi Linear, has three gated-delta layers and then one attention layer with no "
            "positional encoding at all: the recurrent layers below it carry the order. <bookmark mark='b'/> Here "
            "they train. <bookmark mark='c'/> " + v + "<bookmark mark='e'/> " + vs + "<bookmark mark='d'/> Inside a window of 256 tokens the "
            "transformer's cache is small anyway; the hybrid's advantage is meant for long texts. That is the next "
            "chapter."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(arch[0]))
            self.play(FadeIn(arch[1]))
            vo.wait_until("b")
            self.play(FadeIn(bands), Create(lines[0]), Create(lines[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(rh), FadeIn(rows))
            vo.wait_until("d")
            self.play(Indicate(rows[1], color=HY_C, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def samples(self):
        r = load("lm")
        snaps = [int(s_) for s_ in r["snap_steps"]]
        sam = list(r["hybrid_samples"])
        vals = np.asarray(r["hybrid_snaps_val"])[0]
        prompt = str(r["prompt"])
        pl = data_text(prompt, font="DejaVu Sans Mono", font_size=24, color=GREY_A).to_edge(UP, buff=0.5)
        hl = label(r"the hybrid, seed $0$, \ sampled during training", font_size=22, color=HY_C).next_to(pl, DOWN, buff=0.2)
        picks = [0, len(snaps) // 3, 2 * len(snaps) // 3, len(snaps) - 1]
        boxes = VGroup()
        for i in picks:
            boxes.add(VGroup(label(rf"step ${snaps[i]}$: \ held-out loss ${vals[i]:.2f}$", font_size=18, color=GREY_B),
                             said(prompt + sam[i], chars=60, font_size=17, max_lines=2, box_color=HY_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        boxes.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(hl, DOWN, buff=0.3)
        if boxes.height > 5.0:
            boxes.height = 5.0
            boxes.next_to(hl, DOWN, buff=0.3)
        with self.voiceover(
            "And here is the hybrid's writing as it learns, continuing the same opening at four moments of "
            f"training. <bookmark mark='a'/> At step {snaps[picks[0]]}, noise. <bookmark mark='b'/> Then words, "
            "<bookmark mark='c'/> then something like sentences: <bookmark mark='d'/> about as far as "
            f"{int(r['hybrid_params']) / 1e6:.1f} million weights and {int(r['tokens']) / 1e6:.1f} million tokens can go."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(hl))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(boxes[k], shift=UP * 0.1))
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
