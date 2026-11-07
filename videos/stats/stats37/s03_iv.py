from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403


class Instruments(VoiceoverScene):
    def construct(self):
        self.card()
        self.wright()
        self.graph()
        self.quarters()
        self.wald()
        self.tsls()
        self.lottery()

    def card(self):
        card = chapter_card(2, r"Instrumental variables", r"A nudge that reaches the outcome only through the treatment",
                            lit=(1928, 1990, 1991), part=PART)
        with self.voiceover("Chapter two. Instrumental variables."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def wright(self):
        rows = fit_rows(VGroup(
            label(r"Philip Wright (1928): \ \emph{The Tariff on Animal and Vegetable Oils}, \ Appendix B", font_size=26, color=TAUC),
            label(r"price and quantity are set together by supply and demand: \ regressing one on the other finds neither", font_size=26),
            label(r"a variable that shifts supply but not demand \ (the weather on the flax fields) \ traces out the demand curve", font_size=26, color=IVC),
            label(r"the slope: \ the change in quantity over the change in price that the weather caused", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The idea first appears in an appendix to a 1928 book about tariffs on butter and flaxseed, "
            "by the economist Philip Wright, probably with help from his son Sewall, the inventor of path diagrams in Part "
            "thirty-six. <bookmark mark='b'/> Price and quantity are set together by supply and demand, so regressing one on "
            "the other estimates neither curve. <bookmark mark='c'/> But a variable that shifts supply without affecting "
            "demand, such as the weather where flax is grown, moves the market along the demand curve. <bookmark mark='d'/> "
            "The demand curve's slope is then the change in quantity divided by the change in price that the weather caused."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def graph(self):
        G = CausalGraph({"Z": (-3.2, 0), "D": (-0.6, 0), "Y": (2.0, 0), "U": (0.7, 1.8)},
                        [("Z", "D"), ("D", "Y"), ("U", "D"), ("U", "Y")], center=[-2.0, 0.0, 0], scale=0.95,
                        colors={"Z": IVC, "D": Y1C, "Y": Y0C, "U": MISSC},
                        labels={"Z": r"$Z$", "D": r"$D$", "Y": r"$Y$", "U": r"$U$"})
        side = fit_rows(VGroup(
            label(r"relevance: \ $Z$ moves $D$ \ (checkable)", font_size=22, color=IVC),
            label(r"independence: \ $Z$ as good as random", font_size=22, color=BANDC),
            label(r"exclusion: \ no arrow $Z \to Y$, \ none through $U$", font_size=22, color=MISSC),
            label(r"monotonicity: \ no defiers \ $\Rightarrow$ \ the LATE \ (Part 35)", font_size=22, color=TAUC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> As a causal graph: an instrument Z, a treatment D, an outcome Y, and unmeasured "
            "confounders U of the treatment and the outcome. No adjustment can close the back door through U. The "
            "instrument instead needs three things. <bookmark mark='b'/> Relevance: it moves the treatment, which the"
            " data can check. <bookmark mark='c'/> Independence: it is as good as randomly assigned. <bookmark "
            "mark='d'/> Exclusion: it affects the outcome only through the treatment, with no arrow of its own and no"
            " path through U. That one cannot be checked. <bookmark mark='e'/> With effects that differ between "
            "people, Part thirty-five added monotonicity for binary treatment and found the complier average effect. "
            "With years of schooling, a continuous treatment, extra structural or weighted marginal-effect conditions"
            " are needed; the World uses a constant log-wage effect."
        ) as vo:
            self.play(FadeIn(G))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k]))
        self.clear_scene()

    def quarters(self):
        d = load("iv")
        bq = d["byq"]
        A = axes([0.5, 4.5], [12.3, 12.7], x_length=4.6, y_length=3.4, xlabel=r"quarter of birth", ylabel=r"years of schooling",
                 xticks=[1, 2, 3, 4], yticks=[12.3, 12.5, 12.7], yfmt=lambda v: f"{v:.1f}", center=[-3.6, 0.3, 0])
        B = axes([0.5, 4.5], [6.92, 6.96], x_length=4.6, y_length=3.4, xlabel=r"quarter of birth", ylabel=r"mean log weekly wage",
                 xticks=[1, 2, 3, 4], yticks=[6.92, 6.94, 6.96], yfmt=lambda v: f"{v:.2f}", center=[2.6, 0.3, 0])
        sch = [bq[str(j)]["school"] for j in (1, 2, 3, 4)]
        wag = [bq[str(j)]["wage"] for j in (1, 2, 3, 4)]
        b1 = bars_at(A.ax, [1, 2, 3, 4], sch, 0.6, Y1C, opacity=0.8, highlight=[0], hcolor=IVC)
        b2 = bars_at(B.ax, [1, 2, 3, 4], wag, 0.6, Y0C, opacity=0.8, highlight=[0], hcolor=IVC)
        foot = fit_rows(VGroup(
            label(r"born January--March: \ older at school entry, \ reach the leaving age with less schooling", font_size=22, color=IVC),
            label(r"axes zoomed: \ the differences are a tenth of a year and one percent of wages", font_size=20, color=GREY_B),
        ), 12.4, 0.25, [0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1991 Angrist and Alan Krueger found an instrument in the calendar. Children "
            "start school in the year they turn six, but may leave at sixteen, so those born early in the year are "
            "older when they start and reach the leaving age having done less school. The World's survey of two "
            "hundred thousand adults has the same rule. <bookmark mark='b'/> People born in the first quarter have "
            "about a seventh of a year less schooling than the rest. <bookmark mark='c'/> And their wages are about "
            "one percent lower. <bookmark mark='d'/> The World constructs quarter of birth independently and makes it"
            " affect wages only through schooling. In real data, birth season, family background and other channels "
            "make these assumptions substantive questions. Note how small these differences are; we will return to "
            "that."
        ) as vo:
            self.add(survey_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(B), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(b1))
            vo.wait_until("c")
            self.play(FadeIn(b2))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def wald(self):
        d = load("iv")
        rows = [
            cmath(r"\text{first stage}", r":", rf"E[D \mid Z{{=}}1] - E[D \mid Z{{=}}0] = {d['dS']:.3f}", font_size=30),
            cmath(r"\text{reduced form}", r":", rf"E[Y \mid Z{{=}}1] - E[Y \mid Z{{=}}0] = {d['dW']:.4f}", font_size=30),
            cmath(r"\hat\beta_{\text{Wald}}", r"=", rf"\dfrac{{{d['dW']:.4f}}}{{{d['dS']:.3f}}} = {d['wald']:.3f}", font_size=32),
            cmath(r"\text{OLS}", r"=", rf"{d['full1']['ols']:.3f}", font_size=30),
        ]
        rows[2][-1].set_color(BANDC)
        rows[3][-1].set_color(MISSC)
        whys = [why(r"quarter 1 against the rest"), why(r"the instrument's effect on wages"),
                why(rf"the World's truth: \ {d['truth']:.3f} per year"), why(r"ability raises both schooling and wages")]
        with self.voiceover(
            "<bookmark mark='a'/> With a binary instrument the estimate is a ratio, due to the statistician Abraham Wald. The "
            "first stage: being born in the first quarter changes schooling by minus " + say(-d["dS"], 3) + " years. "
            "<bookmark mark='b'/> The reduced form: it changes log wages by minus " + say(-d["dW"], 4) + ". <bookmark "
            "mark='c'/> If the instrument acts only through schooling, the wage change per year of schooling is their ratio, "
            + say(d["wald"], 3) + ", and the World's truth is point zero seven five log points per year, about seven point eight percent. "
            "<bookmark mark='d'/> Ordinary least squares says " + say(d["full1"]["ols"], 2) + ", more than twice as much, because ability raises both "
            "schooling and wages."
        ) as vo:
            self.add(survey_tag())
            intro=label('The Wald ratio divides reduced form by first stage',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tsls(self):
        d = load("iv")
        f1, f3 = d["full1"], d["full3"]
        rows = [
            cmath(r"\hat D", r"=", r"P_Z D \quad \text{(fit } D \text{ on the instruments)}", font_size=30),
            cmath(r"\hat\beta_{\text{2SLS}}", r"=", r"(\hat D^\top \hat D)^{-1} \hat D^\top Y = (D^\top P_Z D)^{-1} D^\top P_Z Y", font_size=30),
            cmath(r"\text{SE}", r":", r"\text{from } Y - D\hat\beta, \ \text{not from the second-stage residuals}", font_size=28),
            cmath(r"\text{three quarters}", r":", rf"\hat\beta = {f3['beta']:.3f}\ ({f3['se']:.3f}), \ F = {f3['F']:.0f}", font_size=30),
        ]
        rows[1][-1].set_color(IVC)
        whys = [why(r"include or partial out exogenous controls and a constant"), why(r"Theil (1953), \ Basmann (1957)"),
                why(r"a classic slip"), why(r"200,000 adults")]
        with self.voiceover(
            "<bookmark mark='a'/> With several instruments, the general recipe is two-stage least squares, two projections. "
            "First fit the treatment on the instruments, keeping only the part of schooling that the calendar explains. "
            "<bookmark mark='b'/> Then regress wages on that fitted part. <bookmark mark='c'/> The standard error must use the "
            "residuals with the actual schooling, not the fitted one; running the two stages by hand gets this wrong. "
            "<bookmark mark='d'/> With all three quarter indicators in the full survey, the estimate is " + say(f3["beta"], 3)
            + ", with a standard error of " + say(f3["se"], 3) + ", and a first-stage F statistic of " + str(round(f3["F"]))
            + "."
        ) as vo:
            intro=label('Two-stage least squares projects treatment onto valid instruments',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lottery(self):
        rows = fit_rows(VGroup(
            label(r"Angrist (1990): \ the Vietnam draft lottery ranked birthdays at random", font_size=26, color=TAUC),
            label(r"a low number made service more likely: \ an instrument for being a veteran", font_size=26, color=IVC),
            label(r"IV estimate for white draft compliers: \ earnings about 15\% lower", font_size=26, color=BANDC),
            label(r"the effect for compliers: \ men who served because their number came up", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Angrist's earlier instrument, from 1990, was a real lottery. In the Vietnam era, "
            "birthdays were drawn at random to set the order of the draft. <bookmark mark='b'/> A low number made "
            "military service much more likely, so the lottery number is an instrument for being a veteran. <bookmark"
            " mark='c'/> The instrumental-variable analysis estimated that white men induced into service earned "
            "about fifteen percent less in the early nineteen-eighties than they would have without service. "
            "<bookmark mark='d'/> That effect belongs to the compliers, men who served because their number came up "
            "and otherwise would not have, not to volunteers or to those who avoided service anyway."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
