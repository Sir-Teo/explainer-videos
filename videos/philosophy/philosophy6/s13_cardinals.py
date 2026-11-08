from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


class Cardinals(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Alephs", r"How do you add and multiply infinite sizes?", lit=(1883,), part=PART)
        with self.voiceover("Chapter twelve. Alephs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.alephs()
        self.arithmetic()
        self.square()
        self.continuum()

    def alephs(self):
        head = label(r"A size is measured by the first ordinal of that size", font_size=30, color=CONN).to_edge(
            UP, buff=0.5)
        ladder = VGroup()
        items = [(r"\aleph_0 = \omega", r"the countable"), (r"\aleph_1 = \omega_1", r"the first uncountable ordinal"),
                 (r"\aleph_2 = \omega_2", r"the next size up"), (r"\aleph_\omega", r"the limit of $\aleph_0, \aleph_1, "
                                                                                 r"\aleph_2, \dots$"),
                 (r"\aleph_{\omega_1},\ \aleph_{\aleph_{\omega}},\ \dots", r"an aleph for every ordinal")]
        for i, (a, b) in enumerate(items):
            row = VGroup(MathTex(a, font_size=40, color=interpolate_color(ManimColor(SETC), ManimColor(CARD), i / 4)),
                         label(b, font_size=24, color=GREY_A))
            row[0].move_to([-3.6 + row[0].width / 2, 1.6 - 0.9 * i, 0])
            row[1].move_to([1.2 + row[1].width / 2, 1.6 - 0.9 * i, 0])
            ladder.add(row)
        note_ = label(r"every well-orderable set has exactly one aleph as its size; \ with choice, every set is",
                      font_size=24, color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How big is an infinite set? <bookmark mark='a'/>The answer uses the ordinals. A set's size, its "
            "cardinal, is the first ordinal that can be matched with it. The natural numbers have size aleph zero, "
            "the first infinite cardinal, which is omega itself. <bookmark mark='b'/>Aleph one is the first ordinal "
            "that cannot be counted, omega one. Then aleph two, and so on. <bookmark mark='c'/>After all the finite "
            "alephs comes aleph omega, their limit. <bookmark mark='d'/>And there is an aleph for every ordinal. "
            "<bookmark mark='e'/>Every set that can be well-ordered has exactly one aleph as its size; with the axiom "
            "of choice, every set can be."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", ladder[:4]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            self.play(FadeIn(ladder[4]))
            vo.wait_until("e")
            self.play(FadeIn(note_))
        self.clear_scene()

    def arithmetic(self):
        head = label(r"Infinite arithmetic is easy, \ except for powers", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(MathTex(r"\aleph_0 + \aleph_0 = \aleph_0", font_size=40),
                   label(r"evens and odds", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.5),
            VGroup(MathTex(r"\aleph_0 \cdot \aleph_0 = \aleph_0", font_size=40),
                   label(r"Cantor's pairing, \ Chapter 2", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.5),
            VGroup(MathTex(r"\kappa + \lambda = \kappa \cdot \lambda = \max(\kappa, \lambda)", font_size=40, color=GOAL),
                   label(r"for infinite $\kappa$ \ (Hessenberg 1906)", font_size=24, color=GREY_A)).arrange(
                RIGHT, buff=0.5),
            VGroup(MathTex(r"2^{\kappa} > \kappa", font_size=40, color=CARD),
                   label(r"Cantor's theorem, \ Chapter 3", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.5),
            VGroup(MathTex(r"2^{\aleph_0} = \ ?", font_size=44, color=BAD),
                   label(r"the size of the real numbers", font_size=24, color=BAD)).arrange(RIGHT, buff=0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Arithmetic with alephs is strangely easy. <bookmark mark='a'/>Aleph zero plus aleph zero is aleph "
            "zero: the even and the odd numbers together are just the numbers. <bookmark mark='b'/>Aleph zero times "
            "aleph zero is aleph zero: that is Cantor's pairing of the grid. <bookmark mark='c'/>In general, for "
            "infinite cardinals, the sum and the product are simply the larger of the two. "
            "<bookmark mark='d'/>Only powers are hard. Two to the kappa, the number of subsets, is always bigger "
            "than kappa. <bookmark mark='e'/>But which aleph is two to the aleph zero, the number of real numbers? "
            "Cantor could not find out. Neither can anyone else, for a reason we will see."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def square(self):
        d = load("hilbert")
        hc = history_card(1877, r"Cantor to Dedekind", r"`Je le vois, mais je ne le crois pas': \ I see it, but I do "
                          r"not believe it", width=6.6, color=HIST).to_corner(UL, buff=0.3)
        inter = VGroup(MathTex(rf"x = {d['x']}\dots", font_size=34, color=P.CLAIM),
                       MathTex(rf"y = {d['y']}\dots", font_size=34, color=GOAL),
                       MathTex(rf"z = {d['z']}\dots", font_size=34),
                       label(r"interleave the digits: \ a point of the square becomes a point of the line",
                             font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-3.3, -0.4, 0])
        z = inter[2]
        cols = [P.CLAIM, GOAL]
        for i, ch in enumerate(d["z"][2:]):
            z[0][4 + i].set_color(cols[i % 2])
        size = 3.4
        c0 = np.array([3.3, -0.6, 0])
        frame = Square(side_length=size, stroke_color=GREY_C).move_to(c0)

        def curve(k):
            pts = [c0 + np.array([(x - 0.5) * size, (y - 0.5) * size, 0]) for x, y in d["curves"][str(k)]]
            return VMobject(stroke_color=SETC, stroke_width=max(1.2, 3.5 - 0.5 * k)).set_points_as_corners(pts)

        curves = [curve(k) for k in range(1, 6)]
        cl = label(r"Hilbert's curve: \ the line, folded to fill the square", font_size=22, color=SETC).next_to(
            frame, DOWN, buff=0.25)
        moral = label(r"$|\mathbb{R}^2| = |\mathbb{R}|$: \ size does not see dimension \ (Brouwer 1911: topology "
                      r"does)", font_size=24, color=OK).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Cantor's most startling result in this direction came in 1877. <bookmark mark='a'/>He proved that the "
            "square has no more points than its side, and wrote to Dedekind, in French: I see it, but I do not "
            "believe it. <bookmark mark='b'/>The idea is to interleave digits. A point of the square has two "
            "coordinates. Alternate their digits, and you have a single number: a point of the line. Done carefully, "
            "this is a one-to-one correspondence. <bookmark mark='c'/>Giuseppe Peano and David Hilbert then found "
            "something even stranger: continuous curves that pass through every point of the square. Here is "
            "Hilbert's, at ever finer stages. <bookmark mark='d'/>Size, it turns out, does not see dimension. What "
            "makes the square two-dimensional is its topology, as Brouwer proved in 1911: no correspondence that is "
            "continuous both ways can flatten it onto a line."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(frame))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in inter], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(Create(curves[0]), FadeIn(cl))
            for k in range(1, 5):
                self.play(ReplacementTransform(curves[k - 1], curves[k]), run_time=1.1)
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()

    def continuum(self):
        head = label(r"Where is $2^{\aleph_0}$?", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        axis = NumberLine(x_range=[0, 6, 1], length=11.0, include_numbers=False, color=GREY_C).move_to([0, 0.6, 0])
        names = [r"\aleph_0", r"\aleph_1", r"\aleph_2", r"\aleph_3", r"\cdots", r"\aleph_\omega", r"\cdots"]
        labs = VGroup(*[MathTex(n, font_size=34, color=CARD).next_to(axis.n2p(i), DOWN, buff=0.25)
                        for i, n in enumerate(names)])
        ch = VGroup(Arrow(axis.n2p(1) + UP * 1.3, axis.n2p(1) + UP * 0.15, buff=0, color=GOAL),
                    label(r"CH: \ here", font_size=24, color=GOAL))
        ch[1].next_to(ch[0], UP, buff=0.1)
        no = VGroup(Cross(scale_factor=0.25, stroke_color=BAD).move_to(axis.n2p(5) + UP * 0.5),
                    label(r"not here: \ König (1905)", font_size=22, color=BAD).next_to(axis.n2p(5) + UP * 0.5, UP,
                                                                                        buff=0.3))
        facts = VGroup(label(r"Cantor's continuum hypothesis (1878): \ $2^{\aleph_0} = \aleph_1$", font_size=26,
                             color=GOAL),
                       label(r"König: \ $2^{\aleph_0}$ is not a countable limit of smaller alephs, \ so not $\aleph_\omega$",
                             font_size=24),
                       label(r"Easton (1970): \ beyond such restrictions, \ ZFC allows almost any value", font_size=24,
                             color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here are the alephs on a line. Where does the size of the real numbers sit? <bookmark mark='a'/>Cantor "
            "conjectured in 1878 that it is the very next one, aleph one: no set of real numbers is strictly between "
            "the natural numbers and the reals in size. This is the continuum hypothesis. <bookmark mark='b'/>Julius "
            "König showed in 1905 that it cannot be aleph omega, or any aleph that is a countable limit of smaller "
            "ones. <bookmark mark='c'/>And William Easton showed in 1970 that, beyond restrictions of this kind, the "
            "axioms are consistent with almost any value at all. Chapter 15 explains how such a thing can be proved."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(no), FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
        self.clear_scene()
