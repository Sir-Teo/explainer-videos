from __future__ import annotations

import numpy as np

from videos.music.music9.common import *  # noqa: F403


class Shape(SoundScene):
    def construct(self):
        chapter(self, 9, r"Hearing a shape", r"Can one hear the shape of a drum?", lit=(1877,), extra=((1966, r"Kac's question"), (1992, r"two drums, one spectrum")))
        self.weyl()
        self.count()
        self.pair()
        self.fold()
        self.quiz()
        self.answer()

    # ------------------------------------------------------------------
    def weyl(self):
        d = load("shape")
        g = axes([0, 320], [0, 80], x_length=6.4, y_length=3.8, xlabel=r"frequency squared (scaled)", ylabel=r"modes below it", xticks=[0, 100, 200, 300], yticks=[0, 20, 40, 60, 80], font_size=20)
        g.move_to(RIGHT * 3.0 + DOWN * 0.5)
        lam = np.asarray(d["lam"])
        steps = VMobject(stroke_color=SKIN, stroke_width=3).set_points_as_corners([g.ax.c2p(x, y) for x, y in zip(lam, d["counted"])])
        wl = curve_from(g, lam, np.maximum(d["weyl"], 0), TUNE, stroke_width=2.5)
        key = VGroup(label(r"counted: \ a drum's modes", font_size=22, color=SKIN), label(r"Weyl's formula: \ area and rim only", font_size=22, color=TUNE)).arrange(DOWN, buff=0.06, aligned_edge=LEFT).next_to(g, UP, buff=0.15)
        notes = VGroup(label(r"Kac, \ 1966: \ suppose you knew every overtone", font_size=26, color=GREY_A),
                       MathTex(r"N \approx \frac{\text{area}}{4\pi}\,\lambda - \frac{\text{rim}}{4\pi}\sqrt{\lambda}", font_size=34, color=TUNE),
                       label(r"so the overtones tell you \\ the drum's area, \ and the length of its rim", font_size=26, color=GOOD),
                       label(r"Kac added: \ and how many holes it has", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(LEFT * 3.5 + DOWN * 0.2)
        with self.voiceover(
            "Now back to Mark Kac. His drum is an ideal skin of any outline, and you are told every one of "
            "its overtones, to any accuracy. What can you work out? <bookmark mark='a'/> Quite a lot. Count "
            "how many modes lie below each frequency. Hermann Weyl proved in 1911 that the count grows in "
            "proportion to the area of the skin, with a correction in proportion to the length of its rim, "
            "and nothing else about the shape comes into it. Here is the count for one drum, and Weyl's "
            "formula laid over it. <bookmark mark='b'/> So from the overtones alone you can hear how big a "
            "drum is, and how long its edge. Kac showed you can also hear how many holes it has. With that "
            "much decided by the sound, it seemed a fair guess that the whole shape was."
        ) as vo:
            self.play(FadeIn(notes[0]), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(steps), FadeIn(key[0]), run_time=2.0)
            self.play(Create(wl), FadeIn(key[1]), FadeIn(notes[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        title = label(r"A worked example: \ hearing how big a drum is", font_size=36).to_edge(UP, buff=0.4)
        ask = pause_card(r"The count of modes grows as the drum's area \\ times the frequency squared. \\ One drum has its hundredth mode at 1000 Hz. \\ A second, \ of the same skin and tension, \ has twice the area. \\ Where is its hundredth mode?", width=7.6, font_size=28).move_to(UP * 0.3)
        work = VGroup(MathTex(r"N \propto \text{area} \times f^2", font_size=40),
                      MathTex(r"2 \times f^2 = 1000^2 \quad\Rightarrow\quad f = \frac{1000}{\sqrt2} = 707\ \text{Hz}", font_size=38, color=TUNE),
                      label(r"twice the area: \ every count is reached half an octave sooner", font_size=28, color=GREY_A),
                      label(r"a big drum is not just lower: \ its overtones are packed closer", font_size=28, color=GOOD)).arrange(DOWN, buff=0.3).move_to(DOWN * 0.6)
        with self.voiceover(
            "A worked example of hearing size. The count of modes grows as the area of the drum times the "
            "square of the frequency. Suppose one drum has its hundredth mode at a thousand hertz. A second "
            "drum, of the same skin at the same tension, has twice the area. Where is its hundredth mode? "
            "Pause, and work it out."
        ):
            self.play(FadeIn(title), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "Twice the area, so the frequency squared must halve to keep the count at a hundred. A thousand "
            "over the square root of two: seven hundred and seven hertz. <bookmark mark='a'/> Every count is "
            "reached half an octave sooner. So a big drum is not only lower than a small one. Its overtones "
            "are packed more closely, and that crowding is something you hear, as the difference between a "
            "bass drum's rumble and a bongo's pop, whatever the shapes."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(work[0]), FadeIn(work[1]))
            vo.wait_until("a")
            self.play(FadeIn(work[2]), FadeIn(work[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fold(self):
        d = load("shape")
        sc = 0.95
        t1 = [[(0, 0), (1, 0), (0, 1)], [(1, 0), (1, 1), (0, 1)], [(0, 1), (1, 1), (1, 2)], [(1, 1), (2, 1), (1, 2)], [(2, 1), (2, 2), (1, 2)], [(1, 2), (2, 2), (2, 3)], [(2, 1), (3, 2), (2, 2)]]
        t2 = [[(1, 0), (1, 1), (0, 1)], [(0, 1), (1, 1), (0, 2)], [(1, 1), (1, 2), (0, 2)], [(1, 1), (2, 1), (1, 2)], [(2, 1), (2, 2), (1, 2)], [(2, 1), (3, 2), (2, 2)], [(2, 2), (3, 2), (2, 3)]]

        def tiles(tris, col, at):
            g = VGroup(*[Polygon(*[np.array([x * sc, y * sc, 0.0]) for x, y in t], stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.1 + 0.07 * (k % 3)) for k, t in enumerate(tris)])
            return g.move_to(at)

        a, b = tiles(t1, SKIN, LEFT * 3.6 + UP * 0.9), tiles(t2, AIR, RIGHT * 3.6 + UP * 0.9)
        arrow = Arrow(LEFT * 1.3 + UP * 0.9, RIGHT * 1.3 + UP * 0.9, color=GREY_B, stroke_width=3, buff=0)
        al = label(r"cut, \ turn over, \ add", font_size=24, color=GREY_B).next_to(arrow, UP, buff=0.15)
        head = label(r"Why they sound alike", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        rows = VGroup(label(r"each drum is seven copies of one triangle", font_size=26, color=GREY_A),
                      label(r"a mode of the first, \ cut into its seven pieces, \ rebuilds as a mode of the second: \\ each new piece is a sum of three old ones", font_size=26, color=TUNE),
                      label(r"the pieces still join smoothly, \ and still vanish at the rim: \ so it is a mode, \ at the same frequency", font_size=26, color=GOOD)).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How can that be? The proof is something you could do with scissors. <bookmark mark='a'/> Each "
            "drum is seven copies of the same triangle, joined along their edges in a different pattern. "
            "<bookmark mark='b'/> Take any mode of the first drum, and cut it along those edges into seven "
            "triangular pieces. Now build a shape on the second drum: on each of its triangles, lay three "
            "of the seven pieces on top of one another, some of them flipped over, and add them. Which three, "
            "and which way up, is a fixed recipe. <bookmark mark='c'/> The recipe is arranged so that where "
            "two triangles of the second drum meet, the sums join smoothly, and where a triangle lies on "
            "the rim, the sum comes to zero. A smooth shape that vanishes on the rim and ripples at one "
            "frequency is a mode. So every note of the first drum is a note of the second, and the same "
            "recipe run backwards gives the reverse. The idea came from the theory of symmetry, where "
            "Toshikazu Sunada had shown in 1985 how to manufacture such pairs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(b), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(al), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pair(self):
        d = load("shape")
        e1, e2 = np.asarray(d["eigs1"]), np.asarray(d["eigs2"])
        sc = 0.72
        a = polygon_shape(d["drum1"], sc).move_to(LEFT * 4.6 + UP * 1.5)
        b = polygon_shape(d["drum2"], sc).move_to(LEFT * 4.6 + DOWN * 1.5)
        ia = mode_image(np.asarray(d["a0"]), 3 * sc).move_to(a.get_center())
        ib = mode_image(np.asarray(d["b0"]), 3 * sc).move_to(b.get_center())
        ia4 = mode_image(np.asarray(d["a4"]), 3 * sc).move_to(a.get_center())
        ib4 = mode_image(np.asarray(d["b4"]), 3 * sc).move_to(b.get_center())
        card = history_card(1992, r"Carolyn Gordon, \ David Webb and Scott Wolpert", r"two flat shapes, each made of the same seven triangles, differently joined.", width=5.6, font_size=20).move_to(RIGHT * 2.2 + UP * 2.75)
        tab = VGroup()
        for k in range(6):
            tab.add(VGroup(label(str(k + 1), font_size=24, color=GREY_B), label(rf"{e1[k]:.4f}", font_size=26, color=SKIN), label(rf"{e2[k]:.4f}", font_size=26, color=AIR)))
        for k, r in enumerate(tab):
            r[0].move_to(LEFT * 0.6 + UP * (0.85 - 0.46 * k))
            r[1].move_to(RIGHT * 1.2 + UP * (0.85 - 0.46 * k))
            r[2].move_to(RIGHT * 3.6 + UP * (0.85 - 0.46 * k))
        th = VGroup(label(r"mode", font_size=22, color=GREY_B).move_to(LEFT * 0.6 + UP * 1.35), label(r"the upper drum", font_size=22, color=SKIN).move_to(RIGHT * 1.2 + UP * 1.35), label(r"the lower drum", font_size=22, color=AIR).move_to(RIGHT * 3.6 + UP * 1.35))
        ours, pub = d["ours"], d["driscoll"]
        check = VGroup(label(rf"largest difference between the columns: \ {d['largest_gap']:.0e}", font_size=24, color=GOOD),
                       label(rf"the first, \ rescaled: \ {ours[0]:.4f}. \ Published (Driscoll, \ 1997): \ {pub[0]:.4f}", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(RIGHT * 2.0 + DOWN * 2.6)
        with self.voiceover(
            "In 1992 Carolyn Gordon, David Webb and Scott Wolpert settled it, with a pair of shapes you could "
            "cut out of card. <bookmark mark='a'/> Each is made of the same seven triangles, joined along "
            "different edges. They have the same area and the same length of rim, as Weyl says they must. "
            "They are plainly not the same shape: no turning or flipping lays one on the other. "
            "<bookmark mark='b'/> Monochord stretches a skin over each, and solves for its modes. Here are "
            "the six lowest of each drum. <bookmark mark='c'/> They are the same. Not close: the same, to "
            "thirteen decimal places, which is as many as the computer keeps. The lowest, rescaled to the "
            "size used in the mathematical literature, comes out at "
            f"{say(ours[0], 4)}, against a published value of {say(pub[0], 4)}; the small difference is our "
            "grid. <bookmark mark='d'/> The modes themselves look quite different on the two drums. Here is "
            "the lowest of each, and here the fifth. Different shapes, different patterns of motion, and "
            "identical notes, all the way up."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(b))
            vo.wait_until("b")
            self.play(FadeIn(th), LaggedStart(*[FadeIn(r) for r in tab], lag_ratio=0.25), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(check[0]))
            self.play(FadeIn(check[1]))
            vo.wait_until("d")
            self.play(FadeIn(ia), FadeIn(ib))
            self.wait(max(vo.remaining() - 6.0, 0.1))
            self.play(FadeOut(ia), FadeOut(ib), FadeIn(ia4), FadeIn(ib4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("shape")
        c = clip("shape.three")
        q = listen_card(r"Three drums of the same area, \ each sounding its twelve lowest modes. \\ Two of them have exactly the same notes. \ Which is the odd one out?", width=9.6, font_size=26).to_edge(UP, buff=0.35)
        bx = boxes(("A", "B", "C"), buff=1.2, width=2.6, height=1.2).move_to(UP * 0.5)
        with self.voiceover(
            "You can check this with your own ears. Three drums of the same area, each sounding its twelve "
            "lowest modes. Two of them have exactly the same notes. Which is the odd one out?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"three drums", detail=r"computed modes of three skins", corner=DL, tag_corner=DR)
            for ev, b in zip("ABC", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 1.6)
        sc = 0.5
        sa = polygon_shape(d["drum1"], sc).next_to(bx[0], DOWN, buff=0.4)
        sq = Square(side_length=d["side"] * sc, color=BAD, stroke_width=3, fill_color=BAD, fill_opacity=0.12).next_to(bx[1], DOWN, buff=0.4)
        sb = polygon_shape(d["drum2"], sc, color=AIR).next_to(bx[2], DOWN, buff=0.4)
        with self.voiceover(
            "B, the middle one. It was a square drum of the same area: you can hear that it is the same "
            "size, and you can hear that it is a different shape. A and C were the two drums of 1992. Not "
            "even a perfect ear could tell which of them it was listening to."
        ):
            self.play(FadeOut(q), FadeIn(sa), FadeIn(sq), FadeIn(sb))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def answer(self):
        head = label(r"So: \ can one hear the shape of a drum?", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"not always", r"two different drums can have every overtone in common. \\ The proof cuts a mode of one into seven triangles and reassembles it on the other."),
            (r"it has been tried", r"1994: \ two metal boxes in these shapes, \ filled with microwaves. \\ Their resonances agreed, \ line for line."),
            (r"but often", r"a triangle can be heard; \ so can a drum with a smooth, \ symmetric outline. \\ The known exceptions all have corners."),
            (r"and always", r"its area, \ the length of its rim, \ and the number of its holes."),
        ], left=-6.5, text_left=-3.6, top=1.9, step=1.42, name_size=28, text_size=23, color=SKIN)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "So, can one hear the shape of a drum? <bookmark mark='a'/> Not always. Two different drums can "
            "share every overtone. The proof is a piece of paper folding: take any mode of one drum, cut it "
            "along the seven triangles, and the pieces, with some of them turned over, fit together into a "
            "mode of the other drum at the same frequency. <bookmark mark='b'/> In 1994 two physicists built "
            "the shapes as flat copper boxes and filled them with microwaves, which obey the same equation "
            "as a drumhead. The resonances of the two boxes agreed, line for line. <bookmark mark='c'/> But "
            "the answer is often yes. A triangle is known by its overtones. So is a drum with a smooth, "
            "symmetric outline. Every pair of sound-alike drums found so far has corners. <bookmark mark='d'/> "
            "And always, whatever the shape, you can hear its area, the length of its rim, and the number "
            "of holes in it. Which is a good deal more than Kac's audience expected."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
