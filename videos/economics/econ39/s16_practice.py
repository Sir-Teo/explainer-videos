from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ pay audits and workforce plans", r"Who does this for a living?",
             "Chapter fourteen. In practice: pay audits and workforce plans.", lit={1983: r"Leontief"},
             scale=("firm", "nation"), horizon=("a year", "a decade"))
        self.jobs()
        self.audit()
        self.called()

    def jobs(self):
        rows = VGroup(
            label(r"the people who do this", font_size=27, color=E.ACCENT),
            label(r"pay-equity analysts: \ regressions of pay on role, \ level and tenure, \ group by group",
                  font_size=21, color=WOMEN),
            label(r"workforce planners: \ which tasks will machines take, \ and whom to retrain", font_size=21,
                  color=MIDS),
            label(r"compensation teams: \ pay bands from market surveys", font_size=21, color=FIRM),
            label(r"labour economists in government: \ discrimination cases, \ statistics, \ policy", font_size=21,
                  color=WORKER),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        with self.voiceover(
            "Who uses this? <bookmark mark='a'/> Pay-equity analysts, inside firms and for regulators, run the "
            "regressions of chapter eleven on a firm's own payroll, comparing like with like. "
            "<bookmark mark='b'/> Workforce planners ask which tasks machines will take and whom to retrain. "
            "<bookmark mark='c'/> Compensation teams set pay bands from market surveys. <bookmark mark='d'/> And "
            "labour economists in government bring discrimination cases, run the earnings statistics this part "
            "used, and advise on policy."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def audit(self):
        O = load("oaxaca")
        g = O["85"]
        steps = flow_chain([(r"the payroll", GREY_B), (r"compare like \\ with like", WORKER),
                            (r"the gap that \\ remains", WOMEN), (r"explain it \\ or fix it", GAIN)],
                           notes=[r"pay, \ role, \ level, \\ tenure, \ location", r"a regression \\ within each "
                                  r"job family", r"Oaxaca-Blinder: \\ `unexplained'", r"and ask what the \\ controls "
                                  r"hide"], box_w=2.7, font_size=20, note_size=15).move_to(UP * 0.9)
        warn = label(r"the trap: \ controlling for level and role \ can hide discrimination in who gets promoted",
                     font_size=20, color=E.ACCENT).to_edge(DOWN, buff=1.2)
        ex = label(rf"in the 1985 CPS: \ a gap of {g['gap']:.2f}, \ almost none of it `explained'", font_size=18,
                   color=GREY_A).next_to(warn, DOWN, buff=0.25)
        with self.voiceover(
            "A pay audit is the decomposition of chapter eleven, done on one employer. <bookmark mark='a'/> Take the "
            "payroll; <bookmark mark='b'/> compare people in the same job family, level and location; "
            "<bookmark mark='c'/> measure what gap remains; <bookmark mark='d'/> and either explain it or fix it. "
            "<bookmark mark='e'/> The trap is the same as before: if women are promoted more slowly, controlling for "
            "level hides exactly the discrimination the audit is meant to find."
        ) as vo:
            self.play(FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(steps.arrows[0]), FadeIn(steps.boxes[1]), FadeIn(steps.notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(steps.arrows[1]), FadeIn(steps.boxes[2]), FadeIn(steps.notes[2]))
            vo.wait_until("d")
            self.play(GrowArrow(steps.arrows[2]), FadeIn(steps.boxes[3]), FadeIn(steps.notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(warn), FadeIn(ex))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["leontief_1983"]
        L = load("leontief")
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=21)
        foot = label(rf"prime-age employment: \ {L['epop1983']:.1f}\% in 1983, \ {L['epop2025']:.1f}\% in 2025; \ "
                     rf"the labour share: \ down {100 * (1 - L['ls2025'] / L['ls1983']):.0f}\%", font_size=18,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(tables.LEONTIEF_1983.tag + r"; \ BLS via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1983 Wassily Leontief, who won the Nobel prize for input-output "
            "analysis, told a symposium that the role of humans as the most important factor of production was bound "
            "to diminish, as the role of horses in farming had been diminished and then eliminated by tractors. "
            "<bookmark mark='b'/> Forty years on, a larger share of Americans in their prime work than in 1983: "
            f"{L['epop1983']:.1f} percent then, {L['epop2025']:.1f} percent in 2025. But labour's share of business "
            f"income has fallen by about {100 * (1 - L['ls2025'] / L['ls1983']):.0f} percent, and the middle of the "
            "wage distribution has hollowed out. <bookmark mark='c'/> The verdict: too early to say. Horses, unlike "
            "people, could not move to new tasks; whether people always can is exactly what artificial intelligence "
            "will test."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01), FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
