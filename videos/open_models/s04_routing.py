from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.open_models.common import (
    KEYS, MCOLOR, NAMES, Plot, block, cfg, label, model, note, random_values, schematic_tag, show_chapter_card,
    toy_tag, vector_strip,
)
from videos.open_models.toys import balancing_demo, expert_vectors, route, sigmoid, synthetic_batch

LOGITS = np.array([1.2, -0.4, 2.1, 0.3, -1.0, 0.8, 1.7, -0.2])


class Routing(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 3, "Routing, and keeping the experts busy")
        self.router()
        self.imbalance()
        self.bias_trick()
        self.real_biases()
        self.quantile()

    # ------------------------------------------------------------------
    def router(self):
        n = len(LOGITS)
        x = vector_strip(random_values(10, seed=4), cell=0.2).move_to(LEFT * 5.6 + DOWN * 0.2)
        x_l = MathTex(r"\vec x", font_size=40, color=C.EMBED).next_to(x, UP, buff=0.15)
        experts = VGroup(*[vector_strip(random_values(10, seed=20 + i), cell=0.13, color=C.EXPERT, direction=RIGHT)
                           for i in range(n)]).arrange(DOWN, buff=0.17).move_to(LEFT * 2.6 + DOWN * 0.2)
        e_l = VGroup(*[MathTex(rf"\vec e_{{{i + 1}}}", font_size=28, color=C.EXPERT).next_to(e, LEFT, buff=0.15)
                       for i, e in enumerate(experts)])
        e_title = label(r"one learned vector per expert", font_size=24, color=C.EXPERT).next_to(experts, UP, buff=0.25)
        s = sigmoid(LOGITS)
        k = 2
        top = np.argsort(-s)[:k]
        pl = Plot((0, 1.05), (0, n), width=3.2, height=experts.height + 0.3, x_ticks=[0, 0.5, 1], x_fmt=lambda v: f"{v:g}")
        pl.move_to(RIGHT * 0.6 + DOWN * 0.2, aligned_edge=LEFT)
        pl.shift(UP * (experts.get_bottom()[1] - 0.3 - pl.x_axis.get_start()[1]))
        bars = VGroup()
        for i, v in enumerate(s):
            y = experts[i].get_y()
            b = Rectangle(width=3.2 * v / 1.05, height=0.28, stroke_width=0, fill_color=C.ROUTER, fill_opacity=0.35)
            b.move_to([pl.x_axis.get_start()[0], y, 0], aligned_edge=LEFT)
            bars.add(b)
        vals = VGroup(*[DecimalNumber(v, num_decimal_places=2, font_size=24, color=GREY_A).next_to(b, RIGHT, buff=0.1)
                        for v, b in zip(s, bars)])
        f1 = MathTex(r"s_i", "=", r"\sigma", r"(\vec e_i \cdot \vec x)", font_size=40).to_edge(UP, buff=0.4).shift(RIGHT * 1.6)
        f1[0].set_color(C.ROUTER)
        sig_note = label(r"$\sigma$: the sigmoid, squashes any number into $(0,1)$", font_size=24, color=GREY_A)
        sig_note.next_to(f1, DOWN, buff=0.12)
        w = s[top] / s[top].sum()
        f2 = MathTex(r"\text{weight}_i", "=", r"{s_i \over \sum_{j\in\text{top}} s_j}", font_size=36)
        f2.to_corner(DR, buff=0.4).shift(UP * 0.9)
        w_l = VGroup(*[MathTex(f"{v:.2f}", font_size=28, color=YELLOW).next_to(vals[i], RIGHT, buff=0.35)
                       for v, i in zip(w, top)])
        w_head = label(r"weights", font_size=24, color=YELLOW).next_to(w_l, UP, buff=0.3).align_to(w_l, LEFT)
        w_head.set_y(e_title.get_y())
        with self.voiceover(
            "How does the router choose? <bookmark mark='e'/> Each expert has a learned vector, a bit like a key. "
            "<bookmark mark='d'/> The router takes the dot product of the token's vector with every expert's vector, "
            "<bookmark mark='s'/> and squashes each result into a score between zero and one, with a sigmoid. "
            "<bookmark mark='k'/> The top scores win: here two out of eight, in MiMo eight out of 384. "
            "<bookmark mark='w'/> Their scores, rescaled to add up to one, become the blending weights. All three "
            "models use this same recipe."
        ) as vo:
            self.play(FadeIn(x), FadeIn(x_l))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(e, shift=LEFT * 0.1) for e in experts], lag_ratio=0.08), FadeIn(e_l),
                      FadeIn(e_title))
            vo.wait_until("d")
            self.play(Write(f1), Indicate(x, color=C.EMBED, scale_factor=1.05),
                      Indicate(experts, color=C.EXPERT, scale_factor=1.03), run_time=1.0)
            self.play(Create(pl), FadeIn(sig_note), run_time=0.8)
            vo.wait_until("s")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.08), FadeIn(vals), run_time=1.5)
            vo.wait_until("k")
            self.play(*[bars[i].animate.set_fill(opacity=0.95) for i in top],
                      *[experts[i].animate.set_opacity(0.3) for i in range(n) if i not in top],
                      *[vals[i].animate.set_color(YELLOW) for i in top])
            vo.wait_until("w")
            self.play(Write(f2), FadeIn(w_l), FadeIn(w_head))
        self.clear_scene()

    # ------------------------------------------------------------------
    def imbalance(self):
        n = 16
        E, pop = expert_vectors(n)
        s = synthetic_batch(8192, E, pop, seed=1)
        _, loads = route(s, np.zeros(n), 2)
        target = 8192 * 2 / n
        pl = Plot((0, n), (0, 2.6), width=6.4, height=3.6, y_ticks=[0, 1, 2], y_fmt=lambda v: f"{v:g}\\times")
        pl.move_to(LEFT * 2.8 + DOWN * 0.3)
        fair = DashedLine(pl.c2p(0, 1), pl.c2p(n, 1), color=WHITE, stroke_width=2)
        fair_l = label(r"fair share", font_size=24).next_to(fair, RIGHT, buff=0.1)
        even = pl.bars(np.arange(n) + 0.5, np.ones(n), 0.32, C.BALANCE)
        skew = pl.bars(np.arange(n) + 0.5, loads / target, 0.32, C.BALANCE)
        yl = label(r"tokens sent to each expert", font_size=26, color=C.BALANCE).next_to(pl, UP, buff=0.15).align_to(pl, LEFT)
        loop = VGroup(label(r"chosen more", font_size=26), label(r"$\Rightarrow$ trained more", font_size=26),
                      label(r"$\Rightarrow$ better", font_size=26), label(r"$\Rightarrow$ chosen even more", font_size=26))
        loop.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.5).shift(UP * 1.4)
        gpus = VGroup()
        per = loads.reshape(4, 4).sum(1) / (4 * target)
        for i, f in enumerate(per):
            box = RoundedRectangle(width=0.9, height=1.4, corner_radius=0.08, stroke_color=GREY_B, stroke_width=2)
            fill = Rectangle(width=0.7, height=1.2 * min(f, 2.0) / 2.0, stroke_width=0, fill_color=C.BALANCE, fill_opacity=0.9)
            fill.move_to(box.get_bottom() + UP * 0.1, aligned_edge=DOWN)
            gpus.add(VGroup(box, fill, label(rf"GPU {i + 1}", font_size=20, color=GREY_A).next_to(box, DOWN, buff=0.08)))
        gpus.arrange(RIGHT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.9)
        g_l = label(r"experts live on different GPUs", font_size=24, color=GREY_A).next_to(gpus, UP, buff=0.15)
        tag = toy_tag(r"toy router: 16 experts, random tokens")
        with self.voiceover(
            "But left alone, this goes wrong in a predictable way. <bookmark mark='r'/> An expert that gets chosen a lot "
            "gets more training, so it gets better, so it gets chosen even more. <bookmark mark='l'/> A few experts end up "
            "overloaded, and others are starved, and never learn much of anything. <bookmark mark='g'/> And since the "
            "experts are spread across many GPUs, an overloaded expert means one GPU working flat out while the others "
            "wait."
        ) as vo:
            self.play(Create(pl), FadeIn(yl), Create(fair), FadeIn(fair_l), FadeIn(even), FadeIn(tag))
            vo.wait_until("r")
            self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in loop], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("l")
            self.play(Transform(even, skew), run_time=2)
            vo.wait_until("g")
            self.play(FadeIn(gpus), FadeIn(g_l))
        self.clear_scene()

    # ------------------------------------------------------------------
    def bias_trick(self):
        s = np.array([0.82, 0.78, 0.74, 0.62, 0.58, 0.55])
        b = np.array([-0.30, 0.0, -0.10, 0.0, 0.22, 0.05])
        n = len(s)
        pl = Plot((0, n), (0, 1.0), width=6.0, height=3.4, y_ticks=[0, 0.5, 1]).move_to(LEFT * 2.6 + DOWN * 0.6)
        xs = np.arange(n) + 0.5
        sb = pl.bars(xs, s, 0.5, C.ROUTER)
        lbls = VGroup(*[MathTex(rf"e_{{{i + 1}}}", font_size=26, color=C.EXPERT).next_to(pl.c2p(x, 0), DOWN, 0.12)
                        for i, x in enumerate(xs)])
        top_before = set(np.argsort(-s)[:2].tolist())
        top_after = set(np.argsort(-(s + b))[:2].tolist())
        assert top_before == {0, 1} and top_after == {1, 4}
        bias = VGroup()
        for i, x in enumerate(xs):
            lo, hi = sorted([s[i], s[i] + b[i]])
            r = Rectangle(width=0.5, height=max(1e-3, pl.c2p(0, hi)[1] - pl.c2p(0, lo)[1]), stroke_color=C.BALANCE,
                          stroke_width=2, fill_color=C.BALANCE, fill_opacity=0.25 if b[i] > 0 else 0.0)
            r.move_to(pl.c2p(x, (lo + hi) / 2))
            if b[i] < 0:
                r.set_stroke(C.BALANCE, 2).set_fill(BACKGROUND, 0.6)
            bias.add(r)
        crowns = lambda idx, col: VGroup(*[Star(n=5, outer_radius=0.13, color=col, fill_opacity=1).next_to(
            pl.c2p(xs[i], max(s[i], s[i] + b[i] if col == C.BALANCE else s[i])), UP, buff=0.12) for i in idx])
        cr1 = crowns(sorted(top_before), C.ROUTER)
        cr2 = crowns(sorted(top_after), C.BALANCE)
        f = VGroup(
            MathTex(r"\text{choose: top-}k \text{ of }", r"s_i", "+", r"b_i", font_size=36),
            MathTex(r"\text{blend with: }", r"s_i", r"\text{ only}", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6).shift(UP * 0.9)
        f[0][1].set_color(C.ROUTER)
        f[0][3].set_color(C.BALANCE)
        f[1][1].set_color(C.ROUTER)
        rule = VGroup(label(r"expert overloaded $\Rightarrow$ lower its bias", font_size=26, color=C.BALANCE),
                      label(r"expert underused $\Rightarrow$ raise its bias", font_size=26, color=C.BALANCE))
        rule.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(f, DOWN, buff=0.5).align_to(f, LEFT)
        leg = VGroup(VGroup(Square(0.22, stroke_width=0, fill_color=C.ROUTER, fill_opacity=0.85),
                            label(r"router score $s_i$", font_size=24, color=C.ROUTER)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.22, stroke_color=C.BALANCE, stroke_width=2, fill_color=C.BALANCE, fill_opacity=0.25),
                            label(r"bias $b_i$ (up or down)", font_size=24, color=C.BALANCE)).arrange(RIGHT, buff=0.1),
                     VGroup(Star(n=5, outer_radius=0.12, color=C.BALANCE, fill_opacity=1),
                            label(r"chosen", font_size=24)).arrange(RIGHT, buff=0.1))
        leg.arrange(RIGHT, buff=0.4).next_to(pl, UP, buff=0.35).align_to(pl, LEFT)
        old = label(r"old fix: a penalty in the loss for imbalance (fights the real objective)", font_size=26,
                    color=GREY_B).to_edge(UP, buff=0.45)
        src = note(r"auxiliary-loss-free balancing: DeepSeek-V3 (2024); used by all three models").to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The classic fix was an extra penalty in the training loss for imbalance, <bookmark mark='t'/> but that "
            "penalty fights against the real goal, predicting text well. <bookmark mark='b'/> All three models instead "
            "use a trick introduced by DeepSeek: give each expert a bias, a kind of handicap, that is added to its score "
            "only when choosing the winners, <bookmark mark='n'/> not when blending their outputs. <bookmark mark='u'/> "
            "If an expert is overloaded, lower its bias; if it's underused, raise it. <bookmark mark='f'/> The router "
            "learns freely; the biases just keep the traffic fair."
        ) as vo:
            self.play(FadeIn(old))
            vo.wait_until("t")
            self.play(old.animate.set_opacity(0.5))
            self.play(Create(pl), FadeIn(sb), FadeIn(lbls), FadeIn(cr1))
            vo.wait_until("b")
            self.play(Write(f[0]), LaggedStart(*[FadeIn(r) for r in bias], lag_ratio=0.1), FadeIn(src), FadeIn(leg))
            self.play(ReplacementTransform(cr1, cr2))
            vo.wait_until("n")
            self.play(Write(f[1]))
            vo.wait_until("u")
            self.play(FadeIn(rule[0]), Indicate(bias[0], color=C.BALANCE))
            self.play(FadeIn(rule[1]), Indicate(bias[4], color=C.BALANCE))
        self.clear_scene()

    # ------------------------------------------------------------------
    def real_biases(self):
        plots = VGroup()
        for k in KEYS:
            rb = model(k)["router_bias"]
            v = np.sort(np.array(rb["example"]))[::-1]
            lo, hi = float(v.min()), float(v.max())
            pad = 0.08 * (hi - lo)
            pl = Plot((0, len(v)), (lo - pad, hi + pad), width=3.0, height=2.6,
                      y_ticks=[round(lo, 2), round(hi, 2)], y_fmt=lambda t: f"{t:+.2f}" if abs(t) < 5 else f"{t:.2f}",
                      font_size=22)
            bars = VGroup()
            base = lo - pad
            for i, val in enumerate(v):
                top, bot = pl.c2p(i + 0.5, val), pl.c2p(i + 0.5, base)
                bars.add(Line(bot, top, stroke_width=max(0.6, 2.8 * 96 / len(v)), color=C.BALANCE))
            name = label(NAMES[k], font_size=28, color=MCOLOR[k]).next_to(pl, UP, buff=0.35)
            sub = label(rf"layer {rb['example_layer'] + 1}: {len(v)} experts, sorted", font_size=22, color=GREY_A)
            sub.next_to(name, DOWN, buff=0.08)
            plots.add(VGroup(name, sub, pl, bars))
        plots.arrange(RIGHT, buff=1.25).move_to(DOWN * 0.2)
        if plots.width > 13.4:
            plots.width = 13.4
        title = label(r"Real learned balancing biases, read from the weights", font_size=34).to_edge(UP, buff=0.35)
        glm = model("glm")["router_bias"]["example"]
        assert 7.5 < min(glm) and max(glm) < 8.5
        off = label(r"GLM's sit near $+8$: adding the same number to every score never changes the winners",
                    font_size=26, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "These are the actual balancing biases of one layer in each model, read straight from the weight files, "
            "<bookmark mark='m'/> MiMo's 384, <bookmark mark='g'/> GLM's 256, <bookmark mark='k'/> and Kimi's 896, sorted "
            "from largest to smallest. Each one records how much the balancing had to boost or hold back one expert. "
            "<bookmark mark='o'/> Notice that GLM's are all around eight. That's fine: only the differences between "
            "experts matter, since adding the same number to every score never changes which ones come out on top."
        ) as vo:
            self.play(FadeIn(title))
            for i, mk in enumerate("mgk"):
                vo.wait_until(mk)
                p = plots[i]
                self.play(FadeIn(p[0]), FadeIn(p[1]), Create(p[2]), Create(p[3], lag_ratio=0.002), run_time=1.2)
            vo.wait_until("o")
            self.play(FadeIn(off, shift=UP * 0.2), Indicate(plots[1][2].y_labels, color=YELLOW))
        self.clear_scene()

    # ------------------------------------------------------------------
    def quantile(self):
        assert cfg("kimi")["experts"] == 896 and cfg("kimi")["experts_per_token"] == 16
        tag = label(r"Kimi K3: Quantile Balancing", font_size=34, color=C.KIMI).to_edge(UP, buff=0.35)
        rng = np.random.default_rng(7)
        m, q = 24, 6
        margins = np.sort(rng.normal(-0.25, 0.3, m))[::-1]
        nl = NumberLine(x_range=[-1.2, 0.8, 0.4], length=7.5, include_numbers=True, font_size=22,
                        decimal_number_config={"num_decimal_places": 1}).move_to(UP * 0.6)
        nl_l = label(r"for one expert: each token's score, minus what it would take to make that token's top 16",
                     font_size=24, color=GREY_A).next_to(nl, DOWN, buff=0.55)
        ys = np.tile([0.25, 0.5, 0.75], m)[:m]
        dots = VGroup(*[Dot(nl.n2p(v) + UP * y, radius=0.08, color=C.ROUTER) for v, y in zip(margins, ys)])
        thr = (margins[q - 1] + margins[q]) / 2
        cut = DashedLine(nl.n2p(thr) + DOWN * 0.15, nl.n2p(thr) + UP * 1.2, color=C.BALANCE, stroke_width=3)
        cut_l = label(rf"set the bias here: exactly {q} tokens get through", font_size=24, color=C.BALANCE)
        cut_l.next_to(cut, UP, buff=0.1)
        demo = balancing_demo()
        imb_s, imb_q = demo["imbalance_sign"], demo["imbalance_qb"]
        assert imb_q[1] < 1.35 and imb_s[1] > 1.9 and imb_s[0] == imb_q[0]
        steps = np.arange(len(imb_s))
        pl = Plot((0, len(imb_s) - 1), (1.0, 2.5), width=6.0, height=2.6, x_ticks=[0, 5, 10, 15],
                  y_ticks=[1, 1.5, 2, 2.5], y_fmt=lambda v: f"{v:g}\\times", font_size=22).to_edge(DOWN, buff=0.75)
        pl.shift(LEFT * 1.0)
        l_s = pl.line(steps, imb_s, GREY_B, 3)
        l_q = pl.line(steps, imb_q, C.BALANCE, 4)
        yl = label(r"busiest expert vs.\ fair share", font_size=22, color=GREY_A).next_to(pl, UP, 0.1).align_to(pl, LEFT)
        xl = label(r"training step", font_size=22, color=GREY_A).next_to(pl, DOWN, buff=0.4)
        lg = VGroup(label(r"fixed nudges", font_size=24, color=GREY_B),
                    label(r"quantile rule", font_size=24, color=C.BALANCE)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        lg.next_to(pl, RIGHT, buff=0.4)
        tt = toy_tag(r"toy: 16 experts, 8{,}192 random tokens per step", corner=UR)
        with self.voiceover(
            "Kimi K3 sharpens this. With 896 experts, small fixed nudges are too slow, and big ones overshoot. "
            "<bookmark mark='q'/> So instead of nudging, its Quantile Balancing computes, from a single batch, the bias "
            "that would give each expert exactly its fair share. <bookmark mark='m'/> Take one expert, and for every token "
            "in the batch, measure how far that token's score for this expert is from the cutoff it would need to make "
            "the token's top sixteen. <bookmark mark='c'/> Then put the bias at the point where exactly the fair number of "
            "tokens get through: a quantile."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("m")
            self.play(Create(nl), FadeIn(nl_l), LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.04))
            vo.wait_until("c")
            self.play(Create(cut), FadeIn(cut_l))
            self.play(*[dots[i].animate.set_color(YELLOW).scale(1.3) for i in range(q)],
                      *[dots[i].animate.set_opacity(0.35) for i in range(q, m)])
        with self.voiceover(
            "Here's a toy run with 16 experts, on random tokens. <bookmark mark='s'/> With fixed nudges, the busiest "
            "expert starts at more than twice its fair share, and it takes about ten steps to come down. "
            "<bookmark mark='g'/> The quantile rule gets most of the way in a single step."
        ) as vo:
            self.play(VGroup(nl, nl_l, dots, cut, cut_l).animate.scale(0.75).shift(UP * 0.85), run_time=0.8)
            self.play(Create(pl), FadeIn(yl), FadeIn(xl), FadeIn(tt))
            vo.wait_until("s")
            self.play(Create(l_s), FadeIn(lg[0]), run_time=2.0)
            vo.wait_until("g")
            self.play(Create(l_q), FadeIn(lg[1]), run_time=2.0)
        self.clear_scene()
