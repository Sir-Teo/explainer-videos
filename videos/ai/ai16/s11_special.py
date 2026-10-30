from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (DENSEC, EXPERT_COLORS, HISTC, MOEC, MONO, PART, TOTALC, load, ms, show, take_away)


class Special(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()
        self.information()
        self.literature()
        self.board()

    def card(self):
        card = chapter_card(10, r"What experts learn", r"Do experts specialize, \ and in what?", part=PART)
        with self.voiceover("Chapter ten. What experts learn."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def table(self):
        s = load("special")
        chars = [str(c_) for c_ in s["route_chars"]]
        nl = sum(1 for k in s if k.startswith("moe_s0_l"))
        li = nl - 1  # the last block
        M = np.asarray(s[f"moe_s0_l{li}"]["table"], float)
        E = M.shape[1]
        cell = min(0.34, 11.0 / len(chars))
        grid = VGroup()
        for i in range(len(chars)):
            for j in range(E):
                grid.add(Square(cell, stroke_width=0.4, stroke_color=GREY_D, fill_color=EXPERT_COLORS[j],
                                fill_opacity=0.04 + 0.92 * float(M[i, j])).move_to([i * cell, -j * cell, 0]))
        grid.center().move_to(DOWN * 0.2)
        names = VGroup(*[data_text(show(c_), font=MONO, font_size=20, color=C.BITS if c_ in "aeiou" else GREY_A)
                         .next_to(grid[i * E], UP, buff=0.08) for i, c_ in enumerate(chars)])
        el = VGroup(*[MathTex(rf"E_{j + 1}", font_size=22, color=EXPERT_COLORS[j]).next_to(grid[j], LEFT, buff=0.1) for j in range(E)])
        head = label(rf"our mixture, \ block {li + 1}: \ where each character's tokens go \ (both choices; \ seed 1)",
                     font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        top1 = M.argmax(1)
        vow = [i for i, c_ in enumerate(chars) if c_ in "aeiou"]
        punct = [i for i, c_ in enumerate(chars) if c_ in " .,;\"'?!-"]
        caps = [i for i, c_ in enumerate(chars) if c_.isupper()]
        bv = np.bincount(top1[vow], minlength=E)
        ev, cv = int(bv.argmax()), int(bv.max())
        bp = np.bincount(top1[punct], minlength=E)
        ep, cp = int(bp.argmax()), int(bp.max())
        pattern = cv * 2 > len(vow) or cp * 2 > len(punct)
        boxes = VGroup()
        if pattern:
            for idx, e in ((vow, ev), (punct, ep)):
                for i in idx:
                    if top1[i] == e:
                        boxes.add(SurroundingRectangle(grid[i * E + e], color=WHITE, buff=0.0, stroke_width=2))
        note_ = label(r"columns: \ the character just read; \ rows: \ experts; \ bright: \ often chosen", font_size=20,
                      color=GREY_B).next_to(grid, DOWN, buff=0.3)
        verdict = label((rf"${cv}$ of the ${len(vow)}$ vowels go mostly to $E_{ev + 1}$; \ "
                         rf"${cp}$ of the ${len(punct)}$ spaces and marks to $E_{ep + 1}$")
                        if pattern else r"no neat specialties: \ the experts split the work in ways \\ that don't "
                        r"map onto our categories", font_size=24, color=C.BITS).to_edge(DOWN, buff=0.4)
        if pattern:
            found = (f"Some patterns appear: {cv} of the {len(vow)} vowels go mostly to expert {ev + 1}, and {cp} of the "
                     f"{len(punct)} spaces and punctuation marks to expert {ep + 1}. Nobody told it to. ")
        else:
            found = "There's structure, but not the neat specialties you might imagine. "
        with self.voiceover(
            "What do the experts learn? Here's where our mixture sends each common character's tokens, in its last "
            "block: one column per character just read, one row per expert. <bookmark mark='a'/> " + found
            + "<bookmark mark='b'/> But is it about the character itself, or about what comes next? We can measure it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(names), FadeIn(el), FadeIn(note_))
            vo.wait_until("a")
            self.play(FadeIn(verdict), LaggedStart(*[Create(b_) for b_ in boxes], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Indicate(verdict, color=WHITE, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def information(self):
        s = load("special")
        seeds = [int(x) for x in s["seeds"]]
        nl = sum(1 for k in s if k.startswith("moe_s0_l"))
        kinds = [("prv", r"the character before", GREY_B), ("cur", r"the character just read", C.BITS),
                 ("nxt", r"the character to come", C.TRUE_P), ("shuf", r"shuffled \ (chance)", GREY_D)]
        vals = {(li, k): [float(s[f"moe_s{sd}_l{li}"][k]) for sd in seeds] for li in range(nl) for k, _, _ in kinds}
        top = max(max(v) for v in vals.values()) * 1.15
        groups = VGroup()
        for li in range(nl):
            g = VGroup()
            for j, (k, nm, col) in enumerate(kinds):
                mu, lo, hi = ms(vals[(li, k)])
                h = 3.4 * mu / top
                bar = Rectangle(width=0.55, height=max(h, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85)
                bar.move_to([j * 0.75, h / 2, 0])
                er = Line([j * 0.75, 3.4 * lo / top, 0], [j * 0.75, 3.4 * hi / top, 0], color=WHITE, stroke_width=2)
                v = MathTex(f"{mu:.2f}", font_size=20, color=col).next_to(bar, UP, buff=0.08)
                g.add(VGroup(bar, er, v))
            base = Line([-0.4, 0, 0], [3 * 0.75 + 0.4, 0, 0], color=GREY_C)
            t = label(rf"block {li + 1}", font_size=24, color=WHITE).next_to(base, DOWN, buff=0.25)
            groups.add(VGroup(g, base, t))
        groups.arrange(RIGHT, buff=1.4, aligned_edge=DOWN).move_to([-1.6, -0.6, 0])
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=col, fill_opacity=0.85), label(nm, font_size=20, color=col))
                       .arrange(RIGHT, buff=0.12) for _, nm, col in kinds]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        key.move_to([4.7, 0.6, 0])
        head = label(r"how much an expert's being chosen tells you about... \ (mutual information, bits)", font_size=24)
        head.to_edge(UP, buff=0.35)
        tag = note(r"three seeds: \ bars the mean, \ lines the range; \ $16{,}384$ held-out tokens, both choices",
                   font_size=18).to_edge(DOWN, buff=0.25)
        last = nl - 1
        cur, nxt, prv = (ms(vals[(last, k)])[0] for k in ("cur", "nxt", "prv"))
        first_cur = ms(vals[(0, "cur")])[0]
        if cur > nxt and cur > prv:
            v1 = (f"The choice of expert says most about the character just read: {cur:.2f} bits in the last block, "
                  f"against {nxt:.2f} about the one to come and {prv:.2f} about the one before. ")
        elif nxt > cur:
            v1 = (f"In the last block the choice says more about the character to come, {nxt:.2f} bits, than about the "
                  f"one just read, {cur:.2f}. ")
        else:
            v1 = f"In the last block the choice says most about the character before, {prv:.2f} bits. "
        v2 = ("So the experts sort tokens mostly by what they are, on the surface, not by what the model must predict: "
              "the router is a fast lookup on the current token. " if cur > nxt else
              "So the router is sorting by what the model must predict. ")
        fseeds = [int(x) for x in range(2)]
        fcur = ms([float(s[f"fine_s{sd}_l{last}"]["cur"]) for sd in fseeds])[0]
        fH = float(s[f"fine_s0_l{last}"]["H"])
        fl_ = label(rf"$32$ fine experts: \ ${fcur:.2f}$ bits about the character just read, \ of at most ${fH:.0f}$",
                    font_size=20, color=C.BITS).next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        v3 = (f"With thirty-two smaller experts there's more room to sort: the choice says {fcur:.2f} bits about the "
              f"current character, against {cur:.2f} with eight. " if fcur > cur + 0.05 else
              f"With thirty-two smaller experts, the choice says {fcur:.2f} bits about the current character, much as "
              f"with eight. ")
        with self.voiceover(
            "Mutual information, from part one: how many bits the choice of expert tells you about a character. "
            "<bookmark mark='a'/> " + v1 + "<bookmark mark='v'/>" + v2 + "<bookmark mark='b'/> The shuffled bars are chance: what a router "
            "that ignored the characters would score, given this much text. <bookmark mark='c'/> " + v3
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), FadeIn(tag), *[FadeIn(VGroup(g_[1], g_[2])) for g_ in groups])
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1:])) for g_ in groups for b_ in g_[0][:3]],
                                  lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(*[AnimationGroup(GrowFromEdge(g_[0][3][0], DOWN), FadeIn(g_[0][3][1:])) for g_ in groups])
            vo.wait_until("c")
            self.play(FadeIn(fl_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def literature(self):
        cards = VGroup(
            history_card(2024, r"Mixtral of Experts \ (Jiang et al.)", r"no obvious experts for topics like biology "
                         r"or philosophy; \ instead, syntax: \ the same expert for \texttt{self} in Python, \ for "
                         r"indentation, \ for consecutive tokens", width=6.0, color=HISTC),
            history_card(2024, r"OLMoE \ (Muennighoff et al.)", r"a fully open mixture, \ $64$ experts, \ $8$ chosen: "
                         r"\ clearer specialization by domain \ and by vocabulary", width=6.0, color=HISTC),
        ).arrange(DOWN, buff=0.3).move_to([-3.2, -0.1, 0])
        pts = VGroup(
            label(r"our characters: \ experts by spelling", font_size=24, color=C.BITS),
            label(r"big models: \ experts by syntax and vocabulary, \\ more than by topic", font_size=24, color=GREY_A),
            label(r"``experts'' is a name, \ not a job description", font_size=26, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.6, 0.0, 0])
        with self.voiceover(
            "The big models look similar. <bookmark mark='a'/> Mistral's analysis of Mixtral found no experts for "
            "topics like biology or philosophy. Instead, syntax: the same expert for the word self in Python, for "
            "indentation, and often for consecutive tokens. <bookmark mark='b'/> OLMoE, a fully open mixture from "
            "2024, found clearer specialization, by domain and by vocabulary. <bookmark mark='c'/> The name is a little "
            "misleading. An expert isn't a specialist in chemistry; it's a slice of the network that a router learned "
            "to reach for, often for reasons on the surface of the text."
        ) as vo:
            self.play(FadeIn(pts[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=RIGHT * 0.2), FadeIn(pts[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        S = load("scoreboard")
        rows = [dict(r) for r in S["rows"]]
        mine = [i for i, r in enumerate(rows) if r.get("part") == 16]
        board = scoreboard(rows, highlight=tuple(mine), max_bits=4.0, row_h=0.46, font_size=20, bar_width=5.6,
                           label_width=5.2)
        board.move_to([0, -0.3, 0])
        head = label(r"The scoreboard: \ \textit{The Maltese Falcon}, \ chapter 2", font_size=30).to_edge(UP, buff=0.3)
        by = {r.get("key"): r for r in rows}
        m, da, dt = by["moe16"]["bits"], by["dense16"]["bits"], by["dense16t"]["bits"]
        tf = next(r for r in rows if r["part"] == 13)["bits"]
        if m < da:
            v = (f"On the scoreboard's passage, our mixture scores {m:.2f} bits a character, ahead of the dense model "
                 f"with the same arithmetic, {da:.2f}, and the dense model with all its parameters scores {dt:.2f}. ")
        else:
            v = (f"On the scoreboard's passage, our mixture scores {m:.2f} bits a character, against {da:.2f} for the "
                 f"dense model with the same arithmetic and {dt:.2f} for the one with all its parameters. ")
        w = (f"They're behind Part 13's transformer, {tf:.2f}, which reads four times as much context and is twice "
             "as wide and twice as deep: sparsity buys capacity, not context. " if tf < min(m, da, dt) else
             f"Part 13's transformer scores {tf:.2f}. ")
        with self.voiceover(
            "And the scoreboard, the series' running test on a chapter of The Maltese Falcon. <bookmark mark='a'/> "
            + v + "<bookmark mark='w'/>" + w
        ) as vo:
            self.play(FadeIn(head), FadeIn(board.axis), *[FadeIn(r_) for i, r_ in enumerate(board.rows) if i not in mine])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(board.rows[i], shift=RIGHT * 0.2) for i in mine], lag_ratio=0.4))
        self.wait(0.5)
        self.clear_scene()
