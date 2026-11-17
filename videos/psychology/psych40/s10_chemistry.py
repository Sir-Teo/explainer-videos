from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


class Chemistry(VoiceoverScene):
    def construct(self):
        self.card()
        self.story()
        self.review()

    def card(self):
        card = chapter_card(9, r"The chemical story", r"Is depression a lack of serotonin?",
                            lit={1965: r"Schildkraut", 2022: r"Moncrieff et al."}, part=PART,
                            scale=("molecule", "person"), marr=("what",))
        with self.voiceover("Chapter nine. The chemical story."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def story(self):
        head = heading(r"Two accidents and a hypothesis")
        rows = rows_of([
            (r"1950s: \ reserpine, \ a blood-pressure drug that depletes monoamines, \ was reported to bring on low "
             r"mood in some patients", AUTH),
            (r"iproniazid, \ a tuberculosis drug that blocks the enzyme breaking monoamines down, \ was reported to "
             r"lift patients' spirits", GOOD),
            (r"the monoamine hypothesis: \ depression is a shortage of noradrenaline or serotonin, \ and "
             r"antidepressants correct it", SYMP),
            (r"it became the public story of depression as a ``chemical imbalance'', \ repeated in advertising "
             r"and clinics", PERSON),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        tag = historical_tag(r"Schildkraut (1965)")
        with self.voiceover(
            "The drugs came first, by accident. <bookmark mark='a'/> In the 1950s, reserpine, a blood-pressure drug "
            "that depletes monoamines, was reported to bring on low mood in some patients. <bookmark mark='b'/> And "
            "iproniazid, a tuberculosis drug that blocks the enzyme that breaks monoamines down, was reported to lift "
            "patients' spirits. <bookmark mark='c'/> From these came the monoamine hypothesis: depression is a "
            "shortage of noradrenaline or serotonin, and antidepressants correct it. <bookmark mark='d'/> It became "
            "the public story of depression as a chemical imbalance, repeated in advertising and in clinics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def review(self):
        head = heading(r"What the evidence on serotonin shows")
        rows = rows_of([
            (r"Moncrieff and colleagues, \ 2022: \ an umbrella review of the research on serotonin and depression", WHITE),
            (r"they found no consistent evidence that depression is associated with, \ or caused by, \ lower "
             r"serotonin activity", AUTH),
            (r"critics replied that serotonin may still matter for some people, \ and that the drugs' benefit does "
             r"not depend on the deficit story", SYMP),
            (r"the logical point stands either way: \ that a drug relieves a condition does not show the condition "
             r"is a shortage of what the drug changes; \ aspirin relieves headaches, \ and headaches are not a "
             r"shortage of aspirin", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        tag = published_tag(r"Moncrieff et al.\ (2022)")
        with self.voiceover(
            "Does the evidence support it? <bookmark mark='a'/> In 2022 Joanna Moncrieff and colleagues published an "
            "umbrella review of the research on serotonin and depression. <bookmark mark='b'/> They found no "
            "consistent evidence that depression is associated with, or caused by, lower serotonin activity. "
            "<bookmark mark='c'/> Critics replied that serotonin may still matter for some people, and that the "
            "drugs' benefit doesn't depend on the deficit story. <bookmark mark='d'/> The logical point stands either "
            "way. That a drug relieves a condition doesn't show the condition is a shortage of what the drug changes. "
            "Aspirin relieves headaches, and headaches aren't a shortage of aspirin. The Ledger marks the serotonin "
            "deficit account, as stated, as failed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
