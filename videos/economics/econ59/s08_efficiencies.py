from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Efficiencies(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Efficiencies, \ pass-through and entry", r"If the merger saves costs, \ how much reaches "
             r"the buyers?", "Chapter seven. Efficiencies, pass-through and entry.",
             lit={1997: r"Staples' 15--17\%"}, scale=("firm", "market"), horizon=("a year",))
        self.pass_through()
        self.staples()
        self.entry()

    def pass_through(self):
        E_ = load("efficiency")
        pt = E_["pass_through"]
        ax = plane([-0.6, 2.6], [0, 100], center=LEFT * 2.8 + DOWN * 0.4, x_length=6.0, y_length=4.6, xticks=[],
                   yticks=[0, 25, 50, 75, 100], ylabel=r"share of a cost saving passed on, \ \%",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        vals = [100 * pt["single"], 100 * pt["merged"][0], 100 * pt["merged"][1]]
        cols = (ALDER, SIM, BIRCH)
        names = (r"Alder alone \\ cuts its cost", r"the merged firm: \\ Alder", r"the merged firm: \\ Birch")
        bars, labs, vl = VGroup(), VGroup(), VGroup()
        for k, (v, c, n) in enumerate(zip(vals, cols, names)):
            p0, p1 = ax.ax.c2p(k - 0.3, 0), ax.ax.c2p(k + 0.3, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=c, fill_opacity=0.85,
                               stroke_width=0).move_to((p0 + p1) / 2))
            labs.add(label(n, font_size=15, color=c).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.15))
            vl.add(label(f"{v:.0f}", font_size=18, color=c).next_to(bars[-1], UP, buff=0.06))
        side = VGroup(
            label(r"a 2\% cut in marginal cost", font_size=21, color=SAVE),
            label(r"pass-through below 100\% \\ with logit demand: \ the margin absorbs some", font_size=19,
                  color=GREY_A),
            label(r"the merged firm passes on less: \\ a lower price now also steals sales \\ from its own other "
                  r"chain", font_size=19, color=SIM),
            label(r"the guidelines count savings that are \\ verifiable, \ specific to the merger, \ and passed "
                  r"on", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"the Island: \ the town with all three chains", corner=DL, font_size=12)
        with self.voiceover(
            "The merging firms always say the deal will save money, and lower costs push prices down. But how much "
            "of a saving reaches buyers? That is the pass-through rate. <bookmark mark='a'/> On the Island, cut "
            "Alder's marginal cost by two percent with Alder still independent, and its price falls by "
            f"{vals[0]:.0f} percent of the saving: the logit's curvature lets the margin absorb the rest. <bookmark "
            f"mark='b'/> Give the same saving to the merged firm, and it passes on only {vals[1]:.0f} percent at "
            "Alder and about as much at Birch. A lower price at Alder now also steals sales from Birch, which the "
            "merged firm owns, so cutting is worth less. <bookmark mark='c'/> That is why the guidelines credit "
            "savings only if they are verifiable, specific to the merger, and likely to be passed on, and why the "
            "relevant pass-through is the merged firm's, not the industry's."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(labs), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(vl[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], DOWN), GrowFromEdge(bars[2], DOWN), FadeIn(vl[1]), FadeIn(vl[2]),
                      FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def staples(self):
        rows = VGroup(
            label(r"the companies: \ two-thirds of the savings would reach customers", font_size=24, color=DEF),
            label(r"the FTC's economists: \ a cost change at one firm, \ not the industry", font_size=24, color=GOV),
            MathTex(r"\ln p_{st} = \alpha_s + \theta_t + \beta\,\ln c^{\,\text{firm}}_{st} + \gamma\,\ln "
                    r"c^{\,\text{industry}}_{t} + \varepsilon_{st}", font_size=32, color=WHITE),
            label(r"Staples' own history: \ about 15--17\% of firm-specific cost changes passed on", font_size=24,
                  color=GOV),
            label(r"the court relied on it: \ the claimed savings could not offset the harm", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(DOWN * 0.1)
        tag = published_tag(r"FTC v. Staples (1997); \ Ashenfelter, Ashmore, Baker and McKernan, \ FTC working "
                            r"paper 217 (1998)", corner=DL, font_size=12)
        with self.voiceover(
            "This was a turning point in the Staples case. <bookmark mark='a'/> The companies projected large "
            "savings and said two-thirds of them would be passed on to customers. <bookmark mark='b'/> The FTC's "
            "economists and its expert, Orley Ashenfelter, pointed out that a merger's savings are a cost change at "
            "one "
            "firm, and firms pass on a cost change that hits only them much less than one that hits the whole "
            "industry, since rivals' prices do not move with it. <bookmark mark='c'/> They separated the two in "
            "Staples' own data, in a regression of this kind: prices on the firm's own costs and on the costs "
            "common to everyone. <bookmark mark='d'/> Historically Staples had passed on only about fifteen to "
            "seventeen percent of firm-specific cost changes. <bookmark mark='e'/> The judge quoted the comparison "
            "in his opinion: two-thirds claimed, fifteen to seventeen percent in the record. The savings could not "
            "save the merger."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=UP * 0.1))
        self.clear_scene()

    def entry(self):
        E_ = load("efficiency")
        T = load("towns")
        mp = island_map(T, width=6.4, height=3.8).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        me = np.array([np.nan if v is None else v for v in T["merger_effect"]], float)
        for k, d in enumerate(mp.dots):
            if not T["birch"][k]:
                d.set_opacity(0.15)
        side = VGroup(
            label(r"the merger's true effect on Alder's price", font_size=20, color=GREY_A),
            label(rf"where Cedar is present \ ({E_['n_cedar']} towns): \ +{E_['effect_cedar']:.1f}\%", font_size=22,
                  color=WHITE),
            label(rf"where it is not \ ({E_['n_no_cedar']} towns): \ +{E_['effect_no_cedar']:.1f}\%", font_size=22,
                  color=BIRCH),
            label(r"entry must be timely, \ likely and sufficient: \\ a rival that could come is not a rival that "
                  r"is there", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.45)
        tag = island_tag(r"the Island: \ the towns where Alder and Birch meet, \ lit", corner=DL, font_size=12)
        lo, hi = np.nanmin(me), np.nanmax(me)
        with self.voiceover(
            "The other standard defence is entry: if prices rise, someone new will come. <bookmark mark='a'/> On "
            "the Island the truth answers it town by town. <bookmark mark='b'/> Where Cedar is already present, "
            f"the merger raises Alder's price by {E_['effect_cedar']:.1f} percent: Cedar is the discipline. "
            f"<bookmark mark='c'/> Where it is not, by {E_['effect_no_cedar']:.1f}. Across the towns the effect runs "
            f"from {100 * lo:.0f} to {100 * hi:.0f} percent. <bookmark mark='d'/> So the defence's question is "
            "whether Cedar would arrive in the towns it has stayed out of, and the guidelines ask that entry be "
            "timely, likely and sufficient to undo the harm. A rival that could come is not a rival that is there; "
            "a store takes years to open, and Cedar stayed out of those towns for reasons that a merger does not "
            "remove."
        ) as vo:
            self.play(FadeIn(mp.coast), FadeIn(mp.dots), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]),
                      *[Indicate(d, color=WHITE, scale_factor=1.6) for k, d in enumerate(mp.dots)
                        if T["birch"][k] and T["cedar"][k]])
            vo.wait_until("c")
            self.play(FadeIn(side[2]),
                      *[Indicate(d, color=BIRCH, scale_factor=1.6) for k, d in enumerate(mp.dots)
                        if T["birch"][k] and not T["cedar"][k]])
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
