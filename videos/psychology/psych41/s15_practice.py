from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.services()

    def card(self):
        card = chapter_card(14, r"In practice: \ services, \ trade-offs and harm reduction", r"What helps, \ in "
                            r"practice?", lit=(), part=PART, scale=("person", "society"), marr=("how",))
        with self.voiceover("Chapter fourteen. In practice: services, trade-offs and harm reduction."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def services(self):
        head = heading(r"What helps")
        data = (
            (r"early intervention", r"teams that see young people soon after a first episode, \ with medication, "
                                    r"therapy, \ family work, \ and help with school and jobs", SYMP),
            (r"shared decisions", r"antipsychotics trade fewer relapses against movement, \ weight and metabolic "
                                  r"harms: \ the person weighs them, \ with the prescriber", GOOD),
            (r"harm reduction", r"opioid substitution with methadone or buprenorphine lowers deaths; \ naloxone "
                                r"reverses overdoses; \ clean needles prevent infections", PERSON),
            (r"supports, \ not cures", r"for autistic and ADHD children and adults: \ adjustments at school and work, "
                                       r"\ clear routines, \ fewer sensory demands", MODEL),
            (r"language", r"``a person with schizophrenia'', \ ``autistic person'': \ ask, \ and follow the person", YOU),
        )
        rows = VGroup()
        for what, how, c in data:
            rows.add(VGroup(word_chip(what, color=c, font_size=18, width=3.6), wrapped_label(how, 8.2, 19, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.3, 0])
        with self.voiceover(
            "What helps, in practice? <bookmark mark='a'/> Early intervention: teams that see young people soon after "
            "a first episode of psychosis, with medication, therapy, family work, and help with school and jobs. "
            "<bookmark mark='b'/> Shared decisions: antipsychotics trade fewer relapses against movement, weight and "
            "metabolic harms, and the person weighs them with the prescriber. <bookmark mark='c'/> Harm reduction: "
            "opioid substitution with methadone or buprenorphine lowers deaths, naloxone reverses overdoses, and "
            "clean needles prevent infections. It meets people where they are. <bookmark mark='d'/> Supports, not "
            "cures, for autistic and ADHD children and adults: adjustments at school and work, clear routines, fewer "
            "sensory demands. <bookmark mark='e'/> And language. A person with schizophrenia; an autistic person. "
            "Ask, and follow the person. Whether the talking therapies work, and how well, is Part 42."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
