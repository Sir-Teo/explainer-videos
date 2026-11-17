from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403


class Ethics(VoiceoverScene):
    def construct(self):
        card_section(self, 3, r"Ethics as practice", r"What does a researcher owe the people studied?",
                     scale=("society",))
        self.belmont()
        self.data()
        self.failures()

    def belmont(self):
        chips_section(self, r"The Belmont principles, \ applied", [
            (r"respect for persons", r"informed consent, \ the right to stop, \ extra protection for those who "
                                     r"cannot consent for themselves", MODEL),
            (r"beneficence", r"minimize harm, \ and weigh what remains against what will be learned", GOOD),
            (r"justice", r"the burdens and benefits of research shared fairly, \ not borne by the convenient", PERSON),
            (r"data", r"open data that protects people: \ consent for sharing, \ removal of identifiers, \ access "
                      r"rules for what cannot be made safe", SYMP),
        ], "What does a researcher owe the people studied? The Belmont Report of 1979 named three principles. "
           "<bookmark mark='a'/> Respect for persons: informed consent, the right to stop, and extra protection for "
           "those who can't consent for themselves. <bookmark mark='b'/> Beneficence: minimize harm, and weigh what "
           "remains against what will be learned. <bookmark mark='c'/> Justice: the burdens and benefits of research "
           "shared fairly, not borne by whoever is convenient. <bookmark mark='d'/> And today, data: open data that "
           "protects people, with consent for sharing, identifiers removed, and access rules for what can't be made "
           "safe. This dissertation uses only data that was published openly, with consent, for reuse.",
           tag=historical_tag(r"Belmont Report (1979)"))

    def failures(self):
        rows_section(self, r"The profession's failures, \ and its codes", [
            (r"Part 2 met the studies that changed the rules: \ deception without debriefing, \ distress without "
             r"consent", WHITE),
            (r"2015: \ an independent review commissioned by the American Psychological Association found that its "
             r"officials had kept its ethics policy in line with military interrogation practice", AUTH),
            (r"the association changed its policy to bar psychologists from national-security interrogations", GOOD),
            (r"codes exist because good intentions were not enough; \ ethics is a practice, \ checked by others", YOU),
        ], "The profession has failed, and its codes record the failures. <bookmark mark='a'/> Part 2 met the "
           "studies that changed the rules: deception without debriefing, and distress without consent. "
           "<bookmark mark='b'/> In 2015 an independent review commissioned by the American Psychological "
           "Association found that its officials had kept its ethics policy in line with military interrogation "
           "practice. <bookmark mark='c'/> The association then changed its policy to bar psychologists from "
           "national-security interrogations. <bookmark mark='d'/> Codes exist because good intentions weren't "
           "enough. Ethics is a practice, checked by others.", tag=historical_tag(r"Hoffman et al.\ (2015)"))

    def data(self):
        chips_section(self, r"Ethics after the session ends", [
            (r"consent for reuse", r"open data needs consent that says so: \ participants agree to what will be "
                                   r"shared, \ with whom, \ and for how long", MODEL),
            (r"de-identification", r"names removed is not anonymous: \ age, \ postcode and a rare answer can identify "
                                   r"a person; \ share at the coarsest level the analysis needs", AUTH),
            (r"this film's data", r"Part 62's analysis uses trial-level data the original authors posted openly, \ "
                                  r"fetched and checked, \ never copied into the course", GOOD),
            (r"the participant's view", r"report back what was found, \ in plain words, \ to the people who gave "
                                        r"the time", PERSON),
        ], "Ethics continues after the session ends. <bookmark mark='a'/> Open data needs consent that says so: "
           "participants agree to what will be shared, with whom, and for how long. <bookmark mark='b'/> Removing "
           "names isn't the same as anonymity. Age, postcode and one rare answer can identify a person, so share at "
           "the coarsest level the analysis needs. <bookmark mark='c'/> This part's analysis uses trial-level data "
           "that the original authors posted openly, fetched and checked, and never copied into the course. "
           "<bookmark mark='d'/> And from the participant's side: report back what was found, in plain words, to "
           "the people who gave their time.", chip_w=3.8, text_w=8.4)
