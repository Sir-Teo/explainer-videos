from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403


class Hoare(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Programs as modalities", r"Can a program be proved correct?", lit=(1969,),
                            part=PART)
        with self.voiceover("Chapter fourteen. Programs as modalities."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.triples()
        self.loop()
        self.dynamic()

    def triples(self):
        hcs = VGroup(history_card(1967, r"Robert Floyd", r"assertions on flowcharts", width=4.4, color=HIST,
                                  font_size=20),
                     history_card(1969, r"Tony Hoare", r"`An axiomatic basis for computer programming'", width=5.4,
                                  color=HIST, font_size=20)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        tri = VGroup(MathTex(r"\{P\}", r"\ C\ ", r"\{Q\}", font_size=56),
                     label(r"if $P$ holds before $C$ runs, \ then $Q$ holds after, \ if $C$ finishes", font_size=26,
                           color=GREY_A)).arrange(DOWN, buff=0.3).move_to([0, 0.6, 0])
        tri[0][0].set_color(P.CLAIM)
        tri[0][2].set_color(GOAL)
        rules = VGroup(
            MathTex(r"\{Q[e/x]\}\ x := e\ \{Q\}", font_size=32),
            MathTex(r"\frac{\{P\}\,C_1\,\{R\} \quad \{R\}\,C_2\,\{Q\}}{\{P\}\,C_1; C_2\,\{Q\}}", font_size=32),
            MathTex(r"\frac{\{I \land b\}\,C\,\{I\}}{\{I\}\ \textbf{while } b \textbf{ do } C\ \{I \land \lnot b\}}",
                    font_size=32)).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.6)
        rl = VGroup(*[label(t, font_size=20, color=GREY_A).next_to(r, UP, buff=0.15) for t, r in zip(
            (r"assignment", r"sequence", r"loop, with invariant $I$"), rules)])
        with self.voiceover(
            "Temporal logic checks what a program does over time. Program logic proves what it computes. "
            "<bookmark mark='a'/>Robert Floyd in 1967 and Tony Hoare in 1969 proposed triples: P, then a command C, "
            "then Q, meaning that if P is true before C runs, then Q is true afterwards, if C finishes. "
            "<bookmark mark='b'/>Each kind of command has a rule. An assignment: Q holds after x gets e if Q with e "
            "for x held before. A sequence: chain the middle condition. <bookmark mark='c'/>And a loop: find an "
            "invariant, a condition the body preserves. Then it still holds when the loop stops, together with the "
            "negation of the loop's test."
        ) as vo:
            self.play(FadeIn(hcs), Write(tri[0]), FadeIn(tri[1]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rules[0]), FadeIn(rl[0]), FadeIn(rules[1]), FadeIn(rl[1]))
            vo.wait_until("c")
            self.play(FadeIn(rules[2]), FadeIn(rl[2]))
        self.clear_scene()

    def loop(self):
        d = load("hoare")
        prog = VGroup(MathTex(r"\{n \geq 0\}", font_size=34, color=P.CLAIM),
                      MathTex(r"i := 0;\ s := 0;", font_size=34),
                      MathTex(r"\textbf{while } i < n \textbf{ do } (i := i + 1;\ s := s + i)", font_size=34),
                      MathTex(r"\{s = n(n+1)/2\}", font_size=34, color=GOAL)).arrange(DOWN, aligned_edge=LEFT,
                                                                                     buff=0.2)
        prog.move_to([-2.6, 1.2, 0])
        inv = VGroup(label(r"invariant:", font_size=26, color=OK),
                     MathTex(r"I:\ \ s = i(i+1)/2 \ \land\ i \leq n", font_size=36, color=OK)).arrange(RIGHT, buff=0.3)
        inv.next_to(prog, DOWN, buff=0.6).align_to(prog, LEFT)
        steps = VGroup(label(r"holds at the start: \ $0 = 0$", font_size=24),
                       label(r"preserved: \ $s + (i+1) = (i+1)(i+2)/2$", font_size=24),
                       label(r"at exit, $i = n$: \ so $s = n(n+1)/2$", font_size=24, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(inv, DOWN, buff=0.35).align_to(inv, LEFT)
        chk = label(rf"the Reasoner: \ the invariant checked at all {d['checks']} loop points for $n = 0, \dots, "
                    rf"{d['n_max']}$ \ $\checkmark$", font_size=22, color=OK).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is a small proof. <bookmark mark='a'/>Starting with n at least zero, this loop adds the numbers "
            "from one to n. Afterwards s should be n times n plus one over two. <bookmark mark='b'/>The invariant: "
            "s equals i times i plus one over two, and i is at most n. <bookmark mark='c'/>It holds at the start, "
            "when both are zero. Each pass of the body preserves it, by a line of algebra. And when the loop stops, "
            "i equals n, so s has the right value. <bookmark mark='d'/>A proof covers every n at once. As a sanity "
            f"check, the Reasoner ran the loop for n up to {d['n_max']} and tested the invariant at all {d['checks']} "
            "points where it should hold."
        ) as vo:
            self.play(FadeIn(prog))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(inv))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.15) for s_ in steps], lag_ratio=0.5), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(chk))
        self.clear_scene()

    def dynamic(self):
        hc = history_card(1976, r"Vaughan Pratt", r"dynamic logic: \ a box for every program", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            VGroup(MathTex(r"[\alpha]\,\varphi", font_size=44, color=GOAL),
                   label(r"after every run of $\alpha$ that ends, $\varphi$", font_size=26)),
            VGroup(MathTex(r"\langle\alpha\rangle\,\varphi", font_size=44, color=GOAL),
                   label(r"some run of $\alpha$ ends with $\varphi$", font_size=26)),
            VGroup(MathTex(r"\{P\}\,\alpha\,\{Q\} \ \equiv\ P \to [\alpha]\,Q", font_size=40, color=OK),
                   label(r"Hoare's triples are modal formulas", font_size=26))).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.4)
        for r in rows:
            r.arrange(RIGHT, buff=0.5)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        rows.move_to([0.3, -0.4, 0])
        ax = label(r"$[\alpha;\beta]\varphi \leftrightarrow [\alpha][\beta]\varphi$, \quad "
                   r"$[\alpha \cup \beta]\varphi \leftrightarrow [\alpha]\varphi \land [\beta]\varphi$, \quad "
                   r"$[\alpha^*]\varphi \leftrightarrow \varphi \land [\alpha][\alpha^*]\varphi$", font_size=24,
                   color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 1976 Vaughan Pratt saw that this, too, is modal logic. <bookmark mark='a'/>Give each program alpha "
            "its own box: box alpha phi means that after every run of alpha that ends, phi holds. "
            "<bookmark mark='b'/>And diamond alpha phi: some run of alpha ends with phi. The worlds are states of "
            "the machine, and the arrows are runs of programs. <bookmark mark='c'/>A Hoare triple is just the modal "
            "formula 'if P, then box alpha Q'. <bookmark mark='d'/>The laws of programs become modal axioms: doing "
            "alpha then beta is a box inside a box; choosing alpha or beta is a conjunction of boxes; repeating alpha "
            "is a fixed point, like the ones in the model checker."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(ax))
        self.clear_scene()
