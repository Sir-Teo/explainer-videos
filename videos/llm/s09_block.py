from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.llm.common import Plot, block, data, label, show_chapter_card


def fmt(n: int) -> str:
    return f"{n:,}".replace(",", "{,}")


def residual_block(height=6.4, x=0.0, scale=1.0) -> VGroup:
    """Pre-norm transformer block: stream with two read -> LN -> f -> add branches."""
    y0, y1 = -height / 2, height / 2
    stream = Arrow([x, y0, 0], [x, y1, 0], buff=0, color=C.EMBED, stroke_width=6, max_tip_length_to_length_ratio=0.04)
    g = VGroup(stream)
    adds, branches = VGroup(), VGroup()
    for k, (name, col) in enumerate([("Attention", C.ATTN), ("MLP", C.MLP)]):
        yb = y0 + height * (0.3 + 0.4 * k)
        ln = block("LN", C.NORM, width=0.9, height=0.6, font_size=26).move_to([x + 1.6, yb - 0.55, 0])
        f = block(name, col, width=2.3, height=0.75, font_size=30).move_to([x + 1.6, yb + 0.55, 0])
        plus = VGroup(Circle(0.2, color=WHITE, stroke_width=3).set_fill(BACKGROUND, 1),
                      MathTex("+", font_size=36)).move_to([x, yb + 1.15, 0])
        p_read = [x, yb - 1.15, 0]
        read = VGroup(Line(p_read, [x + 1.6, yb - 1.15, 0], color=GREY_B, stroke_width=3),
                      Arrow([x + 1.6, yb - 1.15, 0], ln.get_bottom(), buff=0.02, color=GREY_B, stroke_width=3,
                            max_tip_length_to_length_ratio=0.3))
        mid = Arrow(ln.get_top(), f.get_bottom(), buff=0.02, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        back = VGroup(Line(f.get_top(), [x + 1.6, yb + 1.15, 0], color=col, stroke_width=3),
                      Arrow([x + 1.6, yb + 1.15, 0], plus.get_right(), buff=0.02, color=col, stroke_width=3,
                            max_tip_length_to_length_ratio=0.3))
        br = VGroup(read, ln, mid, f, back)
        br.ln, br.f = ln, f
        branches.add(br)
        adds.add(plus)
    g.add(branches, adds)
    g.stream, g.branches, g.adds = stream, branches, adds
    return g.scale(scale)


class TransformerBlock(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 8, "Stacking the blocks")
        self.d = data()
        self.assemble()
        self.layer_norm()
        self.roles()
        self.stack_and_count()

    # ------------------------------------------------------------------
    def assemble(self):
        blk = residual_block(height=6.6).shift(LEFT * 3.6 + DOWN * 0.1)
        x_in = MathTex(r"\vec x", font_size=40, color=C.EMBED).next_to(blk.stream, DOWN, buff=0.1)
        x_l = label(r"residual stream", font_size=28, color=C.EMBED).next_to(blk.stream.get_start(), LEFT, buff=0.3)
        x_l.shift(UP * 0.6)
        f1 = MathTex(r"\vec x", r"\;\leftarrow\;", r"\vec x", "+", r"\text{Attention}", r"(\text{LN}(\vec x))", font_size=40)
        f2 = MathTex(r"\vec x", r"\;\leftarrow\;", r"\vec x", "+", r"\text{MLP}", r"(\text{LN}(\vec x))", font_size=40)
        for f, col in ((f1, C.ATTN), (f2, C.MLP)):
            f[0].set_color(C.EMBED)
            f[2].set_color(C.EMBED)
            f[4].set_color(col)
        fs = VGroup(f2, f1).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(RIGHT * 3.4 + DOWN * 0.1)
        att, mlp = blk.branches
        with self.voiceover(
            "Let's assemble one complete layer, called a transformer block. <bookmark mark='s'/> Picture the residual stream "
            "as a line running upward. <bookmark mark='a'/> The attention step branches off, reads the current vectors, "
            "<bookmark mark='p'/> and adds its result back in. <bookmark mark='m'/> Then the MLP does the same: it reads, "
            "and adds its result back in."
        ) as vo:
            vo.wait_until("s")
            self.play(GrowArrow(blk.stream), FadeIn(x_in), FadeIn(x_l))
            vo.wait_until("a")
            self.play(Create(att[0]), FadeIn(att[1]), Create(att[2]), FadeIn(att[3]), run_time=1.5)
            vo.wait_until("p")
            self.play(Create(att[4]), FadeIn(blk.adds[0]), Write(f1))
            vo.wait_until("m")
            self.play(Create(mlp[0]), FadeIn(mlp[1]), Create(mlp[2]), FadeIn(mlp[3]), run_time=1.2)
            self.play(Create(mlp[4]), FadeIn(blk.adds[1]), Write(f2))
        self.blk = VGroup(blk, x_in, x_l)
        self.formulas = fs

    # ------------------------------------------------------------------
    def layer_norm(self):
        blk = self.blk[0]
        lns = VGroup(blk.branches[0].ln, blk.branches[1].ln)
        rng = np.random.default_rng(3)
        raw = rng.normal(1.6, 2.4, 12)
        centered = raw - raw.mean()
        normed = centered / centered.std()
        gamma = np.abs(rng.normal(1.0, 0.35, 12))
        beta = rng.normal(0, 0.3, 12)
        final = gamma * normed + beta
        pl = Plot((0, 12), (-5, 7), width=5.2, height=2.8, y_ticks=[-4, 0, 4]).move_to(RIGHT * 3.4 + DOWN * 1.6)
        zero = DashedLine(pl.c2p(0, 0), pl.c2p(12, 0), color=GREY_D, stroke_width=1.5)

        def bars(v, color=C.NORM):
            g = VGroup()
            for i, val in enumerate(v):
                top, bot = pl.c2p(i + 0.5, max(val, 0)), pl.c2p(i + 0.5, min(val, 0))
                r = Rectangle(width=0.3, height=max(0.01, top[1] - bot[1]), stroke_width=0, fill_color=color, fill_opacity=0.9)
                r.move_to((top + bot) / 2)
                g.add(r)
            return g

        b_raw = bars(raw)
        steps = VGroup(label(r"subtract the mean", font_size=28), label(r"divide by the spread", font_size=28),
                       label(r"learned scale and shift", font_size=28))
        ln_f = MathTex(r"\text{LN}(\vec x)", "=", r"\gamma \odot", r"{\vec x - \mu \over \sigma}", r"+\, \beta", font_size=38)
        ln_f.next_to(pl, UP, buff=0.5)
        with self.voiceover(
            "One detail I've skipped: <bookmark mark='l'/> before each branch reads the stream, the vector passes through "
            "a layer norm. <bookmark mark='a'/> It shifts each vector so that its numbers average to zero, "
            "<bookmark mark='b'/> rescales them to a standard size, <bookmark mark='c'/> then applies a learned scale and "
            "shift. This keeps the numbers in a healthy range as they pass through dozens of layers, which makes training "
            "much more stable."
        ) as vo:
            self.play(self.formulas.animate.scale(0.8).to_corner(UR, buff=0.4))
            vo.wait_until("l")
            self.play(Indicate(lns, color=YELLOW, scale_factor=1.3), Create(pl), FadeIn(zero), FadeIn(b_raw), Write(ln_f))
            vo.wait_until("a")
            st = steps[0].next_to(pl, DOWN, buff=0.25)
            self.play(Transform(b_raw, bars(centered)), FadeIn(st))
            vo.wait_until("b")
            self.play(Transform(b_raw, bars(normed)), Transform(st, steps[1].move_to(st)))
            vo.wait_until("c")
            self.play(Transform(b_raw, bars(final, C.EMBED)), Transform(st, steps[2].move_to(st)))
        self.play(FadeOut(VGroup(pl, zero, b_raw, st, ln_f)))

    # ------------------------------------------------------------------
    def roles(self):
        r1 = VGroup(block("Attention", C.ATTN, width=2.2, height=0.8, font_size=30),
                    label(r"moves information\\\emph{between} positions", font_size=30)).arrange(RIGHT, buff=0.35)
        r2 = VGroup(block("MLP", C.MLP, width=2.2, height=0.8, font_size=30),
                    label(r"processes information\\\emph{within} each position", font_size=30)).arrange(RIGHT, buff=0.35)
        for r in (r1, r2):
            r[1].align_to(r[0].get_right() + RIGHT * 0.35, LEFT)
        roles = VGroup(r1, r2).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(RIGHT * 3.7 + DOWN * 1.5)
        with self.voiceover(
            "A useful summary of the two halves: <bookmark mark='a'/> attention moves information between positions. "
            "<bookmark mark='m'/> The MLP processes the information sitting at each position."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(r1, shift=UP * 0.2))
            vo.wait_until("m")
            self.play(FadeIn(r2, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def stack_and_count(self):
        pp = self.d["params"]
        assert pp["total"] == 124439808 and pp["n_layer"] == 12
        def mini():
            a = Rectangle(width=0.8, height=0.32, stroke_color=C.ATTN, stroke_width=1.5, fill_color=C.ATTN, fill_opacity=0.35)
            m = Rectangle(width=0.8, height=0.32, stroke_color=C.MLP, stroke_width=1.5, fill_color=C.MLP, fill_opacity=0.35)
            return VGroup(a, m).arrange(RIGHT, buff=0.08)

        blocks = VGroup(*[mini() for _ in range(12)]).arrange(UP, buff=0.12)
        emb = block("embed", C.EMBED, width=1.7, height=0.42, font_size=24).next_to(blocks, DOWN, buff=0.18)
        unemb = block("predict", C.PROB, width=1.7, height=0.42, font_size=24).next_to(blocks, UP, buff=0.18)
        stream = Line(emb.get_top(), unemb.get_bottom(), color=C.EMBED, stroke_width=3).next_to(blocks, LEFT, buff=0.12)
        stack = VGroup(stream, blocks, emb, unemb).move_to(LEFT * 5.2)
        brace = Brace(blocks, RIGHT, buff=0.15, color=GREY_B)
        bl = label(r"12 blocks\\in GPT-2 small", font_size=28)
        bl.next_to(brace, RIGHT, buff=0.15)
        g3 = label(r"(GPT-3: 96)", font_size=26, color=GREY_A).next_to(bl, DOWN, buff=0.15)
        with self.voiceover(
            "Then stack these blocks, one on top of another. <bookmark mark='s'/> GPT-2 small has 12. "
            "<bookmark mark='g'/> GPT-3 has 96. Embeddings go in at the bottom, and the prediction comes out at the top."
        ) as vo:
            self.play(FadeIn(emb), Create(stream))
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in blocks], lag_ratio=0.1), run_time=2)
            self.play(FadeIn(unemb))
            vo.wait_until("s")
            self.play(GrowFromCenter(brace), FadeIn(bl))
            vo.wait_until("g")
            self.play(FadeIn(g3))

        rows = [
            (r"token embeddings", r"50{,}257 \times 768", pp["token_embedding"], C.EMBED),
            (r"position embeddings", r"1{,}024 \times 768", pp["position_embedding"], C.POSITION),
            (r"attention, per block", r"4 \times 768^2 + \text{biases}", pp["attention_per_layer"], C.ATTN),
            (r"MLP, per block", r"2 \times 768 \times 3{,}072 + \text{biases}", pp["mlp_per_layer"], C.MLP),
            (r"layer norms", r"", pp["norms_per_layer"] * 12 + pp["final_norm"], C.NORM),
        ]
        table = VGroup()
        for name, how, n, col in rows:
            r = VGroup(label(name, font_size=28, color=col), MathTex(how, font_size=26, color=GREY_A) if how else VectorizedPoint(),
                       MathTex(fmt(n), font_size=30))
            table.add(r)
        x_name, x_how, x_num = -1.0, 1.85, 6.9
        for i, r in enumerate(table):
            y = 2.6 - i * 0.62
            r[0].move_to([x_name, y, 0], aligned_edge=LEFT)
            r[1].move_to([x_how, y, 0], aligned_edge=LEFT)
            r[2].move_to([x_num, y, 0], aligned_edge=RIGHT)
        line = Line([x_name, 2.6 - 5 * 0.62 + 0.15, 0], [x_num, 2.6 - 5 * 0.62 + 0.15, 0], color=GREY_B, stroke_width=2)
        total = VGroup(label(r"total", font_size=32), MathTex(fmt(pp["total"]), font_size=36, color=YELLOW))
        total[0].move_to([x_name, 2.6 - 5.6 * 0.62, 0], aligned_edge=LEFT)
        total[1].move_to([x_num, 2.6 - 5.6 * 0.62, 0], aligned_edge=RIGHT)
        with self.voiceover(
            "Now we can count every single parameter in GPT-2 small. <bookmark mark='e'/> The token embedding table: "
            "50,257 tokens times 768 numbers, about 38.6 million. <bookmark mark='p'/> Position embeddings: under a million. "
            "<bookmark mark='a'/> Each attention layer: about 2.4 million, <bookmark mark='m'/> each MLP: about 4.7 million, "
            "<bookmark mark='n'/> plus a few thousand for the layer norms."
        ) as vo:
            for i, m in enumerate("epamn"):
                vo.wait_until(m)
                self.play(FadeIn(table[i], shift=LEFT * 0.2), run_time=0.7)

        share = (pp["token_embedding"] + pp["position_embedding"]) / pp["total"]
        assert 0.3 < share < 0.33
        frac = VGroup(
            Rectangle(width=10.0 * pp["token_embedding"] / pp["total"], height=0.45, stroke_width=0, fill_color=C.EMBED,
                      fill_opacity=0.85),
            Rectangle(width=max(0.05, 10.0 * pp["position_embedding"] / pp["total"]), height=0.45, stroke_width=0,
                      fill_color=C.POSITION, fill_opacity=0.85),
            Rectangle(width=10.0 * 12 * pp["attention_per_layer"] / pp["total"], height=0.45, stroke_width=0, fill_color=C.ATTN,
                      fill_opacity=0.85),
            Rectangle(width=10.0 * 12 * pp["mlp_per_layer"] / pp["total"], height=0.45, stroke_width=0, fill_color=C.MLP,
                      fill_opacity=0.85),
        ).arrange(RIGHT, buff=0).move_to(RIGHT * 1.6 + DOWN * 3.3)
        fl = label(r"almost a third of GPT-2 small is its embedding table", font_size=28, color=GREY_A).next_to(frac, UP, 0.15)
        with self.voiceover(
            "Multiply the per-block numbers by 12, add everything up, <bookmark mark='t'/> and you get 124,439,808 "
            "parameters: the 124 million in GPT-2 small's name. <bookmark mark='f'/> Notice that almost a third of this "
            "small model is just the embedding table. In bigger models, the blocks dominate."
        ) as vo:
            vo.wait_until("t")
            self.play(Create(line), FadeIn(total))
            vo.wait_until("f")
            self.play(FadeOut(VGroup(brace, bl, g3)), LaggedStart(*[GrowFromEdge(r, LEFT) for r in frac], lag_ratio=0.3),
                      FadeIn(fl))
        self.clear_scene()
