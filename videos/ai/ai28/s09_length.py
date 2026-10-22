from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai28.common import (CHAIN, DIRECT, LEN, PART, POLICY, RIGHT_C, WRONG_C, heat, load, seeds_plot,
                                   solution_chips)

COST_C = {"plain": CHAIN, "gentle": C.BITS, "strong": DIRECT}


class Length(VoiceoverScene):
    def construct(self):
        self.card()
        self.r1()
        self.replay()
        self.overthink()
        self.dial()
        self.practice()

    def card(self):
        card = chapter_card(8, r"How long to think", r"Does a model learn to think longer, and should it?",
                            lit=(2025,), part=PART)
        with self.voiceover("Chapter eight. How long to think."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def r1(self):
        hc = history_card(2025, r"DeepSeek-R1-Zero, \ during reinforcement learning",
                          r"its thinking grew longer throughout training, \ from hundreds of tokens to thousands, \ "
                          r"though nothing rewarded length", width=8.2, color=LEN).move_to(UP * 1.7)
        aha = VGroup(label(r"an intermediate version, \ mid-solution:", font_size=22, color=GREY_A),
                     label(r"``Wait, wait. Wait. That's an aha moment I can flag here.''", font_size=30, color=CHAIN))
        aha.arrange(DOWN, buff=0.2).move_to(DOWN * 0.5)
        meaning = label(r"re-checking, \ backtracking, \ trying again: \ learned because they paid", font_size=26,
                        color=GREY_A).to_edge(DOWN, buff=0.7)
        cite_ = cite(r"DeepSeek-AI, \textit{DeepSeek-R1} (2025), \ Table 3")
        with self.voiceover(
            "When DeepSeek trained R1-Zero with reinforcement learning, something happened that nobody had asked for. "
            "Its thinking grew longer, steadily, throughout training, from hundreds of tokens to thousands, though "
            "the reward only checked the final answer. <bookmark mark='a'/> And in the middle of one solution, an "
            "intermediate version wrote: wait, wait, wait. That's an aha moment I can flag here. Then it went back "
            "and redid the step. <bookmark mark='b'/> Re-checking, backtracking, trying another way: none of it was "
            "demonstrated. It appeared because longer, more careful chains earned more reward."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(aha, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(meaning))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        d = load("think_rl")
        ns = [int(n) for n in d["ns"]]
        snaps = np.asarray(d["plain_snap_steps"])
        Hs = np.asarray(d["plain_snap_hist"])  # (snaps, len(ns), S + 4): at once, then 0, 1, ... steps
        ncol = max(ns) + 2  # at once, 0 .. max(ns) steps
        logs = np.asarray(d["plain_steps"])
        L = np.asarray(d["plain_len"]).mean(2)  # (seeds, logs): mean steps of thought, over list lengths
        A = np.asarray(d["plain_acc"]).mean(2)
        W, Hh = 4.6, 3.6
        center = np.array([-3.6, -0.1, 0])

        def img(k):
            M = Hs[k][:, :ncol]
            M = M / np.maximum(M.sum(1, keepdims=True), 1)
            return heat(M, W, Hh, color=CHAIN, vmax=1.0).move_to(center)

        frame = Rectangle(width=W, height=Hh, stroke_color=GREY_C, stroke_width=1).move_to(center)
        cw, rh = W / ncol, Hh / len(ns)
        rl = VGroup(*[label(rf"${n}$", font_size=18, color=GREY_B).move_to(frame.get_corner(UL) + np.array([-0.25, -(i + 0.5) * rh, 0]))
                      for i, n in enumerate(ns)])
        cl = VGroup(label(r"at once", font_size=14, color=DIRECT).move_to(frame.get_corner(DL) + np.array([cw / 2, -0.25, 0])),
                    *[label(rf"${j}$", font_size=16, color=GREY_B).move_to(frame.get_corner(DL) + np.array([(j + 1.5) * cw, -0.25, 0]))
                      for j in range(0, ncol - 1)])
        yl = label(r"digits in the list", font_size=20, color=GREY_A).rotate(PI / 2).next_to(rl, LEFT, buff=0.15)
        xl = label(r"steps of thought it chose", font_size=20, color=GREY_A).next_to(cl, DOWN, buff=0.12)
        diag = VGroup(*[Square(min(cw, rh) * 0.92, stroke_color=WHITE, stroke_width=1.5).move_to(
            frame.get_corner(UL) + np.array([(n + 1.5) * cw, -(i + 0.5) * rh, 0])) for i, n in enumerate(ns)])
        dl = label(r"outlined: \ the whole chain", font_size=18, color=WHITE).next_to(frame, UP, buff=0.1)
        g = axes([0, logs[-1]], [0, max(ns)], x_length=4.2, y_length=1.6, ylabel=r"mean steps of thought",
                 xticks=[0, logs[-1]], yticks=[0, max(ns)], center=[3.9, 1.7, 0], font_size=16)
        h = axes([0, logs[-1]], [0, 1], x_length=4.2, y_length=1.6, xlabel=r"RL steps", ylabel=r"accuracy",
                 xticks=[0, logs[-1]], yticks=[0, 1], yfmt=lambda v: rf"{int(100 * v)}\%", center=[3.9, -1.25, 0],
                 font_size=16)
        kt = ValueTracker(0)

        def upto(Y, ax, col):
            i = int(np.searchsorted(logs, kt.get_value(), side="right"))
            return seeds_plot(ax, logs[:i], Y[:, :i], col) if i >= 2 else VGroup()

        lg_ = always_redraw(lambda: upto(L, g.ax, LEN))
        la_ = always_redraw(lambda: upto(A, h.ax, RIGHT_C))
        cnt = always_redraw(lambda: label(rf"RL step ${int(kt.get_value())}$", font_size=26, color=C.BITS)
                            .to_edge(UP, buff=0.3).shift(LEFT * 3.6))
        tag = note(r"computed: \ reward for the right sum only; \ $3$ runs, \ band: lowest to highest; \ map: run $1$")
        tag.to_corner(DR, buff=0.2)
        cur = img(0)
        l0, l1 = float(L[:, 0].mean()), float(L[:, -1].mean())
        a0, a1 = float(A[:, 0].mean()), float(A[:, -1].mean())
        th = np.asarray(d["plain_think"])  # (seeds, logs, len(ns))
        p2, p9 = float(th[:, -1, 0].mean()), float(th[:, -1, -1].mean())
        pt0 = float(th[:, 0, :].mean())
        H0, HK = Hs[0][:, :ncol], Hs[-1][:, :ncol]
        full = lambda M: float(np.mean([M[i, n + 1] / max(M[i].sum(), 1) for i, n in enumerate(ns)]))  # noqa: E731
        partial0 = float(np.mean([M_[1:n + 1].sum() / max(M_.sum(), 1) for M_, n in zip(H0, ns)]))
        if partial0 > 0.15:
            start = (f"At the start it thinks {100 * pt0:.0f} percent of the time, and often stops before the end of "
                     "the list.")
        else:
            start = f"At the start it thinks {100 * pt0:.0f} percent of the time."
        if full(HK) > 0.8:
            end = (f"By the end it writes the whole chain almost every time: it thinks on {100 * p9:.0f} percent of "
                   f"nine-digit lists, and on {100 * p2:.0f} percent of two-digit ones.")
        else:
            end = (f"By the end it thinks on {100 * p9:.0f} percent of nine-digit lists, and on {100 * p2:.0f} percent "
                   "of two-digit ones.")
        with self.voiceover(
            "Our adding model can show the same thing in miniature. Reward it only for the right sum, and replay the "
            "training. <bookmark mark='a'/> The map shows, for each length of list, how many steps of thought it "
            "chooses: the first column is answering at once, and the outlined cells are the whole chain. "
            f"{start} <bookmark mark='b'/> Watch the mass move. <bookmark mark='c'/> Mean thinking goes from "
            f"{l0:.1f} steps to {l1:.1f}, and accuracy from {100 * a0:.0f} percent to {100 * a1:.0f}. {end}"
        ) as vo:
            self.play(FadeIn(frame), FadeIn(cur), FadeIn(rl), FadeIn(cl), FadeIn(yl), FadeIn(xl), FadeIn(g), FadeIn(h),
                      FadeIn(tag))
            self.add(lg_, la_, cnt)
            vo.wait_until("a")
            self.play(Create(diag), FadeIn(dl))
            vo.wait_until("b")
            K = len(snaps)
            dt = max(0.4, min(1.2, (vo.until("c") - 0.3) / max(K - 1, 1)))
            for k in range(1, K):
                self.play(Transform(cur, img(k)), kt.animate.set_value(snaps[k]), run_time=dt, rate_func=linear)
            self.play(kt.animate.set_value(logs[-1]), run_time=0.3)
            vo.wait_until("c")
            self.play(Indicate(diag, color=WHITE))
        for m in (lg_, la_, cnt):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def overthink(self):
        s = load("think_sft")
        d = load("think_rl")
        ns = [int(n) for n in d["ns"]]
        ad, at = float(s["acc_direct"][0]), float(s["acc_think"][0])
        p2 = float(np.asarray(d["plain_think"])[:, -1, 0].mean())
        hc = history_card(2024, r"X.~Chen et al., \ \textit{Do NOT Think That Much for 2+3=?}",
                          r"o1-like models spend far more tokens on easy questions than they need: \ ``overthinking''",
                          width=7.6, color=LEN).move_to(UP * 1.8)
        bars = VGroup()
        for i, (t, v, c) in enumerate(((r"answering at once", ad, DIRECT), (r"thinking", at, CHAIN))):
            b = Rectangle(width=0.9, height=2.6 * v, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([-4.6 + 1.6 * i, -2.4, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, label(rf"${100 * v:.0f}\%$", font_size=22, color=c).next_to(b, UP, buff=0.08),
                            label(t, font_size=18, color=c).next_to(b, DOWN, buff=0.12)))
        bh = label(r"two-digit lists, \ before RL", font_size=22, color=GREY_A).next_to(bars, UP, buff=0.45)
        txt = VGroup(label(rf"after RL it thinks on ${100 * p2:.0f}\%$ of them", font_size=26, color=CHAIN),
                     label(r"nothing in the reward says tokens cost anything", font_size=24, color=LEN))
        txt.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, -1.2, 0])
        gap = 100 * (at - ad)
        if gap > 1:
            said = (f"On two-digit lists, before any reinforcement learning, answering at once was already right "
                    f"{100 * ad:.0f} percent of the time, thinking {100 * at:.0f}: a gain of {gap:.0f} points.")
        else:
            said = (f"On two-digit lists, before any reinforcement learning, answering at once was right "
                    f"{100 * ad:.0f} percent of the time, and thinking {100 * at:.0f}: no gain at all.")
        if p2 > 0.5:
            after = (f"After training, ours thinks on {100 * p2:.0f} percent of them anyway. Nothing in the reward says "
                     "a token of thought costs anything, so any gain at all, however small, is worth any length.")
        else:
            after = (f"After training, ours thinks on only {100 * p2:.0f} percent of them: here the small gain was "
                     "not enough to make thinking a habit. Larger models, rewarded the same way, are not so careful.")
        with self.voiceover(
            "There is a cost hiding in that last number. In late 2024, researchers at Tencent and Shanghai Jiao Tong "
            "University named it: reasoning models overthink, spending far more tokens than needed on questions as "
            f"easy as two plus three. <bookmark mark='a'/> {said} <bookmark mark='b'/> {after}"
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(bh), LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2]))
                                                for b in bars], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.1) for t_ in txt], lag_ratio=0.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dial(self):
        d = load("think_rl")
        ns = [int(n) for n in d["ns"]]
        names = list(d["names"])
        costs = d["costs"]
        rew = cmath(r"\text{reward}", r"=", r"\mathbf 1[\text{right}]", r"-", r"c", r"\times", r"\text{steps of thought}",
                    font_size=34).to_edge(UP, buff=0.35)
        rew[4].set_color(LEN)
        g1 = axes([ns[0] - 0.5, ns[-1] + 0.5], [0, 1], x_length=5.2, y_length=3.0, xlabel=r"digits in the list",
                  ylabel=r"how often it thinks", xticks=ns, yticks=[0, 0.5, 1], yfmt=lambda v: rf"{int(100 * v)}\%",
                  center=[-3.4, -0.9, 0])
        g2 = axes([ns[0] - 0.5, ns[-1] + 0.5], [0, 1], x_length=5.2, y_length=3.0, xlabel=r"digits in the list",
                  ylabel=r"right", xticks=ns, yticks=[0, 0.5, 1], yfmt=lambda v: rf"{int(100 * v)}\%",
                  center=[3.3, -0.9, 0])
        th = {k: np.asarray(d[f"{k}_think"])[:, -1, :] for k in names}  # (seeds, len(ns)) at the end
        ac = {k: np.asarray(d[f"{k}_acc"])[:, -1, :] for k in names}
        p1 = {k: seeds_plot(g1.ax, ns, th[k], COST_C[k]) for k in names}
        p2 = {k: seeds_plot(g2.ax, ns, ac[k], COST_C[k]) for k in names}
        lg = legend([(COST_C[k], rf"$c = {float(costs[k]):g}$") for k in names], font_size=20)
        lg.next_to(rew, DOWN, buff=0.25)
        lg.arrange(RIGHT, buff=0.6).next_to(rew, DOWN, buff=0.25)
        tag = note(r"computed: \ after $250$ RL steps; \ $3$ runs each, \ band: lowest to highest").to_corner(DR, buff=0.2)
        g_t = th["gentle"].mean(0)
        g_s = th["strong"].mean(0)
        acc9 = {k: float(ac[k][:, -1].mean()) for k in names}
        if g_t[-1] > g_t[0] + 0.3:
            gentle = (f"With a cost of {float(costs['gentle']):g} per step, it learns to choose: it thinks on "
                      f"{100 * g_t[0]:.0f} percent of two-digit lists and {100 * g_t[-1]:.0f} percent of nine-digit "
                      "ones. Short lists, it answers; long ones, it works out.")
        else:
            gentle = (f"With a cost of {float(costs['gentle']):g} per step, it thinks on {100 * g_t[0]:.0f} percent of "
                      f"two-digit lists and {100 * g_t[-1]:.0f} percent of nine-digit ones.")
        if acc9["strong"] < acc9["plain"] - 0.05:
            strong = (f"With {float(costs['strong']):g}, thinking is too expensive: it thinks on "
                      f"{100 * g_s[-1]:.0f} percent even of the longest lists, and gets them right "
                      f"{100 * acc9['strong']:.0f} percent of the time, against {100 * acc9['plain']:.0f} with no cost. "
                      "Too little thought, now.")
        else:
            strong = (f"With {float(costs['strong']):g}, it thinks on {100 * g_s[-1]:.0f} percent of the longest lists, "
                      f"and gets them right {100 * acc9['strong']:.0f} percent of the time, against "
                      f"{100 * acc9['plain']:.0f} with no cost.")
        tp = float(th["plain"].mean())
        if tp > 0.85:
            plain = "With no cost, it thinks on nearly everything."
        else:
            plain = f"With no cost, it thinks on {100 * tp:.0f} percent of lists, averaged over lengths."
        with self.voiceover(
            "The fix is to make thought cost something: subtract a small amount c from the reward for every step of "
            f"thought. We trained three ways, three runs each. <bookmark mark='a'/> {plain} <bookmark mark='b'/> "
            f"{gentle} <bookmark mark='c'/> {strong} <bookmark mark='d'/> The cost is a dial between overthinking and "
            "underthinking."
        ) as vo:
            self.play(Write(rew), FadeIn(g1), FadeIn(g2), FadeIn(tag))
            for k, mk in zip(names, "abc"):
                vo.wait_until(mk)
                self.play(FadeIn(lg[names.index(k)]), FadeIn(p1[k][0]), Create(p1[k][1]), FadeIn(p2[k][0]),
                          Create(p2[k][1]), run_time=1.5)
            vo.wait_until("d")
            self.play(Indicate(rew[4], color=LEN, scale_factor=1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        kimi = cmath(r"\lambda", r"=", r"0.5 - \frac{\text{len} - \text{min len}}{\text{max len} - \text{min len}}",
                     font_size=32)
        cards = VGroup(
            history_card(2025, r"Kimi k1.5 \ (Moonshot, \ January)", kimi, width=6.3, color=LEN),
            history_card(2025, r"L1 \ (Aggarwal \& Welleck, \ March)", r"the length is in the prompt; \ RL rewards "
                         r"hitting it: \ ``think for $512$ tokens''", width=6.3, color=LEN),
            history_card(2025, r"DAPO \ (March)", r"a soft penalty only past a maximum length", width=6.3, color=C.BITS),
            history_card(2025, r"in products", r"a thinking budget in tokens, \ or an effort setting: \ low, medium, "
                         r"high", width=6.3, color=POLICY),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3)).move_to(DOWN * 0.1)
        kl = label(r"Kimi's length reward, \ within each group of answers: \ shorter right answers earn more",
                   font_size=20, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The frontier recipes do the same, more carefully. <bookmark mark='a'/> Moonshot's Kimi k1.5 adds a length "
            "reward measured within each group: among right answers, shorter earns more. <bookmark mark='b'/> L1, from "
            "Carnegie Mellon, puts the desired length in the prompt and rewards the model for hitting it. "
            "<bookmark mark='c'/> DAPO penalizes only answers that run past a maximum length. <bookmark mark='d'/> "
            "And the products expose the dial directly: a budget of thinking tokens, or an effort setting of low, "
            "medium or high."
        ) as vo:
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15), *([FadeIn(kl)] if k == 0 else []))
        self.wait(0.3)
        self.clear_scene()
