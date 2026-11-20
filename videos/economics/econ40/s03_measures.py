from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class Measures(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Measuring inequality", r"What does each measure see, \ and what does it hide?",
             "Chapter two. Measuring inequality.", lit={1905: r"Lorenz", 1912: r"Gini", 1970: r"Atkinson"},
             scale=("household", "nation"), horizon=("a year",))
        self.lorenz()
        self.census()
        self.atkinson()
        self.crossing()

    def lorenz(self):
        M = load("measures")
        m = M["m"]
        ax = plane([0, 1], [0, 1], center=LEFT * 2.6 + DOWN * 0.3, x_length=5.4, y_length=5.4,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"share of people, \ poorest first", ylabel=r"share of income",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        diag = seg(ax, 0, 0, 1, 1, GREY_B, 2, dashed=True)
        lc = path(ax, M["p"], M["L"], LORENZ, 3.6, smooth=False)
        gap = band(ax, M["p"], M["L"], M["p"], LORENZ, 0.22)
        rows = [(r"Gini", m["gini"], r"twice the shaded area"),
                (r"top 10\% share", m["top10"], r"of all income"),
                (r"top 1\% share", m["top1"], r""),
                (r"Theil index", m["theil"], r"an entropy")]
        side = VGroup(label(rf"the Island: \ {M['n']:,} incomes", font_size=20, color=WHITE))
        for nm, v, note_ in rows:
            fmt = f"{100 * v['value']:.1f}\\%" if "share" in nm else f"{v['value']:.3f}"
            se = f"{100 * v['se']:.1f}" if "share" in nm else f"{v['se']:.3f}"
            side.add(label(rf"{nm}: \ {fmt} \ (s.e. {se})", font_size=19, color=LORENZ if nm == "Gini" else WHITE))
        side.add(label(r"standard errors: \ resample the 2,000 \\ incomes 400 times", font_size=16, color=GREY_A))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Part three drew the Lorenz curve; here it is again, for two thousand of the Island's incomes. Line "
            "everyone up from poorest to richest and plot the share of income held by each poorest fraction. "
            "<bookmark mark='a'/> With perfect equality the curve is the diagonal. <bookmark mark='b'/> The Gini "
            f"index is twice the area between them: here {m['gini']['value']:.2f}. <bookmark mark='c'/> Every "
            "measure is an estimate from a sample, so each deserves a standard error. Resampling the two thousand "
            f"incomes gives about {m['gini']['se']:.3f} for the Gini, and for the top one percent's share, "
            f"{100 * m['top1']['value']:.1f} percent, about {100 * m['top1']['se']:.0f} point: the very top is always "
            "measured least precisely, because so few people are in it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(diag), FadeIn(side[0]), run_time=1.5)
            self.play(Create(lc), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(diag, color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(gap), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in side[2:]], lag_ratio=0.4), run_time=2.0)
        self.clear_scene()

    def census(self):
        M = load("measures")
        ys, g = M["census_years"], M["census_gini"]
        ax = plane([1965, 2027], [0.35, 0.52], center=LEFT * 1.4 + DOWN * 0.4, x_length=9.0, y_length=4.8,
                   xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[0.36, 0.40, 0.44, 0.48, 0.52],
                   ylabel=r"Gini index of household money income", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.2f}", font_size=14)
        ln = path(ax, ys, g, LORENZ, 3.2, smooth=False)
        ends = VGroup(dot(ax, ys[0], g[0], LORENZ, 0.08), dot(ax, ys[-1], g[-1], LORENZ, 0.08))
        side = VGroup(
            label(rf"{ys[0]}: \ {g[0]:.3f}", font_size=20, color=LORENZ),
            label(rf"{ys[-1]}: \ {g[-1]:.3f}", font_size=20, color=LORENZ),
            label(r"surveys miss the very top \\ and count income \\ before taxes and \\ most transfers", font_size=17,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"U.S. Census Bureau, \ CPS, \ via FRED: \ GINIALLRH", corner=DR, font_size=12)
        with self.voiceover(
            "For American households, the Census Bureau has computed the Gini every year since 1967, from its "
            f"survey. <bookmark mark='a'/> It was {g[0]:.2f} in {ys[0]}, <bookmark mark='b'/> and {g[-1]:.2f} in "
            f"{ys[-1]}: a large rise, most of it in the 1980s and 1990s. <bookmark mark='c'/> Surveys have limits: "
            "few very rich households answer them, and the income counted is before taxes and most transfers. "
            "Chapter three turns to the tax records instead."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            for mk, k in zip("ab", range(2)):
                vo.wait_until(mk)
                self.play(FadeIn(ends[k], scale=1.5), FadeIn(side[k]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def atkinson(self):
        M = load("measures")
        e = M["ede"]
        mean = M["mean"]
        eps = ("0.0", "0.5", "1.0", "2.0", "4.0")
        bars = VGroup()
        for k, ek in enumerate(eps):
            v = e[ek]
            y = 1.7 - 0.9 * k
            w = v / mean * 6.0
            r = Rectangle(width=w, height=0.55, stroke_width=0, fill_color=MIDDLE if ek != "0.0" else GREY_B,
                          fill_opacity=0.85).move_to(np.array([-2.0 + w / 2, y, 0]))
            nm = label(rf"$\varepsilon$ = {float(ek):g}", font_size=20, color=WHITE).next_to(
                np.array([-2.0, y, 0]), LEFT, buff=0.2)
            val = label(rf"\${v:,.0f} \ (Atkinson {1 - v / mean:.2f})" if ek != "0.0" else rf"\${v:,.0f}: \ the mean",
                        font_size=18, color=WHITE).next_to(r, RIGHT, buff=0.15)
            bars.add(VGroup(r, nm, val))
        eq = MathTex(r"W = \frac{1}{n}\sum_i \frac{x_i^{1-\varepsilon}}{1-\varepsilon}, \qquad "
                     r"A_\varepsilon = 1 - \frac{x_{\mathrm{ede}}}{\bar x}", font_size=32).to_edge(UP, buff=0.4)
        head = label(r"the equally distributed equivalent: \ the income which, \ given to everyone, \ is as good",
                     font_size=19, color=GREY_A).next_to(eq, DOWN, buff=0.25)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 1970 Anthony Atkinson pointed out that every index of inequality hides a judgement about how much "
            "inequality matters. He made the judgement explicit. Value each income by a concave function, with a "
            "parameter epsilon for aversion to inequality, and ask: what income, given equally to everyone, would be "
            "as good as the actual distribution? <bookmark mark='a'/> With epsilon zero, only the total counts: the "
            f"answer is the mean, {mean:,.0f} dollars. <bookmark mark='b'/> With epsilon one half, "
            f"{e['0.5']:,.0f} dollars: society would give up {say_pct(1 - e['0.5'] / mean, 0)} of income for equality. "
            f"<bookmark mark='c'/> With epsilon one, {e['1.0']:,.0f} dollars; <bookmark mark='d'/> with two, "
            f"{e['2.0']:,.0f} dollars; <bookmark mark='e'/> with four, a society that cares almost only about its "
            f"poorest, {e['4.0']:,.0f} dollars. Atkinson's index is the share given up. The data cannot choose "
            "epsilon; "
            "that is ethics."
        ) as vo:
            self.play(Write(eq), FadeIn(head), FadeIn(tag), FadeIn(bars[0]), *[FadeIn(b_[1]) for b_ in bars[1:]],
                      run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(bars[0][0], color=WHITE, scale_factor=1.02))
            for mk, b_ in zip("bcde", bars[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(b_[0], shift=RIGHT * 0.1), FadeIn(b_[2]))
        self.clear_scene()

    def crossing(self):
        C = load("measures")["crossing"]
        ax = plane([0, 1], [0, 1], center=LEFT * 2.6 + DOWN * 0.3, x_length=5.2, y_length=5.2,
                   xticks=[0, 0.5, 1.0], yticks=[0, 0.5, 1.0], xlabel=r"share of people", ylabel=r"share of income",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        diag = seg(ax, 0, 0, 1, 1, GREY_B, 2, dashed=True)
        la = path(ax, C["pa"], C["La"], SOC_A, 3.4, smooth=False)
        lb = path(ax, C["pb"], C["Lb"], SOC_B, 3.4, smooth=False)
        A2, B2 = C["atk"]["2.0"]
        A5, B5 = C["atk"]["0.5"]
        side = VGroup(
            label(r"A: \ four people poor, \\ six alike", font_size=19, color=SOC_A),
            label(r"B: \ one person rich, \\ nine alike", font_size=19, color=SOC_B),
            label(rf"the same Gini: \ {C['gini']:.3f}", font_size=20, color=WHITE),
            label(rf"top 10\% share: \ A {100 * C['top10'][0]:.0f}\%, \ B {100 * C['top10'][1]:.0f}\% \\ "
                  r"$\Rightarrow$ B is more unequal", font_size=18, color=SOC_B),
            label(rf"Atkinson, \ $\varepsilon$ = 0.5: \ A {A5:.3f}, \ B {B5:.3f} \\ $\Rightarrow$ B, \ just",
                  font_size=18, color=SOC_B),
            label(rf"Atkinson, \ $\varepsilon$ = 2: \ A {A2:.2f}, \ B {B2:.2f} \\ $\Rightarrow$ A, \ by far",
                  font_size=18, color=SOC_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = label(r"two invented societies of ten", font_size=14, color=GREY_B).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Measures can disagree, and the reason is that Lorenz curves can cross. Two societies of ten. "
            "<bookmark mark='a'/> In A, four people are poor and the other six have the same income. "
            "<bookmark mark='b'/> In B, one person is rich and the other nine are alike. The curves cross. "
            "<bookmark mark='c'/> Their Gini indices are identical. <bookmark mark='d'/> The top ten percent's share "
            "calls B far more unequal: its rich person takes more than a third. <bookmark mark='e'/> Atkinson's "
            "index with a mild aversion to inequality agrees, just. <bookmark mark='f'/> With a strong aversion, it "
            "calls A far more unequal, because it weighs the poorest most. When curves cross, there is no ranking "
            "without a value judgement: one more reason to report several measures, and to say which part of the "
            "distribution each one watches."
        ) as vo:
            self.play(FadeIn(ax), Create(diag), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(la), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()
