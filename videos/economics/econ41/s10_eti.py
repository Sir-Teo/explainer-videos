from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class ETI(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Measuring the elasticity", r"How much do top incomes respond to the rate?",
             "Chapter eight. Measuring the elasticity.", lit={1995: r"Feldstein", 2002: r"Gruber and Saez",
                                                              2012: r"Saez, \ Slemrod and Giertz"},
             scale=("person", "nation"), horizon=("a year", "a decade"))
        self.century()
        self.tra86()
        self.choice()

    def century(self):
        Et = load("eti")
        ys = np.array(Et["years"])
        ax = plane([1913, 2026], [0, 100], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.8,
                   xticks=[1920, 1940, 1960, 1980, 2000, 2020], yticks=[0, 25, 50, 75, 100],
                   ylabel=r"percent", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        rate = path(ax, ys, Et["rate"], RATE, 3.0, smooth=False)
        share = path(ax, ys, 4 * np.array(Et["top1"]), TOP, 3.2, smooth=False)
        side = VGroup(
            label(r"pink: \ the top statutory rate", font_size=18, color=RATE),
            label(r"gold: \ the top 1\% share \\ of income, \ times 4", font_size=18, color=TOP),
            label(r"when the top rate fell, \\ the top share rose", font_size=18, color=WHITE),
            label(r"but rates are not \\ the only thing that \\ changed", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"IRS via FRED; \ Piketty and Saez, \ updated to 2022", corner=DR, font_size=12)
        with self.voiceover(
            "The elasticity of taxable income is the key number, so how is it measured? Start with the long view. "
            "<bookmark mark='a'/> The top rate of the American income tax: seven percent in 1913, ninety-four at the "
            "end of the Second World War, ninety-one through the 1950s, seventy until 1981, twenty-eight in 1988, "
            "thirty-seven today. <bookmark mark='b'/> And the top one percent's share of income, magnified four "
            "times to share the scale. <bookmark mark='c'/> They move in opposite directions: high rates, low top "
            "shares; low rates, high ones. <bookmark mark='d'/> But a century brings wars, unions, technology and "
            "globalization, so the picture alone cannot say how much is the rate. Better evidence comes from sharp "
            "reforms."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(rate), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(share), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def tra86(self):
        Et = load("eti")
        rows = [(r"the top rate, \ 1986 $\to$ 1988", rf"{Et['r1986']:.0f}\% $\to$ {Et['r1988']:.0f}\%", RATE),
                (r"the share kept, \ $1 - t$", rf"{100 - Et['r1986']:.0f}\% $\to$ {100 - Et['r1988']:.0f}\% \ "
                                                rf"(+{100 * ((100 - Et['r1988']) / (100 - Et['r1986']) - 1):.0f}\%)",
                 GAIN),
                (r"the top 1\% share of income", rf"{Et['s1986']:.1f}\% $\to$ {Et['s1988']:.1f}\% \ "
                                                  rf"(+{100 * (Et['s1988'] / Et['s1986'] - 1):.0f}\%)", TOP),
                (r"implied elasticity", rf"{Et['tra86']:.2f}", E.ACCENT)]
        tbl = VGroup(*[VGroup(label(a, font_size=22, color=WHITE), label(b, font_size=22, color=c)).arrange(
            RIGHT, buff=0.6) for a, b, c in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(UP * 0.5)
        head = label(r"the Tax Reform Act of 1986", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = VGroup(
            label(r"much of it was relabelling: \ business profits moved from corporate to personal returns",
                  font_size=19,
                  color=GREY_A),
            label(rf"and timing: \ with capital gains, \ the top share jumped to {Et['s1986_kg']:.1f}\% in 1986, \ "
                  rf"before a higher capital-gains rate, \ then fell back to {Et['s1987_kg']:.1f}\%", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.55)
        tag = data_tag(r"IRS via FRED; \ Piketty and Saez; \ " + tables.ETI_STUDIES.tag, corner=DR, font_size=10)
        with self.voiceover(
            "The sharpest American reform cut the top rate from fifty percent in 1986 to twenty-eight in 1988. "
            "<bookmark mark='a'/> The share of each extra dollar a top earner kept rose by "
            f"{100 * ((100 - Et['r1988']) / (100 - Et['r1986']) - 1):.0f} percent. <bookmark mark='b'/> The top one "
            f"percent's share of income rose by {100 * (Et['s1988'] / Et['s1986'] - 1):.0f} percent, "
            f"<bookmark mark='c'/> an elasticity of about {Et['tra86']:.1f}. In 1995 Martin Feldstein, following the "
            "same taxpayers in a Treasury panel, found an elasticity of at least one. With more reforms and more "
            "years, Jonathan Gruber and Emmanuel Saez found about 0.4. <bookmark mark='d'/> Why so large in 1986? "
            "Much of the response was relabelling: the reform made it cheaper to run a business through a personal "
            "return than a corporate one, so income moved onto the personal returns the series counts. And some was "
            "timing: realized capital gains surged in 1986, before a higher capital-gains rate began."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tbl[0]))
            for mk, k in zip("abc", range(1, 4)):
                vo.wait_until(mk)
                self.play(FadeIn(tbl[k], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def choice(self):
        cards = point_cards([
            (r"real responses", r"working, \ saving \\ and investing less: \\ a true cost", LOSS),
            (r"relabelling", r"the same income \\ in another form, \\ or another year", RATE),
            (r"avoidance and evasion", r"deductions, \\ shelters, \\ hiding", CAPITAL),
            (r"a policy choice", r"a broad base with \\ few escape routes \\ makes $e$ small", GAIN),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"why the elasticity is not a law of nature", font_size=28, color=E.ACCENT).to_edge(UP,
                                                                                                buff=0.6)
        tag = published_tag(tables.ETI_STUDIES.tag, corner=DR, font_size=10)
        with self.voiceover(
            "Emmanuel Saez, Joel Slemrod and Seth Giertz reviewed the whole literature in 2012, and drew a lesson "
            "that changes the question. <bookmark mark='a'/> Some of the response is real: people work, save or "
            "invest less. <bookmark mark='b'/> Some is relabelling income into a lighter-taxed form, or shifting it "
            "in time. <bookmark mark='c'/> Some is deductions, shelters and evasion. <bookmark mark='d'/> Only the "
            "first is a fixed feature of preferences. The rest depends on the tax law itself: a broad base with few "
            "escape routes makes the elasticity small, which raises the best top rate. The elasticity is partly a "
            "policy choice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
