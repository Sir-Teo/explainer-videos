from __future__ import annotations

from videos.economics.econ25.s12_banks import tacct
from videos.economics.econ26.common import *  # noqa: F403


class Bank(VoiceoverScene):
    def construct(self):
        card(self, 1, r"What a bank does", r"Why lend long and borrow short?", "Chapter one. What a bank does.",
             lit={1694: r"Bank of England", 1983: r"Diamond and Dybvig"}, scale=("firm",), horizon=("a day", "years"))
        self.sheet()
        self.transform()

    def sheet(self):
        S = load("sheet")
        bank = tacct(r"the Island's bank", DEPOSIT,
                     [(rf"reserves \ {S['reserves']:.0f}", CB), (rf"loans \ {S['loans']:.0f}", LOAN),
                      (rf"bonds \ {S['bonds']:.0f}", BOND)],
                     [(rf"deposits \ {S['deposits']:.0f}", DEPOSIT), (rf"equity \ {S['equity']:.0f}", EQUITY)],
                     width=5.4).move_to(UP * 1.0)
        rows = VGroup(
            label(r"its liabilities: \ deposits, \ repayable on demand, \ at par", font_size=23, color=DEPOSIT),
            label(r"its assets: \ loans and bonds that pay off over years, \ and a little cash", font_size=23,
                  color=LOAN),
            label(r"equity: \ the owners' stake, \ the first to absorb losses", font_size=23, color=EQUITY),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.7)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island has a bank now. Here is its balance sheet, as T-accounts. <bookmark mark='a'/> On the right, "
            "what it owes: ninety in deposits, which any depositor may withdraw at any moment, at full value. "
            "<bookmark mark='b'/> On the left, what it owns: ten in reserves, sixty in loans to the Island's "
            "bakers and boat-builders that will be repaid over years, and thirty in ten-year bonds. "
            "<bookmark mark='c'/> And ten of equity: the owners' stake, which absorbs losses first."
        ) as vo:
            self.play(FadeIn(bank), FadeIn(tag))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def transform(self):
        rows = VGroup(
            label(r"maturity transformation: \ borrow short, \ lend long", font_size=27, color=E.ACCENT),
            label(r"depositors get money they can spend at once; \ borrowers get loans they need not repay at once",
                  font_size=22, color=GREY_A),
            label(r"the bank earns the gap between long and short rates", font_size=22, color=RATE),
            label(r"and holds only a fraction of deposits in cash, \ because not everyone withdraws on the same day",
                  font_size=22, color=CB),
            label(r"which is why it cannot pay everyone on the same day", font_size=25, color=RUN),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "That is what a bank does. <bookmark mark='a'/> It borrows short and lends long. "
            "<bookmark mark='b'/> Depositors get money they can spend at once, and borrowers get loans they need not "
            "repay at once: both are better off than if each had to find the other. <bookmark mark='c'/> The bank "
            "earns the gap between the long rate it charges and the short rate it pays. <bookmark mark='d'/> It keeps "
            "only a fraction of deposits in cash, because on any normal day only a few depositors want their money. "
            "<bookmark mark='e'/> Which is exactly why it cannot pay everyone on the same day."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
