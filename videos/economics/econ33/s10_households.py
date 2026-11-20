from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403


class Households(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Households: \ debt and spending", r"Why did spending fall most where households owed most?",
             "Chapter eight. Households: debt and spending.", lit={2013: r"Mian, Rao and Sufi",
                                                                    2014: r"\emph{House of Debt}"},
             scale=("household", "city"), horizon=("a year",))
        self.levered()
        self.counties()

    def levered(self):
        rows = VGroup(
            label(r"a house worth 100, \ bought with a mortgage of 80: \ equity 20", font_size=25, color=HOUSE),
            label(r"prices fall 20\%: \ the house is worth 80, \ the mortgage is still 80, \ equity 0", font_size=25,
                  color=CRISIS),
            label(r"the lender loses nothing yet; \ the borrower has lost everything", font_size=25, color=WHITE),
            label(r"debt puts the first losses on the borrowers, \ who spend more of each dollar they lose",
                  font_size=24, color=CREDIT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.2)
        tag = published_tag(r"Mian and Sufi, \ \emph{House of Debt} (2014)", corner=DR, font_size=12)
        head = label(r"who bears the fall in house prices?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Atif Mian and Amir Sufi asked who bore the fall in house prices, and why that mattered. "
            "<bookmark mark='a'/> Take a house worth a hundred, bought with a mortgage of eighty. The owner's equity "
            "is twenty. <bookmark mark='b'/> Prices fall twenty percent. The house is worth eighty, the mortgage is "
            "still eighty, and the equity is gone. <bookmark mark='c'/> The lender has lost nothing yet; the "
            "borrower has lost everything. <bookmark mark='d'/> Debt concentrates the first losses on borrowers, "
            "who are poorer and spend more of each dollar they gain or lose, so the same fall in house prices cuts "
            "spending more when it lands on them."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def counties(self):
        C = load("counties")
        lev = np.array(C["lev"])
        loss = np.array(C["loss"])
        ds = np.array(C["ds"])
        ax = plane([-160, 0], [-12, 1], center=LEFT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                   xticks=[-150, -100, -50, 0], yticks=[-12, -8, -4, 0],
                   xlabel=r"housing wealth lost, \ \% of a year's spending", ylabel=r"spending, \ \% change",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        def tint(lv):
            return interpolate_color(ManimColor(CALM), ManimColor(CRISIS), float(np.clip(lv / 0.8, 0, 1)))

        pts = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.035, color=tint(lv))
                       for x, y, lv in zip(loss, ds, lev) if -160 <= x <= 0 and -12 <= y <= 1])
        q = C["by_quintile"]
        ax2 = plane([0.5, 5.5], [0, 8], center=RIGHT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                    xticks=[1, 2, 3, 4, 5], yticks=[0, 2, 4, 6, 8], xlabel=r"leverage, \ lowest to highest fifth",
                    ylabel=r"cents spent per dollar of housing wealth", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:.0f}", font_size=13)
        bars = VGroup()
        truths = VGroup()
        for k, row in enumerate(q):
            p0, p1 = ax2.ax.c2p(k + 0.7, 0), ax2.ax.c2p(k + 1.3, 100 * row["mpc"])
            col = interpolate_color(ManimColor(CALM), ManimColor(CRISIS), k / 4)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=0.85,
                               stroke_width=0).move_to((p0 + p1) / 2))
            truths.add(seg(ax2, k + 0.62, 100 * row["truth"], k + 1.38, 100 * row["truth"], WHITE, 2.5))
        k1 = label(r"each dot a county: \ green low leverage, \ red high", font_size=16, color=GREY_A).next_to(
            ax, UP, buff=0.1)
        k2 = label(r"bars: \ estimated; \ white: \ planted", font_size=16, color=GREY_A).next_to(ax2, UP, buff=0.1)
        foot = label(rf"overall: \ {100 * C['mpc']:.1f} cents per dollar; \ {100 * q[0]['mpc']:.1f} in the least "
                     rf"levered fifth, \ {100 * q[-1]['mpc']:.1f} in the most \ (Mian, \ Rao and Sufi: \ 5 to 7)",
                     font_size=19, color=WHITE).to_edge(DOWN, buff=0.3).shift(LEFT * 0.8)
        tag = island_tag(corner=DR, font_size=13)
        with self.voiceover(
            "Their evidence came from comparing American counties and zip codes. Here is the same design on the "
            "Island's four hundred counties, with the truth planted. <bookmark mark='a'/> House prices fell "
            "everywhere, more where housing supply was tight and where borrowing had been heaviest. Each dot is a "
            "county: how much housing wealth it lost, and how much its spending fell. <bookmark mark='b'/> "
            "Splitting the counties by how leveraged their households were, and estimating the spending response "
            "in each group, recovers what was planted: the more indebted the households, the more they cut "
            "spending per dollar of lost wealth. <bookmark mark='c'/> In the American data, Mian, Kamalesh Rao and "
            "Sufi estimated five to seven cents per dollar of housing wealth on average, with more indebted and "
            "poorer zip codes cutting much more. Their conclusion, in the book House of Debt, was that the slump of "
            "2008 was driven by indebted households, and that relieving mortgage debt would have done more for "
            "spending than rescuing the lenders did. That conclusion is still argued; the cross-county pattern is "
            "not."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(ax2), FadeIn(tag), FadeIn(k1),
                      LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.004), run_time=1.8)
            vo.wait_until("a")
            self.play(Indicate(k1, color=WHITE))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), FadeIn(truths),
                      FadeIn(k2), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
