from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Fatigue(VoiceoverScene):
    def construct(self):
        card_section(self, 12, r"Fatigue as a measured risk", r"How tired is too tired?")
        self.alcohol()
        self.clock()
        self.manage()

    def alcohol(self):
        d = load("fatigue")
        h, b = np.asarray(d["hours"]), np.asarray(d["bac"])
        head = heading(r"Hours awake, \ in drinks")
        A = axes([8, 26], [0, 0.12], x_length=5.6, y_length=3.0, xticks=[10, 14, 17, 20, 24], yticks=[0, 0.05, 0.1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}\\%", xlabel=r"hours awake",
                 ylabel=r"equivalent blood alcohol", center=[-3.3, 0.3, 0], font_size=12)
        c = curve(A.ax, h, b, AUTH, stroke_width=4)
        l5 = DashedLine(A.ax.c2p(8, 0.05), A.ax.c2p(26, 0.05), color=GREY_B)
        l5t = label(r"0.05\%: \ the driving limit in much of Europe and Australia", font_size=12, color=GREY_B)
        l5t.next_to(A.ax.c2p(8.3, 0.05), UR, buff=0.05)
        rows = rows_of([
            (r"Drew Dawson and Kathryn Reid, \ 1997: \ a hand-eye tracking task through 28 hours awake, \ and the same "
             r"people after doses of alcohol", WHITE),
            (r"after about 17 hours awake, \ performance like a blood alcohol of 0.05\%; \ after about 24 hours, \ "
             r"like 0.10\%", AUTH),
            (r"a shift that starts at 7 in the morning reaches 17 hours awake at midnight", PERSON),
            (r"the line is drawn as reported; \ the equivalence varies by task, \ but the scale holds", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Dawson \& Reid (1997)")
        with self.voiceover(
            "Part 10 built the clocks. Here's what they cost at work. <bookmark mark='a'/> In 1997 Drew Dawson and "
            "Kathryn Reid tested a hand-eye tracking task through twenty-eight hours awake, and in the same people "
            "after doses of alcohol. <bookmark mark='b'/> After about seventeen hours awake, performance was like a "
            "blood alcohol of zero point zero five percent. After about twenty-four hours, like zero point one. "
            "<bookmark mark='c'/> A shift that starts at seven in the morning reaches seventeen hours awake at "
            "midnight. <bookmark mark='d'/> The line here is drawn as they reported it. The equivalence varies by "
            "task, but the scale holds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(l5), FadeIn(l5t))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def clock(self):
        rows_section(self, r"Not only hours: \ the clock", [
            (r"Part 10's two processes: \ sleep pressure builds with hours awake; \ the circadian clock adds a trough "
             r"in the small hours", WHITE),
            (r"single-vehicle crashes from falling asleep peak in the early morning, \ and again in mid-afternoon",
             AUTH),
            (r"microsleeps: \ seconds of lost attention the person often does not notice", PERSON),
            (r"tired people judge their own impairment poorly: \ Part 25's confidence, \ again out of step with "
             r"accuracy", MODEL),
            (r"so a rule about hours alone misses the night shift's trough and the long commute home", YOU),
        ], "It's not only the hours. <bookmark mark='a'/> Part 10's two processes: sleep pressure builds with hours "
           "awake, and the circadian clock adds a trough in the small hours. <bookmark mark='b'/> Crashes from "
           "falling asleep at the wheel peak in the early morning, and again in mid-afternoon. <bookmark mark='c'/> "
           "There are microsleeps, seconds of lost attention that the person often doesn't notice. "
           "<bookmark mark='d'/> And tired people judge their own impairment poorly. That's Part 25's confidence, "
           "out of step with accuracy again. <bookmark mark='e'/> So a rule about hours alone misses the night "
           "shift's trough and the long drive home.")

    def manage(self):
        chips_section(self, r"Managing fatigue", [
            (r"hours of service", r"limits on duty and driving hours: \ simple to audit, \ blind to the clock and to "
                                  r"the sleep a person actually got", MODEL),
            (r"risk management", r"fatigue risk management systems: \ model the rosters with the two-process clock, "
                                 r"\ report fatigue without blame, \ and adjust", GOOD),
            (r"countermeasures", r"planned naps, \ caffeine timed to the trough, \ light, \ and a ride home after a "
                                 r"night shift", PERSON),
            (r"junior doctors", r"trials of shorter shifts for interns found fewer serious errors; \ later, \ larger "
                                r"trials of duty-hour rules found smaller or mixed effects", AUTH),
        ], "So how is fatigue managed? <bookmark mark='a'/> With limits on hours of service. They're simple to "
           "audit, and blind to the clock and to the sleep a person actually got. <bookmark mark='b'/> With fatigue "
           "risk management systems, which model the rosters with the two-process clock, collect fatigue reports "
           "without blame, and adjust. <bookmark mark='c'/> With countermeasures: planned naps, caffeine timed to the "
           "trough, light, and a ride home after a night shift. <bookmark mark='d'/> And for junior doctors, a "
           "contested case. A trial of shorter shifts for interns found fewer serious errors. Later and larger trials "
           "of duty-hour rules found smaller or mixed effects. The schedule matters, and so does what happens at "
           "each handover.", chip_w=3.6, text_w=8.6)
