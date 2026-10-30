from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import HIST, PART, load, takeaway_card

B_COLORS = {1: C.SURPRISE, 16: C.BITS}


def loss_axes(d, center=(-2.8, -0.3), width=6.6):
    """The two-weight logistic loss of Part 6: axes and contour lines."""
    w1, w2 = np.asarray(d["w1"]), np.asarray(d["w2"])
    ax = Axes(x_range=[w1[0], w1[-1], 0.5], y_range=[w2[0], w2[-1], 0.5], x_length=width,
              y_length=width * (w2[-1] - w2[0]) / (w1[-1] - w1[0]) * 0.75, tips=False,
              axis_config={"stroke_width": 0}).move_to([*center, 0])
    L = np.asarray(d["L"])

    def f(x, y):
        i = int(np.clip(np.searchsorted(w2, y), 1, len(w2) - 1))
        j = int(np.clip(np.searchsorted(w1, x), 1, len(w1) - 1))
        return float(L[i, j])

    lmin = float(L.min())
    cont = contour_lines(ax, f, (w1[0], w1[-1]), (w2[0], w2[-1]),
                         list(lmin + np.array([0.003, 0.01, 0.025, 0.05, 0.09, 0.15, 0.22, 0.32, 0.45])), n=(120, 140),
                         stroke_width=1.4)
    star = Star(n=5, outer_radius=0.12, color=WHITE, fill_opacity=1).move_to(ax.c2p(*d["w_star"]))
    return ax, cont, star


