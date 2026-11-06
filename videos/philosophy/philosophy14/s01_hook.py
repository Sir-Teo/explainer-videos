from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.swan()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"No statement is immune to revision.", r"W.\ V.\ O.\ Quine", r"`Two Dogmas of Empiricism' \ "
                                                                                    r"(1951)", width=7.6,
                       font_size=28).next_to(t, DOWN, buff=0.6)
        with self.voiceover(
            "Part 13 told us how degrees of belief should move with evidence. This part asks the same of belief itself, "
            "and of the sentences that guide change: conditionals. <bookmark mark='a'/>Quine said that no statement is "
            "immune to revision. <bookmark mark='b'/>But when something must go, logic does not say which."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=NEW, scale_factor=1.03))
        self.clear_scene()

    def swan(self):
        head = label(r"A black swan", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        beliefs = VGroup(*[VGroup(RoundedRectangle(width=4.6, height=0.7, corner_radius=0.14, color=BEL,
                                                   stroke_width=3), label(t, font_size=24)).arrange(ORIGIN)
                           for t in (r"all swans are white", r"this bird is a swan", r"my eyes are reliable here")])
        beliefs.arrange(DOWN, buff=0.3).move_to([-3.4, 0.2, 0])
        news = VGroup(RoundedRectangle(width=4.0, height=0.8, corner_radius=0.14, color=NEW, stroke_width=4),
                      label(r"I see: \ this bird is black", font_size=24, color=NEW)).arrange(ORIGIN).move_to(
            [3.4, 0.2, 0])
        clash = label(r"together: \ inconsistent", font_size=26, color=BAD).next_to(VGroup(beliefs, news), DOWN,
                                                                                    buff=0.6)
        rows = stack([(r"logic says \textit{that} something must go", WHITE),
                      (r"not \textit{which}, \ nor how much else goes with it", GOAL)], font_size=25).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "Here is the simplest case. <bookmark mark='a'/>You believe that all swans are white, that this bird is a "
            "swan, and that your eyes are reliable in this light. <bookmark mark='b'/>Then you see that the bird is "
            "black. <bookmark mark='c'/>Together, the four are inconsistent. <bookmark mark='d'/>Logic tells you that "
            "something must go. It does not tell you which, or how much else must go with it. Do you lose the belief "
            "that all swans are white, and also every belief you derived from it? Or doubt your eyes? This part is "
            "about the logic of that choice."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in beliefs], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(news, shift=LEFT * 0.3))
            vo.wait_until("c")
            self.play(FadeIn(clash), *[Indicate(b, color=BAD, scale_factor=1.03) for b in beliefs])
            vo.wait_until("d")
            self.play(FadeIn(rows))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"expansion, \ revision, \ contraction; \ revision versus update",
            r"the AGM postulates, \ checked; \ Grove's spheres; \ partial meet contraction",
            r"iterated revision: \ Spohn's ranks, \ Darwiche and Pearl",
            r"conditionals: \ the Ramsey test, \ and Gärdenfors's impossibility \ (the Wall)",
            r"counterfactuals: \ Stalnaker and Lewis; \ the probability of conditionals \ (Price List)",
            r"McGee's counterexample; \ default logic, \ System Z, \ KLM",
            r"argumentation frameworks; \ machines that revise, \ and LLM knowledge editing",
        ], font_size=24)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Three ways to change a mind, and the difference between learning and "
            "updating. <bookmark mark='b'/>The AGM postulates, which the Reasoner checks, and the spheres that "
            "characterize them. <bookmark mark='c'/>Changing again, and again. <bookmark mark='d'/>Then conditionals: "
            "Ramsey's test, and Gärdenfors's theorem that it cannot coexist with revision, this part's brick in the "
            "Wall. <bookmark mark='e'/>Counterfactuals, and why the probability of a conditional is not the probability "
            "of any proposition. <bookmark mark='f'/>A counterexample to modus ponens, and the logics of jumping to "
            "conclusions. <bookmark mark='g'/>Arguments that attack each other; and machines, including large language "
            "models, that have to change their minds."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
