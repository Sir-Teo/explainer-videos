from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Heart(VoiceoverScene):
    def construct(self):
        card_section(self, 12, r"Personality and the heart", r"Does a hurried, \ competitive personality cause heart "
                     r"attacks?", scale=("person",))
        self.typea()
        self.maids()

    def typea(self):
        rows_section(self, r"Type A", [
            (r"1950s: \ two cardiologists, \ Meyer Friedman and Ray Rosenman, \ described the ``Type A'' pattern: \ "
             r"hurried, \ competitive, \ hostile", WHITE),
            (r"the Western Collaborative Group Study followed about 3,000 men; \ Type A men had about twice the rate "
             r"of heart disease", PERSON),
            (r"later and larger studies found no reliable association for Type A as a whole", AUTH),
            (r"hostility, \ one component, \ kept a smaller association; \ and some of the early research was later "
             r"found to have been funded by the tobacco industry, \ which favoured personality explanations", MODEL),
            (r"the Ledger: \ failed, \ with hostility remaining, \ weaker", YOU),
        ], "Does a hurried, competitive personality cause heart attacks? <bookmark mark='a'/> In the nineteen fifties "
           "two cardiologists, Meyer Friedman and Ray Rosenman, described the Type A pattern: hurried, competitive "
           "and hostile. <bookmark mark='b'/> The Western Collaborative Group Study followed about three thousand men, "
           "and Type A men had about twice the rate of heart disease. <bookmark mark='c'/> Later and larger studies "
           "found no reliable association for Type A as a whole. <bookmark mark='d'/> Hostility, one component, kept "
           "a smaller association. And some of the early research was later found to have been funded by the tobacco "
           "industry, which favoured personality explanations. <bookmark mark='e'/> The Ledger says failed, with "
           "hostility remaining, weaker.", tag=historical_tag(r"Friedman \& Rosenman (1959)"))

    def maids(self):
        rows_section(self, r"Exercise by mindset?", [
            (r"Crum and Langer, \ 2007: \ hotel room attendants told that their work met recommendations for "
             r"exercise lost a little weight and lowered their blood pressure over four weeks", WHITE),
            (r"84 women in seven hotels, \ assigned by hotel, \ with no measure of what they actually did at work or "
             r"after it", AUTH),
            (r"a striking idea, \ widely cited, \ never replicated at a larger scale", PERSON),
            (r"the Ledger: \ contested; \ the expectation account of chapter four makes it plausible, \ and "
             r"plausible is not tested", YOU),
        ], "Here's a newer claim about mindset and the body. <bookmark mark='a'/> In 2007 Alia Crum and Ellen Langer "
           "told hotel room attendants that their work met the recommendations for exercise. Over four weeks they lost "
           "a little weight and their blood pressure fell. <bookmark mark='b'/> But there were eighty-four women in "
           "seven hotels, assigned by hotel, with no measure of what they actually did at work or after it. "
           "<bookmark mark='c'/> It's a striking idea, widely cited, and never replicated at a larger scale. "
           "<bookmark mark='d'/> The Ledger says contested. The expectation account of chapter four makes it "
           "plausible, and plausible isn't tested.", tag=published_tag(r"Crum \& Langer (2007)"))
