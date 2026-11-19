from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403

LETTERS = "ABCDE"
CHIP = ("#F2C14E", "#7EC8F5", "#F2788F", "#7BD88F", "#C9A0FF")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ when did the climb begin?", r"On an empty axis from 1270 to today, \ where does "
             r"England's income per head start to rise for good?", "Chapter one. Play it: when did the climb begin?",
             lit={1270: r"the first estimate", 1800: r"?"}, scale=("nation",), horizon=("a century",))
        self.guess()
        self.reveal()
        self.log_view()

    def axis(self, center=DOWN * 0.35):
        return plane([1260, 2020], [0, 30000], center=center, x_length=11.4, y_length=4.6,
                     xticks=[1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000], yticks=[0, 10000, 20000, 30000],
                     ylabel=r"England's real GDP per head, \ pounds of 2013", xfmt=lambda v: f"{v:.0f}",
                     yfmt=lambda v: f"{v / 1000:.0f}" + r"\,000" if v else "0", font_size=17)

    def guess(self):
        p = load("playit")
        stage = game_stage(12.6, 6.4, center=DOWN * 0.1)
        ax = self.axis(center=DOWN * 0.45)
        chips = VGroup()
        for k, (y, c) in enumerate(zip(p["options"], CHIP)):
            x = ax.ax.c2p(y, 0)
            chips.add(VGroup(DashedLine(x, ax.ax.c2p(y, 26000), color=c, stroke_width=2),
                             label(rf"{LETTERS[k]}: \ {y}", font_size=21, color=c).next_to(ax.ax.c2p(y, 26000), UP,
                                                                                          buff=0.08)))
        head = label(r"England, \ 1270 to 2016: \ where does income per head start to climb for good?", font_size=22,
                     color=GREY_A).move_to(stage.box.get_top() + DOWN * 0.5)
        ring = countdown().move_to(ax.ax.c2p(1400, 15000))
        with self.voiceover(
            "Before any theory, a guess. <bookmark mark='a'/> Here is an empty axis: England, from 1270 to 2016, "
            "and on it, income per head, in pounds of 2013. <bookmark mark='b'/> Five candidates for the moment when "
            "it starts to climb for good: A, 1350; B, 1500; C, 1650; D, 1800; E, 1900. "
            "<bookmark mark='c'/> Where does the line leave the floor? Pause, and choose."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ax))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in chips], lag_ratio=0.5), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        p = load("playit")
        ax = self.axis()
        years, g = np.array(p["years"], float), np.array(p["gdppc"])
        line = path(ax, years, g, color=GDP, width=4, smooth=False)
        chips = VGroup(*[DashedLine(ax.ax.c2p(y, 0), ax.ax.c2p(y, 26000), color=c, stroke_width=1.5)
                         for y, c in zip(p["options"], CHIP)])
        k = p["key"]
        rows = VGroup(
            label(rf"1270: \ {k['1270']['gdppc']:,.0f} \quad 1650: \ {k['1650']['gdppc']:,.0f} \quad 1800: \ "
                  rf"{k['1800']['gdppc']:,.0f} \quad 2016: \ {k['2016']['gdppc']:,.0f}".replace(",", "{,}"),
                  font_size=21, color=GDP),
            label(rf"since 1800, \ $\times${p['ratio_1800_2016']:.1f}", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.15).move_to(ax.ax.c2p(1530, 20000))
        src = data_tag(data.cite("millennium"), corner=DR, font_size=12)
        with self.voiceover(
            "Here is the answer, from the Bank of England's millennium dataset, which uses Stephen Broadberry and "
            "his colleagues' reconstruction of English output. <bookmark mark='a'/> For five centuries the line "
            "lies along the floor. <bookmark mark='b'/> Around 1800 it lifts off, and it has not come down: income "
            f"per head in 2016 was about {p['ratio_1800_2016']:.0f} times its level of 1800. If you chose D, you "
            "chose the moment the floor was left behind for good."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(chips), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(line), run_time=6, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(rows), Indicate(chips[3], color=WHITE))
        self.clear_scene()

    def log_view(self):
        p = load("playit")
        years, g, w = np.array(p["years"], float), np.array(p["gdppc"]), np.array(p["wage"])
        ax = plane([1260, 2020], [np.log10(500), np.log10(40000)], center=DOWN * 0.45 + LEFT * 0.2, x_length=11.0,
                   y_length=4.6, xticks=[1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000],
                   yticks=[np.log10(v) for v in (500, 1000, 3000, 10000, 30000)],
                   ylabel=r"GDP per head, \ log scale", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), font_size=17)
        line = log_axis(ax, years, g, GDP, width=4)
        rates = [(1270, 1650, p["growth_1270_1650"]), (1650, 1800, p["growth_1650_1800"]),
                 (1800, 2016, p["growth_1800_2016"])]
        labs = VGroup()
        for a, b, r in rates:
            ya = float(np.log10(np.interp(a, years, g)))
            yb = float(np.log10(np.interp(b, years, g)))
            mid = ax.ax.c2p((a + b) / 2, (ya + yb) / 2)
            labs.add(label(rf"{100 * r:.2f}\% a year", font_size=21, color=E.ACCENT).move_to(mid + UP * 0.55))
        head = label(r"on a log scale, \ equal slopes are equal growth rates", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.35)
        wn = label(rf"real wages did not pass their level of 1450 for good until {p['wage_beyond_1450']}",
                   font_size=22, color=WAGE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A log scale tells more, because on it equal slopes mean equal rates of growth. "
            f"<bookmark mark='a'/> From 1270 to 1650, income per head grew by about {100 * p['growth_1270_1650']:.2f} "
            "percent a year: nothing. <bookmark mark='b'/> From 1650 to 1800, by more than half a percent a year: a "
            "slow climb had begun before the Industrial Revolution. <bookmark mark='c'/> From 1800, by more than one "
            "percent a year, for two centuries. <bookmark mark='d'/> And wages were slower still: English real wages "
            f"did not pass their peak of 1450, set after the Black Death, for good until {p['wage_beyond_1450']}. "
            "Something kept them down for four hundred years. Malthus thought he knew what."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), Create(line), run_time=2.5)
            for mk, lb in zip("abc", labs):
                vo.wait_until(mk)
                self.play(FadeIn(lb, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(wn))
        self.clear_scene()
