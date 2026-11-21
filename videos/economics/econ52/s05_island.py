from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403


class Island(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The Island's 100,000 households".replace(",", "{,}"),
             r"Does the economy look the same when you follow the people?",
             "Chapter four. The Island's hundred thousand households.", lit={2010: r"Young"},
             scale=("household", "nation"), horizon=("a century",))
        self.paths()
        self.crowd_()
        self.table()

    def paths(self):
        I = load("island")
        P = np.array(I["paths"])
        T = P.shape[1]
        ax = plane([0, T], [0, 40], center=LEFT * 1.4 + DOWN * 0.3, x_length=8.6, y_length=5.0,
                   xticks=[0, 50, 100, 150, 200], yticks=[0, 10, 20, 30, 40], xlabel=r"years",
                   ylabel=r"wealth", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        cols = (POOR, MANY, RICH, DIST, INDIRECT)
        lines = VGroup(*[path(ax, np.arange(T), np.minimum(P[k], 40), cols[k], 2.0, smooth=False)
                         for k in range(P.shape[0])])
        mean = seg(ax, 0, I["K"], T, I["K"], WHITE, 2.0, dashed=True)
        side = VGroup(
            label(r"five of the Island's \\ households, \ followed \\ for two centuries", font_size=19, color=WHITE),
            label(r"dashed: \ the economy's \\ capital per household", font_size=19, color=GREY_A),
            label(r"nobody stays rich \\ or poor for ever: \\ the distribution is \\ stationary, \ the people \\ are "
                  r"not", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"simulated: \ the Island, \ this part's equilibrium rules", corner=DL, font_size=12)
        with self.voiceover(
            "The rules are now known, so the Island can be populated. Give a hundred thousand households the "
            "equilibrium rules, draw each one's luck, and let them live. <bookmark mark='a'/> Here are five of "
            "them, followed for two centuries. A run of good years carries one up; a run of bad years drains its "
            "buffer to zero. <bookmark mark='b'/> The dashed line is the economy's capital per household. "
            "<bookmark mark='c'/> No household stays rich or poor for ever. The distribution settles down; the "
            "people inside it keep moving."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.25), run_time=6.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()

    def crowd_(self):
        I = load("island")
        bins = np.array(I["bins"])
        ax = plane([0, 60], [0, 0.08], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.8, y_length=4.6,
                   xticks=[0, 20, 40, 60], yticks=[0, 0.04, 0.08], xlabel=r"wealth",
                   ylabel=r"share of households", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        bars = VGroup()
        for x0, x1, h in zip(bins[:-1], bins[1:], I["hist"]):
            p0, p1 = ax.ax.c2p(x0, 0), ax.ax.c2p(x1, min(h, 0.08))
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.005), stroke_width=0.4,
                               stroke_color=BLACK, fill_color=DIST, fill_opacity=0.8).move_to((p0 + p1) / 2))
        head = VGroup(label(r"", font_size=18), label(r"simulated", font_size=18, color=MANY),
                      label(r"histogram", font_size=18, color=DIST))
        rows = [
            (r"wealth Gini", f"{I['gini_sim']:.3f}", f"{I['gini_hist']:.3f}"),
            (r"top 1\%'s share", rf"{100 * I['top1_sim']:.1f}\%", rf"{100 * I['top1_hist']:.1f}\%"),
            (r"at the limit", rf"{100 * I['at_limit_sim']:.1f}\%", rf"{100 * I['at_limit_hist']:.1f}\%"),
            (r"mean wealth", f"{I['mean']:.2f}", f"{I['K']:.2f}"),
        ]
        grid = VGroup(*head)
        for r in rows:
            grid.add(label(r[0], font_size=18, color=WHITE), label(r[1], font_size=18, color=MANY),
                     label(r[2], font_size=18, color=DIST))
        grid.arrange_in_grid(rows=len(rows) + 1, cols=3, buff=(0.4, 0.28), col_alignments="lcc")
        grid.to_edge(RIGHT, buff=0.35).shift(UP * 0.6)
        note_ = label(r"two ways to the same answer: \\ follow the people, \ or move \\ the whole distribution at once",
                      font_size=18, color=E.ACCENT).next_to(grid, DOWN, buff=0.5)
        with self.voiceover(
            "After four hundred years of simulated time, here is the whole crowd: wealth across all hundred "
            f"thousand households. <bookmark mark='a'/> A wealth Gini of {I['gini_sim']:.2f}, the top one percent "
            f"holding {100 * I['top1_sim']:.1f} percent, and {100 * I['at_limit_sim']:.1f} percent of households "
            "at the borrowing limit. <bookmark mark='b'/> The same numbers come from a different calculation with "
            "no random draws at all: Young's method from Part fifty-one, which moves the whole histogram forward "
            "at once, splitting each household's savings between the two nearest grid points. <bookmark mark='c'/> "
            "The two agree to the second or third digit. The simulation is what the economy looks like; the "
            "histogram is how it is computed."
        ) as vo:
            self.play(FadeIn(ax), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*grid[:3])), *[FadeIn(grid[3 * (k + 1)]) for k in range(len(rows))],
                      *[FadeIn(grid[3 * (k + 1) + 1]) for k in range(len(rows))])
            vo.wait_until("b")
            self.play(*[FadeIn(grid[3 * (k + 1) + 2]) for k in range(len(rows))])
            vo.wait_until("c")
            self.play(FadeIn(note_, shift=UP * 0.1))
        self.clear_scene()

    def table(self):
        Tb = load("table")
        rows = Tb["rows"]
        rho_t = Tb["rho_time"]
        head = label(r"the equilibrium interest rate, \ \% \ (recomputed): \ "
                     rf"the rate of time preference is {rho_t:.2f}\%", font_size=24, color=E.ACCENT).to_edge(
            UP, buff=0.45)
        blocks = VGroup()
        for sd in Tb["sds"]:
            cells = VGroup()
            top = VGroup(label(rf"spread {sd}", font_size=19, color=WHITE),
                         *[label(rf"$\gamma = {g:.0f}$", font_size=18, color=GREY_A) for g in Tb["gammas"]])
            cells.add(*top)
            for rho in Tb["rhos"]:
                cells.add(label(rf"persistence {rho}", font_size=18, color=GREY_A))
                for g in Tb["gammas"]:
                    v = next(r["r"] for r in rows if r["sd"] == sd and r["rho"] == rho and r["gamma"] == g)
                    shade_ = interpolate_color(ManimColor(GRID), ManimColor(ERR), float(np.clip(1 - v / rho_t, 0, 1)
                                                                                         ) ** 0.6)
                    cells.add(label(f"{v:.2f}", font_size=20, color=shade_))
            cells.arrange_in_grid(rows=len(Tb["rhos"]) + 1, cols=len(Tb["gammas"]) + 1, buff=(0.45, 0.26),
                                  col_alignments="l" + "c" * len(Tb["gammas"]))
            blocks.add(cells)
        blocks.arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.6)
        if blocks.width > 13.2:
            blocks.width = 13.2
        lo = min(rows, key=lambda r: r["r"])
        foot = label(r"every rate sits below the rate of time preference; \ more risk, \ more persistence, \ more "
                     r"risk aversion: \ lower", font_size=20, color=WHITE).to_edge(DOWN, buff=0.9)
        tag = published_tag(r"after Aiyagari (1994), \ Table II, \ recomputed with Rouwenhorst's chain",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Aiyagari's own table varied three things: how widely wages are spread, how persistent they are, and "
            "how much households dislike risk. Here it is, recomputed with the methods of Part fifty-one. <bookmark "
            "mark='a'/> With a small spread and no persistence, the rate is barely below the rate of time "
            "preference: a bad year is soon over, and a little saving covers it. <bookmark mark='b'/> Raise the "
            "spread, the persistence and the risk aversion, and the rate falls, as households pile up buffers: down "
            f"to {lo['r']:.2f} percent with persistence {lo['rho']} and risk aversion {lo['gamma']:.0f}. <bookmark "
            "mark='c'/> Every cell is below the rate of time preference. Uninsured risk lowers interest rates, and "
            "the more persistent the risk, the more it lowers them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(blocks[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(blocks[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
