from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import A, K, MONO, Q, STATE, V, curve, gib, load, vec_column


class KVCache(VoiceoverScene):
    def construct(self):
        self.card()
        self.why()
        self.shrink()
        self.latent()

    def card(self):
        card = chapter_card(1, r"The cache", r"What does attention have to remember?", part=12)
        with self.voiceover("Chapter one. The cache."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def why(self):
        words = "the Falcon was gone".split()
        g = np.random.default_rng(2)
        ks = VGroup(*[vec_column(g.normal(size=6), color=K) for _ in words])
        vs = VGroup(*[vec_column(g.normal(size=6), color=V) for _ in words])
        cols = VGroup(*[VGroup(k_, v_).arrange(RIGHT, buff=0.06) for k_, v_ in zip(ks, vs)])
        toks = VGroup(*[Text(w, font=MONO, font_size=26, color=GREY_A) for w in words])
        step = max(t.width for t in toks) + 0.35  # room for the longest word under each column
        for i, (c_, t) in enumerate(zip(cols, toks)):
            c_.move_to([i * step, 0, 0])
            t.next_to(c_, DOWN, buff=0.25)
        kl = MathTex(r"k", font_size=30, color=K).next_to(ks[0], UP, buff=0.15)
        vl = MathTex(r"v", font_size=30, color=V).next_to(vs[0], UP, buff=0.15)
        new = vec_column(g.normal(size=6), color=Q).next_to(cols, RIGHT, buff=1.0)
        nl = MathTex(r"q", font_size=30, color=Q).next_to(new, UP, buff=0.15)
        nt = Text("?", font=MONO, font_size=26, color=Q).next_to(new, DOWN, buff=0.25)
        arcs = VGroup(*[CurvedArrow(new.get_left() + LEFT * 0.05, c_.get_top() + UP * 0.05, angle=PI / 4, color=A,
                                    stroke_width=2, tip_length=0.12) for c_ in cols])
        VGroup(cols, toks, kl, vl, new, nl, nt, arcs).scale(1.3).move_to(UP * 0.7)
        brace = Brace(cols, DOWN, buff=0.75, color=GREY_B)
        bl = label(r"the KV cache: \ every past key and value, kept", font_size=26, color=GREY_A).next_to(brace, DOWN, buff=0.1)
        cost = label(r"memory grows with every token; \\ so does the work per new token", font_size=26, color=C.SURPRISE)
        cost.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "When a model writes, it makes one token at a time, and each new token's query looks at every earlier "
            "token's key and value. <bookmark mark='a'/> Recomputing all of those for every new token would be "
            "wasteful, so the model keeps them: the KV cache. <bookmark mark='b'/> The cache grows with every token, "
            "and every new token has to read all of it. For a long conversation, this memory, not the model's "
            "weights, is what fills the graphics card."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in cols], lag_ratio=0.2), FadeIn(toks), FadeIn(kl),
                      FadeIn(vl), run_time=1.6)
            self.play(FadeIn(new), FadeIn(nl), FadeIn(nt), LaggedStart(*[Create(a_) for a_ in arcs], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(GrowFromCenter(brace), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shrink(self):
        k = load("kvcache")
        pt = k["per_token"]
        cf = k["configs"]
        rows = [(r"Llama 3.1 70B, \ one key and value per head", pt["llama_mha"], GREY_B),
                (r"Llama 3.1 70B, \ grouped queries", pt["llama"], C.TRUE_P),
                (r"DeepSeek-V3, \ as full attention", pt["mla_full"], GREY_B),
                (r"DeepSeek-V3, \ latent attention", pt["mla"], C.BITS),
                (r"Qwen3-Next, \ $1$ attention layer in $4$", pt["qwen"], C.INTERVAL)]
        lo, hi = 4.0, 7.0  # log10 bytes
        scale = 6.4 / (hi - lo)
        g = VGroup()
        for i, (t, v, c_) in enumerate(rows):
            y = 1.9 - i * 0.85
            name = label(t, font_size=24, color=c_).move_to([-1.2, y, 0], aligned_edge=RIGHT)
            w = (math.log10(v) - lo) * scale
            bar = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=c_, fill_opacity=0.85).move_to([-0.95 + w / 2, y, 0])
            val = MathTex(gib(v), font_size=28, color=c_).next_to(bar, RIGHT, buff=0.15)
            g.add(VGroup(name, bar, val))
        keep_in_frame(g)
        head = label(r"memory per token of context \ (bf16, \ log scale)", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        L = cf["llama70"]
        gqa = label(rf"grouped queries: \ ${L['q_heads']}$ query heads share ${L['kv_heads']}$ keys and values",
                    font_size=24, color=C.TRUE_P).to_edge(DOWN, buff=0.85)
        src = note(r"layer and head counts from each model's published configuration").to_edge(DOWN, buff=0.3)
        r1 = pt["llama_mha"] / pt["llama"]
        with self.voiceover(
            "How big is it? Take Llama 3.1, seventy billion parameters, eighty layers. <bookmark mark='a'/> If every "
            f"attention head kept its own keys and values, each token of context would cost {pt['llama_mha'] / 2**20:.1f} "
            "megabytes. <bookmark mark='b'/> Llama shares: its sixty-four query heads are split into eight groups, and "
            f"each group shares one key and one value. That's {r1:.0f} times less, {pt['llama'] / 2**10:.0f} kilobytes a "
            "token, and the quality barely changes. <bookmark mark='c'/> DeepSeek-V3 goes further, and so does the "
            "hybrid Qwen3-Next. Let's see how."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(g[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(g[1], shift=RIGHT * 0.2), FadeIn(gqa))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g[2:]], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def latent(self):
        k = load("kvcache")
        D = k["configs"]["deepseek"]
        pt = k["per_token"]
        h = vec_column(np.random.default_rng(3).normal(size=10), cell=0.24, color=C.EMBED).move_to([-5.2, 0.2, 0])
        c = vec_column(np.random.default_rng(4).normal(size=4), cell=0.24, color=C.BITS).move_to([-2.4, 0.2, 0])
        kk = vec_column(np.random.default_rng(5).normal(size=10), cell=0.24, color=K).move_to([0.6, 1.1, 0])
        vv = vec_column(np.random.default_rng(6).normal(size=10), cell=0.24, color=V).move_to([0.6, -1.9, 0])
        a1 = Arrow(h.get_right(), c.get_left(), buff=0.15, color=GREY_B, stroke_width=3)
        a2 = Arrow(c.get_right(), kk.get_left(), buff=0.15, color=GREY_B, stroke_width=3)
        a3 = Arrow(c.get_right(), vv.get_left(), buff=0.15, color=GREY_B, stroke_width=3)
        l1 = MathTex(r"W^{DKV}", font_size=28, color=GREY_A).next_to(a1, UP, buff=0.08)
        l2 = MathTex(r"W^{UK}", font_size=28, color=K).next_to(a2.get_center(), UL, buff=0.05)
        l3 = MathTex(r"W^{UV}", font_size=28, color=V).next_to(a3.get_center(), UR, buff=0.05)
        cl = label(rf"the latent: \ ${D['kv_lora_rank']}$ numbers \\ (plus ${D['rope_dim']}$ for positions) \\ "
                   r"\textbf{the only thing cached}", font_size=22, color=C.BITS).next_to(c, DOWN, buff=0.35)
        hl = label(r"the token", font_size=22, color=C.EMBED).next_to(h, DOWN, buff=0.3)
        kl = label(rf"keys for ${D['q_heads']}$ heads", font_size=22, color=K).next_to(kk, RIGHT, buff=0.2)
        vl = label(rf"values for ${D['q_heads']}$ heads", font_size=22, color=V).next_to(vv, RIGHT, buff=0.2)
        colors = {r"W^{UK}": K, r"c": C.BITS, r"q": Q}
        f = cmath(r"q^{\top} k", "=", r"q^{\top}", r"W^{UK}", r"c", "=", r"\big(", r"W^{UK\top}", r"q", r"\big)^{\top}", r"c",
                  colors=colors, font_size=36).to_corner(UR, buff=0.4)
        fl = label(r"fold $W^{UK}$ into the query: \\ attend to the latent directly", font_size=22, color=GREY_A)
        fl.next_to(f, DOWN, buff=0.15).align_to(f, RIGHT)
        ratio = pt["mla_full"] / pt["mla"]
        res = label(rf"${gib(pt['mla_full'])}$ $\to$ ${gib(pt['mla'])}$ a token: \ ${ratio:.0f}\times$ less", font_size=28,
                    color=C.BITS).to_edge(DOWN, buff=0.4).shift(RIGHT * 2.5)
        cite_ = cite(r"DeepSeek-AI, \textit{DeepSeek-V2} (2024): \ multi-head latent attention", corner=DL)
        with self.voiceover(
            "DeepSeek's trick is multi-head latent attention. <bookmark mark='a'/> Each token is squeezed into a short "
            f"latent vector, {D['kv_lora_rank']} numbers, and only that is cached. <bookmark mark='b'/> Keys and values "
            f"for all {D['q_heads']} heads are unpacked from it by two more matrices when needed. <bookmark mark='c'/> "
            "And they don't even need to be unpacked: since a query's score is a product of matrices, the key's "
            "matrix can be folded into the query, part two's linear algebra, so attention reads the latent directly. "
            f"<bookmark mark='d'/> Against full attention of the same shape, that's {ratio:.0f} times less memory."
        ) as vo:
            self.play(FadeIn(h), FadeIn(hl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(l1), FadeIn(c), FadeIn(cl))
            vo.wait_until("b")
            self.play(GrowArrow(a2), GrowArrow(a3), FadeIn(l2), FadeIn(l3), FadeIn(kk), FadeIn(vv), FadeIn(kl), FadeIn(vl))
            vo.wait_until("c")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
