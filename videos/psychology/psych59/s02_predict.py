from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"A task's effect: \ 200 trials per condition, \ reliability 0.5. \ How many trials for 0.9?", PERSON),
    (r"2", r"Cluster 220 patients' brain data that has no subgroups at all. \ How often do the clusters differ in "
           r"symptoms?", MODEL),
    (r"3", r"A model predicts treatment outcome with AUC 0.72 in its own trial. \ In a new trial?", AUTH),
    (r"4", r"A trial to show a treatment works needs 350 patients. \ To show a rule for choosing treatments works?",
     GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        card_section(self, 1, r"On you: \ design a task, \ and four numbers", r"Can a task be good for groups and "
                     r"for individuals?")
        self.slider()
        self.quiz()

    def slider(self):
        d = load("tradeoff")
        head = heading(r"The designer's slider")
        A = axes([0, 1], [0, 1.0], x_length=5.6, y_length=3.2, xticks=[0, 0.5, 1.0], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"share of the effect that varies "
                 r"between people", ylabel=r"reliability", center=[-3.3, 0.2, 0], font_size=12)
        cols = [AUTH, PERSON, MODEL, SYMP, GOOD, CARE]
        sh = np.asarray(d["shares"])
        cs = VGroup(*[curve(A.ax, sh, np.asarray(d["reliability"])[i], cols[i], stroke_width=3) for i in range(6)])
        key = VGroup(*[label(rf"{int(n)}", font_size=12, color=c) for n, c in zip(d["trials"], cols)])
        key.arrange(RIGHT, buff=0.25).next_to(A, UP, buff=0.2)
        kt = label(r"trials per condition:", font_size=12, color=GREY_A).next_to(key, LEFT, buff=0.2)
        rows = rows_of([
            (r"on the course site: \ a slider moves a task's effect between uniform (everyone shows it) and variable "
             r"(people differ)", WHITE),
            (r"uniform: \ a huge group effect, \ useless reliability; \ variable: \ the reverse", AUTH),
            (r"each curve is a number of trials: \ only more trials buy both", GOOD),
            (r"the cost is time with a patient: \ the clinic's real currency", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{precision.design\_tradeoff}")
        with self.voiceover(
            "First, a slider. <bookmark mark='a'/> On the course site, you move a task's effect between uniform, "
            "where everyone shows it, and variable, where people differ. <bookmark mark='b'/> Uniform gives a huge "
            "group effect and useless reliability. Variable gives the reverse. <bookmark mark='c'/> Each curve here "
            "is a number of trials, and only more trials buy both. <bookmark mark='d'/> The cost is time with a "
            "patient, which is the clinic's real currency."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key), FadeIn(kt))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[Create(c_) for c_ in cs], lag_ratio=0.2))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 21, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers. <bookmark mark='a'/> One: a task's effect with two hundred trials per condition has "
            "reliability zero point five. How many trials for zero point nine? <bookmark mark='b'/> Two: cluster two "
            "hundred and twenty patients' brain data that has no subgroups at all. How often do the clusters differ "
            "in symptoms? <bookmark mark='c'/> Three: a model predicts treatment outcome with an AUC of zero point "
            "seven two in its own trial. What about in a new trial? <bookmark mark='d'/> And four: a trial to show a "
            "treatment works needs three hundred and fifty patients. How many to show that a rule for choosing "
            "treatments works? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
