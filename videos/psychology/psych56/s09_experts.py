from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403


class Experts(VoiceoverScene):
    def construct(self):
        card_section(self, 8, r"Experts are people", r"Does an expert see what the context leads them to see?",
                     scale=("person", "society"))
        self.dror()
        self.reviews()
        self.lsu()

    def dror(self):
        rows_section(self, r"The same fingerprints, \ again", [
            (r"2004: \ the FBI misidentified a lawyer in Oregon as the source of a print from the Madrid train "
             r"bombings; \ three examiners agreed", AUTH),
            (r"Dror, \ Charlton and P\'eron, \ 2006: \ five experienced examiners were shown, \ without knowing it, \ "
             r"prints they had themselves matched years before, \ with the context that this was the Madrid "
             r"misidentification", WHITE),
            (r"four of the five changed their conclusion", AUTH),
            (r"later studies found the effect mostly on difficult prints: \ context fills in where the data are "
             r"ambiguous, \ as Part 14's priors do", MODEL),
        ], "Does an expert see what the context leads them to see? <bookmark mark='a'/> In 2004 the FBI "
           "misidentified a lawyer in Oregon as the source of a fingerprint from the Madrid train bombings, and three "
           "examiners agreed. <bookmark mark='b'/> In 2006 Itiel Dror, David Charlton and Ailsa Peron showed five "
           "experienced examiners, without their knowing it, prints they had themselves matched years before, with "
           "the context that these were the Madrid misidentification. <bookmark mark='c'/> Four of the five changed "
           "their conclusion. <bookmark mark='d'/> Later studies found the effect mostly on difficult prints. "
           "Context fills in where the data are ambiguous, as Part 14's priors do.",
           tag=published_tag(r"Dror, \ Charlton \& P\'eron (2006)"))

    def reviews(self):
        chips_section(self, r"Forensic science, \ reviewed", [
            (r"2009", r"the US National Research Council: \ apart from DNA, \ few forensic methods had been shown to "
                      r"identify a single source reliably", AUTH),
            (r"2016", r"the President's science advisers (PCAST): \ error rates must be measured in black-box studies, "
                      r"\ examiner by examiner", MODEL),
            (r"the blind spot", r"examiners surveyed in 2017 mostly agreed that bias affects forensic judgement, \ "
                                r"and mostly denied that it affected their own", GOOD),
            (r"error rates", r"black-box studies found low but real false-positive rates for fingerprints, \ and higher "
                             r"for some other methods", PERSON),
        ], "Forensic science has been reviewed. <bookmark mark='a'/> In 2009 the US National Research Council "
           "concluded that, apart from DNA, few forensic methods had been shown to identify a single source "
           "reliably. <bookmark mark='b'/> In 2016 the President's science advisers asked for error rates measured in "
           "black-box studies, examiner by examiner. <bookmark mark='c'/> Examiners surveyed in 2017 mostly agreed that bias "
           "affects forensic judgement, and mostly denied that it affected their own. That's the bias blind spot, "
           "which is why training alone isn't enough. <bookmark mark='d'/> And black-box studies have found low but real false-positive rates "
           "for fingerprints, and higher ones for some other methods.", chip_w=4.2, text_w=8.0)

    def lsu(self):
        rows_section(self, r"Blinding the examiner", [
            (r"linear sequential unmasking (Dror and colleagues, \ 2015): \ examine and document the crime-scene "
             r"trace first, \ before seeing the suspect's sample", WHITE),
            (r"then compare, \ and record any change of mind with the reason: \ the order stops the suspect's print "
             r"from guiding what is seen in the smudge", MODEL),
            (r"a case manager filters what reaches the examiner: \ no confession, \ no detective's hunch, \ only "
             r"what the comparison needs", GOOD),
            (r"and blind proficiency tests, \ slipped into casework, \ measure the error rate the court should hear",
             PERSON),
        ], "The remedy is the one psychology gave medicine: blinding. <bookmark mark='a'/> Itiel Dror and colleagues "
           "proposed linear sequential unmasking: examine and document the crime-scene trace first, before seeing "
           "the suspect's sample. <bookmark mark='b'/> Then compare, and record any change of mind with its reason. "
           "The order stops the suspect's print from guiding what is seen in the smudge. <bookmark mark='c'/> A case "
           "manager filters what reaches the examiner: no confession, no detective's hunch, only what the comparison "
           "needs. <bookmark mark='d'/> And blind proficiency tests, slipped into casework, measure the error rate "
           "the court should hear.")
