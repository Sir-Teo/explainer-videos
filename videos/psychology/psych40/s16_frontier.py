from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.fast()
        self.open_questions()

    def card(self):
        card = chapter_card(15, r"Frontier: \ subtypes, \ speed and computation", r"What is still unknown about "
                            r"fear and sadness?", lit=(), part=PART, scale=("molecule", "circuit", "person"),
                            marr=("what", "how"))
        with self.voiceover("Chapter fifteen. Frontier: subtypes, speed and computation."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def fast(self):
        head = heading(r"Three frontiers")
        rows = rows_of([
            (r"subtypes: \ if depression is many conditions (Part 39), \ treatments may work for some and not "
             r"others; \ finding the subtypes from symptoms, \ biology or course has proved hard", SYMP),
            (r"speed: \ most antidepressants take weeks; \ ketamine, \ a drug acting on glutamate, \ can lift mood "
             r"within hours in some people, \ which a slow monoamine story cannot explain", MODEL),
            (r"computation: \ fitting learning models like chapter eight's to each person's choices, \ to measure "
             r"what differs in that person (Part 59)", PERSON),
            (r"each promises treatment matched to the person; \ none has yet delivered it reliably", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "At the frontier, three ideas. <bookmark mark='a'/> Subtypes: if depression is many conditions, as Part "
            "39 suggested, treatments may work for some and not others. Finding the subtypes, from symptoms, "
            "biology or course, has proved hard. <bookmark mark='b'/> Speed: most antidepressants take weeks, but "
            "ketamine, a drug acting on glutamate, can lift mood within hours in some people, which a slow monoamine "
            "story can't explain. <bookmark mark='c'/> And computation: fitting learning models like chapter eight's "
            "to each person's choices, to measure what differs in that person. That's Part 59. "
            "<bookmark mark='d'/> Each promises treatment matched to the person. None has yet delivered it reliably."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"how can exposure's gains be made to last outside the clinic?", GOOD),
            (r"is anhedonia a problem of liking, \ learning or effort, \ and does it differ between people?", MODEL),
            (r"who benefits from an antidepressant, \ and can that be known before starting?", PERSON),
            (r"what does a fast-acting treatment act on, \ if not a monoamine shortage?", SYMP),
            (r"how can people at risk of suicide be helped without relying on prediction?", YOU),
        ], 12.4, 24, 0.46).move_to([0, -0.2, 0])
        with self.voiceover(
            "So, open questions. How can exposure's gains be made to last outside the clinic? "
            "<bookmark mark='b'/> Is anhedonia a problem of liking, learning or effort, and does it differ between "
            "people? <bookmark mark='c'/> Who benefits from an antidepressant, and can that be known before "
            "starting? <bookmark mark='d'/> What does a fast-acting treatment act on, if not a monoamine shortage? "
            "<bookmark mark='e'/> And how can people at risk of suicide be helped without relying on prediction?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.15))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
