from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403


class Hume(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Hume's problem", r"Can experience justify expectations?", lit=(1739, 1748),
                            part=PART)
        with self.voiceover("Chapter one. Hume's problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.argument()
        self.circle()
        self.living()
        self.responses()

    def argument(self):
        hc = history_card(1748, r"David Hume", r"\textit{An Enquiry concerning Human Understanding}, \ \S 4",
                          width=6.6, color=HIST).to_corner(UL, buff=0.35)
        inf = VGroup(label(r"observed: \ every emerald so far is green", font_size=24, color=PAST),
                     MathTex(r"\Downarrow \ ?", font_size=36),
                     label(r"so: \ the next emerald is green", font_size=24, color=FUT)).arrange(DOWN, buff=0.2)
        inf.next_to(hc, DOWN, buff=0.5).set_x(-3.0)
        need = label(r"needs: \ the future resembles the past \ (the uniformity principle)", font_size=22,
                     color=GOAL).next_to(inf, DOWN, buff=0.35).set_x(-3.0)
        fork = VGroup(
            VGroup(label(r"proved by reason?", font_size=23, color=A_C),
                   label(r"no: \ its denial is conceivable, \ so not a demonstration", font_size=20, color=GREY_A))
            .arrange(DOWN, buff=0.1),
            VGroup(label(r"learned from experience?", font_size=23, color=B_C),
                   label(r"only by an inference that already assumes it", font_size=20, color=GREY_A)).arrange(
                DOWN, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, -0.6, 0])
        with self.voiceover(
            "Hume's argument, from the Enquiry of 1748. <bookmark mark='a'/>We observe that every emerald so far has "
            "been green, and conclude that the next one will be. <bookmark mark='b'/>The step needs a premise: that "
            "the future will resemble the past. <bookmark mark='c'/>How could we know it? Not by reason alone: its "
            "denial is perfectly conceivable, so no demonstration can prove it. <bookmark mark='d'/>Not by "
            "experience: experience tells us only about the past, and to project it onto the future we must already "
            "assume the principle in question."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(inf))
            vo.wait_until("b")
            self.play(FadeIn(need))
            vo.wait_until("c")
            self.play(FadeIn(fork[0]))
            vo.wait_until("d")
            self.play(FadeIn(fork[1]))
        self.clear_scene()

    def circle(self):
        head = label(r"The circle", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        nodes = [label(t, font_size=22) for t in (r"induction has worked so far", r"so induction will keep working",
                                                  r"by induction")]
        pos = [np.array([0, 1.5, 0]), np.array([3.4, -1.3, 0]), np.array([-3.4, -1.3, 0])]
        for n, p in zip(nodes, pos):
            n.move_to(p)
        a0, a1, a2 = nodes
        arrows = VGroup(
            CurvedArrow(a0.get_right() + RIGHT * 0.15, a1.get_top() + UP * 0.15, angle=-PI / 3, color=PAST),
            CurvedArrow(a1.get_bottom() + DOWN * 0.15, a2.get_bottom() + DOWN * 0.15, angle=-PI / 3, color=PAST),
            CurvedArrow(a2.get_top() + UP * 0.15, a0.get_left() + LEFT * 0.15, angle=-PI / 3, color=PAST))
        foot = label(r"a justification of induction by induction \ assumes what it should prove", font_size=24,
                     color=BAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The tempting reply is circular. <bookmark mark='a'/>Induction has worked so far; <bookmark mark='b'/>so "
            "it will keep working; <bookmark mark='c'/>but that step is itself an induction. <bookmark mark='d'/>A "
            "justification of induction by induction assumes exactly what it was supposed to prove."
        ) as vo:
            self.play(FadeIn(head))
            for mk, n in zip("abc", nodes):
                vo.wait_until(mk)
                self.play(FadeIn(n))
                if mk != "a":
                    self.play(Create(arrows["bc".index(mk)]))
            self.play(Create(arrows[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def living(self):
        head = label(r"Living with the circle", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hume = stack([(r"Hume's own `sceptical solution': \ \textit{custom}", PAST),
                      (r"we expect because we are made to; \ an explanation, \ not a justification", GREY_A)],
                     font_size=22).next_to(head, DOWN, buff=0.3)
        hd = [r"", r"\text{the record}", r"\text{so, next time}"]
        rows = [[label(r"inductivist", font_size=21, color=OK), label(r"induction has mostly worked", font_size=20),
                 label(r"it will work \ (by induction)", font_size=20, color=OK)],
                [label(r"counterinductivist", font_size=21, color=BAD),
                 label(r"counterinduction has mostly failed", font_size=20),
                 label(r"it will work \ (by counterinduction)", font_size=20, color=BAD)]]
        grid = ValueGrid(hd, rows, col_w=[3.0, 4.6, 4.2], cell_h=0.62, font_size=22).next_to(hume, DOWN, buff=0.35)
        black = label(r"Black \ (1958): \ only \textit{rule}-circular, \ not premise-circular; \ Salmon: \ then so is "
                      r"its mirror image", font_size=20, color=GREY_A).next_to(grid, DOWN, buff=0.25)
        diss = stack([(r"Strawson \ (1952): \ `is induction reasonable?' \ is like \ `is the law legal?'", FUT),
                      (r"Goodman \ (1955): \ rules and inferences are justified together, \ by mutual adjustment",
                       FUT)], font_size=21).next_to(black, DOWN, buff=0.6)
        with self.voiceover(
            "How have philosophers lived with the circle? <bookmark mark='a'/>Hume's own answer was what he called "
            "a sceptical solution: custom. We expect the future to resemble the past because we are made that way. "
            "That explains our expectations; it does not justify them. <bookmark mark='b'/>Max Black argued that "
            "the inductive defence of induction is circular only in a harmless way: it does not assume its "
            "conclusion as a premise, it merely uses the rule it defends. <bookmark mark='c'/>Wesley Salmon's reply "
            "was a mirror. The counterinductivist predicts the opposite of the past. Counterinduction has mostly "
            "failed so far, so, by counterinduction, it will work next time. If rule-circularity is harmless, this "
            "argument is just as good. <bookmark mark='d'/>Peter Strawson tried to dissolve the question: asking "
            "whether induction is reasonable is like asking whether the law is legal, since being reasonable means, "
            "in part, proportioning belief to inductive evidence. <bookmark mark='e'/>And Goodman held that rules "
            "and particular inferences are justified together, each adjusted to the other: the method later called "
            "reflective equilibrium."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hume))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[1]], FadeIn(black))
            vo.wait_until("d")
            self.play(FadeIn(diss[0]))
            vo.wait_until("e")
            self.play(FadeIn(diss[1]))
        self.clear_scene()

    def responses(self):
        head = label(r"Six kinds of answer, \ all met in this part", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"probability", r"induction is probable, \ not certain: \ Laplace, \ Bayes", r"Ch.\ 2, 9"),
            (r"falsification", r"science never needs induction: \ Popper", r"Ch.\ 7"),
            (r"explanation", r"infer what would best explain the evidence", r"Ch.\ 8"),
            (r"learning theory", r"which methods converge to the truth, \ and fastest?", r"Ch.\ 10, 11"),
            (r"simplicity", r"a universal prior that favours short explanations", r"Ch.\ 12, 13"),
            (r"vindication", r"if any method works, \ this one does: \ Reichenbach", r"Ch.\ 15"),
        ]
        g = VGroup()
        for i, (a, b, c) in enumerate(rows):
            x = label(a, font_size=23, color=FUT)
            y = label(b, font_size=21)
            z = label(c, font_size=19, color=GREY_B)
            x.move_to([-6.2 + x.width / 2, 1.7 - i * 0.78, 0])
            y.move_to([-3.4 + y.width / 2, 1.7 - i * 0.78, 0])
            z.move_to([5.8, 1.7 - i * 0.78, 0])
            g.add(VGroup(x, y, z))
        foot = label(r"and the theorem behind the Wall: \ no method works in every possible world \ (Ch.\ 14)",
                     font_size=23, color=BAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Philosophers have given six kinds of answer, and this part meets each of them. <bookmark mark='a'/>Make "
            "induction probable rather than certain, with Laplace and Bayes. <bookmark mark='b'/>Do science without "
            "induction, with Popper. <bookmark mark='c'/>Infer whatever would best explain the evidence. "
            "<bookmark mark='d'/>Ask which methods are guaranteed to converge on the truth, and which do so most "
            "efficiently. <bookmark mark='e'/>Prefer simple explanations, made precise as a universal prior. "
            "<bookmark mark='f'/>Or argue, with Reichenbach, that if any method works, induction does. "
            "<bookmark mark='g'/>Behind all of them stands a theorem: no method of learning works in every possible "
            "world."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("g")
            self.play(FadeIn(foot))
        self.clear_scene()
