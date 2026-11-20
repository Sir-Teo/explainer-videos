from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


class Keynes(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Keynes: \ effective demand and the multiplier", r"If spending sets output, \ what sets "
             r"spending?", "Chapter four. Keynes: effective demand and the multiplier.",
             lit={1931: r"Kahn", 1936: r"\emph{The General Theory}"}, scale=("nation",), horizon=("a year",))
        self.book()
        self.cross()
        self.rounds()

    def book(self):
        C = load("cross")
        rows = VGroup(
            label(r"Keynes, \ \emph{The General Theory of Employment, Interest and Money}, \ 1936", font_size=24,
                  color=E.ACCENT),
            label(r"effective demand: \ firms produce what they expect to sell", font_size=24, color=OUTPUT),
            label(r"so output, \ and employment, \ are set by planned spending", font_size=24, color=SPEND),
            label(rf"consumption rises with income, \ but by less: \ $C = a + b\,(Y - T)$, \ with $b = {C['b']}$ "
                  r"on the Island", font_size=23, color=SPEND),
            label(r"$b$: \ the marginal propensity to consume", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Keynes, \emph{The General Theory} (1936), \ chs.\ 3, 8--10", corner=DR, font_size=12)
        with self.voiceover(
            "In 1936 John Maynard Keynes published The General Theory of Employment, Interest and Money. "
            "<bookmark mark='a'/> Its starting point is effective demand. Firms produce what they expect to sell, "
            "and hire the workers they need to produce it. <bookmark mark='b'/> So output, and with it employment, "
            "are set by planned spending, not by how many people want to work. <bookmark mark='c'/> The biggest "
            "part of spending is households' consumption, and Keynes proposed that it rises with income, but by "
            f"less than income does. On the Island, consumption is two hundred plus {C['b']} times income after "
            f"taxes. <bookmark mark='d'/> That {C['b']} is the marginal propensity to consume: the share of an "
            "extra dollar of income that is spent."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def cross(self):
        C = load("cross")
        b0, b1 = C["base"], C["up"]
        ax = plane([0, 2200], [0, 2200], center=LEFT * 2.3 + DOWN * 0.3, x_length=5.4, y_length=5.0,
                   xticks=[0, 500, 1000, 1500, 2000], yticks=[0, 500, 1000, 1500, 2000], xlabel=r"income $Y$",
                   ylabel=r"planned spending $E$", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=15)
        diag = seg(ax, 0, 0, 2200, 2200, color=GREY_B, width=2, dashed=True)
        auto0 = C["a"] - C["b"] * C["T"] + C["I"] + C["G"]
        e0 = seg(ax, 0, auto0, 2200, auto0 + C["b"] * 2200, color=SPEND, width=4)
        e1 = seg(ax, 0, auto0 + C["dG"], 2200, auto0 + C["dG"] + C["b"] * 2200, color=GOV, width=4)
        d0 = dot(ax, b0["Y"], b0["Y"], color=OUTPUT, r=0.09)
        d1 = dot(ax, b1["Y"], b1["Y"], color=GOV, r=0.09)
        side = VGroup(
            label(r"$E = C + I + G$", font_size=26, color=SPEND),
            label(r"dashed: \ $E = Y$, \ where what is spent \\ is what is produced", font_size=20, color=GREY_B),
            label(rf"equilibrium: \ $Y = {b0['Y']:.0f}$", font_size=22, color=OUTPUT),
            label(r"$Y = \dfrac{a - bT + I + G}{1 - b}$", font_size=26, color=WHITE),
            label(rf"raise $G$ by {C['dG']:.0f}: \ $Y = {b1['Y']:.0f}$", font_size=22, color=GOV),
            label(rf"a multiplier of $1/(1-b) = {b0['multiplier']:.1f}$", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Keynesian cross puts it in one picture. <bookmark mark='a'/> Planned spending is consumption, plus "
            "investment, plus the government's purchases. It rises with income, because consumption does. "
            "<bookmark mark='b'/> The dashed line is where spending equals income: what is bought equals what is "
            "produced. <bookmark mark='c'/> The economy settles where the two cross. On the Island, at an income of "
            f"{b0['Y']:,.0f}. If firms produced more, it would go unsold and they would cut back; if less, their "
            "shelves would empty and they would produce more. <bookmark mark='d'/> Solving, income is everything "
            "spent regardless of income, divided by one minus the propensity to consume. "
            f"<bookmark mark='e'/> Now let the government buy {C['dG']:.0f} more. Income rises to "
            f"{b1['Y']:,.0f}: <bookmark mark='f'/> by {b1['Y'] - b0['Y']:.0f}, two and a half times the extra "
            "spending. That ratio is the multiplier."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(e0), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(diag), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromCenter(d0), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(e1), GrowFromCenter(d1), FadeIn(side[4]), run_time=1.2)
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def rounds(self):
        C = load("cross")
        R = C["rounds"]
        n = 10
        bars = VGroup()
        w = 0.9
        for k in range(n):
            h = 3.0 * R["adds"][k] / R["adds"][0]
            bars.add(Rectangle(width=w, height=max(h, 0.02), fill_color=GOV if k == 0 else SPEND, fill_opacity=0.8,
                               stroke_width=0))
        bars.arrange(RIGHT, buff=0.15, aligned_edge=DOWN).move_to(LEFT * 1.2 + DOWN * 0.9)
        intro = label(r"the government spends 100 on a bridge: \ follow the money round", font_size=24,
                      color=GOV).next_to(bars, UP, buff=0.4).align_to(bars, LEFT)
        labels_ = VGroup(*[label(f"{R['adds'][k]:.0f}" if R["adds"][k] >= 1 else f"{R['adds'][k]:.1f}",
                                 font_size=16, color=GREY_A).next_to(bars[k], UP, buff=0.08) for k in range(n)])
        run = DecimalNumber(0, num_decimal_places=0, font_size=40, color=E.ACCENT).to_edge(RIGHT, buff=1.4).shift(
            UP * 1.2)
        run_lab = label(r"total so far", font_size=20, color=GREY_A).next_to(run, UP, buff=0.15)
        side = VGroup(
            MathTex(r"100\,(1 + b + b^2 + b^3 + \cdots) = \frac{100}{1-b}", font_size=36, color=WHITE),
            label(rf"$= {R['limit']:.0f}$ \ with $b = {C['b']}$", font_size=24, color=E.ACCENT),
            label(r"Richard Kahn, \ 1931: \ the multiplier", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.6)
        tag = published_tag(r"Kahn, \ ``The relation of home investment to unemployment'', \ Economic Journal "
                            r"41(162) (1931): \ 173--198", corner=DR, font_size=12)
        with self.voiceover(
            "Where does the multiplier come from? Follow the money. <bookmark mark='a'/> The government spends a "
            "hundred, on a bridge. That is a hundred of income for the builders. <bookmark mark='b'/> They spend "
            f"{C['b']} of it, sixty, in the shops: sixty more income for the shopkeepers. <bookmark mark='c'/> They "
            "spend thirty-six of that, and so on, each round smaller than the last. <bookmark mark='d'/> Add up the "
            "rounds and you get a geometric series: a hundred times one plus b plus b squared and so on, which is a "
            f"hundred divided by one minus b. With b at {C['b']}, that is {R['limit']:.0f}. "
            "<bookmark mark='e'/> Richard Kahn, Keynes's student, worked this out in 1931 for public works and "
            "jobs. Notice what makes it big: a high propensity to consume, and nothing else leaking out of the "
            "circle, into taxes, imports or higher interest rates. The next chapters add the leaks."
        ) as vo:
            self.add(run_lab, run)
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(labels_[0]), FadeIn(tag),
                      run.animate.set_value(R["cumulative"][0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(labels_[1]), run.animate.set_value(R["cumulative"][1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[k], DOWN), FadeIn(labels_[k]))
                                    for k in range(2, n)], lag_ratio=0.4),
                      run.animate.set_value(R["cumulative"][n - 1]), run_time=3)
            vo.wait_until("d")
            self.play(FadeOut(intro), FadeIn(side[0]), FadeIn(side[1]), run.animate.set_value(R["limit"]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.clear_scene()
