from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403

CORR_NAMES = {"frac_black": r"share of Black residents", "single_mothers": r"children with single mothers",
              "gini99": r"inequality, \ bottom 99\%", "racial_seg": r"racial segregation",
              "income_seg": r"income segregation", "test_scores": r"test scores", "school_spend": r"school spending",
              "foreign": r"foreign-born share", "middle": r"middle-class share", "social_capital": r"social capital",
              "commute15": r"short commutes", "religious": r"religious share"}


class Places(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Places", r"Where in America do poor children rise, \ and is it the place?",
             "Chapter ten. Places.", lit={2014: r"Chetty et al.", 2016: r"Moving to Opportunity",
                                          2018: r"Chetty and Hendren"},
             scale=("city", "nation"), horizon=("a decade",))
        self.spread()
        self.cities()
        self.correlates()
        self.causal()

    def spread(self):
        P = load("places")
        am = np.array(P["am"])
        pop = np.array(P["pop"])
        edges = np.arange(25, 67, 2.0)
        h, _ = np.histogram(am, bins=edges, weights=pop)
        h = h / h.sum()
        ax = plane([25, 65], [0, 0.35], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[30, 40, 50, 60], yticks=[0, 0.1, 0.2, 0.3],
                   xlabel=r"upward mobility: \ the expected rank of a child from the 25th percentile",
                   ylabel=r"share of Americans", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        bars = VGroup()
        for a, b, v in zip(edges[:-1], edges[1:], h):
            p0, p1 = ax.ax.c2p(a + 0.1, 0), ax.ax.c2p(b - 0.1, max(v, 0.001))
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=CHILD,
                               fill_opacity=0.85).move_to((p0 + p1) / 2))
        side = VGroup(
            label(rf"{P['n']} commuting zones, \\ weighted by people", font_size=18, color=GREY_A),
            label(rf"the 10th percentile \\ of places: \ {P['am_p10']:.0f}", font_size=19, color=WHITE),
            label(rf"the 90th: \ {P['am_p90']:.0f}", font_size=19, color=WHITE),
            label(rf"the same family, \\ a different place: \\ a gap like that between \\ parents "
                  rf"{(P['am_p90'] - P['am_p10']) / load('chetty')['slope']:.0f} percentiles apart", font_size=17,
                  color=CHILD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Chetty, \ Hendren, \ Kline and Saez (2014), \ Online Data Table V", corner=DR, font_size=11)
        gap_pct = (P["am_p90"] - P["am_p10"]) / load("chetty")["slope"]
        with self.voiceover(
            "The tax records also say where each child grew up. For every commuting zone, the authors computed "
            "upward mobility: the expected rank, as an adult, of a child whose parents were at the twenty-fifth "
            "percentile. <bookmark mark='a'/> It varies enormously across America. <bookmark mark='b'/> In the "
            f"places at the tenth percentile, such a child is expected to reach rank {P['am_p10']:.0f}; "
            f"<bookmark mark='c'/> at the ninetieth, rank {P['am_p90']:.0f}. <bookmark mark='d'/> That gap is as "
            f"large as the gap, nationally, between children whose parents are about {gap_pct:.0f} percentiles "
            "apart."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(bars, color=WHITE, scale_factor=1.0))
            for mk, k in zip("bcd", (1, 2, 3)):
                vo.wait_until(mk)
                self.play(FadeIn(side[k]))
        self.clear_scene()

    def cities(self):
        P = load("places")
        bars = VGroup()
        for k, (nm, q) in enumerate(zip(P["pick"], P["pick_q"])):
            y = 2.3 - 0.62 * k
            col = LOSS if k < 4 else GAIN
            r = Rectangle(width=q * 40, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-0.6 + q * 20, y, 0]))
            bars.add(VGroup(label(tex_safe(nm), font_size=19, color=WHITE).next_to(np.array([-0.75, y, 0]), LEFT,
                                                                                    buff=0.15),
                            r, label(f"{100 * q:.1f}\\%", font_size=19, color=col).next_to(r, RIGHT, buff=0.15)))
        head = label(r"chance of rising from the bottom fifth to the top fifth", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.35)
        sub = label(r"the lowest four and the highest four of America's fifty largest commuting zones", font_size=17,
                    color=GREY_A).next_to(head, DOWN, buff=0.15)
        tag = data_tag(r"Chetty, \ Hendren, \ Kline and Saez (2014), \ Online Data Table V", corner=DR, font_size=11)
        with self.voiceover(
            "Among the fifty largest places, the extremes are striking. <bookmark mark='a'/> In Charlotte, a child "
            f"from the bottom fifth has a {100 * P['pick_q'][0]:.1f} percent chance of reaching the top fifth; in "
            "Atlanta, Raleigh and Indianapolis, about five. <bookmark mark='b'/> In Boston, Pittsburgh and Salt "
            f"Lake City, about ten; in San Jose, {100 * P['pick_q'][5]:.1f}: three times Charlotte's chance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars[:4]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars[4:]], lag_ratio=0.3), run_time=2.0)
        self.clear_scene()

    def correlates(self):
        P = load("places")
        items = sorted(P["corrs"].items(), key=lambda kv: kv[1])
        bars = VGroup()
        for k, (key, v) in enumerate(items):
            y = 2.5 - 0.44 * k
            w = abs(v) * 4.0
            col = GAIN if v > 0 else LOSS
            r = Rectangle(width=w, height=0.32, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([0.6 + (w / 2 if v > 0 else -w / 2), y, 0]))
            nm = label(CORR_NAMES[key], font_size=16, color=WHITE)
            if v > 0:
                nm.next_to(np.array([0.5, y, 0]), LEFT, buff=0.12)
                val = label(f"{v:+.2f}", font_size=15, color=col).next_to(r, RIGHT, buff=0.1)
            else:
                nm.next_to(np.array([0.6 - w, y, 0]), LEFT, buff=0.12)
                val = label(f"{v:+.2f}", font_size=15, color=col).next_to(np.array([0.7, y, 0]), RIGHT, buff=0.05)
            bars.add(VGroup(r, nm, val))
        axis = Line(np.array([0.6, 2.75, 0]), np.array([0.6, 2.5 - 0.44 * len(items) + 0.2, 0]), color=GREY_B,
                    stroke_width=2)
        head = label(r"what goes with upward mobility, \ across commuting zones", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.25)
        side = label(r"correlations, \\ weighted by \\ population; \\ not causes", font_size=18,
                     color=GREY_A).to_edge(RIGHT, buff=0.4).shift(DOWN * 1.5)
        tag = data_tag(r"Chetty, \ Hendren, \ Kline and Saez (2014), \ Online Data Tables V and VIII; \ computed",
                       corner=DR, font_size=11)
        with self.voiceover(
            "What do the high-mobility places have in common? Here are the correlations of upward mobility with "
            "characteristics of each place. <bookmark mark='a'/> The strongest negative ones: the share of children "
            "raised by single mothers, the share of Black residents, inequality, and segregation, by race and by "
            "income. <bookmark mark='b'/> The positive ones: a large middle class, short commutes, social capital, "
            "religious participation, better schools. The authors summarized five factors: segregation, "
            "inequality, schools, social capital and family structure. <bookmark mark='c'/> These are correlations "
            "across places. Is it the places themselves, or the families who live there?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(tag))
            neg = [b for b, (_, v) in zip(bars, items) if v < 0]
            pos = [b for b, (_, v) in zip(bars, items) if v > 0]
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.1) for b in neg], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in pos], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.clear_scene()

    def causal(self):
        L = tables.PLACES.data
        ax = plane([0, 20], [0, 1.0], center=LEFT * 2.6 + DOWN * 0.5, x_length=5.8, y_length=4.2,
                   xticks=[0, 5, 10, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"years of childhood in the new place", ylabel=r"share of the gap closed",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=13)
        xs = np.linspace(0, 20, 41)
        ln = path(ax, xs, np.minimum(xs * L["exposure"] / 100, 1.0), MIDDLE, 3.4, smooth=False)
        side = VGroup(
            label(rf"movers: \ children converge \\ to their new place \\ at about {L['exposure']}\% a year",
                  font_size=19, color=MIDDLE),
            label(r"Moving to Opportunity, \ 1994--98: \\ housing vouchers by lottery, \\ five cities", font_size=19,
                  color=WHITE),
            label(rf"moved before 13: \\ +\${L['mto_dollars']:,} a year in their \\ mid-twenties \ "
                  rf"(+{L['mto_pct']}\%)", font_size=19, color=GAIN),
            label(r"moved after 13: \ no gain", font_size=19, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = published_tag(tables.PLACES.tag, corner=DR, font_size=10)
        with self.voiceover(
            "Two designs answer that. <bookmark mark='a'/> Chetty and Hendren followed millions of families who "
            "moved, and compared siblings and children who moved at different ages. Children's outcomes converge to "
            f"those of the place they move to at about {L['exposure']} percent a year of childhood spent there: "
            "what matters is how long, not just where. <bookmark mark='b'/> And in the Moving to Opportunity "
            "experiment of the 1990s, families in public housing in five cities won, by lottery, vouchers to move "
            "to lower-poverty neighbourhoods. <bookmark mark='c'/> Children who moved before thirteen earned "
            f"{L['mto_dollars']:,} dollars a year more in their mid-twenties, {L['mto_pct']} percent more than the "
            "control group. <bookmark mark='d'/> Those who moved as teenagers did not gain. Places matter, and they "
            "matter most early."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(side[0]), run_time=2.0)
            for mk, k in zip("bcd", (1, 2, 3)):
                vo.wait_until(mk)
                self.play(FadeIn(side[k]))
        self.clear_scene()
