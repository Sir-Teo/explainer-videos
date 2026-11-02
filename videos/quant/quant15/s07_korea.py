from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, GOOD, OPT, PART, SPOT, illustration, load, real_data, ymd_to_year


class Korea(VoiceoverScene):
    def construct(self):
        k = load("korea")
        self.card()
        self.notes(k)
        self.file()

    def card(self):
        c = chapter_card(6, r"Korea's ELS", r"What happens when a bank sells a knock-in to savers?", part=PART)
        with self.voiceover("Chapter six. Korea's equity-linked securities."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def notes(self, k):
        t = ymd_to_year(k["date"])
        px = np.asarray(k["close"])
        g = axes([2020, 2025], [3000, 13000], x_length=7.4, y_length=4.4, ylabel=r"HSCEI",
                 xticks=[2020, 2021, 2022, 2023, 2024, 2025], yticks=[4000, 8000, 12000],
                 yfmt=lambda u: f"{u:,.0f}".replace(",", "{,}"), font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, t, px, SPOT, stroke_width=2.2)
        rows = k["rows"]
        marks = VGroup()
        for r in rows:
            t0 = ymd_to_year([r["start"]])[0]
            col = BAD if r["knocked_in"] else GOOD
            marks.add(VGroup(Dot(ax.c2p(t0, r["S0"]), radius=0.06, color=col),
                             DashedLine(ax.c2p(t0, 0.5 * r["S0"]), ax.c2p(min(t0 + 3, 2025), 0.5 * r["S0"]),
                                        stroke_color=col, stroke_width=1.2, dash_length=0.06)))
        lost = [r for r in rows if r["knocked_in"]]
        side = VGroup(
            wrapped_label(r"a stylized step-down ELS, as sold by Korean banks: three years; early redemption every six "
                          r"months if the index is above 90, 90, 85, 85, 80\% of its start, paying 6\% a year; a "
                          r"knock-in at 50\%, watched daily", 4.4, 18, GREY_A),
            wrapped_label(rf"issued monthly through 2021: {len(lost)} of {len(rows)} knocked in during 2022's fall and "
                          rf"matured in 2024 with losses of {100 * min(-r['return'] for r in lost):.0f} to "
                          rf"{100 * max(-r['return'] for r in lost):.0f}\%", 4.4, 19, BAD),
            wrapped_label(r"the rest were redeemed or repaid with their coupon: the same product, a few months apart", 4.4,
                          19, GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        src = real_data(r"Yahoo Finance: Hang Seng China Enterprises Index, daily; stylized terms, not any one bank's note")
        with self.voiceover(
            "Korea's version is the equity-linked security, and its favourite underlying was Hong Kong's index of "
            "Chinese companies, the HSCEI. A typical note ran three years. Every six months it could be repaid early "
            "with a coupon, if the index stood above a stepped-down level, and it carried a knock-in at half the "
            "starting level. <bookmark mark='a'/> Here are notes issued each month of 2021, near the index's peak. "
            "The dashed lines are their knock-ins. In 2022 the index fell through half of its early-2021 level. "
            f"{len(lost)} of the {len(rows)} notes knocked in, and at maturity in 2024 their buyers lost between "
            f"{100 * min(-r['return'] for r in lost):.0f} and {100 * max(-r['return'] for r in lost):.0f} percent. "
            "<bookmark mark='b'/> Notes issued a few months later, a little lower, never touched their barriers and "
            "paid their coupons. The same product, months apart, opposite outcomes."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(src), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.15, run_time=3), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def file(self):
        card = crisis_card(
            r"2023 -- 2024", r"Korea's HSCEI-linked ELS",
            r"Korean banks and brokers sold equity-linked securities tied to the HSCEI to savers, many of them retail "
            r"customers who had come in for deposits. About 19.3 trillion won were outstanding in November 2023, 15.9 "
            r"trillion of it sold through commercial banks. As 2021's notes matured, losses reached 1.2 trillion won in "
            r"the first two months of 2024. The Financial Supervisory Service set out a compensation scheme in March "
            r"2024, and banks paid back part of investors' losses, typically 20 to 50\%.",
            stats=[(r"19.3\ \text{tn won}", r"outstanding, November 2023"), (r"1.2\ \text{tn won}", r"lost, Jan--Feb 2024"),
                   (r"20\text{--}50\%", r"of losses compensated")], width=11.6, font_size=24)
        card.move_to(ORIGIN)
        src = note(r"Korea JoongAng Daily, Korea Economic Daily and Korea Herald reports, citing the FSS and the banks",
                   font_size=18, color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "The real numbers. About nineteen trillion won of these notes were outstanding at the end of 2023, most "
            "of them sold through commercial banks, often to savers who had walked in for a deposit. In the first "
            "two months of 2024 alone, maturing notes lost 1.2 trillion won. Korea's Financial Supervisory Service "
            "laid out a compensation scheme that March, and the banks paid back part of the losses, typically "
            "between a fifth and a half. Regulators faulted how the notes were sold, not their arithmetic: each was a "
            "short put, sold like a deposit with a coupon, to people who could not price it."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()
