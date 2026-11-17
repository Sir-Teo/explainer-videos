from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.care()
        self.colds()
        self.question()
        self.objectives()

    def care(self):
        card = care_card().move_to([0, 0, 0])
        with self.voiceover(
            "Before we start. This part is about health, illness and care, including mental health services. "
            "<bookmark mark='a'/> It's education, not diagnosis or treatment. If any of it touches your own life, "
            "talk to a doctor, a counsellor, or someone you trust. <bookmark mark='b'/> If you're in danger now, call "
            "your local emergency number. In the United States you can call or text nine eight eight. In the UK and "
            "Ireland, Samaritans are on one one six, one two three. And find a helpline dot com lists free, "
            "confidential lines in other countries."
        ) as vo:
            self.play(FadeIn(card.box), FadeIn(card.head))
            vo.wait_until("a")
            self.play(FadeIn(card.body))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.6), run_time=3.0)
        self.wait(1.5)
        self.clear_scene()

    def colds(self):
        head = heading(r"Nose drops and stress")
        A = axes([0.3, 5.7], [0, 0.6], x_length=5.4, y_length=3.0, xticks=None, yticks=[0, 0.2, 0.4, 0.6],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"developed a cold", center=[-3.3, 0.3, 0], font_size=12)
        vals = [0.27, 0.33, 0.38, 0.42, 0.47]
        b = bars(A.ax, [1, 2, 3, 4, 5], vals, [GOOD, SYMP, PERSON, AUTH, AUTH], width=0.6)
        names = VGroup(*[label(rf"{k}", font_size=13, color=GREY_A).next_to(A.ax.c2p(k, 0), DOWN, buff=0.12)
                         for k in range(1, 6)])
        nl = label(r"stress index, \ lowest to highest", font_size=13, color=GREY_A).next_to(names, DOWN, buff=0.1)
        rows = rows_of([
            (r"Cohen, \ Tyrrell and Smith, \ 1991: \ about 400 healthy volunteers rated their stress, \ then took nose "
             r"drops containing a cold virus, \ and were quarantined", WHITE),
            (r"the more stress they had reported, \ the more of them developed a cold: \ a dose-response line, \ with "
             r"health habits and immunity controlled", PERSON),
            (r"the bars show the pattern, \ from about a quarter to about half (approximate)", GREY_B),
            (r"this part's first half: \ how psychological states change bodies; \ its second: \ how help reaches the "
             r"people who need it", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Cohen, \ Tyrrell \& Smith (1991)")
        with self.voiceover(
            "In 1991 Sheldon Cohen, David Tyrrell and Andrew Smith ran an unusual experiment. <bookmark mark='a'/> "
            "About four hundred healthy volunteers rated their stress, then took nose drops containing a cold virus, "
            "and were quarantined. <bookmark mark='b'/> The more stress they'd reported, the more of them developed a "
            "cold, in a dose-response line, with health habits and immunity controlled. <bookmark mark='c'/> The bars "
            "show the pattern, from about a quarter to about half. They're approximate. <bookmark mark='d'/> This "
            "part's first half is how psychological states change bodies. Its second half is how help reaches the "
            "people who need it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(nl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in b], lag_ratio=0.3))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        rows_section(self, r"Today: \ how does the mind get into the body, \ and how does help get to people?", [
            (r"stress, \ placebo and expectation", SYMP),
            (r"pain, \ behaviour, \ sleep and mindfulness", MODEL),
            (r"the treatment gap, \ stepped care and feedback", PERSON),
            (r"help at scale, \ and what failed", GOOD),
        ], "So this part asks: how does the mind get into the body, and how does help get to the people who need it? "
           "<bookmark mark='a'/> Stress, placebo and expectation. <bookmark mark='b'/> Pain, behaviour, sleep and "
           "mindfulness. <bookmark mark='c'/> The treatment gap, stepped care and feedback. <bookmark mark='d'/> And "
           "help at scale, and what failed.", font_size=27, buff=0.48)

    def objectives(self):
        head = VGroup(label(r"Part 57", font_size=34, color=GREY_B), label(r"Health and Care", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"stress and illness, \ and the limits of correlation",
            r"placebo: \ what survives the critique, \ and why",
            r"expectation as a prior on bodily signals; \ nocebo",
            r"behaviour as treatment: \ adherence, \ diabetes prevention, \ sleep",
            r"the treatment gap and stepped care, \ simulated",
            r"lay counsellors, \ digital therapeutics, \ and personality and the heart",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 57 of Psychology, Built: health and care, the last part of Act Twelve. <bookmark mark='a'/> "
            "We'll weigh stress and illness, and the limits of correlation. We'll see what survives of the placebo, "
            "and why. We'll treat expectation as a prior on the body's signals. We'll make behaviour the treatment, "
            "for diabetes and for sleep. We'll simulate the treatment gap and stepped care. And we'll meet lay "
            "counsellors, digital therapeutics, and the personality that was said to cause heart attacks."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
