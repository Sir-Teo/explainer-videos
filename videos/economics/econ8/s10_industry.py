from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403


class Industry(VoiceoverScene):
    def construct(self):
        card(self, 8, r"The industry: \ entry, exit and rents", r"With free entry, how many boatyards will the Island "
             r"have, and who earns what?", "Chapter eight. The industry: entry, exit and rents.",
             scale=("firm", "market"), horizon=("a year", "a decade"))
        self.free_entry()
        self.rents()

    def free_entry(self):
        i = load("industry")
        s = i["same"]
        qs = np.array(i["qs"])
        ax = plane([0, 20], [0, 2500], center=LEFT * 4.2 + DOWN * 0.3, x_length=4.2, y_length=4.6,
                   xticks=[0, 10, 20], yticks=[0, 1000, 2000], xlabel=r"one yard's boats", ylabel=r"\$ a boat",
                   font_size=15)
        bx = plane([0, 400], [0, 2500], center=RIGHT * 0.6 + DOWN * 0.3, x_length=4.2, y_length=4.6,
                   xticks=[0, 200, 400], yticks=[0, 1000, 2000], xlabel=r"the Island's boats",
                   ylabel=r"\$ a boat", font_size=15)
        atc = path(ax, qs, i["atc"], color=ATC, width=3, yr=(0, 2500))
        mc = path(ax, qs, i["mc"], color=MC, width=2.5, yr=(0, 2500))
        pl = DashedLine(ax.ax.c2p(0, s["price"]), ax.ax.c2p(20, s["price"]), color=PRICE, stroke_width=2)
        P = Dot(ax.ax.c2p(s["q"], s["price"]), radius=0.08, color=PRICE)
        a, b = i["demand"]
        dem = Line(bx.ax.c2p(0, a / b), bx.ax.c2p(a, 0), color=LAB, stroke_width=3)
        names = VGroup(
            label(r"$MC$", font_size=17, color=MC).next_to(ax.ax.c2p(20, i["mc"][-1]), UP, buff=0.06),
            label(r"$ATC$", font_size=17, color=ATC).next_to(ax.ax.c2p(20, i["atc"][-1]), DOWN, buff=0.1),
            label(r"demand", font_size=17, color=LAB).next_to(bx.ax.c2p(60, a / b - 300), RIGHT, buff=0.1))
        lrs = DashedLine(bx.ax.c2p(0, s["price"]), bx.ax.c2p(400, s["price"]), color=PRICE, stroke_width=3)
        Q = Dot(bx.ax.c2p(s["Q"], s["price"]), radius=0.08, color=PRICE)
        side = VGroup(
            label(r"every yard has the same costs; \\ anyone may open one", font_size=23),
            label(rf"profits draw entrants until the price \\ falls to the bottom of average cost: "
                  rf"\${s['price']:,.0f}".replace(",", "{,}"), font_size=23, color=PRICE),
            label(rf"each yard builds {s['q']:.1f} boats; \\ the Island buys {s['Q']:.0f}: \\ about "
                  rf"{s['firms']:.0f} yards", font_size=23),
            label(r"zero profit: \ owners earn what they \\ could earn elsewhere, \ no more", font_size=22,
                  color=GREY_A),
            label(r"more demand brings more yards, \\ not a higher price: \ a flat long-run supply", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "One yard is a firm; many make an industry. <bookmark mark='a'/> Suppose every yard has the same costs, "
            "and anyone can open one. <bookmark mark='b'/> While yards make a profit, new ones open, and the extra "
            "boats push the price down, until it reaches the bottom of average cost: a thousand and ninety-four "
            "dollars. <bookmark mark='c'/> Each yard builds its efficient scale, about nine boats a month; at that "
            "price the Island buys a hundred and eighty-one; so there's room for about twenty yards. "
            "<bookmark mark='d'/> At that point profit is zero, which in economics means owners earn exactly what "
            "their money and time could earn elsewhere. <bookmark mark='e'/> And if demand rises, the price rises only "
            "until new yards open: in the long run, supply is flat at the bottom of average cost."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(bx), FadeIn(tag), Create(atc), Create(mc), Create(dem),
                      FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(pl), FadeIn(P), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lrs), FadeIn(Q), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def rents(self):
        i = load("industry")
        h = i["het"]
        prof = np.array(i["het_profits"])
        n = len(prof)
        ax = plane([0, n + 1], [0, max(prof) * 1.15], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.6, y_length=4.6,
                   xticks=[1, 10, 20, n], yticks=[0, 250, 500, 750, 1000], xlabel=r"yards, \ cheapest first",
                   ylabel=r"profit, \ \$ a month", font_size=17)
        a = ax.ax
        bars = VGroup(*[Rectangle(width=0.16, height=max(a.c2p(0, v)[1] - a.c2p(0, 0)[1], 1e-3), stroke_width=0,
                                  fill_color=OUT, fill_opacity=0.85).move_to(a.c2p(k + 1, 0), aligned_edge=DOWN)
                        for k, v in enumerate(prof)])
        side = VGroup(
            label(r"now the yards differ: \ fixed costs \\ from \$2{,}000 to \$8{,}000 a month", font_size=23),
            label(r"they open cheapest first, \ until the next \\ would lose money", font_size=23),
            label(rf"{h['firms']} yards; \ price \${h['price']:,.0f}".replace(",", "{,}"), font_size=24,
                  color=PRICE),
            label(r"the last yard earns least, \\ and a 28th would lose money; \\ the cheapest earn rents",
                  font_size=23, color=OUT),
            label(rf"rents: \ \${h['rents']:,.0f} a month in all".replace(",", "{,}"), font_size=24, color=OUT),
            label(r"returns to something scarce: \ a better site, \\ a better manager (Ricardo's rent on land)",
                  font_size=22, color=GREY_A),
            label(r"long-run supply now slopes up: \\ more boats need costlier yards", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Real yards aren't identical. <bookmark mark='a'/> Give the Island's potential yards fixed costs spread "
            "between two and eight thousand dollars a month. <bookmark mark='b'/> They open cheapest first, until "
            "the next one would lose money. <bookmark mark='c'/> Twenty-seven open, and the price settles at nine "
            "hundred and sixty-six dollars. <bookmark mark='d'/> The last yard to open earns the least, and a "
            "twenty-eighth would lose money; the cheaper ones earn well above their costs: rents, here about "
            "fourteen and a half thousand dollars a "
            "month across the industry. <bookmark mark='e'/> Rents are returns to something scarce that competition "
            "can't copy: a better site on the shore, a better manager. David Ricardo's rent on land is the "
            "original. <bookmark mark='f'/> And with differences like these, the long-run supply curve slopes up: to "
            "build more boats, the Island must use costlier yards."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.08), FadeIn(side[1]),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
            vo.wait_until("f")
            self.play(FadeIn(side[6]))
        self.clear_scene()
