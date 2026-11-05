from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, mono, region)


class Correct(VoiceoverScene):
    def construct(self):
        self.card()
        self.stakes()
        self.csmith()
        self.ours()
        self.rules()
        self.proofs()

    def card(self):
        card = chapter_card(14, r"Is the compiler right?", r"How would we know if it were not?", lit=(2011,),
                            extra=((2011, r"Kafka; \ Csmith"),), part=PART)
        with self.voiceover("Chapter fourteen. Is the compiler right?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def stakes(self):
        head = label(r"A miscompilation is a silent wrong answer", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"the source is right; \ the machine code is not", font_size=23, color=GREY_A),
            label(r"no crash, \ no warning: \ just a different number", font_size=23, color=GREY_A),
            label(r"every pass must preserve the meaning, \ on every program", font_size=23, color=HEAD),
            label(r"``every program'' includes ones no human would write", font_size=23, color=NO),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.6)
        ub = label(r"(and C's undefined behaviour, \ Part 11, \ lets the compiler assume it never happens)",
                   font_size=20, color=GREY_B).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A compiler bug is worse than most bugs. <bookmark mark='a'/> The source is right and the machine code "
            "is not. There is no crash and no warning, only a different answer, and the programmer will look "
            "everywhere except the compiler. <bookmark mark='b'/> Every pass must preserve the meaning of every "
            "program, <bookmark mark='c'/> and that includes strange programs no human would write, but that "
            "inlining and macros produce all the time. <bookmark mark='d'/> In C, undefined behaviour adds a "
            "twist, as Part 11 showed: the compiler may assume it never happens, so a program that relies on it can "
            "change meaning between optimization levels, and that is not a compiler bug."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("b")
            self.play(FadeIn(pts[2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[3]))
            vo.wait_until("d")
            self.play(FadeIn(ub))
        self.wait(0.3)
        self.clear_scene()

    def csmith(self):
        head = label(r"Csmith: \ random programs, \ many compilers", font_size=34).to_edge(UP, buff=0.3)
        gen = VGroup(region(3.0, 1.2, r"random C program", DATA, font_size=22),
                     label(r"no undefined behaviour", font_size=18, color=GREY_A))
        gen[1].next_to(gen[0], DOWN, buff=0.12)
        gen.move_to(LEFT * 4.6 + UP * 0.6)
        comps = VGroup(*[region(2.4, 0.6, t, CTRL, font_size=18) for t in (r"gcc \texttt{-O0}", r"gcc \texttt{-O3}",
                                                                           r"clang \texttt{-O2}", r"CompCert")]
                       ).arrange(DOWN, buff=0.25).move_to(LEFT * 0.8 + UP * 0.6)
        outs = VGroup(*[mono(t, 18, c) for t, c in (("checksum 7a1f", YES), ("checksum 7a1f", YES),
                                                     ("checksum 03c2", NO), ("checksum 7a1f", YES))])
        for o, c in zip(outs, comps):
            o.next_to(c, RIGHT, buff=0.6)
        arrs = VGroup(*[Arrow(gen.get_right(), c.get_left(), buff=0.08, color=GREY_D, stroke_width=1.5,
                              tip_length=0.12) for c in comps])
        vote = label(r"disagree? \ one of them is wrong", font_size=21, color=NO).next_to(outs, RIGHT, buff=0.4)
        facts = VGroup(
            label(r"Yang, Chen, Eide, Regehr \ (Utah, \ 2011): \ over 325 bugs in gcc and LLVM", font_size=21,
                  color=GREY_A),
            label(r"every compiler they tested could be made to crash \ or to emit wrong code", font_size=21,
                  color=GREY_A),
            label(r"except the proved parts of CompCert: \ no wrong-code bug found there", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How do you find such bugs? In 2011 a group at the University of Utah built Csmith. <bookmark "
            "mark='a'/> It generates random C programs, large and strange, but carefully free of undefined "
            "behaviour, so every program has exactly one correct output. <bookmark mark='b'/> Compile each with "
            "many compilers at many levels, run them all, and compare. <bookmark mark='c'/> If the outputs "
            "disagree, at least one compiler is wrong, and the program is a test case. <bookmark mark='d'/> They "
            "reported more than three hundred and twenty-five bugs in gcc and LLVM. Every compiler they tried "
            "could be made to crash or to produce wrong code, except in one place: the parts of CompCert that had "
            "been proved correct, where they found no wrong-code bugs at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(gen))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.2), FadeIn(comps))
            self.play(LaggedStart(*[FadeIn(o) for o in outs], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(Indicate(outs[2], color=NO), FadeIn(vote))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.5), run_time=3)
        self.wait(0.3)
        self.clear_scene()

    def ours(self):
        fz = load("fuzz")
        head = label(r"Our own fuzzer", font_size=34).to_edge(UP, buff=0.3)
        lines = [l if len(l) <= 58 else l[:56] + " …" for l in fz["sample"][7:27]]
        sample = code(lines, size=12, color=CODE).to_edge(LEFT, buff=0.4).shift(DOWN * 0.35)
        sl = label(r"one random Pebble program \ (an excerpt)", font_size=17, color=GREY_B).next_to(sample, UP,
                                                                                                buff=0.1)
        sl.align_to(sample, LEFT)
        total = fz["ran"] + fz["stuck"]
        pts = VGroup(
            label(r"bounded loops, \ in-range indices, \ divisors that are never zero", font_size=19, color=GREY_A),
            label(r"the reference: \ the IR interpreter, \ no optimizer", font_size=19, color=GREY_A),
            label(rf"{total} programs, \ about {fz['lines']:.0f} lines each; \ {fz['stuck']} ran too long, \ set aside",
                  font_size=19, color=GREY_A),
            label(rf"{fz['ran']} programs $\times$ 4 levels: \ {len(fz['mismatches'])} mismatches", font_size=22,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        found = fz["found_during_development"]
        bugs = VGroup(
            label(r"but while we built it, \ it found:", font_size=19, color=NO),
            label(r"\textbullet\ a parameter assigned in the entry block, \ never renamed into SSA", font_size=17,
                  color=GREY_A),
            label(rf"\qquad ({found[0]['programs_failing']} programs wrong)", font_size=17, color=GREY_B),
            label(r"\textbullet\ in the reference: \ dividing by zero gave $-1$, \ as on RISC-V; \ Pebble traps",
                  font_size=17, color=GREY_A),
            label(rf"\qquad ({found[1]['programs_failing']} programs wrong)", font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        if bugs.width > 6.2:
            bugs.scale_to_fit_width(6.2)
        bugs.next_to(pts, DOWN, buff=0.45).align_to(pts, LEFT)
        with self.voiceover(
            "We did the same to our own compiler. <bookmark mark='a'/> A generator writes random Pebble programs, "
            "with nested loops, arrays, pointers and globals. Every loop is bounded, every index is reduced into "
            "range, and every divisor is a square plus one, so it is never zero. <bookmark mark='b'/> The "
            "reference is the IR interpreter, which runs the program with no optimizer at all. <bookmark "
            "mark='c'/> We generated two hundred and forty programs, each about eighty lines. Fifty ran too long "
            "for the interpreter's step limit and were set aside. <bookmark mark='d'/> The other hundred and ninety, "
            "compiled at all four levels and run on the emulator, gave no mismatches. <bookmark mark='e'/> That was "
            "not true while the compiler was being built. The fuzzer found that a parameter assigned in the entry "
            "block was never renamed into SSA, which broke nine programs. And it found a bug in the reference "
            "itself: the interpreter assumed that dividing by zero gives minus one, as RISC-V does, but Pebble "
            "traps. A tester is only as good as its notion of the right answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sample), FadeIn(sl))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
            vo.wait_until("e")
            self.play(FadeIn(bugs))
        self.wait(0.3)
        self.clear_scene()

    def rules(self):
        so = load("superopt")
        head = label(r"Proving rewrite rules, \ for all $2^{32}$ inputs", font_size=34).to_edge(UP, buff=0.3)
        rows, cols = [], []
        for r in so["rules"]:
            rows.append([r["rule"].replace(">>u", ">>>"), "holds" if r["holds"] else "false",
                         "" if r["holds"] else f"x = {r['counterexample'][0]:,}"])
            cols.append([WHITE, YES if r["holds"] else NO, NO])
        tab = grid_table([r"rule, \ on 32-bit integers", r"z3 says", r"counterexample"], rows,
                         widths=[5.2, 1.6, 3.4], row_h=0.55, font_size=19, colors=cols, mono_cols=(0, 2)).next_to(
            head, DOWN, buff=0.5)
        how = VGroup(
            label(r"ask an SMT solver: \ is there any $x$ with \ $\mathrm{lhs}(x) \ne \mathrm{rhs}(x)$?",
                  font_size=21, color=GREY_A),
            label(r"``no'' is a proof; \ ``yes'' comes with the $x$", font_size=21, color=GREY_A),
            label(r"Alive \ (Lopes et al., \ 2015): \ 334 of LLVM's peephole rules checked; \ 8 were wrong",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Testing samples a few inputs. For the small algebraic rules of chapter seven we can do better, and "
            "check every input at once. <bookmark mark='a'/> Ask an SMT solver, here z3: is there any thirty-two-bit "
            "x for which the two sides differ? If the answer is no, the rule is proved. If yes, the solver hands "
            "back an x. <bookmark mark='b'/> Multiplying by eight is shifting by three: proved. Dividing by two is "
            "shifting right by one: false, at x equals minus one. The correct version adds the sign bit before "
            "shifting: proved. x plus one is greater than x: false at the largest integer, where it overflows. And "
            "x times three, divided by three, is x: false, at a number the solver found by itself. <bookmark "
            "mark='c'/> In 2015 the Alive project translated three hundred and thirty-four of LLVM's peephole "
            "rules into this form, and found eight that were wrong."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(how[:2]))
            vo.wait_until("b")
            self.play(FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]])
            for r in tab.cells[1:]:
                self.play(*[FadeIn(c) for c in r], run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(how[2]))
        self.wait(0.3)
        self.clear_scene()

    def proofs(self):
        head = label(r"From testing to proof", font_size=34).to_edge(UP, buff=0.3)
        ladder = [
            (r"differential testing", r"Csmith; \ our fuzzer", r"finds bugs; \ proves nothing", DATA),
            (r"rule checking", r"Alive; \ our z3 checks", r"proves each small rewrite", CTRL),
            (r"translation validation", r"Pnueli 1998; \ Necula 2000", r"proves each compilation, \ after the fact",
             YES),
            (r"a verified compiler", r"CompCert \ (Leroy, \ 2006--)", r"proves the compiler, \ once, \ for every "
                                                                     r"program", FUNC),
        ]
        rows = VGroup()
        for name, who, what, c in ladder:
            r = VGroup(region(3.4, 0.7, name, c, font_size=20), label(who, font_size=18, color=GREY_A),
                       label(what, font_size=18, color=WHITE)).arrange(RIGHT, buff=0.4)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.5)
        for r in rows:
            r[1].move_to([-1.1, r[0].get_y(), 0], aligned_edge=LEFT)
            r[2].move_to([2.2, r[0].get_y(), 0], aligned_edge=LEFT)
        rows.set_x(0)
        nxt = VGroup(
            label(r"CompCert's proof, \ in the Coq proof assistant: \ Part 54", font_size=21, color=HEAD),
            label(r"and a compiler that lies about \textit{itself} \ (Thompson, \ 1984): \ Part 55", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "These are rungs on a ladder. <bookmark mark='a'/> Differential testing finds bugs, but can never "
            "show there are none. <bookmark mark='b'/> Rule checking proves each small rewrite correct. <bookmark "
            "mark='c'/> Translation validation proves each compilation correct after the fact: a separate checker "
            "confirms that this output means the same as this input, and if it cannot, the build fails. <bookmark "
            "mark='d'/> And a verified compiler is proved correct once, for every program. Xavier Leroy's "
            "CompCert, a C compiler written and proved in the Coq proof assistant, is the landmark; Airbus uses it "
            "for flight software. <bookmark mark='e'/> How such proofs work is Part 54. And Part 55, the finale, "
            "asks the strangest question of all: Ken Thompson's compiler that lies about itself, and whether you "
            "can trust any compiler you did not write."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(nxt))
        self.wait(0.3)
        self.clear_scene()
