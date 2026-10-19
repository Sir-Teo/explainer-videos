from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import DECAY, K, Q, STATE, V, curve, load


def bucket_picture() -> VGroup:
    """A state-space model as a leaky bucket: the input pours in, the level leaks slowly away, the level is read."""
    w_top, w_bot, h = 1.3, 1.0, 1.3
    wall = VMobject(color=GREY_A, stroke_width=3).set_points_as_corners(
        [[-w_top / 2, h / 2, 0], [-w_bot / 2, -h / 2, 0], [w_bot / 2, -h / 2, 0], [w_top / 2, h / 2, 0]])
    lvl = 0.15  # the water's top, in the bucket's coordinates
    f = (lvl + h / 2) / h
    w_lvl = w_bot + (w_top - w_bot) * f
    water = Polygon([-w_bot / 2, -h / 2, 0], [w_bot / 2, -h / 2, 0], [w_lvl / 2, lvl, 0], [-w_lvl / 2, lvl, 0],
                    stroke_width=0, fill_color=STATE, fill_opacity=0.7)
    pour = Arrow([-0.15, h / 2 + 0.7, 0], [-0.15, lvl + 0.05, 0], buff=0, color=K, stroke_width=4,
                 max_tip_length_to_length_ratio=0.15)
    pl = label(r"input $x$ pours in", font_size=20, color=K).next_to(pour, RIGHT, buff=0.12).shift(UP * 0.35)
    leak = Arrow([w_bot / 2 - 0.05, -h / 2 + 0.12, 0], [w_bot / 2 + 0.6, -h / 2 - 0.15, 0], buff=0, color=DECAY,
                 stroke_width=3, max_tip_length_to_length_ratio=0.25)
    ll = label(r"slowly leaks", font_size=20, color=DECAY).next_to(leak, RIGHT, buff=0.1)
    tick = DashedLine([-w_lvl / 2 - 0.35, lvl, 0], [-w_lvl / 2 - 0.05, lvl, 0], color=STATE, stroke_width=2)
    hl = label(r"the level $h$: \\ what you read", font_size=20, color=STATE).next_to(tick, LEFT, buff=0.1)
    return VGroup(water, wall, pour, pl, leak, ll, tick, hl)


