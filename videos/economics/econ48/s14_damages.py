from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Damages(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Damages measured", r"What does a hotter year do to an economy, and to people?",
             "Chapter twelve. Damages measured.",
             lit={2012: r"Dell, Jones and Olken", 2015: r"Burke, Hsiang and Miguel", 2016: r"Barreca et al."},
             scale=("nation", "world"), horizon=("a year",))
        self.design()
        self.curve()
        self.health()

    def design(self):
        T = tables.DAMAGES_48.data
        chain = flow_chain([(r"a country's \\ weather varies \\ year to year", COOL), (r"compare it with \\ itself",
                                                                                     GREY_B),
                            (r"and with the \\ same year elsewhere", GREY_B), (r"growth in the \\ warmer years",
                                                                                HEAT)],
                           notes=[r"as if by chance", r"country fixed effects \\ and its own trends",
                                  r"year fixed effects", r"the effect of heat"],
                           box_w=2.8, font_size=20, note_size=16).move_to(UP * 1.3)
        finds = VGroup(
            label(rf"Dell, \ Jones and Olken, \ 2012: \ a year 1\textdegree C warmer cut growth in poor countries by "
                  rf"about {T['djo']} points; \ in rich ones, \ no robust effect", font_size=20, color=WHITE),
            label(rf"Burke, \ Hsiang and Miguel, \ 2015: \ {T['bhm_n']} countries; \ output peaks at an average of "
                  rf"{T['bhm_opt']}\textdegree C, \ and falls steeply above", font_size=20, color=HEAT),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 1.8)
        tag = published_tag(tables.DAMAGES_48.tag, corner=DR, font_size=11)
        with self.voiceover(
            "DICE's damage function came from a synthesis of studies. Since 2012 economists have measured damage "
            "from the data directly. <bookmark mark='a'/> The idea: a country's weather varies from year to year, "
            "much as if by chance. <bookmark mark='b'/> Compare each country with itself, allowing for its own "
            "trends, <bookmark mark='c'/> and with every other country in the same year, to strip out world booms "
            "and busts. <bookmark mark='d'/> What is left is the effect of a hotter or cooler year. <bookmark "
            "mark='e'/> Melissa Dell, Benjamin Jones and Benjamin Olken found that a year one degree warmer cut "
            f"growth in poor countries by about {T['djo']} percentage points, with no robust effect in rich ones. "
            "<bookmark mark='f'/> Marshall Burke, Solomon Hsiang and Edward Miguel found a single curve for all "
            f"countries: output peaks where the average temperature is about {T['bhm_opt']} degrees and falls "
            "steeply in hotter places."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(finds[0], shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(finds[1], shift=UP * 0.1))
        self.clear_scene()

    def curve(self):
        P = load("panel")
        T = tables.DAMAGES_48.data
        g, r = np.array(P["grid"]), np.array(P["response"])
        k = (g >= -5) & (g <= 30)
        ax = plane([-5, 30], [-0.20, 0.04], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=4.4,
                   xticks=[-5, 0, 5, 10, 15, 20, 25, 30], yticks=[-0.2, -0.15, -0.1, -0.05, 0],
                   xlabel=r"a country's average temperature, \ \textdegree C",
                   ylabel=r"growth against the best temperature", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}".replace("-", "{-}") + r"\%" if v else "0", font_size=14)
        ln = path(ax, g[k], r[k], HEAT, 3.4)
        opt = vline(ax, P["optimum"], -0.2, 0.04, OPT)
        rug = VGroup(*[Line(ax.ax.c2p(x, -0.2), ax.ax.c2p(x, -0.19), color=GREY_B, stroke_width=1.2)
                       for x in P["mean_temps"] if -5 <= x <= 30])
        named = VGroup()
        for code, x in P["named"].items():
            if code in ("CAN", "USA", "CHN", "IND", "NGA", "MLI"):
                y = float(np.interp(x, g, r))
                named.add(VGroup(dot(ax, x, y, WHITE, 0.05), label(code, font_size=13, color=WHITE).next_to(
                    ax.ax.c2p(x, y), DR if x > P["optimum"] else DL, buff=0.05)))
        side = VGroup(
            label(rf"{P['countries']} countries, \\ {P['years'][0]}--{P['years'][1]}: \ ERA5's \\ temperatures, \ the "
                  r"World \\ Bank's growth", font_size=17, color=WHITE),
            label(rf"best: \ about {P['optimum']:.1f}\textdegree C \\ (Burke et al.: \ {T['bhm_opt']})", font_size=18,
                  color=OPT),
            label(rf"a country at 25\textdegree: \\ a degree warmer, \\ growth "
                  rf"{100 * P['marg25']:+.1f} points".replace("-", "{-}"), font_size=18, color=HEAT),
            label(rf"poorer half, \ linear: \\ {100 * P['djo_poor']:+.1f} \ (s.e. {100 * P['djo_poor_se']:.1f})"
                  .replace("-", "{-}"), font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"ERA5 (Copernicus) via Our World in Data; \ World Bank WDI; \ estimated here", corner=DL,
                       font_size=12)
        q_add = label(r"add up? \ each hot \\ year's loss stays", font_size=17, color=HEAT)
        q_fade = label(r"or fade? \ output \\ catches up", font_size=17, color=COOL)
        VGroup(q_add, q_fade).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(side, DOWN, aligned_edge=LEFT,
                                                                                buff=0.35)
        with self.voiceover(
            "Here is that regression, run for this film on newer data. <bookmark mark='a'/> Temperatures for "
            f"{P['countries']} countries from the ERA5 reanalysis, growth of GDP per head from the World Bank, "
            f"{P['years'][0]} to {P['years'][1]}, with Burke, Hsiang and Miguel's controls. <bookmark mark='b'/> "
            f"The curve peaks near {P['optimum']:.1f} degrees, a little cooler than their {T['bhm_opt']}, and the "
            "marks along the bottom are the countries' own average temperatures. <bookmark mark='c'/> For a country "
            f"averaging twenty-five degrees, a year one degree warmer means growth about {100 * abs(P['marg25']):.1f} "
            "points lower; for a cool country, a little higher. <bookmark mark='d'/> Splitting the countries by "
            f"income instead, as Dell, Jones and Olken did, gives {100 * P['djo_poor']:+.1f} points for the poorer "
            f"half, with a standard error of {100 * P['djo_poor_se']:.1f}: the same sign as theirs, and much less "
            "certain. <bookmark mark='e'/> The open question is whether such losses add up, year after year, "
            "<bookmark mark='f'/> or fade as people adapt. If they add up, the damage from warming is several times "
            "DICE's."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            self.play(Create(ln), FadeIn(rug), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(opt), FadeIn(side[1]), Indicate(rug, color=WHITE, scale_factor=1.0), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in named], lag_ratio=0.2), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(q_add, shift=UP * 0.1), Indicate(named, color=WHITE, scale_factor=1.1), run_time=1.2)
            vo.wait_until("f")
            self.play(FadeIn(q_fade, shift=UP * 0.1))
        self.clear_scene()

    def health(self):
        H = tables.HEALTH_48.data
        cards = point_cards([
            (r"heat, \ adapted to", rf"US deaths from days \\ above 80\textdegree F fell \\ about {H['ac']}\%, \ "
                                   r"chiefly \\ through air \\ conditioning", COOL),
            (r"days above 90\textdegree F", rf"about {H['deaths_now']:,} early \\ deaths a year, \\ against "
                                            rf"{H['deaths_then']:,} \\ before 1960".replace(",", "{,}"), HEAT),
            (r"the Huai River", rf"north of it, \ free \\ coal for heating: \\ life expectancy \\ "
                                rf"{H['years_2017']} years lower", LOSS),
            (r"per 10 $\mu$g of PM$_{10}$", rf"{H['per10']} years of \\ life lost; \ the same \\ coal that warms "
                                             r"\\ the planet", LOSS),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"damage to people, \ and how they adapt", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.HEALTH_48.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Damage falls on people as well as output, and people adapt. <bookmark mark='a'/> Alan Barreca and "
            "colleagues found that the toll of very hot days in the United States fell by about "
            f"{H['ac']} percent over the twentieth century, chiefly through air conditioning in homes. <bookmark "
            f"mark='b'/> Days above ninety degrees Fahrenheit caused about {H['deaths_now']:,} early deaths a year "
            f"from 1960 to 2004, against some {H['deaths_then']:,} had the old relationship held. <bookmark "
            "mark='c'/> And the fuels that warm the climate damage health directly. China gave free or cheap coal for "
            "winter heating north of the Huai River, and not south of it. Comparing people on either side, Avraham "
            f"Ebenstein and colleagues found far dirtier air and life expectancy {H['years_2017']} years lower just "
            f"to the north; <bookmark mark='d'/> each extra ten micrograms of fine particles costs {H['per10']} "
            "years of life. A tonne of carbon from coal comes with this local damage too, which is why cutting it "
            "can pay even before the climate is counted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
