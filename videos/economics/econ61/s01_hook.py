from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403


def clock(m: float) -> str:
    """Minutes after 11 pm as a clock label."""
    h = (23 + int(m // 60)) % 24
    return f"{12 if h % 12 == 0 else h % 12}" + (r"\,am" if h < 12 else r"\,pm")


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.night()
        self.question()
        self.title()
        self.objectives()

    def story(self):
        cards = VGroup(
            history_card(2014, r"New Year's Eve, \ New York", r"a ride-hailing app's busiest night; \ when "
                         r"requests outrun drivers, \ surge pricing raises the fare until they match",
                         color=RIDER, width=11.2, font_size=21),
            history_card(r"26 min", r"a fault switches surge pricing off", r"fares stay at the normal price; \ "
                         r"requests pile up, \ drivers do not come, \ and the app shows no cars", color=SURGE,
                         width=11.2, font_size=21),
            history_card(r"25\%", r"of requests completed during the outage", r"against nearly all of them "
                         r"after a sold-out concert at Madison Square Garden, \ with surge working", color=DRIVER,
                         width=11.2, font_size=21),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.3)
        note_ = label(r"the case study was written by the company's own economists", font_size=19,
                      color=GREY_A).next_to(cards, DOWN, buff=0.4)
        tag = published_tag(r"Hall, \ Kendrick and Nosko, \ `The Effects of Uber's Surge Pricing: \ A Case Study' "
                            r"(2015)", corner=DL, font_size=12)
        with self.voiceover(
            "New Year's Eve, 2014, in New York: one of the busiest nights of the year for a ride-hailing app. When "
            "requests outrun the drivers on the road, the app raises the fare, the surge, until the two match. "
            "<bookmark mark='a'/> That night a fault switched surge pricing off for twenty-six minutes. Fares "
            "stayed at the normal price. Requests piled up, drivers did not come, and riders opening the app saw "
            "no cars. <bookmark mark='b'/> During the outage only about a quarter of requests were completed. After "
            "a sold-out concert at Madison Square Garden, with surge working, nearly every request had been met. "
            "<bookmark mark='c'/> The comparison comes from a case study by the company's own economists, which is "
            "itself part of this part's story: firms now employ economists to design their markets, run their "
            "experiments and measure what their prices do."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.clear_scene()

    def night(self):
        N = load("night")
        on, off = N["on"], N["off"]
        t = np.array(on["t"], float)
        ax = plane([0, 120], [0, 360], center=LEFT * 2.7 + DOWN * 0.45, x_length=7.0, y_length=4.8,
                   xticks=[0, 30, 60, 90, 120], yticks=[0, 100, 200, 300], xlabel=r"the Island's night",
                   ylabel=r"rides a minute", xfmt=lambda v: clock(v) if v % 60 == 0 else "",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        dem = path(ax, t, off["demand"], WHITE, 2.2, smooth=False)
        dem_d = DashedVMobject(dem, num_dashes=60)
        drv_off = path(ax, t, off["drivers"], OFF, 3.0, smooth=False)
        gap = band(ax, t, np.array(off["drivers"]), np.array(off["demand"]), SURGE, opacity=0.25)
        req_on = path(ax, t, on["requests"], RIDER, 3.0, smooth=False)
        drv_on = path(ax, t, on["drivers"], DRIVER, 3.0, smooth=False)
        k = int(np.argmax(on["m"]))
        side = VGroup(
            label(r"white: \ requests at the normal fare", font_size=19, color=WHITE),
            label(r"surge off: \ drivers stay at their usual number", font_size=19, color=OFF),
            label(rf"red: \ requests nobody fills; \ about {100 * off['rate_peak']:.0f}\% completed", font_size=19,
                  color=SURGE),
            label(rf"surge on: \ the fare rises to {max(on['m']):.1f} times normal", font_size=19, color=RIDER),
            label(r"fewer requests, \ more drivers, \ and every request filled", font_size=19, color=DRIVER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.35)
        pk = dot(ax, t[k], on["requests"][k], RIDER, 0.07)
        tag = island_tag(r"the Island: \ agora.platform.surge\_night; \ demand and drivers' response planted",
                         corner=DL, font_size=12)
        with self.voiceover(
            "The Island has a ride-hailing app too, and a New Year's Eve. <bookmark mark='a'/> At the normal fare, "
            "requests spike at midnight to more than five times the usual rate. <bookmark mark='b'/> With surge "
            "off, the drivers on the road stay at their usual number, <bookmark mark='c'/> and everything above "
            f"that line goes unfilled: at the peak, about {100 * off['rate_peak']:.0f} percent of requests are "
            "completed. <bookmark mark='d'/> With surge on, the fare rises, to "
            f"{max(on['m']):.1f} times normal at the peak. Some riders wait, walk or share instead, <bookmark "
            "mark='e'/> while more drivers come out, a few minutes later. Every request that is made is filled. "
            "Who gains and who loses is the subject of chapter three; here, the point is what a price does when "
            "it is allowed to move."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(dem_d), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(drv_off), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(gap), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeOut(gap), Create(req_on), FadeIn(pk), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(Create(drv_on), FadeIn(side[4]), run_time=1.5)
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"how does a platform set its prices, \ its fees and its rules?", font_size=26, color=PLAT),
            label(r"what do ranking, \ ratings and ad auctions do to a market?", font_size=26, color=SELL),
            label(r"does advertising pay, \ and how would anyone know?", font_size=26, color=AD),
            label(r"how do you run an experiment when buyers share the same drivers?", font_size=26, color=TEST),
            label(r"and what is a free service worth?", font_size=26, color=RIDER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: what do the economists inside technology companies do? <bookmark mark='a'/> They help "
            "set a platform's prices, fees and rules. <bookmark mark='b'/> They study what ranking, ratings and ad "
            "auctions do to the market. <bookmark mark='c'/> They ask whether advertising pays, and how anyone "
            "could know. <bookmark mark='d'/> They design experiments in markets where every buyer shares the "
            "same drivers or rooms. <bookmark mark='e'/> And they ask what a free service is worth to the people "
            "who use it."
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        riders = VGroup(*[Dot(radius=0.09, color=RIDER) for _ in range(6)]).arrange(DOWN, buff=0.18)
        drivers = VGroup(*[Dot(radius=0.09, color=DRIVER) for _ in range(6)]).arrange(DOWN, buff=0.18)
        hub = Circle(radius=0.45, color=PLAT, stroke_width=3).set_fill(PLAT, opacity=0.25)
        net = VGroup(riders, hub, drivers).arrange(RIGHT, buff=1.6)
        lines = VGroup(*[Line(d.get_center(), hub.get_center(), stroke_width=1.4, color=GREY_B)
                         for d in list(riders) + list(drivers)])
        g = VGroup(lines, net)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 61 \ $\cdot$ \ Economics at the Platforms", font_size=34, color=E.ACCENT)
        VGroup(g, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part sixty-one: economics at the platforms."):
            self.play(FadeIn(net), Create(lines), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act XI \ $\cdot$ \ Economics at Work", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"a platform as a designed market: \ commissions, \ surge pricing, \ ranking and reputation",
            r"ad auctions with quality scores and reserves, \ and why advertising is so hard to measure",
            r"experiments at scale: \ peeking, \ variance reduction, \ and markets where units interfere",
            r"causal machine learning in production: \ uplift, \ and long-term effects from surrogates",
            r"gig work, \ the value of flexibility, \ and what free goods are worth",
        ], color=E.ACCENT, font_size=28, width=13.0)
        with self.voiceover(
            "Part sixty set one firm's prices. This part runs a marketplace. By the end you will know <bookmark "
            "mark='a'/> how a platform is designed, from its commission and surge pricing to its ranking and "
            "ratings; <bookmark mark='b'/> how ad auctions work in practice, and why the return on advertising is "
            "so hard to measure; <bookmark mark='c'/> how experiments are run at scale, and what goes wrong when "
            "units interfere; <bookmark mark='d'/> how machine learning is used to target and to forecast long-term "
            "effects; <bookmark mark='e'/> and what flexible work and free services are worth to the people who "
            "use them."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
