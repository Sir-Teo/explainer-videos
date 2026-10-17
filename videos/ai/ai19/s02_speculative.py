from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.compute import load

DRAFT, TARGET = GREY_B, C.NEURAL


class Speculative(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.rule()
        self.speed()

    def card(self):
        card = chapter_card(1, r"Guess ahead, check at once", r"Can a big model write several tokens per step?", part=19)
        with self.voiceover("Chapter one. Guess ahead, check at once."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        word = list("the girl ")
        draft = VGroup(*[VGroup(Square(0.55, stroke_color=DRAFT, stroke_width=2, fill_color=DRAFT, fill_opacity=0.12),
                                Text(c if c != " " else "·", font="DejaVu Sans Mono", font_size=30, color=WHITE))
                         for c in word[:5]]).arrange(RIGHT, buff=0.1)
        for b in draft:
            b[1].move_to(b[0])
        draft.move_to(UP * 1.0)
        dl = label(r"a small, fast model drafts $5$ characters, one by one", font_size=24, color=DRAFT).next_to(draft, UP, buff=0.3)
        big = RoundedRectangle(width=6.0, height=1.0, corner_radius=0.15, stroke_color=TARGET, stroke_width=2.5).move_to(DOWN * 0.6)
        bl = label(r"the big model scores all $5$ positions in one run", font_size=24, color=TARGET).move_to(big)
        verdict = ["ok", "ok", "ok", "no", ""]
        marks = VGroup(*[MathTex(r"\checkmark" if v == "ok" else r"\times" if v == "no" else r"", font_size=36,
                                 color=C.INTERVAL if v == "ok" else C.SURPRISE).move_to([d.get_x(), -1.5, 0])
                     for v, d in zip(verdict, draft)])  # below the big model's box
        fix = label(r"keep the agreed ones; \ at the first disagreement, \ take the big model's own choice", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "A big model writes one token per run, and each run has to read all its billions of weights from memory. "
            "That reading, not the arithmetic, is the bottleneck. <bookmark mark='a'/> So let a small, fast model "
            "draft a few tokens ahead. <bookmark mark='b'/> Then the big model checks all of them in a single run, "
            "since it can score every position at once, the way it does in training. <bookmark mark='c'/> Keep the "
            "drafts it agrees with; at the first disagreement, take the big model's choice and start again."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(dl), LaggedStart(*[FadeIn(d, shift=RIGHT * 0.2) for d in draft], lag_ratio=0.25), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(big), FadeIn(bl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.25), FadeIn(fix))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rule(self):
        s = load("speculative")
        p, q, e = np.asarray(s["p_top"]), np.asarray(s["q_top"]), np.asarray(s["emp_top"])
        names = [str(c) if str(c) != " " else "·" for c in s["top_chars"]]
        k = len(p)
        top = max(p.max(), q.max(), e.max())
        bw = 0.28

        def bars(v, col, dx):
            return VGroup(*[Rectangle(width=bw, height=max(3.0 * x / top, 0.01), stroke_width=0, fill_color=col, fill_opacity=0.85)
                            .move_to([-4.6 + 1.05 * i + dx, -2.0 + 1.5 * x / top, 0]) for i, x in enumerate(v)])

        bq, bp, be = bars(q, DRAFT, -0.3), bars(p, TARGET, 0.0), bars(e, C.BITS, 0.3)
        base = Line([-5.2, -2.0, 0], [-4.6 + 1.05 * k, -2.0, 0], color=GREY_C, stroke_width=2)
        xl = VGroup(*[Text(n, font="DejaVu Sans Mono", font_size=24, color=GREY_A).move_to([-4.6 + 1.05 * i, -2.35, 0])
                      for i, n in enumerate(names)])
        key = VGroup(label(r"the draft's guess, $q$", font_size=22, color=DRAFT), label(r"the big model, $p$", font_size=22, color=TARGET),
                     label(rf"what the rule actually outputs \\ (${int(s['N']):,}$ samples)".replace(",", "{,}"), font_size=22,
                           color=C.BITS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 1.8, 0])
        colors = {r"p(x)": TARGET, r"q(x)": DRAFT}
        f = cmath(r"\text{accept } x \text{ with probability } \min\!\Big(1, \frac{", r"p(x)", r"}{", r"q(x)", r"}\Big)",
                  colors=colors, font_size=32).to_edge(UP, buff=0.4).shift(LEFT * 1.5)
        f2 = label(r"if rejected: \ sample from what $p$ has left over, \ $\max(0, p - q)$", font_size=22, color=GREY_A)
        f2.next_to(f, DOWN, buff=0.15).align_to(f, LEFT)
        tv = float(s["tv"])
        res = label(rf"distance from $p$: \ ${tv:.4f}$ \\ (sampling noise alone)", font_size=24, color=C.BITS).next_to(key, DOWN, buff=0.5)
        cite_ = cite(r"Y.~Leviathan, M.~Kalman \& Y.~Matias (2023); \ C.~Chen et al.\ (2023)", corner=DR)
        with self.voiceover(
            "The clever part is that nothing changes about what the big model says. Accept a drafted token with "
            "probability p over q, capped at one; if it's rejected, sample from what's left of p after taking q "
            "away. <bookmark mark='a'/> Here it is on our own models: part eleven's transformer as the big one, a "
            "small counting model as the draft. <bookmark mark='b'/> Run the rule two hundred thousand times, and the "
            "characters it outputs follow the big model's probabilities exactly, not the draft's: speculative "
            "decoding is faster with no change in quality."
        ) as vo:
            self.play(Write(f), FadeIn(f2), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(base), FadeIn(xl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bq], lag_ratio=0.05),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bp], lag_ratio=0.05), FadeIn(key[:2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in be], lag_ratio=0.05), FadeIn(key[2]), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def speed(self):
        s = load("speculative")
        ks, pr = [int(k) for k in s["ks"]], [float(v) for v in s["per_run"]]
        a = float(s["alpha"])
        ax = Axes(x_range=[0, 9, 1], y_range=[0, max(pr) * 1.2, 0.5], x_length=6.8, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.4, -0.6, 0])
        xt = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.1) for k in ks])
        xn = label(r"characters drafted per round", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"characters written per run of the big model", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(k, v), radius=0.07, color=C.BITS) for k, v in zip(ks, pr)])
        line = VMobject(color=C.BITS, stroke_width=3).set_points_smoothly([ax.c2p(k, v) for k, v in zip(ks, pr)])
        f = cmath(r"\frac{1 - \alpha^{k+1}}{1 - \alpha}", font_size=40).move_to([4.2, 0.6, 0])
        fl = label(rf"$\alpha = {a:.2f}$: \ how often our draft's \\ character is accepted", font_size=24, color=GREY_A).next_to(f, DOWN, buff=0.3)
        with self.voiceover(
            f"Our little draft is accepted {100 * a:.0f} percent of the time. <bookmark mark='a'/> Drafting k "
            "characters, the big model writes on average one minus alpha to the k plus one, over one minus alpha, "
            f"per run: {pr[ks.index(4)]:.1f} with four drafted. Real systems reach two to three times the speed this "
            "way, and some models, like DeepSeek-V3, are trained to draft for themselves."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1), Write(f), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()
