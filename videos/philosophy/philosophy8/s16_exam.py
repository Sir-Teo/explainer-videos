from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Exam(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"The surprise exam", r"Can a teacher's announcement refute itself?",
                            part=PART)
        with self.voiceover("Chapter fifteen. The surprise exam."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.puzzle()
        self.announce()
        self.knower()
        self.knower_proof()

    def puzzle(self):
        d = load("exam")
        head = label(r"`There will be an exam next week, \ and you will not know the night before'", font_size=28,
                     color=GOAL).to_edge(UP, buff=0.5)
        days = VGroup()
        for i, dname in enumerate(d["days"]):
            box = RoundedRectangle(width=1.8, height=1.2, corner_radius=0.12, stroke_color=GREY_C, stroke_width=2,
                                   fill_color="#151A24", fill_opacity=1).move_to([-4.8 + 2.4 * i, 1.0, 0])
            days.add(VGroup(box, label(dname, font_size=30).move_to(box)))
        reasons = [r"not Friday: \ on Thursday night we would know", r"so not Thursday either: \ on Wednesday night "
                   r"we would know", r"so not Wednesday", r"so not Tuesday", r"so not Monday: \ no exam is possible"]
        texts = VGroup(*[label(t, font_size=24, color=GREY_A) for t in reasons]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.18)
        texts.move_to([0, -1.4, 0])
        crosses = VGroup(*[Cross(days[i - 1], stroke_color=BAD, stroke_width=4) for i in d["struck"]])
        twist = label(r"then the exam is given on Wednesday, \ and it is a complete surprise", font_size=28,
                      color=SELF).to_edge(DOWN, buff=0.35)
        assert d["struck"] == [5, 4, 3, 2, 1]
        with self.voiceover(
            "A teacher announces: there will be an exam next week, and you will not know the night before which "
            "day it is. The puzzle was in print by 1948, in a paper of D. J. O'Connor. <bookmark mark='a'/>The "
            "students reason. It cannot be Friday: if no exam had come by Thursday night, we would know. "
            "<bookmark mark='b'/>So Friday is out, and Thursday becomes the last day; by the same argument, not "
            "Thursday. Then not Wednesday, not Tuesday, not Monday. No surprise exam is possible. "
            "<bookmark mark='c'/>The teacher gives the exam on Wednesday. The students are completely surprised. "
            "Something in their argument went wrong, and Quine, among many others, tried to say exactly what."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(dd) for dd in days], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(Create(crosses[0]), FadeIn(texts[0]))
            vo.wait_until("b")
            for k in range(1, 5):
                self.play(Create(crosses[k]), FadeIn(texts[k]), run_time=0.9)
            vo.wait_until("c")
            self.play(FadeOut(crosses[2]), days[2][0].animate.set_stroke(SELF, 4), FadeIn(twist))
        self.clear_scene()


    def announce(self):
        d = load("announce")
        hc = history_card(2007, r"Jelle Gerbrandy", r"`The surprise examination in dynamic epistemic logic'", width=6.6,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup()
        for i, ws in enumerate(d["steps"]):
            chips = VGroup(*[VGroup(RoundedRectangle(width=0.8, height=0.5, corner_radius=0.08, stroke_width=0,
                                                     fill_color=OK if k in ws else "#2A303C", fill_opacity=0.8),
                                    label(["Mon", "Tue", "Wed", "Thu", "Fri"][k - 1], font_size=18)).arrange(ORIGIN)
                             for k in range(1, 6)]).arrange(RIGHT, buff=0.12)
            tag = label(r"before" if i == 0 else rf"after {i} announcement{'s' if i > 1 else ''}", font_size=20,
                        color=GREY_A)
            rows.add(VGroup(tag, chips).arrange(RIGHT, buff=0.4))
        for r in rows:
            r[1].move_to([1.6, r.get_y(), 0])
            r[0].next_to(r[1], LEFT, buff=0.4)
        rows.arrange(DOWN, buff=0.18).move_to([0.3, -0.2, 0])
        for r in rows:
            r[0].align_to(rows[0][0], RIGHT)
        notes = VGroup(label(r"one truthful announcement removes only Friday: \ Wednesday is still a surprise",
                             font_size=22, color=OK),
                       label(r"the students' argument repeats the announcement \ as if it stayed true once learned",
                             font_size=22, color=BAD),
                       label(r"like Moore's sentences: \ true when said, \ false once believed", font_size=22,
                             color=GOAL)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        assert d["wednesday_after_one"] and d["steps"][-1] == []
        with self.voiceover(
            "Dynamic epistemic logic, the subject of Part 12, offers a precise diagnosis, given by Jelle Gerbrandy. "
            "<bookmark mark='a'/>Model the students' uncertainty as five possible days. The announcement, 'the exam "
            "will be a surprise', rules out the days on which it would be false. Before it, every day is possible. "
            "<bookmark mark='b'/>Learning it rules out Friday. If the students then treat the announcement as still "
            "true, it rules out Thursday, then Wednesday, and so on, until nothing is left: that is their argument, "
            "and the Reasoner runs it. <bookmark mark='c'/>But a single truthful announcement only removes Friday. "
            "After it, if the exam is on Wednesday, the students still cannot know it the night before. "
            "<bookmark mark='d'/>The announcement is true when it is made, and stops being true once it is learned, "
            "like Moore's sentences in the next chapter."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows[1:]], lag_ratio=0.4), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(notes[0]), Indicate(rows[1], color=OK, scale_factor=1.03))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
        self.clear_scene()

    def knower(self):
        hc = history_card(1960, r"David Kaplan \& Richard Montague", r"`A paradox regained'", width=5.8,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            label(r"the teacher's announcement talks about the students' own knowledge of it", font_size=24),
            label(r"Kaplan and Montague: \ the knower, \ `this sentence is not known'", font_size=26, color=SELF),
            label(r"if knowledge is factive \ ($K\varphi \to \varphi$), \ and known to be, \ contradiction follows",
                  font_size=24, color=BAD),
            label(r"the same diagonal as the liar and Gödel: \ `known', like `true', \ cannot be a predicate with all "
                  r"the obvious properties", font_size=24, color=GOAL),
            label(r"Chow (1998) surveys over a hundred papers on the exam", font_size=20, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.4, 0])
        with self.voiceover(
            "What makes the exam paradoxical? <bookmark mark='a'/>The announcement is about the students' own "
            "knowledge of it. <bookmark mark='b'/>David Kaplan and Richard Montague distilled that into a paradox "
            "of its own in 1960, the knower: this sentence is not known. <bookmark mark='c'/>If knowledge is "
            "factive, so that whatever is known is true, and that principle is itself known, a contradiction "
            "follows, by the liar's argument with 'known' for 'true'. <bookmark mark='d'/>It is the same diagonal "
            "as Tarski's and Gödel's. Knowledge, like truth and provability, cannot be a predicate with every "
            "property we expect of it. <bookmark mark='e'/>The literature on the surprise exam alone runs to well "
            "over a hundred papers."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()

    def knower_proof(self):
        head = label(r"The knower, \ in five lines", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = [(r"K \leftrightarrow \lnot\,\mathrm{Kn}(\ulcorner K \urcorner)", r"the diagonal lemma"),
                (r"\mathrm{Kn}(\ulcorner K \urcorner) \to K", r"factivity: \ what is known is true"),
                (r"\mathrm{Kn}(\ulcorner K \urcorner) \to \lnot\,\mathrm{Kn}(\ulcorner K \urcorner), \ \text{so} \ "
                 r"\lnot\,\mathrm{Kn}(\ulcorner K \urcorner), \ \text{so} \ K", r"from 1 and 2"),
                (r"\mathrm{Kn}(\ulcorner K \urcorner)", r"$K$ is proved, \ so it is known"),
                (r"\bot", r"lines 3 and 4")]
        tab = VGroup()
        for i, (f, why) in enumerate(rows):
            y = 1.6 - 0.8 * i
            tab.add(VGroup(label(rf"{i + 1}.", font_size=24, color=GREY_B).move_to([-6.0, y, 0]),
                           MathTex(f, font_size=30, color=BAD if i == 4 else WHITE).move_to([-5.5, y, 0],
                                                                                            aligned_edge=LEFT),
                           label(why, font_size=21, color=GREY_A).move_to([1.6, y, 0], aligned_edge=LEFT)))
        moral = label(r"not even truth is needed: \ factivity and closure suffice", font_size=26, color=GOAL).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "Here is the knower, in five lines. <bookmark mark='a'/>By the diagonal lemma, a sentence K says: K is "
            "not known. <bookmark mark='b'/>Knowledge is factive: if K is known, K is true. "
            "<bookmark mark='c'/>So if K is known, K is not known; so K is not known; and that is K. "
            "<bookmark mark='d'/>But we have just proved K from principles we know, so K is known. "
            "<bookmark mark='e'/>Contradiction. No truth predicate was used: factivity, and knowing what we can "
            "prove, are enough."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            self.play(FadeIn(moral))
        self.clear_scene()
