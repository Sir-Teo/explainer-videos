from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, mono)


def sched_row(rows, job, code_, pred):
    return next(r for r in rows if r["job"] == job and r["code"] == code_ and r["predictor"] == pred)


class Schedule(VoiceoverScene):
    def construct(self):
        self.card()
        self.dag()
        self.listsched()
        self.measure()
        self.predictors()
        self.swp()

    def card(self):
        card = chapter_card(12, r"Scheduling and the pipeline", r"In what order should the instructions run?",
                            lit=(1981,), extra=((1981, r"Chaitin's colouring; \ Rau's modulo scheduling"),),
                            part=PART)
        with self.voiceover("Chapter twelve. Scheduling and the pipeline."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def dag(self):
        lp = load("loops")
        asm = lp["asm"]["with"]
        k = asm.index("word.and33:")
        blk = asm[k + 1:k + 6]
        head = label(r"The dependence graph of a block", font_size=34).to_edge(UP, buff=0.3)
        lst = VGroup(*[mono(f"{j + 1}  {l}", 18, CODE) for j, l in enumerate(blk)]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).to_edge(LEFT, buff=0.8).shift(UP * 0.6)
        cap = label(r"the inner loop of \texttt{word}: \ compare one letter", font_size=19, color=GREY_B).next_to(
            lst, UP, buff=0.2).align_to(lst, LEFT)
        pos = {0: (2.0, 2.0), 1: (2.0, 0.6), 2: (4.6, 0.6), 3: (4.6, -0.8), 4: (3.3, -2.2)}
        nodes = {}
        for j, (x, y) in pos.items():
            c = Circle(radius=0.32, stroke_color=DATA, fill_color=DATA, fill_opacity=0.2).move_to([x, y, 0])
            nodes[j] = VGroup(c, mono(str(j + 1), 18, WHITE).move_to(c))
        deps = [(0, 1, r"\texttt{t3}", YES), (1, 2, r"WAR \texttt{t3}", NO), (2, 3, r"\texttt{t3}", YES),
                (3, 4, r"\texttt{t3}: \ load--use", HEAD), (1, 4, r"\texttt{a5}: \ load--use", HEAD)]
        es = VGroup()
        for a, b, t, c in deps:
            ar = Arrow(nodes[a][0].get_center(), nodes[b][0].get_center(), buff=0.34, color=c, stroke_width=2.5,
                       tip_length=0.14)
            tl = label(t, font_size=15, color=c).next_to(ar.get_center(), RIGHT if a != 1 or b != 4 else LEFT,
                                                         buff=0.1)
            if (a, b) == (1, 2):
                tl.next_to(ar, UP, buff=0.05)
            es.add(VGroup(ar, tl))
        notes = VGroup(
            label(r"edges: \ one instruction must wait for another", font_size=20, color=GREY_A),
            label(r"a load's result arrives a cycle late on Part 7's pipeline", font_size=20, color=HEAD),
            label(r"WAR: \ 3 may not overwrite \texttt{t3} before 2 has read it", font_size=20, color=NO),
            label(r"a false dependence, \ created by register allocation reusing \texttt{t3}", font_size=20,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.8)
        with self.voiceover("The last job of the back end is to choose an order for the instructions within each block. <bookmark mark='a'/> Here is the inner loop of word: compare one letter. Add, load a byte, add, load a byte, branch if equal. <bookmark mark='b'/> Draw an edge from one instruction to another when the second must wait for the first. The first add produces the address the first load uses. <bookmark mark='c'/> The branch needs both loaded bytes, and on Part 7's pipeline a load's result arrives a cycle late: a branch right after the load it depends on stalls. <bookmark mark='d'/> And one edge is different. Instruction three overwrites t three, which instruction two reads. Three must wait for two, not because of any value, but because the register allocator chose to reuse t three. A false dependence, and an example of the two phases fighting: allocate first and you constrain the schedule; schedule first and you may need more registers.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(cap), FadeIn(lst), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(*[FadeIn(n) for n in nodes.values()], FadeIn(es[0]), FadeIn(es[2]), FadeIn(notes[0]))
            vo.wait_until('c')
            self.play(FadeIn(es[3]), FadeIn(es[4]), FadeIn(notes[1]))
            vo.wait_until('d')
            self.play(FadeIn(es[1]), FadeIn(notes[2:]))
        self.wait(0.3)
        self.clear_scene()

    def listsched(self):
        head = label(r"List scheduling", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"keep a list of \textbf{ready} instructions: \ everything they wait for has been placed",
                  font_size=21, color=GREY_A),
            label(r"each cycle, \ place the ready one with the longest path to the end of the block", font_size=21,
                  color=GREY_A),
            label(r"so the critical path starts first, \ and independent work fills the gaps", font_size=21,
                  color=GREY_A),
            label(r"finding the best order is NP-hard in general; \ this greedy rule is nearly always used",
                  font_size=21, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        a = code(["add  t3, a2, s0", "lbu  a5, 0(t3)", "add  t3, t2, s0", "lbu  t3, 0(t3)", "    (stall)",
                  "beq  a5, t3, body22"], size=17)
        a[4].set_color(NO)
        b = code(["add  t3, a2, s0", "add  t4, t2, s0", "lbu  a5, 0(t3)", "lbu  t3, 0(t4)", "    (stall)",
                  "beq  a5, t3, body22"], size=17, color=YES)
        b[4].set_color(NO)
        VGroup(a, b).arrange(RIGHT, buff=1.5, aligned_edge=UP).next_to(steps, DOWN, buff=0.5).to_edge(LEFT,
                                                                                                    buff=1.2)
        al = label(r"as allocated", font_size=18, color=GREY_B).next_to(a, UP, buff=0.1).align_to(a, LEFT)
        bl = label(r"with a spare register", font_size=18, color=YES).next_to(b, UP, buff=0.1).align_to(b, LEFT)
        verdict = label(r"either way the last load feeds the branch: \ a chain of five has nothing to hide behind",
                        font_size=20, color=HEAD).next_to(VGroup(a, b), RIGHT, buff=0.5)
        if verdict.width > 4.5:
            verdict = VGroup(label(r"either way, \ the last load", font_size=20, color=HEAD),
                             label(r"feeds the branch:", font_size=20, color=HEAD),
                             label(r"a block of five", font_size=20, color=HEAD),
                             label(r"has nothing to hide behind", font_size=20, color=HEAD)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08).next_to(VGroup(a, b), RIGHT, buff=0.6)
        with self.voiceover("The standard method is list scheduling. <bookmark mark='a'/> Keep a list of the instructions that are ready, because everything they wait for has been placed. Each cycle, place the ready instruction with the longest path to the end of the block, so the critical path starts as early as possible and independent work fills the gaps. Finding the very best order is NP-hard in general, and this greedy rule is what nearly everyone uses. <bookmark mark='b'/> In our block it cannot help much. Even with a spare register, removing the false dependence, the second load must still come right before the branch that needs it. A block of five instructions in a single chain has nothing to hide the delay behind. To do better, a scheduler must look across blocks, and across loop iterations.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.5), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(a), FadeIn(al))
            self.play(FadeIn(b), FadeIn(bl))
            self.play(FadeIn(verdict))
        self.wait(0.3)
        self.clear_scene()

    def measure(self):
        s = load("sched")
        R = s["rows"]
        head = label(r"On Part 7's pipeline", font_size=34).to_edge(UP, buff=0.3)
        rows, cols = [], []
        for job, code_, name in (("hand", "hand-written", r"hand-written \ (Part 6)"),
                                 ("array", "as compiled", r"compiled, \ array"),
                                 ("array", "scheduled", r"compiled \ and scheduled"),
                                 ("list", "as compiled", r"compiled, \ list")):
            r = sched_row(R, job, code_, "not taken")
            rows.append([name, f"{r['instructions']:,}", f"{r['load_use']:,}", f"{r['flush']:,}",
                         f"{r['cycles']:,}", f"{r['cpi']:.2f}"])
            cols.append([WHITE, WHITE, WHITE, NO if job != "hand" else WHITE, WHITE, WHITE])
        tab = grid_table([r"program", r"instructions", r"load--use stalls", r"branch flushes", r"cycles", r"CPI"],
                         rows, widths=[3.4, 1.9, 2.1, 2.0, 1.7, 0.9], row_h=0.5, font_size=19, colors=cols,
                         mono_cols=()).next_to(head, DOWN, buff=0.4)
        cap = label(rf"a {s['bytes']:,}-byte passage; \ predict not taken, \ as Part 7 began", font_size=18,
                    color=GREY_B).next_to(tab, DOWN, buff=0.15)
        h = sched_row(R, "hand", "hand-written", "not taken")
        a = sched_row(R, "array", "as compiled", "not taken")
        a2 = sched_row(R, "array", "scheduled", "not taken")
        pts = VGroup(
            label(rf"scheduling removed {a['load_use'] - a2['load_use']} stalls out of {a['load_use']:,}: "
                  r"\ the Job's loops are chains", font_size=20, color=GREY_A),
            label(rf"relative to hand-written: instructions {100 * (a['instructions'] / h['instructions'] - 1):+.1f}\%; cycles {100 * (a['cycles'] / h['cycles'] - 1):+.1f}\%", font_size=21,
                  color=NO),
            label(r"why: \ inverted loops branch \textit{backward} every iteration, \ and this pipeline predicts "
                  r"``not taken''", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(cap, DOWN, buff=0.4)
        with self.voiceover(f"Now measure the generated code on Part 7's simulated pipeline, using the same {s['bytes']:,}-byte passage. <bookmark mark='a'/> Compare the hand-written program, the compiled array program, its scheduled form and the compiled list program. <bookmark mark='b'/> Scheduling removes {a['load_use'] - a2['load_use']:,} of the compiled array program's {a['load_use']:,} load-use stall cycles. The remaining dependency chains limit this local scheduler's opportunities. <bookmark mark='c'/> Relative to hand-written code, the compiled array instruction count changes by {100 * (a['instructions'] / h['instructions'] - 1):+.1f} percent, while its cycle count changes by {100 * (a['cycles'] / h['cycles'] - 1):+.1f} percent. <bookmark mark='d'/> In this configuration, every conditional branch is predicted not taken. The inverted loops repeatedly take their conditional back branches, creating flushes. The next comparison changes the predictor while keeping this program and input fixed.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(tab), FadeIn(cap), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[0]), Indicate(VGroup(*tab.cells[3]), color=YES))
            vo.wait_until('c')
            self.play(FadeIn(pts[1]))
            vo.wait_until('d')
            self.play(FadeIn(pts[2]), *[Indicate(tab.cells[k][3], color=NO) for k in (2, 3, 4)])
        self.wait(0.3)
        self.clear_scene()

    def predictors(self):
        s = load("sched")
        R = s["rows"]
        head = label(r"A compiler assumes a machine", font_size=34).to_edge(UP, buff=0.3)
        rows, cols = [], []
        for pred in ("not taken", "two-bit", "tournament"):
            h = sched_row(R, "hand", "hand-written", pred)
            a = sched_row(R, "array", "as compiled", pred)
            l_ = sched_row(R, "list", "as compiled", pred)
            win = a["cycles"] < h["cycles"]
            rows.append([pred, f"{h['cycles']:,}", f"{a['cycles']:,}", f"{l_['cycles']:,}",
                         f"{100 * (a['cycles'] / h['cycles'] - 1):+.0f}\\%"])
            cols.append([WHITE, WHITE, YES if win else NO, WHITE, YES if win else NO])
        tab = grid_table([r"predictor \ (Part 7)", r"hand-written", r"compiled, \ array", r"compiled, \ list",
                          r"compiled vs hand"], rows, widths=[2.8, 2.2, 2.3, 2.2, 2.4], row_h=0.55, font_size=20,
                         colors=cols, mono_cols=()).next_to(head, DOWN, buff=0.6)
        cap = label(r"cycles on the same passage", font_size=18, color=GREY_B).next_to(tab, DOWN, buff=0.15)
        pts = VGroup(
            label("on this input, the recorded predictors change the cycle comparison", font_size=21,
                  color=YES),
            label("loop inversion trades branch behavior, instruction count and code size", font_size=21,
                  color=GREY_A),
            label(r"and hardware is designed for the code compilers emit: \ the two evolve together", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(cap, DOWN, buff=0.5)
        with self.voiceover("Now change this simulated pipeline's branch predictor. <bookmark mark='a'/> A two-bit counter can learn the frequently taken loop-back branches, and the recorded cycle counts change. The tournament predictor gives another measured comparison. These gains belong to these programs, inputs and machine configurations. <bookmark mark='b'/> Loop inversion trades tests, jumps, code size and branch behavior. Prediction is one part of that tradeoff; an architecture with a different branch cost may still benefit for other reasons. <bookmark mark='c'/> Compiler heuristics and microarchitecture therefore need compatible cost models. Hardware teams, compiler projects and application developers contribute to that agreement, and they need not belong to the same company.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(tab), FadeIn(cap), run_time=0.6)
            vo.wait_until('a')
            self.play(FadeIn(pts[0]))
            vo.wait_until('b')
            self.play(FadeIn(pts[1]))
            vo.wait_until('c')
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def swp(self):
        head = label(r"Across iterations: \ software pipelining", font_size=34).to_edge(UP, buff=0.3)
        stages = ["load", "add", "store"]
        cols = [DATA, YES, FUNC]
        grid = VGroup()
        for it in range(4):
            for st in range(3):
                r = RoundedRectangle(width=1.2, height=0.5, corner_radius=0.08, stroke_color=cols[st],
                                     fill_color=cols[st], fill_opacity=0.25)
                t = label(rf"{stages[st]} {it + 1}", font_size=16, color=WHITE).move_to(r)
                g = VGroup(r, t).move_to([-4.2 + 1.35 * (it + st), 1.4 - 0.65 * it, 0])
                grid.add(g)
        steady = SurroundingRectangle(VGroup(grid[2], grid[4], grid[6]), color=HEAD, buff=0.08)
        sl = label(r"steady state: \ load $i{+}2$, \ add $i{+}1$, \ store $i$, \ every cycle", font_size=20,
                   color=HEAD).next_to(grid, DOWN, buff=0.4)
        pts = VGroup(
            label(r"modulo scheduling \ (Rau and Glaeser, \ 1981; \ Lam, \ 1988): \ overlap the iterations "
                  r"themselves", font_size=20, color=GREY_A),
            label(r"essential for in-order and VLIW machines \ (Itanium, \ DSPs, \ GPUs)", font_size=20,
                  color=GREY_A),
            label(r"an out-of-order core does it in hardware, \ at run time \ (Part 8): \ static scheduling matters "
                  r"less there", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover("Independent work from different iterations can sometimes overlap. <bookmark mark='a'/> Suppose an iteration loads, adds and stores, and its dependencies permit the next iteration's load before the previous store finishes. Starting iterations at regular intervals creates a software pipeline. <bookmark mark='b'/> On a machine with enough issue width and the required functional units, the steady state can contain a load, an add and a store from different iterations at once. Memory aliases, loop-carried dependencies and available registers limit that overlap; a load-add-store sketch alone does not prove it is legal. <bookmark mark='c'/> Modulo scheduling and related software-pipelining methods are especially useful where hardware exposes scheduling decisions, including VLIW targets. Out-of-order hardware can discover some overlap dynamically, but finite windows, dependencies and resource limits mean it need not reproduce the same schedule or make static optimization irrelevant.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.12), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Create(steady), FadeIn(sl))
            vo.wait_until('c')
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.5), run_time=3)
        self.wait(0.3)
        self.clear_scene()
