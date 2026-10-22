from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (ARCH_COLOR, DECODER, ENCDEC, OPEN, PART, PRIOR, F, config_card, human, load,
                                   month_year, take_away)

GOOD = C.REWARD  # the choice the field converged on

MATRIX = ["transformer", "gpt2", "t5", "gpt3", "palm", "llama", "llama2", "mistral", "llama3", "dsv3", "qwen3"]
COLS = [("norm", r"normalization"), ("act", r"activation"), ("pos", r"positions"), ("attn", r"attention"),
        ("bias", r"biases")]
WIN = {"norm": {"pre-RMS"}, "act": {"SwiGLU"}, "pos": {"RoPE"}, "attn": {"GQA", "GQA + window", "GQA + QK-norm"},
       "bias": {False}}
SHOW = {"post-LN": r"post-norm", "pre-LN": r"pre-norm", "pre-RMS": r"pre-norm RMS", "ReLU": r"ReLU",
        "GELU": r"GELU", "SwiGLU": r"SwiGLU", "sinusoidal": r"sine waves", "learned": r"learned",
        "relative": r"relative bias", "RoPE": r"RoPE", "MHA": r"multi-head", "MQA": r"multi-query",
        "GQA": r"grouped-query", "GQA + window": r"grouped + window", "GQA + QK-norm": r"grouped + QK-norm",
        "MLA": r"latent (MLA)", "dense + sparse": r"dense + sparse", True: r"yes", False: r"none", None: r"--"}


