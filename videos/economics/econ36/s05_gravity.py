from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


class Gravity(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Gravity", r"How much does distance cost, and does a border?", "Chapter four. Gravity.",
             lit={1962: r"Tinbergen", 1995: r"McCallum", 2003: r"Anderson and van Wincoop", 2006: r"PPML"},
             scale=("nation", "world"), horizon=("a year",))
        self.germany()
        self.table()
        self.fit()
        self.borders()

    def germany(self):
        G = load("gravity")
        ax = plane([np.log(300), np.log(20000)], [np.log(1e-3), np.log(300)], center=LEFT * 1.8 + DOWN * 0.4,
                   x_length=8.6, y_length=4.6, xticks=[float(np.log(x)) for x in (500, 1000, 2000, 5000, 10000, 20000)],
                   yticks=[float(np.log(x)) for x in (0.01, 0.1, 1, 10, 100)], xlabel=r"distance from Germany, \ km "
                   r"(log scale)", ylabel=r"Germany's exports per \$1,000 of the partner's GDP (log)",
                   xfmt=lambda v: f"{np.exp(v):,.0f}", yfmt=lambda v: f"{np.exp(v):g}", font_size=13)
        pts = VGroup(*[Dot(ax.ax.c2p(np.log(dd), np.log(r)), radius=0.04, color=ARCH)
                       for dd, r in zip(G["de_dist"], G["de_rel"]) if r > 1e-3 and 300 <= dd <= 20000])
        lx = np.log(np.array(G["de_dist"]))
        ly = np.log(np.array(G["de_rel"]))
        ok = np.isfinite(ly) & (np.array(G["de_rel"]) > 1e-3)
        c = np.polyfit(lx[ok], ly[ok], 1)
        fit = seg(ax, np.log(400), c[1] + c[0] * np.log(400), np.log(18000), c[1] + c[0] * np.log(18000), WHITE, 3)
        side = VGroup(
            label(r"each dot: \ one of \\ Germany's partners", font_size=18, color=ARCH),
            label(rf"slope {G['de_slope']:.2f}: \\ twice as far, \\ about half the trade", font_size=19,
                  color=WHITE),
            label(r"Tinbergen (1962): \\ the same shape \\ for every country", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"CEPII Gravity database (BACI), \ 2019", corner=DR, font_size=12)
        with self.voiceover(
            "In 1962 the Dutch economist Jan Tinbergen noticed that trade between two countries behaves like "
            "Newton's gravity: it grows with their sizes and falls with the distance between them. "
            "<bookmark mark='a'/> Here are Germany's exports in 2019 to each of its partners, divided by the "
            "partner's GDP, against distance, both on log scales. <bookmark mark='b'/> The cloud falls along a line "
            f"with a slope of {G['de_slope']:.2f}: twice as far, roughly half the trade, even though shipping a "
            "container twice as far does not cost twice as much. <bookmark mark='c'/> Every country's exports look "
            "like this. Gravity is the most reliable regularity in empirical economics."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.01), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def table(self):
        G = load("gravity")
        rows = VGroup(label(r"", font_size=20), label(r"least squares", font_size=20, color=GREY_A),
                      label(r"PPML, \ fixed effects", font_size=20, color=GREY_A))
        grid = VGroup()
        names = G["names"]
        ols = dict(zip(names, G["ols"]))
        ppml = dict(zip(G["ppml_names"], G["ppml"]))
        for k, nm in enumerate(names):
            y = 1.9 - 0.52 * k
            grid.add(label(tex_safe(nm), font_size=20, color=WHITE).move_to(np.array([-3.2, y, 0])))
            grid.add(label(f"{ols[nm]:+.2f}", font_size=20, color=ARCH).move_to(np.array([1.0, y, 0])))
            grid.add(label(f"{ppml[nm]:+.2f}" if nm in ppml else r"(absorbed)", font_size=20,
                           color=GAIN if nm in ppml else GREY_B).move_to(np.array([4.0, y, 0])))
        rows[1].move_to(np.array([1.0, 2.5, 0]))
        rows[2].move_to(np.array([4.0, 2.5, 0]))
        foot = label(rf"{G['n']:,} country pairs, \ 2019; \ PPML works in levels and absorbs each exporter's and "
                     r"importer's size", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Santos Silva and Tenreyro, \ \emph{REStat} 88(4) (2006); \ CEPII (2019); \ this film",
                            corner=DR, font_size=12)
        with self.voiceover(
            f"Estimated on all {G['n']:,} pairs of countries, the equation fits remarkably. <bookmark mark='a'/> "
            "By least squares on the logarithms, trade rises almost one for one with the importer's GDP, falls "
            f"with distance with an elasticity of {G['ols'][2]:.2f}, and a shared border, a common language, a "
            "colonial past and a trade agreement each multiply it by about two or three. <bookmark mark='b'/> "
            "João Santos Silva and "
            "Silvana Tenreyro showed in 2006 that logarithms bias these estimates when errors vary with size, and "
            "proposed estimating the equation in levels by Poisson pseudo-maximum likelihood, with a fixed effect "
            f"for each exporter and importer. Then distance's elasticity is {G['ppml'][0]:.2f}, and the other "
            "effects shrink. The method is now the standard."
        ) as vo:
            self.play(FadeIn(rows[1:]), FadeIn(grid[0::3]), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in grid[1::3]], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g) for g in grid[2::3]], lag_ratio=0.15), FadeIn(foot))
        self.clear_scene()

    def fit(self):
        F = load("fit")
        y, mu = np.log10(np.array(F["y"]) / 1e6), np.log10(np.array(F["mu"]) / 1e6)
        ax = plane([-4, 3], [-4, 3], center=LEFT * 2.2 + DOWN * 0.4, x_length=5.4, y_length=5.4,
                   xticks=[-4, -2, 0, 2], yticks=[-4, -2, 0, 2], xlabel=r"predicted, \ \$ billions (log)",
                   ylabel=r"actual, \ \$ billions (log)", xfmt=lambda v: f"{10 ** v:g}", yfmt=lambda v: f"{10 ** v:g}",
                   font_size=13)
        pts = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.022, color=ARCH, fill_opacity=0.5)
                       for a, b in zip(mu, y) if -4 <= a <= 3 and -4 <= b <= 3])
        diag = seg(ax, -4, -4, 3, 3, WHITE, 2, dashed=True)
        names = {"USA-CAN": r"America to Canada", "CHN-USA": r"China to America", "DEU-FRA": r"Germany to France",
                 "AUS-NZL": r"Australia to New Zealand"}
        marks = VGroup()
        for k, nm in names.items():
            if k in F["labels"]:
                a, b = (np.log10(v / 1e6) for v in F["labels"][k][::-1])
                marks.add(VGroup(dot(ax, a, b, WHITE, 0.07), label(nm, font_size=14, color=WHITE).next_to(
                    ax.ax.c2p(a, b), LEFT, buff=0.12)))
        side = VGroup(
            label(r"each dot: \ one pair of countries, \\ 2019 (1,500 of 28,107)", font_size=17, color=GREY_A),
            label(r"predicted from distance, \ borders, \\ language, \ colonial ties, \\ agreements, \ and each "
                  r"\\ country's fixed effect", font_size=17, color=WHITE),
            label(rf"variance of log trade \\ explained: \ {100 * F['r2_logs']:.0f}\%", font_size=19, color=ARCH),
            label(rf"of trade in dollars: \ {100 * F['r2_levels']:.0f}\%", font_size=19, color=ARCH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"CEPII Gravity database (BACI), \ 2019; \ PPML computed", corner=DR, font_size=12)
        with self.voiceover(
            "How well does gravity actually fit? Take the Poisson fit with each country's fixed effect, and "
            "compare its prediction for every pair of countries with the trade that happened. "
            "<bookmark mark='a'/> Each dot is a pair; on the diagonal, the prediction is exact. <bookmark mark='b'/> "
            "The big flows sit close to it: America's exports to Canada, China's to America, Germany's to France. "
            "<bookmark mark='c'/> Across all pairs, the equation explains about "
            f"{100 * F['r2_logs']:.0f} percent of the variation in log trade, <bookmark mark='d'/> and "
            f"{100 * F['r2_levels']:.0f} percent of the variation in dollars, because the largest flows, which carry "
            "most of world trade, are predicted best. The scatter around the line is where the interesting economics "
            "lives: pairs that trade much more, or much less, than their geography says."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(diag), FadeIn(pts, lag_ratio=0.001), FadeIn(side[0]),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m_) for m_ in marks], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def borders(self):
        G = load("gravity")
        cards = point_cards([
            (r"McCallum (1995)", rf"Canadian provinces \\ traded about {G['mccallum']} times \\ more with each "
                                 r"other \\ "
                                 r"than with US states \\ of the same size and distance", TARIFF),
            (r"Anderson and van Wincoop (2003)", r"trade depends on \\ costs relative to \\ all other partners: \\ "
                                                 r"`multilateral resistance'; \\ the border effect shrinks", GAIN),
            (r"what remains", r"the border still \\ cuts trade a lot, \\ with tariffs between \\ the US and Canada "
                              r"\\ already low", WHITE),
        ], width=12.6, cols=3, font_size=20).move_to(DOWN * 0.1)
        head = label(r"the border puzzle", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.MCCALLUM_1995.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Gravity also measures borders. <bookmark mark='a'/> In 1995 John McCallum used data on trade between "
            "Canadian provinces and found that, in 1988, provinces traded about twenty-two times more with each "
            "other than with American states of the same size and distance, across one of the world's most open "
            "borders. <bookmark mark='b'/> James Anderson and Eric van Wincoop showed in 2003 that part of the "
            "puzzle was a mistake: what matters is the cost of trading with a partner relative to all the others, "
            "which they called multilateral resistance, and for a small country like Canada that changes the "
            "answer a great deal. <bookmark mark='c'/> But the border effect that remains is still large. Borders "
            "matter for reasons tariffs do not capture: currencies, rules, networks, trust."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
