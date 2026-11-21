from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403


class Economy(VoiceoverScene):
    def construct(self):
        card(self, 6, r"The budget and the wider economy", r"What does it cost, \ who pays, \ and what else moves?",
             "Chapter six. The budget and the wider economy.", lit={2005: r"Milligan", 2022: r"Egger et al."},
             scale=("nation",), horizon=("a year", "a decade"))
        self.cost()
        self.financing()
        self.ripples()

    def cost(self):
        I = load("island")
        Ec = load("economy")
        B = load("budget")
        gdp_w, frac = 11.0, Ec["share_gdp"]
        bar_gdp = Rectangle(width=gdp_w, height=0.55, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9)
        bar_gdp.move_to(DOWN * 1.0)
        bar_cost = Rectangle(width=max(gdp_w * frac, 0.04), height=0.55, stroke_width=0, fill_color=NEW,
                             fill_opacity=1.0).align_to(bar_gdp, LEFT).align_to(bar_gdp, DOWN)
        l_gdp = label(rf"American GDP, \ 2024: \ \${Ec['gdp_2024'] / 1e12:.1f} trillion", font_size=18,
                      color=GREY_A).next_to(bar_gdp, UP, buff=0.12).align_to(bar_gdp, RIGHT)
        l_cost = label(rf"the allowance, \ scaled: \ about \${Ec['us_cost'] / 1e9:.0f} billion a year, \ "
                       rf"{100 * Ec['share_gdp']:.2f}\% of GDP", font_size=18, color=NEW).next_to(
            bar_gdp, DOWN, buff=0.2).align_to(bar_gdp, LEFT)
        top = VGroup(
            label(rf"the Island: \ \${I['cost'] / 1e6:.0f} million a year", font_size=26, color=BUDGET),
            label(rf"\${I['per_child']:,.0f} for each child, \ after taxes and credits change".replace(",", "{,}"),
                  font_size=22, color=WHITE),
            label(rf"of which responses add \${B['fiscal_externality'] / 1e6:.1f} million: \ "
                  rf"{100 * B['fe_share']:.1f}\%", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.22).move_to(UP * 2.0)
        tags = VGroup(island_tag(corner=DR, font_size=12),
                      data_tag(r"BEA, \ via FRED (GDPA); \ scaled by some 70 million children", corner=DL,
                               font_size=12))
        with self.voiceover(
            "First, the budget. <bookmark mark='a'/> On the Island the allowance costs "
            f"{I['cost'] / 1e6:.0f} million dollars a year more than the old credit, <bookmark mark='b'/> about "
            f"{I['per_child']:,.0f} dollars for each child, counting the credits paid and the change in taxes "
            "collected. <bookmark mark='c'/> Surprisingly, families' responses barely change the cost: the parents "
            "who stop working earned little, paid little tax and received the earned income credit, so the budget "
            f"loses almost nothing when they stop, about {100 * B['fe_share']:.1f} percent of the cost. <bookmark "
            "mark='d'/> Scaled to some seventy million American children, that is about "
            f"{Ec['us_cost'] / 1e9:.0f} billion dollars a year: <bookmark mark='e'/> about a third of one percent "
            "of the country's income. Large in dollars, small against the economy."
        ) as vo:
            self.play(FadeIn(tags[0]))
            vo.wait_until("a")
            self.play(FadeIn(top[0]))
            vo.wait_until("b")
            self.play(FadeIn(top[1]))
            vo.wait_until("c")
            self.play(FadeIn(top[2]))
            vo.wait_until("d")
            self.play(FadeIn(bar_gdp), FadeIn(l_gdp), FadeIn(tags[1]))
            vo.wait_until("e")
            self.play(GrowFromEdge(bar_cost, LEFT), FadeIn(l_cost))
            self.play(Indicate(bar_cost, color=WHITE, scale_factor=1.3))
        self.clear_scene()

    def financing(self):
        Ec = load("economy")
        ax = plane([0, 0.6], [1.0, 2.6], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[1.0, 1.5, 2.0, 2.5],
                   xlabel=r"elasticity of taxable income at the top",
                   ylabel=r"cost to top earners of \$1 of revenue", xfmt=lambda v: f"{v:.1f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        curve = path(ax, Ec["curve_e"], Ec["curve_mcpf"], BUDGET, 3.2)
        pts = VGroup(*[dot(ax, e, m, BUDGET, 0.08) for e, m in zip(Ec["e"], Ec["mcpf"])])
        nums = VGroup(*[label(f"{m:.2f}", font_size=15, color=WHITE).next_to(p, UL, buff=0.08)
                        for p, m in zip(pts, Ec["mcpf"])])
        opts = VGroup(
            label(r"three ways to pay:", font_size=20, color=WHITE),
            label(r"borrow: \\ the bill moves \\ to later taxpayers", font_size=18, color=GREY_A),
            label(r"a top surtax: \\ the curve", font_size=18, color=BUDGET),
            label(r"cut other spending: \\ the cost is what \\ that spending did", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        assume = label(rf"top rate {100 * Ec['tau']:.0f}\%, \ Pareto exponent {Ec['a']:.1f} \ (Part 41)",
                       font_size=14, color=GREY_B).next_to(ax, DOWN, buff=0.45)
        with self.voiceover(
            "Who pays? A memo must not hide this, because the answer can depend on it. <bookmark mark='a'/> There "
            "are three ways. Borrowing, which moves the bill to later taxpayers. <bookmark mark='b'/> A tax on top "
            "incomes. <bookmark mark='c'/> Or cutting other spending, whose cost is whatever that spending was "
            "doing. <bookmark mark='d'/> For the surtax, Part forty-one's tools give the price. With a top rate of "
            "forty percent and top incomes spread like American ones, raising a dollar of revenue costs top "
            f"earners {Ec['mcpf'][0]:.2f} dollars if their elasticity is 0.1, <bookmark mark='e'/> "
            f"{Ec['mcpf'][1]:.2f} at a quarter, and {Ec['mcpf'][2]:.2f} at 0.4, because some of each new dollar of "
            "tax is lost to smaller reported incomes. <bookmark mark='f'/> That number, the marginal cost of "
            "public funds, returns in chapter nine, where it sits underneath the value of the allowance."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(opts[0]), FadeIn(assume))
            vo.wait_until("a")
            self.play(FadeIn(opts[1]))
            vo.wait_until("b")
            self.play(FadeIn(opts[2]))
            vo.wait_until("c")
            self.play(FadeIn(opts[3]))
            vo.wait_until("d")
            self.play(Create(curve), FadeIn(pts[0]), FadeIn(nums[0]), run_time=1.8)
            vo.wait_until("e")
            self.play(FadeIn(pts[1:]), FadeIn(nums[1:]))
            vo.wait_until("f")
            self.play(Indicate(nums, color=WHITE))
        self.clear_scene()

    def ripples(self):
        Ec = load("economy")
        cards = point_cards([
            (r"prices", rf"spending rises by about {100 * Ec['share_pce']:.1f}\% of consumption, \ spread across "
                        r"the country: \ in Kenya, \ far larger transfers moved local prices little (Part 46)",
             NEW),
            (r"wages", r"if some parents leave work, \ those who stay earn a little more: \ small, \ and in the "
                       r"same direction as the policy", WORK),
            (r"births", r"Quebec's allowance of up to 8,000 Canadian dollars a birth raised fertility by up to a "
                        r"quarter where the full amount was paid: \ a weaker incentive here, \ but not zero"
             .replace("8,000", "8{,}000"), CHILD),
            (r"the long run", r"children's health, \ schooling and earnings: \ the budget's biggest unknown",
             EVIDENCE),
        ], width=12.4, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"what else moves", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(r"Milligan, \ REStat (2005); \ Egger et al., \ Econometrica (2022)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "What else moves, beyond the families themselves? General equilibrium, in the language of Part nine. "
            "<bookmark mark='a'/> Prices: the allowance adds about half of one percent to what Americans spend, "
            "spread across the whole country. In Kenya, transfers far larger relative to local incomes moved local "
            "prices very little. <bookmark mark='b'/> Wages: if some parents leave work, those who stay may earn a "
            "little more, a small effect in the policy's own direction. <bookmark mark='c'/> Births: from 1988 "
            "Quebec paid up to eight thousand Canadian dollars for a birth, and Kevin Milligan found fertility rose, "
            "by up to a quarter among families eligible for the full amount. A smaller yearly payment per child is "
            "a weaker incentive, but not none, and Part forty-nine's quantity and quality says what it might do. "
            "<bookmark mark='d'/> And the long run: what the money does for children's health, schooling and later "
            "earnings, which is also the budget's biggest unknown, because healthier, better-educated adults pay "
            "more tax. The next chapter is the evidence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
