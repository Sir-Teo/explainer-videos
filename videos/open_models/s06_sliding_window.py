from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.open_models.common import (
    Plot, cfg, label, layer_strip, model_tag, note, schematic_tag, show_chapter_card,
)
from videos.open_models.toys import cache_gb, kv_cache, swa_reach


class SlidingWindow(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 5, "MiMo: look nearby, mostly")
        self.c = cfg("mimo")
        self.tag = model_tag("mimo")
        self.add(self.tag)
        self.masks()
        self.layout()
        self.reach()
        self.memory()
        self.gqa()

    # ------------------------------------------------------------------
    def masks(self):
        c = self.c
        assert c["window"] == 128
        n, cell, w = 24, 0.2, 6

        def mask(window=None):
            g = VGroup()
            for i in range(n):
                for j in range(n):
                    if j > i:
                        col, op = GREY_E, 0.2
                    elif window is not None and i - j >= window:
                        col, op = GREY_D, 0.25
                    else:
                        col, op = (C.LOCAL if window else C.GLOBAL), 0.85
                    g.add(Square(cell * 0.9, stroke_width=0, fill_color=col, fill_opacity=op).move_to([j * cell, -i * cell, 0]))
            return g

        full, band = mask(), mask(w)
        full.move_to(LEFT * 2.2 + DOWN * 0.3)
        band.move_to(full)
        rl = label(r"token doing the looking", font_size=24, color=GREY_A).rotate(PI / 2).next_to(full, LEFT, buff=0.2)
        cl = label(r"token being looked at", font_size=24, color=GREY_A).next_to(full, UP, buff=0.2)
        t_full = label(r"global attention:\\every earlier token", font_size=30, color=C.GLOBAL).move_to(RIGHT * 3.6 + UP * 0.6)
        t_band = label(r"sliding window:\\only the last 128 tokens", font_size=30, color=C.LOCAL).move_to(t_full)
        w_note = note(r"window drawn as 6 tokens").next_to(t_band, DOWN, buff=0.3)
        with self.voiceover(
            "MiMo first. Here's the pattern of a normal attention layer: each row is a token, and each column a token it "
            "can look at. <bookmark mark='c'/> Every token sees everything before it, so the pattern is a triangle. "
            "<bookmark mark='w'/> In a sliding-window layer, each token only sees the most recent 128 tokens, itself "
            "included. The triangle becomes a narrow band, and the band never gets wider, however long the text."
        ) as vo:
            self.play(FadeIn(full, lag_ratio=0.002), FadeIn(rl), FadeIn(cl), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(t_full))
            vo.wait_until("w")
            self.play(Transform(full, band), Transform(t_full, t_band), FadeIn(w_note), run_time=1.5)
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def layout(self):
        c = self.c
        types = c["layer_types"]
        assert len(types) == 70 and types.count("swa") == 60 and types.count("global") == 10
        assert types[0] == "global" and types[-1] == "global" and c["dense_layers"] == 1
        strip = layer_strip(types, {"swa": C.LOCAL, "global": C.GLOBAL}, cell=0.15, gap=0.03, height=0.9)
        strip.move_to(UP * 0.4)
        nums = VGroup(*[MathTex(str(i + 1), font_size=20, color=GREY_B).next_to(strip[i], DOWN, buff=0.1)
                        for i in (0, 9, 19, 29, 39, 49, 59, 69)])
        leg = VGroup(
            VGroup(Square(0.25, stroke_width=0, fill_color=C.LOCAL, fill_opacity=0.9),
                   label(r"60 sliding-window layers", font_size=28, color=C.LOCAL)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.25, stroke_width=0, fill_color=C.GLOBAL, fill_opacity=0.9),
                   label(r"10 global layers", font_size=28, color=C.GLOBAL)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.8).next_to(strip, DOWN, buff=0.75)
        first = label(r"layer 1: global, with a dense feed-forward network", font_size=24, color=GREY_A)
        first.next_to(strip[0], UP, buff=0.35).align_to(strip, LEFT)
        last = label(r"layer 70: global", font_size=24, color=GREY_A).next_to(strip[-1], UP, buff=0.35).align_to(strip, RIGHT)
        title = label(r"MiMo-V2.6-Pro's 70 layers, from its config", font_size=32).to_edge(UP, buff=0.9)
        with self.voiceover(
            "<bookmark mark='p'/> Of MiMo's 70 layers, 60 are sliding-window layers, and 10 are global. "
            "<bookmark mark='l'/> Here's the real layout. The first layer is global, and then a global layer comes after "
            "every six or seven local ones, all the way up. <bookmark mark='e'/> The very last layer is global too."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("p")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in strip], lag_ratio=0.02), FadeIn(nums), run_time=2)
            self.play(FadeIn(leg))
            vo.wait_until("l")
            self.play(FadeIn(first), Indicate(strip[0], color=WHITE))
            self.play(LaggedStart(*[Indicate(r, color=WHITE, scale_factor=1.4) for r in strip if r.layer_type == "global"],
                                  lag_ratio=0.15), run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(last), Indicate(strip[-1], color=WHITE))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def reach(self):
        w = 4
        n = 22
        dots = VGroup(*[Dot(radius=0.07, color=GREY_B) for _ in range(n)]).arrange(RIGHT, buff=0.36)
        rows = VGroup(*[dots.copy() for _ in range(4)]).arrange(UP, buff=0.75).move_to(DOWN * 0.3 + RIGHT * 0.6)
        layer_l = VGroup(*[label(rf"layer {i + 1}", font_size=22, color=GREY_A).next_to(r, LEFT, buff=0.3)
                           for i, r in enumerate(rows)])
        target = n - 1
        arcs = VGroup()
        lit = []
        frontier = {target}
        for L in range(3, 0, -1):
            new = set()
            for t in frontier:
                for j in range(max(0, t - w + 1), t + 1):
                    new.add(j)
                    arcs.add(Line(rows[L][t].get_center(), rows[L - 1][j].get_center(), color=C.LOCAL, stroke_width=1.6)
                             .set_stroke(opacity=0.55))
            lit.append(sorted(new))
            frontier = new
        reach_l = label(r"after 3 window layers: 3 hops of up to 3 tokens back", font_size=26, color=C.LOCAL)
        reach_l.next_to(rows, DOWN, buff=0.35)
        assert swa_reach(128, 60) == 7620
        real = MathTex(r"60 \text{ layers} \times 127 \text{ tokens} = 7{,}620 \text{ tokens}", font_size=36, color=C.LOCAL)
        real.to_edge(UP, buff=0.9)
        glob = label(r"global layers: any token, in one hop", font_size=30, color=C.GLOBAL).next_to(real, DOWN, buff=0.2)
        with self.voiceover(
            "Information can still travel far. <bookmark mark='h'/> Within one local layer, a token can only pull from its "
            "window. <bookmark mark='r'/> But the next layer up can pull from tokens that have already pulled from their "
            "windows, so the reach grows with every layer. <bookmark mark='n'/> Through MiMo's 60 local layers, "
            "information could creep back about 7,600 tokens. <bookmark mark='g'/> But the long jumps are the global "
            "layers' job: they reach any token in the context, in a single hop."
        ) as vo:
            self.play(FadeIn(rows), FadeIn(layer_l), rows[3][target].animate.set_color(YELLOW).scale(1.6))
            vo.wait_until("h")
            for L, idx in zip((2, 1, 0), lit):
                seg = VGroup(*[a for a in arcs if abs(a.get_start()[1] - rows[L + 1][0].get_y()) < 1e-3])
                self.play(Create(seg), *[rows[L][j].animate.set_color(C.LOCAL).scale(1.3) for j in idx], run_time=0.9)
                if L == 2:
                    vo.wait_until("r")
            self.play(FadeIn(reach_l))
            vo.wait_until("n")
            self.play(Write(real))
            vo.wait_until("g")
            self.play(FadeIn(glob, shift=UP * 0.2))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def memory(self):
        kv = kv_cache()["mimo"]
        assert kv["per_token"] == 51200 and kv["all_global_per_token"] == 358400
        assert round(kv["fixed"] / 1e6) == 39
        win = VGroup(*[Rectangle(width=0.12, height=0.35, stroke_width=0, fill_color=C.LOCAL, fill_opacity=0.85)
                       for _ in range(12)]).arrange(RIGHT, buff=0.03)
        glob = VGroup(*[Rectangle(width=0.12, height=0.35, stroke_width=0, fill_color=C.GLOBAL, fill_opacity=0.85)
                        for _ in range(40)]).arrange(RIGHT, buff=0.03)
        win_l = label(r"a local layer caches its last 128 tokens, forever", font_size=26, color=C.LOCAL)
        glob_l = label(r"a global layer caches every token", font_size=26, color=C.GLOBAL)
        g1 = VGroup(win_l, win).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        g2 = VGroup(glob_l, glob).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        VGroup(g1, g2).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(UP, buff=1.0).to_edge(LEFT, buff=0.8)
        pl = Plot((0, 2), (0, 400), width=4.0, height=3.0, y_ticks=[0, 100, 200, 300, 400], font_size=22)
        pl.to_corner(DR, buff=0.8).shift(LEFT * 0.4)
        bars = VGroup(
            Rectangle(width=1.0, height=3.0 * 358.4 / 400, stroke_width=0, fill_color=GREY_B, fill_opacity=0.7),
            Rectangle(width=1.0, height=3.0 * 51.2 / 400, stroke_width=0, fill_color=C.MIMO, fill_opacity=0.95),
        )
        bars[0].move_to(pl.c2p(0.5, 0), aligned_edge=DOWN)
        bars[1].move_to(pl.c2p(1.5, 0), aligned_edge=DOWN)
        yl = label(r"GB of cache at a million tokens", font_size=24, color=GREY_A).next_to(pl, UP, buff=0.15)
        bl = VGroup(label(r"all 70 layers\\global", font_size=22, color=GREY_A).next_to(bars[0], DOWN, buff=0.15),
                    label(r"MiMo's\\actual layout", font_size=22, color=C.MIMO).next_to(pl.c2p(1.5, 0), DOWN, buff=0.15))
        bv = VGroup(label(r"358", font_size=28).next_to(bars[0], UP, buff=0.1),
                    label(r"51", font_size=28, color=C.MIMO).next_to(bars[1], UP, buff=0.1))
        per = VGroup(
            label(r"per token of context:", font_size=28),
            label(r"51 KB instead of 358 KB", font_size=32, color=YELLOW),
            label(r"plus a fixed 39 MB for all the windows", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.8).shift(UP * 0.4)
        assert abs(cache_gb(kv, 1e6) - 51.2) < 0.1
        cap = note(r"keys and values in 16-bit precision, computed from the config").to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The payoff is memory. <bookmark mark='s'/> A local layer only has to cache its last 128 tokens, no matter how "
            "long the context gets. <bookmark mark='g'/> Only the 10 global layers have to keep everything. "
            "<bookmark mark='n'/> So per token of context, MiMo caches about 51 kilobytes, where the same model with every "
            "layer global would need 358. <bookmark mark='t'/> At a million tokens, that's 51 gigabytes instead of 358."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeIn(win_l), LaggedStart(*[FadeIn(r) for r in win], lag_ratio=0.05))
            vo.wait_until("g")
            self.play(FadeIn(glob_l), LaggedStart(*[FadeIn(r) for r in glob], lag_ratio=0.02))
            vo.wait_until("n")
            self.play(FadeIn(per), FadeIn(cap))
            vo.wait_until("t")
            self.play(Create(pl), FadeIn(yl))
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(bl[0]), FadeIn(bv[0]))
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(bl[1]), FadeIn(bv[1]))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def gqa(self):
        c = self.c
        assert c["heads"] == 128 and c["kv_heads"] == 8 and c["swa_kv_heads"] == 8
        rope_dims = int(c["head_dim"] * c["rope_fraction"])
        assert rope_dims == 64 and c["head_dim"] == 192
        assert c["rope_theta_global"] == 10_000_000 and c["rope_theta_swa"] == 10_000
        qs = VGroup(*[Square(0.13, stroke_width=0, fill_color=C.QUERY, fill_opacity=0.9) for _ in range(128)])
        qs.arrange_in_grid(8, 16, buff=0.05)
        groups = VGroup(*[VGroup(*qs[16 * i:16 * (i + 1)]) for i in range(8)])
        kvs = VGroup(*[VGroup(Square(0.3, stroke_width=0, fill_color=C.KEY, fill_opacity=0.9),
                              Square(0.3, stroke_width=0, fill_color=C.VALUE, fill_opacity=0.9)).arrange(RIGHT, buff=0.03)
                       for _ in range(8)]).arrange(DOWN, buff=0.08)
        VGroup(qs, kvs).arrange(RIGHT, buff=2.2).move_to(UP * 0.7)
        lines = VGroup(*[Line(groups[i].get_right(), kvs[i].get_left(), color=GREY_B, stroke_width=1.5) for i in range(8)])
        q_l = label(r"128 query heads", font_size=28, color=C.QUERY).next_to(qs, UP, buff=0.2)
        kv_l = label(r"8 cached key--value heads", font_size=28).next_to(kvs, UP, buff=0.2)
        g_l = label(r"grouped-query attention: 16 query heads share each cached entry", font_size=28)
        g_l.next_to(VGroup(qs, kvs), DOWN, buff=0.4)
        head = VGroup(*[Square(0.07, stroke_width=0, fill_color=C.POSITION if i < 64 else C.QUERY, fill_opacity=0.9)
                        for i in range(192)]).arrange(RIGHT, buff=0.01)
        head.width = 11.0
        head.to_edge(DOWN, buff=1.0)
        hb1 = Brace(VGroup(*head[:64]), DOWN, buff=0.05, color=C.POSITION)
        hb2 = Brace(VGroup(*head[64:]), DOWN, buff=0.05, color=C.QUERY)
        ht1 = label(r"64: rotated by position", font_size=22, color=C.POSITION).next_to(hb1, DOWN, buff=0.08)
        ht2 = label(r"128: content only", font_size=22, color=C.QUERY).next_to(hb2, DOWN, buff=0.08)
        h_l = label(r"one head's 192 query--key dimensions", font_size=24, color=GREY_A).next_to(head, UP, buff=0.12)
        with self.voiceover(
            "MiMo shrinks the cache in a second way, too, called grouped-query attention. <bookmark mark='q'/> It has 128 "
            "query heads, <bookmark mark='k'/> but they share just 8 sets of cached keys and values: <bookmark mark='g'/> "
            "sixteen heads read from each one. <bookmark mark='r'/> And within each head, only the first 64 of the 192 "
            "query and key dimensions are rotated to encode position. The rest match on content alone. The global layers "
            "rotate slowly, suited to distances of up to a million tokens, and the local layers rotate fast."
        ) as vo:
            vo.wait_until("q")
            self.play(FadeIn(qs, lag_ratio=0.005), FadeIn(q_l), run_time=1.2)
            vo.wait_until("k")
            self.play(FadeIn(kvs), FadeIn(kv_l))
            vo.wait_until("g")
            self.play(*[g.animate.shift(RIGHT * 0.05 * (i % 2)) for i, g in enumerate(groups)], Create(lines), FadeIn(g_l))
            vo.wait_until("r")
            self.play(FadeIn(head, lag_ratio=0.002), FadeIn(h_l))
            self.play(GrowFromCenter(hb1), GrowFromCenter(hb2), FadeIn(ht1), FadeIn(ht2))
        self.clear_scene()
