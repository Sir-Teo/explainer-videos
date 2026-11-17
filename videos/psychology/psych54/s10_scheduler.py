from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403


class Scheduler(VoiceoverScene):
    def construct(self):
        card_section(self, 9, r"Scheduling reviews", r"When should the next review be?", marr=("how",))
        self.history()
        self.race()
        self.everyday()
        self.budget()

    def history(self):
        chips_section(self, r"From boxes to models", [
            (r"Leitner's boxes", r"1970s: \ flashcards move up a box when recalled, \ back to the first when not; \ "
                                 r"higher boxes are reviewed less often", GREY_B),
            (r"SM-2", r"Piotr Wo\'zniak's 1987 algorithm: \ each card's interval multiplied by an ease factor after "
                      r"each review; \ still inside many flashcard apps", MODEL),
            (r"half-life regression", r"Settles and Meeder, \ 2016: \ a model learned from millions of learners' "
                                      r"reviews predicts each word's half-life (Part 21)", PERSON),
            (r"optimal control", r"choose the review times that maximize what will be remembered when it is "
                                 r"needed, \ under a memory model", GOOD),
        ], "Spaced repetition began with boxes. <bookmark mark='a'/> In Sebastian Leitner's system of the "
           "nineteen seventies, a flashcard moves up a box when it's recalled and back to the first when it isn't, "
           "and higher boxes are reviewed less often. <bookmark mark='b'/> In 1987 Piotr Wozniak's SM-2 algorithm "
           "multiplied each card's interval by an ease factor after each review. It still runs inside many "
           "flashcard apps. <bookmark mark='c'/> In 2016 Burr Settles and Brendan Meeder fitted half-life "
           "regression to millions of learners' reviews, predicting each word's half-life, as Part 21 showed. "
           "<bookmark mark='d'/> And the frontier treats it as optimal control: choose the review times that "
           "maximize what will be remembered when it's needed, under a memory model.",
           chip_w=3.8, text_w=8.4, tag=published_tag(r"Settles \& Meeder (2016)"))

    def race(self):
        d = load("policies")
        head = heading(r"Four schedules, \ raced on Psyche")
        A = axes([0.3, 4.7], [0, 0.85], x_length=5.0, y_length=2.8, xticks=None, yticks=[0, 0.4, 0.8],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"recall on day 60", center=[-3.5, 0.6, 0], font_size=12)
        cols = [AUTH, PERSON, MODEL, GOOD]
        b = bars(A.ax, [1, 2, 3, 4], d["recall"], cols, width=0.6)
        names = VGroup(*[label(s, font_size=13, color=c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, (s, c) in enumerate(zip([r"massed", r"expanding", r"equal", r"model"], cols))])
        T = axes([0, 30], [0.5, 4.5], x_length=5.0, y_length=1.5, xticks=[0, 7, 14, 21, 28], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"review day", center=[-3.5, -2.5, 0], font_size=11)
        marks = VGroup()
        for i, times in enumerate(d["times"]):
            for t in times[1:]:
                marks.add(Dot(T.ax.c2p(float(t), 4 - i), radius=0.06, color=cols[i]))
        rows = rows_of([
            (r"60 items studied on day 0, \ then four reviews each before day 28; \ the test on day 60", WHITE),
            (rf"massed in one session: \ {100 * d['recall'][0]:.0f}\%", AUTH),
            (rf"expanding gaps: \ {100 * d['recall'][1]:.0f}\%; \ equal gaps: \ {100 * d['recall'][2]:.0f}\%: \ at a "
             rf"long delay, \ expanding is not better (as Karpicke and Roediger found)", PERSON),
            (rf"the model's choice, \ the schedule that maximizes predicted recall on day 60: \ "
             rf"{100 * d['recall'][3]:.0f}\%, \ with gaps that shrink towards the end", GOOD),
            (r"what matters most is spacing at all; \ the schedule's shape matters less, \ and depends on the test "
             r"date", YOU),
        ], 6.4, 18, 0.32).move_to([3.3, -0.4, 0])
        tag = psyche_tag(r"\texttt{work.schedule}, \ 60 items, \ equal study time")
        with self.voiceover(
            "Here are four schedules, raced on Psyche at equal study time. <bookmark mark='a'/> Sixty items are "
            "studied on day zero, each gets four reviews before day twenty-eight, and the test is on day sixty. "
            "<bookmark mark='b'/> Massed in one session, recall is seventeen percent. <bookmark mark='c'/> With "
            "expanding gaps, sixty-seven percent. With equal gaps, seventy-one. At a long delay, expanding isn't "
            "better, as Jeffrey Karpicke and Henry Roediger found. <bookmark mark='d'/> The model's choice, the "
            "schedule that maximizes predicted recall on day sixty, does about as well as equal gaps, with gaps that "
            "shrink towards the end. <bookmark mark='e'/> What matters most is spacing at all. The schedule's shape "
            "matters less, and depends on the test date."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(T))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(marks))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(b[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def budget(self):
        d = load("budget")
        head = heading(r"More reviews, \ or better-placed ones?")
        A = axes([0, 9], [0, 0.85], x_length=5.6, y_length=3.0, xticks=[1, 2, 4, 6, 8], yticks=[0, 0.4, 0.8],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"reviews per item",
                 ylabel=r"recall on day 60", center=[-3.3, 0.3, 0], font_size=12)
        cm = curve(A.ax, d["reviews"], d["massed"], AUTH, stroke_width=4)
        cf = curve(A.ax, d["reviews"], d["fixed"], GOOD, stroke_width=4)
        key = VGroup(label(r"massed", font_size=13, color=AUTH), label(r"spaced over four weeks", font_size=13,
                                                                     color=GOOD)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.2)
        rows = rows_of([
            (rf"massed: \ eight reviews in one session reach {100 * d['massed'][-1]:.0f}\%", AUTH),
            (rf"spaced: \ a single review a month later already gives {100 * d['fixed'][0]:.0f}\%", GOOD),
            (r"where a review goes is worth more than how many there are", MODEL),
            (r"for a learner with an hour a week, \ the scheduler's job is to spend it where forgetting is about to "
             r"happen", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.schedule}")
        with self.voiceover(
            "More reviews, or better-placed ones? <bookmark mark='a'/> Massed, even eight reviews in one session reach "
            "only about a quarter. <bookmark mark='b'/> Spaced, a single review four weeks later already gives forty "
            "percent. <bookmark mark='c'/> Where a review goes is worth more than how many there are. "
            "<bookmark mark='d'/> For a learner with an hour a week, the scheduler's job is to spend it where "
            "forgetting is about to happen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(cm))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cf))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def everyday(self):
        d = load("curves")
        days = d["days"]
        dt = float(days[1] - days[0])
        pols = ["massed", "expanding", "fixed", "model"]
        cols = [AUTH, PERSON, MODEL, GOOD]
        above = [float((d[p] >= 0.5).sum() * dt) for p in pols]
        head = heading(r"Best on the test day, \ or best every day?")
        A = axes([0, 61], [0, 1.05], x_length=5.6, y_length=2.6, xticks=[0, 14, 28, 45, 60], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"day",
                 ylabel=r"recall, \ one item", center=[-3.3, 0.9, 0], font_size=12)
        half = DashedLine(A.ax.c2p(0, 0.5), A.ax.c2p(61, 0.5), color=GREY_B, stroke_width=2)
        cs = VGroup(*[curve(A.ax, days, d[p], c, stroke_width=3) for p, c in zip(pols, cols)])
        B = axes([0.3, 4.7], [0, 64], x_length=5.6, y_length=1.6, xticks=None, yticks=[0, 30, 60],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"days above half", center=[-3.3, -2.3, 0], font_size=11)
        b = bars(B.ax, [1, 2, 3, 4], above, cols, width=0.6)
        bl = VGroup(*[label(t, font_size=12, color=c).next_to(B.ax.c2p(i + 1, 0), DOWN, buff=0.1)
                      for i, (t, c) in enumerate(zip([r"massed", r"expanding", r"equal", r"model"], cols))])
        rows = rows_of([
            (r"the same four schedules, \ one item, \ followed every day instead of only on day 60", WHITE),
            (rf"massed stays above one half for {above[0]:.0f} of the 60 days", AUTH),
            (rf"expanding gaps keep it above half on all {above[1]:.0f}: \ early reviews come before the first "
             rf"forgetting", PERSON),
            (rf"the model's schedule, \ chosen for day 60, \ lets recall dip early: \ {above[3]:.0f} days", GOOD),
            (r"a learner who will be tested once wants the last; \ a nurse or a pilot who may need the fact any day "
             r"wants the second: \ the goal sets the schedule", YOU),
        ], 6.0, 18, 0.32).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"Psyche's memory (Part 21), \ decay capped")
        with self.voiceover(
            "But best on the test day isn't the only goal. <bookmark mark='a'/> Here are the same four schedules for "
            "one item, followed every day instead of only on day sixty. <bookmark mark='b'/> Massed study stays above "
            "one half for about seventeen of the sixty days. <bookmark mark='c'/> Expanding gaps keep it above half "
            "on all sixty, because the early reviews come before the first forgetting. <bookmark mark='d'/> The "
            "model's schedule, chosen for day sixty, lets recall dip early, and is above half on about fifty-two "
            "days. <bookmark mark='e'/> A learner who'll be tested once wants the last. A nurse or a pilot, who may "
            "need the fact on any day, wants the second. The goal sets the schedule."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(half), FadeIn(B), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), *[Create(c) for c in cs], run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(b[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
