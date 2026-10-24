from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import (CNN_C, HIST, PART, PATCH, VIT_C, fmt_int, glyph_sheet, load, mean_band, spread_bars,
                                   take_away)


def locality_picture() -> VGroup:
    """Inductive bias: a convolution's unit sees a 3 x 3 neighbourhood with the same weights everywhere; an attention
    head may look anywhere, with weights it computes."""
    cell = 0.22
    grid_a = VGroup(*[Square(cell, stroke_width=0.6, stroke_color=GREY_D) for _ in range(49)]).arrange_in_grid(7, 7, buff=0)
    grid_b = grid_a.copy()
    VGroup(grid_a, grid_b).arrange(RIGHT, buff=0.9)
    win = Square(3 * cell, stroke_color=CNN_C, stroke_width=3, fill_color=CNN_C, fill_opacity=0.25).move_to(grid_a[24])
    q = grid_b[24].copy().set_fill(VIT_C, 0.8)
    rays = VGroup(*[Line(grid_b[24].get_center(), grid_b[k].get_center(), color=VIT_C, stroke_width=1.5,
                         stroke_opacity=0.8) for k in (0, 6, 10, 30, 44, 48, 17)])
    la = label(r"convolution: \ nearby, \\ the same weights everywhere", font_size=16, color=CNN_C).next_to(grid_a, DOWN, buff=0.1)
    lb = label(r"attention: \ anywhere, \\ weights it computes", font_size=16, color=VIT_C).next_to(grid_b, DOWN, buff=0.1)
    return VGroup(grid_a, grid_b, win, rays, q, la, lb)


