from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (ATTNC, DECODEC, F, KVC, PART, hbars, load, loglog, x_)

COLORS = {r"m_s": C.BITS, r"\ell_s": C.BITS, r"o_s": ATTNC, r"M": C.BITS}
WINC, GEMC, DSAC = C.BITS, C.HOT, C.INDEXER


class ServeAttention(VoiceoverScene):
    def construct(self):
        self.card()
        self.flashdec()
        self.windows()

    def card(self):
        card = chapter_card(15, r"Attention at serve time", r"One query, \ and a million keys?", part=PART)
        with self.voiceover("Chapter fifteen. Attention at serve time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def flashdec(self):
        f = load("flash")
        occ, sp = f["occ"], f["occ_splits"]
        heads = int(f["occ_heads"])
        # the GPU's multiprocessors, and how many have work (batch 1, one block per head)
        n = F.H100_SMS
        cols = 22
        sms = VGroup(*[Square(0.22, stroke_width=0.6, stroke_color=GREY_D, fill_color=GREY_D, fill_opacity=0.25)
                       for _ in range(n)]).arrange_in_grid(rows=math.ceil(n / cols), cols=cols, buff=0.04)
        sms.move_to([-2.8, 1.9, 0])
        sl = label(rf"an H100's ${n}$ multiprocessors", font_size=20, color=GREY_A).next_to(sms, UP, buff=0.15)
        busy = lambda k: VGroup(*[sms[i].copy().set_fill(DECODEC, 0.85) for i in range(min(k, n))])  # noqa: E731
        b1 = busy(heads)
        b8 = busy(heads * 8)
        rows = [
            cmath(r"o", r"=", r"\frac{\sum_s e^{m_s - M}\, o_s}{\sum_s e^{m_s - M}\, \ell_s},", r"\quad M = \max_s m_s",
                  colors=COLORS, font_size=34),
        ]
        rows[0].move_to([-2.2, -0.6, 0])
        wl = why(r"each chunk $s$: \ its max $m_s$, \ sum $\ell_s$, \ output $o_s$, \ computed in parallel")
        wl.next_to(rows[0], DOWN, buff=0.25).align_to(rows[0], LEFT)
        o1 = label(rf"batch $1$, \ ${heads}$ heads: \ ${100 * occ[0]:.0f}\%$ of the chip busy", font_size=21,
                   color=DECODEC)
        k8 = sp.index(8)
        o8 = label(rf"split each head's cache in $8$: \ ${100 * occ[k8]:.0f}\%$", font_size=21, color=DECODEC)
        ol = VGroup(o1, o8).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, 1.9, 0])
        chk = label(rf"checked on Part 13's attention, \ $8$ chunks: \ within ${sci(f['split_dev'], 0)}$", font_size=20,
                    color=C.BITS).next_to(wl, DOWN, buff=0.35).align_to(rows[0], LEFT)
        hc = history_card(2023, r"Tri Dao, Daniel Haziza, Francisco Massa \& Grigory Sizov", rf"Flash-Decoding: \ up to "
                          rf"${F.FLASHDEC['gain']}\times$ faster generation on very long sequences", width=4.4,
                          font_size=16, color=ATTNC).move_to([4.4, -1.4, 0])
        tag = note(r"a simple model: \ one block of work per multiprocessor").to_corner(DR, buff=0.2)
        with self.voiceover(
            "FlashAttention was built for reading prompts, where thousands of queries share each tile of keys. "
            "Decoding has one query per conversation, against a cache that may hold a million keys. "
            "<bookmark mark='a'/> FlashAttention hands each head's work to one of the GPU's multiprocessors. With "
            f"one conversation and {heads} heads, an H100 keeps {heads} of its {n} busy: {100 * occ[0]:.0f} percent. "
            "<bookmark mark='b'/> Flash-Decoding, from Tri Dao and colleagues in 2023, also splits the cache into "
            "chunks, attends to each in parallel, and combines the partial answers with the same trick as the "
            "online softmax: weight each chunk's output and sum by e to its max minus the overall max. "
            f"<bookmark mark='c'/> With eight chunks per head, {100 * occ[k8]:.0f} percent of the chip has work. "
            "We checked the combination on Part 13's attention: exact to rounding. Its authors measured up to "
            "eight times faster generation at long contexts."
        ) as vo:
            self.play(FadeIn(sms), FadeIn(sl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(b1), FadeIn(o1))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(wl))
            vo.wait_until("c")
            self.play(FadeIn(b8), FadeIn(o8))
            self.play(FadeIn(chk), FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def windows(self):
        k, ph = load("kv"), load("phases")
        ctx = np.asarray(k["ctxs"])
        series = [("read_full", r"every layer looks at everything", KVC),
                  ("read_oss", r"gpt-oss: \ every other layer, \ the last $128$", WINC),
                  ("read_gemma_pattern", r"Gemma 3's pattern: \ $5$ of $6$ layers, \ the last $1{,}024$", GEMC),
                  ("read_dsa", r"DeepSeek's sparse attention: \ the best $2{,}048$", DSAC)]
        g = loglog((math.log10(256), 6.05), (6, 11.2), x_length=6.6, y_length=4.0,
                   xlabel=r"context: \ tokens so far", ylabel=r"cache read per decode step, \ one conversation",
                   center=[-2.6, -0.3, 0], xfmt=lambda v: {3: r"10^3", 4: r"10^4", 5: r"10^5", 6: r"10^6"}.get(int(v), ""),
                   yfmt=lambda v: {6: r"\text{MB}", 9: r"\text{GB}"}.get(int(v), ""))
        ax = g.ax
        lines = VGroup(*[curve(ax, np.log10(ctx), np.log10(np.asarray(k[key])), c_, 3) for key, _, c_ in series])
        leg = legend([(c_, t) for _, t, c_ in series], font_size=17).move_to([3.9, 2.2, 0])
        tag = note(r"computed from gpt-oss-120b's sizes \ ($36$ layers, \ $8$ key-value heads of $64$), \ $16$ bits",
                   font_size=17).to_corner(DL, buff=0.2)
        # measured: our model with a window of 128, against full attention
        ctxs = list(ph["ctxs"])
        i8 = list(ph["ctx_B"]).index(8)
        full = np.asarray(ph["ctx_t"])[i8] * 1e3
        win = np.asarray(ph["win_t"]) * 1e3
        mb = hbars([full[-1], win[-1]], [r"full attention", r"window of $128$"], [KVC, WINC], width=2.4, row_h=0.4,
                   font_size=18, lo=0, hi=full[-1] * 1.1, fmt_v=lambda v: rf"{v:.1f}\,\text{{ms}}")
        mt = label(rf"our model, \ batch $8$, \ ${ctxs[-1]:,}$ tokens: \ one step".replace(",", "{,}"), font_size=18,
                   color=GREY_A)
        meas = VGroup(mt, mb).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.0, -1.9, 0])
        hc = history_card(2025, r"DeepSeek-V3.2", r"a cheap indexer scores every past token; \ attention reads only the "
                          rf"top ${F.DSV32['topk']:,}$".replace(",", "{,}"), width=4.0, font_size=15,
                          color=DSAC).to_corner(UR, buff=0.15).shift(DOWN * 2.3)
        i128 = int(np.argmin(np.abs(ctx - 131072)))
        rf = np.asarray(k["read_full"])[i128]
        ro, rg, rd = (np.asarray(k[x])[i128] for x in ("read_oss", "read_gemma_pattern", "read_dsa"))
        with self.voiceover(
            "The other way to read less of the cache is to look at less of it. <bookmark mark='a'/> With full "
            "attention, every step reads the whole cache, and the read grows with the conversation. "
            "<bookmark mark='b'/> gpt-oss alternates: every other layer looks back only 128 tokens, so half the "
            f"reading stops growing. At 128 thousand tokens it reads {rf / ro:.1f} times less. "
            "<bookmark mark='c'/> Gemma 3, in 2025, gave five layers in six a window of 1,024 tokens: "
            f"{x_(rf / rg)} times less. <bookmark mark='d'/> And DeepSeek's sparse attention, in V3.2, keeps every "
            "token but lets a small, fast indexer choose 2,048 of them for each query. The indexer still glances "
            "at every token, through a few small eight-bit heads, but the main attention's read stops growing: "
            f"{x_(rf / rd)} times less at 128 thousand. <bookmark mark='e'/> On our own model a window is "
            f"easy to try: at {ctxs[-1]:,} tokens, a decode step for eight conversations takes {full[-1]:.1f} "
            f"milliseconds with full attention, and {win[-1]:.1f} with a window of 128. What it costs in quality "
            "depends on what the model learned to do with it: these models were trained with their windows."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(leg[2]))
            vo.wait_until("d")
            self.play(Create(lines[3]), FadeIn(leg[3]), FadeIn(hc))
            vo.wait_until("e")
            self.play(FadeIn(meas))
        self.wait(0.3)
        self.clear_scene()
