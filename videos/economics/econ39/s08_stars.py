from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Stars(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Superstars and the labour share", r"Why does the top pull away?",
             "Chapter seven. Superstars and the labour share.",
             lit={1981: r"Rosen", 2020: r"Autor et al."}, scale=("person", "firm", "nation"),
             horizon=("a decade",))
        self.rosen()
        self.share()

    def rosen(self):
        S = load("stars")
        ks, cols = S["reach"], (GREY_B, COLLEGE, LOSS)
        ax = plane([0.75, 1.35], [0, 6], center=LEFT * 2.2 + DOWN * 0.4, x_length=7.4, y_length=4.8,
                   xticks=[0.8, 0.9, 1.0, 1.1, 1.2, 1.3], yticks=[0, 2, 4, 6],
                   xlabel=r"talent \ (the median performer = 1)", ylabel=r"earnings \ (the median = 1)",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        q = np.linspace(0.75, 1.35, 80)
        curves = VGroup(*[path(ax, q, q ** k, c, 3.2, yr=(0, 6)) for k, c in zip(ks, cols)])
        side = VGroup(
            label(rf"the top 1\% of talent \\ has {100 * S['talent_top1']:.1f}\% of all talent", font_size=18,
                  color=WHITE),
            *[label(rf"reach {k:g}: \ the top 1\% earn {100 * t:.1f}\% \\ of all earnings; \ the 99th \\ "
                    rf"percentile earns {r:.1f} times the median", font_size=16, color=c)
              for k, t, r, c in zip(ks, S["top1"], S["p99_p50"], cols)],
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 1981 Sherwin Rosen asked why the best performers in some trades earn so much more than the "
            "merely good, when their talents differ so little. His answer was reach. <bookmark mark='a'/> On the "
            "Island, talent varies only a little: the most talented one percent hold "
            f"{100 * S['talent_top1']:.1f} percent of all talent. If a performer can only serve a room, earnings "
            "track talent, the grey line. <bookmark mark='b'/> When a recording or a broadcast lets one performer "
            "serve a whole country, audiences flock to the best, and earnings become a steep function of talent. "
            "<bookmark mark='c'/> Steeper still, and a tiny edge in talent becomes a vast difference in pay: with "
            f"the steepest curve, the top one percent take {100 * S['top1'][-1]:.1f} percent of earnings, and the "
            f"ninety-ninth percentile earns {S['p99_p50'][-1]:.1f} times the median. Technology that widens reach "
            "stretches the top of the distribution, for singers, surgeons, chief executives and software."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(curves[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(curves[0], color=WHITE), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(curves[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(curves[2]), FadeIn(side[3]))
        self.clear_scene()

    def share(self):
        S = load("stars")
        ys, v = np.array(S["ls_years"]), np.array(S["labour_share"])
        ax = plane([1946, 2027], [90, 120], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.6, y_length=4.6,
                   xticks=[1950, 1970, 1990, 2010], yticks=[90, 100, 110, 120],
                   ylabel=r"labour share, \ nonfarm business \ (index, \ 2017 = 100)", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=14)
        ln = path(ax, ys, v, WAGE, 3.2, smooth=False)
        k80 = list(ys).index(1980)
        m = VGroup(dot(ax, 1980, v[k80], WAGE, 0.08), dot(ax, ys[-1], v[-1], WAGE, 0.08))
        side = VGroup(
            label(rf"1980: \ {v[k80]:.0f}; \ {ys[-1]}: \ {v[-1]:.0f}", font_size=19, color=WAGE),
            label(r"most of the fall: \\ value added moving \\ to firms with \\ low labour shares", font_size=18,
                  color=WHITE),
            label(r"where concentration \\ rose most, \ the labour \\ share fell most", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"BLS via FRED; \ " + tables.ADKPV_2020.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Superstars can be firms as well as people. <bookmark mark='a'/> Here is the share of income in "
            "America's business sector that goes to labour, as an index. It was steady for decades; since 1980 it "
            f"has fallen by about {100 * (1 - v[-1] / v[k80]):.0f} percent. <bookmark mark='b'/> In 2020 David "
            "Autor, David Dorn, Lawrence Katz, Christina Patterson and John Van Reenen looked inside, firm by firm. "
            "The typical firm's labour share barely fell. What changed is that sales and value added moved towards "
            "a few superstar firms, which are highly productive and pay a small share of their revenue to labour. "
            "<bookmark mark='c'/> The industries where concentration rose most saw the largest falls in the "
            "labour share. A winner-take-most economy shifts income from wages to profits, and within wages, "
            "towards those who work at the winners."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(m), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()
