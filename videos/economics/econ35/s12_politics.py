from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403


class Politics(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Protection for sale", r"If tariffs make a country poorer, why are there so many?",
             "Chapter ten. Protection for sale.", lit={1846: r"the Corn Laws repealed", 1930: r"Smoot-Hawley",
                                                       1994: r"Grossman and Helpman"},
             scale=("nation", "world"), horizon=("a decade", "a century"))
        self.history()
        self.collapse()
        self.sale()

    def history(self):
        cards = point_cards([
            (r"Britain, \ 1815--46", r"the Corn Laws \\ protect landowners; \\ repealed in 1846, \\ after a campaign "
                                     r"\\ by manufacturers", LAND),
            (r"America, \ 1930", r"Smoot-Hawley \\ raises tariffs on \\ thousands of goods, \\ as prices fall", TARIFF),
            (r"the pattern", r"protection follows \\ organized interests, \\ not national gain", WHITE),
        ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.1)
        head = label(r"two famous tariffs", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(r"Irwin, \ \emph{Peddling Protectionism} (2011); \ Irwin, \ \emph{REStat} 80(2) (1998)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "If tariffs usually make a country poorer, why are there so many? History offers a clue. "
            "<bookmark mark='a'/> After 1815 Britain's Corn Laws kept out foreign grain, raising rents for the "
            "landowners who sat in Parliament, as specific factors predict. They were repealed in 1846, after a "
            "long campaign by manufacturers who wanted cheaper bread for their workers, and cheaper workers. "
            "<bookmark mark='b'/> In 1930 the United States passed the Smoot-Hawley tariff, which raised duties on "
            "thousands of goods as Congress traded votes among industries. <bookmark mark='c'/> In both, protection "
            "followed the interests that were organized, not the interest of the country."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def collapse(self):
        P = load("politics")
        O = load("openness")
        Sm = P["smoot"]
        ax = plane([1900, 1960], [0, 60], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.6, y_length=4.6,
                   xticks=[1900, 1913, 1929, 1945, 1960], yticks=[0, 20, 40, 60],
                   ylabel=r"exports plus imports, \ \% of GDP", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        wars = shade(ax, [(1914, 1918), (1939, 1945)], 0, 60, RECESS, 0.6)
        med = path(ax, O["years"], O["median"], WHITE, 3.2, xr=(1900, 1960), smooth=False)
        us = path(ax, O["usa_y"], O["usa"], USA, 2.4, xr=(1900, 1960), smooth=False)
        side = VGroup(
            label(rf"America's tariff \\ on dutiable goods: \\ {Sm['1929']:.0f}\% (1929) $\to$ {Sm['1932']:.0f}\% "
                  rf"(1932)", font_size=18, color=TARIFF),
            label(r"much of the rise \\ came from deflation: \\ duties in cents per unit \\ grew as prices fell",
                  font_size=17, color=GREY_A),
            label(r"others retaliated; \\ trade fell further \\ than output", font_size=18, color=WHITE),
            label(rf"by 1948: \ {Sm['1948']:.0f}\%", font_size=18, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Irwin (1998, 2011); \ Jord\`a, \ Schularick and Taylor, \ Macrohistory Database R6",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Smoot-Hawley's reputation is worse than its arithmetic, but the arithmetic is bad enough. "
            f"<bookmark mark='a'/> The average duty on America's dutiable imports rose from {Sm['1929']:.0f} percent "
            f"in 1929 to {Sm['1932']:.0f} percent in 1932. <bookmark mark='b'/> Douglas Irwin has shown that much of "
            "the rise came not from the law but from deflation: many duties were so many cents a pound, and as "
            "prices fell they became a larger share of the price. <bookmark mark='c'/> Other countries retaliated, "
            "and here is the result: trade, white for the median rich economy and blue for America, fell much "
            "further than output in the early 1930s. Tariffs did not cause the Depression, but they deepened the "
            f"collapse of trade. <bookmark mark='d'/> By 1948, after a decade of agreements, America's average was "
            f"{Sm['1948']:.0f} percent."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(wars), FadeIn(tag), Create(med), Create(us), run_time=2.0)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def sale(self):
        P = load("politics")
        n = len(P["t"])
        order = np.argsort(np.array(P["z"]) / np.array(P["e"]))
        ax = plane([0.4, n + 0.6], [-0.05, 0.10], center=LEFT * 1.8 + DOWN * 0.6, x_length=8.4, y_length=3.8,
                   xticks=[], yticks=[-0.05, 0, 0.05, 0.10], ylabel=r"the tariff, \ ad valorem",
                   yfmt=lambda v: f"{100 * v:+.0f}\\%" if v else "0", font_size=14)
        zero = seg(ax, 0.4, 0, n + 0.6, 0, GREY_B, 1.5)
        bars = VGroup()
        for k, i in enumerate(order):
            v = P["t"][i]
            col = TARIFF if P["organized"][i] else GREY_B
            p0, p1 = ax.ax.c2p(k + 0.65, 0), ax.ax.c2p(k + 1.35, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(abs(p1[1] - p0[1]), 0.01), fill_color=col,
                               fill_opacity=0.85, stroke_width=0).move_to((p0 + p1) / 2))
        eq = MathTex(r"\frac{t_i}{1+t_i} = \frac{I_i - \alpha_L}{a + \alpha_L}\cdot\frac{z_i}{e_i}", font_size=40,
                     color=WHITE).to_edge(UP, buff=0.35)
        side = VGroup(
            label(r"$I_i = 1$: \ the industry lobbies \\ $z_i$: \ output over imports \\ $e_i$: \ import elasticity",
                  font_size=17, color=GREY_A),
            label(r"red: \ organized industries, \\ protected more where \\ output is large and \\ imports "
                  r"unresponsive", font_size=17, color=TARIFF),
            label(rf"$a$ = {P['a']:.0f}: \ welfare weighs \\ {P['a']:.0f} times contributions; \\ the highest tariff "
                  rf"{100 * P['max_org']:.0f}\%", font_size=17, color=WHITE),
            label(rf"with $a$ = 5 \ it would be {100 * P['max_org5']:.0f}\%", font_size=17, color=TARIFF),
            label(rf"Goldberg and Maggi, \\ US tariffs in 1983: \\ $a$ between {P['gm_lo']} and {P['gm_hi']}",
                  font_size=17, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Grossman and Helpman, \ \emph{AER} 84(4) (1994); \ Goldberg and Maggi, \ "
                            r"\emph{AER} 89(5) (1999); \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "In 1994 Gene Grossman and Elhanan Helpman turned this into a theory: protection for sale. "
            "<bookmark mark='a'/> Industries that organize offer politicians contributions in exchange for "
            "tariffs; the government weighs the contributions against the welfare of voters. "
            "<bookmark mark='b'/> The result is a formula for every industry's tariff. Organized industries get "
            "protection, more where their output is large relative to imports, so the stakes are big, and where "
            "imports respond little to price, so the triangles are small. Unorganized industries get nothing, "
            "here even a tiny subsidy to imports. <bookmark mark='c'/> How much depends on how much the government "
            f"cares about welfare. If welfare counts {P['a']:.0f} times as much as a dollar of contributions, the "
            f"highest tariff on the Island is {100 * P['max_org']:.0f} percent; <bookmark mark='d'/> if only five "
            f"times as much, {100 * P['max_org5']:.0f} percent. <bookmark mark='e'/> Penny Goldberg and Giovanni "
            "Maggi fitted the model to American tariffs in 1983. The pattern fit, and the weight on welfare came "
            f"out between {P['gm_lo']} and {P['gm_hi']} times that on contributions: protection is for sale, but "
            "not cheaply."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(side[1]),
                      run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
