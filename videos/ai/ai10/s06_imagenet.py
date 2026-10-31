from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (CNN, FMAP, HAND, HIST, KERNEL, PART, load, nn_layer_boxes)
from videos.ai.ai10.specs import ALEXNET_EXTRA, ILSVRC, ILSVRC_2012_SECOND, ILSVRC_SIZES


class ImageNet(VoiceoverScene):
    def construct(self):
        self.card()
        self.dataset()
        self.contest()
        self.anatomy()
        self.aftermath()

    def card(self):
        card = chapter_card(5, r"ImageNet and AlexNet", r"What happens when the data gets thousands of times bigger?",
                            lit=(2009, 2012), part=PART)
        with self.voiceover("Chapter five. ImageNet and AlexNet."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def dataset(self):
        hc = history_card(2009, r"Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li \& Fei-Fei Li",
                          r"ImageNet: \ pictures for the nouns of WordNet, \ gathered from the web, \ "
                          r"checked by people on Amazon Mechanical Turk", width=5.6, color=HIST).to_corner(UL, buff=0.4)
        n_tr = ILSVRC_SIZES["train"]
        sets = [("MNIST", 60_000, 28 * 28, GREY_B), ("CIFAR-10", 50_000, 32 * 32 * 3, FMAP),
                ("ImageNet (ILSVRC)", n_tr, 224 * 224 * 3, KERNEL)]
        vals = [n * p for _, n, p, _ in sets]
        top = math.log10(max(vals))
        lo = math.log10(min(vals)) - 1
        rows = VGroup()
        for k, ((nm, n, p, c), v) in enumerate(zip(sets, vals)):
            w = 6.0 * (math.log10(v) - lo) / (top - lo)
            b = Rectangle(width=w, height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([-0.6 + w / 2, -0.6 - 1.05 * k, 0])
            t = label(rf"{nm}: \ ${n:,}$ training images".replace(",", "{,}"), font_size=22, color=c)
            t.next_to(b, UP, buff=0.06).align_to(b, LEFT)
            e = int(math.floor(math.log10(v)))
            val = MathTex(rf"{v / 10 ** e:.1f} \times 10^{{{e}}}", font_size=26, color=c).next_to(b, RIGHT, buff=0.15)
            rows.add(VGroup(b, t, val))
        rl = label(r"numbers in the training set: \ images $\times$ pixel values (log scale)", font_size=22,
                   color=GREY_B).next_to(rows, DOWN, buff=0.3).align_to(rows, LEFT)
        facts = VGroup(label(rf"the contest: \ ${ILSVRC_SIZES['classes']:,}$ classes".replace(",", "{,}"),
                             font_size=24, color=WHITE),
                       label(rf"${ILSVRC_SIZES['val']:,}$ validation, \ ${ILSVRC_SIZES['test']:,}$ test images"
                             .replace(",", "{,}"), font_size=24, color=GREY_A),
                       label(r"top-5 error: \ wrong if the true class \\ is not among five guesses", font_size=24,
                             color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, 2.0, 0])
        cite_ = cite(r"Deng et al.\ (2009); \ Russakovsky et al.\ (2015)", corner=DR)
        ratio = vals[2] / vals[0]
        # a corner of WordNet's tree of nouns (levels skipped); the leaves are classes of the contest
        pos = {"entity": (0.2, 2.6), "animal": (-1.7, 1.5), "artifact": (2.0, 1.5), "dog": (-2.6, 0.4),
               "bird": (-0.2, 0.4), "vehicle": (2.0, 0.4), "Siberian husky": (-3.4, -0.7), "dalmatian": (-1.7, -0.7),
               "goldfinch": (-0.2, -0.7), "fire engine": (2.0, -0.7)}
        leaves = ("Siberian husky", "dalmatian", "goldfinch", "fire engine")
        nodes = {k: label(k, font_size=24, color=KERNEL if k in leaves else GREY_A).move_to([x, y, 0])
                 for k, (x, y) in pos.items()}
        edges = VGroup(*[Line(nodes[p_].get_bottom() + DOWN * 0.08, nodes[c_].get_top() + UP * 0.08,
                              stroke_width=1.6, color=GREY_C)
                         for p_, c_ in (("entity", "animal"), ("entity", "artifact"), ("animal", "dog"),
                                        ("animal", "bird"), ("artifact", "vehicle"), ("dog", "Siberian husky"),
                                        ("dog", "dalmatian"), ("bird", "goldfinch"), ("vehicle", "fire engine"))])
        tl = label(r"a corner of WordNet's tree of nouns, \\ many levels left out; \ in yellow, classes of the "
                   r"contest", font_size=20, color=GREY_B)
        tree = VGroup(edges, *nodes.values())
        tl.next_to(tree, DOWN, buff=0.3)
        tree = VGroup(tree, tl)
        if tree.width > 6.0:
            tree.width = 6.0
        tree.move_to([3.5, 0.6, 0])
        sch = note(r"schematic").to_corner(DL, buff=0.25)
        with self.voiceover(
            "In 2009 Fei-Fei Li, then at Princeton, and her students published ImageNet. <bookmark mark='a'/> The "
            "idea was to collect pictures for every noun in WordNet, a dictionary of English organized as a tree "
            "of meanings, searched for on the web and checked one by one by people paid through Amazon's "
            "Mechanical Turk. <bookmark mark='b'/> From 2010 a yearly contest used a thousand of its classes: "
            f"{n_tr:,} training photographs, with five guesses allowed per test image. <bookmark mark='c'/> "
            "Count the numbers a network has to learn from, images times pixel values, and ImageNet's contest is "
            f"about {ratio:,.0f} times MNIST: thousands of times bigger, and messier."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(nodes["entity"]), FadeIn(sch))
            self.play(LaggedStart(*[AnimationGroup(Create(e_), FadeIn(n_)) for e_, n_ in
                                    zip(edges, list(nodes.values())[1:])], lag_ratio=0.5), FadeIn(tl), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeOut(tree), FadeOut(sch))
            self.play(FadeIn(facts, shift=UP * 0.1), FadeIn(cite_))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.4), FadeIn(rl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def contest(self):
        data = [(f"{y}", t, e, HAND) for y, t, e, _ in ILSVRC[:2]]
        data += [("2012", ILSVRC_2012_SECOND[0] + r" \ (second)", ILSVRC_2012_SECOND[1], HAND),
                 ("2012", r"SuperVision", ILSVRC[2][2], CNN)]
        bars = VGroup()
        for k, (y, t, e, c) in enumerate(data):
            h = 4.4 * e / 30
            b = Rectangle(width=1.1, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([-5.2 + 1.7 * k, -2.3 + h / 2, 0])
            v = MathTex(rf"{e}\%", font_size=30, color=c).next_to(b, UP, buff=0.1)
            yl = MathTex(y, font_size=24, color=GREY_B).next_to(b, DOWN, buff=0.12)
            tl = label(t, font_size=18, color=GREY_A).next_to(yl, DOWN, buff=0.08)
            if tl.width > 1.6:
                tl.width = 1.6
            bars.add(VGroup(b, v, yl, tl))
        base = Line([-6.0, -2.3, 0], [0.4, -2.3, 0], color=GREY_C, stroke_width=1.5)
        bt = label(r"ILSVRC top-5 error", font_size=24, color=GREY_A).next_to(VGroup(bars, base), UP, buff=0.3)
        bt.align_to(base, LEFT)
        hc = history_card(2012, r"Alex Krizhevsky, Ilya Sutskever \& Geoffrey Hinton, \ Toronto",
                          rf"a deep convolutional network on two GPUs: \ ${ILSVRC[2][2]}\%$, \ ${ALEXNET_EXTRA}\%$ "
                          r"with extra training images", width=5.4, color=CNN).move_to([3.7, 1.4, 0])
        p17 = label(r"how two GTX 580 cards made it possible: \ Part 17", font_size=22, color=GREY_B)
        p17.next_to(hc, DOWN, buff=0.4)
        cite_ = cite(r"Russakovsky et al.\ (2015), \ Tables 5--7", corner=DR)
        with self.voiceover(
            f"The first two contests went to pipelines like the ones in Chapter 1: {ILSVRC[0][2]} percent top-5 "
            f"error in 2010, {ILSVRC[1][2]} in 2011. <bookmark mark='a'/> In 2012 the second-best entry, from the "
            f"University of Tokyo, used SIFT and other features and reached {ILSVRC_2012_SECOND[1]}. "
            "<bookmark mark='b'/> The winner, entered as SuperVision by Alex Krizhevsky, Ilya Sutskever and "
            f"Geoffrey Hinton, reached {ILSVRC[2][2]} percent, and {ALEXNET_EXTRA} with extra training images. "
            "Almost ten points better than the next entry, in a contest where a year's progress had been a point or "
            "two. <bookmark mark='c'/> The network "
            "became known as AlexNet. Part 17 will explain how it was trained, on two gaming graphics cards; here, what "
            "was inside."
        ) as vo:
            self.play(Create(base), FadeIn(bt), FadeIn(bars[0], shift=UP * 0.1), FadeIn(bars[1], shift=UP * 0.1),
                      FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(bars[2], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[3][0], DOWN), FadeIn(bars[3][1:]), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(p17))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def anatomy(self):
        a = load("alexnet")
        rows = a["alexnet"]
        S = a["alexnet_sum"]
        names = [r[0] for r in rows]
        params = np.array([r[1] for r in rows], float)
        macs = np.array([r[2] for r in rows], float)

        def chart(vals, x0, color_conv, color_fc, title, unit, scale):
            g = VGroup()
            vmax = vals.max()
            for k, (nm, v) in enumerate(zip(names, vals)):
                w = max(3.6 * v / vmax, 0.02)
                c = color_conv if nm.startswith("conv") else color_fc
                b = Rectangle(width=w, height=0.38, stroke_width=0, fill_color=c, fill_opacity=0.85)
                b.move_to([x0 + w / 2, 1.9 - 0.55 * k, 0])
                t = MathTex(rf"\text{{{nm}}}", font_size=22, color=GREY_A).next_to([x0, b.get_y(), 0], LEFT,
                                                                                    buff=0.15)
                val = MathTex(f"{v / scale:.2f}" if v / scale < 0.95 else f"{v / scale:.1f}", font_size=22,
                              color=c).next_to(b, RIGHT, buff=0.1)
                g.add(VGroup(b, t, val))
            head = label(title, font_size=24, color=WHITE).move_to([x0 + 1.6, 2.6, 0])
            ul = label(unit, font_size=18, color=GREY_B).next_to(g, DOWN, buff=0.2).align_to(g, LEFT)
            return VGroup(head, g, ul)

        left = chart(params, -5.3, FMAP, KERNEL, r"weights", r"millions", 1e6)
        right = chart(macs, 1.6, FMAP, KERNEL, r"multiply-adds per image", r"millions", 1e6)
        tot = VGroup(label(rf"total: \ ${S['params']:,}$ weights".replace(",", "{,}"), font_size=24, color=WHITE),
                     label(rf"total: \ ${S['macs'] / 1e6:,.0f}$ million multiply-adds".replace(",", "{,}"),
                           font_size=24, color=WHITE))
        tot[0].next_to(left, DOWN, buff=0.3).align_to(left[1], LEFT)
        tot[1].next_to(right, DOWN, buff=0.3).align_to(right[1], LEFT)
        key = VGroup(VGroup(Square(0.22, stroke_width=0, fill_color=FMAP, fill_opacity=0.85),
                            label(r"convolutional", font_size=20, color=FMAP)).arrange(RIGHT, buff=0.12),
                     VGroup(Square(0.22, stroke_width=0, fill_color=KERNEL, fill_opacity=0.85),
                            label(r"fully connected", font_size=20, color=KERNEL)).arrange(RIGHT, buff=0.12))
        key.arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.35)
        tag = note(r"computed from the published architecture").to_corner(DR, buff=0.25)
        pc, mc = S["conv_param_share"], S["conv_mac_share"]
        # the layer list, drawn (sizes not to scale)
        arch = nn_layer_boxes([0.15, 0.2, 0.26, 0.3, 0.3, 0.26, 0.12, 0.12, 0.1], [2.6, 2.0, 1.4, 1.0, 1.0, 1.0, 2.3,
                              2.3, 1.4], [GREY_B] + [FMAP] * 5 + [KERNEL] * 3, buff=0.45, depth=0.2).move_to([0, 0.5, 0])
        anames = [r"input \\ $224{\times}224{\times}3$", r"conv1 \\ $96$ @ $11{\times}11$, \\ stride $4$",
                  r"conv2 \\ $256$ @ $5{\times}5$", r"conv3 \\ $384$", r"conv4 \\ $384$", r"conv5 \\ $256$",
                  r"fc6 \\ $4096$", r"fc7 \\ $4096$", r"fc8 \\ $1000$, softmax"]
        alabs = VGroup(*[label(t, font_size=16, color=GREY_A).next_to(b, DOWN if k % 2 == 0 else UP, buff=0.2)
                         for k, (t, b) in enumerate(zip(anames, arch))])
        diagram = VGroup(arch, alabs)
        diagram.scale(min(12.0 / diagram.width, 5.6 / diagram.height)).move_to([0, 0.3, 0])
        keep_in_frame(diagram)
        sch = note(r"schematic: \ sizes not to scale").to_corner(DL, buff=0.25)
        with self.voiceover(
            "AlexNet was LeNet's design, grown. Five convolutional layers, the first with 96 kernels of eleven by "
            "eleven pixels at a stride of four, then three fully connected layers, ending in a thousand-way "
            f"softmax. <bookmark mark='a'/> Count its weights from the published layer list: {S['params']:,}. "
            f"Only {100 * pc:.0f} percent of them are in the convolutions; the first fully connected layer alone "
            f"holds {params[5] / 1e6:.0f} million. <bookmark mark='b'/> Now count the arithmetic, per image: "
            f"{S['macs'] / 1e6:,.0f} million multiply-adds, and {100 * mc:.0f} percent of those are in the "
            "convolutions, because each of their few weights is used at every position. <bookmark mark='c'/> "
            "Weights live in the dense layers, work in the convolutions: that split comes back in every network "
            "after it."
        ) as vo:
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b_), FadeIn(l_)) for b_, l_ in zip(arch, alabs)],
                                  lag_ratio=0.35), FadeIn(sch), run_time=5.0)
            vo.wait_until("a")
            self.play(FadeOut(diagram), FadeOut(sch))
            self.play(FadeIn(key), FadeIn(tag))
            self.play(FadeIn(left[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in left[1]], lag_ratio=0.1),
                      FadeIn(left[2]), FadeIn(tot[0]))
            vo.wait_until("b")
            self.play(FadeIn(right[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in right[1]],
                                                    lag_ratio=0.1), FadeIn(right[2]), FadeIn(tot[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def aftermath(self):
        cards = VGroup(
            history_card(2011, r"Dan Cire\c{s}an, Ueli Meier, Jonathan Masci \& J\"urgen Schmidhuber",
                         r"GPU-trained convolutional networks win a traffic-sign contest: \ $99.46\%$ right, \ "
                         r"people averaged $98.84\%$", width=6.2, color=HIST),
            history_card(2012, r"Hinton, Deng, Yu, Dahl, Mohamed, Jaitly, Senior, Vanhoucke, Nguyen, Sainath \& "
                         r"Kingsbury", r"four research groups: \ deep networks beat the old acoustic models in "
                         r"speech recognition", width=6.2, color=HIST),
            history_card(2013, r"ILSVRC 2013", r"almost every team used a convolutional network", width=6.2,
                         color=CNN),
            history_card(2018, r"Turing Award (announced 2019)", r"Yoshua Bengio, Geoffrey Hinton \& Yann LeCun",
                         width=6.2, color=HIST),
        )
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.4)).move_to(DOWN * 0.2)
        if cards.width > 13.4:
            cards.width = 13.4
        head = label(r"AlexNet was a turn, \ not a bolt from the blue", font_size=34).to_edge(UP, buff=0.4)
        cite_ = cite(r"Cire\c{s}an et al.\ (2012); \ Hinton et al.\ (2012); \ Russakovsky et al.\ (2015); \ ACM",
                     corner=DR)
        with self.voiceover(
            "AlexNet didn't come from nowhere. <bookmark mark='a'/> In 2011 Dan Ciresan and colleagues in Jurgen "
            "Schmidhuber's lab had already won contests with convolutional networks on GPUs, beating the average "
            "human tester on traffic signs. <bookmark mark='b'/> In 2012 groups at Toronto, Microsoft, Google and "
            "IBM reported together that deep networks beat the old models of speech. <bookmark mark='c'/> But "
            "ImageNet was the benchmark vision cared about, and the field turned at once: in 2013 nearly every "
            "team entered a convolutional network. <bookmark mark='d'/> Bengio, Hinton and LeCun later shared the "
            "Turing Award for 2018."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            ghosts = cards.copy().set_opacity(0.25)
            self.play(FadeIn(ghosts))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeOut(ghosts[k]), FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
