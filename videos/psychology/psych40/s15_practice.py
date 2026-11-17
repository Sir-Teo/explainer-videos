from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.mapping()

    def card(self):
        card = chapter_card(14, r"In practice: \ treatments as models", r"What does each therapy act on?", lit=(),
                            part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter fourteen. In practice: treatments as models."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def mapping(self):
        head = heading(r"Each therapy acts on a model")
        data = (
            (r"exposure", r"the avoidance loop of chapter two: \ stay, \ and learn the danger does not come", GOOD),
            (r"behavioural activation", r"schedule rewarding activities, \ to restart the learning from reward that "
                                        r"depression slows (chapter eight)", PERSON),
            (r"cognitive therapy", r"test the beliefs of chapters four and six against evidence", SYMP),
            (r"medication", r"a modest average effect; \ choose with the person, \ watch side effects, \ review at "
                            r"weeks, \ not days", MODEL),
            (r"screening", r"Part 39's base rates: \ a positive screen leads to an assessment, \ not a label", AUTH),
        )
        rows = VGroup()
        for what, how, c in data:
            rows.add(VGroup(word_chip(what, color=c, font_size=18, width=3.6), wrapped_label(how, 8.2, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.2, 0])
        with self.voiceover(
            "In practice, each treatment acts on one of these models. <bookmark mark='a'/> Exposure acts on the "
            "avoidance loop of chapter two: stay, and learn that the danger doesn't come. <bookmark mark='b'/> "
            "Behavioural activation schedules rewarding activities, to restart the learning from reward that "
            "depression slows. <bookmark mark='c'/> Cognitive therapy tests the beliefs of chapters four and six "
            "against evidence. <bookmark mark='d'/> Medication has a modest average effect: choose it with the "
            "person, watch the side effects, and review it over weeks, not days. <bookmark mark='e'/> And screening "
            "follows Part 39's base rates: a positive screen leads to an assessment, not a label. Whether these "
            "treatments work, and how well, is Part 42."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
