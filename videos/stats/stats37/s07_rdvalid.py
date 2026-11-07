from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403


class RDValid(VoiceoverScene):
    def construct(self):
        self.card()
        self.remark()
        self.density()
        self.balance()
        self.fuzzy_plot()
        self.fuzzy_math()
        self.elections()
        self.checklist()

    def card(self):
        card = chapter_card(6, r"RD validity", r"What a cutoff can hide", lit=(2008,), part=PART)
        with self.voiceover("Chapter six. Is the discontinuity valid?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def remark(self):
        rows = fit_rows(VGroup(
            label(r"precise sorting can undermine continuity of potential outcomes", font_size=26, color=MISSC),
            label(r"in the World's second version, \ teachers re-mark scripts that fell just short", font_size=26),
            label(r"35\% of the scripts scoring 56 to 59.9 are pushed to 60 or just above", font_size=26, color=CUTC),
            label(r"then those just above the line include students who would have been just below", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One threat to the design is precise sorting across the cutoff, which can make "
            "potential-outcome means discontinuous there. Validity also needs consistency and exclusion of other "
            "discontinuous changes; no single sorting test establishes all of these. <bookmark mark='b'/> In a second"
            " version of the World's scholarship, teachers, knowing what is at stake, re-mark the scripts that fell "
            "just short. <bookmark mark='c'/> A third of the scripts scoring between fifty-six and sixty are found a "
            "few extra marks and pushed over the line. <bookmark mark='d'/> Now the students just above the line "
            "include weaker students who would have been below it."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def density(self):
        d = load("rdvalid")
        mids = np.asarray(d["mids"], float)
        dc, dr = np.asarray(d["dens_clean"], float), np.asarray(d["dens_rem"], float)
        A = axes([40, 80], [0, 0.07], x_length=8.0, y_length=4.2, xlabel=r"exam score", ylabel=r"density",
                 xticks=[40, 50, 60, 70, 80], yticks=[0, 0.02, 0.04, 0.06], yfmt=lambda v: f"{v:g}", center=[-1.6, 0.2, 0])
        ax = A.ax
        bc = bars_at(ax, mids, dc, 0.45, Y0C, opacity=0.7)
        br = bars_at(ax, mids, dr, 0.45, MISSC, opacity=0.7)
        cut = DashedLine(ax.c2p(60, 0), ax.c2p(60, 0.07), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"McCrary (2008): \ does the density jump at the cutoff?", font_size=22, color=TAUC),
            label(rf"honest marking: \ $\hat\theta$ = {d['clean']['theta']:.3f}, \ $z$ = {d['clean']['z']:.1f}", font_size=22, color=Y0C),
            label(rf"re-marked: \ $\hat\theta$ = {d['rem']['theta']:.2f}, \ $z$ = {d['rem']['z']:.0f}", font_size=22, color=MISSC),
            label(rf"a log jump of {d['rem']['theta']:.2f}: \ {np.exp(d['rem']['theta']):.1f} times as many just above", font_size=22, color=GREY_A),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Justin McCrary's test of 2008 looks for the fingerprint: a jump in the density of "
            "the running variable at the cutoff. It fits a smooth density on each side and compares the logs at the "
            "line. <bookmark mark='b'/> With honest marking this coarse histogram shows no clear jump. Scores are "
            "rounded to tenths; the continuous-density test here is a teaching approximation. <bookmark mark='c'/> "
            "After re-marking, a gap opens just below the line and a heap appears just above it. <bookmark mark='d'/>"
            " The estimated log jump is " + say(d["rem"]["theta"], 2) + ": almost three times as many "
            "scripts just above the line as just below, a z statistic of " + str(round(d["rem"]["z"])) + "."
        ) as vo:
            self.add(schol_tag())
            self.play(FadeIn(A), Create(cut), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bc), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeOut(bc), FadeIn(br), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def balance(self):
        d = load("rdvalid")
        bc, br, o = d["bal_clean"], d["bal_rem"], d["out_rem"]
        rows = fit_rows(VGroup(
            label(r"second check: \ pre-treatment covariates should not jump \ (here: \ aptitude)", font_size=26, color=TAUC),
            label(rf"honest marking: \ jump {bc['tau']:+.3f} \ (SE {bc['se']:.3f})", font_size=26, color=Y0C),
            label(rf"re-marked: \ jump {br['tau']:+.3f} \ (SE {br['se']:.3f}): \ a hint, \ $z$ = {br['tau'] / br['se']:.1f}", font_size=26, color=MISSC),
            label(rf"the RD estimate after re-marking: \ {o['tau']:.2f}, \ against a truth of 3.0", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A second check: characteristics fixed before the exam should not jump at the line. In the "
            "World we can use aptitude itself. <bookmark mark='b'/> With honest marking, no jump. <bookmark mark='c'/> After "
            "re-marking, aptitude is lower just above the line, but only by a little: a z statistic of "
            + say(br["tau"] / br["se"], 1) + ", which would not alarm most analysts. Only three and a half percent of "
            "students were moved. <bookmark mark='d'/> Yet the estimated effect of the scholarship falls to "
            + say(o["tau"], 2) + ", from a truth of three. The density test shouted; the covariate test barely whispered."
        ) as vo:
            self.add(schol_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def fuzzy_plot(self):
        d = load("rdvalid")
        tm, tmeans = np.asarray(d["take_mids"], float), np.asarray(d["take_means"], float)
        A = axes([30, 90], [0, 1], x_length=8.0, y_length=4.0, xlabel=r"exam score", ylabel=r"share with a scholarship",
                 xticks=[30, 45, 60, 75, 90], yticks=[0, 0.5, 1], yfmt=lambda v: f"{v:g}", center=[-1.6, 0.2, 0])
        k = (tm >= 30) & (tm <= 90)
        L = CutoffLens(A.ax, tm[k], tmeans[k], 60)
        side = fit_rows(VGroup(
            label(r"fuzzy: \ 80\% of those offered take it up", font_size=22),
            label(r"and 5\% below the line win one on appeal", font_size=22),
            label(rf"jump in take-up: \ {d['fuzzy']['jump_d']:.2f}", font_size=22, color=CUTC),
            label(rf"takers vs the rest: \ +{d['naive_took']:.1f} thousand", font_size=22, color=MISSC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Often the cutoff only changes the chance of treatment. In the World, eighty percent of "
            "those offered a scholarship take it up; <bookmark mark='b'/> and five percent of those below the line win one "
            "on appeal. <bookmark mark='c'/> The share with a scholarship jumps by " + say(d["fuzzy"]["jump_d"], 2)
            + " at sixty, not by one. This is a fuzzy discontinuity. <bookmark mark='d'/> Comparing those who took a "
            "scholarship with those who did not gives a nonsensical " + say(d["naive_took"], 1) + " thousand."
        ) as vo:
            self.add(schol_tag())
            self.play(FadeIn(A), FadeIn(L), FadeIn(side[0]))
            for k_, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k_ + 1]))
        self.clear_scene()

    def fuzzy_math(self):
        d = load("rdvalid")
        f = d["fuzzy"]
        rows = [
            cmath(r"\tau_{\text{fuzzy}}", r"=", r"\dfrac{\text{jump in } E[Y \mid R]}{\text{jump in } P(D{=}1 \mid R)}", font_size=32),
            cmath(r"\text{the cutoff}", r":", r"\text{an instrument, \ valid only at } c", font_size=30),
            cmath(r"\text{the World}", r":", rf"\dfrac{{{f['jump_y']:.2f}}}{{{f['jump_d']:.2f}}} = {f['tau']:.2f} \ ({f['se']:.2f})", font_size=32),
            cmath(r"\text{for}", r":", r"\text{compliers at the cutoff: \ take it if and only if offered}", font_size=30),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"a local Wald ratio"), why(r"Part 35's LATE, \ at a point"), why(r"local quadratics; \ truth 3.0"),
                why(r"Hahn, \ Todd \& van der Klaauw (2001)")]
        with self.voiceover(
            "<bookmark mark='a'/> The fuzzy estimate divides the jump in outcomes by the jump in take-up: a Wald ratio, at "
            "the cutoff. <bookmark mark='b'/> Crossing the line is an instrument for the scholarship, but only right at the "
            "line. <bookmark mark='c'/> In the World the jump in earnings is " + say(f["jump_y"], 2) + ", the jump in take-up "
            + say(f["jump_d"], 2) + ", and their ratio " + say(f["tau"], 2) + ", against a truth of three. <bookmark mark='d'/> With a nonzero first-stage jump, local exclusion, "
            "monotonicity and continuity assumptions, it identifies the effect for compliers at the cutoff: students "
            "who take a scholarship if and only if they are offered one."
        ) as vo:
            self.add(schol_tag())
            intro=label('Fuzzy discontinuity is a local instrumental-variable design',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def elections(self):
        rows = fit_rows(VGroup(
            label(r"Lee (2008): \ US House elections, \ running variable = the vote margin", font_size=26, color=TAUC),
            label(r"a party that barely wins is otherwise like one that barely loses: \ the incumbency advantage", font_size=26),
            label(r"Caughey \& Sekhon (2011): \ in the closest post-war House races, \ incumbents won too often", font_size=26, color=MISSC),
            label(r"Eggers et al. (2015): \ that sorting is rare elsewhere: \ check each application", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The most famous discontinuity is political. David Lee, in 2008, took the vote margin in "
            "elections to the United States House of Representatives as the running variable. <bookmark mark='b'/> A party "
            "that barely won should be otherwise like one that barely lost, so the jump in its chance of winning the next "
            "election measures the advantage of incumbency. <bookmark mark='c'/> Devin Caughey and Jasjeet Sekhon found in "
            "2011 that in the very closest post-war House races, incumbents won far more often than chance would allow, as "
            "if close contests could be nudged. <bookmark mark='d'/> Andrew Eggers and colleagues found that such sorting is "
            "rare in other countries and offices. The lesson is to check each application, not the design in general."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def checklist(self):
        rows = fit_rows(VGroup(
            label(r"1. \ the density of the running variable: \ smooth at the cutoff", font_size=26, color=CUTC),
            label(r"2. \ pre-treatment covariates: \ no jumps", font_size=26, color=Y0C),
            label(r"3. \ placebo cutoffs: \ no jumps where nothing happens", font_size=26, color=TAUC),
            label(r"4. \ bandwidths and polynomial orders: \ the answer should not hinge on them", font_size=26, color=BANDC),
            label(r"5. \ donut sensitivity: \ changes extrapolation; does not automatically repair sorting", font_size=26, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So every discontinuity should come with checks. The density of the running "
            "variable, smooth through the cutoff. <bookmark mark='b'/> Covariates fixed before treatment, with no "
            "jumps. <bookmark mark='c'/> Placebo cutoffs, at scores where nothing happens, with no effects. <bookmark"
            " mark='d'/> An answer that does not hinge on the bandwidth or the polynomial order, and never a global "
            "polynomial of high degree, which Andrew Gelman and Guido Imbens warned in 2019 can manufacture jumps. "
            "<bookmark mark='e'/> A donut can be a sensitivity check: dropping the nearest scores changes the "
            "extrapolation problem and may lose local identification. It does not automatically repair manipulation."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
