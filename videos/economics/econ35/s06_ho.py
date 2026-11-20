from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403

MACH = "#7EC8F5"   # machines


class HO(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Factor proportions", r"Does what a country has decide what it sells?",
             "Chapter five. Factor proportions.", lit={1919: r"Heckscher", 1933: r"Ohlin", 1948: r"Lerner"},
             scale=("nation", "world"), horizon=("a decade",))
        self.idea()
        self.lerner()
        self.trade()
        self.theorems()

    def idea(self):
        H = load("ho")
        rows = VGroup(
            label(r"same technology everywhere; \ different endowments", font_size=28, color=E.ACCENT),
            label(rf"the Island: \ {H['island']['L']:.0f} workers, \ {H['island']['K']:.0f} units of capital",
                  font_size=24, color=ISLAND),
            label(rf"the Archipelago: \ {H['arch']['L']:.0f} workers, \ {H['arch']['K']:.0f} units of capital",
                  font_size=24, color=ARCH),
            label(rf"cloth uses labour intensively \ (labour's share {H['alphas'][0]:.1f}); \ machines use capital "
                  rf"\ ({1 - H['alphas'][1]:.1f})", font_size=23, color=CLOTH),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.2)
        tag = island_tag(corner=DR, font_size=14)
        two = VGroup(label(r"Ricardo: \ technologies differ", font_size=24, color=WINE),
                     label(r"Heckscher and Ohlin: \ endowments differ", font_size=24, color=CAPITAL)).arrange(
            RIGHT, buff=1.2).to_edge(UP, buff=0.5)
        rows.next_to(two, DOWN, buff=0.7)
        with self.voiceover(
            "Ricardo explains trade by differences in technology. In 1919 the Swedish economist Eli Heckscher, and "
            "in 1933 his student Bertil Ohlin, offered a second reason, which needs no difference in technology at "
            "all. <bookmark mark='a'/> Give every country the same ways of making things, and let them differ only "
            "in what they have. <bookmark mark='b'/> The Island has many workers and little capital; "
            "<bookmark mark='c'/> the Archipelago has fewer workers and much more capital. <bookmark mark='d'/> "
            "And the two goods use them in different proportions: weaving cloth takes mostly labour, building "
            "machines mostly capital."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(two[0]))
            self.wait(2.0)
            self.play(FadeIn(two[1]))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def lerner(self):
        H = load("ho")
        I1, I2 = H["iso"]["good1"], H["iso"]["good2"]
        ax = plane([0, 3.2], [0, 3.2], center=LEFT * 2.0 + DOWN * 0.3, x_length=5.0, y_length=5.0,
                   xticks=[0, 1, 2, 3], yticks=[0, 1, 2, 3], xlabel=r"labour", ylabel=r"capital",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        q1 = path(ax, I1["L"], I1["K"], CLOTH, 3.2, xr=(0, 3.2), yr=(0, 3.2))
        q2 = path(ax, I2["L"], I2["K"], MACH, 3.2, xr=(0, 3.2), yr=(0, 3.2))
        cost = seg(ax, H["isocost"]["L0"], 0, 0, H["isocost"]["K0"], WHITE, 2.5)
        s1 = dot(ax, *I1["star"], CLOTH, 0.08)
        s2 = dot(ax, *I2["star"], MACH, 0.08)
        r1 = seg(ax, 0, 0, I1["star"][0] * 2.2, I1["star"][1] * 2.2, CLOTH, 1.5, dashed=True)
        r2 = seg(ax, 0, 0, min(I2["star"][0] * 1.6, 3.2), min(I2["star"][1] * 1.6, 3.2), MACH, 1.5, dashed=True)
        side = VGroup(
            label(r"pink: \ a dollar's worth of cloth", font_size=19, color=CLOTH),
            label(r"blue: \ a dollar's worth of machines", font_size=19, color=MACH),
            label(r"white: \ the inputs a dollar buys \\ at wage $w$ and rent $r$", font_size=19, color=WHITE),
            label(rf"tangent to both: \ $w$ = {H['w']:.2f}, \ $r$ = {H['r']:.2f} \\ the prices of goods fix \\ the "
                  r"prices of factors", font_size=19, color=GAIN),
            label(r"the dashed rays: \ the cone \\ in which a country \\ makes both goods", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        tag = published_tag(r"Lerner (1952, written 1933); \ the Island's technologies", corner=DR, font_size=12)
        with self.voiceover(
            "The model has a picture, drawn by Abba Lerner as a student in 1933. <bookmark mark='a'/> The pink "
            "curve is every mix of labour and capital that makes one dollar's worth of cloth at world prices. "
            "<bookmark mark='b'/> The blue curve, one dollar's worth of machines: it lies up and to the left, "
            "because machines need more capital. <bookmark mark='c'/> If both are made, each must cost exactly a "
            "dollar to make, so a single line of inputs costing one dollar must touch both curves. "
            "<bookmark mark='d'/> That line fixes the wage and the rent. The prices of goods determine the prices "
            "of the factors, whatever a country's endowments, which is the first surprising result. "
            "<bookmark mark='e'/> The two dashed rays are the proportions each good uses; a country with "
            "endowments between them makes both goods."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(q1), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(q2), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(cost), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(s1, scale=1.5), FadeIn(s2, scale=1.5), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(r1), Create(r2), FadeIn(side[4]))
        self.clear_scene()

    def trade(self):
        H = load("ho")
        I, A = H["island"], H["arch"]
        ax = plane([0, 2.6], [0, 2.6], center=LEFT * 3.0 + DOWN * 0.4, x_length=4.6, y_length=4.4,
                   xticks=[0, 1, 2], yticks=[0, 1, 2], xlabel=r"", ylabel=r"price of machines, \ in cloth",
                   xfmt=lambda v: "", yfmt=lambda v: f"{v:.1f}", font_size=14)

        def bar(x, v, col):
            p0, p1 = ax.ax.c2p(x - 0.25, 0), ax.ax.c2p(x + 0.25, v)
            return Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=0.85,
                             stroke_width=0).move_to((p0 + p1) / 2)

        bI, bA = bar(0.6, I["aut_p"], ISLAND), bar(2.0, A["aut_p"], ARCH)
        world = seg(ax, 0, H["p"], 2.6, H["p"], WHITE, 2.5, dashed=True)
        nms = VGroup(label(r"the Island, \\ alone", font_size=16, color=ISLAND).next_to(ax.ax.c2p(0.6, 0), DOWN, 0.1),
                     label(r"the Archipelago, \\ alone", font_size=16, color=ARCH).next_to(ax.ax.c2p(2.0, 0), DOWN,
                                                                                      0.1))
        wl = label(rf"with trade: \ {H['p']:.2f}", font_size=17, color=WHITE).next_to(ax.ax.c2p(2.6, H["p"]), UP,
                                                                                     buff=0.06).shift(LEFT * 0.9)
        side = VGroup(
            label(rf"alone, \ machines cost the Island {I['aut_p']:.2f} cloth, \ the Archipelago {A['aut_p']:.2f}",
                  font_size=20, color=WHITE),
            label(rf"with trade, \ the Island sells {I['X'][0]:.0f} cloth \ and buys {-I['X'][1]:.0f} machines",
                  font_size=20, color=ISLAND),
            label(r"each exports the good that uses \\ its abundant factor intensively", font_size=21, color=GAIN),
            label(rf"the wage and the rent end up the same in both: \\ $w$ = {H['w']:.2f}, \ $r$ = {H['r']:.2f}, "
                  rf"\ against {I['aut_w']:.2f} and {I['aut_r']:.2f} \\ on the Island alone", font_size=19,
                  color=CAPITAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now let the two trade. <bookmark mark='a'/> Alone, the Island, short of capital, finds machines dear: "
            f"{I['aut_p']:.2f} bolts of cloth each. The Archipelago, rich in capital, pays {A['aut_p']:.2f}. "
            f"<bookmark mark='b'/> With trade one price settles between them, {H['p']:.2f}, and the Island sells "
            f"{I['X'][0]:.0f} bolts of cloth for {-I['X'][1]:.0f} machines. <bookmark mark='c'/> That is the "
            "Heckscher-Ohlin theorem: a country exports the good that uses its abundant factor intensively. "
            "<bookmark mark='d'/> And something stranger happens. Labour on the Island, cheap before trade, gets "
            "dearer; capital gets cheaper; and the wage and the rent end up exactly the same in both places, though "
            "not one worker or machine has crossed the sea. Trading goods is a way of trading the labour and "
            "capital inside them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(bI, DOWN), GrowFromEdge(bA, DOWN), FadeIn(nms), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(world), FadeIn(wl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def theorems(self):
        H = load("ho")
        R = H["rybczynski"]["dQ"]
        S = load("stolper")
        cards = point_cards([
            (r"Heckscher-Ohlin", r"a country exports \\ the good that uses \\ its abundant factor", ISLAND),
            (r"factor price equalization", r"free trade in goods \\ equalizes wages \\ and rents", CAPITAL),
            (r"Stolper-Samuelson", rf"cloth +10\%: \\ wage {100 * S['dw']:+.0f}\%, \\ rent {100 * S['dr']:+.0f}\%",
             CLOTH),
            (r"Rybczynski", rf"the Archipelago's capital +10\%: \\ machines {100 * R[1]:+.0f}\%, \\ cloth "
                            rf"{100 * R[0]:+.0f}\%", MACH),
        ], width=12.8, cols=4, font_size=20).move_to(DOWN * 0.1)
        head = label(r"four theorems from one picture", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Four theorems come out of this picture. <bookmark mark='a'/> Heckscher and Ohlin's, about the pattern "
            "of trade. <bookmark mark='b'/> Factor price equalization, the one we just saw. <bookmark mark='c'/> "
            "Stolper and Samuelson's, about who gains, which is the next chapter. <bookmark mark='d'/> And "
            "Rybczynski's: at fixed prices, more capital raises the output of machines by more than its own growth "
            f"and lowers the output of cloth. Give the Archipelago ten percent more capital and it makes "
            f"{100 * R[1]:.0f} percent more machines and {abs(100 * R[0]):.0f} percent less cloth. Growth can make an "
            "economy more specialized, not less."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
