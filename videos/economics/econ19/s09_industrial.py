from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403


class Industrial(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The Industrial Revolution in numbers", r"If the machines were so remarkable, \ why did income "
             r"per head grow so slowly, \ and why did wages lag?", "Chapter seven. The Industrial Revolution in numbers.",
             lit={1845: r"Engels", 1992: r"Crafts and Harley", 2009: r"Allen's pause"}, scale=("nation",),
             horizon=("a decade", "a century"))
        self.slow()
        self.pause()

    def slow(self):
        ind = load("industrial")
        gr = ind["growth"]
        ax = plane([-0.6, 4.6], [0, 1.4], center=LEFT * 2.2 + DOWN * 0.45, x_length=7.6, y_length=4.6,
                   yticks=[0, 0.4, 0.8, 1.2], ylabel=r"growth of English GDP per head, \ \% a year", font_size=17)
        xs = list(range(len(gr)))
        bars = VGroup()
        for k, g in zip(xs, gr):
            v = 100 * g["gdppc"]
            r = Polygon(ax.ax.c2p(k - 0.32, 0), ax.ax.c2p(k + 0.32, 0), ax.ax.c2p(k + 0.32, v), ax.ax.c2p(k - 0.32, v),
                        stroke_width=0, fill_color=GDP if g["first"] >= 1830 else WAGE, fill_opacity=0.85)
            bars.add(VGroup(r, label(rf"{v:.2f}", font_size=19, color=WHITE).next_to(r, UP, buff=0.08),
                            label(rf"{g['first']}--{str(g['last'])[2:]}", font_size=17, color=GREY_A).next_to(
                                ax.ax.c2p(k, 0), DOWN, buff=0.12)))
        rows = VGroup(
            label(r"1700--1830: \ a fifth to a third of a percent a year", font_size=21, color=WAGE),
            label(r"Crafts and Harley: \ a revolution in cotton and iron, \\ not yet in the whole economy",
                  font_size=21),
            label(r"farms and services, \ most of the jobs, \ changed slowly", font_size=21, color=GREY_A),
            label(r"steam added little to growth until after 1830 \ (Crafts)", font_size=21, color=TECH),
            label(r"then: \ more than 1\% a year, \ for good", font_size=22, color=GDP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(UP * 0.2)
        for r in rows:
            if r.width > 5.4:
                r.width = 5.4
        tag = published_tag(r"Crafts and Harley, EcHR 45(4) (1992); \ Crafts, EJ 114(495) (2004)", corner=DR,
                            font_size=12)
        src = data_tag(data.cite("millennium"), corner=DL, font_size=12)
        g1, g2, g3, g4 = gr[1], gr[2], gr[3], gr[4]
        with self.voiceover(
            "If the machines were so remarkable, the national figures should show it. <bookmark mark='a'/> They "
            "barely do. English income per head grew by about a third of a percent a year from 1700 to 1800, and by "
            f"only {100 * g2['gdppc']:.2f} percent a year from 1800 to 1830, with war against France for much of "
            "it. <bookmark mark='b'/> Nicholas Crafts and Knick Harley revised the older, faster estimates down, and "
            "concluded that the revolution was in cotton and iron, not yet in the whole economy. "
            "<bookmark mark='c'/> Farms and services, where most people worked, changed slowly. "
            "<bookmark mark='d'/> Even steam, Crafts later found, added little to growth until after 1830, because "
            "engines were few, costly and fuel-hungry for decades. <bookmark mark='e'/> Then, from 1830 to 1870, "
            f"growth reached {100 * g3['gdppc']:.2f} percent a year, and it has never gone back."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars[:3]], lag_ratio=0.5), FadeIn(rows[0]),
                      run_time=3)
            for mk, r in zip("bcd", rows[1:4]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars[3:]], lag_ratio=0.5), FadeIn(rows[4]),
                      run_time=2.5)
        self.clear_scene()

    def pause(self):
        ind = load("industrial")
        yrs = np.array(ind["years"], float)
        ax = plane([1770, 1850], [80, 160], center=LEFT * 2.9 + DOWN * 0.45, x_length=6.8, y_length=4.8,
                   xticks=[1780, 1800, 1820, 1840], yticks=[80, 100, 120, 140, 160], ylabel=r"index, \ 1780 = 100",
                   xfmt=lambda v: f"{v:.0f}", font_size=17)
        cg = path(ax, yrs, ind["gdppc_index"], color=GDP, width=4, smooth=False)
        cw = path(ax, yrs, ind["wage_index"], color=WAGE, width=4, smooth=False)
        lg = label(r"GDP per head", font_size=19, color=GDP).next_to(ax.ax.c2p(1850, ind["gdppc_index"][-1]), RIGHT,
                                                                     buff=0.1)
        lw = label(r"real wages", font_size=19, color=WAGE).next_to(ax.ax.c2p(1850, ind["wage_index"][-1]), RIGHT,
                                                                    buff=0.1)
        rows = VGroup(
            label(rf"1780--1840: \\ output per head $+{ind['gdppc_1840'] - 100:.0f}\%$, \\ real wages "
                  rf"$+{ind['wage_1840'] - 100:.0f}\%$", font_size=21, color=WHITE),
            label(r"Friedrich Engels, \ 1845: \\ \emph{The Condition of the Working Class in England}", font_size=20,
                  color=GREY_A),
            label(r"the gain went to profits, \\ reinvested in machines \\ (Allen: \ Engels's pause)", font_size=21,
                  color=TECH),
            label(r"after 1840, \ wages begin to catch up", font_size=21, color=WAGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        for r in rows:
            if r.width > 4.2:
                r.width = 4.2
        rows.to_edge(RIGHT, buff=0.3).shift(UP * 0.6)
        tag = published_tag(r"Allen, EEH 46(4) (2009); \ Engels (1845)", corner=DR, font_size=13)
        with self.voiceover(
            "And the workers? <bookmark mark='a'/> Set output per head and real wages to a hundred in 1780 and "
            f"follow them. By 1840 output per head had risen by about {ind['gdppc_1840'] - 100:.0f} percent; real "
            f"wages by about {ind['wage_1840'] - 100:.0f}. <bookmark mark='b'/> This is the England Friedrich Engels "
            "described in 1845, in The Condition of the Working Class in England. <bookmark mark='c'/> Robert Allen "
            "called the gap Engels's pause: the gains went to profits, which were reinvested in machines and "
            "factories. <bookmark mark='d'/> Only after 1840 did wages begin to catch up. The first two "
            "generations of the escape were not the ones who enjoyed it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cg), Create(cw), run_time=4, rate_func=linear)
            self.play(FadeIn(lg), FadeIn(lw), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
