from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (DINO_C, HIST, JEPA, MAE_C, PART, PIX, POS, RAND, ROT, SIMCLR, SUP, arrow, digit,
                                   digit_sheet, load, node_box, pct, take_away)


class Problem(VoiceoverScene):
    def construct(self):
        self.card()
        self.labels()
        self.define()
        self.history()
        self.judge()
        self.bench()

    def card(self):
        card = chapter_card(1, r"Learning without labels", r"Where do representations come from \\ when nobody labels "
                            r"the data?", lit=(2009, 2012), part=PART)
        with self.voiceover("Chapter one. Learning without labels."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def labels(self):
        # images, on a log scale: what was labelled by hand, and what self-supervised models now train on
        rows = [(r"MNIST, \ labelled (1998)", 6e4, SUP), (r"ImageNet-1k, \ labelled (2009)", 1.28e6, SUP),
                (r"DINOv2's curated set (2023)", 1.42e8, DINO_C), (r"DINOv3's curated set (2025)", 1.689e9, DINO_C),
                (r"DINOv3's raw pool", 1.7e10, PIX)]
        x0, W = -1.2, 6.3
        lo, hi = 4, 10.5
        X = lambda v: x0 + W * (math.log10(v) - lo) / (hi - lo)  # noqa: E731
        bars = VGroup()
        for i, (nm, v, col) in enumerate(rows):
            y = 1.6 - 0.75 * i
            b = Rectangle(width=X(v) - x0, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.8)
            b.move_to([x0 + (X(v) - x0) / 2, y, 0])
            n = label(nm, font_size=22, color=GREY_A).next_to([x0, y, 0], LEFT, buff=0.2)
            val = MathTex(sci(v, 2 if v < 1e9 else 1).replace(r"\times", r"\!\times\!"), font_size=26, color=col)
            val.next_to(b, RIGHT, buff=0.15)
            bars.add(VGroup(b, n, val))
        ticks = VGroup()
        for e in range(lo, 11, 2):
            ticks.add(MathTex(rf"10^{{{e}}}", font_size=22, color=GREY_B).move_to([X(10 ** e), -2.25, 0]))
        axis = Line([x0, -1.95, 0], [x0 + W, -1.95, 0], color=GREY_C, stroke_width=1.5)
        unit = label(r"images", font_size=22, color=GREY_B).next_to(axis, RIGHT, buff=0.2)
        head = label(r"Labels cost people's time; \ pictures don't", font_size=36).to_edge(UP, buff=0.4)
        src = cite(r"Deng et al.\ (2009); \ Oquab et al.\ (2023); \ Sim\'eoni et al.\ (2025)", corner=DR)
        with self.voiceover(
            "For thirty years, a network learned to see by being told. MNIST, the digits we use in this part, came "
            "with sixty thousand labels; <bookmark mark='a'/> ImageNet with more than a million, each one checked by people. "
            "<bookmark mark='b'/> But pictures without labels are nearly free. DINOv2, in 2023, trained on a hundred "
            "and forty-two million unlabelled images; <bookmark mark='c'/> DINOv3, in 2025, on one point seven "
            "billion, chosen from a pool of about seventeen billion. <bookmark mark='d'/> Nobody will ever label "
            "those. The question is how to learn from them anyway."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks), FadeIn(unit), FadeIn(src))
            self.play(GrowFromEdge(bars[0][0], LEFT), FadeIn(bars[0][1:]))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[1][0], LEFT), FadeIn(bars[1][1:]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[2][0], LEFT), FadeIn(bars[2][1:]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[3][0], LEFT), FadeIn(bars[3][1:]))
            self.play(GrowFromEdge(bars[4][0], LEFT), FadeIn(bars[4][1:]))
            vo.wait_until("d")
            self.play(Indicate(bars[4][0], color=PIX, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def define(self):
        cake = VGroup()
        layers = [(r"predict any part of the input \\ from any other part", 1.5, SIMCLR),
                  (r"supervised: \ a label", 0.55, SUP), (r"reinforcement: \ a reward", 0.35, C.REWARD)]
        y = -2.3
        widths = [4.6, 4.6, 0.9]
        for (t, h, col), w in zip(layers, widths):
            if w < 1:
                c_ = Circle(radius=0.32, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([-3.6, y + 0.32, 0])
                lab = label(t, font_size=20, color=col).next_to(c_, RIGHT, buff=0.3)
                cake.add(VGroup(c_, lab))
                y += 0.64
            else:
                r_ = Rectangle(width=w, height=h, stroke_width=1.5, stroke_color=col, fill_color=col,
                               fill_opacity=0.25).move_to([-3.6, y + h / 2, 0])
                lab = label(t, font_size=20, color=WHITE).move_to(r_)
                cake.add(VGroup(r_, lab))
                y += h
        cake_c = cite(r"after LeCun's cake, \ NIPS 2016 keynote; \ schematic", corner=DL)
        d = definition_card(r"self-supervised learning",
                            r"a training signal made from the data itself: \ hide part of an input, \ or change it, "
                            r"\ or pair it with another, \ and ask the network to recover what was hidden \ or "
                            r"which goes with which. \ The product is the network's internal vector "
                            r"$h = f(x)$, \ its \textbf{representation}.", width=6.6, font_size=23)
        d.move_to([3.2, 1.0, 0])
        why_ = label(r"no one writes the answers: \ the data does", font_size=24, color=POS)
        why_.next_to(d, DOWN, buff=0.4).align_to(d, LEFT)
        with self.voiceover(
            "In 2016 Yann LeCun drew intelligence as a cake. <bookmark mark='a'/> Supervised learning, from labels, "
            "is the icing; reinforcement learning, from rewards, is the cherry on top. <bookmark mark='b'/> The "
            "cake itself is learning to predict any part of the input from any other part: there is far more "
            "information in a picture than in its label. <bookmark mark='c'/> He later gave the cake its current "
            "name: self-supervised learning. Hide part of an input, or change it, or pair it with another, and ask "
            "the network to recover what was hidden, or which goes with which. <bookmark mark='d'/> Nobody writes "
            "the answers; the data does. What we keep is not the answer but the network's internal vector, its "
            "representation."
        ) as vo:
            self.play(FadeIn(cake[0]), FadeIn(cake_c))
            vo.wait_until("a")
            self.play(FadeIn(cake[1], shift=DOWN * 0.1))
            self.play(FadeIn(cake[2], shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(Indicate(cake[0], color=SIMCLR, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(d, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(why_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        events = [
            (1961, r"Barlow: \\ redundancy \\ reduction", HIST),
            (1992, r"Becker \& Hinton: \\ modules that \\ must agree", SIMCLR),
            (1993, r"Siamese \\ networks", SIMCLR),
            (2006, r"a contrastive \\ loss (DrLIM)", SIMCLR),
            (2008, r"denoising \\ autoencoders", MAE_C),
            (2010, r"noise-contrastive \\ estimation", SIMCLR),
            (2013, r"word2vec's \\ negatives", SIMCLR),
            (2015, r"pretext \\ puzzles", ROT),
            (2018, r"CPC and \\ InfoNCE", SIMCLR),
            (2020, r"MoCo, SimCLR, \\ BYOL", SIMCLR),
            (2021, r"DINO, MAE, \\ CLIP", DINO_C),
            (2023, r"I-JEPA, \\ DINOv2", JEPA),
            (2025, r"DINOv3, \\ V-JEPA 2", DINO_C),
            (2026, r"V-JEPA 2.1; \\ one space, \\ every sense", JEPA),
        ]
        y0 = -0.2

        def X(yr):  # a broken axis: 1958-2004 squeezed on the left
            if yr < 2004:
                return -6.5 + 3.4 * (yr - 1958) / (2004 - 1958)
            return -2.6 + 9.0 * (yr - 2004) / (2027 - 2004)

        line = VGroup(Line([X(1958), y0, 0], [X(2003) + 0.05, y0, 0], color=GREY_C, stroke_width=2),
                      Line([X(2004) - 0.05, y0, 0], [X(2027), y0, 0], color=GREY_C, stroke_width=2))
        brk = VGroup(*[Line([x - 0.06, y0 - 0.12, 0], [x + 0.06, y0 + 0.12, 0], color=GREY_C, stroke_width=2)
                       for x in (X(2003) + 0.12, X(2004) - 0.12)])
        items = VGroup()
        for k, (yr, txt, col) in enumerate(events):
            dot = Dot([X(yr), y0, 0], radius=0.07, color=col)
            grp = VGroup(label(str(yr), font_size=19, color=col), label(txt, font_size=16, color=WHITE)).arrange(
                DOWN, buff=0.05)
            up = k % 2 == 0
            grp.next_to(dot, UP if up else DOWN, buff=0.3)
            items.add(VGroup(dot, Line(), grp))
        for side in (0, 1):
            same = [items[k] for k in range(len(items)) if k % 2 == side]
            for a, b in zip(same, same[1:]):
                gap = b[2].get_left()[0] - a[2].get_right()[0]
                if gap < 0.1:
                    b[2].shift(RIGHT * (0.1 - gap))
            over = same[-1][2].get_right()[0] - 6.9
            if over > 0:
                for it in same:
                    it[2].shift(LEFT * over * (1 if it is same[-1] else 0))
                for i in range(len(same) - 2, -1, -1):
                    gap = same[i + 1][2].get_left()[0] - same[i][2].get_right()[0]
                    if gap < 0.1:
                        same[i][2].shift(LEFT * (0.1 - gap))
        for it in items:
            dot, _, grp = it
            end = [grp.get_x(), grp.get_bottom()[1] if grp.get_y() > y0 else grp.get_top()[1], 0]
            it[1].become(Line(dot.get_center(), end, color=dot.get_color(), stroke_width=1.2))
        head = label(r"How we got here", font_size=36).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How we got here. In 1961 the neuroscientist Horace Barlow proposed that the senses recode what they "
            "receive to remove its redundancy. <bookmark mark='a'/> In 1992 Sue Becker and Geoffrey Hinton trained "
            "two small networks that looked at neighbouring parts of an image to agree with each other, and they "
            "discovered depth. <bookmark mark='b'/> Siamese networks for signatures followed, then a contrastive "
            "loss that pulls similar pairs together and pushes others apart. <bookmark mark='c'/> Denoising "
            "autoencoders hid part of the input; noise-contrastive estimation and word2vec learned by telling real "
            "data from noise. <bookmark mark='d'/> Around 2015 came pretext puzzles, and in 2018 the InfoNCE loss. "
            "<bookmark mark='e'/> Between 2019 and 2021, MoCo, SimCLR, BYOL, DINO and MAE closed the gap to "
            "supervised training. <bookmark mark='f'/> Since then: prediction in representation space, and models "
            "trained on billions of images and on video."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(brk))
            groups = [[0], [1], [2, 3], [4, 5, 6], [7, 8], [9, 10], [11, 12, 13]]
            for k, mk in enumerate([None, "a", "b", "c", "d", "e", "f"]):
                if mk:
                    vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(items[i], shift=UP * 0.1) for i in groups[k]], lag_ratio=0.3),
                          run_time=0.8 + 0.3 * len(groups[k]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def judge(self):
        v = load("views")
        d0 = np.asarray(v["orig"])[7]
        img = digit(d0, 1.3, frame=True).move_to([-5.4, 0.6, 0])
        enc = node_box(r"encoder $f$", SIMCLR, font_size=26, height=1.0).move_to([-3.1, 0.6, 0])
        lock = label(r"frozen", font_size=20, color=GREY_B).next_to(enc, UP, buff=0.12)
        h = VGroup(*[Square(0.2, stroke_width=1, stroke_color=SIMCLR, fill_color=SIMCLR,
                            fill_opacity=float(o)) for o in np.random.default_rng(3).uniform(0.1, 0.9, 8)])
        h.arrange(DOWN, buff=0.03).move_to([-1.3, 0.6, 0])
        hl = MathTex(r"h", font_size=34, color=SIMCLR).next_to(h, UP, buff=0.15)
        a1, a2 = arrow(img.get_right(), enc.get_left()), arrow(enc.get_right(), h.get_left())
        tests = VGroup(
            node_box(r"linear probe: \ a linear classifier \ from all $60{,}000$ labels", C.BITS, font_size=21),
            node_box(r"$k$-NN: \ the vote of the $20$ nearest \ training digits", POS, font_size=21),
            node_box(r"few labels: \ a linear classifier \ from $10$ labels per digit", C.MODEL_Q, font_size=21),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.6, 0.6, 0])
        arrs = VGroup(*[arrow(h.get_right(), t.get_left(), color=GREY_C, stroke_width=2) for t in tests])
        head = label(r"How to judge a representation", font_size=34).to_edge(UP, buff=0.4)
        cites = cite(r"Alain \& Bengio (2016); \ Wu et al.\ (2018); \ the linear protocol: \ Zhang, Isola \& Efros "
                     r"(2016)")
        with self.voiceover(
            "How do you judge a representation, when the whole point was not to use labels? You freeze the "
            "network, <bookmark mark='a'/> and ask how easily its vectors can be read. <bookmark mark='b'/> A linear "
            "probe: train only a linear classifier on top, with all the labels. If the digits are separated by "
            "flat walls in this space, the network has done the work. <bookmark mark='c'/> A nearest-neighbour "
            "vote: no training at all, just ask the twenty closest training digits. <bookmark mark='d'/> And the "
            "test that matters most in practice: a linear classifier from only ten labelled examples of each "
            "digit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(img), GrowArrow(a1), FadeIn(enc), FadeIn(cites))
            vo.wait_until("a")
            self.play(FadeIn(lock), GrowArrow(a2), FadeIn(h), FadeIn(hl))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(arrs[k]), FadeIn(tests[k], shift=LEFT * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bench(self):
        b = load("baselines")
        sup = load("supervised")
        v = load("views")
        px = b["pixels"]
        rc = b["random_cnn"]
        ss = sup["summary"]["cnn"]
        names = [r"raw pixels", r"untrained network", r"supervised network"]
        cols = [PIX, RAND, SUP]
        lin = [px["linear"], np.mean([r["linear"] for r in rc]), ss["linear"][0]]
        knn = [px["knn"], np.mean([r["knn"] for r in rc]), ss["knn"][0]]
        few = [np.mean(px["few"]), np.mean([np.mean(r["few"]) for r in rc]), ss["few"][0]]
        hdr = VGroup(*[label(t, font_size=22, color=GREY_A) for t in (r"", r"linear probe", r"$k$-NN",
                                                                    r"10 labels per digit")])
        xs = [-3.6, 0.4, 2.7, 5.2]
        rows = VGroup()
        for i in range(3):
            r_ = VGroup(label(names[i], font_size=26, color=cols[i]),
                        MathTex(pct(lin[i]) + r"\%", font_size=32), MathTex(pct(knn[i]) + r"\%", font_size=32),
                        MathTex(pct(few[i]) + r"\%", font_size=32, color=C.MODEL_Q))
            rows.add(r_)
        tab = VGroup(hdr, *rows)
        for k, r_ in enumerate(tab):
            for j, m in enumerate(r_):
                m.move_to([xs[j], -0.6 - 0.75 * k, 0])
        rule = Line([-5.8, -0.95, 0], [6.6, -0.95, 0], color=GREY_D, stroke_width=1.2)
        grid = digit_sheet(np.asarray(v["grid"])[:24], 2, 12, size=0.62, gap=0.06).move_to([0, 2.3, 0])
        facts = label(rf"MNIST: \ ${v['n_train']:,}$ training digits, \ ${v['n_test']:,}$ test; \ every method: the "
                      rf"same small network, \ ${v['steps']}$ updates of ${v['batch']}$ digits $\times$ 2 views, \ "
                      r"three seeds".replace(",", "{,}"), font_size=21, color=GREY_A).next_to(grid, DOWN, buff=0.2)
        gap_few = few[2] - few[0]
        verdict = (f"Raw pixels already score {pct(knn[0], 1)} percent by nearest neighbours: MNIST is easy that way. "
                   f"The hard test is ten labels per digit, where pixels manage {pct(few[0], 0)} percent and the "
                   f"supervised network, which saw all sixty thousand labels, {pct(few[2], 0)}."
                   if knn[0] > 0.9 else
                   f"With ten labels per digit, pixels manage {pct(few[0], 0)} percent and the supervised network "
                   f"{pct(few[2], 0)}.")
        with self.voiceover(
            "Our test bench is MNIST: sixty thousand handwritten digits to learn from, ten thousand to test on. "
            f"<bookmark mark='a'/> Every method gets the same small network, the same {v['steps']} updates and "
            "the same views, from three random starts. <bookmark mark='b'/> Three yardsticks first. The raw pixels; "
            f"an untrained network; and the same network trained with every label. <bookmark mark='c'/> {verdict} "
            "A self-supervised method sits somewhere between the untrained network and the one that was told."
        ) as vo:
            self.play(FadeIn(grid))
            vo.wait_until("a")
            self.play(FadeIn(facts))
            vo.wait_until("b")
            self.play(FadeIn(hdr), Create(rule))
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in rows], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(VGroup(*[r_[3] for r_ in rows]), color=C.MODEL_Q, scale_factor=1.08))
        self.wait(0.3)
        self.clear_scene()
