from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403

SHOW = ("Miami", "Los Angeles", "San Francisco", "New York", "Boston", "Seattle", "Chicago", "Denver", "Phoenix",
        "Dallas", "Houston", "Atlanta", "Charlotte", "Indianapolis", "Wichita")


def sd_panel(es, dp, dq, center, col, title):
    """A small supply-and-demand diagram: demand shifts out by 20 percent against supply of elasticity ``es``."""
    ax = plane([0, 2], [0, 2], center=center, x_length=4.2, y_length=3.6, xticks=[], yticks=[],
               xlabel=r"houses", ylabel=r"price", font_size=14)
    a = ax.ax
    # supply through (1, 1): log p = log q / es; demand through (1, 1) with elasticity 1, shifted by 20 percent
    qs = np.linspace(0.3, 1.9, 60)
    sup = path(ax, qs, qs ** (1 / es), col, 3.2, yr=(0, 2))
    d0 = path(ax, qs, 1 / qs, GREY_B, 2.4, yr=(0, 2))
    d1 = path(ax, qs, 1.2 / qs, WHITE, 2.4, yr=(0, 2))
    e0 = Dot(a.c2p(1, 1), radius=0.06, color=GREY_B)
    q1, p1 = np.exp(dq), np.exp(dp)
    e1 = Dot(a.c2p(q1, p1), radius=0.08, color=E.ACCENT)
    head = label(title, font_size=19, color=col).next_to(ax, UP, buff=0.15)
    res = label(rf"price +{100 * dp:.1f}\%, \ houses +{100 * dq:.1f}\%", font_size=18, color=E.ACCENT).next_to(
        ax, DOWN, buff=0.35)
    return VGroup(ax, d0, sup, head), VGroup(d1, e1, res), e0


