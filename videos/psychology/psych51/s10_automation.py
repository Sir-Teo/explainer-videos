from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Automation(VoiceoverScene):
    def construct(self):
        card_section(self, 9, r"The ironies of automation", r"Does better automation make a safer system?",
                     scale=("person", "society"))
        self.levels()
        self.ironies()
        self.takeover()
        self.modes()
        self.af447()

    def levels(self):
        chips_section(self, r"Levels and stages", [
            (r"ten levels", r"Sheridan and Verplank, \ 1978: \ from the human doing everything, \ through the computer "
                            r"suggesting, \ to the computer acting and telling no one", MODEL),
            (r"four stages", r"Parasuraman, \ Sheridan and Wickens, \ 2000: \ automate acquiring information, \ "
                             r"analysing it, \ deciding, \ or acting; \ each to its own level", PERSON),
            (r"driving's levels", r"the SAE's 0 to 5: \ at level 2 the driver supervises at every moment; \ at level 3 "
                                  r"the car drives, \ and the driver must take over when asked", AUTH),
            (r"the question", r"not ``how much automation?'' \ but ``which function, \ to what level, \ with the human "
                              r"doing what?''", YOU),
        ], "Automation isn't all or nothing. <bookmark mark='a'/> In 1978 Thomas Sheridan and William Verplank laid out "
           "ten levels, from the human doing everything, through the computer suggesting, to the computer acting and "
           "telling no one. <bookmark mark='b'/> In 2000 Raja Parasuraman, Sheridan and Christopher Wickens added "
           "stages. You can automate acquiring information, analysing it, deciding, or acting, each to its own level. "
           "<bookmark mark='c'/> Driving has its own scale, from zero to five. At level two the driver supervises at "
           "every moment. At level three the car drives, and the driver must take over when asked. "
           "<bookmark mark='d'/> So the question isn't how much automation. It's which function, to what level, with "
           "the human doing what?", chip_w=3.4, text_w=8.8)

    def ironies(self):
        rows_section(self, r"Lisanne Bainbridge's ironies, \ 1983", [
            (r"designers automate the tasks people do badly, \ and leave the human the tasks they could not automate",
             WHITE),
            (r"the human becomes a monitor: \ Part 18's vigilance, \ asked of someone with nothing to do", PERSON),
            (r"and the backup when the automation fails: \ but skills fade without practice, \ and the failures that "
             r"reach the human are the hard ones", AUTH),
            (r"the more reliable the automation, \ the rarer the practice, \ and the less ready the human when it "
             r"fails", MODEL),
            (r"her advice: \ keep the human in practice: \ simulators, \ manual phases, \ displays that show what the "
             r"automation is doing", GOOD),
        ], "In 1983 Lisanne Bainbridge named the ironies of automation. <bookmark mark='a'/> Designers automate the "
           "tasks people do badly, and leave the human the tasks they couldn't automate. <bookmark mark='b'/> The "
           "human becomes a monitor. That's Part 18's vigilance, asked of someone with nothing to do. "
           "<bookmark mark='c'/> And the human is the backup when the automation fails. But skills fade without "
           "practice, and the failures that reach the human are the hard ones. <bookmark mark='d'/> So the more "
           "reliable the automation, the rarer the practice, and the less ready the human when it fails. "
           "<bookmark mark='e'/> Her advice was to keep the human in practice: simulators, manual phases, and "
           "displays that show what the automation is doing.", tag=published_tag(r"Bainbridge (1983)"))

    def takeover(self):
        d = load("takeover")
        head = heading(r"The irony, \ as a model")
        A = axes([0.3, 4.7], [0, 1.0], x_length=5.4, y_length=3.0, xticks=None, yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"takeovers within 7 s", center=[-3.3, 0.4, 0],
                 font_size=12)
        b = bars(A.ax, [1, 2, 3, 4], d["within"], MODEL, width=0.6)
        names = VGroup(*[label(rf"1 in {round(1 / (1 - r)):,}", font_size=13, color=GREY_A)
                         .next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12) for i, r in enumerate(d["reliability"])])
        nl = label(r"automation fails", font_size=13, color=GREY_A).next_to(names, DOWN, buff=0.1)
        vals = VGroup(*[label(rf"{100 * w:.0f}\%", font_size=14, color=MODEL).next_to(A.ax.c2p(i + 1, w), UP, buff=0.08)
                        for i, w in enumerate(d["within"])])
        sf = d["system_fail"]
        rows = rows_of([
            (r"assumed: \ the operator's median takeover time grows with the log of the time between failures", WHITE),
            (rf"median takeover: \ {d['median_s'][0]:.1f} s at one failure in 10, \ {d['median_s'][-1]:.1f} s at one "
             rf"in 10,000", MODEL),
            (rf"within a 7-second budget: \ {100 * d['within'][0]:.0f}\% falls to {100 * d['within'][-1]:.0f}\%", AUTH),
            (rf"yet the system still gets safer: \ failures per demand fall from {1000 * sf[0]:.1f} in 1,000 to "
             rf"{100000 * sf[-1]:.0f} in 100,000", GOOD),
            (r"the irony is not that automation is unsafe: \ it is that the residual risk moves to the moment the "
             r"human is least ready", YOU),
        ], 6.0, 19, 0.32).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.takeover}, \ an assumed slowing")
        with self.voiceover(
            "Here's the irony as a model. <bookmark mark='a'/> Assume that an operator's median takeover time grows "
            "with the logarithm of the time between failures, as practice and expectation fade. That's an "
            "assumption, chosen to show the shape. <bookmark mark='b'/> The median takeover goes from about three and "
            "a half seconds, when the automation fails once in ten demands, to six seconds, when it fails once in ten "
            "thousand. <bookmark mark='c'/> Within a seven-second budget, ninety-five percent of takeovers succeed at "
            "first, and sixty-two percent at the end. <bookmark mark='d'/> And yet the system still gets safer. "
            "Failures per demand fall from about five in a thousand to about four in a hundred thousand, because the "
            "automation fails so much less often. <bookmark mark='e'/> So the irony isn't that automation is unsafe. "
            "It's that the residual risk moves to the moment the human is least ready."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(nl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b), FadeIn(vals))
            for m, r in zip("cde", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def modes(self):
        rows_section(self, r"Mode confusion", [
            (r"a mode is the automation's current way of interpreting the same input", WHITE),
            (r"Strasbourg, \ 1992: \ an Airbus crew meant a 3.3-degree descent path; \ the autopilot was in a "
             r"vertical-speed mode, \ and the same entry meant 3,300 feet per minute", AUTH),
            (r"the two modes differed on the display by a few characters", PERSON),
            (r"``what is it doing now?'' \ is the most common question in automated cockpits (Wiener's surveys)", MODEL),
            (r"the design rule: \ few modes, \ no silent mode changes, \ and the mode shown where the eyes are", GOOD),
        ], "Automation adds a new error: mode confusion. <bookmark mark='a'/> A mode is the automation's current way of "
           "interpreting the same input. <bookmark mark='b'/> Near Strasbourg in 1992, an Airbus crew is believed to "
           "have meant a three point three degree descent path. The autopilot was in a vertical-speed mode, and the "
           "same entry meant three thousand three hundred feet per minute. <bookmark mark='c'/> The two modes differed "
           "on the display by a few characters. <bookmark mark='d'/> In Earl Wiener's surveys of airline pilots, what "
           "is it doing now was among the most common questions in automated cockpits. <bookmark mark='e'/> The design "
           "rule: few modes, no silent mode changes, and the mode shown where the eyes already are.")

    def af447(self):
        rows_section(self, r"Air France 447, \ 2009", [
            (r"over the Atlantic at night, \ ice blocked the airspeed probes; \ the autopilot disconnected and handed "
             r"the aircraft back", WHITE),
            (r"the pilot flying pulled the nose up; \ the aircraft climbed, \ slowed, \ and stalled", AUTH),
            (r"the stall warning sounded, \ then fell silent when the airspeed read so low it was rejected as "
             r"invalid; \ lowering the nose brought it back", PERSON),
            (r"the crew never identified the stall; \ 228 people died", AUTH),
            (r"the investigators cited the surprise of a takeover at altitude, \ little practice in manual flight "
             r"there, \ and a warning that taught the wrong lesson", YOU),
        ], "Here's the takeover problem at its worst. <bookmark mark='a'/> In 2009, over the Atlantic at night, ice "
           "blocked an Airbus's airspeed probes. The autopilot disconnected and handed the aircraft back to the crew. "
           "<bookmark mark='b'/> The pilot flying pulled the nose up. The aircraft climbed, slowed, and stalled. "
           "<bookmark mark='c'/> The stall warning sounded, and then fell silent when the airspeed read so low that "
           "it was rejected as invalid. Lowering the nose, the right action, brought the warning back. "
           "<bookmark mark='d'/> The crew never identified the stall, and two hundred and twenty-eight people died. "
           "<bookmark mark='e'/> The French investigators cited the surprise of a takeover at cruise altitude, little "
           "practice in manual flight there, and a warning that taught the wrong lesson. Bainbridge's ironies, all "
           "at once.")
