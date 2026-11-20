from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403


class IMF(VoiceoverScene):
    def construct(self):
        card(self, 9, r"The IMF and its critics", r"When a country runs out of dollars, who lends, and on what terms?",
             "Chapter nine. The IMF and its critics.", lit={1944: r"Bretton Woods", 1997: r"Asia",
                                                           2012: r"the institutional view"},
             scale=("nation", "world"), horizon=("a year",))
        self.lender()

    def lender(self):
        rows = VGroup(
            label(r"the IMF: \ a lender to countries that run short of foreign currency", font_size=25,
                  color=E.ACCENT),
            label(r"its loans come with conditions: \ budgets, \ interest rates, \ banks, \ reforms", font_size=23,
                  color=WHITE),
            label(r"1997--98, \ Thailand, \ Indonesia, \ Korea: \ high interest rates, \ tighter budgets, \ bank "
                  r"closures", font_size=22, color=CRISIS),
            label(r"the critics: \ austerity in a collapse, \ and rules written for the wrong kind of crisis",
                  font_size=22, color=GREY_A),
            label(r"its own evaluators, \ 2003: \ Korea's fiscal tightening was unnecessary in hindsight; \ the "
                  r"balance-sheet effects were underestimated", font_size=21, color=DEM),
            label(r"since 2012: \ controls on capital flows accepted as a tool, \ in some circumstances", font_size=22,
                  color=CALM),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"IMF Independent Evaluation Office, \ \emph{The IMF and Recent Capital Account Crises} "
                            r"(2003); \ Stiglitz (2002)", corner=DR, font_size=12)
        with self.voiceover(
            "When a country runs out of foreign currency, the lender of last resort is the International Monetary "
            "Fund, set up at Bretton Woods in 1944. <bookmark mark='a'/> Its loans come with conditions: on budgets, "
            "interest rates, banks and reforms, meant to restore confidence and ensure it is repaid. "
            "<bookmark mark='b'/> In Asia in 1997 and 1998 it asked Thailand, Indonesia and Korea for high interest "
            "rates to stop their currencies falling, tighter budgets, and the closure of weak banks. "
            "<bookmark mark='c'/> Critics, Joseph Stiglitz most prominently, argued that this was austerity in the "
            "middle of a collapse, applying the medicine for a first-generation crisis to a third-generation one, "
            "and that closing banks in a panic spread it. <bookmark mark='d'/> The Fund's own Independent Evaluation "
            "Office, in 2003, concluded that Korea's fiscal tightening had been unnecessary in hindsight, and that "
            "the damage from firms' and banks' dollar debts had been underestimated. <bookmark mark='e'/> Since 2012 "
            "the Fund has accepted that controls on capital flows can be a legitimate tool in some circumstances, a "
            "change that would have surprised it in 1997."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
