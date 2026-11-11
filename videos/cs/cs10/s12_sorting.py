from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from explainer.cs.pebble import parallel as Pa
from videos.cs.cs10.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, grid_table, load,
                                   wire_diagram)


class Sorting(VoiceoverScene):
    def construct(self):
        self.card()
        self.comparator()
        self.bitonic()
        self.principle()
        self.checked()
        self.limits()

    def card(self):
        card = chapter_card(11, r"Sorting networks", r"Can a fixed wiring of comparisons sort anything?",
                            lit=(1968, 1983), extra=((1968, r"Batcher"), (1983, r"Ajtai, \ Koml\'os, \ "
                                                                                r"Szemer\'edi")), part=PART)
        with self.voiceover("Chapter eleven. Sorting networks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def comparator(self):
        head = label(r"A comparator, \ and a network", font_size=34).to_edge(UP, buff=0.35)
        w1 = Line(LEFT * 2 + UP * 0.8, RIGHT * 2 + UP * 0.8, color=GREY_B, stroke_width=2.5)
        w2 = Line(LEFT * 2 + DOWN * 0.2, RIGHT * 2 + DOWN * 0.2, color=GREY_B, stroke_width=2.5)
        comp = VGroup(Line(UP * 0.8, DOWN * 0.2, color=DATA, stroke_width=4), Dot(UP * 0.8, color=DATA, radius=0.09),
                      Dot(DOWN * 0.2, color=DATA, radius=0.09))
        g = VGroup(w1, w2, comp).shift(LEFT * 2.5 + UP * 0.6)
        ins = VGroup(Text("7", font="DejaVu Sans Mono", font_size=24).next_to(w1, LEFT, buff=0.15),
                     Text("3", font="DejaVu Sans Mono", font_size=24).next_to(w2, LEFT, buff=0.15))
        outs = VGroup(Text("3", font="DejaVu Sans Mono", font_size=24, color=YES).next_to(w1, RIGHT, buff=0.15),
                      Text("7", font="DejaVu Sans Mono", font_size=24, color=YES).next_to(w2, RIGHT, buff=0.15))
        cl = label(r"smaller up, \ larger down", font_size=20, color=DATA).next_to(g, DOWN, buff=0.25)
        pts = VGroup(
            label(r"a \textit{sorting network}: \ a fixed list of comparators, \ chosen before seeing any data",
                  font_size=22, color=GREY_A),
            label(r"comparators on different wires run at once: \ \textit{depth} is the parallel time", font_size=22,
                  color=DATA),
            label(r"data-oblivious: \ the same operations on every input", font_size=22, color=YES),
            label(r"so: \ hardware, \ SIMD registers, \ GPUs, \ and constant-time cryptography", font_size=22,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            (
            "Sorting is the next test of parallel thinking, and its parallel form is beautiful. <bookmark "
            "mark='a'/> The building block is a comparator: two wires in, and out come the same two values, the "
            "smaller on top and the larger below. <bookmark mark='b'/> A sorting network is a fixed list of "
            "comparators, chosen before seeing any data, that sorts every input. <bookmark mark='c'/> Comparators "
            "on different wires can work at the same moment, so a network's depth, its number of layers, is its "
            "parallel time. <bookmark mark='d'/> And because it does the same operations whatever the data, a "
            "network suits hardware, SIMD registers and GPUs, where branches are expensive, and some "
            "constant-time cryptographic code. A fixed comparison pattern helps, but comparators, memory accesses "
            "and the surrounding implementation must also avoid secret-dependent timing."
        )
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Create(w1), Create(w2), FadeIn(comp), FadeIn(ins), run_time=0.6)
            vo.wait_until('a')
            self.play(TransformFromCopy(ins, outs), FadeIn(cl))
            for mk, p in zip("bcd", pts[:3]):
                vo.wait_until(mk)
                self.play(FadeIn(p))
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bitonic(self):
        sn = load("sortnet")["bitonic8"]
        layers = [[tuple(c) for c in l] for l in sn["layers"]]
        head = label(r"Batcher's bitonic sorter, \ 8 wires", font_size=34).to_edge(UP, buff=0.3)
        wd = wire_diagram(8, layers, x0=-5.2, y0=1.9, dy=0.55, dx=0.36, gap=0.3)
        xs = [5, 2, 7, 1, 8, 3, 6, 4]
        vals = [Text(str(v), font="DejaVu Sans Mono", font_size=20, color=WHITE).next_to(wd.wires[i], LEFT,
                                                                                         buff=0.15)
                for i, v in enumerate(xs)]
        cur = list(xs)
        stage = [r"sort pairs", r"merge into fours", r"", r"merge into eights", r"", r""]
        cap = label(rf"{sum(len(l) for l in layers)} comparators, \ depth {len(layers)}: \ "
                    r"$\frac12 \log_2 n\,(\log_2 n + 1)$ layers", font_size=22, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is one of the classic designs, Kenneth Batcher's bitonic sorter from 1968, on eight wires. "
            "<bookmark mark='a'/> Watch eight numbers pass through it, one layer at a time. The first layer sorts "
            "pairs. The next two merge pairs into sorted fours: the first of them compares mirror images, the "
            "second neighbours. The last three merge the fours into a sorted eight. <bookmark mark='b'/> "
            "Twenty-four comparators in six layers. In general, the depth grows as the square of log n: for a "
            "thousand and twenty-four wires, fifty-five layers."
        ) as vo:
            self.play(FadeIn(head), Create(wd.wires), *[FadeIn(v) for v in vals])
            vo.wait_until("a")
            for k, l in enumerate(layers):
                self.play(FadeIn(wd.comps[k]), run_time=0.5)
                nxt = Pa.apply(l, cur)
                x = wd.comps[k].get_right()[0] + 0.12
                new = [Text(str(v), font="DejaVu Sans Mono", font_size=18,
                            color=YES if k == len(layers) - 1 else GREY_A).move_to([x + 0.1, wd.wires[i].get_y() + 0.18,
                                                                                    0])
                       for i, v in enumerate(nxt)]
                self.play(*[FadeIn(t) for t in new], run_time=0.6)
                cur = nxt
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def principle(self):
        head = label(r"The 0--1 principle", font_size=36).to_edge(UP, buff=0.3)
        thm = label(r"if a network sorts every input of 0s and 1s, \ it sorts every input", font_size=28,
                    color=HEAD).next_to(head, DOWN, buff=0.35)
        steps = VGroup(
            label(r"for any rising function $f$: \ $\min(f(a), f(b)) = f(\min(a, b))$, \ and the same for $\max$",
                  font_size=22, color=GREY_A),
            label(r"so a comparator commutes with $f$, \ and so does the whole network: \ $N(f(x)) = f(N(x))$",
                  font_size=22, color=GREY_A),
            label(r"suppose $N$ fails on some $x$: \ outputs $y_i > y_{i+1}$ for some $i$", font_size=22, color=NO),
            label(r"take $f(v) = 1$ if $v \ge y_i$, \ else 0: \ then $N(f(x)) = f(y)$ has a 1 above a 0", font_size=22,
                  color=NO),
            label(r"so $N$ fails on the 0--1 input $f(x)$ too. \quad $\blacksquare$", font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(thm, DOWN, buff=0.45)
        gain = label(r"to check $n$ wires: \ $2^n$ inputs instead of $n!$", font_size=26, color=YES).to_edge(DOWN,
                                                                                                         buff=0.35)
        with self.voiceover(
            "How do you know a network sorts every input? There are n factorial orders to try. The shortcut, proved "
            "in Knuth's Art of Computer Programming, is the zero-one principle. <bookmark mark='a'/> If a network sorts every input made of zeros and "
            "ones, it sorts every input at all. The proof is four lines. <bookmark mark='b'/> Take any rising "
            "function f. Applying f and then taking the smaller of two values is the same as taking the smaller and "
            "then applying f. <bookmark mark='c'/> So f passes through each comparator, and through the whole "
            "network. <bookmark mark='d'/> Now suppose the network fails on some input: somewhere in the output, a "
            "larger value y i sits above a smaller one. <bookmark mark='e'/> Let f send everything at least y i to "
            "one and everything smaller to zero. The network's output on f of x is f of its output on x, which has a "
            "one above a zero. <bookmark mark='f'/> So the network also fails on an input of zeros and ones. "
            "<bookmark mark='g'/> To check a network on n wires, two to the n inputs suffice, instead of n factorial."
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(thm), run_time=0.6)
            vo.wait_until('a')
            for mk, s in zip("bcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s, shift=RIGHT * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(gain))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def checked(self):
        sn = load("sortnet")
        rows = sn["rows"]
        head = label(r"Every network checked, \ $n$ up to 10", font_size=34).to_edge(UP, buff=0.3)
        hdr = [r"$n$", r"$2^n$", r"$n!$", r"insertion", r"Batcher", r"best known"]
        body = []
        for r in rows:
            b = r["batcher"]
            body.append([str(r["n"]), f"{r['inputs_01']:,}", f"{r['permutations']:,}",
                         rf"{r['insertion']['size']} \ / \ {r['insertion']['depth']}",
                         rf"{b['size']} \ / \ {b['depth']}", rf"{r['best_size']} \ / \ {r['best_depth']}"])
        colors = [[GREY_A, YES, GREY_B, GREY_A, DATA, HEAD]] * len(body)
        t = grid_table(hdr, body, [0.8, 1.3, 1.9, 2.0, 2.0, 2.3], row_h=0.36, font_size=19, colors=colors,
                       mono_cols=()).move_to(UP * 0.1 + LEFT * 0.3)
        cap = note(r"size \ / \ depth; \ both networks built here sort all $2^n$ 0--1 inputs \ (and, for $n \le 8$, \ all "
                   r"$n!$ orders); \ best known: \ Knuth 5.3.4, \ optimal sizes for $n \le 10$ proved by computer "
                   r"search \ (Codish et al., \ 2014)", font_size=16).to_edge(DOWN, buff=0.85)
        br = sn["broken"]
        bad = label(rf"remove one comparator from Batcher's network for 8, \ wires {br['removed'][0]}--"
                    rf"{br['removed'][1]}: \ the 0--1 input {''.join(map(str, br['input']))} comes out "
                    rf"{''.join(map(str, br['output']))}", font_size=20, color=NO).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            (
            "With the principle, we checked networks exhaustively. <bookmark mark='a'/> For ten wires, one "
            "thousand and twenty-four inputs instead of three point six million orders. For each n up to ten we "
            "built two networks: the insertion network, which mimics insertion sort, and Batcher's odd-even merge "
            "network. Both sort all zero-one inputs, and the Batcher networks through eight wires were separately "
            "checked on every permutation. Beside them, the smallest sizes and depths known. <bookmark mark='b'/> "
            "That column is a research story of its own: the remaining nine- and ten-wire minimum-size cases were "
            "proved optimal in the 2014 work, by a computer search that relied on this same principle. <bookmark "
            "mark='c'/> And the principle catches mistakes. Remove a single comparator from Batcher's network for "
            "eight wires, and the check immediately produces a zero-one input it fails to sort."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.2),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(cap), *[Indicate(t.cells[r][5], color=HEAD) for r in range(1, len(t.cells))])
            vo.wait_until("c")
            self.play(FadeIn(bad))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        big = load("sortnet")["big"]
        head = label(r"How shallow can a sorting network be?", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            wrapped_label(rf"1024 wires: \ bitonic {big['1024']['bitonic_size']:,}, \ odd-even merge "
                          rf"{big['1024']['oem_size']:,} comparators; \ both depth {big['1024']['oem_depth']}",
                          12.0, font_size=22, color=DATA),
            label(r"Ajtai, \ Koml\'os and Szemer\'edi \ (1983): \ depth $O(\log n)$ \ is possible", font_size=22,
                  color=HEAD),
            label(r"asymptotic optimality does not make AKS the practical default", font_size=22,
                  color=NO),
            label(r"in practice: \ bitonic networks in GPU sorts and in SIMD registers, \ merge sort around them",
                  font_size=22, color=YES),
            label(r"17 wires: \ depth 10 proved optimal \ (Ehlers and M\"uller, \ 2015)",
                  font_size=22, color=FUNC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.1)
        with self.voiceover(
            (
            "How fast can a network sort? <bookmark mark='a'/> Batcher's networks have depth on the order of log "
            "n squared: for a thousand and twenty-four wires, fifty-five layers; the bitonic construction here "
            "has exactly twenty-eight thousand one hundred and sixty comparators. <bookmark mark='b'/> In 1983 "
            "Miklós Ajtai, János Komlós and Endre Szemerédi proved that depth on the order of log n is possible, "
            "which is optimal. <bookmark mark='c'/> But the constant in their construction is so large that the "
            "asymptotic construction is not the practical default for ordinary problem sizes. <bookmark "
            "mark='d'/> So in practice, GPU sorting libraries and SIMD sorting routines use bitonic networks for "
            "small blocks, inside a merge sort. <bookmark mark='e'/> And the smallest exact questions are still "
            "open: even small optimality questions require substantial search. Seventeen-wire depth ten is proved "
            "optimal in the cited Ehlers and Mueller work; our exhaustive checks cover only the small networks "
            "listed in this chapter."
        )
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, p in zip('abcde', pts):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1), run_time=0.6 if mk == 'a' else 1.0)
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()
