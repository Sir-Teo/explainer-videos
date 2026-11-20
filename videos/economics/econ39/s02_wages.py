from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Wages(VoiceoverScene):
    def construct(self):
        card(self, 1, r"The wage distribution since 1979", r"Who gained, \ and who did not?",
             "Chapter one. The wage distribution since 1979.",
             lit={1979: r"the BLS's earnings series", 2013: r"Autor and Dorn"}, scale=("nation",),
             horizon=("a decade", "a century"))
        self.premium()
        self.spread()
        self.hollow()

    def premium(self):
        W = load("wages")
        ys, r = np.array(W["years"]), np.array(W["ratio"])
        dr = np.exp(np.array(W["dropout"]))
        ax = plane([1978, 2026], [1.0, 2.0], center=LEFT * 1.4 + DOWN * 0.4, x_length=9.0, y_length=4.8,
                   xticks=[1980, 1990, 2000, 2010, 2020], yticks=[1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
                   ylabel=r"median weekly earnings, \ ratio", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        ln = path(ax, ys, r, COLLEGE, 3.4, smooth=False)
        ln2 = path(ax, ys, dr, HSCHOOL, 2.6, smooth=False)
        k92 = list(ys).index(1992)
        marks = VGroup(dot(ax, ys[0], r[0], COLLEGE, 0.08), dot(ax, 1992, r[k92], COLLEGE, 0.08),
                       dot(ax, ys[-1], r[-1], COLLEGE, 0.08))
        side = VGroup(
            label(r"college graduates \\ over high-school graduates", font_size=18, color=COLLEGE),
            label(rf"1979: \ {r[0]:.2f}; \ 1992: \ {r[k92]:.2f}; \\ 2025: \ {r[-1]:.2f}", font_size=18,
                  color=WHITE),
            label(r"high-school graduates \\ over dropouts", font_size=18, color=HSCHOOL),
            label(r"full-time workers aged 25 and over", font_size=15, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BLS, \ Current Population Survey, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Start with the simplest measure of how education is paid. <bookmark mark='a'/> In 1979 the median "
            "full-time worker with a college degree earned "
            f"{r[0]:.2f} times as much each week as the median high-school graduate. <bookmark mark='b'/> By 1992 "
            f"the ratio was {r[k92]:.2f}: most of the rise came in a single decade, the 1980s. <bookmark mark='c'/> "
            f"Since then it has crept up, to {r[-1]:.2f} in 2025, and has hardly moved for fifteen years. "
            "<bookmark mark='d'/> Below it, the gap between high-school graduates and those who never finished "
            "widened too. Whatever happened, it rewarded schooling, and it happened fastest in the 1980s."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(side[3]))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(marks[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(marks[1], scale=1.5), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(marks[2], scale=1.5))
            vo.wait_until("d")
            self.play(Create(ln2), FadeIn(side[2]), run_time=1.5)
        self.clear_scene()

    def spread(self):
        W = load("wages")
        yr, real = np.array(W["real_years"]), np.array(W["real"])
        yd = np.array(W["dec_years"])
        ax1 = plane([1978, 2026], [300, 400], center=LEFT * 3.6 + DOWN * 0.3, x_length=5.6, y_length=4.2,
                    xticks=[1980, 2000, 2020], yticks=[300, 350, 400], ylabel=r"median weekly earnings, \ 1982--84 \$",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        ax2 = plane([1999, 2026], [1.5, 5.0], center=RIGHT * 3.2 + DOWN * 0.3, x_length=5.6, y_length=4.2,
                    xticks=[2000, 2010, 2020], yticks=[2, 3, 4, 5], ylabel=r"ratio of weekly earnings",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        l1 = path(ax1, yr, real, WAGE, 3.0, smooth=False)
        l90 = path(ax2, yd, W["r9010"], E.ACCENT, 3.0, smooth=False)
        l95 = path(ax2, yd, W["r9050"], COLLEGE, 2.6, smooth=False)
        l51 = path(ax2, yd, W["r5010"], HSCHOOL, 2.6, smooth=False)
        k1 = label(rf"90th over 10th: \ {W['r9010'][0]:.2f} $\to$ {W['r9010'][-1]:.2f}", font_size=15,
                   color=E.ACCENT)
        k2 = label(rf"90th over median: \ {W['r9050'][0]:.2f} $\to$ {W['r9050'][-1]:.2f}", font_size=15,
                   color=COLLEGE)
        k3 = label(rf"median over 10th: \ {W['r5010'][0]:.2f} $\to$ {W['r5010'][-1]:.2f}", font_size=15,
                   color=HSCHOOL)
        VGroup(k1, k2, k3).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax2, DOWN, buff=0.25)
        n1 = label(rf"\${W['real1979']:.0f} in 1979, \ \${W['real2025']:.0f} in 2025: \ "
                   rf"+{100 * (W['real2025'] / W['real1979'] - 1):.0f}\% in 46 years", font_size=16,
                   color=WAGE).next_to(ax1, DOWN, buff=0.35)
        tag = data_tag(r"BLS, \ Current Population Survey, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "What about the typical worker? <bookmark mark='a'/> The median full-time worker's weekly pay, in "
            f"dollars of 1982 to 1984, was {W['real1979']:.0f} in 1979 and {W['real2025']:.0f} in 2025: "
            f"{100 * (W['real2025'] / W['real1979'] - 1):.0f} percent more in forty-six years, while output per hour "
            f"worked in the business sector grew {W['prod_ratio']:.1f} times. <bookmark mark='b'/> The spread can be "
            "read from the deciles, published since 2000. "
            "A worker at the ninetieth percentile earned "
            f"{W['r9010'][0]:.1f} times as much as one at the tenth in 2000, and {W['r9010'][-1]:.1f} times in 2025. "
            "<bookmark mark='c'/> All of that widening is at the top: the ninetieth percentile pulled away from the "
            "median, <bookmark mark='d'/> while the median moved closer to the tenth, as many states raised their "
            "minimum wages and low-wage labour markets tightened after 2020."
        ) as vo:
            self.play(FadeIn(ax1), FadeIn(ax2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(l1), FadeIn(n1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(l90), FadeIn(k1), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(l95), FadeIn(k2), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(l51), FadeIn(k3), run_time=1.5)
        self.clear_scene()

    def hollow(self):
        W = load("wages")
        P = load("polar")
        p, w = np.array(W["pctile"]), np.array(P["wsmooth"])
        ax = plane([0, 100], [0.0, 0.30], center=LEFT * 1.4 + DOWN * 0.4, x_length=9.0, y_length=4.8,
                   xticks=[0, 20, 40, 60, 80, 100], yticks=[0, 0.1, 0.2, 0.3],
                   xlabel=r"occupations ranked by their 1980 mean wage \ (percentile)",
                   ylabel=r"change in log hourly wage, \ 1980--2005", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        raw = VGroup(*[dot(ax, x, y, GREY_B, 0.025) for x, y in zip(p, W["dwage8005"]) if 0 <= y <= 0.3])
        ln = path(ax, p, w, WAGE, 3.6)
        side = VGroup(
            label(rf"the bottom: \ +{w[:10].mean():.2f}", font_size=19, color=WAGE),
            label(rf"the middle: \ +{w[40:60].mean():.2f}", font_size=19, color=MIDS),
            label(rf"the top: \ +{w[-10:].mean():.2f}", font_size=19, color=WAGE),
            label(r"a U, \ not a ramp: \\ the hollow middle", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"Autor and Dorn (2013), \ replication data", corner=DR, font_size=12)
        with self.voiceover(
            "A sharper picture ranks occupations, not people. David Autor and David Dorn sorted every occupation by "
            "its mean wage in 1980, from the lowest paid to the highest, and asked how each one's wages grew to "
            "2005. <bookmark mark='a'/> Each grey dot is a percentile of 1980 employment; the line smooths them. "
            f"<bookmark mark='b'/> Wages at the bottom grew by about {w[:10].mean():.2f} in logs, "
            f"<bookmark mark='c'/> at the top by {w[-10:].mean():.2f}, <bookmark mark='d'/> and in the middle by only "
            f"{w[40:60].mean():.2f}. Growth was not a ramp rising with skill but a U: the middle was hollowed out. "
            "The rest of this part tries to explain both shapes."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(raw, lag_ratio=0.01), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(ln), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]), FadeIn(side[3]))
        self.clear_scene()
