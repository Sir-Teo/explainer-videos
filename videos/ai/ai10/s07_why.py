from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (ACTC, CNN, FMAP, HIST, KERNEL, MLPC, PART, load, pct, seed_band)
from videos.ai.ai10.specs import ALEXNET


class WhyItWon(VoiceoverScene):
    def construct(self):
        self.card()
        self.relu()
        self.race()
        self.dropout()
        self.data()
        self.together()

    def card(self):
        card = chapter_card(6, r"Why AlexNet won", r"Which ingredients mattered?", lit=(2012,), part=PART)
        with self.voiceover("Chapter six. Why AlexNet won."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def relu(self):
        ax = axes([-4, 4], [-1.2, 2.2], x_length=5.2, y_length=3.4, xticks=[-4, 0, 4], yticks=[-1, 0, 1, 2],
                  center=[-3.3, -0.3, 0])
        A = ax.ax
        xs = np.linspace(-4, 4, 200)
        f = {"relu": np.maximum(xs, 0), "tanh": np.tanh(xs), "sigmoid": 1 / (1 + np.exp(-xs))}
        df = {"relu": (xs > 0).astype(float), "tanh": 1 - np.tanh(xs) ** 2,
              "sigmoid": np.exp(-xs) / (1 + np.exp(-xs)) ** 2}
        fc = VGroup(*[curve(A, xs, np.clip(f[k], -1.2, 2.2), ACTC[k], 4) for k in ("relu", "tanh", "sigmoid")])
        ax2 = axes([-4, 4], [0, 1.1], x_length=5.2, y_length=2.4, xticks=[-4, 0, 4], yticks=[0, 0.25, 1],
                   center=[3.3, -0.8, 0])
        B = ax2.ax
        dc = VGroup(*[curve(B, xs, df[k], ACTC[k], 4) for k in ("relu", "tanh", "sigmoid")])
        t1 = label(r"the activation", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.25)
        t2 = label(r"its slope: \ what a gradient is multiplied by", font_size=24, color=GREY_A)
        t2.next_to(ax2, UP, buff=0.25)
        leg = legend([(ACTC["relu"], r"ReLU: \ $\max(0, x)$"), (ACTC["tanh"], r"$\tanh x$"),
                      (ACTC["sigmoid"], r"sigmoid: \ $1/(1+e^{-x})$")], font_size=22).to_corner(UL, buff=0.35)
        cite_ = cite(r"Nair \& Hinton (2010); \ Glorot, Bordes \& Bengio (2011); \ Krizhevsky et al.\ (2012)",
                     corner=DR)
        with self.voiceover(
            "The first difference inside AlexNet is small: the activation. <bookmark mark='a'/> The networks of "
            "the 1990s squashed each unit with a tanh or a sigmoid. AlexNet used the rectified linear unit, zero "
            "for negative inputs and the input itself otherwise, made popular by Vinod Nair and Hinton in 2010. "
            "<bookmark mark='b'/> The reason is in the slopes, which backpropagation multiplies the gradient by at "
            "every layer. The sigmoid's is at most a quarter, and both it and tanh flatten to nothing once a unit "
            "is pushed far from zero: it saturates and stops learning. The ReLU's slope is one wherever it is on. "
            "<bookmark mark='c'/> Krizhevsky measured it on CIFAR-10: a four-layer network with ReLUs reached "
            f"25 percent training error {ALEXNET['relu_speedup']} times faster than the same network with tanh."
        ) as vo:
            self.play(FadeIn(leg), Create(ax), FadeIn(t1))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in fc], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(ax2), FadeIn(t2), LaggedStart(*[Create(c) for c in dc], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        a = load("activations")
        runs, reach, thr = a["runs"], a["reach"], a["threshold"]
        S = int(a["steps"])
        ax = axes([0, S], [0, 0.95], x_length=7.4, y_length=4.2, xlabel=r"training steps ($64$ digits each)",
                  ylabel=r"training error (smoothed)", xticks=[0, S // 2, S], yticks=[0, 0.5, 0.9],
                  yfmt=lambda v: f"{int(100 * v)}\\%", center=[-1.6, -0.3, 0])
        A = ax.ax
        curves = VGroup()
        for act in ("relu", "tanh", "sigmoid"):
            R = [np.asarray(runs[f"{act}-{s}"]["curve"]) for s in (0, 1, 2)]
            xs = R[0][:, 0]
            curves.add(seed_band(A, xs, [r[:, 2] for r in R], ACTC[act]))
        thr_l = DashedLine(A.c2p(0, thr), A.c2p(S, thr), color=GREY_B, stroke_width=2)
        thr_t = label(rf"${int(100 * thr)}\%$", font_size=22, color=GREY_B).next_to(thr_l, RIGHT, buff=0.1)
        leg = legend([(ACTC["relu"], r"ReLU"), (ACTC["tanh"], r"tanh"), (ACTC["sigmoid"], r"sigmoid")],
                     font_size=24).to_corner(UR, buff=0.5)
        sub = note(r"computed: \ six $3 \times 3$ conv layers, \ SGD with momentum, \ each activation with its usual "
                   r"initialization; \ three seeds, \ band = min--max").to_edge(DOWN, buff=0.15)
        if sub.width > 13:
            sub.width = 13

        def mean_reach(act):
            v = [reach[f"{act}-{s}"] for s in (0, 1, 2)]
            return None if any(x is None for x in v) else float(np.mean(v))

        rr, rt, rs = mean_reach("relu"), mean_reach("tanh"), mean_reach("sigmoid")
        test = {k: np.mean([runs[f"{k}-{s}"]["test_error"] for s in (0, 1, 2)]) for k in ("relu", "tanh", "sigmoid")}
        if rr and rt:
            ratio = rt / rr
            verdict = (f"ReLU gets there in about {rr:.0f} steps, tanh in {rt:.0f}: {ratio:.1f} times as many."
                       if ratio > 1.15 else
                       f"ReLU and tanh get there in about the same time, {rr:.0f} and {rt:.0f} steps: at this "
                       "depth, with a good initialization, tanh keeps up. The gap opens in deeper networks.")
        else:
            verdict = "Not every run gets there within our budget."
        sig = (f"The sigmoid networks are still at {pct(test['sigmoid'], 0)} percent test error when we stop: its "
               "small slopes, multiplied layer after layer, starve the first layers of gradient."
               if rs is None else
               f"Even the sigmoid gets there, after {rs:.0f} steps.")
        with self.voiceover(
            "We ran the race ourselves, on the digits: the same six-layer convolutional network, three times with "
            "each activation, trained by plain gradient descent with momentum, as AlexNet was. "
            f"<bookmark mark='a'/> The dashed line is {int(100 * thr)} percent training error. "
            f"<bookmark mark='b'/> {verdict} <bookmark mark='c'/> {sig}"
        ) as vo:
            self.play(Create(ax), FadeIn(leg), FadeIn(sub))
            vo.wait_until("a")
            self.play(Create(thr_l), FadeIn(thr_t))
            self.play(LaggedStart(*[FadeIn(c) for c in curves[:2]], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(curves[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dropout(self):
        d = load("dropout")
        E = int(d["epochs"])
        runs = d["runs"]
        ax = axes([0, E], [0, 0.08], x_length=6.0, y_length=3.8, xlabel=r"passes over the $5{,}000$ digits",
                  ylabel=r"error", xticks=[0, E // 2, E], yticks=[0, 0.04, 0.08],
                  yfmt=lambda v: f"{100 * v:.0f}\\%", center=[2.6, -0.3, 0])
        A = ax.ax
        out = VGroup()
        vals = {}
        for p, col in (("0.0", MLPC), ("0.5", CNN)):
            R = [np.asarray(runs[f"{p}-{s}"]) for s in (0, 1, 2)]
            xs = R[0][:, 0]
            tr = seed_band(A, xs, [np.minimum(r[:, 1], 0.08) for r in R], col, opacity=0.1, stroke_width=2.5)
            tr[1].set_stroke(opacity=0.7)
            te = seed_band(A, xs, [np.minimum(r[:, 2], 0.08) for r in R], col)
            out.add(VGroup(tr, te))
            vals[p] = (np.mean([r[-1, 1] for r in R]), np.mean([r[-1, 2] for r in R]))
        leg = legend([(MLPC, r"no dropout"), (CNN, r"dropout, \ $p = 0.5$")], font_size=22)
        leg.next_to(ax, UP, buff=0.2).align_to(ax, RIGHT)
        kl = label(r"solid: \ test digits; \ faint: \ the training digits", font_size=20, color=GREY_B)
        kl.next_to(leg, LEFT, buff=0.4)
        # a schematic network with dropped units
        layers = [4, 6, 6, 3]
        dots = VGroup()
        g = np.random.default_rng(7)
        dropped = []
        for li, n in enumerate(layers):
            col = VGroup(*[Circle(radius=0.13, stroke_color=GREY_B, stroke_width=2) for _ in range(n)])
            col.arrange(DOWN, buff=0.22).move_to([-5.6 + 1.1 * li, 0.0, 0])
            dots.add(col)
            if 0 < li < len(layers) - 1:
                dropped += [(li, k) for k in range(n) if g.random() < 0.5]
        wires = VGroup()
        for li in range(len(layers) - 1):
            for a_ in range(layers[li]):
                for b_ in range(layers[li + 1]):
                    off = (li, a_) in dropped or (li + 1, b_) in dropped
                    wires.add(Line(dots[li][a_].get_center(), dots[li + 1][b_].get_center(), stroke_width=0.8,
                                   color=GREY_D if off else GREY_B, stroke_opacity=0.25 if off else 0.6))
        crosses = VGroup(*[Cross(dots[li][k], stroke_color=C.PENALTY, stroke_width=3, scale_factor=0.8)
                           for li, k in dropped])
        nl = label(r"each step, \ half the hidden units are switched off at random", font_size=20, color=GREY_A)
        nl.next_to(dots, DOWN, buff=0.35)
        if nl.width > 4.8:
            nl.width = 4.8
        cite_ = cite(r"Hinton et al.\ (2012); \ Srivastava et al.\ (2014)", corner=DL)
        tag = note(r"computed: \ a $784$--$512$--$512$--$10$ network, \ three seeds").to_corner(DR, buff=0.2)
        gap0, gap5 = vals["0.0"][1] - vals["0.0"][0], vals["0.5"][1] - vals["0.5"][0]
        better = vals["0.5"][1] < vals["0.0"][1] - 0.002
        verdict = (f"With dropout the test error ends at {pct(vals['0.5'][1])} percent instead of "
                   f"{pct(vals['0.0'][1])}." if better else
                   f"Here dropout changes the test error little: {pct(vals['0.5'][1])} percent against "
                   f"{pct(vals['0.0'][1])}.")
        with self.voiceover(
            "The second ingredient: dropout, from Hinton's group the same year. <bookmark mark='a'/> At every "
            "training step, switch off each hidden unit with probability one half, so the network can't lean on a "
            "conspiracy of a few; at test time keep them all, scaled to match. It is like averaging a huge family "
            "of thinner networks that share weights. AlexNet used it in its two big fully connected layers; "
            "without it, its authors wrote, the network overfitted substantially. <bookmark mark='b'/> We gave a fully connected network "
            "just five thousand digits and let it train for sixty passes. Without dropout it learns every "
            f"training digit, {pct(vals['0.0'][0])} percent wrong on them, while the test error stalls. "
            f"<bookmark mark='c'/> " + verdict + f" The gap between training and test shrinks from "
            f"{pct(gap0)} points to {pct(gap5)}."
        ) as vo:
            self.play(FadeIn(dots), Create(wires), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in crosses], lag_ratio=0.1), FadeIn(nl))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(leg), FadeIn(kl), FadeIn(tag), FadeIn(out[0]))
            vo.wait_until("c")
            self.play(FadeIn(out[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def data(self):
        d = load("datasize")
        sizes = [int(n) for n in d["sizes"]]
        runs = d["runs"]
        lx = [math.log10(n) for n in sizes]
        ax = axes([2.5, 5.0], [-2.5, 0], x_length=6.4, y_length=4.0, xlabel=r"training digits", ylabel=r"test error",
                  xticks=[3, 4], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[-2, -1, 0],
                  yfmt=lambda v: {-2: r"1\%", -1: r"10\%", 0: r"100\%"}[int(v)], center=[-2.4, -0.3, 0])
        A = ax.ax
        plain = [[math.log10(runs[f"{n}-0-{s}"]["test_error"]) for n in sizes] for s in (0, 1, 2)]
        aug_n = [n for n in sizes if f"{n}-1-0" in runs]
        aug = [[math.log10(runs[f"{n}-1-{s}"]["test_error"]) for n in aug_n] for s in (0, 1, 2)]
        cp = seed_band(A, lx, plain, CNN)
        ca = seed_band(A, [math.log10(n) for n in aug_n], aug, KERNEL)
        dots = VGroup(*[Dot(A.c2p(x, np.mean([p[i] for p in plain])), radius=0.06, color=CNN)
                        for i, x in enumerate(lx)])
        leg = legend([(CNN, r"the digits as they are"), (KERNEL, r"with shifted copies")], font_size=22)
        leg.to_corner(UR, buff=0.5)
        slope = float(d["slope"])
        fit = label(rf"slope $\approx {slope:.2f}$: \ error $\propto n^{{{slope:.2f}}}$", font_size=26,
                    color=CNN).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        tag = note(rf"computed: \ LeNet, \ ${int(d['steps']):,}$ steps each, \ three seeds".replace(",", "{,}"))
        tag.to_corner(DR, buff=0.2)
        e_small = np.mean([runs[f"{sizes[1]}-0-{s}"]["test_error"] for s in (0, 1, 2)])
        e_small_aug = np.mean([runs[f"{sizes[1]}-1-{s}"]["test_error"] for s in (0, 1, 2)]) if aug_n else e_small
        e_next = np.mean([runs[f"{sizes[2]}-0-{s}"]["test_error"] for s in (0, 1, 2)])
        if e_small_aug < e_small - 0.002:
            tail = ("better than four times as many real digits." if e_small_aug < e_next else
                    f"not as good as four times as many real digits, {pct(e_next)}.")
            aug_v = (f"Shifted copies help: with {sizes[1]:,} digits, {pct(e_small)} percent wrong becomes "
                     f"{pct(e_small_aug)}, " + tail)
        else:
            aug_v = "Shifted copies barely help at this size."
        with self.voiceover(
            "The third ingredient was the one ImageNet supplied: data. <bookmark mark='a'/> Train the same "
            "LeNet, for the same number of steps, on more and more digits. On a log-log plot the test error falls "
            f"along a straight line, a power law with slope about {slope:.2f}: each doubling of the data cuts the "
            f"errors by {100 * (1 - 2 ** slope):.0f} percent. <bookmark mark='b'/> And there is a cheap way to "
            "get more: make it. AlexNet trained on random crops of its photographs and their mirror images, "
            f"{ALEXNET['augment_factor']:,} variants of each. " + aug_v + " Part 12 is about such straight lines."
        ) as vo:
            self.play(Create(ax), FadeIn(leg), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cp), LaggedStart(*[FadeIn(dd, scale=0.5) for dd in dots], lag_ratio=0.2))
            self.play(FadeIn(fit))
            vo.wait_until("b")
            self.play(FadeIn(ca))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def together(self):
        items = [
            (2010, r"rectified linear units", r"Nair \& Hinton", CNN),
            (2012, r"dropout", r"Hinton, Srivastava, Krizhevsky, Sutskever \& Salakhutdinov", CNN),
            (2009, r"a million labelled photographs", r"ImageNet; \ augmentation on top", FMAP),
            (2009, r"GPUs for deep networks", r"Raina, Madhavan \& Ng; \ Part 17", KERNEL),
        ]
        cards = VGroup(*[history_card(y, w, t, width=6.2, color=c) for y, w, t, c in items])
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.4)).move_to(DOWN * 0.1)
        head = label(r"none of it new; \ all of it together, \ at scale", font_size=34).to_edge(UP, buff=0.45)
        with self.voiceover(
            "So which ingredient mattered? <bookmark mark='a'/> None of them was new in 2012: rectified units from "
            "2010, dropout from that year, convolutional networks from 1989, GPUs for neural networks from 2009, "
            "and ImageNet from 2009. <bookmark mark='b'/> What was new was all of them together, at a scale where "
            "each one mattered: enough data that a sixty-million-weight network didn't simply memorize it, "
            "activations that let gradients reach eight layers down, and enough arithmetic to train it in a week."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.3), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()


_ = HIST
