from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono


class Safety(VoiceoverScene):
    def construct(self):
        self.card()
        self.statistic()
        self.affine()
        self.borrow()
        self.proof()

    def card(self):
        card = chapter_card(3, r"Memory safety", r"Can the language rule the bug out?", lit=(2010, 2018),
                            extra=((2010, r"Rust's ownership"), (2018, r"RustBelt")), part=PART)
        with self.voiceover("Chapter three. Memory safety."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def statistic(self):
        head = label(r"Why this is worth the trouble", font_size=36).to_edge(UP, buff=0.3)
        bar = Rectangle(width=8.0, height=1.0, stroke_color=GREY_B, stroke_width=1.5, fill_color=BG, fill_opacity=1)
        bar.move_to([0, 1.1, 0])
        unsafe = Rectangle(width=8.0 * 0.70, height=1.0, stroke_width=0, fill_color=NO,
                           fill_opacity=0.8).align_to(bar, LEFT).set_y(1.1)
        safe = Rectangle(width=8.0 * 0.30, height=1.0, stroke_width=0, fill_color=YES,
                         fill_opacity=0.6).next_to(unsafe, RIGHT, buff=0).set_y(1.1)
        lu = label(r"memory-safety bugs \ ($\approx 70\%$)", font_size=20, color=WHITE).move_to(unsafe)
        ls = label(r"the rest", font_size=18, color=WHITE).move_to(safe)
        kinds = VGroup(
            label(r"buffer overflow \ \textbullet\ \ use-after-free", font_size=20, color=NO),
            label(r"double free \ \textbullet\ \ out-of-bounds read \ \textbullet\ \ uninitialised memory",
                  font_size=20, color=NO),
        ).arrange(DOWN, buff=0.2).next_to(bar, DOWN, buff=0.7)
        src = label(r"Microsoft \ (2019) \ and the Chromium project each reported \ $\approx 70\%$ \ of their serious "
                    r"security bugs were memory-safety bugs", font_size=18, color=GREY_A).next_to(kinds, DOWN,
                                                                                                  buff=0.5)
        with self.voiceover(
            "Canaries, W, xor, X and control-flow integrity all fight the overflow after it is written. The question "
            "of this chapter is whether we can stop writing it at all, and the reason the question matters is a "
            "single number. <bookmark mark='a'/> Around 2019 both Microsoft and the Chromium project reported the "
            "same thing: roughly seventy per cent of their serious security bugs were memory-safety bugs. "
            "<bookmark mark='b'/> Buffer overflows, use-after-free, double frees, reads past the end of an array, "
            "uninitialised memory. Not clever cryptographic breaks, but the same handful of mistakes, made over and "
            "over, in languages that let you make them. <bookmark mark='c'/> If a language could forbid that whole "
            "category, it would remove most of the vulnerabilities people actually ship."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bar), FadeIn(unsafe), FadeIn(safe), FadeIn(lu), FadeIn(ls))
            vo.wait_until("b")
            self.play(FadeIn(kinds))
            vo.wait_until("c")
            self.play(FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def affine(self):
        head = label(r"Ownership is an affine type \ (Part 14)", font_size=36).to_edge(UP, buff=0.3)
        r1 = MathTex(r"\dfrac{\Gamma, x\!:\!A,\ x\!:\!A \ \vdash\ e}{\Gamma, x\!:\!A \ \vdash\ e}",
                     font_size=40).move_to([-3.4, 0.9, 0])
        t1 = label(r"ordinary types: \ \textbf{contraction} \ --- \ use $x$ as often as you like", font_size=19,
                   color=GREY_A).next_to(r1, DOWN, buff=0.4)
        r2 = MathTex(r"\Gamma, x\!:\!A \ \vdash\ e \quad\Longrightarrow\quad x \text{ used at most once}",
                     font_size=36).move_to([-3.4, 0.9, 0])
        t2 = label(r"affine types: \ drop contraction \ --- \ each value has \textbf{one owner}", font_size=19,
                   color=HEAD).next_to(r2, DOWN, buff=0.4)
        # the value's life as a small state machine
        states = {}
        pos = {"owned": [3.6, 1.9], "shared": [1.9, 0.3], "mut": [5.3, 0.3], "moved": [3.6, -1.6]}
        cols = {"owned": YES, "shared": DATA, "mut": LAM, "moved": NO}
        txt = {"owned": r"owned", "shared": r"shared\\borrow (\&)", "mut": r"unique\\borrow (\&mut)",
               "moved": r"moved\\(gone)"}
        for k, p in pos.items():
            c = Circle(radius=0.55, color=cols[k], fill_color=BG, fill_opacity=1, stroke_width=2).move_to([*p, 0])
            lab = label(txt[k], font_size=15, color=cols[k]).move_to(c)
            states[k] = VGroup(c, lab)
        edges = VGroup(
            Arrow(states["owned"][0].get_left(), states["shared"][0].get_top(), buff=0.1, stroke_width=2,
                  color=GREY_B, max_tip_length_to_length_ratio=0.1),
            Arrow(states["owned"][0].get_right(), states["mut"][0].get_top(), buff=0.1, stroke_width=2,
                  color=GREY_B, max_tip_length_to_length_ratio=0.1),
            Arrow(states["shared"][0].get_top(), states["owned"][0].get_left(), buff=0.1, stroke_width=2,
                  color=GREY_D, max_tip_length_to_length_ratio=0.1),
            Arrow(states["mut"][0].get_top(), states["owned"][0].get_right(), buff=0.1, stroke_width=2,
                  color=GREY_D, max_tip_length_to_length_ratio=0.1),
            Arrow(states["owned"][0].get_bottom(), states["moved"][0].get_top(), buff=0.1, stroke_width=2.5,
                  color=NO, max_tip_length_to_length_ratio=0.1),
        )
        sm = VGroup(*states.values(), edges)
        smnote = label(r"borrows return; \ a move is final", font_size=16, color=GREY_A).next_to(
            states["moved"], DOWN, buff=0.2)
        with self.voiceover(
            "Rust's answer reaches back to Part 14 and the typed lambda calculus. <bookmark mark='a'/> In an "
            "ordinary type system there is a rule called contraction: if a variable is in scope you may use it as "
            "many times as you wish. <bookmark mark='b'/> Drop that rule and you get an affine type, where a value "
            "may be used at most once. Rust builds its whole discipline on this: every value has exactly one owner, "
            "and assigning it to someone else moves it, so the old name is no longer usable. "
            "<bookmark mark='c'/> You can lend a value out instead of moving it. A shared borrow gives many readers "
            "and no writer; a unique mutable borrow gives one writer and no one else. Every borrow ends, returning "
            "the value to its owner; but a move is final, and using what you moved is a compile error, not a "
            "crash."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(r1), FadeIn(t1))
            vo.wait_until("b")
            self.play(TransformMatchingTex(r1, r2), FadeOut(t1), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(sm), FadeIn(smnote))
        self.wait(0.4)
        self.clear_scene()

    def borrow(self):
        rows = load("borrow")["rows"]
        head = label(r"A tiny borrow checker, \ run on ten programs", font_size=36).to_edge(UP, buff=0.3)
        table, colors = [], []
        for r in rows:
            verdict = (r"accepted", YES) if r["accepted"] else (r"rejected", NO)
            reason = r["reason"] if r["reason"] else r"well-formed"
            table.append([r["name"], verdict[0], reason])
            colors.append([WHITE, verdict[1], GREY_A])
        g = grid_table([r"program", r"verdict", r"why"], table, widths=[4.6, 2.0, 6.0], row_h=0.44, font_size=16,
                       mono_cols=())
        for r, cr in zip(g.cells[1:], colors):
            for c, col in zip(r, cr):
                c.set_color(col)
        g.next_to(head, DOWN, buff=0.4).set_x(-0.6)
        chk = label(r"all ten verdicts match what Rust would say", font_size=19, color=HEAD).next_to(
            g, DOWN, buff=0.4)
        with self.voiceover(
            "To see what the rule buys, we built a toy borrow checker and ran it on ten small programs. "
            "<bookmark mark='a'/> It enforces four things, each the cause of a real class of bug. No use after a "
            "move, which would be a dangling reference. No two mutable borrows at once, which would be a data race. "
            "No shared and mutable borrow together, so no one reads a value while another is changing it. And no "
            "reference outliving the value it points at, which is use-after-free by another name. "
            "<bookmark mark='b'/> Each rejected program is rejected with a reason, at compile time, and each sound "
            "one is accepted; moving a value and then using the destination is fine, lending it within its lifetime "
            "is fine. <bookmark mark='c'/> This is the borrow checker in miniature: it turns the whole seventy per "
            "cent into errors the compiler catches before the program ever runs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g.cells[0][0]), FadeIn(g.cells[0][1]), FadeIn(g.cells[0][2]), FadeIn(g.rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*g.cells[i])) for i in range(1, len(rows) + 1)],
                                  lag_ratio=0.15), run_time=3.5)
            vo.wait_until("c")
            self.play(FadeIn(chk))
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        head = label(r"What is proved, \ and what is not", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            VGroup(label(r"the guarantee", font_size=22, color=YES),
                   wrapped_label(r"a program the checker accepts has no use-after-free, \ no double free, \ no data "
                                 r"race, \ no dangling pointer \ --- \ by construction", 5.4, font_size=18,
                                 color=GREY_A)).arrange(DOWN, buff=0.2),
            VGroup(label(r"\texttt{unsafe}", font_size=22, color=NO),
                   wrapped_label(r"an escape hatch for raw pointers, \ needed to \textit{build} the safe "
                                 r"abstractions; \ the danger is penned into blocks you can audit", 5.4,
                                 font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2),
        ).arrange(RIGHT, buff=0.8).next_to(head, DOWN, buff=0.5)
        rb = wrapped_label(r"\textbf{RustBelt} \ (Jung et al., 2018): \ a machine-checked proof that the type system "
                           r"is sound \textit{even with} the \texttt{unsafe} inside the standard library's "
                           r"abstractions \ --- \ the trusted base made small and then verified \ (Part 54)", 12.6,
                           font_size=20, color=HEAD).next_to(tiles, DOWN, buff=0.6)
        foot = wrapped_label(r"not a cure-all: \ logic errors, \ leaks and the \texttt{unsafe} core remain; \ and "
                             r"billions of lines of C and C++ will not rewrite themselves \ (the frontier)", 12.6,
                             font_size=20, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "What exactly has been proved? <bookmark mark='a'/> A program the borrow checker accepts has, by "
            "construction, no use-after-free, no double free, no data race and no dangling pointer. The absence is "
            "guaranteed, not merely tested. <bookmark mark='b'/> But some things genuinely need raw pointers, so "
            "Rust keeps an escape hatch, marked unsafe, and you use it to build the safe data structures everyone "
            "else relies on. The danger is not removed; it is penned into small blocks a human can audit. "
            "<bookmark mark='c'/> And here the series closes a loop. In 2018 the RustBelt project gave a "
            "machine-checked proof that the type system stays sound even accounting for that unsafe code inside the "
            "standard library, exactly the Part 54 idea of shrinking the trusted base and then verifying it. "
            "<bookmark mark='d'/> It is not a cure-all. Logic errors remain, the unsafe core must still be right, and "
            "the world's existing C and C plus plus will not rewrite itself, which is a problem we leave for the "
            "frontier."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tiles[0]))
            vo.wait_until("b")
            self.play(FadeIn(tiles[1]))
            vo.wait_until("c")
            self.play(FadeIn(rb))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES, PART, mono)
