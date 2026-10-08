from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.open_models.common import (
    block, cfg, heat_image, label, model, model_tag, note, show_chapter_card, source,
)
from videos.open_models.toys import softmax


class AttentionResiduals(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 12, "Kimi: attention across depth")
        self.c = cfg("kimi")
        self.tag = model_tag("kimi")
        self.add(self.tag)
        self.plain_sum()
        self.over_depth()
        self.blocks()
        self.real_queries()

    # ------------------------------------------------------------------
    def plain_sum(self):
        n = 5
        outs = VGroup(*[block(rf"layer {i + 1}", C.MLP if i % 2 else C.ATTN, width=2.0, height=0.55, font_size=24)
                        for i in range(n)]).arrange(UP, buff=0.35).move_to(LEFT * 3.4 + DOWN * 0.2)
        stream = Line(outs.get_bottom() + DOWN * 0.6 + LEFT * 1.8, outs.get_top() + UP * 0.6 + LEFT * 1.8, color=C.EMBED,
                      stroke_width=6)
        emb = label(r"embedding", font_size=22, color=C.EMBED).next_to(stream.get_start(), DOWN, buff=0.1)
        adds = VGroup()
        for o in outs:
            p = stream.point_from_proportion(0) * 0 + np.array([stream.get_x(), o.get_y() + 0.05, 0])
            adds.add(Arrow(o.get_left(), p, buff=0.05, color=GREY_B, stroke_width=2.5, max_tip_length_to_length_ratio=0.2))
        f = MathTex(r"\vec h_{l}", "=", r"\vec h_1", "+", r"f_1", "+", r"f_2", "+", r"\cdots", "+", r"f_{l-1}", font_size=40)
        f.to_edge(RIGHT, buff=0.5).shift(UP * 1.2)
        f[0].set_color(C.EMBED)
        f_l = label(r"every earlier output, added with weight 1", font_size=26, color=GREY_A).next_to(f, DOWN, buff=0.25)
        rnn = VGroup(label(r"like an old recurrent network over time:", font_size=26),
                     label(r"everything squeezed into one running state", font_size=26, color=YELLOW))
        rnn.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(f_l, DOWN, buff=0.6).align_to(f_l, LEFT)
        with self.voiceover(
            "Kimi's next idea applies attention in a direction you might not expect: across depth. <bookmark mark='r'/> "
            "Recall the residual stream. Each layer reads the running vector, computes something, and adds its result back. "
            "<bookmark mark='s'/> So the input to any layer is the embedding plus the outputs of all the layers below it, "
            "all added up with equal weight. <bookmark mark='n'/> Moonshot points out that this is much like how an old "
            "recurrent network treats time: everything that has happened gets squeezed into one running state."
        ) as vo:
            vo.wait_until("r")
            self.play(Create(stream), FadeIn(emb), LaggedStart(*[FadeIn(o) for o in outs], lag_ratio=0.15))
            self.play(LaggedStart(*[GrowArrow(a) for a in adds], lag_ratio=0.15))
            vo.wait_until("s")
            self.play(Write(f), FadeIn(f_l))
            vo.wait_until("n")
            self.play(FadeIn(rnn))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def over_depth(self):
        n = 6
        srcs = VGroup(*[RoundedRectangle(width=1.1, height=0.7, corner_radius=0.08, stroke_color=GREY_B, stroke_width=2,
                                         fill_color=C.EMBED if i == 0 else (C.ATTN if i % 2 else C.MLP), fill_opacity=0.3)
                        for i in range(n)]).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.2 + LEFT * 1.4)
        sl = VGroup(*[MathTex(r"\vec h_1" if i == 0 else rf"f_{{{i}}}", font_size=30).move_to(s) for i, s in enumerate(srcs)])
        here = RoundedRectangle(width=1.3, height=0.8, corner_radius=0.08, stroke_color=YELLOW, stroke_width=3,
                                fill_color=YELLOW, fill_opacity=0.15).next_to(srcs, RIGHT, buff=0.9)
        here_l = label(r"layer $l$", font_size=26).move_to(here)
        depth = Arrow(srcs.get_left() + DOWN * 0.7, here.get_right() + DOWN * 0.7 + RIGHT * 0.2, buff=0, color=GREY_B,
                      stroke_width=2)
        depth_l = label(r"depth", font_size=24, color=GREY_A).next_to(depth, DOWN, buff=0.1)
        logits = np.array([1.4, -0.3, 0.2, 1.9, -0.8, 0.9])
        a = softmax(logits)
        arcs = VGroup(*[ArcBetweenPoints(here.get_top(), s.get_top(), angle=0.9, color=C.DEPTH,
                                         stroke_width=1 + 9 * w).set_stroke(opacity=0.35 + 0.65 * min(1, 2.5 * w))
                        for s, w in zip(srcs, a)])
        wl = VGroup(*[DecimalNumber(w, num_decimal_places=2, font_size=24, color=C.DEPTH).next_to(s, UP, buff=0.12)
                      for s, w in zip(srcs, a)])
        f = MathTex(r"\vec h_l", "=", r"\sum_i", r"\alpha_{i\to l}", r"\,\vec v_i", font_size=44)
        f2 = MathTex(r"\alpha_{i\to l}", "=", r"\operatorname{softmax}_i", r"\big(", r"\vec w_l", r"\cdot",
                     r"\mathrm{RMSNorm}(\vec v_i)", r"\big)", font_size=40)
        VGroup(f, f2).arrange(DOWN, buff=0.3).to_edge(UP, buff=1.0).shift(RIGHT * 0.8)
        f[0].set_color(C.EMBED)
        f[3].set_color(C.DEPTH)
        f2[0].set_color(C.DEPTH)
        f2[4].set_color(C.QUERY)
        wq = label(r"$\vec w_l$: one learned query vector per layer", font_size=26, color=C.QUERY).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Transformers fixed that problem for sequences, by letting every token attend over all the tokens before it. "
            "<bookmark mark='q'/> Attention Residuals do the same thing for layers. Turn the depth axis on its side, so the "
            "earlier layers' outputs line up like tokens in a sequence. <bookmark mark='a'/> Each layer now attends over "
            "them, and chooses what to read. <bookmark mark='k'/> Concretely, each layer has its own learned query vector. "
            "The keys are the earlier outputs themselves, normalized. <bookmark mark='m'/> A softmax turns the matches into "
            "weights, <bookmark mark='o'/> and the layer's input is the weighted blend, instead of the plain sum."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(s) for s in srcs], lag_ratio=0.1), FadeIn(sl), FadeIn(here), FadeIn(here_l),
                      GrowArrow(depth), FadeIn(depth_l))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(x) for x in arcs], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("k")
            self.play(Write(f2[4:]), FadeIn(wq))
            vo.wait_until("m")
            self.play(Write(f2[:4]), FadeIn(wl))
            vo.wait_until("o")
            self.play(Write(f))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def blocks(self):
        c = self.c
        assert c["attn_res_block"] == 12 and c["layers"] == 93
        n_blocks = -(-93 // 12)
        assert n_blocks == 8
        cells = VGroup(*[Rectangle(width=0.1, height=0.6, stroke_width=0,
                                   fill_color=C.MEMORY if t == "kda" else C.GLOBAL, fill_opacity=0.85)
                         for t in c["layer_types"]]).arrange(RIGHT, buff=0.024).move_to(DOWN * 0.6 + RIGHT * 0.5)
        groups = VGroup(*[VGroup(*cells[12 * b:12 * (b + 1)]) for b in range(n_blocks)])
        boxes = VGroup(*[SurroundingRectangle(g, buff=0.06, color=WHITE, stroke_width=2) for g in groups])
        blabels = VGroup(*[label(rf"block {b + 1}", font_size=20, color=GREY_A).next_to(boxes[b], DOWN, buff=0.12)
                           for b in range(n_blocks)])
        emb = RoundedRectangle(width=0.7, height=0.6, corner_radius=0.06, stroke_color=C.EMBED, stroke_width=2,
                               fill_color=C.EMBED, fill_opacity=0.3).next_to(cells, LEFT, buff=0.35)
        emb_l = label(r"embedding", font_size=20, color=C.EMBED).next_to(emb, DOWN, buff=0.12)
        rule = VGroup(
            label(r"inside a block: plain sum", font_size=28),
            label(r"across blocks: attention over at most 9 summaries", font_size=28, color=C.DEPTH),
            label(r"(the embedding, one per finished block, and the current block so far)", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=1.55)
        title = label(r"Block Attention Residuals in K3: 93 layers in blocks of 12", font_size=32).to_edge(UP, buff=0.9)
        with self.voiceover(
            "<bookmark mark='b'/> Keeping every one of 93 layers' outputs around would cost a lot of memory, so K3 groups "
            "its layers into blocks of 12. <bookmark mark='s'/> Inside a block, outputs are summed as usual. "
            "<bookmark mark='a'/> Across blocks, each layer attends over at most nine summaries: the embedding, one for "
            "each finished block, and the current block so far."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("b")
            self.play(FadeIn(cells, lag_ratio=0.01), FadeIn(emb), FadeIn(emb_l), run_time=1.2)
            self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.1), FadeIn(blabels))
            vo.wait_until("s")
            self.play(FadeIn(rule[0]))
            vo.wait_until("a")
            self.play(FadeIn(rule[1]), FadeIn(rule[2]))
            arcs = VGroup(*[ArcBetweenPoints(cells[70].get_top(), t.get_top(), angle=0.5, color=C.DEPTH, stroke_width=3)
                            for t in [emb] + [boxes[b] for b in range(5)]])
            self.play(Indicate(cells[70], color=YELLOW), LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.1))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def real_queries(self):
        q = model("kimi")["attn_res_queries"]
        C_ = np.array(q["cosine"])
        assert C_.shape == (186, 186)
        np.fill_diagonal(C_, 1.0)
        C_ = np.nan_to_num(C_)
        within, across = [], []
        for i in range(1, 92):
            v = C_[np.ix_([2 * i, 2 * i + 1], [2 * i + 2, 2 * i + 3])].mean()
            (across if (i + 1) % 12 == 0 else within).append(v)
        assert np.mean(within) > 0.45 and np.mean(across) < 0.27
        img = heat_image(C_, height=5.0, colors=(BACKGROUND, "#FFB86B"), vmin=0.0, vmax=0.7).move_to(LEFT * 2.3 + DOWN * 0.4)
        frame = SurroundingRectangle(img, buff=0.0, color=GREY_B, stroke_width=1.5)
        ticks = VGroup()
        x0, y0, s = img.get_left()[0], img.get_top()[1], img.width / 186
        for b in range(1, 8):
            p = 24 * b * s
            ticks.add(DashedLine([x0 + p, y0, 0], [x0 + p, y0 - img.height, 0], color=WHITE, stroke_width=1,
                                 dash_length=0.06).set_stroke(opacity=0.5))
            ticks.add(DashedLine([x0, y0 - p, 0], [x0 + img.width, y0 - p, 0], color=WHITE, stroke_width=1,
                                 dash_length=0.06).set_stroke(opacity=0.5))
        xl = label(r"186 learned queries (2 per layer), bottom layer first", font_size=22, color=GREY_A)
        xl.next_to(frame, DOWN, buff=0.15)
        b_l = label(r"dashed lines: the 12-layer block boundaries", font_size=22, color=GREY_A).next_to(xl, DOWN, buff=0.08)
        facts = VGroup(
            label(r"similarity of neighbouring layers' queries:", font_size=26),
            label(rf"same block: {np.mean(within):.2f}", font_size=30, color="#FFB86B"),
            label(rf"across a block boundary: {np.mean(across):.2f}", font_size=30, color=GREY_B),
            label(r"layers in a block see the same past summaries,\\and learned to ask similar questions of them",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4)
        title = label(r"Kimi K3's depth-attention queries, read from its weights", font_size=32).to_edge(UP, buff=0.9)
        with self.voiceover(
            "Here are the real learned queries: 186 of them, one for the attention half and one for the feed-forward half "
            "of every layer. <bookmark mark='h'/> This grid shows how similar each pair of queries is: brighter means they "
            "point in more similar directions. <bookmark mark='b'/> The dashed lines are the block boundaries, and the "
            "bright squares line up with them. <bookmark mark='n'/> Neighbouring layers in the same block have similarity "
            "of about 0.47; neighbours across a boundary, only about 0.25. Layers in the same block see the same set of "
            "past summaries, and they learned to ask similar questions of them."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("h")
            self.play(FadeIn(img), Create(frame), FadeIn(xl), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ticks, lag_ratio=0.05), FadeIn(b_l))
            vo.wait_until("n")
            self.play(LaggedStart(*[FadeIn(x, shift=LEFT * 0.1) for x in facts], lag_ratio=0.3), run_time=2)
        self.clear_scene()
