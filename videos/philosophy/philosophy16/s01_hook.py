from __future__ import annotations

from videos.philosophy.philosophy16.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.crisis()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"Every experiment may be said to exist only in order to give the facts a chance of disproving "
                       r"the null hypothesis.", r"R.\ A.\ Fisher", r"\textit{The Design of Experiments} \ (1935)",
                       width=9.6, font_size=26).next_to(t, DOWN, buff=0.6)
        with self.voiceover(
            "Part 15 asked whether experience can justify any expectation at all. This part asks a narrower, "
            "practical question: when numbers come in, how much do they tell us? <bookmark mark='a'/>Ronald Fisher "
            "put the twentieth century's answer in one sentence: every experiment exists only to give the facts a "
            "chance of disproving the null hypothesis. <bookmark mark='b'/>A century later, that machinery is in "
            "crisis."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=BAD, scale_factor=1.03))
        self.clear_scene()

    def crisis(self):
        head = label(r"Estimating the reproducibility of psychological science", font_size=28,
                     color=CONN).to_edge(UP, buff=0.35)
        sub = label(r"Open Science Collaboration \ (2015): \ 100 studies from three leading journals, \ repeated",
                    font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.2)
        base = Line([-5.8, -2.3, 0], [0.6, -2.3, 0], color=GREY_C, stroke_width=2)
        vals = [(r"original studies \ significant", 0.97, NULLC), (r"replications \ significant", 0.36, BAD)]
        bars = VGroup()
        for i, (t, v, c) in enumerate(vals):
            b = Rectangle(width=1.6, height=3.4 * v, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([-4.2 + i * 3.0, -2.3 + b.height / 2, 0])
            pct = label(rf"{round(100 * v)}\%", font_size=30, color=c).next_to(b, UP, buff=0.1)
            lab = label(t, font_size=19, color=GREY_A).next_to(b, DOWN, buff=0.15)
            bars.add(VGroup(b, pct, lab))
        side = stack([(r"mean effect size: \ $r = 0.40$ \ $\to$ \ $r = 0.20$", WHITE),
                      (r"Bem \ (2011): \ nine experiments `show' precognition, \ $p < 0.05$ in eight", BAD),
                      (r"medicine: \ Amgen could confirm 6 of 53 landmark cancer studies \ (2012)", GREY_A),
                      (r"is the method broken, \ or its use, \ or our reading of it?", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=6.2).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "In 2015 the Open Science Collaboration repeated a hundred studies from three leading psychology "
            "journals. <bookmark mark='a'/>Ninety-seven of the originals had reported a significant result. "
            "<bookmark mark='b'/>Thirty-six of the replications did. <bookmark mark='c'/>The average effect size "
            "halved. <bookmark mark='d'/>Four years earlier, Daryl Bem had published nine experiments in a top "
            "journal, eight of them significant, apparently showing that people can feel the future. "
            "<bookmark mark='e'/>In medicine, a team at Amgen could confirm only six of fifty-three landmark cancer "
            "studies. <bookmark mark='f'/>Is the method broken, or its use, or our reading of what it says? To "
            "answer, we need to know what the numbers mean. That is the philosophy of statistics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), Create(base))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1]), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1]), FadeIn(bars[1][2]))
            for mk, r in zip("cdef", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Fisher, \ Neyman--Pearson, \ Bayes: \ three answers from one coin",
            r"what a $p$-value is, \ and six things it is not, \ simulated",
            r"base rates; \ why most published findings may be false; \ the garden of forking paths",
            r"optional stopping; \ the likelihood principle and Birnbaum's theorem \ (the Wall)",
            r"Lindley's paradox; \ severity; \ Simpson's paradox; \ the reference class",
            r"A/B tests and peeking; \ testing by betting, \ with Ville's inequality",
            r"AIC and BIC: \ choosing a model to predict",
        ], font_size=24)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Three schools of statistics, giving three different verdicts on the same "
            "coin. <bookmark mark='b'/>What a p-value is, and six things it is not, each refuted by simulation. "
            "<bookmark mark='c'/>Base rates, why most published findings may be false, and a machine that turns "
            "noise into discoveries. <bookmark mark='d'/>Optional stopping, and the likelihood principle, with "
            "Birnbaum's theorem: this part's brick in the Wall. <bookmark mark='e'/>Lindley's paradox, severe "
            "testing, Simpson's paradox and the reference class. <bookmark mark='f'/>Tests in industry, and the "
            "newest idea in the field: testing by betting. <bookmark mark='g'/>And choosing a model for prediction."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
