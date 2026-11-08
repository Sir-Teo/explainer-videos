from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Turing(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Turing machines", r"What is a mechanical procedure?", lit=(1936,), part=PART)
        with self.voiceover("Chapter nine. Turing machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.idea()
        self.run()
        self.spacetime()
        self.universal()

    def idea(self):
        hc = history_card(1936, r"Alan Turing, \ aged 24", r"`On computable numbers, \ with an application to the "
                          r"\textit{Entscheidungsproblem}'", width=7.0, color=HIST).to_corner(UL, buff=0.35)
        clerk = VGroup(label(r"a human computer, \ reduced to essentials:", font_size=26, color=GOAL),
                       label(r"a tape of squares, \ each blank or marked", font_size=24),
                       label(r"a finite number of states of mind", font_size=24),
                       label(r"look at one square; \ write; \ move one step; \ change state", font_size=24),
                       label(r"the rule depends only on the state and the symbol seen", font_size=24)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28).move_to([-1.6, -0.1, 0])
        tape = tape_row([0, 0, 1, 1, 0, 1, 0, 0], head=3, state="A", cell=0.55).move_to([3.6, -2.5, 0])
        church = label(r"the same year: \ Alonzo Church's $\lambda$-calculus, \ Emil Post's workers: \ all "
                       r"equivalent", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 1936 Alan Turing, aged twenty-four, asked what it is to compute by following rules. "
            "<bookmark mark='a'/>He imagined a human computer, a clerk, and stripped the work down. Paper becomes "
            "a tape of squares, each blank or marked. The clerk has finitely many states of mind. At each step "
            "the clerk looks at one square, may change its mark, moves one square left or right, and changes "
            "state, by a rule that depends only on the current state and the symbol seen. "
            "<bookmark mark='b'/>That is a Turing machine. <bookmark mark='c'/>The same year Alonzo Church, with "
            "the lambda calculus, and Emil Post, with his workers in boxes, gave other definitions. All of them "
            "turned out to define exactly the same functions."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in clerk], lag_ratio=0.5), run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(tape))
            vo.wait_until("c")
            self.play(FadeIn(church))
        self.clear_scene()

    def run(self):
        d = load("tm")
        head = label(r"A two-state machine, \ run by the Reasoner", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        hd = [label(r"state", font_size=22, color=P.CLAIM), label(r"reads", font_size=22, color=P.CLAIM),
              label(r"writes", font_size=22, color=P.CLAIM), label(r"moves", font_size=22, color=P.CLAIM),
              label(r"next", font_size=22, color=P.CLAIM)]
        rows = []
        for st, sym, w, mv, nx in d["rules2"]:
            rows.append([MathTex(st, font_size=28, color=STATE_COLORS[st]), MathTex(str(sym), font_size=28),
                         MathTex(str(w), font_size=28), MathTex(r"\rightarrow" if mv > 0 else r"\leftarrow",
                                                              font_size=28),
                         MathTex(r"\text{halt}" if nx == "H" else nx, font_size=26,
                                 color=STATE_COLORS.get(nx, WHITE))])
        grid = ValueGrid(hd, rows, col_w=[1.1, 1.0, 1.1, 1.1, 1.3], cell_h=0.55, font_size=24).to_corner(UL, buff=0.6)
        grid.shift(DOWN * 0.5)
        st = d["st2"]
        lo = 0
        W = len(st[0][0])
        tapes = []
        for cells, h, s in st:
            t = tape_row(cells, head=h, state=s if s != "H" else "H", cell=0.62).move_to([2.6, 0.6, 0])
            tapes.append(t)
        step = label(r"step 0", font_size=26, color=GREY_A).move_to([2.6, 1.8, 0])
        res = label(r"halts after 6 steps, \ leaving 4 ones", font_size=28, color=OK).move_to([2.6, -1.0, 0])
        with self.voiceover(
            "Here is a machine with two states, A and B, as a table of four rules. <bookmark mark='a'/>Start on a "
            "blank tape in state A. A reads zero: write one, move right, go to B. B reads zero: write one, move left, "
            "back to A. <bookmark mark='b'/>And so on, step by step. <bookmark mark='c'/>After six steps it reaches "
            "the halting rule and stops, leaving four ones on the tape. Keep that number in mind: no machine with "
            "two states does better."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid))
            vo.wait_until("a")
            cur = tapes[0]
            self.play(FadeIn(cur), FadeIn(step))
            vo.wait_until("b")
            for i, t in enumerate(tapes[1:], 1):
                ns = label(rf"step {i}", font_size=26, color=GREY_A).move_to(step)
                self.play(ReplacementTransform(cur, t), ReplacementTransform(step, ns), run_time=0.8)
                cur, step = t, ns
                self.wait(0.4)
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.clear_scene()

    def spacetime(self):
        d = load("tm")
        head = label(r"Four states: \ 107 steps, \ time running to the right", font_size=30, color=CONN).to_edge(
            UP, buff=0.4)
        im = spacetime_image(d["st4"], height=1.8, across=True).move_to([0.15, 1.1, 0])
        frame = SurroundingRectangle(im, buff=0.02, color=GREY_C, stroke_width=1.5)
        tl = VGroup(Arrow(im.get_corner(DL) + DOWN * 0.3, im.get_corner(DR) + DOWN * 0.3, buff=0, color=GREY_B,
                          stroke_width=2, max_tip_length_to_length_ratio=0.02),
                    label(r"step 0 \ \ $\longrightarrow$ \ \ step 107", font_size=20, color=GREY_B))
        tl[1].next_to(tl[0], DOWN, buff=0.1)
        sl = label(r"tape", font_size=20, color=GREY_B).rotate(PI / 2).next_to(im, LEFT, buff=0.15)
        key = VGroup(*[VGroup(Square(side_length=0.25, fill_color=c, fill_opacity=1, stroke_width=0),
                              label(t, font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.15)
                       for c, t in ((TAPE, r"a 1 on the tape"), (STATE_COLORS["A"], r"the head, in state A"),
                                    (STATE_COLORS["B"], r"\dots B"), (STATE_COLORS["C"], r"\dots C"),
                                    (STATE_COLORS["D"], r"\dots D"))]).arrange(RIGHT, buff=0.45).move_to([0, -1.35, 0])
        facts = VGroup(label(r"Allen Brady's machine: \ 13 ones", font_size=26, color=GOAL),
                       label(r"proved the best possible for four states \ (1983)", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.15).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "A run can be drawn as a single picture: one column of tape per step, with time running from left to "
            "right. "
            "<bookmark mark='a'/>This is a four-state machine found by Allen Brady. Its head sweeps back and forth, "
            "building a growing block of ones, in a hundred and seven steps, before it halts with thirteen ones on "
            "the tape. <bookmark mark='b'/>No four-state machine leaves more, or runs longer and still halts: that "
            "was proved in 1983."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(im), Create(frame), FadeIn(tl), FadeIn(sl), FadeIn(key), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(facts))
        self.clear_scene()

    def universal(self):
        head = label(r"One machine to run them all", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        u = RoundedRectangle(width=3.0, height=1.6, corner_radius=0.15, stroke_color=GOAL, stroke_width=3,
                             fill_color="#151A24", fill_opacity=1).move_to([0, 0.6, 0])
        ul = label(r"$U$", font_size=48, color=GOAL).move_to(u)
        inp = VGroup(label(r"the table of a machine $M$, \ as a string", font_size=24, color=TAPE),
                     label(r"an input $x$", font_size=24, color=TAPE)).arrange(DOWN, aligned_edge=RIGHT,
                                                                             buff=0.3).next_to(u, LEFT, buff=1.2)
        arrows = VGroup(Arrow(inp.get_right() + UP * 0.25, u.get_left() + UP * 0.25, buff=0.1, color=GREY_B),
                        Arrow(inp.get_right() + DOWN * 0.25, u.get_left() + DOWN * 0.25, buff=0.1, color=GREY_B))
        out = label(r"whatever $M$ does on $x$", font_size=24, color=GOAL).next_to(u, RIGHT, buff=1.2)
        a3 = Arrow(u.get_right(), out.get_left(), buff=0.1, color=GREY_B)
        notes = VGroup(label(r"programs are data: \ the idea behind every computer since", font_size=26, color=OK),
                       label(r"and the start of trouble: \ a machine can be asked about machines, \ including "
                             r"itself", font_size=26, color=SELF)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Turing's deepest observation was the next one. <bookmark mark='a'/>A machine's table can itself be "
            "written on a tape, as a string of symbols. And there is a single universal machine U which, given the "
            "description of any machine M and an input x, does whatever M would do on x. "
            "<bookmark mark='b'/>Programs are data. Every computer since has been built on that idea. "
            "<bookmark mark='c'/>It is also where the trouble starts. A machine can be asked questions about "
            "machines, including itself, and the diagonal is waiting. Part 3 used it to show that no machine "
            "decides which machines halt; the next chapter measures how badly."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(inp), *[GrowArrow(a) for a in arrows], FadeIn(u), FadeIn(ul))
            self.play(GrowArrow(a3), FadeIn(out))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.clear_scene()
