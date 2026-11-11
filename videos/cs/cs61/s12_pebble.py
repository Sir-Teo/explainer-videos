from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import pebble, pebble_pile
from videos.cs.cs1.compute import load as load1
from videos.cs.cs61.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
         "seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def say(n) -> str:
    """A whole number as a speaker says it (British: 'thirty-three')."""
    n = int(round(n))
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + say(n % 100))
    return say(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + say(n % 1000))


def say_dec(x: float, digits: int = 1) -> str:
    """A decimal, spoken digit by digit after the point: 'one point five four'."""
    whole, frac = f"{x:.{digits}f}".split(".")
    return say(int(whole)) + " point " + " ".join(_ONES[int(c)] for c in frac)


def ordinal(n: int) -> str:
    """'twenty-first', 'third', 'twelfth'."""
    words = say(n)
    head, _, last = words.rpartition("-") if "-" in words.split()[-1] else words.rpartition(" ")
    sep = "-" if "-" in words.split()[-1] else " "
    irregular = {"one": "first", "two": "second", "three": "third", "five": "fifth", "eight": "eighth",
                 "nine": "ninth", "twelve": "twelfth"}
    last = irregular.get(last, last[:-1] + "ieth" if last.endswith("y") else last + "th")
    return (head + sep if head else "") + last


# the final ledger: every row from Part 6's single-cycle Pebble to Part 60's word-counting unit
LED = load("ledger")["rows"]
FIRST, LAST = LED[0], LED[-1]
SPEEDUP = FIRST["seconds"] / LAST["seconds"]
STEPS = len(LED) - 1
GEO = SPEEDUP ** (1 / STEPS)                       # the geometric mean of the row-to-row speedups
RATIOS = [a["seconds"] / b["seconds"] for a, b in zip(LED, LED[1:])]
assert abs(math.prod(RATIOS) - SPEEDUP) < 1e-6 * SPEEDUP   # the product telescopes
SLOWER = sum(1 for r in RATIOS if r < 1)
BEST = max(range(STEPS), key=lambda i: RATIOS[i])
WORST = min(range(STEPS), key=lambda i: RATIOS[i])
NATIVE = sum(1 for r in LED if r.get("native"))
SLOWEST = max(LED, key=lambda r: r["seconds"])
OPEN = load("open")["rows"]
PEB = load1("pebbles")
COLS = (NO, HEAD, YES, DATA, LAM, KERN)


