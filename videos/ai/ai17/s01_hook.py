from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import BYTEC, COMMC, CPUC, FLOPC, GPUC, PART, load, machine_name, machine_spoken
from videos.ai.ai17.specs import ALEXNET_FLOP, LLAMA31_FLOP, LLAMA31_GPUS


class Hook(VoiceoverScene):
    def construct(self):
        self.two_vs_many()
        self.here()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def two_vs_many(self):
        two = VGroup(*[RoundedRectangle(width=1.2, height=0.7, corner_radius=0.08, stroke_color=GPUC, stroke_width=2,
                                        fill_color=GPUC, fill_opacity=0.5) for _ in range(2)]).arrange(DOWN, buff=0.2)
        two.move_to([-4.5, 0.4, 0])
        tl = VGroup(label(r"2012: \ AlexNet", font_size=28, color=GPUC),
                    label(r"two GeForce GTX 580s, \ five to six days", font_size=22, color=GREY_A))
        tl.arrange(DOWN, buff=0.12).next_to(two, DOWN, buff=0.35)
        side = int(math.isqrt(LLAMA31_GPUS))  # 16,384 = 128 x 128
        px = 6  # each GPU a 5-pixel square with a 1-pixel gap, drawn as one image
        img = np.zeros((side * px, side * px, 4), np.uint8)
        rgb = (np.array(ManimColor(GPUC).to_rgb()) * 255).astype(np.uint8)
        for i in range(side):
            img[i * px:i * px + px - 1, :, :3] = rgb
            img[i * px:i * px + px - 1, :, 3] = 230
        img[:, px - 1::px, 3] = 0
        grid = ImageMobject(img)
        grid.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        grid.height = 4.6
        grid.move_to([2.4, 0.6, 0])
        gl = VGroup(label(rf"2024: \ Llama 3.1, \ ${LLAMA31_GPUS:,}$ H100s".replace(",", "{,}"), font_size=28,
                          color=GPUC),
                    label(r"one square per GPU", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.1)
        gl.next_to(grid, DOWN, buff=0.25)
        ratio = LLAMA31_FLOP / ALEXNET_FLOP
        big = label(rf"$\times\,{ratio / 1e6:.0f}$ million \ the arithmetic", font_size=34, color=FLOPC)
        big.move_to([-4.3, -2.6, 0])
        cite_ = cite(r"Krizhevsky et al.\ (2012); \ Meta (2024); \ training compute: Epoch AI", corner=DR)
        with self.voiceover(
            "In 2012, the neural network that started the deep learning boom, AlexNet, was trained in five to six "
            "days on two graphics cards made for video games. <bookmark mark='a'/> Twelve years later Meta trained "
            "Llama 3.1, a language model of 405 billion parameters, on 16,384 of NVIDIA's H100 GPUs: here they are, "
            "one square each. <bookmark mark='b'/> By Epoch AI's count, that run used about "
            f"{ratio / 1e6:.0f} million times as many floating-point operations as AlexNet. Almost all of them were "
            "multiplications and additions of matrices."
        ) as vo:
            self.play(FadeIn(two, lag_ratio=0.3), FadeIn(tl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(grid, scale=0.92), FadeIn(gl), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(big, scale=1.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def here(self):
        mm = load("matmul")
        r1 = max(r[1] for r in mm["np_float32"])
        d_alex = ALEXNET_FLOP / r1 / 86400
        y_llama = LLAMA31_FLOP / r1 / (86400 * 365.25)
        chip = RoundedRectangle(width=2.6, height=2.6, corner_radius=0.15, stroke_color=CPUC, stroke_width=2.5,
                                fill_color=CPUC, fill_opacity=0.12).move_to([-4.2, 0.4, 0])
        cl = data_text(machine_name(), font_size=20, color=CPUC).next_to(chip, DOWN, buff=0.2)
        if cl.width > 4.4:
            cl.width = 4.4
        meas = VGroup(label(r"one core, \ measured:", font_size=24, color=CPUC),
                      label(rf"${r1 / 1e9:.0f}$ GFLOP/s", font_size=30, color=WHITE)).arrange(DOWN, buff=0.15)
        meas.move_to(chip)
        if meas.width > 2.4:
            meas.width = 2.4
        rows = VGroup(
            label(rf"AlexNet's training here: \ $\approx {d_alex:.0f}$ days", font_size=30, color=WHITE),
            label(rf"Llama 3.1's: \ $\approx {y_llama / 1e6:.0f}$ million years", font_size=30, color=FLOPC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([2.4, 0.6, 0])
        tag = note(r"computed: \ matrix products on this computer, \ one thread, \ best of seven").to_corner(DR,
                                                                                                         buff=0.2)
        with self.voiceover(
            f"The computer making this video reports its processor as {machine_spoken()}. <bookmark mark='a'/> We "
            f"measured how fast one of its cores multiplies matrices: at best, about {r1 / 1e9:.0f} billion operations a second. "
            "<bookmark mark='b'/> At that speed, AlexNet's training would take about "
            f"{d_alex:.0f} days. <bookmark mark='c'/> Llama 3.1's would take about {y_llama / 1e6:.0f} million years."
        ) as vo:
            self.play(FadeIn(chip), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(meas), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(rows[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows[1], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        q = label(r"Why does AI run on GPUs? \\ And what would a chip built for it look like?", font_size=40)
        q.move_to(UP * 1.2)
        path = VGroup(label(r"the power wall", font_size=22, color=C.HOT), MathTex(r"\to", font_size=28),
                      label(r"GPUs and CUDA", font_size=22, color=GPUC), MathTex(r"\to", font_size=28),
                      label(r"AlexNet", font_size=22, color=GPUC), MathTex(r"\to", font_size=28),
                      label(r"the roofline", font_size=22, color=FLOPC), MathTex(r"\to", font_size=28),
                      label(r"the TPU", font_size=22, color=FLOPC), MathTex(r"\to", font_size=28),
                      label(r"FP4", font_size=22, color=C.MAN_BIT), MathTex(r"\to", font_size=28),
                      label(r"rack-scale machines", font_size=22, color=COMMC)).arrange(RIGHT, buff=0.18)
        if path.width > 13.2:
            path.width = 13.2
        path.move_to(DOWN * 0.8)
        ours = label(r"measured on the computer making this video, \ wherever we can", font_size=26, color=CPUC)
        ours.to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "That gap is the subject of this part. Why does AI run on graphics processors, and what would a chip "
            "built for it look like? <bookmark mark='a'/> We'll follow the hardware from the moment clock speeds "
            "stopped rising, through the GPU, CUDA and AlexNet, to the arithmetic of matrix products and the "
            "roofline that bounds them, Google's TPU, numbers four bits wide, and machines the size of a room that "
            "act as one computer. <bookmark mark='b'/> And wherever we can, we'll measure it on the computer making "
            "this video."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in path], lag_ratio=0.12), run_time=3.5)
            vo.wait_until("b")
            self.play(FadeIn(ours))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Silicon", font_size=44).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.6)
        obj = objectives_card([
            r"why clocks stopped and cores multiplied: \ Dennard scaling and the power wall",
            r"GPUs from graphics to CUDA: \ SIMT, \ warps, \ latency hiding; \ AlexNet",
            r"matrix multiply: \ FLOPs, \ tiling, \ arithmetic intensity; \ the memory hierarchy; \ the roofline",
            r"systolic arrays, \ the TPU \ and tensor cores; \ number formats from FP32 to FP4",
            r"interconnect and the $\alpha$--$\beta$ model; \ ring all-reduce; \ writing a kernel",
            r"trends in FLOPs, dollars and watts; \ other accelerators; \ the frontier in late 2026",
        ], font_size=26)
        with self.voiceover(
            "This is Part 17 of AI, Built, in the third act, the transformer era. <bookmark mark='a'/> In this part: "
            "why clocks stopped getting faster; how graphics chips became the engines of AI; why matrix "
            "multiplication is the workload, and what bounds its speed, from the memory hierarchy to the roofline; "
            "systolic arrays and the number formats in the hardware; how chips talk to each other; how a fast "
            "kernel is written; and where the hardware stands now."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.3)
        self.clear_scene()
