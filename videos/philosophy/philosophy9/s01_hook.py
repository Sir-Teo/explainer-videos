from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.meno()
        self.puzzle()
        self.preview()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"Mathematics may be defined as the subject in which we never know what we are talking about, "
                       r"nor whether what we are saying is true.", r"Bertrand Russell",
                       r"`Recent work on the principles of mathematics', \ 1901", width=9.6,
                       font_size=28).next_to(t, DOWN, buff=0.6)
        with self.voiceover(
            "Part 9 asks a question that sounds simple. When we do mathematics, what are we talking about? "
            "<bookmark mark='a'/>Bertrand Russell joked, in 1901, that mathematics is the subject in which we never "
            "know what we are talking about, nor whether what we are saying is true. <bookmark mark='b'/>He meant it "
            "as praise: a proof holds whatever its symbols stand for. But the joke has an edge, and this part is "
            "about the edge."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=GOAL, scale_factor=1.03))
        self.clear_scene()

    def meno(self):
        d = load("meno")
        u = 0.8
        origin = np.array([-6.4, -3.1, 0])

        def sq(x0, y0, side, color, fill=0.0, width=3):
            return Polygon(*[origin + u * np.array(p + (0,)) for p in
                             ((x0, y0), (x0 + side, y0), (x0 + side, y0 + side), (x0, y0 + side))],
                           stroke_color=color, stroke_width=width, fill_color=color, fill_opacity=fill)
        grid = VGroup(*[sq(i, j, 1, GREY_D, width=1) for i in range(4) for j in range(4)])
        two = sq(0, 0, 2, NUM, 0.25)
        four = sq(0, 0, 4, BAD, 0.08)
        three = sq(0, 0, 3, GOAL, 0.1)
        diag = Polygon(*[origin + u * np.array(p) for p in ((2, 0, 0), (4, 2, 0), (2, 4, 0), (0, 2, 0))],
                       stroke_color=OK, stroke_width=4, fill_color=OK, fill_opacity=0.25)
        hc = history_card(r"c.\ 380 BCE", r"Plato, \textit{Meno}", r"Socrates questions a boy who has never studied "
                          r"geometry", width=5.6, color=HIST).to_corner(UR, buff=0.4)
        rows = VGroup(label(r"a square of side 2 has area 4: \ which square has area 8?", font_size=26),
                      label(rf"the boy: \ side 4? \ area {d['guesses'][0]['area']}, \ four times as big", font_size=24,
                            color=BAD),
                      label(rf"the boy: \ side 3? \ area {d['guesses'][1]['area']}, \ still too big", font_size=24,
                            color=GOAL),
                      label(rf"Socrates draws the diagonals: \ four half-squares, \ area {d['guesses'][2]['area']}",
                            font_size=24, color=OK),
                      label(r"Plato: \ the boy was not taught, \ he \textit{recollected}", font_size=24,
                            color=ABSTRACT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, -0.6, 0])
        with self.voiceover(
            "The question is old. <bookmark mark='a'/>In Plato's dialogue Meno, written about 380 BCE, Socrates "
            "draws in the sand for an enslaved boy who has never studied geometry. <bookmark mark='b'/>Here is a "
            "square of side two, with area four. Which square has twice the area? <bookmark mark='c'/>The boy "
            "doubles the side. But a square of side four has area sixteen, four times as big. <bookmark mark='d'/>"
            "Side three, then? Area nine: still too big. <bookmark mark='e'/>Socrates draws the diagonals. The "
            "square on the diagonal is made of four half-squares, so its area is eight, exactly twice four. "
            "<bookmark mark='f'/>Nobody told the boy the answer; he was only asked questions. Plato concluded that "
            "he had recollected it, from a life before this one. The answer was in him, not in the sand."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(grid), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(two), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(four), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeOut(four), Create(three), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeOut(three), Create(diag), FadeIn(rows[3]))
            vo.wait_until("f")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def puzzle(self):
        head = label(r"Three facts about `7 is prime'", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        cols = VGroup(*[VGroup(label(a, font_size=30, color=c), label(b, font_size=22, color=GREY_A),
                               label(e, font_size=20, color=GREY_B)).arrange(DOWN, buff=0.18)
                        for a, b, e, c in (
                            (r"necessary", r"it could not have been otherwise", r"true in every world \ (Part 4)",
                             ABSTRACT),
                            (r"a priori", r"known without looking at the world", r"the boy needed no ruler", NUM),
                            (r"applicable", r"it runs bridges, orbits and atoms", r"Wigner (1960): \ `unreasonable "
                             r"effectiveness'", CONCRETE))]).arrange(RIGHT, buff=0.8).move_to([0, 0.9, 0])
        q = VGroup(label(r"if it is about the world, \ why is it necessary and known a priori?", font_size=26),
                   label(r"if it is about something else, \ why does it apply to the world?", font_size=26),
                   label(r"and if it is about nothing at all, \ why is it true?", font_size=26, color=GOAL)).arrange(
            DOWN, buff=0.25).move_to([0, -2.0, 0])
        with self.voiceover(
            "Take any simple mathematical truth, say that seven is prime. <bookmark mark='a'/>Three things are true "
            "of it. It is necessary: it could not have been otherwise, which in Part 4's terms means true in every "
            "possible world. <bookmark mark='b'/>It is a priori: we know it without looking at the world, as the "
            "boy needed no ruler. <bookmark mark='c'/>And it is applicable: mathematics runs bridges, orbits and "
            "atoms. The physicist Eugene Wigner, in 1960, called this its unreasonable effectiveness. Complex "
            "numbers, invented to solve equations, turned out to be the language of quantum mechanics. "
            "<bookmark mark='d'/>Now the puzzle. If mathematics is about the world, why is it necessary, and known "
            "without looking? <bookmark mark='e'/>If it is about something else, why does it apply to the world? "
            "<bookmark mark='f'/>And if it is about nothing at all, why is it true?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abc", cols):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.15))
            for mk, r in zip("def", q):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def preview(self):
        head = label(r"Six answers", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        opts = VGroup(*[VGroup(label(a, font_size=28, color=c), label(b, font_size=21, color=GREY_A)).arrange(
            DOWN, buff=0.14) for a, b, c in (
            (r"platonism", r"abstract objects, \ outside space and time \ (Plato, Frege, Gödel)", ABSTRACT),
            (r"logicism", r"logic in disguise \ (Frege; \ Wright and Hale)", NUM),
            (r"formalism", r"a game with symbols \ (Hilbert, Curry)", CONN),
            (r"intuitionism", r"constructions of the mind \ (Brouwer)", PROOF),
            (r"structuralism", r"structures, \ not objects \ (Dedekind, Benacerraf, Shapiro)", OK),
            (r"fictionalism", r"a useful story \ (Field)", CONCRETE))]).arrange_in_grid(
            rows=3, cols=2, buff=(1.4, 0.55)).move_to([0, 0.15, 0])
        brick = label(r"this part's brick in the Wall: \ Benacerraf's two dilemmas", font_size=26,
                      color=P.WALL).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "Philosophers have given six main answers, and the part takes them in turn. <bookmark mark='a'/>"
            "Mathematics is about abstract objects, outside space and time: platonism. It is logic in disguise: "
            "logicism. It is a game played with symbols: formalism. It is about constructions of the mind: "
            "intuitionism. It is about structures, not objects: structuralism. Or it is a story, false but "
            "useful: fictionalism. <bookmark mark='b'/>Each answer meets two dilemmas posed by Paul Benacerraf, one "
            "about how we could know abstract objects, and one about which objects the numbers are. They are this "
            "part's brick in the Wall."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.1) for o in opts], lag_ratio=0.55), run_time=7)
            vo.wait_until("b")
            self.play(FadeIn(brick))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"platonism, \ and Benacerraf's problem of access",
            r"logicism: \ Frege's numbers, \ Frege's theorem, \ and bad company",
            r"formalism and Hilbert's ideal elements; \ Brouwer and the weak counterexamples",
            r"proofs as programs: \ the Curry--Howard correspondence, \ built",
            r"predicativity; \ structuralism and the identity of $i$ and $-i$",
            r"indispensability, \ fictionalism, \ and the Price List",
            r"univalence; \ Lakatos; \ diagrams; \ proofs checked by machine",
        ], font_size=25)
        with self.voiceover(
            "So: <bookmark mark='a'/>first platonism, and the problem of how we could know about abstract objects. "
            "<bookmark mark='b'/>Then Frege's attempt to build numbers out of logic, its collapse, and its revival. "
            "<bookmark mark='c'/>Then mathematics as a game, and mathematics as construction. <bookmark mark='d'/>"
            "Then the discovery that proofs are programs, built and run by the Reasoner. <bookmark mark='e'/>Then "
            "the vicious circle, and the view that mathematics is about structure. <bookmark mark='f'/>Then the "
            "argument from science, the reply that mathematics is a fiction, and the Price List. "
            "<bookmark mark='g'/>And last, mathematics as it is practised: a new foundation, proofs and "
            "refutations, pictures, and proofs checked by machine."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
