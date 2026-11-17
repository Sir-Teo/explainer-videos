from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card_section(self, 14, r"In practice: \ a takeover request, \ designed", r"How would you hand a car back to "
                     r"its driver?", scale=("person", "society"))
        self.where()
        self.design()
        self.timeline()
        self.case()

    def where(self):
        chips_section(self, r"Where human factors works", [
            (r"aviation", r"certification requires a human-factors case for cockpit designs; \ incidents are reported "
                          r"without blame and analysed", MODEL),
            (r"medical devices", r"usability engineering standards: \ test with real users the tasks where a "
                                 r"use error could harm", SYMP),
            (r"control rooms", r"nuclear, \ rail and power: \ alarm management targets, \ procedure design, \ "
                               r"simulator training", PERSON),
            (r"vehicles", r"driver monitoring, \ takeover requests, \ and the evidence that drivers of partly automated "
                          r"cars look away", AUTH),
        ], "Where does this work get done? <bookmark mark='a'/> In aviation, where certification asks for a "
           "human-factors case for cockpit designs, and incidents are reported without blame and analysed. "
           "<bookmark mark='b'/> In medical devices, where usability standards require testing with real users on the "
           "tasks where a use error could harm. <bookmark mark='c'/> In control rooms for nuclear power, rail and the "
           "grid: alarm management targets, procedure design, and simulator training. <bookmark mark='d'/> And in "
           "vehicles: driver monitoring, takeover requests, and the evidence that drivers of partly automated cars "
           "look away.", chip_w=3.4, text_w=8.8)

    def design(self):
        chips_section(self, r"The brief", [
            (r"the situation", r"a level-3 car on a motorway; \ the system will reach the end of the road it can handle "
                               r"in 40 seconds, \ or meets a fault now", WHITE),
            (r"what we know", r"chapter nine: \ takeover times stretch with reliability; \ chapter six: \ a driver "
                              r"out of the loop has lost awareness at levels 2 and 3", MODEL),
            (r"the target", r"most drivers stable and in control before the budget runs out, \ measured in a "
                            r"simulator, \ with a pre-registered criterion", GOOD),
        ], "Here's a worked design. <bookmark mark='a'/> The situation: a level-three car on a motorway. The system "
           "will reach the end of the road it can handle in forty seconds, or it meets a fault now. "
           "<bookmark mark='b'/> What we know: chapter nine's takeover times stretch with reliability, and a driver "
           "out of the loop has lost awareness at levels two and three. <bookmark mark='c'/> The target: most drivers "
           "stable and in control before the budget runs out, measured in a simulator, with a criterion written down "
           "in advance, as Part 43 asked.", chip_w=3.0, text_w=9.2)

    def timeline(self):
        head = heading(r"A takeover request, \ in four steps")
        steps = [
            (r"early", r"a planned end of automation: \ an advisory at 40 s, \ shown and spoken, \ with the reason",
             GOOD),
            (r"request", r"at about 10 s: \ a sound, \ a seat vibration and a display, \ three channels for Wickens's "
                         r"pools", MODEL),
            (r"check", r"driver monitoring confirms eyes on the road and hands on the wheel before handing over",
             PERSON),
            (r"fallback", r"no response: \ the car slows and stops in the safest lane it can reach, \ hazard lights on",
             AUTH),
        ]
        line = Line([-6.0, 1.2, 0], [6.0, 1.2, 0], color=GREY_B, stroke_width=3)
        ticks, boxes = VGroup(), VGroup()
        xs = np.linspace(-4.6, 4.6, 4)
        for x, (name, what, col) in zip(xs, steps):
            ticks.add(Dot([x, 1.2, 0], radius=0.12, color=col))
            boxes.add(VGroup(word_chip(name, col, 21, width=2.4), wrapped_label(what, 2.8, 17, WHITE))
                      .arrange(DOWN, buff=0.2).next_to([x, 1.2, 0], DOWN, buff=0.35))
        foot = wrapped_label(r"each step is a hypothesis about a person, \ tested in the simulator against the target, "
                             r"\ and again on the road", 12.0, 20, YOU).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A takeover request, in four steps. <bookmark mark='a'/> Early: for a planned end of automation, an "
            "advisory at forty seconds, shown and spoken, with the reason. <bookmark mark='b'/> The request, at about "
            "ten seconds: a sound, a seat vibration and a display. Three channels, one for each of Wickens's pools. "
            "<bookmark mark='c'/> A check: driver monitoring confirms eyes on the road and hands on the wheel before "
            "the car hands over. <bookmark mark='d'/> And a fallback. If there's no response, the car slows and stops "
            "in the safest lane it can reach, with the hazard lights on. <bookmark mark='e'/> Each step is a "
            "hypothesis about a person, tested in the simulator against the target, and again on the road."
        ) as vo:
            self.play(FadeIn(head), Create(line))
            for m, t, b in zip("abcd", ticks, boxes):
                vo.wait_until(m)
                self.play(FadeIn(t, scale=1.4), FadeIn(b, shift=DOWN * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def case(self):
        rows_section(self, r"The human-factors section of a safety case", [
            (r"the tasks: \ what the person must perceive, \ decide and do, \ and in how long", WHITE),
            (r"the hazards: \ for each step, \ the slips, \ lapses and mistakes that could happen there", MODEL),
            (r"the evidence: \ user tests and simulator studies, \ with their samples, \ criteria and failures", PERSON),
            (r"the residual risk: \ what remains, \ and why it is acceptable, \ in numbers where possible", AUTH),
            (r"and a plan to learn from the field: \ incident reports read for design, \ not for blame", GOOD),
        ], "All of this goes into a safety case. <bookmark mark='a'/> Its human-factors section lists the tasks: what "
           "the person must perceive, decide and do, and in how long. <bookmark mark='b'/> The hazards: for each step, "
           "the slips, lapses and mistakes that could happen there. <bookmark mark='c'/> The evidence: user tests and "
           "simulator studies, with their samples, criteria and failures. <bookmark mark='d'/> The residual risk: what "
           "remains, and why it's acceptable, in numbers where possible. <bookmark mark='e'/> And a plan to learn from "
           "the field, reading incident reports for design, not for blame.")
