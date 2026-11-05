from __future__ import annotations

import numpy as np

from videos.stats.stats25.common import *  # noqa: F403


def baseball_plot(d, with_truth=True, center=(0.6, 0.3, 0)):
    return ShrinkagePlot(d["y"], d["js"], d["p"] if with_truth else None, x_range=(0.14, 0.41), width=10.4, center=list(center),
                         gap=1.6, labels={"raw": "first 45", "shrunk": "James--Stein", "truth": "rest of season"},
                         ticks=[0.15, 0.2, 0.25, 0.3, 0.35, 0.4], fmt=lambda v: f"{v:.2f}".lstrip("0"),
                         colors={"raw": RAW, "shrunk": SHRUNK, "truth": TRUE})


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.raw()
        self.shrink()
        self.score()
        self.paradox()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1975,)).to_edge(UP, buff=0.35)
        hc = history_card(1975, r"Bradley Efron \& Carl Morris, \ \emph{JASA}",
                          r"eighteen major-league hitters after their first 45 at-bats of the 1970 season. \ Predict each "
                          r"player's average for the rest of the season. \ The obvious answer, \ each player's own average "
                          r"so far, \ loses badly to a rule that pulls every player towards the others",
                          color=PATH, width=11.0, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"Roberto Clemente: \ 18 hits in 45, \ .400", font_size=24),
            label(r"is he really a .400 hitter?", font_size=24, color=RES),
        ), 12.0, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1975 Bradley Efron and Carl Morris took eighteen major-league baseball players after "
            "their first forty-five times at bat in the 1970 season, and asked how well each player's average so far "
            "predicts his average for the rest of the season. <bookmark mark='b'/> Roberto Clemente had eighteen hits in "
            "forty-five, a batting average of point four oh oh. <bookmark mark='c'/> Is he really a point four oh oh hitter? "
            "Nobody had hit that well over a whole season for almost thirty years."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def raw(self):
        d = load("baseball")
        P = baseball_plot(d)
        foot = fit_rows(VGroup(
            label(r"blue: \ each hitter's average over his first 45 at-bats", font_size=22, color=RAW),
            label(r"gold: \ his average over the rest of the season, \ 70 to 586 more at-bats", font_size=22, color=TRUE),
            label(r"the extremes came back towards the middle", font_size=22, color=GREY_A),
        ), 12.0, 0.22, [0, -2.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are all eighteen early averages, from Clemente's point four oh oh down to Max Alvis's "
            "point one five six. <bookmark mark='b'/> And here is what each player actually hit over the rest of the season, "
            "between seventy and nearly six hundred more at-bats. <bookmark mark='c'/> The truths are bunched far more "
            "tightly: the hot starts cooled and the cold starts warmed. Forty-five at-bats is a small sample, and the "
            "spread of the early averages is mostly luck."
        ) as vo:
            self.add(baseball_tag())
            self.play(FadeIn(P.lines[0]), FadeIn(P.names[0]), FadeIn(P.ticks))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in P.raw], lag_ratio=0.05), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(P.lines[2]), FadeIn(P.names[2]), LaggedStart(*[FadeIn(x, scale=0.5) for x in P.truth], lag_ratio=0.05),
                      FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def shrink(self):
        d = load("baseball")
        P = baseball_plot(d)
        gl = DashedLine([P.x_of(d["grand"]), 2.2, 0], [P.x_of(d["grand"]), -1.6, 0], color=GREY_B, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(rf"grand average: \ {d['grand']:.3f}", font_size=22, color=GREY_B),
            label(rf"James--Stein keeps {100 * (1 - d['B']):.0f}\% of each player's distance from it", font_size=22, color=SHRUNK),
            label(r"the amount is learned from the data", font_size=22, color=GREY_A),
        ), 12.0, 0.22, [0, -2.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Efron and Morris instead used the James–Stein estimator. Find the grand average of all "
            "eighteen players, point two six five. <bookmark mark='b'/> Then move every player towards it, keeping only "
            "about a fifth of his distance from the average. <bookmark mark='c'/> How far to move them is not chosen by "
            "hand: it is estimated from how spread out the eighteen early averages are, compared with how spread out they "
            "would be from luck alone."
        ) as vo:
            self.add(baseball_tag())
            self.play(FadeIn(P.lines[0]), FadeIn(P.names[0]), FadeIn(P.raw), FadeIn(P.ticks))
            vo.wait_until("a")
            self.play(Create(gl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(P.lines[1]), FadeIn(P.names[1]), LaggedStart(*[Create(a) for a in P.arrows], lag_ratio=0.05),
                      LaggedStart(*[FadeIn(x) for x in P.shrunk], lag_ratio=0.05), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def score(self):
        d = load("baseball")
        P = baseball_plot(d)
        rows = fit_rows(VGroup(
            label(rf"total squared error, \ own averages: \ {d['sse_mle']:.4f}", font_size=22, color=RAW),
            label(rf"total squared error, \ James--Stein: \ {d['sse_js']:.4f}", font_size=22, color=SHRUNK),
            label(rf"{d['ratio']:.1f} times smaller; \ closer for {d['closer']} of the 18 players", font_size=22, color=HIT),
        ), 12.0, 0.22, [0, -2.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now compare with the rest of the season. Using each player's own average, the total squared "
            "error is point oh seven five. <bookmark mark='b'/> With James–Stein it is point oh two two: <bookmark mark='c'/> "
            "three and a half times smaller, and closer for fifteen of the eighteen players. Shrinking every estimate towards "
            "the others was better than trusting each one."
        ) as vo:
            self.add(baseball_tag())
            self.play(FadeIn(P.lines), FadeIn(P.names), FadeIn(P.raw), FadeIn(P.shrunk), FadeIn(P.truth), FadeIn(P.ticks), FadeIn(P.arrows))
            self.play(LaggedStart(*[Create(l) for l in P.truth_links], lag_ratio=0.05))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k]))
        self.clear_scene()

    def paradox(self):
        rows = [
            cmath(r"\text{each } \theta_i", r":", r"\text{its own player, \ its own data}", font_size=30),
            cmath(r"\text{yet}", r":", r"\text{estimate each using all the others}", font_size=30),
            cmath(r"\text{Stein (1956)}", r":", r"\text{for 3 or more, \ the separate means are inadmissible}", font_size=30),
            cmath(r"\text{the resolution}", r":", r"\text{they come from one population: \ borrow strength}", font_size=28),
        ]
        rows[2][-1].set_color(RES)
        whys = [why(r"Clemente's average is about Clemente"), why(r"Alvis's hits change Clemente's estimate"),
                why(r"a better estimator exists, \ always"), why(r"Part 26: \ hierarchical models")]
        with self.voiceover(
            "<bookmark mark='a'/> It sounds paradoxical. Each player's true ability is about that player alone, and his own "
            "hits are the direct evidence. <bookmark mark='b'/> Yet the best estimate of Clemente's ability uses Max Alvis's "
            "hits too. <bookmark mark='c'/> Charles Stein proved in 1956 that with three or more means to estimate, the "
            "separate sample means are inadmissible: something always does better in total squared error. "
            "<bookmark mark='d'/> The resolution is that the players come from one population, and the population tells us "
            "how much an extreme early average is luck. That is the idea of this part: borrowing strength."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 25", font_size=34, color=GREY_B), label(r"Borrowing Strength", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"James--Stein, \ its risk, \ and SURE; \ empirical Bayes and Tweedie's formula",
            r"random effects, \ the linear mixed model, \ BLUPs; \ ML vs REML",
            r"inference for mixed models; \ longitudinal, \ nested and crossed designs",
            r"fixed vs random effects; \ GLMMs and league tables",
            r"small areas, \ meta-analysis, \ and item response theory",
        ], color=SHRUNK, font_size=26)
        prereq = note(r"prerequisites: \ Parts 15, \ 22 and 23").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.shrink}, \ \texttt{statkit.mixed}; \ the shrinkage plot").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part twenty-five: borrowing strength. <bookmark mark='b'/> We'll prove James–Stein's "
            "advantage and estimate its risk; see it as empirical Bayes; meet random effects and the linear mixed model with "
            "its best linear unbiased predictors; compare maximum likelihood with REML; do inference, including tests on "
            "the boundary; model growth curves and nested and crossed designs; decide between fixed and random effects; fit "
            "mixed models for binary outcomes and rank hospitals fairly; and apply all of it to small areas, meta-analysis and educational testing."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
