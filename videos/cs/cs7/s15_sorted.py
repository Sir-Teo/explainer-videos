from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt,
                                  load, mono)


class Sorted(VoiceoverScene):
    def construct(self):
        self.card()
        self.puzzle()
        self.host()
        self.pebble()
        self.branchless()

    def card(self):
        card = chapter_card(14, r"The sorted-array puzzle", r"Why does sorting the data make a loop faster?",
                            lit=(2012,), extra=((2012, r"the sorted-array question"),), part=PART)
        with self.voiceover("Chapter fourteen. The sorted-array puzzle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def puzzle(self):
        head = label(r"The same loop, \ the same data, \ in a different order", font_size=34).to_edge(UP, buff=0.35)
        code = VGroup(*[mono(t, 22) for t in ("for (i = 0; i < n; i++)", "    if (data[i] >= 128)",
                                              "        sum += data[i];")]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        code.move_to(UP * 2.0)
        rng = np.random.default_rng(2)
        vals = rng.integers(0, 256, 40)
        def strip(v, y):
            return VGroup(*[Rectangle(width=0.2, height=0.05 + 1.0 * x / 255, stroke_width=0,
                                      fill_color=YES if x >= 128 else GREY_C, fill_opacity=0.8).move_to(
                [-4.3 + 0.22 * k, y + (0.05 + 1.0 * x / 255) / 2, 0]) for k, x in enumerate(v)])
        a = strip(vals, -0.55)
        b = strip(np.sort(vals), -2.55)
        la = label(r"random: \ the branch is a coin toss", font_size=22, color=NO).next_to(a, DOWN, buff=0.15)
        lb = label(r"sorted: \ not taken, \ then taken, \ for good", font_size=22, color=YES).next_to(b, DOWN,
                                                                                                buff=0.15)
        so = label(r"Stack Overflow, \ 2012: \ the site's most famous question", font_size=20, color=HIST).next_to(
            code, DOWN, buff=0.35)
        with self.voiceover(
            "In 2012 someone asked on Stack Overflow why this loop ran six times faster after the array was sorted. It "
            "became the most famous question the site has ever had. <bookmark mark='a'/> The loop adds up the elements "
            "of an array of bytes that are at least a hundred and twenty-eight. Sorting changes nothing about the work: "
            "the same elements, the same additions. <bookmark mark='b'/> It changes the branch. On random data, whether "
            "each element passes the test is a coin toss, and no predictor can learn a coin. <bookmark mark='c'/> On "
            "sorted data, the branch goes one way for the first half of the array and the other way for the second "
            "half, and even a two-bit counter gets it almost always right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), FadeIn(so))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in a], lag_ratio=0.02), FadeIn(la), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in b], lag_ratio=0.02), FadeIn(lb), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def host(self):
        h = load("sorted")["host"]
        head = label(r"Measured on the machine that made this video", font_size=34).to_edge(UP, buff=0.35)
        cpu = label(rf"{h['cpu']}; \ C, \ {h['n']:,} bytes $\times$ {h['reps']} passes".replace(",", "{,}"),
                    font_size=20, color=GREY_B).next_to(head, DOWN, buff=0.2)
        items = [("random", h["random"], NO), ("sorted", h["sorted"], YES)]
        scale = 7.0 / max(v for _, v, _ in items)
        bars = VGroup()
        for k, (n, v, c) in enumerate(items):
            y = 0.7 - 1.1 * k
            r = Rectangle(width=v * scale, height=0.6, stroke_width=0, fill_color=c, fill_opacity=0.65).move_to(
                [-3.2 + v * scale / 2, y, 0])
            nl = label(n, font_size=24, color=c).next_to(r, LEFT, buff=0.2).align_to([-3.4, 0, 0], RIGHT)
            vl = label(rf"{v * 1e3:.1f} ms", font_size=22, color=GREY_A).next_to(r, RIGHT, buff=0.15)
            bars.add(VGroup(nl, r, vl))
        res = VGroup(
            label(rf"{h['ratio']:.1f} times faster, \ sorted", font_size=32, color=HEAD),
            label(r"a modern core loses 15 to 20 cycles per mispredicted branch, \\ and could have run several "
                  r"instructions in each \ (Part 8)", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is the experiment, run in C on the machine that computed this video. <bookmark mark='a'/> Thirty-two "
            "thousand random bytes, summed three hundred times: forty-four milliseconds. The same bytes sorted: under "
            "six. <bookmark mark='b'/> Sorting made the loop more than seven times faster, purely through branch "
            "prediction. A modern core's pipeline is deep, and it runs several instructions per cycle, which Part 8 "
            "explains, so each misprediction throws away fifteen or twenty cycles in which it could have done dozens of "
            "instructions' work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cpu))
            vo.wait_until("a")
            for b in bars:
                self.play(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pebble(self):
        p = load("sorted")["pebble"]
        head = label(r"And on Pebble's pipeline", font_size=36).to_edge(UP, buff=0.35)
        rows = VGroup()
        for k, n in enumerate(("random", "sorted")):
            v = p[n]
            rows.add(label(rf"{n}: \ {fmt(v['cycles'])} cycles, \ CPI {v['cpi']:.2f}, \ {fmt(v['mispredicts'])} "
                           rf"mispredictions", font_size=26, color=NO if k == 0 else YES))
        rows.arrange(DOWN, buff=0.35).move_to(UP * 0.8)
        ratio = p["random"]["cycles"] / p["sorted"]["cycles"]
        res = VGroup(
            label(rf"only {ratio:.2f} times faster: \ a mistake costs Pebble 2 cycles, \ not 20", font_size=26,
                  color=HEAD),
            label(r"the deeper and wider the machine, \ the more a predictable branch is worth", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 1.3)
        with self.voiceover(
            "On Pebble's five-stage pipeline the same experiment, three thousand bytes summed twice, tells a milder "
            "story. <bookmark mark='a'/> On random data, three thousand mispredictions; on sorted data, fourteen. "
            "<bookmark mark='b'/> But a misprediction costs Pebble only two cycles, so sorting gains only thirteen "
            "percent. The same program, the same predictions, and a seven-fold difference on one machine against a "
            "thirteen percent one on the other. The deeper and wider the processor, the more a predictable branch is "
            "worth."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def branchless(self):
        h = load("sorted")["host"]
        p = load("sorted")["pebble"]
        head = label(r"No branch, \ no misprediction", font_size=36).to_edge(UP, buff=0.35)
        code = VGroup(mono("sltiu t3, t2, 128     # 1 if small", 20), mono("addi  t3, t3, -1      # all ones if big",
                                                                            20),
                      mono("and   t3, t3, t2", 20), mono("add   a0, a0, t3      # adds x, or 0", 20)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(UP * 1.5)
        res = VGroup(
            label(rf"this machine: \ {h['random_branchless'] * 1e3:.1f} ms random, \ {h['sorted_branchless'] * 1e3:.1f} ms "
                  r"sorted: \ the order no longer matters", font_size=24, color=YES),
            label(rf"Pebble: \ {fmt(p['random, branchless']['cycles'])} cycles either way: \ more instructions, \ and "
                  r"its cheap mistakes were worth less", font_size=24, color=GREY_A),
            label(r"compilers emit conditional moves \ (\texttt{cmov}); \ databases, \ video codecs \ and trading "
                  r"systems \\ write branch-free inner loops on purpose", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.28).move_to(DOWN * 1.2)
        with self.voiceover(
            "If a branch cannot be predicted, remove it. <bookmark mark='a'/> The comparison produces a one or a zero; "
            "subtracting one turns that into a mask of all zeros or all ones; and-ing the mask with the element gives "
            "the element or nothing, which is simply added. No branch, so nothing to mispredict. "
            "<bookmark mark='b'/> On the Xeon, the branch-free loop takes eleven milliseconds whichever order the data is "
            "in: slower than the lucky sorted case, four times faster than the random one. On Pebble it is a little "
            "slower in both cases, because it runs more instructions and Pebble's mistakes were cheap. "
            "<bookmark mark='c'/> Real processors have conditional-move instructions for exactly this, compilers use "
            "them when they can prove it safe, and the inner loops of databases, video codecs and trading systems are "
            "often written without branches on purpose."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in code], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
            vo.wait_until("c")
            self.play(FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()
