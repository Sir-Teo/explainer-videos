from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403

PROPOSALS = [
    (r"larger samples and power analysis", r"strong: \ replication rates rise with power (Part 4)", GOOD),
    (r"registered reports", r"strong: \ far more null results published; \ quality rated at least as high", GOOD),
    (r"open data and code", r"good: \ errors found and corrected; \ uptake still partial", GOOD),
    (r"big team science", r"good: \ precise answers on heterogeneity; \ slow and costly", MODEL),
    (r"preregistration alone", r"mixed: \ often vague, \ and deviations unreported", PERSON),
    (r"integrative design, \ formal theory", r"promising: \ few tests of whether they speed discovery", PERSON),
    (r"lowering the significance threshold", r"argued, \ not tested", AUTH),
]


class Ranked(VoiceoverScene):
    def construct(self):
        card_section(self, 12, r"Proposals, \ ranked by evidence", r"Which reforms work?", scale=("society",))
        self.table()

    def table(self):
        head = heading(r"The proposals, \ and the evidence they work")
        rows = VGroup()
        for i, (p, e, c) in enumerate(PROPOSALS):
            rows.add(VGroup(label(rf"{i + 1}", font_size=22, color=c), wrapped_label(p, 4.4, 20, WHITE),
                            wrapped_label(e, 7.2, 19, c)).arrange(RIGHT, buff=0.35, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([0, -0.3, 0])
        with self.voiceover(
            "Which reforms work? Here are the proposals, ranked by the evidence that they do. <bookmark mark='a'/> "
            "Larger samples and power analysis: strong evidence, since replication rates rise with power, as Part 4 "
            "showed. <bookmark mark='b'/> Registered reports: strong. Far more null results are published, and "
            "their quality is rated at least as high. <bookmark mark='c'/> Open data and code: good evidence. Errors "
            "are found and corrected, though uptake is still partial. <bookmark mark='d'/> Big team science: good, "
            "with precise answers about heterogeneity, but slow and costly. <bookmark mark='e'/> Preregistration "
            "alone: mixed. Plans are often vague, and deviations go unreported. <bookmark mark='f'/> Integrative "
            "design and formal theory: promising, with few tests of whether they speed discovery. "
            "<bookmark mark='g'/> And lowering the significance threshold: argued, but not tested."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcdefg", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
