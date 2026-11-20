from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Islands(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Lucas's islands", r"Why would a surprise move output at all?", "Chapter seven. Lucas's "
             "islands.", lit={1972: r"Lucas", 1975: r"Sargent and Wallace"}, scale=("market", "nation"),
             horizon=("a year",))
        self.story()
        self.weight()
        self.ineffective()

    def story(self):
        rows = VGroup(
            label(r"Lucas, \ 1972: \ producers on separate islands", font_size=26, color=E.ACCENT),
            label(r"each sees only the price of its own good", font_size=23, color=WAGE),
            label(r"a higher price might mean more demand for my good: \ produce more", font_size=23, color=OUTPUT),
            label(r"or more money everywhere: \ all prices up, \ and nothing real has changed", font_size=23,
                  color=INFL),
            label(r"so each producer guesses: \ a signal-extraction problem", font_size=24, color=EXPECT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Lucas, \ ``Expectations and the neutrality of money'', \ JET 4(2) (1972): \ 103--124",
                            corner=DR, font_size=12)
        with self.voiceover(
            "If people forecast rationally, why would a surprise ever move output? Robert Lucas answered in 1972 "
            "with a parable. <bookmark mark='a'/> Producers live on separate islands. Each sees only the price of "
            "its own good. <bookmark mark='b'/> When that price rises, it might mean more people want this good. "
            "Then it pays to work harder and produce more. <bookmark mark='c'/> Or it might mean that there is "
            "more money everywhere, every price is up, and nothing real has changed. Then producing more is a "
            "mistake. <bookmark mark='d'/> Each producer has to guess which, from a single price. Economists call it "
            "a signal-extraction problem."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def weight(self):
        I = load("islands")
        ax = plane([0, 4], [0, 1], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.0, y_length=4.8,
                   xticks=[0, 1, 2, 3, 4], yticks=[0, 0.25, 0.5, 0.75, 1], xlabel=r"how volatile money is, "
                   r"$\sigma_m$", ylabel=r"output's response to a money surprise", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:g}", font_size=15)
        th = path(ax, I["sigma_m"], I["theta"], color=EXPECT, width=4)
        c, w = I["calm"], I["wild"]
        d0 = dot(ax, I["sigma_m_calm"], c["slope"], color=OUTPUT, r=0.09)
        d1 = dot(ax, I["sigma_m_wild"], w["slope"], color=INFL, r=0.09)
        side = VGroup(
            MathTex(r"\theta = \frac{\sigma_z^2}{\sigma_z^2 + \sigma_m^2}", font_size=36, color=EXPECT),
            label(r"the share of a price rise \\ a producer reads as real", font_size=19, color=GREY_A),
            label(rf"calm money ($\sigma_m = {I['sigma_m_calm']}$): \\ output responds {c['slope']:.2f}", font_size=19,
                  color=OUTPUT),
            label(rf"wild money ($\sigma_m = {I['sigma_m_wild']:.0f}$): \\ only {w['slope']:.2f}", font_size=19,
                  color=INFL),
            label(r"the trade-off is steepest \\ where inflation is volatile: \\ Lucas, \ 1973, \ across countries",
                  font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The answer depends on how noisy each kind of news is. <bookmark mark='a'/> A rational producer treats a "
            "share theta of any price surprise as real, where theta compares the variance of relative prices with "
            "the variance of money. <bookmark mark='b'/> On the Island, with two hundred producers and sixty years: "
            f"when money is calm, output responds {c['slope']:.2f} to a money surprise, because a price rise usually "
            f"means real demand. <bookmark mark='c'/> When money is wild, output responds only {w['slope']:.2f}, "
            "because producers have learned that most price rises are just inflation. <bookmark mark='d'/> So the "
            "trade-off should be steepest where inflation is most volatile, and Lucas found that pattern across "
            "eighteen countries in 1973: in Argentina, with its wild inflation, demand moved prices and barely "
            "moved output."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(th), FadeIn(side[0]), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(GrowFromCenter(d0), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(GrowFromCenter(d1), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def ineffective(self):
        rows = VGroup(
            label(r"Sargent and Wallace, \ 1975: \ the policy-ineffectiveness proposition", font_size=25,
                  color=E.ACCENT),
            label(r"only surprises move output", font_size=24, color=SURPRISE),
            label(r"a monetary rule that responds to last year's slump is foreseen, \ so it surprises nobody",
                  font_size=23, color=CB),
            label(r"so systematic monetary policy cannot steady output: \ only random policy moves it, \ and "
                  r"badly", font_size=23, color=INFL),
            label(r"if prices are flexible: \ Part 30 shows what sticky prices change", font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Sargent and Wallace, \ JPE 83(2) (1975): \ 241--254", corner=DR, font_size=12)
        with self.voiceover(
            "Thomas Sargent and Neil Wallace drew the startling conclusion in 1975. <bookmark mark='a'/> If only "
            "surprises move output, <bookmark mark='b'/> then a monetary rule that eases after a bad year is "
            "foreseen, built into expectations, and surprises nobody. <bookmark mark='c'/> Systematic monetary "
            "policy cannot steady output at all; only random policy moves it, and that only adds noise. "
            "<bookmark mark='d'/> The result needs prices that adjust freely. Part thirty shows what happens when "
            "prices are set in advance, and policy works again."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
