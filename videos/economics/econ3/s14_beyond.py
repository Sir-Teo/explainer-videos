from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403

WELFARE = "#7BD88F"
INCOME = E.ACCENT


class Beyond(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Beyond GDP", r"Can one number measure how well people live?",
             "Chapter twelve. Beyond GDP.", lit=("households",), scale=("person", "nation", "world"),
             horizon=("a lifetime",))
        self.mew()
        self.hdi()
        self.welfare()

    # ------------------------------------------------------------------
    def mew(self):
        nt = load("beyond")["nt"]
        who = history_card(r"1972", r"William Nordhaus and James Tobin, ``Is Growth Obsolete?''",
                           r"a measure of economic welfare built from the national accounts", color=WELFARE,
                           width=6.6, font_size=24).to_corner(UL, buff=0.45)
        plus = VGroup(label(r"add", font_size=26, color=E.GAIN),
                      label(r"the value of leisure", font_size=24),
                      label(r"work done at home", font_size=24),
                      label(r"the services of cars, homes, appliances", font_size=24)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18)
        minus = VGroup(label(r"take away", font_size=26, color=E.MISS),
                       label(r"``regrettables'': \ defence, \ commuting", font_size=24),
                       label(r"the costs of crowded cities", font_size=24),
                       label(r"investment that only keeps up", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        VGroup(plus, minus).arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to(DOWN * 0.1)
        res = VGroup(label(rf"1929--65, a year per head: \ NNP {nt['nnp_growth']}\%, \ MEW {nt['mew_growth']}\%",
                           font_size=30, color=WELFARE),
                     label(r"slower, \ and still growing", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15)
        res.to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Nordhaus and Tobin, NBER (1972), table 2", corner=DR, font_size=15)
        with self.voiceover(
            "By 1970 many people wondered whether growth of GDP was worth having at all. <bookmark mark='a'/> In "
            "1972 William Nordhaus and James Tobin answered with the accounts themselves. They built a measure of "
            "economic welfare: <bookmark mark='b'/> GDP, plus the value of leisure and of work done at home, plus "
            "the services people get from the cars and houses and machines they own; <bookmark mark='c'/> minus "
            "what they called regrettables, spending like defence and commuting that is a cost of living rather "
            "than a benefit, minus the disamenities of crowded cities. <bookmark mark='d'/> From 1929 to 1965, "
            f"they found, welfare per head grew {nt['mew_growth']} percent a year, against "
            f"{nt['nnp_growth']} for net national product. Slower, but growing. Their title asked whether growth "
            "was obsolete, and their answer was no."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(who, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(plus, lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(minus, lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(res, shift=UP * 0.1))
        self.clear_scene()

    def hdi(self):
        b = load("beyond")
        x = np.log10(np.array(b["gnipc"]))
        y = np.array(b["hdi"])
        ax = axes([np.log10(500), np.log10(150000)], [0.3, 1.0], x_length=7.0, y_length=5.0,
                  xticks=[np.log10(v) for v in (1000, 10000, 100000)], yticks=[0.4, 0.6, 0.8, 1.0],
                  xfmt=lambda v: rf"\${10 ** v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"{v:.1f}",
                  xlabel=r"income per head (GNI, 2021 PPP dollars), \ log scale",
                  ylabel=r"Human Development Index", font_size=20, center=LEFT * 2.7 + DOWN * 0.2)
        a = ax.ax
        dots = VGroup(*[Dot(a.c2p(xx, yy), radius=0.05, color=GREY_A, fill_opacity=0.7) for xx, yy in zip(x, y)])
        picks = VGroup()
        for code, nm, col, side in (("CUB", r"Cuba", E.GAIN, UP), ("TON", r"Tonga", E.GAIN, UP),
                                    ("QAT", r"Qatar", E.MISS, DOWN), ("BRN", r"Brunei", E.MISS, DOWN),
                                    ("GUY", r"Guyana", E.MISS, DOWN)):
            i = b["codes"].index(code)
            pt = a.c2p(x[i], y[i])
            picks.add(VGroup(Dot(pt, radius=0.07, color=col), label(nm, font_size=19, color=col).next_to(pt, side,
                                                                                                    buff=0.08)))
        what = VGroup(label(r"UNDP, since 1990: \ Mahbub ul Haq and Amartya Sen", font_size=22, color=E.ACCENT),
                      label(r"a long life: \ life expectancy", font_size=22),
                      label(r"knowledge: \ years of schooling", font_size=22),
                      label(r"a decent living: \ income, on a log scale", font_size=22),
                      label(rf"correlation with log income: \ {b['corr_log']:.2f}", font_size=22, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3).shift(UP * 0.6)
        if what.width > 5.2:
            what.width = 5.2
        tag = data_tag(r"UNDP, Human Development Report 2025 (data for 2023)", corner=DL, font_size=15)
        with self.voiceover(
            "The best-known alternative is the Human Development Index, published by the United Nations since "
            "1990 and designed by the economist Mahbub ul Haq with Amartya Sen. <bookmark mark='a'/> It averages "
            "three things: how long people live, how much schooling they get, and their income, counted on a log "
            "scale so that an extra dollar matters less to the rich. <bookmark mark='b'/> Here it is for "
            f"{len(y)} countries, against income per head. <bookmark mark='c'/> It's tightly tied to income: the "
            f"correlation with log income is {b['corr_log']:.2f}, partly because income is one of its three "
            "parts. <bookmark mark='d'/> The interesting countries are the ones off the line: <bookmark mark='e'/> "
            "some, like Cuba and Tonga, do far better at keeping people alive and in school than their income "
            "alone would suggest, "
            "<bookmark mark='f'/> and others far worse, among them several rich in oil and gas, like Qatar, "
            "Brunei and Guyana, where income has outrun health and schooling."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(what[0]))
            vo.wait_until("a")
            self.play(FadeIn(what[1:4], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.005), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(what[4]))
            vo.wait_until("d")
            self.wait(0.2)
            vo.wait_until("e")
            self.play(FadeIn(picks[0]), FadeIn(picks[1]))
            vo.wait_until("f")
            self.play(FadeIn(picks[2]), FadeIn(picks[3]), FadeIn(picks[4]))
        self.clear_scene()

    def welfare(self):
        jk = load("beyond")["jk"]
        rows = jk["rows"]
        lo, hi = np.log10(0.7), np.log10(110)
        x0, x1 = -2.2, 5.6

        def X(v):
            return x0 + (x1 - x0) * (np.log10(v) - lo) / (hi - lo)

        axis = Line([x0, -2.9, 0], [x1, -2.9, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[label(f"{v:g}", font_size=19, color=GREY_B).move_to([X(v), -3.2, 0]) for v in (1, 3, 10, 30,
                                                                                                         100)])
        unit = label(r"US $= 100$, \ log scale", font_size=19, color=GREY_B).next_to(axis, DOWN, buff=0.45)
        unit.align_to(axis, RIGHT)
        lines = VGroup()
        for k, (name, wel, inc) in enumerate(rows):
            y = 2.55 - k * 0.43
            nm = label(name, font_size=20, color=GREY_A).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
            di = Dot([X(inc), y, 0], radius=0.075, color=INCOME)
            dw = Dot([X(wel), y, 0], radius=0.075, color=WELFARE)
            seg = Line([X(inc), y, 0], [X(wel), y, 0], color=WELFARE if wel > inc else E.MISS, stroke_width=3)
            lines.add(VGroup(nm, seg, di, dw))
        key = VGroup(VGroup(Dot(radius=0.075, color=INCOME), label(r"income per person", font_size=21,
                                                                   color=INCOME)).arrange(RIGHT, buff=0.1),
                     VGroup(Dot(radius=0.075, color=WELFARE), label(r"consumption-equivalent welfare", font_size=21,
                                                                    color=WELFARE)).arrange(RIGHT, buff=0.1)).arrange(
            RIGHT, buff=0.6).to_edge(UP, buff=0.15)
        fr = jk["france"]
        france = VGroup(
            label(r"France vs the US", font_size=24, color=E.ACCENT),
            label(rf"consumption: \ {fr['consumption']}\%", font_size=21),
            label(rf"life: \ {fr['life_expectancy'][0]:.0f} vs {fr['life_expectancy'][1]:.0f} years", font_size=21),
            label(rf"hours: \ {fr['hours'][0]} vs {fr['hours'][1]} a year", font_size=21),
            label(r"more equal consumption", font_size=21),
            label(r"welfare: \ 92\%", font_size=24, color=WELFARE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DL, buff=0.35).shift(UP * 0.6)
        tag = published_tag(r"Jones and Klenow, AER (2016), table 2 (about 2005)", corner=DR, font_size=14)
        with self.voiceover(
            "The most economic answer came in 2016, from Charles Jones and Peter Klenow. They asked a single "
            "question: what share of an American's consumption would make you indifferent between living in "
            "America and living in another country, given each country's consumption, leisure, life expectancy "
            "and inequality? <bookmark mark='a'/> Here are their thirteen countries, around 2005: income per "
            "person in gold, their welfare measure in green, the United States set at a hundred. "
            "<bookmark mark='b'/> France has 67 percent of America's income and 60 percent of its consumption. But "
            "the French live about three years longer, work far fewer hours, and share consumption more equally. "
            "Counting those, French welfare is 92 percent of America's. <bookmark mark='c'/> For the poorer "
            "countries it goes the other way: shorter lives and more inequality put welfare below income. "
            "<bookmark mark='d'/> Across countries the two measures correlate at 0.98, so GDP per head is a good "
            "first guide. But the typical gap between them is about a third, and gaps like that are exactly what "
            "Kuznets warned about in 1934."
        ) as vo:
            self.play(FadeIn(key), Create(axis), FadeIn(ticks), FadeIn(unit), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l[0]) for l in lines], lag_ratio=0.05),
                      LaggedStart(*[FadeIn(l[2]) for l in lines], lag_ratio=0.05))
            self.play(LaggedStart(*[AnimationGroup(Create(l[1]), FadeIn(l[3])) for l in lines], lag_ratio=0.08),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(lines[2], color=WELFARE, scale_factor=1.03), FadeIn(france, lag_ratio=0.15))
            vo.wait_until("c")
            self.play(*[Indicate(l[1], color=E.MISS) for l in lines[5:]])
            vo.wait_until("d")
            self.wait(0.5)
        self.clear_scene()
