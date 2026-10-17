from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import EXPERT_COLORS, MONO, load


class Special(VoiceoverScene):
    def construct(self):
        self.card()
        self.routes()
        self.worth()

    def card(self):
        card = chapter_card(3, r"What experts learn", r"Do experts specialize?", part=13)
        with self.voiceover("Chapter three. What experts learn."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def routes(self):
        m = load("moe")
        chars = [str(c_) for c_ in m["route_chars"]]
        M = np.asarray(m["route"])
        E = M.shape[1]
        cell = 0.2
        grid = VGroup()
        for i in range(len(chars)):
            for j in range(E):
                v = float(M[i, j])
                grid.add(Square(cell, stroke_width=0.4, stroke_color=GREY_D, fill_color=EXPERT_COLORS[j],
                                fill_opacity=0.05 + 0.9 * v).move_to([i * cell, -j * cell, 0]))
        grid.center().move_to(DOWN * 0.2)
        names = VGroup(*[(Text(c_ if c_ != " " else "␣", font=MONO, font_size=16, color=GREY_A)).next_to(grid[i * E], UP, buff=0.08)
                         for i, c_ in enumerate(chars)])
        el = VGroup(*[MathTex(rf"E_{j + 1}", font_size=18, color=EXPERT_COLORS[j]).next_to(grid[j], LEFT, buff=0.1) for j in range(E)])
        head = label(r"where each character sends its context \ (the expert chosen first, \ trained with the bias)",
                     font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        top1 = M.argmax(1)
        vow = [i for i, c_ in enumerate(chars) if c_ in "aeiou"]
        punct = [i for i, c_ in enumerate(chars) if c_ in " .,;\"'?!"]
        shared_v = np.bincount(top1[vow], minlength=E).max() / max(len(vow), 1)
        shared_p = np.bincount(top1[punct], minlength=E).max() / max(len(punct), 1)
        note_ = label(r"columns: \ the last character read; \ rows: \ experts; \ bright: \ often chosen", font_size=20,
                      color=GREY_B).next_to(grid, DOWN, buff=0.3)
        verdict = label((r"some experts take the vowels, \ others the spaces and punctuation: \\ "
                         r"the kinds of character Part 8's vectors grouped together")
                        if max(shared_v, shared_p) >= 0.5 else
                        r"no neat specialties: \ experts split the work in ways \\ that don't map onto our categories",
                        font_size=26, color=C.BITS).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "What do the experts learn? Here's where our balanced model sends each character's context: one column "
            "per character just read, one row per expert. <bookmark mark='a'/> "
            + ("Clear patterns appear: some experts take most contexts ending in a vowel, others those ending in a "
               "space or punctuation, the same groups the character vectors found in part eight. Nobody told it to."
               if max(shared_v, shared_p) >= 0.5 else
               "There's structure, but not the neat specialties people imagine: in large models too, experts tend to "
               "split the work along surface patterns, not topics.")
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(names), FadeIn(el), FadeIn(note_))
            vo.wait_until("a")
            self.play(FadeIn(verdict))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worth(self):
        m = load("moe")
        E, k = int(m["E"]), int(m["k"])
        rows = [(rf"dense, \ as much compute \ ($1$ layer of ${k}$ experts' width)", float(m["bits_dense_active"]), GREY_B),
                (rf"mixture: \ ${k}$ of ${E}$ experts", float(m["bits_bias"]), C.INTERVAL),
                (rf"dense, \ as many parameters \ (${E}$ experts' width)", float(m["bits_dense_total"]), GREY_A)]
        lo = min(r[1] for r in rows) - 0.06
        hi = max(r[1] for r in rows) + 0.03
        sc = 6.0 / (hi - lo)
        g = VGroup()
        for i, (t, v, col) in enumerate(rows):
            y = 1.2 - i * 1.0
            nm = label(t, font_size=24, color=col).move_to([-0.6, y, 0], aligned_edge=RIGHT)
            w = (v - lo) * sc
            bar = Rectangle(width=w, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([-0.3 + w / 2, y, 0])
            val = MathTex(f"{v:.3f}", font_size=28, color=col).next_to(bar, RIGHT, buff=0.12)
            g.add(VGroup(nm, bar, val))
        head = label(r"held-out bits per character \ (shorter is better; \ axis starts at "
                     + f"${lo:.2f}$)", font_size=24, color=GREY_A).to_edge(UP, buff=0.5)
        gain = (rows[0][1] - rows[1][1]) / max(rows[0][1] - rows[2][1], 1e-9)
        with self.voiceover(
            "Is it worth it? Compare three models. <bookmark mark='a'/> A dense one doing as much arithmetic per "
            "character as the mixture; the mixture; and a dense one with as many parameters in total. "
            f"<bookmark mark='b'/> The mixture gets {100 * min(max(gain, 0), 1):.0f} percent of the way from the first "
            "to the third, for the cost of the first. That's the trade the biggest models make: knowledge in the "
            "total, cost in the active."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(g[1], color=C.INTERVAL))
        self.wait(0.3)
        self.clear_scene()
