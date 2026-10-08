from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.open_models.common import (
    MCOLOR, NAMES, cfg, label, model, note, show_chapter_card,
)
from videos.open_models.toys import kv_cache


def kv_head(h=0.5, w=0.07) -> VGroup:
    k = Rectangle(width=w, height=h, stroke_width=0, fill_color=C.KEY, fill_opacity=0.85)
    v = Rectangle(width=w, height=h, stroke_width=0, fill_color=C.VALUE, fill_opacity=0.85)
    return VGroup(k, v).arrange(RIGHT, buff=0.01)


class LongContext(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 4, "The million-token problem")
        self.how_big()
        self.quadratic()
        self.three_answers()

    # ------------------------------------------------------------------
    def how_big(self):
        g = cfg("glm")
        kv = kv_cache()["glm"]
        per_layer = kv["per_layer_mha"]
        assert g["heads"] == 64 and g["qk_nope_head_dim"] + g["qk_rope_head_dim"] == 256 and g["v_head_dim"] == 256
        assert per_layer == 32768 and g["layers"] == 78
        per_tok = kv["mha_per_token"]
        assert 5.0e6 < per_tok < 5.2e6
        weights_tb = sum(model("glm")["params"]["storage_bytes"].values()) / 1e12
        assert 0.7 < weights_tb < 0.8 and 6.5 < per_tok * 1e6 / 1e12 / weights_tb < 7.0

        title = label(r"What if GLM-5.3 used textbook attention?", font_size=36).to_edge(UP, buff=0.35)
        heads = VGroup(*[kv_head() for _ in range(64)]).arrange_in_grid(4, 16, buff=(0.06, 0.12))
        heads.move_to(LEFT * 3.4 + UP * 0.9)
        h_l = label(r"one token, one layer: 64 heads $\times$ (key + value of 256 numbers)", font_size=24, color=GREY_A)
        h_l.next_to(heads, UP, buff=0.2)
        n1 = MathTex(r"64 \times (256 + 256) = 32{,}768", r"\text{ numbers}", font_size=32).next_to(heads, DOWN, buff=0.3)
        n2 = MathTex(r"\times\, 78 \text{ layers} \times 2 \text{ bytes}", r"\approx 5.1\ \text{MB per token}",
                     font_size=32).next_to(n1, DOWN, buff=0.2)
        n2[1].set_color(YELLOW)
        n3 = MathTex(r"\times\, 1{,}000{,}000 \text{ tokens}", r"\approx 5.1\ \text{TB}", font_size=36).next_to(n2, DOWN, 0.3)
        n3[1].set_color(RED)
        bars = VGroup(
            Rectangle(width=0.9, height=4.0 * weights_tb / 5.2, stroke_width=0, fill_color=C.GLM, fill_opacity=0.85),
            Rectangle(width=0.9, height=4.0 * per_tok * 1e6 / 1e12 / 5.2, stroke_width=0, fill_color=RED, fill_opacity=0.85),
        ).arrange(RIGHT, buff=0.8, aligned_edge=DOWN).move_to(RIGHT * 4.3 + DOWN * 0.6)
        bl = VGroup(label(r"the model's\\own weights", font_size=24, color=C.GLM).next_to(bars[0], DOWN, buff=0.15),
                    label(r"the cache, at\\1M tokens", font_size=24, color=RED).next_to(bars[1], DOWN, buff=0.15))
        bv = VGroup(label(rf"{weights_tb:.2f} TB", font_size=26).next_to(bars[0], UP, buff=0.12),
                    label(r"5.1 TB", font_size=26).next_to(bars[1], UP, buff=0.12))
        with self.voiceover(
            "Let's put numbers on the second bill. <bookmark mark='m'/> Suppose GLM-5.3 used the textbook version of "
            "attention, where each of its 64 heads stores a key and a value of 256 numbers, for every token, in each of "
            "its 78 layers. <bookmark mark='n'/> That's over 5 megabytes per token. <bookmark mark='t'/> At a million "
            "tokens of context, 5 terabytes: <bookmark mark='w'/> about seven times the size of the model's own weights. "
            "<bookmark mark='x'/> And every new token would have to read through all of it."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("m")
            self.play(LaggedStart(*[FadeIn(h) for h in heads], lag_ratio=0.01), FadeIn(h_l), run_time=1.5)
            self.play(Write(n1))
            vo.wait_until("n")
            self.play(Write(n2))
            vo.wait_until("t")
            self.play(Write(n3))
            vo.wait_until("w")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(bl[0]), FadeIn(bv[0]))
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(bl[1]), FadeIn(bv[1]), run_time=1.5)
            vo.wait_until("x")
            self.play(Indicate(n3[1], color=RED))
        self.clear_scene()

    # ------------------------------------------------------------------
    def quadratic(self):
        n = 24
        cell = 0.17
        tri = VGroup()
        for i in range(n):
            for j in range(i + 1):
                tri.add(Square(cell * 0.9, stroke_width=0, fill_color=C.ATTN, fill_opacity=0.75).move_to([j * cell, -i * cell, 0]))
        tri.move_to(LEFT * 3.0 + DOWN * 0.2)
        rows_l = label(r"each token (row)", font_size=24, color=GREY_A).next_to(tri, LEFT, buff=0.2).rotate(PI / 2)
        cols_l = label(r"compared with each earlier token (column)", font_size=24, color=GREY_A).next_to(tri, UP, buff=0.2)
        eq = MathTex(r"\tfrac12 \times (10^{6})^2", r"= 5 \times 10^{11}", font_size=44).move_to(RIGHT * 3.2 + UP * 0.6)
        eq[1].set_color(YELLOW)
        eq_l = label(r"pairs of tokens, in one head of one layer,\\for a million-token context", font_size=28,
                     color=GREY_A).next_to(eq, DOWN, buff=0.3)
        with self.voiceover(
            "And compute grows even faster. <bookmark mark='q'/> Across a whole document, attention compares every token "
            "with every token before it. <bookmark mark='p'/> For a million tokens, that's about half a trillion pairs, "
            "in every head of every layer."
        ) as vo:
            vo.wait_until("q")
            self.play(LaggedStart(*[FadeIn(s) for s in tri], lag_ratio=0.003), FadeIn(rows_l), FadeIn(cols_l), run_time=2)
            vo.wait_until("p")
            self.play(Write(eq), FadeIn(eq_l))
        self.clear_scene()

    # ------------------------------------------------------------------
    def three_answers(self):
        n = 14
        cell = 0.2

        def grid(fn):
            g = VGroup()
            for i in range(n):
                for j in range(i + 1):
                    col, op = fn(i, j)
                    g.add(Square(cell * 0.9, stroke_width=0, fill_color=col, fill_opacity=op).move_to([j * cell, -i * cell, 0]))
            return g

        rng = np.random.default_rng(3)
        picks = {i: set(rng.choice(i + 1, size=min(i + 1, 4), replace=False).tolist()) for i in range(n)}
        g1 = grid(lambda i, j: (C.LOCAL, 0.9) if i - j < 4 else (GREY_D, 0.25))
        g2 = grid(lambda i, j: (C.INDEXER, 0.9) if j in picks[i] else (C.LATENT, 0.25))
        g3 = grid(lambda i, j: (GREY_D, 0.2))
        mem = VGroup(*[Square(0.32, stroke_width=0, fill_color=C.MEMORY, fill_opacity=float(o))
                       for o in rng.uniform(0.3, 1.0, 16)]).arrange_in_grid(4, 4, buff=0.04)
        cols = VGroup()
        texts = [
            ("mimo", r"look nearby", r"most layers see only\\the last 128 tokens", C.LOCAL),
            ("glm", r"compress, then select", r"store a small code per token,\\read only the top 2{,}048", C.INDEXER),
            ("kimi", r"keep a running summary", r"a fixed-size memory,\\rewritten as it reads", C.MEMORY),
        ]
        for (k, head, sub, col), g in zip(texts, (g1, g2, g3)):
            name = label(NAMES[k], font_size=30, color=MCOLOR[k])
            h = label(head, font_size=32, color=col)
            s = label(sub, font_size=24, color=GREY_A)
            if k == "kimi":
                mem.move_to(g)
                g = VGroup(g, mem)
            cols.add(VGroup(name, g, h, s).arrange(DOWN, buff=0.25))
        cols.arrange(RIGHT, buff=0.9).move_to(UP * 0.1)
        life = label(r"\dots and all three keep \textbf{some} full, global attention as a lifeline to the distant past",
                     font_size=28, color=C.GLOBAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The three models answer this in three different ways. <bookmark mark='m'/> MiMo looks nearby: most of its "
            "layers only see a short window of recent tokens. <bookmark mark='g'/> GLM compresses each token's memory "
            "into a small code, and then reads only the entries that matter. <bookmark mark='k'/> Kimi keeps a running "
            "summary of fixed size, which it rewrites as it reads. <bookmark mark='a'/> And all three keep some layers of "
            "full, global attention, as a lifeline to the distant past. Let's take them one at a time."
        ) as vo:
            for i, mk in enumerate("mgk"):
                vo.wait_until(mk)
                self.play(FadeIn(cols[i][0]), FadeIn(cols[i][1], lag_ratio=0.01), run_time=1.0)
                self.play(FadeIn(cols[i][2]), FadeIn(cols[i][3]), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(life, shift=UP * 0.2))
        self.clear_scene()
