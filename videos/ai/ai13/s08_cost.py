from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import A, MLPC, OURS, PART, curve, load

ATT, MLP_, NRM, EMB = A, MLPC, C.NORM, C.EMBED
GPT3_D = 12288  # Brown et al. (2020), Table 2.1: GPT-3 175B's d_model


class Cost(VoiceoverScene):
    def construct(self):
        self.card()
        self.params()
        self.flops()
        self.crossover()

    def card(self):
        card = chapter_card(7, r"What a block costs", r"How many numbers, and how much arithmetic, per character?",
                            lit=(2020,), part=PART)
        with self.voiceover("Chapter seven. What a block costs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def params(self):
        h = load("heads")
        d, L, K = int(h["d"]), int(h["L"]), int(h["K"])
        P = {k: int(v) for k, v in h["params"].items()}
        rows = [
            cmath(r"W_Q, W_K, W_V, W_O", r":", r"4\,d^2", font_size=34, colors={r"W_Q, W_K, W_V, W_O": ATT}),
            cmath(r"\text{MLP}", r":", r"d \cdot 4d + 4d \cdot d = 8\,d^2", font_size=34, colors={r"\text{MLP}": MLP_}),
            cmath(r"\text{one block}", r":", r"12\,d^2 + 9\,d", font_size=34),
            cmath(r"\text{the model}", r":", r"L\,(12\,d^2 + 9\,d) + 2Kd + 2d", font_size=34),
        ]
        whys = [why(r"four $d \times d$ matrices"), why(r"up to $4d$ and back"),
                why(r"$+$ biases and layer-norm gains, \ $9d$"), why(r"$+$ the character table in and out")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-2.4, buff=0.5, edge=6.9)
        tot = int(h["n_params"])
        fml = int(h["formula_total"])
        check = label(rf"$d = {d}, \ L = {L}, \ K = {K}$: \ formula ${fml:,}$, \ counted ${tot:,}$".replace(",", "{,}"),
                      font_size=24, color=C.TRUE_P).move_to([0, -0.55, 0])
        kinds = [("attention", ATT, r"attention"), ("mlp", MLP_, r"MLPs"), ("norm", NRM, r"norms"),
                 ("embed", EMB, r"character tables")]
        W = 11.0
        x = -W / 2
        bar = VGroup()
        for k, col, name in kinds:
            w = W * P[k] / tot
            r = Rectangle(width=max(w, 0.02), height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to([x + w / 2, -1.7, 0])
            t = label(rf"{name}: \ ${100 * P[k] / tot:.1f}\%$", font_size=20, color=col)
            bar.add(VGroup(r, t))
            x += w
        for i, (r, t) in enumerate(bar):
            t.next_to(r, DOWN if i % 2 == 0 else UP, buff=0.12)
        bar[2][1].next_to(bar[2][0], UP, buff=0.12).shift(LEFT * 0.4)
        bar[3][1].next_to(bar[3][0], DOWN, buff=0.12).shift(RIGHT * 0.2)
        keep_in_frame(bar)
        att_share = P["attention"] / (P["attention"] + P["mlp"])
        with self.voiceover(
            "First, the numbers a block stores. <bookmark mark='a'/> Attention has four d by d matrices: queries, "
            "keys, values and the output. <bookmark mark='b'/> The MLP goes up to four d and back: eight d squared. "
            "<bookmark mark='c'/> So a block is twelve d squared, plus a few biases and layer-norm gains. "
            "<bookmark mark='d'/> Add the table that turns characters into vectors and the one that turns vectors "
            f"back into guesses. <bookmark mark='e'/> For ours, with d of {d}, {L} blocks and {K} characters, the "
            f"formula gives {fml:,}, and counting the model's parameters one by one gives {tot:,}. "
            f"<bookmark mark='f'/> Attention is {att_share:.0%} of each block; the MLP holds the rest."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][0], color=ATT), GrowFromEdge(bar[0][0], LEFT))
            vo.wait_until("b")
            step(1)
            self.play(GrowFromEdge(bar[1][0], LEFT))
            vo.wait_until("c")
            step(2)
            self.play(GrowFromEdge(bar[2][0], LEFT))
            vo.wait_until("d")
            step(3)
            self.play(GrowFromEdge(bar[3][0], LEFT))
            vo.wait_until("e")
            self.play(FadeIn(check))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(b_[1]) for b_ in bar], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def flops(self):
        h = load("heads")
        d, L, K = int(h["d"]), int(h["L"]), int(h["K"])
        Ts = [int(v) for v in h["Ts"]]
        meas, form, kap = (np.asarray(h[k], float) for k in ("flops_per_token", "flops_formula", "flops_kaplan"))
        tr = float(h["flops_train_token"])
        i256 = Ts.index(256)
        rows = [
            cmath(r"\text{weights}", r":", r"2 \times 12\,L\,d^2 \;+\; 2\,d\,K", font_size=32, colors={r"\text{weights}": MLP_}),
            cmath(r"q \cdot k_j,\ \ \textstyle\sum_j p_j v_j", r":", r"2\,T\,d \;+\; 2\,T\,d \ \text{per layer}",
                  font_size=32, colors={r"q \cdot k_j,\ \ \textstyle\sum_j p_j v_j": ATT}),
            cmath(r"\text{per character}", r":", r"24\,L\,d^2 + 2dK + 4\,L\,T\,d", font_size=32),
        ]
        whys = [why(r"each weight: \ one multiply, one add"), why(r"$T$ keys, \ $d$ numbers each"),
                why(r"the full $T \times T$ square, \\ as our kernel computes it")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-2.6, buff=0.5, edge=6.9)
        xs = [-3.2, -0.6, 1.9, 4.4]
        head = VGroup(*[label(t_, font_size=20, color=GREY_A).move_to([x, -0.75, 0]) for t_, x in
                        zip((r"context $T$", r"measured", r"formula", r"causal half (Kaplan)"), xs)])
        tab = VGroup(head)
        for j, T in enumerate(Ts):
            y = -1.2 - 0.4 * j
            tab.add(VGroup(MathTex(str(T), font_size=24).move_to([xs[0], y, 0]),
                           MathTex(f"{meas[j]:,.0f}".replace(",", "{,}"), font_size=24, color=C.TRUE_P).move_to([xs[1], y, 0]),
                           MathTex(f"{form[j]:,.0f}".replace(",", "{,}"), font_size=24).move_to([xs[2], y, 0]),
                           MathTex(f"{kap[j]:,.0f}".replace(",", "{,}"), font_size=24, color=GREY_B).move_to([xs[3], y, 0])))
        exact = bool(np.allclose(meas, form, rtol=1e-6))
        match = "They match the formula exactly." if exact else "They match the formula to within a fraction of a percent."
        cap = note(r"floating-point operations per character, \ one forward pass, \ counted by PyTorch").to_corner(DL, buff=0.25)
        ratio = tr / meas[i256]
        with self.voiceover(
            "Now the arithmetic for each character. <bookmark mark='a'/> Every weight is used once per character, "
            "for one multiplication and one addition: two operations per weight. <bookmark mark='b'/> Attention "
            "adds work that no weight accounts for: the query against T keys, d numbers each, and the weighted sum "
            "of T values. <bookmark mark='c'/> Together, per character. <bookmark mark='d'/> We counted the "
            "operations of a real forward pass with PyTorch's counter, for contexts from "
            f"{Ts[0]} to {Ts[-1]:,} characters. "
            + match + " Jared Kaplan and colleagues' version counts only half the square, because the causal mask throws "
            "the other half away; kernels that skip the masked half really do save it. <bookmark mark='e'/> Training "
            f"costs more: a forward and a backward pass came to {ratio:.1f} times the forward alone, which is where "
            "the rule of six operations per weight per character comes from."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=MLP_))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(tab[0]), FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("e")
            self.play(Indicate(tab[1 + i256], color=C.TRUE_P))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def crossover(self):
        h = load("heads")
        d, L, K = int(h["d"]), int(h["L"]), int(h["K"])
        Tx = int(h["crossover_T"])
        Ts = [int(v) for v in h["Ts"]]
        meas = np.asarray(h["flops_per_token"], float)
        g = axes([1, 5, 1], [0, 1.0, 0.25], x_length=7.0, y_length=4.0, xlabel=r"context length $T$, \ characters",
                 ylabel=r"share of each character's arithmetic", xticks=[], yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", center=[-2.4, -0.35, 0])
        ax = g.ax
        for e in (1, 2, 3, 4, 5):
            g.add(MathTex(f"10^{{{e}}}", font_size=20, color=GREY_B).next_to(ax.c2p(e, 0), DOWN, buff=0.12))
        lt = np.linspace(1, 5, 200)
        T = 10 ** lt
        w = 24 * L * d * d + 2 * d * K
        att = 2 * L * T * d  # the causal half
        share = att / (att + w)
        c_att = curve(ax, lt, share, A, 3.5)
        c_w = curve(ax, lt, 1 - share, MLP_, 3.5)
        la = label(r"attention over the context", font_size=20, color=A).next_to(ax.c2p(4.6, float(np.interp(4.6, lt, share))), UP, buff=0.1)
        lw = label(r"the weights", font_size=20, color=MLP_).next_to(ax.c2p(1.4, float(np.interp(1.4, lt, 1 - share))), DOWN, buff=0.12)
        xl = math.log10(Tx)
        vx = DashedLine(ax.c2p(xl, 0), ax.c2p(xl, 1), color=WHITE, stroke_width=1.5)
        vxl = MathTex(r"T = 12\,d = " + f"{Tx:,}".replace(",", "{,}"), font_size=22).next_to(ax.c2p(xl, 0.05), RIGHT, buff=0.1)
        eq = cmath(r"2\,L\,T\,d", r"=", r"24\,L\,d^2", r"\;\Leftrightarrow\;", r"T = 12\,d", font_size=32).move_to([3.9, 2.4, 0])
        gx = 12 * GPT3_D
        facts = VGroup(label(rf"ours, \ $d = {d}$: \ $T = {Tx:,}$".replace(",", "{,}"), font_size=22, color=OURS),
                       label(rf"GPT-3, \ $d = {GPT3_D:,}$: \ $T = {gx:,}$".replace(",", "{,}"), font_size=22, color=GREY_A),
                       note(r"GPT-3's width: \ Brown et al.\ (2020), Table 2.1", font_size=18))
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.4, 1.0, 0])
        quad = label(r"and in total, \ over $T$ characters: \\ $T \times T$ \ grows as the square", font_size=22,
                     color=A).move_to([4.4, -1.4, 0])
        with self.voiceover(
            "Which term wins? <bookmark mark='a'/> Per character, attention's share grows with the context, the "
            "weights' does not. They are equal when two L T d equals twenty-four L d squared: when the context is "
            f"twelve times the width. <bookmark mark='b'/> For our model that is {Tx:,} characters, longer than "
            f"anything it reads, so its cost is mostly weights. For GPT-3, {gx:,} tokens. <bookmark mark='c'/> But "
            "the attention term has a sting: summed over a whole text of T characters it grows as T squared, and "
            "every past key and value has to be kept to write the next character. That is why long contexts are "
            "expensive, and why Parts 15, 16 and 19 exist."
        ) as vo:
            self.play(FadeIn(g), FadeIn(eq))
            vo.wait_until("a")
            self.play(Create(c_w), Create(c_att), FadeIn(la), FadeIn(lw), run_time=2.0)
            self.play(Create(vx), FadeIn(vxl))
            vo.wait_until("b")
            self.play(FadeIn(facts[0]))
            self.play(FadeIn(facts[1:]))
            vo.wait_until("c")
            self.play(FadeIn(quad))
        self.wait(0.3)
        self.clear_scene()
