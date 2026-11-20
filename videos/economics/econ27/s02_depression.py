from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


class Depression(VoiceoverScene):
    def construct(self):
        card(self, 1, r"The Depression in data", r"What happened, \ and what did economists expect to happen?",
             "Chapter one. The Depression in data.", lit={1803: r"Say", 1929: r"the crash"}, scale=("nation",),
             horizon=("a decade",))
        self.output()
        self.jobs()
        self.say()

    def output(self):
        d = load("depression")
        yrs = np.array(d["years"])
        g = 100 * np.array(d["gnp"]) / d["gnp"][0]
        p = 100 * np.array(d["deflator"]) / d["deflator"][0]
        ax = plane([1928.5, 1941.5], [60, 130], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[1929, 1931, 1933, 1935, 1937, 1939, 1941], yticks=[60, 80, 100, 120],
                   ylabel=r"1929 $= 100$", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        base = seg(ax, 1928.5, 100, 1941.5, 100, color=GREY_D, width=2)
        gl = path(ax, yrs, g, color=OUTPUT, width=4, smooth=False)
        pl = path(ax, yrs, p, color=PRICE, width=4, smooth=False)
        side = VGroup(
            label(rf"real GNP: \ $-${d['gnp_fall']:.0f}\% \\ from 1929 to 1933", font_size=21, color=OUTPUT),
            label(rf"prices: \ $-${d['price_fall']:.0f}\% \\ over the same years", font_size=21, color=PRICE),
            label(rf"output was back to 1929's \\ level only in {d['gnp_back']}", font_size=20, color=GREY_A),
            label(r"and fell again \\ in 1937--38", font_size=20, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BEA: \ real GNP and the GDP deflator, \ annual, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Start with what happened. Here is America's real output and its price level, each set to a hundred in "
            f"1929. <bookmark mark='a'/> From 1929 to 1933, real output fell by about {d['gnp_fall']:.0f} percent. "
            f"<bookmark mark='b'/> Prices fell by about {d['price_fall']:.0f} percent. Falling prices are what the "
            "economics of the day said should cure a glut, and they did not. <bookmark mark='c'/> Output got back "
            f"to its 1929 level only in {d['gnp_back']}, <bookmark mark='d'/> and then fell again in the recession "
            "of 1937 and 1938."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(base), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(gl), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(pl), FadeIn(side[1]), run_time=1.5)
            for mk, r_ in zip("cd", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def jobs(self):
        d = load("depression")
        ax = plane([1928.5, 1941.5], [0, 26], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[1929, 1931, 1933, 1935, 1937, 1939, 1941], yticks=[0, 5, 10, 15, 20, 25],
                   ylabel=r"unemployment rate, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=16)
        bars = VGroup()
        for y, v in zip(d["years"], d["unemployment"]):
            if not np.isfinite(v):
                continue
            lo, hi = ax.ax.c2p(y, 0), ax.ax.c2p(y, v)
            bars.add(Rectangle(width=0.42, height=hi[1] - lo[1], fill_color=PRICE, fill_opacity=0.8,
                               stroke_width=0).move_to((lo + hi) / 2))
        side = VGroup(
            label(rf"1929: \ {d['u29']:.1f}\%", font_size=22, color=GREY_A),
            label(rf"1933: \ {d['u33']:.0f}\%", font_size=24, color=PRICE),
            label(r"other estimates put 1933 \\ at about a quarter \\ of the labour force", font_size=19,
                  color=GREY_B),
            label(r"and it stayed in double digits \\ until the war", font_size=20, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"NBER Macrohistory Database: \ unemployment rate, \ 1929--1942, \ monthly, \ averaged by "
                       r"year, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "And here is what it did to work: the unemployment rate, year by year, in one monthly series from the "
            f"time. <bookmark mark='a'/> In 1929, about {d['u29']:.1f} percent by this series' count. "
            f"<bookmark mark='b'/> In 1933, about {d['u33']:.0f} percent. <bookmark mark='c'/> Other estimates "
            "differ in the details, and put 1933 at about a quarter of the labour force. "
            "<bookmark mark='d'/> Either way, unemployment stayed in double digits for the rest of the decade, "
            "until the war."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1),
                      run_time=2)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def say(self):
        rows = VGroup(
            label(r"what the classics said", font_size=28, color=E.ACCENT),
            label(r"Say, \ 1803: \ every sale is also a purchase, \ so there can be no general glut", font_size=23,
                  color=GREY_A),
            label(r"Keynes's summary of it: \ supply creates its own demand", font_size=23, color=OUTPUT),
            label(r"if workers are idle, \ wages fall until it pays to hire them; \ if goods go unsold, \ prices fall",
                  font_size=22, color=GREY_A),
            label(r"so a slump should cure itself", font_size=24, color=OUTPUT),
            label(r"but in the co-op, \ a coupon earned need not be spent: \ money can be held", font_size=24,
                  color=COUPON),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Say, \emph{Trait\'e d'\'economie politique} (1803); \ Keynes, \emph{The General "
                            r"Theory} (1936), \ ch.\ 2", corner=DR, font_size=12)
        with self.voiceover(
            "What did economists expect? <bookmark mark='a'/> Jean-Baptiste Say had argued in 1803 that every sale "
            "is also a purchase: people produce in order to buy, so there can be no general glut of everything at "
            "once. <bookmark mark='b'/> Keynes later summed up the view in a phrase: supply creates its own demand. "
            "<bookmark mark='c'/> If workers are idle, wages fall until it pays to hire them. If goods go unsold, "
            "their prices fall until they sell. <bookmark mark='d'/> So a slump should cure itself, given time. "
            "<bookmark mark='e'/> The co-op shows the gap in the argument. A coupon earned by sitting need not be "
            "spent on an evening out. It can be held. When everyone wants to hold more money, the sale and the "
            "purchase come apart."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
