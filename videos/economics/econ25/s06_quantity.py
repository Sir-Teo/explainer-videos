from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403


def lg(pct):
    return float(np.log10(max(pct, 0.3)))


class Quantity(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The quantity theory", r"Does more money mean higher prices?", "Chapter five. The quantity "
             r"theory.", lit={1911: r"Fisher", 1963: r"Friedman and Schwartz", 1995: r"McCandless and Weber"},
             scale=("nation", "world"), horizon=("decades",))
        self.equation()
        self.world()
        self.short_run()
        self.us()

    def equation(self):
        rows = VGroup(
            MathTex(r"M\,V \;=\; P\,Y", font_size=64, color=WHITE),
            label(r"money $\times$ how often each dollar is spent $=$ the price level $\times$ real output",
                  font_size=23, color=GREY_A),
            label(r"an identity: \ it defines velocity $V$", font_size=22, color=GREY_B),
            MathTex(r"\pi \;\approx\; \Delta\ln M \;+\; \Delta\ln V \;-\; \Delta\ln Y", font_size=46, color=PRICE),
            label(r"it becomes a theory if velocity is stable and output does not depend on money: \ then inflation "
                  r"is money growth less output growth", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Fisher, \emph{The Purchasing Power of Money} (1911)", corner=DR, font_size=12)
        with self.voiceover(
            "Irving Fisher wrote the oldest equation in monetary economics in its modern form in 1911. "
            "<bookmark mark='a'/> The stock of money times velocity, how many times a year each dollar is spent, "
            "equals the price level times real output: total spending, counted two ways. <bookmark mark='b'/> As it "
            "stands it is an identity: it defines velocity. <bookmark mark='c'/> In growth rates, inflation is money "
            "growth, plus the growth of velocity, minus the growth of output. <bookmark mark='d'/> It becomes a "
            "theory when velocity is stable and output grows for its own reasons, as in Act Five. Then, over long "
            "periods, inflation is simply money growth less output growth."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def world(self):
        w = load("world")
        ax = plane([lg(0.3), lg(200)], [lg(0.3), lg(200)], center=LEFT * 2.2 + DOWN * 0.3, x_length=6.4, y_length=5.2,
                   xticks=[lg(1), lg(3), lg(10), lg(30), lg(100)], yticks=[lg(1), lg(3), lg(10), lg(30), lg(100)],
                   xlabel=r"broad money growth, \ \% a year \ (log scale)", ylabel=r"inflation, \ \% a year",
                   xfmt=lambda v: f"{10 ** v:.0f}", yfmt=lambda v: f"{10 ** v:.0f}", font_size=15)
        pts = VGroup(*[dot(ax, lg(100 * np.expm1(p["money"])), lg(100 * np.expm1(p["inflation"])), color=MONEY,
                           r=0.045) for p in w["points"]])
        diag = seg(ax, lg(0.3), lg(0.3), lg(200), lg(200), color=GREY_B, width=2, dashed=True)
        names = VGroup()
        for name, short in (("Japan", "Japan"), ("United States", "US"), ("China", "China"), ("Brazil", "Brazil"),
                            ("Angola", "Angola"), ("Turkiye", "Turkey")):
            p = w["labels"].get(name)
            if p:
                names.add(label(short, font_size=14, color=WHITE).next_to(
                    ax.ax.c2p(lg(100 * np.expm1(p["money"])), lg(100 * np.expm1(p["inflation"]))), LEFT, buff=0.08))
        side = VGroup(
            label(rf"{w['n']} countries, \\ averages over 1990--2024", font_size=20, color=GREY_A),
            label(rf"correlation \ {w['corr']:.2f}", font_size=24, color=MONEY),
            label(rf"slope \ {w['slope']:.2f}; \\ net of output growth \ {w['slope_net']:.2f}", font_size=21,
                  color=E.ACCENT),
            label(r"McCandless and Weber, \ 1995: \\ 110 countries, \ 30 years: \\ the same picture", font_size=18,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"World Bank, \ WDI: \ broad money growth and CPI inflation, \ annual averages of logs",
                       corner=DR, font_size=12)
        with self.voiceover(
            "Here is the theory on the world's data. <bookmark mark='a'/> Each dot is a country: its average growth "
            "of broad money from 1990 to 2024, against its average inflation, on log scales. "
            f"<bookmark mark='b'/> The correlation across {w['n']} countries is {w['corr']:.2f}. "
            f"<bookmark mark='c'/> The slope is {w['slope']:.2f}: a country whose money grew ten points faster had "
            "about ten points more inflation. Allowing for output growth, it is almost exactly one. Japan sits at "
            "the bottom left; Angola and Brazil are far up to the right. <bookmark mark='d'/> George McCandless and Warren "
            "Weber drew the same picture in 1995, for a hundred and ten countries over thirty years. Milton Friedman "
            "and Anna Schwartz's monetary history of the United States, in 1963, had found it in a century of "
            "American data. In the long run, inflation is a monetary phenomenon."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(diag), FadeIn(tag), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.01),
                      run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(names))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def short_run(self):
        w = load("world")
        rows = VGroup(
            label(r"but not year by year", font_size=30, color=E.ACCENT),
            label(rf"in {commas(w['annual_n'])} country-years with inflation below 10\%:", font_size=23,
                  color=GREY_A),
            label(rf"the correlation of money growth with the same year's inflation: \ {w['annual_corr']:.2f}",
                  font_size=26, color=PRICE),
            label(r"velocity moves; \ output moves; \ prices adjust slowly \ (Part 30)", font_size=23, color=GREY_A),
            label(r"the series' fact: \ across countries and decades, \ inflation tracks money growth; \ over a year "
                  r"or two, \ it does not", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = data_tag(r"World Bank, \ WDI", corner=DR, font_size=12)
        with self.voiceover(
            "But only in the long run. <bookmark mark='a'/> Take every year in every country where inflation was "
            "below ten percent, "
            f"{w['annual_n']:,} country-years. <bookmark mark='b'/> The correlation between money growth and the "
            f"same year's inflation is only {w['annual_corr']:.2f}. <bookmark mark='c'/> Over a year or two, "
            "velocity moves, output moves, and prices adjust slowly, so money and prices drift apart; Part thirty "
            "explains why prices are sticky. <bookmark mark='d'/> That is the series' fact: across countries and "
            "decades, inflation tracks money growth; over a year or two, it does not."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def us(self):
        u = load("us_money")
        ax = plane([1959, 2027], [1.0, 2.3], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[1960, 1980, 2000, 2020], yticks=[1.0, 1.5, 2.0], ylabel=r"velocity of M2: \ nominal "
                   r"GDP $\div$ M2", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=16)
        line_ = path(ax, u["v_t"], u["v"], color=MONEY, width=3, smooth=False)
        side = VGroup(
            label(rf"1959: \ {u['v_first']:.2f}", font_size=21, color=MONEY),
            label(rf"peak: \ {u['v_max']:.2f} \ in {u['v_max_when'][:4]}", font_size=21, color=MONEY),
            label(rf"now: \ {u['v_last']:.2f}", font_size=21, color=MONEY),
            label(r"velocity is not a constant: \\ it moves with interest rates, \\ financial innovation and fear",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Federal Reserve Bank of St.\ Louis, \ velocity of M2, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "And velocity is not a constant of nature. Here is American M2's velocity: nominal GDP divided by the "
            f"stock of broad money. <bookmark mark='a'/> In 1959, each dollar of M2 was spent about {u['v_first']:.1f} "
            f"times a year on output. <bookmark mark='b'/> It rose to about {u['v_max']:.1f} by {u['v_max_when'][:4]}, "
            "as interest rates and new financial products made holding money costlier. <bookmark mark='c'/> Then it "
            f"fell, to about {u['v_last']:.1f} now, with the low interest rates of the 2010s and the cash piles of the "
            "pandemic. <bookmark mark='d'/> Velocity moves with interest rates, innovation and fear: chapter nine "
            "asks why people hold money at all."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(line_), run_time=2)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
