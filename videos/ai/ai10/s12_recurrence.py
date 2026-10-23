from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import (GRADC, HIST, KERNEL, LSTMC, PART, RNNC, img_heat, load)

HC = RNNC  # hidden states
XC = GREY_A  # inputs
RHO_C = {0.8: C.TRUE_P, 1.0: C.INTERVAL, 1.25: C.MODEL_Q, 2.0: C.SURPRISE}


class Recurrence(VoiceoverScene):
    def construct(self):
        self.card()
        self.unroll()
        self.bptt()
        self.decay()
        self.cliff()

    def card(self):
        card = chapter_card(11, r"Recurrence and vanishing gradients",
                            r"How does a network carry information through time, and why does it forget?",
                            lit=(1986, 1991), part=PART)
        with self.voiceover("Chapter eleven. Recurrence and vanishing gradients."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def chain(self, n=6, y=-0.6, x0=-5.0, dx=2.0):
        hs = VGroup(*[Circle(radius=0.36, stroke_color=HC, stroke_width=2.5, fill_color=HC, fill_opacity=0.15)
                      .move_to([x0 + dx * i, y, 0]) for i in range(n)])
        hl = VGroup(*[MathTex(rf"h_{{{i + 1}}}", font_size=28, color=HC).move_to(h) for i, h in enumerate(hs)])
        xs = VGroup(*[Square(0.55, stroke_color=XC, stroke_width=2).move_to([x0 + dx * i, y - 1.6, 0])
                      for i in range(n)])
        xl = VGroup(*[MathTex(rf"x_{{{i + 1}}}", font_size=26, color=XC).move_to(s) for i, s in enumerate(xs)])
        up = VGroup(*[Arrow(s.get_top(), h.get_bottom(), buff=0.06, stroke_width=2.5, color=XC,
                            max_tip_length_to_length_ratio=0.25) for s, h in zip(xs, hs)])
        side = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, stroke_width=3, color=HC,
                              max_tip_length_to_length_ratio=0.2) for a, b in zip(hs, hs[1:])])
        wl = VGroup(*[MathTex(r"W", font_size=24, color=HC).next_to(s, UP, buff=0.05) for s in side])
        ul = VGroup(*[MathTex(r"U", font_size=22, color=XC).next_to(a, LEFT, buff=0.05) for a in up])
        return VGroup(hs, hl, xs, xl, up, side, wl, ul)

    def unroll(self):
        card = definition_card(r"A recurrent network",
                               cmath(r"h_t = \tanh(W h_{t-1} + U x_t + b)", font_size=34), width=6.4,
                               color=HC).to_corner(UL, buff=0.35)
        ch = self.chain()
        hcs = VGroup(history_card(1986, r"Michael Jordan", r"networks with feedback, \ for sequences of actions",
                                  width=3.6, color=HIST, font_size=20),
                     history_card(1990, r"Jeffrey Elman", r"\textit{Finding Structure in Time}", width=3.6,
                                  color=HIST, font_size=20)).arrange(RIGHT, buff=0.25).to_corner(UR, buff=0.3)
        same = label(r"the same $W$ and $U$ at every step: \ weight sharing, in time", font_size=24, color=HC)
        same.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now the other half of this part: sequences. A convolution shares its weights across space. A "
            "recurrent network shares them across time. <bookmark mark='a'/> It keeps a hidden state h, a vector, "
            "and at each step mixes the old state with the new input through the same two weight matrices, W and "
            "U, and a squashing tanh. <bookmark mark='b'/> Unrolled in time, it's a very deep network with one "
            "layer per step, all of them sharing weights. <bookmark mark='c'/> Michael Jordan in 1986 and Jeffrey "
            "Elman in 1990 made the idea popular in cognitive science: Elman's networks found word boundaries and "
            "grammatical categories just by predicting the next item."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(ch[0][0]), FadeIn(ch[1][0]), FadeIn(ch[2][0]), FadeIn(ch[3][0]), GrowArrow(ch[4][0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(ch[5][i]), FadeIn(ch[6][i]), FadeIn(ch[0][i + 1]),
                                                   FadeIn(ch[1][i + 1]), FadeIn(ch[2][i + 1]), FadeIn(ch[3][i + 1]),
                                                   GrowArrow(ch[4][i + 1])) for i in range(5)], lag_ratio=0.4),
                      run_time=3.0)
            self.play(FadeIn(ch[7]), FadeIn(same))
            vo.wait_until("c")
            self.play(FadeIn(hcs, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bptt(self):
        colors = {r"W": HC, r"\sigma_{\max}(W)": HC, r"\mathrm{diag}\big(\tanh'(a_t)\big)": GRADC}
        rows = [
            cmath(r"\frac{\partial L}{\partial h_k}", r"=", r"\frac{\partial L}{\partial h_T}\,"
                  r"\frac{\partial h_T}{\partial h_k}", font_size=36),
            cmath(r"\frac{\partial h_T}{\partial h_k}", r"=", r"\prod_{t=k+1}^{T}", r"\mathrm{diag}\big(\tanh'(a_t)"
                  r"\big)", r"W", colors=colors, font_size=36),
            cmath(r"\Big\|\frac{\partial h_T}{\partial h_k}\Big\|", r"\le", r"\prod_{t=k+1}^{T}", r"1", r"\cdot",
                  r"\sigma_{\max}(W)", r"=", r"\sigma_{\max}(W)^{\,T-k}", colors=colors, font_size=36),
        ]
        rows[2][7].set_color(HC)
        whys = [why(r"the chain rule, \ back through time"),
                why(r"one Jacobian per step: \ $a_t = W h_{t-1} + U x_t + b$"),
                why(r"norms multiply at most; \ $|\tanh'| \le 1$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-2.6, align_index=1, edge=6.8)
        cases = VGroup(label(r"$\sigma_{\max} < 1$: \ the gradient vanishes, \ exponentially fast", font_size=26,
                             color=C.TRUE_P),
                       label(r"eigenvalues $> 1$: \ it can explode", font_size=26, color=C.SURPRISE))
        cases.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.5)
        hc = history_card(1991, r"Sepp Hochreiter, \ diploma thesis, \ Munich",
                          r"the problem analysed; \ then Bengio, Simard \& Frasconi (1994)", width=4.6,
                          color=HIST, font_size=20).to_corner(DR, buff=0.3).shift(UP * 1.4)
        cite_ = cite(r"Werbos (1990); \ Hochreiter (1991); \ Bengio, Simard \& Frasconi (1994)", corner=DL)
        with self.voiceover(
            "To train it, unroll it and backpropagate, as Paul Werbos described in 1990: backpropagation through "
            "time. <bookmark mark='a'/> The gradient with respect to an early state h k passes through every later "
            "state. <bookmark mark='b'/> Each step back multiplies it by that step's Jacobian: the tanh's slopes "
            "times the same matrix W, again and again. <bookmark mark='c'/> The slopes are at most one, so the "
            "product is at most the largest singular value of W, raised to the number of steps. "
            "<bookmark mark='d'/> Below one, the gradient from far back shrinks exponentially; with eigenvalues "
            "above one, it can blow up. <bookmark mark='e'/> Sepp Hochreiter worked this out in his 1991 diploma "
            "thesis; Yoshua Bengio, Patrice Simard and Paolo Frasconi published it in 1994."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(cases, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decay(self):
        g = load("rnn_grad")
        ks = np.asarray(g["ks"])
        rhos = list(g["rhos"])
        M, LO, HI = np.asarray(g["tanh_median"]), np.asarray(g["tanh_lo"]), np.asarray(g["tanh_hi"])
        LM = np.asarray(g["linear_median"])
        ylo, yhi = -12, 12
        ax = axes([0, ks[-1]], [ylo, yhi], x_length=7.0, y_length=4.4, xlabel=r"steps back, \ $T - k$",
                  ylabel=r"$\|\partial h_T / \partial h_k\|$", xticks=[0, 50, 100], yticks=[-10, -5, 0, 5, 10],
                  yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.0, -0.4, 0])
        A = ax.ax
        cl = lambda a: np.clip(a, ylo, yhi)  # noqa: E731
        tanh_c = VGroup(*[VGroup(band(A, ks, cl(LO[i]), cl(HI[i]), RHO_C[r], 0.15),
                                 curve(A, ks, cl(M[i]), RHO_C[r], 4)) for i, r in enumerate(rhos)])
        lin_c = VGroup(*[DashedVMobject(curve(A, ks, cl(LM[i]), RHO_C[r], 2.5), num_dashes=40)
                         for i, r in enumerate(rhos)])
        leg = legend([(RHO_C[r], rf"largest eigenvalue of $W$: \ ${r:g}$") for r in rhos], font_size=22)
        leg.to_corner(UR, buff=0.4)
        kl = label(r"solid: \ tanh; \ dashed: \ the same network, \ linear", font_size=20, color=GREY_B)
        kl.next_to(leg, DOWN, buff=0.3).align_to(leg, LEFT)
        tag = note(rf"computed: \ ${g['n']}$ hidden units, \ ${g['draws']}$ random networks each, \ median and "
                   r"10--90\%").to_corner(DR, buff=0.2)
        i50 = list(ks).index(50)
        a, b = M[0][i50], M[2][i50]
        lb = LM[2][i50]
        top = M[3][i50]
        if b < 0:
            mid = (f"Even at {rhos[2]:g}, where the linear network's gradient grows to ten to the {lb:.0f}, the "
                   f"tanh network's shrinks, to ten to the {b:.0f}: its units saturate, their slopes fall, and "
                   "they pull the product down.")
        else:
            mid = (f"At {rhos[2]:g} it grows: ten to the {b:.0f} after fifty steps, and the linear network's ten "
                   f"to the {lb:.0f}.")
        tail = (f"At {rhos[3]:g} the tanh network is chaotic, and its gradient explodes: ten to the {top:.0f}."
                if top > 1 else
                f"Even at {rhos[3]:g}, saturation keeps it near ten to the {top:.0f}.")
        with self.voiceover(
            "We measured it. Take random recurrent networks, run them on random inputs, and multiply the "
            "Jacobians back from the last step. <bookmark mark='a'/> When the largest eigenvalue of W is "
            f"{rhos[0]:g}, the gradient that reaches fifty steps back is ten to the {a:.0f} of what it was: gone. "
            f"<bookmark mark='b'/> {mid} <bookmark mark='c'/> {tail} <bookmark mark='d'/> Either way, a plain "
            "recurrent network has a narrow window of time over which it can learn anything, and the window is "
            "set by the size of W."
        ) as vo:
            self.play(Create(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(tanh_c[0]), FadeIn(leg[0]), FadeIn(lin_c[0]))
            vo.wait_until("b")
            self.play(FadeIn(tanh_c[1]), FadeIn(tanh_c[2]), FadeIn(lin_c[1]), FadeIn(lin_c[2]), FadeIn(leg[1]),
                      FadeIn(leg[2]), FadeIn(kl))
            vo.wait_until("c")
            self.play(FadeIn(tanh_c[3]), FadeIn(lin_c[3]), FadeIn(leg[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cliff(self):
        g = load("rnn_grad")
        ws, bs = np.asarray(g["cliff_ws"]), np.asarray(g["cliff_bs"])
        L = np.asarray(g["cliff_loss"])
        # rows of the array run from the lowest b; a picture's first row is its top
        img = img_heat(np.log10(L[::-1] + 1e-3), 5.6, sym=False, pos=C.HOT, mid="#0B1530", height=4.6)
        img.move_to([-2.6, -0.3, 0])
        frame = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.2)

        def P(w, b):
            x = img.get_left()[0] + img.width * (w - ws[0]) / (ws[-1] - ws[0])
            y = img.get_bottom()[1] + img.height * (b - bs[0]) / (bs[-1] - bs[0])
            return np.array([x, y, 0])

        xl = label(r"$w$", font_size=26).next_to(frame, DOWN, buff=0.12)
        yl = label(r"$b$", font_size=26).next_to(frame, LEFT, buff=0.12)
        title = label(r"$h_t = \tanh(w\,h_{t-1} + b)$, \ $50$ steps: \ the loss $(h_{50} - 0.7)^2$", font_size=24)
        title.to_edge(UP, buff=0.3)
        raw, clip = np.asarray(g["path_raw"]), np.asarray(g["path_clip"])
        inside = [p for p in raw if ws[0] <= p[0] <= ws[-1] and bs[0] <= p[1] <= bs[-1]]
        k_out = len(inside)
        pr = VMobject(color=C.SURPRISE, stroke_width=3).set_points_as_corners([P(*p) for p in inside])
        pc = VMobject(color=KERNEL, stroke_width=3).set_points_as_corners([P(*p) for p in clip])
        start = Dot(P(*g["cliff_start"]), radius=0.08, color=WHITE)
        far = raw[k_out] if k_out < len(raw) else raw[-1]
        out_arrow = Arrow(P(*inside[-1]), P(*inside[-1]) + RIGHT * 1.2, buff=0.0, color=C.SURPRISE, stroke_width=3)
        out_l = label(rf"thrown to $w \approx {far[0]:,.0f}$".replace(",", "{,}"), font_size=22, color=C.SURPRISE)
        out_l.next_to(out_arrow, RIGHT, buff=0.1)
        keep_in_frame(out_l)
        nr = np.asarray(g["norm_raw"])
        leg = legend([(C.SURPRISE, r"gradient descent"), (KERNEL, r"the same, \ gradient clipped to length $1$")],
                     font_size=22).to_corner(UR, buff=0.35).shift(DOWN * 0.6)
        res = VGroup(label(rf"largest gradient met: \ ${nr.max():,.0f}$".replace(",", "{,}"), font_size=22,
                           color=C.SURPRISE),
                     label(rf"clipped, \ final loss: \ ${g['loss_clip'][-1]:.4f}$", font_size=22, color=KERNEL))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        cite_ = cite(r"after Pascanu, Mikolov \& Bengio (2013)", corner=DR)
        tag = note(r"computed").to_corner(DL, buff=0.25)
        with self.voiceover(
            "Exploding gradients have a shape. <bookmark mark='a'/> Take the smallest recurrent network, one unit "
            "with a weight w and a bias b, run it for fifty steps, and ask its last state to be 0.7. Here is the "
            "loss over every w and b, bright where it is high. Where the unit switches from settling high to "
            "settling low, the loss jumps: a cliff. <bookmark mark='b'/> Gradient descent from near the edge meets "
            f"the cliff wall, where the gradient is {nr.max():,.0f}, and is thrown off the map. "
            "<bookmark mark='c'/> The fix, from Razvan Pascanu, Tomas Mikolov and Bengio in 2013: if the gradient "
            "is longer than a threshold, shrink it to that length. Clipped, the same descent ends at a loss of "
            f"{g['loss_clip'][-1]:.4f}. Our recurrent networks are trained with clipping, and so are today's "
            "language models."
        ) as vo:
            self.play(FadeIn(title), FadeIn(cite_), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(img), Create(frame), FadeIn(xl), FadeIn(yl))
            vo.wait_until("b")
            self.play(FadeIn(start), FadeIn(leg[0]))
            self.play(Create(pr), run_time=1.5)
            self.play(GrowArrow(out_arrow), FadeIn(out_l))
            vo.wait_until("c")
            self.play(Create(pc), FadeIn(leg[1]), run_time=2.0)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()


_ = (LSTMC, math)
