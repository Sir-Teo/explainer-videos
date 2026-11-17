from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class Care(VoiceoverScene):
    def construct(self):
        card_section(self, 8, r"Machines as helpers and companions", r"Can a chatbot help, \ and what would show it?",
                     scale=("person",))
        self.evidence()
        self.design()
        self.standards()

    def evidence(self):
        rows_section(self, r"The trial evidence so far", [
            (r"scripted chatbots delivering CBT exercises: \ small, \ short trials with modest improvements against "
             r"information-only controls", WHITE),
            (r"Heinz and colleagues, \ 2025: \ a generative chatbot built for therapy, \ randomized against a waiting "
             r"list, \ about 200 adults: \ larger falls in depression and anxiety symptoms during the trial", GOOD),
            (r"waiting-list controls flatter any treatment (Part 42); \ no trial yet against a human therapist or "
             r"an active control", AUTH),
            (r"companion apps: \ many users report less loneliness; \ heavy use goes with more loneliness in some "
             r"studies, \ and the direction is unknown", MODEL),
        ], "Can a chatbot help, and what would show it? <bookmark mark='a'/> Scripted chatbots that deliver CBT "
           "exercises have been tested in small, short trials, with modest improvements against information-only "
           "controls. <bookmark mark='b'/> In 2025 Michael Heinz and colleagues randomized about two hundred adults to "
           "a generative chatbot built for therapy, or to a waiting list, and found larger falls in depression and "
           "anxiety symptoms during the trial. <bookmark mark='c'/> But waiting-list controls flatter any treatment, "
           "as Part 42 showed, and there's no trial yet against a human therapist or an active control. "
           "<bookmark mark='d'/> Companion apps: many users report less loneliness, but heavy use goes with more "
           "loneliness in some studies, and the direction of cause is unknown.",
           tag=published_tag(r"Heinz et al.\ (2025)"))

    def standards(self):
        chips_section(self, r"What Part 42's standards require", [
            (r"an active control", r"the comparison a patient would otherwise get, \ not a waiting list", GOOD),
            (r"lasting outcomes", r"months, \ measured by people blind to the arm", MODEL),
            (r"harms counted", r"wrong advice, \ dependence, \ privacy, \ and how the system responds when someone "
                               r"needs urgent help", AUTH),
            (r"who it reaches", r"whether it adds care for people who had none, \ or replaces care for people who "
                                r"had some", PERSON),
        ], "So what do Part 42's standards require? <bookmark mark='a'/> An active control: the comparison a patient "
           "would otherwise get, not a waiting list. <bookmark mark='b'/> Lasting outcomes, measured over months by "
           "people blind to the arm. <bookmark mark='c'/> Harms counted: wrong advice, dependence, privacy, and how "
           "the system responds when someone needs urgent help. <bookmark mark='d'/> And who it reaches: whether it "
           "adds care for people who had none, or replaces care for people who had some.",
           foot=r"if you need help now, \ contact local emergency services, \ or find a free line at findahelpline.com")

    def design(self):
        chips_section(self, r"A helper that hands over", [
            (r"scope", r"say what it is for (practising a skill, \ tracking mood) and what it is not (diagnosis, \ "
                       r"emergencies)", MODEL),
            (r"escalation", r"detect when a person needs more than it can give, \ and connect them to a person, \ "
                            r"tested like any classifier for misses", AUTH),
            (r"comparison", r"judged against an active control, \ not a waiting list (Part 42), \ on outcomes "
                            r"measured weeks later", GOOD),
            (r"privacy", r"what people tell it is health data: \ stored, \ shared and deleted under the same rules "
                         r"as a clinic's", PERSON),
        ], "What would a well-designed helper look like? <bookmark mark='a'/> Scope: it says what it's for, such as "
           "practising a skill or tracking mood, and what it isn't for, such as diagnosis or emergencies. "
           "<bookmark mark='b'/> Escalation: it detects when a person needs more than it can give, and connects them "
           "to a person, and that detector is tested like any classifier, for its misses. <bookmark mark='c'/> "
           "Comparison: it's judged against an active control, not a waiting list, as Part 42 required, on outcomes "
           "measured weeks later. <bookmark mark='d'/> And privacy: what people tell it is health data, stored, "
           "shared and deleted under the same rules as a clinic's.", chip_w=3.4, text_w=8.8)
