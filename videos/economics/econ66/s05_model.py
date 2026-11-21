from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403


class Model(VoiceoverScene):
    def construct(self):
        card(self, 4, r"A 15\% tariff in the quantitative model", r"What does a uniform American tariff do to the "
             r"world, \ with and without retaliation?", "Chapter four. A fifteen percent tariff in the quantitative "
             "model.", lit={2008: "Dekle, Eaton and Kortum"}, scale=("nation", "world"), horizon=("a decade",))
        self.setup_world()
        self.welfare()
        self.incidence()

    def setup_world(self):
        W = load("world")
        eq = MathTex(r"\pi'_{ni} = \frac{\pi_{ni}\,(\hat w_i\,(1+t_{ni}))^{-\theta}}"
                     r"{\sum_k \pi_{nk}\,(\hat w_k\,(1+t_{nk}))^{-\theta}}", font_size=40).to_edge(UP, buff=0.6)
        rows = VGroup(
            label(r"thirteen economies: \ the twelve largest and the rest, \ CEPII's 2019 flows", font_size=21,
                  color=GREY_A),
            label(r"tariff revenue goes back to the country that collects it", font_size=21, color=PRICE),
            label(rf"the United States: \ {100 * W['us_gdp_share']:.0f}\% of world spending, \ imports "
                  rf"{100 * W['us_import_share']:.0f}\% of what it spends", font_size=21, color=US),
            label(r"deficits set to zero first, \ so they do not drive the answer", font_size=21, color=GREY_A),
            label(r"$\theta$, \ the trade elasticity: \ 2, \ 4 or 8", font_size=21, color=STATE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(eq, DOWN, buff=0.6)
        tag = published_tag(r"Dekle, \ Eaton and Kortum, \ IMF Staff Papers 55(3) (2008); \ Costinot and "
                            r"Rodr\'iguez-Clare, \ Handbook (2014); \ CEPII Gravity (2019)", corner=DL, font_size=12)
        with self.voiceover(
            "Now a tariff in the quantitative model of Part thirty-six, by exact hat algebra. <bookmark mark='a'/> "
            "Each country's spending share on each supplier changes with the supplier's wage and the tariff, raised "
            "to minus theta. <bookmark mark='b'/> The world is thirteen economies: the twelve largest and the rest, "
            "with their trade flows of 2019 from CEPII. <bookmark mark='c'/> The tariff revenue goes back to the "
            "country that collects it. <bookmark mark='d'/> The United States is about a quarter of world spending "
            f"and imports about {100 * W['us_import_share']:.0f} percent of what it spends. <bookmark mark='e'/> We "
            "set deficits to zero first, as the literature does, so that a deficit held fixed by assumption does "
            "not drive the answer; and we try three trade elasticities, because the evidence of chapter one says "
            "it is small in the short run and larger later."
        ) as vo:
            self.play(Write(eq), FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def welfare(self):
        S = load("scenarios")
        rows = S["rows"]
        thetas = sorted({r["theta"] for r in rows})
        ax = plane([-0.5, 5.5], [-0.5, 0.65], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.8,
                   xticks=[], yticks=[-0.4, -0.2, 0, 0.2, 0.4, 0.6], ylabel=r"real income, \ \% change",
                   yfmt=lambda v: f"{v:.1f}".replace("-", "{-}"), font_size=14)
        zero = seg(ax, -0.5, 0, 5.5, 0, GREY_C, 1.5)
        groups = VGroup()
        labels = VGroup()
        k = 0
        for retal in (False, True):
            for th in thetas:
                r = [x for x in rows if x["theta"] == th and x["retaliation"] == retal][0]
                vals = [100 * r["us"], 100 * r["partners"]]
                b = bars(ax, [k - 0.18, k + 0.18], vals, [US, ROW], width=0.34)
                groups.add(b)
                labels.add(label(rf"$\theta = {th:.0f}$", font_size=15, color=THETA[f"{th:.1f}"]).next_to(
                    ax.ax.c2p(k, -0.5), DOWN, buff=0.12))
                k += 1
        hdr = VGroup(label(r"no retaliation", font_size=18, color=FREE).move_to(ax.ax.c2p(1, 0.6)),
                     label(r"retaliation in kind", font_size=18, color=TARIFF).move_to(ax.ax.c2p(4, 0.6)))
        sep = vline(ax, 2.5, -0.5, 0.65, GREY_C)
        key = legend_rows([(US, "the United States"), (ROW, "its partners (weighted by size)")],
                          font_size=16).next_to(ax.ax, RIGHT, buff=0.3).shift(UP * 1.4)
        r4 = [x for x in rows if x["theta"] == 4.0]
        n4, y4 = r4[0], r4[1]
        side = VGroup(
            label(rf"$\theta = 4$, \ no retaliation: \ US {100 * n4['us']:+.2f}\%", font_size=17, color=US),
            label(rf"with retaliation: \ US {100 * y4['us']:+.2f}\%".replace("-", "{-}"), font_size=17, color=US),
            label(rf"US imports fall {100 * n4['imports_fall']:.0f}\% \ ({100 * y4['imports_fall']:.0f}\% with "
                  r"retaliation)", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(key, DOWN, buff=0.4).align_to(key, LEFT)
        tag = island_tag(r"computed: \ agora.tradewar.tariff\_scenarios", corner=DL, font_size=12)
        with self.voiceover(
            "Impose a uniform fifteen percent tariff on all American imports. <bookmark mark='a'/> With no "
            f"retaliation and theta of four, American real income rises {100 * n4['us']:.2f} percent: the terms "
            f"of trade again. The partners lose {-100 * n4['partners']:.2f} percent. The gain is largest when "
            "trade responds least, because then foreigners cannot escape the tax. <bookmark mark='b'/> Now let "
            "every partner answer with fifteen percent on American goods. <bookmark mark='c'/> America's gain "
            f"becomes a loss: {100 * y4['us']:+.2f} percent at theta of four, and larger when trade is more "
            "responsive. <bookmark mark='d'/> American imports fall by "
            f"{100 * n4['imports_fall']:.0f} percent without retaliation and {100 * y4['imports_fall']:.0f} with "
            "it. The numbers are small as shares of income, as Fajgelbaum and coauthors found, because trade is a "
            "modest share of a large economy; they are large for the industries and places that trade."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(sep), FadeIn(hdr[0]), FadeIn(key), FadeIn(tag),
                      FadeIn(labels[:3]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if b_.get_center()[1] > ax.ax.c2p(0, 0)[1] else UP)
                                    for g_ in groups[:3] for b_ in g_], lag_ratio=0.15), FadeIn(side[0]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(hdr[1]), FadeIn(labels[3:]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if b_.get_center()[1] > ax.ax.c2p(0, 0)[1] else UP)
                                    for g_ in groups[3:] for b_ in g_], lag_ratio=0.15), FadeIn(side[1]),
                      run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def incidence(self):
        S = load("scenarios")
        r4 = [x for x in S["rows"] if x["theta"] == 4.0 and not x["retaliation"]][0]
        rows = VGroup(
            VGroup(label(rf"{100 * r4['absorbed']:.0f}\%", font_size=54, color=ROW),
                   label(r"of the tariff borne by foreigners in the model, \\ through lower wages and prices "
                         r"abroad, \ in the long run", font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.4),
            VGroup(label(r"$\approx 0$", font_size=54, color=PRICE),
                   label(r"borne by foreigners in the data, \ 2018--19 and 2025, \\ in the first year or two",
                         font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(UP * 0.6)
        why = VGroup(
            label(r"why: \ most imports are priced in dollars and sticky in the short run \ (Part 34);", font_size=19,
                  color=GREY_A),
            label(r"trade responds slowly: \ an elasticity of 0.76 in the first year, \ about 2 after a decade",
                  font_size=19, color=GREY_A),
            label(r"the terms-of-trade gain, \ if it comes, \ comes late", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(rows, DOWN, buff=0.6)
        tag = published_tag(r"Boehm, \ Levchenko and Pandalai-Nayar, \ AER 113(4) (2023); \ Gopinath, \ Itskhoki "
                            r"and Rigobon, \ AER 100(1) (2010)", corner=DL, font_size=12)
        with self.voiceover(
            "Who pays, in the model? <bookmark mark='a'/> In the long run, about "
            f"{100 * r4['absorbed']:.0f} percent of the tariff is borne abroad, through lower wages and prices in "
            "the countries America buys from. <bookmark mark='b'/> In the data, in the first year or two of both "
            "rounds, foreigners bore almost none of it. <bookmark mark='c'/> The two are not in contradiction. Most "
            "American imports are priced in dollars, and those prices are sticky, as Part thirty-four showed; and "
            "trade responds slowly: Christoph Boehm, Andrei Levchenko and Nitya Pandalai-Nayar estimate an "
            "elasticity of about three quarters in the first year and about two after a decade. The "
            "terms-of-trade gain the optimal-tariff argument relies on, if it comes, comes late, and only if "
            "nobody retaliates."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.1))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(w_) for w_ in why], lag_ratio=0.5), run_time=2.0)
        self.clear_scene()
