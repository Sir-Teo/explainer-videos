from __future__ import annotations

from scipy import optimize

from videos.economics.econ61.common import *  # noqa: F403


class Surge(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Surge pricing", r"Who gains when the fare rises with the queue, \ and how would you measure "
             r"it?", "Chapter three. Surge pricing.",
             lit={2014: r"the emergency cap", 2016: r"Cohen et al."}, scale=("person", "market"),
             horizon=("a day",))
        self.clearing()
        self.surplus()
        self.limits()

    def clearing(self):
        N = load("night")
        P = N["params"]
        peak = P["base_demand"] + P["spike"]
        beta, d0, sl = P["beta"], P["drivers0"], P["supply_slope"]
        dem = (lambda m: peak * np.exp(-beta * (m - 1.0)))
        sup = (lambda m: d0 + sl * (m - 1.0))
        m_star = optimize.brentq(lambda m: dem(m) - sup(m), 1.0, 5.0)
        ms = np.linspace(1.0, 3.6, 80)
        ax = plane([0, 360], [0.8, 3.6], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.2, y_length=4.6,
                   xticks=[0, 100, 200, 300], yticks=[1, 2, 3], xlabel=r"rides a minute, \ at midnight",
                   ylabel=r"the fare, \ times normal", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}x",
                   font_size=14)
        dc = path(ax, dem(ms), ms, RIDER, 3.0)
        sc = path(ax, sup(ms), ms, DRIVER, 3.0)
        one = seg(ax, 0, 1.0, 360, 1.0, GREY_B, 1.4, dashed=True)
        short = Line(ax.ax.c2p(sup(1.0), 1.0), ax.ax.c2p(dem(1.0), 1.0), color=SURGE, stroke_width=7)
        eq = dot(ax, sup(m_star), m_star, WHITE, 0.08)
        eql = seg(ax, 0, m_star, sup(m_star), m_star, WHITE, 1.4, dashed=True)
        side = VGroup(
            label(r"blue: \ riders' requests, \ falling with the fare", font_size=19, color=RIDER),
            label(r"gold: \ drivers on the road, \ rising with it", font_size=19, color=DRIVER),
            label(rf"at the normal fare: \ {dem(1.0):.0f} requests, \ {sup(1.0):.0f} drivers", font_size=19,
                  color=SURGE),
            label(rf"the fare that clears the market: \ {m_star:.1f} times normal", font_size=19, color=WHITE),
            label(rf"rides at that fare: \ {sup(m_star):.0f} a minute, \ against {sup(1.0):.0f}", font_size=19,
                  color=GAIN),
            label(r"the app's multiplier runs higher at first: \\ drivers take minutes to arrive", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ the peak minute; \ demand and supply from agora.platform.NIGHT", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Surge pricing is the oldest idea in this series: a price that clears the market. Take the Island's "
            "peak minute. <bookmark mark='a'/> Riders' requests fall as the fare rises, <bookmark mark='b'/> and "
            "the number of drivers on the road rises with it. <bookmark mark='c'/> At the normal fare, "
            f"{dem(1.0):.0f} requests meet {sup(1.0):.0f} drivers, and the shortage is rationed by luck and by "
            f"waiting. <bookmark mark='d'/> The fare that clears the market is {m_star:.1f} times normal. <bookmark "
            f"mark='e'/> At that fare there are {sup(m_star):.0f} rides a minute, not {sup(1.0):.0f}: more rides, "
            "not fewer, because the higher fare brings out drivers who would otherwise have stayed at home. "
            "<bookmark mark='f'/> The app's own multiplier runs above the static answer for the first minutes of "
            "a spike, because drivers take time to arrive; surge is a price that has to anticipate its own supply."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(one))
            vo.wait_until("a")
            self.play(Create(dc), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(sc), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(short), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(eq), Create(eql), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def surplus(self):
        S = load("surplus")
        mu = S["mu_hat"]
        levels = np.array(S["levels"])
        fares = 15.0 * levels
        xs = np.linspace(10, 70, 120)
        ax = plane([10, 70], [0, 0.7], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.2, y_length=4.6,
                   xticks=[15, 30, 45, 60], yticks=[0, 0.2, 0.4, 0.6], xlabel=r"the fare shown, \ \$",
                   ylabel=r"share of sessions that book", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        dots = VGroup(*[dot(ax, f, r, RIDER, 0.08) for f, r in zip(fares, S["rates"])])
        curve = path(ax, xs, np.exp(-xs / mu), WHITE, 2.6)
        xx = np.linspace(15, 70, 80)
        area = band(ax, xx, np.zeros_like(xx), np.exp(-xx / mu), GAIN, opacity=0.3)
        side = VGroup(
            label(r"riders who opened the app at random surge levels", font_size=19, color=RIDER),
            label(rf"the fitted demand curve: \ $e^{{-p/{mu:.1f}}}$", font_size=19, color=WHITE),
            label(r"green: \ consumer surplus at the normal fare, \ \$15", font_size=19, color=GAIN),
            label(rf"the Island: \ \${S['cs_per_dollar']:.2f} of surplus per dollar spent", font_size=21,
                  color=GAIN),
            label(r"Cohen et al. \ (2016), \ UberX in four cities: \ about \$1.60 per dollar; \\ elasticities "
                  r"mostly between {-}0.4 and {-}0.6", font_size=18, color=GREY_A),
            label(r"identification: \ the surge's rounding thresholds, \ a regression discontinuity; \\ two of the "
                  r"authors worked for the company", font_size=17, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Cohen, \ Hahn, \ Hall, \ Levitt and Metcalfe, \ NBER Working Paper 22627 (2016); \ "
                            r"the Island: \ agora.platform.surge\_surplus", corner=DL, font_size=12)
        with self.voiceover(
            "Surge also does something for the economist: it varies the price, many times a day, for reasons "
            "riders cannot see. <bookmark mark='a'/> Here are the Island's riders who opened the app when the "
            "surge happened to be at each level, and the share who booked. <bookmark mark='b'/> Those points "
            "trace out the demand curve. <bookmark mark='c'/> The area under it, above the fare, is what riders "
            "would have paid and did not have to: consumer surplus. <bookmark mark='d'/> On the Island it comes "
            f"to {S['cs_per_dollar']:.2f} dollars for every dollar spent. <bookmark mark='e'/> Cohen, Hahn, Hall, "
            "Levitt and Metcalfe did this with almost fifty million sessions in four American cities in 2015. "
            "They found demand inelastic, with elasticities mostly between minus 0.4 and minus 0.6, and about a "
            "dollar sixty of consumer surplus for every dollar spent. <bookmark mark='f'/> Their variation came "
            "from the surge algorithm's rounding: sessions just above and just below a threshold saw different "
            "prices for the same conditions, a regression discontinuity. Two of the authors worked for the "
            "company, which supplied the data; the design is what makes the number worth taking seriously."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.15), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curve), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(area), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def limits(self):
        cards = point_cards([
            (r"who gains", r"riders who would pay more get a car; \ drivers earn more on the busiest nights; \ riders "
             r"who would not are priced out instead of waiting", RIDER),
            (r"why it angers", r"a price that jumps when you most need it feels like exploitation \ (Part 45's "
             r"fairness norms)", SURGE),
            (r"the emergency cap", r"2014: \ in emergencies, \ fares in New York capped at the range of the past 60 "
                                   r"days, \ less the three highest days", HOLD),
            (r"what it does not fix", r"if drivers cannot get there in time, \ a higher fare only rations the cars "
                                      r"that are already on the road", GREY_A),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"what surge does, \ and why people hate it", font_size=30, color=E.ACCENT).to_edge(UP,
                                                                                                    buff=0.5)
        tag = published_tag(r"New York Attorney General's agreement with Uber, \ 8 July 2014; \ Part 45", corner=DL,
                            font_size=12)
        with self.voiceover(
            "So who gains? <bookmark mark='a'/> Riders who would pay more get a car; drivers earn more on the "
            "busiest nights; riders who would not pay the higher fare are priced out, where without surge they "
            "would have waited, mostly in vain. <bookmark mark='b'/> And yet surge is widely hated. A price that "
            "jumps when you most need the service feels like exploitation; Part forty-five's fairness norms are "
            "real constraints on what firms can charge. <bookmark mark='c'/> In July 2014 the company agreed with "
            "New York's attorney general that in emergencies, from storms to power failures, fares would be "
            "capped at the range of the previous sixty days, leaving out the three highest days. <bookmark "
            "mark='d'/> And surge cannot conjure drivers who are too far away to arrive in time: in the first "
            "minutes of a spike, a higher fare only decides which riders get the cars already on the road."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
