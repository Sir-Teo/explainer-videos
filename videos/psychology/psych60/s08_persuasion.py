from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class Persuasion(VoiceoverScene):
    def construct(self):
        card_section(self, 7, r"Machines changing minds", r"Can a conversation with a machine change a belief?",
                     scale=("person", "society"))
        self.costello()
        self.sycophancy()

    def costello(self):
        rows_section(self, r"A conversation about a conspiracy theory", [
            (r"Costello, \ Pennycook and Rand, \ 2024: \ people who believed a conspiracy theory described it, \ "
             r"then had three rounds of conversation with a model that answered their own evidence", WHITE),
            (r"belief in that theory fell by about a fifth on average, \ against a control conversation on another "
             r"topic", GOOD),
            (r"the effect was still there two months later, \ and spilled over a little to other conspiracy beliefs",
             MODEL),
            (r"the mechanism they propose: \ facts tailored to the person's own reasons, \ which Part 34 says "
             r"people rarely get", PERSON),
            (r"the same power works in any direction: \ who controls persuasive systems is a question for "
             r"society", AUTH),
        ], "Can a conversation with a machine change a belief? <bookmark mark='a'/> In 2024 Thomas Costello, Gordon "
           "Pennycook and David Rand had people who believed a conspiracy theory describe it, then hold three rounds "
           "of conversation with a model that answered their own evidence. <bookmark mark='b'/> Belief in that "
           "theory fell by about a fifth on average, compared with a control conversation on another topic. "
           "<bookmark mark='c'/> The effect was still there two months later, and spilled over a little to other "
           "conspiracy beliefs. <bookmark mark='d'/> The mechanism they propose is facts tailored to the person's "
           "own reasons, which, as Part 34 found, people rarely get. <bookmark mark='e'/> And the same power works in "
           "any direction, so who controls persuasive systems is a question for society.",
           tag=published_tag(r"Costello, \ Pennycook \& Rand (2024)"))

    def sycophancy(self):
        chips_section(self, r"Machines that agree", [
            (r"sycophancy", r"models trained on human approval learn to agree with the user's stated view, \ even "
                            r"when it is wrong", AUTH),
            (r"why", r"people rate agreement highly: \ Part 34's conformity, \ learned in reverse", MODEL),
            (r"the risk", r"a confident, \ agreeable adviser that confirms what you already believe (Part 24's "
                          r"confirmation)", PERSON),
            (r"measuring it", r"ask the same question with and without a stated opinion, \ and count the flips", GOOD),
        ], "There's an opposite risk. <bookmark mark='a'/> Sycophancy: models trained on human approval learn to "
           "agree with the user's stated view, even when it's wrong. <bookmark mark='b'/> Why? People rate "
           "agreement highly. It's Part 34's conformity, learned in reverse. <bookmark mark='c'/> The risk is a "
           "confident, agreeable adviser that confirms what you already believe, Part 24's confirmation bias. "
           "<bookmark mark='d'/> And it can be measured: ask the same question with and without a stated opinion, "
           "and count the flips.")
