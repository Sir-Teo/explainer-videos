from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


class Grice(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"What is meant", r"How do we say more than our words say?", lit=(1957, 1975), part=PART)
        with self.voiceover("Chapter eight. What is meant."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.principle()
        self.examples()
        self.tests()
        self.flouting()

    def principle(self):
        q = quote_card(r"Make your conversational contribution such as is required, \ at the stage at which it occurs, "
                       r"\ by the accepted purpose or direction of the talk exchange in which you are engaged.",
                       r"H. P. Grice", r"`Logic and Conversation' \ (William James lectures, 1967; \ published 1975)",
                       width=11.0, font_size=23).to_edge(UP, buff=0.4)
        rows = [
            (r"Quantity", r"be as informative as is required, \ and no more", WORD),
            (r"Quality", r"say only what you believe true, \ and have evidence for", WORLD),
            (r"Relation", r"be relevant", USE),
            (r"Manner", r"be perspicuous: \ avoid obscurity and ambiguity; \ be brief, \ and orderly", RULE_C),
        ]
        g = rows_table(rows, top=-0.4, gap=0.4, width=8.8, x_text=-3.0, label_size=23, text_size=21)
        with self.voiceover(
            "Paul Grice, in his William James lectures of 1967, gave the theory of how hearers get from what is said "
            "to what is meant. <bookmark mark='a'/>It starts from a principle: make your contribution such as is "
            "required, at the stage at which it occurs, by the accepted purpose of the talk exchange. He called it "
            "the cooperative principle. <bookmark mark='b'/>Under it fall four maxims. Quantity: be as informative as "
            "is required, and no more. <bookmark mark='c'/>Quality: say only what you believe true, and have evidence "
            "for. <bookmark mark='d'/>Relation: be relevant. <bookmark mark='e'/>Manner: be perspicuous; avoid "
            "obscurity and ambiguity; be brief and orderly."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            for mk, r in zip("bcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def examples(self):
        head = label(r"Implicature", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        ex1 = stack([(r"A: \ `I am out of petrol.'", WORD), (r"B: \ `There is a garage round the corner.'", USE),
                     (r"implicated: \ the garage is open, \ and sells petrol \ (Relation)", GOAL)], font_size=22,
                    aligned_edge=LEFT, buff=0.2)
        ex2 = stack([(r"a reference letter for a philosophy post: \ `Mr X's command of English is excellent, \ and his "
                      r"attendance at tutorials has been regular.'", WORD),
                     (r"implicated: \ he is no good at philosophy \ (Quantity, \ flouted)", GOAL)], font_size=22,
                    aligned_edge=LEFT, width=11.4, buff=0.2)
        VGroup(ex1, ex2).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([0, 0.2, 0])
        foot = label(r"what is meant \ = \ what is said \ + \ what the hearer must assume to keep the speaker "
                     r"cooperative", font_size=21, color=RULE_C).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Now watch the maxims work. <bookmark mark='a'/>A says: I am out of petrol. B says: there is a garage "
            "round the corner. B has not said the garage is open. <bookmark mark='b'/>But if B is being relevant, B "
            "must think it is open and sells petrol; so that is what B conveys. Grice called it a conversational "
            "implicature. <bookmark mark='c'/>A harsher example. A professor writes a reference for a philosophy job: "
            "Mr X's command of English is excellent, and his attendance at tutorials has been regular. "
            "<bookmark mark='d'/>The writer is obviously saying far less than is required. A cooperative writer "
            "would only do that if he had nothing good to say about X's philosophy. The maxim is flouted, openly, to "
            "convey something it would be rude to say. <bookmark mark='e'/>What is meant is what is said, plus what "
            "the hearer must assume to keep the speaker cooperative."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ex1[0]), FadeIn(ex1[1]))
            vo.wait_until("b")
            self.play(FadeIn(ex1[2]))
            vo.wait_until("c")
            self.play(FadeIn(ex2[0]))
            vo.wait_until("d")
            self.play(FadeIn(ex2[1]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def tests(self):
        head = label(r"How to tell an implicature", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"cancellable", r"`there is a garage round the corner, \ but it's closed': \ no contradiction", OK),
            (r"calculable", r"the hearer can work it out from what is said, \ the maxims and the context", RULE_C),
            (r"non-detachable", r"say the same thing in other words, \ and the implicature remains", WORD),
            (r"not said", r"so the sentence's truth conditions do not include it: \ Part 27's semantics can stay "
                          r"simple", USE),
            (r"meaning itself", r"Grice \ (1957): \ to mean something is to intend an effect by means of the hearer's "
                                r"recognizing that intention", HIST),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "Grice gave tests that separate implicature from what is said. <bookmark mark='a'/>It is cancellable: "
            "there is a garage round the corner, but it's closed, is not a contradiction. <bookmark mark='b'/>It is "
            "calculable: the hearer can work it out from what was said, the maxims and the context. "
            "<bookmark mark='c'/>It is non-detachable: say the same thing in other words, and the implicature remains. "
            "<bookmark mark='d'/>So it is not part of what the sentence says, and the truth conditions of Part 27 "
            "can stay simple. <bookmark mark='e'/>Behind all this was Grice's account of meaning itself, from 1957: "
            "to mean something by an utterance is to intend to produce an effect in a hearer by means of the hearer's "
            "recognition of that very intention."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def flouting(self):
        head = label(r"Flouting, \ and after Grice", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"flouting", r"breaking a maxim openly, \ so that the hearer looks for what is meant instead", USE),
            (r"Quantity", r"`war is war': \ a tautology says nothing, \ so it must be meant to convey something", WORD),
            (r"Quality", r"`he is a fine friend', \ of a traitor: \ irony; \ `you are the cream in my coffee': \ "
                         r"metaphor", BAD),
            (r"Manner", r"`Miss X produced a series of sounds that corresponded closely with the score of "
                        r"\textit{Home Sweet Home}'", RULE_C),
            (r"generalized", r"some implicatures arise by default \ (`some' $\to$ `not all'); \ others only in a "
                             r"context \ (the garage)", GOAL),
            (r"after Grice", r"Horn \ (1984): \ two principles, \ Q and R; \ Levinson \ (2000): \ Q, \ I and M; \ "
                             r"Sperber and Wilson \ (1986): \ relevance alone", HIST),
        ]
        g = rows_table(rows, top=1.7, gap=0.4, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "Maxims can also be broken in the open. <bookmark mark='a'/>Grice called this flouting: a speaker "
            "plainly fails to observe a maxim, and the hearer, still assuming cooperation, looks for what is meant "
            "instead. <bookmark mark='b'/>War is war is a tautology. Taken literally it says nothing, so it must be "
            "meant to convey something, perhaps that terrible things happen in war, and that is how it goes. "
            "<bookmark mark='c'/>He is a fine friend, said of someone who has just betrayed you, flouts Quality, and "
            "is heard as irony; you are the cream in my coffee flouts it too, and is heard as metaphor. "
            "<bookmark mark='d'/>A reviewer who writes that Miss X produced a series of sounds that corresponded "
            "closely with the score of Home Sweet Home, rather than that she sang it, flouts Manner, and conveys "
            "what she thought of the singing. <bookmark mark='e'/>Grice also distinguished generalized "
            "implicatures, which arise by default, like some suggesting not all, from particularized ones, which "
            "need a special context, like the garage. <bookmark mark='f'/>His successors simplified the maxims. "
            "Laurence Horn reduced them to two opposed principles: say as much as you can, and say no more than you "
            "must. Stephen Levinson used three heuristics; Dan Sperber and Deirdre Wilson, in their theory of "
            "relevance, kept only one."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
