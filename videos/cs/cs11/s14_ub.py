from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, region)


class Undefined(VoiceoverScene):
    def construct(self):
        self.card()
        self.what()
        self.overflow()
        self.nullcheck()
        self.sanitizers()
        self.shadow()

    def card(self):
        card = chapter_card(13, r"Undefined behaviour", r"What may a compiler assume about your program?", part=PART)
        with self.voiceover("Chapter thirteen. Undefined behaviour."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def what(self):
        head = label(r"Behaviour the standard leaves undefined", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"signed integer overflow; \ reading past an array; \ dereferencing a null pointer; \ "
                  r"using freed memory", font_size=22, color=NO),
            label(r"the C standard says nothing about what happens: \ \textit{anything} is allowed", font_size=22,
                  color=GREY_A),
            label(r"why: \ machines differ \ (wrapping, \ trapping, \ saturating), \ and checks cost time", font_size=22,
                  color=GREY_A),
            label(r"the twist: \ an optimizer may assume it \textit{never happens}, \ and reason from that", font_size=23,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "C leaves some operations undefined. <bookmark mark='a'/> Overflowing a signed integer, reading past "
            "the end of an array, dereferencing a null pointer, using memory after freeing it. <bookmark mark='b'/> "
            "For these the standard does not say the program crashes, or gives a wrong answer. It says nothing at "
            "all: any behaviour is allowed. <bookmark mark='c'/> There were reasons. Machines handled overflow "
            "differently, and checking every array access costs time. <bookmark mark='d'/> But modern optimizers "
            "draw a sharper conclusion: since a correct program never does these things, the compiler may assume "
            "they never happen, and optimize on that assumption. We measured what that does on this computer."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def overflow(self):
        u = load("ub")
        head = label(r"Signed overflow, \ measured", font_size=34).to_edge(UP, buff=0.3)
        src = code(["int bigger(int x) { return x + 1 > x; }", "bigger(INT_MAX)",
                    "for (int i = 1; i > 0; i += 1000000000) n++;"], size=19, color=YES).next_to(head, DOWN, buff=0.4)
        rows = [[k, str(v["bigger"]), str(v["loop"])] for k, v in u.items()]
        t = grid_table([r"gcc", r"\texttt{bigger(INT\_MAX)}", r"loop trips"], rows, [3.0, 3.6, 2.4], row_h=0.55,
                       font_size=22, colors=[[CODE, NO, CTRL]] * len(rows), mono_cols=(0,)).next_to(src, DOWN,
                                                                                                buff=0.5)
        pts = VGroup(
            label(r"$x + 1 > x$ \ is ``always true'' \ if overflow cannot happen: \ the compiler answers 1 without "
                  r"looking", font_size=20, color=GREY_A),
            label(r"the loop: \ the same source, \ different trip counts at different optimization levels",
                  font_size=20, color=NO),
            label("\\texttt{-fwrapv}: gcc wrapping semantics for these signed operations", font_size=20,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "Signed overflow separates C semantics from a particular instruction's arithmetic. <bookmark "
            "mark='a'/> At INT_MAX, evaluating signed x plus one is undefined in ordinary C. <bookmark mark='b'/> "
            "The host instruction set has wrapping addition, but this expression is not required to compile into "
            "that instruction. gcc can return one for x plus one greater than x because every defined signed "
            "addition satisfies the comparison. <bookmark mark='c'/> The table records the loop-trip counts "
            "produced by these exact builds. Once the loop overflows, ordinary C imposes no portable trip count; "
            "optimization-level differences are observations, not language guarantees. <bookmark mark='d'/> gcc's "
            "fwrapv option supplies wrapping semantics for the relevant signed arithmetic in these examples. That "
            "implementation option changes the assumptions; it does not make unrelated bounds or lifetime "
            "violations defined."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            vo.wait_until("b")
            self.play(*[FadeIn(VGroup(*t.cells[r][:2])) for r in range(1, len(t.cells))], FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(t.cells[r][2]) for r in range(1, len(t.cells))], FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def nullcheck(self):
        u = load("ub")
        head = label(r"A null check, \ deleted", font_size=34).to_edge(UP, buff=0.3)
        src = code(["int deref(int *p) {", "    int v = *p;          // use it", "    if (!p) return -1;   // then check it",
                    "    return v;", "}"], size=19, color=YES).to_edge(LEFT, buff=0.6).shift(UP * 0.7)
        o0 = VGroup(label(r"\texttt{-O0}", font_size=20, color=GREY_A),
                    code([l.replace("\t", " ") for l in u["O0"]["deref_asm"]], size=14)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        o2 = VGroup(label(r"\texttt{-O2}", font_size=20, color=NO),
                    code([l.replace("\t", " ") for l in u["O2"]["deref_asm"]], size=16)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        VGroup(o0, o2).arrange(RIGHT, buff=0.8, aligned_edge=UP).to_edge(RIGHT, buff=0.6).shift(UP * 0.5)
        why = VGroup(
            label(r"\texttt{*p} came first, \ so $p \neq$ NULL \ ``must'' hold: \ the check is dead code", font_size=21,
                  color=GREY_A),
            label(r"2009: \ exactly this pattern removed a null check in the Linux kernel's TUN driver, \ and made it "
                  r"exploitable", font_size=21, color=NO),
            label(r"Linux now builds with \texttt{-fno-delete-null-pointer-checks}", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover("Second, a null check. <bookmark mark='a'/> This function reads through a pointer, and only then checks whether the pointer was null. <bookmark mark='b'/> Without optimization, gcc compiles both: the load, the comparison, the early return. <bookmark mark='c'/> With optimization, the whole function is one load and a return. The reasoning: the program already dereferenced p, and dereferencing null is undefined, so p cannot be null, so the check can never fire. <bookmark mark='d'/> This is not hypothetical. In 2009 exactly this pattern in the Linux kernel's network tunnel driver let the compiler delete a null check, and the result was exploitable. Linux has been built ever since with a flag that forbids this particular optimization. The lesson of the chapter: in C, the program you meant and the program you wrote can differ, and the optimizer will take the one you wrote at its word.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(src), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(o0))
            vo.wait_until('c')
            self.play(FadeIn(o2), FadeIn(why[0]))
            vo.wait_until('d')
            self.play(FadeIn(why[1]), FadeIn(why[2]))
        self.wait(0.3)
        self.clear_scene()

    def sanitizers(self):
        sa = load("sanitize")["cases"]
        head = label(r"Catching it as it happens: \ sanitizers", font_size=34).to_edge(UP, buff=0.3)
        rows = [(r"\texttt{x + 1} for the largest \texttt{int}", r"\texttt{-fsanitize=undefined}", "overflow", DATA),
                (r"write one element past a 64-byte \texttt{malloc}", r"\texttt{-fsanitize=address}", "heap", NO),
                (r"read a block after \texttt{free}", r"\texttt{-fsanitize=address}", "freed", CTRL),
                (r"write one byte past a stack array", r"\texttt{-fsanitize=address}", "stack", FUNC)]
        g = VGroup()
        for bug, flag, key, c in rows:
            rep = sa[key]["report"]
            where = sa[key]["where"]
            where = where.split(" is ", 1)[1] if " is " in where else ""
            body = VGroup(Text(rep[:78], font="DejaVu Sans Mono", font_size=15, color=c))
            if where:
                body.add(Text(where[:78], font="DejaVu Sans Mono", font_size=13, color=GREY_B))
            body.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            g.add(VGroup(VGroup(label(bug, font_size=20, color=GREY_A), label(flag, font_size=16, color=GREY_B))
                         .arrange(RIGHT, buff=0.3), body).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        foot = note(r"each report also names the source line, \ and for the heap, \ where the block was allocated",
                    font_size=17).to_edge(DOWN, buff=0.35)
        with self.voiceover("The practical defence is to catch undefined behaviour as it happens. <bookmark mark='a'/> Compile with the undefined-behaviour sanitizer, and our overflowing addition stops to report it: the largest int plus one cannot be represented in type int. <bookmark mark='b'/> AddressSanitizer catches memory errors: a write just past the end of a sixty-four-byte block from malloc, <bookmark mark='c'/> a read from a block already freed, <bookmark mark='d'/> and a write past an array on the stack, the very bug of the next chapter. Each report gives the address, the line of source, and for the heap, where the block was allocated.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, r in zip('abcd', g):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def shadow(self):
        b = load("sanitize")["bench"]
        w, m = b["words"]["slowdown"], b["malloc"]["slowdown"]
        head = label(r"How AddressSanitizer knows", font_size=34).to_edge(UP, buff=0.3)
        parts = [(r"red zone", 2, NO, 0.35, "fa"), (r"a 64-byte block", 8, YES, 0.25, "00"),
                 (r"red zone", 2, NO, 0.35, "fa"), (r"freed: \ in quarantine", 4, CTRL, 0.25, "fd"),
                 (r"red zone", 2, NO, 0.35, "fa")]
        U = 0.55
        mem, shadow = VGroup(), VGroup()
        for name, n8, c, fill, sh in parts:
            mem.add(region(n8 * U, 0.75, name, c, font_size=16, fill=fill))
            shadow.add(VGroup(*[region(U, 0.42, rf"\texttt{{{sh}}}", c, font_size=13, fill=0.12) for _ in range(n8)]
                              ).arrange(RIGHT, buff=0))
        mem.arrange(RIGHT, buff=0).move_to(UP * 1.5)
        shadow.arrange(RIGHT, buff=0).next_to(mem, DOWN, buff=1.0)
        ml = label(r"the program's heap", font_size=17, color=GREY_B).next_to(mem, UP, buff=0.12).align_to(mem, LEFT)
        sl = label(r"shadow memory: \ one byte for every 8", font_size=17, color=GREY_B).next_to(shadow, DOWN,
                                                                                                buff=0.12)
        sl.align_to(shadow, LEFT)
        maps = VGroup(*[Line(mem[1].get_bottom() + RIGHT * (k - 3.5) * U, shadow[1][k].get_top(), color=GREY_D,
                             stroke_width=1) for k in range(8)])
        chk = code(["schematic check: access stays within one 8-byte shadow group", "mov  (%rdi), %eax        # the program's load", "     ...preceded by:",
                    "s = shadow(addr >> 3)", "last = (addr & 7) + size - 1", "if (s != 0 && (s < 0 || last >= s)) report"], size=13)
        chk.to_edge(LEFT, buff=0.7).to_edge(DOWN, buff=1.25)
        cost = VGroup(label(rf"word count of \textit{{Pride and Prejudice}}: \ {w:.1f}$\times$ the time", font_size=20,
                            color=HEAD),
                      label(rf"nothing but \texttt{{malloc}} and \texttt{{free}}: \ {m:.0f}$\times$", font_size=20,
                            color=NO),
                      label("ASan: testing-oriented runtime; \\\\ assess overhead and security limitations", font_size=20, color=YES)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.6).to_edge(DOWN, buff=0.9)
        with self.voiceover(f"A typical AddressSanitizer implementation tracks addressability with shadow memory. <bookmark mark='a'/> It poisons allocation red zones and can quarantine freed blocks, delaying reuse. Detection still depends on instrumentation and what executes. <bookmark mark='b'/> In the usual one-to-eight mapping, zero means all eight bytes are addressable; positive values describe partially addressable groups, and negative poison codes describe inaccessible regions. <bookmark mark='c'/> The compiler instruments eligible accesses with checks of their shadow state and access size. The schematic check includes partial groups: a nonzero shadow byte is not automatically an error. <bookmark mark='d'/> Here the compiled word-count experiment takes {w:.1f} times the plain time, and the allocation-only loop {m:.0f} times. Those workload-specific launch-inclusive measurements are not universal slowdowns. Sanitizers are especially useful in testing and fuzzing. Clang describes the standard ASan runtime as a testing tool that is not hardened for production security. Other instrumentation choices have different tradeoffs. Passing a run does not prove memory safety.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(mem), FadeIn(ml), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Create(maps), FadeIn(shadow), FadeIn(sl))
            vo.wait_until('c')
            self.play(FadeIn(chk))
            vo.wait_until('d')
            self.play(LaggedStart(*[FadeIn(c) for c in cost], lag_ratio=0.4), run_time=2)
        self.wait(0.3)
        self.clear_scene()
