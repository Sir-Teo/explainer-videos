from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403


class Zipf(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Zipf's law", r"Why are the sizes of cities so regular?",
             "Chapter five. Zipf's law.", lit={1949: r"Zipf", 1999: r"Gabaix"}, scale=("city", "nation"),
             horizon=("a century",))
        self.ranks()
        self.gibrat()
        self.fact()

    def ranks(self):
        Z = load("zipf")
        pops = np.array(Z["pops"])
        rank = np.arange(1, len(pops) + 1)
        ax = plane([4.6, 7.5], [0, 2.7], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[5, np.log10(3e5), 6, np.log10(3e6), 7], yticks=[0, 1, 2],
                   xlabel=r"population \ (log scale)", ylabel=r"rank \ (log scale)",
                   xfmt=lambda v: f"{round(10 ** v / 1e6):d}m" if v >= 5.99 else f"{round(10 ** v / 1e3):d}k",
                   yfmt=lambda v: f"{10 ** v:.0f}", font_size=14)
        pts = VGroup(*[Dot(ax.ax.c2p(np.log10(p), np.log10(r)), radius=0.03, color=CITY, fill_opacity=0.85)
                       for p, r in zip(pops, rank)])
        # the fitted line on the top 100: log(rank - 1/2) = c - zeta log(size), drawn in base 10
        z, c = Z["zeta_100"], Z["c_100"]
        x0, x1 = np.log10(pops[99]), np.log10(pops[0])
        line = seg(ax, x0, (c - z * x0 * np.log(10)) / np.log(10), x1, (c - z * x1 * np.log(10)) / np.log(10),
                   E.ACCENT, 3.0)
        side = VGroup(
            label(r"rank $\times$ size $\approx$ constant", font_size=21, color=E.ACCENT),
            label(rf"the largest 100: \\ exponent {z:.2f} \ ($\pm${Z['se_100']:.2f})", font_size=18, color=WHITE),
            label(rf"all {Z['n']}: \ {Z['zeta_all']:.2f}", font_size=18, color=GREY_A),
            label(rf"New York {Z['ny'] / 1e6:.1f}m, \\ Los Angeles {Z['second'] / 1e6:.1f}m, \\ tenth: \ "
                  rf"{Z['tenth'] / 1e6:.1f}m", font_size=17, color=CITY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"US Census Bureau, \ Vintage 2024; \ Gabaix and Ibragimov's rank $-\frac{1}{2}$ fit",
                       corner=DR, font_size=12)
        with self.voiceover(
            "In 1949 the linguist George Kingsley Zipf noticed a regularity in city sizes. Rank a country's cities "
            "by population and plot rank against size on logarithmic scales. <bookmark mark='a'/> The points fall "
            "near a straight line with a slope of about minus one: the second city is about half the size of the "
            "first, the tenth about a tenth. Rank times size is roughly constant. <bookmark mark='b'/> For "
            f"America's largest hundred metropolitan areas in 2024 the exponent is {z:.2f}, give or take "
            f"{Z['se_100']:.2f}; <bookmark mark='c'/> across all {Z['n']} it is {Z['zeta_all']:.2f}. "
            "<bookmark mark='d'/> Not exact: Los Angeles is more than half New York's size. But a law this regular "
            "across countries and centuries asks for an explanation."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(pts, lag_ratio=0.003), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def gibrat(self):
        Z = load("zipf")
        paths = np.array(Z["gibrat_paths"])
        T = paths.shape[0]
        ax1 = plane([0, T], [-3.5, 3.5], center=LEFT * 3.4 + UP * 0.2, x_length=5.6, y_length=3.8,
                    xticks=[0, T // 2, T], yticks=[-3, 0, 3], xlabel=r"time", ylabel=r"size \ (log, \ relative to "
                    r"the mean)", xfmt=lambda v: "", yfmt=lambda v: f"{v:.0f}", font_size=13)
        cols = TOWN_COLORS
        lines = VGroup(*[path(ax1, np.arange(T), np.log(np.maximum(paths[:, k], 1e-6)), cols[k % 6], 2.6,
                              smooth=False) for k in range(min(4, paths.shape[1]))])
        floor = seg(ax1, 0, np.log(Z["floor"]), T, np.log(Z["floor"]), RENT, 1.8, dashed=True)
        sizes = np.array(Z["gibrat_sizes"])
        rank = np.arange(1, len(sizes) + 1)
        ax2 = plane([0, 2.6], [0, 3.4], center=RIGHT * 3.4 + UP * 0.2, x_length=4.8, y_length=3.8,
                    xticks=[0, 1, 2], yticks=[0, 1, 2, 3], xlabel=r"size \ (log$_{10}$)", ylabel=r"rank \ (log$_{10}$)",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        lo = np.log10(sizes.min())
        pts = VGroup(*[Dot(ax2.ax.c2p(np.log10(s) - lo, np.log10(r)), radius=0.022, color=E.AGORA)
                       for s, r in zip(sizes[::4], rank[::4])])
        foot = VGroup(
            label(r"every town grows at a random rate, \ independent of its size \ (Gibrat); \ none may fall below "
                  r"the floor", font_size=18, color=WHITE),
            label(rf"20,000 towns: \ exponent {Z['gibrat_zeta']:.2f} \ (theory: \ {Z['gibrat_theory']:.2f})",
                  font_size=19, color=E.AGORA),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is one, from Xavier Gabaix in 1999. <bookmark mark='a'/> Suppose every town grows each year at a "
            "random rate whose distribution does not depend on the town's size: Robert Gibrat's law of "
            "proportional growth. Four towns' paths wander up and down. <bookmark mark='b'/> Add one more rule: no "
            "town can shrink below a floor, a small fraction of the average. <bookmark mark='c'/> Run twenty "
            "thousand towns for long enough and their sizes settle into a power law with an exponent of one over "
            f"one minus the floor, here {Z['gibrat_theory']:.2f}; the simulation gives {Z['gibrat_zeta']:.2f}. "
            "Zipf's law needs no planner and no special theory of cities: only growth that is random and "
            "proportional."
        ) as vo:
            self.play(FadeIn(ax1), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.15), FadeIn(foot[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(floor))
            vo.wait_until("c")
            self.play(FadeIn(ax2), FadeIn(pts, lag_ratio=0.002), FadeIn(foot[1]), run_time=2.0)
        self.clear_scene()

    def fact(self):
        Z = load("zipf")
        f = next(x for x in facts.FACTS if x.key == "zipf_cities")
        data_m = label(rf"America, \ 2024: \\ {Z['zeta_100']:.2f} for the top 100, \\ {Z['zeta_all']:.2f} for all "
                       rf"{Z['n']}", font_size=18, color=WHITE)
        theory_m = label(r"Gibrat's growth \\ with a floor gives \\ an exponent near one", font_size=18, color=CITY)
        agora_m = label(rf"20,000 towns: \\ {Z['gibrat_zeta']:.2f}", font_size=18, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, CITY, None)).move_to(UP * 0.3)
        tag = published_tag(r"Zipf (1949); \ Gabaix, \ \emph{QJE} 114(3) (1999); \ Census Bureau", corner=DR,
                            font_size=12)
        with self.voiceover(
            "That makes Zipf's law one of the series' facts. <bookmark mark='a'/> In America's data the exponent is "
            "close to one. <bookmark mark='b'/> The theory: random, proportional growth with a floor. "
            "<bookmark mark='c'/> And Agora reproduces it. The fit is rougher at the very top, where a handful of "
            "giant cities sit, and it holds better for the large cities than for the small."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0][2:]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1][2:]))
            vo.wait_until("c")
            self.play(FadeIn(fc.cols[2][2:]))
        self.clear_scene()
