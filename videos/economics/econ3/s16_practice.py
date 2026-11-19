from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ the people who make the numbers", r"Who measures an economy for a living?",
             "Chapter fourteen. In practice: the people who make the numbers.", scale=("nation", "world"),
             horizon=("a month", "a year"))
        self.jobs()
        self.friday()

    def jobs(self):
        head = heading(r"In practice")
        items = [
            (r"national accountants", r"at statistical agencies: \ they assemble GDP from surveys, tax records and "
             r"the census of businesses, \ and revise it", E.ACCENT),
            (r"price statisticians", r"they choose the basket, \ the shops and the quality adjustments, \ and "
             r"defend them to Congress", FISHER),
            (r"survey methodologists", r"they design the samples behind the unemployment rate, \ and repair them "
             r"when people stop answering", E.HOUSEHOLDS),
            (r"nowcasters", r"at central banks and banks: \ they estimate this quarter's GDP before it is "
             r"published, \ from whatever arrives first", E.PRED),
            (r"country economists", r"at the IMF and the World Bank: \ they check whether a country's numbers add "
             r"up \ before lending to it", E.WORLD),
            (r"data scientists", r"at card networks, payroll firms and satellite companies: \ they sell faster, \ "
             r"rougher readings of the same economy", E.AGORA),
        ]
        pc = point_cards(items, width=12.8, cols=2, font_size=24).move_to(DOWN * 0.3)
        with self.voiceover(
            "Who does this for a living? <bookmark mark='a'/> National accountants at statistical agencies, who "
            "assemble GDP every quarter from surveys, tax records and a census of businesses, and spend years "
            "revising it. <bookmark mark='b'/> Price statisticians, who choose the basket, the shops and the "
            "quality adjustments, and have to defend each choice when someone's pension depends on it. "
            "<bookmark mark='c'/> Survey methodologists, who design the samples behind the unemployment rate, and "
            "repair them as fewer and fewer people answer the door or the phone. <bookmark mark='d'/> Nowcasters, "
            "at central banks and investment banks, who estimate this quarter's GDP before it is published, from "
            "whatever data arrive first. <bookmark mark='e'/> Country economists at the International Monetary "
            "Fund and the World Bank, who check whether a government's numbers add up before lending to it. "
            "<bookmark mark='f'/> And data scientists at card networks, payroll processors and satellite firms, "
            "who sell faster and rougher readings of the same economy."
        ) as vo:
            self.play(FadeIn(head))
            for mark, c in zip("abcdef", pc.cards):
                vo.wait_until(mark)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def friday(self):
        d = load("unemployment")
        clock = VGroup(Circle(radius=0.8, stroke_color=E.ACCENT, stroke_width=4),
                       Line(ORIGIN, UP * 0.6, color=WHITE, stroke_width=5),
                       Line(ORIGIN, RIGHT * 0.45 + DOWN * 0.2, color=WHITE, stroke_width=5),
                       Dot(radius=0.07, color=WHITE)).move_to(LEFT * 4.6 + UP * 1.3)
        time = label(r"8:30 a.m., \ a Friday, \ Washington", font_size=26, color=E.ACCENT).next_to(clock, DOWN,
                                                                                                buff=0.3)
        steps = VGroup(
            label(r"the jobs report: \ two surveys, \ released together", font_size=31),
            label(r"payrolls, \ from employers' records: \ how many jobs?", font_size=27, color=E.FIRMS),
            label(rf"the unemployment rate, \ from households: \ {d['us']['U-3']:.1f}\% in October 2026",
                  font_size=27, color=E.HOUSEHOLDS),
            label(r"forecasters' guesses, \ markets' reaction, \ within seconds", font_size=27, color=E.PRED),
            label(r"and next month, \ revisions to this month", font_size=27, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(RIGHT * 1.5 + DOWN * 0.1)
        tag = published_tag(r"BLS, The Employment Situation (monthly news release)", corner=DR, font_size=15)
        with self.voiceover(
            "The busiest moment in this world comes on the first Friday of most months, at 8:30 in the morning in "
            "Washington. <bookmark mark='a'/> The Bureau of Labor Statistics releases the jobs report: two surveys "
            "at once. <bookmark mark='b'/> One counts jobs from employers' payroll records. <bookmark mark='c'/> "
            "The other is the household survey of chapter eight, which gives the unemployment rate. "
            "<bookmark mark='d'/> Economists at banks have spent the week forecasting both numbers, and markets move "
            "within seconds of the release. <bookmark mark='e'/> And a month later, part of what they reacted to is "
            "revised."
        ) as vo:
            self.play(FadeIn(clock), FadeIn(time), FadeIn(tag))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s, shift=RIGHT * 0.15))
        self.clear_scene()
