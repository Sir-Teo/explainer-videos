from __future__ import annotations

import numpy as np

from videos.music.music67.common import *  # noqa: F403


class Practice(SoundScene):
    def construct(self):
        chapter(self, 10, r"Reading papers, \ and practice as research", r"How do you read a paper in a field you do not know?")
        self.reading()
        self.subfields()
        self.example()
        self.practice()

    # ------------------------------------------------------------------
    def reading(self):
        items = [
            (r"first: \ what is the claim, \ in one sentence, \ and what would make it false?", WHITE),
            (r"then: \ the evidence's kind \ (Chapter 1) \ and its usual failure", WHITE),
            (r"then: \ the numbers: \ how many pieces, \ listeners, \ splits; \ with what uncertainty", WHITE),
            (r"last: \ what the authors say they cannot show, \ and what they did not say", TUNE),
        ]
        rows_scene(self, r"reading a paper", items,
                   "How do you read a paper in a corner of the field you do not know? <bookmark mark='b'/> First, find the claim, "
                   "in one sentence, and ask what would make it false. <bookmark mark='c'/> Then the kind of evidence, from Chapter "
                   "1, and that kind's usual failure. <bookmark mark='d'/> Then the numbers: how many pieces, listeners or splits, "
                   "with what uncertainty. <bookmark mark='e'/> And last, what the authors say they cannot show, and what they did "
                   "not say at all.", marks="bcde")

    # ------------------------------------------------------------------
    def subfields(self):
        rows = [(r"historical musicology", r"which sources, \ how dated, \ what is inferred from silence"),
                (r"music theory and analysis", r"the counter-example; \ the corpus behind a `rule'"),
                (r"ethnomusicology", r"who was asked, \ who speaks, \ who consented"),
                (r"music psychology", r"the sample, \ preregistration, \ the effect size and its interval"),
                (r"music information retrieval", r"the split, \ leakage, \ annotator agreement, \ the baseline"),
                (r"music technology", r"the listening test's design, \ and what is heard rather than measured")]
        g = VGroup(*[VGroup(label(a, font_size=19, color=TUNE), label(b, font_size=17, color=WHITE)) for a, b in rows]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.3)
        for r in g:
            r[1].next_to(r[0], RIGHT, buff=0.3).align_to(g, LEFT).shift(RIGHT * 4.4)
        head = label(r"what to check first, \ by subfield", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "And each subfield has its first question. <bookmark mark='a'/> In historical musicology: which sources, how dated, "
            "and what is inferred from silence. In theory and analysis: the counter-example, and the corpus behind any rule. "
            "<bookmark mark='b'/> In ethnomusicology: who was asked, who speaks, and who consented. In music psychology: the "
            "sample, whether it was preregistered, and the effect with its interval. <bookmark mark='c'/> In music information "
            "retrieval: the split, leakage, annotator agreement, and the baseline. And in music technology: the listening "
            "test's design, and what was heard rather than measured."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g[0]), FadeIn(g[1]))
            vo.wait_until("b")
            self.play(FadeIn(g[2]), FadeIn(g[3]))
            vo.wait_until("c")
            self.play(FadeIn(g[4]), FadeIn(g[5]))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        items = [
            (r"practice as research: \ a composition, \ a performance or an instrument as the result, \ with a written account", WHITE),
            (r"its knowledge is often how-to: \ a way of bowing, \ voicing a chord, \ building a reed", WHITE),
            (r"its check is that others can use it: \ the method is shown, \ the work can be heard and taken apart", WHITE),
            (r"this series is one: \ Monochord, \ the Tune and its Variations, \ built so that every claim can be run", TUNE),
        ]
        rows_scene(self, r"practice as research", items,
                   "Some research is made rather than written. <bookmark mark='b'/> Practice as research offers a composition, a "
                   "performance or an instrument as the result, with an account of what was found. <bookmark mark='c'/> Its "
                   "knowledge is often how-to: a way of bowing, of voicing a chord, of building a reed. <bookmark mark='d'/> Its "
                   "check is that others can use it: the method is shown, and the work can be heard and taken apart. "
                   "<bookmark mark='e'/> This series is one: Monochord, the Tune and its Variations, built so that every claim in it "
                   "can be run again.", marks="bcde")

    # ------------------------------------------------------------------
    def example(self):
        items = [
            (r"the claim: \ ten minutes of a Mozart sonata raises spatial reasoning, \ for about ten to fifteen minutes", WHITE),
            (r"what would refute it: \ no difference against other music, \ or against anything that wakes listeners up", WHITE),
            (r"the evidence: \ an experiment; \ its usual failure is that it does not replicate", WHITE),
            (r"the numbers: \ 36 students, \ one laboratory, \ three conditions; \ no preregistration \ (nobody did, \ in 1993)", WHITE),
            (r"what was not said, \ and was heard anyway: \ `Mozart makes babies smarter'", TUNE),
        ]
        rows_scene(self, r"the 1993 paper, \ read that way", items,
                   "Read the 1993 paper that way. <bookmark mark='b'/> The claim: ten minutes of a Mozart sonata raises spatial reasoning, for about ten to fifteen minutes. <bookmark mark='c'/> What would challenge a Mozart-specific mechanism: no difference against other music, or against anything that simply wakes listeners up. <bookmark mark='d'/> The evidence is an experiment, whose usual failure is not to replicate. <bookmark mark='e'/> The numbers: thirty-six students, one laboratory, three conditions, and no preregistration reported in the account discussed here. <bookmark mark='f'/> And what was not said, but heard anyway: that Mozart makes babies smarter. The paper studied students, not babies.",
                   marks="bcdef")
