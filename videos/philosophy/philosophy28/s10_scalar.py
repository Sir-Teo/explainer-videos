from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


class Scalar(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Some, \ not all", r"Why does `some' suggest `not all'?", lit=(1972, 2001), part=PART)
        with self.voiceover("Chapter nine. Some, not all."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.scales()
        self.derivation()
        self.evidence()

    def scales(self):
        head = label(r"Horn scales", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        scales = [(r"some", r"all"), (r"warm", r"hot"), (r"possible", r"certain"), (r"or", r"and"),
                  (r"good", r"excellent")]
        rows = VGroup()
        for i, (w, s) in enumerate(scales):
            a = label(w, font_size=24, color=WORD)
            b = label(s, font_size=24, color=USE)
            ar = Arrow(LEFT, RIGHT, color=GREY_B, buff=0).scale(0.6)
            g = VGroup(a, ar, b).arrange(RIGHT, buff=0.3)
            rows.add(g)
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([-3.2, -0.1, 0])
        side = stack([(r"each pair: \ the stronger term entails the weaker", WHITE),
                      (r"`all passed' entails `some passed'; \ not the other way", RULE_C),
                      (r"using the weaker term conveys that the stronger does not hold", GOAL),
                      (r"Horn \ (1972): \ these ordered scales generate implicatures systematically", HIST)],
                     font_size=21, aligned_edge=LEFT, width=6.0, buff=0.3).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "One implicature is so regular that it can be studied like a law. <bookmark mark='a'/>Laurence Horn "
            "noticed in 1972 that words come in scales: some and all; warm and hot; possible and certain; or and and; "
            "good and excellent. <bookmark mark='b'/>In each pair the stronger term entails the weaker. All the "
            "students passed entails that some did; not the other way. <bookmark mark='c'/>And using the weaker term "
            "conveys that the stronger one does not hold. Some passed suggests not all; warm suggests not hot; "
            "possible suggests not certain. <bookmark mark='d'/>The pattern is systematic enough to be called scalar "
            "implicature."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25))
            for mk, r in zip("bcd", (side[:2], side[2:3], side[3:])):
                vo.wait_until(mk)
                self.play(*[FadeIn(x) for x in r])
        self.clear_scene()

    def derivation(self):
        head = label(r"The Gricean derivation", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        steps = [
            (r"1", r"she said `some of the students passed'", WORD),
            (r"2", r"`all of them passed' would have been more informative, \ and just as easy to say", RULE_C),
            (r"3", r"she is cooperative, \ so by Quantity she would have said it, \ if she believed it and it was "
                   r"relevant", USE),
            (r"4", r"she is well informed about the exam", WORLD),
            (r"5", r"so she believes that not all of them passed", GOAL),
            (r"cancel", r"`some of the students passed, \ in fact all of them did': \ no contradiction", OK),
        ]
        g = rows_table(steps, top=1.6, gap=0.42, width=9.6, x_text=-4.6, label_size=22, text_size=21)
        with self.voiceover(
            "Grice's maxims derive it. <bookmark mark='a'/>She said some of the students passed. "
            "<bookmark mark='b'/>All of them passed would have been more informative, and no harder to say. "
            "<bookmark mark='c'/>She is cooperative, so by the maxim of Quantity she would have said it, if she "
            "believed it. <bookmark mark='d'/>She is well informed about the exam; she would know. "
            "<bookmark mark='e'/>So she believes that not all of them passed. <bookmark mark='f'/>And the inference "
            "can be cancelled: some of the students passed, in fact all of them did, is not a contradiction. The not "
            "all is implicated, not said."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def evidence(self):
        head = label(r"What experiments show", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"children", r"Noveck \ (2001): \ `some giraffes have long necks' \ accepted far more often by children "
                          r"than by adults: \ children are more literal", WORD),
            (r"timing", r"Bott and Noveck \ (2004): \ adults who read `some' as `not all' take longer to respond", USE),
            (r"context", r"the implicature weakens when the stronger alternative is irrelevant, \ or the speaker is "
                         r"uninformed", WORLD),
            (r"the debate", r"pragmatic inference \ (neo-Griceans; \ relevance theory) \ or a grammatical operator "
                            r"like a silent `only' \ (Chierchia, \ Fox, \ Spector)?", RULE_C),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "Scalar implicature became one of the best studied phenomena in experimental pragmatics. "
            "<bookmark mark='a'/>Ira Noveck found in 2001 that children accept statements like some giraffes have "
            "long necks far more often than adults do. Children are more literal; adults hear not all, and object. "
            "<bookmark mark='b'/>Lewis Bott and Noveck found in 2004 that adults who take some to mean not all are "
            "slower to respond, as if the inference costs effort. <bookmark mark='c'/>The implicature also weakens "
            "when the stronger alternative is irrelevant, or the speaker is not in a position to know. "
            "<bookmark mark='d'/>Whether it is a pragmatic inference, as the neo-Griceans and relevance theorists "
            "hold, or the work of a silent grammatical operator like only, as Gennaro Chierchia, Danny Fox and "
            "Benjamin Spector have argued, is still debated. The next chapter builds the pragmatic account as "
            "explicit probabilistic reasoning."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
