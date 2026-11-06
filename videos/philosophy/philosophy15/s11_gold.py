from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403


def guess_tex(g) -> str:
    if g == "N":
        return r"\mathbb{N}"
    return r"\{0..%d\}" % max(g) if len(g) > 1 else r"\{0\}"


class Gold(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Learning in the limit", r"What can be learned, \ even in principle?",
                            lit=(1963, 1967), part=PART)
        with self.voiceover("Chapter ten. Learning in the limit."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.intro()
        self.gold()
        self.putnam()
        self.hierarchy()

    def intro(self):
        head = label(r"A new question: \ not `is it justified?' \ but `does it get there?'", font_size=28,
                     color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"a learner sees data one item at a time, \ and after each item guesses", WHITE),
            (r"it \textit{identifies the truth in the limit} \ if, \ after some finite time, \ every guess is right",
             FUT),
            (r"it never has to know \textit{when} it has arrived", PAST),
            (r"Hilary Putnam \ (1965) \ and E.\ Mark Gold \ (1965, \ 1967): \ the same idea, \ the same year", GREY_A),
            (r"Hans Reichenbach's `posits' \ (Ch.\ 15) \ were its ancestor", GREY_A),
        ], font_size=24, buff=0.38, aligned_edge=LEFT).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "In the 1960s a new question replaced Hume's. Not: is induction justified? But: can a method be "
            "guaranteed to get to the truth? <bookmark mark='a'/>A learner sees data one item at a time, and after "
            "each item it guesses. <bookmark mark='b'/>It identifies the truth in the limit if, after some finite "
            "time, every guess it makes is right. <bookmark mark='c'/>It never has to know when it has arrived. "
            "That is the price of asking only for convergence. <bookmark mark='d'/>Hilary Putnam and Mark Gold "
            "introduced the idea independently in 1965. <bookmark mark='e'/>Its ancestor was Reichenbach's notion of "
            "a posit, which we meet in chapter fifteen."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def gold(self):
        d = load("gold")["gold"]
        hc = history_card(1967, r"E.\ Mark Gold", r"`Language Identification in the Limit'", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        cls = label(r"the class: \ every finite set of numbers, \ and $\mathbb{N}$ itself", font_size=23,
                    color=FUT).next_to(hc, DOWN, buff=0.3).set_x(0)
        n = 16
        cw = 0.8
        x0 = -cw * (n - 1) / 2
        data = VGroup()
        gs = VGroup()
        for k in range(n):
            x = x0 + k * cw
            rep = k > 0 and d["data"][k] == d["data"][k - 1]
            c = Square(side_length=cw - 0.06, stroke_color=GREY_C, stroke_width=1.5, fill_color=PAST if not rep
                       else GREY_D, fill_opacity=0.25).move_to([x, 0.4, 0])
            data.add(VGroup(c, MathTex(str(d["data"][k]), font_size=24).move_to(c)))
            g = d["guesses"][k]
            gs.add(MathTex(guess_tex(g), font_size=19 if g != "N" else 28, color=BAD if g == "N" else
                           GREY_A).move_to([x, -0.45, 0]))
        dl = label(r"data", font_size=19, color=PAST).next_to(data, LEFT, buff=0.15)
        gl = label(r"guess", font_size=19, color=GREY_A).next_to(gs, LEFT, buff=0.15)
        VGroup(data, gs, dl, gl).set_x(0.2)
        rules = stack([
            (r"the adversary: \ while the learner guesses finite, \ show a new number", PAST),
            (r"when it guesses $\mathbb{N}$, \ repeat an old one \ (grey) \ until it backs down", BAD),
            (r"this learner: \ " + str(d["mind_changes"]) + r" mind changes in " + str(len(d["data"])) +
             r" steps, \ and on forever", WHITE),
            (r"Gold: \ \textit{every} learner fails on this class from positive data, \ so on the regular "
             r"languages too", GOAL),
        ], font_size=21, aligned_edge=LEFT).next_to(gs, DOWN, buff=0.45).set_x(0)
        with self.voiceover(
            "Mark Gold's 1967 paper found the first limit on learning in the limit. <bookmark mark='a'/>Take the "
            "class of languages consisting of every finite set of numbers, together with the set of all numbers. "
            "The learner sees examples from the true language, positive examples only, and guesses which language "
            "it is. <bookmark mark='b'/>Here is an adversary. While the learner guesses a finite set, the "
            "adversary shows a new number. <bookmark mark='c'/>When the learner guesses all the numbers, the "
            "adversary repeats an old one, and keeps repeating, until the learner backs down to a finite guess. If "
            "it never backs down, the data were from a finite language, and the learner is wrong forever. "
            "<bookmark mark='d'/>This learner backs down, so the adversary goes on: twenty-nine changes of mind in "
            "thirty steps, and on forever, while the data spell out every number. <bookmark mark='e'/>Gold proved "
            "that every learner can be beaten this way. No method identifies this class from positive data alone, and "
            "since every finite language, and the language of all strings, is regular, no method identifies the "
            "regular languages either. "
            "With negative examples as well, far more becomes learnable. Children hear few negative examples, and "
            "linguists have read Gold's theorem as evidence that the grammars a child can learn are constrained in "
            "advance."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(cls))
            vo.wait_until("b")
            self.play(FadeIn(dl), FadeIn(gl), FadeIn(rules[0]))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(data[k]), FadeIn(gs[k])) for k in range(4)],
                                  lag_ratio=0.5))
            vo.wait_until("c")
            self.play(FadeIn(rules[1]))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(data[k]), FadeIn(gs[k])) for k in range(4, n)],
                                  lag_ratio=0.25), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(rules[2]))
            vo.wait_until("e")
            self.play(FadeIn(rules[3]))
        self.clear_scene()

    def putnam(self):
        d = load("gold")["putnam"]
        hc = history_card(1963, r"Hilary Putnam", r"`Degree of Confirmation and Inductive Logic'", width=6.6,
                          color=HIST).to_corner(UL, buff=0.3)
        idea = stack([(r"take any computable predictor of the next bit", WHITE),
                      (r"build the sequence that always does the opposite: \ it is computable too", BAD)],
                     font_size=22).next_to(hc, DOWN, buff=0.3).set_x(0)
        n = d["n"]
        cw = 0.48
        x0 = -cw * (n - 1) / 2
        bars = VGroup()
        bits = VGroup()
        for k in range(n):
            p = d["predictions"][k]
            b = Rectangle(width=cw - 0.1, height=max(p * 1.6, 0.03), stroke_width=0, fill_color=FUT,
                          fill_opacity=0.8)
            b.move_to([x0 + k * cw, -1.2 + b.height / 2, 0])
            bars.add(b)
            bits.add(MathTex(str(d["sequence"][k]), font_size=24, color=BAD).move_to([x0 + k * cw, -1.6, 0]))
        half = DashedLine([x0 - 0.3, -1.2 + 0.8, 0], [-x0 + 0.3, -1.2 + 0.8, 0], color=GREY_B, stroke_width=1.5)
        bl = label(r"Laplace's $P(1)$", font_size=18, color=FUT).next_to(half, UP, buff=0.08).align_to(half, LEFT)
        sl = label(r"actual", font_size=18, color=BAD).next_to(bits, LEFT, buff=0.15)
        foot = stack([(r"Laplace's rule: \ wrong " + str(d["wrong"]) + r" times out of " + str(n), BAD),
                      (r"no computable method learns every computable regularity", GOAL)], font_size=22).to_edge(
            DOWN, buff=0.25)
        with self.voiceover(
            "Hilary Putnam had already turned a similar argument against Carnap. <bookmark mark='a'/>Take any "
            "computable method for predicting the next bit of a sequence. <bookmark mark='b'/>Build the sequence "
            "that always does the opposite of what the method predicts. Since the method is computable, so is this "
            "sequence. <bookmark mark='c'/>Here the method is Laplace's rule. Whenever it thinks a one is more likely, "
            "the sequence shows a zero, and the other way round. <bookmark mark='d'/>Laplace's rule is wrong twenty "
            "four times out of twenty four, on a sequence as simple as zero one zero one. Every computable inductive "
            "method has such a blind spot: no computable method can learn every computable regularity."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("ab", idea):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("c")
            self.play(Create(half), FadeIn(bl), FadeIn(sl))
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[k], DOWN), FadeIn(bits[k])) for k in
                                    range(n)], lag_ratio=0.12), run_time=4)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def hierarchy(self):
        head = label(r"How hard is a question? \ Kelly's hierarchy", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{solvable by}", r"\text{example}", r"\text{form}"]
        rows = [[label(r"verify with certainty", font_size=21, color=OK),
                 label(r"`some swan is black'", font_size=21), MathTex(r"\Sigma_1", font_size=28, color=OK)],
                [label(r"refute with certainty", font_size=21, color=BAD),
                 label(r"`all swans are white' \ (Popper's kind)", font_size=21),
                 MathTex(r"\Pi_1", font_size=28, color=BAD)],
                [label(r"decide in the limit", font_size=21, color=FUT),
                 label(r"`exactly three particles exist'", font_size=21), MathTex(r"\Delta_2", font_size=28,
                                                                                    color=FUT)],
                [label(r"verify in the limit", font_size=21, color=PAST),
                 label(r"`only finitely many black swans'", font_size=21),
                 MathTex(r"\Sigma_2", font_size=28, color=PAST)],
                [label(r"refute in the limit", font_size=21, color=A_C),
                 label(r"`infinitely many black swans'", font_size=21), MathTex(r"\Pi_2", font_size=28, color=A_C)]]
        grid = ValueGrid(hd, rows, col_w=[3.6, 5.6, 1.4], cell_h=0.68, font_size=24).next_to(head, DOWN, buff=0.45)
        foot = stack([(r"the solvable questions are exactly the levels of a topological hierarchy \ (Kelly, \ 1996)",
                       GOAL),
                      (r"falsifiability is one rung, \ not the whole ladder", GREY_A)], font_size=22).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Kevin Kelly turned these ideas into a theory of how hard an empirical question is. "
            "<bookmark mark='a'/>Some hypotheses can be verified with certainty: some swan is black. When it is "
            "true, you eventually see the swan and can say so for good. <bookmark mark='b'/>Some can be refuted "
            "with certainty, like all swans are white: these are exactly Popper's falsifiable hypotheses. "
            "<bookmark mark='c'/>Some can only be decided in the limit: exactly three particles exist. You can be "
            "wrong for a while, but you settle eventually. <bookmark mark='d'/>Some can only be verified in the "
            "limit: only finitely many black swans. <bookmark mark='e'/>And some only refuted in the limit. "
            "<bookmark mark='f'/>Kelly showed that what a method can achieve corresponds exactly to the level of the "
            "hypothesis in a topological hierarchy, like the arithmetical hierarchy of Part 7. Falsifiability is "
            "one rung, not the whole ladder."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abcde", range(5)):
                vo.wait_until(mk)
                self.play(*[FadeIn(grid.cell[r][c]) for c in range(3)])
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()
