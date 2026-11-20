from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ22.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ the propensity to spend a windfall", r"How much of a one-off payment do "
             r"households spend, \ and on what does it depend?", "Chapter thirteen. The Dials: the propensity to "
             "spend a windfall.", scale=("household", "nation"),
             lit={2006: r"Johnson et al.", 2013: r"Parker et al.", 2018: r"Kueng"}, horizon=("a quarter", "a year"))
        self.mpc()
        self.gap()

    def mpc(self):
        dial = dials.DIALS["mpc_windfall"]
        head = status_head(dial, r"the propensity to spend a windfall \ (new)")
        frame, rows = dial_rows(dial, 0, 60, [0, 10, 20, 30, 40, 50, 60], r"percent spent", top=2.2, step=0.68,
                                fmt="{:.0f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 17, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"the six rows' sources: \ see the dial's record", corner=DR, font_size=12)
        e = dial.estimates
        with self.voiceover(
            "This part opens a dial: the propensity to spend a windfall, the share of a one-off payment that is "
            "spent soon after it arrives. <bookmark mark='a'/> The 2001 rebates: thirty percent, the middle of "
            "twenty to forty, on nondurables within the quarter. <bookmark mark='b'/> The 2008 payments: about "
            "twenty-one, the middle of twelve to thirty, before counting cars. <bookmark mark='c'/> The 2020 "
            f"payments: about {e[2].value:.0f}. <bookmark mark='d'/> Alaska's dividend, in account data: "
            f"{e[3].value:.0f}. <bookmark mark='e'/> Italians asked directly, over a year: {e[4].value:.0f}. "
            "<bookmark mark='f'/> And the Island's buffer-stock households, a model, over a year: "
            f"{e[5].value:.0f}. <bookmark mark='g'/> The status: it depends on the setting. Who receives the money "
            "matters more than any average: households short of cash spend far more, whatever their net worth, and "
            "when many households already have cash, as in 2020, the share falls."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("g")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def gap(self):
        rows = VGroup(
            label(r"theory against the dial", font_size=30, color=E.ACCENT),
            label(r"permanent income: \ about 1\% a quarter", font_size=24, color=INCOME),
            label(r"one-asset buffer stock: \ about 23\% in a year, \ less in a quarter", font_size=24, color=SPEND),
            label(r"the data: \ 10 to 40\% in a quarter on nondurables alone", font_size=24, color=SAVE),
            label(r"the two-asset model of chapter 8 closes most of the gap: \ many households with wealth, \ little "
                  r"of it liquid", font_size=23, color=HOUSE),
            label(r"Part 52 builds economies of such households, \ and asks what they do to monetary and fiscal policy",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "Put the dial next to the theory. <bookmark mark='a'/> Permanent income says about one percent a "
            "quarter. <bookmark mark='b'/> The one-asset buffer stock says about a quarter of a windfall within a "
            "year, and less within a quarter. <bookmark mark='c'/> The data say ten to forty percent within a "
            "quarter, on nondurables alone. <bookmark mark='d'/> The model with two assets, a house or pension that "
            "pays well and cash that does not, closes most of the gap, because it makes many households wealthy and "
            "short of cash at once. Kaplan and Violante built it to match the rebates. <bookmark mark='e'/> Part "
            "fifty-two builds whole economies of such households, and asks what they change about monetary and "
            "fiscal policy."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
