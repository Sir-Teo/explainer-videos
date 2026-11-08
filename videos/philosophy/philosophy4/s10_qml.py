from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403


class QML(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Quantifiers and modality", r"Could there have been things that do not exist?",
                            lit=(1946,), part=PART)
        with self.voiceover("Chapter nine. Quantifiers and modality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.barcan()
        self.domains()
        self.quine()
        self.identity()

    def barcan(self):
        hc = history_card(1946, r"Ruth Barcan Marcus", r"the first systems of quantified modal logic", width=6.2,
                          color=HIST).to_corner(UL, buff=0.35)
        bf = VGroup(MathTex(r"\Diamond \exists x\, \varphi(x) \to \exists x\, \Diamond \varphi(x)", font_size=44,
                            color=GOAL),
                    label(r"the Barcan formula: \ if there could have been a $\varphi$, \ there is something that could "
                          r"have been $\varphi$", font_size=24, color=GREY_A),
                    MathTex(r"\forall x\, \Box \varphi(x) \to \Box \forall x\, \varphi(x)", font_size=40),
                    label(r"equivalently", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.25).move_to([0, -0.4, 0])
        bf[2].shift(DOWN * 0.45)
        bf[3].move_to((bf[1].get_bottom() + bf[2].get_top()) / 2)
        ex = label(r"`there could have been a child of Wittgenstein' \ $\Rightarrow$ \ something exists that could have "
                   r"been his child?", font_size=24, color=BAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now add quantifiers. <bookmark mark='a'/>Ruth Barcan Marcus built the first quantified modal logics in "
            "1946 and 1947, and one formula still carries her name. <bookmark mark='b'/>If there could have been "
            "something with a property, then there is something that could have had it. <bookmark mark='c'/>It "
            "sounds harmless until you try an example. There could have been a child of Wittgenstein, who had none. "
            "Does it follow that something actually exists that could have been his child? A merely possible child, "
            "existing already?"
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Indicate(hc, color=HIST, scale_factor=1.03))
            vo.wait_until("b")
            self.play(Write(bf[0]), FadeIn(bf[1]))
            self.play(FadeIn(bf[3]), FadeIn(bf[2]))
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.clear_scene()

    def domains(self):
        d = load("barcan")
        w0 = VGroup(Circle(radius=1.0, stroke_color=WORLD, stroke_width=3),
                    MathTex(r"w_0", font_size=26, color=GREY_A)).move_to([-3.0, 0.2, 0])
        w0[1].next_to(w0[0], DOWN, buff=0.15)
        w1 = VGroup(Circle(radius=1.3, stroke_color=WORLD, stroke_width=3),
                    MathTex(r"w_1", font_size=26, color=GREY_A)).move_to([2.6, 0.2, 0])
        w1[1].next_to(w1[0], DOWN, buff=0.15)
        ar = Arrow(w0[0].get_right(), w1[0].get_left(), buff=0.1, color=ACC)
        a0 = VGroup(Dot(color=WORLD), MathTex("a", font_size=28)).arrange(
            RIGHT, buff=0.1).move_to(w0[0])
        a1 = VGroup(Dot(color=WORLD), MathTex("a", font_size=28), MathTex(r"\,F", font_size=24, color=OK)).arrange(
            RIGHT, buff=0.1).move_to(w1[0].get_center() + UP * 0.4)
        b1 = VGroup(Dot(color=BAD), MathTex("b", font_size=28), MathTex(r"\,\lnot F", font_size=24, color=BAD)).arrange(
            RIGHT, buff=0.1).move_to(w1[0].get_center() + DOWN * 0.4)
        g = d["growing"]
        ev = VGroup(
            label(r"$\forall x\, \Box F(x)$ at $w_0$: \ the only thing there, $a$, is $F$ in every visible world",
                  font_size=24, color=OK if g["antecedent"] else BAD),
            label(r"$\Box \forall x\, F(x)$ at $w_0$: \ fails, \ $w_1$ has a new thing $b$ that is not $F$",
                  font_size=24, color=OK if g["consequent"] else BAD)).arrange(DOWN, aligned_edge=LEFT,
                                                                             buff=0.2).to_edge(DOWN, buff=0.9)
        moral = label(r"constant domains: \ the Barcan formula is valid; \ growing domains: \ it fails", font_size=24,
                      color=GOAL).to_edge(DOWN, buff=0.35)
        assert d["constant"]["antecedent"] and d["constant"]["consequent"] and not g["consequent"]
        with self.voiceover(
            "In Kripke's semantics for quantified modal logic, each world has its own domain of things. "
            "<bookmark mark='a'/>Here world zero contains one thing, a, and it sees world one, which contains a and "
            "a newcomer, b. <bookmark mark='b'/>Let F be true of a at world one, but not of b. <bookmark mark='c'/>"
            "Then at world zero, everything is necessarily F: the only thing there is a. But it is not necessary that "
            "everything is F, because world one has something that is not. <bookmark mark='d'/>So the Barcan formula "
            "holds when every world has the same domain, and fails when domains can grow. Accepting it means believing "
            "in a fixed stock of possible things: necessitism, as Timothy Williamson defends it."
        ) as vo:
            self.play(Create(w0[0]), FadeIn(w0[1]), Create(w1[0]), FadeIn(w1[1]), GrowArrow(ar), FadeIn(a0),
                      FadeIn(a1[:2]), FadeIn(b1[:2]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(a1[2]), FadeIn(b1[2]))
            vo.wait_until("c")
            self.play(FadeIn(ev))
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()

    def quine(self):
        hc = history_card(1953, r"W.\ V.\ Quine", r"`Reference and Modality': \ quantifying into modal contexts is "
                          r"confused", width=6.6, color=HIST).to_corner(UL, buff=0.35)
        arg = VGroup(MathTex(r"\Box (9 > 7)", font_size=40, color=OK),
                     MathTex(r"9 = \text{the number of planets}", font_size=36),
                     MathTex(r"\Box (\text{the number of planets} > 7)\ ?", font_size=40, color=BAD)).arrange(
            DOWN, buff=0.3).move_to([0, -0.2, 0])
        bar = Line(LEFT * 3.2, RIGHT * 3.2, color=GREY_B).next_to(arg[1], DOWN, buff=0.15)
        fix = VGroup(label(r"\textit{de dicto}: \ necessarily, the number of planets exceeds 7 \ (false)",
                           font_size=24),
                     label(r"\textit{de re}: \ the number of planets is such that, necessarily, it exceeds 7 \ (true)",
                           font_size=24, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN,
                                                                                                    buff=0.45)
        with self.voiceover(
            "Quine thought the whole project was confused. <bookmark mark='a'/>Necessarily, nine is greater than "
            "seven. In 1953 there were nine known planets, so nine was the number of planets. Substitute equals for "
            "equals, and you get: necessarily, the number of planets is greater than seven, which is false, since "
            "there could have been five. <bookmark mark='b'/>The answer, made precise by Russell's scope distinctions "
            "from Part 3, separates two readings. De dicto: necessarily, whatever number the planets have exceeds "
            "seven: false. De re: the thing that is in fact the number of planets, namely nine, necessarily exceeds "
            "seven: true. Quine's further worry, that de re necessity commits us to essences, is the subject of "
            "Part 22."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(arg[0]), FadeIn(arg[1]), Create(bar))
            self.play(FadeIn(arg[2]))
            vo.wait_until("b")
            self.play(FadeIn(fix))
        self.clear_scene()

    def identity(self):
        steps = VGroup(MathTex(r"a = b", font_size=40),
                       MathTex(r"\Box (a = a)", font_size=40, color=OK),
                       MathTex(r"\therefore\ \Box (a = b)", font_size=44, color=GOAL)).arrange(DOWN, buff=0.3).move_to(
            [-3.0, 0.4, 0])
        sl = label(r"substitute $b$ for the second $a$ \ (Barcan 1947)", font_size=22, color=GREY_A).next_to(
            steps, DOWN, buff=0.3)
        hp = VGroup(label(r"Hesperus $=$ Phosphorus", font_size=30, color=GOAL),
                    label(r"discovered by astronomy, \ yet necessary?", font_size=24, color=GREY_A),
                    VGroup(label(r"Kripke (1971): \ names are rigid designators,", font_size=24, color=OK),
                           label(r"so there are necessary truths known \textit{a posteriori}", font_size=24,
                                 color=OK)).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.25).move_to([3.1, 0.2, 0])
        fwd = label(r"Part 22, \textit{Possible Worlds}: \ rigid designation, essence, and what worlds are",
                    font_size=24, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "One more theorem with philosophical teeth. <bookmark mark='a'/>Suppose a is b. Everything is necessarily "
            "identical to itself, so necessarily a is a. Substitute b for the second a, and you get: necessarily a "
            "is b. Marcus proved it in 1947: identities, if true, are necessary. <bookmark mark='b'/>But Hesperus, "
            "the evening star, turned out to be Phosphorus, the morning star: a discovery of astronomy. How can it be "
            "necessary? <bookmark mark='c'/>Kripke's answer in 1971 was that names are rigid: they pick out the same "
            "thing in every world, so the identity is necessary, though we learn it by observation. Necessary truths "
            "known a posteriori: a central idea of Part 22."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(s_, shift=DOWN * 0.15) for s_ in steps], lag_ratio=0.4), FadeIn(sl))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(hp[:2]))
            vo.wait_until("c")
            self.play(FadeIn(hp[2]), FadeIn(fwd))
        self.clear_scene()
