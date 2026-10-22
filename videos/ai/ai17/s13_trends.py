from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import BYTEC, FLOPC, GPUC, PART, POWERC, load
from videos.ai.ai17.specs import (EPOCH_TRENDS, GPUS, IEA, LLAMA31_GPUS, LLAMA31_MW, MEMORY_WALL, NVL72_RUBIN)


def fit_line(ax, t, y, color, t0, t1):
    k, b = np.polyfit(t, np.log10(y), 1)
    return DashedLine(ax.c2p(t0, k * t0 + b), ax.c2p(t1, k * t1 + b), color=color, dash_length=0.1)


class Trends(VoiceoverScene):
    def construct(self):
        self.card()
        self.flops_vs_bw()
        self.ridges()
        self.energy()
        self.power()

    def card(self):
        card = chapter_card(12, r"FLOPs, dollars and watts", r"How fast is the hardware improving, and at what cost?",
                            lit=(2020, 2024), part=PART)
        with self.voiceover("Chapter twelve. FLOPs, dollars and watts."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def flops_vs_bw(self):
        t = load("trends")
        yr, ten, bw = np.asarray(t["acc_year"]), np.asarray(t["acc_tensor"]), np.asarray(t["acc_bw"])
        okt, okb = np.isfinite(ten), np.isfinite(bw)
        g = axes([2016.5, 2026.5], [11, 16], x_length=6.6, y_length=4.6, xlabel=r"release",
                 ylabel=r"per second \ (log scale)", xticks=[2017, 2020, 2023, 2026], yticks=[11, 12, 13, 14, 15, 16],
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.6, -0.3, 0])
        dt = VGroup(*[Dot(g.ax.c2p(a, math.log10(b)), radius=0.06, color=FLOPC) for a, b in zip(yr[okt], ten[okt])])
        db = VGroup(*[Dot(g.ax.c2p(a, math.log10(b)), radius=0.06, color=BYTEC) for a, b in zip(yr[okb], bw[okb])])
        ft = fit_line(g.ax, yr[okt], ten[okt], FLOPC, 2017, 2026.3)
        fb = fit_line(g.ax, yr[okb], bw[okb], BYTEC, 2017, 2026.3)
        Tt, Tb, Tr = t["tensor_doubling"], t["bw_doubling"], t["ridge_doubling"]
        lt = label(rf"16-bit tensor FLOP/s: \ doubling every ${Tt:.1f}$ years", font_size=22, color=FLOPC)
        lb = label(rf"memory bytes/s: \ every ${Tb:.1f}$ years", font_size=22, color=BYTEC)
        lgrp = VGroup(lt, lb).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, 1.9, 0])
        lgrp.shift(RIGHT * (1.5 - lgrp.get_left()[0]))
        ep = VGroup(label(rf"Epoch AI, $47$ accelerators to 2023: \ ${EPOCH_TRENDS['flops_doubling']}$ vs "
                          rf"${EPOCH_TRENDS['bw_doubling']:.0f}$ years", font_size=19, color=GREY_A),
                    label(rf"Gholami et al.\ (2024), $20$ years: \ ${MEMORY_WALL['flops']}\times$ vs "
                          rf"${MEMORY_WALL['dram']}\times$ per two years", font_size=19, color=GREY_A))
        for m_ in ep:
            if m_.width > 5.3:
                m_.width = 5.3
        ep.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, -1.3, 0])
        ep.shift(RIGHT * (1.5 - ep.get_left()[0]))
        src = cite(rf"data: \ Epoch AI, \textit{{ML hardware}} (CC BY): \ ${t['n_tensor']}$ flagships of NVIDIA, Google, "
                   r"AMD, Amazon", corner=DL)
        with self.voiceover(
            "How fast is all this improving? <bookmark mark='a'/> Here are the flagship accelerators of NVIDIA, "
            "Google, AMD and Amazon since 2017, from Epoch AI's database. Their sixteen-bit tensor arithmetic doubled "
            f"every {Tt:.1f} years. <bookmark mark='b'/> Their memory bandwidth doubled every {Tb:.1f}. "
            "<bookmark mark='c'/> Arithmetic is outrunning memory. Epoch's own study of forty-seven accelerators "
            "found the same, 2.3 years against four, and Amir Gholami and colleagues, looking back twenty years, "
            "called it the memory wall. <bookmark mark='d'/> So the ridge of the roofline keeps moving right: "
            f"in this data the operations a chip can do per byte it reads doubled every {Tr:.1f} years. Each "
            "generation needs more reuse to stay busy."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dt], lag_ratio=0.08), run_time=2.0)
            self.play(Create(ft), FadeIn(lt))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in db], lag_ratio=0.08), run_time=2.0)
            self.play(Create(fb), FadeIn(lb))
            vo.wait_until("c")
            self.play(FadeIn(ep))
            vo.wait_until("d")
            self.play(Indicate(VGroup(ft, fb), scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ridges(self):
        rows_ = [("V100", "tensor", r"FP16"), ("A100", "tensor", r"BF16"), ("H100", "fp8", r"FP8"),
                 ("GB200", "fp4", r"FP4"), ("Rubin", "fp4", r"NVFP4")]
        vals = [GPUS[g_][k] / GPUS[g_]["bw"] for g_, k, _ in rows_]
        b16 = [GPUS[g_]["tensor"] / GPUS[g_]["bw"] for g_, _, _ in rows_]
        mx = math.log10(max(vals))
        bars, labs, nums, bars16 = VGroup(), VGroup(), VGroup(), VGroup()
        for k, ((g_, _, fmt), v, v16) in enumerate(zip(rows_, vals, b16)):
            y = 1.7 - 0.85 * k
            w = 7.0 * math.log10(v) / mx
            w16 = 7.0 * math.log10(v16) / mx
            bars.add(Rectangle(width=w, height=0.5, stroke_width=0, fill_color=FLOPC, fill_opacity=0.85)
                     .move_to([-2.6 + w / 2, y, 0]))
            bars16.add(Rectangle(width=w16, height=0.5, stroke_width=2, stroke_color=GPUC, fill_opacity=0)
                       .move_to([-2.6 + w16 / 2, y, 0]))
            labs.add(label(rf"{g_} \ ({GPUS[g_]['year']}), \ {fmt}", font_size=22, color=GREY_A)
                     .next_to([-2.8, y, 0], LEFT, buff=0.1))
            nums.add(label(rf"${v:,.0f}$".replace(",", "{,}"), font_size=22).next_to(bars[-1], RIGHT, buff=0.15))
        head = label(r"the ridge: \ peak FLOP/s $\div$ memory bytes/s \ (log scale)", font_size=26).to_edge(UP, buff=0.4)
        key = VGroup(label(r"filled: \ in each chip's smallest format", font_size=20, color=FLOPC),
                     label(r"outline: \ in 16-bit", font_size=20, color=GPUC)).arrange(RIGHT, buff=0.6)
        key.move_to([-0.6, -2.3, 0])
        cite_ = cite(r"NVIDIA datasheets and product pages; \ dense figures", corner=DR)
        with self.voiceover(
            "Here's the ridge, generation by generation, from the datasheets. <bookmark mark='a'/> In sixteen-bit "
            f"numbers it moved from about {b16[0]:.0f} operations per byte for a V100 to about {b16[3]:.0f} for a "
            "Blackwell GPU. <bookmark mark='b'/> But each generation also added a smaller format, and in its "
            f"smallest format the ridge has climbed to about {vals[-1]:,.0f} for Rubin. Smaller numbers do double "
            "duty: twice the arithmetic per cycle, and half the bytes per number, which is what brings a workload "
            "back up to the ridge."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(labs))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b_) for b_ in bars16], lag_ratio=0.2), FadeIn(key[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, LEFT) for b_ in bars], lag_ratio=0.2), FadeIn(nums), FadeIn(key[0]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def energy(self):
        t = load("trends")
        yr, ten, tdp = np.asarray(t["acc_year"]), np.asarray(t["acc_tensor"]), np.asarray(t["acc_tdp"])
        ok = np.isfinite(ten) & np.isfinite(tdp)
        eff = ten[ok] / tdp[ok]
        g = axes([2016.5, 2026.5], [11, 13.5], x_length=6.4, y_length=4.0, xlabel=r"release",
                 ylabel=r"16-bit FLOP/s per watt \ (log)", xticks=[2017, 2020, 2023, 2026], yticks=[11, 12, 13],
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.6, -0.2, 0])
        dots = VGroup(*[Dot(g.ax.c2p(a, math.log10(e)), radius=0.06, color=POWERC) for a, e in zip(yr[ok], eff)])
        fl = fit_line(g.ax, yr[ok], eff, POWERC, 2017, 2026.3)
        Te = t["eff_doubling"]
        H, X = GPUS["H100"], GPUS["GTX 580"]
        pj_h = H["watts"] / H["tensor"] * 1e12
        pj_x = X["watts"] / X["fp32"] * 1e12
        facts = VGroup(label(rf"doubling every ${Te:.1f}$ years \ (Epoch: ${EPOCH_TRENDS['energy_doubling']:.0f}$)",
                             font_size=22, color=POWERC),
                       label(rf"GTX 580 (2010, FP32): \ ${pj_x:.0f}$ pJ per FLOP", font_size=22, color=GREY_A),
                       label(rf"H100 (2022, BF16): \ ${pj_h:.1f}$ pJ per FLOP", font_size=22, color=GPUC),
                       label(r"at full power, \ arithmetic only", font_size=18, color=GREY_B))
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.0, 0.4, 0])
        src = cite(r"Epoch AI (TDP and peak dense FLOP/s); \ datasheets", corner=DL)
        with self.voiceover(
            "What about energy? <bookmark mark='a'/> Divide each chip's peak by its power: sixteen-bit operations "
            f"per second per watt doubled every {Te:.1f} years in this data; Epoch found three. "
            "<bookmark mark='b'/> The graphics card AlexNet trained on spent about "
            f"{pj_x:.0f} picojoules per floating-point operation. An H100 spends about {pj_h:.1f}: about "
            f"{round(pj_x / pj_h, -1):.0f} times less, partly by using fewer bits. Chapter six's lesson still holds, "
            "though: fetching the operands from memory "
            "costs more than the arithmetic. Price-performance, by Epoch's count, doubles about every two years."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.08), run_time=2.0)
            self.play(Create(fl), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f_) for f_ in facts[1:]], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def power(self):
        gw = IEA["twh_2024"] * 1e12 / (365.25 * 24) / 1e9
        per_gpu = NVL72_RUBIN["factory_mw"] * 1e6 / NVL72_RUBIN["factory_gpus"]
        bars = LiveBars([IEA["twh_2024"], IEA["twh_2030"]], max_value=1000, height=3.2, bar_width=1.3, gap=1.6, colors=[POWERC, POWERC],
                        show_values=True, digits=0, value_font=28, labels=[r"2024", r"2030 (projected)"],
                        label_font=22)
        bars.place(base_y=-2.4, x=-3.6)
        bl = label(r"data centres worldwide, \ TWh a year", font_size=22, color=POWERC).move_to([-3.6, 1.6, 0])
        facts = VGroup(
            label(rf"2024: \ ${IEA['twh_2024']}$ TWh, \ about ${IEA['share_2024']}\%$ of the world's electricity, \\ "
                  rf"$\approx {gw:.0f}$ GW on average", font_size=22, color=GREY_A),
            label(rf"Llama 3.1's ${LLAMA31_GPUS:,}$ H100s: \ $\approx {LLAMA31_MW:.0f}$ MW \ (Epoch's estimate)"
                  .replace(",", "{,}"), font_size=22, color=GREY_A),
            label(rf"a Rubin \textit{{AI factory}}: \ ${NVL72_RUBIN['factory_mw']}$ MW for "
                  rf"${NVL72_RUBIN['factory_gpus']:,}$ GPUs, \\ $\approx {per_gpu / 1e3:.1f}$ kW each, all in"
                  .replace(",", "{,}"), font_size=22, color=GPUC),
        )
        for f_ in facts:
            if f_.width > 6.4:
                f_.width = 6.4
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, 0.0, 0])
        src = cite(r"IEA, \textit{Energy and AI} (2025); \ Epoch AI; \ NVIDIA", corner=DR)
        with self.voiceover(
            "And then there's the electricity. <bookmark mark='a'/> The International Energy Agency estimated that "
            f"data centres used about {IEA['twh_2024']} terawatt-hours in 2024, about one and a half percent of the "
            f"world's electricity, and projected about {IEA['twh_2030']} by 2030, with AI the main driver. "
            "<bookmark mark='b'/> Training Llama 3.1 took a cluster drawing an estimated twenty-odd megawatts. "
            "<bookmark mark='c'/> NVIDIA now describes its Rubin systems in units of a hundred-megawatt AI factory: "
            f"forty thousand GPUs, about {per_gpu / 1e3:.1f} kilowatts each once cooling and networking are "
            "counted. The constraint on building AI is increasingly the power line."
        ) as vo:
            self.play(FadeIn(bl), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(bars, shift=UP * 0.2), FadeIn(facts[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()
