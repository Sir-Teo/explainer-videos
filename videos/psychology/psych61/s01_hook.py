from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.challenge()
        self.question()
        self.objectives()

    def challenge(self):
        d = load("challenge")
        head = heading(r"A hundred and sixty teams")
        sc = np.asarray(d["scores"])
        A = axes([0, len(sc)], [-0.05, 0.25], x_length=5.6, y_length=3.2, xticks=None, yticks=[0, 0.1, 0.2],
                 yfmt=lambda v: f"{v:g}", ylabel=r"held-out $R^2$", center=[-3.3, 0.2, 0], font_size=12)
        dots = VGroup(*[Dot(A.ax.c2p(i + 0.5, float(max(v, -0.05))), radius=0.03, color=MODEL)
                        for i, v in enumerate(sc)])
        base = DashedLine(A.ax.c2p(0, d["baseline"]), A.ax.c2p(len(sc), d["baseline"]), color=AUTH, stroke_width=2)
        ceil = DashedLine(A.ax.c2p(0, d["ceiling"]), A.ax.c2p(len(sc), d["ceiling"]), color=GOOD, stroke_width=2)
        key = VGroup(label(r"teams, \ sorted", font_size=13, color=MODEL),
                     label(r"four variables, \ least squares", font_size=13, color=AUTH),
                     label(r"the most any model could get", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.3)
        key.next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"Salganik and colleagues, \ 2020: \ 160 teams, \ thousands of variables on about 4,000 families, \ any "
             r"method: \ predict six outcomes in the children's lives", WHITE),
            (r"the best models barely beat a four-variable regression, \ and explained little of the variance", AUTH),
            (rf"Psyche's cohort: \ the best of 160 teams scores {d['best']:.2f}, \ the four-variable regression "
             rf"{d['baseline']:.2f}, \ and no model could exceed {d['ceiling']:.2f}", MODEL),
            (r"a field that explains much and predicts little has to decide what it is for", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{community.challenge}")
        tag2 = published_tag(r"Salganik et al.\ (2020)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "In 2020 Matthew Salganik and colleagues ran a contest. <bookmark mark='a'/> A hundred and sixty teams got "
            "thousands of variables on about four thousand families, and could use any method they liked, to predict "
            "six outcomes in the children's lives, like their grades at fifteen. <bookmark mark='b'/> The best models "
            "barely beat a regression on four variables, and explained little of the variance. "
            "<bookmark mark='c'/> Here's the same contest on a cohort Psyche simulated. The best of a hundred and "
            "sixty teams scores zero point one three, and so does the four-variable regression, under a ceiling of "
            "zero point two that no model could exceed. <bookmark mark='d'/> A field that explains much and predicts "
            "little has to decide what it's for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(base))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.01), Create(ceil),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def question(self):
        rows_section(self, r"Today: \ what would psychology look like if it were designed today?", [
            (r"prediction, \ explanation, \ and how to have both", SYMP),
            (r"bigger teams, \ bigger and broader samples", MODEL),
            (r"experiments as spaces, \ theories as code, \ machines that help find theories", PERSON),
            (r"a model of the research community itself, \ and the proposals ranked by evidence", GOOD),
        ], "So this part asks: what would psychology look like if it were designed today? <bookmark mark='a'/> "
           "Prediction, explanation, and how to have both. <bookmark mark='b'/> Bigger teams, and bigger and broader "
           "samples. <bookmark mark='c'/> Experiments designed as spaces instead of points, theories written as code, "
           "and machines that help find theories. <bookmark mark='d'/> A model of the research community itself, and "
           "the proposals ranked by the evidence that they work.", font_size=27, buff=0.48)

    def objectives(self):
        head = VGroup(label(r"Part 61", font_size=34, color=GREY_B), label(r"The Next Psychology", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"separate explanation from prediction, \ and say what each buys",
            r"read many-labs heterogeneity, \ and what big samples can and cannot fix",
            r"design an experiment as a space, \ with a surrogate model",
            r"write a theory as code that makes a risky prediction",
            r"run a model of a research community under two sets of incentives",
            r"rank the reform proposals by the evidence that they work",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 61 of Psychology, Built: the next psychology. <bookmark mark='a'/> We'll separate "
            "explanation from prediction, and say what each buys. We'll read many-labs heterogeneity, and what big "
            "samples can and can't fix. We'll design an experiment as a space, with a surrogate model. We'll write a "
            "theory as code that makes a risky prediction. We'll run a model of a research community under two sets "
            "of incentives. And we'll rank the reform proposals by the evidence that they work."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
