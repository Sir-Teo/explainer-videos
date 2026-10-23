from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (ACTS, C_COL, D_COL, F, GPU, GRADS, N_COL, OPT, PART, WEIGHTS, load, nbytes,
                                   spoken_int, take_away)


class Accounting(VoiceoverScene):
    def construct(self):
        self.card()
        self.six()
        self.measured()
        self.bytes_per_param()
        self.activations()

    def card(self):
        card = chapter_card(8, r"Counting FLOPs and bytes", r"How much arithmetic, and how much memory, does a "
                            r"training step need?", lit=(2020,), part=PART)
        with self.voiceover("Chapter eight. Counting FLOPs and bytes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def six(self):
        colors = {r"W": WEIGHTS, r"x": ACTS, r"y": ACTS, r"\delta": GRADS}
        rows = [
            cmath(r"\text{forward:}", r"\ y = W x", r"\Rightarrow", r"2", r"\text{ per weight per token}",
                  colors=colors, font_size=32),
            cmath(r"\text{backward, input:}", r"\ \delta_x = W^{\top} \delta_y", r"\Rightarrow", r"2",
                  r"\text{ per weight per token}", colors=colors, font_size=32),
            cmath(r"\text{backward, weights:}", r"\ \delta_W = \delta_y\, x^{\top}", r"\Rightarrow", r"2",
                  r"\text{ per weight per token}", colors=colors, font_size=32),
            cmath(r"C", r"\approx", r"6\,N\,D", colors={r"C": C_COL, r"N": N_COL, r"D": D_COL}, font_size=40),
        ]
        whys = [why(r"a multiply and an add", font_size=20), why(r"the error sent to the layer below", font_size=20),
                why(r"the weight's own gradient", font_size=20),
                why(r"$N$ weights, $D$ tokens; \ attention's own products extra", font_size=20)]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=0.6, buff=0.55, align_index=2, edge=6.9)
        with self.voiceover(
            "First, arithmetic. Almost all of a transformer's work is matrix products, one per weight matrix. "
            "<bookmark mark='a'/> Going forward, each weight multiplies one input and adds it in: two operations, "
            "per weight, per token. <bookmark mark='b'/> Going backward, each weight is used twice more. Once to "
            "send the error down to the layer below: two operations. <bookmark mark='c'/> And once to compute its "
            "own gradient: two more. <bookmark mark='d'/> Six operations per weight per token: the C of six N D, "
            "plus attention's own products, which grow with the length of the context."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        A = load("accounting")
        T = A["T"]
        items = [(r"forward", A["fwd"], ACTS), (r"backward", A["bwd"], GRADS), (r"both", A["both"], C_COL),
                 (r"$6 N T$", A["six"], N_COL)]
        mx = max(v for _, v, _ in items)
        bars = VGroup()
        for i, (t, v, c) in enumerate(items):
            w = 6.0 * v / mx
            b = Rectangle(width=w, height=0.45, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([-2.0 + w / 2, 1.6 - 0.7 * i, 0])
            nm = label(t, font_size=22, color=c).next_to(b, LEFT, buff=0.2).set_x(-2.2 - 0.0, direction=RIGHT)
            val = label(rf"${sci(v, 3)}$", font_size=22, color=c).next_to(b, RIGHT, buff=0.15)
            bars.add(VGroup(nm, b, val))
        head = label(rf"PyTorch's FLOP counter, \ one step of our model on ${T}$ tokens", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.45)
        model = label(rf"${A['d']}$ wide, \ ${A['layers']}$ layers, \ $N = {A['compute_params']:,}$ weights in its "
                      r"matrices".replace(",", "{,}"), font_size=22, color=N_COL).next_to(head, DOWN, buff=0.15)
        res = VGroup(
            label(rf"backward $/$ forward $= {A['ratio']:.2f}$", font_size=26, color=GRADS),
            label(rf"counted $/$ $6NT$ $= {A['both'] / A['six']:.4f}$", font_size=26, color=C_COL),
            label(rf"with attention's products counted too: \ $+{100 * A['attn_share'] / (1 - A['attn_share']):.0f}\%$ "
                  rf"at ${T}$ tokens", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0.6, -1.9, 0])
        tag = note(r"computed", font_size=18).to_corner(DR, buff=0.2)
        with self.voiceover(
            "We can check this on our own model, with PyTorch's FLOP counter, which counts the operations of every "
            f"matrix product in one training step on {T} tokens. <bookmark mark='a'/> The backward pass costs "
            f"{A['ratio']:.2f} times the forward pass. <bookmark mark='b'/> And the total is six times the weights "
            f"times the tokens, to within {100 * abs(A['both'] / A['six'] - 1):.2f} percent. <bookmark mark='c'/> "
            "Attention's own products, the scores and the weighted sum, add "
            f"{100 * A['attn_share'] / (1 - A['attn_share']):.0f} percent more at this length, and they grow with it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(model), FadeIn(tag),
                      LaggedStart(*[AnimationGroup(FadeIn(b_[0]), GrowFromEdge(b_[1], LEFT), FadeIn(b_[2]))
                                    for b_ in bars[:2]], lag_ratio=0.5))
            vo.wait_until("a")
            self.play(FadeIn(res[0]))
            vo.wait_until("b")
            self.play(*[AnimationGroup(FadeIn(b_[0]), GrowFromEdge(b_[1], LEFT), FadeIn(b_[2])) for b_ in bars[2:]])
            self.play(FadeIn(res[1]))
            vo.wait_until("c")
            self.play(FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bytes_per_param(self):
        P = load("published")
        parts = [(r"weights, \ BF16", 2, WEIGHTS), (r"gradients, \ BF16", 2, GRADS),
                 (r"FP32 master weights", 4, OPT), (r"Adam's first moment", 4, OPT), (r"Adam's second moment", 4, OPT)]
        blocks = VGroup()
        x = -6.0
        for t, b, c in parts:
            w = 0.62 * b
            r_ = Rectangle(width=w, height=0.8, stroke_width=1.5, stroke_color=BLACK, fill_color=c, fill_opacity=0.85)
            r_.move_to([x + w / 2, 1.9, 0])
            lab = label(rf"${b}$", font_size=24, color=BLACK).move_to(r_)
            nm = label(t, font_size=17, color=c).rotate(PI / 6).next_to(r_, DOWN, buff=0.1).shift(RIGHT * 0.25)
            blocks.add(VGroup(r_, lab, nm))
            x += w
        total = label(r"$= 16$ bytes per parameter", font_size=30, color=WHITE).next_to(blocks, RIGHT, buff=0.35)
        total.shift(UP * 0.35)
        m16 = P["mem16"]
        need = VGroup(
            label(rf"Llama 3.1 405B: \ ${nbytes(m16['llama3'])}$ \ $\to$ \ at least ${P['h100_needed']}$ H100s of "
                  r"$80$ GB, \ before a single activation", font_size=24, color=GPU),
            label(rf"DeepSeek-V3, $671$B: \ ${nbytes(m16['dsv3'])}$; \ Kimi K2, $1.04$T: \ ${nbytes(m16['k2'])}$",
                  font_size=24, color=GPU),
            label(r"DeepSeek-V3 keeps Adam's two moments in BF16", font_size=21, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 1.4)
        src = cite(r"Rajbhandari et al., ZeRO (2020), Sec.\ 3.1; \ DeepSeek-AI (2024), Sec.\ 3.3", font_size=17)
        with self.voiceover(
            "Now memory. Train in mixed precision, the standard recipe since 2018, and every parameter costs sixteen "
            "bytes. <bookmark mark='a'/> Two for the weight in bfloat16 and two for its gradient; <bookmark mark='b'/> "
            "then the optimizer's state, in thirty-two bits: a master copy of the weight, four bytes, and Adam's two "
            "running averages, four each. <bookmark mark='c'/> For Llama 3.1, sixteen bytes times 405 billion is "
            f"{m16['llama3'] / 1e12:.1f} terabytes: at least {P['h100_needed']} GPUs of eighty gigabytes just to hold "
            "the model, before any activations. <bookmark mark='d'/> Every byte saved here counts; DeepSeek-V3, for one, "
            "keeps Adam's averages in sixteen bits."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in blocks[:2]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in blocks[2:]], lag_ratio=0.4), run_time=2.0)
            self.play(FadeIn(total))
            vo.wait_until("c")
            self.play(FadeIn(need[0]), FadeIn(need[1]))
            vo.wait_until("d")
            self.play(FadeIn(need[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def activations(self):
        A, P = load("accounting"), load("published")
        mem = A["mem"]
        Ts = np.array([r["T"] for r in mem], float)
        top = max(r["unfused"] for r in mem) / 1e6
        g = axes([0, 1100], [0, math.ceil(top / 20) * 20], x_length=5.6, y_length=3.6,
                 xlabel=r"tokens in the sequence", ylabel=r"activations kept for the backward pass (MB)",
                 xticks=[0, 256, 512, 1024], yticks=[0, math.ceil(top / 20) * 20], center=[-3.3, -0.3, 0],
                 font_size=18)
        cols = {"fused": ACTS, "unfused": C.ATTN, "recompute": GREY_A}
        lines = VGroup()
        dots = VGroup()
        for k in ("unfused", "fused", "recompute"):
            ys = [r[k] / 1e6 for r in mem]
            lines.add(curve(g.ax, Ts, ys, cols[k], 3))
            dots.add(VGroup(*[Dot(g.ax.c2p(t, y), radius=0.05, color=cols[k]) for t, y in zip(Ts, ys)]))
        lg = legend([(C.ATTN, r"attention unfused: \ a $T \times T$ matrix per head"),
                     (ACTS, r"attention fused \ (as PyTorch runs it)"),
                     (GREY_A, r"each block recomputed in the backward pass")], font_size=18)
        lg.next_to(g, UP, buff=0.2).align_to(g, LEFT)
        res = VGroup(
            label(rf"fused: \ ${A['per_fused']:.1f}\,d$ numbers per token per layer", font_size=22, color=ACTS),
            label(rf"unfused: \ $+\,{A['quad_per_head']:.2f}\,T^2$ per head per layer", font_size=22, color=C.ATTN),
            label(rf"recomputed: \ ${A['per_recompute']:.1f}\,d$, \ for $+{100 * (A['ckpt_ratio'] - 1):.0f}\%$ "
                  r"arithmetic", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, 1.4, 0])
        al = P["act_llama"]
        big = VGroup(
            label(r"Korthikanti et al.'s count, \ $16$-bit, \ per layer and sequence:", font_size=20, color=GREY_A),
            cmath(r"s\,b\,h\,\Big(34 + 5\,\frac{a\,s}{h}\Big)", font_size=30),
            label(rf"at Llama 3.1 405B's shape, \ $s = {al['s']:,}$:".replace(",", "{,}") +
                  rf" \ ${nbytes(al['linear'])}$ per layer, \ ${nbytes(al['per_seq'])}$ for ${al['layers']}$ layers",
                  font_size=20, color=ACTS),
            label(rf"plus ${nbytes(al['attn'])}$ per layer if attention isn't fused", font_size=20, color=C.ATTN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.3, -1.6, 0])
        tag = note(r"computed: \ the tensors autograd saves, counted", font_size=18).to_corner(DR, buff=0.15)
        with self.voiceover(
            "The other big consumer of memory is the activations: what the forward pass keeps for the backward pass. "
            "We counted the tensors PyTorch's autograd saves for our model, at lengths from 64 to 1,024 tokens. "
            "<bookmark mark='a'/> With attention fused, as PyTorch runs it, the memory grows in a straight line: "
            f"{A['per_fused']:.1f} numbers per token per layer, in units of the width. <bookmark mark='b'/> Compute "
            "attention the textbook way, and it also keeps a T by T matrix for each head: a parabola. That quadratic term "
            "is what FlashAttention removes. <bookmark mark='c'/> Or keep only each block's input, and recompute the rest "
            "during the backward pass: one number per token per layer, for "
            f"{100 * (A['ckpt_ratio'] - 1):.0f} percent more arithmetic here, and at most a third more in general. "
            "<bookmark mark='d'/> At frontier scale this matters. Korthikanti and colleagues' count, at Llama 3.1's shape "
            "and eight thousand tokens: four and a half gigabytes per layer, more than half a terabyte per sequence."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines[1]), FadeIn(dots[1]), FadeIn(lg[1]), FadeIn(res[0]))
            vo.wait_until("b")
            self.play(Create(lines[0]), FadeIn(dots[0]), FadeIn(lg[0]), FadeIn(res[1]))
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(dots[2]), FadeIn(lg[2]), FadeIn(res[2]))
            vo.wait_until("d")
            self.play(FadeIn(big, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
