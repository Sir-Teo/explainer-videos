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
        bl0 = label(r"the big model: \ one run per character", font_size=24, color=TARGET).move_to(big)
        bl = label(r"the big model scores all $5$ positions in one run", font_size=24, color=TARGET).move_to(big)
        wl = label(r"every run reads all of its weights from memory", font_size=22, color=GREY_A).next_to(big, DOWN, buff=0.3)
        slow = VGroup(*[Text(c if c != " " else "·", font="DejaVu Sans Mono", font_size=30, color=TARGET).move_to(d)
                        for c, d in zip(word[:3], draft)])
        runs = [label(rf"runs: \ ${i + 1}$", font_size=24, color=TARGET).next_to(big, RIGHT, buff=0.3) for i in range(3)]
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
            self.play(FadeIn(tag), Create(big), FadeIn(bl0), FadeIn(wl))
            for i in range(3):
                self.play(big.animate.set_fill(TARGET, 0.35), run_time=0.35)
                self.play(big.animate.set_fill(TARGET, 0.0), FadeIn(slow[i], shift=UP * 0.3),
                          FadeIn(runs[i]) if i == 0 else Transform(runs[0], runs[i]), run_time=0.45)
            vo.wait_until("a")
            self.play(FadeOut(slow), FadeOut(runs[0]), FadeOut(wl))
            self.play(FadeIn(dl), LaggedStart(*[FadeIn(d, shift=RIGHT * 0.2) for d in draft], lag_ratio=0.25), run_time=1.6)
            vo.wait_until("b")
            self.play(ReplacementTransform(bl0, bl), big.animate.set_fill(TARGET, 0.25),
                      *[Indicate(d, color=TARGET, scale_factor=1.08) for d in draft])
            self.play(big.animate.set_fill(TARGET, 0.0))
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
        # the rule on the bars: where the draft guesses too often, the excess is rejected; where too rarely, p's leftover
        def part(lo, hi, i, dx, col):
            return Rectangle(width=bw, height=3.0 * (hi - lo) / top, stroke_width=0, fill_color=col, fill_opacity=0.75).move_to(
                [-4.6 + 1.05 * i + dx, -2.0 + 1.5 * (lo + hi) / top, 0])

        excess = VGroup(*[part(p[i], q[i], i, -0.3, C.SURPRISE) for i in range(k) if q[i] > p[i]])
        left = VGroup(*[part(q[i], p[i], i, 0.0, C.INTERVAL) for i in range(k) if p[i] > q[i]])
        key = VGroup(label(r"the draft's guess, $q$", font_size=22, color=DRAFT), label(r"the big model, $p$", font_size=22, color=TARGET),
                     label(r"the draft's excess: \\ rejected", font_size=22, color=C.SURPRISE),
                     label(r"$p$'s leftover: \\ where rejections resample", font_size=22, color=C.INTERVAL),
                     label(rf"what the rule actually outputs \\ (${int(s['N']):,}$ samples)".replace(",", "{,}"), font_size=22,
                           color=C.BITS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 1.5, 0])
        colors = {r"p(x)": TARGET, r"q(x)": DRAFT}
        f = cmath(r"\text{accept } x \text{ with probability } \min\!\Big(1, \frac{", r"p(x)", r"}{", r"q(x)", r"}\Big)",
                  colors=colors, font_size=32).to_edge(UP, buff=0.4).shift(LEFT * 1.5)
        f2 = label(r"if rejected: \ sample from what $p$ has left over, \ $\max(0, p - q)$", font_size=22, color=GREY_A)
        f2.next_to(f, DOWN, buff=0.15).align_to(f, LEFT)
        tv = float(s["tv"])
        res = label(rf"distance from $p$: \ ${tv:.4f}$ \\ (sampling noise alone)", font_size=24, color=C.BITS).next_to(key, DOWN, buff=0.4)
        cite_ = cite(r"Y.~Leviathan, M.~Kalman \& Y.~Matias (2023); \ C.~Chen et al.\ (2023)", corner=DR)
        # where in the passage: the text so far, and the character both models are guessing
        ctx = data_text(str(s["context"])[-34:], font="DejaVu Sans Mono", font_size=30, color=GREY_A)
        qbox = VGroup(Square(0.5, stroke_color=C.BITS, stroke_width=2.5, fill_color=C.BITS, fill_opacity=0.15),
                      Text("?", font="DejaVu Sans Mono", font_size=30, color=C.BITS))
        qbox.next_to(ctx, RIGHT, buff=0.12)
        line_ = VGroup(ctx, qbox)
        if line_.width > 12.4:
            line_.scale_to_fit_width(12.4)
        line_.move_to([0, 0.4, 0])
        cl_ = label(r"the passage so far: \ which character comes next?", font_size=26, color=GREY_A).next_to(line_, UP, buff=0.4)
        with self.voiceover(
            "The clever part is that nothing changes about what the big model says. <bookmark mark='a'/> Here are "
            "both guesses for the next character, on our own models: part eleven's transformer as the big one, a "
            "small counting model as the draft. <bookmark mark='b'/> Accept a drafted character with probability p "
            "over q, capped at one: where the draft guesses a character too often, the excess gets thrown out. "
            "<bookmark mark='c'/> If it's rejected, sample from what's left of p after taking q away: exactly the "
            "part the draft guessed too rarely. <bookmark mark='d'/> Run the rule two hundred thousand times, and the "
            "characters it outputs follow the big model's probabilities exactly, not the draft's: speculative "
            "decoding is faster with no change in quality."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(cl_), FadeIn(ctx), run_time=1.0)
            self.play(FadeIn(qbox, scale=1.3))
            vo.wait_until("a")
            self.play(FadeOut(cl_), line_.animate.scale_to_fit_width(7.6).move_to([-1.6, 1.85, 0]), run_time=0.8)
            self.play(Create(base), FadeIn(xl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bq], lag_ratio=0.05),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bp], lag_ratio=0.05), FadeIn(key[:2]))
            vo.wait_until("b")
            self.play(Write(f))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in excess], lag_ratio=0.1), FadeIn(key[2]))
            vo.wait_until("c")
            self.play(FadeIn(f2), LaggedStart(*[FadeIn(r_) for r_ in left], lag_ratio=0.1), FadeIn(key[3]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in be], lag_ratio=0.05), FadeIn(key[4]), FadeIn(res))
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
        yt = VGroup(*[MathTex(f"{v:g}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in np.arange(0, max(pr) * 1.2, 0.5)])
        one = DashedLine(ax.c2p(0, 1), ax.c2p(9, 1), color=GREY_B, stroke_width=1.5)
        onel = label(r"no draft: \ $1$", font_size=20, color=GREY_B).next_to(ax.c2p(9, 1), UR, buff=0.05)
        dots = VGroup(*[Dot(ax.c2p(k, v), radius=0.07, color=C.BITS) for k, v in zip(ks, pr)])
        line = VMobject(color=C.BITS, stroke_width=3).set_points_smoothly([ax.c2p(k, v) for k, v in zip(ks, pr)])
        f = cmath(r"\frac{1 - \alpha^{k+1}}{1 - \alpha}", font_size=40).move_to([4.2, 0.6, 0])
        fl = label(rf"$\alpha = {a:.2f}$: \ how often our draft's \\ character is accepted", font_size=24, color=GREY_A).next_to(f, DOWN, buff=0.3)
        # the acceptance chance at each of the 300 places in the passage it was measured: a spread, not one number
        acc = np.asarray(s["accept"], float)
        nb = 10
        hc = np.histogram(acc, bins=nb, range=(0, 1))[0]
        HW, HH, hx0, hy0 = 3.8, 1.0, 2.4, 2.05
        hbars = VGroup(*[Rectangle(width=HW / nb * 0.85, height=max(HH * c_ / hc.max(), 0.01), stroke_width=0, fill_color=C.BITS,
                                   fill_opacity=0.75).move_to([hx0 + HW * (i + 0.5) / nb, hy0 + HH * c_ / hc.max() / 2, 0])
                         for i, c_ in enumerate(hc)])
        hbase = Line([hx0, hy0, 0], [hx0 + HW, hy0, 0], color=GREY_C, stroke_width=1.5)
        hticks = VGroup(MathTex(r"0", font_size=20, color=GREY_B).next_to([hx0, hy0, 0], DOWN, buff=0.08),
                        MathTex(r"100\%", font_size=20, color=GREY_B).next_to([hx0 + HW, hy0, 0], DOWN, buff=0.08))
        hmean = DashedLine([hx0 + HW * a, hy0, 0], [hx0 + HW * a, hy0 + HH + 0.1, 0], dash_length=0.06, stroke_width=2, color=WHITE)
        hml = MathTex(rf"\alpha = {a:.2f}", font_size=22, color=WHITE).next_to(hmean, UP, buff=0.05)
        hl = label(rf"chance of acceptance, \ at ${len(acc)}$ places in the passage", font_size=18, color=GREY_A)
        hl.next_to(hbase, DOWN, buff=0.38)
        hist = VGroup(hbars, hbase, hticks, hmean, hml, hl)
        with self.voiceover(
            f"Our little draft is accepted {100 * a:.0f} percent of the time. <bookmark mark='a'/> Drafting k "
            "characters, the big model writes on average one minus alpha to the k plus one, over one minus alpha, "
            f"per run: {pr[ks.index(4)]:.1f} with four drafted. Real systems reach two to three times the speed this "
            "way, and some models, like DeepSeek-V3, are trained to draft for themselves."
        ) as vo:
            self.play(Create(hbase), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in hbars], lag_ratio=0.08), FadeIn(hticks),
                      FadeIn(hl), run_time=1.2)
            self.play(Create(hmean), FadeIn(hml), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(one), FadeIn(onel))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1), Write(f), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()
