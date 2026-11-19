from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403

LIN = "#7EC8F5"
CES = "#F2A65A"


class PassThrough(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Pass-through: \ who pays when costs rise?", r"When a seller's cost rises by a dollar, how "
             r"much does its price rise?", "Chapter thirteen. Pass-through: who pays when costs rise?",
             lit={2010: r"Nakamura and Zerom"}, scale=("firm", "market", "world"), horizon=("a quarter", "a year"))
        self.theory()
        self.fact()
        self.lags()
        self.accounting()

    def theory(self):
        p = load("passthrough")
        cs = np.array(p["cs"])
        ax = plane([0, 6], [0, 10], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.2, y_length=5.0,
                   xticks=[0, 2, 4, 6], yticks=[0, 2, 4, 6, 8, 10], xlabel=r"marginal cost, \ \$",
                   ylabel=r"monopoly price, \ \$", font_size=17)
        a = ax.ax
        lin = path(ax, cs, p["lin_p"], color=LIN, width=3.5, smooth=False)
        ce = path(ax, cs, p["ce_p"], color=CES, width=3.5, smooth=False, yr=(0, 10))
        diag = DashedLine(a.c2p(0, 0), a.c2p(6, 6), color=GREY_C, stroke_width=1.5)
        dl = label(r"price = cost", font_size=16, color=GREY_B).next_to(a.c2p(5.6, 5.6), DR, buff=0.02)
        ll = label(r"straight-line demand", font_size=17, color=LIN).next_to(a.c2p(1.2, 5.75), UP, buff=0.05)
        cl = label(rf"constant elasticity, \ $\varepsilon = {p['eps']:.0f}$", font_size=17, color=CES).next_to(
            a.c2p(2.3, 3.5), LEFT, buff=0.05)
        side = VGroup(
            label(r"pass-through: \ how much the price moves \\ per dollar of cost", font_size=22),
            MathTex(r"\rho = \frac{dp}{dc}", font_size=40, color=E.ACCENT),
            label(rf"straight-line demand: \ $\rho = {p['rho_lin']:.1f}$, \\ the firm absorbs half", font_size=22,
                  color=LIN),
            label(rf"constant elasticity: \ $p = \frac{{\varepsilon}}{{\varepsilon - 1}}\,c$, \ $\rho = "
                  rf"{p['rho_ce']:.1f}$, \\ more than the cost rise", font_size=22, color=CES),
            label(r"the shape of demand decides: \\ how fast elasticity changes along it", font_size=22,
                  color=E.ACCENT),
            label(r"in a competitive market: \ the tax-incidence \\ rule of Part 2, \ by supply and demand",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "When a monopolist's cost rises, who pays? <bookmark mark='a'/> Economists measure it with pass-through: "
            "how many cents the price rises for each dollar of cost. <bookmark mark='b'/> With straight-line demand "
            "the monopoly price is halfway between the cost and the top of the demand curve, so a dollar of cost "
            "raises the price by fifty cents. The seller absorbs the other half. <bookmark mark='c'/> With constant "
            "elasticity demand the price is a fixed markup on cost, one and a half times cost when the elasticity is "
            "three, so a dollar of cost raises the price by a dollar fifty, more than the cost itself. "
            "<bookmark mark='d'/> So pass-through depends on the shape of demand: whether customers become more "
            "sensitive or less sensitive as the price rises. <bookmark mark='e'/> In a competitive market the "
            "same question is answered by supply and demand, the tax-incidence rule of Part two."
        ) as vo:
            self.play(FadeIn(ax), Create(diag), FadeIn(dl), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Write(side[1]))
            vo.wait_until("b")
            self.play(Create(lin), FadeIn(ll), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(ce), FadeIn(cl), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def fact(self):
        p = load("passthrough")
        fa = facts.BY_KEY["passthrough"]
        months = p["months"]
        x = np.array([int(m[:4]) + (int(m[5:7]) - 1) / 12 for m in months])
        guess = label(r"(yours: \ of a 10\% rise \\ in the bean price, \\ how much on the shelf?)", font_size=22,
                      color=E.ACCENT)
        mini = plane([1980, 2027], [0, 10], x_length=3.4, y_length=1.25, xticks=[1980, 2000, 2020],
                     yticks=[0, 5, 10], font_size=12)
        sh = path(mini, x, p["shelf"], color=SHELF, width=1.6, smooth=False)
        bn = path(mini, x, p["bean"], color=BEAN, width=1.6, smooth=False)
        data_col = VGroup(VGroup(mini, sh, bn),
                          label(r"\$ a pound: \ ground coffee on the shelf \\ (white), \ green arabica (brown)",
                                font_size=18, color=GREY_A)).arrange(DOWN, buff=0.08)
        ag = VGroup(
            label(rf"straight-line demand: \ {p['rho_lin']:.1f}", font_size=22, color=LIN),
            label(rf"constant elasticity: \ {p['rho_ce']:.1f}", font_size=22, color=CES),
            label(r"per dollar of cost", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fc = fact_card(fa.statement, columns=((r"your guess", guess), (r"the data", data_col), (r"Agora", ag)),
                       width=12.6).move_to(UP * 1.0)
        rows = VGroup(
            label(rf"{len(months)} months, \ {months[0][:4]}--{months[-1][:4]}: \ the bean price swings by a "
                  r"factor of almost eight", font_size=24),
            label(r"the shelf price follows, \ slowly and partly", font_size=24, color=SHELF),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.55)
        tag = data_tag(r"FRED (BLS): APU0000717311; World Bank Pink Sheet, arabica", corner=DL, font_size=13)
        with self.voiceover(
            "Real markets give the fourth of this series' Facts. <bookmark mark='a'/> Before the data, a guess: if "
            "the price of green coffee beans rises ten percent, how much do you think the price of a pound of "
            "ground coffee in an American supermarket rises? <bookmark mark='b'/> Here are the two prices, which "
            "the intermission played: the shelf price from the Bureau of Labor Statistics, and green arabica beans "
            "from the World Bank, both in dollars a pound, every month since 1980. <bookmark mark='c'/> Agora's two "
            "monopolies gave half and one and a half. <bookmark mark='d'/> Over five hundred months the bean price "
            "swings by a factor of almost eight. <bookmark mark='e'/> The shelf price follows, but slowly, and only part "
            "of the way."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc.head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1]))
            vo.wait_until("c")
            self.play(FadeIn(fc.cols[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def lags(self):
        p = load("passthrough")
        el = np.array(p["elasticity_lags"])
        cum = el.cumsum()
        ax = plane([-0.5, 6.5], [0, 0.7], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.2, y_length=5.0,
                   xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
                   xlabel=r"quarters after the bean price moves", ylabel=r"shelf price change per 1\% of beans, \ \%",
                   font_size=16)
        a = ax.ax
        bars = VGroup(*[Rectangle(width=0.55, height=max(a.c2p(0, v)[1] - a.c2p(0, 0)[1], 1e-3), stroke_width=0,
                                  fill_color=SHELF, fill_opacity=0.85).move_to(a.c2p(k, 0), aligned_edge=DOWN)
                        for k, v in enumerate(cum)])
        nums = VGroup(*[label(rf"{v:.2f}", font_size=16, color=SHELF).next_to(b, UP, buff=0.05)
                        for b, v in zip(bars, cum)])
        share = DashedLine(a.c2p(-0.5, p["bean_share"]), a.c2p(6.5, p["bean_share"]), color=BEAN, stroke_width=2)
        key = DashedLine(ORIGIN, RIGHT * 0.45, color=BEAN, stroke_width=2)
        sl = VGroup(key, label(rf"beans' share of the shelf price, \ {p['bean_share']:.2f}", font_size=16,
                               color=BEAN)).arrange(RIGHT, buff=0.12)
        sl.move_to(a.c2p(-0.4, 0.665), aligned_edge=LEFT)
        side = VGroup(
            label(r"regress the quarterly change in the log shelf price \\ on this quarter's and six earlier "
                  r"quarters' changes \\ in the log bean price", font_size=20),
            label(rf"in the first quarter: \ {p['elasticity_first']:.2f}", font_size=22, color=SHELF),
            label(rf"after six quarters: \ {p['elasticity']:.2f}", font_size=22, color=SHELF),
            label(r"a 10\% rise in beans: \ about 1.5\% on the shelf at once, \\ about 5.5\% after a year and a half",
                  font_size=21, color=E.ACCENT),
            label(rf"in dollars: \ \${p['dollars']:.2f} on the shelf per \$1 a pound of beans, \\ "
                  r"and a pound of roast coffee takes about 1.19 pounds of beans", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"FRED (BLS): APU0000717311; Pink Sheet; quarterly, 1980--2026 (computed)", corner=DR,
                       font_size=13)
        with self.voiceover(
            "To measure it, Agora averages each price over the quarter and regresses the change in the log of the "
            "shelf price on the change in the log of the bean price, this quarter's and the six before. "
            "<bookmark mark='a'/> In the first quarter, the shelf price moves fifteen hundredths of a percent for "
            "every percent on the beans. <bookmark mark='b'/> The effect builds, and after six quarters it reaches "
            "fifty-five hundredths. <bookmark mark='c'/> So a ten percent rise in the bean price adds about one and "
            "a half percent to the shelf price at once, and about five and a half percent after a year and a half. "
            "<bookmark mark='d'/> In dollars, though, the picture is different: each dollar a pound on green beans "
            "adds about a dollar sixty to a pound on the shelf, and a pound of roast coffee takes about one point "
            "one nine pounds of beans, because roasting drives off water. So in dollars, the bean cost is passed on "
            "in full, and a little more."
        ) as vo:
            self.play(FadeIn(ax), Create(share), FadeIn(sl), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(nums[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[1:]], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(n_) for n_ in nums[1:]], lag_ratio=0.3), FadeIn(side[2]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def accounting(self):
        nz = load("passthrough")["nz"]
        lc, mk = nz["local_costs"], nz["markups"]
        after_local = 1 - lc
        after_mark = after_local * (1 - mk)
        steps = VGroup()
        for name, v, col in ((r"constant markups, \ beans the only cost", 1.0, CES),
                             (r"add the costs that don't move with beans", after_local, GREY_B),
                             (r"let markups adjust", after_mark, SHELF)):
            steps.add(VGroup(label(name, font_size=21, color=col),
                             Rectangle(width=6.0 * v, height=0.4, stroke_width=0, fill_color=col, fill_opacity=0.85),
                             label(rf"{v:.2f}", font_size=21, color=col)))
        for g in steps:
            g[1].next_to(g[0], DOWN, buff=0.12, aligned_edge=LEFT)
            g[2].next_to(g[1], RIGHT, buff=0.15)
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(LEFT, buff=0.8)
        side = VGroup(
            label(r"Nakamura and Zerom (2010): \\ a model of the coffee industry, \\ brand by brand", font_size=22),
            label(rf"local costs cut long-run pass-through \\ by {100 * lc:.0f}\%", font_size=22, color=GREY_B),
            label(rf"markups adjusting cut it \\ by a further {100 * mk:.0f}\%", font_size=22, color=SHELF),
            label(r"small menu costs \\ explain the delay, \ not the size", font_size=22, color=GREY_A),
            label(r"incomplete in percent, \\ near complete in dollars: \\ say which you mean", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        tag = published_tag(r"Nakamura and Zerom, REStud 77(3) (2010), abstract", corner=DR, font_size=14)
        with self.voiceover(
            "Emi Nakamura and Dawit Zerom asked where the missing pass-through goes, with a model of the coffee "
            "industry fitted brand by brand. <bookmark mark='a'/> Their benchmark is a seller with constant markups "
            "whose only cost is beans: the shelf price would move one for one, in percent. <bookmark mark='b'/> Add "
            "the costs that don't move with the bean price, roasting, packing, shipping, shelf space, and long-run "
            "pass-through falls by fifty-nine percent. <bookmark mark='c'/> Let markups adjust, as they do when "
            "demand is less curved than constant elasticity, and it falls by a further third. "
            "<bookmark mark='d'/> Small costs of changing prices explain why the response is slow, but not why it is "
            "small. <bookmark mark='e'/> And the lesson for anyone reading a pass-through number: incomplete in "
            "percent can be complete in dollars. Say which you mean."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps[0][0]), GrowFromEdge(steps[0][1], LEFT), FadeIn(steps[0][2]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1][0]), GrowFromEdge(steps[1][1], LEFT), FadeIn(steps[1][2]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2][0]), GrowFromEdge(steps[2][1], LEFT), FadeIn(steps[2][2]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
