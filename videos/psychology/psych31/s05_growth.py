from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403

PALETTE = [CHILD, AGE, COHORT, PERIOD, GOOD, OLD]


class Growth(VoiceoverScene):
    def construct(self):
        self.card()
        self.children()
        self.model()
        self.shrink()

    def card(self):
        card = chapter_card(4, r"Growth curves", r"How do you describe a thousand different paths?",
                            lit={1958: r"Rao", 1982: r"Laird \& Ware"}, part=PART, scale=("person", "group"),
                            marr=("what",))
        with self.voiceover("Chapter four. Growth curves."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _axes(self):
        return axes([-0.3, 4.3], [70, 150], x_length=6.2, y_length=4.8, xticks=[0, 1, 2, 3, 4],
                    yticks=[80, 100, 120, 140], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                    xlabel=r"years since the first visit", ylabel=r"score", center=[-3.0, -0.4, 0], font_size=16)

    def children(self):
        d = load("growth")
        head = heading(r"Every child a line")
        A = self._axes()
        dots, lines = VGroup(), VGroup()
        t = d["t"]
        for i, y in enumerate(d["y"]):
            col = PALETTE[i % len(PALETTE)]
            ok = ~np.isnan(y)
            dots.add(scatter(A.ax, t[ok], y[ok], col, radius=0.06))
            b0, b1 = d["ols"][i]
            lines.add(Line(A.ax.c2p(0, b0), A.ax.c2p(4, b0 + 4 * b1), color=col, stroke_width=2.5,
                           stroke_opacity=0.8))
        rows = rows_of([
            (rf"{d['n_children']} simulated children, \ five yearly visits, \ some visits missed: \ "
             rf"{d['n_obs']} scores; \ twelve are drawn", WHITE),
            (r"each child has a starting level and a rate of growth, \ and each visit adds measurement noise", CHILD),
            (r"a line through each child's own points: \ the lines fan out", AGE),
            (r"the questions: \ the average path, \ how much children differ in level and in growth, \ and "
             r"whether starting high goes with growing fast", YOU),
        ], 5.6, 22, 0.36).move_to([3.6, -0.2, 0])
        tag = simulated_tag(r"simulated: \texttt{lifespan.growth\_data}")
        with self.voiceover(
            "Development is change within people, and people change at different rates. "
            f"<bookmark mark='a'/> Here are simulated children, {d['n_children']} of them, measured at five yearly "
            f"visits, with some visits missed: {d['n_obs']} scores in all. Twelve are drawn. "
            "<bookmark mark='b'/> Each child has a starting level and a rate of growth, and every visit adds "
            "measurement noise. <bookmark mark='c'/> Draw a line through each child's own points, and the lines fan "
            "out. <bookmark mark='d'/> The questions are the average path, how much children differ in level and in "
            "growth, and whether starting high goes with growing fast."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in dots], lag_ratio=0.15), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def model(self):
        d = load("growth")
        head = heading(r"The population a fan: \ a mixed model")
        eq = VGroup(
            label(r"$y_{ij} = (\beta_0 + u_{0i}) + (\beta_1 + u_{1i})\,t_j + \varepsilon_{ij}$", font_size=34),
            label(r"$\begin{pmatrix} u_{0i} \\ u_{1i} \end{pmatrix} \sim N\!\left(0, \ \begin{pmatrix} "
                  r"\sigma_0^2 & \rho\sigma_0\sigma_1 \\ \rho\sigma_0\sigma_1 & \sigma_1^2 \end{pmatrix}\right), "
                  r"\quad \varepsilon_{ij} \sim N(0, \sigma^2)$", font_size=30, color=CHILD),
        ).arrange(DOWN, buff=0.35).move_to([0, 1.7, 0])
        tbl = VGroup()
        items = [(r"average start, \ $\beta_0$", f"{d['beta'][0]:.1f}", "100"),
                 (r"average growth a year, \ $\beta_1$", f"{d['beta'][1]:.2f}", "6"),
                 (r"spread of starts, \ $\sigma_0$", f"{d['sd_int']:.1f}", "8"),
                 (r"spread of growth, \ $\sigma_1$", f"{d['sd_slope']:.2f}", "2"),
                 (r"start with growth, \ $\rho$", f"{d['rho']:.2f}", "0.3"),
                 (r"noise per visit, \ $\sigma$", f"{d['sd_e']:.1f}", "5")]
        hdr = VGroup(label(r"parameter", font_size=22, color=GREY_B), label(r"fitted", font_size=22, color=MODEL),
                     label(r"true", font_size=22, color=TRUE))
        for name, fit, true in items:
            tbl.add(VGroup(label(name, font_size=22), label(fit, font_size=22, color=MODEL),
                           label(true, font_size=22, color=TRUE)))
        grid = VGroup(hdr, *tbl)
        for k, row in enumerate(grid):
            y = -0.35 - 0.42 * k
            row[0].move_to([-1.2, y, 0]).align_to([-5.2, 0, 0], LEFT)
            row[1].move_to([1.6, y, 0])
            row[2].move_to([3.2, y, 0])
        rows = wrapped_label(r"fitted by EM: \ guess each child's deviations from the current fit, \ then refit the "
                             r"averages and spreads, \ and repeat", 8.6, 21, GREY_A)
        rows.to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        tag = psyche_tag(r"\texttt{lifespan.fit\_growth}")
        with self.voiceover(
            "The model that describes the fan is a linear mixed model. <bookmark mark='a'/> Each child's score at "
            "visit j is an average start plus the child's own deviation, plus an average rate of growth plus the "
            "child's own deviation, times time, plus noise. <bookmark mark='b'/> The two deviations are drawn from a "
            "normal distribution with spreads sigma zero and sigma one and a correlation rho; the noise has its own "
            "spread. <bookmark mark='c'/> Psyche fits it by EM: guess each child's deviations from the current fit, "
            "then refit the averages and spreads, and repeat until nothing changes. <bookmark mark='d'/> Every "
            f"parameter comes back close to the truth: growth of {d['beta'][1]:.2f} a year against six, a spread of "
            f"growth of {d['sd_slope']:.2f} against two, a correlation of {d['rho']:.2f} against 0.3. Part 47 "
            "builds these models properly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(eq[0]))
            vo.wait_until("b")
            self.play(FadeIn(eq[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows))
            vo.wait_until("d")
            self.play(FadeIn(grid[0]), LaggedStart(*[FadeIn(r_) for r_ in tbl], lag_ratio=0.3))
        self.clear_scene()

    def shrink(self):
        d = load("growth")
        head = heading(r"Each child's line, \ shrunk toward the fan")
        A = axes([0, 13], [0, 13], x_length=5.0, y_length=5.0, xticks=[0, 4, 8, 12], yticks=[0, 4, 8, 12],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"growth from the child's own line",
                 ylabel=r"growth from the model", center=[-3.2, -0.4, 0], font_size=15)
        diag = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(13, 13), color=GREY_B, stroke_width=2)
        mean = DashedLine(A.ax.c2p(0, d["beta"][1]), A.ax.c2p(13, d["beta"][1]), color=MODEL, stroke_width=2)
        ok = ~np.isnan(d["ols"][:, 1])
        pts = scatter(A.ax, d["ols"][ok, 1], d["blup"][ok, 1], CHILD, radius=0.05)
        rows = rows_of([
            (r"each child's own line uses only its own four or five noisy points", CHILD),
            (r"the model's estimate for each child, \ the BLUP, \ pulls it toward the average, \ more when its "
             r"data are thin", MODEL),
            (rf"spread of growth: \ own lines {d['sd_ols']:.2f}, \ truth {d['sd_true']:.2f}, \ BLUPs "
             rf"{d['sd_blup']:.2f}", WHITE),
            (r"own lines exaggerate how differently children grow; \ shrunken lines are better guesses for each "
             r"child, \ the James--Stein idea again", YOU),
        ], 5.8, 21, 0.36).move_to([3.5, -0.2, 0])
        tag = psyche_tag(r"\texttt{lifespan.fit\_growth}: \ BLUPs")
        with self.voiceover(
            "The model also gives each child a line. <bookmark mark='a'/> A child's own line uses only its four or "
            "five noisy points. <bookmark mark='b'/> The model's estimate for that child, called the BLUP, pulls it "
            "toward the average, and pulls harder when the child's data are thin. On this plot, the points lie "
            "flatter than the diagonal. <bookmark mark='c'/> The spreads tell the story: the children's own lines "
            f"vary by {d['sd_ols']:.2f} points a year, the true growth rates by {d['sd_true']:.2f}, and the "
            f"shrunken ones by {d['sd_blup']:.2f}. <bookmark mark='d'/> So own lines exaggerate how differently "
            "children grow, because they carry the noise. The shrunken lines are better guesses for each child. "
            "It's the James-Stein idea again: borrow strength from everyone to estimate anyone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(diag), Create(mean), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.01), FadeIn(rows[1]), run_time=2.0)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
