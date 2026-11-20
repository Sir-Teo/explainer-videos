from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403


class Optimum(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The optimum quantity of money", r"What rate of inflation is best?",
             "Chapter twelve. The optimum quantity of money.", lit={1969: r"Friedman", 2000: r"Lucas"},
             scale=("nation",), horizon=("years",))
        self.rule()
        self.cost()
        self.practice()

    def rule(self):
        rows = VGroup(
            label(r"Milton Friedman, \ ``The Optimum Quantity of Money'', \ 1969", font_size=26, color=E.ACCENT),
            label(r"money costs nothing to print; \ holding it costs you the interest you give up", font_size=23,
                  color=GREY_A),
            label(r"so people economize on something society could provide free: \ a waste", font_size=23,
                  color=PRICE),
            MathTex(r"i = r + \pi = 0 \quad\Longrightarrow\quad \pi = -r", font_size=48, color=MONEY),
            label(r"the Friedman rule: \ a gentle deflation, \ at the real rate of interest", font_size=24,
                  color=MONEY),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Friedman, \emph{The Optimum Quantity of Money and Other Essays} (1969)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "How much money should there be? <bookmark mark='a'/> Milton Friedman's answer, in 1969, starts from a "
            "gap. <bookmark mark='b'/> Printing money costs society almost nothing, but holding it costs each of us "
            "the interest we give up. <bookmark mark='c'/> So people make extra trips to the bank and keep balances "
            "too thin, economizing on something the economy could provide for free. <bookmark mark='d'/> Close the "
            "gap: make the nominal interest rate zero. By Fisher's equation that means inflation equal to minus the "
            "real rate. <bookmark mark='e'/> The Friedman rule: a gentle, steady deflation."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def cost(self):
        c = load("cia")
        mu = np.array(c["mu"])
        ax = plane([-0.05, 0.5], [0, 0.09], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.2, y_length=4.8,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 0.02, 0.04, 0.06, 0.08],
                   xlabel=r"money growth \ $=$ inflation, \ a year", ylabel=r"welfare cost, \ share of consumption",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16)
        line_ = path(ax, mu, c["loss"], color=PRICE, width=4, yr=(0, 0.09))
        fr = dot(ax, c["friedman_mu"], 0, color=MONEY, r=0.1)
        ten = dot(ax, 0.10, c["at"]["10"], color=E.ACCENT, r=0.09)
        side = VGroup(
            label(r"the Island with cash in advance: \\ consumption bought with money \\ carried from the day "
                  r"before", font_size=19, color=GREY_A),
            label(rf"the Friedman rule: \ ${100 * c['friedman_mu']:.0f}\%$ a year, \\ no cost", font_size=20,
                  color=MONEY),
            label(rf"10\% inflation: \ {100 * c['at']['10']:.2f}\% \\ of consumption, \ for ever", font_size=21,
                  color=E.ACCENT),
            label(rf"50\%: \ {100 * c['at']['50']:.1f}\%", font_size=20, color=PRICE),
            label(r"Lucas, \ 2000, \ on US data: \\ 10\% to zero is worth \\ slightly less than 1\% of income",
                  font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Lucas, Econometrica 68(2) (2000): \ 247--274", corner=DR, font_size=12)
        with self.voiceover(
            "How much does the gap cost? Agora gives the Island cash in advance: islanders must buy today's "
            "consumption with money carried from yesterday. Inflation taxes that money, so they work and consume a "
            "little less. <bookmark mark='a'/> At the Friedman rule, a deflation of four percent a year here, the "
            f"cost is zero. <bookmark mark='b'/> At ten percent inflation it is about {100 * c['at']['10']:.1f} "
            "percent of consumption, every year, for ever. <bookmark mark='c'/> At fifty percent, about "
            f"{100 * c['at']['50']:.0f}. <bookmark mark='d'/> Robert Lucas estimated in 2000, from a century of "
            "American money demand, that bringing inflation from ten percent to zero is worth slightly less than "
            "one percent of income. Small each year, large over a lifetime."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(line_), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(GrowFromCenter(fr), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(GrowFromCenter(ten), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def practice(self):
        rows = VGroup(
            label(r"no central bank follows the Friedman rule", font_size=27, color=E.ACCENT),
            label(r"with prices that adjust slowly, \ steady prices avoid other costs \ (Part 30)", font_size=23,
                  color=GREY_A),
            label(r"interest rates near zero leave no room to cut in a slump \ (Part 31)", font_size=23,
                  color=RATE),
            label(r"measured inflation overstates true inflation a little \ (Part 3)", font_size=23, color=GREY_A),
            label(r"so most aim for about 2\%: \ an inflation target, \ first adopted by New Zealand in 1990",
                  font_size=24, color=MONEY),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "Yet no central bank follows the Friedman rule. <bookmark mark='a'/> When prices adjust slowly, a "
            "steady price level avoids other costs, which Part thirty measures. <bookmark mark='b'/> Interest rates "
            "kept near zero leave no room to cut them in a slump. <bookmark mark='c'/> And measured inflation "
            "slightly overstates the true rise in the cost of living, as Part three showed. "
            "<bookmark mark='d'/> So most central banks aim for about two percent a year, an inflation target, a "
            "practice New Zealand began in 1990. Part thirty-one asks why two."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
