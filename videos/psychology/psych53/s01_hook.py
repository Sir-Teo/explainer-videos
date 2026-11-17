from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.reanalysis()
        self.question()
        self.objectives()

    def story(self):
        rows_section(self, r"The lights at Hawthorne", [
            (r"1924 to 1927: \ at Western Electric's Hawthorne Works near Chicago, \ engineers vary the lighting in "
             r"the rooms where workers assemble relays and coils", WHITE),
            (r"the story: \ raise the light and output rises; \ lower it and output rises again", PERSON),
            (r"the moral drawn: \ workers respond to being watched and cared about, \ not to the conditions", MODEL),
            (r"later studies at the plant, \ written up by Roethlisberger and Dickson in 1939, \ made it the founding "
             r"tale of ``human relations'' at work", GOOD),
            (r"the ``Hawthorne effect'' entered every methods textbook (Part 2)", YOU),
        ], "Every course on psychology at work begins with the same story. <bookmark mark='a'/> From 1924 to 1927, at "
           "Western Electric's Hawthorne Works near Chicago, engineers varied the lighting in the rooms where workers "
           "assembled telephone parts. <bookmark mark='b'/> As the story goes, when they raised the light, output "
           "rose, and when they lowered it, output rose again. <bookmark mark='c'/> The moral drawn: workers respond "
           "to being watched and cared about, not to the conditions. <bookmark mark='d'/> Later studies at the plant, "
           "written up by Fritz Roethlisberger and William Dickson in 1939, made it the founding tale of human "
           "relations at work. <bookmark mark='e'/> And the Hawthorne effect entered every methods textbook, Part 2's "
           "included.", tag=historical_tag(r"Roethlisberger \& Dickson (1939)"))

    def reanalysis(self):
        rows_section(self, r"The data, \ found again", [
            (r"the illumination studies were never properly published; \ their data were thought lost", WHITE),
            (r"2011: \ Steven Levitt and John List found the original output records and analysed them", MODEL),
            (r"output rose in the experimental periods, \ but also with the season and on the days after the lights "
             r"were changed, \ which always fell on a Monday", PERSON),
            (r"evidence of a Hawthorne effect in the data was slight; \ the famous rise and rise again is mostly "
             r"the retelling", AUTH),
            (r"the real history of work psychology is less romantic, \ and more useful: \ numbers about prediction", YOU),
        ], "What do the data actually show? <bookmark mark='a'/> The illumination studies were never properly "
           "published, and their data were thought lost. <bookmark mark='b'/> In 2011 the economists Steven Levitt "
           "and John List found the original output records and analysed them. <bookmark mark='c'/> Output did rise "
           "in the experimental periods, but it also rose with the season, and the lighting changes always fell on a "
           "Monday, after the weekend. <bookmark mark='d'/> The evidence of a Hawthorne effect in the data was "
           "slight. The famous rise and rise again is mostly the retelling. <bookmark mark='e'/> The real history of "
           "work psychology is less romantic and more useful. It's about numbers that predict.",
           tag=published_tag(r"Levitt \& List (2011)"))

    def question(self):
        rows_section(self, r"Today: \ how well can anyone predict who will be good at a job?", [
            (r"validity: \ correlations between a method and later performance, \ and why they mislead", SYMP),
            (r"a century of evidence, \ and its revision in 2022", MODEL),
            (r"money, \ fairness and algorithms", PERSON),
            (r"goals, \ pay, \ teams and where people work", GOOD),
        ], "So this part asks: how well can anyone predict who will be good at a job? <bookmark mark='a'/> Validity: "
           "correlations between a method and later performance, and why they mislead. <bookmark mark='b'/> A "
           "century of evidence, and its revision in 2022. <bookmark mark='c'/> Money, fairness and algorithms. "
           "<bookmark mark='d'/> And goals, pay, teams, and where people work.", font_size=27, buff=0.48)

    def objectives(self):
        head = VGroup(label(r"Part 53", font_size=34, color=GREY_B), label(r"People at Work", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"validity, \ the criterion problem and rater noise",
            r"unreliability and range restriction, \ corrected and overcorrected",
            r"which hiring methods predict, \ after the 2022 revision",
            r"utility in money, \ and the Taylor-Russell tables",
            r"adverse impact and the validity-diversity frontier",
            r"goals, \ incentives, \ crowding out, \ teams and remote work",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 53 of Psychology, Built: people at work. <bookmark mark='a'/> We'll define validity, and "
            "meet the problem of measuring job performance at all. We'll see how unreliability and range restriction "
            "hide validity, and how corrections can overshoot. We'll ask which hiring methods predict, after the "
            "revision of 2022. We'll turn a correlation into money. We'll compute adverse impact and the frontier "
            "between validity and diversity. And we'll look at goals, incentives, what money crowds out, teams, and "
            "working from home."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
