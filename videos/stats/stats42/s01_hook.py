from __future__ import annotations

from videos.stats.stats42.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.letter()
        self.questions()
        self.fisher()
        self.format()
        self.objectives()

    def letter(self):
        tl = timeline(lit=(1919, 1978)).to_edge(UP, buff=0.35)
        m = memo([
            (r"Dear statistician,", WHITE),
            (r"we have two decisions to make before the budget closes, \ in six weeks.", GREY_A),
            (r"Both are about blood pressure, \ the island's largest cause of early death.", GREY_A),
            (r"We have some data, \ not as clean as we would like. \ Can you help?", GREY_A),
            (r"--- the Ministry of Health", S.ACCENT),
        ], r"Ministry of Health \ \textbullet\ \ request for statistical advice").move_to([0, -0.6, 0])
        with self.voiceover(
            "This part closes the master's degree, and like the last part of the bachelor's, it introduces no new method. "
            "<bookmark mark='a'/> It begins with a letter. The World's ministry of health has two decisions to make before "
            "its budget closes, in six weeks. Both are about blood pressure, the island's largest cause of early death. "
            "They have some data, not as clean as they would like, and they want help. A statistician's working life is "
            "made of letters like this one, and the master's is the degree that says you can answer them."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(m[0]), FadeIn(m[1]))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in m[2]], lag_ratio=0.5), run_time=5.0)
        self.clear_scene()

    def questions(self):
        c1 = memo([
            (r"We want to send community health workers into towns: \ visits, \ pressure checks, \ advice.", GREY_A),
            (r"Before we pay for 200 towns, \ we will test it. \ How? \ And how many towns?", WHITE),
            (r"We have a pilot survey: \ 30 adults measured in each town.", GREY_A),
        ], r"Question 1 \ \textbullet\ \ a decision not yet made", width=12.4, font_size=23)
        c2 = memo([
            (r"A potassium-enriched salt substitute went on sale last year.", GREY_A),
            (r"A survey of 3,000 adults finds its users' pressure 6.7 mm Hg \emph{higher}.", WHITE),
            (r"The newspapers want it withdrawn. \ Should we?", GREY_A),
        ], r"Question 2 \ \textbullet\ \ a decision about the past", width=12.4, font_size=23)
        VGroup(c1, c2).arrange(DOWN, buff=0.35).move_to([0, -0.1, 0])
        c1[1].set_color(CASE1)
        c2[1].set_color(CASE2)
        with self.voiceover(
            "<bookmark mark='a'/> The first question is about the future. The ministry wants to send community health workers "
            "into its towns, to visit households, check pressures and give advice. Before paying for all two hundred towns, it "
            "will test the idea. How should the test be done, and how many towns does it need? There is a pilot survey: "
            "thirty adults measured in each town. <bookmark mark='b'/> The second question is about the past. A salt substitute, "
            "with some of the sodium replaced by potassium, went on sale a year ago. A survey of three thousand adults finds "
            "that the people who use it have pressures six point seven millimetres higher than those who don't. The newspapers "
            "want it withdrawn. Should it be?"
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.2))
        self.clear_scene()

    def fisher(self):
        hc = history_card(1919, r"R. A. Fisher at Rothamsted Experimental Station",
                          r"hired for six months to look at 66 years of data from the Broadbalk wheat field; \ he stayed 14 "
                          r"years, \ and invented much of experimental design in answering the station's questions",
                          color=CASE1, width=11.4, font_size=23).move_to([0, 1.3, 0])
        q = VGroup(
            label(r"``To consult the statistician after an experiment is finished", font_size=27),
            label(r"is often merely to ask him to conduct a \emph{post mortem} examination.", font_size=27),
            label(r"He can perhaps say what the experiment died of.''", font_size=27),
            note(r"R. A. Fisher, \ Presidential Address to the first Indian Statistical Congress \ (1938)"),
        ).arrange(DOWN, buff=0.2).move_to([0, -1.6, 0])
        q[2].set_color(S.ACCENT)
        with self.voiceover(
            "<bookmark mark='a'/> Consulting is as old as the profession. In 1919, Ronald Fisher was hired for six months by "
            "the Rothamsted Experimental Station, to see what could be learned from sixty-six years of records of its wheat "
            "field. He stayed fourteen years, and in answering the station's questions he invented much of the design of "
            "experiments. <bookmark mark='b'/> He also left the consultant's motto. To consult the statistician after an "
            "experiment is finished is often merely to ask him to conduct a post mortem examination. <bookmark mark='c'/> He "
            "can perhaps say what the experiment died of. Our two questions are the two sides of that remark: one arrives "
            "before the study, and one after."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(q[0]), FadeIn(q[1]), FadeIn(q[3]))
            vo.wait_until("c")
            self.play(FadeIn(q[2]))
        self.clear_scene()

    def format(self):
        card = ExamCard(None, r"how the exam works", r"Parts 21--41",
                        [r"Each problem is posed on a card like this one, \ with the parts it draws on and its marks.",
                         r"The clock is your time to try it: \ pause the video, \ work it out, \ then watch the solution."],
                        marks=0, color=GREY_B).move_to([0, 1.6, 0])
        rows = fit_rows(VGroup(
            label(r"Case 1: \ a trial to design \ (Parts 13, \ 25, \ 35)", font_size=26, color=CASE1),
            label(r"Case 2: \ an observational survey to analyse \ (Parts 36, \ 41)", font_size=26, color=CASE2),
            label(r"then twelve exam problems, \ one from each corner of the master's", font_size=26, color=S.ACCENT),
            label(r"every number recomputed by statkit; \ every solution written out in the README", font_size=22, color=GREY_A),
        ), 12.4, 0.4, [0, -1.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> After the two consulting cases comes the comprehensive exam itself. Each problem is posed "
            "on a card like this one, with the parts of the course it draws on. <bookmark mark='b'/> The clock is your time "
            "to try it: pause the video, work it out on paper, then watch the solution. <bookmark mark='c'/> The first case "
            "is a trial to design, and draws on Parts thirteen, twenty-five and thirty-five. The second is a survey to "
            "analyse, and draws on Parts thirty-six and forty-one. Then come twelve problems, one from each corner of the "
            "master's, and every number on screen is recomputed by our own code, with full solutions in the README."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(card.sweep(4.0))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.6), run_time=6.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 42", font_size=34, color=GREY_B), label(r"The Comprehensive Exam", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"design a cluster-randomized trial: \ the unit, \ the ICC, \ the sample size, \ the analysis plan",
            r"analyse an observational survey: \ the graph, \ bad controls, \ imputation, \ AIPW, \ sensitivity",
            r"write the report a minister can act on",
            r"twelve exam problems, \ from the sandwich to Greenwood's formula",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 21--41").to_corner(DL, buff=0.3)
        built = note(r"built: \ the MSc problem bank; \ the exam card").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-two: the comprehensive exam. <bookmark mark='b'/> We'll design a cluster-randomized "
            "trial, from the choice of unit to the analysis plan; analyse an observational survey with a causal graph, "
            "imputation, a doubly robust estimator and a sensitivity analysis; write the report a minister can act on; and "
            "then sit twelve exam problems, from the sandwich variance to Greenwood's formula."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
