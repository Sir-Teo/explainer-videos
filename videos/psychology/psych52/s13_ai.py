from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Ai(VoiceoverScene):
    def construct(self):
        card_section(self, 12, r"Talking to machines", r"What do people expect from an interface that talks?",
                     scale=("person", "society"))
        self.expect()
        self.repair()

    def expect(self):
        rows_section(self, r"Expectation", [
            (r"Reeves and Nass, \ 1996: \ people apply social rules to computers, \ politeness, \ flattery, \ "
             r"teammates, \ without believing the computer is a person", WHITE),
            (r"a fluent, \ human-sounding reply raises expectations of competence everywhere: \ Part 35's "
             r"mind-reading, \ switched on by language", PERSON),
            (r"the gulf of evaluation widens: \ a wrong answer looks exactly like a right one", AUTH),
            (r"so the interface must show what the system can and cannot do, \ and how sure it is: \ Part 51's "
             r"calibrated trust", YOU),
        ], "What do people expect from an interface that talks? <bookmark mark='a'/> In 1996 Byron Reeves and "
           "Clifford Nass showed that people apply social rules to computers, politeness, flattery and teammates, "
           "without believing the computer is a person. <bookmark mark='b'/> A fluent, human-sounding reply raises "
           "expectations of competence everywhere. It's Part 35's mind-reading, switched on by language. "
           "<bookmark mark='c'/> And the gulf of evaluation widens, because a wrong answer looks exactly like a right "
           "one. <bookmark mark='d'/> So the interface has to show what the system can and can't do, and how sure it "
           "is. That's Part 51's calibrated trust.")

    def repair(self):
        chips_section(self, r"Conversation, \ designed", [
            (r"repair", r"conversations go wrong all the time; \ people fix them with a quick ``you mean?'' \ a good "
                        r"system asks and accepts corrections", GOOD),
            (r"turn-taking", r"Part 23's gaps between turns are about 200 ms; \ a slow reply feels like hesitation", MODEL),
            (r"anthropomorphism", r"a name and a personality increase use and trust, \ whether or not trust is earned",
             AUTH),
            (r"measuring it", r"task success and the cost of errors, \ not how pleasant the conversation felt", PERSON),
        ], "Conversation itself can be designed. <bookmark mark='a'/> Repair: conversations go wrong all the time, "
           "and people fix them with a quick you mean? A good system asks, and accepts corrections. "
           "<bookmark mark='b'/> Turn-taking: Part 23's gaps between turns are about two hundred milliseconds, so a "
           "slow reply feels like hesitation. <bookmark mark='c'/> Anthropomorphism: a name and a personality "
           "increase use and trust, whether or not the trust is earned. <bookmark mark='d'/> And measuring it: task "
           "success and the cost of errors, not how pleasant the conversation felt. Part 60 returns to minds and "
           "machines.")
