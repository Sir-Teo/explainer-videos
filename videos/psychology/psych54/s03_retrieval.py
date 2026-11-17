from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403


class Retrieval(VoiceoverScene):
    def construct(self):
        card_section(self, 2, r"Retrieval practice", r"Is a test only a measurement?")
        self.lab()
        self.formats()
        self.classroom()

    def lab(self):
        head = heading(r"Study, \ or test?")
        A = axes([0.3, 4.7], [0, 0.9], x_length=5.4, y_length=3.0, xticks=None, yticks=[0, 0.4, 0.8],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"recall of a prose passage", center=[-3.3, 0.3, 0],
                 font_size=12)
        vals = [0.81, 0.75, 0.42, 0.56]
        cols = [PERSON, MODEL, PERSON, MODEL]
        b = bars(A.ax, [1, 2, 3.2, 4.2], vals, cols, width=0.6)
        names = VGroup(*[label(s, font_size=13, color=GREY_A).next_to(A.ax.c2p(x, 0), DOWN, buff=0.12)
                         for s, x in zip([r"restudy", r"test", r"restudy", r"test"], [1, 2, 3.2, 4.2])])
        when = VGroup(label(r"5 minutes later", font_size=13, color=GREY_B).next_to(A.ax.c2p(1.5, 0), DOWN, buff=0.45),
                      label(r"one week later", font_size=13, color=GREY_B).next_to(A.ax.c2p(3.7, 0), DOWN, buff=0.45))
        rows = rows_of([
            (r"Roediger and Karpicke, \ 2006: \ students read a passage, \ then either read it again or took a recall "
             r"test without feedback", WHITE),
            (r"five minutes later, \ rereading was ahead", PERSON),
            (r"a week later, \ the tested group remembered more: \ retrieval strengthens what it retrieves (Part 21)",
             MODEL),
            (r"the bars are the published means, \ approximately", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Roediger \& Karpicke (2006)")
        with self.voiceover(
            "Is a test only a measurement? <bookmark mark='a'/> In 2006 Henry Roediger and Jeffrey Karpicke had "
            "students read a passage, then either read it again or take a recall test without feedback. "
            "<bookmark mark='b'/> Five minutes later, rereading was ahead. <bookmark mark='c'/> A week later, the "
            "tested group remembered more. Retrieval strengthens what it retrieves. That's Part 21's testing effect. "
            "<bookmark mark='d'/> The bars here are the published means, approximately."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(when))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]), FadeIn(b[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[2]), FadeIn(b[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def classroom(self):
        chips_section(self, r"In classrooms", [
            (r"low-stakes quizzes", r"short, \ frequent, \ ungraded or nearly so: \ effects on later exams in middle "
                                    r"schools and universities", GOOD),
            (r"feedback", r"retrieval helps most when wrong answers are corrected afterwards", MODEL),
            (r"the transfer question", r"tested facts are remembered; \ transfer to new problems is smaller, \ but "
                                       r"present when quizzes ask for application", PERSON),
            (r"why students skip it", r"testing feels like failing, \ and rereading feels like learning", AUTH),
        ], "And in classrooms? <bookmark mark='a'/> Short, frequent, low-stakes quizzes improve later exams, in "
           "middle schools and universities alike. <bookmark mark='b'/> Retrieval helps most when wrong answers are "
           "corrected afterwards. <bookmark mark='c'/> Tested facts are remembered. Transfer to new problems is "
           "smaller, but present when the quizzes ask for application. <bookmark mark='d'/> And students skip it "
           "because testing feels like failing, and rereading feels like learning.")

    def formats(self):
        rows_section(self, r"Which kind of test?", [
            (r"recall (writing the answer) does more than recognition, \ when the learner can succeed at it", GOOD),
            (r"multiple choice still works when the wrong options are plausible: \ each must be ruled out, \ which "
             r"is retrieval", MODEL),
            (r"even a test before study helps: \ guessing wrong, \ then reading the answer, \ beats reading alone "
             r"(Richland, \ Kornell and Kao, \ 2009)", PERSON),
            (r"what does not work is a test too hard to answer and never corrected: \ retrieval needs success, \ or "
             r"feedback", AUTH),
        ], "Which kind of test? <bookmark mark='a'/> Recall, writing the answer out, does more than recognizing it, "
           "as long as the learner can succeed at it. <bookmark mark='b'/> Multiple choice still works when the wrong "
           "options are plausible, because each one has to be ruled out, and that's retrieval too. "
           "<bookmark mark='c'/> Even a test before study helps. Guessing wrong and then reading the answer beats "
           "reading alone. Lindsey Richland and colleagues showed it in 2009. "
           "<bookmark mark='d'/> What doesn't work is a test too hard to answer and never corrected. Retrieval needs "
           "success, or feedback.")
