from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import (A, K, PART, Q, V, curve, framed, heat_image, load, matrix_box, signed_image)

OV = C.VALUE


class Heads(VoiceoverScene):
    def construct(self):
        self.card()
        self.bilinear()
        self.spectra()
        self.many()

    def card(self):
        card = chapter_card(4, r"Heads are low-rank maps", r"What does one head compute, written as matrices?",
                            lit=(2017,), part=PART)
        with self.voiceover("Chapter four. Heads are low-rank maps."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def bilinear(self):
        h = load("heads")
        d, dh = int(h["d"]), int(h["dh"])
        colors = {r"x_i": Q, r"x_j": K, r"W_Q": Q, r"W_K": K, r"W_{QK}": A}
        rows = [
            cmath(r"q_i \cdot k_j", r"=", r"(W_Q x_i)^\top (W_K x_j)", font_size=36, colors=colors),
            cmath(r"q_i \cdot k_j", r"=", r"x_i^\top\, W_Q^\top W_K\, x_j", font_size=36, colors=colors),
            cmath(r"q_i \cdot k_j", r"=", r"x_i^\top\, W_{QK}\, x_j", font_size=36, colors=colors),
            cmath(r"\operatorname{rank} W_{QK}", r"\le", rf"d_h = {dh}", font_size=36, colors=colors),
        ]
        whys = [why(r"$q = W_Q x$, \ $k = W_K x$"), why(r"transpose of a product"),
                why(rf"one ${d} \times {d}$ matrix: \\ a bilinear form on the stream"),
                why(rf"it factors through ${dh}$ numbers")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-2.6, buff=0.55, edge=6.9)
        u = 0.02
        wq = matrix_box(d, dh, u, Q, fill=Q, label_tex=r"W_Q^\top", font_size=22)
        wk = matrix_box(dh, d, u, K, fill=K, label_tex=r"W_K", font_size=22)
        eq = MathTex(r"=", font_size=40)
        wqk = matrix_box(d, d, u, A, fill=A, label_tex=r"W_{QK}", font_size=26)
        prod = VGroup(wq, wk, eq, wqk).arrange(RIGHT, buff=0.3).move_to([-2.2, -1.95, 0])
        wk.align_to(wq, UP)
        dims = VGroup(MathTex(rf"{d} \times {dh}", font_size=20, color=Q).next_to(wq, DOWN, buff=0.1),
                      MathTex(rf"{dh} \times {d}", font_size=20, color=K).next_to(wk, DOWN, buff=0.1),
                      MathTex(rf"{d} \times {d}", font_size=20, color=A).next_to(wqk, DOWN, buff=0.1))
        rowsov = cmath(r"W_{OV}", r"=", r"W_O\, W_V", font_size=34, colors={r"W_{OV}": OV})
        ovl = label(r"what the head writes back, \\ given what it read: \\ also rank $\le " + str(dh) + r"$",
                    font_size=22, color=GREY_A)
        ovg = VGroup(rowsov, ovl).arrange(DOWN, buff=0.2).move_to([4.2, -2.1, 0])
        cite_ = cite(r"N.~Elhage et al., \textit{A Mathematical Framework for Transformer Circuits} (2021)", corner=DR)
        with self.voiceover(
            "Let's write one head as matrices. Character i's query is W Q times its vector in the residual stream, "
            "and character j's key is W K times its vector. <bookmark mark='a'/> Move the transpose inside, "
            "<bookmark mark='b'/> and the score is x i, times one matrix, times x j: a single "
            f"{d} by {d} matrix, W Q K, that compares two positions of the stream. "
            f"<bookmark mark='c'/> But it is a product of a tall, thin {d} by {dh} matrix and a short, wide one, so "
            f"its rank is at most {dh}. A head can only compare along {dh} directions of the stream. "
            "<bookmark mark='d'/> The same holds for what the head moves: W O times W V, also of rank at most "
            f"{dh}. Nelson Elhage, Chris Olah and colleagues called these the QK and OV circuits: one decides "
            "where to look, the other what to carry."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(wqk), FadeIn(dims[2]))
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(wq), FadeIn(wk), FadeIn(eq), FadeIn(dims[:2]))
            vo.wait_until("d")
            self.play(FadeIn(ovg), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectra(self):
        h = load("heads")
        d, dh = int(h["d"]), int(h["dh"])
        L, H = int(h["L"]), int(h["H"])
        sv = np.asarray(h["sv_qk"])  # layer, head, d
        rank, lrank = int(h["rank_qk"]), int(h["layer_rank"])
        k90 = np.asarray(h["k90_qk"])
        ln_txt = (f"That is every direction but one, the average of the {d} numbers, which layer norm removes before "
                  "any head sees it." if lrank == d - 1 else "That is close to the whole stream.")
        g = axes([0, d, 32], [-17, 1, 4], x_length=6.6, y_length=3.8, xlabel=r"direction, \ largest first",
                 ylabel=r"singular values of $W_{QK}$, \ relative to the largest", xticks=[0, 32, 64, 96, 128],
                 yticks=[-16, -12, -8, -4, 0], yfmt=lambda v: f"10^{{{int(v)}}}", center=[-3.0, -0.4, 0])
        ax = g.ax
        lines = VGroup()
        for l_ in range(L):
            for hh in range(H):
                rel = np.log10(np.maximum(sv[l_, hh] / sv[l_, hh, 0], 1e-17))
                lines.add(curve(ax, np.arange(1, d + 1), rel, interpolate_color(ManimColor(A), ManimColor(Q), l_ / max(L - 1, 1)),
                                1.6).set_stroke(opacity=0.8))
        cut = DashedLine(ax.c2p(dh, -17), ax.c2p(dh, 1), color=WHITE, stroke_width=1.5)
        cutl = MathTex(rf"d_h = {dh}", font_size=24).next_to(ax.c2p(dh, -6), RIGHT, buff=0.12)
        fl = label(r"rounding error", font_size=20, color=GREY_B).move_to(ax.c2p(80, -14.5))
        tag = note(rf"our transformer: \ all ${L * H}$ heads, \ layer norm folded in").to_corner(DL, buff=0.3)
        ex = np.asarray(h["qk_example"])
        img = framed(signed_image(ex, 2.6, 2.6)).move_to([4.4, 1.2, 0])
        il = label(rf"one head's $W_{{QK}}$: \ ${d} \times {d}$ numbers", font_size=20, color=GREY_A).next_to(img, UP, buff=0.12)
        facts = VGroup(
            label(rf"nonzero directions: \ at most ${rank}$", font_size=22, color=A),
            label(rf"$90\%$ of a head's size: \ ${int(k90.min())}$ to ${int(k90.max())}$ directions", font_size=22, color=GREY_A),
            label(rf"a layer's ${H}$ heads together: \ rank ${lrank}$", font_size=22, color=Q),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, -1.7, 0])
        keep_in_frame(facts)
        with self.voiceover(
            f"Here are the singular values of W Q K for every one of our transformer's {L * H} heads, largest "
            f"first, on a log scale. <bookmark mark='a'/> Exactly {rank} of them are real; after that the values "
            "fall off a cliff, to the size of the computer's rounding error. <bookmark mark='b'/> And even within "
            f"those {dh}, a head is lopsided: {int(k90.min())} to {int(k90.max())} directions hold ninety percent of "
            f"its size. <bookmark mark='c'/> Add a layer's {H} heads together and the rank is {lrank}. "
            "<bookmark mark='d'/> " + ln_txt + " Between them, the heads cover the stream, but each one looks through a narrow slit."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(img), FadeIn(il))
            self.play(LaggedStart(*[Create(c_) for c_ in lines], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(cut), FadeIn(cutl), FadeIn(fl), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def many(self):
        t = load("tf")
        maps = np.asarray(t["maps"])
        H, dh, d = int(t["heads"]), int(t["d"]) // int(t["heads"]), int(t["d"])
        S = 2.5
        imgs = Group(*[framed(heat_image(maps[0, hh], S, S, color=A, gamma=0.4, mask_upper=True)) for hh in range(H)])
        imgs.arrange(RIGHT, buff=0.35).move_to([0, 0.75, 0])
        hl = VGroup(*[label(rf"head {hh + 1}", font_size=20, color=GREY_B).next_to(m, UP, buff=0.1)
                      for hh, m in enumerate(imgs)])
        under = note(r"layer 1 of our transformer, \ on a sentence of the passage").next_to(imgs, UP, buff=0.5)
        eq = cmath(r"\operatorname{Attn}(x)_i", r"=", r"\sum_{h=1}^{" + str(H) + r"}", r"\sum_j", r"A^{h}_{ij}",
                   r"\, W_{OV}^{h}\, x_j", font_size=36, colors={r"A^{h}_{ij}": A, r"\, W_{OV}^{h}\, x_j": OV})
        eq.move_to([0, -2.35, 0])
        eql = label(r"each head: \ its own pattern $A^h$, \ its own low-rank move $W^h_{OV}$", font_size=22,
                    color=GREY_A).next_to(eq, DOWN, buff=0.2)
        same = label(rf"${H}$ heads of ${dh}$, \ or one of ${d}$: \ the same $4d^2 = {4 * d * d:,}$ weights".replace(",", "{,}"),
                     font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cite_ = cite(r"S.~Bhojanapalli et al., \textit{Low-Rank Bottleneck in Multi-head Attention Models} (2020)",
                     corner=DR)
        n = maps.shape[-1]
        idx = np.arange(n)
        prev = [float(np.mean([maps[0, hh, i, i - 1] for i in range(8, n)])) for hh in range(H)]
        dist = [float(np.mean([(maps[0, hh, i, : i + 1] * (i - idx[: i + 1])).sum() for i in range(8, n)]))
                for hh in range(H)]
        hp, hw = int(np.argmax(prev)), int(np.argmax(dist))
        stats = VGroup(*[label(rf"one back: ${100 * prev[hh]:.0f}\%$ \\ mean distance ${dist[hh]:.1f}$", font_size=18,
                               color=GREY_A).next_to(imgs[hh], DOWN, buff=0.15) for hh in range(H)])
        looks = (f"head {hp + 1} puts {prev[hp]:.0%} of its weight on the character just before, while head "
                 f"{hw + 1} looks {dist[hw]:.0f} characters back on average." if hp != hw else
                 f"head {hp + 1} puts {prev[hp]:.0%} of its weight on the character just before, while the others "
                 f"look between {min(dist):.0f} and {max(dist):.0f} characters back on average.")
        with self.voiceover(
            f"So why split attention into {H} narrow heads, instead of one head of {d}? It costs the same: "
            f"{H} heads of {dh} have exactly as many weights as one of {d}. <bookmark mark='a'/> But each head "
            "has its own softmax, and so its own pattern. One head can make only one weighted average per "
            f"character; the {H} heads of our first layer make {H} different ones at once: " + looks
            + " <bookmark mark='b'/> The layer's output is a sum over heads of "
            "pattern times low-rank move. <bookmark mark='c'/> There is a price: a narrow head cannot express "
            "every pattern. Srinadh Bhojanapalli and colleagues called it the low-rank bottleneck in 2020. Real "
            "models live with it, and spend their savings elsewhere: Part 15 shows how they share or compress "
            "the keys and values to make the memory of past tokens smaller."
        ) as vo:
            self.play(FadeIn(same), LaggedStart(*[FadeIn(m) for m in imgs], lag_ratio=0.15), FadeIn(hl), FadeIn(under))
            vo.wait_until("a")
            self.play(FadeIn(stats), Indicate(hl[hp], color=A), Indicate(hl[hw], color=A))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(eql))
            vo.wait_until("c")
            self.play(FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()
