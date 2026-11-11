from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import tree
from videos.cs.cs13.common import (CODE, CTRL, DATA, DEMO_POS, FUNC, HEAD, NO, PART, YES, cfg_view, code, load,
                                   mono, region)


DEMO_SRC = ["fn total(a: *int, n: int) -> int {", "    var s: int = 0;", "    var i: int = 0;", "    while i < n {",
            "        if a[i] > 0 { s = s + a[i]; }", "        else { s = s - 1; }", "        i = i + 1;", "    }",
            "    return s;", "}"]


def demo_source(size=15):
    return code(DEMO_SRC, size=size, color=CODE)


class IR(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.control()
        self.blocks()
        self.real()

    def card(self):
        card = chapter_card(3, r"Three-address code and the control-flow graph", r"What does the middle of a "
                            r"compiler see?", lit=(1970,), extra=((1970, r"Allen: \ control-flow analysis"),),
                            part=PART)
        with self.voiceover("Chapter three. Three-address code and the control-flow graph."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def three(self):
        head = label(r"One operation per line", font_size=36).to_edge(UP, buff=0.3)
        expr = mono("s = s + a[i];", 22, CODE).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        t = tree(("=", ["s", ("+", ["s", ("[ ]", ["a", "i"])])]), dx=0.9, dy=0.85, font_size=22)
        t.next_to(expr, DOWN, buff=0.5).align_to(expr, LEFT).shift(RIGHT * 0.3)
        lines = ["%t8  = %i * 4", "%t9  = %a + %t8", "%t10 = load [%t9]", "%t11 = %s + %t10", "%s   = %t11"]
        notes = [r"scale the index: \ an \texttt{int} is 4 bytes", r"the element's address",
                 r"read memory", r"the addition", r"the assignment"]
        rows = VGroup(*[VGroup(mono(l, 20, YES), label(n, font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.5)
                        for l, n in zip(lines, notes)]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for r in rows:
            r[1].move_to([r[0].get_left()[0] + 3.0, r[0].get_y(), 0], aligned_edge=LEFT)
        rows.move_to([2.2, 0.3, 0])
        cap = label("arithmetic core: one result and at most two inputs", font_size=22, color=HEAD).to_edge(
            DOWN, buff=1.0)
        cap2 = label(r"\texttt{\%t}: \ temporaries, \ as many as we like \ --- \ registers of an imaginary machine",
                     font_size=20, color=GREY_A).next_to(cap, DOWN, buff=0.2)
        with self.voiceover(
            (
            "Our middle end uses simple instructions grouped into basic blocks. Other compilers may use different "
            "tree or graph representations. <bookmark mark='a'/> Take s equals s plus a of i. Its syntax tree "
            "contains an assignment, an addition and an array index. <bookmark mark='b'/> Lowering gives the "
            "intermediate results names: scale i by four for an integer element, add the array address, load, add "
            "to s, and assign the result. <bookmark mark='c'/> The arithmetic has the familiar three-address "
            "shape: a destination and up to two inputs. Calls, branches, stores and later phi functions have "
            "their own operand conventions; the name is not a universal arity rule for every IR instruction. "
            "<bookmark mark='d'/> The percent names denote values or virtual registers. We can introduce as many "
            "as the translation needs, leaving the problem of fitting live values into physical registers to the "
            "back end."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(expr))
            vo.wait_until("a")
            self.play(FadeIn(t))
            vo.wait_until("b")
            for r in rows:
                self.play(FadeIn(r, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(cap))
            vo.wait_until("d")
            self.play(FadeIn(cap2))
        self.wait(0.3)
        self.clear_scene()

    def control(self):
        d = load("ir")
        src = demo_source().to_edge(LEFT, buff=0.4).shift(UP * 0.6)
        head = label(r"Control becomes jumps", font_size=30).to_corner(UL, buff=0.35)
        cfg = cfg_view(d["func"], DEMO_POS, size=12, at=RIGHT * 3.0 + DOWN * 0.1)
        B = cfg.blocks
        rules = VGroup(
            label(r"\texttt{while c \{ body \}}: \ test at the top, \ jump back from the bottom", font_size=17,
                  color=GREY_A),
            label(r"\texttt{if c \{ \} else \{ \}}: \ two branches that meet again", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(src, DOWN, buff=0.45).align_to(src, LEFT)
        loop_hl = VGroup(B["while1"].box, B["body2"].box, B["then5"].box, B["else7"].box, B["endif6"].box)
        with self.voiceover(
            "Control flow is lowered the same way. Here is a small function, total, which adds up the positive "
            "entries of an array and subtracts one for each other entry. <bookmark mark='a'/> The entry block sets s "
            "and i to zero. The while loop becomes a block that tests i against n and branches either into the "
            "body or out to the exit. <bookmark mark='b'/> The body loads a of i and tests it. The if becomes two "
            "blocks, then and else, which meet again at endif. <bookmark mark='c'/> And endif increments i and "
            "jumps back to the test. Every structured statement turns into labelled blocks and branches between "
            "them. <bookmark mark='d'/> Notice that then and else both load a of i again, as the source said. A "
            "naive translation repeats work. The optimizer will remove some of it, and we will see what it misses."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(B["entry"]), FadeIn(B["while1"]), GrowArrow(cfg.edges[("entry", "while1")]),
                      FadeIn(B["endwhile3"]), GrowArrow(cfg.edges[("while1", "endwhile3")]))
            self.play(FadeIn(rules[0]))
            vo.wait_until("b")
            self.play(FadeIn(B["body2"]), GrowArrow(cfg.edges[("while1", "body2")]))
            self.play(FadeIn(B["then5"]), FadeIn(B["else7"]), GrowArrow(cfg.edges[("body2", "then5")]),
                      GrowArrow(cfg.edges[("body2", "else7")]), FadeIn(rules[1]))
            vo.wait_until("c")
            self.play(FadeIn(B["endif6"]), GrowArrow(cfg.edges[("then5", "endif6")]),
                      GrowArrow(cfg.edges[("else7", "endif6")]))
            self.play(Create(cfg.edges[("endif6", "while1")]), run_time=1.5)
            vo.wait_until("d")
            self.play(Indicate(B["body2"].lines[2], color=HEAD), Indicate(B["then5"].lines[2], color=HEAD))
        self.wait(0.3)
        self.clear_scene()

    def blocks(self):
        d = load("ir")
        p = load("pipeline")
        cfg = cfg_view(d["func"], DEMO_POS, size=12, at=RIGHT * 3.0 + DOWN * 0.1)
        head = label(r"Basic blocks, \ and the graph", font_size=30).to_corner(UL, buff=0.35)
        defs = VGroup(
            label(r"a \textbf{basic block}: \ a straight run of instructions", font_size=20, color=GREY_A),
            label("normal flow: top entry, bottom transfer; traps or nonreturning calls can interrupt", font_size=20, color=GREY_A),
            label(r"a \textbf{leader} starts one: \ the first instruction,", font_size=20, color=GREY_A),
            label(r"every jump target, \ and whatever follows a jump", font_size=20, color=GREY_A),
            label(r"the \textbf{control-flow graph}: \ blocks as nodes,", font_size=20, color=HEAD),
            label(r"possible jumps as edges", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(head, DOWN, buff=0.4).align_to(head, LEFT)
        stats = VGroup(
            label(r"the whole list Job:", font_size=20, color=GREY_B),
            label(rf"{p['ir']} instructions \ in \ {p['blocks']} blocks", font_size=22, color=YES),
            label(r"a loop is a cycle in the graph", font_size=20, color=CTRL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(defs, DOWN, buff=0.5).align_to(defs, LEFT)
        back = cfg.edges[("endif6", "while1")]
        with self.voiceover(
            (
            "The graph's straight-line pieces are basic blocks. <bookmark mark='a'/> Under normal control flow, "
            "entry is at the first instruction and transfer is at the terminator. A trap, exception or "
            "nonreturning call can prevent later instructions from running, so entering a block does not "
            "unconditionally guarantee that every instruction finishes. Leaders include the first instruction, "
            "branch targets and instructions after transfers; richer exception models add their own boundaries. "
            "<bookmark mark='b'/> A control-flow graph has blocks as nodes and possible transfers as edges. "
            "Frances Allen's work helped establish compiler control-flow analysis. <bookmark mark='c'/> The "
            "displayed whole-Job counts come from our actual lowered representation. <bookmark mark='d'/> Cycles "
            "identify repeated control paths. Dominance later isolates natural loops; profiling and input "
            "behavior determine which cycles dominate the execution cost."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(cfg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in defs[:4]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(defs[4:]))
            self.play(*[Indicate(e, color=HEAD) for e in cfg.edges.values()], run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(stats[:2]))
            vo.wait_until("d")
            self.play(FadeIn(stats[2]), back.animate.set_color(CTRL))
            self.play(*[B.box.animate.set_stroke(CTRL, 3) for k, B in cfg.blocks.items()
                        if k in ("while1", "body2", "then5", "else7", "endif6")])
        self.wait(0.3)
        self.clear_scene()

    def real(self):
        lv = load("llvm")
        head = label(r"Real compilers do the same", font_size=34).to_edge(UP, buff=0.3)
        ours = code(["%t8  = %i * 4", "%t9  = %a + %t8", "%t10 = load [%t9]", "%t11 = %t10 > 0",
                     "if %t11 br then5 else else7"], size=16, color=YES)
        body = lv["ssa"][lv["ssa"].index("5:"):lv["ssa"].index("10:")]
        theirs = code(body, size=16, color=FUNC)
        VGroup(ours, theirs).arrange(DOWN, buff=0.9, aligned_edge=LEFT).move_to(DOWN * 0.1)
        lo = label(r"ours: \ the body block of \texttt{total}", font_size=20, color=YES).next_to(ours, UP, buff=0.12)
        lo.align_to(ours, LEFT)
        lt = label(r"LLVM IR, \ from clang, \ for the same function written in C", font_size=20,
                   color=FUNC).next_to(theirs, UP, buff=0.12).align_to(theirs, LEFT)
        foot = label("GIMPLE and LLVM: register-like IR; Java bytecode: stack-based", font_size=21,
                     color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover("We can compare the same function in an industrial compiler. <bookmark mark='a'/> Here is our body block. <bookmark mark='b'/> Beside it is the LLVM IR emitted by the recorded Clang build for the C version. It extends the index for this target's pointer arithmetic, computes an element address with getelementptr, loads, compares and branches. The address calculation does not itself access memory. <bookmark mark='c'/> GCC's GIMPLE and LLVM IR also expose simple operations and explicit control flow, though their instructions, types and semantics differ. Java bytecode is stack based; a JIT can translate it into a different internal representation for optimization.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(lo), FadeIn(ours), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(lt), FadeIn(theirs))
            vo.wait_until('c')
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
