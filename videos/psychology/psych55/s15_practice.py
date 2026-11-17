from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card_section(self, 14, r"In practice: \ a trial, \ designed", r"How would you test a letter to a million "
                     r"people?", scale=("society",))
        self.where()
        self.trial()

    def where(self):
        chips_section(self, r"Where this is a job", [
            (r"behavioural insights teams", r"government units that redesign letters, \ forms and services, \ and "
                                            r"test them by trial", MODEL),
            (r"growth and retention", r"product teams running onboarding, \ reminder and pricing experiments", PERSON),
            (r"public health", r"vaccination reminders, \ screening invitations, \ smoking cessation", GOOD),
            (r"policy evaluation", r"what persists after the trial, \ and what it costs per unit of change", SYMP),
        ], "Where is this a job? <bookmark mark='a'/> In behavioural insights teams: government units that redesign "
           "letters, forms and services, and test them by trial. <bookmark mark='b'/> In growth and retention, where "
           "product teams run onboarding, reminder and pricing experiments. <bookmark mark='c'/> In public health: "
           "vaccination reminders, screening invitations, smoking cessation. <bookmark mark='d'/> And in policy "
           "evaluation: what persists after the trial, and what it costs per unit of change.")

    def trial(self):
        rows_section(self, r"A worked trial: \ reminders for unpaid fines", [
            (r"the question: \ does a redesigned reminder letter raise payment within 30 days?", WHITE),
            (r"preregistered primary outcome: \ paid in full within 30 days, \ from administrative records; \ one "
             r"outcome, \ one analysis, \ written down first", MODEL),
            (r"power: \ a plausible effect is one or two points on a base of about 30\%; \ for two points at 80\% "
             r"power, \ about 8,400 people per arm", PERSON),
            (r"arms: \ the old letter, \ the new letter, \ and the new letter with a norm line; \ randomize by "
             r"person, \ check balance", SYMP),
            (r"report the effect with its interval, \ whatever it is; \ check who it worked for only as planned; \ "
             r"and follow up at six months for persistence", GOOD),
            (r"then cost per extra payment, \ and the decision", YOU),
        ], "Here's a worked trial: reminders for unpaid fines. <bookmark mark='a'/> The question: does a redesigned "
           "reminder letter raise payment within thirty days? <bookmark mark='b'/> The primary outcome, preregistered: "
           "paid in full within thirty days, from administrative records. One outcome and one analysis, written down "
           "first. <bookmark mark='c'/> Power: a plausible effect is one or two points on a base of about thirty "
           "percent. To detect two points with eighty percent power takes about eighty-four hundred people per arm. "
           "<bookmark mark='d'/> The arms: the old letter, the new letter, and the new letter with a norm line, "
           "randomized by person, with balance checked. <bookmark mark='e'/> Report the effect with its interval, "
           "whatever it is. Check who it worked for only as planned, and follow up at six months for persistence. "
           "<bookmark mark='f'/> Then compute the cost per extra payment, and decide.", font_size=21, buff=0.36)
