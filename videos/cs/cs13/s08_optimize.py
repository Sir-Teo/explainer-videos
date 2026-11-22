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


class Optimize(WatchScene):
    def construct(self):
        self.card()
        self.lattice()
        self.sccp()
        self.gvn()

    def card(self):
        self.chapter(7, r"Optimizations on SSA", r"Which work can be proved unnecessary?", lit=(1991,), extra=((1991, r"Wegman--Zadeck: \ SCCP"),), part=PART, said="Chapter seven. Optimizations on SSA.")

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
        self.ask(r"\texttt{a = 4; b = a * 8; if (b > 16) ... else ...} \\ Can the compiler delete the else branch?",
                 [r"no", r"yes"], 1,
                 say="a is four, b is a times eight, and if b is more than sixteen we do one thing, else another. Can the "
                     "compiler delete the else?",
                 reveal="Yes. b is always thirty-two, so the else can never run.")
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


