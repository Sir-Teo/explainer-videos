from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class Behaviour(VoiceoverScene):
    def construct(self):
        card_section(self, 12, r"A science of machine behaviour", r"What does psychology bring?", scale=("society",))
        self.rahwan()
        self.toolkit()

    def rahwan(self):
        rows_section(self, r"Machine behaviour", [
            (r"Rahwan and colleagues, \ 2019: \ study machines as animals are studied: \ their behaviour in the "
             r"wild, \ its development, \ its function, \ its evolution", WHITE),
            (r"engineers know the code but not the behaviour that emerges from training and use", MODEL),
            (r"psychology's century of method fits: \ experiments, \ controls, \ reliability, \ samples, \ "
             r"replication", GOOD),
            (r"and machines change: \ a result is about a model at a date, \ like a Ledger row (Part 4)", AUTH),
        ], "What does psychology bring? <bookmark mark='a'/> In 2019 Iyad Rahwan and colleagues proposed studying "
           "machines as animals are studied: their behaviour in the wild, its development, its function, and its "
           "evolution. <bookmark mark='b'/> Engineers know the code but not the behaviour that emerges from training "
           "and use. <bookmark mark='c'/> Psychology's century of method fits: experiments, controls, reliability, "
           "samples and replication. <bookmark mark='d'/> And machines change, so a result is about a model at a "
           "date, like a Ledger row.", tag=published_tag(r"Rahwan et al.\ (2019)"))

    def toolkit(self):
        chips_section(self, r"The toolkit, \ part by part", [
            (r"Part 2", r"randomize, \ control, \ blind the scorer", MODEL),
            (r"Parts 3 and 45", r"construct validity, \ reliability, \ item response theory", PERSON),
            (r"Part 4", r"preregister, \ count the forking paths, \ report every model tried", AUTH),
            (r"Part 47", r"the model as the subject; \ many models, \ not many prompts", GOOD),
            (r"Part 48", r"compare fitted models of behaviour, \ not single scores", SYMP),
        ], "Here's the toolkit, part by part. <bookmark mark='a'/> Part 2: randomize, control, and blind the scorer. "
           "<bookmark mark='b'/> Parts 3 and 45: construct validity, reliability, and item response theory. "
           "<bookmark mark='c'/> Part 4: preregister, count the forking paths, and report every model tried. "
           "<bookmark mark='d'/> Part 47: the model is the subject, so test many models, not many prompts. "
           "<bookmark mark='e'/> And Part 48: compare fitted models of behaviour, not single scores.")
