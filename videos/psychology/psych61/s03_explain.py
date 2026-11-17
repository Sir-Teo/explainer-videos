from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403


class Explain(VoiceoverScene):
    def construct(self):
        card_section(self, 2, r"Explanation and prediction", r"What is psychology for?", marr=("what",))
        self.yarkoni()
        self.overfit()
        self.both()

    def yarkoni(self):
        chips_section(self, r"Two goals", [
            (r"explanation", r"identify causes and mechanisms, \ usually by testing whether a coefficient differs "
                             r"from zero in one sample", MODEL),
            (r"prediction", r"forecast new cases accurately, \ judged on data the model has not seen", PERSON),
            (r"Yarkoni and Westfall, \ 2017", r"psychology chose explanation, \ and its models often predict "
                                              r"poorly out of sample, \ which should worry an explainer too", AUTH),
            (r"overfitting", r"Part 59's lesson: \ in-sample fit flatters every model, \ explanatory ones included",
             SYMP),
        ], "What is psychology for? There are two goals. <bookmark mark='a'/> Explanation identifies causes and "
           "mechanisms, usually by testing whether a coefficient differs from zero in one sample. "
           "<bookmark mark='b'/> Prediction forecasts new cases accurately, judged on data the model hasn't seen. "
           "<bookmark mark='c'/> In 2017 Tal Yarkoni and Jacob Westfall argued that psychology chose explanation, and "
           "that its models often predict poorly out of sample, which should worry an explainer too. "
           "<bookmark mark='d'/> That's Part 59's lesson: in-sample fit flatters every model, explanatory ones "
           "included.", tag=published_tag(r"Yarkoni \& Westfall (2017)"), chip_w=4.0, text_w=8.0)

    def both(self):
        rows_section(self, r"Having both", [
            (r"Hofman and colleagues, \ 2021: \ integrative modelling: \ causal models that are also scored on "
             r"held-out prediction", WHITE),
            (r"report the ceiling: \ how predictable is the outcome at all, \ given the noise in it?", MODEL),
            (r"a theory that explains a little of the variance can still be right and useful: \ small causes add "
             r"up across a population", GOOD),
            (r"and a model that predicts well can still be wrong about causes (Part 47's within and between)", AUTH),
        ], "How do you have both? <bookmark mark='a'/> Jake Hofman and colleagues proposed integrative modelling in "
           "2021: causal models that are also scored on held-out prediction. <bookmark mark='b'/> Report the ceiling: "
           "how predictable is the outcome at all, given the noise in it? <bookmark mark='c'/> A theory that "
           "explains a little of the variance can still be right and useful, because small causes add up across a "
           "population. <bookmark mark='d'/> And a model that predicts well can still be wrong about causes, Part "
           "47's lesson about within and between.", tag=published_tag(r"Hofman et al.\ (2021)"))

    def overfit(self):
        d = load("overfit")
        head = heading(r"More variables, \ less prediction")
        x = np.log2(d["k"])
        A = axes([-0.3, 9.0], [-0.35, 0.6], x_length=5.6, y_length=3.2, xticks=[0, 2, 4, 6, 8],
                 yticks=[-0.2, 0, 0.2, 0.4], xfmt=lambda v: f"{2 ** v:.0f}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"variables in the model", ylabel=r"$R^2$", center=[-3.3, 0.3, 0], font_size=12)
        zero = DashedLine(A.ax.c2p(-0.3, 0), A.ax.c2p(9.0, 0), color=GREY_C, stroke_width=2)
        ceil = DashedLine(A.ax.c2p(-0.3, d["true_r2"]), A.ax.c2p(9.0, d["true_r2"]), color=GOOD, stroke_width=2)
        ci = curve(A.ax, x, d["in"], AUTH, stroke_width=4)
        co = curve(A.ax, x, d["out"], PERSON, stroke_width=4)
        key = VGroup(label(r"in the sample it was fitted to", font_size=13, color=AUTH),
                     label(r"on new people", font_size=13, color=PERSON),
                     label(r"the ceiling", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.35)
        key.next_to(A, UP, buff=0.2)
        k_best = int(d["k"][int(np.argmax(d["out"]))])
        rows = rows_of([
            (r"Psyche's cohort: \ 400 baseline variables, \ four with clear effects and the rest tiny; \ least "
             r"squares on 1{,}000 people, \ scored on 3{,}000 others", WHITE),
            (rf"in the sample, \ $R^2$ rises with every variable: \ {d['in'][-1]:.2f} with all 400", AUTH),
            (rf"on new people it peaks at {d['out'].max():.2f} with {k_best} variables, \ and falls to "
             rf"{d['out'][-1]:.2f}: \ worse than predicting the average", PERSON),
            (rf"the true ceiling is {d['true_r2']:.2f}: \ most of the outcome is noise, \ and no method can beat "
             r"that", GOOD),
            (r"an explanatory paper reports the red curve; \ the question it should also answer is the gold one", YOU),
        ], 6.0, 18, 0.32).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{community.cohort}, \ least squares")
        with self.voiceover(
            "Here is the problem in one picture. <bookmark mark='a'/> Psyche's cohort has four hundred baseline "
            "variables, four with clear effects and the rest tiny. A model is fitted by least squares to a thousand "
            "people, and scored on three thousand others. <bookmark mark='b'/> In the sample, R squared rises with "
            "every variable added, to over half with all four hundred. <bookmark mark='c'/> On new people it peaks "
            "at about zero point one six with four variables, and then falls below zero: worse than just predicting "
            "the average. <bookmark mark='d'/> The true ceiling is about zero point two. Most of the outcome is noise, "
            "and no method can beat that. <bookmark mark='e'/> An explanatory paper reports the red curve. The "
            "question it should also answer is the gold one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(ci), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(co), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Create(ceil))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
