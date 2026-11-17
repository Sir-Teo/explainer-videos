from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.kant()
        self.question()
        self.objectives()

    def kant(self):
        k = archive.KANT_1786.data
        head = label(r"Kant, \ 1786: \ why there can be no science of the mind", font_size=34, color=KANT)
        head.to_edge(UP, buff=0.4)
        tiles = VGroup()
        for i, (name, key) in enumerate((("mathematics", "mathematics"), ("experiment", "experiment"),
                                         ("observation", "observation"))):
            box = RoundedRectangle(width=4.0, height=2.6, corner_radius=0.15, stroke_color=KANT, stroke_width=2)
            t = VGroup(label(rf"{i + 1}.\ {name}", font_size=28, color=KANT),
                       wrapped_label(rf"``{k[key]}''", 3.6, 18, WHITE)).arrange(DOWN, buff=0.25)
            t.move_to(box)
            tiles.add(VGroup(box, t))
        tiles.arrange(RIGHT, buff=0.35).move_to([0, 0.2, 0])
        q = label(r"Was Kant right?", font_size=44, color=YOU).to_edge(DOWN, buff=0.7)
        src = historical_tag(archive.KANT_1786.cite)
        with self.voiceover(
            "In Part 1, Immanuel Kant explained in 1786 why there could never be a science of the mind. "
            "<bookmark mark='a'/> First: mathematics can't be applied to what goes on in the mind. "
            "<bookmark mark='b'/> Second: you can't experiment on it, because its contents can be told apart in "
            "thought but not held apart and recombined at will. <bookmark mark='c'/> Third: observing your own mind "
            "alters and distorts the thing observed. <bookmark mark='d'/> Sixty-one parts later, it's time to "
            "answer him. Was Kant right?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for m, t in zip("abc", tiles):
                vo.wait_until(m)
                self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def question(self):
        rows_section(self, r"Today: \ the series ends as a doctorate does", [
            (r"one question, \ left open by two earlier parts, \ taken through a registered report", SYMP),
            (r"reviewed before the data are analysed, \ run, \ and reported whatever it shows", MODEL),
            (r"then the accounts are closed: \ Psyche sits the Battery, \ the Ledger is read top to bottom, \ the "
             r"Homunculus is drawn one last time", PERSON),
            (r"and Kant's three objections are answered, \ one at a time", KANT),
        ], "The series ends as a doctorate does. <bookmark mark='a'/> One question, left open by two earlier parts, "
           "is taken through a registered report. <bookmark mark='b'/> It's reviewed before the data are analysed, "
           "run, and reported whatever it shows. <bookmark mark='c'/> Then the accounts are closed. Psyche sits the "
           "Battery, the Ledger is read from top to bottom, and the Homunculus is drawn one last time. "
           "<bookmark mark='d'/> And Kant's three objections are answered, one at a time.", font_size=27, buff=0.48)

    def objectives(self):
        head = VGroup(label(r"Part 62", font_size=34, color=GREY_B), label(r"The Dissertation", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"find a question worth asking, \ and practise research ethics",
            r"write a registered report: \ theory, \ hypotheses, \ design check, \ decision rule",
            r"answer reviewers, \ run Stage 2, \ and report a deviation honestly",
            r"read Psyche's scorecard and the complete Ledger",
            r"give the verdict on Kant's objections, \ and name a fourth",
            r"choose where to go next, \ among sixty-two parts' open problems",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 62 of Psychology, Built: the dissertation. <bookmark mark='a'/> We'll find a question worth "
            "asking, and practise research ethics. We'll write a registered report: theory, hypotheses, a design "
            "check and a decision rule. We'll answer reviewers, run Stage 2, and report a deviation honestly. We'll "
            "read Psyche's scorecard and the complete Ledger. We'll give the verdict on Kant's objections, and name a "
            "fourth. And we'll choose where to go next, among sixty-two parts' open problems."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
