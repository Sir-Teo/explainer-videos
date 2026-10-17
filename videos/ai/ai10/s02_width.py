from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import MUP, SP, WIDTH_COLORS, curve, load, log_axes


class Width(VoiceoverScene):
    def construct(self):
        self.card()
        self.lazy()
        self.mup()

    def card(self):
        card = chapter_card(1, r"Wider and wider", r"What changes when a network gets very wide?", part=10)
        with self.voiceover("Chapter one. Wider and wider."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def lazy(self):
        z = load("lazy")
        W, M = np.asarray(z["widths"], float), np.asarray(z["moved"])
        slope = float(z["slope"])
        lx, ly = np.log10(W), np.log10(M)
        y0, y1 = math.floor(ly.min() * 2) / 2 - 0.25, math.ceil(ly.max() * 2) / 2 + 0.25
        ax, labs = log_axes((1, 3.5), (y0, y1), center=[-2.1, -0.5, 0],
                            x_ticks=[("10", 1), ("100", 2), ("1{,}000", 3)],
                            y_ticks=list(np.arange(math.ceil(y0), y1, 1)), y_fmt=r"10^{{{:.0f}}}")
        xn = label(r"width of the hidden layers", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        yn = label(r"how much the hidden features changed in training", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15)
        yn.align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.08, color=SP) for x, y in zip(lx, ly)])
        b = np.polyfit(lx, ly, 1)
        fit = Line(ax.c2p(1.4, np.polyval(b, 1.4)), ax.c2p(3.4, np.polyval(b, 3.4)), color=WHITE, stroke_width=2.5)
        sl = label(rf"slope ${slope:.2f}$", font_size=28, color=WHITE).next_to(fit.get_center(), UR, buff=0.2)
        notes = VGroup(label(r"the features change less and less", font_size=26, color=SP),
                       label(r"in the limit: \ a fixed kernel, \\ the neural tangent kernel", font_size=26, color=GREY_A),
                       label(r"a model that no longer learns features", font_size=26, color=C.BITS))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.5, 1.7, 0])  # above the card
        cite_ = cite(r"A.~Jacot, F.~Gabriel \& C.~Hongler, \textit{Neural Tangent Kernel} (2018)", corner=DR)
        # the lazy picture: the hidden features frozen as they started, only the weights on them re-learned
        ins = VGroup(*[Dot(radius=0.07, color=GREY_B) for _ in range(4)]).arrange(DOWN, buff=0.3)
        hid = VGroup(*[Circle(radius=0.1, color=SP, stroke_width=2.5) for _ in range(6)]).arrange(DOWN, buff=0.14)
        hid.next_to(ins, RIGHT, buff=1.2)
        out = Circle(radius=0.13, color=C.BITS, stroke_width=3).next_to(hid, RIGHT, buff=1.2)
        frozen = VGroup(*[DashedLine(a.get_center(), b.get_left(), color=GREY_D, stroke_width=1.2, dash_length=0.05)
                          for a in ins for b in hid])
        learned = VGroup(*[Line(b.get_right(), out.get_left(), color=C.BITS, stroke_width=2.2) for b in hid])
        lazy_pic = VGroup(frozen, learned, ins, hid, out,
                          label(r"frozen", font_size=20, color=GREY_B).next_to(frozen, DOWN, buff=0.1),
                          label(r"re-weighted", font_size=20, color=C.BITS).next_to(learned, DOWN, buff=0.1))
        lazy = gloss(r"the lazy regime", r"a very wide net barely changes its features: \\ it can only re-weight what it "
                     r"started with, \\ like Part 5's kernel methods, \ with a frozen similarity rule", lazy_pic,
                     corner=DR, width=4.3, color=SP)
        lazy.shift(UP * 0.45)
        with self.voiceover(
            "Take part nine's character model and make it wider and wider, trained by plain gradient descent, with "
            "step sizes that keep a wide network stable. Measure how much its hidden features change during "
            "training: a feature is what one hidden unit computes from the input, one pattern the network has "
            "learned to look for. <bookmark mark='a'/> The wider the network, the less they "
            f"change. The slope here is about minus {abs(slope):.1f}; in theory it tends to minus a half: one over "
            "the square root of the width. <bookmark mark='b'/> In the limit, the features don't move at all. A very "
            "wide net can only re-weight what it started with, like part five's kernel methods with a frozen "
            "similarity rule: a fixed kernel, called the neural tangent kernel. This is called the lazy regime. "
            "Elegant, and exactly what we don't want: a network whose features never change learns nothing new "
            "about its data's structure."
        ) as vo:
            self.play(Create(ax), FadeIn(labs), FadeIn(xn), FadeIn(yn), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.15), run_time=1.5)
            self.play(Create(fit), FadeIn(sl), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), FadeIn(lazy, shift=UP * 0.2))
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mup(self):
        m = load("mup")
        lrs = np.log10(np.asarray(m["lrs"]))
        widths = [int(w) for w in m["widths"]]
        allv = np.concatenate([np.asarray(m[f"{k}{w}"]) for k in ("sp", "mup") for w in widths])
        allv = allv[np.isfinite(allv)]
        lo, hi = float(np.floor(allv.min() * 10) / 10), float(min(np.ceil(np.percentile(allv, 85) * 10) / 10, allv.min() + 1.2))
        panels = VGroup()
        for k, (mode, title, col) in enumerate((("sp", r"the usual parametrization", SP), ("mup", r"$\mu$P", MUP))):
            ax = CornerAxes(x_range=[lrs[0], lrs[-1], 0.5], y_range=[lo, hi, 0.2], x_length=5.6, y_length=3.8, tips=False,
                      axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
            ax.move_to([-3.4 + 6.8 * k, -0.6, 0])
            lines, bests = VGroup(), VGroup()
            for w, wc in zip(widths, WIDTH_COLORS):
                v = np.asarray(m[f"{mode}{w}"])
                v = np.where(np.isfinite(v), np.minimum(v, hi), hi)
                lines.add(curve(ax, lrs, v, wc, 3))
                i = int(np.argmin(v))
                bests.add(Dot(ax.c2p(lrs[i], v[i]), radius=0.08, color=wc))
            xl = label(r"learning rate (log)", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.15)
            t = label(title, font_size=30, color=col).next_to(ax, UP, buff=0.2)
            yt = VGroup(*[MathTex(f"{v:.1f}", font_size=20, color=GREY_B).next_to(ax.c2p(lrs[0], v), LEFT, buff=0.08)
                          for v in np.arange(lo, hi + 1e-9, 0.2)])
            panels.add(VGroup(ax, xl, t, lines, bests, yt))
        key = VGroup(*[label(rf"width ${w:,}$".replace(",", "{,}"), font_size=24, color=c) for w, c in zip(widths, WIDTH_COLORS)])
        key.arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.3)
        yn = label(r"held-out bits after $800$ steps \ (lower is better)", font_size=22, color=GREY_A).next_to(key, DOWN, buff=0.15)
        drift = m["drift"]
        colors = {r"\tfrac{1}{n}": MUP}
        rule = cmath(r"\text{hidden learning rate}", r"\;\propto\;", r"\tfrac{1}{n}", colors=colors, font_size=30)
        rule.next_to(panels[1][0], DOWN, buff=0.55)
        cite_ = cite(r"G.~Yang \& E.~Hu (2021); \ G.~Yang et al., \textit{Tensor Programs V} (2022)", corner=DR)
        bl = m["best_loss"]
        transfer = drift["sp"] >= drift["mup"] + 0.4
        # muP in a picture: as the layer widens, its starting weights and its step size shrink
        cols_ = VGroup()
        for j, w_ in enumerate((1, 2, 4)):
            layer = Rectangle(width=0.45 * w_, height=0.3, stroke_color=MUP, stroke_width=2, fill_color=MUP, fill_opacity=0.2)
            init = Rectangle(width=0.18, height=0.9 / w_ ** 0.5, stroke_width=0, fill_color=GREY_B, fill_opacity=0.9)
            step = Rectangle(width=0.18, height=0.9 / w_, stroke_width=0, fill_color=C.BITS, fill_opacity=0.9)
            bars_ = VGroup(init, step).arrange(RIGHT, buff=0.08, aligned_edge=DOWN).next_to(layer, DOWN, buff=0.12)
            cols_.add(VGroup(layer, bars_))
        cols_.arrange(RIGHT, buff=0.5, aligned_edge=UP)
        mkey = VGroup(label(r"layer width", font_size=20, color=MUP), label(r"starting weights", font_size=20, color=GREY_B),
                      label(r"step size", font_size=20, color=C.BITS)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        mkey.next_to(cols_, RIGHT, buff=0.4)
        mupc = gloss(r"$\mu$P", r"as the network widens, shrink each layer's \\ starting weights and step size, \\ so every "
                     r"layer keeps changing by about the same amount", VGroup(cols_, mkey), width=5.6, color=MUP)
        mupc.scale(1.25).move_to(DOWN * 0.6)  # mid-frame, before the panels: room to be larger
        with self.voiceover(
            "Greg Yang asked how to scale a network so that every layer keeps learning features, at any width. His "
            "answer, the maximal update parametrization, mu-P, rescales the initialization and learning rate of each "
            "layer by the width. <bookmark mark='m'/> In plain terms: as the network widens, shrink each layer's "
            "starting weights and step size, so that every layer keeps changing by about the same amount. "
            "<bookmark mark='a'/> Sweep the learning rate at three widths, the usual way"
            + (f": the best learning rate drifts as the model grows, by {drift['sp']:.1f} powers of ten here. "
               f"<bookmark mark='b'/> In mu-P, the curves line up: the best learning rate stays put, within "
               f"{drift['mup']:.1f}. So you can tune a small model and copy its settings to a big one."
               if transfer else
               f". At our small sizes, the best rate barely moves. <bookmark mark='b'/> Now in mu-P. What shows "
               f"here is what mu-P is for: its widest model is the best of all, {bl['mup'][-1]:.2f} bits against "
               f"{bl['sp'][-1]:.2f} the usual way, because every layer keeps learning. At large scale the usual "
               "way's best rate does drift, and mu-P holds it still: Yang and colleagues tuned a forty-million-"
               "parameter model and copied its settings to a GPT-3 of six point seven billion, which beat the "
               "original.")
        ) as vo:
            self.play(FadeIn(key), FadeIn(cite_), FadeIn(yn), FadeIn(mupc, shift=UP * 0.2))  # the picture from the first word
            vo.wait_until("a")
            self.play(FadeOut(mupc))
            p = panels[0]
            self.play(Create(p[0]), FadeIn(p[1]), FadeIn(p[2]), FadeIn(p[5]), LaggedStart(*[Create(l_) for l_ in p[3]], lag_ratio=0.3),
                      run_time=2.0)
            self.play(FadeIn(p[4]))
            vo.wait_until("b")
            p = panels[1]
            self.play(Create(p[0]), FadeIn(p[1]), FadeIn(p[2]), FadeIn(p[5]), LaggedStart(*[Create(l_) for l_ in p[3]], lag_ratio=0.3),
                      run_time=2.0)
            self.play(FadeIn(p[4]), FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()
