from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


class Moderators(VoiceoverScene):
    def construct(self):
        self.card()
        self.regression()
        self.power()

    def card(self):
        card = chapter_card(3, r"Moderators", r"When do effects differ, \ and can a meta-analysis tell?", lit=(),
                            part=PART, scale=("society",), marr=("what",))
        with self.voiceover("Chapter three. Moderators."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def regression(self):
        head = heading(r"Meta-regression")
        eq = MathTex(r"y_i = \beta_0 + \beta_1 x_i + u_i + e_i", font_size=40, color=MODEL).move_to([0, 1.8, 0])
        rows = rows_of([
            (r"when effects vary, \ ask why: \ a study-level feature $x$ (age of the sample, \ dose, \ online or in "
             r"the lab) as a predictor of the effect", WHITE),
            (r"it is a regression with studies as the cases, \ weighted by precision, \ with the remaining spread "
             r"$\tau^2$", MODEL),
            (r"its cases are few, \ and its predictor was not randomized: \ studies that differ in $x$ differ in much "
             r"else", AUTH),
            (r"so a moderator is a correlation across studies, \ like Part 47's between-person slope: \ a hypothesis "
             r"to test by design", YOU),
        ], 12.4, 22, 0.42).move_to([0, -0.9, 0])
        with self.voiceover(
            "When effects vary, ask why. <bookmark mark='a'/> A feature of each study, such as the age of its sample, "
            "the dose, or whether it ran online, becomes a predictor of its effect. <bookmark mark='b'/> It's a "
            "regression with studies as the cases, weighted by precision, with the leftover spread tau squared. "
            "<bookmark mark='c'/> But its cases are few, and its predictor wasn't randomized. Studies that differ in "
            "one feature differ in much else. <bookmark mark='d'/> So a moderator is a correlation across studies, "
            "like Part 47's between-person slope: a hypothesis to test by design."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def power(self):
        d = load("moderator")
        head = heading(r"Moderators hide")
        A = axes([0, 170], [0, 1.05], x_length=5.6, y_length=3.0, xticks=[10, 40, 80, 160], yticks=[0, 0.5, 0.8, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"studies in the meta-analysis",
                 ylabel=r"power to find the moderator", center=[-3.3, 0.3, 0], font_size=12)
        eighty = DashedLine(A.ax.c2p(0, 0.8), A.ax.c2p(170, 0.8), color=GREY_B, stroke_width=1.5)
        c = curve(A.ax, d["k"], d["power"], MODEL, stroke_width=4)
        dots = VGroup(*[Dot(A.ax.c2p(k, p), radius=0.07, color=MODEL) for k, p in zip(d["k"], d["power"])])
        rows = rows_of([
            (r"half the studies have a true effect larger by 0.2 (0.5 against 0.3), \ with $\tau$ = 0.2 besides", WHITE),
            (rf"with 20 studies, \ the moderator is found {100 * d['power'][1]:.0f}\% of the time; \ with 40, \ "
             rf"{100 * d['power'][2]:.0f}\%", AUTH),
            (rf"it takes about 80 studies for 80\% power ({100 * d['power'][3]:.0f}\%)", GOOD),
            (r"so ``no moderator found'' in a typical meta-analysis says little; \ and a moderator found among many "
             r"tried is Part 4's garden again", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{meta.moderator\_power}, \ 300 meta-analyses each")
        with self.voiceover(
            "And moderators hide. <bookmark mark='a'/> Make half the studies' true effect larger by zero point two, "
            "with other real variation besides. <bookmark mark='b'/> With twenty studies, the moderator is found "
            "less than a third of the time. With forty, a bit more than half. <bookmark mark='c'/> It takes about "
            "eighty studies for eighty percent power. <bookmark mark='d'/> So no moderator found, in a typical "
            "meta-analysis, says little. And a moderator found among many tried is Part 4's garden of forking paths "
            "again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(eighty))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(c), FadeIn(dots))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
