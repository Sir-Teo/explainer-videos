from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Frontier: \ whose inflation, \ whose welfare?", r"If prices rise differently for rich and "
             r"poor, and tastes change with income, what is ``the'' cost of living?", "Chapter thirteen. Frontier: "
             "whose inflation, whose welfare?", scale=("household", "nation"), horizon=("a decade",))
        self.jaravel()
        self.variety()
        self.nonhomothetic()

    def jaravel(self):
        j = load("frontier")["jaravel"]
        from explainer.ai.viz import axes

        items = [(r"retail goods", j["retail_gap"], COCO), (r"retail, \\ with new products", j["retail_gap_variety"],
                                                              GIFF),
                 (r"the whole \\ basket (CEX)", j["full_basket_gap"], HICKS)]
        ax = axes([0, 3], [0, 1.0], x_length=5.6, y_length=4.4, xticks=None, yticks=[0, 0.25, 0.5, 0.75, 1.0],
                  ylabel=r"points a year", font_size=17, yfmt=lambda v: f"{v:.2f}", center=LEFT * 3.2 + DOWN * 0.45)
        a = ax.ax
        bars = VGroup()
        for k, (n, (v, se), col) in enumerate(items):
            r = Polygon(a.c2p(k + 0.2, 0), a.c2p(k + 0.8, 0), a.c2p(k + 0.8, v), a.c2p(k + 0.2, v), stroke_width=0,
                        fill_color=col, fill_opacity=0.85)
            wh = Line(a.c2p(k + 0.5, v - 1.96 * se), a.c2p(k + 0.5, v + 1.96 * se), color=WHITE, stroke_width=2.5)
            t = label(rf"{v:.2f}", font_size=21, color=col).next_to(wh, UP, buff=0.06)
            nm = label(n, font_size=17, color=GREY_A).next_to(a.c2p(k + 0.5, 0), DOWN, buff=0.12)
            bars.add(VGroup(r, wh, t, nm))
        head = label(r"inflation of the poorest fifth \ minus \ the richest fifth, \ 2004--2015", font_size=24,
                     color=E.ACCENT).next_to(ax, UP, buff=0.15)
        side = VGroup(
            label(r"Jaravel (2019): \ scanner data, \\ barcode by barcode, \ priced \\ for each household's own "
                  r"basket", font_size=22),
            label(rf"over twelve years, \ {j['retail_gap'][0]:.2f} a year \\ is about "
                  rf"{100 * ((1 + j['retail_gap'][0] / 100) ** 12 - 1):.0f}\% of purchasing power", font_size=22,
                  color=COCO),
            label(r"why? \ new products are aimed \\ at the growing market of the \\ better-off, \ and competition "
                  r"there \\ holds prices down", font_size=22, color=GIFF),
            label(rf"his calibration: \ over {100 * j['share_explained']:.0f}\% of the gap", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Jaravel, QJE 134(2) (2019), abstract", corner=DR, font_size=13)
        with self.voiceover(
            "The frontier starts from a fact the textbook index hides: different households face different "
            "inflation. <bookmark mark='a'/> Xavier Jaravel used scanner data, which record purchases barcode by "
            "barcode, to price each household's own basket. <bookmark mark='b'/> From 2004 to 2015, retail "
            "inflation for the poorest fifth of American households ran about two thirds of a point a year above "
            "that of the richest fifth; counting new products, almost nine tenths of a point; over the whole "
            "basket, about a third of a point. <bookmark mark='c'/> Two thirds of a point for twelve years is about "
            "eight percent of purchasing power. <bookmark mark='d'/> His explanation runs through demand: as the "
            "better-off grow richer, firms launch new products for them, and competition in those markets holds "
            "their prices down. By his calibration that channel explains more than half of the gap."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(head), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Indicate(side[0], color=E.ACCENT))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def variety(self):
        f = load("frontier")
        from explainer.ai.viz import axes

        lam = np.array(f["lam"])
        ax = axes([0.8, 1.0], [0.85, 1.0], x_length=6.0, y_length=4.6, xticks=[0.8, 0.85, 0.9, 0.95, 1.0],
                  yticks=[0.85, 0.9, 0.95, 1.0], xlabel=r"share of spending on goods sold last year too",
                  ylabel=r"the price index's correction", font_size=17, xfmt=lambda v: f"{v:.2f}",
                  yfmt=lambda v: f"{v:.2f}", center=LEFT * 3.0 + DOWN * 0.35)
        a = ax.ax
        cols = {"2": GIFF, "4": E.ACCENT, "8": HICKS}
        curves = VGroup()
        for s, col in cols.items():
            ys = np.array(f["curves"][s])
            pts = [a.c2p(x, y) for x, y in zip(lam, ys) if y >= 0.85]
            ln = VMobject(stroke_color=col, stroke_width=4).set_points_smoothly(pts)
            curves.add(VGroup(ln, label(rf"$\sigma = {s}$", font_size=19, color=col).next_to(pts[0], UP, buff=0.08)))
        ex = f["example"]
        dot = Dot(a.c2p(0.95, ex), radius=0.09, color=WHITE)
        side = VGroup(
            label(r"Feenstra (1994): \ with CES tastes, \\ new goods lower the true index by", font_size=23),
            MathTex(r"\Big(\frac{\lambda_1}{\lambda_0}\Big)^{1/(\sigma - 1)}", font_size=40, color=E.ACCENT),
            label(rf"5\% of spending on new goods, \ $\sigma = 4$: \\ the cost of living {100 * (1 - ex):.1f}\% lower",
                  font_size=22, color=WHITE),
            label(r"the less a new good resembles the old, \\ the more it's worth", font_size=22, color=GREY_A),
            label(r"Redding and Weinstein (2020): \ when tastes \\ for particular goods shift too, \ the usual \\ "
                  r"index is biased up", font_size=22, color=HICKS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(r"computed: agora.demand.feenstra", corner=DR, font_size=13)
        with self.voiceover(
            "Measuring that requires a price index that counts new goods, which chapter nine did by hand for one "
            "cereal. <bookmark mark='a'/> Robert Feenstra showed in 1994 that with CES tastes the correction has a "
            "simple form: the share of spending on goods that existed in both periods, raised to one over sigma "
            "minus one. <bookmark mark='b'/> If five percent of this year's spending goes on goods that didn't "
            "exist last year, and sigma is four, the true cost of living is one point seven percent lower than the "
            "index of continuing goods says. The less substitutable the new goods, the larger the gain. "
            "<bookmark mark='c'/> Stephen Redding and David Weinstein added in 2020 that tastes for particular goods "
            "shift too, and that ignoring those shifts biases the usual index upward."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Write(side[1]), LaggedStart(*[Create(c_) for c_ in curves], lag_ratio=0.3),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(dot, scale=1.5), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def nonhomothetic(self):
        j = load("frontier")["jaravel"]
        cards = point_cards([
            (r"tastes change with income",
             rf"Jaravel and Lashkari (2024): \ a chained index \\ assumes they don't; \ correcting for it, \\ real "
             rf"consumption in 1955 was understated \\ by {100 * j['lashkari_1955_understated']:.1f}\%, \ and growth "
             rf"since \\ is {j['lashkari_growth_bp']} basis points a year lower", E.ACCENT),
            (r"prices you can't see",
             r"Atkin, Faber, Fally and Gonzalez-Navarro \\ (2024): \ where many prices are missing, \\ relative Engel "
             r"curves still recover \\ welfare by income group: \ rural India, \\ 1987--2000", HICKS),
            (r"one number, \ many households",
             r"the cost of living depends on who you are: \\ what you buy, \ how you'd substitute, \\ and what's "
             r"new on your shelves", GIFF),
        ], width=13.2, cols=3, font_size=22).move_to(DOWN * 0.2)
        head = label(r"The frontier: \ welfare that depends on who you are", font_size=34).to_edge(UP, buff=0.5)
        tag = published_tag(r"Jaravel and Lashkari, QJE 139(1); Atkin et al., QJE 139(1) (2024)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Two papers from 2024 push the theory of this part to its limit. <bookmark mark='a'/> Xavier Jaravel "
            "and Danial Lashkari start from Engel: when tastes change with income, an ordinary chained index answers "
            "the wrong question. Correcting for it, American real consumption per household in 1955 was understated "
            "by eleven and a half percent, and growth since then has been eighteen basis points a year slower than "
            "measured. <bookmark mark='b'/> David Atkin and his co-authors take Hamilton's idea further: where "
            "prices for much of what people buy are missing, the way spending shares shift with income still "
            "recovers welfare changes for each income group, which they did for rural India between 1987 and 2000. "
            "<bookmark mark='c'/> The common thread: the cost of living is not one number. It depends on what you "
            "buy, how you'd substitute, and what is new on your shelves. Duality, Engel curves and Slutsky's two "
            "effects are the tools that measure it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c_ in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.15))
        self.clear_scene()
