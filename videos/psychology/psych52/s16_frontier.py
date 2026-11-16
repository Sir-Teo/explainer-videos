from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card_section(self, 15, r"Frontier: \ simulated users", r"Can a model of a person test a design for us?",
                     scale=("person", "society"))
        self.new()
        self.open()

    def new(self):
        chips_section(self, r"What is new", [
            (r"end-to-end users", r"cognitive architectures that see the screen, \ move a simulated hand and make "
                                  r"errors, \ run on a design before anyone builds it", MODEL),
            (r"learned users", r"reinforcement-learning agents bounded by human limits (computational rationality) "
                               r"used to optimize layouts and keyboards", PERSON),
            (r"language models as users", r"simulated participants answering surveys or trying an interface: \ cheap, "
                                          r"\ and of unknown fidelity (Part 46's warning)", AUTH),
            (r"evaluating AI interfaces", r"the human with the assistant as the unit: \ time, \ errors and over-reliance, "
                                         r"\ not the model's benchmark", GOOD),
        ], "Can a model of a person test a design for us? <bookmark mark='a'/> Cognitive architectures can now see a "
           "screen, move a simulated hand and make errors, and run on a design before anyone builds it. "
           "<bookmark mark='b'/> Reinforcement-learning agents, bounded by human limits, an approach called "
           "computational rationality, are used to optimize layouts and keyboards. <bookmark mark='c'/> Language "
           "models are offered as simulated users, answering surveys or trying an interface. They're cheap, and of "
           "unknown fidelity, which was Part 46's warning. <bookmark mark='d'/> And evaluating AI interfaces means "
           "measuring the human with the assistant: time, errors and over-reliance, not the model's benchmark score.",
           chip_w=4.0, text_w=8.2)

    def open(self):
        chips_section(self, r"Open problems", [
            (r"fidelity", r"how close must a simulated user be before its verdict on a design can be trusted?", MODEL),
            (r"errors", r"models of time are good; \ models of errors and learning are much weaker", AUTH),
            (r"long-term use", r"habits, \ fatigue and trust over months, \ not one session", PERSON),
            (r"whose user", r"simulated users built from one population may design for that population only", GOOD),
        ], "And the open problems. <bookmark mark='a'/> Fidelity: how close must a simulated user be before its "
           "verdict on a design can be trusted? <bookmark mark='b'/> Errors: models of time are good, and models of "
           "errors and learning are much weaker. <bookmark mark='c'/> Long-term use: habits, fatigue and trust over "
           "months, not one session. <bookmark mark='d'/> And whose user: simulated users built from one population "
           "may design for that population only.")