class Housing(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Housing supply", r"Why are some cities so expensive?",
             "Chapter eight. Housing supply.", lit={2010: r"Saiz", 2019: r"Hsieh and Moretti"},
             scale=("market", "city"), horizon=("a decade",))
        self.shift()
        self.saiz()
        self.prices()
        self.misallocation()

    def shift(self):
        H = load("housing")
        I = H["illus"]
        l0, l1, le = sd_panel(0.6, I["0.6"]["dp"], I["0.6"]["dq"], LEFT * 3.3 + DOWN * 0.2, RENT,
                              r"supply elasticity 0.6")
        r0, r1, re = sd_panel(3.0, I["3.0"]["dp"], I["3.0"]["dq"], RIGHT * 3.3 + DOWN * 0.2, GAIN,
                              r"supply elasticity 3")
        head = label(r"demand for a town's houses rises 20\%", font_size=24, color=WHITE).to_edge(UP, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The last chapter's shocks raised rents more in some towns than others. The difference is the supply "
            "of housing. <bookmark mark='a'/> Suppose demand for a town's houses rises by a fifth. Where builders "
            f"can respond only slowly, with a supply elasticity of 0.6, prices rise {100 * I['0.6']['dp']:.1f} "
            f"percent and the stock only {100 * I['0.6']['dq']:.1f}. <bookmark mark='b'/> Where they can build "
            f"freely, with an elasticity of three, prices rise {100 * I['3.0']['dp']:.0f} percent and the stock "
            f"{100 * I['3.0']['dq']:.0f}. The same boom becomes expensive houses in one town and more houses, and "
            "more people, in the other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(l0), FadeIn(le), FadeIn(r0), FadeIn(re))
            vo.wait_until("a")
            self.play(Create(l1[0]), FadeIn(l1[1:]))
            vo.wait_until("b")
            self.play(Create(r1[0]), FadeIn(r1[1:]))
        self.clear_scene()

    def saiz(self):
        S = tables.SAIZ_2010.data
        m = S["metros"]
        bars = VGroup()
        for k, name in enumerate(SHOW):
            v = m[name]
            y = 2.5 - 0.36 * k
            r = Rectangle(width=v * 1.45, height=0.26, stroke_width=0, fill_color=RENT if v < 1 else (
                GOLD if v < 2 else GAIN), fill_opacity=0.85).move_to(np.array([-2.2 + v * 0.725, y, 0]))
            bars.add(VGroup(label(name, font_size=15, color=GREY_A).move_to(np.array([-3.4, y, 0]), aligned_edge=RIGHT),
                            r, label(f"{v:.2f}", font_size=14, color=WHITE).next_to(r, RIGHT, buff=0.08)))
        avg = DashedLine(np.array([-2.2 + S["weighted"] * 1.45, 2.75, 0]),
                         np.array([-2.2 + S["weighted"] * 1.45, 2.5 - 0.36 * (len(SHOW) - 1) - 0.25, 0]),
                         color=E.ACCENT, stroke_width=2)
        side = VGroup(
            label(r"red: \ under one", font_size=18, color=RENT),
            label(rf"dashed: \ the average, \\ weighted by population, \\ {S['weighted']:.2f}", font_size=18,
                  color=E.ACCENT),
            label(r"why so low? \\ the sea, \ steep hills \\ and regulation", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        tag = published_tag(tables.SAIZ_2010.tag + r", \ Table VI", corner=DR, font_size=12)
        with self.voiceover(
            "Albert Saiz measured these elasticities for American cities from satellite maps of where land can be "
            "built on. <bookmark mark='a'/> Miami, Los Angeles, San Francisco, New York and Boston are all below "
            "one; Houston, Atlanta and Charlotte two to three; Wichita over five. <bookmark mark='b'/> The average "
            f"metropolitan resident lives where it is {S['weighted']:.2f}. <bookmark mark='c'/> The low ones are "
            "hemmed in by the sea and by steep hills, which leave little flat land to build on, and, Saiz found, "
            "by stricter regulation, which itself tends to be adopted where land is already scarce and dear."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars], lag_ratio=0.12),
                      run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(avg), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def prices(self):
        H = load("housing")
        rows = H["rows"]
        ax = plane([np.log(0.5), np.log(3.5)], [0.6, 1.6], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.4,
                   y_length=4.6, xticks=[np.log(v) for v in (0.5, 1, 2, 3)], yticks=[np.log(v) for v in (2, 3, 4)],
                   xlabel=r"Saiz's supply elasticity \ (log scale)", ylabel=r"house prices, \ 2025 over 2000 \ (log)",
                   xfmt=lambda v: f"{np.exp(v):.1f}", yfmt=lambda v: f"{np.exp(v):.0f}x", font_size=14)
        pts = VGroup()
        for r in rows:
            x, y = np.log(r["elasticity"]), np.log(r["growth"])
            nm = r["metro"]
            pts.add(VGroup(dot(ax, x, y, CITY, 0.07), label(nm, font_size=12, color=GREY_A).next_to(
                ax.ax.c2p(x, y), UP if nm not in ("Detroit", "Cleveland", "Chicago") else DOWN, buff=0.06)))
        line = seg(ax, np.log(0.55), H["icpt"] + H["slope"] * np.log(0.55), np.log(3.3),
                   H["icpt"] + H["slope"] * np.log(3.3), E.ACCENT, 2.6)
        side = VGroup(
            label(rf"correlation {H['corr']:.2f}", font_size=20, color=E.ACCENT),
            label(rf"consumer prices: \\ {H['cpi']:.2f}x", font_size=18, color=GREY_A),
            label(r"Detroit, \ Cleveland: \\ elastic enough, \\ but little demand", font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"S\&P CoreLogic Case-Shiller indices, \ via FRED; \ Saiz (2010)", corner=DR, font_size=12)
        with self.voiceover(
            "Does it show in prices? Here are the twenty metropolitan areas with Case-Shiller house price indices: "
            "the rise in house prices from 2000 to 2025 against Saiz's elasticity. <bookmark mark='a'/> Prices "
            "roughly quadrupled in Los Angeles, Miami and San Diego, and rose least where building is easy. The "
            f"correlation is {H['corr']:.2f}. <bookmark mark='b'/> Consumer prices rose {H['cpi']:.2f} times over "
            "the same years, so in real terms the coastal cities' houses doubled. <bookmark mark='c'/> The "
            "exceptions teach too: Detroit and Cleveland could build, but demand was weak, so prices barely kept up "
            "with inflation. Prices need a demand shock and a tight supply."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.08), run_time=3.0)
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def misallocation(self):
        H = load("housing")
        T = load("towns")
        hm = H["hm"]
        R = T["relax"]
        cards = point_cards([
            (r"Hsieh and Moretti, \ 2019", rf"tight housing in the most \\ productive cities lowered \\ US growth "
                                          rf"by {hm['growth_cut']}\% \\ from 1964 to 2009", RENT),
            (r"Greaney, \ 2026", r"coding errors; \ in a \\ corrected model the gain \\ is two orders of \\ "
                                 r"magnitude smaller", GOLD),
            (r"the Island", rf"Harbour builds freely: \\ people +{100 * R['dlogN']:.0f}\%, \ rents "
                            rf"{100 * R['dlogr']:.0f}\% \\ output +{100 * R['doutput']:.2f}\%", E.AGORA),
        ], width=12.4, cols=3, font_size=20).move_to(DOWN * 0.1)
        head = label(r"what do tight cities cost the country?", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"rents are a transfer to landowners for sure; \ the national output lost is contested",
                     font_size=19, color=GREY_A).to_edge(DOWN, buff=0.55)
        tag = published_tag(tables.HSIEH_MORETTI_2019.tag + r"; \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "What does it cost the whole country when the most productive cities cannot grow? "
            "<bookmark mark='a'/> In 2019 Chang-Tai Hsieh and Enrico Moretti estimated that tight housing in New "
            "York, San Jose and San Francisco kept workers out of the places where they would be most productive, "
            f"and lowered America's growth by {hm['growth_cut']} percent between 1964 and 2009. A striking number, "
            "widely quoted. <bookmark mark='b'/> In 2026 Brian Greaney published a comment: he found errors in the "
            "code, and in a corrected model the gain from loosening the three cities' rules was about a hundredth "
            "of the size reported. <bookmark mark='c'/> On the Island, letting Harbour, the most productive town, "
            f"build freely brings {100 * R['dlogN']:.0f} percent more people and cuts its rents "
            f"{abs(100 * R['dlogr']):.0f} percent, but raises the Island's output by only "
            f"{100 * R['doutput']:.2f} percent. <bookmark mark='d'/> Expensive cities clearly transfer income to "
            "those who own land in them; how much national output they cost is an open and contested question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
