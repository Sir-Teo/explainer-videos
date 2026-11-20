from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403


class Leontief(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Leontief's paradox \ and the missing trade", r"Does America export capital-intensive goods?",
             "Chapter seven. Leontief's paradox, and the missing trade.",
             lit={1953: r"Leontief", 1980: r"Leamer", 1995: r"Trefler"}, scale=("nation", "world"),
             horizon=("a year",))
        self.table()
        self.answers()
        self.missing()

    def table(self):
        L = load("leontief")
        cells = [["", r"capital", r"labour \ (worker-years)", r"capital per worker-year"],
                 [r"exports", rf"\${L['exports']['capital']:,.0f}", f"{L['exports']['labour']:.1f}",
                  rf"\${L['k_exports']:,.0f}"],
                 [r"import replacements", rf"\${L['imports']['capital']:,.0f}", f"{L['imports']['labour']:.1f}",
                  rf"\${L['k_imports']:,.0f}"]]
        xs = (-4.6, -1.5, 1.3, 4.4)
        g = VGroup()
        for i, row in enumerate(cells):
            for j, txt in enumerate(row):
                if not txt:
                    continue
                col = GREY_A if i == 0 else ((GAIN, TARIFF)[i - 1] if j == 0 else WHITE)
                g.add(label(txt, font_size=21 if i == 0 else 24, color=col).move_to(np.array([xs[j], 1.0 - 0.9 * i,
                                                                                             0])))
        head = label(r"per million dollars of US trade, \ 1947", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.6)
        last = VGroup(*[m for m in g if abs(m.get_center()[0] - xs[3]) < 0.01])
        foot = VGroup(
            label(rf"imports would need {L['ratio']:.2f} times the capital per worker", font_size=24, color=TARIFF),
            label(r"the most capital-rich country in the world \ exported labour-intensive goods", font_size=22,
                  color=WHITE),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Leontief, \ \emph{Proc.\ American Philosophical Society} 97(4) (1953)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "The first serious test of Heckscher and Ohlin came in 1953, from Wassily Leontief, who had built the "
            "input-output table of Part three. <bookmark mark='a'/> He asked how much capital and labour it would "
            "take to make a million dollars of America's exports, counting everything that goes into them, and a "
            "million dollars of the goods America imported, if America had to make them itself. "
            "<bookmark mark='b'/> Per worker-year, the exports needed about fourteen thousand dollars of capital; "
            "the import replacements about eighteen thousand. <bookmark mark='c'/> The richest country in capital "
            "in the world, in 1947, was exporting labour-intensive goods and importing capital-intensive ones. The "
            "opposite of the theory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(VGroup(*[m for m in g if m not in last])))
            vo.wait_until("a")
            self.play(Indicate(VGroup(*g[4:7]), color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(last))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def answers(self):
        cards = point_cards([
            (r"skills", r"American workers \\ were more skilled: \\ count human capital, \\ and exports look \\ "
                        r"skill-intensive", LABOUR),
            (r"land and resources", r"many imports \\ were minerals \\ and crops that need \\ what America lacked",
             LAND),
            (r"technology", r"Leontief's own answer: \\ American labour \\ was more productive, \\ so effectively "
                            r"\\ abundant", ISLAND),
            (r"the wrong test", r"Leamer (1980): \\ with unbalanced trade, \\ compare production \\ with consumption; "
                                r"\\ then America is \\ capital-abundant", CAPITAL),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"a paradox with four answers", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(r"Leontief (1953, 1956); \ Leamer, \ \emph{JPE} 88(3) (1980)", corner=DR, font_size=12)
        with self.voiceover(
            "The paradox drew answers for decades. <bookmark mark='a'/> American workers were more skilled than "
            "most; count their skill as a kind of capital, and the exports look intensive in it. "
            "<bookmark mark='b'/> Many imports were raw materials that need land, mines or climate America lacked. "
            "<bookmark mark='c'/> Leontief's own answer was that American workers were so productive that, counted "
            "in efficiency units, labour was America's abundant factor. <bookmark mark='d'/> And in 1980 Edward "
            "Leamer showed that with unbalanced trade, as America's was in 1947, Leontief's comparison is the wrong "
            "test; the right one, comparing what the country produces with what it consumes, shows America "
            "abundant in capital after all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def missing(self):
        L = load("leontief")
        ax = plane([-3.5, 5], [-3.5, 5], center=LEFT * 2.2 + DOWN * 0.3, x_length=5.2, y_length=5.2,
                   xticks=[-2, 0, 2, 4], yticks=[-2, 0, 2, 4], xlabel=r"predicted by endowments",
                   ylabel=r"measured in trade", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        diag = seg(ax, -3.5, -3.5, 5, 5, GREY_B, 1.5, dashed=True)
        pts = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.045, color=CAPITAL if f == "capital" else
                           (LAND if f in ("cropland", "pasture") else LABOUR))
                       for x, y, f in zip(L["predicted"], L["measured"], L["factor"])
                       if -3.5 <= x <= 5 and -3.5 <= y <= 5])
        side = VGroup(
            label(rf"{L['n_countries']} countries, \ {L['n_factors']} factors, \ 1983", font_size=19, color=WHITE),
            label(r"the theory: \ every point \\ on the dashed line", font_size=19, color=GREY_B),
            label(rf"right sign: \ {100 * L['sign_test']:.0f}\% \\ (a coin would get 50\%)", font_size=19,
                  color=TARIFF),
            label(rf"measured variance: \\ {L['variance_ratio']:.3f} of predicted \\ "
                  rf"(Trefler: {L['paper_variance']:.3f})",
                  font_size=19, color=CAPITAL),
            label(r"the missing trade: \\ fixed by productivity \\ differences and home bias", font_size=18,
                  color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"Trefler, \ \emph{AER} 85(5) (1995): \ his data, \ this film's computation", corner=DR,
                       font_size=12)
        with self.voiceover(
            "The modern test uses every factor and every country at once. <bookmark mark='a'/> In 1995 Daniel "
            "Trefler took thirty-three countries and nine factors, kinds of labour, capital and land, in 1983. "
            "For each, the theory predicts how much of the factor a country's trade should carry, from how much of "
            "it the country has compared with its share of world spending. <bookmark mark='b'/> If the theory held, "
            "every point would sit on the dashed line. <bookmark mark='c'/> Instead, recomputed here from Trefler's "
            f"own data, the measured content has the right sign {100 * L['sign_test']:.0f} percent of the time, "
            "no better than a coin. <bookmark mark='d'/> And the points lie almost flat: the measured factor content "
            f"has about {1 / L['variance_ratio']:.0f} times less variance than the prediction. Trefler called it "
            "the case of the "
            "missing trade. <bookmark mark='e'/> His remedy, and Donald Davis and David Weinstein's after him, was "
            "to let technology differ across countries, as Ricardo had, and to let people prefer goods made at "
            "home. With both, the theory fits far better. Ricardo and Heckscher and Ohlin are not rivals: real "
            "trade needs both."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.004), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(diag), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
