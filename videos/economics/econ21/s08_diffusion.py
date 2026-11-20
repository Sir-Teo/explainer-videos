from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Diffusion(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Diffusion: \ ideas cross borders slowly", r"If ideas are non-rival, \ why doesn't every "
             r"country use the best ones?", "Chapter seven. Diffusion: ideas cross borders slowly.",
             lit={1998: r"Basu and Weil", 2010: r"Comin and Hobijn"}, scale=("world",), horizon=("decades",))
        self.lags()
        self.levels()

    def lags(self):
        rows = VGroup(
            label(r"Diego Comin and Bart Hobijn, \ 2010", font_size=27, color=E.ACCENT),
            label(r"15 technologies, \ from steam ships and the telegraph to personal computers", font_size=22,
                  color=GREY_A),
            label(r"166 countries, \ two centuries", font_size=22, color=GREY_A),
            label(r"on average, \ a country adopted a technology 45 years after its invention", font_size=26,
                  color=IDEA),
            label(r"differences in adoption lags explain at least a quarter of differences in income per head",
                  font_size=23, color=OUTPUT),
            label(r"and the technology of rich countries may not suit poor ones \ (Basu and Weil, \ 1998): \ "
                  r"appropriate technology", font_size=21, color=HOLD),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Comin and Hobijn, AER 100(5) (2010): \ 2031--2059, \ abstract; \ Basu and Weil, QJE "
                            r"113(4) (1998)", corner=DR, font_size=12)
        with self.voiceover(
            "An idea can be used by everyone at once. In practice it is not. <bookmark mark='a'/> Diego Comin and "
            "Bart Hobijn traced the spread of fifteen technologies, from steam and the telegraph to the personal "
            "computer, <bookmark mark='b'/> across a hundred and sixty-six countries and two centuries. "
            "<bookmark mark='c'/> On average, a country adopted a technology forty-five years after it was "
            "invented. <bookmark mark='d'/> And the differences in those lags alone explain at least a quarter of "
            "the differences in income per head across countries. <bookmark mark='e'/> Using an idea takes "
            "skills, complementary machines, managers and markets, and the technologies designed for rich "
            "countries, rich in capital and skills, may not suit poor ones at all: Susanto Basu and David Weil's "
            "appropriate technology."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def levels(self):
        t = load("tfp")
        v = np.array(t["ctfp"])
        ax = plane([-0.5, len(v) - 0.5], [0, 1.4], center=LEFT * 1.4 + DOWN * 0.4, x_length=9.0, y_length=4.8,
                   xticks=[], yticks=[0, 0.5, 1.0], ylabel=r"TFP level, \ United States $= 1$, \ 2019",
                   yfmt=lambda x: f"{x:g}", font_size=16)
        bars = VGroup()
        w = 9.0 / len(v) * 0.8
        for i, x in enumerate(v):
            h = ax.ax.c2p(0, min(x, 1.4))[1] - ax.ax.c2p(0, 0)[1]
            col = COUNTRY[t["codes"][i]][1] if t["codes"][i] in COUNTRY else GREY_B
            bars.add(Rectangle(width=w, height=max(h, 0.01), stroke_width=0, fill_color=col,
                               fill_opacity=0.9).move_to(ax.ax.c2p(i, 0), aligned_edge=DOWN))
        one = DashedLine(ax.ax.c2p(-0.5, 1), ax.ax.c2p(len(v) - 0.5, 1), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            label(rf"{t['n']} countries \ (PWT's ctfp)", font_size=20, color=GREY_A),
            label(rf"10th percentile: \ {t['p10']:.2f}", font_size=21, color=WEDGE),
            label(rf"90th percentile: \ {t['p90']:.2f}", font_size=21, color=OUTPUT),
            label(rf"a ratio of {t['ratio_90_10']:.1f}, \\ in the efficiency of use alone", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        src = data_tag(r"Penn World Table 11.0 \ (ctfp, \ current PPPs); \ countries of a million people or more",
                       corner=DR, font_size=11)
        with self.voiceover(
            "The result is the gap that part twenty measured. <bookmark mark='a'/> Here is total factor "
            "productivity in 2019, relative to the United States, from the Penn World Table, country by country. "
            f"<bookmark mark='b'/> A country at the tenth percentile gets about {t['p10']:.2f} as much out of the "
            f"same capital and skills as America; at the ninetieth, about {t['p90']:.2f}. "
            f"<bookmark mark='c'/> A ratio of {t['ratio_90_10']:.1f} to one, in efficiency alone. Some of it is "
            "slow adoption of ideas. The next chapters look for the rest: in how resources are allocated, and in "
            "the institutions that decide it. After a short break."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.02), Create(one),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()
