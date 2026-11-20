from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ financial stability", r"Who watches the system for a living?",
             "Chapter fifteen. In practice: financial stability.", lit={2005: r"Rajan at Jackson Hole"},
             scale=("market", "nation"), horizon=("a quarter", "a year"))
        self.jobs()
        self.called()

    def jobs(self):
        rows = VGroup(
            label(r"the people who do this", font_size=27, color=E.ACCENT),
            label(r"financial-stability departments: \ credit gaps, \ house prices, \ leverage, \ funding; \ a "
                  r"report twice a year", font_size=21, color=BANK),
            label(r"supervisors' stress tests: \ every large bank, \ every year, \ against a severe scenario \ "
                  r"(Part 26)", font_size=21, color=RATE),
            label(r"risk managers in banks and funds: \ value at risk, \ margins, \ liquidity \ (\emph{Quant, \ "
                  r"Built}, \ Parts 40--41)", font_size=21, color=CREDIT),
            label(r"the tools: \ this part's: \ leverage, \ collateral, \ credit booms, \ and how they feed back",
                  font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"\emph{Quant, \ Built}, \ Parts 40--41: \ risk", corner=DR, font_size=12)
        with self.voiceover(
            "Who does this for a living? <bookmark mark='a'/> Most central banks now have a financial stability "
            "department, which tracks credit gaps, house prices, leverage and how banks fund themselves, and "
            "publishes a report on the risks once or twice a year. <bookmark mark='b'/> Supervisors run stress "
            "tests of every large bank against a severe scenario every year, the descendants of the tests of May "
            "2009. <bookmark mark='c'/> Inside banks and funds, risk managers measure what a portfolio could lose, "
            "set margins and watch liquidity; the series Quant, Built treats their tools in Parts forty and "
            "forty-one. <bookmark mark='d'/> All of them use this part's ideas: leverage, collateral, booms, and "
            "the loops that join them."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["rajan_2005"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=18).move_to(UP * 0.3)
        tag = published_tag(r"Rajan, \ Jackson Hole symposium (2005), \ NBER WP 11728", corner=DR, font_size=12)
        foot = label(r"the call was about incentives and liquidity, \ not housing or a date: \ the right kind of "
                     r"warning, \ and the hard kind to act on", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In August 2005, at the Kansas City Fed's symposium in Jackson Hole, a "
            "gathering in honour of Alan Greenspan, Raghuram Rajan, then the IMF's chief economist, presented a "
            "paper asking whether financial development had made the world riskier. His answer was yes. Managers "
            "paid for beating their peers are drawn to take risks that rarely show, and to herd; in a boom these "
            "behaviours reinforce each other, creating, in his words, a greater, albeit still small, probability "
            "of a catastrophic meltdown. Many in the room thought him wrong. <bookmark mark='b'/> Three years later "
            "the system came close to the meltdown he described: the rare risks came due together, and the markets "
            "everyone relied on to sell in froze. <bookmark mark='c'/> The verdict: right. <bookmark mark='d'/> But "
            "notice what kind of call it was: about incentives and liquidity, with no date and no mention of "
            "housing. The right kind of warning, and the hard kind to act on."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
