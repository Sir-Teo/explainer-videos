from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class PassThrough(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Cost pass-through, \ 2021--22", r"When costs jumped, \ how much reached the shelf?",
             "Chapter eleven. Cost pass-through, 2021 to 22.", lit={2021: r"the cost jump"},
             scale=("market", "nation"), horizon=("a month", "a year"))
        self.lags()
        self.jump()

    def lags(self):
        Pt = load("passthrough")
        cum = np.array(Pt["cum"])
        ax = plane([-0.7, 12.7], [0, 0.8], center=LEFT * 2.7 + DOWN * 0.4, x_length=6.4, y_length=4.6,
                   xticks=[0, 3, 6, 9, 12], yticks=[0, 0.2, 0.4, 0.6, 0.8], xlabel=r"months after the change",
                   ylabel=r"cumulative pass-through", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        b = bars(ax, range(13), cum, [PPI] * 13, width=0.6)
        err = Line(ax.ax.c2p(12, cum[-1] - 2 * Pt["cum_se"]), ax.ax.c2p(12, cum[-1] + 2 * Pt["cum_se"]),
                   color=WHITE, stroke_width=2.4)
        side = VGroup(
            MathTex(r"\Delta \ln p^{\text{shelf}}_t = a + \sum_{k=0}^{12} b_k\, \Delta \ln p^{\text{factory}}_{t-k} "
                    r"+ e_t", font_size=28, color=WHITE),
            label(r"monthly, \ 2000--2019: \ food at home \ (CPI) \\ on processed food at the factory gate \ (PPI)",
                  font_size=19, color=GREY_A),
            label(rf"after a year: \ {cum[-1]:.2f} \ (s.e. {Pt['cum_se']:.2f})", font_size=22, color=PPI),
            label(r"a 10\% rise at the factory gate \\ raises the grocer's prices about 6\% within a year",
                  font_size=19, color=WHITE),
            label(r"the rest: \ the grocer's own costs, \ labour, \ rent, \ which did not move", font_size=18,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.35)
        tag = data_tag(rf"BLS via FRED: \ CUSR0000SAF11, \ WPU02, \ retrieved {Pt['retrieved']}", corner=DL,
                       font_size=12)
        with self.voiceover(
            "How much of a cost change reaches the price a buyer pays is the pass-through rate of Part fifty-nine, "
            "now for a whole industry. <bookmark mark='a'/> Take the price of food at the grocer's, from the "
            "consumer price index, and the price of processed food at the factory gate, from the producer price "
            "index. Regress the monthly change in the first on this month's and the past year's changes in the "
            "second, over 2000 to 2019. <bookmark mark='b'/> The cumulative pass-through builds over the months "
            f"and reaches {cum[-1]:.2f} after a year, with a standard error of {Pt['cum_se']:.2f}. <bookmark "
            "mark='c'/> So a ten percent rise at the factory gate raised the grocer's prices by about six percent "
            "within a year. The rest of the grocer's price is its own labour, rent and margin, which do not move "
            "with the factory price."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in b], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(err), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def jump(self):
        Pt = load("passthrough")
        months = Pt["months"]
        n = len(months)
        x = np.arange(n)
        top = max(max(Pt["ppi"]), max(Pt["actual"])) * 1.15
        ax = plane([0, n - 1], [-2, top], center=LEFT * 2.7 + DOWN * 0.4, x_length=6.4, y_length=4.6,
                   xticks=[0, 12, 24, 36], yticks=[0, 5, 10, 15, 20, 25], xlabel=r"months from December 2020",
                   ylabel=r"cumulative change, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        pp = path(ax, x, Pt["ppi"], PPI, 2.8, smooth=False)
        pa = path(ax, x, Pt["actual"], FOOD, 3.0, smooth=False)
        pr = DashedVMobject(path(ax, x, Pt["pred"], WHITE, 2.4, smooth=False), num_dashes=40)
        key = VGroup(label(r"orange: \ the factory gate", font_size=15, color=PPI),
                     label(r"green: \ the grocer's, \ actual", font_size=15, color=FOOD),
                     label(r"white: \ the grocer's, \ predicted \\ by 2000--19's pass-through", font_size=15,
                           color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        key.move_to(ax.ax.c2p(n - 1, 0.8), aligned_edge=DR)
        side = VGroup(
            label(rf"2021--2023: \ factory gate +{Pt['ppi_change']:.1f}\%; \ grocer's +{Pt['cpi_change']:.1f}\%",
                  font_size=20, color=WHITE),
            label(rf"the old relation predicted +{Pt['pred_change']:.1f}\%", font_size=20, color=GREY_A),
            label(r"pass-through was higher when costs rose together:", font_size=20, color=E.ACCENT),
            label(r"a cost every rival shares is passed on more \\ than one only you bear \ (Part 59's Staples)",
                  font_size=18, color=PPI),
            label(r"when everyone's prices rise, \ raising yours is less noticed, \\ and changing a price often "
                  r"costs little next to the cost change", font_size=18, color=GREY_A),
            label(r"how much was wider margins is still argued over", font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BLS via FRED: \ CUSR0000SAF11, \ WPU02", corner=DL, font_size=12)
        with self.voiceover(
            "Then came 2021. <bookmark mark='a'/> From the end of 2020 to the end of 2023, processed food at the "
            f"factory gate rose {Pt['ppi_change']:.1f} percent <bookmark mark='b'/> and food at the grocer's "
            f"{Pt['cpi_change']:.1f} percent. <bookmark mark='c'/> Feed the factory-gate rise through the pass-through "
            f"of 2000 to 2019, and the grocer's prices should have risen about {Pt['pred_change']:.1f} percent. They "
            "rose more. <bookmark mark='d'/> Theory offers reasons. A cost that every rival shares is passed on more "
            "than one a single firm bears, the distinction the Staples case turned on. When everyone's prices are "
            "rising, raising yours is noticed less, and changing a price costs little next to the change in cost, "
            "so prices adjust faster and further. <bookmark mark='e'/> How much was also wider margins is still "
            "argued over, and an industry-level regression cannot settle it; it can only show that the relation "
            "of quiet years did not hold."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(pp), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(pa), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(pr), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        self.clear_scene()
