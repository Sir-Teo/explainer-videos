from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (ACTS, BASE_C, COMM, C_COL, F, FULL_C, GPU, PART, ShardGrid, hbars, load, node_box,
                                   play_fly, spoken_int, take_away)

QC, KVC = C.QUERY, C.KEY


class Context(VoiceoverScene):
    def construct(self):
        self.card()
        self.ring()
        self.balance()
        self.experts()
        self.four_d()
        self.mfu()

    def card(self):
        card = chapter_card(13, r"Context, experts, and utilization", r"The last two cuts, and how much of the "
                            r"hardware a run really uses", part=PART)
        with self.voiceover("Chapter thirteen. Context, experts, and utilization."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def ring(self):
        Pr = load("parallel")
        R = Pr["ring"]
        p = Pr["p"]
        g = ShardGrid(p, 2, cell=0.66, row_gap=0.3).move_to([-3.4, -1.0, 0])
        for r in range(p):
            g.set(r, 0, QC, 0.85)
            g.set(r, 1, KVC, 0.85)
        cols = g.label_cols([r"$Q$", r"$K, V$"], font_size=22)
        seq = VGroup(*[Rectangle(width=2.2, height=0.6, stroke_width=1, stroke_color=BLACK, fill_color=ACTS,
                                 fill_opacity=0.35 + 0.15 * k) for k in range(p)]).arrange(RIGHT, buff=0)
        seq.to_edge(UP, buff=0.9)
        sl = label(rf"one sequence of ${R['T']}$ tokens, \ cut into ${p}$ blocks", font_size=24, color=ACTS)
        sl.next_to(seq, UP, buff=0.12)
        owners = VGroup(*[label(rf"GPU {k}", font_size=20, color=GPU).next_to(b_, DOWN, buff=0.1)
                          for k, b_ in enumerate(seq)])
        steps_ = VGroup(
            label(r"each GPU keeps its block of queries", font_size=22, color=QC),
            label(r"the key--value blocks travel round the ring", font_size=22, color=KVC),
            label(r"each new block is folded in with the online softmax: \\ a running maximum and a running sum",
                  font_size=22, color=GREY_A),
            label(rf"measured, \ ${p}$ processes: \ largest difference from full attention ${sci(R['err'], 1)}$",
                  font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([2.9, -1.0, 0])
        src = cite(r"Liu, Zaharia \& Abbeel, Ring Attention (2023); \ Milakov \& Gimelshein (2018)", corner=DR,
                   font_size=17)
        with self.voiceover(
            "Two more ways to cut. The first is for long sequences: at a million tokens, one sequence's activations no "
            "longer fit on a GPU, so split the sequence itself: context parallelism. <bookmark mark='a'/> Each GPU keeps "
            "one block of positions. Everything in a transformer is per position, except attention, which needs every "
            "key. <bookmark mark='b'/> Ring attention, from Berkeley in 2023: each GPU keeps its queries, and the blocks "
            "of keys and values travel round the ring, one hop per step. <bookmark mark='c'/> Each arriving block is "
            "folded in with the online softmax, a running maximum and a running sum, as in FlashAttention, so the answer "
            "is exact. <bookmark mark='d'/> We ran it on four processes, 256 tokens in four blocks: the result matches "
            f"full attention to {R['err']:.7f}."
        ) as vo:
            self.play(FadeIn(seq), FadeIn(sl), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(o_, shift=DOWN * 0.1) for o_ in owners], lag_ratio=0.2))
            self.play(FadeIn(g), FadeIn(cols))
            vo.wait_until("b")
            self.play(FadeIn(steps_[0]), FadeIn(steps_[1]))
            for s in range(p - 1):
                play_fly(self, g, [(r, 1, (r + 1) % p, 1) for r in range(p)], run_time=0.6, color_after=KVC)
            vo.wait_until("c")
            self.play(FadeIn(steps_[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps_[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def balance(self):
        Pr = load("parallel")
        p = Pr["p"]
        n = 2 * p

        def tri(assign, center, title):
            cell = 0.42
            g = VGroup()
            for q in range(n):
                for k in range(n):
                    if k <= q:
                        owner = assign[q]
                        sq = Square(cell, stroke_width=0.6, stroke_color=BLACK,
                                    fill_color=[GPU, C.PROB, COMM, C.EMBED][owner], fill_opacity=0.85)
                        sq.move_to([k * cell, -q * cell, 0])
                        g.add(sq)
            g.move_to(center)
            t = label(title, font_size=20, color=GREY_A).next_to(g, UP, buff=0.2)
            return VGroup(g, t)

        contiguous = [q // 2 for q in range(n)]
        zig = [0] * n
        for r in range(p):
            zig[r] = r
            zig[n - 1 - r] = r
        a = tri(contiguous, [-3.3, -0.4, 0], r"contiguous blocks")
        b = tri(zig, [3.3, -0.4, 0], r"chunk $i$ and chunk $2p - 1 - i$")
        ca = label(r"work per GPU: \ " + r", \ ".join(f"${2 * w}$" for w in Pr["contiguous"]) +
                   r" \ (in half-blocks)", font_size=20, color=GREY_A).next_to(a, DOWN, buff=0.25)
        cb = label(r"work per GPU: \ " + r", \ ".join(f"${w}$" for w in Pr["zigzag"]), font_size=20,
                   color=GREY_A).next_to(b, DOWN, buff=0.25)
        head = label(r"causal attention: \ which query block (row) needs which key block (column)", font_size=22)
        head.to_edge(UP, buff=0.45)
        src = cite(r"Llama Team (2024), Sec.\ 3.3.2: \ all-gather of $K, V$; \ $2 \times$CP chunks", corner=DR,
                   font_size=17)
        zz = Pr["zigzag"]
        even = ("Now every GPU does the same work." if len(set(zz)) == 1 else
                f"Now the busiest GPU does {max(zz) / min(zz):.2f} times the work of the idlest.")
        with self.voiceover(
            "There's a catch with causal attention. A position only looks back, so the first block of queries needs "
            "one block of keys, and the last needs all of them. <bookmark mark='a'/> With contiguous blocks, the "
            f"last GPU does {Pr['contiguous'][-1]} times the work of the first, and everyone waits for it. "
            "<bookmark mark='b'/> The fix: cut the sequence into twice as many chunks, and give GPU i both chunk i "
            "and chunk 2p minus one minus i, one from each end. " + even + " Llama 3 did "
            "exactly this for its 128-thousand-token training, with sixteen-way context parallelism."
        ) as vo:
            ghost = a[0].copy().set_fill(GREY_D, opacity=0.7)
            self.play(FadeIn(head), FadeIn(src), FadeIn(ghost), FadeIn(a[1]))
            vo.wait_until("a")
            self.play(FadeIn(a[0]), FadeIn(ca))
            self.remove(ghost)
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(cb))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experts(self):
        D = F.DSV3
        p = 4
        g = ShardGrid(p, p, cell=0.5, row_gap=0.25, font_size=18).move_to([-3.2, -0.4, 0])
        cols_ = [C.EXPERT, C.ROUTER, C.PROB, C.EMBED]
        for r in range(p):
            for c in range(p):
                g.set(r, c, cols_[c], 0.3)
        lab = label(r"tokens on each GPU, \ coloured by the expert they're routed to", font_size=20, color=GREY_A)
        lab.next_to(g, UP, buff=0.25)
        facts = VGroup(
            label(r"experts live on different GPUs: \ expert parallelism", font_size=22, color=C.EXPERT),
            label(r"all-to-all: \ send each token to its experts, \ and the results back", font_size=22, color=COMM),
            label(rf"DeepSeek-V3: \ ${D['ep']}$-way expert parallel over ${D['nodes']}$ nodes; \ each token to at most "
                  rf"${D['max_nodes']}$ nodes", font_size=20, color=GREY_A),
            label(rf"InfiniBand ${D['ib'] / 1e9:.0f}$ GB/s against NVLink ${D['nvlink'] / 1e9:.0f}$ GB/s; \ "
                  rf"${D['comm_sms']}$ of ${D['sms']}$ SMs kept for communication", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.0, -0.3, 0])
        src = cite(r"Part 16; \ DeepSeek-AI (2024), Secs.\ 3.2, 3.4", corner=DR, font_size=17)
        with self.voiceover(
            "The second cut is for mixtures of experts, from Part 16: put different experts on different GPUs. "
            "<bookmark mark='a'/> Each token's router picks its experts wherever they live, so every layer begins with an "
            "all-to-all, each GPU sending its tokens to the GPUs that hold their experts, <bookmark mark='b'/> and ends "
            "with another, sending the results back. <bookmark mark='c'/> DeepSeek-V3 spread its experts over 64 GPUs in "
            "eight machines, and let each token visit at most four machines, because the network between machines is "
            "about three times slower than NVLink inside one. It even set aside twenty of each GPU's 132 processor blocks "
            "just to move tokens."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lab), FadeIn(src), FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(FadeIn(facts[1]))
            moves = [(r, c, c, r) for r in range(p) for c in range(p) if r != c]
            play_fly(self, g, moves, run_time=1.0, opacity_after=0.85)
            self.play(*[g.cells[r][c].animate.set_fill(cols_[r], opacity=0.85) for r in range(p) for c in range(p)],
                      run_time=0.4)
            vo.wait_until("b")
            play_fly(self, g, moves, run_time=1.0, opacity_after=0.3)
            vo.wait_until("c")
            self.play(FadeIn(facts[2]), FadeIn(facts[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def four_d(self):
        L = F.LLAMA3
        rows = L["table4"]
        cols = [r"GPUs", r"tensor", r"context", r"pipeline", r"data", r"sequence", r"TFLOP/s \\ per GPU", r"MFU"]
        xs = [-5.7, -4.0, -2.6, -1.1, 0.35, 1.9, 3.8, 5.7]
        hd = VGroup(*[label(c, font_size=23, color=GREY_B).move_to([x, 1.9, 0]) for c, x in zip(cols, xs)])
        body = VGroup()
        for i, r_ in enumerate(rows):
            y = 1.05 - 0.72 * i
            vals = [f"{r_[0]:,}", r_[1], r_[2], r_[3], r_[4], f"{r_[5]:,}", r_[8], f"{r_[9]}\\%"]
            body.add(VGroup(*[label(f"${v}$".replace(",", "{,}"), font_size=25,
                                    color=[WHITE, GPU, C.PROB, COMM, C.EMBED, ACTS, C_COL, C_COL][j]).move_to([x, y, 0])
                              for j, (v, x) in enumerate(zip(vals, xs))]))
        prods = [r_[1] * r_[2] * r_[3] * r_[4] for r_ in rows]
        assert prods == [r_[0] for r_ in rows]
        nest = VGroup()
        for k, (t, c) in enumerate(((r"data: \ FSDP", C.EMBED), (r"pipeline", COMM), (r"context", C.PROB),
                                    (r"tensor: \ inside one machine", GPU))):
            box = RoundedRectangle(width=11.0 - 2.4 * k, height=1.5 - 0.3 * k, corner_radius=0.12, stroke_color=c,
                                   stroke_width=2)
            nest.add(VGroup(box, label(t, font_size=20, color=c).next_to(box.get_corner(UL), DR, buff=0.08)))
        for b_ in nest:
            b_.move_to(DOWN * 2.5)
        src = cite(r"Llama Team (2024), Table 4", corner=DR, font_size=17)
        with self.voiceover(
            "A frontier run uses several cuts at once. Here is Llama 3's own table. <bookmark mark='a'/> On 16,384 "
            "GPUs with eight-thousand-token sequences: eight-way tensor parallel, sixteen pipeline stages, and 128 "
            "data-parallel groups. Eight times sixteen times 128 is 16,384. <bookmark mark='b'/> For the "
            "128-thousand-token stage, sixteen-way context parallelism took GPUs from the data dimension. "
            "<bookmark mark='c'/> The order matters. Tensor parallelism, which talks in every layer, is innermost, "
            "inside one machine. Context and pipeline come next. Data parallelism, which talks once a step and can "
            "wait, spans the whole cluster."
        ) as vo:
            self.play(FadeIn(hd), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(body[0]), FadeIn(body[1]))
            vo.wait_until("b")
            self.play(FadeIn(body[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in nest], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mfu(self):
        P, M = load("published"), load("mfu")
        Pa, O = F.PALM, F.OLMO3
        defn = definition_card(r"model FLOPs utilization", cmath(r"\text{MFU}", r"=",
                                                                 r"\frac{\text{tokens per second} \times 6N}"
                                                                 r"{\text{peak FLOP/s}}", font_size=30),
                               color=C_COL, width=6.4)
        defn.to_corner(UL, buff=0.4)
        d0 = defn.copy().scale(1.35).move_to(UP * 0.4)  # first shown large, in the middle
        palm = cmath(r"\text{PaLM}", r":", rf"\frac{{{Pa['tps'] / 1e3:.1f}\text{{k}} \times 6 \times 540\text{{B}}}}"
                     rf"{{275\text{{T}} \times 6{{,}}144}}", r"=", rf"{100 * P['palm_mfu']:.1f}\%", font_size=28)
        palm.next_to(defn, DOWN, buff=0.4).align_to(defn, LEFT)
        items = [(r"PaLM (2022)", Pa["mfu"] / 100, C_COL), (r"MegaScale (2024)", F.MEGASCALE["mfu"] / 100, C_COL),
                 (r"Llama 3 (2024)", 0.41, C_COL), (r"Olmo 3, 7B (2025)", O["mfu"][0] / 100, C_COL),
                 (r"ours, \ 2020 recipe", M["base"]["mfu"], BASE_C), (r"ours, \ 2026 recipe", M["full"]["mfu"], FULL_C)]
        rows = hbars(items, 1.0, width=4.2, bar_h=0.4, gap=0.2, font_size=22, label_width=3.2,
                     fmt=lambda v: rf"${100 * v:.0f}\%$")
        rows.move_to([3.6, 0.1, 0])
        rh = label(r"model FLOPs utilization", font_size=24, color=GREY_A).next_to(rows, UP, buff=0.25)
        ours = label(rf"this computer: \ peak ${M['peak'] / 1e9:.0f}$ GFLOP/s on one core \ (a $1024^2$ matrix product)",
                     font_size=18, color=GREY_B).next_to(rows, DOWN, buff=0.3)
        src = cite(r"Chowdhery et al.\ (2022); \ Jiang et al.\ (2024); \ Llama Team (2024); \ Team OLMo (2025)",
                   corner=DL, font_size=16)
        b, f = M["base"]["mfu"], M["full"]["mfu"]
        with self.voiceover(
            "With all this machinery, how much of the hardware does a run use? PaLM's paper defined the measure in 2022: "
            "model FLOPs utilization, the operations the model needs, six N per token times tokens per second, over the "
            "hardware's peak; recomputation and waiting don't count. <bookmark mark='a'/> PaLM processed 238 thousand "
            f"tokens a second on 6,144 TPU chips of 275 teraflops: {100 * P['palm_mfu']:.1f} percent, or 46.2 with "
            "attention counted. <bookmark mark='b'/> ByteDance's MegaScale reached 55 percent; Llama 3, 38 to 43; Olmo 3, "
            "43. About half of what a cluster could compute is lost to communication, bubbles, memory traffic and "
            "failures. <bookmark mark='c'/> Our own training runs, on one core of this computer: "
            f"{100 * b:.0f} and {100 * f:.0f} percent of its peak."
        ) as vo:
            self.play(FadeIn(d0, shift=UP * 0.1), FadeIn(src))
            vo.wait_until("a")
            self.play(ReplacementTransform(d0, defn))
            self.play(Write(palm))
            vo.wait_until("b")
            self.play(FadeIn(rh), LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2]))
                                                for r_ in rows[:4]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in rows[4:]],
                      FadeIn(ours))
        self.wait(0.3)
        self.clear_scene()
