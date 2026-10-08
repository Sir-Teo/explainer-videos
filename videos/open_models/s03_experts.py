from __future__ import annotations


from explainer import *  # noqa: F403
from videos.open_models.common import (
    KEYS, MCOLOR, NAMES, bar_row, block, cfg, expert_grid, label, model, note, pick_active, random_values,
    show_chapter_card, vector_strip,
)
from videos.open_models.toys import expert_combinations

GRIDS = {"mimo": (16, 24), "glm": (16, 16), "kimi": (28, 32)}


class Experts(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 2, "Mixture of experts")
        self.idea()
        self.three_grids()
        self.whole_model()
        self.combinations()

    # ------------------------------------------------------------------
    def idea(self):
        dense = Rectangle(width=4.8, height=3.2, stroke_color=C.MLP, stroke_width=3, fill_color=C.MLP, fill_opacity=0.5)
        dense.move_to(RIGHT * 1.3)
        d_l = label(r"one big feed-forward network", font_size=28, color=C.MLP).next_to(dense, UP, buff=0.2)
        rows, cols = 6, 8
        cw, ch = 4.8 / cols, 3.2 / rows
        pieces = VGroup(*[Rectangle(width=cw * 0.82, height=ch * 0.8, stroke_color=C.EXPERT, stroke_width=1.5,
                                    fill_color=C.EXPERT, fill_opacity=0.18) for _ in range(rows * cols)])
        pieces.arrange_in_grid(rows, cols, buff=(cw * 0.18, ch * 0.2)).move_to(dense)
        p_l = label(r"48 small experts (in real models: hundreds)", font_size=28, color=C.EXPERT).next_to(dense, UP, buff=0.2)
        x = vector_strip(random_values(8, seed=3), cell=0.2).move_to(LEFT * 5.2)
        x_l = label(r"token", font_size=26, color=C.EMBED).next_to(x, UP, buff=0.15)
        router = block("router", C.ROUTER, width=1.5, height=0.7, font_size=28).move_to(LEFT * 3.1)
        chosen = [5, 18, 27, 44]
        w = [0.38, 0.27, 0.21, 0.14]
        arrows = VGroup(*[Arrow(router.get_right(), pieces[i].get_left(), buff=0.08, color=C.ROUTER, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.08) for i in chosen])
        wl = VGroup(*[MathTex(f"{v:.2f}", font_size=24, color=C.ROUTER).move_to(a.point_from_proportion(0.55) + UP * 0.18)
                      for v, a in zip(w, arrows)])
        out = vector_strip(random_values(8, seed=9), cell=0.2, color=C.EXPERT).move_to(RIGHT * 5.4)
        out_l = label(r"weighted sum", font_size=26, color=C.EXPERT).next_to(out, UP, buff=0.15)
        merge = VGroup(*[Arrow(pieces[i].get_right(), out.get_left(), buff=0.08, color=C.EXPERT, stroke_width=2,
                               max_tip_length_to_length_ratio=0.06) for i in chosen])

        with self.voiceover(
            "Here's the idea behind a mixture of experts. Take the big feed-forward network inside one layer, "
            "<bookmark mark='s'/> and split it into many small ones, called experts. <bookmark mark='r'/> Then add a small "
            "router, which looks at each token and picks just a few experts for it. <bookmark mark='o'/> Only those experts "
            "run. Their outputs are blended, with weights from the router, and added back into the token's vector. "
            "<bookmark mark='i'/> The other experts sit idle, for this token."
        ) as vo:
            self.play(FadeIn(dense), FadeIn(d_l))
            vo.wait_until("s")
            self.play(ReplacementTransform(dense, pieces), ReplacementTransform(d_l, p_l), run_time=1.5)
            vo.wait_until("r")
            x_arrow = Arrow(x.get_right(), router.get_left(), buff=0.12, color=C.EMBED, stroke_width=3)
            self.play(FadeIn(x), FadeIn(x_l))
            self.play(GrowArrow(x_arrow), FadeIn(router))
            self.play(Indicate(router, color=C.ROUTER))
            vo.wait_until("o")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), FadeIn(wl),
                      *[pieces[i].animate.set_fill(C.EXPERT, opacity=0.95) for i in chosen])
            self.play(LaggedStart(*[GrowArrow(a) for a in merge], lag_ratio=0.1), FadeIn(out), FadeIn(out_l))
            vo.wait_until("i")
            self.play(*[p.animate.set_stroke(opacity=0.35) for j, p in enumerate(pieces) if j not in chosen], run_time=0.8)

        why = VGroup(
            label(r"parameters (what the model can store): \textbf{all} the experts", font_size=30, color=C.EXPERT),
            label(r"compute per token: only the \textbf{few} experts it uses", font_size=30, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "This breaks the link between the two halves of the first bill. <bookmark mark='p'/> The model's capacity to "
            "store knowledge grows with all of its experts, <bookmark mark='c'/> while the compute for each token depends "
            "only on the few experts that actually run."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(why[0], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(why[1], shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def three_grids(self):
        c = {k: cfg(k) for k in KEYS}
        for k in KEYS:
            r, cc = GRIDS[k]
            assert r * cc == c[k]["experts"]
        assert [c[k]["experts_per_token"] for k in KEYS] == [8, 8, 16]
        assert [c[k]["shared_experts"] for k in KEYS] == [0, 1, 2]
        cell = {"mimo": 0.14, "glm": 0.14, "kimi": 0.095}
        cols = VGroup()
        grids = {}
        for k in KEYS:
            r, cc = GRIDS[k]
            act = pick_active(c[k]["experts"], c[k]["experts_per_token"], seed=len(k))
            g = expert_grid(r, cc, active=act, shared=c[k]["shared_experts"], cell=cell[k], gap=0.035,
                            active_color=YELLOW)
            grids[k] = g
            name = label(NAMES[k], font_size=32, color=MCOLOR[k])
            num = label(rf"{c[k]['experts']} experts, {c[k]['experts_per_token']} per token", font_size=26)
            sh = c[k]["shared_experts"]
            shl = label(rf"+ {sh} shared expert{'s' if sh > 1 else ''}, always on" if sh else r"no shared expert",
                        font_size=24, color=C.SHARED_EXPERT if sh else GREY_B)
            col = VGroup(name, g, num, shl).arrange(DOWN, buff=0.2)
            cols.add(col)
        cols.arrange(RIGHT, buff=0.55, aligned_edge=UP).move_to(DOWN * 0.1)
        for col in cols:
            col[0].align_to(cols, UP)
        per_layer = note(r"one mixture-of-experts layer of each model (which experts light up is illustrative)")
        per_layer.to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Here are the real numbers. <bookmark mark='m'/> In each expert layer, MiMo has 384 experts, and every token "
            "uses 8 of them. <bookmark mark='g'/> GLM has 256, and also uses 8, plus one shared expert that every token "
            "passes through. <bookmark mark='k'/> And Kimi K3 has 896 experts, uses 16 of them, plus two shared experts. "
            "<bookmark mark='l'/> Nearly every layer of each model has a block like this."
        ) as vo:
            for i, mk in enumerate("mgk"):
                vo.wait_until(mk)
                col = cols[i]
                self.play(FadeIn(col[0]), FadeIn(col[1][0], lag_ratio=0.002), run_time=1.2)
                self.play(FadeIn(col[2]), FadeIn(col[3]), *[FadeIn(s, scale=1.3) for s in col[1].shared], run_time=0.8)
            vo.wait_until("l")
            self.play(FadeIn(per_layer))
        self.clear_scene()

    # ------------------------------------------------------------------
    def whole_model(self):
        cats = {k: model(k)["params"]["by_category"] for k in KEYS}
        tot = {k: model(k)["params"]["total"] for k in KEYS}
        frac = {k: cats[k]["routed_experts"] / tot[k] for k in KEYS}
        assert [round(100 * frac[k]) for k in KEYS] == [98, 96, 98]
        order = [("routed_experts", r"routed experts", C.EXPERT),
                 ("shared_experts", r"shared experts", C.SHARED_EXPERT),
                 ("attention", r"attention", C.ATTN),
                 ("rest", r"everything else", GREY_B)]
        rows = VGroup()
        for k in KEYS:
            vals = []
            for key, _, _ in order[:-1]:
                vals.append(cats[k].get(key, 0))
            vals.append(tot[k] - sum(vals))
            bar = bar_row(vals, 9.5, 0.55, [o[2] for o in order])
            name = label(NAMES[k], font_size=30, color=MCOLOR[k])
            name.next_to(bar, LEFT, buff=0.3)
            pct = label(rf"{100 * frac[k]:.0f}\% experts", font_size=28, color=C.EXPERT).next_to(bar, RIGHT, buff=0.25)
            rows.add(VGroup(name, bar, pct))
        rows.arrange(DOWN, buff=0.55)
        for r in rows:
            r[1].align_to(rows[0][1], LEFT)
            r[0].next_to(r[1], LEFT, buff=0.3)
            r[2].next_to(r[1], RIGHT, buff=0.25)
        rows.move_to(UP * 0.3)
        leg = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.85), label(t, font_size=24, color=c))
                       .arrange(RIGHT, buff=0.1) for _, t, c in order]).arrange(RIGHT, buff=0.45).next_to(rows, DOWN, buff=0.5)
        title = label(r"Where the parameters are", font_size=36).to_edge(UP, buff=0.4)
        src = note(r"every tensor in the published weight files, classified by name and counted from its shape")
        src.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Now let's count every parameter in each model, using the shapes of all the tensors in the published weight "
            "files. <bookmark mark='b'/> The routed experts are almost the entire model: 98 percent of MiMo, 96 percent "
            "of GLM, and 98 percent of Kimi K3. <bookmark mark='a'/> Attention, the embeddings, the router, the shared "
            "experts: all of it is a thin shell around a vast library of experts."
        ) as vo:
            self.play(FadeIn(title), FadeIn(src))
            vo.wait_until("b")
            for r in rows:
                self.play(FadeIn(r[0]), LaggedStart(*[GrowFromEdge(s, LEFT) for s in r[1]], lag_ratio=0.3), run_time=1.0)
                self.play(FadeIn(r[2]), run_time=0.4)
            vo.wait_until("a")
            self.play(FadeIn(leg))
        self.clear_scene()

    # ------------------------------------------------------------------
    def combinations(self):
        combos = expert_combinations()
        assert 1e16 <= combos["mimo"] < 1.2e16
        few = expert_grid(2, 4, active=[1, 6], cell=0.55, gap=0.15, active_color=YELLOW)
        few_l = label(r"8 big experts, pick 2:\ \ 28 possible teams", font_size=30).next_to(few, DOWN, buff=0.3)
        many = expert_grid(16, 24, active=pick_active(384, 8, 5), cell=0.14, gap=0.035, active_color=YELLOW)
        many_l = label(r"384 small experts, pick 8:", font_size=30).next_to(many, DOWN, buff=0.3)
        num = MathTex(r"\binom{384}{8} \approx 1.1 \times 10^{16}", font_size=40, color=YELLOW).next_to(many_l, DOWN, 0.2)
        VGroup(VGroup(few, few_l), VGroup(many, many_l, num)).arrange(RIGHT, buff=1.4).move_to(UP * 0.2)
        num.next_to(many_l, DOWN, buff=0.2)
        sh_note = label(r"shared experts (GLM, Kimi): what every token needs, so routed experts can specialize",
                        font_size=26, color=C.SHARED_EXPERT).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why so many small experts, instead of a few big ones? <bookmark mark='f'/> Because what matters is the "
            "combination. With 8 big experts and 2 picks, there are only 28 possible teams. <bookmark mark='m'/> With "
            "8 picks out of 384, there are about ten quadrillion. Small, specialized experts can be mixed and matched "
            "far more flexibly. <bookmark mark='s'/> The shared experts in GLM and Kimi play the opposite role: they "
            "handle whatever every token needs, so the routed experts are free to specialize."
        ) as vo:
            vo.wait_until("f")
            self.play(FadeIn(few), FadeIn(few_l))
            vo.wait_until("m")
            self.play(FadeIn(many, lag_ratio=0.002), FadeIn(many_l), run_time=1.2)
            self.play(Write(num))
            vo.wait_until("s")
            self.play(FadeIn(sh_note, shift=UP * 0.2))
        self.clear_scene()
