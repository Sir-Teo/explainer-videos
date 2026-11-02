from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, DELTA, GOOD, IV, OPT, PART, SPOT, illustration, load, real_data, ymd_to_year


class Crash(VoiceoverScene):
    def construct(self):
        b = load("book2024")
        m = load("market")
        self.card()
        self.file(m)
        self.book(b)
        self.debate()

    def card(self):
        c = chapter_card(5, r"January 2024: the snowballs melt", r"What happens when a crowded barrier breaks?", part=PART)
        with self.voiceover("Chapter five. January 2024: the snowballs melt."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def file(self, m):
        f = m["fall_2024"]
        card = crisis_card(
            r"January -- February 2024", r"The snowball knock-ins",
            r"China's small-cap indices fell through the knock-in levels of snowballs sold in 2021--2023. On 11 January "
            r"Bloomberg reported about \$13 billion of snowballs near their loss triggers; UBS put the whole market at "
            r"about \$50 billion. Brokers that had issued them unwound the index futures they held as hedges. In April, "
            r"regulators told brokers to limit their snowball exposure.",
            stats=[(rf"{100 * f['drop']:.0f}\%", r"CSI 500 (ETF), 29 Dec to 5 Feb"), (r"\$13\text{bn}", r"near knock-in, 11 Jan"),
                   (r"\$50\text{bn}", r"UBS's estimate of the market")], width=11.6, font_size=24)
        card.move_to(ORIGIN)
        src = note(r"Bloomberg (11 January and 24 April 2024); Reuters via Asia Financial; Risk.net; Yahoo Finance (510500.SS)",
                   font_size=18, color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "In January 2024 China's small-cap indices fell through the knock-in levels of the snowballs sold over "
            f"the previous three years. The CSI 500 fell {100 * abs(f['drop']):.0f} percent in five weeks; the CSI 1000 "
            "fell further. On the eleventh of January, Bloomberg reported about thirteen billion dollars of snowballs "
            "close to their loss triggers; UBS estimated the whole market at around fifty billion. As notes knocked "
            "in, the brokers that issued them unwound the index futures they held as hedges. In April, regulators "
            "told brokers to limit their exposure to the product."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()

    def book(self, b):
        t = ymd_to_year(b["dates"])
        px = np.asarray(b["close"])
        ki = np.asarray(b["knocked_in"])
        dl = np.asarray(b["dealer_delta"])
        t0, t1 = t[0], t[-1]
        g1 = axes([t0, t1], [4.3, 5.9], x_length=10.0, y_length=1.9, ylabel=r"CSI 500 ETF", xticks=[], yticks=[4.5, 5.0, 5.5],
                  font_size=14)
        g2 = axes([t0, t1], [0, 12], x_length=10.0, y_length=1.6, ylabel=r"notes knocked in", xticks=[], yticks=[0, 6, 12],
                  font_size=14)
        g3 = axes([t0, t1], [10, 27], x_length=10.0, y_length=1.9, ylabel=r"dealers' hedge", yticks=[10, 15, 20, 25],
                  xticks=[ymd_to_year([20231201])[0], ymd_to_year([20240102])[0], ymd_to_year([20240201])[0],
                          ymd_to_year([20240229])[0]],
                  xfmt=lambda u: {0: "1 Dec", 1: "2 Jan", 2: "1 Feb", 3: "29 Feb"}[int(np.argmin(np.abs(
                      ymd_to_year([20231201, 20240102, 20240201, 20240229]) - u)))], font_size=14)
        G = VGroup(g1, g2, g3).arrange(DOWN, buff=0.25).to_edge(LEFT, buff=0.6)
        l1 = curve(g1.ax, t, px, SPOT, stroke_width=2.5)
        steps = VMobject(stroke_color=BAD, stroke_width=3).set_points_as_corners(
            [g2.ax.c2p(a, v) for i in range(len(t)) for a, v in ((t[i], ki[i - 1] if i else ki[0]), (t[i], ki[i]))])
        l3 = curve(g3.ax, t, dl, DELTA, stroke_width=3)
        i_pk = int(np.argmax(dl))
        i_low = int(np.argmin(px))
        side = VGroup(
            wrapped_label(r"36 snowballs, one issued at the start of each month of 2021--2023 on the CSI 500 (knock-out "
                          r"103\% monthly, knock-in 75\% daily, 24 months), followed day by day on the index's real path",
                          3.4, 17, GREY_A),
            wrapped_label(rf"{b['n_ki_2024']} knocked in between 22 January and 5 February", 3.4, 19, BAD),
            wrapped_label(rf"the dealers' futures hedge, priced by the surrogate (chapter 9): it grew from {dl[0]:.0f} to "
                          rf"{dl[i_pk]:.0f} notes' worth as the index fell, then the knock-ins cut it to {dl[i_low]:.0f} on "
                          r"the day of the low: selling into the fall", 3.4, 17, DELTA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        src = illustration(r"stylized book, one note of notional 1 a month; the index path is real (510500.SS)", corner=DL)
        with self.voiceover(
            "Rebuild it on the real path. Suppose one snowball was issued at the start of every month from 2021 to "
            "2023 on the CSI 500, with the standard terms, and follow all of them, day by day, through the winter. "
            "<bookmark mark='a'/> From the twenty-second of January the notes struck in 2022 and 2023 start to knock "
            f"in, {b['n_ki_2024']} of them by the fifth of February. <bookmark mark='b'/> Now the issuers' hedge, "
            "priced every day by the neural surrogate of chapter nine. As the index fell toward the barriers, the "
            f"hedge grew, from {dl[0]:.0f} notes' worth of futures to {dl[i_pk]:.0f}: the dealers were buying the dip. "
            f"Then the knock-ins came, and the hedge collapsed to {dl[i_low]:.0f} on the day of the low. The same "
            "desks that had been buying all the way down were forced to sell, at the bottom."
        ) as vo:
            self.play(FadeIn(G[0]), Create(l1), FadeIn(side[0]), FadeIn(src), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(G[1]), Create(steps), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(G[2]), Create(l3), FadeIn(side[2]), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def debate(self):
        a = history_card(r"Risk.net", r"the selling side", r"Issuers' re-hedging after the knock-ins added to the sell-off "
                         r"in index futures, which pushed the indices toward more barriers: a feedback loop, like the "
                         r"inverse VIX notes of Part 12.", color=QC.CRISIS, width=5.8)
        b_ = history_card(r"SRP", r"the sceptics", r"Analysts quoted by StructuredRetailProducts argued that the "
                          r"outstanding notional was modest next to the futures market, and that hedges do not all move one "
                          r"way, so the knock-ins could not by themselves explain the fall.", color=QC.IDEA, width=5.8)
        VGroup(a, b_).arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to(UP * 0.3)
        foot = wrapped_label(r"how much the hedging moved the market is disputed; that the knock-ins forced hedges to be sold "
                             r"at the worst moment is arithmetic", 11.0, 20, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Did the hedging cause the fall? Reports in Risk.net described issuers' re-hedging adding to the selling "
            "in index futures, pushing the indices toward more barriers, a feedback loop like Part twelve's inverse "
            "volatility notes. <bookmark mark='a'/> Others were sceptical: the notional outstanding was modest next "
            "to the futures market, and hedges do not all point one way. How much the hedging moved the market is "
            "disputed. That the knock-ins forced hedges to be sold at the worst moment is arithmetic."
        ) as vo:
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(b_, shift=UP * 0.2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
