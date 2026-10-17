from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import A, K, Q, STATE, V, curve, grid_matrix, load, vec_column


def block(w, h, color, tex, font_size=34):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.18)
    return VGroup(r, MathTex(tex, font_size=font_size, color=color).move_to(r))


class Linear(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.reorder()
        self.recurrence()
        self.cost()

    def card(self):
        card = chapter_card(2, r"Attention without the softmax", r"Can attention run in constant memory?", part=12)
        with self.voiceover("Chapter two. Attention without the softmax."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def reorder(self):
        T, d = 3.0, 0.9  # drawn sizes: T tokens long, d numbers wide
        q, kt, v = block(d, T, Q, r"Q"), block(T, d, K, r"K^{\top}"), block(d, T, V, r"V")
        left = VGroup(q, kt, v).arrange(RIGHT, buff=0.25).move_to([-3.2, 0.6, 0])
        qk = block(T, T, A, r"QK^{\top}", 36).move_to([-3.6, 0.6, 0])
        q2, kt2, v2 = block(d, T, Q, r"Q"), block(T, d, K, r"K^{\top}"), block(d, T, V, r"V")
        right = VGroup(q2, kt2, v2).arrange(RIGHT, buff=0.25).move_to([3.4, 0.6, 0])
        kv = block(d, d, STATE, r"K^{\!\top}\!V", 26).move_to(right.get_center() + RIGHT * 0.6)
        lt = label(r"$(QK^{\top})\,V$: \ a $T\times T$ table", font_size=26, color=A).next_to(left, DOWN, buff=0.6)
        rt = label(r"$Q\,(K^{\top}V)$: \ a $d\times d$ table", font_size=26, color=STATE).next_to(right, DOWN, buff=0.6)
        same = label(r"the same answer, \ by associativity \ $\dots$ \ if there is no softmax in between", font_size=28,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        top = cmath(r"\mathrm{softmax}(QK^{\top})\,V", r"\;\longrightarrow\;", r"\phi(Q)\,\phi(K)^{\top}\,V",
                    font_size=38, colors={r"\mathrm{softmax}(QK^{\top})\,V": A}).to_edge(UP, buff=0.4)
        cite_ = cite(r"A.~Katharopoulos et al., \textit{Transformers are RNNs} (2020)", corner=DR)
        with self.voiceover(
            "Here's attention for a whole text of T tokens: queries times keys, then times values. <bookmark mark='a'/> "
            "The product of queries and keys is a T by T table of scores: it grows with the square of the length. "
            "<bookmark mark='b'/> But matrix products can be grouped either way. Multiply keys and values first, and "
            "the table in the middle is only d by d, however long the text. <bookmark mark='c'/> The catch is the "
            "softmax: it sits between Q K and V, and blocks the regrouping. Replace it with simple positive features "
            "of the queries and keys, and you're allowed: that's linear attention."
        ) as vo:
            self.play(FadeIn(left))
            vo.wait_until("a")
            self.play(ReplacementTransform(VGroup(q, kt), qk), v.animate.next_to(qk, RIGHT, buff=0.25), FadeIn(lt))
            vo.wait_until("b")
            self.play(FadeIn(right))
            self.play(ReplacementTransform(VGroup(kt2, v2), kv), q2.animate.next_to(kv, LEFT, buff=0.25), FadeIn(rt))
            self.play(FadeIn(same))
            vo.wait_until("c")
            self.play(Write(top), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recurrence(self):
        lin = load("linear")
        n = 6
        g = np.random.default_rng(7)
        words = "a cat sat on the mat".split()
        steps, S_vals = [], np.zeros((n, n))
        for _ in words:
            kk, vv = g.normal(size=n), g.normal(size=n)
            S_vals = S_vals + np.outer(vv, kk)
            steps.append((kk, vv, S_vals.copy()))
        top = max(np.abs(st[2]).max() for st in steps)
        cell = 0.42

        def tower(S_):
            """The state as a field of bars: one per number, up for positive, down for negative."""
            grp = VGroup()
            for i in range(n):
                for j in range(n):
                    h = float(S_[i, j] / top * 1.6)
                    b = Prism(dimensions=[cell * 0.82, cell * 0.82, max(abs(h), 0.02)], fill_opacity=0.9, stroke_width=0.3,
                              stroke_color="#0E1117")
                    b.set_fill(C.TRUE_P if h >= 0 else C.SURPRISE)
                    b.move_to([(j - (n - 1) / 2) * cell, ((n - 1) / 2 - i) * cell, h / 2])
                    grp.add(b)
            return grp.shift(LEFT * 2.6 + DOWN * 0.4)

        base = Square(n * cell, stroke_color=GREY_C, stroke_width=1.5).move_to(LEFT * 2.6 + DOWN * 0.4)
        cur = tower(np.zeros((n, n)))
        colors = {r"S_t": STATE, r"S_{t-1}": STATE, r"v_t": V, r"k_t": K, r"q_t": Q}
        f1 = cmath(r"S_t", "=", r"S_{t-1}", "+", r"v_t", r"\,", r"k_t", r"^{\top}", colors=colors, font_size=40)
        f2 = cmath(r"\mathrm{out}_t", "=", r"S_t", r"\,", r"q_t", colors=colors, font_size=40)
        fs = VGroup(f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.4, 1.6, 0])
        sl = label(r"the state $S$: \ $d \times d$ numbers, \ fixed size \\ (blue $+$, \ red $-$)", font_size=24,
                   color=STATE).to_corner(DL, buff=0.4)
        rnn = label(r"a transformer without the softmax \\ is a recurrent network", font_size=26, color=GREY_A)
        rnn.next_to(fs, DOWN, buff=0.5)
        chk = label(rf"computed both ways on ${lin['T']}$ tokens: \\ they agree to "
                    rf"$10^{{{math.ceil(math.log10(max(float(lin['dev']), 1e-16)))}}}$", font_size=22, color=GREY_B)
        chk.next_to(rnn, DOWN, buff=0.35)
        toks = VGroup(*[Text(w, font="DejaVu Sans Mono", font_size=24, color=GREY_A) for w in words]).arrange(RIGHT, buff=0.35)
        toks.to_edge(UP, buff=0.4).shift(LEFT * 2.2)
        for m in (f1, f2, sl, rnn, chk, toks):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-50 * DEGREES, zoom=0.95)
        with self.voiceover(
            "Now read the text one token at a time. With the product regrouped, everything the model needs from the "
            "past is one d by d matrix, the state. <bookmark mark='a'/> Each new token writes into it: its value "
            "times its key, an outer product, added on. <bookmark mark='b'/> To read, multiply the state by the "
            "query. The memory never grows: a transformer without the softmax is a recurrent network, Katharopoulos "
            "and colleagues showed in 2020."
        ) as vo:
            self.play(Create(base), FadeIn(cur), FadeIn(sl), FadeIn(toks))
            self.begin_ambient_camera_rotation(rate=0.06)
            vo.wait_until("a")
            self.play(Write(f1))
            for i, (kk, vv, S_) in enumerate(steps):
                self.play(toks[i].animate.set_color(C.BITS), Transform(cur, tower(S_)), run_time=0.8)
            vo.wait_until("b")
            self.play(Write(f2))
            self.play(FadeIn(rnn), FadeIn(chk))
            self.stop_ambient_camera_rotation()
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------------------
    def cost(self):
        lin = load("linear")
        Ts, so, lo_ = np.asarray(lin["Ts"]), np.asarray(lin["softmax_ops"]), np.asarray(lin["linear_ops"])
        lx = np.log10(Ts)
        y0, y1 = math.floor(np.log10(lo_.min())), math.ceil(np.log10(so.max()))
        ax = Axes(x_range=[3, 6, 1], y_range=[y0, y1, 1], x_length=7.6, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.6, -0.4, 0])
        xt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, y0), DOWN, buff=0.1)
                      for t, v in ((r"1{,}000", 3), (r"10{,}000", 4), (r"100{,}000", 5), (r"10^6", 6))])
        yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=22, color=GREY_B).next_to(ax.c2p(3, v), LEFT, buff=0.1)
                      for v in range(y0, y1 + 1, 2)])
        xn = label(r"length of the text, \ in tokens", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"multiplications per layer, \ whole text \ ($d = 128$)", font_size=22, color=GREY_A)
        yn.next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        cs = curve(ax, lx, np.log10(so), A, 4)
        cl = curve(ax, lx, np.log10(lo_), C.INTERVAL, 4)
        k1 = label(r"softmax attention: \ $\propto T^2 d$", font_size=26, color=A).move_to([4.5, 1.4, 0])
        k2 = label(r"linear attention: \ $\propto T d^2$", font_size=26, color=C.INTERVAL).next_to(k1, DOWN, buff=0.3).align_to(k1, LEFT)
        r = so[-1] / lo_[-1]
        gap = label(rf"at a million tokens: \ ${r:,.0f}\times$ fewer".replace(",", "{,}"), font_size=26, color=WHITE)
        gap.next_to(k2, DOWN, buff=0.5).align_to(k1, LEFT)
        keep_in_frame(gap)
        with self.voiceover(
            "The payoff grows with length. Softmax attention's work grows with the square of the text; the "
            "recurrence's grows in a straight line. <bookmark mark='a'/> At a million tokens, that's "
            f"{r:,.0f} times fewer multiplications. So why doesn't everyone use it? Because a fixed-size memory "
            "has to forget, and how it writes decides what it forgets."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            self.play(Create(cs), FadeIn(k1), Create(cl), FadeIn(k2), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(gap))
        self.wait(0.3)
        self.clear_scene()
