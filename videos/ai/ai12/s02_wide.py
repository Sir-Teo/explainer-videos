from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import FIT, HIST, LAZY, PART, RICH, load


class Wide(VoiceoverScene):
    def construct(self):
        self.card()
        self.gaussian()
        self.kernel()
        self.measure()

    def card(self):
        card = chapter_card(1, r"Infinitely wide", r"What does a network compute when it is infinitely wide?",
                            part=PART)
        with self.voiceover("Chapter one. Infinitely wide."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def gaussian(self):
        g = load("nngp")
        widths = [int(w) for w in g["widths"]]
        show = [w for w in widths if w in (1, 2, 8, 512)] or widths[:4]
        var = float(g["var_theory"])
        x = float(g["x"])
        panels = VGroup()
        for w in show:
            f = np.asarray(g[f"draws{w}"])
            edges = np.linspace(-3.6, 3.6, 37)
            h, _ = np.histogram(f, bins=edges, density=True)
            ax = Axes(x_range=[-3.6, 3.6, 1.8], y_range=[0, 0.9, 0.3], x_length=2.7, y_length=1.7, tips=False,
                      axis_config={"stroke_color": GREY_D, "include_ticks": False})
            bars = VGroup(*[Rectangle(width=ax.c2p(edges[1], 0)[0] - ax.c2p(edges[0], 0)[0], height=max(1e-3, ax.c2p(0, min(v, 0.9))[1]
                                      - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=LAZY, fill_opacity=0.75)
                            .move_to(ax.c2p((a + b) / 2, 0), aligned_edge=DOWN) for a, b, v in zip(edges, edges[1:], h)])
            xs = np.linspace(-3.6, 3.6, 120)
            pdf = curve(ax, xs, np.exp(-xs ** 2 / (2 * var)) / math.sqrt(2 * math.pi * var), C.BITS, 2.5, smooth=True)
            kurt = float(g["kurt"][str(w)])
            t = label(rf"$n = {w}$", font_size=24, color=WHITE).next_to(ax, UP, buff=0.1)
            k = label(rf"excess kurtosis ${kurt:.1f}$", font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.1)
            panels.add(VGroup(ax, bars, pdf, t, k))
        panels.arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.55)
        formula = MathTex(r"f(x) = \frac{1}{\sqrt{n}} \sum_{j=1}^{n} a_j \,\mathrm{relu}(u_j x + c_j)", font_size=34)
        formula.move_to([-3.4, -0.95, 0])
        fl = label(r"$a_j, u_j, c_j$ \ drawn at random, \ $\mathcal{N}(0, 1)$", font_size=22, color=GREY_A)
        fl.next_to(formula, DOWN, buff=0.2)
        cap = label(rf"the output at $x = {x}$ \ over ${len(np.asarray(g[f'draws{show[0]}'])):,}$ random starts; \ "
                    rf"yellow: \ the Gaussian of variance $(x^2 + 1)/2 = {var:.3f}$".replace(",", "{,}"), font_size=20,
                    color=GREY_B).next_to(panels, DOWN, buff=0.15)
        # five functions drawn by a wide random network: samples of a Gaussian process
        xs, S = np.asarray(g["xs"]), np.asarray(g["samples"])
        sx = Axes(x_range=[-1, 1, 0.5], y_range=[-2.6, 2.6, 1.3], x_length=4.4, y_length=2.3, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([3.6, -1.75, 0])
        samples = VGroup(*[curve(sx, xs, np.clip(y, -2.6, 2.6), c, 2.5, smooth=True)
                           for y, c in zip(S, ["#7FD3FF", C.BITS, C.MODEL_Q, C.INTERVAL, C.CONTEXT])])
        sl = label(r"five random networks, $n = 2{,}000$: \\ samples of a Gaussian process", font_size=20, color=GREY_A)
        sl.next_to(sx, UP, buff=0.1)
        hc = history_card(1994, r"Radford Neal", r"an infinitely wide one-layer network, with random weights, "
                          r"is a Gaussian process \ (\textit{Bayesian Learning for Neural Networks}, 1996)",
                          width=5.6, color=HIST).scale(0.85).move_to([-3.4, -2.75, 0])
        with self.voiceover(
            "Start a network with random weights, and ask what it computes. One hidden layer of n units; each "
            "unit's output is weighted by a random number, and the sum is divided by the square root of n. "
            "<bookmark mark='a'/> With one unit, the output at one point, over thousands of random starts, is lumpy "
            "and heavy-tailed. <bookmark mark='b'/> With many units it is a sum of many independent terms, and part "
            "five's central limit theorem takes over: a Gaussian, with exactly the variance the formula predicts. "
            "<bookmark mark='c'/> Not just at one point: the whole function becomes a Gaussian process, a random "
            "smooth curve whose covariance, a kernel, is fixed by the architecture. Radford Neal saw this in 1994; "
            "in 2018 it was extended to deep networks."
        ) as vo:
            self.play(Write(formula), FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]), FadeIn(cap))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in panels[1:]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(sx), FadeIn(sl), LaggedStart(*[Create(c_) for c_ in samples], lag_ratio=0.2), run_time=2.0)
            self.play(FadeOut(formula), FadeOut(fl), FadeIn(hc, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kernel(self):
        dfn = definition_card(r"the neural tangent kernel",
                              r"$\Theta(x, x') = \nabla_\theta f(x) \cdot \nabla_\theta f(x')$: \ how much a step "
                              r"that changes the output at $x'$ also changes it at $x$", width=6.2, font_size=22,
                              color=LAZY)
        dfn.to_corner(UL, buff=0.35)
        colors = {r"\Theta": LAZY}
        rows = [
            cmath(r"\dot\theta", r"=", r"-\tfrac{\eta}{m} \sum_i \nabla_\theta f(x_i)\,\big(f(x_i) - y_i\big)", font_size=34),
            cmath(r"\dot f(x)", r"=", r"\nabla_\theta f(x) \cdot \dot\theta", font_size=34),
            cmath(r"\dot f(x)", r"=", r"-\tfrac{\eta}{m} \sum_i", r"\Theta", r"(x, x_i)\,\big(f(x_i) - y_i\big)",
                  font_size=34, colors=colors),
            cmath(r"f_\infty(x)", r"=", r"f_0(x) +", r"\Theta", r"(x, X)\,", r"\Theta", r"(X, X)^{-1}\big(y - f_0(X)\big)",
                  font_size=34, colors=colors),
        ]
        whys = [why(r"gradient descent, \ squared error"), why(r"chain rule"), why(r"definition of $\Theta$"),
                why(r"if $\Theta$ stays fixed: \ a linear equation, \ solved")]
        step = ladder(self, rows, whys, keep=4, top=0.75, x=-1.0, buff=0.42, edge=6.8)
        lin = label(r"$\Theta$ fixed $\Rightarrow$ \ training is kernel regression \ (Part 6), \ with this kernel",
                    font_size=24, color=LAZY).to_edge(DOWN, buff=0.35)
        cite_ = cite(r"A.~Jacot, F.~Gabriel \& C.~Hongler, \textit{Neural Tangent Kernel} (2018)", corner=UR)
        with self.voiceover(
            "That is the network before training. In 2018, Arthur Jacot, Franck Gabriel and Clément Hongler asked "
            "what happens during it. <bookmark mark='a'/> Gradient descent moves the weights along the gradient of "
            "the error. <bookmark mark='b'/> By the chain rule, the output at any point x moves by its own gradient "
            "times that step. <bookmark mark='c'/> Put the two together and one object appears: the dot product of "
            "the gradients at two inputs, the neural tangent kernel. It says how much a step that fixes the output "
            "at one input also moves it at another. <bookmark mark='d'/> If the kernel stays put, this is a linear "
            "equation, and its solution is kernel regression, part six's method, with this kernel. Their theorem: "
            "as the width goes to infinity, the kernel does stay put."
        ) as vo:
            self.play(FadeIn(dfn, shift=UP * 0.1), FadeIn(cite_))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(lin))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        z = load("ntk")
        W = np.asarray(z["widths"], float)
        mh, km = np.asarray(z["moved_hidden"]), np.asarray(z["kernel_moved"])
        sw, sk = float(z["slope_moved_hidden"]), float(z["slope_kernel_moved"])
        lw = np.log10(W)
        allv = np.log10(np.concatenate([mh.ravel(), km.ravel()]))
        y0, y1 = math.floor(allv.min()) - 0.1, math.ceil(allv.max() * 2) / 2 + 0.1
        ax = CornerAxes(x_range=[1.3, 4.7, 1], y_range=[y0, y1, 1], x_length=5.2, y_length=4.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-3.6, -0.55, 0])
        xt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(v, y0), DOWN, buff=0.1)
                      for t, v in ((r"10^2", 2), (r"10^3", 3), (r"10^4", 4))])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax.c2p(1.3, k), LEFT, buff=0.08)
                      for k in range(math.ceil(y0), math.floor(y1) + 1)])
        xn = label(r"width $n$", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(r"relative change in training", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)

        def series(M, col):
            pts = VGroup(*[Dot(ax.c2p(a, math.log10(v)), radius=0.045, color=col) for a, row in zip(lw, M) for v in row])
            line = curve(ax, lw, np.log10(M.mean(1)), col, 3)
            return VGroup(line, pts)

        s_w, s_k = series(mh, RICH), series(km, LAZY)
        lg = VGroup(label(rf"the weights: \ slope ${sw:.2f}$", font_size=22, color=RICH),
                    label(rf"the kernel $\Theta$: \ slope ${sk:.2f}$", font_size=22, color=LAZY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        lg.next_to(ax.c2p(1.3, y0), UR, buff=0.15)
        half = label(r"theory: \ $n^{-1/2}$", font_size=22, color=GREY_B).next_to(lg, UP, buff=0.15).align_to(lg, LEFT)
        seeds = note(r"three seeds per width").next_to(ax, DOWN, buff=0.75).align_to(ax, LEFT)
        # the trained function against its linearization, at two widths, replayed through training
        X, y = np.asarray(z["X"]), np.asarray(z["y"])
        grid = np.asarray(z["grid"])
        steps = [int(v) for v in z["snap_steps"]]
        pans = VGroup()
        lives = []
        for k, n in enumerate((100, 10000)):
            px = Axes(x_range=[-1, 1, 0.5], y_range=[-2.2, 2.2, 1.1], x_length=4.6, y_length=1.9, tips=False,
                      axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([3.5, 1.35 - 2.85 * k, 0])
            pts = VGroup(*[Dot(px.c2p(a, b), radius=0.05, color=WHITE) for a, b in zip(X, y)])
            fl = DashedVMobject(curve(px, grid, np.clip(np.asarray(z[f"flin_{n}"]), -2.2, 2.2), LAZY, 3, smooth=True),
                                num_dashes=50)
            t = label(rf"$n = {n:,}$".replace(",", "{,}"), font_size=22, color=WHITE).next_to(px, UP, buff=0.05).align_to(px, LEFT)
            pans.add(VGroup(px, pts, fl, t))
            lives.append((px, np.asarray(z[f"snaps_{n}"]), np.asarray(z[f"fT_{n}"])))
        gap100, gap10k = float(np.asarray(z["lin_gap"])[list(W).index(100)].mean()), float(np.asarray(z["lin_gap"])[-1].mean())
        key = VGroup(label(r"the network, \ through training", font_size=20, color=RICH),
                     label(r"its linearization (dashed)", font_size=20, color=LAZY)).arrange(RIGHT, buff=0.4)
        key.next_to(pans, DOWN, buff=0.12)
        lazy_ok = -0.75 < sk < -0.3
        said1 = (
            "Both close to minus a half. Each of the n weights moves by about one over the square root of n: too "
            "little to change what any unit computes, yet together enough to move the output. "
            if lazy_ok else
            "Both shrink with width, though not exactly at the rate of one over root n the theory predicts at "
            "infinite width. "
        )
        with self.voiceover(
            "Check it, on that one-layer network, trained by gradient descent on ten points, at widths from thirty "
            "to thirty thousand. <bookmark mark='a'/> Measure how far the weights travel, relative to where they "
            f"started: the slope is {sw:.2f}. <bookmark mark='b'/> And how far the kernel moves: slope {sk:.2f}. "
            + said1
            + "<bookmark mark='c'/> So a wide network trains like its own linearization. At a hundred units, the "
            f"trained function strays from the linear prediction by up to {gap100:.2f}; at ten thousand, by "
            f"{gap10k:.2f}."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(seeds))
            vo.wait_until("a")
            self.play(Create(s_w[0]), FadeIn(s_w[1]), FadeIn(lg[0]))
            vo.wait_until("b")
            self.play(Create(s_k[0]), FadeIn(s_k[1]), FadeIn(lg[1]), FadeIn(half))
            vo.wait_until("c")
            self.play(*[FadeIn(p) for p in pans], FadeIn(key))
            nets = [curve(px, grid, np.clip(S[0], -2.2, 2.2), RICH, 3, smooth=True) for px, S, _ in lives]
            self.play(*[Create(c_) for c_ in nets])
            for t in range(1, len(steps)):
                new = [curve(px, grid, np.clip(S[t], -2.2, 2.2), RICH, 3, smooth=True) for px, S, _ in lives]
                self.play(*[Transform(a_, b_) for a_, b_ in zip(nets, new)], run_time=0.7)
            new = [curve(px, grid, np.clip(fT, -2.2, 2.2), RICH, 3, smooth=True) for px, _, fT in lives]
            self.play(*[Transform(a_, b_) for a_, b_ in zip(nets, new)], run_time=0.7)
        self.wait(0.3)
        self.clear_scene()
