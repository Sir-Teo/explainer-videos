from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.chicken()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"The man who has fed the chicken every day throughout its life at last wrings its neck "
                       r"instead.", r"Bertrand Russell", r"\textit{The Problems of Philosophy} \ (1912)", width=9.6,
                       font_size=26).next_to(t, DOWN, buff=0.6)
        with self.voiceover(
            "Parts 13 and 14 told us how to change our minds when evidence arrives. This part asks whether the "
            "evidence of the past can tell us anything at all about the future. <bookmark mark='a'/>Bertrand Russell's "
            "chicken expected breakfast every morning, with ever greater confidence, <bookmark mark='b'/>until the "
            "morning it got something else."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=BAD, scale_factor=1.03))
        self.clear_scene()

    def chicken(self):
        head = label(r"A thousand mornings", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        n = 40
        days = VGroup(*[Square(side_length=0.22, stroke_width=0, fill_color=PAST, fill_opacity=0.85).move_to(
            [-6.2 + (i % 40) * 0.3, 1.4, 0]) for i in range(n)])
        last = Square(side_length=0.22, stroke_width=0, fill_color=BAD, fill_opacity=0.9).next_to(days, RIGHT,
                                                                                                buff=0.08)
        conf = stack([
            (r"each morning: \ fed; \ confidence that tomorrow is the same \ grows", PAST),
            (r"the evidence was real; \ the inference was natural; \ the conclusion was false", BAD),
            (r"Hume: \ \textit{nothing} in the past entails anything about the future", GOAL),
            (r"science, \ machine learning \ and everyday life all bet that it does", WHITE),
        ], font_size=24, buff=0.32, width=12.4).next_to(days, DOWN, buff=0.7).set_x(0)
        with self.voiceover(
            "Picture the chicken's life. <bookmark mark='a'/>Every morning it is fed, and every morning its "
            "confidence that tomorrow will be the same grows. <bookmark mark='b'/>Then the farmer comes with a knife. "
            "The evidence was real, the inference natural, and the conclusion false. <bookmark mark='c'/>David Hume's "
            "point is that nothing in the past, however long and regular, entails anything about the future. "
            "<bookmark mark='d'/>Yet science, machine learning and everyday life all depend on learning from "
            "experience. Can that be justified, and if not, what can be said for it?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in days], lag_ratio=0.04), FadeIn(conf[0]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(last, scale=1.5), FadeIn(conf[1]))
            for mk, r in zip("cd", conf[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Hume's problem; \ Laplace's rule and the sunrise; \ de Finetti; \ Carnap's continuum",
            r"inference in India: \ the wheel of reasons, \ checked",
            r"the ravens \ (Price List); \ confirmation measures; \ grue, \ in a network",
            r"Popper's falsification; \ the best explanation, \ raced; \ the merging of opinions",
            r"learning in the limit: \ Gold, \ Putnam; \ Ockham's razor as fewest retractions",
            r"Solomonoff's universal prior; \ compression and MDL",
            r"no free lunch \ (the Wall); \ Reichenbach's pragmatic vindication",
        ], font_size=24)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Hume's problem, and the first mathematical answer, Laplace's. "
            "<bookmark mark='b'/>The Indian logicians, who faced the same problem a thousand years earlier. "
            "<bookmark mark='c'/>Three paradoxes of confirmation: the ravens, the choice of measure, and grue, which "
            "the Reasoner reproduces in a neural network. <bookmark mark='d'/>Popper, inference to the best "
            "explanation, and the theorem that Bayesians eventually agree. <bookmark mark='e'/>The theory of learning in the limit, and a theorem that justifies "
            "Ockham's razor. <bookmark mark='f'/>The universal prior, and compression. <bookmark mark='g'/>And the no "
            "free lunch theorem, this part's brick in the Wall, with the best vindication of induction we have."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
