from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Structure(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"What numbers could not be", r"If numbers are not objects, \ what are they?",
                            lit=(1888, 1997), part=PART)
        with self.voiceover("Chapter nine. What numbers could not be."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ernie()
        self.dedekind()
        self.kinds()
        self.identity()
        self.graphs()
        self.brick()

    def ernie(self):
        hc = history_card(1965, r"Paul Benacerraf", r"`What numbers could not be'", width=5.0, color=HIST).to_corner(
            UL, buff=0.35)
        rowsZ = VGroup(*[nested_boxes(k, "Z", unit=0.22, color=CONCRETE) for k in range(4)]).arrange(RIGHT, buff=0.45)
        rowsV = VGroup(*[nested_boxes(k, "V", unit=0.22, color=ABSTRACT) for k in range(4)]).arrange(RIGHT, buff=0.45)
        lZ = label(r"Johnny learned Zermelo's numbers: \ $n + 1 = \{n\}$", font_size=24, color=CONCRETE)
        lV = label(r"Ernie learned von Neumann's: \ $n + 1 = \{0, \dots, n\}$", font_size=24, color=ABSTRACT)
        blockZ = VGroup(lZ, rowsZ).arrange(DOWN, buff=0.25)
        blockV = VGroup(lV, rowsV).arrange(DOWN, buff=0.25)
        both = VGroup(blockZ, blockV).arrange(DOWN, buff=0.45).move_to([0.6, 0.25, 0])
        nums = VGroup(*[MathTex(str(k), font_size=26, color=NUM).next_to(rowsZ[k], DOWN, buff=0.1) for k in range(4)])
        nums2 = VGroup(*[MathTex(str(k), font_size=26, color=NUM).next_to(rowsV[k], DOWN, buff=0.1) for k in range(4)])
        verdict = VGroup(label(r"both count, \ add and multiply perfectly; \ they disagree whether $1 \in 3$ \ (Part 6)",
                               font_size=23, color=GREY_A),
                         label(r"nothing could decide who is right: \ so numbers are not sets, \ and not objects at "
                               r"all", font_size=24, color=GOAL)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Benacerraf's second dilemma came first, in 1965, as a story about two children. <bookmark mark='a'/>"
            "Johnny was taught that the numbers are Zermelo's sets: zero is the empty set, and each number is the "
            "set containing the one before. <bookmark mark='b'/>Ernie was taught von Neumann's: each number is the "
            "set of all the numbers before it. <bookmark mark='c'/>Both count, add and multiply perfectly. They "
            "disagree only about questions like whether one is a member of three, the junk theorems of Part 6. "
            "<bookmark mark='d'/>If numbers really were sets, one of them would be wrong. But nothing in "
            "arithmetic could decide which. Benacerraf concluded that numbers are not sets, and more boldly, that "
            "they are not objects at all."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(blockZ), FadeIn(nums))
            vo.wait_until("b")
            self.play(FadeIn(blockV), FadeIn(nums2))
            vo.wait_until("c")
            self.play(FadeIn(verdict[0]))
            vo.wait_until("d")
            self.play(FadeIn(verdict[1]))
        self.clear_scene()

    def dedekind(self):
        d = load("transport")
        q = quote_card(r"Arithmetic is therefore the science that elaborates the abstract structure that all progressions "
                       r"have in common merely in virtue of being progressions.", r"Paul Benacerraf",
                       r"`What numbers could not be', \ 1965", width=10.4, font_size=26).to_edge(UP, buff=0.35)
        hd = [label(r"number", font_size=22, color=P.CLAIM), label(r"unary numeral", font_size=22, color=CONCRETE),
              label(r"binary numeral", font_size=22, color=ABSTRACT), label(r"even?", font_size=22, color=P.CLAIM)]
        rows = [[MathTex(str(k), font_size=26), MathTex(rf"\mathsf{{{u}}}", font_size=24, color=CONCRETE),
                 MathTex(rf"\mathtt{{{b}}}", font_size=26, color=ABSTRACT), e] for k, u, b, e in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[1.3, 2.7, 2.1, 1.2], cell_h=0.4, font_size=22).move_to([-3.2, -1.3, 0])
        assert d["inverse"] and d["respects_successor"] and d["even_is_last_bit_zero"]
        side = VGroup(
            VGroup(label(r"Dedekind (1888):", font_size=22, color=NUM),
                   label(r"any two progressions are isomorphic", font_size=22, color=NUM)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"the Reasoner: \ the maps between them", font_size=20, color=OK),
                   label(rf"are inverse, \ and respect successor \ (checked to {d['checked']})", font_size=20,
                         color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"so every arithmetic truth", font_size=22, color=GOAL),
                   label(r"holds in both alike", font_size=22, color=GOAL)).arrange(DOWN, aligned_edge=LEFT,
                                                                                 buff=0.1)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -1.3, 0])
        with self.voiceover(
            "What is left, if numbers are not objects? <bookmark mark='a'/>Benacerraf answered: arithmetic is the "
            "science that elaborates the abstract structure that all progressions have in common merely in virtue "
            "of being progressions. <bookmark mark='b'/>Richard Dedekind had proved, in 1888, that any two "
            "progressions satisfying his axioms are isomorphic: they match point for point, with successor matching "
            "successor. <bookmark mark='c'/>The Reasoner tries two progressions of numerals, strokes and binary. The "
            "maps between them are inverse to each other, and carry successor to successor. <bookmark mark='d'/>"
            "So every truth of arithmetic, such as which numbers are even, holds in both alike. Arithmetic cannot "
            "tell them apart, and does not need to."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r][:3])) for r in range(len(rows))], lag_ratio=0.2),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][3]) for r in range(len(rows))], lag_ratio=0.2),
                      FadeIn(side[2]))
        self.clear_scene()

    def kinds(self):
        head = label(r"Three structuralisms", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        specs = ((r"\textit{ante rem}", r"Shapiro (1997); \ Resnik (1997)",
                  [r"structures exist;", r"numbers are places in one"], ABSTRACT),
                 (r"eliminative", r"Benacerraf; \ \textit{in re}",
                  [r"`2 + 2 = 4' means: \ in every progression,", r"the place 2 + 2 is the place 4"], NUM),
                 (r"modal", r"Hellman (1989)",
                  [r"if there were a progression, \ then in it \dots", r"no objects needed"], OK))
        cols = VGroup()
        for a, b, lines, c in specs:
            col = VGroup(label(a, font_size=28, color=c), label(b, font_size=21, color=WHITE),
                         *[label(t, font_size=20, color=GREY_A) for t in lines]).arrange(DOWN, buff=0.18)
            cols.add(col)
        cols.arrange(RIGHT, buff=0.9).move_to([0, 0.4, 0])
        if cols.width > 13.2:
            cols.width = 13.2
        moral = label(r"each keeps the mathematics, \ and differs on what exists", font_size=24,
                      color=GOAL).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "This is structuralism, and it comes in three kinds. <bookmark mark='a'/>For Stewart Shapiro and "
            "Michael Resnik, writing in 1997, structures themselves exist, and a number is a place in one, as "
            "shortstop is a position on a baseball team, whoever plays it. <bookmark mark='b'/>For eliminative "
            "structuralists, there are no structures over and above their instances: 'two plus two is four' says "
            "that in every progression, the place for two plus two is the place for four. <bookmark mark='c'/>And "
            "for Geoffrey Hellman's modal structuralism, not even actual progressions are needed: arithmetic says "
            "what would hold in any progression, if there were one. <bookmark mark='d'/>All three keep the "
            "mathematics. They differ on what exists."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abc", cols):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()

    def identity(self):
        d = load("roots")
        head = label(r"Which one is $i$?", font_size=34, color=CONN).to_edge(UP, buff=0.45)
        R = 1.7
        c0 = np.array([-3.4, -0.2, 0])
        angles = [0, PI / 2, PI, 3 * PI / 2]
        names = [r"1", r"i", r"-1", r"-i"]
        ring = Circle(radius=R, color=GREY_D, stroke_width=2).move_to(c0)
        dots = VGroup(*[Dot(c0 + R * np.array([np.cos(a), np.sin(a), 0]), radius=0.09,
                            color=NUM if k % 2 == 0 else ABSTRACT) for k, a in enumerate(angles)])
        labs = VGroup(*[MathTex(n, font_size=32, color=NUM if k % 2 == 0 else ABSTRACT).move_to(
            c0 + (R + 0.45) * np.array([np.cos(a), np.sin(a), 0])) for k, (n, a) in enumerate(zip(names, angles))])
        axis = DashedLine(c0 + LEFT * (R + 0.8), c0 + RIGHT * (R + 0.8), color=GREY_B, stroke_width=1.5)
        assert [tuple(p) for p in d["autos"]] == [(0, 1, 2, 3), (0, 3, 2, 1)] and d["fixed"] == [0, 2]
        rows = VGroup(
            label(r"$\{1, i, -1, -i\}$ under multiplication: \ the Reasoner finds 2 symmetries", font_size=22),
            label(r"the identity, \ and the swap $i \leftrightarrow -i$ \ (complex conjugation)", font_size=22,
                  color=ABSTRACT),
            label(r"$1$ and $-1$ are fixed; \ $i$ and $-i$ \ share every structural property", font_size=22,
                  color=GOAL),
            label(r"so if a number is only a place in a structure, \ is $i = -i$?", font_size=24, color=BAD),
            label(r"Burgess (1999); \ Keränen (2001)", font_size=20, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28).move_to([2.9, -0.2, 0])
        with self.voiceover(
            "Structuralism has its own puzzle, and the complex numbers pose it. <bookmark mark='a'/>Take the four "
            "fourth roots of one: one, i, minus one, minus i. <bookmark mark='b'/>The Reasoner looks for every "
            "rearrangement of the four that preserves multiplication, and finds two: doing nothing, and swapping i "
            "with minus i, which is complex conjugation, a reflection in the real axis. <bookmark mark='c'/>So one "
            "and minus one are fixed, but i and minus i have exactly the same structural properties. Whatever the "
            "structure says of one, it says of the other. <bookmark mark='d'/>If a number is nothing but a place in "
            "a structure, what makes i different from minus i? John Burgess and Jukka Keränen pressed the point "
            "around 2000."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ring), FadeIn(dots), FadeIn(labs))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), Create(axis))
            self.play(Swap(labs[1], labs[3]), run_time=1.5)
            self.play(Swap(labs[1], labs[3]), run_time=1.5)
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
        self.clear_scene()

    def graphs(self):
        d = load("graphs")
        head = label(r"Symmetry decides what structure can tell apart", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        layouts = {"two points": [(-0.5, 0), (0.5, 0)], "two points, joined": [(-0.5, 0), (0.5, 0)],
                   "a path of three": [(-0.8, 0), (0, 0), (0.8, 0)],
                   "a triangle with a tail": [(-0.7, -0.4), (0.1, -0.4), (-0.3, 0.3), (0.7, 0.55)],
                   "an asymmetric graph": [(-1.0, -0.3), (-0.5, 0.25), (0, -0.3), (0.5, 0.25), (0.8, -0.35),
                                           (1.25, 0.25)]}
        cards = VGroup()
        for name, info in d.items():
            pts = [np.array([x, y, 0]) for x, y in layouts[name]]
            fixed = set(info["fixed"])
            g = VGroup(*[Line(pts[a], pts[b], color=GREY_B, stroke_width=3) for a, b in info["edges"]])
            g.add(*[Dot(p, radius=0.1, color=OK if k in fixed else GOAL) for k, p in enumerate(pts)])
            cap = VGroup(label(name, font_size=20, color=WHITE),
                         label(rf"{info['autos']} symmetr{'y' if info['autos'] == 1 else 'ies'}", font_size=18,
                               color=GREY_A)).arrange(DOWN, buff=0.08)
            cards.add(VGroup(g, cap).arrange(DOWN, buff=0.3))
        cards.arrange(RIGHT, buff=0.55, aligned_edge=DOWN).move_to([0, 0.9, 0])
        if cards.width > 13.4:
            cards.width = 13.4
        key = label(r"green: \ fixed by every symmetry, \ so the structure picks it out; \ yellow: \ not",
                    font_size=21, color=GREY_A).next_to(cards, DOWN, buff=0.4)
        replies = VGroup(
            label(r"Shapiro (2008): \ identity is primitive; \ structure need not \textit{ground} it", font_size=22,
                  color=ABSTRACT),
            label(r"Ladyman (2005): \ two joined points are \textit{weakly} discernible: \ a relation holds between "
                  r"them, \ never of one to itself", font_size=22, color=OK)).arrange(DOWN, buff=0.2).to_edge(
            DOWN, buff=0.45)
        with self.voiceover(
            "The Reasoner can survey the question on small graphs. <bookmark mark='a'/>For each, it finds every "
            "symmetry: every rearrangement of the points that preserves the lines. A point that every symmetry "
            "leaves in place is one the structure itself picks out; it is coloured green. Two bare points can be "
            "swapped, so neither is picked out. A path of three fixes its middle, but not its ends. A triangle with a "
            "tail fixes two of its points. And this graph of six points has no symmetry but the trivial one, so "
            "structure alone distinguishes all six. <bookmark mark='b'/>Two replies. Shapiro, in 2008: identity is "
            "primitive, and structure need not ground it, so i and minus i are two places, with no further "
            "difference. <bookmark mark='c'/>James Ladyman, in 2005: two joined points are weakly discernible, since "
            "a relation holds between them that holds of neither to itself. The same goes for i and minus i: the "
            "relation 'adds up to zero' holds between them, but not between i and itself, since i plus i is not "
            "zero."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.5), FadeIn(key), run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(replies[0]))
            vo.wait_until("c")
            self.play(FadeIn(replies[1]))
        self.clear_scene()

    def brick(self):
        w = wall(upto=9, current=9).scale(0.42).move_to([-3.65, -0.2, 0])
        wc = wall_card(9, width=6.4, font_size=22).move_to([3.3, -0.2, 0])
        with self.voiceover(
            "This is the ninth brick in the Wall. <bookmark mark='a'/>The dream: to know mathematical objects as we "
            "know tables. The wall: Benacerraf's two dilemmas. Access: abstract objects cause nothing, so how could we "
            "know them? Identification: nothing in mathematics settles which objects the numbers are. What it forces: "
            "structure, fiction, or a special faculty of knowing."
        ) as vo:
            self.play(FadeIn(w))
            self.play(Indicate(w.brick[9], color=P.CONCL, scale_factor=1.08))
            vo.wait_until("a")
            self.play(FadeIn(wc))
        self.wait(1)
        self.clear_scene()
