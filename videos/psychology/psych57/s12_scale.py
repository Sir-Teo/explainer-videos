from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Scale(VoiceoverScene):
    def construct(self):
        card_section(self, 11, r"Help at scale", r"Who else can deliver care?", scale=("society",))
        self.bench()
        self.digital()

    def bench(self):
        rows_section(self, r"The Friendship Bench", [
            (r"Zimbabwe: \ a country with very few psychiatrists; \ Dixon Chibanda trained lay health workers, \ "
             r"often older women, \ to deliver problem-solving therapy on a wooden bench outside clinics", WHITE),
            (r"Chibanda and colleagues, \ 2016: \ a cluster-randomized trial in Harare; \ at six months, \ far "
             r"fewer people in the Friendship Bench arm still had high symptom scores than with enhanced usual "
             r"care", GOOD),
            (r"task-sharing: \ trained, \ supervised non-specialists delivering structured therapy, \ tested in "
             r"trials across many countries", MODEL),
            (r"the evidence for task-sharing is among the strongest answers to the treatment gap", YOU),
        ], "Who else can deliver care? <bookmark mark='a'/> Zimbabwe has very few psychiatrists. Dixon Chibanda "
           "trained lay health workers, often older women, to deliver problem-solving therapy on a wooden bench "
           "outside clinics. <bookmark mark='b'/> In 2016 Chibanda and colleagues reported a cluster-randomized trial "
           "in Harare. At six months, far fewer people in the Friendship Bench arm still had high symptom scores than "
           "with enhanced usual care. <bookmark mark='c'/> This is task-sharing: trained, supervised non-specialists "
           "delivering structured therapy, tested in trials across many countries. <bookmark mark='d'/> The evidence "
           "for task-sharing is among the strongest answers to the treatment gap.",
           tag=published_tag(r"Chibanda et al.\ (2016)"))

    def digital(self):
        chips_section(self, r"Digital therapeutics", [
            (r"trial evidence", r"internet CBT with some human guidance works about as well as face-to-face for "
                                r"depression and anxiety in trials", GOOD),
            (r"the engagement cliff", r"outside trials, \ most people who download a mental health app stop using it "
                                      r"within weeks", AUTH),
            (r"business", r"a company with a prescription app cleared by the US regulator went bankrupt in 2023: \ "
                          r"evidence did not guarantee payment", PERSON),
            (r"privacy", r"in 2023 the US Federal Trade Commission acted against an online therapy company for "
                         r"sharing users' health information with advertisers", MODEL),
        ], "And digital therapeutics? <bookmark mark='a'/> Internet-delivered CBT with some human guidance works "
           "about as well as face-to-face therapy for depression and anxiety, in trials. <bookmark mark='b'/> But "
           "there's an engagement cliff. Outside trials, most people who download a mental health app stop using it "
           "within weeks. <bookmark mark='c'/> A company whose prescription app was cleared by the US regulator went "
           "bankrupt in 2023. Evidence didn't guarantee payment. <bookmark mark='d'/> And in 2023 the US Federal "
           "Trade Commission acted against an online therapy company for sharing users' health information with "
           "advertisers.", chip_w=3.8, text_w=8.4)
