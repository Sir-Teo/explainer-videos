from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ stimulus and pensions", r"How do governments use what is known about "
             r"spending, \ and who measures it?", "Chapter fourteen. In practice: stimulus and pensions.",
             lit={2001: r"Madrian and Shea", 2012: r"Sahm, Shapiro, Slemrod"}, scale=("household", "nation"),
             horizon=("a quarter", "a lifetime"))
        self.stimulus()
        self.pensions()
        self.who()

    def stimulus(self):
        rows = VGroup(
            label(r"designing a stimulus payment", font_size=28, color=E.ACCENT),
            label(r"1. \ aim at households short of cash: \ they spend it; \ others mostly save it", font_size=23,
                  color=CASH),
            label(r"2. \ speed: \ in 2020 the payments went straight to bank accounts the tax authority already "
                  r"held", font_size=23, color=SPEND),
            label(r"3. \ the form matters: \ a cheque in the mail, \ or a little more in each paycheque?", font_size=23,
                  color=SAVE),
            label(r"\quad Sahm, \ Shapiro and Slemrod: \ 25\% said they would mostly spend 2008's one-time payment; "
                  r"\ 13\% said so of 2009's lower withholding", font_size=20, color=GREY_A),
            label(r"4. \ the evidence in this part is the toolkit: \ randomized timing, \ account data, \ surveys",
                  font_size=23, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Sahm, Shapiro and Slemrod, AEJ: Economic Policy 4(3) (2012): \ 216--250", corner=DR,
                            font_size=12)
        with self.voiceover(
            "What do governments do with all this? Start with stimulus. <bookmark mark='a'/> First, aim the money at "
            "households short of cash. They spend it; households with a cushion mostly save it. "
            "<bookmark mark='b'/> Second, speed. In 2020 the first payments went straight into the bank accounts "
            "the tax authority already had on file, within weeks. <bookmark mark='c'/> Third, the form. In 2008 "
            "Americans got one-time payments; in 2009 most workers got a tax credit as slightly lower withholding "
            "in every paycheque. <bookmark mark='d'/> Claudia Sahm, Matthew Shapiro and Joel Slemrod asked "
            "households in the Michigan survey what they did. Twenty-five percent said they would mostly spend the "
            "2008 payment; thirteen percent said so of the 2009 paycheque increase. The same money, delivered "
            "differently, about half the response. <bookmark mark='e'/> And the tools for knowing all this are the "
            "ones in this part: random timing, account data, careful surveys."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def pensions(self):
        ms = tables.MADRIAN_SHEA_2001.data
        part = list(ms["participation"].values())
        ax = plane([0.4, 2.6], [0, 1.0], center=LEFT * 3.0 + DOWN * 0.5, x_length=5.0, y_length=4.4,
                   xticks=[], yticks=[0, 0.25, 0.5, 0.75, 1.0], ylabel=r"share of new hires in the plan",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16)
        bars = VGroup()
        for k, (name, v, col) in enumerate(((r"before: \\ opt in", part[1], GREY_B), (r"after: \\ opt out", part[0],
                                                                                         PENSION))):
            x = k + 1
            b = Rectangle(width=ax.ax.c2p(x + 0.3, 0)[0] - ax.ax.c2p(x - 0.3, 0)[0],
                          height=ax.ax.c2p(0, v)[1] - ax.ax.c2p(0, 0)[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to(ax.ax.c2p(x, 0), aligned_edge=DOWN)
            nm = label(name, font_size=17, color=col).next_to(ax.ax.c2p(x, 0), DOWN, buff=0.15)
            val = label(f"{100 * v:.0f}\\%", font_size=22, color=col).next_to(b, UP, buff=0.08)
            bars.add(VGroup(b, nm, val))
        side = VGroup(
            label(r"saving for retirement", font_size=26, color=E.ACCENT),
            label(r"pay-as-you-go: \ today's workers pay today's retirees \\ (chapter 11)", font_size=20,
                  color=PENSION),
            label(r"funded: \ each generation saves for itself", font_size=20, color=SAVE),
            label(r"a default works where theory says it should not: \\ Madrian and Shea, \ 1998's switch to "
                  r"automatic \\ enrolment in a US firm's 401(k)", font_size=20, color=GREY_A),
            label(rf"{100 * ms['at_default']:.0f}\% of those enrolled kept the default \\ contribution rate "
                  rf"({100 * ms['default_rate']:.0f}\%)", font_size=20, color=GREY_A),
            label(r"the United Kingdom made it national \\ in 2012: \ Part 42", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = published_tag(tables.MADRIAN_SHEA_2001.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Then pensions. <bookmark mark='a'/> A pay-as-you-go system, chapter eleven's, has today's workers pay "
            "today's retirees. <bookmark mark='b'/> A funded one has each generation save for itself. "
            "<bookmark mark='c'/> Either way, a life-cycle household should save the right amount whatever form the "
            "paperwork takes. It does not. Brigitte Madrian and Dennis Shea studied an American firm that, in 1998, "
            "switched its retirement plan from opt in to opt out. <bookmark mark='d'/> Among new hires, "
            f"participation went from {100 * part[1]:.0f} percent to {100 * part[0]:.0f}. "
            f"<bookmark mark='e'/> And {100 * ms['at_default']:.0f} percent of those enrolled automatically kept "
            f"the default contribution rate of {100 * ms['default_rate']:.0f} percent, low as it was. "
            "<bookmark mark='f'/> Defaults are policy. The United Kingdom made automatic enrolment national from "
            "2012; Part forty-two takes up pensions in full."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(*[GrowFromEdge(b[0], DOWN) for b in bars], *[FadeIn(b[1:]) for b in bars])
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def who(self):
        cards = point_cards([
            (r"treasuries and finance ministries", r"stimulus design; \\ scoring tax changes", SAVE),
            (r"central banks", r"how spending responds \\ to rates and income", INCOME),
            (r"pension funds and regulators", r"defaults, \ contribution \\ rates, \ annuities", PENSION),
            (r"banks and fintech", r"account data: \ spending \\ seen day by day", CASH),
        ], width=12.4, cols=2, font_size=22).move_to(DOWN * 0.2)
        head = label(r"who uses this", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Who uses this? <bookmark mark='a'/> Treasuries and finance ministries, to design stimulus and to "
            "estimate what a tax change will do. <bookmark mark='b'/> Central banks, whose models need to know how "
            "spending responds to interest rates and income. <bookmark mark='c'/> Pension funds and their "
            "regulators, who choose defaults and contribution rates. <bookmark mark='d'/> And banks and financial "
            "technology firms, whose account data now let researchers see spending day by day, as Kueng's did, and "
            "as the frontier does."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
