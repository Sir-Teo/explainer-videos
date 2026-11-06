from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"An organism has conscious mental states if and only if there is something that it is like "
                       r"to \textit{be} that organism --- something it is like \textit{for} the organism.",
                       r"Thomas Nagel", r"`What Is It Like to Be a Bat?' \ (1974)", width=9.4,
                       font_size=28).next_to(t, DOWN, buff=0.45)
        with self.voiceover(
            "Part 30 asked whether a machine could have a mind, and left one question for later: whether anyone "
            "would be home. <bookmark mark='a'/>In 1974 Thomas Nagel put it in a sentence: an organism has conscious "
            "mental states if and only if there is something that it is like to be that organism, something it is "
            "like for the organism. <bookmark mark='b'/>This part is about that something: why it seems to resist "
            "every physical explanation, the arguments that it does, the scientific theories that try anyway, and "
            "who, among animals and machines, might have it."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=FEEL, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        head = label(r"Four questions about experience", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"what it is", r"the felt quality of seeing red or tasting coffee: \ is it one more thing to explain, "
                            r"\ or the thing that cannot be?", FEEL),
            (r"why it resists", r"every physical fact seems compatible with its absence: \ does that show anything "
                                r"about the world?", BAD),
            (r"how it works", r"a workspace, \ a higher-order state, \ integrated information, \ a prediction: \ "
                              r"which theory, \ and how could we test it?", FUNC),
            (r"who has it", r"other people, \ octopuses, \ bees, \ a language model: \ how could we tell?", PRED),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Four questions run through it. <bookmark mark='a'/>What experience is: the felt quality of seeing red "
            "or tasting coffee. Is it one more thing for science to explain, or the one thing it cannot? "
            "<bookmark mark='b'/>Why it resists: every physical fact seems compatible with its absence. Does that "
            "show something about the world, or only about our concepts? This is the hard problem, this part's "
            "brick in the Wall. <bookmark mark='c'/>How it works: a global workspace, a higher-order state, "
            "integrated information, a prediction. Which theory, and how could we tell? "
            "<bookmark mark='d'/>And who has it: other people, octopuses, bees, perhaps a language model."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Nagel's bat; \ access and phenomenal consciousness",
            r"the hard problem \ (the Wall); \ Mary's room, \ as an epistemic model",
            r"zombies: \ a two-dimensional matrix, \ computed; \ the zombie argument's Price List",
            r"the explanatory gap; \ phenomenal concepts; \ illusionism, \ with a self-model built",
            r"panpsychism, \ Russellian monism, \ and the combination problem",
            r"a global workspace that ignites, \ built; \ higher-order theories and blindsight, \ simulated",
            r"integrated information, \ computed; \ Aaronson's objection and the unfolding argument",
            r"an active-inference agent, \ built; \ the theories tested; \ animals and machines",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Nagel's bat, and Ned Block's two kinds of consciousness. "
            "<bookmark mark='b'/>The hard problem, this part's brick in the Wall, and Mary's room, as a model of what "
            "she can rule out. <bookmark mark='c'/>Zombies, with the two-dimensional matrix from Part 22 computed, "
            "and the zombie argument's Price List. <bookmark mark='d'/>The explanatory gap, phenomenal concepts, and "
            "illusionism, with a self-model the Reasoner builds. <bookmark mark='e'/>Panpsychism, and the problem of "
            "combining minds. <bookmark mark='f'/>Then the science: a global workspace that ignites, and "
            "higher-order theories, with blindsight simulated. <bookmark mark='g'/>Integrated information, "
            "computed, and two objections to it, computed too. <bookmark mark='h'/>An agent that minimizes free "
            "energy; the great experiment that tested the theories; and the question of animals and machines."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
