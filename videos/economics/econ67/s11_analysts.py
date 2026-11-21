from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403


class Analysts(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Many analysts, \ one dataset", r"Give the same data and the same question to seven careful "
             r"economists: \ how many answers come back?", "Chapter nine. Many analysts, one dataset.",
             lit={2018: "DellaVigna and Pope", 2021: "Huntington-Klein et al."}, scale=("world",),
             horizon=("a year",))
        self.published()
        self.teams()
        self.curve()
        self.forecasts()

    def published(self):
        D = tables.REPLICATION_67.data
        rows = VGroup(
            label(r"two published causal results, \ each given to seven replicators with the original data sources",
                  font_size=21, color=GREY_A),
            label(r"no two replicators ended with the same sample size", font_size=22, color=PUB),
            label(rf"the estimates spread {D['hk_ratio'][0]} to {D['hk_ratio'][1]} times as widely as the standard "
                  r"errors each reported", font_size=22, color=FAIL),
            label(r"for one study, \ the sign of the effect differed across replicators", font_size=22,
                  color=FAIL),
            label(r"most of the choices behind the differences would never appear in a paper", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(UP * 0.2)
        tag = published_tag(r"Huntington-Klein et al., \ \emph{Economic Inquiry} 59(3) (2021)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "In 2021 Nick Huntington-Klein and coauthors ran an experiment on economists. <bookmark mark='a'/> They "
            "took two published causal studies and gave each to seven experienced researchers, with the original "
            "data sources and the question, and let each build the analysis from scratch. <bookmark mark='b'/> "
            "No two of the "
            "replicators ended with the same number of observations. <bookmark mark='c'/> Their estimates spread "
            "three to four times as widely as the standard error each of them reported. <bookmark mark='d'/> For "
            "one study, even the sign differed. <bookmark mark='e'/> And most of the choices that drove the "
            "differences, how to clean a variable, whom to drop, are the kind no paper reports. A standard error "
            "measures sampling noise; it says nothing about the analyst."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def teams(self):
        A = load("analysts")
        rows = A["rows"]
        ax = plane([-0.05, 0.3], [0, 8], center=LEFT * 2.4 + DOWN * 0.2, x_length=7.2, y_length=5.0,
                   xticks=[0, 0.1, 0.2, 0.3], yticks=[], xlabel=r"estimated effect on earnings, \ log points",
                   xfmt=lambda v: f"{v:.1f}", font_size=14)
        zero = vline(ax, 0, 0, 8, GREY_C, 1.4)
        truth = vline(ax, A["ate"], 0, 8, TRUE, 2.4)
        tl = label(rf"the effect for those who finished: \ {A['ate']:.2f}", font_size=14, color=TRUE).next_to(
            ax.ax.c2p(A["ate"], 8), UP, buff=0.06)
        lines = VGroup()
        for k, r in enumerate(rows):
            y = 7 - k
            col = FIRST if r["treated"] == "enrolled" else PUB
            lines.add(VGroup(Line(ax.ax.c2p(r["est"] - 1.96 * r["se"], y), ax.ax.c2p(r["est"] + 1.96 * r["se"], y),
                                  stroke_color=col, stroke_width=3),
                             Dot(ax.ax.c2p(r["est"], y), radius=0.07, color=col),
                             label(rf"team {r['team']}: \ $n = {r['n']:,}$".replace(",", "{,}"), font_size=13,
                                   color=GREY_A).next_to(ax.ax.c2p(-0.05, y), LEFT, buff=0.1)))
        key = legend_rows([(FIRST, "counts everyone who enrolled"), (PUB, "counts only those who finished")],
                          font_size=15).next_to(ax.ax, RIGHT, buff=0.4).shift(UP * 1.4)
        side = VGroup(
            label(rf"spread of the estimates: \ {A['spread']:.3f}", font_size=17, color=GREY_A),
            label(rf"average reported standard error: \ {A['mean_se']:.3f}", font_size=17, color=GREY_A),
            label(rf"ratio: \ {A['ratio']:.1f}", font_size=20, color=FAIL),
            label(r"every team defensible; \\ the choices are the uncertainty", font_size=17, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        tag = island_tag(r"a simulated dataset: \ agora.field.many\_analysts \ (4,000 people, \ the truth known)",
                         corner=DL, font_size=12)
        with self.voiceover(
            "The same experiment on a dataset where the truth is known. <bookmark mark='a'/> Four thousand people, "
            "a training programme, and earnings afterwards. The programme helps the young most and the old not at "
            "all; the young, the poor and some regions enrol more; earnings have heavy tails and a few miscoded "
            "records; and three in ten who enrol drop out. <bookmark mark='b'/> Seven analysts each make choices a "
            "referee would accept: an age range, whether to drop outliers, how to control for age, income and "
            "region, and whether to count everyone who enrolled or only those who finished. <bookmark mark='c'/> "
            f"Seven sample sizes, seven estimates, from {min(r['est'] for r in rows):.2f} to "
            f"{max(r['est'] for r in rows):.2f}. <bookmark mark='d'/> Their spread is {A['ratio']:.1f} times the "
            "standard error they report. Every one of them is defensible. The choices are the uncertainty."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(truth), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(key))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.25), run_time=2.4)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.3), run_time=1.8)
        self.clear_scene()

    def curve(self):
        A = load("analysts")
        cv = A["curve"]
        n = len(cv)
        ax = plane([0, n + 1], [-0.05, 0.3], center=UP * 0.2 + LEFT * 0.3, x_length=11.0, y_length=4.4,
                   xticks=[1, 72, 144, 216, 288], yticks=[0, 0.1, 0.2, 0.3],
                   xlabel=r"the specifications, \ sorted by estimate",
                   ylabel=r"effect, \ log points", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        zero = seg(ax, 0, 0, n + 1, 0, GREY_C, 1.4)
        band_ = VGroup(*[Line(ax.ax.c2p(k + 1, r["est"] - 1.96 * r["se"]), ax.ax.c2p(k + 1, r["est"] + 1.96 * r["se"]),
                              stroke_color=GREY_B, stroke_width=1.0, stroke_opacity=0.5) for k, r in enumerate(cv)])
        pts = VGroup(*[Dot(ax.ax.c2p(k + 1, r["est"]), radius=0.028,
                           color=FIRST if r["treated"] == "enrolled" else PUB) for k, r in enumerate(cv)])
        truth = seg(ax, 0, A["ate"], n + 1, A["ate"], TRUE, 2.0, dashed=True)
        key = legend_rows([(FIRST, "counts everyone who enrolled"), (PUB, "counts only those who finished"),
                           (TRUE, "the effect for those who finished")], font_size=14).next_to(
            ax.ax.c2p(0, 0.3), DR, buff=0.15)
        side = label(rf"{n} specifications: \ {100 * A['share_sig']:.0f}\% significant; \ estimates from "
                     rf"{A['curve_lo']:.2f} to {A['curve_hi']:.2f}", font_size=19, color=E.ACCENT).to_edge(
            DOWN, buff=0.35)
        tag = island_tag(r"computed: \ agora.field.specification\_curve", corner=DR, font_size=12)
        with self.voiceover(
            "Seven teams sampled seven paths. A computer can walk them all. <bookmark mark='a'/> Every combination "
            f"of the same choices gives {n} specifications. Sort their estimates from smallest to largest, each "
            "with its confidence interval: this is a specification curve. <bookmark mark='b'/> Colour them by one "
            "choice, whom to count as treated, and the curve splits: counting everyone who enrolled, including "
            "those who quit, dilutes the effect. <bookmark mark='c'/> "
            f"{100 * A['share_sig']:.0f} percent are significant, so the programme's benefit is robust. Its size "
            f"is not: from {A['curve_lo']:.2f} to {A['curve_hi']:.2f}, a factor of "
            f"{A['curve_hi'] / A['curve_lo']:.0f}. The honest report is the "
            "whole curve, with the choice that moves it named."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(band_), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.004), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(key), Create(truth))
            vo.wait_until("c")
            self.play(FadeIn(side, shift=UP * 0.1))
        self.clear_scene()

    def forecasts(self):
        D = tables.FORECASTS_67.data
        cards = point_cards([
            (r"the study", rf"{D['experts']} experts forecast the effects of {D['treatments']} ways to motivate "
             r"effort, \ in an experiment with nearly 10,000 people", FIRST),
            (r"the crowd", rf"the experts' average forecast beat {100 * D['beats']:.0f}\% of individual "
             r"forecasts", TRUE),
            (r"the credentials", r"citations, \ rank and field did not predict who forecast well", PUB),
            (r"the use", r"collect forecasts before a study: \ a result is news by how far it moves the crowd", STATE),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"could experts have told us?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"DellaVigna and Pope, \ \emph{JPE} 126(6) (2018)", corner=DL, font_size=12)
        with self.voiceover(
            "If analysts disagree, ask whether experts can forecast results at all. <bookmark mark='a'/> Stefano "
            "DellaVigna and Devin Pope ran an online experiment with nearly ten thousand people and fifteen ways to "
            "motivate effort, from piece rates to charity, and asked two hundred and eight experts to forecast each "
            "effect first. <bookmark mark='b'/> The experts' average forecast was good, better than ninety-six "
            "percent of the individual forecasts: the wisdom of crowds. <bookmark mark='c'/> And credentials did "
            "not predict accuracy: citations, academic rank and field made no difference. <bookmark mark='d'/> The "
            "practical lesson: collect forecasts before a study. A result is news in proportion to how far it moves "
            "what the crowd expected, and a forecast written down cannot be revised after the fact."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
