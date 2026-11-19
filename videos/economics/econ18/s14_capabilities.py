from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403

SHOW = {"LKA": (r"Sri Lanka", WELF, UP), "GNQ": (r"Equatorial Guinea", CYCLE, DOWN), "CUB": (r"Cuba", HARS, UP),
        "USA": (r"United States", MONEY, DOWN), "CRI": (r"Costa Rica", RAWLS, UP), "QAT": (r"Qatar", LIFE, UP)}


class Capabilities(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Capabilities: \ what to measure", r"Should we judge a society by its income, \ its happiness, "
             r"\ or what its people are able to do and be?", "Chapter twelve. Capabilities: what to measure.",
             lit={1985: r"Sen", 1990: r"the first HDI", 2012: r"Ravallion's critique"}, scale=("person", "nation",
                                                                                               "world"),
             horizon=("a decade",))
        self.idea()
        self.scatter()
        self.index()

    def idea(self):
        rows = VGroup(
            label(r"income is a means: \ what it buys depends on health, \ place, \ disability, \ and the law",
                  font_size=23),
            label(r"happiness adapts: \ people who have little often learn to want little", font_size=23,
                  color=GREY_A),
            label(r"Sen: \ judge by capabilities, \ what people are able to do and to be", font_size=24, color=WELF),
            label(r"to live long, \ to read, \ to move freely, \ to take part in the life of the community",
                  font_size=23, color=WELF),
            label(r"which capabilities, \ and how to weigh them: \ \emph{Philosophy, Built}, \ Part 38", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Sen, \emph{Commodities and Capabilities} (1985); \ \emph{Development as Freedom} "
                            r"(1999)", corner=DR, font_size=12)
        with self.voiceover(
            "Everything so far has added up incomes or utilities. Sen asked whether either is the right thing to "
            "add. <bookmark mark='a'/> Income is only a means. What it buys depends on your health, where you live, "
            "whether you have a disability, and what the law lets you do. <bookmark mark='b'/> And happiness "
            "adapts: people who have little often learn to want little, so a measure of satisfaction can make "
            "deprivation look acceptable. <bookmark mark='c'/> Sen proposed judging a society by people's "
            "capabilities: what they are able to do and to be. <bookmark mark='d'/> To live a long life, to read, to "
            "move freely, to take part in the life of the community. <bookmark mark='e'/> Which capabilities count, "
            "and how to weigh them, is a question for philosophy; Part thirty-eight of Philosophy, Built takes it "
            "up."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def scatter(self):
        h = load("hdi")
        ax = plane([np.log10(600), np.log10(150000)], [50, 86], center=DOWN * 0.35 + LEFT * 0.6, x_length=11.0,
                   y_length=5.3, xticks=[3, 4, 5], yticks=[50, 60, 70, 80],
                   xfmt=lambda v: {3: r"1{,}000", 4: r"10{,}000", 5: r"100{,}000"}[int(v)],
                   xlabel=r"income per head, \ 2023 \ (2021 PPP dollars, \ log scale)",
                   ylabel=r"life expectancy at birth, \ years", font_size=17)
        dots = VGroup(*[Dot(ax.ax.c2p(np.log10(r["gni"]), r["le"]), radius=0.045, color=GREY_B, fill_opacity=0.7)
                        for r in h["rows"] if 600 <= r["gni"] <= 150000 and 50 <= r["le"] <= 86])
        named = h["named"]
        marks = {}
        for code, (name, c, side) in SHOW.items():
            r = named[code]
            p = ax.ax.c2p(np.log10(r["gni"]), r["le"])
            d = Dot(p, radius=0.09, color=c)
            t = label(rf"{name}: \ \${r['gni']:,.0f}, \ {r['le']:.1f} years".replace(",", "{,}"), font_size=16,
                      color=c).next_to(p, side, buff=0.12)
            marks[code] = VGroup(d, t)
        lk, gq = named["LKA"], named["GNQ"]
        gap = DoubleArrow(ax.ax.c2p(np.log10(gq["gni"]) + 0.03, gq["le"]), ax.ax.c2p(np.log10(lk["gni"]) + 0.03,
                                                                                     lk["le"]),
                          buff=0.1, color=E.ACCENT, stroke_width=3, tip_length=0.15)
        gl = label(rf"{lk['le'] - gq['le']:.0f} years", font_size=18, color=E.ACCENT).next_to(gap, RIGHT, buff=0.1)
        src = data_tag(r"UNDP, \ Human Development Report 2025 data", corner=DR, font_size=12)
        with self.voiceover(
            "The data show why it matters. <bookmark mark='a'/> Each dot is a country in 2023: income per head "
            "across, on a log scale, and life expectancy up. Richer countries live longer, but the spread at any "
            "income is wide. <bookmark mark='b'/> Sri Lanka and Equatorial Guinea have almost the same income, a "
            "little under thirteen thousand dollars a head. <bookmark mark='c'/> Sri Lankans live to about "
            "seventy-seven and a half; Equatorial Guineans to about sixty-four: <bookmark mark='d'/> fourteen years "
            "apart. <bookmark mark='e'/> Cuba, with an income about a ninth of America's, has almost the same life "
            "expectancy, and Costa Rica, with less than a third, a longer one. Qatar, one of the richest countries, "
            "has long lives too. Income is a poor guide to the capability that matters most: staying alive."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(marks["LKA"][0]), FadeIn(marks["GNQ"][0]))
            vo.wait_until("c")
            self.play(FadeIn(marks["LKA"][1]), FadeIn(marks["GNQ"][1]))
            vo.wait_until("d")
            self.play(GrowFromCenter(gap), FadeIn(gl))
            vo.wait_until("e")
            for k in ("CUB", "USA", "CRI", "QAT"):
                self.play(FadeIn(marks[k]), run_time=0.7)
        self.clear_scene()

    def index(self):
        n = load("hdi")["named"]
        q, c, u = n["QAT"], n["CUB"], n["USA"]
        formula = MathTex(r"\text{HDI} = \big(I_{\text{health}} \cdot I_{\text{education}} \cdot "
                          r"I_{\text{income}}\big)^{1/3}", font_size=36, color=WHITE).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"1990: \ Mahbub ul Haq and Sen build the Human Development Index", font_size=23),
            label(r"each index runs from 0 to 1 between a floor and a goal; \ income enters as a logarithm",
                  font_size=21, color=GREY_A),
            label(rf"Qatar: \ {ordinal(q['gni_rank'])} of {len(load('hdi')['rows'])} by income, \ "
                  rf"{ordinal(q['hdi_rank'])} by the HDI", font_size=23, color=LIFE),
            label(rf"Cuba: \ {ordinal(c['gni_rank'])} by income, \ {ordinal(c['hdi_rank'])} by the HDI; \ the United "
                  rf"States: \ {ordinal(u['gni_rank'])} and {ordinal(u['hdi_rank'])}", font_size=23, color=HARS),
            label(r"but the weights are a choice: \ in the poorest countries the HDI trades a year of life for very "
                  r"little income \ (Ravallion)", font_size=21, color=CYCLE),
            label(r"a measure is a welfare function in disguise: \ ask what it trades for what", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.36).next_to(formula, DOWN, buff=0.45)
        for r in rows:
            if r.width > 13.0:
                r.width = 13.0
        tag = published_tag(r"UNDP, \emph{Human Development Report} (1990, 2025); \ Ravallion, JDE 99(2) (2012)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "In 1990 the Pakistani economist Mahbub ul Haq, working with Sen, turned the idea into a number for "
            "the United Nations. <bookmark mark='a'/> The Human Development Index combines health, education and "
            "income. <bookmark mark='b'/> Each part is scaled from nought to one between a floor and a goal, income "
            "entering as a logarithm, and since 2010 the three have been combined by a geometric mean. "
            f"<bookmark mark='c'/> It reorders the world. Qatar ranks {ordinal(q['gni_rank'])} by income, but "
            f"{ordinal(q['hdi_rank'])} by the index. <bookmark mark='d'/> Cuba ranks {ordinal(c['gni_rank'])} by "
            f"income and {ordinal(c['hdi_rank'])} by the index; the United States {ordinal(u['gni_rank'])} and "
            f"{ordinal(u['hdi_rank'])}. "
            "<bookmark mark='e'/> But its weights are a choice too. Martin Ravallion showed in 2012 that in the "
            "poorest countries, the index treats a year of life as worth very little income. "
            "<bookmark mark='f'/> Every index is a welfare function in disguise. Ask what it trades for what."
        ) as vo:
            self.play(FadeIn(formula), FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
