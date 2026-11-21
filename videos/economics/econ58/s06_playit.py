from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Play it: \ the minister's budget", r"The static score says 143 million. \ What will the "
             r"higher top rate really raise?", "Chapter five. Play it: the minister's budget.",
             lit={2001: r"Saez's formula", 2002: r"Gruber and Saez"}, scale=("person", "nation"),
             horizon=("a year",))
        self.stage()
        self.reveal()

    def stage(self):
        P = load("playit")
        edges, hist = np.array(P["edges"]) / 1000.0, np.array(P["hist"])
        ax = plane([150, 1000], [0, float(hist.max()) * 1.15], center=LEFT * 3.0 + DOWN * 0.5, x_length=6.4,
                   y_length=4.4, xticks=[150, 400, 600, 800, 1000], yticks=[], xlabel=r"income, \ thousands",
                   ylabel=r"taxpayers \ (grossed up)", xfmt=lambda v: f"{v:.0f}", font_size=15)
        bars = VGroup()
        for a, b, h in zip(edges[:-1], edges[1:], hist):
            p0, p1 = ax.ax.c2p(a, 0), ax.ax.c2p(b, h)
            bars.add(Rectangle(width=(p1[0] - p0[0]) * 0.92, height=max(p1[1] - p0[1], 0.001), fill_color=BEHAV,
                               fill_opacity=0.7, stroke_width=0).move_to((p0 + p1) / 2))
        head = label(rf"the top rate: \ {100 * P['t0']:.0f}\% $\to$ {100 * P['t1']:.0f}\% \ on income above "
                     r"150,000".replace(",", "{,}"), font_size=26, color=E.ACCENT).to_edge(UP, buff=0.45)
        side = VGroup(
            label(rf"the survey: \ {P['n_records']:,} records \ $\times$ \ weights \ $=$ \ {P['grossed']:,.0f} "
                  r"taxpayers".replace(",", "{,}"), font_size=19, color=GREY_A),
            label(rf"above 150,000: \ {P['top_people']:,.0f}, \ averaging {P['mean_top'] / 1e3:.0f} thousand"
                  .replace(",", "{,}"), font_size=19, color=BEHAV),
            MathTex(r"\text{static} = \sum_i w_i \times 0.05 \times (z_i - 150{,}000)", font_size=26, color=STATIC),
            label(rf"static score: \ {P['static']:.0f} million a year", font_size=24, color=STATIC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(UP * 0.4)
        tag = island_tag(r"the Island: \ 400,000 taxpayers, \ a survey of one in ten \ (one in two at the top)"
                         .replace(",", "{,}"), corner=DL, font_size=12)
        with self.voiceover(
            "Your turn. The Island's minister of finance wants to raise the top rate of income tax from forty to "
            "forty-five percent, on income above a hundred and fifty thousand. You are the scorer. <bookmark "
            f"mark='a'/> Your data are a survey: {P['n_records']:,} records, each with a weight saying how many "
            f"taxpayers it stands for, which gross it up to the Island's {P['grossed']:,.0f}. The survey takes one "
            "taxpayer in ten, but one in two at the top, where the money is. <bookmark mark='b'/> About ten thousand "
            "people have income above the threshold, and their incomes have a long Pareto tail. <bookmark "
            "mark='c'/> The static score is arithmetic: five percent of everyone's income above the threshold, "
            f"added up: {P['static']:.0f} million a year. <bookmark mark='d'/> But taxpayers respond. Part "
            "forty-one's dial puts the elasticity of taxable income at about a quarter. What will the higher rate "
            "really raise?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ax))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(bars, color=WHITE, scale_factor=1.0))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("d")
        opts = VGroup(*[label(t_, font_size=24, color=c_) for t_, c_ in (
            (r"A \ \ about 143 million: \ the static score", STATIC), (r"B \ \ about 100 million", BEHAV),
            (r"C \ \ about 60 million", DYN), (r"D \ \ nothing: \ the rich move it all away", COST))])
        opts.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
        self.play(FadeOut(side), FadeIn(opts, shift=UP * 0.1))
        ring = countdown().scale(0.6).next_to(opts, UP, buff=0.4)
        self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=7.0, rate_func=linear)
        self.play(FadeOut(ring), Indicate(opts[1], color=WHITE, scale_factor=1.1))
        self.wait(0.5)
        self.clear_scene()

    def reveal(self):
        P = load("playit")
        es, ratio = np.array(P["es"]), np.array(P["ratios"])
        ax = plane([0, 1.0], [-0.2, 1.05], center=LEFT * 2.8 + DOWN * 0.4, x_length=6.2, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"elasticity of taxable income", ylabel=r"revenue with behaviour \ $\div$ \ static",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=15)
        curve = path(ax, es, ratio, BEHAV, 3.0, smooth=True)
        zero = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(1.0, 0), color=GREY_C, stroke_width=1.2)
        formula = path(ax, es, 1 - es * 1.5 * P["t1"] / (1 - P["t1"]), WHITE, 1.8, smooth=False).set_stroke(
            opacity=0.6)
        d = dot(ax, P["e"], P["ratio"], BEHAV, 0.1)
        side = VGroup(
            label(rf"incomes above 150,000 fall by {100 * (1 - ((1 - P['t1']) / (1 - P['t0'])) ** P['e']):.1f}\%, \\ "
                  r"\ \ and the 40\% on what is lost goes too".replace(",", "{,}"), font_size=20, color=GREY_A),
            label(rf"with behaviour: \ {P['behavioural']:.0f} million \ ({100 * P['ratio']:.0f}\% of static)",
                  font_size=24, color=BEHAV),
            MathTex(r"\frac{\text{revenue}}{\text{static}} \approx 1 - e\,a\,\frac{\tau}{1 - \tau}"
                    rf"= 1 - 0.25 \times 1.5 \times \tfrac{{0.45}}{{0.55}} = {P['formula']:.2f}", font_size=26,
                    color=WHITE),
            label(r"Saez (2001): \ $a$ is the Pareto exponent of the top tail", font_size=18, color=GREY_B),
            label(rf"B was right; \ C needs an elasticity near {P['e_c']:.1f}", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"the Island: \ the grossed-up survey; \ white: \ Saez's formula", corner=DL, font_size=12)
        one = DashedLine(ax.ax.c2p(0, 1), ax.ax.c2p(1.0, 1), color=STATIC, stroke_width=1.6)
        onel = label(rf"the static score, \ {P['static']:.0f}", font_size=17, color=STATIC).next_to(
            ax.ax.c2p(0.5, 1), UP, buff=0.08)
        with self.voiceover(
            "Here is what happened in the Island's model. <bookmark mark='a'/> With an elasticity of a quarter, "
            f"incomes in the top band fall by about {100 * (1 - ((1 - P['t1']) / (1 - P['t0'])) ** P['e']):.1f} "
            "percent: some effort, some deferral, some income moved into forms the tax does not reach. On every "
            "dollar that disappears, the forty percent that was already being collected goes too. <bookmark "
            f"mark='b'/> The higher rate raises {P['behavioural']:.0f} million, about {100 * P['ratio']:.0f} percent "
            "of the static score. <bookmark mark='c'/> Emmanuel Saez gave the shortcut in 2001: the ratio is about "
            "one minus the elasticity times the Pareto exponent times the tax rate over one minus the tax rate. "
            f"Here, {P['formula']:.2f}. <bookmark mark='d'/> The answer moves with the elasticity: at nought, the "
            f"static score is right; at about {say_num(P['e_c'], 1)}, the rise raises sixty million; at about "
            f"{say_num(P['e_zero'], 1)}, nothing, and beyond that the top of Laffer's curve is passed. <bookmark "
            "mark='e'/> So B. A score that ignores behaviour overstates what tax "
            "rises raise and what tax cuts cost, and the size of the error is the dial."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), Create(one), FadeIn(onel))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(d, scale=1.5), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]), Create(formula))
            vo.wait_until("d")
            self.play(Create(curve), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
