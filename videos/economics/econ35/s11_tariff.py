from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403


class Tariff(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Tariffs and quotas", r"Who pays a tariff, and can a country ever gain from one?",
             "Chapter nine. Tariffs and quotas.", lit={1844: r"Mill", 1906: r"Bickerdike"},
             scale=("market", "nation"), horizon=("a year",))
        self.triangles()
        self.quota()
        self.large()

    def _market(self):
        T = load("tariff")
        ax = plane([0, 80], [0, 10], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.0, y_length=4.8,
                   xticks=[0, 20, 40, 60, 80], yticks=[0, 2, 4, 6, 8, 10], xlabel=r"bolts of cloth, \ a week",
                   ylabel=r"price", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        a, b, c, d = T["a"], T["b"], T["c"], T["d"]
        qs = np.linspace(0, 80, 81)
        dem = path(ax, qs, (a - qs) / b, WHITE, 3.0, yr=(0, 10))
        sup = path(ax, qs, (qs - c) / d, CAPITAL, 3.0, yr=(0, 10))
        return T, ax, dem, sup

    def poly(self, ax, pts, color, op=0.45):
        return Polygon(*[ax.ax.c2p(x, y) for x, y in pts], stroke_width=0, fill_color=color, fill_opacity=op)

    def triangles(self):
        T, ax, dem, sup = self._market()
        S = T["small"]
        pw, p = T["pw"], S["p"]
        world = seg(ax, 0, pw, 80, pw, GREY_B, 2.0, dashed=True)
        tline = seg(ax, 0, p, 80, p, TARIFF, 2.5, dashed=True)
        A = self.poly(ax, [(0, pw), (S["S0"], pw), (S["S1"], p), (0, p)], CAPITAL)
        B = self.poly(ax, [(S["S0"], pw), (S["S1"], pw), (S["S1"], p)], TARIFF, 0.7)
        C = self.poly(ax, [(S["S1"], pw), (S["D1"], pw), (S["D1"], p), (S["S1"], p)], FISH)
        D = self.poly(ax, [(S["D1"], pw), (S["D0"], pw), (S["D1"], p)], TARIFF, 0.7)
        imp0 = DoubleArrow(ax.ax.c2p(S["S0"], pw - 0.6), ax.ax.c2p(S["D0"], pw - 0.6), color=GAIN, buff=0,
                           stroke_width=3, tip_length=0.15)
        imp1 = DoubleArrow(ax.ax.c2p(S["S1"], p + 0.6), ax.ax.c2p(S["D1"], p + 0.6), color=GAIN, buff=0,
                           stroke_width=3, tip_length=0.15)
        side = VGroup(
            label(rf"world price {pw:.0f}: \ imports {S['M0']:.0f}", font_size=19, color=GAIN),
            label(rf"a tariff of {T['t']:.0f}: \ price {p:.0f}, \ imports {S['M1']:.0f}", font_size=19, color=TARIFF),
            label(rf"shoppers lose {S['cs_loss']:.0f}", font_size=19, color=WHITE),
            label(rf"gold: \ weavers gain {S['ps_gain']:.0f}", font_size=19, color=CAPITAL),
            label(rf"blue: \ the treasury {S['revenue']:.0f}", font_size=19, color=FISH),
            label(rf"red: \ lost to no one, \ {S['dwl_production'] + S['dwl_consumption']:.0f}", font_size=19,
                  color=TARIFF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now the tool most often used to change trade: the tariff. <bookmark mark='a'/> Here is the Island's "
            "market for cloth: demand in white, the Island's own weavers' supply in gold. "
            f"<bookmark mark='b'/> At the world price of {pw:.0f}, Islanders buy {S['D0']:.0f} bolts a week and "
            f"weave {S['S0']:.0f}; the other {S['M0']:.0f} are imported. <bookmark mark='c'/> A tariff of "
            f"{T['t']:.0f} raises the price at home to {p:.0f}. Islanders buy less, weave more, and imports halve. "
            f"<bookmark mark='d'/> Shoppers lose {S['cs_loss']:.0f}: everything between the two prices, left of "
            f"demand. <bookmark mark='e'/> Weavers gain {S['ps_gain']:.0f} of it, the gold area. "
            f"<bookmark mark='f'/> The treasury collects {S['revenue']:.0f}, the blue rectangle. "
            f"<bookmark mark='g'/> And the two red triangles, {S['dwl_production'] + S['dwl_consumption']:.0f} in "
            "all, go to no one: cloth woven at home at more than it costs abroad, and cloth not bought that was "
            "worth more to buyers than it cost the world. A small country that taxes imports makes itself poorer."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(dem), Create(sup), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(world), GrowFromCenter(imp0), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(tline), FadeOut(imp0), GrowFromCenter(imp1), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(A), FadeIn(side[3]))
            vo.wait_until("f")
            self.play(FadeIn(C), FadeIn(side[4]))
            vo.wait_until("g")
            self.play(FadeIn(B), FadeIn(D), FadeIn(side[5]))
        self.clear_scene()

    def quota(self):
        T = load("tariff")
        Q = T["quota"]
        rows = VGroup(
            label(rf"a quota of {T['small']['M1']:.0f} bolts: \ the same price, \ {Q['p']:.0f}", font_size=26,
                  color=WHITE),
            label(rf"the blue rectangle, \ {Q['rent']:.0f}, \ now goes to whoever holds the licences", font_size=24,
                  color=FISH),
            label(r"if foreigners hold them, \ the Island loses that too", font_size=24, color=TARIFF),
            label(r"1981--94: \ Japan's `voluntary' limits on cars sold in America \ handed the rent to Japanese "
                  r"makers", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"the Island; \ Berry, \ Levinsohn and Pakes, \ \emph{AER} 89(3) (1999)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "A quota does the same to prices with a different owner. <bookmark mark='a'/> Limit imports to "
            f"{T['small']['M1']:.0f} bolts and the price rises to {Q['p']:.0f}, as with the tariff. "
            "<bookmark mark='b'/> But the blue rectangle is no longer tax revenue. It goes to whoever holds the "
            "right to import, <bookmark mark='c'/> and if that is foreign exporters, the Island loses it too. "
            "<bookmark mark='d'/> From 1981 Japan's car makers agreed to limit their exports to America, at "
            "America's request. American buyers paid more for Japanese cars, and much of the difference went to "
            "the Japanese firms."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def large(self):
        T = load("tariff")
        ax = plane([0, 2.5], [-8, 8], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5], yticks=[-8, -4, 0, 4, 8], xlabel=r"the tariff",
                   ylabel=r"the Island's gain, \ against free trade", xfmt=lambda v: f"{v:.1f}",
                   yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=14)
        zero = seg(ax, 0, 0, 2.5, 0, GREY_B, 1.5)
        w = path(ax, T["grid"], T["welfare"], GAIN, 3.4, yr=(-8, 8))
        opt = dot(ax, T["opt_t"], T["opt_welfare"], WHITE, 0.09)
        side = VGroup(
            label(r"if the Island is large, \\ its tariff lowers \\ the world price", font_size=18, color=WHITE),
            label(rf"the Archipelago now gets \\ {T['opt_pw']:.2f} instead of {T['pw']:.0f}", font_size=18,
                  color=ARCH),
            label(rf"the best tariff: \ {T['opt_t']:.2f}, \\ {100 * T['opt_av']:.0f}\% of the world price \\ $= 1/$ "
                  r"the foreign supply \\ elasticity", font_size=18, color=GAIN),
            label(r"it gains by making \\ its neighbour poorer, \\ and only if the \\ neighbour does not \\ "
                  r"retaliate", font_size=18, color=TARIFF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Bickerdike (1906); \ the Island, \ large", corner=DR, font_size=12)
        with self.voiceover(
            "There is one case in which a tariff can pay. <bookmark mark='a'/> Suppose the Island is large, a big "
            "enough buyer that when it buys less, the world price falls. Then part of the tariff is paid by "
            f"foreigners: <bookmark mark='b'/> the Archipelago's weavers now receive {T['opt_pw']:.2f} a bolt "
            f"instead of {T['pw']:.0f}. <bookmark mark='c'/> The green curve is the Island's gain. A small tariff "
            f"helps; the best one is {T['opt_t']:.2f}, about {100 * T['opt_av']:.0f} percent, equal to one over the "
            "elasticity of the Archipelago's export supply, as Charles Bickerdike showed in 1906. Beyond it, the "
            "triangles win again. <bookmark mark='d'/> But every unit of that gain is a loss to the neighbour, "
            "who can play the same game. Which is the subject of chapter eleven."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(w), FadeIn(side[0]), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(opt, scale=1.4), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
