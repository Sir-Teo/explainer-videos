from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import fmt_int, K, MIX_C, MIX_NAME, MIX_SHORT, MONO, PART, V, axes, curve, load


class Recall(VoiceoverScene):
    def construct(self):
        self.card()
        self.task()
        self.replay()
        self.results()
        self.lesson()

    def card(self):
        card = chapter_card(11, r"A recall test", r"Which memory can look things up?", lit=(2017,), part=PART)
        with self.voiceover("Chapter eleven. A recall test."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def task(self):
        m = load("mqar")
        pairs = [("A", "4"), ("Q", "7"), ("M", "2"), ("D", "9"), ("X", "1")]
        boxes = VGroup()
        for kk, vv in pairs:
            boxes.add(VGroup(data_text(kk, font=MONO, font_size=30, color=K), data_text(vv, font=MONO, font_size=30, color=V))
                      .arrange(RIGHT, buff=0.12))
        boxes.arrange(RIGHT, buff=0.45).move_to(UP * 2.0 + LEFT * 1.5)
        qs = VGroup(*[data_text(c_, font=MONO, font_size=30, color=K) for c_ in ("M", "A", "X")]).arrange(RIGHT, buff=0.45)
        qs.next_to(boxes, RIGHT, buff=0.9)
        ans = VGroup(*[data_text(c_, font=MONO, font_size=30, color=C.BITS) for c_ in ("2", "4", "1")])
        for a_, q_ in zip(ans, qs):
            a_.next_to(q_, DOWN, buff=0.35)
        bl = label(r"pairs: \ a key, then its value", font_size=24, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        ql = label(r"then keys again: \ answer with their values", font_size=24, color=C.BITS).next_to(ans, DOWN, buff=0.3)
        mix = list(m["mixers"])
        N, steps = int(m["N"]), int(m["steps"])
        dks = [int(x) for x in m["dks"]]
        p = [int(m[f"params_{k}"]) for k in mix]
        setup = VGroup(*[label(MIX_NAME[k].replace(r"\\", r"\ "), font_size=20, color=MIX_C[k]) for k in mix])
        setup.arrange_in_grid(rows=2, cols=3, buff=(0.5, 0.18)).move_to(DOWN * 1.1)
        rule = label(rf"two layers each, \ ${fmt_int(min(p))}$--${fmt_int(max(p))}$ weights, \ ${fmt_int(steps)}$ steps; \ ${N}$ pairs; \ "
                     rf"keys of ${dks[0]}$ to ${dks[-1]}$ numbers; \ {len(m['seeds'])} seeds",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.45)
        cite_ = cite(r"S.~Arora et al., \textit{Zoology: Measuring and Improving Recall in Efficient Language Models} (2023)",
                     corner=UR, font_size=17)
        with self.voiceover(
            "Here's a test of pure memory, multi-query associative recall, from Simran Arora and colleagues at "
            "Stanford: a list of keys, each followed by its value; <bookmark mark='a'/> then some of the keys again, "
            "in a new order, and the model must answer with their values. It's the skill a model needs to quote a "
            "name or a number from far back in a document, and in 2023 they found it explains most of the gap in "
            "quality between attention and the fast memories. <bookmark mark='b'/> We trained six kinds of small "
            "two-layer models on it: softmax attention, linear attention, a Mamba-2-style selective state-space "
            "model, the delta rule, the gated delta rule, and a hybrid with a gated delta layer under an attention "
            f"layer. <bookmark mark='c'/> Lists of {N} pairs, keys from {dks[0]} to {dks[-1]} numbers long, so the "
            "fixed memories range from far too small to big enough; the same weights, give or take a few gates, the "
            f"same {steps:,} steps, {len(m['seeds'])} seeds each."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes], lag_ratio=0.2), FadeIn(bl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(qs))
            self.play(LaggedStart(*[FadeIn(a_, shift=DOWN * 0.15) for a_ in ans], lag_ratio=0.3), FadeIn(ql))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in setup], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        m = load("mqar")
        mix = list(m["mixers"])
        dk = int(m["replay_dk"])
        steps = np.asarray(m["curve_steps"], float)
        picks = {k: np.asarray(m[f"picks_{k}"]) for k in mix}
        di = [int(x) for x in m["dks"]].index(dk)
        curves = {k: np.asarray(m[f"curves_{k}"])[di, 0] for k in mix}
        n_ev, N = picks[mix[0]].shape
        cell = 0.26
        grids, names = VGroup(), VGroup()
        for r, k in enumerate(mix):
            y = 2.3 - r * 0.62
            g = VGroup(*[Square(cell, stroke_width=0.8, stroke_color=GREY_D, fill_color=GREY_D, fill_opacity=0.3)
                         .move_to([-5.0 + 2.3 + q * (cell + 0.04), y, 0]) for q in range(N)])
            grids.add(g)
            names.add(label(MIX_SHORT[k], font_size=20, color=MIX_C[k]).next_to(g, LEFT, buff=0.25))
        gl = label(rf"one fixed list of ${N}$ pairs: \ each square an answer, \ lit when right \ (key size ${dk}$, seed $0$)",
                   font_size=18, color=GREY_A).next_to(grids, UP, buff=0.2).align_to(names, LEFT)
        g2 = axes([0, steps[-1]], [0, 1], x_length=5.0, y_length=3.4, xlabel=r"training steps",
                  ylabel=r"answers right, \ fixed batch", xticks=[0, steps[-1] / 2, steps[-1]], yticks=[0, 0.5, 1],
                  center=[3.9, -1.0, 0], xfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), yfmt=lambda v: rf"{int(100 * v)}\%")
        ax = g2.ax
        tk = ValueTracker(0)

        def make_lines():
            n = max(2, int(round(tk.get_value())) + 1)
            return VGroup(*[curve(ax, steps[:n], curves[k][:n], MIX_C[k], 3) for k in mix])

        lines = always_redraw(make_lines)
        counter = VGroup(label(r"step", font_size=22, color=GREY_A), Integer(0, font_size=26)).arrange(RIGHT, buff=0.15)
        counter.next_to(g2, UP, buff=0.2)

        def paint(e):
            anims = []
            for r, k in enumerate(mix):
                for q in range(N):
                    ok = bool(picks[k][e, q])
                    anims.append(grids[r][q].animate.set_fill(MIX_C[k] if ok else GREY_D, opacity=0.9 if ok else 0.3))
            return anims

        first = {k: next((int(steps[e]) for e in range(n_ev) if picks[k][e].mean() >= 0.5), None) for k in mix}
        quick = sorted([k for k in mix if first[k] is not None], key=lambda k: first[k])
        never = [k for k in mix if first[k] is None]
        nm = {k: MIX_SHORT[k].replace("$", "") for k in mix}
        v1 = (f"The first to get half of this list right is {nm[quick[0]]}, by step {first[quick[0]]:,}; "
              if quick else "None of them gets half of this list right; ")
        v2 = (f"the last, {nm[quick[-1]]}, by step {first[quick[-1]]:,}. " if len(quick) > 1 else "")
        v3 = (f"{len(never)} of the six never get there in this run." if len(never) > 1 else
              f"One, {nm[never[0]]}, never gets there in this run." if never else "")
        with self.voiceover(
            "Here is training, replayed, for keys of " + f"{dk} numbers. On the left, one list the models never "
            "train on: each square is one of its answers, lit when the model gets it right. On the right, the share "
            "right on a fixed batch. <bookmark mark='a'/> At first every model guesses. Then, one by one, they "
            "discover the trick: find the earlier copy of the key, and copy what came after it. <bookmark mark='b'/> "
            + v1 + "<bookmark mark='c'/> " + v2 + "<bookmark mark='d'/> " + v3
        ) as vo:
            self.play(FadeIn(grids), FadeIn(names), FadeIn(gl), FadeIn(g2), FadeIn(counter))
            self.add(lines)
            counter[1].add_updater(lambda c_: c_.set_value(int(steps[min(int(round(tk.get_value())), n_ev - 1)])))
            vo.wait_until("a")
            for e in range(1, n_ev):
                if e == n_ev // 3:
                    vo.wait_until("b")
                self.play(tk.animate.set_value(e), *paint(e), run_time=max(0.25, (vo.duration - 6) / n_ev * 0.6),
                          rate_func=linear)
        counter[1].clear_updaters()
        lines.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        m = load("mqar")
        mix = list(m["mixers"])
        dks = [int(x) for x in m["dks"]]
        acc = {k: np.asarray(m[f"acc_{k}"]) for k in mix}  # (dks, seeds)
        lx = np.log2(dks)
        g = axes([lx[0] - 0.3, lx[-1] + 0.3], [0, 1.02], x_length=7.4, y_length=4.4,
                 xlabel=r"key size: \ the fixed memories hold key size $\times\ 64$ numbers a layer",
                 ylabel=r"answers right, \ $1{,}024$ fresh lists", xticks=list(lx), yticks=[0, 0.25, 0.5, 0.75, 1],
                 xfmt=lambda v: f"{int(round(2 ** v))}", yfmt=lambda v: rf"{int(100 * v)}\%", center=[-1.7, -0.45, 0])
        ax = g.ax
        dots, lines = VGroup(), VGroup()
        off = np.linspace(-0.12, 0.12, len(mix))
        for j, k in enumerate(mix):
            for i in range(len(dks)):
                for s_ in range(acc[k].shape[1]):
                    dots.add(Dot(ax.c2p(lx[i] + off[j], acc[k][i, s_]), radius=0.045, color=MIX_C[k]).set_opacity(0.85))
            lines.add(curve(ax, lx + off[j], acc[k].mean(1), MIX_C[k], 3))
        leg = legend([(MIX_C[k], MIX_NAME[k].replace(r"\\", r"\ ")) for k in mix], font_size=17).move_to([4.6, 0.9, 0])
        cap = note(r"each dot one seed; \ lines: \ the mean", font_size=16).next_to(leg, DOWN, buff=0.3).align_to(leg, LEFT)
        mean = {k: acc[k].mean(1) for k in mix}
        nm = {k: MIX_SHORT[k].replace("$", "") for k in mix}
        small = sorted(mix, key=lambda k: -mean[k][0])
        lin_last = mean["linear"][-1]
        v_small = (f"With keys of {dks[0]} numbers, softmax attention gets {100 * mean['softmax'][0]:.0f} percent, "
                   f"the hybrid {100 * mean['hybrid'][0]:.0f}; of the fixed memories, {nm[[k for k in small if k not in ('softmax', 'hybrid')][0]]} "
                   f"does best, {100 * max(mean[k][0] for k in mix if k not in ('softmax', 'hybrid')):.0f} percent. ")
        fixed = [k for k in mix if k not in ("softmax", "hybrid", "linear")]
        v_big = (f"With keys of {dks[-1]}, the fixed memories that can forget or correct reach "
                 f"{100 * min(mean[k][-1] for k in fixed):.0f} to {100 * max(mean[k][-1] for k in fixed):.0f} percent, "
                 f"but linear attention, which only adds, stays at {100 * lin_last:.0f}. ")
        spread = max(float(acc[k][i].max() - acc[k][i].min()) for k in mix for i in range(len(dks)))
        v_seed = (f"The seeds disagree by up to {100 * spread:.0f} points: these small models sometimes find the trick "
                  "and sometimes don't." if spread > 0.15 else
                  f"The seeds agree to within {100 * spread:.0f} points.")
        with self.voiceover(
            "And here is every run at the end, against the size of the key, which sets the size of the fixed "
            "memories. <bookmark mark='a'/> " + v_small + "<bookmark mark='b'/> " + v_big + "<bookmark mark='c'/> "
            + v_seed
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.005), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(dots, color=WHITE, scale_factor=1.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lesson(self):
        m = load("mqar")
        mix = list(m["mixers"])
        N = int(m["N"])
        dks = [int(x) for x in m["dks"]]
        acc = {k: np.asarray(m[f"acc_{k}"]).mean(1) for k in mix}
        T = 3 * N
        cache = [T * (dk + 64) for dk in dks]
        state = [dk * 64 for dk in dks]
        head = label(r"what each memory holds, \ after reading the list", font_size=30).to_edge(UP, buff=0.4)
        rows = VGroup()
        for i, dk in enumerate(dks):
            rows.add(VGroup(MathTex(rf"{dk}", font_size=26, color=GREY_A),
                            MathTex(rf"{state[i]:,}".replace(",", "{,}"), font_size=26, color=MIX_C["gdn"]),
                            MathTex(rf"{cache[i]:,}".replace(",", "{,}"), font_size=26, color=MIX_C["softmax"])))
        hdr = VGroup(label(r"key size", font_size=20, color=GREY_B), label(r"a fixed memory", font_size=20, color=MIX_C["gdn"]),
                     label(rf"attention's cache, \ ${T}$ tokens", font_size=20, color=MIX_C["softmax"]))
        xs = [-3.6, 0.0, 3.6]
        for h_, x in zip(hdr, xs):
            h_.move_to([x, 1.9, 0])
        for i, r_ in enumerate(rows):
            for c_, x in zip(r_, xs):
                c_.move_to([x, 1.2 - i * 0.6, 0])
        tw = label(r"attention pays for exact recall with a cache that grows with the text; \\ a fixed memory must be "
                   r"big enough, \ or know what to overwrite; \\ one attention layer on top of a fast one gets most of both",
                   font_size=24, color=WHITE).to_edge(DOWN, buff=0.6)
        hy = acc["hybrid"][0]
        gd = acc["gdn"][0]
        v = (f"With the smallest keys, adding one attention layer above a gated delta layer lifts recall from "
             f"{100 * gd:.0f} to {100 * hy:.0f} percent." if hy > gd + 0.1 else
             f"With the smallest keys, the hybrid gets {100 * hy:.0f} percent, against {100 * gd:.0f} for two gated "
             "delta layers.")
        with self.voiceover(
            "Why? Count what each memory holds after reading the list. <bookmark mark='a'/> A fixed memory with "
            f"keys of {dks[0]} numbers holds {state[0]:,} numbers a layer, whatever the length. Attention's cache "
            f"holds every key and value it has seen, {cache[0]:,} here, and {cache[0] * 1000:,} for a text a "
            "thousand times longer. <bookmark mark='b'/> Exact recall is what attention buys with that growing "
            "cache; a fixed memory has to be big enough, or know what to overwrite. " + v + " That is the case for "
            "hybrids."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in rows], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()
