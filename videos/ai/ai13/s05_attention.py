from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import MONO, curve, load
from videos.ai.ai20.common import show


class SparseAttention(VoiceoverScene):
    def construct(self):
        self.card()
        self.mass()
        self.choose()
        self.designs()
        self.exact()

    def card(self):
        card = chapter_card(4, r"Sparse attention", r"Does every query need every key?", part=13)
        with self.voiceover("Chapter four. Sparse attention."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def mass(self):
        t = load("topk")
        ks = [int(v) for v in t["ks"]]
        M = np.asarray(t["mass"])  # layer, head, k
        L, H, _ = M.shape
        lx = np.log2(ks)
        ax = Axes(x_range=[0, lx[-1], 1], y_range=[0, 1, 0.25], x_length=7.4, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.8, -0.5, 0])
        xt = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(np.log2(v), 0), DOWN, buff=0.1) for v in ks])
        yt = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0, 0.5, 1)])
        xn = label(r"the $k$ keys a query weights most \ (of $128$ to $256$)", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"share of its attention they hold", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        cols = [C.TRUE_P, C.INTERVAL, C.BITS, C.SURPRISE]
        lines = VGroup(*[curve(ax, lx, M[l_, h], cols[l_ % 4], 2.5).set_stroke(opacity=0.8) for l_ in range(L) for h in range(H)])
        key = VGroup(*[label(rf"layer {l_ + 1}", font_size=22, color=cols[l_ % 4]) for l_ in range(L)])
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 0.6, 0])
        m16 = float(M[..., ks.index(16)].mean())
        head = label(r"Part 11's transformer, \ every head, \ on held-out text", font_size=26).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Attention looks at every earlier token, but how much of that does it use? Take part eleven's "
            "transformer and, for each query, rank its keys by weight. <bookmark mark='a'/> Each line is one head: "
            "how much of the attention its top k keys hold. "
            f"On average, the top sixteen keys, out of between a hundred and twenty-eight and two hundred and fifty-six, "
            f"hold {100 * m16:.0f} percent. Most of the "
            "attention goes to a few keys."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.05), FadeIn(key), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def choose(self):
        t = load("topk")
        kk = [int(v) for v in t["kk"]]
        tk, wn = np.asarray(t["bits_topk"]), np.asarray(t["bits_window"])
        full = float(t["full"])
        lx = np.log2(kk)
        lo = math.floor((full - 0.05) / 0.25) * 0.25
        hi = math.ceil((max(wn.max(), tk.max()) + 0.05) / 0.25) * 0.25
        ax = Axes(x_range=[lx[0] - 0.3, lx[-1] + 0.3, 1], y_range=[lo, hi, 0.25], x_length=7.4, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.8, -0.5, 0])
        xt = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(np.log2(v), lo), DOWN, buff=0.1) for v in kk])
        xn = label(r"keys each query may use, \ $k$", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yt = VGroup(*[MathTex(f"{v:.2f}", font_size=22, color=GREY_B).next_to(ax.c2p(lx[0] - 0.3, v), LEFT, buff=0.1)
                      for v in np.arange(lo, hi + 1e-9, 0.25)])
        yn = label(r"bits per character", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        fl = DashedLine(ax.c2p(lx[0] - 0.3, full), ax.c2p(lx[-1] + 0.3, full), color=GREY_B, stroke_width=1.5)
        fll = label(rf"all keys: \ ${full:.3f}$", font_size=22, color=GREY_B).next_to(ax.c2p(lx[-1] + 0.3, full), UR, buff=0.05)
        cw = VGroup(curve(ax, lx, wn, C.SURPRISE, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=C.SURPRISE) for a, b in zip(lx, wn)])
        ct = VGroup(curve(ax, lx, tk, C.INTERVAL, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=C.INTERVAL) for a, b in zip(lx, tk)])
        k1 = label(r"the last $k$ keys \ (a sliding window)", font_size=24, color=C.SURPRISE).move_to([4.4, 1.6, 0])
        k2 = label(r"the $k$ highest-scoring keys", font_size=24, color=C.INTERVAL).next_to(k1, DOWN, buff=0.3).align_to(k1, LEFT)
        i8 = kk.index(8)
        with self.voiceover(
            "So let each query use only k keys. Which k? <bookmark mark='a'/> The simplest choice is the most recent "
            f"ones, a sliding window: with {kk[i8]} keys, {wn[i8]:.2f} bits a character. <bookmark mark='b'/> Better, "
            f"take the {kk[i8]} keys it would weight most: {tk[i8]:.2f}. With {kk[-1]}, "
            + (f"it's within {tk[-1] - full:.3f} bits of using everything."
               if tk[-1] - full >= 0.0005 else "it's within a thousandth of a bit of using everything.")
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(fl), FadeIn(fll))
            vo.wait_until("a")
            self.play(Create(cw[0]), FadeIn(cw[1:]), FadeIn(k1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ct[0]), FadeIn(ct[1:]), FadeIn(k2), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def designs(self):
        r = load("row")
        w, text = np.asarray(r["weights"], float), str(r["text"])
        n = len(w)
        blk = n // len(r["blocks"])
        x0, pitch = -4.2, 10.8 / n
        xs = [x0 + pitch * (i + 0.5) for i in range(n)]

        def cells(y, h=0.3):
            return VGroup(*[Rectangle(width=pitch * 0.86, height=h, stroke_color=GREY_D, stroke_width=1, fill_opacity=0).move_to([x, y, 0])
                            for x in xs])

        def lit(row, idx, color):
            return [row[i].animate.set_fill(color, 0.85).set_stroke(color) for i in idx]

        def side(y, name, sub, color, held, keys):
            g = VGroup(label(name, font_size=24, color=color))
            if sub:
                g.add(label(sub, font_size=18, color=color))
            g.add(label(rf"${keys}$ keys \ hold ${100 * held:.0f}\%$", font_size=20, color=GREY_A))
            return g.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-5.6, y, 0]).align_to([-6.8, 0, 0], LEFT)

        # the query's real weights, over its last 48 keys
        strip = VGroup(*[VGroup(Rectangle(width=pitch * 0.86, height=0.36, stroke_color=GREY_C, stroke_width=1),
                                Text(show(ch), font=MONO, font_size=15, color=GREY_A)) for ch in text])
        for c, x in zip(strip, xs):
            c.move_to([x, 1.25, 0])
            c[1].move_to(c[0])
        strip[-1][0].set_stroke(C.BITS, 2.5)
        ql = label(r"the query", font_size=18, color=C.BITS).next_to(strip[-1], DOWN, buff=0.1).align_to(strip[-1], RIGHT)
        bars = VGroup(*[Rectangle(width=pitch * 0.7, height=max(1.25 * v / w.max(), 0.01), stroke_width=0, fill_color=C.TRUE_P,
                                  fill_opacity=0.9).move_to([x, 1.5, 0], aligned_edge=DOWN) for x, v in zip(xs, w)])
        bl = label(r"how much \\ it weighs each key", font_size=20, color=C.TRUE_P).move_to([-5.6, 2.1, 0]).align_to([-6.8, 0, 0], LEFT)
        head = label(rf"one query of Part 11's transformer \ (layer ${int(r['layer']) + 1}$, \ head ${int(r['head']) + 1}$): "
                     r"\ its last $48$ keys", font_size=26).to_edge(UP, buff=0.3)
        divs = VGroup(*[DashedLine([x0 + pitch * blk * j, 1.0, 0], [x0 + pitch * blk * j, 2.85, 0], dash_length=0.05, stroke_width=1,
                                   color=GREY_C) for j in range(1, n // blk)])
        # three ways to keep 8 to 24 of them
        top = [int(i) for i in r["top"]]
        chosen = [int(c) for c in r["chosen"]]
        nsa_idx = sorted({i for c in chosen for i in range(c * blk, (c + 1) * blk)} | set(range(n - 8, n)))
        y_w, y_n, y_d = 0.05, -1.15, -2.45
        win_row, nsa_row, dsa_row = cells(y_w), cells(y_n), cells(y_d)
        s_w = side(y_w, r"sliding window", None, C.SURPRISE, float(r["window"]), 8)
        s_n = side(y_n, r"NSA", r"DeepSeek, \ 2025", C.BITS, float(r["nsa"]), int(r["nsa_keys"]))
        s_d = side(y_d, r"DSA", r"DeepSeek-V3.2, \ 2025", C.INTERVAL, float(r["topk"]), len(top))
        bm = np.asarray(r["blocks"], float)
        summ = VGroup(*[Rectangle(width=pitch * blk - 0.06, height=0.3, stroke_color=C.BITS, stroke_width=1.5, fill_color=C.BITS,
                                  fill_opacity=0.1 + 0.8 * v / bm.max()).move_to([x0 + pitch * blk * (j + 0.5), y_n, 0])
                        for j, v in enumerate(bm)])
        sl = label(r"each block of $8$ squeezed into one summary", font_size=18, color=C.BITS).next_to(summ, DOWN, buff=0.1)
        idx = VGroup(*[Rectangle(width=pitch * 0.5, height=max(0.5 * v / w.max(), 0.01), stroke_width=0, fill_color=GREY_B,
                                 fill_opacity=0.8).move_to([x, y_d + 0.2, 0], aligned_edge=DOWN) for x, v in zip(xs, w)])
        il = label(r"a tiny indexer scores every key \ (here: \ the real weights, \ an ideal indexer)", font_size=18,
                   color=GREY_B).next_to(dsa_row, DOWN, buff=0.12)
        catch = label(r"the catch: \ finding the top keys must cost far less than attending to all of them", font_size=24,
                      color=C.BITS).to_edge(DOWN, buff=0.55)
        cite_ = cite(r"J.~Yuan et al., \textit{Native Sparse Attention} (2025); \ DeepSeek-AI, \textit{DeepSeek-V3.2-Exp} (2025)",
                     corner=DR)
        with self.voiceover(
            "Choosing by score is what real models now do. <bookmark mark='a'/> Here's one query in our transformer, "
            f"and how it weighs its last forty-eight keys. Together they hold {100 * float(r['strip_mass']):.0f} percent "
            "of its attention, and most of it lands on a handful of characters well back from the end. "
            "<bookmark mark='b'/> A sliding window keeps only the last eight keys: they hold just "
            f"{100 * float(r['window']):.0f} percent. <bookmark mark='c'/> DeepSeek's native sparse attention cuts the "
            "past into blocks and squeezes each one into a summary. <bookmark mark='d'/> The query scores the "
            "summaries, reads the best blocks in full, and keeps a window of recent tokens too: "
            f"{100 * float(r['nsa']):.0f} percent, from {int(r['nsa_keys'])} keys. <bookmark mark='e'/> In "
            "DeepSeek-V3.2, a tiny, fast indexer gives every past token a score, and the query attends to the top "
            f"ones only: two thousand and forty-eight in the real model, eight here, holding "
            f"{100 * float(r['topk']):.0f} percent. <bookmark mark='f'/> The trick in both is that finding the "
            "important keys must be much cheaper than attending to all of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), LaggedStart(*[FadeIn(c) for c in strip], lag_ratio=0.02), FadeIn(ql))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.02), FadeIn(bl), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(win_row), FadeIn(s_w[:-1]))
            self.play(LaggedStart(*lit(win_row, range(n - 8, n), C.SURPRISE), lag_ratio=0.08), FadeIn(s_w[-1]))
            vo.wait_until("c")
            self.play(Create(divs))
            self.play(*[ReplacementTransform(VGroup(*[strip[i][0].copy() for i in range(j * blk, (j + 1) * blk)]), summ[j])
                        for j in range(len(summ))], FadeIn(s_n[:-1]), FadeIn(sl), run_time=1.5)
            vo.wait_until("d")
            self.play(*[Indicate(summ[c], color=C.BITS, scale_factor=1.1) for c in chosen])
            self.add(nsa_row)
            self.play(FadeOut(summ), FadeOut(sl), *lit(nsa_row, nsa_idx, C.BITS), FadeIn(s_n[-1]), run_time=1.2)
            vo.wait_until("e")
            self.play(FadeIn(dsa_row), FadeIn(s_d[:-1]), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in idx], lag_ratio=0.01),
                      FadeIn(il), run_time=1.2)
            self.play(LaggedStart(*lit(dsa_row, top, C.INTERVAL), lag_ratio=0.1), FadeIn(s_d[-1]),
                      idx.animate.set_fill(opacity=0.25))
            vo.wait_until("f")
            self.play(FadeIn(catch))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exact(self):
        colors = {r"g^{c}_t": C.BITS, r"I_{t,s}": C.INTERVAL}
        nsa = VGroup(
            label(r"NSA:", font_size=26, color=C.BITS),
            cmath(r"o_t = \sum_{c \,\in\, \{\text{cmp},\ \text{slc},\ \text{win}\}}", r"g^{c}_t", r"\cdot \operatorname{Attn}\big(q_t,\ "
                  r"\tilde K^{c}_t,\ \tilde V^{c}_t\big)", colors=colors, font_size=32),
        ).arrange(RIGHT, buff=0.4)
        nn_ = label(r"three branches: \ block summaries, \ the chosen blocks in full, \ a recent window; \ "
                    r"learned gates $g$ mix them", font_size=20, color=GREY_A)
        dsa = VGroup(
            label(r"DSA:", font_size=26, color=C.INTERVAL),
            cmath(r"I_{t,s}", r"= \sum_{j=1}^{H^{I}} w_{t,j}\, \operatorname{ReLU}\big(q^{I}_{t,j} \cdot k^{I}_{s}\big)", colors=colors,
                  font_size=32),
        ).arrange(RIGHT, buff=0.4)
        dn = label(r"a few small heads, \ in $8$-bit numbers \ ($256$ possible values): \ cheap to run over every past token", font_size=20, color=GREY_A)
        dsa2 = cmath(r"o_t = \operatorname{Attn}\big(q_t,\ \{k_s, v_s : I_{t,s} \in \operatorname{top}_{2048}\}\big)", font_size=32)
        cost = MathTex(r"\underbrace{O(L^2)}_{\text{tiny indexer}} \;+\; \underbrace{O(L \cdot 2048)}_{\text{real attention}}",
                       font_size=32, color=GREY_A)
        g = VGroup(nsa, nn_, dsa, dn, dsa2, cost).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([0, -0.1, 0])
        sq = label(r"$O(L^2)$: \ grows like $L^2$, \ the length squared", font_size=20, color=GREY_A)
        nn_.shift(RIGHT * 0.9)
        dn.shift(RIGHT * 0.9)
        dsa2.shift(RIGHT * 0.9)
        cost.shift(RIGHT * 0.9)
        sq.next_to(cost, RIGHT, buff=0.5)
        head = label(r"the two designs, \ exactly", font_size=28).to_edge(UP, buff=0.35)
        cite_ = cite(r"J.~Yuan et al.\ (2025); \ DeepSeek-AI, \textit{DeepSeek-V3.2-Exp} (2025)", corner=DR)
        with self.voiceover(
            "In equations: <bookmark mark='a'/> NSA's output is a gated sum of three attentions, over the block "
            "summaries, over the chosen blocks in full, and over a recent window, with gates the model learns. "
            "<bookmark mark='b'/> DSA's indexer scores each past token with a few small heads: a weighted sum of "
            "rectified dot products, where any negative score is set to zero, part eight's ReLU, all computed in "
            "eight-bit numbers: each rounded to one of two hundred and fifty-six values, to save time and memory. <bookmark mark='c'/> Then real attention runs "
            "over the top two thousand and forty-eight. <bookmark mark='d'/> The indexer still looks at every pair, "
            "but it's so small that the expensive part now grows with the length times two thousand, not the length "
            "squared."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Write(nsa), FadeIn(nn_))
            vo.wait_until("b")
            self.play(Write(dsa), FadeIn(dn))
            vo.wait_until("c")
            self.play(Write(dsa2))
            vo.wait_until("d")
            self.play(Write(cost), FadeIn(sq))
        self.wait(0.3)
        self.clear_scene()
