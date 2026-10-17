from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import GRAD, VALUE, load


def node(tex, pos, color=GREY_B, r=0.42):
    c = Circle(radius=r, color=color, stroke_width=3, fill_color=BACKGROUND, fill_opacity=1).move_to(pos)
    return VGroup(c, MathTex(tex, font_size=34).move_to(c))


class Backprop(VoiceoverScene):
    def construct(self):
        self.card()
        self.by_hand()
        self.fan_in()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"Backpropagation, by hand", r"What actually happens, step by step?", part=3)
        with self.voiceover("Chapter five. Backpropagation, by hand."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def by_hand(self):
        t = load("tiny")
        x, w, b, y = (t["inputs"][k] for k in "xwby")
        v, g = t["values"], t["grads"]
        assert abs(v["L"] - 0.854) < 0.001 and abs(g["w"] + 0.259) < 0.001
        Y = 0.6
        ops = [(r"\times", -4.3, 0.42), (r"+", -1.6, 0.42), (r"\sigma", 1.1, 0.42), (r"(\,\cdot - y\,)^2", 3.9, 0.66)]
        opn = [node(o, [xx, Y, 0], r=r) for o, xx, r in ops]
        ins = [node(r"x", [-6.1, 2.0, 0], VALUE), node(r"w", [-6.1, -0.8, 0], C.BITS), node(r"b", [-2.9, -1.1, 0], C.BITS),
               node(r"y", [2.5, -1.2, 0], VALUE)]
        L_end = node(r"\mathcal{L}", [6.3, Y, 0], C.LOSS, r=0.36)
        edges = [(ins[0], opn[0]), (ins[1], opn[0]), (opn[0], opn[1]), (ins[2], opn[1]), (opn[1], opn[2]), (opn[2], opn[3]),
                 (ins[3], opn[3]), (opn[3], L_end)]
        arrows = []
        for a, bb in edges:
            d = bb.get_center() - a.get_center()
            d = d / np.linalg.norm(d)
            arrows.append(Arrow(a.get_center() + d * a[0].width / 2, bb.get_center() - d * bb[0].width / 2, buff=0.06,
                                color=GREY_D, stroke_width=3, max_tip_length_to_length_ratio=0.12))

        def tag(edge, text, color, side=UP, buff=0.1):
            return MathTex(text, font_size=28, color=color).next_to(arrows[edge].get_center(), side, buff=buff)

        fwd = [tag(0, rf"{x:g}", VALUE, LEFT), tag(1, rf"{w:g}", VALUE, LEFT), tag(2, rf"u = {v['u']:g}", VALUE),
               tag(3, rf"{b:g}", VALUE, RIGHT), tag(4, rf"z = {v['z']:g}", VALUE), tag(5, rf"a = {v['a']:.3f}", VALUE),
               tag(6, rf"{y:g}", VALUE, RIGHT), tag(7, rf"{v['L']:.3f}", VALUE)]
        bwd = [tag(7, r"1", GRAD, DOWN), tag(5, rf"{g['a']:.3f}", GRAD, DOWN), tag(4, rf"{g['z']:.3f}", GRAD, DOWN),
               tag(3, rf"{g['b']:.3f}", GRAD, LEFT), tag(2, rf"{g['u']:.3f}", GRAD, DOWN), tag(1, rf"{g['w']:.3f}", GRAD, RIGHT)]
        local = [MathTex(t_, font_size=26, color=GREY_A).next_to(opn[k], UP, buff=0.14) for k, t_ in
                 ((3, r"\times 2(a - y)"), (2, r"\times a(1-a)"), (1, r"\times 1"), (0, r"\times x"))]
        legend = VGroup(label(r"values, forwards", font_size=24, color=VALUE),
                        label(r"gradients $\partial \mathcal{L} / \partial(\cdot)$, backwards", font_size=24, color=GRAD),
                        label(r"each step's own derivative", font_size=24, color=GREY_A))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DR, buff=0.45)
        head = label(r"one input, one weight, one bias, a sigmoid, a squared error", font_size=30).to_edge(UP, buff=0.35)
        # the squash, drawn under its node: an S-curve from 0 up to 1
        sx = np.linspace(-3, 3, 40)
        s_ax = VGroup(DashedLine([-0.55, 0, 0], [0.55, 0, 0], color=GREY_D, stroke_width=1.5, dash_length=0.05),
                      DashedLine([-0.55, 0.5, 0], [0.55, 0.5, 0], color=GREY_D, stroke_width=1.5, dash_length=0.05))
        s_curve = VMobject(stroke_color=C.MLP, stroke_width=3).set_points_smoothly(
            [np.array([u / 3 * 0.55, 0.5 / (1 + np.exp(-2 * u)), 0]) for u in sx])
        s_lab = VGroup(MathTex("0", font_size=18, color=GREY_B).next_to(s_ax[0], LEFT, buff=0.06),
                       MathTex("1", font_size=18, color=GREY_B).next_to(s_ax[1], LEFT, buff=0.06))
        squash = VGroup(s_ax, s_curve, s_lab).next_to(opn[2], DOWN, buff=0.35)
        parts = gloss(r"weight, \ bias, \ sigmoid, \ squared error",
                      r"$z = w\,x + b$: \ the input times a weight, plus a bias (a shift)\\"
                      r"$a = \sigma(z)$: \ an S-curve squashes $z$ into $0$ to $1$\\"
                      r"$\mathcal{L} = (a - y)^2$: \ the miss from the target $y$, squared", corner=DL, width=5.6, color=VALUE)
        with self.voiceover(
            "Let's run it by hand, on the smallest network there is, drawn as a flowchart of operations called a "
            "computation graph, each circle a node. One input, x, times one weight, plus one bias, a shift; "
            "<bookmark mark='s'/> then a squashing function, the sigmoid, an S-curve that presses any number into "
            "the range zero to one; and a squared error: the miss from the target y, squared. <bookmark mark='a'/> "
            "Forwards first: the values flow from left to right, and end in the loss, 0.854."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(m) for m in ins + opn + [L_end]], lag_ratio=0.08),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), run_time=2.0)
            self.play(FadeIn(parts))
            vo.wait_until("s")
            self.play(Create(s_curve), FadeIn(s_ax), FadeIn(s_lab))
            vo.wait_until("a")
            for k in range(8):
                self.play(FadeIn(fwd[k], shift=RIGHT * 0.1), arrows[k].animate.set_color(VALUE), run_time=0.45)
            self.play(FadeIn(legend[0]))
        with self.voiceover(
            "Now backwards. Start at the loss, with a gradient of one, and walk back. <bookmark mark='a'/> Each step "
            "multiplies the gradient arriving from the right by its own local derivative, and passes the result to "
            "the left. <bookmark mark='b'/> At the weight, the gradient is minus 0.259: raise the weight a little, "
            "and the loss falls by about a quarter as much. No step needed to know anything but its own derivative."
        ) as vo:
            self.play(FadeIn(bwd[0]), arrows[7].animate.set_color(GRAD), FadeIn(legend[1]))
            vo.wait_until("a")
            for k, lk, arr in ((1, 0, 5), (2, 1, 4), (3, 2, 3), (4, None, 2), (5, 3, 1)):
                anims = [FadeIn(bwd[k], shift=LEFT * 0.1), arrows[arr].animate.set_color(GRAD)]
                if lk is not None:
                    anims.append(FadeIn(local[lk]))
                if k == 1:
                    anims.append(FadeIn(legend[2]))
                self.play(*anims, run_time=0.7)
            vo.wait_until("b")
            self.play(Indicate(bwd[5], color=GRAD, scale_factor=1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fan_in(self):
        w = node(r"w", [-3.2, 0, 0], C.BITS)
        a = node(r"f", [0.2, 1.3, 0])
        b = node(r"g", [0.2, -1.3, 0])
        L = node(r"\mathcal{L}", [3.6, 0, 0], C.LOSS, r=0.38)
        arr = [Arrow(p.get_center(), q.get_center(), buff=0.48, color=GREY_D, stroke_width=3) for p, q in
               ((w, a), (w, b), (a, L), (b, L))]
        back = [Arrow(q.get_center(), p.get_center(), buff=0.48, color=GRAD, stroke_width=4).shift(0.15 * DOWN)
                for p, q in ((w, a), (w, b))]
        plus = MathTex(r"\frac{\partial \mathcal{L}}{\partial w} = \frac{\partial \mathcal{L}}{\partial w}\Big|_{\text{via } f} + "
                       r"\frac{\partial \mathcal{L}}{\partial w}\Big|_{\text{via } g}", font_size=40, color=GRAD).to_edge(DOWN, buff=0.6)
        algo = label(r"visit the nodes in reverse order; \ each passes its gradient back to its inputs, \ and adds up "
                     r"what arrives", font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "One more rule. When a value feeds into two places, <bookmark mark='a'/> the gradients coming back from "
            "both are added together. <bookmark mark='b'/> That's the whole algorithm: visit the nodes in reverse "
            "order, and let each one pass its gradient back to its inputs."
        ) as vo:
            self.play(FadeIn(w), FadeIn(a), FadeIn(b), FadeIn(L), *[GrowArrow(x) for x in arr])
            vo.wait_until("a")
            self.play(*[GrowArrow(x) for x in back])
            self.play(Write(plus))
            vo.wait_until("b")
            self.play(FadeIn(algo))
        self.wait(0.3)
        self.clear_scene()
