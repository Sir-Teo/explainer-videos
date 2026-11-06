from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (HEAD, LAM, NO, PART, T0C, T1C, YES, load, mono, num)


class Mutex(VoiceoverScene):
    def construct(self):
        self.card()
        self.naive()
        self.peterson()
        self.proof()
        self.bakery()
        self.grid()

    def card(self):
        card = chapter_card(3, r"Mutual exclusion from reads and writes", r"Can loads and stores alone build a lock?",
                            lit=(1965, 1974, 1981), extra=((1965, r"Dijkstra: \ Dekker's algorithm"),
                                                           (1974, r"Lamport: \ the bakery"), (1981, r"Peterson")),
                            part=PART)
        with self.voiceover("Chapter three. Mutual exclusion from nothing but reads and writes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def naive(self):
        d = load("mutex")
        head = label(r"What a lock must do, \ and an obvious one that fails", font_size=32).to_edge(UP, buff=0.3)
        req = VGroup(
            label(r"\textbf{safety}: \ never two threads in the critical section", font_size=21, color=WHITE),
            label(r"\textbf{progress}: \ if some want in, \ one gets in", font_size=21, color=WHITE),
            label(r"\textbf{bounded waiting}: \ nobody is passed over forever", font_size=21, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.8)
        code = VGroup(mono("while (flag[other]) ;   // wait", 19, GREY_A), mono("flag[me] = 1;", 19, GREY_A),
                      mono("critical section", 19, YES), mono("flag[me] = 0;", 19, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08)
        box = SurroundingRectangle(code, color=GREY_D, buff=0.15, corner_radius=0.08)
        cg = VGroup(box, code).next_to(req, RIGHT, buff=0.7).align_to(req, UP)
        tr = d["naive"]["trace"]
        steps = VGroup(*[mono(t, 17, T0C if t.startswith("P0") else T1C) for t in tr]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06)
        tl = label(r"the checker's counterexample:", font_size=19, color=NO).next_to(steps, UP, buff=0.12).align_to(
            steps, LEFT)
        sg = VGroup(tl, steps).next_to(VGroup(req, cg), DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        note = label(r"both looked before either raised a flag: \ the check and the act are not one step",
                     font_size=21, color=NO).next_to(sg, RIGHT, buff=0.5).shift(DOWN * 0.2)
        if note.get_right()[0] > 6.9:
            note.width = 6.9 - note.get_left()[0]
        with self.voiceover(
            "Suppose the hardware gave us only loads and stores. Could we still build a lock? <bookmark mark='a'/> A "
            "lock must guarantee three things. Safety: never two threads in the critical section. Progress: if some "
            "thread wants to enter, one does. And bounded waiting: nobody is passed over forever. <bookmark mark='b'/> "
            "The obvious attempt: wait until the other thread's flag is down, then raise your own. <bookmark "
            "mark='c'/> The checker breaks it in eight steps. Both threads look, both see the other's flag down, both "
            "raise their flags, both enter. <bookmark mark='d'/> Checking and acting are two separate steps, and the "
            "other thread can slip between them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(req))
            vo.wait_until("b")
            self.play(FadeIn(cg))
            vo.wait_until("c")
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def peterson(self):
        head = label(r"Peterson's algorithm, \ 1981", font_size=36).to_edge(UP, buff=0.3)
        code = VGroup(mono("flag[me] = 1;          // I want in", 20, WHITE),
                      mono("turn = other;          // but you go first", 20, WHITE),
                      mono("while (flag[other] && turn == other)", 20, WHITE),
                      mono("    ;                  // wait", 20, GREY_B),
                      mono("critical section", 20, YES),
                      mono("flag[me] = 0;", 20, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        box = SurroundingRectangle(code, color=GREY_D, buff=0.2, corner_radius=0.08)
        VGroup(box, code).next_to(head, DOWN, buff=0.5)
        lines = VGroup(
            label(r"two flags and one shared \texttt{turn}: \ a thread defers to the other, \ and the last to "
                  r"defer waits", font_size=21, color=WHITE),
            label(r"Dekker's \ (1965, \ published by Dijkstra) \ was the first correct one, \ and much more "
                  r"complicated", font_size=21, color=GREY_A),
            label(r"Peterson's is four lines; \ the checker finds no violation in all 1{,}487 states of two rounds",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Gary Peterson found the simple answer in 1981. <bookmark mark='a'/> Each thread raises its flag: I want "
            "in. <bookmark mark='b'/> Then it sets the shared variable turn to the other thread: but you go first. "
            "<bookmark mark='c'/> Then it waits while the other thread wants in and it is the other's turn. "
            "<bookmark mark='d'/> If both want in at once, the one that deferred last waits, and the other enters. "
            "<bookmark mark='e'/> The first correct solution, Dekker's, which Dijkstra published in 1965, was far more "
            "complicated. <bookmark mark='f'/> Peterson's is four lines, and our checker finds no violation in any of "
            "the one thousand four hundred and eighty-seven states of two rounds."
        ) as vo:
            self.play(FadeIn(head), Create(box))
            for mk, ln in zip("abc", (code[0], code[1], VGroup(code[2], code[3]))):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
            self.play(FadeIn(code[4]), FadeIn(code[5]))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
            vo.wait_until("f")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def proof(self):
        head = label(r"Why it works: \ a proof", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"suppose both threads are in the critical section", font_size=23, color=WHITE),
            label(r"each wrote \texttt{turn} once on the way in; \ say thread 0 wrote it last, \ so "
                  r"\texttt{turn = 1} from then on", font_size=23, color=WHITE),
            label(r"thread 1 raised \texttt{flag[1]} \textit{before} it wrote \texttt{turn}, \ so before thread 0's "
                  r"write too", font_size=23, color=WHITE),
            label(r"after its write, \ thread 0 read \texttt{flag[1] = 1} and \texttt{turn = 1}: \ it must have "
                  r"waited", font_size=23, color=NO),
            label(r"contradiction: \ so at most one is inside \qquad $\blacksquare$", font_size=23, color=YES),
            label(r"the proof uses the \textbf{order} of each thread's own writes and reads", font_size=23,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Why does it work? <bookmark mark='a'/> Suppose both threads are in the critical section. <bookmark "
            "mark='b'/> Each wrote turn once on the way in. Say thread zero wrote it last, so turn is one from then on. "
            "<bookmark mark='c'/> Thread one raised its flag before writing turn, so before thread zero's write too. "
            "<bookmark mark='d'/> So after its write, thread zero read flag one equal to one, and turn equal to one, "
            "and it must have kept waiting. It could not have entered. <bookmark mark='e'/> That is a contradiction, "
            "so at most one thread is ever inside. <bookmark mark='f'/> Notice what the proof relies on: that each "
            "thread's own writes and reads happen in the order the program gives them. Remember that."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def bakery(self):
        head = label(r"Lamport's bakery, \ 1974", font_size=36).to_edge(UP, buff=0.3)
        code = VGroup(mono("choosing[me] = 1;", 19, GREY_B),
                      mono("number[me] = 1 + max(number[0..n-1]);", 19, WHITE),
                      mono("choosing[me] = 0;", 19, GREY_B),
                      mono("for each other thread j:", 19, WHITE),
                      mono("    while (choosing[j]) ;", 19, GREY_B),
                      mono("    while (number[j] != 0 &&", 19, WHITE),
                      mono("           (number[j], j) < (number[me], me)) ;", 19, WHITE),
                      mono("critical section;   number[me] = 0;", 19, YES)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.07)
        box = SurroundingRectangle(code, color=GREY_D, buff=0.18, corner_radius=0.08)
        cg = VGroup(box, code).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.5)
        tickets = VGroup()
        for i, (n, c) in enumerate(((3, T0C), (0, GREY_D), (2, T1C), (2, LAM))):
            t = VGroup(RoundedRectangle(width=0.95, height=0.9, corner_radius=0.1, stroke_color=c, stroke_width=2,
                                        fill_color=c, fill_opacity=0.15),
                       label(rf"P{i}", font_size=17, color=GREY_A), MathTex(str(n) if n else r"-", font_size=34,
                                                                            color=WHITE))
            t[1].next_to(t[0].get_top(), DOWN, buff=0.06)
            t[2].move_to(t[0]).shift(DOWN * 0.12)
            tickets.add(t)
        tickets.arrange(RIGHT, buff=0.15).next_to(cg, RIGHT, buff=0.4).align_to(cg, UP)
        tl = label(r"P2 and P3 both took 2: \\ the tie goes to the smaller id, \ P2", font_size=19,
                   color=HEAD).next_to(tickets, DOWN, buff=0.25)
        lines = VGroup(
            label(r"take a number larger than any you see; \ the smallest (number, id) enters next", font_size=21,
                  color=WHITE),
            label(r"\texttt{choosing} stops a thread being judged while it is still picking its number", font_size=21,
                  color=GREY_A),
            label(r"first come, first served; \ and correct even if a read that overlaps a write returns garbage",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "For any number of threads, Lamport's bakery algorithm of 1974 works like the ticket machine at a shop "
            "counter. <bookmark mark='a'/> To enter, take a number one larger than any number you can see. <bookmark "
            "mark='b'/> Then wait for every thread with a smaller number. Two threads can pick the same number if they "
            "choose at the same moment, so ties go to the smaller thread id. <bookmark mark='c'/> The choosing flag "
            "makes others wait while a thread is still reading the numbers, so nobody is judged by a number that is "
            "not yet written. <bookmark mark='d'/> It serves threads first come, first served, and Lamport showed it "
            "stays correct even if a read that overlaps a write returns any value at all. It needs no hardware "
            "atomicity whatsoever."
        ) as vo:
            self.play(FadeIn(head), Create(box), FadeIn(code))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tickets], lag_ratio=0.2), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(tl), Indicate(tickets[2], color=YES))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def grid(self):
        d = load("mutex")
        pet = d["peterson"]
        head = label(r"Peterson's state space, \ by where each thread is", font_size=32).to_edge(UP, buff=0.3)
        names = [r"before", r"flag up", r"waiting", r"\textbf{inside}", r"after"]
        cells = {tuple(c) for c in pet["cells"]}
        s = 0.85
        grid = VGroup()
        for i in range(5):
            for j in range(5):
                ok = (i, j) in cells
                bad = i == 3 and j == 3
                c = NO if bad else (YES if ok else GREY_D)
                sq = Square(s, stroke_color=c, stroke_width=2 if bad else 1.2, fill_color=c,
                            fill_opacity=0.08 if bad else (0.3 if ok else 0.05))
                sq.move_to([j * s, -i * s, 0])
                grid.add(sq)
        grid.move_to([-2.4, -0.3, 0])
        cross = Cross(grid[3 * 5 + 3], stroke_color=NO, stroke_width=4)
        rl = VGroup(*[label(t, font_size=17, color=T0C).next_to(grid[i * 5], LEFT, buff=0.12) for i, t in
                      enumerate(names)])
        cl = VGroup(*[label(t, font_size=17, color=T1C).next_to(grid[j], UP, buff=0.12).rotate(0) for j, t in
                      enumerate(names)])
        ax0 = label(r"thread 0", font_size=19, color=T0C).next_to(rl, LEFT, buff=0.15)
        ax1 = label(r"thread 1", font_size=19, color=T1C).next_to(cl, UP, buff=0.1)
        bak = d["bakery"]
        notes = VGroup(
            label(rf"{pet['states']} states for one round each; \\ {len(cells)} of the 25 combinations occur",
                  font_size=20, color=WHITE),
            label(r"never \textbf{(inside, inside)}", font_size=20, color=NO),
            label(rf"Lamport's bakery, \ any $n$ threads: \\ take a number; \ smallest goes. \\ checked: "
                  rf"{num(bak['2']['states'])} states for 2, \ {num(bak['3']['states'])} for 3", font_size=20,
                  color=LAM),
            label(r"Burns and Lynch \ (1980): \ $n$ threads need \\ at least $n$ shared variables \\ if all they "
                  r"have is reads and writes", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(grid, RIGHT, buff=0.9).align_to(grid, UP)
        with self.voiceover(
            "The checker can also show us the whole state space. <bookmark mark='a'/> Group Peterson's states by where "
            "each thread is: before the lock, flag raised, waiting, inside, or after. <bookmark mark='b'/> For one "
            "round each there are two hundred and fifty-eight states, and twenty-four of the twenty-five combinations "
            "occur. <bookmark mark='c'/> The one that never occurs is both inside. <bookmark mark='d'/> The checker "
            "confirms the bakery too, for two threads and for three, where it has over ninety thousand states. "
            "<bookmark mark='e'/> But there is a price. Burns and Lynch proved in 1980 that with only reads and "
            "writes, n threads need at least n shared variables. Real locks use a stronger instruction, and chapter "
            "five shows why that is not just a matter of convenience."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rl), FadeIn(cl), FadeIn(ax0), FadeIn(ax1), FadeIn(grid))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(Create(cross), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
