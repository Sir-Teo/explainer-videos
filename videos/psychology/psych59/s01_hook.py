from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.care()
        self.paradox()
        self.question()
        self.objectives()

    def care(self):
        card = care_card().move_to([0, 0, 0])
        with self.voiceover(
            "Before we start. This part is about psychiatry and mental illness, including depression, anxiety and "
            "compulsive disorders. <bookmark mark='a'/> It's education, not diagnosis or treatment. If any of it "
            "touches your own life, talk to a doctor, a counsellor, or someone you trust. <bookmark mark='b'/> If "
            "you're in danger now, call your local emergency number. In the United States you can call or text nine "
            "eight eight. In the UK and Ireland, Samaritans are on one one six, one two three. And find a helpline dot "
            "com lists free, confidential lines in other countries."
        ) as vo:
            self.play(FadeIn(card.box), FadeIn(card.head))
            vo.wait_until("a")
            self.play(FadeIn(card.body))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.6), run_time=3.0)
        self.wait(1.5)
        self.clear_scene()

    def paradox(self):
        d = load("paradox")
        head = heading(r"Robust effects, \ unreliable people")
        s1, s2 = np.asarray(d["s1"]), np.asarray(d["s2"])
        A = axes([-150, 260], [-150, 260], x_length=4.2, y_length=4.0, xticks=[0, 100, 200], yticks=[0, 100, 200],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"effect, \ session 1 (ms)",
                 ylabel=r"effect, \ session 2 (ms)", center=[-3.9, 0.0, 0], font_size=12)
        pts = scatter(A.ax, np.clip(s1, -145, 255), np.clip(s2, -145, 255), CROWD, radius=0.03)
        rows = rows_of([
            (r"the plan: \ give a patient a task from Acts IV and V, \ fit the model, \ read off the parameter that "
             r"has gone wrong", WHITE),
            (rf"Psyche's 400 people do a Stroop-like task twice: \ the group effect is enormous, \ $t$ = {d['t']:.0f}",
             GOOD),
            (rf"but each person's effect barely repeats: \ test-retest $r$ = {d['retest_r']:.2f}", AUTH),
            (r"Hedge, \ Powell and Sumner, \ 2018: \ the tasks are trusted because everyone shows the effect, \ which "
             r"is why they cannot tell people apart", MODEL),
            (r"this part is a young field's promise, \ and the measurement discipline of Part 3 it is relearning", YOU),
        ], 7.0, 19, 0.34).move_to([2.9, -0.1, 0])
        tag = psyche_tag(r"\texttt{precision.paradox}, \ 400 simulated people")
        with self.voiceover(
            "Here's the plan of computational psychiatry. <bookmark mark='a'/> Give a patient a task from Acts Four "
            "and Five, fit the model, and read off the parameter that has gone wrong. Then choose the treatment. "
            "<bookmark mark='b'/> But here's the first obstacle. Psyche's four hundred people do a Stroop-like task "
            "twice. The group effect is enormous, with a t statistic near fifty. <bookmark mark='c'/> But each "
            "person's effect barely repeats: the test-retest correlation is about zero point three. "
            "<bookmark mark='d'/> Craig Hedge, Gavin Powell and Petroc Sumner called it the reliability paradox in "
            "2018. The tasks are trusted because everyone shows the effect, and that's exactly why they can't tell "
            "people apart. <bookmark mark='e'/> This part is a young field's promise, and the measurement discipline "
            "of Part 3 it's having to relearn."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(pts))
            for m, r in zip("de", rows[3:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        rows_section(self, r"Today: \ can a model of the mind tell a clinician something a conversation cannot?", [
            (r"the programme, \ and two worked cases", SYMP),
            (r"measurement: \ reliability, \ biotypes, \ prediction that travels", MODEL),
            (r"choosing treatments, \ and new interventions", PERSON),
            (r"phones, \ and what would count as a target", GOOD),
        ], "So this part asks: can a model of the mind tell a clinician something a conversation can't? "
           "<bookmark mark='a'/> The programme, and two worked cases. <bookmark mark='b'/> Measurement: reliability, "
           "biotypes, and prediction that travels. <bookmark mark='c'/> Choosing treatments, and new interventions. "
           "<bookmark mark='d'/> And phones, and what would count as a target.", font_size=27, buff=0.48)

    def objectives(self):
        head = VGroup(label(r"Part 59", font_size=34, color=GREY_B), label(r"Computational Psychiatry", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the reliability paradox, \ and the trials it costs",
            r"theory-driven and data-driven computational psychiatry",
            r"compulsivity, \ volatility and mood as computations",
            r"biotypes that are not there, \ and how to tell",
            r"prediction that fails in a new trial, \ and treatment selection's sample",
            r"stimulation, \ psychedelics and phones, \ judged by Part 2's standards",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 59 of Psychology, Built: computational psychiatry. <bookmark mark='a'/> We'll meet the "
            "reliability paradox, and count the trials it costs. We'll separate theory-driven and data-driven "
            "programmes. We'll look at compulsivity, volatility and mood as computations. We'll find biotypes in data "
            "that has none, and learn how to tell. We'll watch prediction fail in a new trial, and size a trial for "
            "choosing treatments. And we'll judge stimulation, psychedelics and phones by Part 2's standards."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
