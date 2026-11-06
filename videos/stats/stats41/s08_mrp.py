from __future__ import annotations

import numpy as np

from videos.stats.stats41.common import *  # noqa: F403


class MRP(VoiceoverScene):
    def construct(self):
        self.card()
        self.xbox()
        self.idea()
        self.model()
        self.sample()
        self.result()
        self.regions()
        self.yougov()
        self.limits()
        self.cousins()
        self.board()

    def card(self):
        card = chapter_card(7, r"MRP", r"Multilevel regression and poststratification", lit=(1997, 2015), part=PART)
        with self.voiceover("Chapter seven. Multilevel regression and poststratification."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def xbox(self):
        rows = fit_rows(VGroup(
            label(r"2012: \ an opt-in poll on Microsoft's Xbox, \ in the 45 days before the US election", font_size=26, color=TAUC),
            label(r"respondents: \ 93\% men, \ 65\% aged 18--29; \ the raw numbers favoured Romney", font_size=26, color=MNC),
            label(r"Wang, \ Rothschild, \ Goel \& Gelman (2015): \ MRP turned it into an accurate forecast", font_size=26, color=MIC),
            label(r"the most biased sample imaginable, \ fixed by modelling, \ not by sampling", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2012, players of Microsoft's Xbox game console could answer a daily poll on the US "
            "presidential election. <bookmark mark='b'/> The respondents were ninety-three percent men and two thirds aged "
            "eighteen to twenty-nine, and the raw numbers favoured Romney. <bookmark mark='c'/> Wei Wang, David Rothschild, "
            "Sharad Goel and Andrew Gelman showed that multilevel regression and poststratification turned this into a "
            "forecast as accurate as the major polls. <bookmark mark='d'/> About the most biased sample imaginable, repaired "
            "by modelling rather than sampling."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def idea(self):
        rows = [
            cmath(r"\text{cells } c", r":", r"\text{age} \times \text{sex} \times \text{region} \times \text{income}", font_size=30),
            cmath(r"\hat\theta_c", r":", r"\text{the opinion in cell } c, \ \text{from a model}", font_size=30),
            cmath(r"\hat\theta", r"=", r"\textstyle\sum_c N_c\, \hat\theta_c \big/ \textstyle\sum_c N_c", font_size=32),
            cmath(r"\text{assumption}", r":", r"\text{within a cell, \ respondents are like everyone else}", font_size=30),
        ]
        rows[2][-1].set_color(MIC)
        whys = [why(r"Part 18's strata"), why(r"too many cells to average"), why(r"poststratify with census counts"),
                why(r"MAR, \ given the cells")]
        with self.voiceover(
            "<bookmark mark='a'/> The idea. Divide the population into cells by the variables that drive both "
            "participation and opinion. <bookmark mark='b'/> Estimate the opinion in each cell. With hundreds of cells, "
            "many have few or no respondents, so a raw average per cell is useless; a model is needed. <bookmark "
            "mark='c'/> Then weight each cell's estimate by its size in the population, from a census: Part eighteen's "
            "poststratification. <bookmark mark='d'/> The assumption is missing at random given the cells: within a cell, "
            "those who answer are like those who do not."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def model(self):
        rows = [
            cmath(r"\text{logit}\, P(y_i = 1)", r"=", r"\alpha_0 + \alpha^{\text{age}}_{a[i]} + \alpha^{\text{sex}}_{s[i]} + \alpha^{\text{reg}}_{r[i]} + \alpha^{\text{inc}}_{k[i]}", font_size=28),
            cmath(r"\alpha^{\text{reg}}_r", r"\sim", r"N(0, \tau_{\text{reg}}^2), \ \ \text{etc.}", font_size=30),
            cmath(r"\text{small cells}", r":", r"\text{pulled toward what similar cells say}", font_size=30),
            cmath(r"\tau", r":", r"\text{estimated: \ how different the groups really are}", font_size=30),
        ]
        rows[1][-1].set_color(MIC)
        whys = [why(r"Gelman \& Little (1997)"), why(r"random effects"), why(r"Part 25's partial pooling"), why(r"from the data")]
        with self.voiceover(
            "<bookmark mark='a'/> Andrew Gelman and Thomas Little's model of 1997 is a logistic regression with an effect "
            "for each age group, sex, region and income group, <bookmark mark='b'/> each set of effects drawn from a normal "
            "distribution with its own spread. <bookmark mark='c'/> Small cells borrow strength from similar ones, Part "
            "twenty-five's partial pooling, <bookmark mark='d'/> and the spreads, estimated from the data, decide how much."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sample(self):
        d = load("mrp")
        c = d["comp"]
        rows = [[r"the World's opt-in poll \ (3,000)", r"sample", r"adult population"],
                [r"aged under 30", f"{100 * c['sample_young']:.0f}\\%", f"{100 * c['pop_young']:.0f}\\%"],
                [r"men", f"{100 * c['sample_male']:.0f}\\%", f"{100 * c['pop_male']:.0f}\\%"],
                [r"support for Blue", f"{100 * d['raw']:.1f}\\%", f"{100 * d['truth']:.1f}\\%"]]
        tab = table_rows(rows, font_size=28, col_buff=1.2, row_buff=0.36, colors=[GREY_A, None, None, MNC]).move_to([0, 0.8, 0])
        foot = label(r"joining depends on age, \ sex, \ region and income, \ which also predict the vote", font_size=24, color=GREY_A).move_to([0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World holds an election in which " + say(100 * d["truth"], 1) + " percent of adults "
            "support the challenger, Blue. An online poll invites anyone to join; three thousand do. <bookmark mark='b'/> "
            "Twice as many are under thirty as in the population, and two thirds are men. <bookmark mark='c'/> The raw poll "
            "puts Blue at " + say(100 * d["raw"], 1) + " percent, four points too high, because the young, the men and the "
            "well-off who join lean Blue."
        ) as vo:
            self.add(poll_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
        self.clear_scene()

    def result(self):
        d = load("mrp")
        t = d["truth"]
        A = axes([0.35, 0.45], [0, 3.5], x_length=8.0, y_length=3.6, xlabel=r"support for Blue", ylabel=r"",
                 xticks=[0.35, 0.375, 0.4, 0.425, 0.45], yticks=[], xfmt=lambda v: f"{v:.3f}", center=[0.8, 0.2, 0])
        ax = A.ax
        truth = DashedLine(ax.c2p(t, 0), ax.c2p(t, 3.5), color=TRUEC, stroke_width=2.5)
        items = [(r"raw poll", d["raw"], (d["raw"] - 1.645 * d["raw_se"], d["raw"] + 1.645 * d["raw_se"]), MNC),
                 (r"raked weights", d["raked"], None, IPWC),
                 (r"MRP", d["mrp"], tuple(d["mrp_ci"]), MIC)]
        marks = VGroup()
        for k, (nm, v, ci, col) in enumerate(items):
            yv = 2.8 - k * 1.0
            g = VGroup(Dot(ax.c2p(v, yv), radius=0.1, color=col), label(nm, font_size=24, color=col).next_to(ax.c2p(0.35, yv), LEFT, buff=0.25))
            if ci:
                g.add(Line(ax.c2p(ci[0], yv), ax.c2p(ci[1], yv), color=col, stroke_width=5))
            marks.add(g)
        with self.voiceover(
            "<bookmark mark='a'/> Against the truth, in gold. <bookmark mark='b'/> The raw poll is " + say(100 * d["raw"], 1)
            + " percent, with a confident interval that misses. <bookmark mark='c'/> Raking the weights to the population's "
            "age, sex, region and income margins brings it to " + say(100 * d["raked"], 1) + ". <bookmark mark='d'/> MRP, with "
            "six age groups, two sexes, ten regions and five income groups, gives " + say(100 * d["mrp"], 1) + " percent, "
            "within half a point of the truth, and its ninety percent interval covers it."
        ) as vo:
            self.add(poll_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(truth))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(marks[k]))
        self.clear_scene()

    def regions(self):
        d = load("mrp")["by_region"]
        tr = np.asarray(d["truth"], float)
        raw = np.array([np.nan if v is None else v for v in d["raw"]], float)
        mr = np.asarray(d["mrp"], float)
        A = axes([0.25, 0.55], [0.25, 0.55], x_length=4.6, y_length=4.6, xlabel=r"true support, \ by region", ylabel=r"estimate",
                 xticks=[0.3, 0.4, 0.5], yticks=[0.3, 0.4, 0.5], xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", center=[-3.2, 0.0, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(0.25, 0.25), ax.c2p(0.55, 0.55), color=GREY_B, stroke_width=2)
        s_raw = scatter(ax, tr, raw, MNC, 0.08)
        s_mrp = scatter(ax, tr, mr, MIC, 0.08)
        r1 = float(np.sqrt(np.nanmean((raw - tr) ** 2)))
        r2 = float(np.sqrt(np.mean((mr - tr) ** 2)))
        side = fit_rows(VGroup(
            label(r"the ten regions", font_size=22),
            label(rf"orange: \ raw regional shares \ (RMSE {100 * r1:.1f} points)", font_size=22, color=MNC),
            label(rf"green: \ MRP \ (RMSE {100 * r2:.1f} points)", font_size=22, color=MIC),
            label(rf"region sizes in the poll: \ {min(d['n'])} to {max(d['n'])}", font_size=22, color=GREY_A),
            label(r"small regions are pulled toward the island: \ only a modest gain", font_size=22, color=TAUC),
        ), 5.0, 0.42, [3.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> MRP is also used for small areas. The ten regions, true support against estimate. "
            "<bookmark mark='b'/> The raw regional shares mostly sit above the diagonal, missing by " + say(100 * r1, 1)
            + " points on average, because each region's joiners are skewed the same way. <bookmark mark='c'/> MRP removes "
            "that shared skew, missing by " + say(100 * r2, 1) + ". <bookmark mark='d'/> The gain is modest, because some "
            "regions had only sixty respondents, and the model pulls them toward the island as a whole, while the World's "
            "regions differ for reasons no census variable explains. <bookmark mark='e'/> Small-area estimates improve most "
            "when area-level predictors, such as past votes, explain the differences between areas; with them, MRP has "
            "estimated opinion in every US state and British constituency from national polls."
        ) as vo:
            self.add(poll_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(diag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(s_raw), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(s_mrp), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def limits(self):
        rows = fit_rows(VGroup(
            label(r"MRP corrects only for what defines the cells", font_size=26, color=MNC),
            label(r"if joiners differ from non-joiners within a cell, \ no model can see it", font_size=26),
            label(r"census counts must exist for the cells: \ the joint table, \ or a model for it", font_size=26, color=GREY_A),
            label(r"and intervals must carry the model's uncertainty, \ including $\tau$", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The limits. MRP corrects only for what defines the cells. <bookmark mark='b'/> If those who "
            "join an online poll differ from those who do not even within a cell, for example by political interest, "
            "nothing in the model can see it. <bookmark mark='c'/> It needs population counts for every cell, the joint "
            "table, which censuses do not always publish. <bookmark mark='d'/> And honest intervals must carry all the "
            "model's uncertainty, including the spreads of the group effects."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("opt-in", "MRP")
        text = (
            "<bookmark mark='a'/> The Board, over two hundred opt-in polls of fifteen hundred. The raw share's interval "
            "almost never covers the truth. <bookmark mark='b'/> MRP's covers far more often, but still short of ninety "
            "percent: its approximate posterior, which fixes the group spreads at their estimates, is too narrow, and some "
            "selection remains within the cells. A huge improvement, and still not a promise kept."
        )
        show_board(self, rows, text, [("a", [0]), ("b", [1])])

    def yougov(self):
        rows = fit_rows(VGroup(
            label(r"2017: \ YouGov's MRP model of the UK election, \ constituency by constituency", font_size=26, color=TAUC),
            label(r"most polls expected a large Conservative majority; \ the model foresaw a hung parliament", font_size=26, color=MIC),
            label(r"which is what happened", font_size=26, color=MIC),
            label(r"and in other elections MRP has missed: \ a model, \ not a guarantee", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> MRP entered public life in Britain in 2017, when the polling firm YouGov published "
            "constituency-by-constituency estimates from a model of this kind. <bookmark mark='b'/> Most polls expected a "
            "large Conservative majority; the model suggested a hung parliament, <bookmark mark='c'/> which is what "
            "happened. <bookmark mark='d'/> It has missed in other elections. MRP is a model, and its accuracy depends on "
            "the cells capturing who answers."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def cousins(self):
        rows = fit_rows(VGroup(
            label(r"MRP's cousins: \ small-area estimation \ (Fay \& Herriot 1979, \ Part 25)", font_size=26, color=TAUC),
            label(r"area-level models: \ shrink each area's direct estimate toward a regression", font_size=26, color=None),
            label(r"unit-level models: \ predict every person, \ then add up: \ MRP", font_size=26, color=MIC),
            label(r"both trade bias for variance, \ and both need honest uncertainty", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> MRP belongs to a larger family, small-area estimation, which we met in Part twenty-five with "
            "Fay and Herriot's model. <bookmark mark='b'/> Area-level models shrink each area's direct survey estimate "
            "toward a regression on area characteristics. <bookmark mark='c'/> Unit-level models, like MRP, predict every "
            "person in the population and add them up. <bookmark mark='d'/> Both trade a little bias for a lot of "
            "variance, and both need intervals that carry the model's uncertainty."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

