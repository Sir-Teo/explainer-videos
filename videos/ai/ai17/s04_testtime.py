from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import CHAIN, RIGHT_C, WRONG_C, curve, hit_image, load

PASS, VOTE = C.BITS, C.TRUE_P


class TestTime(VoiceoverScene):
    def construct(self):
        self.card()
        self.samples()
        self.curves()

    def card(self):
        card = chapter_card(4, r"Thinking longer", r"What does more computation at answer time buy?", lit=(2024,), part=17)
        with self.voiceover("Chapter four. Thinking longer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def samples(self):
        r = load("rl")
        V, truth = np.asarray(r["vals_before"]), np.asarray(r["truth"])
        R = V == truth[:, None]
        order = np.argsort(-R.sum(1), kind="stable")
        R = R[order]
        nq, n = R.shape
        W, H = 6.4, 5.2
        img = hit_image(R, W, H).move_to([-2.6, -0.3, 0])
        frame = SurroundingRectangle(img, color=GREY_C, buff=0.02, stroke_width=1)
        xl = label(rf"${n}$ samples per question", font_size=22, color=GREY_A).next_to(img, UP, buff=0.15)
        yl = label(rf"${nq}$ questions, \ most often right at the top", font_size=22, color=GREY_A).rotate(PI / 2).next_to(img, LEFT, buff=0.15)
        c = R.sum(1)
        all_right, never = int((c == n).sum()), int((c == 0).sum())
        some = nq - all_right - never
        k1 = label(rf"always right: \ ${all_right}$", font_size=26, color=RIGHT_C)
        k2 = label(rf"sometimes: \ ${some}$", font_size=26, color=C.BITS)
        k3 = label(rf"never: \ ${never}$", font_size=26, color=WRONG_C)
        keys = VGroup(k1, k2, k3).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, 1.3, 0])
        colors = {r"c": RIGHT_C, r"k": PASS}
        f = cmath(r"\text{pass@}", r"k", r"= 1 - \binom{n - ", r"c", r"}{", r"k", r"} \Big/ \binom{n}{", r"k", r"}", colors=colors,
                  font_size=36).move_to([3.6, -1.0, 0])
        fl = label(r"the chance that at least one \\ of $k$ tries is right", font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.25)
        # one question that is sometimes right: highlight its row
        row = int(np.where((c > 0) & (c < n))[0][len(np.where((c > 0) & (c < n))[0]) // 2]) if some else 0
        y = img.get_top()[1] - (row + 0.5) * H / nq
        band = Rectangle(width=W + 0.1, height=max(H / nq, 0.05) + 0.04, stroke_color=C.BITS, stroke_width=2).move_to([img.get_x(), y, 0])
        cite_ = cite(r"M.~Chen et al., \textit{Evaluating Large Language Models Trained on Code} (pass@$k$, 2021)", corner=DR)
        with self.voiceover(
            "There's another way to spend computation: at answer time. Take our addition model, before the "
            f"reinforcement learning, and let it answer each of {nq} questions {n} times. <bookmark mark='a'/> Green "
            "is right, red is wrong. "
            + (f"Not one question is always right, and not one is always wrong: each of the {nq} comes out right "
               "only some of the time. <bookmark mark='b'/> So trying again always has a chance of helping. "
               if all_right == 0 and never == 0 else
               f"{all_right} questions it always gets right, {never} it never does, and {some} it gets right only "
               "sometimes. <bookmark mark='b'/> For those, trying again helps. ")
            + "<bookmark mark='c'/> If c of n samples are right, the chance that at least one of k tries is right is "
            "one minus n minus c choose k, over n choose k. It's called pass at k, and it needs a checker to tell "
            "which try was the right one."
        ) as vo:
            self.play(FadeIn(img), Create(frame), FadeIn(xl), FadeIn(yl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(FadeIn(k1), FadeIn(k3), FadeIn(k2), lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(band), Indicate(k2, color=C.BITS))
            vo.wait_until("c")
            self.play(Write(f), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        s = load("sampling")
        ks = [int(k) for k in s["ks"]]
        pk, mj = [float(v) for v in s["passk"]], [float(v) for v in s["majority"]]
        lk = [math.log2(k) for k in ks]
        lo = math.floor(min(pk + mj) * 10) / 10
        ax = Axes(x_range=[0, lk[-1], 1], y_range=[lo, 1, 0.1], x_length=7.0, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.0, -0.5, 0])
        xt = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(ax.c2p(math.log2(k), lo), DOWN, buff=0.1) for k in ks])
        yt = VGroup(*[MathTex(rf"{int(round(100 * v))}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in np.arange(lo, 1.001, 0.1 if 1 - lo <= 0.5 else 0.2)])
        xn = label(r"tries per question, \ $k$ \ (doubling)", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"questions answered right", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        lp, lm = curve(ax, lk, pk, PASS, 4), curve(ax, lk, mj, VOTE, 4)
        dp = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=PASS) for x, y in zip(lk, pk)])
        dm = VGroup(*[Dot(ax.c2p(x, y), radius=0.06, color=VOTE) for x, y in zip(lk, mj)])
        kp = label(r"with a checker: \ any try right \ (pass@$k$)", font_size=24, color=PASS)
        kv = label(r"no checker: \ the most common answer \ (majority vote)", font_size=24, color=VOTE)
        keys = VGroup(kp, kv).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(UP, buff=0.3).shift(RIGHT * 2.2)
        r = load("rl")
        rl_line = DashedLine(ax.c2p(0, float(r["after"])), ax.c2p(lk[-1], float(r["after"])), color=CHAIN, stroke_width=2)
        rl_l = label(r"one try, \ after RL", font_size=20, color=CHAIN).next_to(rl_line, RIGHT, buff=0.1)
        gain = mj[-1] - mj[0]
        with self.voiceover(
            "So how much does trying more buy? <bookmark mark='a'/> With a checker, a lot: one try is right "
            f"{100 * pk[0]:.0f} percent of the time, and with {ks[-1]} tries, {100 * pk[-1]:.0f} percent. Every "
            "doubling of the tries buys a little more. <bookmark mark='b'/> Without a checker, take a vote: the "
            f"answer it gives most often. That climbs from {100 * mj[0]:.0f} to {100 * mj[-1]:.0f} percent"
            + (": less, because a vote can't recover an answer the model rarely gives." if gain < (pk[-1] - pk[0]) else ".")
            + " <bookmark mark='c'/> And the dashed line is the same model after reinforcement learning, with just "
            f"one try: {100 * float(r['after']):.0f} percent. Training moved what used to need many tries into one. "
            "Today's reasoning models do both: trained by RL to think in long chains, and then given more time to "
            "think when the question is hard."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(Create(lp), LaggedStart(*[FadeIn(d_) for d_ in dp], lag_ratio=0.15), FadeIn(kp), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(lm), LaggedStart(*[FadeIn(d_) for d_ in dm], lag_ratio=0.15), FadeIn(kv), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(rl_line), FadeIn(rl_l))
        self.wait(0.3)
        self.clear_scene()
