from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import CONS, GRAD, HESS, PART, VALUE, load, matrix_heat


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def plane(xr, yr, h=TH - 0.2):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=h, tips=False,
                        axis_config={"stroke_color": GREY_D, "include_ticks": False})

        out = []
        # 1. the best straight line: error against step
        la = load("linapprox")
        a1 = plane([-4, -0.8, 1], [-8, 0, 2])
        hs = np.log10(np.asarray(la["hs"]))
        out.append((VGroup(a1, curve(a1, hs, np.log10(np.asarray(la["err"])), GRAD, 3),
                           curve(a1, hs, np.log10(np.asarray(la["err_bad"])), C.SURPRISE, 2)),
                    rf"best line: \ error $\sim h^{{{la['slope']:.2f}}}$", GRAD))
        # 2. the softmax Jacobian
        jc = load("jacobians")
        out.append((matrix_heat(np.asarray(jc["J_sm"]), cell=0.34), r"$\operatorname{diag}(p) - pp^\top$", GRAD))
        # 3. forward against reverse, counted
        md = load("modes")
        ratio = np.asarray(md["fwd"]) / np.asarray(md["rev"])
        out.append((matrix_heat(np.log10(ratio), cell=0.34, pos=VALUE, neg=GRAD), r"forward $n$, \ reverse $m$", VALUE))
        # 4. a rank-one gradient
        m2 = load("mlp2")
        out.append((matrix_heat(np.asarray(m2["dW1_0"]), cell=0.34), r"$\delta x^\top$: \ rank one", GRAD))
        # 5. the V-curve
        vc = load("vcurve")
        a5 = plane([-13, 0, 2], [-14, 0, 2])
        hv = np.log10(np.asarray(vc["hs"]))
        g5 = VGroup(a5)
        for k, col in (("fp64", C.TRUE_P), ("fp32", GRAD)):
            yv = np.asarray(vc[f"central_{k}"])
            ok = yv > 0
            g5.add(curve(a5, hv[ok], np.clip(np.log10(yv[ok]), -14, 0), col, 2.5))
        out.append((g5, r"the gradient check's V", C.TRUE_P))
        # 6. checkpoints
        ck = load("checkpoint")
        ks = np.asarray(ck["ks"])
        a6 = plane([0, math.log2(ck["n"]), 1], [0, ck["n"] + 10, 64])
        out.append((VGroup(a6, curve(a6, np.log2(ks), np.asarray(ck["peak"]), CONS, 3)),
                    rf"memory: \ $2\sqrt n$ at $k = \sqrt n$", CONS))
        # 7. the Hessian spectrum, trained
        he = load("hessian")
        nk = len(he["keep"]) - 1
        ev = np.sort(np.asarray(he[f"eig{nk}"]))
        sl = np.sign(ev) * np.log10(1 + np.abs(ev / ev.max()) / 1e-3) / 3.0
        a7 = plane([0, len(ev), 100], [-1, 1, 1])
        out.append((VGroup(a7, *[Dot(a7.c2p(i, float(v)), radius=0.015, color=HESS if v > 0.66 else GREY_B)
                                 for i, v in enumerate(sl)]),
                    rf"a flat bulk, \ ${he[f'nout{nk}']}$ steep directions", HESS))
        # 8. the support vector machine and its multipliers
        kk = load("kkt")
        X, y = np.asarray(kk["X"]), np.asarray(kk["y"])
        a8 = plane([-2.0, 2.5, 1], [-2.6, 2.8, 1])
        g8 = VGroup(*[Dot(a8.c2p(*p), radius=0.035, color=C.TRUE_P if c > 0 else GRAD) for p, c in zip(X, y)])
        g8.add(*[Circle(radius=0.09, color=CONS, stroke_width=2).move_to(a8.c2p(*X[i])) for i in kk["sv"]])
        out.append((g8, rf"KKT: \ ${len(kk['sv'])}$ support vectors", CONS))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, \ in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. A derivative is the best straight line, the one whose error shrinks faster than the "
            "step; a gradient, the steepest direction, by Cauchy–Schwarz; a Jacobian, the best matrix, and real "
            "layers' Jacobians are never formed, only multiplied. Forward mode pays per input and reverse mode per "
            "output, so training runs backwards: backpropagation, whose weight gradients are outer products of an "
            "error signal and an input. We built it, checked it and trained with it. Floats round and cancel, so "
            "softmaxes subtract their maximum and gradient checks pick their step. Checkpoints trade memory for "
            "time at the square root. Curvature sets the pace of descent, Hessian-vector products reach it "
            "cheaply, and a trained network's Hessian is mostly flat. Constraints bring multipliers, KKT and a dual "
            "problem, and an equation's solution can be differentiated without unrolling it."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"our library: \ backpropagation, \ XOR", [9]),
            (r"Jacobians through depth: \ vanishing and exploding", [9, 10]),
            (r"the condition number, \ saddles, \ momentum, \ Adam", [11]),
            (r"duality and support vectors", [6]),
            (r"the KL-regularized closed form", [27]),
            (r"number formats, \ checkpointing, \ quantization", [17, 18, 19]),
        ], font_size=24)
        with self.voiceover(
            "This is the engine of everything that follows. Our library trains the series' first neural networks in "
            "Part 9; Jacobians multiplied through depth decide whether deep networks can learn, in Parts 9 and 10; "
            "curvature, saddles and better optimizers fill Part 11; duality builds the support vector machine in Part "
            "6, and the closed form of chapter fifteen becomes direct preference optimization in Part 27; and number "
            "formats and memory come back in Parts 17 to 19."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Show that the softmax Jacobian $J = \operatorname{diag}(p) - pp^\top$ is positive semidefinite, with "
            r"$v^\top J v$ the variance of $v$ under $p$, \ and that $J\mathbf 1 = 0$.",
            r"A chain of $L$ dense layers of width $w$ maps $\mathbb R^n \to \mathbb R^m$. \ Count the multiply-adds "
            r"of its full Jacobian in forward and in reverse mode. \ When is each cheaper?",
            r"For the central difference with error $E(h) = \tfrac{h^2}{6}|f'''| + u|f|/h$, \ find $h^*$ and $E(h^*)$. "
            r"\ Do the same for the forward difference, \ and compare how each scales with $u$.",
            r"With a checkpoint every $k$ layers of $n$, memory is $n/k + k$. \ Show $k = \sqrt n$ is best; \ with "
            r"two levels of checkpoints, \ show memory $O(n^{1/3})$ is possible.",
            r"Gradient descent on $\tfrac12 x^\top H x$ with $\eta = 2/(\lambda_{\min} + \lambda_{\max})$: \ show the "
            r"error shrinks by $(\kappa - 1)/(\kappa + 1)$ per step, \ and about $\tfrac{\kappa}{2}\ln\tfrac1\epsilon$ "
            r"steps reach $\epsilon$.",
            r"Maximize $\mathbb E_\pi[r] - \beta\,\mathrm{KL}(\pi \,\|\, \pi_{\mathrm{ref}})$ over distributions $\pi$ "
            r"with a Lagrange multiplier, \ and show $\pi^* \propto \pi_{\mathrm{ref}}\, e^{r/\beta}$, \ with value "
            r"$\beta \log \textstyle\sum_a \pi_{\mathrm{ref}}(a)\, e^{r(a)/\beta}$.",
        ], font_size=21)
        with self.voiceover(
            "Here are six problems to try, from the softmax's Jacobian to reinforcement learning's closed form. "
            "Pause here and work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 5, \ Randomness in Motion", font_size=40).to_edge(UP, buff=0.35)
        g = np.random.default_rng(1827)
        paths = VGroup()
        for k in range(14):
            steps = g.normal(size=240) * 0.11
            ys = np.cumsum(steps)
            pts = [np.array([-5.5 + 11 * i / 239, yv, 0]) for i, yv in enumerate(ys)]
            paths.add(VMobject(color=interpolate_color(ManimColor(C.TRUE_P), ManimColor(C.BITS), k / 13),
                               stroke_width=2).set_points_as_corners(pts))
        paths.stretch_to_fit_height(min(paths.height, 4.6)).move_to(DOWN * 0.2)
        tag = label(r"random walks, \ illustrative; \ Robert Brown watched pollen jiggle in 1827", font_size=24,
                    color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Next time: randomness. Probability distributions that move, random walks that become Brownian motion, "
            "gradients that are only estimates, and the noise that diffusion models learn to undo. "
            "<bookmark mark='a'/> It's the last piece of mathematics we need before the models themselves."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.1), FadeIn(tag), run_time=3.0)
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"A.~Griewank \& A.~Walther, \textit{Evaluating Derivatives}, 2nd ed.\ (2008); \ M.~Blondel \& V.~Roulet, "
            r"\textit{The Elements of Differentiable Programming} (2024)",
            r"J.~Nocedal \& S.~J.~Wright, \textit{Numerical Optimization}, 2nd ed.\ (2006); \ S.~Boyd \& L.~Vandenberghe, "
            r"\textit{Convex Optimization} (2004)",
            r"N.~J.~Higham, \textit{Accuracy and Stability of Numerical Algorithms}, 2nd ed.\ (2002); \ I.~Goodfellow, "
            r"Y.~Bengio \& A.~Courville, \textit{Deep Learning} (2016)",
        ]
        papers = [
            r"Cauchy (1847); \ Karush (1939); \ Kuhn \& Tucker (1951); \ Jaynes (1957); \ Wengert (1964); \ "
            r"Linnainmaa (1970); \ Werbos (1974); \ Speelpenning (1980)",
            r"Rumelhart, Hinton \& Williams (1986); \ Griewank (1992); \ Pearlmutter (1994); \ Boser, Guyon \& Vapnik "
            r"(1992); \ IEEE 754 (1985); \ Goldberg, \textit{What Every Computer Scientist Should Know About "
            r"Floating-Point Arithmetic} (1991)",
            r"Bergstra et al., Theano (2010); \ Tokui et al., Chainer (2015); \ Abadi et al., TensorFlow (2016); \ "
            r"Paszke et al., PyTorch (2017, 2019); \ Frostig, Johnson \& Leary, JAX (2018); \ Baydin et al.\ (2018); \ "
            r"Karpathy, micrograd (2020)",
            r"Dauphin et al.\ (2014); \ Chen et al., \textit{Sublinear Memory Cost} (2016); \ Sagun, Bottou \& LeCun "
            r"(2016); \ Jin et al.\ (2017); \ Micikevicius et al., \textit{FP8 Formats for Deep Learning} (2022)",
            r"Amos \& Kolter, OptNet (2017); \ Bai, Kolter \& Koltun, \textit{Deep Equilibrium Models} (2019); \ "
            r"Rajeswaran et al., iMAML (2019)",
        ]
        card = reference_card(books, papers, font_size=19)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels). \ Every number on screen is computed by this "
                    r"part's code or cited; \ schematics and illustrations are labeled.", font_size=18).to_edge(DOWN, buff=0.2)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=18)
        credit.next_to(data, UP, buff=0.08)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.12:
            card.scale((card.height - (credit.get_top()[1] + 0.12 - card.get_bottom()[1])) / card.height)
            card.next_to(credit, UP, buff=0.12)
        with self.voiceover(
            "Griewank and Walther's Evaluating Derivatives is the book on automatic differentiation, and Blondel and "
            "Roulet's Elements of Differentiable Programming is the modern one. Thanks for watching, and see you in "
            "Part 5."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
