from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class Reversible(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"The thermodynamics of computing", r"What must a computer pay?", lit=(1973, 2012),
                            part=PART)
        with self.voiceover("Chapter thirteen. The thermodynamics of computing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.and_gate()
        self.toffoli()
        self.bennett_trick()
        self.industry()

    def and_gate(self):
        la = load("landauer")
        head = label(r"An AND gate forgets", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ins = [(0, 0), (0, 1), (1, 0), (1, 1)]
        left = VGroup(*[MathTex(str(a) + str(b), font_size=30, color=LAW).move_to([-4.6, 1.2 - 0.85 * i, 0])
                        for i, (a, b) in enumerate(ins)])
        right = VGroup(MathTex(r"0", font_size=34, color=BAD).move_to([-1.4, 0.35, 0]),
                       MathTex(r"1", font_size=34, color=OK).move_to([-1.4, -1.35, 0]))
        arrows = VGroup(*[Arrow(left[i].get_right(), right[0 if a * b == 0 else 1].get_left(), buff=0.15,
                                color=BAD if a * b == 0 else OK, stroke_width=3) for i, (a, b) in enumerate(ins)])
        hl = label(r"inputs", font_size=19, color=GREY_A).next_to(left, UP, buff=0.25)
        hr = label(r"output", font_size=19, color=GREY_A).next_to(right, UP, buff=1.0)
        lost = la["and_lost_bits"]
        side = stack([(r"three inputs go to 0: \ from the output you cannot tell which", BAD),
                      (r"in: \ 2 bits; \ out: \ $H(\tfrac14, \tfrac34) \approx 0.811$ bits", ABS),
                      (rf"lost: \ {lost:.3f} bits per operation, \ on uniform inputs", BAD),
                      (rf"so at least {la['and_min_energy'] * 1e21:.2f}$\times 10^{{-21}}$ J of heat at room "
                       r"temperature", ENT)], font_size=21, aligned_edge=LEFT, width=5.6).move_to([3.8, -0.3, 0])
        with self.voiceover(
            "Landauer's principle says that what costs is forgetting, so look at what ordinary logic forgets. "
            "<bookmark mark='a'/>An AND gate takes two bits and outputs one: zero unless both inputs are one. "
            "<bookmark mark='b'/>Three different inputs give the output zero. From the output you cannot tell which "
            "of them it was: the gate has erased information. <bookmark mark='c'/>On uniformly random inputs, two "
            "bits go in and the output carries only about point eight one bits. <bookmark mark='d'/>So each "
            "operation destroys about one point one nine bits, <bookmark mark='e'/>and must release at least that "
            "many units of k T log two as heat. Ordinary computers forget at every step."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(right), FadeIn(hl), FadeIn(hr))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def toffoli(self):
        la = load("landauer")
        head = label(r"The Toffoli gate forgets nothing", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"a\,b\,c", r"\to", r"a\,b\,(c \oplus ab)"]
        rows = []
        for r in la["toffoli"]:
            i, o = r["in"], r["out"]
            changed = i != o
            rows.append([MathTex("".join(map(str, i)), font_size=26),
                         MathTex(r"\mapsto", font_size=24, color=GREY_B),
                         MathTex("".join(map(str, o)), font_size=26, color=GOAL if changed else WHITE)])
        grid = ValueGrid(hd, rows, col_w=[1.8, 0.9, 2.6], cell_h=0.46, font_size=24).move_to([-3.4, -0.5, 0])
        side = stack([(r"Toffoli \ (1980): \ flip the third bit if the first two are both 1", ABS),
                      (r"8 inputs, \ 8 distinct outputs: \ a permutation, \ so nothing is erased", OK),
                      (r"set $c = 0$ and the third output is $a$ AND $b$: \ the gate is universal", LAW),
                      (r"Fredkin and Toffoli \ (1982): \ conservative logic", HIST)], font_size=21,
                     aligned_edge=LEFT, width=5.4).move_to([3.4, -0.3, 0])
        assert la["toffoli_bijective"]
        with self.voiceover(
            "Logic does not have to forget. <bookmark mark='a'/>Tommaso Toffoli's gate takes three bits, passes the "
            "first two through, and flips the third if the first two are both one. <bookmark mark='b'/>Its eight "
            "inputs go to eight different outputs. It is a permutation, so it can be run backwards and erases "
            "nothing. <bookmark mark='c'/>And it computes AND: set the third input to zero, and the third output is "
            "a and b. Toffoli gates alone can build any computation. <bookmark mark='d'/>Edward Fredkin and Toffoli "
            "called this conservative logic: computing that conserves information, and so has no Landauer cost."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.3)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(VGroup(*grid.cell[6], *grid.cell[7]), color=GOAL))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def bennett_trick(self):
        head = label(r"Compute, \ copy, \ uncompute", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        boxes = VGroup()
        names = [(r"input", WHITE), (r"compute \ (reversibly)", LAW), (r"copy the answer", DATA),
                 (r"uncompute", TIME), (r"input + answer", OK)]
        for i, (t, c) in enumerate(names):
            r = RoundedRectangle(width=2.2, height=1.0, corner_radius=0.15, color=c, stroke_width=2.5)
            r.move_to([-5.2 + 2.6 * i, 0.6, 0])
            boxes.add(VGroup(r, label(t, font_size=18, color=c).move_to(r)))
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.08, color=GREY_B)
                          for i in range(4)])
        junk = label(r"garbage bits pile up \dots", font_size=18, color=BAD).next_to(boxes[1], DOWN, buff=0.3)
        gone = label(r"\dots and are run back to blank", font_size=18, color=TIME).next_to(boxes[3], DOWN, buff=0.3)
        rows = stack([(r"Bennett \ (1973): \ every computation can be made logically reversible", ABS),
                      (r"the cost moves from heat to time and memory", CHANCE),
                      (r"quantum computers are reversible by nature: \ every gate is unitary \ (Part 26)", LAW)],
                     font_size=21, aligned_edge=LEFT, width=11.0, buff=0.28).move_to([0, -1.9, 0])
        with self.voiceover(
            "Charles Bennett showed in 1973 that any computation at all can be made reversible. "
            "<bookmark mark='a'/>Start from the input. <bookmark mark='b'/>Compute with reversible gates; the "
            "trouble is that they leave garbage, intermediate bits you would normally erase. "
            "<bookmark mark='c'/>Copy the answer, which can be done reversibly into a blank register. "
            "<bookmark mark='d'/>Then run the whole computation backwards, uncomputing the garbage back to blank. "
            "<bookmark mark='e'/>You are left with the input and the answer, and nothing has been erased. "
            "<bookmark mark='f'/>The price is paid in time and memory instead of heat. And quantum computers are "
            "reversible by nature: every quantum gate is a unitary transformation, and the Toffoli gate is one of "
            "them, which Part 26 takes up."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(boxes[1]), FadeIn(junk))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(boxes[2]))
            vo.wait_until("d")
            self.play(GrowArrow(arrows[2]), FadeIn(boxes[3]), FadeIn(gone))
            vo.wait_until("e")
            self.play(GrowArrow(arrows[3]), FadeIn(boxes[4]))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4))
        self.clear_scene()

    def industry(self):
        la = load("landauer")
        head = label(r"How far from the floor?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = NumberLine(x_range=[-21, -12, 1], length=10.0, color=GREY_B, include_numbers=False).move_to(
            [0, 0.6, 0])
        ticks = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_A).next_to(ax.n2p(k), DOWN, buff=0.15)
                         for k in range(-21, -11)])
        unit = label(r"joules per elementary operation", font_size=19, color=GREY_A).next_to(ax, DOWN, buff=0.7)
        ln = np.log10(la["joules_per_bit"])
        floor = VGroup(Dot(ax.n2p(ln), radius=0.1, color=OK),
                       label(r"Landauer: \ $kT \ln 2$", font_size=19, color=OK).next_to(ax.n2p(ln), UP, buff=0.3))
        chips = Rectangle(width=ax.n2p(-15)[0] - ax.n2p(-18)[0], height=0.35, stroke_width=0, fill_color=BAD,
                          fill_opacity=0.5).move_to((ax.n2p(-15) + ax.n2p(-18)) / 2)
        cl = label(r"today's logic: \ roughly attojoules to femtojoules", font_size=19, color=BAD).next_to(
            chips, UP, buff=0.3)
        rows = stack([(r"hundreds to hundreds of thousands of times above the floor: \ not yet the limit", CHANCE),
                      (r"but every joule a data centre uses ends as heat: \ the second law sends the bill", ENT),
                      (r"reversible and adiabatic circuits are being built to approach the floor", LAW),
                      (r"and the demon's lesson stands: \ information is physical", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=11.4, buff=0.28).move_to([0, -2.0, 0])
        with self.voiceover(
            "How close are real computers to Landauer's floor? <bookmark mark='a'/>Put energies per operation on a "
            "logarithmic line. <bookmark mark='b'/>The floor, k T log two at room temperature, is near three times "
            "ten to the minus twenty-one joules. <bookmark mark='c'/>A switching event in today's logic costs "
            "somewhere around attojoules to femtojoules, ten to the minus eighteen to ten to the minus fifteen. "
            "<bookmark mark='d'/>So we are hundreds to hundreds of thousands of times above the floor, and the "
            "floor is not yet what limits us. <bookmark mark='e'/>But every joule a data centre draws ends up as heat, and the "
            "second law sends the bill. <bookmark mark='f'/>Reversible and adiabatic circuits, which recover the "
            "energy of each switching event instead of dumping it, are being built to approach the floor. "
            "<bookmark mark='g'/>Maxwell's demon taught physics that information is physical. It is now an "
            "engineering problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(ticks), FadeIn(unit))
            vo.wait_until("b")
            self.play(FadeIn(floor))
            vo.wait_until("c")
            self.play(FadeIn(chips), FadeIn(cl))
            for mk, r in zip("defg", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
