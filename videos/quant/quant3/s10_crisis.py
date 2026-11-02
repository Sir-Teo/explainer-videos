from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import CASH, PART

IS_C = QC.IDEA


class Crisis(VoiceoverScene):
    def construct(self):
        self.card()
        self.enron()
        self.wirecard()
        self.lessons()

    def card(self):
        c = chapter_card(9, r"When the statements lie", r"What do you do when the numbers are false?",
                         lit=(2001, 2020), part=PART)
        with self.voiceover("Chapter nine. When the statements lie."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def enron(self):
        card = crisis_card(r"8 November -- 2 December 2001", r"Enron",
                           r"America's seventh-largest company by revenue restated four years of earnings, then filed "
                           r"for what was then the largest bankruptcy in US history. Its auditor, Arthur Andersen, "
                           r"collapsed with it.",
                           stats=[(r"\$586\text{m}", r"earnings removed, 1997--2000, by the restatement"),
                                  (r"> \$5\text{bn}", r"loans booked as operating cash flow through ``prepays'', "
                                                      r"1997--2001 (SEC)")],
                           width=7.0)
        how = VGroup(
            label(r"how the statements were bent", font_size=24, color=GREY_A),
            wrapped_label(r"profits booked up front: long-term contracts marked to Enron's own models", 5.0, 21,
                          IS_C),
            wrapped_label(r"debt kept off the balance sheet in partnerships run by its own finance chief", 5.0, 21,
                          QC.CASH),
            wrapped_label(r"loans dressed as commodity trades, so borrowed cash appeared as cash from operations", 5.0,
                          21, CASH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(card, how).arrange(RIGHT, buff=0.6, aligned_edge=UP).scale_to_fit_width(13.2).move_to(ORIGIN)
        with self.voiceover(
            "On the eighth of November 2001, Enron, an energy trader that was then America's seventh-largest "
            "company by revenue, restated its earnings for the previous four years, removing five hundred and "
            "eighty-six million dollars. On the second of December it filed for bankruptcy, the largest in American "
            "history to that day, and its auditor, Arthur Andersen, did not survive the scandal. "
            "<bookmark mark='a'/> Its statements had been bent in all three ledgers. Profits on long-term contracts "
            "were booked up front, at values from Enron's own models. Debt was kept off the balance sheet in "
            "partnerships run by its own chief financial officer. <bookmark mark='b'/> And, according to the SEC, "
            "more than five billion dollars of loans were dressed up as commodity trades called prepays, so that "
            "borrowed money appeared as cash from operations. Sloan's accrual signal compares earnings with "
            "operating cash; Enron had faked the cash too."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(how[0]), FadeIn(how[1]), FadeIn(how[2]))
            vo.wait_until("b")
            self.play(FadeIn(how[3]))
        self.wait(0.4)
        self.clear_scene()

    def wirecard(self):
        card = crisis_card(r"18 -- 25 June 2020", r"Wirecard",
                           r"A German payments company in the DAX told investors that cash held for it in trust "
                           r"accounts at two Philippine banks could not be confirmed; a week later it filed for "
                           r"insolvency. Its chief executive resigned and was arrested.",
                           stats=[(r"\text{EUR\,}1.9\text{bn}", r"cash that most likely did not exist"),
                                  (r"\approx 1/4", r"of its balance sheet")],
                           width=7.0)
        story = VGroup(
            label(r"the warnings were public", font_size=24, color=GREY_A),
            wrapped_label(r"2015--2019: the Financial Times reported irregularities, later from whistle-blowers in "
                          r"its Asian offices", 5.0, 21, GREY_A),
            wrapped_label(r"February 2019: the German regulator BaFin banned new short positions in Wirecard for two "
                          r"months, and filed a criminal complaint against FT journalists", 5.0, 21, QC.LOSS),
            wrapped_label(r"June 2020: the auditor, EY, refused to sign the 2019 accounts", 5.0, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(card, story).arrange(RIGHT, buff=0.6, aligned_edge=UP).scale_to_fit_width(13.2).move_to(ORIGIN)
        with self.voiceover(
            "Nineteen years later the same story was told with cash itself. Wirecard was a German payments company in "
            "the DAX, the country's index of its largest firms. In June 2020 its auditor, EY, could not confirm one "
            "point nine billion euros held for it in trust accounts at two banks in the Philippines, about a quarter "
            "of its balance sheet. The banks said the documents were not theirs. Within a week the chief executive "
            "had resigned and been arrested, and the company had filed for insolvency. <bookmark mark='a'/> The "
            "warnings had been public for years. The Financial Times had reported irregularities since 2015. In "
            "February 2019 the German regulator responded, not by investigating the company, but by banning new "
            "short positions in its shares and filing a criminal complaint against the reporters. Short sellers, "
            "who had been right, were treated as the threat."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in story], lag_ratio=0.5, run_time=5))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        rows = VGroup(*[label(t, font_size=26, color=c) for t, c in [
            (r"a statement is a model of a firm, built by the firm; its inputs can be chosen", GREY_A),
            (r"check the identities: earnings against cash, cash against interest earned on it", IS_C),
            (r"read who signs: auditors, related parties, partnerships the managers own", GREY_A),
            (r"short sellers and journalists are data too, and so are regulators' reactions to them", QC.LOSS),
            (r"restatements are events: store the number as first reported, and the day it changed", QC.HOUSE),
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        title = label(r"What a quant takes from this", font_size=34).to_edge(UP, buff=0.6)
        rows.next_to(title, DOWN, buff=0.7)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "What a quant takes from this. A financial statement is a model of a firm, built by the firm, and its "
            "inputs can be chosen. The identities are the first check: earnings that never turn into cash, or a "
            "mountain of cash that earns no interest, should both be impossible. Read who signs, and who is on both "
            "sides of a deal. Treat short sellers' reports and journalists' investigations as data. And treat a "
            "restatement as an event: the House stores every number as it was first reported, and the day it "
            "changed, because a backtest that uses the corrected numbers knows what nobody knew at the time."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.6,
                                                 run_time=10))
        self.wait(0.4)
        self.clear_scene()
