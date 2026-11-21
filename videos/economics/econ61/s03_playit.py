from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403

OPTIONS = ("0.1", "0.2", "0.3", "0.45")
NAMES = ("A", "B", "C", "D")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ set the commission", r"Which commission earns the platform the most?",
             "Chapter two. Play it: set the commission.", scale=("firm", "market"), horizon=("a day",))
        self.stage()
        self.reveal()
        self.both_sides()

    def stage(self):
        C = load("commission")
        P = C["params"]
        chain = flow_chain([(r"a higher commission", PLAT), (r"lower pay per trip", DRIVER),
                            (r"fewer drivers", DRIVER), (r"longer waits", SURGE), (r"fewer riders", RIDER)],
                           box_w=2.2, box_h=0.95, buff=0.42, font_size=19).scale(0.95).to_edge(UP, buff=0.55)
        facts = VGroup(
            label(rf"the fare: \ \${P['fare']:.0f} a trip, \ set by the platform and fixed here", font_size=20,
                  color=WHITE),
            label(rf"drivers drive when their hourly pay beats their other work, \ about \${P['w0']:.0f} an hour",
                  font_size=20, color=DRIVER),
            label(r"riders ride when the wait is short; \ the wait grows as drivers get busy", font_size=20,
                  color=RIDER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(chain, DOWN, buff=0.45)
        opts = VGroup(*[label(rf"{n} \ \ {100 * float(c):.0f}\%", font_size=28, color=PLAT)
                        for n, c in zip(NAMES, OPTIONS)]).arrange(RIGHT, buff=1.0).next_to(facts, DOWN, buff=0.5)
        tag = island_tag(r"the Island: \ agora.platform.commission; \ riders' and drivers' choices planted",
                         corner=DL, font_size=12)
        with self.voiceover(
            "Your turn. You run the Island's ride-hailing app, and you choose one number: the commission, the "
            "share of each fare the platform keeps. <bookmark mark='a'/> The fare is twenty dollars a trip, and "
            "here it is fixed. Drivers drive when their pay for an hour beats their other work, about twenty "
            "dollars an hour; riders ride when the wait is short, and the wait grows as drivers get busy. "
            "<bookmark mark='b'/> So the commission works through both sides: a higher commission means lower "
            "pay per trip, fewer drivers, longer waits, and fewer riders. <bookmark mark='c'/> Ten percent, twenty, "
            "thirty, or forty-five: which earns the platform the most?"
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in chain.boxes], lag_ratio=0.3),
                      LaggedStart(*[GrowArrow(a) for a in chain.arrows], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.1) for o in opts], lag_ratio=0.2))
        ring = countdown().scale(0.6).next_to(opts, DOWN, buff=0.4)
        self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=7.0, rate_func=linear)
        self.play(FadeOut(ring), Indicate(opts[2], color=WHITE, scale_factor=1.1))
        self.wait(0.5)
        self.clear_scene()

    def reveal(self):
        C = load("commission")
        O = C["options"]
        top = max(O[c]["platform"] for c in OPTIONS) * 1.25
        ax = plane([-0.6, 3.6], [0, top], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.0, y_length=4.6, xticks=[],
                   yticks=[0, 200, 400, 600], ylabel=r"the platform's take, \ \$ an hour",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        cols = (GREY_B, GREY_B, PLAT, GREY_B)
        b = bars(ax, range(4), [O[c]["platform"] for c in OPTIONS], cols, width=0.55)
        labs = VGroup(*[label(rf"{n}: \ {100 * float(c):.0f}\%", font_size=16, color=PLAT).next_to(
            ax.ax.c2p(k, 0), DOWN, buff=0.12) for k, (n, c) in enumerate(zip(NAMES, OPTIONS))])
        vals = VGroup(*[label(rf"\${O[c]['platform']:.0f}", font_size=15, color=WHITE).next_to(x, UP, buff=0.06)
                        for c, x in zip(OPTIONS, b)])
        rows = VGroup(*[label(rf"{n}: \ {O[c]['trips']:.0f} trips, \ {O[c]['drivers']:.0f} drivers, \ waits of "
                              rf"{O[c]['wait']:.1f} min", font_size=18, color=PLAT if n == "C" else GREY_A)
                        for n, c in zip(NAMES, OPTIONS)]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        side = VGroup(
            rows,
            label(rf"the platform's best: \ {100 * C['best_c']:.0f}\%", font_size=22, color=PLAT),
            label(r"below it, \ more trips but too little kept from each; \\ above it, \ too few drivers, \ too "
                  r"long a wait", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ each commission's equilibrium of riders and drivers", corner=DL,
                         font_size=12)
        O1, O3, O45 = O["0.1"], O["0.3"], O["0.45"]
        with self.voiceover(
            "Here is each commission's equilibrium, where the drivers who choose to drive and the riders who "
            "choose to ride are consistent with each other's choices. <bookmark mark='a'/> At ten percent, "
            f"{O1['trips']:.0f} trips an hour, but the platform keeps only {O1['platform']:.0f} dollars. <bookmark "
            f"mark='b'/> At twenty, {O['0.2']['platform']:.0f}. <bookmark mark='c'/> At thirty, "
            f"{O3['platform']:.0f}, the most of the four, from {O3['trips']:.0f} trips. <bookmark mark='d'/> At "
            f"forty-five percent the take falls back, to {O45['platform']:.0f}: drivers' pay is so low that only "
            f"{O45['drivers']:.0f} drive, waits stretch to {O45['wait']:.0f} minutes, and riders give up. So C. "
            f"The platform's best commission on a fine grid is {100 * C['best_c']:.0f} percent. Below it, trips "
            "are many but too little is kept from each; above it, there are too few drivers and too long a wait."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[k], DOWN), FadeIn(vals[k]), FadeIn(rows[k]))
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.clear_scene()

    def both_sides(self):
        C = load("commission")
        cs = np.array(C["c"])
        top = max(C["rider_cs"]) * 1.1
        ax = plane([0, 0.6], [0, top], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.0, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[0, 1000, 2000, 3000],
                   xlabel=r"the commission", ylabel=r"\$ an hour", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), font_size=14)
        pr = path(ax, cs, C["rider_cs"], RIDER, 3.0)
        pd = path(ax, cs, C["driver_surplus"], DRIVER, 3.0)
        pp = path(ax, cs, C["platform"], PLAT, 3.0)
        k = int(np.argmax(C["platform"]))
        mark = vline(ax, cs[k], 0, top * 0.9, PLAT, 1.6)
        i10, i30 = int(np.argmin(abs(cs - 0.1))), int(np.argmin(abs(cs - 0.3)))
        lost = C["rider_cs"][i10] + C["driver_surplus"][i10] - C["rider_cs"][i30] - C["driver_surplus"][i30]
        gain = C["platform"][i30] - C["platform"][i10]
        side = VGroup(
            label(r"blue: \ riders' surplus", font_size=20, color=RIDER),
            label(r"gold: \ drivers' surplus", font_size=20, color=DRIVER),
            label(r"purple: \ the platform's take", font_size=20, color=PLAT),
            label(rf"from 10\% to 30\%: \ the platform gains \${gain:.0f}, \\ riders and drivers lose \${lost:,.0f}"
                  .replace(",", "{,}"), font_size=19, color=WHITE),
            label(r"each driver who leaves lengthens every rider's wait: \\ a cross-side effect the commission "
                  r"ignores", font_size=19, color=GREY_A),
            label(r"competition between platforms, \ and drivers on several apps, \\ limit how far a commission "
                  r"can rise", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ surplus by logit inclusive values, \ in dollars an hour", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Now look at everyone, not just the platform. <bookmark mark='a'/> Riders' surplus, in dollars an "
            "hour, <bookmark mark='b'/> drivers' surplus, <bookmark mark='c'/> and the platform's take, peaking "
            f"at {100 * C['best_c']:.0f} percent. <bookmark mark='d'/> Moving from ten percent to thirty, the "
            f"platform gains {gain:.0f} dollars an hour, and riders and drivers together lose {lost:,.0f}. "
            "<bookmark mark='e'/> The loss is so much larger because of a cross-side effect: each driver who stops "
            "driving lengthens every rider's wait, and the commission, chosen for the platform's take alone, "
            "ignores it. This is Part forty-four's two-sided market with numbers in it. <bookmark mark='f'/> What "
            "keeps commissions down in practice is competition: between platforms, and from drivers and riders "
            "who keep two apps on their phones."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(pr), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(pd), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(pp), Create(mark), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()
