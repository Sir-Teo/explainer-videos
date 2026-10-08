from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import Plot, bar_rows, calc, eval_curve, label, load, note, num_table, source

A_NS, B_NS, C_NS = 3.4445, -4.7750, 2.0315


def ns_poly(x):
    return A_NS * x + B_NS * x**3 + C_NS * x**5


def valley_paths(n=60):
    """Gradient descent vs Adam on an elongated quadratic f = (25 x^2 + y^2) / 2 (computed, not drawn)."""
    def grad(p):
        return np.array([25 * p[0], p[1]])
    start = np.array([-1.0, 2.6])
    sgd, p = [start.copy()], start.copy()
    for _ in range(n):
        p = p - 0.075 * grad(p)
        sgd.append(p.copy())
    adam, p = [start.copy()], start.copy()
    m = v = np.zeros(2)
    b1, b2, lr = 0.9, 0.99, 0.12
    for t in range(1, n + 1):
        g = grad(p)
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        p = p - lr * (m / (1 - b1**t)) / (np.sqrt(v / (1 - b2**t)) + 1e-8)
        adam.append(p.copy())
    return np.array(sgd), np.array(adam)


class Optimizer(VoiceoverScene):
    def construct(self):
        self.adam()
        self.adam_math()
        self.spectrum()
        self.newton_schulz()
        self.ns_math()
        self.race()
        self.adoption()

    # ------------------------------------------------------------------
    def adam(self):
        ax = Axes(x_range=[-1.3, 1.3, 1], y_range=[-1.0, 3.0, 1], x_length=7.5, y_length=5.2,
                  axis_config={"include_ticks": False, "stroke_color": GREY_D}).move_to(LEFT * 2.2 + DOWN * 0.3)
        levels = VGroup()
        for c in [0.05, 0.2, 0.6, 1.4, 2.6, 4.2, 6.5]:
            pts = [ax.c2p(np.sqrt(2 * c / 25) * np.cos(t), np.sqrt(2 * c) * np.sin(t)) for t in np.linspace(0, 2 * PI, 120)]
            levels.add(VMobject(stroke_color=GREY_C, stroke_width=1.2).set_points_smoothly(pts))
        sgd, adam = valley_paths()
        ps = VMobject(stroke_color=C.PENALTY, stroke_width=3).set_points_as_corners([ax.c2p(*q) for q in sgd[:40]])
        pa = VMobject(stroke_color=C.ADAMW, stroke_width=4).set_points_as_corners([ax.c2p(*q) for q in adam[:40]])
        start = Dot(ax.c2p(*sgd[0]), color=WHITE)
        goal = Dot(ax.c2p(0, 0), color=YELLOW, radius=0.07)
        ls = label(r"plain gradient descent", font_size=26, color=C.PENALTY)
        la = label(r"Adam: each coordinate's step\\divided by its typical size", font_size=26, color=C.ADAMW)
        VGroup(ls, la).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(RIGHT * 4.0 + UP * 1.0)
        head = label(r"The optimizer turns a gradient into a step", font_size=36).to_edge(UP, buff=0.35)
        mem = label(r"AdamW (2017): Adam + decoupled weight decay,\\the default for most of a decade", font_size=26, color=GREY_A).next_to(la, DOWN, buff=0.6).align_to(la, LEFT)
        tag = note(r"computed on $f = \tfrac12(25x^2 + y^2)$").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Next, the optimizer: the rule that turns each gradient into an update. Plain gradient descent steps "
            "straight downhill, <bookmark mark='s'/> and in a long, narrow valley it zigzags across the steep walls "
            "while creeping along the floor. <bookmark mark='a'/> Adam fixes this one coordinate at a time: it keeps "
            "running averages of each parameter's gradient and squared gradient, and divides one by the square root "
            "of the other, so every coordinate moves at a similar speed. <bookmark mark='w'/> With decoupled weight "
            "decay, AdamW has been the default for most of a decade."
        ) as vo:
            self.play(FadeIn(head), Create(levels), FadeIn(start), FadeIn(goal), FadeIn(tag))
            vo.wait_until("s")
            self.play(Create(ps), FadeIn(ls), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(pa), FadeIn(la), run_time=2.5)
            vo.wait_until("w")
            self.play(FadeIn(mem))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def adam_math(self):
        b1, b2, eps = 0.9, 0.95, 1e-8  # the betas our runs use

        def adam(gs):
            m = v = 0.0
            out = []
            for t, g in enumerate(gs, 1):
                m = b1 * m + (1 - b1) * g
                v = b2 * v + (1 - b2) * g * g
                mh, vh = m / (1 - b1**t), v / (1 - b2**t)
                out.append((mh, np.sqrt(vh), mh / (np.sqrt(vh) + eps)))
            return out
        big, small = [4.0, 5.0, 3.0], [0.04, 0.05, 0.03]
        A, Bs = adam(big), adam(small)
        assert all(abs(a[2] - b[2]) < 1e-5 for a, b in zip(A, Bs)) and round(A[-1][2], 3) == 0.974
        eqs = calc(r"m_t &= \beta_1\, m_{t-1} + (1-\beta_1)\, g_t", r"\\ v_t &= \beta_2\, v_{t-1} + (1-\beta_2)\, g_t^2",
                   r"\\ \Delta\theta &= -\eta\,\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon},\qquad "
                   r"\hat m_t = \frac{m_t}{1-\beta_1^t},\ \hat v_t = \frac{v_t}{1-\beta_2^t}", font_size=32)
        eqs.to_edge(UP, buff=0.4).set_x(0)
        betas = MathTex(r"\beta_1 = 0.9,\ \beta_2 = 0.95", font_size=26, color=GREY_A).next_to(eqs, DOWN, buff=0.15)
        f = lambda x: f"{x:.3g}"  # noqa: E731
        rows = [[str(t + 1), f(gb), f(a[0]), f(a[1]), rf"{a[2]:.3f}", f(gs), f(b[0]), f(b[1]), rf"{b[2]:.3f}"]
                for t, (gb, gs, a, b) in enumerate(zip(big, small, A, Bs))]
        tab = num_table([r"t", r"g", r"\hat m", r"\sqrt{\hat v}", r"\hat m/\sqrt{\hat v}",
                         r"g", r"\hat m", r"\sqrt{\hat v}", r"\hat m/\sqrt{\hat v}"], rows, font_size=28,
                        col_colors=[GREY_A, C.GRADS, WHITE, WHITE, C.ADAMW, C.GRADS, WHITE, WHITE, C.ADAMW])
        tab.next_to(betas, DOWN, buff=0.55).set_x(0)
        c1 = VGroup(*tab.cols[1:5])
        c2 = VGroup(*tab.cols[5:9])
        g1 = label(r"parameter 1: big gradients", font_size=24, color=C.GRADS).next_to(c1, UP, buff=0.2)
        g2 = label(r"parameter 2: 100$\times$ smaller", font_size=24, color=C.GRADS).next_to(c2, UP, buff=0.2)
        hi = VGroup(*[SurroundingRectangle(VGroup(tab.rows[i][4], tab.rows[i][8]), buff=0.06, color=C.ADAMW, stroke_width=0)
                      for i in range(3)])
        box1 = SurroundingRectangle(tab.cols[4][1:], buff=0.1, color=C.ADAMW, stroke_width=2)
        box2 = SurroundingRectangle(tab.cols[8][1:], buff=0.1, color=C.ADAMW, stroke_width=2)
        tag = label(r"same step for both: Adam divides out the gradient's scale", font_size=28, color=C.ADAMW)
        tag.next_to(tab, DOWN, buff=0.45)
        wd = MathTex(r"\text{AdamW also shrinks every weight: } \theta \leftarrow \theta - \eta\lambda\theta", font_size=28,
                     color=GREY_A).next_to(tag, DOWN, buff=0.25)
        del hi
        with self.voiceover(
            "Here's Adam in equations. It keeps a running average of the gradient, m, <bookmark mark='v'/> and of "
            "the squared gradient, v. <bookmark mark='u'/> The step is m divided by the square root of v, after a "
            "correction for the averages starting at zero. <bookmark mark='t'/> Run it on two parameters: one with "
            "gradients around four, one with gradients a hundred times smaller. <bookmark mark='r'/> The averages "
            "differ by a factor of a hundred, but their ratio doesn't: after three steps both parameters move by "
            "0.974 learning rates. <bookmark mark='w'/> AdamW adds one more term, shrinking every weight slightly, "
            "kept separate from the gradient step."
        ) as vo:
            self.play(Write(eqs[0]), FadeIn(betas))
            vo.wait_until("v")
            self.play(Write(eqs[1]))
            vo.wait_until("u")
            self.play(Write(eqs[2]))
            vo.wait_until("t")
            self.play(FadeIn(tab.header), Create(tab.rule), FadeIn(g1), FadeIn(g2))
            for r in tab.rows:
                self.play(LaggedStart(*[FadeIn(c) for c in r], lag_ratio=0.06), run_time=0.9)
            vo.wait_until("r")
            self.play(Create(box1), Create(box2), FadeIn(tag))
            vo.wait_until("w")
            self.play(FadeIn(wd))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectrum(self):
        d = load("muon_svd")
        g = np.asarray(d["grad_sv"], float)
        g = g / g.max()
        n = len(g)
        assert d["shape"] == [336, 128] and n == 128
        top5 = (g[:5] ** 2).sum() / (g**2).sum()
        self.top5 = top5
        assert 0.6 < top5 < 0.72 and 35 < 1 / np.median(g) < 65
        plot = Plot(x_range=(0, n), y_range=(1e-3, 1.5), width=9.0, height=3.8, log_y=True, x_ticks=[1, 32, 64, 96, 128],
                    y_ticks=[1e-3, 1e-2, 1e-1, 1], x_label=r"direction (singular vector), largest first",
                    y_label=r"size of the gradient along it", y_fmt=lambda v: MathTex(rf"10^{{{int(round(np.log10(v)))}}}", font_size=24, color=GREY_A))
        plot.move_to(DOWN * 0.5)
        bars = VGroup(*[Line(plot.c2p(i + 0.5, 1e-3), plot.c2p(i + 0.5, max(1e-3, v)), stroke_width=3.2, color=C.GRADS)
                        for i, v in enumerate(g)])
        flat = VGroup(*[Line(plot.c2p(i + 0.5, 1e-3), plot.c2p(i + 0.5, 1.0), stroke_width=3.2, color=C.MUON) for i in range(n)])
        head = label(r"A real gradient: one $336\times128$ weight matrix of our pocket model", font_size=32).to_edge(UP, buff=0.35)
        svd = MathTex(r"G = U\,\Sigma\,V^{\top} \quad\longrightarrow\quad U V^{\top}", font_size=40).next_to(head, DOWN, buff=0.25)
        svd[0][0:6].set_color(C.GRADS)
        lt = label(rf"top 5 of 128 directions: {100 * top5:.0f}\% of the gradient", font_size=26, color=C.GRADS)
        lt.next_to(plot.c2p(60, 0.6), RIGHT, buff=0.1)
        lm = label(r"Muon: every direction gets the same size step", font_size=26, color=C.MUON)
        lm.next_to(svd, DOWN, buff=0.12).align_to(plot, RIGHT)
        with self.voiceover(
            "A newer optimizer, Muon, treats each weight matrix as a whole. A matrix's gradient can be broken into "
            "directions, its singular vectors, each with a size. <bookmark mark='g'/> Here are the sizes for a real "
            "gradient from one of our pocket models, on a log scale. A handful of directions dominate: the top five, "
            "out of 128, carry about two thirds of it, while a typical direction is some fifty times smaller than the largest. <bookmark mark='m'/> Muon keeps the directions but sets every size to one: each direction gets an "
            "equal step."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot))
            vo.wait_until("g")
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.01), run_time=2.0)
            self.play(FadeIn(lt))
            vo.wait_until("m")
            self.play(FadeIn(svd), ReplacementTransform(bars, flat), FadeOut(lt), FadeIn(lm), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def newton_schulz(self):
        d = load("muon_svd")
        ns = np.asarray(d["ns_sv"], float)  # (6, 128): after normalization, then after each iteration
        assert ns.shape[0] == 6 and ns[-1].min() > 0.3 and ns[-1].max() < 1.3
        plot = Plot(x_range=(0, 1.25), y_range=(0, 1.4), width=6.0, height=4.6, x_ticks=[0, 0.5, 1], y_ticks=[0, 0.5, 1],
                    x_label=r"singular value in", y_label=r"out")
        plot.move_to(LEFT * 3.4 + DOWN * 0.4)
        xs = np.linspace(0, 1.2, 300)
        curve = plot.line(xs, ns_poly(xs), color=C.MUON, stroke_width=4)
        diag = plot.line([0, 1.25], [0, 1.25], color=GREY_D, stroke_width=1.5)
        poly = MathTex(r"p(\sigma) = 3.4445\,\sigma - 4.7750\,\sigma^3 + 2.0315\,\sigma^5", font_size=30, color=C.MUON)
        poly.to_edge(UP, buff=0.4)
        mat = MathTex(r"X \leftarrow aX + (bA + cA^2)X,\quad A = XX^{\top}", font_size=30).next_to(poly, DOWN, buff=0.2)
        exact = VGroup(MathTex(r"G = U\,\Sigma\,V^{\top} \;\longrightarrow\; U V^{\top}", font_size=44),
                       label(r"exact, but needs a singular value decomposition: slow on GPUs", font_size=26, color=GREY_A)
                       ).arrange(DOWN, buff=0.3)
        exact[0][0][0:6].set_color(C.GRADS)
        why = label(r"(a matrix polynomial acts on each singular value: no SVD needed)", font_size=22, color=GREY_A).next_to(mat, DOWN, buff=0.12)
        line = NumberLine(x_range=[0, 1.3, 0.25], length=5.4, include_numbers=False, color=GREY_C).move_to(RIGHT * 3.4 + DOWN * 2.5)
        nums = VGroup(*[MathTex(f"{v:g}", font_size=22, color=GREY_A).next_to(line.n2p(v), DOWN, buff=0.12) for v in [0, 0.5, 1]])
        rng = np.random.default_rng(0)
        jit = rng.uniform(-0.9, 0.9, ns.shape[1])

        def dots_at(k):
            return VGroup(*[Dot(line.n2p(min(1.29, v)) + UP * (1.6 + 0.45 * j), radius=0.035, color=C.MUON if k else C.GRADS)
                            for v, j in zip(ns[k], jit)])
        dots = dots_at(0)
        it = VGroup(label(r"iteration", font_size=24, color=GREY_A), Integer(0, font_size=28)).arrange(RIGHT, buff=0.15)
        it.next_to(line, UP, buff=2.9)
        lo, hi = ns[-1].min(), ns[-1].max()
        band = label(rf"after 5 iterations: all between {lo:.1f} and {hi:.1f}", font_size=24, color=C.MUON).next_to(line, DOWN, buff=0.6)
        assert round(lo, 1) == 0.6 and round(hi, 1) == 1.2
        with self.voiceover(
            "Computing that exactly would need a singular value decomposition, which is slow on GPUs. Muon's trick "
            "is a polynomial. <bookmark mark='p'/> Multiplying a matrix by itself in this pattern applies the same "
            "polynomial to every singular value at once, <bookmark mark='i'/> and the coefficients are chosen so that "
            "five rounds push every value toward one. <bookmark mark='d'/> Here are the real singular values of our "
            "gradient, scaled below one, going through five iterations: small ones are lifted fast, any that overshoot "
            "are pulled back, and all of them end up between about 0.6 and 1.2."
        ) as vo:
            self.play(FadeIn(exact))
            vo.wait_until("p")
            self.play(FadeOut(exact), FadeIn(poly), FadeIn(mat), FadeIn(why))
            vo.wait_until("i")
            self.play(FadeIn(plot), Create(diag), Create(curve), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(line), FadeIn(nums), FadeIn(dots), FadeIn(it))
            for k in range(1, 6):
                self.play(Transform(dots, dots_at(k)), it[1].animate.set_value(k), run_time=1.0)
            self.play(FadeIn(band))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ns_math(self):
        start = [0.9, 0.3, 0.03]
        hist = []
        for s0 in start:
            row, x = [s0], s0
            for _ in range(5):
                x = ns_poly(x)
                row.append(x)
            hist.append(row)
        hist = np.array(hist)
        assert round(hist[2, 1], 3) == 0.103 and 0.65 < hist[:, -1].min() and hist[:, -1].max() < 1.15
        one = calc(r"p(0.03) &= 3.4445(0.03) - 4.7750(0.03)^3 + 2.0315(0.03)^5",
                   r"\\ &= 0.1033 - 0.0001 + 0.0000 = 0.103", font_size=32)
        one.to_edge(UP, buff=0.5).set_x(0)
        rows = [[rf"{v:.3f}" for v in r] for r in hist]
        tab = num_table([r"\sigma_0", r"p(\sigma)", r"p^{2}", r"p^{3}", r"p^{4}", r"p^{5}"], rows, font_size=32,
                        col_colors=[C.GRADS] + [C.MUON] * 5)
        tab.next_to(one, DOWN, buff=0.7).set_x(0)
        band = SurroundingRectangle(tab.cols[5][1:], buff=0.12, color=C.MUON, stroke_width=2)
        bt = label(rf"all end between {hist[:, -1].min():.2f} and {hist[:, -1].max():.2f}: roughly equal, which is all Muon needs",
                   font_size=26, color=C.MUON).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Here is that arithmetic for three of them. Take a singular value of 0.03. One application of the "
            "polynomial is mostly the first term: 3.4445 times 0.03, minus a tiny cubic correction, gives 0.103. "
            "<bookmark mark='t'/> Apply it again: 0.35, then 1.01. A value that starts at 0.9 overshoots and "
            "oscillates instead. <bookmark mark='e'/> But after five rounds, all three sit between 0.68 and 1.12. "
            "They aren't exactly one, and they don't need to be: roughly equal steps in every direction is the whole "
            "point."
        ) as vo:
            self.play(Write(one[0]))
            self.play(Write(one[1]))
            vo.wait_until("t")
            self.play(FadeIn(tab.header), Create(tab.rule), FadeIn(tab.cols[0][1:]))
            for k in range(1, 6):
                self.play(FadeIn(tab.cols[k][1:], shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until("e")
            self.play(Create(band), FadeIn(bt))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        res = load("optim")
        a, m = res["opt_adamw"], res["opt_muon"]
        _, ta, va = eval_curve(a)
        _, tm, vm = eval_curve(m)
        assert a["run"]["decay_frac"] == m["run"]["decay_frac"] and a["run"]["tokens"] == m["run"]["tokens"]
        decay_at = (1 - a["run"]["decay_frac"]) * ta[-1]

        def muon_tokens_to(loss):  # tokens Muon needed to first reach `loss` (linear between evals)
            i = int(np.argmax(vm <= loss))
            f = (vm[i - 1] - loss) / (vm[i - 1] - vm[i])
            return tm[i - 1] + f * (tm[i] - tm[i - 1])
        # compare while both learning rates are still at their peak (before the cooldown)
        stable = [(t, v) for t, v in zip(ta, va) if 1e6 <= t <= decay_at]
        ratios = np.array([muon_tokens_to(v) / t for t, v in stable])
        t_ref, l_ref = stable[-1]
        t_mu = muon_tokens_to(l_ref)
        frac = t_mu / t_ref
        self.frac = frac
        assert (vm < va).all() and ratios.max() < 0.7 and 0.6 < frac < 0.67
        assert np.isfinite(va).all() and np.isfinite(vm).all()
        plot = Plot(x_range=(0, ta[-1] / 1e6), y_range=(3.4, 6.0), width=9.0, height=4.4,
                    x_ticks=[0, 3, 6, 9, 12], y_ticks=[3.5, 4.0, 4.5, 5.0, 5.5, 6.0],
                    x_label=r"training tokens (millions)", y_label=r"validation loss")
        plot.move_to(DOWN * 0.4 + LEFT * 0.6)
        cool = Polygon(plot.c2p(decay_at / 1e6, 3.4), plot.c2p(ta[-1] / 1e6, 3.4), plot.c2p(ta[-1] / 1e6, 6.0),
                       plot.c2p(decay_at / 1e6, 6.0), stroke_width=0, fill_color=C.LR, fill_opacity=0.12)
        cool_t = label(r"learning rate\\lowered", font_size=20, color=C.LR).move_to(plot.c2p((decay_at + ta[-1]) / 2e6, 5.6))
        la = plot.line(ta / 1e6, np.minimum(va, 6.0), color=C.ADAMW, stroke_width=4)
        lm = plot.line(tm / 1e6, np.minimum(vm, 6.0), color=C.MUON, stroke_width=4)
        ka = label(rf"AdamW {va[-1]:.2f}", font_size=24, color=C.ADAMW).next_to(plot.c2p(ta[-1] / 1e6, va[-1]), RIGHT, buff=0.1)
        km = label(rf"Muon {vm[-1]:.2f}", font_size=24, color=C.MUON).next_to(plot.c2p(tm[-1] / 1e6, vm[-1]), RIGHT, buff=0.1)
        pa = Dot(plot.c2p(t_ref / 1e6, l_ref), radius=0.08, color=C.ADAMW)
        pm = Dot(plot.c2p(t_mu / 1e6, l_ref), radius=0.08, color=C.MUON)
        arr = Arrow(pa.get_center(), pm.get_center(), buff=0.1, color=WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        ht = label(rf"same loss with {100 * frac:.0f}\% of the tokens", font_size=24).move_to(plot.c2p(3.4, 3.7))
        head = label(r"Same model, same data, two optimizers (real runs, $\approx$1M parameters)", font_size=30).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Does it help? Here's our pocket model trained twice on the same data, once with AdamW and once with "
            "Muon, each with the better of the learning rates we tried in short test runs. <bookmark mark='r'/> Muon "
            "pulls ahead early and stays ahead. <bookmark mark='h'/> While the learning rate is held at its peak, Muon "
            "reaches these losses with roughly two thirds of the tokens AdamW needs. <bookmark mark='d'/> At the "
            "end, both learning rates are lowered and both losses drop, which is the subject of the next chapter. "
            f"Muon finishes at {vm[-1]:.2f}, AdamW at {va[-1]:.2f}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot))
            vo.wait_until("r")
            self.play(Create(la), Create(lm), run_time=3.0)
            vo.wait_until("h")
            self.play(FadeIn(pa), FadeIn(pm), GrowArrow(arr), FadeIn(ht))
            vo.wait_until("d")
            self.play(FadeIn(cool), FadeIn(cool_t))
            self.play(FadeIn(ka), FadeIn(km))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def adoption(self):
        head = label(r"From a speedrun trick to frontier models", font_size=34).to_edge(UP, buff=0.35)
        src = source(r"Jordan et al.\ 2024; Liu et al.\ arXiv 2502.16982; Kimi K2 report; GLM-4.5 report; DeepSeek-V4 report; "
                     r"Wen et al.\ arXiv 2509.02046")
        x0, x1, y = -6.0, 6.0, 1.3
        t0, t1 = 2024.7, 2026.8

        def X(t):
            return x0 + (x1 - x0) * (t - t0) / (t1 - t0)
        axis = Line([x0, y, 0], [x1, y, 0], color=GREY_C, stroke_width=2)
        years = VGroup(*[VGroup(Line([X(t), y - 0.08, 0], [X(t), y + 0.08, 0], color=GREY_C, stroke_width=2),
                                label(str(t), font_size=22, color=GREY_A).next_to([X(t), y, 0], DOWN, buff=0.15))
                         for t in (2025, 2026)])
        events = [  # (date, label, above?)
            (2024.85, r"modded-nanoGPT\\speedrun", True),
            (2025.13, r"\textbf{Moonlight}: about half\\the FLOPs of AdamW", False),
            (2025.53, r"\textbf{Kimi K2}: MuonClip,\\1T parameters", True),
            (2025.57, r"\textbf{GLM-4.5}", False),
            (2026.29, r"\textbf{DeepSeek-V4}", True),
            (2026.53, r"\textbf{Kimi K3}", False),
        ]
        marks = VGroup()
        for t, txt, up in events:
            d = Dot([X(t), y, 0], radius=0.08, color=C.MUON)
            stem = Line([X(t), y, 0], [X(t), y + (0.55 if up else -0.75), 0], color=C.MUON, stroke_width=1.5)
            lab = label(txt, font_size=22).next_to(stem, UP if up else DOWN, buff=0.08)
            marks.add(VGroup(stem, d, lab))
        speed = 1 / self.frac
        assert 1.5 < speed < 1.7
        bars = bar_rows([(r"our pocket model, $\approx$1M parameters (lightly tuned)", speed - 1, C.MUON, rf"{speed:.1f}$\times$"),
                         (r"0.1B parameters (Wen et al.)", 0.4, GREY_B, r"1.4$\times$"),
                         (r"1.2B parameters (Wen et al.)", 0.1, GREY_B, r"1.1$\times$")],
                        5.0, font_size=22, bar_h=0.3, buff=0.14)
        bt = label(r"Muon's speed-up over AdamW (tokens to reach the same loss), bar = gain above 1$\times$", font_size=22,
                   color=GREY_A).next_to(bars, UP, buff=0.15).align_to(bars, LEFT)
        cav = VGroup(bt, bars).to_edge(DOWN, buff=0.6).set_x(0)
        with self.voiceover(
            "Muon began in 2024 as a trick for a community speedrun of small GPT models. <bookmark mark='m'/> In "
            "2025, Moonshot showed it scales, needing about half the training compute of AdamW, <bookmark mark='k'/> "
            "and trained the trillion-parameter Kimi K2 with it. <bookmark mark='g'/> By 2026, Zhipu's GLM models, "
            "DeepSeek-V4 and Kimi K3 all use Muon variants. <bookmark mark='c'/> One caveat: a careful 2025 "
            "benchmark found the speed-up shrinks as models grow, from 1.4 times at a hundred million parameters to "
            f"1.1 times at 1.2 billion. <bookmark mark='o'/> Our tiny model's {speed:.1f} fits that trend, though our tuning "
            "was far lighter. Optimizer gains are real, but they're hard to measure at scale."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(axis), FadeIn(years))
            self.play(FadeIn(marks[0]))
            vo.wait_until("m")
            self.play(FadeIn(marks[1]))
            vo.wait_until("k")
            self.play(FadeIn(marks[2]))
            vo.wait_until("g")
            self.play(LaggedStart(*[FadeIn(m) for m in marks[3:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(bt), *[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in bars[1:]])
            vo.wait_until("o")
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
        self.wait(0.4)
        self.clear_scene()