class Bias(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.bias()
        self.predict()
        self.experiment()

    def card(self):
        card = chapter_card(2, r"Convolutions or attention?", r"What does a vision transformer give up?", lit=(2012,), part=PART)
        with self.voiceover("Chapter two. Convolutions or attention?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        head = label(r"From AlexNet to the vision transformer", font_size=36).to_edge(UP, buff=0.35)
        cards = VGroup(
            history_card(2012, r"AlexNet; \ then VGG, \ ResNet", r"convolutions win ImageNet \ (Part 10)", color=HIST,
                         width=4.3, font_size=26),
            history_card(2018, r"non-local networks", r"attention added to convolutional networks", color=HIST, width=4.3,
                         font_size=26),
            history_card(2020, r"ViT \ (Dosovitskiy et al.)", r"pretrained on $300$ million images: \ $88.55\%$ on "
                         r"ImageNet; \ on ImageNet alone, \ a few points below ResNets", color=HIST, width=4.3, font_size=26),
            history_card(2021, r"DeiT; \ Swin", r"ImageNet only, \ $83.1\%$, \ in under $3$ days; \ local windows, \ "
                         r"a hierarchy", color=HIST, width=4.3, font_size=26),
            history_card(2022, r"ConvNeXt", r"a modernized convolutional network: \ $87.8\%$, \ level with Swin",
                         color=HIST, width=4.3, font_size=26),
            history_card(2023, r"ViT-22B; \ DINOv2", r"vision transformers at scale; \ self-supervised encoders \ (Part 24)",
                         color=HIST, width=4.3, font_size=26),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.45)).next_to(head, DOWN, buff=0.45)
        if cards.width > 13.3:
            cards.width = 13.3
        quote = label(r"``large scale training trumps inductive bias'' \ \textemdash\ Dosovitskiy et al.\ (2020)",
                      font_size=22, color=VIT_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "From 2012, convolutional networks ruled vision: AlexNet, then VGG and ResNet, Part 10's story. "
            "<bookmark mark='a'/> Attention crept in as an add-on. <bookmark mark='b'/> Then the 2020 vision "
            "transformer dropped convolutions altogether. Trained on ImageNet's million images alone, it fell a few "
            "points short of ResNets. Pretrained on three hundred million, it reached eighty-eight point five five "
            "percent. Their summary: large-scale training trumps inductive bias. <bookmark mark='c'/> Within months, "
            "DeiT trained one on ImageNet alone, with heavy augmentation and distillation, to eighty-three percent; "
            "Swin brought back local windows and a hierarchy. <bookmark mark='d'/> In 2022 ConvNeXt answered for "
            "convolutions, matching Swin. <bookmark mark='e'/> But at scale the transformers won: today's vision "
            "encoders, like DINOv2, are vision transformers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.1))
            self.play(FadeIn(quote))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(cards[4], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(cards[5], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bias(self):
        card = definition_card(r"Inductive bias",
                               r"an assumption built into a model before it sees any data. \ A convolution assumes "
                               r"\textit{locality}: \ a unit looks at a small neighbourhood; \ and \textit{translation "
                               r"equivariance}: \ the same weights at every place, \ so a shifted picture gives shifted "
                               r"features.", width=6.2, color=CNN_C)
        card.to_corner(UL, buff=0.4)
        pic = locality_picture().scale(1.55).move_to([3.4, 0.7, 0])
        pay = VGroup(label(r"right assumptions: \ fewer examples needed", font_size=28, color=CNN_C),
                     label(r"fewer assumptions: \ more to learn, \ more it can learn", font_size=28, color=VIT_C)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -2.7, 0])
        with self.voiceover(
            "What did the transformer give up? An inductive bias: an assumption built in before any data arrives. "
            "<bookmark mark='a'/> A convolution assumes locality, that a unit only needs a small neighbourhood, and "
            "that the same weights work at every place in the picture. <bookmark mark='b'/> Attention assumes "
            "neither: any patch may look at any other, with weights it computes on the spot. <bookmark mark='c'/> "
            "Right assumptions mean fewer examples are needed; fewer assumptions mean more to learn, but more it "
            "can learn. So which wins depends on how much data there is."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(pic[0]), FadeIn(pic[2]), FadeIn(pic[5]))
            vo.wait_until("b")
            self.play(FadeIn(pic[1]), FadeIn(pic[4]), LaggedStart(*[Create(r_) for r_ in pic[3]], lag_ratio=0.1),
                      FadeIn(pic[6]))
            vo.wait_until("c")
            self.play(FadeIn(pay[0]))
            self.play(FadeIn(pay[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def predict(self):
        d = load("vitcnn")
        sizes = [int(s) for s in d["sizes"]]
        card = pause_card(rf"A vision transformer and a convolutional network with the same number of weights learn "
                          rf"to name letters from {sizes[0]} fonts, \ or from all {sizes[-1]}. \ Which wins each time, "
                          r"and by how much?", width=8.6).move_to(UP * 0.6)
        card.to_edge(UP, buff=0.35)
        from videos.ai.ai22.base import dataset

        imgs, labels, test, n_fonts, font = dataset()
        train_fonts = np.unique(font[~test])
        chosen = np.sort(np.random.default_rng(100).permutation(train_fonts)[:sizes[0]])  # seed 0's choice
        cols_ = [0, 4, 6, 12, 17, 22]  # A E G M R W, the first of each letter's three copies

        def sheet(fonts_, size):
            ims = [imgs[(f * 26 + c) * 3] for f in fonts_ for c in cols_]
            return glyph_sheet(np.array(ims), len(fonts_), len(cols_), size=size, gap=0.03)

        setup = Group(Group(label(rf"{sizes[0]} training fonts", font_size=20, color=GREY_A), sheet(chosen, 0.32)).arrange(DOWN, buff=0.15),
                      Group(label(rf"all {sizes[-1]}", font_size=20, color=GREY_A), sheet(train_fonts, 0.16)).arrange(DOWN, buff=0.15),
                      Group(label(r"$4$ held-out fonts", font_size=20, color=C.SURPRISE),
                            sheet(np.unique(font[test]), 0.32)).arrange(DOWN, buff=0.15)
                      ).arrange(RIGHT, buff=1.0, aligned_edge=UP).next_to(card, DOWN, buff=0.45)
        with self.voiceover(
            "We can test that on our letters. Two models with the same number of weights, the same training steps, "
            "batches and augmentations; one a vision transformer, one a convolutional network. They learn from "
            f"{sizes[0]} fonts, or {sizes[1]}, or all {sizes[-1]}, and are tested on four fonts neither has seen. "
            "<bookmark mark='a'/> Pause and predict: which wins with little data, and does that change with more?"
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            self.play(LaggedStart(*[FadeIn(g_) for g_ in setup], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(card.box, color=C.ADVANTAGE, scale_factor=1.02))
        self.wait(2.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experiment(self):
        d = load("vitcnn")
        sizes = [int(s) for s in d["sizes"]]
        va, ca = np.asarray(d["vit_acc"]), np.asarray(d["cnn_acc"])  # (sizes, seeds)
        n_tr = [int(x) for x in d["n_train"]]
        head = label(rf"Same weights \ (ViT ${fmt_int(d['vit_params'])}$, \ CNN ${fmt_int(d['cnn_params'])}$), \ "
                     rf"same ${fmt_int(d['steps'])}$ steps of ${int(d['batch'])}$ letters, \ three seeds",
                     font_size=22, color=GREY_A).to_edge(UP, buff=0.3)
        bars = spread_bars([[ca[i], va[i]] for i in range(len(sizes))], [CNN_C, VIT_C], None, height=3.0, bar_w=0.55,
                           gap=0.12, group_gap=0.7, vmax=1.0, fmt=lambda x: rf"{100 * x:.0f}\%", font_size=18,
                           group_names=[rf"{s} fonts \ (${fmt_int(n)}$)" for s, n in zip(sizes, n_tr)])
        bars.move_to([-3.3, -0.2, 0])
        yl = label(r"right on the $4$ held-out fonts", font_size=20, color=GREY_A).next_to(bars, UP, buff=0.25)
        leg = legend([(CNN_C, r"convolutional network"), (VIT_C, r"vision transformer")], font_size=20)
        # the learning curves on the smallest set
        xs = np.asarray(d["curve_steps"], float)
        vc, cc_ = np.asarray(d["vit_curve"]), np.asarray(d["cnn_curve"])
        ax = axes([0, xs[-1]], [0, 1], x_length=4.6, y_length=2.6, xlabel=r"training step", ylabel=r"held-out accuracy",
                  xticks=[0, xs[-1]], yticks=[0, 0.5, 1], center=[3.6, 0.4, 0], font_size=18, xfmt=lambda x: fmt_int(x))
        cap = label(rf"learning, \ on {sizes[0]} fonts \ (band: \ three seeds)", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1)
        leg.next_to(ax, DOWN, buff=0.25)
        lines = VGroup(mean_band(ax.ax, xs, cc_[0], CNN_C), mean_band(ax.ax, xs, vc[0], VIT_C))
        gap = ca.mean(1) - va.mean(1)  # CNN minus ViT, per data size
        macs = (int(d["vit_macs"]), int(d["cnn_macs"]))
        if np.all(gap > 0.01) and gap[-1] < gap[0] - 0.02:
            verdict = (f"The convolutional network wins at every size, by {100 * gap[0]:.0f} points with {sizes[0]} "
                       f"fonts, and the gap narrows to {100 * gap[-1]:.0f} with all {sizes[-1]}: more data, less need "
                       "for the built-in assumptions.")
        elif np.all(gap > 0.01):
            verdict = (f"The convolutional network wins at every size, by {100 * gap[0]:.0f} points with {sizes[0]} "
                       f"fonts and {100 * gap[-1]:.0f} with all {sizes[-1]}: at this scale, the built-in assumptions "
                       "keep paying.")
        elif gap[0] > 0.01 and gap[-1] < -0.01:
            verdict = (f"With {sizes[0]} fonts the convolutional network wins by {100 * gap[0]:.0f} points; with all "
                       f"{sizes[-1]} the transformer passes it, by {-100 * gap[-1]:.0f}.")
        elif gap[0] > 0.01:
            verdict = (f"With {sizes[0]} fonts the convolutional network wins by {100 * gap[0]:.0f} points; with all "
                       f"{sizes[-1]} the transformer has caught up.")
        else:
            verdict = (f"Here the transformer holds its own even on {sizes[0]} fonts: the convolutional network's "
                       f"lead is {100 * gap[0]:.0f} points there and {100 * gap[-1]:.0f} with all {sizes[-1]}. Letters "
                       "this small don't need much locality.")
        ratio = macs[1] / macs[0]
        cost = (f"The convolution also spends {ratio:.1f} times the arithmetic per picture: its stencils run at every "
                "pixel." if ratio > 1.15 else
                f"The two spend about the same arithmetic per picture, {ratio:.1f} to 1.")
        tk = take_away(r"little data: \ build the assumptions in. \ \ A lot of data: \ let the model learn them.")
        with self.voiceover(
            "Here are the results, three seeds each: every dot is one training run. <bookmark mark='a'/> " + verdict + " <bookmark mark='b'/> " + cost + " <bookmark mark='c'/> The lesson of the last decade: with little data, build the "
            "assumptions in; with a lot, let the model learn them. Every generator in this part is a transformer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars.base), FadeIn(bars.gnames), FadeIn(yl), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.15) for g_ in bars.bars for b_ in g_], lag_ratio=0.15),
                      run_time=2.0)
            self.play(Create(ax), FadeIn(cap), *[Create(l_[1]) for l_ in lines], *[FadeIn(l_[0]) for l_ in lines],
                      run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(head, color=PATCH, scale_factor=1.02))
            vo.wait_until("c")
            self.play(FadeIn(tk, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
