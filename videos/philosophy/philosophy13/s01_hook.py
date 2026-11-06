from __future__ import annotations

from videos.philosophy.philosophy13.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.forecast()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"The subject of our inquiry is the logic of partial belief.", r"Frank Ramsey",
                       r"`Truth and Probability' \ (1926)", width=8.6, font_size=28).next_to(t, DOWN, buff=0.6)
        with self.voiceover(
            "Parts 11 and 12 treated belief as all or nothing: you know, or believe, or you don't. "
            "<bookmark mark='a'/>But most of what we think comes in degrees. Frank Ramsey, at twenty-three, "
            "announced the subject of this part: the logic of partial belief. <bookmark mark='b'/>It turned out to "
            "be probability theory, and it has become the working epistemology of science, medicine, finance and "
            "machine learning."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=CRED, scale_factor=1.03))
        self.clear_scene()

    def forecast(self):
        head = label(r"`70\% chance of rain'", font_size=36, color=CONN).to_edge(UP, buff=0.5)
        bar_bg = Rectangle(width=8.0, height=0.5, stroke_color=GREY_C, stroke_width=2).move_to([0, 1.4, 0])
        bar = Rectangle(width=5.6, height=0.5, stroke_width=0, fill_color=CRED, fill_opacity=0.8)
        bar.align_to(bar_bg, LEFT).set_y(1.4)
        pct = label(r"0.7", font_size=26, color=CRED).next_to(bar, UP, buff=0.15)
        rows = VGroup(
            label(r"not knowledge, \ not mere belief: \ a degree of confidence", font_size=25),
            label(r"what laws must degrees obey? \ the probability axioms, \ and why", font_size=24, color=GOAL),
            label(r"how should they change with evidence? \ Bayes, \ Jeffrey", font_size=24, color=GOAL),
            label(r"where do they start? \ indifference, \ and Bertrand's chords \ (the Wall)", font_size=24,
                  color=BAD),
            label(r"how do they meet belief, \ chance, \ and the question `where am I?'", font_size=24,
                  color=GOAL)).arrange(DOWN, buff=0.3).move_to([0, -1.2, 0])
        with self.voiceover(
            "Take a weather forecast. <bookmark mark='a'/>Seventy percent chance of rain. <bookmark mark='b'/>The "
            "forecaster does not know it will rain, and does not simply believe it either. She has a degree of "
            "confidence, a credence. <bookmark mark='c'/>What laws must degrees of belief obey, and why those? "
            "<bookmark mark='d'/>How should they change when evidence comes in? <bookmark mark='e'/>Where do they "
            "start, before any evidence? Here we lay this part's brick in the Wall: Bertrand's paradox, which shows "
            "that the natural answer, indifference, is not even well defined. <bookmark mark='f'/>And how do degrees "
            "of belief connect with all-or-nothing belief, with objective chance, and with the strange question "
            "of where, and when, you are?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(bar_bg), GrowFromEdge(bar, LEFT), FadeIn(pct))
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"credences as points on a simplex: \ Ramsey, \ de Finetti, \ Kolmogorov",
            r"two arguments for the axioms: \ the Dutch book, \ found by an LP; \ accuracy dominance",
            r"proper scoring rules, \ and forecasters scored",
            r"conditionalization, \ diachronic books, \ Jeffrey's cloth; \ priors and maximum entropy",
            r"Bertrand's chords \ (the Wall); \ chance and the Principal Principle; \ imprecise credence",
            r"the lottery, \ the preface, \ stable belief; \ Sleeping Beauty; \ Doomsday",
            r"Bayesian machines, \ and what they cannot compute",
        ], font_size=25)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Credences as points in a geometric space. <bookmark mark='b'/>Two "
            "arguments that they must obey the laws of probability: one about betting, one about accuracy, each "
            "computed. <bookmark mark='c'/>How to score a forecaster honestly. <bookmark mark='d'/>How credences "
            "should change, and where they should start. <bookmark mark='e'/>Bertrand's chords, objective chance, and "
            "credences too vague for a single number. <bookmark mark='f'/>The lottery and the preface, Sleeping "
            "Beauty, and the Doomsday argument. <bookmark mark='g'/>And Bayesian machines, and the limits of what "
            "they can compute."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