class Pebble(VoiceoverScene):
    def construct(self):
        self.card()
        self.piles()
        self.climb()
        self.ledger()
        self.speedup()
        self.sky()
        self.stone()

    def card(self):
        card = chapter_card(11, r"The pebble, \ the last time", r"What did one rule become?",
                            lit=(1928, 1936), part=PART)
        with self.voiceover("Chapter eleven. The pebble, the last time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def piles(self):
        steps = PEB["steps"]
        L, R = np.array([-3.4, -2.6, 0]), np.array([3.4, -2.6, 0])
        head = label(r"Two piles and a rule \ (Part 1)", font_size=36).to_edge(UP, buff=0.3)
        rule = label(r"if the piles differ, \ take from the bigger as many as the smaller has", font_size=22,
                     color=GREY_A).next_to(head, DOWN, buff=0.25)
        left = pebble_pile(steps[0][0], L, cols=6, seed=1, radius=0.2)
        right = pebble_pile(steps[0][1], R, cols=6, seed=40, radius=0.2)
        cl = Integer(steps[0][0], font_size=50, color=DATA).move_to(L + UP * 2.35)
        cr = Integer(steps[0][1], font_size=50, color=DATA).move_to(R + UP * 2.35)
        gcd = MathTex(rf"{PEB['gcd']} = \gcd({steps[0][0]}, {steps[0][1]})", font_size=40, color=YES).move_to(
            DOWN * 0.6)
        q1 = VGroup(label(r"1928", font_size=26, color=HEAD),
                    wrapped_label(r"Hilbert and Ackermann: \ is there a mechanical procedure that decides every "
                                  r"mathematical claim? \ The \textit{Entscheidungsproblem}", 10.6, font_size=21,
                                  color=WHITE)).arrange(RIGHT, buff=0.35, aligned_edge=UP)
        q2 = VGroup(label(r"1936", font_size=26, color=HEAD),
                    wrapped_label(r"Turing: \ no. \ To prove it, \ he had to say what a mechanical procedure is, "
                                  r"\ and the answer was a machine", 10.6, font_size=21, color=WHITE)).arrange(
            RIGHT, buff=0.35, aligned_edge=UP)
        VGroup(q1, q2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Part 1 began with a game for someone who knows nothing about numbers: two piles of pebbles, and one "
            "rule. <bookmark mark='a'/> If the piles differ, take from the bigger as many as the smaller has. "
            f"{say(steps[0][0]).capitalize()} and {say(steps[0][1])} become {say(steps[1][0])} and "
            f"{say(steps[1][1])}, then {say(steps[2][0])} and {say(steps[2][1])}, then {say(steps[3][0])} and "
            f"{say(steps[3][1])}, <bookmark mark='b'/> and {say(PEB['gcd'])} is their greatest common divisor. "
            "<bookmark mark='c'/> In 1928 Hilbert and Ackermann asked whether every mathematical question could be "
            "settled like that, by a mechanical procedure that moves symbols the way the player moves stones: the "
            "Entscheidungsproblem. <bookmark mark='d'/> In 1936 Turing answered no, and to prove it he first had to "
            "say exactly what a mechanical procedure is. His answer was a machine, and everything else in this "
            "series was built on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left), FadeIn(right), FadeIn(cl), FadeIn(cr))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            for a, b in steps[1:]:
                nl = pebble_pile(a, L, cols=6, seed=1, radius=0.2)
                nr = pebble_pile(b, R, cols=6, seed=40, radius=0.2)
                self.play(Transform(left, nl), Transform(right, nr),
                          Transform(cl, Integer(a, font_size=50, color=DATA).move_to(cl)),
                          Transform(cr, Integer(b, font_size=50, color=DATA).move_to(cr)), run_time=0.9)
            vo.wait_until("b")
            self.play(cl.animate.set_color(YES), cr.animate.set_color(YES), Write(gcd))
            vo.wait_until("c")
            self.play(FadeOut(rule), FadeOut(cl), FadeOut(cr), gcd.animate.scale(0.8).move_to(DOWN * 1.0),
                      FadeIn(q1, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(q2, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def climb(self):
        head = label(r"The tower the series built", font_size=36).to_edge(UP, buff=0.3)
        keys = [k for k, _ in LAYERS]
        dim = tower(lit=(), labels="all", height=5.6, width=3.0, font_size=17)
        lit = tower(lit=tuple(keys) + ("limits", "practice"), labels="all", height=5.6, width=3.0, font_size=17)
        v = np.array([-3.4, -0.45, 0]) - dim.get_center()
        dim.shift(v)
        lit.shift(v)
        x0 = dim.get_right()[0] + 0.95
        groups = [
            (("math",), r"Parts 1--2: \ Turing's machine, \ proof and counting"),
            (("physics", "gates"), r"Part 3: \ every gate from NAND"),
            (("arith", "isa"), r"Parts 4--6: \ arithmetic, \ memory, \ Pebble-32 runs the Job"),
            (("uarch",), r"Parts 7--10: \ pipelines, \ caches, \ four cores"),
            (("code", "lang"), r"Parts 11--15: \ a linker, \ a compiler, \ types, \ collectors"),
            (("algo",), r"Parts 16--24: \ algorithms, \ the hash table, \ sketches"),
            (("os", "data"), r"Parts 31--35: \ PebbleOS, \ a file system, \ a database"),
            (("net", "dist"), r"Parts 36--39: \ our TCP, \ Raft, \ MapReduce"),
            (("cloud", "apps"), r"Parts 40--50: \ the web, \ services, \ the cloud, \ search"),
        ]
        notes = []
        for ks, text in groups:
            y = np.mean([dim.layer[k][0].get_y() for k in ks])
            col = LAYER_COLOR[ks[-1]]
            t = label(text, font_size=19, color=col)
            t.move_to([x0 + t.width / 2, y, 0])
            notes.append(t)
        trust = label(r"Part 55: \ can any of it be trusted?", font_size=21, color=HEAD)
        trust.move_to([x0 + trust.width / 2, lit.layer["apps"][0].get_top()[1] + 0.5, 0])

        top = lit.column["limits"][0].get_top()
        cols = VGroup(*[label(name, font_size=17, color=c) for _, name, c in COLUMNS])
        cols[0].next_to(top, UP, buff=0.12).align_to(lit.column["limits"][0], LEFT)
        cols[1].next_to(cols[0], UP, buff=0.08).align_to(lit.column["practice"][0], LEFT)

        def up(i):
            ks = groups[i][0]
            return [Transform(dim.layer[k], lit.layer[k]) for k in ks] + [FadeIn(notes[i], shift=LEFT * 0.1)]

        with self.voiceover(
            "Then the series climbed, from the mathematics at the bottom. <bookmark mark='a'/> Part 3 built every "
            "gate from one kind, NAND, <bookmark mark='b'/> and by Part 6 those gates were Pebble, a thirty-two-bit "
            "computer that ran the Job. <bookmark mark='c'/> Pipelines, caches and four cores made it fast; "
            "<bookmark mark='d'/> a linker, a compiler, types and garbage collectors let us speak to it; "
            "<bookmark mark='e'/> algorithms told it what to do. <bookmark mark='f'/> PebbleOS shared it among "
            "programs and kept their data on a disk; <bookmark mark='g'/> our own TCP, Raft and MapReduce joined "
            "many Pebbles; <bookmark mark='h'/> and the web, services and the cloud put the whole thing in front "
            "of people. <bookmark mark='i'/> Beside the stack stand two columns: the limits, what no machine can "
            "compute or keep secret, and the practice, how people build such things together. "
            "<bookmark mark='j'/> And in Part 55 we asked whether any of it could be trusted, and watched a "
            "compiler lie about itself, and a second compiler catch it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dim))
            self.play(*up(0))
            for i, mk in enumerate("abcdefgh", 1):
                vo.wait_until(mk)
                self.play(*up(i), run_time=0.8)
            vo.wait_until("i")
            self.play(Transform(dim.column["limits"][0], lit.column["limits"][0]),
                      Transform(dim.column["practice"][0], lit.column["practice"][0]), FadeIn(cols))
            vo.wait_until("j")
            self.play(FadeIn(trust), Indicate(dim, color=HEAD, scale_factor=1.03), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        head = label(r"The ledger, \ every row", font_size=36).to_edge(UP, buff=0.3)
        tab = ledger_table(LED, shown=len(LED), lo=-2.5, hi=5.5, font_size=20, row_h=0.24,
                           label_width=4.8).scale(0.8).move_to(
            UP * 0.4)
        for r in tab.rows:
            r.value.set_opacity(0)
        hi = VGroup(SurroundingRectangle(tab.rows[0], color=HEAD, buff=0.04, stroke_width=1.5),
                    SurroundingRectangle(tab.rows[-1], color=HEAD, buff=0.04, stroke_width=1.5))
        hrs = SLOWEST["seconds"] / 3600
        notes = VGroup(
            label(rf"first: \ Part {FIRST['part']}'s single-cycle Pebble, \ {FIRST['seconds']:.0f} s; \ "
                  rf"slowest: \ Part {SLOWEST['part']}'s $\lambda$-core, \ {hrs:.1f} hours", font_size=19,
                  color=GREY_A),
            label(rf"last: \ Part {LAST['part']}'s word-counting unit, \ {1000 * LAST['seconds']:.1f} ms, \ "
                  r"if the text arrives a byte a cycle", font_size=19, color=HEAD),
            label(rf"{NATIVE} rows timed natively on this machine; \ the others computed by the series' own machines "
                  r"and simulators", font_size=17, color=GREY_B),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.22)
        with self.voiceover(
            "The Job kept score the whole way: count the words of the thirty novels, and list the twenty most "
            f"common. <bookmark mark='a'/> Here is every row of the ledger, {say(len(LED))} of them, on a scale where "
            f"each step is a factor of ten. Part 6's single-cycle Pebble needed {say(FIRST['seconds'])} seconds. "
            f"<bookmark mark='b'/> Part {say(SLOWEST['part'])}'s lambda-calculus machine took {say_dec(hrs)} hours, "
            "and caches, compilers, hash tables, kernels, networks and clusters pushed the bar back and forth. "
            f"<bookmark mark='c'/> The last row is Part 60's word-counting circuit: about "
            f"{say(1000 * LAST['seconds'])} milliseconds, if the text arrives a byte every cycle. Most rows are "
            "computed by the machines the series built; a few were timed natively on this one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), *[FadeIn(r.name) for r in tab.rows])
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r.bar, LEFT), r.value.animate.set_opacity(1))
                                    for r in tab.rows], lag_ratio=0.25), run_time=5.0)
            self.play(Create(hi[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            slow = next(r for r in tab.rows if r.data is SLOWEST)
            self.play(Indicate(slow.bar, color=NO, scale_factor=1.05))
            vo.wait_until("c")
            self.play(Create(hi[1]), FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def speedup(self):
        head = label(r"First row against last", font_size=36).to_edge(UP, buff=0.3)
        p0, p1 = FIRST["part"], LAST["part"]
        e1 = MathTex(r"S", r"=", rf"\frac{{t_{{{p0}}}}}{{t_{{{p1}}}}}", font_size=40)
        e2 = MathTex(r"S", r"=", rf"\frac{{{FIRST['seconds']:.2f}\ \mathrm{{s}}}}{{{LAST['seconds']:.6f}\ "
                                 r"\mathrm{s}}", font_size=40)
        e3 = MathTex(r"S", r"\approx", rf"{SPEEDUP:,.0f}".replace(",", "{,}"), font_size=40)
        for e in (e1, e2, e3):
            e.move_to([0, 2.3, 0])
        q = [LED[1]["part"], LED[2]["part"], LED[-2]["part"]]
        e4 = MathTex(rf"\frac{{t_{{{p0}}}}}{{t_{{{p1}}}}}", r"=",
                     rf"\frac{{t_{{{p0}}}}}{{t_{{{q[0]}}}}} \cdot \frac{{t_{{{q[0]}}}}}{{t_{{{q[1]}}}}} \cdots "
                     rf"\frac{{t_{{{q[2]}}}}}{{t_{{{p1}}}}}", r"\quad", rf"\text{{({STEPS} factors)}}", font_size=34)
        e5 = MathTex(rf"\sqrt[{STEPS}]{{S}}", r"\approx", rf"{GEO:.2f}", r"\quad",
                     r"\text{(the typical step: a geometric mean, chapter 3)}", font_size=34)
        for e in (e4, e5):
            e.move_to([0, 1.2, 0])
        # the twenty-one steps, as bars on a log scale: up is faster than the row before, down is slower
        base_y, per_decade, dx = -1.35, 0.42, 0.56
        x_start = -dx * (STEPS - 1) / 2
        base = Line([x_start - 0.4, base_y, 0], [-x_start + 0.4, base_y, 0], color=GREY_C, stroke_width=1.5)
        bars, tags = VGroup(), VGroup()
        for i, r in enumerate(RATIOS):
            hgt = abs(math.log10(r)) * per_decade
            col = YES if r >= 1 else NO
            b = Rectangle(width=0.36, height=max(hgt, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([x_start + i * dx, base_y + (hgt / 2 if r >= 1 else -hgt / 2), 0])
            bars.add(b)
            tags.add(label(rf"{LED[i + 1]['part']}", font_size=16, color=GREY_B).move_to(
                [x_start + i * dx, base_y - 1.2, 0]))
        best = label(rf"$\times${RATIOS[BEST]:,.0f}", font_size=17, color=YES).next_to(bars[BEST], UP, buff=0.08)
        worst = label(rf"$\div${1 / RATIOS[WORST]:,.0f}", font_size=17, color=NO).next_to(bars[WORST], LEFT,
                                                                                           buff=0.08)
        axis_note = label(r"each step: \ how many times faster than the row before \ (log scale)", font_size=17,
                          color=GREY_A).move_to([2.6, 0.25, 0])
        foot = label(rf"{SLOWER} of the {STEPS} steps went slower: \ each row changed what was measured, \ not only "
                     r"how fast it ran", font_size=19, color=WHITE).to_edge(DOWN, buff=0.3)
        b_from, b_to = LED[BEST]["part"], LED[BEST + 1]["part"]
        w_from, w_to = LED[WORST]["part"], LED[WORST + 1]["part"]
        with self.voiceover(
            "So how much faster did the series make the Job? <bookmark mark='a'/> Divide the first row by the "
            f"last: {say(FIRST['seconds'])} seconds over about {say(1000 * LAST['seconds'])} milliseconds, "
            f"<bookmark mark='b'/> a speedup of about {say(SPEEDUP)} times. <bookmark mark='c'/> That ratio is a "
            f"product of {say(STEPS)} steps, one from each row to the next, and they did not all point the same way. "
            f"<bookmark mark='d'/> {say(SLOWER).capitalize()} of them went slower, because each row changed what was "
            "measured as well as how fast it ran, adding a kernel, a network or a cluster. The largest step forward "
            f"was {say(RATIOS[BEST])}-fold, from Part {say(b_from)} to Part {say(b_to)}; the largest step back, "
            f"{say(1 / RATIOS[WORST])}-fold, from Part {say(w_from)} to Part {say(w_to)}. <bookmark mark='e'/> And "
            f"the typical step, by chapter three's rule for averaging ratios, is the {ordinal(STEPS)} root of the "
            f"total: about {say_dec(GEO, 2)} times faster, row after row."
        ) as vo:
            self.play(FadeIn(head), Write(e1))
            vo.wait_until("a")
            self.play(TransformMatchingTex(e1, e2))
            vo.wait_until("b")
            self.play(TransformMatchingTex(e2, e3))
            vo.wait_until("c")
            self.play(Write(e4), Create(base), FadeIn(axis_note), FadeIn(tags))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if r >= 1 else UP) for b, r in zip(bars, RATIOS)],
                                  lag_ratio=0.15), run_time=3.0)
            vo.wait_until("d")
            self.play(*[Indicate(b, color=NO, scale_factor=1.15) for b, r in zip(bars, RATIOS) if r < 1],
                      FadeIn(foot))
            self.play(FadeIn(best), FadeIn(worst))
            vo.wait_until("e")
            self.play(TransformMatchingTex(e4, e5))
            self.play(Indicate(e5[2], color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sky(self):
        head = label(r"Above the top floor", font_size=36).to_edge(UP, buff=0.3)
        tw = tower(lit=tuple(k for k, _ in LAYERS) + ("limits", "practice"), labels="none", height=2.3, width=1.6)
        tw.to_edge(DOWN, buff=0.45)
        slots = [(x, 2.45) for x in (-5.1, -1.7, 1.7, 5.1)] + [(x, 1.4) for x in (-3.4, 0.0, 3.4)] + \
                [(x, 0.35) for x in (-5.3, -2.7, 2.7, 5.3)]
        stars = VGroup()
        for i, r in enumerate(OPEN):
            x, y = slots[i % len(slots)]
            s = Star(n=5, outer_radius=0.12, color=COLS[i % 6], fill_opacity=1).move_to([x, y, 0])
            t = label(r["problem"], font_size=16, color=COLS[i % 6]).next_to(s, DOWN, buff=0.08)
            if t.width > 2.7:
                t.width = 2.7
            stars.add(VGroup(s, t))
        with self.voiceover(
            "At the top of the tower the floors stop, and the sky of chapter nine begins: <bookmark mark='a'/> P "
            "against NP, one-way functions, the exponent of matrix multiplication, the sixth Busy Beaver, and the "
            "rest, each met somewhere on the way up. <bookmark mark='b'/> Hilbert hoped that one procedure could "
            "settle every such question. Turing's answer means that no machine ever will, so this sky will never "
            "be empty: there will always be a question for someone to start on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tw, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in stars], lag_ratio=0.2), run_time=3.5)
            vo.wait_until("b")
            self.play(*[Indicate(s[0], scale_factor=1.6) for s in stars])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stone(self):
        small = pebble(0.13, seed=3).move_to(DOWN * 2.6)
        big = pebble(1.15, seed=3).move_to(UP * 0.5)
        word = label(r"\textit{calculus}", font_size=40, color=HEAD).next_to(big, DOWN, buff=0.5)
        gloss = label(r"Latin: \ a small stone", font_size=24, color=GREY_A).next_to(word, DOWN, buff=0.2)
        with self.voiceover(
            "Every floor of that tower, and every star above it, began the way Part 1 did: <bookmark mark='a'/> "
            "with a small stone, moved by a rule. The Romans called such a stone a calculus. "
            "<bookmark mark='b'/> It is still the smallest thing a computer is made of: a mark that is either "
            "there or not, moved one rule at a time."
        ) as vo:
            self.play(FadeIn(small, scale=0.5))
            vo.wait_until("a")
            self.play(ReplacementTransform(small, big), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(word), FadeIn(gloss))
        self.wait(3.0)


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
