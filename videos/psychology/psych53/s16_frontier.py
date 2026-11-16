from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card_section(self, 15, r"Frontier: \ new assessments, \ old questions", r"Do new ways of assessing people "
                     r"predict better?", scale=("society",))
        self.new()
        self.open()

    def new(self):
        chips_section(self, r"What is new", [
            (r"game-based assessment", r"puzzles and games scored for traits and abilities: \ engaging, \ and with "
                                       r"thin evidence of validity for performance", MODEL),
            (r"automated interviews", r"video or text answers scored by models: \ structure is built in, \ but what "
                                      r"the score measures needs the old validation", PERSON),
            (r"language-model scoring", r"essays and work samples rated by models: \ reliable, \ fast, \ and able to "
                                        r"inherit the biases of the ratings they learned from", AUTH),
            (r"performance without ratings", r"objective records and many raters instead of one annual rating: \ a "
                                             r"better criterion would change every validity in this part", GOOD),
        ], "Do new ways of assessing people predict better? <bookmark mark='a'/> Game-based assessments score puzzles "
           "and games for traits and abilities. They're engaging, and their evidence of validity for job performance "
           "is thin. <bookmark mark='b'/> Automated interviews score video or text answers with models. Structure is "
           "built in, but what the score measures needs the old validation. <bookmark mark='c'/> Language models "
           "score essays and work samples. They're reliable and fast, and they can inherit the biases of the ratings "
           "they learned from. <bookmark mark='d'/> And performance without ratings: objective records and many "
           "raters instead of one annual rating. A better criterion would change every validity in this part.",
           chip_w=4.2, text_w=8.0)

    def open(self):
        chips_section(self, r"Open problems", [
            (r"corrections", r"how restricted were the samples behind each validity? \ the 2022 argument is not "
                             r"settled", MODEL),
            (r"remote and hybrid work", r"long-run effects on promotion, \ learning and innovation, \ not just "
                                        r"output", PERSON),
            (r"algorithmic fairness", r"which definition of fairness a hiring model should meet, \ when they conflict",
             AUTH),
            (r"validity over time", r"jobs change faster than validation studies are run", GOOD),
        ], "And the open problems. <bookmark mark='a'/> Corrections: how restricted were the samples behind each "
           "validity? The argument of 2022 isn't settled. <bookmark mark='b'/> Remote and hybrid work: the long-run "
           "effects on promotion, learning and innovation, not just output. <bookmark mark='c'/> Algorithmic "
           "fairness: which definition of fairness a hiring model should meet, when the definitions conflict. "
           "<bookmark mark='d'/> And validity over time, because jobs change faster than validation studies are run.")
