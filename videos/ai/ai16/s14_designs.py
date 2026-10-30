from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (BLOCKC, F, FULLC, HISTC, INDEXC, MONO, PART, WINC, load, ms, show, take_away)


class Designs(VoiceoverScene):
    def construct(self):
        self.card()
        self.designs()
        self.exact()
        self.recall_setup()
        self.recall_result()
        self.v4()

    def card(self):
        card = chapter_card(13, r"Sparse attention by design", r"Can a model learn which keys to read?", lit=(2025,), part=PART)
        with self.voiceover("Chapter thirteen. Sparse attention, by design."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

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
        head = label(rf"one query of Part 13's transformer \ (layer ${int(r['layer']) + 1}$, \ head ${int(r['head']) + 1}$): "
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
            "rectified dot products, where any negative score is set to zero, part nine's ReLU, all computed in "
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

    # ------------------------------------------------------------------
    def recall_setup(self):
        from videos.ai.ai16 import recall as Q

        d = load("recall")
        toks = np.asarray(d["example_tokens"], int)
        q = int(d["example_q"])
        ans = int(d["example_answer_pos"])

        def name(t):
            if t == Q.BOS:
                return r"\texttt{>}"
            if t < Q.ASK0:
                return rf"{(t - Q.FACT0) // Q.NV}{{\to}}{(t - Q.FACT0) % Q.NV}"
            if t < Q.VAL0:
                return rf"{t - Q.ASK0}?"
            if t < Q.FILL0:
                return rf"{t - Q.VAL0}"
            return r"\cdot"

        n = len(toks)
        cw = 13.0 / n
        row = VGroup()
        for i, t in enumerate(toks):
            col = (C.BITS if t < Q.ASK0 else C.TRUE_P if t < Q.VAL0 else C.INTERVAL if t < Q.FILL0 else GREY_D)
            box = Rectangle(width=cw * 0.92, height=0.5, stroke_width=0.8, stroke_color=col, fill_color=col,
                            fill_opacity=0.25 if t < Q.FILL0 else 0.08)
            row.add(box.move_to([-6.5 + cw * (i + 0.5), 1.6, 0]))
        labs = VGroup(label(r"$8$ facts: \ key $\to$ value, \ one token each", font_size=20, color=C.BITS),
                      label(r"$40$ filler tokens", font_size=20, color=GREY_B),
                      label(r"then each key is asked: \ \textit{key?} \ \textit{answer}", font_size=20, color=C.TRUE_P))
        labs[0].next_to(row[1:9], UP, buff=0.2)
        labs[1].next_to(row[9:49], UP, buff=0.2)
        labs[2].next_to(row[49:], UP, buff=0.2).align_to(row, RIGHT)
        zoom = VGroup(*[label(rf"${name(int(toks[i]))}$", font_size=22, color=WHITE) for i in range(1, 9)])
        zoom.arrange(RIGHT, buff=0.35).move_to([-3.0, 0.4, 0])
        qz = VGroup(*[label(rf"${name(int(toks[i]))}$", font_size=22, color=WHITE) for i in range(49, 57)])
        qz.arrange(RIGHT, buff=0.3).move_to([3.4, 0.4, 0])
        arc = CurvedArrow(row[q].get_bottom() + DOWN * 0.05, row[ans].get_bottom() + DOWN * 0.05, angle=-PI / 3,
                          color=FULLC, stroke_width=2.5, tip_length=0.15)
        rules = VGroup(
            label(rf"every sparse pattern gets ${int(d['keys'])}$ keys per query:", font_size=22, color=GREY_A),
            label(rf"a sliding window of ${int(d['keys'])}$", font_size=22, color=WINC),
            label(r"block selection: \ its own block of $4$, \ and the one block whose mean key scores best \ (MoBA, NSA)",
                  font_size=22, color=BLOCKC),
            label(rf"a learned indexer: \ any ${int(d['keys'])}$ keys \ (DSA)", font_size=22, color=INDEXC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        tag = note(r"after Zoology's associative recall (Arora et al., 2023)", font_size=17).to_corner(UR, buff=0.2)
        with self.voiceover(
            "Can a model learn where to look? We need a task where it matters. <bookmark mark='a'/> Each sequence "
            "starts with eight facts, each a single token that binds a key to a value: key three goes with value "
            "eleven, say. <bookmark mark='b'/> Then forty tokens of filler. <bookmark mark='c'/> Then each key is "
            "asked, and the model must answer with its value. The fact it needs is at least forty tokens back. "
            "<bookmark mark='d'/> We train our small transformer on it with full attention, and with three sparse "
            f"patterns that each allow {int(d['keys'])} keys per query: a sliding window; block selection, the "
            "query's own block of four and the one block whose average key it scores best, as in MoBA and NSA; and "
            "a learned indexer that may pick any keys, as in DeepSeek's sparse attention."
        ) as vo:
            self.play(FadeIn(row), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(labs[0]), FadeIn(zoom))
            vo.wait_until("b")
            self.play(FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(FadeIn(labs[2]), FadeIn(qz), Create(arc))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rules], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recall_result(self):
        d = load("recall")
        S = int(d["steps"])
        keys = [("full", r"full attention", FULLC), ("window", rf"sliding window", WINC),
                ("blocks", r"block selection", BLOCKC), ("index", r"learned indexer", INDEXC)]
        ax = Axes(x_range=[0, S + int(d["idx_steps"]), 250], y_range=[0, 1, 0.25], x_length=7.4, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.0, -0.2, 0])
        yt = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 0.5, 1)])
        xt = VGroup(*[MathTex(f"{v:,}".replace(",", "{,}"), font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (0, S, S + int(d["idx_steps"]))])
        xl = label(r"training steps", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"answers right \ (two seeds; \ chance: $1$ in $16$)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        lines = {}
        for k, nm, col in keys:
            a = np.asarray(d[f"{k}_curve"], float)
            if k == "index":
                a = a.copy()
                a[:, :, 0] += S
            xs = a[0, :, 0]
            lines[k] = VGroup(band(ax, xs, a[:, :, 1].min(0), a[:, :, 1].max(0), col, 0.2),
                              curve(ax, xs, a[:, :, 1].mean(0), col, 3))
        warm = DashedLine(ax.c2p(S, 0), ax.c2p(S, 1), color=GREY_C, stroke_width=1.5)
        wl = label(r"indexer: \ from the full model", font_size=16, color=INDEXC).next_to(ax.c2p(S, 1), UR, buff=0.05)
        acc = {k: ms(d[f"{k}_acc"])[0] for k, _, _ in keys}
        names = VGroup(*[label(rf"{nm}: \ ${100 * acc[k]:.0f}\%$", font_size=22, color=col) for k, nm, col in keys])
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.6, 1.2, 0])
        keep_in_frame(names)
        imp = VGroup(label(r"the full models, \ a pattern imposed \\ without retraining:", font_size=20, color=GREY_A),
                     *[label(rf"{nm}: \ ${100 * ms(d[f'imposed_{k}_acc'])[0]:.0f}\%$", font_size=20, color=col)
                       for k, nm, col in ((("window", r"window", WINC), ("blocks", r"blocks", BLOCKC),
                                           ("topk", r"its own top $8$", C.ATTN)))])
        imp.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(names, DOWN, buff=0.45).align_to(names, LEFT)
        fw, ww, bw, iw = acc["full"], acc["window"], acc["blocks"], acc["index"]
        v1 = (f"Full attention learns it completely: {100 * fw:.0f} percent. The sliding window can't see the facts, "
              f"and stays near chance, {100 * ww:.0f} percent. " if ww < 0.3 else
              f"Full attention reaches {100 * fw:.0f} percent, and the window {100 * ww:.0f}. ")
        if bw > 0.8:
            v2 = f"Block selection gets {100 * bw:.0f} percent: it learns to find the right block. "
        elif bw > 0.3:
            v2 = (f"Block selection gets {100 * bw:.0f} percent: an average key is a blurry summary, and sometimes it "
                  "picks the wrong block. ")
        else:
            v2 = (f"Block selection gets {100 * bw:.0f} percent: an average key is too blurry a summary to find the "
                  "right block. ")
        v3 = (f"And the learned indexer, started from the full model, reaches {100 * iw:.0f} percent with eight keys. "
              if iw > 0.8 else
              f"The learned indexer, started from the full model, reaches {100 * iw:.0f} percent. ")
        ti = ms(d["imposed_topk_acc"])[0]
        if ti > 0.8:
            v4 = (f"Imposing a pattern on the full model without retraining is a different story: its own top eight "
                  f"keys keep {100 * ti:.0f} percent, so the information is there, if you can find it cheaply. ")
        else:
            v4 = (f"Imposing a pattern on the full model without retraining is a different story: even its own top "
                  f"eight keys keep only {100 * ti:.0f} percent. ")
        with self.voiceover(
            "Here's training, the share of answers right. <bookmark mark='a'/> " + v1 + "<bookmark mark='b'/> " + v2
            + "<bookmark mark='c'/> " + v3 + "<bookmark mark='d'/> " + v4
        ) as vo:
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(lines["full"]), FadeIn(names[0]), FadeIn(lines["window"]), FadeIn(names[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(lines["blocks"]), FadeIn(names[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(warm), FadeIn(wl), FadeIn(lines["index"]), FadeIn(names[3]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(imp))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def v4(self):
        a = F.DSV4_ATT
        rows = VGroup(
            label(r"DeepSeek-V4 \ (April 2026): \ two kinds of attention layer, \ interleaved", font_size=34),
            label(rf"compressed sparse attention: \ every ${a['m']}$ keys and values squeezed into one entry; \\ a "
                  rf"lightning indexer picks the top ${a['topk'][0]:,}$; \ plus a window of the last ${a['window']}$"
                  .replace(",", "{,}"), font_size=26, color=INDEXC),
            label(rf"heavily compressed attention: \ every ${a['m2']}$ squeezed into one, \ read in full", font_size=26,
                  color=BLOCKC),
            label(rf"the indexer: \ ${a['idx_heads']}$ heads of ${a['idx_dim']}$, \ in ${a['idx_bits']}$-bit numbers", font_size=26,
                  color=GREY_A),
            label(rf"at a million tokens: \ ${100 * a['flops']:.0f}\%$ of V3.2's computation per token, \ "
                  rf"${100 * a['kv']:.0f}\%$ of its cache \ (its makers' figures)", font_size=26, color=C.BITS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.5, 0])
        if rows.width > 13.0:
            rows.width = 13.0
        cite_ = cite(r"DeepSeek-AI, \textit{DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence} (2026)",
                     corner=UL, font_size=18)
        ta = take_away(r"sparse attention, 2026: \ compress, \ then choose \ \textperiodcentered\ \ the cache it saves: \ Part 15; \ "
                       r"serving it: \ Part 19", color=INDEXC, font_size=22)
        with self.voiceover(
            "This year's frontier combines the ideas. <bookmark mark='a'/> DeepSeek-V4, released in April 2026, "
            f"compresses every {a['m']} keys and values into one entry, and a lightning indexer chooses the best "
            f"{a['topk'][0]:,} of those for each query, with a window of the last {a['window']} tokens for local detail. "
            f"<bookmark mark='b'/> Other layers compress {a['m2']} to one and read everything that's left. "
            f"<bookmark mark='c'/> Its indexer has {a['idx_heads']} heads, computed in {a['idx_bits']}-bit numbers. "
            f"<bookmark mark='d'/> At a million tokens, DeepSeek reports {100 * a['flops']:.0f} percent of V3.2's "
            f"computation per token and {100 * a['kv']:.0f} percent of its cache. What the cache saves is part "
            "fifteen's subject, and serving it is part nineteen's."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(cite_))
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[i + 1], shift=RIGHT * 0.1))
            self.play(FadeIn(ta))
        self.wait(0.3)
        self.clear_scene()
