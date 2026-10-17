from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import HINGE, NEURON, curve, load, patch_image


class Depth(VoiceoverScene):
    def construct(self):
        self.card()
        self.folding()
        self.random_nets()

    def card(self):
        card = chapter_card(2, r"What depth adds", r"Why stack layers at all?", part=8)
        with self.voiceover("Chapter two. What depth adds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def folding(self):
        s = load("sawtooth")
        xs = np.asarray(s["xs"])
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=6.2, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.6, -0.6, 0])
        ident = curve(ax, xs, xs, GREY_B, 3)
        teeth = [curve(ax, xs, np.asarray(s[f"tent{k}"]), HINGE, 4) for k in range(1, 6)]
        colors = {r"t(x)": HINGE}
        f = cmath(r"t(x)", "=", r"2\max(0, x) - 4\max(0,\, x - \tfrac12)", colors=colors, font_size=34)
        f.to_edge(UP, buff=0.4).shift(LEFT * 2.6)
        fl = label(r"one layer of $2$ units: \ a tent", font_size=26, color=GREY_A).next_to(f, DOWN, buff=0.15)
        kv = Integer(1, font_size=40, color=HINGE)
        kl = VGroup(label(r"layers:", font_size=30), kv).arrange(RIGHT, buff=0.2).move_to([0, 1.6, 0]).align_to([1.6, 0, 0], LEFT)
        pv = Integer(2, font_size=40, color=C.BITS)
        pl = VGroup(label(r"straight pieces:", font_size=30), pv).arrange(RIGHT, buff=0.2).next_to(kl, DOWN, buff=0.3)
        pl.align_to(kl, LEFT)
        rule = label(r"$k$ layers, \ $2k$ units: \ $2^k$ pieces; \\ one layer would need $2^k$ units", font_size=28,
                     color=C.BITS).next_to(pl, DOWN, buff=0.6).align_to(kl, LEFT)
        cite_ = cite(r"M.~Telgarsky, \textit{Benefits of Depth in Neural Networks} (2016)", corner=DR)
        with self.voiceover(
            "If one layer can do anything, why stack them? Here's the answer in one picture. Two units make a tent: "
            "up from zero to one, and back down. <bookmark mark='a'/> Feed the tent into another tent: the line is "
            "folded twice, and you get four pieces. <bookmark mark='b'/> Three layers, eight pieces. Five layers, "
            "thirty-two. Each layer doubles the pieces, while a single layer would need a unit for every piece. "
            "Depth can buy complexity exponentially cheaply."
        ) as vo:
            self.play(Create(ax), Create(ident), Write(f), FadeIn(fl), FadeIn(cite_))
            self.play(Transform(ident, teeth[0]), FadeIn(kl), FadeIn(pl))
            vo.wait_until("a")
            self.play(Transform(ident, teeth[1]), ChangeDecimalToValue(kv, 2), ChangeDecimalToValue(pv, 4))
            vo.wait_until("b")
            for k in (3, 4, 5):
                self.play(Transform(ident, teeth[k - 1]), ChangeDecimalToValue(kv, k), ChangeDecimalToValue(pv, 2 ** k),
                          run_time=1.0)
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def random_nets(self):
        s = load("sawtooth")
        depths, counts = [int(d) for d in s["depths"]], np.asarray(s["counts"])
        tiles = Group()
        for d, cnt in zip(depths, counts):
            img = patch_image(s[f"map{d}"], 2.3, 2.3, seed=d)
            cap = label(rf"${d}$ layer{'s' if d > 1 else ''} of ${48 // d}$", font_size=22, color=NEURON)
            num = label(rf"$\approx {cnt:.0f}$ pieces", font_size=22, color=WHITE)
            tiles.add(Group(img, VGroup(cap, num).arrange(DOWN, buff=0.06).next_to(img, DOWN, buff=0.12)))
        tiles.arrange(RIGHT, buff=0.3).move_to(UP * 0.2)
        head = label(r"$48$ ReLU units in the plane, \ randomly initialized, \ arranged in $1$ to $6$ layers", font_size=28)
        head.to_edge(UP, buff=0.4)
        note_ = label(r"at random, depth does not multiply the pieces: \\ what it can do, and what training finds, differ",
                      font_size=28, color=C.BITS).to_edge(DOWN, buff=0.75)
        cite_ = cite(r"B.~Hanin \& D.~Rolnick, \textit{Deep ReLU Networks Have Surprisingly Few Activation Patterns} (2019)",
                     corner=DR)
        with self.voiceover(
            "But that's what depth can do, with weights chosen by hand. What does a random network do? Here are "
            "forty-eight units cutting the plane, arranged in one layer, then two, three, four and six. "
            "<bookmark mark='a'/> The number of pieces barely changes, and even falls. Hanin and Rolnick showed in "
            "2019 that typical networks have far fewer pieces than the maximum. Depth helps in subtler ways: by "
            "making useful functions easy for training to reach."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(note_), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()
