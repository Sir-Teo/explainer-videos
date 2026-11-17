from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403


class Travel(VoiceoverScene):
    def construct(self):
        card_section(self, 8, r"Prediction that does not travel", r"Will a model that predicts response work in the "
                     r"next clinic?")
        self.chekroud()
        self.three()
        self.why()

    def chekroud(self):
        rows_section(self, r"Predicting who responds", [
            (r"Chekroud and colleagues, \ 2016: \ 25 baseline questions from about 1,900 patients in a large "
             r"antidepressant trial, \ a machine-learning model of who would remit", WHITE),
            (r"tested in another trial: \ about 60\% accuracy in a similar drug arm, \ little above chance in a "
             r"different one", MODEL),
            (r"Chekroud and colleagues, \ 2024: \ five antipsychotic trials, \ train in one and test in the others", AUTH),
            (r"good within the trial a model was built in; \ close to chance in the others", AUTH),
        ], "Will a model that predicts response work in the next clinic? <bookmark mark='a'/> In 2016 Adam Chekroud "
           "and colleagues took twenty-five baseline questions from about nineteen hundred patients in a large "
           "antidepressant trial, and trained a machine-learning model of who would remit. <bookmark mark='b'/> "
           "Tested in another trial, it was about sixty percent accurate in a similar drug arm, and little better "
           "than chance in a different one. <bookmark mark='c'/> In 2024 the same group took five antipsychotic "
           "trials, trained in one, and tested in the others. <bookmark mark='d'/> Models were good within the trial "
           "they were built in, and close to chance in the others.", tag=published_tag(r"Chekroud et al.\ (2024)"))

    def three(self):
        d = load("travel")
        head = heading(r"Three accuracies for one model")
        A = axes([0.4, 3.6], [0.5, 0.8], x_length=5.2, y_length=3.0, xticks=None, yticks=[0.5, 0.6, 0.7, 0.8],
                 yfmt=lambda v: f"{v:g}", ylabel=r"AUC", center=[-3.4, 0.3, 0], font_size=12)
        vals = [d["apparent"], d["cv"], d["new_trial"]]
        cols = [AUTH, MODEL, GOOD]
        bs = [bars(A.ax, [i + 1], [v], c, width=0.6) for i, (v, c) in enumerate(zip(vals, cols))]
        names = VGroup(*[label(t, font_size=13, color=c).next_to(A.ax.c2p(i + 1, 0.5), DOWN, buff=0.12)
                         for i, (t, c) in enumerate(zip([r"same data", r"cross-validated", r"new trial"], cols))])
        nums = VGroup(*[label(f"{v:.2f}", font_size=15, color=c).next_to(b, UP, buff=0.06)
                        for v, c, b in zip(vals, cols, bs)])
        rows = rows_of([
            (r"Psyche's trials: \ 300 patients, \ 40 baseline features, \ three weakly predictive; \ the model keeps "
             r"the ten best and fits a logistic regression", WHITE),
            (rf"scored on the data it was built from: \ AUC {d['apparent']:.2f}", AUTH),
            (rf"honest cross-validation, \ selection inside each fold: \ {d['cv']:.2f}", MODEL),
            (rf"a new trial, \ another site, \ relations drifted a little: \ {d['new_trial']:.2f}; \ your third number",
             GOOD),
        ], 6.2, 19, 0.36).move_to([3.3, -0.1, 0])
        tag = psyche_tag(r"\texttt{precision.cross\_trial}, \ 60 pairs of trials")
        with self.voiceover(
            "Here are three accuracies for one model. <bookmark mark='a'/> Psyche's trials have three hundred patients "
            "and forty baseline features, of which three are weakly predictive. The model keeps the ten best features "
            "and fits a logistic regression. <bookmark mark='b'/> Scored on the data it was built from, the AUC is "
            "zero point seven two. <bookmark mark='c'/> Honest cross-validation, with feature selection inside each "
            "fold, gives zero point five nine. <bookmark mark='d'/> In a new trial at another site, where the "
            "relations have drifted a little, it's zero point five seven. That's your third number."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for m, r_, b, n_ in zip("bcd", rows[1:], bs, nums):
                vo.wait_until(m)
                self.play(FadeIn(r_), GrowFromEdge(b, DOWN), FadeIn(n_))
        self.clear_scene()

    def why(self):
        chips_section(self, r"Why prediction does not travel", [
            (r"selection on all the data", r"choosing features before cross-validation leaks the answer into the "
                                           r"estimate", AUTH),
            (r"different patients", r"inclusion criteria, \ sites and severity shift the features' distribution", SYMP),
            (r"different relations", r"protocols, \ doses and raters change how features relate to outcome", MODEL),
            (r"a small signal", r"when the true signal is weak, \ noise the model learned is a large share of what "
                                r"it knows", PERSON),
            (r"the standard", r"external validation in an independent sample, \ registered before it is run "
                              r"(TRIPOD)", GOOD),
        ], "Why doesn't prediction travel? <bookmark mark='a'/> Selection on all the data: choosing features before "
           "cross-validation leaks the answer into the estimate. <bookmark mark='b'/> Different patients: inclusion "
           "criteria, sites and severity shift the features' distribution. <bookmark mark='c'/> Different relations: "
           "protocols, doses and raters change how features relate to outcome. <bookmark mark='d'/> A small signal: "
           "when the true signal is weak, the noise a model learned is a large share of what it knows. "
           "<bookmark mark='e'/> And the standard to ask for: external validation in an independent sample, "
           "registered before it's run, as the TRIPOD reporting guideline sets out.")
