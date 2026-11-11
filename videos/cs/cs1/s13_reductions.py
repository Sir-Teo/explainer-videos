from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import ADV, CODE, CTRL, DATA, HEAD, HIST, LIMIT, NO, PART, YES


class Reductions(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.blank()
        self.gallery()
        self.rice()
        self.practice()

    def card(self):
        card = chapter_card(12, r"Reductions", r"If one problem is impossible, which others are?", lit=(1936,),
                            part=PART)
        with self.voiceover("Chapter twelve. Reductions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        inst = node_box(r"an instance \\ $\langle M, w \rangle$ \ of HALT", CODE, font_size=26)
        f = node_box(r"transform \\ (a program)", CTRL, font_size=26)
        b = node_box(r"an instance \\ of problem $B$", DATA, font_size=26)
        dec = node_box(r"a decider \\ for $B$?", HEAD, font_size=26)
        ans = node_box(r"the answer \\ for HALT", YES, font_size=26)
        row = VGroup(inst, f, b, dec, ans).arrange(RIGHT, buff=0.55).move_to(UP * 0.6)
        if row.width > 13.4:
            row.width = 13.4
        arr = VGroup(*[Arrow(x.get_right(), y.get_left(), buff=0.08, color=GREY_B) for x, y in zip(row, row[1:])])
        whole = DashedVMobject(SurroundingRectangle(VGroup(f, b, dec), buff=0.25, color=ADV, corner_radius=0.15),
                               num_dashes=60)
        wl = label(r"together: \ a decider for HALT, \ which cannot exist", font_size=28, color=ADV).next_to(whole, DOWN,
                                                                                                          buff=0.3)
        concl = label(r"so $B$ has no decider either: \ HALT \textit{reduces} to $B$", font_size=32, color=LIMIT)
        concl.to_edge(DOWN, buff=0.5)
        head = label(r"Borrowing an impossibility", font_size=40).to_edge(UP, buff=0.4)
        with self.voiceover(
            "One impossible problem gives many. Suppose you want to show that some problem B has no decider. "
            "<bookmark mark='a'/> Find a program that turns any halting question, a machine and an input, into a "
            "question about B, with the same answer. <bookmark mark='b'/> Then if B had a decider, you could chain them: "
            "transform, then decide. That would decide halting, which is impossible. <bookmark mark='c'/> So B has no "
            "decider either. This is called a reduction: halting reduces to B. It is the most used tool in this whole "
            "theory, and Part 26 runs on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(inst))
            vo.wait_until("a")
            self.play(GrowArrow(arr[0]), FadeIn(f), GrowArrow(arr[1]), FadeIn(b))
            vo.wait_until("b")
            self.play(GrowArrow(arr[2]), FadeIn(dec), GrowArrow(arr[3]), FadeIn(ans))
            self.play(Create(whole), FadeIn(wl))
            vo.wait_until("c")
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blank(self):
        head = label(r"Does $M$ halt when started on a blank tape?", font_size=38).to_edge(UP, buff=0.4)
        mw = VGroup(node_box(r"write $w$ \\ on the tape", DATA, font_size=28), node_box(r"rewind", GREY_B, font_size=28),
                    node_box(r"run $M$", CODE, font_size=28)).arrange(RIGHT, buff=0.6)
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B) for a, b in zip(mw, mw[1:])])
        frame_ = SurroundingRectangle(VGroup(mw, arr), buff=0.35, color=CTRL, corner_radius=0.2)
        name = label(r"the machine $M_w$", font_size=30, color=CTRL).next_to(frame_, UP, buff=0.15)
        g = VGroup(mw, arr, frame_, name).move_to(UP * 0.4)
        claim = cmath(r"M_w", r"\text{ halts on a blank tape}", r"\iff", r"M", r"\text{ halts on } w", font_size=38,
                      colors={r"M_w": CTRL, r"M": CODE}).next_to(g, DOWN, buff=0.6)
        sub = label(r"$M_w$ is built from $\langle M \rangle$ and $w$ by a simple program: \ $|w|$ new states in front of $M$",
                    font_size=26, color=GREY_A).next_to(claim, DOWN, buff=0.35)
        concl = label(r"so the blank-tape halting problem is undecidable too", font_size=32, color=LIMIT)
        concl.to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A first example. Is there a decider for the simpler question: does M halt when started on a blank tape? "
            "<bookmark mark='a'/> Given any M and w, build a new machine, M sub w. It writes w on its tape, rewinds, and "
            "then behaves exactly like M. Building it is mechanical: a few new states in front of M's table. "
            "<bookmark mark='b'/> M sub w halts on a blank tape exactly when M halts on w. <bookmark mark='c'/> So a "
            "decider for blank tapes would decide halting. There is none. We will need this one in the next chapter."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(name), Create(frame_), LaggedStart(*[FadeIn(m) for m in mw], lag_ratio=0.3),
                      LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(Write(claim), FadeIn(sub))
            vo.wait_until("c")
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gallery(self):
        head = label(r"Each of these has no decider", font_size=40).to_edge(UP, buff=0.4)
        qs = [
            (r"does $M$ ever write a $1$?", r"make $M$ write a 1 just when it would halt"),
            (r"does $M$ accept no input at all?", r"run $M$ on $w$ first, whatever the input"),
            (r"do $M_1$ and $M_2$ compute the same function?", r"compare with a machine that accepts nothing"),
            (r"will this program ever divide by zero?", r"divide by zero just when it would halt"),
            (r"is this program the shortest that does its job?", r"Part 25: \ Kolmogorov complexity"),
        ]
        rows = VGroup()
        for q, h in qs:
            rows.add(VGroup(label(q, font_size=28), label(r"$\leftarrow$ \ " + h, font_size=22, color=GREY_B)))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.4)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to(DOWN * 0.2)
        if rows.width > 13.4:
            rows.width = 13.4
        with self.voiceover(
            "The same trick spreads impossibility everywhere. <bookmark mark='a'/> Does a machine ever write a one? "
            "Rig it to write a one exactly when it would have halted. Does it accept nothing at all? Do two programs "
            "compute the same thing? Will this program ever divide by zero? Is it the shortest program that does its "
            "job? <bookmark mark='b'/> Each comes with its own reduction from halting, and none has a decider."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.45), run_time=4.0)
            vo.wait_until("b")
            self.play(*[Indicate(r[0], color=LIMIT) for r in rows])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rice(self):
        thm = theorem_card(r"Rice (1953)", r"Every non-trivial question about the \textit{function} a program computes, \ its "
                           r"behaviour rather than its text, \ is undecidable.", width=11.4, font_size=28)
        thm.to_edge(UP, buff=0.45)
        left = VGroup(label(r"about the text: \ decidable", font_size=30, color=YES),
                      label(r"does it contain a \texttt{while} loop? \\ is it under 100 lines?", font_size=26,
                            color=GREY_A)).arrange(DOWN, buff=0.25)
        right = VGroup(label(r"about the function: \ undecidable", font_size=30, color=LIMIT),
                       label(r"halts on every input? \\ outputs only zero?", font_size=26,
                             color=GREY_A)).arrange(DOWN, buff=0.25)
        left.move_to(LEFT * 3.4 + DOWN * 0.6)
        right.move_to(RIGHT * 3.4 + DOWN * 0.6)
        bar = Line(UP * 0.4, DOWN * 1.8, color=GREY_D)
        foot = note(r"non-trivial: \ true of some programs and false of others; \ proved in Part 25", font_size=22)
        foot.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1953 Henry Rice proved the general law. <bookmark mark='a'/> Any non-trivial property of the partial "
            "function a program computes is undecidable. Non-trivial means true of some computed functions and false "
            "of others. "
            "<bookmark mark='b'/> Questions about the text are fine: does it contain a while loop, is it under a hundred "
            "lines. <bookmark mark='c'/> Questions about the computed function are different: does it halt on every "
            "input, and does it return zero whenever it halts? We prove Rice's theorem in Part 25."
        ) as vo:
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(left))
            vo.wait_until("c")
            self.play(Create(bar), FadeIn(right), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        card = practice_card([
            (r"virus scanners", r"no program detects every virus (Cohen, 1987): \ scanners match known patterns and "
                                r"guess at behaviour"),
            (r"static analyzers", r"linters and type checkers must either miss some bugs \ or warn about some correct "
                                  r"code: \ they approximate (Part 54)"),
            (r"compilers", r"no compiler can always find the fastest or shortest equivalent program (Parts 13, 25)"),
            (r"testing", r"tests check some inputs; \ no tool proves every program correct automatically"),
        ])
        with self.voiceover(
            "This is not only theory. <bookmark mark='a'/> It is why no virus scanner can detect every virus, which Fred "
            "Cohen proved in 1987. It is why every static analyzer and linter either misses some bugs or complains "
            "about some correct code. It is why compilers cannot always find the best program, and why tests can show "
            "bugs but never prove their absence in general. <bookmark mark='b'/> Engineers live with this by "
            "approximating, by restricting what programs may do, and by asking people to supply proofs, which is how "
            "Part 54 verifies software anyway."
        ) as vo:
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(card.head, color=C.CS_PRACTICE))
        self.wait(0.3)
        self.clear_scene()
