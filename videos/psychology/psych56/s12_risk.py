from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403


class Risk(VoiceoverScene):
    def construct(self):
        card_section(self, 11, r"Risk assessment", r"Can a formula predict who will reoffend, \ fairly?",
                     scale=("society",))
        self.actuarial()
        self.impossible()

    def actuarial(self):
        rows_section(self, r"Actuarial against clinical", [
            (r"Part 39's Meehl: \ a formula combining a few factors usually predicts at least as well as a clinician's "
             r"judgement", WHITE),
            (r"risk tools for bail, \ sentencing and parole score age, \ criminal history and other factors; \ their "
             r"accuracy is moderate (areas under the ROC around 0.7)", MODEL),
            (r"Dressel and Farid, \ 2018: \ untrained people online predicted reoffending about as accurately as a "
             r"commercial tool, \ around 65\%", AUTH),
            (r"the question is not machine against human, \ but what the tool's errors are, \ and who bears them", YOU),
        ], "Can a formula predict who'll reoffend, and fairly? <bookmark mark='a'/> Part 39's Meehl found that a "
           "formula combining a few factors usually predicts at least as well as a clinician's judgement. "
           "<bookmark mark='b'/> Risk tools for bail, sentencing and parole score age, criminal history and other "
           "factors. Their accuracy is moderate, with areas under the ROC curve around zero point seven. "
           "<bookmark mark='c'/> Julia Dressel and Hany Farid found in 2018 that untrained people online predicted "
           "reoffending about as accurately as a commercial tool, around sixty-five percent. <bookmark mark='d'/> So "
           "the question isn't machine against human. It's what the tool's errors are, and who bears them.",
           tag=published_tag(r"Dressel \& Farid (2018)"))

    def impossible(self):
        d = load("risk")
        head = heading(r"Calibrated, \ and unequal")
        A = axes([0.3, 4.7], [0, 0.65], x_length=5.4, y_length=3.0, xticks=None, yticks=[0, 0.2, 0.4, 0.6],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"rate", center=[-3.3, 0.3, 0], font_size=12)
        vals = [d["fpr"][0], d["fpr"][1], d["fnr"][0], d["fnr"][1]]
        b = bars(A.ax, [1, 2, 3.3, 4.3], vals, [MODEL, PERSON, MODEL, PERSON], width=0.6)
        names = VGroup(*[label(s, font_size=12, color=GREY_A).next_to(A.ax.c2p(x, 0), DOWN, buff=0.12)
                         for s, x in zip([r"group A", r"group B", r"group A", r"group B"], [1, 2, 3.3, 4.3])])
        what = VGroup(label(r"false positives", font_size=13, color=GREY_B).next_to(A.ax.c2p(1.5, 0), DOWN, buff=0.5),
                      label(r"false negatives", font_size=13, color=GREY_B).next_to(A.ax.c2p(3.8, 0), DOWN, buff=0.5))
        rows = rows_of([
            (r"one risk score, \ calibrated in both groups: \ the same score means the same chance of reoffending; \ "
             r"base rates 30\% and 50\%; \ flag above a 50\% risk", WHITE),
            (rf"false-positive rates: \ {100 * d['fpr'][0]:.0f}\% in group A, \ {100 * d['fpr'][1]:.0f}\% in group B; \ "
             rf"false negatives the other way round", AUTH),
            (r"Chouldechova, \ and Kleinberg and colleagues, \ 2016-17: \ with unequal base rates, \ no score can be "
             r"calibrated and have equal error rates in both groups", MODEL),
            (r"ProPublica's 2016 analysis and the tool's makers were each right by a different definition; \ choosing "
             r"the definition is a decision about values (\emph{Statistics, Built} Part 63)", YOU),
        ], 6.0, 19, 0.34).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.risk\_groups}")
        with self.voiceover(
            "Here's why fairness is hard. <bookmark mark='a'/> Take one risk score, calibrated in both groups, so the "
            "same score means the same chance of reoffending. The base rates are thirty and fifty percent, and the "
            "tool flags anyone above fifty percent risk. <bookmark mark='b'/> The false-positive rates are ten "
            "percent in group A and twenty-eight in group B, and the false negatives run the other way. "
            "<bookmark mark='c'/> Alexandra Chouldechova, and Jon Kleinberg and colleagues, proved in 2016 and 2017 "
            "that with unequal base rates, no score can be calibrated and have equal error rates in both groups. "
            "<bookmark mark='d'/> ProPublica's 2016 analysis and the tool's makers were each right, by a different "
            "definition. Choosing the definition is a decision about values. Statistics, Built's Part 63 works it "
            "through."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(what))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
