from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card_section(self, 14, r"In practice: \ a stepped-care service, \ planned", r"How many therapists does a "
                     r"town need?", scale=("society",))
        self.where()
        self.plan()

    def where(self):
        chips_section(self, r"Where this is a job", [
            (r"health psychology", r"behaviour change in chronic illness: \ adherence, \ rehabilitation, \ pain", MODEL),
            (r"behavioural medicine", r"psychological treatment inside medical care: \ insomnia, \ diabetes "
                                      r"prevention, \ smoking", GOOD),
            (r"service design", r"capacity, \ waiting and pathways in mental health services", PERSON),
            (r"digital health evaluation", r"trials, \ engagement data and privacy review for apps and programmes",
             SYMP),
        ], "Where is this a job? <bookmark mark='a'/> In health psychology: behaviour change in chronic illness, "
           "adherence, rehabilitation and pain. <bookmark mark='b'/> In behavioural medicine: psychological treatment "
           "inside medical care, for insomnia, diabetes prevention and smoking. <bookmark mark='c'/> In service "
           "design: capacity, waiting and pathways in mental health services. <bookmark mark='d'/> And in digital "
           "health evaluation: trials, engagement data, and privacy review for apps and programmes.")

    def plan(self):
        d = load("care")
        rows_section(self, r"A worked capacity plan", [
            (r"demand: \ 100 referrals a week; \ about 70\% mild to moderate, \ 30\% severe; \ the target: \ most "
             r"people starting treatment within two weeks", WHITE),
            (r"flow: \ everyone starts at the step that suits them; \ guided self-help courses of 6 weeks, \ therapy "
             r"of 12; \ about six in ten step up", MODEL),
            (r"capacity: \ each week's starts must at least match each week's arrivals at each step, \ or a queue "
             r"grows without limit: \ about 100 self-help starts and about 60 therapy starts a week", PERSON),
            (rf"Psyche's check: \ with 100 and 60 starts, \ the first wait falls to under a week, \ and "
             rf"{100 * d['recovered_26'][3]:.0f}\% recover within six months", GOOD),
            (r"then measure every session, \ flag the off-track, \ and publish the service's own recovery rates", YOU),
        ], "Here's a worked capacity plan. <bookmark mark='a'/> Demand is a hundred referrals a week, about seventy "
           "percent mild to moderate and thirty severe, and the target is for most people to start treatment within "
           "two weeks. <bookmark mark='b'/> In the flow, everyone starts at the step that suits them: guided "
           "self-help courses of six weeks and therapy of twelve, with about six in ten stepping up. <bookmark mark='c'/> "
           "For capacity, each week's starts must at least match each week's arrivals at each step, or a queue grows "
           "without limit. That means about a hundred self-help starts and about sixty therapy starts a week. "
           "<bookmark mark='d'/> Psyche's check: with a hundred self-help starts and sixty therapy starts, the first wait falls to under a "
           "week, and about three quarters recover within six months. <bookmark mark='e'/> Then measure every session, flag "
           "the off-track, and publish the service's own recovery rates.", tag=psyche_tag(r"\texttt{work.stepped\_care}"))
