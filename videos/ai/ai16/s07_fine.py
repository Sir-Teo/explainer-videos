from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (EXPERTC, HISTC, MOEC, PART, ROUTER, SHAREDC, expert_row, load, ms, take_away)

NAMES = {"moe": (r"coarse: \ $2$ of $8$ experts, \ width $128$", MOEC),
         "fine": (r"fine-grained: \ $8$ of $32$, \ width $32$", C.BITS),
         "shared": (r"fine $+$ shared: \ $1$ shared $+$ $7$ of $31$", SHAREDC)}


class Fine(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.claims()
        self.count()
        self.result()

    def card(self):
        card = chapter_card(6, r"Fine-grained and shared experts", r"Many small experts, or a few big ones?", part=PART)
        with self.voiceover("Chapter six. Fine-grained and shared experts."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        rows = VGroup()
        specs = [(r"a few big experts", 8, (1, 5), 0, 0.5, 0.12, MOEC),
                 (r"cut each into four, \ choose four times as many", 32, (2, 7, 9, 14, 19, 22, 27, 30), 0, 0.22, 0.05, C.BITS),
                 (r"one of them shared by every token", 31, (3, 8, 12, 17, 21, 25, 29), 1, 0.22, 0.05, SHAREDC)]
        for t, n, lit, sh, size, buff, col in specs:
            r = expert_row(n, lit=lit, size=size, color=EXPERTC, buff=buff, shared=sh)
            if r.width > 9.5:
                r.width = 9.5
            rows.add(VGroup(label(t, font_size=22, color=col), r).arrange(DOWN, buff=0.18))
        rows.arrange(DOWN, buff=0.55).move_to([-1.0, -0.2, 0])
        card = history_card(2024, r"Damai Dai et al.\ (DeepSeek)", r"\textit{DeepSeekMoE}: \ fine-grained segmentation and "
                            r"shared-expert isolation", width=4.0, color=HISTC).to_corner(UR, buff=0.3)
        tag = note(r"the same arithmetic in all three: \ two big experts' worth", font_size=20).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In January 2024 Damai Dai and colleagues at DeepSeek asked how big an expert should be. "
            "<bookmark mark='a'/> Mixtral used a few big experts and chose two. <bookmark mark='b'/> Cut every expert "
            "into four smaller ones, and choose four times as many: the same parameters, the same arithmetic per "
            "token, but each token's mixture is assembled from finer pieces. <bookmark mark='c'/> And set one expert "
            "aside to be shared by every token, so that what every token needs, like common words and grammar, is "
            "learned once instead of being copied into every expert. They called these fine-grained segmentation and "
            "shared-expert isolation."
        ) as vo:
            self.play(FadeIn(card, shift=LEFT * 0.2), FadeIn(tag))
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[i], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def claims(self):
        rows = VGroup(
            VGroup(label(r"DeepSeekMoE $2$B", font_size=26, color=SHAREDC), label(r"$\approx$", font_size=30),
                   label(r"GShard $2.9$B", font_size=26, color=MOEC),
                   label(r"which has $1.5\times$ the expert parameters and computation", font_size=20, color=GREY_A)),
            VGroup(label(r"DeepSeekMoE $16$B", font_size=26, color=SHAREDC), label(r"$\approx$", font_size=30),
                   label(r"LLaMA2 $7$B", font_size=26, color=GREY_B),
                   label(r"with about $40\%$ of the computation", font_size=20, color=GREY_A)),
        )
        for r_ in rows:
            r_[:3].arrange(RIGHT, buff=0.35)
            r_[3].next_to(r_[:3], DOWN, buff=0.12)
        rows.arrange(DOWN, buff=0.7).move_to([0, 0.2, 0])
        head = label(r"what DeepSeek reported \ (January 2024)", font_size=28).to_edge(UP, buff=0.5)
        cite_ = cite(r"D.~Dai et al., \textit{DeepSeekMoE} (arXiv 2401.06066), \ abstract", corner=DR)
        with self.voiceover(
            "They reported that it pays. <bookmark mark='a'/> At two billion parameters, DeepSeekMoE matched GShard's "
            "design with one and a half times the expert parameters and computation. <bookmark mark='b'/> Scaled to "
            "sixteen billion, it matched Meta's dense LLaMA 2 7B with about forty percent of the computation. Those "
            "are the makers' own numbers; let's check the idea on ours."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        c1, c2, c3 = math.comb(8, 2), math.comb(32, 8), math.comb(31, 7)
        d1, d2 = math.comb(16, 2), math.comb(64, 8)
        rows = [
            cmath(r"\binom{8}{2}", r"=", rf"{c1}", font_size=38),
            cmath(r"\binom{32}{8}", r"=", rf"{c2:,}".replace(",", "{,}"), font_size=38),
            cmath(r"\Big(\frac{N}{k}\Big)^{k}", r"\le", r"\binom{N}{k}", r"\le", r"\Big(\frac{eN}{k}\Big)^{k}", font_size=38),
            cmath(r"\binom{64}{8}", r"=", rf"{d2:,}".replace(",", "{,}"), r"\quad\text{vs.}\quad \binom{16}{2} = ", rf"{d1}",
                  font_size=38),
        ]
        whys = [why(r"ways to choose $2$ of $8$: \ our coarse mixture"), why(r"$8$ of $32$: \ ours, \ fine-grained"),
                why(r"the standard bounds: \ a power of $k$"), why(r"DeepSeekMoE's own example, \ same compute")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.8, buff=0.55, edge=6.8)
        ta = take_away(r"more combinations: \ each token gets a more specific team", color=C.BITS, font_size=26)
        with self.voiceover(
            "Why should finer pieces help? Count the teams a token can get. <bookmark mark='a'/> Two of eight experts "
            f"can be chosen {c1} ways. <bookmark mark='b'/> Eight of thirty-two, the same arithmetic, can be chosen "
            f"{c2 / 1e6:.1f} million ways. <bookmark mark='c'/> The count grows like a power of k: it's "
            "squeezed between N over k and e N over k, to the power k. <bookmark mark='d'/> DeepSeek's own example: two of sixteen experts gives "
            f"{d1} teams; cut each into four and choose eight of sixty-four, and there are {d2 / 1e9:.1f} billion. "
            "Each token can get a team built more precisely for it."
        ) as vo:
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(i)
            self.play(FadeIn(ta))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        f = load("fine")
        keys = ["moe", "fine", "shared"]
        vals = {k: ms(f[f"{k}_valid"]) for k in keys}
        lo = min(v[1] for v in vals.values()) - 0.03
        hi = max(v[2] for v in vals.values()) + 0.01
        W = 5.5
        rows = VGroup()
        for i, k in enumerate(keys):
            nm, col = NAMES[k]
            mean, a, b = vals[k]
            y = 1.2 - i * 1.1
            x0 = -0.6

            def X(v):
                return x0 + W * (v - lo) / (hi - lo)
            bar = Rectangle(width=X(mean) - x0, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.8)
            bar.move_to([(x0 + X(mean)) / 2, y, 0])
            rng_ = Line([X(a), y, 0], [X(b), y, 0], color=WHITE, stroke_width=2.5)
            dots = VGroup(*[Dot([X(v), y, 0], radius=0.05, color=WHITE) for v in f[f"{k}_valid"]])
            nm_ = label(nm, font_size=21, color=col).move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT)
            val = MathTex(f"{mean:.3f}", font_size=26, color=col).next_to([X(max(b, mean)), y, 0], RIGHT, buff=0.2)
            cnt = f[f"{k}_counts"]
            sub = label(rf"${cnt['total']:,}$ parameters, \ ${cnt['active']:,}$ used".replace(",", "{,}"), font_size=16,
                        color=GREY_B).next_to(nm_, DOWN, buff=0.06).align_to(nm_, RIGHT)
            rows.add(VGroup(nm_, sub, bar, rng_, dots, val))
        head = label(r"held-out bits per character, \ after $2{,}000$ steps \ (two seeds each: \ the dots; \ axis from "
                     + rf"${lo:.2f}$)", font_size=22, color=GREY_A).to_edge(UP, buff=0.5)
        mc, mf, msh = (vals[k][0] for k in keys)
        best = min(keys, key=lambda k: vals[k][0])
        sep = lambda a_, b_: vals[a_][2] < vals[b_][1] or vals[b_][2] < vals[a_][1]  # noqa: E731  seeds don't overlap
        if mf < mc - 0.002 and sep("fine", "moe"):
            v1 = (f"Cutting the experts finer helps: {mf:.3f} bits against {mc:.3f} for the coarse mixture, and the "
                  "seeds don't overlap. ")
        elif mf < mc - 0.002:
            v1 = (f"Cutting the experts finer helps: {mf:.3f} bits against {mc:.3f} for the coarse mixture, though the "
                  "seeds overlap. ")
        else:
            v1 = (f"Cutting the experts finer doesn't help at our scale: {mf:.3f} bits against {mc:.3f} for the coarse "
                  "mixture. ")
        if msh < mf - 0.002:
            v2 = f"Adding a shared expert helps a little more: {msh:.3f}. "
        elif abs(msh - mf) <= 0.002:
            v2 = f"A shared expert adds nothing here: {msh:.3f}. "
        else:
            v2 = f"With a shared expert, {msh:.3f}: a little worse than fine-grained alone. "
        ta = take_away(r"DeepSeek-V3: \ $256$ fine experts, \ $8$ chosen, \ $1$ shared \ $\cdot$ \ Kimi K3: \ $896$, \ "
                       r"$16$ chosen, \ $2$ shared", color=SHAREDC, font_size=24)
        with self.voiceover(
            "We trained all three, with the same parameters and the same arithmetic per character, two seeds each. "
            "<bookmark mark='a'/> " + v1 + "<bookmark mark='v'/>" + v2 + "<bookmark mark='b'/> At the frontier the direction is clear: DeepSeek-V3 "
            "has two hundred and fifty-six fine experts and chooses eight, plus one shared; Kimi K3 has eight hundred "
            "and ninety-six, chooses sixteen, and shares two."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(VGroup(r_[0], r_[1])) for r_ in rows])
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_[2], LEFT), FadeIn(r_[3:])) for r_ in rows],
                                  lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(ta))
        self.wait(0.3)
        self.clear_scene()
