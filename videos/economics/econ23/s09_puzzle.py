from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class Puzzle(VoiceoverScene):
    def construct(self):
        card(self, 8, r"The equity premium puzzle, \ computed", r"Can any sensible patience and risk aversion produce "
             r"the premium?", "Chapter eight. The equity premium puzzle, computed.",
             lit={1985: r"Mehra and Prescott", 1991: r"Hansen and Jagannathan", 1989: r"Weil"},
             scale=("market", "nation"), horizon=("a century",))
        self.region()
        self.hj()
        self.riskfree()
        self.fact()

    def region(self):
        r = load("region")
        mo = load("moments")
        ax = plane([0, 0.20], [0, 0.07], center=LEFT * 1.9 + DOWN * 0.4, x_length=8.0, y_length=4.9,
                   xticks=[0, 0.05, 0.10, 0.15, 0.20], yticks=[0, 0.02, 0.04, 0.06],
                   xlabel=r"average risk-free rate, \ a year", ylabel=r"equity premium, \ a year",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16)
        pts = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.022, color=SDF).set_opacity(0.6)
                       for x, y in zip(r["rf"], r["premium"]) if 0 <= x <= 0.2 and 0 <= y <= 0.07])
        pub = mo["published"]
        data_pt = dot(ax, pub["bill"], pub["premium_mean"], color=STOCK, r=0.11)
        data_lab = label(r"the record, \ 1889--1978", font_size=19, color=STOCK).next_to(data_pt, RIGHT, buff=0.15)
        box = DashedLine(ax.ax.c2p(r["rf_max"], 0), ax.ax.c2p(r["rf_max"], 0.07), color=GREY_B, stroke_width=2)
        side = VGroup(
            label(r"Mehra and Prescott's economy: \\ consumption grows 1.8\% a year, \\ $\pm 3.6$ points, \ "
                  r"persistence 0.43", font_size=18, color=GREY_A),
            label(r"every dot: \ one patience $\beta < 1$ \\ and one risk aversion $\gamma \le 10$", font_size=18,
                  color=SDF),
            label(rf"with a safe rate below {pc(r['rf_max'], 0)}, \\ the largest premium: \ "
                  rf"{100 * r['max_premium_rf4']:.2f}\%", font_size=20, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Mehra and Prescott did not just compute one number. They asked what the model could produce at all. "
            "<bookmark mark='a'/> Their economy's consumption grows 1.8 percent a year on average, up or down by 3.6 "
            "points, with a little persistence, matching the century's data. <bookmark mark='b'/> Agora solves it "
            "for every combination of patience below one and risk aversion up to ten, and plots each solution as a "
            "dot: the average safe rate it produces, and the premium. <bookmark mark='c'/> The record sits up here, "
            f"a safe rate under one percent and a premium of {100 * pub['premium_mean']:.1f}. "
            "<bookmark mark='d'/> Among all the model's economies with a safe rate below four percent, the largest "
            f"premium is {100 * r['max_premium_rf4']:.2f} percent: their famous bound. To raise the premium, "
            "the model must raise risk aversion, and that sends the safe rate far off to the right."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.001), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(data_pt), FadeIn(data_lab))
            vo.wait_until("d")
            self.play(FadeIn(box), FadeIn(side[2]))
        self.clear_scene()

    def hj(self):
        h = load("hj")
        mo = h["moments"]
        ax = plane([0, 30], [0, 1.0], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.6, y_length=4.8,
                   xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"risk aversion $\gamma$", ylabel=r"$\sigma(m)/\mathbb{E}(m)$", xfmt=lambda v: f"{v:g}",
                   yfmt=lambda v: f"{v:g}", font_size=16)
        curve = path(ax, h["gamma"], h["ratio"], color=SDF, width=4, yr=(0, 1.0))
        bound = seg(ax, 0, h["sharpe"], 30, h["sharpe"], color=STOCK, width=3, dashed=True)
        need = DashedLine(ax.ax.c2p(h["needed_gamma"], 0), ax.ax.c2p(h["needed_gamma"], h["sharpe"]), color=HOLD,
                          stroke_width=2)
        side = VGroup(
            MathTex(r"\frac{\sigma(m)}{\mathbb{E}(m)} \;\ge\; \frac{|\mathbb{E}[R - R_f]|}{\sigma(R - R_f)}",
                    font_size=34, color=WHITE),
            label(r"Hansen and Jagannathan, \ 1991", font_size=19, color=GREY_B),
            label(rf"stocks' Sharpe ratio, \ 1889--2009: \ {h['sharpe']:.2f}", font_size=20, color=STOCK),
            label(rf"power utility: \ $\sigma(m)/\mathbb{{E}}(m) \approx \gamma\,\sigma_c$, \\ "
                  rf"$\sigma_c = {100 * mo['sd_growth']:.1f}\%$", font_size=20, color=SDF),
            label(rf"needs $\gamma \ge {h['needed_gamma']:.1f}$", font_size=24, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Hansen and Jagannathan, JPE 99(2) (1991): \ 225--262", corner=DR, font_size=12)
        with self.voiceover(
            "In 1991 Lars Peter Hansen and Ravi Jagannathan found a sharper way to say it, with no model of "
            "consumption at all. <bookmark mark='a'/> Whatever the true discount factor is, its volatility relative "
            "to its mean must be at least the Sharpe ratio of any asset: its average excess return divided by the "
            "standard deviation of that return. <bookmark mark='b'/> For American stocks from 1889 to 2009, that "
            f"ratio is {h['sharpe']:.2f}. <bookmark mark='c'/> With power utility the discount factor's volatility "
            "is about gamma times the volatility of consumption growth, "
            f"{100 * mo['sd_growth']:.1f} percent. <bookmark mark='d'/> To clear the bar, gamma must be at least "
            f"{h['needed_gamma']:.1f}. Consumption is simply too smooth for anyone with ordinary risk aversion to "
            "demand six percent for holding stocks."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(bound))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), Indicate(bound))
            vo.wait_until("c")
            self.play(Create(curve), FadeIn(side[3]), run_time=2)
            vo.wait_until("d")
            self.play(Create(need), FadeIn(side[4]))
        self.clear_scene()

    def riskfree(self):
        h = load("hj")
        rows = VGroup(
            label(r"and then a second puzzle", font_size=28, color=E.ACCENT),
            MathTex(r"r_f \;\approx\; \rho + \gamma\, g - \tfrac{1}{2}\gamma^2\sigma_c^2", font_size=46, color=BILL),
            label(rf"with $\gamma = {h['needed_gamma']:.1f}$, \ patience $\beta = {h['beta']}$ and growth "
                  rf"{100 * h['moments']['growth']:.1f}\%: \ a safe rate of {100 * h['rf_at_need']:.0f}\% a year",
                  font_size=24, color=HOLD),
            label(rf"the record: \ about {100 * h['moments']['bill']:.0f}\%", font_size=24, color=STOCK),
            label(r"people so averse to risk want to borrow against a richer future; \ only a very high rate stops "
                  r"them", font_size=22, color=GREY_A),
            label(r"the risk-free rate puzzle \ (Philippe Weil, \ 1989)", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Weil, JME 24(3) (1989): \ 401--421", corner=DR, font_size=12)
        with self.voiceover(
            "And raising risk aversion that far creates a second puzzle. <bookmark mark='a'/> With power utility, "
            "the safe rate is roughly impatience, plus gamma times expected growth, less a precautionary term. "
            "<bookmark mark='b'/> With gamma above eight and consumption growing two percent a year, the safe rate "
            f"would be about {100 * h['rf_at_need']:.0f} percent. <bookmark mark='c'/> In the record it was about "
            f"{100 * h['moments']['bill']:.0f}. <bookmark mark='d'/> People that averse to risk are also unwilling "
            "to let their consumption grow, so they would want to borrow heavily against a richer future, and only "
            "a very high interest rate would stop them. <bookmark mark='e'/> Philippe Weil named this the risk-free "
            "rate puzzle in 1989. Power utility ties two things together, aversion to risk and willingness to "
            "substitute over time, that the data want apart."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def fact(self):
        mo = load("moments")
        f = next(x for x in facts.FACTS if x.key == "equity_premium")
        data_m = label(rf"1889--1978: \ stocks {100 * mo['published']['stock']:.1f}\%, \\ bills "
                       rf"{100 * mo['published']['bill']:.1f}\%; \ premium {100 * mo['published']['premium_mean']:.1f}"
                       r"\% \\ (Mehra and Prescott)", font_size=19, color=WHITE)
        theory_m = label(rf"power utility, \ $\gamma \le 10$: \\ at most {100 * mo['published']['model_max_premium']:.2f}"
                         r"\% \\ (chapter 8)", font_size=19, color=SDF)
        agora_m = label(r"the premium is risk aversion \\ times covariance with bad \\ times; \ explained only with \\ "
                        r"disasters or habits \ (chapter 9)", font_size=19, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, SDF, None)).move_to(UP * 0.1)
        with self.voiceover(
            "That goes on the list of facts. <bookmark mark='a'/> Stocks have paid several points a year more than "
            "safe bills: six, in Mehra and Prescott's century, five and a half in Shiller's longer one. "
            "<bookmark mark='b'/> The standard theory can give a third of a point. Agora's column waits for the "
            "next chapter, which repairs the model three ways."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols])
            vo.wait_until("a")
            self.play(FadeIn(fc.cols[0][2:]))
            vo.wait_until("b")
            self.play(FadeIn(fc.cols[1][2:]), FadeIn(fc.cols[2][2:]))
        self.clear_scene()
