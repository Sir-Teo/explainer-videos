from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card_section(self, 14, r"In practice: \ the roles", r"Where does this series lead, \ as work?",
                     scale=("society",))
        self.roles()

    def roles(self):
        chips_section(self, r"Roles, \ and the parts that prepare for them", [
            (r"research", r"academic and industry research: \ Acts I, \ XI and XIII", MODEL),
            (r"the clinic", r"clinical psychology and psychiatry's allied professions, \ with their own training "
                            r"and licensing: \ Act X and Part 57", CARE),
            (r"people and products", r"user research, \ human factors and design: \ Parts 51 and 52", PERSON),
            (r"organizations and policy", r"selection, \ education, \ behavioural policy, \ law: \ Parts 53 to 56",
             GOOD),
            (r"measurement and data", r"psychometrics, \ experimentation, \ evaluation of AI: \ Parts 44 to 50 and "
                                      r"60", SYMP),
        ], "Where does this series lead, as work? <bookmark mark='a'/> To research, in universities and in industry: "
           "Acts One, Eleven and Thirteen. <bookmark mark='b'/> To the clinic: clinical psychology and the allied "
           "professions, each with its own training and licensing, prepared for by Act Ten and Part 57. "
           "<bookmark mark='c'/> To people and products: user research, human factors and design, Parts 51 and 52. "
           "<bookmark mark='d'/> To organizations and policy: selection, education, behavioural policy and law, "
           "Parts 53 to 56. <bookmark mark='e'/> And to measurement and data: psychometrics, experimentation, and "
           "the evaluation of AI, Parts 44 to 50 and 60.", chip_w=3.8, text_w=8.4)
