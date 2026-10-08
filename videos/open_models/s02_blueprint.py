from __future__ import annotations


from explainer import *  # noqa: F403
from videos.open_models.common import (
    MONO, block, label, random_values, show_chapter_card, vector_strip,
)
from videos.open_models.toys import kv_cache

WORDS = ["The", "cat", "sat", "on", "the"]


def token_box(s: str, color=C.TOKEN, font_size=28) -> VGroup:
    t = Text(s, font=MONO, font_size=font_size)
    box = RoundedRectangle(width=max(0.9, t.width + 0.3), height=0.6, corner_radius=0.08, stroke_color=color,
                           stroke_width=2, fill_color=color, fill_opacity=0.12)
    return VGroup(box, t.move_to(box))


class Blueprint(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 1, "The blueprint, and its two bills")
        self.blueprint()
        self.compute_bill()
        self.memory_bill()

    # ------------------------------------------------------------------
    def blueprint(self):
        toks = VGroup(*[token_box(w) for w in WORDS]).arrange(RIGHT, buff=0.25).move_to(DOWN * 3.3 + LEFT * 2.6)
        vecs = VGroup(*[vector_strip(random_values(6, seed=i), cell=0.15).next_to(t, UP, buff=0.25) for i, t in enumerate(toks)])
        layers = VGroup()
        for i in range(2):
            att = block("attention", C.ATTN, width=5.6, height=0.5, font_size=26)
            ffn = block("feed-forward network", C.MLP, width=5.6, height=0.5, font_size=26)
            layers.add(VGroup(att, ffn).arrange(UP, buff=0.1))
        layers.arrange(UP, buff=0.22).next_to(vecs, UP, buff=0.3)
        layers.set_x(toks.get_x())
        dots = MathTex(r"\vdots", color=GREY_B).next_to(layers, UP, buff=0.08)
        out = VGroup(*[Rectangle(width=0.18, height=h, stroke_width=0, fill_color=C.PROB, fill_opacity=0.85)
                       for h in (0.1, 0.55, 0.2, 0.08, 0.3, 0.12, 0.05)]).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
        out.next_to(dots, UP, buff=0.15).set_x(toks[-1].get_x())
        out_l = label(r"probability of each\\possible next token", font_size=24, color=C.PROB).next_to(out, RIGHT, buff=0.25)
        stream = Arrow([0, vecs.get_bottom()[1], 0], [0, out.get_bottom()[1], 0], buff=0, color=C.EMBED,
                       stroke_width=5, max_tip_length_to_length_ratio=0.03)
        stream.set_x(layers.get_left()[0] - 0.35)
        stream_l = label(r"each token's vector flows up", font_size=24, color=C.EMBED).rotate(PI / 2).next_to(stream, LEFT, 0.1)
        notes = VGroup(
            label(r"\textbf{attention}: each token looks back", font_size=26, color=C.ATTN),
            label(r"at earlier tokens and pulls in what's relevant", font_size=26, color=C.ATTN),
            label(r"\textbf{feed-forward}: each token is processed", font_size=26, color=C.MLP),
            label(r"on its own by a big two-layer network", font_size=26, color=C.MLP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(RIGHT, buff=0.35).shift(UP * 0.3)
        notes[2].shift(DOWN * 0.25)
        notes[3].shift(DOWN * 0.25)

        with self.voiceover(
            "Let's start from the blueprint all three share. Text is cut into tokens, <bookmark mark='e'/> each token "
            "becomes a long vector of numbers, <bookmark mark='l'/> and those vectors flow up through a stack of layers. "
            "Each layer has two parts. <bookmark mark='a'/> In attention, every token looks back at the tokens before it, "
            "and pulls in whatever is relevant. <bookmark mark='f'/> In the feed-forward network, each token is processed "
            "on its own, by a big two-layer network; this is where much of a model's knowledge seems to be stored. "
            "<bookmark mark='p'/> At the top, the final vector becomes a probability for every possible next token. Pick "
            "one, append it, and repeat."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in toks], lag_ratio=0.1))
            vo.wait_until("e")
            self.play(*[TransformFromCopy(t, v) for t, v in zip(toks, vecs)], run_time=1.2)
            vo.wait_until("l")
            self.play(GrowArrow(stream), FadeIn(stream_l),
                      LaggedStart(*[FadeIn(l, shift=UP * 0.15) for l in layers], lag_ratio=0.2), FadeIn(dots), run_time=1.6)
            vo.wait_until("a")
            self.play(*[Indicate(l[0], color=C.ATTN, scale_factor=1.04) for l in layers], FadeIn(notes[:2]))
            vo.wait_until("f")
            self.play(*[Indicate(l[1], color=C.MLP, scale_factor=1.04) for l in layers], FadeIn(notes[2:]))
            vo.wait_until("p")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in out], lag_ratio=0.08), FadeIn(out_l))
        self.layers, self.toks = layers, toks
        self.clear_scene()

    # ------------------------------------------------------------------
    def compute_bill(self):
        title = label(r"Bill 1: compute", font_size=40, color=C.MLP).to_edge(UP, buff=0.4)
        grid = VGroup(*[Square(0.16, stroke_width=0, fill_color=C.MLP, fill_opacity=0.2) for _ in range(20 * 26)])
        grid.arrange_in_grid(20, 26, buff=0.035).move_to(LEFT * 2.6 + DOWN * 0.3)
        g_l = label(r"every parameter of a dense model", font_size=26, color=GREY_A).next_to(grid, UP, buff=0.15)
        tok = token_box("cat").next_to(grid, LEFT, buff=0.35)
        rule = MathTex(r"\text{operations per token}", r"\approx", r"2", r"\times", r"\text{parameters}", font_size=40)
        rule[4].set_color(C.MLP)
        rule.scale(0.85).to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        tril = MathTex(r"1\ \text{trillion parameters}", r"\;\Rightarrow\;", r"2\times 10^{12}", font_size=34)
        tril[2].set_color(YELLOW)
        tril.next_to(rule, DOWN, buff=0.5).align_to(rule, RIGHT)
        tril_l = label(r"operations for every single token", font_size=28, color=YELLOW).next_to(tril, DOWN, buff=0.2)
        tril_l.align_to(rule, RIGHT)
        with self.voiceover(
            "At this scale, that design runs up two bills. <bookmark mark='c'/> The first is compute. In a plain, dense "
            "transformer, every parameter takes part in processing every token: <bookmark mark='r'/> about two arithmetic "
            "operations per parameter, per token, one multiply and one add. <bookmark mark='t'/> For a trillion-parameter "
            "model, that would be two trillion operations for every single token it reads or writes."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("c")
            self.play(FadeIn(grid, lag_ratio=0.001), FadeIn(g_l), FadeIn(tok), run_time=1.2)
            self.play(grid.animate.set_fill(opacity=0.9), Indicate(tok, color=WHITE), run_time=1.0)
            vo.wait_until("r")
            self.play(Write(rule))
            vo.wait_until("t")
            self.play(FadeIn(tril, shift=UP * 0.2), FadeIn(tril_l))
        self.clear_scene()

    # ------------------------------------------------------------------
    def memory_bill(self):
        title = label(r"Bill 2: memory, which grows with the context", font_size=40, color=C.ATTN).to_edge(UP, buff=0.4)
        n_l, n_t = 4, 14
        cw = 0.36
        cache = VGroup()
        for i in range(n_l):
            row = VGroup()
            for j in range(n_t):
                k = Rectangle(width=cw * 0.42, height=0.42, stroke_width=0, fill_color=C.KEY, fill_opacity=0.8)
                v = Rectangle(width=cw * 0.42, height=0.42, stroke_width=0, fill_color=C.VALUE, fill_opacity=0.8)
                row.add(VGroup(k, v).arrange(RIGHT, buff=0.02))
            row.arrange(RIGHT, buff=0.1)
            cache.add(row)
        cache.arrange(UP, buff=0.22).move_to(LEFT * 1.3 + DOWN * 0.2)
        lay_l = VGroup(*[label(rf"layer {i + 1}", font_size=24, color=GREY_A).next_to(cache[i], LEFT, buff=0.25)
                         for i in range(n_l)])
        leg = VGroup(
            VGroup(Square(0.2, stroke_width=0, fill_color=C.KEY, fill_opacity=0.8), label("key", font_size=24, color=C.KEY)),
            VGroup(Square(0.2, stroke_width=0, fill_color=C.VALUE, fill_opacity=0.8),
                   label("value", font_size=24, color=C.VALUE)),
        )
        for g in leg:
            g.arrange(RIGHT, buff=0.1)
        leg.arrange(RIGHT, buff=0.4).next_to(cache, DOWN, buff=0.35)
        cap = label(r"the cache: one key and one value per token, per layer", font_size=26, color=GREY_A)
        cap.next_to(leg, DOWN, buff=0.2)
        newq = VGroup(Square(0.3, stroke_width=0, fill_color=C.QUERY, fill_opacity=0.9),
                      label(r"new token's query", font_size=24, color=C.QUERY)).arrange(DOWN, buff=0.1)
        newq.next_to(cache, RIGHT, buff=0.6).align_to(cache[1], DOWN)
        arcs = VGroup(*[ArcBetweenPoints(newq[0].get_left(), cache[1][j].get_top(), angle=-0.6, color=C.ATTN,
                                         stroke_width=1.5).set_stroke(opacity=0.6) for j in range(n_t)])

        tri = VGroup()
        n = 12
        for i in range(n):
            for j in range(i + 1):
                tri.add(Square(0.16, stroke_width=0, fill_color=C.ATTN, fill_opacity=0.7).move_to([j * 0.18, -i * 0.18, 0]))
        tri.move_to(RIGHT * 4.6 + DOWN * 0.2)
        tri_l = label(r"comparisons: every pair", font_size=26, color=C.ATTN).next_to(tri, UP, buff=0.2)
        quad = MathTex(r"\text{work} \propto n^2", font_size=36, color=C.ATTN).next_to(tri, DOWN, buff=0.25)

        with self.voiceover(
            "<bookmark mark='m'/> The second bill is memory, and it grows with the length of the context. To avoid "
            "recomputing, attention keeps a cache: <bookmark mark='c'/> a key and a value vector for every past token, in "
            "every layer. <bookmark mark='q'/> Each new token compares its query against all of those keys. "
            "<bookmark mark='g'/> So the cache grows with every token you add, <bookmark mark='s'/> and over a whole "
            "text, the number of comparisons grows with the square of its length."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("c")
            self.play(FadeIn(lay_l), LaggedStart(*[FadeIn(cache[i][j]) for j in range(8) for i in range(n_l)],
                                                 lag_ratio=0.02), FadeIn(leg), FadeIn(cap), run_time=1.5)
            vo.wait_until("q")
            self.play(FadeIn(newq), LaggedStart(*[Create(a) for a in arcs[:8]], lag_ratio=0.05), run_time=1.2)
            vo.wait_until("g")
            self.play(LaggedStart(*[FadeIn(cache[i][j], shift=LEFT * 0.1) for j in range(8, n_t) for i in range(n_l)],
                                  lag_ratio=0.02), LaggedStart(*[Create(a) for a in arcs[8:]], lag_ratio=0.05), run_time=1.6)
            vo.wait_until("s")
            self.play(cache.animate.shift(LEFT * 1.6), lay_l.animate.shift(LEFT * 1.6), leg.animate.shift(LEFT * 1.6),
                      cap.animate.shift(LEFT * 1.6), newq.animate.shift(LEFT * 1.6), arcs.animate.shift(LEFT * 1.6))
            self.play(LaggedStart(*[FadeIn(s) for s in tri], lag_ratio=0.01), FadeIn(tri_l), run_time=1.5)
            self.play(Write(quad))

        kv = kv_cache()["glm"]
        assert kv["mha_per_token"] > 5e6
        part = VGroup(label(r"All three pay bill 1 the same way: a \textbf{mixture of experts}.", font_size=32,
                            color=C.EXPERT),
                      label(r"Bill 2 is where they part ways.", font_size=32, color=C.ATTN)).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> All three models pay the first bill the same way, with a mixture of experts. "
            "<bookmark mark='b'/> The second bill is where they part ways."
        ) as vo:
            self.clear_scene(run_time=0.8)
            self.play(FadeIn(part[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(part[1], shift=UP * 0.2))
        self.clear_scene()
