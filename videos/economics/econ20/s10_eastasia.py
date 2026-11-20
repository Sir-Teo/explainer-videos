from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403


class EastAsia(VoiceoverScene):
    def construct(self):
        card(self, 8, r"East Asia: \ perspiration or inspiration?", r"Did the four tigers grow by using inputs "
             r"better, \ or by piling them up?", "Chapter eight. East Asia: perspiration or inspiration?",
             lit={1961: r"Samuelson's forecast", 1994: r"Krugman", 1995: r"Young", 2002: r"Hsieh"},
             scale=("nation",), horizon=("decades",))
        self.soviet()
        self.call()
        self.young()
        self.hsieh()
        self.slowing()

    def soviet(self):
        e = load("eastasia")["soviet"]
        ax = plane([1926, 1993], [0, 0.5], center=DOWN * 0.45 + LEFT * 1.4, x_length=8.8, y_length=4.8,
                   xticks=[1930, 1950, 1970, 1990], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                   ylabel=r"Soviet GDP per head, \ United States $= 1$", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16)
        line = path(ax, e["years"], e["ratio"], color=NORTH, width=4, smooth=False)
        dec = e["decades"]
        side = VGroup(
            label(r"Soviet growth of GDP per head:", font_size=21, color=GREY_A),
            *[label(rf"{k}: \ {pc(v)} a year", font_size=21, color=NORTH) for k, v in dec.items()],
            label(rf"peak: \ {pc(e['peak'], 0)} of America's, \ {e['peak_year']}", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = data_tag(r"Maddison Project Database 2023 \ (the former USSR)", corner=DR, font_size=12)
        with self.voiceover(
            "The argument over East Asia began with another economy. <bookmark mark='a'/> In the 1950s and 1960s "
            f"the Soviet Union grew fast: income per head by about {100 * dec['1950s']:.1f} percent a year, by the "
            "Maddison Project's reckoning, and it was closing the gap with America. <bookmark mark='b'/> Its planners "
            "did it by force of accumulation: very high investment, and millions moved from farms into factories. "
            f"<bookmark mark='c'/> Then growth slowed, to {100 * dec['1970s']:.1f} percent in the 1970s and "
            f"{100 * dec['1980s']:.1f} in the 1980s. Soviet income per head never passed about "
            f"{100 * e['peak']:.0f} percent of America's. Diminishing returns, with a small residual, is exactly "
            "what Solow's model says such growth runs into."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), run_time=3, rate_func=linear)
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]), FadeIn(side[5]))
        self.clear_scene()

    def call(self):
        c = calls.CALLS["samuelson_soviet"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.4,
                       font_size=21).move_to(UP * 0.1)
        tag = published_tag(r"Levy and Peart, J.\ Econ.\ Behavior \& Organization 78(1--2) (2011): \ 110--125",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Many economists extrapolated. <bookmark mark='a'/> The best-selling textbook of the age, Paul "
            "Samuelson's Economics, showed in its 1961 edition Soviet national income overtaking America's between "
            "1984 and 1997, on the growth rates it assumed. The 1980 edition still drew the crossing, now between "
            "2002 and 2012. <bookmark mark='b'/> The forecast rested on carrying past growth into the future at its "
            "past rate. <bookmark mark='c'/> What happened: Soviet growth slowed decade by decade, and the Soviet "
            "Union dissolved in 1991 without overtaking. Called it? Wrong. The economists David Levy and Sandra "
            "Peart traced the forecast through the editions."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("c")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()

    def young(self):
        e = load("eastasia")
        order = e["order"]
        unit = 1.3 / 0.01          # screen units per percentage point
        rows = VGroup()
        for i, c in enumerate(order):
            name, span, v = e["young"][c]
            o = e["ours"][c]
            y = 1.7 - i * 1.05
            nm = label(rf"{name}, \ {span.replace('-', '--')}", font_size=19, color=COUNTRY[c][1]).move_to(
                [-3.2, y, 0], aligned_edge=RIGHT)
            b1 = Rectangle(width=max(v * unit, 0.02), height=0.32, stroke_width=0, fill_color=TFP,
                           fill_opacity=0.95).move_to([-3.0, y + 0.19, 0], aligned_edge=LEFT)
            b2 = Rectangle(width=max(o["tfp"] * unit, 0.02), height=0.32, stroke_width=1.5, stroke_color=TFP,
                           fill_color=TFP, fill_opacity=0.3).move_to([-3.0, y - 0.19, 0], aligned_edge=LEFT)
            l1 = label(rf"Young: \ {pc(v)}", font_size=16, color=TFP).next_to(b1, RIGHT, buff=0.12)
            l2 = label(rf"PWT 11.0: \ {pc(o['tfp'])} \ (output {pc(o['output'])}, \ capital "
                       rf"{pc(o['capital'])})", font_size=16, color=GREY_A).next_to(b2, RIGHT, buff=0.12)
            rows.add(VGroup(nm, b1, l1, b2, l2))
        head = label(r"total factor productivity growth, \ a year", font_size=24, color=GREY_A).to_edge(UP,
                                                                                                    buff=0.4)
        note_ = label(r"Young's Korea and Taiwan exclude agriculture", font_size=16, color=GREY_B).to_edge(
            DOWN, buff=0.45)
        tag = published_tag(r"Young, QJE 110(3) (1995): \ 641--680; \ Krugman, Foreign Affairs 73(6) (1994)",
                            corner=DR, font_size=12)
        sg = e["ours"]["SGP"]
        with self.voiceover(
            "In 1994 Paul Krugman applied the same reasoning to East Asia, in an essay called The Myth of Asia's "
            "Miracle. Its evidence came from Alwyn Young, who had measured the four tigers' inputs with unusual "
            "care: hours, schooling, the entry of women into paid work, and capital by type of asset. "
            "<bookmark mark='a'/> Hong Kong's residual: about 2.3 percent a year. <bookmark mark='b'/> Singapore's: "
            "0.2. <bookmark mark='c'/> South Korea's: 1.7, and Taiwan's 2.6, outside agriculture. Respectable "
            "numbers, but no better than many slower-growing economies in the OECD or Latin America. The miracle "
            "was in the inputs. <bookmark mark='d'/> The same accounting on the Penn World Table, with its own "
            "inputs, tells a similar story: Singapore grew by "
            f"{100 * sg['output']:.1f} percent a year from 1966 to 1990, and capital alone accounts for "
            f"{100 * sg['capital']:.1f} points of it. Its residual is {100 * sg['tfp']:.1f}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(note_), *[FadeIn(r[0]) for r in rows])
            for mk, r in zip("ab", rows[:2]):
                vo.wait_until(mk)
                self.play(GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
            vo.wait_until("c")
            for r in rows[2:]:
                self.play(GrowFromEdge(r[1], LEFT), FadeIn(r[2]), run_time=0.8)
            vo.wait_until("d")
            self.play(*[AnimationGroup(GrowFromEdge(r[3], LEFT), FadeIn(r[4])) for r in rows], run_time=2)
        self.clear_scene()

    def hsieh(self):
        rows = VGroup(
            label(r"Chang-Tai Hsieh, \ 2002: \ measure the residual from prices instead", font_size=25,
                  color=E.ACCENT),
            MathTex(r"g_A = s_K\, g_r + s_L\, g_w", font_size=48),
            label(r"if capital piled up as fast as the national accounts say, \ its return should have collapsed",
                  font_size=22, color=GREY_A),
            label(r"in Singapore it did not: \ the price-based residual is more than 2 points a year higher",
                  font_size=22, color=RATE),
            label(r"Taiwan: \ about 1 point higher; \ Korea and Hong Kong: \ the two roughly agree", font_size=22,
                  color=GREY_A),
            label(r"so either Singapore's investment figures are overstated, \ or its returns are; \ the dispute "
                  r"is about data", font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Hsieh, AER 92(3) (2002): \ 502--526, \ abstract", corner=DR, font_size=12)
        with self.voiceover(
            "The verdict was challenged. <bookmark mark='a'/> Chang-Tai Hsieh measured the residual a second way, "
            "from prices rather than quantities. <bookmark mark='b'/> If output per unit of input is rising, the "
            "inputs' prices must be rising on average too: the residual is the share-weighted growth of the rental "
            "rate of capital and the wage. <bookmark mark='c'/> If capital had piled up as fast as Singapore's "
            "national accounts say, with so little productivity growth, its return should have collapsed. "
            "<bookmark mark='d'/> It did not. Hsieh's price-based residual for Singapore is more than two points a "
            "year higher than the quantity-based one. <bookmark mark='e'/> For Taiwan about one point; for Korea and "
            "Hong Kong the two methods roughly agree. <bookmark mark='f'/> Both methods rest on the same identity, so "
            "one of the data sets is wrong: Singapore's investment figures, or its interest rates. The argument "
            "became one about measurement."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def slowing(self):
        e = load("eastasia")
        dec = e["kor_decades"]
        ax = plane([-0.5, 5.5], [0, 0.09], center=DOWN * 0.5 + LEFT * 1.3, x_length=8.6, y_length=4.6, xticks=[],
                   yticks=[0, 0.02, 0.04, 0.06, 0.08], ylabel=r"South Korea: \ growth of GDP per head, \ a year",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16)
        bars = VGroup()
        for i, (k, v) in enumerate(dec.items()):
            h = ax.ax.c2p(0, v)[1] - ax.ax.c2p(0, 0)[1]
            r = Rectangle(width=1.0, height=h, stroke_width=0, fill_color=COUNTRY["KOR"][1],
                          fill_opacity=0.85).move_to(ax.ax.c2p(i, 0), aligned_edge=DOWN)
            bars.add(VGroup(r, label(k, font_size=16, color=GREY_A).next_to(r, DOWN, buff=0.1),
                            label(pc(v), font_size=16, color=WHITE).next_to(r, UP, buff=0.06)))
        side = VGroup(
            label(r"perspiration is not a slur:", font_size=22, color=E.ACCENT),
            label(r"saving, \ schooling \ and work \\ are real achievements", font_size=20, color=GREY_A),
            label(r"but growth from inputs \\ slows as the inputs \\ run into diminishing returns", font_size=20,
                  color=HOLD),
            label(r"Korea caught up \\ and then slowed, \\ as Solow predicts", font_size=20,
                  color=COUNTRY["KOR"][1]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        src = data_tag(r"Penn World Table 11.0", corner=DR, font_size=12)
        with self.voiceover(
            "What should we make of it? <bookmark mark='a'/> Perspiration is not a slur. Saving forty percent of "
            "output, keeping children in school and bringing women into paid work are real achievements, and they "
            "made tens of millions of people rich. <bookmark mark='b'/> But growth that comes from piling up "
            "inputs slows as the inputs run into diminishing returns. <bookmark mark='c'/> South Korea's income per "
            f"head grew by about {100 * dec['1980s']:.0f} percent a year in the 1980s, {100 * dec['2000s']:.0f} in "
            f"the 2000s and {100 * dec['2010s']:.0f} in the 2010s, as it neared the frontier. Unlike the Soviet "
            "Union, it got there first. <bookmark mark='d'/> That is the difference the residual makes."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.3), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
