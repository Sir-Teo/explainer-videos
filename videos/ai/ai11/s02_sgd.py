from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import load

B_COLORS = {1: C.SURPRISE, 16: C.BITS}
PUSH, KICK = C.TRUE_P, C.NEURAL  # the SDE's two parts


class SGD(VoiceoverScene):
    def construct(self):
        self.card()
        self.paths()
        self.sde()

    def card(self):
        card = chapter_card(1, r"Stochastic gradient descent", r"Why use a noisy gradient on purpose?", part=11)
        with self.voiceover("Chapter one. Stochastic gradient descent."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def axes(self, d):
        w1, w2 = np.asarray(d["w1"]), np.asarray(d["w2"])
        ax = Axes(x_range=[w1[0], w1[-1], 0.5], y_range=[w2[0], w2[-1], 0.5], x_length=6.6, y_length=6.6 * (w2[-1] - w2[0]) / (w1[-1] - w1[0]) * 0.75,
                  tips=False, axis_config={"stroke_width": 0}).move_to([-2.8, -0.3, 0])
        L = np.asarray(d["L"])

        def f(x, y):
            i = int(np.clip(np.searchsorted(w2, y), 1, len(w2) - 1))
            j = int(np.clip(np.searchsorted(w1, x), 1, len(w1) - 1))
            return float(L[i, j])

        lmin = float(L.min())
        cont = contour_lines(ax, f, (w1[0], w1[-1]), (w2[0], w2[-1]), list(lmin + np.array([0.003, 0.01, 0.025, 0.05, 0.09, 0.15, 0.22, 0.32, 0.45])),
                             n=(120, 140), stroke_width=1.4)
        return ax, cont

    # ------------------------------------------------------------------
    def paths(self):
        d = load("noise")
        n = int(d["n"])
        ax, cont = self.axes(d)
        star = Star(n=5, outer_radius=0.12, color=WHITE, fill_opacity=1).move_to(ax.c2p(*d["w_star"]))
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
        head = label(r"Part 6's logistic regression, \ two weights: \ the real loss", font_size=26, color=GREY_A)
        head.next_to(key, UP, buff=0.4).align_to(key, LEFT)
        cost = label(r"one step on $16$ pages costs $1/28$ of a full step", font_size=24, color=C.BITS)
        cost.next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        block = VGroup(head, key, cost)
        if block.get_right()[0] > 6.8:  # keep the column inside the frame
            block.shift(LEFT * (block.get_right()[0] - 6.8))
        with self.voiceover(
            "Computing the exact gradient means going through all the training data, for every single step. Real "
            "models train on trillions of words; nobody can afford that. <bookmark mark='a'/> Here's a real loss "
            "with two weights: part six's logistic regression on two word rates. With the whole dataset, each step "
            "goes straight downhill. <bookmark mark='b'/> Instead, estimate the gradient from a small random batch. "
            "Sixteen pages: the path wobbles, but it's twenty-eight times cheaper per step. <bookmark mark='c'/> One "
            "page at a time: wild, but still it gets there."
        ) as vo:
            self.play(Create(cont), FadeIn(star), FadeIn(names), FadeIn(head), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(p_full), FadeIn(key[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(p16), FadeIn(key[1]), FadeIn(cost), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(p1), FadeIn(key[2]), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sde(self):
        d = load("noise")
        ax, cont = self.axes(d)
        star = Star(n=5, outer_radius=0.12, color=WHITE, fill_opacity=1).move_to(ax.c2p(*d["w_star"]))
        w1, w2 = np.asarray(d["w1"]), np.asarray(d["w2"])

        def inside(P):
            P = np.asarray(P)
            return P[(P[:, 0] > w1[0]) & (P[:, 0] < w1[-1]) & (P[:, 1] > w2[0]) & (P[:, 1] < w2[-1])]

        c1 = VGroup(*[Dot(ax.c2p(*p), radius=0.025, color=B_COLORS[1], fill_opacity=0.6) for p in inside(d["cloud1"])])
        c16 = VGroup(*[Dot(ax.c2p(*p), radius=0.025, color=B_COLORS[16], fill_opacity=0.8) for p in inside(d["cloud16"])])
        sde = cmath(r"d\theta", "=", r"-\nabla L(\theta)\,dt", "+", r"\sqrt{\eta / B}", r"\;\Sigma^{1/2}\,dW_t",
                    colors={r"-\nabla L(\theta)\,dt": PUSH, r"\sqrt{\eta / B}": KICK, r"\;\Sigma^{1/2}\,dW_t": KICK},
                    font_size=38).move_to([3.6, 2.4, 0])
        parts = VGroup(brace_note(term(sde, r"-\nabla L(\theta)\,dt"), r"push downhill", color=PUSH, font_size=20),
                       brace_note(VGroup(term(sde, r"\sqrt{\eta / B}"), term(sde, r"\;\Sigma^{1/2}\,dW_t")), r"random kick",
                                  color=KICK, font_size=20))
        sn = label(r"Part 5's equation: \ a push downhill, \ plus noise", font_size=24, color=GREY_A).next_to(parts, DOWN, buff=0.15)
        sn.set_x(3.6)
        sp1, sp16 = float(d["spread1"]), float(d["spread16"])
        ratio = sp1 / sp16
        nums = VGroup(label(rf"batch $1$: \ spread ${sp1:.2f}$", font_size=26, color=B_COLORS[1]),
                      label(rf"batch $16$: \ spread ${sp16:.2f}$ \ \ ($\approx 1/\sqrt{{16}}$: \ ${1 / ratio:.2f}\times$)",
                            font_size=26, color=B_COLORS[16]))
        nums.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(sn, DOWN, buff=0.5).set_x(3.6)
        flat = label(r"the noise keeps it out of sharp, narrow holes: \\ it settles where the valley is wide",
                     font_size=26, color=C.BITS).next_to(nums, DOWN, buff=0.5).set_x(3.6)
        cite_ = cite(r"Q.~Li, C.~Tai \& W.~E (2017); \ S.~Mandt, M.~Hoffman \& D.~Blei (2017)", corner=DR)
        assert 2.5 < ratio < 6

        # a sharp pit beside a wide basin (illustrative), and a jiggling ball that hops out of the pit
        def land(x):
            return 0.95 - 0.8 * np.exp(-((x + 1.3) / 0.16) ** 2) - 0.75 * np.exp(-((x - 0.9) / 0.7) ** 2) + 0.04 * x * x

        lx0, ly0, sx, sy = 3.6, -3.05, 1.25, 1.3

        def lp(x, lift=0.0):
            return np.array([lx0 + sx * x, ly0 + sy * land(x) + lift, 0])

        lcurve = VMobject(color=GREY_A, stroke_width=3).set_points_smoothly([lp(x) for x in np.linspace(-2.3, 2.3, 140)])
        lsharp = label(r"sharp", font_size=20, color=C.SURPRISE).next_to(lp(-1.3), DOWN, buff=0.1)
        lwide = label(r"wide", font_size=20, color=C.INTERVAL).next_to(lp(0.9), DOWN, buff=0.1)
        hops = [-1.3, -1.22, -1.4, -1.18, -1.45, -1.05, -0.6, -0.1, 0.45, 0.8, 1.05, 0.85, 1.0, 0.9]
        ball = Dot(lp(hops[0], 0.09), radius=0.09, color=WHITE)
        with self.voiceover(
            "Keep going, and the walker never quite stops. It jiggles around the bottom forever, in a cloud. "
            "<bookmark mark='a'/> That's part five's stochastic differential equation: a push downhill, plus random "
            "kicks whose size grows with the learning rate and shrinks with the batch. <bookmark mark='b'/> Sixteen "
            f"times the batch, and the cloud is about {ratio:.0f} times narrower: one over the square root of sixteen. "
            "<bookmark mark='c'/> The noise isn't only a cost. Picture a sharp minimum, a narrow pit, beside a wide "
            "one, a broad basin. A jiggling walker can't stay in the narrow pit, so it "
            "tends to settle where the valley is wide, and wide minima tend to work better on new data."
        ) as vo:
            self.play(FadeIn(cont), FadeIn(star))
            self.play(LaggedStart(*[FadeIn(p) for p in c1], lag_ratio=0.003), run_time=2.0)
            vo.wait_until("a")
            self.play(Write(sde), FadeIn(cite_))
            self.play(FadeIn(parts), FadeIn(sn))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in c16], lag_ratio=0.003), FadeIn(nums), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(flat), Create(lcurve), FadeIn(lsharp), FadeIn(lwide), FadeIn(ball))
            self.play(Succession(*[ball.animate(run_time=0.3, rate_func=smooth).move_to(lp(x, 0.09)) for x in hops[1:]]))
        self.wait(0.3)
        self.clear_scene()
