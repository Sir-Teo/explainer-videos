from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Sleep(VoiceoverScene):
    def construct(self):
        card_section(self, 7, r"Sleep, \ treated", r"Can insomnia be treated without pills?", scale=("person",))
        self.cbti()

    def cbti(self):
        chips_section(self, r"CBT for insomnia", [
            (r"sleep restriction", r"time in bed cut to the time actually slept, \ then lengthened: \ Part 10's sleep "
                                   r"pressure, \ built up deliberately", MODEL),
            (r"stimulus control", r"the bed only for sleep; \ up if awake: \ Part 16's conditioning, \ re-learned",
             PERSON),
            (r"cognitive work", r"worry about sleep keeps people awake; \ beliefs about the costs of a bad night are "
                                r"tested", SYMP),
            (r"the evidence", r"trials find large improvements that last beyond the end of treatment; \ guidelines "
                              r"recommend it before sleeping pills", GOOD),
            (r"the gap", r"few trained therapists: \ digital versions have trial evidence, \ with the usual drop-out",
             AUTH),
        ], "Can insomnia be treated without pills? <bookmark mark='a'/> Cognitive behavioural therapy for insomnia "
           "starts with sleep restriction: time in bed is cut to the time actually slept, then lengthened. That's "
           "Part 10's sleep pressure, built up deliberately. <bookmark mark='b'/> Stimulus control: the bed is only "
           "for sleep, and you get up if you're awake. That's Part 16's conditioning, re-learned. "
           "<bookmark mark='c'/> Cognitive work: worry about sleep keeps people awake, so beliefs about the costs of a "
           "bad night are tested. <bookmark mark='d'/> Trials find large improvements that last beyond the end of "
           "treatment, and guidelines recommend it before sleeping pills. <bookmark mark='e'/> The gap is that there "
           "are few trained therapists. Digital versions have trial evidence, with the usual drop-out.",
           chip_w=3.6, text_w=8.6)
        rows_section(self, r"Why it works, \ in Part 10's model", [
            (r"Borbély's two processes: \ sleep pressure (S) builds with time awake; \ the circadian clock (C) "
             r"opens the gate", WHITE),
            (r"spending long hours in bed awake spreads sleep thin: \ pressure is low at bedtime", AUTH),
            (r"restriction concentrates it: \ more pressure, \ faster sleep, \ fewer awakenings; \ then the window "
             r"grows", GOOD),
            (r"a model of the mind, \ turned into a treatment: \ the series' theme, \ in one clinic", YOU),
        ], "Why does it work? <bookmark mark='a'/> In Part 10's model, Alexander Borbely's two processes: sleep "
           "pressure builds with time awake, and the circadian clock opens the gate. <bookmark mark='b'/> Spending "
           "long hours in bed awake spreads sleep thin, so pressure is low at bedtime. <bookmark mark='c'/> "
           "Restriction concentrates it: more pressure, faster sleep and fewer awakenings. Then the window grows. "
           "<bookmark mark='d'/> It's a model of the mind turned into a treatment, which is the series' theme, in "
           "one clinic.")
