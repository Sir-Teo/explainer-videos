from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403


class Regions(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Macro from the cross-section", r"Can regions stand in for the nation?",
             "Chapter nine. Macro from the cross-section.",
             lit={2014: r"Nakamura and Steinsson", 2020: r"Goldsmith-Pinkham, Sorkin and Swift", 2023: r"Wolf"},
             scale=("city", "nation"), horizon=("a decade",))
        self.regions()
        self.shift_share()

    def regions(self):
        G = load("regions")
        g, y = np.array(G["g"]), np.array(G["y"])
        gd, yd = (g - g.mean(axis=0)), (y - y.mean(axis=0))
        rng = np.random.default_rng(55)
        pick = rng.choice(gd.size, 420, replace=False)
        gx, yy = gd.ravel()[pick], yd.ravel()[pick]
        axl = plane([-3, 3], [-8, 8], center=LEFT * 3.3 + DOWN * 0.45, x_length=5.2, y_length=4.2,
                    xticks=[-2, 0, 2], yticks=[-6, -3, 0, 3, 6], xlabel=r"a region's spending, \ minus the year's mean",
                    ylabel=r"its output, \ minus the year's mean", xfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v
                    else "0", yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=12)
        axr = plane([-3, 3], [-3, 3], center=RIGHT * 2.6 + DOWN * 0.45, x_length=4.2, y_length=4.2,
                    xticks=[-2, 0, 2], yticks=[-2, 0, 2], xlabel=r"the nation's spending", ylabel=r"its output",
                    xfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0",
                    yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=12)
        dl = VGroup(*[Dot(axl.ax.c2p(a, b), radius=0.025, color=DATA, fill_opacity=0.6) for a, b in zip(gx, yy)
                      if abs(b) < 8])
        ll = seg(axl, -3, -3 * G["b_fe"], 3, 3 * G["b_fe"], EST, 2.8)
        dr = VGroup(*[Dot(axr.ax.c2p(a, b), radius=0.05, color=MODEL) for a, b in zip(G["gbar"], G["ybar"])
                      if abs(b) < 3])
        lr = seg(axr, -3, -3 * G["b_nat"], 3, 3 * G["b_nat"], MODEL, 2.8)
        side = VGroup(
            label(rf"{G['R']} regions, \ {G['T']} years, \\ one central bank", font_size=18, color=WHITE),
            label(rf"across regions: \\ {G['b_fe']:.2f} \ (planted {G['m_local']:.1f})", font_size=19, color=EST),
            label(rf"the nation: \\ {G['b_nat']:.2f} \ (planted {G['m_agg']:.1f})", font_size=19, color=MODEL),
            label(r"the difference sits in \\ the year effects: \\ the missing intercept", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.2)
        tag = island_tag(r"simulated: \ Part 32's currency union", corner=DR, font_size=13)
        lo_, hi_ = np.percentile(g, 5), np.percentile(g, 95)

        def shade_(v):
            return interpolate_color(ManimColor(DATA), ManimColor(EST), float(np.clip((v - lo_) / (hi_ - lo_), 0, 1)))

        tiles = VGroup(*[Square(side_length=0.46, stroke_width=1, stroke_color=GREY_D, fill_color=shade_(g[r_, 0]),
                                fill_opacity=0.85) for r_ in range(G["R"])]).arrange_in_grid(6, 8, buff=0.08)
        tiles.move_to(LEFT * 1.3 + DOWN * 0.2)
        year = label(r"year 1", font_size=24, color=WHITE).next_to(tiles, UP, buff=0.3)
        tkey = label(r"each square a region, \ shaded by its spending: \ blue low, \ gold high",
                     font_size=18, color=GREY_B).next_to(tiles, DOWN, buff=0.3)
        with self.voiceover(
            "One history is one data point. A cross-section has many. Emi Nakamura and Jón Steinsson compared "
            "American states that receive more or less of national military spending. Part thirty-two built such "
            f"a union on the Island: {G['R']} regions over {G['T']} years, with one central bank. <bookmark "
            "mark='a'/> Compare regions within each year, and a region that gets a point more spending than "
            f"average produces {G['b_fe']:.2f} points more output: the relative multiplier, planted at "
            f"{G['m_local']:.1f}. <bookmark mark='b'/> But the nation's output rises only {G['b_nat']:.2f} per point "
            "of national spending, because the central bank leans against national spending, and cannot lean "
            "against one region's. <bookmark mark='c'/> Everything national, including monetary policy's response, "
            "is soaked up by the year effects that made the comparison clean. The regional estimate is right, and "
            "answers a different question. Christian Wolf showed how a model can bridge the two: the missing "
            "intercept is the price of using the cross-section."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(side[0]), LaggedStart(*[FadeIn(t_) for t_ in tiles], lag_ratio=0.02),
                      FadeIn(year), FadeIn(tkey), run_time=2.0)
            for yr_ in (1, 2, 3):
                self.wait(1.0)
                self.play(*[t_.animate.set_fill(shade_(g[r_, yr_])) for r_, t_ in enumerate(tiles)],
                          Transform(year, label(rf"year {yr_ + 1}", font_size=24, color=WHITE).move_to(year)),
                          run_time=1.0)
            vo.wait_until("a")
            self.play(FadeOut(VGroup(tiles, year, tkey)), run_time=0.6)
            self.play(FadeIn(axl), FadeIn(axr), FadeIn(dl), Create(ll), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(dr), Create(lr), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def shift_share(self):
        eq = MathTex(r"z_r = \sum_k \underbrace{s_{rk}}_{\text{region } r\text{'s share of industry } k}\;"
                     r"\underbrace{g_k}_{\text{a national shock to } k}", font_size=40, color=THEORY).move_to(UP * 1.6)
        rows = VGroup(
            label(r"a shift-share instrument: \ exposure times national shocks \ (Part 36's China shock)",
                  font_size=21, color=WHITE),
            label(r"identified by the shares: \ they must be as good as random \ (Goldsmith-Pinkham, \ Sorkin and "
                  r"Swift)", font_size=21, color=EST),
            label(r"or by the shocks: \ many of them, \ as good as random \ (Borusyak, \ Hull and Jaravel)",
                  font_size=21, color=MODEL),
            label(r"either way, \ the answer is relative: \ the missing intercept again", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.32).next_to(eq, DOWN, buff=0.7)
        tag = published_tag(r"Goldsmith-Pinkham, \ Sorkin and Swift, \ AER (2020); \ Borusyak, \ Hull and Jaravel, "
                            r"\ REStud (2022)", corner=DR, font_size=12)
        with self.voiceover(
            "The same logic powers the shift-share designs of Part thirty-six's China shock. <bookmark mark='a'/> A "
            "region's exposure is its mix of industries, times national shocks to those industries. <bookmark "
            "mark='b'/> Paul Goldsmith-Pinkham, Isaac Sorkin and Henry Swift showed that such an instrument is "
            "valid if the industry shares are as good as random; <bookmark mark='c'/> Kirill Borusyak, Peter Hull and "
            "Xavier Jaravel, that it can instead be valid if the national shocks are, provided there are many of "
            "them. <bookmark mark='d'/> Either way, the answer compares regions with each other, and the effect on "
            "the nation as a whole has to come from somewhere else."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(rows[0]), run_time=1.5)
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
