from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Simulation(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Merger simulation in court", r"Same data, \ different demand curves: \ how far apart can "
             r"the answers be?", "Chapter six. Merger simulation in court.",
             lit={1999: r"Crooke, Froeb, Tschantz and Werden"}, scale=("market",), horizon=("a year",))
        self.forms()
        self.attacks()
        self.agency()

    def forms(self):
        F = load("forms")
        rise = F["rise"]
        cols = (CEDAR, ALDER, BIRCH, CARTEL)
        names = (r"linear", r"logit", r"linear in \\ log price", r"constant \\ elasticity")
        top = max(rise) * 1.15
        ax = plane([-0.6, 3.6], [0, top], center=LEFT * 2.6 + DOWN * 0.5, x_length=6.8, y_length=4.6, xticks=[],
                   yticks=[0, 5, 10, 15, 20, 25], ylabel=r"predicted price rise, \ \%", yfmt=lambda v: f"{v:.0f}",
                   font_size=15)
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        for k, (v, col, n) in enumerate(zip(rise, cols, names)):
            p0, p1 = ax.ax.c2p(k - 0.3, 0), ax.ax.c2p(k + 0.3, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=0.85,
                               stroke_width=0).move_to((p0 + p1) / 2))
            vals.add(label(f"{v:.1f}", font_size=17, color=col).next_to(bars[-1], UP, buff=0.06))
            labs.add(label(n, font_size=15, color=col).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.15))
        g = DashedLine(ax.ax.c2p(-0.6, F["guppi"]), ax.ax.c2p(3.6, F["guppi"]), color=GOV, stroke_width=2)
        gl = label(rf"GUPPI {F['guppi']:.0f}\%", font_size=16, color=GOV).next_to(ax.ax.c2p(3.6, F["guppi"]), UP,
                                                                                  buff=0.05).shift(LEFT * 0.6)
        side = VGroup(
            label(r"two identical firms; \ the same data for every curve:", font_size=20, color=GREY_A),
            label(rf"price 1, \ margin {100 * F['m']:.0f}\%, \ diversion {100 * F['D']:.0f}\%, \ own elasticity "
                  rf"{F['elasticity']:.2f}", font_size=20, color=WHITE),
            label(r"the curves agree at today's price \\ and differ only in how they bend away from it",
                  font_size=20, color=E.ACCENT),
            label(r"the more the demand curve flattens as price rises, \\ the less a merged firm wants to raise it",
                  font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(UP * 0.5)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = agora_tag(r"computed: \ agora.merger.functional\_forms", corner=DL, font_size=12)
        with self.voiceover(
            "A simulation needs a demand system, and the demand system must be extended from the prices we see to "
            "prices nobody has charged. <bookmark mark='a'/> Take two identical firms. Each sells at a price of one, "
            f"with a margin of {100 * F['m']:.0f} percent and a diversion ratio of {100 * F['D']:.0f} percent to "
            "the other. Fit four standard demand curves to exactly these numbers. They agree at today's price, in "
            "level, slope and diversion. <bookmark mark='b'/> Simulate the merger with each. Linear demand predicts "
            f"a rise of {rise[0]:.1f} percent; the logit {rise[1]:.1f}; demand that falls with the log of price "
            f"{rise[2]:.1f}; and constant elasticity {rise[3]:.1f}. <bookmark mark='c'/> "
            "The difference is curvature: how the demand curve bends as price rises, which no data at today's "
            "prices can reveal. Gregory Werden and his coauthors made the point in 1999, and every simulation "
            "presented in court has been attacked along it since. The GUPPI, a first-order number, sits in the "
            "middle and does not pretend to know."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            for k in range(4):
                self.play(GrowFromEdge(bars[k], DOWN), FadeIn(vals[k]), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]), Create(g), FadeIn(gl))
        self.clear_scene()

    def attacks(self):
        cards = point_cards([
            (r"the curve", r"why logit and not linear? \ the prediction moves with the shape", CARTEL),
            (r"the elasticities", r"estimated on which prices, \ which instruments, \ which years?", ALDER),
            (r"the conduct", r"Bertrand pricing assumed: \ were the firms already coordinating?", BIRCH),
            (r"the outside good", r"how many buyers would stop buying at all? \ it sets the market's size", SHOPS),
            (r"the savings", r"left out, \ or taken on trust?", SAVE),
            (r"what it adds", r"it forces every assumption into the open, \ where it can be tested", E.ACCENT),
        ], width=12.8, cols=3, font_size=20).move_to(DOWN * 0.2)
        head = label(r"how a simulation is cross-examined", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "So a simulation is attacked in a few standard places. <bookmark mark='a'/> The shape of demand, as you "
            "just saw. <bookmark mark='b'/> The elasticities: estimated from which prices, with which instruments, "
            "over which years. <bookmark mark='c'/> The conduct: Bertrand competition before the merger is "
            "assumed; if the firms were already coordinating, the model is wrong from the start. <bookmark "
            "mark='d'/> The outside good: how many buyers would stop buying altogether, which sets how much the "
            "inside firms can raise prices together. <bookmark mark='e'/> And the cost savings: left out, or "
            "taken on trust. <bookmark mark='f'/> What a simulation adds is not a better number than the evidence "
            "it rests on. It is discipline: every assumption is written down, and each can be tested against the "
            "documents and the data. Judges have been wary of simulations they could not follow, and readier to "
            "credit ones that agree with the firms' own records."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()

    def agency(self):
        A = load("agency")
        pred, truth, cedar = np.array(A["predicted"]), np.array(A["truth"]), np.array(A["cedar"], bool)
        ax = plane([0, 25], [0, 25], center=LEFT * 2.8 + DOWN * 0.4, x_length=5.0, y_length=5.0,
                   xticks=[0, 5, 10, 15, 20, 25], yticks=[0, 5, 10, 15, 20, 25],
                   xlabel=r"the agency's prediction, \ \%",
                   ylabel=r"the truth, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        diag = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(25, 25), color=GREY_C, stroke_width=1.4)
        pts = VGroup(*[Dot(ax.ax.c2p(min(p, 24.6), min(t, 24.6)), radius=0.07, color=WHITE if c else BIRCH)
                       for p, t, c in zip(pred, truth, cedar)])
        side = VGroup(
            label(r"the agency's model: \ a plain logit, \\ calibrated to each town's prices, \ shares \\ and "
                  r"Alder's true elasticity", font_size=19, color=SIM),
            label(rf"its average prediction: \ +{A['mean_predicted']:.1f}\%", font_size=22, color=SIM),
            label(rf"the truth: \ +{A['mean_truth']:.1f}\%", font_size=22, color=WHITE),
            label(r"white: \ towns with Cedar; \ gold: \ without", font_size=17, color=GREY_A),
            label(r"the plain logit sends lost sales to rivals \\ in proportion to their shares: \\ it cannot know "
                  r"the superstores are closer to each other \\ than to the corner shops", font_size=18,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"the Island: \ the 36 towns where Alder and Birch meet", corner=DL, font_size=12)
        with self.voiceover(
            "On the Island we can do what no court can: compare a simulation with the truth. <bookmark mark='a'/> "
            "Suppose the agency uses a plain logit, calibrated in each town to the prices, the shares and even "
            "Alder's true own-price elasticity. <bookmark mark='b'/> Town by town, it predicts the merger will raise "
            f"Alder's price by {A['mean_predicted']:.1f} percent on average. <bookmark mark='c'/> The truth is "
            f"{A['mean_truth']:.1f}. <bookmark mark='d'/> Every town sits above the diagonal, most of all the gold "
            "ones, where Cedar is absent and the merger leaves Alder with no superstore rival. <bookmark mark='e'/> "
            "The plain logit sends customers who leave Alder to every rival in proportion to its share, so it "
            "cannot know that superstores are closer substitutes for each other than for the corner shops. It "
            "understates the diversion between the merging chains, and so the harm. Getting the substitution "
            "pattern right was the whole point of Part forty-three's random coefficients and nests."
        ) as vo:
            self.play(FadeIn(ax), Create(diag), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p, scale=1.4) for p in pts], lag_ratio=0.04), FadeIn(side[3]),
                      run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
