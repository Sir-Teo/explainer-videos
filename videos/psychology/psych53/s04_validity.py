from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Validity(VoiceoverScene):
    def construct(self):
        card_section(self, 3, r"Validity and the criterion", r"What does it mean for a test to predict a job?")
        self.cloud()
        self.criterion()

    def cloud(self):
        d = load("selection")
        head = heading(r"A predictor and a criterion")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        A = axes([-3.5, 3.5], [-3.5, 3.5], x_length=4.6, y_length=4.0, xticks=[-2, 0, 2], yticks=[-2, 0, 2],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"test score (z)",
                 ylabel=r"rated performance (z)", center=[-3.6, 0.0, 0], font_size=12)
        pts = scatter(A.ax, np.clip(x[:1200], -3.4, 3.4), np.clip(y[:1200], -3.4, 3.4), CROWD, radius=0.025)
        rows = rows_of([
            (r"criterion-related validity: \ the correlation between a predictor (a test, \ an interview) and a "
             r"criterion (later performance)", WHITE),
            (rf"Psyche's applicants: \ a test whose true validity is 0.5; \ with a rating as the criterion, \ the "
             rf"observed correlation is {d['r_all_obs']:.2f}", MODEL),
            (r"a correlation of 0.5 is large for psychology, \ and still a wide cloud: \ many high scorers do "
             r"poorly, \ and the reverse", PERSON),
            (r"predictive designs test applicants and wait; \ concurrent designs test current staff: \ cheaper, \ "
             r"and with consequences for the corrections of chapter four", YOU),
        ], 7.2, 19, 0.36).move_to([2.9, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.selection}, \ simulated applicants")
        with self.voiceover(
            "What does it mean for a test to predict a job? <bookmark mark='a'/> Criterion-related validity is the "
            "correlation between a predictor, a test or an interview, and a criterion, usually later performance. "
            "<bookmark mark='b'/> Here are Psyche's applicants. The test's true validity is zero point five, and with "
            "a supervisor's rating as the criterion, the observed correlation is about zero point three nine. "
            "<bookmark mark='c'/> A correlation of zero point five is large for psychology, and still a wide cloud. "
            "Many high scorers do poorly, and the reverse. <bookmark mark='d'/> Predictive designs test applicants "
            "and wait. Concurrent designs test current staff, which is cheaper, and has consequences for the "
            "corrections of chapter four."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(pts))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def criterion(self):
        chips_section(self, r"The criterion problem", [
            (r"what is performance?", r"output, \ quality, \ helping colleagues, \ not causing harm: \ task and "
                                      r"contextual performance, \ and counterproductive behaviour", MODEL),
            (r"who rates it?", r"usually one supervisor, \ once a year", PERSON),
            (r"rater idiosyncrasy", r"in Scullen, \ Mount and Goff's analysis, \ more of the variance in ratings "
                                   r"belonged to the rater than to the person rated", AUTH),
            (r"reliability", r"two supervisors rating the same people agree at about 0.5: \ Part 3's attenuation, \ "
                             r"built into every validity", SYMP),
        ], "And then there's the criterion problem. <bookmark mark='a'/> What is performance? Output, quality, "
           "helping colleagues, not causing harm. Researchers distinguish task performance, contextual performance, "
           "and counterproductive behaviour. <bookmark mark='b'/> Who rates it? Usually one supervisor, once a year. "
           "<bookmark mark='c'/> In Steven Scullen, Michael Mount and Maynard Goff's analysis of multi-rater "
           "feedback, more of the variance in ratings belonged to the rater than to the person being rated. "
           "<bookmark mark='d'/> And two supervisors rating the same people agree at about zero point five. That's "
           "Part 3's attenuation, built into every validity.", chip_w=3.6, text_w=8.6)
