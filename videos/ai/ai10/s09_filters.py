from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (CNN, FMAP, HIST, KERNEL, PART, grid_of, img_filter, img_gray, img_rgb,
                                   load, nn_layer_boxes, pct)


def classes():
    return list(load("data")["cifar_classes"])


class Filters(VoiceoverScene):
    def construct(self):
        self.card()
        self.network()
        self.replay()
        self.hubel()
        self.deeper()

    def card(self):
        card = chapter_card(8, r"What the filters learn", r"What did the network invent on its own?", lit=(2012,),
                            part=PART)
        with self.voiceover("Chapter eight. What the filters learn."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def network(self):
        d, cf = load("data"), load("cifar")
        grid = np.asarray(d["cifar_grid"])  # (10, 8, 32, 32, 3)
        names = classes()
        rows = Group()
        for k in range(10):
            ims = Group(*[img_rgb(grid[k, i], 0.42) for i in range(8)]).arrange(RIGHT, buff=0.04)
            nm = data_text(names[k], font_size=16, color=GREY_A).next_to(ims, LEFT, buff=0.15)
            rows.add(Group(nm, ims))
        rows.arrange(DOWN, buff=0.05, aligned_edge=RIGHT).move_to([-3.4, -0.1, 0])
        if rows.height > 6.4:
            rows.height = 6.4
        dl = label(r"CIFAR-10 \ (Krizhevsky, 2009): \ $32 \times 32$ photographs, \ ten classes", font_size=22,
                   color=GREY_A).next_to(rows, UP, buff=0.15)
        boxes = nn_layer_boxes([0.18, 0.22, 0.28, 0.28, 0.12], [2.2, 1.6, 1.0, 0.6, 0.9],
                               [FMAP, FMAP, FMAP, FMAP, CNN], buff=0.35, depth=0.2).move_to([3.6, 1.9, 0])
        bl = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(b, DOWN, buff=0.12) for t, b in zip(
            [r"$48$ @ $7{\times}7$, \\ stride 2", r"$64$", r"$128$", r"$128$", r"$10$"], boxes)])
        bl.set_y(boxes.get_bottom()[1] - 0.4)
        ax = axes([0, int(cf["epochs"])], [0.3, 1.0], x_length=4.6, y_length=2.0,
                  xlabel=r"test accuracy, \ by passes over the photographs", ylabel=r"", xticks=[0, 5, 10], yticks=[0.5, 1.0], yfmt=lambda v: f"{int(100 * v)}\\%",
                  center=[3.6, -1.95, 0])
        t = np.asarray(cf["test"])
        per = int(cf["total_steps"]) / int(cf["epochs"])
        cur = curve(ax.ax, t[:, 0] / per, t[:, 1], CNN, 4)
        acc = float(cf["test_acc"])
        res = MathTex(rf"{100 * acc:.1f}\%", font_size=32, color=CNN).next_to(ax.ax.c2p(t[-1, 0] / per, t[-1, 1]), UP, buff=0.12)
        keep_in_frame(res)
        tag = note(rf"computed: \ ${cf['params']:,}$ weights, \ trained here in ${cf['seconds'] / 60:.0f}$ minutes"
                   .replace(",", "{,}")).to_corner(DR, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> CIFAR-10, "
            "collected by Krizhevsky in 2009: sixty thousand pictures of thirty-two by thirty-two pixels, in ten "
            "classes. <bookmark mark='b'/> Our network for it has an AlexNet-like first layer, 48 kernels of "
            "seven by seven pixels in colour, at a stride of two, then three more convolutional layers. "
            f"<bookmark mark='c'/> Trained on this computer for {cf['epochs']} passes over the fifty thousand "
            f"training photographs, it labels {pct(acc)} percent of the ten thousand test photographs correctly."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dl), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.2), FadeIn(bl))
            vo.wait_until("c")
            self.play(Create(ax), Create(cur), FadeIn(tag))
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        cf = load("cifar")
        steps = [int(s) for s in cf["steps"]]
        W = np.asarray(cf["w1"])  # (snaps, 48, 3, 7, 7)
        accs = np.asarray(cf["snap_acc"])
        cv = np.asarray(cf["curve"])

        def tiles(i):
            return grid_of([img_filter(w, 0.62) for w in W[i]], cols=8, buff=0.07).move_to([-2.6, -0.3, 0])

        cur = tiles(0)
        frame = SurroundingRectangle(cur, color=GREY_D, buff=0.12, stroke_width=1.2)
        ax = axes([0, steps[-1]], [0, 2.5], x_length=4.4, y_length=2.6, xlabel=r"training steps",
                  ylabel=r"training loss", xticks=[0, steps[-1]], yticks=[0, 1, 2], center=[4.2, 1.2, 0])
        A = ax.ax
        k = ValueTracker(0)
        sm = np.convolve(cv[:, 1], np.ones(10) / 10, mode="same")

        def path():
            s = steps[int(k.get_value())]
            n = max(2, int(np.searchsorted(cv[:, 0], s)))
            return VMobject(color=CNN, stroke_width=3).set_points_as_corners(
                [A.c2p(x, min(y, 2.5)) for x, y in zip(cv[:n, 0], sm[:n])])

        live = always_redraw(path)

        def readout():
            i = int(k.get_value())
            return VGroup(MathTex(rf"\text{{step }}{steps[i]:,}".replace(",", "{,}"), font_size=28),
                          MathTex(rf"{100 * accs[i]:.0f}\%\ \text{{right}}", font_size=28, color=CNN)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.0, -1.6, 0])

        clock = always_redraw(readout)
        hl = label(r"the $48$ first-layer kernels, \ as colours", font_size=22, color=KERNEL).next_to(frame, UP,
                                                                                                 buff=0.15)
        cite_ = cite(r"compare Krizhevsky, Sutskever \& Hinton (2012), \ Figure 3", corner=DR)
        mid = next((i for i, a in enumerate(accs) if a > 0.5), len(steps) // 2)
        o = load("orientation")
        no_, nc_ = int(o["n_oriented"]), int(o["n_colour"])
        if no_ >= 6 and nc_ >= 6:
            fin = ("By the end, some have become edge detectors, light against dark at one angle, and others blobs "
                   "of one colour against another. Krizhevsky's paper showed the same kinds of kernel for AlexNet's "
                   "96, and the same kinds of filter are found in the visual cortex.")
        elif no_ >= 6:
            fin = ("By the end, some have become edge detectors, light against dark at one angle. Krizhevsky's paper "
                   "showed the same kind of kernel for AlexNet, and the same kind of filter is found in the visual "
                   "cortex.")
        else:
            fin = ("By the end the patterns are smoother, but few are clean edges; AlexNet's 96 kernels, in "
                   "Krizhevsky's paper, trained far longer on far more photographs, are much cleaner.")
        with self.voiceover(
            "Now replay the training and watch the first layer. <bookmark mark='a'/> At the start, 48 patches of "
            f"noise, and {pct(accs[0], 0)} percent of the answers right: chance. <bookmark mark='b'/> Within "
            f"{steps[mid]:,} steps, more than half right, and the noise has begun to organize. "
            f"<bookmark mark='c'/> {fin}"
        ) as vo:
            self.play(FadeIn(cur), Create(frame), FadeIn(hl), Create(ax), FadeIn(cite_))
            self.add(live, clock)
            vo.wait_until("a")
            for i in range(1, len(steps)):
                if i == 1:
                    vo.wait_until("b")
                if i == mid + 1:
                    vo.wait_until("c")
                nxt = tiles(i)
                self.play(k.animate.set_value(i), FadeOut(cur), FadeIn(nxt), run_time=0.9)
                cur = nxt
        for m in (live, clock):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def polar(self, R, center, radius=1.0, color=KERNEL):
        R = np.asarray(R, float)
        R = R / max(R.max(), 1e-9)
        n = len(R)
        pts = []
        for j in range(2 * n + 1):
            # grating j has its wave vector at pi j / n in image coordinates (y down); draw the answer along its
            # stripes as they look on screen, so the shape lies the way the filter's own stripes do
            th = math.pi / 2 - math.pi * j / n
            r = radius * R[j % n]
            pts.append(np.asarray(center) + r * np.array([math.cos(th), math.sin(th), 0]))
        shape = Polygon(*pts[:-1], stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25)
        ring = Circle(radius=radius, stroke_color=GREY_D, stroke_width=1.2).move_to(center)
        axis = VGroup(Line(np.asarray(center) + LEFT * radius, np.asarray(center) + RIGHT * radius, color=GREY_D,
                           stroke_width=1), Line(np.asarray(center) + DOWN * radius, np.asarray(center) + UP * radius,
                                                 color=GREY_D, stroke_width=1))
        return VGroup(ring, axis, shape)

    def hubel(self):
        o = load("orientation")
        W = np.asarray(o["w1"])
        R, best = np.asarray(o["R"]), [int(b) for b in o["best"]][:3]
        # a grating, turning: the stimulus
        size = 2.2
        th = ValueTracker(0.0)

        def grating():
            yy, xx = np.mgrid[:48, :48] - 23.5
            a = th.get_value()
            u = xx * math.cos(a) + yy * math.sin(a)
            g = 0.5 + 0.5 * np.cos(2 * math.pi * u / 12)
            return img_gray(g, size, lo=0, hi=1, color=WHITE).move_to([-5.0, 1.2, 0])

        gr = always_redraw(grating)
        gl = label(r"the stimulus: \ a grating, \ turned", font_size=20, color=GREY_B).move_to([-5.0, -0.2, 0])
        triples = Group(*[Group(img_filter(W[b], 1.1), self.polar(R[b], ORIGIN, 0.95)).arrange(DOWN, buff=0.3)
                          for b in best]).arrange(RIGHT, buff=0.7).move_to([0.9, 0.6, 0])
        tl = label(r"three of our filters, \ and how strongly each answers at each angle", font_size=22,
                   color=KERNEL).next_to(triples, UP, buff=0.2)
        n, no, nc, no0 = int(o["n"]), int(o["n_oriented"]), int(o["n_colour"]), int(o["n_oriented0"])
        counts = VGroup(
            label(rf"trained: \ ${no}$ of ${n}$ strongly tuned to an angle; \ ${nc}$ mostly colour", font_size=24,
                  color=CNN),
            label(rf"the same filters before training: \ ${no0}$ of ${n}$ tuned", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        sel = label(rf"tuned: \ selectivity $\frac{{R_{{\text{{best}}}} - R_{{\perp}}}}{{R_{{\text{{best}}}} + "
                    rf"R_{{\perp}}}} \ge {o['selective']}$", font_size=20, color=GREY_B).to_corner(UR, buff=0.3)
        tag = note(r"computed").to_corner(DR, buff=0.25)
        if no0 == 0 and no > 3:
            verdict = "Before training, not one of them passes the same test. The tuning was learned."
        elif no > no0 + 3:
            verdict = f"Before training, only {no0} pass the same test, by chance; after, {no} do."
        else:
            verdict = f"Before training, {no0} pass the same test by chance; after, {no}."
        with self.voiceover(
            "We can run Hubel and Wiesel's experiment on our own network. <bookmark mark='a'/> Show each filter a "
            "striped pattern, a grating, at sixteen angles, and record how strongly it answers at each one. "
            "<bookmark mark='b'/> Here are three of the filters, and their answers drawn as a shape around a "
            "circle: a long thin shape means the filter cares about one angle and ignores the one at right angles "
            "to it, like the cat's cell. <bookmark mark='c'/> Count the filters whose answer at their best angle "
            f"is at least three times the answer at right angles: {no} of the {n}, and {nc} more respond mostly "
            f"to colour. {verdict}"
        ) as vo:
            self.add(gr)
            self.play(FadeIn(gl), FadeIn(sel), FadeIn(tag), FadeIn(tl), *[FadeIn(t[0]) for t in triples])
            vo.wait_until("a")
            self.play(th.animate.set_value(math.pi), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t[1], shift=UP * 0.1) for t in triples], lag_ratio=0.3))
            self.play(th.animate.set_value(2 * math.pi), run_time=2.5, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(counts, shift=UP * 0.1))
        gr.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def deeper(self):
        f = load("filters")
        P3 = np.asarray(f["patches3"])  # (12, 9, 21, 21, 3)
        I4 = np.asarray(f["imgs4"])  # (8, 6, 32, 32, 3)
        names = classes()
        left = Group()
        for c in range(6):
            left.add(Group(*[img_rgb(P3[c, i], 0.56) for i in range(6)]).arrange(RIGHT, buff=0.04))
        left.arrange(DOWN, buff=0.12).move_to([-3.5, -0.4, 0])
        ll = label(r"layer 3 \ ($21 \times 21$ pixels seen): \\ the patches that excite six channels most",
                   font_size=20, color=FMAP).next_to(left, UP, buff=0.2)
        right = Group()
        for c in range(4):
            ims = Group(*[img_rgb(I4[c, i], 0.62) for i in range(6)]).arrange(RIGHT, buff=0.05)
            cn = [names[k] for k in f["cls4"][c]]
            top = max(set(cn), key=cn.count)
            lab = data_text(f"{cn.count(top)}/6 {top}", font_size=16, color=GREY_A).next_to(ims, RIGHT, buff=0.12)
            right.add(Group(ims, lab))
        right.arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([3.4, -0.4, 0])
        rl = label(r"layer 4 \ (the whole photograph): \\ the images that excite four channels most", font_size=20,
                   color=CNN).next_to(right, UP, buff=0.2)
        cite_ = cite(r"Zeiler \& Fergus (2013)", corner=DL)
        tag = note(r"computed: \ our network, \ the $10{,}000$ test photographs").to_corner(DR, buff=0.2)
        zf = history_card(2013, r"Matthew Zeiler \& Rob Fergus, \ NYU",
                          r"\textit{Visualizing and Understanding Convolutional Networks}: \ to see what a deep unit "
                          r"wants, \ find the inputs that excite it most", width=7.0, color=HIST).move_to(UP * 0.3)
        purity = [max(f["cls4"][c].count(k) for k in set(f["cls4"][c])) for c in range(4)]
        with self.voiceover(
            "Higher layers combine the edges. To see what a deeper unit wants, the trick from Matthew Zeiler and "
            "Rob Fergus in 2013 is to find the inputs that excite it most. <bookmark mark='a'/> In our third "
            "layer, each unit sees twenty-one pixels square, and its favourite patches share a texture, a colour "
            "boundary, a curve or a corner. <bookmark mark='b'/> The fourth layer sees the whole photograph, and "
            "its favourite images begin to share a class: for these four channels, "
            f"{purity[0]}, {purity[1]}, {purity[2]} and {purity[3]} of the top six images are of one kind. Nobody "
            "labelled the channels. The labels only ever reached the very last layer."
        ) as vo:
            self.play(FadeIn(zf, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeOut(zf), FadeIn(cite_))
            self.play(FadeIn(ll), LaggedStart(*[FadeIn(r) for r in left], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(rl), LaggedStart(*[FadeIn(r) for r in right], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()


_ = (HIST, img_gray)
