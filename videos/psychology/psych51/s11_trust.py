from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Trust(VoiceoverScene):
    def construct(self):
        card_section(self, 10, r"Trust and alarms", r"How much should an operator believe a machine?")
        self.calibration()
        self.alarm()
        self.wolf()
        self.ward()

    def calibration(self):
        head = heading(r"Trust that fits")
        A = axes([0, 1], [0, 1], x_length=4.0, y_length=4.0, xticks=[0, 1], yticks=[0, 1],
                 xfmt=lambda v: [r"low", r"high"][int(v)], yfmt=lambda v: [r"low", r"high"][int(v)],
                 xlabel=r"the automation's reliability", ylabel=r"the operator's trust", center=[-3.8, 0.0, 0],
                 font_size=12)
        diag = Line(A.ax.c2p(0, 0), A.ax.c2p(1, 1), color=GOOD, stroke_width=4)
        over = Polygon(A.ax.c2p(0, 0), A.ax.c2p(0, 1), A.ax.c2p(1, 1), color=AUTH, fill_opacity=0.18, stroke_width=0)
        under = Polygon(A.ax.c2p(0, 0), A.ax.c2p(1, 0), A.ax.c2p(1, 1), color=MODEL, fill_opacity=0.18,
                        stroke_width=0)
        lo = label(r"overtrust: \ misuse", font_size=15, color=AUTH).move_to(A.ax.c2p(0.3, 0.78))
        lu = label(r"distrust: \ disuse", font_size=15, color=MODEL).move_to(A.ax.c2p(0.72, 0.22))
        rows = rows_of([
            (r"John Lee and Katrina See, \ 2004: \ the goal is not high trust but calibrated trust, \ on the diagonal",
             WHITE),
            (r"misuse: \ relying on automation beyond its competence; \ automation bias, \ following a wrong "
             r"recommendation, \ or missing what it misses", AUTH),
            (r"disuse: \ ignoring good automation after a few false alarms or one vivid failure", MODEL),
            (r"trust follows what operators can see: \ show the automation's reliability for this situation, \ not "
             r"on average", GOOD),
            (r"Part 26's algorithm aversion is disuse; \ the complacency row in chapter thirteen is misuse", YOU),
        ], 6.6, 19, 0.32).move_to([3.0, -0.2, 0])
        with self.voiceover(
            "How much should an operator believe a machine? <bookmark mark='a'/> John Lee and Katrina See put it "
            "simply in 2004. The goal isn't high trust but calibrated trust, on the diagonal, matched to how reliable "
            "the automation really is. <bookmark mark='b'/> Above the diagonal is misuse: relying on automation beyond "
            "its competence. Automation bias, following a wrong recommendation or missing what it misses. "
            "<bookmark mark='c'/> Below is disuse: ignoring good automation after a few false alarms or one vivid "
            "failure. <bookmark mark='d'/> Trust follows what operators can see, so show the automation's reliability "
            "for this situation, not on average. <bookmark mark='e'/> Part 26's algorithm aversion is disuse, and "
            "chapter thirteen's complacency row is misuse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(diag))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(over), FadeIn(lo))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(under), FadeIn(lu))
            for m, r in zip("de", rows[3:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def alarm(self):
        d = load("alarm")
        th = np.asarray(d["threshold"])
        head = heading(r"An alarm is a criterion")
        A = axes([-0.5, 3.5], [0, 1.0], x_length=5.8, y_length=3.2, xticks=[0, 1, 2, 3], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"alarm threshold (sensor SDs)",
                 ylabel=r"rate", center=[-3.2, 0.3, 0], font_size=12)
        ch = curve(A.ax, th, d["hit"], PERSON, stroke_width=4)
        cp = curve(A.ax, th, d["ppv"], AUTH, stroke_width=4)
        cc = curve(A.ax, th, d["caught"], GOOD, stroke_width=4)
        key = VGroup(label(r"events alarmed", font_size=13, color=PERSON), label(r"alarms that are real", font_size=13,
                                                                                   color=AUTH),
                     label(r"events answered", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.3)
        key.next_to(A, UP, buff=0.2)
        k1 = int(np.argmin(np.abs(th - 1.0)))
        best = float(d["best"])
        vb = DashedLine(A.ax.c2p(best, 0), A.ax.c2p(best, 1.0), color=GOOD)
        rows = rows_of([
            (r"a sensor reads noise, \ or an event 2.5 SDs higher; \ events are 1 reading in 100", WHITE),
            (rf"a cautious threshold of 1 SD alarms on {100 * d['hit'][k1]:.0f}\% of events, \ but only "
             rf"{100 * d['ppv'][k1]:.1f}\% of its alarms are real", PERSON),
            (r"operators learn the odds: \ if they answer an alarm as often as alarms are real (Bliss's probability "
             r"matching), \ few events get an answer", AUTH),
            (rf"the threshold that gets most events answered is {best:.1f} SDs, \ and it gets only "
             rf"{100 * d['best_caught']:.0f}\%", GOOD),
            (r"the engineer sets one criterion, \ the operator's trust sets a second; \ design both", YOU),
        ], 6.0, 19, 0.32).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.alarm}, \ $d'$ = 2.5, \ base rate 1\%")
        with self.voiceover(
            "An alarm is Part 12's criterion, chosen by an engineer. <bookmark mark='a'/> A sensor reads noise, or an "
            "event two and a half standard deviations higher, and events are one reading in a hundred. "
            "<bookmark mark='b'/> A cautious threshold of one standard deviation alarms on ninety-three percent of "
            "events. But only five or six percent of its alarms are real. <bookmark mark='c'/> Operators learn the "
            "odds. James Bliss found that people answer alarms about as often as alarms are real, and if they do, few "
            "events get an answer. <bookmark mark='d'/> The threshold that gets the most events answered is about two "
            "point seven, and even it gets only twenty-three percent. <bookmark mark='e'/> So the engineer sets one "
            "criterion, and the operator's trust sets a second. You have to design both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(ch), Create(cp))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(cc))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Create(vb))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def wolf(self):
        chips_section(self, r"Better alarms", [
            (r"raise the base rate", r"alarm on combinations and trends rather than single readings, \ so more alarms "
                                     r"are real", GOOD),
            (r"grade the alarm", r"likelihood alarms: \ ``possible'', \ ``likely'', \ ``certain'', \ so the response "
                                 r"can match (Sorkin)", MODEL),
            (r"delay and fit", r"a few seconds' delay and limits fitted to the patient remove many alarms that "
                               r"settle on their own", PERSON),
            (r"count them", r"alarms per hour and the share acted on are measurable; \ a design review sets targets",
             SYMP),
        ], "So how do you build a better alarm? <bookmark mark='a'/> Raise the base rate. Alarm on combinations and "
           "trends rather than single readings, so more alarms are real. <bookmark mark='b'/> Grade the alarm. "
           "Robert Sorkin's likelihood alarms say possible, likely or certain, so the response can match. "
           "<bookmark mark='c'/> Delay and fit. A few seconds' delay, and limits fitted to the patient, remove many "
           "alarms that settle on their own. <bookmark mark='d'/> And count them. Alarms per hour and the share acted "
           "on are measurable, and a design review can set targets.", chip_w=3.6, text_w=8.6)

    def ward(self):
        rows_section(self, r"Alarm fatigue on the ward", [
            (r"a monitored intensive-care bed can sound hundreds of alarms a day", WHITE),
            (r"studies of bedside monitors find that most alarms are false or need no action", AUTH),
            (r"nurses turn volumes down, \ widen limits, \ or stop hearing them: \ the ``cry wolf'' effect, \ "
             r"a learned criterion", PERSON),
            (r"in 2013 the US Joint Commission issued an alert on alarm safety, \ after deaths linked to alarms that "
             r"went unanswered", AUTH),
            (r"the nurse's criterion is rational for the alarms they have been given: \ fix the alarms", YOU),
        ], "Here's what that looks like in a hospital. <bookmark mark='a'/> A monitored intensive-care bed can sound "
           "hundreds of alarms a day. <bookmark mark='b'/> Studies of bedside monitors find that most of those alarms "
           "are false or need no action. <bookmark mark='c'/> So nurses turn volumes down, widen limits, or stop "
           "hearing them. That's the cry wolf effect, and it's a learned criterion. <bookmark mark='d'/> In 2013 the "
           "American Joint Commission issued an alert on alarm safety, after deaths linked to alarms that went "
           "unanswered. <bookmark mark='e'/> The nurse's criterion is rational for the alarms they've been given. "
           "Fix the alarms.")
