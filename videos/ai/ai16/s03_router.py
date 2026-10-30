from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import EXPERT_COLORS, EXPERTC, GRADC, PART, ROUTER, load, take_away


class Router(VoiceoverScene):
    def construct(self):
        self.card()
        self.mechanism()
        self.derive()
        self.check()
        self.top1()

    def card(self):
        card = chapter_card(2, r"Top-$k$ gates and the router's gradient", r"What does a router learn from?", part=PART)
        with self.voiceover("Chapter two. Top-k gates, and the router's gradient."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def mechanism(self):
        E, k = 8, 2
        x = VGroup(*[Square(0.24, stroke_width=0.6, stroke_color=GREY_D, fill_color=C.EMBED, fill_opacity=o)
                     for o in (0.3, 0.8, 0.5, 0.2, 0.7, 0.4)]).arrange(DOWN, buff=0).move_to([-5.6, 0.3, 0])
        xl = MathTex(r"x", font_size=34, color=C.EMBED).next_to(x, UP, buff=0.15)
        router = RoundedRectangle(width=1.3, height=0.8, corner_radius=0.12, stroke_color=ROUTER, stroke_width=3).move_to([-3.6, 0.3, 0])
        rl = label(r"router", font_size=24, color=ROUTER).move_to(router)
        logits = np.array([0.4, 2.1, -0.3, 0.9, 1.7, -0.8, 0.1, 0.5])
        probs = np.exp(logits) / np.exp(logits).sum()
        top = np.argsort(-logits)[:k]
        bars = VGroup()
        for i, p in enumerate(probs):
            b = Rectangle(width=0.32, height=max(2.6 * p, 0.03), stroke_width=0, fill_color=ROUTER, fill_opacity=0.85)
            b.move_to([-1.9 + 0.42 * i, -0.9 + 1.3 * p, 0])
            bars.add(b)
        bl = label(r"scores $s_i$, \ softmax over the experts", font_size=20, color=GREY_A).next_to(bars, DOWN, buff=0.2)
        experts = VGroup(*[RoundedRectangle(width=0.9, height=0.55, corner_radius=0.1, stroke_color=EXPERT_COLORS[i],
                                            stroke_width=2).move_to([2.4, 2.75 - 0.7 * i, 0]) for i in range(E)])
        el = VGroup(*[MathTex(rf"E_{i + 1}", font_size=24, color=EXPERT_COLORS[i]).move_to(e_) for i, e_ in enumerate(experts)])
        arrows = VGroup(*[Arrow(router.get_right(), experts[i].get_left(), buff=0.1, color=ROUTER, stroke_width=3) for i in top])
        out = MathTex(r"y", font_size=34, color=C.BITS).move_to([5.2, 0.3, 0])
        outs = VGroup(*[Arrow(experts[i].get_right(), out.get_left(), buff=0.1, color=EXPERT_COLORS[i], stroke_width=3) for i in top])
        colors = {r"g_i": ROUTER, r"E_i": EXPERTC}
        f = cmath(r"y", "=", r"\sum_{i \,\in\, \mathcal K}", r"g_i", r"\,", r"E_i", r"(x)", r",\qquad \mathcal K = \operatorname{top}_k(s)",
                  r",\qquad", r"g_i", r"= \frac{e^{s_i}}{\sum_{j \in \mathcal K} e^{s_j}}", colors=colors,
                  font_size=34).to_edge(DOWN, buff=0.4)
        tag = note(r"illustrative router scores").to_corner(UR, buff=0.3)
        cite_ = cite(r"Mixtral's gate: \ A.~Jiang et al.\ (2024)", corner=UL)
        with self.voiceover(
            "Here's one layer of a modern mixture of experts. The feed-forward network of each transformer block "
            "becomes several smaller ones, the experts. <bookmark mark='a'/> A router, just one matrix, gives the "
            "token a score against every expert. <bookmark mark='b'/> Only the top k scores count: here, two of eight. "
            "Those experts run; the others don't. <bookmark mark='c'/> Their outputs are added up, weighted by gates: "
            "a softmax over the chosen experts' scores alone, so the gates add to one. That's Mixtral's gate, and "
            "the one most models use."
        ) as vo:
            self.play(FadeIn(x), FadeIn(xl), FadeIn(experts), FadeIn(el), FadeIn(cite_), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(router), FadeIn(rl), GrowArrow(Arrow(x.get_right(), router.get_left(), buff=0.1, color=GREY_B)))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(bl))
            vo.wait_until("b")
            self.play(*[bars[i].animate.set_fill(EXPERT_COLORS[i]) for i in top],
                      *[bars[i].animate.set_fill(opacity=0.25) for i in range(E) if i not in top],
                      *[experts[i].animate.set_fill(EXPERT_COLORS[i], opacity=0.35) for i in top])
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in outs], lag_ratio=0.3), FadeIn(out), Write(f))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"g_j": ROUTER, r"g_i": ROUTER, r"u_j": EXPERTC, r"u_i": EXPERTC, r"\bar u": C.BITS}
        rows = [
            cmath(r"\frac{\partial L}{\partial s_j}", r"=", r"\sum_{i \in \mathcal K}", r"u_i", r"\,\frac{\partial", r"g_i",
                  r"}{\partial s_j}", r",\qquad", r"u_i", r"= \frac{\partial L}{\partial y}\cdot E_i(x)", colors=colors,
                  font_size=34),
            cmath(r"\frac{\partial", r"g_i", r"}{\partial s_j}", r"=", r"g_i", r"\,(\delta_{ij} -", r"g_j", r")",
                  r"\qquad i, j \in \mathcal K", colors=colors, font_size=34),
            cmath(r"\frac{\partial L}{\partial s_j}", r"=", r"g_j", r"\big(", r"u_j", r"-", r"\bar u", r"\big)",
                  r",\qquad", r"\bar u", r"= \sum_{i \in \mathcal K}", r"g_i", r"u_i", colors=colors, font_size=34),
            cmath(r"\frac{\partial L}{\partial s_j}", r"=", r"0", r"\qquad j \notin \mathcal K", font_size=34),
        ]
        whys = [why(r"chain rule \ ($y$ depends on $s$ only through the gates)"), why(r"the softmax's Jacobian \ (Part 4)"),
                why(r"collect terms"), why(r"an expert not chosen has no gate")]
        for r_ in rows:
            r_.scale(0.92)
        step = ladder(self, rows, whys, keep=4, top=3.25, x=-2.2, buff=0.36, edge=6.8)
        remind = cmath(r"y = \sum_{i\in\mathcal K}", r"g_i", r"\,E_i(x)", r",\quad", r"g_i", r"= \frac{e^{s_i}}{\sum_{j\in\mathcal K}"
                       r" e^{s_j}}", colors={r"g_i": ROUTER}, font_size=30).to_edge(DOWN, buff=0.6)
        rl_ = label(r"the layer, \ from the last scene", font_size=18, color=GREY_B).next_to(remind, UP, buff=0.12)
        meaning = VGroup(
            label(r"$u_j$: \ how much expert $j$'s answer would raise the loss", font_size=22, color=EXPERTC),
            label(r"$u_j < \bar u$: \ $j$ helped more than the average chosen expert: \ its score goes up", font_size=22,
                  color=C.BITS),
            label(r"the router learns only about the experts it tried", font_size=26, color=GRADC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)
        for m_ in meaning[:2]:
            m_.scale(0.9)
        with self.voiceover(
            "What does the router learn from? Take the gradient of the loss with respect to a score s j. "
            "<bookmark mark='a'/> The output depends on the scores only through the gates, so by the chain rule "
            "it's a sum over the chosen experts of u i, how much expert i's output pushes the loss, times the gate's "
            "derivative. <bookmark mark='b'/> The gates are a softmax, whose Jacobian is part four's g i times "
            "delta i j minus g j. <bookmark mark='c'/> Collect the terms: the gradient is g j times u j minus u bar, "
            "the gate-weighted average of the chosen experts. A chosen expert that helped more than the average "
            "gets its score raised; one that helped less gets it lowered. <bookmark mark='d'/> And an expert that "
            "wasn't chosen has no gate, so its score gets no gradient at all. <bookmark mark='e'/> The router only "
            "learns about the experts it tried. It never finds out whether an unchosen expert would have done better."
        ) as vo:
            self.play(FadeIn(remind), FadeIn(rl_))
            step(0)
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for i, mk in zip((1, 2, 3), "bcd"):
                vo.wait_until(mk)
                step(i)
            vo.wait_until("e")
            self.play(FadeOut(remind), FadeOut(rl_))
            self.play(LaggedStart(*[FadeIn(m_) for m_ in meaning], lag_ratio=0.5), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        d = load("gradcheck")
        r = d["softmax-k"]
        E = int(d["E"])
        auto, ana, fd = (np.asarray(r[k_], float) for k_ in ("auto", "analytic", "fd"))
        chosen = [int(c) for c in r["chosen"]]
        top = max(np.abs(fd).max(), 1e-9)
        ax = Axes(x_range=[-0.5, E - 0.5, 1], y_range=[-1.15, 1.15, 0.5], x_length=7.0, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-2.3, -0.3, 0])
        cols = [(fd, GREY_B, -0.22, r"finite differences"), (ana, C.BITS, 0.0, r"the formula"),
                (auto, GRADC, 0.22, r"automatic differentiation")]
        sets = VGroup()
        for vals, col, off, _ in cols:
            g = VGroup()
            for i, v in enumerate(vals):
                h = 1.6 * abs(v) / top
                b = Rectangle(width=0.2, height=max(h, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.9)
                b.move_to(ax.c2p(i + off, 0) + (UP if v >= 0 else DOWN) * max(h, 0.02) / 2)
                g.add(b)
            sets.add(g)
        xl = VGroup(*[MathTex(rf"s_{i + 1}", font_size=24, color=EXPERT_COLORS[i] if i in chosen else GREY_C)
                      .next_to(ax.c2p(i, -1.15), DOWN, buff=0.1) for i in range(E)])
        ch = VGroup(*[SurroundingRectangle(xl[i], color=ROUTER, buff=0.06) for i in chosen])
        key = VGroup(*[VGroup(Square(0.18, stroke_width=0, fill_color=c_, fill_opacity=0.9), label(t, font_size=20, color=c_))
                       .arrange(RIGHT, buff=0.12) for _, c_, _, t in cols]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        key.move_to([4.3, 1.6, 0])
        errs = VGroup(
            label(rf"largest relative gap: \ ${sci(r['err_analytic'])}$", font_size=22, color=C.BITS),
            label(rf"our MoE layer's router, \ every weight: \ ${sci(float(d['layer_err']))}$", font_size=22, color=GRADC),
            label(rf"nonzero: \ ${int(r['nonzero'])}$ of ${E}$ \ (the chosen)", font_size=22, color=ROUTER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.3, -0.8, 0])
        head = label(r"one token, \ $8$ experts, \ top $2$: \ $\partial L / \partial s$ three ways \ (float64)", font_size=26)
        head.to_edge(UP, buff=0.35)
        tag = note(r"computed", font_size=18).to_corner(DR, buff=0.25)
        p1 = int(-np.log10(max(r["err_analytic"], 1e-16)))
        p2 = int(-np.log10(max(float(d["layer_err"]), 1e-16)))
        with self.voiceover(
            "Let's check it. One token, eight experts that are random linear maps, the top two chosen, and a squared "
            "error. <bookmark mark='a'/> Nudge each score up and down by a millionth and watch the loss: that's the "
            "gradient by finite differences. <bookmark mark='b'/> The formula gives the same bars, and so does "
            f"automatic differentiation: they agree to {p1} decimal places, relative to the largest bar. "
            f"<bookmark mark='c'/> {E - int(r['nonzero'])} of the {E} bars are exactly zero: only the chosen experts' scores move. "
            "We ran the same check on the router of the mixture layer we'll train in the next chapter, every one of "
            f"its weights: they agree to {p2} decimal places."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(key[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if v >= 0 else UP) for b, v in zip(sets[0], fd)], lag_ratio=0.08))
            vo.wait_until("b")
            self.play(FadeIn(key[1]), LaggedStart(*[GrowFromEdge(b, DOWN if v >= 0 else UP) for b, v in zip(sets[1], ana)], lag_ratio=0.05))
            self.play(FadeIn(key[2]), LaggedStart(*[GrowFromEdge(b, DOWN if v >= 0 else UP) for b, v in zip(sets[2], auto)], lag_ratio=0.05),
                      FadeIn(errs[0]))
            vo.wait_until("c")
            self.play(Create(ch), FadeIn(errs[2]))
            self.play(FadeIn(errs[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def top1(self):
        d = load("gradcheck")
        kinds = [("softmax-k", r"softmax over the top $2$ \ (Mixtral)"), ("sigmoid-k", r"sigmoids over the top $2$ \ (DeepSeek-V3)"),
                 ("switch", r"top $1$, \ gate $= p_i$ \ (Switch)"), ("top1-renorm", r"top $1$, \ gate renormalized to $1$")]
        rows = VGroup()
        for kind, name in kinds:
            r = d[kind]
            n = int(r["nonzero"])
            cells = VGroup(*[Square(0.3, stroke_width=1, stroke_color=GREY_C,
                                    fill_color=GRADC if abs(float(v)) > 1e-9 else GREY_D,
                                    fill_opacity=0.85 if abs(float(v)) > 1e-9 else 0.15) for v in r["fd"]]).arrange(RIGHT, buff=0.06)
            rows.add(VGroup(label(name, font_size=22, color=GREY_A), cells,
                            label(rf"${n}$ of ${int(d['E'])}$ scores learn", font_size=22,
                                  color=GRADC if n else C.SURPRISE)))
        for r_ in rows:
            r_[0].move_to([-3.2, 0, 0], aligned_edge=RIGHT)
            r_[1].next_to([-3.0, 0, 0], RIGHT, buff=0)
            r_[2].next_to(r_[1], RIGHT, buff=0.35)
        rows.arrange(DOWN, buff=0.4).move_to([0.2, 0.2, 0])
        for r_ in rows:
            r_[0].align_to(rows[0][0], RIGHT)
            r_[1].align_to(rows[0][1], LEFT)
            r_[2].next_to(r_[1], RIGHT, buff=0.35)
        pc = pause_card(r"With one expert per token and its gate renormalized to $1$, \ what does the router learn?",
                        width=9.0, font_size=26).to_edge(UP, buff=0.3)
        head = label(r"which router scores get a gradient \ (computed)", font_size=24, color=GREY_A).next_to(rows, UP, buff=0.35)
        ta = take_away(r"a router learns only from the experts it tried: \ it needs noise to explore, \ and help to share",
                       color=ROUTER, font_size=24)
        cite_ = cite(r"W.~Fedus, B.~Zoph \& N.~Shazeer, \textit{Switch Transformers} (2021)", corner=DR)
        with self.voiceover(
            "Pause and predict. With one expert per token, and its gate renormalized to one, what does the router "
            "learn? <bookmark mark='a'/> Here are the four gates side by side. With two experts, mixed by a softmax "
            "or by DeepSeek's sigmoids, the two chosen scores learn. <bookmark mark='b'/> Switch's single expert is "
            "multiplied by its full softmax probability, so every score learns, through the softmax's denominator. "
            "<bookmark mark='c'/> But renormalize a single expert's gate and it's always exactly one: the router "
            "learns nothing, ever. That's why Switch keeps the raw probability. <bookmark mark='d'/> Either way, a "
            "router learns only from what it tried, which is why it needs noise to explore, and, as the next "
            "chapters show, help to share the work."
        ) as vo:
            self.play(FadeIn(pc))
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(cite_))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            self.play(Indicate(rows[3][2], color=C.SURPRISE))
            vo.wait_until("d")
            self.play(FadeOut(cite_), FadeIn(ta))
        self.wait(0.3)
        self.clear_scene()
