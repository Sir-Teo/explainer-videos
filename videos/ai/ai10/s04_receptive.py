from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (CNN, FMAP, KERNEL, PART, img_heat, load)

SHIFTC = C.INTERVAL


class Receptive(VoiceoverScene):
    def construct(self):
        self.card()
        self.cone()
        self.recursion()
        self.table()
        self.pooling()
        self.effective()

    def card(self):
        card = chapter_card(3, r"Receptive fields, stride and pooling",
                            r"How much of the image does a unit deep in the network see?", lit=(2012,), part=PART)
        with self.voiceover("Chapter three. Receptive fields, stride and pooling."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def layer_pts(self, l, n, c=0.22, x0=-4.6, y0=-3.0, dy=1.55):
        """Screen positions of grid cell (i, j) of layer l, drawn obliquely (a cheap 3D view)."""
        def P(i, j):
            return np.array([x0 + j * c + i * c * 0.55, y0 + l * dy + i * c * 0.32, 0])
        return P

    def cone(self):
        n, layers = 15, 4
        c = 0.22
        planes, patches, spans = VGroup(), VGroup(), []
        center = 7
        r = 1
        for l in range(layers):
            P = self.layer_pts(l, n, c)
            quad = Polygon(P(-0.5, -0.5), P(-0.5, n - 0.5), P(n - 0.5, n - 0.5), P(n - 0.5, -0.5),
                           stroke_color=GREY_C, stroke_width=1.5, fill_color=FMAP if l else GREY_D,
                           fill_opacity=0.1 if l else 0.25)
            planes.add(quad)
            spans.append(r)
        # receptive field of the top unit at each layer below: 1 at the top, growing by 2 per 3x3 layer
        sizes = [2 * (layers - 1 - l) + 1 for l in range(layers)]
        for l, sz in enumerate(sizes):
            P = self.layer_pts(l, n, c)
            a, b = center - sz // 2 - 0.5, center + sz // 2 + 0.5
            patches.add(Polygon(P(a, a), P(a, b), P(b, b), P(b, a), stroke_color=KERNEL, stroke_width=2,
                                fill_color=KERNEL, fill_opacity=0.35))
        lines = VGroup()
        for l in range(layers - 1):
            up, dn = patches[l + 1], patches[l]
            for k in range(4):
                lines.add(Line(up.get_vertices()[k], dn.get_vertices()[k], color=KERNEL, stroke_width=1.2,
                               stroke_opacity=0.7))
        names = VGroup(*[label(t, font_size=20, color=GREY_B).next_to(planes[l], RIGHT, buff=0.3)
                         for l, t in enumerate([r"the input", r"layer 1", r"layer 2", r"layer 3"])])
        sz_l = VGroup(*[MathTex(rf"{s} \times {s}", font_size=26, color=KERNEL).next_to(names[l], RIGHT, buff=0.3)
                        for l, s in enumerate(sizes)])
        cap = label(r"$3 \times 3$ kernels, \ stride $1$", font_size=24, color=WHITE).to_corner(UR, buff=0.5)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "One unit of the first layer sees three pixels by three. <bookmark mark='a'/> A unit of the second "
            "layer sees three by three units of the first, and each of those sees its own three by three, so "
            "together they cover five by five pixels. <bookmark mark='b'/> A third layer, seven by seven. This "
            "is the unit's receptive field: the part of the image that can change it at all. Stacked, the fields "
            "make a cone, and deep units see a lot of the picture, built out of small looks."
        ) as vo:
            self.play(FadeIn(planes), FadeIn(names), FadeIn(cap), FadeIn(tag))
            self.play(FadeIn(patches[3]), FadeIn(patches[2]), FadeIn(sz_l[3]), FadeIn(sz_l[2]),
                      Create(lines[8:]))
            vo.wait_until("a")
            self.play(FadeIn(patches[1]), FadeIn(sz_l[1]), Create(lines[4:8]))
            vo.wait_until("b")
            self.play(FadeIn(patches[0]), FadeIn(sz_l[0]), Create(lines[:4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recursion(self):
        colors = {r"r_\ell": KERNEL, r"r_{\ell-1}": KERNEL, r"j_\ell": FMAP, r"j_{\ell-1}": FMAP, r"k_\ell": WHITE,
                  r"s_\ell": SHIFTC, r"r_L": KERNEL}
        defs = VGroup(
            label(r"$k_\ell$: \ kernel size of layer $\ell$", font_size=24, color=WHITE),
            label(r"$s_\ell$: \ its stride (how far the kernel jumps)", font_size=24, color=SHIFTC),
            label(r"$j_\ell$: \ pixels between neighbouring units of layer $\ell$", font_size=24, color=FMAP),
            label(r"$r_\ell$: \ receptive field of one unit of layer $\ell$", font_size=24, color=KERNEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UL, buff=0.45)
        rows = [
            cmath(r"r_\ell", r"=", r"r_{\ell-1}", r"+", r"(k_\ell - 1)", r"\,", r"j_{\ell-1}", colors=colors,
                  font_size=40),
            cmath(r"j_\ell", r"=", r"j_{\ell-1}", r"\,", r"s_\ell", colors=colors, font_size=40),
            cmath(r"r_L", r"=", r"1 + \sum_{\ell=1}^{L} (k_\ell - 1) \prod_{i < \ell} s_i", colors=colors,
                  font_size=40),
        ]
        whys = [why(r"each extra tap reaches one more unit below, $j_{\ell-1}$ pixels on"),
                why(r"a stride $s$ spreads the units $s$ times further apart"),
                why(r"unrolled, from $r_0 = 1$, $j_0 = 1$")]
        step = ladder(self, rows, whys, keep=3, top=0.9, x=-2.2, align_index=1, edge=6.8)
        ex = VGroup(label(r"two $3 \times 3$ layers: \ $1 + 2 + 2 = 5$", font_size=26, color=GREY_A),
                    label(r"AlexNet's first layer, $11 \times 11$ at stride $4$: \ the next $3 \times 3$ adds "
                          r"$2 \times 4 = 8$", font_size=26, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                   buff=0.2)
        ex.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "We can count the cone exactly. <bookmark mark='a'/> Name the kernel size, the stride, the spacing "
            "between neighbouring units in pixels, and the receptive field. <bookmark mark='b'/> A kernel of size "
            "k has k minus 1 taps beyond the first, each reaching one more unit of the layer below, and those "
            "units sit j pixels apart: so the field grows by k minus 1 times j. <bookmark mark='c'/> And a stride "
            "multiplies the spacing: after a stride of 2, neighbouring units are twice as far apart in the image. "
            "<bookmark mark='d'/> Unrolled from one pixel: one, plus each layer's extra taps times the product of "
            "all the strides before it. <bookmark mark='e'/> That is why strides matter so much: every layer after "
            "a stride counts for more."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 0.1) for d in defs], lag_ratio=0.3))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1, transform=False)
            vo.wait_until("d")
            step(2, transform=False)
            vo.wait_until("e")
            self.play(FadeIn(ex, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        t = load("receptive")["tables"]
        rows = [("LeNet-5", t["LeNet-5"], 32, CNN), ("AlexNet", t["AlexNet"], 224, KERNEL),
                ("VGG-16", t["VGG-16"], 224, KERNEL), ("ResNet-50", t["ResNet-50"], 224, KERNEL),
                ("our CIFAR network", t["our CIFAR network"], 32, CNN)]
        vmax = max(r[1][-1][4] for r in rows)
        bars = VGroup()
        for k, (nm, tab, img, col) in enumerate(rows):
            rf = tab[-1][4]
            w = 7.5 * rf / vmax
            b = Rectangle(width=w, height=0.44, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-3.2 + w / 2, 1.8 - 0.95 * k, 0])
            n = label(nm, font_size=22, color=col).next_to(b, UP, buff=0.06).align_to(b, LEFT)
            v = MathTex(rf"{rf}\ \text{{px}}", font_size=28, color=col).next_to(b, RIGHT, buff=0.15)
            wi = 7.5 * img / vmax
            mark = DashedLine([-3.2 + wi, 1.8 - 0.95 * k - 0.3, 0], [-3.2 + wi, 1.8 - 0.95 * k + 0.3, 0],
                              color=WHITE, stroke_width=2)
            bars.add(VGroup(b, n, v, mark))
        key = VGroup(DashedLine(ORIGIN, RIGHT * 0.4, color=WHITE, stroke_width=2),
                     label(r"the width of its input image", font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.15)
        key.to_corner(DR, buff=0.4)
        head = label(r"the receptive field of the last layer, \ computed from the published layer lists",
                     font_size=26).to_edge(UP, buff=0.4)
        a, v, r50 = t["AlexNet"][-1][4], t["VGG-16"][-1][4], t["ResNet-50"][-1][4]
        with self.voiceover(
            "Apply the rule to real networks, layer list by layer list. <bookmark mark='a'/> LeNet-5's last "
            f"convolution sees {t['LeNet-5'][-1][4]} pixels square: its whole input. <bookmark mark='b'/> AlexNet's "
            f"last pooling layer sees {a} pixels, VGG-16's {v}, ResNet-50's {r50}: wider than the 224-pixel images "
            "they were trained on, so a unit at the top can in principle be moved by any pixel. "
            "<bookmark mark='c'/> Our own CIFAR network, which we'll meet in Chapter 8, reaches "
            f"{t['our CIFAR network'][-1][4]} pixels on 32-pixel photographs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(bars[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars[1:4]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(bars[4], shift=RIGHT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pooling(self):
        e = load("equivariance")
        vals = np.array([[1, 3, 0, 2], [4, 2, 1, 1], [0, 1, 5, 2], [2, 0, 3, 1]])
        cells = VGroup()
        for i in range(4):
            for j in range(4):
                sq = Square(0.7, stroke_color=GREY_C, stroke_width=1.5, fill_color=FMAP,
                            fill_opacity=0.12 + 0.12 * vals[i, j])
                cells.add(VGroup(sq, MathTex(str(vals[i, j]), font_size=28).move_to(sq)))
        cells.arrange_in_grid(rows=4, cols=4, buff=0).move_to([-4.6, 0.6, 0])
        pooled = VGroup()
        for i in range(2):
            for j in range(2):
                v = vals[2 * i:2 * i + 2, 2 * j:2 * j + 2].max()
                sq = Square(0.9, stroke_color=KERNEL, stroke_width=2, fill_color=FMAP, fill_opacity=0.12 + 0.12 * v)
                pooled.add(VGroup(sq, MathTex(str(v), font_size=32).move_to(sq)))
        pooled.arrange_in_grid(rows=2, cols=2, buff=0).move_to([-1.6, 0.6, 0])
        quads = VGroup(*[SurroundingRectangle(VGroup(*[cells[4 * (2 * i + a) + 2 * j + b] for a in (0, 1)
                                                         for b in (0, 1)]), buff=0, color=KERNEL, stroke_width=2.5)
                         for i in range(2) for j in range(2)])
        arr = Arrow(cells.get_right(), pooled.get_left(), buff=0.15, color=GREY_B, stroke_width=3)
        pl = label(r"max pooling, $2 \times 2$, stride $2$", font_size=22, color=KERNEL).next_to(VGroup(cells, pooled),
                                                                                              UP, buff=0.3)
        errs = [e["err_pool_1"], e["err_pool_2"], e["err_pool_3"], e["err_pool_4"]]
        bars = VGroup()
        for k, v in enumerate(errs):
            h = max(3.0 * v / max(max(errs), 1e-9), 0.03)
            b = Rectangle(width=0.7, height=h, stroke_width=0, fill_color=SHIFTC if k % 2 else C.PENALTY,
                          fill_opacity=0.85)
            b.move_to([2.4 + 1.1 * k, -1.6 + h / 2, 0])
            n = MathTex(str(k + 1), font_size=28, color=GREY_A).next_to(b, DOWN, buff=0.12).set_y(-1.85)
            val = MathTex(f"{v:.2f}", font_size=24, color=WHITE).next_to(b, UP, buff=0.08)
            bars.add(VGroup(b, n, val))
        base = Line([1.9, -1.6, 0], [6.3, -1.6, 0], color=GREY_C, stroke_width=1.5)
        bl = label(r"shift of the input, \ in pixels", font_size=20, color=GREY_B).next_to(base, DOWN, buff=0.45)
        bt = label(r"after pooling: \ how far from a shifted copy", font_size=22, color=GREY_A)
        bt.next_to(VGroup(bars, base), UP, buff=0.3)
        cite_ = cite(r"Azulay \& Weiss (2019); \ Zhang (2019)", corner=DL)
        tag = note(r"computed: \ our LeNet's first layer, \ circular padding").to_corner(DR, buff=0.25)
        odd_bad = min(errs[0], errs[2]) > 10 * max(errs[1], errs[3], 1e-12)
        mid = ("A shift by 2 or 4 pixels comes out as an exact shift of the pooled map. A shift by 1 or 3 does "
               "not: after pooling it's a different map, off by a large fraction of its values."
               if odd_bad else
               "Here the pooled maps after odd and even shifts differ by similar amounts.")
        with self.voiceover(
            "Two more ingredients shrink the maps as they go up. <bookmark mark='a'/> Pooling: in each 2 by 2 "
            "block keep only the largest value, and move on by 2. Nudge a feature by a pixel inside its block and "
            "the pooled output doesn't change: a little invariance, Hubel and Wiesel's complex cell again. "
            "<bookmark mark='b'/> But a stride of 2 breaks the exact equivariance of the last chapter. "
            "<bookmark mark='c'/> We shifted the digit by one to four pixels before our first layer and its pooling. "
            + mid + " <bookmark mark='d'/> Real networks inherit this: in 2019 Aharon Azulay and Yair Weiss showed "
            "that shifting a photograph by a single pixel can change a modern network's answer, and Richard Zhang "
            "showed that blurring before each stride, as signal processing would, mostly fixes it."
        ) as vo:
            self.play(FadeIn(cells))
            vo.wait_until("a")
            self.play(Create(quads))
            self.play(GrowArrow(arr), FadeIn(pooled), FadeIn(pl))
            vo.wait_until("c")
            self.play(Create(base), FadeIn(bl), FadeIn(bt), FadeIn(tag))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def effective(self):
        r = load("receptive")
        t = r["tables"]["our CIFAR network"][-1][4]
        a = img_heat(np.asarray(r["erf_untrained"]), 3.4, sym=False, pos=KERNEL).move_to([-3.2, -0.2, 0])
        b = img_heat(np.asarray(r["erf_trained"]), 3.4, sym=False, pos=KERNEL).move_to([2.4, -0.2, 0])
        fa = SurroundingRectangle(a, buff=0, color=GREY_D, stroke_width=1.2)
        fb = SurroundingRectangle(b, buff=0, color=GREY_D, stroke_width=1.2)
        la = label(rf"untrained: \ RMS radius ${r['erf_untrained_radius']:.1f}$ px", font_size=22,
                   color=GREY_A).next_to(a, DOWN, buff=0.2)
        lb = label(rf"trained: \ RMS radius ${r['erf_trained_radius']:.1f}$ px", font_size=22,
                   color=CNN).next_to(b, DOWN, buff=0.2)
        head = label(r"how much each pixel moves one unit at the top: \ $|\partial\, \text{unit} / \partial\, "
                     r"\text{pixel}|$", font_size=26).to_edge(UP, buff=0.4)
        sub = label(rf"our CIFAR network: \ the whole $32 \times 32$ image is inside the theoretical field "
                    rf"(${t}$ px)", font_size=22, color=GREY_B).next_to(head, DOWN, buff=0.15)
        tag = note(r"computed: \ averaged over $64$ test photographs").to_corner(DR, buff=0.25)
        cite_ = cite(r"Luo, Li, Urtasun \& Zemel (2016)", corner=DL)
        grew = r["erf_trained_radius"] > r["erf_untrained_radius"] * 1.05
        verdict = (f"Training widens it, from {r['erf_untrained_radius']:.1f} pixels to "
                   f"{r['erf_trained_radius']:.1f}, as Luo and his colleagues found in large networks: the network "
                   "learns to use more of what it can see." if grew else
                   f"Here training leaves it about the same, {r['erf_untrained_radius']:.1f} pixels before and "
                   f"{r['erf_trained_radius']:.1f} after.")
        with self.voiceover(
            "But the receptive field is only where a unit could look. Where does it actually look? "
            "<bookmark mark='a'/> Take one unit at the top of our CIFAR network and ask how much it changes when "
            "each pixel changes: the gradient, averaged over many photographs. <bookmark mark='b'/> Its "
            "theoretical field covers the whole image, but the gradient is a soft blob in the middle. This is the "
            "effective receptive field, named by Wenjie Luo and colleagues in 2016: paths through the middle of "
            "the cone are many, paths to its edge are few, so the influence falls off roughly like a Gaussian. "
            "<bookmark mark='c'/> " + verdict
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(tag), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(a), Create(fa), FadeIn(la))
            vo.wait_until("c")
            self.play(FadeIn(b), Create(fb), FadeIn(lb))
        self.wait(0.3)
        self.clear_scene()
