from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (DENSEC, F, HISTC, PART, TICKETC, load, ms, take_away)

KEEPC, CUTC = C.INTERVAL, GREY_D
METHODS = [("unstructured", r"$50\%$, \ any pattern", C.TRUE_P), ("magnitude_24", r"$2{:}4$, \ by size", C.BITS),
           ("wanda_24", r"$2{:}4$, \ by Wanda's score", C.HOT), ("random_24", r"$2{:}4$, \ at random", GREY_B)]


class Structured(VoiceoverScene):
    def construct(self):
        self.card()
        self.pattern()
        self.result()
        self.activations()
        self.cost()

    def card(self):
        card = chapter_card(15, r"Two in four, \ and sparse activations", r"What sparsity can hardware use?", part=PART)
        with self.voiceover("Chapter fifteen. Two in four, and sparse activations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pattern(self):
        p = load("prune24")
        W = np.asarray(p["example_w_s0"], float)[:4, :16]
        Mk = np.asarray(p["example_m_s0"], float)[:4, :16]
        top = np.abs(W).max()
        cells = VGroup()
        for i in range(W.shape[0]):
            for j in range(W.shape[1]):
                v = W[i, j]
                sq = Square(0.5, stroke_width=1, stroke_color=GREY_C, fill_color=C.TRUE_P if v > 0 else C.SURPRISE,
                            fill_opacity=0.15 + 0.8 * abs(v) / top)
                sq.move_to([j * 0.56 + (j // 4) * 0.18, -i * 0.56, 0])
                cells.add(sq)
        cells.move_to([0, 0.9, 0])
        cuts = VGroup(*[Cross(cells[i * W.shape[1] + j], stroke_color=WHITE, stroke_width=2, scale_factor=0.5)
                        for i in range(W.shape[0]) for j in range(W.shape[1]) if Mk[i, j] == 0])
        braces = VGroup(*[Brace(VGroup(*cells[g * 4:(g + 1) * 4]), UP, buff=0.08, color=GREY_B) for g in range(4)])
        bl = VGroup(*[label(r"keep $2$ of $4$", font_size=16, color=GREY_B).next_to(b_, UP, buff=0.05) for b_ in braces])
        head = label(r"our dense model's first feed-forward matrix: \ a corner \ (colour: sign; \ brightness: size)",
                     font_size=22, color=GREY_A).to_edge(UP, buff=0.3)
        facts = VGroup(
            label(r"unstructured: \ any $50\%$ \ \textemdash\ hard to speed up: \ the zeros are scattered", font_size=22,
                  color=C.TRUE_P),
            label(r"$2{:}4$: \ in every group of $4$ weights, \ exactly $2$ are zero: \ store $2$ values and $2$-bit "
                  r"positions", font_size=22, color=C.BITS),
            label(r"NVIDIA's A100 (2020) onward: \ sparse tensor cores run $2{:}4$ matrices at twice the rate \ (Part 17)",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Removing half the weights doesn't make a network twice as fast. The zeros are scattered, and a GPU "
            "reads and multiplies in dense blocks. <bookmark mark='a'/> Here's a corner of our dense model's first "
            "feed-forward matrix. <bookmark mark='b'/> In 2020 NVIDIA's A100 introduced a compromise: two in four. "
            "In every group of four consecutive weights, exactly two must be zero. <bookmark mark='c'/> Then the "
            "matrix can be stored as two values and two small position indices per group, and the sparse tensor "
            "cores of part seventeen multiply it at twice the dense rate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells))
            vo.wait_until("a")
            self.play(FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(braces), FadeIn(bl), FadeIn(facts[1]))
            self.play(LaggedStart(*[Create(c_) for c_ in cuts], lag_ratio=0.02), run_time=1.5)
            self.play(*[cells[i * W.shape[1] + j].animate.set_fill(opacity=0.05) for i in range(W.shape[0])
                        for j in range(W.shape[1]) if Mk[i, j] == 0])
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        p = load("prune24")
        seeds = [int(s) for s in p["seeds"]]
        dense = ms([p[f"dense_s{s}"] for s in seeds])
        vals = [(r"dense", ms([p[f"dense_s{s}"] for s in seeds]), DENSEC)]
        for k, nm, col in METHODS:
            vals.append((nm, ms([p[f"{k}_s{s}"] for s in seeds]), col))
        vals.append((r"$2{:}4$ by size, \ retrained", ms([p[f"magnitude_24_ft_s{s}"] for s in seeds]), C.BITS))
        vals.append((r"$2{:}4$ by Wanda, \ retrained", ms([p[f"wanda_24_ft_s{s}"] for s in seeds]), C.HOT))
        lo = dense[0] - 0.05
        hi_raw = max(v[1][2] for v in vals)
        hi = min(hi_raw, dense[0] + 2.5)
        W = 5.4
        rows = VGroup()
        for i, (nm, (m_, a_, b_), col) in enumerate(vals):
            y = 2.3 - i * 0.68
            w = W * (min(m_, hi) - lo) / (hi - lo)
            bar = Rectangle(width=max(w, 0.03), height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85)
            bar.move_to([-0.6 + w / 2, y, 0])
            rngl = Line([-0.6 + W * (min(a_, hi) - lo) / (hi - lo), y, 0], [-0.6 + W * (min(b_, hi) - lo) / (hi - lo), y, 0],
                        color=WHITE, stroke_width=2)
            nm_ = label(nm, font_size=20, color=col).move_to([-0.8, y, 0], aligned_edge=RIGHT)
            v = MathTex(f"{m_:.3f}" + (r"\,\to" if m_ > hi else ""), font_size=22, color=col).next_to(bar, RIGHT, buff=0.12)
            rows.add(VGroup(nm_, bar, rngl, v))
        head = label(r"held-out bits per character, \ every weight matrix pruned \ (three seeds: \ white lines)", font_size=22,
                     color=GREY_A).to_edge(UP, buff=0.3)
        foot = label(rf"Wanda: \ score $|W_{{ij}}| \cdot \|x_j\|$, \ the weight's size times its input's \ (Sun et al., 2023) "
                     rf"\ $\cdot$ \ retrained: \ ${int(p['ft_steps'])}$ steps with the pattern held", font_size=18,
                     color=GREY_A).to_edge(DOWN, buff=0.3)
        un, mg, wd, rd = (ms([p[f"{k}_s{s}"] for s in seeds])[0] for k in ("unstructured", "magnitude_24", "wanda_24", "random_24"))
        mf, wf = (ms([p[f"{k}_ft_s{s}"] for s in seeds])[0] for k in ("magnitude_24", "wanda_24"))
        v1 = (f"Pruning half the weights hurts: by size and in any pattern, {un - dense[0]:.2f} bits a character; "
              f"forced into two in four, {mg - dense[0]:.2f}; at random, {rd - dense[0]:.1f}. ")
        v2 = (f"Wanda's score, which weighs each weight by the size of the inputs it multiplies, does better: "
              f"{wd - dense[0]:.2f}. " if wd < mg - 0.01 else
              f"Wanda's score, which weighs each weight by the size of its inputs, does no better here: "
              f"{wd - dense[0]:.2f}. ")
        if (mf - dense[0]) < 0.5 * (mg - dense[0]):
            v3 = (f"A short retraining with the pattern held closes most of the gap: {mf - dense[0]:.2f} bits behind "
                  f"the dense model after {int(p['ft_steps'])} steps. ")
        else:
            v3 = f"A short retraining recovers part of it: {mf - dense[0]:.2f} bits behind after {int(p['ft_steps'])} steps. "
        with self.voiceover(
            "What does two in four cost? We pruned every weight matrix of our dense model, three seeds. "
            "<bookmark mark='a'/> " + v1 + "<bookmark mark='b'/> " + v2 + "<bookmark mark='c'/> " + v3
            + "That's NVIDIA's recipe: prune once, then retrain. For big language models, SparseGPT in 2023 pruned "
            "without retraining, using part nineteen's GPTQ machinery."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in (rows[1], rows[2], rows[4])], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[5:]], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def activations(self):
        a = load("actsparse")
        edges = np.asarray(a["edges"], float)
        H = np.asarray(a["hist_s0"], float)[0]
        H = H / H.sum()
        mids = (edges[:-1] + edges[1:]) / 2
        ax = Axes(x_range=[edges[0], edges[-1], 0.25], y_range=[0, float(H.max()) * 1.1, float(H.max()) / 2], x_length=6.0,
                  y_length=3.2, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.2, 0.2, 0])
        bars = VGroup(*[Rectangle(width=6.0 / len(H) * 0.9, height=max(3.2 * h / (H.max() * 1.1), 0.005), stroke_width=0,
                                  fill_color=C.MLP if abs(m) >= 0.1 else C.BITS, fill_opacity=0.85)
                        .move_to(ax.c2p(m, 0), aligned_edge=DOWN) for m, h in zip(mids, H)])
        xt = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1) for v in (0, 0.5, 1.0, 1.5)])
        xl = label(r"a feed-forward activation's value, \ after GELU \ (block 1)", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        small = np.asarray([a[f"small_s{s}"] for s in a["seeds"]], float)  # seeds, layers, cuts
        cut_i = list(a["cuts"]).index(0.1)
        sh = float(small[:, :, cut_i].mean())
        sl = label(rf"yellow: \ $|a| < 0.1$, \ ${100 * sh:.0f}\%$ of them", font_size=22, color=C.BITS).next_to(ax, UP, buff=0.15)
        fr = [float(f) for f in a["fracs"]]
        B = np.asarray([a[f"bits_s{s}"] for s in a["seeds"]], float)
        ax2 = Axes(x_range=[0, 1, 0.25], y_range=[float(B.min()) - 0.02, float(B.max()) + 0.02, 0.1], x_length=4.6, y_length=3.0,
                   tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.8, 0.2, 0])
        x2 = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=20, color=GREY_B).next_to(ax2.c2p(v, float(B.min()) - 0.02), DOWN, buff=0.1)
                      for v in (0, 0.5, 0.9)])
        l2 = label(r"smallest activations set to zero", font_size=20, color=GREY_A).next_to(x2, DOWN, buff=0.1)
        y2 = label(r"held-out bits", font_size=20, color=GREY_A).next_to(ax2, UP, buff=0.1).align_to(ax2, LEFT)
        c2 = VGroup(band(ax2, fr, B.min(0), B.max(0), C.MLP, 0.2), curve(ax2, fr, B.mean(0), C.MLP, 3),
                    *[Dot(ax2.c2p(x, y), radius=0.045, color=C.MLP) for x, y in zip(fr, B.mean(0))])
        i50, i90 = fr.index(0.5), fr.index(0.9)
        d50, d90 = float((B[:, i50] - B[:, 0]).mean()), float((B[:, i90] - B[:, 0]).mean())
        with self.voiceover(
            "Sparsity also hides in the activations. <bookmark mark='a'/> Here are our dense model's feed-forward "
            f"activations, after the GELU: {100 * sh:.0f} percent of them are smaller than a tenth. A neuron "
            "whose activation is zero needn't be computed, nor its weights read. <bookmark mark='b'/> So set the "
            "smallest ones to zero and see what it costs. "
            f"Zeroing half of them costs {d50:.3f} bits a character; zeroing ninety percent costs {d90:.2f}."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.01), FadeIn(sl), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ax2), FadeIn(x2), FadeIn(l2), FadeIn(y2))
            self.play(FadeIn(c2), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        a = load("actsparse")
        Z = [np.asarray(z, float) for z in a["relu_zeros"]]
        ax = Axes(x_range=[0, float(Z[0][-1, 0]), 250], y_range=[0, 1, 0.25], x_length=5.6, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4, 0.0, 0])
        yt = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0, 0.5, 1)])
        xl = label(r"training steps", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"ReLU units exactly zero \ (the lottery network)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        ln = VGroup(*[curve(ax, z[:, 0], z[:, 1 + j], col, 3) for z in Z for j, col in ((0, C.MLP), (1, C.BITS))])
        names = VGroup(label(r"first hidden layer", font_size=20, color=C.MLP), label(r"second hidden layer", font_size=20, color=C.BITS))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(ax, RIGHT, buff=0.3).shift(UP * 0.8)
        fin = float(np.mean([z[-1, 1:].mean() for z in Z]))
        cards = VGroup(
            history_card(2022, r"Zonglin Li et al.\ (Google)", rf"\textit{{The Lazy Neuron Phenomenon}}: \ only "
                         rf"${100 * F.LAZY['t5']:.0f}\%$ of T5's ReLU activations are nonzero", width=5.0, color=HISTC),
            history_card(2024, r"James Liu et al., \ TEAL", rf"zero the smallest ${int(100 * F.TEAL['sparsity'][0])}$--"
                         rf"${int(100 * F.TEAL['sparsity'][1])}\%$ of Llama's activations: \ decoding up to "
                         rf"${F.TEAL['speed'][1]}\times$ faster", width=5.0, color=HISTC),
        ).arrange(DOWN, buff=0.25).move_to([3.7, -0.6, 0])
        ta = take_away(r"sparsity pays when the hardware can skip it: \ experts, \ blocks, \ two in four", color=TICKETC, font_size=24)
        with self.voiceover(
            "With ReLU the zeros are exact. In the small ReLU network of the lottery chapter, "
            f"{100 * fin:.0f} percent of hidden units are exactly zero for a given input by the end of training. "
            "<bookmark mark='a'/> In 2022 Zonglin Li and colleagues found that only three percent of T5-Base's activations "
            "are nonzero, and called it the lazy neuron phenomenon. <bookmark mark='b'/> Modern models use GELU and "
            "SwiGLU, without exact zeros, but in 2024 TEAL zeroed the smallest forty to fifty percent of Llama's "
            "activations, with little loss, and decoded up to 1.8 times faster, because a zero means a column of "
            "weights that needn't be read. <bookmark mark='c'/> The common thread of this part: sparsity pays when "
            "the hardware can skip it."
        ) as vo:
            self.play(Create(ax), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(ln), FadeIn(names), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(ta))
        self.wait(0.3)
        self.clear_scene()