class SSM(VoiceoverScene):
    def construct(self):
        self.card()
        self.continuous()
        self.selective()
        self.duality()

    def card(self):
        card = chapter_card(4, r"State-space models", r"Can a memory choose what to keep?", part=15)
        with self.voiceover("Chapter four. State-space models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def continuous(self):
        s = load("ssm")
        t = np.asarray(s["t"], float)
        deltas = [float(v) for v in s["deltas"]]
        colors = {r"h": STATE, r"x": K, r"y": Q, r"\Delta": DECAY}
        f1 = cmath(r"h'(t)", "=", r"A\,", r"h", r"(t) + B\,", r"x", r"(t)", r",\qquad", r"y", r"(t) = C\,", r"h", r"(t)",
                   colors=colors, font_size=38).to_edge(UP, buff=0.4)
        f2 = cmath(r"h", r"_t", "=", r"e^{", r"\Delta", r"A}\,", r"h", r"_{t-1}", "+", r"\Delta", r"\,B\,", r"x", r"_t",
                   colors=colors, font_size=38).next_to(f1, DOWN, buff=0.35)
        f2l = label(r"read in steps of size $\Delta$", font_size=22, color=GREY_A).next_to(f2, RIGHT, buff=0.3)
        ax = Axes(x_range=[0, t[-1], 20], y_range=[0, 1.05, 0.5], x_length=7.4, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-1.6, -1.7, 0])
        xn = label(r"tokens since an input", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yn = label(r"how much of it the state still holds", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        cols = [C.SURPRISE, C.BITS, C.INTERVAL]
        cs = VGroup(*[curve(ax, t, np.asarray(s[f"imp{dt:g}"]), c_, 3.5) for dt, c_ in zip(sorted(deltas, reverse=True), cols)])
        ks = VGroup(*[label(rf"$\Delta = {dt:g}$", font_size=24, color=c_) for dt, c_ in zip(sorted(deltas, reverse=True), cols)])
        ks.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, -1.4, 0])
        cite_ = cite(r"A.~Gu, K.~Goel \& C.~R\'e, \textit{S4} (2022)", corner=DR)
        # the equation at work: a leaky state, pushed by two pulses of input (A = -1, B = C = 1)
        tt = np.linspace(0, 10, 400)
        xin = ((tt > 1) & (tt < 1.6)).astype(float) + 0.7 * ((tt > 4.5) & (tt < 5.1))
        hh = np.zeros_like(tt)
        for i in range(1, len(tt)):
            hh[i] = hh[i - 1] + (tt[i] - tt[i - 1]) * (-hh[i - 1] + 1.6 * xin[i - 1])
        bx = Axes(x_range=[0, 10, 2], y_range=[0, 1.1, 0.5], x_length=8.0, y_length=2.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-0.6, -1.0, 0])
        kx = label(r"input $x(t)$", font_size=24, color=K)
        kh = label(r"state $h(t)$: \\ rises, then leaks away", font_size=24, color=STATE)
        bx.shift(LEFT * 0.8)
        VGroup(kx, kh).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(bx, RIGHT, buff=0.4)
        keep_in_frame(VGroup(kx, kh))
        lx = VMobject(color=K, stroke_width=3).set_points_as_corners([bx.c2p(a_, b_) for a_, b_ in zip(tt, xin)])
        lh = VMobject(color=STATE, stroke_width=4).set_points_smoothly([bx.c2p(a_, b_) for a_, b_ in zip(tt[::4], hh[::4])])
        bl = note(r"illustrative: \ $A = -1$").next_to(bx, DOWN, buff=0.15).align_to(bx, LEFT)
        dot = glow_dot(bx.c2p(0, 0), color=STATE, radius=0.08)
        bucket = gloss(r"state-space model", r"a leaky bucket: input pours in, the level slowly \\ leaks away, "
                       r"and you read the level", bucket_picture(), width=4.6, color=STATE).to_corner(UR, buff=0.3)
        bucket.shift(DOWN * 1.0)
        with self.voiceover(
            "A different road to the same place started in control theory. A state-space model is a differential "
            "equation: a hidden state h that evolves, pushed by the input x, read out as y. <bookmark mark='l'/> "
            "Picture a leaky bucket: the input pours in, the level slowly leaks away, and the level is what you "
            "read. <bookmark mark='a'/> "
            "Read a text in steps of size delta, and it becomes a recurrence: shrink the state, add the input. "
            "<bookmark mark='b'/> The step size sets the memory. Small steps, and an input lingers for a long time; "
            "large steps, and it's gone in a few tokens."
        ) as vo:
            self.play(Write(f1), FadeIn(cite_))
            vo.wait_until("l")
            self.play(FadeIn(bucket, shift=UP * 0.2))
            self.play(Create(bx), Create(lx), FadeIn(kx), FadeIn(bl), run_time=1.2)
            self.play(Create(lh), MoveAlongPath(dot, lh.copy()), FadeIn(kh), run_time=3.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeOut(bucket), Write(f2), FadeIn(f2l))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(bx, lx, lh, kx, kh, bl, dot)))
            self.play(Create(ax), FadeIn(xn), FadeIn(yn))
            self.play(LaggedStart(*[Create(c_) for c_ in cs], lag_ratio=0.4), FadeIn(ks), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def selective(self):
        s = load("ssm")
        u, fx, sel = np.asarray(s["u"]), np.asarray(s["fixed"]), np.asarray(s["selective"])
        marks = [int(m) for m in s["mark"]]
        T = len(u)
        ax = Axes(x_range=[0, T, 20], y_range=[-2.5, 2.5, 1], x_length=10.0, y_length=2.0, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        ins = ax.copy().move_to(UP * 1.4)
        a1, a2 = ax.copy().move_to(DOWN * 0.8), ax.copy().move_to(DOWN * 0.8)
        dots = VGroup(*[Dot(ins.c2p(i, u[i]), radius=0.045 if i not in marks else 0.1,
                            color=C.BITS if i in marks else GREY_B) for i in range(T)])
        il = label(r"the input: \ noise, \ and two marked values", font_size=22, color=GREY_A).next_to(ins, UP, buff=0.05)
        il.align_to(ins, LEFT)
        cf = curve(a1, np.arange(T), fx, C.SURPRISE, 3)
        csel = curve(a2, np.arange(T), sel, C.INTERVAL, 3.5)
        hl = label(r"the state", font_size=22, color=GREY_A).next_to(a1, UP, buff=0.05).align_to(a1, LEFT)
        k1 = label(r"fixed step: \ the marked value fades into the noise", font_size=24, color=C.SURPRISE).to_edge(DOWN, buff=0.9)
        k2 = label(r"selective step, \ set by each input: \ large on marked values, \ tiny on noise", font_size=24,
                   color=C.INTERVAL).to_edge(DOWN, buff=0.4)
        cite_ = cite(r"A.~Gu \& T.~Dao, \textit{Mamba} (2023)", corner=UR)
        with self.voiceover(
            "But a fixed step size can't tell what matters. Here's an input stream of noise with two marked values "
            "worth remembering. <bookmark mark='a'/> With a fixed step, each marked value washes out in the noise "
            "that follows. <bookmark mark='b'/> Mamba's idea, in 2023, was to let each input choose its own step "
            "size: a big step to take in something important, almost no step at all for noise, so the state holds "
            "still. Now the state keeps the marked value until the next one replaces it. A memory that chooses."
        ) as vo:
            self.play(FadeIn(ins), FadeIn(il), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.005), FadeIn(cite_),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(a1), FadeIn(hl), Create(cf), FadeIn(k1), run_time=2.5)
            vo.wait_until("b")
            self.play(cf.animate.set_stroke(opacity=0.3), Create(csel), FadeIn(k2), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def duality(self):
        rows = [
            (r"linear attention", r"S_t = S_{t-1} + v_t k_t^{\top}", C.SURPRISE),
            (r"Mamba-2, \ RetNet, \ GLA", r"S_t = a_t\,S_{t-1} + v_t k_t^{\top}", DECAY),
            (r"DeltaNet", r"S_t = S_{t-1} + \beta_t (v_t - S_{t-1}k_t)\,k_t^{\top}", C.INTERVAL),
            (r"Gated DeltaNet, \\ Kimi Delta Attention", r"S_t = a_t\,S_{t-1} + \beta_t (v_t - a_t S_{t-1}k_t)\,k_t^{\top}", C.BITS),
        ]
        g = VGroup()
        for i, (n, f, c_) in enumerate(rows):
            y = 1.6 - i * 1.05
            g.add(VGroup(label(n, font_size=26, color=c_).move_to([-2.4, y, 0], aligned_edge=RIGHT),
                         MathTex(f, font_size=32).move_to([-2.1, y, 0], aligned_edge=LEFT)))
        keep_in_frame(g)
        head = label(r"one matrix memory, \ four ways to write to it \ (read: \ $\mathrm{out}_t = S_t\,q_t$)", font_size=28)
        head.to_edge(UP, buff=0.4)
        foot = label(r"Mamba-2: \ a selective state-space model \emph{is} linear attention with a decay", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.6)
        cite_ = cite(r"T.~Dao \& A.~Gu, \textit{Transformers are SSMs} (2024); \ S.~Yang, J.~Kautz \& A.~Hatamizadeh, "
                     r"\textit{Gated Delta Networks} (2025)", corner=DR)
        with self.voiceover(
            "In 2024, Mamba-2 showed the two roads meet. A selective state-space model is linear attention with a "
            "decay: its input matrix plays the key, its output matrix the query. <bookmark mark='a'/> So today's "
            "fast memories are one family: a matrix that's read with a query, and written by one of a few rules. "
            "Add; decay then add; correct with the delta rule; or decay and correct, the gated delta rule of Qwen3-Next "
            "and Kimi Linear."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g[0]), FadeIn(g[1]), FadeIn(foot), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(FadeIn(g[2], shift=RIGHT * 0.2), FadeIn(g[3], shift=RIGHT * 0.2), lag_ratio=0.5),
                      run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
