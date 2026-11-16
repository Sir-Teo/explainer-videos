from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.estes()
        self.craft()
        self.question()
        self.objectives()

    def estes(self):
        d = load("jump")
        head = heading(r"A curve no animal had")
        A = axes([0, 40], [0, 1], x_length=5.6, y_length=3.4, xticks=[0, 10, 20, 30, 40], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"trial", ylabel=r"P(correct)",
                 center=[-3.3, 0.3, 0], font_size=13)
        cols = [SYMP, PERSON, GOOD, AUTH, MODEL, CARE, YOU, GREY_A]
        steps = VGroup(*[curve(A.ax, d["t"], y, c, stroke_width=2) for y, c in zip(d["each"], cols)])
        avg = curve(A.ax, d["t"], d["mean"], WHITE, stroke_width=5)
        rows = rows_of([
            (r"1956: \ William Estes asks what a smooth learning curve means", WHITE),
            (r"Psyche's learners each jump from guessing to knowing on one trial: \ every curve is a step", PERSON),
            (r"average 200 of them, \ and a smooth, \ gradual curve appears: \ the shape of no learner at all", MODEL),
            (r"a model fitted to the average would describe a mind that does not exist; \ this part is the craft of "
             r"not fooling yourself with models", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.jump\_learners}, \ 200 simulated learners")
        with self.voiceover(
            "In 1956 the psychologist William Estes asked what a smooth learning curve means. <bookmark mark='a'/> "
            "Here are some of Psyche's learners. Each jumps from guessing to knowing on a single trial, so every "
            "curve is a step. <bookmark mark='b'/> Average two hundred of them, and a smooth, gradual curve appears. "
            "It's the shape of no learner at all. <bookmark mark='c'/> A model fitted to that average would describe "
            "a mind that doesn't exist. This part is the craft of not fooling yourself with models."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), LaggedStart(*[Create(s) for s in steps], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), Create(avg))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def craft(self):
        head = heading(r"Every part has fitted models")
        rows = rows_of([
            (r"Part 17 fitted learning rates; \ Part 25 fitted diffusion models; \ Part 40 fitted a model of mood", WHITE),
            (r"each time, \ a program that turns parameters into behaviour, \ and a search for the parameters that "
             r"make the data most likely", MODEL),
            (r"this part opens the harness: \ can the parameters be recovered? \ can the models be told apart? \ "
             r"does the winner reproduce the data's signature?", PERSON),
            (r"a model is more than a curve fit when it could have failed, \ and did not", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "The series has fitted models all along. <bookmark mark='a'/> Part 17 fitted learning rates. Part 25 "
            "fitted diffusion models, and Part 40 a model of mood. <bookmark mark='b'/> "
            "Each time, a program that turns parameters into behaviour, and a search for the parameters that make the "
            "data most likely. <bookmark mark='c'/> This part opens that harness. Can the parameters be recovered? Can "
            "the models be told apart? Does the winner reproduce the data's signature? <bookmark mark='d'/> A model "
            "is more than a curve fit when it could have failed, and didn't."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ when is a model of the mind more than a curve fit?")
        rows = rows_of([
            (r"generative models, \ likelihoods and fitting", SYMP),
            (r"recovery, \ trade-offs and model comparison", MODEL),
            (r"posterior prediction, \ hierarchy and averages", PERSON),
            (r"rational analysis, \ networks and language models", GOOD),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks when a computational model of the mind is more than a curve fit. "
            "<bookmark mark='a'/> Generative models, likelihoods and fitting. <bookmark mark='b'/> Recovery, "
            "trade-offs and model comparison. <bookmark mark='c'/> Posterior prediction, hierarchy, and the danger of "
            "averages. <bookmark mark='d'/> And rational analysis, neural networks, and language models offered as "
            "models of minds."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 48", font_size=34, color=GREY_B), label(r"Modelling Behaviour", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"a cognitive model as a generative program",
            r"maximum likelihood with restarts, \ and its traps",
            r"parameter recovery, \ and parameters that trade off",
            r"model comparison and model recovery",
            r"posterior predictive checks, \ and hierarchical fits",
            r"averages that describe no one, \ networks and language models",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 48 of Psychology, Built: modelling behaviour. <bookmark mark='a'/> We'll treat a cognitive "
            "model as a program that generates behaviour. We'll fit it by maximum likelihood, with restarts, and meet "
            "the traps. We'll check whether parameters can be recovered, and see two that trade off. We'll compare "
            "models, and check that comparison can tell them apart. We'll ask whether a winning model reproduces the "
            "data, and fit people as a population. And we'll see averages that describe no one, then neural networks "
            "and language models offered as models of minds."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
