from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Errors(VoiceoverScene):
    def construct(self):
        card_section(self, 3, r"Slips, \ lapses and mistakes", r"Is every error the same kind of failure?")
        self.kinds()
        self.srk()
        self.blame()

    def kinds(self):
        chips_section(self, r"Three kinds of error", [
            (r"slips", r"the right plan, \ the wrong action: \ the gear lever for the flap lever; \ caught by design "
                       r"(coding, \ interlocks)", SYMP),
            (r"lapses", r"the right plan, \ a step forgotten: \ the fuel cap left off, \ the checklist item skipped "
                        r"after an interruption (Part 19's working memory)", MODEL),
            (r"mistakes", r"the wrong plan, \ carried out well: \ a misdiagnosis, \ a rule applied where it does "
                          r"not fit; \ caught by feedback and other people", PERSON),
            (r"violations", r"a rule broken on purpose, \ often because the rule was unworkable", AUTH),
        ], "Not every error is the same failure. <bookmark mark='a'/> Slips: the right plan, the wrong action, like "
           "the gear lever for the flap lever. Design catches them, with coding and interlocks. "
           "<bookmark mark='b'/> Lapses: the right plan, with a step forgotten. The fuel cap left off, or a checklist "
           "item skipped after an interruption. That's Part 19's working memory. <bookmark mark='c'/> Mistakes: the "
           "wrong plan, carried out well. A misdiagnosis, or a rule applied where it doesn't fit. Feedback and other "
           "people catch them. <bookmark mark='d'/> And violations: a rule broken on purpose, often because the rule "
           "was unworkable. Donald Norman and James Reason drew these lines.",
           tag=published_tag(r"Reason (1990)"))

    def srk(self):
        chips_section(self, r"Skills, \ rules and knowledge", [
            (r"skill-based", r"fluent, \ automatic action: \ fast and accurate, \ and prone to slips when attention "
                             r"wanders", GOOD),
            (r"rule-based", r"``if this, \ then that'': \ procedures and learned patterns; \ errors are good rules "
                            r"misapplied", MODEL),
            (r"knowledge-based", r"reasoning from first principles in a new situation: \ slow, \ effortful, \ and "
                                 r"where most mistakes are made", AUTH),
        ], "Jens Rasmussen added a ladder of control. <bookmark mark='a'/> Skill-based: fluent, automatic action, fast "
           "and accurate, and prone to slips when attention wanders. <bookmark mark='b'/> Rule-based: if this, then "
           "that. Procedures and learned patterns, whose errors are good rules misapplied. <bookmark mark='c'/> "
           "Knowledge-based: reasoning from first principles in a new situation. It's slow and effortful, and it's "
           "where most mistakes are made. An emergency often pushes an operator down this ladder, at the worst "
           "possible moment.")

    def blame(self):
        rows_section(self, r"The old view and the new", [
            (r"the old view: \ the system is safe, \ and human error is the cause of accidents", AUTH),
            (r"the new view: \ human error is a symptom of trouble deeper in the system; \ ask why it made sense at "
             r"the time", GOOD),
            (r"Sidney Dekker: \ hindsight sees the path to the accident; \ the operator saw a forest of possible "
             r"paths", MODEL),
            (r"so the question of this part becomes: \ which design made this error likely?", YOU),
        ], "This changes the question. <bookmark mark='a'/> The old view says the system is safe, and human error is "
           "the cause of accidents. <bookmark mark='b'/> The new view says human error is a symptom of trouble deeper "
           "in the system, so ask why the action made sense at the time. <bookmark mark='c'/> Hindsight sees the path "
           "to the accident, as Sidney Dekker puts it. The operator saw a forest of possible paths. "
           "<bookmark mark='d'/> So this part's question becomes: which design made this error likely?")
