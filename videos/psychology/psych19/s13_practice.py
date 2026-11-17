from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.design()
        self.readback()
        self.testing()

    def card(self):
        card = chapter_card(12, r"In practice: \ forms, \ read-backs, \ tests",
                            r"Where does a four-item limit cost time, \ money or lives?", lit=(), part=PART,
                            scale=("person", "culture"), marr=("what",))
        with self.voiceover("Chapter twelve. In practice: forms, read-backs, tests."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def design(self):
        head = heading(r"Designing for a small workspace")
        raw = label(r"4929381047561203", font_size=44, color=LOST)
        chunked = label(r"4929 \ 3810 \ 4756 \ 1203", font_size=44, color=MEM)
        pair = VGroup(raw, chunked).arrange(DOWN, buff=0.35).move_to([0, 2.1, 0])
        rows = rows_of([
            (r"card numbers, \ phone numbers, \ bank codes and one-time passcodes are printed in groups: \ chunks", MEM),
            (r"don't make people carry a code from one screen to the next: \ show it where it is typed", WHITE),
            (r"``seven plus or minus two'' is often quoted as a menu limit: \ menus are seen, \ not held; \ the "
             r"limit is for what must be remembered", GREY_A),
            (r"interruptions are costly because they evict what was being held: \ resuming is a reconstruction", LOST),
            (r"cognitive load in teaching: \ worked examples free the workspace for learning; \ Part 54", EXEC),
        ], 12.4, 25, 0.3).move_to([0, -1.1, 0])
        with self.voiceover(
            "A limit of about four chunks shows up all over design. <bookmark mark='a'/> Sixteen digits in a row are "
            "beyond anyone's span. In groups of four they are four chunks of four, which is why card numbers, phone "
            "numbers and one-time passcodes are printed in groups. <bookmark mark='b'/> Forms that make you carry a "
            "code or a reference number from one screen to another are asking for a working-memory feat; show it "
            "where it has to be typed. <bookmark mark='c'/> Miller's seven is often quoted as a limit on the length "
            "of menus. That's a misreading: a menu is in front of you, and the limit is on what has to be held "
            "without it. <bookmark mark='d'/> Interruptions are expensive for the same reason. They evict whatever "
            "you were holding, and getting back to the task means rebuilding it. <bookmark mark='e'/> And in "
            "teaching, cognitive load theory designs lessons around the workspace, for instance with worked "
            "examples that leave room for learning. Part 54 examines how well that holds up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(raw))
            vo.wait_until("a")
            self.play(FadeIn(chunked, shift=DOWN * 0.1), FadeIn(rows[0]))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def readback(self):
        head = heading(r"Read-backs and checklists")
        atc = VGroup(label(r"``climb and maintain flight level 240, \ turn left heading 270, \ contact 128.75''",
                           font_size=26, color=LOOP),
                     label(r"``climb FL240, \ left 270, \ 128.75, \ Skyline 21''", font_size=26, color=MEM)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 2.0, 0])
        tags = VGroup(label(r"controller", font_size=19, color=LOOP).next_to(atc[0], LEFT, buff=0.3),
                      label(r"pilot reads back", font_size=19, color=MEM).next_to(atc[1], LEFT, buff=0.3))
        keep_in_frame(VGroup(atc, tags))
        rows = rows_of([
            (r"a clearance holds three or four numbers: \ at the limit, \ and heard once", WHITE),
            (r"the read-back puts the pilot's memory where the controller can check it: \ a hear-back closes the "
             r"loop", MEM),
            (r"a classic error: \ a number from the last clearance, \ or another aircraft's, \ substituted: \ a swap",
             LOST),
            (r"checklists and written clearances move the load from memory to paper or screen", GOOD),
            (r"the same logic in hospitals: \ read-back of verbal orders and test results", GREY_A),
        ], 12.4, 25, 0.3).move_to([0, -1.1, 0])
        with self.voiceover(
            "Aviation learned this the hard way. <bookmark mark='a'/> An air traffic clearance can carry three or "
            "four numbers, an altitude, a heading, a frequency, heard once over a noisy radio, which is right at the "
            "limit. <bookmark mark='b'/> So the pilot reads it back, putting their memory where the controller can "
            "check it; the controller listening for errors is the hear-back. <bookmark mark='c'/> A classic error is "
            "substitution: a number from the previous clearance, or from another aircraft's, which is exactly a swap "
            "error, the right value bound to the wrong slot. <bookmark mark='d'/> Checklists, and clearances sent "
            "as text, move the load from memory to paper or a screen. <bookmark mark='e'/> Hospitals adopted the "
            "same logic for verbal orders and critical test results: say it back. Part 51 takes up this kind of "
            "design in general."
        ) as vo:
            self.play(FadeIn(head), FadeIn(atc[0]), FadeIn(tags[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(atc[1]), FadeIn(tags[1]), FadeIn(rows[1]))
            for m, r in zip("cde", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def testing(self):
        head = heading(r"Span as a clinical and research measure")
        rows = rows_of([
            (r"digit span forwards and backwards is part of the Wechsler intelligence scales", WHITE),
            (r"backwards is harder: \ you must hold and transform, \ a small complex span", MEM),
            (r"spans grow through childhood, \ peak in early adulthood, \ and decline slowly with age: \ Part 31", LOOP),
            (r"low working memory scores are common in ADHD and many learning difficulties: \ Part 41", EXEC),
            (r"a task score is not a pure measure: \ speed, \ strategy, \ knowledge and effort all enter", LOST),
            (r"and a reliable score for ranking people may be a poor one for detecting change: \ Part 59", GREY_A),
        ], 12.4, 26, 0.32).move_to([0, -0.2, 0])
        with self.voiceover(
            "Spans are also measurements of people. <bookmark mark='a'/> Digit span, forwards and backwards, is part "
            "of the Wechsler intelligence scales, and of many neuropsychological batteries. <bookmark mark='b'/> "
            "Backwards span is harder, because the digits must be held and reordered: a small complex span. "
            "<bookmark mark='c'/> Spans grow through childhood, peak in early adulthood, and decline slowly after "
            "that, which Part 31 examines. <bookmark mark='d'/> Low working-memory scores are common in ADHD and in "
            "many learning difficulties, Part 41. <bookmark mark='e'/> But a span score is not a pure measure of "
            "capacity: as this part has shown, speed of speech, strategy, knowledge of the material and effort all "
            "enter it. <bookmark mark='f'/> And a score that ranks people reliably can be a poor one for detecting "
            "change within a person, a problem Part 59 calls the reliability paradox."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
