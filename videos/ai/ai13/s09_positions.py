from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import (A, K, PART, POS, POS_COLORS, Q, V, curve, framed, heat_image, load, signed_image)
from videos.ai.ai13.compute import alibi_slopes

SINC, ALIBIC, NOPEC = POS_COLORS["sin"], POS_COLORS["alibi"], POS_COLORS["nope"]


class Positions(VoiceoverScene):
    def construct(self):
        self.card()
        self.sinusoids()
        self.relative()
        self.nope()

    def card(self):
        card = chapter_card(8, r"Where is each character?", r"How does attention, blind to order, learn positions?",
                            lit=(2017,), part=PART)
        with self.voiceover("Chapter eight. Where is each character?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def sinusoids(self):
        r = load("rope")
        pe = np.asarray(r["pe"])  # position, dimension
        dot = np.asarray(r["pe_dot"])
        k, dev = int(r["sin_k"]), float(r["sin_dev"])
        img = framed(signed_image(pe.T, 5.4, 2.0, pos=SINC, neg=C.SURPRISE)).move_to([-3.3, 1.35, 0])
        il = label(r"position $t \to$ \ ($64$ positions, \ $16$ numbers each)", font_size=20, color=GREY_A)
        il.next_to(img, DOWN, buff=0.12)
        f = cmath(r"PE(t)_{2i}", r"=", r"\sin(t\,\omega_i), \quad PE(t)_{2i+1} = \cos(t\,\omega_i), \quad "
                  r"\omega_i = 10000^{-2i/d}", font_size=28).move_to([0, 3.35, 0])
        rows = [
            cmath(r"\begin{pmatrix}\sin (t+k)\omega \\ \cos (t+k)\omega\end{pmatrix}", r"=",
                  r"\begin{pmatrix}\cos k\omega & \sin k\omega \\ -\sin k\omega & \cos k\omega\end{pmatrix}",
                  r"\begin{pmatrix}\sin t\omega \\ \cos t\omega\end{pmatrix}", font_size=28),
        ]
        rows[0].move_to([3.2, 1.3, 0])
        rw = label(r"angle addition: \ the same rotation for every $t$", font_size=20, color=GREY_A).next_to(rows[0], DOWN, buff=0.15)
        chk = label(rf"checked for $k = {k}$ and $t$ up to $300$: \ off by ${sci(dev)}$", font_size=20, color=C.TRUE_P)
        chk.next_to(rw, DOWN, buff=0.1)
        dimg = framed(heat_image(dot - dot.min(), 2.3, 2.3, color=SINC, gamma=1.0)).move_to([-4.6, -2.15, 0])
        dl = label(r"$PE(t) \cdot PE(s)$: \\ depends only on $t - s$", font_size=20, color=GREY_A).next_to(dimg, RIGHT, buff=0.25)
        learned = label(r"GPT-2 (2019): \ a learned vector for each of $1{,}024$ positions; \\ "
                        r"position $1{,}025$ simply has none", font_size=22, color=GREY_A).move_to([3.3, -2.15, 0])
        cite_ = cite(r"A.~Vaswani et al.\ (2017), \S3.5", corner=DR)
        with self.voiceover(
            "Chapter five ended with a problem: attention cannot tell 'dog bites man' from 'man bites dog'. The "
            "2017 paper's answer was to add a position signal to each character's vector before the first layer. "
            "<bookmark mark='a'/> Pairs of numbers oscillate at different speeds, a sine and a cosine each, from one "
            "turn every six positions to one in tens of thousands. <bookmark mark='b'/> Why sines? Because of the "
            "angle-addition formulas: moving k positions along is the same rotation of each pair, wherever you "
            "start, so a layer can learn to look a fixed distance back with one fixed matrix. "
            f"<bookmark mark='c'/> Checked numerically, it holds to rounding error. And the dot product of two "
            "positions depends only on how far apart they are. <bookmark mark='d'/> GPT-2 went another way and "
            "simply learned one vector per position, 1,024 of them. That works, but a position it never saw has no "
            "vector at all."
        ) as vo:
            self.play(FadeIn(f), FadeIn(cite_), FadeIn(img), FadeIn(il))
            vo.wait_until("a")
            self.play(Indicate(img, scale_factor=1.03))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(rw))
            vo.wait_until("c")
            self.play(FadeIn(chk), FadeIn(dimg), FadeIn(dl))
            vo.wait_until("d")
            self.play(FadeIn(learned))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def relative(self):
        H = 4
        sl = alibi_slopes(H)
        n = 24
        i = np.arange(n)
        D = np.clip(i[:, None] - i[None], 0, None).astype(float)
        imgs = Group()
        for h in range(H):
            B = np.where(np.tril(np.ones((n, n), bool)), np.exp(-sl[h] * D), 0.0)  # e^{bias}: how much a key keeps
            imgs.add(framed(heat_image(B, 2.0, 2.0, color=ALIBIC, gamma=1.0, mask_upper=True)))
        imgs.arrange(RIGHT, buff=0.35).move_to([0, -1.35, 0])
        hl = VGroup(*[MathTex(rf"m_{h + 1} = 2^{{-{8 * (h + 1) // H}}}", font_size=24, color=ALIBIC).next_to(m, UP, buff=0.12)
                      for h, m in enumerate(imgs)])
        cap = note(r"$e^{-m (i - j)}$: \ how much each head's bias leaves of a key $i - j$ back").next_to(imgs, DOWN, buff=0.15)
        f = cmath(r"s_{ij}", r"=", r"\frac{q_i \cdot k_j}{\sqrt{d}}", r"-", r"m_h\,(i - j)", font_size=40,
                  colors={r"m_h\,(i - j)": ALIBIC}).move_to([0, 2.5, 0])
        fl = label(r"no position vectors at all: \ a penalty growing with distance, \ a different slope per head",
                   font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.25)
        hist = label(r"relative positions: \ Shaw et al.\ (2018); \ T5's learned buckets (2019); \ "
                     r"ALiBi, \ Press, Smith \& Lewis (2021)", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "A different idea: forget absolute positions and tell attention only how far apart two characters are. "
            "In 2018 Peter Shaw and colleagues learned a vector for each distance, and T5 learned a bias for each "
            "range of distances. <bookmark mark='a'/> In 2021 Ofir Press, Noah Smith and Mike Lewis made it as "
            "simple as possible. ALiBi adds no position vectors at all: it subtracts from each score a penalty "
            "proportional to the distance. <bookmark mark='b'/> Each head gets its own slope, from a geometric "
            "sequence: steep heads look only at the last few characters, shallow ones far back. They reported "
            "that a model trained on 1,024 tokens read 2,048 as well as a model trained at that length."
        ) as vo:
            self.play(FadeIn(f), FadeIn(hist), LaggedStart(*[FadeIn(m) for m in imgs], lag_ratio=0.2), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(fl), Indicate(f[3:], color=ALIBIC))
            vo.wait_until("b")
            self.play(FadeIn(hl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nope(self):
        rows = [
            cmath(r"p_{tj}", r"=", r"\tfrac{1}{t} \quad (j = 1 \dots t)", font_size=34, colors={r"p_{tj}": A}),
            cmath(r"\operatorname{out}_t", r"=", r"\tfrac{1}{t}\textstyle\sum_{j \le t} v_j", font_size=34,
                  colors={r"\operatorname{out}_t": V}),
            cmath(r"v_1 = e,\ \ v_{j>1} \perp e", r"\;\Rightarrow\;", r"\operatorname{out}_t \cdot e = \tfrac{1}{t}",
                  font_size=34),
        ]
        whys = [why(r"a head that attends evenly \\ to everything it may see"), why(r"the average of the past"),
                why(r"a marked first token: \\ the average reveals $t$")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-3.0, buff=0.6, edge=6.9)
        g = axes([1, 32, 8], [0, 1.05, 0.5], x_length=4.6, y_length=2.4, xlabel=r"position $t$",
                 ylabel=r"$\operatorname{out}_t \cdot e$", xticks=[1, 8, 16, 24, 32], yticks=[0, 0.5, 1],
                 center=[-3.2, -2.0, 0])
        ts = np.arange(1, 33)
        c_ = VGroup(*[Dot(g.ax.c2p(t, 1 / t), radius=0.045, color=NOPEC) for t in ts])
        tag = note(r"illustration").next_to(g, RIGHT, buff=0.2).align_to(g, DOWN)
        nn_ = 16
        U = np.tril(np.ones((nn_, nn_))) / np.arange(1, nn_ + 1)[:, None]
        uimg = framed(heat_image(U, 2.4, 2.4, color=A, gamma=0.6, mask_upper=True)).move_to([4.6, 1.2, 0])
        ul = label(r"even attention over the past: \\ row $t$ holds $t$ weights of $1/t$", font_size=18,
                   color=GREY_A).next_to(uimg, DOWN, buff=0.15)
        facts = VGroup(
            label(r"no positions (NoPE): \ the causal mask leaks them", font_size=22, color=NOPEC),
            label(r"Haviv et al.\ (2022): \ such models still learn positions", font_size=20, color=GREY_A),
            label(r"Kazemnejad et al.\ (2023): \ and generalize to longer inputs \\ better than explicit schemes "
                  r"on reasoning tasks", font_size=20, color=GREY_A),
            label(r"Llama 4 (2025): \ layers without positions, \\ interleaved with rotary ones", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, -2.2, 0])
        keep_in_frame(facts)
        with self.voiceover(
            "And the most surprising answer: give no positions at all. A decoder still has its causal mask, and "
            "the mask leaks position. <bookmark mark='a'/> Take a head that spreads its attention evenly over "
            "everything it may see: at position t, each of the t keys gets one over t. <bookmark mark='b'/> Its "
            "output is the average of the past. <bookmark mark='c'/> If the first token is marked, the share of "
            "that mark in the average is one over t, and a later layer can read the position off it. "
            "<bookmark mark='d'/> Adi Haviv and colleagues found in 2022 that language models without position "
            "signals still learn where they are, and Amirhossein Kazemnejad and colleagues that, on reasoning "
            "tasks, they generalize to longer inputs better than models with explicit positions. Meta's Llama 4 "
            "interleaves layers without positions among rotary ones. Rotary positions, the answer nearly every "
            "model uses today, are next."
        ) as vo:
            step(0)
            self.play(FadeIn(uimg), FadeIn(ul))
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=A))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d_) for d_ in c_], lag_ratio=0.03), FadeIn(tag))
            vo.wait_until("d")
            self.play(FadeOut(uimg), FadeOut(ul))
            self.play(LaggedStart(*[FadeIn(f_, shift=UP * 0.1) for f_ in facts], lag_ratio=0.5), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()
