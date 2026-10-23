from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (CNN, FMAP, HIST, KERNEL, MLPC, OK, PART, grid_of, img_gray, img_heat, load,
                                   nn_layer_boxes, oriented_fit, pct, seed_band)
from videos.ai.ai10.specs import LENET5_1998, LENET5_DISTORT, ZIP1989


class LeNet(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.architecture()
        self.replay()
        self.results()
        self.bias()

    def card(self):
        card = chapter_card(4, r"LeNet and MNIST", r"Can a network learn its features from the pixels up?",
                            lit=(1986, 1998), part=PART)
        with self.voiceover("Chapter four. LeNet and MNIST."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(1980, r"Kunihiko Fukushima, \ the Neocognitron",
                         r"layers of S-cells and C-cells, \ after Hubel and Wiesel's simple and complex cells; "
                         r"\ tolerant of shifts; \ trained without backpropagation", width=4.3, color=HIST),
            history_card(1989, r"Yann LeCun and colleagues, \ Bell Labs",
                         rf"backpropagation through shared weights; \ ${ZIP1989['train']:,}$ zip-code digits; \ "
                         rf"${ZIP1989['error']:.1f}\%$ test error".replace(",", "{,}"), width=4.3, color=CNN),
            history_card(1989, r"Alex Waibel and colleagues, \ the time-delay network",
                         r"the same idea along time: \ shared weights sliding over speech", width=4.3, color=HIST),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.4)
        if cards.width > 13.4:
            cards.width = 13.4
        foot = label(rf"about ${ZIP1989['params']:,}$ free parameters; \ three days of training on a workstation"
                     .replace(",", "{,}"), font_size=22, color=GREY_B).to_edge(DOWN, buff=0.7)
        cite_ = cite(r"Fukushima (1980); \ LeCun et al.\ (1989); \ Waibel et al.\ (1989); \ "
                     r"figures as reproduced by Karpathy (2022)", corner=DL)
        with self.voiceover(
            "The first network built on Hubel and Wiesel's plan came from Japan. <bookmark mark='a'/> In 1980 "
            "Kunihiko Fukushima's Neocognitron stacked layers of S-cells and C-cells, after the simple and complex "
            "cells, and recognized digits even when they were shifted. But it learned without backpropagation, by "
            "rules of its own. <bookmark mark='b'/> In 1989, at Bell Labs, Yann LeCun and his colleagues trained "
            "a convolutional network end to end with backpropagation, through the shared weights, on digits from "
            f"real zip codes: {ZIP1989['train']:,} for training, with {ZIP1989['error']:.0f} percent errors on the "
            "test digits. <bookmark mark='c'/> The same year Alex Waibel's group slid shared weights along time."
        ) as vo:
            ghosts = cards.copy().set_opacity(0.25)
            self.play(FadeIn(ghosts))
            vo.wait_until("a")
            self.play(FadeOut(ghosts[0]), FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(ghosts[1]), FadeIn(cards[1], shift=UP * 0.2), FadeIn(foot), FadeIn(cite_))
            vo.wait_until("c")
            self.play(FadeOut(ghosts[2]), FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def architecture(self):
        dd = load("data")
        grid = np.asarray(dd["mnist_grid"])  # (10, 10, 28, 28)
        tiles = grid_of([img_gray(grid[k, i], 0.42) for i in range(10) for k in range(10)], cols=10, buff=0.03)
        tiles.move_to([4.3, 1.0, 0])
        tl = label(r"MNIST: \ $60{,}000$ training digits, \ $10{,}000$ test", font_size=22, color=GREY_A)
        tl.next_to(tiles, DOWN, buff=0.2)
        widths = [0.25, 0.25, 0.32, 0.32, 0.18, 0.15, 0.12]
        heights = [2.2, 1.4, 1.2, 0.8, 2.0, 1.5, 0.9]
        cols = [FMAP, GREY_B, FMAP, GREY_B, CNN, CNN, OK]
        boxes = nn_layer_boxes(widths, heights, cols, buff=0.42, depth=0.22).move_to([-3.0, -1.3, 0])
        names = [r"C1 \\ $6 @ 28^2$", r"S2 \\ $6 @ 14^2$", r"C3 \\ $16 @ 10^2$", r"S4 \\ $16 @ 5^2$",
                 r"C5 \\ $120$", r"F6 \\ $84$", r"out \\ $10$"]
        nl = VGroup(*[label(n, font_size=18, color=c).next_to(b, DOWN, buff=0.15) for n, b, c in
                      zip(names, boxes, cols)])
        nl.set_y(boxes.get_bottom()[1] - 0.45)
        head = label(r"LeNet-5 \ (LeCun, Bottou, Bengio \& Haffner, 1998)", font_size=28, color=CNN)
        head.next_to(boxes, UP, buff=1.0).align_to(boxes, LEFT)
        facts = VGroup(label(rf"published test error: \ ${LENET5_1998}\%$, \ ${LENET5_DISTORT}\%$ with "
                             r"distorted copies", font_size=22, color=GREY_A),
                       label(r"its check reader read several million checks a day", font_size=22, color=GREY_A))
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(head, DOWN, buff=0.2).align_to(head, LEFT)
        ours = note(r"ours: \ the same layout, \ with today's ReLU, \ max pooling and a softmax").to_corner(DR,
                                                                                                          buff=0.25)
        with self.voiceover(
            "By 1998 the design had a name and a benchmark. <bookmark mark='a'/> LeNet-5, from LeCun, Leon Bottou, "
            "Yoshua Bengio and Patrick Haffner: two rounds of convolution and pooling, six maps then sixteen, "
            "then three fully connected layers down to ten digits. <bookmark mark='b'/> And MNIST, seventy "
            "thousand handwritten digits, remixed from two US government collections, one written by Census "
            "Bureau employees and one by high-school students. <bookmark mark='c'/> LeNet-5 missed "
            f"{LENET5_1998} percent of the test digits, {LENET5_DISTORT} trained on distorted copies, and a "
            "system built around it went to work in banks, reading several million checks a day. "
            "<bookmark mark='d'/> We built the same layout, with today's ReLU and max pooling."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in boxes], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(n) for n in nl], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.005), FadeIn(tl), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(facts, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(ours))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        L = load("lenet")
        steps = [int(s) for s in L["steps"]]
        errs = np.asarray(L["snap_error"])
        W1, A1, P = np.asarray(L["w1"]), np.asarray(L["a1"]), np.asarray(L["p"])
        digit = np.asarray(L["digit"])
        ax = axes([0, math.log10(steps[-1] + 10) + 0.05], [0, 1.0], x_length=5.6, y_length=3.4,
                  xlabel=r"training steps ($64$ digits each)", ylabel=r"test error", xticks=[1, 2, 3],
                  xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[0, 0.5, 1.0], yfmt=lambda v: f"{int(100 * v)}\\%",
                  center=[-3.6, 0.6, 0])
        A = ax.ax
        xs = [math.log10(s + 10) for s in steps]
        k = ValueTracker(0)

        def path():
            n = int(k.get_value()) + 1
            return VMobject(color=CNN, stroke_width=4).set_points_as_corners([A.c2p(x, e) for x, e in
                                                                               zip(xs[:n], errs[:n])]
                                                                              + ([A.c2p(xs[0], errs[0])]
                                                                                 if n == 1 else []))

        live = always_redraw(path)
        rider = always_redraw(lambda: glow_dot(A.c2p(xs[int(k.get_value())], errs[int(k.get_value())]), color=CNN))

        def readout():
            i = int(k.get_value())
            return VGroup(MathTex(rf"\text{{step }}{steps[i]:,}".replace(",", "{,}"), font_size=28),
                          MathTex(rf"{100 * errs[i]:.1f}\%\ \text{{wrong}}", font_size=28, color=CNN)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1).move_to([-2.2, 2.9, 0])

        clock = always_redraw(readout)

        def filters(i):
            return grid_of([img_heat(W1[i][f], 0.62) for f in range(6)], cols=6, buff=0.1)

        def maps(i):
            return grid_of([img_heat(A1[i][f], 0.62, sym=False, pos=FMAP) for f in range(6)], cols=6, buff=0.1)

        def probs(i):
            bars = VGroup()
            for d in range(10):
                h = max(1.3 * P[i][d], 0.02)
                bars.add(Rectangle(width=0.26, height=h, stroke_width=0,
                                   fill_color=OK if d == int(L["digit_label"]) else GREY_B, fill_opacity=0.85))
            bars.arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
            return bars

        fpos, mpos, ppos = np.array([3.6, 2.2, 0]), np.array([3.6, 0.4, 0]), np.array([4.2, -2.0, 0])
        cur_f, cur_m, cur_p = filters(0).move_to(fpos), maps(0).move_to(mpos), probs(0)
        cur_p.move_to(ppos).align_to(ppos + DOWN * 0.65, DOWN)
        fl = label(r"its six first-layer kernels", font_size=20, color=KERNEL).next_to(cur_f, UP, buff=0.12)
        ml = label(r"what they make of this digit", font_size=20, color=FMAP).next_to(cur_m, UP, buff=0.12)
        dg = img_gray(digit, 1.3).move_to([1.2, -1.9, 0])
        digits = VGroup(*[MathTex(str(d), font_size=20, color=GREY_B) for d in range(10)])
        pl = label(r"its answer", font_size=20, color=OK).move_to(ppos + UP * 1.05)
        tag = note(r"computed: \ seed $0$ of three").to_corner(DR, buff=0.2)

        def place_digits():
            for d, b in zip(digits, cur_p):
                d.next_to(b, DOWN, buff=0.08)

        place_digits()
        e0, eN = errs[0], errs[-1]
        i_half = next((i for i, e in enumerate(errs) if e < 0.05), len(errs) - 1)
        if errs[i_half] < 0.05:
            fast = f"Within {steps[i_half]:,} steps, under five percent wrong."
        else:
            fast = f"Even after {steps[i_half]:,} steps it is {pct(errs[i_half], 0)} percent wrong."
        # which kernels look like a bar or an edge (Chapter 2's test), at the start and at the end
        fit0 = [oriented_fit(w) for w in W1[0]]
        fitN = [oriented_fit(w) for w in W1[-1]]
        n0 = sum(f > 0.45 for f, _ in fit0)
        nN = sum(f > 0.45 for f, _ in fitN)
        angs = sorted(a for f, a in fitN if f > 0.45)
        spread = len(angs) > 1 and min(min(abs(a - b), 180 - abs(a - b)) for i_, a in enumerate(angs)
                                       for b in angs[i_ + 1:]) >= 15
        if nN >= 4 and spread:
            kern = (f"Of the six kernels, {nN} now match a bar or an edge, each at a different angle; at the start, "
                    f"{n0} did.")
        else:
            kern = f"Of the six kernels, {nN} match a bar or an edge; at the start, {n0} did."
        with self.voiceover(
            "Now let's watch ours learn. On the left, its test error; on the right, its six first-layer kernels, "
            "what they make of one digit, and its answer. "
            f"<bookmark mark='a'/> At the start the kernels are random noise and the answers are guesses: "
            f"{pct(e0, 0)} percent wrong. <bookmark mark='b'/> {fast} <bookmark mark='c'/> After {L['epochs']} "
            f"passes over the training digits, {pct(eN, 2)} percent wrong. {kern} Nobody designed those kernels: "
            "they are whatever made the answers right."
        ) as vo:
            self.play(Create(ax), FadeIn(cur_f), FadeIn(cur_m), FadeIn(fl), FadeIn(ml), FadeIn(dg), FadeIn(cur_p),
                      FadeIn(digits), FadeIn(pl), FadeIn(tag))
            self.add(live, rider, clock)
            vo.wait_until("a")
            for i in range(1, len(steps)):
                if i == 1:
                    vo.wait_until("b")
                if i == len(steps) - 2:
                    vo.wait_until("c")
                nf, nm, npb = filters(i).move_to(fpos), maps(i).move_to(mpos), probs(i)
                npb.move_to(ppos).align_to(ppos + DOWN * 0.65, DOWN)
                self.play(k.animate.set_value(i), FadeOut(cur_f), FadeIn(nf), FadeOut(cur_m), FadeIn(nm),
                          Transform(cur_p, npb), run_time=0.9)
                cur_f, cur_m = nf, nm
        for m in (live, rider, clock):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        L = load("lenet")
        errs = np.asarray(L["test_error"])
        wrong = np.asarray(L["wrong_img"])
        wt, wp = L["wrong_true"], L["wrong_pred"]
        gal = Group()
        for img, t, p in list(zip(wrong, wt, wp))[:16]:
            im = img_gray(img, 1.0)
            lab = VGroup(MathTex(str(t), font_size=22, color=GREY_B), MathTex(r"\to", font_size=20, color=GREY_C),
                         MathTex(str(p), font_size=22, color=C.PENALTY)).arrange(RIGHT, buff=0.06)
            lab.next_to(im, DOWN, buff=0.06)
            gal.add(Group(im, lab))
        gal.arrange_in_grid(rows=2, cols=8, buff=(0.22, 0.25)).move_to([0, -1.3, 0])
        gl = label(r"some of the digits it got wrong: \ true $\to$ its answer", font_size=22, color=GREY_A)
        gl.next_to(gal, UP, buff=0.2)
        m, lo, hi = errs.mean(), errs.min(), errs.max()
        res = VGroup(label(r"test error, \ three seeds:", font_size=28, color=GREY_A),
                     MathTex(rf"{100 * m:.2f}\% \quad ({100 * lo:.2f}\text{{--}}{100 * hi:.2f}\%)", font_size=36,
                             color=CNN),
                     label(rf"LeNet-5 in 1998: \ ${LENET5_1998}\%$", font_size=26, color=GREY_B))
        res.arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.7)
        if res.width > 13:
            res.width = 13
        if hi < LENET5_1998 / 100:
            cmp = (f"a little better than LeNet-5's {LENET5_1998} percent in 1998: today's ReLU and Adam, and "
                   "ten thousand times the computing, help.")
        elif lo > LENET5_1998 / 100:
            cmp = (f"a little worse than LeNet-5's {LENET5_1998} percent; we trained for only {L['epochs']} passes "
                   "over the digits.")
        else:
            cmp = f"about where LeNet-5 was in 1998, at {LENET5_1998} percent."
        with self.voiceover(
            f"Over three training runs with different random starts, our network gets {pct(m, 2)} percent of the "
            f"test digits wrong, between {pct(lo, 2)} and {pct(hi, 2)}: {cmp} <bookmark mark='a'/> And here "
            "are some it got wrong. Several of them would make a person hesitate too."
        ) as vo:
            self.play(FadeIn(res, shift=UP * 0.1), FadeIn(gl), LaggedStart(*[FadeIn(g) for g in gal], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(Indicate(gl, color=WHITE))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bias(self):
        M = load("mlp_cnn")
        ec, em = np.asarray(M["error"]["cnn"]), np.asarray(M["error"]["mlp"])
        sh = np.asarray(M["shifts"])
        sc, sm = np.asarray(M["shifted"]["cnn"]), np.asarray(M["shifted"]["mlp"])
        ax = axes([0, sh[-1]], [0, 1.0], x_length=5.2, y_length=3.2, xlabel=r"shift of the test digits, pixels",
                  ylabel=r"test error", xticks=list(sh), yticks=[0, 0.5, 1.0],
                  yfmt=lambda v: f"{int(100 * v)}\\%", center=[-3.4, -0.4, 0])
        cnn_c = seed_band(ax.ax, sh, sc, CNN)
        mlp_c = seed_band(ax.ax, sh, sm, MLPC)
        leg = legend([(CNN, rf"LeNet, \ ${M['params']['cnn']:,}$ weights".replace(",", "{,}")),
                      (MLPC, rf"MLP, \ ${M['params']['mlp']:,}$ weights".replace(",", "{,}"))], font_size=22)
        leg.to_corner(UL, buff=0.4)
        base = VGroup(label(r"unshifted test digits:", font_size=22, color=GREY_A),
                      MathTex(rf"{100 * ec.mean():.2f}\%", font_size=30, color=CNN),
                      MathTex(rf"{100 * em.mean():.2f}\%", font_size=30, color=MLPC)).arrange(RIGHT, buff=0.3)
        base.next_to(leg, RIGHT, buff=0.6)
        P = M["perm"]
        pe = int(M["perm_epochs"])
        bars = VGroup()
        vals = [np.mean(P["cnn_plain"]), np.mean(P["cnn"]), np.mean(P["mlp_plain"]), np.mean(P["mlp"])]
        cols = [CNN, CNN, MLPC, MLPC]
        vmax = max(vals)
        for i, (v, c) in enumerate(zip(vals, cols)):
            h = max(2.4 * v / vmax, 0.03)
            b = Rectangle(width=0.55, height=h, stroke_width=0, fill_color=c, fill_opacity=0.9 if i % 2 == 0 else 0.45)
            b.move_to([2.2 + 0.75 * i + (0.35 if i >= 2 else 0), -2.3 + h / 2, 0])
            t = MathTex(rf"{100 * v:.1f}\%", font_size=22, color=c).next_to(b, UP, buff=0.08)
            bars.add(VGroup(b, t))
        # under each bar, how the pixels were; under each pair, which network
        bl = VGroup(*[label(t, font_size=15, color=GREY_B).move_to([bars[i][0].get_x(), -2.5, 0])
                      for i, t in enumerate([r"in place", r"shuffled"] * 2)])
        bl.add(*[label(t, font_size=20, color=c).move_to([(bars[i][0].get_x() + bars[i + 1][0].get_x()) / 2, -2.85, 0])
                 for i, t, c in [(0, r"LeNet", CNN), (2, r"MLP", MLPC)]])
        pd = img_gray(np.asarray(M["perm_digit"]), 1.1).move_to([5.4, 1.75, 0])
        od = img_gray(np.asarray(M["digit"]), 1.1).next_to(pd, LEFT, buff=0.6)
        pa = Arrow(od.get_right(), pd.get_left(), buff=0.08, stroke_width=2.5, color=GREY_B)
        pt = label(rf"one fixed shuffle; \ retrained, \ ${pe}$ passes", font_size=18, color=GREY_B)
        pt.next_to(Group(od, pd), DOWN, buff=0.12)
        tag = note(r"computed: \ three seeds each, \ equal training").to_corner(DR, buff=0.2)
        gap1 = (sm[:, 3].mean() - sc[:, 3].mean())
        shifted_v = (f"Shift the test digits by three pixels and the network of fully connected units "
                     f"goes from {pct(em.mean())} to {pct(sm[:, 3].mean(), 0)} percent wrong; the convolutional "
                     f"one to {pct(sc[:, 3].mean(), 0)}." if gap1 > 0.05 else
                     f"Shift the test digits by three pixels and both suffer: {pct(sm[:, 3].mean(), 0)} and "
                     f"{pct(sc[:, 3].mean(), 0)} percent wrong.")
        hurt = np.mean(P["cnn"]) - np.mean(P["cnn_plain"])
        perm_v = (f"Shuffle the pixels, the same way in every image, and retrain both. The fully connected network "
                  f"doesn't care: {pct(np.mean(P['mlp_plain']))} percent before, {pct(np.mean(P['mlp']))} after, "
                  "because to it the pixels never had an order. The convolutional network falls from "
                  f"{pct(np.mean(P['cnn_plain']))} to {pct(np.mean(P['cnn']))}: its assumption, that nearby pixels "
                  "belong together, is now false." if hurt > 0.005 else
                  "Shuffle the pixels and retrain both: here the convolutional network loses little.")
        with self.voiceover(
            "Is it the convolution that helps, or just the training? Compare it fairly, with a fully connected "
            f"network of the same size, {M['params']['mlp']:,} weights against {M['params']['cnn']:,}, trained the "
            f"same way, three times each. <bookmark mark='a'/> On ordinary test digits: {pct(ec.mean(), 2)} "
            f"percent wrong for the convolutional network, {pct(em.mean(), 2)} for the other. "
            f"<bookmark mark='b'/> {shifted_v} Neither is perfectly shift-invariant: the fully connected "
            "layers at the top of LeNet see positions. <bookmark mark='c'/> And the cleanest test of the "
            f"assumption. {perm_v}"
        ) as vo:
            # first, large in the middle; then up into the corner when the plot arrives
            desc = VGroup(label(r"LeNet: \ convolution, pooling, convolution, pooling, \ three dense layers",
                                font_size=22, color=CNN),
                          label(r"MLP: \ $784$ pixels $\to$ $78$ hidden units $\to$ $10$", font_size=22, color=MLPC))
            desc.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            intro = VGroup(leg.copy(), base.copy()).arrange(DOWN, buff=0.5).scale(1.5).move_to(UP * 0.9)
            desc.next_to(intro, DOWN, buff=0.6)
            self.play(FadeIn(intro[0]), FadeIn(desc), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(intro[1]))
            vo.wait_until("b")
            self.play(ReplacementTransform(intro[0], leg), ReplacementTransform(intro[1], base), FadeOut(desc))
            self.play(Create(ax), FadeIn(cnn_c), FadeIn(mlp_c))
            vo.wait_until("c")
            self.play(FadeIn(od), GrowArrow(pa), FadeIn(pd), FadeIn(pt))
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars], lag_ratio=0.3), FadeIn(bl))
        self.wait(0.3)
        self.clear_scene()
