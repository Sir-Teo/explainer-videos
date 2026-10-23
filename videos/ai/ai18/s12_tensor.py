from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (ACTS, COMM, F, GPU, GRADS, PART, WEIGHTS, load, spoken_int, take_away)

G1, G2 = "#6EA8FE", "#FFB86B"  # the two GPUs' halves


def mat(w, h, color, text, opacity=0.35, font_size=26):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=opacity)
    t = MathTex(text, font_size=font_size, color=WHITE).move_to(r)
    return VGroup(r, t)


class TensorParallel(VoiceoverScene):
    def construct(self):
        self.card()
        self.mlp()
        self.attention()
        self.measured()

    def card(self):
        card = chapter_card(11, r"Tensor parallelism", r"What if one layer is too big for one GPU?", part=PART)
        with self.voiceover("Chapter eleven. Tensor parallelism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def mlp(self):
        X = mat(1.0, 1.6, ACTS, r"X")
        A1, A2 = mat(0.8, 1.0, G1, r"A_1"), mat(0.8, 1.0, G2, r"A_2")
        A = VGroup(A1, A2).arrange(RIGHT, buff=0.0)
        Y1, Y2 = mat(0.8, 1.6, G1, r"Y_1"), mat(0.8, 1.6, G2, r"Y_2")
        Y = VGroup(Y1, Y2).arrange(RIGHT, buff=0.0)
        B1, B2 = mat(1.0, 0.8, G1, r"B_1"), mat(1.0, 0.8, G2, r"B_2")
        Bm = VGroup(B1, B2).arrange(DOWN, buff=0.0)
        Z1, Z2 = mat(1.0, 1.6, G1, r"Z_1"), mat(1.0, 1.6, G2, r"Z_2")
        eq1 = VGroup(X, MathTex(r"\times", font_size=34), A, MathTex(r"=", font_size=34), Y).arrange(RIGHT, buff=0.25)
        eq1.move_to([-3.4, 1.6, 0])
        f1 = label(r"split $A$ by columns: \ no communication", font_size=22, color=GREY_A).next_to(eq1, DOWN, buff=0.25)
        act = label(r"SwiGLU acts on each column alone: \ still local", font_size=22, color=GREY_A)
        act.next_to(f1, DOWN, buff=0.15)
        Ycopy = VGroup(Y1.copy(), Y2.copy()).arrange(RIGHT, buff=0.0)
        eq2 = VGroup(Ycopy, MathTex(r"\times", font_size=34), Bm, MathTex(r"=", font_size=34), Z1,
                     MathTex(r"+", font_size=34), Z2).arrange(RIGHT, buff=0.25)
        eq2.move_to([-3.0, -1.6, 0])
        f2 = label(r"split $B$ by rows: \ the partial sums must be added: \ all-reduce", font_size=22, color=COMM)
        f2.next_to(eq2, DOWN, buff=0.25)
        colors = {r"f": COMM, r"g": COMM}
        side = VGroup(
            label(r"Megatron-LM's MLP, \ on $t$ GPUs:", font_size=24, color=WHITE),
            cmath(r"Z", r"=", r"g\Big(\sum_{i} \mathrm{SwiGLU}\big(f(X)\,A_i\big)\, B_i\Big)", colors=colors, font_size=30),
            label(r"$f$: \ identity forward, \ all-reduce backward", font_size=20, color=COMM),
            label(r"$g$: \ all-reduce forward, \ identity backward", font_size=20, color=COMM),
            label(r"one all-reduce each way, \ per MLP", font_size=22, color=COMM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.7, 0.4, 0])
        hist = cite(r"Shoeybi et al., Megatron-LM (NVIDIA, 2019)", corner=DR, font_size=17)
        with self.voiceover(
            "When a single layer is too big or too slow for one GPU, split the layer itself. NVIDIA's Megatron-LM "
            "showed "
            "how in 2019. Take the MLP: Z equals X times A, a nonlinearity, then times B. <bookmark mark='a'/> Split "
            "A by "
            "columns, half on each GPU: each computes its half of Y from the whole input, with no communication. "
            "<bookmark mark='b'/> The nonlinearity acts on each column alone, so it stays local too. <bookmark "
            "mark='c'/> "
            "Now split B by rows. Each GPU multiplies its half of Y by its half of B and gets a full-size partial "
            "result; "
            "the answer is their sum, one all-reduce. <bookmark mark='d'/> So the whole MLP costs one all-reduce going "
            "forward, called g, and one going backward, f, for the gradient of the input both halves used."
        ) as vo:
            self.play(FadeIn(X), FadeIn(hist), FadeIn(eq1[1:].copy().set_opacity(0.15)))
            vo.wait_until("a")
            self.play(FadeIn(eq1[1:]), FadeIn(f1))
            vo.wait_until("b")
            self.play(FadeIn(act))
            vo.wait_until("c")
            self.play(TransformFromCopy(Y, Ycopy), FadeIn(eq2[1:]))
            self.play(FadeIn(f2))
            vo.wait_until("d")
            self.play(FadeIn(side, shift=LEFT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def attention(self):
        heads = VGroup()
        for h in range(8):
            col = G1 if h < 4 else G2
            box = RoundedRectangle(width=0.9, height=1.6, corner_radius=0.08, stroke_color=col, stroke_width=2,
                                   fill_color=col, fill_opacity=0.25)
            t = label(rf"head \\ ${h + 1}$", font_size=22, color=col).move_to(box)
            heads.add(VGroup(box, t))
        heads.arrange(RIGHT, buff=0.12).move_to([0, 1.7, 0])
        g1 = label(r"GPU 1: \ $Q$, $K$, $V$ of heads 1--4", font_size=22, color=G1)
        g2 = label(r"GPU 2: \ heads 5--8", font_size=22, color=G2)
        VGroup(g1, g2).arrange(RIGHT, buff=1.4).next_to(heads, DOWN, buff=0.25)
        outp = label(r"output projection split by rows: \ all-reduce", font_size=24, color=COMM).next_to(VGroup(g1, g2),
                                                                                                    DOWN, buff=0.4)
        per = VGroup(
            label(r"per layer: \ $2$ all-reduces forward, \ $2$ backward, \ of $b \times s \times h$ numbers each",
                  font_size=24, color=COMM),
            label(r"every layer, every micro-batch: \ only inside a node's NVLink domain", font_size=24, color=GPU),
            label(r"Llama 3: \ tensor parallel $8$, \ the innermost dimension", font_size=22, color=GREY_A),
            label(r"sequence parallelism (Korthikanti et al., 2022): \ all-reduce $\to$ reduce-scatter $+$ all-gather, "
                  r"\\ and the norms' activations split by position too", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(DOWN * 1.9)
        src = cite(r"Shoeybi et al.\ (2019); \ Korthikanti et al.\ (2022); \ Llama Team (2024), Sec.\ 3.3",
                   corner=DR, font_size=17)
        with self.voiceover(
            "Attention splits even more naturally: its heads are independent. <bookmark mark='a'/> Give each GPU the "
            "queries, keys and values of half the heads; each computes its heads alone, and the output projection, "
            "split "
            "by rows, ends in one all-reduce. <bookmark mark='b'/> So a transformer layer costs two all-reduces "
            "forward and "
            "two backward, each of a full activation: batch times sequence times width. <bookmark mark='c'/> That "
            "happens "
            "in every layer for every micro-batch, so tensor parallelism lives where bandwidth is highest, inside one "
            "machine's NVLink domain; Llama 3 used eight-way tensor parallelism, the innermost of its four dimensions. "
            "<bookmark mark='d'/> A refinement from 2022, sequence parallelism, turns each all-reduce into a "
            "reduce-scatter and an all-gather, and splits the remaining activations by position too."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(h_) for h_ in heads], lag_ratio=0.1), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(g1), FadeIn(g2))
            self.play(FadeIn(outp))
            vo.wait_until("b")
            self.play(FadeIn(per[0]))
            vo.wait_until("c")
            self.play(FadeIn(per[1]), FadeIn(per[2]))
            vo.wait_until("d")
            self.play(FadeIn(per[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        Pr = load("parallel")
        tp = Pr["tp"]
        head = label(r"one transformer block of our design, \ split by Megatron's rules", font_size=26)
        head.to_edge(UP, buff=0.5)
        cols = [r"GPUs", r"output: \\ largest difference", r"input \\ gradient", r"weight \\ gradients",
                r"all-reduces \\ (fwd, bwd)", r"weights \\ per GPU"]
        xs = [-5.9, -3.4, -0.9, 1.4, 3.8, 5.9]
        hd = VGroup(*[label(c, font_size=22, color=GREY_B).move_to([x, 1.9, 0]) for c, x in zip(cols, xs)])
        body = VGroup()
        for i, k in enumerate(("2", "4")):
            r = tp[k]
            y = 0.85 - 0.95 * i
            vals = [rf"${k}$", rf"${sci(r['err_y'], 1)}$", rf"${sci(r['err_gx'], 1)}$", rf"${sci(r['err_w'], 1)}$",
                    rf"${r['fwd_allreduce']}, \ {r['bwd_allreduce']}$", rf"$1/{r['full_weights'] // r['local_weights']}$"]
            body.add(VGroup(*[label(v, font_size=27, color=WHITE if j == 0 else GREY_A).move_to([x, y, 0])
                              for j, (v, x) in enumerate(zip(vals, xs))]))
        sc = label(rf"for scale: \ the output's largest entry is ${tp['2']['y_scale']:.1f}$", font_size=25,
                   color=GREY_A).move_to(DOWN * 1.5)
        tw = take_away(r"the same block, \ to rounding; \ two all-reduces each way", color=COMM, font_size=26)
        tag = note(r"computed: \ PyTorch's gloo backend, \ against the unsplit block", font_size=18).to_corner(DR,
                                                                                                         buff=0.2)
        worst = max(max(tp[k]["err_y"], tp[k]["err_gx"], tp[k]["err_w"]) for k in tp)
        if worst < 1e-4:
            verdict = (f"On two GPUs and on four, the split block's output and every gradient match the unsplit "
                       f"block's to within {worst:.6f}: rounding, from adding in a different order.")
        else:
            verdict = (f"The split block's results differ from the unsplit block's by up to {worst:.6f}: more than "
                       "rounding.")
        with self.voiceover(
            "We split one block of our own transformer this way, across two and then four processes, with an "
            "all-reduce for each f and g. <bookmark mark='a'/> " + verdict + " <bookmark mark='b'/> Each process "
            "holds a half, or a quarter, of the block's matrices, and the counts are Megatron's: two all-reduces "
            "forward, two backward."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hd), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in body], lag_ratio=0.5), FadeIn(sc))
            vo.wait_until("b")
            self.play(FadeIn(tw, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
