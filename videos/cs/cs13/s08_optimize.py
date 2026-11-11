from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, cfg_edge, code, ir_block, load,
                                   mono, region)


def blocks_view(fv, size=14, colors=None, gap=0.35):
    """A function's blocks in a column, with their edges."""
    bs = {}
    for b in fv["blocks"]:
        bs[b["label"]] = ir_block(b["label"], b["ins"], (colors or {}).get(b["label"], DATA), size)
    return bs


def measured(rows, a, b, key="array"):
    ra, rb = rows[a][key], rows[b][key]
    return ra, rb, 100 * (rb - ra) / ra


class Optimize(VoiceoverScene):
    def construct(self):
        self.card()
        self.lattice()
        self.sccp()
        self.dce()
        self.gvn()
        self.identities()
        self.ordering()

    def card(self):
        card = chapter_card(7, r"Optimizations on SSA", r"Which work can be proved unnecessary?", lit=(1991,),
                            extra=((1991, r"Wegman--Zadeck: \ SCCP"),), part=PART)
        with self.voiceover("Chapter seven. Optimizations on SSA."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def lattice(self):
        head = label(r"Constant propagation: \ a three-level lattice", font_size=34).to_edge(UP, buff=0.3)
        top = region(2.8, 0.6, r"$\top$: \ not yet seen", GREY_B, font_size=20).move_to(UP * 1.6)
        consts = VGroup(*[region(0.9, 0.55, t, YES, font_size=20) for t in
                          (r"$\cdots$", r"$-1$", r"$0$", r"$1$", r"$2$", r"$32$", r"$\cdots$")]).arrange(
            RIGHT, buff=0.3).move_to(UP * 0.1)
        bot = region(3.4, 0.6, r"$\bot$: \ varies at run time", NO, font_size=20).move_to(DOWN * 1.4)
        lines = VGroup(*[Line(top.get_bottom(), c.get_top(), color=GREY_D, stroke_width=1.3) for c in consts[1:-1]],
                       *[Line(c.get_bottom(), bot.get_top(), color=GREY_D, stroke_width=1.3) for c in consts[1:-1]])
        rules = VGroup(
            label(r"each SSA name starts at $\top$ \ and can only move down: \ at most twice", font_size=21,
                  color=GREY_A),
            label(r"$\phi(3, 3) = 3$, \ \ $\phi(3, 4) = \bot$, \ \ $\phi(3, \top) = 3$: \ the meet", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.6)
        with self.voiceover("Constant propagation uses another finite-height lattice. <bookmark mark='a'/> This diagram chooses the dual ordering to the earlier growing liveness sets. Top means that no executable evidence has arrived yet. A particular constant is in the middle; bottom means conflicting values or a value that varies. <bookmark mark='b'/> The analysis moves downward: an SSA name changes at most from unseen to a constant to varying. That bounds value changes, while a worklist also tracks executable edges. Reversing the order would describe the same information process as an ascent from bottom. <bookmark mark='c'/> Merge three with three and obtain three. Merge three with four and obtain varying. Merge three with an input whose edge is not yet known executable, and provisionally retain three. If more executable evidence arrives, the value must be revised. This optimism belongs to the analysis, not permission to assume a runtime value without proof.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(top), run_time=0.6)
            vo.wait_until('a')
            self.play(LaggedStart(*[FadeIn(c) for c in consts], lag_ratio=0.15), Create(lines[:5]))
            self.play(FadeIn(bot), Create(lines[5:]))
            vo.wait_until('b')
            self.play(FadeIn(rules[0]))
            vo.wait_until('c')
            self.play(FadeIn(rules[1]))
        self.wait(0.3)
        self.clear_scene()

    def sccp(self):
        o = load("opts")
        p = load("passes")
        head = label(r"Sparse conditional constant propagation", font_size=32).to_edge(UP, buff=0.3)
        src = code(["fn f(x: int) -> int {", "    var a: int = 4;", "    var b: int = a * 8;", "    var c: int = 0;",
                    "    if b > 16 { c = x + b; }", "    else { c = x - 1; }", "    return c * 2;", "}"], size=15)
        src.to_corner(UL, buff=0.5).shift(DOWN * 0.8)
        bs = blocks_view(o["sccp_before"], size=13)
        bs["entry"].move_to([0.9, 1.7, 0])
        bs["then2"].next_to(bs["entry"], DOWN, buff=0.6).shift(LEFT * 1.3)
        bs["else4"].next_to(bs["entry"], DOWN, buff=0.6).shift(RIGHT * 1.3)
        bs["endif3"].next_to(VGroup(bs["then2"], bs["else4"]), DOWN, buff=0.6)
        es = VGroup(*[cfg_edge(bs[a], bs[b]) for a, b in (("entry", "then2"), ("entry", "else4"),
                                                          ("then2", "endif3"), ("else4", "endif3"))])
        before = VGroup(*bs.values(), es)
        after = blocks_view(o["sccp_after"], size=14, colors={"entry": YES, "then2": YES, "endif3": YES})
        aft = VGroup(after["then2"], after["endif3"]).arrange(DOWN, buff=0.4).move_to([5.2, 0.2, 0])
        vals = VGroup(mono("a = 4", 15, YES), mono("b = 32", 15, YES), mono("b > 16 = 1", 15, YES),
                      label(r"\texttt{else4}: never executes", font_size=15, color=NO), mono("c.4 = φ(c.3, —) = x + 32", 15, YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(src, DOWN, buff=0.45).align_to(src, LEFT)
        r0, r1, pct = measured(p["rows"], 3, 4)
        meas = label(rf"on the Job: \ {r0:,} $\to$ {r1:,} instructions \ ({pct:+.1f}\%): \ the Job has few "
                     r"constants", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            (
            "Here is a function made for the purpose. a is four, b is a times eight, and if b is more than "
            "sixteen, c is x plus b, otherwise x minus one. <bookmark mark='a'/> In SSA form it has four blocks "
            "and a phi at the join. <bookmark mark='b'/> The analysis finds that a is four, so b is thirty-two, "
            "so the comparison is true. <bookmark mark='c'/> And it tracks which edges can execute at the same "
            "time as which values are constant. Since the comparison is always true, the edge to else is never "
            "taken: else never runs. <bookmark mark='d'/> So the phi at the join may ignore the operand arriving "
            "from else, and c dot four is simply x plus thirty-two. <bookmark mark='e'/> What remains is two "
            "instructions: x plus thirty-two, times two. Doing both jobs at once, constants and reachable code, "
            "finds more than running either one first. This is Wegman and Zadeck's algorithm, from 1991. "
            "<bookmark mark='f'/> On this Job and at this point in the pass order, the measured change is small. "
            "Other programs can expose many constants, and inlining or loop transformations can create further "
            "opportunities."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(before))
            vo.wait_until("b")
            self.play(FadeIn(vals[:3]), Indicate(bs["entry"].lines[:5], color=YES))
            vo.wait_until("c")
            self.play(FadeIn(vals[3]), es[1].animate.set_color(NO).set_opacity(0.4), es[3].animate.set_color(NO)
                      .set_opacity(0.4), bs["else4"].animate.set_opacity(0.3))
            vo.wait_until("d")
            self.play(FadeIn(vals[4]), Indicate(bs["endif3"].lines[0], color=YES))
            vo.wait_until("e")
            self.play(FadeIn(aft))
            vo.wait_until("f")
            self.play(FadeIn(meas))
        self.wait(0.3)
        self.clear_scene()

    def dce(self):
        head = label(r"Dead code, \ and copies", font_size=34).to_edge(UP, buff=0.3)
        lines = ["%a  = 4", "%t1 = %a * 8", "%b  = %t1", "%c.1 = 0", "%t6 = %x + %b", "%t8 = %t6 * 2", "ret %t8"]
        lst = VGroup(*[mono(l, 20, CODE) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(
            LEFT * 3.4 + DOWN * 0.2)
        steps = VGroup(
            label(r"\textbf{copy propagation}: \ after \ \texttt{\%b = \%t1}, \ use \texttt{\%t1} for \texttt{\%b}",
                  font_size=21, color=GREY_A),
            label(r"\textbf{dead code}: \ mark what is useful, \ sweep the rest", font_size=21, color=GREY_A),
            label(r"useful: \ returns, \ stores, \ calls, \ branches; \ and whatever they use", font_size=20,
                  color=GREY_A),
            label(r"in SSA, \ a definition with no uses is dead at once", font_size=20, color=GREY_A),
            label(r"like a garbage collector, \ over instructions \ (Part 15)", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 2.8 + DOWN * 0.1)
        dead = [0, 1, 2, 3]
        with self.voiceover(
            (
            "Two cleanup passes use those value links. <bookmark mark='a'/> Copy propagation replaces a use of an "
            "SSA copy by its source, because the copied names do not acquire later assignments. <bookmark "
            "mark='b'/> Dead code elimination can resemble a garbage collector over instructions. <bookmark "
            "mark='c'/> Start from instructions whose behavior must remain: returns, memory effects, calls and "
            "required control flow. An operation that can trap may also need preservation unless the semantics or "
            "a proof allows removing it. Follow their dependencies backward through the def-use links. <bookmark "
            "mark='d'/> Unneeded computations can then disappear. In the constant example, folding the branch and "
            "values makes several old arithmetic definitions unused. Our simple pass keeps control-flow roots "
            "conservatively rather than proving every possible dead branch itself. <bookmark mark='e'/> Part 15 "
            "develops the related mark-and-sweep idea for objects in memory."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(lst))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), *[lst[k].animate.set_color(YES) for k in (4, 5, 6)])
            vo.wait_until("d")
            self.play(FadeIn(steps[3]), *[lst[k].animate.set_color(NO).set_opacity(0.35) for k in dead])
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()

    def gvn(self):
        o = load("opts")
        p = load("passes")
        head = label(r"Value numbering: \ the same value, \ computed once", font_size=32).to_edge(UP, buff=0.3)
        src = code(["var x: int = p[i] + i * 4;", "var y: int = i * 4 + 1;", "return x + y;"], size=17)
        src.next_to(head, DOWN, buff=0.35)
        b0 = ir_block("before", o["gvn_before"]["blocks"][0]["ins"], DATA, 17)
        b1 = ir_block("after", o["gvn_after"]["blocks"][0]["ins"], YES, 17)
        VGroup(b0, b1).arrange(RIGHT, buff=1.4, aligned_edge=UP).next_to(src, DOWN, buff=0.5)
        arr = Arrow(b0.get_right(), b1.get_left(), buff=0.25, color=GREY_B)
        same = [k for k, l in enumerate(o["gvn_before"]["blocks"][0]["ins"]) if "%i * 4" in l]
        how = VGroup(
            label(r"key each instruction by \ (operation, \ operand values)", font_size=20, color=GREY_A),
            label(r"a key seen before: \ reuse the earlier name", font_size=20, color=GREY_A),
            label("SSA keeps operand identities stable; reuse still needs a dominating definition", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=1.0)
        r0, r1, pct = measured(p["rows"], 4, 5)
        meas = label(rf"on the array Job: \ {r0:,} $\to$ {r1:,} instructions \ ({pct:+.0f}\%): \ "
                     r"\texttt{table[i]}'s address, \ computed once", font_size=20, color=YES).to_edge(DOWN,
                                                                                                    buff=0.35)
        with self.voiceover(
            (
            "Value numbering reuses an already available computation. This example forms i times four repeatedly. "
            "<bookmark mark='a'/> A key records a supported operation and its operand values. For selected "
            "commutative operations, canonical operand order exposes another equality. <bookmark mark='b'/> When "
            "the key matches an available earlier instruction, replace the later uses with that earlier result. "
            "<bookmark mark='c'/> Our global pass scopes the table while walking the dominator tree, so the "
            "reused definition is available on every path to its new use. SSA keeps operand identities stable, "
            "but does not make memory immutable. This pass does not merge loads; calls, traps and memory effects "
            "require their own legality arguments. <bookmark mark='d'/> On this recorded array Job, eliminating "
            "repeated table-address arithmetic reduces the instruction count by the amount shown. The percentage "
            "measures this workload and pass ordering, rather than all programs or elapsed time."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(b0), FadeIn(how[0]))
            vo.wait_until("b")
            self.play(*[Indicate(b0.lines[k], color=HEAD) for k in same], FadeIn(how[1]))
            self.play(GrowArrow(arr), FadeIn(b1))
            vo.wait_until("c")
            self.play(FadeIn(how[2]))
            vo.wait_until("d")
            self.play(FadeOut(how), FadeIn(meas))
        self.wait(0.3)
        self.clear_scene()

    def identities(self):
        head = label(r"Algebra, \ and its traps", font_size=34).to_edge(UP, buff=0.3)
        good = VGroup(*[mono(t, 20, YES) for t in ("x * 8   →  x << 3", "x * 1   →  x", "x + 0   →  x",
                                                    "4 * x   →  x * 4   (constants to the right)")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2)
        bad = VGroup(*[mono(t, 20, NO) for t in ("x / 2   →  x >> 1   ?", "(x + 1) > x   →  true   ?",
                                                  "x * 2 / 2   →  x   ?")]).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.2)
        VGroup(good, bad).arrange(DOWN, buff=0.6, aligned_edge=LEFT).next_to(head, DOWN, buff=0.5).to_edge(
            LEFT, buff=1.2)
        gl = label(r"always true on 32-bit integers", font_size=20, color=YES).next_to(good, RIGHT, buff=0.8)
        bl = VGroup(label(r"false for $x = -1$: \ $-1 / 2 = 0$, \ but $-1 \gg 1 = -1$", font_size=20, color=NO),
                    label(r"false when $x + 1$ overflows", font_size=20, color=NO),
                    label(r"false when $x \cdot 2$ overflows", font_size=20, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2)
        for b, r in zip(bl, bad):
            b.next_to(r, RIGHT, buff=0.6)
            b.align_to(gl, LEFT)
        foot = label(r"chapter 14: \ a solver checks such rules for all $2^{32}$ inputs at once", font_size=21,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover("Many small rewrites are pure algebra. <bookmark mark='a'/> Multiplying by eight is a shift left by three, which is cheaper. Multiplying by one, or adding zero, does nothing. Our strength pass also moves constants to the right, so that value numbering sees four times x and x times four as the same. <bookmark mark='b'/> But machine integers are not the integers of school. Dividing by two is not a shift right by one: minus one divided by two is zero, rounding toward zero, but minus one shifted right is still minus one. x plus one is not always more than x, because it can overflow. Every rewrite rule has to be true for all four billion values of x, including the awkward ones. <bookmark mark='c'/> In chapter fourteen a solver will check such rules for all of them at once.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(g) for g in good], lag_ratio=0.3), FadeIn(gl), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            for r, b in zip(bad, bl):
                self.play(FadeIn(r), FadeIn(b), run_time=0.8)
            vo.wait_until('c')
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def ordering(self):
        lv = load("llvm")
        head = label(r"Which order? \ The phase-ordering problem", font_size=34).to_edge(UP, buff=0.3)
        from explainer.cs.lang.compiler.opt import PIPELINE
        names = {"copyprop": r"copies", "sccp": r"SCCP", "strength": r"algebra", "gvn": r"GVN", "licm": r"LICM",
                 "ivsr": r"IVSR", "dce": r"DCE"}
        cols = {"copyprop": GREY_B, "sccp": YES, "strength": CTRL, "gvn": DATA, "licm": FUNC, "ivsr": FUNC,
                "dce": NO}
        chips = VGroup(*[region(1.25, 0.6, names[p], cols[p], font_size=19) for p in PIPELINE]).arrange(
            RIGHT, buff=0.12).next_to(head, DOWN, buff=0.6)
        if chips.width > 13:
            chips.scale_to_fit_width(13)
        cap = label(r"our \texttt{-O2}: \ eleven passes, \ some run twice", font_size=20, color=GREY_A).next_to(
            chips, DOWN, buff=0.2)
        pts = VGroup(
            label(r"each pass creates work for others: \ SCCP leaves copies, \ GVN leaves dead code", font_size=21,
                  color=GREY_A),
            label(r"the best order depends on the program; \ finding it is itself a search problem", font_size=21,
                  color=GREY_A),
            label(rf"opt \texttt{{-O2}} pipeline text: \ {lv['passes']} parsed names, \ {lv['distinct']} distinct",
                  font_size=22, color=FUNC),
            label(r"chosen by decades of measurement; \ machine learning now tunes some (chapter 15)",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(cap, DOWN, buff=0.6)
        with self.voiceover(f"Passes run in an order, and sometimes repeat. <bookmark mark='a'/> Our level-two pipeline lists {len(PIPELINE)} pass invocations. <bookmark mark='b'/> A pass creates opportunities for others: constant propagation can leave copies, value numbering can leave unused code, and loop motion changes which expressions dominate later uses. <bookmark mark='c'/> Selecting a useful sequence is the phase-ordering problem. The best choice depends on the input and the cost objective. <bookmark mark='d'/> For the recorded LLVM version and pipeline-printing command, our parser counts {lv['passes']} pass-name occurrences and {lv['distinct']} distinct names. This is a textual pipeline statistic, not a count of every per-function runtime invocation or a universal Clang constant. <bookmark mark='e'/> Production pipelines combine engineering measurements and heuristics; some decisions can also use learned policies.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in chips], lag_ratio=0.15), FadeIn(cap), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[0]))
            vo.wait_until('c')
            self.play(FadeIn(pts[1]))
            vo.wait_until('d')
            self.play(FadeIn(pts[2]))
            vo.wait_until('e')
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()
