from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (ACCEPTC, DRAFTC, PART, REJECTC, TARGETC, load)

DRAFT, TARGET = DRAFTC, TARGETC


class Exact(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.rule()
        self.proof()
        self.joint()

    def card(self):
        card = chapter_card(6, r"Guess ahead, \ check at once", r"Can a big model write several tokens per pass, "
                            r"\ and still say exactly what it would have said?", part=PART)
        with self.voiceover("Chapter six. Guess ahead, check at once."):
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
        dl = label(r"a small, fast model drafts $5$ characters, one by one", font_size=24, color=DRAFT).next_to(draft, UP,
                                                                                                            buff=0.3)
        big = RoundedRectangle(width=6.0, height=1.0, corner_radius=0.15, stroke_color=TARGET, stroke_width=2.5).move_to(
            DOWN * 0.6)
        bl0 = label(r"the big model: \ one pass per character", font_size=24, color=TARGET).move_to(big)
        bl = label(r"the big model checks all $5$ positions in one pass", font_size=24, color=TARGET).move_to(big)
        wl = label(r"every pass reads all of its weights from memory", font_size=22, color=GREY_A).next_to(big, DOWN,
                                                                                                         buff=0.3)
        slow = VGroup(*[Text(c if c != " " else "·", font="DejaVu Sans Mono", font_size=30, color=TARGET).move_to(d)
                        for c, d in zip(word[:3], draft)])
        runs = [label(rf"passes: \ ${i + 1}$", font_size=24, color=TARGET).next_to(big, RIGHT, buff=0.3) for i in range(3)]
        verdict = ["ok", "ok", "ok", "no", ""]
        marks = VGroup(*[MathTex(r"\checkmark" if v == "ok" else r"\times" if v == "no" else r"", font_size=36,
                                 color=ACCEPTC if v == "ok" else REJECTC).move_to([d.get_x(), -1.5, 0])
                         for v, d in zip(verdict, draft)])
        fix = label(r"keep the agreed ones; \ at the first disagreement, \ take the big model's own choice",
                    font_size=24, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        hc = history_card(2018, r"Mitchell Stern, Noam Shazeer \& Jakob Uszkoreit", r"blockwise parallel decoding: \ "
                          r"guess several tokens, \ keep what the model agrees with \ (for greedy decoding)",
                          width=4.6, font_size=17, color=TARGET).to_corner(UL, buff=0.25)
        with self.voiceover(
            "Chapter one showed that decoding one conversation leaves the chip's arithmetic idle, while every pass "
            "reads all the weights. <bookmark mark='a'/> So let a small, fast model draft a few tokens ahead. "
            "<bookmark mark='b'/> Then the big model checks all of them in a single pass, the way it reads a "
            "prompt: one read of the weights for several tokens. <bookmark mark='c'/> Keep the drafts it agrees "
            "with; at the first disagreement, take the big model's choice and start again. Mitchell Stern, Noam "
            "Shazeer and Jakob Uszkoreit did this in 2018 for a model that always picks its likeliest token."
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
            self.play(FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rule(self):
        s = load("exact")
        p, q, e = np.asarray(s["p_top"]), np.asarray(s["q_top"]), np.asarray(s["emp_top"])
        names = [str(c) if str(c) != " " else "·" for c in s["top_chars"]]
        k = len(p)
        top = max(p.max(), q.max(), e.max())
        bw = 0.28

        def bars(v, col, dx):
            return VGroup(*[Rectangle(width=bw, height=max(3.0 * x / top, 0.01), stroke_width=0, fill_color=col,
                                      fill_opacity=0.85).move_to([-4.6 + 1.05 * i + dx, -2.0 + 1.5 * x / top, 0])
                            for i, x in enumerate(v)])

        bq, bp, be = bars(q, DRAFT, -0.3), bars(p, TARGET, 0.0), bars(e, C.BITS, 0.3)
        base = Line([-5.2, -2.0, 0], [-4.6 + 1.05 * k, -2.0, 0], color=GREY_C, stroke_width=2)
        xl = VGroup(*[data_text(n, font="DejaVu Sans Mono", font_size=24, color=GREY_A).move_to([-4.6 + 1.05 * i, -2.35, 0])
                      for i, n in enumerate(names)])

        def part(lo, hi, i, dx, col):
            return Rectangle(width=bw, height=3.0 * (hi - lo) / top, stroke_width=0, fill_color=col,
                             fill_opacity=0.75).move_to([-4.6 + 1.05 * i + dx, -2.0 + 1.5 * (lo + hi) / top, 0])

        excess = VGroup(*[part(p[i], q[i], i, -0.3, REJECTC) for i in range(k) if q[i] > p[i]])
        left = VGroup(*[part(q[i], p[i], i, 0.0, ACCEPTC) for i in range(k) if p[i] > q[i]])
        key = VGroup(label(r"the draft's guess, $q$", font_size=22, color=DRAFT),
                     label(r"the big model, $p$", font_size=22, color=TARGET),
                     label(r"the draft's excess: \\ rejected", font_size=22, color=REJECTC),
                     label(r"$p$'s leftover: \\ where rejections resample", font_size=22, color=ACCEPTC),
                     label(rf"what the rule actually outputs \\ (${int(s['N']):,}$ samples)".replace(",", "{,}"),
                           font_size=22, color=C.BITS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 1.3, 0])
        colors = {r"p(x)": TARGET, r"q(x)": DRAFT}
        f = cmath(r"\text{accept } x \text{ with probability } \min\!\Big(1, \frac{", r"p(x)", r"}{", r"q(x)",
                  r"}\Big)", colors=colors, font_size=32).to_edge(UP, buff=0.4).shift(LEFT * 1.5)
        f2 = label(r"if rejected: \ sample from what $p$ has left over, \ $\max(0, p - q)$", font_size=22, color=GREY_A)
        f2.next_to(f, DOWN, buff=0.15).align_to(f, LEFT)
        tv, tvd = float(s["tv"]), float(s["tv_direct"])
        res = label(rf"distance from $p$: \ ${tv:.4f}$ \\ sampling $p$ itself: \ ${tvd:.4f}$", font_size=22,
                    color=C.BITS).next_to(key, DOWN, buff=0.35)
        ctx = data_text(str(s["context"])[-34:], font="DejaVu Sans Mono", font_size=30, color=GREY_A)
        qbox = VGroup(Square(0.5, stroke_color=C.BITS, stroke_width=2.5, fill_color=C.BITS, fill_opacity=0.15),
                      Text("?", font="DejaVu Sans Mono", font_size=30, color=C.BITS))
        qbox.next_to(ctx, RIGHT, buff=0.12)
        line_ = VGroup(ctx, qbox)
        if line_.width > 12.4:
            line_.scale_to_fit_width(12.4)
        line_.move_to([0, 0.4, 0])
        cl_ = label(r"the passage so far: \ which character comes next?", font_size=26, color=GREY_A).next_to(line_, UP,
                                                                                                            buff=0.4)
        hc = history_card(2022, r"Yaniv Leviathan, Matan Kalman \& Yossi Matias; \ Charlie Chen et al.\ (2023)",
                          r"speculative sampling: \ the same distribution as the big model, \ $2$--$3\times$ faster",
                          width=5.0, font_size=17, color=ACCEPTC).to_corner(DR, buff=0.2)
        same = "as close to p as sampling p itself" if tv < 2.5 * tvd + 1e-3 else "close to p"
        with self.voiceover(
            "Sampling is harder: the big model doesn't have one answer, it has a distribution, and the drafts come "
            "from a different one. In late 2022, Yaniv Leviathan, Matan Kalman and Yossi Matias at Google found a "
            "rule that makes the output come out exactly right, and Charlie Chen's team at DeepMind found it too. "
            "<bookmark mark='a'/> Here are both guesses for the next character, on our own models: Part 13's "
            "transformer as the big one, a counting model on the last two characters as the draft. "
            "<bookmark mark='b'/> Accept a drafted character with probability p over q, capped at one: where the "
            "draft guesses a character too often, the excess is thrown out. <bookmark mark='c'/> If it's rejected, "
            "sample from what's left of p after taking q away: exactly where the draft guessed too rarely. "
            f"<bookmark mark='d'/> Run the rule {int(s['N']):,} times: the characters it writes are {same}."
        ) as vo:
            self.play(FadeIn(cl_), FadeIn(ctx), FadeIn(hc), run_time=1.0)
            self.play(FadeIn(qbox, scale=1.3))
            vo.wait_until("a")
            self.play(FadeOut(cl_), FadeOut(hc), line_.animate.scale_to_fit_width(7.6).move_to([-1.6, 1.85, 0]), run_time=0.8)
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
    def proof(self):
        colors = {r"p(x)": TARGET, r"q(x)": DRAFT, r"p(y)": TARGET, r"q(y)": DRAFT, r"r(x)": ACCEPTC}
        rows = [
            cmath(r"\Pr[\text{out} = x]", r"=", r"q(x)\min\!\Big(1, \tfrac{p(x)}{q(x)}\Big)", r"+",
                  r"\Pr[\text{reject}]\; r(x)", colors=colors, font_size=30),
            cmath(r"q(x)\min\!\Big(1, \tfrac{p(x)}{q(x)}\Big)", r"=", r"\min\big(p(x), q(x)\big)", colors=colors,
                  font_size=30),
            cmath(r"\Pr[\text{reject}]", r"=", r"1 - \sum_y \min\big(p(y), q(y)\big)", r"=",
                  r"\sum_y \big(p(y) - \min(p(y), q(y))\big)", colors=colors, font_size=30),
            cmath(r"r(x)", r"=", r"\frac{p(x) - \min(p(x), q(x))}{\sum_y \big(p(y) - \min(p(y), q(y))\big)}",
                  colors=colors, font_size=30),
            cmath(r"\Pr[\text{out} = x]", r"=", r"\min(p(x), q(x)) + p(x) - \min(p(x), q(x))", r"=", r"p(x)",
                  colors=colors, font_size=30),
        ]
        whys = [why(r"accepted, \ or rejected and resampled"), why(r"multiply in: \ $\min(q, p)$"),
                why(r"$\sum_y p(y) = 1$"), why(r"the leftover, \ normalized"), why(r"the denominators cancel")]
        step = ladder(self, rows, whys, keep=5, top=3.4, x=-1.2, buff=0.24, edge=6.8)
        thm = theorem_card(r"speculative sampling is exact", r"Whatever the draft $q$, \ the token written has "
                           r"distribution exactly $p$. \ The draft only changes how often a pass is saved.",
                           who=r"Leviathan, Kalman \& Matias (2022); \ Chen et al.\ (2023)", width=7.6, font_size=20,
                           color=ACCEPTC).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Why is that exact? <bookmark mark='a'/> The rule writes x in one of two ways: x is drafted and "
            "accepted, or a draft is rejected and x is resampled. <bookmark mark='b'/> Drafted and accepted has "
            "probability q times the acceptance, which is the smaller of p and q. <bookmark mark='c'/> A rejection "
            "happens with probability one minus the sum of those minimums, which, since p sums to one, is the sum "
            "of what p has left over. <bookmark mark='d'/> And the resampling distribution is that leftover, "
            "normalized by the same sum. <bookmark mark='e'/> Multiply, and the sums cancel: the minimum plus the "
            "leftover is p. Whatever the draft, the token written has exactly the big model's distribution. The "
            "draft only decides how often a pass is saved."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(FadeIn(thm, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def joint(self):
        jt = load("exact")["joint"]
        p, sp_, di, nv = (np.asarray(jt[k]) for k in ("p_top", "spec_top", "direct_top", "naive_top"))
        names = ["".join(t).replace("\n", "↵") for t in jt["top_text"]]
        k = len(p)
        top = max(p.max(), sp_.max(), di.max(), nv.max())
        bw = 0.2
        cols = [(TARGET, p), (ACCEPTC, sp_), (GREY_B, di), (REJECTC, nv)]
        X0, dxs = -5.6, (-0.3, -0.1, 0.1, 0.3)
        allbars = VGroup()
        for (col, v), dx in zip(cols, dxs):
            allbars.add(VGroup(*[Rectangle(width=bw, height=max(3.0 * x / top, 0.01), stroke_width=0, fill_color=col,
                                           fill_opacity=0.85).move_to([X0 + 1.2 * i + dx, -2.1 + 1.5 * x / top, 0])
                                 for i, x in enumerate(v)]))
        base = Line([X0 - 0.5, -2.1, 0], [X0 + 1.2 * k - 0.6, -2.1, 0], color=GREY_C, stroke_width=2)
        xl = VGroup(*[data_text(n, font="DejaVu Sans Mono", font_size=16, color=GREY_A).move_to([X0 + 1.2 * i, -2.4, 0])
                      for i, n in enumerate(names)])
        for t_ in xl:
            if t_.width > 1.1:
                t_.width = 1.1
        ctx = data_text("…" + str(jt["context"]).replace("\n", " ")[-40:], font="DejaVu Sans Mono", font_size=22,
                        color=GREY_A).to_edge(UP, buff=0.35)
        head = label(r"the next two tokens of our novels model: \ the likeliest pairs", font_size=22,
                     color=GREY_A).next_to(ctx, DOWN, buff=0.15)
        key = VGroup(label(r"exactly, \ $p(y_1)\,p(y_2 \mid y_1)$", font_size=20, color=TARGET),
                     label(r"speculative, \ $2$ tokens drafted", font_size=20, color=ACCEPTC),
                     label(r"sampling the big model directly", font_size=20, color=GREY_B),
                     label(r"drafts kept unchecked", font_size=20, color=REJECTC)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.12)
        key.move_to([4.5, 0.8, 0])
        tvs = VGroup(label(r"total variation from exact:", font_size=20, color=GREY_A),
                     label(rf"speculative \ ${jt['tv_spec']:.3f}$", font_size=20, color=ACCEPTC),
                     label(rf"direct \ ${jt['tv_direct']:.3f}$", font_size=20, color=GREY_B),
                     label(rf"unchecked \ ${jt['tv_naive']:.3f}$", font_size=20, color=REJECTC)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(key, DOWN, buff=0.35).align_to(key, LEFT)
        ok = jt["tv_spec"] < 1.3 * jt["tv_direct"] + 0.005
        verdict = ("Speculative sampling is as close to exact as sampling the big model itself: what's left is the "
                   "noise of a finite sample" if ok else "Speculative sampling lands farther from exact than direct "
                   "sampling, more than the noise of a finite sample")
        with self.voiceover(
            "One more check, on the novels model, with the small drafter we'll train in the next chapter. "
            "<bookmark mark='a'/> At one place in a held-out novel, we drafted two tokens at a time and let the "
            f"rule run, {int(jt['N']):,} times, keeping the first two tokens it wrote. The exact answer is known: "
            "the big model's probability of the first token, times its probability of the second given the "
            "first. <bookmark mark='b'/> " + verdict + f": a total variation of {jt['tv_spec']:.3f}, "
            f"against {jt['tv_direct']:.3f}. <bookmark mark='c'/> Keep the drafts without checking, and you get the "
            f"draft's distribution instead: {jt['tv_naive']:.3f}."
        ) as vo:
            self.play(FadeIn(ctx), FadeIn(head), Create(base), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in allbars[0]], lag_ratio=0.05), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in allbars[1]], lag_ratio=0.05),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in allbars[2]], lag_ratio=0.05), FadeIn(key[1:3]),
                      FadeIn(tvs[:3]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in allbars[3]], lag_ratio=0.05), FadeIn(key[3]),
                      FadeIn(tvs[3]))
        self.wait(0.3)
        self.clear_scene()
