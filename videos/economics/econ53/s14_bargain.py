from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


class Bargaining(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Bargaining", r"How is a surplus split, \ and why do talks drag on?",
             "Chapter twelve. Bargaining.", lit={1950: r"Nash", 1982: r"Rubinstein", 1972: r"Coase"},
             scale=("person", "firm"), horizon=("a day",))
        self.nash()
        self.rubinstein()
        self.coase()

    def nash(self):
        Bg = load("bargain")
        x = np.array(Bg["frontier_x"])
        y = np.array(Bg["frontier_y"])
        ax = plane([0, 1.05], [0, 1.05], center=LEFT * 2.6 + DOWN * 0.3, x_length=5.0, y_length=5.0,
                   xticks=[0, 0.5, 1.0], yticks=[0, 0.5, 1.0], xlabel=r"what Ann gets", ylabel=r"what Bob gets",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        fr = path(ax, x, y, THEORY, 3.0)
        hyp = path(ax, np.linspace(0.3, 1.0, 50), Bg["nash"]["product"] / np.linspace(0.3, 1.0, 50), GREY_B, 1.6,
                   yr=(0, 1.05))
        nb = dot(ax, Bg["nash"]["x"], Bg["nash"]["y"], SENDER, 0.12)
        axioms = VGroup(
            label(r"Nash's four axioms:", font_size=22, color=E.ACCENT),
            label(r"efficiency: \ nothing left on the table", font_size=19, color=WHITE),
            label(r"symmetry: \ equal players, \ equal shares", font_size=19, color=WHITE),
            label(r"scale: \ units of utility do not matter", font_size=19, color=WHITE),
            label(r"irrelevant alternatives: \ removing unchosen \\ deals does not change the choice", font_size=19,
                  color=WHITE),
            label(r"only one rule satisfies all four: \\ maximize the product of the gains", font_size=21,
                  color=SENDER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Nash, \ Econometrica 18(2) (1950)", corner=DR, font_size=12)
        with self.voiceover(
            "Bargaining is where private information hurts most. Start with the case without it. In 1950 John Nash "
            "asked what any sensible rule for splitting a surplus must satisfy. <bookmark mark='a'/> The curve is "
            "the set of deals that leave nothing on the table. <bookmark mark='b'/> Nash's axioms: efficiency; "
            "symmetry; independence of the units in which utility is measured; and that removing deals nobody "
            "chose should not change the choice. <bookmark mark='c'/> Only one rule satisfies all four: choose the "
            "deal that maximizes the product of the two gains, where the frontier touches the highest of these "
            "hyperbolas. Elegant, but it says nothing about how people actually get there."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(fr), run_time=1.4)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in axioms[:5]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(hyp), FadeIn(nb, scale=1.5), FadeIn(axioms[5]))
        self.clear_scene()

    def rubinstein(self):
        Bg = load("bargain")
        rows = Bg["rubinstein"]
        eq = MathTex(r"x^* = \frac{1 - \delta_2}{1 - \delta_1 \delta_2}", r"\;\xrightarrow{\;\delta_1 = \delta_2 = "
                     r"\delta\;}\; \frac{1}{1 + \delta}", font_size=42, color=THEORY).move_to(UP * 2.0)
        steps = VGroup(
            label(r"Ann offers, \ Bob accepts or counter-offers next round; \ waiting shrinks the pie", font_size=21,
                  color=WHITE),
            label(r"the unique subgame-perfect equilibrium: \ the first offer is accepted, \ at once", font_size=21,
                  color=GAIN),
        ).arrange(DOWN, buff=0.25).next_to(eq, DOWN, buff=0.5)
        tab = VGroup(label(r"patience $\delta$", font_size=19, color=GREY_A),
                     label(r"first proposer's share", font_size=19, color=GREY_A))
        for r in rows:
            tab.add(label(f"{r['delta']}", font_size=20, color=WHITE), label(f"{r['first']:.3f}", font_size=20,
                                                                             color=SENDER))
        tab.arrange_in_grid(rows=len(rows) + 1, cols=2, buff=(0.8, 0.18)).next_to(steps, DOWN, buff=0.45)
        tag = published_tag(r"Rubinstein, \ Econometrica 50(1) (1982)", corner=DR, font_size=12)
        with self.voiceover(
            "Ariel Rubinstein modelled the haggling itself, in 1982. <bookmark mark='a'/> Ann makes an offer; Bob "
            "accepts or makes a counter-offer next round; every round of delay shrinks what is left. <bookmark "
            "mark='b'/> The game has exactly one subgame-perfect equilibrium, and in it the first offer is "
            "accepted at once. The first proposer's share depends only on the two players' patience. <bookmark "
            "mark='c'/> With equal patience it is one over one plus delta: two thirds when the discount is a half, "
            "and approaching one half as the delay between offers shrinks, which is where Nash's rule would put "
            "it. With complete information, there is no delay at all."
        ) as vo:
            self.play(Write(eq), FadeIn(tag), run_time=1.8)
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab), run_time=1.4)
        self.clear_scene()

    def coase(self):
        Bg = load("bargain")
        co = Bg["coase"]
        s, p1 = co["best"], co["best"]["p1"]
        rows = VGroup(
            label(rf"a seller; \ a buyer who values the good at {Bg['v_high']:.0f} or {Bg['v_low']:.1f}, "
                  rf"\ equally likely; \ two periods, \ discount {Bg['delta']}", font_size=21, color=WHITE),
            label(rf"with commitment: \ price {Bg['v_high']:.0f} for ever: \ profit {co['commitment_profit']:.2f}",
                  font_size=21, color=GREY_A),
            label(r"without: \ once the high-value buyer has bought, \ the seller will cut the price", font_size=21,
                  color=ERR),
            label(rf"the high-value buyer foresees it: \ she pays at most {p1:.2f} today", font_size=21,
                  color=WEAK),
            label(rf"the best the seller can do: \ {p1:.2f} now, \ {s['p2']:.1f} later: \ profit {s['profit']:.2f}",
                  font_size=21, color=SENDER),
            label(rf"the low-value buyer waits: \ delay, \ with probability {s['delay']:.1f}", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(UP * 0.1)
        tag = published_tag(r"Coase, \ JLE 15(1) (1972); \ Fudenberg and Tirole (1991), \ ch. 10", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Add private information, and delay appears. <bookmark mark='a'/> A seller faces a buyer who values "
            f"the good at {Bg['v_high']:.0f} or {Bg['v_low']:.1f}, equally likely, over two periods. <bookmark "
            f"mark='b'/> If the seller could commit, he would charge {Bg['v_high']:.0f} and never cut the price. "
            "<bookmark mark='c'/> But he cannot: once the high-value buyer has bought, the only buyer left values "
            "the good at less, and the seller will cut the price. <bookmark mark='d'/> The high-value buyer "
            f"foresees the cut and will pay only {p1:.2f} today. <bookmark mark='e'/> The seller's best plan is to "
            f"charge {p1:.2f} now and {s['p2']:.1f} later, <bookmark mark='f'/> and the low-value buyer waits: "
            "a deal that both want is delayed, purely because of what the seller does not know. Ronald Coase "
            "argued that a monopolist selling a durable good, unable to commit, competes with its own future self."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
