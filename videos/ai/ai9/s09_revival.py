from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import BWD, FWD, HIST, NEURON, PART, load, log_axes


class Revival(VoiceoverScene):
    def construct(self):
        self.card()
        self.vanishing()
        self.nineties()
        self.dbn()
        self.fixes()

    def card(self):
        card = chapter_card(8, r"The second winter, and the revival", r"If backpropagation works, why did deep "
                            r"networks fail?", lit=(1991, 2010, 2012), part=PART)
        with self.voiceover("Chapter eight. The second winter, and the revival."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def vanishing(self):
        r = load("ridge")
        gs = np.asarray(r["gsd_sigmoid_std"])
        L = int(r["L"])
        lg = np.log10(np.maximum(gs, 1e-300))
        lo = int(math.floor(lg.min() / 10) * 10)
        g = log_axes([1, L], [lo, 0], 6.6, 4.4, center=[-2.6, -0.7, 0], xlabel=r"layer \ (input $\to$ output)",
                     ylabel=r"size of the gradient reaching each layer \ (log scale)", xticks=[], yticks=range(lo, 1, 10))
        g.add(MathTex("1", font_size=20, color=GREY_B).next_to(g.ax.c2p(1, lo), DOWN, buff=0.12),
              MathTex(str(L), font_size=20, color=GREY_B).next_to(g.ax.c2p(L, lo), DOWN, buff=0.12))
        layers = np.arange(1, L + 1)
        line = curve(g.ax, layers, lg, BWD, 4)
        per = 10 ** (-(lg[-1] - lg[0]) / (L - 1))
        e = int(round(-lg[0]))
        hc = history_card(1991, r"Sepp Hochreiter, \ TU Munich, \ diploma thesis",
                          r"gradients through many layers, \ or many time steps, \ vanish or explode", width=5.0,
                          color=HIST).move_to([4.45, 2.0, 0])
        why_ = label(r"each layer multiplies the gradient \\ by a slope $\le \tfrac14$ \\ and a weight matrix", font_size=26,
                     color=GREY_A).move_to([4.45, -0.7, 0])
        # the product the gradient goes through, layer by layer
        prod = cmath(r"\delta^{1}", r"=", r"D_1 W_2^{\top}\, D_2 W_3^{\top} \cdots D_{L-1} W_L^{\top}", r"\,\delta^{L}",
                     font_size=44, colors={r"\delta^{1}": BWD, r"\,\delta^{L}": BWD}).move_to([-1.4, 0.6, 0])
        prod_l = label(r"$D_l$: \ the slopes of layer $l$'s units, \ $\sigma'(z^l) \le \tfrac14$ for a sigmoid", font_size=28,
                       color=GREY_A).next_to(prod, DOWN, buff=0.35)
        tag = note(r"computed: \ $50$ sigmoid layers of $256$, \ weights $U[-1/\sqrt{n}, 1/\sqrt{n}]$").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Through the nineties, backpropagation worked for networks with one or two hidden layers. Deeper ones "
            "barely trained. <bookmark mark='a'/> In 1991 Sepp Hochreiter, a student in Munich, worked out why. The "
            "gradient that reaches an early layer is a product of one factor for every layer above it, and those "
            "factors are rarely close to one. <bookmark mark='b'/> Here is a fifty-layer network of S-shaped units, "
            "set up the usual way of the time, with a gradient sent down from the top. Each layer multiplies it by "
            f"the slope of a sigmoid, at most a quarter, and by the weights: about {per:.1f} times smaller per layer. "
            f"<bookmark mark='c'/> By the first layer it's ten to the minus {e}. The early layers might as well be "
            "frozen."
        ) as vo:
            self.play(Write(prod), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(prod_l))
            vo.wait_until("b")
            self.play(FadeOut(prod), FadeOut(prod_l))
            self.play(FadeIn(g), FadeIn(tag))
            self.play(Create(line), run_time=3.0, rate_func=linear)
            self.play(FadeIn(why_))
            vo.wait_until("c")
            self.play(Flash(g.ax.c2p(1, lg[0]), color=BWD, flash_radius=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nineties(self):
        cards = VGroup(
            history_card(1995, r"Corinna Cortes \& Vladimir Vapnik: \ support vector machines",
                         r"convex training, \ a theory of generalization, \ kernels: \ they win the benchmarks \ (Part 6)",
                         width=6.2, color=C.TRUE_P),
            history_card(1997, r"Sepp Hochreiter \& J\"urgen Schmidhuber: \ LSTM",
                         r"a fix for vanishing gradients through time \ (Part 10)", width=6.2, color=HIST),
            history_card(1998, r"Yann LeCun, L\'eon Bottou, Yoshua Bengio \& Patrick Haffner",
                         r"convolutional networks read handwriting and bank checks \ (Part 10)", width=6.2, color=HIST),
            history_card(r"1990s", r"the second winter for networks",
                         r"deep networks are hard to train and hard to analyse; \ most of the field moves to kernels "
                         r"and graphical models \ (Parts 6 and 7)", width=6.2, color=GREY_B),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.35)).move_to(DOWN * 0.1)
        head = label(r"The nineties", font_size=34).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Meanwhile, other methods were winning. <bookmark mark='a'/> In 1995 Corinna Cortes and Vladimir Vapnik "
            "introduced the support vector machine: convex, so training always found the best answer, with a theory "
            "of generalization behind it. <bookmark mark='b'/> Networks kept a few strongholds: the LSTM of 1997, built "
            "to carry gradients through time, <bookmark mark='c'/> and Yann LeCun's convolutional networks, which by "
            "the late nineties were reading handwriting and bank checks. <bookmark mark='d'/> But for most of the "
            "field, deep networks were hard to train and harder to analyse, and attention moved to kernels and "
            "graphical models. For networks, it was a second winter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(Circumscribe(cards[0], color=C.TRUE_P))
            for k, mk in zip((1, 2, 3), "bcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dbn(self):
        """Greedy layer-wise pretraining, as a schematic: each layer learns to model the one below, then the stack is
        fine-tuned by backpropagation."""
        xs = [-5.6, -4.0, -2.4, -0.8]
        cols = [GREY_B, NEURON, NEURON, NEURON]
        layers = VGroup(*[VGroup(*[Circle(radius=0.15, color=c, stroke_width=2.5).move_to([x, 1.6 - 0.5 * j, 0])
                                   for j in range(7)]) for x, c in zip(xs, cols)])
        names = VGroup(label(r"data", font_size=22, color=GREY_B).next_to(layers[0], DOWN, buff=0.2),
                       *[label(rf"layer {i}", font_size=22, color=NEURON).next_to(layers[i], DOWN, buff=0.2)
                         for i in (1, 2, 3)])
        links = [VGroup(*[Line(a_.get_center(), b_.get_center(), buff=0.15, stroke_width=1, color=GREY_D)
                          for a_ in layers[i] for b_ in layers[i + 1]]) for i in range(3)]
        steps = VGroup(label(r"1. \ layer 1 learns to model the data", font_size=24, color=NEURON),
                       label(r"2. \ freeze it; \ layer 2 learns to model layer 1", font_size=24, color=NEURON),
                       label(r"3. \ and so on, \ one layer at a time", font_size=24, color=NEURON),
                       label(r"4. \ fine-tune the whole stack by backpropagation", font_size=24, color=BWD))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.9, 0])
        hc = history_card(2006, r"Geoffrey Hinton, Simon Osindero \& Yee-Whye Teh: \ deep belief nets",
                          r"each layer a restricted Boltzmann machine \ (Part 20), \ trained without labels", width=6.0,
                          color=HIST).move_to([3.6, -2.2, 0])
        tag = note(r"schematic").to_corner(DL, buff=0.25)
        cifar = label(r"2004: \ CIFAR's program in neural computation, \ led by Hinton, \ keeps a small community "
                      r"together", font_size=22, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "A small community kept going, supported from 2004 by a Canadian research program led by Geoffrey "
            "Hinton. In 2006 he and his colleagues found a way to train deep networks. <bookmark mark='a'/> Don't "
            "train them all at once. First let one layer learn, without labels, to model the data. "
            "<bookmark mark='b'/> Freeze it, and let the next layer learn to model the first layer's outputs; "
            "<bookmark mark='c'/> and so on up the stack. <bookmark mark='d'/> Then fine-tune everything together "
            "with backpropagation, starting from these sensible weights instead of random ones. They called it a "
            "deep belief net, and with work by Yoshua Bengio's group and others the same year, the name deep "
            "learning stuck."
        ) as vo:
            self.play(FadeIn(cifar), FadeIn(layers[0]), FadeIn(names[0]), FadeIn(tag), FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(links[0]), FadeIn(layers[1]), FadeIn(names[1]), FadeIn(steps[0]))
            self.play(layers[1].animate.set_fill(NEURON, opacity=0.4))
            vo.wait_until("b")
            self.play(links[0].animate.set_color(GREY_B), Create(links[1]), FadeIn(layers[2]), FadeIn(names[2]),
                      FadeIn(steps[1]))
            self.play(layers[2].animate.set_fill(NEURON, opacity=0.4))
            vo.wait_until("c")
            self.play(Create(links[2]), FadeIn(layers[3]), FadeIn(names[3]), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(*[l_.animate.set_color(BWD) for l_ in links], FadeIn(steps[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fixes(self):
        items = [
            (2009, r"GPUs: \ Raina, Madhavan \& Ng; \ 2010: \ Cire\c{s}an et al.\ train plain deep nets on graphics "
                   r"cards, \ no pretraining", C.GRADS),
            (2010, r"Glorot \& Bengio: \ initialization \ (next chapter); \ ReLUs \ (Nair \& Hinton; \ Glorot, "
                   r"Bordes \& Bengio, 2011)", FWD),
            (2012, r"speech recognition \ (four groups, \ with Hinton); \ AlexNet wins ImageNet \ (Part 10)", HIST),
            (2018, r"Bengio, Hinton \& LeCun share the Turing Award", C.BITS),
        ]
        cards = VGroup(*[history_card(y, t, r"", width=6.2, color=c) for y, t, c in items])
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.4)).move_to(UP * 0.4)
        head = label(r"Then the pretraining turned out not to be needed", font_size=32).to_edge(UP, buff=0.35)
        plan = label(r"the fixes, one at a time: \ initialization, \ the edge of chaos, \ residual streams, \ "
                     r"normalization", font_size=26, color=C.BITS).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Then, within a few years, the pretraining turned out not to be needed. <bookmark mark='a'/> Graphics "
            "cards made training many times faster, and in 2010 Dan Ciresan and colleagues set a record on "
            "handwritten digits with plain deep networks, trained by plain backpropagation. "
            "<bookmark mark='b'/> Better starting weights, from Xavier Glorot and Yoshua Bengio, and the ReLU, kept "
            "signals alive. <bookmark mark='c'/> In 2012 deep networks took over speech recognition and, with "
            "AlexNet, image recognition: Part 10's story. <bookmark mark='d'/> In 2018 Bengio, Hinton and LeCun "
            "shared the Turing Award. <bookmark mark='e'/> The rest of this part takes the fixes one at a time, with "
            "their mathematics: initialization, the edge of chaos, residual streams, and normalization."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(Circumscribe(cards[0], color=C.GRADS))
            for k, mk in zip((1, 2, 3), "bcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(plan))
        self.wait(0.3)
        self.clear_scene()
