from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.crisis()
        self.sides()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"But although all our cognition commences with experience, yet it does not on that account all "
                       r"arise from experience.", r"Immanuel Kant", r"\textit{Critique of Pure Reason}, \ B1 \ (1787)",
                       width=9.6, font_size=28).next_to(t, DOWN, buff=0.6)
        with self.voiceover(
            "Part 10 opens the act on knowledge, and it begins with a question about the mind. <bookmark mark='a'/>"
            "How much of what we know comes in from the world, and how much does the mind bring to it? "
            "<bookmark mark='b'/>Immanuel Kant's answer, at the start of his Critique of Pure Reason, is the "
            "destination of this part: all our knowledge begins with experience, but it does not all arise from "
            "experience."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=KANT, scale_factor=1.03))
        self.clear_scene()

    def crisis(self):
        hcs = VGroup(history_card(r"c.\ 200", r"Sextus Empiricus", r"\textit{Outlines of Pyrrhonism}: \ for every "
                                  r"argument, \ an equal argument against", width=4.6, color=HIST),
                     history_card(1580, r"Michel de Montaigne", r"\textit{Essays}: \ `Que sais-je?' \ (What do I "
                                  r"know?)", width=4.2, color=HIST),
                     history_card(1610, r"Galileo Galilei", r"\textit{Sidereus Nuncius}: \ the telescope shows what "
                                  r"the eye cannot", width=4.4, color=HIST)).arrange(RIGHT, buff=0.3).to_edge(UP,
                                                                                                        buff=0.4)
        rows = VGroup(
            label(r"Agrippa's trilemma: \ every reason needs a reason, \ so the chain runs forever, \ circles, \ or "
                  r"stops by fiat", font_size=24, color=DOUBT),
            label(r"the old authorities fail: \ the moon has mountains, \ and Jupiter has moons", font_size=24,
                  color=SENSE),
            label(r"the new science needs a foundation that cannot be doubted", font_size=26, color=GOAL)).arrange(
            DOWN, buff=0.4).move_to([0, -0.8, 0])
        with self.voiceover(
            "In the sixteenth century certainty was in short supply. <bookmark mark='a'/>The ancient skeptics had "
            "been rediscovered. Sextus Empiricus, around the year 200, taught that every argument can be met by an "
            "equal argument against, and recorded Agrippa's trilemma: every reason needs a reason, so the chain of "
            "reasons either runs on forever, comes round in a circle, or stops at something simply assumed. "
            "<bookmark mark='b'/>In 1580 Michel de Montaigne took as his motto: what do I know? <bookmark mark='c'/>"
            "And in 1610 Galileo turned a telescope on the sky and saw mountains on the moon and moons around Jupiter. "
            "The heavens of Aristotle, taught for two thousand years, were wrong. <bookmark mark='d'/>The new "
            "science needed a foundation that could not be doubted. Where could it come from?"
        ) as vo:
            self.play(FadeIn(hcs[0]))
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hcs[1]))
            vo.wait_until("c")
            self.play(FadeIn(hcs[2]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def sides(self):
        head = label(r"Two answers, \ and a third", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        left = VGroup(label(r"from reason", font_size=30, color=REASON),
                      label(r"Descartes, \ Spinoza, \ Leibniz", font_size=24, color=WHITE),
                      label(r"innate ideas; \ truths seen by the light of reason", font_size=21, color=GREY_A),
                      label(r"the model: \ geometry", font_size=21, color=REASON)).arrange(DOWN, buff=0.2)
        right = VGroup(label(r"from experience", font_size=30, color=SENSE),
                       label(r"Locke, \ Berkeley, \ Hume", font_size=24, color=WHITE),
                       label(r"the mind begins as white paper", font_size=21, color=GREY_A),
                       label(r"the model: \ the new experimental science", font_size=21, color=SENSE)).arrange(
            DOWN, buff=0.2)
        cols = VGroup(left, right).arrange(RIGHT, buff=2.2).move_to([0, 0.6, 0])
        kant = VGroup(label(r"Kant: \ the mind supplies the form, \ experience the content", font_size=26,
                            color=KANT),
                      label(r"this part's brick in the Wall: \ Hume's problem \ and Kant's antinomies", font_size=24,
                            color=P.WALL)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Two answers dominated the next century and a half. <bookmark mark='a'/>The rationalists, Descartes, "
            "Spinoza and Leibniz, looked to reason. Some ideas are innate, and some truths are seen by the natural "
            "light of reason alone, as in geometry, their model of knowledge. <bookmark mark='b'/>The empiricists, "
            "Locke, Berkeley and Hume, looked to experience. The mind begins as white paper, and everything written "
            "on it comes through the senses, as in the new experimental science. <bookmark mark='c'/>Kant tried to "
            "combine them: the mind supplies the form of knowledge, experience its content. And on the way we meet "
            "this part's brick in the Wall: Hume's problem about experience, and Kant's antinomies, where reason "
            "contradicts itself."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left, shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(kant))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Descartes: \ doubt, \ the cogito, \ the circle; \ coordinates and the method of normals",
            r"Spinoza's \textit{Ethics} as a proof graph, \ built from the text",
            r"Leibniz: \ sufficient reason, \ finite and infinite analysis, \ the best of worlds",
            r"Locke, \ Molyneux's question, \ Berkeley",
            r"Hume: \ ideas, \ the fork, \ causation and induction",
            r"Kant: \ the synthetic a priori, \ space and time, \ the categories, \ the antinomies",
            r"what became of Kant's examples; \ Hegel, \ briefly; \ the Price List",
        ], font_size=25)
        with self.voiceover(
            "So: <bookmark mark='a'/>first Descartes, his doubt, his certainty, and his geometry. "
            "<bookmark mark='b'/>Then Spinoza's Ethics, which the Reasoner turns into a graph of proofs, read "
            "straight from the text. <bookmark mark='c'/>Then Leibniz and the principle of sufficient reason. "
            "<bookmark mark='d'/>Then the empiricists: Locke, a question about the newly sighted, and Berkeley. "
            "<bookmark mark='e'/>Then Hume, who woke Kant. <bookmark mark='f'/>Then Kant's system: the synthetic a "
            "priori, space and time, the categories, and the antinomies. <bookmark mark='g'/>And last, what later "
            "science did to Kant's examples, a short and honest look at Hegel, and the Price List."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
