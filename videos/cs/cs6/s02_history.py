from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, YES, box, fmt, load,
                                  say)


class History(WatchScene):
    def construct(self):
        self.card()
        self.eniac()
        self.baby()
        self.edsac()

    def card(self):
        self.chapter(1, r"Cables, \ then memory", r"How was the first computer programmed?", lit=(1945, 1948, 1949), part=PART, said="Chapter one. Cables, then memory.")

    # ------------------------------------------------------------------
    def eniac(self):
        head = label(r"ENIAC \ (1945): \ programmed with cables", font_size=38).to_edge(UP, buff=0.35)
        rng = np.random.default_rng(4)
        panels = VGroup()
        for k in range(14):
            p = Rectangle(width=0.62, height=2.3, stroke_color=GREY_B, stroke_width=1.5, fill_color="#1a2030",
                          fill_opacity=1)
            lights = VGroup(*[Dot(radius=0.035, color=HEAD if rng.random() < 0.3 else GREY_D)
                              .move_to(p.get_top() + DOWN * (0.25 + 0.16 * i) + RIGHT * (0.15 * (j - 1)))
                              for i in range(5) for j in range(3)])
            jacks = VGroup(*[Circle(radius=0.045, color=GREY_C, stroke_width=1.2)
                             .move_to(p.get_bottom() + UP * (0.25 + 0.2 * i) + RIGHT * (0.18 * (j - 0.5)))
                             for i in range(3) for j in range(2)])
            panels.add(VGroup(p, lights, jacks))
        panels.arrange(RIGHT, buff=0.08).move_to(UP * 0.7)
        cables = VGroup()
        for _ in range(16):
            a, b = rng.choice(len(panels), 2, replace=False)
            pa = panels[a][2][int(rng.integers(6))].get_center()
            pb = panels[b][2][int(rng.integers(6))].get_center()
            mid = (pa + pb) / 2 + DOWN * rng.uniform(0.4, 1.3)
            cables.add(VMobject(stroke_color=[CTRL, NO, DATA, YES][int(rng.integers(4))], stroke_width=2.5)
                       .set_points_smoothly([pa, mid, pb]))
        stats = VGroup(
            label(r"17{,}468 vacuum tubes, \ 30 tons, \ about 5{,}000 additions a second", font_size=26, color=GREY_A),
            label(r"a new problem: \ days of plugging cables and setting switches", font_size=26, color=NO),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=1.4)
        names = label(r"Kay McNulty, \ Betty Jennings, \ Betty Snyder, \ Marlyn Wescoff, \ Fran Bilas, \ Ruth "
                      r"Lichterman", font_size=24, color=HIST).to_edge(DOWN, buff=0.75)
        nn = label(r"its first programmers, \ worked out every wire from the logic diagrams", font_size=22,
                   color=GREY_B).next_to(names, DOWN, buff=0.12)
        with self.voiceover(
            "In 1945, at the University of Pennsylvania, John Presper Eckert and John Mauchly finished ENIAC, an early"
            " general-purpose electronic computer, publicly unveiled in 1946. <bookmark mark='a'/> It filled a room: "
            "seventeen thousand vacuum tubes, thirty tons, and it added five thousand numbers a second, a thousand "
            "times faster than the relay machines before it. <bookmark mark='b'/> But it had no program in the sense "
            "we mean. Each problem was set up by hand: units connected by cables, and switches set on every panel, so "
            "that numbers flowed from accumulator to multiplier in the right order. A new problem took days of "
            "re-plugging. <bookmark mark='c'/> The people who did it were six women hired as human computers: Kay "
            "McNulty, Betty Jennings, Betty Snyder, Marlyn Wescoff, Fran Bilas and Ruth Lichterman. With no manuals, "
            "they learned the machine from its logic diagrams and worked out every connection. They were not "
            "introduced when ENIAC was shown to the press in 1946, and their work was recognised only decades later."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.05), run_time=1.6)
            self.play(FadeIn(stats[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in cables], lag_ratio=0.12), run_time=3.0)
            self.play(FadeIn(stats[1]))
            vo.wait_until("c")
            self.play(FadeIn(names), FadeIn(nn))
        self.wait(0.3)
        self.clear_scene()


    # ------------------------------------------------------------------
    def baby(self):
        self.ask(r"June 1948: the first program ever run \\ from a computer's own memory. It computed...",
                 [r"a table of squares", r"the largest factor of $2^{18}$", r"digits of $\pi$"], 1,
                 say="In June 1948, a program ran from a computer's own memory for the first time. What did it compute?",
                 reveal="The largest proper factor of two to the eighteen, by trying every candidate, in fifty-two minutes.")
        head = label(r"Manchester, \ 21 June 1948: \ the first stored program runs", font_size=34).to_edge(UP,
                                                                                                          buff=0.35)
        grid = VGroup(*[Dot(radius=0.05, color=YES if (r * 7 + c * 3) % 5 < 2 else GREY_D)
                        for r in range(32) for c in range(32)]).arrange_in_grid(32, 32, buff=0.045)
        grid.height = 3.4
        grid.move_to(LEFT * 4.0 + DOWN * 0.3)
        frame = SurroundingRectangle(grid, buff=0.15, color=GREY_B, corner_radius=0.1)
        gl = label(r"32 words of 32 bits, \\ dots on a Williams tube", font_size=22, color=GREY_A).next_to(frame, DOWN,
                                                                                                         buff=0.15)
        prob = VGroup(
            label(r"Tom Kilburn's first program:", font_size=26, color=HIST),
            MathTex(r"\text{the largest proper factor of } 2^{18} = 262{,}144", font_size=32, color=CODE),
            label(r"try every number from $2^{18} - 1$ down; \ divide by repeated subtraction \\ (the Baby could only "
                  r"subtract)", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 2.2 + UP * 1.2)
        trial = ValueTracker(262143)
        tv = always_redraw(lambda: MathTex(rf"\text{{trying }} {int(trial.get_value()):,}".replace(",", "{,}"),
                                           font_size=34, color=HEAD).move_to(RIGHT * 2.2 + DOWN * 0.6))
        res = VGroup(
            label(r"answer: \ 131{,}072, \ after 52 minutes \\ and about 3.5 million instructions", font_size=26,
                  color=YES),
            label("Baby: \\ 7 instruction types, \\ 1 kilobit of memory",
                  font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 2.2 + DOWN * 2.0)
        with self.voiceover(
            "The first machine to actually run a program from its memory was small. <bookmark mark='a'/> At "
            "Manchester, Freddie Williams, Tom Kilburn and Geoff Tootill built a test bed for Williams's tube memory, "
            "nicknamed the Baby: thirty-two words of thirty-two bits, stored as dots of charge on a screen. <bookmark "
            "mark='b'/> On the twenty-first of June 1948, it ran Kilburn's first program: find the largest proper "
            "factor of two to the eighteen. The Baby could not divide, or even add; it could only subtract. So the "
            "program tried every number downwards, dividing by repeated subtraction. <bookmark mark='c'/> After "
            "fifty-two minutes and about three and a half million instructions, the answer appeared on the screen: a "
            "hundred and thirty-one thousand and seventy-two. An instruction set of seven operations, a kilobit of "
            "memory, and the first program ever to run from the same store that held its data."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(frame), LaggedStart(*[FadeIn(d) for d in grid], lag_ratio=0.0005), FadeIn(gl),
                      run_time=1.6)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in prob], lag_ratio=0.4), run_time=2.0)
            self.add(tv)
            self.play(trial.animate.set_value(131072), run_time=5.0, rate_func=rate_functions.ease_in_quad)
            vo.wait_until("c")
            self.play(FadeIn(res[0]))
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def edsac(self):
        head = label(r"EDSAC \ (Cambridge, \ 6 May 1949): \ a computer people could use", font_size=34).to_edge(
            UP, buff=0.35)
        squares = VGroup(*[MathTex(rf"{n} \ \ {n * n}", font_size=24, color=DATA) for n in range(10)]).arrange(
            DOWN, buff=0.08, aligned_edge=LEFT).move_to(LEFT * 5.2 + DOWN * 0.3)
        sl = label(r"its first program: \\ a table of squares", font_size=22, color=GREY_A).next_to(squares, UP,
                                                                                                 buff=0.2)
        main = box(2.2, 2.6, r"\text{main program}", CODE, 22).move_to(LEFT * 1.4 + DOWN * 0.3)
        sub = box(2.2, 1.6, r"\text{subroutine}", FUNC, 22).move_to(RIGHT * 2.2 + UP * 0.2)
        call = CurvedArrow(main.get_right() + UP * 0.6, sub.get_left() + UP * 0.4, color=YES, angle=-0.6)
        back = CurvedArrow(sub.get_left() + DOWN * 0.4, main.get_right() + DOWN * 0.4, color=HEAD, angle=-0.6)
        cl = label(r"jump, \ leaving the \\ return address", font_size=20, color=YES).next_to(call, UP, buff=0.1)
        bl = label(r"jump back to it", font_size=20, color=HEAD).next_to(back, DOWN, buff=0.1)
        notes = VGroup(
            label("the \\textit{Wheeler jump}: \\ an early subroutine technique \\ (David Wheeler)", font_size=24, color=HIST),
            label(r"a library of tested subroutines, \ and \textit{initial orders} that loaded programs from paper "
                  r"tape", font_size=22, color=GREY_A),
            label(r"Pebble's \texttt{jal} \ does the same in one instruction \ (Part 11)", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A year later at Cambridge, Maurice Wilkes's EDSAC became the first stored-program computer in regular "
            "service. <bookmark mark='a'/> On the sixth of May 1949 it printed its first output, a table of squares, "
            "and soon it was computing for scientists across the university. <bookmark mark='b'/> Its team invented "
            "much of what programming still is. David Wheeler found a way to call a subroutine and come back: the "
            "caller jumps, leaving its own address where the subroutine can find it, and the subroutine ends by jumping "
            "to that address. <bookmark mark='c'/> They built a library of tested subroutines, and a loader, the "
            "initial orders, that read programs from paper tape and fixed up their addresses. Pebble's jump-and-link "
            "instruction does Wheeler's trick in a single step, and Part 11 builds the calling convention on it."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(sl), LaggedStart(*[FadeIn(s) for s in squares], lag_ratio=0.12), run_time=1.6)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(main), FadeIn(sub))
            self.play(Create(call), FadeIn(cl))
            self.play(Create(back), FadeIn(bl))
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
