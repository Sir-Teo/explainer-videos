from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (EXPC, F, LEVELC, MANC, PART, RTNC, SIGNC, WEIGHTC, bit_cells, hbars, load, times)

MXC, NVC, INTC = C.BITS, C.TRUE_P, C.PROB
E2M1 = [0, 0.5, 1, 1.5, 2, 3, 4, 6]


def code_cells(code: str, cell=0.2, font_size=13):
    return bit_cells(code, [SIGNC, EXPC, EXPC, MANC], cell=cell, font_size=font_size)


class Formats(VoiceoverScene):
    def construct(self):
        self.card()
        self.e2m1()
        self.mx()
        self.nv()
        self.results()
        self.gptoss()

    def card(self):
        card = chapter_card(12, r"Four-bit floats: \ MXFP4 and NVFP4", r"What does a weight look like in four bits?",
                            part=PART)
        with self.voiceover("Chapter twelve. Four-bit floats: MXFP4 and NVFP4."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def e2m1(self):
        nl = NumberLine(x_range=[0, 6, 1], length=8.4, include_numbers=False, color=GREY_C, tick_size=0.05)
        nl.move_to([0, 0.4, 0])
        band = [GREY_B, C.TRUE_P, C.INTERVAL, C.BITS]
        bands = [0, 0, 1, 1, 2, 2, 3, 3]
        dots = VGroup(*[Dot(nl.n2p(v), radius=0.09, color=band[b]) for v, b in zip(E2M1, bands)])
        nums = VGroup(*[MathTex(t, font_size=26, color=band[b]).next_to(nl.n2p(v), DOWN, buff=0.15)
                        for t, v, b in zip(("0", r"\tfrac12", "1", r"\tfrac32", "2", "3", "4", "6"), E2M1, bands)])
        codes = VGroup(*[code_cells(format(i, "04b"), cell=0.22).next_to(nl.n2p(v), UP, buff=0.3)
                         for i, v in enumerate(E2M1)])
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c_, fill_opacity=0.6),
                              label(t, font_size=20, color=c_)).arrange(RIGHT, buff=0.12)
                       for c_, t in ((SIGNC, r"sign"), (EXPC, r"$2$ exponent bits"), (MANC, r"$1$ mantissa bit"))])
        key.arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.5)
        gaps = VGroup(*[label(t, font_size=20, color=band[b]).next_to(nl.n2p(m), DOWN, buff=0.75)
                        for t, m, b in ((r"gap $\tfrac12$", 1.0, 1), (r"gap $1$", 2.5, 2), (r"gap $2$", 5.0, 3))])
        tl = label(r"FP4, \ E2M1: \ Part 17's smallest float", font_size=26, color=LEVELC).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Part 17 met the smallest floating-point format in use, FP4, laid out as E2M1. <bookmark mark='a'/> "
            "One bit of sign, two of exponent, one of mantissa: sixteen codes, eight magnitudes. "
            "<bookmark mark='b'/> Zero and a half, then one and one and a half, two and three, four and six: within "
            "each power of two the gap is the same, and it doubles from one power to the next. "
            "<bookmark mark='c'/> On its own that covers zero to six. To store a model's weights, which are "
            "nothing like that size, each block of weights gets a scale, and the two formats of today's chips "
            "differ in exactly how."
        ) as vo:
            self.play(FadeIn(key), Create(nl), FadeIn(tl))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(c_), FadeIn(d_, scale=1.5), FadeIn(n_))
                                    for c_, d_, n_ in zip(codes, dots, nums)], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g_) for g_ in gaps], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(Indicate(tl, color=LEVELC))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def block_grid(self, values, codes, decoded, n, y, col, cols=16):
        """Values, their 4-bit codes and what they decode to, ``cols`` to a row."""
        g = VGroup()
        for i in range(n):
            r, c = divmod(i, cols)
            x = -6.0 + c * 0.76
            yy = y - r * 1.25
            v = MathTex(f"{values[i]:+.3f}", font_size=15, color=WEIGHTC).move_to([x, yy + 0.32, 0])
            cc = code_cells(codes[i], cell=0.16, font_size=11).move_to([x, yy, 0])
            d = MathTex(f"{decoded[i]:+.3f}", font_size=15, color=col).move_to([x, yy - 0.3, 0])
            g.add(VGroup(v, cc, d))
        return g

    def mx(self):
        f = load("formats")
        blk, codes, dec = np.asarray(f["block"]), list(f["mx_codes"]), np.asarray(f["mx_values"])
        e = int(f["mx_shared_exp"])
        amax = float(np.abs(blk).max())
        head = label(rf"MXFP4: \ one block of $32$ weights of our model \ (\texttt{{{f['layer']}}}, row "
                     rf"${int(f['row'])}$)", font_size=22, color=MXC).to_edge(UP, buff=0.3)
        grid = self.block_grid(blk, codes, dec, 32, 1.6, MXC)
        steps = VGroup(
            MathTex(rf"\max|w| = {amax:.4f}", font_size=26, color=WEIGHTC),
            MathTex(rf"\lfloor \log_2 {amax:.4f} \rfloor - 2 = {e}", font_size=26, color=MXC),
            VGroup(label(r"E8M0 scale:", font_size=20, color=MXC),
                   bit_cells(f["mx_scale_bits"], [EXPC] * 8, cell=0.24, font_size=14),
                   MathTex(rf"= 2^{{{e}}}", font_size=26, color=MXC)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.4, -2.3, 0])
        ratio = amax / 2.0 ** e
        clip = VGroup(label(rf"largest $\div$ scale $= {ratio:.2f}$: \ above $6$, \ so clamped to $6$" if ratio > 6 else
                            rf"largest $\div$ scale $= {ratio:.2f}$: \ below $6$, \ nothing clamped", font_size=20,
                            color=C.SURPRISE),
                      label(rf"blocks of our model with a value clamped: \ ${100 * f['clipped_share']:.0f}\%$",
                            font_size=20, color=C.SURPRISE)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        clip.move_to([3.3, -2.3, 0])
        hc = history_card(2023, r"Bita Darvish Rouhani et al., \ OCP", r"microscaling: \ blocks of $32$, \ a shared "
                          r"power-of-two scale", width=4.0, font_size=16, color=MXC).move_to([4.4, -2.5, 0])
        clamp_say = (f"This block's largest weight is {ratio:.2f} times the scale, above six, so it is clamped to six."
                     if ratio > 6 else
                     f"This block's largest weight is {ratio:.2f} times the scale, below six, so nothing is clamped.")
        with self.voiceover(
            "MXFP4 comes from the Open Compute Project's microscaling standard of September 2023, written by "
            "AMD, Arm, Intel, Meta, Microsoft, NVIDIA and Qualcomm together. <bookmark mark='a'/> Here are thirty-two real weights "
            "from our model, a block. <bookmark mark='b'/> The block shares one scale, and the scale must be a "
            "power of two, stored as an eight-bit exponent, E8M0. The rule: the exponent of the block's largest "
            f"weight, minus two, so that weight lands between four and eight: here two to the {e}. "
            "<bookmark mark='c'/> Divide each weight by the scale, round it to the nearest E2M1 value, and keep "
            "its four-bit code: the middle row. Decoded, the last row. <bookmark mark='d'/> But E2M1 stops at six. "
            + clamp_say + " " +
            f"Across our model, {100 * f['clipped_share']:.0f} percent of the blocks have their largest value cut "
            "down this way: the price of a scale that can only be a power of two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_[0]) for c_ in grid], lag_ratio=0.03), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeOut(hc), FadeIn(steps[0]))
            self.play(FadeIn(steps[1]), FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c_[1]) for c_ in grid], lag_ratio=0.03), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(c_[2]) for c_ in grid], lag_ratio=0.03), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(clip))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nv(self):
        f = load("formats")
        blk = np.asarray(f["block"])[:16]
        codes, dec = list(f["nv_codes"]), np.asarray(f["nv_values"])
        g_, s = float(f["nv_tensor_scale"]), float(f["nv_block_scale"])
        head = label(r"NVFP4: \ the same weights, \ blocks of $16$", font_size=22, color=NVC).to_edge(UP, buff=0.3)
        grid = self.block_grid(blk, codes, dec, 16, 1.7, NVC)
        amax_t = g_ * 6 * 448
        steps = VGroup(
            MathTex(rf"s_{{\text{{tensor}}}} = \frac{{\max_{{\text{{matrix}}}} |w|}}{{6 \times 448}} = {g_:.3e}"
                    .replace("e-0", r"\times 10^{-").replace("e-", r"\times 10^{-") + "}", font_size=26, color=NVC),
            MathTex(rf"s_{{\text{{block}}}} = \mathrm{{E4M3}}\Big(\frac{{\max|w|}}{{6\, s_{{\text{{tensor}}}}}}\Big) = "
                    rf"{s:g}", font_size=26, color=NVC),
            VGroup(label(r"E4M3 scale:", font_size=20, color=NVC),
                   bit_cells(f["nv_scale_bits"], [SIGNC] + [EXPC] * 4 + [MANC] * 3, cell=0.24, font_size=14))
            .arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-2.6, -1.2, 0])
        cmp_ = VGroup(label(r"MXFP4: \ $4 + 8/32 = 4.25$ bits a weight", font_size=22, color=MXC),
                      label(r"NVFP4: \ $4 + 8/16 = 4.5$ bits, \ plus one number per matrix", font_size=22, color=NVC))
        cmp_.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.5)
        hc = history_card(2025, r"NVIDIA, \ Blackwell", rf"NVFP4: \ blocks of ${F.NVFP4['block']}$, \ an FP8 scale; \ "
                          rf"DeepSeek-R1 within ${F.NVFP4['r1_drop']}\%$ of FP8", width=4.0, font_size=16,
                          color=NVC).move_to([4.5, -1.2, 0])
        with self.voiceover(
            "NVIDIA's NVFP4, on its Blackwell chips, changes two things. <bookmark mark='a'/> Blocks of sixteen, "
            "so one large weight spoils fewer neighbours. <bookmark mark='b'/> And the block's scale is itself a "
            "small float, eight-bit E4M3, with three bits of mantissa: it can put the block's largest weight at "
            "six almost exactly, so nothing is clamped. <bookmark mark='c'/> E4M3 only spans a limited range, so "
            "one 32-bit scale for the whole matrix moves every block scale into it. <bookmark mark='d'/> The cost: "
            "four and a half bits a weight, against MXFP4's four and a quarter."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c_[0]) for c_ in grid], lag_ratio=0.04), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(steps[2]))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(c_[1]), FadeIn(c_[2])) for c_ in grid], lag_ratio=0.04),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(steps[0]))
            vo.wait_until("d")
            self.play(FadeIn(cmp_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        f = load("formats")
        base = float(f["fp32"])
        L, bpw = f["loss"], f["bpw"]
        rows = [("int4_row", r"$4$-bit integers, \ a scale per row", RTNC),
                ("mxfp4", r"MXFP4", MXC), ("nvfp4", r"NVFP4", NVC),
                ("int4_g16e4m3", r"$4$-bit integers, \ NVFP4's scales", INTC),
                ("int4_g32", r"$4$-bit integers, \ a 16-bit scale per $32$", C.EMBED)]
        vals = [L[k] - base for k, _, _ in rows]
        b = hbars(vals, [rf"{nm} \ (${bpw[k]:.2f}$)" for k, nm, _ in rows], [c_ for _, _, c_ in rows], width=4.2,
                  row_h=0.55, font_size=20, lo=0, hi=max(vals) * 1.1, fmt_v=lambda v: rf"{v:+.4f}")
        b.move_to([1.4, 0.0, 0])
        head = label(r"extra loss on held-out novels \ (nats per token), \ bits per weight in brackets", font_size=22,
                     color=GREY_A).to_edge(UP, buff=0.4)
        mx, nv, i16 = L["mxfp4"] - base, L["nvfp4"] - base, L["int4_g16e4m3"] - base
        rel = f["rel"]
        if nv < mx:
            a = f"NVFP4's finer, float-valued scales beat MXFP4: {nv:.4f} nats against {mx:.4f}."
        else:
            a = f"MXFP4 matches NVFP4 here: {mx:.4f} nats against {nv:.4f}."
        if i16 < nv * 0.95:
            b_say = ("But give plain four-bit integers NVFP4's very scales, and they do better still, "
                     f"{i16:.4f}: our weights are spread evenly within a block, and sixteen even levels fit them "
                     "better than E2M1's uneven ones. Floats earn their place on wider-ranging numbers, "
                     "activations above all, and because the chips multiply them directly.")
        else:
            b_say = f"Four-bit integers with the same scales come out at {i16:.4f}: no better than the floats."
        with self.voiceover(
            "Which is better on our model? <bookmark mark='a'/> Every block weight stored each way, scales "
            "included, and the loss measured on held-out novels. <bookmark mark='b'/> " + a +
            " <bookmark mark='c'/> " + b_say
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_.name), GrowFromEdge(r_.bar, LEFT), FadeIn(r_.val))
                                    for r_ in b[:3]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(b[2], color=NVC, scale_factor=1.03))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_.name), GrowFromEdge(r_.bar, LEFT), FadeIn(r_.val))
                                    for r_ in b[3:]], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gptoss(self):
        f = load("formats")
        o = F.GPT_OSS_120B
        gib = f["oss_bytes"] / 2 ** 30
        full = f["oss_bf16"]
        parts = VGroup(
            label(rf"experts' weights: \ ${o['mlp'] / 1e9:.2f}$B \ in MXFP4, \ ${o['mxfp4_bits']}$ bits", font_size=22,
                  color=MXC),
            label(rf"attention, \ embedding, \ head: \ ${(o['attn'] + o['embed']) / 1e9:.2f}$B \ in $16$ bits",
                  font_size=22, color=GREY_A),
            label(rf"in all: \ ${gib:.1f}$ GiB \ (the model card: ${o['ckpt_gib']}$ GiB)", font_size=24, color=WHITE),
            label(rf"all in $16$ bits it would be ${full / 1e9:.0f}$ GB", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-1.6, 0.6, 0])
        gpu = RoundedRectangle(width=2.4, height=3.0, corner_radius=0.12, stroke_color=C.GPU, stroke_width=2.5)
        gpu.move_to([4.6, 0.6, 0])
        fill = Rectangle(width=2.2, height=2.8 * gib * 2 ** 30 / 80e9, stroke_width=0, fill_color=MXC, fill_opacity=0.6)
        fill.align_to(gpu, DOWN).shift(UP * 0.1)
        gl = label(r"one $80$ GB GPU", font_size=20, color=C.GPU).next_to(gpu, UP, buff=0.15)
        head = label(rf"gpt-oss-120b \ (OpenAI, \ August 2025): \ ${o['total'] / 1e9:.1f}$B parameters, \ "
                     rf"${o['active'] / 1e9:.2f}$B per token", font_size=24, color=MXC).to_edge(UP, buff=0.4)
        k3 = F.KIMIK3
        more = label(rf"2026: \ Kimi K3 (${k3['total'] / 1e12:.1f}$T parameters) \ learns MXFP4 weights in training "
                     r"(Part 18)", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "This is how a frontier-size open model fits on one chip. <bookmark mark='a'/> In August 2025 OpenAI "
            "released gpt-oss-120b: 117 billion parameters, five of them used per token, because most live in "
            "experts. <bookmark mark='b'/> The experts' weights are stored in MXFP4, and the rest in sixteen bits. "
            f"Adding it up gives {gib:.1f} gibibytes, which matches the model card's {o['ckpt_gib']}. "
            f"<bookmark mark='c'/> In sixteen bits it would be {full / 1e9:.0f} gigabytes; in four, it fits on a "
            "single eighty-gigabyte GPU. <bookmark mark='d'/> And four bits are moving into training itself: in "
            "2026 Kimi K3 learned its weights in MXFP4 from the start, as Part 18 described."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(gpu), FadeIn(gl))
            vo.wait_until("b")
            self.play(FadeIn(parts[:3]))
            vo.wait_until("c")
            self.play(FadeIn(parts[3]), GrowFromEdge(fill, DOWN))
            vo.wait_until("d")
            self.play(FadeIn(more))
        self.wait(0.3)
        self.clear_scene()
