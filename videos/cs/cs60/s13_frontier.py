from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs60.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES

# A datacentre GPU of 2022 (NVIDIA H100 SXM, datasheet): dense 16-bit tensor throughput and HBM3 bandwidth.
GPU_TFLOPS = 989.0
GPU_TBS = 3.35


def tile(title, body, col, w=4.2, h=3.4):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=19, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.3).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.decode()
        self.scale()
        self.open()

    def card(self):
        card = chapter_card(12, r"Frontier: \ accelerators for language models",
                            r"Why does generating one word at a time waste a chip?", lit=(2017, 2022),
                            extra=((2017, r"Jouppi et al.: \ the TPU"),
                                   (2022, r"Dao et al.: \ FlashAttention")), part=PART)
        with self.voiceover("Chapter twelve, the frontier. Why does generating text one word at a time leave most of a "
                            "chip idle?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def decode(self):
        head = label(r"One token at a time is memory-bound", font_size=36).to_edge(UP, buff=0.3)
        ridge = GPU_TFLOPS / GPU_TBS
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 3.3, 1], x_length=7.6, y_length=4.4,
                  axis_config={"color": GREY_D, "include_ticks": False}).move_to(LEFT * 2.2 + DOWN * 0.35)
        lx = VGroup(*[label(rf"$10^{{{p}}}$", font_size=16, color=GREY_B).next_to(ax.c2p(p, 0), DOWN, buff=0.12)
                      for p in range(5)])
        ly = VGroup(*[label(rf"$10^{{{p}}}$", font_size=16, color=GREY_B).next_to(ax.c2p(0, p), LEFT, buff=0.12)
                      for p in range(4)])
        xl = label(r"flops per byte of weights read", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.5)
        yl = label(r"TFLOP/s", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)

        def att(i):
            return min(GPU_TFLOPS, i * GPU_TBS)

        def pt(i):
            return ax.c2p(math.log10(i), math.log10(att(i)))

        roof = VMobject(color=KERN, stroke_width=4).set_points_as_corners(
            [ax.c2p(0, math.log10(GPU_TBS)), ax.c2p(math.log10(ridge), math.log10(GPU_TFLOPS)),
             ax.c2p(4, math.log10(GPU_TFLOPS))])
        rlab = label(rf"ridge: \ {ridge:.0f} flops per byte", font_size=18, color=KERN).next_to(
            ax.c2p(math.log10(ridge), math.log10(GPU_TFLOPS)), UP, buff=0.15)
        batches = (1, 8, 64, 512)
        dots = VGroup(*[Dot(pt(b), radius=0.08, color=HEAD if b < ridge else YES) for b in batches])
        dl = VGroup(*[label(rf"batch {b}", font_size=16, color=HEAD if b < ridge else YES).next_to(d, RIGHT, buff=0.1)
                      .shift(DOWN * 0.2) for b, d in zip(batches, dots)])
        side = VGroup(
            label(r"each new token reads every weight once:", font_size=19, color=WHITE),
            MathTex(r"2P \ \text{flops for } 2P \ \text{bytes}", font_size=30, color=WHITE),
            label(r"so about 1 flop per byte per sequence", font_size=19, color=HEAD),
            label(rf"at batch 1: \ {100 * att(1) / GPU_TFLOPS:.1f}\% of the peak", font_size=19, color=NO),
            label(r"remedies: \ batch, \ quantize the weights, \ ", font_size=19, color=GREY_A),
            label(r"speculate, \ keep attention in SRAM", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        src = note(rf"a 2022 datacentre GPU: \ {GPU_TFLOPS:.0f} TFLOP/s dense 16-bit, \ {GPU_TBS} TB/s \ (datasheet); "
                   r"one 16-bit weight is 2 bytes", font_size=16).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The newest accelerators are built for language models, and the roofline of chapter two explains their "
            "hardest problem. <bookmark mark='a'/> Here is the roofline of a datacentre GPU from 2022: nearly a "
            f"thousand trillion sixteen-bit operations a second, but only {GPU_TBS} terabytes a second from its "
            f"memory, so its ridge sits at about {ridge:.0f} operations per byte. <bookmark mark='b'/> To generate "
            "one token, a model with P parameters does about two P operations, and reads every one of its weights, "
            "two P bytes. That is one operation per byte. <bookmark mark='c'/> For a single conversation, the chip "
            f"runs at about {100 * att(1) / GPU_TFLOPS:.1f} percent of its peak. Serving many conversations at once "
            "reuses each weight read across the batch, and the point slides up the roof. <bookmark mark='d'/> Every "
            "remedy is the memory wall again: batch the users; quantize the weights to eight or four bits, "
            "Part 4's floats once more; guess several tokens with a small model and check them with one pass of the "
            "large one; and, as Tri Dao and colleagues showed with FlashAttention in 2022, reorder attention so "
            "that it stays in on-chip memory."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(lx), FadeIn(ly), FadeIn(xl), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(roof), FadeIn(rlab))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(dots[0]), FadeIn(dl[0]), FadeIn(side[3]))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d), FadeIn(t)) for d, t in zip(dots[1:], dl[1:])],
                                  lag_ratio=0.5), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

    def scale(self):
        head = label(r"Bigger than a chip", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"wafer scale", r"Cerebras \ (2019): \ one processor the size of a whole wafer, \ its memory spread "
                 r"among the cores, \ and spare cores to route around defects", HEAD),
            tile(r"chiplets", r"several small dies in one package, \ joined by short dense wires \ (AMD's server "
                 r"chips, \ 2017; \ the UCIe standard, \ 2022): \ better yield, \ mixed processes", DATA),
            tile(r"stacked memory", r"DRAM dies stacked beside the processor \ (HBM): \ wide and close, \ the "
                 r"bandwidth every accelerator above depends on", YES),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 0.4)
        foot = wrapped_label(r"the same fight as chapter eight: \ shorten the distance a byte must travel", 12.4,
                             font_size=21, color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The largest models do not fit on one chip, and the frontier is in how chips are put together. "
            "<bookmark mark='a'/> Cerebras made a single processor out of an entire silicon wafer, its memory spread "
            "among hundreds of thousands of cores, with spare cores so that manufacturing defects can be routed "
            "around. <bookmark mark='b'/> Most others went the opposite way: chiplets, several small dies in one "
            "package, joined by short and dense wires, which yield better than one huge die and can mix "
            "manufacturing processes. <bookmark mark='c'/> And memory is stacked into towers of DRAM dies right "
            "beside the processor, wide and close, which is where an accelerator's bandwidth comes from. "
            "<bookmark mark='d'/> All three are the fight of chapter eight, at a larger scale: shorten the distance "
            "that every byte must travel."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Design automation}: \ placement and routing are still heuristics; \ whether "
                          r"learned placers beat them is disputed.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{Verified hardware at scale}: \ the proofs of Part 54 for a whole "
                          r"accelerator, \ not one unit.", 12.4, font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Programming spatial machines}: \ a compiler that maps any loop nest onto a "
                          r"grid as well as an expert does.", 12.4, font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Past the memory wall}: \ serving large models at the speed of their "
                          r"arithmetic, \ not their memory.", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ the least data movement for a matrix "
                             r"product on an $N \times N$ grid of cells with $M$ words each \ (Hong and Kung's "
                             r"red--blue pebble game, \ 1981, \ on a grid), \ matched by a dataflow, \ with a proof",
                             12.4, font_size=23, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Placing and wiring billions of transistors is still done by "
            "heuristics, and whether learned placement beats them is disputed. <bookmark mark='b'/> Proofs of "
            "correctness, Part 54's kind, for a whole accelerator rather than one unit. <bookmark mark='c'/> A "
            "compiler that maps any loop nest onto a grid of cells as well as an expert does by hand. "
            "<bookmark mark='d'/> And serving large models at the speed of their arithmetic rather than their memory. "
            "<bookmark mark='e'/> This part's research problem returns to pebbles. In 1981 Hong Jia-Wei and H. T. "
            "Kung proved how many words the classical matrix product must move between a small fast memory and a large slow "
            "one, with a game of red and blue pebbles. Find the same bound for a grid of cells, each with its own "
            "small memory, and a dataflow that meets it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO, YES)
