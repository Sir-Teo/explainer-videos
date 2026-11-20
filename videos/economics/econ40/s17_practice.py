from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ distributional analysis", r"Who gains and who loses from a policy?",
             "Chapter fifteen. In practice: distributional analysis.", lit={}, scale=("household", "nation"),
             horizon=("a year",))
        self.table()
        self.choices()
        self.precision()

    def table(self):
        P = load("practice")
        rel = np.array(P["rel"])
        ax = plane([0.5, 10.5], [-0.2, 0.8], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.8,
                   xticks=list(range(1, 11)), yticks=[-0.2, 0, 0.2, 0.4, 0.6, 0.8],
                   xlabel=r"decile of pre-tax income", ylabel=r"net gain, \ percent of pre-tax income",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:+.0f}\\%", font_size=14)
        zero = seg(ax, 0.5, 0, 10.5, 0, GREY_B, 1.5)
        bars = VGroup()
        for k, v in enumerate(rel):
            x = k + 1
            p0, p1 = ax.ax.c2p(x - 0.35, 0), ax.ax.c2p(x + 0.35, v)
            col = GAIN if v > 0 else LOSS
            r = Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(f"{100 * v:+.0f}\\%", font_size=14, color=col).next_to(
                r, UP if v > 0 else DOWN, buff=0.06)))
        cross = next(k for k, v in enumerate(rel) if v < 0) + 1
        side = VGroup(
            label(rf"a flat tax of {100 * P['tax']:.0f}\% \\ on every income, \\ paid back as \\ "
                  rf"\${P['transfer']:,.0f} "
                  r"each", font_size=18, color=WHITE),
            label(rf"deciles 1--{cross - 1} gain; \\ {cross}--10 pay", font_size=19, color=GAIN),
            label(rf"Gini: \ {P['gini_pre']:.3f} $\to$ {P['gini_post']:.3f}", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        head = label(r"a distributional table: \ who gains, \ who pays, \ decile by decile", font_size=22,
                     color=E.ACCENT).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Budget offices, treasuries and research institutes publish distributional tables for major tax and "
            "benefit changes: who gains and who loses, decile by decile. Here is one for the Island. "
            "<bookmark mark='a'/> A flat tax of "
            f"{100 * P['tax']:.0f} percent on every income, with the revenue paid back equally, "
            f"{P['transfer']:,.0f} dollars a head. <bookmark mark='b'/> Rank people by pre-tax income and compute each "
            f"decile's net gain. The poorest tenth gains {100 * rel[0]:.0f} percent of its income; "
            f"<bookmark mark='c'/> deciles {cross} to ten pay, the top tenth {say_pct(-rel[-1], 0)} of its income. "
            f"<bookmark mark='d'/> The Gini falls from {P['gini_pre']:.2f} to {P['gini_post']:.2f}. A flat tax with "
            "an equal grant is progressive: what matters is the whole system, not one rate."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(head), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars[:cross - 1]],
                                                   lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(bars[0], color=WHITE))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_, shift=DOWN * 0.1) for b_ in bars[cross - 1:]], lag_ratio=0.2),
                      FadeIn(side[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def choices(self):
        steps = flow_chain([(r"the unit", BOTTOM), (r"the income", TOP), (r"the ranking", MIDDLE),
                            (r"the measures", LORENZ)],
                           notes=[r"person, \ household \\ or tax unit; \\ equivalence scales", r"market, \ pre-tax "
                                  r"\\ or disposable; \\ capital gains?", r"by income before \\ or after the "
                                  r"policy", r"several, \ each \\ with a standard \\ error"],
                           box_w=2.6, font_size=20, note_size=15).move_to(UP * 0.6)
        warn = label(r"every top share and every Gini in this part rests on these four choices", font_size=20,
                     color=E.ACCENT).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Every such table rests on four choices, and readers should look for each. <bookmark mark='a'/> The "
            "unit: a person, a household or a tax unit, and how a family's needs are scaled to its size. "
            "<bookmark mark='b'/> The income: market income, pre-tax, or disposable, and whether capital gains and "
            "untaxed income count, the heart of chapter three's dispute. <bookmark mark='c'/> The ranking: by "
            "income before the policy or after it. <bookmark mark='d'/> And the measures: several, since they watch "
            "different parts of the distribution, each with its uncertainty."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(steps.arrows[0]), FadeIn(steps.boxes[1]), FadeIn(steps.notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(steps.arrows[1]), FadeIn(steps.boxes[2]), FadeIn(steps.notes[2]))
            vo.wait_until("d")
            self.play(GrowArrow(steps.arrows[2]), FadeIn(steps.boxes[3]), FadeIn(steps.notes[3]), FadeIn(warn))
        self.clear_scene()

    def precision(self):
        P = load("practice")
        rows = [(rf"Gini, \ {P['n']:,} people", P["gini"], "{:.3f}", 1.0),
                (r"Gini, \ 200 people", P["gini_small"], "{:.3f}", 1.0),
                (rf"top 1\% share, \ {P['n']:,} people", P["top1"], "{:.1f}\\%", 100.0),
                (r"top 1\% share, \ 200 people", P["top1_small"], "{:.1f}\\%", 100.0)]
        lines = VGroup()
        for k, (nm, v, fmt, sc) in enumerate(rows):
            y = 1.4 - 0.95 * k
            lo, hi = v["value"] - 1.96 * v["se"], v["value"] + 1.96 * v["se"]
            lines.add(VGroup(
                label(nm, font_size=21, color=WHITE).next_to(np.array([-0.6, y, 0]), LEFT, buff=0.2),
                label((fmt.format(sc * v["value"])) + rf" \ (95\%: \ {fmt.format(sc * lo)} to {fmt.format(sc * hi)})",
                      font_size=21, color=E.ACCENT if k % 2 else MIDDLE).next_to(np.array([-0.4, y, 0]), RIGHT,
                                                                                 buff=0.1)))
        head = label(r"a sample is not the population", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"the top of a distribution is where samples are thinnest: \ tax records, \ not surveys, \ for "
                     r"top shares", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "And every number from a sample comes with uncertainty, largest at the top. <bookmark mark='a'/> With "
            f"{P['n']:,} of the Island's people, the Gini is {P['gini']['value']:.2f}, give or take two "
            f"hundredths. <bookmark mark='b'/> With two hundred, the interval is twice as wide. <bookmark mark='c'/> "
            "The top one percent's share is harder: from two thousand people, twenty in the top percent, the "
            "interval spans several points; <bookmark mark='d'/> from two hundred, two people in the top percent, "
            "it is too wide to be useful. That is why top shares come from tax records, which cover everyone who files."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, l_ in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l_, shift=RIGHT * 0.1))
            self.play(FadeIn(foot))
        self.clear_scene()
