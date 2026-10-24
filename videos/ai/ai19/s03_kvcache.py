from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (DECODEC, F, KVC, PART, WEIGHTC, hbars, human_bytes, load, loglog, spoken_bytes,
                                   take_away, times)


class KVCache(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.table()
        self.growth()
        self.measured()

    def card(self):
        card = chapter_card(2, r"The key-value cache, priced", r"What does it cost to remember the conversation?",
                            part=PART)
        with self.voiceover("Chapter two. The key-value cache, priced."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"L": GREY_A, r"n_h": C.QUERY, r"n_g": KVC, r"d_h": GREY_A, r"d_c": C.LATENT, r"d_R": C.POSITION}
        rows = [
            cmath(r"\text{MHA}", r":\;", r"2\,L\,", r"n_h", r"\,", r"d_h", colors=colors, font_size=40),
            cmath(r"\text{GQA}", r":\;", r"2\,L\,", r"n_g", r"\,", r"d_h", colors=colors, font_size=40),
            cmath(r"\text{MLA}", r":\;", r"L\,(", r"d_c", r"+", r"d_R", r")", colors=colors, font_size=40),
        ]
        whys = [why(r"a key and a value, \ every head, \ every layer"),
                why(r"$n_h / n_g$ query heads share each key and value"),
                why(r"one compressed vector, \ plus a small rotary key")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-3.4, buff=0.55, edge=6.8)
        head = label(r"numbers kept per token, \ for the whole model", font_size=26, color=KVC).to_edge(UP, buff=0.35)
        hist = VGroup(
            history_card(2019, r"Noam Shazeer, \ Google", r"multi-query attention: \ one key and value for all heads",
                         width=4.1, font_size=18, color=KVC),
            history_card(2023, r"Joshua Ainslie et al., \ Google", rf"grouped-query attention; \ a model converted "
                         rf"with ${F.GQA['uptrain']}\%$ of its training", width=4.1, font_size=18, color=KVC),
            history_card(2024, r"DeepSeek-V2", rf"multi-head latent attention: \ ${F.DSV2['kv_cut']}\%$ less cache "
                         r"than DeepSeek 67B", width=4.1, font_size=18, color=C.LATENT),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part 15 built the key-value cache: every token a model has read leaves a key and a value in every "
            "attention head of every layer, so that the next token can look back at it without recomputing. "
            "<bookmark mark='a'/> With L layers and n h heads of size d h, that's two L n h d h numbers per token. "
            "<bookmark mark='b'/> In 2019 Noam Shazeer let all the heads share one key and one value, and in 2023 "
            "grouped-query attention found the middle: n g groups, each shared by several query heads. "
            "<bookmark mark='c'/> In 2024 DeepSeek went further. Multi-head latent attention caches one compressed "
            "vector per token, of size d c, plus a small key that carries the rotary positions, and rebuilds every "
            "head's keys and values from it."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=KVC))
            vo.wait_until("b")
            step(1)
            self.play(FadeIn(hist[0], shift=UP * 0.2), FadeIn(hist[1], shift=UP * 0.2))
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(hist[2], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        k = load("kv")
        pt = k["per_token"]
        rows = [("llama70_mha", r"Llama 3.1 70B, \ if every head had its own", GREY_B),
                ("llama70", r"Llama 3.1 70B: \ $8$ groups (GQA)", KVC),
                ("dsv3_mha", r"DeepSeek-V3, \ uncompressed", GREY_B),
                ("dsv3", r"DeepSeek-V3: \ MLA", C.LATENT),
                ("oss_full", r"gpt-oss-120b: \ $8$ groups of $64$", C.BITS),
                ("ours", r"our novels model \ ($32$-bit)", C.NEURAL)]
        vals = [math.log10(pt[r[0]]) for r in rows]
        bars = hbars(vals, [r[1] for r in rows], [r[2] for r in rows], width=4.6, row_h=0.62, font_size=22,
                     lo=3.5, hi=7.0, fmt_v=lambda v: "", name_w=6.0)
        for b_, (key, _, col) in zip(bars, rows):
            b_.val.become(label(human_bytes(pt[key]).replace(" ", r"\ "), font_size=22, color=col).next_to(b_.bar, RIGHT,
                                                                                                         buff=0.15))
        bars.move_to([0.9, -0.2, 0])
        head = label(r"cache per token, \ $16$-bit numbers \ (published configurations)", font_size=26,
                     color=KVC).to_edge(UP, buff=0.4)
        axl = label(r"log scale", font_size=18, color=GREY_B).next_to(bars, DOWN, buff=0.25).align_to(bars[0].bar, LEFT)
        src = cite(r"model configurations: \ Llama Team (2024), \ DeepSeek-AI (2024), \ OpenAI (2025)", corner=DR)
        cut = k["mla_ratio"]
        with self.voiceover(
            "Here is what that means for real models. <bookmark mark='a'/> Llama 3.1 70B has 80 layers and 64 query "
            "heads of 128 numbers. Give each head its own key and value, and every token costs "
            f"{spoken_bytes(pt['llama70_mha'])}. <bookmark mark='b'/> It uses eight groups instead, so a token costs "
            f"{spoken_bytes(pt['llama70'])}, {k['gqa_ratio']:.0f} times less. <bookmark mark='c'/> DeepSeek-V3's 128 "
            f"heads, uncompressed, would cost {spoken_bytes(pt['dsv3_mha'])} a token. <bookmark mark='d'/> With MLA, "
            f"{spoken_bytes(pt['dsv3'])}: {cut:.0f} times less, about what grouped attention with "
            f"{k['mla_groups']:.2f} groups would keep. <bookmark mark='e'/> gpt-oss keeps {spoken_bytes(pt['oss_full'])}, "
            f"and our little model {spoken_bytes(pt['ours'])}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(axl))
            for i, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(FadeIn(bars[i].name), GrowFromEdge(bars[i].bar, LEFT), FadeIn(bars[i].val))
            self.play(FadeIn(bars[5].name), GrowFromEdge(bars[5].bar, LEFT), FadeIn(bars[5].val))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def growth(self):
        k = load("kv")
        ctx = np.asarray(k["ctxs"])
        W70 = 2 * F.LLAMA31_70B["params"]
        lc = np.log10(ctx)
        g = loglog((math.log10(256), 6.05), (6, 12.5), x_length=7.6, y_length=4.4,
                   xlabel=r"context: \ tokens in the conversation", ylabel=r"bytes of cache, \ one conversation",
                   center=[-1.6, -0.4, 0], xfmt=lambda v: {3: r"10^3", 4: r"10^4", 5: r"10^5", 6: r"10^6"}.get(int(v), ""),
                   yfmt=lambda v: {6: r"\text{MB}", 9: r"\text{GB}", 12: r"\text{TB}"}.get(int(v), ""))
        ax = g.ax
        curves = [("curve_llama70_mha", GREY_B, r"Llama 70B, \ every head"), ("curve_llama70", KVC, r"Llama 70B, \ GQA"),
                  ("curve_dsv3", C.LATENT, r"DeepSeek-V3, \ MLA"), ("curve_oss", C.BITS, r"gpt-oss: \ window on half")]
        lines = VGroup(*[curve(ax, lc, np.log10(np.asarray(k[key])), col, 3) for key, col, _ in curves])
        leg = legend([(col, t) for _, col, t in curves], font_size=20).move_to([4.7, -1.2, 0])
        wl = DashedLine(ax.c2p(math.log10(256), math.log10(W70)), ax.c2p(6.05, math.log10(W70)), color=WEIGHTC,
                        dash_length=0.08)
        wll = label(r"Llama 3.1 70B's weights: \ $141$ GB", font_size=20, color=WEIGHTC)
        wll.next_to(ax.c2p(math.log10(300), math.log10(W70)), UP, buff=0.08, aligned_edge=LEFT)
        cr = k["cross_llama70"]
        cross = Dot(ax.c2p(math.log10(cr), math.log10(W70)), radius=0.08, color=KVC)
        crl = label(rf"${cr / 1e3:.0f}$k tokens", font_size=20, color=KVC).next_to(cross, DOWN, buff=0.15)
        mem = DashedLine(ax.c2p(math.log10(256), math.log10(80e9)), ax.c2p(6.05, math.log10(80e9)), color=GREY_C,
                         dash_length=0.05).set_stroke(opacity=0.6)
        meml = label(r"one H100: \ $80$ GB", font_size=18, color=GREY_B).next_to(ax.c2p(5.2, math.log10(80e9)), DOWN,
                                                                                  buff=0.08)
        osc = np.asarray(k["curve_oss"])
        osf = np.asarray(k["curve_oss_full"])
        i128 = int(np.argmin(np.abs(ctx - 131072)))
        with self.voiceover(
            "And the cache grows with every token of the conversation. <bookmark mark='a'/> On log scales, each "
            "model is a straight line: bytes per token times tokens. <bookmark mark='b'/> Compare the weights. "
            f"Llama 3.1 70B's weights take 141 gigabytes. With grouped attention, one conversation's cache "
            f"outgrows them at about {cr / 1e3:.0f} thousand tokens; with every head its own, at "
            f"{k['cross_llama70_mha'] / 1e3:.0f} thousand. <bookmark mark='c'/> And a server holds many "
            "conversations at once. One H100 has eighty gigabytes for all of it. <bookmark mark='d'/> gpt-oss bends "
            "its line differently: every other layer looks back only 128 tokens, so those layers' caches stop "
            f"growing, and at 128 thousand tokens it keeps {osf[i128] / osc[i128]:.1f} times less than full "
            "attention everywhere would."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines[:3]], lag_ratio=0.3), FadeIn(leg[:3]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(wl), FadeIn(wll))
            self.play(FadeIn(cross, scale=0.5), FadeIn(crl))
            vo.wait_until("c")
            self.play(Create(mem), FadeIn(meml))
            vo.wait_until("d")
            self.play(Create(lines[3]), FadeIn(leg[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        k, ph = load("kv"), load("phases")
        nb = np.asarray(k["meas_ctx_bytes"])  # (batches, contexts) bytes read per step: weights + caches
        tt = np.asarray(k["meas_ctx_t"]) * 1e3
        Bs, ctxs = ph["ctx_B"], ph["ctxs"]
        wbytes = 4.0 * ph["sizes"]["read"]
        x_hi = math.log10(nb.max() * 1.6)
        g = loglog((math.log10(wbytes * 0.7), x_hi), (0, math.log10(tt.max() * 2)), x_length=6.6, y_length=4.2,
                   xlabel=r"bytes a decode step reads: \ weights $+$ caches",
                   ylabel=r"time per step \ (ms, \ this computer)", center=[-2.7, -0.4, 0],
                   xfmt=lambda v: {7: r"10\,\text{MB}", 8: r"100\,\text{MB}", 9: r"1\,\text{GB}"}.get(int(v), ""))
        ax = g.ax
        cols = [DECODEC, KVC, C.BITS]
        dots = VGroup()
        for i, (B, col) in enumerate(zip(Bs, cols)):
            dots.add(VGroup(*[Dot(ax.c2p(math.log10(nb[i, j]), math.log10(tt[i, j])), radius=0.07, color=col)
                              for j in range(len(ctxs))]))
        lines = VGroup(*[curve(ax, np.log10(nb[i]), np.log10(tt[i]), cols[i], 2) for i in range(len(Bs))])
        leg = legend([(c_, rf"batch ${B}$, \ context ${ctxs[0]}$ to ${ctxs[-1]:,}$".replace(",", "{,}"))
                      for B, c_ in zip(Bs, cols)], font_size=19).move_to([4.2, 1.4, 0])
        i = len(Bs) - 1
        kv_last = nb[i, -1] - wbytes
        slope = (nb[i, -1] - nb[i, 0]) / ((tt[i, -1] - tt[i, 0]) / 1e3)
        notes = VGroup(
            label(rf"weights: \ ${wbytes / 1e6:.0f}$ MB", font_size=21, color=WEIGHTC),
            label(rf"batch ${Bs[i]}$ at ${ctxs[-1]:,}$ tokens: \ ${kv_last / 1e6:,.0f}$ MB of cache".replace(",", "{,}"),
                  font_size=21, color=C.BITS),
            label(rf"each extra byte read: \ $\approx {slope / 1e9:.1f}$ GB/s", font_size=21, color=KVC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.2, -1.0, 0])
        tw = take_away(r"long conversations make decoding a matter of reading the cache", font_size=26)
        grow = tt[i, -1] / tt[i, 0]
        rate = nb / (tt / 1e3)  # bytes a second each step managed
        lo_r, hi_r = float(rate.min()), float(rate.max())
        trend = ("the points fall close to one line" if hi_r / lo_r < 2 else
                 "time grows with the bytes, though not on one line")
        with self.voiceover(
            "We measured the same thing on our model. <bookmark mark='a'/> A decode step, for batches of 1, 8 and "
            f"{Bs[-1]} conversations, each with {ctxs[0]} to {ctxs[-1]:,} tokens already cached. "
            "<bookmark mark='b'/> Plot the time of a step against the bytes it has to read, and " + trend + ": "
            f"every step moved between {lo_r / 1e9:.0f} and {hi_r / 1e9:.0f} gigabytes a second. At a batch of "
            f"{Bs[i]} and {ctxs[-1]:,} tokens, the caches are "
            f"{kv_last / 1e6:,.0f} megabytes, {times(kv_last / wbytes)} the weights, and a step takes "
            f"{times(grow)} as long as at {ctxs[0]} tokens. <bookmark mark='c'/> Every extra byte of cache costs "
            f"time at about {slope / 1e9:.1f} gigabytes a second, this processor's memory speed. Long conversations "
            "turn decoding into reading the cache: shrink it, as MLA does; look at less of it, as windows do; or "
            "store it in fewer bits, in chapter 13."
        ) as vo:
            self.play(FadeIn(g), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.3), FadeIn(leg), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()
