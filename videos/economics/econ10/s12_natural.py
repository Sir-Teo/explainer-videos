from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403

HOUSE = "#7EC8F5"
YARD = "#F2A65A"


class Natural(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Natural monopoly and Ramsey prices", r"When one firm is cheapest, who should pay for its fixed "
             r"costs?", "Chapter ten. Natural monopoly and Ramsey prices.", lit={1956: r"Boiteux's prices"},
             scale=("firm", "market", "nation"))
        self.natural()
        self.ramsey()

    def natural(self):
        ax = plane([0, 120], [0, 10], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.4, y_length=5.0,
                   xticks=[0, 40, 80, 120], yticks=[0, 2, 4, 6, 8, 10], xlabel=r"water delivered",
                   ylabel=r"\$ a unit", font_size=17)
        a = ax.ax
        qs = np.linspace(4, 120, 200)
        F, c = 200.0, 1.0
        ac = path(ax, qs, F / qs + c, color=MR, width=3.5, yr=(0, 10))
        mc = DashedLine(a.c2p(0, c), a.c2p(120, c), color=MC, stroke_width=2)
        dq = np.linspace(0, 118.75, 100)
        dem = path(ax, dq, 9.5 - 0.08 * dq, color=DEM, width=3)
        # average-cost price: where 9.5 - 0.08 q = 200 / q + 1
        q_ac = max(np.roots([-0.08, 8.5, -200.0]).real)
        p_ac = 9.5 - 0.08 * q_ac
        q_mc = (9.5 - c) / 0.08
        names = VGroup(label(r"average cost", font_size=17, color=MR).next_to(a.c2p(110, 2.82), UP, buff=0.3),
                       label(r"demand", font_size=17, color=DEM).next_to(a.c2p(14, 7.9), DL, buff=0.1),
                       label(r"marginal cost, \ \$1", font_size=17, color=MC).next_to(a.c2p(60, 1), UP, buff=0.06))
        A = Dot(a.c2p(q_ac, p_ac), radius=0.09, color=MR)
        M = Dot(a.c2p(q_mc, c), radius=0.09, color=MC)
        side = VGroup(
            label(r"the Island's waterworks: \ one set of pipes, \ \$200 a day, \\ plus \$1 a unit of water",
                  font_size=22),
            label(r"average cost falls with volume: \ one firm is cheapest", font_size=22, color=MR),
            label(r"price at marginal cost, \ \$1: \ efficient, \ but the pipes go unpaid", font_size=22, color=MC),
            label(rf"price at average cost: \ \${p_ac:.2f}, \ the firm breaks even, \\ but some water worth more "
                  r"than \$1 is not used", font_size=22, color=MR),
            label(r"who pays for the pipes, \ and how?", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = illustrative_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Some markets are monopolies because one firm is simply cheapest. <bookmark mark='a'/> The Island's "
            "waterworks has one set of pipes, which costs two hundred dollars a day whatever flows through it, and a "
            "dollar for each unit of water. <bookmark mark='b'/> Average cost falls the more water it delivers, so "
            "two sets of pipes would be a waste: a natural monopoly. <bookmark mark='c'/> Pricing water at its "
            "marginal cost, a dollar, would be efficient, but then nothing pays for the pipes. "
            "<bookmark mark='d'/> Pricing at average cost lets the firm break even, but turns away water that is "
            "worth more than it costs. <bookmark mark='e'/> So the real question is who pays for the pipes, and how."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ac), Create(dem), FadeIn(names[0]), FadeIn(names[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(mc), FadeIn(names[2]), FadeIn(M), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(A), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def ramsey(self):
        r = load("ramsey")
        m1, m2 = r["markups"]
        bars = VGroup()
        for k, (name, col, rm, u) in enumerate(((r"households \ ($\varepsilon = 1.5$)", HOUSE, m1, r["uniform_markup"]),
                                                (r"boatyards \ ($\varepsilon = 4$)", YARD, m2, r["uniform_markup"]))):
            unif = 1 - 1 / u
            g = VGroup(label(name, font_size=22, color=col),
                       Rectangle(width=4.5 * rm, height=0.4, stroke_width=0, fill_color=col, fill_opacity=0.85),
                       label(rf"Ramsey: \ {100 * rm:.0f}\% of the price", font_size=20, color=col),
                       Rectangle(width=4.5 * unif, height=0.4, stroke_color=GREY_B, stroke_width=1.5,
                                 fill_opacity=0),
                       label(rf"uniform: \ {100 * unif:.0f}\%", font_size=20, color=GREY_A))
            bars.add(g)
        for g in bars:
            g[1].next_to(g[0], DOWN, buff=0.15, aligned_edge=LEFT)
            g[2].next_to(g[1], RIGHT, buff=0.2)
            g[3].next_to(g[1], DOWN, buff=0.12, aligned_edge=LEFT)
            g[4].next_to(g[3], RIGHT, buff=0.2)
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(LEFT, buff=0.7).shift(UP * 0.6)
        side = VGroup(
            label(rf"two groups, \ marginal cost \${r['c'][0]:.0f}, \\ and a fixed cost of \${r['F']:.0f} a day to "
                  r"cover", font_size=22),
            MathTex(r"\frac{p_i - c_i}{p_i} = \frac{k}{\varepsilon_i}", font_size=42, color=E.ACCENT),
            label(r"markups in inverse proportion to elasticity, \\ just high enough to cover the pipes", font_size=22),
            label(rf"surplus lost: \ \${r['loss_ramsey']:.1f} a day with Ramsey prices, \\ \${r['loss_uniform']:.1f} with "
                  r"one uniform markup", font_size=22, color=CS),
            label(r"Ramsey (1927) for taxes; \ Boiteux (1956) for \'Electricit\'e de France", font_size=20,
                  color=GREY_B),
            label(r"efficient, \ but it charges most to those who can least do without", font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Suppose the waterworks sells to two groups: households, who need water whatever it costs, with an "
            "elasticity of one and a half, and boatyards, who can recycle or drill their own well, with an "
            "elasticity of four. Its fixed cost of forty must be covered. <bookmark mark='a'/> The prices that cover "
            "it with the least loss of surplus put markups in inverse proportion to elasticity. "
            "<bookmark mark='b'/> Households pay a markup of forty percent of the price, boatyards fifteen. "
            "<bookmark mark='c'/> The surplus lost is seventeen and a half a day, against thirty-three with one "
            "markup for both. <bookmark mark='d'/> Frank Ramsey derived the rule for taxes in 1927, and Marcel "
            "Boiteux for the prices of France's state electricity company in 1956. <bookmark mark='e'/> It is "
            "efficient, but it charges the most to the customers who can least do without, and that is a political "
            "choice as much as an economic one."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(bars[0][0]), FadeIn(bars[1][0]), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Write(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(g[1], LEFT) for g in bars], *[FadeIn(g[2]) for g in bars],
                      *[FadeIn(g[3]) for g in bars], *[FadeIn(g[4]) for g in bars])
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        self.clear_scene()
