from __future__ import annotations

from videos.psychology.psych3.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.everywhere()
        self.five()

    def card(self):
        card = chapter_card(13, r"In practice: \ every score is a measurement", r"Where do these ideas earn a living?",
                            lit=(), part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter thirteen. In practice: every score is a measurement."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def everywhere(self):
        head = heading(r"Four scores you have met")
        tiles = VGroup()
        for title, rel, val, color in (
                (r"a hiring test", r"Would it rank the same people highly next week?",
                 r"Does it predict how they do in the job?", "#7EC8F5"),
                (r"a satisfaction survey", r"One question, or ten?",
                 r"Does it mean the same in every group that answers it?", "#F2C14E"),
                (r"a clinical questionnaire", r"How big a change is more than error?",
                 r"Does a lower score mean the patient is better?", "#7BD88F"),
                (r"a product metric", r"Does it wobble from week to week?",
                 r"Is it what you care about, or what is easy to count?", "#F2A65A")):
            body = VGroup(
                label(title, font_size=30, color=color),
                label(r"reliability", font_size=20, color=GREY_B), wrapped_label(rel, 2.75, 24, WHITE),
                label(r"validity", font_size=20, color=GREY_B), wrapped_label(val, 2.75, 24, WHITE),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            box = panel(3.2, 4.3, color=color)
            body.move_to(box)
            tiles.add(VGroup(box, body))
        tiles.arrange(RIGHT, buff=0.2).move_to([0, -0.45, 0])
        with self.voiceover(
            "None of this is confined to the psychology laboratory. Every score attached to a person, or to "
            "something people did, is a measurement, with a reliability and a validity argument. Or without "
            "them. <bookmark mark='a'/> A hiring test. Would it rank the same candidates highly if they sat it "
            "again next week? And does it predict how they'll do in the job, which is the only reason to use it? "
            "<bookmark mark='b'/> A satisfaction survey. You know now why one question is a poor instrument. And "
            "you can ask whether a four means the same thing in every group that answers. <bookmark mark='c'/> "
            "A clinical questionnaire. If a patient's score falls three points, is that more than the standard "
            "error of measurement? And does a lower score mean the patient is better, or better at the "
            "questionnaire? <bookmark mark='d'/> A product metric, like engagement. Does it wobble from week to "
            "week for no reason? And is it the thing you care about, or the thing that was easy to count? Each "
            "of those is a question from this part, in other clothes."
        ) as vo:
            self.play(FadeIn(head))
            for m, t in zip("abcd", tiles):
                vo.wait_until(m)
                self.play(FadeIn(t, shift=UP * 0.2))
        self.clear_scene()

    def five(self):
        ts = load("truescore")
        half = 1.96 * ts["sem"]
        head = label(r"Five questions for any score", font_size=44, color=P.ACCENT).to_edge(UP, buff=0.45)
        qs = VGroup(
            label(r"1. \ What kind of scale is it?", font_size=34),
            label(r"2. \ How much of it is error?", font_size=34),
            label(r"3. \ Consistent across what?", font_size=34),
            label(r"4. \ What shows it measures what its name says?", font_size=34),
            label(r"5. \ Is it a new name for an old thing?", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.6, 0.35, 0])
        side = VGroup(
            label(r"which sentences about it mean something", font_size=24, color=GREY_A),
            label(rf"a score of 33 is a range: \ $33 \pm {half:.0f}$", font_size=24, color=GREY_A),
            label(r"questions, days, or judges", font_size=24, color=GREY_A),
            label(r"other methods agree; \ other traits do not", font_size=24, color=GREY_A),
            label(r"correct for unreliability, then compare", font_size=24, color=GREY_A),
        )
        for s_, q in zip(side, qs):
            s_.next_to(q, RIGHT, buff=0.5)
            s_.set_x(3.9)
        who = wrapped_label(r"Who uses this: \ test developers, survey researchers, clinicians, people-analytics "
                            r"and data teams, and anyone who is handed a score and asked to act on it.", 12.4, 26,
                            GREY_A).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "So here are five questions to carry away, for the next time someone hands you a score. "
            "<bookmark mark='a'/> One: what kind of scale is it? That tells you which sentences about it mean "
            "something. <bookmark mark='b'/> Two: how much of it is error? A single score is a range, not a "
            f"point. Our thirty-three was thirty-three, give or take {half:.0f}. <bookmark mark='c'/> Three: "
            "consistent across what? Questions, days, or judges. <bookmark mark='d'/> Four: what's the evidence "
            "that it measures what its name says? Other methods of measuring the same thing should agree with "
            "it, and measures of other things shouldn't. <bookmark mark='e'/> And five: is it a new name for an "
            "old thing? <bookmark mark='f'/> These are the working questions of test developers, survey "
            "researchers, clinicians, and the analysts who turn behaviour into numbers. They cost nothing to "
            "ask, and most scores in circulation have never been asked them."
        ) as vo:
            self.play(FadeIn(head))
            for m, q, s_ in zip("abcde", qs, side):
                vo.wait_until(m)
                self.play(FadeIn(q, shift=RIGHT * 0.2))
                self.play(FadeIn(s_), run_time=0.6)
            vo.wait_until("f")
            self.play(FadeIn(who))
        self.clear_scene()
