from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403


class Real(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Real and nominal: \ whose basket?", r"When prices change, how much more did we really make?",
             "Chapter four. Real and nominal: whose basket?", scale=("nation",), horizon=("a year", "a century"))
        self.century()
        self.kuznets()
        self.formulas()

    # ------------------------------------------------------------------
    def century(self):
        d = load("indices")["us"]
        years = d["years"]
        lo, hi = np.log10(50), np.log10(40000)
        ax = year_axis([1929, 2026], [lo, hi], x_length=9.0, y_length=4.8, xticks=list(range(1930, 2030, 10)),
                       yticks=[np.log10(v) for v in (100, 1000, 10000)], log_y=True,
                       ylabel=r"billions of dollars, \ log scale", center=LEFT * 1.4 + DOWN * 0.3)
        a = ax.ax
        nom = VMobject(stroke_color=E.DATA, stroke_width=3.5).set_points_as_corners(
            [a.c2p(y, np.log10(v)) for y, v in zip(years, d["nominal"])])
        real = VMobject(stroke_color=E.ACCENT, stroke_width=3.5).set_points_as_corners(
            [a.c2p(y, np.log10(v)) for y, v in zip(years, d["real"])])
        nl = label(r"in the dollars \\ of each year \\ (nominal)", font_size=21, color=E.DATA)
        nl.next_to(a.c2p(years[-1], np.log10(d["nominal"][-1])), RIGHT, buff=0.15).shift(UP * 0.25)
        rl = label(r"in 2017 dollars \\ (real)", font_size=21, color=E.ACCENT)
        rl.next_to(a.c2p(years[-1], np.log10(d["real"][-1])), RIGHT, buff=0.15).shift(DOWN * 0.35)
        facts = VGroup(
            label(rf"nominal: \ $\times {d['ratio_nominal']:.0f}$, \ {100 * d['growth_nominal']:.1f}\% a year",
                  font_size=24, color=E.DATA),
            label(rf"real: \ $\times {d['ratio_real']:.0f}$, \ {100 * d['growth_real']:.1f}\% a year", font_size=24,
                  color=E.ACCENT),
            label(r"the rest is prices", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        facts.move_to(a.c2p(2004, np.log10(230)))
        dep = label(rf"1929--33: \ nominal $-{100 * d['fall_29_33_nominal']:.0f}\%$, \ "
                    rf"real $-{100 * d['fall_29_33_real']:.0f}\%$", font_size=22, color=GREY_A)
        dep.move_to(a.c2p(1962, np.log10(95)))
        dep_arrow = Arrow(dep.get_top() + LEFT * 1.0, a.c2p(1933.5, np.log10(d["nominal"][4])), buff=0.1,
                          color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.12)
        tag = data_tag(rf"BEA: GDP in current dollars (GDPA) and in chained 2017 dollars (GDPCA), "
                       rf"{data.fred_cite('GDPA')}", corner=DL, font_size=15)
        with self.voiceover(
            "Here is American GDP every year since 1929, measured two ways. <bookmark mark='a'/> In white, in the "
            "dollars of each year: what the books add up to. From 1929 to 2025 it grew "
            f"{d['ratio_nominal']:.0f} times over. <bookmark mark='b'/> In gold, in the dollars of a single year, "
            f"2017: it grew {d['ratio_real']:.0f} times. <bookmark mark='c'/> The gap between them is prices. A "
            "dollar of 2025 buys much less than a dollar of 1929, and most of the growth in the white line is "
            f"inflation: {100 * d['growth_nominal']:.1f} percent a year in current dollars, "
            f"{100 * d['growth_real']:.1f} percent a year in real terms. <bookmark mark='d'/> Even the Depression "
            f"looks different. In current dollars GDP fell {100 * d['fall_29_33_nominal']:.0f} percent between "
            f"1929 and 1933. Prices fell too, so the real fall, the fall in what was actually produced, was "
            f"{100 * d['fall_29_33_real']:.0f} percent: still the worst in the country's history."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(nom, rate_func=linear), FadeIn(nl), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(real, rate_func=linear), FadeIn(rl), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(dep), GrowArrow(dep_arrow))
        self.clear_scene()

    def kuznets(self):
        k = load("kuznets")
        rows = VGroup()
        head = VGroup(VectorizedPoint(), *[label(str(y), font_size=24, color=GREY_B) for y in k["years"]])
        r1 = VGroup(label(r"income paid out, \$ billion", font_size=22, color=E.HOUSEHOLDS),
                    *[label(f"{v / 1000:.1f}", font_size=24) for v in k["paid_out"]])
        r2 = VGroup(label(r"cost of living, 1929 $= 100$", font_size=22, color=FISHER),
                    *[label(f"{v:.1f}", font_size=24) for v in k["cost_of_living"]])
        r3 = VGroup(label(r"real income paid out, 1929 dollars", font_size=22, color=E.ACCENT),
                    *[label(f"{v / 1000:.1f}", font_size=24, color=E.ACCENT) for v in k["real_paid"]])
        for r in (head, r1, r2, r3):
            r[0].move_to([-3.6, 0, 0], aligned_edge=RIGHT)
            for i in range(1, 5):
                r[i].move_to([-2.4 + 1.7 * i, 0, 0])
            rows.add(r)
        rows.arrange(DOWN, buff=0.5).move_to(UP * 0.6)
        for r in rows:
            r[0].set_x(-3.6 - r[0].width / 2)
            for i in range(1, 5):
                r[i].set_x(-2.4 + 1.7 * i)
        div = MathTex(r"\text{real} = \frac{\text{nominal}}{\text{price index}} \times 100", font_size=38)
        div.to_edge(UP, buff=0.4)
        result = label(rf"nominal: \ $-{100 * k['fall_paid']:.0f}\%$ \qquad real: \ "
                       rf"$-{100 - k['real_paid_rel'][-1]:.0f}\%$", font_size=30, color=E.ACCENT).to_edge(DOWN, buff=1.4)
        caveat = label(r"but which prices? \ whose basket?", font_size=28, color=FISHER).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"National Income, 1929--32, table 1 (BLS cost-of-living index)", corner=DL, font_size=16)
        with self.voiceover(
            "Kuznets did the same thing in 1934. <bookmark mark='a'/> To turn a nominal number into a real one, "
            "divide by an index of prices. <bookmark mark='b'/> Income paid out fell from 81 billion dollars to "
            "49. <bookmark mark='c'/> But the Bureau of Labor Statistics' cost-of-living index fell too, by about "
            "a fifth. <bookmark mark='d'/> So in dollars of 1929, income paid out fell from 81 billion to 61: "
            f"by {100 - k['real_paid_rel'][-1]:.0f} percent, not {100 * k['fall_paid']:.0f}. Everything rests on "
            "the price index. <bookmark mark='e'/> And a price index hides a question with no single answer."
        ) as vo:
            self.play(Write(div), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(FadeIn(r1))
            vo.wait_until("c")
            self.play(FadeIn(r2))
            vo.wait_until("d")
            self.play(FadeIn(r3), FadeIn(result))
            vo.wait_until("e")
            self.play(FadeIn(caveat))
        self.clear_scene()

    def formulas(self):
        basket = VGroup(fish_glyph(0.8), coconut(0.2), fish_glyph(0.8), coconut(0.2), coconut(0.2)).arrange(
            RIGHT, buff=0.25)
        bl = label(r"a basket: \ so many fish, \ so many coconuts, \dots", font_size=26, color=GREY_A)
        top = VGroup(basket, bl).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.5)
        las = VGroup(
            label(r"\'Etienne Laspeyres, 1871: \ the \emph{old} basket", font_size=26, color=LASP),
            MathTex(r"P_L = \frac{\sum_i p_{i1}\, q_{i0}}{\sum_i p_{i0}\, q_{i0}}", font_size=46, color=LASP),
        ).arrange(DOWN, buff=0.25)
        pas = VGroup(
            label(r"Hermann Paasche, 1874: \ the \emph{new} basket", font_size=26, color=PAAS),
            MathTex(r"P_P = \frac{\sum_i p_{i1}\, q_{i1}}{\sum_i p_{i0}\, q_{i1}}", font_size=46, color=PAAS),
        ).arrange(DOWN, buff=0.25)
        VGroup(las, pas).arrange(RIGHT, buff=1.2).move_to(UP * 0.2)
        key = label(r"$p$: \ prices; \ $q$: \ quantities; \ 0: \ the first year, \ 1: \ the second", font_size=22,
                    color=GREY_B).next_to(VGroup(las, pas), DOWN, buff=0.4)
        sub = label(r"when a price rises, \ people buy less of that good", font_size=26, color=E.DEMAND)
        sub.to_edge(DOWN, buff=1.1)
        over = label(r"the old basket over-weights what got dearer; \ the new basket under-weights it", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "To measure the price level, you price a basket of goods in two years and compare. "
            "<bookmark mark='a'/> In 1871 a German economist, Étienne Laspeyres, proposed the obvious basket: "
            "what people bought in the first year. Price it at the old prices and at the new, and divide. "
            "<bookmark mark='b'/> Three years later Hermann Paasche proposed the other obvious basket: what people "
            "buy now. <bookmark mark='c'/> If people bought the same things in both years, the two would agree. But "
            "they don't, and the reason is the subject of Part two: when the price of something rises, people buy "
            "less of it. <bookmark mark='d'/> So the old basket gives too much weight to the goods that got dearer, "
            "and the new basket too little. Which one is right? Before I tell you, you'll work it out yourself."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(las, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(pas, shift=UP * 0.2), FadeIn(key))
            vo.wait_until("c")
            self.play(FadeIn(sub))
            vo.wait_until("d")
            self.play(FadeIn(over))
        self.clear_scene()
