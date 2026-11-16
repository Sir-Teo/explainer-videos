from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403


class Centre(VoiceoverScene):
    def construct(self):
        self.card()
        self.split()
        self.fallacy()
        self.naive()

    def card(self):
        card = chapter_card(8, r"Within against between", r"Which question does the coefficient answer?",
                            lit={1950: r"Robinson"}, part=PART, scale=("person", "group"), marr=("what", "how"))
        with self.voiceover("Chapter eight. Within against between."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def split(self):
        d = load("simpson")
        head = heading(r"Person-mean centring")
        eq = MathTex(r"y_{pt} = \alpha + \beta_W\,(x_{pt} - \bar x_p) + \beta_B\,\bar x_p + u_p + \varepsilon_{pt}",
                     font_size=38, color=MODEL).move_to([0, 1.8, 0])
        A = axes([0.3, 3.7], [-1.2, 1.2], x_length=4.6, y_length=2.8, xticks=None, yticks=[-1, 0, 1],
                 yfmt=lambda v: f"{v:g}", ylabel=r"slope", center=[-3.6, -1.0, 0], font_size=13)
        b = bars(A.ax, [1, 2, 3], [d["pooled"], d["within"], d["between"]], [GREY_B, GOOD, AUTH], width=0.6)
        names = VGroup(*[label(t, font_size=13, color=c).next_to(A.ax.c2p(i + 1, -1.2), DOWN, buff=0.1) for i, (t, c)
                         in enumerate(((r"pooled", GREY_B), (r"within", GOOD), (r"between", AUTH)))])
        rows = rows_of([
            (r"split each predictor into the person's average $\bar x_p$ and today's departure from it", WHITE),
            (rf"$\beta_W$ answers the question about a person: \ {d['within']:+.2f}, \ close to the planted "
             rf"{d['true_within']:+.1f}", GOOD),
            (rf"$\beta_B$ answers the question about people: \ {d['between']:+.2f}", AUTH),
            (rf"the pooled slope, \ {d['pooled']:+.2f}, \ answers neither: \ a blend weighted by how much of x varies "
             rf"within and between", PERSON),
        ], 6.0, 19, 0.38).move_to([3.4, -1.0, 0])
        tag = psyche_tag(r"\texttt{within.simpson\_cloud}")
        with self.voiceover(
            "The repair is simple. <bookmark mark='a'/> Split each predictor into the person's own average, and "
            "today's departure from it, and give each its own slope. <bookmark mark='b'/> The within slope answers "
            "the question about a person: here about plus zero point six, as planted. <bookmark mark='c'/> The "
            "between slope answers the question about people: about minus one. <bookmark mark='d'/> And the pooled "
            "slope answers neither. It's a blend, weighted by how much of x varies within and between people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def fallacy(self):
        head = heading(r"The ecological fallacy, \ inside one mind")
        rows = rows_of([
            (r"Robinson, \ 1950: \ US states with more immigrants had higher literacy, \ though immigrants were less "
             r"often literate; \ the correlation across states said nothing about individuals", WHITE),
            (r"the same holds one level down: \ a correlation across people says little about how one person works",
             AUTH),
            (r"a cross-sectional finding that anxious people sleep less does not show that a person sleeps less on "
             r"anxious nights", PERSON),
            (r"the question decides the data: \ a claim about a person needs repeated measures of persons", GOOD),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        tag = published_tag(r"Robinson (1950)")
        with self.voiceover(
            "There's an old name for the mistake. <bookmark mark='a'/> In 1950 William Robinson showed that American "
            "states with more immigrants had higher literacy, though immigrants were less often literate. The "
            "correlation across states said nothing about individuals. <bookmark mark='b'/> The same holds one level "
            "down. A correlation across people says little about how one person works. <bookmark mark='c'/> Finding "
            "that anxious people sleep less doesn't show that a person sleeps less on anxious nights. "
            "<bookmark mark='d'/> The question decides the data. A claim about a person needs repeated measures of "
            "persons."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def naive(self):
        d = load("naive")
        head = heading(r"Ignoring the person")
        A = axes([0.3, 2.7], [0, 0.2], x_length=4.0, y_length=3.0, xticks=None, yticks=[0, 0.05, 0.1, 0.15],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"false positives", center=[-3.8, 0.3, 0], font_size=13)
        b = bars(A.ax, [1, 2], [d["naive"], d["summary"]], [AUTH, GOOD], width=0.6)
        five = DashedLine(A.ax.c2p(0.3, 0.05), A.ax.c2p(2.7, 0.05), color=GREY_B, stroke_width=1.5)
        names = VGroup(*[wrapped_label(t, 1.6, 12, c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1) for i, (t, c) in
                         enumerate(((r"all 600 points in one regression", AUTH), (r"one slope per person, \ then a "
                                                                                 r"t-test", GOOD)))])
        rows = rows_of([
            (r"30 people, \ 20 occasions each; \ each person has their own slope, \ and on average the slope is zero",
             WHITE),
            (rf"pool all 600 points into one regression, \ and its test is significant {100 * d['naive']:.0f}\% of "
             rf"the time", AUTH),
            (rf"fit each person's slope, \ then test the 30 slopes: \ {100 * d['summary']:.1f}\%", GOOD),
            (r"the unit of replication is the person: \ the test must count people, \ not points; \ the multilevel "
             r"model with random slopes does this, \ and more", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"2,000 simulated studies")
        with self.voiceover(
            "One more way to get a person wrong: ignore them. <bookmark mark='a'/> Thirty people, twenty occasions "
            "each. Each has their own slope, and on average the slope is zero. <bookmark mark='b'/> Pool all six "
            "hundred points into one regression, and its test is significant fifteen percent of the time. "
            "<bookmark mark='c'/> Fit each person's slope, then test the thirty slopes, and it's five percent, as "
            "promised. <bookmark mark='d'/> The unit of replication is the person. The test must count people, not "
            "points. The multilevel model with random slopes does this, and more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(five))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
