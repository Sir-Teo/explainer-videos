from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ capital budgeting, \ valuation, \ pensions", r"Where do these formulas decide "
             r"real money?", "Chapter fourteen. In practice: capital budgeting, valuation, pensions.",
             lit={2011: r"Novy-Marx and Rauh"}, scale=("firm", "nation"), horizon=("years", "decades"))
        self.budgeting()
        self.pensions()
        self.who()

    def budgeting(self):
        rows = VGroup(
            label(r"capital budgeting: \ the net present value rule", font_size=27, color=E.ACCENT),
            MathTex(r"\text{NPV} = -I + \sum_t \frac{\mathbb{E}[\text{cash}_t]}{(1 + r_{\text{project}})^t}",
                    font_size=42, color=FIRM),
            label(r"discount at the project's own risk, \ not the firm's average: \ Modigliani--Miller's lesson",
                  font_size=22, color=GREY_A),
            label(r"plus the option to wait \ (chapter 3): \ a positive NPV is necessary, \ not sufficient", font_size=22,
                  color=FIRM),
            label(r"valuation: \ forecast cash for some years, \ then a Gordon formula for the rest", font_size=22,
                  color=STOCK),
            label(r"the terminal value is often most of the answer, \ and one point on $r$ moves it by a fifth",
                  font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "Where do these formulas decide real money? <bookmark mark='a'/> In every firm's capital budget. A "
            "project is worth building if the present value of its expected cash exceeds its cost. "
            "<bookmark mark='b'/> The discount rate should match the project's own risk, its covariance with bad "
            "times, not the firm's average: that is Modigliani and Miller's lesson applied. "
            "<bookmark mark='c'/> And the option to wait means a positive net present value is necessary, not "
            "sufficient. <bookmark mark='d'/> In valuing a company, analysts forecast cash for a few years and then "
            "put a Gordon formula on everything after. <bookmark mark='e'/> That terminal value is often most of the "
            "answer, and as chapter one showed, one point on the discount rate moves it by a fifth."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def pensions(self):
        rows = VGroup(
            label(r"pension promises: \ what rate should discount them?", font_size=27, color=E.ACCENT),
            label(r"American public plans discounted promised pensions at the return they expected on their assets, \ "
                  r"around 8\%", font_size=22, color=GREY_A),
            label(r"but the promises are close to riskless for the retirees: \ the discount factor says use a "
                  r"near-riskless rate", font_size=22, color=BILL),
            label(r"Robert Novy-Marx and Joshua Rauh, \ 2011: \ at Treasury rates, \ the fifty states' main plans "
                  r"were \\ about \$3 trillion short", font_size=22, color=HOLD),
            label(r"the rate chosen moved the measured gap by trillions: \ asset pricing is pension policy",
                  font_size=23, color=WHITE),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Novy-Marx and Rauh, JF 66(4) (2011): \ 1211--1249, \ and their later summaries",
                            corner=DR, font_size=12)
        with self.voiceover(
            "And in pensions. <bookmark mark='a'/> American state pension funds long discounted the pensions they "
            "had promised at the return they expected to earn on their investments, around eight percent. "
            "<bookmark mark='b'/> But the promises are close to riskless for the people who will receive them, so "
            "the discount factor says to discount them at a near-riskless rate, whatever the fund holds. "
            "<bookmark mark='c'/> Robert Novy-Marx and Joshua Rauh did that calculation: at Treasury rates, the "
            "fifty states' main plans were about three trillion dollars short. <bookmark mark='d'/> The rate chosen "
            "moved the measured gap by trillions. Asset pricing is pension policy."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def who(self):
        cards = point_cards([
            (r"corporate finance teams", r"capital budgets, \\ costs of capital", FIRM),
            (r"analysts and investors", r"valuation; \ risk premia \\ and their forecasts", STOCK),
            (r"pension funds and regulators", r"discounting promises", BILL),
            (r"central banks and treasuries", r"rates, \ house prices \\ and investment", HOUSE),
        ], width=12.4, cols=2, font_size=22).move_to(DOWN * 0.2)
        head = label(r"who uses this", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Who uses this? <bookmark mark='a'/> Corporate finance teams, setting capital budgets and costs of "
            "capital. <bookmark mark='b'/> Analysts and investors, valuing firms and estimating risk premia. "
            "<bookmark mark='c'/> Pension funds and their regulators, discounting promises. <bookmark mark='d'/> And "
            "central banks and treasuries, watching how interest rates move house prices and investment."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
