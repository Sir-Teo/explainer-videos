from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403


class Monopoly(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Marginal revenue and the monopoly price", r"Why does a seller who sets the price sell less than a "
             r"competitive market would?", "Chapter two. Marginal revenue and the monopoly price.",
             lit={1933: r"Robinson's \emph{Imperfect Competition}"})
        self.mr()
        self.optimum()
        self.lerner()

    def axes(self, m):
        return plane([0, 100], [-10, 10], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.4, y_length=5.2,
                     xticks=[0, 25, 50, 75, 100], yticks=[-10, -5, 0, 5, 10], xlabel=r"crossings a day",
                     ylabel=r"\$ a crossing", font_size=17)

    def mr(self):
        m = load("monopoly")
        ax = self.axes(m)
        a = ax.ax
        dem = path(ax, m["qs"], m["p_of_q"], color=DEM, width=3.5, smooth=False)
        mrc = path(ax, m["qs"], m["mr"], color=MR, width=3.5, smooth=False)
        q0, dq = 40, 5                       # drawn for five more crossings, so that the strips can be seen
        p0 = float(np.interp(q0, m["qs"], m["p_of_q"]))
        p1 = float(np.interp(q0 + dq, m["qs"], m["p_of_q"]))
        gain = Rectangle(width=a.c2p(q0 + dq, 0)[0] - a.c2p(q0, 0)[0], height=a.c2p(0, p1)[1] - a.c2p(0, 0)[1],
                         stroke_width=0, fill_color=CS, fill_opacity=0.8).move_to(a.c2p(q0, 0), aligned_edge=DL)
        loss = Rectangle(width=a.c2p(q0, 0)[0] - a.c2p(0, 0)[0], height=a.c2p(0, p0)[1] - a.c2p(0, p1)[1],
                         stroke_width=0, fill_color=DWL, fill_opacity=0.8).move_to(a.c2p(0, p1), aligned_edge=DL)
        side = VGroup(
            label(r"demand: \ $Q = 100 - 10p$, \ so $p = 10 - Q/10$", font_size=23, color=DEM),
            label(r"to sell one more crossing, \ Bo must cut the fare for everyone", font_size=22),
            label(r"he gains the new passengers' fares (green) \\ and loses the cut on all the others (red)",
                  font_size=22, color=GREY_A),
            label(r"(drawn for five more crossings, \ so that the strips show)", font_size=18, color=GREY_B),
            label(r"marginal revenue: \ $MR = 10 - Q/5$, \\ below the demand curve, \ twice as steep", font_size=23,
                  color=MR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.45)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Smooth out the hundred islanders into a demand curve: at a fare of p dollars, a hundred minus ten p "
            "crossings a day. <bookmark mark='a'/> What does one more crossing earn Bo? To sell it, he has to lower "
            "the fare, and not just for the new passenger: for everyone. <bookmark mark='b'/> So he gains the new "
            "passenger's fare, the green strip, and loses the price cut on all the passengers he had already, the "
            "red one. <bookmark mark='c'/> What's left is marginal revenue. For a straight-line demand curve it is "
            "a straight line too, starting at the same place and falling twice as fast. Past fifty crossings it is "
            "negative: selling more would bring in less."
        ) as vo:
            self.play(FadeIn(ax), Create(dem), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(gain), FadeIn(loss), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Create(mrc), FadeIn(side[4]))
        self.clear_scene()

    def optimum(self):
        m = load("monopoly")
        ax = self.axes(m)
        a = ax.ax
        dem = path(ax, m["qs"], m["p_of_q"], color=DEM, width=3.5, smooth=False)
        mrc = path(ax, m["qs"], m["mr"], color=MR, width=3.5, smooth=False)
        mc = DashedLine(a.c2p(0, 0), a.c2p(100, 0), color=MC, stroke_width=2)
        Q = Dot(a.c2p(m["q"], 0), radius=0.08, color=MR)
        P = Dot(a.c2p(m["q"], m["p"]), radius=0.09, color=PROFIT)
        drop = DashedLine(a.c2p(m["q"], 0), a.c2p(m["q"], m["p"]), color=GREY_B, stroke_width=1.5)
        prof = region(ax, [(0, 0), (m["q"], 0), (m["q"], m["p"]), (0, m["p"])], PROFIT, 0.25)
        mc2 = DashedLine(a.c2p(0, m["c2"]), a.c2p(100, m["c2"]), color=GREY_B, stroke_width=1.5)
        w = m["with_cost"]
        P2 = Dot(a.c2p(w["q"], w["p"]), radius=0.08, color=GREY_A)
        side = VGroup(
            label(r"profit is greatest where \ $MR = MC$", font_size=24, color=MR),
            label(rf"here $MC = 0$: \ {m['q']:.0f} crossings, \ fare \${m['p']:.0f}, \ takings \${m['profit']:.0f}",
                  font_size=22, color=PROFIT),
            label(r"a competitive market would carry 100: \ price = marginal cost", font_size=22, color=GREY_A),
            label(rf"if a crossing cost \${m['c2']:.0f}: \ {w['q']:.0f} crossings at \${w['p']:.0f}", font_size=22),
            label(r"no supply curve: \ the price depends on the shape of demand, \\ not only on cost", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "So Bo carries passengers as long as the next one adds more to revenue than to cost. "
            "<bookmark mark='a'/> The best number is where marginal revenue equals marginal cost. "
            "<bookmark mark='b'/> Here a crossing costs nothing, so it is where marginal revenue is zero: fifty "
            "crossings, at a fare of five dollars, for takings of two hundred and fifty dollars a day. "
            "<bookmark mark='c'/> A competitive market, pricing at cost, would carry a hundred. "
            "<bookmark mark='d'/> If each crossing cost Bo two dollars in fuel, he would carry forty, at six "
            "dollars: the fare rises by only half the cost. <bookmark mark='e'/> And notice that a monopolist has no "
            "supply curve. Its price depends on the whole shape of demand, not just on its costs, which is why the "
            "competitive theory of Part eight doesn't carry over."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(dem), FadeIn(mrc), Create(mc))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(Q))
            vo.wait_until("b")
            self.play(Create(drop), FadeIn(P), FadeIn(prof), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(mc2), FadeIn(P2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def lerner(self):
        m = load("monopoly")
        w = m["with_cost"]
        rows = VGroup(
            MathTex(r"MR = p\left(1 + \frac{1}{\varepsilon}\right) = MC", font_size=42, color=MR),
            MathTex(r"\frac{p - MC}{p} = -\frac{1}{\varepsilon}", font_size=46, color=PROFIT),
            label(r"the Lerner index: \ the share of the price that is markup", font_size=26),
            label(rf"Bo with a \${m['c2']:.0f} cost: \ $(6 - 2)/6 = {w['lerner']:.2f}$, \ and demand's elasticity at "
                  rf"\$6 is $-1.5$", font_size=25, color=GREY_A),
            label(r"the less elastic the demand, \ the larger the markup; \\ a monopolist never prices where demand "
                  r"is inelastic", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38)
        hc = history_card(1934, r"Abba Lerner", r"``The Concept of Monopoly and the Measurement of Monopoly Power''",
                          color=PROFIT, width=9.0, font_size=22)
        VGroup(hc, rows).arrange(DOWN, buff=0.4)
        tag = published_tag(r"Lerner, Review of Economic Studies 1(3) (1934)", corner=DR, font_size=14)
        with self.voiceover(
            "There's a neat way to write the rule. <bookmark mark='a'/> Marginal revenue is the price times one plus "
            "one over the elasticity of demand. Setting it equal to marginal cost and rearranging, "
            "<bookmark mark='b'/> the markup, as a share of the price, is minus one over the elasticity. Abba "
            "Lerner proposed it in 1934 as the measure of monopoly power: the Lerner index. "
            "<bookmark mark='c'/> For Bo with a two-dollar cost, the markup is four dollars on a six-dollar fare, "
            "two thirds, and demand's elasticity at six dollars is minus one and a half. Two thirds is one over one "
            "and a half. <bookmark mark='d'/> So the less elastic the demand, the bigger the markup. And a "
            "monopolist never sets a price where demand is inelastic: there, a higher price would raise revenue "
            "and lower cost."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
