from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (CNN, FMAP, HIST, KERNEL, PART, box_label, img_rgb, load)
from videos.ai.ai10.specs import CONVNEXT_STEPS, CONVNEXT_XL_22K, MOBILENET, SWIN_T

DW, PW = C.INTERVAL, C.CONTEXT


class Efficient(VoiceoverScene):
    def construct(self):
        self.card()
        self.separable()
        self.measured()
        self.mobilenet()
        self.dilated()
        self.convnext()

    def card(self):
        card = chapter_card(10, r"Cheaper convolutions", r"Does every filter need to look at every channel?",
                            lit=(2015,), part=PART)
        with self.voiceover("Chapter ten. Cheaper convolutions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def block(self, w, h, d, color, center, op=0.25):
        f = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.6, fill_color=color, fill_opacity=op)
        t = Polygon(f.get_corner(UL), f.get_corner(UL) + np.array([d * 0.6, d * 0.4, 0]),
                    f.get_corner(UR) + np.array([d * 0.6, d * 0.4, 0]), f.get_corner(UR), stroke_color=color,
                    stroke_width=1.2, fill_color=color, fill_opacity=op * 0.6)
        s = Polygon(f.get_corner(UR), f.get_corner(UR) + np.array([d * 0.6, d * 0.4, 0]),
                    f.get_corner(DR) + np.array([d * 0.6, d * 0.4, 0]), f.get_corner(DR), stroke_color=color,
                    stroke_width=1.2, fill_color=color, fill_opacity=op * 0.4)
        return VGroup(f, t, s).move_to(center)

    def separable(self):
        std = self.block(0.9, 0.9, 1.6, KERNEL, [-4.5, 1.6, 0])
        sl = label(r"standard: \ $k \times k \times C$, \ for each of $C'$ outputs", font_size=20, color=KERNEL)
        sl.next_to(std, DOWN, buff=0.2)
        dws = VGroup(*[self.block(0.9, 0.9, 0.12, DW, [0, 0, 0]) for _ in range(5)]).arrange(RIGHT, buff=0.12)
        dws.move_to([-0.2, 1.6, 0])
        dl = label(r"depthwise: \ one $k \times k$ per channel", font_size=20, color=DW).next_to(dws, DOWN, buff=0.2)
        pw = self.block(0.18, 0.18, 1.6, PW, [4.2, 1.6, 0], op=0.5)
        pl = label(r"pointwise: \ $1 \times 1 \times C$, \ for each output", font_size=20, color=PW)
        pl.next_to(pw, DOWN, buff=0.35)
        colors = {r"k^2": KERNEL, r"C'": PW, r"\frac{1}{C'}": PW, r"\frac{1}{k^2}": DW}
        rows = [
            cmath(r"\text{standard}", r"=", r"H W\, C\, C'\, k^2", font_size=36),
            cmath(r"\text{separable}", r"=", r"H W\, C\, k^2", r"+", r"H W\, C\, C'", font_size=36),
            cmath(r"\text{ratio}", r"=", r"\frac{1}{C'}", r"+", r"\frac{1}{k^2}", colors=colors, font_size=40),
        ]
        rows[1][2].set_color(DW)
        rows[1][4].set_color(PW)
        whys = [why(r"multiply-adds: \ every output, every input channel, every tap"),
                why(r"filter each channel alone, \ then mix channels"),
                why(r"$k = 3$, $C' = 256$: \ about $8.7\times$ cheaper")]
        step = ladder(self, rows, whys, keep=3, top=-0.2, x=-3.0, align_index=1, edge=6.8)
        cite_ = cite(r"Sifre (2014); \ Chollet (2016); \ Howard et al.\ (2017)", corner=DR)
        with self.voiceover(
            "A convolution kernel looks at a small patch, but through every channel of the layer below: k by k "
            "by C weights, for each of the C prime output channels. <bookmark mark='a'/> In 2014 Laurent Sifre "
            "split it in two. First filter each channel on its own, with one small kernel per channel: depthwise. "
            "<bookmark mark='b'/> Then mix the channels at each pixel with a one-by-one convolution: pointwise. "
            "<bookmark mark='c'/> Count the multiply-adds. Standard: height times width times C times C prime "
            "times k squared. <bookmark mark='d'/> Separable: the depthwise part, H W C k squared, plus the "
            "pointwise part, H W C C prime. <bookmark mark='e'/> Their ratio is one over C prime plus one over k "
            "squared: for three-by-three kernels and 256 channels, about a ninth of the arithmetic."
        ) as vo:
            self.play(FadeIn(std), FadeIn(sl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in dws], lag_ratio=0.15), FadeIn(dl))
            vo.wait_until("b")
            self.play(FadeIn(pw), FadeIn(pl))
            vo.wait_until("c")
            step(0)
            vo.wait_until("d")
            step(1, transform=False)
            vo.wait_until("e")
            step(2, transform=False)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        d = load("depthwise")
        rows = d["rows"]
        Cs = [r["C"] for r in rows]
        bars = VGroup()
        for k, r in enumerate(rows):
            x = -5.2 + 1.75 * k
            hf = 4.0 * r["flop_ratio"]
            ht = 4.0 * min(r["time_ratio"], 1.0)
            bf = Rectangle(width=0.55, height=max(hf, 0.03), stroke_width=0, fill_color=KERNEL, fill_opacity=0.85)
            bt = Rectangle(width=0.55, height=max(ht, 0.03), stroke_width=0, fill_color=DW, fill_opacity=0.85)
            bf.move_to([x, -2.4 + hf / 2, 0])
            bt.move_to([x + 0.6, -2.4 + ht / 2, 0])
            vf = MathTex(f"{r['flop_ratio']:.2f}", font_size=20, color=KERNEL).next_to(bf, UP, buff=0.06)
            vt = MathTex(f"{r['time_ratio']:.2f}", font_size=20, color=DW).next_to(bt, UP, buff=0.06)
            cl = MathTex(rf"C = {r['C']}", font_size=22, color=GREY_B).move_to([x + 0.3, -2.75, 0])
            bars.add(VGroup(bf, bt, vf, vt, cl))
        base = Line([-5.7, -2.4, 0], [3.8, -2.4, 0], color=GREY_C, stroke_width=1.5)
        one = DashedLine([-5.7, 1.6, 0], [3.8, 1.6, 0], color=GREY_D, stroke_width=1.5)
        ol = MathTex(r"1 = \text{standard}", font_size=22, color=GREY_B).next_to(one, RIGHT, buff=0.1)
        leg = legend([(KERNEL, r"arithmetic, \ separable / standard"), (DW, r"measured time, \ separable / standard")],
                     font_size=22).to_corner(UL, buff=0.4)
        r128 = next(r for r in rows if r["C"] == 128)
        sp = VGroup(label(r"speed, \ billions of operations per second:", font_size=20, color=GREY_A),
                    MathTex(rf"\text{{standard }}{r128['gflops_std']:.0f},\ \ \text{{depthwise }}"
                            rf"{r128['gflops_dw']:.1f},\ \ \text{{pointwise }}{r128['gflops_pw']:.0f}",
                            font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        sp.to_corner(UR, buff=0.4).shift(DOWN * 0.1)
        if sp.width > 5.8:
            sp.width = 5.8
        tag = note(rf"computed: \ this computer, \ ${d['threads']}$ threads, \ $3 \times 3$ kernels on "
                   rf"${d['hw']} \times {d['hw']}$ maps, \ batch ${d['batch']}$").to_corner(DR, buff=0.2)
        ft = r128["flop_ratio"]
        tt = r128["time_ratio"]
        verdict = (f"The arithmetic falls to {ft:.2f} of the standard layer's, but the time only to {tt:.2f}. "
                   f"The depthwise step runs at {r128['gflops_dw']:.1f} billion operations a second, against "
                   f"{r128['gflops_std']:.0f} for the standard convolution: each of its weights touches one channel, "
                   "so it does little arithmetic per byte it reads, and Part 17's roofline caps it." if tt > 1.5 * ft
                   else
                   f"The arithmetic falls to {ft:.2f} of the standard layer's, and the time to {tt:.2f}: here the "
                   "saving is nearly all realized.")
        with self.voiceover(
            "Fewer operations should mean faster. We measured both versions on the computer making this video. "
            "<bookmark mark='a'/> For 128 channels: " + verdict + " <bookmark mark='b'/> Counting operations is "
            "not the same as counting time, and efficient networks are designed for the hardware they run on."
        ) as vo:
            self.play(FadeIn(leg), Create(base), Create(one), FadeIn(ol), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(sp, shift=UP * 0.1))
            self.play(Indicate(bars[Cs.index(128)], color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mobilenet(self):
        rows = VGroup()
        for k, (nm, acc, macs, params) in enumerate(MOBILENET):
            c = CNN if k == 0 else GREY_B
            rows.add(VGroup(label(nm, font_size=24, color=c), MathTex(rf"{acc}\%", font_size=30, color=c),
                            MathTex(rf"{macs:,}".replace(",", "{,}"), font_size=30, color=c),
                            MathTex(rf"{params:g}", font_size=30, color=c)))
        head = VGroup(VectorizedPoint(), label(r"ImageNet top-1", font_size=22, color=GREY_A),
                      label(r"million mult-adds", font_size=22, color=GREY_A),
                      label(r"million weights", font_size=22, color=GREY_A))
        tab = VGroup(head, *rows)
        colx = [-5.4, 0.2, 2.8, 5.2]
        for ri, r in enumerate(tab):
            y = 1.4 - 0.75 * ri
            r[0].move_to([colx[0] + r[0].width / 2, y, 0])
            for j in (1, 2, 3):
                r[j].move_to([colx[j], y, 0])
        hc = history_card(2017, r"Andrew Howard and colleagues, \ Google: \ MobileNets",
                          r"depthwise separable convolutions all the way down, \ for phones", width=6.0,
                          color=HIST).to_edge(UP, buff=0.3)
        cite_ = cite(r"Howard et al.\ (2017), \ Table 8", corner=DR)
        m, g, v = MOBILENET
        with self.voiceover(
            "In 2017 Andrew Howard's team at Google built a whole network of separable convolutions, for phones: "
            f"MobileNet. <bookmark mark='a'/> It came within {v[1] - m[1]:.1f} points of VGG-16's accuracy on "
            f"ImageNet with {v[2] / m[2]:.0f} times fewer multiply-adds and {v[3] / m[3]:.0f} times fewer "
            "weights, and beat GoogLeNet with fewer of both."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dilated(self):
        r = load("receptive")["dilated"]
        L = 4
        n = 2 ** (L + 1) - 1  # the receptive field of the top unit
        xs = np.linspace(-6.0, 6.0, n)
        ys = [-2.4 + 1.25 * l for l in range(L + 1)]
        nodes = VGroup(*[VGroup(*[Dot([x, y, 0], radius=0.07, color=GREY_C) for x in xs]) for y in ys])
        top = n // 2
        lines = VGroup()
        lit = {L: {top}}
        for l in range(L, 0, -1):
            d = 2 ** (l - 1)
            lit[l - 1] = set()
            for i in lit[l]:
                for o in (-d, 0, d):
                    j = i + o
                    if 0 <= j < n:
                        lit[l - 1].add(j)
                        lines.add(Line(nodes[l][i].get_center(), nodes[l - 1][j].get_center(), color=KERNEL,
                                       stroke_width=2, stroke_opacity=0.8))
        for l in range(L + 1):
            for i in lit[l]:
                nodes[l][i].set_color(KERNEL).scale(1.3)
        dl = VGroup(*[label(rf"dilation ${2 ** (l - 1)}$", font_size=18, color=GREY_B).next_to(nodes[l], LEFT,
                                                                                            buff=0.15)
                      for l in range(1, L + 1)])
        for t in dl:
            if t.get_left()[0] < -6.9:
                t.shift(RIGHT * (-6.9 - t.get_left()[0]))
        head = label(rf"$3$-tap kernels with gaps: \ ${L}$ layers see ${r['dilated'][L - 1]}$ inputs, \ "
                     rf"against ${r['plain'][L - 1]}$ without gaps", font_size=26).to_edge(UP, buff=0.35)
        cite_ = cite(r"Holschneider et al.\ (1989); \ Yu \& Koltun (2015); \ van den Oord et al.\ (2016)",
                     corner=DR)
        with self.voiceover(
            "The other trick spreads a kernel out instead of slimming it. <bookmark mark='a'/> A dilated "
            "convolution leaves gaps between its taps: one apart in the first layer, two in the next, then four, "
            "then eight. <bookmark mark='b'/> The receptive field doubles with every layer: after ten layers "
            f"of three taps, {r['dilated'][9]:,} inputs instead of {r['plain'][9]}, at no extra cost. "
            "<bookmark mark='c'/> The idea is old, the algorithme a trous of 1989; DeepMind's WaveNet used it in "
            "2016 to generate speech."
        ) as vo:
            self.play(FadeIn(nodes), FadeIn(head), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(lines), FadeIn(dl), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def convnext(self):
        vals = [a for _, a in CONVNEXT_STEPS]
        lo, hi = 75.0, 82.5
        bars = VGroup()
        for k, (nm, a) in enumerate(CONVNEXT_STEPS):
            w = 6.0 * (a - lo) / (hi - lo)
            b = Rectangle(width=w, height=0.36, stroke_width=0, fill_color=CNN if k == len(vals) - 1 else FMAP,
                          fill_opacity=0.85)
            y = 2.3 - 0.52 * k
            b.move_to([-0.8 + w / 2, y, 0])
            t = label(nm, font_size=18, color=GREY_A).next_to([-0.8, y, 0], LEFT, buff=0.15)
            v = MathTex(f"{a}", font_size=22, color=WHITE).next_to(b, RIGHT, buff=0.1)
            bars.add(VGroup(b, t, v))
        sx = -0.8 + 6.0 * (SWIN_T - lo) / (hi - lo)
        swin = DashedLine([sx, 2.6, 0], [sx, 2.3 - 0.52 * (len(vals) - 1) - 0.3, 0], color=ATTN_C, stroke_width=2.5)
        swl = label(rf"Swin-T, \ a vision transformer: \ ${SWIN_T}\%$", font_size=20, color=ATTN_C)
        swl.next_to(swin, DOWN, buff=0.1)
        head = label(r"ResNet-50 modernized, \ one step at a time \ (ImageNet top-1, \%)", font_size=26)
        head.to_edge(UP, buff=0.25)
        foot = VGroup(
            label(rf"ConvNeXt-XL, \ pre-trained on ImageNet-22K: \ ${CONVNEXT_XL_22K}\%$", font_size=22, color=CNN),
            label(r"2023: \ convolutional networks trained on $4$ billion images match vision transformers", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        cite_ = cite(r"Dosovitskiy et al.\ (2020); \ Liu et al.\ (2022); \ Smith et al.\ (2023)", corner=DR)
        foot.next_to(cite_, UP, buff=0.15).to_edge(LEFT, buff=0.5)
        vit = history_card(2020, r"Alexey Dosovitskiy and colleagues, \ Google",
                           r"the vision transformer: \ an image cut into patches of $16 \times 16$ pixels, \ fed to a "
                           r"transformer; \ with enough data, \ as good as the best convolutional networks; \ Part 22",
                           width=7.0, color=HIST).move_to(UP * 1.9)
        # schematic: a photograph cut into patches, each a token for a transformer
        photo = np.asarray(load("data")["cifar_grid"])[7, 0]
        P = 4
        tiles = Group(*[img_rgb(photo[r * 8:(r + 1) * 8, c * 8:(c + 1) * 8], 0.5) for r in range(P) for c in range(P)])
        whole = Group(*[t.copy() for t in tiles]).arrange_in_grid(rows=P, cols=P, buff=0.0).move_to([-4.6, -1.4, 0])
        seq = Group(*[t.copy() for t in tiles]).arrange(RIGHT, buff=0.06).scale(0.7).move_to([0.6, -1.4, 0])
        tbox = box_label(r"transformer", ATTN_C, font_size=24).move_to([5.3, -1.4, 0])
        a1 = Arrow(whole.get_right(), seq.get_left(), buff=0.15, stroke_width=2.5, color=GREY_B)
        a2 = Arrow(seq.get_right(), tbox.get_left(), buff=0.15, stroke_width=2.5, color=GREY_B)
        sch = note(r"schematic: \ $16$ patches of one CIFAR-10 photograph").next_to(seq, DOWN, buff=0.4)
        vitfig = Group(whole, a1, seq, a2, tbox, sch)
        with self.voiceover(
            "In 2020 a transformer fed an image cut into patches matched the best convolutional networks, and "
            "vision transformers soon led the benchmarks: Part 22. <bookmark mark='a'/> In 2022 Zhuang Liu and "
            "colleagues at Meta asked how much of the lead was architecture and how much recipe. They took a "
            "ResNet-50 at 76.1 percent: the transformers' training recipe alone gave 78.8; depthwise convolutions, "
            "wider layers, seven-by-seven kernels and the transformer's layer norm took it to "
            f"{vals[-1]}, <bookmark mark='b'/> above the transformer of the same size, at {SWIN_T}, with no "
            "attention at all: ConvNeXt. <bookmark mark='c'/> In 2023 DeepMind matched vision transformers with "
            "convolutional networks trained on four billion images. At scale, recipe and compute matter more than "
            "architecture: Part 12's lesson."
        ) as vo:
            self.play(FadeIn(vit, shift=UP * 0.2), FadeIn(cite_))
            self.play(FadeIn(whole), GrowArrow(a1), LaggedStart(*[FadeIn(t) for t in seq], lag_ratio=0.08),
                      GrowArrow(a2), FadeIn(tbox), FadeIn(sch), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeOut(vit), FadeOut(vitfig), FadeIn(head))
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars], lag_ratio=0.25), run_time=4.0)
            vo.wait_until("b")
            self.play(Create(swin), FadeIn(swl))
            vo.wait_until("c")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()


ATTN_C = C.ATTN
_ = KERNEL
