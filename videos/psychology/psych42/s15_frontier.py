from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ mechanisms, \ matching and psychedelics", r"What is still unknown?",
                            lit=(), part=PART, scale=("molecule", "person"), marr=("what", "how"))
        with self.voiceover("Chapter fourteen. Frontier: mechanisms, matching and psychedelics."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def three(self):
        head = heading(r"Three frontiers")
        rows = rows_of([
            (r"mechanisms: \ therapies claim to work by changing thoughts, \ skills or relationships, \ but showing "
             r"that the change comes first, \ and causes the improvement, \ is rare", SYMP),
            (r"matching: \ models that predict, \ from a person's characteristics, \ which of two treatments will suit "
             r"them better; \ promising, \ and still to be tested prospectively (Part 59)", MODEL),
            (r"psychedelics: \ psilocybin and MDMA given with therapy; \ participants nearly always know whether they "
             r"had the drug, \ so blinding fails, \ and in 2024 the US regulator declined to approve MDMA-assisted "
             r"therapy for PTSD", PERSON),
            (r"each frontier needs what this part used: \ a good control, \ an unfiltered record, \ and outcomes that "
             r"matter to the person", YOU),
        ], 12.4, 22, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "At the frontier, three ideas. <bookmark mark='a'/> Mechanisms: therapies claim to work by changing "
            "thoughts, skills or relationships. But showing that the change comes first, and causes the improvement, "
            "is rare. <bookmark mark='b'/> Matching: models that predict, from a person's characteristics, which of "
            "two treatments will suit them better. They're promising, and still to be tested prospectively. That's "
            "Part 59. <bookmark mark='c'/> Psychedelics: psilocybin and MDMA, given with therapy. Participants nearly "
            "always know whether they had the drug, so blinding fails, and in 2024 the American regulator declined to "
            "approve MDMA-assisted therapy for post-traumatic stress. <bookmark mark='d'/> Each frontier needs what "
            "this part used: a good control, an unfiltered record, and outcomes that matter to the person."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"how much of therapy's effect is common factors, \ and how much specific technique?", SYMP),
            (r"what is the right placebo for a talking therapy?", MODEL),
            (r"why do some clients get worse, \ and can it be predicted?", AUTH),
            (r"can simpler, \ cheaper therapies close the treatment gap without losing the effect?", GOOD),
            (r"can trials of psychedelic therapy be made blind, \ or should they be judged differently?", YOU),
        ], 12.4, 24, 0.46).move_to([0, -0.2, 0])
        with self.voiceover(
            "So, open questions. How much of therapy's effect is common factors, and how much specific technique? "
            "<bookmark mark='b'/> What's the right placebo for a talking therapy? <bookmark mark='c'/> Why do some "
            "clients get worse, and can it be predicted? <bookmark mark='d'/> Can simpler, cheaper therapies close "
            "the treatment gap without losing the effect? <bookmark mark='e'/> And can trials of psychedelic therapy "
            "be made blind, or should they be judged differently?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.15))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
