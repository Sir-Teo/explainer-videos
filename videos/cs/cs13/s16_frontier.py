from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, mono, region)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.employment()
        self.superopt()
        self.cost()
        self.stochastic()
        self.egraph()
        self.learned()
        self.open()

    def card(self):
        card = chapter_card(15, r"Frontier: \ searching for the best program", r"Can a machine find the optimal "
                            r"code?", lit=(1987, 2009), extra=((1987, r"Massalin's superoptimizer"),
                                                               (2009, r"equality saturation")), part=PART)
        with self.voiceover("Chapter fifteen. Frontier: searching for the best program."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def employment(self):
        head = label(r"``Optimizing'' compilers do not optimize", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"they apply rules that usually help; \ nothing says the result is the best", font_size=22,
                  color=GREY_A),
            label(r"and no compiler can always find the best:", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.5)
        loop = code(["loop:  j loop"], size=24, color=YES).next_to(pts, DOWN, buff=0.5)
        why = VGroup(
            label(r"the smallest program that runs forever and prints nothing", font_size=21, color=GREY_A),
            label(r"a compiler that always found the smallest program \ would output this exactly when the input "
                  r"never halts", font_size=21, color=GREY_A),
            label(r"so it would decide the halting problem: \ impossible \ (Part 25)", font_size=22, color=NO),
            label(r"``the full employment theorem for compiler writers''", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(loop, DOWN, buff=0.4)
        with self.voiceover(
            "Despite the name, an optimizing compiler does not optimize. <bookmark mark='a'/> It applies rules "
            "that usually help, and nothing guarantees that the result is the best program possible. <bookmark "
            "mark='b'/> In fact no compiler can always find the best. Consider this program: one instruction that "
            "jumps to itself. It is the smallest program that runs forever and prints nothing. <bookmark "
            "mark='c'/> A compiler that always produced the smallest equivalent program would output exactly this "
            "whenever its input never halts, and so it would decide the halting problem. <bookmark mark='d'/> "
            "Andrew Appel calls this the full employment theorem for compiler writers: there will always be a "
            "better optimizer to build. But for short pieces of code, we can search."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]), FadeIn(loop), FadeIn(why[0]))
            vo.wait_until("c")
            self.play(FadeIn(why[1:3]))
            vo.wait_until("d")
            self.play(FadeIn(why[3]))
        self.wait(0.3)
        self.clear_scene()

    def superopt(self):
        so = load("superopt")
        head = label(r"Superoptimization: \ try every program, \ shortest first", font_size=32).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"1. \ enumerate Pebble sequences of length 1, 2, 3, ...", font_size=20, color=GREY_A),
            label(r"2. \ run each on 32 test inputs; \ discard any that differ from the target", font_size=20,
                  color=GREY_A),
            label(r"3. \ prove the survivors with z3, \ for all $2^{32}$ inputs", font_size=20, color=GREY_A),
            label(r"Massalin, \ 1987: \ found tricks no human had", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        rows, cols = [], []
        for t in so["targets"]:
            rows.append([t["name"], str(t["length"]), "; ".join(" ".join(x.split()) for x in t["program"]),
                         f"{t['seconds']:.2f} s"])
            cols.append([WHITE, YES, WHITE, GREY_B])
        tab = grid_table([r"target", r"length", r"shortest Pebble program \ (proved)", r"search"], rows,
                         widths=[2.3, 1.1, 7.4, 1.4], row_h=0.42, font_size=17, colors=cols,
                         mono_cols=(0, 2)).next_to(steps, DOWN, buff=0.35).set_x(0)
        absrow = [k for k, t in enumerate(so["targets"]) if t["name"] == "|x|"][0]
        explain = label(r"$|x|$: \ $m = x \gg 31$ \ is 0 or $-1$; \ then \ $(x + m) \oplus m$: \ for $x < 0$, \ subtract one "
                        r"and flip every bit, \ which is $-x$", font_size=19, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 1987 Henry Massalin built the first superoptimizer. <bookmark mark='a'/> Enumerate every instruction "
            "sequence of length one, then two, then three. Run each on a few dozen test inputs, and throw away any "
            "that disagrees with the target function. <bookmark mark='b'/> Then prove the survivors correct for "
            "every input. Massalin checked his mostly by hand; we can ask z3. <bookmark mark='c'/> Ours finds "
            "the shortest Pebble programs for these small functions. Is x nonzero: one instruction. Is x equal to "
            "y: two. Clear the lowest set bit: two. <bookmark mark='d'/> Absolute value without a branch: three. "
            "Shift right by thirty-one, which gives zero or minus one; add it; exclusive-or with it. For a negative "
            "x, that subtracts one and flips every bit, which is negation. Signed division by two, correct for "
            "negative numbers: three. And the minimum of two numbers, with no branch: four, using a multiply."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[:2]))
            vo.wait_until("b")
            self.play(FadeIn(steps[2:]))
            vo.wait_until("c")
            self.play(FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]])
            for r in tab.cells[1:5]:
                self.play(*[FadeIn(c) for c in r], run_time=0.5)
            vo.wait_until("d")
            for r in tab.cells[5:]:
                self.play(*[FadeIn(c) for c in r], run_time=0.5)
            self.play(Indicate(VGroup(*tab.cells[absrow + 1]), color=HEAD), FadeIn(explain))
        self.wait(0.3)
        self.clear_scene()

    def cost(self):
        so = load("superopt")
        head = label(r"The price: \ exponential", font_size=34).to_edge(UP, buff=0.3)
        best = {}
        for t in so["targets"]:
            best[t["length"]] = max(best.get(t["length"], 0), t["seconds"])
        ks = sorted(best)
        ch = VGroup()
        ax = Axes(x_range=[0.5, 4.5, 1], y_range=[0, 6, 1], x_length=5.5, y_length=4.0,
                  axis_config={"color": GREY_D, "include_ticks": True},
                  y_axis_config={"include_numbers": False}).move_to(LEFT * 2.6 + DOWN * 0.3)
        ylab = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(0.5, y), LEFT, buff=0.1)
                        for y, t in ((1, r"10 ms"), (3, r"1 s"), (5, r"100 s"))])
        xlab = VGroup(*[label(str(k), font_size=16, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.1)
                        for k in ks])
        xt = label(r"program length", font_size=17, color=GREY_B).next_to(ax, DOWN, buff=0.45)
        import math
        dots = VGroup(*[Dot(ax.c2p(k, 3 + math.log10(best[k])), color=NO, radius=0.08) for k in ks])
        line = VMobject(color=NO, stroke_width=2).set_points_as_corners([d.get_center() for d in dots])
        vals = VGroup(*[label(f"{best[k]:.3f} s" if best[k] < 1 else f"{best[k]:.0f} s", font_size=15,
                              color=NO).next_to(dots[i], UP + LEFT * 0.3, buff=0.1) for i, k in enumerate(ks)])
        side = VGroup(
            label(r"each instruction: \ about 20 operations $\times$ every pair of registers so far", font_size=19,
                  color=GREY_A),
            label(r"so each extra instruction multiplies the search by hundreds", font_size=19, color=GREY_A),
            label(r"pruning helps: \ skip any value already computed \ (observational equivalence)", font_size=19,
                  color=GREY_A),
            label(r"but brute force stops at about 5 instructions", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The catch is the cost. <bookmark mark='a'/> The longest search at each length: a few milliseconds for "
            "one instruction, under a second for three, and four minutes for the four-instruction minimum, on a "
            "logarithmic scale. <bookmark mark='b'/> Each new instruction can be any of twenty operations, on any "
            "pair of the registers computed so far, so each extra instruction multiplies the search by hundreds. "
            "Pruning helps: a sequence whose new value was already computed some shorter way is skipped. But brute "
            "force runs out at about five instructions, far short of a whole function."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(ylab), FadeIn(xlab), FadeIn(xt))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.4), Create(line), FadeIn(vals),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in side], lag_ratio=0.6), run_time=5)
        self.wait(0.3)
        self.clear_scene()

    def stochastic(self):
        head = label(r"Smarter search", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(label(r"STOKE", font_size=24, color=YES),
                   label(r"Schkufza, Sharma, Aiken, \ 2013", font_size=18, color=GREY_B),
                   label(r"a random walk over x86 programs (Markov chain Monte Carlo), \ cost $=$ wrongness on "
                         r"tests $+$ estimated time;", font_size=19, color=GREY_A),
                   label(r"found loops faster than \texttt{gcc -O3} and as fast as expert assembly", font_size=19,
                         color=GREY_A)),
            VGroup(label(r"Souper", font_size=24, color=CTRL),
                   label(r"Sasnauskas, Regehr et al., \ 2017", font_size=18, color=GREY_B),
                   label(r"synthesizes small replacements for pieces of LLVM IR with an SMT solver;",
                         font_size=19, color=GREY_A),
                   label(r"its finds are reported as missing optimizations, \ and many were added to LLVM",
                         font_size=19, color=GREY_A)),
            VGroup(label(r"AlphaDev", font_size=24, color=FUNC),
                   label(r"Mankowitz et al., \ 2023", font_size=18, color=GREY_B),
                   label(r"reinforcement learning over assembly for sorting 3 to 5 numbers;", font_size=19,
                         color=GREY_A),
                   label(r"shorter routines, \ merged into LLVM's C++ library", font_size=19, color=GREY_A)),
        )
        for r in rows:
            r[0].move_to([-5.4, 0, 0], aligned_edge=LEFT)
            top = VGroup(r[1], r[2], r[3]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            top.move_to([-3.2, 0, 0], aligned_edge=LEFT)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.5)
        for r in rows:
            r[0].set_x(-5.4 + r[0].width / 2)
            VGroup(r[1], r[2], r[3]).set_x(-3.2 + VGroup(r[1], r[2], r[3]).width / 2)
        with self.voiceover(
            "Smarter search goes further. <bookmark mark='a'/> STOKE, from Stanford in 2013, takes a random walk "
            "through the space of x86 programs. Each step changes one instruction, and a step is kept with a "
            "probability that depends on a cost: how wrong the program is on the tests, plus how slow it is "
            "estimated to be. Walking downhill, mostly, it found loop bodies faster than gcc at its highest level, "
            "and as fast as expert hand-written assembly. <bookmark mark='b'/> Souper, from 2017, uses an SMT "
            "solver to synthesize smaller replacements for pieces of LLVM IR, and reports what it finds as "
            "optimizations the compiler is missing. Many have since been added to LLVM by hand. <bookmark "
            "mark='c'/> And AlphaDev, from DeepMind in 2023, used reinforcement learning to search assembly "
            "programs that sort three, four and five numbers. Its routines were shorter than the human ones, and "
            "they are now in LLVM's C++ library."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def eclass(self, items, color, title=None):
        t = VGroup(*[mono(s, 17, WHITE) for s in items]).arrange(DOWN, buff=0.14)
        box = DashedVMobject(RoundedRectangle(width=t.width + 0.5, height=t.height + 0.4, corner_radius=0.15,
                                              stroke_color=color, stroke_width=2), num_dashes=40)
        box.move_to(t)
        g = VGroup(box, t)
        if title:
            g.add(mono(title, 15, color).next_to(box, UP, buff=0.05).align_to(box, LEFT))
        g.items = t
        return g

    def egraph(self):
        head = label(r"Equality saturation: \ keep every version at once", font_size=32).to_edge(UP, buff=0.3)
        start = mono("(a * 2) * 2", 24, CODE).next_to(head, DOWN, buff=0.35)
        rules = VGroup(*[mono(r, 15, GREY_A) for r in ("x * 2  →  x << 1", "(x * y) * z  →  x * (y * z)",
                                                       "2 * 2  →  4", "x * 4  →  x << 2")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UR, buff=0.4).shift(DOWN * 0.6)
        rl = label(r"rewrite rules \ (all true mod $2^{32}$)", font_size=16, color=GREY_B).next_to(rules, UP,
                                                                                               buff=0.08)
        greedy = VGroup(label(r"one rule at a time:", font_size=19, color=NO),
                        mono("(a << 1) * 2  →  (a << 1) << 1", 16, NO),
                        label(r"two shifts, \ and associativity no longer applies", font_size=17, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_edge(LEFT, buff=0.5).shift(UP * 1.0)
        c1 = self.eclass(["a * 2", "a << 1"], CTRL, "c1")
        c4 = self.eclass(["2 * 2", "4"], CTRL, "c4")
        root = self.eclass(["c1 * 2", "c1 << 1", "a * c4", "a << 2"], YES, "root")
        root.move_to(UP * 0.0 + RIGHT * 0.6)
        c1.move_to(DOWN * 2.3 + LEFT * 1.4)
        c4.move_to(DOWN * 2.3 + RIGHT * 2.6)
        ar = VGroup(
            Arrow(root.items[0].get_left(), c1[0].get_top(), buff=0.1, color=GREY_B, stroke_width=1.6, tip_length=0.12),
            Arrow(root.items[1].get_left(), c1[0].get_top(), buff=0.1, color=GREY_B, stroke_width=1.6, tip_length=0.12),
            Arrow(root.items[2].get_right(), c4[0].get_top(), buff=0.1, color=GREY_B, stroke_width=1.6,
                  tip_length=0.12),
        )
        best = SurroundingRectangle(root.items[3], color=HEAD, buff=0.06)
        notes = VGroup(
            label(r"an \textbf{e-graph}: \ each dashed class holds expressions known to be equal", font_size=19,
                  color=GREY_A),
            label(r"apply every rule everywhere, \ until nothing new appears; \ then extract the cheapest",
                  font_size=19, color=GREY_A),
            label(r"no phase-ordering problem: \ nothing is ever thrown away", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.2).to_edge(RIGHT, buff=0.3)
        for n in notes:
            if n.width > 6.0:
                n.width = 6.0
        with self.voiceover(
            "A newer idea attacks the phase-ordering problem of chapter seven head on. <bookmark mark='a'/> Take a "
            "times two, times two, and four rewrite rules, all true for thirty-two-bit integers. <bookmark "
            "mark='b'/> Apply one rule at a time and the order matters. Turn the inner multiply into a shift first, "
            "and you end with two shifts; the rule that would have combined the multiplies no longer applies. "
            "<bookmark mark='c'/> Equality saturation never chooses. It keeps an e-graph, in which each class "
            "holds expressions already known to be equal. a times two and a shifted by one share a class. So do two "
            "times two, and four. <bookmark mark='d'/> The whole expression's class collects every version the "
            "rules can reach: c one times two, c one shifted by one, a times c four, and a shifted by two. Rules are "
            "applied everywhere, again and again, until nothing new appears. <bookmark mark='e'/> Then the "
            "cheapest version is extracted: a single shift by two. Tate and others introduced the idea in 2009, "
            "and the egg library of 2021 made it fast; it is now used in compilers for hardware, for "
            "floating-point accuracy, and in Cranelift, a production code generator."
        ) as vo:
            self.play(FadeIn(head), FadeIn(start))
            vo.wait_until("a")
            self.play(FadeIn(rl), FadeIn(rules))
            vo.wait_until("b")
            self.play(FadeIn(greedy))
            vo.wait_until("c")
            self.play(FadeOut(greedy), FadeIn(c1), FadeIn(c4), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(root), Create(ar), FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(Create(best), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def learned(self):
        head = label(r"Learning the heuristics", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"a compiler is full of guesses: \ inline this call? \ spill which value? \ unroll how far?",
                  font_size=21, color=GREY_A),
            label(r"\textbf{MLGO} \ (Trofin et al., \ Google, \ 2021): \ a learned inlining policy in LLVM, \ "
                  r"trained by reinforcement learning", font_size=20, color=GREY_A),
            label(r"a few percent smaller code, \ in production; \ later a learned register-eviction policy",
                  font_size=20, color=YES),
            label(r"the hard part: \ the guess must be cheap, \ and stay good when the code changes", font_size=20,
                  color=NO),
            label(r"how such policies are trained: \ \textit{AI, Built}", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "The other direction is to learn. <bookmark mark='a'/> A compiler is full of guesses. Inline this "
            "call? Spill which value? Unroll this loop how far? Each is a hand-tuned heuristic. <bookmark "
            "mark='b'/> In 2021 Google's MLGO project replaced LLVM's inlining heuristic with a small neural "
            "network, trained by reinforcement learning to make code smaller, and later did the same for which "
            "value the register allocator evicts. <bookmark mark='c'/> It saves a few percent of code size in "
            "production. <bookmark mark='d'/> The difficulties are practical: the guess must be fast, since it "
            "runs millions of times, and it must stay good as the programs being compiled change. <bookmark "
            "mark='e'/> How such policies are trained is the subject of our companion series, AI, Built."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open(self):
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.35)
        qs = VGroup(
            label(r"SSA graphs colour easily, \ but spilling and coalescing on them are NP-hard: \ what can be "
                  r"approximated, \ and how well?", font_size=21, color=GREY_A),
            label(r"extracting the cheapest program from an e-graph is NP-hard when costs are shared: \ which "
                  r"cost models are tractable?", font_size=21, color=GREY_A),
            label(r"a verified compiler as fast as \texttt{-O3}: \ CompCert performs roughly like \texttt{gcc -O1}",
                  font_size=21, color=GREY_A),
            label(r"superoptimizing whole loops, \ not just five instructions: \ search, \ proof, \ or learning?",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the first one", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Here is where the field stands. <bookmark mark='a'/> SSA programs colour optimally in linear time, "
            "but deciding what to spill, and which copies to coalesce, remains NP-hard even on SSA. How well can "
            "these be approximated? <bookmark mark='b'/> Extracting the cheapest program from an e-graph is "
            "NP-hard once parts can be shared; which cost models are tractable? <bookmark mark='c'/> CompCert is "
            "proved correct, but its code runs at about the speed of gcc at level one. Can a verified compiler "
            "match level three? <bookmark mark='d'/> And can we superoptimize whole loops rather than five "
            "instructions, by search, by proof, or by learning? <bookmark mark='e'/> The research problem of this "
            "part takes up the first of these."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abcd", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
