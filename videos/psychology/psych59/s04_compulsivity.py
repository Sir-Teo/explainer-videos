from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403


class Compulsivity(VoiceoverScene):
    def construct(self):
        card_section(self, 3, r"Compulsivity and model-based control", r"Is compulsion a habit that planning cannot "
                     r"override?")
        self.gillan()
        self.caveats()

    def gillan(self):
        rows_section(self, r"Fourteen hundred people online", [
            (r"Part 17's two-step task separates model-free learning (repeat what was rewarded) from model-based "
             r"planning (use the task's structure)", WHITE),
            (r"Gillan and colleagues, \ 2016: \ about 1,400 online participants did the task and many symptom "
             r"questionnaires", MODEL),
            (r"factor analysis of the questionnaires found three transdiagnostic dimensions; \ one, \ compulsive "
             r"behaviour and intrusive thought, \ went with less model-based control", GOOD),
            (r"the link was with a dimension that cuts across diagnoses (Part 39), \ not with any one diagnosis", PERSON),
        ], "Is compulsion a habit that planning can't override? <bookmark mark='a'/> Part 17's two-step task separates "
           "model-free learning, repeating what was rewarded, from model-based planning, which uses the task's "
           "structure. <bookmark mark='b'/> In 2016 Claire Gillan and colleagues had about fourteen hundred online "
           "participants do the task and many symptom questionnaires. <bookmark mark='c'/> A factor analysis of the "
           "questionnaires found three transdiagnostic dimensions. One, compulsive behaviour and intrusive thought, "
           "went with less model-based control. <bookmark mark='d'/> The link was with a dimension that cuts across "
           "diagnoses, as in Part 39, not with any one diagnosis.", tag=published_tag(r"Gillan et al.\ (2016)"))

    def caveats(self):
        d = load("attenuate")
        chips_section(self, r"What limits it", [
            (r"size", r"the association is small: \ it describes a population, \ not a patient (Part 47)", AUTH),
            (r"reliability", rf"the two-step task's model-based index has modest retest reliability; \ a true "
                             rf"correlation of 0.5 measured with reliabilities 0.4 and 0.8 shows as "
                             rf"{d['observed'][1]:.2f}", MODEL),
            (r"replication", r"the online finding has replicated in further online and clinical samples", GOOD),
            (r"the next step", r"show that changing model-based control changes compulsion: \ an intervention, \ not "
                               r"a correlation", PERSON),
        ], "What limits it? <bookmark mark='a'/> Size: the association is small. It describes a population, not a "
           "patient, which is Part 47's point. <bookmark mark='b'/> Reliability: the task's model-based index has "
           "modest retest reliability. A true correlation of zero point five, measured with reliabilities of zero "
           "point four and zero point eight, shows as about zero point two eight. <bookmark mark='c'/> Replication: "
           "the online finding has replicated in further online and clinical samples. <bookmark mark='d'/> And the "
           "next step is to show that changing model-based control changes compulsion. That needs an intervention, "
           "not a correlation.")
