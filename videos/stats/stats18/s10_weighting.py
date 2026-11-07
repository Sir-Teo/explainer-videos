from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from explainer.stats.kit import survey as Sv
from videos.stats.stats18.common import *  # noqa: F403
from videos.stats.stats18.compute import adults, age_band, digest_returns, inc_band, raking_steps as margins_after

INC = [r"under 30k", r"30--100k", r"over 100k"]
AGE = [r"18--29", r"30--49", r"50--66", r"67+"]



class Weighting(VoiceoverScene):
    def construct(self):
        self.card()
        self.layers()
        self.cells()
        self.raking()
        self.result()
        self.why_not()
        self.board()
        self.costs()

    def card(self):
        card = chapter_card(9, r"Weighting", r"Making the sample look like the population", lit=(1940,), part=PART)
        with self.voiceover("Chapter nine. Weighting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def layers(self):
        rows = [
            cmath(r"w_i", r"=", r"\underbrace{1/\pi_i}_{\text{design}} \times \underbrace{a_i}_{\text{nonresponse}} \times \underbrace{g_i}_{\text{calibration}}",
                  font_size=32),
            cmath(r"a_i", r"=", r"1/\hat P(\text{respond} \mid \text{cell of } i)", font_size=30),
            cmath(r"g_i", r":", r"\text{make weighted totals match the census}", font_size=30),
            cmath(r"\hat{\bar y}", r"=", r"\textstyle\sum w_i y_i / \sum w_i", font_size=32),
        ]
        rows[3][2].set_color(WEIGHT)
        whys = [why(r"three layers"), why(r"respondents stand in for similar nonrespondents"),
                why(r"post-stratification, \ raking, \ GREG"), why(r"H\'ajek's weighted mean")]
        intro = label('Survey weights combine design, response and calibration', font_size=36)
        with self.voiceover(
            "A real survey's weight has three layers. <bookmark mark='a'/> The design weight, one over the inclusion "
            "probability; a nonresponse adjustment; and a calibration factor. <bookmark mark='b'/> The nonresponse "
            "adjustment divides by the estimated response rate within cells of similar people, so that respondents "
            "stand in for the nonrespondents who resemble them. <bookmark mark='c'/> Calibration then adjusts the "
            "weights so that weighted totals match what a census says: by age, sex, region, education. <bookmark "
            "mark='d'/> Estimates are weighted means. Weighting can't create information, but it can rebalance it."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def cells(self):
        rows = [
            cmath(r"\text{cells}", r":", r"\text{groups known for everyone sampled, \ responders or not}", font_size=28),
            cmath(r"\hat r_c", r"=", r"\text{responders} / \text{sampled, \ in cell } c", font_size=30),
            cmath(r"a_i", r"=", r"1/\hat r_{c(i)}", font_size=32),
            cmath(r"\text{or}", r":", r"\text{a logistic model of response: \ propensity weights}", font_size=28),
        ]
        rows[2][2].set_color(WEIGHT)
        whys = [why(r"e.g. region and age from the frame"), why(r"the response rate in each cell"),
                why(r"each responder stands for the nonresponders like them"), why(r"Part 14's logistic regression; \ Part 35 again")]
        intro = label('Estimate response propensities from observed frame variables', font_size=36)
        with self.voiceover(
            "How is the nonresponse adjustment made? <bookmark mark='a'/> Group everyone who was sampled into cells, "
            "using information known for responders and nonresponders alike, such as region and age from the frame. "
            "<bookmark mark='b'/> In each cell, the response rate is the share who answered. <bookmark mark='c'/> "
            "Each responder's weight is multiplied by one over their cell's response rate, so that they stand in for "
            "the nonresponders who resemble them. <bookmark mark='d'/> With many variables, a logistic regression of "
            "responding on the frame variables, Part 14's model, gives each person a propensity, and its inverse is "
            "the weight. The same idea, inverse probability weighting, returns in Part 35 for causal inference."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def bars(self, ax, shares, x0, color):
        w = ax.c2p(0.32, 0)[0] - ax.c2p(0, 0)[0]
        return VGroup(*[Rectangle(width=w, height=max(0.01, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), stroke_width=0, fill_color=color,
                                  fill_opacity=0.85).move_to(ax.c2p(x0 + k, 0), aligned_edge=DOWN) for k, v in enumerate(shares)])

    def raking(self):
        P = adults()
        R = digest_returns(P)
        steps, ti, ta = margins_after(P, R, 8)
        A = axes([-0.6, 2.6], [0, 0.75], x_length=5.0, y_length=3.4, xlabel=r"income band", ylabel=r"share",
                 yticks=[0, 0.25, 0.5, 0.75], center=[-3.4, 0.6, 0], font_size=18)
        B = axes([-0.6, 3.6], [0, 0.75], x_length=5.6, y_length=3.4, xlabel=r"age band", ylabel=r"share",
                 yticks=[0, 0.25, 0.5, 0.75], center=[3.2, 0.6, 0], font_size=18)
        ti_b = self.bars(A.ax, ti, 0.18, GREY_C)
        ta_b = self.bars(B.ax, ta, 0.18, GREY_C)
        si = self.bars(A.ax, steps[0][0], -0.18, WEIGHT)
        sa = self.bars(B.ax, steps[0][1], -0.18, WEIGHT)
        ni = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(A.ax.c2p(k, 0), DOWN, buff=0.12) for k, t in enumerate(INC)])
        na = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(B.ax.c2p(k, 0), DOWN, buff=0.12) for k, t in enumerate(AGE)])
        key = VGroup(label(r"grey: \ the census", font_size=20, color=GREY_B), label(r"blue: \ the weighted returns", font_size=20,
                                                                                       color=WEIGHT)).arrange(RIGHT, buff=0.8).move_to([0, 3.2, 0])
        counter = label(r"unweighted", font_size=22, color=WEIGHT).move_to([0, -2.3, 0])
        gap = max(np.max(np.abs(steps[-1][0]-ti)), np.max(np.abs(steps[-1][1]-ta)))
        with self.voiceover(
            "<bookmark mark='a'/> Here's calibration by raking, on the World's Digest returns. The returns are far "
            "too rich and too old: ten percent come from the bottom income band, against a third of the population, "
            "and twenty-four percent are over sixty-seven, against eighteen. <bookmark mark='b'/> W. Edwards Deming "
            "and Frederick Stephan, preparing the 1940 US census, invented the fix. Scale the weights so the income "
            "shares match the census exactly. <bookmark mark='c'/> That knocks the age shares out a little, so now "
            "scale them to match age. <bookmark mark='d'/> Income is slightly off again; repeat. <bookmark mark='e'/>"
            " The adjustments shrink rapidly: after four rounds both margins match to within a ten-thousandth. It's "
            "iterative proportional fitting, and it converges whenever a solution exists."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(ni), FadeIn(na), FadeIn(ti_b), FadeIn(ta_b), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(si), FadeIn(sa), FadeIn(counter))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                new_i = self.bars(A.ax, steps[k + 1][0], -0.18, WEIGHT)
                new_a = self.bars(B.ax, steps[k + 1][1], -0.18, WEIGHT)
                txt = label([r"after matching income", r"after matching age", r"income again"][k], font_size=22, color=WEIGHT).move_to(counter)
                self.play(Transform(si, new_i), Transform(sa, new_a), Transform(counter, txt), run_time=1.2)
            vo.wait_until("e")
            for k in range(4, 9):
                self.play(Transform(si, self.bars(A.ax, steps[k][0], -0.18, WEIGHT)),
                          Transform(sa, self.bars(B.ax, steps[k][1], -0.18, WEIGHT)), run_time=0.5)
            self.play(Transform(counter, MathTex(rf"\text{{largest gap after 4 rounds}}: {gap:.0e}", font_size=24, color=WEIGHT)
                                .move_to(counter)))
        self.clear_scene()

    def result(self):
        d = load("rake")
        A = axes([0.3, 0.62], [0, 3], x_length=9.0, y_length=2.4, xlabel=r"Blue's share", xticks=[0.35, 0.4, 0.45, 0.5, 0.55, 0.6],
                 center=[0.4, 0.6, 0], xfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        pts = [(d["truth"], r"the World", HIT), (d["raked"], r"raked: \ region, \ age, \ income", WEIGHT), (d["raw"], r"the returns", RESP)]
        dots = VGroup()
        for v, nm, col in pts:
            dt = Dot(ax.c2p(v, 1.2), radius=0.12, color=col)
            dots.add(VGroup(dt, label(nm, font_size=20, color=col).next_to(dt, UP, buff=0.15)))
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{raw}}\ {100 * d['raw']:.1f}\% \to \text{{raked}}\ {100 * d['raked']:.1f}\%;\ \ \text{{truth}}\ {100 * d['truth']:.1f}\%",
                    font_size=28),
            label(r"raking removed 45\% of the error", font_size=24, color=WEIGHT),
            MathTex(rf"\text{{Kish's }} n_{{\text{{eff}}}} = {d['neff']:,.0f}\ \text{{of}}\ {d['n']:,};\ \ \text{{weights from}}\ {d['w_range'][0]:.2f}\ \text{{to}}\ {d['w_range'][1]:.1f}",
                    font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The result. The raw returns said fifty-eight percent Blue. Raked to the census "
            "margins of region, age and income, they say forty-nine. The truth is thirty-eight. <bookmark mark='b'/> "
            "Weighting removed less than half the error. <bookmark mark='c'/> And it had a cost: the weights range "
            "from point one seven to nearly eight, and Kish's effective sample size falls from thirty-four and a half"
            " thousand to seventeen thousand. That's still plenty of precision. It's the bias that remains."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, scale=1.4) for x in dots], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def why_not(self):
        d = load("digest")
        rows = [
            cmath(r"\text{weighting assumes}", r":", r"\text{within a cell, \ responders resemble nonresponders}", font_size=28),
            cmath(r"\text{missing at random}", r":", r"P(\text{respond}) \text{ depends only on the cells}", font_size=28),
            cmath(r"\text{the World}", r":", rf"\text{{Blue response exceeds Red within income, age and region cells}}",
                  font_size=26),
            cmath(r"\text{so}", r":", r"\text{no weighting on income, \ age or region can fix it}", font_size=28),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"the cell is all we can see"), why(r"Rubin's MAR (Part 41)"),
                why(r"response depends on the answer itself"), why(r"missing not at random")]
        intro = label('Weighting needs adequate information about response', font_size=36)
        with self.voiceover(
            "Why can't weighting finish the job? <bookmark mark='a'/> It assumes that within each weighting cell, the"
            " people who responded resemble the people who didn't. <bookmark mark='b'/> That's Donald Rubin's "
            "condition of missing at random, which Part 41 makes precise: the chance of responding depends only on "
            "things we've weighted for. <bookmark mark='c'/> On the World it's false. Blue voters return their "
            "ballots more often than Red voters at every income, every age, in every region: the response depends on "
            "the answer itself. <bookmark mark='d'/> No reweighting on income, age or region can correct that. The "
            "Digest's nonresponse was missing not at random, the hardest kind."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=18) if r.part == 18 and "raked" in r.method]
        b = coverage_board(rows, lit_part=18, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> On the Board, two hundred fresh mailings: the raked Digest returns, with a plug-in "
            "independent-unit standard error using the weights, cover the truth zero times. That formula is not a "
            "full design-based variance calculation, and cannot remove the eleven-point bias."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
        self.wait(1.0)
        self.clear_scene()

    def costs(self):
        rows = fit_rows(VGroup(
            label(r"weights correct for the variables you weight on, \ and only those", font_size=24),
            label(r"Kish weight-only diagnostic: \ Kish's $n_{\text{eff}} = (\sum w)^2 / \sum w^2$", font_size=24, color=GREY_A),
            label(r"choose weighting variables that predict both response and the answer", font_size=24, color=HIT),
            label(r"a probability sample with weights beats a huge self-selected one", font_size=24, color=OBS),
            label(r"the 2016 polls missed one such variable: \ education", font_size=24, color=RES),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: weights correct for the variables you weight on, and only those. <bookmark "
            "mark='b'/> Kish's effective sample size describes weight dispersion under a working independent, "
            "equal-variance model. It does not measure selection bias or the precision gains from useful calibration "
            "variables. <bookmark mark='c'/> The best weighting variables predict both who responds and what they "
            "answer. <bookmark mark='d'/> A probability sample, weighted for its modest nonresponse, beats a huge "
            "self-selected one. <bookmark mark='e'/> And forgetting one such variable has consequences, as the "
            "American polls of 2016 found with education, which is the last chapter's story."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
