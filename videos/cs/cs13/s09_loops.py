from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, ir_block, load, mono, region)


def asm_after(asm, lab, n):
    k = asm.index(lab + ":")
    return [asm[k]] + ["    " + l for l in asm[k + 1:k + 1 + n]]


def pct(rows, a, b, key="array"):
    return 100 * (rows[b][key] - rows[a][key]) / rows[a][key]


class Loops(WatchScene):
    def construct(self):
        self.card()
        self.natural()
        self.licm()
        self.ivsr()

    def card(self):
        self.chapter(8, r"Loops", r"Where does the time go?", lit=(1971,), extra=((1971, r"Allen--Cocke: \ a catalogue of optimizations"),), part=PART, said="Chapter eight. Loops.")

    def natural(self):
        lp = load("loops")
        head = label(r"Finding the loops in a graph", font_size=34).to_edge(UP, buff=0.3)
        defs = VGroup(
            label(r"a \textbf{back edge}: \ $n \to h$ \ where $h$ dominates $n$", font_size=22, color=GREY_A),
            label(r"its \textbf{natural loop}: \ $h$, \ and every block that reaches $n$ without passing $h$",
                  font_size=22, color=GREY_A),
            label(r"$h$ is the loop's \textbf{header}: \ the only way in", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.4)
        outer, inner = lp["loops"]
        ob = VGroup(*[mono(b, 15, WHITE) for b in sorted(outer["blocks"]) if b not in inner["blocks"]]).arrange_in_grid(
            cols=4, buff=(0.4, 0.2))
        ib = VGroup(*[mono(b, 15, WHITE) for b in sorted(inner["blocks"])]).arrange(RIGHT, buff=0.4)
        ibox = SurroundingRectangle(ib, color=FUNC, buff=0.2, corner_radius=0.1)
        il = label(rf"inner loop: \ header \texttt{{{inner['header']}}}: \ compare the letters", font_size=18,
                   color=FUNC).next_to(ibox, DOWN, buff=0.1)
        inner_g = VGroup(ib, ibox, il)
        content = VGroup(ob, inner_g).arrange(DOWN, buff=0.35)
        obox = SurroundingRectangle(content, color=CTRL, buff=0.3, corner_radius=0.12)
        ol = label(rf"outer loop: \ header \texttt{{{outer['header']}}}: \ scan the table", font_size=18,
                   color=CTRL).next_to(obox, UP, buff=0.1)
        nest = VGroup(content, obox, ol).next_to(defs, DOWN, buff=0.5)
        cap = label(r"the array Job's \texttt{word}: \ two loops, \ one inside the other", font_size=20,
                    color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover("Profiling often identifies loops as important costs. Dominance helps locate one useful class of loops. <bookmark mark='a'/> A back edge n to h has a target h that dominates its source n. <bookmark mark='b'/> Its natural loop contains h and the blocks that can reach n without passing through h; include n itself. <bookmark mark='c'/> The header h is the single entry from outside that natural loop. Irreducible control flow can have multiple-entry cycles that this representation does not capture as one natural loop. <bookmark mark='d'/> In the recorded array Job's word function, the highlighted outer loop scans table entries. <bookmark mark='e'/> Its inner loop compares letters. The displayed block sets come from the actual control-flow graph. Nested loops often multiply execution counts, but early exits, input sizes and paths determine which blocks really run most.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(defs[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(defs[1]))
            vo.wait_until('c')
            self.play(FadeIn(defs[2]))
            vo.wait_until('d')
            self.play(Create(obox), FadeIn(ol), FadeIn(ob), FadeIn(cap))
            vo.wait_until('e')
            self.play(FadeIn(inner_g))
        self.wait(0.3)
        self.clear_scene()


    def licm(self):
        self.ask(r"An expression whose inputs never change inside the loop. \\ Compute it...",
                 [r"every iteration", r"once, before the loop"], 1,
                 say="An expression inside a loop whose inputs never change there. Where should it be computed?",
                 reveal="Once, before the loop: loop-invariant code motion.")
        lp = load("loops")
        p = load("passes")
        head = label(r"Loop-invariant code motion", font_size=34).to_edge(UP, buff=0.3)
        pre_block = next(b for b in lp["after_licm"]["blocks"] if b["label"] == "body5_pre")
        pre = [pre_block["label"] + ":"] + [line for line in pre_block["ins"] if not line.startswith("br ")]
        pre_c = code(pre, size=17, color=CODE).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        notes = {k: (r"the table's address" if "= &table" in line else
                     r"is $0 < n$? (the inner loop's first test)" if "= 0 < %n" in line else
                     r"an invariant value") for k, line in enumerate(pre[1:], 1)}
        tags = VGroup(*[label(t, font_size=18, color=YES).next_to(pre_c[k], RIGHT, buff=0.5) for k, t in
                        notes.items()])
        for t in tags:
            t.set_x(pre_c.get_right()[0] + 0.6 + t.width / 2)
        rules = VGroup(
            label(r"an instruction is \textbf{invariant} if its operands are defined outside the loop, \ or are "
                  r"invariant", font_size=21, color=GREY_A),
            label(r"move it to the preheader: \ computed once, \ not once per table entry", font_size=21,
                  color=GREY_A),
            label("our load rule: header prefix; no earlier trap/effect; no loop stores or calls",
                  font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(pre_c, DOWN, buff=0.6).to_edge(LEFT, buff=0.8)
        meas = label(rf"{lp['stats']['hoisted']} instructions hoisted; \ on the array Job: \ "
                     rf"{pct(p['rows'], 5, 6):+.1f}\% instructions", font_size=21, color=YES).to_edge(DOWN,
                                                                                                buff=0.4)
        guard = region(3.0, 0.55, r"$i=1$?", CTRL, font_size=20).move_to([2.8, -0.8, 0])
        conditional_load = region(3.0, 0.55, r"load \texttt{*p}", DATA, font_size=20).move_to([2.8, -1.9, 0])
        skipped = region(2.3, 0.55, r"skip the load", YES, font_size=20).move_to([-1.0, -1.9, 0])
        guarded_edge = Arrow(guard.get_bottom(), conditional_load.get_top(), buff=0.06,
                             color=GREY_D, stroke_width=1.5, tip_length=0.12)
        skip_edge = Arrow(guard.get_left(), skipped.get_top(), buff=0.06,
                         color=YES, stroke_width=2.5, tip_length=0.12)
        case = label(r"$i=0$, \ $p=\texttt{null}$: the skipped load must stay skipped",
                     font_size=19, color=YES).move_to([1.0, -2.65, 0])
        true_label = label(r"true", font_size=15, color=GREY_B).next_to(guarded_edge, RIGHT, buff=0.07)
        false_label = label(r"false", font_size=15, color=YES).next_to(skip_edge, UP, buff=0.07)
        guard_view = VGroup(guard, conditional_load, skipped, guarded_edge, skip_edge,
                            true_label, false_label, case)
        with self.voiceover(f"Some computations produce the same value on every iteration. <bookmark mark='a'/> Operand invariance is the starting point: each input comes from outside the loop or from another invariant computation. <bookmark mark='b'/> Moving a total, effect-free instruction into the preheader can replace repeated work with one computation. The recorded word-function example hoists {lp['stats']['hoisted']} instructions; follow their destinations in the intermediate-code panel. <bookmark mark='c'/> Loads require two separate arguments: the memory must not change, and moving the access must not introduce a trap on a path that previously skipped it. Our repaired pass allows only header loads before any potentially trapping or effectful instruction, with invariant addresses and no loop stores or calls. It does not assume different widths cannot overlap. A conditional body load remains guarded, even when its address is invariant. <bookmark mark='d'/> In this array-Job pass comparison, the instruction count changes by {pct(p['rows'], 5, 6):+.1f} percent. The result measures this program, not a general promise about loops.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(rules[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pre_c), FadeIn(rules[1]))
            self.play(LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.6), run_time=4)
            vo.wait_until('c')
            self.play(FadeIn(rules[2]), FadeIn(guard_view), Indicate(pre_c, color=NO))
            vo.wait_until('d')
            self.play(FadeIn(meas))
        self.wait(0.3)
        self.clear_scene()

    def ivsr(self):
        lp = load("loops")
        p = load("passes")
        head = label(r"Induction variables: \ multiply becomes add", font_size=34).to_edge(UP, buff=0.3)
        wo = lp["asm"]["without"]
        wi = lp["asm"]["with"]
        left = code(asm_after(wo, "word.body5", 6) + ["    ..."] + asm_after(wo, "word.endif12", 1) +
                    asm_after(wo, "word.latch6", 1), size=15, color=CODE)
        right = code(asm_after(wi, "word.body5", 2) + ["    ..."] + asm_after(wi, "word.endif12", 2) +
                     asm_after(wi, "word.latch6", 1), size=15, color=CODE)
        VGroup(left, right).arrange(RIGHT, buff=1.6, aligned_edge=UP).next_to(head, DOWN, buff=0.75)
        lt = label(r"before: \ \texttt{table + 12*i}, \ every iteration", font_size=20, color=NO).next_to(left, UP,
                                                                                                   buff=0.15)
        rt = label(r"after: \ a pointer that steps by 12", font_size=20, color=YES).next_to(right, UP, buff=0.15)
        lt.align_to(left, LEFT)
        rt.align_to(right, LEFT)
        hl_l = SurroundingRectangle(left[1:5], color=NO, buff=0.05)
        hl_r = SurroundingRectangle(right[6], color=YES, buff=0.05)
        rule = VGroup(
            label(r"$i$ steps by 1 \ $\Rightarrow$ \ $12i + \mathit{table}$ steps by 12", font_size=22, color=GREY_A),
            label(r"keep that value in a register of its own, \ add 12 each time round", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=1.1)
        meas = label(rf"on the array Job: \ {p['rows'][6]['array']:,} $\to$ {p['rows'][7]['array']:,} \ "
                     rf"({pct(p['rows'], 6, 7):+.0f}\%): \ the pointer Part 6 wrote by hand", font_size=21,
                     color=YES).to_edge(DOWN, buff=0.45)
        with self.voiceover(f"An induction recurrence can replace repeated address arithmetic. <bookmark mark='a'/> The left panel recomputes an indexed table address inside the scan. <bookmark mark='b'/> If i increases by one, table plus twelve times i increases by twelve, under this machine's word and address semantics. <bookmark mark='c'/> Carry that derived address as another loop value and advance it by twelve. The compiler must initialize it correctly, preserve exits and updates, and retain valid memory accesses. This is induction-variable strength reduction. The right panel shows the pointer recurrence in the actual generated code. <bookmark mark='d'/> In this pass comparison, the array Job changes from {p['rows'][6]['array']:,} to {p['rows'][7]['array']:,} executed instructions, or {pct(p['rows'], 6, 7):+.1f} percent. It recovers the hand-written loop's pointer idea; the full compiled program still has its own overhead and need not beat that baseline.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(left), FadeIn(lt), run_time=0.6)
            vo.wait_until('a')
            self.play(Create(hl_l))
            vo.wait_until('b')
            self.play(FadeIn(rule[0]))
            vo.wait_until('c')
            self.play(FadeIn(rule[1]), FadeIn(right), FadeIn(rt))
            self.play(Create(hl_r))
            vo.wait_until('d')
            self.play(FadeOut(rule), FadeIn(meas))
        self.wait(0.3)
        self.clear_scene()

