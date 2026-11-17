from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.care()
        self.eysenck()
        self.answer()
        self.question()
        self.objectives()

    def care(self):
        card = care_card().move_to([0, 0, 0])
        with self.voiceover(
            "Before we start. This part is about whether therapy works, and it touches on trauma and self-harm. "
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

    def eysenck(self):
        head = heading(r"Two thirds recover anyway")
        A = axes([0.3, 3.7], [0, 100], x_length=5.0, y_length=3.0, xticks=None, yticks=[0, 50, 100],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"improved", center=[-3.4, 0.5, 0], font_size=13)
        b = bars(A.ax, [1, 2, 3], [44, 64, 72], [SYMP, PERSON, GREY_B], width=0.6)
        names = VGroup(*[wrapped_label(t, 1.5, 13, c).next_to(A.ax.c2p(x, 0), DOWN, buff=0.15) for x, t, c in
                         ((1, r"psychoanalysis", SYMP), (2, r"eclectic therapy", PERSON),
                          (3, r"custodial care, \ no therapy", GREY_B))])
        rows = rows_of([
            (r"Eysenck, \ 1952: \ he gathered the outcome reports of the day for neurotic patients", WHITE),
            (r"about two thirds improved within two years with eclectic therapy, \ and about as many in custodial care "
             r"with no therapy at all", PERSON),
            (r"his conclusion: \ the studies failed to show that psychotherapy helps", AUTH),
            (r"the challenge stood for 25 years: \ answering it needed controls, \ and a way to add up studies", YOU),
        ], 6.0, 20, 0.4).move_to([3.4, -0.2, 0])
        tag = historical_tag(r"Eysenck (1952)")
        with self.voiceover(
            "In 1952 the psychologist Hans Eysenck threw down a challenge. <bookmark mark='a'/> He gathered the "
            "outcome reports of the day for neurotic patients, people with anxiety and depression. "
            "<bookmark mark='b'/> About two thirds improved within two years with eclectic therapy. And about as many "
            "improved in custodial care, with no therapy at all. <bookmark mark='c'/> His conclusion: the studies "
            "failed to show that psychotherapy helps. <bookmark mark='d'/> The challenge stood for twenty-five years. "
            "Answering it needed proper control groups, and a way to add up many studies."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in b], lag_ratio=0.4))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def answer(self):
        head = heading(r"An answer, \ and harder questions")
        rows = rows_of([
            (r"1977: \ Smith and Glass pooled 375 controlled studies with a new method, \ meta-analysis, \ and found "
             r"the average treated client better off than about three quarters of untreated ones", GOOD),
            (r"then the harder questions: \ better than what? \ through which ingredient? \ and how much of the "
             r"published effect is real?", PERSON),
            (r"Eysenck's deeper point survives: \ people improve anyway, \ and only a control group can say how "
             r"much of the improvement therapy caused", YOU),
        ], 12.4, 24, 0.5).move_to([0, -0.3, 0])
        with self.voiceover(
            "The answer came in 1977. <bookmark mark='a'/> Mary Lee Smith and Gene Glass pooled three hundred and "
            "seventy-five controlled studies with a new method, meta-analysis, and found the average treated client "
            "better off than about three quarters of untreated ones. <bookmark mark='b'/> Then came the harder "
            "questions. Better than what? Through which ingredient? And how much of the published effect is real? "
            "<bookmark mark='c'/> Eysenck's deeper point survives. People improve anyway, and only a control group "
            "can say how much of the improvement therapy caused."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ how would you know that talking helped?")
        rows = rows_of([
            (r"the trial: \ randomization, \ and the choice of control", SYMP),
            (r"meta-analysis, \ the dodo bird, \ and the alliance between client and therapist", MODEL),
            (r"the therapies, \ medication, \ and the published effect against the real one", PERSON),
            (r"clinical significance, \ treatments that harm, \ and how much therapy is enough", GOOD),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks how you would know that talking to someone helped. <bookmark mark='a'/> It starts "
            "with the trial: randomization, and the choice of control. <bookmark mark='b'/> Then meta-analysis, the "
            "dodo bird, and the alliance between client and therapist. <bookmark mark='c'/> Then the therapies, "
            "medication, and the published effect against the real one. <bookmark mark='d'/> And finally clinical "
            "significance, treatments that harm, and how much therapy is enough."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 42", font_size=34, color=GREY_B), label(r"Does Therapy Work?", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"why everyone improves: \ regression to the mean and natural recovery",
            r"controls, \ and how the control sets the effect",
            r"meta-analysis by hand, \ the dodo bird and the alliance",
            r"the therapies, \ and therapy against medication",
            r"publication bias, \ and clinical significance derived",
            r"treatments that harm, \ the body treatments, \ and the dose of therapy",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 42 of Psychology, Built: does therapy work? <bookmark mark='a'/> We'll see why everyone "
            "improves, through regression to the mean and natural recovery. We'll see how the control condition "
            "sets the effect. We'll do a meta-analysis by hand, and meet the dodo bird and the alliance. We'll weigh "
            "the therapies, and therapy against medication. We'll measure publication bias, and derive clinical "
            "significance. And we'll end with treatments that harm, the body treatments, and the dose of therapy."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
