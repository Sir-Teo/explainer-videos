from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class UBI(VoiceoverScene):
    def construct(self):
        card(self, 12, r"A basic income?", r"What would a payment to everyone cost, and what does it do?",
             "Chapter twelve. A basic income?", lit={2017: r"Finland's experiment", 2023: r"Banerjee et al.",
                                                     2024: r"Vivalt et al."},
             scale=("household", "nation"), horizon=("a year",))
        self.arithmetic()
        self.financing()
        self.trials()

    def arithmetic(self):
        U = load("ubi")
        A = U["at30"]
        net = np.array(U["net_by_decile"]) / 1000
        bars = VGroup()
        for k, v in enumerate(net):
            x = -5.2 + 0.95 * k
            h = abs(v) * 0.07
            col = GAIN if v > 0 else LOSS
            r = Rectangle(width=0.7, height=max(h, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to(np.array([x, -0.6 + (h / 2 if v > 0 else -h / 2), 0]))
            bars.add(VGroup(r, label(f"{k + 1}", font_size=16, color=GREY_A).move_to(np.array([x, -0.6 - 0.25 if v
                                                                                                > 0 else -0.35, 0])),
                            label(f"{v:+.1f}".replace("-", r"$-$"), font_size=14, color=col).next_to(
                                r, UP if v > 0 else DOWN, buff=0.06)))
        axis = Line(np.array([-5.8, -0.6, 0]), np.array([4.0, -0.6, 0]), color=GREY_B, stroke_width=1.5)
        xl = label(r"net gain by decile of income, \ thousands of dollars a year", font_size=19,
                   color=GREY_A).move_to(np.array([-0.9, 2.0, 0]))
        side = VGroup(
            label(rf"the Island: \ a flat tax \\ of 30\% \ pays everyone \\ \${A['B']:,.0f}", font_size=18,
                  color=WHITE),
            label(rf"net gain below \\ the mean, \ \${A['break_even']:,.0f}: \\ {100 * A['recipients']:.0f}\% of "
                  r"people", font_size=18, color=GAIN),
            label(rf"Gini: \ {A['gini_before']:.3f} $\to$ {A['gini_after']:.3f}", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "A basic income pays everyone the same amount, with no conditions. What would it cost? "
            "<bookmark mark='a'/> The simplest version needs no new arithmetic: tax all income at a flat rate and "
            "pay the proceeds back equally. On the Island, with incomes around fifty thousand dollars, a thirty "
            f"percent tax pays everyone {A['B']:,.0f} dollars a year. <bookmark mark='b'/> Everyone with an income "
            f"below the average, {A['break_even']:,.0f} dollars, gains: {say_pct(A['recipients'], 0)} of people, "
            "because the average is above the typical income. The bottom tenth gains about fifteen thousand "
            "dollars, the top tenth pays about thirty-five. <bookmark mark='c'/> The Gini index falls from "
            f"{A['gini_before']:.2f} to {A['gini_after']:.2f}. It is the flat tax and equal transfer of Part forty, "
            "on a larger scale."
        ) as vo:
            self.play(FadeIn(axis), FadeIn(xl), FadeIn(tag), FadeIn(side[0]), *[FadeIn(b_[1]) for b_ in bars],
                      run_time=1.2)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_[0], DOWN if net[k] > 0 else UP) for k, b_ in
                                    enumerate(bars)], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(*[FadeIn(b_[2]) for b_ in bars], FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def financing(self):
        U = load("ubi")
        t = np.array(U["t"])
        ax = plane([0, 0.9], [0, 60], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[0, 20, 40, 60], xlabel=r"flat tax rate",
                   ylabel=r"basic income, \ thousands of dollars a year", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        l0 = path(ax, t, np.array(U["B0"]) / 1000, GREY_B, 3.0)
        l1 = path(ax, t, np.array(U["B1"]) / 1000, GAIN, 3.4)
        top = dot(ax, U["best_t"], U["best_B"] / 1000, GAIN, 0.09)
        side = VGroup(
            label(r"grey: \ if no one \\ changes what they earn", font_size=18, color=GREY_B),
            label(rf"green: \ incomes shrink \\ with the tax \ ($e$ = {U['e']:g}, \\ Part 41)", font_size=18,
                  color=GAIN),
            label(rf"at 30\%: \ \${U['at30e']['B']:,.0f}", font_size=18, color=WHITE),
            label(rf"the most it can pay: \\ \${U['best_B']:,.0f} at {100 * U['best_t']:.0f}\%", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "But taxes change what people earn. <bookmark mark='a'/> If no one responded, the basic income would "
            "rise in step with the tax rate. <bookmark mark='b'/> With an elasticity of taxable income of a quarter, "
            "as in Part forty-one, incomes shrink as the rate rises, <bookmark mark='c'/> so a thirty percent tax "
            f"pays {U['at30e']['B']:,.0f} dollars instead of {U['at30']['B']:,.0f}. <bookmark mark='d'/> And there "
            f"is a ceiling: the most the Island can pay is about {U['best_B']:,.0f} dollars, at a tax rate of "
            f"{say_pct(U['best_t'], 0)}, the top of its Laffer curve. In a real budget the basic income would also "
            "compete with everything else the taxes pay for."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(l0), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(top, scale=1.4), FadeIn(side[3]))
        self.clear_scene()

    def trials(self):
        T = tables.UBI_TRIALS.data
        cards = point_cards([
            (r"Finland, \ 2017--18", rf"{T['fi_n']:,} unemployed \\ people, \ {T['fi_eur']} euros \\ a month: \ "
                                     r"slightly \\ more work, \ better \\ reported wellbeing", UNEMP),
            (r"United States, \ 2020s", rf"{T['or_n']:,} people, \ \${T['or_usd']:,} \\ a month for three \\ years: "
                                        rf"\ about \\ {T['or_hours']} hours less \\ work a week", PENSION),
            (r"Kenya, \ 2020s", rf"lump sums of about \\ \${T['ke_lump']} beat the same \\ money paid monthly; \\ no "
                                r"sign of less work", GAIN),
            (r"what trials miss", r"who pays, \ and what \\ happens when \\ everyone gets it", HOLD),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"what the trials found", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.UBI_TRIALS.tag, corner=DR, font_size=11)
        with self.voiceover(
            "What do people do with unconditional money? <bookmark mark='a'/> Finland gave two thousand unemployed "
            "people five hundred and sixty euros a month for two years, without conditions: they worked slightly "
            "more than a control group and reported better wellbeing, though the survey had no baseline. "
            "<bookmark mark='b'/> In America, a study led by Eva Vivalt gave a thousand people a thousand dollars a "
            "month for three years: they worked about 1.3 hours a week less, a moderate effect, and spent more on "
            "basic needs. <bookmark mark='c'/> In rural Kenya, a study by Abhijit Banerjee, Tavneet Suri and "
            "coauthors found that lump sums did at least as well as the same money paid monthly, with no sign that "
            "the payments discouraged work. <bookmark mark='d'/> But a trial of a thousand people cannot show what "
            "happens when everyone receives the money and everyone pays the tax for it: prices, wages and the "
            "budget all change."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
