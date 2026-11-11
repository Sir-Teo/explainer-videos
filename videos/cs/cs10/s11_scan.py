from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CODE, CORE_COLORS, CTRL, DATA, FUNC, HEAD, NO, PART, YES, grid_table, load,
                                   mono)


def cells(vals, color=GREY_C, w=0.8, h=0.5, font_size=20, fill=None):
    g = VGroup()
    for v in vals:
        r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.5,
                      fill_color=fill or BG, fill_opacity=0.3 if fill else 1)
        g.add(VGroup(r, Text(str(v), font="DejaVu Sans Mono", font_size=font_size, color=WHITE).move_to(r)))
    return g.arrange(RIGHT, buff=0.08)


class Scan(VoiceoverScene):
    def construct(self):
        self.card()
        self.define()
        self.adder()
        self.hillis()
        self.blelloch()
        self.uses()

    def card(self):
        card = chapter_card(10, r"Parallel prefix", r"How do you keep every running total, \ in parallel?",
                            lit=(1980, 1990), extra=((1980, r"Ladner and Fischer"), (1990, r"Blelloch: \ scans as "
                                                                                          r"primitives")), part=PART)
        with self.voiceover("Chapter ten. Parallel prefix."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def define(self):
        sc = load("scan")
        xs = sc["xs"]
        head = label(r"The scan: \ every running total", font_size=34).to_edge(UP, buff=0.35)
        a = cells(xs).shift(UP * 1.0)
        al = label(r"input", font_size=20, color=GREY_B).next_to(a, LEFT, buff=0.3)
        pre = list(np.cumsum(xs))
        b = cells(pre, color=YES).next_to(a, DOWN, buff=0.9)
        bl = label(r"inclusive scan", font_size=20, color=YES).next_to(b, LEFT, buff=0.3)
        arrows = VGroup(*[Arrow(a[k].get_bottom(), b[k + 1].get_top() if k + 1 < len(xs) else b[k].get_top(),
                                buff=0.05, color=GREY_D, stroke_width=1.5) for k in range(len(xs) - 1)])
        serial = label(r"one at a time: \ $n - 1$ additions, \ but each needs the one before: \ span $n - 1$",
                       font_size=22, color=NO).next_to(b, DOWN, buff=0.6)
        gen = label(r"any \textit{associative} operator works: \ $+$, \ $\max$, \ matrix product, \ the adder's carry "
                    r"rule", font_size=22, color=HEAD).next_to(serial, DOWN, buff=0.35)
        with self.voiceover(
            "Here is the problem at the heart of parallel algorithms. <bookmark mark='a'/> Given a list, compute "
            "every running total: three, then three plus one, then plus four, and so on. This is called a prefix "
            "sum, or a scan. <bookmark mark='b'/> Done the obvious way it takes n minus one additions, which is fine, "
            "but each one needs the one before, so the span is also n minus one: no parallelism at all. <bookmark "
            "mark='c'/> And the operator need not be addition. Anything associative will do: maximum, matrix "
            "products, or a rule you met in Part 4."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a), FadeIn(al))
            vo.wait_until("a")
            self.play(FadeIn(bl), LaggedStart(*[FadeIn(c) for c in b], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(serial))
            vo.wait_until("c")
            self.play(FadeIn(gen))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def adder(self):
        sc = load("scan")["adder"]
        a, b = sc["a"], sc["b"]
        head = label(r"Part 4's carry-lookahead adder \ was a scan", font_size=34).to_edge(UP, buff=0.3)
        bits = lambda x: [(x >> i) & 1 for i in range(7, -1, -1)]
        ra = cells(bits(a), w=0.6, h=0.45, font_size=18).shift(UP * 1.6 + RIGHT * 0.8)
        rb = cells(bits(b), w=0.6, h=0.45, font_size=18).next_to(ra, DOWN, buff=0.12)
        la = label(rf"$a = {a}$", font_size=20, color=GREY_B).next_to(ra, LEFT, buff=0.3)
        lb = label(rf"$b = {b}$", font_size=20, color=GREY_B).next_to(rb, LEFT, buff=0.3)
        gp = sc["gp"][::-1]
        tag = lambda g, p: "g" if g else ("p" if p else "k")
        rg = cells([tag(*x) for x in gp], color=CTRL, w=0.6, h=0.45, font_size=18).next_to(rb, DOWN, buff=0.35)
        lg = label(r"generate, \ propagate, \ kill", font_size=18, color=CTRL).next_to(rg, LEFT, buff=0.3)
        op = MathTex(r"(g_2, p_2) \circ (g_1, p_1) = (g_2 \lor p_2 g_1,\ p_2 p_1)", font_size=30, color=HEAD).next_to(
            rg, DOWN, buff=0.4)
        pref = sc["prefix"][::-1]
        rc = cells([x[0] for x in pref], color=YES, w=0.6, h=0.45, font_size=18).next_to(op, DOWN, buff=0.4)
        lc = label(r"the scan of $\circ$: \ the carry out of each position", font_size=18, color=YES).next_to(
            rc, LEFT, buff=0.3)
        res = label(rf"$a + b = {sc['sum']}$: \ the sum bits are $a_i \oplus b_i \oplus c_{{i-1}}$", font_size=22,
                    color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In Part 4 we built adders. <bookmark mark='a'/> Take two eight-bit numbers. <bookmark mark='b'/> Each "
            "bit position either generates a carry, if both bits are one; propagates one, if exactly one is; or "
            "kills it. <bookmark mark='c'/> Two adjacent stretches of bits combine by this rule: the pair generates "
            "if the upper part generates, or propagates a carry the lower part generates. The rule is associative. "
            "<bookmark mark='d'/> So the carries into every position are a scan of the generate-propagate pairs under "
            "this operator. The carry-lookahead adders of Part 4, Kogge-Stone, Sklansky, Brent-Kung, were parallel "
            "prefix circuits all along, and Brent of Brent-Kung is the Brent of the last chapter's theorem."
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(ra), FadeIn(rb), FadeIn(la), FadeIn(lb), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(FadeIn(rg), FadeIn(lg))
            vo.wait_until("c")
            self.play(Write(op))
            vo.wait_until("d")
            self.play(FadeIn(rc), FadeIn(lc))
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hillis(self):
        sc = load("scan")
        lv = sc["hillis_steele"]
        head = label(r"Hillis and Steele \ (1986): \ $\log_2 n$ steps", font_size=34).to_edge(UP, buff=0.3)
        rows = [cells(l, w=0.75, h=0.45, font_size=18) for l in lv]
        g = VGroup(*rows).arrange(DOWN, buff=0.55).move_to(LEFT * 0.4 + DOWN * 0.2)
        names = VGroup(*[label(r"input" if k == 0 else rf"add the one {2 ** (k - 1)} to the left", font_size=18,
                               color=GREY_B).next_to(rows[k], RIGHT, buff=0.3) for k in range(len(rows))])
        arrows = []
        for k in range(1, len(rows)):
            d = 2 ** (k - 1)
            grp = VGroup()
            for i in range(len(lv[0])):
                grp.add(Line(rows[k - 1][i].get_bottom(), rows[k][i].get_top(), color=GREY_D, stroke_width=1.5))
                if i >= d:
                    grp.add(Line(rows[k - 1][i - d].get_bottom(), rows[k][i].get_top(), color=DATA, stroke_width=2))
            arrows.append(grp)
        cost = label(rf"span $\log_2 n$, \ but work $n \log_2 n$: \ for $n = 2^{{20}}$, \ "
                     rf"{sc['ops'][19]['hillis_steele'] / 1e6:.0f} million additions instead of 1 million",
                     font_size=21, color=NO).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The first parallel answer doubles its reach at every step. <bookmark mark='a'/> In step one, every "
            "element adds the one just to its left. In step two, the one two places to the left. Then four. "
            "<bookmark mark='b'/> After log n steps, each element has added in everything before it. Three steps for "
            "eight elements, twenty for a million. Daniel Hillis and Guy Steele used it on the Connection Machine. "
            "<bookmark mark='c'/> But count the work: nearly n additions at every step, n log n in all. For a "
            "million elements, twenty million additions where one million would do. With few processors that "
            "wasted work is real time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(names[0]))
            vo.wait_until("a")
            for k in range(1, len(rows)):
                self.play(Create(arrows[k - 1]), FadeIn(rows[k]), FadeIn(names[k]), run_time=1.2)
            vo.wait_until("b")
            self.play(Indicate(rows[-1], color=YES))
            vo.wait_until("c")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blelloch(self):
        sc = load("scan")
        up, down = sc["blelloch_up"], sc["blelloch_down"]
        head = label(r"Blelloch \ (1990): \ work-efficient", font_size=34).to_edge(UP, buff=0.3)
        n = len(up[0])
        stages = up + down
        rows = [cells(s, w=0.7, h=0.4, font_size=17) for s in stages]
        g = VGroup(*rows).arrange(DOWN, buff=0.22).move_to(LEFT * 1.2 + DOWN * 0.15)
        tags = []
        for k in range(len(stages)):
            if k == 0:
                t = r"input"
            elif k < len(up):
                t = rf"up-sweep {k}: \ partial sums of blocks of {2 ** k}"
            elif k == len(up):
                t = r"clear the last: \ the identity, 0"
            else:
                t = rf"down-sweep {k - len(up)}: \ pass prefixes down"
            tags.append(label(t, font_size=16, color=DATA if k < len(up) else (NO if k == len(up) else YES)).next_to(
                rows[k], RIGHT, buff=0.3))
        for k in range(1, len(stages)):
            prev, cur = stages[k - 1], stages[k]
            for i in range(n):
                if prev[i] != cur[i]:
                    rows[k][i][0].set_fill(DATA if k < len(up) else (NO if k == len(up) else YES), 0.35)
        cost = label(rf"$2(n-1)$ operations, \ span $2 \log_2 n$: \ for $n = 2^{{20}}$, \ "
                     rf"{sc['ops'][19]['blelloch'] / 1e6:.1f} million", font_size=21, color=HEAD).to_edge(DOWN,
                                                                                                 buff=0.25)
        res = note(r"the result is the \textit{exclusive} scan: \ each position gets the sum of everything before it",
                   font_size=17).next_to(cost, UP, buff=0.12)
        with self.voiceover(
            (
            "In 1990 Guy Blelloch showed how to scan with linear work, using a tree in two passes. <bookmark "
            "mark='a'/> The up-sweep adds neighbours in pairs, then pairs of pairs, building the partial sums of "
            "larger and larger blocks, exactly as you would add up the whole list in parallel. <bookmark "
            "mark='b'/> Then clear the last element, and sweep back down. At each level, every node passes its "
            "value to its left child and gives its right child the sum of that value and the left child's old "
            "block sum. <bookmark mark='c'/> At the bottom, each position holds the sum of everything before it. "
            "For a power-of-two n, the two sweeps use exactly n minus one additions in each sweep, two n minus "
            "two altogether, and two log-base-two n levels in this model. That is linear work, about twice the "
            "serial addition count; exclusive scan also needs an identity element. <bookmark mark='d'/> "
            "Blelloch's point was larger than the algorithm: with a fast scan as a primitive, many problems that "
            "look sequential become parallel."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(tags[0]))
            vo.wait_until("a")
            for k in range(1, len(up)):
                self.play(FadeIn(rows[k]), FadeIn(tags[k]), run_time=0.9)
            vo.wait_until("b")
            for k in range(len(up), len(stages)):
                self.play(FadeIn(rows[k]), FadeIn(tags[k]), run_time=0.9)
            vo.wait_until("c")
            self.play(FadeIn(res), Indicate(rows[-1], color=YES))
            vo.wait_until("d")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uses(self):
        cp = load("scan")["compact"]
        head = label(r"What scans are for: \ stream compaction", font_size=34).to_edge(UP, buff=0.3)
        words = cp["words"][:12]
        flags = cp["flags"][:12]
        pos = cp["positions"][:12]
        ws = VGroup(*[label(w, font_size=17, color=YES if f else GREY_B) for w, f in zip(words, flags)])
        col = lambda k: -5.6 + k * 1.02
        for k, w in enumerate(ws):
            w.move_to([col(k), 1.4, 0])
            if w.width > 0.95:
                w.width = 0.95
        fl = VGroup(*[Text(str(f), font="DejaVu Sans Mono", font_size=18, color=YES if f else GREY_D).move_to(
            [col(k), 0.5, 0]) for k, f in enumerate(flags)])
        ps = VGroup(*[Text(str(p), font="DejaVu Sans Mono", font_size=18, color=DATA if flags[k] else GREY_D).move_to(
            [col(k), -0.4, 0]) for k, p in enumerate(pos)])
        lab = VGroup(label(r"keep the words of 7 letters or more", font_size=18, color=GREY_B),
                     label(r"flags", font_size=18, color=GREY_B), label(r"exclusive scan of the flags", font_size=18,
                                                                        color=DATA))
        for l, row in zip(lab, (ws, fl, ps)):
            l.next_to(row, UP, buff=0.12).align_to([col(0) - 0.4, 0, 0], LEFT)
        kept = [k for k, f in enumerate(flags) if f]
        out = VGroup(*[label(words[k], font_size=20, color=YES) for k in kept]).arrange(RIGHT, buff=0.4).move_to(
            DOWN * 1.3)
        ol = note(r"each kept word goes to the slot its scan value names: \ all at once", font_size=18).next_to(
            out, DOWN, buff=0.2)
        more = label(r"also built on scans: \ radix sort, \ quicksort's partition, \ lexing, \ polynomial "
                     r"recurrences, \ GPU libraries' every primitive", font_size=21, color=GREY_A).to_edge(DOWN,
                                                                                                   buff=0.35)
        with self.voiceover(
            (
            "Here is the most common use. <bookmark mark='a'/> Keep only the words of seven letters or more, in "
            "parallel. <bookmark mark='b'/> Mark each word with a one if it stays, a zero if not. <bookmark "
            "mark='c'/> An exclusive scan of the marks gives each kept word its position in the output: the "
            "number of kept words before it. <bookmark mark='d'/> Now every word can be written to its place at "
            "once, without write conflicts, after the scan and required synchronization complete. <bookmark "
            "mark='e'/> The same trick drives radix sort, which splits keys by each bit in turn, quicksort's "
            "partition step, and tokenizing text in parallel. On a GPU, scan is a building block of many library "
            "primitives, alongside reduction, sorting and other techniques."
        )
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(ws), FadeIn(lab[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(FadeIn(fl), FadeIn(lab[1]))
            vo.wait_until("c")
            self.play(FadeIn(ps), FadeIn(lab[2]))
            vo.wait_until("d")
            self.play(*[TransformFromCopy(ws[k], out[i]) for i, k in enumerate(kept)], FadeIn(ol))
            vo.wait_until("e")
            self.play(FadeIn(more))
        self.wait(0.3)
        self.clear_scene()
