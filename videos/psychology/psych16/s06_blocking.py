from __future__ import annotations

from videos.psychology.psych16.common import *  # noqa: F403


class Blocking(VoiceoverScene):
    def construct(self):
        self.card()
        self.design()
        self.surprise()

    def card(self):
        card = chapter_card(5, r"Blocking", r"Can a perfectly paired cue teach nothing?",
                            lit={1969: r"Kamin"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter five. Blocking."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def design(self):
        head = heading(r"Kamin's design, \ 1969")
        cols = [r"phase 1", r"phase 2", r"test: \ the light alone"]
        xs = [-1.4, 2.1, 5.2]
        heads = VGroup(*[label(t, font_size=26, color=GREY_A).move_to([x, 1.9, 0]) for t, x in zip(cols, xs)])
        r1 = VGroup(label(r"blocking group", font_size=26, color=CUE_A).move_to([-5.0, 1.0, 0]),
                    label(r"noise $\to$ shock", font_size=26, color=CUE_A).move_to([xs[0], 1.0, 0]),
                    label(r"noise + light $\to$ shock", font_size=26).move_to([xs[1], 1.0, 0]),
                    label(r"little fear", font_size=28, color=INHIB).move_to([xs[2], 1.0, 0]))
        r2 = VGroup(label(r"control group", font_size=26, color=CS).move_to([-5.0, -0.1, 0]),
                    label(r"nothing", font_size=26, color=GREY_B).move_to([xs[0], -0.1, 0]),
                    label(r"noise + light $\to$ shock", font_size=26).move_to([xs[1], -0.1, 0]),
                    label(r"strong fear", font_size=28, color=CR).move_to([xs[2], -0.1, 0]))
        rule = Line([-6.4, 1.5, 0], [6.4, 1.5, 0], color=GREY_D, stroke_width=2)
        rows = rows_of([
            (r"both groups get the same pairings of the light with shock in phase 2", WHITE),
            (r"for the blocking group, \ the noise already predicts the shock: \ the light adds no information", CUE_A),
            (r"the earlier learning about the noise blocks learning about the light", INHIB),
        ], 12.4, 27, 0.28).to_edge(DOWN, buff=0.75)
        tag = historical_tag(archive.KAMIN_1969.cite)
        with self.voiceover(
            "The one more experiment was Leon Kamin's, published in 1969, and it's the most important design in this "
            "part. <bookmark mark='a'/> Rats in the blocking group first learn that a noise predicts a shock. "
            "<bookmark mark='b'/> Then the noise and a light come on together, followed by the same shock. A control "
            "group gets only this second phase. <bookmark mark='c'/> Finally the light is tested alone. "
            "<bookmark mark='d'/> Both groups had exactly the same pairings of light with shock. The control rats "
            "learned to fear the light strongly. The blocking rats learned almost nothing about it. "
            "<bookmark mark='e'/> For them the noise already predicted the shock, so the light told them nothing new. "
            "Learning about the noise had blocked learning about the light."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(heads), Create(rule))
            vo.wait_until("a")
            self.play(FadeIn(r1[0]), FadeIn(r1[1]))
            vo.wait_until("b")
            self.play(FadeIn(r1[2]), FadeIn(r2[0]), FadeIn(r2[1]), FadeIn(r2[2]))
            vo.wait_until("c")
            self.play(Indicate(heads[2]))
            vo.wait_until("d")
            self.play(FadeIn(r2[3]), FadeIn(r1[3]), FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def surprise(self):
        head = heading(r"Learning is driven by surprise")
        rows = rows_of([
            (r"Kamin's reading: \ an animal learns only when the outcome is unexpected", WHITE),
            (r"make the shock stronger in phase 2, \ so it is surprising again, \ and the light is learned: "
             r"\ unblocking", US),
            (r"pairing is not enough; \ contingency is not enough; \ what matters is the error in a prediction", CR),
            (r"blocking is in every theory of learning since, \ and in Part 17's dopamine neurons; \ but the Ledger "
             r"finds it less reliable than the textbooks say", GREY_A),
        ], 12.4, 29, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "Kamin's interpretation is the turning point of this part. <bookmark mark='a'/> An animal learns about a "
            "cue only when the outcome that follows it is surprising. <bookmark mark='b'/> He tested the idea "
            "directly. If the shock in phase two is made stronger than the one the noise predicts, the outcome is a "
            "surprise again, and now the light is learned. That's called unblocking. <bookmark mark='c'/> So pairing "
            "isn't enough, and even contingency isn't quite the point. What drives learning is the error in a "
            "prediction: the difference between what happened and what was expected. <bookmark mark='d'/> Blocking "
            "is built into nearly every theory of learning since, and Part 17 finds its signature in the firing of "
            "dopamine neurons. It's also less reliable than the textbooks suggest, and the Ledger will say how much "
            "less."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
