from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403


class Canonical(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Completeness by canonical models", r"Does every valid formula have a proof?",
                            lit=(1959,), part=PART)
        with self.voiceover("Chapter six. Completeness by canonical models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.goal()
        self.build()
        self.canonicity()

    def goal(self):
        two = VGroup(VGroup(MathTex(r"\mathsf{K} \vdash \varphi", font_size=50, color=P.CLAIM),
                            label(r"provable from K's axiom and rules", font_size=24, color=GREY_A)).arrange(DOWN,
                                                                                                         buff=0.2),
                     VGroup(MathTex(r"\models \varphi", font_size=50, color=P.AGENT),
                            label(r"valid on every frame", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.2))
        two.arrange(RIGHT, buff=2.4).move_to([0, 1.0, 0])
        eq = MathTex(r"\Longleftrightarrow", font_size=56, color=GOAL).move_to(
            (two[0][0].get_center() + two[1][0].get_center()) / 2)
        plan = label(r"as in Part 3: \ build a model out of the logic itself", font_size=28, color=GOAL).to_edge(
            DOWN, buff=1.0)
        with self.voiceover(
            "As in Parts 2 and 3, we want proof and truth to agree. <bookmark mark='a'/>On one side, the theorems of "
            "K, derived from its axiom and its rules. <bookmark mark='b'/>On the other, the formulas valid on every "
            "frame. <bookmark mark='c'/>Soundness is easy: K's axiom is valid on every frame, and the rules preserve "
            "validity. For completeness, we use Henkin's idea from Part 3 once more: build the model out of the "
            "logic itself."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(two[0]))
            vo.wait_until("b")
            self.play(FadeIn(two[1]))
            vo.wait_until("c")
            self.play(Write(eq), FadeIn(plan))
        self.clear_scene()

    def build(self):
        def mcs(center, items, color):
            box = RoundedRectangle(width=3.0, height=1.9, corner_radius=0.2, stroke_color=color, stroke_width=2.5)
            t = VGroup(*[MathTex(x, font_size=26) for x in items]).arrange(DOWN, buff=0.08)
            return VGroup(box, t.move_to(box)).move_to(center)

        w = mcs([-3.8, 0.6, 0], [r"\Box p,\ \Box(p \to q)", r"\Diamond r,\ \lnot q", r"\dots"], WORLD)
        v1 = mcs([2.6, 1.7, 0], [r"p,\ p \to q,\ q", r"r", r"\dots"], WORLD)
        v2 = mcs([2.6, -1.0, 0], [r"p,\ p \to q,\ q", r"\lnot r", r"\dots"], WORLD)
        a1 = Arrow(w.get_right(), v1.get_left(), buff=0.1, color=ACC)
        a2 = Arrow(w.get_right(), v2.get_left(), buff=0.1, color=ACC)
        cap = VGroup(
            label(r"worlds: \ maximal consistent sets of formulas \ (Lindenbaum, Part 2)", font_size=24),
            label(r"$w R v$ \ iff \ every $\varphi$ with $\Box\varphi \in w$ \ is in $v$", font_size=24, color=ACC),
            label(r"truth lemma: \ $w \models \varphi$ \ iff \ $\varphi \in w$; \ the key step: if $\Diamond r \in w$, "
                  r"some $v$ with $r$ exists", font_size=22, color=GOAL)).arrange(DOWN, aligned_edge=LEFT,
                                                                                buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is the canonical model. <bookmark mark='a'/>Its worlds are the maximal consistent sets of "
            "formulas: sets that decide every formula, one way or the other, without contradiction, built by "
            "Lindenbaum's construction from Part 2. <bookmark mark='b'/>One world sees another when everything the "
            "first says is necessary is true in the second. If w contains 'necessarily p' and 'necessarily, if p then "
            "q', then every world w sees contains p and 'if p then q', and so q. <bookmark mark='c'/>The truth lemma "
            "says that a formula is true at a world exactly when it belongs to it. The key step is the diamond: if w "
            "says 'possibly r', there really is a visible world containing r. With the truth lemma, any formula K "
            "cannot prove is false somewhere in the canonical model, so it is not valid."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(w), FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(v1), FadeIn(v2), FadeIn(cap[1]))
            vo.wait_until("c")
            self.play(FadeIn(cap[2]))
        self.clear_scene()

    def canonicity(self):
        head = label(r"Canonicity: \ the axiom shapes the canonical frame", font_size=32, color=CONN).to_edge(UP,
                                                                                                         buff=0.5)
        rows = VGroup(
            VGroup(label(r"T in every world:", font_size=26, color=GOAL),
                   label(r"$\Box\varphi \in w$ implies $\varphi \in w$, \ so $wRw$: \ the frame is reflexive",
                         font_size=24)),
            VGroup(label(r"4 in every world:", font_size=26, color=GOAL),
                   label(r"the frame is transitive", font_size=24)),
            VGroup(label(r"so:", font_size=26, color=GOAL),
                   label(r"S4 is complete for reflexive transitive frames; \ S5 for equivalence relations",
                         font_size=24, color=OK))).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        for r in rows:
            r.arrange(RIGHT, buff=0.4)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        rows.next_to(head, DOWN, buff=0.6)
        gl = label(r"but GL is not canonical: \ its canonical frame has infinite chains; \ completeness needs finite "
                   r"models (Segerberg 1971)", font_size=22, color=BAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The same model proves completeness for the stronger logics too, when the axioms shape the canonical "
            "frame. <bookmark mark='a'/>If every world contains all instances of T, then whatever a world says is "
            "necessary, it contains, so it sees itself: the canonical frame is reflexive. <bookmark mark='b'/>With "
            "four, it is transitive. <bookmark mark='c'/>So S4 is complete for reflexive transitive frames, and S5 "
            "for equivalence relations. Axioms with this property are called canonical, and every Sahlqvist axiom "
            "is one. <bookmark mark='d'/>Löb's axiom is not: the canonical frame of GL has infinite chains, and its "
            "completeness had to be proved with finite models instead."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(gl))
        self.clear_scene()
