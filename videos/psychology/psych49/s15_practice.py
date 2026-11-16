from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.where()
        self.audit()

    def card(self):
        card = chapter_card(14, r"In practice: \ clinics, \ devices and claims", r"Where do these analyses run, \ "
                            r"and how should their claims be checked?", lit=(), part=PART, scale=("brain",),
                            marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: clinics, devices and claims."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def where(self):
        head = heading(r"Where they run")
        items = [
            (r"the clinic", r"mapping language and movement before brain surgery, \ one patient at a time, \ where the "
                            r"pipeline is validated and fixed, \ and a false negative has a cost", SYMP),
            (r"device engineering", r"brain-computer interfaces are tested like medical devices: \ accuracy, \ bit "
                                    r"rate, \ stability over months, \ and the user's own goals", MODEL),
            (r"consumer neurotechnology", r"headbands that claim to measure focus or calm: \ EEG from a few dry "
                                          r"electrodes, \ dominated by muscle and eye movement", AUTH),
            (r"data science", r"large shared datasets of thousands of people, \ with fixed pipelines and held-out "
                              r"samples, \ now the standard for brain-behaviour claims", GOOD),
        ]
        rows = VGroup()
        for name, what, col in items:
            rows.add(VGroup(word_chip(name, col, 21, width=4.0), wrapped_label(what, 8.0, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.2, 0])
        with self.voiceover(
            "Where do these analyses run? <bookmark mark='a'/> In the clinic: mapping language and movement before "
            "brain surgery, one patient at a time, with a validated, fixed pipeline, where a false negative has a "
            "cost. <bookmark mark='b'/> In device engineering: brain-computer interfaces are tested like medical "
            "devices, for accuracy, bit rate, stability over months, and the user's own goals. <bookmark mark='c'/> "
            "In consumer neurotechnology: headbands that claim to measure focus or calm, from a few dry electrodes "
            "whose signal is dominated by muscle and eye movement. <bookmark mark='d'/> And in data science: large "
            "shared datasets of thousands of people, with fixed pipelines and held-out samples, now the standard for "
            "brain-behaviour claims."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def audit(self):
        head = heading(r"Auditing a claim about the brain")
        rows = rows_of([
            (r"1. \ \ was the pipeline fixed before the data, \ and how many paths were tried?", WHITE),
            (r"2. \ \ is the test at the level of people, \ with a threshold that fits the noise?", SYMP),
            (r"3. \ \ for a decoder: \ was every choice made inside the cross-validation loop, \ and could a confound "
             r"carry the label?", MODEL),
            (r"4. \ \ for a brain-behaviour claim: \ how many people, \ how reliable the measures, \ and was it tested "
             r"in a held-out sample?", PERSON),
            (r"5. \ \ for a device: \ accuracy against chance, \ bits per minute, \ in whom, \ and for how long?", AUTH),
            (r"6. \ \ is the claim about what the method can show, \ or about what the person thinks?", YOU),
        ], 12.4, 22, 0.36).move_to([0, -0.3, 0])
        with self.voiceover(
            "And here's a checklist for auditing any claim about the brain. <bookmark mark='a'/> Was the pipeline "
            "fixed before the data, and how many paths were tried? <bookmark mark='b'/> Is the test at the level of "
            "people, with a threshold that fits the noise? <bookmark mark='c'/> For a decoder: was every choice made "
            "inside the cross-validation loop, and could a confound carry the label? <bookmark mark='d'/> For a "
            "brain-behaviour claim: how many people, how reliable were the measures, and was it tested in a held-out "
            "sample? <bookmark mark='e'/> For a device: accuracy against chance, bits per minute, in whom, and for how "
            "long? <bookmark mark='f'/> And is the claim about what the method can show, or about what a person "
            "thinks?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
