from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import (ADD, DECAY, DELTA, K, PART, Q, STATE, V, curve, load, signed_column, signed_grid,
                                   ttt_picture, ttt_step)

RULES = [("add", r"add", ADD), ("decay", r"decay, then add", DECAY), ("delta", r"the delta rule", DELTA)]


class Rules(VoiceoverScene):
    def construct(self):
        self.card()
        self.forgetting()
        self.delta()
        self.rewrite()
        self.gradient()

    def card(self):
        card = chapter_card(5, r"Forgetting and correcting", r"What should a full memory forget?", lit=(1960,), part=PART)
        with self.voiceover("Chapter five. Forgetting and correcting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def forgetting(self):
        c = load("capacity")
        age = {r: np.asarray(c[f"age_{r}"]) for r, _, _ in RULES}
        n = len(age["add"])
        colors = {r"S_t": STATE, r"S_{t-1}": STATE, r"v_t": V, r"k_t": K, r"a_t": DECAY}
        f = cmath(r"S_t", "=", r"a_t", r"\,", r"S_{t-1}", "+", r"v_t", r"\,", r"k_t", r"^{\top}", colors=colors,
                  font_size=40).to_edge(UP, buff=0.45)
        fl = label(r"$0 < a_t < 1$: \ old memories fade", font_size=24, color=DECAY).next_to(f, DOWN, buff=0.15)
        ax = Axes(x_range=[0, n, 32], y_range=[0, 2.5, 0.5], x_length=7.4, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.8, -1.2, 0])
        xt = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1) for v in range(0, n + 1, 32)])
        xn = label(rf"age: \ how many pairs ago it was written \ (${n}$ in all)", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"error reading it back \ (relative)", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        yt = VGroup(*[MathTex(f"{v:g}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0, 1, 2)])
        ca = curve(ax, np.arange(n), np.minimum(age["add"], 2.5), ADD, 3)
        cd = curve(ax, np.arange(n), np.minimum(age["decay"], 2.5), DECAY, 3.5)
        k1 = label(r"add: \ everything equally blurred", font_size=24, color=ADD).move_to([4.6, 0.2, 0])
        k2 = label(r"decay: \ recent ones sharp, \\ old ones gone", font_size=24, color=DECAY).next_to(k1, DOWN, buff=0.35).align_to(k1, LEFT)
        used = label(r"RetNet, \ GLA, \ Mamba-2: \\ decay, \ often chosen per token", font_size=22, color=GREY_A)
        used.next_to(k2, DOWN, buff=0.5).align_to(k1, LEFT)
        with self.voiceover(
            "The first fix is to forget on purpose. Before each write, shrink the whole memory a little. "
            f"<bookmark mark='a'/> Here are {n} pairs, read back by age. Adding blurs every pair the same. Decaying "
            "keeps the recent pairs sharp, and lets the old ones go. <bookmark mark='b'/> RetNet, gated linear "
            "attention and Mamba-2 all decay, and the best let each token choose how much: forget a lot at the "
            "start of a new topic, almost nothing in the middle of a sentence."
        ) as vo:
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            self.play(Create(ca), FadeIn(k1), run_time=1.5)
            self.play(Create(cd), FadeIn(k2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(used))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def delta(self):
        c = load("capacity")
        M, W = int(c["M"]), int(c["W"])
        colors = {r"S_t": STATE, r"S_{t-1}": STATE, r"v_t": V, r"k_t": K, r"\beta_t": DELTA}
        f = cmath(r"S_t", "=", r"S_{t-1}", "+", r"\beta_t", r"\big(", r"v_t", "-", r"S_{t-1}", r"k_t", r"\big)", r"\,",
                  r"k_t", r"^{\top}", colors=colors, font_size=40).to_edge(UP, buff=0.45)
        b = Brace(VGroup(*f[5:11]), DOWN, color=DELTA)
        bl = label(r"what should be there, \ minus what is there", font_size=24, color=DELTA).next_to(b, DOWN, buff=0.08)
        story = VGroup(label(r"``the door is open''", font_size=28, color=GREY_A),
                       label(r"\dots \ later: \ ``the door is closed''", font_size=28, color=GREY_A),
                       label(r"\dots \ ``is the door open?''", font_size=28, color=Q))
        story.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.6, 0.0, 0])
        vals = [c[f"update_{r}"] for r, _, _ in RULES]
        top = max(vals)
        scale = 3.0 / math.log10(top / min(vals) * 10)
        bars = VGroup()
        for i, ((r, t, col), v) in enumerate(zip(RULES, vals)):
            y = 0.6 - i * 0.8
            h = (math.log10(v / min(vals)) + 1) * scale
            nm = label(t, font_size=24, color=col).move_to([2.1, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=h, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([2.35 + h / 2, y, 0])
            val = MathTex(f"{v:.2f}", font_size=28, color=col).next_to(bar, RIGHT, buff=0.12)
            bars.add(VGroup(nm, bar, val))
        bh = label(rf"${M}$ keys, \ rewritten ${W}$ times: \\ error reading the \emph{{latest}} values \ (log scale)",
                   font_size=22, color=GREY_A).next_to(bars, UP, buff=0.3).align_to(bars, LEFT)
        cite_ = cite(r"B.~Widrow \& M.~E.~Hoff (1960); \ I.~Schlag, K.~Irie \& J.~Schmidhuber (2021); "
                     r"\ S.~Yang et al., \textit{DeltaNet} (2024)", corner=DR)
        steps = VGroup(label(r"1. \ read what the memory holds for the key: \ $S_{t-1} k_t$", font_size=26, color=STATE),
                       label(r"2. \ the error: \ $v_t - S_{t-1} k_t$", font_size=26, color=V),
                       label(r"3. \ write the error along the key, \ a share $\beta_t$ of it", font_size=26, color=DELTA))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -0.3, 0])
        with self.voiceover(
            "The second fix is smarter. Before writing, read what the memory already says for this key, and write "
            "only the difference: what should be there, minus what is there. That's the delta rule, Widrow and "
            "Hoff's learning rule from 1960. <bookmark mark='a'/> It matters when the world changes. The door is "
            "open; later, the door is closed. Adding stores both, and answers with a mixture. The delta rule "
            "replaces the old value with the new. <bookmark mark='b'/> Here are "
            f"{M} keys, rewritten {W} times with new values, then asked for the latest. Adding: an error of "
            f"{vals[0]:.0f}, it remembers every value ever written. Decaying: {vals[1]:.2f}. The delta rule: "
            f"{vals[2]:.2f}."
        ) as vo:
            self.play(Write(f), FadeIn(cite_))
            self.play(GrowFromCenter(b), FadeIn(bl), LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.2) for s_ in steps],
                                                                 lag_ratio=0.7), run_time=4.0)
            vo.wait_until("a")
            self.play(FadeOut(steps))
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.2) for s_ in story], lag_ratio=0.6), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(bh), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in bars], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rewrite(self):
        m = load("matrix_rw")
        keys, vals, seq = np.asarray(m["keys"]), np.asarray(m["vals"]), np.asarray(m["seq"]).astype(int)
        d = int(m["d"])
        vt = float(np.abs(vals).max())
        top = float(max(np.abs(m["S_add"]).max(), np.abs(m["S_delta"]).max()))
        cell = 0.4
        kk, vv = seq[4]
        head = label(rf"the same four pairs, \ then key $k_{{{kk + 1}}}$ gets a new value", font_size=26).to_edge(UP, buff=0.3)
        panels = VGroup()
        for rule, name, col in (("add", r"adding \ (linear attention)", ADD), ("delta", r"the delta rule, \ $\beta = 1$", DELTA)):
            S3 = signed_grid(np.asarray(m[f"S_{rule}"])[3], d * cell, top)
            t = label(name, font_size=22, color=col).next_to(S3, UP, buff=0.15)
            panels.add(VGroup(t, S3))
        panels.arrange(RIGHT, buff=3.4).move_to([0, 0.6, 0])
        newv = VGroup(MathTex(rf"v_{{{kk + 1}}}' ", font_size=34, color=V), signed_column(vals[vv], 0.3, vt))
        newv.arrange(DOWN, buff=0.1).move_to([0, 0.6, 0])
        arrows = VGroup(Arrow(newv.get_left(), panels[0][1].get_right(), buff=0.2, color=V, stroke_width=3),
                        Arrow(newv.get_right(), panels[1][1].get_left(), buff=0.2, color=V, stroke_width=3))
        ea, ed = np.asarray(m["err_add"])[4], np.asarray(m["err_delta"])[4]
        res = VGroup()
        for e, col, p in ((ea, ADD, panels[0]), (ed, DELTA, panels[1])):
            rows = VGroup(*[label(rf"$k_{j + 1}$: \ ${e[j]:.2f}$", font_size=24, color=WHITE if j == kk else GREY_B)
                            for j in range(4)]).arrange_in_grid(rows=2, cols=2, buff=(0.6, 0.12))
            rh = label(r"error reading the latest values", font_size=22, color=col)
            res.add(VGroup(rh, rows).arrange(DOWN, buff=0.12).next_to(p, DOWN, buff=0.3))
        ka = float(ea[kk])
        with self.voiceover(
            "Watch the difference on the eight-by-eight memory from the last chapter. The same four pairs are "
            f"written, <bookmark mark='a'/> and then key {kk + 1} is given a new value. <bookmark mark='b'/> Adding "
            "piles the new value on top of the old: reading that key now returns a blend of both, an error of "
            f"{ka:.2f}. <bookmark mark='c'/> The delta rule first reads what the memory holds for the key, and writes "
            f"only the difference: the new value comes back exactly, an error of {float(ed[kk]):.0f}. The other keys "
            "move a little, through their overlap with this one; with keys at right angles they wouldn't move at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(panels))
            vo.wait_until("a")
            self.play(FadeIn(newv), GrowArrow(arrows[0]), GrowArrow(arrows[1]))
            vo.wait_until("b")
            self.play(Transform(panels[0][1], signed_grid(np.asarray(m["S_add"])[4], d * cell, top).move_to(panels[0][1])),
                      FadeIn(res[0]))
            vo.wait_until("c")
            self.play(Transform(panels[1][1], signed_grid(np.asarray(m["S_delta"])[4], d * cell, top).move_to(panels[1][1])),
                      FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gradient(self):
        colors = {r"S": STATE, r"k": K, r"v": V, r"\beta": DELTA}
        f1 = cmath(r"\ell(S)", "=", r"\tfrac12", r"\|", r"S", r"k", "-", r"v", r"\|^2", colors=colors, font_size=50)
        f2 = cmath(r"\nabla_S\,\ell", "=", r"(", r"S", r"k", "-", r"v", r")", r"\,", r"k", r"^{\top}", colors=colors, font_size=50)
        f3 = cmath(r"S", r"\;\leftarrow\;", r"S", "-", r"\beta", r"\,(", r"S", r"k", "-", r"v", r")", r"\,", r"k", r"^{\top}",
                   colors=colors, font_size=50)
        fs = VGroup(f1, f2, f3).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(UP * 0.9 + LEFT * 2.4)
        l1 = label(r"how wrong the memory is \\ about this pair", font_size=26, color=GREY_A).next_to(f1, RIGHT, buff=0.5)
        l2 = label(r"the gap, \ times the key", font_size=26, color=GREY_A).next_to(f2, RIGHT, buff=0.5)
        l3 = label(r"one step of gradient descent: \\ the delta rule", font_size=26, color=DELTA).next_to(f3, RIGHT, buff=0.5)
        msg = label(r"the memory is a model, \ trained on the text as it is read", font_size=30, color=WHITE)
        msg.to_edge(DOWN, buff=1.2)
        fam = label(r"gated delta rule: \ Gated DeltaNet (Qwen3-Next), \ Kimi Delta Attention (Kimi Linear); \\ "
                    r"richer memories: \ test-time training, \ Titans", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        ttt = gloss(r"test-time training", r"the memory is a small network, \\ and its weights keep learning while the model "
                    r"reads", ttt_picture(), width=5.4, color=STATE).move_to([0, -0.55, 0])
        tp = ttt[1][-1]
        with self.voiceover(
            "And here is why the delta rule works. Measure how wrong the memory is about one pair: the squared gap "
            "between what it reads for the key and the value. <bookmark mark='a'/> Its gradient is the gap times the "
            "key. <bookmark mark='b'/> One step of gradient descent on it is exactly the delta rule: least squares, "
            "solved online, one example at a time, which is what Widrow and Hoff's least-mean-squares rule did for "
            "their ADALINE in 1960. So the memory is a little model, trained by Part 11's gradient descent on the "
            "text as it's being read; Part 13's attention layer that learned in context was doing the same. "
            "<bookmark mark='c'/> Add decay to the delta rule, and you have the gated delta rule inside Qwen3-Next "
            "and Kimi Linear, the next chapter; make the memory a whole network, and you have test-time training, "
            "chapter ten: a small network whose weights keep learning while the model reads."
        ) as vo:
            for m_ in (f2, l2, f3, l3):  # where the derivation is going, faint until it gets there
                m_.set_opacity(0.15)
            self.play(Write(f1), FadeIn(l1), FadeIn(f2), FadeIn(l2), FadeIn(f3), FadeIn(l3))
            vo.wait_until("a")
            self.play(f2.animate.set_opacity(1), l2.animate.set_opacity(1))
            vo.wait_until("b")
            self.play(f3.animate.set_opacity(1), l3.animate.set_opacity(1))
            self.play(FadeIn(msg))
            vo.wait_until("c")
            # room for the picture: the first two lines have done their work
            self.play(FadeOut(VGroup(f1, l1, f2, l2)), VGroup(f3, l3).animate.move_to([0, 2.65, 0]),
                      msg.animate.move_to([0, 1.65, 0]), FadeIn(fam))
            self.play(FadeIn(ttt, shift=UP * 0.2))
            for k_ in range(1, len(tp[0]) + 1):
                w_, t_ = ttt_step(tp, k_)
                self.play(Transform(tp[2][0], w_), Transform(tp[0], t_), run_time=0.5)
        self.wait(0.3)
        self.clear_scene()
