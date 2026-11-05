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
        with self.voiceover(
            "A program spends almost all its time in loops, so a compiler first has to find them. In a graph, "
            "that takes the dominators. <bookmark mark='a'/> A back edge is an edge from n to h where h dominates "
            "n: an edge that jumps back to something that must already have run. <bookmark mark='b'/> Its natural "
            "loop is h together with every block that can reach n without passing through h. <bookmark mark='c'/> "
            "And h is the loop's header, the only way in from outside. <bookmark mark='d'/> In the array Job's word "
            "function the compiler finds two natural loops. The outer one scans the table, ten blocks with header "
            "body five. <bookmark mark='e'/> Inside it, the inner loop compares letters, three blocks with header "
            "body twenty-two. Loops found this way nest neatly, and the innermost run most often."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defs[0]))
            vo.wait_until("b")
            self.play(FadeIn(defs[1]))
            vo.wait_until("c")
            self.play(FadeIn(defs[2]))
            vo.wait_until("d")
            self.play(Create(obox), FadeIn(ol), FadeIn(ob), FadeIn(cap))
            vo.wait_until("e")
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
        with self.voiceover(
            "The simplest loop transformation changes only the shape. <bookmark mark='a'/> A while loop, lowered "
            "naively, tests at the top. Each iteration runs the body, jumps back up, and tests again: two "
            "branches every time round. <bookmark mark='b'/> Inverting the loop puts a single guard in front, for "
            "the case of zero iterations, and moves the test to the bottom, where it branches straight back into "
            "the body. One branch per iteration. A C programmer would recognize this as turning a while loop into "
            "an if around a do-while. <bookmark mark='c'/> On the array Job this saves six and a half percent of "
            "all instructions, and on the list Job, twelve and a half. It also gives every loop a preheader, a block that "
            "runs once just before the loop, which the next transformation needs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(c1), Create(back1), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(c2), Create(back2), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(meas))
        self.wait(0.3)
        self.clear_scene()

    def licm(self):
        lp = load("loops")
        p = load("passes")
        head = label(r"Loop-invariant code motion", font_size=34).to_edge(UP, buff=0.3)
        pre = asm_after(lp["asm"]["with"], "word.body5_pre", 6)
        pre_c = code(pre, size=17, color=CODE).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        notes = {1: r"\texttt{w[0]}: \ the word's first letter", 2: r"the table's address",
                 3: r"\texttt{entries}", 4: r"is $0 < n$? \ (the inner loop's first test)"}
        tags = VGroup(*[label(t, font_size=18, color=YES).next_to(pre_c[k], RIGHT, buff=0.5) for k, t in
                        notes.items()])
        for t in tags:
            t.set_x(pre_c.get_right()[0] + 0.6 + t.width / 2)
        rules = VGroup(
            label(r"an instruction is \textbf{invariant} if its operands are defined outside the loop, \ or are "
                  r"invariant", font_size=21, color=GREY_A),
            label(r"move it to the preheader: \ computed once, \ not once per table entry", font_size=21,
                  color=GREY_A),
            label(r"a load may move only if nothing in the loop could store there, \ and nothing is called",
                  font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(pre_c, DOWN, buff=0.6).to_edge(LEFT, buff=0.8)
        meas = label(rf"{lp['stats']['hoisted']} instructions hoisted; \ on the array Job: \ "
                     rf"{pct(p['rows'], 5, 6):+.1f}\% instructions", font_size=21, color=YES).to_edge(DOWN,
                                                                                                buff=0.4)
        with self.voiceover(
            "Inside the outer loop, some values are the same on every iteration. <bookmark mark='a'/> An "
            "instruction is loop-invariant if each of its operands is defined outside the loop, or is itself "
            "invariant. <bookmark mark='b'/> Such an instruction can move to the preheader, computed once instead "
            "of once per table entry. In word, the compiler hoists four. The first letter of the new word. The "
            "table's address. The number of entries. And whether zero is less than n, the inner loop's first "
            "test. <bookmark mark='c'/> Loads need care. Moving a load is safe only if nothing inside the loop "
            "could store to that memory, and no call could. Here the loop contains no store at all: the one store, "
            "counting a word it found, is followed at once by a return, outside the loop. <bookmark mark='d'/> "
            "Worth eleven percent of the array Job's instructions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rules[0]))
            vo.wait_until("b")
            self.play(FadeIn(pre_c), FadeIn(rules[1]))
            self.play(LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.6), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(rules[2]), Indicate(pre_c[3], color=NO))
            vo.wait_until("d")
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
        with self.voiceover(
            "The biggest win in the array Job is subtler. <bookmark mark='a'/> Each time round the scan, the code "
            "still computes the address of table of i from scratch: load twelve, multiply by i, add the table's "
            "address. <bookmark mark='b'/> But i goes up by one each time, so twelve i plus the table's address "
            "goes up by exactly twelve. i is an induction variable, and the address is an induction variable "
            "derived from it. <bookmark mark='c'/> So keep the address in a register of its own, start it at the "
            "table, and add twelve each time round. Four instructions, one of them a slow multiply, become one "
            "add. This is strength reduction of induction variables, one of the oldest loop optimizations: the "
            "FORTRAN I compiler already did a version of it. <bookmark mark='d'/> On the array Job it removes over "
            "a third of all instructions. And the result is exactly the pointer we wrote by hand in Part 6, which "
            "is how the compiler came to beat us: it found our trick, and did everything else a little better."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(lt))
            self.play(Create(hl_l))
            vo.wait_until("b")
            self.play(FadeIn(rule[0]))
            vo.wait_until("c")
            self.play(FadeIn(rule[1]), FadeIn(right), FadeIn(rt))
            self.play(Create(hl_r))
            vo.wait_until("d")
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
        with self.voiceover(
            "Production compilers have many more loop transformations. <bookmark mark='a'/> Unrolling copies the "
            "body several times, so the loop tests once per four iterations instead of every one, and the "
            "scheduler has more independent work to interleave; the price is more code. <bookmark mark='b'/> "
            "Vectorization goes further and does four additions in one SIMD instruction, as in Part 10. "
            "Interchange and tiling reorder nested loops to suit the cache, as in Part 9. The polyhedral model "
            "treats a loop nest as a set of integer points in a polyhedron, and its transformations as affine "
            "maps, which lets a compiler search among them. <bookmark mark='c'/> Our compiler does none of these: "
            "Pebble has no vector instructions, and the Job's loops exit as soon as they find what they want."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(orig), GrowArrow(arr), FadeIn(unr), FadeIn(ul))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in more], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()
