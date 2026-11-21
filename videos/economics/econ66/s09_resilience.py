from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403


class Resilience(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Security against efficiency", r"How much should a firm, \ or a country, \ pay to avoid "
             r"depending on a supplier that can be cut off?", "Chapter seven. Security against efficiency.",
             lit={2023: "Alfaro and Chor"}, scale=("firm", "nation"), horizon=("a decade",))
        self.model()
        self.reallocation()

    def model(self):
        R = load("resilience")
        x = np.array(R["grid"])
        priv = 100 * np.array(R["private"])
        soc = 100 * np.array(R["social"])
        ax = plane([0, 1], [6, 21], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.2, y_length=4.8,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[6, 10, 14, 18],
                   xlabel=r"share bought from the cheap supplier that can be cut off",
                   ylabel=r"expected cost, \ \% of the input's value", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        lp = path(ax, x, priv, US, 3.0)
        ls_ = path(ax, x, soc, TARIFF, 3.0)
        mp = dot(ax, R["x_private"], 100 * float(np.interp(R["x_private"], x, priv)), US, 0.1)
        ms = dot(ax, R["x_social"], 100 * float(np.interp(R["x_social"], x, soc)), TARIFF, 0.1)
        key = legend_rows([(US, "the firm's own expected cost"), (TARIFF, "society's: the firm's plus its "
                                                                         "customers' and workers'")],
                          font_size=15).next_to(ax.ax, RIGHT, buff=0.3).shift(UP * 1.5)
        if key.width > 4.4:
            key.scale_to_fit_width(4.4).next_to(ax.ax, RIGHT, buff=0.3).shift(UP * 1.5)
        side = VGroup(
            label(rf"the firm buys {100 * R['x_private']:.0f}\% abroad", font_size=18, color=US),
            label(rf"society would choose {100 * R['x_social']:.0f}\%", font_size=18, color=TARIFF),
            label(rf"the difference: \ {R['social_at_private'] * 100 - R['social_at_social'] * 100:.2f} points "
                  r"of cost", font_size=18, color=GREY_A),
            label(r"a case for paying for diversification, \\ not for autarky", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(key, DOWN, buff=0.45).align_to(key, LEFT)
        tag = published_tag(r"Grossman, \ Helpman and Lhuillier, \ JPE 131(12) (2023); \ a model: \ "
                            r"agora.tradewar.resilience", corner=DL, font_size=12)
        with self.voiceover(
            "Resilience has a price. <bookmark mark='a'/> A firm buys an input from a cheap foreign supplier, "
            f"{100 * R['cost_gap']:.0f} percent cheaper, who is cut off with a probability of "
            f"{100 * R['p']:.0f} percent a year. A cutoff hurts more the more the firm depends on it. Here is the "
            "firm's expected cost, as it varies the share it buys abroad. <bookmark mark='b'/> It chooses about "
            f"{100 * R['x_private']:.0f} percent. <bookmark mark='c'/> But a cutoff also hurts the firm's customers "
            "and workers, who are not in its sums. Counting them, society's expected cost is the red curve, and "
            f"society would buy only {100 * R['x_social']:.0f} percent abroad. <bookmark mark='d'/> Gene Grossman, "
            "Elhanan Helpman and Hugo Lhuillier show how delicate the real case is: with some demand structures "
            "firms buy too little resilience, with others too much, and a subsidy to diversify can beat bringing "
            "production home. Note what even the simple case does not say: the right share is not zero. Security "
            "is bought at the margin, not by leaving trade."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lp), FadeIn(key[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(mp, scale=1.5), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(ls_), FadeIn(key[1]), FadeIn(ms, scale=1.5), FadeIn(side[1:3]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def reallocation(self):
        ax = plane([-0.6, 2.6], [0, 25], center=LEFT * 3.3 + DOWN * 0.4, x_length=5.2, y_length=4.6, xticks=[],
                   yticks=[0, 5, 10, 15, 20, 25], ylabel=r"China's share of US goods imports, \ \%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        vals = [21.6, 16.5, 9.0]
        b = bars(ax, [0, 1, 2], vals, [ROW, ROW, TARIFF], width=0.6)
        names = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.15)
                         for k, t in enumerate((r"2017", r"2022", r"mid-2025"))])
        nums = VGroup(*[label(rf"{v:.1f}\%" if k < 2 else r"about 9\%", font_size=16, color=ROW if k < 2 else TARIFF)
                        .next_to(bb, UP, buff=0.08) for k, (bb, v) in enumerate(zip(b, vals))])
        side = VGroup(
            label(r"who gained: \ Vietnam, \ Mexico, \ others", font_size=20, color=FREE),
            label(r"the cost: \ goods from Vietnam about 10\% dearer, \\ from Mexico about 3\%", font_size=20,
                  color=TARIFF),
            label(r"and much of it still made with Chinese parts", font_size=20, color=GREY_A),
            label(r"friend-shoring: \ less risk, \ higher prices", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(ax.ax, RIGHT, buff=0.8)
        tag = published_tag(r"Alfaro and Chor, \ Jackson Hole (2023); \ NBER WP 34490 (2025)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "The reallocation is already under way. <bookmark mark='a'/> Laura Alfaro and Davin Chor measured "
            "China's share of American goods imports: twenty-one point six percent at its peak in 2017, sixteen "
            "point five in 2022, and in their later work about nine percent by the middle of 2025, after the new "
            "tariffs. <bookmark mark='b'/> The share went to Vietnam, Mexico and others. <bookmark mark='c'/> It "
            "was not free: the unit values of what America bought from Vietnam rose about ten percent, from Mexico "
            "about three. <bookmark mark='d'/> And much of what comes from the new suppliers is still made with "
            "Chinese parts. <bookmark mark='e'/> Friend-shoring buys some security, at a price, and less of it "
            "than the bilateral numbers suggest."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(names), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(bb, DOWN) for bb in b], lag_ratio=0.4), FadeIn(nums), run_time=2.0)
            for mk, r_ in zip("bcde", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
