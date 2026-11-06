from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class KK(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Knowing that you know", r"If you know, do you know that you know?", lit=(1962,),
                            part=PART)
        with self.voiceover("Chapter ten. Knowing that you know."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.principle()
        self.clock_()

    def principle(self):
        head = label(r"The KK principle", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        f = MathTex(r"K p \;\rightarrow\; K K p", font_size=48, color=GOAL).next_to(head, DOWN, buff=0.4)
        rows = VGroup(
            label(r"Hintikka, \textit{Knowledge and Belief} (1962): \ knowledge as $\Box$ over the worlds you cannot "
                  r"rule out", font_size=23),
            label(r"KK is the axiom 4: \ $\Box p \rightarrow \Box\Box p$, \ true on every \textit{transitive} frame "
                  r"\ (Part 4)", font_size=23, color=BEL),
            label(r"its appeal: \ knowing seems transparent; \ if you know, \ reflection should tell you so",
                  font_size=23, color=GREY_A),
            label(r"but margins for error make the relation of `cannot tell apart' \ \textit{not} transitive",
                  font_size=24, color=LUCK)).arrange(DOWN, buff=0.35).move_to([0, -0.6, 0])
        with self.voiceover(
            "A margin for error has a second consequence. <bookmark mark='a'/>The KK principle says: if you know p, "
            "you know that you know p. <bookmark mark='b'/>Jaakko Hintikka, who founded epistemic logic in 1962, "
            "treated knowledge as a box: S knows p when p holds in every world S cannot rule out. "
            "<bookmark mark='c'/>Then KK is the modal axiom four, which we met in Part 4, and which holds on exactly "
            "the frames whose relation is transitive. <bookmark mark='d'/>KK is attractive: knowing seems "
            "transparent, so if you know, reflection ought to reveal it. <bookmark mark='e'/>But with a margin for "
            "error, the relation of being unable to tell two situations apart is not transitive. I cannot tell "
            "twenty from twenty-one, nor twenty-one from twenty-two, but I can tell twenty from twenty-two."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def clock_(self):
        d = load("kk")
        n, b = d["n"], d["bound"]
        sets = [set(s) for s in d["sets"]]
        head = label(r"The unmarked clock", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        nl = NumberLine(x_range=[0, n, 5], length=12.0, include_numbers=True, font_size=22, color=GREY_B).move_to(
            [0, 1.4, 0])
        hand = Arrow(nl.n2p(19) + UP * 0.9, nl.n2p(19) + UP * 0.1, buff=0, color=WHITE, stroke_width=4)
        hl = label(r"the hand, \ really at 19", font_size=20, color=WHITE).next_to(hand, UP, buff=0.1)
        names = [r"$p$: \ the hand is at most 20", r"$Kp$", r"$KKp$", r"$KKKp$"]
        cols = [OK, KNOW, BEL, SKEP]
        bars, labs = VGroup(), VGroup()
        for i, (s, nm, c) in enumerate(zip(sets, names, cols)):
            y = 0.3 - 0.75 * i
            hi = max(s)
            bar = Line(nl.n2p(0) + UP * (y - 1.4), nl.n2p(hi) + UP * (y - 1.4), color=c, stroke_width=10)
            end = label(rf"$\le {hi}$", font_size=20, color=c).next_to(bar, RIGHT, buff=0.15)
            lab = label(nm, font_size=21, color=c).next_to(bar, LEFT, buff=0.2)
            if lab.get_left()[0] < -7.0:
                lab.next_to(bar.get_start(), UP, buff=0.08).align_to(bar, LEFT)
            bars.add(VGroup(bar, end))
            labs.add(lab)
        for lab in labs:
            if lab.get_left()[0] < -6.9:
                lab.shift(RIGHT * (-6.9 - lab.get_left()[0]))
        assert 19 in sets[1] and 19 not in sets[2]
        rows = VGroup(label(r"I see the hand only to within one mark: \ I know $p$ \ iff \ $p$ holds 1 mark either "
                            r"side", font_size=22, color=JUST),
                      label(r"at 19: \ I know the hand is at most 20, \ but I don't know that I know it",
                            font_size=24, color=GOAL),
                      label(r"each $K$ strips one mark from the edge: \ knowledge without KK, \ everywhere near a "
                            r"boundary", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN,
                                                                                                    buff=0.25)
        with self.voiceover(
            "Williamson's example is a clock with no numbers on its face. <bookmark mark='a'/>Its hand can point "
            "to any of thirty-one marks, and from where I stand I can see where it points only to within one mark "
            "either way. <bookmark mark='b'/>Let p be: the hand points at mark twenty or below. <bookmark mark='c'/>"
            "I know p at a position just when p is true at every position I cannot rule out: one mark either side. "
            "So I know p when the hand is at nineteen or below. <bookmark mark='d'/>Knowing that I know p requires "
            "knowing p at every position I cannot rule out, so the hand must be at eighteen or below. And knowing "
            "that I know that I know, at seventeen or below. <bookmark mark='e'/>The hand is really at nineteen. I "
            "know that it points at twenty or below. But I do not know that I know it. Each K strips one mark from "
            "the edge, and near any boundary, knowledge comes without knowledge of itself. KK fails."
        ) as vo:
            self.play(FadeIn(head), Create(nl))
            vo.wait_until("a")
            self.play(GrowArrow(hand), FadeIn(hl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(bars[0][0]), FadeIn(bars[0][1]), FadeIn(labs[0]))
            vo.wait_until("c")
            self.play(Create(bars[1][0]), FadeIn(bars[1][1]), FadeIn(labs[1]))
            vo.wait_until("d")
            self.play(Create(bars[2][0]), FadeIn(bars[2][1]), FadeIn(labs[2]))
            self.play(Create(bars[3][0]), FadeIn(bars[3][1]), FadeIn(labs[3]))
            vo.wait_until("e")
            line = DashedLine(nl.n2p(19) + UP * 0.1, nl.n2p(19) + DOWN * 2.05, color=WHITE, stroke_width=2)
            self.play(Create(line), FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
        self.clear_scene()
