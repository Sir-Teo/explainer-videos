from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import BWD, FWD, HIST, PART, WEIGHT, load, network

COLORS = {r"\delta^l": BWD, r"\delta^L": BWD, r"\delta^{l+1}": BWD, r"W^{l+1}": WEIGHT, r"W^l": WEIGHT,
          r"a^{l-1}": FWD, r"z^l": FWD, r"z^L": FWD}


class Backprop(VoiceoverScene):
    def construct(self):
        self.card()
        self.credit()
        self.derive()
        self.flow()
        self.check()
        self.history()

    def card(self):
        card = chapter_card(4, r"Backpropagation", r"How much is a hidden unit to blame?", lit=(1986,), part=PART)
        with self.voiceover("Chapter four. Backpropagation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def credit(self):
        net = network([3, 4, 4, 2], x0=-6.0, x1=-1.2, height=3.6, center=[-3.6, -0.2, 0], radius=0.22)
        err = VGroup(*[label(r"error", font_size=28, color=C.SURPRISE).next_to(c, RIGHT, buff=0.15)
                       for c in net.layers[-1]])
        qs = VGroup(*[MathTex(r"?", font_size=30, color=BWD).move_to(c) for lay in net.layers[1:3] for c in lay])
        eqs = VGroup(cmath(r"z^l", r"=", r"W^l", r"a^{l-1}", r"+ b^l", font_size=44, colors=COLORS),
                     cmath(r"a^l", r"=", r"\varphi(", r"z^l", r")", font_size=44, colors=COLORS),
                     cmath(r"L", r"=", r"\text{loss}(a^L,\ y)", font_size=44)).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        eqs.move_to([3.4, 1.0, 0])
        notes_ = label(r"$z$: \ a layer's weighted sums; \\ $a$: \ its outputs; \ $\varphi$: \ the bend", font_size=26,
                       color=GREY_A).next_to(eqs, DOWN, buff=0.35)
        chain = label(r"the chain rule \ (Part 4), \ organized: \\ one sweep backwards gives every weight's share",
                      font_size=30, color=BWD).move_to([3.4, -2.5, 0])
        spot = net.get_center()
        net.scale(1.3).move_to(ORIGIN + DOWN * 0.1)
        for e_, c in zip(err, net.layers[-1]):
            e_.next_to(c, RIGHT, buff=0.15)
        for q_, c in zip(qs, [c for lay in net.layers[1:3] for c in lay]):
            q_.move_to(c)
        grp = VGroup(net, err, qs)
        with self.voiceover(
            "XOR showed what was missing: a way to train the units in the middle. At the output, the error is plain "
            "to see: compare the answer with the target. <bookmark mark='a'/> But how much is a hidden unit to blame? "
            "Its effect on the loss passes through every unit after it. <bookmark mark='b'/> Write the network layer "
            "by layer. A layer's weighted sums, z, are a weight matrix times the previous layer's outputs, plus a "
            "bias; its outputs, a, bend z with a nonlinearity, phi; and the loss depends on the last layer. "
            "<bookmark mark='c'/> The chain rule from Part 4 answers the question, and it can be organized so that a "
            "single sweep backwards answers it for every weight at once."
        ) as vo:
            self.play(FadeIn(net), FadeIn(err))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(q, scale=1.4) for q in qs], lag_ratio=0.08))
            vo.wait_until("b")
            grp.generate_target()
            grp.target.scale(1 / 1.3)
            grp.target.shift(spot - grp.target[0].get_center())
            self.play(MoveToTarget(grp), run_time=1.0)
            self.play(LaggedStart(*[Write(e) for e in eqs], lag_ratio=0.4), FadeIn(notes_), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(chain))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"\delta^l", r"\equiv", r"\partial L / \partial", r"z^l", font_size=44, colors=COLORS),
            cmath(r"\delta^L", r"=", r"\nabla_{a^L} L \ \odot\ \varphi'(", r"z^L", r")", font_size=44, colors=COLORS),
            cmath(r"\delta^l", r"=", r"\big(", r"W^{l+1}", r"\big)^{\!\top}", r"\delta^{l+1}", r"\ \odot\ \varphi'(",
                  r"z^l", r")", font_size=44, colors=COLORS),
            cmath(r"\partial L / \partial W^l", r"=", r"\delta^l", r"\big(", r"a^{l-1}", r"\big)^{\!\top}",
                  r",\qquad \partial L / \partial b^l = ", r"\delta^l", font_size=44, colors=COLORS),
        ]
        whys = [why(r"how much the loss cares \\ about layer $l$'s sums"),
                why(r"chain rule at the top: \\ $a^L = \varphi(z^L)$, \ unit by unit"),
                why(r"$z^l$ reaches the loss only \\ through $a^l$, \ then $z^{l+1}$"),
                why(r"$z^l$ is linear in $W^l$ and $b^l$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-3.0, buff=0.85, edge=6.9)
        box = SurroundingRectangle(VGroup(rows[2], rows[3]), color=BWD, buff=0.15, corner_radius=0.08)
        same = label(r"the same matrices, transposed: \ the error flows backwards along the same wires", font_size=30,
                     color=BWD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Define delta for a layer: how much the loss changes when that layer's weighted sums change. "
            "<bookmark mark='a'/> At the top it's immediate: the loss's gradient with respect to the outputs, times "
            "the slope of the bend at each unit. <bookmark mark='b'/> Now go down one layer. Layer l's sums reach the "
            "loss only through its outputs, and those only through the next layer's sums. The chain rule says: "
            "take the next layer's delta, send it back through the transpose of the same weight matrix, and multiply "
            "by the slope of the bend. <bookmark mark='c'/> And once you know a layer's delta, its weights' gradient "
            "is just delta times the outputs coming into it, because the sums are linear in the weights. "
            "<bookmark mark='d'/> Two lines, applied layer after layer from the top: that's backpropagation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(Create(box), FadeIn(same))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def flow(self):
        net = network([3, 4, 4, 2], x0=-6.1, x1=-0.1, height=4.4, center=[-3.1, 0.0, 0], radius=0.26)
        fl = cmath(r"a^l = \varphi(W^l a^{l-1} + b^l)", font_size=36, color=FWD).move_to([3.9, 2.7, 0])
        bl = cmath(r"\delta^l = (W^{l+1})^{\top} \delta^{l+1} \odot \varphi'(z^l)", font_size=36, color=BWD)
        bl.move_to([3.9, 1.75, 0])
        wl = cmath(r"\partial L / \partial W^l = \delta^l (a^{l-1})^{\top}", font_size=36, color=WEIGHT).move_to([3.9, 0.8, 0])
        cost = VGroup(label(r"forward: \ one matrix product per layer", font_size=26, color=FWD),
                      label(r"backward: \ two \ (for $\delta$, \ and for $\partial W$)", font_size=26, color=BWD),
                      label(r"a training step $\approx 3\times$ a forward pass:", font_size=26, color=C.BITS),
                      label(r"about $6$ operations per weight per example \ (Part 12)", font_size=26, color=C.BITS),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        cost.move_to([3.75, -1.5, 0])
        pause = pause_card(r"How does the cost of the backward pass compare with the forward pass?", width=5.6,
                           font_size=26).move_to([3.75, -1.5, 0])

        def sweep(layer_from, layer_to, edges, color):
            dots = [glow_dot(e.get_start() if layer_to > layer_from else e.get_end(), color=color, radius=0.06)
                    for e in edges]
            targets = [e.get_end() if layer_to > layer_from else e.get_start() for e in edges]
            return dots, targets

        with self.voiceover(
            "Picture it as traffic. <bookmark mark='a'/> In the forward pass, values flow up: each layer multiplies by "
            "its weights and bends. <bookmark mark='b'/> At the top the loss compares the answer with the target. "
            "<bookmark mark='c'/> In the backward pass, errors flow down the same wires, through the transposed "
            "matrices, scaled at each unit by the slope of its bend, and every weight gets its gradient on the way "
            "past. <bookmark mark='d'/> Pause and predict: how expensive is the backward pass, compared with the "
            "forward one? <bookmark mark='e'/> Each layer does two matrix products going back, one for the deltas and "
            "one for the weight gradients, against one going forward. So a training step costs about three forward "
            "passes, about six arithmetic operations per weight per example. That six comes back in Part 12, in the "
            "formula for the cost of training a language model."
        ) as vo:
            self.play(FadeIn(net), Write(fl))
            vo.wait_until("a")
            for i in range(3):
                dots, tg = sweep(i, i + 1, net.edges[i], FWD)
                self.add(*dots)
                self.play(*[d_.animate.move_to(t_) for d_, t_ in zip(dots, tg)],
                          *[c.animate.set_fill(FWD, opacity=0.45) for c in net.layers[i + 1]], run_time=0.7)
                self.remove(*dots)
            vo.wait_until("b")
            self.play(*[Flash(c, color=C.SURPRISE) for c in net.layers[-1]])
            vo.wait_until("c")
            self.play(Write(bl))
            for i in (2, 1, 0):
                dots, tg = sweep(i + 1, i, net.edges[i], BWD)
                self.add(*dots)
                self.play(*[d_.animate.move_to(t_) for d_, t_ in zip(dots, tg)],
                          *[c.animate.set_fill(BWD, opacity=0.45) for c in net.layers[i]],
                          net.edges[i].animate.set_color(WEIGHT), run_time=0.7)
                self.remove(*dots)
            self.play(Write(wl))
            vo.wait_until("d")
            self.play(FadeIn(pause, shift=UP * 0.2))
            vo.wait_until("e")
            self.play(FadeOut(pause), LaggedStart(*[FadeIn(c_) for c_ in cost], lag_ratio=0.5), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        d = load("xor")
        ga, gb, gf = (np.asarray(d[k]) for k in ("g_ad", "g_bp", "g_fd"))
        names = [r"W_{1,11}", r"W_{1,12}", r"W_{1,21}", r"W_{1,22}", r"b_{1,1}", r"b_{1,2}", r"W_{2,1}", r"W_{2,2}",
                 r"b_2"]
        head = VGroup(label(r"weight", font_size=28, color=GREY_A), label(r"our autodiff", font_size=28, color=FWD),
                      label(r"the delta equations", font_size=28, color=BWD),
                      label(r"finite differences", font_size=28, color=GREY_B))
        xs = [-5.0, -2.2, 1.1, 4.5]
        for h_, x in zip(head, xs):
            h_.move_to([x, 3.0, 0])
        hl = Line([-6.3, 2.68, 0], [6.3, 2.68, 0], color=GREY_C, stroke_width=1.5)
        rows = VGroup()
        for i, nm in enumerate(names):
            y = 2.25 - 0.5 * i
            rows.add(VGroup(MathTex(nm, font_size=32, color=WEIGHT).move_to([xs[0], y, 0]),
                            MathTex(f"{ga[i]:+.8f}", font_size=32, color=FWD).move_to([xs[1], y, 0]),
                            MathTex(f"{gb[i]:+.8f}", font_size=32, color=BWD).move_to([xs[2], y, 0]),
                            MathTex(f"{gf[i]:+.8f}", font_size=32, color=GREY_B).move_to([xs[3], y, 0])))
        agree = label(rf"largest difference: \ autodiff vs.\ the equations ${sci(max(d['err_bp'], 1e-17), 0)}$; \ "
                      rf"vs.\ finite differences ${sci(d['err_fd'], 0)}$ \ (relative)", font_size=28, color=C.BITS)
        agree.to_edge(DOWN, buff=0.45)
        tag = note(r"computed: \ the XOR network of chapter 3, \ at random weights").to_corner(DR, buff=0.15)
        tag.next_to(agree, UP, buff=0.12).align_to(agree, RIGHT)
        same = all(f"{a_:+.8f}" == f"{b_:+.8f}" == f"{c_:+.8f}" for a_, b_, c_ in zip(ga, gb, gf))
        agreement = ("They agree to the last printed digit. Backpropagation is not an approximation: it is the exact "
                     "gradient, computed in one sweep, where the brute-force way needs two forward passes for every "
                     "weight." if same else
                     "They agree to within the finite differences' own rounding. Backpropagation is the exact gradient, "
                     "computed in one sweep, where the brute-force way needs two forward passes for every weight.")
        with self.voiceover(
            "Let's check it on chapter three's XOR network, at random weights. <bookmark mark='a'/> Here are its nine "
            "gradients three ways: from the series' own automatic differentiation, which knows nothing about "
            "networks; <bookmark mark='b'/> from the delta equations, written out by hand; <bookmark mark='c'/> and by "
            "brute force, nudging each weight a millionth up and down and watching the loss. <bookmark mark='d'/> "
            + agreement
        ) as vo:
            self.play(FadeIn(head[0]), Create(hl), LaggedStart(*[FadeIn(r_[0]) for r_ in rows], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), LaggedStart(*[FadeIn(r_[1]) for r_ in rows], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(FadeIn(head[2]), LaggedStart(*[FadeIn(r_[2]) for r_ in rows], lag_ratio=0.05))
            vo.wait_until("c")
            self.play(FadeIn(head[3]), LaggedStart(*[FadeIn(r_[3]) for r_ in rows], lag_ratio=0.05))
            vo.wait_until("d")
            self.play(FadeIn(agree), FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(1970, r"Seppo Linnainmaa, \ Helsinki", r"the reverse mode of automatic differentiation, \ in "
                         r"a master's thesis, \ without networks", width=6.2, color=HIST),
            history_card(1974, r"Paul Werbos, \ Harvard", r"proposes training networks this way, \ in his PhD thesis; "
                         r"\ few notice", width=6.2, color=HIST),
            history_card(1986, r"David Rumelhart, Geoffrey Hinton \& Ronald Williams", r"\textit{Learning "
                         r"representations by back-propagating errors}, \ \textit{Nature}: \ hidden units learn useful "
                         r"features", width=6.2, color=BWD),
            history_card(1989, r"Yann LeCun et al., \ Bell Labs", r"backpropagation reads handwritten zip codes \ "
                         r"(convolutional networks: \ Part 10)", width=6.2, color=HIST),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.35)).move_to(DOWN * 0.15)
        head = label(r"Who found it", font_size=34).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The idea was found more than once. <bookmark mark='a'/> In 1970 Seppo Linnainmaa, a Finnish master's "
            "student, described the reverse mode of automatic differentiation, with no networks in sight. "
            "<bookmark mark='b'/> In 1974 Paul Werbos proposed training networks this way, in his Harvard thesis, "
            "and few noticed. <bookmark mark='c'/> In 1986 David Rumelhart, Geoffrey Hinton and Ronald Williams "
            "showed in Nature that networks trained by back-propagating errors learn useful features in their hidden "
            "units, and the field woke up. <bookmark mark='d'/> By 1989 Yann LeCun's networks at Bell Labs were "
            "reading handwritten zip codes. Hidden layers could be trained. The next question: what can they "
            "represent?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(Circumscribe(cards[0], color=HIST))
            for k, mk in zip((1, 2, 3), "bcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
