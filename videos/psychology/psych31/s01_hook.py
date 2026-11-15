from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.lottery()
        self.results()
        self.question()
        self.objectives()

    def lottery(self):
        head = heading(r"Bucharest, \ 2000")
        hall = VGroup(Rectangle(width=4.4, height=2.6, color=GREY_B, stroke_width=3),
                      Polygon([-2.4, 1.3, 0], [2.4, 1.3, 0], [0, 2.3, 0], color=GREY_B, stroke_width=3))
        rng = np.random.default_rng(31)
        kids = VGroup(*[Dot([x, y, 0], radius=0.07, color=CHILD) for x, y in zip(rng.uniform(-1.9, 1.9, 40),
                                                                                    rng.uniform(-1.1, 1.0, 40))])
        inst = VGroup(hall, kids).move_to([-3.6, 0.1, 0])
        cap = label(r"children in the city's institutions", font_size=22, color=GREY_B).next_to(inst, DOWN, buff=0.25)
        drum = VGroup(Circle(radius=0.6, color=YOU, stroke_width=4), label(r"lottery", font_size=20, color=YOU))
        drum.move_to([0.4, 0.1, 0])
        foster = word_chip(r"foster care", color=GOOD, font_size=24, width=3.2).move_to([4.2, 1.2, 0])
        usual = word_chip(r"care as usual", color=LOST, font_size=24, width=3.2).move_to([4.2, -0.2, 0])
        never = word_chip(r"never institutionalized", color=AGE, font_size=22, width=3.6).move_to([4.2, -1.5, 0])
        ar1 = Arrow(drum.get_right(), foster.get_left(), color=GOOD, buff=0.15)
        ar2 = Arrow(drum.get_right(), usual.get_left(), color=LOST, buff=0.15)
        rows = rows_of([
            (r"136 children aged 6 to 31 months, \ randomized: \ half to foster families the project recruited and "
             r"paid, \ half left in care as usual", WHITE),
        ], 11.0, 22).move_to([0, -2.6, 0])
        tag = published_tag(r"Nelson et al.\ (2007)")
        with self.voiceover(
            "In 2000, Bucharest had many young children living in state institutions, and almost no foster "
            "families. <bookmark mark='a'/> A team of American and Romanian researchers, led by Charles Nelson, "
            "Nathan Fox and Charles Zeanah, offered to build a foster-care network, but there were too few homes for "
            "every child. <bookmark mark='b'/> So, with the government's agreement, they let a lottery decide. "
            "<bookmark mark='c'/> A hundred and thirty-six children, aged six months to two and a half years, were "
            "randomized: half to foster families the project recruited and paid, half to care as usual. "
            "<bookmark mark='d'/> A third group, children from the same city who had never lived in an institution, "
            "was followed for comparison. This was the Bucharest Early Intervention Project, one of the very few "
            "randomized experiments on how early care shapes a life."
        ) as vo:
            self.play(FadeIn(head), FadeIn(inst), FadeIn(cap), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(kids, color=CHILD))
            vo.wait_until("b")
            self.play(FadeIn(drum, scale=0.8))
            vo.wait_until("c")
            self.play(GrowArrow(ar1), GrowArrow(ar2), FadeIn(foster), FadeIn(usual), FadeIn(rows))
            vo.wait_until("d")
            self.play(FadeIn(never, shift=LEFT * 0.2))
        self.clear_scene()

    def results(self):
        head = heading(r"What the lottery showed")
        times = [(r"42 months", 0), (r"54 months", 1), (r"12 years", 2), (r"18 years", 3)]
        line = Line([-5.6, 1.6, 0], [5.6, 1.6, 0], color=GREY_B, stroke_width=3)
        marks = VGroup(*[VGroup(Dot([-4.5 + 3.0 * i, 1.6, 0], radius=0.09, color=AGE),
                                label(t, font_size=20, color=AGE).move_to([-4.5 + 3.0 * i, 2.05, 0]))
                         for t, i in times])
        rows = rows_of([
            (r"the children left in institutions fell far behind the never-institutionalized children, \ in "
             r"almost every measure", LOST),
            (r"foster care raised IQ, \ and the gains were largest for the children placed youngest", GOOD),
            (r"at 18, \ sixteen years after the lottery: \ the foster-care group scored about 9 IQ points higher, "
             r"\ 0.6 of a standard deviation, \ partly through better caregiving and more secure attachment", GOOD),
            (r"a randomized answer to a question that usually has only correlations", YOU),
        ], 12.2, 25, 0.4).move_to([0, -1.1, 0])
        tag = published_tag(r"Nelson et al.\ (2007); \ Humphreys et al.\ (2022)")
        with self.voiceover(
            "The children were tested again and again as they grew. <bookmark mark='a'/> Those left in institutions "
            "fell far behind the children who had never lived in one, in almost every measure. "
            "<bookmark mark='b'/> Foster care raised IQ, and in the 2007 report, at forty-two and fifty-four "
            "months, the gains were largest for the children placed youngest. <bookmark mark='c'/> At eighteen, "
            "sixteen years after the lottery, the foster-care group scored about nine IQ points higher, six-tenths of "
            "a standard deviation, and part of the effect ran through better caregiving and more secure attachment. "
            "<bookmark mark='d'/> That's a randomized answer to a question that almost always has only "
            "correlations."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(line), LaggedStart(*[FadeIn(m) for m in marks],
                                                                           lag_ratio=0.3))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ what in a life is set early, \ and what stays open?")
        rows = rows_of([
            (r"three clocks, \ age, \ period and cohort, \ and why no data can separate them on their own", AGE),
            (r"three designs that each get ageing wrong in their own way, \ simulated on the Pool", COHORT),
            (r"growth curves, \ windows that close, \ adolescence, \ and what parents and programmes change", CHILD),
            (r"moral development, \ ageing, \ dementia, \ and cohorts that keep changing", OLD),
        ], 12.6, 27, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "Most questions about development can't be settled by a lottery. This part is about the designs that try "
            "to answer them anyway. <bookmark mark='a'/> We'll start with three clocks, age, period and cohort, and "
            "see why no data can separate them on their own. <bookmark mark='b'/> Then three designs that each get "
            "ageing wrong in their own way, simulated where the truth is known. <bookmark mark='c'/> Then growth "
            "curves, windows that close, adolescence, and what parents and programmes really change. "
            "<bookmark mark='d'/> And then moral development, ageing, dementia, and cohorts that keep changing "
            "underneath it all."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 31", font_size=34, color=GREY_B), label(r"The Lifespan", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the age-period-cohort identity, \ and the assumption every answer needs",
            r"cross-sectional, \ longitudinal and cohort-sequential designs, \ with their biases simulated",
            r"growth curves as a mixed model, \ fitted by EM, \ with shrunken lines for each child",
            r"sensitive periods, \ adolescence, \ and what parenting and early programmes change",
            r"ageing: \ speed, \ knowledge, \ emotion, \ reserve, \ and attributable fractions",
            r"the replication record of nine lifespan findings",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 31 of Psychology, Built: the lifespan. <bookmark mark='a'/> We'll derive the "
            "age-period-cohort identity and the assumption that every answer to it needs. We'll simulate "
            "cross-sectional, longitudinal and cohort-sequential designs and watch each one's bias. We'll fit growth "
            "curves as a mixed model, by EM, with a shrunken line for each child. We'll look at sensitive periods, "
            "adolescence, and what parenting and early programmes change. We'll follow ageing through speed, "
            "knowledge, emotion and reserve, and compute what an attributable fraction means. And we'll enter the "
            "replication record of nine lifespan findings."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
