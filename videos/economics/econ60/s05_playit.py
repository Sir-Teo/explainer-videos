from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Play it: \ a hundred seats, \ sixty days", r"Which weekly pricing rule earns the most?",
             "Chapter four. Play it: a hundred seats, sixty days.", scale=("firm",), horizon=("a day", "a year"))
        self.stage()
        self.reveal()

    def stage(self):
        D = load("dynamic")
        P = load("playit")
        F = D["flight"]
        days = np.arange(60)
        ax = plane([0, 60], [0, 340], center=LEFT * 2.6 + DOWN * 0.5, x_length=6.6, y_length=4.4,
                   xticks=[0, 10, 20, 30, 40, 50, 60], yticks=[0, 100, 200, 300],
                   xlabel=r"day of the sale \ (departure on day 60)", ylabel=r"fare, \ \$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        x_sw = F["days"] - F["switch"]
        sw = vline(ax, x_sw, 0, 340, BUS, 1.6)
        swl = label(r"business travellers \\ start booking", font_size=14, color=BUS).next_to(
            ax.ax.c2p(x_sw, 340), DOWN, buff=0.1).shift(RIGHT * 0.9)
        one = path(ax, days, np.full(60, P["fixed_price"]), WHITE, 3.0, smooth=False)
        weeks = days // 7
        low = path(ax, days, np.interp(weeks, [0, 8], [90.0, 300.0]), LEIS, 3.0, smooth=False)
        high = path(ax, [0, 14], [320, 320], COST, 3.0, smooth=False)
        hl = label(r"then cut 15\% \\ after a slow week", font_size=14, color=COST).next_to(ax.ax.c2p(14, 320), RIGHT,
                                                                                            buff=0.1)
        opts = VGroup(
            label(rf"A \ \ one fare all along: \ \${P['fixed_price']:.0f}", font_size=22, color=WHITE),
            label(r"B \ \ start high at \$320, \ cut 15\% after any week \\ \ \ \ \ \ that sells fewer than its share",
                  font_size=22, color=COST),
            label(r"C \ \ start low at \$90, \ raise it every week \\ \ \ \ \ \ to \$300 in the last week",
                  font_size=22, color=LEIS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35).shift(UP * 0.5)
        if opts.width > 6.2:
            opts.width = 6.2
            opts.to_edge(RIGHT, buff=0.35)
        facts = label(rf"leisure buyers early, \ about {F['early']:.0f} a day; \ business buyers in the last "
                      rf"{F['switch']} days, \ about {F['late']:.0f} a day, \ who will pay about three times as much",
                      font_size=17, color=GREY_A).to_edge(UP, buff=0.4)
        if facts.width > 13.0:
            facts.width = 13.0
        tag = island_tag(r"the Island: \ agora.revenue.flight; \ 2,000 simulated flights per rule".replace(",", "{,}"),
                         corner=DL, font_size=12)
        with self.voiceover(
            "Your turn. You price the Island's flight: a hundred seats, sixty days of sales, one fare a week. "
            "<bookmark mark='a'/> Leisure travellers arrive throughout, about five a day at a low enough fare; in "
            "the last three weeks business travellers arrive too, fewer of them, but willing to pay about three "
            "times as much. Nobody knows exactly how many will come. <bookmark mark='b'/> Rule A: one fare all "
            f"along, {P['fixed_price']:.0f} dollars, the best single fare for this flight. <bookmark mark='c'/> "
            "Rule B: start high, at three hundred and twenty, and cut fifteen percent after any week that sells "
            "fewer seats than its share, so the plane fills. <bookmark mark='d'/> Rule C: start low, at ninety, and "
            "raise the fare every week, to three hundred in the last. <bookmark mark='e'/> Which rule earns the "
            "most?"
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(facts), Create(sw), FadeIn(swl))
            vo.wait_until("b")
            self.play(Create(one), FadeIn(opts[0]))
            vo.wait_until("c")
            self.play(Create(high), FadeIn(hl), FadeIn(opts[1]))
            vo.wait_until("d")
            self.play(Create(low), FadeIn(opts[2]))
            vo.wait_until("e")
        ring = countdown().scale(0.6).next_to(opts, DOWN, buff=0.5)
        self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=7.0, rate_func=linear)
        self.play(FadeOut(ring), Indicate(opts[2], color=WHITE, scale_factor=1.05))
        self.wait(0.5)
        self.clear_scene()

    def reveal(self):
        P = load("playit")
        Rr = P["rules"]
        order = ("start high, cut", "one price", "start low, raise", "optimal")
        names = (r"B: start high, \\ cut", r"A: one fare", r"C: start low, \\ raise", r"the optimum \\ (chapter six)")
        cols = (COST, WHITE, LEIS, OPT)
        top = max(Rr[k]["mean"] for k in order) * 1.15
        ax = plane([-0.6, 3.6], [0, top], center=LEFT * 2.6 + DOWN * 0.4, x_length=6.6, y_length=4.6, xticks=[],
                   yticks=[0, 5000, 10000, 15000], ylabel=r"revenue per flight, \ \$",
                   yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=14)
        b = bars(ax, range(4), [Rr[k]["mean"] for k in order], cols, width=0.55)
        labs = VGroup(*[label(n, font_size=14, color=c).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.1)
                        for k, (n, c) in enumerate(zip(names, cols))])
        vals = VGroup(*[label(rf"{Rr[k]['mean']:,.0f} \\ ({Rr[k]['sold']:.0f} seats)".replace(",", "{,}"),
                              font_size=14, color=c).next_to(x, UP, buff=0.05) for k, c, x in zip(order, cols, b)])
        side = VGroup(
            label(r"C wins: \ raise the fare as departure nears", font_size=22, color=LEIS),
            label(r"B is worst: \ cutting late gives business travellers \\ the discount meant for leisure",
                  font_size=19, color=COST),
            label(r"A fills more seats than C, \ and earns less", font_size=19, color=WHITE),
            label(r"the optimum: \ low early, \ high late, \\ and every day it responds to the seats left",
                  font_size=19, color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ 2,000 simulated flights per rule".replace(",", "{,}"), corner=DL,
                         font_size=12)
        with self.voiceover(
            "Here is what two thousand simulated flights earned under each rule. <bookmark mark='a'/> Rule B, start "
            f"high and cut, earns least, {Rr['start high, cut']['mean']:,.0f} dollars a flight: when early weeks sell "
            "slowly it cuts, and the cuts last into the weeks when business travellers arrive, who get a fare meant "
            f"for leisure. <bookmark mark='b'/> Rule A, one fare, earns {Rr['one price']['mean']:,.0f}, and fills "
            "more seats. <bookmark mark='c'/> Rule C, start low and raise, earns the most of the three, "
            f"{Rr['start low, raise']['mean']:,.0f}. So C. The direction of the fare should follow who is buying: "
            "low while the price-sensitive buy, high when those who must travel arrive. <bookmark mark='d'/> The "
            f"best possible policy earns about {Rr['optimal']['mean']:,.0f}, and it does one more thing: every day it "
            "looks at how many seats are left, and raises the fare when the plane is filling fast. Chapters five "
            "and six derive it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(vals[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(vals[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[2], DOWN), FadeIn(vals[2]), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(GrowFromEdge(b[3], DOWN), FadeIn(vals[3]), FadeIn(side[3]))
        self.clear_scene()
