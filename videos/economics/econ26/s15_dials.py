from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ26.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ deposit betas, \ and the cost of a crisis", r"How sticky are deposit rates, "
             r"\ and how much output does a banking crisis cost?", "Chapter thirteen. The Dials: deposit betas, "
             "and the cost of a crisis.", lit={2009: r"Reinhart and Rogoff", 2023: r"the New York Fed"},
             scale=("firm", "nation"), horizon=("years",))
        self.beta()
        self.cost()

    def beta(self):
        dial = dials.DIALS["deposit_beta"]
        head = status_head(dial, r"the deposit beta \ (new)")
        frame, rows = dial_rows(dial, 0.0, 0.7, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], r"share of a rise in "
                                r"the policy rate passed on to depositors", top=2.2, step=0.62)
        meaning = wrapped_label(tex_safe(dial.meaning), 12.0, 17, GREY_A).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Liberty Street Economics (2022, 2023); \ S\&P Global (2023); \ this film", corner=DR,
                            font_size=12)
        b = load("betas")
        with self.voiceover(
            "Two dials open in this part. The first is the deposit beta: the share of a rise in the policy rate "
            "that banks pass on to their depositors. <bookmark mark='a'/> Economists at the New York Fed found "
            "that in the tightening of 2004 to 2006, the beta on interest-bearing deposits approached sixty percent "
            "by the end. <bookmark mark='b'/> In the cycle of 2015 to 2019 it never passed forty. "
            "<bookmark mark='c'/> In the much faster tightening of 2022 it reached almost forty percent by the end of "
            "the year. <bookmark mark='d'/> S&P Global's figure for all deposits, by the third quarter of 2023, "
            "was thirty-eight and a half. <bookmark mark='e'/> This film's own, from the FDIC's national rates: "
            f"savings accounts passed on {100 * b['beta_savings']:.0f} percent of the rise, <bookmark mark='f'/> "
            f"twelve-month certificates of deposit {100 * b['beta_cd']:.0f}. <bookmark mark='g'/> The status: it "
            "depends on the setting, the product, and how long the rise has lasted. And a low beta is worth "
            "something to a bank only while its depositors stay."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("g")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def cost(self):
        dial = dials.DIALS["crisis_cost"]
        c = load("crisis")
        head = status_head(dial, r"the output cost of a banking crisis \ (new)")
        frame, rows = dial_rows(dial, 0.0, 20.0, [0, 5, 10, 15, 20], r"percent of GDP", top=2.0, step=0.68,
                                fmt="{:.1f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.0, 17, GREY_A).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Reinhart and Rogoff, \ AER 99(2) (2009); \ Cerra and Saxena, \ AER 98(1) (2008); \ "
                            r"Romer and Romer, \ AER 107(10) (2017); \ this film", corner=DR, font_size=12)
        with self.voiceover(
            "The second dial: how much output a banking crisis costs. <bookmark mark='a'/> Carmen Reinhart and "
            "Kenneth Rogoff found that after systemic banking crises, real output per person fell by more than nine "
            "percent from peak to trough, on average. <bookmark mark='b'/> Valerie Cerra and Sweta Saxena, with "
            "data on a hundred and ninety countries, found that the loss after a banking crisis is about ten percent "
            "and does not go away. <bookmark mark='c'/> Christina and David Romer, measuring financial distress "
            "directly in twenty-four rich countries, found a peak decline nearer six percent, and only four in "
            "another specification, and very different from one crisis to the next. "
            f"<bookmark mark='d'/> America in 2008: real GDP fell {c['fall']:.1f} percent from peak to trough. "
            f"<bookmark mark='e'/> But by 2019 it was {c['gap_2019']:.0f} percent below the trend of 1990 to 2007, "
            "which would be the biggest number here, if that trend was the right one to draw; growth had begun to "
            "slow before the crisis. <bookmark mark='f'/> The status: contested. The cost is large, but how large "
            "depends on what you compare it with."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("f")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
