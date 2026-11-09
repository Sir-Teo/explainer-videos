from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CODE, CORE_COLORS, CTRL, DATA, FUNC, HEAD, NO, PART, YES, load, mono)


class Gpu(VoiceoverScene):
    def construct(self):
        self.card()
        self.shape()
        self.simt()
        self.divergence()
        self.job()

    def card(self):
        card = chapter_card(8, r"GPUs in one chapter", r"What if you had ten thousand simple cores?",
                            lit=(1999, 2006), extra=((1999, r"GeForce 256"), (2006, r"CUDA")), part=PART)
        with self.voiceover("Chapter eight. GPUs in one chapter."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def shape(self):
        head = label(r"A different bargain", font_size=36).to_edge(UP, buff=0.35)
        cpu = VGroup()
        cb = RoundedRectangle(width=4.6, height=3.6, corner_radius=0.12, stroke_color=DATA, stroke_width=2)
        cores = VGroup(*[RoundedRectangle(width=1.7, height=1.3, corner_radius=0.08, stroke_color=DATA,
                                          fill_color=DATA, fill_opacity=0.25) for _ in range(4)]).arrange_in_grid(
            2, 2, buff=0.25).move_to(cb)
        cpu.add(cb, cores, label(r"a CPU: \ a few big cores", font_size=22, color=DATA).next_to(cb, UP, buff=0.15))
        cpu.add(label(r"out of order, \ predicted, \ deep caches: \\ each thread as fast as possible", font_size=18,
                      color=GREY_A).next_to(cb, DOWN, buff=0.15))
        gb = RoundedRectangle(width=4.6, height=3.6, corner_radius=0.12, stroke_color=YES, stroke_width=2)
        sms = VGroup()
        for k in range(16):
            sm = VGroup(*[Square(side_length=0.09, stroke_width=0, fill_color=YES, fill_opacity=0.8)
                          for _ in range(32)]).arrange_in_grid(4, 8, buff=0.03)
            sms.add(VGroup(RoundedRectangle(width=sm.width + 0.12, height=sm.height + 0.12, corner_radius=0.04,
                                            stroke_color=YES, stroke_width=1), sm))
        sms.arrange_in_grid(4, 4, buff=0.12).move_to(gb)
        gpu = VGroup(gb, sms, label(r"a GPU: \ thousands of simple lanes", font_size=22, color=YES).next_to(
            gb, UP, buff=0.15), label(r"warp scheduling, \ latency hiding: \\ throughput across many threads",
                                      font_size=18, color=GREY_A).next_to(gb, DOWN, buff=0.15))
        VGroup(cpu, gpu).arrange(RIGHT, buff=1.0).shift(DOWN * 0.15)
        nums = note(r"Nvidia H100 SXM \ (2022): \ 132 streaming multiprocessors, \ 16,896 FP32 lanes, \ 3.35 TB/s HBM \ "
                    r"(\textit{AI, Built} 17)", font_size=17).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            (
            "A graphics processor makes the opposite bargain from a CPU. <bookmark mark='a'/> A CPU spends its "
            "transistors on making a few threads as fast as possible: out-of-order execution, branch prediction, "
            "deep caches, everything in Parts 7, 8 and 9. <bookmark mark='b'/> A GPU spends them on arithmetic. "
            "It has thousands of simple lanes, grouped into streaming multiprocessors, using throughput-oriented "
            "warp scheduling rather than the large speculative out-of-order machinery of a CPU. Modern GPUs still "
            "have substantial caches and sophisticated scheduling. But there are tens of thousands of threads, "
            "and when one waits for memory, the hardware simply runs another, the multithreading of Part 8 taken "
            "to the extreme. <bookmark mark='c'/> As a dated hardware example, the 2022 Nvidia H100 SXM has a "
            "hundred and thirty-two multiprocessors and nearly seventeen thousand lanes, fed by stacked memory at "
            "over three terabytes a second."
        )
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(cpu), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(FadeIn(gpu))
            vo.wait_until("c")
            self.play(FadeIn(nums))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def simt(self):
        head = label(r"SIMT: \ 32 threads, \ one instruction", font_size=34).to_edge(UP, buff=0.3)
        code = VGroup(mono("i = thread index;", 19), mono("if (x[i] > 0)", 19), mono("    y[i] = sqrt(x[i]);", 19),
                      mono("else", 19), mono("    y[i] = 0;", 19)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        code.to_edge(LEFT, buff=0.7).shift(UP * 0.6)
        xs = [3, -1, 4, 1, -5, 9, 2, -6, 5, 3, -5, 8, 9, -7, 9, 3, 2, 3, -8, 4, 6, 2, -6, 4, 3, 3, 8, -3, 2, 7, 9, -5]
        lanes = VGroup(*[Square(side_length=0.22, stroke_color=GREY_C, stroke_width=1) for _ in xs]).arrange_in_grid(
            4, 8, buff=0.05).next_to(code, RIGHT, buff=1.2)
        ll = label(r"a warp: \ 32 lanes in lockstep", font_size=19, color=GREY_B).next_to(lanes, UP, buff=0.15)
        ifm = [x > 0 for x in xs]
        step1 = label(r"the warp runs the \texttt{if} branch, \ lanes with $x \le 0$ masked off", font_size=20,
                      color=YES)
        step2 = label(r"then the \texttt{else} branch, \ the others masked off", font_size=20, color=CTRL)
        steps = VGroup(step1, step2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(VGroup(code, lanes), DOWN,
                                                                                         buff=0.6)
        cost = label(r"divergence: \ a warp takes the time of every path any of its lanes takes", font_size=23,
                     color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "The programming model is called single instruction, multiple threads. <bookmark mark='a'/> You write "
            "the code for one thread, as if it ran alone, and launch thousands of copies, each with its own "
            "index. <bookmark mark='b'/> In this Nvidia-style example, the hardware groups them in warps of "
            "thirty-two, which share one instruction stream: at each step, the same instruction for all "
            "thirty-two lanes. <bookmark mark='c'/> So what happens at an if? Some lanes want one branch and some "
            "the other. The warp runs the first branch with the other lanes switched off, <bookmark mark='d'/> "
            "then the second branch with the first lanes switched off. <bookmark mark='e'/> This is the "
            "masked-execution picture of divergence. Actual scheduling, predication and reconvergence depend on "
            "the GPU; other vendors can use different subgroup widths."
        )
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(code), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(FadeIn(lanes), FadeIn(ll))
            vo.wait_until("c")
            self.play(FadeIn(step1), *[lanes[k].animate.set_fill(YES if ifm[k] else GREY_E, 0.8)
                                       for k in range(32)], Indicate(code[2], color=YES))
            vo.wait_until("d")
            self.play(FadeIn(step2), *[lanes[k].animate.set_fill(CTRL if not ifm[k] else GREY_E, 0.8)
                                       for k in range(32)], Indicate(code[4], color=CTRL))
            vo.wait_until("e")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def divergence(self):
        g = load("gpu")
        ex = g["example"]
        head = label(r"The Job's lookups, \ 32 to a warp", font_size=34).to_edge(UP, buff=0.3)
        mx = max(ex)
        W, H = 0.26, 3.4
        bars = VGroup(*[Rectangle(width=W * 0.8, height=max(0.02, H * v / mx), stroke_width=0, fill_color=DATA,
                                  fill_opacity=0.85) for v in ex])
        for k, b in enumerate(bars):
            b.move_to([-6.0 + k * W, -2.2 + b.height / 2, 0])
        full = Rectangle(width=W * 32, height=H, stroke_color=NO, stroke_width=2).move_to(
            [-6.0 + 15.5 * W, -2.2 + H / 2, 0])
        fl = label(r"the warp runs until its longest scan ends", font_size=19, color=NO).next_to(full, UP, buff=0.1)
        lab = label(r"recorded scan lengths in a 32-lane proxy; \ no GPU execution", font_size=18, color=GREY_B).next_to(
            full, DOWN, buff=0.15)
        eff = float(np.mean(ex) / mx)
        side = VGroup(
            label(rf"this warp: \ {100 * eff:.0f}\% of the \\ lanes' time is useful", font_size=22, color=NO),
            label(rf"all {g['lookups'] / 1e6:.1f} million \\ lookups: \ {100 * g['efficiency']:.0f}\%", font_size=22,
                  color=NO),
            label(rf"oracle grouping by length: \\ {100 * g['efficiency_sorted']:.2f}\% \ (cost excluded)", font_size=21, color=YES),
            label(r"GPU code keeps a warp's \\ lanes alike: \ sort the work, \\ avoid branches", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(full, RIGHT, buff=0.45)
        with self.voiceover(
            f"Imagine running the Job's lookups on a GPU, one word per lane, thirty-two to a warp. <bookmark mark='a'/> Here is one group from the recorded scan-length sequence, not an executed GPU warp: for each of its thirty-two words, how many table entries the lookup must scan. A common word is found near the front; a rare one, near the end of a table of tens of thousands. <bookmark mark='b'/> The warp cannot finish until its longest scan does, and meanwhile the lanes that finished early sit idle. Only {100 * eff:.0f} percent of this warp's lane time does useful work. <bookmark mark='c'/> Over all four and a half million lookups, {100 * g['efficiency']:.0f} percent. <bookmark mark='d'/> If an oracle first grouped the lookups by their already-known scan lengths, nearly all of this lane-count proxy would be useful. That excludes finding those lengths, regrouping, memory traffic and maintaining correct shared counts; it is not an achievable speedup claim. That is the craft of GPU programming: arrange the work so that the thirty-two lanes of a warp do the same thing."
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), FadeIn(lab), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(Create(full), FadeIn(fl), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def job(self):
        head = label(r"What GPUs are for", font_size=36).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"the same arithmetic on millions of independent items: \ pixels, \ particles, \ matrix entries",
                  font_size=22, color=YES),
            label(r"memory read in wide, \ regular blocks: \ each warp's 32 loads merged into a few lines", font_size=22,
                  color=DATA),
            label(r"matrix multiply above all: \ tensor cores multiply small matrices in one instruction", font_size=22,
                  color=CTRL),
            label(r"the Job as written is the opposite: \ one long chain, \ data-dependent scans", font_size=22,
                  color=NO),
            label(r"a GPU word count sorts first, \ then counts runs: \ Part 16's algorithm", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.1)
        cite = note(r"how a neural network uses one: \ \textit{AI, Built}, \ Part 17", font_size=18).to_edge(DOWN,
                                                                                                         buff=0.3)
        with self.voiceover(
            (
            "So GPUs shine on a particular kind of work. <bookmark mark='a'/> The same arithmetic on millions of "
            "independent items: pixels, particles, the entries of a matrix. <bookmark mark='b'/> Memory read in "
            "wide, regular blocks, so that the thirty-two loads of a warp merge into a few cache lines. <bookmark "
            "mark='c'/> And matrix multiplication above all: modern GPUs have tensor cores that multiply small "
            "matrices in a single instruction, which is why they run the neural networks of AI, Built. <bookmark "
            "mark='d'/> The Job, as written, is the opposite: one long chain of lookups, each a scan whose length "
            "depends on the data. <bookmark mark='e'/> One GPU-friendly alternative is sorting words and counting "
            "the runs; hashing is another option, and Part 16 develops the sorting approach."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite), run_time=0.5)
            for mk, p in zip('abcde', pts):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1), run_time=0.6 if mk == 'a' else 1.0)
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()
