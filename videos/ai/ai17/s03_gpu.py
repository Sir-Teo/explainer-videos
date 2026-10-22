from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import (BYTEC, CPUC, FLOPC, GPUC, L2C, PART, box_label, code_lines, cpu_die, gpu_die, load,
                                   machine_name)
from videos.ai.ai17.specs import H800_LAT


class Throughput(VoiceoverScene):
    def construct(self):
        self.card()
        self.pixels()
        self.design()
        self.little()
        self.gpgpu()

    def card(self):
        card = chapter_card(2, r"From pixels to GPGPU", r"What kind of chip is good at the same thing a million times?",
                            lit=(1999, 2007), part=PART)
        with self.voiceover("Chapter two. From pixels to GPGPU."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pixels(self):
        cols, rows = 32, 18
        cell = 0.2
        g = np.random.Generator(np.random.PCG64(1999))
        screen = VGroup(*[Square(cell, stroke_width=0.6, stroke_color="#1E2633", fill_color=GPUC, fill_opacity=0.05)
                          for _ in range(cols * rows)]).arrange_in_grid(rows=rows, cols=cols, buff=0)
        screen.move_to([-2.6, 0.6, 0])
        frame = SurroundingRectangle(screen, buff=0.04, color=GREY_C, stroke_width=1.5)
        # a smooth "image": every pixel runs the same little program on its own coordinates
        xs, ys = np.meshgrid(np.linspace(-1, 1, cols), np.linspace(-0.6, 0.6, rows))
        shade = 0.5 + 0.5 * np.cos(4 * np.hypot(xs - 0.3, ys + 0.1)) * np.exp(-np.hypot(xs, ys))
        colors = [interpolate_color(ManimColor("#1B2A6B"), ManimColor("#F2D16B"), float(v)) for v in shade.ravel()]
        prog = code_lines(["color shade(x, y):", "  d = distance(x, y)", "  return light(d)"], font_size=20)
        prog.next_to(frame, DOWN, buff=0.35).align_to(frame, LEFT)
        n_px = 1920 * 1080
        maths = VGroup(MathTex(r"1920 \times 1080", font_size=34, color=WHITE),
                       label(rf"$= {n_px:,}$ pixels".replace(",", "{,}"), font_size=28, color=GREY_A),
                       label(rf"$\times\ 60$ frames a second \ $= {n_px * 60 / 1e6:.0f}$ million".replace(",", "{,}"),
                             font_size=28, color=GPUC)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        maths.move_to([4.2, 1.6, 0])
        hc = history_card(1999, r"NVIDIA GeForce 256", r"sold as \textit{the world's first GPU}: \ the geometry "
                          r"and lighting of 3D games on one chip; \ programmable shaders followed in 2001",
                          width=5.4, color=GPUC).move_to([4.2, -1.5, 0])
        with self.voiceover(
            "Think about what a graphics card does. <bookmark mark='a'/> Every pixel on the screen runs the same "
            "small program, a shader, on its own coordinates, and no pixel needs to know about any other. "
            "<bookmark mark='b'/> A 1080p screen is about two million pixels, sixty times a second: over a hundred "
            "million runs of the same program every second, all independent. <bookmark mark='c'/> In 1999 NVIDIA "
            "sold the GeForce 256 as the world's first GPU, a graphics processing unit, and in 2001 its shaders "
            "became programmable. It was a chip built for doing one thing an enormous number of times."
        ) as vo:
            self.play(FadeIn(screen), Create(frame))
            vo.wait_until("a")
            self.play(FadeIn(prog))
            order = np.argsort((xs + ys).ravel())
            self.play(LaggedStart(*[screen[i].animate.set_fill(colors[i], opacity=0.95) for i in order],
                                  lag_ratio=0.002), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in maths], lag_ratio=0.5))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def design(self):
        m = load("machine")
        lanes = 16 if "avx512f" in m["simd"] else (8 if "avx2" in m["simd"] else 4)
        cpu = cpu_die(width=4.6, height=3.4).move_to([-3.5, 0.5, 0])
        gpu = gpu_die(width=4.6, height=3.4, sms=(6, 9), lanes=(4, 4)).move_to([3.5, 0.5, 0])
        cl = label(r"CPU: \ make one thread fast", font_size=28, color=CPUC).next_to(cpu, UP, buff=0.25)
        gl = label(r"GPU: \ keep thousands of threads busy", font_size=28, color=GPUC).next_to(gpu, UP, buff=0.25)
        key = VGroup(box_label(r"arithmetic", FLOPC, font_size=20, height=0.42),
                     box_label(r"control", GREY_B, font_size=20, height=0.42),
                     box_label(r"cache", L2C, font_size=20, height=0.42)).arrange(RIGHT, buff=0.3)
        key.to_edge(DOWN, buff=0.35)
        cn = label(rf"this computer: \ ${m['cores']}$ cores, \ ${lanes}$-wide vectors", font_size=22,
                   color=CPUC).next_to(cpu, DOWN, buff=0.25)
        gn = label(r"an H100: \ $132$ SMs $\times$ $128$ lanes $= 16{,}896$", font_size=22,
                   color=GPUC).next_to(gpu, DOWN, buff=0.25)
        tag = schematic_tag(corner=UR)
        with self.voiceover(
            "A CPU and a GPU spend their transistors differently. <bookmark mark='a'/> A CPU spends them on making "
            "one stream of instructions fast: large caches, so data is close; branch predictors that guess which "
            "way the program will go; machinery to run instructions out of order. <bookmark mark='b'/> A GPU spends "
            "them on arithmetic: many small processors, NVIDIA calls them streaming multiprocessors, each a block of "
            "simple lanes. <bookmark mark='c'/> The computer making this video, a "
            f"{machine_name()}, has {m['cores']} cores, each with vector units {lanes} numbers wide. An H100 has "
            "132 streaming multiprocessors with 128 lanes each: almost seventeen thousand. <bookmark mark='d'/> Each "
            "lane is slow and simple. There are just a great many of them."
        ) as vo:
            self.play(FadeIn(cpu), FadeIn(gpu), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cl), FadeIn(key))
            self.play(Indicate(cpu.cache, color=L2C), *[Indicate(c_[1], color=GREY_A) for c_ in cpu.cores])
            vo.wait_until("b")
            self.play(FadeIn(gl), LaggedStart(*[Indicate(sm, color=FLOPC, scale_factor=1.05) for sm in gpu.sms],
                                              lag_ratio=0.02), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(cn), FadeIn(gn))
            vo.wait_until("d")
            self.play(gpu.sms.animate.set_opacity(1.0), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def little(self):
        h, mm = load("hierarchy"), load("matmul")
        colors = {r"L": BYTEC, r"\lambda": FLOPC, r"W": C.SURPRISE}
        rows = [
            cmath(r"L", r"=", r"\lambda", r"\,", r"W", colors=colors, font_size=44),
            cmath(r"\text{bytes in flight}", r"=", r"\text{bandwidth}", r"\times", r"\text{latency}", font_size=36),
        ]
        rows[1][0].set_color(BYTEC)
        rows[1][2].set_color(FLOPC)
        rows[1][4].set_color(C.SURPRISE)
        whys = [why(r"Little's law (1961): \ items in a queue $=$ arrival rate $\times$ time each spends"),
                why(r"the same law, for memory requests")]
        step = ladder(self, rows, whys, keep=2, top=3.0, x=-2.2, buff=0.45, edge=6.8)
        # the pipe from memory: requests in flight
        pipe = RoundedRectangle(width=9.0, height=0.8, corner_radius=0.4, stroke_color=GREY_C, stroke_width=2)
        pipe.move_to([0, -0.6, 0])
        mem = box_label(r"memory", BYTEC, font_size=22).next_to(pipe, LEFT, buff=0.15)
        core = box_label(r"cores", FLOPC, font_size=22).next_to(pipe, RIGHT, buff=0.15)
        VGroup(pipe, mem, core).move_to([0, -0.6, 0])
        packets = VGroup(*[RoundedRectangle(width=0.36, height=0.36, corner_radius=0.06, stroke_width=0,
                                            fill_color=BYTEC, fill_opacity=0.9) for _ in range(16)])
        for k, pk in enumerate(packets):
            pk.move_to(pipe.get_left() + RIGHT * (0.45 + k * 0.54))
        lat_s = H800_LAT["glob"] / (H800_LAT["mhz"] * 1e6)
        inflight = H800_LAT["bw"] * lat_s
        sizes = np.asarray(h["sizes"])
        dram_lat = float(np.median(np.asarray(h["latency"])[sizes >= 32 * 2 ** 20]))
        bw1 = float(mm["np_copy"][0])
        ours = bw1 * dram_lat
        gp = label(rf"H800: \ ${H800_LAT['bw'] / 1e9:,.0f}$ GB/s $\times$ ${lat_s * 1e9:.0f}$ ns \ $\approx$ "
                   rf"${inflight / 1e3:.0f}$ KB in flight \ $\approx {inflight / 128:,.0f}$ requests of $128$ bytes"
                   .replace(",", "{,}"), font_size=24, color=GPUC)
        cp = label(rf"one core of this computer: \ ${bw1 / 1e9:.1f}$ GB/s $\times$ ${dram_lat * 1e9:.0f}$ ns "
                   rf"$\approx {ours / 64:.0f}$ cache lines", font_size=24, color=CPUC)
        VGroup(gp, cp).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.85)
        src = cite(r"latency: \ Luo et al.\ (2024), \ measured on an H800", corner=UR)
        tag = note(r"computed: \ this computer's bandwidth and latency").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Simple lanes are the easy part. The hard part is feeding them, because memory is far away. "
            "<bookmark mark='a'/> There's a law from queueing theory, John Little's, from 1961: the number of "
            "things in a system equals the rate they arrive times how long each one stays. <bookmark mark='b'/> "
            "For memory, it says: to keep a memory busy, the bytes you have asked for but not yet received must "
            "equal the bandwidth times the latency. <bookmark mark='c'/> Researchers measured a Hopper GPU's memory "
            f"at about {round(lat_s * 1e9, -1):.0f} nanoseconds away. At two terabytes a second, it needs about "
            f"{round(inflight / 1e3, -1):.0f} kilobytes on the way at every moment: thousands of requests. "
            "<bookmark mark='d'/> One core of this computer, measured, needs only about "
            f"{ours / 64:.0f} cache lines on the way, and it gets them from prefetchers that guess the next "
            "addresses of a long, regular read. A GPU gets its thousands the other way: from thousands of threads, "
            "each waiting on its own load."
        ) as vo:
            self.play(Create(pipe), FadeIn(mem), FadeIn(core))
            step(0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(pk, shift=RIGHT * 0.3) for pk in packets], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(gp), FadeIn(src))
            vo.wait_until("d")
            self.play(FadeIn(cp), FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gpgpu(self):
        items = [
            (2004, r"Ian Buck et al., \ \textit{Brook for GPUs}, \ Stanford", r"arrays as textures, \ programs as "
             r"shaders: \ general computing in graphics' clothes", GREY_A),
            (2004, r"K.-S.~Oh \& K.~Jung", r"a neural network on a GPU, \ $20\times$ faster than the CPU it was "
             r"compared with", C.NEURAL),
            (2007, r"NVIDIA CUDA", r"announced with the GeForce 8800 in November 2006, \ released in 2007: \ C, plus "
             r"a way to launch thousands of threads", GPUC),
            (2009, r"R.~Raina, A.~Madhavan \& A.~Ng", r"deep belief networks on a GPU, \ up to $70\times$ faster "
             r"than a dual-core CPU", C.NEURAL),
        ]
        cards = VGroup(*[history_card(y, w, t, width=6.4, color=c, font_size=23) for y, w, t, c in items])
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.45)).move_to(DOWN * 0.15)
        head = label(r"General-purpose computing on GPUs", font_size=36, color=GPUC).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Researchers noticed. <bookmark mark='a'/> In the early two thousands they disguised arithmetic as "
            "graphics: store an array as a texture, write the computation as a pixel shader, and read the answer "
            "back from the screen. Ian Buck's Brook language at Stanford, in 2004, made that bearable. "
            "<bookmark mark='b'/> The same year, Kyoung-Su Oh and Keechul Jung ran a neural network on a graphics "
            "card, twenty times faster than on the CPU. <bookmark mark='c'/> Buck went to NVIDIA, and with John "
            "Nickolls built CUDA: plain C, plus a way to launch a function on thousands of threads at once. It was "
            "announced with the GeForce 8800 in November 2006 and released in 2007. <bookmark mark='d'/> By 2009 "
            "Rajat Raina, Anand Madhavan and Andrew Ng at Stanford trained deep networks on a GPU up to seventy "
            "times faster than on a CPU. The pieces of the next decade were on the table."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
