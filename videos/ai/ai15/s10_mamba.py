from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import DECAY, DELTA, K, PART, Q, SSM_C, STATE, V, curve, heat_image, load, sci

GATE = C.SURPRISE


class Mamba(VoiceoverScene):
    def construct(self):
        self.card()
        self.selective()
        self.duality()
        self.mamba3()

    def card(self):
        card = chapter_card(9, r"Selectivity: Mamba and after", r"Can a memory choose what to keep?", part=PART)
        with self.voiceover("Chapter nine. Selectivity: Mamba and after."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

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
            "still. Now the state keeps the marked value until the next one replaces it. A memory that chooses. "
            "<bookmark mark='c'/> With delta, B and C all depending on the input, the convolution trick is gone; "
            "Gu and Tri Dao ran the recurrence as last chapter's scan, written to keep the state in the chip's "
            "fastest memory, and reported five times the throughput of a transformer at inference."
        ) as vo:
            self.play(FadeIn(ins), FadeIn(il), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.005), FadeIn(cite_),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(a1), FadeIn(hl), Create(cf), FadeIn(k1), run_time=2.5)
            vo.wait_until("b")
            self.play(cf.animate.set_stroke(opacity=0.3), Create(csel), FadeIn(k2), run_time=2.5)
            vo.wait_until("c")
            self.play(Indicate(k2, color=C.INTERVAL, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def duality(self):
        d = load("delta")
        L, a = np.asarray(d["ssd_L"]), np.asarray(d["ssd_a"])
        n = L.shape[0]
        S = 4.6
        img = heat_image(L, S, S, color=DECAY, gamma=0.5, mask_upper=True).move_to([-2.5, -0.4, 0])
        frame = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.5)
        il = label(r"the mask $L$: \ row $i$, column $j$ \\ how much of token $j$ is left at step $i$", font_size=22,
                   color=GREY_A).next_to(img, UP, buff=0.15)
        cell = S / n
        blk = Rectangle(width=cell * 16, height=cell * 16, stroke_color=WHITE, stroke_width=2.5)
        blk.move_to(img.get_corner(DL) + np.array([cell * 8, cell * 8, 0]))
        forgets = [int(i) for i in np.where(a < 0.2)[0]]
        marks = VGroup(*[Line(img.get_left() + np.array([0, S / 2 - cell * (i + 0.5), 0]),
                              img.get_left() + np.array([-0.25, S / 2 - cell * (i + 0.5), 0]), color=GATE, stroke_width=4)
                         for i in forgets])
        ml = label(r"the gate forgets", font_size=20, color=GATE).next_to(marks, LEFT, buff=0.1)
        colors = {r"L": DECAY, r"Q": Q, r"K": K, r"V": V, r"a": GATE}
        f1 = cmath(r"O", "=", r"(", r"L", r"\circ", r"Q", r"K", r"^{\top}", r")\,", r"V", colors=colors, font_size=40).move_to([3.9, 1.8, 0])
        f2 = cmath(r"L", r"_{ij} = ", r"a", r"_{j+1}\, ", r"a", r"_{j+2} \cdots ", r"a", r"_i", colors=colors, font_size=36)
        f2.next_to(f1, DOWN, buff=0.35)
        rk = label(rf"every block below the diagonal has rank one \\ (second singular value $/$ first: "
                   rf"${sci(float(d['ssd_rank_ratio']))}$)", font_size=20, color=GREY_A).next_to(f2, DOWN, buff=0.35)
        agree = label(rf"masked attention vs the recurrence: \\ largest difference ${sci(float(d['ssd_diff']))}$",
                      font_size=22, color=C.INTERVAL).next_to(rk, DOWN, buff=0.35)
        msg = label(r"one layer, \ two algorithms: \\ a recurrence to generate, \ masked attention to train", font_size=24,
                    color=WHITE).next_to(agree, DOWN, buff=0.4)
        cite_ = cite(r"T.~Dao \& A.~Gu, \textit{Transformers are SSMs: \ Generalized Models and Efficient Algorithms Through "
                     r"Structured State Space Duality} (2024)", corner=DR)
        with self.voiceover(
            "In 2024 Tri Dao and Gu showed that a selective state-space model, with its A reduced to a single "
            "number per step, is the decaying memory of chapter five: linear attention with a gate, its B playing "
            "the key and its C the query. That is Mamba-2, and its state-space duality gives the layer two faces. "
            "<bookmark mark='a'/> "
            "Unroll the recurrence, and every output is a weighted sum of earlier values: exactly attention, with "
            "the query-key scores multiplied by a mask L. <bookmark mark='b'/> Entry i, j of the mask is the "
            "product of the gates between token j and token i: how much of token j survives until step i. Where "
            "the gate forgets, the mask goes dark below that row. <bookmark mark='c'/> That mask is semiseparable, which "
            "just means: every block below the diagonal has rank one, because each entry is a number for its row "
            "times a number for its column. <bookmark mark='d'/> We checked: masked attention and the recurrence "
            "agree to rounding error. So the same layer can run as a recurrence while it writes, using constant "
            "memory, and as masked attention while it trains, using big matrix products."
        ) as vo:
            self.play(FadeIn(cite_), Write(f1), FadeIn(img), Create(frame), FadeIn(il))
            vo.wait_until("a")
            self.play(Indicate(f1, color=WHITE, scale_factor=1.05))
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(marks), FadeIn(ml))
            vo.wait_until("c")
            self.play(Create(blk), FadeIn(rk))
            vo.wait_until("d")
            self.play(FadeIn(agree), FadeIn(msg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mamba3(self):
        head = label(r"Mamba-3 \ (Lahoti, Li, Chen, Wang, Bick, Kolter, Dao \& Gu, \ ICLR 2026)", font_size=28).to_edge(UP, buff=0.35)
        w = 4.1
        # 1. a better step: the trapezoid between the two ends of the step, against the hold at one end
        ax1 = Axes(x_range=[0, 1, 1], y_range=[0, 1.2, 1], x_length=2.6, y_length=1.6, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        fx = lambda x: 0.35 + 0.6 * x ** 1.5  # noqa: E731
        under = ax1.plot(fx, x_range=[0, 1], color=K, stroke_width=3)
        hold = Polygon(ax1.c2p(0, 0), ax1.c2p(1, 0), ax1.c2p(1, fx(1)), ax1.c2p(0, fx(1)), stroke_width=0,
                       fill_color=GREY_B, fill_opacity=0.25)
        trap = Polygon(ax1.c2p(0, 0), ax1.c2p(1, 0), ax1.c2p(1, fx(1)), ax1.c2p(0, fx(0)), stroke_width=1.5,
                       stroke_color=SSM_C, fill_color=SSM_C, fill_opacity=0.35)
        p1 = VGroup(ax1, hold, trap, under)
        t1 = label(r"a better step: \\ both ends of each step, not one \\ (``exponential-trapezoidal'')", font_size=19, color=SSM_C)
        # 2. a complex state: rotation, which can flip and count
        circ = Circle(radius=0.75, color=GREY_C, stroke_width=1.5)
        arr = Arrow(ORIGIN, RIGHT * 0.75, buff=0, color=SSM_C, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        p2 = VGroup(circ, arr, Dot(ORIGIN, radius=0.03, color=GREY_B))
        t2 = label(r"a complex state: \\ it can rotate, \\ so it can track parity", font_size=19, color=SSM_C)
        # 3. MIMO: a rank-r write instead of rank one, for more arithmetic per byte of state
        sq = lambda c_, o: Square(0.22, stroke_width=0.5, stroke_color=GREY_D, fill_color=c_, fill_opacity=o)  # noqa: E731
        one = VGroup(*[sq(SSM_C, 0.25 + 0.6 * ((i * 3 + j * 5) % 7) / 7) for i in range(5) for j in range(5)]).arrange_in_grid(5, 5, buff=0.02)
        p3 = VGroup(MathTex(r"\sum_{r=1}^{R} v_r k_r^{\top}", font_size=28, color=WHITE), one).arrange(RIGHT, buff=0.2)
        t3 = label(r"several inputs and outputs a step (MIMO): \\ more work for each read of the state, \\ the same speed "
                   r"to generate", font_size=19, color=SSM_C)
        cols = VGroup()
        for p_, t_ in ((p1, t1), (p2, t2), (p3, t3)):
            box = RoundedRectangle(width=w, height=3.4, corner_radius=0.14, stroke_color=GREY_D, stroke_width=1.5,
                                   fill_color="#121722", fill_opacity=1)
            p_.move_to(box.get_center() + UP * 0.55)
            t_.next_to(box.get_bottom(), UP, buff=0.25)
            cols.add(VGroup(box, p_, t_))
        cols.arrange(RIGHT, buff=0.3).move_to(UP * 0.1)
        res = label(r"reported: \ the same perplexity as Mamba-2 with half the state; \\ at $1.5$B parameters, $+0.6$ points "
                    r"over Gated DeltaNet, \ $+1.2$ more with MIMO", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.5)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "The line continues. In March 2026 Aakash Lahoti, Gu, Dao and colleagues published Mamba-3, with three "
            "ideas from state-space thinking. <bookmark mark='a'/> First, a better step: instead of holding the "
            "input from one end of the step, use both ends, a trapezoid; with a learned bias added, they could drop "
            "the short convolution that sits in front of every layer of this family. <bookmark mark='b'/> Second, a complex-valued state, which can "
            "rotate as well as shrink: like the delta rule's reflections in chapter six, it lets the memory flip and "
            "count, and track parity, which Mamba-2 cannot. <bookmark mark='c'/> Third, several inputs and outputs "
            "per step, a rank-r write: more arithmetic for every byte of state read, which suits graphics cards, "
            "without slowing generation. <bookmark mark='d'/> They report the perplexity of Mamba-2 with half the "
            "state, and, at one and a half billion parameters, a little ahead of Gated DeltaNet."
        ) as vo:
            veils = VGroup(*[Rectangle(width=c_[0].width + 0.05, height=c_[0].height + 0.05, stroke_width=0,
                                       fill_color=BACKGROUND, fill_opacity=0.82).move_to(c_[0]) for c_ in cols])
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cols), FadeIn(veils))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeOut(veils[k]))
                if k == 1:
                    self.play(Rotate(arr, angle=PI, about_point=ORIGIN + circ.get_center()), run_time=1.0)
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
