from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403


class Rebates(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The rebate experiments", r"What did households do with cheques whose timing was random?",
             "Chapter seven. The rebate experiments.", lit={2001: r"rebates", 2008: r"payments", 2020: r"EIPs",
                                                             2003: r"Hsieh", 2018: r"Kueng"},
             scale=("household", "nation"), horizon=("a quarter",))
        self.design()
        self.results()
        self.alaska()
        self.call()

    def design(self):
        sc = study_card(r"Household Expenditure and the Income Tax Rebates of 2001", r"David Johnson, \ Jonathan "
                        r"Parker \ and Nicholas Souleles, \ American Economic Review, \ 2006", [
                            (r"what varied", r"the three months in which the cheque arrived, \ set by the "
                                             r"second-to-last digit of the Social Security number"),
                            (r"the data", r"the Consumer Expenditure Survey: \ households interviewed every three "
                                          r"months, \ with special questions about the rebate"),
                            (r"the comparison", r"the change in spending of households whose cheque came in a given "
                                                r"three months, \ against households whose cheque had not yet come"),
                            (r"why it works", r"the timing is random, \ so early and late households are alike in "
                                              r"everything else"),
                        ], design="RCT", width=12.4, font_size=22).move_to(UP * 0.1)
        with self.voiceover(
            "Back to the cheques. <bookmark mark='a'/> The government's own survey of household spending, the "
            "Consumer Expenditure Survey, interviews each household every three months. In 2001 it added questions "
            "about the rebate: whether it came, and when. <bookmark mark='b'/> Johnson, Parker and Souleles compared "
            "the change in spending of households whose cheque arrived in a given three months with the change for "
            "households whose cheque had not yet come. <bookmark mark='c'/> Because the timing was set by a digit, "
            "the early and the late households are alike in everything else: their incomes, their jobs, the shock "
            "of September the eleventh. Any difference in spending is the cheque."
        ) as vo:
            self.play(FadeIn(sc.card), FadeIn(sc[1][0]), FadeIn(sc[2]))
            vo.wait_until("a")
            self.play(FadeIn(sc.body[0]), FadeIn(sc.body[1]))
            vo.wait_until("b")
            self.play(FadeIn(sc.body[2]))
            vo.wait_until("c")
            self.play(FadeIn(sc.body[3]))
        self.clear_scene()

    def results(self):
        j = tables.MPC_STUDIES.data
        rows = VGroup(
            label(r"what they found", font_size=28, color=E.ACCENT),
            label(r"2001: \ 20 to 40\% on nondurables in the three months of arrival; \ about two-thirds by the end "
                  r"of the next three", font_size=22, color=SAVE),
            label(r"the response was largest for households with little liquid wealth or low income", font_size=22,
                  color=CASH),
            label(r"2008: \ 12 to 30\% on nondurables; \ 50 to 90\% counting durables, \ mostly vehicles", font_size=22,
                  color=SPEND),
            label(rf"2020: \ about {100 * j['parker2022']['value']:.0f}\% on nondurables and services \ (s.e. "
                  rf"{100 * j['parker2022']['se']:.1f}); \ {100 * j['parker2022']['low_liquid']:.0f}\% for households "
                  r"with little liquid wealth", font_size=22, color=HOUSE),
            label(r"households with cash in hand, \ or few places open to spend it, \ spent less", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Johnson, Parker and Souleles (2006); \ Parker, Souleles, Johnson and McClelland, AER "
                            r"103(6) (2013); \ Parker, Schild, Erhard and Johnson, NBER WP 29648 (2022)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "What they found. <bookmark mark='a'/> In 2001, households spent twenty to forty percent of the rebate "
            "on nondurables in the three months it arrived, and about two-thirds of it by the end of the following "
            "three months. <bookmark mark='b'/> The response was largest for households with little liquid wealth, "
            "or low income: just where the buffer-stock line was steep. <bookmark mark='c'/> In 2008 the economic "
            "stimulus payments were again timed by Social Security numbers. On nondurables, twelve to thirty "
            "percent; counting durable goods, mostly vehicles, fifty to ninety. <bookmark mark='d'/> In 2020 the "
            "economic impact payments of the pandemic were larger, and the response smaller: about ten percent on "
            "nondurables and services in the three months of arrival, though about twenty-two percent for "
            "households with little liquid wealth. <bookmark mark='e'/> Many households had cash in hand, and "
            "there were fewer places open to spend it. The propensity to spend is not a constant of nature. It "
            "depends on who gets the money, and when."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def alaska(self):
        rows = VGroup(
            label(r"a cheque that comes every year: \ Alaska's Permanent Fund dividend", font_size=27, color=E.ACCENT),
            label(r"paid to every resident each autumn from the state's oil fund; \ large, \ regular, \ announced "
                  r"months ahead", font_size=22, color=GREY_A),
            label(r"Chang-Tai Hsieh, \ 2003, \ survey data: \ no response to the dividend; \ the same households "
                  r"did respond to tax refunds", font_size=22, color=SPEND),
            label(r"Lorenz Kueng, \ 2018, \ account data: \ about 25\% spent on nondurables and services within a "
                  r"quarter", font_size=22, color=SAVE),
            label(r"and above 50\% for high-income households with plenty of liquid assets", font_size=22, color=SAVE),
            label(r"for a payment small next to a large income, \ not smoothing it costs almost nothing", font_size=22,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Hsieh, AER 93(1) (2003): \ 397--405; \ Kueng, QJE 133(4) (2018): \ 1693--1751",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Is the rebate special? <bookmark mark='a'/> Alaska pays every resident a dividend each autumn from the "
            "state's oil fund. It is large, it comes every year, and its size is announced months ahead: the "
            "anticipated income change Hall's theory says should not matter. <bookmark mark='b'/> In 2003 "
            "Chang-Tai Hsieh found, in survey data, no response of spending to the dividend, though the same "
            "households did respond to their income-tax refunds. Large, regular, well-known payments seemed to be "
            "smoothed. <bookmark mark='c'/> Then in 2018 Lorenz Kueng looked at account data from a personal-finance "
            "app, which records spending far more accurately than a survey. About twenty-five percent of the "
            "dividend went on nondurables and services within a quarter. <bookmark mark='d'/> And the response "
            "rose with income: above half for high-income households with plenty of liquid assets, who could easily "
            "have smoothed. <bookmark mark='e'/> His reading: for a payment that is small next to a large income, "
            "not bothering to smooth it costs almost nothing. Behaviour that breaks the theory can be nearly "
            "rational."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def call(self):
        c = calls.CALLS["hall_random_walk"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=20).move_to(UP * 0.1)
        tag = published_tag(r"Hall (1978); \ Johnson, Parker and Souleles (2006); \ Hsieh (2003); \ Kueng (2018)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> Hall's prediction, in 1978: nothing known today, anticipated changes in "
            "income included, should predict how consumption changes next. <bookmark mark='b'/> Randomly timed, "
            "announced payments in 2001 and 2008 raised spending in the quarter they arrived, most for households "
            "short of cash. Alaska's dividend showed no response in survey data, but a clear one in account data. "
            "<bookmark mark='c'/> Partly right. The theory describes households with cash to spare and a reason to "
            "care, and many households are not like that."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
