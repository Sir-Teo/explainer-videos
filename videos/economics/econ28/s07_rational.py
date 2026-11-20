from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Rational(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Rational expectations", r"What if people forecast with the true model?", "Chapter six. "
             r"Rational expectations.", lit={1961: r"Muth", 1972: r"Lucas"}, scale=("person", "nation"),
             horizon=("a year",))
        self.idea()
        self.claims()

    def idea(self):
        rows = VGroup(
            label(r"Muth, \ 1961: \ expectations are informed predictions of future events", font_size=24,
                  color=E.ACCENT),
            label(r"assume people's forecasts are the model's own forecasts, \ given what they know", font_size=23,
                  color=EXPECT),
            MathTex(r"\pi^e_t = \mathbb{E}\left[\pi_t \mid \text{information at } t-1\right]", font_size=40,
                    color=EXPECT),
            label(r"then forecast errors are unpredictable: \ no pattern a forecaster could exploit", font_size=23,
                  color=OUTPUT),
            label(r"the opposite of the 1970s' errors, \ which ran the same way for fifteen years", font_size=22,
                  color=HOLD),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Muth, \ Econometrica 29(3) (1961): \ 315--335", corner=DR, font_size=12)
        with self.voiceover(
            "In 1961 John Muth proposed a different idea, which waited a decade to catch on. "
            "<bookmark mark='a'/> Suppose people's forecasts are the same as the model's own forecasts, given "
            "whatever they know. <bookmark mark='b'/> Expected inflation is then the true conditional expectation "
            "of inflation, using the information available. <bookmark mark='c'/> It follows that forecast errors "
            "are unpredictable. If they ran in a pattern, a smart forecaster would spot it and correct for it. "
            "<bookmark mark='d'/> That is exactly the opposite of the errors of the last chapter, which ran the same "
            "way for fifteen years."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def claims(self):
        cards = point_cards([
            (r"it does claim", r"no systematic, \ exploitable \\ errors, \ on average", OUTPUT),
            (r"it does not claim", r"that people know everything, \\ or never make mistakes", HOLD),
            (r"its power", r"a policy everyone can foresee \\ is built into expectations", EXPECT),
            (r"its weakness", r"how did people learn the model? \\ which model? \ (chapter 16)", INFL),
        ], width=12.6, cols=2, font_size=22).move_to(DOWN * 0.1)
        head = label(r"what it claims, \ and what it does not", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Rational expectations is easy to caricature, so be precise. <bookmark mark='a'/> It does claim that "
            "people make no systematic, exploitable errors on average. <bookmark mark='b'/> It does not claim that "
            "people know everything, or that they are never wrong; only that their mistakes are not predictable "
            "from what they already know. <bookmark mark='c'/> Its power is this: a policy that everyone can "
            "foresee is already built into their expectations, and so cannot surprise them. "
            "<bookmark mark='d'/> Its weakness is the question of how people came to know the model, and which "
            "model they believe. The last chapter of this part looks at what surveys say."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
