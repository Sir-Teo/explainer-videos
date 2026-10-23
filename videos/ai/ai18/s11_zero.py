from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (COMM, F, GPU, GRADS, OPT, PART, WEIGHTS, ShardGrid, hbars, load, play_fly, spoken_int,
                                   take_away)


class ZeRO(VoiceoverScene):
    def construct(self):
        self.card()
        self.stages()
        self.memory()
        self.comm()
        self.measured()

    def card(self):
        card = chapter_card(10, r"ZeRO and FSDP", r"Why should every GPU keep a copy of everything?", part=PART)
        with self.voiceover("Chapter ten. ZeRO and FSDP."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def stages(self):
        p = 4
        kinds = [(r"weights", WEIGHTS), (r"gradients", GRADS), (r"optimizer state", OPT)]
        grids = VGroup()
        for k, (nm, col) in enumerate(kinds):
            g = ShardGrid(p, p, cell=0.42, row_gap=0.2, font_size=17)
            for r in range(p):
                for c in range(p):
                    g.set(r, c, col, 0.85)
            if k:
                g.names.set_opacity(0)
            t = label(nm, font_size=22, color=col).next_to(g.rows, UP, buff=0.2)
            grids.add(VGroup(g, t))
        grids.arrange(RIGHT, buff=0.55).move_to(UP * 0.6)
        stage_t = [label(r"data parallel: \ every GPU holds all of it", font_size=26, color=GREY_A),
                   label(r"ZeRO stage 1: \ shard the optimizer state", font_size=26, color=OPT),
                   label(r"ZeRO stage 2: \ and the gradients", font_size=26, color=GRADS),
                   label(r"ZeRO stage 3, \ FSDP: \ and the weights", font_size=26, color=WEIGHTS)]
        for t in stage_t:
            t.to_edge(DOWN, buff=1.7)
        hist = history_card(2019, r"Rajbhandari, Rasley, Ruwase \& He (Microsoft)", r"ZeRO, \ the Zero Redundancy "
                            r"Optimizer, \ in DeepSpeed", width=6.0, color=OPT)
        hist.scale(0.8).to_edge(DOWN, buff=0.15)

        def own_only(gi):
            g = grids[gi][0]
            return [g.cells[r][c].animate.set_fill(opacity=0.85 if r == c else 0.06) for r in range(p) for c in range(p)]

        with self.voiceover(
            "Data parallelism has a waste built in: every GPU keeps the whole model, its gradients and its optimizer "
            "state, chapter eight's sixteen bytes per parameter, all identical. <bookmark mark='a'/> In 2019 Samyam "
            "Rajbhandari and colleagues at Microsoft proposed ZeRO, the zero-redundancy optimizer: split them. "
            "<bookmark mark='b'/> Stage one: each GPU keeps the optimizer state for a quarter of the parameters, and "
            "updates only those. <bookmark mark='c'/> Stage two: only the gradients of its quarter, too. "
            "<bookmark mark='d'/> Stage three: only its quarter of the weights, fetching the rest from its neighbours "
            "just "
            "before a layer needs them, and dropping them after. PyTorch's stage three is called FSDP, fully sharded "
            "data "
            "parallel."
        ) as vo:
            self.play(FadeIn(grids), FadeIn(stage_t[0]))
            vo.wait_until("a")
            self.play(FadeIn(hist, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeOut(hist), ReplacementTransform(stage_t[0], stage_t[1]), *own_only(2))
            vo.wait_until("c")
            self.play(ReplacementTransform(stage_t[1], stage_t[2]), *own_only(1))
            vo.wait_until("d")
            self.play(ReplacementTransform(stage_t[2], stage_t[3]), *own_only(0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def memory(self):
        P, Z = load("published"), F.ZERO
        colors = {r"\Psi": WEIGHTS, r"N": GPU, r"K": OPT}
        rows = [
            cmath(r"\text{data parallel}", r":", r"(2 + 2 + K)\,\Psi", colors=colors, font_size=30),
            cmath(r"\text{stage 1}", r":", r"(2 + 2)\,\Psi + \frac{K\,\Psi}{N}", colors=colors, font_size=30),
            cmath(r"\text{stage 2}", r":", r"2\,\Psi + \frac{(2 + K)\,\Psi}{N}", colors=colors, font_size=30),
            cmath(r"\text{stage 3}", r":", r"\frac{(2 + 2 + K)\,\Psi}{N}", colors=colors, font_size=30),
        ]
        names = [r"everything, everywhere", r"optimizer state split $N$ ways", r"gradients too",
                 r"weights too"]
        mem = P["zero_mem"]
        def gb(m):
            return f"{m:.0f}" if m >= 100 else f"{m:.1f}" if m >= 10 else f"{m:.2f}"

        whys = [why(rf"{n}: \ ${gb(m)}$ GB", font_size=20) for n, m in zip(names, mem)]
        step = ladder(self, rows, whys, keep=4, top=1.95, x=-3.4, buff=0.4, edge=6.9)
        bars = hbars([(t, m, c) for t, m, c in zip((r"data parallel", r"stage 1", r"stage 2", r"stage 3"), mem,
                                                    (GREY_B, OPT, GRADS, WEIGHTS))], mem[0], width=5.4, bar_h=0.24,
                     gap=0.1, font_size=20, label_width=2.4, fmt=lambda v: rf"${gb(v)}$ GB")
        bars.move_to([0.9, -2.85, 0])
        bt = label(r"GB per GPU, \ the paper's example", font_size=18, color=GREY_B).next_to(bars, LEFT, buff=0.5)
        head = label(rf"bytes per GPU: \ $\Psi$ parameters, \ $K = {Z['k']}$, \ $N$ GPUs; \ the paper's example: "
                     rf"$\Psi = {Z['psi'] / 1e9:.1f}$B, \ $N = {Z['nd']}$", font_size=22, color=GREY_A)
        head.to_edge(UP, buff=0.45)
        src = cite(r"Rajbhandari et al., ZeRO (SC 2020), Fig.\ 1: \ $120$, $31.4$, $16.6$, $1.9$ GB", font_size=17)
        with self.voiceover(
            "The arithmetic, in the paper's notation: psi parameters, K bytes of optimizer state for each, twelve "
            "for mixed-precision Adam, and N GPUs. <bookmark mark='a'/> Plain data parallelism: sixteen bytes per "
            f"parameter on every GPU. For their example, 7.5 billion parameters on 64 GPUs: {mem[0]:.0f} gigabytes "
            f"each. <bookmark mark='b'/> Stage one divides the optimizer's twelve bytes by N: {mem[1]:.1f}. "
            f"<bookmark mark='c'/> Stage two, the gradients as well: {mem[2]:.1f}. <bookmark mark='d'/> Stage three "
            f"divides everything: {mem[3]:.2f} gigabytes per GPU. Sixty-four GPUs together hold the model once, "
            "not sixty-four times."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(bt), *[FadeIn(b_[0]) for b_ in bars])
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(k)
                self.play(GrowFromEdge(bars[k][1], LEFT), FadeIn(bars[k][2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def comm(self):
        p = 4
        g = ShardGrid(p, p, cell=0.55, row_gap=0.25).move_to([-3.0, -0.2, 0])
        for r in range(p):
            for c in range(p):
                g.set(r, c, WEIGHTS, 0.85 if r == c else 0.06)
        lab = label(r"a layer's weights, \ one quarter per GPU", font_size=22, color=WEIGHTS).next_to(g, UP, buff=0.3)
        steps_ = VGroup(
            label(r"forward: \ all-gather the layer's weights, \ use, \ drop", font_size=22, color=WEIGHTS),
            label(r"backward: \ all-gather them again, \ use, \ drop", font_size=22, color=WEIGHTS),
            label(r"then: \ reduce-scatter the gradients, \ each keeps its quarter", font_size=22, color=GRADS),
            label(r"stages 1 and 2: \ $2\,\Psi$ moved per step, \ as an all-reduce", font_size=24, color=COMM),
            label(r"stage 3: \ $3\,\Psi$, \ $1.5\times$", font_size=24, color=COMM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.2, -0.2, 0])

        def gather():
            moves = [(c, c, r, c) for c in range(p) for r in range(p) if r != c]
            play_fly(self, g, moves, run_time=0.9, color_after=WEIGHTS, opacity_after=0.85)

        def drop():
            self.play(*[g.cells[r][c].animate.set_fill(opacity=0.06) for r in range(p) for c in range(p) if r != c],
                      run_time=0.5)

        with self.voiceover(
            "What does sharding cost in communication? Stages one and two cost nothing extra: the all-reduce already "
            "was "
            "a reduce-scatter and an all-gather, with each GPU's update in between. <bookmark mark='a'/> Stage three "
            "keeps only a quarter of each layer's weights: "
            "before the layer runs forward, the GPUs all-gather it, and afterwards they drop it. <bookmark mark='b'/> "
            "The "
            "backward pass needs the weights again: gather once more. <bookmark mark='c'/> And the gradients are "
            "reduce-scattered, so each GPU keeps only its quarter. <bookmark mark='d'/> Three passes over the "
            "parameters "
            "instead of two: half as much traffic again, in exchange for memory divided by N. Meta trained Llama 3 "
            "with "
            "FSDP across its data-parallel groups; DeepSeek-V3 used stage one."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lab), FadeIn(steps_[3]))
            vo.wait_until("a")
            self.play(FadeIn(steps_[0]))
            gather()
            drop()
            vo.wait_until("b")
            self.play(FadeIn(steps_[1]))
            gather()
            drop()
            vo.wait_until("c")
            self.play(FadeIn(steps_[2]))
            self.play(*[g.cells[r][c].animate.set_fill(GRADS, opacity=0.85 if r == c else 0.06) for r in range(p)
                        for c in range(p)])
            vo.wait_until("d")
            self.play(FadeIn(steps_[4]), Indicate(steps_[3], scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        Pr = load("parallel")
        p = Pr["p"]
        n = Pr["n_params"]
        rows = [
            (r"one process, \ the whole batch", r"reference", None, None),
            (r"data parallel, \ $4$ processes", rf"${sci(Pr['err']['dp'], 0)}$", Pr["persistent_dp"], Pr["sent_dp"]),
            (r"ZeRO-3 / FSDP, \ $4$ processes", rf"${sci(Pr['err']['zero3'], 0)}$", Pr["persistent_z3"],
             Pr["sent_z3"]),
        ]
        heads = [r"", r"largest parameter \\ difference", r"numbers kept \\ per process", r"numbers sent \\ per step"]
        xs = [-4.5, -0.6, 2.5, 5.3]
        hd = VGroup(*[label(h, font_size=23, color=GREY_B).move_to([x, 2.35, 0]) for h, x in zip(heads, xs)])
        body = VGroup()
        for i, (nm, err, keep, sent) in enumerate(rows):
            y = 1.3 - 0.95 * i
            cells = [label(nm, font_size=26, color=WHITE).move_to([xs[0], y, 0]),
                     label(err, font_size=26, color=GREY_A).move_to([xs[1], y, 0])]
            if keep is not None:
                cells += [label(rf"${keep:,}$".replace(",", "{,}"), font_size=26, color=OPT).move_to([xs[2], y, 0]),
                          label(rf"${sent:,.0f}$".replace(",", "{,}"), font_size=26, color=COMM).move_to([xs[3], y, 0])]
            body.add(VGroup(*cells))
        ratio_mem = Pr["persistent_dp"] / Pr["persistent_z3"]
        ratio_comm = Pr["sent_z3"] / Pr["sent_dp"]
        match15 = ("ZeRO's one and a half, measured." if abs(ratio_comm - 1.5) < 0.05 else
                   "ZeRO's paper predicts one and a half.")
        res = VGroup(
            label(rf"memory: \ ${ratio_mem:.2f}\times$ less, \ plus one layer at a time "
                  rf"(${Pr['transient_z3']:,}$ numbers)".replace(",", "{,}"), font_size=28, color=OPT),
            label(rf"traffic: \ ${ratio_comm:.2f}\times$ more", font_size=28, color=COMM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 2.25)
        e3, e1 = Pr["err"]["zero3"], Pr["err"]["dp"]
        if e3 < 1e-3:
            same = (f"After {Pr['steps']} steps, its parameters match the one-process run to within "
                    f"{e3:.5f}, as plain data parallelism does: only the order of the additions differs.")
        else:
            same = (f"After {Pr['steps']} steps, its parameters differ from the one-process run by up to {e3:.5f}, "
                    "more than rounding alone explains.")
        tag = note(rf"computed: \ a model of ${n:,}$ parameters, \ ${Pr['steps']}$ steps of AdamW, \ PyTorch's gloo "
                   r"backend".replace(",", "{,}"), font_size=18).to_corner(DR, buff=0.2)
        with self.voiceover(
            "We built ZeRO stage three ourselves, on four processes: each holds a quarter of every layer's "
            "parameters, gradients and Adam moments, gathers a layer just before it runs, forward and backward, and "
            "reduce-scatters its gradients. <bookmark mark='a'/> " + same + " "
            f"<bookmark mark='b'/> Each process keeps {ratio_mem:.0f} times fewer numbers, plus one layer at a time. "
            f"<bookmark mark='c'/> And it sends {ratio_comm:.2f} times as much: " + match15
        ) as vo:
            self.play(FadeIn(hd), FadeIn(body[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(body[1][:2]), FadeIn(body[2][:2]))
            vo.wait_until("b")
            self.play(FadeIn(body[1][2]), FadeIn(body[2][2]), FadeIn(res[0]))
            vo.wait_until("c")
            self.play(FadeIn(body[1][3]), FadeIn(body[2][3]), FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()
