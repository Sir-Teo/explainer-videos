from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403

LINES = {"GBR": (r"United Kingdom", "#5DADEC"), "NLD": (r"Netherlands", "#7EC8F5"), "CHN": (r"China", "#F26D6D"),
         "IND": (r"India", "#FF9F5A"), "JPN": (r"Japan", "#E9A3C9")}
ANCIENT = ("ITA", "EGY", "FRA", "ESP", "TUR")  # provinces of the Roman Empire in the year 1


def maddison_cite() -> str:
    return r"Maddison Project Database 2023; England: Broadberry et al. (2015); year 1: Scheidel and Friesen (2009)"


class LongView(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The long view", r"How rich were people, for most of history?",
             "Chapter seven. The long view.", lit={1798: r"Malthus's \emph{Essay}", 1776: r"\emph{The Wealth of "
                                                                                       r"Nations}"},
             scale=("nation", "world"), horizon=("a century",))
        self.linear()
        self.compound()
        self.log_scale()
        self.diverge()
        self.fact()

    # ------------------------------------------------------------------
    def series(self):
        out = {}
        for code in LINES:
            c = data.maddison_country(code)
            y, g = np.array(c["year"]), np.array(c["gdppc"])
            out[code] = (y, g)
        return out

    def linear(self):
        d = load("longrun")
        ax = axes([0, 2030], [0, 40000], x_length=11.6, y_length=5.0, xticks=[1, 500, 1000, 1500, 2022],
                  yticks=[0, 10000, 20000, 30000, 40000], xfmt=lambda v: f"{v:.0f}",
                  yfmt=lambda v: rf"\${v / 1000:.0f}{{,}}000" if v else r"0", font_size=19, center=[0.3, -0.35, 0])
        yl = label(r"GDP per head, \ 2011 dollars, \ adjusted for prices", font_size=22, color=GREY_A)
        yl.next_to(ax.ax, UP, buff=0.15).align_to(ax.ax, LEFT)
        anc = VGroup()
        for code in ANCIENT:
            c = data.maddison_country(code)
            if c["year"][0] == 1:
                anc.add(Circle(radius=0.07, stroke_color=GREY_A, stroke_width=2).move_to(ax.ax.c2p(1, c["gdppc"][0])))
        uk = curve(ax.ax, d["uk_year"], d["uk"], LINES["GBR"][1], 3)
        ukl = label(r"England, then the United Kingdom", font_size=20, color=LINES["GBR"][1])
        ukl.next_to(ax.ax.c2p(2010, d["uk_2022"]), LEFT, buff=0.15).shift(UP * 0.1)
        world = curve(ax.ax, d["world_year"], d["world"], WHITE, 4)
        wl = label(r"the world", font_size=22, color=WHITE).next_to(ax.ax.c2p(2022, d["world_2022"]), LEFT,
                                                                   buff=0.15).shift(DOWN * 0.25)
        al = label(r"year 1: \ estimates for five Roman provinces", font_size=18, color=GREY_A)
        al.next_to(anc, UR, buff=0.1).shift(UP * 0.3)
        src = data_tag(maddison_cite(), font_size=15)
        gdp = definition_card(r"GDP per head", r"the value of everything an economy produces in a year, divided by "
                              r"its people; \ here in 2011 dollars, adjusted for what things cost in each place and "
                              r"time", color=WHITE, width=5.8, font_size=22).move_to([2.6, 1.0, 0])
        with self.voiceover(
            "Step back from Paris and the pin factory, and look at the whole of history at once. "
            "<bookmark mark='a'/> This is income per head, the value of everything produced in a year divided by "
            "the number of people, in dollars of 2011, adjusted for what things cost. The numbers come from the "
            "Maddison Project, a team of economic historians who have reconstructed them, country by country, from "
            "wages, prices, harvests and tax records. <bookmark mark='b'/> In the year one, for the provinces of "
            "the Roman Empire, the estimates run from about nine hundred to fourteen hundred dollars a year. "
            "<bookmark mark='c'/> England's annual series starts in 1252. For five hundred years it barely moves. "
            "<bookmark mark='d'/> Then, around 1800, it takes off, and so does the world. This shape is sometimes "
            "called the hockey stick, and it is the most important fact in economic history."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(gdp, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(a, scale=0.5) for a in anc], lag_ratio=0.15), FadeIn(al), FadeOut(gdp))
            vo.wait_until("c")
            k = int(np.searchsorted(d["uk_year"], 1800))
            part = curve(ax.ax, d["uk_year"][:k], d["uk"][:k], LINES["GBR"][1], 3)
            self.play(Create(part), run_time=3, rate_func=linear)
            vo.wait_until("d")
            self.play(Create(uk), run_time=2.5)
            self.remove(part)
            self.play(Create(world), FadeIn(ukl), FadeIn(wl), run_time=2)
        self.clear_scene()

    def compound(self):
        d = load("longrun")
        rows = VGroup(
            MathTex(r"y_t = y_0\, e^{g t}", font_size=44),
            MathTex(r"\text{doubling time}", r"= \frac{\ln 2}{g}", r"\approx \frac{70}{g \text{ in \%}}",
                    font_size=40),
        ).arrange(DOWN, buff=0.4).to_edge(UP, buff=0.6)
        tab = VGroup()
        for name, g, dbl, col in (
            (r"England, 1270 to 1700", d["g_uk_pre"], d["double_pre"], LINES["GBR"][1]),
            (r"the world, 1820 to 2022", d["g_world"], d["double_world"], WHITE),
        ):
            r_ = VGroup(label(name, font_size=30, color=col), label(rf"{100 * g:.2f}\% a year", font_size=30, color=col),
                        label(rf"doubles in {dbl:.0f} years", font_size=30, color=E.ACCENT))
            tab.add(r_)
        for r_ in tab:
            r_[0].move_to([-3.6, 0, 0])
            r_[1].move_to([0.9, 0, 0])
            r_[2].move_to([4.4, 0, 0])
        tab.arrange(DOWN, buff=0.5).next_to(rows, DOWN, buff=0.7)
        for r_ in tab:
            r_[0].set_x(-3.6)
            r_[1].set_x(0.9)
            r_[2].set_x(4.4)
        fact = label(rf"the world in 2022: \ {d['world_ratio']:.1f} times as rich per head as in 1820", font_size=30,
                     color=WHITE).next_to(tab, DOWN, buff=0.6)
        life = label(r"a person born in 1270 lived in the same economy as their great-great-grandparents; "
                     r"\ one born in 1950 did not", font_size=22, color=GREY_A).next_to(fact, DOWN, buff=0.3)
        with self.voiceover(
            "The difference is compounding. <bookmark mark='a'/> If income grows at a steady rate g, it multiplies "
            "by e to the g t after t years, and it doubles when g t equals the natural log of two, about point "
            "seven. So the doubling time is roughly seventy divided by the growth rate in percent. "
            f"<bookmark mark='b'/> From 1270 to 1700, England's income per head grew at {100 * d['g_uk_pre']:.2f} "
            f"percent a year: a doubling every {d['double_pre']:.0f} years. <bookmark mark='c'/> Since 1820 the "
            f"world's has grown at {100 * d['g_world']:.2f} percent: a doubling every {d['double_world']:.0f} years. "
            f"<bookmark mark='d'/> That's why the world is now {d['world_ratio']:.0f} times as rich per head as in "
            "1820. Before 1800, a person lived in much the same economy as their great-great-grandparents. Now "
            "each generation lives in a different one."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]))
            self.play(Write(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(tab[1], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(fact), FadeIn(life))
        self.clear_scene()

    def log_scale(self):
        d = load("longrun")
        lo, hi = np.log10(400), np.log10(60000)
        ax = axes([1250, 2030], [lo, hi], x_length=11.2, y_length=5.0, xticks=[1300, 1400, 1500, 1600, 1700, 1800,
                                                                                1900, 2000],
                  yticks=[np.log10(v) for v in (500, 1000, 2000, 5000, 10000, 20000, 50000)],
                  xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), font_size=19,
                  center=[0.3, -0.35, 0])
        yl = label(r"GDP per head, \ on a log scale: \ every step up doubles", font_size=22, color=GREY_A)
        yl.next_to(ax.ax, UP, buff=0.15).align_to(ax.ax, LEFT)
        uy = np.array(d["uk_year"])
        uk = curve(ax.ax, uy[uy >= 1252], np.log10(np.array(d["uk"])[uy >= 1252]), LINES["GBR"][1], 3)
        nl_y, nl = d["NLD_year"], d["NLD_gdppc"]
        nld = curve(ax.ax, nl_y[nl_y >= 1250], np.log10(nl[nl_y >= 1250]), LINES["NLD"][1], 2.5)
        world = curve(ax.ax, d["world_year"], np.log10(d["world"]), WHITE, 4)
        names = VGroup(label(r"England / UK", font_size=20, color=LINES["GBR"][1]).move_to(ax.ax.c2p(1330, np.log10(2600))),
                       label(r"Holland / Netherlands", font_size=20, color=LINES["NLD"][1]).move_to(ax.ax.c2p(1420, np.log10(4300))),
                       label(r"the world", font_size=20, color=WHITE).move_to(ax.ax.c2p(1880, np.log10(1050))))
        pre = DashedLine(ax.ax.c2p(1270, np.log10(d["uk_1270"])), ax.ax.c2p(1700, np.log10(d["uk_1700"])),
                         color=E.ACCENT, stroke_width=3)
        post = DashedLine(ax.ax.c2p(1820, np.log10(d["world_1820"])), ax.ax.c2p(2022, np.log10(d["world_2022"])),
                          color=E.ACCENT, stroke_width=3)
        src = data_tag(r"Maddison Project Database 2023; Holland: van Zanden and van Leeuwen (2012)", font_size=15)
        with self.voiceover(
            "Here is the same history on a log scale, where every step up the axis is a doubling. On this scale "
            "steady growth is a straight line, and its slope is the growth rate. <bookmark mark='a'/> England "
            "before 1700 isn't quite flat. It jumps after the Black Death, when there were suddenly far fewer "
            "people to share the land, and falls back for decades in the seventeenth century. Holland runs ahead of "
            "England for four centuries, and stalls after the sixteen fifties. <bookmark mark='b'/> Then the slope "
            "changes, for good. <bookmark mark='c'/> Fit a straight line to each era and the two lines tell the "
            "story: a growth rate of about one sixth of a percent, and then about one and a third. A tiny change in "
            "a slope, compounded over two centuries."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(uk), Create(nld), FadeIn(names[:2]), run_time=3)
            vo.wait_until("b")
            self.play(Create(world), FadeIn(names[2]), run_time=2)
            vo.wait_until("c")
            self.play(Create(pre), Create(post))
        self.clear_scene()

    def diverge(self):
        d = load("longrun")
        lo, hi = np.log10(300), np.log10(80000)
        ax = axes([1820, 2025], [lo, hi], x_length=10.0, y_length=5.2, xticks=[1820, 1870, 1913, 1950, 1980, 2022],
                  yticks=[np.log10(v) for v in (500, 1000, 2000, 5000, 10000, 20000, 50000)],
                  xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), font_size=19,
                  center=[-0.6, -0.35, 0])
        yl = label(r"GDP per head, \ log scale", font_size=22, color=GREY_A).next_to(ax.ax, UP, buff=0.15).align_to(
            ax.ax, LEFT)
        lines, labels_ = VGroup(), VGroup()
        spec = (("USA", r"United States", "#7EC8F5"), ("GBR", r"United Kingdom", "#5DADEC"),
                ("JPN", r"Japan", "#E9A3C9"), ("KOR", r"South Korea", "#C9A0FF"), ("CHN", r"China", "#F26D6D"),
                ("IND", r"India", "#FF9F5A"), ("NGA", r"Nigeria", "#7BD88F"), ("ETH", r"Ethiopia", "#B5D86B"))
        for code, name, col in spec:
            c = data.maddison_country(code)
            y, g = np.array(c["year"]), np.array(c["gdppc"])
            ok = (y >= 1820) & np.isfinite(g)
            if ok.sum() < 2:
                continue
            ln = curve(ax.ax, y[ok], np.log10(g[ok]), col, 3)
            lines.add(ln)
            labels_.add(label(name, font_size=19, color=col).next_to(ax.ax.c2p(y[ok][-1], np.log10(g[ok][-1])), RIGHT,
                                                                       buff=0.1))
        # keep the end labels apart
        order = sorted(range(len(labels_)), key=lambda i: labels_[i].get_y())
        for a, b in zip(order, order[1:]):
            if labels_[b].get_y() - labels_[a].get_y() < 0.26:
                labels_[b].set_y(labels_[a].get_y() + 0.26)
        src = data_tag(r"Maddison Project Database 2023 (country sources in the README)", font_size=16)
        with self.voiceover(
            "And the escape didn't happen everywhere at once. <bookmark mark='a'/> Britain and the United States "
            "pull away first, through the nineteenth century. This is the Great Divergence. In 1820 the richest "
            f"country in these data was about {d['gap_1820']:.0f} times as rich per head as the poorest; by 1913, "
            f"about {d['gap_1913']:.0f} times. <bookmark mark='b'/> Japan joins in the late nineteenth century. "
            f"South Korea in 1950 was poorer than {100 * (1 - d['kor_1950_share_poorer']):.0f} percent of the "
            "countries in the data, and on these estimates it is now richer per head than Britain or France. "
            "China's line turns up after 1978, and India's in the 1980s, faster after 1990. "
            "<bookmark mark='c'/> And some countries have barely begun. Why some places escaped "
            "and others haven't is the subject of Parts nineteen to twenty-one, and of development economics in "
            "Part forty-six."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(labels_[0]), FadeIn(labels_[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(*[Create(x) for x in lines[2:6]], *[FadeIn(x) for x in labels_[2:6]], run_time=3)
            vo.wait_until("c")
            self.play(*[Create(x) for x in lines[6:]], *[FadeIn(x) for x in labels_[6:]], run_time=2)
        self.clear_scene()

    def fact(self):
        d = load("longrun")
        f = facts.BY_KEY["flat_for_millennia"]
        data_col = VGroup(label(rf"England 1270--1700: \ {100 * d['g_uk_pre']:.2f}\% a year", font_size=21,
                                color=WHITE),
                          label(rf"the world 1820--2022: \ {100 * d['g_world']:.2f}\% a year", font_size=21,
                                color=WHITE)).arrange(DOWN, buff=0.12)
        ag = VGroup(label(r"Part 19 builds the economy", font_size=21, color=E.AGORA),
                    label(r"that was stuck, and escaped", font_size=21, color=E.AGORA)).arrange(DOWN, buff=0.08)
        fc = fact_card(f.statement, columns=((r"your guess", label(r"(when did it turn?)", font_size=22,
                                                                   color=E.ACCENT)),
                                             (r"the data", data_col), (r"Agora", ag)), width=12.4).move_to(UP * 1.0)
        pay = payoff_card([(r"why the line was flat, and why it turned", [19]),
                           (r"capital, ideas and institutions", [20, 21]),
                           (r"the countries still waiting", [46])], font_size=22).scale(0.85).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "That's the second of the Facts: income per head was nearly flat for millennia, and then rose without "
            "stopping. Any theory of the economy has to explain both halves: why it was stuck, and why it escaped. "
            "Part nineteen builds the economy that was stuck, and Parts twenty and twenty-one the engines of "
            "growth."
        ):
            self.play(FadeIn(fc, shift=UP * 0.2))
            self.play(FadeIn(pay, shift=UP * 0.2))
        self.clear_scene()
