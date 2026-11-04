from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import CODE, CTRL, DATA, HEAD, HIST, LIMIT, NO, PART, YES


class Hilbert(VoiceoverScene):
    def construct(self):
        self.card()
        self.leibniz()
        self.frege()
        self.program()
        self.godel()
        self.asymmetry()

    def card(self):
        card = chapter_card(3, r"Hilbert's question", r"Could a machine settle every question in mathematics?",
                            lit=(1879, 1900, 1928, 1931), part=PART)
        with self.voiceover("Chapter three. Hilbert's question."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def leibniz(self):
        hc = history_card(r"c. 1685", r"Gottfried Wilhelm Leibniz",
                          r"dreams of a universal language of thought, \textit{characteristica universalis}, and a "
                          r"calculus of reasoning to go with it", width=6.6, font_size=24).to_corner(UL, buff=0.4)
        q = label(r"``If controversies were to arise, \\ there would be no more need of disputation \\ between two "
                  r"philosophers than between two accountants. \\ For it would suffice to take their pencils in their "
                  r"hands, \\ to sit down to their slates, \ and to say to each other: \\ \textit{Calculemus!} \ Let "
                  r"us calculate.''", font_size=28).move_to([1.4, -1.0, 0])
        with self.voiceover(
            "The dream is older than any machine. <bookmark mark='a'/> Around 1685 Gottfried Leibniz imagined a "
            "language in which every idea could be written exactly, and a calculus for reasoning in it. "
            "<bookmark mark='b'/> If philosophers disagreed, he wrote, they would not argue. They would sit down with "
            "their slates and say: let us calculate."
        ) as vo:
            calc = label(r"\textit{Calculemus!}", font_size=80, color=C.CS_HEAD).move_to(DOWN * 0.6)
            self.play(FadeIn(hc, shift=RIGHT * 0.2), FadeIn(calc, scale=0.9))
            vo.wait_until("b")
            self.play(FadeOut(calc), FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frege(self):
        hc = history_card(1879, r"Gottlob Frege, \ \textit{Begriffsschrift}",
                          r"the first complete formal language for logic: \ statements as strings, \ proofs as "
                          r"sequences of strings, \ each line following from earlier lines by fixed rules",
                          width=7.0, font_size=24).to_corner(UL, buff=0.4)
        lines = [
            (r"1.", r"\forall x\, (\mathrm{Man}(x) \to \mathrm{Mortal}(x))", r"premise"),
            (r"2.", r"\mathrm{Man}(\mathrm{Socrates})", r"premise"),
            (r"3.", r"\mathrm{Man}(\mathrm{Socrates}) \to \mathrm{Mortal}(\mathrm{Socrates})", r"from 1, \ instantiate $x$"),
            (r"4.", r"\mathrm{Mortal}(\mathrm{Socrates})", r"from 2 and 3, \ modus ponens"),
        ]
        rows = VGroup()
        for n, f, r in lines:
            rows.add(VGroup(MathTex(n, font_size=30, color=GREY_B), MathTex(f, font_size=32, color=DATA),
                            label(r, font_size=22, color=GREY_B)))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.3)
            r[2].next_to(r[1], RIGHT, buff=0.4)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([-0.4, -0.9, 0])
        for r in rows:
            r[2].set_x(5.4).align_to(r[1], DOWN)
        ticks = VGroup(*[MathTex(r"\checkmark", font_size=34, color=YES).next_to(r[0], LEFT, buff=0.25) for r in rows])
        cap = label(r"checking a proof is mechanical. \ Is \textit{finding} one?", font_size=32, color=HEAD)
        cap.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Two centuries later, logic became exact enough to try. <bookmark mark='a'/> In 1879 Gottlob Frege published "
            "the first complete formal language for logic. A statement is a string of symbols. A proof is a list of "
            "statements in which every line follows from earlier lines by a small set of fixed rules. "
            "<bookmark mark='b'/> All men are mortal; Socrates is a man; so, by instantiating the first premise and "
            "applying modus ponens, Socrates is mortal. <bookmark mark='c'/> Whether each line follows can be checked "
            "by rule, with no understanding: a clerk, or a machine, could check a proof. <bookmark mark='d'/> The "
            "question is whether a machine could also find one."
        ) as vo:
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.35), run_time=2.6)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t, scale=1.5) for t in ticks], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(cap, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

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
