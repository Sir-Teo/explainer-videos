from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Unilateral(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Unilateral effects: \ diversion and pricing pressure", r"Why would a merged firm raise its "
             r"prices, \ with no collusion at all?", "Chapter five. Unilateral effects: diversion and pricing "
             r"pressure.", lit={2010: r"Farrell and Shapiro"}, scale=("firm", "market"), horizon=("a year",))
        self.diversion()
        self.derive()
        self.numbers()

    def diversion(self):
        U = load("upp")
        D = np.array(U["diversion_matrix"])
        names = ("Alder", "Birch", "Cedar", "shops")
        cols = (ALDER, BIRCH, CEDAR, SHOPS)
        cell = 1.15
        grid = VGroup()
        for i in range(4):
            for j in range(4):
                v = D[i, j]
                sq = Square(side_length=cell * 0.94, stroke_width=0, fill_color=GOV if i != j else GREY_D,
                            fill_opacity=0.12 + 0.8 * v if i != j else 0.3).move_to([j * cell, -i * cell, 0])
                t = label(rf"{100 * v:.0f}\%" if i != j else r"--", font_size=20,
                          color=WHITE if i != j else GREY_C).move_to(sq)
                grid.add(VGroup(sq, t))
        rows = VGroup(*[label(n, font_size=18, color=c).move_to([-1.2, -i * cell, 0]) for i, (n, c) in
                        enumerate(zip(names, cols))])
        colh = VGroup(*[label(n, font_size=18, color=c).move_to([j * cell, cell * 0.8, 0]) for j, (n, c) in
                        enumerate(zip(names, cols))])
        VGroup(grid, rows, colh).move_to(LEFT * 2.6 + DOWN * 0.3)
        rl = label(r"price rises here \ $\downarrow$", font_size=15, color=GREY_B).next_to(rows, UP, buff=0.35)
        cl = label(r"lost sales go here \ $\to$", font_size=15, color=GREY_B).next_to(colh, UP, buff=0.12)
        side = VGroup(
            MathTex(r"D_{jk} = \frac{\partial q_k / \partial p_j}{-\,\partial q_j / \partial p_j}", font_size=36,
                    color=WHITE),
            label(r"the share of $j$'s lost sales that go to $k$", font_size=20, color=GREY_A),
            label(rf"Alder $\to$ Birch: \ {100 * D[0, 1]:.0f}\%; \ Birch $\to$ Alder: \ {100 * D[1, 0]:.0f}\%",
                  font_size=21, color=BIRCH),
            label(rf"Alder $\to$ the shops: \ only {100 * D[0, 3]:.0f}\%", font_size=21, color=SHOPS),
            label(r"from a demand system, \ customer surveys, \\ or the firms' own win-loss records", font_size=19,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.5)
        tag = island_tag(r"the Island: \ a town with all three chains; \ diversion from the nested logit",
                         corner=DL, font_size=12)
        with self.voiceover(
            "Concentration is a proxy. The direct question is what the merged firm will want to do with its prices, "
            "and the key number is the diversion ratio. <bookmark mark='a'/> When product j's price rises, it loses "
            "sales; the diversion ratio to k is the share of those lost sales that k picks up. <bookmark mark='b'/> "
            f"In this Island town, {100 * D[0, 1]:.0f} percent of the customers Alder loses go to Birch, and "
            f"{100 * D[1, 0]:.0f} percent of Birch's go to Alder. <bookmark mark='c'/> Only {100 * D[0, 3]:.0f} "
            "percent go to the corner shops. <bookmark mark='d'/> Agencies estimate diversion from a demand system "
            "when they have one, but also from customer surveys, and from the firms' own records of which rival "
            "they lose sales to, which firms keep for their own purposes and must hand over."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows), FadeIn(colh), FadeIn(rl), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.05), run_time=1.6)
            vo.wait_until("b")
            self.play(Indicate(grid[1], color=WHITE), Indicate(grid[4], color=WHITE), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Indicate(grid[3], color=WHITE), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def derive(self):
        rows = VGroup(
            label(r"before: \ Alder sets its price alone", font_size=22, color=ALDER),
            MathTex(r"q_A + (p_A - c_A)\,\frac{\partial q_A}{\partial p_A} = 0", font_size=34, color=WHITE),
            label(r"after: \ it also counts the sales that go to Birch", font_size=22, color=BIRCH),
            MathTex(r"q_A + (p_A - c_A)\,\frac{\partial q_A}{\partial p_A} + (p_B - c_B)\,"
                    r"\frac{\partial q_B}{\partial p_A} = 0", font_size=34, color=WHITE),
            MathTex(r"\Longleftrightarrow\quad q_A + \big(p_A - [\,c_A + \underbrace{D_{AB}\,(p_B - c_B)}_{"
                    r"\text{an opportunity cost}}\,]\big)\frac{\partial q_A}{\partial p_A} = 0", font_size=34,
                    color=E.ACCENT),
            MathTex(r"\text{UPP}_A = D_{AB}\,(p_B - c_B) - E_A\,c_A \qquad \text{GUPPI}_A = "
                    r"\frac{D_{AB}\,(p_B - c_B)}{p_A}", font_size=32, color=GOV),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 0.1)
        tag = published_tag(r"Farrell and Shapiro (2010); \ the Horizontal Merger Guidelines (2010), \S 6.1",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Why does the merged firm raise prices, with no agreement with anyone? Part forty-three gave the "
            "formula; here is where it comes from. <bookmark mark='a'/> Before the merger Alder sets its price "
            "where the profit from one more dollar on every sale just balances the margin lost on customers who "
            "leave. <bookmark mark='b'/> After it, some of the customers who leave Alder go to Birch, and Birch's "
            "margin on them now belongs to the same owner. One extra term. <bookmark mark='c'/> Rearranged, the "
            "extra term acts exactly like a rise in Alder's marginal cost: every sale Alder makes now costs it the "
            "Birch sale it might have diverted, worth the diversion ratio times Birch's margin. A higher cost means "
            "a higher price. <bookmark mark='d'/> Joseph Farrell and Carl Shapiro called this upward pricing "
            "pressure, net of any cost saving from the merger, and its share of the price, the gross upward pricing "
            "pressure index, entered the 2010 guidelines as the value of diverted sales. It needs no market "
            "definition at all: only a diversion ratio and a margin."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Write(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), Write(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4], shift=DOWN * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(rows[5], shift=DOWN * 0.1))
        self.clear_scene()

    def numbers(self):
        U = load("upp")
        P = U["products"]
        sim = U["simulation"]
        cm = U["cmcr"]
        ax = plane([-0.5, 2.5], [0, 18], center=LEFT * 2.8 + DOWN * 0.4, x_length=6.4, y_length=4.6, xticks=[],
                   yticks=[0, 5, 10, 15], ylabel=r"percent of the price", yfmt=lambda v: f"{v:.0f}", font_size=15)
        groups = [(r"GUPPI", [100 * P["Alder"]["guppi"], 100 * P["Birch"]["guppi"]], GOV),
                  (r"simulated \\ price rise", [100 * sim["dp"][0], 100 * sim["dp"][1]], SIM),
                  (r"cost cut that \\ would offset it", [100 * cm[0], 100 * cm[1]], SAVE)]
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        for k, (t, v, col) in enumerate(groups):
            for j, vv in enumerate(v):
                x = k + (j - 0.5) * 0.36
                p0, p1 = ax.ax.c2p(x - 0.16, 0), ax.ax.c2p(x + 0.16, vv)
                b = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col,
                              fill_opacity=0.9 if j == 0 else 0.55, stroke_width=0).move_to((p0 + p1) / 2)
                bars.add(b)
                vals.add(label(f"{vv:.1f}", font_size=15, color=col).next_to(b, UP, buff=0.05))
            labs.add(label(t, font_size=15, color=col).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.15))
        key = label(r"solid: \ Alder; \ pale: \ Birch", font_size=15, color=GREY_A).next_to(ax.ax.c2p(-0.4, 18),
                                                                                            RIGHT, buff=0.0)
        side = VGroup(
            label(rf"Alder's GUPPI: \ {100 * P['Alder']['diversion']:.0f}\% $\times$ "
                  rf"\${P['Alder']['partner_margin']:.2f} $\div$ \${U['prices'][0]:.2f} $=$ "
                  rf"{100 * P['Alder']['guppi']:.1f}\%", font_size=20, color=GOV),
            label(rf"the full simulation: \ Alder +{100 * sim['dp'][0]:.1f}\%, \ Birch +{100 * sim['dp'][1]:.1f}\%,"
                  rf" \ Cedar +{100 * sim['dp'][2]:.1f}\%", font_size=20, color=SIM),
            label(r"the rivals follow a little: \ their competitors are dearer", font_size=18, color=GREY_B),
            label(rf"savings of {100 * cm[0]:.0f}--{100 * cm[1]:.0f}\% of marginal cost would hold prices",
                  font_size=20, color=SAVE),
            label(r"a screen, \ not a verdict: \ a GUPPI under about 5\% \\ is often treated as a weak case",
                  font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ the town with all three chains", corner=DL, font_size=12)
        with self.voiceover(
            f"Now the Island's numbers. <bookmark mark='a'/> Alder's GUPPI: {100 * P['Alder']['diversion']:.0f} "
            f"percent diversion, times Birch's margin of {P['Alder']['partner_margin']:.2f} dollars, over Alder's "
            f"price: {say_pct(P['Alder']['guppi'], 1)}. Birch's is {say_pct(P['Birch']['guppi'], 1)}. <bookmark "
            "mark='b'/> The full simulation of Part forty-three, which lets every price adjust, puts Alder's rise "
            f"at {say_pct(sim['dp'][0], 1)} and Birch's at {say_pct(sim['dp'][1], 1)}. <bookmark mark='c'/> Cedar's "
            f"price rises too, by {say_pct(sim['dp'][2], 1)}: no collusion, just dearer competitors. <bookmark "
            "mark='d'/> And to hold prices where they are, the merger would have to cut the two chains' marginal "
            f"costs by {100 * cm[0]:.0f} to {100 * cm[1]:.0f} percent, which is a great deal for a shop. <bookmark "
            "mark='e'/> In practice the GUPPI is a screen. A value below about five percent is often treated as a "
            "weak case; where it is high, the agencies reach for the full model, and the model is where the arguments "
            "start."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(labs), FadeIn(key))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), GrowFromEdge(bars[1], DOWN), FadeIn(vals[0]), FadeIn(vals[1]),
                      FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[2], DOWN), GrowFromEdge(bars[3], DOWN), FadeIn(vals[2]), FadeIn(vals[3]),
                      FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[4], DOWN), GrowFromEdge(bars[5], DOWN), FadeIn(vals[4]), FadeIn(vals[5]),
                      FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
