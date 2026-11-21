from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403


class Risk(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Risk, \ optimism and the record", r"How far can a project's own forecasts be trusted?",
             "Chapter ten. Risk, optimism and the record.", lit={1993: r"Kahneman and Lovallo", 2002: r"Flyvbjerg",
                                                                 2020: r"Hendren and Sprung-Keyser"},
             scale=("nation", "world"), horizon=("a decade", "a century"))
        self.megaprojects()
        self.outside()
        self.wait_()
        self.track_record()

    def megaprojects(self):
        T = tables.MEGAPROJECTS.data
        ax = plane([-0.6, 2.6], [0, 110], center=LEFT * 3.2 + DOWN * 0.5, x_length=5.6, y_length=4.8, xticks=[],
                   yticks=[0, 25, 50, 75, 100], ylabel=r"cost overrun, \ \% \ (mean, \ and one s.d.)",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        items = [(r"rail", T["rail"], COST), (r"bridges \\ and tunnels", T["fixed"], SAFE), (r"roads", T["road"],
                                                                                              BEN)]
        bars, labs, whisk = VGroup(), VGroup(), VGroup()
        for k, (n_, (m, sd, n), c_) in enumerate(items):
            p0, p1 = ax.ax.c2p(k - 0.3, 0), ax.ax.c2p(k + 0.3, m)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=c_, fill_opacity=0.8,
                               stroke_width=0).move_to((p0 + p1) / 2))
            whisk.add(Line(ax.ax.c2p(k, m), ax.ax.c2p(k, min(m + sd, 110)), color=c_, stroke_width=2))
            labs.add(VGroup(label(n_, font_size=16, color=c_), label(rf"{m:.1f}\% \ ({n})", font_size=15,
                                                                      color=c_)).arrange(DOWN, buff=0.05).next_to(
                ax.ax.c2p(k, 0), DOWN, buff=0.12))
        side = VGroup(
            label(r"258 transport projects, \ \$90 billion: \ nine in ten over budget", font_size=20, color=GREY_A),
            label(rf"rail passenger forecasts: \ {T['rail_demand']}\% too high on average", font_size=20,
                  color=COST),
            label(rf"the Channel Tunnel: \ about {T['chunnel']}\% over budget", font_size=20, color=GREY_A),
            label(r"`error or lie?': \ optimism, \ and strategic misrepresentation", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = published_tag(tables.MEGAPROJECTS.tag, corner=DL, font_size=12)
        with self.voiceover(
            "Every number in the bridge's appraisal is a forecast, and forecasts of public works have a record. "
            "<bookmark mark='a'/> Bent Flyvbjerg, Mette Skamris Holm and Søren Buhl collected 258 transport "
            "projects worth ninety billion dollars. Nine in ten cost more than forecast. <bookmark mark='b'/> In "
            f"constant prices, rail projects came in {T['rail'][0]:.0f} percent over on average, bridges and tunnels "
            f"{T['fixed'][0]:.0f} percent, roads {T['road'][0]:.0f} percent, with long tails. <bookmark mark='c'/> "
            f"Their forecasts of rail passengers were {T['rail_demand']} percent too high on average: twice the "
            "riders that came. The Channel Tunnel ran about eighty percent over budget. <bookmark mark='d'/> They "
            "asked whether this was error or lie. Errors would cancel out; these do not. Part is optimism, the "
            "planning fallacy of Daniel Kahneman's work; part, they argued, is strategic: an honest estimate loses "
            "the competition for funds."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.3), FadeIn(labs),
                      run_time=1.6)
            self.play(LaggedStart(*[Create(w_) for w_ in whisk], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def outside(self):
        R = load("risk")
        cost = np.sort(np.array(R["cost"]))
        ax = plane([0.4, 2.6], [0, 1], center=LEFT * 3.3 + UP * 0.9, x_length=5.6, y_length=2.2,
                   xticks=[0.5, 1.0, 1.5, 2.0, 2.5], yticks=[], xlabel=r"outturn cost $\div$ forecast, \ the Island's "
                   r"last 60 projects", xfmt=lambda v: f"{v:g}", font_size=13)
        rng = np.random.default_rng(3)
        dots = VGroup(*[Dot(ax.ax.c2p(min(c, 2.58), 0.2 + 0.6 * rng.random()), radius=0.05,
                            color=COST if c > 1 else BEN) for c in cost])
        one = DashedLine(ax.ax.c2p(1, 0), ax.ax.c2p(1, 1), color=WHITE, stroke_width=1.5)
        p80 = DashedLine(ax.ax.c2p(1 + R["uplift80"], 0), ax.ax.c2p(1 + R["uplift80"], 1), color=SAFE,
                         stroke_width=2)
        p80l = label(rf"80th percentile: \ $+{100 * R['uplift80']:.0f}\%$", font_size=16, color=SAFE).next_to(
            ax.ax.c2p(1 + R["uplift80"], 1), UP, buff=0.05)
        edges, hist = np.array(R["edges"]), np.array(R["hist"])
        hx = plane([-400, 400], [0, float(hist.max()) * 1.15], center=LEFT * 3.3 + DOWN * 2.2, x_length=5.6,
                   y_length=1.9, xticks=[-400, -200, 0, 200, 400], yticks=[], xlabel=r"the bridge's NPV, \ millions, "
                   r"\ 4,000 draws".replace(",", "{,}"), xfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0",
                   font_size=13)
        hb = VGroup()
        for a, b, h in zip(edges[:-1], edges[1:], hist):
            p0, p1 = hx.ax.c2p(a, 0), hx.ax.c2p(b, h)
            hb.add(Rectangle(width=(p1[0] - p0[0]) * 0.9, height=max(p1[1] - p0[1], 0.001),
                             fill_color=COST if b <= 0 else BEN, fill_opacity=0.75, stroke_width=0).move_to(
                (p0 + p1) / 2))
        fc = DashedLine(hx.ax.c2p(R["forecast"], 0), hx.ax.c2p(R["forecast"], float(hist.max()) * 1.15),
                        color=WHITE, stroke_width=2)
        side = VGroup(
            label(r"the outside view: \ ask how projects like this one turned out", font_size=20, color=E.ACCENT),
            label(rf"over budget: \ {100 * R['share_over']:.0f}\% of the 60; \ the median "
                  rf"$+{100 * R['uplift50']:.0f}\%$",
                  font_size=19, color=COST),
            label(rf"the bridge with an 80th-percentile uplift: \ NPV ${R['uplifted']:+.0f}$".replace("-", "{-}"),
                  font_size=19, color=SAFE),
            label(rf"forecast NPV ${R['forecast']:+.0f}$; \ with the record's costs and traffic: \ mean "
                  rf"${R['mc_mean']:+.0f}$".replace("-", "{-}"), font_size=19, color=WHITE),
            label(rf"the chance it loses money: \ {100 * R['p_negative']:.0f}\%", font_size=22, color=COST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"the Island: \ a reference class planted at Flyvbjerg's averages", corner=DL, font_size=12)
        with self.voiceover(
            "The cure Kahneman proposed is the outside view: before trusting the inside story of this project, ask "
            "how projects like it turned out. <bookmark mark='a'/> The Island has a record: its last sixty public "
            "works, each a dot at its outturn cost over its forecast, planted to match Flyvbjerg's averages. "
            f"<bookmark mark='b'/> {100 * R['share_over']:.0f} percent came in over budget; the median overrun was "
            f"{100 * R['uplift50']:.0f} percent, and one project in five overran by more than "
            f"{100 * R['uplift80']:.0f}. <bookmark mark='c'/> Britain's Treasury tells appraisers to raise their "
            "cost estimates for optimism bias, and its transport department takes the uplift from the reference "
            "class. Uplifted to the eightieth percentile, the bridge's net present "
            f"value at three and a half percent is minus {abs(R['uplifted']):.0f} million. <bookmark mark='d'/> Run "
            "the appraisal four thousand times, with costs and traffic drawn from the record, and its forecast of "
            f"plus {R['forecast']:.0f} million becomes an average of minus {abs(R['mc_mean']):.0f}, <bookmark "
            f"mark='e'/> with a {100 * R['p_negative']:.0f} percent chance of losing money. The bridge that passed on "
            "its own forecasts fails on the record of forecasts like them."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(ax), Create(one), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(p80), FadeIn(p80l), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(hx), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in hb], lag_ratio=0.03), Create(fc),
                      FadeIn(side[3]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def wait_(self):
        R = load("risk")
        W, Wo = R["wait"], R["wait_overrun"]

        def tree(w, title, col):
            now = label(rf"build now: \ ${w['now']:+.0f}$".replace("-", "{-}"), font_size=21, color=col)
            hi = label(rf"high traffic: \ build, \ ${w['npv_high']:+.0f}$".replace("-", "{-}"), font_size=18,
                       color=BEN)
            lo = label(rf"low traffic: \ don't, \ 0 \ (would be ${w['npv_low']:+.0f}$)".replace("-", "{-}"),
                       font_size=18, color=COST)
            wt = label(rf"wait a year: \ ${w['wait']:+.0f}$".replace("-", "{-}"), font_size=21, color=col)
            br = VGroup(hi, lo).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            g = VGroup(label(title, font_size=20, color=GREY_A), now, wt, br).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.25)
            br.shift(RIGHT * 0.5)
            val = label(rf"the option to wait: \ {w['value']:.0f}", font_size=22, color=E.ACCENT).next_to(g, DOWN,
                                                                                                      buff=0.3)
            return VGroup(g, val)

        t1 = tree(W, r"the forecast costs", TRAV)
        t2 = tree(Wo, r"costs 28\% over, \ as the record suggests", SAFE)
        both = VGroup(t1, t2).arrange(RIGHT, buff=1.2, aligned_edge=UP)
        both.scale(min(1.35, 12.4 / both.width)).move_to(DOWN * 0.2)
        head = label(r"the option to wait: \ next year the traffic is known, \ high or low", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Uncertainty has a second consequence. A bridge cannot be unbuilt, so waiting has a value, Part "
            "twenty-three's option to wait. <bookmark mark='a'/> Suppose that a year from now the Island will know "
            "whether traffic will be thirty percent above the forecast or thirty percent below. Build now, and the "
            f"expected net present value is {W['now']:.0f} million. <bookmark mark='b'/> Wait, and build only if "
            f"traffic turns out high: {W['wait']:.0f} million, even after a year's delay. The option is worth "
            f"{W['value']:.0f} million. <bookmark mark='c'/> If costs run twenty-eight percent over, as the record "
            f"suggests they will, building now is worth minus {abs(Wo['now']):.0f}, and waiting "
            f"{Wo['wait']:.0f}: <bookmark mark='d'/> the option to wait is worth {Wo['value']:.0f} million, more "
            "than the bridge itself. Irreversible decisions under uncertainty should be taken later than a simple "
            "net present value says."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t1[0][0]), FadeIn(t1[0][1]))
            vo.wait_until("b")
            self.play(FadeIn(t1[0][2]), FadeIn(t1[0][3]), FadeIn(t1[1]))
            vo.wait_until("c")
            self.play(FadeIn(t2[0]))
            vo.wait_until("d")
            self.play(FadeIn(t2[1]))
        self.clear_scene()

    def track_record(self):
        T = tables.MVPF_2020.data
        hc = history_card(2020, r"Nathaniel Hendren and Ben Sprung-Keyser", rf"{T['policies']} American policies of "
                          r"the last half-century, \ each scored after the fact as willingness to pay over its net "
                          r"cost to the government", color=BEN, width=11.0, font_size=22)
        rows = VGroup(
            label(r"children's health and education: \ the highest values; \ many paid for themselves", font_size=24,
                  color=BEN),
            label(rf"policies for adults: \ mostly between {T['adult_lo']} and {T['adult_hi']:.0f}", font_size=24,
                  color=TRAV),
            label(r"the appraisal before, \ the evaluation after: \ only the second is scored against outcomes",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        VGroup(hc, rows).arrange(DOWN, buff=0.55).move_to(DOWN * 0.1)
        tag = published_tag(tables.MVPF_2020.tag, corner=DL, font_size=12)
        with self.voiceover(
            "The other half of the record is evaluation after the fact, when the outcomes are known. <bookmark "
            "mark='a'/> Part forty-two's marginal value of public funds puts that on one scale. Nathaniel Hendren "
            f"and Ben Sprung-Keyser scored {T['policies']} American policies, from what their beneficiaries would "
            "pay for them and what they really cost the government, long-run taxes included. <bookmark mark='b'/> "
            "Spending on children's health and education came out highest, and much of it paid for itself. "
            f"<bookmark mark='c'/> Policies for adults mostly delivered between {T['adult_lo']} and "
            f"{T['adult_hi']:.0f} dollars of value per dollar of net cost. <bookmark mark='d'/> An appraisal is a "
            "forecast; an evaluation is the score. Governments that commission both, and compare them, learn which "
            "of their forecasts to trust."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(hc, color=BEN, time_width=0.6), run_time=1.2)
            for mk, r_ in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()
