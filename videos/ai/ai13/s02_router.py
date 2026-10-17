from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import EXPERT_COLORS, MONO, ROUTER, billions, load


class Router(VoiceoverScene):
    def construct(self):
        self.card()
        self.mechanism()
        self.table()
        self.exact()

    def card(self):
        card = chapter_card(1, r"A mixture of experts", r"How does a router choose?", part=13)
        with self.voiceover("Chapter one. A mixture of experts."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def mechanism(self):
        E, k = 8, 2
        x = VGroup(*[Square(0.24, stroke_width=0.6, stroke_color=GREY_D, fill_color=C.EMBED, fill_opacity=o)
                     for o in (0.3, 0.8, 0.5, 0.2, 0.7, 0.4)]).arrange(DOWN, buff=0).move_to([-5.6, 0, 0])
        xl = MathTex(r"x", font_size=34, color=C.EMBED).next_to(x, UP, buff=0.15)
        router = RoundedRectangle(width=1.3, height=0.8, corner_radius=0.12, stroke_color=ROUTER, stroke_width=3).move_to([-3.6, 0, 0])
        rl = label(r"router", font_size=24, color=ROUTER).move_to(router)
        logits = np.array([0.4, 2.1, -0.3, 0.9, 1.7, -0.8, 0.1, 0.5])
        probs = np.exp(logits) / np.exp(logits).sum()
        top = np.argsort(-logits)[:k]
        bars = VGroup()
        for i, p in enumerate(probs):
            b = Rectangle(width=0.32, height=max(2.6 * p, 0.03), stroke_width=0, fill_color=ROUTER, fill_opacity=0.85)
            b.move_to([-1.9 + 0.42 * i, -1.2 + 1.3 * p, 0])
            bars.add(b)
        bl = label(r"softmax over the experts", font_size=20, color=GREY_A).next_to(bars, DOWN, buff=0.2)
        experts = VGroup(*[RoundedRectangle(width=0.9, height=0.55, corner_radius=0.1, stroke_color=EXPERT_COLORS[i],
                                            stroke_width=2).move_to([2.4, 2.45 - 0.7 * i, 0]) for i in range(E)])
        el = VGroup(*[MathTex(rf"E_{i + 1}", font_size=24, color=EXPERT_COLORS[i]).move_to(e_) for i, e_ in enumerate(experts)])
        arrows = VGroup(*[Arrow(router.get_right(), experts[i].get_left(), buff=0.1, color=ROUTER, stroke_width=3) for i in top])
        out = MathTex(r"y", font_size=34, color=C.BITS).move_to([5.2, 0, 0])
        outs = VGroup(*[Arrow(experts[i].get_right(), out.get_left(), buff=0.1, color=EXPERT_COLORS[i], stroke_width=3) for i in top])
        colors = {r"g_i": ROUTER, r"E_i": C.BITS}
        f = cmath(r"y", "=", r"\sum_{i \,\in\, \mathrm{top}\,k}", r"g_i", r"\,", r"E_i", r"(x)", colors=colors,
                  font_size=38).to_edge(DOWN, buff=0.45).shift(LEFT * 2.6)
        fl = label(r"$g$: \ the chosen experts' router probabilities, \ rescaled to add to one", font_size=22,
                   color=GREY_A).next_to(f, UP, buff=0.12)
        tag = note(r"illustrative router scores").to_corner(UR, buff=0.3)
        cite_ = cite(r"R.~Jacobs, M.~Jordan, S.~Nowlan \& G.~Hinton (1991); \ N.~Shazeer et al.\ (2017)", corner=UL)
        with self.voiceover(
            "Here's one layer. Instead of one big network, it holds several smaller ones, the experts. "
            "<bookmark mark='a'/> A router, just one more matrix, scores the token against every expert, and a "
            "softmax turns the scores into probabilities. <bookmark mark='b'/> Only the top k experts run: here, "
            "two of eight. <bookmark mark='c'/> Their outputs are mixed, weighted by the router's probabilities. "
            "The idea is from 1991; Noam Shazeer and colleagues made it sparse, and huge, in 2017."
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
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in outs], lag_ratio=0.3), FadeIn(out), Write(f), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        c = load("configs")
        rows = c["rows"]
        lo, hi = 9.0, 12.2  # log10 parameters
        sc = 6.2 / (hi - lo)
        g = VGroup()
        for i, r in enumerate(rows):
            y = 2.0 - i * 0.78
            nm = label(rf"{r['name']} \ ({r['year']})", font_size=22, color=WHITE).move_to([-2.9, y + 0.1, 0], aligned_edge=RIGHT)
            ex = label(rf"${r['k']}$ of ${r['experts']}$" + (r" $+1$ shared" if r["shared"] else ""), font_size=18,
                       color=GREY_B).move_to([-2.9, y - 0.17, 0], aligned_edge=RIGHT)
            wt = (math.log10(r["total"]) - lo) * sc
            wa = (math.log10(r["active"]) - lo) * sc
            bt = Rectangle(width=wt, height=0.42, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9).move_to([-2.6 + wt / 2, y, 0])
            ba = Rectangle(width=wa, height=0.42, stroke_width=0, fill_color=C.BITS, fill_opacity=0.9).move_to([-2.6 + wa / 2, y, 0])
            vt = MathTex(billions(r["total"]), font_size=22, color=GREY_B).next_to(bt, RIGHT, buff=0.1)
            va = MathTex(billions(r["active"]), font_size=20, color=BLACK).move_to(ba.get_right() + LEFT * 0.45)
            g.add(VGroup(nm, ex, bt, ba, vt, va))
        key = VGroup(label(r"all parameters", font_size=22, color=GREY_B), label(r"used per token", font_size=22, color=C.BITS))
        key.arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.3)
        tag = note(r"as published; \ log scale").to_corner(DR, buff=0.3)
        ds = next(r for r in rows if r["name"] == "DeepSeek-V3")
        qn = next(r for r in rows if r["name"].startswith("Qwen3-Next"))
        with self.voiceover(
            "Almost every frontier model now works this way. <bookmark mark='a'/> Mixtral used two experts of "
            f"eight. DeepSeek-V3 uses {ds['k']} of {ds['experts']}; Kimi K2 has a trillion parameters and uses "
            f"thirty-two billion; Qwen3-Next, {qn['k']} of {qn['experts']}, under four percent of its weights per token. "
            "<bookmark mark='b'/> The model knows as much as its total size, roughly, and costs as much to run as its "
            "active size."
        ) as vo:
            self.play(FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exact(self):
        colors = {r"s_i": ROUTER, r"b_i": C.SURPRISE, r"g_i": C.BITS}
        eqs = VGroup(
            cmath(r"s_i", r"= \sigma\big(u^{\top} e_i\big)", colors=colors, font_size=32),
            cmath(r"\mathcal{K} = \operatorname{top}_k\big(", r"s_i", r"+", r"b_i", r"\big)", colors=colors, font_size=32),
            cmath(r"g_i", r"= \frac{", r"s_i", r"}{\sum_{j \in \mathcal{K}} s_j}, \quad i \in \mathcal{K}", colors=colors, font_size=32),
            cmath(r"h = u + \operatorname{FFN}_{\text{shared}}(u) + \sum_{i \in \mathcal{K}}", r"g_i", r"\, \operatorname{FFN}_i(u)",
                  colors=colors, font_size=32),
        ).arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([-3.2, 0.3, 0])
        notes = VGroup(label(r"a sigmoid score per expert, \ not a softmax", font_size=18, color=GREY_A),
                       label(r"the balancing bias picks the experts \ (chapter two)...", font_size=18, color=C.SURPRISE),
                       label(r"...but the weights ignore it", font_size=18, color=C.BITS),
                       label(r"one shared expert for every token", font_size=18, color=GREY_A))
        for n_, e_ in zip(notes, eqs):
            n_.next_to(e_, DOWN, buff=0.06).align_to(e_, LEFT)
        for k in range(1, len(eqs)):
            VGroup(*eqs[k:], *notes[k:]).shift(DOWN * 0.18)
        head = label(r"DeepSeek-V3's router, \ exactly", font_size=28).to_edge(UP, buff=0.35)
        # why many small experts: the number of ways to combine them
        c1, c2 = math.comb(16, 2), math.comb(64, 8)
        big = VGroup(*[Square(0.34, stroke_color=GREY_B, stroke_width=1.5, fill_color=ROUTER, fill_opacity=0.8 if i in (3, 11) else 0.05)
                       for i in range(16)]).arrange_in_grid(rows=2, cols=8, buff=0.06)
        lit_small = {2, 9, 17, 30, 38, 45, 51, 60}
        small = VGroup(*[Square(0.155, stroke_color=GREY_B, stroke_width=1, fill_color=ROUTER, fill_opacity=0.8 if i in lit_small else 0.05)
                         for i in range(64)]).arrange_in_grid(rows=4, cols=16, buff=0.035)
        VGroup(big, small).arrange(DOWN, buff=1.5).move_to([3.6, 0.1, 0])
        bl = MathTex(rf"\binom{{16}}{{2}} = {c1}", font_size=30).next_to(big, DOWN, buff=0.15)
        sl = MathTex(rf"\binom{{64}}{{8}} = {c2:,}".replace(",", "{,}"), font_size=30, color=ROUTER).next_to(small, DOWN, buff=0.15)
        bt = label(r"$2$ of $16$ experts", font_size=20, color=GREY_A).next_to(big, UP, buff=0.12)
        st = label(r"$8$ of $64$, \ each a quarter the size: \ the same compute", font_size=20, color=GREY_A).next_to(small, UP, buff=0.12)
        cite_ = cite(r"DeepSeek-AI, \textit{DeepSeek-V3} (2024); \ D.~Dai et al., \textit{DeepSeekMoE} (2024)", corner=DR)
        with self.voiceover(
            "Here is DeepSeek-V3's router exactly, since it's become a template. <bookmark mark='a'/> Each expert "
            "gets a score from a sigmoid, its own yes-or-no, rather than a softmax that makes experts compete. "
            "<bookmark mark='b'/> The top k are chosen by score plus a bias, the balancing bias of the next chapter. "
            "<bookmark mark='c'/> But the weights that mix the chosen experts use the scores alone, rescaled to add to "
            "one, so balancing never distorts what the model computes. <bookmark mark='d'/> And one shared expert "
            "sees every token, to hold what everything needs. <bookmark mark='e'/> Why so many small experts? Count "
            f"the combinations. Two of sixteen experts can be paired {c1} ways. Cut each expert into four and choose "
            f"eight of sixty-four, for the same compute, and there are {c2 / 1e9:.1f} billion ways: far more room "
            "for each token to get its own specialized mixture."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(Write(eqs[k]), FadeIn(notes[k]))
            vo.wait_until("e")
            self.play(FadeIn(big), FadeIn(bt), Write(bl))
            self.play(FadeIn(small), FadeIn(st), Write(sl))
        self.wait(0.3)
        self.clear_scene()
