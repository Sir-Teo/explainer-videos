from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import CODE, CTRL, DATA, HEAD, HIST, LIMIT, NO, PART, YES


class Hilbert(WatchScene):
    def construct(self):
        self.card()
        self.program()
        self.godel()
        self.asymmetry()

    def card(self):
        self.chapter(3, r"Hilbert's question", r"Could a machine settle every question in mathematics?", lit=(1879, 1900, 1928, 1931), part=PART, said="Chapter three. Hilbert's question.")



    # ------------------------------------------------------------------
    def program(self):
        head = label(r"Hilbert's program \ (1920s)", font_size=42).to_edge(UP, buff=0.4)
        wishes = [
            (r"complete", r"every true statement \\ can be proved", YES),
            (r"consistent", r"no contradiction \\ can be proved", DATA),
            (r"decidable", r"a mechanical procedure \\ decides truth", CTRL),
        ]
        cards = VGroup(*[definition_card(n, b, color=c, width=3.9, font_size=26, kind=r"wish") for n, b, c in wishes])
        cards.arrange(RIGHT, buff=0.35).move_to(UP * 0.9)
        dec = cards[2]
        box = RoundedRectangle(width=2.6, height=1.3, corner_radius=0.15, stroke_color=CTRL, stroke_width=3,
                               fill_color=CTRL, fill_opacity=0.08)
        box.move_to(DOWN * 2.0)
        qm = label(r"?", font_size=60, color=CTRL).move_to(box)
        inp = label(r"a formula of \\ first-order logic", font_size=26, color=DATA).next_to(box, LEFT, buff=1.0)
        out = VGroup(label(r"valid", font_size=28, color=YES), label(r"not valid", font_size=28, color=NO)).arrange(
            DOWN, buff=0.35).next_to(box, RIGHT, buff=1.0)
        arr = VGroup(Arrow(inp.get_right(), box.get_left(), buff=0.12, color=GREY_C),
                     *[Arrow(box.get_right(), o.get_left(), buff=0.12, color=GREY_C) for o in out])
        name = note(r"Hilbert and Ackermann, \textit{Grundz\"uge der theoretischen Logik} (1928)", font_size=22)
        name.to_corner(DR, buff=0.3)
        with self.voiceover(
            "In the 1920s David Hilbert, the most influential mathematician of his time, set out a programme to put "
            "all of mathematics on such foundations. He wanted three things. <bookmark mark='a'/> Completeness: every "
            "true statement can be proved. <bookmark mark='b'/> Consistency: no contradiction can be proved. "
            "<bookmark mark='c'/> And decidability: a mechanical procedure that, given any statement, decides whether "
            "it can be proved. <bookmark mark='d'/> In his 1928 textbook with Wilhelm Ackermann the third wish became a "
            "precise problem: give a procedure that takes any formula of first-order logic and decides, in finitely many "
            "steps, whether it is valid. They called it the main problem of mathematical logic."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(box), FadeIn(qm), FadeIn(inp), FadeIn(out), *[GrowArrow(a) for a in arr], FadeIn(name),
                      Indicate(dec, color=CTRL, scale_factor=1.04))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def godel(self):
        h1 = history_card(r"7 Sept 1930", r"Kurt G\"odel, \ aged 24, \ K\"onigsberg",
                          r"announces, in a discussion at the end of a conference, that arithmetic contains true "
                          r"statements it cannot prove", width=6.2, font_size=23).to_corner(UL, buff=0.35)
        h2 = history_card(r"8 Sept 1930", r"David Hilbert, \ the same city, \ on the radio",
                          r"``\textit{Wir m\"ussen wissen. \ Wir werden wissen.}'' \ We must know. \ We will know.",
                          width=6.2, font_size=23).to_corner(UR, buff=0.35)
        g = RoundedRectangle(width=5.6, height=1.0, corner_radius=0.2, stroke_color=LIMIT, stroke_width=3,
                             fill_color=LIMIT, fill_opacity=0.1).move_to(DOWN * 1.0)
        gt = label(r"$G$: \ ``this statement has no proof''", font_size=32).move_to(g)
        loop = CurvedArrow(g.get_right() + LEFT * 0.4 + UP * 0.5, g.get_left() + RIGHT * 0.6 + UP * 0.5, angle=PI / 2.2,
                           color=LIMIT, stroke_width=3)
        cases = VGroup(
            label(r"if $G$ had a proof, \ it would be false: \ the system proves a falsehood", font_size=26, color=NO),
            label(r"so (if the system is consistent) \ $G$ has no proof, \ which is what it says: \ true", font_size=26,
                  color=YES),
        ).arrange(DOWN, buff=0.25).next_to(g, DOWN, buff=0.4)
        payoff = note(r"made precise, \ with Turing's machines, \ in Part 25", font_size=22).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The first two wishes did not survive long, and the timing was cruel. <bookmark mark='a'/> On the seventh of "
            "September 1930, at a conference in Königsberg, a twenty-four-year-old Kurt Gödel announced that arithmetic "
            "contains true statements it cannot prove. <bookmark mark='b'/> The next day, in the same city, Hilbert "
            "gave a radio address that ended: we must know, we will know. <bookmark mark='c'/> Gödel's idea, in one "
            "picture: he built, inside arithmetic, a statement G that says of itself, I have no proof. "
            "<bookmark mark='d'/> If G had a proof, it would be false, and the system would prove something false. "
            "So, if the system is consistent, G has no proof, which is exactly what it says. G is true and unprovable. "
            "Completeness is impossible. We will prove this properly in Part 25, using what this part builds."
        ) as vo:
            self.play(FadeIn(h1, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(h2, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(g), Write(gt), Create(loop))
            vo.wait_until("d")
            self.play(FadeIn(cases[0]))
            self.play(FadeIn(cases[1]), FadeIn(payoff))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def asymmetry(self):
        self.ask(r"To prove that \textit{no} procedure decides a problem, \\ what must you do first?",
                 [r"try every procedure", r"define exactly what a procedure is", r"find one formula it gets wrong"], 1,
                 say="Proving that a procedure exists is easy: write it down. To prove that none exists, what must you do "
                     "first?",
                 reveal="Define, exactly, what a procedure is. That is what Church and Turing did.")
        head = label(r"The decision problem was still open", font_size=40).to_edge(UP, buff=0.4)
        left = VGroup(label(r"to show a procedure \textbf{exists}:", font_size=30, color=YES),
                      label(r"write one down, \\ and check that it works", font_size=28, color=GREY_A)).arrange(
            DOWN, buff=0.25)
        right = VGroup(label(r"to show \textbf{no} procedure exists:", font_size=30, color=NO),
                       label(r"say exactly what \textit{every} procedure is, \\ and rule them all out", font_size=28,
                             color=GREY_A)).arrange(DOWN, buff=0.25)
        left.move_to([-3.5, 0.9, 0])
        right.move_to([3.4, 0.9, 0])
        bar = Line(UP * 2.0, DOWN * 0.3, color=GREY_D)
        hs = VGroup(
            history_card(r"April 1936", r"Alonzo Church", r"answers with the $\lambda$-calculus: \ no", width=5.6,
                         font_size=24),
            history_card(r"May 1936", r"Alan Turing", r"answers with machines: \ no", width=5.6, font_size=24),
        ).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Gödel had not answered the third question, the decision problem, and there was a reason it was hard. "
            "<bookmark mark='a'/> To show that a procedure exists, you write one down and check it works. "
            "<bookmark mark='b'/> To show that none exists, you must say exactly what counts as a procedure, every "
            "possible procedure, and then rule them all out. Nobody had a definition of a mechanical procedure. "
            "<bookmark mark='c'/> In 1936, within weeks of each other, two people supplied one. In Princeton, Alonzo "
            "Church, with a calculus of functions. In Cambridge, Alan Turing, with a machine. Both answered Hilbert: no. "
            "We start with Turing's, because his definition is the one you can build."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(Create(bar), FadeIn(right))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.2) for h in hs], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()
