from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load


class Hook(VoiceoverScene):
    def construct(self):
        self.race()
        self.preview()
        self.plan()

    def race(self):
        lp = load("loops")
        p = load("passes")
        head = label(r"Who writes the faster loop?", font_size=36).to_edge(UP, buff=0.3)
        hand = code(["word:  mv   t0, s0          # the table", "       li   a2, 0", "scan:  beq  a2, s1, insert",
                     "       lw   t1, 4(t0)       # same length?", "       bne  t1, a1, next", "       ...",
                     "next:  addi t0, t0, 12      # step to the next entry", "       addi a2, a2, 1",
                     "       j    scan"], size=15).to_edge(LEFT, buff=0.5).shift(UP * 0.4)
        hl = label(r"Part 6: \ written by hand", font_size=20, color=DATA).next_to(hand, UP, buff=0.15).align_to(
            hand, LEFT)
        src = code(["while i < entries {", "    if table[i].length == n {", "        ...", "    }", "    i = i + 1;",
                    "}"], size=15, color=YES).to_edge(RIGHT, buff=0.6).shift(UP * 1.7)
        sl = label(r"the same loop, \ in the Pebble language", font_size=20, color=YES).next_to(src, UP, buff=0.15)
        sl.align_to(src, LEFT)
        asm = lp["asm"]["with"]

        def after(lab, n):
            k = asm.index(lab + ":")
            return [asm[k]] + ["    " + l for l in asm[k + 1:k + 1 + n]]
        loop = after("word.body5", 2) + ["    ..."] + after("word.endif12", 2) + after("word.latch6", 1)
        comp = code(loop, size=14, color=CODE).next_to(src, DOWN, buff=0.45).align_to(src, LEFT)
        cl = label(r"what our compiler writes from it", font_size=18, color=FUNC).next_to(comp, UP, buff=0.08)
        cl.align_to(comp, LEFT)
        rows = p["rows"]
        res = VGroup(
            label(rf"on the first chapter of \textit{{Pride and Prejudice}}: \ by hand \ {p['hand']:,} instructions",
                  font_size=24, color=DATA),
            label(rf"compiled, \ no optimization: \ {rows[0]['array']:,}", font_size=24, color=NO),
            label(rf"compiled, \ optimized: \ {rows[-1]['array']:,} \ --- \ "
                  rf"{100 * (1 - rows[-1]['array'] / p['hand']):.0f}\% fewer than by hand", font_size=24, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In Part 6 we wrote the Job's inner loop by hand, in Pebble assembly. <bookmark mark='a'/> Each table "
            "entry is twelve bytes, so the loop keeps a pointer and steps it by twelve. <bookmark mark='b'/> In Part "
            "12 we wrote the same loop in the Pebble language, as you would in C: an index, and the table indexed by "
            "it. <bookmark mark='c'/> This is what our compiler, built in this part, turns it into. It found the "
            "pointer by itself. <bookmark mark='d'/> On the first chapter of Pride and Prejudice, the hand-written "
            "program executes eight hundred and twenty-eight thousand instructions. Compiled with no optimization, "
            "the same algorithm takes four and a half million. Optimized, seven hundred and thirty thousand: twelve "
            "percent fewer than we managed by hand."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hand), FadeIn(hl))
            self.play(Indicate(hand[6], color=DATA))
            vo.wait_until("b")
            self.play(FadeIn(src), FadeIn(sl))
            vo.wait_until("c")
            self.play(FadeIn(comp), FadeIn(cl))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.5), run_time=3)
        self.wait(0.3)
        self.clear_scene()

    def preview(self):
        head = label(r"By the end of this part", font_size=40).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"a whole compiler: \ from the syntax tree to Pebble machine code", font_size=27, color=DATA),
            label(r"the program as a graph: \ dominators, \ SSA, \ dataflow and fixed points", font_size=27,
                  color=CTRL),
            label(r"optimizations, \ each measured on the Job", font_size=27, color=YES),
            label(r"register allocation as graph colouring, \ and why SSA makes it easy", font_size=27, color=FUNC),
            label(r"how to know the compiler is right, \ and how to search for the best program", font_size=27,
                  color=HEAD),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is where we are going. <bookmark mark='a'/> A whole compiler, from the tree Part 12's parser "
            "builds down to Pebble machine code. <bookmark mark='b'/> The program as a graph, with dominators, the "
            "static single assignment form, and dataflow analysis as the search for a fixed point. <bookmark "
            "mark='c'/> A sequence of optimizations, each switched on in turn and measured on the Job. <bookmark "
            "mark='d'/> Register allocation as graph colouring, a hard problem in general, and the theorem that "
            "makes it easy on SSA programs. <bookmark mark='e'/> And the questions at the edge: how do we know a "
            "compiler is right, and can a machine search for the best possible program?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcde", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ The Compiler", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"FORTRAN's promise; \ front end, \ middle end, \ back end",
            r"semantic analysis; \ three-address code; \ control-flow graphs",
            r"dominators, \ SSA, \ dataflow on lattices",
            r"SCCP, \ GVN, \ LICM, \ strength reduction, \ inlining",
            r"instruction selection, \ register allocation, \ scheduling",
            r"the Job compiled; \ fuzzing, \ verification, \ superoptimization",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 13 of Computer Science, Built, in Act Three, Speaking to the Machine. <bookmark "
            "mark='a'/> In this part: FORTRAN's promise, and the shape of every compiler since. Semantic analysis, "
            "three-address code and control-flow graphs. Dominators, static single assignment, and dataflow on "
            "lattices. Constant propagation, value numbering, loop optimizations and inlining. Instruction "
            "selection, register allocation and scheduling. And the Job compiled, with fuzzing, verification and "
            "superoptimization."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
