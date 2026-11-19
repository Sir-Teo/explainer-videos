from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403

LASC, COLIC, PAAC = E.ACCENT, HICKS, SUB


class Living(VoiceoverScene):
    def construct(self):
        card(self, 9, r"The cost of living as a welfare problem", r"How much more money does a household need when "
             r"prices change, and what does a price index miss?", "Chapter nine. The cost of living as a welfare "
             "problem.", scale=("household", "nation"))
        self.konus()
        self.sigma()
        self.new_goods()
        self.boskin()

    def bars(self, vals, cols, names, center, width=4.6, height=3.6, lo=0.6, hi=1.0, fmt="{:.3f}"):
        from explainer.ai.viz import axes

        ax = axes([0, len(vals)], [lo, hi], x_length=width, y_length=height, xticks=None,
                  yticks=list(np.round(np.linspace(lo, hi, 5), 2)), font_size=16, yfmt=lambda v: f"{v:.2f}",
                  center=center)
        a = ax.ax
        g = VGroup(ax)
        for k, (v, c, n) in enumerate(zip(vals, cols, names)):
            r = Polygon(a.c2p(k + 0.18, lo), a.c2p(k + 0.82, lo), a.c2p(k + 0.82, v), a.c2p(k + 0.18, v),
                        stroke_width=0, fill_color=c, fill_opacity=0.85)
            t = label(fmt.format(v), font_size=21, color=c).next_to(r, UP, buff=0.06)
            nm = label(n, font_size=18, color=GREY_A).next_to(a.c2p(k + 0.5, lo), DOWN, buff=0.12)
            g.add(VGroup(r, t, nm))
        return g

    def konus(self):
        lv = load("living")
        bo, rise = lv["bo"], lv["rise"]
        head = VGroup(label(r"Konüs (1924): \ the true cost-of-living index", font_size=32, color=COLIC),
                      MathTex(r"\frac{e(p_1, u)}{e(p_0, u)}", font_size=48, color=COLIC)).arrange(RIGHT, buff=0.5)
        head.to_edge(UP, buff=0.45)
        sub = label(r"the money needed to stay as well off, \ after over before", font_size=24,
                    color=GREY_A).next_to(head, DOWN, buff=0.2)
        names = (r"Laspeyres", r"true", r"Paasche")
        b1 = self.bars([bo["laspeyres"], bo["coli0"], bo["paasche"]], [LASC, COLIC, PAAC], names,
                       LEFT * 3.4 + DOWN * 0.9, lo=0.6, hi=0.8)
        b2 = self.bars([rise["laspeyres"], rise["coli"], rise["paasche"]], [LASC, COLIC, PAAC], names,
                       RIGHT * 2.0 + DOWN * 0.9, lo=1.1, hi=1.35)
        t1 = label(r"fish \$10 $\to$ \$6", font_size=24, color=NEWB).next_to(b1, UP, buff=0.15)
        t2 = label(r"fish \$10 $\to$ \$15", font_size=24, color=NEWB).next_to(b2, UP, buff=0.15)
        side = VGroup(label(r"Laspeyres: \\ the old basket \\ at new prices", font_size=21, color=LASC),
                      label(r"never below \\ the truth", font_size=21, color=GREY_A),
                      label(r"Paasche: \\ the new basket", font_size=21, color=PAAC),
                      label(r"never above it", font_size=21, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.2)
        side.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.8)
        tag = agora_tag(r"computed: Bo's Cobb--Douglas tastes", corner=DR, font_size=13)
        with self.voiceover(
            "Part three built price indices from baskets. This part can say what they're for. "
            "<bookmark mark='a'/> In 1924 the Russian economist Alexander Konüs defined the true cost-of-living "
            "index: the money a household needs at the new prices to be exactly as well off as before, divided by "
            "what it needed at the old prices. It's a ratio of expenditure functions. <bookmark mark='b'/> For Bo, "
            "when fish fall from ten dollars to six, the true index is nought point seven three six: he needs about "
            "a quarter less money. The Laspeyres index, which prices his old basket, says nought point seven six; "
            "the Paasche index, which prices his new one, says nought point seven one four. <bookmark mark='c'/> "
            "When fish rise to fifteen dollars, the same order: Laspeyres above the truth, Paasche below. "
            "<bookmark mark='d'/> That's the concave expenditure function from chapter five. A fixed basket ignores "
            "substitution, so it always overstates what a household needs, and the gap is the substitution bias."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("b")
            self.play(FadeIn(b1), FadeIn(t1))
            vo.wait_until("c")
            self.play(FadeIn(b2), FadeIn(t2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.4), run_time=2)
        self.clear_scene()

    def sigma(self):
        lv = load("living")
        rows = [(r"$\sigma = 0.3$: \ fish and coconuts \\ hard to swap", lv["ces_low"]),
                (r"$\sigma = 1$: \ Bo", lv["bo"]),
                (r"$\sigma = 3$: \ easy to swap", lv["ces_high"])]
        grp = VGroup()
        for name, r in rows:
            gap = r["laspeyres"] / r["coli0"] - 1
            grp.add(VGroup(label(name, font_size=24), label(rf"Laspeyres {r['laspeyres']:.3f}", font_size=24,
                                                            color=LASC),
                           label(rf"true {r['coli0']:.3f}", font_size=24, color=COLIC),
                           label(rf"overstates by {100 * gap:.1f}\%", font_size=24, color=E.ACCENT)).arrange(
                RIGHT, buff=0.55))
        grp.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"fish \$10 $\to$ \$6: \ the bias grows with the ease of substitution", font_size=30).to_edge(
            UP, buff=0.7)
        foot = label(r"$\sigma$: \ the elasticity of substitution (Part 5's CES)", font_size=22,
                     color=GREY_B).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "How big is the bias? It depends on how easily people substitute. <bookmark mark='a'/> With tastes "
            "where fish and coconuts are hard to swap, a CES elasticity of nought point three, the fixed basket "
            "overstates the true cost of living by about one percent. <bookmark mark='b'/> With Bo's Cobb–Douglas "
            "tastes, by three percent. <bookmark mark='c'/> And where the goods are easy to swap, by almost ten. The "
            "more freely people respond to prices, the worse a fixed basket measures what they need."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            for mk, r_ in zip("abc", grp):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()

    def new_goods(self):
        ch = load("living")["cheerios"]
        from explainer.ai.viz import axes

        ax = axes([0, 2.2], [0, 8], x_length=5.4, y_length=4.8, xticks=None, yticks=[0, 2, 4, 6, 8],
                  xlabel=r"quantity bought", ylabel=r"price (\$)", font_size=18, center=LEFT * 3.4 + DOWN * 0.35)
        a = ax.ax
        v, p = ch["virtual"], ch["price"]
        q = (v - p) / v * 2.0                        # a straight line from (0, v) through (q, p), schematic
        dem = Line(a.c2p(0, v), a.c2p(2.0, 0), color=WHITE, stroke_width=4)
        tri = Polygon(a.c2p(0, v), a.c2p(0, p), a.c2p(q, p), stroke_width=0, fill_color=HICKS, fill_opacity=0.45)
        pl = DashedLine(a.c2p(0, p), a.c2p(q, p), color=GREY_B, stroke_width=2)
        vl = label(rf"virtual price \${v:.2f}", font_size=21, color=E.ACCENT).next_to(a.c2p(0, v), RIGHT, buff=0.2)
        pp = label(rf"actual \${p:.2f}", font_size=21, color=GREY_A).next_to(a.c2p(q, p), RIGHT, buff=0.15)
        sch = label(r"schematic: \ a straight line", font_size=16, color=GREY_B).next_to(ax, DOWN, buff=0.1)
        side = VGroup(
            label(r"Hicks (1940): \ before a good exists, \\ its price is the one at which \\ nobody would buy it",
                  font_size=24),
            label(r"Apple-Cinnamon Cheerios, \ 1989", font_size=27, color=E.ACCENT),
            label(rf"virtual price \${v:.2f}, \ about twice \\ the actual \${p:.2f}", font_size=24),
            label(rf"consumers' gain: \ about \${ch['cs_year']:.1f} million a year \\ in the US, \ "
                  rf"{100 * ch['per_person']:.0f} cents a person", font_size=24, color=HICKS),
            label(rf"ignoring new brands, \ the CPI for cereal \\ may be overstated by about {100 * ch['cpi_over']:.0f}\%",
                  font_size=24, color=E.ACCENT),
            label(rf"{ch['brands']} new brands, 1980--92, \ among about {ch['existing']}", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Hausman, in Bresnahan and Gordon (eds.), The Economics of New Goods (1997)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "A fixed basket has a second blind spot: goods that didn't exist when the basket was chosen. "
            "<bookmark mark='a'/> John Hicks suggested in 1940 how to price them. Before a good is sold, its price "
            "is, in effect, the price at which nobody would buy it, the virtual price. When it arrives, its price "
            "falls from there to the shelf price, and the gain is the triangle under the demand curve. "
            "<bookmark mark='b'/> Jerry Hausman did it for one breakfast cereal, Apple-Cinnamon Cheerios, launched "
            "by General Mills in 1989. <bookmark mark='c'/> From scanner data he estimated a virtual price of about "
            "seven dollars, twice the actual price of about three fifty, <bookmark mark='d'/> and a gain to American "
            "consumers of about seventy-eight million dollars a year, thirty-one cents a person. "
            "<bookmark mark='e'/> Leaving new brands out, he concluded, the consumer price index for cereal may be "
            "overstated by about a quarter. <bookmark mark='f'/> And cereal makers launched a hundred and ninety new "
            "brands between 1980 and 1992."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(sch))
            vo.wait_until("a")
            self.play(Create(dem), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(vl), FadeIn(pl), FadeIn(pp), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(tri), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def boskin(self):
        b = load("living")["boskin"]
        parts = [(r"substitution", b["substitution"], LASC), (r"outlets", b["outlets"], GREY_B),
                 (r"new products \\ and quality", b["new_quality"], HICKS)]
        from explainer.ai.viz import axes

        ax = axes([0, 3], [0, 0.8], x_length=6.0, y_length=4.2, xticks=None, yticks=[0, 0.2, 0.4, 0.6, 0.8],
                  ylabel=r"points a year", font_size=18, yfmt=lambda v: f"{v:.1f}", center=LEFT * 2.8 + DOWN * 0.4)
        a = ax.ax
        bars = VGroup()
        for k, (n, v, c) in enumerate(parts):
            r = Polygon(a.c2p(k + 0.2, 0), a.c2p(k + 0.8, 0), a.c2p(k + 0.8, v), a.c2p(k + 0.2, v), stroke_width=0,
                        fill_color=c, fill_opacity=0.85)
            bars.add(VGroup(r, label(rf"{v:.1f}", font_size=22, color=c).next_to(r, UP, buff=0.06),
                            label(n, font_size=19, color=GREY_A).next_to(a.c2p(k + 0.5, 0), DOWN, buff=0.12)))
        side = VGroup(
            label(r"the Boskin Commission, 1996", font_size=27, color=E.ACCENT),
            label(rf"the CPI overstated inflation \\ by about {b['total']:.1f} points a year \\ (range {b['lo']:.1f} to "
                  rf"{b['hi']:.1f})", font_size=24),
            label(r"substitution: \ the concave gap \\ of chapter five", font_size=23, color=LASC),
            label(r"new goods: \ virtual prices", font_size=23, color=HICKS),
            label(r"the dial (Part 3): \ later estimates \\ 0.8 to 0.9 after the reforms", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        tag = published_tag(r"Boskin et al.\ (1996), via Moulton (2018) and Gordon (2006)", corner=DR, font_size=13)
        with self.voiceover(
            "In Part three we met the Boskin Commission's verdict on the American CPI. Now its pieces are welfare "
            "theory. <bookmark mark='a'/> In 1996 the commission put the overstatement at about one point one "
            "points a year. <bookmark mark='b'/> About nought point four of that was substitution, the concave gap "
            "this part has drawn twice; a tenth was shoppers switching to cheaper stores; and the largest piece, "
            "nought point six, was new products and better quality, Hicks's virtual prices on a national scale. "
            "<bookmark mark='c'/> The Bureau of Labor Statistics changed its methods in response, and later "
            "estimates of the remaining bias are a little under one point a year. Chapter twelve shows what it "
            "changed."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.4), FadeIn(side[2]),
                      FadeIn(side[3]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
        self.clear_scene()
