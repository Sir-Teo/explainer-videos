from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403

EDU = (r"school", r"some college", r"a degree")


class Marriage(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Marriage as a matching market", r"Who marries whom, and what does each match produce?",
             "Chapter five. Marriage as a matching market.", lit={1973: r"Becker", 2006: r"Choo and Siow"},
             scale=("household", "nation"), horizon=("a decade",))
        self.becker()
        self.market()
        self.surplus()
        self.shifts()

    def becker(self):
        tab = VGroup()
        vals = ((10, 6), (6, 3))
        for i in range(2):
            for j in range(2):
                sq = Square(side_length=1.3, stroke_color=GREY_B, stroke_width=1.5, fill_color=CHILD,
                            fill_opacity=0.12 + 0.06 * vals[i][j]).move_to(np.array([-3.5 + 1.4 * j, 0.9 - 1.4 * i, 0]))
                tab.add(VGroup(sq, label(f"{vals[i][j]}", font_size=30, color=WHITE).move_to(sq)))
        rl = VGroup(label(r"his skill \\ high", font_size=18, color=MEN).next_to(tab[0], LEFT, buff=0.2),
                    label(r"low", font_size=18, color=MEN).next_to(tab[2], LEFT, buff=0.2))
        cl = VGroup(label(r"hers \\ high", font_size=18, color=WOMEN).next_to(tab[0], UP, buff=0.2),
                    label(r"low", font_size=18, color=WOMEN).next_to(tab[1], UP, buff=0.2))
        right = VGroup(
            label(r"what a couple produces together", font_size=22, color=WHITE),
            label(r"sorted: \ high with high, \ low with low: \ $10 + 3 = 13$", font_size=22, color=GAIN),
            label(r"mixed: \ $6 + 6 = 12$", font_size=22, color=REGULAR),
            label(r"when traits are complements, \\ like marries like", font_size=22, color=E.ACCENT),
            label(r"when they substitute \\ (one earns, \ one keeps house), \\ opposites attract", font_size=20,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 2.6)
        tag = published_tag(r"Becker, \ JPE (1973)", corner=DR, font_size=11)
        with self.voiceover(
            "In 1973 Becker treated marriage as a market in which men and women choose partners, and the gains from "
            "a match are shared. <bookmark mark='a'/> Suppose a couple's output, everything a household makes, "
            "depends on both partners' skills, and that the skills are complements: a high-skilled pair makes ten, "
            "a mixed pair six, a low-skilled pair three. <bookmark mark='b'/> Sorting, high with high and low with "
            "low, makes thirteen in all; <bookmark mark='c'/> mixing makes twelve. <bookmark mark='d'/> So the "
            "market sorts: like marries like, the same supermodularity that drove the stable matchings of Part "
            "seventeen. <bookmark mark='e'/> If instead traits substitute, as when one partner earns and the other "
            "keeps house, the market pairs opposites. Which is true is a question for data."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rl), FadeIn(cl), FadeIn(right[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tab], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(right[1]), Indicate(VGroup(tab[0], tab[3]), color=WHITE, scale_factor=1.05))
            vo.wait_until("c")
            self.play(FadeIn(right[2]), Indicate(VGroup(tab[1], tab[2]), color=WHITE, scale_factor=1.05))
            vo.wait_until("d")
            self.play(FadeIn(right[3]))
            vo.wait_until("e")
            self.play(FadeIn(right[4]))
        self.clear_scene()

    def _grid(self, mu, sm, sw, origin, cell=1.05, font=19, peak=None):
        mu = np.asarray(mu, float)
        peak = peak or mu.max()
        g = VGroup()
        for i in range(3):
            for j in range(3):
                sq = Square(side_length=cell, stroke_color=GREY_B, stroke_width=1.2, fill_color=CHILD,
                            fill_opacity=0.08 + 0.6 * mu[i, j] / peak).move_to(origin + np.array([j * cell,
                                                                                                   -i * cell, 0]))
                g.add(VGroup(sq, label(f"{mu[i, j]:,.0f}".replace(",", "{,}"), font_size=font,
                                       color=WHITE).move_to(sq)))
        singles_m = VGroup(*[label(f"{x:,.0f}".replace(",", "{,}"), font_size=font - 2, color=MEN).move_to(
            origin + np.array([3 * cell + 0.15, -i * cell, 0])) for i, x in enumerate(sm)])
        singles_w = VGroup(*[label(f"{x:,.0f}".replace(",", "{,}"), font_size=font - 2, color=WOMEN).move_to(
            origin + np.array([j * cell, -3 * cell + 0.25, 0])) for j, x in enumerate(sw)])
        return g, singles_m, singles_w

    def market(self):
        M = load("marriage")
        S = M["sample"]
        origin = np.array([-4.2, 1.4, 0])
        g, sm, sw = self._grid(S["mu"], S["single_men"], S["single_women"], origin)
        rows = VGroup(*[label(e, font_size=16, color=MEN).next_to(g[3 * i], LEFT, buff=0.15) for i, e in
                        enumerate(EDU)])
        cols = VGroup(*[label(e, font_size=16, color=WOMEN).next_to(g[j], UP, buff=0.15) for j, e in
                        enumerate(EDU)])
        hm = label(r"men", font_size=18, color=MEN).next_to(rows, LEFT, buff=0.2)
        hw = label(r"women", font_size=18, color=WOMEN).next_to(cols, UP, buff=0.15)
        hs = VGroup(label(r"single", font_size=15, color=MEN).next_to(sm[0], UP, buff=0.2),
                    label(r"single", font_size=15, color=WOMEN).next_to(sw[0], LEFT, buff=0.25))
        side = VGroup(
            label(rf"{sum(M['men']):,} men and {sum(M['women']):,} women \\ by schooling".replace(",", "{,}"),
                  font_size=18, color=WHITE),
            label(rf"the diagonal: \ {M['sorting']:.2f} times \\ what chance would give", font_size=18,
                  color=CHILD),
            label(r"Choo and Siow: \ the counts \\ alone reveal the gains", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(RIGHT * 3.6 + UP * 0.6)
        eq = MathTex(r"\mu_{ij} = \sqrt{\mu_{i0}\,\mu_{0j}}\; e^{\Phi_{ij}/2}", font_size=36, color=THEORY).next_to(
            side, DOWN, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the Island's marriage market. <bookmark mark='a'/> Men and women by schooling, school only, some "
            "college, or a degree, and the number of marriages between each pair of types, with those who stay "
            "single at the edges. <bookmark mark='b'/> The diagonal is heavy: like marries like, "
            f"{M['sorting']:.2f} times as often as if couples formed at random. <bookmark mark='c'/> Eugene Choo and "
            "Aloysius Siow showed in 2006 that counts like these reveal the gains from each kind of match. If tastes "
            "for particular partners vary at random, the number of marriages between two types, relative to the "
            "number who stay single on each side, grows with the joint surplus of that match. <bookmark mark='d'/> "
            "So the surplus of every pairing can be read off a census table."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows), FadeIn(cols), FadeIn(hm), FadeIn(hw), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in g], lag_ratio=0.15), run_time=2.0)
            self.play(FadeIn(sm), FadeIn(sw), FadeIn(hs))
            vo.wait_until("b")
            self.play(Indicate(VGroup(g[0], g[4], g[8]), color=WHITE, scale_factor=1.05), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Write(eq), run_time=1.5)
            vo.wait_until("d")
            self.play(Indicate(eq, color=WHITE))
        self.clear_scene()

    def surplus(self):
        M = load("marriage")
        phi = np.array(M["phi"])
        hat = np.array(M["sample"]["phi_hat"])
        head = label(r"the gains from each match: \ planted, \ and read from the counts", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        tabs = VGroup()
        for t, mat, col in ((r"planted in the Island", phi, GREY_A), (r"estimated from one census", hat, CHILD)):
            g = VGroup()
            for i in range(3):
                for j in range(3):
                    v = mat[i, j]
                    sq = Square(side_length=0.95, stroke_color=GREY_B, stroke_width=1.2,
                                fill_color=GAIN if v > 0 else LOSS, fill_opacity=min(abs(v) / 2.2, 0.8)).move_to(
                        np.array([j * 0.95, -i * 0.95, 0]))
                    g.add(VGroup(sq, label(f"{v:+.2f}".replace("-", "{-}"), font_size=18, color=WHITE).move_to(sq)))
            tabs.add(VGroup(label(t, font_size=20, color=col).next_to(g, UP, buff=0.3), g))
        tabs.arrange(RIGHT, buff=1.4).move_to(UP * 0.1)
        rl = VGroup(*[label(e, font_size=15, color=MEN).next_to(tabs[0][1][3 * i], LEFT, buff=0.15) for i, e in
                      enumerate(EDU)])
        foot = VGroup(
            label(r"rows: \ his schooling; \ columns: \ hers; \ green: \ a gain over staying single", font_size=19,
                  color=GREY_A),
            label(r"Choo and Siow, \ on US censuses: \ the gains of marriage for young adults fell in the 1970s, "
                  r"\ partly with legal abortion", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.FAMILY_49.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Here is the check. <bookmark mark='a'/> On the left, the surplus of each kind of match planted in the "
            "Island: largest for two graduates, negative for a graduate and someone with school only. <bookmark "
            "mark='b'/> On the right, the surplus read back from one census of the Island's marriages, using only "
            "the counts. It is close, within the noise of a finite sample. <bookmark mark='c'/> Choo and Siow did "
            "this with American censuses, and found that the gains to marriage for young adults fell during the "
            "1970s, partly as abortion became legal and the cost of a pregnancy outside marriage fell."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(foot[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(tabs[0]), FadeIn(rl), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(tabs[1]), run_time=1.5)
            self.play(Indicate(tabs[1][1][8], color=WHITE), Indicate(tabs[0][1][8], color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(foot[1], shift=UP * 0.1))
        self.clear_scene()

    def shifts(self):
        M = load("marriage")
        b, mm = M["eq"], M["more_men"]
        db, de = M["deg_base"], M["deg_ed"]
        ax = plane([-0.5, 5.5], [0, 1.0], center=LEFT * 1.4 + DOWN * 0.4, x_length=8.6, y_length=4.2, xticks=[],
                   yticks=[0, 0.25, 0.5, 0.75, 1.0], ylabel=r"share", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        groups = VGroup()
        for i, (nm, v0, v1, col) in enumerate((
                (r"men \\ married", b["married_share_men"], mm["married_share_men"], MEN),
                (r"women \\ married", b["married_share_women"], mm["married_share_women"], WOMEN),
                (r"women with \\ a degree, \\ single", db["deg_women_single"], de["deg_women_single"], CHILD))):
            x = 2.0 * i + 0.5
            pair = VGroup()
            for dx, v, op in ((-0.35, v0, 0.45), (0.35, v1, 0.9)):
                p0, p1 = ax.ax.c2p(x + dx - 0.3, 0), ax.ax.c2p(x + dx + 0.3, v)
                r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                              fill_opacity=op).move_to((p0 + p1) / 2)
                pair.add(VGroup(r, label(rf"{100 * v:.0f}\%", font_size=15, color=WHITE).next_to(r, UP, buff=0.05)))
            groups.add(VGroup(pair, label(nm, font_size=16, color=col).next_to(ax.ax.c2p(x, 0), DOWN, buff=0.2)))
        side = VGroup(
            label(r"faint: \ today's Island", font_size=17, color=GREY_A),
            label(r"a fifth more men \\ (as where sons were \\ preferred): \ men lose", font_size=17, color=MEN),
            label(r"more women than men \\ with degrees: \ more \\ of them stay single \\ or marry down", font_size=17,
                  color=CHILD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Because the model is an equilibrium, it can answer what-ifs. <bookmark mark='a'/> Give the Island a "
            "fifth more men in every group, as in countries where sons were preferred and daughters went unborn. "
            f"The share of men who marry falls from {100 * b['married_share_men']:.0f} to "
            f"{100 * mm['married_share_men']:.0f} percent, <bookmark mark='b'/> and the share of women rises, from "
            f"{100 * b['married_share_women']:.0f} to {100 * mm['married_share_women']:.0f}: the scarce side of a "
            "market does better. <bookmark mark='c'/> Or let women's schooling outrun men's, as it has in most rich "
            "countries, so that women with degrees far outnumber men with degrees. The share of graduate women "
            f"who stay single rises from {100 * db['deg_women_single']:.0f} to "
            f"{100 * de['deg_women_single']:.0f} percent. The frontier chapter returns to markets like these."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(groups[i][1]), *[GrowFromEdge(p_[0], DOWN) for p_ in groups[i][0]],
                          *[FadeIn(p_[1]) for p_ in groups[i][0]], FadeIn(side[min(i + 1, 2)]) if i != 1 else
                          Indicate(groups[0], color=WHITE, scale_factor=1.03), run_time=1.5)
        self.clear_scene()
