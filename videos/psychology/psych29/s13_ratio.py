from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class Ratio(VoiceoverScene):
    def construct(self):
        self.card()
        self.claim()
        self.butterfly()
        self.takedown()

    def card(self):
        card = chapter_card(12, r"The critical positivity ratio", r"How did a magic number get into the textbooks?",
                            lit={2005: r"Fredrickson \& Losada", 2013: r"Brown, \ Sokal \& Friedman"},
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter twelve. The critical positivity ratio."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def claim(self):
        head = heading(r"2.9013")
        big = MathTex(r"\frac{\text{positive}}{\text{negative}} > 2.9013", font_size=72, color=COG).move_to([0, 1.4, 0])
        rows = rows_of([
            (r"2005: \ Barbara Fredrickson and Marcial Losada, \ in \emph{American Psychologist}: \ people flourish "
             r"when their ratio of positive to negative emotions exceeds 2.9013, \ and stop flourishing above "
             r"about 11.6", WHITE),
            (r"the number came from Losada's earlier model of business teams, \ built on the Lorenz equations of "
             r"fluid flow", BODY),
            (r"widely cited, \ in a popular book and in workshops: \ ``three to one''", FACE),
        ], 12.2, 25, 0.4).move_to([0, -1.2, 0])
        tag = historical_tag(r"Fredrickson \& Losada (2005)")
        with self.voiceover(
            "The last story of this part is about a number. <bookmark mark='a'/> In 2005 Barbara Fredrickson and "
            "Marcial Losada published a paper in American Psychologist claiming that people flourish when the "
            "ratio of their positive to negative emotions exceeds 2.9013, and stop flourishing above about 11.6. "
            "<bookmark mark='b'/> The number came from Losada's earlier model of business teams, which was built on "
            "the Lorenz equations, a model of fluid convection. <bookmark mark='c'/> The paper was widely cited, "
            "and three to one became advice in a popular book and in workshops."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(big))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def butterfly(self):
        d = load("lorenz")
        head = heading(r"The Lorenz equations")
        xyz = np.asarray(d["xyz"], float)
        sc = 0.085
        pts = [np.array([-3.4 + sc * x, -2.9 + sc * z, 0]) for x, _, z in xyz]
        path = VMobject(color=BODY, stroke_width=1.6).set_points_as_corners(pts)
        eqs = VGroup(
            MathTex(r"\dot x = \sigma (y - x)", font_size=34),
            MathTex(r"\dot y = x (\rho - z) - y", font_size=34),
            MathTex(r"\dot z = x y - \beta z", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rows = rows_of([
            (r"Edward Lorenz, \ 1963: \ a three-variable model of air rising and falling; \ for some parameters, "
             r"\ chaos: \ the butterfly", WHITE),
            (r"Losada set the parameters, \ called the variables connectivity, \ emotion and inquiry, \ and read "
             r"the ratio off the point where the model's behaviour changes", BODY),
            (r"no data were fitted to the equations, \ and nothing about teams or people determines their "
             r"constants", UNPL),
        ], 5.6, 21, 0.32)
        right = VGroup(eqs, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{emotion.lorenz}: \ $\sigma = 10$, \ $\rho = 28$, \ $\beta = 8/3$")
        with self.voiceover(
            "Here are those equations. <bookmark mark='a'/> Edward Lorenz wrote them in 1963 as a three-variable "
            "model of air rising and falling in convection. For some parameters, the solution never settles and "
            "never repeats: chaos, and the butterfly-shaped curve that became its emblem. Psyche draws it here. "
            "<bookmark mark='b'/> Losada took the equations, set their parameters, renamed the variables "
            "connectivity, emotion and inquiry, and read the ratio off the point where the model's behaviour "
            "changes. <bookmark mark='c'/> No data were fitted to the equations, and nothing about teams or people "
            "determines their constants."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eqs))
            vo.wait_until("a")
            self.play(Create(path), FadeIn(rows[0]), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def takedown(self):
        head = heading(r"2013")
        rows = rows_of([
            (r"Nicholas Brown, \ a graduate student in applied positive psychology, \ found the mathematics "
             r"strange, \ and wrote to Alan Sokal, \ a physicist, \ who brought in Harris Friedman", WHITE),
            (r"their paper, \ ``The complex dynamics of wishful thinking'': \ the equations were used without "
             r"justification, \ and the 2.9013 threshold has no basis", UNPL),
            (r"Losada declined to defend it; \ \emph{American Psychologist} formally withdrew the modelling and "
             r"its predictions", COG),
            (r"Fredrickson's reply kept the broader claim: \ within limits, \ more positive emotion goes with "
             r"better mental health; \ that was not withdrawn", PLEAS),
            (r"the lesson for reviewers: \ mathematics in a psychology paper must be checked like any other "
             r"method", WHITE),
        ], 12.2, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Brown, \ Sokal \& Friedman (2013); \ Fredrickson (2013)")
        with self.voiceover(
            "The number lasted eight years. <bookmark mark='a'/> Nicholas Brown, a graduate student in applied "
            "positive psychology at the University of East London, found the mathematics strange and wrote to Alan "
            "Sokal, a physicist, who brought in the psychologist Harris Friedman. <bookmark mark='b'/> Their 2013 "
            "paper, The Complex Dynamics of Wishful Thinking, showed that the equations were used without "
            "justification, and that the threshold of 2.9013 has no basis at all. <bookmark mark='c'/> Losada declined "
            "to defend the work, and American Psychologist formally withdrew the modelling and the predictions drawn "
            "from it. <bookmark mark='d'/> Fredrickson's reply kept the broader claim: within limits, more positive "
            "emotion goes with better mental health. That part was not withdrawn. <bookmark mark='e'/> The lesson for "
            "reviewers: mathematics in a psychology paper has to be checked like any other method, which is what the "
            "derivations in this series are for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
