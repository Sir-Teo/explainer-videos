from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Play it: \ choose the discount rate", r"What is a dollar of damage in 2100 worth today?",
             "Chapter six. Play it: choose the discount rate.", lit={1928: r"Ramsey"}, scale=("world",),
             horizon=("a century",))
        self.stream()
        self.ask()
        self.reveal()

    def stream(self):
        S = load("scc")
        yr, d = np.array(S["year"]), np.array(S["dC_per_t"])
        ax = plane([2025, 2300], [0, 24], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.4, y_length=4.6,
                   xticks=[2050, 2100, 2150, 2200, 2250, 2300], yticks=[0, 5, 10, 15, 20],
                   xlabel=r"year", ylabel=r"damage that year from one tonne emitted in 2025, \ \$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ln = path(ax, yr, d, LOSS, 3.2, smooth=False)
        area = band(ax, yr, np.zeros_like(d), d, LOSS, 0.2)
        pins = VGroup()
        for y in (2030, 2100, 2200):
            v = float(d[yr == y][0])
            pins.add(VGroup(dot(ax, y, v, WHITE, 0.07), label(rf"{y}: \ \${v:.1f}", font_size=16, color=WHITE).next_to(
                ax.ax.c2p(y, v), UL, buff=0.08)))
        side = VGroup(
            label(r"one more tonne, \\ emitted in 2025", font_size=18, color=WHITE),
            label(r"it stays in the air, \\ the world stays warmer, \\ and the world economy \\ it harms keeps "
                  r"growing", font_size=18, color=LOSS),
            label(rf"added up, \ undiscounted, \\ to 2300: \ \${d.sum():,.0f}".replace(",", "{,}"), font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is what the model says one extra tonne of carbon dioxide, emitted in 2025, does. <bookmark "
            "mark='a'/> Its damage arrives as a stream, in lost consumption, year after year. <bookmark mark='b'/> "
            f"About {d[yr == 2030][0]:.0f} dollar in 2030, {d[yr == 2100][0]:.0f} dollars in 2100, "
            f"{d[yr == 2200][0]:.0f} in 2200. The stream grows, because much of the carbon stays in the air, "
            "the world stays warmer, and the economy it harms keeps growing. <bookmark mark='c'/> Added up without "
            f"discounting, to the year 2300 alone, it comes to about {d.sum():,.0f} dollars. Nobody thinks the "
            "social cost of carbon is that. The question is how to compare a dollar in 2200 with a dollar today."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(area), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pins], lag_ratio=0.5), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def ask(self):
        head = label(r"A dollar of damage in 2100. \ What is it worth to you today?", font_size=30,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        opts = VGroup(*[VGroup(RoundedRectangle(width=2.4, height=1.3, corner_radius=0.12, stroke_color=c,
                                                stroke_width=2.4, fill_color=c, fill_opacity=0.12),
                               label(t, font_size=28, color=c))
                        for t, c in ((r"1\%", STERN), (r"2\%", COOL), (r"3\%", OPT), (r"5\%", METAL))])
        for o in opts:
            o[1].move_to(o[0])
        opts.arrange(RIGHT, buff=0.5).move_to(UP * 0.3)
        worth = VGroup(*[label(rf"{100 / (1 + r) ** 75:.0f} cents", font_size=20, color=GREY_A).next_to(o, DOWN,
                                                                                                        buff=0.2)
                         for r, o in zip((0.01, 0.02, 0.03, 0.05), opts)])
        ring = countdown().scale(0.6).next_to(worth, DOWN, buff=0.6)
        with self.voiceover(
            "Your turn. Discounting at a rate r says a dollar in seventy-five years is worth one over one plus r, "
            "seventy-five times over. At one percent a year, a dollar of damage in 2100 is worth about 47 cents "
            "today; at two, 23; at three, 11; at five, under 3. Pause, and choose the rate you would use for "
            "damage that falls on people not yet born."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(o) for o in opts], lag_ratio=0.3), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(w) for w in worth], lag_ratio=0.3), FadeIn(ring), run_time=2.0)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.clear_scene()

    def reveal(self):
        S = load("scc")
        T = tables.DICE_2023.data
        rates, scc = np.array(S["rates"]) * 100, np.array(S["by_rate"])
        ax = plane([0.8, 6.2], [0, 3.0], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.0, y_length=4.6,
                   xticks=[1, 2, 3, 4, 5, 6], yticks=[np.log10(x) for x in (10, 30, 100, 300, 1000)],
                   xlabel=r"discount rate, \ \% a year", ylabel=r"social cost of carbon, \ \$ a tonne \ (log scale)",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), font_size=14)
        ln = path(ax, rates, np.log10(scc), OPT, 3.4)
        ours = VGroup(*[dot(ax, r, np.log10(v), OPT, 0.06) for r, v in zip(rates, scc)])
        dice_pts = VGroup(*[Square(side_length=0.14, color=METAL, fill_opacity=1).move_to(ax.ax.c2p(r, np.log10(v)))
                            for r, v in T["scc_r"].items()])
        labs = VGroup()
        for r in (1, 2, 3, 5):
            v = scc[list(rates).index(r)]
            labs.add(label(rf"\${v:,.0f}".replace(",", "{,}"), font_size=17, color=OPT).next_to(
                ax.ax.c2p(r, np.log10(v)), UR, buff=0.08))
        side = VGroup(
            label(r"green: \ the model \\ built here", font_size=18, color=OPT),
            label(r"gold: \ DICE-2023 \\ at the same rates", font_size=18, color=METAL),
            label(rf"at 3\%, \ {100 * S['share_after_2100_at3']:.0f}\% of the \\ cost comes from damage \\ after 2100",
                  font_size=18, color=WHITE),
            label(r"halve the rate, \\ and the cost \\ roughly doubles \\ or triples", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is what your choice implies. <bookmark mark='a'/> The social cost of carbon is the whole stream, "
            "discounted to today. At one percent, about "
            f"{scc[0]:,.0f} dollars a tonne; at two percent, {scc[2]:,.0f}; at three, {scc[4]:,.0f}; at five, "
            f"{scc[8]:,.0f}. <bookmark mark='b'/> The gold squares are DICE-2023's own figures at the same rates, "
            f"from {T['scc_r'][1]} dollars at one percent to {T['scc_r'][5]} at five. <bookmark mark='c'/> At three "
            f"percent, {100 * S['share_after_2100_at3']:.0f} percent of the cost comes from damage after 2100. "
            "<bookmark mark='d'/> Nothing else in the model moves the answer this much. Halve the rate and the cost "
            "of a tonne roughly doubles or triples. So the next chapter asks where a discount rate should come from."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(ours), LaggedStart(*[FadeIn(x) for x in labs], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(q) for q in dice_pts], lag_ratio=0.2), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
