from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load, real_data, tbar

ORDER = ["pooled OLS", "clustered by industry", "clustered by month", "two-way clustered", "Fama-MacBeth"]


class EventPanel(VoiceoverScene):
    def construct(self):
        e = load("event")
        p = load("panel")
        self.card()
        self.event(e)
        self.panel(p)

    def card(self):
        c = chapter_card(3, r"Event studies and panels", r"Whose errors move together?", part=PART)
        with self.voiceover("Chapter three. Event studies, and panels."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def event(self, e):
        g = axes([-5.5, 5.5], [-0.2, 0.25], x_length=7.6, y_length=4.2, xlabel=r"trading days around the turn of the "
                 r"month ($-1$: last day, $+1$: first)", ylabel=r"abnormal return, \% a day", xticks=[-5, -3, -1, 1, 3, 5],
                 yticks=[-0.1, 0, 0.1, 0.2], yfmt=lambda u: f"{u:.1f}", font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        groups = VGroup()
        for name, col, off in (("1926-1986", EST, -0.2), ("1987-2020", ALT, 0.2)):
            bars = VGroup()
            for row in e[name]["ar"]:
                k = row["k"]
                b = tbar(ax, k + off, 100 * row["ar"], col, width=0.35)
                err = Line(ax.c2p(k + off, 100 * (row["ar"] - 2 * row["se"])), ax.c2p(k + off, 100 * (row["ar"] + 2 * row["se"])),
                           stroke_width=1.5, color=GREY_B)
                bars.add(VGroup(b, err))
            groups.add(bars)
        win = Rectangle(width=ax.c2p(3.5, 0)[0] - ax.c2p(-1.5, 0)[0], height=ax.c2p(0, 0.25)[1] - ax.c2p(0, -0.2)[1],
                        stroke_color=GOOD, stroke_width=2, fill_opacity=0).move_to(
            (ax.c2p(-1.5, -0.2) + ax.c2p(3.5, 0.25)) / 2)
        a, b = e["1926-1986"], e["1987-2020"]
        side = VGroup(
            legend([(EST, r"1926--1986"), (ALT, r"1987--2020")], font_size=21),
            label(r"the window $[-1, +3]$, about 18\% of trading days:", font_size=21, color=GREY_A),
            MathTex(rf"\text{{share of all returns: }} {100 * a['share_of_return']:.0f}\% \ (t = {a['t']:.1f})", font_size=28,
                    color=EST),
            MathTex(rf"\text{{after publication: }} {100 * b['share_of_return']:.0f}\% \ (t = {b['t']:.1f})", font_size=28,
                    color=ALT),
            wrapped_label(r"abnormal: minus the average return of days outside the window; bars $\pm 2$ standard errors; "
                          r"Ariel (1987), Lakonishok and Smidt (1988)", 4.6, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Kenneth French's daily US market, July 1926 -- December 2020")
        with self.voiceover(
            "An event study asks what happens to prices around an event: an earnings report, a merger, a rate "
            "decision. Line up every occurrence at day zero, subtract a normal return, and average. Craig MacKinlay's "
            "1997 survey is the standard guide. Here is an event with nothing to do with news: the turn of the month. "
            "<bookmark mark='a'/> From 1926 to 1986, the last trading day of each month and the first three of the "
            "next earned far more than normal days. Those four days, under a fifth of all trading days, delivered "
            f"{100 * a['share_of_return']:.0f} percent of the market's entire return. Robert Ariel published it in 1987. "
            f"<bookmark mark='b'/> Since then the effect is weaker but still there: {100 * b['share_of_return']:.0f} "
            "percent of the return, with a t-statistic of two and a half. Payroll and pension flows at month end are "
            "the usual explanation. It is a calendar regularity, and the House treats it as a trial like any other."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in groups[0]], lag_ratio=0.1), Create(win), FadeIn(side[1]),
                      FadeIn(side[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in groups[1]], lag_ratio=0.1), FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def panel(self, p):
        res = p["results"]
        rows = VGroup()
        for k in ORDER:
            r = res[k]
            col = ALT if k == "Fama-MacBeth" else (GOOD if abs(r["t"]) > 1.96 else BAD)
            rows.add(VGroup(label(k, font_size=24, color=GREY_A),
                            MathTex(rf"{r['beta']:.4f}", font_size=30),
                            MathTex(rf"{r['se']:.4f}", font_size=30),
                            MathTex(rf"{r['t']:.2f}", font_size=30, color=col)))
        head = VGroup(label(r"method", font_size=21, color=GREY_B), label(r"slope", font_size=21, color=GREY_B),
                      label(r"std. error", font_size=21, color=GREY_B), label(r"$t$", font_size=21, color=GREY_B))
        cells = [*head] + [c for r in rows for c in r]
        grid = VGroup(*cells).arrange_in_grid(rows=len(ORDER) + 1, cols=4, buff=(0.7, 0.22), col_alignments="lrrr")
        grid.to_edge(UP, buff=0.7)
        notes = VGroup(
            wrapped_label(r"pooled OLS treats 51{,}858 industry-months as independent; but industries in the same month "
                          r"share a market shock, so the errors are correlated within each month (Petersen 2009)", 12.4, 22,
                          GREY_A),
            wrapped_label(r"cluster by month, or run Fama and MacBeth's (1973) monthly cross-sections and use the time "
                          r"series of slopes: both survive the common shock", 12.4, 22, GOOD),
            wrapped_label(r"the slopes differ because pooled OLS weights each month by its cross-sectional dispersion: the "
                          r"turbulent months, when momentum crashed (Part 24), dominate; Fama--MacBeth weights months "
                          r"equally. Decide which question you are asking before you choose.", 12.4, 22, ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(grid, DOWN, buff=0.5)
        with self.voiceover(
            "Back to the opening puzzle. The regression pooled fifty-two thousand industry-months and treated them as "
            "independent. <bookmark mark='a'/> They are not: in any month, all forty-nine industries are hit by the "
            "same market shock. Mitchell Petersen showed in 2009 that a large share of published finance papers "
            "ignored exactly this. Clustering the standard errors by month allows for it, and the t-statistic "
            "collapses. <bookmark mark='b'/> Fama and MacBeth's 1973 method handles it differently: run a "
            "cross-sectional regression each month, and judge the average slope by how much it varies from month to "
            "month. <bookmark mark='c'/> Why is its slope eight times larger? Because pooled least squares weights "
            "each month by how spread out the industries' past returns were. The turbulent months dominate, and in "
            "those months momentum tended to crash, the subject of Part twenty-four. Fama-MacBeth weights every "
            "month equally. They answer different questions; the standard error must match the question."
        ) as vo:
            self.play(FadeIn(VGroup(*cells[:4])), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), LaggedStart(*[FadeIn(r) for r in rows[1:4]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(rows[4]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()
