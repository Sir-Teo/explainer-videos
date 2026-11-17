from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.open()

    def card(self):
        card = chapter_card(15, r"Frontier: \ rates, \ robots and incentives", r"Is the literature getting better?",
                            lit=(), part=PART, scale=("society",), marr=("what",))
        with self.voiceover("Chapter fifteen. Frontier: rates, robots and incentives."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def three(self):
        head = heading(r"Three frontiers")
        items = [
            (r"are replication rates rising?", r"larger samples and preregistration have spread since 2015; \ whether "
                                               r"newer findings replicate better is being measured, \ not yet known",
             GOOD),
            (r"automated checking", r"statcheck, \ GRIM and their successors run at submission; \ language models now "
                                    r"read papers for errors, \ with their own error rates to measure", MODEL),
            (r"incentives as evolution", r"Smaldino and McElreath, \ 2016: \ if labs that publish more are copied, \ "
                                         r"methods that produce more false positives spread, \ without anyone "
                                         r"cheating (Part 61)", AUTH),
        ]
        rows = VGroup()
        for name, what, col in items:
            rows.add(VGroup(word_chip(name, col, 20, width=4.4), wrapped_label(what, 7.8, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.3, 0])
        tag = published_tag(r"Smaldino \& McElreath (2016)")
        with self.voiceover(
            "Three frontiers. <bookmark mark='a'/> Are replication rates rising? Larger samples and preregistration "
            "have spread since 2015. Whether newer findings replicate better is being measured, and isn't yet known. "
            "<bookmark mark='b'/> Automated checking: statcheck, GRIM and their successors now run at submission, "
            "and language models read papers for errors, with error rates of their own to measure. "
            "<bookmark mark='c'/> And incentives as evolution. In 2016 Paul Smaldino and Richard McElreath showed "
            "that if labs that publish more are imitated, methods that produce more false positives spread, without "
            "anyone cheating. Part 61 returns to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"can a filtered literature ever be corrected after the fact, \ or only replaced?", WHITE),
            (r"what share of a field's findings should be replicated, \ and which?", PERSON),
            (r"how should a meta-analysis weigh a registered study against an unregistered one?", MODEL),
            (r"what would a literature look like if publication were decided before the results, \ always?", YOU),
        ], 12.4, 24, 0.5).move_to([0, -0.3, 0])
        with self.voiceover(
            "Open questions. <bookmark mark='a'/> Can a filtered literature ever be corrected after the fact, or "
            "only replaced? <bookmark mark='b'/> What share of a field's findings should be replicated, and which? "
            "<bookmark mark='c'/> How should a meta-analysis weigh a registered study against an unregistered one? "
            "<bookmark mark='d'/> And what would a literature look like if publication were always decided before "
            "the results?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
