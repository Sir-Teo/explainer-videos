from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403


class Where(VoiceoverScene):
    def construct(self):
        card_section(self, 12, r"Where to go", r"What next?", scale=("person",))
        self.reading()
        self.skills()

    def reading(self):
        chips_section(self, r"Reading, \ by direction", [
            (r"the brain", r"Kandel and colleagues, \ \emph{Principles of Neural Science}; \ Dayan and Abbott, \ "
                           r"\emph{Theoretical Neuroscience}", MODEL),
            (r"the mind's models", r"Busemeyer and Diederich, \ \emph{Cognitive Modeling}; \ Farrell and "
                                   r"Lewandowsky, \ \emph{Computational Modeling of Cognition and Behavior}", PERSON),
            (r"measurement", r"Borsboom, \ \emph{Measuring the Mind}; \ McElreath, \ \emph{Statistical Rethinking}",
             GOOD),
            (r"people and societies", r"Henrich, \ \emph{The WEIRDest People in the World}; \ Kahneman, \ "
                                      r"\emph{Thinking, Fast and Slow}, \ read with this series' Ledger beside it", SYMP),
            (r"the clinic", r"Barlow (ed.), \ \emph{Clinical Handbook of Psychological Disorders}; \ the care "
                            r"chapters of Parts 39 to 42 and 57", CARE),
        ], "What next? Here is reading, by direction. <bookmark mark='a'/> For the brain: Kandel and colleagues' "
           "Principles of Neural Science, and Dayan and Abbott's Theoretical Neuroscience. <bookmark mark='b'/> For "
           "the mind's models: Busemeyer and Diederich's Cognitive Modeling, and Farrell and Lewandowsky's "
           "Computational Modeling of Cognition and Behavior. <bookmark mark='c'/> For measurement: Borsboom's "
           "Measuring the Mind, and McElreath's Statistical Rethinking. <bookmark mark='d'/> For people and "
           "societies: Henrich's The WEIRDest People in the World, and Kahneman's Thinking, Fast and Slow, read with "
           "this series' Ledger beside it. <bookmark mark='e'/> And for the clinic: Barlow's Clinical Handbook of "
           "Psychological Disorders, with the care chapters of Parts 39 to 42 and 57.", chip_w=3.4, text_w=8.8,
           font_size=20)

    def skills(self):
        chips_section(self, r"What travels from this course", [
            (r"design", r"a comparison that rules out the boring explanations: \ randomization, \ blinding, \ the "
                        r"right control (Part 2)", GOOD),
            (r"measurement", r"asking how reliable and how valid before asking how big (Part 3)", MODEL),
            (r"inference", r"power, \ intervals, \ forking paths and the denominator (Parts 4 and 50)", PERSON),
            (r"models", r"writing an idea as code, \ fitting it, \ and asking what it rules out (Part 48)", CROWD),
            (r"judgement", r"reading a claim, \ yours included, \ against its Ledger row", YOU),
        ], "What travels from this course, whatever you do next? <bookmark mark='a'/> Design: a comparison that rules "
           "out the boring explanations, with randomization, blinding and the right control, from Part 2. "
           "<bookmark mark='b'/> Measurement: asking how reliable and how valid before asking how big, from Part 3. "
           "<bookmark mark='c'/> Inference: power, intervals, forking paths and the denominator, from Parts 4 and "
           "50. <bookmark mark='d'/> Models: writing an idea as code, fitting it, and asking what it rules out, from "
           "Part 48. <bookmark mark='e'/> And judgement: reading any claim, your own included, against its Ledger "
           "row.", chip_w=3.4, text_w=8.8)
