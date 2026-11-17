from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403


class Repeated(VoiceoverScene):
    def construct(self):
        self.card()
        self.averaging()
        self.levels()
        self.neff()

    def card(self):
        card = chapter_card(2, r"Repeated measures", r"What does averaging over trials throw away?",
                            lit={1982: r"Laird \& Ware", 2008: r"Baayen et al."}, part=PART, scale=("person",),
                            marr=("how",))
        with self.voiceover("Chapter two. Repeated measures."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def averaging(self):
        head = heading(r"Averaging throws away the structure")
        rows = rows_of([
            (r"a typical experiment: \ each person does many trials in each condition; \ the analysis averages them "
             r"into one number per person per condition", WHITE),
            (r"what is lost: \ how much people differ in the effect, \ how much trials differ, \ which stimuli were "
             r"used, \ and how the effect changes over the session", AUTH),
            (r"and with unequal numbers of trials, \ every person counts the same, \ however well measured", PERSON),
            (r"a model of every trial keeps all of it: \ the multilevel, \ or mixed, \ model", GOOD),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        with self.voiceover(
            "Most experiments measure each person many times. <bookmark mark='a'/> The traditional analysis averages "
            "the trials into one number per person per condition, and compares the averages. <bookmark mark='b'/> "
            "What's lost: how much people differ in the effect, how much trials differ, which stimuli were used, and "
            "how the effect changes over the session. <bookmark mark='c'/> And with unequal numbers of trials, every "
            "person counts the same, however well measured. <bookmark mark='d'/> A model of every trial keeps all of "
            "it: the multilevel, or mixed, model."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def levels(self):
        head = heading(r"Regressions within regressions")
        eqs = VGroup(
            MathTex(r"\text{trial: } \quad y_{pt} = a_p + b_p\,x_{pt} + \varepsilon_{pt}", font_size=36, color=WHITE),
            MathTex(r"\text{person: } \quad a_p = \alpha + u_p, \qquad b_p = \beta + v_p", font_size=36, color=MODEL),
            MathTex(r"(u_p, v_p) \sim N(\mathbf{0}, G), \qquad \varepsilon_{pt} \sim N(0, \sigma^2)", font_size=36,
                    color=GOOD),
        ).arrange(DOWN, buff=0.4).move_to([0, 1.2, 0])
        rows = rows_of([
            (r"each person has their own line; \ the lines are drawn from a population of lines", WHITE),
            (r"$\beta$ is the average effect; \ $G$ says how much people differ in it; \ $\sigma^2$ is trial noise", MODEL),
            (r"Laird and Ware wrote the general form in 1982; \ \emph{Statistics, Built} Part 25 fits it, \ and this "
             r"part uses that code", GOOD),
        ], 12.4, 21, 0.38).move_to([0, -2.1, 0])
        tag = published_tag(r"Laird \& Ware (1982)")
        with self.voiceover(
            "Here's the model. <bookmark mark='a'/> At the level of trials, each person has their own line: an "
            "intercept and a slope. <bookmark mark='b'/> At the level of people, those lines are drawn from a "
            "population of lines. Beta is the average effect. G says how much people differ in it. Sigma squared is "
            "the noise between trials. <bookmark mark='c'/> Nan Laird and James Ware wrote the general form in 1982. "
            "Statistics, Built fits it in its Part 25, and this part uses that code."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eqs))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def neff(self):
        d = load("neff")
        head = heading(r"How much is one more observation worth?")
        A = axes([0, 52], [0, 360], x_length=5.6, y_length=3.0, xticks=[1, 10, 20, 50], yticks=[0, 100, 200, 300],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"observations per person (100 people)",
                 ylabel=r"effective sample size", center=[-3.3, 0.3, 0], font_size=13)
        cap = DashedLine(A.ax.c2p(0, d["N"] / d["icc"]), A.ax.c2p(52, d["N"] / d["icc"]), color=AUTH, stroke_width=2)
        cap_l = label(r"the ceiling: \ 100 / 0.3", font_size=13, color=AUTH).next_to(A.ax.c2p(52, d["N"] / d["icc"]),
                                                                                     UP, buff=0.05).shift(LEFT * 0.8)
        c = curve(A.ax, d["m"], d["neff"], MODEL, stroke_width=4)
        dots = VGroup(*[Dot(A.ax.c2p(m, v), radius=0.07, color=PERSON) for m, v in zip(d["m"], d["neff_sim"])])
        i10 = list(d["m"]).index(10)
        rows = rows_of([
            (r"a person's observations share that person: \ here the intraclass correlation is 0.3", WHITE),
            (r"for the grand mean, \ $m$ observations from each of $N$ people are worth $Nm / (1 + (m - 1)\,"
             r"\mathrm{ICC})$ independent ones", MODEL),
            (rf"ten each from 100 people: \ 1,000 observations, \ worth about {d['neff'][i10]:.0f}; \ fifty each: "
             rf"\ about {d['neff'][-1]:.0f}", PERSON),
            (r"for questions about people, \ more people beat more observations; \ for questions about change "
             r"within a person, \ the reverse", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"4,000 simulated studies (dots) \ against the formula")
        with self.voiceover(
            "How much is one more observation worth? <bookmark mark='a'/> A person's observations share that "
            "person. Here the intraclass correlation, the share of the variance that belongs to the person, is zero "
            "point three. <bookmark mark='b'/> For the grand mean, the observations are worth fewer independent ones, "
            "by this formula. The dots are simulated studies. <bookmark mark='c'/> Ten each from a hundred people is "
            "a thousand observations, worth about two hundred and seventy. Fifty each, about three hundred and "
            "twenty, near a ceiling of three hundred and thirty. <bookmark mark='d'/> For questions about people, more "
            "people beat more observations. For questions about change within a person, it's the reverse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), FadeIn(dots))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(cap), FadeIn(cap_l))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
