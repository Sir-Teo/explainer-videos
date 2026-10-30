from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, PART, VALUE, load, matrix_heat


def node(tex, pos, color=GREY_B, r=0.42):
    c = Circle(radius=r, color=color, stroke_width=3, fill_color=BACKGROUND, fill_opacity=1).move_to(pos)
    return VGroup(c, MathTex(tex, font_size=34).move_to(c))


class Backprop(VoiceoverScene):
    def construct(self):
        self.card()
        self.by_hand()
        self.fan_in()
        self.layers()
        self.rank_one()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"Backpropagation, by hand", r"What actually happens, step by step?", lit=(1986,), part=PART)
        with self.voiceover("Chapter six. Backpropagation, by hand."):
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

    # ------------------------------------------------------------------
    def layers(self):
        col = {r"\delta_2": GRAD, r"\delta_1": GRAD, r"x^\top": VALUE, r"a_1^\top": VALUE}
        net = MathTex(r"z_1 = W_1 x + b_1,\quad a_1 = \tanh z_1,\quad z_2 = W_2 a_1 + b_2,\quad q = \operatorname{softmax}(z_2),"
                      r"\quad \mathcal L = -\log q_y", font_size=30, color=GREY_A).to_edge(UP, buff=0.3)
        rows = [
            cmath(r"\delta_2", r"=", r"\frac{\partial \mathcal L}{\partial z_2} = q - e_y", font_size=36, colors=col),
            cmath(r"\frac{\partial \mathcal L}{\partial W_2}", r"=", r"\delta_2", r"\, a_1^\top", font_size=36, colors=col),
            cmath(r"\delta_1", r"=", r"(W_2^\top", r"\delta_2", r")", r"\odot (1 - a_1^2)", font_size=36, colors=col),
            cmath(r"\frac{\partial \mathcal L}{\partial W_1}", r"=", r"\delta_1", r"\, x^\top", font_size=36, colors=col),
        ]
        whys = [why(r"softmax with cross-entropy: \ Part 1's $q - p$"),
                why(r"$z_{2,i} = \sum_j W_{2,ij}\, a_{1,j}$: \ each weight gets \\ its output's $\delta$ times its input"),
                why(r"back through $W_2$ (a VJP: transpose), \\ then through $\tanh$, \ whose slope is $1 - a^2$"),
                why(r"the same rule, one layer down")]
        step = ladder(self, rows, whys, keep=4, top=2.35, x=-2.6, buff=0.48, edge=6.9)
        name = label(r"$\delta = \partial \mathcal L / \partial z$: \ the error signal at a layer", font_size=24, color=GRAD)
        name.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now a real network, in matrices: an input x, a layer with weights W one and a tanh, a second layer, a "
            "softmax and the cross-entropy. Call the gradient with respect to a layer's pre-activation z its delta, "
            "the error signal there. <bookmark mark='a'/> At the top, delta two is Part 1's answer: the predicted "
            "probabilities minus the one-hot truth. <bookmark mark='b'/> Each weight in W two multiplies one input "
            "into one output, so its gradient is that output's delta times that input: an outer product, delta two "
            "times a one transposed. <bookmark mark='c'/> To go down a layer, pull delta back through W two, which "
            "for a matrix means multiplying by its transpose, and then through the tanh, multiplying by its slope. "
            "<bookmark mark='d'/> And the same rule again: the gradient of W one is delta one times x transposed. "
            "Those four lines are backpropagation, for any depth."
        ) as vo:
            self.play(FadeIn(net), FadeIn(name))
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=GRAD, scale_factor=1.05))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rank_one(self):
        m = load("mlp2")
        B, (din, dh, k) = int(m["B"]), m["dims"]
        d1, x0 = np.asarray(m["d1_0"]), np.asarray(m["x0"])
        G = np.asarray(m["dW1_0"])
        sv1, svB = np.asarray(m["sv_one"]), np.asarray(m["sv_all"])
        assert m["d_lib"] < 1e-12 and m["d_torch"] < 1e-12
        cell = 0.55
        col = matrix_heat(d1[:, None], cell=cell, numbers=True, fmt="{:.2f}", font_size=15).move_to([-5.2, -0.2, 0])
        row = matrix_heat(x0[None, :], cell=cell, numbers=True, fmt="{:.2f}", font_size=15).move_to([-1.8, 1.65, 0])
        out = matrix_heat(G, cell=cell, numbers=True, fmt="{:.2f}", font_size=15).move_to([-1.8, -0.2, 0])
        lc = MathTex(r"\delta_1", font_size=30, color=GRAD).next_to(col, UP, buff=0.15)
        lr = MathTex(r"x^\top", font_size=30, color=VALUE).next_to(row, LEFT, buff=0.2)
        lo = MathTex(r"\delta_1 x^\top", font_size=30, color=WHITE).next_to(out, DOWN, buff=0.15)
        times = MathTex(r"\times", font_size=36, color=GREY_B).move_to([-3.95, -0.2, 0])
        n_nonzero = int((sv1 > 1e-10 * sv1[0]).sum())
        rank_b = int((svB > 1e-10 * svB[0]).sum())
        res = VGroup(
            label(rf"one example: \ singular values ${sv1[0]:.3f}$, \ then ${sci(max(sv1[1], 1e-20), 0)}$ and below",
                  font_size=24, color=GREY_A),
            label(rf"rank ${n_nonzero}$: \ every row is a multiple of $x^\top$", font_size=24, color=GRAD),
            label(rf"a batch of ${B}$: \ the sum of ${B}$ such matrices, \ rank ${rank_b}$", font_size=24, color=GREY_A),
            label(rf"by hand \ vs \ our library: \ ${sci(max(m['d_lib'], 1e-17), 0)}$", font_size=24, color=GRAD),
            label(rf"by hand \ vs \ PyTorch: \ ${sci(max(m['d_torch'], 1e-17), 0)}$", font_size=24, color=GRAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.9, -0.2, 0])
        keep_in_frame(res, margin=0.25)
        tag = note(rf"computed: \ a ${din}$--${dh}$--${k}$ network, \ ${B}$ examples").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here is that outer product for one example, computed: the error signal at the hidden layer, a column, "
            "times the input, a row. <bookmark mark='a'/> Every row of the result is a multiple of the same input, "
            f"so the matrix has rank {n_nonzero}: one singular value, then nothing but rounding. "
            f"<bookmark mark='b'/> A batch adds {B} of them, and here reaches rank {rank_b}, the most a "
            f"{dh} by {din} matrix can have. That low-rank structure comes back when models are fine-tuned with "
            "low-rank adapters in Part 27. <bookmark mark='c'/> And these hand-derived gradients match our library and "
            "PyTorch to the last digits a computer keeps."
        ) as vo:
            self.play(FadeIn(col), FadeIn(lc), FadeIn(row), FadeIn(lr), FadeIn(times), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(c) for c in out], lag_ratio=0.03), FadeIn(lo), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("b")
            self.play(FadeIn(res[2]))
            vo.wait_until("c")
            self.play(FadeIn(res[3]), FadeIn(res[4]))
        self.wait(0.3)
        self.clear_scene()
