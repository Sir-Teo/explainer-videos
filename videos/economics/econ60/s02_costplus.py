from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class CostPlus(VoiceoverScene):
    def construct(self):
        card(self, 1, r"What firms say they do", r"If the theory says price by the elasticity, \ why do firms add "
             r"a markup to cost?", "Chapter one. What firms say they do.",
             lit={1939: r"Hall and Hitch", 1998: r"Blinder et al."}, scale=("firm",), horizon=("a year",))
        self.surveys()
        self.flat_top()

    def surveys(self):
        cards = VGroup(
            history_card(1939, r"Robert Hall and Charles Hitch, \ Oxford", r"businessmen interviewed said they priced "
                         r"at `full cost': \ average cost plus a conventional margin, \ and rarely changed it",
                         color=FIRM, width=11.4, font_size=21),
            history_card(1998, r"Alan Blinder and coauthors, \ Asking About Prices", r"two hundred American firms "
                         r"interviewed: \ the typical one changes its price only about once a year", color=FIRM,
                         width=11.4, font_size=21),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.8)
        rule = MathTex(r"\text{the theory: } \ \frac{p - c}{p} = \frac{1}{\varepsilon} \iff p = c\,"
                       r"\frac{\varepsilon}{\varepsilon - 1}", font_size=34, color=WHITE).next_to(cards, DOWN,
                                                                                         buff=0.5)
        tag = published_tag(r"Hall and Hitch, \ Oxford Economic Papers (1939); \ Blinder, \ Canetti, \ Lebow and Rudd "
                            r"(1998)", corner=DL, font_size=12)
        with self.voiceover(
            "Ask firms how they set prices and many give the same answer. <bookmark mark='a'/> In 1939 Robert Hall "
            "and Charles Hitch, at Oxford, interviewed businessmen and reported that most said they priced at full "
            "cost: average cost plus a conventional margin, which they rarely changed. <bookmark mark='b'/> Sixty "
            "years later Alan Blinder and his coauthors interviewed two hundred American firms and found that the "
            "typical one changes its price only about once a year. "
            "<bookmark mark='c'/> The theory of Part ten says something different: set the markup by the "
            "elasticity of demand, so that the margin as a share of price is one over the elasticity. Is "
            "cost-plus simply a mistake?"
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(Write(rule))
        self.clear_scene()

    def flat_top(self):
        C = load("costplus")
        grid, curve = np.array(C["grid"]), np.array(C["curve"])
        ax = plane([1.0, 3.0], [0, 1.05], center=LEFT * 2.7 + DOWN * 0.4, x_length=6.4, y_length=4.6,
                   xticks=[1.0, 1.5, 2.0, 2.5, 3.0], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"price $\div$ marginal cost", ylabel=r"profit, \ share of the best",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        cv = path(ax, grid, curve, OPT, 3.0)
        best = dot(ax, C["p_opt"], 1.0, OPT, 0.09)
        fixed = dot(ax, 1 + C["markup"], C["fixed"], FIRM, 0.09)
        band_ = shade(ax, [(1.45, 1.9)], 0, 1.05, FIRM, 0.12)
        side = VGroup(
            label(rf"elasticity {C['eps']:.1f}: \ the best price is {C['p_opt']:.2f} times cost", font_size=20,
                  color=OPT),
            label(r"the top is flat: \ prices from 1.45 to 1.9 times cost \\ all earn more than 95\% of the best",
                  font_size=19, color=GREY_A),
            label(r"but the elasticity is only estimated:", font_size=20, color=WHITE),
            label(rf"the rule with a noisy estimate: \ {100 * C['rule_mean']:.0f}\% on average, \ "
                  rf"{100 * C['rule_p10']:.0f}\% in the worst tenth", font_size=20, color=TEST),
            label(rf"a fixed markup of {100 * C['markup']:.0f}\%: \ {100 * C['fixed']:.1f}\%", font_size=20,
                  color=FIRM),
            label(r"a rule of thumb can be a sensible answer \\ to not knowing the demand curve", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.35)
        tag = agora_tag(r"computed: \ agora.revenue.cost\_plus\_robustness; \ constant-elasticity demand",
                        corner=DL, font_size=12)
        with self.voiceover(
            "Not necessarily. <bookmark mark='a'/> Here is profit against price, for a product whose demand has an "
            f"elasticity of {C['eps']:.1f}. The best price is {C['p_opt']:.2f} times marginal cost. <bookmark "
            "mark='b'/> But look at the top of the curve: it is flat. Every price from about 1.45 to 1.9 times cost "
            "earns more than ninety-five percent of the best profit. <bookmark mark='c'/> Now suppose the firm does "
            "not know its elasticity, which it never does exactly, and estimates it with a realistic error. "
            "<bookmark mark='d'/> Applying the textbook rule to the estimate earns, on average, "
            f"{100 * C['rule_mean']:.0f} percent of the best profit, and in the worst tenth of cases only "
            f"{100 * C['rule_p10']:.0f}: when the estimated elasticity comes out near one, the rule demands an "
            f"absurd price. <bookmark mark='e'/> A fixed markup of {100 * C['markup']:.0f} percent earns "
            f"{100 * C['fixed']:.1f} percent, every time. <bookmark mark='f'/> So cost-plus is not ignorance of "
            "the theory. A conventional markup, adjusted now and then by what the market will bear, can be a "
            "sensible answer to not knowing the demand curve. The rest of this part is about firms that try to "
            "learn it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(best), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(band_), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(fixed, scale=1.5), FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()
