from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403


class Learning(VoiceoverScene):
    def construct(self):
        card_section(self, 11, r"Learning rules", r"How does a brain learn what to predict?", scale=("brain",),
                     marr=("how",))
        self.backprop()
        self.meta()

    def backprop(self):
        chips_section(self, r"Backpropagation and the brain", [
            (r"the problem", r"deep networks learn by sending exact error gradients backward through every "
                             r"synapse; \ neurons cannot obviously do that", WHITE),
            (r"feedback alignment", r"random backward weights still teach a network (Lillicrap and colleagues, \ "
                                    r"2016)", MODEL),
            (r"predictive coding", r"its error units, \ settled, \ approximate backpropagation's gradients "
                                   r"(Whittington and Bogacz, \ 2017)", PERSON),
            (r"the review", r"Lillicrap and colleagues, \ 2020: \ the brain may approximate it with local signals "
                            r"and feedback; \ untested in detail", GOOD),
        ], "How does a brain learn what to predict? <bookmark mark='a'/> Deep networks learn by sending exact error "
           "gradients backward through every synapse, and neurons can't obviously do that. <bookmark mark='b'/> But "
           "random backward weights still teach a network, which Timothy Lillicrap and colleagues called feedback "
           "alignment. <bookmark mark='c'/> And predictive coding's error units, once settled, approximate "
           "backpropagation's gradients, as James Whittington and Rafal Bogacz showed. <bookmark mark='d'/> In a "
           "2020 review, Lillicrap and colleagues argued the brain may approximate backpropagation with local "
           "signals and feedback. It hasn't been tested in detail.", tag=published_tag(r"Lillicrap et al.\ (2020)"))

    def meta(self):
        rows_section(self, r"Learning to learn", [
            (r"Part 17's dopamine prediction error trains slow weights in prefrontal cortex", WHITE),
            (r"Wang and colleagues, \ 2018: \ a recurrent network trained this way learns, \ in its activity, \ a "
             r"fast learning algorithm of its own", MODEL),
            (r"it reproduced Harlow's ``learning sets'': \ monkeys that get faster at each new problem of a kind", GOOD),
            (r"the same idea runs today's language models: \ learning from examples in the prompt, \ without "
             r"changing a weight (Part 60)", YOU),
        ], "There's a second kind of learning. <bookmark mark='a'/> Part 17's dopamine prediction error trains slow "
           "weights in prefrontal cortex. <bookmark mark='b'/> In 2018 Jane Wang and colleagues showed that a "
           "recurrent network trained this way learns, in its activity, a fast learning algorithm of its own. "
           "<bookmark mark='c'/> It reproduced Harry Harlow's learning sets: monkeys that get faster at each new "
           "problem of a kind. <bookmark mark='d'/> The same idea runs today's language models, which learn from "
           "examples in the prompt without changing a weight. That's Part 60.")