class Converge(VoiceoverScene):
    def construct(self):
        self.card()
        self.cards()
        self.matrix()
        self.prenorm()
        self.swiglu()
        self.attention()

    def card(self):
        card = chapter_card(10, r"The architecture converges", r"What did every open model end up sharing?",
                            lit=(2023, 2024), part=PART)
        with self.voiceover("Chapter ten. The architecture converges."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cards(self):
        keys = ["transformer", "gpt2", "gpt3", "llama", "llama3", "dsv3", "qwen3", "kimik3"]
        rows = ("layers", "d", "heads", "ctx", "params", "tokens")
        cards = [config_card(F.CFG[k], rows=rows, width=5.0, font_size=22).move_to([-3.9, -0.1, 0]) for k in keys]
        # growth of each field relative to the 2017 Transformer (log scale), as dots that move with the card
        base = F.CFG["transformer"]
        fields = [("layers", r"layers", 1, 2.2), ("d", r"width", 1, 2.2), ("ctx", r"context", 512, 4)]
        g = axes([0, 3.6], [0, 4], x_length=5.4, y_length=4.2, ylabel=r"growth since GPT-1 \ (log scale)",
                 yticks=[0, 1, 2, 3, 4], yfmt=lambda v: rf"{10 ** int(v):,}\times".replace(",", "{,}"),
                 center=[3.3, -0.4, 0])
        ax = g.ax
        ref = {"layers": 12, "d": 768, "ctx": 512}  # GPT-1, the first decoder
        names = VGroup(*[label(n, font_size=20, color=GREY_A).move_to(ax.c2p(0.6 + 1.2 * j, 0) + DOWN * 0.3)
                         for j, (_, n, _, _) in enumerate(fields)])

        def bars_for(c):
            out = VGroup()
            for j, (f, _, _, _) in enumerate(fields):
                v = c.get(f)
                r = max(v / ref[f], 1.0) if v else 1.0
                top = ax.c2p(0.6 + 1.2 * j, math.log10(r))
                b = Rectangle(width=0.7, height=max(top[1] - ax.c2p(0, 0)[1], 0.02), stroke_width=0,
                              fill_color=ARCH_COLOR[c["arch"]], fill_opacity=0.85 if v else 0.0)
                b.move_to(ax.c2p(0.6 + 1.2 * j, 0), aligned_edge=DOWN)
                txt = (rf"{r:.1f}\times" if r < 10 else rf"{r:,.0f}\times".replace(",", "{,}")) if v else r"\text{--}"
                t = MathTex(txt, font_size=22, color=WHITE).next_to(b, UP, buff=0.06)
                out.add(VGroup(b, t))
            return out

        bar_sets = [bars_for(F.CFG[k]) for k in keys]
        cite_ = cite(r"published configurations: \ Vaswani et al.\ (2017) \dots\ Kimi K3 model card (2026)")
        k3, gp1 = F.CFG["kimik3"], F.CFG["gpt1"]
        l3 = F.CFG["llama3"]
        with self.voiceover(
            "Open weights mean open configurations, so we can watch the designs change year by year. Here is one "
            "card, and how it changed. <bookmark mark='a'/> The 2017 Transformer. <bookmark mark='b'/> GPT-2, 2019: "
            "forty-eight layers. <bookmark mark='c'/> GPT-3, 2020: ninety-six layers, twelve thousand wide. "
            "<bookmark mark='d'/> LLaMA, 2023: smaller, but trained on 1.4 trillion tokens. <bookmark mark='e'/> "
            f"Llama 3.1, 2024: {l3['layers']} layers, {l3['d']:,} wide, a context of 128 thousand tokens. "
            "<bookmark mark='f'/> DeepSeek-V3: fewer layers, but 671 billion parameters, only 37 billion of them used "
            "for each token. <bookmark mark='g'/> Qwen3, 2025: 36 trillion tokens. <bookmark mark='h'/> And Kimi K3, "
            f"2026: {k3['params'] / 1e12:.1f} trillion parameters and a context of a million tokens, "
            f"{k3['ctx'] // gp1['ctx']:,} times GPT-1's."
        ) as vo:
            self.play(FadeIn(cards[0]), FadeIn(g), FadeIn(names), FadeIn(cite_))
            cur, curb = cards[0], None
            for k, mk in enumerate("abcdefgh"):
                vo.wait_until(mk)
                if k == 0:
                    self.play(FadeIn(bar_sets[0]))
                    curb = bar_sets[0]
                    continue
                self.play(ReplacementTransform(cur, cards[k]), ReplacementTransform(curb, bar_sets[k]), run_time=1.2)
                cur, curb = cards[k], bar_sets[k]
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def matrix(self):
        xs = [-5.3, -2.75, -0.95, 0.85, 2.85, 4.85]
        y0 = 3.15
        head = VGroup(label(r"model", font_size=22, color=GREY_A).move_to([xs[0], y0, 0]),
                      *[label(t, font_size=22, color=GREY_A).move_to([x, y0, 0]) for (_, t), x in zip(COLS, xs[1:])])
        rows = VGroup()
        for i, key in enumerate(MATRIX):
            c = F.CFG[key]
            y = y0 - 0.5 * (i + 1) - 0.1
            nm = label(rf"{c['name']} \ ({c['date'][:4]})", font_size=20, color=ARCH_COLOR[c["arch"]])
            if nm.width > 2.6:
                nm.width = 2.6
            cells = VGroup(nm.move_to([xs[0], y, 0]))
            for (f, _), x in zip(COLS, xs[1:]):
                v = c.get(f)
                won = v in WIN[f]
                box = RoundedRectangle(width=1.7, height=0.4, corner_radius=0.06, stroke_width=0,
                                       fill_color=GOOD if won else GREY_D, fill_opacity=0.35 if won else 0.25)
                t = label(SHOW.get(v, str(v)), font_size=17, color=WHITE if won else GREY_B)
                if t.width > 1.6:
                    t.width = 1.6
                cells.add(VGroup(box, t).move_to([x, y, 0]))
            rows.add(cells)
        groups = [[0], [1, 2, 3], [4], [5, 6, 7, 8], [9, 10]]
        cite_ = cite(r"the papers and model cards of each model", corner=DR)
        with self.voiceover(
            "Now read the recipes side by side, across five design choices. <bookmark mark='a'/> The 2017 "
            "Transformer: layer normalization after each sub-layer, ReLU, sine-wave positions, ordinary multi-head "
            "attention, biases everywhere. <bookmark mark='b'/> GPT-2 and GPT-3 moved the normalization before each "
            "sub-layer; T5 dropped its mean and bias. <bookmark mark='c'/> PaLM, in 2022: SwiGLU, rotary positions, a "
            "single shared key and value, no biases. <bookmark mark='d'/> LLaMA put the pieces together, and from "
            "Llama 2's largest model on, nearly every open model looks the same: pre-norm RMSNorm, SwiGLU, rotary "
            "positions, grouped-query attention, no biases. <bookmark mark='e'/> Then DeepSeek-V3 changed the "
            "attention, Qwen3 added a normalization inside it, and the convergence began to loosen: the next chapter. "
            "First, why each choice won."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            for grp, mk in zip(groups, "abcde"):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(rows[i], shift=UP * 0.1) for i in grp], lag_ratio=0.3),
                          run_time=1.0 + 0.4 * len(grp))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prenorm(self):
        rows = [
            cmath(r"x_{l+1}", r"=", r"\mathrm{LN}\big(x_l + F_l(x_l)\big)", font_size=36),
            cmath(r"x_{l+1}", r"=", r"x_l + F_l\big(\mathrm{N}(x_l)\big)", font_size=36),
            cmath(r"x_L", r"=", r"x_l + \sum_{k=l}^{L-1} F_k\big(\mathrm{N}(x_k)\big)", font_size=36),
            cmath(r"\frac{\partial x_L}{\partial x_l}", r"=", r"I + \sum_{k=l}^{L-1} \frac{\partial F_k}{\partial x_l}",
                  font_size=36),
            cmath(r"\mathrm{RMS}(x)", r"=", r"\sqrt{\tfrac1d \textstyle\sum_i x_i^2}, \quad \mathrm{N}(x) = g \odot "
                                            r"\frac{x}{\mathrm{RMS}(x)}", font_size=36),
        ]
        whys = [why(r"post-norm (2017): \ normalize after adding"),
                why(r"pre-norm: \ normalize the branch's input only"),
                why(r"unroll: \ the stream is a sum of every layer's output"),
                why(r"an identity path: \ the gradient reaches every layer"),
                why(r"RMSNorm: \ no mean, no bias \ (Zhang \& Sennrich, 2019)")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-2.4, buff=0.42, edge=6.9)
        res = label(r"pre-norm trains deep stacks without a long warm-up \ (Xiong et al., 2020); \\ RMSNorm does as well "
                    r"as LayerNorm, \ $7$--$64\%$ faster in its authors' tests", font_size=22, color=GREY_A)
        res.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Normalization first. <bookmark mark='a'/> The 2017 Transformer normalized after adding each sub-layer's "
            "output to the stream. <bookmark mark='b'/> Pre-norm normalizes only the input of the branch, and adds "
            "the branch's output back untouched. <bookmark mark='c'/> Unroll that, and the stream at the top is the "
            "stream at layer l plus the sum of every layer's contribution above it. <bookmark mark='d'/> So its "
            "derivative contains the identity: the gradient reaches every layer directly, however deep the stack. "
            "Ruibin Xiong and colleagues showed in 2020 that pre-norm Transformers train without the long warm-up "
            "post-norm needs. <bookmark mark='e'/> And RMSNorm, from Biao Zhang and Rico Sennrich, drops the mean and "
            "the bias and just rescales by the root mean square: as good, and cheaper."
        ) as vo:
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def swiglu(self):
        P = load("published")
        d = F.CFG["llama"]["d"]
        rows = [
            cmath(r"\mathrm{FFN}(x)", r"=", r"W_2\, \mathrm{ReLU}(W_1 x)", font_size=36),
            cmath(r"\mathrm{SwiGLU}(x)", r"=", r"W_2 \big(\mathrm{Swish}(W_1 x) \odot W_3 x\big)", font_size=36),
            cmath(r"3\, d\, h", r"=", r"2\, d \cdot 4d \ \Rightarrow\ h = \tfrac{2}{3} \cdot 4d", font_size=36),
            cmath(r"h", r"=", rf"\tfrac{{8}}{{3}} \times {d:,} = {P['swiglu_exact']:,.1f} \to {P['swiglu_llama']:,}"
                  .replace(",", "{,}"), font_size=36),
        ]
        whys = [why(r"2017: \ two matrices, \ hidden width $4d$"),
                why(r"a gate: \ one branch decides how much of the other passes"),
                why(r"three matrices: \ same parameters if $h = \frac23 \cdot 4d$"),
                why(r"LLaMA-65B, \ rounded up to a multiple of $256$ \ \checkmark")]
        step = ladder(self, rows, whys, keep=4, top=2.7, x=-2.0, buff=0.55, edge=6.9)
        q = VGroup(label(r"``We offer no explanation as to why these architectures seem to work; \\ we attribute their "
                         r"success, as all else, to divine benevolence.''", font_size=24, color=GREY_A),
                   note(r"Noam Shazeer, \textit{GLU Variants Improve Transformer} (2020)")).arrange(DOWN, buff=0.15)
        q.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The feed-forward network. <bookmark mark='a'/> The original was two matrices with a ReLU between. "
            "<bookmark mark='b'/> SwiGLU, from Noam Shazeer in 2020, adds a third matrix as a gate: one branch, "
            "through the smooth Swish function, decides how much of the other branch passes, element by element. "
            "<bookmark mark='c'/> Three matrices instead of two, so to keep the parameter count, the hidden width "
            "shrinks to two thirds of four d. <bookmark mark='d'/> For LLaMA-65B, eight thirds of 8,192 is 21,845, "
            "rounded up to 22,016: exactly its published width. <bookmark mark='e'/> Why does gating help? It lowered "
            "the loss in Shazeer's experiments, and his paper's own answer is famous."
        ) as vo:
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def attention(self):
        P = load("published")
        l3 = F.CFG["llama3"]
        mha, gqa, mla, g3 = P["kv_llama3_mha"], P["kv_llama3_gqa"], P["kv_dsv3_mla"], P["kv_gpt3"]
        row = cmath(r"\text{cache per token}", r"=", r"2 \times L \times n_{\mathrm{kv}} \times d_{\mathrm{head}} "
                                                     r"\times 2\ \text{bytes}", font_size=34).move_to(UP * 2.9)
        wl = why(r"keys and values, \ every layer, \ every key-value head, \ 16-bit numbers").next_to(row, DOWN, buff=0.15)
        items = [(r"GPT-3, \ multi-head", g3, PRIOR),
                 (r"Llama 3.1 405B, \ if multi-head", mha, PRIOR),
                 (r"Llama 3.1 405B, \ grouped ($8$ of $128$)", gqa, OPEN),
                 (r"DeepSeek-V3, \ latent (MLA)", mla, C.LATENT)]
        lo, hi = 4.0, 7.2
        bars = VGroup()
        for i, (nm, v, col) in enumerate(items):
            w = 6.0 * (math.log10(v) - lo) / (hi - lo)
            n_ = label(nm, font_size=20, color=GREY_A)
            b = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.9)
            t = label(rf"{v / 1e6:.2f} MB" if v >= 1e5 else rf"{v / 1e3:.0f} kB", font_size=22, color=col)
            y = 0.9 - 0.75 * i
            n_.move_to([-1.3, y, 0], aligned_edge=RIGHT)
            b.move_to([-1.1, y, 0], aligned_edge=LEFT)
            t.next_to(b, RIGHT, buff=0.12)
            bars.add(VGroup(n_, b, t))
        scale = label(r"bytes per token of context \ (log scale)", font_size=20, color=GREY_B).next_to(bars, UP, buff=0.2)
        at = l3["ctx"]
        tail = label(rf"at {at // 1024}K tokens of context: \ ${mha * at / 1e12:.2f}$ TB \ $\to$ \ "
                     rf"${gqa * at / 1e9:.0f}$ GB per sequence", font_size=26, color=OPEN).to_edge(DOWN, buff=0.75)
        rope = note(r"RoPE: \ Su et al.\ (2021); \ GQA: \ Ainslie et al.\ (2023); \ MLA: \ DeepSeek-AI (2024), "
                    r"and Part 15").to_edge(DOWN, buff=0.25)
        why_cards = VGroup(
            definition_card(r"rotary positions (RoPE)", r"rotate each query and key by its position: \ the score "
                            r"depends only on the distance \ (proved in Part 13), \ and it stretches to longer "
                            r"contexts", color=C.CONTEXT, width=5.6, font_size=24, kind=r"why it won"),
            definition_card(r"grouped-query attention", r"many query heads share one key-value head: \ less to keep "
                            r"in memory for every past token", color=OPEN, width=5.6, font_size=24, kind=r"why it won"),
        ).arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to(UP * 0.4)
        with self.voiceover(
            "Positions and attention. Rotary embeddings won because a rotated query and key give a score that depends "
            "only on their distance, as Part 13 proved, and they stretch to longer contexts. <bookmark mark='g'/> "
            "Grouped-query attention "
            "won because of memory. <bookmark mark='a'/> To generate text, a model keeps the keys and values of every "
            "past token, in every layer: the KV cache. Per token, that's two, times the layers, times the key-value "
            f"heads, times their size, times two bytes. <bookmark mark='b'/> GPT-3 kept about {g3 / 1e6:.1f} megabytes "
            "per token. "
            f"Llama 3.1, with all {l3['heads']} heads keeping their own keys and values, would need "
            f"{mha / 1e6:.1f}. <bookmark mark='c'/> With grouped-query attention, the {l3['heads']} query heads share "
            f"just {l3['kv_heads']} key-value heads: {gqa / 1e6:.2f} megabytes, sixteen times less. "
            "<bookmark mark='d'/> DeepSeek's latent attention compresses further, to about "
            f"{mla / 1e3:.0f} kilobytes. <bookmark mark='e'/> At {at // 1024} thousand tokens of context, that's the "
            f"difference between {mha * at / 1e12:.1f} terabytes and {gqa * at / 1e9:.0f} gigabytes for a single "
            "conversation. Memory is the subject of Part 15."
        ) as vo:
            self.play(FadeIn(rope), FadeIn(why_cards[0], shift=UP * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(why_cards[1], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(why_cards), Write(row), FadeIn(wl))
            self.play(FadeIn(scale))
            for k, mk in enumerate("bbcd"):
                if k != 1:
                    vo.wait_until(mk)
                self.play(FadeIn(bars[k][0]), GrowFromEdge(bars[k][1], LEFT), FadeIn(bars[k][2]))
            vo.wait_until("e")
            self.play(FadeIn(tail))
        self.wait(0.3)
        self.clear_scene()
