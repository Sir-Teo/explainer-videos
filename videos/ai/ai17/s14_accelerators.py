from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import BYTEC, FLOPC, GPUC, L1C, PART, POWERC, load
from videos.ai.ai17.specs import GPUS, GROQ3_LPX, IRONWOOD, TPU1, TPU8I, TPU8T, TRAINIUM3, WSE3

# Google TPUs, peak per chip in the format each was built around (Jouppi et al. 2017, 2020, 2023; Google Cloud
# documentation and announcements; Epoch AI's database)
TPUS = [("v1", 2015, 92e12, r"INT8"), ("v2", 2017, 46e12, r"BF16"), ("v3", 2018, 123e12, r"BF16"),
        ("v4", 2021, 275e12, r"BF16"), ("v5p", 2023, 459e12, r"BF16"), ("v6e", 2024, 918e12, r"BF16"),
        ("v7 Ironwood", 2025, IRONWOOD["fp8"], r"FP8"), ("8t", 2026, TPU8T["fp4"], r"FP4")]


class Accelerators(VoiceoverScene):
    def construct(self):
        self.card()
        self.tpus()
        self.wafer()
        self.groq()
        self.analog()

    def card(self):
        card = chapter_card(13, r"Beyond the GPU", r"What else can run a neural network?", lit=(2016, 2024),
                            part=PART)
        with self.voiceover("Chapter thirteen. Beyond the GPU."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def tpus(self):
        lo, hi = 13, 16.5
        g = axes([0, len(TPUS)], [lo, hi], x_length=7.0, y_length=4.2, ylabel=r"peak operations a second, \ one chip",
                 yticks=[13, 14, 15, 16], yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.6, -0.1, 0])
        bars, labs, fmts = VGroup(), VGroup(), VGroup()
        for k, (nm, yr, v, fmt) in enumerate(TPUS):
            p0, p1 = g.ax.c2p(k + 0.5, lo), g.ax.c2p(k + 0.5, math.log10(v))
            col = interpolate_color(ManimColor(GPUC), ManimColor(FLOPC), k / (len(TPUS) - 1))
            bars.add(Rectangle(width=0.62, height=p1[1] - p0[1], stroke_width=0, fill_color=col, fill_opacity=0.85)
                     .move_to((p0 + p1) / 2))
            labs.add(VGroup(label(nm, font_size=18, color=WHITE), label(str(yr), font_size=16, color=GREY_B))
                     .arrange(DOWN, buff=0.05).next_to(g.ax.c2p(k + 0.5, lo), DOWN, buff=0.12))
            fmts.add(label(fmt, font_size=15, color=GREY_A).next_to(bars[-1], UP, buff=0.06))
        notes = VGroup(
            label(r"v2: \ HBM, \ bfloat16, \ training pods", font_size=20, color=GREY_A),
            label(r"v4: \ $4{,}096$ chips, \ optical switches", font_size=20, color=GREY_A),
            label(rf"Ironwood: \ ${IRONWOOD['pod']:,}$-chip pods, \ ${IRONWOOD['pod_eflops']}$ EFLOP/s (FP8)"
                  .replace(",", "{,}"), font_size=20, color=GREY_A),
            label(rf"TPU 8t (Apr 2026): \ ${TPU8T['pod']:,}$ chips, \ ${TPU8T['pod_eflops']}$ EFLOP/s (FP4)"
                  .replace(",", "{,}"), font_size=20, color=GREY_A),
        )
        for n_ in notes:
            if n_.width > 5.3:
                n_.width = 5.3
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, 0.6, 0])
        notes.shift(RIGHT * (1.4 - notes.get_left()[0]))
        others = label(rf"also: \ AWS Trainium3, \ ${TRAINIUM3['fp8'] / 1e15:.2f}$ PFLOP/s (MXFP8), \ "
                       rf"${TRAINIUM3['mem'] / 2**30:.0f}$ GiB at ${TRAINIUM3['bw'] / 1e12:.1f}$ TB/s; \ "
                       r"Microsoft Maia, \ Meta MTIA", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.3)
        if others.width > 13.2:
            others.width = 13.2
        src = cite(r"Jouppi et al.\ (2017, 2020, 2023); \ Google; \ AWS Neuron documentation", corner=UL)
        with self.voiceover(
            "The TPU was the first of many chips built only for neural networks. <bookmark mark='a'/> Google's line "
            "went from an eight-bit inference chip in 2015 to training: the TPU v2 in 2017 added high-bandwidth "
            "memory, bfloat16 and pods of chips wired together; v4 linked 4,096 of them through optical switches. "
            f"<bookmark mark='b'/> The seventh generation, Ironwood, in 2025: {IRONWOOD['fp8'] / 1e12:,.0f} trillion "
            f"eight-bit operations a second per chip, in pods of {IRONWOOD['pod']:,}. <bookmark mark='c'/> And in "
            "April 2026 Google announced two eighth-generation chips, one for training and one for serving, with "
            f"training superpods of {TPU8T['pod']:,} chips. Google trains its Gemini models on its own TPUs. "
            "<bookmark mark='d'/> Amazon builds Trainium, Microsoft Maia, Meta MTIA. Most are systolic arrays of "
            "some size, fed by high-bandwidth memory: the recipe of chapters six to eight."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(labs))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[k], DOWN), FadeIn(fmts[k])) for k in range(4)],
                                  lag_ratio=0.3), FadeIn(notes[0]), FadeIn(notes[1]), run_time=2.5)
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[k], DOWN), FadeIn(fmts[k])) for k in (4, 5)],
                                  lag_ratio=0.3))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[6], DOWN), FadeIn(fmts[6]), FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[7], DOWN), FadeIn(fmts[7]), FadeIn(notes[3]))
            vo.wait_until("d")
            self.play(FadeIn(others))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wafer(self):
        w = Circle(radius=2.4, stroke_color=GREY_B, stroke_width=2, fill_color="#1A2230", fill_opacity=1)
        w.move_to([-3.2, -0.2, 0])
        side = 2.4 * math.sqrt(2) * 0.98  # the largest square inside the wafer: WSE's whole chip
        wse = Square(side, stroke_color=FLOPC, stroke_width=2.5, fill_color=FLOPC, fill_opacity=0.12).move_to(w)
        grid = VGroup(*[Square(side / 12 * 0.9, stroke_width=0.6, stroke_color=FLOPC, fill_color=FLOPC,
                               fill_opacity=0.25) for _ in range(144)]).arrange_in_grid(rows=12, cols=12,
                                                                                        buff=side / 12 * 0.1).move_to(w)
        ratio = 46225 / 814  # die areas, mm^2: Cerebras WSE-3, NVIDIA GH100
        h100 = Square(side / math.sqrt(ratio), stroke_color=GPUC, stroke_width=2, fill_color=GPUC,
                      fill_opacity=0.6).move_to([0.6, -1.9, 0])
        hl = label(r"one H100 die, \ to scale", font_size=20, color=GPUC).next_to(h100, RIGHT, buff=0.15)
        wl = label(r"a silicon wafer, \ $300$ mm across", font_size=22, color=GREY_A).next_to(w, DOWN, buff=0.2)
        facts = VGroup(
            label(r"Cerebras WSE-3 (2024): \ one chip per wafer", font_size=26, color=FLOPC),
            label(rf"${WSE3['transistors'] / 1e12:.0f}$ trillion transistors, \ ${WSE3['cores']:,}$ cores"
                  .replace(",", "{,}"), font_size=22, color=GREY_A),
            label(rf"${WSE3['sram'] / 1e9:.0f}$ GB of SRAM on the chip itself", font_size=22, color=L1C),
            label(rf"${46225:,}$ mm$^2$, \ ${ratio:.0f}\times$ an H100's die".replace(",", "{,}"), font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, 1.2, 0])
        src = cite(r"Cerebras (March 2024)", corner=DR)
        tag = schematic_tag(corner=UL)
        with self.voiceover(
            "Others changed the shape of the chip itself. <bookmark mark='a'/> Chips are cut from a silicon wafer "
            "thirty centimetres across. Cerebras doesn't cut it: the whole wafer is one chip. "
            "<bookmark mark='b'/> Its third version, from 2024, has four trillion transistors, nine hundred thousand "
            "cores, and forty-four gigabytes of SRAM spread among them, so a model's weights can sit next to the "
            "arithmetic instead of in memory chips off to the side. <bookmark mark='c'/> It's about fifty-seven "
            "times the area of an H100's die. The hard parts were the ones everyone said were impossible: defects "
            "on a wafer that size, which it routes around, and cooling and powering it."
        ) as vo:
            self.play(FadeIn(w), FadeIn(wl), FadeIn(tag), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(wse), FadeIn(grid, lag_ratio=0.005), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f_) for f_ in facts[1:3]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(h100), FadeIn(hl), FadeIn(facts[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def groq(self):
        R = GPUS["Rubin"]
        per_lpu = GROQ3_LPX["sram_bw"] / GROQ3_LPX["lpus"]
        chips_1t = 1e12 * 0.5 / GROQ3_LPX["sram_per_lpu"]  # a trillion parameters in four bits
        bars = VGroup()
        vals = [(r"Rubin GPU: \ HBM4", R["bw"], BYTEC), (r"Groq 3 LPU: \ on-chip SRAM", per_lpu, L1C)]
        mx = max(v for _, v, _ in vals)
        labs = VGroup()
        for k, (t, v, c_) in enumerate(vals):
            w = 7.0 * v / mx
            y = 0.9 - 0.9 * k
            bars.add(Rectangle(width=w, height=0.55, stroke_width=0, fill_color=c_, fill_opacity=0.85)
                     .move_to([-3.4 + w / 2, y, 0]))
            labs.add(VGroup(label(t, font_size=22, color=c_).next_to([-3.4, y + 0.5, 0], RIGHT, buff=0.0),
                            label(rf"${v / 1e12:.0f}$ TB/s", font_size=22).next_to(bars[-1], RIGHT, buff=0.15)))
        bh = label(r"memory bandwidth per chip", font_size=24, color=GREY_A).move_to([0.0, 2.3, 0])
        cap = VGroup(
            label(rf"but ${GROQ3_LPX['sram_per_lpu'] / 1e6:.0f}$ MB per LPU, \ against ${R['mem'] / 1e9:.0f}$ GB of HBM4",
                  font_size=22, color=GREY_A),
            label(rf"a trillion parameters in four bits: \ $\approx {chips_1t:,.0f}$ LPUs".replace(",", "{,}"),
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -1.9, 0])
        hc = history_card(2016, r"Jonathan Ross founds Groq", r"after helping start the TPU at Google: \ no HBM, \ every "
                          r"weight in SRAM, \ every cycle scheduled by the compiler", width=5.0, color=L1C,
                          font_size=19).to_corner(UR, buff=0.25)
        src = cite(r"NVIDIA technical blog (March 2026); \ Groq (December 2025)", corner=DL)
        # schematic packages: a GPU with HBM stacks beside its die; an LPU with its memory on the die
        gdie = Square(1.4, stroke_color=GPUC, stroke_width=2, fill_color=GPUC, fill_opacity=0.35).move_to([-4.6, 0.4, 0])
        stacks = VGroup(*[Rectangle(width=0.42, height=0.62, stroke_color=BYTEC, stroke_width=1.5, fill_color=BYTEC,
                                    fill_opacity=0.55).move_to(gdie.get_center() + np.array([sx * 1.05, sy * 0.36, 0]))
                          for sx in (-1, 1) for sy in (-1, 1)])
        gpu_pic = VGroup(gdie, stacks)
        gpl = VGroup(label(r"GPU: \ HBM stacks", font_size=22, color=GPUC),
                     label(r"beside the die", font_size=22, color=GPUC)).arrange(DOWN, buff=0.08)
        gpl.next_to(gpu_pic, DOWN, buff=0.3)
        ldie = Square(1.9, stroke_color=L1C, stroke_width=2, fill_color="#14202A", fill_opacity=1).move_to([-0.9, 0.4, 0])
        lcells = VGroup(*[Square(0.36, stroke_width=0, fill_color=(FLOPC if j == 2 else L1C), fill_opacity=0.6)
                          for i in range(4) for j in range(5)]).arrange_in_grid(rows=4, cols=5, buff=0.04)
        lcells.move_to(ldie)
        lpu_pic = VGroup(ldie, lcells)
        lpl = VGroup(label(r"LPU: \ weights in SRAM", font_size=22, color=L1C),
                     label(r"on the die, \ no HBM", font_size=22, color=L1C)).arrange(DOWN, buff=0.08)
        lpl.next_to(lpu_pic, DOWN, buff=0.3).align_to(gpl, UP)
        ptag = schematic_tag(corner=DR)
        with self.voiceover(
            "Groq took the opposite bet from the GPU. <bookmark mark='a'/> Its founder, Jonathan Ross, had helped "
            "start the TPU project at Google. Groq's LPU has no high-bandwidth memory at all: the weights live in on-chip "
            "SRAM, and the compiler schedules every cycle in advance, so nothing waits on a cache. "
            "<bookmark mark='b'/> For writing one token at a time, the roofline's slope is everything, and SRAM is "
            "fast. In December 2025 NVIDIA licensed Groq's technology and hired its founders, and in March 2026 it "
            f"described the result: a rack of 256 Groq 3 LPUs, each with about {per_lpu / 1e12:.0f} terabytes a "
            f"second of SRAM bandwidth, against {R['bw'] / 1e12:.1f} for a Rubin GPU's memory. "
            "<bookmark mark='c'/> The price is capacity: 500 megabytes per chip. A trillion-parameter model in four "
            f"bits needs about {chips_1t:,.0f} of them. So NVIDIA pairs them: GPUs read the long prompt and keep "
            "the attention; LPUs run the rest of each new token."
        ) as vo:
            self.play(FadeIn(gpu_pic), FadeIn(gpl), FadeIn(ptag), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=DOWN * 0.1))
            self.play(FadeIn(lpu_pic), FadeIn(lpl))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(gpu_pic, gpl, lpu_pic, lpl, ptag)))
            self.play(FadeIn(bh), GrowFromEdge(bars[0], LEFT), FadeIn(labs[0]))
            self.play(GrowFromEdge(bars[1], LEFT), FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cap], lag_ratio=0.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def analog(self):
        n = 4
        pitch = 0.9
        org = np.array([-4.6, 1.6, 0])
        rows = VGroup(*[Line(org + np.array([-0.4, -i * pitch, 0]), org + np.array([(n - 1) * pitch + 0.4, -i * pitch, 0]),
                             color=C.EMBED, stroke_width=3) for i in range(n)])
        cols = VGroup(*[Line(org + np.array([j * pitch, 0.4, 0]), org + np.array([j * pitch, -(n - 1) * pitch - 0.5, 0]),
                             color=C.PROB, stroke_width=3) for j in range(n)])
        g = np.random.Generator(np.random.PCG64(4))
        cells = VGroup(*[Circle(radius=0.16, stroke_width=0, fill_color=FLOPC,
                                fill_opacity=float(0.25 + 0.7 * g.random())).move_to(org + np.array([j * pitch, -i * pitch, 0]))
                         for i in range(n) for j in range(n)])
        vin = VGroup(*[MathTex(rf"V_{i + 1}", font_size=26, color=C.EMBED).next_to(rows[i], LEFT, buff=0.1)
                       for i in range(n)])
        iout = VGroup(*[MathTex(rf"I_{j + 1}", font_size=26, color=C.PROB).next_to(cols[j], DOWN, buff=0.1)
                        for j in range(n)])
        colors = {r"I_j": C.PROB, r"V_i": C.EMBED, r"G_{ij}": FLOPC}
        law = cmath(r"I_j", r"=", r"\sum_i", r"G_{ij}", r"V_i", colors=colors, font_size=40).move_to([-3.2, -2.8, 0])
        ll = label(r"Ohm multiplies, \ Kirchhoff adds", font_size=22, color=GREY_A).next_to(law, RIGHT, buff=0.3)
        right = VGroup(
            history_card(2023, r"IBM, \ Ambrogio et al., \ \textit{Nature}", r"$35$ million phase-change memory cells "
                         r"on one chip: \ weights stored as conductances, \ speech recognition run in place",
                         width=5.8, color=FLOPC, font_size=19),
            history_card(2014, r"IBM TrueNorth", r"one million spiking neurons, \ $256$ million synapses", width=5.8,
                         color=C.MLP, font_size=19),
            history_card(2024, r"Intel Hala Point", r"$1{,}152$ Loihi 2 chips: \ $1.15$ billion neurons", width=5.8,
                         color=C.MLP, font_size=19),
        ).arrange(DOWN, buff=0.25).move_to([3.6, 0.1, 0])
        tag = schematic_tag(corner=UL)
        with self.voiceover(
            "Two older dreams are still being chased. <bookmark mark='a'/> Analog computing in memory: store each "
            "weight as the conductance of a cell in a grid, apply the inputs as voltages on the rows, and by Ohm's "
            "law each cell's current is a product; by Kirchhoff's law the currents on a column add up. "
            "<bookmark mark='b'/> A whole matrix-vector product in one step, with no weights moved at all. In 2023 "
            "IBM ran speech recognition on a chip with thirty-five million such cells; the hard parts are noise and "
            "precision. <bookmark mark='c'/> And neuromorphic chips compute with spikes, like neurons, and only "
            "when something changes: IBM's TrueNorth in 2014, Intel's Loihi, and in 2024 Hala Point, with over a "
            "billion artificial neurons. Neither runs today's frontier models. Both are bets on chapter six's "
            "lesson: the cheapest data movement is none."
        ) as vo:
            self.play(FadeIn(rows), FadeIn(cols), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cells, lag_ratio=0.05), FadeIn(vin))
            self.play(FadeIn(iout), Write(law), FadeIn(ll))
            vo.wait_until("b")
            self.play(FadeIn(right[0], shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(right[1], shift=LEFT * 0.2))
            self.play(FadeIn(right[2], shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()
