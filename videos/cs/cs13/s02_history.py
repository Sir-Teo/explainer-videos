from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load, region


class History(VoiceoverScene):
    def construct(self):
        self.card()
        self.fortran()
        self.shape()
        self.retarget()
        self.ours()

    def card(self):
        card = chapter_card(1, r"FORTRAN, and the shape of a compiler", r"Can a program write code as good as ours?",
                            lit=(1952, 1957), part=PART)
        with self.voiceover("Chapter one. FORTRAN, and the shape of a compiler."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def fortran(self):
        head = label(r"Automatic programming, \ 1952--1957", font_size=36).to_edge(UP, buff=0.35)
        a0 = VGroup(label(r"1952: \ Grace Hopper's A-0", font_size=27, color=DATA),
                    label(r"subroutines from a library, \ stitched together by call number", font_size=22,
                          color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        doubt = VGroup(label(r"the general view", font_size=27, color=NO),
                       label(r"``automatic'' code would be far too slow; \ real programmers write machine code",
                             font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        ft = VGroup(label(r"1954--1957: \ John Backus's team at IBM, \ FORTRAN for the 704", font_size=27,
                          color=YES),
                    label(r"delivered April 1957, \ about 18 person-years of work", font_size=22, color=GREY_A),
                    label(r"it simulated the program's flow to guess which loops ran most, \ and gave them the "
                          r"704's three index registers", font_size=22, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1)
        col = VGroup(a0, doubt, ft).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.5)
        col.to_edge(LEFT, buff=0.7)
        quote = VGroup(
            label(r"``if FORTRAN were to translate any reasonable scientific source program", font_size=21,
                  color=HEAD),
            label(r"into an object program only half as fast as its hand-coded counterpart,", font_size=21,
                  color=HEAD),
            label(r"then acceptance of our system would be in serious danger.''", font_size=21, color=HEAD),
            label(r"--- John Backus, \ 1978", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_edge(DOWN, buff=0.45)
        frame = SurroundingRectangle(quote, color=HEAD, buff=0.2, corner_radius=0.1, stroke_width=1.5)
        with self.voiceover("In the early nineteen fifties, programs were written in machine code, by hand. <bookmark mark='a'/> In 1952 Grace Hopper's A-0 system stitched together subroutines from a library by number, and she called it a compiler: it compiled a program out of pieces. <bookmark mark='b'/> But most programmers were sure that anything automatic would produce code far too slow to use. Machine time cost more than programmer time, and the experts wrote tight code. <bookmark mark='c'/> John Backus's team at IBM set out to prove them wrong. Their FORTRAN compiler for the IBM 704 was delivered in April 1957, after about eighteen person-years of work, and most of that work went into optimization. It even simulated the flow of the program to estimate which loops ran most often, and gave those loops the machine's three index registers. <bookmark mark='d'/> Backus explained why, twenty years later: if FORTRAN produced programs only half as fast as hand-coded ones, nobody would have used it. The language was the easy part. The hard part was the promise that the code would be nearly as good as an expert's. That promise is the subject of this part.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(a0, shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(doubt, shift=RIGHT * 0.1))
            vo.wait_until('c')
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in ft], lag_ratio=0.5), run_time=2.5)
            vo.wait_until('d')
            self.play(FadeIn(quote), Create(frame))
        self.wait(0.5)
        self.clear_scene()

    def shape(self):
        head = label("A common compiler architecture", font_size=36).to_edge(UP, buff=0.35)
        spec = [
            (r"front end", DATA, [r"lexing and parsing \ (Part 12)", r"names, \ scopes, \ types",
                                 r"lowering to an IR"], r"knows the language"),
            (r"middle end", YES, [r"the control-flow graph", r"SSA, \ dataflow", r"optimizations"],
             "shared analyses"),
            (r"back end", FUNC, [r"instruction selection", r"register allocation", r"scheduling, \ emission"],
             r"knows the machine"),
        ]
        cols = VGroup()
        for name, c, items, who in spec:
            box = region(3.6, 0.8, name, c, font_size=26)
            its = VGroup(*[label(t, font_size=20, color=GREY_A) for t in items]).arrange(DOWN, buff=0.15)
            its.next_to(box, DOWN, buff=0.3)
            w = label(who, font_size=20, color=c).next_to(its, DOWN, buff=0.35)
            cols.add(VGroup(box, its, w))
        cols.arrange(RIGHT, buff=0.55).move_to(UP * 0.2)
        arrows = VGroup(*[Arrow(cols[k][0].get_right(), cols[k + 1][0].get_left(), buff=0.06, color=GREY_B)
                          for k in range(2)])
        src = label(r"source text", font_size=20, color=CODE).next_to(cols[0][0], UP, buff=0.35)
        out = label(r"machine code", font_size=20, color=CODE).next_to(cols[2][0], UP, buff=0.35)
        ir_l = label(r"the IR: \ intermediate representation", font_size=20, color=YES).next_to(cols[1][0], UP,
                                                                                               buff=0.35)
        foot = label(r"each stage is a function from one representation of the program to another", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover("A common compiler architecture has three broad parts. <bookmark mark='a'/> The front end understands the source language. It lexes and parses, checks names and types, and translates the tree into an intermediate representation, or IR. <bookmark mark='b'/> The middle end analyzes and transforms that representation. Shared optimizations can serve several languages and machines, although some still depend on source semantics or target costs. <bookmark mark='c'/> The back end chooses target instructions, assigns registers, schedules work and emits assembly or machine code. Real compilers may interleave these stages or use several IRs. <bookmark mark='d'/> The organizing principle is a sequence of representations with precise meanings. Each translation must preserve the behaviors required by the source and target semantics.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(src), FadeIn(cols[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(GrowArrow(arrows[0]), FadeIn(ir_l), FadeIn(cols[1]))
            vo.wait_until('c')
            self.play(GrowArrow(arrows[1]), FadeIn(out), FadeIn(cols[2]))
            vo.wait_until('d')
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def retarget(self):
        head = label(r"Why the middle: \ $M$ languages, \ $N$ machines", font_size=36).to_edge(UP, buff=0.35)
        langs = ["C", "C++", "Rust", "Swift", "Fortran"]
        machs = ["x86-64", "ARM", "RISC-V", "GPU"]

        def side(names, x, c):
            return VGroup(*[region(1.6, 0.5, n, c, font_size=19) for n in names]).arrange(DOWN, buff=0.22).move_to(
                [x, -0.3, 0])
        L1, M1 = side(langs, -5.6, DATA), side(machs, -1.8, FUNC)
        mesh = VGroup(*[Line(a.get_right(), b.get_left(), color=NO, stroke_width=1.2) for a in L1 for b in M1])
        t1 = label(rf"${len(langs)} \times {len(machs)} = {len(langs) * len(machs)}$ compilers", font_size=24,
                   color=NO).next_to(VGroup(L1, M1), DOWN, buff=0.35)
        L2, M2 = side(langs, 1.6, DATA), side(machs, 5.9, FUNC)
        hub = region(1.3, 1.0, r"IR", YES, font_size=26).move_to([3.75, -0.3, 0])
        spokes = VGroup(*[Line(a.get_right(), hub.get_left(), color=YES, stroke_width=1.5) for a in L2],
                        *[Line(hub.get_right(), b.get_left(), color=YES, stroke_width=1.5) for b in M2])
        t2 = label(rf"${len(langs)} + {len(machs)} = {len(langs) + len(machs)}$ halves", font_size=24,
                   color=YES).next_to(VGroup(L2, M2), DOWN, buff=0.35)
        hist = label(r"proposed as UNCOL in 1958; \ made real by GCC (1987) and LLVM (2004)", font_size=21,
                     color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover("Why use a shared intermediate representation? <bookmark mark='a'/> Five languages and four machines suggest twenty direct translation combinations. Maintaining each separately would duplicate much of the work. <bookmark mark='b'/> A shared IR lets us organize the interfaces as five front ends and four back ends, with reusable analyses and optimizations in between. Nine interfaces do not imply nine equal-sized jobs: language features, runtime support and target constraints still need engineering. <bookmark mark='c'/> UNCOL proposed a universal intermediate language in 1958. Later retargetable systems, including GCC and LLVM, made related ideas practical at scale. Modern language implementations can share compiler infrastructure without having identical semantics or optimization needs.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(L1), FadeIn(M1), run_time=0.6)
            vo.wait_until('a')
            self.play(Create(mesh), run_time=1.5)
            self.play(FadeIn(t1))
            vo.wait_until('b')
            self.play(FadeIn(L2), FadeIn(M2), FadeIn(hub))
            self.play(Create(spokes), run_time=1.2)
            self.play(FadeIn(t2))
            vo.wait_until('c')
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    def ours(self):
        p = load("pipeline")
        head = label(r"Our compiler, \ and the Job through it", font_size=36).to_edge(UP, buff=0.3)
        stages = [
            (r"source", f"{p['chars']:,}", r"characters", CODE, None),
            (r"lexer", f"{p['tokens']}", r"tokens", DATA, r"Part 12"),
            (r"parser", f"{p['nodes']}", r"tree nodes", DATA, r"Part 12"),
            (r"checker", r"5", r"functions typed", DATA, r"check.py"),
            (r"lowering", f"{p['ir']}", rf"IR instructions, \ {p['blocks']} blocks", YES, r"lower.py"),
            (r"SSA", f"{p['phis']}", r"$\phi$ functions", YES, r"ssa.py"),
            (r"optimizer", f"{p['ir_optimized']}", r"IR instructions", YES, r"opt.py"),
            (r"back end", f"{p['asm']}", rf"machine instructions, \ {p['bytes']:,} bytes", FUNC, r"codegen.py"),
        ]
        rows = VGroup()
        for name, num, what, c, where in stages:
            r = VGroup(label(name, font_size=26, color=c), label(num, font_size=28, color=WHITE),
                       label(what, font_size=24, color=GREY_A),
                       label(where or "", font_size=20, color=GREY_B) if where else VGroup())
            r[0].move_to([-5.2, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-1.7, 0, 0], aligned_edge=RIGHT)
            r[2].move_to([-1.3, 0, 0], aligned_edge=LEFT)
            if where:
                r[3].move_to([4.4, 0, 0], aligned_edge=LEFT)
            rows.add(r)
        rows.arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.5)
        for r, (_, _, _, _, where) in zip(rows, stages):
            r[0].align_to([-5.2, 0, 0], LEFT)
            r[1].align_to([-1.7, 0, 0], RIGHT)
            r[2].align_to([-1.3, 0, 0], LEFT)
            if where:
                r[3].align_to([4.4, 0, 0], LEFT)
        spine = Arrow(rows[0].get_left() + LEFT * 0.35 + UP * 0.1, rows[-1].get_left() + LEFT * 0.35 + DOWN * 0.1,
                      buff=0, color=GREY_D, stroke_width=2, max_tip_length_to_length_ratio=0.04)
        spine.set_x(-5.55)
        foot = label("reproducible compiler demonstrations; historical and research claims have cited sources",
                     font_size=24, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(f"Here is the linked-list Job passing through our compiler. <bookmark mark='a'/> Its {p['chars']:,} source characters become {p['tokens']} tokens and {p['nodes']} syntax-tree nodes. <bookmark mark='b'/> After checking names and types, lowering produces {p['ir']} intermediate instructions in {p['blocks']} blocks. SSA construction inserts {p['phis']} phis. <bookmark mark='c'/> The final recorded optimizer configuration leaves {p['ir_optimized']} intermediate instructions. Inlining, loop tests and other transformations can increase static size while trying to improve execution; smaller source or IR is not the sole objective. <bookmark mark='d'/> The backend emits {p['asm']} machine instructions occupying {p['bytes']:,} bytes in this recorded count. The instructions execute repeatedly, so static code size differs from dynamic work. <bookmark mark='e'/> These demonstrations are reproducible computations. Historical events and general mathematical results require their cited sources and assumptions as well.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.4), GrowArrow(spine), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(LaggedStart(*[FadeIn(r) for r in rows[3:6]], lag_ratio=0.5), run_time=3)
            vo.wait_until('c')
            self.play(FadeIn(rows[6]))
            vo.wait_until('d')
            self.play(FadeIn(rows[7]))
            vo.wait_until('e')
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
