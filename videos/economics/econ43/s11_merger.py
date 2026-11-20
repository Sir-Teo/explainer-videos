from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class Merger(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Merger simulation and new goods", r"What would a merger do, and what is a new product worth?",
             "Chapter nine. Merger simulation and new goods.", lit={1996: r"Werden", 2002: r"Petrin"},
             scale=("firm", "market"), horizon=("a year",))
        self.recipe()
        self.island()
        self.savings()
        self.newgood()

    def recipe(self):
        steps = flow_chain([(r"estimate demand", DEMAND), (r"recover costs", COST), (r"change the owners", PRICE),
                            (r"solve again", LOSS)],
                           notes=[r"elasticities and \\ diversion ratios", r"price minus the \\ markup that \\ conduct "
                                  r"implies", r"merge two firms' \\ rows of $\Omega$", r"new equilibrium \\ prices"],
                           box_w=2.7, font_size=20, note_size=16).move_to(UP * 0.5)
        foot = label(r"the same costs, \ the same demand, \ new incentives", font_size=22,
                     color=E.ACCENT).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.MERGER_2023.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Demand and conduct also predict what a merger would do, before it happens. The recipe has four "
            "steps. <bookmark mark='a'/> Estimate demand, which gives elasticities and the diversion ratios of "
            "chapter two. <bookmark mark='b'/> Recover each product's marginal cost as price minus the markup "
            "competition implies. <bookmark mark='c'/> Merge two firms: in the ownership matrix, their products "
            "now share an owner. <bookmark mark='d'/> Solve for the new equilibrium prices. <bookmark mark='e'/> "
            "Costs and demand are unchanged; only the incentives are new, because each merged brand now counts the "
            "sales it pushes to its new sister as kept, not lost."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(steps.boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps.notes[0]))
            for k, mk in zip(range(3), "bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(steps.arrows[k]), FadeIn(steps.boxes[k + 1]), FadeIn(steps.notes[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def island(self):
        M = load("merger")
        R = load("cereal")
        own = np.array(R["owner"])
        J = len(own)
        dp = np.array(M["dp"])
        ax = plane([0, J], [0, 0.08], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[], yticks=[0, 0.02, 0.04, 0.06, 0.08], ylabel=r"price change after the merger",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        bars = VGroup()
        for j in range(J):
            p0, p1 = ax.ax.c2p(j + 0.5, 0), ax.ax.c2p(j + 0.5, max(dp[j], 0.0005))
            bars.add(Rectangle(width=0.42, height=max(p1[1] - p0[1], 0.01), stroke_width=0,
                               fill_color=FIRM[own[j]], fill_opacity=0.9 if M["merged"][j] else 0.45).move_to(
                (p0 + p1) / 2))
        marks = VGroup()
        for f in range(4):
            idx = np.where(own == f)[0]
            a, b = ax.ax.c2p(idx.min() + 0.08, -0.003), ax.ax.c2p(idx.max() + 0.92, -0.003)
            marks.add(Line(a, b, color=FIRM[f], stroke_width=6))
        side = VGroup(
            label(rf"the two smaller firms merge: \\ {100 * M['share_merged']:.0f}\% of sales", font_size=18,
                  color=WHITE),
            label(rf"Herfindahl: \ {M['hhi0']:,.0f} $\to$ \\ {M['hhi1']:,.0f} \ (+{M['dhhi']:,.0f})", font_size=18,
                  color=GREY_A),
            label(rf"their prices: \ +{100 * M['dp_merged']:.1f}\%", font_size=19, color=LOSS),
            label(rf"rivals: \ +{100 * M['dp_rivals']:.1f}\%: \\ they follow a little", font_size=19, color=DEMAND),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Run it on the Island's aisle. <bookmark mark='a'/> The two smaller firms, with "
            f"{say_pct(M['share_merged'], 0)} of sales between them, propose to merge, and the simulation puts a "
            f"number on the harm: the merging brands' prices rise by {say_pct(M['dp_merged'], 1)} on average. "
            f"<bookmark mark='b'/> The Herfindahl index rises by {M['dhhi']:,.0f} points, to {M['hhi1']:,.0f}: under "
            "the American guidelines, a merger presumed to harm competition. <bookmark mark='d'/> The rivals' prices "
            f"rise too, by {say_pct(M['dp_rivals'], 1)}, because with dearer competitors they can charge a little "
            "more. No collusion is involved; the merger simply changes what is privately optimal."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(marks), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(bars[j], DOWN) for j in range(J) if M["merged"][j]],
                                  lag_ratio=0.2), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(bars[j], DOWN) for j in range(J) if not M["merged"][j]],
                                  lag_ratio=0.1), FadeIn(side[3]), run_time=1.5)
        self.clear_scene()

    def savings(self):
        M = load("merger")
        eq = MathTex(r"c^{\,\text{after}} \;=\; p \;+\; \big(\Omega^{\,\text{after}} \circ "
                     r"\tfrac{\partial s}{\partial p}'\big)^{-1} s", font_size=40, color=E.ACCENT).to_edge(UP, buff=0.7)
        sub = label(r"the costs at which the merged firm would choose today's prices", font_size=20,
                    color=GREY_A).next_to(eq, DOWN, buff=0.25)
        c = np.array(M["cmcr"])
        merged = np.array(M["merged"])
        vals = c[merged]
        R = load("cereal")
        own = np.array(R["owner"])
        bars = VGroup()
        for k, v in enumerate(vals):
            r = Rectangle(width=0.9, height=v * 18, stroke_width=0, fill_color=FIRM[own[np.where(merged)[0][k]]],
                          fill_opacity=0.85)
            r.move_to(np.array([-3.0 + 1.3 * k, -2.4 + v * 9, 0]))
            bars.add(VGroup(r, label(rf"{100 * v:.0f}\%", font_size=19, color=WHITE).next_to(r, UP, buff=0.1)))
        side = VGroup(
            label(rf"the merged brands' costs \\ must fall about {100 * M['cmcr_merged']:.0f}\% \\ for prices to "
                  r"stay put", font_size=20, color=GAIN),
            label(r"savings that large \\ are rare, \ and must be \\ verifiable and specific \\ to the merger",
                  font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(RIGHT * 3.6 + DOWN * 0.9)
        tag = published_tag(r"Werden (1996); \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Mergers can also save costs, which pushes prices down. How large would the savings have to be? "
            "<bookmark mark='a'/> Gregory Werden's answer: find the marginal costs at which the merged firm would "
            "choose exactly today's prices. <bookmark mark='b'/> On the Island the merging brands' costs would have "
            f"to fall by about {say_pct(M['cmcr_merged'], 0)}, brand by brand as shown. <bookmark mark='c'/> "
            "Savings that large in the cost of one more box are rare, and the agencies count only savings that are "
            "verifiable and specific to the merger, a standard that chapter fourteen's beer story puts to the test."
        ) as vo:
            self.play(Write(eq), FadeIn(sub), FadeIn(tag), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_[0], DOWN) for b_ in bars], lag_ratio=0.2),
                      *[FadeIn(b_[1]) for b_ in bars], FadeIn(side[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def newgood(self):
        N = load("newgood")
        sg = np.array(N["sigma"])
        g = np.array(N["gains"])
        ax = plane([0, 1.0], [0, 0.1], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=[0, 0.025, 0.05, 0.075, 0.1],
                   xlabel=r"nesting parameter $\sigma$: \ how alike products in a nest are",
                   ylabel=r"gain per shopper from a copy of Nut Clusters, \ dollars",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.3f}", font_size=14)
        ln = path(ax, sg, g, BLP_C, 3.2)
        lg = dot(ax, 0.0, N["logit"], LOSS, 0.1)
        gm = dot(ax, N["game_sigma"], N["at_game"], PRICE, 0.09)
        side = VGroup(
            label(rf"plain logit \ ($\sigma$ = 0): \\ an identical copy \\ is worth \${N['logit']:.3f} \\ to every "
                  r"shopper", font_size=18, color=LOSS),
            label(rf"the game's nests \\ ($\sigma$ = {N['game_sigma']}): \ \${N['at_game']:.3f}", font_size=18,
                  color=PRICE),
            label(r"perfect substitutes: \\ nothing", font_size=18, color=BLP_C),
            label(rf"Petrin: \ the minivan \\ ({N['minivan']}); \ who buys \\ tells what it is \\ worth",
                  font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.PETRIN_2002.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Demand also values new products, and here the logit's flaw becomes absurd. <bookmark mark='a'/> In the "
            "plain logit every product carries its own independent taste, so adding an exact copy of Nut Clusters, "
            f"same box, same price, gives every shopper a gain worth {N['logit']:.3f} dollars, about "
            f"{say_pct(N['pct_logit'], 0)} of its price, from the chance that they like the copy better. "
            "<bookmark mark='b'/> With the game's nests the gain is "
            f"{N['at_game']:.3f} dollars, <bookmark mark='c'/> and as products in a nest become perfect substitutes "
            "it vanishes, as it should. <bookmark mark='d'/> In 2002 Amil Petrin measured the value of the minivan, "
            f"introduced in {N['minivan']}. Adding information on who buys which car, families buying minivans, to "
            "the market data changed the estimated gains substantially; the plain logit overstated them. What a new "
            "product is worth depends on how it is different, and from whom it draws its buyers."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=1.8)
            vo.wait_until("a")
            self.play(FadeIn(lg, scale=1.5), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(gm, scale=1.5), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
