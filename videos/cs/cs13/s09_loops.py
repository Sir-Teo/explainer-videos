from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, ir_block, load, mono, region)


def asm_after(asm, lab, n):
    k = asm.index(lab + ":")
    return [asm[k]] + ["    " + l for l in asm[k + 1:k + 1 + n]]


def pct(rows, a, b, key="array"):
    return 100 * (rows[b][key] - rows[a][key]) / rows[a][key]


class Loops(VoiceoverScene):
    def construct(self):
        self.card()
        self.natural()
        self.inversion()
        self.licm()
        self.ivsr()
        self.unroll()

    def card(self):
        card = chapter_card(8, r"Loops", r"Where does the time go?", lit=(1971,),
                            extra=((1971, r"Allen--Cocke: \ a catalogue of optimizations"),), part=PART)
        with self.voiceover("Chapter eight. Loops."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

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

    def inversion(self):
        p = load("passes")
        head = label(r"Loop inversion: \ test at the bottom", font_size=34).to_edge(UP, buff=0.3)

        def flow(blocks, edges, x):
            bs = {}
            for k, (name, lines, c) in enumerate(blocks):
                bs[name] = ir_block(name, lines, c, 19)
            col = VGroup(*bs.values()).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([x, -0.4, 0])
            return bs, col
        b1, c1 = flow([("test", ["if i >= n br done"], CTRL), ("body", ["...", "i = i + 1", "br test"], DATA),
                       ("done", ["..."], GREY_B)], None, -3.4)
        b2, c2 = flow([("guard", ["if i >= n br done"], CTRL), ("body", ["...", "i = i + 1",
                                                                        "if i < n br body"], DATA),
                       ("done", ["..."], GREY_B)], None, 3.0)
        back1 = CurvedArrow(b1["body"].box.get_right(), b1["test"].box.get_right(), angle=1.2, color=NO,
                            stroke_width=2, tip_length=0.13)
        back2 = CurvedArrow(b2["body"].box.get_right() + DOWN * 0.25, b2["body"].box.get_right() + UP * 0.25,
                            angle=2.2, color=YES, stroke_width=2, tip_length=0.13)
        t1 = label(r"two branches per iteration", font_size=20, color=NO).next_to(c1, UP, buff=0.3)
        t2 = label(r"one branch per iteration", font_size=20, color=YES).next_to(c2, UP, buff=0.3)
        meas = label(rf"on the array Job: \ {pct(p['rows'], 1, 2):+.1f}\% instructions; \ on the list Job: \ "
                     rf"{pct(p['rows'], 1, 2, 'list'):+.1f}\%", font_size=21, color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover(f"Loop inversion changes the control-flow shape. <bookmark mark='a'/> In the left sketch, the body jumps to a top test, and the test chooses whether to enter again. <bookmark mark='b'/> In the right sketch, an initial guard preserves the zero-iteration case. The repeated body ends in the conditional back branch. This can remove an unconditional jump from the repeated path, while changing code size and branch behavior. The guard must preserve the original conditions and effects. <bookmark mark='c'/> In this pass sequence, the executed instruction count changes by {pct(p['rows'], 1, 2):+.1f} percent for the array Job and {pct(p['rows'], 1, 2, 'list'):+.1f} percent for the list Job. The transformed loops also provide entry blocks useful for later code motion. Whether fewer instructions save cycles still depends on the machine.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(c1), Create(back1), FadeIn(t1), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(c2), Create(back2), FadeIn(t2))
            vo.wait_until('c')
            self.play(FadeIn(meas))
        self.wait(0.3)
        self.clear_scene()

    def licm(self):
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

    def unroll(self):
        head = label(r"More loop transformations", font_size=34).to_edge(UP, buff=0.3)
        orig = code(["for i in 0..n:", "    s += a[i]"], size=18)
        unr = code(["for i in 0..n step 4:", "    s += a[i]", "    s += a[i+1]", "    s += a[i+2]",
                    "    s += a[i+3]", "(and the leftover iterations)"], size=18, color=YES)
        VGroup(orig, unr).arrange(RIGHT, buff=1.5, aligned_edge=UP).next_to(head, DOWN, buff=0.6).shift(LEFT * 1.5)
        arr = Arrow(orig.get_right(), unr.get_left(), buff=0.3, color=GREY_B)
        ul = label(r"\textbf{unrolling}: \ one test per four iterations; \ room for scheduling; \ more code",
                   font_size=20, color=GREY_A).next_to(VGroup(orig, unr), DOWN, buff=0.5)
        more = VGroup(
            label(r"\textbf{vectorization}: \ four additions in one SIMD instruction \ (Part 10)", font_size=20,
                  color=GREY_A),
            label(r"\textbf{interchange and tiling}: \ reorder nested loops for the cache \ (Part 9)", font_size=20,
                  color=GREY_A),
            label(r"\textbf{the polyhedral model}: \ loop nests as integer polyhedra; \ transformations as "
                  r"affine maps", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(ul, DOWN, buff=0.4)
        note = label(r"not in our compiler: \ Pebble has no SIMD, \ and the Job's loops exit early", font_size=20,
                     color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover("Production compilers consider many other loop transformations. <bookmark mark='a'/> Unrolling copies a body, potentially reducing repeated tests and exposing independent work. The implementation still needs correct handling of leftover iterations, exits and effects; more code can also be costly. <bookmark mark='b'/> SIMD vectorization groups compatible operations into lanes. Interchange and tiling can improve locality when dependencies permit. Polyhedral methods model suitable affine loop domains and accesses as integer sets, then search legal transformations. Arbitrary pointer-dependent control flow does not automatically fit that model. <bookmark mark='c'/> Our compiler implements none of these additional methods. Pebble lacks SIMD instructions. Early exits in the Job make several transformations more complicated, but do not establish that all unrolling or loop restructuring is impossible.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(orig), GrowArrow(arr), FadeIn(unr), FadeIn(ul), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(LaggedStart(*[FadeIn(m) for m in more], lag_ratio=0.5), run_time=3)
            vo.wait_until('c')
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()
