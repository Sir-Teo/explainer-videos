from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, HIST, PART, VALUE, load

ACT = C.ACTS
CKP = C.BITS


def chain_row(n, y, size=0.5, gap=0.12):
    sq = VGroup(*[Square(side_length=size, stroke_color=GREY_C, stroke_width=1.5, fill_color=ACT, fill_opacity=0.0)
                  for _ in range(n)]).arrange(RIGHT, buff=gap)
    return sq.move_to([0, y, 0])


class Memory(VoiceoverScene):
    def construct(self):
        self.card()
        self.stores()
        self.derive()
        self.measured()

    def card(self):
        card = chapter_card(11, r"Memory: storing or recomputing", r"What does backpropagation have to remember?",
                            part=PART)
        with self.voiceover("Chapter eleven. Memory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def stores(self):
        n = 16
        row = chain_row(n, 0.6)
        idx = VGroup(*[MathTex(rf"h_{{{k + 1}}}", font_size=20, color=GREY_B).next_to(s, DOWN, buff=0.1)
                       for k, s in enumerate(row)])
        head = label(r"a chain of $16$ layers: \ the forward pass keeps every layer's output", font_size=28, color=GREY_A)
        head.to_edge(UP, buff=0.4)
        mem = label(r"held in memory:", font_size=24, color=ACT).move_to([-4.6, -1.4, 0])
        cnt = Integer(0, font_size=40, color=ACT).next_to(mem, RIGHT, buff=0.3)
        why_ = label(r"each backward step needs its layer's input: \ $\partial h_{k+1}/\partial h_k$ depends on $h_k$",
                     font_size=24, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Reverse mode has a price, and it is memory. <bookmark mark='a'/> On the way forward, every layer's output "
            "must be kept, <bookmark mark='b'/> because on the way back each step needs it: a layer's Jacobian depends "
            "on its input. <bookmark mark='c'/> Only as the backward pass reaches a layer can its activations be "
            "freed. So the memory grows with the depth, and with the batch and the width too; training large models, "
            "it is the activations, not the weights, that fill the GPU, which is Part 18's problem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row), FadeIn(idx), FadeIn(mem), FadeIn(cnt))
            vo.wait_until("a")
            self.play(LaggedStart(*[s.animate.set_fill(ACT, opacity=0.75) for s in row], lag_ratio=0.15),
                      cnt.animate.set_value(n), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(why_))
            vo.wait_until("c")
            self.play(LaggedStart(*[s.animate.set_fill(GRAD, opacity=0.0).set_stroke(GRAD) for s in reversed(row)],
                                  lag_ratio=0.15), cnt.animate.set_value(0), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        n, k = 16, 4
        row = chain_row(n, 2.5, size=0.42, gap=0.1)
        for j, s in enumerate(row):
            if (j + 1) % k == 0:
                s.set_fill(CKP, opacity=0.85)
        lab = label(r"keep every $k$-th output \ (here $k = 4$); \ recompute a segment when the backward pass needs it",
                    font_size=22, color=GREY_A).next_to(row, DOWN, buff=0.25)
        rows = [
            cmath(r"M(k)", r"=", r"\frac{n}{k} + k", font_size=40),
            cmath(r"M'(k)", r"=", r"-\frac{n}{k^2} + 1 = 0", font_size=40),
            cmath(r"k^*", r"=", r"\sqrt n, \qquad M(k^*) = 2\sqrt n", font_size=40, colors={r"k^*": CKP}),
            cmath(r"\text{extra work}", r"=", r"n - \frac{n}{k} \;\approx\; \text{one more forward pass}", font_size=36),
        ]
        whys = [why(r"$n/k$ checkpoints, \ plus one segment of $k$", font_size=22),
                why(r"smallest where the slope is zero", font_size=22), None,
                why(r"each segment is recomputed once", font_size=22)]
        step = ladder(self, rows, whys, keep=4, top=1.1, x=-2.4, buff=0.4, edge=6.9)
        hist = VGroup(
            history_card(1992, r"Andreas Griewank", r"binomial checkpointing: \ memory and recomputation both "
                         r"growing only like $\log n$", width=4.6, font_size=17, color=HIST),
            history_card(2016, r"Tianqi Chen, Bing Xu, Chiyuan Zhang, Carlos Guestrin", r"$\sqrt n$ checkpoints for deep "
                         r"networks: \ \textit{sublinear memory cost}", width=4.6, font_size=17, color=HIST),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_corner(DR, buff=0.25)
        with self.voiceover(
            "The way out is to trade memory for time. <bookmark mark='a'/> Keep only every k-th output, a "
            "checkpoint; when the backward pass reaches a segment, run that segment forward again from its "
            "checkpoint, and keep its k outputs just while they're needed. <bookmark mark='b'/> The memory is n over k "
            "checkpoints plus one segment of k. <bookmark mark='c'/> It's smallest where its slope is zero, "
            "<bookmark mark='d'/> at k equal to the square root of n, where it is two root n instead of n. "
            "<bookmark mark='e'/> The cost: every segment is recomputed once, about one extra forward pass. Tianqi "
            "Chen and colleagues brought this to deep networks in 2016; Andreas Griewank had shown in 1992 that "
            "recursive checkpoints bring both costs down to a logarithm."
        ) as vo:
            self.play(FadeIn(row))
            vo.wait_until("a")
            self.play(FadeIn(lab))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            step(3)
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        d = load("checkpoint")
        n = int(d["n"])
        ks, peak, evals = np.asarray(d["ks"]), np.asarray(d["peak"]), np.asarray(d["evals"])
        assert d["worst"] < 1e-12
        rt = int(round(math.sqrt(n)))
        g = axes([0, math.log2(n), 1], [0, n + 20, 64], x_length=6.2, y_length=4.0, xlabel=r"checkpoint every $k$ layers",
                 ylabel=r"most activations held at once", xticks=list(range(0, 9, 2)),
                 xfmt=lambda v: f"{2 ** int(v)}", yticks=[0, 64, 128, 192, 256], center=[-3.2, -0.2, 0])
        ax = g.ax
        lk = np.log2(ks)
        c_peak = curve(ax, lk, peak, CKP, 3.5)
        form = curve(ax, lk, n / ks + ks, GREY_B, 1.5)
        lo, hi = int(d["klo"]), int(d["khi"])
        bottom = Line(ax.c2p(math.log2(lo), peak.min()), ax.c2p(math.log2(hi), peak.min()), color=WHITE, stroke_width=6)
        root = DashedLine(ax.c2p(math.log2(rt), 0), ax.c2p(math.log2(rt), n), color=WHITE, stroke_width=1.5)
        rl = MathTex(rf"\sqrt{{{n}}} = {rt}", font_size=24).next_to(root, UP, buff=0.08)
        leg = VGroup(label(r"measured", font_size=20, color=CKP), label(r"$n/k + k$", font_size=20, color=GREY_B))
        leg.arrange(RIGHT, buff=0.4).next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        k_rt = int(np.where(ks == rt)[0][0])
        tab = VGroup(
            label(rf"a chain of ${n}$ tanh layers \ (computed):", font_size=22, color=GREY_A),
            label(rf"keep everything: \ ${int(peak[0])}$ held, \ ${int(evals[0])}$ layer evaluations", font_size=22, color=ACT),
            label(rf"every ${rt}$th: \ ${int(peak[k_rt])}$ held, \ ${int(evals[k_rt])}$ evaluations", font_size=22, color=CKP),
            label(rf"keep nothing: \ ${int(d['none_peak'])}$ held, \ ${int(d['none_evals']):,}$ evaluations".replace(",", "{,}"),
                  font_size=22, color=C.SURPRISE),
            label(r"the gradient: \ identical every way", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.7, 1.4, 0])
        ns, bk, bp = d["ns"], d["best_k"], d["best_peak"]
        sc = VGroup(label(r"longer chains: \ best $k$ \ (and $\sqrt n$)", font_size=20, color=GREY_A),
                    *[MathTex(rf"n = {a}: \ k = {b} \ ({int(round(math.sqrt(a)))}), \ \text{{held }} {c}", font_size=24)
                      for a, b, c in zip(ns, bk, bp)]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.7, -1.9, 0])
        ratio = d["t_ck"] / d["t_all"]
        inside = lo <= rt <= hi
        verdict = (f"and the square root of {n}, {rt}, is among them" if inside else
                   f"which is near the square root of {n}, {rt}, if not on it")
        all_root = all(abs(b - math.sqrt(a)) <= 0.15 * math.sqrt(a) + 1 for a, b in zip(ns, bk))
        scaling = ("On longer chains the best interval keeps tracking the square root." if all_root else
                   "On longer chains the best interval stays close to the square root.")
        with self.voiceover(
            f"Measured, on a chain of {n} layers. <bookmark mark='a'/> The most activations held at once follows n "
            f"over k plus k: {int(peak[0])} if you keep everything, and {int(peak.min())} at the bottom, which is flat "
            f"from k of {lo} to {hi}, {verdict}. <bookmark mark='b'/> The price is in evaluations: {int(evals[0])} "
            f"layers run forward if everything is kept, {int(evals[k_rt])} with checkpoints, and "
            f"{int(d['none_evals']):,} if nothing is kept and every input is recomputed from the start. "
            f"<bookmark mark='c'/> {scaling} Timed on a deeper, wider chain, checkpoints cost {ratio:.2f} times the "
            "time, and the gradient is the same in every case, to the last bit."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            self.play(Create(form), Create(c_peak), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(root), FadeIn(rl), Create(bottom))
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("c")
            self.play(FadeIn(sc))
        self.wait(0.3)
        self.clear_scene()
