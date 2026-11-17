from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Defaults(VoiceoverScene):
    def construct(self):
        card_section(self, 2, r"Why defaults work", r"Why does a pre-ticked box matter so much?", marr=("how",))
        self.madrian()
        self.why()
        self.smart()

    def madrian(self):
        d = load("inertia")
        head = heading(r"Automatic enrolment")
        A = axes([0.3, 2.7], [0, 1.0], x_length=4.0, y_length=3.0, xticks=None, yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"enrolled in the savings plan", center=[-4.0, 0.6, 0],
                 font_size=12)
        b = bars(A.ax, [1, 2], [0.37, 0.86], [AUTH, GOOD], width=0.7)
        names = VGroup(label(r"opt in", font_size=14, color=AUTH).next_to(A.ax.c2p(1, 0), DOWN, buff=0.12),
                       label(r"enrolled unless they opt out", font_size=14, color=GOOD).next_to(A.ax.c2p(2, 0), DOWN,
                                                                                                buff=0.12))
        eq = MathTex(r"\text{opt in} = (1-q)\,p, \qquad \text{opt out} = q + (1-q)\,p", font_size=30)
        eq.move_to([3.2, 2.0, 0])
        rows = rows_of([
            (r"Madrian and Shea, \ 2001: \ a US company switched new employees from opt-in to automatic enrolment; \ "
             r"participation rose from 37\% to 86\%", WHITE),
            (r"a two-type reading: \ a share $q$ stay with whatever is set; \ of the rest, \ a share $p$ want in", MODEL),
            (rf"solving: \ $q$ = {d['inertia']:.2f}, \ $p$ = {d['prefer']:.2f}: \ half the workforce goes with the "
             rf"default", PERSON),
            (r"but most also stayed at the default contribution rate and fund: \ the default sets what people save, \ "
             r"not only whether", AUTH),
        ], 6.2, 19, 0.34).move_to([3.2, -0.6, 0])
        tag = published_tag(r"Madrian \& Shea (2001)")
        with self.voiceover(
            "The cleanest default is in retirement saving. <bookmark mark='a'/> In 2001 Brigitte Madrian and Dennis "
            "Shea studied a company that switched new employees from opting in to automatic enrolment. Participation "
            "rose from thirty-seven percent to eighty-six. <bookmark mark='b'/> Here's a simple reading. A share q of "
            "people stay with whatever is set, and of the rest, a share p want in. <bookmark mark='c'/> Solving the "
            "two equations: q is about a half, and p about three quarters. Half the workforce goes with the default. "
            "<bookmark mark='d'/> But most also stayed at the default contribution rate and fund, which were low. The "
            "default sets what people save, not only whether."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Write(eq))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def why(self):
        chips_section(self, r"Three reasons a default works", [
            (r"effort", r"changing it takes a form, \ a decision and time; \ inertia wins when the stakes feel "
                        r"distant", PERSON),
            (r"endorsement", r"a default reads as a recommendation: \ the designer must know best", MODEL),
            (r"reference point", r"the default becomes what you have, \ and leaving it a loss (Part 26's loss "
                                 r"aversion)", AUTH),
            (r"the lesson", r"choosing no default is impossible: \ every form has one, \ so choose it deliberately", GOOD),
        ], "Why does a pre-ticked box matter so much? <bookmark mark='a'/> Effort: changing it takes a form, a "
           "decision and time, and inertia wins when the stakes feel distant. <bookmark mark='b'/> Endorsement: a "
           "default reads as a recommendation, as if the designer must know best. <bookmark mark='c'/> And reference "
           "point: the default becomes what you have, and leaving it feels like a loss. That's Part 26's loss "
           "aversion. <bookmark mark='d'/> The lesson: choosing no default is impossible. Every form has one, so "
           "choose it deliberately.")

    def smart(self):
        rows_section(self, r"Save More Tomorrow", [
            (r"Thaler and Benartzi, \ 2004: \ employees committed in advance to raise their saving rate at each "
             r"future pay rise", WHITE),
            (r"it used three of Part 26's biases: \ present bias (the cost is later), \ loss aversion (take-home pay "
             r"never falls), \ and inertia (it continues unless stopped)", MODEL),
            (r"in the first company, \ saving rates of participants rose from about 3.5\% to about 13.6\% over "
             r"four years", GOOD),
            (r"automatic escalation is now common in pension law; \ the evidence is strongest where people would "
             r"otherwise save too little", PERSON),
        ], "Defaults can also move over time. <bookmark mark='a'/> In 2004 Richard Thaler and Shlomo Benartzi had "
           "employees commit in advance to raise their saving rate at each future pay rise. <bookmark mark='b'/> It "
           "used three of Part 26's biases: present bias, because the cost comes later; loss aversion, because "
           "take-home pay never falls; and inertia, because it continues unless stopped. <bookmark mark='c'/> In the "
           "first company, participants' saving rates rose from about three and a half percent to about thirteen and "
           "a half over four years. <bookmark mark='d'/> Automatic escalation is now common in pension law. The "
           "evidence is strongest where people would otherwise save too little.",
           tag=published_tag(r"Thaler \& Benartzi (2004)"))
