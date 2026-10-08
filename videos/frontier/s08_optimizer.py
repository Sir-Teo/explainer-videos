from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import Plot, eval_curve, label, load, note, source

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
        self.spectrum()
        self.newton_schulz()
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
        assert (vm < va).all() and ratios.max() < 2 / 3 and 0.6 < frac < 0.66
        assert round(va[-1], 2) == 3.80 and round(vm[-1], 2) == 3.61
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
            "reaches any given loss with less than two thirds of the tokens AdamW needs. <bookmark mark='d'/> At the "
            "end, both learning rates are lowered and both losses drop, which is the subject of the next chapter. "
            "Muon finishes at 3.61, AdamW at 3.80."
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
        items = VGroup(
            label(r"\textbf{Moonlight} (Feb 2025): Muon scaled up; about half the training FLOPs of AdamW", font_size=27),
            label(r"\textbf{Kimi K2} (Jul 2025): MuonClip, 1T parameters, 15.5T tokens, ``zero loss spike''", font_size=27),
            label(r"\textbf{GLM-4.5 / GLM-5}, \textbf{DeepSeek-V4} (Apr 2026), \textbf{Kimi K3}: Muon variants", font_size=27),
            label(r"\textbf{Caveat}: with carefully tuned baselines, the speed-up shrinks with scale:", font_size=27, color=GREY_A),
            label(r"$1.4\times$ at 0.1B parameters, $1.1\times$ at 1.2B (Wen et al., 2025)", font_size=27, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.2)
        items[3].shift(DOWN * 0.25)
        items[4].shift(DOWN * 0.25 + RIGHT * 0.4)
        head = label(r"From a speedrun trick to frontier models", font_size=36).to_edge(UP, buff=0.5)
        src = source(r"Jordan et al.\ 2024; Liu et al.\ arXiv 2502.16982; Kimi K2 report; DeepSeek-V4 report; Wen et al.\ arXiv 2509.02046")
        with self.voiceover(
            "Muon began in 2024 as a trick for a community speedrun of small GPT models. In 2025, Moonshot showed it "
            "scales, needing about half the training compute of AdamW, and trained the trillion-parameter Kimi K2 "
            "with it. By 2026, Zhipu's GLM models, DeepSeek-V4 and Kimi K3 all use Muon variants. <bookmark mark='c'/> "
            "One caveat: a careful 2025 benchmark found the speed-up shrinks as models grow, from 1.4 times at a "
            "hundred million parameters to 1.1 times at 1.2 billion. Optimizer gains are real, but they're hard to "
            "measure at scale."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items[:3]], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(items[3]), FadeIn(items[4]))
        self.wait(0.4)
        self.clear_scene()
