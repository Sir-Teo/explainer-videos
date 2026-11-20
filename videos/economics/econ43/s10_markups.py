from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class Markups(VoiceoverScene):
    def construct(self):
        card(self, 8, r"From elasticities to markups: \ Nevo's cereals", r"Is it collusion, or many brands?",
             "Chapter eight. From elasticities to markups: Nevo's cereals.", lit={2001: r"Nevo"},
             scale=("firm", "market"), horizon=("a year",))
        self.lerner()
        self.aisle()
        self.test()
        self.caveats()

    def lerner(self):
        lines = VGroup(
            MathTex(r"\frac{p - c}{p} \;=\; \frac{1}{|\varepsilon|}", font_size=46),
            MathTex(r"s_j(p) \;+\; \sum_{k \,\in\, F_f} (p_k - c_k)\,\frac{\partial s_k}{\partial p_j} \;=\; 0",
                    font_size=40),
            MathTex(r"p - c \;=\; -\big(\Omega \circ \tfrac{\partial s}{\partial p}'\big)^{-1} s", font_size=44,
                    color=E.ACCENT),
        ).arrange(DOWN, buff=0.85).move_to(UP * 0.7)
        notes = VGroup(
            label(r"one product: \ Lerner's rule \ (Part 10)", font_size=19, color=GREY_A),
            label(r"a firm $f$ owning several products prices each with an eye on the others", font_size=19,
                  color=GREY_A),
            label(r"$\Omega$: \ who owns what. \ Demand and ownership give markups, \ with no costs in sight",
                  font_size=20, color=E.ACCENT),
        )
        notes[0].next_to(lines[0], RIGHT, buff=0.5)
        notes[1].next_to(lines[1], DOWN, buff=0.15)
        notes[2].next_to(lines[2], DOWN, buff=0.2)
        tag = published_tag(tables.NEVO_2001.tag, corner=DR, font_size=11)
        with self.voiceover(
            "With demand in hand, markups follow. <bookmark mark='a'/> A firm selling one product sets its margin, "
            "as a share of price, at one over the elasticity of its demand: Lerner's rule from Part ten. "
            "<bookmark mark='b'/> A firm selling several products prices each one knowing that a higher price sends "
            "some shoppers to its other brands, which it does not mind. Its first-order conditions add those "
            "diverted profits. <bookmark mark='c'/> Stack the conditions for every product, with a matrix omega "
            "that records who owns what, and solve. The markups come out of demand and ownership alone. Costs are "
            "never observed; they are what is left: price minus markup."
        ) as vo:
            self.play(Write(lines[0]), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(lines[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Write(lines[2]), FadeIn(notes[2]))
        self.clear_scene()

    def aisle(self):
        R = load("cereal")
        own = np.array(R["owner"])
        J = len(own)
        A = R["implied"]
        ax = plane([0, J], [0, 1.0], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[], yticks=[0, 0.25, 0.5, 0.75, 1.0], ylabel=r"margin, \ $(p - c)/p$",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        groups = {}
        for key, col, off in (("single", DEMAND, -0.27), ("actual", PRICE, 0.0), ("joint", LOSS, 0.27)):
            g = VGroup()
            for j in range(J):
                v = A[key][j]
                p0 = ax.ax.c2p(j + 0.5 + off, 0)
                p1 = ax.ax.c2p(j + 0.5 + off, min(v, 1.0))
                g.add(Rectangle(width=0.15, height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=col,
                                fill_opacity=0.9).move_to((p0 + p1) / 2))
            groups[key] = g
        firm_marks = VGroup()
        for f in range(4):
            idx = np.where(own == f)[0]
            a, b = ax.ax.c2p(idx.min() + 0.08, -0.04), ax.ax.c2p(idx.max() + 0.92, -0.04)
            firm_marks.add(Line(a, b, color=FIRM[f], stroke_width=6))
        av = R["avg"]
        side = VGroup(
            label(r"the Island's aisle: \\ 12 brands, \ 4 firms \\ (coloured underneath)", font_size=18, color=WHITE),
            label(rf"blue: \ each brand \\ its own firm: \ {100 * av['single']:.0f}\%", font_size=18, color=DEMAND),
            label(rf"gold: \ the real owners: \\ {100 * av['actual']:.0f}\%", font_size=18, color=PRICE),
            label(rf"red: \ one owner, \\ a cartel: \ {100 * av['joint']:.0f}\%", font_size=18, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Nevo's test turns this around. Take observed prices and estimated demand, and ask what margins each "
            "theory of conduct implies. <bookmark mark='a'/> Here is the Island's cereal aisle: twelve brands from "
            "four firms, with demand known. <bookmark mark='b'/> If every brand were priced by its own firm, the "
            f"margins that would make today's prices optimal average {say_pct(av['single'], 0)}: that much comes from "
            "differentiation alone. <bookmark mark='c'/> With the real owners, each firm pricing its portfolio, they "
            f"average {say_pct(av['actual'], 0)}. <bookmark mark='d'/> And if all four firms acted as one, a "
            f"cartel, today's prices would imply margins of {say_pct(av['joint'], 0)}: a cartel would charge far more "
            "than this, so prices this low are hard to square with collusion."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(firm_marks), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in groups["single"]], lag_ratio=0.05),
                      FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in groups["actual"]], lag_ratio=0.05),
                      FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in groups["joint"]], lag_ratio=0.05),
                      FadeIn(side[3]), run_time=1.5)
        self.clear_scene()

    def test(self):
        R = load("cereal")
        av = R["avg"]
        drops = (0.2, 0.75, 0.2)
        parts = [(r"differentiation", av["single"], DEMAND), (r"the portfolio", av["actual"] - av["single"], PRICE),
                 (r"what a cartel \\ would add", av["joint"] - av["actual"], LOSS)]
        x0 = -5.0
        bars = VGroup()
        for (nm, v, col), dr in zip(parts, drops):
            w = v * 9.5
            r = Rectangle(width=w, height=0.8, stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to(np.array([x0 + w / 2, 0.6, 0]))
            bars.add(VGroup(r, label(nm, font_size=18, color=col).next_to(r, DOWN, buff=dr),
                            label(rf"{100 * v:.0f}", font_size=20, color=WHITE).move_to(r)))
            x0 += w
        obs = DashedLine(np.array([-5.0 + av["actual"] * 9.5, 1.5, 0]), np.array([-5.0 + av["actual"] * 9.5, -0.3, 0]),
                         color=WHITE, stroke_width=2.6)
        ol = label(rf"the margin measured \ (here: \ the truth, \ {100 * R['true_avg']:.0f}\%)", font_size=19,
                   color=WHITE).next_to(obs, UP, buff=0.1)
        head = label(r"margin points, \ split by source", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.5)
        verdict = VGroup(
            label(r"Nevo, \ on the leading American cereal brands: \ differentiation and portfolios explain most "
                  r"of the margins", font_size=20, color=GAIN),
            label(r"prices are consistent with competition among multi-product firms; \ collusion is not needed",
                  font_size=20, color=GAIN),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.7)
        tag = published_tag(tables.NEVO_2001.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Now compare with margins measured some other way. <bookmark mark='a'/> On the Island, split the margin "
            f"into its sources: {100 * av['single']:.0f} points from differentiation, "
            f"{100 * (av['actual'] - av['single']):.0f} from firms owning several brands, and another "
            f"{100 * (av['joint'] - av['actual']):.0f} that a cartel would add. <bookmark mark='b'/> The margin "
            f"actually earned, which on the Island we know, is {say_pct(R['true_avg'], 0)}: exactly what competition "
            "among multi-product firms predicts. <bookmark mark='c'/> Nevo did this for the leading American cereal "
            "brands, comparing with margins from accounting data. Differentiation and portfolios explained most of "
            "the margins. The industry's prices were consistent with firms competing, not colluding, despite the "
            "high margins that had made the Commission suspicious."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[1]), FadeIn(bars[2]))
            vo.wait_until("b")
            self.play(Create(obs), FadeIn(ol))
            vo.wait_until("c")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.clear_scene()

    def caveats(self):
        cards = point_cards([
            (r"demand must be right", r"the markups inherit \\ every error in the \\ elasticities", DEMAND),
            (r"conduct is a hypothesis", r"Nash-Bertrand is \\ tested against \\ alternatives, \ not \\ proved", PRICE),
            (r"the benchmark is rough", r"accounting margins \\ mix marginal and \\ average costs", HOLD),
            (r"other evidence", r"documents, \ price \\ jumps, \ cases: \ the \\ MillerCoors story \\ (chapter 14)",
             LOSS),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.1)
        head = label(r"what the method needs", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.NEVO_2001.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The method is powerful, and it rests on assumptions worth naming. <bookmark mark='a'/> Demand must be "
            "right: every error in the elasticities passes straight into the markups. <bookmark mark='b'/> Conduct "
            "is a hypothesis: competition among multi-product firms is tested against alternatives, not proved. "
            "<bookmark mark='c'/> The benchmark is rough: accounting margins mix the cost of one more box with "
            "average costs such as advertising. <bookmark mark='d'/> And economists also use other evidence, such "
            "as documents and sudden price jumps, as a story in chapter fourteen shows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