class SGD(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.paths()
        self.monro()
        self.era()
        self.takeaway()

    def card(self):
        c = chapter_card(3, r"Stochastic gradients", r"Why use a noisy gradient on purpose?", part=PART)
        with self.voiceover("Chapter three. Stochastic gradients."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def idea(self):
        colors = {r"g_B": C.BITS, r"\nabla L": WHITE}
        eqs = VGroup(
            cmath(r"\nabla L(\theta)", "=", r"\frac{1}{n}\sum_{i=1}^{n} \nabla \ell_i(\theta)", font_size=38),
            cmath(r"g_B(\theta)", "=", r"\frac{1}{B}\sum_{i \in B} \nabla \ell_i(\theta)", colors=colors, font_size=38),
            cmath(r"\mathbb{E}\,g_B", "=", r"\nabla L", r",\qquad \operatorname{Cov} g_B = \frac{\Sigma}{B}", font_size=38),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([-2.6, 0.4, 0])
        notes = VGroup(label(r"the true gradient: \ every example, \ every step", font_size=22, color=GREY_A),
                       label(r"a random batch of $B$ examples: \ $n/B$ times cheaper", font_size=22, color=C.BITS),
                       label(r"right on average; \ noisy, \ less so for bigger batches", font_size=22, color=GREY_A))
        for n_, e_ in zip(notes, eqs):
            n_.next_to(e_, RIGHT, buff=0.4)
        VGroup(eqs, notes).move_to([0, 0.5, 0])
        keep_in_frame(VGroup(eqs, notes))
        hist = history_card(1951, r"Herbert Robbins \& Sutton Monro", r"\textit{A Stochastic Approximation Method}: \ "
                            r"find where a function is zero from noisy measurements of it", width=6.2)
        hist.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The loss of a model is an average over its training examples, and so is its gradient. Computing it "
            "exactly means going through all the data for every single step; real models train on trillions of "
            "words. <bookmark mark='a'/> Instead, average over a small random batch. <bookmark mark='b'/> On average "
            "that estimate is exactly right, and its noise shrinks as the batch grows: the covariance falls like one "
            "over B. <bookmark mark='c'/> Herbert Robbins and Sutton Monro, statisticians at North Carolina, asked "
            "in 1951 when steps along such noisy estimates still reach the answer."
        ) as vo:
            self.play(Write(eqs[0]), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Write(eqs[1]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(Write(eqs[2]), FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(FadeIn(hist, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def paths(self):
        d = load("noise")
        n = int(d["n"])
        ax, cont, star = loss_axes(d)
        names = VGroup(MathTex(r"w_{\text{the}}", font_size=26, color=GREY_A).next_to(ax, DOWN, buff=0.1),
                       MathTex(r"w_{\text{not}}", font_size=26, color=GREY_A).next_to(ax, LEFT, buff=0.1))
        full = np.asarray(d[f"path{n}"])
        p_full = VMobject(color=WHITE, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in full])
        p16 = VMobject(color=B_COLORS[16], stroke_width=2.2).set_points_as_corners([ax.c2p(*p) for p in np.asarray(d["path16"])])
        p1 = VMobject(color=B_COLORS[1], stroke_width=1.6).set_points_as_corners([ax.c2p(*p) for p in np.asarray(d["path1"])])
        key = VGroup(label(rf"all ${n}$ pages each step", font_size=26, color=WHITE),
                     label(r"$16$ random pages each step", font_size=26, color=B_COLORS[16]),
                     label(r"$1$ random page each step", font_size=26, color=B_COLORS[1]))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.9, 1.6, 0])
        head = label(r"Part 6's logistic regression, \ two weights: \ a real loss", font_size=26, color=GREY_A)
        head.next_to(key, UP, buff=0.4).align_to(key, LEFT)
        cost = label(rf"a step on $16$ pages costs $1/{n // 16}$ of a full one", font_size=24, color=C.BITS)
        cost.next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        same = label(r"$300$ steps each, \ the same step size", font_size=22, color=GREY_B).next_to(cost, DOWN, buff=0.3)
        same.align_to(key, LEFT)
        block = VGroup(head, key, cost, same)
        if block.get_right()[0] > 6.8:
            block.shift(LEFT * (block.get_right()[0] - 6.8))
        with self.voiceover(
            "Here's a real loss with two weights: part six's logistic regression, telling Austen from Dickens by "
            f"two word rates. <bookmark mark='a'/> With all {n} training pages, each step goes straight downhill. "
            "<bookmark mark='b'/> With sixteen random pages per step, the path wobbles, but each step costs "
            f"{n // 16} times less. <bookmark mark='c'/> With one page at a time it is wild, but it still heads for "
            "the bottom."
        ) as vo:
            self.play(Create(cont), FadeIn(star), FadeIn(names), FadeIn(head), FadeIn(same), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(p_full), FadeIn(key[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(p16), FadeIn(key[1]), FadeIn(cost), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(p1), FadeIn(key[2]), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def monro(self):
        d = load("noise")
        ax, cont, star = loss_axes(d, center=(-3.4, 0.2), width=5.6)
        w1, w2 = np.asarray(d["w1"]), np.asarray(d["w2"])

        def inside(P):
            P = np.asarray(P)
            return P[(P[:, 0] > w1[0]) & (P[:, 0] < w1[-1]) & (P[:, 1] > w2[0]) & (P[:, 1] < w2[-1])]

        cloud = VGroup(*[Dot(ax.c2p(*p), radius=0.022, color=B_COLORS[1], fill_opacity=0.6) for p in inside(d["cloud1"])])
        cl = label(r"one page a step, \ a constant step: \ it never settles", font_size=22, color=B_COLORS[1])
        cl.next_to(ax, DOWN, buff=0.15)
        conds = VGroup(cmath(r"\sum_k \eta_k = \infty", font_size=36), cmath(r"\sum_k \eta_k^2 < \infty", font_size=36))
        conds.arrange(RIGHT, buff=0.8).move_to([3.4, 2.7, 0])
        cn = VGroup(label(r"enough distance \\ to get anywhere", font_size=20, color=GREY_A).next_to(conds[0], DOWN, buff=0.15),
                    label(r"little enough noise \\ in total to settle", font_size=20, color=GREY_A).next_to(conds[1], DOWN, buff=0.15))
        eg = label(r"e.g. \ $\eta_k = \eta_0 / (1 + k/100)$", font_size=22, color=C.BITS).next_to(cn, DOWN, buff=0.25)
        rc, rd = np.asarray(d["rm_constant"]), np.asarray(d["rm_decay"])
        K = len(rc)
        ks = np.unique(np.round(np.geomspace(1, K, 160)).astype(int)) - 1
        lo = math.floor(np.log10(min(rc[ks].min(), rd[ks].min())))
        hi = math.ceil(np.log10(max(rc[ks].max(), rd[ks].max())))
        bx = CornerAxes(x_range=[0, math.log10(K), 1], y_range=[lo, hi, 1], x_length=5.4, y_length=2.9, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([3.5, -1.65, 0])
        xt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=18, color=GREY_B).next_to(bx.c2p(k, lo), DOWN, buff=0.08)
                      for k in range(0, int(math.log10(K)) + 1)])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=18, color=GREY_B).next_to(bx.c2p(0, k), LEFT, buff=0.08)
                      for k in range(lo, hi + 1)])
        yn = label(r"$|w - w^*|^2$, \ mean of $5$ runs", font_size=20, color=GREY_A).next_to(bx, UP, buff=0.08).align_to(bx, LEFT)
        c_const = curve(bx, np.log10(ks + 1), np.log10(rc[ks]), B_COLORS[1], 2.5)
        c_dec = curve(bx, np.log10(ks + 1), np.log10(rd[ks]), C.INTERVAL, 3)
        lg = VGroup(label(r"constant step", font_size=18, color=B_COLORS[1]), label(r"shrinking step", font_size=18,
                                                                                    color=C.INTERVAL))
        lg.arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(bx.c2p(0, lo), UR, buff=0.12)
        end_c, end_d = float(rc[-1000:].mean()), float(rd[-1000:].mean())
        better = end_d < end_c
        with self.voiceover(
            "Keep a constant step, and the walker never quite stops: it jiggles around the bottom forever, in a "
            "cloud. <bookmark mark='a'/> Robbins and Monro's answer: let the steps shrink, but not too fast. Their "
            "sum must be infinite, so the walker can still get anywhere; the sum of their squares must be finite, so "
            "the total noise it collects is finite. <bookmark mark='b'/> A step that shrinks like one over k does "
            "both. <bookmark mark='c'/> Measured: "
            + (f"with the constant step, the squared distance stalls at about {end_c:.3f}; with the shrinking step "
               f"it keeps falling, to {end_d:.4f} after {K:,} steps."
               if better else
               f"with the constant step the squared distance stalls near {end_c:.3f}; the shrinking step reaches "
               f"{end_d:.3f}, not yet below it after {K:,} steps.")
        ) as vo:
            self.play(Create(cont), FadeIn(star))
            self.play(LaggedStart(*[FadeIn(p) for p in cloud], lag_ratio=0.003), FadeIn(cl), run_time=2.0)
            vo.wait_until("a")
            self.play(Write(conds), FadeIn(cn))
            vo.wait_until("b")
            self.play(FadeIn(eg))
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(xt), FadeIn(yt), FadeIn(yn), FadeIn(lg))
            self.play(Create(c_const), Create(c_dec), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def era(self):
        h1 = history_card(1986, r"Rumelhart, Hinton \& Williams", r"backpropagation; \ every weight changed by "
                          r"$-\varepsilon\,\partial E/\partial w$ plus $\alpha$ times its last change: \ momentum",
                          width=5.4)
        h2 = history_card(1998, r"LeCun, Bottou, Orr \& M\"uller", r"\textit{Efficient BackProp}: \ update after every "
                          r"example, \ shuffle, \ normalize the inputs, \ a step size for each layer", width=5.4)
        h3 = history_card(2012, r"Krizhevsky, Sutskever \& Hinton", r"AlexNet: \ SGD, \ batch $128$, \ momentum $0.9$, \ "
                          r"weight decay $0.0005$, \ the step divided by $10$ when progress stalled", width=5.4)
        g = VGroup(h1, h2, h3).arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.35), cell_alignment=UL)
        g.move_to(DOWN * 0.15)
        head = label(r"the workhorse, \ 1986--2014", font_size=34).to_edge(UP, buff=0.3)
        rec = VGroup(cmath(r"v", r"\leftarrow", r"0.9\,v + g_B", font_size=34),
                     cmath(r"\theta", r"\leftarrow", r"\theta - \eta\,v", font_size=34)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rec.move_to(g[1].get_center() + g[2].get_center() - g[0].get_center() + DOWN * 0.3)
        rl = label(r"the recipe that trained \\ the first deep networks", font_size=22, color=C.BITS).next_to(rec, UP, buff=0.25)
        with self.voiceover(
            "This noisy method became the workhorse of neural networks. <bookmark mark='a'/> The 1986 "
            "backpropagation paper already trained with momentum. <bookmark mark='b'/> Yann LeCun, Leon Bottou and "
            "colleagues wrote down the practical craft in 1998: update after every example or small batch, "
            "shuffle the data, normalize the inputs. <bookmark mark='c'/> And in 2012 AlexNet, the network that started the deep learning boom, was "
            "trained by stochastic gradient descent with momentum zero point nine, dividing the step by ten whenever "
            "progress stalled."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rec), FadeIn(rl))
            vo.wait_until("a")
            self.play(FadeIn(h1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(h2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(h3, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        t = takeaway_card(r"Noisy steps are cheap, \ and they never quite settle",
                          r"A batch's gradient is right on average, with covariance $\Sigma/B$. \ At a constant step "
                          r"the walker ends in a cloud; \ steps that shrink like $1/k$ bring it home.",
                          r"Next: \ how big is the cloud, \ and what does the noise do?")
        with self.voiceover(
            "So a random batch gives a gradient that is right on average and cheap, at the price of noise. With a "
            "constant step, training ends in a cloud around the bottom. How big is that cloud, and is the noise only "
            "a cost?"
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
