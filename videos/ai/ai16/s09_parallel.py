from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (COMMC, EXPERT_COLORS, F, MODE_COLOR, MODES, PART, load, ms, take_away)


class Parallel(VoiceoverScene):
    def construct(self):
        self.card()
        self.picture()
        self.traffic()
        self.busiest()

    def card(self):
        card = chapter_card(8, r"Experts across chips", r"What does it cost to send tokens to their experts?", part=PART)
        with self.voiceover("Chapter eight. Experts across chips."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def picture(self):
        D, per = 4, 2
        g = np.random.default_rng(8)
        gpus = VGroup()
        for d in range(D):
            box = RoundedRectangle(width=2.7, height=3.6, corner_radius=0.15, stroke_color=C.GPU, stroke_width=2)
            ex = VGroup(*[RoundedRectangle(width=0.95, height=0.55, corner_radius=0.08, stroke_color=EXPERT_COLORS[d * per + j],
                                           stroke_width=2, fill_color=EXPERT_COLORS[d * per + j], fill_opacity=0.2)
                          for j in range(per)]).arrange(RIGHT, buff=0.25)
            el = VGroup(*[MathTex(rf"E_{d * per + j + 1}", font_size=22, color=EXPERT_COLORS[d * per + j]).move_to(e_)
                          for j, e_ in enumerate(ex)])
            nm = label(rf"GPU {d + 1}", font_size=22, color=C.GPU)
            inner = VGroup(nm, VGroup(ex, el)).arrange(DOWN, buff=0.25)
            inner.move_to(box.get_top() + DOWN * 0.75)
            gpus.add(VGroup(box, inner))
        gpus.arrange(RIGHT, buff=0.35).move_to([0, 0.2, 0])
        toks = VGroup()
        dest = g.integers(0, D * per, (D, 6))
        for d in range(D):
            row = VGroup(*[Square(0.26, stroke_width=0, fill_color=EXPERT_COLORS[int(e)], fill_opacity=0.9) for e in dest[d]])
            row.arrange_in_grid(rows=2, cols=3, buff=0.06).move_to(gpus[d][0].get_bottom() + UP * 0.75)
            toks.add(row)
        tl = label(r"each GPU's tokens, \ coloured by the expert they're routed to", font_size=22, color=GREY_A)
        tl.to_edge(UP, buff=0.3)
        cite_ = cite(r"Part 18: \ expert parallelism and collectives", corner=DL)
        a2a = label(r"all-to-all: \ every GPU sends each token to its experts' GPU, \ and gets the answers back",
                    font_size=22, color=COMMC).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A model with hundreds of experts doesn't fit on one chip, so the experts are spread out: expert "
            "parallelism, which part 18 builds. Here, eight experts on four GPUs. <bookmark mark='a'/> Each GPU "
            "holds some of the tokens, and the router sends them anywhere. <bookmark mark='b'/> So every MoE layer "
            "begins with an all-to-all, each GPU sending every token to its experts' GPU, <bookmark mark='c'/> and "
            "ends with another, bringing the answers home."
        ) as vo:
            self.play(FadeIn(gpus), FadeIn(cite_), FadeIn(tl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in toks], lag_ratio=0.2))
            vo.wait_until("b")
            targets = []
            for d in range(D):
                for t_, e in zip(toks[d], dest[d]):
                    dd, j = int(e) // per, int(e) % per
                    ex = gpus[dd][1][1][0][j]
                    targets.append((t_, ex.get_center() + DOWN * 0.55 + RIGHT * (0.09 * (len(targets) % 3) - 0.09)))
            orig = [t_.get_center() for t_, _ in targets]
            self.play(*[t_.animate.move_to(p) for t_, p in targets], FadeIn(a2a), run_time=1.8)
            vo.wait_until("c")
            self.play(*[t_.animate.move_to(p) for (t_, _), p in zip(targets, orig)], run_time=1.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def traffic(self):
        p = load("parallel")
        c = F.DSV3_CONFIG
        r = F.DSV3_ROUTING
        colors = {r"k": C.ROUTER, r"d": GREY_A, r"h": C.EXPERT}
        rows = [
            cmath(r"\text{bytes}", r"=", r"k\, d", r"\,(1 + 2)", r"=", rf"{int(p['v3_bytes']):,}".replace(",", "{,}"),
                  font_size=32),
            cmath(r"\text{FLOPs}", r"=", r"2 \cdot 3\, d\, h \cdot k", r"=", rf"{p['v3_flops'] / 1e6:.0f}\ \text{{M}}",
                  font_size=32),
            cmath(r"\frac{\text{FLOPs}}{\text{byte}}", r"=", r"2h", r"=", rf"{p['v3_intensity']:,.0f}".replace(",", "{,}"),
                  font_size=32),
            cmath(r"\frac{\text{FP8 FLOP/s}}{\text{InfiniBand B/s}}", r"=", rf"\frac{{{p['h800_flops'] / 1e12:,.0f}\ \text{{T}}}}"
                  rf"{{{p['ib'] / 1e9:.0f}\ \text{{G}}}}".replace(",", "{,}"), r"\approx", rf"{p['ridge_ib']:,.0f}".replace(",", "{,}"),
                  font_size=32),
        ]
        whys = [why(r"per token, per MoE layer: \ $8$ copies out in FP8, \ back in BF16"),
                why(r"the $8$ routed experts' SwiGLU: \ $3$ matrices of $d \times h$"),
                why(rf"DeepSeek-V3: \ $d = {c['d']:,}$, \ $h = {c['moe_ffn']:,}$".replace(",", "{,}")),
                why(r"what a GPU must do per byte, \ to keep up \ (Part 17)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.0, buff=0.5, edge=6.8)
        ratio = p["ridge_ib"] / p["v3_intensity"]
        fixes = VGroup(
            label(rf"each token to at most ${r['max_nodes']}$ of ${r['nodes']}$ nodes: \ InfiniBand once per node, \ then NVLink "
                  rf"(${r['nvlink'] / 1e9:.0f}$ GB/s)", font_size=20, color=COMMC),
            label(r"dispatch in $8$-bit numbers; \ compute overlapped with communication \ (DualPipe, \ Part 18)",
                  font_size=20, color=COMMC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        cite_ = cite(r"DeepSeek-AI, \textit{DeepSeek-V3} (2024), \ Secs.~2.1.2, 3.2; \ NVIDIA H100 datasheet", corner=UR,
                     font_size=17)
        with self.voiceover(
            "How expensive is that? Take DeepSeek-V3, one token, one MoE layer. <bookmark mark='a'/> It sends eight "
            f"copies of a {c['d']:,}-number vector out, in eight-bit numbers, and gets eight answers back in sixteen "
            f"bits: {p['v3_bytes'] / 1e3:.0f} kilobytes. <bookmark mark='b'/> The eight experts do "
            f"{p['v3_flops'] / 1e6:.0f} million operations on it. <bookmark mark='c'/> That's {p['v3_intensity']:,.0f} "
            "operations per byte moved: twice the expert's width, whatever the model. <bookmark mark='d'/> But a GPU "
            f"doing eight-bit arithmetic needs about {p['ridge_ib']:,.0f} operations per byte from InfiniBand to stay "
            f"busy, part seventeen's roofline. Sent naively, the network would take {ratio:.0f} times as long as the "
            "experts. <bookmark mark='e'/> So DeepSeek sent each token to at most four of its eight machines, crossing "
            "InfiniBand once per machine and spreading over NVLink inside it, dispatched in eight bits, and hid the "
            "rest by computing one batch while another was in flight."
        ) as vo:
            self.play(FadeIn(cite_))
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(i)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(f_) for f_ in fixes], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def busiest(self):
        p = load("parallel")
        D = int(p["devices"])
        groups = VGroup()
        for i, (k, name, col) in enumerate(MODES):
            dev = np.asarray(p[f"{k}_dev"], float)  # seeds, layers, devices
            show = dev[:, 0].mean(0)  # block 1, mean over seeds
            bars = VGroup(*[Rectangle(width=0.45, height=max(4.0 * v, 0.02), stroke_width=0, fill_color=C.GPU,
                                      fill_opacity=0.85) for v in show]).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
            base = Line(bars.get_left() + LEFT * 0.15, bars.get_right() + RIGHT * 0.15, color=GREY_C).align_to(bars, DOWN)
            fair = DashedLine(base.get_left() + UP * 4.0 / D, base.get_right() + UP * 4.0 / D, color=GREY_B, stroke_width=1.5)
            gl = VGroup(*[label(rf"GPU {j + 1}", font_size=16, color=GREY_B).next_to(b_, DOWN, buff=0.1) for j, b_ in enumerate(bars)])
            t = label(name, font_size=22, color=col)
            s = label(rf"the step waits for the busiest: \ ${p[f'{k}_slowdown']:.2f}\times$", font_size=20, color=WHITE)
            grp = VGroup(VGroup(bars, base, fair, gl), t, s)
            t.next_to(grp[0], UP, buff=0.4)
            s.next_to(grp[0], DOWN, buff=0.15).shift(DOWN * 0.3)
            groups.add(grp)
        groups.arrange(RIGHT, buff=0.8, aligned_edge=DOWN).move_to([0, -0.2, 0])
        head = label(r"our routers, \ their experts spread over $4$ GPUs: \ each GPU's share of the work \ (block 1)",
                     font_size=24).to_edge(UP, buff=0.35)
        tag = note(r"three seeds' mean; \ dashed: \ a quarter each; \ a simulation of the placement", font_size=18)
        tag.to_edge(DOWN, buff=0.25)
        sl = {k: float(p[f"{k}_slowdown"]) for k, _, _ in MODES}
        ta = take_away(r"balance is speed: \ every GPU waits for the busiest", color=COMMC, font_size=26)
        with self.voiceover(
            "And balance, which looked like a matter of using every parameter, turns out to be a matter of speed. "
            "Put our trained experts on four GPUs, two each, and count each GPU's share of the work. "
            "<bookmark mark='a'/> Every GPU must finish before the next layer can start, so the step takes as long "
            "as the busiest GPU. Without balancing, that's "
            f"{sl['none']:.2f} times a fair share; with Switch's loss, {sl['aux']:.2f}; with the bias, "
            f"{sl['moe']:.2f}. <bookmark mark='b'/> On a real cluster that factor multiplies the time of every MoE "
            "layer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(VGroup(g_[0][1], g_[0][3], g_[1])) for g_ in groups])
            self.play(*[GrowFromEdge(b_, DOWN) for g_ in groups for b_ in g_[0][0]], *[Create(g_[0][2]) for g_ in groups])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g_[2]) for g_ in groups], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(FadeIn(ta))
        self.wait(0.3)
        self.clear_scene()
