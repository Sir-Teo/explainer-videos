from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403


class Bjork(VoiceoverScene):
    def construct(self):
        card_section(self, 4, r"Learning against performance", r"Why does the better method feel worse?")
        self.curves()
        self.feel()

    def curves(self):
        d = load("curves")
        head = heading(r"Cramming wins the week, \ and loses the term")
        A = axes([0, 61], [0, 1.05], x_length=5.6, y_length=3.0, xticks=[0, 7, 14, 21, 28, 60], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"day",
                 ylabel=r"recall, \ if tested now", center=[-3.3, 0.3, 0], font_size=12)
        cm = curve(A.ax, d["days"], d["massed"], AUTH, stroke_width=4)
        cf = curve(A.ax, d["days"], d["fixed"], GOOD, stroke_width=4)
        key = VGroup(label(r"four reviews crammed on day 0", font_size=13, color=AUTH),
                     label(r"four reviews a week apart", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.2)
        k5, k60 = int(np.argmin(np.abs(d["days"] - 5))), len(d["days"]) - 1
        rows = rows_of([
            (r"Psyche studies once and reviews four times: \ all at once, \ or once a week", WHITE),
            (rf"on day 5, \ cramming looks far better: \ {100 * d['massed'][k5]:.0f}\% against "
             rf"{100 * d['fixed'][k5]:.0f}\%", AUTH),
            (rf"on day 60: \ {100 * d['massed'][k60]:.0f}\% against {100 * d['fixed'][k60]:.0f}\%", GOOD),
            (r"Robert and Elizabeth Bjork: \ performance during learning is a poor guide to learning; \ the "
             r"difficulties that slow practice down are often the ones that make it last", MODEL),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"Psyche's memory (Part 21), \ decay capped")
        with self.voiceover(
            "Why does the better method feel worse? <bookmark mark='a'/> Psyche studies once and reviews four times: "
            "all at once, or once a week. <bookmark mark='b'/> On day five, cramming looks far better: over ninety "
            "percent, against about thirty for the spaced learner, who is due a review. <bookmark mark='c'/> On day "
            "sixty, it's fourteen percent against seventy-four. <bookmark mark='d'/> Robert and Elizabeth Bjork call "
            "this the difference between learning and performance. Performance during practice is a poor guide to "
            "learning, and the difficulties that slow practice down are often the ones that make it last. They call "
            "them desirable difficulties."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(cm), Create(cf), run_time=2.5)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def feel(self):
        rows_section(self, r"The illusion of fluency", [
            (r"rereading makes the text feel familiar, \ and familiarity feels like knowing (Part 25's confidence)", WHITE),
            (r"Kornell and Bjork, \ 2008: \ most learners judged massed study of painters' styles better, \ even after "
             r"learning more from the interleaved", AUTH),
            (r"Deslauriers and colleagues, \ 2019: \ physics students learned more in active classes, \ and rated "
             r"them as teaching them less", MODEL),
            (r"Freeman and colleagues, \ 2014: \ across 225 studies, \ students in traditional lectures were about one "
             r"and a half times as likely to fail as in active learning", GOOD),
            (r"so learners need to be told, \ with evidence on themselves, \ that the hard way works", YOU),
        ], "The trap has a name: the illusion of fluency. <bookmark mark='a'/> Rereading makes the text feel familiar, "
           "and familiarity feels like knowing. That's Part 25's confidence, misled. <bookmark mark='b'/> Nate "
           "Kornell and Robert Bjork found that most learners judged massed study of painters' styles to be better, "
           "even after learning more from interleaved study. <bookmark mark='c'/> Louis Deslauriers and colleagues "
           "found that physics students learned more in active classes, and rated those classes as teaching them "
           "less. <bookmark mark='d'/> And across two hundred and twenty-five studies, Scott Freeman and colleagues "
           "found students in traditional lectures about one and a half times as likely to fail as in active "
           "learning. <bookmark mark='e'/> So learners need to be told, with evidence on themselves, that the hard "
           "way works. That's what the experiment on you is for.", tag=published_tag(r"Deslauriers et al.\ (2019)"))
