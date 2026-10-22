from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import BYTEC, COMMC, CPUC, FLOPC, GPUC, L1C, PART, POWERC, box_label, load
from videos.ai.ai17.specs import GPUS, GROQ3_LPX, IRONWOOD, NVL72_GB200, NVL72_RUBIN, TPU8I, TPU8T


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.blackwell()
        self.rubin()
        self.domains()
        self.split()

    def card(self):
        card = chapter_card(14, r"The frontier, late 2026", r"What does a computer built for AI look like now?",
                            lit=(2025, 2026), part=PART)
        with self.voiceover("Chapter fourteen. The frontier, late 2026."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def blackwell(self):
        d1 = Rectangle(width=2.0, height=2.6, stroke_color=GPUC, stroke_width=2, fill_color=GPUC, fill_opacity=0.15)
        d2 = d1.copy()
        dies = VGroup(d1, d2).arrange(RIGHT, buff=0.25).move_to([-3.6, 0.4, 0])
        link = VGroup(*[Line(d1.get_right() + UP * y, d2.get_left() + UP * y, color=COMMC, stroke_width=3)
                        for y in np.linspace(-1.0, 1.0, 9)])
        hbm = VGroup(*[RoundedRectangle(width=0.7, height=0.55, corner_radius=0.06, stroke_color=BYTEC,
                                        fill_color=BYTEC, fill_opacity=0.35) for _ in range(8)])
        top, bot = VGroup(*hbm[:4]).arrange(RIGHT, buff=0.15), VGroup(*hbm[4:]).arrange(RIGHT, buff=0.15)
        top.next_to(dies, UP, buff=0.2)
        bot.next_to(dies, DOWN, buff=0.2)
        dl = label(r"two dies, \ one GPU", font_size=24, color=GPUC).next_to(bot, DOWN, buff=0.2)
        ll = label(r"$10$ TB/s between them", font_size=20, color=COMMC).next_to(top, UP, buff=0.15)
        G = GPUS["GB200"]
        facts = VGroup(
            label(r"Blackwell \ (announced March 2024)", font_size=28, color=GPUC),
            label(r"$208$ billion transistors", font_size=22, color=GREY_A),
            label(rf"per GPU: \ ${G['fp4'] / 1e15:.0f}$ PFLOP/s in FP4, \ ${G['tensor'] / 1e15:.1f}$ in BF16 \ (dense)",
                  font_size=22, color=FLOPC),
            label(rf"GB200 NVL72: \ ${NVL72_GB200['gpus']}$ GPUs, \ one NVLink domain, \ "
                  rf"${NVL72_GB200['nvlink'] / 1e12:.0f}$ TB/s, \ liquid-cooled", font_size=22, color=COMMC),
            label(r"Blackwell Ultra (2025): \ $288$ GB of HBM3E per GPU", font_size=22, color=BYTEC),
        )
        for f_ in facts:
            if f_.width > 6.6:
                f_.width = 6.6
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.2, 0.4, 0])
        tag = schematic_tag(corner=UL)
        cite_ = cite(r"NVIDIA Blackwell architecture, GB200 and GB300 NVL72 pages", corner=DR)
        with self.voiceover(
            "Where does all this stand at the end of 2026? <bookmark mark='a'/> NVIDIA's Blackwell, announced in "
            "March 2024, hit the limit of chipmaking: a die can't be larger than the area a lithography machine "
            "exposes at once. So Blackwell is two dies at that limit, joined by ten terabytes a second so they act "
            "as one GPU: 208 billion transistors, with tensor cores for four-bit numbers. <bookmark mark='b'/> The "
            "unit of sale became the rack. A GB200 NVL72 puts seventy-two of them on one NVLink fabric, liquid "
            "cooled, so that the rack behaves like one enormous GPU, and the 2025 Blackwell Ultra raised the memory "
            "to 288 gigabytes per GPU."
        ) as vo:
            self.play(FadeIn(dies), FadeIn(hbm), FadeIn(tag), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in link], lag_ratio=0.1), FadeIn(dl), FadeIn(ll))
            self.play(LaggedStart(*[FadeIn(f_) for f_ in facts[:3]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(facts[3]))
            self.play(FadeIn(facts[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rubin(self):
        R, rack = GPUS["Rubin"], NVL72_RUBIN
        # the rack: compute trays of GPUs and CPUs, switch trays in the middle
        trays = VGroup()
        for k in range(18):
            tray = VGroup(*[Square(0.2, stroke_width=0.5, stroke_color=GPUC, fill_color=GPUC, fill_opacity=0.7)
                            for _ in range(4)],
                          *[Square(0.2, stroke_width=0.5, stroke_color=CPUC, fill_color=CPUC, fill_opacity=0.6)
                            for _ in range(2)]).arrange(RIGHT, buff=0.08)
            trays.add(tray)
        sw = VGroup(*[Rectangle(width=1.65, height=0.16, stroke_width=0, fill_color=COMMC, fill_opacity=0.7)
                      for _ in range(9)]).arrange(DOWN, buff=0.06)
        col = VGroup(*trays[:9], sw, *trays[9:]).arrange(DOWN, buff=0.06)
        frame = SurroundingRectangle(col, buff=0.15, color=GREY_C, stroke_width=2)
        rk = VGroup(frame, col).move_to([-4.6, -0.2, 0])
        keys = VGroup(label(r"GPUs", font_size=18, color=GPUC), label(r"CPUs", font_size=18, color=CPUC),
                      label(r"NVLink switches", font_size=18, color=COMMC)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.1)
        keys.next_to(frame, RIGHT, buff=0.2).align_to(frame, DOWN)
        facts = VGroup(
            label(r"Vera Rubin NVL72 \ (in production, 2026)", font_size=28, color=GPUC),
            label(rf"per GPU: \ ${R['mem'] / 1e9:.0f}$ GB of HBM4 at ${R['bw'] / 1e12:.1f}$ TB/s", font_size=22,
                  color=BYTEC),
            label(rf"per GPU: \ NVFP4 ${R['fp4'] / 1e15:.0f}$ PFLOP/s, \ FP8 ${R['fp8'] / 1e15:.1f}$, \ BF16 "
                  rf"${R['tensor'] / 1e15:.0f}$ \ (dense)", font_size=22, color=FLOPC),
            label(rf"NVLink 6: \ ${R['link'] / 1e12:.0f}$ TB/s per GPU, \ ${rack['nvlink'] / 1e12:.0f}$ TB/s per rack",
                  font_size=22, color=COMMC),
            label(rf"a $100$-MW \textit{{AI factory}}: \ ${rack['factory_gpus']:,}$ GPUs".replace(",", "{,}"),
                  font_size=22, color=POWERC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.0, 0.6, 0])
        for f_ in facts:
            if f_.width > 7.4:
                f_.width = 7.4
        ridge = R["fp4"] / R["bw"]
        rl = label(rf"its ridge, in NVFP4: \ $\approx {ridge:,.0f}$ FLOPs per byte".replace(",", "{,}"), font_size=22,
                   color=GREY_A).next_to(facts, DOWN, buff=0.45).align_to(facts, LEFT)
        cite_ = cite(r"NVIDIA Vera Rubin NVL72 page (accessed October 2026)", corner=DR)
        tag = schematic_tag(corner=UL)
        with self.voiceover(
            "Its successor is in production now. <bookmark mark='a'/> A Vera Rubin NVL72 rack holds seventy-two "
            "Rubin GPUs and thirty-six of NVIDIA's own Arm CPUs. <bookmark mark='b'/> Each GPU has 288 gigabytes of "
            f"the fourth generation of high-bandwidth memory, read at {R['bw'] / 1e12:.1f} terabytes a second, and "
            f"does {R['fp4'] / 1e15:.0f} quadrillion four-bit operations a second for training. The sixth NVLink "
            f"moves {R['link'] / 1e12:.0f} terabytes a second per GPU, {rack['nvlink'] / 1e12:.0f} across the rack. "
            "<bookmark mark='c'/> NVIDIA now sells these by the hundred megawatts: forty thousand GPUs in one "
            f"building. <bookmark mark='d'/> And note the ridge: about {ridge:,.0f} operations per byte in four-bit "
            "arithmetic. Only work with enormous reuse can use all of it."
        ) as vo:
            self.play(FadeIn(rk), FadeIn(keys), FadeIn(tag), FadeIn(cite_), FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(t_, scale_factor=1.05) for t_ in trays], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f_) for f_ in facts[1:4]], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(facts[4]))
            vo.wait_until("d")
            self.play(FadeIn(rl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def domains(self):
        items = [(r"HGX H100 server \ (2022)", 8, GPUC), (r"GB200 NVL72 \ (2024)", 72, GPUC),
                 (r"TPU v4 pod \ (2021)", 4096, FLOPC), (r"Ironwood pod \ (2025)", IRONWOOD["pod"], FLOPC),
                 (r"TPU 8t superpod \ (2026)", TPU8T["pod"], FLOPC)]
        mx = math.log10(max(v for _, v, _ in items))
        bars, labs = VGroup(), VGroup()
        for k, (t, v, c_) in enumerate(items):
            w = 0.3 + 6.6 * math.log10(v) / mx
            y = 1.6 - 0.8 * k
            bars.add(Rectangle(width=w, height=0.5, stroke_width=0, fill_color=c_, fill_opacity=0.85)
                     .move_to([-1.9 + w / 2, y, 0]))
            labs.add(VGroup(label(t, font_size=22, color=c_).next_to([-2.1, y, 0], LEFT, buff=0.1),
                            label(rf"${v:,}$".replace(",", "{,}"), font_size=22).next_to(bars[-1], RIGHT, buff=0.15)))
        head = label(r"chips in one tightly linked domain \ (log scale)", font_size=26).to_edge(UP, buff=0.4)
        note_ = label(rf"Google: \ near-linear scaling claimed to a million TPU 8t chips in one logical cluster",
                      font_size=20, color=GREY_A).move_to([0, -2.85, 0])
        cite_ = cite(r"NVIDIA; \ Google (2021, 2025, 2026)", corner=DR)
        with self.voiceover(
            "The unit of computing keeps growing. <bookmark mark='a'/> In 2022 the GPUs that shared a fast fabric "
            "were the eight in one server. <bookmark mark='b'/> With Blackwell, seventy-two in a rack. "
            "<bookmark mark='c'/> Google's torus pods were larger still: 4,096 TPU v4 chips, 9,216 Ironwood chips "
            f"in 2025, and {TPU8T['pod']:,} in a TPU 8t superpod announced this year. <bookmark mark='d'/> Google "
            "says its new data-centre network can make a million of them work as one cluster. Part 18 is about "
            "what it takes to use machines like these for a single training run."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], LEFT))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], LEFT), FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[k], LEFT), FadeIn(labs[k])) for k in (2, 3, 4)],
                                  lag_ratio=0.5), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def split(self):
        left = VGroup(box_label(r"prefill: \ read the whole prompt", FLOPC, font_size=24),
                      label(r"a matrix times a matrix: \ high intensity, \ on the roof", font_size=20, color=GREY_A))
        right = VGroup(box_label(r"decode: \ one token at a time", BYTEC, font_size=24),
                       label(r"a matrix times a vector: \ $\approx 1$ FLOP/byte, \ on the slope", font_size=20,
                             color=GREY_A))
        for g_ in (left, right):
            g_.arrange(DOWN, buff=0.2)
        VGroup(left, right).arrange(RIGHT, buff=1.4).move_to([0, 2.3, 0])
        chips = VGroup(
            label(r"Rubin GPUs \ (and Rubin CPX, for long prompts)", font_size=22, color=GPUC).next_to(left, DOWN,
                                                                                                    buff=0.5),
            label(rf"Groq 3 LPX: \ ${GROQ3_LPX['sram_bw'] / 1e15:.0f}$ PB/s of SRAM per rack", font_size=22,
                  color=L1C).next_to(right, DOWN, buff=0.5),
        )
        tpu = label(rf"Google: \ TPU 8t for training; \ TPU 8i for serving, \ ${TPU8I['sram'] / 1e6:.0f}$ MB of SRAM "
                    r"for the KV cache", font_size=22, color=FLOPC).move_to([0, -2.45, 0])
        # a schematic roofline: prefill on the roof, decode on the slope
        o = np.array([-2.0, -1.75, 0])
        rax = VGroup(Line(o, o + RIGHT * 4.2, stroke_width=2, color=GREY_B),
                     Line(o, o + UP * 2.3, stroke_width=2, color=GREY_B))
        ridge = o + np.array([2.0, 1.9, 0])
        roof = VMobject(color=WHITE, stroke_width=3).set_points_as_corners(
            [o + np.array([0.1, 0.15, 0]), ridge, o + np.array([4.1, 1.9, 0])])
        rxl = label(r"FLOP per byte", font_size=18, color=GREY_B).next_to(rax[0], DOWN, buff=0.1)
        ryl = label(r"FLOP/s", font_size=18, color=GREY_B).next_to(rax[1], LEFT, buff=0.1)
        pf = glow_dot(o + np.array([3.4, 1.9, 0]), color=FLOPC)
        dc = glow_dot(o + np.array([0.5, 0.15 + 0.4 * 1.75 / 1.9, 0]), color=BYTEC)
        pfl = label(r"prefill", font_size=20, color=FLOPC).next_to(pf, UP, buff=0.15)
        dcl = label(r"decode", font_size=20, color=BYTEC).next_to(dc, RIGHT, buff=0.2)
        mini = VGroup(rax, roof, rxl, ryl)
        stag = schematic_tag(corner=UR)
        limits = label(r"what limits now: \ power, \ memory bandwidth, \ and the links between chips", font_size=26,
                       color=WHITE).move_to([-0.5, -3.15, 0])
        cite_ = cite(r"NVIDIA (2026); \ Google (April 2026)", corner=DR)
        with self.voiceover(
            "The newest trend is to split the work by where it sits on the roofline. <bookmark mark='a'/> Reading "
            "a prompt multiplies matrices by matrices: high intensity, arithmetic-bound. Writing the answer, one "
            "token at a time, multiplies matrices by vectors: low intensity, memory-bound. <bookmark mark='b'/> So "
            "NVIDIA pairs Rubin GPUs, and a variant for very long prompts, with Groq's SRAM chips for decoding; "
            "<bookmark mark='c'/> and Google's eighth generation is two chips, one for training and one for "
            "serving, with three times its predecessor's on-chip memory for the attention cache. "
            "<bookmark mark='d'/> The limits now are power, memory bandwidth and the links between chips, the three "
            "threads of this part."
        ) as vo:
            self.play(FadeIn(left), FadeIn(right), FadeIn(cite_), FadeIn(mini), FadeIn(stag))
            vo.wait_until("a")
            self.play(Indicate(left[0], color=FLOPC), FadeIn(pf), FadeIn(pfl))
            self.play(Indicate(right[0], color=BYTEC), FadeIn(dc), FadeIn(dcl))
            vo.wait_until("b")
            self.play(FadeIn(chips))
            vo.wait_until("c")
            self.play(FadeIn(tpu))
            vo.wait_until("d")
            self.play(FadeIn(limits, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
