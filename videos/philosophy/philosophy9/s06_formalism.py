from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Formalism(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"A game with symbols", r"Is mathematics just marks and rules?", lit=(1572, 1925),
                            part=PART)
        with self.voiceover("Chapter five. A game with symbols."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.game()
        self.bombelli()
        self.hilbert()

    def game(self):
        hcs = VGroup(history_card(1872, r"Eduard Heine", r"numbers are signs on paper", width=4.4, color=HIST),
                     history_card(1880, r"Johannes Thomae", r"arithmetic as a game, \ like chess", width=4.4,
                                  color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.35)
        chess = VGroup(label(r"chess", font_size=28, color=CONCRETE),
                       label(r"pieces, \ legal moves, \ positions", font_size=22, color=GREY_A)).arrange(DOWN,
                                                                                                    buff=0.12)
        arith = VGroup(label(r"arithmetic", font_size=28, color=NUM),
                       label(r"numerals, \ rules of calculation, \ equations", font_size=22, color=GREY_A)).arrange(
            DOWN, buff=0.12)
        pair = VGroup(chess, arith).arrange(RIGHT, buff=2.2).move_to([0, 0.7, 0])
        arr = DoubleArrow(chess.get_right(), arith.get_left(), buff=0.3, color=GREY_B, stroke_width=2)
        q = quote_card(r"It is applicability alone which elevates arithmetic from a game to the rank of a science.",
                       r"Gottlob Frege", r"\textit{Grundgesetze der Arithmetik} II, \S 91, \ 1903", width=10.0,
                       font_size=26).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The third answer says that mathematics is about nothing at all. <bookmark mark='a'/>In the 1870s and "
            "1880s Eduard Heine and Johannes Thomae proposed that numbers are signs, and arithmetic a game played "
            "with them, like chess. <bookmark mark='b'/>Chess has pieces, legal moves and positions; arithmetic has "
            "numerals, rules of calculation, and the equations they produce. A chess position is not true or false, "
            "and needs no objects to be about. <bookmark mark='c'/>Frege attacked the view at length in 1903. A "
            "chess position tells you nothing about the world, but arithmetic does: it tells you how many chairs "
            "to bring. It is applicability alone, he wrote, which elevates arithmetic from a game to the rank of a "
            "science."
        ) as vo:
            self.play(FadeIn(hcs))
            vo.wait_until("b")
            self.play(FadeIn(pair), GrowFromCenter(arr))
            vo.wait_until("c")
            self.play(FadeIn(q))
        self.clear_scene()

    def bombelli(self):
        d = load("bombelli")
        hc = history_card(1572, r"Rafael Bombelli", r"\textit{L'Algebra}", width=4.0, color=HIST).to_corner(UL,
                                                                                                          buff=0.35)
        lines = [r"x^3 = 15x + 4",
                 r"x = \sqrt[3]{2 + \sqrt{-121}} + \sqrt[3]{2 - \sqrt{-121}}",
                 r"(2 + \sqrt{-1})^3 = 2 + 11\sqrt{-1} = 2 + \sqrt{-121}",
                 r"x = (2 + \sqrt{-1}) + (2 - \sqrt{-1}) = 4",
                 r"4^3 = 64 = 15 \cdot 4 + 4"]
        glosses = [r"a cubic with three real roots", r"Cardano's formula (1545): \ a square root of $-121$",
                   rf"Bombelli: \ treat $\sqrt{{-1}}$ as a symbol obeying the rules", r"the imaginary parts cancel",
                   r"and the answer checks"]
        cols = [WHITE, GOAL, CONN, NUM, OK]
        tab = VGroup()
        for i, (f, g, c) in enumerate(zip(lines, glosses, cols)):
            y = 1.9 - 0.82 * i
            tab.add(VGroup(MathTex(f, font_size=32, color=c).move_to([-6.4, y, 0], aligned_edge=LEFT),
                           label(g, font_size=20, color=GREY_A).move_to([-6.4, y - 0.38, 0], aligned_edge=LEFT)))
        assert tuple(d["cube"]) == (2, 11) and d["x"] == 4 and d["check"] and d["disc"] == "-121"
        ax = Axes(x_range=[-5, 5, 1], y_range=[-40, 40, 20], x_length=4.6, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "stroke_width": 2}).move_to([3.9, -0.6, 0])
        curve = ax.plot(lambda x: x ** 3 - 15 * x - 4, x_range=[-4.6, 4.75], color=NUM, stroke_width=3)
        roots = VGroup(*[Dot(ax.c2p(r, 0), radius=0.07, color=OK) for r in d["real_roots"]])
        rl = label(r"$y = x^3 - 15x - 4$: \ three real roots, \ $4$ and $-2 \pm \sqrt{3}$", font_size=20,
                   color=GREY_A).next_to(ax, DOWN, buff=0.15)
        moral = label(r"a real answer, \ reached through `impossible' numbers: \ the game ran ahead of the meaning",
                      font_size=24, color=OK).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Yet there are moments when the game runs ahead of the meaning. <bookmark mark='a'/>Take the cubic x "
            "cubed equals fifteen x plus four. Its graph crosses the axis three times, so it has three real roots. "
            "<bookmark mark='b'/>Cardano's formula of 1545 gives a root, but on the way it asks for the square root "
            "of minus one hundred and twenty-one, which in 1545 did not exist. <bookmark mark='c'/>In 1572 Rafael "
            "Bombelli simply calculated with the square root of minus one as a symbol obeying the usual rules. "
            "Two plus that symbol, cubed, comes out as two plus the square root of minus one hundred and "
            "twenty-one. So the cube roots in the formula are two plus and two minus the symbol. "
            "<bookmark mark='d'/>Add them: the imaginary parts cancel, and x is four. <bookmark mark='e'/>And four "
            "is a root: sixty-four equals sixty plus four. The Reasoner does the complex arithmetic and checks it. "
            "<bookmark mark='f'/>A real answer, reached through numbers nobody believed in. For two centuries the "
            "symbols worked before anyone could say what they meant."
        ) as vo:
            self.play(FadeIn(hc), Create(ax), Create(curve), FadeIn(roots), FadeIn(rl))
            for mk, r in zip("abcde", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(moral))
        self.clear_scene()

    def hilbert(self):
        hc = history_card(1925, r"David Hilbert", r"`On the infinite'", width=4.4, color=HIST).to_corner(UL, buff=0.35)
        q = quote_card(r"If the arbitrarily given axioms do not contradict one another with all their consequences, then "
                       r"they are true and the things defined by the axioms exist.", r"David Hilbert",
                       r"letter to Frege, \ 29 December 1899", width=8.4, font_size=24).to_corner(UR, buff=0.35)
        real = VGroup(label(r"real statements", font_size=28, color=CONCRETE),
                      label(r"finite and checkable: \ $2 + 3 = 5$", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.12)
        ideal = VGroup(label(r"ideal statements", font_size=28, color=ABSTRACT),
                       label(r"about the infinite: \ instruments, \ like Bombelli's $\sqrt{-1}$", font_size=20,
                             color=GREY_A)).arrange(DOWN, buff=0.12)
        cols = VGroup(real, ideal).arrange(RIGHT, buff=1.4).move_to([0, -0.4, 0])
        cons = label(r"the ideal part is safe if it never proves a false real statement: \ a consistency proof would "
                     r"show it", font_size=23, color=GOAL).next_to(cols, DOWN, buff=0.45)
        godel = label(r"Gödel (Part 7): \ no such proof inside the system, \ let alone from finite means", font_size=23,
                      color=BAD).next_to(cons, DOWN, buff=0.25)
        today = label(r"what survives: \ deductivism, \ `mathematics says what follows from what' \ (Curry, 1951)",
                      font_size=22, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "David Hilbert's formalism was subtler than the game view. <bookmark mark='a'/>To Frege he wrote, in "
            "1899: if the arbitrarily given axioms do not contradict one another with all their consequences, then "
            "they are true and the things defined by the axioms exist. Consistency is all the existence mathematics "
            "needs. <bookmark mark='b'/>In his 1925 lecture on the infinite he divided mathematics in two. Real "
            "statements are finite and checkable, such as two plus three is five. <bookmark mark='c'/>Ideal "
            "statements, about the infinite, are like Bombelli's square root of minus one: instruments that need not "
            "mean anything, as long as they lead to true real statements. <bookmark mark='d'/>The ideal part is "
            "safe if it never proves a false real statement, and a proof of consistency would show that. "
            "<bookmark mark='e'/>Part 7 told the rest: by Gödel's second theorem, no such proof exists inside the "
            "system, let alone by finite means. <bookmark mark='f'/>What survives is a modest cousin, deductivism: "
            "a mathematical theorem says only that its axioms imply it. Haskell Curry, in 1951, called mathematics "
            "the science of formal systems."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(real))
            vo.wait_until("c")
            self.play(FadeIn(ideal))
            vo.wait_until("d")
            self.play(FadeIn(cons))
            vo.wait_until("e")
            self.play(FadeIn(godel))
            vo.wait_until("f")
            self.play(FadeIn(today))
        self.clear_scene()
