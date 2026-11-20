from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ actuaries and evaluators", r"Who keeps the promises, and who checks them?",
             "Chapter fifteen. In practice: actuaries and evaluators.", lit={1983: r"the Social Security Amendments"},
             scale=("nation",), horizon=("a decade", "a century"))
        self.who()
        self.arithmetic()
        self.called()

    def who(self):
        rows = VGroup(
            label(r"actuaries: \ project a programme's income and costs for 75 years \ (Social Security's Office "
                  r"of the Chief Actuary)", font_size=20, color=PENSION),
            label(r"budget offices: \ score proposals \ (the Congressional Budget Office)", font_size=20,
                  color=UNEMP),
            label(r"state agencies: \ run unemployment insurance, \ set employers' tax rates by their record of "
                  r"layoffs", font_size=20, color=WORK),
            label(r"evaluators: \ test programmes before they spread, \ as Oregon and RAND did", font_size=20,
                  color=HEALTH),
            label(r"insurers' actuaries: \ price private cover alongside the state's", font_size=20, color=RISK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to(DOWN * 0.1)
        head = label(r"the people who do this", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Who does this for a living? <bookmark mark='a'/> Actuaries project a programme's income and costs far "
            "ahead; Social Security's Office of the Chief Actuary looks seventy-five years out, every year. "
            "<bookmark mark='b'/> Budget offices, like the Congressional Budget Office, score proposals to change "
            "benefits. <bookmark mark='c'/> State agencies run unemployment insurance, and set each employer's tax "
            "by its record of layoffs, so that firms that lay off more pay more. <bookmark mark='d'/> Evaluators, "
            "in government and universities, test programmes before they spread, as RAND and Oregon did. "
            "<bookmark mark='e'/> And insurers' actuaries price the private cover that sits alongside the state's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def arithmetic(self):
        P = load("pensions")
        rep = P["rows"][str(P["r2024"])]["replacement"]
        need = 100 * rep / P["r2035"]
        cut = P["rows"][str(P["r2035"])]["replacement"]
        opts = [(r"today: \ 2.7 workers per beneficiary", rf"{P['payroll']}\% tax pays {100 * rep:.0f}\% of the "
                                                          r"average wage", GREY_B),
                (r"2035, \ keep the benefit", rf"the tax must rise to {need:.1f}\%", LOSS),
                (r"2035, \ keep the tax", rf"the benefit falls to {100 * cut:.0f}\% of the wage", UNEMP),
                (r"or both, \ or more workers", r"a later retirement age, \ more immigrants, \ higher employment",
                 GAIN)]
        tbl = VGroup(*[VGroup(label(a, font_size=21, color=WHITE), label(b, font_size=21, color=c)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1) for a, b, c in opts]).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        tbl.move_to(DOWN * 0.1)
        head = label(r"an actuary's arithmetic", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.PENSIONS.tag + r"; \ computed", corner=DR, font_size=11)
        with self.voiceover(
            "Here is the kind of arithmetic an actuary does, with chapter eight's identity. "
            f"<bookmark mark='a'/> Today, with {P['r2024']:g} workers per beneficiary, a {P['payroll']} percent "
            f"payroll tax pays {say_pct(rep, 0)} of the average wage. <bookmark mark='b'/> If there are "
            f"{P['r2035']:g} workers per beneficiary in 2035 and the benefit is to stay the same, the tax must rise "
            f"to {need:.1f} percent. <bookmark mark='c'/> If the tax is to stay the same, the benefit falls to "
            f"{say_pct(cut, 0)} of the wage. <bookmark mark='d'/> Or some of each, or more workers: a later "
            "retirement age, more immigrants, higher employment. The arithmetic does not choose; it only says that "
            "something must give."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tbl[0]))
            for mk, r_ in zip("bcd", tbl[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["ss_1983"]
        S = tables.SS_1983.data
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=21)
        foot = label(rf"75 years from 1983: \ 2058; \ the trust funds' projected end: \ {S['now']}", font_size=19,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(tables.SS_1983.tag + r"; \ SSA (2025)", corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1983, with the trust funds months from running short, Congress "
            "raised payroll taxes sooner, taxed some benefits and raised the retirement age in steps. The reform "
            "was expected to keep Social Security solvent for seventy-five years, with surpluses in the early years "
            "paying for deficits later. <bookmark mark='b'/> Seventy-five years from 1983 is 2058. The trustees and "
            f"the Congressional Budget Office now expect the trust funds to run out in {S['now']}, about a quarter "
            "of a century early. The actuaries had expected annual deficits to begin around 2025; the economy and "
            "the population turned out differently from their assumptions. <bookmark mark='c'/> The verdict: "
            "wrong. Seventy-five-year promises depend on numbers no one can know so far ahead, which is why the "
            "actuaries re-run them every year."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01), FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
