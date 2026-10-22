from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import (BYTEC, CPUC, FLOPC, GPUC, L1C, L2C, L3C, PART, REGC, load, machine_name)
from videos.ai.ai17.specs import CC90, ENERGY_PJ, GPUS, H800_LAT


class Hierarchy(VoiceoverScene, MovingCameraScene):
    def construct(self):
        self.card()
        self.zoom()
        self.hbm()
        self.staircase()
        self.energy()

    def card(self):
        card = chapter_card(6, r"The memory hierarchy", r"Why is there more than one kind of memory?", part=PART)
        with self.voiceover("Chapter six. The memory hierarchy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def build_gpu(self):
        pkg = RoundedRectangle(width=10.6, height=5.6, corner_radius=0.2, stroke_color=GREY_C, stroke_width=2,
                               fill_color="#121722", fill_opacity=1)
        die = Rectangle(width=4.4, height=3.6, stroke_color=GPUC, stroke_width=2, fill_color="#16202B",
                        fill_opacity=1)
        hbm = VGroup(*[RoundedRectangle(width=1.3, height=1.45, corner_radius=0.08, stroke_color=BYTEC,
                                        stroke_width=2, fill_color=BYTEC, fill_opacity=0.35) for _ in range(6)])
        left = VGroup(*hbm[:3]).arrange(DOWN, buff=0.2).next_to(die, LEFT, buff=0.55)
        right = VGroup(*hbm[3:]).arrange(DOWN, buff=0.2).next_to(die, RIGHT, buff=0.55)
        # the die: two banks of SMs and the L2 between them
        sm_w, sm_h = 0.42, 0.3
        top = VGroup(*[Rectangle(width=sm_w, height=sm_h, stroke_color=GPUC, stroke_width=0.8, fill_color=GPUC,
                                 fill_opacity=0.18) for _ in range(36)]).arrange_in_grid(rows=4, cols=9, buff=0.04)
        bot = top.copy()
        l2 = Rectangle(width=4.0, height=0.34, stroke_width=0, fill_color=L2C, fill_opacity=0.55)
        body = VGroup(top, l2, bot).arrange(DOWN, buff=0.08).move_to(die)
        sm = top[13]
        # inside one SM: four processing blocks (registers, lanes, a tensor core), shared memory / L1 along the bottom
        inner = VGroup()
        bw, bh = sm_w * 0.44, sm_h * 0.3
        for q in range(4):
            blk = VGroup(Rectangle(width=bw, height=bh, stroke_color=GPUC, stroke_width=0.3, fill_opacity=0))
            reg = Rectangle(width=bw * 0.36, height=bh * 0.8, stroke_width=0, fill_color=REGC, fill_opacity=0.8)
            lanes = Rectangle(width=bw * 0.3, height=bh * 0.8, stroke_width=0, fill_color=FLOPC, fill_opacity=0.5)
            tc = Rectangle(width=bw * 0.2, height=bh * 0.8, stroke_width=0, fill_color=FLOPC, fill_opacity=0.95)
            VGroup(reg, lanes, tc).arrange(RIGHT, buff=bw * 0.04).move_to(blk[0])
            blk.add(reg, lanes, tc)
            inner.add(blk)
        inner.arrange_in_grid(rows=2, cols=2, buff=sm_w * 0.03)
        smem = Rectangle(width=sm_w * 0.92, height=sm_h * 0.2, stroke_width=0, fill_color=L1C, fill_opacity=0.8)
        VGroup(inner, smem).arrange(DOWN, buff=sm_h * 0.04).move_to(sm)
        g = VGroup(pkg, die, hbm, body, inner, smem)
        g.pkg, g.die, g.hbm, g.l2, g.sm, g.inner, g.smem = pkg, die, hbm, l2, sm, inner, smem
        return g

    def zoom(self):
        g = self.build_gpu()
        g.inner.set_opacity(0)
        g.smem.set_opacity(0)
        h = GPUS["H100"]
        k1 = label(rf"HBM3: \ ${h['mem'] / 1e9:.0f}$ GB \ at ${h['bw'] / 1e12:.2f}$ TB/s", font_size=26, color=BYTEC)
        k1.next_to(g.pkg, UP, buff=0.15)
        k1b = label(rf"stacked DRAM beside the die: \ about ${H800_LAT['glob']:.0f}$ cycles away", font_size=22,
                    color=GREY_A).next_to(g.pkg, DOWN, buff=0.15)
        tag = note(r"an H100, \ schematic; \ latencies measured on an H800 (Luo et al.\ 2024)").to_corner(DL, buff=0.2)
        z2 = g.die.width * 2.3  # the frame's width at the second zoom
        s2 = z2 / 14.22  # label scale there
        k2 = label(rf"L2 cache: \ ${CC90['l2'] / 1e6:.0f}$ MB, \ about ${H800_LAT['l2']:.0f}$ cycles", font_size=26,
                   color=L2C).scale(s2).next_to(g.die, UP, buff=0.15)
        k2b = label(rf"$132$ streaming multiprocessors", font_size=24, color=GPUC).scale(s2).next_to(g.die, DOWN,
                                                                                                      buff=0.3 * s2)
        s3 = g.sm.width * 2.4 / 14.22
        k3 = VGroup(
            label(r"registers: \ $64$K $\times$ $4$ bytes $= 256$ KB, \ one cycle", font_size=24, color=REGC),
            label(rf"shared memory and L1: \ $256$ KB, \ about ${H800_LAT['l1']:.0f}$ cycles", font_size=24,
                  color=L1C),
            label(r"lanes and a tensor core in each quarter", font_size=24, color=FLOPC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).scale(s3).next_to(g.sm, RIGHT, buff=0.15 * s3 * 4)
        bg3 = BackgroundRectangle(k3, color=BACKGROUND, fill_opacity=0.9, buff=0.04 * s3 * 4)
        with self.voiceover(
            "A GPU's memory is not one thing. Let's zoom in on an H100. <bookmark mark='a'/> Around the chip sit "
            f"stacks of high-bandwidth memory, DRAM dies piled on top of each other: {h['mem'] / 1e9:.0f} gigabytes, "
            f"read at {h['bw'] / 1e12:.2f} terabytes a second, but hundreds of cycles away. <bookmark mark='b'/> On "
            "the chip itself, a level-two cache of fifty megabytes, shared by all 132 streaming multiprocessors, "
            "about half as far. <bookmark mark='c'/> Inside each multiprocessor: 256 kilobytes of shared memory, "
            "which the programmer fills on purpose, about forty cycles away; <bookmark mark='d'/> and the "
            "registers, another 256 kilobytes, right next to the arithmetic, read every cycle. Each step down is "
            "smaller and closer, and much faster to read."
        ) as vo:
            self.play(FadeIn(g.pkg), FadeIn(g.die), FadeIn(g[3]), FadeIn(g.hbm, lag_ratio=0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(k1), FadeIn(k1b), Indicate(g.hbm, color=BYTEC, scale_factor=1.03))
            vo.wait_until("b")
            self.play(frame_to(self, g.die, width=z2), FadeOut(tag), run_time=2.0)
            self.play(FadeIn(k2), FadeIn(k2b), Indicate(g.l2, color=L2C, scale_factor=1.02))
            vo.wait_until("c")
            self.play(frame_to(self, center=g.sm.get_center() + RIGHT * g.sm.width * 0.7, width=g.sm.width * 2.4),
                      run_time=2.5)
            self.play(g.inner.animate.set_opacity(1), g.smem.animate.set_opacity(0.8), FadeIn(bg3), FadeIn(k3[1]),
                      FadeIn(k3[2]))
            vo.wait_until("d")
            self.play(FadeIn(k3[0]), *[Indicate(b_[1], color=REGC, scale_factor=1.2) for b_ in g.inner])
        self.wait(0.5)
        self.play(frame_home(self), run_time=1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hbm(self):
        gens = ["P100", "V100", "A100", "H100", "GB200", "Rubin"]
        cap = [GPUS[g_]["mem"] / 1e9 for g_ in gens]
        bw = [GPUS[g_]["bw"] / 1e12 for g_ in gens]
        # a stack: DRAM dies on a base die, beside the GPU on a silicon interposer (schematic)
        inter = Rectangle(width=5.4, height=0.25, stroke_width=0, fill_color=GREY_C, fill_opacity=0.6)
        inter.move_to([-3.6, -1.6, 0])
        gpu = Rectangle(width=2.4, height=0.9, stroke_color=GPUC, fill_color=GPUC, fill_opacity=0.35)
        gpu.next_to(inter, UP, buff=0.0).align_to(inter, RIGHT).shift(LEFT * 0.3)
        dies = VGroup(*[Rectangle(width=1.6, height=0.22, stroke_color=BYTEC, stroke_width=1.2, fill_color=BYTEC,
                                  fill_opacity=0.45) for _ in range(9)]).arrange(UP, buff=0.04)
        dies.next_to(inter, UP, buff=0.0).align_to(inter, LEFT).shift(RIGHT * 0.3)
        vias = VGroup(*[Line(dies.get_bottom() + RIGHT * x, dies.get_top() + RIGHT * x, stroke_width=1.2,
                             color=FLOPC) for x in (-0.5, -0.2, 0.1, 0.4)])
        wires = VGroup(*[Line(dies.get_corner(DR) + UP * 0.04 * k + RIGHT * 0.0, gpu.get_corner(DL) + UP * 0.04 * k,
                              stroke_width=1, color=C.CURRENT) for k in range(1, 5)])
        labs = VGroup(label(r"DRAM dies, \ stacked", font_size=20, color=BYTEC).next_to(dies, UP, buff=0.15),
                      label(r"GPU", font_size=20, color=GPUC).move_to(gpu),
                      label(r"silicon interposer: \ thousands of short wires", font_size=18, color=GREY_A)
                      .next_to(inter, DOWN, buff=0.15),
                      label(r"through-silicon vias", font_size=18, color=FLOPC).next_to(dies, LEFT, buff=0.2))
        tag = schematic_tag(corner=UL)
        g = axes([-0.5, 5.5], [0, 300], x_length=5.2, y_length=3.2, ylabel=r"GB per GPU \ (bars)",
                 xticks=list(range(6)), xfmt=lambda v: gens[int(v)], yticks=[0, 100, 200, 300],
                 center=[3.6, 0.3, 0], font_size=18)
        bars = VGroup(*[Rectangle(width=0.5, height=g.ax.c2p(0, c_)[1] - g.ax.c2p(0, 0)[1], stroke_width=0,
                                  fill_color=BYTEC, fill_opacity=0.7).move_to([g.ax.c2p(k, 0)[0],
                                                                               (g.ax.c2p(0, c_)[1] + g.ax.c2p(0, 0)[1]) / 2, 0])
                        for k, c_ in enumerate(cap)])
        bwl = VGroup(*[label(rf"${b_:.1f}$", font_size=18, color=FLOPC).next_to(bars[k], UP, buff=0.08)
                       for k, b_ in enumerate(bw)])
        bwk = label(r"numbers: \ TB/s", font_size=18, color=FLOPC).next_to(g, RIGHT, buff=0.1).shift(UP * 1.0)
        cite_ = cite(r"NVIDIA datasheets and product pages", corner=DR)
        with self.voiceover(
            "That memory is a feat of its own. <bookmark mark='a'/> High-bandwidth memory stacks DRAM dies on top of "
            "each other, wired straight through the silicon, and sets the stack right beside the GPU on a slab of "
            "silicon with thousands of short wires: far more of them than a circuit board could carry. AMD first "
            "used it in a graphics card in 2015. <bookmark mark='b'/> Since the P100, the memory per GPU has grown "
            f"from {cap[0]:.0f} gigabytes to {cap[-1]:.0f} for Rubin, and its bandwidth from {bw[0]:.2f} terabytes a "
            f"second to {bw[-1]:.1f}: about {bw[-1] / bw[0]:.0f} times in ten years. It's the most expensive part of "
            "the package, and, as we'll see, the scarcest resource."
        ) as vo:
            self.play(FadeIn(inter), FadeIn(gpu), FadeIn(tag), FadeIn(labs[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, shift=DOWN * 0.2) for d_ in dies], lag_ratio=0.15), FadeIn(labs[0]))
            self.play(Create(vias), FadeIn(labs[3]), Create(wires), FadeIn(labs[2]))
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(cite_), FadeIn(bwk))
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_, DOWN), FadeIn(l_)) for b_, l_ in zip(bars, bwl)],
                                  lag_ratio=0.3), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def staircase(self):
        h, m = load("hierarchy"), load("machine")
        sizes, bw, lat = np.asarray(h["sizes"], float), np.asarray(h["bandwidth"]), np.asarray(h["latency"])
        x = np.log2(sizes / 1024)
        caches = [(k, v["kib"]) for k, v in sorted(m["caches"].items())]
        colors = {"L1": L1C, "L2": L2C, "L3": L3C}
        g1 = axes([x[0] - 0.3, x[-1] + 0.3], [0, max(bw) / 1e9 * 1.15], x_length=5.6, y_length=3.3,
                  xlabel=r"data size", ylabel=r"reading speed, \ GB/s", xticks=[2, 5, 10, 15, 18],
                  xfmt=lambda v: {2: r"4\,\text{KiB}", 5: r"32\,\text{KiB}", 10: r"1\,\text{MiB}",
                                  15: r"32\,\text{MiB}", 18: r"256\,\text{MiB}"}[int(v)],
                  yticks=[0, 50 * math.floor(max(bw) / 5e10)], center=[-3.4, -0.4, 0])
        g2 = axes([x[0] - 0.3, x[-1] + 0.3], [0, math.log10(max(lat) * 1e9) + 0.2], x_length=5.6, y_length=3.3,
                  xlabel=r"data size", ylabel=r"time per random read, \ ns (log)", xticks=[2, 5, 10, 15, 18],
                  xfmt=lambda v: {2: r"4\,\text{KiB}", 5: r"32\,\text{KiB}", 10: r"1\,\text{MiB}",
                                  15: r"32\,\text{MiB}", 18: r"256\,\text{MiB}"}[int(v)],
                  yticks=[0, 1, 2], yfmt=lambda v: {0: "1", 1: "10", 2: "100"}[int(v)], center=[3.6, -0.4, 0])
        c1 = VGroup(*[Dot(g1.ax.c2p(a, b / 1e9), radius=0.05, color=BYTEC) for a, b in zip(x, bw)])
        c2 = VGroup(*[Dot(g2.ax.c2p(a, math.log10(t * 1e9)), radius=0.05, color=C.SURPRISE) for a, t in zip(x, lat)])
        l1 = VMobject(color=BYTEC, stroke_width=2).set_points_as_corners([d.get_center() for d in c1])
        l2 = VMobject(color=C.SURPRISE, stroke_width=2).set_points_as_corners([d.get_center() for d in c2])
        marks = VGroup()
        for gg in (g1, g2):
            for nm, kib in caches:
                xx = math.log2(kib)
                top = gg.ax.get_bottom()[1] + gg.ax.height
                ln = DashedLine([gg.ax.c2p(xx, 0)[0], gg.ax.get_bottom()[1], 0], [gg.ax.c2p(xx, 0)[0], top, 0],
                                color=colors.get(nm, GREY_B), dash_length=0.08)
                marks.add(VGroup(ln, label(nm, font_size=18, color=colors.get(nm, GREY_B)).next_to(ln, UP, buff=0.05)))
        title = label(rf"one core of this computer \ ({machine_name()})", font_size=26, color=CPUC).to_edge(UP, buff=0.4)
        busy = bool(h["loadavg_before"]) and h["loadavg_before"][0] > 0.5 * m["cores"]
        tag = note(r"computed: \ best of several passes" + (r" \ (other jobs were running)" if busy else ""))
        tag.to_corner(DR, buff=0.2)

        def plateau(lo_kib, hi_kib, arr):
            sel = (sizes / 1024 >= lo_kib) & (sizes / 1024 <= hi_kib)
            return float(np.median(arr[sel])) if sel.any() else float("nan")

        L1k = dict(caches).get("L1", 32)
        L2k = dict(caches).get("L2", 1024)
        b1, b2, bd = plateau(4, L1k, bw), plateau(L1k * 2, L2k / 2, bw), plateau(64 * 1024, 1e9, bw)
        t1, t2, td = plateau(4, L1k, lat), plateau(L1k * 2, L2k / 2, lat), plateau(64 * 1024, 1e9, lat)
        fast = sizes[lat < td / 2]
        last_mib = float(fast.max()) / 2 ** 20 if fast.size else 0.0
        L3k = dict(caches).get("L3")
        if L3k and last_mib < L3k / 1024 / 2:
            tail = (f"The last level is nominally {L3k / 1024:.0f} megabytes, but it's shared by every core on the "
                    f"chip, and here our walk leaves it after about {last_mib:.0f}.")
        elif L3k:
            tail = f"The last level holds up to about its {L3k / 1024:.0f} megabytes."
        else:
            tail = "The last level is shared by every core on the chip."
        with self.voiceover(
            "We can see the same hierarchy on this computer's own processor, by timing it. <bookmark mark='a'/> On "
            "the left, one core reads an array over and over and adds it up; the array grows from four kilobytes to "
            f"256 megabytes. While it fits in the first-level cache, about {b1 / 1e9:.0f} gigabytes a second. "
            f"Past that, from the second level, about {b2 / 1e9:.0f}. From main memory, about {bd / 1e9:.0f}. "
            "<bookmark mark='b'/> On the right, the same core follows a chain of pointers in random order, so "
            f"every read waits for the one before. In the first-level cache, a read takes about {t1 * 1e9:.1f} "
            f"nanoseconds; in the second, about {t2 * 1e9:.0f}; in main memory, about {td * 1e9:.0f}. "
            "<bookmark mark='c'/> The dashed lines are the cache sizes the processor reports. " + tail
        ) as vo:
            self.play(FadeIn(title), FadeIn(g1), FadeIn(g2), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in c1], lag_ratio=0.05), Create(l1), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in c2], lag_ratio=0.05), Create(l2), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(marks))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def energy(self):
        rows = ENERGY_PJ
        mx = math.log10(max(v for _, v in rows))
        bars = VGroup()
        names = VGroup()
        vals = VGroup()
        cols = [FLOPC, FLOPC, FLOPC, FLOPC, L1C, BYTEC]
        for k, (nm, v) in enumerate(rows):
            w = 1.2 + 6.0 * (math.log10(v) + 1) / (mx + 1)
            y = 1.9 - 0.75 * k
            bars.add(Rectangle(width=w, height=0.45, stroke_width=0, fill_color=cols[k], fill_opacity=0.85)
                     .move_to([-1.2 + w / 2, y, 0]))
            names.add(label(nm, font_size=22, color=cols[k]).next_to([-1.4, y, 0], LEFT, buff=0.1))
            vals.add(label(rf"${v:g}$ pJ", font_size=22, color=WHITE).next_to(bars[-1], RIGHT, buff=0.15))
        head = label(r"energy per operation, \ $45$ nm \ (log scale)", font_size=28).to_edge(UP, buff=0.4)
        ratio = ENERGY_PJ[-1][1] / ENERGY_PJ[3][1]
        take = label(rf"one read from DRAM $\approx$ ${ratio:.0f}$ floating-point multiplies", font_size=28,
                     color=BYTEC).to_edge(DOWN, buff=0.6)
        cite_ = cite(r"M.~Horowitz, ISSCC (2014), \ as tabulated by Han et al.\ (2016)", corner=DR)
        with self.voiceover(
            "Why build it this way? Distance costs energy. <bookmark mark='a'/> Mark Horowitz tabulated what each "
            "operation costs on a 45-nanometre chip. Adding two 32-bit numbers: a tenth of a picojoule. Multiplying "
            "two floats: 3.7. <bookmark mark='b'/> Reading 32 bits from a small on-chip memory: about five. "
            "<bookmark mark='c'/> Reading them from DRAM: 640, as much as about "
            f"{ratio:.0f} multiplies. The arithmetic is cheap; moving the numbers is what costs. The newer chips "
            "change the numbers, not the ratio's lesson: every byte fetched from far away has to be used many times."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[k], LEFT), FadeIn(names[k]), FadeIn(vals[k]))
                                    for k in range(4)], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[4], LEFT), FadeIn(names[4]), FadeIn(vals[4]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[5], LEFT), FadeIn(names[5]), FadeIn(vals[5]))
            self.play(FadeIn(take, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
