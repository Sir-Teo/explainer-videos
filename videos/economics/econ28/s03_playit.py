from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403

CHIP = ("#7FD1B9", "#F2C14E", "#F25F5C")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ forecast inflation", r"It is the end of 1972. \ What will inflation be next year?",
             "Chapter two. Play it: forecast inflation.", lit={1973: r"the first oil shock"},
             scale=("person", "nation"), horizon=("a year",))
        self.choose()
        self.reveal()

    def _axes(self):
        return plane([1959.5, 1981], [0, 14], center=LEFT * 1.6 + UP * 0.2, x_length=8.6, y_length=4.2,
                     xticks=[1960, 1965, 1970, 1975, 1980], yticks=[0, 4, 8, 12], ylabel=r"inflation, \ \%",
                     xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)

    def choose(self):
        P = load("play")
        ax = self._axes()
        bars = VGroup()
        for y, v in zip(P["years"], P["history"]):
            lo, hi = ax.ax.c2p(y, 0), ax.ax.c2p(y, v)
            bars.add(Rectangle(width=0.28, height=hi[1] - lo[1], fill_color=EXPECT, fill_opacity=0.75,
                               stroke_width=0).move_to((lo + hi) / 2))
        o = P["options"]
        chips = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=0.9, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(t, font_size=26, color=c))
                         for c, t in zip(CHIP, (rf"A: \ about {o[0]:.0f}\%", rf"B: \ about {o[1]:.0f}\%",
                                                rf"C: \ about {o[2]:.0f}\%"))]).arrange(RIGHT, buff=0.5)
        for ch in chips:
            ch[1].move_to(ch[0])
        chips.to_edge(DOWN, buff=0.9)
        ring = countdown().scale(0.7).next_to(chips, RIGHT, buff=0.3)
        tag = data_tag(r"BLS: \ the CPI, \ annual averages, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Your turn. It is the end of 1972. Here is American inflation, year by year, from 1960. "
            "<bookmark mark='a'/> It crept up through the late 1960s, to almost six percent in 1970, then fell back, "
            f"to {P['last']:.1f} percent in 1972, under price controls. <bookmark mark='b'/> What will inflation be "
            f"in 1973? About {o[0]:.0f} percent, like last year; about {o[1]:.0f}; or about {o[2]:.0f}? Pause, and "
            "choose. Write your answer down: you will need it again."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3), FadeIn(ring),
                      run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        P = load("play")
        ax = self._axes()
        bars = VGroup()
        allys = P["years"] + list(range(P["target"], P["target"] + 8))
        allv = P["history"] + P["next5"]
        for y, v in zip(allys, allv):
            lo, hi = ax.ax.c2p(y, 0), ax.ax.c2p(y, v)
            bars.add(Rectangle(width=0.28, height=hi[1] - lo[1], fill_color=EXPECT if y < P["target"] else INFL,
                               fill_opacity=0.75, stroke_width=0).move_to((lo + hi) / 2))
        old = bars[:len(P["years"])]
        new = bars[len(P["years"]):]
        side = VGroup(
            label(rf"1973: \ {P['answer']:.1f}\%: \ B was closest", font_size=22, color=INFL),
            label(rf"1974: \ {P['next5'][1]:.1f}\%", font_size=22, color=INFL),
            label(r"forecasting from the past \\ always lagged behind", font_size=20, color=EXPECT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.5).shift(RIGHT * 3)
        tag = data_tag(r"BLS: \ the CPI, \ annual averages, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            f"<bookmark mark='a'/> In 1973, inflation was {P['answer']:.1f} percent. If you chose B, you were "
            "closest. The controls were lifted, and food prices jumped. <bookmark mark='b'/> In 1974, after the "
            f"oil embargo, {P['next5'][1]:.0f} percent. Hardly anyone looking at the 1960s would have guessed. "
            "<bookmark mark='c'/> Most people forecast by looking back, as you just did, and through the 1970s "
            "forecasts made that way kept falling behind. That is this part's subject: how expectations are formed, "
            "and what they do to the trade-off."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(old), run_time=0.6)
            vo.wait_until("a")
            self.play(GrowFromEdge(new[0], DOWN), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in new[1:]], lag_ratio=0.2), FadeIn(side[1]),
                      run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()
