from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import heat_image
from videos.ai.ai12.common import ADD, DECAY, DELTA, K, Q, STATE, V, curve, load

RULES = [("add", r"add", ADD), ("decay", r"decay, then add", DECAY), ("delta", r"the delta rule", DELTA)]


class Rules(VoiceoverScene):
    def construct(self):
        self.card()
        self.crosstalk()
        self.forgetting()
        self.delta()
        self.gradient()

    def card(self):
        card = chapter_card(3, r"How to write to memory", r"What should a full memory forget?", part=12)
        with self.voiceover("Chapter three. How to write to memory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def err_axes(self, c, center):
        Ns = np.asarray(c["Ns"], float)
        ax = Axes(x_range=[0, Ns[-1], 64], y_range=[0, 2.5, 0.5], x_length=6.2, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to(center)
        xt = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1) for v in (0, 64, 128, 192, 256)])
        yt = VGroup(*[MathTex(f"{v:g}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0, 1, 2)])
        xn = label(r"pairs stored, \ $N$", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"error reading them back \ (relative)", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        return ax, VGroup(xt, yt, xn, yn)

    # ------------------------------------------------------------------
    def crosstalk(self):
        c = load("capacity")
        d = int(c["d"])
        Ns = np.asarray(c["Ns"], float)
        colors = {r"S": STATE, r"k_j": K, r"v_j": V, r"v_i": V, r"k_i": K}
        f = cmath(r"S", r"\,", r"k_j", "=", r"v_j", "+", r"\sum_{i \ne j}", r"v_i", r"\,(", r"k_i", r"\cdot", r"k_j", r")",
                  colors=colors, font_size=40).to_edge(UP, buff=0.45)
        b = Brace(VGroup(*f[5:]), DOWN, color=ADD)
        bl = label(r"crosstalk: \ every other pair leaks in", font_size=24, color=ADD).next_to(b, DOWN, buff=0.08)
        ax, deco = self.err_axes(c, [-2.6, -1.0, 0])
        ca = curve(ax, Ns, np.minimum(np.asarray(c["err_add"]), 2.5), ADD, 4)
        th = DashedLine(ax.c2p(0, -1 / d), ax.c2p(Ns[-1], min((Ns[-1] - 1) / d, 2.5)), color=GREY_B, stroke_width=1.5)
        thl = MathTex(r"\tfrac{N-1}{d}", font_size=30, color=GREY_B).next_to(ax.c2p(200, min(200 / d, 2.3)), DR, buff=0.1)
        note_ = label(rf"$d = {d}$: \ by $N = {d}$ pairs, \\ the leaks are as big \\ as the answer", font_size=26,
                      color=ADD).move_to([4.2, -0.6, 0])
        # the overlaps themselves: |k_i . k_j| for random unit keys; the diagonal is each pair's own key
        g = np.random.default_rng(12)
        keys = g.normal(size=(128, d))
        keys /= np.linalg.norm(keys, axis=1, keepdims=True)

        def gram(n):
            img = heat_image(np.abs(keys[:n] @ keys[:n].T), 3.6, 3.6, color=ADD, gamma=0.5).move_to([-1.6, -1.1, 0])
            lab = label(rf"$|k_i \cdot k_j|$ \ for ${n}$ random keys, \ $d = {d}$", font_size=22, color=GREY_A)
            return Group(img, lab.next_to(img, UP, buff=0.15))

        gr = gram(16)
        row = SurroundingRectangle(gr[0], buff=0.02, color=WHITE, stroke_width=2).stretch_to_fit_height(3.6 / 16 * 1.1)
        row.move_to([gr[0].get_x(), gr[0].get_top()[1] - 3.6 / 16 * 2.5, 0])
        rl = label(r"reading pair $j$: \ its own key (the bright one), \ plus a little of every other", font_size=22,
                   color=GREY_A).next_to(gr[0], RIGHT, buff=0.5)
        with self.voiceover(
            "Use the state as a memory. Write a few pairs, each a value times its key, then read one back with its "
            "key. <bookmark mark='a'/> You get its value, plus a little of every other value, in proportion to how "
            "much their keys overlap. Random keys in d dimensions overlap by about one over the square root of d, "
            "<bookmark mark='b'/> so the leaks add up like N over d. With d equals "
            f"{d}, by {d} pairs the noise is as big as the answer. Adding can never erase: the memory just fills up."
        ) as vo:
            self.play(Write(f))
            self.play(FadeIn(gr))
            vo.wait_until("a")
            self.play(GrowFromCenter(b), FadeIn(bl), Create(row), FadeIn(rl))
            g48, g128 = gram(48), gram(128)
            self.play(FadeOut(row), FadeOut(gr), FadeIn(g48), run_time=1.0)  # a cross-fade: FadeTransform can't restore images
            self.wait(0.3)
            self.play(FadeOut(g48), FadeIn(g128), run_time=1.0)
            vo.wait_until("b")
            self.play(*[FadeOut(m_) for m_ in self.mobjects if m_ not in (f, b, bl)])
            self.play(Create(ax), FadeIn(deco), Create(th), FadeIn(thl))
            self.play(Create(ca), FadeIn(note_), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

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
        yn = label(r"error reading it back", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
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
            self.play(Create(ax), FadeIn(xt), FadeIn(xn), FadeIn(yn))
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
            self.play(GrowFromCenter(b), FadeIn(bl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.2) for s_ in story], lag_ratio=0.6), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(bh), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in bars], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gradient(self):
        colors = {r"S": STATE, r"k": K, r"v": V, r"\beta": DELTA}
        f1 = cmath(r"\ell(S)", "=", r"\tfrac12", r"\|", r"S", r"k", "-", r"v", r"\|^2", colors=colors, font_size=42)
        f2 = cmath(r"\nabla_S\,\ell", "=", r"(", r"S", r"k", "-", r"v", r")", r"\,", r"k", r"^{\top}", colors=colors, font_size=42)
        f3 = cmath(r"S", r"\;\leftarrow\;", r"S", "-", r"\beta", r"\,(", r"S", r"k", "-", r"v", r")", r"\,", r"k", r"^{\top}",
                   colors=colors, font_size=42)
        fs = VGroup(f1, f2, f3).arrange(DOWN, buff=0.45).move_to(UP * 0.9)
        l1 = label(r"how wrong the memory is about this pair", font_size=22, color=GREY_A).next_to(f1, RIGHT, buff=0.4)
        l3 = label(r"one step of gradient descent: \\ the delta rule", font_size=22, color=DELTA).next_to(f3, RIGHT, buff=0.4)
        msg = label(r"the memory is a model, \ trained on the text as it is read", font_size=30, color=WHITE)
        msg.to_edge(DOWN, buff=1.2)
        fam = label(r"gated delta rule: \ Gated DeltaNet (Qwen3-Next), \ Kimi Delta Attention (Kimi Linear); \\ "
                    r"richer memories: \ test-time training, \ Titans", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "And here is why the delta rule works. Measure how wrong the memory is about one pair: the squared gap "
            "between what it reads for the key and the value. <bookmark mark='a'/> Its gradient is the gap times the "
            "key. <bookmark mark='b'/> One step of gradient descent on it is exactly the delta rule. So the memory "
            "is a little model, trained by part nine's gradient descent on the text as it's being read; part "
            "eleven's attention layer that learned in context was doing the same. <bookmark mark='c'/> Add decay to "
            "the delta rule, and you have the gated delta rule inside Qwen3-Next and Kimi Linear; make the memory a "
            "whole network, and you have test-time training."
        ) as vo:
            self.play(Write(f1), FadeIn(l1))
            vo.wait_until("a")
            self.play(Write(f2))
            vo.wait_until("b")
            self.play(Write(f3), FadeIn(l3))
            self.play(FadeIn(msg))
            vo.wait_until("c")
            self.play(FadeIn(fam))
        self.wait(0.3)
        self.clear_scene()
